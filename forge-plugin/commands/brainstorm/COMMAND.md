---
name: brainstorm
description: "Interactive requirements discovery through Socratic dialogue and systematic exploration"
category: orchestration
complexity: advanced
skills: [file-schema-analysis, database-schema-analysis]
context: [commands/brainstorming_patterns]
---

# /brainstorm - Interactive Requirements Discovery

## Triggers
- Ambiguous project ideas requiring structured exploration
- Requirements discovery and specification development
- Concept validation and feasibility assessment
- Feature planning and scope definition

## Usage
```
/brainstorm [topic/idea] [--depth shallow|normal|deep] [--output requirements|stories|both]
```

**Parameters**:
- `topic/idea`: The concept or feature to explore (required)
- `--depth`: Exploration thoroughness (default: normal)
  - `shallow`: Quick exploration, 3-5 questions
  - `normal`: Standard exploration, 5-10 questions
  - `deep`: Comprehensive exploration, 10+ questions with feasibility analysis
- `--output`: Output format (default: both)

## Workflow

### Step 1: Understand the Idea

1. Parse the topic/idea description
2. Identify the domain (web app, API, data pipeline, infrastructure, etc.)
3. Assess initial complexity and scope
4. If existing codebase: Analyze current architecture for context

### Step 2: Load Context & Memory

**Context Loading**:
1. Read `../../context/commands/index.md` for command guidance
2. Load `../../context/commands/brainstorming_patterns.md` for questioning techniques
3. If data modeling involved: Load `../../context/schema/index.md`

**Memory Loading**:
1. Determine project name
2. Check `../../memory/commands/{project}/brainstorm_notes.md` for past brainstorming
3. Load relevant skill memory for existing project understanding

### Step 3: Socratic Dialogue

Engage in progressive questioning to clarify requirements:

**Phase 1 - Clarifying (Always)**:
- What problem does this solve?
- Who is the primary user?
- What does success look like?

**Phase 2 - Probing (Normal + Deep)**:
- What assumptions are we making?
- What are the constraints (technical, business, regulatory)?
- How does this integrate with existing systems?
- What are the edge cases?

**Phase 3 - Exploring (Deep only)**:
- What's the minimum viable version?
- What's the ideal version?
- What are the risks and unknowns?
- What data is needed and where does it come from?

**Questioning Strategy**:
- Ask 2-3 questions at a time (not overwhelming)
- Build on previous answers
- Challenge assumptions respectfully
- Offer options when users are uncertain

### Step 4: Skill Delegation (if applicable)

When brainstorming involves data modeling:

**File schema analysis**:
```
skill:file-schema-analysis --target [existing schemas]
```
Understand current data structures to inform new feature design

**Database schema analysis**:
```
skill:database-schema-analysis --target [existing database]
```
Map current data model to identify integration points

### Step 5: Generate Requirements

Based on dialogue, produce:

**Functional Requirements**:
- User stories with acceptance criteria
- Feature list with priority (Must/Should/Could/Won't)
- Edge cases and error scenarios

**Non-Functional Requirements**:
- Performance targets
- Security requirements
- Scalability expectations
- Compliance needs

**Scope Assessment**:
- T-shirt size estimate (XS/S/M/L/XL)
- Risk assessment (High/Medium/Low)
- Open questions for further exploration

### Step 6: Generate Output & Update Memory

**Output**:
Save results to `/claudedocs/requirements_{topic}_{date}.md`:

```markdown
# Requirements - {Topic}
**Date**: {date}
**Command**: /brainstorm {full invocation}
**Project**: {name}
**Depth**: {shallow|normal|deep}

## Problem Statement
{What problem are we solving and for whom?}

## Goals
{What does success look like?}

## User Stories
### Story 1: {Title}
**As a** {role}, **I want to** {action} **so that** {benefit}

**Acceptance Criteria**:
- [ ] Given {context}, when {action}, then {result}

### Story 2: {Title}
...

## Functional Requirements
| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR-1 | {requirement} | Must | {notes} |

## Non-Functional Requirements
| Category | Requirement | Target |
|----------|-------------|--------|
| Performance | {requirement} | {target} |
| Security | {requirement} | {target} |

## Scope Estimate
- **Size**: {T-shirt size}
- **Risk**: {High|Medium|Low}
- **Key Risks**: {list}

## Open Questions
1. {unresolved question}
2. {unresolved question}

## Next Steps
- Use `/implement` to begin development
- Use `/analyze` to assess existing codebase for integration points
```

**Memory Updates**:
1. Append to `../../memory/commands/{project}/command_history.md`
2. Update `../../memory/commands/{project}/brainstorm_notes.md`:
   - Requirements gathered, decisions made, open questions

## Tool Coordination
- **Read**: Existing codebase analysis for context
- **Grep/Glob**: Pattern detection in existing code
- **Write**: Requirements document generation
- **WebSearch**: Technology validation and market research (when needed)

## Key Patterns
- **Progressive Depth**: Start broad, narrow based on answers
- **User-Centered**: Focus on who uses it and why
- **Feasibility-Aware**: Consider technical constraints throughout
- **Memory-Enhanced**: Build on past brainstorming sessions

## Boundaries

**Will:**
- Transform ambiguous ideas into concrete requirements through dialogue
- Generate requirements documents with user stories and acceptance criteria
- Assess feasibility and identify risks
- Delegate to schema analysis skills for data modeling context

**Will Not:**
- Create architecture designs or system diagrams (use `/implement` for that)
- Generate implementation code during brainstorming
- Make final architectural decisions without user input
- Design database schemas (only discuss requirements for them)
- Skip Socratic dialogue and jump to solutions

**Output**: Requirements document saved to `/claudedocs/requirements_{topic}_{date}.md`

**Next Step**: Use `/implement` to begin development, or `/analyze` to assess existing code for integration.
