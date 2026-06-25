#!/usr/bin/env python3
"""Lint AGENTS.md and AI context docs for obvious unfinished placeholders."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ANGLE_PLACEHOLDER_RE = re.compile(r"<[^>\n]+>")
TEXT_PLACEHOLDER_RE = re.compile(r"\b(?:TBD|TODO)\b", re.IGNORECASE)
REQUIRED_DOCS = (
    "00-index.md",
    "project-brief.md",
    "tech-baseline.md",
    "architecture.md",
    "domain-rules.md",
    "api-contracts.md",
    "frontend-guidelines.md",
    "testing-strategy.md",
    "git-workflow.md",
    "migration-map.md",
    "active-context.md",
    "context-health.md",
    "decisions.md",
)

CORE_DOCS = (
    "00-index.md",
    "tech-baseline.md",
    "architecture.md",
    "git-workflow.md",
    "active-context.md",
    "context-health.md",
)


def line_count(path: Path) -> int:
    try:
        return len(path.read_text(encoding="utf-8").splitlines())
    except OSError:
        return 0


def strip_inline_code(text: str) -> str:
    """Ignore placeholders inside backticks, such as `<type>/vX.Y.Z/<description>`."""
    return re.sub(r"`[^`\n]*`", "", text)


def has_unfinished_placeholder(text: str) -> bool:
    searchable = strip_inline_code(text)
    return bool(ANGLE_PLACEHOLDER_RE.search(searchable) or TEXT_PLACEHOLDER_RE.search(searchable))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True, help="Project root")
    parser.add_argument("--docs-dir", default="docs/ai", help="AI docs directory relative to project root")
    parser.add_argument("--profile", choices=("core", "full"), default="core")
    args = parser.parse_args()

    project = Path(args.project).expanduser().resolve()
    raw_docs_dir = args.docs_dir.strip()
    docs_candidate = Path(raw_docs_dir)
    if (
        not raw_docs_dir
        or docs_candidate.is_absolute()
        or docs_candidate.drive
        or any(part == ".." for part in docs_candidate.parts)
        or raw_docs_dir.startswith(("/", "\\"))
    ):
        raise SystemExit("--docs-dir must be a relative path inside the project")

    docs_dir = project / raw_docs_dir.strip("/\\")
    problems: list[str] = []

    agents = project / "AGENTS.md"
    if not agents.exists():
        problems.append("missing AGENTS.md")
    else:
        if line_count(agents) > 100:
            problems.append("AGENTS.md exceeds 100 lines")
        agents_text = agents.read_text(encoding="utf-8", errors="replace")
        if has_unfinished_placeholder(agents_text):
            problems.append("unfinished placeholders in AGENTS.md")

    required_docs = CORE_DOCS if args.profile == "core" else REQUIRED_DOCS
    for name in required_docs:
        path = docs_dir / name
        if not path.exists():
            problems.append(f"missing {args.docs_dir}/{name}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if has_unfinished_placeholder(text):
            problems.append(f"unfinished placeholders in {args.docs_dir}/{name}")

    if problems:
        for problem in problems:
            print(f"problem  {problem}")
        return 1

    print("ok       AI context lint passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
