# Commands Memory Index

This directory stores **project-specific command execution history and insights**. Unlike skill memory (which tracks deep analysis patterns), command memory tracks execution history, learned preferences, and accumulated insights from command usage.

## Purpose

Command memory enables:
- **Execution History**: Track which commands were run, when, and what they found
- **Accumulated Insights**: Remember patterns discovered across multiple command executions
- **Project Preferences**: Learn project-specific conventions and preferences
- **Continuity**: Build on previous command results in future sessions

## Memory vs Skill Memory

| Aspect | Command Memory (this directory) | Skill Memory (`../skills/`) |
|--------|--------------------------------|------------------------------|
| **Scope** | Cross-command execution tracking | Per-skill deep analysis |
| **Granularity** | Summary-level insights | Detailed patterns and issues |
| **Update Frequency** | Every command execution | Every skill invocation |
| **Content** | Command history, quick insights | Project overview, known issues, review history |
| **Growth** | Linear (append history) | Structured (refine understanding) |

## Directory Structure

```
memory/commands/
├── index.md (this file)
└── {project-name}/              # Per-project command memory
    ├── command_history.md       # All command executions (append-only)
    ├── analyze_insights.md      # Insights from /analyze runs
    ├── implement_patterns.md    # Patterns from /implement runs
    ├── improve_history.md       # Improvement tracking
    ├── document_conventions.md  # Documentation preferences
    ├── test_results.md          # Test execution history
    ├── build_config.md          # Build configuration insights
    └── brainstorm_notes.md      # Requirements and ideas
```

## Memory Lifecycle

### First Command Execution (New Project)

1. Command detects project name (from git repo name or directory)
2. Checks `memory/commands/{project-name}/` - directory doesn't exist
3. Executes command using only context files
4. Creates memory directory and initial files:
   - `command_history.md` with first entry
   - `{command}_insights.md` with initial findings

### Subsequent Command Executions

1. Checks `memory/commands/{project-name}/` - directory exists
2. Reads `command_history.md` for previous executions
3. Reads `{command}_insights.md` for accumulated insights
4. Executes command with enhanced context
5. Appends to `command_history.md`
6. Updates `{command}_insights.md` with new learnings

## Memory File Formats

### command_history.md (Append-Only Log)

```markdown
# Command History - {project-name}

## 2026-02-09 14:30 - /analyze src/auth --focus security
**Result**: 3 high, 5 medium findings
**Key Finding**: SQL injection risk in user_queries.py
**Output**: /claudedocs/analyze_auth_20260209.md

## 2026-02-09 15:00 - /test src/auth
**Result**: 45/50 tests passing, 5 failures
**Key Finding**: Missing edge case tests for token expiry
**Output**: /claudedocs/test_auth_20260209.md
```

### {command}_insights.md (Evolving Insights)

```markdown
# Analyze Insights - {project-name}

## Project Patterns
- Authentication uses JWT with custom middleware
- Database queries use raw SQL (not ORM) in legacy modules
- Security headers configured in middleware.py

## Recurring Issues
- SQL injection in legacy query builders (found 3 times)
- Missing input validation on API endpoints

## Preferences
- Team prefers detailed security reports
- Focus areas: auth, payments, user data
```

## Memory Best Practices

### DO
- Append to `command_history.md` after every command execution
- Update insight files with genuinely new patterns
- Keep entries concise (1-3 lines per execution)
- Include output file paths for reference
- Date all entries

### DON'T
- Duplicate information already in skill memory
- Store full command output (that's in `/claudedocs`)
- Let history grow unbounded (archive after 50 entries)
- Store project-wide knowledge (that belongs in skill memory)

## Integration with Commands

Commands follow this memory workflow:

1. **Before execution**: Read `command_history.md` and relevant insight file
2. **During execution**: Apply learned patterns and preferences
3. **After execution**: Append history entry and update insights

## Related Documentation

- **Commands**: See `../../commands/index.md` for command documentation
- **Skill Memory**: See `../index.md` for deep analysis memory
- **Context**: See `../../context/commands/index.md` for command context
