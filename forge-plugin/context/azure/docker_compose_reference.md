# Docker Compose Reference for Azure Functions

## Basic Structure

Docker Compose file for Azure Functions local development defines:
1. Function app services
2. Azurite storage service
3. Network configuration
4. Environment variables
5. Port mappings
6. Volume mounts

---

## Complete Example: docker-compose.dev.yml

```yaml
# Docker Compose configuration for Azure Functions development

services:
  # First function app
  my-function:
    image: my-function-dev  # Built by Tilt
    ports:
      - "${MY_FUNCTION_PORT:-7071}:80"
    environment:
      - AzureWebJobsStorage=UseDevelopmentStorage=true;DevelopmentStorageProxyUri=http://azurite
      - AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=${AZURITE_ACCOUNT_KEY};BlobEndpoint=http://azurite:10000/devstoreaccount1;QueueEndpoint=http://azurite:10001/devstoreaccount1;TableEndpoint=http://azurite:10002/devstoreaccount1
      - FUNCTIONS_WORKER_RUNTIME=python
      - MY_CUSTOM_VAR=${MY_CUSTOM_VAR:-default_value}
    depends_on:
      - azurite
    volumes:
      - $HOME/.azure:/root/.azure  # Share Azure CLI credentials

  # Second function app
  another-function:
    image: another-function-dev
    ports:
      - "${ANOTHER_FUNCTION_PORT:-7072}:80"
    environment:
      - AzureWebJobsStorage=UseDevelopmentStorage=true;DevelopmentStorageProxyUri=http://azurite
      - AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=${AZURITE_ACCOUNT_KEY};BlobEndpoint=http://azurite:10000/devstoreaccount1;QueueEndpoint=http://azurite:10001/devstoreaccount1;TableEndpoint=http://azurite:10002/devstoreaccount1
      - FUNCTIONS_WORKER_RUNTIME=python
    depends_on:
      - azurite
    volumes:
      - $HOME/.azure:/root/.azure

  # Azurite storage emulator
  azurite:
    image: my-azurite  # Built by Tilt with custom initialization
    ports:
      - "${AZURITE_BLOB_PORT:-10000}:10000"   # Blob storage
      - "${AZURITE_QUEUE_PORT:-10001}:10001"  # Queue storage
      - "${AZURITE_TABLE_PORT:-10002}:10002"  # Table storage
    environment:
      - AZURITE_ACCOUNTS=devstoreaccount1
      - AZURITE_ACCOUNT_KEY=${AZURITE_ACCOUNT_KEY}
    volumes:
      - azurite_data:/data  # Persist storage data
    command: azurite --blobHost 0.0.0.0 --queueHost 0.0.0.0 --tableHost 0.0.0.0 --location /data --debug /data/debug.log

volumes:
  azurite_data:  # Named volume for Azurite data
```

---

## Service Definitions

### Function App Service

```yaml
my-function:
  image: my-function-dev          # Image name (built by Tilt)
  ports:
    - "7071:80"                    # Host:Container port mapping
  environment:
    # Required Azure Functions variables
    - AzureWebJobsStorage=UseDevelopmentStorage=true;DevelopmentStorageProxyUri=http://azurite
    - FUNCTIONS_WORKER_RUNTIME=python

    # Storage connection string
    - AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=${AZURITE_ACCOUNT_KEY};BlobEndpoint=http://azurite:10000/devstoreaccount1;QueueEndpoint=http://azurite:10001/devstoreaccount1;TableEndpoint=http://azurite:10002/devstoreaccount1

    # Custom environment variables
    - MY_VAR=${MY_VAR:-default_value}

  depends_on:
    - azurite                      # Start azurite first

  volumes:
    - $HOME/.azure:/root/.azure    # Optional: Share Azure credentials
```

**Key components**:
- **image**: Must match `ref` in Tiltfile docker_build()
- **ports**: Map container port 80 to host port (7071+)
- **environment**: All required Azure Functions variables
- **depends_on**: Ensure Azurite starts first
- **volumes**: Optional mounts for credentials or data

---

### Azurite Service

