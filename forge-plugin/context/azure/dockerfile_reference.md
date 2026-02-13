---
id: "azure/dockerfile_reference"
domain: azure
title: "Dockerfile Reference for Azure Functions"
type: reference
estimatedTokens: 2200
loadingStrategy: onDemand
version: "0.3.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "Base Images"
    estimatedTokens: 54
    keywords: [base, images]
  - name: "Complete Python Dockerfile (with pip)"
    estimatedTokens: 53
    keywords: [complete, python, dockerfile, pip]
  - name: "Complete Python Dockerfile (with Poetry)"
    estimatedTokens: 78
    keywords: [complete, python, dockerfile, poetry]
  - name: "Python Dockerfile with Local Package"
    estimatedTokens: 111
    keywords: [python, dockerfile, local, package]
  - name: "Node.js Dockerfile (with npm)"
    estimatedTokens: 32
    keywords: [nodejs, dockerfile, npm]
  - name: ".NET Dockerfile"
    estimatedTokens: 48
    keywords: [net, dockerfile]
  - name: "Dockerfile Optimization Patterns"
    estimatedTokens: 86
    keywords: [dockerfile, optimization, patterns]
  - name: "Additional Tools Installation"
    estimatedTokens: 78
    keywords: [additional, tools, installation]
  - name: "Environment Variables"
    estimatedTokens: 41
    keywords: [environment, variables]
  - name: "Best Practices"
    estimatedTokens: 122
    keywords: [best]
  - name: "Debugging Dockerfiles"
    estimatedTokens: 60
    keywords: [debugging, dockerfiles]
  - name: "Common Issues"
    estimatedTokens: 60
    keywords: [issues]
  - name: "Official Documentation"
    estimatedTokens: 10
    keywords: [official, documentation]
tags: [azure, dockerfile, docker, python, poetry, multi-stage, functions]
---

# Dockerfile Reference for Azure Functions

## Base Images

### Python Functions

```dockerfile
# Azure Functions v4 with Python 3.11
FROM mcr.microsoft.com/azure-functions/python:4-python3.11

# Other available versions
# FROM mcr.microsoft.com/azure-functions/python:4-python3.9
# FROM mcr.microsoft.com/azure-functions/python:4-python3.10
```

### Node.js Functions

```dockerfile
# Azure Functions v4 with Node.js 18
FROM mcr.microsoft.com/azure-functions/node:4-node18

# Other available versions
# FROM mcr.microsoft.com/azure-functions/node:4-node16
# FROM mcr.microsoft.com/azure-functions/node:4-node20
```

### .NET Functions

```dockerfile
# Azure Functions v4 with .NET 6
FROM mcr.microsoft.com/azure-functions/dotnet:4

# Isolated worker process
# FROM mcr.microsoft.com/azure-functions/dotnet-isolated:4-dotnet-isolated6.0
```

**Official registry**: `mcr.microsoft.com/azure-functions/`

---

## Complete Python Dockerfile (with pip)

```dockerfile
FROM mcr.microsoft.com/azure-functions/python:4-python3.11

# Create and set working directory
RUN mkdir -p /home/site/wwwroot && chmod -R 755 /home/site/wwwroot
WORKDIR /home/site/wwwroot

# Set Azure Functions environment variables
ENV AzureWebJobsScriptRoot=/home/site/wwwroot
ENV AzureFunctionsJobHost__Logging__Console__IsEnabled=true
ENV PYTHONPATH=/home/site/wwwroot

# Copy requirements file
COPY functions/my-function/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy function code
COPY functions/my-function/ .

# Expose port (Azure Functions listens on port 80 in container)
EXPOSE 80
```

---

## Complete Python Dockerfile (with Poetry)

```dockerfile
FROM mcr.microsoft.com/azure-functions/python:4-python3.11

# Create working directory
RUN mkdir -p /home/site/wwwroot && chmod -R 755 /home/site/wwwroot
WORKDIR /home/site/wwwroot

# Environment variables
ENV AzureWebJobsScriptRoot=/home/site/wwwroot
ENV AzureFunctionsJobHost__Logging__Console__IsEnabled=true
ENV PYTHONPATH=/home/site/wwwroot
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

# Install Poetry in separate virtual environment
RUN python -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry poetry-plugin-export

# Add poetry to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

# Copy poetry files
COPY functions/my-function/pyproject.toml functions/my-function/poetry.lock* ./

# Export requirements and install dependencies
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes \
    && pip install --no-cache-dir -r requirements.txt

# Copy function code
COPY functions/my-function/ .

EXPOSE 80
```

