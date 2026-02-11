# ⚒️ The Forge — Roadmap

> *"Hephaestus's forge never cools. Each skill sharpened, each agent awakened, each command invoked brings us closer to the perfect workshop — where mortal developers wield divine tools."*

---

## The Factory Today

The Forge is a fully operational **Agentic Software Factory** — a Claude Code plugin built on convention, powered by 4 core interfaces, and staffed by a pantheon of divine agents.

### What's Forged and Ready

| Component | Count | Status |
|-----------|-------|--------|
| **Skills** | 22 | ✅ All operational, interface-based |
| **Commands** | 12 | ✅ All operational, interface-based |
| **Agents** | 11 | ✅ 4 Olympian + 7 specialist, all with config.json |
| **Context Files** | 81 | ✅ 9 domains, all with YAML frontmatter |
| **Interfaces** | 4 | ✅ ContextProvider, MemoryStore, SkillInvoker, ExecutionContext |
| **Adapters** | 3 | ✅ MarkdownFileContextProvider, MarkdownFileMemoryAdapter, CachedContextProvider |
| **Hooks** | 20 | ✅ 9 events, 4 layers (Shield, Chronicle, Foreman, Town Crier) |
| **MCP Servers** | 8 | ✅ Connected external conduits |

### The Pantheon (Active Agents)

**Olympian Tier** — @hephaestus (tool creation), @prometheus (strategy), @ares (deployment), @poseidon (data flow)

**Specialist Legion** — @python-engineer, @frontend-engineer, @devops-engineer, @developer-environment-engineer, @data-scientist, @full-stack-engineer, @technical-writer

### The Armory (Active Skills)

**Code Review** — python-code-review · dotnet-code-review · angular-code-review · get-git-diff

**Test Generation** — generate-python-unit-tests · generate-jest-unit-tests · test-cli-tools

**Infrastructure** — generate-azure-functions · generate-azure-pipelines · generate-azure-bicep · generate-tilt-dev-environment · generate-mock-service

**Analysis** — file-schema-analysis · database-schema-analysis · python-dependency-management

**Productivity** — commit-helper · email-writer · slack-message-composer · documentation-generator

**Data Science** — excel-skills · jupyter-notebook-skills

**Meta** — generate-more-skills-with-claude

### The War Room (Active Commands)

`/analyze` · `/implement` · `/improve` · `/document` · `/test` · `/build` · `/brainstorm` · `/remember` · `/mock` · `/azure-pipeline` · `/etl-pipeline` · `/azure-function`

---

## What's Been Forged

### Phase 5 — Optimization & Hardening ✅

Refined the interface layer for robustness and performance.

- [x] Three-tier cached context provider with session-scoped invalidation
- [x] Shared loading patterns replacing 15-35 lines/skill with ~5 lines
- [x] Deprecation rules for legacy patterns with detection regex
- [x] Future adapter designs: SQLite, Context7 MCP, VectorStore

### Phase 6 — The Anvil (Hooks & Automated Reinforcement) ✅

Expanded the hook system from 5 legacy scripts to **20 registered handlers across 9 events**, organized into 4 thematic layers with comprehensive security, memory hygiene, workflow enforcement, and health reporting.

**🛡️ The Shield — Security & Initialization (5 hooks)**
- [x] `root_agent_validator` — Validate root session safety config on start
- [x] `dependency_sentinel` — Block malicious/typosquatted package installs
- [x] `git_hygiene_enforcer` — Enforce branch naming, conventional commits, block pushes to main
- [x] `sandbox_boundary_guard` — Prevent file operations outside project directory
- [x] `pii_redactor` — Sanitize PII from user input before model context

**📜 The Chronicle — Memory & Learning (4 hooks)**
- [x] `memory_freshness_enforcer` — Auto-flag stale memory (>90 days) with system notifications
- [x] `memory_cross_pollinator` — Propagate critical findings to shared project memory
- [x] `memory_quality_gate` — Validate memory entries on write via `memoryStore.validate()`
- [x] `memory_pruning_daemon` — Batch-prune memory files post-session to enforce line limits

**👷 The Foreman — Workflow & Quality (8 hooks)**
- [x] `skill_compliance_checker` — Audit skill invocations for mandatory workflow step compliance
- [x] `agent_config_validator` — Validate agent config.json against schema before spawn
- [x] `context_drift_detector` — Detect dependency changes that conflict with loaded context
- [x] `frontmatter_validator` — Enforce YAML frontmatter schema on context file edits
- [x] `output_quality_scorer` — Score skill output completeness and actionability
- [x] `command_chain_context` — Persist ExecutionContext between chained commands
- [x] `pre_commit_quality` — Block commits with secrets or `/claudedocs` files
- [x] `output_archival` — Archive skill output with manifest tracking

**📢 The Town Crier — Operational & Telemetry (3 hooks)**
- [x] `forge_telemetry` — Aggregate session stats (skills, memory writes, token usage)
- [x] `context_usage_tracker` — Identify unreferenced/over-used context files
- [x] `system_health_emitter` — Aggregate all hook warnings into single `[System Health]` block

### Phase 7 — The Grand Reforging (Documentation & Identity) ✅

Complete documentation rewrite to reflect the Factory's mature architecture.

- [x] `CLAUDE.md` — Rewritten as the Forge Operating Manual
- [x] `copilot-instructions.md` — Rewritten as the Contributor's Codex
- [x] `CONTRIBUTING.md` — Comprehensive contribution guide
- [x] `LICENSE` — MIT License
- [x] `ROADMAP.md` — Living vision document (this file)
- [x] `README.md` — Public-facing showcase of the Software Factory

### Phase 8 — The Proving Grounds (Testing Architecture) 🔨

Layered testing architecture validating the entire plugin — from static file structure to runtime hook behavior — using only bash, python3, and optionally shellcheck. See `TESTING_ROADMAP.md` for full specifications.

**Phase 1 — Foundation & Infrastructure ✅**
- [x] `tests/conftest.py` — Shared pytest config with FORGE_DIR resolution, YAML frontmatter extraction, JSON loader
- [x] `tests/pytest.ini` — Pytest configuration with markers
- [x] `tests/run_all.sh` — Master test runner with `--layer2`/`--e2e` flags
- [x] `tests/layer1/run_layer1.sh` — Layer 1 specific runner
- [x] `test_json_schemas.py` — All 11 agent configs + hooks.json + plugin.json + safety profile validated against schemas (170 tests)
- [x] `test_file_structure.py` — Agent file pairing, skill/command directory conventions, structural integrity
- [x] `test_hook_syntax.sh` — Shebang, strict mode, `bash -n` syntax, executable permissions (96 checks)

