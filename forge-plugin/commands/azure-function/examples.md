# /azure-function Examples

## Example 1: Simple HTTP API Function

```
/azure-function hello-api --runtime python --trigger http
```

**What happens**:
1. Delegates to `skill:generate-azure-functions`
2. Generates Python HTTP-triggered function:
   - GET/POST endpoint at `/api/hello-api`
   - Function key authentication
   - JSON request/response handling
3. Sets up local development:
   - Tiltfile for live reload
   - Azurite for storage emulation
4. Provides test command: `curl http://localhost:7071/api/hello-api`
5. Saves guide to `/claudedocs/azure-function_hello-api_20260210.md`

## Example 2: Timer-Triggered Function (Scheduled Job)

```
/azure-function daily-cleanup --runtime node --trigger timer
```

**What happens**:
1. Asks for schedule: "What schedule (cron)?"
   - User: "0 2 * * *" (daily at 2 AM)
2. Generates Node.js timer function:
   - Runs on schedule
   - Cleans up old data from Blob Storage
3. Includes cron expression in function.json
4. Sets up logging for execution tracking
5. Provides test command: `func start` (triggers locally)

## Example 3: Queue-Triggered Function

```
/azure-function process-orders --runtime python --trigger queue
```

**What happens**:
1. Asks for queue details:
   - "Queue name?" → orders-queue
   - "Output?" → Cosmos DB
2. Generates Python function with:
   - Azure Storage Queue trigger
   - Cosmos DB output binding
3. Local dev with Azurite Queue emulation
4. Test by adding message to local queue:
   ```bash
   az storage message put \
     --queue-name orders-queue \
     --content '{"orderId": 123}' \
     --connection-string "UseDevelopmentStorage=true"
   ```

## Example 4: Blob-Triggered File Processor

```
/azure-function image-processor --runtime dotnet --trigger blob
```

**What happens**:
1. Asks: "Blob container and path pattern?"
   - User: "uploads/{name}.jpg"
2. Generates C# function with:
   - Blob trigger on new JPG uploads
   - Image processing (resize, compress)
   - Output to "processed" container
3. Uses Azure.Storage.Blobs SDK
4. Local dev with Azurite Blob emulation
5. Test by uploading blob to local storage

## Example 5: Event Hub Streaming Function

```
/azure-function stream-processor --runtime python --trigger eventhub
```

**What happens**:
1. Asks for Event Hub details:
   - "Event Hub name?" → clickstream-events
   - "Consumer group?" → analytics-group
2. Generates streaming function with:
   - Event Hub trigger (batch processing)
   - Processes events in batches of 100
   - Aggregates data and writes to Cosmos DB
3. Configures checkpointing for fault tolerance
4. Local dev requires Event Hub (provides Azure connection)

## Example 6: Multi-Function App

```
/azure-function order-service --runtime node
```

**What happens**:
1. Asks: "Multiple functions in this app?"
   - User: "Yes - create-order, get-order, list-orders"
2. Generates Function App with 3 functions:
   - POST /api/orders (create-order)
   - GET /api/orders/{id} (get-order)
   - GET /api/orders (list-orders)
3. Shared dependencies in package.json
4. Shared utilities in /shared folder
5. Single Tiltfile manages all functions

## Example 7: Function with Cosmos DB Integration

```
/azure-function user-api --runtime python --trigger http
```

**What happens**:
1. Asks: "Need database integration?"
   - User: "Yes, Cosmos DB"
2. Generates function with:
   - HTTP trigger for CRUD operations
   - Cosmos DB input/output bindings
   - Connection string in application settings
3. Delegates to `skill:generate-azure-bicep` for infrastructure:
   - Cosmos DB account
   - Database and container
   - Function App
4. Local dev uses Cosmos DB Emulator (or real Cosmos)

## Example 8: Durable Functions Workflow

```
/azure-function order-workflow --runtime dotnet --trigger http
```

**What happens**:
1. Asks: "Need orchestration?"
   - User: "Yes, multi-step order processing"
2. Generates Durable Functions:
   - HTTP starter function
   - Orchestrator function (order workflow)
   - Activity functions (validate, charge, ship)
3. Workflow pattern: Chaining
4. Includes status query endpoint
5. Local dev with durable task hub

## Example 9: Function with Key Vault Integration

```
/azure-function secure-api --runtime python --trigger http
```

**What happens**:
1. Asks: "Use Key Vault for secrets?"
   - User: "Yes"
2. Generates function with:
   - Managed Identity enabled
   - Key Vault references in app settings:
     - `@Microsoft.KeyVault(SecretUri=...)`
3. Delegates to `skill:generate-azure-bicep`:
   - Key Vault with secrets
   - Function App with system-assigned identity
   - Access policies for Function App
4. Local dev uses service principal or local secrets

## Example 10: Complete CI/CD Setup

```
/azure-function payment-api --runtime node --trigger http
```

**What happens**:
1. Generates Node.js HTTP function
2. After generation, suggests:
   - "Generate CI/CD pipeline? (yes/no)" → yes
3. Automatically runs:
   ```
   /azure-pipeline payment-api --target function --type ci-cd
   ```
4. Creates complete setup:
   - Function code with tests
   - Local dev environment (Tilt + Azurite)
   - Infrastructure as Code (Bicep)
   - Azure DevOps pipeline (build, test, deploy)
5. Ready for: `git push` → auto-deploy
