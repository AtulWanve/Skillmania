---
title: Review Engine
tags: [runtime, review, evaluation, quality]
aliases: [ReviewEngine, AI Review]
---

# Review Engine

Evaluates implementation quality after [[runtime/static-validator|Static Validator]] passes. Feeds into [[runtime/confidence-engine|Confidence Engine]].

## Structured Output Contract

### Schema

Returns a `ReviewResult` object:

| Field | Type | Description |
|-------|------|-------------|
| `overallScore` | `number` (0-100) | Aggregate quality score |
| `scores` | `ReviewDimension[]` | Per-category scores |
| `blocking` | `boolean` | If true, the change is rejected |
| `reviewRequired` | `boolean` | Propagated unchanged from [[runtime/task-classifier\|Task Classification]]. |
| `accepted` | `boolean` | Derived: `!blocking && overallScore >= 90` (canonical threshold, consistent with [[runtime/confidence-engine|Confidence Engine]]) |
| `acceptedChange` | `AcceptedChange \| null` | Approved change payload. **Must** be non-null when `accepted` is `true`; **must** be `null` when `accepted` is `false` (i.e., when rejected). Consumers ([[runtime/graph-updater|Graph Updater]], [[runtime/memory-updater|Memory Updater]]) **must** validate this invariant. |
| `feedback` | `string` | Human-readable review summary |

### Score Meanings (`ReviewDimension`)

| Field | Type | Range |
|-------|------|-------|
| `category` | `string` | One of the eight canonical categories: `"architecture"`, `"security"`, `"maintainability"`, `"readability"`, `"intent"`, `"side-effects"`, `"scalability"`, or `"regression"` |
| `score` | `number` | 0-100 |
| `weight` | `number` | 0.0-1.0 (default 1/8 = 0.125 per category; weights **must** sum to 1) |
| `notes` | `string` | Justification |

The `scores` array **must** contain exactly one entry for each of the eight canonical categories: no duplicates, no omissions. Each `score` must be 0-100, each `weight` must be 0.0-1.0, and weights must sum to exactly 1 (within floating-point tolerance). Consumers **must** reject arrays that violate these constraints.

### Blocking Thresholds

- Any single `score` < 40 sets `blocking = true`.
- `overallScore` is the weighted average of per-category scores.
- `overallScore` < 50 sets `blocking = true`.
- `accepted` (for downstream confidence scoring) also requires `overallScore >= 90`.
- Overall the canonical acceptance gate is: `!blocking && overallScore >= 90`.

> [!warning] These thresholds are the canonical rules. Consumers - especially [[runtime/graph-updater|Graph Updater]] and [[runtime/memory-updater|Memory Updater]] - MUST recompute and validate them independently before processing.

### Accepted Change (`AcceptedChange`)

| Field | Type | Description |
|-------|------|-------------|
| `idempotencyKey` | `string` | UUID for safe retry (consumed by [[runtime/graph-updater|Graph Updater]]) |
| `taskId` | `string` | Stable task identifier (consumed by [[runtime/memory-updater|Memory Updater]]) |
| `graphDiff` | `{ nodes: NodeDiff[]; edges: EdgeDiff[] }` | Incremental graph changes |
| `memoryAppend` | `{ targetFile: string; content: string }[]` | Memory file append operations |

### Consumer Integration and Validation

- **[[runtime/graph-updater|Graph Updater]]** reads `acceptedChange.idempotencyKey` and `acceptedChange.graphDiff`.
- **[[runtime/memory-updater|Memory Updater]]** reads `acceptedChange.taskId` and `acceptedChange.memoryAppend`.
- Both receive the full `ReviewResult` and **must** recompute and validate these invariants before processing `acceptedChange`:
  1. **Recompute `overallScore`** from the weighted `scores` array using `Σ(score_i × weight_i) / Σ(weight_i)`. Reject the result if the recomputed value differs from the provided `overallScore` by more than floating-point tolerance (1e-9).
   2. **Validate ranges and category set**: Every `score` in `scores` must be 0-100, every `weight` must be 0.0-1.0, and weights must sum to exactly 1 (within 1e-9 tolerance). The `scores` array must contain exactly one entry for each of the eight canonical categories (`"architecture"`, `"security"`, `"maintainability"`, `"readability"`, `"intent"`, `"side-effects"`, `"scalability"`, `"regression"`): no duplicates, no omissions. The `overallScore` must be 0-100 after recomputation.
  3. **Validate blocking thresholds**: Set `blocking = true` if any single `score` < 40 or if `overallScore` < 50. Reject if the provided `blocking` field contradicts this derivation.
  4. **Recompute `accepted`** as `!blocking && overallScore >= 90`. Reject if the provided `accepted` field contradicts this derivation.
  5. **Enforce the acceptedChange invariant**: `acceptedChange` must be non-null when `accepted` is `true` and `null` when `accepted` is `false`. Reject malformed results before processing.
- **External Skill Findings**: Findings from external audit tools (such as `test-audit` or `security-review`) must be mapped into the notes and scores of the eight canonical categories. They cannot introduce custom top-level fields or bypass acceptance thresholds. See [[standards/skills|External Skill Standards]].
- If any validation fails, the consumer must treat the result as invalid and not apply any changes.
