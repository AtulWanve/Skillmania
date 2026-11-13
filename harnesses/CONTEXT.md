# Harnesses

## Inputs
- Harness documentation and format specifications (how each tool expects skills/rules/agents to be structured).
- Deploy paths: where each harness reads its config from on disk.

## Process
- One spec file per harness describing: skill format (markdown frontmatter, agents.md, .cursorrules, etc.), deploy locations (global vs project-level), and any transformation rules needed.
- Supported harnesses: Claude Code, OpenCode, Cursor, Windsurf, Cline (extensible).

## Outputs
- Format specs consumed by `scripts/` to transform canonical skills into harness-native format.
- Deploy path mappings so automation knows where to place files.
