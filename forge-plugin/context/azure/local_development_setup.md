---
id: "azure/local_development_setup"
domain: azure
title: "Azure Functions Local Development Setup"
type: reference
estimatedTokens: 1650
loadingStrategy: onDemand
version: "0.3.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "Overview"
    estimatedTokens: 12
    keywords: [overview]
  - name: "Architecture"
    estimatedTokens: 65
    keywords: [architecture]
  - name: "Prerequisites"
    estimatedTokens: 79
    keywords: [prerequisites]
  - name: "Standard Port Allocation"
    estimatedTokens: 64
    keywords: [standard, port, allocation]
  - name: "Environment Variables"
    estimatedTokens: 60
    keywords: [environment, variables]
  - name: "Project Structure"
    estimatedTokens: 75
    keywords: [project, structure]
  - name: "local.settings.json Template"
    estimatedTokens: 38
    keywords: [localsettingsjson, template]
  - name: "Development Workflow"
    estimatedTokens: 162
    keywords: [development, workflow]
  - name: "Common Issues and Solutions"
    estimatedTokens: 73
    keywords: [issues, solutions]
  - name: "Best Practices"
    estimatedTokens: 45
    keywords: [best]
  - name: "Debugging"
    estimatedTokens: 51
    keywords: [debugging]
  - name: "Performance Tips"
    estimatedTokens: 32
    keywords: [performance, tips]
  - name: "Official Documentation"
    estimatedTokens: 12
    keywords: [official, documentation]
tags: [azure, local-dev, tilt, azurite, docker, debugging, workflow]
---

# Azure Functions Local Development Setup

## Overview

Local Azure Functions development using **Tilt** (for live reload and orchestration) and **Azurite** (for Azure Storage emulation).

## Architecture

```
┌─────────────────────────────────────────────────┐
│                    Tilt                         │
│  (Orchestrates Docker containers + live reload) │
└────────┬──────────────────────────┬─────────────┘
         │                          │
    ┌────▼─────┐              ┌─────▼──────┐
    │ Function │              │  Azurite   │
    │   Apps   │◄─────────────┤  Storage   │
    │ (Docker) │  Connection  │ Emulator   │
    └──────────┘              └────────────┘
         │
    ┌────▼─────┐
    │   HTTP   │
    │  Clients │
    └──────────┘
```

**Components**:
- **Tilt**: Orchestrates Docker builds, live updates, and service dependencies
- **Azurite**: Local Azure Storage emulator (Blob, Queue, Table)
- **Docker Compose**: Defines services and networking
- **Function Apps**: Run in Docker containers with Azure Functions runtime

---

## Prerequisites

### Required Tools

1. **Docker Desktop** or Docker Engine
   ```bash
   docker --version  # Should be 20.x or higher
   ```

2. **Tilt**
   ```bash
   # macOS
   brew install tilt

   # Linux
   curl -fsSL https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.sh | bash

   # Verify
   tilt version
   ```

3. **Azure Functions Core Tools**
   ```bash
   # macOS
   brew tap azure/functions
   brew install azure-functions-core-tools@4

   # Linux
   curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
   sudo mv microsoft.gpg /etc/apt/trusted.gpg.d/microsoft.gpg
   sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/microsoft-ubuntu-$(lsb_release -cs)-prod $(lsb_release -cs) main" > /etc/apt/sources.list.d/dotnetdev.list'
   sudo apt update
   sudo apt install azure-functions-core-tools-4

   # Verify
   func --version  # Should be 4.x
   ```

4. **Python 3.9+** (for Python functions)
   ```bash
   python --version
   ```

---

## Standard Port Allocation

| Service | Port | Protocol | Purpose |
|---------|------|----------|---------|
| Function App 1 | 7071 | HTTP | Primary function app |
| Function App 2 | 7072 | HTTP | Secondary function app |
| Function App N | 7070+N | HTTP | Additional function apps |
| Azurite Blob | 10000 | HTTP | Blob storage emulator |
| Azurite Queue | 10001 | HTTP | Queue storage emulator |
| Azurite Table | 10002 | HTTP | Table storage emulator |

---

## Environment Variables

### Required for Function Apps

```bash
# Azure Functions Runtime
FUNCTIONS_WORKER_RUNTIME=python  # or node, dotnet

# Azurite Connection (local development)
AzureWebJobsStorage=UseDevelopmentStorage=true;DevelopmentStorageProxyUri=http://azurite

# Full Azurite Connection String
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=${AZURITE_ACCOUNT_KEY};BlobEndpoint=http://azurite:10000/devstoreaccount1;QueueEndpoint=http://azurite:10001/devstoreaccount1;TableEndpoint=http://azurite:10002/devstoreaccount1
```

### Required for Azurite

```bash
# Azurite Account Configuration
AZURITE_ACCOUNTS=devstoreaccount1
AZURITE_ACCOUNT_KEY=<your-custom-key-or-use-default>
```

**Default Azurite Account Key** (standard emulator key):
```
Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==
```

**Recommended**: Generate custom key and store in `.env.local` (add to `.gitignore`):
```bash
# Generate a random key (example)
openssl rand -base64 64 | tr -d '\n' > .azurite-key
```

---

## Project Structure

Recommended directory structure:

```
my-azure-project/
├── .docker/                        # Docker configurations
│   ├── azurite/
│   │   └── Dockerfile             # Azurite container
│   ├── my-function/
│   │   └── Dockerfile             # Function app container
│   ├── docker-compose.dev.yml     # Development services
│   └── scripts/
│       └── init_azurite.sh        # Azurite initialization
├── functions/                      # Function apps
│   ├── my-function/
│   │   ├── function_app.py        # v2 model
│   │   ├── host.json
│   │   ├── requirements.txt
│   │   └── local.settings.json
│   └── another-function/
│       └── ...
├── Tiltfile                        # Tilt orchestration
├── .env.local                      # Local secrets (gitignored)
├── .funcignore                     # Functions deployment ignore
└── README.md
```

---

## local.settings.json Template

Each function app should have a `local.settings.json`:

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=YOUR_KEY;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;TableEndpoint=http://127.0.0.1:10002/devstoreaccount1",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AZURE_STORAGE_CONNECTION_STRING": "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=YOUR_KEY;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;TableEndpoint=http://127.0.0.1:10002/devstoreaccount1"
  },
  "Host": {
    "LocalHttpPort": 7071,
    "CORS": "*",
    "CORSCredentials": false
  }
}
```

**Note**: This is for local testing **outside** Docker. When running in Docker via Tilt, environment variables come from docker-compose.yml.

---

## Development Workflow

### 1. Start Development Environment

```bash
# Start all services
tilt up

# Start specific services only
tilt up my-function azurite
```

Tilt will:
- Build Docker images
- Start containers
- Set up live reload
- Display logs in UI

### 2. Access Tilt UI

```bash
# Opens in browser
open http://localhost:10350
```

UI shows:
- Service status (green = healthy, red = error)
- Real-time logs
- Build progress
- Resource dependencies

### 3. Make Code Changes

When you edit code, Tilt automatically:
1. Syncs changed files to container
2. Reinstalls dependencies (if needed)
3. Restarts container
4. Shows updated logs

**Live reload** is near-instant for code changes.

### 4. Test Functions

```bash
# HTTP Trigger example
curl -X POST http://localhost:7071/api/my-function \
  -H "Content-Type: application/json" \
  -d '{"name": "test"}'
```

### 5. Access Azurite Storage

**Using Azure Storage Explorer**:
- Connect to local emulator
- Connection string: (from local.settings.json)

**Using Azure CLI**:
```bash
# List blobs in container
az storage blob list \
  --container-name mycontainer \
  --connection-string "DefaultEndpointsProtocol=http;..."
```

### 6. View Logs

- **Tilt UI**: Real-time logs for all services
- **Function logs**: Visible in Tilt under function service
- **Azurite logs**: Debug logs in /data/debug.log

### 7. Stop Environment

```bash
# Stop all services
tilt down

# Or Ctrl+C in terminal
```

---

## Common Issues and Solutions

### Issue: Azurite not ready when function starts

**Solution**: Use resource_deps in Tiltfile:
```python
dc_resource(name='my-function',
    resource_deps=['azurite', 'init-azurite']
)
```

### Issue: Connection refused to Azurite

**Solution**: Check docker-compose network configuration:
- Functions should use `http://azurite:10000` (service name)
- Host should use `http://127.0.0.1:10000` or `http://localhost:10000`

### Issue: Live reload not working

**Solution**: Check live_update configuration in Tiltfile:
- Ensure sync() paths are correct
- Add restart_container() at end of live_update

### Issue: Environment variables not loading

**Solution**:
- Check docker-compose.yml environment section
- Verify .env.local file exists and is loaded by Tilt
- Use `${VAR_NAME}` syntax in docker-compose.yml

---

## Best Practices

1. **Use .env.local for secrets**: Never commit secrets to git
2. **Pin dependency versions**: Ensure consistent builds
3. **Use resource dependencies**: Ensure services start in correct order
4. **Configure live_update**: For fast development iteration
5. **Use labels in Tilt**: Group related services
6. **Test with Azurite first**: Before deploying to Azure
7. **Clean up Azurite data periodically**: Delete docker volumes

---

## Debugging

### Debug in VS Code

1. Install Azure Functions extension
2. Set breakpoints in code
3. Attach to Python process in container:

**.vscode/launch.json**:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Attach to Azure Functions",
      "type": "python",
      "request": "attach",
      "port": 9091,
      "host": "localhost",
      "pathMappings": [
        {
          "localRoot": "${workspaceFolder}/functions/my-function",
          "remoteRoot": "/home/site/wwwroot"
        }
      ]
    }
  ]
}
```

4. Add debugpy to requirements.txt
5. Start debugpy in function code

---

## Performance Tips

1. **Use .dockerignore**: Reduce build context size
2. **Multi-stage builds**: Separate build and runtime dependencies
3. **Cache Poetry/pip installs**: Use Docker layer caching
4. **Minimize live_update triggers**: Only sync necessary files
5. **Use ignore patterns**: Exclude .venv, __pycache__, tests from Tilt builds

---

## Official Documentation

- [Azure Functions Local Development](https://learn.microsoft.com/azure/azure-functions/functions-develop-local)
- [Azurite Storage Emulator](https://learn.microsoft.com/azure/storage/common/storage-use-azurite)
- [Tilt Quick Start](https://docs.tilt.dev/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