---

## Python Dockerfile with Local Package

**Scenario**: Function depends on a local shared package.

```dockerfile
FROM mcr.microsoft.com/azure-functions/python:4-python3.11

RUN mkdir -p /home/site/wwwroot && chmod -R 755 /home/site/wwwroot
WORKDIR /home/site/wwwroot

ENV AzureWebJobsScriptRoot=/home/site/wwwroot
ENV AzureFunctionsJobHost__Logging__Console__IsEnabled=true
ENV PYTHONPATH=/home/site/wwwroot
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

# Install Poetry
RUN python -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry poetry-plugin-export

ENV PATH="${PATH}:${POETRY_VENV}/bin"

# Build local package first
WORKDIR /tmp/my-shared-package
COPY my-shared-package/pyproject.toml my-shared-package/poetry.lock* ./
COPY my-shared-package/README.md ./
COPY my-shared-package/src ./src

# Build wheel
RUN poetry build

# Switch to function directory
WORKDIR /home/site/wwwroot

# Create dist directory and copy wheel
RUN mkdir -p ./dist
RUN cp /tmp/my-shared-package/dist/*.whl ./dist/

# Copy function dependencies
COPY functions/my-function/pyproject.toml functions/my-function/poetry.lock* ./

# Export and install (including local wheel)
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir ./dist/*.whl

# Copy function code
COPY functions/my-function/ .

EXPOSE 80
```

---

## Node.js Dockerfile (with npm)

```dockerfile
FROM mcr.microsoft.com/azure-functions/node:4-node18

# Create working directory
RUN mkdir -p /home/site/wwwroot
WORKDIR /home/site/wwwroot

# Environment variables
ENV AzureWebJobsScriptRoot=/home/site/wwwroot

# Copy package files
COPY functions/my-function/package*.json ./

# Install dependencies
RUN npm ci --production

# Copy function code
COPY functions/my-function/ .

EXPOSE 80
```

---

## .NET Dockerfile

```dockerfile
FROM mcr.microsoft.com/azure-functions/dotnet:4 AS build

WORKDIR /src

# Copy csproj and restore dependencies
COPY functions/my-function/*.csproj ./
RUN dotnet restore

# Copy source and build
COPY functions/my-function/ ./
RUN dotnet build -c Release -o /app/build

# Publish
FROM build AS publish
RUN dotnet publish -c Release -o /app/publish

# Final stage
FROM mcr.microsoft.com/azure-functions/dotnet:4
WORKDIR /home/site/wwwroot
COPY --from=publish /app/publish .

ENV AzureWebJobsScriptRoot=/home/site/wwwroot

EXPOSE 80
```

---

## Dockerfile Optimization Patterns

### Multi-Stage Build (Python)

```dockerfile
# Stage 1: Build dependencies
FROM mcr.microsoft.com/azure-functions/python:4-python3.11 AS builder

WORKDIR /build
COPY functions/my-function/requirements.txt .
RUN pip install --no-cache-dir --target=/build/packages -r requirements.txt

# Stage 2: Runtime
FROM mcr.microsoft.com/azure-functions/python:4-python3.11

WORKDIR /home/site/wwwroot
ENV AzureWebJobsScriptRoot=/home/site/wwwroot
ENV PYTHONPATH=/home/site/wwwroot

# Copy installed packages from builder
COPY --from=builder /build/packages /home/site/wwwroot/.python_packages/lib/site-packages

# Copy function code
COPY functions/my-function/ .

EXPOSE 80
```

**Benefits**: Smaller final image, faster rebuilds.

### Layer Caching

```dockerfile
FROM mcr.microsoft.com/azure-functions/python:4-python3.11

WORKDIR /home/site/wwwroot
ENV AzureWebJobsScriptRoot=/home/site/wwwroot

# Copy and install dependencies FIRST (cached layer)
COPY functions/my-function/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code LAST (changes frequently)
COPY functions/my-function/ .

EXPOSE 80
```

**Principle**: Copy files in order from least to most frequently changed.

---

## Additional Tools Installation

### Install Azure CLI

