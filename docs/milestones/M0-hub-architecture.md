# Milestone M0: Hub Architecture & Canonical Registry

## Objective
Establish the foundational hub architecture, harness specifications, subsystem boundaries, and canonical registry of 27 skills.

## Scope & Issues
- [ ] Issue #1: Repository Hygiene, Context Architecture & Milestone Baseline
- [ ] Issue #2: Target Harness Integration Specifications
- [ ] Issue #3: Skill Authoring Guides, Decision Framework & Subsystem Boundaries
- [ ] Issue #4: Canonical Skills Registry Baseline
- [ ] Issue #5: Milestone M0 Capstone Verification & Baseline Audit

## Acceptance Criteria
<!-- Mandatory criteria that must be satisfied before this milestone is closed -->
This milestone is COMPLETE only when:
1. All core project directories have valid, up-to-date `CONTEXT.md` files defining inputs, processes, and outputs.
2. Local tooling (Ruff, Bandit, and `scripts/validate_registry.py`) and CI workflow (`.github/workflows/ci.yml`) pass with zero errors.
3. Target harness specifications are documented for Claude Code and OpenCode in `harnesses/`.
4. Exactly 27 canonical skills are tracked in `registry/` with self-contained `skill.md` and `meta.yaml` definitions.
5. Untracked prototype assets (`comment/` and `SEED Turn a Raw Idea Into a PAUL-Ready Build Plan.md`) remain isolated on disk with zero git tracking.
6. All 5 discrete task commits are recorded on `main` with 1:1 mapping to issues.

## Downstream Transition
- **Next Milestone**: M1: Automation Scripts & Harness Sync Engine
- **Prerequisites**: M1 tasks cannot be merged until M0 Acceptance Criteria pass.
