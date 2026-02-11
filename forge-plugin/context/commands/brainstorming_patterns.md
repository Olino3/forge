---
id: "commands/brainstorming_patterns"
domain: commands
title: "Brainstorming Patterns"
type: pattern
estimatedTokens: 1200
loadingStrategy: onDemand
version: "0.1.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "Socratic Questioning Techniques"
    estimatedTokens: 135
    keywords: [socratic, questioning, techniques]
  - name: "Requirements Elicitation"
    estimatedTokens: 78
    keywords: [requirements, elicitation]
  - name: "Feature: {name}"
    estimatedTokens: 53
    keywords: [feature, name]
  - name: "Feasibility Analysis"
    estimatedTokens: 139
    keywords: [feasibility, analysis]
  - name: "Prioritization Frameworks"
    estimatedTokens: 110
    keywords: [prioritization, frameworks]
  - name: "Brainstorming Output Format"
    estimatedTokens: 20
    keywords: [brainstorming, output, format]
  - name: "Problem Statement"
    estimatedTokens: 20
    keywords: [problem, statement]
  - name: "Goals"
    estimatedTokens: 20
    keywords: [goals]
  - name: "User Stories"
    estimatedTokens: 20
    keywords: [user, stories]
  - name: "Functional Requirements"
    estimatedTokens: 20
    keywords: [functional, requirements]
  - name: "Non-Functional Requirements"
    estimatedTokens: 20
    keywords: [non-functional, requirements]
  - name: "Constraints"
    estimatedTokens: 20
    keywords: [constraints]
  - name: "Open Questions"
    estimatedTokens: 20
    keywords: [open, questions]
  - name: "Risks"
    estimatedTokens: 20
    keywords: [risks]
  - name: "Estimated Scope"
    estimatedTokens: 20
    keywords: [estimated, scope]
  - name: "Skill Integration"
    estimatedTokens: 15
    keywords: [skill, integration]
  - name: "Boundaries"
    estimatedTokens: 45
    keywords: [boundaries]
  - name: "Official References"
    estimatedTokens: 20
    keywords: [official, references]
tags: [commands, brainstorming, requirements, socratic, prioritization, feasibility]
---

# Brainstorming Patterns

Reference patterns for the `/brainstorm` command. Covers Socratic questioning, requirements elicitation, feasibility analysis, and prioritization techniques.

## Socratic Questioning Techniques

### Progressive Depth
Start broad, narrow progressively:

1. **Clarifying Questions**: "What do you mean by...?" "Can you give an example?"
2. **Probing Assumptions**: "What are you assuming about...?" "Is that always the case?"
3. **Exploring Implications**: "What would happen if...?" "How would that affect...?"
4. **Questioning Viewpoints**: "What's an alternative approach?" "Who would disagree?"
5. **Evaluating Evidence**: "What data supports this?" "How would you validate?"

### Domain-Specific Questions

**For Features**:
- Who is the primary user of this feature?
- What problem does it solve?
- How do users currently solve this problem?
- What's the minimum viable version?
- What would make this feature delightful vs adequate?

**For Architecture**:
- What are the scalability requirements?
- What are the consistency/availability trade-offs?
- What existing systems does this need to integrate with?
- What's the expected data volume?
- What are the latency requirements?

**For Data Models**:
- What entities are involved?
- What are the relationships between them?
- What queries need to be fast?
- How does the data change over time?
- What's the data retention policy?

## Requirements Elicitation

### Functional Requirements
- **User Stories**: "As a [role], I want to [action] so that [benefit]"
- **Acceptance Criteria**: Specific, testable conditions for completion
- **Use Cases**: Step-by-step interaction flows
- **Edge Cases**: Boundary conditions and error scenarios

### Non-Functional Requirements
| Category | Questions |
|----------|-----------|
| **Performance** | Response time targets? Throughput requirements? |
| **Scalability** | Expected user count? Data growth rate? |
| **Security** | Authentication needs? Data sensitivity? Compliance? |
| **Reliability** | Uptime requirements? Recovery time? |
| **Maintainability** | Expected change frequency? Team size? |
| **Usability** | Accessibility requirements? Supported devices? |

