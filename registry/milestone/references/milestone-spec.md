# Milestone Specification

Use this contract to define, track, and verify project milestones.

## Milestone Definition Schema

Each phase milestone (e.g., M0, M1, M2) is documented and tracked as a checked-in repository file at `docs/milestones/M<N>-<name>.md`. This keeps milestone status, issue checklists, and acceptance criteria transparent, version-controlled, and accessible without requiring external API tokens or CLI tools.

### Phase Decomposition (1 Milestone : N Discrete Tasks)
Decompose each milestone into small, incremental task issues (Issues #1 through #N). Each task issue represents one isolated capability or verification step, resolved by its own pull request.

```markdown
# Milestone M0: <Phase Name>

## Objective
<!-- High-level outcome this phase delivers -->

## Scope & Issues
- [ ] Issue #1: <Task Title>
- [ ] Issue #2: <Task Title>
- [ ] Issue #3: <Task Title>

## Acceptance Criteria
<!-- Mandatory criteria that must be satisfied before this milestone is closed -->
This milestone is COMPLETE only when:
1. All phase issues (#1 through #N) have passed their individual acceptance criteria.
2. The entire automated test suite passes with zero regressions.
3. All scope restrictions across phase issues were preserved.

<!-- CONDITIONAL: Include ## Downstream Transition only when downstream milestones are planned. Omit entirely if subsequent phases are not yet defined. -->
## Downstream Transition
- **Next Milestone**: M1: <Next Phase Name>
- **Prerequisites**: M1 tasks cannot be merged until M0 Acceptance Criteria pass.
```

## Verification Rollup

Issues, pull requests, and milestones connect across three levels:

1. **Issue Acceptance**: Every task issue states the milestone acceptance criteria it contributes to, along with its specific binary acceptance criteria and scope restrictions.
2. **PR Verification**: Every PR resolves one issue, verifying that issue's acceptance criteria and certifying zero anti-goals were breached.
3. **Milestone Closeout**: The milestone phase closes only when every issue on its checklist is resolved and verified. No work from the subsequent phase may merge until the current milestone's acceptance criteria pass.
4. **Milestone Document Lifecycle & Immutability**: The milestone tracking document (`docs/milestones/M<N>-<name>.md`) is committed twice per milestone: initially during Issue #1 to establish baseline scope, and finally during the final capstone issue (#N) to record criteria verification and close the phase. Intermediate issues must not stage or commit the milestone document. Once closed, the milestone document is sealed and immutable; any changes to closed milestone files during later milestones must not be staged or committed into feature PRs. If historical milestone edits are genuinely needed, handle them in a discrete maintenance milestone.