**Phase 2 — Static Validation (Context, Memory, Cross-References) ✅**
- [x] `test_yaml_frontmatter.py` — All 81 context files validated against `context_metadata.schema.json` (813 tests)
- [x] `test_cross_references.py` — Referential integrity: agent→skill, agent→domain, agent→memory, hooks.json→scripts, plugin→commands
- [x] `test_hooks_registration.py` — Registration completeness, duplicate detection, known unregistered script tracking
- [x] `test_memory_structure.py` — Directory structure, timestamp formats, line limit enforcement
- [x] `test_plugin_manifest.py` — All 12 commands validated, path resolution, convention compliance
- [x] `test_shellcheck.sh` — Bash linting at warning level (graceful skip if shellcheck absent)

**Summary**: ~1,300 static validation tests across 10 test files (1,131 pytest + 96 bash + shellcheck)

**Phase 3 — Hook Test Harness + Shield Layer Tests ✅**
- [x] `layer2/hooks/hook_helpers.py` — HookRunner, HookResult, TempForgeEnvironment classes with path resolution constants
- [x] `layer2/hooks/conftest.py` — Pytest fixtures (hook_runner, temp_forge_env, forge_dir, repo_root)
- [x] `fixtures/hook_inputs/*.json` — 18 fixture files covering PreToolUse (Read, Write, Edit, Bash) and UserPromptSubmit events
- [x] `test_sandbox_boundary_guard.py` — Project path allow/deny, sensitive files, bash dangerous paths/patterns (66 tests)
- [x] `test_pii_redactor.py` — Email, SSN, AWS keys, GitHub tokens, private keys, phone numbers, multi-PII (23 tests)
- [x] `test_dependency_sentinel.py` — pip/npm/yarn allow/deny, typosquats, malicious packages, deny list validation (54 tests)
- [x] `test_git_hygiene_enforcer.py` — Push protection, force push, conventional commits, secrets in staged diffs (42 tests)
- [x] `test_pre_commit_quality.py` — Staged secrets, claudedocs, SKILL.md version history, memory absolute paths (23 tests)

**Summary**: ~1,508 total tests (1,131 Layer 1 pytest + 96 bash + shellcheck + 208 Layer 2 hook integration)

**Phase 4 — Chronicle, Foreman & Town Crier Hook Tests ✅**
- [x] `test_health_buffer_lib.py` — health_buffer.sh shared library: append, flush, max-line cap, init (10 tests)
- [x] `test_memory_freshness_enforcer.py` — Memory age classification: fresh/aging/stale/missing timestamp, operational skip (17 tests)
- [x] `test_memory_quality_gate.py` — Timestamp injection, line limits, vague entry & absolute path detection (15 tests)
- [x] `test_memory_cross_pollinator.py` — Critical/Security/Breaking/Performance section propagation (10 tests)
- [x] `test_memory_pruning_daemon.py` — Line-limit pruning (200/300/500), header preservation, operational skip (9 tests)
- [x] `test_frontmatter_validator.py` — Domain/type/strategy enum validation, missing fields, special file skip (18 tests)
- [x] `test_agent_config_validator.py` — Real agent configs, built-in agent skip, informational-only (11 tests)
- [x] `test_skill_compliance_checker.py` — 6-step workflow compliance, compliant/non-compliant sessions (9 tests)
- [x] `test_output_quality_scorer.py` — Claudedocs scoring (Completeness/Actionability/Formatting/Naming), metadata append (9 tests)
- [x] `test_context_drift_detector.py` — Dependency file recognition, missing conflicts file handling (11 tests)
- [x] `test_command_chain_context.py` — chain_state.json creation, command chaining, session reset (11 tests)
- [x] `test_output_archival.py` — Archive creation, manifest tracking, standalone script execution (6 tests)
- [x] `test_root_agent_validator.py` — Real structure validation, component counts, .forge creation (7 tests)
- [x] `test_system_health_emitter.py` — Buffer seeding, flush+emit cycle, empty buffer handling (7 tests)
- [x] `test_forge_telemetry.py` — Metrics extraction (tool calls, skills, memory, context, commands), telemetry logging (13 tests)
- [x] `test_context_usage_tracker.py` — Context usage analysis, waste estimation, telemetry logging (12 tests)

**Summary**: ~1,683 total tests (1,131 Layer 1 pytest + 96 bash + shellcheck + 208 Phase 3 + 175 Phase 4 hook integration)

---

## Planned Agents

> *"The remaining Olympians await their summons — each divine power destined for its domain."*

### The Olympian Council (8 agents)

The complete pantheon of the Twelve Olympians, each embodying a core aspect of the software factory.

| Agent | Domain | Divine Power | Status |
|-------|--------|--------------|--------|
| **@zeus** | Orchestration & Leadership | King of the gods — orchestrates multi-agent workflows, delegates tasks, oversees the entire factory. Commands the divine council and coordinates complex engineering initiatives. | 📋 Planned |
| **@hera** | Project Management & Governance | Queen of the gods — manages project lifecycles, enforces standards, maintains architectural coherence. Guards the integrity of the codebase and ensures team alignment. | 📋 Planned |
| **@athena** | Wisdom & Strategic Architecture | Goddess of wisdom and strategy — designs system architecture, evaluates technical decisions, provides strategic counsel. Synthesizes complex requirements into elegant solutions. | 📋 Planned |
| **@apollo** | Code Quality & Optimization | God of light and prophecy — illuminates code quality issues, predicts performance bottlenecks, optimizes algorithms. Brings clarity and precision to engineering challenges. | 📋 Planned |
| **@artemis** | Testing & Quality Assurance | Goddess of the hunt — tracks down bugs with precision, designs comprehensive test strategies, ensures code integrity. Hunts defects across the wilderness of the codebase. | 📋 Planned |
| **@aphrodite** | UX/UI & Design Systems | Goddess of beauty — crafts beautiful user experiences, designs elegant interfaces, ensures visual harmony. Makes software delightful and human-centered. | 📋 Planned |
| **@hermes** | Integration & Communication | Messenger of the gods — manages API integrations, handles inter-service communication, facilitates data exchange. Swift connector between disparate systems. | 📋 Planned |
| **@demeter** | Data Cultivation & Growth | Goddess of harvest — nurtures data pipelines, cultivates analytics, ensures data quality and growth. Tends to the fields of information that feed the factory. | 📋 Planned |

**Already Active (4 Olympians):**
- ✅ **@hephaestus** — Tool creation and craftsmanship (blacksmith of the gods)
- ✅ **@ares** — Deployment and DevOps warfare (god of war)
- ✅ **@poseidon** — Data flow and streams (god of the seas)
- ✅ **@prometheus** — Strategic foresight (titan of forethought) *Note: Titan, not Olympian*

### Alternative Olympians

*Two seats at the Olympian table were contested in mythology — Hestia and Dionysus.*

| Agent | Domain | Divine Power | Status |
|-------|--------|--------------|--------|
| **@hestia** | Stability & Core Infrastructure | Goddess of the hearth — maintains foundational systems, ensures stability, guards core infrastructure. The eternal flame that keeps the factory running. | 🔮 Alternate |
| **@dionysus** | Experimentation & Innovation | God of wine and ecstasy — drives creative exploration, facilitates A/B testing, encourages unconventional solutions. Breaks boundaries to discover new possibilities. | 🔮 Alternate |

