# ⚒️ The Forge — Cookbook

> *"Know the recipe before you light the forge. A smith who swings blindly wastes both steel and time."*

Strategies, workflows, persona-based plugin selection, and proven recipes for getting the most out of The Forge.

---

## Table of Contents

- [Persona Quick Starts](#persona-quick-starts)
- [Workflow Recipes](#workflow-recipes)
- [Plugin Selection Guide](#plugin-selection-guide)
- [Agent Delegation Patterns](#agent-delegation-patterns)
- [Tips & Tricks](#tips--tricks)

---

## Persona Quick Starts

Choose the persona closest to your role and install the recommended plugins. All personas include the `forge-core` plugin by default.

### 🐍 Python Developer

**Goal**: Azure SDK, FastAPI, data pipelines, testing

**Install**:
```bash
/plugin install ms-skills-python@forge-marketplace
/plugin install ms-skills-core@forge-marketplace
/plugin install modern-python@forge-marketplace
```

**Key Skills**: `fastapi` · `django` · `pandas` · `postgres` · `python-code-review` · `generate-python-unit-tests` · `python-dependency-management` + 41 Azure SDK Python skills

**Recommended Agents**: `@python-engineer` · `@data-scientist` · `@apollo` (quality)

**Starter Workflow**:
```
/analyze → understand the codebase
/implement → build new features
/test → generate pytest suites
/improve → refactor and optimize
```

---

### 🔐 Security Researcher

**Goal**: Vulnerability detection, smart contract auditing, code security review

**Install**:
```bash
/plugin install sharp-edges@forge-marketplace
/plugin install insecure-defaults@forge-marketplace
/plugin install static-analysis@forge-marketplace
/plugin install differential-review@forge-marketplace
/plugin install variant-analysis@forge-marketplace
/plugin install semgrep-rule-creator@forge-marketplace
```

**Key Skills**: `secure-code` · `security-reviewer` · `code-reviewer` + Trail of Bits security plugins (53 skills across 27 plugins)

**Recommended Agents**: `@athena` (architecture review) · `@apollo` (quality) · `@ares` (deployment hardening)

**Starter Workflow**:
```
/analyze → map attack surface
skill:sharp-edges → identify footgun APIs
skill:insecure-defaults → detect hardcoded secrets
skill:variant-analysis → find similar vulns across codebase
/document → write security findings report
```

---

### ⚛️ Full-Stack Engineer

**Goal**: React/Next.js frontend + backend API development

**Install**:
```bash
/plugin install vercel-skills@forge-marketplace
/plugin install stitch-skills@forge-marketplace
/plugin install ms-skills-typescript@forge-marketplace
```

**Key Skills**: `nextjs` · `react-forms` · `tailwind-patterns` · `accessibility` · `nestjs` · `graphql-design` · `api-design` + Vercel and Google Labs skills

**Recommended Agents**: `@frontend-engineer` · `@full-stack-engineer` · `@aphrodite` (UX/UI) · `@athena` (architecture)

**Starter Workflow**:
```
/brainstorm → explore architecture options
/implement → build features end-to-end
skill:accessibility → verify WCAG compliance
/test → generate Jest and integration tests
/build → bundle and deploy
```

---

### 🔷 .NET Developer

**Goal**: Azure SDK for .NET, ASP.NET Core, C# development

**Install**:
```bash
/plugin install ms-skills-dotnet@forge-marketplace
/plugin install ms-skills-core@forge-marketplace
/plugin install ms-agents@forge-marketplace
```

**Key Skills**: `dotnet-core` · `csharp` · `dotnet-code-review` · `azure-function` + 29 Azure SDK .NET skills

**Recommended Agents**: `@devops-engineer` · `@athena` (architecture) · `@apollo` (quality)

**Starter Workflow**:
```
/analyze → understand solution structure
/azure-function → scaffold Azure Functions
/azure-pipeline → set up CI/CD
/test → generate xUnit test suites
```

---

### 🔗 Smart Contract Auditor

**Goal**: Blockchain security auditing, compliance verification

**Install**:
```bash
/plugin install building-secure-contracts@forge-marketplace
/plugin install entry-point-analyzer@forge-marketplace
/plugin install spec-to-code-compliance@forge-marketplace
/plugin install property-based-testing@forge-marketplace
```

**Key Skills**: Trail of Bits blockchain security suite (11 skills for 6 blockchains) + `secure-code` · `code-reviewer`

**Recommended Agents**: `@athena` (architecture) · `@apollo` (quality) · `@artemis` (testing)

**Starter Workflow**:
```
skill:entry-point-analyzer → map state-changing functions
skill:building-secure-contracts → run vulnerability scanners
skill:spec-to-code-compliance → verify spec conformance
skill:property-based-testing → generate property tests
/document → write audit report
```

---

### ⚛️ React / React Native Developer

**Goal**: Modern React patterns, mobile development, component design

**Install**:
```bash
/plugin install vercel-skills@forge-marketplace
/plugin install stitch-skills@forge-marketplace
```

**Key Skills**: `react-expert` · `react-native-expert` · `nextjs` · `react-forms` · `tailwind-patterns` · `animate` · `responsive-images` + Vercel composition patterns and best practices

**Recommended Agents**: `@frontend-engineer` · `@aphrodite` (UX/UI design) · `@artemis` (testing)

**Starter Workflow**:
```
/brainstorm → component architecture decisions
/implement → build components and pages
skill:accessibility → WCAG compliance check
skill:responsive-images → optimize image loading
/test → generate React Testing Library tests
```

---

## Workflow Recipes

Proven multi-step workflows for common development scenarios.

### Recipe: Feature Development (End-to-End)

```
1. /analyze              → Understand existing code and architecture
2. /brainstorm           → Explore design options with @athena
3. /implement            → Build the feature, delegating to specialists
4. /test                 → Generate comprehensive test suites
5. /improve              → Refactor, optimize, add error handling
6. /document             → Update docs and create /claudedocs output
7. /build                → Verify build passes and deploy
```

**Best for**: New features, major enhancements, greenfield components

---

### Recipe: /analyze → /improve → /test (Codebase Hardening)

```
1. /analyze              → Map code quality issues, tech debt, and risks
2. /improve              → Apply targeted improvements
3. /test                 → Ensure changes don't break existing functionality
4. skill:secure-code     → Security review of critical paths
5. /document             → Document changes for team
```

**Best for**: Legacy code improvement, pre-release hardening, tech debt sprints

---

### Recipe: Azure Deployment Pipeline

```
1. /analyze              → Understand the application structure
2. /azure-function       → Generate Azure Functions (with Tilt + Azurite for local dev)
3. /azure-pipeline       → Create CI/CD pipeline YAML
4. skill:generate-azure-bicep  → Infrastructure as Code
5. /test                 → Integration and smoke tests
6. /build                → Validate deployment artifacts
```

**Best for**: Cloud-native Azure deployments, serverless architectures

---

### Recipe: Legacy Modernization

```
1. /analyze              → Assess current state, dependencies, and risks
2. skill:legacy-modernizer  → Get modernization strategy
3. /brainstorm           → Architecture modernization options with @prometheus
4. /implement            → Incremental migration (strangler fig pattern)
5. /test                 → Ensure backward compatibility
6. skill:architecture-design → Validate new architecture
7. /document             → Document migration decisions and progress
```

**Best for**: Monolith-to-microservices, framework upgrades, Python 2→3

---

### Recipe: Security Audit

```
1. /analyze              → Map the codebase and entry points
2. skill:security-reviewer → Systematic security review
3. skill:sharp-edges     → Identify footgun APIs (if Trail of Bits plugins installed)
4. skill:insecure-defaults → Detect hardcoded secrets and weak crypto
5. skill:static-analysis → Run CodeQL/Semgrep analysis
6. /improve              → Apply security fixes
7. /test                 → Regression tests for fixes
8. /document             → Security audit report to /claudedocs
```

**Best for**: Pre-launch security reviews, compliance audits, pen-test preparation

---

### Recipe: ETL Pipeline Development

```
1. /analyze              → Understand data sources and schemas
2. skill:database-schema-analysis → Map existing schemas
3. /etl-pipeline         → Generate extraction, transformation, loading code
4. skill:database-optimizer → Optimize query performance
5. /test                 → Data validation and pipeline tests
6. /mock                 → Generate mock data for testing
```

**Best for**: Data engineering, warehouse loading, API data integration

---

## Plugin Selection Guide

### Token Budget Strategy

The Forge's modular plugin system lets you control your context window usage. Load only what you need:

| Strategy | Plugins Loaded | Est. Context Use | Best For |
|----------|---------------|------------------|----------|
| **Minimal** | forge-core only | ~15% | Quick fixes, small tasks |
| **Focused** | forge-core + 1-2 vendor plugins | ~25% | Typical development |
| **Full-Stack** | forge-core + 3-4 vendor plugins | ~40% | Complex multi-domain work |
| **Comprehensive** | forge-core + many plugins | ~60%+ | Audits, large migrations |

### Decision Tree

```
What are you building?
├── Python backend → ms-skills-python + ms-skills-core
├── .NET backend → ms-skills-dotnet + ms-skills-core
├── TypeScript/Node → ms-skills-typescript + ms-skills-core
├── Java backend → ms-skills-java + ms-skills-core
├── React/Next.js frontend → vercel-skills + stitch-skills
├── Security audit → Trail of Bits plugins (pick by domain)
├── Smart contract audit → building-secure-contracts + entry-point-analyzer
├── CI/CD setup → sentry-skills (code review + PR workflows)
└── General development → forge-core is sufficient
```

### Anti-Patterns

| Don't | Why | Do Instead |
|-------|-----|-----------|
| Load all 38 plugins at once | Wastes 60%+ of context window | Load 2-4 plugins relevant to your task |
| Install language plugins you don't use | Skills for Java won't help a Python project | Match plugins to your tech stack |
| Skip forge-core | All 102 core skills and 19 agents are in forge-core | Always keep forge-core installed |
| Ignore the Armory listing | You might miss a skill that solves your exact problem | Run `skill:divine` to discover relevant skills |

---

## Agent Delegation Patterns

### When to Delegate vs. Do It Yourself

| Scenario | Approach |
|----------|----------|
| Quick file edit | Direct — no agent needed |
| Code review | `@apollo` — quality assessments are his domain |
| Architecture decision | `@athena` — strategic analysis and design |
| Multi-step feature | `@zeus` — orchestration across agents |
| Testing strategy | `@artemis` — comprehensive test planning |
| UX/UI review | `@aphrodite` — design system and accessibility |
| Data pipeline | `@demeter` — data cultivation and transformation |
| Deployment | `@ares` — battle-tested deployment strategies |
| Integration work | `@hermes` — API integration and communication |
| Documentation | `@technical-writer` — professional docs |

### Multi-Agent Workflow Example

For a complex feature that touches frontend, backend, and infrastructure:

```
1. @zeus → Plan the work, break into tasks
2. @athena → Design the architecture
3. @frontend-engineer → Build React components
4. @python-engineer → Build API endpoints
5. @artemis → Design test strategy
6. @apollo → Code review everything
7. @ares → Deploy to staging
8. @technical-writer → Document the feature
```

### The Olympian Council Pattern

For critical decisions, convene multiple agents:

```
@zeus: "We need to decide on the authentication strategy for this multi-tenant app."
  → @athena analyzes architecture implications
  → @ares evaluates security posture  
  → @hermes reviews API integration impact
  → @hera ensures governance compliance
  → @zeus synthesizes and decides
```

---

## Tips & Tricks

### Skill Discovery

- Run `skill:divine` to get personalized recommendations based on your codebase
- Browse [forge-plugin/skills/](forge-plugin/skills/) for the full 102-skill listing
- Use `skill:docs-workflow` to bootstrap project documentation

### Memory System

- Memory is persistent across sessions — The Forge remembers what worked
- Each skill, agent, and command has its own memory namespace
- Use `/remember` to explicitly store important decisions
- Memory auto-prunes stale entries (see `memory/lifecycle.md`)

### Context Loading

- Context is loaded on-demand by default — the 5-step loading protocol minimizes waste
- Use `contextProvider.getIndex("{domain}")` to explore available context
- Cross-domain triggers automatically load related context (see `cross_domain.md`)

### Performance

- Start with `/analyze` to give agents proper context before delegating
- Use focused plugin sets — don't load plugins you won't use
- Chain commands with appropriate breaks to let agents process results
- Memory from prior sessions accelerates repeated workflows

### Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Agent produces generic output | Run `/analyze` first to provide codebase context |
| Wrong skill triggered | Use explicit `skill:name` syntax instead of natural language |
| Memory stale or conflicting | Check `memory/lifecycle.md`, run memory pruning |
| Too many plugins loaded | Remove unused plugins, check token budget strategy above |
| Hook failures | Check `forge-plugin/hooks/lib/health_buffer.sh` and logs |

---

*"The best smith doesn't just know their tools — they know which tool to reach for, and when."*

*Last Updated: February 13, 2026*
*Maintained by: The Forge Keepers*
