# Skill Creator Examples

This file contains example scenarios demonstrating how to use the skill-creator skill to design and generate new Claude Code skills.

---

## Example 1: Creating a Code Review Skill for Go

### Scenario
Creating a new skill that performs structured code reviews for Go projects, checking for idiomatic patterns, concurrency issues, error handling, and performance anti-patterns.

### User Prompt
```
Create a new skill for reviewing Go code. It should check for idiomatic Go patterns, proper error handling, goroutine safety, and common performance issues. Target experienced Go developers.
```

### Skill Execution

**Step 1 - Initial Analysis**:
```
Skill: go-code-review
Domain: engineering (primary), go (supporting — if available)
Purpose: Perform structured code reviews for Go projects, producing actionable findings with severity levels and fix suggestions
Target Users: Experienced Go developers seeking automated review feedback
Triggers: ["review go code", "go code review", "check go patterns"]
Type: Code Analysis
Scope: 6 workflow steps, single output document
```

**Step 2 - Load Memory**:
- No previous memory found; first skill creation session

**Step 3 - Load Context**:
- Loaded engineering domain context for code review standards
- Loaded SKILL_TEMPLATE.md for canonical structure
- No Go-specific domain context available — will rely on built-in knowledge

**Step 4 - Design Skill Architecture**:
```
Freedom Level: Strict Procedural
  - Code reviews require consistent checklist execution
  - Missing a check category could let bugs through
  - All 4 review categories must be evaluated every time

Token Budget: Compact
  - Target users are experienced Go developers
  - Focus on checklist items, not Go tutorials
  - Include brief rationale per finding, not explanations of Go concepts

Error Prevention Patterns:
  1. Reviewing non-Go files — validate file extensions before analysis
  2. Missing concurrency checks — require goroutine/channel analysis even if none found
  3. Ignoring test files — explicitly include or exclude test files based on user request
  4. Shallow error handling review — check for bare `if err != nil` without wrapping

Progressive Disclosure:
  - Essential: 4 review categories with findings and severity
  - On demand: Fix suggestions with code snippets
  - Reference: Links to Go style guide and effective Go docs

Interface Usage:
  - ContextProvider: Load engineering domain for review standards
  - MemoryStore: Track review patterns per project, common findings
  - SkillInvoker: Not needed — standalone skill
  - ExecutionContext: Not needed — no command chaining
```

**Step 5 - Generate SKILL.md**:

## ```markdown
name: go-code-review
version: 1.0.0
description: Perform structured code reviews for Go projects checking idiomatic patterns, error handling, concurrency safety, and performance anti-patterns.
context:
  primary_domain: engineering
  memory:
    skill_memory: go-code-review
    scopes:
      - review_patterns
      - project_findings
tags:
  - code-review
  - go
  - quality
  - analysis
triggers:
  - review go code
  - go code review
##   - check go patterns

# Go Code Review

## ⚠️ MANDATORY COMPLIANCE ⚠️
...

## Mandatory Workflow

### Step 1: Initial Analysis
- Identify target files or packages for review
- Detect Go version and module structure

### Step 2: Load Memory
- Load previous review findings for this project

### Step 3: Load Context
- Load engineering domain context for review standards

### Step 4: Execute Review Checklist
- **Idiomatic Go**: Naming conventions, receiver types, interface design, slice/map usage
- **Error Handling**: Error wrapping, sentinel errors, panic recovery, error type assertions
- **Concurrency Safety**: Goroutine lifecycle, channel usage, mutex patterns, race conditions
- **Performance**: Unnecessary allocations, string concatenation in loops, inefficient sorting

### Step 5: Generate Output
- Save review findings to `/claudedocs/go-code-review_{project}_{date}.md`

