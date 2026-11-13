# Claude Code - Harness Specification

## Overview
Claude Code is Anthropic's CLI-based AI coding assistant. It has a native skill system with slash-command invocation, automatic trigger matching, and reference file loading.

## Skill Format

### Directory Structure
```
~/.claude/skills/{skill-name}/
  SKILL.md              # Required: main skill file
  references/           # Optional: supporting documents
    *.md                 # Loaded into context alongside SKILL.md
```

### SKILL.md Structure
The file can optionally start with YAML frontmatter:
```yaml
---
name: my-skill
description: One-line summary shown in listings
---
```

The body contains the instructions the model receives when the skill is invoked. Written in imperative/second-person ("You must...", "When the user asks...").

### Trigger System
- **Explicit invocation**: User types `/skill-name` as a slash command
- **Auto-trigger**: If the skill listing in the system-reminder includes trigger keywords, the skill loads automatically when those keywords appear in the user's prompt
- **Programmatic**: Another skill or the model itself can call `Skill` tool with `skill: "skill-name"`

### Reference Files
Files in `references/` are loaded into the model's context alongside the main SKILL.md. Use for:
- Large lookup tables or checklists
- Domain-specific documentation
- Code templates or patterns

## Deploy Paths

### Global Skills (available in all projects)
```
~/.claude/skills/{skill-name}/
```
On Windows: `C:\Users\{username}\.claude\skills\{skill-name}\`

### Project-Level Skills (available only in that project)
```
{project-root}/.claude/skills/{skill-name}/
```

Project-level skills override global skills with the same name.

## Hooks (Complementary System)
Not skills, but relevant: Claude Code supports hooks in `settings.json` that execute scripts on tool events:
- `PreToolUse`, `PostToolUse`, `Notification`, etc.
- Configured in `~/.claude/settings.json` under the `hooks` key
- Use for automated checks, formatting, or side effects that skills alone can't handle

## Adaptation Rules (from Canonical Registry)
When deploying a canonical skill from the Skillmania registry:
1. Rename `skill.md` to `SKILL.md` (uppercase)
2. Copy `references/` as-is (preserving relative paths)
3. Deploy to `~/.claude/skills/{skill-name}/` for global, or `{project}/.claude/skills/{skill-name}/` for project-level
