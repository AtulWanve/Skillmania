#!/usr/bin/env python3
"""Audit skill registry for prohibited language, em dashes, and AI writing patterns."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "registry"

# Exclude humanizer itself since it defines and cites these patterns as examples to catch
EXCLUDED_SKILLS = {"humanizer"}

BUZZWORDS = [
    r"\bdelve\b",
    r"\btestament\b",
    r"\btapestry\b",
    r"\bparadigm\b",
    r"\bsubstrate\b",
    r"\bbeacon\b",
    r"\bmultifaceted\b",
    r"\binterplay\b",
    r"\bintricacies\b",
    r"\bvibrant\b",
    r"\bmeticulous(?:ly)?\b",
    r"\bpivotal\b",
    r"\blandscape\b",
    r"\bleverage\b",
]

STAGING_PATTERNS = [
    r"\bnot\s+just\b",
    r"\bnot\s+only\b",
    r"\blet['’]s\s+dive\s+in\b",
    r"\bit\s+is\s+worth\s+noting\b",
    r"\bfurthermore\b",
    r"\bmoreover\b",
    r"\bthat\s+is\s+the\s+real\s+win\b",
    r"\blet\s+that\s+sink\s+in\b",
]

META_JARGON = [
    r"room/lens",
    r"lens\s+scaffolding",
    r"artifact\s+purity",
    r"process\s+leak",
]


def audit() -> int:
    if not REGISTRY.is_dir():
        print(f"Error: Registry not found at {REGISTRY}")
        return 1

    total_violations = 0
    file_count = 0
    violating_files = set()
    violations_by_category: dict[str, list[dict[str, str | int]]] = {
        "em_dash": [],
        "buzzwords": [],
        "staging": [],
        "meta_jargon": [],
    }

    md_files = [p for p in REGISTRY.rglob("*.md") if not any(x in p.parts for x in EXCLUDED_SKILLS)]

    for path in sorted(md_files):
        file_count += 1
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except Exception as exc:
            print(f"Error reading {path}: {exc}")
            continue

        rel_path = path.relative_to(ROOT)

        for line_idx, line in enumerate(lines, 1):
            # 1. Em dash check
            if "—" in line:
                violations_by_category["em_dash"].append({
                    "file": str(rel_path),
                    "line": line_idx,
                    "text": line.strip()[:100],
                })
                violating_files.add(str(rel_path))
                total_violations += 1

            # 2. Buzzwords check
            for pattern in BUZZWORDS:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    violations_by_category["buzzwords"].append({
                        "file": str(rel_path),
                        "line": line_idx,
                        "word": match.group(0),
                        "text": line.strip()[:100],
                    })
                    violating_files.add(str(rel_path))
                    total_violations += 1

            # 3. Staging check
            for pattern in STAGING_PATTERNS:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    violations_by_category["staging"].append({
                        "file": str(rel_path),
                        "line": line_idx,
                        "pattern": match.group(0),
                        "text": line.strip()[:100],
                    })
                    violating_files.add(str(rel_path))
                    total_violations += 1

            # 4. Meta-jargon check
            for pattern in META_JARGON:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    violations_by_category["meta_jargon"].append({
                        "file": str(rel_path),
                        "line": line_idx,
                        "jargon": match.group(0),
                        "text": line.strip()[:100],
                    })
                    violating_files.add(str(rel_path))
                    total_violations += 1

    print("=" * 60)
    print("SKILL REGISTRY LANGUAGE AUDIT RESULTS")
    print("=" * 60)
    print(f"Total markdown files audited: {file_count}")
    print(f"Files with violations: {len(violating_files)}")
    print(f"Total violations found: {total_violations}")
    print("-" * 60)
    print(f"Em dashes:        {len(violations_by_category['em_dash'])}")
    print(f"Stock buzzwords:  {len(violations_by_category['buzzwords'])}")
    print(f"Staged openers:   {len(violations_by_category['staging'])}")
    print(f"Meta-jargon:      {len(violations_by_category['meta_jargon'])}")
    print("=" * 60)

    if violating_files:
        print("\nAffected files by skill:")
        skills_affected: dict[str, list[str]] = {}
        for f in sorted(violating_files):
            parts = Path(f).parts
            skill_name = parts[1] if len(parts) > 1 else "root"
            skills_affected.setdefault(skill_name, []).append(f)

        for skill, files in sorted(skills_affected.items()):
            print(f"\n[{skill}] ({len(files)} files):")
            for f in files:
                print(f"  - {f}")

    return 0


if __name__ == "__main__":
    sys.exit(audit())
