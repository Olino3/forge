# SkillInvoker Interface

**Version**: 0.1.0-alpha
**Status**: Phase 1 - Interface Definition

## Purpose

The SkillInvoker interface formalizes skill delegation, the mechanism by which commands (e.g., `/analyze`, `/test`) invoke specialized skills (e.g., `python-code-review`, `generate-python-unit-tests`) for deep analysis. Currently, skill delegation is described in prose within COMMAND.md files with no structured contract. The SkillInvoker provides a typed interface for invocation, result handling, and skill discovery.

### What It Replaces

Commands currently delegate to skills via inline prose instructions:

```markdown
# From /analyze COMMAND.md, Step 4:
skill:python-code-review --target [files] --depth deep
Process skill output: Incorporate review findings into analysis report
```

The SkillInvoker replaces this with a structured invocation and result contract.

---

## Types

### SkillResult

Returned by `invoke()` and `delegateAnalysis()`.

```
SkillResult {
  status: "success" | "partial" | "error"
  findings: Finding[]
  recommendations: string[]
  memoryUpdates: MemoryUpdate[]
  outputPath: string | null       // Path to generated report in /claudedocs
  tokenUsage: { input: number, output: number, total: number }
}
```

### Finding

Individual finding from a skill execution.

```
Finding {
  severity: "critical" | "high" | "medium" | "low"
  location: string               // File path and line number (e.g., "app/auth/middleware.py:45")
  description: string            // What was found
  recommendation: string         // What to do about it
  category: string               // e.g., "security", "performance", "architecture"
}
```

### MemoryUpdate

Describes a memory file that was created or updated during skill execution.

```
MemoryUpdate {
  layer: "shared-project" | "skill-specific" | "command"
  fileType: string               // e.g., "project_overview", "review_history"
  action: "created" | "updated" | "appended"
}
```

### SkillMetadata

Describes a skill's capabilities without invoking it.

```
SkillMetadata {
  name: string                   // e.g., "python-code-review"
  version: string                // e.g., "2.1.0"
  domain: string                 // e.g., "python", "dotnet", "angular", "infrastructure"
  capabilities: string[]         // e.g., ["code-review", "security-audit", "performance-analysis"]
  contextDomains: string[]       // e.g., ["python", "security"] - which context domains it loads
  memoryTypes: string[]          // e.g., ["project_overview", "common_patterns", "known_issues", "review_history"]
}
```

---

## Methods

### 1. `invoke(skillName, params)`

Invoke a skill and receive a structured result.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `skillName` | `string` | Yes | Skill to invoke (e.g., `"python-code-review"`) |
| `params` | `object` | Yes | Invocation parameters |
| `params.target` | `string` | Yes | Target files, directories, or scope |
| `params.depth` | `string` | No | Analysis depth: `"quick"` or `"deep"` (default: `"deep"`) |
| `params.options` | `object` | No | Skill-specific options (e.g., `{ focus: "security" }`) |

**Returns**: `SkillResult`

**Behavior**:
- Loads the skill's `SKILL.md` and executes its mandatory workflow
- The skill handles its own context and memory loading internally
- Captures all findings in structured `Finding` objects
- Tracks memory files created/updated during execution
- Records token usage for efficiency tracking

**Before** (current approach in `/analyze`):
```markdown
### Step 4: Skill Delegation (Deep Analysis)

**Python projects**:
skill:python-code-review --target [files] --depth deep

Process skill output: Incorporate review findings into analysis report

# Result: Unstructured text output, manual parsing required,
# no formal contract for findings, no token tracking
```

**After** (with SkillInvoker):
```
result = invoke("python-code-review", {
  target: "src/auth/",
  depth: "deep",
  options: { focus: "security" }
})

// result.status → "success"
// result.findings → [{ severity: "high", location: "src/auth/middleware.py:45", ... }]
// result.recommendations → ["Add rate limiting to login endpoint", ...]
// result.memoryUpdates → [{ layer: "skill-specific", fileType: "review_history", action: "appended" }]
// result.outputPath → "/claudedocs/python_code_review_my-api_2026-02-10.md"
```

---

