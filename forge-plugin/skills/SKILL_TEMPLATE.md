# skill:{skill-name} - [Short Description]

## Version: 1.0.0

## Purpose

[What this skill does, when to use it, and what it produces]

## File Structure

```
skills/{skill-name}/
├── SKILL.md (this file)
├── examples.md
├── scripts/ (optional)
│   └── [helper scripts]
└── templates/ (optional)
    └── [output templates]
```

## Mandatory Workflow

> **IMPORTANT**: Execute ALL steps in order. Do not skip any step.

### Step 1: Initial Analysis

- Gather inputs (user parameters, target files, scope)
- Detect project type (language, framework, architecture)
- Determine project name for memory lookup

### Step 2: Load Indexes & Memory

- Read `../../context/loading_protocol.md` for context loading guidance
- Read `../../context/{domain}/index.md` for available context files
- Read `../../memory/projects/{project}/project_profile.md` (if exists) for shared project knowledge
- Read `../../memory/skills/{this-skill}/{project}/` (if exists) for skill-specific memory

### Step 3: Load Context

- Follow `loading_protocol.md` Steps 1-5 for the primary domain
- Load always-load files for the domain
- Load conditional files based on project detection
- Check `../../context/cross_domain.md` for secondary context needs
- Stay within 4-6 file token budget

### Step 4: [Skill-Specific Core Action]

[Describe the main action this skill performs]

### Step 5: [Additional Skill-Specific Steps as Needed]

[Add more steps as needed for the skill's workflow]

### Step N-1: Generate Output

- Save output to `/claudedocs/{skill-name}_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
- Use templates from `templates/` directory if available

### Step N: Update Memory

- Update skill-specific memory in `../../memory/skills/{this-skill}/{project}/`
- Update shared project memory if new project-level info was learned:
  - Create `../../memory/projects/{project}/project_profile.md` if it doesn't exist
  - Update `../../memory/projects/{project}/technology_stack.md` with new discoveries
  - Add to `../../memory/projects/{project}/cross_skill_insights.md` if applicable
- Add freshness timestamp `<!-- Last Updated: YYYY-MM-DD -->` to modified memory files

## Compliance Checklist

Before completing, verify:

- [ ] All mandatory workflow steps executed in order
- [ ] Context loading protocol followed (`loading_protocol.md`)
- [ ] Shared project memory checked (`memory/projects/{project}/`)
- [ ] Skill-specific memory checked (`memory/skills/{skill}/{project}/`)
- [ ] Output saved with standard naming convention
- [ ] Skill-specific memory updated with new insights
- [ ] Shared project memory updated if new project info learned
- [ ] Freshness timestamps added to modified memory files

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | YYYY-MM-DD | Initial release |
