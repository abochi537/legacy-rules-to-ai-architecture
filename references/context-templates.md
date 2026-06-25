# Context Templates

Use these templates to create durable AI project context. Keep `AGENTS.md`
short; put detailed rules in `docs/ai/*`.

## AGENTS.md

```md
# AGENTS.md

## Project Contract
Always read `docs/ai/00-index.md` before coding. Do not rely only on the
current chat history for project rules.

## Project Summary
- Name: <project-name>
- Purpose: <one-paragraph product purpose>
- Current phase: <legacy extraction | migration | rebuild | maintenance>
- Target architecture: <brief target>

## Hard Rules
- Do not upgrade frameworks, UI libraries, state managers, build tools, or API
  clients without explicit approval; see `docs/ai/tech-baseline.md`.
- Do not bypass architecture boundaries; see `docs/ai/architecture.md`.
- Business rule changes must update `docs/ai/domain-rules.md` with evidence.
- API changes must update `docs/ai/api-contracts.md` or the source schema.
- New pages must reuse existing layouts, components, tokens, and interaction
  patterns; see `docs/ai/frontend-guidelines.md`.
- Do not introduce a second implementation pattern for the same concern unless
  `docs/ai/decisions.md` records the reason.
- Before multi-turn modifications, read `docs/ai/active-context.md`.

## Required Checks
- Typecheck: <command or TBD>
- Unit tests: <command or TBD>
- Integration/E2E: <command or TBD>
- Architecture checks: <command or TBD>
- Visual regression: <command or TBD>
- Git/release checks: see `docs/ai/git-workflow.md`

## Navigation
- Index: `docs/ai/00-index.md`
- Project brief: `docs/ai/project-brief.md`
- Tech baseline: `docs/ai/tech-baseline.md`
- Architecture: `docs/ai/architecture.md`
- Domain rules: `docs/ai/domain-rules.md`
- API contracts: `docs/ai/api-contracts.md`
- Frontend consistency: `docs/ai/frontend-guidelines.md`
- Testing: `docs/ai/testing-strategy.md`
- Git workflow: `docs/ai/git-workflow.md`
- Migration map: `docs/ai/migration-map.md`
- Current context: `docs/ai/active-context.md`
- Context health: `docs/ai/context-health.md`
- Decisions: `docs/ai/decisions.md`
```

## docs/ai/00-index.md

```md
# AI Context Index

This directory is the durable project context for AI-assisted development.

## Rule Priority
When sources conflict, prefer evidence in this order:
1. Runtime behavior observed in production or characterization tests.
2. Existing automated tests and fixtures.
3. API schema, database schema, generated client types, migrations.
4. Implementation code on the active path.
5. Product documentation or release notes.
6. Comments, names, and inferred intent.

Conflicts must be recorded in `decisions.md` or `Unknowns`; do not silently
turn inconsistent legacy behavior into a hard rule.

## Read Order
- New feature: project-brief, architecture, domain-rules, active-context
- Frontend page: frontend-guidelines, architecture, domain-rules
- API/backend: api-contracts, architecture, testing-strategy
- Legacy migration: migration-map, domain-rules, testing-strategy

## Evidence Rule
Do not guess. If a rule cannot be traced to code, tests, schemas, logs, or
product docs, mark it as `Unknown` and list the missing evidence.
```

## docs/ai/project-brief.md

```md
# Project Brief

## Purpose
<What the system does and for whom.>

## Core Workflows
| Workflow | Entry point | Users | Notes |
| --- | --- | --- | --- |

## Non-Goals
- <Things the rebuild must not attempt yet.>

## Evidence
- <README, product docs, routes, tests, demos, or user notes.>
```

## docs/ai/tech-baseline.md

```md
# Tech Baseline

## Stack
| Area | Current choice | Version/source | Upgrade policy |
| --- | --- | --- | --- |
| Language | | | Do not upgrade without approval |
| Framework | | | Do not upgrade without approval |
| UI library | | | Do not replace without approval |
| State | | | Do not introduce alternatives |
| Styling | | | Follow existing tokens |
| API client | | | Reuse existing client |

## Commands
| Purpose | Command | Source |
| --- | --- | --- |

## Package Boundaries
- <workspace/package/module notes>
```

## docs/ai/architecture.md

```md
# Architecture

## Layers
| Layer | Responsibility | Allowed dependencies | Forbidden dependencies |
| --- | --- | --- | --- |

## Approved Patterns
| Concern | Standard pattern | Evidence | Avoid |
| --- | --- | --- | --- |

## Placement Guide
| New code type | Put it here | Reuse first | Do not |
| --- | --- | --- | --- |
| Feature/page | | | |
| API endpoint/client | | | |
| State/store | | | |
| Shared component | | | |
| Utility/helper | | | |

## Conflicts
| Area | Competing patterns | Canonical choice | Decision link |
| --- | --- | --- | --- |

## Module Map
| Module | Purpose | Owner/consumer | Notes |
| --- | --- | --- | --- |

## Enforcement Ideas
- dependency-cruiser / eslint import rules / ast-grep / semgrep:
```

## docs/ai/domain-rules.md

