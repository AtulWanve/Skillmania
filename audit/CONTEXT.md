# Audit

## Inputs
- Skill registry metadata (staleness dates, usage flags, target harnesses).
- Current harness capabilities (to detect skills that duplicate built-in features).

## Process
- Health checks: flag skills past their staleness date, skills with no recorded usage, or skills that overlap with harness built-ins.
- Generate audit reports showing skill status across all harnesses.

## Outputs
- Audit reports (markdown or structured data) listing skills by health status.
- Recommended actions: upgrade, retire, or keep.
