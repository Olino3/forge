# ⚒️ Forge Roadmap

> *Where Hephaestus crafts tools for the divine architects of code*

---

## 🔨 Skills

### ✅ Forged & Battle-Tested
- **get-git-diff** (v1.1.0) - Analyze the flames of change
- **dotnet-code-review** (v1.0.0) - Cast .NET artifacts of quality
- **python-code-review** (v2.1.0) - Temper Python steel with expert critique
- **angular-code-review** - Shape TypeScript frameworks with precision
- **python-dependency-management** - Forge unbreakable dependency chains
- **generate-python-unit-tests** - Craft shields of test coverage
- **generate-jest-unit-tests** - Weave JavaScript testing armor
- **test-cli-tools** - Hammer command-line tools into reliability
- **generate-azure-functions** (v1.0.0) - Summon serverless constructs with Tilt & Azurite
- **generate-azure-pipelines** (v1.0.0)- Build automated deployment forges
- **generate-azure-bicep** (v1.0.0) - Shape infrastructure as code
- **generate-tilt-dev-environment** (v1.0.0) - Construct local development realms
- **generate-mock-service** (v1.0.0) - Forge simulated service doppelgangers
- **file-schema-analysis** (v1.0.0) - Decode the structure of artifacts
- **database-schema-analysis** (v1.0.0) - Map the foundations of data temples
- **commit-helper** (v1.0.0) - Craft meaningful change chronicles
- **email-writer** (v1.0.0) - Compose professional correspondence
- **slack-message-composer** (v1.0.0) - Shape team communications
- **documentation-generator** (v1.0.0) - Inscribe knowledge into permanence
- **excel-skills** (v1.0.0) - Master spreadsheet manipulation
- **jupyter-notebook-skills** (v1.0.0) - Command interactive data exploration
- **generate-more-skills-with-claude** (v1.0.0) - Let the AI forge new tools

### 📋 Blueprints Awaiting (Planned)

#### Meta-Skill
(None currently planned)

---

## ⚡ Commands

> *Divine words that invoke the power of the forge*

### ✅ Forged & Battle-Tested
- `/analyze` (v1.0.0) - Deep dive into codebase mysteries
- `/implement` (v1.0.0) - Bring features into existence
- `/improve` (v1.0.0) - Refine existing creations
- `/document` (v1.0.0) - Chronicle knowledge and patterns
- `/test` (v1.0.0) - Validate with trial by fire
- `/build` (v1.0.0) - Construct and compile artifacts
- `/brainstorm` (v1.0.0) - Spark creative solutions
- `/remember` (v1.0.0) - Store wisdom in project memory
- `/mock` (v1.0.0) - Summon test doubles and simulacra
- `/azure-pipeline` (v1.0.0) - Orchestrate Azure CI/CD
- `/etl-pipeline` (v1.0.0) - Engineer data transformations
- `/azure-function` (v1.0.0) - Deploy serverless logic

### 📋 Awaiting Implementation (Planned)
(None currently planned)

---

## 🛡️ Agents

> *Specialized artificers, each a master of their domain*

### ✅ Legion Summoned & Ready
- **@devops-engineer** (v1.0.0) - Master of deployment and infrastructure
- **@python-engineer** (v1.0.0) - Python language specialist
- **@frontend-engineer** (v1.0.0) - UI/UX craftsperson
- **@developer-environment-engineer** (v1.0.0) - Local tooling expert

#### Divine Council (Olympian Tier)
- **@hephaestus** (v1.0.0) - Chief artificer and tool creator
- **@prometheus** (v1.0.0) - Foresight and strategic planning
- **@ares** (v1.0.0) - Battle-tested deployment warrior
- **@poseidon** (v1.0.0) - Data flow and stream orchestrator

### 📋 Legion Awaiting Summons (Planned)
- **@technical-writer** - Documentation artisan
- **@full-stack-engineer** - End-to-end architect
- **@data-scientist** - Analytics and ML specialist

---

## 🪝 Hooks

> *Automated rituals that trigger at key moments*

### ✅ Forged & Battle-Tested
- **memory_sync** (PostToolUse) - Validate and timestamp memory files after writes
- **pre_commit_quality** (PreToolUse) - Block commits with secrets or /claudedocs files
- **context_freshness** (Manual) - Audit context file health and broken links
- **output_archival** (PostToolUse) - Archive skill output with manifest
- **session_context** (Manual) - Summarize project state at session start

### 📋 Planned Enchantments
- Additional hooks based on usage patterns

---

## 🔌 MCP Integration

> *Model Context Protocol servers - external knowledge conduits*

### ✅ Forged & Connected
- **sequential-thinking** - Step-by-step reasoning for complex problems
- **context7** - Library documentation access
- **magic** - UI component generation (requires `TWENTYFIRST_API_KEY`)
- **playwright** - Browser automation and E2E testing
- **serena** - Code intelligence and navigation (requires Python + uv)
- **morphllm-fast-apply** - Fast code application/editing (requires `MORPH_API_KEY`)
- **tavily** - Web search and research (requires `TAVILY_API_KEY`, free tier available)
- **chrome-devtools** - Chrome DevTools Protocol for performance/debugging

