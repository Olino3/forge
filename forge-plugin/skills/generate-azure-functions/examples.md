# Azure Functions Generation Examples

This file demonstrates typical usage scenarios for the `generate-azure-functions` skill.

---

## Example 1: Simple HTTP Trigger Function (v2 Model)

### User Request

"I need to create a new Azure Functions project with a simple HTTP trigger. I want to use the modern Python v2 model and be able to develop it locally."

### Skill Execution

**Step 1-4**: Load context and understand Azure Functions patterns.

**Step 5: Requirements Gathering**

Claude asks:
- **Programming model?** → v2 (modern, recommended)
- **Runtime?** → Python 3.11
- **Function types?** → HTTP trigger
- **Number of function apps?** → 1
- **Function app name?** → "api"
- **Storage requirements?** → Just basic blob container for testing
- **Dependency management?** → pip (simple project)
- **Local packages?** → No

**Step 6: Project Generation**

Generated structure:
```
my-api-project/
├── .docker/
│   ├── api/
│   │   └── Dockerfile
│   ├── azurite/
│   │   └── Dockerfile
│   ├── docker-compose.dev.yml
│   └── scripts/
│       └── init_azurite.sh
├── functions/
│   └── api/
│       ├── function_app.py
│       ├── host.json
│       ├── requirements.txt
│       ├── local.settings.json
│       └── .funcignore
├── Tiltfile
├── .env.local
├── .gitignore
├── .dockerignore
└── README.md
```

**function_app.py** (generated):
```python
import azure.functions as func
import logging

app = func.FunctionApp()

@app.function_name(name="HttpExample")
@app.route(route="hello", auth_level=func.AuthLevel.ANONYMOUS)
def http_example(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}!")
    else:
        return func.HttpResponse(
            "Please pass a name on the query string or in the request body",
            status_code=400
        )
```

**Step 8: User Instructions**

```bash
cd my-api-project
tilt up

# Access function at:
# http://localhost:7071/api/hello?name=World
```

---

## Example 2: Multiple Function Apps (Microservices)

### User Request

"I'm building a data processing pipeline with three Azure Functions: an orchestrator that splits files, a processor that transforms data, and a loader that loads to external systems. I need local development with Azurite."

### Skill Execution

**Step 5: Requirements Gathering**

Claude asks:
- **Programming model?** → v2
- **Runtime?** → Python 3.11
- **Function types?** → HTTP triggers, Blob triggers, Queue triggers
- **Number of function apps?** → 3
- **Function app names?** → orchestrator, processor, loader
- **Storage requirements?**:
  - Blob containers: raw, queued, processed, loaded
  - Tables: AuditLog, ProcessingStatus
  - Queues: processing-queue
- **Dependency management?** → Poetry (shared local package)
- **Local packages?** → Yes, shared "data-utils" package at `./data-utils`

**Step 6: Project Generation**

Generated structure:
```
data-pipeline/
├── .docker/
│   ├── orchestrator/
│   │   └── Dockerfile
│   ├── processor/
│   │   └── Dockerfile
│   ├── loader/
│   │   └── Dockerfile
│   ├── azurite/
│   │   └── Dockerfile
│   ├── docker-compose.dev.yml
│   └── scripts/
│       └── init_azurite.sh
├── functions/
│   ├── orchestrator/
│   │   ├── function_app.py
│   │   ├── host.json
│   │   ├── pyproject.toml
│   │   ├── poetry.lock
│   │   └── local.settings.json
│   ├── processor/
│   │   ├── function_app.py
│   │   ├── host.json
│   │   ├── pyproject.toml
│   │   ├── poetry.lock
│   │   └── local.settings.json
│   └── loader/
│       ├── function_app.py
│       ├── host.json
│       ├── pyproject.toml
│       ├── poetry.lock
│       └── local.settings.json
├── data-utils/              # Shared package
│   ├── src/
│   │   └── data_utils/
│   ├── pyproject.toml
│   └── README.md
├── Tiltfile
├── .env.local
└── README.md
```

