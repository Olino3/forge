---
id: "azure/azure_functions_overview"
domain: azure
title: "Azure Functions Overview"
type: reference
estimatedTokens: 1350
loadingStrategy: onDemand
version: "0.2.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "Programming Models Comparison"
    estimatedTokens: 149
    keywords: [programming, models, comparison]
  - name: "Quick Comparison Table"
    estimatedTokens: 56
    keywords: [quick, comparison, table]
  - name: "Common Triggers and Bindings"
    estimatedTokens: 54
    keywords: [triggers, bindings]
  - name: "host.json Configuration"
    estimatedTokens: 27
    keywords: [hostjson, configuration]
  - name: "Azure Functions CLI Commands"
    estimatedTokens: 51
    keywords: [azure, functions, cli, commands]
  - name: "Migration from v1 to v2"
    estimatedTokens: 60
    keywords: [migration]
  - name: "Detection Patterns"
    estimatedTokens: 31
    keywords: [detection, patterns]
  - name: "Best Practices"
    estimatedTokens: 42
    keywords: [best]
  - name: "Example .funcignore"
    estimatedTokens: 10
    keywords: [example, funcignore]
  - name: "Official Documentation"
    estimatedTokens: 14
    keywords: [official, documentation]
tags: [azure, functions, serverless, python, triggers, bindings, v1, v2]
---

# Azure Functions Overview

## Programming Models Comparison

### v1 Programming Model (Legacy)

**Structure**:
```
functions/
├── my-function/
│   ├── __init__.py         # Function code
│   └── function.json       # Bindings configuration
├── another-function/
│   ├── __init__.py
│   └── function.json
└── host.json               # Global configuration
```

**Example function.json** (HTTP Trigger):
```json
{
  "scriptFile": "__init__.py",
  "bindings": [
    {
      "authLevel": "anonymous",
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

**Example __init__.py**:
```python
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    name = req.params.get('name')
    return func.HttpResponse(f"Hello, {name}!")
```

**When to use**:
- Migrating from existing v1 projects
- Need explicit control over binding configuration
- Working with older Azure Functions runtime (<4.0)

---

### v2 Programming Model (Modern, Recommended)

**Structure**:
```
functions/
├── function_app.py         # All functions defined here
├── host.json
└── requirements.txt
```

**Example function_app.py**:
```python
import azure.functions as func
import logging

app = func.FunctionApp()

@app.function_name(name="HttpTriggerExample")
@app.route(route="hello", auth_level=func.AuthLevel.ANONYMOUS)
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    name = req.params.get('name')
    return func.HttpResponse(f"Hello, {name}!")

@app.function_name(name="BlobTriggerExample")
@app.blob_trigger(arg_name="myblob", path="samples/{name}",
                  connection="AzureWebJobsStorage")
def blob_trigger(myblob: func.InputStream):
    logging.info(f"Blob name: {myblob.name}, Size: {myblob.length} bytes")
```

**When to use**:
- New projects (recommended)
- Want cleaner, more Pythonic code
- Prefer decorator-based configuration
- Using Azure Functions runtime 4.x+

---

## Quick Comparison Table

| Feature | v1 | v2 |
|---------|----|----|
| **Configuration** | function.json files | Python decorators |
| **File Structure** | One directory per function | Single function_app.py |
| **Bindings** | JSON configuration | Decorators |
| **Runtime Required** | 2.x, 3.x, 4.x | 4.x only |
| **Code Style** | Imperative | Declarative/Pythonic |
| **Maintenance** | More files to manage | Centralized |
| **Recommended** | No (legacy) | Yes |

---

## Common Triggers and Bindings

### HTTP Trigger
```python
# v2 example
@app.route(route="api/users", methods=["GET", "POST"])
def users_api(req: func.HttpRequest) -> func.HttpResponse:
    pass
```

### Timer Trigger
```python
# v2 example - runs every 5 minutes
@app.schedule(schedule="0 */5 * * * *", arg_name="timer")
def timer_function(timer: func.TimerRequest):
    pass
```

### Blob Trigger
```python
# v2 example
@app.blob_trigger(arg_name="blob", path="container/{name}",
                  connection="AzureWebJobsStorage")
def process_blob(blob: func.InputStream):
    pass
```

### Queue Trigger
```python
# v2 example
@app.queue_trigger(arg_name="msg", queue_name="myqueue",
                   connection="AzureWebJobsStorage")
def process_queue(msg: func.QueueMessage):
    pass
```

---

## host.json Configuration

**Common configuration** (works for both v1 and v2):
```json
{
  "version": "2.0",
  "logging": {
    "applicationInsights": {
      "samplingSettings": {
        "isEnabled": true,
        "maxTelemetryItemsPerSecond": 20
      }
    }
  },
  "extensionBundle": {
    "id": "Microsoft.Azure.Functions.ExtensionBundle",
    "version": "[4.*, 5.0.0)"
  }
}
```

---

## Azure Functions CLI Commands

### Create Function App (v1)
```bash
func init my-function-app --python --model v1
cd my-function-app
func new --name HttpTrigger --template "HTTP trigger" --authlevel anonymous
```

### Create Function App (v2)
```bash
func init my-function-app --python --model v2
cd my-function-app
# Functions added directly in function_app.py
```

### Add New Function (v1 only)
```bash
func new --name MyNewFunction --template "HTTP trigger"
```

### Run Locally
```bash
func start
```

---

## Migration from v1 to v2

**Steps**:
1. Create new `function_app.py`
2. Convert function.json bindings to decorators
3. Move function code from `__init__.py` to decorated functions
4. Update `host.json` if needed
5. Test thoroughly

**Example v1 to v2 conversion**:

**Before (v1)** - `my-function/function.json`:
```json
{
  "bindings": [
    {"type": "httpTrigger", "direction": "in", "name": "req"},
    {"type": "http", "direction": "out", "name": "$return"}
  ]
}
```

**Before (v1)** - `my-function/__init__.py`:
```python
def main(req):
    return func.HttpResponse("Hello")
```

**After (v2)** - `function_app.py`:
```python
@app.route(route="my-function")
def my_function(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("Hello")
```

---

## Detection Patterns

### Detect v1 Project
- Has `function.json` files in function directories
- Each function in separate directory
- `scriptFile` field in function.json

### Detect v2 Project
- Has `function_app.py` in root
- Uses decorators (@app.route, @app.schedule, etc.)
- No function.json files

---

## Best Practices

1. **Use v2 for new projects** - Modern, cleaner syntax
2. **Keep host.json minimal** - Use defaults when possible
3. **Use environment variables** - For connection strings and secrets
4. **Enable Application Insights** - For production monitoring
5. **Use .funcignore** - To exclude unnecessary files from deployment
6. **Pin dependency versions** - In requirements.txt or pyproject.toml

---

## Example .funcignore

```
.git
.venv
__pycache__
*.pyc
.python_version
.env
.vscode
local.settings.json
tests/
.coverage
.pytest_cache
```

---

## Official Documentation

- [Azure Functions Python Developer Guide](https://learn.microsoft.com/azure/azure-functions/functions-reference-python)
- [v2 Programming Model](https://learn.microsoft.com/azure/azure-functions/functions-reference-python?tabs=asgi%2Capplication-level)
- [Triggers and Bindings](https://learn.microsoft.com/azure/azure-functions/functions-triggers-bindings)
- [Azure Functions CLI Reference](https://learn.microsoft.com/azure/azure-functions/functions-core-tools-reference)
