# Memory Updater

The Memory Updater is responsible for applying incremental updates to the modular memory files in `memory/`.

## Idempotency Contract

- The memory updater operates idempotently by using task IDs and content hashes as update anchors.
- Before applying an update, it checks if the exact same change has already been applied for the given task.
- Partial updates are designed so that re-applying them over a partially updated file results in the same final state.
- Updates are strictly incremental.
- Task IDs and content hashes serve as deduplication anchors only; they do not replace the concurrency and durability guarantees below.

## Concurrency and Crash-Safety Guarantees

- **Writer serialization**: Every update acquires an exclusive advisory file lock on `memory/.memory-lock` before reading or writing any memory file. Acquisition uses a 5-second timeout; on timeout the update fails with `ConcurrentUpdateError` rather than proceeding concurrently.
- **Read-modify-write under lock**: Reading the current memory file, detecting conflicts against it, and writing the merged result all happen while the lock is held, so no two updates can interleave their modify steps.
- **Conflict detection**: If the file changed since the updater last observed it (stale read), the update fails with `ConcurrentUpdateError` and is retried as a whole: appended changes are never silently dropped.
- **Atomic replacement**: Updates never mutate a memory file in place. The new content is written to a temporary file, flushed and fsynced, then renamed over the target path, so readers see either the previous content or the new content, never a partial mix.
- **Durability before release**: The lock is always released in a `try/finally` block, and only after the renamed file is durable. A crash mid-write leaves the previous intact content; leftover temporary files are ignored and cleaned up by the next successful run.
