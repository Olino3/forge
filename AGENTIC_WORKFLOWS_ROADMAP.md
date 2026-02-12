# ⚒️ The Forge — Agentic Workflows Roadmap

> *"The tireless automatons of Hephaestus's workshop never sleep — they sweep the forge floor, sharpen every blade, and polish each shield while the gods rest."*

This document details the phased plan for implementing **Continuous Quality Workflows** for The Forge using [GitHub Agentic Workflows (gh-aw)](https://github.github.com/gh-aw/). Each workflow runs as a GitHub Action powered by an AI agent (Copilot engine), continuously improving Forge's codebase quality.

---

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Phase 0 — Bootstrap & Foundation](#phase-0--bootstrap--foundation)
- [Phase 1A — Continuous Simplicity](#phase-1a--continuous-simplicity)
- [Phase 1B — Continuous Context](#phase-1b--continuous-context)
- [Phase 2A — Continuous Refactoring](#phase-2a--continuous-refactoring)
- [Phase 2B — Continuous Style](#phase-2b--continuous-style)
- [Phase 3 — Continuous Improvement](#phase-3--continuous-improvement)
- [Phase 4 — Continuous Documentation](#phase-4--continuous-documentation)
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

## Phase 0 — Bootstrap & Foundation

> **Goal**: Set up gh-aw infrastructure in the Forge repository.
> **Duration**: 1-2 days
> **Dependencies**: None
> **Parallelizable**: No (must complete before all other phases)

### Step 0.1: Install gh-aw CLI

```bash
# Install GitHub CLI (if not already)
gh auth login

# Install gh-aw extension
gh extension install github/gh-aw
```

### Step 0.2: Initialize Repository

```bash
cd /path/to/forge
gh aw init
```

This creates:
- `.github/workflows/` directory structure for agentic workflows
- Necessary configuration files
- Action pin manifest (`.github/aw/actions-lock.json`)

### Step 0.3: Configure Copilot Engine Secret

Since we're using the **Copilot engine**, ensure the repository has access to GitHub Copilot. No additional secrets are required beyond the default `GITHUB_TOKEN`.

### Step 0.4: Create Shared Imports

Create reusable shared configuration files for all Forge workflows:

**`.github/workflows/shared/forge-base.md`** — Common permissions and constraints:
```markdown
---
description: "Shared base configuration for all Forge agentic workflows"
permissions:
  contents: read
engine: copilot
strict: true
---
```

**`.github/workflows/shared/forge-pr-creator.md`** — For workflows that create PRs:
```markdown
---
description: "Shared PR creation configuration for Forge workflows"
permissions:
  contents: write
  pull-requests: write
safe-outputs:
  create-pull-request:
    labels: ["forge-automation", "agentic-workflow"]
    max: 3
    close-older: true
    expire: "+7d"
---
```

**`.github/workflows/shared/forge-issue-creator.md`** — For workflows that create issues:
```markdown
---
description: "Shared issue creation configuration for Forge workflows"
permissions:
  issues: write
safe-outputs:
  create-issue:
    labels: ["forge-automation", "agentic-workflow"]
    max: 3
    close-older: true
    expire: "+7d"
---
```

### Step 0.5: Create Forge Conventions Reference

**`.github/workflows/shared/forge-conventions.md`** — Inline context for all Forge agents:
```markdown
---
description: "Forge project conventions for agentic workflows"
---

## Forge Project Structure

- **Skills**: `forge-plugin/skills/{name}/SKILL.md` + `examples.md`
- **Agents**: `forge-plugin/agents/{name}.md` + `{name}.config.json`
- **Context**: `forge-plugin/context/{domain}/` with YAML frontmatter
- **Hooks**: `forge-plugin/hooks/{name}.sh` (bash, `set -euo pipefail`)
- **Commands**: `forge-plugin/commands/{name}.md` with YAML frontmatter

## Key Conventions

- All documentation is Markdown
- All config is JSON (2-space or 4-space indent)
- All scripts are Bash with `set -e`
- Skills follow the 6-step mandatory workflow
- Context files have YAML frontmatter with tags, sections, estimated tokens
- Hooks must complete in < 5 seconds
- No hardcoded filesystem paths — use interface references
```

### Step 0.6: Compile & Validate Baseline

```bash
# Compile all shared imports
gh aw compile

# Validate compilation
gh aw status
```

### Deliverables

| Artifact | Path |
|----------|------|
| gh-aw initialized repo | `.github/workflows/`, `.github/aw/` |
| Shared base import | `.github/workflows/shared/forge-base.md` |
| Shared PR creator import | `.github/workflows/shared/forge-pr-creator.md` |
| Shared issue creator import | `.github/workflows/shared/forge-issue-creator.md` |
| Forge conventions reference | `.github/workflows/shared/forge-conventions.md` |

---

## Phase 1A — Continuous Simplicity

> **Goal**: Detect and reduce unnecessary complexity in Forge's Markdown, JSON, and Bash assets.
> **Duration**: 2-3 days
> **Dependencies**: Phase 0
> **Parallelizable with**: Phase 1B

### Inspiration

From [Peli's Factory — Continuous Simplicity](https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-continuous-simplicity/):

- **[Automatic Code Simplifier](https://github.com/github/gh-aw/blob/v0.42.13/.github/workflows/code-simplifier.md?plain=1)** — 83% merge rate (5/6 PRs merged)
- **[Duplicate Code Detector](https://github.com/github/gh-aw/blob/v0.42.13/.github/workflows/duplicate-code-detector.md?plain=1)** — 79% merge rate (76/96 PRs merged)

### Quick-Start (from gh-aw)

```bash
# Add the reference workflow, then customize
gh aw add-wizard https://github.com/github/gh-aw/blob/v0.42.13/.github/workflows/code-simplifier.md
```

### Workflow 1A.1: Forge Skill Simplifier

**File**: `.github/workflows/forge-skill-simplifier.md`

**Purpose**: Analyze `SKILL.md` files for overcomplicated instructions, redundant sections, inconsistent structure, and verbose examples.

**Forge-Specific Adaptations** (vs. gh-aw's Code Simplifier):

| gh-aw Original | Forge Adaptation |
|----------------|------------------|
| Analyzes Go source files | Analyzes `forge-plugin/skills/*/SKILL.md` files |
| Looks for code complexity | Looks for instruction verbosity, section bloat, inconsistent patterns |
| Creates PRs with simplified code | Creates PRs with simplified skill documentation |
| Runs on recently modified files | Runs on changed skills in PR, 3 per run max |

**Frontmatter Configuration**:
```yaml
---
description: "Simplify Forge skill documentation by reducing verbosity and improving clarity"
imports:
  - shared/forge-base.md
  - shared/forge-pr-creator.md
  - shared/forge-conventions.md
on:
  pull_request:
    types: [opened, synchronize]
    branches: [develop, main]
  workflow_dispatch:
permissions:
  contents: write
  pull-requests: write
tools:
  github:
    toolsets: [default]
safe-outputs:
  create-pull-request:
    labels: ["forge-automation", "simplicity", "skills"]
    title-prefix: "[simplify] "
    max: 3
    close-older: true
    expire: "+7d"
---
```

**Prompt** (natural language body):
```markdown
# Forge Skill Simplifier

Analyze skill files in `forge-plugin/skills/` for simplification opportunities.

## Analysis Targets

For each `SKILL.md` file, check for:

1. **Verbose instructions** — can they be expressed more concisely?
2. **Redundant sections** — duplicate information across Overview, Workflow Steps, etc.
3. **Inconsistent structure** — deviations from `SKILL_TEMPLATE.md` pattern
4. **Over-engineered examples** — examples that demonstrate too many concepts at once
5. **Dead references** — links to skills, agents, or context files that don't exist

## Constraints

- Preserve all meaningful content — only remove true redundancy
- Keep technical accuracy — don't simplify at the cost of correctness
- Follow the 6-step mandatory workflow pattern
- Maximum 3 PRs per run
- Each PR should address one skill file

## Output

For each simplification, create a PR with:
- Clear title: `[simplify] {skill-name}: {what was simplified}`
- Description explaining what was simplified and why
- Before/after comparison in PR body
```

### Workflow 1A.2: Forge Duplication Detector

**File**: `.github/workflows/forge-duplication-detector.md`

**Purpose**: Find duplicated content patterns across skills, context files, and agent configs.

**Forge-Specific Focus**:
- Duplicate instructions across similar skills (e.g., all auth skills sharing boilerplate)
- Copy-pasted context sections that should be cross-referenced
- Identical hook logic that should be extracted to `hooks/lib/`
- Duplicate frontmatter patterns that should become shared templates

**Frontmatter Configuration**:
```yaml
---
description: "Detect duplicated content across Forge skills, context, and hooks"
imports:
  - shared/forge-base.md
  - shared/forge-issue-creator.md
  - shared/forge-conventions.md
on:
  pull_request:
    types: [opened, synchronize]
    branches: [develop, main]
  workflow_dispatch:
permissions:
  contents: read
  issues: write
tools:
  github:
    toolsets: [default]
safe-outputs:
  create-issue:
    labels: ["forge-automation", "simplicity", "duplication"]
    title-prefix: "[duplication] "
    max: 3
    close-older: true
    expire: "+14d"
    assignees: ["copilot"]
---
```

### Deliverables

| Artifact | Path |
|----------|------|
| Skill Simplifier workflow | `.github/workflows/forge-skill-simplifier.md` |
| Duplication Detector workflow | `.github/workflows/forge-duplication-detector.md` |
| Compiled lock files | `.github/workflows/*.lock.yml` |

---

## Phase 1B — Continuous Context

> **Goal**: Automatically generate context files when new skills are added, and prune/maintain existing context files.
> **Duration**: 3-4 days
> **Dependencies**: Phase 0
> **Parallelizable with**: Phase 1A

This is a **Forge-original workflow** — not based on a gh-aw reference. It addresses a unique Forge need: the `forge-plugin/context/` system requires high-quality, structured context files that stay in sync with skills.

### Workflow 1B.1: Context Generator (On Skill Add)

**File**: `.github/workflows/forge-context-generator.md`

**Purpose**: When a PR adds a new skill to `forge-plugin/skills/`, automatically generate corresponding context files with proper YAML frontmatter.

**Trigger**: On PR merge that adds files matching `forge-plugin/skills/*/SKILL.md`

**How it works**:

1. **Detect new skills** — Compare merged PR's changed files against existing context domains
2. **Determine domain** — Map the new skill to the appropriate context domain (python, dotnet, angular, engineering, etc.)
3. **Generate context file** — Create a context `.md` file with:
   - Valid YAML frontmatter (id, domain, title, type, estimatedTokens, loadingStrategy, sections, tags)
   - Common issues section derived from the skill's domain expertise
   - Quick reference for the skill's key patterns
   - Integration notes with existing context
4. **Update domain index** — Add the new file entry to `context/{domain}/index.md`
5. **Update top-level index** — Update `context/index.md` with file count changes
6. **Create PR** — Submit for human review

**Frontmatter Configuration**:
```yaml
---
description: "Generate context files when new skills are added to Forge"
imports:
  - shared/forge-base.md
  - shared/forge-pr-creator.md
  - shared/forge-conventions.md
on:
  pull_request:
    types: [closed]
    paths:
      - "forge-plugin/skills/*/SKILL.md"
permissions:
  contents: write
  pull-requests: write
tools:
  github:
    toolsets: [default, pull_requests]
safe-outputs:
  create-pull-request:
    labels: ["forge-automation", "context", "new-skill"]
    title-prefix: "[context] "
    max: 1
    expire: "+14d"
---
```

**Prompt**:
```markdown
# Forge Context Generator

When a new skill is added to `forge-plugin/skills/`, generate a matching context file.

## Step 1: Identify New Skills

Check the merged PR for new `SKILL.md` files added under `forge-plugin/skills/`.
If this PR does not add new skills (only modifies existing ones), exit with no action.

## Step 2: Determine Context Domain

Map the skill to an existing context domain based on its category:

| Skill Category | Context Domain |
|---------------|----------------|
| Python-related (django, fastapi, pandas, etc.) | `python/` |
| .NET-related (dotnet-core, csharp) | `dotnet/` |
| Angular-related | `angular/` |
| Azure-related (azure-auth, generate-azure-*) | `azure/` |
| Security-related (secure-code, security-reviewer) | `security/` |
| Git-related (get-git-diff, commit-helper) | `git/` |
| General engineering | `engineering/` |

If no domain exists, place in `engineering/`.

## Step 3: Generate Context File

Create `forge-plugin/context/{domain}/{skill-name}.md` with this structure:

```yaml
---
id: "{domain}/{skill-name}"
domain: {domain}
title: "{Skill Display Name} Context"
type: reference
estimatedTokens: 400
loadingStrategy: conditional
version: "0.2.0-alpha"
lastUpdated: "{today's date}"
sections:
  - name: "Overview"
    estimatedTokens: 50
    keywords: [overview, {skill-name}]
  - name: "Common Issues"
    estimatedTokens: 150
    keywords: [common, issues, problems]
  - name: "Quick Reference"
    estimatedTokens: 100
    keywords: [quick, reference, patterns]
  - name: "Integration"
    estimatedTokens: 100
    keywords: [integration, workflow]
tags: [{domain}, {skill-name}, context, reference]
---
```

Populate sections by reading the skill's `SKILL.md` and extracting:
- **Overview**: Key purpose and when to use this skill
- **Common Issues**: Typical problems and pitfalls (from the skill's domain)
- **Quick Reference**: Essential patterns, commands, or configurations
- **Integration**: How this skill connects to other Forge skills and context

## Step 4: Update Domain Index

Add the new file to `forge-plugin/context/{domain}/index.md`.

## Step 5: Create PR

Create a single PR with all generated context files for human review.
Include in the PR body:
- Which skills triggered the generation
- Which domains were targeted
- What sections were generated
- Token estimates for each file
```

### Workflow 1B.2: Context Pruner & Maintainer

**File**: `.github/workflows/forge-context-pruner.md`

**Purpose**: Maintain existing context files by:
1. Detecting **stale context** — files referencing skills/agents that no longer exist
2. Validating **frontmatter integrity** — required fields, valid domains, reasonable token estimates
3. Identifying **drift** — context that has diverged from its source skill's current capabilities
4. Pruning **orphaned entries** — domain index entries pointing to deleted files

**Trigger**: PRs to develop/main + on-demand

**Frontmatter Configuration**:
```yaml
---
description: "Prune stale context files and validate context integrity in Forge"
imports:
  - shared/forge-base.md
  - shared/forge-issue-creator.md
  - shared/forge-conventions.md
on:
  pull_request:
    types: [opened, synchronize]
    branches: [develop, main]
  workflow_dispatch:
permissions:
  contents: read
  issues: write
tools:
  github:
    toolsets: [default]
safe-outputs:
  create-issue:
    labels: ["forge-automation", "context", "maintenance"]
    title-prefix: "[context-maintenance] "
    max: 1
    close-older: true
    expire: "+14d"
---
```

**Prompt**:
```markdown
# Forge Context Pruner & Maintainer

Validate and maintain the integrity of Forge's context file system.

## Validation Checks

### 1. Staleness Detection
For each context file in `forge-plugin/context/`:
- Check if referenced skills still exist in `forge-plugin/skills/`
- Check if referenced agents still exist in `forge-plugin/agents/`
- Flag files with `lastUpdated` older than 90 days

### 2. Frontmatter Validation
Every context file must have:
- `id` (string, format: "{domain}/{filename}")
- `domain` (string, must match parent directory)
- `title` (string)
- `type` (string: reference | guide | checklist)
- `estimatedTokens` (number, > 0, < 5000)
- `loadingStrategy` (string: always | conditional | on-demand)
- `version` (string, semver)
- `lastUpdated` (string, ISO date)
- `sections` (array with name, estimatedTokens, keywords)
- `tags` (array of strings)

### 3. Drift Detection
Compare context file content against its source skill's SKILL.md:
- Are the context's "Common Issues" still relevant?
- Has the skill added capabilities not reflected in context?
- Are framework versions mentioned still current?

### 4. Index Integrity
- Every file in `forge-plugin/context/{domain}/` must have an entry in `{domain}/index.md`
- Every entry in `{domain}/index.md` must point to an existing file
- `forge-plugin/context/index.md` file counts must match actual counts

## Output

Create a single issue titled "[context-maintenance] Context Health Report — {date}"
with a table of findings organized by severity:
- 🔴 **Critical**: Broken references, missing required frontmatter
- 🟡 **Warning**: Stale content, drift from source skills
- 🟢 **Info**: Suggestions for improvement
```

### Deliverables

| Artifact | Path |
|----------|------|
| Context Generator workflow | `.github/workflows/forge-context-generator.md` |
| Context Pruner workflow | `.github/workflows/forge-context-pruner.md` |
| Compiled lock files | `.github/workflows/*.lock.yml` |

---

## Phase 2A — Continuous Refactoring

> **Goal**: Identify structural improvements across Forge's skill and agent organization.
> **Duration**: 2-3 days
> **Dependencies**: Phase 0
> **Parallelizable with**: Phase 2B

### Inspiration

From [Peli's Factory — Continuous Refactoring](https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-continuous-refactoring/):

- **[Semantic Function Refactor](https://github.com/github/gh-aw/blob/v0.42.13/.github/workflows/semantic-function-refactor.md?plain=1)** — Spots misplaced functions and suggests reorganization
- **[Daily File Diet](https://github.com/github/gh-aw/blob/v0.42.13/.github/workflows/daily-file-diet.md?plain=1)** — 79% merge rate (26/33 PRs merged)

### Quick-Start (from gh-aw)

```bash
gh aw add-wizard https://github.com/github/gh-aw/blob/v0.42.13/.github/workflows/semantic-function-refactor.md
gh aw add-wizard https://github.com/github/gh-aw/blob/v0.42.13/.github/workflows/daily-file-diet.md
```

### Workflow 2A.1: Forge Skill Structure Validator

**File**: `.github/workflows/forge-skill-validator.md`

**Purpose**: Validate all skills adhere to `SKILL_TEMPLATE.md` structure and identify skills that need restructuring.

**Forge-Specific Adaptations**:

| Dimension | What It Checks |
|-----------|----------------|
| **Template Compliance** | Does each `SKILL.md` have all required sections from `SKILL_TEMPLATE.md`? |
| **6-Step Workflow** | Does each skill follow Initial Analysis → Load Memory → Load Context → Perform Analysis → Generate Output → Update Memory? |
| **Examples Presence** | Does each skill dir contain `examples.md`? |
| **Skill Isolation** | Can the skill operate independently without hardcoded references to other skills? |
| **Output Conventions** | Does the skill reference `OUTPUT_CONVENTIONS.md` for its output format? |

**Frontmatter Configuration**:
```yaml
---
description: "Validate Forge skill structure compliance against SKILL_TEMPLATE.md"
imports:
  - shared/forge-base.md
  - shared/forge-issue-creator.md
  - shared/forge-conventions.md
on:
  schedule: "0 9 * * 2,4"  # Tuesdays and Thursdays
  workflow_dispatch:
permissions:
  contents: read
  issues: write
tools:
  github:
    toolsets: [default]
safe-outputs:
  create-issue:
    labels: ["forge-automation", "refactoring", "skills"]
    title-prefix: "[skill-structure] "
    max: 5
    close-older: true
    expire: "+14d"
    assignees: ["copilot"]
---
```

### Workflow 2A.2: Forge Agent Config Validator

**File**: `.github/workflows/forge-agent-validator.md`

**Purpose**: Validate all agent configurations against `agent_config.schema.json` and check cross-references.

**Validation Checks**:

| Check | Description |
|-------|-------------|
| **Schema Compliance** | Does `.config.json` conform to `interfaces/schemas/agent_config.schema.json`? |
| **Skill References** | Do all skills listed in `contextDomains` and `skills` actually exist? |
| **MCP References** | Do referenced MCPs exist in `forge-plugin/mcps/`? |
| **Memory Directory** | Does the agent's `memoryPath` directory exist? |
| **Personality File** | Does the corresponding `.md` file exist with required sections? |
| **Model Consistency** | Is the declared model compatible with the agent's task profile? |

**Frontmatter Configuration**:
```yaml
---
description: "Validate Forge agent configurations for schema compliance and reference integrity"
imports:
  - shared/forge-base.md
  - shared/forge-issue-creator.md
  - shared/forge-conventions.md
on:
  schedule: "0 9 * * 3"  # Wednesdays
  pull_request:
    types: [opened, synchronize]
    paths:
      - "forge-plugin/agents/*.config.json"
      - "forge-plugin/agents/*.md"
  workflow_dispatch:
permissions:
  contents: read
  issues: write
tools:
  github:
    toolsets: [default]
safe-outputs:
  create-issue:
    labels: ["forge-automation", "refactoring", "agents"]
    title-prefix: "[agent-config] "
    max: 3
    close-older: true
    expire: "+14d"
---
```

### Deliverables

| Artifact | Path |
|----------|------|
| Skill Structure Validator | `.github/workflows/forge-skill-validator.md` |
| Agent Config Validator | `.github/workflows/forge-agent-validator.md` |
| Compiled lock files | `.github/workflows/*.lock.yml` |

---

## Phase 2B — Continuous Style

> **Goal**: Enforce consistent style and conventions across all Forge assets.
> **Duration**: 2-3 days
> **Dependencies**: Phase 0
> **Parallelizable with**: Phase 2A

### Inspiration

From [Peli's Factory — Continuous Style](https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-continuous-style/):

- **[Terminal Stylist](https://github.com/github/gh-aw/blob/v0.42.13/.github/workflows/terminal-stylist.md?plain=1)** — 80% merge rate (16/20 PRs merged via causal chain)

### Quick-Start (from gh-aw)

```bash
gh aw add-wizard https://github.com/github/gh-aw/blob/v0.42.13/.github/workflows/terminal-stylist.md
```

### Workflow 2B.1: Forge Convention Enforcer

**File**: `.github/workflows/forge-convention-enforcer.md`

**Purpose**: Enforce Forge-specific style conventions across all asset types.

**Style Rules**:

| Asset | Convention | Example |
|-------|-----------|---------|
| Skill dirs | kebab-case | `react-forms/` not `ReactForms/` |
| Agent files | kebab-case `.md` + `.config.json` | `apollo.md` + `apollo.config.json` |
| Context frontmatter | Required YAML fields present | `id`, `domain`, `tags`, `sections` |
| Hook scripts | `set -euo pipefail` first line after shebang | Every `.sh` in `hooks/` |
| JSON config | Consistent indentation (match existing) | 2-space or 4-space, not mixed |
| Markdown headings | ATX-style (`#`), no trailing `#` | `## Section` not `## Section ##` |
| Interface references | No hardcoded paths | `contextProvider.getIndex()` not `context/python/index.md` |

**Frontmatter Configuration**:
```yaml
---
description: "Enforce Forge coding conventions and style consistency"
imports:
  - shared/forge-base.md
  - shared/forge-pr-creator.md
  - shared/forge-conventions.md
on:
  pull_request:
    types: [opened, synchronize]
    branches: [develop, main]
  workflow_dispatch:
permissions:
  contents: write
  pull-requests: write
tools:
  github:
    toolsets: [default]
safe-outputs:
  create-pull-request:
    labels: ["forge-automation", "style", "conventions"]
    title-prefix: "[style] "
    max: 3
    close-older: true
    expire: "+7d"
---
```

### Workflow 2B.2: Forge Hook Quality Checker

**File**: `.github/workflows/forge-hook-checker.md`

**Purpose**: Validate hook scripts for correctness, safety, and performance budget compliance.

**Checks**:

| Check | Rationale |
|-------|-----------|
| `set -euo pipefail` present | Fail-fast on errors |
| No commands without `\|\| true` on optional greps | Prevent false failures |
| Sources `lib/health_buffer.sh` if using health reporting | Shared utility dependency |
| No `sleep` or long-running commands | 5-second budget |
| Idempotent (safe to run multiple times) | Hook reliability |
| Registered in `hooks.json` | Discovery requirement |
| Documented in `HOOKS_GUIDE.md` | Discoverability |

**Frontmatter Configuration**:
```yaml
---
description: "Validate Forge hook scripts for quality, safety, and performance"
imports:
  - shared/forge-base.md
  - shared/forge-issue-creator.md
  - shared/forge-conventions.md
on:
  schedule: "0 7 * * 5"  # Fridays at 7am
  pull_request:
    types: [opened, synchronize]
    paths:
      - "forge-plugin/hooks/*.sh"
      - "forge-plugin/hooks/hooks.json"
  workflow_dispatch:
permissions:
  contents: read
  issues: write
tools:
  github:
    toolsets: [default]
  bash: ["shellcheck", "grep", "wc", "time"]
safe-outputs:
  create-issue:
    labels: ["forge-automation", "hooks", "quality"]
    title-prefix: "[hook-quality] "
    max: 1
    close-older: true
    expire: "+14d"
---
```

### Deliverables

| Artifact | Path |
|----------|------|
| Convention Enforcer workflow | `.github/workflows/forge-convention-enforcer.md` |
| Hook Quality Checker workflow | `.github/workflows/forge-hook-checker.md` |
| Compiled lock files | `.github/workflows/*.lock.yml` |

---

## Phase 3 — Continuous Improvement

> **Goal**: Holistic repository health analysis and cross-cutting quality improvements.
> **Duration**: 3-4 days
> **Dependencies**: Phase 1A, Phase 1B (for context awareness)
> **Parallelizable with**: Phase 4

### Inspiration

From [Peli's Factory — Continuous Improvement](https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-continuous-improvement/):

- **Repository Quality Improver** — 62% merge rate (25/40 PRs merged)
- **Go Module Usage Expert** — dependency freshness
- **Typist** — type safety improvements

### Workflow 3.1: Forge Health Dashboard

**File**: `.github/workflows/forge-health-dashboard.md`

**Purpose**: Generate a weekly health report covering all Forge quality dimensions.

**Report Sections**:

| Section | Metrics |
|---------|---------|
| **Skills Health** | Total count, template compliance %, skills missing `examples.md`, skills with outdated versions |
| **Context Health** | File count per domain, stale files (>90 days), orphaned index entries, coverage gaps (skills without context) |
| **Agent Health** | Config validation results, broken skill/MCP references, missing memory dirs |
| **Hook Health** | Scripts passing shellcheck, registered in hooks.json, documented in HOOKS_GUIDE |
| **Cross-Reference Integrity** | Broken links between skills, agents, context, and commands |
| **Growth Trends** | Skills/context/agents added since last report |

**Frontmatter Configuration**:
```yaml
---
description: "Weekly Forge health dashboard summarizing all quality dimensions"
imports:
  - shared/forge-base.md
  - shared/forge-conventions.md
on:
  schedule: "0 9 * * 0"  # Sundays at 9am
  workflow_dispatch:
permissions:
  contents: read
  issues: write
tools:
  github:
    toolsets: [default]
  bash: ["find", "jq", "wc", "grep"]
safe-outputs:
  create-issue:
    labels: ["forge-automation", "health-dashboard", "weekly-report"]
    title-prefix: "[health] "
    max: 1
    close-older: true
---
```

### Workflow 3.2: Forge Cross-Reference Checker

**File**: `.github/workflows/forge-xref-checker.md`

**Purpose**: Detect broken cross-references between Forge components.

**Cross-Reference Matrix**:

```
Skills ←→ Context Files (domain mapping)
Skills ←→ Agent Configs (skills[] array)  
Skills ←→ Commands (skills[] in frontmatter)
Agents ←→ MCP Configs (allowedMcps[])
Context ←→ Domain Indexes (file listings)
Hooks  ←→ hooks.json (registration)
Hooks  ←→ HOOKS_GUIDE.md (documentation)
```

**Frontmatter Configuration**:
```yaml
---
description: "Detect broken cross-references between Forge components"
imports:
  - shared/forge-base.md
  - shared/forge-issue-creator.md
  - shared/forge-conventions.md
on:
  schedule: "0 8 * * 2"  # Tuesdays
  workflow_dispatch:
permissions:
  contents: read
  issues: write
tools:
  github:
    toolsets: [default]
  bash: ["jq", "grep", "find"]
safe-outputs:
  create-issue:
    labels: ["forge-automation", "cross-reference", "integrity"]
    title-prefix: "[xref] "
    max: 1
    close-older: true
    expire: "+14d"
---
```

### Workflow 3.3: Forge Best Practices Improver

**File**: `.github/workflows/forge-best-practices-improver.md`

**Purpose**: When a feature branch PR targets `develop`, analyze the changed skills, agents, and commands for alignment with current best practices from Anthropic's [Claude Code](https://github.com/anthropics/claude-code) repository conventions. Create a PR **back to the triggering feature branch** with improvements, so the author can review and merge before the feature lands on `develop`.

**Why Anthropic's Claude Code?**

| Reason | Detail |
|--------|--------|
| **Canonical reference** | Claude Code's `CLAUDE.md` and plugin conventions are the upstream standard Forge extends |
| **Evolving best practices** | Anthropic updates their conventions frequently; this workflow keeps Forge current |
| **Quality uplift** | Skills, agents, and commands that follow upstream patterns are more compatible and maintainable |

**Analysis Scope**:

| Component | Checks |
|-----------|--------|
| **Skills** | SKILL.md follows latest CLAUDE.md patterns, examples use current idioms, no deprecated conventions |
| **Agents** | Config references valid tools/models, personality sections follow current prompting best practices |
| **Commands** | Frontmatter uses current schema, workflow steps align with recommended patterns |

**Trigger**: Feature branch PRs to `develop` only (not main — improvements should land before release)

**Frontmatter Configuration**:
```yaml
---
description: "Improve skills, agents, and commands based on Anthropic Claude Code best practices"
imports:
  - shared/forge-base.md
  - shared/forge-pr-creator.md
  - shared/forge-conventions.md
on:
  pull_request:
    types: [opened, synchronize]
    branches: [develop]
  workflow_dispatch:
permissions:
  contents: write
  pull-requests: write
tools:
  github:
    toolsets: [default]
safe-outputs:
  create-pull-request:
    base-ref: ${{ github.head_ref }}  # PR targets the feature branch, not develop
    labels: ["forge-automation", "best-practices", "improvement"]
    title-prefix: "[best-practices] "
    max: 1
    close-older: true
    expire: "+7d"
---
```

**Prompt**:
```markdown
# Forge Best Practices Improver

You are an expert on Anthropic's Claude Code conventions and Forge plugin architecture.
When a feature branch PR targets `develop`, analyze the **changed files** for improvement
opportunities based on current best practices.

## Reference Sources

1. **Anthropic Claude Code repo** — https://github.com/anthropics/claude-code
   - Check their CLAUDE.md, plugin conventions, and recommended patterns
2. **Forge conventions** — `CONTRIBUTING.md`, `CLAUDE.md`, skill/agent/command templates

## Analysis Steps

1. Identify which skills, agents, or commands were modified in this PR
2. For each modified file, compare against current Anthropic Claude Code conventions
3. Look for:
   - Outdated prompting patterns that Anthropic has since improved
   - Missing best-practice sections (e.g., error handling, edge cases)
   - Inconsistencies with upstream CLAUDE.md conventions
   - Opportunities to leverage newer Claude Code capabilities
4. Generate improvement PRs **targeting the feature branch** (not develop)

## Constraints

- Only improve files that were **changed in the triggering PR** — don't scan the whole repo
- Each improvement must include a rationale citing the specific best practice
- Preserve the author's intent and domain-specific customizations
- Maximum 1 improvement PR per triggering PR
- If no improvements needed, do nothing (don't create empty PRs)

## Output

For each improvement, create a PR targeting `${{ github.head_ref }}` with:
- Clear title: `[best-practices] {component}: {improvement summary}`
- Description linking to the specific Anthropic convention or pattern
- Before/after comparison showing the improvement
```

### Deliverables

| Artifact | Path |
|----------|------|
| Health Dashboard workflow | `.github/workflows/forge-health-dashboard.md` |
| Cross-Reference Checker | `.github/workflows/forge-xref-checker.md` |
| Best Practices Improver | `.github/workflows/forge-best-practices-improver.md` |
| Compiled lock files | `.github/workflows/*.lock.yml` |

---

## Phase 4 — Continuous Documentation

> **Goal**: Keep Forge documentation accurate and consistent with code changes.
> **Duration**: 2-3 days
> **Dependencies**: Phase 0
> **Parallelizable with**: Phase 3

### Inspiration

From [Peli's Factory — Continuous Documentation](https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-documentation/):

- **[Daily Documentation Updater](https://github.com/github/gh-aw/blob/v0.42.13/.github/workflows/daily-doc-updater.md?plain=1)** — 96% merge rate (57/59 PRs merged) ⭐
- **[Documentation Unbloat](https://github.com/github/gh-aw/blob/v0.42.13/.github/workflows/unbloat-docs.md?plain=1)** — 85% merge rate (88/103 PRs merged)

### Quick-Start (from gh-aw)

```bash
gh aw add-wizard https://github.com/github/gh-aw/blob/v0.42.13/.github/workflows/daily-doc-updater.md
gh aw add-wizard https://github.com/github/gh-aw/blob/v0.42.13/.github/workflows/unbloat-docs.md
```

### Workflow 4.1: Forge Doc Sync

**File**: `.github/workflows/forge-doc-sync.md`

**Purpose**: Ensure `ROADMAP.md`, `CONTRIBUTING.md`, `COOKBOOK.md`, `README.md` and other top-level docs stay in sync with the actual state of skills, agents, commands, and hooks.

**Sync Targets**:

| Document | What to Check |
|----------|---------------|
| `ROADMAP.md` | Skill/agent/command/hook counts match reality |
| `CONTRIBUTING.md` | File structure examples match actual layout |
| `COOKBOOK.md` | Referenced skills/commands still exist |
| `README.md` | Feature claims match implemented capabilities |
| Domain `index.md` files | File listings match directory contents |

**Frontmatter Configuration**:
```yaml
---
description: "Keep Forge top-level documentation in sync with codebase reality"
imports:
  - shared/forge-base.md
  - shared/forge-pr-creator.md
  - shared/forge-conventions.md
on:
  schedule: "0 7 * * 1-5"  # Weekdays at 7am
  workflow_dispatch:
permissions:
  contents: write
  pull-requests: write
tools:
  github:
    toolsets: [default]
safe-outputs:
  create-pull-request:
    labels: ["forge-automation", "documentation", "sync"]
    title-prefix: "[docs] "
    max: 3
    close-older: true
    expire: "+7d"
---
```

### Workflow 4.2: Forge Doc Unbloat

**File**: `.github/workflows/forge-doc-unbloat.md`

**Purpose**: Review and simplify documentation by reducing verbosity, removing redundancy, and improving scannability.

**Frontmatter Configuration**:
```yaml
---
description: "Reduce documentation bloat in Forge by simplifying verbose content"
imports:
  - shared/forge-base.md
  - shared/forge-pr-creator.md
  - shared/forge-conventions.md
on:
  schedule: "0 10 * * 4"  # Thursdays at 10am
  workflow_dispatch:
permissions:
  contents: write
  pull-requests: write
tools:
  github:
    toolsets: [default]
safe-outputs:
  create-pull-request:
    labels: ["forge-automation", "documentation", "unbloat"]
    title-prefix: "[docs-unbloat] "
    max: 3
    close-older: true
    expire: "+7d"
---
```

### Deliverables

| Artifact | Path |
|----------|------|
| Doc Sync workflow | `.github/workflows/forge-doc-sync.md` |
| Doc Unbloat workflow | `.github/workflows/forge-doc-unbloat.md` |
| Compiled lock files | `.github/workflows/*.lock.yml` |

---

## Dependency Graph

```
Phase 0 (Bootstrap)
  │
  ├──→ Phase 1A (Simplicity)     ←── can run in parallel ──→  Phase 1B (Context)
  │         │                                                       │
  │         └──→ Phase 3 (Improvement) ←──── depends on ───────────┘
  │                    │
  ├──→ Phase 2A (Refactoring)    ←── can run in parallel ──→  Phase 2B (Style)
  │
  └──→ Phase 4 (Documentation)  ←── can run in parallel ──→  Phase 3 (Improvement)
```

### Parallelization Matrix

| Phase | Can Run With | Blocked By |
|-------|-------------|------------|
| **0** | Nothing | Nothing |
| **1A** | 1B, 2A, 2B, 4 | 0 |
| **1B** | 1A, 2A, 2B, 4 | 0 |
| **2A** | 1A, 1B, 2B, 4 | 0 |
| **2B** | 1A, 1B, 2A, 4 | 0 |
| **3** | 4 | 1A, 1B |
| **4** | 1A, 1B, 2A, 2B, 3 | 0 |

### Recommended Execution Order

For a single developer:
```
Week 1:  Phase 0 → Phase 1A + Phase 1B (parallel)
Week 2:  Phase 2A + Phase 2B (parallel) → Phase 4
Week 3:  Phase 3 (depends on 1A + 1B outputs)
```

For two developers:
```
Dev A:  Phase 0 → Phase 1A → Phase 2A → Phase 3
Dev B:  (wait for Phase 0) → Phase 1B → Phase 2B → Phase 4
```

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

### Phase Completion Criteria

| Phase | Done When |
|-------|-----------|
| 0 | `gh aw compile` succeeds, shared imports compile, `gh aw status` shows ready |
| 1A | Both simplicity workflows run successfully, first PR/issue created |
| 1B | Context generator fires on test skill PR, pruner produces first health report |
| 2A | Skill validator catches known non-compliant skill, agent validator catches test error |
| 2B | Convention enforcer proposes at least one valid style fix |
| 3 | Health dashboard produces accurate report, xref checker finds known broken link, best practices improver creates valid improvement PR on feature branch |
| 4 | Doc sync catches intentionally stale count, unbloat proposes readable simplification |

### Ongoing KPIs (post-launch)

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Merge Rate** | > 70% | Merged PRs / Created PRs per workflow |
| **False Positive Rate** | < 20% | Closed-without-merge PRs + wontfix issues |
| **Context Coverage** | > 80% | Skills with matching context files / total skills |
| **Template Compliance** | > 90% | Skills passing structure validation / total skills |
| **Agent Config Validity** | 100% | Agents passing schema validation / total agents |
| **Hook Budget Compliance** | 100% | Hooks completing < 5s / total hooks |

---

## Workflow Schedule Overview

Spread across the week to avoid overlapping runs and PR noise:

| Trigger | Schedule / Event | Workflow |
|---------|-----------------|----------|
| **PR** | `pull_request → develop, main` | Forge Skill Simplifier |
| **PR** | `pull_request → develop, main` | Forge Duplication Detector |
| **PR** | `pull_request → develop, main` | Context Pruner & Maintainer |
| **PR** | `pull_request → develop, main` | Forge Convention Enforcer |
| **PR** | `pull_request → develop` (feature branches) | Forge Best Practices Improver |
| **PR merge** | `push → main` (post-merge) | Forge Context Generator |
| **Schedule** | Mon-Fri 07:00 | Forge Doc Sync |
| **Schedule** | Tue 08:00 | Forge Cross-Reference Checker |
| **Schedule** | Tue, Thu 09:00 | Forge Skill Structure Validator |
| **Schedule** | Wed 09:00 | Forge Agent Config Validator |
| **Schedule** | Thu 10:00 | Forge Doc Unbloat |
| **Schedule** | Fri 07:00 | Forge Hook Quality Checker |
| **Schedule** | Sun 09:00 | Forge Health Dashboard |

All PR-triggered workflows also support `workflow_dispatch` for on-demand runs.

---

## References

### gh-aw Documentation
- [Quick Start Guide](https://github.github.com/gh-aw/setup/quick-start/)
- [Creating Workflows](https://github.github.com/gh-aw/setup/creating-workflows/)
- [Frontmatter Reference](https://github.github.com/gh-aw/reference/frontmatter/)
- [Safe Outputs Reference](https://github.github.com/gh-aw/reference/safe-outputs/)
- [Workflow Structure](https://github.github.com/gh-aw/reference/workflow-structure/)
- [Design Patterns](https://github.github.com/gh-aw/blog/2026-01-24-design-patterns/)
- [DailyOps Pattern](https://github.github.com/gh-aw/patterns/dailyops/)
- [Authoring Workflows](https://github.github.com/gh-aw/blog/2026-02-08-authoring-workflows/)

### Peli's Factory Blog Series
- [Welcome to Peli's Agent Factory](https://github.github.com/gh-aw/blog/2026-01-12-welcome-to-pelis-agent-factory/)
- [Continuous Simplicity](https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-continuous-simplicity/) — Code Simplifier, Duplicate Code Detector
- [Continuous Refactoring](https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-continuous-refactoring/) — Semantic Function Refactor, Daily File Diet
- [Continuous Style](https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-continuous-style/) — Terminal Stylist
- [Continuous Improvement](https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-continuous-improvement/) — Repository Quality Improver
- [Continuous Documentation](https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-documentation/) — Daily Doc Updater, Doc Unbloat

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

*Last Updated: February 12, 2026*
*Maintained by: The Forge Keepers*

*Forged by Hephaestus. Automated by his tireless automatons. Worthy of Olympus.*
