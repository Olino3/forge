---
id: "azure/tiltfile_reference"
domain: azure
title: "Tiltfile Reference for Azure Functions"
type: reference
estimatedTokens: 2100
loadingStrategy: onDemand
version: "0.1.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "Basic Structure"
    estimatedTokens: 23
    keywords: [basic, structure]
  - name: "Complete Example Tiltfile"
    estimatedTokens: 127
    keywords: [complete, example, tiltfile]
  - name: "Tiltfile Components"
    estimatedTokens: 457
    keywords: [tiltfile, components]
  - name: "Advanced Patterns"
    estimatedTokens: 42
    keywords: [advanced, patterns]
  - name: "Tilt UI Features"
    estimatedTokens: 51
    keywords: [tilt, features]
  - name: "Best Practices"
    estimatedTokens: 47
    keywords: [best]
  - name: "Troubleshooting"
    estimatedTokens: 51
    keywords: [troubleshooting]
  - name: "Official Documentation"
    estimatedTokens: 11
    keywords: [official, documentation]
tags: [azure, tilt, tiltfile, live-update, docker-build, orchestration]
---

# Tiltfile Reference for Azure Functions

## Basic Structure

A Tiltfile for Azure Functions typically includes:
1. Service dependency configuration
2. Environment variable loading
3. Docker Compose integration
4. Docker build configurations
5. Resource definitions
6. Live update rules

---

## Complete Example Tiltfile

```python
# Load environment variables from .env.local
load('ext://dotenv', 'dotenv')
dotenv('.env.local')

# Define service dependencies
RESOURCE_DEPENDENCIES = {
    'my-function': ['azurite', 'init-azurite'],
    'another-function': ['azurite', 'init-azurite'],
    'azurite': [],
    'init-azurite': ['azurite']
}

# Optional: Service selection logic
config.define_string_list('args', args=True)
cfg = config.parse()
requested_services = cfg.get('args', [])

if requested_services:
    # Enable only requested services + dependencies
    enabled = get_all_dependencies(requested_services, RESOURCE_DEPENDENCIES)
    config.set_enabled_resources(enabled)

# Initialize Azurite
local_resource(
    name='init-azurite',
    cmd='echo "Azurite initialization handled by Dockerfile entrypoint"',
    labels=['storage'],
    resource_deps=['azurite']
)

# Load Docker Compose
docker_compose('.docker/docker-compose.dev.yml')

# Build function app image
docker_build(
    ref='my-function-dev',
    context='.',
    dockerfile='.docker/my-function/Dockerfile',
    ignore=['tests', '.git', '.venv', '__pycache__'],
    live_update=[
        # Sync code changes
        sync('./functions/my-function/', '/home/site/wwwroot/'),

        # Reinstall dependencies when requirements change
        run(
            'pip install --no-cache-dir -r requirements.txt',
            trigger=['./functions/my-function/requirements.txt']
        ),

        # Restart container
        restart_container()
    ]
)

# Build Azurite image
docker_build(
    ref='my-azurite',
    context='.',
    dockerfile='.docker/azurite/Dockerfile'
)

# Define resources
dc_resource(
    name='my-function',
    labels=['functions'],
    links=['http://localhost:7071'],
    resource_deps=['azurite', 'init-azurite']
)

dc_resource(
    name='azurite',
    labels=['storage'],
    links=['http://localhost:10000']
)

# Print helpful information
print("""
Development environment ready!

Function Apps:
- my-function: http://localhost:7071/api/{route}

Azurite Storage:
- Blob:  http://localhost:10000
- Queue: http://localhost:10001
- Table: http://localhost:10002

Run: tilt up
""")
```

---

## Tiltfile Components

### 1. Load Extensions

```python
# Load dotenv extension
load('ext://dotenv', 'dotenv')
dotenv('.env.local')  # Load environment variables

# Other useful extensions
load('ext://helm', 'helm')
load('ext://restart_process', 'restart_process')
```

**Common extensions**:
- `dotenv`: Load .env files
- `restart_process`: Restart processes in containers
- `helm`: Kubernetes Helm charts

---

### 2. Service Dependencies

