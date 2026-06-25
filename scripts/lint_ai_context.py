#!/usr/bin/env python3
"""Lint AGENTS.md and AI context docs for obvious unfinished placeholders.

The linter is intentionally scoped to starter-template residue. Project context
docs often contain Markdown autolinks, HTML/XML fragments, and domain words such
as "Todo"; those are valid evidence and must not be treated as unfinished work.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ANGLE_TOKEN_RE = re.compile(r"<[^>\n]+>")
TODO_MARKER_RE = re.compile(r"(?<![\w-])(?:TODO|TBD)(?=\s*(?:[:\-]|$))", re.IGNORECASE)
TAG_NAME_RE = re.compile(r"^<([A-Za-z][\w:-]*)>$")
KNOWN_ANGLE_PLACEHOLDERS = frozenset(
    {
        "<project-name>",
        "<one-paragraph product purpose>",
        "<legacy extraction | migration | rebuild | maintenance>",
        "<brief target>",
        "<command or TBD>",
        "<workspace/package/module notes>",
        "<What the system does and for whom.>",
        "<Things the rebuild must not attempt yet.>",
        "<README, product docs, routes, tests, demos, or user notes.>",
        "<title>",
        "<What the current AI/developer session is trying to complete.>",
        "<One concrete next step.>",
    }
)
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


def strip_markdown_code(text: str) -> str:
    """Ignore placeholders inside fenced and inline code examples."""
    without_fences = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    return re.sub(r"`[^`\n]*`", "", without_fences)


def is_balanced_xml_tag(line: str, token: str, end: int) -> bool:
    """Return true when `<name>` is evidence markup rather than a placeholder."""
    match = TAG_NAME_RE.match(token)
    if not match:
        return False
    return f"</{match.group(1)}>" in line[end:]


def has_unfinished_placeholder(text: str) -> bool:
    searchable = strip_markdown_code(text)
    has_known_angle_placeholder = False
    for line in searchable.splitlines():
        for match in ANGLE_TOKEN_RE.finditer(line):
            token = match.group(0)
            if token in KNOWN_ANGLE_PLACEHOLDERS and not is_balanced_xml_tag(line, token, match.end()):
                has_known_angle_placeholder = True
                break
        if has_known_angle_placeholder:
            break
    return bool(has_known_angle_placeholder or TODO_MARKER_RE.search(searchable))


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
