---
title: Documentation Review
tags: [review, documentation, evaluation]
aliases: [Documentation Review]
---

# Documentation Review

## Scope

Evaluates whether the implementation is properly documented. See [[standards/documentation|Documentation Standards]] for the conventions this review checks against.

## Checklist

- [ ] Public APIs have JSDoc comments
- [ ] Memory files are updated if architecture changed
- [ ] Breaking changes are documented
- [ ] New environment variables are documented
- [ ] New dependencies are recorded
- [ ] No stale or misleading comments
- [ ] README updated if setup/usage changed

## Scoring

### Checklist Item States

Each checklist item is in one of the following states:

| State | Representation | Contribution |
|-------|---------------|--------------|
| Passed | `1` | Counts toward `checks-passed` and `total-applicable` |
| Failed | `0` | Counts toward `total-applicable` only |
| Partial credit | A decimal between 0 and 1 (e.g., `0.5`) | That value counts toward `checks-passed` and toward `total-applicable` |
| N/A (not applicable) | `"N/A"` | Excluded from both `checks-passed` and `total-applicable` |

### Score Formula

Score = `(checks-passed / total-applicable) × 100`, where `total-applicable` excludes N/A items. The result is rounded to the nearest integer (0.5 rounds up).

Threshold: `Blocking` is `true` when `score < 50`.

N/A (not applicable) items are excluded from the score denominator. If all items are N/A, the score is defined as `null` (no score) and `Blocking` is `false`. When `score` is `null`, the review is treated as passed for this dimension.

## Output

- Score (`number` 0-100, or `null` when all items are N/A)
- Missing documentation
- Recommendations
- Blocking: boolean (`true` when score < 50, `false` otherwise or when score is `null`)

> [!info] Results from all review types are aggregated by the [[runtime/review-engine|Review Engine]] as part of the eight canonical dimensions.
