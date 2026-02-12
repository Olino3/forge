# ⚒️ The Forge — Roadmap

> *"Hephaestus's forge never cools. Each skill sharpened, each agent awakened, each command invoked brings us closer to the perfect workshop — where mortal developers wield divine tools."*

---

## The Factory Today

The Forge is a fully operational **Agentic Software Factory** — a Claude Code plugin built on convention, powered by 4 core interfaces, and staffed by a pantheon of divine agents.

### What's Forged and Ready

| Component | Count | Status |
|-----------|-------|--------|
| **Skills** | 27 | ✅ All operational, interface-based |
| **Commands** | 12 | ✅ All operational, interface-based |
| **Agents** | 19 | ✅ 12 Olympian + 7 specialist, all with config.json |
| **Context Files** | 81 | ✅ 9 domains, all with YAML frontmatter |
| **Interfaces** | 4 | ✅ ContextProvider, MemoryStore, SkillInvoker, ExecutionContext |
| **Adapters** | 3 | ✅ MarkdownFileContextProvider, MarkdownFileMemoryAdapter, CachedContextProvider |
| **Hooks** | 20 | ✅ 9 events, 4 layers (Shield, Chronicle, Foreman, Town Crier) |
| **MCP Servers** | 8 | ✅ Connected external conduits |

### The Pantheon (Active Agents)

**Olympian Tier** — @zeus (orchestration), @hera (governance), @athena (architecture), @apollo (quality), @artemis (testing), @aphrodite (UX/UI), @hermes (integration), @demeter (data cultivation), @hephaestus (tool creation), @prometheus (strategy), @ares (deployment), @poseidon (data flow)

**Specialist Legion** — @python-engineer, @frontend-engineer, @devops-engineer, @developer-environment-engineer, @data-scientist, @full-stack-engineer, @technical-writer

### The Armory (Active Skills)

**Code Review** — python-code-review · dotnet-code-review · angular-code-review · get-git-diff

**Test Generation** — generate-python-unit-tests · generate-jest-unit-tests · test-cli-tools

**Infrastructure** — generate-azure-functions · generate-azure-pipelines · generate-azure-bicep · generate-tilt-dev-environment · generate-mock-service

**Analysis** — file-schema-analysis · database-schema-analysis · python-dependency-management

**Programming Languages** — cpp · csharp · java-architect · javascript · typescript

**Productivity** — commit-helper · email-writer · slack-message-composer · documentation-generator

**Data Science** — excel-skills · jupyter-notebook-skills

**Meta** — generate-more-skills-with-claude

### The War Room (Active Commands)

`/analyze` · `/implement` · `/improve` · `/document` · `/test` · `/build` · `/brainstorm` · `/remember` · `/mock` · `/azure-pipeline` · `/etl-pipeline` · `/azure-function`

---

## Planned Skills

> *"The blueprints are drawn — these weapons await their turn at the anvil."*

### Frontend & UI (15 skills)

| Skill | Description |
|-------|-------------|
| **accessibility** | Build WCAG 2.1 AA compliant websites with semantic HTML, proper ARIA, focus management, and screen reader support. Includes color contrast (4.5:1 text), keyboard navigation, form labels, and live regions. |
| **animate** | Zero-config animations for React, Vue, Solid, Svelte, Preact with @formkit/auto-animate (3.28kb). Prevents 15 errors. |
| **nextjs** | Build Next.js 16 apps with App Router, Server Components/Actions, Cache Components ("use cache"), and async route params. Includes proxy.ts and React 19.2. Prevents 25 errors. |
| **react-forms** | Build type-safe validated forms using React Hook Form v7 and Zod v4. Single schema works on client and server with full TypeScript inference via `z.infer`. |
| **responsive-images** | Implement performant responsive images with srcset, sizes, lazy loading, and modern formats (WebP, AVIF). Covers aspect-ratio for CLS prevention, picture element for art direction, and fetchpriority. Triggers: `srcset`, `loading=`, `lazy`, `eager` |
| **tailwind-patterns** | Production-ready Tailwind CSS patterns for common website components: responsive layouts, cards, navigation, forms, buttons, and typography. Includes spacing scale, breakpoints, mobile-first patterns. Triggers: `Tailwind CSS`, `CSS utility classes`, `first CSS`, `shadcn/ui components` |
 
