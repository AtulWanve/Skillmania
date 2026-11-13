# Skillmania

A central hub for authoring, auditing, and distributing AI coding skills across tools like Claude Code and OpenCode.

## Overview

Coding assistants use custom instructions and prompt templates to guide language models during development tasks. Most tools store these files in machine-specific local directories, such as `~/.claude/skills` or `.cursor/rules`.

Managing skills directly in those local paths creates three common issues:
- Installed skills drift across different machines and tools.
- Skills go stale when assistants add native features that replace them.
- Prompt instructions accumulate without version control or clear trigger conditions.

Skillmania keeps canonical versions of each skill in a single repository. Each skill has one source of truth, explicit deployment targets, and automated validation to keep formatting consistent.

## Repository layout

- `registry/`: Canonical skill sources. Each skill has its own folder containing `skill.md` (the core instructions) and `meta.yaml` (metadata, triggers, and deployment targets).
- `harnesses/`: Target tool specifications. Documents format requirements and installation paths for tools like Claude Code and OpenCode.
- `docs/`: Guides for skill authoring, evaluating whether to keep or retire skills, and milestone records.
- `scripts/`: Validation and sync scripts, including `validate_registry.py`.
- `audit/`: Health check tooling to detect outdated skills, missing triggers, or overlap with built-in assistant features.
- `.github/`: Issue templates, pull request templates, and CI workflows.

## Validation and tests

Local verification runs with Python 3.12:

```bash
# Lint Python scripts
ruff check .

# Security scan
bandit -c pyproject.toml -r .

# Validate registry structure and skill metadata
python scripts/validate_registry.py
```

The GitHub Actions CI workflow runs these checks on every push and pull request to the `main` branch.

## Adding a skill

1. Create a directory in `registry/<skill-name>/`.
2. Add `skill.md` containing the prompt instructions.
3. Add `meta.yaml` defining `name`, `description`, `status` (`active` or `archived`), and target harnesses (for example, `targets: [claude-code]`).
4. Run `python scripts/validate_registry.py` to confirm the folder passes schema and context checks.
