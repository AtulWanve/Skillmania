# Graph Updater

The Graph Updater is responsible for applying incremental structural changes to the graph files in `graph/`.

## Idempotency Contract

- The graph updater is strictly idempotent.
- Graph updates specify the nodes and edges to be added, removed, or modified.
- Operations like `addNode` or `addEdge` will not duplicate elements if they already exist with the same properties.
- Operations like `removeNode` or `removeEdge` will silently succeed if the element does not exist.
- If a synchronization job fails midway, restarting it will safely replay the operations without corrupting the graph state.
- Replays are keyed by `acceptedChange.idempotencyKey` (from the [[runtime/review-engine|Review Engine]]); re-running a completed or partially completed job yields the same final graph state without duplicating elements.

## Concurrency and Crash-Safety Guarantees

- **Writer serialization**: Every synchronization job acquires an advisory file lock on `graph/.graph-lock` (via `flock` / `LockFile`) before reading or writing any graph state, following the same lock-guarded protocol used by the [[runtime/memory-updater|Memory Updater]]. Acquisition uses a 5-second timeout; on timeout the job fails with `ConcurrentUpdateError` rather than proceeding concurrently. The lock is always released in a `try/finally` block.
- **Atomic snapshots**: Jobs never mutate the current snapshot in place. A new version directory (`graph/v-<timestamp>/`) is written through the atomic-write sequence (temp file → flush/fsync → rename), so every node and edge file is fully durable before it becomes visible.
- **Durability before publication**: `graph/manifest.json` is the single publication pointer. It is rewritten last, also atomically (temp file → flush/fsync → rename), and only after the entire new snapshot is durable. Readers therefore observe either the previous snapshot or the new one, never a partial mix.
- **Conflict handling**: An interrupted or overlapping job cannot leave partial state: a crash mid-write leaves the manifest pointing at the previous consistent snapshot, and leftover temporary directories are ignored (cleaned up by the next successful run). Conflicting concurrent updates fail with `ConcurrentUpdateError` and are retried as a whole: no update is silently dropped.
