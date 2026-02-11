# ⚒️ The Forge ⚒️

> *"As Hephaestus crafted divine weapons for the gods, so too does the Forge craft tools for mortal developers."*

<div align="center">

🔥 **An Agentic Software Factory for Claude Code** 🔥

*Where divine agents, battle-tested skills, and structured commands transform code into artifacts worthy of Mount Olympus*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Forged in Shell](https://img.shields.io/badge/Forged_in-Shell-success?style=for-the-badge&logo=gnu-bash)](https://github.com/Olino3/forge)
[![Agents](https://img.shields.io/badge/Agents-11-blue?style=for-the-badge)](forge-plugin/agents/)
[![Skills](https://img.shields.io/badge/Skills-22-orange?style=for-the-badge)](forge-plugin/skills/)
[![Hooks](https://img.shields.io/badge/Hooks-20-red?style=for-the-badge)](forge-plugin/hooks/)

</div>

---

## What Is The Forge?

The Forge is not a plugin collection — it is a complete **Agentic Software Factory** that extends [Claude Code](https://claude.ai/code) with an entire engineering workshop. Built on pure convention (no build tools, no package managers, no compiled code), the Forge provides:

| Component | Count | What It Does |
|-----------|-------|-------------|
| 🏛️ **Agents** | 11 | AI personas with deep domain expertise (4 Olympian + 7 specialist) |
| 🔨 **Skills** | 22 | Specialized capabilities — code review, test generation, infrastructure |
| ⚡ **Commands** | 12 | Structured workflows — `/analyze`, `/implement`, `/test`, and more |
| 📚 **Context** | 81 files | Shared knowledge across 9 domains with YAML frontmatter |
| 🧠 **Memory** | 4 layers | Project-specific learning that grows with every invocation |
| 🪝 **Hooks** | 20 | Automated security, quality gates, and integrity enforcement |
| 🔌 **MCP Servers** | 8 | External knowledge conduits (docs, browser, search, code intel) |
| ⚙️ **Interfaces** | 4 | Abstract contracts decoupling all components from the filesystem |
| 🧪 **Tests** | ~1,993 | Layered test suite — static validation, hook integration, E2E |

---

## Quick Start

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

## 🏛️ The Pantheon — 11 Agents

Agents are AI personas with deep domain expertise, persistent memory, and curated skill sets.

### Divine Council (Olympian Tier)

| Agent | Domain | Specialization |
|-------|--------|---------------|
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

## 🔨 The Armory — 22 Skills

Skills are deep, specialized capabilities invoked via `skill:{name}` syntax.

| Category | Skills |
|----------|--------|
| **Code Review** | `python-code-review` · `dotnet-code-review` · `angular-code-review` · `get-git-diff` |
| **Test Generation** | `generate-python-unit-tests` · `generate-jest-unit-tests` · `test-cli-tools` |
| **Infrastructure** | `generate-azure-functions` · `generate-azure-pipelines` · `generate-azure-bicep` · `generate-tilt-dev-environment` · `generate-mock-service` |
| **Analysis** | `file-schema-analysis` · `database-schema-analysis` · `python-dependency-management` |
| **Productivity** | `commit-helper` · `email-writer` · `slack-message-composer` · `documentation-generator` |
| **Data Science** | `excel-skills` · `jupyter-notebook-skills` |
| **Meta** | `generate-more-skills-with-claude` |

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
│  11 Agents      22 Skills     12 Commands            │
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

CI runs automatically via GitHub Actions on every push/PR. See [TESTING_ROADMAP.md](TESTING_ROADMAP.md) for the full testing architecture.

---

## 📁 Project Structure

```
forge/
├── CLAUDE.md                    # The Forge Operating Manual (for Claude Code)
├── README.md                    # This file
├── ROADMAP.md                   # Vision and changelog
├── TESTING_ROADMAP.md           # Testing architecture and specifications
├── CONTRIBUTING.md              # How to contribute
├── LICENSE                      # MIT License
└── forge-plugin/                # The Forge Plugin
    ├── agents/                  # 11 agents (.md + .config.json each)
    ├── skills/                  # 22 skills (SKILL.md + examples.md each)
    ├── commands/                # 12 commands (COMMAND.md + examples.md each)
    ├── context/                 # 81 files across 9 domains
    ├── memory/                  # 4-layer project learning
    ├── hooks/                   # 20 automated handlers + hooks.json
    ├── interfaces/              # 4 core contracts + adapters + schemas
    ├── tests/                   # Automated test suite (~1,993 checks)
    └── mcps/                    # 8 MCP server integrations
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
