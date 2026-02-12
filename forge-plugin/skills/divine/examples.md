# Divine Toolkit Examples

This file contains example scenarios demonstrating how to use the divine skill to discover and orchestrate Forge capabilities.

---

## Example 1: Discovering Available Skills

### Scenario
A new user wants to understand what The Forge can do and which skills are available for Python development.

### User Prompt
```
What tools do I have available for Python development?
```

### Skill Execution

**Step 1 - Initial Analysis**:
- Intent: Discover available Python-related tools
- Scope: Skill and agent discovery filtered by domain
- Mode: Single-domain catalog request

**Step 2 - Load Memory**:
- Check `memoryStore.getSkillMemory("divine", "{project-name}")` for past recommendations
- No prior recommendations found (first use)

**Step 3 - Load Context**:
- Load skill registry via `contextProvider`
- Load agent registry for Python-relevant agents

**Step 4 - Discover Available Tools**:
Python-relevant tools identified:
| Tool | Type | Description |
|------|------|-------------|
| python-code-review | Skill | Comprehensive Python code review with best practices |
| generate-python-unit-tests | Skill | Generate pytest unit tests for Python code |
| python-dependency-management | Skill | Manage Python dependencies and virtual environments |
| @python-engineer | Agent | Specialist agent for Python development |
| @data-scientist | Agent | Data science with Python (pandas, numpy, ML) |

**Step 5 - Match & Recommend**:
Presented categorized catalog with usage triggers for each tool.

**Step 6 - Output**:
```
🔱 The Forge — Python Toolkit

Skills:
  • python-code-review — Review Python code for quality, security, and best practices
  • generate-python-unit-tests — Generate comprehensive pytest test suites
  • python-dependency-management — Manage requirements.txt, pyproject.toml, virtual envs

Agents:
  • @python-engineer — Dedicated Python development specialist
  • @data-scientist — Data analysis and ML with Python

Commands:
  • /analyze — Run code analysis (delegates to python-code-review)
  • /test — Generate tests (delegates to generate-python-unit-tests)
```

---

## Example 2: Recommending a Workflow for a New Project

### Scenario
Developer wants to start a new web application project and needs guidance on which Forge tools to use in what order.

### User Prompt
```
I'm starting a new Next.js app with authentication and a database. What's the best workflow?
```

### Skill Execution

**Step 1 - Initial Analysis**:
- Intent: Multi-step workflow composition for new project
- Scope: Full workflow orchestration
- Domain: Frontend (Next.js) + Backend (auth, database)

**Step 2 - Load Memory**:
- Check for prior workflow compositions
- Found pattern: Next.js projects commonly use project-planning → project-session-management

**Step 3 - Load Context**:
- Load full skill, agent, and command registries

**Step 4 - Discover**:
Relevant tools: project-planning, project-session-management, database-schema-analysis, documentation-generator, generate-jest-unit-tests, commit-helper

**Step 5 - Match & Score**:
| Tool | Relevance | Phase |
|------|-----------|-------|
| project-planning | 95% | Phase 1: Planning |
| project-session-management | 90% | Phase 1: Planning |
| database-schema-analysis | 85% | Phase 2: Design |
| documentation-generator | 80% | Phase 3: Documentation |
| generate-jest-unit-tests | 75% | Phase 4: Testing |
| commit-helper | 70% | Ongoing |

**Step 6 - Compose Workflow**:
```
🔱 Recommended Workflow: New Next.js Application

Phase 1: Planning
  1. Use skill:project-planning to generate IMPLEMENTATION_PHASES.md
  2. Use skill:project-session-management to set up SESSION.md tracking
  3. Use /plan-project command for structured planning

Phase 2: Design & Architecture
  4. Use skill:database-schema-analysis to design the data model
  5. Delegate to @athena for architecture review

Phase 3: Implementation
  6. Use @full-stack-engineer for feature development
  7. Use skill:commit-helper for clean git history

Phase 4: Quality Assurance
  8. Use skill:generate-jest-unit-tests for test coverage
  9. Use /test command to validate coverage

Phase 5: Documentation & Release
  10. Use skill:documentation-generator for project docs
  11. Use /document command to generate README
```

---

## Example 3: Finding the Right Tool for a Specific Task

### Scenario
Developer has a specific task and wants to know which single skill or command handles it best.

### User Prompt
```
I need to review the git changes from my last 3 commits and write good commit messages. What should I use?
```

### Skill Execution

**Step 1 - Initial Analysis**:
- Intent: Identify specific tools for git diff review and commit message crafting
- Scope: Single-task tool recommendation
- Domain: Git/version control

**Step 2 - Load Memory**:
- Prior recommendations for git tasks found
- Previous success: get-git-diff + commit-helper combo rated highly

**Step 3 - Load Context**:
- Load git-domain skills from registry

**Step 4 - Discover**:
Git-relevant tools:
- get-git-diff: Analyze git diffs with structured summaries
- commit-helper: Craft convention-compliant commit messages

**Step 5 - Match**:
| Tool | Task Match | Confidence |
|------|-----------|------------|
| get-git-diff | Review changes from last 3 commits | 98% |
| commit-helper | Write commit messages | 97% |

**Step 6 - Recommend**:
```
🔱 Recommended Tools

For reviewing changes:
  → skill:get-git-diff — Analyzes diffs between any two commits
  Usage: "Show me the diff for the last 3 commits"

For writing commit messages:
  → skill:commit-helper — Crafts Conventional Commits messages
  Usage: "Help me write a commit message for my staged changes"

💡 Pro Tip: Use get-git-diff first to analyze changes, then
   commit-helper to craft messages based on the analysis.
```

---

## Summary

The divine skill serves three primary use cases:

1. **Discovery** — "What tools are available for X?" → Returns filtered catalog
2. **Workflow Composition** — "How should I approach X?" → Returns ordered multi-step workflow
3. **Task Matching** — "What should I use for X?" → Returns ranked single-tool recommendations
