---
title: Task Classifier
tags: [runtime, classifier, classification, pipeline]
aliases: [Classifier]
---

# Task Classifier

Classifies incoming user prompts before graph retrieval. The first stage in the [[runtime/orchestrator|Orchestrator]] pipeline.

## Responsibilities

- Prompt decomposition
- Complexity estimation
- Risk assessment
- Task type classification
- Determine review requirements
- Define rollback strategy

## Output Contract

Returns a `ClassifierResult` object, consumed by [[system/planner]] and the [[runtime/orchestrator|Orchestrator]]:

| Field | Type | Description |
|-------|------|-------------|
| `taskType` | `"feature" \| "fix" \| "refactor" \| "docs" \| "test" \| "config" \| "other"` | Category of the task |
| `complexity` | `"low" \| "medium" \| "high"` | Estimated implementation complexity |
| `risk` | `"low" \| "medium" \| "high"` | Risk of unintended side effects |
| `reviewRequired` | `boolean` | Whether AI review is mandatory. When review runs, the result must strictly pass the acceptance gate (`!blocking && overallScore >= 90`) before proceeding; no bypass allows sub-90 scores. In every case AI Review runs after static validation passes and is skipped for any pass in which static validation fails (that pass returns to Execution instead). |
| `rollbackStrategy` | `"none" \| "revert" \| "migration"` | Strategy for undoing the change if needed |
| `confidence` | `number` (0-100) | Classifier's confidence in its own assessment |

> [!info] The `ClassifierResult` is also embedded in the [[templates/task-entry-template|Task Entry Template]] for persistence.