### Step 6: Update Memory
- Record findings patterns and project-specific conventions
```

**Step 6 - Generate examples.md**:
- 3 examples: HTTP handler review, concurrent pipeline review, CLI tool review

**Step 7 - Generate Memory Structure**:
- Created `memory/skills/go-code-review/index.md` with `review_patterns.md` and `project_findings.md`

**Step 8 - Quality Validation**:
```
✅ YAML frontmatter: All required fields present
✅ Interface references: All four links included
✅ Mandatory workflow: 6 steps with gate conditions
✅ Compliance checklist: 6 checkboxes present
✅ Examples: 3 complete scenarios
✅ Memory structure: index.md with 2 memory files
```

**Step 9 - Output**:
- `skills/go-code-review/SKILL.md`
- `skills/go-code-review/examples.md`
- `memory/skills/go-code-review/index.md`

**Step 10 - Memory Update**:
- Created `created_skills.md` with go-code-review entry (Code Analysis, Strict Procedural, Compact)
- Created `design_patterns.md` with code review skill pattern

---

## Example 2: Creating a Deployment Automation Skill

### Scenario
Creating a skill that generates deployment configurations and runbooks for containerized applications, supporting Docker Compose, Kubernetes, and cloud-specific platforms.

### User Prompt
```
I need a skill that helps automate deployments. Given an application, it should generate Docker Compose files, Kubernetes manifests, and deployment runbooks. It should handle different environments (dev, staging, prod).
```

### Skill Execution

**Step 1 - Initial Analysis**:
```
Skill: deploy-automation
Domain: engineering (primary), devops (supporting)
Purpose: Generate deployment configurations and runbooks for containerized applications across multiple environments and platforms
Target Users: DevOps engineers and full-stack developers deploying containerized apps
Triggers: ["deploy app", "generate deployment", "create deployment config", "deployment automation"]
Type: DevOps & Infrastructure
Scope: 8 workflow steps, conditional outputs based on target platform
```

**Step 2 - Load Memory**:
- No previous memory found; first skill creation session

**Step 3 - Load Context**:
- Loaded engineering domain context
- Loaded devops domain context for deployment patterns
- Loaded SKILL_TEMPLATE.md for canonical structure

**Step 4 - Design Skill Architecture**:
```
Freedom Level: Flexible Guidance
  - Deployment configurations vary widely by project
  - Users may need only Docker Compose, only Kubernetes, or both
  - Environment-specific overrides require adaptive logic

Token Budget: Detailed
  - Deployment mistakes are costly (downtime, data loss)
  - Rationale for each configuration choice prevents misconfigurations
  - Include environment-specific warnings and best practices

Error Prevention Patterns:
  1. Hardcoded secrets in configs — validate no secrets in generated files, use env vars or secret managers
  2. Missing health checks — require health/readiness probes in every deployment config
  3. No resource limits — enforce CPU/memory limits in Kubernetes manifests
  4. Single-replica production — warn if prod config has replicas < 2
  5. Missing rollback strategy — require rollback procedure in every runbook

Progressive Disclosure:
  - Essential: Core deployment config for the primary platform
  - On demand: Multi-environment overrides, scaling policies, monitoring integration
  - Reference: Platform-specific API references, Helm chart structure

Interface Usage:
  - ContextProvider: Load devops domain for deployment patterns and best practices
  - MemoryStore: Track deployment patterns per project, environment configs
  - SkillInvoker: Not needed — standalone skill
  - ExecutionContext: Not needed — no command chaining
```

**Step 5 - Generate SKILL.md**:

## ```markdown
name: deploy-automation
version: 1.0.0
description: Generate deployment configurations and runbooks for containerized applications across Docker Compose, Kubernetes, and cloud platforms with environment-specific overrides.
context:
  primary_domain: engineering
  supporting_domains:
    - devops
  memory:
    skill_memory: deploy-automation
    scopes:
      - deployment_patterns
      - project_configs
tags:
  - devops
  - deployment
  - docker
  - kubernetes
  - automation
triggers:
  - deploy app
  - generate deployment
  - create deployment config
##   - deployment automation

# Deployment Automation

## ⚠️ MANDATORY COMPLIANCE ⚠️
...

## Mandatory Workflow

### Step 1: Initial Analysis
- Identify application type, tech stack, and deployment requirements
- Classify target platform(s): Docker Compose, Kubernetes, cloud-native
- Determine environments needed: dev, staging, production

### Step 2: Load Memory
- Load previous deployment configs for this project

