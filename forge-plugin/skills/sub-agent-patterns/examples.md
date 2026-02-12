# Sub-Agent Patterns Examples

This file contains example scenarios demonstrating how to use the sub-agent-patterns skill to select agents, create custom agents, and design delegation chains.

---

## Example 1: Choosing the Right Built-in Agent for Code Exploration

### Scenario
A developer needs to understand how authentication works in a large TypeScript codebase they've never seen before. They want to find all authentication-related files, understand the flow, and get a summary of the approach used.

### User Prompt
```
I need to understand how authentication works in this codebase. Find all auth-related files and explain the authentication flow.
```

### Skill Execution

**Step 1 - Initial Analysis**:
```
Task Type: Choosing an existing agent
Target Goal: Explore a codebase to understand authentication flow
Tools Needed: File search (grep, glob), file reading (view)
Reasoning Depth: Fast search + moderate synthesis
Scope: Single agent selection
```

**Step 2 - Load Memory**:
- No previous memory found; first sub-agent-patterns session for this project

**Step 3 - Load Context**:
- Loaded engineering domain context for agent selection standards
- Reviewed available agents under `agents/`

**Step 4 - Catalog Available Agents**:
```
Built-in candidates for code exploration:

| Agent           | Fit    | Rationale                                              |
|-----------------|--------|--------------------------------------------------------|
| Explore         | ★★★★★  | Purpose-built for codebase search; grep, glob, view    |
| Task            | ★★☆☆☆  | CLI-focused; overkill for read-only exploration        |
| General-Purpose | ★★★☆☆  | Full toolset but slower and more expensive than needed  |
```

**Step 5 - Design Delegation Strategy**:
```
Recommendation: Use the Explore agent

Rationale:
- The task is read-only codebase search — no CLI commands needed
- Explore uses Haiku (fast, cheap) and has grep/glob/view tools
- Returns focused answers under 300 words — perfect for summaries
- Safe to call in parallel if we want to search multiple patterns simultaneously

Delegation Architecture:
- Agent type: Built-in (Explore)
- Delegation depth: Single agent invocation
- Context passing: Provide the question directly as the prompt
- Output expectations: Summarized answer under 300 words
- Execution mode: Single call (or parallel if splitting into multiple search queries)

Alternative approach — two parallel Explore calls:
  1. "Find all files related to authentication — middleware, guards, JWT, session"
  2. "How does the login flow work? Trace from route handler to token generation"

Error Handling:
- If Explore returns insufficient results, escalate to General-Purpose agent for deeper analysis
- If the codebase is too large for a single Explore call, split into targeted queries
```

**Step 6 - Generate Agent Configuration**:
```
No new agent needed — using built-in Explore agent.

Usage Template:
  Agent: Explore
  Prompt: "Find all authentication-related files in this codebase (middleware,
           guards, JWT, session handlers). Explain the authentication flow from
           login request to token issuance."
  Parallel: Yes — safe to run alongside other Explore calls

Fallback:
  If Explore produces incomplete results:
  Agent: General-Purpose
  Prompt: Same prompt with added instruction to trace code paths in detail
```

**Step 7 - Output**:
- Saved to `/claudedocs/sub-agent-selection_auth-exploration_2025-07-16.md`

**Step 8 - Memory Update**:
- Created `agent_catalog.md` with Explore agent profile and code exploration strength
- Created `delegation_patterns.md` with single-agent selection pattern for read-only tasks

---

## Example 2: Creating a Custom Specialist Agent for Database Optimization

### Scenario
A team frequently works on PostgreSQL performance tuning and wants a custom Forge agent that specializes in database optimization — analyzing query plans, suggesting index improvements, and reviewing schema designs.

### User Prompt
```
Create a custom agent that specializes in PostgreSQL database optimization. It should be able to analyze query performance, suggest indexes, and review schema designs.
```

### Skill Execution

**Step 1 - Initial Analysis**:
```
Task Type: Creating a new agent
Target Goal: Custom specialist agent for PostgreSQL optimization
Tools Needed: Shell (for running EXPLAIN queries), file access (for reading schema files)
Reasoning Depth: Deep — database optimization requires careful analysis
Scope: Full agent creation (`.md` + `.config.json` + memory directory)
```

**Step 2 - Load Memory**:
- No previous memory found; first sub-agent-patterns session for this project

**Step 3 - Load Context**:
- Loaded engineering domain context
- Loaded documentation standards for agent `.md` files
- Reviewed existing agent `.md` and `.config.json` files for structural patterns