### Requirements Template
```markdown
## Feature: {name}

### User Story
As a {role}, I want to {action} so that {benefit}.

### Acceptance Criteria
- [ ] Given {context}, when {action}, then {result}
- [ ] Given {context}, when {action}, then {result}

### Non-Functional Requirements
- Performance: {target}
- Security: {requirements}
- Scalability: {expectations}

### Edge Cases
- {edge case 1}: Expected behavior
- {edge case 2}: Expected behavior

### Open Questions
- {question 1}
- {question 2}
```

## Feasibility Analysis

### Technical Feasibility
1. **Can it be built?** - Do the required technologies exist?
2. **Can we build it?** - Do we have the skills and tools?
3. **Can it scale?** - Will it handle expected load?
4. **Can it integrate?** - Does it work with existing systems?
5. **Can it be maintained?** - Is the complexity manageable?

### Risk Assessment
| Risk Level | Criteria | Action |
|-----------|----------|--------|
| **High** | Unproven technology, complex integration, security-critical | Prototype first, expert review |
| **Medium** | Known patterns but new to team, moderate complexity | Spike investigation, design review |
| **Low** | Well-understood patterns, team experience, simple integration | Standard development |

### Complexity Estimation (T-Shirt Sizing)
| Size | Scope | Typical Duration | Risk |
|------|-------|-----------------|------|
| **XS** | Single function/component | Hours | Minimal |
| **S** | Single feature, few files | 1-2 days | Low |
| **M** | Multi-component feature | 3-5 days | Medium |
| **L** | Cross-cutting feature | 1-2 weeks | Medium-High |
| **XL** | System-level change | 2-4 weeks | High |

## Prioritization Frameworks

### MoSCoW Method
| Priority | Description | Action |
|----------|-------------|--------|
| **Must** | Essential for launch, non-negotiable | Build first |
| **Should** | Important but not critical | Build if time allows |
| **Could** | Nice to have, enhances experience | Build in next iteration |
| **Won't** | Explicitly deferred | Document for future |

### RICE Scoring
- **Reach**: How many users will this impact?
- **Impact**: How much will it impact each user? (3=massive, 2=high, 1=medium, 0.5=low, 0.25=minimal)
- **Confidence**: How confident are we in estimates? (100%/80%/50%)
- **Effort**: How many person-months?

**Score** = (Reach x Impact x Confidence) / Effort

### Value vs Effort Matrix
```
High Value │ Quick Wins    │ Major Projects
           │ (DO FIRST)    │ (PLAN CAREFULLY)
           │───────────────│────────────────
Low Value  │ Fill-ins      │ Time Sinks
           │ (DO IF IDLE)  │ (AVOID)
           └───────────────┴────────────────
             Low Effort      High Effort
```

## Brainstorming Output Format

### Requirements Document Structure
```markdown
# Requirements: {Feature Name}

## 1. Problem Statement
{What problem are we solving and for whom?}

## 2. Goals
{What does success look like?}

## 3. User Stories
{List of user stories with acceptance criteria}

## 4. Functional Requirements
{Detailed functional requirements}

## 5. Non-Functional Requirements
{Performance, security, scalability, etc.}

## 6. Constraints
{Technical, business, regulatory constraints}

## 7. Open Questions
{Unresolved questions requiring further discussion}

## 8. Risks
{Identified risks with mitigation strategies}

## 9. Estimated Scope
{T-shirt size estimate with justification}
```

## Skill Integration

When brainstorming involves data modeling:
- **File schemas**: `skill:file-schema-analysis` for analyzing existing schemas
- **Database schemas**: `skill:database-schema-analysis` for understanding data structures

## Boundaries

### Brainstorm Will
- Explore and clarify requirements through dialogue
- Generate requirements documents and user stories
- Assess feasibility and identify risks
- Prioritize features and suggest scope

### Brainstorm Will NOT
- Create architecture designs (use `/implement` or dedicated design process)
- Generate implementation code
- Make final architectural decisions
- Design database schemas (only discuss requirements for them)

## Official References

- [User Stories Applied](https://www.mountaingoatsoftware.com/agile/user-stories)
- [MoSCoW Prioritization](https://en.wikipedia.org/wiki/MoSCoW_method)
- [RICE Framework](https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/)
