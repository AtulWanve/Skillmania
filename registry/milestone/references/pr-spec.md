# PR Specification

Use this contract whenever authoring or reviewing pull request descriptions and managing task branches.

## Branch Workflow (Before Editing Code)

1. **Check Active Branch**: Before modifying files or committing, check the current git branch.
2. **Never Work on Default Branch**: Never commit or push changes directly to `main`.
3. **Confirm or Create Branch**:
   - If on `main`, ask the user if they have already created a branch for this task.
   - If not created, create a dedicated task branch: `task/issue-<N>-<short-slug>` (e.g., `task/issue-26-headless-verification`).
4. **Merge Strategy**: Use **Squash and Merge** on GitHub when merging the PR. This guarantees that `main` retains a clean, linear history where 1 commit equals 1 completed issue, with the PR summary preserved.

## Contract Structure

```markdown
## Summary
<!-- Concise overview of the changes and how they fulfill the issue goal -->

## Acceptance Criteria Verification
<!-- Check off each acceptance criterion from the issue -->
- [x] <Criterion 1 from issue verbatim>
- [x] <Criterion 2 from issue verbatim>

resolves #<issue-number>
```

## Critical Rules

1. **Issue Linking**: Include `resolves #<issue-number>` (or `closes #<issue-number>`, `fixes #<issue-number>`) as the strict final line of the PR body so GitHub automatically links and closes the issue upon merge.
2. **Acceptance Criteria 1:1 Mapping**: Every checklist item under `## Acceptance Criteria Verification` must map directly to the corresponding issue's acceptance criteria line for line. Check off the box (`- [x]`) using the issue's criteria text.
3. **No Appended Commentary or Test Dumps**: Do not append colon descriptions, explanations, or test counts to the checklist lines (for example, do NOT write `: 19/19 tests pass` or `: verified in diff`). The checked box (`- [x]`) is the verification. Do not add raw terminal output dumps or separate placeholder headers.

## Recommended Execution Commands
When providing git commands to commit and open a PR:
1. **Scoped Staging**: Always scope staging commands strictly to files relevant to this particular issue:
   `git add <file1> <file2>`
   Never suggest `git add .` or `git add -A` so unrelated, untracked, ignored, or historical milestone files are never swept into the commit.
2. **Commit Changes**:
   `git commit -m "<concise summary of changes>"`
   (Issue closure is handled automatically by the PR body's resolution link upon merge.)
3. **Push to Task Branch**:
   `git push -u origin task/issue-<issue-number>-<short-slug>`
