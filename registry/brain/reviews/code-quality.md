---
title: Code Quality Review
tags: [review, code-quality, maintainability]
aliases: [Code Quality Review]
---

# Code Quality Review

## Scope

Evaluates code quality, maintainability, and adherence to project standards. See also [[reviews/architecture-review|Architecture Review]], [[reviews/documentation-review|Documentation Review]], [[reviews/performance-review|Performance Review]], and [[reviews/security-review|Security Review]].

## Checklist

- [ ] Follows [[standards/typescript|TypeScript]]/[[standards/react|React]]/[[standards/nextjs|Next.js]] standards
- [ ] Proper error handling (no swallowed errors)
- [ ] No dead code or commented-out code
- [ ] Consistent naming conventions (see [[standards/naming|Naming Standards]])
- [ ] Functions are focused (single responsibility)
- [ ] No excessive complexity (consider extracting)
- [ ] Proper typing (no `any` abuse)
- [ ] Tests are meaningful and cover edge cases
- [ ] No debug artifacts (console.log, debugger)

## Scoring

### Checklist Item States

Each checklist item is in one of the following states (aligned with the architecture rubric):

| State | Representation | Contribution |
|-------|---------------|--------------|
| Passed | `1` | Counts toward `checks-passed` and `total-applicable` |
| Failed | `0` | Counts toward `total-applicable` only |
| Partial credit | A decimal between 0 and 1 (e.g., `0.5`) | That value counts toward `checks-passed` and toward `total-applicable` |
| N/A (not applicable) | `"N/A"` | Excluded from both `checks-passed` and `total-applicable` |

### Score Formula

Score = `(checks-passed / total-applicable) × 100`, where `total-applicable` excludes N/A items.

If all items are N/A, the score is defined as `null` (no score), `Blocking` is `false`, and the review is treated as passed for that dimension.

Threshold: score < 60 sets `Blocking: true`. Any single issue classified as "Critical" in the Issues found section also sets `Blocking: true` regardless of the aggregate score.

## Output

- Score (0-100)
- Issues found (each classified as Critical or Minor)
- Recommendations
- Blocking: boolean (true when score < 60 or any Critical issue is present)