```python
RESOURCE_DEPENDENCIES = {
    'function1': ['azurite', 'init-azurite'],
    'function2': ['azurite', 'init-azurite', 'function1'],  # Depends on function1
    'azurite': [],  # No dependencies
    'init-azurite': ['azurite']  # Depends on azurite
}
```

**Purpose**: Define which services must start before others.

---

### 3. Service Selection Logic

```python
def get_all_dependencies_for_selection(selected_services, dep_map):
    """Recursively get all dependencies for selected services."""
    resources_to_enable = set()
    queue = list(selected_services)

    while queue:
        service = queue.pop(0)
        if service not in resources_to_enable and service in dep_map:
            resources_to_enable.add(service)
            for dep in dep_map[service]:
                if dep not in resources_to_enable:
                    queue.append(dep)

    return list(resources_to_enable)

# Allow running specific services
config.define_string_list('args', args=True)
cfg = config.parse()
requested = cfg.get('args', [])

if requested:
    enabled = get_all_dependencies_for_selection(requested, RESOURCE_DEPENDENCIES)
    config.set_enabled_resources(enabled)
```

**Usage**:
```bash
# Run all services
tilt up

# Run only my-function and its dependencies
tilt up my-function
```

---

### 4. Local Resources

```python
local_resource(
    name='init-azurite',
    cmd='./scripts/init_azurite.sh',  # Command to run
    labels=['storage'],                # Group in Tilt UI
    resource_deps=['azurite']          # Wait for azurite
)
```

**Use cases**:
- Initialize databases/storage
- Run setup scripts
- Generate code/assets

---

### 5. Docker Compose Integration

```python
docker_compose('.docker/docker-compose.dev.yml')
```

**What it does**:
- Loads services from docker-compose file
- Creates Tilt resources for each service
- Manages container lifecycle

---

### 6. Docker Build Configuration

#### Basic Build

```python
docker_build(
    ref='my-image-name',          # Image reference (matches docker-compose)
    context='.',                   # Build context directory
    dockerfile='.docker/Dockerfile' # Path to Dockerfile
)
```

#### Build with Ignore Patterns

```python
docker_build(
    ref='my-function-dev',
    context='.',
    dockerfile='.docker/my-function/Dockerfile',
    ignore=[
        'tests/',
        '.git/',
        '.venv/',
        '**/.venv/',
        '__pycache__/',
        '**/__pycache__/',
        '*.pyc',
        '**/*.pyc'
    ]
)
```

**Purpose**: Reduce build context size, speed up builds.

#### Build with Live Update

```python
docker_build(
    ref='my-function-dev',
    context='.',
    dockerfile='.docker/my-function/Dockerfile',
    ignore=['tests', '.git', '.venv'],
    live_update=[
        # Sync Python code changes
        sync('./functions/my-function/', '/home/site/wwwroot/'),

        # Reinstall requirements when changed
        run(
            'pip install --no-cache-dir -r requirements.txt',
            trigger=['./functions/my-function/requirements.txt']
        ),

        # Restart container to apply changes
        restart_container()
    ]
)
```

**Live Update Rules**:
- `sync(local_path, container_path)`: Copy files to container
- `run(cmd, trigger=[...])`: Run command when files change
- `restart_container()`: Restart container after updates

---

### 7. Live Update Patterns

#### Pattern 1: Simple Code Sync

```python
live_update=[
    sync('./functions/my-function/', '/home/site/wwwroot/'),
    restart_container()
]
```

**Use**: When code changes don't require dependency reinstall.

#### Pattern 2: Dependency Management

```python
live_update=[
    # Sync code
    sync('./functions/my-function/my_function', '/home/site/wwwroot/my_function'),
    sync('./functions/my-function/host.json', '/home/site/wwwroot/host.json'),

    # Reinstall dependencies when requirements.txt changes
    run(
        'pip install --no-cache-dir -r requirements.txt',
        trigger=['./functions/my-function/requirements.txt']
    ),

    restart_container()
]
```

#### Pattern 3: Poetry Projects

```python
live_update=[
    sync('./functions/my-function/', '/home/site/wwwroot/'),

    # Reinstall when poetry files change
    run(
        'poetry export -f requirements.txt --output requirements.txt --without-hashes && '
        'pip install --no-cache-dir -r requirements.txt',
        trigger=['./functions/my-function/poetry.lock', './functions/my-function/pyproject.toml']
    ),

    restart_container()
]
```

