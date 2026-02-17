# ⚒️ The Forge — Agentic Workflows Roadmap

> *"The tireless automatons of Hephaestus's workshop never sleep — they sweep the forge floor, sharpen every blade, and polish each shield while the gods rest."*

This document tracks **planned future work** for The Forge's agentic workflows. For a description of the 20 operational workflows and how they integrate into the development lifecycle, see **[AGENTIC_FORGE.md](AGENTIC_FORGE.md)**.

---

## Current State

**11 agentic workflows** are implemented and compiling cleanly (0 errors) across 4 categories:

| Category | Workflows | Count |
|----------|-----------|-------|
| Improvement | Component Improver, Test Coverage Improver | 2 |
| Documentation | Doc Maintainer, Context Generator, Health Dashboard | 3 |
| Operations | CI Failure Diagnostician, Dependency Sentinel, Release Notes Generator | 3 |
| Planning | Feature Decomposer, Milestone Lifecycle, Project Manager Agent, Stale Gardener | 4 |

**Supporting infrastructure**: 9 shared imports (5 base + 4 model templates), 5 issue templates, `SECURITY.md`, quality issue contract.

**Validation workflows**: 7 former validation workflows migrated to deterministic CI (`forge-tests.yml`) — fast, LLM-free pytest/bash jobs.

---

## AI Model Strategy

The Forge uses **model tiering** to optimize cost vs. quality for each workflow type. Model selection is configured via `engine.model` in workflow frontmatter, with specialized prompt templates in `.github/workflows/shared/model-*.md`.

### Model Tiers

| Model | Nickname | Strengths | Cost/1M Tokens | Use Case |
|-------|----------|-----------|----------------|----------|
| **gpt-5.1-codex-mini** | "The Scalpel" | High-speed tool use, grep mastery, massive refactors | ~$1.50 | Mechanical operations, pattern matching |
| **gpt-4.1** | "The Surgeon" | Precise editing, diff generation, low hallucination | ~$2.00 | Precision editing, conservative curation |
| **gemini-3-pro-preview** | "The Context King" | 1M+ token window, deep cross-file analysis | ~$1.25 | Large-context aggregation, milestone tracking |
| **claude-opus-4.6** | "The Strat" | Logic sanity, strategic reasoning, safety checks | ~$15.00 | Strategic analysis only (weekly runs) |

### Model-Prompt Matrix

| Workflow | Model | Rationale |
|----------|-------|-----------|
| **Forge Component Improver** | gpt-5.1-codex-mini | Mechanical file operations, tool-heavy, rule-based checking |
| **Forge Doc Maintainer** | gpt-4.1 | Precision editing, character-perfect diffs, factual accuracy |
| **Forge Milestone Lifecycle** | gemini-3-pro-preview | 1M+ context to ingest all milestones, issues, PRs |
| **Forge Health Dashboard** | gemini-3-pro-preview | Aggregate ~200+ files, cross-ref tallies, trend analysis |
| **Forge Release Notes Generator** | gpt-4.1 | Structured classification, low hallucination critical |
| **Forge Context Generator** | gpt-5.1-codex-mini | Template expansion from skill content, mechanical generation |
| **Forge Dependency Sentinel** | gpt-5.1-codex-mini | Pattern matching on version strings, grep-based scanning |
| **Forge Test Coverage Improver** | gpt-5.1-codex-mini | Test generation from patterns, codex-mini sweet spot |
| **Forge Stale Gardener** | gpt-4.1 | Conservative judgment, decision tree logic, grace periods |
| **Forge Project Manager Agent** | claude-opus-4.6 | Strategic PM analysis, ROADMAP synthesis, weekly only |

### Prompt Templates

Each model tier has a specialized system prompt template in `.github/workflows/shared/`:

- **model-codex-mini.md**: Tool-Use-First approach, structured JSON output, anti-patterns list
- **model-gpt4.md**: Precision Editor framework, before/after examples, self-verification checklist
- **model-gemini.md**: XML data delimiting, chain-of-thought protocol, multi-document QA
- **model-claude-opus.md**: Strategic Advisor framework, Socratic prompting, execution plans

Workflows import the appropriate template via `imports: [shared/model-*.md]` in frontmatter.

---

## Planned Work

### Phase 8 — Rollout, Validation, and Tuning

> **Status**: 📋 Planned
> **Goal**: Verify workflow behavior in production, tune noise levels, and harden operational guardrails.

#### Rollout Sequence

1. Run each workflow via `workflow_dispatch` once before relying on schedules.
2. Review issue/PR output quality against template contracts.
3. Tune labels, severity thresholds, and output verbosity to reduce false positives.
4. Promote stable workflows to ongoing scheduled operations.
5. Monitor for 2 weeks to validate false-positive rate stays below 20%.

