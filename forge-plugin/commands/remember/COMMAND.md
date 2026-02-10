---
name: remember
description: "Store and retrieve project-specific wisdom, patterns, and decisions in organized memory"
category: utility
complexity: basic
skills: []
context: [commands/memory_patterns]
---

# /remember - Project Memory Management

## Triggers
- Storing important decisions, patterns, or conventions discovered during development
- Documenting project-specific knowledge for future reference
- Recording lessons learned from debugging or optimization
- Capturing team conventions and coding standards

## Usage
```
/remember [content] [--category decision|pattern|convention|lesson] [--scope project|skill]
```

**Parameters**:
- `content`: The knowledge to store (can be provided inline or interactively)
- `--category`: Type of memory (default: decision)
  - `decision`: Architectural or technical decisions
  - `pattern`: Recurring patterns or solutions
  - `convention`: Coding standards or team conventions
  - `lesson`: Lessons learned from experience
- `--scope`: Memory scope (default: project)
  - `project`: Project-wide memory
  - `skill`: Skill-specific memory

## Workflow

### Step 1: Parse Input

1. Identify what needs to be remembered:
   - If content provided inline: Use it directly
   - If content missing: Prompt user with guided questions
2. Determine category and scope from flags
3. Detect project name from git repository or directory

### Step 2: Load Context & Existing Memory

**Context Loading**:
1. Read `../../context/commands/index.md` for command guidance
2. Load `../../context/commands/memory_patterns.md` (if exists) for memory organization patterns

**Memory Loading**:
1. Determine project name (from git repo name or directory)
2. Check existing memory structure in `../../memory/`
3. Load relevant existing memory files:
   - Project memory: `../../memory/commands/{project}/`
   - Skill memory: `../../memory/skills/{skill}/{project}/`

### Step 3: Interactive Capture (if needed)

If content not provided inline, guide user through structured capture:

**For Decisions**:
- What decision was made?
- What alternatives were considered?
- Why was this option chosen?
- What are the trade-offs?

**For Patterns**:
- What problem does this pattern solve?
- When should this pattern be used?
- What are the key implementation details?

**For Conventions**:
- What is the convention?
- Where does it apply (files, naming, structure)?
- Are there exceptions?

**For Lessons**:
- What was the challenge or issue?
- How was it resolved?
- What should be avoided or preferred in the future?

### Step 4: Organize & Store Memory

Based on category and scope, store memory in appropriate location:

**Project-scoped decisions**:
- Path: `../../memory/commands/{project}/decisions.md`
- Format: Timestamped entries with context

**Project-scoped patterns**:
- Path: `../../memory/commands/{project}/patterns.md`
- Format: Pattern name, use case, implementation notes

**Project-scoped conventions**:
- Path: `../../memory/commands/{project}/conventions.md`
- Format: Categorized list (naming, structure, testing, etc.)

**Project-scoped lessons**:
- Path: `../../memory/commands/{project}/lessons_learned.md`
- Format: Challenge, solution, takeaway

**Skill-scoped memory**:
- Path: `../../memory/skills/{skill}/{project}/notes.md`
- Format: Skill-specific observations and learnings

### Step 5: Generate Confirmation & Update Index

**Output**:
Provide confirmation message:

```markdown
✓ Memory stored successfully

**Category**: {category}
**Scope**: {project|skill}
**Location**: {file path}

**Summary**: {brief summary of what was stored}

The knowledge has been added to project memory and will be available for future commands and skills.
```

**Memory Index Update**:
1. Update `../../memory/commands/{project}/index.md` with new entry
2. Include timestamp, category, and brief summary
3. Ensure easy retrieval for future commands

## Tool Coordination
- **Read**: Load existing memory files
- **Write**: Store new memory entries
- **Grep**: Search existing memory for duplicates or related entries
- **Bash**: Git operations for tracking memory changes (optional)

## Key Patterns
- **Structured Capture**: Guided questions ensure complete information
- **Organized Storage**: Category-based organization for easy retrieval
- **Incremental Learning**: Memory grows over time with each entry
- **Searchable**: Memory files use consistent format for grep/search

## Boundaries

**Will:**
- Store project-specific decisions, patterns, conventions, and lessons
- Organize memory in a structured, searchable format
- Provide interactive capture when content not provided
- Update memory index for easy discovery

**Will Not:**
- Store sensitive information (credentials, API keys) - use environment variables
- Replace documentation - memory is for project-specific knowledge
- Store code snippets - use skills or templates for reusable code
- Automatically capture everything - user explicitly decides what to remember

**Output**: Confirmation message with storage location

**Next Step**: Use `/analyze`, `/implement`, or `/improve` commands - they will automatically load relevant project memory.