---

## Planned Skills

> *"The blueprints are drawn — these weapons await their turn at the anvil."*

### Frontend & UI (15 skills)

| Skill | Description |
|-------|-------------|
| **accessibility** | Build WCAG 2.1 AA compliant websites with semantic HTML, proper ARIA, focus management, and screen reader support. Includes color contrast (4.5:1 text), keyboard navigation, form labels, and live regions. |
| **auto-animate** | Zero-config animations for React, Vue, Solid, Svelte, Preact with @formkit/auto-animate (3.28kb). Prevents 15 errors. |
| **hono-routing** | Build type-safe APIs with Hono for Cloudflare Workers, Deno, Bun, Node.js. Routing, middleware, validation (Zod/Valibot), RPC, streaming (SSE), WebSocket, security (CSRF, secureHeaders). |
| **motion** | Build React animations with Motion (Framer Motion) — gestures (drag, hover, tap), scroll effects, spring physics, layout animations, SVG. Bundle: 2.3 KB (mini) to 34 KB (full). |
| **nextjs** | Build Next.js 16 apps with App Router, Server Components/Actions, Cache Components ("use cache"), and async route params. Includes proxy.ts and React 19.2. Prevents 25 errors. |
| **react-hook-form-zod** | Build type-safe validated forms using React Hook Form v7 and Zod v4. Single schema works on client and server with full TypeScript inference via `z.infer`. |
| **responsive-images** | Implement performant responsive images with srcset, sizes, lazy loading, and modern formats (WebP, AVIF). Covers aspect-ratio for CLS prevention, picture element for art direction, and fetchpriority. Triggers: `srcset`, `loading=`, `lazy`, `eager` |
| **tailwind-patterns** | Production-ready Tailwind CSS patterns for common website components: responsive layouts, cards, navigation, forms, buttons, and typography. Includes spacing scale, breakpoints, mobile-first patterns. Triggers: `Tailwind CSS`, `CSS utility classes`, `first CSS`, `shadcn/ui components` |
| **tailwind-v4-shadcn** | Set up Tailwind v4 with shadcn/ui using @theme inline pattern and CSS variable architecture. Four-step pattern: CSS variables, Tailwind mapping, base styles, automatic dark mode. Prevents 8 errors. |
| **tanstack-query** | Manage server state in React with TanStack Query v5. Covers useMutationState, simplified optimistic updates, throwOnError, network mode (offline/PWA), and infiniteQueryOptions. |
| **tanstack-router** | Build type-safe, file-based React routing with TanStack Router. Supports client-side navigation, route loaders, and TanStack Query integration. Prevents 20 errors. Triggers: `TanStack Router`, `@tanstack/react-router`, `type-safe routing` |
| **tanstack-start** | Build full-stack React apps with TanStack Start on Cloudflare Workers. Type-safe routing, server functions, SSR/streaming, D1/KV/R2 integration. Prevents 9 errors. |
| **tanstack-table** | Build headless data tables with TanStack Table v8. Server-side pagination, filtering, sorting, and virtualization for Cloudflare Workers + D1. Prevents 12 errors. Triggers: `data table`, `datagrid`, `table component`, `server-side pagination` |
| **tiptap** | Build rich text editors with Tiptap — headless editor framework with React and Tailwind v4. Covers SSR-safe setup, image uploads, prose styling, and collaborative editing. |
| **zustand-state-management** | Build type-safe global state in React with Zustand. Supports TypeScript, persist middleware, devtools, slices pattern, and Next.js SSR with hydration handling. Prevents 6 errors. |

### Authentication (5 skills)

| Skill | Description |
|-------|-------------|
| **azure-auth** | Microsoft Entra ID (Azure AD) authentication for React SPAs with MSAL.js and Cloudflare Workers JWT validation using jose library. Full-stack pattern with Authorization Code Flow + PKCE. Prevents 8 errors. |
| **better-auth** | Self-hosted auth for TypeScript/Cloudflare Workers with social auth, 2FA, passkeys, organizations, RBAC, and 15+ plugins. Requires Drizzle ORM or Kysely for D1 (no direct adapter). Triggers: `better-auth`, `authentication with D1`, `Cloudflare D1 auth setup` |
| **clerk-auth** | Clerk auth with API Keys beta (Dec 2025), Next.js 16 proxy.ts (March 2025 CVE context), API version 2025-11-10 breaking changes, clerkMiddleware() options, webhooks, production considerations. Prevents 15 errors. Triggers: `clerk`, `clerk auth`, `@clerk/nextjs` |
| **firebase-auth** | Build with Firebase Authentication — email/password, OAuth providers, phone auth, and custom tokens. Use when: setting up auth flows, implementing sign-in/sign-up, managing user sessions, protecting routes. Prevents 12 errors. |
| **oauth-integrations** | Implement OAuth 2.0 authentication with GitHub and Microsoft Entra (Azure AD) in Cloudflare Workers. Triggers: `GitHub OAuth`, `GitHub authentication`, `Microsoft OAuth` |

### Database & Storage (6 skills)

| Skill | Description |
|-------|-------------|
| **firebase-firestore** | Build with Firestore NoSQL database — real-time sync, offline support, and scalable document storage. Use when: creating collections, querying documents, setting up security rules, handling real-time updates. Prevents 10 errors. |
| **firebase-storage** | Build with Firebase Cloud Storage — file uploads, downloads, and secure access. Use when: uploading images/files, generating download URLs, implementing file pickers, setting up storage security rules. Prevents 9 errors. |
| **neon-vercel-postgres** | Set up serverless Postgres with Neon or Vercel Postgres for Cloudflare Workers/Edge. Includes connection pooling, git-like branching, and Drizzle ORM integration. |
| **snowflake-platform** | Build on Snowflake's AI Data Cloud with snow CLI, Cortex AI (COMPLETE, SUMMARIZE, AI_FILTER), Native Apps, and Snowpark. Covers JWT auth, account identifiers, Marketplace publishing. Prevents 11 errors. Triggers: `snowflake`, `snow cli`, `snowflake connection` |
| **vercel-blob** | Integrate Vercel Blob for file uploads and CDN-delivered assets in Next.js. Supports client-side uploads with presigned URLs and multipart transfers for large files. Prevents 16 errors. Triggers: `@vercel/blob`, `vercel blob`, `vercel file upload` |
| **vercel-kv** | Integrate Redis-compatible Vercel KV for caching, session management, and rate limiting in Next.js. Powered by Upstash with strong consistency and TTL support. Triggers: `@vercel/kv`, `vercel kv`, `upstash vercel` |

### Content Management (3 skills)

