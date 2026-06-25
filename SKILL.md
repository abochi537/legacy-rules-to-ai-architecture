---
name: legacy-rules-to-ai-architecture
description: Extract legacy rules into durable AI project context.
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

## Workflow

1. Confirm the target project root, the AI docs directory, and the user's
   preferred skills directory. Default AI docs to `docs/ai`. If the user does
   not want skills inside the repo, use their global or shared path.
2. Inspect the repository structure narrowly before reading deeply. Prefer
   CodeGraph if indexed; otherwise use fast file search and framework-specific
   entry points.
3. Create a feature inventory before deep extraction: routes/pages, API
   endpoints, jobs, commands, domain modules, shared components, and tests.
   Pick a bounded slice for each pass; do not try to fully reverse-engineer a
   large repository in one turn.
4. Identify the technical baseline: language, framework versions, routing,
   state management, API client, styling system, tests, build commands.
5. Extract architecture rules from existing boundaries: modules, layers,
   dependency direction, shared packages, API conventions, and forbidden shortcuts.
6. Extract domain rules by feature area. Every rule needs evidence: file path
   with line, symbol, route, schema, database field, fixture, log, screenshot,
   product doc, or test. Record confidence and last verified date.
7. Extract frontend consistency rules: layout primitives, page patterns,
   component library, design tokens, forms, tables, dialogs, loading/error/empty
   states, responsive behavior, canonical screenshots, breakpoint matrix, and
   visual-regression gaps.
8. Separate canonical patterns from deprecated or conflicting patterns. If the
   legacy codebase has multiple implementations, write a decision entry before
   turning one into a hard rule.
9. Create `AGENTS.md` with no more than 100 lines. Keep it as a contract and
   navigation file, not a full knowledge base. Existing files require explicit
   merge/diff review before editing.
10. Create `<ai-docs-dir>/*` using the templates in
    `references/context-templates.md`.
11. Capture Git and release governance. If the user wants CSG-style Git
    governance, use `Links17/csg-git-skill` as the source of truth and write
    project-specific notes to `<ai-docs-dir>/git-workflow.md`.
12. Recommend machine-checkable gates: typecheck, unit/integration tests,
   dependency checks, API contract tests, lint rules, AST rules, Storybook or
   visual regression.
13. Only after stable patterns emerge, create optional workflow skills for
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

## Quick Scaffold

To create the starter context files in a project without overwriting existing
files, invoke through the `terminal` tool:

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