### Authentication (5 skills)

| Skill | Description |
|-------|-------------|
| **azure-auth** | Microsoft Entra ID (Azure AD) authentication for React SPAs with MSAL.js and Cloudflare Workers JWT validation using jose library. Full-stack pattern with Authorization Code Flow + PKCE. Prevents 8 errors. |
| **better-auth** | Self-hosted auth for TypeScript/Cloudflare Workers with social auth, 2FA, passkeys, organizations, RBAC, and 15+ plugins. Requires Drizzle ORM or Kysely for D1 (no direct adapter). Triggers: `better-auth`, `authentication with D1`, `Cloudflare D1 auth setup` |
| **clerk-auth** | Clerk auth with API Keys beta (Dec 2025), Next.js 16 proxy.ts (March 2025 CVE context), API version 2025-11-10 breaking changes, clerkMiddleware() options, webhooks, production considerations. Prevents 15 errors. Triggers: `clerk`, `clerk auth`, `@clerk/nextjs` |
| **firebase-auth** | Build with Firebase Authentication — email/password, OAuth providers, phone auth, and custom tokens. Use when: setting up auth flows, implementing sign-in/sign-up, managing user sessions, protecting routes. Prevents 12 errors. |
| **oauth-integrations** | Implement OAuth 2.0 authentication with GitHub, Okta, Google, and Microsoft Entra (Azure AD) ||

### Database & Storage (6 skills)

| Skill | Description |
|-------|-------------|
| **firebase-firestore** | Build with Firestore NoSQL database — real-time sync, offline support, and scalable document storage. Use when: creating collections, querying documents, setting up security rules, handling real-time updates. Prevents 10 errors. |
| **firebase-storage** | Build with Firebase Cloud Storage — file uploads, downloads, and secure access. Use when: uploading images/files, generating download URLs, implementing file pickers, setting up storage security rules. Prevents 9 errors. |
| **neon-vercel-postgres** | Set up serverless Postgres with Neon or Vercel Postgres for Cloudflare Workers/Edge. Includes connection pooling, git-like branching, and Drizzle ORM integration. |
| **snowflake-platform** | Build on Snowflake's AI Data Cloud with snow CLI, Cortex AI (COMPLETE, SUMMARIZE, AI_FILTER), Native Apps, and Snowpark. Covers JWT auth, account identifiers, Marketplace publishing. Prevents 11 errors. Triggers: `snowflake`, `snow cli`, `snowflake connection` |
| **vercel-blob** | Integrate Vercel Blob for file uploads and CDN-delivered assets in Next.js. Supports client-side uploads with presigned URLs and multipart transfers for large files. Prevents 16 errors. Triggers: `@vercel/blob`, `vercel blob`, `vercel file upload` |
| **vercel-kv** | Integrate Redis-compatible Vercel KV for caching, session management, and rate limiting in Next.js. Powered by Upstash with strong consistency and TTL support. Triggers: `@vercel/kv`, `vercel kv`, `upstash vercel` |

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

### Developer Workflow (3 skills)

| Skill | Description |
|-------|-------------|
| **create-agents** | Design and build custom Claude Code agents with effective descriptions, tool access patterns, and delegation strategies. Triggers: `create agent`, `custom agent`, `build agent`, `agent description` |
| **power-debug** | Multi-agent investigation for stubborn bugs. Use when: going in circles debugging, need to investigate browser/API interactions, complex bugs resisting normal debugging, or when symptoms don't match expectations. |
| **dev-tools** | Essential development workflow agents for code review, debugging, testing, documentation, and git operations. Triggers: `step` |

### Backend & Frameworks (6 skills)

| Skill | Description |
|-------|-------------|
| **django** | Expert-level Django development patterns and best practices |
| **dotnet-core** | .NET Core/ASP.NET Core architecture and implementation |
| **fastapi** | Modern Python API development with FastAPI framework |
| **nestjs** | Enterprise-grade NestJS applications with TypeScript |
| **rails** | Ruby on Rails application development and architecture |
| **php** | Professional PHP development patterns and frameworks |

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

### Data & Database (4 skills)

| Skill | Description |
|-------|-------------|
| **database-optimizer** | SQL query optimization, indexing, and performance tuning |
| **pandas** | Advanced data manipulation and analysis with pandas |
| **postgres** | PostgreSQL administration, optimization, and advanced features |
| **sql** | Expert SQL across multiple database engines |