| Skill | Description |
|-------|-------------|
| **sveltia-cms** | Set up Sveltia CMS — lightweight Git-backed CMS successor to Decap/Netlify CMS (300KB bundle, 270+ fixes). Framework-agnostic for Hugo, Jekyll, 11ty, Astro. Prevents 10 errors. |
| **tinacms** | Build content-heavy sites with Git-backed TinaCMS. Provides visual editing for blogs, documentation, and marketing sites. Supports Next.js, Vite+React, and Astro with TinaCloud or Node.js self-hosting. Prevents 10 errors. |
| **wordpress-plugin-core** | Build secure WordPress plugins with hooks, database interactions, Settings API, custom post types, and REST API. Covers Simple, OOP, and PSR-4 architecture patterns plus the Security Trinity. |

### Planning & Workflow (9 skills)

| Skill | Description |
|-------|-------------|
| **divine** | Entry point to the divine toolkit — skills, agents, and commands that work with Claude Code's capabilities. |
| **docs-workflow** | Four slash commands for documentation lifecycle: `/docs`, `/docs-init`, `/docs-update`, `/docs-claude`. Create, maintain, and audit CLAUDE.md, README.md, and docs/ structure with smart templates. Triggers: `create CLAUDE.md`, `initialize documentation`, `docs init`, `update documentation` |
| **project-health** | AI-agent readiness auditing for project documentation and workflows. Triggers: `AI readability`, `agent readiness`, `context auditor`, `workflow validator` |
| **project-planning** | Generate structured planning docs for web projects with context-safe phases, verification criteria, and exit conditions. Creates IMPLEMENTATION_PHASES.md plus conditional docs. Triggers: `new project`, `start a project`, `create app`, `build app` |
| **project-session-management** | Track progress across sessions using SESSION.md with git checkpoints and concrete next actions. Converts IMPLEMENTATION_PHASES.md into trackable session state. Triggers: `create SESSION.md`, `set up session tracking`, `manage session state`, `session handoff` |
| **project-workflow** | Nine integrated slash commands for complete project lifecycle: `/explore-idea`, `/plan-project`, `/plan-feature`, `/wrap-session`, `/continue-session`, `/workflow`, `/release`, `/brief`, `/reflect`. Triggers: `start new project`, `/plan-project` |
| **skill-creator** | Design effective Claude Code skills with optimal descriptions, progressive disclosure, and error prevention patterns. Covers freedom levels, token efficiency, and quality standards. |
| **skill-review** | Audit claude-skills with systematic 9-phase review: standards compliance, official docs verification, code accuracy, cross-file consistency, and version drift detection. Triggers: `review this skill`, `audit [skill-name]`, `check if X needs updates` |
| **sub-agent-patterns** | Comprehensive guide to sub-agents in Claude Code: built-in agents (Explore, Plan, general-purpose), custom agent creation, configuration, and delegation patterns. Triggers: `sub-agent`, `sub-agents`, `subagent` |

### Utilities (11 skills)

| Skill | Description |
|-------|-------------|
| **color-palette** | Generate complete, accessible color palettes from a single brand hex. Creates 11-shade scale (50-950), semantic tokens (background, foreground, card, muted), and dark mode variants. Includes WCAG contrast checking. Triggers: `color palette`, `tailwind colors`, `css variables`, `hsl colors` |
| **email-gateway** | Multi-provider email sending for Cloudflare Workers and Node.js applications. Triggers: `resend`, `sendgrid`, `mailgun`, `smtp2go` |
| **favicon-gen** | Generate custom favicons from logos, text, or brand colors — prevents launching with CMS defaults. Extract icons from logos, create monogram favicons from initials, or use branded shapes. Outputs all required formats. |
| **firecrawl-scraper** | Convert websites into LLM-ready data with Firecrawl API. Features: scrape, crawl, map, search, extract, agent (autonomous), batch operations, and change tracking. Handles JavaScript, anti-bot bypass. Prevents 10 errors. |
| **icon-design** | Select semantically appropriate icons for websites using Lucide, Heroicons, or Phosphor. Covers concept-to-icon mapping, React/HTML templates, and tree-shaking patterns. |
| **image-gen** | Generate website images with Gemini 3 Native Image Generation. Covers hero banners, service cards, infographics with legible text, and multi-turn editing. Prevents 5 errors. Triggers: `gemini image generation`, `gemini-3-flash-image-generation`, `google genai` |
| **jquery-4** | Migrate jQuery 3.x to 4.0.0 safely in WordPress and legacy web projects. Covers all breaking changes: removed APIs ($.isArray, $.trim, $.parseJSON, $.type), focus event order changes, slim build differences. |
| **office** | Generate Office documents (DOCX, XLSX, PDF, PPTX) with TypeScript. Pure JS libraries that work everywhere: Claude Code CLI, Cloudflare Workers, browsers. Uses docx (Word), xlsx/SheetJS (Excel), pdf-lib (PDF). |
| **open-source-contributions** | Create maintainer-friendly pull requests with clean code and professional communication. Triggers: `submit PR to [project]`, `create pull request for [repo]`, `contribute to [project]` |
| **playwright-local** | Build browser automation and web scraping with Playwright on your local machine. Prevents 10 errors. |
| **seo-meta** | Generate complete SEO meta tags for every page. Covers title patterns, meta descriptions, Open Graph, Twitter Cards, and JSON-LD structured data (LocalBusiness, Service, FAQ, BreadcrumbList). Triggers: `seo`, `open graph`, `twitter cards`, `json-ld` |

### Developer Workflow (3 skills)

| Skill | Description |
|-------|-------------|
| **agent-development** | Design and build custom Claude Code agents with effective descriptions, tool access patterns, and delegation strategies. Triggers: `create agent`, `custom agent`, `build agent`, `agent description` |
| **deep-debug** | Multi-agent investigation for stubborn bugs. Use when: going in circles debugging, need to investigate browser/API interactions, complex bugs resisting normal debugging, or when symptoms don't match expectations. |
| **developer-toolbox** | Essential development workflow agents for code review, debugging, testing, documentation, and git operations. Triggers: `step` |

### Backend & Frameworks (6 skills)

| Skill | Description |
|-------|-------------|
| **django-expert** | Expert-level Django development patterns and best practices |
| **dotnet-core-expert** | .NET Core/ASP.NET Core architecture and implementation |
| **fastapi-expert** | Modern Python API development with FastAPI framework |
| **nestjs-expert** | Enterprise-grade NestJS applications with TypeScript |
| **rails-expert** | Ruby on Rails application development and architecture |
| **php-pro** | Professional PHP development patterns and frameworks |

### Frontend & Mobile (7 skills)

| Skill | Description |
|-------|-------------|
| **angular-architect** | Enterprise Angular application architecture and patterns |
| **flutter-expert** | Cross-platform mobile development with Flutter/Dart |
| **nextjs-developer** | (See above in Frontend & UI section) |
| **react-expert** | Advanced React patterns, hooks, and architecture |
| **react-native-expert** | Mobile app development with React Native |
| **vue-expert-js** | Vue.js 3 Composition API and JavaScript patterns |
| **vue-expert** | Comprehensive Vue.js application development |

### Programming Languages (5 skills)

