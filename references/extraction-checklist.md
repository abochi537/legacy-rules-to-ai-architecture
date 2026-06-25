# Extraction Checklist

Use this checklist when analyzing an existing codebase before a rebuild or
migration. Keep every durable statement tied to evidence.

## Repository Intake

- Detect project root, package manager, workspaces, framework, app entries.
- Locate routing, pages, API handlers, API clients, state management, database
  access, auth, permissions, feature flags, config, tests, and CI.
- Prefer existing indexes such as CodeGraph when present. Otherwise use fast
  file search and framework conventions.
- Do not read the whole repository linearly unless the project is tiny.

## Slice Planning

- Build a feature inventory before deep analysis: route/page, API endpoint,
  job/command, domain module, shared component, and test coverage.
- Pick a bounded slice for each pass. A good slice is one feature workflow, one
  API family, or one frontend page family.
- Record skipped areas in `active-context.md` so future passes know what remains.
- Stop when the slice has enough evidence to write rules with confidence, not
  when every file has been skimmed.

## Business Rule Extraction

For each feature area:

- Identify user-facing routes, pages, or commands.
- Trace data entry points, validation, transformations, persistence, and output.
- Read tests, fixtures, schemas, and seed data before inferring behavior.
- Capture exceptional paths: permissions, disabled states, empty states, error
  handling, retries, timeouts, concurrency, and idempotency.
- Record rule confidence:
  - High: code plus tests or runtime behavior agree.
  - Medium: code path is clear but tests/runtime evidence are missing.
  - Low: rule is inferred from naming, comments, or partial code only.

## Architecture Extraction

- Identify layers and allowed dependency direction.
- List shared abstractions that must be reused.
- Find duplicate patterns that should be unified during rebuild.
- Identify places where the old system violates its intended architecture.
- Separate canonical patterns from deprecated or accidental patterns.
- If old code and tests disagree, record a conflict instead of choosing silently.
- Convert important boundaries into lint, dependency, or AST checks where possible.

## Frontend Consistency Extraction

- Inventory existing layouts, route shells, navigation, page density, spacing,
  typography, color tokens, component variants, forms, tables, modals, drawers,
  toasts, charts, loading states, empty states, and error states.
- Identify canonical pages that future AI work should imitate.
- Record anti-patterns already present so future work does not replicate them.
- Recommend Storybook stories or Playwright screenshots for critical components.

## API And Data Extraction

- Identify source of truth: OpenAPI, GraphQL schema, route handlers, client
  types, database migrations, ORM models, generated clients, fixtures.
- Capture request/response contracts and error shapes.
- Link API rules to UI consumers and tests.
- Recommend contract tests for behavior that must survive migration.

## Validation Plan

- Characterization tests for legacy behavior.
- Dependency/layer checks for architecture drift.
- Typecheck and lint for baseline safety.
- API contract tests for backend compatibility.
- Visual regression for frontend consistency.
- Golden master or approval tests for complex generated output.

## Open Source Practice Mapping

Use these when they fit the project:

| Practice | Purpose | Context file |
| --- | --- | --- |
| ADR / decisions log | Record canonical choices and rejected alternatives | `decisions.md` |
| CODEOWNERS / reviewers | Make ownership explicit | `architecture.md` |
| CONTRIBUTING / required checks | Turn AI rules into human workflow | `testing-strategy.md` |
| dependency-cruiser / import rules | Enforce layer boundaries | `architecture.md` |
| eslint / ast-grep / semgrep | Enforce code-shape and forbidden patterns | `architecture.md` |
| OpenAPI / GraphQL schema | Lock API contracts | `api-contracts.md` |
| Schemathesis / contract tests | Verify backend compatibility | `testing-strategy.md` |
| Storybook | Document UI component states | `frontend-guidelines.md` |
| Playwright screenshots / Backstop | Catch visual drift | `frontend-guidelines.md` |
| Approval/golden tests | Preserve legacy outputs | `testing-strategy.md` |
| Links17/csg-git-skill | Standardize SemVer, branches, commits, tags, test-release and release flow | `git-workflow.md` |

## Final Review Questions

- Which rules are evidence-backed and which are `Unknown`?
- Which implementation patterns must future AI reuse?
- Which patterns must future AI avoid?
- Which checks will fail if an agent invents a second architecture?
- Which frontend screenshots or stories prove visual consistency?
- Which optional workflow skills would reduce repeated prompting?
