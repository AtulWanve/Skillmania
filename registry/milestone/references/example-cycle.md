# End-to-End Milestone Lifecycle Walkthrough

This reference demonstrates a complete cycle through the milestone lifecycle: Milestone -> Issue -> PR -> Milestone Closure.

---

## Step 1: Milestone Definition (`docs/milestones/M0-foundation.md`)
Demonstrates milestone decomposition into multiple small, incremental task issues:

```markdown
# Milestone M0: Foundation Execution

## Objective
Establish and verify the core headless execution engine without GUI dependencies.

## Scope & Issues
- [ ] Issue #24: Implement Headless State Transitions
- [ ] Issue #25: Implement Event Ordering and Serialization
- [ ] Issue #26: Verify Headless Foundation Execution

## Acceptance Criteria
This milestone is COMPLETE only when:
1. All phase issues (Issues #24, #25, and #26) pass their individual binary acceptance criteria.
2. Full automated test suite passes with zero regressions.
3. All scope restrictions (no GUI, no renderer) were preserved across all issues.

<!-- CONDITIONAL: Include ## Downstream Transition only when downstream milestones are planned. Omit if subsequent phases are not yet defined. -->
## Downstream Transition
- **Next Milestone**: M1: Scratch Renderer and Human Input
- **Prerequisites**: M1 tasks cannot be merged until M0 Acceptance Criteria pass.
```

---

## Step 2: Task Issue (`Issue #26` - Final Capstone Verification Task in M0)
*(Note: Intermediate Issues #24 and #25 omitted the `## Milestone Completion` section. It is included here specifically because Issue #26 is the final closing verification task of Phase M0.)*

```markdown
## Goal
Verify that the complete engine foundation works correctly without GUI or renderer dependencies.

## Tasks
### Core Implementation
- [ ] Run headless environment without opening a window
- [ ] Verify reset(), step(), legal_actions(), and is_terminal()
- [ ] Verify state transitions and event serialization

### Automated Tests & Regression Checks
- [ ] Reuse existing tests wherever possible; add only missing test coverage
- [ ] Add headless execution smoke test
- [ ] Verify deterministic outputs across repeated runs
- [ ] Run automated test suite and observe passing output with zero regressions

### Documentation
- [ ] Document known boundaries and limitations

## Acceptance Criteria
- [ ] Complete episode runs headless without GUI
- [ ] State transitions verified
- [ ] Deterministic execution passes
- [ ] Full existing test suite passes with zero regressions
- [ ] No renderer or HUD code added
- [ ] No AI planning or learning introduced

## Scope Restrictions
- Do not implement renderer or HUD.
- Do not implement AI planning or learning.
- Do not introduce unnecessary dependencies.

## Milestone Completion
- Milestone M0 is COMPLETE only after Issue #26 passes acceptance criteria.
```

---

## Step 3: Pull Request (`PR #27`)

```markdown
## Summary
Verified engine headless foundation execution. Confirmed state transitions, event serialization, and deterministic episode execution with no graphical dependencies.

## Acceptance Criteria Verification
- [x] Complete episode runs headless without GUI
- [x] State transitions verified
- [x] Deterministic execution passes
- [x] Full existing test suite passes with zero regressions
- [x] No renderer or HUD code added
- [x] No AI planning or learning introduced

resolves #26
```

---

## Step 4: Milestone Closure

1. CI validates that PR #27 tests pass and that `resolves #26` is the strict final line.
2. PR #27 merges into `main`.
3. Issue #26 automatically closes.
4. Milestone M0 acceptance criteria are audited: all issues closed, test suite green, zero scope restriction breaches.
5. Milestone M0 is marked CLOSED, unlocking M1 for execution.
