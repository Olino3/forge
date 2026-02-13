# ⚒️ The Forge — Agentic Workflows Roadmap

> *"The tireless automatons of Hephaestus's workshop never sleep — they sweep the forge floor, sharpen every blade, and polish each shield while the gods rest."*

This document details the phased plan for implementing **Continuous Quality Workflows** for The Forge using [GitHub Agentic Workflows (gh-aw)](https://github.github.com/gh-aw/). Each workflow runs as a GitHub Action powered by an AI agent (Copilot engine), continuously improving Forge's codebase quality.

---

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Foundation: Completed Agentic Workflows](#foundation-completed-agentic-workflows)
  - [Bootstrap & Infrastructure](#bootstrap--infrastructure)
  - [Continuous Simplicity (Phase 1A)](#continuous-simplicity-phase-1a)
  - [Continuous Context (Phase 1B)](#continuous-context-phase-1b)
  - [Continuous Refactoring (Phase 2A)](#continuous-refactoring-phase-2a)
  - [Continuous Style (Phase 2B)](#continuous-style-phase-2b)
  - [Continuous Improvement (Phase 3)](#continuous-improvement-phase-3)
  - [Continuous Documentation (Phase 4)](#continuous-documentation-phase-4)
  - [Workflow Schedule Overview](#workflow-schedule-overview)
- [Future Phases](#future-phases)
- [Dependency Graph](#dependency-graph)
- [Risk Register](#risk-register)
- [Success Metrics](#success-metrics)
- [References](#references)

---

## Architecture Overview

### How gh-aw Workflows Work

Each workflow is a **Markdown file** with YAML frontmatter that gets compiled into a GitHub Actions `.lock.yml` file:

```
.github/
├── workflows/
│   ├── forge-simplicity.md          # Source: natural language + config
│   ├── forge-simplicity.lock.yml    # Compiled: GitHub Actions YAML
│   ├── forge-context-gen.md
│   ├── forge-context-gen.lock.yml
│   └── ...
└── aw/
    └── actions-lock.json            # Action pin manifest
```

### Forge-Specific Workflow Targets

Unlike gh-aw's Go-centric workflows, Forge's codebase is **Markdown, JSON, and Bash**. Our workflows target:

| Asset Type | Count | Quality Dimensions |
|-----------|-------|--------------------|
| **Skills** (`SKILL.md`) | 102 | Template adherence, required sections, examples presence |
| **Agent Configs** (`.config.json`) | 19 | Schema compliance, valid skill/MCP references |
| **Context Files** (`.md`) | 81 | Frontmatter validity, token estimates, staleness |
| **Hooks** (`.sh`) | 20 | Idempotency, 5s budget, `set -euo pipefail`, error handling |
| **Commands** (`.md`) | 12 | Frontmatter structure, workflow steps, skill references |

### Engine & Permissions Model

All workflows use the **Copilot engine** (GitHub-native, no external API keys). Permissions follow the principle of least privilege:

- **Read-only** workflows create issues/discussions with findings
- **Write** workflows create PRs with proposed changes (require human review)

---

## Foundation: Completed Agentic Workflows

> **Status**: ✅ **COMPLETE** — All foundational workflows operational as of February 13, 2026  
> **Total Workflows**: 13 workflows across 7 categories  
> **Compilation Status**: 0 errors, 4 warnings (schedule scattering only)

The Forge now has a comprehensive suite of autonomous quality improvement workflows running continuously via GitHub Actions powered by Copilot agents. This foundation provides automated code simplification, context generation, structure validation, style enforcement, health monitoring, and documentation synchronization.

---

### Bootstrap & Infrastructure

**Goal**: Establish gh-aw infrastructure and shared configuration patterns.

#### Setup Components

| Component | Purpose | Status |
|-----------|---------|--------|
| **gh-aw CLI** | Command-line tool for workflow management | ✅ Installed |
| **Repository Init** | Initialize agentic workflow structure | ✅ Complete |
| **Shared Imports** | Reusable workflow configuration fragments | ✅ 4 files |
| **Copilot Engine** | GitHub-native AI execution engine | ✅ Configured |

#### Shared Configuration Files

Located in `.github/workflows/shared/`:

1. **forge-base.md** — Common engine and permissions
   - Engine: `copilot`
   - Base permissions: `contents: read`
   - Strict mode enforcement

2. **forge-pr-creator.md** — PR-creating workflow defaults
   - Safe-outputs for pull requests
   - Standard labels and expiration
   - Draft PR defaults

3. **forge-issue-creator.md** — Issue-creating workflow defaults
   - Safe-outputs for issues
   - Max limits and auto-close
   - Expiration policies

4. **forge-conventions.md** — Forge project structure context
   - Skill organization patterns
   - Agent configuration standards
   - Context file conventions
   - Hook system architecture

---

### Continuous Simplicity (Phase 1A)

**Goal**: Reduce code complexity and eliminate duplication.  
**Completed**: February 2026

| Workflow | File | Type | Trigger | Purpose |
|----------|------|------|---------|---------|
| **Skill Simplifier** | `forge-skill-simplifier.md` | PR | PRs to `develop`/`main` | Simplify verbose skill documentation |
| **Duplication Detector** | `forge-duplication-detector.md` | PR | PRs to `develop`/`main` | Detect duplicate content across skills/agents/commands |

#### Key Features

**Skill Simplifier**:
- Analyzes changed `SKILL.md` files for verbosity
- Reduces redundant sections
- Improves clarity while preserving technical accuracy
- Creates PRs with before/after comparisons
- Max 3 PRs per run, 7-day expiration

**Duplication Detector**:
- Scans for duplicate code patterns across components
- Identifies copy-paste between skills, agents, and commands
- Suggests consolidation into shared utilities
- Creates issues with specific refactoring recommendations

---

### Continuous Context (Phase 1B)

**Goal**: Maintain context file integrity and coverage.  
**Completed**: February 2026

| Workflow | File | Type | Trigger | Purpose |
|----------|------|------|---------|---------|
| **Context Generator** | `forge-context-generator.md` | PR | PRs to `main` (post-merge) | Auto-generate context files for new skills |
| **Context Pruner** | `forge-context-pruner.md` | Issue | PRs to `develop`/`main` | Validate context integrity and detect drift |

#### Key Features

**Context Generator**:
- Detects new skills added in merged PRs
- Generates context files with proper YAML frontmatter
- Follows `context_metadata.schema.json` validation
- Creates PRs with generated context for review
- Ensures new skills have corresponding context coverage

**Context Pruner**:
- Validates YAML frontmatter in all context files
- Detects stale content (>90 days old)
- Identifies broken skill/agent references
- Checks domain index integrity
- Creates consolidated health reports as issues

---

### Continuous Refactoring (Phase 2A)

**Goal**: Validate structural compliance and configuration integrity.  
**Completed**: February 2026

| Workflow | File | Type | Trigger | Purpose |
|----------|------|------|---------|---------|
| **Skill Validator** | `forge-skill-validator.md` | Issue | Tue/Thu 09:00 UTC | Validate skill template compliance |
| **Agent Validator** | `forge-agent-validator.md` | Issue | Wed 09:00 UTC, PRs to agents | Validate agent configs against schema |

#### Key Features

**Skill Validator**:
- Checks all skills against `SKILL_TEMPLATE.md` structure
- Validates 6-step mandatory workflow adherence
- Detects missing `examples.md` files
- Ensures output conventions compliance
- Bi-weekly automated runs + PR-triggered validation

**Agent Validator**:
- Validates JSON configs against `agent_config.schema.json`
- Checks skill references exist
- Verifies MCP server references
- Confirms memory directory structure
- Creates issues with specific fix instructions

---

### Continuous Style (Phase 2B)

**Goal**: Enforce consistent conventions across all asset types.  
**Completed**: February 2026

| Workflow | File | Type | Trigger | Purpose |
|----------|------|------|---------|---------|
| **Convention Enforcer** | `forge-convention-enforcer.md` | PR | PRs to `develop`/`main` | Enforce Forge coding conventions |
| **Hook Quality Checker** | `forge-hook-checker.md` | Issue | Fri 07:00 UTC, PRs to hooks | Validate hook script quality |

#### Key Features

**Convention Enforcer**:
- Enforces kebab-case naming for skills/agents
- Validates YAML frontmatter completeness
- Checks for interface references (no hardcoded paths)
- Ensures consistent JSON indentation
- Creates PRs with automated style fixes

**Hook Quality Checker**:
- Validates `set -euo pipefail` presence
- Checks 5-second performance budget
- Ensures idempotency and graceful failure
- Verifies hooks.json registration
- Confirms HOOKS_GUIDE.md documentation
- Optional shellcheck integration

---

### Continuous Improvement (Phase 3)

**Goal**: Holistic health monitoring and best practices alignment.  
**Completed**: February 13, 2026

| Workflow | File | Type | Trigger | Purpose |
|----------|------|------|---------|---------|
| **Health Dashboard** | `forge-health-dashboard.md` | Issue | Sun 09:00 UTC | Weekly comprehensive health report |
| **Cross-Reference Checker** | `forge-xref-checker.md` | Issue | Tue 08:00 UTC | Detect broken references between components |
| **Best Practices Improver** | `forge-best-practices-improver.md` | PR | PRs to `develop` | Align with Anthropic Claude Code conventions |

#### Key Features

**Health Dashboard**:
- 6 comprehensive health dimensions:
  - Skills Health (template compliance, examples, versions)
  - Context Health (staleness, orphaned entries, coverage)
  - Agent Health (config validation, broken references)
  - Hook Health (shellcheck, registration, documentation)
  - Cross-Reference Integrity (8 validation matrices)
  - Growth Trends (week-over-week changes)
- Creates single consolidated weekly issue
- Color-coded status indicators (🟢/🟡/🔴)
- Auto-closes previous week's report

**Cross-Reference Checker**:
- Validates 8 cross-reference matrices:
  1. Skills ↔ Context Files
  2. Skills ↔ Agent Configs
  3. Skills ↔ Commands
  4. Agents ↔ MCP Configs
  5. Context ↔ Domain Indexes
  6. Hooks ↔ hooks.json
  7. Hooks ↔ HOOKS_GUIDE.md
  8. Commands ↔ Context Domains
- Organized by severity (Critical/Warning/Info)
- Provides actionable fix suggestions
- Bi-weekly automated validation

**Best Practices Improver**:
- Triggered on feature branch PRs to `develop`
- Analyzes only changed files (skills/agents/commands/context)
- Compares against Anthropic Claude Code best practices
- Checks for outdated patterns, missing sections, interface violations
- Creates improvement PRs targeting the feature branch (not develop)
- Includes before/after comparisons with rationale
- Ensures quality uplift before features land on develop

---

### Continuous Documentation (Phase 4)

**Goal**: Keep documentation synchronized with codebase reality.  
**Completed**: February 2026

| Workflow | File | Type | Trigger | Purpose |
|----------|------|------|---------|---------|
| **Doc Sync** | `forge-doc-sync.md` | PR | Mon-Fri 07:00 UTC | Sync top-level docs with codebase |
| **Doc Unbloat** | `forge-doc-unbloat.md` | PR | Thu 10:00 UTC | Simplify verbose documentation |

#### Key Features

**Doc Sync**:
- Validates component counts in ROADMAP.md
- Checks file structure examples in CONTRIBUTING.md
- Verifies skill/command references in COOKBOOK.md
- Ensures README.md claims match implementation
- Updates domain index.md file listings
- Creates PRs with synchronized updates
- Weekday automation (Mon-Fri)

**Doc Unbloat**:
- Reviews documentation for verbosity
- Removes redundant explanations
- Improves scannability with better formatting
- Preserves technical accuracy
- Creates PRs with simplified versions
- Weekly Thursday runs

---

### Workflow Schedule Overview

Strategic distribution across the week to minimize overlap and PR noise:

| Day / Event | Time (UTC) | Workflow | Type | Status |
|-------------|-----------|----------|------|--------|
| **Sunday** | 09:00 | Health Dashboard | Issue | Active |
| **Monday-Friday** | 07:00 | Doc Sync | PR | Active |
| **Tuesday** | 08:00 | Cross-Reference Checker | Issue | Active |
| **Tuesday** | 09:00 | Skill Validator | Issue | Active |
| **Wednesday** | 09:00 | Agent Validator | Issue | Active |
| **Thursday** | 09:00 | Skill Validator | Issue | Active |
| **Thursday** | 10:00 | Doc Unbloat | PR | Active |
| **Friday** | 07:00 | Hook Quality Checker | Issue | Active |
| **Weekly (Sat)** | Scattered | Stale Issue/PR Gardener | Issue | Planned rollout |
| **Daily** | Scattered | Dependency Update Sentinel | PR | Planned rollout |
| **Daily** | Scattered | Project Milestone Tracker | Issue | Planned rollout |
| **Weekly (Mon)** | Scattered | Project Manager Agent | Issue | Planned rollout |
| **PR Events** | - | Skill Simplifier | PR | Active |
| **PR Events** | - | Duplication Detector | PR | Active |
| **PR Events** | - | Context Pruner | Issue | Active |
| **PR Events** | - | Convention Enforcer | PR | Active |
| **PR Events** | - | Best Practices Improver (to develop) | PR | Active |
| **PR Merge** | - | Context Generator (main only) | PR | Active |
| **Issue Events** | - | Issue Triage Agent | Issue | Planned rollout |
| **Tag/Release Events** | - | Release Notes Generator | Issue | Planned rollout |
| **ROADMAP Change Events** | - | Project Manager Agent | Issue | Planned rollout |

**Total**: 11 scheduled + 10 event-triggered workflows

All workflows support `workflow_dispatch` for manual triggering.

---

## Future Phases

The foundational workflows (Phases 0-4) are complete. The next execution phases align directly to `ROADMAP.md` workflow targets.

### Phase 5 — Issue Intake Foundation & Template Migration

> **Status**: 🚧 Ready for implementation rollout
> **Goal**: Standardize issue intake and align workflow-generated issues to a canonical quality template.

#### Deliverables

1. Add issue templates under `.github/ISSUE_TEMPLATE/`:
   - `bug_report.yml`
   - `feature_request.yml`
   - `documentation_improvement.yml`
   - `security_vulnerability.yml`
   - `quality_issue.yml`
2. Add `.github/ISSUE_TEMPLATE/config.yml`:
   - disable blank issues
   - security contact link
3. Add `SECURITY.md` reporting policy.
4. Add shared workflow import:
   - `.github/workflows/shared/forge-quality-issue-template.md`
5. Migrate all existing issue-producing workflows to the quality issue contract:
   - `forge-agent-validator.md`
   - `forge-context-pruner.md`
   - `forge-duplication-detector.md`
   - `forge-health-dashboard.md`
   - `forge-hook-checker.md`
   - `forge-skill-validator.md`
   - `forge-xref-checker.md`

---

### Phase 6 — Operations & Release Workflows

> **Status**: 🚧 Ready for implementation rollout
> **Goal**: Automate release intelligence, dependency hygiene, and operational metrics.

#### Workflows

| Workflow | File | Trigger | Output |
|----------|------|---------|--------|
| **Release Notes Generator** | `.github/workflows/forge-release-notes-generator.md` | On tag/release + manual | Draft release notes issue categorized by feature/fix/breaking |
| **Dependency Update Sentinel** | `.github/workflows/forge-dependency-update-sentinel.md` | Daily + manual | Draft dependency upgrade PR with compatibility analysis |
| **Health Dashboard (expanded)** | `.github/workflows/forge-health-dashboard.md` | Weekly + manual | Weekly issue including test coverage, issue velocity, PR cycle time, code quality trend |

#### Notes

- Health Dashboard expansion preserves existing Forge-structure metrics and adds delivery/operations metrics.
- Dependency updates remain conservative: no broad, unscoped version churn.

---

### Phase 7 — Planning & Coordination Workflows

> **Status**: 🚧 Ready for implementation rollout
> **Goal**: Automate backlog triage, milestone tracking, roadmap execution planning, and stale work gardening.

#### Workflows

| Workflow | File | Trigger | Output |
|----------|------|---------|--------|
| **Issue Triage Agent** | `.github/workflows/forge-issue-triage-agent.md` | Issue opened/reopened + manual | Triage recommendation issue with labels/priority/assignment guidance |
| **Project Milestone Tracker** | `.github/workflows/forge-project-milestone-tracker.md` | Daily + manual | Milestone progress and blocker report issue |
| **Project Manager Agent** | `.github/workflows/forge-project-manager-agent.md` | Weekly + on ROADMAP changes + manual | Roadmap execution plan issue with decomposed work packages |
| **Stale Issue/PR Gardener** | `.github/workflows/forge-stale-gardener.md` | Weekly + manual | Stale inventory issue with ping/close recommendations |

---

### Phase 8 — Rollout, Validation, and Tuning

> **Status**: 📋 Planned
> **Goal**: Verify workflow behavior, tune noise levels, and harden operational guardrails.

#### Rollout Sequence

1. Compile all workflow specs (`gh aw compile`) and resolve errors.
2. Run each new workflow via `workflow_dispatch` once before relying on schedules.
3. Review issue/PR output quality against template contracts.
4. Tune labels, severity thresholds, and output verbosity to reduce false positives.
5. Promote stable workflows to ongoing scheduled operations.

#### Guardrails

✅ Shared imports for consistency  
✅ Read-only permissions with safe-outputs for writes  
✅ Staggered schedules to avoid overlap/noise  
✅ Human review for all generated PRs  
✅ Conservative stale/closure policies with grace periods

---

## Dependency Graph

**Status**: Foundation complete (Phases 0-4), expansion phases (5-8) in rollout

```
Phase 0 (Bootstrap) ✅
  │
  ├──→ Phase 1A (Simplicity) ✅    ←── parallel ──→  Phase 1B (Context) ✅
  │         │                                              │
  │         └──→ Phase 3 (Improvement) ✅ ←─ depends ─────┘
  │                    │
  ├──→ Phase 2A (Refactoring) ✅   ←── parallel ──→  Phase 2B (Style) ✅
  │
  └──→ Phase 4 (Documentation) ✅  ←── parallel ──→  Phase 3 ✅

Phase 5 (Issue Intake Foundation) 🚧
  │
  ├──→ Phase 6 (Operations & Release) 🚧
  ├──→ Phase 7 (Planning & Coordination) 🚧
  └──→ Phase 8 (Rollout & Tuning) 📋
```

### Implementation History

Foundation phases were completed in February 2026; expansion phases are now staged:

| Phase | Duration | Completion Date | Workflows |
|-------|----------|----------------|-----------|
| **0** | Bootstrap | Feb 2026 | Shared imports (4 files) |
| **1A** | Simplicity | Feb 2026 | Skill Simplifier, Duplication Detector |
| **1B** | Context | Feb 2026 | Context Generator, Context Pruner |
| **2A** | Refactoring | Feb 2026 | Skill Validator, Agent Validator |
| **2B** | Style | Feb 2026 | Convention Enforcer, Hook Quality Checker |
| **3** | Improvement | Feb 13, 2026 | Health Dashboard, Cross-Reference Checker, Best Practices Improver |
| **4** | Documentation | Feb 2026 | Doc Sync, Doc Unbloat |
| **5** | Issue Intake Foundation | Planned rollout | Issue templates + quality issue migration |
| **6** | Operations & Release | Planned rollout | Release Notes Generator, Dependency Sentinel, Health Dashboard expansion |
| **7** | Planning & Coordination | Planned rollout | Issue Triage, Milestone Tracker, Project Manager Agent, Stale Gardener |
| **8** | Rollout & Tuning | Planned | Canary, validation, threshold tuning |

**Foundation Delivery Time**: ~4 weeks  
**Workflow Inventory**: 19 workflow specs (13 active foundation + 6 expansion) + 5 shared imports

---

## Risk Register

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| gh-aw CLI breaking changes | High | Low | Pin to `v0.43.10`, watch CHANGELOG |
| Copilot engine rate limits | Medium | Medium | Max 3 PRs/issues per workflow run, stagger schedules, PR-triggered workflows use `max: 1-3` limits |
| AI-generated context files are low quality | Medium | Medium | All PRs require human review, include quality checklist |
| Workflow creates too many noisy PRs/issues | Medium | High | Use `close-older: true`, `expire: "+7d"`, `max: 3` |
| False positives in validation workflows | Low | High | Start with issue creation (not auto-fix PRs), tune over time |
| Token cost overhead | Medium | Low | Schedule workflows on weekdays, limit scope per run |

---

## Success Metrics

### Foundation Completion Criteria

✅ **All criteria met as of February 13, 2026**

| Phase | Completion Criteria | Status |
|-------|-------------------|--------|
| **0** | `gh aw compile` succeeds, shared imports compile, `gh aw status` shows ready | ✅ Complete |
| **1A** | Both simplicity workflows run successfully, first PR/issue created | ✅ Complete |
| **1B** | Context generator fires on test skill PR, pruner produces first health report | ✅ Complete |
| **2A** | Skill validator catches known non-compliant skill, agent validator catches test error | ✅ Complete |
| **2B** | Convention enforcer proposes at least one valid style fix | ✅ Complete |
| **3** | Health dashboard produces accurate report, xref checker finds known broken link, best practices improver creates valid improvement PR on feature branch | ✅ Complete |
| **4** | Doc sync catches intentionally stale count, unbloat proposes readable simplification | ✅ Complete |

### Expansion Phase Completion Criteria (Phases 5-8)

| Phase | Completion Criteria | Status |
|-------|-------------------|--------|
| **5** | Issue templates created, `SECURITY.md` present, all issue-producing workflows import quality issue contract | 🚧 In rollout |
| **6** | Release notes workflow drafts release issue on tag, dependency sentinel proposes valid draft PR, health dashboard includes delivery metrics | 🚧 In rollout |
| **7** | Triage/milestone/manager/stale workflows generate actionable planning reports with low noise | 🚧 In rollout |
| **8** | Canary manual runs pass, schedules enabled, false-positive rate remains under threshold for 2 weeks | 📋 Planned |

### Ongoing KPIs (Active Monitoring)

These metrics guide continuous workflow tuning:

| Metric | Target | Measurement | Tracking Method |
|--------|--------|-------------|-----------------|
| **Merge Rate** | > 70% | Merged PRs / Created PRs per workflow | GitHub PR analytics |
| **False Positive Rate** | < 20% | Closed-without-merge PRs + wontfix issues | Issue/PR close reasons |
| **Context Coverage** | > 80% | Skills with matching context files / total skills | Health Dashboard weekly |
| **Template Compliance** | > 90% | Skills passing structure validation / total skills | Skill Validator reports |
| **Agent Config Validity** | 100% | Agents passing schema validation / total agents | Agent Validator reports |
| **Hook Budget Compliance** | 100% | Hooks completing < 5s / total hooks | Hook Quality Checker |
| **Cross-Reference Integrity** | > 95% | Valid references / total references | Cross-Reference Checker |
| **Documentation Freshness** | > 90% | Up-to-date docs / total docs | Doc Sync reports |
| **Issue Triage Latency** | < 24h | Median time from issue creation to triage recommendation | Issue Triage Agent reports |
| **Milestone Predictability** | > 80% | Milestones delivered within planned window | Milestone Tracker reports |
| **Stale Backlog Ratio** | < 15% | Stale issues+PRs / total active issues+PRs | Stale Gardener reports |

---

## References

### gh-aw Documentation
- [Quick Start Guide](https://github.github.com/gh-aw/setup/quick-start/)
- [Creating Workflows](https://github.github.com/gh-aw/setup/creating-workflows/)
- [Frontmatter Reference](https://github.github.com/gh-aw/reference/frontmatter/)
- [Safe Outputs Reference](https://github.github.com/gh-aw/reference/safe-outputs/)
- [Workflow Structure](https://github.github.com/gh-aw/reference/workflow-structure/)
- [Design Patterns](https://github.github.com/gh-aw/blog/design-patterns/)
- [DailyOps Pattern](https://github.github.com/gh-aw/patterns/dailyops/)
- [Authoring Workflows](https://github.github.com/gh-aw/blog/authoring-workflows/)

### Peli's Factory Blog Series
- [Welcome to Peli's Agent Factory](https://github.github.com/gh-aw/blog/welcome-to-pelis-agent-factory/)
- [Continuous Simplicity](https://github.github.com/gh-aw/blog/continuous-simplicity/) — Code Simplifier, Duplicate Code Detector
- [Continuous Refactoring](https://github.github.com/gh-aw/blog/continuous-refactoring/) — Semantic Function Refactor, Daily File Diet
- [Continuous Style](https://github.github.com/gh-aw/blog/continuous-style/) — Terminal Stylist
- [Continuous Improvement](https://github.github.com/gh-aw/blog/continuous-improvement/) — Repository Quality Improver
- [Continuous Documentation](https://github.github.com/gh-aw/blog/continuous-documentation/) — Daily Doc Updater, Doc Unbloat
- [Operations & Release Workflows](https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-operations-release/) — Release Notes, Dependency Sentinel
- [Metrics & Analytics Workflows](https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-metrics-analytics/) — Health reporting and trend metrics
- [Issue Management Workflows](https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-issue-management/) — Triage and stale management
- [Project Coordination Workflows](https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-campaigns/) — Milestone and roadmap coordination

### Reference Workflows (source code)
- [code-simplifier.md](https://github.com/github/gh-aw/blob/v0.42.13/.github/workflows/code-simplifier.md?plain=1)
- [duplicate-code-detector.md](https://github.com/github/gh-aw/blob/v0.42.13/.github/workflows/duplicate-code-detector.md?plain=1)
- [semantic-function-refactor.md](https://github.com/github/gh-aw/blob/v0.42.13/.github/workflows/semantic-function-refactor.md?plain=1)
- [daily-file-diet.md](https://github.com/github/gh-aw/blob/v0.42.13/.github/workflows/daily-file-diet.md?plain=1)
- [terminal-stylist.md](https://github.com/github/gh-aw/blob/v0.42.13/.github/workflows/terminal-stylist.md?plain=1)
- [daily-doc-updater.md](https://github.com/github/gh-aw/blob/v0.42.13/.github/workflows/daily-doc-updater.md?plain=1)
- [unbloat-docs.md](https://github.com/github/gh-aw/blob/v0.42.13/.github/workflows/unbloat-docs.md?plain=1)

### Forge Internal References
- `forge-plugin/skills/SKILL_TEMPLATE.md` — Canonical skill structure
- `forge-plugin/interfaces/schemas/agent_config.schema.json` — Agent config schema
- `forge-plugin/context/loading_protocol.md` — 5-step context loading protocol
- `forge-plugin/context/cross_domain.md` — Cross-domain trigger matrix
- `forge-plugin/hooks/HOOKS_GUIDE.md` — Hook architecture and guidelines
- `forge-plugin/hooks/hooks.json` — Hook registration manifest
- `forge-plugin/skills/OUTPUT_CONVENTIONS.md` — Output formatting standards

---

*Last Updated: February 13, 2026*
*Maintained by: The Forge Keepers*

*Forged by Hephaestus. Automated by his tireless automatons. Worthy of Olympus.*
