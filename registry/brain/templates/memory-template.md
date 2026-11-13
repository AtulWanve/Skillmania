---
title: Memory Template
tags: [templates, memory, records]
aliases: [Memory Record Template]
---

# Memory Record

Structured record appended to the memory file after an accepted change. Consumed by the [[runtime/memory-updater|Memory Updater]].

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `memoryKey` | `string` (UUID) | Yes | Stable unique identifier for this memory record |
| `sourceTaskId` | `string` (UUIDv4) | Yes | Planner-assigned UUIDv4 for the task that produced this memory. This is the canonical deduplication identifier: the [[runtime/memory-updater|Memory Updater]] writes it as `<!-- taskId: <sourceTaskId> -->` in the record and scans for that marker when checking for duplicates. Retries use this same field for idempotency. |
| `timestamp` | `string` (ISO-8601 UTC) | Yes | When the record was created |
| `confidence` | `number` (0-100) | Yes | Confidence score from [[runtime/confidence-engine|Confidence Engine]] |
| `affectedGraphNodes` | `string[]` | Yes | IDs of graph nodes affected by the change |
| `content` | `string` | Yes | Free-form memory content |
| `deduplicationKey` | `string` | No | Optional secondary hash or logical key for additional deduplication beyond `sourceTaskId`. The primary deduplication mechanism is the `<!-- taskId: <sourceTaskId> -->` marker. If `deduplicationKey` is present, the updater checks for it as a secondary constraint after the primary taskId check passes. |

## Record Format (YAML front-matter + body)

```markdown
---
memoryKey: "uuid-here"
sourceTaskId: "task-uuid"
timestamp: "2026-07-10T12:00:00Z"
confidence: 95
affectedGraphNodes: ["module:auth", "api:login"]
deduplicationKey: "auth-login-flow-v3"
---
<!-- taskId: task-uuid -->

Record content in markdown...
```

The `---` delimiters separate YAML front matter (metadata) from the markdown body. Metadata fields (`memoryKey`, `sourceTaskId`, `timestamp`, `confidence`, `affectedGraphNodes`, `deduplicationKey`) are in the YAML block. The `content` field is **not** a YAML key: it is the entire markdown body after the closing `---`. Parsers **must** read the body after the second `---` as the record content.

> [!warning] This is a per-record frontmatter, not the file-level frontmatter. The `---` blocks inside records are nested YAML: parsers must handle multiple records per file, each with its own `---` delimiters.

## Deduplication (Lock-Guarded Protocol)

The [[runtime/memory-updater|Memory Updater]] uses a single normative concurrency protocol:

1. **Acquire lock**: Obtain an advisory file lock on `memory/.memory-lock` (via `flock` / `LockFile`).
2. **Timeout**: The lock acquisition has a 5-second timeout. If the lock cannot be acquired within this period, fail with `ConcurrentUpdateError`.
3. **Read/check/append while holding the lock**: While the lock is held, scan the target memory file for an existing `<!-- taskId: <id> -->` marker (using `sourceTaskId`). If found, release the lock and skip (idempotent retry). If not found, proceed to the atomic-write sequence (temp file → flush → rename).
4. **Release lock**: Release the lock only after the rename succeeds or after any failure (using try/finally to guarantee release).

This single protocol replaces any alternative concurrency mechanisms. The unconstrained read-then-append flow (check all records, then append if not found) is **not safe** under concurrency and must not be used.

### Secondary Deduplication (Optional)

When `deduplicationKey` is set (in addition to `sourceTaskId`), the updater checks for an existing record with a matching `deduplicationKey` in the YAML front matter **after** the primary `sourceTaskId` check finds no match (i.e., no duplicate by taskId). If a record with the same `deduplicationKey` is found, even if it belongs to a different `sourceTaskId`, the updater treats it as a duplicate and skips (idempotent behavior). This prevents the same logical change from being recorded multiple times under different task identifiers. Both checks occur while holding the advisory lock.

### Graph Synchronization

Each record's `affectedGraphNodes` links back to the graph state, enabling cross-referencing between memory and graph updater contracts. See [[runtime/graph-updater|Graph Updater]] for the graph schema.
