---
name: diagnose
description: Disciplined bug diagnosis loop. Enforces reproducing regressions with a failing test before editing production code.
---

# Diagnosing Bugs

A strict discipline for fixing bugs, crashes, or regressions.

## Rules of Diagnosis

1. **Do NOT Edit Production Code Yet**:
   - Never guess a fix and apply it before proving you understand the failure mechanism.
   - Any premature edit risks introducing subtle secondary regressions.

2. **Formulate a Hypothesis**:
   - Trace the error, stack trace, or unexpected output to a specific input boundary or state mismatch.
   - State your hypothesis clearly in one sentence.

3. **Create a Minimal Reproduction (RED)**:
   - Write a minimal failing test or standalone reproduction script (e.g. `tests/test_repro_<issue>.py` or inline assertion).
   - Run the reproduction script to observe the exact failure.
   - If the script passes or fails with a different error, your hypothesis is wrong. Re-investigate.

4. **Surgical Fix (GREEN)**:
   - Only after observing the expected failure, apply the minimum necessary fix to the codebase.
   - Re-run the reproduction test to verify it turns green.

5. **Verify No Regressions**:
   - Run the test suite or adjacent tests to ensure existing behavior remains intact.
   - Delete temporary reproduction scripts if not meant for the permanent test suite.
