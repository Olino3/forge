# ⚒️ Model-Workflow Matrix

> *"Every blade from the Forge is tempered with the right flame — divine fire for creation, mortal fire for shaping."*

This document maps each agentic workflow to its assigned AI model, explains the rationale, and defines prompt engineering standards for each model tier.

---

## Model Assignments

| Workflow | Model | Cost | Role | Rationale |
|----------|-------|------|------|-----------|
| **Component Improver** | `gemini-3-pro` | Low | Context Researcher | Analyzes components against full codebase context, requiring simultaneous loading of multiple files (CLAUDE.md, SKILL_TEMPLATE.md, OUTPUT_CONVENTIONS.md, etc.). Gemini's large context window enables comprehensive best-practices analysis without truncation. |
| **Context Generator** | `gpt-4.1` | Free | Code Writer | Generates new context files from skill definitions — needs high-fidelity Markdown output that matches existing conventions (YAML frontmatter, ATX headings, tag structure). GPT-4.1's instruction-following precision avoids format drift. |
| **Improve Test Coverage** | `gpt-4.1` | Free | Test Generator | Generates pytest test functions matching existing patterns (`conftest.py` fixtures, `FORGE_DIR` resolution, class-based grouping). Few-shot prompting with real test file examples produces code that passes on first run. |
| **Feature Decomposer** | `gemini-3-pro` | Low | Strategic Decomposer | Decomposes complex features into work items by analyzing feature descriptions, acceptance criteria, and codebase structure. Requires deep understanding of task dependencies and architectural implications. Gemini's reasoning capabilities produce well-structured, implementable work items. |
| **Dependency Sentinel** | `gpt-5.1-codex-mini` | Free | Tool Executor | Scans `.gitmodules`, workflow files, and marketplace manifests for outdated references. Predominantly grep/search operations with structured output. Codex Mini's fast tool invocation keeps daily runs under 2 minutes. |
| **Stale Gardener** | `gpt-5.1-codex-mini` | Free | Batch Processor | Lists stale issues/PRs and applies labels — bulk API operations with simple 30-day/14-day threshold logic. No deep reasoning required. Codex Mini processes the batch in a single fast pass. |
| **Doc Maintainer** | `gemini-3-pro` | Low | Context Researcher | Syncs docs against the full codebase, then unbloats. Requires loading `CLAUDE.md` (900+ lines), `README.md`, `ROADMAP.md`, `CONTRIBUTING.md`, and `COOKBOOK.md` simultaneously. Gemini's large context window handles the full corpus without truncation, enabling accurate drift detection. |
| **CI Failure Diagnostician** | `gpt-4.1` | Free | Log Analyst | Ingests full CI run logs (often 10K+ lines), correlates failures across multiple test files, and identifies root causes. GPT-4.1's precision in parsing structured logs and generating actionable diagnostics makes it ideal for the analyze→fix pipeline. |
| **Milestone Lifecycle** | `claude-opus-4.6` | Premium | Strategic Orchestrator | Manages complete milestone lifecycle: planning, progress tracking, and completion review. Requires sophisticated chain-of-thought reasoning across multiple issues, categorization logic, completion calculations, blocker identification, and reprioritization recommendations. Opus's advanced reasoning ensures comprehensive, actionable milestone oversight. |
| **Project Manager Agent** | `claude-opus-4.6` | Premium | Strategic Planner | Compares ROADMAP objectives against implementation state — requires nuanced gap analysis, prioritization judgment, and long-term strategic planning. Opus's advanced reasoning capabilities and persona-based prompting yield deeply actionable execution plans with architectural awareness. |
| **Release Notes Generator** | `claude-haiku-4.5` | Low | Summarizer | Synthesizes merged PRs into categorized changelog (Added/Changed/Fixed/Removed). Requires editorial judgment about categorization and audience-appropriate language. Haiku excels at structured summarization with consistent voice. |

---

## Model Tiers

### GPT-5.1-Codex-Mini (Free) — "The Worker"

**Best for:** High-speed tool execution, grep/search operations, batch processing, terse output.

| Attribute | Guideline |
|-----------|-----------|
| **Prompt Strategy** | Terse, imperative, tool-first |
| **System Role** | Direct executor — no analysis persona |
| **Prompt Structure** | Command → Tool calls → Output format |
| **Pro-patterns** | `"Execute immediately"`, tool call examples, structured output schemas |
| **Anti-patterns** | ❌ Chain-of-Thought, ❌ "Think step by step", ❌ Persona descriptions |
| **Token Budget** | Minimize input — no examples longer than 5 lines |

**Example system prompt style:**
```
Decompose this feature into 3-5 work items. For each: create an issue
with title '[Work item] {description}', body with acceptance criteria,
and label 'milestone-feature'. Execute tool calls immediately. No preamble.
```

### GPT-4.1 (Free) — "The Editor"

**Best for:** Precision editing, diff generation, code writing, format-sensitive output.

| Attribute | Guideline |
|-----------|-----------|
| **Prompt Strategy** | Few-Shot with precision diff examples |
| **System Role** | Surgical editor with before/after examples |
| **Prompt Structure** | Role → Examples (2-3 few-shot) → Task → Output format (diff) |
| **Pro-patterns** | `<before>` / `<after>` blocks, exact file paths, line-level precision |
| **Anti-patterns** | ❌ Open-ended exploration, ❌ "Consider alternatives" |
| **Token Budget** | Include 2-3 concrete examples in system prompt |

