# Skillmania

## What we are building
A central management hub for AI coding skills across all harnesses (Claude Code, Cursor, Windsurf, Cline, etc.). This project is the single source of truth for creating, auditing, upgrading, and distributing skills, keeping them portable and maintained.

## What good looks like
- Skills stored here as canonical sources, deployed to target harnesses via scripts.
- Clear documentation on what each skill does, when to use it, and which harnesses it targets.
- Audit tooling that flags stale skills, skills the harness has outgrown, or skills that never fire.
- The owner (Atul) understands every skill well enough to decide its fate without AI hand-holding.

## What to avoid
- Skills that duplicate built-in harness capabilities (if Claude Code ships a feature, retire the skill).
- Blind skill creation without understanding the trigger conditions and format requirements.
- Harness-specific lock-in: skills should be authored in a portable canonical form where possible.
- Accumulating skills that never get used or whose purpose is forgotten.
