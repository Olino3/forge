---
name: azure-function
description: "Deploy serverless logic with Azure Functions including local development with Tilt and Azurite"
category: orchestration
complexity: intermediate
skills: [generate-azure-functions, generate-tilt-dev-environment, generate-azure-bicep]
context: [azure, commands/serverless_patterns]
---

# /azure-function - Serverless Azure Functions Deployment

## Triggers
- Creating serverless APIs and event-driven functions
- Building HTTP triggers, timer triggers, or queue-triggered functions
- Implementing microservices with Azure Functions
- Setting up local development environment for Azure Functions

## Usage
```
/azure-function [function-name] [--runtime python|node|dotnet] [--trigger http|timer|queue|blob|eventhub] [--local-dev]
```

**Parameters**:
- `function-name`: Name of the function or function app (required)
- `--runtime`: Function runtime (default: auto-detect from project)
  - `python`: Python 3.8, 3.9, 3.10, 3.11
  - `node`: Node.js 14, 16, 18, 20
  - `dotnet`: .NET 6, .NET 7, .NET 8
- `--trigger`: Trigger type (default: http)
  - `http`: HTTP-triggered function (REST API)
  - `timer`: Scheduled function (cron)
  - `queue`: Azure Storage Queue trigger
  - `blob`: Blob storage trigger (file processing)
  - `eventhub`: Event Hub trigger (streaming)
  - `servicebus`: Service Bus trigger
- `--local-dev`: Set up local development with Tilt and Azurite (default: true)

## Workflow

### Step 1: Analyze Requirements

1. Identify function purpose:
   - API endpoint, scheduled job, event processor?
   - Input and output bindings needed?
   - Dependencies on other Azure services?
2. Detect or confirm runtime:
   - Check existing project files
   - Determine version compatibility
3. Determine local development needs:
   - Docker available for Tilt and Azurite?
   - Need for emulated storage?

### Step 2: Load Context & Memory

**Context Loading** (via ContextProvider):
1. Load serverless best practices: `contextProvider.getConditionalContext("commands", "serverless_patterns")`
2. Load Azure-specific patterns: `contextProvider.getConditionalContext("azure", "index")`
3. Load Functions configuration: `contextProvider.getConditionalContext("azure", "azure_functions")`
4. Load local development setup: `contextProvider.getConditionalContext("azure", "tilt_azurite")`

**Memory Loading** (via MemoryStore):
1. Determine project name
2. Load existing functions: `memoryStore.getCommandMemory("azure-function", project)`
3. Load function patterns: `memoryStore.getSkillMemory("generate-azure-functions", project)`
4. Check for existing Azure infrastructure configuration

### Step 3: Gather Function Details

If details not provided, gather interactively:

**Questions**:
- What does this function do? (brief description)
- What triggers it? (HTTP, timer, queue, etc.)
- What inputs does it need? (parameters, body, queue message)
- What outputs does it produce? (HTTP response, queue, blob)
- What Azure services does it use? (Cosmos DB, Blob Storage, etc.)
- Need authentication? (anonymous, function key, Azure AD)

### Step 4: Delegate to Skills

**Generate Azure Function**:
```
skill:generate-azure-functions --name {function-name} --runtime {runtime} --trigger {trigger}
```

Skill handles:
- Function project scaffolding
- Function code template with bindings
- `function.json` or attributes configuration
- Dependencies (requirements.txt, package.json, .csproj)
- Application settings templates

**Generate Local Dev Environment** (if --local-dev):
```
skill:generate-tilt-dev-environment --target azure-function --runtime {runtime}
```

Skill handles:
- Tiltfile for live reload
- Docker Compose with Azurite (storage emulator)
- Connection string configuration
- Hot reload setup

**Generate Infrastructure** (optional):
```
skill:generate-azure-bicep --resource-type function-app --runtime {runtime}
```

Skill handles:
- Bicep template for Function App
- App Service Plan (Consumption or Premium)
- Application Insights
- Storage Account

### Step 5: Configure Bindings and Dependencies

1. Set up input/output bindings:
   - HTTP trigger: Request/response bindings
   - Timer: Cron schedule expression
   - Queue: Connection string, queue name
   - Blob: Container, path pattern
2. Configure application settings:
   - Connection strings (Storage, Cosmos DB, etc.)
   - API keys and secrets
   - Feature flags
3. Add dependencies:
   - Azure SDK packages
   - Third-party libraries
   - Shared packages (if multi-function app)

### Step 6: Local Development Setup

If `--local-dev` enabled:

1. Create Tiltfile for live reload:
   - Watch function code
   - Rebuild on changes
   - Hot reload without restarting
2. Set up Azurite for local storage:
   - Blob storage emulation
   - Queue storage emulation
   - Table storage emulation
3. Configure local.settings.json:
   - Use Azurite connection strings
   - Set local-only settings
4. Create Makefile for common tasks:
   - `make dev`: Start Tilt
   - `make test`: Run tests
   - `make deploy`: Deploy to Azure

### Step 7: Generate Output & Update Memory

**Output**:
Save function documentation to `/claudedocs/azure-function_{name}_{date}.md`:

