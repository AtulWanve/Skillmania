# Decision framework: skill, command, or neither?

Quick-reference decision tree. Scan in 30 seconds.

---

## Step 1: Skill, Command, or Just Prompt It?

```
Do I need this behavior more than once?
  |
  NO  -> Just prompt it normally. No need to persist.
  |
  YES -> Continue below...

Is this Claude Code specific?
  |
  NO  -> Make it a SKILL (portable across harnesses)
  |
  YES -> Continue below...

Does it need rich structure (references/, auto-triggers, multi-file)?
  |
  YES -> Make it a SKILL (~/.claude/skills/)
  |
  NO  -> Is it just a template with user input?
         |
         YES -> Make it a COMMAND (~/.claude/commands/)
         |
         NO  -> Make it a SKILL anyway (more powerful)
```

### Quick Comparison Table

| Feature | Skill | Command | Just Prompt It |
|---------|-------|---------|----------------|
| Repeating pattern (>3x) | ✓ | ✓ | ✗ |
| Auto-trigger on keywords | ✓ | ✗ | ✗ |
| Reference files | ✓ | ✗ | ✗ |
| Runtime arguments | ✗ (fixed) | ✓ ($ARGUMENTS) | ✓ (manual) |
| Portable to other harnesses | ✓ | ✗ | ✓ |
| Complexity level | Medium-High | Low | N/A |

**When to use each:**
- **Skill**: Complex, reusable instructions with optional references/triggers. Most use cases.
- **Command**: Simple prompt template where you just need to fill in blanks (e.g., `/onboard $PROJECT_NAME`).
- **Just prompt it**: One-off tasks, exploratory questions, or things that vary too much to templatize.

---

## Step 2: The Quick Test (for skills/commands)

1. **Am I repeating this instruction pattern?** (>3 times = yes)
2. **Does it need to be consistent across sessions?** (same format/constraints = yes)
3. **Is this something the harness can't already do?** (check built-ins first)

| Result | Action |
|--------|--------|
| All three YES | Make a skill or command |
| Any is NO | Probably don't need one |

---

## Step 3: Scope Check

```
Is this harness-specific or should it work everywhere?
  |
  +-- Harness-specific
  |     -> Write directly in that harness's format
  |
  +-- Portable
        -> Write as canonical skill in Skillmania registry, deploy to targets
```

---

## Step 4: Complexity Check

```
What does it need?
  |
  +-- Just a prompt template with user input ($ARGUMENTS)?
  |     -> COMMAND: single {name}.md in ~/.claude/commands/
  |
  +-- Just instructions (no reference data, no arguments)?
  |     -> Simple SKILL: single SKILL.md
  |
  +-- Reference tables, checklists, or domain docs?
  |     -> Compound SKILL: SKILL.md + references/
  |
  +-- Multi-step workflow orchestration?
  |     -> Orchestration SKILL: SKILL.md that instructs Agent tool usage
  |
  +-- Needs to run actual code on events?
        -> NOT a skill/command. Use hooks (settings.json) instead.
```

---

## Step 5: Staleness Signals (audit quarterly)

- [ ] Harness now does this natively
- [ ] Skill references outdated APIs/tools/models
- [ ] Haven't invoked it in 2+ months
- [ ] Trigger keywords clash with other skills or built-ins
- [ ] Instructions conflict with current harness behavior

**If 2+ signals checked -> Retire or rewrite the skill.**

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It's Bad |
|-------------|-------------|
| "God skills" that handle everything | Impossible to maintain, conflicting instructions |
| Skills that just say "be better at X" | No specificity, model already tries this |
| Duplicate skills across harnesses | They drift apart, inconsistent behavior |
| Triggers so broad they fire on unrelated prompts | Wrong skill loading is worse than none |
| Putting hooks logic in a skill | Skills are instructions, not executables |
| Skipping the built-in check | Duplicating native features with worse quality |

---

## One-Line Decision

**Skill**: You've typed the same complex instructions 3+ times and wish the model "just knew" to do it that way.

**Command**: You have a workflow template where only the input changes (project name, file path, search term).

**Neither**: It is a one-off, exploratory task or varies too much to templatize: prompt it directly.