```yaml
azurite:
  image: my-azurite                 # Custom Azurite image with init
  ports:
    - "10000:10000"                 # Blob storage
    - "10001:10001"                 # Queue storage
    - "10002:10002"                 # Table storage
  environment:
    - AZURITE_ACCOUNTS=devstoreaccount1
    - AZURITE_ACCOUNT_KEY=${AZURITE_ACCOUNT_KEY}
  volumes:
    - azurite_data:/data            # Persist data across restarts
  command: azurite --blobHost 0.0.0.0 --queueHost 0.0.0.0 --tableHost 0.0.0.0 --location /data --debug /data/debug.log
```

**Standard Azurite ports**:
- **10000**: Blob storage
- **10001**: Queue storage
- **10002**: Table storage

---

## Environment Variables

### Required for Function Apps

```yaml
environment:
  # Azure Functions runtime identifier
  - FUNCTIONS_WORKER_RUNTIME=python  # or node, dotnet, java

  # Azurite connection (simplified for local)
  - AzureWebJobsStorage=UseDevelopmentStorage=true;DevelopmentStorageProxyUri=http://azurite

  # Full connection string (for SDK usage)
  - AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=${AZURITE_ACCOUNT_KEY};BlobEndpoint=http://azurite:10000/devstoreaccount1;QueueEndpoint=http://azurite:10001/devstoreaccount1;TableEndpoint=http://azurite:10002/devstoreaccount1
```

**Variable substitution**:
- `${VAR_NAME}`: Required variable (fails if not set)
- `${VAR_NAME:-default}`: Optional with default value
- Load from `.env.local` via Tilt: `dotenv('.env.local')`

### Connection String Format

**Local development** (within Docker network):
```
DefaultEndpointsProtocol=http;
AccountName=devstoreaccount1;
AccountKey=${AZURITE_ACCOUNT_KEY};
BlobEndpoint=http://azurite:10000/devstoreaccount1;
QueueEndpoint=http://azurite:10001/devstoreaccount1;
TableEndpoint=http://azurite:10002/devstoreaccount1
```

**Important**:
- Use service name `azurite` (not `localhost` or `127.0.0.1`)
- Docker Compose creates internal network where services can find each other by name

---

## Port Mapping Patterns

### Single Function App

```yaml
ports:
  - "7071:80"  # Fixed port
```

### Multiple Function Apps

```yaml
# Function 1
ports:
  - "7071:80"

# Function 2
ports:
  - "7072:80"

# Function 3
ports:
  - "7073:80"
```

### Configurable Ports (Recommended)

```yaml
ports:
  - "${MY_FUNCTION_PORT:-7071}:80"  # Use env var or default to 7071
```

**Benefits**:
- Can override via `.env.local`
- Avoid port conflicts
- Different ports for different developers

---

## Volume Mounts

### Azure CLI Credentials

```yaml
volumes:
  - $HOME/.azure:/root/.azure
```

**Purpose**: Share Azure CLI authentication from host to container.

**Use case**: Access Azure resources during development (Key Vault, Storage, etc.)

### Azurite Data Persistence

```yaml
volumes:
  - azurite_data:/data
```

**Purpose**: Keep storage data between container restarts.

**Management**:
```bash
# List volumes
docker volume ls

# Remove volume (clear data)
docker volume rm <volume-name>

# Remove all unused volumes
docker volume prune
```

### Function Code (Not Recommended)

```yaml
volumes:
  - ./functions/my-function:/home/site/wwwroot
```

**Don't do this**: Use Tilt's live_update instead for better performance and control.

---

## depends_on

```yaml
my-function:
  depends_on:
    - azurite
```

**What it does**:
- Docker Compose starts `azurite` before `my-function`
- Does **not** wait for azurite to be "ready"

**Limitation**: Service may start before dependency is ready.

**Solution**: Use health checks (see below) or initialization logic in Tiltfile.

---

## Health Checks (Optional)

```yaml
azurite:
  image: my-azurite
  healthcheck:
    test: ["CMD", "nc", "-z", "127.0.0.1", "10000"]
    interval: 5s
    timeout: 3s
    retries: 10
    start_period: 10s

my-function:
  depends_on:
    azurite:
      condition: service_healthy  # Wait until health check passes
```

