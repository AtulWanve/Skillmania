# Harnesses

Each file in this directory describes one AI coding harness: its skill format, deploy paths, and how to adapt a canonical skill from `registry/` into that harness's native format.

## Currently Supported
- **claude-code.md** - Claude Code (Anthropic CLI)
- **opencode.md** - OpenCode (open-source terminal AI)

## Adding a New Harness
1. Create `{harness-name}.md` in this directory
2. Follow the same structure: Format, Deploy Paths, Adaptation Rules
3. Update the list above
4. Add the harness name to relevant `meta.yaml` target lists in `registry/`

## Core principle
The canonical skill in `registry/` is the single source of truth. Harness specs describe the transformation, not the content. When a skill is updated in the registry, it should be re-deployed to all target harnesses using the scripts in `scripts/`.
