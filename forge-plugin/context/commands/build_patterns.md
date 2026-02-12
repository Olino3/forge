---
id: "commands/build_patterns"
domain: commands
title: "Build Patterns"
type: pattern
estimatedTokens: 950
loadingStrategy: onDemand
version: "0.2.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "Build System Detection"
    estimatedTokens: 108
    keywords: [build, system, detection]
  - name: "Build Types"
    estimatedTokens: 54
    keywords: [build, types]
  - name: "Docker Build Patterns"
    estimatedTokens: 102
    keywords: [docker, build, patterns]
  - name: "Build Caching Strategies"
    estimatedTokens: 82
    keywords: [build, caching, strategies]
  - name: "Build Error Handling"
    estimatedTokens: 102
    keywords: [build, error, handling]
  - name: "Artifact Optimization"
    estimatedTokens: 49
    keywords: [artifact, optimization]
  - name: "Skill Integration"
    estimatedTokens: 14
    keywords: [skill, integration]
  - name: "Official References"
    estimatedTokens: 20
    keywords: [official, references]
tags: [commands, build, docker, caching, artifacts, multi-stage, ci]
---

# Build Patterns

Reference patterns for the `/build` command. Covers build system detection, Docker builds, caching strategies, and artifact optimization.

## Build System Detection

| Indicator | Build System | Language | Build Command |
|-----------|-------------|----------|---------------|
| `package.json` | npm/yarn/pnpm | JavaScript/TypeScript | `npm run build` |
| `pyproject.toml` | Poetry/pip | Python | `poetry build` / `pip install -e .` |
| `setup.py` | setuptools | Python | `python setup.py build` |
| `*.csproj` | dotnet CLI | C#/.NET | `dotnet build` |
| `Makefile` | Make | Any | `make build` |
| `Dockerfile` | Docker | Any | `docker build .` |
| `docker-compose.yml` | Docker Compose | Any | `docker compose build` |
| `Tiltfile` | Tilt | Any | `tilt up` |
| `go.mod` | Go modules | Go | `go build ./...` |
| `Cargo.toml` | Cargo | Rust | `cargo build` |
| `pom.xml` | Maven | Java | `mvn package` |
| `build.gradle` | Gradle | Java/Kotlin | `./gradlew build` |

## Build Types

### Development Build
- Optimized for speed and debugging
- Source maps enabled
- Hot reload / watch mode
- Minimal optimization
- Verbose logging

### Production Build
- Optimized for size and performance
- Minification and tree-shaking
- No source maps (or separate)
- Environment variable injection
- Asset optimization (images, fonts)

### Test Build
- Optimized for test execution
- Coverage instrumentation
- Mock service configuration
- Test database setup

## Docker Build Patterns

### Multi-Stage Builds
```dockerfile
# Stage 1: Build
FROM node:20-slim AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:20-slim
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/index.js"]
```

**Benefits**: Smaller final image, build tools not in production, layer caching

### Python Docker Build
```dockerfile
FROM python:3.11-slim AS builder
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-dev

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /app/.venv ./.venv
COPY . .
CMD [".venv/bin/python", "-m", "app"]
```

### .NET Docker Build
```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY *.csproj ./
RUN dotnet restore
COPY . .
RUN dotnet publish -c Release -o /app

FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=build /app .
ENTRYPOINT ["dotnet", "MyApp.dll"]
```

## Build Caching Strategies

### Layer Caching (Docker)
- Copy dependency files first (`package.json`, `requirements.txt`)
- Install dependencies (cached if lock file unchanged)
- Copy source code last (changes frequently)

### Dependency Caching (CI)
| System | Cache Key | Cache Path |
|--------|-----------|------------|
| npm | `package-lock.json` hash | `~/.npm` or `node_modules` |
| pip | `requirements.txt` hash | `~/.cache/pip` |
| Poetry | `poetry.lock` hash | `~/.cache/pypoetry` |
| NuGet | `*.csproj` hash | `~/.nuget/packages` |
| Go | `go.sum` hash | `~/go/pkg/mod` |

### Build Output Caching
- **Incremental builds**: Only rebuild changed modules
- **Remote caching**: Share build cache across CI runners
- **Artifact caching**: Reuse build outputs across pipelines

## Build Error Handling

### Common Build Failures
| Error Type | Likely Cause | Resolution |
|-----------|-------------|------------|
| Dependency resolution | Version conflict | Check lock file, update dependencies |
| Compilation error | Syntax/type error | Fix source code |
| Out of memory | Large project, insufficient resources | Increase memory limit, split build |
| Permission denied | File/directory permissions | Fix ownership, check Docker user |
| Network timeout | Package registry unreachable | Retry, check proxy settings |
| Missing tool | Build tool not installed | Install required toolchain |

### Error Analysis Strategy
1. Read the full error message
2. Identify the failing step (dependency, compile, link, package)
3. Check if error is environment-specific or code-specific
4. Check recent changes that could cause the failure
5. Search for known issues in project memory

## Artifact Optimization

### JavaScript/TypeScript
- Tree-shaking (remove unused exports)
- Code splitting (lazy load routes/features)
- Minification (terser, esbuild)
- Gzip/Brotli compression
- Image optimization

### Python
- Wheel distribution (`.whl`) over source
- Exclude test files from package
- Use `__all__` for explicit exports
- Strip debug symbols from C extensions

### .NET
- Trimming (remove unused assemblies)
- Ready-to-Run (R2R) compilation
- Single-file publish
- Compression

## Skill Integration

For local development builds with containers:
- **Tilt environments**: `skill:generate-tilt-dev-environment`
- **Azure Functions**: `skill:generate-azure-functions` for local dev with Azurite

## Official References

- [Docker Build Documentation](https://docs.docker.com/build/)
- [npm Scripts](https://docs.npmjs.com/cli/v10/using-npm/scripts)
- [Poetry Build](https://python-poetry.org/docs/cli/#build)
- [dotnet build](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-build)