**Benefits**:
- Ensures dependency is ready before starting dependent service
- Reduces race conditions

**Drawback**:
- Adds complexity
- Not always necessary with Tilt resource_deps

---

## Networks (Usually Not Needed)

Docker Compose creates a default network automatically. All services can communicate using service names.

**Custom network** (if needed):
```yaml
services:
  my-function:
    networks:
      - app-network

  azurite:
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

**Use case**: Multiple compose files, advanced networking.

---

## Multiple Function Apps Pattern

```yaml
services:
  orchestrator:
    image: my-project-orchestrator-dev
    ports:
      - "7071:80"
    environment:
      - FUNCTIONS_WORKER_RUNTIME=python
      - AzureWebJobsStorage=UseDevelopmentStorage=true;DevelopmentStorageProxyUri=http://azurite
      - AZURE_STORAGE_CONNECTION_STRING=...
    depends_on:
      - azurite

  processor:
    image: my-project-processor-dev
    ports:
      - "7072:80"
    environment:
      - FUNCTIONS_WORKER_RUNTIME=python
      - AzureWebJobsStorage=UseDevelopmentStorage=true;DevelopmentStorageProxyUri=http://azurite
      - AZURE_STORAGE_CONNECTION_STRING=...
    depends_on:
      - azurite

  loader:
    image: my-project-loader-dev
    ports:
      - "7073:80"
    environment:
      - FUNCTIONS_WORKER_RUNTIME=python
      - AzureWebJobsStorage=UseDevelopmentStorage=true;DevelopmentStorageProxyUri=http://azurite
      - AZURE_STORAGE_CONNECTION_STRING=...
    depends_on:
      - azurite

  azurite:
    image: my-project-azurite
    ports:
      - "10000:10000"
      - "10001:10001"
      - "10002:10002"
    environment:
      - AZURITE_ACCOUNT_KEY=${AZURITE_ACCOUNT_KEY}
    volumes:
      - azurite_data:/data

volumes:
  azurite_data:
```

---

## Environment-Specific Files

### Development: docker-compose.dev.yml

Use this for local development with Tilt.

### CI/CD: docker-compose.ci.yml

```yaml
services:
  my-function:
    build:
      context: .
      dockerfile: .docker/my-function/Dockerfile
    # No ports needed in CI
    # No volumes needed
```

### Testing: docker-compose.test.yml

```yaml
services:
  test-runner:
    build: .
    command: pytest tests/
    depends_on:
      - azurite
```

**Load specific file**:
```bash
docker-compose -f docker-compose.test.yml up
```

---

## Best Practices

1. **Use environment variable substitution**: `${VAR:-default}`
2. **Externalize secrets**: Load from `.env.local`, never commit
3. **Use named volumes**: For data persistence
4. **Set depends_on**: Define service dependencies
5. **Use service names**: For inter-service communication (not localhost)
6. **Keep images generic**: Specific config via environment variables
7. **Document environment variables**: Add comments
8. **Use health checks**: For critical dependencies (optional)

---

## Common Issues

### Issue: Connection refused to Azurite

**Cause**: Using `localhost` instead of service name.

**Solution**: Use `http://azurite:10000` in connection strings.

### Issue: Port already in use

**Cause**: Another service using the port.

**Solution**:
1. Use environment variables for ports
2. Change port in `.env.local`
3. Or stop conflicting service

### Issue: Environment variables not loading

**Cause**: .env.local not loaded by Tilt.

**Solution**: Add to Tiltfile:
```python
load('ext://dotenv', 'dotenv')
dotenv('.env.local')
```

---

## Official Documentation

- [Docker Compose File Reference](https://docs.docker.com/compose/compose-file/)
- [Environment Variables in Compose](https://docs.docker.com/compose/environment-variables/)
- [Networking in Compose](https://docs.docker.com/compose/networking/)
- [Azurite Connection Strings](https://learn.microsoft.com/azure/storage/common/storage-use-azurite)