**Example system prompt style:**
```
You are a precision code editor. Output ONLY file diffs. Do not explain.
For each file, output:
  <file path='...'>
    <before>...</before>
    <after>...</after>
  </file>
```

### Gemini 3 Pro (Low Cost) — "The Researcher"

**Best for:** Deep context analysis, log parsing, documentation sync, needle-in-haystack retrieval.

| Attribute | Guideline |
|-----------|-----------|
| **Prompt Strategy** | Needle-in-Haystack retrieval with XML data delimiting |
| **System Role** | Deep context analyst with massive input windows |
| **Prompt Structure** | Role → `<data>` blocks (XML delimited) → Retrieval instructions → Output schema |
| **Pro-patterns** | Full file contents in XML blocks, `"Find all instances of X in <data>"`, structured XML output |
| **Anti-patterns** | ❌ Short prompts, ❌ Truncated context |
| **Token Budget** | Maximize input — use full token window for comprehensive analysis |

**Example system prompt style:**
```
You are a CI failure analyst.
<logs>{{workflow run logs}}</logs>
<test_files>{{relevant test files}}</test_files>
Find the root cause. Output:
  <diagnosis>
    <root_cause>...</root_cause>
    <failing_test>...</failing_test>
    <fix_suggestion>...</fix_suggestion>
    <confidence>high|medium|low</confidence>
  </diagnosis>
```

### Claude Haiku 4.5 (Low Cost) — "The Critic"

**Best for:** Structured reasoning, gap analysis, summarization, editorial judgment, sanity checks.

| Attribute | Guideline |
|-----------|-----------|
| **Prompt Strategy** | Chain-of-Thought with structured reasoning and persona |
| **System Role** | Analytical critic with thinking blocks |
| **Prompt Structure** | Persona → `<thinking>` → Step-by-step analysis → Structured JSON/Markdown output |
| **Pro-patterns** | `"Think step by step"`, numbered reasoning steps, confidence scores, `"Identify what's wrong before suggesting fixes"` |
| **Anti-patterns** | ❌ Tool-heavy workflows, ❌ Massive refactors |
| **Token Budget** | Medium — prioritize reasoning quality over input volume |

**Example system prompt style:**
```
You are a project management analyst. Think step-by-step:
1) List all open issues in the milestone.
2) Categorize: completed / in-progress / blocked / not-started.
3) Calculate completion %.
4) Identify blockers with root causes.
5) Output as JSON: {completion_pct, issues: [...], recommendations: []}
```

### Claude Opus 4.6 (Premium) — "The Strategist"

**Best for:** Complex strategic planning, multi-faceted analysis, long-term roadmap alignment, sophisticated orchestration.

| Attribute | Guideline |
|-----------|-----------|
| **Prompt Strategy** | Multi-stage reasoning with architectural context and strategic oversight |
| **System Role** | Strategic orchestrator with deep analytical capabilities |
| **Prompt Structure** | Persona → Context loading → Multi-phase analysis → Chain-of-Thought → Strategic output with confidence scoring |
| **Pro-patterns** | `"Analyze dependencies"`, `"Consider long-term implications"`, multi-issue correlation, architectural awareness, `"Provide strategic recommendations"` |
| **Anti-patterns** | ❌ Simple batch operations, ❌ Single-file edits, ❌ Grep/search-only tasks |
| **Token Budget** | High — maximize input for comprehensive strategic analysis across multiple documents/issues |

**Example system prompt style:**
```
You are a strategic project manager overseeing milestone lifecycle.
Phase 1: Analyze all open issues in this milestone — categorize by status, priority, and dependencies.
Phase 2: Calculate completion percentage based on acceptance criteria completion, not just issue closure.
Phase 3: Identify blockers — both technical (broken builds, failing tests) and organizational (awaiting review, unclear requirements).
Phase 4: Recommend reprioritization based on blocker resolution paths and strategic value.
Output: {
  completion_pct,
  issues: [{id, status, blockers, priority_recommendation}],
  strategic_recommendations: [],
  confidence: high|medium|low
}
```

---

## Cost Projection

| Model | Workflows | Runs/Month (est.) | Cost |
|-------|-----------|-------------------|------|
| GPT-4.1 | 3 | ~12 | Free |
| GPT-5.1-Codex-Mini | 2 | ~9 | Free |
| Gemini 3 Pro | 3 | ~12 | Low (per-token) |
| Claude Haiku 4.5 | 1 | ~5 | Low (per-token) |
| Claude Opus 4.6 | 2 | ~8 | Premium (per-token) |
| **Deterministic CI** | 8 jobs | ~20 | $0 (GitHub Actions minutes) |
| **Total** | 11 + CI | ~66 | ~$5-10/month |

**Before optimization:** ~500 runs/month across 24 workflows using default model.
**After optimization:** ~68 runs/month across 11 workflows + CI, with model-appropriate assignments.

---

*Forged by Hephaestus. Each tool matched to its fire.*
