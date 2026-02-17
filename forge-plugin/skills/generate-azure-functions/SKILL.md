---
name: generate-azure-functions
description: Generate complete Azure Functions projects with local development environment using Tilt and Azurite
version: "0.3.0-alpha"
context:
  primary: [azure]
  topics: [azure_functions_overview, local_development_setup, tiltfile_reference, docker_compose_reference, dockerfile_reference, azurite_setup]
memory:
  scope: per-project
##   files: [project_config.md, generated_files.md, customizations.md, setup_notes.md]

# Skill: generate-azure-functions

**Version**: 0.3.0-alpha
**Purpose**: Generate complete Azure Functions projects with local development environment using Tilt and Azurite
**Author**: The Forge
**Last Updated**: 2025-11-18

---

## Purpose

Generate complete Azure Functions projects with local development environment using Tilt and Azurite


## Title

**Generate Azure Functions** - Create production-ready Azure Functions projects with local development setup (Tilt + Azurite)

---

## File Structure

```
forge-plugin/skills/generate-azure-functions/
├── SKILL.md                  # This file - mandatory workflow
├── examples.md               # Usage scenarios and examples
├── scripts/
│   └── project_generator.py  # Helper script for project generation
└── templates/
    ├── tiltfile_template.txt           # Tiltfile template
    ├── docker_compose_template.txt     # Docker Compose template
    ├── dockerfile_template.txt         # Dockerfile template
    ├── azurite_dockerfile_template.txt # Azurite Dockerfile template
    ├── init_azurite_template.sh        # Azurite init script template
    ├── env_template.txt                # .env.local template
    ├── host_json_template.txt          # host.json template
    └── local_settings_template.txt     # local.settings.json template
```

---

## Interface References

- [ContextProvider](../../interfaces/context_provider.md) — `getDomainIndex("azure")`, `getConditionalContext("azure", topic)`
- [MemoryStore](../../interfaces/memory_store.md) — `getSkillMemory("generate-azure-functions", project)`, `update()`

**Context** (via ContextProvider):
- `contextProvider.getDomainIndex("azure")` — Azure Functions context navigation
- `contextProvider.getConditionalContext("azure", "azure_functions_overview")` — v1 vs v2 comparison
- `contextProvider.getConditionalContext("azure", "local_development_setup")` — Tilt + Azurite architecture
- `contextProvider.getConditionalContext("azure", "tiltfile_reference")` — Tiltfile patterns
- `contextProvider.getConditionalContext("azure", "docker_compose_reference")` — Docker Compose patterns
- `contextProvider.getConditionalContext("azure", "dockerfile_reference")` — Dockerfile patterns
- `contextProvider.getConditionalContext("azure", "azurite_setup")` — Azurite setup patterns

**Memory** (via MemoryStore):
- `memoryStore.getSkillMemory("generate-azure-functions", project)` returns per-project files:
  - `project_config.md` — Previous project configurations
  - `generated_files.md` — What was generated before
  - `customizations.md` — User-specific modifications
  - `setup_notes.md` — Important setup information

---

## Design Requirements

### Core Functionality

This skill must:
1. **Ask user about programming model** (v1 or v2)
2. **Ask about function requirements** (triggers, bindings, number of functions)
3. **Use Azure Functions CLI** to scaffold function project
4. **Generate complete Tilt + Azurite setup** for local development
5. **Create working Docker environment** with live reload
6. **Generate all configuration files** (Tiltfile, docker-compose.yml, Dockerfiles, etc.)
7. **Initialize Azurite storage** with required containers/queues/tables
8. **Store project configuration** in memory for future reference

### Output Requirements

Generate a **complete, working Azure Functions project** with:
- Function app code (scaffolded by Azure Functions CLI)
- Tiltfile with live reload configured
- docker-compose.yml with all services
- Dockerfiles for function apps and Azurite
- Azurite initialization script
- Environment configuration (.env.local, local.settings.json)
- README with setup instructions
- All necessary ignore files (.dockerignore, .funcignore)

### Quality Requirements

Generated projects must:
- **Work immediately** with `tilt up` (no manual fixes needed)
- **Support live reload** (code changes reflected without rebuild)
- **Include proper error handling** (Azurite initialization waits for ready)
- **Follow best practices** (layer caching, ignore patterns, pinned versions)
- **Be well-documented** (README, inline comments)