### Architecture & Design (4 skills)

| Skill | Description |
|-------|-------------|
| **api-design** | RESTful and RPC API design patterns and best practices |
| **architecture-design** | Software architecture patterns and system design |
| **graphql-design** | GraphQL schema design, resolvers, and federation |
| **microservices-design** | Microservices patterns, orchestration, and service mesh |

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
| **debugging-expert** | Advanced debugging techniques across languages and platforms |
| **secure-code** | Secure coding practices and vulnerability prevention |
| **security-reviewer** | Security audits, threat modeling, and compliance |
| **testing** | Comprehensive testing strategies: unit, integration, E2E |

### Specialized (10 skills)

| Skill | Description |
|-------|-------------|
| **cli-developer** | Command-line tool development and CLI UX patterns |
| **feature-forge** | Feature development workflow and implementation patterns |
| **fullstack-development** | Full-stack development oversight and architecture |
| **legacy-modernizer** | Legacy code modernization and technical debt reduction |
| **mcp-developer** | Model Context Protocol server development and integration |
| **monitoring-expert** | Application monitoring, metrics, alerting, and observability |
| **playwright-expert** | (See above in Utilities section) |
| **prompt-engineer** | LLM prompt design, optimization, and evaluation |
| **websocket-engineer** | Real-time communication with WebSocket patterns |

---

## Planned Commands

> *"New incantations to invoke the divine powers — commands that guide the forge's mighty hand."*

| Command | Description |
|---------|-------------|
| **/divine** | Analyze the codebase and suggest possible workflows and cookbooks with commands, skills, and agents from the forge-plugin. Recommends strategies and techniques to integrate agentic coding into the codebase using The Forge plugin. Entry point for discovering optimal forge patterns for your specific project. |

---

## Planned Hooks

> *"The watchers and keepers — hooks that guard the gates of knowledge and wisdom."*

### Memory & Context Management (User-Triggered)

| Hook Event | Description |
|------------|-------------|
| **on_user_prompt** | Load relevant memory and context when user initiates a prompt, ensuring the agent has access to prior learnings and project-specific knowledge |
| **on_skill_use** | Store insights, patterns, and outcomes when skills are invoked, building a knowledge base of what works in this project |

### External Plugin Integration

| Hook Event | Description |
|------------|-------------|
| **on_external_skill_load** | Integrate Forge's memory and context management for skills from other Claude Code plugins, enabling unified knowledge sharing |
| **on_external_skill_complete** | Capture and store learnings from external plugin skills into Forge's memory system for future reference |

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
- **New skill domains**: React, Vue, Go, Rust code review
- **Advanced command chains**: Multi-step automated workflows with rollback
- **Agent collaboration**: Multiple agents coordinating on complex tasks
- **More MCP integrations**: Expanding the external knowledge network
- **Enterprise skill adoption**: Integrate selected skills from Vercel, Google Labs, Trail of Bits, Microsoft, and Anthropic catalogs

### Mid-Term
- **Advanced Olympian Council workflows**: All 12 Olympians actively collaborating on complex engineering challenges with sophisticated delegation patterns
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

Current state and recent milestones:

| Date | Milestone |
|------|-----------|
| **Feb 12, 2026** | Roadmap Expansion — Added `/divine` command and 4 new hook events for memory/context integration |
| **Feb 12, 2026** | Factory Stable — 22 skills, 12 commands, 11 agents, 81 context files, 20 hooks, ~1,683 tests |
| **Feb 11, 2026** | Enterprise Skills Catalog — Documented 173 skills from Vercel, Google Labs, Trail of Bits, Microsoft, Anthropic, Sentry |
| **Feb 11, 2026** | Community Skills Catalog — Documented 99+ planned skills across 15 domains |
| **Feb 10, 2026** | MCP Integration — 8 external knowledge conduits connected |
| **Nov 18, 2025** | Azure Functions — generate-azure-functions with Tilt + Azurite |
| **Nov 14, 2025** | .NET Code Review — dotnet-code-review with 12 context files |

---

*Last Updated: February 12, 2026*
*Maintained by: The Forge Keepers*

*Forged by Hephaestus. Tempered by experience. Worthy of Olympus.*