**Tiltfile** (key sections):
```python
RESOURCE_DEPENDENCIES = {
    'orchestrator': ['azurite', 'init-azurite'],
    'processor': ['azurite', 'init-azurite'],
    'loader': ['azurite', 'init-azurite'],
    'azurite': [],
    'init-azurite': ['azurite']
}

# Build each function with local package
for function_name in ['orchestrator', 'processor', 'loader']:
    docker_build(
        ref=f'data-pipeline-{function_name}-dev',
        context='.',
        dockerfile=f'.docker/{function_name}/Dockerfile',
        live_update=[
            sync(f'./functions/{function_name}/', '/home/site/wwwroot/'),
            sync('./data-utils/src/data_utils', '/tmp/data-utils/src/data_utils'),
            run(
                'cd /tmp/data-utils && poetry build && '
                'pip install --no-cache-dir --force-reinstall dist/*.whl',
                trigger=['./data-utils/src/']
            ),
            restart_container()
        ]
    )
```

**init_azurite.sh** (customized):
```python
containers = [
    ("raw", "Raw input files"),
    ("queued", "Files ready for processing"),
    ("processed", "Processed files"),
    ("loaded", "Successfully loaded files")
]

tables = [
    ("AuditLog", "Processing audit log"),
    ("ProcessingStatus", "Current processing status")
]

queues = [
    ("processing-queue", "Files to process")
]
```

**Step 8: User Instructions**

```bash
cd data-pipeline
tilt up

# Or run specific services:
tilt up orchestrator processor

# Access functions:
# Orchestrator: http://localhost:7071/api/orchestrate
# Processor:    http://localhost:7072/api/process
# Loader:       http://localhost:7073/api/load
```

---

## Example 3: Migrating from v1 to v2

### User Request

"I have an existing Azure Function using the v1 model (function.json files). I want to set up local development with Tilt, but keep using v1 for now."

### Skill Execution

**Step 5: Requirements Gathering**

Claude asks:
- **Programming model?** → v1 (maintain compatibility)
- **Runtime?** → Python 3.10 (existing)
- **Existing functions?** → Yes, HttpTrigger, BlobTrigger, TimerTrigger
- **Storage requirements?** → Containers: uploads, processed
- **Dependency management?** → requirements.txt (existing)

**Step 6: Project Generation**

Generated structure (wraps existing):
```
existing-function/
├── .docker/               # NEW
│   ├── my-function/
│   │   └── Dockerfile
│   ├── azurite/
│   │   └── Dockerfile
│   ├── docker-compose.dev.yml
│   └── scripts/
│       └── init_azurite.sh
├── functions/             # EXISTING (no changes)
│   └── my-function/
│       ├── HttpTrigger/
│       │   ├── __init__.py
│       │   └── function.json
│       ├── BlobTrigger/
│       │   ├── __init__.py
│       │   └── function.json
│       ├── TimerTrigger/
│       │   ├── __init__.py
│       │   └── function.json
│       ├── host.json
│       ├── requirements.txt
│       └── local.settings.json
├── Tiltfile               # NEW
├── .env.local             # NEW
└── README.md              # NEW/UPDATED
```

Claude notes:
- Existing function code untouched
- Added Docker/Tilt wrapper for local development
- Can migrate to v2 later (instructions in README)

---

## Example 4: Node.js Functions with TypeScript

### User Request

"Create a Node.js Azure Functions project with TypeScript. I need HTTP triggers for a REST API."

### Skill Execution

**Step 5: Requirements Gathering**

- **Programming model?** → v4 (Node.js uses v4 for modern model)
- **Runtime?** → Node.js 18
- **Language?** → TypeScript
- **Function types?** → HTTP triggers (REST API)
- **Number of function apps?** → 1 ("api")
- **Storage requirements?** → Basic blob container
- **Package manager?** → npm

**Step 6: Project Generation**

```
my-node-api/
├── .docker/
│   ├── api/
│   │   └── Dockerfile       # Node.js base image
│   ├── azurite/
│   │   └── Dockerfile
│   └── docker-compose.dev.yml
├── functions/
│   └── api/
│       ├── src/
│       │   ├── functions/
│       │   │   ├── httpExample.ts
│       │   │   └── users.ts
│       │   └── index.ts
│       ├── host.json
│       ├── package.json
│       ├── tsconfig.json
│       └── local.settings.json
├── Tiltfile
└── README.md
```

