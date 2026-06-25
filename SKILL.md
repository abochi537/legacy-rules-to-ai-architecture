---
name: legacy-rules-to-ai-architecture
description: Use whenever the user wants to analyze a legacy codebase, extract existing behavior rules, initialize AGENTS.md/docs/ai context, rebuild or migrate with stable architecture, or keep frontend pages consistent across AI coding sessions. Default to running the bundled scaffold/lint scripts yourself; do not make the user manually execute scripts unless tooling or permissions block execution.
---

# Legacy Rules To AI Architecture

Use this skill when the user wants AI to recover behavior and implementation
rules from an existing codebase, then use those rules to guide a rebuild,
migration, or long-running AI development effort. The output is not "one huge
memory file"; it is a small project contract plus evidence-backed docs and
optional workflow skills stored wherever the user prefers.

## Core Principle

Build a durable project context that future agents must read before coding:

- `AGENTS.md`: short project contract, hard rules, and navigation.
- `<ai-docs-dir>/*`: evidence-backed project knowledge and migration context.
- Optional skills: reusable workflows, stored in a user-chosen skills directory.
- Optional Git governance: call or install `Links17/csg-git-skill` when the
  project needs SemVer, branch naming, commit, tag, test-release, or release rules.
- Checks: tests, dependency rules, API contracts, and visual regression where available.

Do not invent missing business rules. If evidence is missing, write `Unknown`
and list what source would be needed.

## User Experience Contract

The user should be able to invoke this skill with one natural-language request.
Do not require them to know script paths or copy/paste scaffold commands.

When this skill is triggered for a concrete project:

1. Resolve the target project root. If the user did not specify one, use the
   current workspace root. Ask only when multiple plausible roots exist or the
   target is unsafe.
2. Resolve the AI docs directory. Default to `docs/ai`; use the user's preferred
   path if they name one.
3. Run `scripts/scaffold_ai_context.py` through the terminal tool yourself
   unless the user explicitly requested read-only analysis or no file writes.
4. After extracting or updating rules, run `scripts/lint_ai_context.py` yourself.
5. Report what was created, what already existed, what still has placeholders,
   and what evidence is missing.

Only show manual commands when execution is blocked by missing Python, missing
terminal access, filesystem permissions, or an explicit read-only request.

## Workflow

1. Resolve the target project root, the AI docs directory, and the user's
   preferred skills directory. Default AI docs to `docs/ai`. If the user does
   not want skills inside the repo, use their global or shared path.
2. Run the scaffold script yourself to create the starter durable context
   without overwriting existing files. Use `core` by default; use `full` when
   the user explicitly asks for a migration/rebuild context or broad rule
   extraction.
3. Inspect the repository structure narrowly before reading deeply. Prefer
   CodeGraph if indexed; otherwise use fast file search and framework-specific
   entry points.
4. Create a feature inventory before deep extraction: routes/pages, API
   endpoints, jobs, commands, domain modules, shared components, and tests.
   Pick a bounded slice for each pass; do not try to fully reverse-engineer a
   large repository in one turn.
5. Identify the technical baseline: language, framework versions, routing,
   state management, API client, styling system, tests, build commands.
6. Extract architecture rules from existing boundaries: modules, layers,
   dependency direction, shared packages, API conventions, and forbidden shortcuts.
7. Extract domain rules by feature area. Every rule needs evidence: file path
   with line, symbol, route, schema, database field, fixture, log, screenshot,
   product doc, or test. Record confidence and last verified date.
8. Extract frontend consistency rules: layout primitives, page patterns,
   component library, design tokens, forms, tables, dialogs, loading/error/empty
   states, responsive behavior, canonical screenshots, breakpoint matrix, and
   visual-regression gaps.
9. Separate canonical patterns from deprecated or conflicting patterns. If the
   legacy codebase has multiple implementations, write a decision entry before
   turning one into a hard rule.
10. Keep `AGENTS.md` at no more than 100 lines. Keep it as a contract and
   navigation file, not a full knowledge base. Existing files require explicit
   merge/diff review before editing.
11. Create or update `<ai-docs-dir>/*` using the templates in
    `references/context-templates.md`.
