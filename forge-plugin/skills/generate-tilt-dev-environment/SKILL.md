# Skill: generate-tilt-dev-environment

**Version**: 1.0.0
**Purpose**: Generate complete local development environments using Tilt, Docker Compose, and containerization
**Author**: The Forge
**Last Updated**: 2026-02-06

---

## Title

**Generate Tilt Development Environment** - Construct local development realms with Tilt orchestration

---

## File Structure

```
forge-plugin/skills/generate-tilt-dev-environment/
├── SKILL.md                  # This file - mandatory workflow
├── examples.md               # Usage scenarios and examples
├── scripts/
│   └── environment_generator.py  # Helper script for environment generation
└── templates/
    ├── tiltfile_template.txt           # Tiltfile template
    ├── docker_compose_template.txt     # Docker Compose template
    ├── dockerfile_template.txt         # Dockerfile template
    ├── env_template.txt                # .env template
    └── makefile_template.txt           # Makefile template
```

---

## Required Reading

**Before executing this skill**, read these files in order:

1. **Context indexes** (understand what context is available):
   - `../../context/azure/index.md` - Azure context navigation (if using Azure services)
   - Look for Docker, containerization context files

2. **Memory index** (understand memory structure):
   - `../../memory/skills/generate-tilt-dev-environment/index.md` - Memory structure for this skill

3. **Project memory** (if exists):
   - `../../memory/skills/generate-tilt-dev-environment/{project-name}/` - Previous project configurations

---

## Design Requirements

### Core Functionality

This skill must:
1. **Analyze existing project structure** to understand services and dependencies
2. **Ask user about service requirements** (services to containerize, dependencies)
3. **Generate Tiltfile** with live reload and service orchestration
4. **Create Docker Compose configuration** for service dependencies
5. **Generate Dockerfiles** for each service
6. **Create development scripts** (Makefile, startup scripts)
7. **Configure environment variables** (.env files, settings)
8. **Store project configuration** in memory for future reference

### Output Requirements

Generate a **complete, working Tilt development environment** with:
- Tiltfile with live reload configured
- docker-compose.yml with all services and dependencies
- Dockerfiles for each application service
- Environment configuration (.env, .env.local, .env.example)
- Makefile with common commands (up, down, logs, clean)
- Development scripts (initialization, seed data, cleanup)
- README with setup instructions
- All necessary ignore files (.dockerignore, .gitignore)

### Quality Requirements

Generated environments must:
- **Work immediately** with `tilt up` (no manual fixes needed)
- **Support live reload** (code changes reflected without rebuild)
- **Include proper health checks** (services wait for dependencies)
- **Follow best practices** (layer caching, ignore patterns, pinned versions)
- **Be well-documented** (README, inline comments)
- **Support multiple environments** (development, testing, staging)

---

## Prompting Guidelines

### User Questions Framework

After analyzing project structure, ask user about:

#### 1. Project Type
- **Question**: "What type of project are you developing?"
  - Web application (frontend + backend)
  - Microservices architecture
  - API service
  - Full-stack application
  - Data pipeline
  - Mobile app backend
- **Why ask**: Determines service structure and dependencies
- **Follow-up**: "What is the primary programming language/framework?"

#### 2. Services to Containerize
- **Question**: "Which services need to be containerized?"
  - Backend API
  - Frontend application
  - Database (PostgreSQL, MySQL, MongoDB)
  - Cache (Redis, Memcached)
  - Message queue (RabbitMQ, Kafka)
  - Search (Elasticsearch, OpenSearch)
  - Storage (MinIO, Azurite)
- **Why ask**: Determines number of containers and dependencies
- **Follow-up**: "Are there any existing Dockerfiles we should use as a base?"

#### 3. Programming Languages & Runtimes
- **Question**: "What programming languages/runtimes are you using?"
  - Python (specify version: 3.9, 3.10, 3.11, 3.12)
  - Node.js (specify version: 16, 18, 20, 22)
  - .NET (specify version: 6, 7, 8)
  - Go (specify version)
  - Java (specify version: 11, 17, 21)
  - Ruby (specify version)
  - PHP (specify version)
- **Why ask**: Determines base Docker images and build processes

#### 4. Database & Storage
- **Question**: "What databases or storage systems do you need?"
  - PostgreSQL (specify version)
  - MySQL/MariaDB (specify version)
  - MongoDB (specify version)
  - Redis (specify version)
  - File storage (MinIO, local volumes)
- **Why ask**: Determines service dependencies and data persistence
- **Follow-up**: "Do you need seed data or initialization scripts?"

#### 5. Development Dependencies
- **Question**: "What development dependencies do you need?"
  - Package managers (pip, npm, yarn, poetry, cargo)
  - Build tools (make, gradle, maven, webpack)
  - Testing tools (pytest, jest, mocha)
  - Linters (eslint, pylint, golangci-lint)
  - Debugging tools
- **Why ask**: Determines development container configuration

