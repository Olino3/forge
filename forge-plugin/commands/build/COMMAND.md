---
name: build
description: "Project building, compilation, and packaging with intelligent error handling"
category: utility
complexity: enhanced
skills: [generate-tilt-dev-environment]
context: [azure, commands/build_patterns]
---

# /build - Project Building and Packaging

## Triggers
- Project compilation and packaging requests
- Build error debugging and resolution
- Environment-specific build configuration (dev/prod/test)
- Docker image building and optimization

## Usage
```
/build [target] [--type dev|prod|test] [--clean] [--verbose]
```

**Parameters**:
- `target`: Project, service, or component to build (default: entire project)
- `--type`: Build environment configuration (default: dev)
- `--clean`: Clean build artifacts before building
- `--verbose`: Show detailed build output

## Workflow

### Step 1: Analyze Build System

1. Detect build system from project files:
   - `package.json` → npm/yarn/pnpm
   - `pyproject.toml` / `setup.py` → Poetry/pip/setuptools
   - `*.csproj` → dotnet CLI
   - `Makefile` → Make
   - `Dockerfile` → Docker
   - `docker-compose.yml` → Docker Compose
   - `Tiltfile` → Tilt (local development)
   - `go.mod` → Go modules
   - `Cargo.toml` → Cargo
2. Identify build configuration (scripts, commands, targets)
3. Check for environment-specific configurations

### Step 2: Load Context & Memory

**Context Loading** (index-first approach):
1. Read `../../context/commands/index.md` for command guidance
2. Load `../../context/commands/build_patterns.md` for build strategies
3. If Docker/container build: Load `../../context/azure/dockerfile_reference.md`
4. If Tilt-based: Load `../../context/azure/tiltfile_reference.md`
5. If Docker Compose: Load `../../context/azure/docker_compose_reference.md`

**Memory Loading**:
1. Determine project name
2. Check `../../memory/commands/{project}/build_config.md` for build history
3. Load known build issues and workarounds

### Step 3: Validate Environment

1. Check required build tools are available
2. Verify dependency files exist (lock files, manifest files)
3. If `--clean`: Remove build artifacts and caches
4. Validate environment variables for `--type` configuration

### Step 4: Execute Build

1. Run the appropriate build command:
   - **npm**: `npm run build` / `npm run build:prod`
   - **Poetry**: `poetry build` / `poetry install`
   - **dotnet**: `dotnet build` / `dotnet publish -c Release`
   - **Docker**: `docker build -t {name} .`
   - **Docker Compose**: `docker compose build [service]`
   - **Tilt**: `tilt up [--stream]`
   - **Make**: `make build` / `make {target}`
2. Monitor build output for errors and warnings
3. Capture build timing and artifact information

### Step 5: Handle Build Errors

If build fails:
1. Parse error message and identify failure point
2. Categorize error:
   - **Dependency**: Missing or conflicting packages → suggest resolution
   - **Compilation**: Syntax or type errors → identify file and line
   - **Configuration**: Missing config or env vars → identify what's needed
   - **Resource**: Memory, disk, or network → suggest workarounds
3. Check memory for known build issues
4. Provide actionable fix recommendation

### Step 6: Generate Output & Update Memory

**Output**:
Save results to `/claudedocs/build_report_{date}.md`:

```markdown
# Build Report - {Project}
**Date**: {date}
**Command**: /build {full invocation}
**Build System**: {detected system}
**Type**: {dev|prod|test}

## Result
**Status**: {success|failure}
**Duration**: {time}

## Build Details
- **Command Executed**: {actual command}
- **Artifacts Generated**: {list}
- **Warnings**: {count}

## Errors (if any)
### {Error 1}
- **Step**: {build step}
- **Message**: {error message}
- **Resolution**: {suggested fix}

## Artifact Summary
| Artifact | Size | Type |
|----------|------|------|
| {name} | {size} | {type} |

## Next Steps
- {recommendations}
```

**Memory Updates**:
1. Append to `../../memory/commands/{project}/command_history.md`
2. Update `../../memory/commands/{project}/build_config.md`:
   - Build system, commands used, common errors, timing benchmarks

## Tool Coordination
- **Bash**: Build system execution and process management
- **Read**: Configuration analysis and manifest inspection
- **Grep**: Error parsing and build log analysis
- **Glob**: Artifact discovery and validation
- **Write**: Build reports

## Key Patterns
- **System Detection**: Config files → appropriate build command
- **Error Recovery**: Build failure → diagnostic analysis → resolution guidance
- **Environment Awareness**: dev/prod/test → appropriate configuration
- **Memory Learning**: Track build times, common errors, successful configurations

## Skill Integration

For local development environment builds:
- **Tilt environments**: `skill:generate-tilt-dev-environment` for Tilt + Docker setup
- **Azure Functions**: `skill:generate-azure-functions` for local dev with Azurite

## Boundaries

**Will:**
- Execute project build systems using existing configurations
- Provide comprehensive error analysis and resolution guidance
- Generate build reports with timing and artifact details
- Track build history and learn from past failures

**Will Not:**
- Modify build system configuration without user approval
- Install missing build tools or dependencies automatically
- Execute deployment operations beyond artifact preparation
- Run builds that require credentials or external services without setup

**Output**: Build report saved to `/claudedocs/build_report_{date}.md`

**Next Step**: If build succeeds, use `/test` to validate. If build fails, apply suggested fixes.
