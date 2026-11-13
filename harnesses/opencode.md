# OpenCode - Harness Specification

## Overview
OpenCode is an open-source terminal-based AI coding tool. It does not have a native skill/slash-command system like Claude Code. Instructions are delivered through project-level markdown files and JSON configuration.

## Instruction Format

### AGENTS.md (Project-Level Instructions)
OpenCode reads `AGENTS.md` from the project root. This is the primary way to inject instructions:
```
{project-root}/AGENTS.md
```

Content is free-form markdown. OpenCode loads it into the model's context for every conversation in that project.

### opencode.json (Global Configuration)
Located at `~/.config/opencode/opencode.json`. Contains:
- Provider and model configuration
- Agent definitions (subagent configs)

```json
{
  "agent": {
    "agent-name": {
      "description": "What this agent does",
      "mode": "subagent",
      "model": "provider/model-name"
    }
  }
}
```

## Differences from Claude Code
| Feature | Claude Code | OpenCode |
|---------|------------|----------|
| Global skills | ~/.claude/skills/ | No equivalent (project-level only) |
| Slash commands | /skill-name | No native support |
| Auto-triggers | Keyword matching | No equivalent |
| Reference files | references/ subfolder | Inline in AGENTS.md or separate .md files |
| Hooks | settings.json hooks | No equivalent |

## Deploy Paths

### Project-Level Instructions
```
{project-root}/AGENTS.md
```

### Global Config
```
~/.config/opencode/opencode.json
```
On Windows: `C:\Users\{username}\.config\opencode\opencode.json`

## Adaptation Rules (from Canonical Registry)
When deploying a canonical skill from the Skillmania registry to an OpenCode project:

### Option A: Embed in AGENTS.md
Append the skill content as a headed section in the project's AGENTS.md:
```markdown
## {Skill Name}
{skill.md body content here}
```
Reference files can be inlined below the section or kept as separate .md files in the project root.

### Option B: Standalone Instruction File
Create a separate markdown file and reference it from AGENTS.md:
```markdown
# AGENTS.md
See `instructions/{skill-name}.md` for {skill description}.
```

### Option C: Agent Definition
For skills that define subagent behavior, add an entry to the `"agent"` key in opencode.json.

## Limitations
- No global skill persistence across projects (must deploy per-project)
- No automatic trigger system (user must manually reference instructions)
- No native hooks or event system
- Adding a new "skill" requires editing AGENTS.md or creating new .md files manually

## Workaround: Shared Instructions
To share instructions between Claude Code and OpenCode in the same project, use AGENTS.md that points to CLAUDE.md:
```markdown
# AGENTS.md
Treat CLAUDE.md as your instruction file. Read CLAUDE.md in the root of this project for all instructions.
```
This way both harnesses read from a single source. However, this doesn't support Claude Code's trigger/slash-command features.
