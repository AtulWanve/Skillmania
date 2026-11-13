---
name: milestone
description: Scaffold, plan, and execute milestone workflows with task specifications, CI workflows, and resolution-linked PRs.
---

# Milestone Workflow & Execution

Standardized project structure, milestone phases, task specifications, and pull request workflows.

## Milestone Lifecycle
Organize work into sequential milestone phases (M0, M1, M2). Break each milestone into small, single-objective task issues (Issues #1 through #N). A milestone closes only after all designated issues pass their individual acceptance criteria.

## Quick Start Lifecycle Sequence
For a complete end-to-end walkthrough, see `references/example-cycle.md`.
1. **Scaffold (`/milestone scaffold`)**: Deploy repo contracts (`.github/ISSUE_TEMPLATE.md`, `.github/pull_request_template.md`, `.github/workflows/ci.yml`).
2. **Plan (`/milestone plan`)**: Define milestone scope and breakdown into multiple small task issues in `docs/milestones/M<N>-<name>.md`.
3. **Issue (`/milestone issue`)**: Create small, focused task issues for the milestone, each containing binary acceptance criteria, test reuse tasks, and binding scope restrictions.
4. **Branch & PR (`/milestone pr`)**: Confirm or create dedicated task branch (`task/issue-<N>-<slug>`), author PR verifying acceptance criteria and anti-goals, ending with issue resolution link (`resolves #<issue-number>`).
5. **Close Milestone**: Merge PR via Squash & Merge (1 clean commit per issue on `main`), verify all milestone issues pass, CI turns green, and advance to the next milestone.

---

## Operating Modes
Invoked explicitly via `/milestone <mode>` or triggered automatically when authoring milestones, tasks, PRs, or repository scaffolding:

### 1. Scaffolding (`/milestone scaffold`)
Deploys standardized repo hygiene and contract templates to the repository (see `references/ci-workflow-spec.md`):
- `.github/ISSUE_TEMPLATE.md` (or `task.md`): Enforces goals, structured task checklists, binary acceptance criteria, scope restrictions, and milestone completion criteria (bypasses template chooser on single-template repos).
- `.github/pull_request_template.md`: Audits acceptance criteria, audits anti-goals, and links to issue resolution.
- `.github/workflows/ci.yml`: Standard GitHub Actions workflow running automated tests and linters.

### 2. Milestone Planning (`/milestone plan`)
Defines or audits milestone boundaries (see `references/milestone-spec.md`):
- Establishes phase goals and numerical scope in `docs/milestones/M<N>-<name>.md`.
- Sets the **Milestone Acceptance Criteria**: the explicit checklist of issues that must pass acceptance criteria to complete the phase.
- Documents downstream milestones if planned; omitted if subsequent phases are not yet defined.

### 3. Issue Specification (`/milestone issue`)
Authors or reviews task issues against the task specification (see `references/issue-spec.md`):
- **Goal**: A single, unambiguous, verifiable objective.
- **Tasks**:
  - `Core Implementation`: Targeted functional requirements and behavioral capabilities.
  - `Automated Tests & Regression Checks`: Reusing existing tests, writing missing coverage, verifying deterministic outputs, and verifying passing test output with zero regressions.
  - `Documentation`: Updating project docs when deliverables alter APIs, configuration, schema, or known boundaries.
- **Acceptance Criteria**: Strict binary (pass/fail) conditions required to close the issue.
- **Scope Restrictions (Anti-Goals)**: Explicit guardrails specifying what must NOT be built or introduced (guards against premature abstractions and scope creep).
- **Open Contract Invariant**: Task and acceptance criteria checklists in an issue must be unchecked (`- [ ]`). Scope restrictions must use plain bullet points (`-`), never checkboxes. Checked boxes (`- [x]`) belong exclusively in Pull Request verification.
- **Milestone Completion (Conditional)**: Included ONLY on the final capstone/verification issue (#N) of the milestone. Omitted on intermediate issues (#1 through #N-1).

### 4. PR Verification & Branch Workflow (`/milestone pr`)
Drafts or reviews PR bodies and enforces branch hygiene (see `references/pr-spec.md`):
- **Branch Check**: Never commit directly to `main`. If on `main`, ask user if branch already exists for this task; if not, create `task/issue-<N>-<short-slug>`.
- **Summary**: Concise overview matching the issue's goal.
- **Criteria Verification**: Verifies each acceptance criterion from the issue with checked boxes (`- [x]`) without appending colon explanations or test counts.
- **Issue Linking**: Ends with `resolves #<issue-number>` (or `closes #<issue-number>`, `fixes #<issue-number>`) as the strict final line so GitHub links and closes the issue upon merge.
- **Merge Strategy**: Recommends Squash & Merge on GitHub for a clean, linear commit history on `main`.
- **Scoped Command Generation**: When providing git commands, always output explicit, issue-scoped commands:
  - Branch: `git checkout -b task/issue-<N>-<short-slug>`
  - Scoped Staging: `git add <issue-relevant-files>` (only add files relevant to this particular issue; never suggest `git add .` or blanket staging; ensure non-issue files, uncommitted work, and historical milestone documents are excluded)
  - Commit: `git commit -m "<concise summary of changes>"`
  - Push: `git push -u origin task/issue-<N>-<short-slug>`

---

## Verification Rollup

Verification connects across three levels:
1. **Issue Level**: Tasks enforce binary acceptance criteria and binding scope restrictions. The final milestone issue (#N) audits that all prior milestone tasks passed.
2. **PR Level**: Verifies all issue criteria, linking issue closure upon merge.
3. **Milestone Level**: The milestone phase cannot close until 100% of its designated issues are resolved and the full test suite passes with zero regressions. Subsequent milestone work cannot merge until the prior milestone's acceptance criteria pass.

---

## Operating Rules

1. **Anti-Goals Are Binding**: If code touches an item listed under Scope Restrictions, it must be rejected or the issue specification renegotiated.
2. **Binary Verification**: Acceptance criteria must never be subjective. Each criterion must be provable via running tests or inspection.
3. **Test Reuse First**: Always reuse existing tests before introducing new test suites or harnesses.
4. **Branch Isolation**: Never commit directly to default branch `main`. Check active branch and ask user before creating `task/issue-<N>-<slug>`.
5. **No AI Attribution / Fingerprints**: Avoid em dashes; use hyphens, colons, or parentheses.
6. **One PR Resolves One Issue**: Pull requests map 1:1 to task issues. Multi-issue batches compromise isolation and are prohibited.
7. **Violation Enforcement**: When reviewing a PR, if any acceptance criterion fails or an anti-goal is breached, halt approval immediately, report the breach, and request corrective changes. Scope renegotiation requires explicit user approval.
8. **Zero Skill Branding**: Do not brand generated artifacts, commit messages, PR descriptions, issues, or milestones with skill names, process trademarks, or internal jargon (e.g., 'phase-task', 'phase-gate', 'completion gate'). Use plain, industry-standard engineering terminology (e.g., 'task', 'milestone', 'acceptance criteria', 'prerequisites').
9. **Scoped Staging & Open Contracts**: Issue checklists must strictly use unchecked boxes (`- [ ]`), while scope restrictions use plain bullet points (`-`). Pull requests verify criteria by checking off the box (`- [x]`) without appending colon commentary or test counts. When providing git commands, always scope `git add` to only files relevant to this particular issue to protect uncommitted or non-issue work from leaking into the PR; never suggest blanket staging (`git add .`, `git add -A`) or staging untracked/ignored metadata.
10. **Milestone Document Commit Timing**: The milestone tracking document (`docs/milestones/M<N>-<name>.md`) is committed twice per milestone:
    - First in Issue #1 with unchecked boxes (`- [ ]`) to establish the baseline scope.
    - Finalized in the final capstone issue (#N) to record criteria verification (`- [x]`) and close the milestone.
    - Intermediate issues (#2 through #N-1) must only stage and commit files relevant to their specific task, and must not stage or commit the milestone tracking document.
11. **Closed Milestone Immutability**: Once a milestone is closed, its tracking document is sealed and read-only.
    - If a closed milestone document is modified on disk during work on later milestones, do not stage or commit those changes into active issue PRs. Only commit files relevant to the active issue.
    - If edits to closed milestone documents are genuinely required, handle them in a discrete, dedicated maintenance milestone rather than bundling them into active feature work.