---

## Prompting Guidelines

### User Questions Framework

After analyzing requirements, ask user about:

#### 1. Programming Model
- **Question**: "Which Azure Functions programming model do you want to use?"
  - v1 (function.json + __init__.py per function)
  - v2 (function_app.py with decorators) - **Recommended**
- **Why ask**: Determines project structure and scaffolding approach
- **Follow-up**: "Do you need to maintain compatibility with existing v1 functions?"

#### 2. Runtime and Version
- **Question**: "Which runtime and version?"
  - Python 3.9, 3.10, 3.11 (specify which)
  - Node.js 16, 18, 20
  - .NET 6, 7, 8
- **Why ask**: Determines base Docker image and dependencies

#### 3. Function Types
- **Question**: "What types of functions do you need?"
  - HTTP triggers
  - Blob triggers
  - Queue triggers
  - Timer triggers
  - Table storage bindings
- **Why ask**: Determines what Azurite resources to initialize

#### 4. Number of Function Apps
- **Question**: "How many function apps in this project?"
  - Single function app (most common)
  - Multiple function apps (microservices pattern)
- **Why ask**: Determines number of Docker containers and ports
- **Follow-up**: "What are the names of each function app?"

#### 5. Storage Requirements
- **Question**: "What Azurite storage resources do you need?"
  - Blob containers (list names)
  - Queues (list names)
  - Tables (list names)
- **Why ask**: Determines initialization script content

#### 6. Dependency Management
- **Question**: "How do you want to manage Python dependencies?" (if Python)
  - pip (requirements.txt)
  - Poetry (pyproject.toml) - **Recommended for complex projects**
- **Why ask**: Determines Dockerfile and dependency installation approach

#### 7. Local Package Dependencies
- **Question**: "Does your function depend on any local packages?"
  - Yes (need to build and install local wheels)
  - No (only external dependencies)
- **Why ask**: Determines if Dockerfile needs local package build steps
- **Follow-up**: "What is the path to the local package?"

---

## Instructions

## Mandatory Workflow

### MANDATORY STEPS (Must Execute in Order)

---

#### **Step 1: Initial Analysis**

**Purpose**: Understand project context and requirements

**Actions**:
1. Identify working directory and project name
2. Check if Azure Functions CLI is available (`func --version`)
3. Check if Docker and Tilt are installed
4. Determine if this is a new project or adding to existing project
5. Note any existing function apps or infrastructure

**Output**: Clear understanding of project environment

---

#### **Step 2: Load Index Files**

**Purpose**: Understand available context and memory

**Actions**:
1. Load Azure domain index via `contextProvider.getDomainIndex("azure")`
2. Identify which context topics will be needed based on requirements

**Output**: Knowledge of available guidance and domain structure

---

#### **Step 3: Load Project Memory (if exists)**

**Purpose**: Understand previous configurations for this project

**Actions**:
1. Load project memory via `memoryStore.getSkillMemory("generate-azure-functions", project)`
2. If memory exists, review:
   - `project_config.md` - Previous configuration decisions
   - `generated_files.md` - What was generated before
   - `customizations.md` - User-specific modifications
   - `setup_notes.md` - Important setup information
3. If no memory exists, note this is first-time generation

**Output**: Understanding of project history or recognition of new project

---

#### **Step 4: Load Context**

**Purpose**: Load relevant Azure Functions knowledge

**Actions**:
1. Load `contextProvider.getConditionalContext("azure", "azure_functions_overview")` - Always load
2. Load `contextProvider.getConditionalContext("azure", "local_development_setup")` - Always load
3. Load `contextProvider.getConditionalContext("azure", "tiltfile_reference")` - For Tiltfile generation
4. Load `contextProvider.getConditionalContext("azure", "docker_compose_reference")` - For docker-compose generation
5. Load `contextProvider.getConditionalContext("azure", "dockerfile_reference")` - For Dockerfile generation
6. Load `contextProvider.getConditionalContext("azure", "azurite_setup")` - For Azurite setup

**Output**: Comprehensive understanding of Azure Functions patterns and best practices

---

#### **Step 5: Gather Requirements**

**Purpose**: Understand user's needs through conversation

