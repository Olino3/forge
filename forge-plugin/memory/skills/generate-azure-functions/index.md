# Memory Structure: generate-azure-functions

## Purpose

This directory stores **project-specific** Azure Functions configurations, generated files, and customizations learned during project generation. Each project gets its own subdirectory to track generation history and user preferences.

## Conceptual Overview

### Memory vs Context

- **Context** (`../../../context/azure/`): **Shared, static** Azure Functions standards (Tiltfile patterns, Dockerfile templates, best practices)
- **Memory** (this directory): **Project-specific, dynamic** generation history (which files were generated, user choices, customizations)

**Example**:
- Context says: "Here's how to structure a Tiltfile for Azure Functions with live reload"
- Memory records: "In this project, we generated 3 function apps (orchestrator, processor, loader) using Python 3.11 with v2 model and Poetry for dependencies"

## Directory Structure

```
generate-azure-functions/
├── index.md                    # This file - explains memory structure
└── {project-name}/             # Per-project memory (created on first use)
    ├── project_config.md       # Configuration decisions made
    ├── generated_files.md      # Complete list of generated files
    ├── customizations.md       # User-specific modifications
    └── setup_notes.md          # Important setup information
```

## Memory Files

### 1. `project_config.md`

**What to store**:
- Programming model chosen (v1, v2, v4)
- Runtime and version (Python 3.11, Node.js 18, etc.)
- Function app names and ports
- Storage resources (containers, queues, tables)
- Dependency management approach (pip, Poetry, npm)
- Local package dependencies (if any)
- Generation timestamp and skill version

**Example content**:
```markdown
# Project Configuration for my-data-pipeline

**Generated**: 2025-11-18 15:30:00
**Skill Version**: generate-azure-functions v1.0.0

## Programming Model

- **Model**: v2 (Python modern, decorator-based)
- **Runtime**: Python 3.11
- **Dependency Management**: Poetry

## Function Apps

1. **orchestrator**
   - Port: 7071
   - Triggers: HTTP (POST /api/orchestrate)
   - Purpose: Split and route incoming files

2. **processor**
   - Port: 7072
   - Triggers: Blob trigger (queued container)
   - Purpose: Transform data

3. **loader**
   - Port: 7073
   - Triggers: HTTP (POST /api/load)
   - Purpose: Load to external systems

## Storage Resources

### Blob Containers
- `raw` - Raw input files
- `queued` - Files ready for processing
- `processed` - Processed files
- `loaded` - Successfully loaded files

### Queues
- `processing-queue` - Files to process

### Tables
- `AuditLog` - Processing audit log
- `ProcessingStatus` - Current processing status

## Local Package Dependencies

- **Package Name**: data-utils
- **Path**: ./data-utils
- **Purpose**: Shared data transformation utilities
- **Build**: Poetry build to wheel, installed in all function apps

## Custom Environment Variables

- `PALANTE_ENVIRONMENT` - Environment identifier (development, staging, production)

## Azurite Account Key

Custom key generated and stored in .env.local (not committed to git)
```

---

### 2. `generated_files.md`

**What to store**:
- Complete list of all generated files
- Timestamp of generation
- File purpose and description
- Whether file should be modified by user
- Template used for generation

