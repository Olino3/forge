# Generate More Skills with Claude - Examples

This file contains example scenarios demonstrating how to use the generate-more-skills-with-claude skill to create new Claude Code skills for The Forge.

---

## Example 1: Generate a Simple Text Processing Skill

### Scenario
A developer wants to create a skill that generates professional changelog entries from git commits, following conventional commit format and semantic versioning principles.

### User Prompt
```
Generate a new skill called "changelog-generator" that creates professional CHANGELOG.md entries from git commit history. It should parse conventional commits, group by type (feat, fix, chore, etc.), and format output following Keep a Changelog standards.
```

### Skill Execution

**Step 1 - Gather Requirements**:
- **Purpose**: Transform git commit history into structured changelog documentation
- **Target Users**: Release managers, DevOps engineers, project maintainers
- **Scope**: Parse commits → classify by type → format as markdown changelog
- **Domain**: Git workflows, semantic versioning, conventional commits
- **Inputs**: Git commit range, version number, release date
- **Outputs**: CHANGELOG.md formatted text

**Step 2 - Design Workflow**:
- Step 1: Gather context (repo, version, date range)
- Step 2: Fetch commit history using git commands
- Step 3: Parse commits using conventional commit format
- Step 4: Group and organize by change type
- Step 5: Generate changelog section
- Step 6: Validate and format output
- Compliance checklist: All steps completed, conventional format followed

**Step 3 - Load Context**:
- Review similar skills: `commit-helper`, `get-git-diff`
- Check context files: `../../context/git/index.md` exists
- Pattern: Workflow-driven, git integration, template-based output

**Step 4 - Generate SKILL.md**:
## ```markdown
name: changelog-generator
## description: Generates professional CHANGELOG.md entries from git commit history following Keep a Changelog and Conventional Commits standards. Parses commits, groups by type, formats with semantic versioning. Transforms the scattered chronicle of changes into a structured narrative of evolution.

# Changelog Generator

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: The 6-step workflow outlined in this document MUST be followed...
[Complete SKILL.md content following the template]
```

**Step 5 - Generate examples.md**:
```markdown
# Changelog Generator Examples

## Example 1: Generate Changelog for Minor Version Release
### Scenario
Release manager preparing v1.5.0 release notes from commits since v1.4.0
### User Prompt
Generate a changelog for version 1.5.0 covering commits from v1.4.0 to HEAD
...
```

**Step 6 - Generate Templates**:
- `templates/changelog_entry.md`: Template for changelog sections
- `templates/release_notes.md`: Template for full release documentation

### Generated Skill Structure

```
changelog-generator/
├── SKILL.md                      # 250+ lines
├── examples.md                   # 6 examples, 400+ lines
└── templates/
    ├── changelog_entry.md        # Changelog section template
    └── release_notes.md          # Full release template
```

**SKILL.md** (abbreviated):
## ```markdown
name: changelog-generator
## description: Generates professional CHANGELOG.md entries...

## MANDATORY WORKFLOW

### ⚠️ STEP 1: Gather Context (REQUIRED)
1. Identify version number and release date
2. Determine commit range (e.g., v1.4.0..HEAD)
3. Understand project's changelog format preference
...

### ⚠️ STEP 6: Validate and Format (REQUIRED)
- [ ] All commit types categorized correctly
- [ ] Breaking changes highlighted
- [ ] Links to commits/PRs included
...
```

---

## Example 2: Generate a Code Generation Skill with Scripts

### Scenario
A platform engineer wants to create a skill that generates Terraform modules following the team's internal conventions and best practices.

### User Prompt
```
Create a skill called "generate-terraform-modules" that scaffolds Terraform module projects with our team's structure: variables.tf, main.tf, outputs.tf, README.md, examples/, and tests/. It should support AWS, Azure, and GCP providers.
```

### Skill Execution

**Step 1 - Gather Requirements**:
- **Purpose**: Scaffold production-ready Terraform modules with best practices
- **Target Users**: Platform engineers, DevOps engineers, infrastructure teams
- **Scope**: Generate module structure → create files → populate templates → add examples
- **Domain**: Infrastructure as Code (IaC), Terraform, multi-cloud
- **Inputs**: Module name, cloud provider, resource types
- **Outputs**: Complete Terraform module directory structure

**Step 2 - Design Workflow**:
- Step 1: Gather module requirements (name, provider, purpose)
- Step 2: Load project memory for team conventions
- Step 3: Generate core Terraform files
- Step 4: Create example usage code
- Step 5: Generate testing structure
- Step 6: Validate module structure
- Scripts needed: `scaffold-module.sh`, `validate-terraform.sh`

**Step 3 - Load Context**:
- Review similar skills: `generate-azure-bicep`, `generate-azure-functions`
- Check context files: No terraform context exists → will create `../../context/terraform/` reference
- Pattern: Multi-file generation, validation scripts, template-driven

**Step 4 - Generate SKILL.md**:
## ```markdown
name: generate-terraform-modules
## description: Scaffolds production-ready Terraform modules following HashiCorp best practices and team conventions. Generates complete module structure with variables, outputs, examples, tests, and documentation. Shapes infrastructure as code like a master mason laying the foundation of cloud architecture.

