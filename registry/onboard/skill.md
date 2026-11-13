---
description: Automatically set up standardized root CLAUDE.md, root CONTEXT.md, and folder-level CONTEXT.md files for any new or existing project.
---

Initialize and standardize the project context architecture in the current workspace.

Arguments passed (if any): $ARGUMENTS

### Execution Guidelines (Zero Context Bloat & Safety)
- **Directory Scope**:
  - Place `CONTEXT.md` ONLY in directories where application logic, code, or scripts live (top-level source modules or 1-2 levels deep, e.g., `src/api`, `src/services`, `backend`, `frontend`, `scripts`).
  - Automatically ignore gitignored paths, package dependencies, build/compiler outputs, static media/assets, and hidden dot-folders.
  - Do NOT place context files inside leaf folders, individual UI components, or test fixtures.
- **Surgical Sampling**:
  - To identify a folder's core responsibilities and contracts (Step 3), inspect only module READMEs, export index files, or router signatures (read with `limit: 50`). NEVER read full implementation files.
- **Non-Destructive Execution**:
  - NEVER overwrite an existing `CLAUDE.md`. If one exists, preserve all user rules and only append or update the "Folder Structure (The Map)" section.
- **Tone & Terminology**:
  - Use standard, clean software engineering terms (directories, modules, services, utilities). No internal methodology buzzwords or spatial metaphors (never call folders "rooms" or the map a "floor plan" in docs, comments, or output).
  - Explain findings in plain, everyday English. Avoid robotic jargon, buzzwords, or overly formal systems terminology.
  - Talk like a helpful teammate giving a clear, easy-to-read summary of what was found and set up.

---

### Step 1: Detect Project State & Non-Destructive Routing

Inspect the workspace root for `CLAUDE.md` and `CONTEXT.md`.

#### Scenario A: Both `CLAUDE.md` and `CONTEXT.md` Exist (Sync & Audit Mode)
Do NOT overwrite either file. Run an audit:
1. List source directories on disk (excluding dependency, build, and asset folders).
2. Compare them against the existing Map in `CLAUDE.md`:
   - If any source folder is missing a `CONTEXT.md`, create it following Step 3 below.
   - If folders were deleted or added, update "The Map" and refresh the directory tree in `CLAUDE.md`.
3. Stop and jump directly to **Step 5 (Report Completion)**.

#### Scenario B: Existing Project with `CLAUDE.md` (Preserve & Merge Mode)
`CLAUDE.md` exists, but `CONTEXT.md` is missing:
1. Do NOT delete or overwrite the existing `CLAUDE.md`.
2. Generate root `CONTEXT.md` (Step 2) and folder `CONTEXT.md` files (Step 3).
3. Append or update the "Folder Structure (The Map)" section in the existing `CLAUDE.md` without touching the user's existing rules.
4. Stop and jump directly to **Step 5 (Report Completion)**.

#### Scenario C: First-Time Setup (New Project or Unconfigured Repo)
Neither file exists. Proceed through Steps 2, 3, 4, and 5 sequentially.

---

### Step 2: Generate Root `CONTEXT.md`
Determine the project name and primary stack from package files (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, etc.) or `$ARGUMENTS`.
If in an empty directory without `$ARGUMENTS`, ask the user one concise question before creating files: *"What are we building and what stack should we use?"*

Write `CONTEXT.md` in the workspace root (replace bracketed text with concrete project facts):
```markdown
# [Project Name or Current Project]

## What we are building
[1-2 sentences clearly describing the project purpose and primary tech stack]

## What good looks like
- Clean, modular code adhering to standard conventions.
- Tests passing for any new logic or changes.
- Minimal dependencies and surgical edits.

## What to avoid
- Over-engineering simple features or adding unrequested abstractions.
- Hardcoding credentials, tokens, or environment-specific connection strings.
- Bloating the codebase with unused boilerplate.
```

---

### Step 3: Generate Folder-Level `CONTEXT.md` Files
For each qualifying source folder (top-level or 1-2 levels deep):
Write `CONTEXT.md` inside that folder (populate with concrete inputs/outputs discovered via surgical sampling):
```markdown
# [Folder Name]

## Inputs
- [Key data formats, environment variables, or dependencies consumed by this folder]

## Process
- [Core responsibility and business logic handled here]
- [Coding conventions, constraints, or boundaries specific to this folder]

## Outputs
- [Exposed APIs, exported functions, generated artifacts, or database updates]
```

---

### Step 4: Generate Root `CLAUDE.md`
Write `CLAUDE.md` in the project root:
```markdown
# Identity
You are helping the user build and maintain this project.

# Folder Structure (The Map)
This project uses a folder-context architecture.

**ROUTING INSTRUCTION:**
When given a task, determine which folder it belongs to. Read that folder's `CONTEXT.md` BEFORE taking any action or modifying code inside it.

[Generate a bulleted list of each primary folder with a 1-line description of its role]

## Directory Map
[Insert a clean ASCII tree: directories only, max depth 2, max 25 lines]

## Rules
- ALWAYS check for `CONTEXT.md` when entering or modifying a folder.
- **SYNC & ANTI-DRIFT RULES**:
  - If you add, remove, or rename a directory, update "The Map" and the Directory Map in this file immediately.
  - If a code change alters a folder's core responsibilities, adds an entry point, or changes its input/output contract, update that folder's `CONTEXT.md` (Inputs/Process/Outputs) in the same turn before finishing.
  - Never let context files describe an outdated state.
- **Commands**:
  - Build: [Insert detected build command, or N/A]
  - Test: [Insert detected test command, or N/A]
  - Lint: [Insert detected lint command, or N/A]
```

---

### Step 5: Report Completion
Present a clean, plain-English summary of what was set up:
- What the project does (1 concise line based on detected package/code facts).
- Setup status and file count:
  - Mode executed (first-time setup, updating an existing project, or audit/sync).
  - Exact count of context files created or updated.
- What was created or updated:
  - Root files (`CLAUDE.md` and/or `CONTEXT.md`) and detected build/test commands.
  - Which specific folders were mapped and what role they play (e.g. `src/api` for routes, `src/services` for business logic).
  - Any folders skipped to prevent bloat (e.g. build outputs or asset directories).
- A closing confirmation that the project map is ready for work.
