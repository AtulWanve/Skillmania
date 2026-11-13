---
title: Task Entry Template
tags: [templates, tasks, schema]
aliases: [Task Entry Schema]
---

# Task Entry

Schema for task entries used in [[tasks/active|Active Tasks]], [[tasks/completed|Completed Tasks]], and [[tasks/failed|Failed Tasks]].

| Field | Format / Allowed Values | Required | Description |
|-------|------------------------|----------|-------------|
| `taskId` | `string` (UUID) | Yes | Stable unique identifier for the task |
| `taskDescription` | `string` | Yes | Human-readable description of the task |
| `goal` | `string` | Yes | Intended outcome |
| `filesChanged` | `string[]` (array of file paths) | Yes | Files modified during execution |
| `modulesChanged` | `string[]` (array of module names) | Yes | Graph module identifiers affected |
| `classifierResult` | `ClassifierResult` (see nested contract below) | Yes | Output from [[runtime/task-classifier|Task Classifier]] |
| `reviewScore` | `number` (0-100) or `null` | Yes | Aggregate score from [[runtime/review-engine|Review Engine]] (`null` before review has run, or when `reviewRequired` is `false` and review was skipped) |
| `confidenceScore` | `number` (0-100) or `null` | Yes | Score from [[runtime/confidence-engine|Confidence Engine]] (`null` if not scored) |
| `completedAt` | `string` (ISO-8601 UTC) or `null` | Yes | When the task completed. Must be `null` for unfinished (active or failed) tasks; set to a valid ISO-8601 UTC timestamp only when the task reached a terminal completed state. |
| `memoryUpdated` | `"not-run" \| "completed" \| "failed"` | Yes | Status of [[runtime/memory-updater|Memory Updater]] |
| `graphUpdated` | `"not-run" \| "completed" \| "failed"` | Yes | Status of [[runtime/graph-updater|Graph Updater]] |
| `accepted` | `boolean` or `null` | Yes | Whether the change passed acceptance (`null` before the acceptance gate has been evaluated; `true` or `false` after evaluation) |

### `ClassifierResult` Nested Contract

| Field | Type | Required | Allowed Values |
|-------|------|----------|---------------|
| `taskType` | `string` | Yes | `"feature"`, `"fix"`, `"refactor"`, `"docs"`, `"test"`, `"config"`, `"other"` |
| `complexity` | `string` | Yes | `"low"`, `"medium"`, `"high"` |
| `risk` | `string` | Yes | `"low"`, `"medium"`, `"high"` |
| `reviewRequired` | `boolean` | Yes | `true` or `false` |
| `rollbackStrategy` | `string` | Yes | `"none"`, `"revert"`, `"migration"` |
| `confidence` | `number` (0-100) | Yes | Integer between 0 and 100 |

> [!info] See [[runtime/task-classifier|Task Classifier]] for the source of the `ClassifierResult` contract.
