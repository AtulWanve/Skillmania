---
title: Performance Review
tags: [review, performance, optimization]
aliases: [Performance Review]
---

# Performance Review

## Scope

Evaluates performance implications of the implementation. See [[standards/performance|Performance Standards]] for the guidelines this review checks against.

## Checklist

- [ ] No unnecessary re-renders introduced
- [ ] Bundle size impact is acceptable
- [ ] Network requests are optimized (batching, caching)
- [ ] Database queries are indexed and paginated
- [ ] No N+1 query patterns introduced
- [ ] Lazy loading used where appropriate
- [ ] Memoization applied correctly
- [ ] No expensive computations on render path

Items that do not apply to the change under review should be marked as `N/A` instead of pass or fail. N/A items are excluded from the score denominator. Score is calculated as `(checks-passed / (total-checks - N/A-checks)) × 100`.

If **all** items are marked `N/A`, the score is defined as `null` (no score), `Blocking` is `false`, and the review is treated as passed for that dimension. No manual review or escalation is required for an all-N/A performance review.

## Scoring

Score: 0-100

Threshold: score < 60 sets `Blocking: true`; score >= 60 sets `Blocking: false`. When all items are N/A, the score is defined as `null`, `Blocking` is `false`, and the review is treated as passed for this dimension (already stated above).

## Output

- Score (0-100, or `null` when all items are N/A)
- Issues found
- Recommendations
- Blocking: boolean (derived: `true` when score is not null and score < 60; `false` when score >= 60 or score is `null`)

> [!info] This review contributes to the "Performance" dimension in the [[runtime/review-engine|Review Engine]]'s eight canonical categories.