| Skill | Description |
|-------|-------------|
| **cpp-pro** | Modern C++ (C++17/20/23) development and best practices |
| **csharp-developer** | C# language features and .NET ecosystem development |
| **java-architect** | Enterprise Java architecture and design patterns |
| **javascript-pro** | Advanced JavaScript patterns, ES2024+, and runtime optimization |
| **typescript-pro** | TypeScript advanced types, generics, and strict configuration |

### Data & Database (4 skills)

| Skill | Description |
|-------|-------------|
| **database-optimizer** | SQL query optimization, indexing, and performance tuning |
| **pandas-pro** | Advanced data manipulation and analysis with pandas |
| **postgres-pro** | PostgreSQL administration, optimization, and advanced features |
| **sql-pro** | Expert SQL across multiple database engines |

### Architecture & Design (4 skills)

| Skill | Description |
|-------|-------------|
| **api-designer** | RESTful and RPC API design patterns and best practices |
| **architecture-designer** | Software architecture patterns and system design |
| **graphql-architect** | GraphQL schema design, resolvers, and federation |
| **microservices-architect** | Microservices patterns, orchestration, and service mesh |

### Cloud & Infrastructure (5 skills)

| Skill | Description |
|-------|-------------|
| **cloud-architect** | Multi-cloud architecture and cloud-native design patterns |
| **devops-engineer** | CI/CD pipelines, infrastructure automation, and DevOps practices |
| **kubernetes-specialist** | Kubernetes cluster management, deployments, and operators |
| **sre-engineer** | Site reliability engineering, observability, and incident response |
| **terraform-engineer** | Infrastructure as Code with Terraform across cloud providers |

### Quality & Security (6 skills)

| Skill | Description |
|-------|-------------|
| **code-documenter** | Technical documentation, API docs, and code comments |
| **code-reviewer** | Code review best practices and quality assessment |
| **debugging-wizard** | Advanced debugging techniques across languages and platforms |
| **secure-code-guardian** | Secure coding practices and vulnerability prevention |
| **security-reviewer** | Security audits, threat modeling, and compliance |
| **test-master** | Comprehensive testing strategies: unit, integration, E2E |

### Specialized (10 skills)

| Skill | Description |
|-------|-------------|
| **cli-developer** | Command-line tool development and CLI UX patterns |
| **feature-forge** | Feature development workflow and implementation patterns |
| **fine-tuning-expert** | LLM fine-tuning, prompt engineering, and model optimization |
| **fullstack-guardian** | Full-stack development oversight and architecture |
| **legacy-modernizer** | Legacy code modernization and technical debt reduction |
| **mcp-developer** | Model Context Protocol server development and integration |
| **monitoring-expert** | Application monitoring, metrics, alerting, and observability |
| **playwright-expert** | (See above in Utilities section) |
| **prompt-engineer** | LLM prompt design, optimization, and evaluation |
| **websocket-engineer** | Real-time communication with WebSocket patterns |

---

## Enterprise & Official Skills

> *"The great workshops share their blueprints — wisdom forged in the fires of industry."*

### Skills by Vercel Engineering Team (8 skills)

| Skill | Description |
|-------|-------------|
| **react-best-practices** | React best practices and patterns (`vercel-labs/react-best-practices`) |
| **vercel-deploy-claimable** | Deploy projects to Vercel (`vercel-labs/vercel-deploy-claimable`) |
| **web-design-guidelines** | Web design guidelines and standards (`vercel-labs/web-design-guidelines`) |
| **composition-patterns** | React component composition and reusable patterns (`vercel-labs/composition-patterns`) |
| **next-best-practices** | Next.js best practices and recommended patterns (`vercel-labs/next-best-practices`) |
| **next-cache-components** | Caching strategies and cache-aware components in Next.js (`vercel-labs/next-cache-components`) |
| **next-upgrade** | Upgrade Next.js projects to newer versions (`vercel-labs/next-upgrade`) |
| **react-native-skills** | React Native best practices and performance guidelines (`vercel-labs/react-native-skills`) |

### Skills by Google Labs (Stitch) (6 skills)

*Agent Skills for the Stitch MCP server, compatible with Claude Code, Gemini CLI, Cursor, and more.*

| Skill | Description |
|-------|-------------|
| **design-md** | Create and manage DESIGN.md files (`google-labs-code/design-md`) |
| **enhance-prompt** | Improve prompts with design specs and UI/UX vocabulary (`google-labs-code/enhance-prompt`) |
| **react-components** | Stitch to React components conversion (`google-labs-code/react-components`) |
| **remotion** | Generate walkthrough videos from Stitch app designs (`google-labs-code/remotion`) |
| **shadcn-ui** | Build UI components with shadcn/ui (`google-labs-code/shadcn-ui`) |
| **stitch-loop** | Iterative design-to-code feedback loop (`google-labs-code/stitch-loop`) |

### Security Skills by Trail of Bits Team (22 skills)

| Skill | Description |
|-------|-------------|
| **ask-questions-if-underspecified** | Prompt for clarification on ambiguous requirements (`trailofbits/ask-questions-if-underspecified`) |
| **audit-context-building** | Deep architectural context via ultra-granular code analysis (`trailofbits/audit-context-building`) |
| **building-secure-contracts** | Smart contract security toolkit with vulnerability scanners for 6 blockchains (`trailofbits/building-secure-contracts`) |
| **burpsuite-project-parser** | Search and extract data from Burp Suite project files (`trailofbits/burpsuite-project-parser`) |
| **claude-in-chrome-troubleshooting** | Diagnose and fix Claude in Chrome MCP extension connectivity issues (`trailofbits/claude-in-chrome-troubleshooting`) |
| **constant-time-analysis** | Detect compiler-induced timing side-channels in crypto code (`trailofbits/constant-time-analysis`) |
| **culture-index** | Index and search culture documentation (`trailofbits/culture-index`) |
| **differential-review** | Security-focused diff review with git history analysis (`trailofbits/differential-review`) |
| **dwarf-expert** | DWARF debugging format expertise (`trailofbits/dwarf-expert`) |
| **entry-point-analyzer** | Identify state-changing entry points in smart contracts (`trailofbits/entry-point-analyzer`) |
| **firebase-apk-scanner** | Scan Android APKs for Firebase misconfigurations and security vulnerabilities (`trailofbits/firebase-apk-scanner`) |
| **fix-review** | Verify fix commits address audit findings without new bugs (`trailofbits/fix-review`) |
| **insecure-defaults** | Detect insecure default configurations like hardcoded secrets, default credentials, and weak crypto (`trailofbits/insecure-defaults`) |
| **modern-python** | Modern Python tooling with uv, ruff, ty, and pytest best practices (`trailofbits/modern-python`) |
| **property-based-testing** | Property-based testing for multiple languages and smart contracts (`trailofbits/property-based-testing`) |
| **semgrep-rule-creator** | Create and refine Semgrep rules for vulnerability detection (`trailofbits/semgrep-rule-creator`) |
| **semgrep-rule-variant-creator** | Port existing Semgrep rules to new target languages with test-driven validation (`trailofbits/semgrep-rule-variant-creator`) |
| **sharp-edges** | Identify error-prone APIs and dangerous configurations (`trailofbits/sharp-edges`) |
| **spec-to-code-compliance** | Specification-to-code compliance checker for blockchain audits (`trailofbits/spec-to-code-compliance`) |
| **static-analysis** | Static analysis toolkit with CodeQL, Semgrep, and SARIF (`trailofbits/static-analysis`) |
| **testing-handbook-skills** | Testing Handbook skills: fuzzers, static analysis, sanitizers (`trailofbits/testing-handbook-skills`) |
| **variant-analysis** | Find similar vulnerabilities via pattern-based analysis (`trailofbits/variant-analysis`) |

