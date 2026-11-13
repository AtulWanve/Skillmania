# Skill Authoring Guide

A practical reference for understanding, building, and maintaining AI skills.

---

## What a skill is

A skill is a set of instructions injected into an LLM's context window when invoked. That's it.

It is **not** code that executes. It is text that shapes the model's behavior for that turn. When you invoke a skill, the model reads the skill instructions and follows them as if they were part of its system prompt. The model doesn't "run" the skill; it reads it and adjusts its behavior accordingly.

Skills can include reference documents that get loaded alongside the main instructions. These provide domain knowledge, checklists, or lookup tables the model wouldn't otherwise have access to.

Think of it this way: if the system prompt is the model's permanent personality, a skill is a temporary persona overlay that lasts for the duration of the task.

---

## Skills vs Commands (Claude Code)

Claude Code has two distinct mechanisms that both appear as slash commands:

**Skills** (`~/.claude/skills/{name}/SKILL.md`):
- Rich structure with frontmatter, references/, agents/
- Auto-trigger support (keyword matching in user prompts)
- Invoked via `/skill-name` or loaded automatically when triggers match
- Full instructions loaded into context

**Commands** (`~/.claude/commands/{name}.md`):
- Simple prompt templates
- Use `$ARGUMENTS` placeholder for runtime substitution
- Only invoked explicitly via `/command-name [args]`
- Lighter weight, easier to create for one-off workflows

Both are managed in this registry. The `type` field in `meta.yaml` distinguishes them (`type: skill` or `type: command`). Most of what's in your registry are skills; `onboard` is the only command.

---

## Anatomy of a Claude Code Command

Commands are simpler than skills. They're single-file prompt templates with runtime argument substitution.

### File Structure

```
~/.claude/commands/{name}.md
```

That's it. One file. No directories, no references, no agents.

### Command Format

```markdown
---
description: One-line summary shown in slash command listings
---

Your prompt template here. Use $ARGUMENTS where user input goes.

Example: Create a new component named $ARGUMENTS with standard boilerplate.
```

When you invoke `/command-name foo bar`, the harness replaces `$ARGUMENTS` with `foo bar` and sends the expanded prompt to the model.

### When to Use Commands vs Skills

**Use a command when:**
- You have a template where only the input varies (file path, project name, search term)
- No auto-triggers needed (commands are always explicit invocation)
- No reference files needed (all instructions fit in one template)
- Simple, single-purpose workflow

**Use a skill when:**
- Complex instructions that need structure (frontmatter, references)
- Auto-triggers (keyword matching)
- Portable across harnesses (commands are Claude Code-specific)
- Need multi-file reference support

**Example**: `onboard` is a command because it's a workflow template where the only variable is the project description. If it needed a 10-page architecture reference doc, it would be a skill.

---

## Anatomy of a Claude Code Skill

### Directory Structure

```
~/.claude/skills/{name}/
  SKILL.md            # Required. The core instructions.
  references/          # Optional. Additional context docs.
    palette.md
    api-reference.md
    checklist.md
```

### SKILL.md Format

The file has two parts: frontmatter (metadata) and body (instructions).

```markdown
---
name: My Skill Name
description: One-line summary shown in skill listings
trigger: keyword1, keyword2, "exact phrase match"
---

## Instructions

You are now operating in [mode]. When the user asks X, do Y.

### What to do
- Step 1
- Step 2

### What NOT to do
- Don't do A
- Don't do B
```

#### Frontmatter Fields

| Field | Required | Purpose |
|-------|----------|---------|
| `name` | Yes | Display name shown in listings |
| `description` | Yes | One-line summary. This is what users scan when deciding whether to invoke |
| `trigger` | No | Keywords or patterns matched against user prompts for auto-invocation. Omit for manual-only skills invoked via `/skill-name` |

#### Body

The actual instructions the model receives. Written in second person ("You should...", "When X, do Y..."). This is where the skill's behavior is defined.

The body supports full Markdown. Use headers, lists, tables, and code blocks to structure the instructions clearly. The model parses all of it.