## File Structure
- SKILL.md
- examples.md
- scripts/
  - scaffold-module.sh
  - validate-terraform.sh
- templates/
  - variables.tf.tmpl
  - main.tf.tmpl
  - outputs.tf.tmpl
  - README.md.tmpl
  - example.tf.tmpl

## MANDATORY WORKFLOW
### ⚠️ STEP 1: Gather Module Requirements
...
```

**Step 5 - Generate examples.md**:
- Example 1: Simple AWS S3 module
- Example 2: Azure AKS cluster module
- Example 3: GCP VPC network module
- Example 4: Multi-cloud load balancer module
- Example 5: Module with complex dependencies
- Example 6: Module with testing integration

**Step 6 - Generate Templates & Scripts**:

**templates/main.tf.tmpl**:
```hcl
# {{module_name}} - {{description}}
# Provider: {{provider}}
# Created: {{date}}

terraform {
  required_version = ">= 1.0"
  required_providers {
    {{provider}} = {
      source  = "hashicorp/{{provider}}"
      version = "~> {{provider_version}}"
    }
  }
}

{{#resources}}
resource "{{type}}" "{{name}}" {
  # Resource configuration
}
{{/resources}}
```

**scripts/scaffold-module.sh**:
```bash
#!/bin/bash
# Scaffold a new Terraform module structure

set -euo pipefail

MODULE_NAME=$1
PROVIDER=$2

mkdir -p "$MODULE_NAME"/{examples,tests}
touch "$MODULE_NAME"/{variables.tf,main.tf,outputs.tf,README.md}
...
```

### Generated Output
Complete Terraform module skill with 8 templates, 2 helper scripts, comprehensive examples.

---

## Example 3: Generate a Code Review Skill for a New Language

### Scenario
Team is adopting Rust and needs a code review skill similar to the existing dotnet-code-review and python-code-review skills.

### User Prompt
```
Generate a "rust-code-review" skill modeled after the python-code-review skill. It should check for idiomatic Rust patterns, ownership/borrowing issues, error handling, unsafe code, performance considerations, and cargo best practices.
```

### Skill Execution

**Step 1 - Gather Requirements**:
- **Purpose**: Automated code review for Rust following language idioms and best practices
- **Target Users**: Rust developers at all skill levels
- **Scope**: Review changed files → analyze patterns → identify issues → provide feedback
- **Domain**: Rust language, ownership system, cargo ecosystem
- **Integration**: Works with `get-git-diff` skill
- **Quality focus**: Memory safety, performance, idiomatic code

**Step 2 - Design Workflow**:
- Step 1: Get changed files (integrate with get-git-diff)
- Step 2: Load Rust context and project memory
- Step 3: Analyze code for issues
- Step 4: Generate review comments
- Step 5: Prioritize findings
- Step 6: Format review output
- Step 7: Update memory (optional)

**Step 3 - Load Context**:
- Review exemplar skills: `python-code-review`, `dotnet-code-review`, `angular-code-review`
- Pattern observed: All code review skills share similar workflow structure
- Need to create context files: `../../context/rust/` directory with index.md, ownership.md, error_handling.md, performance.md, cargo.md

**Step 4 - Generate SKILL.md**:
## ```markdown
name: rust-code-review
## description: Reviews Rust code for idiomatic patterns, ownership correctness, error handling, unsafe usage, and performance considerations. Analyzes changed files, identifies issues across 12 dimensions, and provides actionable feedback. Like a master blacksmith inspecting forged steel, this skill ensures your Rust code is memory-safe, performant, and idiomatic.

## Focus Areas
1. **Ownership & Borrowing**: Lifetimes, references, ownership transfer
2. **Error Handling**: Result/Option usage, ? operator, custom errors
3. **Memory Safety**: Unsafe code audit, raw pointer usage
4. **Concurrency**: Thread safety, Send/Sync, Arc/Mutex patterns
5. **Performance**: Zero-cost abstractions, allocation patterns
6. **Idiomatic Code**: Iterator chains, pattern matching, trait usage
7. **Cargo & Dependencies**: Crate selection, feature flags, version management
...

### ⚠️ STEP 2: Load Context & Project Memory
**YOU MUST:**
1. READ `../../context/rust/index.md` for Rust-specific patterns
2. Based on code being reviewed, load relevant context:
   - `ownership.md` for borrowing and lifetime issues
   - `error_handling.md` for Result/Option patterns
   - `performance.md` for optimization opportunities
   - `cargo.md` for dependency and build issues
...
```

**Step 5 - Generate examples.md**:
- Example 1: Review PR with ownership issues
- Example 2: Unsafe code audit
- Example 3: Error handling refactoring suggestions
- Example 4: Performance optimization opportunities
- Example 5: Idiomatic pattern improvements
- Example 6: Cargo.toml dependency review

**Step 6 - Create Context Files** (NEW):
Since Rust context doesn't exist, generate context file structure:

**../../context/rust/index.md**:
```markdown
# Rust Context Files

Navigate Rust-specific knowledge:
- **ownership.md** - Ownership, borrowing, lifetimes
- **error_handling.md** - Result, Option, custom errors
- **performance.md** - Zero-cost abstractions, optimization
- **cargo.md** - Dependency management, build configuration
```

### Generated Skill + Context

```
rust-code-review/
├── SKILL.md
├── examples.md
└── templates/
    └── review_report.md

../../context/rust/              # NEW CONTEXT FILES
├── index.md
├── ownership.md
├── error_handling.md
├── performance.md
└── cargo.md
```

---

## Example 4: Generate a Skill with Memory Integration

### Scenario
A tech writer wants a skill that generates API documentation but learns the team's preferred terminology and style over time.

### User Prompt
```
Create "api-doc-generator" that creates OpenAPI/REST API documentation. It should learn from feedback — if I correct terminology or style choices, remember those preferences for the project.
```

### Skill Execution

**Step 1 - Gather Requirements**:
- **Purpose**: Generate API reference docs with project-specific style learning
- **Memory Integration**: CRITICAL — must persist terminology, style preferences, examples
- **Inputs**: OpenAPI spec, code files, existing docs
- **Outputs**: Formatted API documentation

**Step 2 - Design Workflow**:
- Step 1: Gather API scope and format preferences
- Step 2: **Load project memory** (terminology, style, conventions)
- Step 3: Extract API endpoints and schemas
- Step 4: Generate documentation sections
- Step 5: Apply project-specific style
- Step 6: Review and validate
- Step 7: **Update memory** with new learnings (REQUIRED)

**Step 3 - Load Context**:
- Review memory-enabled skills: `documentation-generator`, `email-writer`
- Pattern: Early memory load step, optional memory update step
- Memory structure: `../../memory/skills/api-doc-generator/{project-name}/`

**Step 4 - Generate SKILL.md** with memory emphasis:
```markdown
### ⚠️ STEP 2: Load Project Memory (REQUIRED)
**YOU MUST:**
1. Identify project name from repository or ask user
2. **READ** `../../memory/skills/api-doc-generator/{project-name}/`
3. If memory exists, load:
   - `terminology.md` - Project-specific terms and glossary
   - `style_guide.md` - Preferred documentation patterns
   - `api_patterns.md` - Common endpoint structures
4. If no memory exists, initialize empty preferences

### ⚠️ STEP 7: Update Memory (OPTIONAL)
**IF** user provides feedback or corrections:
1. Identify what changed (terminology, style, pattern)
2. Update relevant memory file:
   - New terms → `terminology.md`
   - Style preferences → `style_guide.md`
   - API patterns → `api_patterns.md`
3. Include timestamp and rationale
```

**Step 5 - Generate examples.md** showing memory evolution:
- Example 1: First use (no memory, generic output)
- Example 2: User corrects terminology → memory updated
- Example 3: Second use (memory applied, preferred terms used)
- Example 4: Learning API patterns from multiple endpoints
- Example 5: Memory across different projects
- Example 6: Exporting/sharing memory between teams

**Step 6 - Generate Templates**:
- `templates/api_endpoint.md` - Single endpoint documentation
- `templates/api_overview.md` - API reference index
- Memory templates in the examples showing structure

### Key Feature: Memory Learning Loop

```
First Use:
User: "Document the /users endpoint"
Skill: Generates doc with generic term "identifier"

Feedback:
User: "We call it 'userId' not 'identifier'"

Memory Update:
File: memory/skills/api-doc-generator/myproject/terminology.md
Entry: "identifier → userId (preferred for user references)"

Second Use:
User: "Document the /posts endpoint"
Skill: *Loads memory, uses 'userId' automatically*
```

---

## Example 5: Generate a Complex Multi-Tool Skill

### Scenario
DevOps team needs a skill that sets up complete observability stacks with Prometheus, Grafana, Loki, and Tempo.

### User Prompt
```
Generate "deploy-observability-stack" skill that creates a complete observability setup with Prometheus for metrics, Grafana for visualization, Loki for logs, and Tempo for traces. Should generate Kubernetes manifests, Helm values, docker-compose for local dev, and Grafana dashboards.
```

### Skill Execution

**Step 1 - Gather Requirements**:
- **Purpose**: End-to-end observability stack deployment
- **Complexity**: HIGH — multiple tools, formats, platforms
- **Outputs**: K8s YAML, Helm charts, docker-compose, Grafana JSON, docs
- **Scope**: Very broad — requires orchestration of multiple generation tasks

**Step 2 - Design Workflow**:
- Step 1: Gather stack requirements (platform, scale, features)
- Step 2: Load memory and select components
- Step 3: Generate Prometheus configuration
- Step 4: Generate Loki configuration
- Step 5: Generate Tempo configuration
- Step 6: Generate Grafana dashboards
- Step 7: Generate deployment manifests (K8s/docker-compose)
- Step 8: Create setup documentation
- Step 9: Validate configuration compatibility

**Step 3 - Load Context**:
- Similar skills: `generate-azure-functions`, `generate-tilt-dev-environment`
- Pattern: Multi-file, multi-format generation
- Need context files for observability patterns

**Step 4 - Generate SKILL.md** (complex workflow):
```markdown
### ⚠️ STEP 3: Generate Prometheus Configuration
**YOU MUST:**
1. Create `prometheus.yml` with scrape configs
2. Define service discovery for target environments
3. Configure retention and storage
4. Add alerting rules for common issues
5. Template job configurations for extensibility

### ⚠️ STEP 6: Generate Grafana Dashboards
**YOU MUST:**
1. Create dashboard JSON for each service type
2. Include panels for: request rate, error rate, duration
3. Configure data source variables (Prometheus, Loki, Tempo)
4. Add links between metrics, logs, and traces
5. Use templates to allow customization
```

**Step 5 - Generate examples.md**:
- Example 1: Basic stack for small service (docker-compose)
- Example 2: Production Kubernetes stack
- Example 3: Stack with custom metrics and dashboards
- Example 4: Multi-cluster observability
- Example 5: Stack with authentication and security
- Example 6: Migrating from existing monitoring

**Step 6 - Generate Templates & Scripts** (extensive):
```
deploy-observability-stack/
├── SKILL.md
├── examples.md
├── scripts/
│   ├── validate-prometheus.sh
│   ├── test-grafana.sh
│   └── deploy-k8s.sh
└── templates/
    ├── prometheus.yml.tmpl
    ├── loki.yml.tmpl
    ├── tempo.yml.tmpl
    ├── grafana-dashboard-service.json.tmpl
    ├── grafana-dashboard-infra.json.tmpl
    ├── kubernetes-manifests.yaml.tmpl
    ├── docker-compose.yml.tmpl
    ├── helm-values.yaml.tmpl
    └── README.md.tmpl
```

### Complexity Handling

The skill handles complexity through:
1. **Staged workflow**: Each tool configured separately
2. **Template library**: 9 different output templates
3. **Validation scripts**: Test configurations before deployment
4. **Progressive examples**: Simple → complex usage
5. **Integration focus**: Ensures tools work together (metrics → traces)

---

## Example 6: Generate a Lightweight Utility Skill

### Scenario
Developer wants a quick skill to generate .gitignore files for different project types.

### User Prompt
```
Create a simple skill "gitignore-generator" that creates .gitignore files for common project types like Node.js, Python, Java, .NET, Go, Rust. Just quick and straightforward.
```

### Skill Execution

**Step 1 - Gather Requirements**:
- **Purpose**: Quick .gitignore file generation
- **Scope**: NARROW — single file output, template-based
- **Complexity**: LOW — simple selection and file generation

**Step 2 - Design Workflow** (simplified):
- Step 1: Ask project type
- Step 2: Load template for that type
- Step 3: Customize if needed
- Step 4: Generate .gitignore
- Only 4 steps for simple skills

**Step 3 - Load Context**:
- Review simple skills: `commit-helper` (also lightweight)
- Pattern: Minimal workflow, template-driven

**Step 4 - Generate SKILL.md** (concise):
## ```markdown
name: gitignore-generator
## description: Generates .gitignore files for common project types (Node.js, Python, Java, .NET, Go, Rust). Selects appropriate patterns, adds custom exclusions, ensures comprehensive coverage. A simple guardian that keeps your repository clean from the detritus of builds and dependencies.

## MANDATORY WORKFLOW

### ⚠️ STEP 1: Identify Project Type
- Ask user or detect from files
- Support: Node.js, Python, Java, .NET, Go, Rust, Generic

### ⚠️ STEP 2: Load Template
- Select base template for project type
- Combine multiple if needed (e.g., Node + Docker)

### ⚠️ STEP 3: Customize
- Add project-specific patterns
- Include IDE exclusions if requested

### ⚠️ STEP 4: Generate File
- Output .gitignore content
- Suggest where to place it
```

**Step 5 - Generate examples.md**:
- Example 1: Node.js project
- Example 2: Python project
- Example 3: Multi-language project (Node + Python)
- Example 4: Adding custom patterns
- Example 5: Merging with existing .gitignore
- Example 6: Docker + language combination

**Step 6 - Generate Templates**:
```
gitignore-generator/
├── SKILL.md          # Concise, ~100 lines
├── examples.md       # 6 examples, ~200 lines
└── templates/
    ├── nodejs.gitignore
    ├── python.gitignore
    ├── java.gitignore
    ├── dotnet.gitignore
    ├── go.gitignore
    ├── rust.gitignore
    ├── docker.gitignore
    └── ide.gitignore
```

**templates/python.gitignore**:
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
...
```

### Lightweight Pattern

This demonstrates that not all skills need to be complex:
- Simple 4-step workflow
- Template-based (no scripts needed)
- Concise documentation
- Still follows the mandatory pattern

---

## Summary of Skill Types

1. **Text Processing** (`changelog-generator`) - Transform git commits to documentation
2. **Code Generation** (`generate-terraform-modules`) - Scaffold projects with scripts
3. **Code Review** (`rust-code-review`) - Language-specific analysis with context files
4. **Memory-Enabled** (`api-doc-generator`) - Learning from feedback over time
5. **Multi-Tool Orchestration** (`deploy-observability-stack`) - Complex, many outputs
6. **Simple Utility** (`gitignore-generator`) - Lightweight, template-driven

## Best Practices Demonstrated

- **Workflow first**: Design the workflow before writing SKILL.md
- **Load context early**: Check memory and existing skills in Step 3
- **Template everything**: Output should be template-driven for consistency
- **Comprehensive examples**: Cover the spectrum from simple to complex
- **Special cases matter**: Document error handling and edge cases
- **Version and date**: Always include version history
- **Poetic descriptions**: Match The Forge's thematic style
- **Compliance gates**: Every step must have validation criteria
- **Scripts when needed**: Automate complex or repetitive tasks
- **Memory for learning**: Enable skills to improve with usage

## Pattern Recognition

All skills share this structure:
```
skill-name/
├── SKILL.md          # Frontmatter + workflow + checklist
├── examples.md       # 6+ scenarios with full execution traces
├── templates/        # Output format templates (optional)
│   └── *.md / *.yml / *.json
└── scripts/          # Helper automation (optional)
    └── *.sh
```

Meta-lesson: Consistency in structure enables skills to compose and integrate seamlessly.