#### Guardrails

✅ Shared imports for consistency
✅ Read-only permissions with safe-outputs for writes
✅ Staggered schedules to avoid overlap/noise
✅ Human review for all generated PRs
✅ Conservative stale/closure policies with grace periods

#### Completion Criteria

| Criteria | Target |
|----------|--------|
| Manual dispatch runs pass | All 20 workflows |
| Schedules enabled in production | All scheduled workflows |
| False-positive rate | < 20% for 2 consecutive weeks |
| Merge rate for PR-creating workflows | > 70% |

---

### Future Workflow Candidates

These workflows are candidates for implementation after Phase 8 stabilization:

| Workflow | Description | Trigger | Reference |
|----------|-------------|---------|----------|
| **Improve Test Coverage** | Analyze coverage gaps, generate missing tests | Schedule (weekly) | [Peli's Testing & Validation](https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-testing-validation/) |
| **Diagnose CI Failures** | Auto-investigate CI failures, post root cause analysis | On CI failure | [Peli's Fault Investigation](https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-quality-hygiene/) |

**Note**: Feature Decomposer and Milestone Progress Reviewer have been implemented and are now part of the Planning & Coordination category.

---

## Ongoing KPIs

These metrics guide continuous workflow tuning:

| Metric | Target | Tracking Method |
|--------|--------|-----------------|
| **Merge Rate** | > 70% | GitHub PR analytics |
| **False Positive Rate** | < 20% | Issue/PR close reasons |
| **Context Coverage** | > 80% | Health Dashboard weekly |
| **Template Compliance** | > 90% | Skill Validator reports |
| **Agent Config Validity** | 100% | Agent Validator reports |
| **Hook Budget Compliance** | 100% | Hook Quality Checker |
| **Cross-Reference Integrity** | > 95% | Cross-Reference Checker |
| **Documentation Freshness** | > 90% | Doc Sync reports |
| **Issue Triage Latency** | < 24h | Issue Triage Agent |
| **Milestone Predictability** | > 80% | Milestone Tracker |
| **Milestone Delivery Rate** | > 75% | Milestone Progress Reviewer |
| **Feature Decomposition Coverage** | > 90% | Feature Decomposer |
| **Stale Backlog Ratio** | < 15% | Stale Gardener |

---

## Risk Register

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| gh-aw CLI breaking changes | High | Low | Pin to `v0.43.10`, watch CHANGELOG |
| Copilot engine rate limits | Medium | Medium | Max 3 PRs/issues per workflow run, stagger schedules |
| Workflow creates too many noisy PRs/issues | Medium | High | Use `close-older-issues: true`, `expires: 7`, `max: 3` |
| False positives in validation workflows | Low | High | Start with issue creation, tune over time |
| Token cost overhead | Medium | Low | Schedule workflows strategically, limit scope per run |

---

## References

### gh-aw Documentation
- [Quick Start Guide](https://github.github.com/gh-aw/setup/quick-start/)
- [Creating Workflows](https://github.github.com/gh-aw/setup/creating-workflows/)
- [Frontmatter Reference](https://github.github.com/gh-aw/reference/frontmatter/)
- [Safe Outputs Reference](https://github.github.com/gh-aw/reference/safe-outputs/)
- [Design Patterns](https://github.github.com/gh-aw/blog/design-patterns/)

### Peli's Factory Blog Series
- [Welcome to Peli's Agent Factory](https://github.github.com/gh-aw/blog/welcome-to-pelis-agent-factory/)
- [Continuous Simplicity](https://github.github.com/gh-aw/blog/continuous-simplicity/)
- [Continuous Refactoring](https://github.github.com/gh-aw/blog/continuous-refactoring/)
- [Continuous Style](https://github.github.com/gh-aw/blog/continuous-style/)
- [Continuous Improvement](https://github.github.com/gh-aw/blog/continuous-improvement/)
- [Continuous Documentation](https://github.github.com/gh-aw/blog/continuous-documentation/)
- [Operations & Release](https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-operations-release/)
- [Issue Management](https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-issue-management/)
- [Project Coordination](https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-campaigns/)

### Forge Internal References
- `AGENTIC_FORGE.md` — Contributor-facing guide with lifecycle diagrams and scenarios
- `forge-plugin/skills/SKILL_TEMPLATE.md` — Canonical skill structure
- `forge-plugin/interfaces/schemas/agent_config.schema.json` — Agent config schema
- `forge-plugin/hooks/HOOKS_GUIDE.md` — Hook architecture and guidelines

---

*Last Updated: February 13, 2026*
*Maintained by: The Forge Keepers*

*Forged by Hephaestus. Automated by his tireless automatons. Worthy of Olympus.*