#### 6. Port Configuration
- **Question**: "What ports should each service expose?"
  - Frontend (default: 3000, 8080)
  - Backend API (default: 8000, 5000)
  - Database (default: 5432, 3306, 27017)
  - Custom ports for specific services
- **Why ask**: Prevents port conflicts and ensures proper routing
- **Follow-up**: "Do you have any existing services running on these ports?"

#### 7. Environment Variables
- **Question**: "What environment variables does your application need?"
  - Database connection strings
  - API keys (development only)
  - Feature flags
  - Service URLs
  - Configuration values
- **Why ask**: Determines .env file content
- **Follow-up**: "Which values should be different between environments?"

#### 8. Live Reload Requirements
- **Question**: "Which services need live reload during development?"
  - Hot reload for frontend (React, Vue, Angular)
  - Auto-restart for backend (nodemon, uvicorn --reload)
  - File watching for specific directories
- **Why ask**: Determines Tiltfile live_update configuration

---

## Instructions

### MANDATORY STEPS (Must Execute in Order)

---

#### **Step 1: Initial Analysis**

**Purpose**: Understand project context and existing structure

**Actions**:
1. Identify working directory and project name
2. Check if Tilt is installed (`tilt version`)
3. Check if Docker is installed (`docker --version`)
4. Scan project directory for:
   - Existing Dockerfiles or docker-compose.yml
   - Language-specific files (package.json, requirements.txt, go.mod, pom.xml)
   - Framework indicators (Angular, React, Django, Flask, Express)
   - Configuration files
5. Identify services that need to be containerized
6. Note any existing development setup

**Output**: Clear understanding of project structure and services

---

#### **Step 2: Load Index Files**

**Purpose**: Understand available context and memory

**Actions**:
1. Check for relevant context files in `../../context/`
2. Check if `../../memory/skills/generate-tilt-dev-environment/index.md` exists
3. Identify which context files will be needed based on project type

**Output**: Knowledge of available guidance and memory structure

---

#### **Step 3: Load Project Memory (if exists)**

**Purpose**: Understand previous configurations for this project

**Actions**:
1. Check if `../../memory/skills/generate-tilt-dev-environment/{project-name}/` exists
2. If exists, read:
   - `environment_config.md` - Previous configuration decisions
   - `generated_files.md` - What was generated before
   - `customizations.md` - User-specific modifications
   - `setup_notes.md` - Important setup information
3. If not exists, note this is first-time generation

**Output**: Understanding of project history or recognition of new project

---

#### **Step 4: Load Context**

**Purpose**: Load relevant development environment knowledge

**Actions**:
1. Read relevant context files based on project stack:
   - `../../context/docker/` - If Docker context exists
   - `../../context/python/` - For Python projects
   - `../../context/azure/tiltfile_reference.md` - For Tilt patterns
   - Framework-specific context files
2. Note any best practices or patterns relevant to the project

**Output**: Comprehensive understanding of development environment patterns

---

#### **Step 5: Gather Requirements**

**Purpose**: Understand user's needs through conversation

**Actions**:
1. Ask user about **project type**
2. Ask about **services to containerize**
3. Ask about **programming languages and runtimes**
4. Ask about **database and storage requirements**
5. Ask about **development dependencies**
6. Ask about **port configuration**
7. Ask about **environment variables**
8. Ask about **live reload requirements**
9. Confirm all requirements with user before proceeding

**Output**: Complete specification of environment to generate

---

#### **Step 6: Generate Environment Configuration**

**Purpose**: Create Tilt development environment files

**Actions**:

1. **Generate Tiltfile**:
   - Use `templates/tiltfile_template.txt` as base
   - Configure docker_build() for each service
   - Set up k8s_resource() or docker_compose() orchestration
   - Configure live_update for services that need it:
     ```python
     # Example live_update for Python
     live_update=[
         sync('./src', '/app/src'),
         run('pip install -r requirements.txt', trigger='requirements.txt'),
         restart_container()
     ]
     ```
   - Add local_resource() for build tasks
   - Configure resource dependencies
   - Add custom commands and buttons

2. **Generate docker-compose.yml**:
   - Use `templates/docker_compose_template.txt`
   - Add service for each containerized component
   - Configure networks and volumes
   - Set environment variables
   - Map ports correctly
   - Add health checks where appropriate
   - Configure service dependencies (depends_on)

3. **Generate Dockerfiles for each service**:
   - Use `templates/dockerfile_template.txt`
   - Customize for each runtime (Python/Node/.NET/Go/Java)
   - Configure multi-stage builds if appropriate
   - Add development tools and dependencies
   - Set up working directory
   - Configure proper layer caching
   - Add .dockerignore support

4. **Generate environment files**:
   - `.env.example` - Template with all required variables
   - `.env` - Local development values (add to .gitignore)
   - `.env.local` - Optional override file
   - Document each variable purpose

