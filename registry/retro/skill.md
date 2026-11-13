---
name: retro
description: Review the session for real, recurring repo problems, while ignoring one-off slips and generic syntax issues.
---

# Session Retrospective

Review the session to see if the agent ran into real roadblocks caused by missing project rules. Most sessions do not need any changes to `CLAUDE.md`. Only recommend a rule if it solves a real, recurring issue specific to this project.

## Tone & Communication

Explain findings in plain, everyday English. Avoid robotic jargon, buzzwords, or overly formal systems terminology. Talk like a helpful teammate explaining what went wrong, why it was skipped, or why a fix actually matters.

## Prerequisite Check

- If the active session has fewer than 2 user turns and no notes were supplied, let the user know that /retro needs an active session history, or ask them to paste the error or notes to look at.

## What to Look for in the Session

Look through the chat history specifically for:
1. **Finding files & navigation**: Did the agent wander across directories or miss folder `CONTEXT.md` instructions?
2. **Commands & tools**: Did commands fail repeatedly because of hidden paths, missing env vars, or undocumented repo build steps?
3. **Repeated corrections**: Did the user have to correct the agent multiple times about the same repo convention or project rule?
4. **Wrong assumptions**: Did the agent make guesses about system architecture that had to be unwound later?

## What NEVER Goes into CLAUDE.md

Skip these completely:
1. **Conversational timing or manners**: Things like "explain before editing", "pause for approval", or "ask before starting". These are prompt preferences, not project rules.
2. **General shell, OS, or language syntax**: Standard stuff like PowerShell quotes, bash escaping, Python virtualenv activation, or common CLI flags.
3. **One-off prompt misunderstandings**: Slips where the agent simply missed an instruction in that specific turn.
4. **Obvious code facts**: Things any developer or agent can already see by checking `package.json`, folder structure, configs, or types.
5. **Micromanaging one-time errors**: Negative "never do X" rules created from a single typo or bad turn.

## Does This Actually Belong in a Project File?

Only consider proposing a rule if it passes all three questions:
1. **Is this unique to this repository?** (It is not a general programming or shell issue.)
2. **Will this help someone 6 months from now?** (An agent working on a completely different file would still benefit from knowing it.)
3. **Did it cause repeated trouble?** (The problem happened 2 or more times, or wasted serious time.)

## Where Does the Fix Belong?

If an issue actually qualifies, put it in the most specific place possible:
- **Skip entirely**: For one-off slips, generic syntax, or simple prompt confusion.
- **Prompt advice**: Suggest how the user can phrase the prompt more clearly (do not write to files).
- **Harness / Tool settings**: CLI flags, permissions, or settings (goes to settings, not project documentation).
- **Subfolder CONTEXT.md**: Rules or entry points that only apply to a specific subfolder.
- **Root CLAUDE.md**: Reserved only for project-wide build/test commands, architecture rules, or core project constraints.

## Output Format

### When Nothing Needs to Be Added (Most Common)

```markdown
### Retrospective: No Changes Needed
Everything looks good. No recurring project traps or missing repository rules found.

#### Issues Looked At (and Skipped):
- **What happened**: [Short, simple description of the slip, e.g. PowerShell quote error or editing too early]
  - **Why skipped**: [Plain explanation, e.g. "This was a standard Windows shell quirk, not something specific to this codebase."]
  - **Better fix**: [e.g. "Run with single quotes or use a separate script file."]
```

### When a Rule Is Actually Needed

```markdown
### Retrospective: Recommended Update

- **Target File**: [Path to CLAUDE.md or specific folder CONTEXT.md]
- **Section**: [Heading where it belongs]
- **What kept failing**: [Plain English description of the repeating issue and wasted turns]
- **Suggested Rule**: [One clear, simple instruction with no em dashes or corporate jargon]
```

Do not edit files automatically. Share your thoughts and ask before making any changes.
