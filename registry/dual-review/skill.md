---
name: dual-review
description: Review a diff across two independent axes (Functional / Spec Verification vs. Code Quality & Maintainability) and present findings side-by-side.
---

# Dual-Perspective Code Review

Review the git diff since a fixed point (defaulting to the working tree against `HEAD`, or a specified branch/commit) from two completely separate evaluation perspectives.

## Perspective 1: Functional / Spec Verification

Evaluate the diff against the original requirement or task intent:
- **Missing Requirements**: What was asked for that was omitted or only partially built?
- **Unrequested Scope (YAGNI)**: Did the agent add unnecessary abstractions, speculative features, or unrelated edits?
- **Behavioral Regressions**: Could any altered function signatures or side effects break existing callers?

## Perspective 2: Code Quality & Maintainability

Evaluate the diff against clean code principles and repository rules:
- **Project Rule Compliance**: Does the diff follow `CLAUDE.md`, folder `CONTEXT.md`, and naming patterns?
- **Code Smells (Refactoring Checklist)**:
  - Long methods / functions doing more than one job.
  - Duplicated logic or boilerplate that standard libraries already solve.
  - Inconsistent error handling or swallow-all `except Exception` blocks.
  - Leaky abstractions or improper module boundaries.

## Reporting Format

Present the findings side-by-side or in two distinct sections:
```markdown
### Functional / Spec Verification
- [Pass/Fail/Caution]: [Finding summary]
  - Detail and recommended adjustment.

### Code Quality & Maintainability
- [Smell / Rule]: [File:Line]
  - Issue description and recommended refactor.
```