### 2. `delegateAnalysis(skillName, target, depth)`

Convenience method for code review delegation. Wraps `invoke()` with analysis-specific defaults.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `skillName` | `string` | Yes | Analysis skill to invoke |
| `target` | `string` | Yes | Files or directories to analyze |
| `depth` | `string` | No | `"quick"` or `"deep"` (default: `"deep"`) |

**Returns**: `SkillResult`

**Behavior**:
- Equivalent to `invoke(skillName, { target, depth })`
- Maps to how `/analyze` currently delegates to `python-code-review`, `dotnet-code-review`, and `angular-code-review`

**Skill mapping** (from `/analyze` COMMAND.md):

| Project Type | Skill Invoked |
|-------------|--------------|
| Python | `python-code-review` |
| .NET/C# | `dotnet-code-review` |
| Angular/TypeScript | `angular-code-review` |

**Before** (from `/analyze` COMMAND.md Step 4):
```markdown
**Python projects**:
skill:python-code-review --target [files] --depth deep
Process skill output: Incorporate review findings into analysis report

**.NET projects**:
skill:dotnet-code-review --target [files] --depth deep
Process skill output: Merge .NET-specific findings with overall analysis

**Angular projects**:
skill:angular-code-review --target [files] --depth deep
Process skill output: Integrate Angular-specific patterns

**Multi-language projects**: Invoke multiple skills and aggregate results
```

**After**:
```
// Single-language project
pythonResult = delegateAnalysis("python-code-review", "src/", "deep")

// Multi-language project - invoke multiple skills and aggregate
pythonResult = delegateAnalysis("python-code-review", "backend/", "deep")
angularResult = delegateAnalysis("angular-code-review", "frontend/", "deep")

// Structured aggregation
allFindings = [...pythonResult.findings, ...angularResult.findings]
allFindings.sort(f => f.severity)  // Aggregate by severity across skills
```

---

### 3. `delegateTestGeneration(skillName, target)`

Convenience method for test generation delegation. Wraps `invoke()` with test generation defaults.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `skillName` | `string` | Yes | Test generation skill to invoke |
| `target` | `string` | Yes | Files or components to generate tests for |

**Returns**: `SkillResult`

**Behavior**:
- Equivalent to `invoke(skillName, { target, depth: "deep", options: { mode: "generate" } })`
- Maps to how `/test` currently delegates to `generate-python-unit-tests` and `generate-jest-unit-tests`

**Skill mapping** (from `/test` COMMAND.md):

| Project Type | Skill Invoked |
|-------------|--------------|
| Python | `generate-python-unit-tests` |
| Angular/TypeScript | `generate-jest-unit-tests` |

**Before** (from `/test` COMMAND.md Step 3):
```markdown
### Step 3: Generate Missing Tests (if --generate)

**Python projects**:
skill:generate-python-unit-tests --target [untested files]

**Angular projects**:
skill:generate-jest-unit-tests --target [untested components/services]
```

**After**:
```
// Python test generation
testResult = delegateTestGeneration("generate-python-unit-tests", "src/services/user.py")

// testResult.findings → [] (test generation produces files, not findings)
// testResult.outputPath → path to generated test file
// testResult.memoryUpdates → [{ layer: "skill-specific", fileType: "testing_patterns", action: "updated" }]
```

---

### 4. `getSkillMetadata(skillName)`

Get skill information without invoking it.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `skillName` | `string` | Yes | Skill name to query |

**Returns**: `SkillMetadata`

**Behavior**:
- Reads the skill's `SKILL.md` frontmatter (YAML header between `---` markers)
- Extracts version from version history section
- Determines domain from the skill's context dependencies
- Lists capabilities from the skill's focus areas
- Lists memory types from the skill's memory documentation

**Example**:
```
getSkillMetadata("python-code-review")
→ {
    name: "python-code-review",
    version: "2.1.0",
    domain: "python",
    capabilities: ["code-review", "security-audit", "performance-analysis", "architecture-review"],
    contextDomains: ["python", "security"],
    memoryTypes: ["project_overview", "common_patterns", "known_issues", "review_history"]
  }
```