**Example content**:
```markdown
# Generated Files for my-data-pipeline

**Generated**: 2025-11-18 15:30:00

## Docker Configuration

### .docker/orchestrator/Dockerfile
- **Purpose**: Dockerfile for orchestrator function app
- **Template**: dockerfile_template.txt (Python + Poetry + local package)
- **User Editable**: Yes (for adding system packages or custom build steps)

### .docker/processor/Dockerfile
- **Purpose**: Dockerfile for processor function app
- **Template**: dockerfile_template.txt (Python + Poetry + local package)
- **User Editable**: Yes

### .docker/loader/Dockerfile
- **Purpose**: Dockerfile for loader function app
- **Template**: dockerfile_template.txt (Python + Poetry + local package)
- **User Editable**: Yes

### .docker/azurite/Dockerfile
- **Purpose**: Dockerfile for Azurite storage emulator with initialization
- **Template**: azurite_dockerfile_template.txt
- **User Editable**: Rarely (unless changing initialization approach)

### .docker/docker-compose.dev.yml
- **Purpose**: Docker Compose configuration for all services
- **Template**: docker_compose_template.txt
- **User Editable**: Yes (for adding new services or environment variables)

### .docker/scripts/init_azurite.sh
- **Purpose**: Azurite initialization script (create containers/queues/tables)
- **Template**: init_azurite_template.sh
- **User Editable**: Yes (to add more storage resources or test data)

## Tilt Configuration

### Tiltfile
- **Purpose**: Tilt orchestration with live reload
- **Template**: tiltfile_template.txt
- **User Editable**: Yes (to customize build behavior or add services)

## Environment Configuration

### .env.local
- **Purpose**: Local environment variables (secrets, ports)
- **Template**: env_template.txt
- **User Editable**: Yes (add custom variables)
- **Git Tracked**: NO (in .gitignore)

## Function Apps

### functions/orchestrator/
- **Generated by**: Azure Functions CLI (func init)
- **Files**: function_app.py, host.json, pyproject.toml, local.settings.json
- **User Editable**: Yes (this is where you write your function code)

### functions/processor/
- **Generated by**: Azure Functions CLI
- **User Editable**: Yes

### functions/loader/
- **Generated by**: Azure Functions CLI
- **User Editable**: Yes

## Ignore Files

### .gitignore
- **Purpose**: Git ignore patterns
- **User Editable**: Yes (add project-specific patterns)

### .dockerignore
- **Purpose**: Docker build context ignore patterns
- **User Editable**: Yes

### functions/*/..funcignore
- **Purpose**: Azure Functions deployment ignore patterns
- **User Editable**: Rarely

## Documentation

### README.md
- **Purpose**: Project documentation with setup instructions
- **Generated**: Yes (comprehensive setup guide)
- **User Editable**: Yes (add project-specific details)

## Total Files Generated

- Docker configuration: 6 files
- Tilt configuration: 1 file
- Environment configuration: 1 file
- Function apps: 3 directories (12+ files via CLI)
- Ignore files: 4 files
- Documentation: 1 file

**Total**: ~25+ files
```

---

### 3. `customizations.md`

**What to store**:
- User-specific requirements not captured in standard templates
- Deviations from default patterns
- Special configurations
- Reasons for non-standard choices

**Example content**:
```markdown
# Customizations for my-data-pipeline

## Custom Environment Variables

User requested custom environment variable for tracking environment:
- `PALANTE_ENVIRONMENT` - Set to "development", "staging", or "production"
- Used across all three function apps
- Determines which external systems to connect to

## Port Assignments

Default ports (7071, 7072, 7073) used without modification.

## Azurite Storage Resources

User requested additional table beyond defaults:
- `ProcessingStatus` table - Tracks current processing status for each file
  - PartitionKey: filename
  - RowKey: timestamp
  - Fields: status, error_message, processed_rows

## Local Package Integration

User has existing `data-utils` package that needs to be shared across all functions:
- Located at ./data-utils
- Built with Poetry
- Contains data transformation utilities
- All Dockerfiles updated to build and install this package
- Tilt live_update configured to rebuild package on changes

## Dockerfile System Packages

User requested Azure CLI be installed in all function app containers:
- Needed for accessing Azure Key Vault secrets
- Added to all function Dockerfiles

## Docker Compose Volumes

User requested Azure CLI credentials be mounted from host:
- Mounted $HOME/.azure:/root/.azure in all function services
- Allows using Azure CLI authentication from host machine

## Dependency Management

User chose Poetry over pip for better dependency management:
- Each function app has pyproject.toml and poetry.lock
- Dockerfiles use poetry export to generate requirements.txt
- Live reload configured to detect poetry.lock changes

## Programming Model

User chose v2 model (modern Python with decorators):
- Cleaner code
- All functions in single function_app.py per app
- No function.json files needed
```