**Actions**:
1. Ask user about **programming model** (v1 or v2)
2. Ask about **runtime and version**
3. Ask about **function types** needed
4. Ask about **number of function apps**
5. Ask about **storage requirements** (containers, queues, tables)
6. Ask about **dependency management** approach
7. Ask about **local package dependencies**
8. Confirm all requirements with user before proceeding

**Output**: Complete specification of what to generate

---

#### **Step 6: Generate Project Structure**

**Purpose**: Create Azure Functions project using CLI and templates

**Actions**:

1. **Create project directory structure**:
   ```bash
   mkdir -p {project-name}/.docker/{azurite,scripts}
   mkdir -p {project-name}/functions
   mkdir -p {project-name}/claudedocs
   ```

2. **For each function app, use Azure Functions CLI**:
   ```bash
   # v2 model (recommended)
   cd {project-name}/functions
   func init {function-name} --python --model v2
   cd {function-name}

   # Add functions directly in function_app.py (v2)
   # Or use func new for v1 model

   # v1 model (if needed)
   func init {function-name} --python --model v1
   cd {function-name}
   func new --name MyHttpTrigger --template "HTTP trigger"
   ```

3. **Generate Tiltfile** from template:
   - Use `templates/tiltfile_template.txt`
   - Customize for number of function apps
   - Set up live_update for each function
   - Configure service dependencies

4. **Generate docker-compose.yml** from template:
   - Use `templates/docker_compose_template.txt`
   - Add service for each function app
   - Configure Azurite service
   - Set environment variables
   - Map ports (7071, 7072, 7073, ...)

5. **Generate Dockerfile for each function** from template:
   - Use `templates/dockerfile_template.txt`
   - Customize for runtime (Python/Node/.NET)
   - Configure dependency management (pip/Poetry/npm)
   - Add local package build if needed
   - Set up working directory and environment

6. **Generate Azurite Dockerfile** from template:
   - Use `templates/azurite_dockerfile_template.txt`
   - Include Python SDK installation
   - Add initialization script

7. **Generate Azurite initialization script** from template:
   - Use `templates/init_azurite_template.sh`
   - Customize containers/queues/tables based on requirements
   - Add test data if requested

8. **Generate configuration files**:
   - `.env.local` from `templates/env_template.txt` (with custom Azurite key)
   - `host.json` from `templates/host_json_template.txt`
   - `local.settings.json` from `templates/local_settings_template.txt`
   - `.dockerignore`, `.funcignore`, `.gitignore`

9. **Generate README.md** with:
   - Project overview
   - Prerequisites (Docker, Tilt, func CLI)
   - Setup instructions (`tilt up`)
   - API endpoints and usage
   - Azurite connection strings
   - Testing instructions

**Output**: Complete project structure with all files generated

---

#### **Step 7: Validate Generated Project**

**Purpose**: Ensure project works before presenting to user

**Actions**:
1. Verify all required files exist
2. Check Tiltfile syntax (no obvious errors)
3. Verify docker-compose.yml is valid YAML
4. Ensure Dockerfiles have proper structure
5. Check that ports don't conflict
6. Verify file paths are correct

**Do NOT run `tilt up` or `docker build`** - just validate file structure and syntax

**Output**: Confidence that generated project is correct

---

#### **Step 8: Present Results to User**

**Purpose**: Show user what was generated and next steps

**Actions**:
1. List all generated files with brief description
2. Highlight key configuration decisions made
3. Show project directory structure
4. Provide next steps:
   ```bash
   cd {project-name}
   tilt up  # Start development environment
   ```
5. Point to README.md for detailed instructions
6. Mention Tilt UI at http://localhost:10350

**Output**: User understands what was created and how to use it

---

#### **Step 9: Update Project Memory**

**Purpose**: Store configuration for future reference

**Actions**:
1. Use `memoryStore.update("generate-azure-functions", project, filename, content)` for each file
2. Create `project_config.md`:
   - Programming model (v1/v2)
   - Runtime and version
   - Function app names and ports
   - Storage resources created
   - Dependency management approach
   - Local package dependencies
3. Create `generated_files.md`:
   - List of all generated files
   - Timestamp of generation
   - Skill version used
4. Create `customizations.md`:
   - User-specific requirements
   - Special configurations
   - Deviations from templates
5. Create `setup_notes.md`:
   - Important setup information
   - Known issues or quirks
   - Testing recommendations

**Output**: Memory stored for future skill invocations

---

