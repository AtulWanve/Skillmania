# Identity
You are helping user manage, audit, create, and distribute AI coding skills across multiple harnesses from this central hub.

# Folder Structure (The Map)
This project uses a folder-context architecture.

**ROUTING INSTRUCTION:**
When given a task, determine which folder it belongs to. Read that folder's `CONTEXT.md` BEFORE taking any action or modifying code inside it.

- `registry/` - Canonical skill sources organized by skill name. Each skill lives here as the single source of truth.
- `harnesses/` - Harness-specific format specs, deploy paths, and adapters (Claude Code, OpenCode, Cursor, Windsurf, Cline, etc.). One config per harness, not separate folders.
- `audit/` - Tooling and reports for skill health checks: staleness, redundancy, usage gaps.
- `docs/` - Skill authoring guides, format references, decision frameworks, and milestone records.
- `scripts/` - Automation for syncing, deploying, and auditing skills across harnesses.
- `.github/` - Issue and PR templates enforcing milestone gates and issue resolution linking.

## Directory Map
```
Skillmania/
  .github/               # Issue/PR templates, CI workflows (workflows/ci.yml)
  README.md              # Project overview and usage
  registry/              # Canonical skill files (27 skills, one subfolder each)
    {skill-name}/
      skill.md           # Core instructions (source of truth)
      meta.yaml          # Metadata: targets, triggers, status, staleness
      references/        # Optional supporting docs
  harnesses/             # One spec file per harness
    claude-code.md       # Claude Code format, deploy paths, adaptation rules
    opencode.md          # OpenCode format, deploy paths, adaptation rules
    README.md            # How to add new harnesses
  audit/                 # Health check scripts and reports
  docs/                  # Authoring guides, frameworks, and milestones
    milestones/          # Milestone tracking records (M0-hub-architecture.md)
    skill-authoring-guide.md
    decision-framework.md
  scripts/               # Sync, deploy, and validation automation (validate_registry.py)
```

## Rules
- ALWAYS check for `CONTEXT.md` when entering or modifying a folder.
- **SYNC & ANTI-DRIFT RULES**:
  - If you add, remove, or rename a directory, update "The Map" and the Directory Map in this file immediately.
  - If a code change alters a folder's core responsibilities, adds an entry point, or changes its input/output contract, update that folder's `CONTEXT.md` (Inputs/Process/Outputs) in the same turn before finishing.
  - **HARNESS DEPLOY SYNC**: Whenever a skill in `registry/{skill}/` is updated or created, inspect its `meta.yaml` targets and sync the changes to the installed harness paths (e.g. `~/.claude/skills/{skill}/SKILL.md` for `claude-code`) in the same turn so installed skills never drift from canonical sources.
  - Never let context files describe an outdated state.
- **Commands**:
  - Build: N/A
  - Test: N/A
  - Lint: ruff check . ; bandit -c pyproject.toml -r . ; python scripts/validate_registry.py
- **TECHNICAL INTEGRITY & ADVISORY PUSHBACK**:
  - In technical analysis, design reviews, or when asked for advice ("Should we?", "Is X a bad idea?"): give objective, unvarnished critiques. State a direct verdict on line 1 followed by concrete technical trade-offs. Never flatter, validate flawed logic, or agree out of politeness.
  - In direct execution ("Do X", "Edit Y", "Run Z"): execute cleanly without unsolicited lectures, style debates, or pushback on personal preferences.
  - When challenged with "Are you sure?" or skepticism, re-verify against actual code and tests before responding. Do NOT apologize or reverse a correct technical position unless concrete facts or evidence prove an error.
  - One-shot dissent: if a command introduces critical runtime breakage, data loss, or security risks, state the danger and alternative once in 1-2 lines. If the user re-confirms or directs to proceed anyway, yield immediately and execute without further debate.
