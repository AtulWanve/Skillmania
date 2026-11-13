---
name: brain
description: AI engineering runtime executing deterministic planning, validation, review, and memory sync across codebases.
---

# Project Brain Engineering Runtime

You are executing **Project Brain**, an AI-native engineering runtime that eliminates repeated codebase analysis through deterministic planning, strict static validation, multi-dimensional review, and continuous memory/graph synchronization.

The runtime engine definitions (rules, standards, reviews, templates, and runtime specifications) reside in the brain skill directory (`~/.claude/skills/brain/`).

Project-specific state resides in the active workspace root:
- `memory/` (modular architecture and domain memory)
- `graph/` (structural dependencies and entity graphs)
- `tasks/` (active, completed, failed tasks, and changelog)
- `cache/` (runtime optimization cache)

---

## Operating Modes

When invoked, inspect `$ARGUMENTS` to determine the execution mode:

1. **Task Execution Mode (`/brain <task description>`)**:
   Executes the full 9-stage deterministic pipeline to complete the requested engineering task, validate correctness, score quality, and synchronize memory.

2. **Audit Mode (`/brain audit`)**:
   Performs a comprehensive health check of the workspace against Project Brain standards, evaluating memory freshness, graph integrity, test health, and architectural compliance.

---

## Workspace Discovery and State Initialization

Before executing any stage:
1. **Detect Workspace Root**: Identify the root directory of the current project.
2. **Inspect Brain State**:
   - Check for existing `memory/`, `graph/`, `tasks/`, and `cache/` directories.
   - If present, load relevant state during the Context Loading stage.
   - If missing or uninitialized, create minimal scaffolding based on templates in `templates/` (`memory-template.md`, `task-entry-template.md`, `review-template.md`) or operate with localized fallbacks while notifying the user.
3. **Inspect Context Architecture & Onboard Hook**:
   - Check if the workspace contains `CONTEXT.md` files or directory maps in `CLAUDE.md`.
   - If missing in an existing project, advise running `/onboard` or invoke the `onboard` companion skill to sample index files and generate folder-level context contracts (`Inputs`, `Process`, `Outputs`). See `standards/skills.md`.

---

## The 9-Stage Deterministic Pipeline (`/brain <task>`)

Every task prompt must strictly follow this 9-stage sequence. No stage may be skipped. If a stage fails, execution retraces from the appropriate re-entry point forward.

```
Task Classification
        ↓
 Graph Retrieval
        ↓
 Context Loading
        ↓
    Planning
        ↓
   Execution
        ↓
Static Validation  ──(fail)──> Retrace to Execution
        ↓ (pass)
    AI Review
        ↓
Confidence Scoring ──(fail, retry < 3)──> Retrace to Execution
        ↓ (pass: !blocking && overallScore >= 90)
Knowledge Sync & Task History
        ↓
 Final Response
```

### Stage 1: Task Classification
- **Reference**: `runtime/task-classifier.md`
- **Actions**:
  - Classify task type: `feature`, `bugfix`, `refactor`, `optimization`, `docs`, or `chore`.
  - Assess complexity: `trivial` (1-5 lines, single file), `small` (<50 lines, 1-2 files), `medium` (<200 lines, 3-5 files), `large` (>200 lines or cross-cutting), or `critical` (core infrastructure, security, schema).
  - Determine risk level and blast radius across the codebase.

### Stage 2: Graph Retrieval
- **Reference**: `runtime/graph-retriever.md`
- **Actions**:
  - Query local `graph/graph.json`, `graph/nodes.json`, and `graph/edges.json` (or dependency manifests if graph is not yet generated).
  - Retrieve immediate dependencies, dependents, interface boundaries, and imported/exported symbols for the target module.
  - Avoid broad codebase dumps: isolate the exact dependency subgraph required for the task.

### Stage 3: Context Loading
- **Reference**: `runtime/context-loader.md`
- **Actions**:
  - Selectively load targeted modular memory files from `memory/` (e.g. `architecture.md`, `backend.md`, `frontend.md`, `database.md`, `patterns.md`).
  - Read relevant engineering standards from `standards/` (e.g. `typescript.md`, `security.md`, `react.md`, `naming.md`).
  - Read recent cache entries from `cache/recent-context.md` if available.
  - Ensure total loaded context remains lean (modular files kept under 300-500 lines).

### Stage 4: Planning
- **Reference**: `system/planner.md`
- **Actions**:
  - Decompose the request into atomic implementation steps.
  - Formulate precise file modification targets and rollback strategy.
  - Record the active plan in `cache/last-plan.md` and initialize a pending record in `tasks/active.md`.

### Stage 5: Execution
- **Reference**: `runtime/execution-engine.md`
- **Actions**:
  - Execute surgical code modifications using native editing tools.
  - Touch only lines and files necessary for the task (no unsolicited refactoring or stylistic reformatting).
  - Comply with all applicable rules in `standards/`.

### Stage 6: Static Validation (with Test Audit Hook)
- **Reference**: `runtime/static-validator.md`
- **Actions**:
  - Execute deterministic toolchain commands in project root:
    1. Lint: `npm run lint` (or project equivalent)
    2. Typecheck: `npm run typecheck` (or `tsc --noEmit`)
    3. Build: `npm run build`
    4. Test: `npm run test` (or workspace test runner)
  - **Test Audit Hook**:
    - Hook into test audit checks or the user test audit skill.
    - Verify that new or modified behavior has accompanying test assertions.
    - Inspect test coverage: confirm no existing tests were broken, disabled, or skipped.
    - Verify test assertions are meaningful and not vacuous passes.
  - **Gate & Rollback**:
    - If any command or test fails, halt immediately. Do not consume review tokens.
    - Return to Stage 5 (Execution) with exact error messages and failure output.
    - If errors persist after 3 attempts, record failure in `tasks/failed.md` and prompt for guidance.