**Dockerfile** (Node.js):
```dockerfile
FROM mcr.microsoft.com/azure-functions/node:4-node18

WORKDIR /home/site/wwwroot
ENV AzureWebJobsScriptRoot=/home/site/wwwroot

COPY functions/api/package*.json ./
RUN npm ci --production

COPY functions/api/ .
RUN npm run build

EXPOSE 80
```

**Tiltfile** (live_update for TypeScript):
```python
live_update=[
    sync('./functions/api/src/', '/home/site/wwwroot/src/'),
    run('npm run build', trigger=['./functions/api/src/']),
    restart_container()
]
```

---

## Example 5: .NET Functions with Entity Framework

### User Request

"I need a .NET 8 Azure Functions project that will use Entity Framework Core. I want local development with SQL Server in Docker."

### Skill Execution

**Step 5: Requirements Gathering**

- **Programming model?** → Isolated worker model (recommended for .NET)
- **Runtime?** → .NET 8
- **Function types?** → HTTP triggers (CRUD API)
- **Storage requirements?** → Need SQL Server (not just Azurite)
- **Database?** → Add SQL Server service

**Step 6: Project Generation**

```
my-dotnet-api/
├── .docker/
│   ├── api/
│   │   └── Dockerfile
│   ├── azurite/
│   │   └── Dockerfile
│   ├── docker-compose.dev.yml   # Includes SQL Server service
│   └── scripts/
│       └── init_azurite.sh
├── functions/
│   └── api/
│       ├── Functions/
│       │   └── UserFunctions.cs
│       ├── Data/
│       │   └── AppDbContext.cs
│       ├── Models/
│       │   └── User.cs
│       ├── Program.cs
│       ├── host.json
│       ├── local.settings.json
│       └── api.csproj
├── Tiltfile
└── README.md
```

**docker-compose.dev.yml** (includes SQL Server):
```yaml
services:
  api:
    # ... function app config ...
    environment:
      - ConnectionStrings__Database=Server=sqlserver;Database=MyDb;...
    depends_on:
      - azurite
      - sqlserver

  sqlserver:
    image: mcr.microsoft.com/mssql/server:2022-latest
    ports:
      - "1433:1433"
    environment:
      - ACCEPT_EULA=Y
      - SA_PASSWORD=${SQL_SA_PASSWORD}
    volumes:
      - sqlserver_data:/var/opt/mssql

  azurite:
    # ... azurite config ...

volumes:
  sqlserver_data:
  azurite_data:
```

Claude notes:
- Added SQL Server service automatically
- Generated connection string configuration
- Reminded user to run migrations (`dotnet ef database update`)

---

## Example 6: Existing Project - Add Local Development

### User Request

"I have an Azure Functions project already deployed to Azure. I want to add Tilt and Azurite for local development without changing my existing code."

### Skill Execution

**Step 3: Load Project Memory**

- Check existing code structure
- Detect programming model (v1 or v2)
- Identify dependencies

**Step 5: Requirements Gathering**

- **Keep existing code?** → Yes (don't modify)
- **Current setup?** → Deployed to Azure, no local dev environment
- **Runtime?** → Auto-detected (Python 3.11, v2 model)
- **Storage resources?** → Auto-detect from code (bindings reveal containers/tables)

**Step 6: Project Generation**

- Generate **only** Docker/Tilt files:
  - `.docker/` directory
  - `Tiltfile`
  - `.env.local`
  - Update `.gitignore`
- Do **not** modify existing function code
- Generate README section "Local Development Setup"

**Step 9: Memory**

Store:
- "Existing project, added local dev only"
- "Do not regenerate function code"
- "Preserve user's code structure"

---

## Common Patterns Across Examples

### User Question Flow

All examples follow:
1. Ask about programming model (v1/v2)
2. Ask about runtime/version
3. Ask about function types and triggers
4. Ask about storage needs
5. Ask about dependencies

### Generated Files

All projects include:
- Tiltfile (orchestration)
- docker-compose.yml (services)
- Dockerfiles (containers)
- Azurite setup (init script)
- Configuration (.env.local, local.settings.json)
- Documentation (README.md)

### Validation

All projects:
- Work with `tilt up` immediately
- Support live reload
- Include proper error handling
- Follow best practices
- Are well-documented

---

These examples demonstrate the versatility of the `generate-azure-functions` skill across different scenarios, runtimes, and complexity levels.