#### Pattern 4: Local Package Development

```python
live_update=[
    # Sync function code
    sync('./functions/my-function/', '/home/site/wwwroot/'),

    # Rebuild local package when its source changes
    sync('./my-package/src/', '/tmp/my-package/src/'),
    run(
        'cd /tmp/my-package && poetry build && '
        'pip install --no-cache-dir --force-reinstall dist/*.whl',
        trigger=['./my-package/src/']
    ),

    restart_container()
]
```

---

### 8. Resource Definitions

```python
dc_resource(
    name='my-function',           # Must match docker-compose service name
    labels=['functions'],         # Group in Tilt UI (optional)
    links=['http://localhost:7071'],  # Quick links in UI (optional)
    resource_deps=['azurite']     # Dependencies (optional)
)
```

**labels**: Group related services in Tilt UI
**links**: Add clickable URLs in Tilt UI
**resource_deps**: Ensure dependencies start first

---

### 9. Multiple Function Apps Example

```python
# Build images for each function
for function_name in ['orchestrator', 'processor', 'loader']:
    docker_build(
        ref=f'my-project-{function_name}-dev',
        context='.',
        dockerfile=f'.docker/{function_name}/Dockerfile',
        ignore=['tests', '.git', '.venv'],
        live_update=[
            sync(f'./functions/{function_name}/', '/home/site/wwwroot/'),
            run(
                'pip install --no-cache-dir -r requirements.txt',
                trigger=[f'./functions/{function_name}/requirements.txt']
            ),
            restart_container()
        ]
    )

    # Define resource
    dc_resource(
        name=function_name,
        labels=['functions'],
        resource_deps=['azurite', 'init-azurite']
    )
```

---

## Advanced Patterns

### Custom Commands

```python
# Add custom button in Tilt UI
local_resource(
    name='run-tests',
    cmd='pytest tests/',
    labels=['testing'],
    auto_init=False,  # Don't run automatically
    trigger_mode=TRIGGER_MODE_MANUAL  # Run on button click
)
```

### Conditional Configuration

```python
# Different config for different environments
if os.environ.get('CI') == 'true':
    # CI-specific configuration
    docker_build(ref='my-app', cache_from=['my-registry/my-app:latest'])
else:
    # Local development configuration
    docker_build(ref='my-app', live_update=[...])
```

---

## Tilt UI Features

When you run `tilt up`, the UI (http://localhost:10350) shows:

1. **Resource list**: All services with status (green/red/yellow)
2. **Logs**: Real-time logs for each service
3. **Build progress**: Docker build status
4. **Trigger mode**: Manual/auto for each resource
5. **Links**: Quick access to endpoints
6. **Alerts**: Errors and warnings

**Keyboard shortcuts**:
- `r`: Trigger rebuild for selected resource
- `t`: Toggle trigger mode (auto/manual)
- `/`: Focus search

---

## Best Practices

1. **Use labels**: Group related services (`functions`, `storage`, `databases`)
2. **Add links**: Make endpoints easily accessible
3. **Configure live_update**: Fast iteration without full rebuilds
4. **Use ignore patterns**: Reduce build context size
5. **Set resource_deps**: Ensure correct startup order
6. **Add helpful print statements**: Guide developers
7. **Use service selection**: Allow running subset of services
8. **Document in comments**: Explain complex configurations

---

## Troubleshooting

### Issue: Live update not working

**Check**:
- sync() paths are correct (container path must exist)
- restart_container() is called
- File changes are within sync paths

### Issue: Services start in wrong order

**Solution**: Set resource_deps correctly
```python
dc_resource(
    name='my-function',
    resource_deps=['azurite', 'init-azurite']  # Start these first
)
```

### Issue: Build context too large

**Solution**: Add ignore patterns
```python
docker_build(
    ...,
    ignore=['node_modules/', '.venv/', 'tests/', '.git/']
)
```

---

## Official Documentation

- [Tilt Docs](https://docs.tilt.dev/)
- [Tiltfile API Reference](https://docs.tilt.dev/api.html)
- [Live Update Guide](https://docs.tilt.dev/live_update_reference.html)
- [Docker Build Options](https://docs.tilt.dev/api.html#api.docker_build)