### `references/` Subfolder

Additional markdown files loaded into context alongside SKILL.md. Use for:

- Large reference tables (color palettes, API endpoint lists)
- Checklists that would bloat the main SKILL.md
- Domain knowledge documents (style guides, conventions)
- Examples and templates

Each file in `references/` is loaded as additional context. Keep individual files focused - one topic per file.

---

## Beyond Markdown: What Else Skills Can Do

Skills are text instructions, but they exist within a broader ecosystem of capabilities.

### Hooks

Claude Code has a hooks system (configured in `settings.json`) that runs executable scripts on tool events - before/after a file edit, on commit, etc. These are **not** skills, but they complement skills. A skill tells the model *what to do*; a hook runs *actual code* when a specific event fires.

Example: A skill could instruct the model to follow a formatting convention. A hook could run a linter automatically after every file write to enforce it.

### Subagent Orchestration

A skill's instructions can tell the model to use the Agent tool to spawn subagents. This effectively creates multi-agent workflows triggered by a single slash command. The skill defines the orchestration strategy: which agents to spawn, what each one handles, and how to merge results.

### Tool Guidance

Skills can instruct the model on how to use specific tools, MCP servers, or CLI commands that it might not know about by default. If your workflow depends on a custom CLI tool or an MCP server with a non-obvious API, a skill can document the correct usage patterns so the model doesn't guess.

---

## When to Create a Skill (Decision Points)

**Create a skill when:**

- You find yourself writing the same prompt instructions more than 3 times. That repetition is a signal the behavior should be packaged.
- You need consistent behavior across sessions: same output format, constraints, and quality bar. Without a skill, you get drift.
- You want to package domain knowledge the model doesn't have. Internal API docs, project conventions, proprietary formats. Put these in `references/`.
- A team needs shared standards. Skills in a registry ensure everyone gets the same model behavior.

**Don't create a skill when:**

- The task is a one-off or varies significantly each time. Just prompt it directly.
- The harness already does this natively. Check built-in commands first (e.g., Claude Code ships `/code-review`, `/simplify`, `/pr`, so no skill is needed for these).
- The behavior is simple enough to capture in a CLAUDE.md rule. Project-level instructions in CLAUDE.md are simpler than a full skill for basic constraints.

---

## When a Skill Has Gone Stale

Skills rot. Audit them quarterly. Signals that a skill needs retirement or rewrite:

- **The harness ships the feature natively.** Your custom skill now duplicates built-in behavior, possibly with worse instructions than the official version.
- **The skill references outdated tool names, APIs, or model capabilities.** If the skill mentions tools that no longer exist or APIs that have changed, it will confuse the model.
- **You never invoke it.** If a skill hasn't been used in 2+ months, question whether it's still needed. Either it's solving a problem that went away, or its trigger is broken.
- **Trigger keywords conflict with other skills or built-in commands.** Overlapping triggers cause unpredictable invocation. The wrong skill loading is worse than no skill loading.

---

## How to Test a Skill

1. **Invoke it explicitly.** Use `/skill-name` or mention the trigger keywords in a prompt.
2. **Check it loads.** The skill content should appear in the system-reminder block. If it doesn't show up, the skill is not being found; check the directory structure and name.
3. **Verify behavior change.** Compare model output with and without the skill active. The difference should be clear and match what the skill instructions specify.
4. **Test edge cases.** Try inputs that should NOT trigger the skill. If the skill fires on unrelated prompts, the trigger is too broad.
5. **Test instruction conflicts.** If the skill interacts with CLAUDE.md rules or other skills, verify they compose correctly and don't contradict each other.

---

## Good vs Bad Skill Design

### Good Skills

- **Focused.** One responsibility per skill. A skill that does code review should not also handle deployment.
- **Clear triggers.** Specific keywords that match the intended use case and nothing else.
- **Actionable instructions.** "When you see X, output Y in format Z." Not "try to be good at X."
- **Includes what to avoid.** Negative instructions ("Do NOT...") are as important as positive ones. They prevent the model from falling back to default behaviors that conflict with the skill's purpose.
- **Self-contained.** A reader (human or model) can understand the skill without external context.