### Skills by Microsoft — .NET (31 skills)

*Domain-specific knowledge for Azure SDK and Foundry development.*

| Skill | Description |
|-------|-------------|
| **azure-ai-agents-persistent-dotnet** | Persistent AI agents with threads and tools (`microsoft/azure-ai-agents-persistent-dotnet`) |
| **azure-ai-document-intelligence-dotnet** | Document text, table, and data extraction (`microsoft/azure-ai-document-intelligence-dotnet`) |
| **azure-ai-openai-dotnet** | GPT-4, embeddings, DALL-E, and Whisper client (`microsoft/azure-ai-openai-dotnet`) |
| **azure-ai-projects-dotnet** | AI Foundry project management SDK (`microsoft/azure-ai-projects-dotnet`) |
| **azure-ai-voicelive-dotnet** | Real-time bidirectional voice AI (`microsoft/azure-ai-voicelive-dotnet`) |
| **azure-eventgrid-dotnet** | Event Grid topic and domain publishing (`microsoft/azure-eventgrid-dotnet`) |
| **azure-eventhub-dotnet** | High-throughput event streaming (`microsoft/azure-eventhub-dotnet`) |
| **azure-identity-dotnet** | Microsoft Entra ID authentication (`microsoft/azure-identity-dotnet`) |
| **azure-maps-search-dotnet** | Geocoding, routing, and weather services (`microsoft/azure-maps-search-dotnet`) |
| **azure-mgmt-apicenter-dotnet** | API inventory and governance (`microsoft/azure-mgmt-apicenter-dotnet`) |
| **azure-mgmt-apimanagement-dotnet** | API Management provisioning via ARM (`microsoft/azure-mgmt-apimanagement-dotnet`) |
| **azure-mgmt-applicationinsights-dotnet** | Application Insights resource management (`microsoft/azure-mgmt-applicationinsights-dotnet`) |
| **azure-mgmt-arizeaiobservabilityeval-dotnet** | Arize AI observability management (`microsoft/azure-mgmt-arizeaiobservabilityeval-dotnet`) |
| **azure-mgmt-botservice-dotnet** | Bot Service provisioning via ARM (`microsoft/azure-mgmt-botservice-dotnet`) |
| **azure-mgmt-fabric-dotnet** | Microsoft Fabric capacity management (`microsoft/azure-mgmt-fabric-dotnet`) |
| **azure-mgmt-mongodbatlas-dotnet** | MongoDB Atlas as ARM resources (`microsoft/azure-mgmt-mongodbatlas-dotnet`) |
| **azure-mgmt-weightsandbiases-dotnet** | Weights & Biases deployment management (`microsoft/azure-mgmt-weightsandbiases-dotnet`) |
| **azure-resource-manager-cosmosdb-dotnet** | Cosmos DB resource provisioning (`microsoft/azure-resource-manager-cosmosdb-dotnet`) |
| **azure-resource-manager-durabletask-dotnet** | Durable Task Scheduler management (`microsoft/azure-resource-manager-durabletask-dotnet`) |
| **azure-resource-manager-mysql-dotnet** | MySQL Flexible Server management (`microsoft/azure-resource-manager-mysql-dotnet`) |
| **azure-resource-manager-playwright-dotnet** | Playwright Testing workspace management (`microsoft/azure-resource-manager-playwright-dotnet`) |
| **azure-resource-manager-postgresql-dotnet** | PostgreSQL Flexible Server management (`microsoft/azure-resource-manager-postgresql-dotnet`) |
| **azure-resource-manager-redis-dotnet** | Azure Cache for Redis provisioning (`microsoft/azure-resource-manager-redis-dotnet`) |
| **azure-resource-manager-sql-dotnet** | Azure SQL resource management (`microsoft/azure-resource-manager-sql-dotnet`) |
| **azure-search-documents-dotnet** | Full-text, vector, and hybrid search (`microsoft/azure-search-documents-dotnet`) |
| **azure-security-keyvault-keys-dotnet** | Cryptographic key management (`microsoft/azure-security-keyvault-keys-dotnet`) |
| **azure-servicebus-dotnet** | Enterprise messaging with queues and topics (`microsoft/azure-servicebus-dotnet`) |
| **m365-agents-dotnet** | M365, Teams, and Copilot Studio agents (`microsoft/m365-agents-dotnet`) |
| **microsoft-azure-webjobs-extensions-authentication-events-dotnet** | Entra ID custom auth events handler (`microsoft/microsoft-azure-webjobs-extensions-authentication-events-dotnet`) |

### Skills by Microsoft — Python (52 skills)

