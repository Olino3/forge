# ⚒️ The Forge — Roadmap

> *"Hephaestus's forge never cools. Each skill sharpened, each agent awakened, each command invoked brings us closer to the perfect workshop — where mortal developers wield divine tools."*

**Current Version**: `0.3.0-alpha` · **Target**: Beta · **Versioning**: Alpha bumps increment minor by 1 — versions track state, not scope. Focus is velocity.

Each milestone maps 1:1 to a [GitHub Milestone](https://github.com/Olino3/forge/milestones). This roadmap always details the next two milestones; remaining milestones carry goal-level plans until they enter the detail window.

---

## Beta Vision

> *"What survives the furnace of alpha is worthy of the hands of mortals."*

Beta graduation means the Forge is **reliable, measurable, and portable**. The system exits alpha when:

| Criterion | Measurement |
|-----------|-------------|
| **Agent reliability** | All 19 agents reliably complete their designated tasks (≥80% session quality score) |
| **Skill completeness** | All core skills pass deterministic + mocked tests with full 6-step workflow compliance |
| **Memory/context reliability** | No data loss, no stale reads, hook-enforced lifecycle across all operations |
| **Measurable quality** | Every session produces quality scores; trends are trackable across sessions |
| **Multi-platform** | Works on Claude Code (native) AND GitHub Copilot (via transpiled adapters) |
| **Installable** | External contributors can install, configure, and use the system with documented onboarding |
| **Secure** | Layer 3 security tests all pass |
| **No critical bugs** | Zero critical issues open for >7 days |

**Beta version**: TBD — determined after v0.8.0-alpha based on quality data readiness. Could be v0.9.0-beta or later.

---

## Current State — v0.3.0-alpha

> *"The workshop stands. The tools are forged. Now they must be tempered."*

| Component | Count | Status |
|-----------|-------|--------|
| Core skills | 102 | Forged, not all verified for 6-step compliance |
| External skills (marketplace) | 212 across 38 plugins | Documented, symlinks validated |
| Agents | 19 (12 Olympian + 7 specialist) | Configs exist, not all populate `skills[]` |
| Commands | 12 | Formatted, not all tested in Claude Code |
| Context files | 81 across 9 domains | YAML frontmatter validated (Layer 1) |
| Hooks | 20 across 9 events, 4 layers | Registered, Layer 2 tested |
| MCP integrations | 8 servers | Documented with activation protocol |
| Agentic workflows | 19 operational | Compiled, not all dispatch-tested |
| Tests | ~1,993 across 2 layers + E2E | Layer 1 CI-ready, Layer 2/E2E gated |
| Interfaces | 4 (specification-only) | Convention-based, not enforced |

### Known Gaps

- Agent configs have empty `skills: []` arrays (Athena and others)
- Skills reference `contextProvider.*`/`memoryStore.*` — but enforcement is honor-system
- Layer 3 security testing: described but no test files exist
- `TESTING_ROADMAP.md` referenced in CLAUDE.md but missing
- Document count inconsistencies (19 vs 22 workflows across docs)
- Telemetry is local-only, no cross-session aggregation
- No quality scoring baseline established

---

## Milestone: v0.4.0-alpha — Foundation Hardening

> *"Before the blade can cut, the steel must be folded a thousand times."*

**Theme**: Everything works. Hooks enforce it. Tests prove it.

**GitHub Milestone**: [`v0.4.0-alpha`](https://github.com/Olino3/forge/milestone/v0.4.0-alpha)

---

### 1. Agent Compliance Audit

Verify every agent meets the Forge contract.

| Task | Acceptance Criteria |
|------|-------------------|
| Validate all 19 agent `.config.json` files against `agent_config.schema.json` | All pass schema validation |
| Populate empty `skills[]` — every agent declares ≥1 skill | No agent has `skills: []` |
| Verify every agent `.md` includes all 6 workflow steps (Initial Analysis → Load Memory → Load Context → Core Action → Generate Output → Update Memory) | All 19 agent `.md` files contain all 6 steps |
| Verify `context.primaryDomains`, `context.alwaysLoadFiles`, `memory.storagePath`, `memory.categories` are correctly populated | All required fields present and valid |

**Requirements**: Audit tooling (Layer 1 test `test_cross_references.py` can be extended)

---

### 2. Skill Compliance Audit

Ensure all 102 core skills follow the 6-step mandatory workflow.

| Task | Acceptance Criteria |
|------|-------------------|
| Validate every `SKILL.md` against `SKILL_TEMPLATE.md` structure | All skills match template sections |
| Verify YAML frontmatter includes `context.primary_domain`, `context.file_budget`, `memory.scopes` | Frontmatter validates for all 102 skills |
| Verify each skill uses `contextProvider.*` and `memoryStore.*` interface references — no raw file paths | Zero hardcoded paths in workflow steps |
| Ensure every skill directory has both `SKILL.md` and `examples.md` | 102/102 directories complete |

**Requirements**: Extend `test_file_structure.py` and `test_yaml_frontmatter.py`

---

### 3. Command & Agent Formatting for Claude Code

Verify commands and agents render correctly in Claude Code's interface.

| Task | Acceptance Criteria |
|------|-------------------|
| Verify all 12 commands are invokable via `/command` in Claude Code | Documented with invocation logs for each command |
| Verify `@agent` mentions in command workflows resolve correctly | Agent delegation works for all referenced agents |
| Verify `skill:{name}` delegation syntax in command workflow steps | Skill delegation invokes the correct skill |
| Test YAML frontmatter format, trigger syntax, and usage blocks render properly | No formatting errors in Claude Code UI |

**Requirements**: Manual testing with Claude Code; document results per command
**Consideration**: This step requires interactive Claude Code sessions — cannot be fully automated. Create a test checklist and capture invocation evidence.

---

### 4. Hook-Driven Memory & Context Management

Replace direct memory/context file I/O with transparent hook interception. Hooks become the primary mechanism — skills no longer perform raw file reads/writes for memory and context.

#### Architecture

```
Before (v0.3.0):  Skill → direct file I/O → memory/*.md / context/**/*.md
After  (v0.4.0):  Skill → tool call → Hook intercepts → managed I/O → memory/*.md / context/**/*.md
```

| Task | Acceptance Criteria |
|------|-------------------|
| **`PreToolUse(Read)` — context auto-injection**: When a skill's `SKILL.md` is read, hook pre-loads the skill's declared context domains into the session | Context domains from skill frontmatter are available without explicit loading |
| **`PreToolUse(Read)` — memory freshness**: Intercept reads of `memory/*.md` files, inject freshness metadata and relevant cross-domain context automatically | All memory reads include freshness header; stale reads trigger warnings |
| **`PostToolUse(Write|Edit)` — memory lifecycle**: Intercept writes to `memory/` paths, automatically categorize entries, add timestamps, enforce line limits, trigger cross-pollination | Consolidates logic from `memory_quality_gate`, `memory_freshness_enforcer`, `memory_cross_pollinator` |
| **Remove direct I/O from skills**: Skills no longer call `contextProvider.*`/`memoryStore.*` for file operations — hooks handle transparently | Zero direct memory/context file I/O in skill workflow steps |
| **Backward compatibility**: Existing Layer 2 memory tests still pass | All 30 Layer 2 tests green |

**Tradeoffs**:
- **Pro**: Enforcement — skills can't bypass memory/context management
- **Pro**: Centralized logic — one place to audit memory hygiene
- **Con**: Couples to Claude Code's hook event model — skills become less portable (addressed in v0.6.0 via adapters)
- **Con**: Debugging is harder when I/O is implicit — mitigated by adding verbose logging to hooks

**Requirements**: Refactor 3 hooks (`memory_quality_gate`, `memory_freshness_enforcer`, `memory_cross_pollinator`) into a unified interception layer. Update all skill SKILL.md files to remove direct I/O instructions.

---

### 5. Layer 3 Security Testing

Create the security testing infrastructure described in the current roadmap.

| Category | Tests | Acceptance Criteria |
|----------|-------|-------------------|
| **Prompt injection** (4) | skill-injection-scan, context-poisoning-test, output-sanitization, indirect-injection-via-data | Scan all SKILL.md + context files for hijack patterns; verify memory can't inject unauthorized instructions; validate chained output sanitization; test data file injection vectors |
| **Plugin security** (4) | permission-scope-audit, plugin-isolation-test, manifest-tampering-detect, mcp-server-trust-boundary | Verify plugin file access stays within manifest scope; confirm cross-plugin isolation; detect manifest modifications; validate MCP permission boundaries |
| **Supply chain** (4) | submodule-provenance, dependency-drift-detect, skill-content-hash, typosquat-detection | All submodules point to `Olino3/` forks; SHA manifest matches; content hashes stable; no typosquat matches against known packages |

| Infrastructure | Acceptance Criteria |
|---------------|-------------------|
| Create `forge-plugin/tests/layer3/` directory structure | Directory exists with test files |
| Wire into `run_all.sh` with `--layer3` flag | `make test-security` runs Layer 3 |
| Add to CI pipeline | Layer 3 runs on PRs touching hooks, skills, or plugins |

**Requirements**: 12 test files, test runner integration, CI pipeline update

---

### 6. Automated Testing — Deterministic + Mocked

Extend testing beyond static validation to cover actual agent/skill/command behavior.

#### Deterministic Tests (no LLM)

| Test | Validates |
|------|----------|
| Agent→skill resolution | Every agent config's `skills[]` references skills that exist |
| Command→skill resolution | Every command's `skills` frontmatter references existing skills |
| Hook→file pattern matching | Every hook's file pattern matches ≥1 real file in the repo |
| Skill→context resolution | Every skill's declared `context.primary_domain` has files in that context domain |
| Cross-reference integrity | Agent → skill → context → memory chain is fully connected |

#### Mocked LLM Tests (fixture-based)

| Flow | Description |
|------|-------------|
| `/implement` end-to-end | Command invocation → skill delegation → memory write; uses recorded Claude responses from fixture files |
| Agent task completion | Agent receives task → selects skill → produces output → output scored; validate the full chain |
| Hook chain execution | File write triggers PostToolUse hooks in correct order; validate hook JSON stdin/stdout contract |

| Task | Acceptance Criteria |
|------|-------------------|
| Create test fixtures directory with recorded responses | `tests/fixtures/` with ≥3 flow fixtures |
| Build hook event simulator (JSON stdin/stdout mock) | Hook tests run in isolation without Claude Code |
| ≥80% component coverage | 80%+ of agent configs, skills, commands, hooks have ≥1 dedicated test |
| CI performance | Full test suite completes in <5 minutes |

**Consideration**: Mocked tests can drift from real LLM behavior. Fixtures should be refreshed when skills change significantly. Telemetry sampling in v0.5.0 provides a mechanism to auto-generate fresh fixtures.

---

### 7. Metrics & Telemetry Enforcement

Ensure telemetry fires reliably on every session and produces actionable data.

| Task | Acceptance Criteria |
|------|-------------------|
| Verify `forge_telemetry.sh` fires on every session stop | Every session with ≥1 skill/command produces a telemetry entry in `.forge/telemetry.log` |
| Verify `output_quality_scorer.sh` scores every `/claudedocs/` output | All output files have quality metadata blocks |
| Verify `context_usage_tracker.sh` tracks all context loads | `.forge/context_usage.json` reflects actual context usage |
| Create `session_summary` hook (Stop event) | Human-readable session report aggregating telemetry, quality scores, and context usage |
| No silent failures | Telemetry hooks log errors to `.forge/health_buffer` instead of failing silently |

**Requirements**: Validate existing hook scripts handle edge cases (empty sessions, no skills invoked, no output files)

---

### 8. Documentation Hygiene

Fix known inconsistencies and create missing referenced files.

| Task | Acceptance Criteria |
|------|-------------------|
| Create `TESTING_ROADMAP.md` | File exists; referenced from CLAUDE.md and README.md |
| Fix workflow count inconsistencies (19 vs 22 across docs) | Single accurate count across ROADMAP, CLAUDE.md, AGENTIC_FORGE.md |
| Update CLAUDE.md architecture summary counts | Agent count (19), skill count (102), workflow count match reality |
| Verify all internal cross-references resolve | No broken links in `.md` files |

---

### v0.4.0-alpha Completion Criteria

- [ ] All 19 agent configs pass schema validation and reference ≥1 skill
- [ ] All 102 skills validated for 6-step workflow and frontmatter compliance
- [ ] All 12 commands tested and documented in Claude Code
- [ ] Hook-driven memory/context management replaces direct I/O
- [ ] 12 Layer 3 security tests passing
- [ ] ≥80% component test coverage (deterministic + mocked)
- [ ] Telemetry fires on every session; quality scores on all outputs
- [ ] Zero document inconsistencies; all referenced files exist

---

## Milestone: v0.5.0-alpha — Modular Architecture & Quality Signals

> *"The master smith organizes the workshop — each tool in its place, each apprentice with their specialty."*

**Theme**: Break apart the monolith. Scope agent access. Measure quality. Optimize cost.

**GitHub Milestone**: [`v0.5.0-alpha`](https://github.com/Olino3/forge/milestone/v0.5.0-alpha)

---

### 1. 5-Category Plugin Decomposition

Split 102 core skills from monolithic `forge-plugin/skills/` into 5 focused installable plugins plus the core.

| Plugin | Category | Est. Skills | Examples |
|--------|----------|-------------|---------|
| **forge-core** (always installed) | Foundation | — | 19 agents, 12+ commands, hooks, MCPs, interfaces, context, memory |
| **forge-skills-backend** | Backend / API / Data | ~25 | Python, .NET, Java, SQL, Django, FastAPI, ETL, data modeling, database skills |
| **forge-skills-frontend** | Frontend / UI / Mobile | ~18 | React, Angular, Vue, Next.js, Flutter, accessibility, CSS, responsive |
| **forge-skills-quality** | Testing / Security / Review | ~20 | Unit tests, code review, security audit, debugging, refactoring, linting |
| **forge-skills-infra** | DevOps / Cloud / Architecture | ~18 | CI/CD, Docker, K8s, Azure, Terraform, cloud architecture, API design |
| **forge-skills-productivity** | Utilities / Planning / Docs | ~21 | Commit helper, documentation, project planning, office tools, image gen |

| Task | Acceptance Criteria |
|------|-------------------|
| Categorize all 102 skills into 5 categories | Every skill assigned to exactly one category; cross-cutting skills go to primary category |
| Create `plugin.json` for each skill plugin | 5 valid plugin manifests |
| Create `forge-skills-all` meta-plugin | Installs all 5 skill plugins (backward-compatible default) |
| Update `marketplace.json` | New plugins registered; no broken references |
| Migration script | Moves skills without breaking agent/command references |
| Skill name resolution | Core agents resolve skills by name regardless of which plugin provides them |

**Tradeoff**: Skills like `generate-python-unit-tests` span backend and quality. Decision: assign to PRIMARY category (quality for test-gen skills). Document the categorization rationale.

**Requirements**: v0.4.0 complete (skills are validated and compliant before being moved)

---

### 2. Agent Skill & MCP Scoping

Give each agent access to only the skills and MCPs relevant to its domain.

| Task | Acceptance Criteria |
|------|-------------------|
| Add `allowedSkills` (array, glob patterns) to `agent_config.schema.json` | Schema validates; `additionalProperties` constraint updated |
| Add `allowedMcps` (array, MCP server names) to `agent_config.schema.json` | Schema validates |
| Populate all 19 agent configs with scoped skill lists | Every agent declares specific `allowedSkills` |
| Extend `agent_config_validator` hook | Warns when agent attempts out-of-scope skill use |
| Default scope: all skills (backward-compatible) | Existing workflows unchanged |
| Scope escalation via `@zeus` | Zeus can delegate any skill to any agent when orchestrating |

**Scoping examples**:

| Agent | `allowedSkills` | `allowedMcps` |
|-------|----------------|---------------|
| `@python-engineer` | `fastapi, django, pandas, python-*, generate-python-*` | `context7, github` |
| `@frontend-engineer` | `nextjs, react-*, tailwind-*, accessibility, animate, generate-jest-*` | `context7, playwright` |
| `@devops-engineer` | `cloud-*, kubernetes-*, terraform-*, sre-*, generate-azure-*` | `context7, github` |

---

### 3. Session Quality Scoring

Move from per-file quality scores to composite session scoring.

| Task | Acceptance Criteria |
|------|-------------------|
| Create `session_quality_scorer` hook (Stop event) | Fires on session end; produces composite score |
| Score dimensions: task completion, context relevance, memory hygiene, output quality | All 4 dimensions produce sub-scores |
| Composite score (0–100) with thresholds: red (<50), yellow (50–75), green (>75) | Score categorized with actionable feedback |
| Store in `.forge/quality_scores.json` with timestamps | Persistent across sessions; trend-visible |
| Sample session outputs for quality analysis | ≥3 output files sampled per session |

**Consideration**: Scoring is heuristic without LLM evaluation. Calibrate thresholds using real data from v0.4.0 telemetry before enforcing gates.

---

### 4. Token Optimization — Model Routing + Context Reduction

Reduce cost per session through intelligent model selection and context management.

#### Model Routing

| Task | Acceptance Criteria |
|------|-------------------|
| Add `modelOverride` field to skill YAML frontmatter (`opus`, `sonnet`, `haiku`) | Schema supports the field |
| Classify skills: template/scaffold → `haiku`; analytical → `sonnet`; complex reasoning → `opus` | ≥30% of skills have `modelOverride` set |
| Agent `model` field provides default; skill `modelOverride` takes precedence | Precedence documented and tested |

**Consideration**: Claude Code may not support mid-session model switching. If so, model routing operates at agent-level only (already supported via `model` field). Skill-level routing becomes advisory metadata for future platforms.

#### Context Reduction

| Task | Acceptance Criteria |
|------|-------------------|
| Implement lazy context loading — hooks inject only the active domain's context, not all `alwaysLoadFiles` | Context loaded on-demand per domain |
| Add `context_budget` field to skill frontmatter (max files to load) | Skills declare and respect budgets |
| Context summarization for files >200 lines (load headers + summary, full on demand) | Large context files use summary mode by default |

#### Token Tracking

| Task | Acceptance Criteria |
|------|-------------------|
| Add token usage estimation to `forge_telemetry.sh` (approximate from file sizes) | Per-session token estimate in telemetry log |
| Report cost breakdown: context loading vs. skill execution vs. memory I/O | Breakdown visible in session summary |

---

### v0.5.0-alpha Completion Criteria

- [ ] 102 skills distributed across 5 category plugins + core
- [ ] `forge-skills-all` meta-plugin installs everything (backward-compatible)
- [ ] All 19 agents declare `allowedSkills` and `allowedMcps`
- [ ] Agent scope violations produce warnings (not blocks)
- [ ] Every session produces a composite quality score (0–100)
- [ ] ≥30% of skills specify `modelOverride`
- [ ] Context loading respects `context_budget`
- [ ] Token estimates appear in telemetry

---

## Milestone: v0.6.0-alpha — Multi-Platform Compatibility

> *"A weapon forged by Hephaestus serves any warrior who wields it — not just the one who commissioned it."*

**Theme**: Break free from Claude Code exclusivity. GitHub Copilot is the first expansion target.

**GitHub Milestone**: [`v0.6.0-alpha`](https://github.com/Olino3/forge/milestone/v0.6.0-alpha)

### Goals

| Goal | Description |
|------|-------------|
| **Universal Skill Schema** | Platform-agnostic skill definition (JSON/YAML) capturing intent, context, examples, workflow — transpilable to native formats |
| **GitHub Copilot Transpiler** | Convert `SKILL.md` → `.instructions.md` / `.github/copilot-instructions.md`; convert agent configs → Copilot custom instructions |
| **Adapter layer** | Platform adapters in `interfaces/adapters/` translating `SkillInvoker` and `ContextProvider` to platform conventions |
| **Graceful degradation** | Hook-driven memory/context (v0.4.0) is Claude Code-specific; Copilot adapter degrades to read-only context injection or Copilot-native mechanisms |
| **Test matrix** | CI validates transpiled outputs are well-formed for Copilot |

### Target Platforms

| Platform | Skill Format | Agent Format | Priority |
|----------|-------------|-------------|---------|
| **Claude Code** | `SKILL.md` (native) | `.md` + `.config.json` (native) | ✅ Current |
| **GitHub Copilot CLI** | `.instructions.md` / `.github/copilot-instructions.md` | Custom instructions | 🎯 v0.6.0 |
| **Gemini CLI** | `AGENTS.md` + skill files | Agent config files | 🔲 v0.6.0+ |
| **Cursor** | `.cursor/rules/` rule files | Cursor agent rules | 🔲 v0.6.0+ |
| **Codex** (OpenAI) | `AGENTS.md` + instruction files | Agent spec files | 🔲 Future |

### Deliverables

| Deliverable | Description |
|-------------|-------------|
| `forge-export-copilot` | Transpile Forge skills into GitHub Copilot `.instructions.md` files |
| `forge-export-gemini` | Generate Gemini CLI-compatible `AGENTS.md` and skill files |
| `forge-export-cursor` | Convert Forge skills into Cursor `.cursor/rules/` rule files |
| `forge-compat-tests` | Cross-platform test suite verifying transpiled outputs work on each target |

### Key Constraint

Hook-driven memory/context from v0.4.0 is Claude Code-specific. The adapter layer must define how memory and context work on each platform:
- **Copilot**: Context injected via `.instructions.md` preamble; memory is read-only (no hooks to enforce writes)
- **Gemini/Cursor**: Context via their native file-discovery mechanisms; memory may require platform-specific plugins

---

## Milestone: v0.7.0-alpha — Intelligent Orchestration

> *"The forge runs itself — the smith need only speak, and the hammers know where to strike."*

**Theme**: MCP-native memory/context. Dynamic model routing. Cross-platform task handoff.

**GitHub Milestone**: [`v0.7.0-alpha`](https://github.com/Olino3/forge/milestone/v0.7.0-alpha)

### Goals

| Goal | Description |
|------|-------------|
| **Internal MCP for memory/context** | Replace hook-driven memory/context with a locally-running MCP server providing `memory_read`, `memory_write`, `context_load`, `context_search` tools. Decouples from Claude Code hooks; makes memory/context available to any MCP-compatible platform |
| **Dynamic model routing** | Route skills to models based on task complexity metrics (not just static config). Use telemetry data from v0.5.0 to auto-classify skill complexity: simple skills → haiku, moderate → sonnet, complex → opus |
| **Continuous Maintenance** | Agentic workflows monitor upstream platform changelogs (Claude Code, Copilot, Gemini), detect breaking changes, auto-generate PRs to update adapters/transpilers |
| **Cross-platform task handoff** | When a platform hits usage limits (e.g., rate limits), seamlessly hand off the current task to another platform (Copilot, Aider, etc.). Requires: shared memory (via MCP), task state serialization, handoff protocol |

### Key Tradeoff

The internal MCP adds infrastructure complexity (a running process). For pure-Claude-Code users, hooks (v0.4.0) were simpler. Decision: **support both** — hooks for lightweight single-platform usage, MCP for multi-platform orchestration. The MCP server can wrap the same Markdown storage.

### Architectural Constraint

Cross-platform handoff requires:
- Shared memory store (MCP provides this)
- Task state serialization (current task, progress, context loaded, outputs produced)
- Platform detection and capability negotiation
- Graceful handoff protocol (export state → switch platform → import state → resume)

---

## Milestone: v0.8.0-alpha — Data-Driven Refinement

> *"A blade tested in battle is reforged stronger — data from the field tempers the steel."*

**Theme**: Use telemetry and quality scores to systematically improve every component.

**GitHub Milestone**: [`v0.8.0-alpha`](https://github.com/Olino3/forge/milestone/v0.8.0-alpha)

### Goals

| Goal | Description |
|------|-------------|
| **Skill effectiveness dashboard** | Aggregate quality scores, token usage, success rates per skill. Identify underperformers for refactoring or retirement |
| **Agent performance profiles** | Track completion rates, failure patterns, token consumption per agent. Tune configs based on data |
| **Command usage analytics** | Most/least used commands. Refine or retire low-usage; add commands based on observed patterns |
| **Automated regression detection** | Compare quality scores across versions. Alert when a bump degrades skill quality |
| **Quality gates** | Block version bumps (`make bump-*`) if aggregate quality score drops below threshold |
| **Fixture refresh** | Use telemetry-sampled outputs to auto-generate fresh test fixtures, solving mock drift from v0.4.0 |

---

## Post-v0.8.0 → Beta Graduation

**Version**: TBD — evaluated after v0.8.0 based on quality data.

If all beta vision criteria are met after v0.8.0, the next release is `v0.9.0-beta`. If gaps remain, additional alpha milestones are added until criteria are satisfied.

### Possible gap-closing milestones

| Gap | Milestone focus |
|-----|----------------|
| Quality scores below threshold | Additional skill refinement sprint |
| Copilot adapter incomplete | Dedicated platform porting sprint |
| Security issues found | Security hardening sprint |
| Onboarding documentation gaps | Documentation and tutorial sprint |

---

## Versioning Policy

| Phase | Versioning | Rationale |
|-------|-----------|-----------|
| **Alpha** (current) | Minor bumps always +1 (v0.3.0 → v0.4.0 → v0.5.0...) regardless of scope | Versions track state transitions, not change magnitude. Focus is velocity |
| **Beta** (future) | Semantic versioning — patch for fixes, minor for features, major for breaking changes | Stability matters; consumers depend on compatibility |
| **Milestones** | Each version = one GitHub milestone. Milestone title matches version number | Issues tagged to milestones; Milestone Planner/Feature Decomposer/Progress Reviewer workflows drive decomposition |
| **Rolling window** | ROADMAP details the next 2 milestones; remaining milestones carry goal-level plans | As milestones ship, the detail window slides forward |

**Single source of truth**: `VERSION` file at repo root. Bump with `make bump-minor`.

---

## Agentic Workflows — Autonomous Quality Agents

> *"The tireless automatons of Hephaestus's workshop never sleep."*

The Forge runs **19 autonomous agentic workflows** via [GitHub Agentic Workflows (gh-aw)](https://github.github.com/gh-aw/), powered by the Copilot engine. These workflows continuously monitor, validate, and improve the codebase — creating issues with findings or draft PRs with proposed changes. Nothing merges without human approval.

See **[AGENTIC_FORGE.md](AGENTIC_FORGE.md)** for the contributor guide and **[AGENTIC_WORKFLOWS_ROADMAP.md](AGENTIC_WORKFLOWS_ROADMAP.md)** for the technical roadmap.

| Category | Workflows | Trigger |
|----------|-----------|---------|
| **Continuous Simplicity** | Skill Simplifier, Duplication Detector | PR events |
| **Continuous Context** | Context Generator, Context Pruner | PR events / merge |
| **Continuous Refactoring** | Skill Validator, Agent Validator | Schedule + PR |
| **Continuous Style** | Convention Enforcer, Hook Quality Checker | PR + schedule |
| **Continuous Improvement** | Health Dashboard, Cross-Reference Checker, Best Practices Improver | Schedule + PR |
| **Continuous Documentation** | Doc Sync, Doc Unbloat | Schedule |
| **Continuous Testing** | CI Failure Diagnostician | CI failure events |
| **Operations & Release** | Release Notes Generator, Dependency Update Sentinel | Release / daily |
| **Planning & Coordination** | Issue Triage Agent, Milestone Planner, Feature Decomposer, Milestone Progress Reviewer, Stale Gardener | Issue events / schedule / PR events |

### Continuous Milestone Delivery ✅

Three interlocking agents autonomously drive milestones from planning through completion:

| Workflow | Trigger | Status |
|----------|---------|--------|
| **Milestone Planner** | Milestone created | ✅ Implemented |
| **Feature Decomposer** | Issue labeled `milestone-feature` | ✅ Implemented |
| **Milestone Progress Reviewer** | PR events (milestone-associated) | ✅ Implemented |

---

## Forge Chronicle

| Date | Milestone |
|------|-----------|
| **Feb 13, 2026** | v0.3.0-alpha — Agentic Workflows (19), Documentation Overhaul, COOKBOOK.md, Marketplace (38 plugins, 212 external skills) |
| **Feb 12, 2026** | Architecture/Design Skills (4), Frontend/Mobile Skills (6), Frontend/UI Skills (6), Utilities (10), Database/Storage (3) |
| **Feb 12, 2026** | Factory Stable — 102 skills, 12 commands, 19 agents, 81 context files, 20 hooks, ~1,993 tests |
| **Feb 11, 2026** | Enterprise Skills Catalog (173 skills), Community Skills Catalog (99+ planned) |
| **Feb 10, 2026** | MCP Integration — 8 external knowledge conduits connected |
| **Nov 18, 2025** | Azure Functions — generate-azure-functions with Tilt + Azurite |
| **Nov 14, 2025** | .NET Code Review — dotnet-code-review with 12 context files |

---

*Last Updated: February 13, 2026*
*Maintained by: The Forge Keepers*

*Forged by Hephaestus. Tempered by experience. Worthy of Olympus.*
