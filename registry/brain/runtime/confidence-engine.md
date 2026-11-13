---
title: Confidence Engine
tags: [runtime, confidence, scoring, quality]
aliases: [ConfidenceEngine, Phase 14]
---

# Confidence Engine (Phase 14)

Every accepted implementation receives quantitative scoring. Runs after [[runtime/review-engine|Review Engine]].

## Scoring Dimensions

Dimensions and weights match Phase 14 engineering disciplines and the [[runtime/review-engine|Review Engine]].

| Category | Weight |
|----------|--------|
| Architecture | 1/8 |
| Performance | 1/8 |
| Security | 1/8 |
| Naming | 1/8 |
| Documentation | 1/8 |
| Testing | 1/8 |
| Maintainability | 1/8 |
| Readability | 1/8 |

Weights sum to 1 (8 × 1/8 = 1).

### Normalization

Each dimension is scored 0-100. The overall score is a **weighted arithmetic mean**:

```
overallScore = Σ(score_i × weight_i) / Σ(weight_i)
```

When all dimensions are applicable (none are N/A) and weights sum to 1, this simplifies to `Σ(score_i × weight_i)`.

### N/A Dimension Handling

When a dimension is marked N/A (not applicable), it is excluded from the calculation:

1. Remove all N/A dimensions from the `scores` array.
2. Redistribute the remaining weights so they sum to 1: `adjusted_weight_i = weight_i / Σ(applicable_weights)`.
3. Compute `overallScore = Σ(score_i × adjusted_weight_i)`.

If all dimensions are N/A, the overall score is defined as `null` and `accepted` is `false` (there are no scored dimensions to evaluate).

## Acceptance Threshold

Acceptance follows the canonical gate defined in the [[runtime/review-engine|Review Engine]], guarded so a `null` score (all-N/A) is never accepted: `overallScore !== null && !blocking && overallScore >= 90`.

- `overallScore !== null && !blocking && overallScore >= 90`: accepted
- `overallScore === null || blocking || overallScore < 90`: improve → review again

## Scoring Rules

- Each dimension scored 0-100
- Overall score is weighted average (see Normalization above)
- Scores are derived from review results
- Scores persist in task history for trend analysis

## Retry Logic

- If `overallScore === null || blocking || overallScore < 90` (i.e., not accepted): return to execution with improvement instructions
- Maximum 3 review cycles per task
- After 3 failures: escalate to human review

> [!note] Retry state is coordinated by the [[runtime/orchestrator|Orchestrator]]. The confidence score is also recorded in [[tasks/completed|Completed Tasks]].
