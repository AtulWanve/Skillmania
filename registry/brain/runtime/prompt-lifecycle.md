---
title: Prompt Lifecycle
tags: [runtime, lifecycle, pipeline, end-to-end]
aliases: [PromptLifecycle, Phase 18]
---

# Prompt Lifecycle (Phase 18)

The complete end-to-end lifecycle of a user prompt. See also [[runtime/orchestrator]] for the deterministic pipeline and [[system/workflow]] for the high-level view.

## Full Pipeline

```
Receive Prompt
↓
Task Classification      ← [[runtime/task-classifier|Task Classifier]]
↓
Graph Retrieval          ← [[runtime/graph-retriever|Graph Retriever]]
↓
Load Relevant Memory     ← [[runtime/context-loader|Context Loader]]
↓
Planning                 ← [[system/planner]]
↓
Execution                ← [[runtime/execution-engine|Execution Engine]]
↓
Static Validation        ← [[runtime/static-validator|Static Validator]]
↓
AI Review                ← [[runtime/review-engine|Review Engine]]
↓
Confidence Scoring       ← [[runtime/confidence-engine|Confidence Engine]]
↓
!blocking && overallScore >= 90 ?
├── No
│   ↓
│   Retry count < max (default 3) ?
│   ├── Yes → increment retry count, re-enter at Execution with improvement instructions
│   │         and proceed through the remaining stages in order (never skip stages)
│   └── No  → Escalate to human review, return escalation response (no further retries)
│
└── Yes
    ↓
    Knowledge Synchronization   ← [[runtime/memory-updater|Memory Updater]] + [[runtime/graph-updater|Graph Updater]]
    ↓
    Append Task History         → updated in [[tasks/completed]] / [[tasks/failed]]
    ↓
    Return Final Response
```

## Design Principles

- Every stage is deterministic
- No stage may be skipped
- Failures at any stage return actionable feedback
- Knowledge grows incrementally with every completed task
- Token consumption is minimized by early validation

> [!info] This lifecycle is enforced by the [[runtime/orchestrator|Orchestrator]]. Each runtime component runs in strict order: retries always re-enter at Execution and proceed through the remaining stages in order; no stage-skipping is permitted.
