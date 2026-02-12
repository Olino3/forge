# ⚒️ The Forge — Roadmap

> *"Hephaestus's forge never cools. Each skill sharpened, each agent awakened, each command invoked brings us closer to the perfect workshop — where mortal developers wield divine tools."*

---

## The Factory Today

The Forge is a fully operational **Agentic Software Factory** — a Claude Code plugin built on convention, powered by 4 core interfaces, and staffed by a pantheon of divine agents.

## Future Work

> *"The blueprints are drawn — these weapons await their turn at the anvil."*

### Planned Skills

| Skill | Category | Description |
|-------|----------|-------------|
| **neon-vercel-postgres** | Database & Storage | Set up serverless Postgres with Neon or Vercel Postgres for Cloudflare Workers/Edge. Includes connection pooling, git-like branching, and Drizzle ORM integration |
| **vercel-blob** | Database & Storage | Integrate Vercel Blob for file uploads and CDN-delivered assets in Next.js. Supports client-side uploads with presigned URLs and multipart transfers |
| **vercel-kv** | Database & Storage | Integrate Redis-compatible Vercel KV for caching, session management, and rate limiting in Next.js |

---

### Planned Commands

| Command | Description |
|---------|-------------|
| **/divine** | Analyze the codebase and suggest possible workflows and cookbooks with commands, skills, and agents from the forge-plugin. Recommends strategies and techniques to integrate agentic coding into the codebase using The Forge plugin. Entry point for discovering optimal forge patterns for your specific project. |

---

### Planned Hooks

#### Memory & Context Management (User-Triggered)

| Hook Event | Description |
|------------|-------------|
| **on_user_prompt** | Load relevant memory and context when user initiates a prompt, ensuring the agent has access to prior learnings and project-specific knowledge |
| **on_skill_use** | Store insights, patterns, and outcomes when skills are invoked, building a knowledge base of what works in this project |

#### External Plugin Integration

| Hook Event | Description |
|------------|-------------|
| **on_external_skill_load** | Integrate Forge's memory and context management for skills from other Claude Code plugins, enabling unified knowledge sharing |
| **on_external_skill_complete** | Capture and store learnings from external plugin skills into Forge's memory system for future reference |

#### Plugin Security Hooks

| Hook Event | Description |
|------------|-------------|
| **on_plugin_install** | Validate plugin integrity, verify checksums, and scan for known malicious patterns before allowing installation |
| **on_skill_output** | Inspect skill outputs for prompt injection artifacts, sensitive data leakage, and unexpected tool calls before returning results |
| **on_external_skill_load** (security layer) | Enforce allowlists for external plugin sources, validate symlink targets, and check plugin signatures against trusted registries |
| **on_submodule_update** | Scan updated submodule contents for supply chain risks — new dependencies, modified entry points, or altered plugin manifests |
| **on_context_injection** | Detect and sanitize context payloads that may contain prompt injection attempts or adversarial instructions embedded in data files |

---

## Agentic Workflows — Continuous Quality (Detailed Roadmap)

> *"The tireless automatons of Hephaestus's workshop never sleep — they sweep the forge floor, sharpen every blade, and polish each shield while the gods rest."*

