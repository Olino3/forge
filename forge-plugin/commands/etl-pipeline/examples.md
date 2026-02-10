# /etl-pipeline Examples

## Example 1: Simple Daily ETL with Airflow

```
/etl-pipeline daily-sales-report --orchestrator airflow --schedule daily
```

**What happens**:
1. Asks about data sources:
   - "What's the source?" → PostgreSQL sales database
   - "What's the target?" → Synapse Analytics warehouse
2. Delegates to `skill:database-schema-analysis` for both source and target
3. Generates Airflow DAG:
   - Extract: Query sales data from PostgreSQL
   - Transform: Calculate daily aggregates, clean data
   - Load: Insert into Synapse fact table
4. Includes data quality checks (row count validation)
5. Schedules for 2 AM daily execution

## Example 2: ELT Pattern with Azure Data Factory

```
/etl-pipeline customer-360 --pattern elt --orchestrator azuredf
```

**What happens**:
1. Identifies multiple data sources:
   - CRM database (customer profiles)
   - E-commerce transactions (SQL)
   - Support tickets (MongoDB)
2. Generates Azure Data Factory pipeline:
   - **Extract**: Copy all sources to Data Lake (raw zone)
   - **Load**: Load raw data into Synapse staging tables
   - **Transform**: SQL transformations in Synapse (T-SQL)
3. Creates linked services for all data sources
4. Creates datasets with schema definitions
5. Sets up data flows for transformations

## Example 3: Streaming Pipeline

```
/etl-pipeline realtime-analytics --pattern streaming --schedule realtime
```

**What happens**:
1. Identifies streaming source:
   - Azure Event Hubs (clickstream events)
2. Generates Spark Structured Streaming job:
   - Read from Event Hub
   - Window aggregations (5-minute tumbling windows)
   - Write to Delta Lake tables
3. Configures checkpointing for fault tolerance
4. Adds monitoring with Azure Application Insights
5. Provides Databricks notebook and job configuration

## Example 4: Incremental Load Pipeline

```
/etl-pipeline incremental-sync --orchestrator airflow
```

**What happens**:
1. Asks: "Full or incremental load?"
   - User: "Incremental based on updated_at"
2. Generates pipeline with:
   - State table tracking last processed timestamp
   - Query filter: `WHERE updated_at > last_run_timestamp`
   - Merge/upsert logic in target (not truncate/insert)
3. Handles late-arriving data
4. Creates backfill capability for full refresh

## Example 5: Multi-Source Data Warehouse Pipeline

```
/etl-pipeline enterprise-warehouse --orchestrator databricks --schedule daily
```

**What happens**:
1. Identifies multiple sources:
   - 3 operational databases (PostgreSQL, SQL Server, Oracle)
   - CSV files from SFTP
   - REST APIs (Salesforce, HubSpot)
2. Generates Databricks workflow with:
   - Parallel extraction from all sources
   - Bronze layer: Raw data in Delta Lake
   - Silver layer: Cleaned and standardized data
   - Gold layer: Business-level aggregations
3. Uses Delta Lake for ACID transactions
4. Implements slowly changing dimensions (SCD Type 2)
5. Creates data quality monitoring

## Example 6: File-Based ETL Pipeline

```
/etl-pipeline csv-processor --orchestrator airflow
```

**What happens**:
1. Asks about file details:
   - "File location?" → Azure Blob Storage
   - "File format?" → CSV with headers
2. Delegates to `skill:file-schema-analysis` to understand CSV structure
3. Generates Airflow DAG:
   - Sensor: Wait for new files in blob storage
   - Extract: Download and validate CSVs
   - Transform: Pandas-based transformations
   - Load: Bulk insert into PostgreSQL
4. Handles file archival after processing
5. Logs processed file names to avoid duplicates

## Example 7: Data Quality-Focused Pipeline

```
/etl-pipeline quality-pipeline --orchestrator airflow
```

**What happens**:
1. Emphasizes data quality throughout:
   - **Extract**: Schema validation on source
   - **Transform**: Great Expectations suite
     - Null checks on required fields
     - Range validation on numeric fields
     - Referential integrity checks
   - **Load**: Post-load validation
2. Generates quality report after each run
3. Quarantines bad records in separate table
4. Alerts on quality threshold violations (>1% bad records)

## Example 8: API to Database Pipeline

```
/etl-pipeline api-sync --orchestrator airflow --schedule hourly
```

**What happens**:
1. Identifies REST API as source:
   - "API endpoint?" → https://api.example.com/v1/orders
   - "Authentication?" → API key in header
2. Generates pipeline with:
   - Extract: HTTP requests with pagination handling
   - Transform: JSON parsing and flattening
   - Load: Upsert into PostgreSQL
3. Handles API rate limiting (exponential backoff)
4. Caches responses to avoid duplicate API calls
5. Manages incremental sync based on order timestamps

## Example 9: Cross-Database Sync

```
/etl-pipeline db-replication --pattern elt --schedule hourly
```

**What happens**:
1. Source: Production PostgreSQL
2. Target: Read-replica for analytics (Redshift)
3. Generates pipeline:
   - Change Data Capture (CDC) using database logs
   - Extract only changed rows (inserts, updates, deletes)
   - Load into target with merge strategy
4. Handles schema evolution (new columns)
5. Provides lag monitoring (replication delay alerts)