**Step 4 - Catalog Available Agents**:
```
Existing agents reviewed for overlap:

Built-in agents: None specialize in database optimization
Custom Forge agents: No existing database-focused agent found

Conclusion: A new custom agent is justified — no existing agent covers this domain
```

**Step 5 - Design Delegation Strategy**:
```
This is a new agent creation task, not a delegation task.

Agent Design Decisions:
- Model: Sonnet — database optimization requires deep reasoning about query plans
  and schema trade-offs; Haiku would be too shallow
- Tools: Shell (for EXPLAIN ANALYZE), file access (for reading SQL migrations),
  grep (for finding query patterns in code)
- Context Domains: engineering (primary), database/sql (if available)
- Skills: database-schema-analysis (existing skill to leverage)
- Memory: Track optimization patterns per database/project
```

**Step 6 - Generate Agent Configuration**:

Agent personality file (`agents/db-optimizer.md`):
```markdown
# DB Optimizer — The Query Whisperer

## Personality
You are a meticulous database performance engineer with deep expertise in
PostgreSQL internals. You think in terms of query plans, index B-trees, and
I/O costs. You communicate findings with precision, always backing
recommendations with EXPLAIN ANALYZE output and cost estimates.

## Expertise Areas
- Query plan analysis and optimization
- Index design (B-tree, GIN, GiST, BRIN)
- Schema normalization and denormalization trade-offs
- Connection pooling and resource management
- Vacuum and maintenance strategies

## Workflow
1. Gather the target queries or schema files
2. Run EXPLAIN ANALYZE on problematic queries
3. Analyze sequential scans, nested loops, and sort operations
4. Recommend index additions or query rewrites
5. Estimate performance improvement with cost comparisons
6. Document findings with before/after query plans
```

Agent configuration (`agents/db-optimizer.config.json`):
```json
{
  "name": "db-optimizer",
  "description": "PostgreSQL database optimization specialist",
  "model": "sonnet",
  "contextDomains": ["engineering"],
  "skills": ["database-schema-analysis"],
  "memoryPath": "memory/agents/db-optimizer",
  "tools": ["shell", "file_access", "grep", "glob"]
}
```

Memory directory: `memory/agents/db-optimizer/`

**Step 7 - Output**:
- Saved to `/claudedocs/sub-agent-config_db-optimizer_2025-07-16.md`
- Includes: agent `.md`, `.config.json`, and memory directory structure

**Step 8 - Memory Update**:
- Updated `agent_catalog.md` with db-optimizer agent profile and PostgreSQL specialization
- Updated `delegation_patterns.md` with custom agent creation pattern — noted Sonnet model choice for deep reasoning tasks

---

## Example 3: Designing a Multi-Agent Delegation Chain for Complex Refactoring

### Scenario
A tech lead needs to refactor a monolithic Express.js application into a modular architecture. The task involves: understanding the current codebase structure, identifying module boundaries, generating the new file structure, moving code, and verifying nothing is broken. This is too complex for any single agent.

### User Prompt
```
I need to refactor this Express.js monolith into modules. Design a multi-agent workflow that explores the codebase, plans the module boundaries, executes the refactoring, and verifies everything still works.
```

### Skill Execution

**Step 1 - Initial Analysis**:
```
Task Type: Designing delegation patterns
Target Goal: Multi-agent workflow for monolith-to-modules refactoring
Tools Needed: File search, code analysis, shell commands, test execution
Reasoning Depth: Mixed — fast search for exploration, deep reasoning for planning
Scope: Multi-agent delegation chain with 4 phases
```

**Step 2 - Load Memory**:
- Found previous memory from sub-agent-patterns sessions
- Reviewed: Explore agent works well for initial codebase mapping
- Applied: Use parallel Explore calls for independent search tasks

**Step 3 - Load Context**:
- Loaded engineering domain context for refactoring standards
- Loaded JavaScript domain context for Express.js patterns
- Reviewed available agents for refactoring capabilities

**Step 4 - Catalog Available Agents**:
```
Agents needed for this workflow:

| Phase        | Agent           | Rationale                                           |
|--------------|-----------------|-----------------------------------------------------|
| Discovery    | Explore         | Fast codebase search to map routes, models, services|
| Planning     | General-Purpose | Deep reasoning to design module boundaries          |
| Execution    | General-Purpose | Full toolset for file operations and code changes   |
| Verification | Task            | Run tests, lints, and build to verify correctness   |
```

