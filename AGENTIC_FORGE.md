# ⚒️ The Forge — Agentic Workflows Guide

> *"The tireless automatons of Hephaestus's workshop never sleep — they sweep the forge floor, sharpen every blade, and polish each shield while the gods rest."*

This guide explains, in plain language, how The Forge's **19 agentic workflows** work alongside you as a contributor. No deep infrastructure knowledge required — just an understanding of PRs, issues, and releases.

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
│  GitHub detects the PR event and triggers these          │
│  workflows based on changed file paths:                  │
│                                                          │
│  ┌──────────────────┐  Changed skills/agents/context?    │
│  │ Skill Simplifier │──▶ Creates a PR simplifying        │
│  │                  │    verbose documentation            │
│  └──────────────────┘                                    │
│                                                          │
│  ┌──────────────────┐  Changed any Forge files?          │
│  │ Duplication      │──▶ Creates an issue listing         │
│  │ Detector         │    duplicated content               │
│  └──────────────────┘                                    │
│                                                          │
│  ┌──────────────────┐  Changed context files?            │
│  │ Context Pruner   │──▶ Creates an issue if frontmatter  │
│  │                  │    is invalid or refs are broken     │
│  └──────────────────┘                                    │
│                                                          │
│  ┌──────────────────┐  Changed any Forge files?          │
│  │ Convention       │──▶ Creates a PR fixing naming,      │
│  │ Enforcer         │    formatting, convention drift      │
│  └──────────────────┘                                    │
│                                                          │
│  ┌──────────────────┐  PR targets develop?               │
│  │ Best Practices   │──▶ Creates a PR on YOUR branch      │
│  │ Improver         │    with quality improvements         │
│  └──────────────────┘                                    │
│                                                          │
│  ┌──────────────────┐  Changed hook scripts?             │
│  │ Hook Quality     │──▶ Creates an issue if hooks         │
│  │ Checker          │    violate safety/perf rules         │
│  └──────────────────┘                                    │
│                                                          │
└──────────────────────────────────────────────────────────┘
       │
       ▼
  Human reviewer sees your code + workflow outputs
  and makes the merge decision
