---
title: Review Template
tags: [templates, review, evaluation]
aliases: [Review Template]
---

# <Review Type> Review

## Scope

What is being evaluated. See concrete review types: [[reviews/architecture-review|Architecture]], [[reviews/code-quality|Code Quality]], [[reviews/documentation-review|Documentation]], [[reviews/performance-review|Performance]], [[reviews/security-review|Security]].

## Checklist

- [ ] Item 1
- [ ] Item 2
- [ ] Item 3

## Findings

Each finding is a structured object:

| Field | Type | Description |
|-------|------|-------------|
| `description` | `string` | Brief description of the issue |
| `severity` | `"critical" \| "high" \| "medium" \| "low"` | Impact severity |
| `category` | `"architecture" \| "maintainability" \| "readability" \| "intent" \| "side-effects" \| "scalability" \| "regression" \| "security"` | Dimension category |
| `recommendation` | `string` | Suggested remediation |

## Score

| Field | Type | Description |
|-------|------|-------------|
### Aggregation Rules

- `overallScore` = weighted average of per-category scores: `Σ(score_i × weight_i)`, with weights normalized to sum to 1.
- Dimensions with all N/A items are excluded from the weighted average (their weight is redistributed proportionally across remaining dimensions).
- `blocking` is `true` if **any** dimension's blocking threshold is triggered, regardless of overall score. Blocking takes precedence over score thresholds.
- `accepted` = `!blocking && overallScore >= 90`. When `accepted` is `false`, escalation rules apply: if `retryCycle < 3`, return for improvement; otherwise escalate.
- `acceptedChange` **must** be non-null when `accepted === true` and `null` when `accepted === false`.

| Field | Type | Description |
|-------|------|-------------|
| `overallScore` | `number` (0-100) | Aggregate quality score (weighted average) |
| `dimensionScores` | `{ category: string; score: number; weight: number; notes: string }[]` | Per-dimension breakdown; each weight is 0.0-1.0, all weights sum to 1 |
| `blocking` | `boolean` | `true` if any blocking threshold is triggered |
| `accepted` | `boolean` | `!blocking && overallScore >= 90` (canonical threshold) |
| `acceptedChange` | `AcceptedChange \| null` | Approved change payload (non-null when accepted, null when rejected) |
| `retryCycle` | `number` (0-3) | Current retry attempt (0 = first pass) |
| `escalation` | `{ required: boolean; reason: string \| null }` | Whether human escalation is needed and why |
| `feedback` | `string` | Human-readable review summary |

### AcceptedChange Shape

```typescript
interface AcceptedChange {
  idempotencyKey: string;                               // UUID for safe retry
  taskId: string;                                       // Stable task identifier
  graphDiff: { nodes: NodeDiff[]; edges: EdgeDiff[] };  // Incremental graph changes
  memoryAppend: { targetFile: string; content: string }[]; // Memory file append operations
}
```

- `NodeDiff` and `EdgeDiff` types are defined in the [[runtime/graph-updater|Graph Updater]] contract.
- `acceptedChange` is `null` when `accepted` is `false`: consumers ([[runtime/graph-updater|Graph Updater]], [[runtime/memory-updater|Memory Updater]]) **must** check for `null` before accessing fields.

> [!info] The [[runtime/review-engine|Review Engine]] implements the score aggregation and acceptance logic defined in this template. See [[runtime/confidence-engine|Confidence Engine]] for the scoring model.
