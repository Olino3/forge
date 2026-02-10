# generate-tilt-dev-environment Memory

## Purpose

Remember project-specific Tilt development environment configurations, service definitions, and customizations for efficient environment updates and maintenance.

## Directory Structure

```
generate-tilt-dev-environment/{project-name}/
├── environment_config.md    # Core environment configuration
├── services.md              # Service definitions and ports
├── customizations.md        # User-specific deviations
└── setup_notes.md           # Operational knowledge
```

## Required Memory Files

### `environment_config.md` (ALWAYS CREATE)

- Services included (application, database, cache, queue, mock services)
- Port mappings and networking configuration
- Volume mounts and persistent storage
- Environment variable sources and templates
- Live reload configuration per service
- Build tool and dependency management approach
- Generation timestamp and skill version

**Example snippet**:
```markdown
<!-- Last Updated: 2026-02-10 -->
# Environment Configuration - my-app

## Services
- **app** (Python/FastAPI): Port 8000, live reload via Tilt
- **postgres**: Port 5432, persistent volume
- **redis**: Port 6379, ephemeral
- **mock-payment**: Port 9000, WireMock

## Build
- Dependency Manager: Poetry
- Docker Base: python:3.11-slim
- Live Reload: sync local files → container
```

### `services.md` (COMPREHENSIVE LIST)

- All services with ports, health checks, dependencies
- Resource dependencies (which services depend on which)
- Startup order and readiness probes
- Docker image sources and build contexts

### `customizations.md` (USER-SPECIFIC)

- Non-standard configurations and reasons
- Custom Tiltfile extensions
- Additional Docker Compose services
- Special networking or volume requirements

### `setup_notes.md` (OPERATIONAL)

- First-time setup instructions and prerequisites
- Known issues and workarounds
- Performance tuning recommendations
- Troubleshooting common problems

## Why This Skill Needs Memory

- **Configuration reuse**: Remember service configurations for updates
- **Avoid regeneration**: Know what was already generated
- **Track customizations**: Document non-standard choices
- **Operational knowledge**: Store setup issues and solutions

## Memory Growth Pattern

**First generation**: Baseline environment config, all services, initial setup notes
**Subsequent operations**: New services added, customizations tracked, issues documented

---

*Last Updated: 2026-02-10*