```md
# Domain Rules

## Rule Format
Every rule must include evidence and confidence.

### RULE-001 <title>
- Rule:
- Evidence:
- Scope:
- Confidence: High | Medium | Low
- Migration note:

## Unknowns
| Question | Needed evidence | Owner |
| --- | --- | --- |
```

## docs/ai/api-contracts.md

```md
# API Contracts

## API Surface
| Endpoint/function | Method | Request | Response | Evidence |
| --- | --- | --- | --- | --- |

## Error Handling
| Case | Expected behavior | Evidence |
| --- | --- | --- |

## Contract Tests
- OpenAPI/GraphQL schema:
- Schemathesis or equivalent:
- Mock server / fixtures:
```

## docs/ai/frontend-guidelines.md

```md
# Frontend Guidelines

## Design Baseline
| Area | Standard | Evidence |
| --- | --- | --- |
| Layout | | |
| Components | | |
| Forms | | |
| Tables/lists | | |
| Dialogs/drawers | | |
| Empty/loading/error states | | |
| Responsive behavior | | |

## Canonical References
| Reference | Location | What it proves | Last checked |
| --- | --- | --- | --- |
| Canonical page screenshot | | layout/density/spacing | |
| Component story | | variants/states | |
| Design tokens | | colors/spacing/type | |
| Mobile breakpoint | | responsive behavior | |

## Hard Rules
- Reuse existing layout and components before creating new ones.
- Do not create a second button, form, modal, table, or notification pattern.
- Add new design tokens only when the existing system cannot express the need.
- Check desktop and mobile viewports for every new page.

## Deprecated Patterns
| Pattern | Why deprecated | Replacement | Evidence |
| --- | --- | --- | --- |

## Page Pattern Inventory
| Page | Route | Layout | Key components | Reusable pattern |
| --- | --- | --- | --- | --- |

## Visual Checks
- Storybook:
- Playwright screenshots:
- Backstop/visual regression:
```

## docs/ai/testing-strategy.md

```md
# Testing Strategy

## Existing Tests
| Type | Command | Scope | Notes |
| --- | --- | --- | --- |

## Gate Tiers
| Tier | Required checks | When |
| --- | --- | --- |
| Minimum | typecheck, lint, focused characterization tests | Every behavior or architecture change |
| Recommended | API contract tests, dependency/layer checks | API/backend or shared module changes |
| Mature | visual regression, golden master, broader E2E | UI-critical or migration-critical changes |

## Characterization Tests
Use these to lock old-system behavior before rebuilding.

| Feature | Golden behavior | Test location | Evidence |
| --- | --- | --- | --- |

## Required For Changes
- Business rule change:
- API change:
- Frontend page change:
- Migration step:
```

## docs/ai/git-workflow.md

```md
# Git Workflow

## Source Of Truth
Use the installed `csg-git-skill` for detailed SemVer, Conventional Commits,
branch naming, tag, test-release, hotfix, and release flow decisions. If it is
not installed, install from:

Install command:

    npx skills add Links17/csg-git-skill -g -a cursor -a claude-code -a codex -y

## Project Overrides
| Topic | Project rule | Evidence |
| --- | --- | --- |
| Main branch | | |
| Dev/test branch | | |
| Version file | | |
| CI release trigger | | |
| Test-release owner | | |

## Release Checks
Fill this section from `csg-git-skill` and project-specific evidence.

| Check | Project rule | Evidence |
| --- | --- | --- |
| Version bump | | |
| Branch naming | | |
| Commit message | | |
| Test-release tag | | |
| Production release tag | | |
```

## docs/ai/migration-map.md

```md
# Migration Map

## Feature Mapping
| Legacy feature | Evidence | Target module | Status | Notes |
| --- | --- | --- | --- | --- |

## Compatibility
| Concern | Legacy behavior | New behavior | Risk |
| --- | --- | --- | --- |

## Cutover Plan
1.
2.
3.
```

## docs/ai/active-context.md

```md
# Active Context

## Current Goal
<What the current AI/developer session is trying to complete.>

## Recent Decisions
| Date | Decision | Reason | Link |
| --- | --- | --- | --- |

## Open Questions
| Question | Blocked work | Needed evidence |
| --- | --- | --- |

## Next Safe Step
<One concrete next step.>
```

## docs/ai/context-health.md

```md
# Context Health

## Last Verified
| Date | Command/check | Result | Notes |
| --- | --- | --- | --- |

## Known Drift
| Area | Symptom | Evidence | Owner |
| --- | --- | --- | --- |

## Stale Or Weak Rules
| Rule/doc | Issue | Needed evidence |
| --- | --- | --- |

## Maintenance Protocol
- Start of multi-turn work: read `AGENTS.md`, `00-index.md`, and `active-context.md`.
- End of multi-turn work: update `active-context.md` and any docs affected by changed rules.
- Before release/PR: run the required checks from `AGENTS.md` and record results here.
```

## docs/ai/decisions.md

```md
# Decisions

## ADR-001 <title>
- Date:
- Status: proposed | accepted | superseded
- Context:
- Decision:
- Consequences:
- Alternatives considered:
```