| Skill | Description |
|-------|-------------|
| **agent-framework-azure-ai-py** | Agent Framework for Azure AI Foundry (`microsoft/agent-framework-azure-ai-py`) |
| **agents-v2-py** | Container-based hosted agents (`microsoft/agents-v2-py`) |
| **azure-ai-contentsafety-py** | Harmful content detection (`microsoft/azure-ai-contentsafety-py`) |
| **azure-ai-contentunderstanding-py** | Multimodal content extraction (`microsoft/azure-ai-contentunderstanding-py`) |
| **azure-ai-ml-py** | Azure ML workspace and job management (`microsoft/azure-ai-ml-py`) |
| **azure-ai-projects-py** | AI Foundry project client and agents (`microsoft/azure-ai-projects-py`) |
| **azure-ai-textanalytics-py** | NLP: sentiment, entities, key phrases (`microsoft/azure-ai-textanalytics-py`) |
| **azure-ai-transcription-py** | Speech-to-text transcription (`microsoft/azure-ai-transcription-py`) |
| **azure-ai-translation-document-py** | Batch document translation (`microsoft/azure-ai-translation-document-py`) |
| **azure-ai-translation-text-py** | Real-time text translation (`microsoft/azure-ai-translation-text-py`) |
| **azure-ai-vision-imageanalysis-py** | Image captions, tags, OCR, objects (`microsoft/azure-ai-vision-imageanalysis-py`) |
| **azure-ai-voicelive-py** | Real-time bidirectional voice AI (`microsoft/azure-ai-voicelive-py`) |
| **azure-appconfiguration-py** | Feature flags and dynamic settings (`microsoft/azure-appconfiguration-py`) |
| **azure-containerregistry-py** | Container image and registry management (`microsoft/azure-containerregistry-py`) |
| **azure-cosmos-db-py** | Cosmos DB with Python/FastAPI patterns (`microsoft/azure-cosmos-db-py`) |
| **azure-cosmos-py** | Cosmos DB NoSQL client library (`microsoft/azure-cosmos-py`) |
| **azure-data-tables-py** | NoSQL key-value table storage (`microsoft/azure-data-tables-py`) |
| **azure-eventgrid-py** | Event-driven pub/sub routing (`microsoft/azure-eventgrid-py`) |
| **azure-eventhub-py** | High-throughput event streaming (`microsoft/azure-eventhub-py`) |
| **azure-identity-py** | Microsoft Entra ID authentication (`microsoft/azure-identity-py`) |
| **azure-keyvault-py** | Secrets, keys, and certificate management (`microsoft/azure-keyvault-py`) |
| **azure-messaging-webpubsubservice-py** | Real-time WebSocket messaging (`microsoft/azure-messaging-webpubsubservice-py`) |
| **azure-mgmt-apicenter-py** | API inventory and governance (`microsoft/azure-mgmt-apicenter-py`) |
| **azure-mgmt-apimanagement-py** | API Management service administration (`microsoft/azure-mgmt-apimanagement-py`) |
| **azure-mgmt-botservice-py** | Bot Service resource management (`microsoft/azure-mgmt-botservice-py`) |
| **azure-mgmt-fabric-py** | Microsoft Fabric capacity management (`microsoft/azure-mgmt-fabric-py`) |
| **azure-monitor-ingestion-py** | Custom log ingestion to Azure Monitor (`microsoft/azure-monitor-ingestion-py`) |
| **azure-monitor-opentelemetry-exporter-py** | OpenTelemetry export to Application Insights (`microsoft/azure-monitor-opentelemetry-exporter-py`) |
| **azure-monitor-opentelemetry-py** | One-line Application Insights setup (`microsoft/azure-monitor-opentelemetry-py`) |
| **azure-monitor-query-py** | Query Azure Monitor logs and metrics (`microsoft/azure-monitor-query-py`) |
| **azure-search-documents-py** | Full-text, vector, and hybrid search (`microsoft/azure-search-documents-py`) |
| **azure-servicebus-py** | Enterprise messaging with queues and topics (`microsoft/azure-servicebus-py`) |
| **azure-speech-to-text-rest-py** | REST speech-to-text for short audio (`microsoft/azure-speech-to-text-rest-py`) |
| **azure-storage-blob-py** | Blob object storage client (`microsoft/azure-storage-blob-py`) |
| **azure-storage-file-datalake-py** | Hierarchical data lake storage (`microsoft/azure-storage-file-datalake-py`) |
| **azure-storage-file-share-py** | SMB file share management (`microsoft/azure-storage-file-share-py`) |
| **azure-storage-queue-py** | Simple message queuing (`microsoft/azure-storage-queue-py`) |
| **fastapi-router-py** | FastAPI routers with CRUD and auth (`microsoft/fastapi-router-py`) |
| **hosted-agents-v2-py** | Container-based hosted agents (`microsoft/hosted-agents-v2-py`) |
| **m365-agents-py** | M365, Teams, and Copilot Studio agents (`microsoft/m365-agents-py`) |
| **pydantic-models-py** | Pydantic models for API schemas (`microsoft/pydantic-models-py`) |

### Skills by Microsoft — TypeScript (25 skills)

| Skill | Description |
|-------|-------------|
| **azure-ai-contentsafety-ts** | Content safety for text and images (`microsoft/azure-ai-contentsafety-ts`) |
| **azure-ai-document-intelligence-ts** | Document text and table extraction (`microsoft/azure-ai-document-intelligence-ts`) |
| **azure-ai-projects-ts** | AI Foundry project client and agents (`microsoft/azure-ai-projects-ts`) |
| **azure-ai-translation-ts** | Text and document translation (`microsoft/azure-ai-translation-ts`) |
| **azure-ai-voicelive-ts** | Real-time bidirectional voice AI (`microsoft/azure-ai-voicelive-ts`) |
| **azure-appconfiguration-ts** | App config, feature flags, dynamic refresh (`microsoft/azure-appconfiguration-ts`) |
| **azure-cosmos-ts** | Cosmos DB NoSQL CRUD and queries (`microsoft/azure-cosmos-ts`) |
| **azure-eventhub-ts** | High-throughput event streaming (`microsoft/azure-eventhub-ts`) |
| **azure-identity-ts** | Microsoft Entra ID authentication (`microsoft/azure-identity-ts`) |
| **azure-keyvault-keys-ts** | Cryptographic key management (`microsoft/azure-keyvault-keys-ts`) |
| **azure-keyvault-secrets-ts** | Secret storage and retrieval (`microsoft/azure-keyvault-secrets-ts`) |
| **azure-microsoft-playwright-testing-ts** | Playwright tests at scale on Azure (`microsoft/azure-microsoft-playwright-testing-ts`) |
| **azure-monitor-opentelemetry-ts** | Application Insights tracing and metrics (`microsoft/azure-monitor-opentelemetry-ts`) |
| **azure-postgres-ts** | PostgreSQL Flexible Server connection (`microsoft/azure-postgres-ts`) |
| **azure-search-documents-ts** | Vector/hybrid search with semantic ranking (`microsoft/azure-search-documents-ts`) |
| **azure-servicebus-ts** | Messaging with queues and topics (`microsoft/azure-servicebus-ts`) |
| **azure-storage-blob-ts** | Blob upload, download, and management (`microsoft/azure-storage-blob-ts`) |
| **azure-storage-file-share-ts** | SMB file share operations (`microsoft/azure-storage-file-share-ts`) |
| **azure-storage-queue-ts** | Queue message operations (`microsoft/azure-storage-queue-ts`) |
| **azure-web-pubsub-ts** | Real-time WebSocket pub/sub messaging (`microsoft/azure-web-pubsub-ts`) |
| **frontend-ui-dark-ts** | Dark-themed React with Tailwind and animations (`microsoft/frontend-ui-dark-ts`) |
| **m365-agents-ts** | M365, Teams, and Copilot Studio agents (`microsoft/m365-agents-ts`) |
| **react-flow-node-ts** | React Flow node components with Zustand (`microsoft/react-flow-node-ts`) |
| **zustand-store-ts** | Zustand stores with middleware patterns (`microsoft/zustand-store-ts`) |

### Skills by Microsoft — General (5 skills)

| Skill | Description |
|-------|-------------|
| **azd-deployment** | Azure Container Apps deployment with azd (`microsoft/azd-deployment`) |
| **github-issue-creator** | Structured GitHub issue reports from notes (`microsoft/github-issue-creator`) |
| **mcp-builder** | MCP server creation guide (`microsoft/mcp-builder`) |
| **podcast-generation** | AI podcast audio with GPT Realtime Mini (`microsoft/podcast-generation`) |
| **skill-creator** | Skill creation guide for Azure AI agents (`microsoft/skill-creator`) |