---

### 4. `setup_notes.md`

**What to store**:
- Important setup information
- Known issues or quirks
- Testing recommendations
- Deployment considerations
- Troubleshooting tips

**Example content**:
```markdown
# Setup Notes for my-data-pipeline

## Prerequisites Verified

- Docker Desktop installed and running
- Tilt installed (v0.33.1)
- Azure Functions Core Tools installed (v4.0.5455)
- Python 3.11 installed
- Poetry installed (v1.7.0)

## First-Time Setup

1. Generate custom Azurite key:
   ```bash
   python scripts/project_generator.py generate-key > .azurite-key
   ```

2. Create .env.local from template (already done):
   ```bash
   cp .env.local.template .env.local
   ```

3. Start development environment:
   ```bash
   tilt up
   ```

4. Wait for all services to be green in Tilt UI (http://localhost:10350)

## Testing Recommendations

### Test Orchestrator
```bash
curl -X POST http://localhost:7071/api/orchestrate \
  -H "Content-Type: application/json" \
  -d '{"filename": "test.csv"}'
```

### Test Processor
Upload file to `queued` container via Azure Storage Explorer, or:
```bash
curl -X POST http://localhost:7072/api/process \
  -H "Content-Type: application/json" \
  -d '{"filename": "test.csv"}'
```

### Test Loader
```bash
curl -X POST http://localhost:7073/api/load \
  -H "Content-Type: application/json" \
  -d '{"filename": "test.csv"}'
```

## Known Issues

### Issue: data-utils package not found

**Symptom**: ImportError when importing from data_utils package

**Cause**: Local package not rebuilt after changes

**Solution**: Tilt should auto-rebuild, but if not:
```bash
# In Tilt UI, trigger rebuild of affected function
# Or restart Tilt: tilt down && tilt up
```

### Issue: Azurite initialization fails

**Symptom**: Function apps can't connect to Azurite

**Cause**: Azurite not fully initialized before functions start

**Solution**: Check Tilt UI for azurite and init-azurite resources. Should be green before functions start. If issue persists, restart Tilt.

## Development Workflow

1. Make code changes in functions/{app-name}/
2. Tilt automatically syncs changes to container
3. Container restarts (< 5 seconds)
4. Test changes immediately

For dependency changes:
1. Update pyproject.toml in function directory
2. Run `poetry lock` locally
3. Tilt detects poetry.lock change
4. Dependencies reinstalled in container
5. Container restarts

For data-utils changes:
1. Make changes in ./data-utils/src/
2. Tilt detects changes
3. Package rebuilt and reinstalled
4. All function containers restart

## Deployment Considerations

### Preparing for Azure Deployment

1. Update connection strings to use Azure Storage (not Azurite)
2. Set AZURE_STORAGE_CONNECTION_STRING in Azure Function App settings
3. Deploy each function app separately:
   ```bash
   cd functions/orchestrator
   func azure functionapp publish my-orchestrator-func-app
   ```

### Environment Variables

Production environment variables to set in Azure:
- AZURE_STORAGE_CONNECTION_STRING (Azure Storage account)
- PALANTE_ENVIRONMENT=production
- Any custom variables from .env.local

### Secrets Management

For production, migrate secrets from .env.local to:
- Azure Key Vault (recommended)
- Azure Function App Application Settings (encrypted)

## Troubleshooting

### Container won't start

Check Docker Desktop has enough resources:
- Memory: At least 4GB (6GB+ recommended for 3 function apps)
- CPU: At least 2 cores

### Port conflicts

If ports 7071-7073 are in use, update .env.local:
```bash
ORCHESTRATOR_HOST_PORT=8071
PROCESSOR_HOST_PORT=8072
LOADER_HOST_PORT=8073
```

Then restart Tilt.

### Live reload not working

1. Check Tilt UI for errors
2. Verify file paths in Tiltfile sync() calls match actual structure
3. Try manual rebuild in Tilt UI
4. Restart Tilt as last resort

## Performance Tips

- Keep .dockerignore updated to exclude unnecessary files
- Use Docker layer caching (already configured)
- Only run needed function apps: `tilt up orchestrator`
- Stop Tilt when not developing: `tilt down`
```