---

### 5. `getAvailableSkills(domain?)`

List available skills, optionally filtered by domain.

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `domain` | `string` | No | Filter by domain (e.g., `"python"`, `"angular"`, `"infrastructure"`) |

**Returns**: `SkillMetadata[]`

**Behavior**:
- Scans `skills/` directory for subdirectories containing `SKILL.md`
- Reads frontmatter from each `SKILL.md` to build metadata
- If `domain` is specified, filters to skills matching that domain
- Results sorted alphabetically by name

**Example**:
```
getAvailableSkills("python")
→ [
    { name: "python-code-review", version: "2.1.0", domain: "python", ... },
    { name: "generate-python-unit-tests", domain: "python", ... },
    { name: "python-dependency-management", domain: "python", ... }
  ]

getAvailableSkills()
→ [all 102 skills with metadata]
```

---

## Skill Registry

The 102 currently registered core skills, organized by domain:

### Frontend & UI (6)
| Skill | Domain | Delegated By |
|-------|--------|-------------|
| `accessibility` | frontend | - |
| `animate` | frontend | - |
| `nextjs` | frontend | - |
| `react-forms` | frontend | - |
| `responsive-images` | frontend | - |
| `tailwind-patterns` | frontend | - |

### Frontend & Mobile (6)
| Skill | Domain | Delegated By |
|-------|--------|-------------|
| `angular-architect` | angular | - |
| `flutter-expert` | mobile | - |
| `react-expert` | frontend | - |
| `react-native-expert` | mobile | - |
| `vue-expert` | frontend | - |
| `vue-expert-js` | frontend | - |

### Authentication (5)
| Skill | Domain | Delegated By |
|-------|--------|-------------|
| `azure-auth` | azure | - |
| `better-auth` | engineering | - |
| `clerk-auth` | engineering | - |
| `firebase-auth` | engineering | - |
| `oauth-integrations` | engineering | - |

### Backend & Frameworks (6)
| Skill | Domain | Delegated By |
|-------|--------|-------------|
| `django` | python | - |
| `dotnet-core` | dotnet | - |
| `fastapi` | python | - |
| `nestjs` | engineering | - |
| `rails` | engineering | - |
| `php` | engineering | - |

### Architecture & Design (4)
| Skill | Domain | Delegated By |
|-------|--------|-------------|
| `api-design` | engineering | - |
| `architecture-design` | engineering | - |
| `graphql-design` | engineering | - |
| `microservices-design` | engineering | - |

### Cloud & Infrastructure (5)
| Skill | Domain | Delegated By |
|-------|--------|-------------|
| `cloud-architect` | infrastructure | - |
| `devops-engineer` | infrastructure | - |
| `kubernetes-specialist` | infrastructure | - |
| `sre-engineer` | infrastructure | - |
| `terraform-engineer` | infrastructure | - |

### Programming Languages (5)
| Skill | Domain | Delegated By |
|-------|--------|-------------|
| `cpp` | engineering | - |
| `csharp` | dotnet | - |
| `java-architect` | engineering | - |
| `javascript` | engineering | - |
| `typescript` | engineering | - |

### Data & Database (6)
| Skill | Domain | Delegated By |
|-------|--------|-------------|
| `database-optimizer` | schema | `/analyze` |
| `database-schema-analysis` | schema | `/analyze` |
| `pandas` | data-science | - |
| `postgres` | schema | - |
| `snowflake-platform` | schema | - |
| `sql` | schema | - |

### Database & Storage (2)
| Skill | Domain | Delegated By |
|-------|--------|-------------|
| `firebase-firestore` | engineering | - |
| `firebase-storage` | engineering | - |

### Quality & Security (6)
| Skill | Domain | Delegated By |
|-------|--------|-------------|
| `code-documenter` | engineering | `/document` |
| `code-reviewer` | engineering | `/analyze` |
| `debugging-expert` | engineering | - |
| `secure-code` | security | - |
| `security-reviewer` | security | `/analyze` |
| `testing` | testing | `/test` |