### Bad Skills

- **Kitchen-sink skills** that try to cover everything. These are hard to maintain, hard to test, and the model struggles to prioritize conflicting instructions within them.
- **Vague instructions** like "be helpful" or "write better code." The model already tries to do these things. A skill needs to add specificity.
- **No clear trigger conditions.** If you can't describe when the skill should fire, it shouldn't be a skill.
- **Instructions that conflict with the model's defaults or other skills.** This creates unpredictable behavior. If you need to override a default, be explicit about it.
- **Overly long skills** that exceed what the model can effectively follow. If your SKILL.md is over ~2000 words, break the reference material into `references/` files and keep the core instructions tight.

---

## Distilling SOPs and Source Material into Skills

When transforming unstructured playbooks, runbooks, videos, or process documentation into a structured skill:

1. **Extract the Core Trigger**: Identify the exact conditions or requests that necessitate this workflow. Avoid broad triggers that cause unintended invocations.
2. **Isolate Deterministic Steps**: Separate mandatory procedural steps (such as command flags, required verification, or specific tool ordering) from subjective guidance.
3. **Define Negative Guards**: List clear anti-patterns, forbidden actions, and scope boundaries (what the skill must explicitly avoid doing).
4. **Standardize Output Contracts**: Enforce strict output schemas. For complex reporting or file generation, include a dedicated `references/output-template.md` rather than describing the expected output loosely in prose.
5. **Strip Packaging Dead Weight**: Remove third-party licenses, author tags, repository URLs, credit blocks, and version stamps from `skill.md` frontmatter and metadata. Skills in this hub contain only operational instructions and standard harness fields (`name`, `description`, `trigger`). Never leave packaging residue from upstream repos.
6. **Deploy via Filesystem Copy**: Never edit installed harness directories directly (`~/.claude/skills/`). The canonical directory (`registry/{skill}/`) is the single source of truth. Synchronize changes to installed harnesses using shell copy commands (`Copy-Item -Force`).
7. **Template Hygiene (No Dummy Prose or Conditional Prompts)**: When authoring templates in skills or references, never write realistic English sentences, parenthetical guidance, or conditional prompts as placeholders (e.g. "Core functional changes implemented", "(if applicable)", "or mark N/A"). Models treat natural language dummy text as literal requirements and copy it verbatim into output artifacts. Always use explicit angle-bracket placeholder tokens (such as `<specific functional deliverable>` or `<criterion 1 from issue verbatim>`).
8. **Path Portability (Relative References Only)**: Never hardcode host user directory paths (such as `C:\Users\...` or `/Users/...`) in skills. Reference internal skill files relatively (`standards/`, `reviews/`, `templates/`) or use generic home directory paths (`~/.claude/skills/<skill-name>/`).

---

## Plain language and writing style for skills

When writing skill prompts, documentation, references, and descriptions, follow these Plain Language rules:

- **Lead with the main point**: State the action, verdict, or rule in the first sentence.
- **Use direct verbs and active voice**: Prefer simple verbs (use, run, build, check) over abstract nouns and inflated Latinate words (utilize, orchestrate, instantiate).
- **Keep sentences and paragraphs short**: Avoid repetitive 20-word compound sentences. Mix punchy declarative statements with necessary technical explanations.
- **Maintain consistent terminology**: Use one term for the same item throughout. Do not rotate synonyms.
- **Use `must` for requirements**: Reserve `must` for strict boundaries and invariants; do not dilute it on optional suggestions.
- **Eliminate structural staging**: Never use artificial contrasts ("not just X, but Y"), theatrical one-line closers, or introductory run-up filler ("Let's dive in").
- **Avoid double negatives**: State what should happen directly rather than what should not be avoided.
- **Preserve exact technical precision**: Keep exact identifiers, commands, paths, schema fields, quotations, watched phrases, and behavior-bearing examples intact. Never dumb down code symbols into fuzzy metaphors.