### Step 100: Generate Output

Create deliverables and save to `/claudedocs/`:
- Follow OUTPUT_CONVENTIONS.md naming: `generate-azure-functions_{project}_{YYYY-MM-DD}.md`
- Include all required sections
- Provide clear, actionable recommendations

## Best Practices

### Code Generation

1. **Use templates**: Don't hardcode - use template files and substitute variables
2. **Follow conventions**: Use standard ports (7071+), standard paths (/home/site/wwwroot)
3. **Pin versions**: Specify exact versions in requirements.txt, pyproject.toml
4. **Add comments**: Explain non-obvious configurations in generated files
5. **Use .dockerignore**: Reduce build context size

### Tilt Configuration

1. **Configure live_update**: Essential for fast development iteration
2. **Set resource_deps**: Ensure Azurite starts before functions
3. **Add helpful labels**: Group services (functions, storage)
4. **Include links**: Make endpoints easily accessible in Tilt UI
5. **Use service selection**: Allow running subset of function apps

### Docker Configuration

1. **Optimize layer caching**: Copy dependencies before code
2. **Use multi-stage builds**: For smaller images (if needed)
3. **Set up health checks**: For Azurite readiness
4. **Use named volumes**: For Azurite data persistence
5. **Share Azure credentials**: Mount $HOME/.azure if needed

### Azurite Setup

1. **Wait for ready**: Use netcat or similar in init script
2. **Handle existing resources**: Catch "AlreadyExists" exceptions
3. **Provide feedback**: Print what's being created
4. **Add test data**: If helpful for development
5. **Document resources**: List containers/queues/tables in README

---

## Additional Notes

### Prerequisites Check

Before generating, verify user has:
- Docker Desktop or Docker Engine installed
- Tilt installed
- Azure Functions Core Tools installed
- Python/Node/.NET SDK (for their chosen runtime)

If missing, provide installation instructions from `contextProvider.getConditionalContext("azure", "local_development_setup")`.

### Multiple Function Apps Pattern

When generating multiple function apps:
- Use consistent naming (orchestrator, processor, loader, etc.)
- Increment ports sequentially (7071, 7072, 7073)
- Share Azurite instance across all functions
- Consider dependencies (does one function depend on another?)
- Add all to Tiltfile with proper dependencies

### Error Handling

If Azure Functions CLI fails:
- Check CLI is installed: `func --version`
- Verify runtime is available: `python --version`, `node --version`, etc.
- Check directory doesn't already exist
- Provide helpful error messages with solutions

### Customization Support

Support user customization by:
- Generating clean, commented code
- Using environment variables for configuration
- Documenting where to make changes
- Storing customizations in memory for future reference

---

## Compliance Checklist

Before marking this skill as complete, verify:

- [ ] Step 1: Initial analysis performed, environment checked
- [ ] Step 2: Index files read and understood
- [ ] Step 3: Project memory loaded (or noted as first-time)
- [ ] Step 4: All relevant context files loaded
- [ ] Step 5: Requirements gathered through user questions
- [ ] Step 6: Complete project structure generated with all files
- [ ] Step 7: Generated files validated (syntax, structure)
- [ ] Step 8: Results presented to user with next steps
- [ ] Step 9: Project memory updated with configuration
- [ ] Generated project includes Tiltfile with live reload
- [ ] Generated project includes docker-compose.yml with all services
- [ ] Generated project includes Dockerfile(s) for function apps
- [ ] Generated project includes Azurite Dockerfile and init script
- [ ] Generated project includes all configuration files
- [ ] Generated project includes comprehensive README
- [ ] All files use templates (not hardcoded)
- [ ] Port conflicts avoided
- [ ] Best practices followed (caching, ignores, dependencies)
- [ ] User informed of next steps (`tilt up`)

---

## Version History

### v1.1.0 (2025-07-15)
- Phase 4 Migration: Replaced hardcoded `../../context/` and `../../memory/` paths with ContextProvider and MemoryStore interface calls
- Added YAML frontmatter with context/memory declarations
- Added Interface References section

### v1.0.0 (2025-11-18)
- Initial skill implementation
- Support for Python functions (v1 and v2 models)
- Tilt + Azurite local development setup
- Complete project generation from templates
- Memory system integration
- Context system integration
- Support for multiple function apps
- Poetry and pip dependency management
