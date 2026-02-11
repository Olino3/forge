---
id: "azure/azurite_setup"
domain: azure
title: "Azurite Storage Emulator Setup"
type: reference
estimatedTokens: 2400
loadingStrategy: onDemand
version: "1.0.0"
lastUpdated: "2026-02-10"
sections:
  - name: "Overview"
    estimatedTokens: 22
    keywords: [overview]
  - name: "Azurite Dockerfile"
    estimatedTokens: 102
    keywords: [azurite, dockerfile]
  - name: "Azurite Initialization Script"
    estimatedTokens: 274
    keywords: [azurite, initialization, script]
  - name: "Connection Strings"
    estimatedTokens: 45
    keywords: [connection, strings]
  - name: "Custom Account Key"
    estimatedTokens: 38
    keywords: [custom, account]
  - name: "Azurite Command Line Options"
    estimatedTokens: 45
    keywords: [azurite, command, line, options]
  - name: "Data Persistence"
    estimatedTokens: 67
    keywords: [data, persistence]
  - name: "Accessing Azurite Storage"
    estimatedTokens: 81
    keywords: [accessing, azurite, storage]
  - name: "Health Checks"
    estimatedTokens: 48
    keywords: [health, checks]
  - name: "Common Use Cases"
    estimatedTokens: 100
    keywords: [cases]
  - name: "Troubleshooting"
    estimatedTokens: 92
    keywords: [troubleshooting]
  - name: "Best Practices"
    estimatedTokens: 43
    keywords: [best]
  - name: "Official Documentation"
    estimatedTokens: 12
    keywords: [official, documentation]
tags: [azure, azurite, storage, emulator, blob, queue, table, docker]
---

# Azurite Storage Emulator Setup

## Overview

**Azurite** is the official Azure Storage emulator for local development. It provides:
- Blob storage
- Queue storage
- Table storage

All compatible with Azure Storage SDK and APIs.

---

## Azurite Dockerfile

### Basic Azurite Dockerfile

```dockerfile
FROM mcr.microsoft.com/azure-storage/azurite:latest

# Expose storage ports
EXPOSE 10000 10001 10002

# Start Azurite with all services
CMD ["azurite", "--blobHost", "0.0.0.0", "--queueHost", "0.0.0.0", "--tableHost", "0.0.0.0", "--location", "/data"]
```

### Azurite with Initialization Script

```dockerfile
FROM mcr.microsoft.com/azure-storage/azurite:latest

# Install Python and dependencies for initialization
USER root
RUN apk add --no-cache python3 py3-pip netcat-openbsd

# Create virtual environment and install Azure Storage SDK
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir \
    azure-storage-blob \
    azure-storage-queue \
    azure-data-tables

# Copy initialization script
COPY .docker/scripts/init_azurite.sh /init_azurite.sh
RUN chmod +x /init_azurite.sh

# Expose ports
EXPOSE 10000 10001 10002

# Start Azurite and run initialization
ENTRYPOINT ["/bin/sh", "-c", "azurite --blobHost 0.0.0.0 --queueHost 0.0.0.0 --tableHost 0.0.0.0 --location /data --debug /data/debug.log & sleep 5 && /init_azurite.sh && wait"]
```

**Purpose**: Initialize containers, queues, and tables on startup.

---

## Azurite Initialization Script

### Complete init_azurite.sh