```markdown
# Azure Function - {Function Name}
**Date**: {date}
**Command**: /azure-function {full invocation}
**Runtime**: {runtime}
**Trigger**: {trigger}

## Function Overview
**Purpose**: {brief description}
**Trigger**: {trigger type}
**Input Bindings**: {list}
**Output Bindings**: {list}

## Project Structure
```
{function-name}/
├── {function-name}/          # Function code
│   ├── __init__.py           # Function handler (Python)
│   └── function.json         # Bindings (v1 model)
├── host.json                 # Function app configuration
├── local.settings.json       # Local development settings
├── requirements.txt          # Dependencies (Python)
├── Tiltfile                  # Local dev with Tilt
├── docker-compose.yml        # Azurite and dependencies
└── infrastructure/           # Bicep templates
    └── main.bicep
```

## Function Code
**File**: `{function-name}/__init__.py` (Python example)

```python
import logging
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing HTTP request')
    
    name = req.params.get('name')
    if not name:
        return func.HttpResponse(
            "Please pass a name",
            status_code=400
        )
    
    return func.HttpResponse(
        f"Hello, {name}!",
        status_code=200
    )
```

## Bindings Configuration

### function.json (v1 model)
```json
{
  "bindings": [
    {
      "authLevel": "function",
      "type": "httpTrigger",
      "direction": "in",
      "name": "req",
      "methods": ["get", "post"]
    },
    {
      "type": "http",
      "direction": "out",
      "name": "$return"
    }
  ]
}
```

## Local Development

### Start Local Environment
```bash
# Using Tilt (recommended)
tilt up

# Or manually
docker-compose up azurite
func start
```

### Test Function Locally
```bash
curl http://localhost:7071/api/{function-name}?name=World
# Response: Hello, World!
```

### Environment Variables
**local.settings.json**:
```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "{runtime}",
    "COSMOS_CONNECTION_STRING": "..."
  }
}
```

## Deployment

### Deploy to Azure
```bash
# Create Function App (if not exists)
az functionapp create \
  --resource-group {rg} \
  --name {function-app-name} \
  --storage-account {storage} \
  --runtime {runtime} \
  --functions-version 4 \
  --consumption-plan-location eastus

# Deploy function code
func azure functionapp publish {function-app-name}
```

### Infrastructure Deployment
```bash
# Deploy infrastructure with Bicep
az deployment group create \
  --resource-group {rg} \
  --template-file infrastructure/main.bicep \
  --parameters functionAppName={name}
```

## Application Settings
Configure in Azure Portal or with CLI:
```bash
az functionapp config appsettings set \
  --name {function-app-name} \
  --resource-group {rg} \
  --settings "COSMOS_CONNECTION_STRING=@Microsoft.KeyVault(...)"
```

## Monitoring
- **Application Insights**: Enabled by default
- **Logs**: Azure Portal > Function App > Monitor
- **Metrics**: Execution count, duration, errors
- **Live Metrics**: Real-time monitoring

## Testing
```bash
# Unit tests
pytest tests/

# Integration tests (with Azurite)
docker-compose up -d azurite
pytest tests/integration/
```

## CI/CD Integration
Use `/azure-pipeline` to create CI/CD pipeline:
```bash
/azure-pipeline {function-name} --target function
```

## Next Steps
- Test locally: `tilt up`
- Add more functions: Create new function folders
- Deploy to Azure: `func azure functionapp publish`
- Set up monitoring: Configure alerts in Application Insights
- Use `/azure-pipeline` for automated deployment
```

**Memory Updates** (via MemoryStore):
1. `memoryStore.append("commands", project, "command_history.md", entry)`
2. `memoryStore.update("commands", project, "azure_functions.md", content)`:
   - Function names, triggers, runtimes
   - Deployment configuration
3. `memoryStore.update("skills", project, "generate-azure-functions", functionPatterns)` — update skill memory with function patterns

## Tool Coordination
- **Read**: Existing function code, configuration files
- **Grep/Glob**: Find existing functions and infrastructure
- **Write**: Function code, Bicep templates, documentation
- **Bash**: Azure CLI commands, Tilt, Docker operations
- **Skills**: generate-azure-functions, generate-tilt-dev-environment, generate-azure-bicep

## Key Patterns
- **Local-First**: Development with Tilt and Azurite before Azure deployment
- **Infrastructure as Code**: Bicep templates for reproducible deployments
- **Binding-Driven**: Declarative bindings for integrations
- **Monitoring-Ready**: Application Insights configured by default

## Boundaries

**Will:**
- Generate complete Azure Functions projects with scaffolding
- Set up local development environment with Tilt and Azurite
- Create infrastructure as code (Bicep) for Function Apps
- Configure bindings for various triggers and outputs
- Delegate to specialized skills for function generation

**Will Not:**
- Write complete business logic (provides templates)
- Create Azure resources directly (provides infrastructure code)
- Handle complex multi-tenant scenarios without guidance
- Replace manual testing and validation

**Output**: Function documentation saved to `/claudedocs/azure-function_{name}_{date}.md`

**Next Step**: Use `tilt up` for local development, or `/azure-pipeline` for CI/CD setup.
