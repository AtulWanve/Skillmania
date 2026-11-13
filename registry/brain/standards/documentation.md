---
title: Documentation Standards
tags: [standards, documentation, comments, memory]
aliases: [Documentation Standards]
---

# Documentation Standards

## Code Comments

- Document why, not what (code should be self-documenting)
- JSDoc for public APIs and exported functions
- Inline comments for non-obvious logic only
- Avoid commented-out code

## README

- Every package or module has a README.md
- Include: purpose, setup, usage, API, configuration
- Keep it concise; link to detailed docs

## Memory Documentation

- Update only affected memory files per change
- Never regenerate entire documentation
- Append, never rewrite, unless explicitly requested
- Keep each file under 500 lines
- **Compaction**: When a memory file reaches 450 lines, the next write must trigger a compaction pass: archive older records (identified by timestamp or insertion order) to a `memory/archive/` subdirectory, keeping only the most recent records needed to stay under 500 lines and preserve continuity. Compaction copies removed records to an archive file (named `<original-file>-<YYYY-MM>.md`) rather than deleting them. The compaction itself follows the same atomic-write and lock-guarded protocol defined in the [[runtime/memory-updater|Memory Updater]]. If the file would exceed 500 lines without compaction, the write fails with a `FileSizeLimitExceeded` error: compaction must be completed before the write can proceed.

> [!tip] See [[templates/memory-template|Memory Template]] for the record format used in memory files.
