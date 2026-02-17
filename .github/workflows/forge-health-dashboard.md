---
description: "Weekly Forge health dashboard summarizing all quality dimensions"
imports:
  - shared/forge-base.md
  - shared/forge-issue-creator.md
  - shared/forge-quality-issue-template.md
  - shared/forge-conventions.md
  - shared/model-gemini.md
engine:
  id: copilot
  model: gemini-3-flash-preview
on:

  workflow_dispatch:
permissions:
  contents: read
  issues: read
  pull-requests: read
tools:
  github:
    toolsets: [default]
safe-outputs:
  create-issue:
    labels: ["forge-automation", "health-dashboard", "weekly-report"]
    title-prefix: "[health] "
    max: 1
    close-older-issues: true
---

# Forge Health Dashboard

Generate a comprehensive weekly health report covering all Forge quality dimensions.

## Report Sections

### 1. Skills Health

For all files in `forge-plugin/skills/`:

- **Total count** of skill directories
- **Template compliance %** — skills with all required sections from `SKILL_TEMPLATE.md`
- **Missing examples** — skills without `examples.md` file
- **Outdated versions** — skills with `version` field older than 90 days
- **6-Step workflow compliance** — skills following the mandatory workflow pattern

### 2. Context Health

For all files in `forge-plugin/context/`:

- **File count per domain** — breakdown by `engineering/`, `angular/`, `azure/`, `dotnet/`, `python/`, etc.
- **Stale files** — context files with `lastUpdated` older than 90 days
- **Orphaned index entries** — files listed in domain `index.md` but don't exist
- **Missing index entries** — files that exist but aren't in domain `index.md`
- **Coverage gaps** — skills without corresponding context files

### 3. Agent Health

For all files in `forge-plugin/agents/`:

- **Total count** — number of agent `.md` + `.config.json` pairs
- **Config validation** — agents with valid JSON against `agent_config.schema.json`
- **Broken skill references** — skills listed in agent configs that don't exist
- **Broken MCP references** — MCPs referenced that don't exist in `forge-plugin/mcps/`
- **Missing memory directories** — agents without `memory/agents/{name}/` directory

### 4. Hook Health

For all files in `forge-plugin/hooks/`:

- **Total count** — number of `.sh` scripts
- **Shellcheck passing** — hooks with no shellcheck warnings/errors
- **Registered in hooks.json** — scripts listed in `forge-plugin/hooks/hooks.json`
- **Documented in HOOKS_GUIDE.md** — hooks documented in the guide
- **Safety compliance** — scripts with `set -euo pipefail` present

### 5. Cross-Reference Integrity

Check all cross-references:

- **Skills → Context** — skills referencing context domains that exist
- **Skills → Agents** — agent configs referencing valid skills
- **Skills → Commands** — commands referencing valid skills
- **Agents → MCPs** — agent configs referencing valid MCP servers
- **Hooks → hooks.json** — all hook scripts registered
- **Context → Indexes** — all context files listed in domain indexes

### 6. Growth Trends

Compare against last week's report (if exists):

- **Skills added/removed** — net change in skill count
- **Context files added/removed** — net change per domain
- **Agents added/removed** — net change in agent count
- **Hooks added/removed** — net change in hook count

### 7. Delivery & Operations Metrics

Track repository execution health from issue/PR activity:

- **Test coverage trend** — latest coverage and week-over-week delta (if available from CI artifacts/reports)
- **Issue velocity** — issues opened vs closed in trailing 7 and 30 days
- **PR cycle time** — median time from PR open to merge in trailing 30 days
- **Review throughput** — merged PR count and review turnaround trends
- **Code quality trend** — trendline from quality workflow findings (critical/warning/info counts)

## Output Format

Create a single issue with:

```markdown
# Forge Health Report — {YYYY-MM-DD}

Template: quality_issue
Source Workflow: forge-health-dashboard
Run Trigger: schedule
Detected On: {YYYY-MM-DD}
Severity: info

## 📊 Executive Summary

- Overall Health Score: {percentage}
- Critical Issues: {count}
- Warnings: {count}
- Total Components: {count}

## 🔨 Skills Health ({count} total)

| Metric | Value | Status |
|--------|-------|--------|
| Template Compliance | {%} | {🟢/🟡/🔴} |
| Missing Examples | {count} | {🟢/🟡/🔴} |
| Outdated Versions | {count} | {🟢/🟡/🔴} |
| 6-Step Compliance | {%} | {🟢/🟡/🔴} |

## 📚 Context Health ({count} total)

| Domain | Files | Stale | Orphaned | Missing |
|--------|-------|-------|----------|---------|
| engineering | {n} | {n} | {n} | {n} |
| angular | {n} | {n} | {n} | {n} |
| ... | ... | ... | ... | ... |

## 🏛️ Agent Health ({count} total)

| Metric | Value | Status |
|--------|-------|--------|
| Valid Configs | {count} | {🟢/🟡/🔴} |
| Broken Skill Refs | {count} | {🟢/🟡/🔴} |
| Broken MCP Refs | {count} | {🟢/🟡/🔴} |
| Missing Memory Dirs | {count} | {🟢/🟡/🔴} |

## 🪝 Hook Health ({count} total)

| Metric | Value | Status |
|--------|-------|--------|
| Shellcheck Passing | {%} | {🟢/🟡/🔴} |
| Registered | {count}/{total} | {🟢/🟡/🔴} |
| Documented | {count}/{total} | {🟢/🟡/🔴} |
| Safety Compliant | {%} | {🟢/🟡/🔴} |

## 🔗 Cross-Reference Integrity

| Reference Type | Valid | Broken | Status |
|----------------|-------|--------|--------|
| Skills → Context | {n} | {n} | {🟢/🟡/🔴} |
| Agents → Skills | {n} | {n} | {🟢/🟡/🔴} |
| Commands → Skills | {n} | {n} | {🟢/🟡/🔴} |
| Agents → MCPs | {n} | {n} | {🟢/🟡/🔴} |
| Hooks → Registry | {n} | {n} | {🟢/🟡/🔴} |

## 📈 Growth Trends (vs. last week)

| Component | Change | Trend |
|-----------|--------|-------|
| Skills | {+/-n} | {📈/📉/➡️} |
| Context Files | {+/-n} | {📈/📉/➡️} |
| Agents | {+/-n} | {📈/📉/➡️} |
| Hooks | {+/-n} | {📈/📉/➡️} |

## 🚚 Delivery & Operations Metrics

| Metric | 7-Day | 30-Day | Trend | Status |
|--------|-------|--------|-------|--------|
| Test Coverage | {x%} | {x%} | {📈/📉/➡️} | {🟢/🟡/🔴} |
| Issue Velocity (opened/closed) | {n}/{n} | {n}/{n} | {📈/📉/➡️} | {🟢/🟡/🔴} |
| PR Cycle Time (median) | {xh} | {xh} | {📈/📉/➡️} | {🟢/🟡/🔴} |
| Review Throughput (merged PRs) | {n} | {n} | {📈/📉/➡️} | {🟢/🟡/🔴} |
| Quality Findings (C/W/I) | {n/n/n} | {n/n/n} | {📈/📉/➡️} | {🟢/🟡/🔴} |

## 🎯 Action Items

{List of prioritized recommendations based on findings}
```

## Constraints

- Use 🟢 for healthy (0 issues), 🟡 for warning (1-3 issues), 🔴 for critical (4+ issues)
- Calculate overall health score as weighted average of all dimensions
- Only create one issue per week (max: 1, close-older-issues: true)
- If no significant changes from last week, still create report but note stability
- Include direct links to problematic files for easy navigation
- Keep issue structure aligned with `.github/ISSUE_TEMPLATE/quality_issue.yml`

## Analysis Tools

Use these bash commands for analysis:

```bash
# Count skills
find forge-plugin/skills -name "SKILL.md" | wc -l

# Find missing examples.md
find forge-plugin/skills -type d -mindepth 1 -maxdepth 1 ! -exec test -e '{}/examples.md' \; -print

# Count agents
ls forge-plugin/agents/*.config.json | wc -l

# Validate JSON configs
for f in forge-plugin/agents/*.config.json; do jq empty "$f" 2>&1 || echo "Invalid: $f"; done

# Count hooks
find forge-plugin/hooks -name "*.sh" -type f | wc -l

# Check hook registration
jq -r '.hooks[].handler' forge-plugin/hooks/hooks.json | sort

# Count context files per domain
find forge-plugin/context -name "*.md" ! -name "index.md" | cut -d/ -f3 | sort | uniq -c
```
