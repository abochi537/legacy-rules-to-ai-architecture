from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile


REPO_ROOT = Path(__file__).resolve().parents[1]
SCAFFOLD = REPO_ROOT / "scripts" / "scaffold_ai_context.py"
LINT = REPO_ROOT / "scripts" / "lint_ai_context.py"
PACKAGE = REPO_ROOT / "scripts" / "package_skill.py"
CORE_DOCS = (
    "00-index.md",
    "tech-baseline.md",
    "architecture.md",
    "git-workflow.md",
    "active-context.md",
    "context-health.md",
)
PACKAGE_NAMES = [
    "legacy-rules-to-ai-architecture/SKILL.md",
    "legacy-rules-to-ai-architecture/README.md",
    "legacy-rules-to-ai-architecture/agents/openai.yaml",
    "legacy-rules-to-ai-architecture/references/context-templates.md",
    "legacy-rules-to-ai-architecture/references/extraction-checklist.md",
    "legacy-rules-to-ai-architecture/references/workflow-skill-template.md",
    "legacy-rules-to-ai-architecture/scripts/lint_ai_context.py",
    "legacy-rules-to-ai-architecture/scripts/scaffold_ai_context.py",
]


def run_script(script: Path, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *args],
        cwd=cwd or REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def write_clean_core_project(project: Path) -> None:
    docs = project / "docs" / "ai"
    docs.mkdir(parents=True)
    (project / "AGENTS.md").write_text(
        "# AGENTS.md\n\n"
        "## Project Contract\n"
        "Read docs/ai/00-index.md before coding.\n",
        encoding="utf-8",
    )
    for name in CORE_DOCS:
        (docs / name).write_text(f"# {name}\n\nContent is filled.\n", encoding="utf-8")


class CliSmokeTests(unittest.TestCase):
    def test_scaffold_core_creates_git_workflow(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)

            result = run_script(SCAFFOLD, "--project", str(project))
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

            self.assertTrue((project / "AGENTS.md").exists())
            for name in CORE_DOCS:
                self.assertTrue((project / "docs" / "ai" / name).exists(), name)

            check = run_script(SCAFFOLD, "--project", str(project), "--check")
            self.assertEqual(check.returncode, 0, check.stderr + check.stdout)

    def test_lint_allows_evidence_links_html_and_todo_domain_words(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            write_clean_core_project(project)
            architecture = project / "docs" / "ai" / "architecture.md"
            architecture.write_text(
                "# Architecture\n\n"
                "- Evidence: <https://example.com/spec>\n"
                "- HTML evidence: <feature enabled=\"true\">stable</feature>\n"
                "- HTML title evidence: <title>Home</title>\n"
                "- Covered domain: Todo lifecycle\n",
                encoding="utf-8",
            )

            result = run_script(LINT, "--project", str(project))
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertIn("AI context lint passed", result.stdout)

    def test_lint_rejects_known_template_placeholders(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            write_clean_core_project(project)
            (project / "AGENTS.md").write_text(
                "# AGENTS.md\n\n"
                "## Project Summary\n"
                "- Name: <project-name>\n",
                encoding="utf-8",
            )
            (project / "docs" / "ai" / "architecture.md").write_text(
                "# Architecture\n\n"
                "### RULE-001 <title>\n"
                "- Evidence: missing.\n",
                encoding="utf-8",
            )

            result = run_script(LINT, "--project", str(project))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unfinished placeholders in AGENTS.md", result.stdout)
            self.assertIn("unfinished placeholders in docs/ai/architecture.md", result.stdout)

    def test_lint_rejects_explicit_todo_markers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            write_clean_core_project(project)
            (project / "docs" / "ai" / "context-health.md").write_text(
                "# Context Health\n\nTODO: fill verification evidence.\n",
                encoding="utf-8",
            )

            result = run_script(LINT, "--project", str(project))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unfinished placeholders in docs/ai/context-health.md", result.stdout)

    def test_lint_rejects_explicit_tbd_markers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            write_clean_core_project(project)
            (project / "docs" / "ai" / "context-health.md").write_text(
                "# Context Health\n\nTBD: add owner.\n",
                encoding="utf-8",
            )

            result = run_script(LINT, "--project", str(project))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unfinished placeholders in docs/ai/context-health.md", result.stdout)

    def test_package_skill_creates_clean_install_zip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "legacy-rules-to-ai-architecture.zip"

            result = run_script(PACKAGE, "--output", str(output))
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

            with ZipFile(output) as zf:
                names = zf.namelist()
            self.assertEqual(names, PACKAGE_NAMES)
            self.assertFalse(any(".git" in name for name in names))
            self.assertFalse(any("__pycache__" in name for name in names))
            self.assertFalse(any(name.endswith(".pyc") for name in names))


if __name__ == "__main__":
    unittest.main()