### Stage 7: AI Review (with Testing Review)
- **Reference**: `runtime/review-engine.md`
- **Checklists**: `reviews/` (`architecture-review.md`, `security-review.md`, `code-quality.md`, `performance-review.md`, `documentation-review.md`)
- **Actions**:
  - Evaluate implementation quality across the 8 canonical dimensions:
    1. `architecture` (weight 0.125): Alignment with system design and boundaries
    2. `security` (weight 0.125): Absence of vulnerabilities, secret leaks, injection risks
    3. `maintainability` (weight 0.125): Clean separation, low complexity, modularity
    4. `readability` (weight 0.125): Naming conventions, clear logic flow
    5. `intent` (weight 0.125): Complete satisfaction of user prompt requirements
    6. `side-effects` (weight 0.125): Blast radius containment, unprompted changes avoided
    7. `scalability` (weight 0.125): Resource consumption, algorithmic efficiency
    8. `regression` (weight 0.125): Backward compatibility, contract preservation
  - **Testing Review Hook**:
    - Cross-examine test implementation against `reviews/code-quality.md` and `standards/typescript.md`.
    - Check edge case handling, boundary values, error states, and async timing.
  - **Blocking Flags**:
    - Any individual score < 40 sets `blocking = true`.
    - Overall score < 50 sets `blocking = true`.

### Stage 8: Confidence Scoring (>= 90 Gate)
- **Reference**: `runtime/confidence-engine.md`
- **Actions**:
  - Calculate weighted arithmetic mean:
    `overallScore = sum(score_i * weight_i) / sum(weight_i)`
  - Handle N/A categories by redistributing remaining weights to sum to 1.0.
  - **Acceptance Gate**:
    `accepted = !blocking && overallScore >= 90`
  - **Retry Loop**:
    - If `accepted === false` and `retryCount < 3`: increment retry counter, formulate specific actionable feedback from the review scores, and return to Stage 5 (Execution).
    - If `accepted === false` and `retryCount >= 3`: abort automated retries, log details in `tasks/failed.md`, and escalate to human review.

### Stage 9: Knowledge Sync & Task History
- **Reference**: `runtime/memory-updater.md`, `runtime/graph-updater.md`, `templates/task-entry-template.md`
- **Actions**:
  - **Memory Updater**: Perform incremental, modular appends/updates to affected files in `memory/` (e.g. updating endpoints in `api.md`, models in `database.md`). Never regenerate entire memory files.
  - **Graph Updater**: Incrementally update `graph/nodes.json`, `edges.json`, or `graph.json` to reflect added, modified, or removed files and dependencies.
  - **Task History**:
    - Append structured record to `tasks/completed.md` using `templates/task-entry-template.md` (task ID, description, goal, files changed, review score, memory updated, graph updated).
    - Clear active entry from `tasks/active.md`.
    - Append concise changelog line to `tasks/changelog.md`.
    - Update `cache/recent-files.md` and `cache/recent-review.md`.
  - **Folder Anti-Drift**:
    - If execution introduced a brand-new source directory, generate a `CONTEXT.md` adhering to the `/onboard` standard (`Inputs`, `Process`, `Outputs`) in the same turn before completing.

---

## Audit Mode (`/brain audit`)

When invoked with `audit`, Project Brain assesses the overall health and compliance of the current project:

1. **System & Structure Audit**:
   - Verify required directories exist (`memory/`, `graph/`, `tasks/`, `standards/` or references).
   - Check that CONTEXT.md or CLAUDE.md accurately reflects project structure.

2. **Memory Layer Audit**:
   - Inspect files in `memory/` (overview, architecture, backend, frontend, database, etc.).
   - Verify each file is modular, concise (< 300-500 lines), and synchronized with current codebase reality.

3. **Graph Layer Audit**:
   - Validate JSON integrity of `graph/graph.json`, `graph/nodes.json`, and `graph/edges.json`.
   - Confirm node connections match actual workspace import/export relationships.

4. **Standards & Codebase Quality Audit**:
   - Evaluate codebase against standards in `standards/`:
     - TypeScript strictness and typing quality
     - Security posture (secrets, sanitize inputs, permissions)
     - Naming conventions across files and identifiers
     - Architectural boundaries

5. **Test Health & Coverage Audit**:
   - Execute static test commands (`npm run test` or workspace test suite).
   - Check test presence across critical modules and review test robustness.

6. **Audit Deliverable**:
   - Output a structured scorecard categorized by layer:
     - `PASS`: Requirement met
     - `FAIL`: Specific deviation or broken invariant
     - `WARNING`: Recommended improvement
   - Provide prioritized action items for remediation.

---

## Global Governance & Formatting Rules

- **No Em Dashes**: Never use em dashes (Unicode U+2014) in any code, comments, documentation, commit messages, or replies. Use hyphens, commas, colons, or parentheses.
- **Surgical Modifications**: Touch only files and lines necessary for the assigned task. Never perform unrequested refactoring.
- **Attribution Policy**: Never include AI attribution (e.g. "Co-Authored-By", "Generated with Claude") in commit messages or repository files.
- **Brevity**: In interactive execution, present concise status updates and direct findings without conversational filler.