**Step 5 - Design Delegation Strategy**:
```
Delegation Architecture: Sequential 4-phase chain with parallel sub-tasks

Phase 1 — Discovery (Explore agents, parallel):
  Call 1: "Find all Express route handlers — list files and endpoints"
  Call 2: "Find all database models and their relationships"
  Call 3: "Find all shared utilities, middleware, and service files"
  Execution: Parallel (3 independent searches)
  Output: Combined codebase map with routes, models, and services

Phase 2 — Planning (General-Purpose agent, sequential):
  Input: Codebase map from Phase 1
  Prompt: "Given this codebase map, design module boundaries. Group related
           routes, models, and services into cohesive modules. Define the
           new directory structure and list all file moves needed."
  Output: Module boundary plan with file move manifest

Phase 3 — Execution (General-Purpose agent, sequential):
  Input: Module boundary plan from Phase 2
  Prompt: "Execute the refactoring plan. Create the new directory structure,
           move files, update all import paths, and fix any circular
           dependencies."
  Output: Refactored codebase with updated imports

Phase 4 — Verification (Task agent, sequential):
  Input: None (operates on current codebase state)
  Prompt: "Run the full test suite, linter, and build. Report any failures."
  Output: Pass/fail status with failure details if any

Error Handling:
  - Phase 1 failure: Retry individual Explore calls with narrower search scope
  - Phase 2 failure: Provide additional context about the project's conventions
  - Phase 3 failure: Roll back changes via git and retry with smaller batches
  - Phase 4 failure: Return to Phase 3 to fix specific test/lint failures

Context Passing Between Phases:
  Phase 1 → 2: Concatenate Explore outputs into a structured codebase map
  Phase 2 → 3: Pass the complete module plan with file move manifest
  Phase 3 → 4: No explicit passing — Task agent operates on filesystem state
  Phase 4 → 3: If failures, pass error details back for targeted fixes
```

**Step 6 - Generate Agent Configuration**:
```
No new custom agents needed — all phases use built-in agents.

Delegation Chain Specification:

┌─────────────────────────────────────────────┐
│ Phase 1: Discovery (Parallel Explore × 3)   │
│  ├─ Explore: Route handlers                 │
│  ├─ Explore: Database models                │
│  └─ Explore: Utilities & middleware         │
└──────────────┬──────────────────────────────┘
               │ Codebase map
┌──────────────▼──────────────────────────────┐
│ Phase 2: Planning (General-Purpose × 1)     │
│  └─ Design module boundaries & file moves   │
└──────────────┬──────────────────────────────┘
               │ Module plan
┌──────────────▼──────────────────────────────┐
│ Phase 3: Execution (General-Purpose × 1)    │
│  └─ Move files, update imports, fix deps    │
└──────────────┬──────────────────────────────┘
               │ Refactored codebase
┌──────────────▼──────────────────────────────┐
│ Phase 4: Verification (Task × 1)            │
│  └─ Run tests, lint, build                  │
└──────────────┬──────────────────────────────┘
               │ Pass/Fail
        ┌──────▼──────┐
        │  Complete?   │──No──→ Return to Phase 3
        └──────┬──────┘
               │ Yes
          ✅ Done
```

**Step 7 - Output**:
- Saved to `/claudedocs/sub-agent-delegation_express-refactor_2025-07-16.md`
- Includes: 4-phase chain specification, agent assignments, context passing contracts, error handling

**Step 8 - Memory Update**:
- Updated `agent_catalog.md` with parallel Explore pattern for codebase discovery
- Updated `delegation_patterns.md` with multi-phase delegation chain pattern — noted effectiveness of parallel Explore for discovery, General-Purpose for planning/execution, Task for verification

---

## Summary of Sub-Agent Pattern Scenarios

1. **Agent selection** — Matched a read-only code exploration task to the Explore agent based on tool requirements, speed, and cost; documented fallback to General-Purpose for deeper analysis
2. **Custom agent creation** — Designed a PostgreSQL optimization specialist with Sonnet model, shell tools, and database-schema-analysis skill integration; produced `.md`, `.config.json`, and memory directory
3. **Multi-agent delegation** — Designed a 4-phase sequential chain with parallel sub-tasks for monolith refactoring; Explore for discovery, General-Purpose for planning/execution, Task for verification; included error handling and context passing contracts

## Best Practices

- Always prefer built-in agents for simple tasks — they are faster and cheaper than custom agents
- Use Explore for any read-only codebase search — it is purpose-built for this and safe to run in parallel
- Use Task for command execution where you only need pass/fail status — it keeps output clean
- Reserve General-Purpose for tasks requiring deep reasoning or the full toolset
- When designing delegation chains, minimize sequential dependencies — parallelize where possible
- Always define error handling and fallback strategies at each phase of a multi-agent workflow
- Document context passing contracts explicitly — agents are stateless and need complete input each time
