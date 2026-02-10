---
name: document
description: "Documentation generation for components, APIs, and features with language-specific conventions"
category: utility
complexity: basic
skills: []
context: [python, dotnet, angular, commands/documentation_standards]
---

# /document - Documentation Generation

## Triggers
- Documentation requests for specific components, functions, or features
- API documentation and reference material generation
- Inline code documentation (docstrings, JSDoc, XML comments)
- README and user guide creation

## Usage
```
/document [target] [--type inline|external|api|guide] [--style brief|detailed]
```

**Parameters**:
- `target`: File, directory, module, or feature to document (required)
- `--type`: Documentation format (default: inline)
  - `inline`: Add docstrings, comments, type annotations to code
  - `external`: Create separate documentation files
  - `api`: Generate API reference documentation
  - `guide`: Create user-focused how-to guide
- `--style`: Documentation depth (default: brief)

## Workflow

### Step 1: Analyze Documentation Target

1. Read target files to understand structure and interfaces
2. Detect language and framework
3. Identify existing documentation (what exists vs what's missing)
4. Determine public interfaces that need documentation

### Step 2: Load Context & Memory

**Context Loading** (index-first approach):
1. Read `../../context/commands/index.md` for command guidance
2. Load `../../context/commands/documentation_standards.md` for format conventions
3. Based on detected language, load domain-specific doc standards:
   - **Python**: Google/NumPy docstring style, PEP 257
   - **.NET**: XML documentation comment patterns
   - **TypeScript/Angular**: JSDoc/TSDoc patterns

**Memory Loading**:
1. Determine project name
2. Check `../../memory/commands/{project}/document_conventions.md` for established patterns
3. If first run: Detect existing documentation style from codebase

### Step 3: Generate Documentation

**For `--type inline`**:
1. Identify functions, classes, and methods missing docstrings
2. Generate documentation following detected language convention:
   - **Python**: Google-style docstrings with Args, Returns, Raises
   - **C#**: XML doc comments with summary, param, returns, exception
   - **TypeScript**: JSDoc with @param, @returns, @throws
3. Add type annotations where missing and beneficial
4. Add clarifying comments only where logic is non-obvious

**For `--type external`**:
1. Analyze component structure and public interfaces
2. Generate markdown documentation with:
   - Component overview and purpose
   - API reference (methods, properties, events)
   - Usage examples
   - Configuration options
3. Save to appropriate location (alongside code or in docs directory)

**For `--type api`**:
1. Extract all public endpoints/methods
2. Document each with: method, path/signature, parameters, responses, examples
3. Generate in markdown or OpenAPI format based on project type
4. Include authentication requirements and error codes

**For `--type guide`**:
1. Analyze feature from user perspective
2. Create step-by-step usage guide with:
   - Prerequisites
   - Quick start
   - Detailed usage
   - Common patterns
   - Troubleshooting

### Step 4: Apply Documentation

**Inline documentation**: Edit source files to add docstrings and comments
**External documentation**: Create new markdown files in appropriate location
**API documentation**: Generate reference files
**User guides**: Create guide files in docs directory

### Step 5: Generate Output & Update Memory

**Output**:
- Inline: Modified source files with added documentation
- External: New documentation files saved to project
- Report saved to `/claudedocs/document_{target}_{date}.md`:

```markdown
# Documentation Report - {Target}
**Date**: {date}
**Command**: /document {full invocation}
**Project**: {name}
**Type**: {inline|external|api|guide}

## Summary
- **Files Documented**: {count}
- **Functions/Methods Documented**: {count}
- **New Documentation Files**: {list}

## Coverage
- **Before**: {percentage of documented public interfaces}
- **After**: {percentage after documentation}

## Files Modified
- `path/to/file.py` - Added {count} docstrings
- `docs/api_reference.md` - New file

## Style Applied
{Documentation convention used}

## Next Steps
- Review generated documentation for accuracy
- Run `/analyze` to check overall documentation coverage
```

**Memory Updates**:
1. Append to `../../memory/commands/{project}/command_history.md`
2. Update `../../memory/commands/{project}/document_conventions.md`:
   - Documentation style used, conventions detected, preferences learned

## Tool Coordination
- **Read**: Source code analysis and existing documentation review
- **Grep**: Reference extraction and pattern identification
- **Edit**: Adding inline documentation to source files
- **Write**: Creating new documentation files
- **Glob**: Multi-file documentation discovery

## Key Patterns
- **Convention Detection**: Analyze existing docs → match established style
- **Public-First**: Document public interfaces before internal implementation
- **Context-Aware**: Language-specific documentation formats and conventions
- **Completeness Focus**: Identify and fill documentation gaps

## Boundaries

**Will:**
- Generate focused documentation following project conventions
- Create multiple documentation formats (inline, external, API, guide)
- Detect and match existing documentation style
- Track documentation coverage improvements

**Will Not:**
- Override existing documentation without explicit request
- Generate documentation that exposes sensitive implementation details
- Create verbose documentation for self-explanatory code
- Modify code logic while adding documentation

**Output**: Documentation in source files and/or `/claudedocs/document_{target}_{date}.md`

**Next Step**: Review generated documentation, then use `/analyze` to verify quality.
