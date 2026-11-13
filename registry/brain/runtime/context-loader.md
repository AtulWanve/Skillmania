---
title: Context Loader
tags: [runtime, context, memory, loading]
aliases: [ContextLoader]
---

# Context Loader

Loads only the relevant memory files required for the current task. Receives `AffectedNode[]` from [[runtime/graph-retriever|Graph Retriever]] and loads from `memory/` files.

## Node-to-Memory Mapping Policy

### Resolution Rules

Each `AffectedNode` from [[runtime/graph-retriever|Graph Retriever]] resolves to a memory file as follows:

1. Strip the `type` prefix from `id` to produce a base name (e.g., `module:auth` → `auth`).
2. Append `.md` and resolve relative to `memory/` (e.g., `memory/auth.md`).
3. If no direct match, fall back to the `path` field: extract the filename stem (e.g., `src/routes/login.ts` → `login`) and look for `memory/login.md`.

### Directory Escape Enforcement

- All resolved paths are normalized and checked against `memory/` as the root.
- If a resolved path would escape `memory/` (e.g., `../../etc/passwd`), throw `EscapeError` and return no context.
- Symbolic links within `memory/` are followed, but the target must also reside under `memory/`.

### Missing and Duplicate Files

- **Missing file**: Silently skipped, no error raised.
- **Duplicate**: If two nodes resolve to the same file, load it once and include it once.

### Affected-Node-Only Loading

- Only nodes in `AffectedNode[]` are resolved. No additional memory files are loaded.
- Assembled context concatenates loaded file contents, each prefixed with its path as a header.

### Empty-Graph Fallback Mode

Fallback is entered only when `graphEmpty === true` (the explicit signal from [[runtime/graph-retriever|Graph Retriever]]). It is **not** triggered by an empty `AffectedNode[]` from a non-empty graph.

1. Load **only `overview.md` and `architecture.md`** as a fallback. (Loading all memory files would overwhelm context tokens).
2. Apply the same path-safety enforcement as normal resolution: normalize each resolved path and verify it stays under `memory/`; throw `EscapeError` immediately and return no context otherwise.
3. Silent skip any file that fails to load due to missing or unreadable file (I/O errors only; EscapeError and other non-I/O failures are never swallowed).
4. Fallback mode is only entered when `graphEmpty === true`: it is not a general "load everything" override.

## Folder Context Architecture & Onboard Hook

In addition to modular memory, Project Brain leverages folder-level `CONTEXT.md` files:
- When a task touches specific folders, the Context Loader reads that folder's `CONTEXT.md` (`Inputs`, `Process`, `Outputs`) before inspecting source files.
- If the workspace lacks folder context or directory maps, Project Brain hooks into the `onboard` companion skill to establish baseline documentation without mass file inspection. See [[standards/skills|External Skill Standards]].

## Multi-Resolution Loading (Blueprint)

Inspired by [PageIndex](https://github.com/VectifyAI/PageIndex) and [ChatIndex](https://github.com/VectifyAI/ChatIndex), the context loader can support **multi-resolution access**:

- **Summary-only**: Load node summaries for broad context (fast, low token cost)
- **Full content**: Load raw content only when the summary is insufficient
- **Dynamic resolution**: LLM determines depth needed during retrieval traversal
- **Session memory**: Use [ChatIndex](https://github.com/VectifyAI/ChatIndex) topic trees for long-running agent conversations: load only relevant branches instead of full history

See [[memory/vectifyai-blueprints]] for the full pattern specification.

> [!tip] Memory files are designed as append-only stubs. See [[standards/documentation|Documentation Standards]] for the 500-line compaction policy.