### Step 3: Load Context
- Load devops domain for deployment patterns and security best practices

### Step 4: Analyze Application Requirements
- Map services, dependencies, and inter-service communication
- Identify stateful vs stateless components
- Determine storage, networking, and secret management needs

### Step 5: Generate Deployment Configs
- Docker Compose for local dev (if applicable)
- Kubernetes manifests with health checks, resource limits, and scaling policies (if applicable)
- Environment-specific overrides for staging and production

### Step 6: Generate Deployment Runbook
- Pre-deployment checklist (tests pass, images built, secrets configured)
- Deployment steps with verification at each stage
- Rollback procedure with specific commands
- Post-deployment validation checks

### Step 7: Generate Output
- Save all configs and runbook to `/claudedocs/`

### Step 8: Update Memory
- Record deployment patterns and environment configurations
```

**Step 6 - Generate examples.md**:
- 3 examples: Node.js microservice to Kubernetes, Python API with Docker Compose, multi-service app with Helm charts

**Step 7 - Generate Memory Structure**:
- Created `memory/skills/deploy-automation/index.md` with `deployment_patterns.md` and `project_configs.md`

**Step 8 - Quality Validation**:
```
✅ YAML frontmatter: All required fields present
✅ Interface references: All four links included
✅ Mandatory workflow: 8 steps with gate conditions
✅ Compliance checklist: 8 checkboxes present
✅ Examples: 3 complete scenarios
✅ Memory structure: index.md with 2 memory files
```

**Step 9 - Output**:
- `skills/deploy-automation/SKILL.md`
- `skills/deploy-automation/examples.md`
- `memory/skills/deploy-automation/index.md`

**Step 10 - Memory Update**:
- Updated `created_skills.md` with deploy-automation entry (DevOps & Infrastructure, Flexible Guidance, Detailed)
- Updated `design_patterns.md` with deployment skill pattern — noted the importance of error prevention for secret management

---

## Example 3: Creating a Testing Strategy Skill

### Scenario
Creating a skill that designs comprehensive testing strategies for projects, including test pyramid definition, framework selection, coverage targets, and CI integration plans.

### User Prompt
```
Create a skill that designs testing strategies for projects. Given a codebase, it should recommend a test pyramid, select testing frameworks, set coverage targets, and plan CI integration. It should work for any language.
```

### Skill Execution

**Step 1 - Initial Analysis**:
```
Skill: testing-strategy
Domain: engineering (primary)
Purpose: Design comprehensive testing strategies including test pyramid, framework selection, coverage targets, and CI integration plans
Target Users: Tech leads and senior developers establishing testing practices for new or under-tested projects
Triggers: ["testing strategy", "test plan", "design tests", "testing approach"]
Type: Planning & Workflow
Scope: 8 workflow steps, conditional outputs based on project characteristics
```

**Step 2 - Load Memory**:
- Found previous memory from skill-creator sessions
- Reviewed: Planning & Workflow skills benefit from detailed token budget
- Applied: Use structured tables for framework comparisons

**Step 3 - Load Context**:
- Loaded engineering domain context for testing standards
- Loaded SKILL_TEMPLATE.md for canonical structure

**Step 4 - Design Skill Architecture**:
```
Freedom Level: Flexible Guidance
  - Testing strategies vary significantly by language, framework, and team maturity
  - Some projects need unit-heavy pyramids, others need integration-heavy diamonds
  - Framework selection depends on ecosystem and team preferences

Token Budget: Detailed
  - Testing strategy decisions have long-term impact
  - Include rationale for each framework recommendation
  - Explain trade-offs between coverage targets and development velocity

Error Prevention Patterns:
  1. Language-agnostic framework recommendations — always validate frameworks exist for the target language
  2. Unrealistic coverage targets — calibrate targets based on project type (100% for libraries, 70-80% for applications)
  3. Ignoring integration tests — ensure the strategy addresses all test levels, not just unit tests
  4. Missing CI integration — every strategy must include how tests run in CI

Progressive Disclosure:
  - Essential: Test pyramid with level definitions and framework selection
  - On demand: Coverage targets per module, CI pipeline configuration, test data management
  - Reference: Framework comparison matrices, example test structures