### Official Claude Skills by Anthropic (17 skills)

| Skill | Description |
|-------|-------------|
| **docx** | Create, edit, and analyze Word documents (`anthropics/docx`) |
| **doc-coauthoring** | Collaborative document editing and co-authoring (`anthropics/doc-coauthoring`) |
| **pptx** | Create, edit, and analyze PowerPoint presentations (`anthropics/pptx`) |
| **xlsx** | Create, edit, and analyze Excel spreadsheets (`anthropics/xlsx`) |
| **pdf** | Extract text, create PDFs, and handle forms (`anthropics/pdf`) |
| **algorithmic-art** | Create generative art using p5.js with seeded randomness (`anthropics/algorithmic-art`) |
| **canvas-design** | Design visual art in PNG and PDF formats (`anthropics/canvas-design`) |
| **frontend-design** | Frontend design and UI/UX development tools (`anthropics/frontend-design`) |
| **slack-gif-creator** | Create animated GIFs optimized for Slack size constraints (`anthropics/slack-gif-creator`) |
| **theme-factory** | Style artifacts with professional themes or generate custom themes (`anthropics/theme-factory`) |
| **web-artifacts-builder** | Build complex claude.ai HTML artifacts with React and Tailwind (`anthropics/web-artifacts-builder`) |
| **mcp-builder** | Create MCP servers to integrate external APIs and services (`anthropics/mcp-builder`) |
| **webapp-testing** | Test local web applications using Playwright (`anthropics/webapp-testing`) |
| **brand-guidelines** | Apply Anthropic's brand colors and typography to artifacts (`anthropics/brand-guidelines`) |
| **internal-comms** | Write status reports, newsletters, and FAQs (`anthropics/internal-comms`) |
| **skill-creator** | Guide for creating skills that extend Claude's capabilities (`anthropics/skill-creator`) |
| **template** | Basic template for creating new skills (`anthropics/template`) |

### Skills by Sentry Team (7 skills)

| Skill | Description |
|-------|-------------|
| **agents-md** | Generate and manage AGENTS.md files (`getsentry/agents-md`) |
| **claude-settings-audit** | Audit Claude settings configuration (`getsentry/claude-settings-audit`) |
| **code-review** | Perform code reviews (`getsentry/code-review`) |
| **commit** | Create commits with best practices (`getsentry/commit`) |
| **create-pr** | Create pull requests (`getsentry/create-pr`) |
| **find-bugs** | Find and identify bugs in code (`getsentry/find-bugs`) |
| **iterate-pr** | Iterate on pull request feedback (`getsentry/iterate-pr`) |

---

## Long-Term Vision

> *"The ultimate forge needs no smith — it reads the blueprint and shapes the metal itself."*

### Near-Term (Post Phase 7)
- **Complete the Olympian Council**: Summon the remaining 8 Olympian agents (Zeus, Hera, Athena, Apollo, Artemis, Aphrodite, Hermes, Demeter)
- **New skill domains**: React, Vue, Go, Rust code review
- **Advanced command chains**: Multi-step automated workflows with rollback
- **Agent collaboration**: Multiple agents coordinating on complex tasks
- **More MCP integrations**: Expanding the external knowledge network
- **Enterprise skill adoption**: Integrate selected skills from Vercel, Google Labs, Trail of Bits, Microsoft, and Anthropic catalogs

### Mid-Term
- **The Olympian Council in session**: All 12 Olympians actively collaborating on complex engineering challenges
- **Self-improving skills**: Skills that analyze their own output quality and refine themselves
- **Autonomous memory curation**: Memory that self-organizes, merges, and prunes without intervention
- **Cross-project learning**: Insights from one project improving analysis of similar projects
- **Divine delegation patterns**: Zeus orchestrating multi-agent workflows with strategic task distribution

### Long-Term
- **Fully autonomous forge**: Agents self-organize to solve complex engineering challenges end-to-end
- **Predictive engineering**: The Factory anticipates needs before they're articulated
- **Multi-forge federation**: Multiple Forge instances sharing knowledge across organizations

---

## Forge Chronicle

Key milestones in the Factory's history:

| Date | Milestone |
|------|-----------|
| **Feb 11, 2026** | Olympian Council Expansion — Planned 8 remaining Olympian agents (Zeus, Hera, Athena, Apollo, Artemis, Aphrodite, Hermes, Demeter) |
| **Feb 11, 2026** | Enterprise Skills Catalog — Documented 173 skills from Vercel, Google Labs, Trail of Bits, Microsoft, Anthropic, Sentry |
| **Feb 12, 2026** | Phase 8 — The Proving Grounds (Phase 1+2) — ~1,300 static validation tests across 10 test files |
| **Feb 11, 2026** | Testing Roadmap — Comprehensive testing architecture with 6 phases and ~300 tests planned |
| **Feb 11, 2026** | Community Skills Catalog — Documented 99+ planned skills across 15 domains |
| **Feb 11, 2026** | Phase 7 — The Grand Reforging — Complete documentation rewrite |
| **Feb 11, 2026** | Phase 6 — The Anvil — 20 hooks across 9 events and 4 layers |
| **Feb 11, 2026** | Phase 5 — Optimization & Hardening — Cached context, shared patterns, future adapters |
| **Feb 10, 2026** | Phase 4 — Interface migration complete (22 skills, 12 commands, 11 agents migrated) |
| **Feb 10, 2026** | MCP Integration — 8 external knowledge conduits connected |
| **Feb 10, 2026** | Infrastructure — Hooks, loading protocol, memory lifecycle, quality guidance |
| **Feb 10, 2026** | Commands Phase 2 — 5 new commands (/remember, /mock, /azure-pipeline, /etl-pipeline, /azure-function) |
| **Feb 9, 2026** | Commands Phase 1 — 7 commands (/analyze, /implement, /improve, /document, /test, /build, /brainstorm) |
| **Feb 9, 2026** | Divine Council — 4 Olympian agents summoned (Hephaestus, Prometheus, Ares, Poseidon) |
| **Feb 9, 2026** | Specialist agents — Python Engineer, Frontend Engineer, Developer Environment Engineer |
| **Feb 9, 2026** | Meta-skill — generate-more-skills-with-claude for autonomous skill creation |
| **Feb 6, 2026** | Data Science & Productivity — 6 skills (excel, jupyter, commit-helper, email, slack, docs) |
| **Feb 6, 2026** | Dev Environment — generate-tilt-dev-environment, generate-mock-service |
| **Feb 6, 2026** | Schema Analysis — file-schema-analysis, database-schema-analysis |
| **Nov 18, 2025** | Azure Functions — generate-azure-functions with Tilt + Azurite |
| **Nov 14, 2025** | .NET Code Review — dotnet-code-review with 12 context files |

---

*Last Updated: February 12, 2026*
*Maintained by: The Forge Keepers*

*Forged by Hephaestus. Tempered by experience. Worthy of Olympus.*