12. Capture Git and release governance. If the user wants CSG-style Git
    governance, use `Links17/csg-git-skill` as the source of truth and write
    project-specific notes to `<ai-docs-dir>/git-workflow.md`.
13. Recommend machine-checkable gates: typecheck, unit/integration tests,
   dependency checks, API contract tests, lint rules, AST rules, Storybook or
   visual regression.
14. Run the lint script yourself and fix or report any placeholders or missing
    context files.
15. Only after stable patterns emerge, create optional workflow skills for
    repeatable tasks such as `migrate-feature`, `add-api-endpoint`,
    `add-page`, or `preserve-frontend-consistency`.

## Long-Term Maintenance Loop

At the start of a multi-turn task, read `AGENTS.md`, `<ai-docs-dir>/00-index.md`,
and `<ai-docs-dir>/active-context.md`. For frontend work, also read
`frontend-guidelines.md`; for API/backend work, read `api-contracts.md`; for
migration work, read `migration-map.md` and `domain-rules.md`.

At the end of a multi-turn task, update `active-context.md` with the current
goal, recent decisions, open questions, and next safe step. If a rule changed,
update the owning doc and record weak or stale areas in `context-health.md`.
If competing patterns were discovered, add or update an entry in `decisions.md`.

Before handoff or PR, run the project's required checks from `AGENTS.md`, then
record the date, command, and result in `context-health.md`.

## Automatic Scaffold

Run the starter context scaffold yourself through the terminal tool. Do not ask
the user to run this manually unless execution is blocked:

```bash
python <skill-dir>/scripts/scaffold_ai_context.py --project <project-root>
```

This default `core` profile creates only `AGENTS.md`, `00-index.md`,
`tech-baseline.md`, `architecture.md`, `active-context.md`, and
`context-health.md`. For a full migration/rebuild context, use:

```bash
python <skill-dir>/scripts/scaffold_ai_context.py --project <project-root> --profile full
```

Use a custom docs directory if the user dislikes `docs/ai`:

```bash
python <skill-dir>/scripts/scaffold_ai_context.py --project <project-root> --docs-dir .ai/context
```

The script only writes missing files. After scaffolding, fill each section with
evidence from the actual codebase.

Check for obvious unfinished context:

```bash
python <skill-dir>/scripts/lint_ai_context.py --project <project-root>
```

## Output Contract

When finishing an extraction pass, report:

- `AGENTS.md` status: created, merge needed, or already existed.
- `<ai-docs-dir>` status: files created, missing, or unresolved sections.
- Top rules extracted, grouped by architecture, domain, API, frontend, and tests.
- Evidence gaps that need user input, runtime traces, logs, or product docs.
- Conflicts between legacy patterns and the canonical pattern chosen.
- Suggested checks that should become CI gates.
- Optional skills worth creating and the directory where the user wants them.

## When To Read References

- Read `references/context-templates.md` before creating `AGENTS.md` or
  `<ai-docs-dir>/*`.
- Read `references/extraction-checklist.md` before analyzing an unfamiliar
  repository or writing evidence-backed rules.
- Read `references/workflow-skill-template.md` before creating optional skills.
- If the task involves Git versioning, branch naming, commit messages, tags,
  test-release docs, CSG Base, hotfixes, or release flow, invoke the installed
  `csg-git-skill` or tell the user to install it from
  `https://github.com/Links17/csg-git-skill`.

## Pitfalls

- Do not summarize the whole repo into a single skill. Skills capture reusable
  procedures; project facts belong in `<ai-docs-dir>/*`.
- Do not treat comments or current implementation as truth without corroborating
  behavior when the rule is high-risk.
- Do not allow frontend consistency to remain prose-only. Recommend tokens,
  component inventory, Storybook, screenshots, or visual regression checks.
- Do not let `AGENTS.md` exceed about 100 lines. Long context belongs in docs.
- Do not place generated skills in the project root unless the user explicitly
  prefers that location.

## Verification

After writing or updating project context, verify:

```bash
python <skill-dir>/scripts/scaffold_ai_context.py --project <project-root> --check
python <skill-dir>/scripts/lint_ai_context.py --project <project-root>
```

If the project used the full profile, include `--profile full` in both commands
so domain, API, frontend, migration, and decision docs are also checked.

Then run the project's discovered quality gates, at minimum typecheck or tests
when available.
