# Task Issue Specification

Use this specification whenever authoring, reviewing, or breaking down tasks and issues. Use directly as task markdown or deploy to `.github/ISSUE_TEMPLATE.md` to open pre-filled issue templates on GitHub.

## Contract Structure

```markdown
## Goal
<!-- Single, verifiable objective for this task -->

## Tasks
### Core Implementation
- [ ] <Task item 1>
- [ ] <Task item 2>

### Automated Tests & Regression Checks
- [ ] Reuse existing tests wherever possible; add only missing test coverage
- [ ] Add or update automated tests covering new behavior
- [ ] Verify deterministic execution where applicable
- [ ] Run automated test suite and observe passing output with zero regressions

### Documentation
<!-- Include only when deliverables change user-facing behavior, APIs, schemas, or configs. Omit this section entirely if documentation is unchanged. -->
- [ ] Update API specs, schema, or configuration
- [ ] Document known boundaries or limitations

## Acceptance Criteria
<!-- Concrete, binary pass/fail conditions verifiable by running tests or inspection. Define 2-5 task-specific deliverables; never leave generic placeholders. -->
- [ ] <Specific functional outcome verifiable in code or behavior>
- [ ] <Specific automated test covering new behavior passes>
- [ ] Full existing test suite passes with zero regressions

## Scope Restrictions
<!-- Explicit anti-goals specifying what must NOT be built or touched. Use plain bullet points (-), NEVER checkboxes (- [ ]). -->
- Do not <specific out-of-scope feature, abstraction, or dependency>
- Do not <unapproved file, layer, or module to modify>

<!-- CONDITIONAL: Include ## Milestone Completion ONLY on the final capstone/verification issue (#N) of the milestone. Omit on all intermediate issues (#1 through #N-1). -->
## Milestone Completion
<!-- Final capstone issue only: audits that all phase issues have passed -->
- Milestone M<N> is COMPLETE only after Issues #1 through #N pass acceptance criteria.
```

## Open Contract Invariants

1. **Checklists Use Unchecked Boxes (`- [ ]`), Anti-Goals Use Plain Bullets (`-`)**: Task and acceptance criteria items MUST use unchecked checkboxes (`- [ ]`). Scope restrictions (anti-goals) are negative boundaries and MUST use plain bullet points (`- Do not...`), never checkboxes. Checked boxes (`- [x]`) are prohibited in issues and belong exclusively in Pull Request verification.
2. **Functional Requirements Over File Edits**: An issue defines what must be achieved (functional requirements, expected behaviors, acceptance criteria, anti-goals), not an internal execution walkthrough or patch list. Even when code is already implemented or partially written:
   - Do NOT list specific source file paths, line numbers, or internal function names in task checklists (e.g., write "Validate authorization token expiration", not "Edit `src/auth/jwt.py` line 42").
   - Do NOT paste code diffs, patches, or terminal dumps into the issue.
   - Describe capabilities from the caller, consumer, or system boundary perspective so the issue remains a durable specification rather than an implementation script.
3. **Deliverables vs Routine Development Operations**: Tasks and acceptance criteria must track codebase deliverables (functional code, automated test suites, schema or API updates). Routine development workflow operations (running linters, formatters, typechecks, code review bots, or CI checks) belong to PR gates and must never appear as issue tasks or acceptance criteria.

## Section Requirements

### 1. Goal
A single, unambiguous statement declaring what this task achieves. Avoid vague statements like "improve performance" or "refactor code".

### 2. Tasks
Organized by execution phases:
- **Core Implementation**: Targeted functional requirements and behavioral capabilities. Describe what the system must do without referencing specific source file paths, line numbers, or internal code identifiers.
- **Automated Tests & Regression Checks**: Mandates test reuse, new coverage, deterministic output checks, and observing passing test suite output.
- **Documentation**: Updates to APIs, schemas, configurations, or operational boundaries (when applicable).

### 3. Acceptance Criteria
Binary pass/fail statements tailored to the specific functional deliverables of this task. Do not leave generic placeholder statements. Every criterion must be a concrete condition verifiable by running tests or inspecting deliverables.

### 4. Scope Restrictions (Anti-Goals)
Explicit negative guardrails stating what must NOT be implemented in this issue. Always format as plain bullet points (`- Do not...`), never checkboxes. This protects against scope creep and premature abstraction.

### 5. Milestone Completion (Conditional: Final Milestone Issue Only)
- **Intermediate Issues (#1 through #N-1)**: Omit this section entirely. Intermediate issues focus purely on their isolated task goals and scope restrictions.
- **Final Capstone / Verification Issue (#N)**: Must include this section. As the closing issue of the milestone, it audits that all preceding issues in the phase passed and verifies zero regressions.
