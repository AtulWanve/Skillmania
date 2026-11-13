# Scripts

## Inputs
- Canonical skills from `registry/`, format specs from `harnesses/`, audit rules from `audit/`.

## Process
- `validate_registry.py`: Validates canonical skill definitions (`skill.md`, `meta.yaml`) and workspace context files.
- `deploy`: Transform a canonical skill into harness-native format and copy it to the correct deploy path.
- `import`: Pull an existing skill from a harness install into the registry as canonical form.
- `audit`: Run health checks across all registered skills and produce a report.
- `sync`: Ensure deployed skills match their canonical registry versions (detect drift).

## Outputs
- Validation reports and exit codes for CI and local health checks.
- Deployed skill files in harness-specific locations.
- Imported canonical skills in the registry.
- Audit and sync reports.
