#!/usr/bin/env python3
"""Canonical skill registry and context architecture validator.

Validates that:
1. Primary workspace directories contain valid CONTEXT.md files.
2. Every skill in registry/ contains skill.md and a valid meta.yaml.
3. meta.yaml schema adheres to required fields and directory name matching.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

PRIMARY_DIRECTORIES = [
    ".github",
    "audit",
    "docs",
    "harnesses",
    "registry",
    "scripts",
]

REQUIRED_META_FIELDS = {
    "name": str,
    "description": str,
    "status": str,
    "targets": list,
}


def validate_context_files(errors: list[str]) -> None:
    """Validate presence and basic structure of CONTEXT.md files."""
    root_context = ROOT / "CONTEXT.md"
    if not root_context.is_file():
        errors.append("Missing root CONTEXT.md file.")

    for folder_name in PRIMARY_DIRECTORIES:
        folder = ROOT / folder_name
        if not folder.is_dir():
            errors.append(f"Primary directory not found: {folder_name}/")
            continue

        context_file = folder / "CONTEXT.md"
        if not context_file.is_file():
            errors.append(f"Missing CONTEXT.md in primary directory: {folder_name}/")
        elif context_file.stat().st_size == 0:
            errors.append(f"Empty CONTEXT.md in: {folder_name}/")


def validate_skill_metadata(skill_dir: Path, errors: list[str]) -> None:
    """Validate skill.md and meta.yaml for a single skill directory."""
    skill_name = skill_dir.name

    skill_md = skill_dir / "skill.md"
    if not skill_md.is_file():
        errors.append(f"[{skill_name}] Missing skill.md entrypoint.")
    elif skill_md.stat().st_size == 0:
        errors.append(f"[{skill_name}] Empty skill.md file.")
    else:
        text = skill_md.read_text(encoding="utf-8")
        if text.startswith("---"):
            parts = text.split("---", 2)
            if len(parts) >= 3:
                try:
                    fm = yaml.safe_load(parts[1])
                    if isinstance(fm, dict):
                        prohibited_keys = {
                            "license", "author", "metadata", "credits", "version", "copyright"
                        }
                        found = prohibited_keys.intersection(fm.keys())
                        if found:
                            key_list = ", ".join(sorted(found))
                            errors.append(
                                f"[{skill_name}] skill.md frontmatter contains "
                                f"prohibited packaging field(s): {key_list}"
                            )
                except yaml.YAMLError as exc:
                    errors.append(f"[{skill_name}] Malformed YAML in skill.md frontmatter: {exc}")

        for doc in skill_dir.rglob("*.md"):
            try:
                doc_text = doc.read_text(encoding="utf-8")
                if re.search(r"[a-zA-Z]:[\\/]Users[\\/]", doc_text, re.I):
                    rel_path = doc.relative_to(skill_dir)
                    errors.append(
                        f"[{skill_name}] {rel_path} contains hardcoded local user path."
                    )
            except Exception as exc:
                errors.append(f"[{skill_name}] Error reading {doc.name}: {exc}")

    meta_file = skill_dir / "meta.yaml"
    if not meta_file.is_file():
        errors.append(f"[{skill_name}] Missing meta.yaml.")
        return

    try:
        content = meta_file.read_text(encoding="utf-8")
        data = yaml.safe_load(content)
    except Exception as exc:
        errors.append(f"[{skill_name}] Malformed YAML in meta.yaml: {exc}")
        return

    if not isinstance(data, dict):
        errors.append(f"[{skill_name}] meta.yaml must be a key-value mapping.")
        return

    for field, expected_type in REQUIRED_META_FIELDS.items():
        if field not in data:
            errors.append(f"[{skill_name}] meta.yaml missing required field: '{field}'")
        elif not isinstance(data[field], expected_type):
            errors.append(
                f"[{skill_name}] meta.yaml field '{field}' must be {expected_type.__name__}, "
                f"got {type(data[field]).__name__}"
            )

    declared_name = data.get("name")
    if declared_name and declared_name != skill_name:
        errors.append(
            f"[{skill_name}] meta.yaml 'name' ({declared_name!r}) does not match "
            f"directory name ({skill_name!r})."
        )

    status = data.get("status")
    targets = data.get("targets", [])
    if isinstance(targets, list):
        if len(targets) == 0 and status != "archived":
            errors.append(f"[{skill_name}] meta.yaml 'targets' list must not be empty.")
        for target in targets:
            if not isinstance(target, str) or not target.strip():
                errors.append(f"[{skill_name}] meta.yaml targets must contain non-empty strings.")


def validate_registry(errors: list[str]) -> int:
    """Validate all skill folders inside registry/."""
    registry_dir = ROOT / "registry"
    if not registry_dir.is_dir():
        errors.append("Registry directory 'registry/' does not exist.")
        return 0

    skills = [p for p in registry_dir.iterdir() if p.is_dir()]
    if not skills:
        errors.append("Registry directory 'registry/' contains no skill subdirectories.")
        return 0

    for skill_dir in sorted(skills):
        validate_skill_metadata(skill_dir, errors)

    return len(skills)


def main() -> int:
    """Run validation checks and report outcome."""
    errors: list[str] = []

    validate_context_files(errors)
    skill_count = validate_registry(errors)

    if errors:
        print(f"Validation failed with {len(errors)} error(s):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(
        f"Validation passed: Verified root architecture and {skill_count} "
        "canonical skills in registry/."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
