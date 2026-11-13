---
title: Planner
tags: [system, planner, planning, classification, phase-10]
aliases: [Planning Phase, Phase 10]
---

# Planner (Phase 10)

Part of the deterministic pipeline orchestrated by [[runtime/orchestrator|Orchestrator]]. The Planner runs after [[runtime/context-loader|Context Loader]] has assembled the relevant memory files and graph relationships. Its structured output feeds directly into the [[runtime/execution-engine|Execution Engine]].

> [!important] Non-Negotiable Rule
> Only after planning is approved does execution begin. Under no circumstances may code modification or file generation proceed without an approved, validated execution plan.

## Responsibilities

- Prompt decomposition into actionable requirements
- Dependency and graph node analysis
- Implementation sequencing and scoping
- Risk and regression mitigation
- Verification and testing formulation
- Failure containment and rollback formulation

## Phase 10 Deliverables

Before writing code, the planner produces a structured `ExecutionPlan` containing all eight canonical deliverables:

1. **Goal**: Explicit objective, requirements, and target outcome for the task.
2. **Affected Modules**: Architectural modules and graph nodes impacted by the proposed change.
3. **Execution Order**: Ordered, deterministic step-by-step sequence of operations for implementation.
4. **Estimated Complexity**: Implementation complexity classification (`"low"`, `"medium"`, or `"high"`), aligned with [[runtime/task-classifier|Task Classifier]].
5. **Risk Analysis**: Assessment of potential regressions, side effects, performance impact, and security considerations.
6. **Testing Strategy**: Specific testing commands, verification suites, and manual validation steps to confirm correctness.
7. **Rollback Strategy**: Recovery mechanism (`"none"`, `"revert"`, or `"migration"`) to undo changes if execution, validation, or review fails.
8. **Estimated Files**: Comprehensive list of file paths anticipated to be created, modified, or deleted.

## Execution Plan Schema

The Planner emits an `ExecutionPlan` object consumed by the [[runtime/execution-engine|Execution Engine]]:

| Field | Type | Description |
|-------|------|-------------|
| `goal` | `string` | Clear statement of intent and acceptance criteria |
| `affectedModules` | `string[]` | Graph module identifiers and subsystem domains |
| `executionOrder` | `PlanStep[]` | Sequential list of discrete execution actions |
| `estimatedComplexity` | `"low" \| "medium" \| "high"` | Assessed difficulty and cognitive overhead |
| `riskAnalysis` | `RiskReport` | Identified risks, failure modes, and mitigation strategies |
| `testingStrategy` | `string[]` | Deterministic verification commands and test targets |
| `rollbackStrategy` | `"none" \| "revert" \| "migration"` | Prescribed rollback action if downstream stages fail |
| `estimatedFiles` | `string[]` | Relative file paths bounded by surgical scope rules |

### Plan Step (`PlanStep`)

| Field | Type | Description |
|-------|------|-------------|
| `step` | `number` | 1-based sequential index |
| `action` | `"create" \| "modify" \| "delete"` | Operation type |
| `targetFile` | `string` | File path targeted by this step |
| `description` | `string` | Specific modification instructions and constraints |

## Pipeline Integration

- **Upstream Input**: Receives decomposed prompt, classifier output from [[runtime/task-classifier|Task Classifier]], retrieved graph nodes from [[runtime/graph-retriever|Graph Retriever]], and active memory contexts from [[runtime/context-loader|Context Loader]].
- **Downstream Output**: Emits the validated `ExecutionPlan` to the [[runtime/execution-engine|Execution Engine]].
- **Retry Handling**: If downstream [[runtime/static-validator|Static Validator]] or [[runtime/review-engine|Review Engine]] returns actionable failure feedback requiring architectural re-planning, the Orchestrator re-enters the Planner with the error diagnostic payload.