A detailed, phased roadmap for implementing Continuous Quality Workflows using [GitHub Agentic Workflows (gh-aw)](https://github.github.com/gh-aw/) is maintained in **[AGENTIC_WORKFLOWS_ROADMAP.md](AGENTIC_WORKFLOWS_ROADMAP.md)**.

The plan covers 7 phases across 10 workflows:

| Phase | Workflows | Parallelizable |
|-------|-----------|----------------|
| **Phase 0** — Bootstrap | gh-aw init, shared imports, forge conventions | No (prerequisite) |
| **Phase 1A** — Continuous Simplicity | Skill Simplifier, Duplication Detector | Yes (with 1B) |
| **Phase 1B** — Continuous Context | Context Generator (on skill add), Context Pruner | Yes (with 1A) |
| **Phase 2A** — Continuous Refactoring | Skill Structure Validator, Agent Config Validator | Yes (with 2B) |
| **Phase 2B** — Continuous Style | Convention Enforcer, Hook Quality Checker | Yes (with 2A) |
| **Phase 3** — Continuous Improvement | Health Dashboard, Cross-Reference Checker, Best Practices Improver | After 1A+1B |
| **Phase 4** — Continuous Documentation | Doc Sync, Doc Unbloat | Yes (with Phase 3) |

All workflows use the **Copilot engine** and leverage gh-aw's quick-start examples from [Peli's Agent Factory](https://github.github.com/gh-aw/blog/2026-01-12-welcome-to-pelis-agent-factory/), customized for Forge's Markdown/JSON/Bash codebase.

---

## CI/CD Validation & Plugin Discovery

> *"The forge's gates must be tested — every hammer strike verified, every blade inspected before it leaves the anvil."*

### GitHub Actions — Claude Code Validation

| Workflow | Description |
|----------|-------------|
| **validate-skills** | Run Claude Code skill discovery commands in CI to confirm all 102 core skills are resolvable and have valid `SKILL.md` files |
| **validate-plugins** | Automated plugin discovery tests that confirm all 38 marketplace plugins are properly installed, symlinks resolve, and plugin.json manifests are valid |
| **validate-agents** | Verify all 19 agent `.config.json` files conform to `agent_config.schema.json` and memory directories exist |
| **validate-hooks** | Execute hook scripts in dry-run mode to ensure they complete within the 5-second budget and exit cleanly |
| **validate-external-submodules** | Confirm all git submodules are checked out, symlinks point to valid targets, and external skill directories contain expected files |

### Automated Plugin Discovery Tests

| Test | Description |
|------|-------------|
| **plugin-install-smoke** | Install each marketplace plugin in an isolated environment and verify skill resolution succeeds |
| **symlink-integrity** | Walk all symlinks in wrapper plugin directories and confirm targets exist and are readable |
| **marketplace-schema** | Validate `marketplace.json` against a JSON schema — required fields, valid source paths, no duplicate names |
| **cross-platform-paths** | Verify plugin paths resolve correctly on Linux, macOS, and Windows (WSL) environments |

---

## Layer 3 Security Testing

> *"The deepest fires reveal hidden flaws — what survives the crucible is truly worthy."*

A dedicated security testing layer that goes beyond unit and integration tests to address adversarial threats specific to agentic plugin systems.

### Prompt Injection Defense

| Test | Description |
|------|-------------|
| **skill-injection-scan** | Scan all `SKILL.md` files and context files for patterns that could hijack agent instructions — embedded system prompts, role overrides, instruction-ignoring directives |
| **context-poisoning-test** | Verify that user-supplied memory files cannot inject instructions that alter agent behavior beyond their intended scope |
| **output-sanitization** | Ensure skill outputs passed between chained commands are sanitized — no embedded tool calls, escalation attempts, or data exfiltration patterns |
| **indirect-injection-via-data** | Test that data files (CSV, JSON, YAML) processed by skills cannot contain embedded prompt injections that execute during analysis |

### Plugin Security Risks

| Test | Description |
|------|-------------|
| **permission-scope-audit** | Verify each plugin only accesses files and tools declared in its manifest — no scope creep beyond declared `contextDomains` and `skills` |
| **plugin-isolation-test** | Confirm plugins cannot read or modify other plugins' memory, context, or configuration files |
| **manifest-tampering-detect** | Detect unauthorized modifications to `plugin.json`, `marketplace.json`, or `hooks.json` between commits |
| **mcp-server-trust-boundary** | Validate that MCP server integrations cannot escalate permissions or access resources beyond their declared scope |

### Supply Chain Security

| Test | Description |
|------|-------------|
| **submodule-provenance** | Verify all git submodules point to forks under `Olino3/` — no direct references to upstream repos that could be compromised |
| **dependency-drift-detect** | Compare submodule commit SHAs against a pinned manifest and alert on unexpected changes |
| **skill-content-hash** | Maintain a hash manifest of all external skill files; detect unauthorized content modifications after submodule syncs |
| **typosquat-detection** | Scan plugin names and skill names for potential typosquatting of known popular packages or skills |
| **license-compliance** | Automated license scanning of all external plugins to ensure compatibility with The Forge's license |

---

## Modular Core — Plugin Decomposition

> *"A smith does not carry every tool to every job — only the weapons the battle demands."*

Break `forge-core` into focused plugin modules so users install only the skills they need. The 12 Olympian agents and 7 specialist agents remain in the core plugin as the foundation.

### Proposed Plugin Split

| Plugin | Contents | Est. Skills |
|--------|----------|-------------|
| **forge-core** (always installed) | 19 agents, 12 commands, 4 interfaces, context, memory, hooks | Core framework |
| **forge-skills-frontend** | accessibility, animate, nextjs, react-forms, responsive-images, tailwind-patterns, angular-architect, flutter-expert, react-expert, react-native-expert, vue-expert, vue-expert-js | 12 |
| **forge-skills-backend** | django, dotnet-core, fastapi, nestjs, rails, php | 6 |
| **forge-skills-languages** | cpp, csharp, java-architect, javascript, typescript | 5 |
| **forge-skills-cloud** | cloud-architect, devops-engineer, kubernetes-specialist, sre-engineer, terraform-engineer | 5 |
| **forge-skills-data** | database-optimizer, pandas, postgres, sql, firebase-firestore, firebase-storage, snowflake-platform | 7 |
| **forge-skills-security** | secure-code, security-reviewer, code-documenter, code-reviewer, debugging-expert, testing | 6 |
| **forge-skills-auth** | azure-auth, better-auth, clerk-auth, firebase-auth, oauth-integrations | 5 |
| **forge-skills-azure** | generate-azure-functions, generate-azure-pipelines, generate-azure-bicep, generate-tilt-dev-environment | 4 |
| **forge-skills-planning** | divine, docs-workflow, project-health, project-planning, project-session-management, project-workflow, skill-creator, skill-review, sub-agent-patterns | 9 |
| **forge-skills-utilities** | color-palette, email-gateway, favicon-gen, firecrawl-scraper, icon-design, image-gen, jquery-4, office, open-source-contributions, playwright-local | 10 |
| **forge-skills-review** | python-code-review, dotnet-code-review, angular-code-review, get-git-diff | 4 |
| **forge-skills-codegen** | generate-python-unit-tests, generate-jest-unit-tests, generate-mock-service, generate-more-skills-with-claude, test-cli-tools | 5 |
| **forge-skills-productivity** | commit-helper, email-writer, slack-message-composer, documentation-generator, excel-skills, jupyter-notebook-skills | 6 |
| **forge-skills-specialized** | cli-developer, feature-forge, fullstack-development, legacy-modernizer, mcp-developer, monitoring-expert, prompt-engineer, websocket-engineer, create-agents, power-debug, dev-tools | 11 |
| **forge-skills-architecture** | api-design, architecture-design, graphql-design, microservices-design | 4 |
| **forge-skills-analysis** | file-schema-analysis, database-schema-analysis, python-dependency-management | 3 |

### Migration Strategy

1. Add a `forge-skills-all` meta-plugin that installs everything (backward-compatible default)
2. Publish individual skill plugins to the marketplace
3. Update `marketplace.json` with the new plugin entries
4. Deprecate monolithic `forge-core` skills directory over 2 releases
5. Core agents continue to reference skills by name — the resolution layer handles which plugin provides them

---

## Agent Skill & MCP Scoping

> *"Each god wields only the weapons befitting their divine domain."*

Give custom agents explicit access to specific skills and MCP servers based on their focus area, rather than exposing the full skill catalog to every agent.

### Scoping Model

| Agent | Scoped Skills | Scoped MCPs |
|-------|--------------|-------------|
| **@python-engineer** | fastapi, django, pandas, python-code-review, generate-python-unit-tests, python-dependency-management | Context7 (Python docs), GitHub |
| **@frontend-engineer** | nextjs, react-forms, tailwind-patterns, accessibility, animate, responsive-images, generate-jest-unit-tests | Context7 (React/Next docs), Playwright |
| **@devops-engineer** | cloud-architect, kubernetes-specialist, terraform-engineer, sre-engineer, generate-azure-pipelines | Azure MCP, GitHub |
| **@data-scientist** | pandas, sql, postgres, database-optimizer, jupyter-notebook-skills, excel-skills | Context7 (data libs), Filesystem |
| **@security-reviewer** | secure-code, security-reviewer, code-reviewer + Trail of Bits plugins | GitHub (security advisories) |

### Implementation

- Extend `agent_config.schema.json` with `allowedSkills[]` and `allowedMcps[]` fields
- `SkillInvoker` checks agent scope before delegating — returns a helpful error if a skill is out-of-scope
- Agents can request scope escalation via `@zeus` (orchestrator pattern)
- Default scope: all skills (backward-compatible) — scoping is opt-in per agent config

---

## Agentic Workflows — GitHub Actions Integration

> *"The forge runs day and night — tireless agents keeping the workshop in perfect order."*

Inspired by [Peli's Agent Factory](https://github.github.com/gh-aw/blog/2026-01-12-welcome-to-pelis-agent-factory/) (GitHub Next + Microsoft Research), implement automated agentic workflows as GitHub Actions that run continuously alongside development. Each workflow is a specialized agent defined in Markdown, compiled into secure GitHub Actions with scoped permissions and guardrails.

### Continuous Quality Workflows

| Workflow | Description | Trigger | Reference |
|----------|-------------|---------|----------|
| **Continuous Simplicity** | Proactively identify and propose simplification PRs — remove dead code, flatten abstractions, reduce complexity scores | Schedule (daily) + on PR merge | [Peli's Continuous Simplicity](https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-continuous-simplicity/) |
| **Continuous Refactoring** | Detect code smells, duplication, and anti-patterns; propose targeted refactoring PRs with before/after metrics | Schedule (daily) | [Peli's Continuous Refactoring](https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-continuous-refactoring/) |
| **Continuous Style** | Enforce coding conventions, naming standards, and project-specific patterns beyond what linters catch | On PR + schedule (weekly) | [Peli's Continuous Style](https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-continuous-style/) |
| **Continuous Improvement** | Analyze merged PRs for optimization opportunities — performance, bundle size, query efficiency | On PR merge | [Peli's Continuous Improvement](https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-continuous-improvement/) |
| **Continuous Documentation** | Keep README, API docs, and inline comments in sync with code changes; flag stale documentation | On PR merge + schedule (weekly) | [Peli's Continuous Documentation](https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-documentation/) |

### Testing & Validation Workflows

| Workflow | Description | Trigger | Reference |
|----------|-------------|---------|----------|
| **Improve Test Coverage** | Analyze coverage gaps, generate missing unit/integration tests, submit as PRs | Schedule (weekly) | [Peli's Testing & Validation](https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-testing-validation/) |
| **Diagnose CI Failures** | On CI failure, automatically investigate root cause — parse logs, identify flaky tests, bisect regressions, post diagnosis as PR comment | On CI failure | [Peli's Fault Investigation](https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-quality-hygiene/) |

### Operations & Release Workflows

| Workflow | Description | Trigger | Reference |
|----------|-------------|---------|----------|
| **Release Notes Generator** | Compile changelog from merged PRs, categorize by type (feature/fix/breaking), draft release notes | On tag/release | [Peli's Operations & Release](https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-operations-release/) |
| **Dependency Update Sentinel** | Monitor dependencies for security advisories and updates, propose upgrade PRs with compatibility analysis | Schedule (daily) | [Peli's Operations & Release](https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-operations-release/) |
| **Health Dashboard** | Generate weekly repository health reports — test coverage trends, issue velocity, PR cycle time, code quality metrics | Schedule (weekly) | [Peli's Metrics & Analytics](https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-metrics-analytics/) |

### Planning & Coordination Workflows

| Workflow | Description | Trigger | Reference |
|----------|-------------|---------|----------|
| **Issue Triage Agent** | Auto-label, prioritize, and assign incoming issues based on content analysis and project context | On issue creation | [Peli's Issue Management](https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-issue-management/) |
| **Project Milestone Tracker** | Monitor progress toward milestones, identify blocked issues, suggest re-prioritization | Schedule (daily) | [Peli's Project Coordination](https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-campaigns/) |
| **Stale Issue/PR Gardener** | Identify stale issues and PRs, ping assignees, auto-close after grace period with summary comment | Schedule (weekly) | [Peli's Issue Management](https://github.github.com/gh-aw/blog/2026-01-13-meet-the-workflows-issue-management/) |


### Implementation Plan

1. Define each workflow as a Markdown specification in `.github/workflows/agents/`
2. Compile Markdown specs into GitHub Actions YAML with scoped permissions (read-only by default, write for PR-creating workflows)
3. Use Forge skills as the execution engine — each workflow delegates to relevant skills
4. Implement guardrails: max changes per PR, human-approval gates for destructive operations, cost budgets per run
5. Add meta-agent that monitors workflow health, tracks costs, and adjusts schedules based on value delivered

---

## Multi-Platform Compatibility

> *"A weapon forged by Hephaestus serves any warrior who wields it — not just the one who commissioned it."*

Extend skill and agent compatibility beyond Claude Code to support additional AI-assisted development platforms.

### Target Platforms

| Platform | Skill Format | Agent Format | Status |
|----------|-------------|-------------|--------|
| **Claude Code** | `SKILL.md` (native) | `.md` + `.config.json` (native) | ✅ Current |
| **GitHub Copilot CLI** | `.instructions.md` / `.github/copilot-instructions.md` | Custom instructions | 🔲 Planned |
| **Gemini CLI** | `AGENTS.md` + skill files | Agent config files | 🔲 Planned |
| **Factory** (GitHub Agentic Workflows) | Markdown workflow specs → GitHub Actions YAML | Workflow-scoped agents | 🔲 Planned |
| **Cursor** | `.cursor/rules/` rule files | Cursor agent rules | 🔲 Planned |
| **Codex** (OpenAI) | `AGENTS.md` + instruction files | Agent spec files | 🔲 Planned |

### Compatibility Strategy

1. **Universal Skill Format**: Define a platform-agnostic skill schema that captures intent, context, and examples — then transpile to each platform's native format
2. **Adapter Layer**: Build platform adapters in `interfaces/adapters/` that translate Forge's `SkillInvoker` and `ContextProvider` interfaces into platform-specific conventions
3. **Agent Config Transpiler**: Convert `agent_config.schema.json` into platform-native agent definitions (Cursor rules, Gemini agents, Copilot instructions)
4. **Shared Context**: Context files (`forge-plugin/context/`) are Markdown with YAML frontmatter — already compatible with most platforms. Ensure `tags` and `sections` metadata maps to each platform's discovery mechanism
5. **Test Matrix**: CI validates that transpiled outputs are well-formed for each target platform

### Deliverables

| Deliverable | Description |
|-------------|-------------|
| `forge-export-copilot` | Transpile Forge skills into GitHub Copilot `.instructions.md` files |
| `forge-export-gemini` | Generate Gemini CLI-compatible `AGENTS.md` and skill files |
| `forge-export-cursor` | Convert Forge skills into Cursor `.cursor/rules/` rule files |
| `forge-export-factory` | Compile Forge workflow recipes into GitHub Actions YAML via Factory patterns |
| `forge-export-codex` | Generate OpenAI Codex-compatible agent and instruction files |
| `forge-compat-tests` | Cross-platform test suite verifying transpiled outputs work on each target platform |

---

## Long-Term Vision

> *"The ultimate forge needs no smith — it reads the blueprint and shapes the metal itself."*

### Near-Term
- **Modular core decomposition**: Break forge-core into 16 focused skill plugins (see above)
- **Agent skill scoping**: Agents access only domain-relevant skills and MCPs
- **CI/CD validation**: GitHub Actions workflows for skill, plugin, agent, and hook validation
- **Layer 3 security testing**: Prompt injection defense, plugin isolation, supply chain verification
- **Plugin security hooks**: 5 new hooks for install-time, runtime, and update-time security checks
- **Multi-platform transpilers**: Export Forge skills to Copilot CLI, Gemini CLI, Cursor, Codex, and Factory formats

### Mid-Term
- **Agentic GitHub workflows**: 13 automated workflows inspired by Peli's Factory — continuous simplicity, refactoring, style, improvement, documentation, CI diagnosis, test coverage, release automation, issue triage, and project coordination
- **Advanced Olympian Council workflows**: All 12 Olympians actively collaborating on complex engineering challenges with sophisticated delegation patterns
- **Self-improving skills**: Skills that analyze their own output quality and refine themselves
- **Meta-agents**: Agents that monitor and improve the health of other agents and workflows
- **Cross-project learning**: Insights from one project improving analysis of similar projects
- **Divine delegation patterns**: Zeus orchestrating multi-agent workflows with strategic task distribution
- **New skill domains**: Go, Rust, Swift code review and generation

### Long-Term
- **Fully autonomous forge**: Agents self-organize to solve complex engineering challenges end-to-end
- **Predictive engineering**: The Factory anticipates needs before they're articulated
- **Multi-forge federation**: Multiple Forge instances sharing knowledge across organizations
- **Autonomous memory curation**: Memory that self-organizes, merges, and prunes without intervention
- **Community marketplace**: Public plugin registry for community-contributed skills and agents

---

## Forge Chronicle

Current state and recent milestones:

| Date | Milestone |
|------|-----------|
| **Feb 13, 2026** | Documentation Overhaul — All planned internal skills forged (102 core skills), Forge Marketplace documented (38 plugins, 212 external skills), COOKBOOK.md created |
| **Feb 12, 2026** | Architecture & Design Skills — Forged 4 skills (api-design, architecture-design, graphql-design, microservices-design) with 100 tests |
| **Feb 12, 2026** | Frontend & Mobile Skills — 6 new skills forged: angular-architect, flutter-expert, react-expert, react-native-expert, vue-expert-js, vue-expert |
| **Feb 12, 2026** | Frontend & UI Skills — Forged 6 skills: accessibility, animate, nextjs, react-forms, responsive-images, tailwind-patterns |
| **Feb 12, 2026** | Utilities Forged — 10 Utilities skills implemented: color-palette, email-gateway, favicon-gen, firecrawl-scraper, icon-design, image-gen, jquery-4, office, open-source-contributions, playwright-local |
| **Feb 12, 2026** | Database & Storage Skills — Forged firebase-firestore, firebase-storage, snowflake-platform (3 new skills, 25 total) |
| **Feb 12, 2026** | Roadmap Expansion — Added `/divine` command and 4 new hook events for memory/context integration |
| **Feb 12, 2026** | Factory Stable — 22 skills, 12 commands, 11 agents, 81 context files, 20 hooks, ~1,683 tests |
| **Feb 11, 2026** | Enterprise Skills Catalog — Documented 173 skills from Vercel, Google Labs, Trail of Bits, Microsoft, Anthropic, Sentry |
| **Feb 11, 2026** | Community Skills Catalog — Documented 99+ planned skills across 15 domains |
| **Feb 10, 2026** | MCP Integration — 8 external knowledge conduits connected |
| **Nov 18, 2025** | Azure Functions — generate-azure-functions with Tilt + Azurite |
| **Nov 14, 2025** | .NET Code Review — dotnet-code-review with 12 context files |

---

*Last Updated: February 13, 2026*
*Maintained by: The Forge Keepers*

*Forged by Hephaestus. Tempered by experience. Worthy of Olympus.*
