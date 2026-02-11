# Commands Directory Index

This directory contains **commands** - structured workflows that bridge the gap between quick operations and deep skill analyses. Commands leverage forge's three-layer architecture (Context/Memory/Skills) while remaining more flexible than mandatory skill workflows.

## Commands vs Skills

| Aspect | Commands | Skills |
|--------|----------|--------|
| **Structure** | Structured workflows | Mandatory step sequences |
| **Flexibility** | Adaptive to context | Strict compliance checklists |
| **Use Case** | Quick-to-moderate operations | Deep, specialized analysis |
| **Context Loading** | Index-first, load relevant | Index-first, load relevant |
| **Memory Updates** | Append to command history | Full memory lifecycle |
| **Output** | `/claudedocs` reports | `/claudedocs` reports |
| **Skill Delegation** | Can invoke skills | Are the skills |
| **Compliance** | Best-effort quality | Non-negotiable checklists |

## When to Use Commands vs Skills

**Use Commands when:**
- You need a quick analysis or operation
- The task spans multiple domains (analysis + improvement)
- You want flexibility in approach
- The task doesn't require deep, specialized analysis

**Use Skills directly when:**
- You need deep, specialized analysis (e.g., full .NET code review)
- The task matches a specific skill's mandatory workflow
- You need comprehensive memory tracking
- Quality compliance is critical

## Available Commands

| Command | Category | Description | Related Skills |
|---------|----------|-------------|----------------|
| [`/analyze`](analyze/COMMAND.md) | utility | Code analysis and quality assessment | `python-code-review`, `dotnet-code-review`, `angular-code-review` |
| [`/implement`](implement/COMMAND.md) | workflow | Feature implementation with testing | `generate-python-unit-tests`, `generate-jest-unit-tests` |
| [`/improve`](improve/COMMAND.md) | workflow | Code improvement and refactoring | `python-code-review`, `dotnet-code-review` |
| [`/document`](document/COMMAND.md) | utility | Documentation generation | N/A |
| [`/test`](test/COMMAND.md) | utility | Test execution and validation | `test-cli-tools`, `generate-python-unit-tests`, `generate-jest-unit-tests` |
| [`/build`](build/COMMAND.md) | utility | Project building and packaging | `generate-tilt-dev-environment` |
| [`/brainstorm`](brainstorm/COMMAND.md) | orchestration | Requirements discovery and planning | `file-schema-analysis`, `database-schema-analysis` |
| [`/remember`](remember/COMMAND.md) | utility | Memory management and recall | N/A |
| [`/mock`](mock/COMMAND.md) | workflow | Mock service generation | `generate-mock-service` |
| [`/azure-pipeline`](azure-pipeline/COMMAND.md) | workflow | Azure DevOps pipeline generation | `generate-azure-pipelines` |
| [`/etl-pipeline`](etl-pipeline/COMMAND.md) | workflow | ETL pipeline scaffolding | `database-schema-analysis`, `file-schema-analysis` |
| [`/azure-function`](azure-function/COMMAND.md) | workflow | Azure Function generation | `generate-azure-functions` |

## Command Selection Matrix

| Need | Recommended Command | When to Use Skill Instead |
|------|-------------------|---------------------------|
| Quick code quality check | `/analyze` | Use `skill:python-code-review` for full review with memory |
| Implement a feature | `/implement` | N/A - command is the right choice |
| Refactor code | `/improve` | Use code review skill first for deep analysis |
| Generate docs | `/document` | N/A - command is the right choice |
| Run tests | `/test` | Use `skill:test-cli-tools` for systematic CLI testing |
| Build project | `/build` | N/A - command is the right choice |
| Explore requirements | `/brainstorm` | Use schema analysis skills for data modeling |
| Store/recall knowledge | `/remember` | N/A - command is the right choice |
| Create mock services | `/mock` | Use `skill:generate-mock-service` for fine-grained control |
| Azure pipeline setup | `/azure-pipeline` | Use `skill:generate-azure-pipelines` for customization |
| ETL pipeline creation | `/etl-pipeline` | Use schema analysis skills for data modeling first |
| Azure function setup | `/azure-function` | Use `skill:generate-azure-functions` for advanced config |

## Command Workflow Pattern

All commands follow this general pattern:

### 1. Initial Analysis
- Detect language, framework, and project type
- Understand the target (files, directories, features)

### 2. Load Context & Memory
**Context Loading** (index-first approach):
1. Read `../context/index.md` for overview
2. Read `../context/{domain}/index.md` for domain-specific guidance
3. Read `../context/commands/index.md` for command context
4. Load relevant context files based on indexes

**Memory Loading**:
1. Check `../memory/commands/{project}/command_history.md`
2. Load `../memory/commands/{project}/{command}_insights.md` if exists

### 3. Execute Primary Action
- Perform the command's core functionality
- Delegate to skills when deep analysis is needed

### 4. Generate Output & Update Memory
**Output**: Save results to `/claudedocs/{command}_{target}_{timestamp}.md`

**Memory Updates**:
- Append to `command_history.md`
- Update `{command}_insights.md` with learnings

## Output Standards

All commands save output to `/claudedocs` with this format:

```markdown
# {Command} Results - {Target}
**Date**: {timestamp}
**Command**: {full invocation}
**Project**: {name}

## Summary
[High-level results]

## Details
[Comprehensive findings]

## Next Steps
[Recommended follow-up actions]
```

## Integration Patterns

### Skill Delegation
Commands can invoke skills for deep analysis:
```
/analyze src/auth --focus security
  → Detects Python
  → Invokes skill:python-code-review for deep security analysis
  → Aggregates and formats results
```

### Command Chaining
Commands recommend follow-up commands:
```
/analyze → findings → /improve → apply fixes → /test → validate
/brainstorm → requirements → /implement → code → /test → validate
```

---

## Directory Structure

```
commands/
├── index.md (this file)
├── analyze/
│   ├── COMMAND.md
│   └── examples.md
├── azure-function/
│   ├── COMMAND.md
│   └── examples.md
├── azure-pipeline/
│   ├── COMMAND.md
│   └── examples.md
├── brainstorm/
│   ├── COMMAND.md
│   └── examples.md
├── build/
│   ├── COMMAND.md
│   └── examples.md
├── document/
│   ├── COMMAND.md
│   └── examples.md
├── etl-pipeline/
│   ├── COMMAND.md
│   └── examples.md
├── implement/
│   ├── COMMAND.md
│   └── examples.md
├── improve/
│   ├── COMMAND.md
│   └── examples.md
├── mock/
│   ├── COMMAND.md
│   └── examples.md
├── remember/
│   ├── COMMAND.md
│   └── examples.md
└── test/
    ├── COMMAND.md
    └── examples.md
```

## Related Documentation

- **Skills**: See `../skills/` for deep analysis workflows
- **Context**: See `../context/` for shared knowledge
- **Memory**: See `../memory/` for project-specific learning
- **Plugin**: See `../.claude-plugin/plugin.json` for plugin metadata