---

## Workflow

### When Creating Memory (First Time)

1. **During Step 1 (Initial Analysis)**:
   - Identify project name from repository or user specification
   - Check if `{project-name}/` directory exists
   - If not exists, note that memory will be created in Step 9

2. **During Step 3 (Load Project Memory)**:
   - If directory doesn't exist: Note this is first-time generation
   - Continue with empty memory

3. **During Step 9 (Update Memory)**:
   - Create `{project-name}/` directory
   - Create all four memory files with configuration details
   - Document all choices made during generation
   - Record any deviations from standard templates

### When Using Existing Memory (Subsequent Times)

1. **During Step 3 (Load Project Memory)**:
   - Read all existing memory files
   - Know what was generated before
   - Understand customizations made
   - Determine if regenerating or adding to existing

2. **During Step 9 (Update Memory)**:
   - **Update** project_config.md if configuration changed
   - **Append** to generated_files.md if new files added
   - **Add** to customizations.md for new user requirements
   - **Append** to setup_notes.md for new issues or tips discovered

## Memory Evolution

Memory should grow and improve over time:

### First Generation
- Establish baseline configuration
- Document initial choices
- Record generated files
- Capture setup process

### Subsequent Generations
- Update when adding new function apps
- Track new customizations
- Document encountered issues and solutions
- Refine setup instructions based on experience

### Maintenance
- Update when Azure Functions runtime changes
- Document migration from v1 to v2 (if applicable)
- Track changes in dependency management
- Update deployment procedures

## Best Practices

1. **Be Specific**: Document exact versions (Python 3.11, not just "Python 3")
2. **Include Timestamps**: Always timestamp generation and updates
3. **Explain Choices**: Document WHY a choice was made, not just WHAT
4. **Track Deviations**: Note when user requests non-standard configuration
5. **Document Issues**: Capture problems encountered and solutions
6. **Link to Generated Files**: Reference specific files and line numbers when relevant
7. **Update Regularly**: Keep memory current with project state

## Related Files

- `../../../context/azure/` - Azure Functions context (shared standards)
- `../../../skills/generate-azure-functions/SKILL.md` - Skill workflow
- `/claudedocs/` - Detailed generation reports (if created)

---

## Example Memory Snippet

Here's a minimal example of project memory after first generation:

**project_config.md**:
```markdown
# Project Configuration for simple-api

**Generated**: 2025-11-18 16:00:00
**Skill Version**: v1.0.0

## Programming Model
- Model: v2
- Runtime: Python 3.11
- Dependency Management: pip

## Function Apps
1. api (Port: 7071) - HTTP triggers

## Storage Resources
- Blob: data
- Table: AuditLog
```

**generated_files.md**:
```markdown
# Generated Files for simple-api

**Generated**: 2025-11-18 16:00:00

- Tiltfile
- .docker/api/Dockerfile
- .docker/azurite/Dockerfile
- .docker/docker-compose.dev.yml
- .docker/scripts/init_azurite.sh
- .env.local
- functions/api/ (via Azure Functions CLI)
- README.md
```

**customizations.md**:
```markdown
# Customizations for simple-api

No special customizations. Standard v2 Python project with single HTTP trigger function.
```

**setup_notes.md**:
```markdown
# Setup Notes for simple-api

## First-Time Setup
1. Run `tilt up`
2. Access API at http://localhost:7071/api/hello

No issues encountered during setup.
```

---

This memory structure enables the skill to:
- Remember project configuration for future updates
- Avoid regenerating files unnecessarily
- Understand user's custom requirements
- Provide better assistance on subsequent invocations