```

### What you'll actually see

When a workflow activates on your PR, one of two things appears:

1. **A new issue** is created — labeled `forge-automation` — with findings about your changes. Check the Issues tab for anything prefixed with `[duplication]`, `[context-maintenance]`, `[skill-structure]`, or `[hook-quality]`.

2. **A new draft PR** is created — either targeting your branch (Best Practices Improver) or targeting `develop`/`main` (Simplifier, Convention Enforcer). These show up as separate PRs you can review, cherry-pick from, or ignore.

### What to do about workflow outputs

| Output you see | What it means | What to do |
|---|---|---|
| `[duplication]` issue | Content is repeated across files | Consider consolidating; close the issue if intentional |
| `[context-maintenance]` issue | Broken references or stale frontmatter | Fix the references in your PR before merging |
| `[skill-structure]` issue | Your skill is missing required sections | Add the missing sections per `SKILL_TEMPLATE.md` |
| Draft PR on your branch | Suggested quality improvements | Review the diff, merge if helpful, close if not |
| Draft PR on develop/main | Simplification or convention fix | Review at your pace; it auto-expires after 7 days |

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

Workflow-generated issues (from Health Dashboard, Cross-Reference Checker, etc.) also follow the **Quality Issue** template structure. This means all issues — whether created by humans or automation — share a consistent format that makes triage, filtering, and milestone planning predictable.

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
│  │ (06:00 UTC, scattered)       │  for outdated or vulnerable    │
│  │                              │  references. Creates a draft   │
│  │ Output: Draft PR             │  PR with safe upgrades.        │
│  └──────────────────────────────┘                                │
│                                                                  │
│  ┌──────────────────────────────┐                                │
│  │ Project Milestone Tracker    │  Scans open milestones for     │
│  │ (08:00 UTC, scattered)       │  progress, blocked items, and  │
│  │                              │  velocity trends. Creates a    │
│  │ Output: Issue                │  daily status report.          │
│  └──────────────────────────────┘                                │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Weekday workflows (Monday–Friday)

```
┌──────────────────────────────────────────────────────────────────┐
│                    MONDAY THROUGH FRIDAY                          │
│                                                                  │
│  ┌──────────────────────────────┐                                │
│  │ Doc Sync                     │  Validates that README,        │
│  │ (07:00 UTC)                  │  ROADMAP, CONTRIBUTING, and    │
│  │                              │  COOKBOOK match the actual      │
│  │ Output: PR                   │  codebase counts and paths.    │
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
│  │ Health Dashboard             │  The "executive summary"       │
│  │ (09:00 UTC)                  │  of repo health. Covers 7      │
│  │                              │  dimensions: skills, context,  │
│  │ Output: Issue                │  agents, hooks, cross-refs,    │
│  │                              │  growth trends, and delivery   │
│  │                              │  metrics (issue velocity,      │
│  │                              │  PR cycle time, coverage).     │
│  └──────────────────────────────┘                                │
│                                                                  │
│  MONDAY                                                          │
│  ┌──────────────────────────────┐                                │
│  │ Project Manager Agent        │  Compares ROADMAP targets      │
│  │ (09:00 UTC)                  │  against actual implementation │
│  │                              │  state. Proposes milestone     │
│  │ Output: Issue                │  breakdowns and priorities.    │
│  └──────────────────────────────┘                                │
│                                                                  │
│  TUESDAY                                                         │
│  ┌──────────────────────────────┐  ┌──────────────────────────┐  │
│  │ Cross-Reference Checker      │  │ Skill Validator          │  │
│  │ (08:00 UTC)                  │  │ (09:00 UTC)              │  │
│  │                              │  │                          │  │
│  │ Validates 8 reference        │  │ Checks skill template    │  │
│  │ matrices between skills,     │  │ compliance, mandatory    │  │
│  │ agents, context, hooks,      │  │ 6-step workflow, and     │  │
│  │ commands, and MCPs.          │  │ examples.md presence.    │  │
│  │                              │  │                          │  │
│  │ Output: Issue                │  │ Output: Issue            │  │
│  └──────────────────────────────┘  └──────────────────────────┘  │
│                                                                  │
│  WEDNESDAY                                                       │
│  ┌──────────────────────────────┐                                │
│  │ Agent Validator              │  Validates all .config.json    │
│  │ (09:00 UTC)                  │  files against the agent       │
│  │                              │  schema and checks skill/MCP   │
│  │ Output: Issue                │  references exist.             │
│  └──────────────────────────────┘                                │
│                                                                  │
│  THURSDAY                                                        │
│  ┌──────────────────────────────┐  ┌──────────────────────────┐  │
│  │ Skill Validator (2nd run)    │  │ Doc Unbloat              │  │
│  │ (09:00 UTC)                  │  │ (10:00 UTC)              │  │
│  │                              │  │                          │  │
│  │ Same as Tuesday run.         │  │ Reviews docs for         │  │
│  │                              │  │ verbosity and creates    │  │
│  │ Output: Issue                │  │ PRs with simplified      │  │
│  │                              │  │ versions.                │  │
│  └──────────────────────────────┘  │                          │  │
│                                    │ Output: PR               │  │
│                                    └──────────────────────────┘  │
│  FRIDAY                                                          │
│  ┌──────────────────────────────┐                                │
│  │ Hook Quality Checker         │  Validates set -euo pipefail,  │
│  │ (07:00 UTC)                  │  5-second budget, idempotency, │
│  │                              │  hooks.json registration, and  │
│  │ Output: Issue                │  HOOKS_GUIDE.md documentation. │
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

- A **Health Dashboard** issue with the overall score and drill-down tables
- A **Cross-Reference** issue (if any broken links were found)
- Possibly a **Stale Review** issue listing dormant work
- Any **validation issues** from Skill/Agent/Hook checkers

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

All 19 workflows at a glance, organized by when they run:

### Event-triggered workflows (run when something happens)

| Workflow | Trigger | Creates | What it checks |
|---|---|---|---|
| **Skill Simplifier** | PR to `develop`/`main` | Draft PR | Verbosity in skill documentation |
| **Duplication Detector** | PR to `develop`/`main` | Issue | Repeated content across components |
| **Context Pruner** | PR to `develop`/`main` | Issue | Frontmatter validity, stale refs, index integrity |
| **Convention Enforcer** | PR to `develop`/`main` | Draft PR | Naming, formatting, convention adherence |
| **Best Practices Improver** | PR to `develop` | Draft PR (on your branch) | Alignment with Claude Code best practices |
| **Context Generator** | Push to `main` (post-merge) | Draft PR | Missing context files for new skills |
| **Issue Triage Agent** | Issue opened/reopened | Issue | Labels, priority, assignment recommendations |
| **Release Notes Generator** | Tag push or release publish | Issue | Categorized changelog from merged PRs |

### Scheduled workflows (run on a timer)

