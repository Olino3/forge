# ⚒️ The Forge ⚒️

> *"As Hephaestus crafted divine weapons for the gods, so too does the Forge craft tools for mortal developers."*

<div align="center">

🔥 **An Agentic Software Factory for Claude Code** 🔥

*Where divine agents, battle-tested skills, and structured commands transform code into artifacts worthy of Mount Olympus*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Forged in Shell](https://img.shields.io/badge/Forged_in-Shell-success?style=for-the-badge&logo=gnu-bash)](https://github.com/Olino3/forge)
[![Agents](https://img.shields.io/badge/Agents-19-blue?style=for-the-badge)](forge-plugin/agents/)
[![Core Skills](https://img.shields.io/badge/Core_Skills-102-orange?style=for-the-badge)](forge-plugin/skills/)
[![External Skills](https://img.shields.io/badge/External_Skills-212-blueviolet?style=for-the-badge)](ROADMAP.md)
[![Plugins](https://img.shields.io/badge/Plugins-38-purple?style=for-the-badge)](.claude-plugin/marketplace.json)
[![Hooks](https://img.shields.io/badge/Hooks-20-red?style=for-the-badge)](forge-plugin/hooks/)

</div>

---

## What Is The Forge?

The Forge is not a plugin collection — it is a complete **Agentic Software Factory** that extends [Claude Code](https://claude.ai/code) with an entire engineering workshop. Built on pure convention (no build tools, no package managers, no compiled code), the Forge provides:

| Component | Count | What It Does |
|-----------|-------|-------------|
| 🏛️ **Agents** | 19 | AI personas with deep domain expertise (12 Olympian + 7 specialist) |
| 🔨 **Core Skills** | 102 | Built-in capabilities — code review, infrastructure, frontend, backend, security, cloud, and more |
| 🌐 **External Skills** | 212 | Enterprise skills from Microsoft (133), Trail of Bits (53), Sentry (15), Google Labs (6), Vercel (5) |
| 🧩 **Marketplace Plugins** | 38 | Modular plugin system for selective skill loading via the Forge Marketplace |
| ⚡ **Commands** | 12 | Structured workflows — `/analyze`, `/implement`, `/test`, and more |
| 📚 **Context** | 81 files | Shared knowledge across 9 domains with YAML frontmatter |
| 🧠 **Memory** | 4 layers | Project-specific learning that grows with every invocation |
| 🪝 **Hooks** | 20 | Automated security, quality gates, and integrity enforcement |
| 🔌 **MCP Servers** | 8 | External knowledge conduits (docs, browser, search, code intel) |
| ⚙️ **Interfaces** | 4 | Abstract contracts decoupling all components from the filesystem |
| 🧪 **Tests** | ~1,993 | Layered test suite — static validation, hook integration, E2E |

---

## Quick Start

### Clone with Dependencies

The Forge uses git submodules for external skill repositories. Clone with all dependencies:

```bash
# Clone with all submodules (RECOMMENDED)
git clone --recursive https://github.com/Olino3/forge.git
cd forge

# Run setup script (initializes submodules, verifies symlinks, validates plugins)
./scripts/setup.sh
```

### Already Cloned Without `--recursive`?

If you cloned without `--recursive`, you can initialize dependencies with one command:

```bash
# One command fixes everything
./scripts/setup.sh
```

This will:
- ✅ Initialize all git submodules (5 external repositories)
- ✅ Verify 260 symlinks are healthy
- ✅ Fix broken symlinks if found
- ✅ Validate all plugins

### Troubleshooting Setup

**Broken symlinks?** `./scripts/fix-symlinks.sh`  
**Plugins not loading?** `./scripts/validate-plugins.sh`  
**Submodule issues?** `git submodule update --init --recursive --force`

See [SETUP.md](SETUP.md) for detailed setup instructions or [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues.

---

### Install the Forge

```bash
# Add The Forge as a Claude Code plugin
/plugin install forge-plugin@Olino3/forge
```

### Verify Installation

```bash
# Check available commands
/help
```

### Start Using It

```bash
# Analyze your codebase
/analyze src/ --focus security

# Implement a feature with tests
/implement "Add user authentication" --tests

# Review Python code
skill:python-code-review src/auth/

# Summon a specialist agent
@python-engineer Review this FastAPI service for performance issues
```

---

## 🏛️ The Pantheon — 19 Agents

Agents are AI personas with deep domain expertise, persistent memory, and curated skill sets.

### Divine Council (Olympian Tier)

| Agent | Domain | Specialization |
|-------|--------|---------------|
| **@zeus** | Orchestration & Leadership | Multi-agent workflows, task delegation, factory oversight |
| **@hera** | Project Management | Lifecycle management, standards enforcement, architectural coherence |
| **@athena** | Wisdom & Architecture | System architecture, technical decisions, strategic counsel |
| **@apollo** | Code Quality | Quality analysis, performance optimization, algorithm refinement |
| **@artemis** | Testing & QA | Bug tracking, test strategy design, code integrity assurance |
| **@aphrodite** | UX/UI & Design | User experience design, interface elegance, visual harmony |
| **@hermes** | Integration | API integrations, inter-service communication, data exchange |
| **@demeter** | Data Cultivation | Data pipelines, analytics, data quality and growth |
| **@hephaestus** | Tool Creation | Forges new skills, templates, and meta-capabilities |
| **@prometheus** | Strategy | Architecture design, roadmaps, ADRs, tech evaluation |
| **@ares** | Deployment | Production deployment, incident response, monitoring |
| **@poseidon** | Data Flow | ETL pipelines, event-driven architecture, data integration |

### Specialist Legion

| Agent | Domain | Specialization |
|-------|--------|---------------|
| **@python-engineer** | Python | Django, Flask, FastAPI, testing, dependency management |
| **@frontend-engineer** | Frontend | Angular, TypeScript, RxJS, NgRx, accessibility |
| **@devops-engineer** | Infrastructure | Azure Pipelines, Docker, Kubernetes, CI/CD |
| **@developer-environment-engineer** | Tooling | Tilt, Docker Compose, local dev environments |
| **@data-scientist** | Analytics | Notebooks, pandas, ML, statistical analysis, visualization |
| **@full-stack-engineer** | End-to-End | API design, frontend-backend integration, system architecture |
| **@technical-writer** | Documentation | API docs, user guides, technical specifications |

Each agent maintains project-specific memory, so they become more effective over time.

---

## 🔨 The Armory — 102 Core Skills

Skills are deep, specialized capabilities invoked via `skill:{name}` syntax.

| Category | Skills |
|----------|--------|
| **Frontend & UI** (6) | `accessibility` · `animate` · `nextjs` · `react-forms` · `responsive-images` · `tailwind-patterns` |
| **Frontend & Mobile** (6) | `angular-architect` · `flutter-expert` · `react-expert` · `react-native-expert` · `vue-expert` · `vue-expert-js` |
| **Authentication** (5) | `azure-auth` · `better-auth` · `clerk-auth` · `firebase-auth` · `oauth-integrations` |
| **Backend & Frameworks** (6) | `django` · `dotnet-core` · `fastapi` · `nestjs` · `rails` · `php` |
| **Architecture & Design** (4) | `api-design` · `architecture-design` · `graphql-design` · `microservices-design` |
| **Cloud & Infrastructure** (5) | `cloud-architect` · `devops-engineer` · `kubernetes-specialist` · `sre-engineer` · `terraform-engineer` |
| **Programming Languages** (5) | `cpp` · `csharp` · `java-architect` · `javascript` · `typescript` |
| **Data & Database** (6) | `database-optimizer` · `database-schema-analysis` · `pandas` · `postgres` · `snowflake-platform` · `sql` |
| **Database & Storage** (2) | `firebase-firestore` · `firebase-storage` |
| **Quality & Security** (6) | `code-documenter` · `code-reviewer` · `debugging-expert` · `secure-code` · `security-reviewer` · `testing` |
| **Code Review** (4) | `python-code-review` · `dotnet-code-review` · `angular-code-review` · `get-git-diff` |
| **Test Generation** (3) | `generate-python-unit-tests` · `generate-jest-unit-tests` · `test-cli-tools` |
| **Infrastructure** (5) | `generate-azure-functions` · `generate-azure-pipelines` · `generate-azure-bicep` · `generate-tilt-dev-environment` · `generate-mock-service` |
| **Planning & Workflow** (9) | `divine` · `docs-workflow` · `project-health` · `project-planning` · `project-session-management` · `project-workflow` · `skill-creator` · `skill-review` · `sub-agent-patterns` |
| **Developer Workflow** (3) | `create-agents` · `dev-tools` · `power-debug` |
| **Specialized** (8) | `cli-developer` · `feature-forge` · `fullstack-development` · `legacy-modernizer` · `mcp-developer` · `monitoring-expert` · `prompt-engineer` · `websocket-engineer` |
| **Productivity** (5) | `commit-helper` · `documentation-generator` · `email-writer` · `email-gateway` · `slack-message-composer` |
| **Utilities** (10) | `color-palette` · `favicon-gen` · `firecrawl-scraper` · `icon-design` · `image-gen` · `jquery-4` · `office` · `open-source-contributions` · `playwright-local` |
| **Analysis** (2) | `file-schema-analysis` · `python-dependency-management` |
| **Data Science** (2) | `excel-skills` · `jupyter-notebook-skills` |
| **Meta** (1) | `generate-more-skills-with-claude` |

> 💡 **102 core skills** are built into the Forge. An additional **212 external skills** are available via the Forge Marketplace — see [External Skills & Modular Loading](#-external-skills--modular-loading) below.

---

## 🌐 External Skills & Modular Loading

> *"Select only the weapons you need — a bloated armory slows the warrior."*

The **Forge Marketplace** provides **212 additional external skills** from enterprise and community sources, loaded as modular plugins. Users should select skills based on their specific use case to prevent memory/token bloat.

### External Skill Sources

| Source | Skills | Plugins | Integration Pattern |
|--------|--------|---------|--------------------|
| **Microsoft** | 133 | 7 | Multi-Plugin Wrapper — per-language separation (Python, .NET, TypeScript, Java, Rust, Core, Agents) |
| **Trail of Bits** | 53 | 27 | Native Plugin — each skill is its own plugin, imported directly from submodule |
| **Sentry** | 15 | 1 | Native Plugin — direct source path reference |
| **Google Labs** | 6 | 1 | Single Plugin Wrapper — one symlink to skills directory |
| **Vercel** | 5 | 1 | Single Plugin Wrapper — one symlink to skills directory |

### How External Skills Work

1. **Stability Forks**: All external repos are forked under `Olino3/` to insulate the Forge from upstream breaking changes
2. **Git Submodules**: Forks are mounted as submodules in `.gitmodules` (see `microsoft/skills`, `vercel/agent-skills`, etc.)
3. **Plugin Wrappers**: Wrapper directories create `skills/` symlinks pointing into submodules, exposing them as standard Claude Code plugins
4. **Forge Marketplace**: All plugins are registered in `.claude-plugin/marketplace.json` for unified installation

### Installation Examples

```bash
# Install by use case — don't install everything!
/plugin install forge-core@forge-marketplace              # Always install this first

# Python developer
/plugin install ms-skills-python@forge-marketplace
/plugin install modern-python@forge-marketplace

# Security researcher
/plugin install sharp-edges@forge-marketplace
/plugin install static-analysis@forge-marketplace
/plugin install differential-review@forge-marketplace

# React developer
/plugin install vercel-skills@forge-marketplace
/plugin install stitch-skills@forge-marketplace
```

See [COOKBOOK.md](COOKBOOK.md) for persona-based selection guides and workflow recipes.

---

## ⚡ The War Room — 12 Commands

Commands are structured workflows that orchestrate skills, context, and memory.

```bash
/analyze     # Code analysis and quality assessment
/implement   # Feature implementation with tests
/improve     # Code refactoring and improvement
/document    # Documentation generation
/test        # Test execution and validation
/build       # Project building and packaging
/brainstorm  # Requirements discovery (Socratic method)
/remember    # Project memory management
/mock        # Mock service generation
/azure-pipeline  # Azure CI/CD orchestration
/etl-pipeline    # Data transformation pipelines
/azure-function  # Serverless Azure Functions
```

Commands can be **chained**: `/analyze` → `/improve` → `/test` with `ExecutionContext` carrying results between them.

---

## 🪝 The Anvil — 20 Automated Hooks

The Forge's nervous system — organized into 4 thematic layers, enforcing security, quality, and integrity automatically.

| Layer | Hooks | Purpose |
|-------|-------|---------|
| 🛡️ **Shield** | 5 | Security & initialization — sandbox boundaries, dependency scanning, PII redaction, git hygiene |
| 📜 **Chronicle** | 4 | Memory & learning — freshness enforcement, cross-pollination, quality gates, session-end pruning |
| 👷 **Foreman** | 8 | Workflow & quality — skill compliance, frontmatter validation, context drift detection, output scoring |
| 📢 **Town Crier** | 3 | Telemetry & reporting — health aggregation, session stats, context usage tracking |

All hooks fire automatically across 9 Claude Code event types. No manual intervention needed.

---

## ⚙️ Architecture

The Forge uses an **interface-driven architecture** with 4 core abstractions:

```
┌──────────────────────────────────────────────────────┐
│  🛡️ SHIELD        📜 CHRONICLE      👷 FOREMAN       │
│  Security          Memory            Workflow         │
│  (5 hooks)         (4 hooks)         (8 hooks)        │
├──────────────────────────────────────────────────────┤
│  📢 TOWN CRIER — Telemetry (3 hooks)                 │
├──────────────────────────────────────────────────────┤
│              ⚙️ INTERFACE LAYER                       │
│  ContextProvider · MemoryStore · SkillInvoker         │
│              ExecutionContext                         │
├──────────────────────────────────────────────────────┤
│  🏛️ PANTHEON    🔨 ARMORY     ⚡ WAR ROOM            │
│  19 Agents     102 Skills     12 Commands            │
├──────────────────────────────────────────────────────┤
│  🌐 FORGE MARKETPLACE (38 plugins · 212 external)     │
├──────────────────────────────────────────────────────┤
│  📚 ARCHIVE (81 files) · 🧠 MEMORY (4 layers)        │
│  🔌 CONDUITS (8 MCP servers)                         │
└──────────────────────────────────────────────────────┘
```

| Interface | Purpose |
|-----------|---------|
| **ContextProvider** | Load shared knowledge by domain, tags, and sections |
| **MemoryStore** | Read/write project memory with automated lifecycle |
| **SkillInvoker** | Delegate to skills with structured I/O |
| **ExecutionContext** | Pass context between chained commands |

All components reference interfaces — never hardcoded filesystem paths. See [ARCHITECTURAL_ROADMAP.md](ARCHITECTURAL_ROADMAP.md) for the full technical design.

---

## 🔌 MCP Integrations

8 external knowledge servers extend the Forge's reach:

| Server | Purpose | Requires Key? |
|--------|---------|:---:|
| **sequential-thinking** | Step-by-step reasoning | No |
| **context7** | Library documentation | No |
| **playwright** | Browser automation & E2E testing | No |
| **serena** | Code intelligence & navigation | No |
| **chrome-devtools** | Chrome DevTools Protocol | No |
| **magic** | UI component generation | Yes |
| **morphllm-fast-apply** | Fast code transformations | Yes |
| **tavily** | Web search & research | Yes (free tier) |

---

## 🧪 Testing

The Forge has a layered test suite (~1,993 total checks) validating structure, schemas, hook behavior, memory lifecycle, and context loading — using only bash, python3, jq, and optionally shellcheck.

| Layer | What It Covers | Count |
|-------|---------------|-------|
| **Layer 1** (Static/CI) | JSON schemas, file structure, YAML frontmatter, cross-references, hook syntax | ~1,225 pytest + 96 bash |
| **Layer 2** (Integration) | 20 hook I/O contracts, memory lifecycle, context loading protocol | ~504 pytest |
| **E2E** | Plugin loading, command registration, skill discovery | ~168 bash |

```bash
# From forge-plugin/
bash tests/run_all.sh           # Layer 1 only
bash tests/run_all.sh --layer2  # Layer 1 + Layer 2
bash tests/run_all.sh --e2e     # Everything
```

CI runs automatically via GitHub Actions on every push/PR.

---

## 📁 Project Structure

```
forge/
├── CLAUDE.md                    # The Forge Operating Manual (for Claude Code)
├── COOKBOOK.md                   # Strategies, workflows, and persona guides
├── README.md                    # This file
├── ROADMAP.md                   # Vision, future work, and changelog
├── CONTRIBUTING.md              # How to contribute
├── LICENSE                      # MIT License
├── .claude-plugin/
│   └── marketplace.json         # Forge Marketplace (38 plugins)
├── forge-plugin/                # The Forge Core Plugin
│   ├── agents/                  # 19 agents (.md + .config.json each)
│   ├── skills/                  # 102 skills (SKILL.md + examples.md each)
│   ├── commands/                # 12 commands (flat .md files + _docs/ for examples)
│   ├── context/                 # 81 files across 9 domains
│   ├── memory/                  # 4-layer project learning
│   ├── hooks/                   # 20 automated handlers + hooks.json
│   ├── interfaces/              # 4 core contracts + adapters + schemas
│   ├── tests/                   # Automated test suite (~1,993 checks)
│   └── mcps/                    # 8 MCP server integrations
├── microsoft/                   # Microsoft external skills (7 Plugin Wrappers → 133 skills)
├── vercel/                      # Vercel external skills (1 Plugin Wrapper → 5 skills)
├── google-labs-code/            # Google Labs external skills (1 Plugin Wrapper → 6 skills)
├── trailofbits/                 # Trail of Bits external skills (27 Native Plugins → 53 skills)
├── sentry-team/                 # Sentry external skills (1 Native Plugin → 15 skills)
└── scripts/                     # Setup, symlink management, and validation
```

---

## 🎁 Contributing

We welcome contributions! Whether you're forging a new skill, summoning a new agent, or sharpening existing tools:

1. 🍴 **Fork** [Olino3/forge](https://github.com/Olino3/forge)
2. 🌿 **Branch** from `develop`
3. ⚒️ **Build** following the conventions in [CONTRIBUTING.md](CONTRIBUTING.md)
4. 🧪 **Test** with `bash tests/run_all.sh --layer2`
5. 📤 **PR** against `develop`

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on adding skills, agents, commands, context, and hooks.

---

## 📜 License

[MIT License](LICENSE) — forge freely.

---

## 🆘 Need Help?

- 📖 Read [CLAUDE.md](CLAUDE.md) for the complete operating manual
- 🗺️ Check [ROADMAP.md](ROADMAP.md) for what's being built
- 🐛 [Open an issue](https://github.com/Olino3/forge/issues) for bugs or requests
- 🤝 [Submit a PR](https://github.com/Olino3/forge/pulls) to contribute

---

<div align="center">

**⚒️ Forged by Hephaestus. Tempered by experience. Worthy of Olympus. ⚒️**

</div>