### Code Review (4)
| Skill | Domain | Delegated By |
|-------|--------|-------------|
| `python-code-review` | python | `/analyze` |
| `dotnet-code-review` | dotnet | `/analyze` |
| `angular-code-review` | angular | `/analyze` |
| `get-git-diff` | git | `python-code-review`, `dotnet-code-review`, `angular-code-review` |

### Test Generation (3)
| Skill | Domain | Delegated By |
|-------|--------|-------------|
| `generate-python-unit-tests` | python | `/test` |
| `generate-jest-unit-tests` | angular | `/test` |
| `test-cli-tools` | testing | `/test` |

### Infrastructure (5)
| Skill | Domain | Delegated By |
|-------|--------|-------------|
| `generate-azure-functions` | infrastructure | `/azure-function` |
| `generate-azure-pipelines` | infrastructure | `/azure-pipeline` |
| `generate-azure-bicep` | infrastructure | `/azure-pipeline` |
| `generate-tilt-dev-environment` | infrastructure | - |
| `generate-mock-service` | infrastructure | `/mock` |

### Planning & Workflow (9)
| Skill | Domain | Delegated By |
|-------|--------|-------------|
| `divine` | meta | - |
| `docs-workflow` | productivity | `/document` |
| `project-health` | meta | `/analyze` |
| `project-planning` | meta | - |
| `project-session-management` | meta | - |
| `project-workflow` | meta | - |
| `skill-creator` | meta | - |
| `skill-review` | meta | - |
| `sub-agent-patterns` | meta | - |

### Developer Workflow (3)
| Skill | Domain | Delegated By |
|-------|--------|-------------|
| `create-agents` | meta | - |
| `dev-tools` | engineering | - |
| `power-debug` | engineering | - |

### Specialized (8)
| Skill | Domain | Delegated By |
|-------|--------|-------------|
| `cli-developer` | engineering | - |
| `feature-forge` | engineering | - |
| `fullstack-development` | engineering | - |
| `legacy-modernizer` | engineering | - |
| `mcp-developer` | engineering | - |
| `monitoring-expert` | infrastructure | - |
| `prompt-engineer` | meta | - |
| `websocket-engineer` | engineering | - |

### Productivity (5)
| Skill | Domain | Delegated By |
|-------|--------|-------------|
| `commit-helper` | productivity | - |
| `documentation-generator` | productivity | `/document` |
| `email-writer` | productivity | - |
| `email-gateway` | productivity | - |
| `slack-message-composer` | productivity | - |

### Utilities (10)
| Skill | Domain | Delegated By |
|-------|--------|-------------|
| `color-palette` | frontend | - |
| `favicon-gen` | frontend | - |
| `firecrawl-scraper` | engineering | - |
| `icon-design` | frontend | - |
| `image-gen` | frontend | - |
| `jquery-4` | frontend | - |
| `office` | productivity | - |
| `open-source-contributions` | engineering | - |
| `playwright-local` | testing | - |

### Analysis (2)
| Skill | Domain | Delegated By |
|-------|--------|-------------|
| `file-schema-analysis` | schema | `/analyze` |
| `python-dependency-management` | python | - |

### Data Science (2)
| Skill | Domain | Delegated By |
|-------|--------|-------------|
| `excel-skills` | data-science | - |
| `jupyter-notebook-skills` | data-science | - |

### Meta (1)
| Skill | Domain | Delegated By |
|-------|--------|-------------|
| `generate-more-skills-with-claude` | meta | - |

> **Note**: An additional **212 external skills** are available via the Forge Marketplace plugins. See `README.md` and `ROADMAP.md` for the complete external skills catalog.

---

## Related Documents

- **Commands that delegate**: `commands/analyze.md`, `commands/test.md`, `commands/mock.md`, `commands/azure-pipeline.md`, `commands/azure-function.md`, `commands/document.md`
- **Skill template**: `skills/SKILL_TEMPLATE.md` - Defines the mandatory workflow all skills follow
- **Output conventions**: `skills/OUTPUT_CONVENTIONS.md` - Output file naming and location rules
- **Memory interface**: `interfaces/memory_store.md` - How skills interact with project memory

---

*Last Updated: 2026-02-12*