Interface Usage:
  - ContextProvider: Load engineering domain for testing standards
  - MemoryStore: Track testing patterns per project type and language
  - SkillInvoker: May invoke project-health to assess current test coverage
  - ExecutionContext: Not needed — no command chaining
```

**Step 5 - Generate SKILL.md**:

## ```markdown
name: testing-strategy
version: 1.0.0
description: Design comprehensive testing strategies with test pyramid definition, framework selection, coverage targets, and CI integration plans for any language or framework.
context:
  primary_domain: engineering
  memory:
    skill_memory: testing-strategy
    scopes:
      - strategy_patterns
      - project_strategies
tags:
  - testing
  - strategy
  - quality
  - planning
  - ci-cd
triggers:
  - testing strategy
  - test plan
  - design tests
##   - testing approach

# Testing Strategy

## ⚠️ MANDATORY COMPLIANCE ⚠️
...

## Mandatory Workflow

### Step 1: Initial Analysis
- Identify project language(s), framework(s), and current testing state
- Classify project type: library, application, API, CLI tool
- Assess team testing maturity: no tests, basic tests, comprehensive tests

### Step 2: Load Memory
- Load previous testing strategies for similar project types

### Step 3: Load Context
- Load engineering domain for testing standards and best practices

### Step 4: Design Test Pyramid
- Define test levels: unit, integration, end-to-end, contract (if applicable)
- Set ratio targets for each level (e.g., 70/20/10)
- Identify what belongs at each level for this specific project

### Step 5: Select Testing Frameworks
- Recommend framework per test level with rationale
- Compare 2-3 alternatives for each level
- Validate framework compatibility with project tech stack

### Step 6: Define Coverage Targets
- Set overall coverage target calibrated to project type
- Set per-module targets for critical vs non-critical code
- Define what counts as "covered" (line, branch, path)

### Step 7: Generate Output
- Save testing strategy to `/claudedocs/testing-strategy_{project}_{date}.md`

### Step 8: Update Memory
- Record strategy patterns and framework selections by language
```

**Step 6 - Generate examples.md**:
- 3 examples: React SPA testing strategy, Python library testing strategy, microservices API testing strategy

**Step 7 - Generate Memory Structure**:
- Created `memory/skills/testing-strategy/index.md` with `strategy_patterns.md` and `project_strategies.md`

**Step 8 - Quality Validation**:
```
✅ YAML frontmatter: All required fields present
✅ Interface references: All four links included
✅ Mandatory workflow: 8 steps with gate conditions
✅ Compliance checklist: 8 checkboxes present
✅ Examples: 3 complete scenarios
✅ Memory structure: index.md with 2 memory files
```

**Step 9 - Output**:
- `skills/testing-strategy/SKILL.md`
- `skills/testing-strategy/examples.md`
- `memory/skills/testing-strategy/index.md`

**Step 10 - Memory Update**:
- Updated `created_skills.md` with testing-strategy entry (Planning & Workflow, Flexible Guidance, Detailed)
- Updated `design_patterns.md` with testing skill pattern — noted that SkillInvoker integration adds value for project-health cross-referencing

---

## Summary of Skill Creation Scenarios

1. **Go code review** — Strict Procedural skill with compact token budget for experienced users; 4-category checklist with severity levels
2. **Deployment automation** — Flexible Guidance skill with detailed token budget; conditional outputs based on target platform (Docker Compose, Kubernetes, cloud-native)
3. **Testing strategy** — Flexible Guidance skill with detailed token budget; language-agnostic design with ecosystem-specific framework recommendations

## Best Practices

- Always start with the freedom level decision — it shapes the entire skill structure
- Error prevention patterns are the highest-value design element — spend time identifying real mistakes
- Token budget should match the target audience — compact for experts, detailed for complex or unfamiliar domains
- Memory structure should track both patterns (what works) and history (what was done)
- Validate generated skills against SKILL_TEMPLATE.md structure before finalizing
- Examples should cover the full range of the skill's capabilities, not just the happy path
