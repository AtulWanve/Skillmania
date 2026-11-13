# Subsystem Test-Pruning Campaign

A disciplined, 8-step workflow for pruning an entire module or subsystem's test suite. Every step has explicit completion criteria; do not skip ahead.

## Step 1: Baseline

Record the subsystem test line count, production line count, and every test file's pass/fail state at a pinned commit SHA.
- Isolate baseline failures in a separate list.
- Do not assume a failing baseline test is dead code; baseline failures frequently expose real product bugs.
- **Done when**: Every test file in scope has a recorded baseline pass/fail status.

## Step 2: Lanes and Inventory

Partition the subsystem test surface into **lanes** based on functional ownership boundaries, not folder or file prefixes.
- Group tests by the component or service contract they verify (e.g., transport, business logic, storage/database, serialization).
- Include end-to-end integration flows and shared test helpers.
- **Done when**: Every test file and test helper belongs to exactly one lane.

## Step 3: Read-Only Ledger per Lane

Review every test declaration in the lane alongside its production code, callers, and history. Mark each test with one of four marks in a written ledger:

- `R` (Retain): Valid contract protecting against a clear, credible bug.
- `F` (Fix): Valid contract, but the assertion is flawed, vacuous, or passes on an unrelated guard.
- `C` (Consolidate): Merge assertion into a stronger boundary suite or parameter table (e.g., table-driven test cases).
- `D` (Delete): Redundant, mock-inflated, implementation-coupled, or protects no observable contract.

Judge each test by what its assertions actually verify, not by its function or test name.
- **Done when**: Every test declaration in the lane has a mark and an evidence note.

## Step 4: Layer Plan per Lane

Review the completed ledger to identify and eliminate redundant architectural layers across the lane:
- Designate the **Keeper** test suite for each behavior contract.
- Prefer testing at the real transport or service boundary using isolated lightweight fakes over heavy mock collaborators.
- Identify test-only production seams (getters, reset methods, optional injection hooks) that can be deleted once redundant tests are removed.
- **Done when**: The lane plan lists retired files, designated keepers, assertions to carry over, and production seams unlocked for deletion.

## Step 5: Cutover

Apply changes lane by lane:
1. Move retained assertions into designated keeper suites.
2. Delete redundant and low-value tests.
3. Remove unlocked test-only seams from production code (aim for net-negative production lines of code).
4. Run project-level linters or dead-code tools (e.g., dead code and unused export analyzers for your language) to clean up orphaned support files.
5. Verify that keeper suites pass.
- **Done when**: All lane plans are executed and all designated keeper suites pass.

## Step 6: Preservation Review & Mutation Testing

Verify that deleted tests did not create coverage blind spots:
1. An independent pass compares deleted coverage against the keeper suites to catch any accidentally lost contracts.
2. **Mutation Testing**: For any restored or uncertain contract, make one deliberate single-line mutation in production code to prove that the keeper test fails red. Restore the production code byte-for-byte and verify it passes green.
- **Done when**: All reported coverage gaps are restored or confirmed redundant, and every restored contract has a verified caught mutation.

## Step 7: Product Defects

Any baseline failure that persists into a keeper suite must be treated as a real product defect:
- Fix the bug in production code as a separate, dedicated commit.
- Prove the fix with a control run (reverting the fix makes the test fail red) and candidate run (fix applied makes the test pass green).
- **Done when**: Repaired defects have both a failing control and passing candidate record.

## Step 8: Reconcile and Report

Deliver a concise campaign summary:
- Baseline vs. final line counts (test code and production code reported separately).
- Lanes, retired test files, and designated keepers.
- Preservation gaps verified through mutation testing.
- Product defects discovered, fixed, and proven.