```bash
#!/bin/sh
# Initialize Azurite storage emulator with containers, queues, and tables

set -e

echo "Initializing Azurite storage emulator..."

# Wait for Azurite to be ready
echo "Waiting for Azurite to be ready..."
for i in $(seq 1 30); do
  if nc -z 127.0.0.1 10000 2>/dev/null; then
    echo "Azurite is ready!"
    break
  fi
  echo "Waiting... ($i/30)"
  sleep 2
done

# Activate virtual environment
export PATH="/opt/venv/bin:$PATH"

# Get account key from environment
AZURITE_KEY="${AZURITE_ACCOUNT_KEY:-Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==}"

# Run Python initialization
/opt/venv/bin/python3 << 'EOF'
import sys
import os
from azure.storage.blob import BlobServiceClient
from azure.storage.queue import QueueServiceClient
from azure.data.tables import TableServiceClient

# Connection string
account_key = os.environ.get('AZURITE_KEY', 'Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==')
conn_string = f"DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey={account_key};BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;TableEndpoint=http://127.0.0.1:10002/devstoreaccount1"

print("=" * 70)
print("AZURITE INITIALIZATION")
print("=" * 70)

# ============================================================================
# Blob Containers
# ============================================================================
print("\n[1/3] Creating blob containers...")
try:
    blob_service = BlobServiceClient.from_connection_string(conn_string)

    containers = [
        ("uploads", "File uploads"),
        ("processed", "Processed files"),
        ("archive", "Archived files")
    ]

    for container_name, description in containers:
        try:
            blob_service.create_container(container_name)
            print(f"  ✓ '{container_name}' created - {description}")
        except Exception as e:
            if "ContainerAlreadyExists" in str(e):
                print(f"  ✓ '{container_name}' already exists - {description}")
            else:
                print(f"  ✗ Error creating container '{container_name}': {e}")
except Exception as e:
    print(f"❌ Error with blob service: {e}")
    sys.exit(1)

# ============================================================================
# Queues
# ============================================================================
print("\n[2/3] Creating queues...")
try:
    queue_service = QueueServiceClient.from_connection_string(conn_string)

    queues = [
        ("tasks", "Task processing queue"),
        ("notifications", "Notification queue")
    ]

    for queue_name, description in queues:
        try:
            queue_service.create_queue(queue_name)
            print(f"  ✓ '{queue_name}' created - {description}")
        except Exception as e:
            if "QueueAlreadyExists" in str(e):
                print(f"  ✓ '{queue_name}' already exists - {description}")
            else:
                print(f"  ✗ Error creating queue '{queue_name}': {e}")
except Exception as e:
    print(f"❌ Error with queue service: {e}")
    sys.exit(1)

# ============================================================================
# Tables
# ============================================================================
print("\n[3/3] Creating tables...")
try:
    table_service = TableServiceClient.from_connection_string(conn_string)

    tables = [
        ("Users", "User data"),
        ("AuditLog", "Audit logging"),
        ("Configuration", "Application configuration")
    ]

    for table_name, description in tables:
        try:
            table_service.create_table(table_name)
            print(f"  ✓ '{table_name}' created - {description}")
        except Exception as e:
            if "TableAlreadyExists" in str(e):
                print(f"  ✓ '{table_name}' already exists - {description}")
            else:
                print(f"  ✗ Error creating table '{table_name}': {e}")
except Exception as e:
    print(f"❌ Error with table service: {e}")
    sys.exit(1)

print("\n" + "=" * 70)
print("✅ AZURITE INITIALIZATION COMPLETE!")
print("=" * 70)
print()

EOF

echo "Initialization script completed successfully!"
```

**Customization**: Modify container, queue, and table lists for your project.

---

## Connection Strings

### Default Azurite Account

- **Account Name**: `devstoreaccount1`
- **Account Key**: `Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==`

### Connection String Format

**From Docker container** (use service name):
```
DefaultEndpointsProtocol=http;
AccountName=devstoreaccount1;
AccountKey=YOUR_KEY;
BlobEndpoint=http://azurite:10000/devstoreaccount1;
QueueEndpoint=http://azurite:10001/devstoreaccount1;
TableEndpoint=http://azurite:10002/devstoreaccount1
```

**From host machine** (use localhost):
```
DefaultEndpointsProtocol=http;
AccountName=devstoreaccount1;
AccountKey=YOUR_KEY;
BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;
QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;
TableEndpoint=http://127.0.0.1:10002/devstoreaccount1
```

### Simplified Connection String (Azure Functions)

```
UseDevelopmentStorage=true;DevelopmentStorageProxyUri=http://azurite
```

**Note**: Only works from within Docker network.

---

## Custom Account Key

### Generate Custom Key

```bash
# Generate random key
openssl rand -base64 64 | tr -d '\n'
```

### Store in .env.local

```bash
# .env.local (add to .gitignore)
AZURITE_ACCOUNT_KEY=your-generated-key-here
```

### Use in Docker Compose

```yaml
azurite:
  environment:
    - AZURITE_ACCOUNT_KEY=${AZURITE_ACCOUNT_KEY}
```

### Load in Tiltfile

```python
load('ext://dotenv', 'dotenv')
dotenv('.env.local')
```

---

## Azurite Command Line Options

### Basic Options

```bash
azurite \
  --blobHost 0.0.0.0 \
  --queueHost 0.0.0.0 \
  --tableHost 0.0.0.0 \
  --location /data
```

### With Debug Logging

```bash
azurite \
  --blobHost 0.0.0.0 \
  --queueHost 0.0.0.0 \
  --tableHost 0.0.0.0 \
  --location /data \
  --debug /data/debug.log
```

### Custom Ports

```bash
azurite \
  --blobPort 11000 \
  --queuePort 11001 \
  --tablePort 11002
```

**Standard ports**: 10000, 10001, 10002

---

## Data Persistence

### Named Volume (Recommended)

**docker-compose.yml**:
```yaml
azurite:
  volumes:
    - azurite_data:/data

volumes:
  azurite_data:
```

**Benefits**:
- Data persists across container restarts
- Managed by Docker
- Easy to clean up

**Management**:
```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect <volume-name>

# Remove volume (clear all data)
docker volume rm <volume-name>

# Remove all unused volumes
docker volume prune
```

### Bind Mount

```yaml
azurite:
  volumes:
    - ./data/azurite:/data
```

**Benefits**:
- Data visible on host filesystem
- Easy to inspect/backup

**Drawback**:
- Permission issues on Linux

---

## Accessing Azurite Storage

### Azure Storage Explorer