| Workflow | Schedule | Creates | What it checks |
|---|---|---|---|
| **Health Dashboard** | Sun 09:00 UTC | Issue | 7 health dimensions + delivery metrics |
| **Doc Sync** | Mon–Fri 07:00 UTC | Draft PR | Doc accuracy vs actual codebase |
| **Cross-Reference Checker** | Tue 08:00 UTC | Issue | 8 reference matrices between components |
| **Skill Validator** | Tue + Thu 09:00 UTC | Issue | Template compliance, 6-step workflow |
| **Agent Validator** | Wed 09:00 UTC | Issue | Schema compliance, ref integrity |
| **Doc Unbloat** | Thu 10:00 UTC | Draft PR | Documentation verbosity |
| **Hook Quality Checker** | Fri 07:00 UTC | Issue | Script safety, performance, registration |
| **Stale Gardener** | Sat (scattered) | Issue | Dormant issues and PRs |
| **Dependency Sentinel** | Daily (scattered) | Draft PR | Outdated dependency references |
| **Milestone Tracker** | Daily (scattered) | Issue | Progress, blockers, velocity |
| **Project Manager Agent** | Mon (scattered) + ROADMAP changes | Issue | Roadmap–implementation gap analysis |

### How to tell workflow outputs apart

Every workflow output is labeled and prefixed:

| Prefix in title | Source workflow | Type |
|---|---|---|
| `[health]` | Health Dashboard | Weekly report |
| `[xref]` | Cross-Reference Checker | Broken links |
| `[skill-structure]` | Skill Validator | Template gaps |
| `[agent-config]` | Agent Validator | Schema failures |
| `[hook-quality]` | Hook Quality Checker | Script issues |
| `[duplication]` | Duplication Detector | Repeated content |
| `[context-maintenance]` | Context Pruner | Stale/broken context |
| `[triage]` | Issue Triage Agent | Intake recommendation |
| `[milestone]` | Milestone Tracker | Progress report |
| `[pm]` | Project Manager Agent | Roadmap execution plan |
| `[stale]` | Stale Gardener | Dormant work review |
| `[deps]` | Dependency Sentinel | Upgrade proposal |
| `[release-notes]` | Release Notes Generator | Changelog draft |

All workflow-generated items also carry the **`forge-automation`** label, so you can filter them:
- **Issues → Labels → `forge-automation`** to see all automation outputs
- **Pull requests → Labels → `forge-automation`** to see all suggested changes

---

## Common Developer Scenarios

### Scenario 1: "I added a new skill"

You create `forge-plugin/skills/my-new-skill/SKILL.md` and `examples.md`, then open a PR to `develop`.

**What happens automatically:**
1. **Skill Simplifier** reviews your `SKILL.md` for verbosity → may create a simplification PR
2. **Convention Enforcer** checks naming and frontmatter → may create a fix PR
3. **Best Practices Improver** checks against Claude Code patterns → may suggest improvements on your branch
4. **Context Pruner** validates that your skill's context references exist → may create an issue

**After merge to `main`:**
5. **Context Generator** detects your new skill has no context file → creates a PR adding one

**On the next scheduled run:**
6. **Skill Validator** checks your skill against `SKILL_TEMPLATE.md` → creates an issue if sections are missing
7. **Health Dashboard** includes your skill in the weekly count and compliance percentage

### Scenario 2: "I modified an agent config"

You update `forge-plugin/agents/athena.config.json` and open a PR.

**What happens automatically:**
1. **Agent Validator** (if the PR triggers it) checks JSON schema compliance
2. **Convention Enforcer** ensures consistent formatting
3. **Cross-Reference Checker** (on next Tuesday) validates that skills/MCPs in the config still exist

### Scenario 3: "I changed a hook script"

You edit `forge-plugin/hooks/memory_quality_gate.sh` and open a PR.

**What happens automatically:**
1. **Hook Quality Checker** validates `set -euo pipefail`, performance budget, registration in `hooks.json`, and documentation in `HOOKS_GUIDE.md`
2. **Convention Enforcer** checks formatting consistency

### Scenario 4: "I just want to see overall repo health"

No code changes needed. Check the **Issues** tab:
1. Look for the latest `[health]` issue (created every Sunday)
2. It contains tables with traffic-light indicators (🟢/🟡/🔴) for every quality dimension
3. The Action Items section at the bottom lists the highest-priority fixes

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

### "A workflow created a PR on my branch. What do I do?"

The **Best Practices Improver** does this. Review the diff — if the changes are good, merge the PR into your branch. If not, close it. Your original PR is not affected either way.

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
1. The Sunday `[health]` issue — your executive dashboard
2. Any `[stale]` issue from Saturday — dormant work to ping or close
3. The Monday `[pm]` issue — roadmap alignment and priorities
4. Open `forge-automation` PRs — merge the useful ones, close the rest

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
│   ├── forge-*.md                     ← 19 workflow source files (human-readable)
│   └── forge-*.lock.yml               ← Compiled GitHub Actions (auto-generated)

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