5. **Generate Makefile**:
   - Use `templates/makefile_template.txt`
   - Add common commands:
     - `make up` - Start Tilt
     - `make down` - Stop services
     - `make logs` - View logs
     - `make clean` - Clean up containers/volumes
     - `make rebuild` - Force rebuild
     - `make shell-<service>` - Access service shell
   - Add project-specific commands

6. **Generate initialization scripts**:
   - Database seed scripts
   - Data migration scripts
   - Service health check scripts
   - Setup/teardown scripts

7. **Generate .dockerignore**:
   - Exclude common patterns (node_modules, __pycache__, .git)
   - Exclude build artifacts
   - Project-specific exclusions

8. **Generate README.md** with:
   - Project overview
   - Prerequisites (Docker, Tilt)
   - Quick start guide
   - Service descriptions and endpoints
   - Environment variable documentation
   - Common commands
   - Troubleshooting guide

**Output**: Complete environment configuration with all files generated

---

#### **Step 7: Validate Generated Configuration**

**Purpose**: Ensure configuration works before presenting to user

**Actions**:
1. Verify all required files exist
2. Check Tiltfile syntax (no obvious errors)
3. Verify docker-compose.yml is valid YAML
4. Ensure Dockerfiles have proper structure
5. Check that ports don't conflict
6. Verify file paths are correct
7. Ensure environment variables are documented

**Do NOT run `tilt up` or `docker build`** - just validate file structure and syntax

**Output**: Confidence that generated environment is correct

---

#### **Step 8: Present Results to User**

**Purpose**: Show user what was generated and next steps

**Actions**:
1. List all generated files with brief description
2. Highlight key configuration decisions made
3. Show directory structure
4. Provide next steps:
   ```bash
   # Copy example environment file
   cp .env.example .env
   
   # Start development environment
   tilt up
   
   # Or use Makefile
   make up
   ```
5. Point to README.md for detailed instructions
6. Mention Tilt UI at http://localhost:10350
7. List service endpoints and ports

**Output**: User understands what was created and how to use it

---

#### **Step 9: Update Project Memory**

**Purpose**: Store configuration for future reference

**Actions**:
1. Create `../../memory/skills/generate-tilt-dev-environment/{project-name}/` directory
2. Create `environment_config.md`:
   - Project type
   - Services configured
   - Programming languages and versions
   - Ports assigned
   - Environment variables
   - Live reload configuration
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
   - Debugging tips

**Output**: Memory stored for future skill invocations

---

## Best Practices

### Tilt Configuration

1. **Use live_update**: Essential for fast development iteration
2. **Set resource_deps**: Ensure proper service startup order
3. **Add helpful labels**: Group related services
4. **Include links**: Make endpoints easily accessible in Tilt UI
5. **Configure triggers**: Control when rebuilds happen
6. **Add custom buttons**: Common operations accessible via UI

### Docker Configuration

1. **Multi-stage builds**: Keep production images small
2. **Layer caching**: Order commands for optimal caching
3. **Use .dockerignore**: Reduce build context size
4. **Pin versions**: Specify exact versions for reproducibility
5. **Health checks**: Ensure services are ready before dependencies start
6. **Named volumes**: Persist data across container restarts

### Environment Management

1. **Document all variables**: Use .env.example as template
2. **Never commit secrets**: Keep .env in .gitignore
3. **Use different values per environment**: Development vs testing vs production
4. **Validate required variables**: Fail fast if missing
5. **Use sensible defaults**: Minimize configuration burden

### Service Orchestration

1. **Start dependencies first**: Database before API
2. **Wait for health**: Use health checks, not sleep
3. **Graceful shutdown**: Handle SIGTERM properly
4. **Log aggregation**: Use Docker logging drivers
5. **Network isolation**: Use Docker networks properly

---

## Error Handling

### Common Issues

1. **Port conflicts**: Check for existing services, use alternative ports
2. **Permission errors**: Ensure proper file/volume permissions
3. **Build failures**: Check Dockerfile syntax, verify base images exist
4. **Network issues**: Verify service names match in docker-compose and Tilt
5. **Environment variables**: Check for missing required variables

### Debugging

1. **Use `tilt logs <service>`**: View service logs
2. **Check Tilt UI**: Visual representation of service status
3. **Use `docker-compose ps`**: Verify services are running
4. **Exec into containers**: `docker-compose exec <service> /bin/sh`
5. **Validate YAML**: Use yamllint or online validators

---

## Version History

- **1.0.0** (2026-02-06): Initial implementation
  - Tiltfile generation with live reload
  - Docker Compose orchestration
  - Multi-language support (Python, Node.js, .NET, Go, Java)
  - Environment variable management
  - Makefile with common commands
  - Memory system for configuration tracking

---

## Related Skills

- **generate-azure-functions**: For Azure Functions development
- **generate-mock-service**: For creating mock services
- **test-cli-tools**: For validating CLI tools in the environment

---

## References

- [Tilt Documentation](https://docs.tilt.dev/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
