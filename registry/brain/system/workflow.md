---
title: Workflow
tags: [system, workflow, lifecycle, pipeline]
aliases: [Execution Lifecycle, Pipeline Workflow]
---

# Workflow

Defines the execution lifecycle. The detailed implementation lives in [[runtime/orchestrator]].

```
Receive Prompt
↓
Task Classification    ← [[runtime/task-classifier|Task Classifier]]
↓
Retrieve Context       ← [[runtime/context-loader|Context Loader]] + [[runtime/graph-retriever|Graph Retriever]]
↓
Planning               ← [[system/planner]]
↓
Execution              ← [[runtime/execution-engine|Execution Engine]]
↓
Static Validation      ← [[runtime/static-validator|Static Validator]]
↓
Review                 ← [[runtime/review-engine|Review Engine]] + [[runtime/confidence-engine|Confidence Engine]]
↓ (accepted)
Knowledge Sync         ← [[runtime/memory-updater|Memory Updater]] + [[runtime/graph-updater|Graph Updater]]
↓
Append Task History    ← [[templates/task-entry-template|Task History]]
↓
Response
```

> [!info] Knowledge Sync runs only when the review is accepted; rejected results bypass it and return to Execution or escalate. No implementation logic should exist inside this file. It is a high-level map. See the [[runtime/orchestrator|Orchestrator]] for the full deterministic pipeline with retry, escalation, and error handling.