### 📋 Planned Connections
- **aider** - AI pair programming assistant
- **youtube** - Video content integration

---

## 🗺️ The Path Forward

*Hephaestus's forge never cools. Each skill sharpened, each agent awakened, each command invoked brings us closer to the perfect workshop—where mortal developers wield divine tools.*

**Current Focus**: MCP integration and extending server capabilities
**Next Milestone**: Additional hooks based on usage patterns, more MCP servers
**Long-term Vision**: A fully autonomous forge where agents self-organize to solve complex engineering challenges

---

**Recent Forge Activity:**
- ✅ **February 10, 2026**: MCP Server Integration - 8 external knowledge conduits connected
  - **Configuration**: `.mcp.json` at repo root with all 8 server definitions
  - **Free servers**: sequential-thinking, context7, playwright, serena, chrome-devtools
  - **API key servers**: magic (`TWENTYFIRST_API_KEY`), morphllm-fast-apply (`MORPH_API_KEY`), tavily (`TAVILY_API_KEY`)
  - **Documentation**: `forge-plugin/mcps/` with index, activation protocol, installation guide, and 8 per-server docs
  - **Forge integration**: Skill/command-to-server mapping, fallback strategies, anti-patterns
- ✅ **February 10, 2026**: Infrastructure Improvements - Comprehensive quality upgrade
  - **Context Management**: Standardized loading protocol (`loading_protocol.md`), cross-domain references (`cross_domain.md`), engineering best practices context (6 files covering code review, API design, testing, architecture, error recovery)
  - **Memory Management**: Shared project memory layer (`memory/projects/`), lifecycle management with freshness/pruning rules (`lifecycle.md`), quality guidance (`quality_guidance.md`), completed memory index files for generate-tilt-dev-environment and generate-mock-service
  - **Hooks System**: 5 lifecycle hooks (memory_sync, pre_commit_quality, context_freshness, output_archival, session_context) with architecture docs and usage guide
  - **Standards**: Skill workflow template (`SKILL_TEMPLATE.md`), output naming conventions (`OUTPUT_CONVENTIONS.md`)
  - **CLAUDE.md**: Fully reconciled with actual repo state (22 skills, 12 commands, 11 agents, 9 context domains, hooks system)
- ✅ **February 10, 2026**: Commands v1.0.0 - Phase 2 complete (5 new commands)
  - `/remember` - Project memory management for decisions, patterns, conventions, and lessons
  - `/mock` - Mock service generation with multiple frameworks (Express, Flask, FastAPI, WireMock, Prism)
  - `/azure-pipeline` - Azure DevOps CI/CD orchestration with multi-stage pipelines
  - `/etl-pipeline` - Data transformation pipelines with Airflow, Azure Data Factory, Databricks support
  - `/azure-function` - Serverless Azure Functions with Tilt + Azurite local development
  - Plugin now has 12 total commands for comprehensive development workflow
  - Delegates to existing skills: generate-mock-service, generate-azure-pipelines, generate-azure-functions, generate-azure-bicep
- ✅ **February 9, 2026**: Commands v1.0.0 - Phase 1 complete (7 commands)
  - `/analyze` - Code analysis with skill delegation (python/dotnet/angular code review)
  - `/implement` - Feature implementation with test generation integration
  - `/improve` - Code improvement with analysis-first approach
  - `/document` - Documentation generation with language-specific conventions
  - `/test` - Test execution with coverage and skill delegation
  - `/build` - Project building with intelligent error handling
  - `/brainstorm` - Requirements discovery through Socratic dialogue
  - Command-specific context files (7 files in `context/commands/`)
  - Command memory system with execution tracking
  - Plugin version bumped to 1.1.0
- ✅ **February 9, 2026**: Divine Council (Olympian Tier) agents summoned
  - **@hephaestus v1.0.0**: Chief artificer and tool creator
    - Master of skill creation using meta-skill framework
    - Template engineering and code generation expertise
    - Memory tracking for skill patterns and innovations
  - **@prometheus v1.0.0**: Master of foresight and strategic planning
    - Architecture design and technical roadmaps
    - Refactoring strategies and decision records (ADRs)
    - Technology evaluation and risk assessment
  - **@ares v1.0.0**: Battle-tested deployment warrior
    - Production deployment and incident response
    - System monitoring and disaster recovery
    - Performance optimization and operational excellence
  - **@poseidon v1.0.0**: Master of data flow and stream orchestration
    - ETL pipelines and stream processing
    - Event-driven architecture and data integration
    - Data transformation and quality assurance
