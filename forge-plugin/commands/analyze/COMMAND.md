---
name: analyze
description: "Comprehensive code analysis across quality, security, performance, and architecture domains"
category: utility
complexity: basic
skills: [python-code-review, dotnet-code-review, angular-code-review]
context: [python, dotnet, angular, security, commands/analysis_patterns]
---

# /analyze - Code Analysis and Quality Assessment

## Triggers
- Code quality assessment requests for projects or specific components
- Security vulnerability scanning and compliance validation
- Performance bottleneck identification and optimization planning
- Architecture review and technical debt assessment

## Usage
```
/analyze [target] [--focus quality|security|performance|architecture] [--depth quick|deep]
```

**Parameters**:
- `target`: File, directory, or module to analyze (default: entire project)
- `--focus`: Analysis domain to prioritize (default: all domains)
- `--depth`: Analysis depth - `quick` for overview, `deep` for comprehensive (default: quick)

## Workflow

### Step 1: Initial Analysis

1. Identify the analysis target (files, directories, or entire project)
2. Detect language and framework:
   - Check file extensions and configuration files
   - Identify project type (Python, .NET, Angular, etc.)
   - Note multi-language projects for combined analysis
3. Determine analysis scope based on `--focus` and `--depth` flags

### Step 2: Load Context & Memory

**Context Loading** (index-first approach):
1. Use `contextProvider.getDomainIndex("commands")` for command-specific guidance
2. Use `contextProvider.getConditionalContext("commands", {"command": "analyze"})` to load analysis methodologies
3. Based on detected language, load domain-specific context:
   - **Python**: Use `contextProvider.getDomainIndex("python")`, then `contextProvider.getAlwaysLoadFiles("python")` and `contextProvider.getConditionalContext("python", detection)`
   - **.NET**: Use `contextProvider.getDomainIndex("dotnet")`, then `contextProvider.getAlwaysLoadFiles("dotnet")` and `contextProvider.getConditionalContext("dotnet", detection)`
   - **Angular**: Use `contextProvider.getDomainIndex("angular")`, then `contextProvider.getAlwaysLoadFiles("angular")` and `contextProvider.getConditionalContext("angular", detection)`
4. If `--focus security`: Use `contextProvider.getCrossDomainContext("{domain}", ["security_focus"])` to load security guidelines

**Memory Loading**:
1. Determine project name (from git repo name or directory)
2. Use `memoryStore.getCommandMemory("{project}")` to load past analyses and insights
3. Use `memoryStore.getSharedProjectMemory("{project}")` for cross-skill project knowledge

See [ContextProvider](../../interfaces/context_provider.md) and [MemoryStore](../../interfaces/memory_store.md) interfaces.

### Step 3: Execute Analysis

**For `--depth quick`**:
1. Scan project structure and identify key files
2. Apply pattern matching for common issues per detected language
3. Classify findings by severity (Critical/High/Medium/Low)
4. Generate prioritized finding list

**For `--depth deep`**:
1. Perform comprehensive file-by-file analysis
2. Cross-reference findings across files for systemic issues
3. Identify architectural patterns and anti-patterns
4. Generate detailed findings with code references

**Analysis Domains**:
- **Quality**: Complexity, duplication, naming, organization
- **Security**: OWASP patterns, input validation, auth issues
- **Performance**: Algorithm complexity, query patterns, memory usage
- **Architecture**: SOLID adherence, coupling, dependency direction

### Step 4: Skill Delegation (Deep Analysis)

When `--depth deep` is specified or significant issues are found, delegate to specialized skills:

**Python projects**:
```
skill:python-code-review --target [files] --depth deep
```
Process skill output: Incorporate review findings into analysis report

**.NET projects**:
```
skill:dotnet-code-review --target [files] --depth deep
```
Process skill output: Merge .NET-specific findings with overall analysis

**Angular projects**:
```
skill:angular-code-review --target [files] --depth deep
```
Process skill output: Integrate Angular-specific patterns

**Multi-language projects**: Invoke multiple skills and aggregate results

### Step 5: Generate Output & Update Memory

**Output**:
Save results to `/claudedocs/analyze_{target}_{date}.md` using this format:

```markdown
# Analysis Results - {Target}
**Date**: {date}
**Command**: /analyze {full invocation}
**Project**: {name}
**Language(s)**: {detected languages}
**Depth**: {quick|deep}

## Summary
- **Total Findings**: {count} ({critical} critical, {high} high, {medium} medium, {low} low)
- **Files Analyzed**: {count}
- **Key Concern**: {most important finding}

## Findings by Severity

### Critical
{findings}

### High
{findings}

### Medium
{findings}

### Low
{findings}

## Metrics
- Complexity: {assessment}
- Security: {assessment}
- Performance: {assessment}
- Architecture: {assessment}

## Recommendations
1. {prioritized recommendation}
2. {prioritized recommendation}

## Next Steps
- Use `/improve` to apply recommended fixes
- Use `/test` to validate after changes
```

**Memory Updates**:
1. Use `memoryStore.append("command/{project}/command_history", ...)` to record:
   - Date, command invocation, result summary, output file path
2. Use `memoryStore.update("command/{project}/analyze_insights", ...)` to record:
   - Patterns observed, recurring issues, project characteristics

See [MemoryStore Interface](../../interfaces/memory_store.md) for `update()` and `append()` method details.

## Tool Coordination
- **Glob**: File discovery and project structure analysis
- **Grep**: Pattern matching and code search
- **Read**: Source code inspection and configuration analysis
- **Bash**: External tool execution (linters, static analyzers) when available
- **Write**: Report generation

## Key Patterns
- **Language Detection**: File extensions + config files → appropriate analysis pipeline
- **Severity Classification**: Impact + likelihood → prioritized findings
- **Skill Delegation**: Complex analysis → specialized code review skills
- **Incremental Learning**: Memory from past analyses → fewer false positives

## Boundaries

**Will:**
- Perform comprehensive static code analysis across multiple domains
- Generate severity-rated findings with actionable recommendations
- Delegate to specialized skills for deep analysis
- Learn from past analyses via memory system

**Will Not:**
- Execute dynamic analysis requiring code compilation or runtime
- Modify source code or apply fixes without explicit user consent
- Analyze external dependencies beyond import and usage patterns
- Replace full skill invocations (skills provide deeper analysis)

**Output**: Analysis report saved to `/claudedocs/analyze_{target}_{date}.md`

**Next Step**: Use `/improve` to apply recommended fixes, or `/test` to validate current state.
