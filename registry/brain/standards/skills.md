---
title: External Skill Integration Standards
tags: [standards, skills, integrations, quality]
aliases: [Skill Standards, External Skills]
---

# External Skill Integration Standards

Defines how Project Brain interacts with external Claude Code skills (e.g., `test-audit`, `onboard`, `security-review`).

## 1. Architectural Principles

- **Zero Hard Dependencies**: The core runtime pipeline must execute successfully even if an external skill is unavailable in the environment.
- **Deterministic Supremacy**: External AI skills cannot replace deterministic CLI gates in [[runtime/static-validator|Static Validator]] (`npm run test`, `pytest`, `lint`, `typecheck`, `build`).
- **Schema Invariance**: External skills cannot alter the eight canonical dimensions or scoring formulas in [[runtime/review-engine|Review Engine]].
- **Advisory Input**: External skills provide advisory evidence, discovery scaffolding, and specialized pre-execution or post-execution sweeps.

## 2. Recognized Companion Skills

Project Brain defines standardized integration contracts for two primary companion skills:

1. **`onboard` (Context Architect & Scaffolding)**:
   - **Role**: Discovers project stack, constructs directory tree maps, and generates `CONTEXT.md` with explicit `Inputs`, `Process`, and `Outputs` sections.
   - **Hook Phase 0 (Workspace Discovery)**: If `/brain` is executed on a repository lacking `CONTEXT.md` files or directory maps, it advises running `/onboard` to establish the folder-context architecture before deep execution.
   - **Hook Phase 15 (Knowledge Sync & Anti-Drift)**: When `/brain` creates a new directory, it follows `/onboard`'s canonical `CONTEXT.md` format (`Inputs`, `Process`, `Outputs`) to document the folder in the same turn.

2. **`test-audit` (Test Suite Quality & Gate)**:
   - **Role**: Rejects duplicate, trivial, or mock-heavy tests; enforces authoring gates and proportional testing.
   - **Hook Phase 11 (Execution)**: Pre-generation gate to ensure new test files avoid mock abuse and test real contracts.
   - **Hook Phase 12 (Static Validation)**: Advisory pre-validation check before executing test runners.
   - **Hook Phase 13 (AI Review)**: Informs the `testing`, `maintainability`, and `regression` scoring dimensions.

## 3. Lifecycle Hook Points

External skills hook into five designated lifecycle phases:

1. **Workspace Discovery (Phase 0)**: Scaffolding and baseline structure (e.g., using `onboard` to map folder boundaries and contracts).
2. **Planning (Phase 10)**: Informing strategy (e.g., using `test-audit` to specify proportional testing requirements in `testingStrategy`).
3. **Execution (Phase 11)**: Assisting generation (e.g., applying `test-audit` authoring gates to reject mock-heavy or tautological test authoring).
4. **Static Validation (Phase 12)**: Pre-validation gate (e.g., running `test-audit` to inspect test quality before executing test runners).
5. **AI Review (Phase 13)**: Providing dimension evidence (e.g., `test-audit` findings supply concrete notes and scores for `testing`, `maintainability`, and `regression` in [[runtime/confidence-engine|Confidence Engine]]).

## 4. Verification and Fallback Contract

Before invoking any external skill:
- **Capability Check**: Verify skill availability in the session. If absent, fall back to internal baseline checklists without failing the task.
- **Output Ingestion**: Map external skill output strictly into Project Brain data contracts (`FileDiff`, `ReviewDimension.notes`, or `RiskReport`).
- **Validation**: Any code modified or suggested by an external skill must pass all [[runtime/static-validator|Static Validator]] checks.