- ✅ **February 9, 2026**: Three new specialized agents summoned to the legion
  - **@python-engineer v1.0.0**: Python language specialist
    - Deep expertise in Python development, testing, and frameworks (Django, Flask, FastAPI)
    - Integration with python-code-review, generate-python-unit-tests, python-dependency-management skills
    - Comprehensive Python context file navigation (testing, frameworks, ML, data science)
    - Memory system for project-specific patterns and conventions
    - Validation hooks for Python files and dependency manifests
  - **@frontend-engineer v1.0.0**: UI/UX craftsperson
    - Modern frontend development with Angular, TypeScript, RxJS, NgRx
    - Component architecture, responsive design, accessibility (WCAG)
    - Integration with angular-code-review and generate-jest-unit-tests skills
    - Comprehensive Angular context file navigation (components, services, state management)
    - Memory system for UI patterns and design decisions
    - Validation hooks for TypeScript, templates, and configuration files
  - **@developer-environment-engineer v1.0.0**: Local tooling expert
    - Developer experience with Tilt, Docker, Docker Compose, mock services
    - Integration with generate-tilt-dev-environment, generate-mock-service, test-cli-tools skills
    - Context navigation for local development setup and containerization
    - Memory system for environment configurations and workflows
    - Validation hooks for development environment files

- ✅ **February 9, 2026**: Meta-Skill for autonomous skill creation completed
  - **generate-more-skills-with-claude v1.0.0**: Let the AI forge new tools
    - 6-step mandatory workflow for skill generation
    - Template-based SKILL.md and examples.md generation
    - Support for scripts and output templates
    - Memory integration for pattern learning
    - Context file awareness and integration
    - 6 comprehensive examples covering skill complexity spectrum

- ✅ **February 6, 2026**: Data Science Arsenal and Documentation & Communication skills completed
  - **excel-skills**: Master spreadsheet manipulation across Excel, Google Sheets, and LibreOffice
    - Formula engineering (VLOOKUP, INDEX-MATCH, SUMIFS, array formulas)
    - VBA/Apps Script/Python automation for batch operations
    - Data transformation and cleaning workflows
    - Cross-platform compatibility support
    - Template-based output formatting
  - **jupyter-notebook-skills**: Command interactive data exploration in Jupyter notebooks
    - Exploratory Data Analysis (EDA) workflows
    - Machine learning model training and evaluation
    - Statistical analysis and hypothesis testing
    - Data visualization with matplotlib, seaborn, plotly
    - Reproducible notebook generation with best practices
  - **commit-helper v1.0.0**: Craft meaningful change chronicles
    - Conventional Commits compliance
    - Breaking change detection
    - Git diff analysis integration
  - **email-writer v1.0.0**: Compose professional correspondence
    - Audience analysis and tone calibration
    - Support for status updates, requests, announcements, escalations
    - Action item tracking
  - **slack-message-composer v1.0.0**: Shape team communications
    - Channel-appropriate formatting
    - Thread management
    - Emoji and mention integration
  - **documentation-generator v1.0.0**: Inscribe knowledge into permanence
    - API documentation generation
    - README and guide creation
    - Technical specification writing

- ✅ **February 6, 2026**: generate-tilt-dev-environment v1.0.0 and generate-mock-service v1.0.0 completed
  - **generate-tilt-dev-environment**: Complete local development environment generation
    - Tiltfile generation with live reload and service orchestration
    - Docker Compose configuration for all services and dependencies
    - Multi-language support (Python, Node.js, .NET, Go, Java)
    - Makefile with common development commands
    - Environment variable management with templates
    - Memory system for environment configuration tracking
  - **generate-mock-service**: Simulated service generation for testing
    - Multiple mock server types (Express, Flask, FastAPI, WireMock, Prism)
    - Realistic response data generation with Faker
    - Multiple scenario support (success, error, edge cases)
    - Request validation and authentication middleware
    - Docker containerization for easy integration
    - Memory system for mock configuration tracking
- ✅ **February 6, 2025**: Schema Analysis Tools v1.0.0 completed
  - file-schema-analysis skill for analyzing file-based schemas (JSON, Protobuf, GraphQL, OpenAPI, Avro, etc.)
  - database-schema-analysis skill for analyzing database schemas (SQL and NoSQL)
  - Comprehensive context files for schema patterns, file formats, and database patterns
  - Template-based reporting with ERD generation and index analysis
  - Memory system for tracking project-specific schema conventions
  - Helper scripts for schema extraction and database introspection

- ✅ **November 18, 2025**: generate-azure-functions v1.0.0 completed
  - Complete Azure Functions project generation with v1/v2 model support
  - Tilt + Azurite local development environment with live reload
  - 6 comprehensive Azure context files (overview, Tilt, Docker, Azurite setup)
  - Support for Python, Node.js, and .NET runtimes
  - Poetry/pip/npm dependency management
  - Local package integration for shared libraries
  - Memory system for configuration tracking

- ✅ **November 14, 2025**: dotnet-code-review v1.0.0 completed
  - Full .NET Framework 4.8 and modern .NET (Core/.NET 5-8+) support
  - 12 comprehensive context files (async, EF, DI, Blazor, security, performance, LINQ, etc.)
  - Complete memory system with project-specific learning
  - Integrated with get-git-diff for changed-file analysis

---

*Last Updated: February 10, 2026*
*Maintained by: The Forge Keepers*