1. Download [Azure Storage Explorer](https://azure.microsoft.com/features/storage-explorer/)
2. Connect to local emulator
3. Use connection string or attach emulator account

### Azure CLI

```bash
# List blobs
az storage blob list \
  --container-name mycontainer \
  --connection-string "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;..."

# Upload blob
az storage blob upload \
  --container-name mycontainer \
  --file ./myfile.txt \
  --name myfile.txt \
  --connection-string "..."

# List tables
az storage table list \
  --connection-string "..."
```

### Python SDK

```python
from azure.storage.blob import BlobServiceClient

conn_str = "DefaultEndpointsProtocol=http;..."
blob_service = BlobServiceClient.from_connection_string(conn_str)

# List containers
for container in blob_service.list_containers():
    print(container.name)

# Upload blob
blob_client = blob_service.get_blob_client(
    container="mycontainer",
    blob="myfile.txt"
)
with open("./myfile.txt", "rb") as data:
    blob_client.upload_blob(data)
```

---

## Health Checks

### Check Azurite is Ready

```bash
# Check blob service
curl http://localhost:10000/devstoreaccount1?comp=list

# Check table service
curl http://localhost:10002/devstoreaccount1/Tables
```

### Wait for Azurite in Script

```bash
#!/bin/bash
echo "Waiting for Azurite..."
for i in {1..30}; do
  if nc -z localhost 10000; then
    echo "Azurite is ready!"
    exit 0
  fi
  echo "Waiting... ($i/30)"
  sleep 2
done
echo "Azurite failed to start"
exit 1
```

---

## Common Use Cases

### 1. HTTP Trigger with Blob Output

**Function**:
```python
import azure.functions as func

@app.route(route="upload")
@app.blob_output(arg_name="outputblob", path="uploads/{DateTime}.txt",
                 connection="AzureWebJobsStorage")
def upload(req: func.HttpRequest, outputblob: func.Out[str]) -> func.HttpResponse:
    content = req.get_body().decode('utf-8')
    outputblob.set(content)
    return func.HttpResponse("File uploaded!")
```

**Test**:
```bash
curl -X POST http://localhost:7071/api/upload \
  -H "Content-Type: text/plain" \
  -d "Hello, Azurite!"
```

### 2. Blob Trigger

```python
@app.blob_trigger(arg_name="myblob", path="uploads/{name}",
                  connection="AzureWebJobsStorage")
def process_blob(myblob: func.InputStream):
    logging.info(f"Processing blob: {myblob.name}, Size: {myblob.length}")
```

**Test**: Upload blob via Storage Explorer or SDK.

### 3. Queue Trigger

```python
@app.queue_trigger(arg_name="msg", queue_name="tasks",
                   connection="AzureWebJobsStorage")
def process_queue(msg: func.QueueMessage):
    logging.info(f"Processing message: {msg.get_body().decode()}")
```

**Test**: Add message to queue via Storage Explorer or SDK.

### 4. Table Storage

```python
from azure.data.tables import TableServiceClient

conn_str = os.environ['AZURE_STORAGE_CONNECTION_STRING']
table_service = TableServiceClient.from_connection_string(conn_str)

# Insert entity
table_client = table_service.get_table_client("Users")
entity = {
    "PartitionKey": "users",
    "RowKey": "user1",
    "Name": "John Doe",
    "Email": "john@example.com"
}
table_client.create_entity(entity)
```

---

## Troubleshooting

### Issue: Connection refused

**Symptoms**: `ConnectionRefusedError: [Errno 111] Connection refused`

**Causes**:
1. Azurite not started
2. Wrong host (using localhost instead of service name in Docker)
3. Wrong port

**Solutions**:
```bash
# Check Azurite is running
docker ps | grep azurite

# Check logs
docker logs <azurite-container-id>

# Verify connection string uses correct host
# From container: http://azurite:10000
# From host: http://127.0.0.1:10000
```

### Issue: Authentication failed

**Symptoms**: `AuthenticationErrorDetail`

**Cause**: Wrong account key.

**Solution**: Verify AZURITE_ACCOUNT_KEY matches in:
- .env.local
- docker-compose.yml
- Connection strings

### Issue: Container/Table already exists

**Symptoms**: `ResourceExistsError`

**Cause**: Resource created in previous run (data persisted).

**Solutions**:
1. Ignore error (resource exists, that's fine)
2. Clear Azurite data: `docker volume rm <volume-name>`
3. Use try/except in initialization script

---

## Best Practices

1. **Use named volumes**: For data persistence
2. **Initialize on startup**: Create containers/tables automatically
3. **Use custom account key**: Don't rely on default key
4. **Enable debug logging**: Helps troubleshoot issues
5. **Wait for ready**: Use health checks before accessing
6. **Clean up periodically**: Remove old volumes to free space
7. **Document resources**: List containers/queues/tables in README

---

## Official Documentation

- [Azurite GitHub](https://github.com/Azure/Azurite)
- [Use Azurite Emulator](https://learn.microsoft.com/azure/storage/common/storage-use-azurite)
- [Azure Storage SDK for Python](https://learn.microsoft.com/python/api/overview/azure/storage)
- [Azure Table Storage](https://learn.microsoft.com/azure/storage/tables/table-storage-overview)
