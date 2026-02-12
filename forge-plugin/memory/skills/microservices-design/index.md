# microservices-design Memory

Project-specific memory for microservice architectures, service boundaries, communication patterns, and operational concerns.

## Purpose

This memory helps the `skill:microservices-design` remember:
- Service catalog and boundaries
- Data ownership and consistency patterns
- Communication patterns (sync/async) between services
- Saga definitions and compensating actions
- Operational stack decisions (gateway, mesh, observability)
- Architecture Decision Records

## Memory Files Per Project

Each project gets its own directory: `{project-name}/`

### Required Files

#### `project_overview.md`

**Purpose**: High-level system context and constraints

**Must contain**:
- **System scope**: What the distributed system does
- **Team structure**: Teams, ownership, size
- **Infrastructure**: Kubernetes, cloud provider, CI/CD maturity
- **Key constraints**: Consistency requirements, compliance, latency targets
- **Scale parameters**: Request rates, data volumes, geographic distribution

**When to update**: First invocation, team restructuring, infrastructure changes

#### `service_catalog.md`

**Purpose**: Complete inventory of all services and their relationships

**Must contain**:
- **Service inventory**: Name, domain, team, data store, scaling profile
- **Communication map**: Which services talk to which, sync vs async
- **Data ownership**: Which service owns which entities
- **Saga definitions**: Distributed workflow steps and compensating actions
- **Event catalog**: Domain events published and consumed by each service

**When to update**: After each design session, new services added, communication patterns changed

### Optional Files

#### `operational_runbook.md`

**Purpose**: Gateway, mesh, observability, and resilience configuration

#### `architecture_decisions.md`

**Purpose**: ADRs for key microservices decisions

---

## Usage in skill:microservices-design

### Loading Memory (Step 2)

```markdown
project_name = detect_project_name()
memory = memoryStore.getSkillMemory("microservices-design", project_name)

if memory exists:
    # Honor existing service boundaries
    # Ensure new services follow established patterns
    # Reference existing saga definitions
```

### Updating Memory (Step 9)

```markdown
# First design session
if not exists(memory_path):
    create project_overview.md with system context and constraints
    create service_catalog.md with service inventory and interactions

# Subsequent sessions
else:
    update service_catalog.md with new services or changed boundaries
    update architecture_decisions.md with new ADRs
```

---

## Related Documentation

- **Skill Definition**: `../../skills/microservices-design/SKILL.md`
- **Context Files**: `../../context/engineering/`
- **Memory Index**: `../index.md`
