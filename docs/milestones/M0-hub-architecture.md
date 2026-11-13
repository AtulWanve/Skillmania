# Milestone M0: Hub Architecture & Canonical Registry

## Objective
Establish the foundational hub architecture, harness specifications, subsystem boundaries, and canonical registry of 27 skills.

## Scope & Issues
- [x] Issue #1: Target Harness Integration Specifications (resolved by PR #2)
- [x] Issue #3: Skill Authoring Guides, Decision Framework & Subsystem Boundaries (resolved by PR #4)
- [x] Issue #5: Canonical Skills Registry Baseline (resolved by PR #6)
- [x] Issue #7: Milestone M0 Capstone Verification & Baseline Audit (resolved by PR #8)

## Acceptance Criteria
<!-- Mandatory criteria that must be satisfied before this milestone is closed -->
This milestone is COMPLETE:
- [x] 1. All core project directories have valid, up-to-date `CONTEXT.md` files defining inputs, processes, and outputs.
- [x] 2. Local tooling (Ruff, Bandit, and `scripts/validate_registry.py`) and CI workflow (`.github/workflows/ci.yml`) pass with zero errors.
- [x] 3. Target harness specifications are documented for Claude Code and OpenCode in `harnesses/`.
- [x] 4. Exactly 27 canonical skills are tracked in `registry/` with self-contained `skill.md` and `meta.yaml` definitions.
- [x] 5. Untracked prototype assets (`comment/` and `SEED Turn a Raw Idea Into a PAUL-Ready Build Plan.md`) remain isolated on disk with zero git tracking.
- [x] 6. All phase task commits are recorded on `main` with 1:1 resolution linking to issues.

## Downstream Transition
- **Next Milestone**: M1: Automation Scripts & Harness Sync Engine
- **Prerequisites**: M1 tasks cannot be merged until M0 Acceptance Criteria pass.
