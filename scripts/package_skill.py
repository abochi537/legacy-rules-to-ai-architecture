#!/usr/bin/env python3
"""Package this skill into an installable zip artifact."""

from __future__ import annotations

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


SKILL_NAME = "legacy-rules-to-ai-architecture"
PACKAGE_FILES = (
    "SKILL.md",
    "README.md",
    "agents/openai.yaml",
    "references/context-templates.md",
    "references/extraction-checklist.md",
    "references/workflow-skill-template.md",
    "scripts/lint_ai_context.py",
    "scripts/scaffold_ai_context.py",
)
FORBIDDEN_PARTS = (".git", "__pycache__")
FORBIDDEN_SUFFIXES = (".pyc",)


def package_skill(skill_dir: Path, output: Path) -> list[str]:
    output.parent.mkdir(parents=True, exist_ok=True)
    names: list[str] = []
    with ZipFile(output, "w", ZIP_DEFLATED) as zf:
        for rel in PACKAGE_FILES:
            src = skill_dir / rel
            if not src.exists():
                raise FileNotFoundError(f"missing package file: {src}")
            arcname = str(Path(SKILL_NAME) / rel).replace("\\", "/")
            zf.write(src, arcname)
            names.append(arcname)
    return names


def validate_zip(output: Path) -> list[str]:
    problems: list[str] = []
    with ZipFile(output) as zf:
        names = zf.namelist()
    expected = [str(Path(SKILL_NAME) / rel).replace("\\", "/") for rel in PACKAGE_FILES]
    if names != expected:
        problems.append("zip file list does not match PACKAGE_FILES")
    for name in names:
        parts = Path(name).parts
        if any(part in FORBIDDEN_PARTS for part in parts) or name.endswith(FORBIDDEN_SUFFIXES):
            problems.append(f"forbidden artifact in zip: {name}")
    return problems


def main() -> int:
    skill_dir = Path(__file__).resolve().parents[1]
    default_output = skill_dir / "dist" / f"{SKILL_NAME}.zip"
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(default_output), help="Zip artifact path")
    args = parser.parse_args()

    output = Path(args.output).expanduser().resolve()
    names = package_skill(skill_dir, output)
    problems = validate_zip(output)
    if problems:
        for problem in problems:
            print(f"problem  {problem}")
        return 1

    print(f"created  {output}")
    print(f"files    {len(names)}")
    for name in names:
        print(f"include  {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