```dockerfile
FROM mcr.microsoft.com/azure-functions/python:4-python3.11

# ... other setup ...

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    apt-transport-https \
    lsb-release \
    gpg \
    && rm -rf /var/lib/apt/lists/*

# Install Azure CLI
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash

# ... continue with function setup ...
```

### Install System Packages

```dockerfile
FROM mcr.microsoft.com/azure-functions/python:4-python3.11

# Install required system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# ... rest of Dockerfile ...
```

**Important**: Always clean up with `rm -rf /var/lib/apt/lists/*` to reduce image size.

---

## Environment Variables

### Required Variables

```dockerfile
ENV AzureWebJobsScriptRoot=/home/site/wwwroot
ENV AzureFunctionsJobHost__Logging__Console__IsEnabled=true
```

**AzureWebJobsScriptRoot**: Root directory for function code
**AzureFunctionsJobHost__Logging__Console__IsEnabled**: Enable console logging

### Python-Specific

```dockerfile
ENV PYTHONPATH=/home/site/wwwroot
ENV PYTHONUNBUFFERED=1
```

**PYTHONPATH**: Python module search path
**PYTHONUNBUFFERED**: Disable output buffering (better for Docker logs)

### Optional

```dockerfile
ENV FUNCTIONS_WORKER_RUNTIME=python
ENV WEBSITE_HOSTNAME=localhost:7071
```

Usually set in docker-compose.yml, not Dockerfile.

---

## Best Practices

### 1. Use Specific Base Image Tags

```dockerfile
# Good: Specific version
FROM mcr.microsoft.com/azure-functions/python:4-python3.11

# Avoid: Latest tag
# FROM mcr.microsoft.com/azure-functions/python:latest
```

### 2. Minimize Layers

```dockerfile
# Good: Single RUN command
RUN apt-get update && apt-get install -y \
    package1 \
    package2 \
    && rm -rf /var/lib/apt/lists/*

# Avoid: Multiple RUN commands
# RUN apt-get update
# RUN apt-get install -y package1
# RUN apt-get install -y package2
```

### 3. Use .dockerignore

Create `.dockerignore` in build context:
```
.git
.venv
__pycache__
*.pyc
.pytest_cache
.coverage
tests/
*.md
.env
local.settings.json
```

### 4. Don't Run as Root (Advanced)

```dockerfile
FROM mcr.microsoft.com/azure-functions/python:4-python3.11

# Create non-root user
RUN useradd -m -u 1000 funcuser && \
    chown -R funcuser:funcuser /home/site/wwwroot

USER funcuser

# ... rest of setup ...
```

**Note**: Azure Functions images usually handle this, but good practice for security.

### 5. Pin Dependency Versions

**requirements.txt**:
```
azure-functions==1.18.0
requests==2.31.0
pydantic==2.5.0
```

**pyproject.toml**:
```toml
[tool.poetry.dependencies]
python = "^3.11"
azure-functions = "1.18.0"
requests = "2.31.0"
```

---

## Debugging Dockerfiles

### Add Debug Tools

```dockerfile
FROM mcr.microsoft.com/azure-functions/python:4-python3.11

# Install debugging tools
RUN apt-get update && apt-get install -y \
    curl \
    vim \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Enable debugpy for remote debugging
RUN pip install debugpy

# ... rest of setup ...
```

### Test Build Locally

```bash
# Build image
docker build -f .docker/my-function/Dockerfile -t my-function-dev .

# Run container
docker run -p 7071:80 \
  -e AzureWebJobsStorage="UseDevelopmentStorage=true" \
  my-function-dev

# Test endpoint
curl http://localhost:7071/api/my-function
```

---

## Common Issues

### Issue: pip install fails

**Cause**: Missing system dependencies.

**Solution**: Install build tools:
```dockerfile
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*
```

### Issue: Module not found

**Cause**: PYTHONPATH not set or packages not in correct location.

**Solution**:
```dockerfile
ENV PYTHONPATH=/home/site/wwwroot
```

### Issue: Slow builds

**Cause**: Poor layer caching, large build context.

**Solution**:
1. Order Dockerfile commands from least to most changing
2. Use .dockerignore
3. Use multi-stage builds

---

## Official Documentation

- [Azure Functions Docker Images](https://hub.docker.com/_/microsoft-azure-functions)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Azure Functions on Linux](https://learn.microsoft.com/azure/azure-functions/functions-create-function-linux-custom-image)
