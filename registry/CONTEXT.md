# Registry

## Inputs
- Skill ideas, existing skills from harnesses (imported), or user-authored skill specs.
- Canonical format: each skill is a subfolder containing a `skill.md` (the core instructions), optional `references/` subfolder, and a `meta.yaml` (target harnesses, triggers, staleness date, status).

## Process
- Single source of truth for every skill. A skill exists here first, then gets deployed to harnesses.
- Skills are harness-agnostic in their canonical form. Harness-specific adaptations happen at deploy time.
- Each skill subfolder is self-contained: you can understand what it does by reading its contents alone.
- **Intake and Sanitization**: When importing an external skill, run `skill-inspector` before installation. Strip all upstream packaging metadata (licenses, authors, versions, credits) from `skill.md` frontmatter and remove platform-specific interface files that are not used by supported harnesses.
- **Template Hygiene**: Reference templates and schemas must use angle-bracket tokens (`<...>`) instead of realistic dummy prose or parenthetical instructions to prevent agents from copying placeholder text into deliverables.

## Outputs
- Canonical skill definitions consumed by `scripts/` for deployment to target harnesses.
- Skill metadata consumed by `audit/` for health checks.
