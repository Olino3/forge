# ⚒️ The Forge — Agentic Workflows Roadmap

> *"The tireless automatons of Hephaestus's workshop never sleep — they sweep the forge floor, sharpen every blade, and polish each shield while the gods rest."*

This document tracks **planned future work** for The Forge's agentic workflows. For a description of the 19 operational workflows and how they integrate into the development lifecycle, see **[AGENTIC_FORGE.md](AGENTIC_FORGE.md)**.

---

## Current State

**20 agentic workflows** are implemented and compiling cleanly (0 errors) across 9 categories:

| Category | Workflows | Count |
|----------|-----------|-------|
| Continuous Simplicity | Skill Simplifier, Duplication Detector | 2 |
| Continuous Context | Context Generator, Context Pruner | 2 |
| Continuous Refactoring | Skill Validator, Agent Validator | 2 |
| Continuous Style | Convention Enforcer, Hook Quality Checker | 2 |
| Continuous Improvement | Health Dashboard, Cross-Reference Checker, Best Practices Improver | 3 |
| Continuous Documentation | Doc Sync, Doc Unbloat | 2 |
| Continuous Testing | CI Failure Diagnostician | 1 |
| Operations & Release | Release Notes Generator, Dependency Update Sentinel | 2 |
| Planning & Coordination | Issue Triage Agent, Project Milestone Tracker, Project Manager Agent, Stale Gardener | 4 |

**Supporting infrastructure**: 5 shared imports, 5 issue templates, `SECURITY.md`, quality issue contract.

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
| Manual dispatch runs pass | All 19 workflows |
| Schedules enabled in production | All scheduled workflows |
| False-positive rate | < 20% for 2 consecutive weeks |
| Merge rate for PR-creating workflows | > 70% |

---

### Future Workflow Candidates

These workflows are candidates for implementation after Phase 8 stabilization:

| Workflow | Description | Trigger | Reference |
|----------|-------------|---------|----------|
| **Improve Test Coverage** | Analyze coverage gaps, generate missing tests | Schedule (weekly) | [Peli's Testing & Validation](https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-testing-validation/) |
| **Milestone Planner** | Plan features and bugfixes for newly created milestones; create feature issues and associate existing issues | Milestone created | — |
| **Feature Decomposer** | Decompose milestone feature issues into Copilot-assignable sub-issues with acceptance criteria | Issue milestoned | — |
| **Milestone Progress Reviewer** | Evaluate milestone and feature delivery gaps on each PR; create remediation issues to maintain trajectory | PR events | — |

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
