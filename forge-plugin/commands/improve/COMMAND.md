---
name: improve
description: "Code improvement and refactoring with analysis-first approach and safe application"
category: workflow
complexity: standard
skills: [python-code-review, dotnet-code-review, angular-code-review]
context: [python, dotnet, angular, security, commands/refactoring_patterns]
---

# /improve - Code Improvement and Refactoring

## Triggers
- Code quality enhancement and refactoring requests
- Performance optimization and bottleneck resolution
- Maintainability improvements and technical debt reduction
- Best practices application and coding standards enforcement

## Usage
```
/improve [target] [--type quality|performance|maintainability|security] [--safe] [--preview]
```

**Parameters**:
- `target`: File, directory, or module to improve (required)
- `--type`: Improvement focus area (default: quality)
- `--safe`: Only apply auto-fixable improvements, prompt for everything else
- `--preview`: Show proposed changes without applying them

## Workflow

### Step 1: Identify Improvement Target

1. Parse target and improvement type
2. Detect language and framework
3. Read target files to understand current state
4. Identify test coverage for target code (verify tests exist before changing code)

### Step 2: Load Context & Memory

**Context Loading** (index-first approach):
1. Read `../../context/index.md` for overview
2. Read `../../context/commands/index.md` for command guidance
3. Load `../../context/commands/refactoring_patterns.md` for safe refactoring techniques
4. Based on detected language, load domain-specific context:
   - **Python**: `../../context/python/index.md` → `common_issues.md`, framework patterns
   - **.NET**: `../../context/dotnet/index.md` → `common_issues.md`, relevant patterns
   - **Angular**: `../../context/angular/index.md` → `common_issues.md`, relevant patterns
5. If `--type security`: Load `../../context/security/security_guidelines.md`

**Memory Loading**:
1. Determine project name
2. Check `../../memory/commands/{project}/improve_history.md` for past improvements
3. Load `../../memory/commands/{project}/analyze_insights.md` for known issues
4. Check skill memory for project conventions

### Step 3: Analyze Before Improving

**Always analyze first** - delegate to code review skills for assessment:

**Python projects**:
```
skill:python-code-review --target [files]
```

**.NET projects**:
```
skill:dotnet-code-review --target [files]
```

**Angular projects**:
```
skill:angular-code-review --target [files]
```

Use skill output to identify:
- Safe refactorings (can apply without risk)
- Risky changes (need user approval)
- Issues that should NOT be changed (known issues in memory)

### Step 4: Apply Improvements

**Auto-fix (apply automatically unless `--preview`)**:
- Import organization and cleanup
- Unused variable/import removal
- Whitespace and formatting fixes
- Simple type annotation additions
- Consistent naming within file scope

**Approval Required (prompt user first)**:
- Logic refactoring or algorithm changes
- Function signature changes
- Public API modifications
- Architectural restructuring
- Removing any functionality
- Changes affecting multiple files

**Will NOT apply without explicit `--force`**:
- Architectural decisions
- Code removal beyond clearly dead code
- Changes that would break existing tests

If `--preview`: Show all proposed changes without applying any.
If `--safe`: Only apply auto-fixable changes, list everything else as recommendations.

### Step 5: Validate Improvements

1. If tests exist for changed code, run them to verify no regressions
2. Check that improvements align with project conventions (from memory)
3. Verify no new issues introduced

### Step 6: Generate Output & Update Memory

**Output**:
Save results to `/claudedocs/improve_{target}_{date}.md`:

```markdown
# Improvement Report - {Target}
**Date**: {date}
**Command**: /improve {full invocation}
**Project**: {name}
**Type**: {quality|performance|maintainability|security}

## Summary
- **Changes Applied**: {count}
- **Changes Recommended**: {count} (need approval)
- **Issues Skipped**: {count} (known issues from memory)

## Applied Changes
### {Change 1}
- **File**: {path}:{line}
- **Type**: {auto-fix category}
- **Before**: {brief description}
- **After**: {brief description}

## Recommended Changes (Need Approval)
### {Change 1}
- **File**: {path}:{line}
- **Issue**: {description}
- **Proposed Fix**: {description}
- **Risk**: {low|medium|high}
- **Impact**: {description}

## Skipped (Known Issues)
{Issues found but not flagged per project memory}

## Validation
- Tests: {pass|fail|not available}
- Regressions: {none|list}

## Next Steps
- Apply recommended changes with `/improve --force`
- Run `/test` to validate all changes
- Run `/analyze` to verify improvement
```

**Memory Updates**:
1. Append to `../../memory/commands/{project}/command_history.md`
2. Update `../../memory/commands/{project}/improve_history.md`:
   - Changes applied, patterns improved, recurring issues

## Tool Coordination
- **Read/Grep/Glob**: Code analysis and improvement opportunity identification
- **Edit**: Safe code modifications and refactoring
- **Bash**: Test execution for validation
- **Write**: Improvement reports

## Key Patterns
- **Analyze First**: Always assess with code review skills before improving
- **Safe by Default**: Auto-fix only safe changes; prompt for everything else
- **Memory-Aware**: Check known issues before flagging problems
- **Test-Protected**: Verify tests exist before modifying code

## Boundaries

**Will:**
- Apply systematic improvements with domain-specific expertise
- Analyze before improving (via skill delegation)
- Respect project conventions from memory
- Validate improvements against existing tests

**Will Not:**
- Apply risky improvements without user confirmation
- Change code that has no test coverage without warning
- Override project-specific conventions with generic best practices
- Modify code marked as known issues in memory

**Output**: Improvement report saved to `/claudedocs/improve_{target}_{date}.md`

**Next Step**: Use `/test` to validate changes, or `/analyze` to verify improvement quality.
