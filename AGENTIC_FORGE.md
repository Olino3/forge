# ⚒️ The Forge — Agentic Workflows Guide

> *"The tireless automatons of Hephaestus's workshop never sleep — they sweep the forge floor, sharpen every blade, and polish each shield while the gods rest."*

This guide explains, in plain language, how The Forge's **11 agentic workflows** work alongside you as a contributor. No deep infrastructure knowledge required — just an understanding of PRs, issues, and releases.

---

## Table of Contents

- [The One-Sentence Summary](#the-one-sentence-summary)
- [How It All Fits Together](#how-it-all-fits-together)
- [What Happens When You Open a PR](#what-happens-when-you-open-a-pr)
- [What Happens When an Issue Is Created](#what-happens-when-an-issue-is-created)
- [What Happens in the Background](#what-happens-in-the-background)
- [What Happens at Release Time](#what-happens-at-release-time)
- [The Complete Workflow Catalog](#the-complete-workflow-catalog)
- [Where to Find Outputs](#where-to-find-outputs)
- [Common Developer Scenarios](#common-developer-scenarios)
- [FAQ for Contributors](#faq-for-contributors)
- [File Map — Where Things Live](#file-map--where-things-live)

---

## The One-Sentence Summary

**AI-powered workflows continuously watch PRs, issues, schedules, and releases — then create suggestions (as issues or draft PRs) that humans review and decide on.**

Nothing merges or closes without a person approving it.

---

## How It All Fits Together

The Forge's development lifecycle has four stages where automation is active. Here's how a typical contribution flows from idea to release, with the agentic layer shown at each step:

```
╔══════════════════════════════════════════════════════════════════════════╗
║                    THE FORGE DEVELOPMENT LIFECYCLE                      ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐             ║
║   │  1. INTAKE   │────▶│  2. BUILD    │────▶│  3. REVIEW   │            ║
║   │             │     │             │     │             │             ║
║   │ Open issue  │     │ Work on a   │     │ Open PR to  │             ║
║   │ using a     │     │ feature     │     │ develop or  │             ║
║   │ template    │     │ branch      │     │ main        │             ║
║   └──────┬──────┘     └─────────────┘     └──────┬──────┘             ║
║          │                                       │                    ║
║     ┌────▼────┐                            ┌─────▼──────┐             ║
║     │ 🤖 AUTO │                            │  🤖 AUTO   │             ║
║     │ Triage  │                            │  6 PR      │             ║
║     │ Agent   │                            │  workflows │             ║
║     └─────────┘                            └─────┬──────┘             ║
║                                                  │                    ║
║          ┌─────────────┐     ┌───────────────────▼──┐                 ║
║          │  4. RELEASE  │◀───│  MERGE (human decision)│                ║
║          │             │     └──────────────────────┘                 ║
║          │ Tag a       │                                              ║
║          │ version     │     ┌──────────┐                             ║
║          └──────┬──────┘     │ 🤖 AUTO  │                             ║
║                 │            │ Post-    │                             ║
║            ┌────▼────┐      │ merge    │                             ║
║            │ 🤖 AUTO │      │ context  │                             ║
║            │ Release │      │ gen      │                             ║
║            │ Notes   │      └──────────┘                             ║
║            └─────────┘                                                ║
║                                                                        ║
║   ┌────────────────────────────────────────────────────────────────┐   ║
║   │  🤖 BACKGROUND (always running on schedule)                    │   ║
║   │                                                                │   ║
║   │  Daily: dependency checks, milestone tracking                  │   ║
║   │  Weekly: health reports, stale cleanup, cross-ref validation   │   ║
║   │  Weekdays: doc sync, doc simplification                        │   ║
║   └────────────────────────────────────────────────────────────────┘   ║
║                                                                        ║
╚══════════════════════════════════════════════════════════════════════════╝
```

### The golden rule

> **Automation proposes. Humans decide.**
>
> Every workflow creates either an **issue** (a finding to consider) or a **draft PR** (a change to review). Nothing is auto-merged. Nothing is auto-closed without a grace period. You are always in control.

### No-op handling

Workflows intelligently avoid creating noise when there's nothing to report:

**PR-creating workflows** (Component Improver, Doc Maintainer, Test Coverage Improver, CI Failure Diagnostician, Dependency Sentinel, Context Generator):
- Use `if-no-changes: "ignore"` in their safe-outputs configuration
- **Only create a PR when changes are proposed** — if analysis finds no improvements needed, no PR is created
- You only see draft PRs when there's actual work to review

**Issue-creating workflows** (Stale Gardener, Project Manager Agent, Milestone Lifecycle):
- **Always create an issue with summary counts**, even if counts are zero
- Provides audit trail that the workflow ran successfully and found no problems
- Weekly/daily summary format allows tracking trends over time (e.g., "Stale issues: 0" shows the repo is healthy)

**Deterministic CI** (Quality Gate):
- Runs on every PR and weekly schedule
- Reports pass/fail status in GitHub Actions summary
- No issue/PR creation — just CI checkmarks

---

## What Happens When You Open a PR

This is where you'll interact with automation the most. When you open or update a pull request targeting `develop` or `main`, up to **6 workflows** activate depending on what files you changed.

### The PR workflow pipeline

```
  You push code
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│                    PR OPENED / UPDATED                    │
│                                                          │
│  GitHub detects the PR event and triggers workflows      │
│  based on changed file paths and target branches:        │
│                                                          │
│  ┌──────────────────┐  Changed skills/agents/commands/   │
│  │ Component        │  context? PR to develop/main?      │
│  │ Improver         │──▶ Creates a PR with best          │
│  │                  │    practices alignment and          │
│  │                  │    documentation improvements       │
│  └──────────────────┘                                    │
│                                                          │
│  ┌──────────────────┐  All PRs                           │
│  │ Quality Gate CI  │──▶ Runs deterministic tests:       │
│  │ (forge-tests.yml)│    - Schema validation              │
│  │                  │    - Context integrity              │
│  │                  │    - Duplication detection          │
│  │                  │    - Convention enforcement         │
│  │                  │    - Cross-reference validation     │
│  │                  │    - Hook syntax checks             │
│  └──────────────────┘                                    │
│                                                          │
└──────────────────────────────────────────────────────────┘
       │
       ▼
  Human reviewer sees your code + CI results + workflow
  suggestions and makes the merge decision
```

### What you'll actually see

When a workflow activates on your PR, you'll see:

1. **CI Results** — The Quality Gate CI runs on every PR, showing pass/fail status for:
   - Schema validation (agents, context, hooks)
   - Context integrity (YAML frontmatter, cross-references)
   - Duplication detection
   - Convention enforcement (naming, structure)
   - Cross-reference validation

2. **Draft PR (if improvements found)** — Component Improver may create a draft PR targeting `develop`/`main` with suggested improvements to your changes. Review at your pace; it auto-expires after 14 days.

### What to do about workflow outputs

| Output you see | What it means | What to do |
|---|---|---|
| CI failure | Validation checks failed | Review the CI logs, fix the issues in your PR |
| `[improve]` draft PR | Best practices improvements suggested | Review the diff, merge if helpful, close if not |
| Green CI checkmarks | All validation checks passed | Your PR meets quality standards |

### What happens after your PR merges

If your PR merges into `main` and it added new skills, one more workflow activates:

- **Context Generator** — automatically creates a PR adding context files for any new skills that don't have them yet. This ensures every skill has matching reference documentation.

---

## What Happens When an Issue Is Created

The Forge provides **5 issue templates** so that every issue starts with the right structure. When you create a new issue, GitHub presents a chooser:

```
┌─────────────────────────────────────────────────────────────┐
│                  Choose an issue template                    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 🐛  Bug report                                      │   │
│  │     Repro steps, expected vs actual, environment     │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ ✨  Feature request                                  │   │
│  │     Problem, proposed solution, acceptance criteria   │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 📚  Documentation improvement                       │   │
│  │     Location, what's wrong, proposed fix              │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 🔒  Security vulnerability                          │   │
│  │     Redirects to private SECURITY.md process          │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 🔧  Quality issue                                    │   │
│  │     Duplication, dead code, structural drift          │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Blank issues are disabled — use a template above.          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### After you submit the issue

The **Issue Triage Agent** activates and creates a companion `[triage]` issue with:

- **Detected type** — bug, feature, docs, security, or quality
- **Recommended labels** — type, priority (`p0`–`p3`), and area
- **Assignment suggestion** — which contributor or team is the best fit
- **Next action** — what should happen next (needs reproduction, ready for work, etc.)

This triage issue is a **recommendation**, not an auto-action. Maintainers review it and apply labels/assignments manually.

### Why templates matter

Workflow-generated issues (from Component Improver, Milestone Lifecycle, etc.) also follow the **Quality Issue** template structure. This means all issues — whether created by humans or automation — share a consistent format that makes triage, filtering, and milestone planning predictable.

---

## What Happens in the Background

Even when no one is actively contributing, scheduled workflows run to keep the repository healthy. Think of them as a nightly cleaning crew for the codebase.

### Daily workflows

```
┌──────────────────────────────────────────────────────────────────┐
│                        EVERY DAY                                 │
│                                                                  │
│  ┌──────────────────────────────┐                                │
│  │ Dependency Update Sentinel   │  Checks dependency surfaces    │
│  │ (scattered)                  │  for outdated or vulnerable    │
│  │                              │  references. Creates a draft   │
│  │ Output: Draft PR             │  PR with safe upgrades.        │
│  └──────────────────────────────┘                                │
│                                                                  │
│  ┌──────────────────────────────┐                                │
│  │ Milestone Lifecycle Manager  │  Scans open milestones for     │
│  │ (08:00 UTC)                  │  progress, blocked items, and  │
│  │                              │  velocity trends. Also handles │
│  │ Output: Issue                │  planning on milestone.created │
│  └──────────────────────────────┘                                │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Weekly workflows

```
┌──────────────────────────────────────────────────────────────────┐
│                        WEEKLY CADENCE                             │
│                                                                  │
│  SUNDAY                                                          │
│  ┌──────────────────────────────┐                                │
│  │ Forge Quality Gate (CI)      │  Deterministic tests: schema   │
│  │ (09:00 UTC)                  │  validation, context integrity │
│  │                              │  duplication detection, naming │
│  │ Output: CI Results           │  conventions, cross-references │
│  │ (GITHUB_STEP_SUMMARY)       │  — NO LLMs, pure pytest/bash. │
│  └──────────────────────────────┘                                │
│                                                                  │
│  MONDAY                                                          │
│  ┌──────────────────────────────┐                                │
│  │ Project Manager Agent        │  Compares ROADMAP targets      │
│  │ (scattered)                  │  against actual implementation │
│  │                              │  state. Proposes milestone     │
│  │ Output: Issue                │  breakdowns and priorities.    │
│  └──────────────────────────────┘                                │
│                                                                  │
│  TUESDAY                                                         │
│  ┌──────────────────────────────┐                                │
│  │ Test Coverage Improver       │  Identifies coverage gaps and  │
│  │ (09:00 UTC)                  │  generates missing pytest      │
│  │                              │  tests for the test harness.   │
│  │ Output: Draft PR             │                                │
│  └──────────────────────────────┘                                │
│                                                                  │
│  WEDNESDAY                                                       │
│  ┌──────────────────────────────┐                                │
│  │ Component Improver           │  Two-stage pipeline: analyzes  │
│  │ (scattered)                  │  components for best practices │
│  │                              │  alignment, then simplifies    │
│  │ Output: Draft PR             │  verbose documentation.        │
│  └──────────────────────────────┘                                │
│                                                                  │
│  THURSDAY                                                        │
│  ┌──────────────────────────────┐                                │
│  │ Doc Maintainer               │  Two-stage pipeline: syncs     │
│  │ (scattered)                  │  docs with codebase state,     │
│  │                              │  then reduces verbosity in     │
│  │ Output: Draft PR             │  top-level documentation.      │
│  └──────────────────────────────┘                                │
│                                                                  │
│  SATURDAY                                                        │
│  ┌──────────────────────────────┐                                │
│  │ Stale Issue/PR Gardener      │  Identifies stale issues       │
│  │ (scattered)                  │  (30d) and PRs (14d).          │
│  │                              │  Recommends ping or close      │
│  │ Output: Issue                │  with grace period.            │
│  └──────────────────────────────┘                                │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### How to read scheduled outputs

Every Monday, check the **Issues** tab filtered by `forge-automation` label. The weekend and previous-week runs will have produced:

- A **Quality Gate** CI summary with test results across all validation checks
- Possibly a **Stale Review** issue listing dormant work
- Any **Component Improver** or **Doc Maintainer** draft PRs with suggested changes

These are informational. Fix what matters, close what doesn't apply.

---

## What Happens at Release Time

When you push a version tag (`v*`) or publish a GitHub Release:

```
  git tag v0.3.0 && git push --tags
       │
       ▼
┌──────────────────────────────────────────────────────────────────┐
│                    RELEASE NOTES GENERATOR                        │
│                                                                  │
│  1. Finds the previous tag boundary                              │
│  2. Collects all merged PRs between the two tags                 │
│  3. Classifies each PR by type:                                  │
│     🚀 Features  (feat:, enhancement label)                      │
│     🐛 Fixes     (fix:, bug label)                               │
│     ⚠️  Breaking  (breaking, ! in title)                         │
│     🧰 Maintenance (chore, refactor, deps)                       │
│     📚 Documentation (docs)                                      │
│  4. Creates an issue with the complete draft release notes        │
│  5. Includes contributor acknowledgements and upgrade notes       │
│                                                                  │
│  Output: Issue titled "[release-notes] v0.3.0 Draft Notes"       │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

The release notes are a **draft** — you copy them into the GitHub Release description after reviewing.

---

## The Complete Workflow Catalog

All 11 agentic workflows + 1 CI workflow at a glance, organized by when they run:

### Event-triggered workflows (run when something happens)

| Workflow | Trigger | Creates | Model | What it checks |
|---|---|---|---|---|
| **Component Improver** | PR to `develop`/`main` + weekly Wed | Draft PR | `gemini-3-pro` | Best practices alignment + documentation improvements |
| **Context Generator** | Push to `main` (post-merge) | Draft PR | `gpt-4.1` | Missing context files for new skills |
| **CI Failure Diagnostician** | `Forge Tests` workflow fails | Draft PR | `gpt-4.1` | Root cause analysis and proposed fixes for test failures |
| **Milestone Lifecycle** | Milestone created + daily 08:00 UTC | Issue | `claude-opus-4.6` | Feature planning, progress tracking, blocker identification |
| **Feature Decomposer** | Issue labeled `milestone-feature` | Issue (multiple) | `gemini-3-pro` | Decomposes features into Copilot-assignable work items |
| **Release Notes Generator** | Tag push or release publish | Issue | `claude-haiku-4.5` | Categorized changelog from merged PRs |

### Scheduled workflows (run on a timer)

| Workflow | Schedule | Creates | Model | What it checks |
|---|---|---|---|---|
| **Quality Gate (CI)** | Sun 09:00 UTC + every PR | CI Results | N/A (pytest/bash) | Schema validation, context integrity, duplicates, conventions, cross-refs |
| **Project Manager Agent** | Mon (scattered) + ROADMAP changes | Issue | `claude-opus-4.6` | Roadmap–implementation gap analysis |
| **Test Coverage Improver** | Tue 09:00 UTC | Draft PR | `gpt-4.1` | Coverage gaps in test harness, generates missing tests |
| **Doc Maintainer** | Thu (scattered) | Draft PR | `gemini-3-pro` | Doc accuracy + verbosity reduction (two-stage pipeline) |
| **Stale Gardener** | Sat (scattered) | Issue | `gpt-5.1-codex-mini` | Dormant issues and PRs |
| **Dependency Sentinel** | Daily (scattered) | Draft PR | `gpt-5.1-codex-mini` | Outdated dependency references |

### Migrated to Deterministic CI (no longer agentic)

The following validation tasks were moved from LLM-powered agentic workflows to fast, deterministic `pytest` tests in `forge-tests.yml`:

| Former Workflow | CI Replacement | Test File |
|---|---|---|
| Agent Validator | `validate-agents` job | `test_json_schemas.py`, `test_cross_references.py` |
| Skill Validator | `validate-skills` job | `test_file_structure.py`, `test_yaml_frontmatter.py` |
| Hook Quality Checker | `validate-hooks` job | `test_hook_syntax.sh`, `test_shellcheck.sh` |
| Context Pruner | `validate-context` job | `test_context_integrity.py` |
| Cross-Reference Checker | `check-xrefs` job | `test_xref_links.py` |
| Duplication Detector | `detect-duplicates` job | `test_duplication.py` |
| Convention Enforcer | `enforce-conventions` job | `test_conventions.py` |
| Health Dashboard | `quality-report` job | Aggregates all CI results |

### How to tell workflow outputs apart

Every workflow output is labeled and prefixed:

| Prefix in title | Source workflow | Type | Model |
|---|---|---|---|
| `[improve]` | Component Improver | Best practices + documentation | `gemini-3-pro` |
| `[context]` | Context Generator | New skill context files | `gpt-4.1` |
| `[ci-fix]` | CI Failure Diagnostician | Auto-diagnosed test fix | `gpt-4.1` |
| `[milestone]` | Milestone Lifecycle | Planning + progress + review | `claude-opus-4.6` |
| `[Work item]` | Feature Decomposer | Decomposed work items | `gemini-3-pro` |
| `[release-notes]` | Release Notes Generator | Changelog draft | `claude-haiku-4.5` |
| `[pm]` | Project Manager Agent | Roadmap execution plan | `claude-opus-4.6` |
| `[test-coverage]` | Test Coverage Improver | Missing test generation | `gpt-4.1` |
| `[docs]` | Doc Maintainer | Sync + unbloat | `gemini-3-pro` |
| `[stale]` | Stale Gardener | Dormant work review | `gpt-5.1-codex-mini` |
| `[deps]` | Dependency Sentinel | Upgrade proposal | `gpt-5.1-codex-mini` |

All workflow-generated items also carry the **`forge-automation`** label, so you can filter them:
- **Issues → Labels → `forge-automation`** to see all automation outputs
- **Pull requests → Labels → `forge-automation`** to see all suggested changes

---

## Common Developer Scenarios

### Scenario 1: "I added a new skill"

You create `forge-plugin/skills/my-new-skill/SKILL.md` and `examples.md`, then open a PR to `develop`.

**What happens automatically:**
1. **Quality Gate CI** runs on your PR → validates schema, structure, naming conventions, and cross-references
2. **Component Improver** triggers on your PR → may create a draft PR with best-practices improvements

**After merge to `main`:**
3. **Context Generator** detects your new skill has no context file → creates a draft PR adding one

**On the next scheduled run:**
4. **Component Improver** (Wednesday) may suggest additional improvements during its weekly scan

### Scenario 2: "I modified an agent config"

You update `forge-plugin/agents/athena.config.json` and open a PR.

**What happens automatically:**
1. **Quality Gate CI** validates JSON schema compliance, cross-references, and conventions
2. **Component Improver** may suggest improvements to the agent documentation

### Scenario 3: "I changed a hook script"

You edit `forge-plugin/hooks/memory_quality_gate.sh` and open a PR.

**What happens automatically:**
1. **Quality Gate CI** validates hook syntax, safety modes (`set -euo pipefail`), and `hooks.json` registration
2. **Component Improver** may suggest improvements to hook documentation or structure

### Scenario 4: "I just want to see overall repo health"

No code changes needed. Check the **CI results**:
1. Go to **Actions → Forge Tests** and look at the latest run
2. The **Quality Gate Summary** step shows traffic-light results for all validation checks
3. Check the **Issues** tab filtered by `forge-automation` for actionable findings

### Scenario 5: "I want to cut a release"

1. Merge your final PR to `main`
2. Push a tag: `git tag v0.3.0 && git push --tags`
3. The **Release Notes Generator** creates a `[release-notes]` issue within minutes
4. Copy the categorized notes into your GitHub Release description
5. Publish the release

---

## FAQ for Contributors

### "Do I need to fix everything a workflow flags?"

No. Workflow outputs are **suggestions**. Some findings are intentional design choices. Close the issue or PR with a brief note explaining why — this also helps the workflows learn what patterns to avoid flagging in the future.

### "Can I run a workflow manually?"

Yes. Every workflow supports `workflow_dispatch`. Go to **Actions → select the workflow → Run workflow**. This is useful for testing or getting an on-demand check.

### "What happens when a workflow has no changes to propose?"

**PR-creating workflows** (Component Improver, Doc Maintainer, Test Coverage Improver, etc.) use `if-no-changes: "ignore"` in their safe-outputs configuration. This means:
- If the workflow analyzes code but finds no improvements needed → **no PR is created**
- If the workflow would create an empty PR → **no PR is created**
- You only see PRs when there's actual work to review

**Issue-creating workflows** (Stale Gardener, Project Manager Agent, Milestone Lifecycle) always create an issue with summary counts, even if the counts are zero. This provides an audit trail that the workflow ran successfully and found no problems.

### "A workflow created a PR. What do I do?"

Review the diff in the draft PR. If the changes improve code quality, approve and merge it. If not, close it with a brief comment explaining why. The workflow learns from these decisions over time.

### "How do I know if a workflow ran on my PR?"

Check the **Actions** tab on your PR. You'll see workflow runs listed. Also check the **Issues** tab for any new `forge-automation` items created around the same time.

### "The automation created an issue I disagree with."

Close the issue with a comment explaining your reasoning. This is normal and expected — the workflows optimize for catching potential problems, and some will be false positives. A target of < 20% false positive rate is maintained.

### "Do workflows ever modify my code directly?"

Never. Workflows create **issues** (findings) or **draft PRs** (proposed changes). They never push commits to your branch, force-merge, or auto-close your work.

### "What about security issues?"

Security issues should never be reported publicly. The security vulnerability template redirects you to `SECURITY.md`, which explains the private disclosure process via GitHub Security Advisories.

### "I'm a maintainer. What should I check weekly?"

Every Monday morning, review:
1. The Sunday **Quality Gate CI** results — validation status across the codebase
2. Any `[stale]` issue from Saturday — dormant work to ping or close
3. The Monday `[pm]` issue — roadmap alignment and priorities
4. Open `forge-automation` draft PRs — merge the useful ones, close the rest
5. Any `[milestone]` issues from daily runs — blocker identification and progress tracking

---

## File Map — Where Things Live

```
.github/
├── ISSUE_TEMPLATE/                    ← 5 issue forms for contributors
│   ├── bug_report.yml                    Report a defect
│   ├── feature_request.yml               Propose an enhancement
│   ├── documentation_improvement.yml     Flag stale/unclear docs
│   ├── security_vulnerability.yml        Private security reporting
│   ├── quality_issue.yml                 Quality findings (human or automation)
│   └── config.yml                        Disables blank issues, security link
│
├── workflows/
│   ├── shared/                        ← Shared building blocks
│   │   ├── forge-base.md                 Engine + read-only permissions
│   │   ├── forge-pr-creator.md           Defaults for PR-creating workflows
│   │   ├── forge-issue-creator.md        Defaults for issue-creating workflows
│   │   ├── forge-conventions.md          Forge project structure context
│   │   └── forge-quality-issue-template.md  Issue body contract
│   │
│   ├── forge-*.md                     ← 11 workflow source files (human-readable)
│   ├── forge-*.lock.yml               ← Compiled GitHub Actions (auto-generated)
│   └── forge-tests.yml                ← Deterministic CI pipeline (8 validation jobs)

AGENTIC_WORKFLOWS_ROADMAP.md          ← Technical roadmap, schedule, and KPIs
AGENTIC_FORGE.md                      ← This file — contributor guide
SECURITY.md                           ← Private vulnerability reporting policy
```

### Key things to remember about these files

- **Never edit `.lock.yml` files** — they are auto-generated by `gh aw compile`
- **Workflow source is Markdown** — the `.md` files in `.github/workflows/` contain YAML frontmatter (configuration) and a prompt body (instructions for the AI)
- **Shared imports reduce duplication** — workflows import common config from `shared/` instead of repeating it
- **Issue templates use YAML forms** — the `.yml` files in `ISSUE_TEMPLATE/` define structured input forms, not freeform Markdown

---

> *Forged by Hephaestus. Guarded by his tireless automatons. Worthy of Olympus.*

