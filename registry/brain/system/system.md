---
title: System
tags: [system, workflow, orchestrator]
aliases: [Global System, Engineering System]
---

# System

Defines the global engineering workflow.

## Responsibilities

- Receive user prompts
- Enforce execution order via the [[runtime/orchestrator|Orchestrator]]
- Never store architecture (see [[memory/architecture|Architecture Memory]])
- Never store project memory (handled by [[runtime/memory-updater|Memory Updater]])
- Never store implementation details

> [!important] This file should remain stable throughout the lifetime of the project. It is the single source of truth for the high-level workflow, referenced by the [[runtime/orchestrator|Orchestrator]] and [[runtime/prompt-lifecycle|Prompt Lifecycle]].
