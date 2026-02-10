---
name: etl-pipeline
description: "Engineer data transformation pipelines for ETL/ELT workflows with orchestration and monitoring"
category: orchestration
complexity: advanced
skills: [file-schema-analysis, database-schema-analysis]
context: [schema, commands/etl_patterns]
---

# /etl-pipeline - Data Transformation Pipeline Engineering

## Triggers
- Building data pipelines for analytics or data warehousing
- Implementing ETL (Extract, Transform, Load) workflows
- Creating data integration between systems
- Setting up batch or streaming data processing

## Usage
```
/etl-pipeline [pipeline-name] [--pattern etl|elt|streaming] [--orchestrator airflow|azuredf|databricks|custom] [--schedule hourly|daily|weekly|realtime]
```

**Parameters**:
- `pipeline-name`: Name of the pipeline (required)
- `--pattern`: Data processing pattern (default: etl)
  - `etl`: Extract, Transform, Load (transform before loading)
  - `elt`: Extract, Load, Transform (transform in target system)
  - `streaming`: Real-time stream processing
- `--orchestrator`: Pipeline orchestration tool (default: auto-detect)
  - `airflow`: Apache Airflow (Python-based DAGs)
  - `azuredf`: Azure Data Factory
  - `databricks`: Azure Databricks workflows
  - `custom`: Custom orchestration code
- `--schedule`: Pipeline execution schedule (default: daily)
  - `hourly`, `daily`, `weekly`: Batch processing
  - `realtime`: Continuous streaming

## Workflow

### Step 1: Analyze Data Flow

1. Identify data sources:
   - Database tables, APIs, files (CSV, JSON, Parquet)
   - File storage (Azure Blob, S3, local filesystem)
   - Streaming sources (Event Hubs, Kafka)
2. Identify data targets:
   - Data warehouse (Synapse, Snowflake, Redshift)
   - Database (PostgreSQL, SQL Server, MongoDB)
   - Data lake (Azure Data Lake, S3)
3. Understand transformations needed:
   - Data cleaning and validation
   - Aggregations and calculations
   - Joins and enrichment
   - Data type conversions

### Step 2: Load Context & Memory

**Context Loading**:
1. Read `../../context/commands/index.md` for command guidance
2. Load `../../context/commands/etl_patterns.md` for pipeline best practices
3. Load `../../context/schema/index.md` for data schema patterns
4. Load `../../context/python/index.md` if using Python-based tools

**Memory Loading**:
1. Determine project name
2. Check `../../memory/commands/{project}/etl_pipelines.md` for existing pipelines
3. Load schema analysis results from previous runs
4. Check for existing data models and transformation logic

### Step 3: Schema Analysis

Delegate to schema analysis skills to understand data structures:

**Source schema analysis**:
```
skill:database-schema-analysis --target {source_database}
```
or
```
skill:file-schema-analysis --target {source_files}
```

**Target schema analysis**:
```
skill:database-schema-analysis --target {target_database}
```

**Outcome**: Understand source and target schemas for mapping

### Step 4: Gather Pipeline Requirements

If requirements not clear, gather interactively:

**Questions**:
- What data sources? (databases, files, APIs)
- What transformations are needed? (cleaning, aggregation, joins)
- What is the target? (warehouse, database, data lake)
- How often should it run? (schedule)
- Data quality checks needed?
- Failure handling strategy? (retry, alert, skip)
- Incremental or full load?

### Step 5: Generate Pipeline Components

Based on orchestrator and pattern, generate:

**For Airflow**:
- DAG definition (Python)
- Task definitions for extract, transform, load
- Operators for data sources (PostgresOperator, S3Operator, etc.)
- Data quality checks (Great Expectations integration)
- Alerting configuration (email, Slack)

**For Azure Data Factory**:
- Pipeline JSON definitions
- Linked services for data sources/targets
- Datasets for source and target schemas
- Data flows for transformations
- Triggers for scheduling

**For Databricks**:
- Notebook-based transformations (PySpark/Scala)
- Job definitions for orchestration
- Delta Lake table definitions
- Unity Catalog integration

**For Streaming**:
- Stream processor configuration (Spark Structured Streaming, Flink)
- Event Hub/Kafka consumer setup
- State management and checkpointing
- Window functions and aggregations

### Step 6: Implement Transformations

Generate transformation code based on detected pattern:

**Data Cleaning**:
- Handle missing values
- Remove duplicates
- Validate data types
- Standardize formats (dates, addresses, etc.)

**Data Enrichment**:
- Lookup tables and joins
- Calculated fields
- Aggregations and rollups

**Data Quality**:
- Schema validation
- Business rule checks
- Completeness and accuracy metrics

### Step 7: Generate Output & Update Memory

**Output**:
Save pipeline documentation to `/claudedocs/etl-pipeline_{name}_{date}.md`:

```markdown
# ETL Pipeline - {Pipeline Name}
**Date**: {date}
**Command**: /etl-pipeline {full invocation}
**Pattern**: {etl|elt|streaming}
**Orchestrator**: {orchestrator}
**Schedule**: {schedule}

## Pipeline Overview

### Data Flow
```
[Source 1] ---> |              |
[Source 2] ---> | Transformations | ---> [Target]
[Source N] ---> |              |
```

### Sources
| Source | Type | Location | Schema |
|--------|------|----------|--------|
| Users DB | PostgreSQL | prod.db.server | users, profiles |
| Events | CSV Files | /data/events/ | events.csv |

### Targets
| Target | Type | Location | Purpose |
|--------|------|----------|---------|
| Analytics DW | Synapse | azure://warehouse | Reporting |

## Transformations

### 1. Extract
- Connect to source databases
- Read CSV files from blob storage
- Validate source data availability

### 2. Transform
- **Cleaning**: Remove nulls, deduplicate
- **Enrichment**: Join users with profile data
- **Aggregation**: Daily event counts by user
- **Validation**: Check data quality rules

### 3. Load
- Truncate/insert into target tables
- Update metadata tables
- Create indexes if needed

## Implementation

### Airflow DAG
**File**: `dags/{pipeline_name}_dag.py`

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-team',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': True,
    'email': ['alerts@company.com']
}

dag = DAG(
    '{pipeline_name}',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=datetime(2026, 2, 1),
    catchup=False
)

extract_task = PythonOperator(...)
transform_task = PythonOperator(...)
load_task = PythonOperator(...)

extract_task >> transform_task >> load_task
```

### Data Quality Checks
- Row count validation
- Schema compliance
- Business rule validation
- Completeness checks

## Monitoring

### Metrics
- Pipeline execution time
- Rows processed
- Error rate
- Data quality score

### Alerts
- Failure notifications (email, Slack)
- Data quality threshold violations
- Long-running pipeline warnings

## Setup Instructions

### 1. Install Dependencies
```bash
pip install apache-airflow pandas sqlalchemy great-expectations
```

### 2. Configure Connections
Create connections in Airflow:
- `source_db`: PostgreSQL connection
- `target_warehouse`: Synapse connection
- `blob_storage`: Azure Blob Storage

### 3. Deploy Pipeline
```bash
cp dags/{pipeline_name}_dag.py $AIRFLOW_HOME/dags/
airflow dags list | grep {pipeline_name}
```

### 4. Test Run
```bash
airflow dags test {pipeline_name} 2026-02-10
```

## Incremental Loading
- **Strategy**: Track last processed timestamp
- **State Table**: `etl_metadata.{pipeline_name}_state`
- **Logic**: Only process new/updated records

## Error Handling
- Retry failed tasks (3 attempts)
- Alert on persistent failures
- Skip and log bad records (don't fail entire pipeline)
- Quarantine table for failed transformations

## Next Steps
- Test with sample data: Use `/test` to validate transformations
- Schedule production run: Enable Airflow DAG
- Monitor first runs: Check Airflow UI and logs
- Optimize: Profile and tune for performance
```

**Memory Updates**:
1. Append to `../../memory/commands/{project}/command_history.md`
2. Update `../../memory/commands/{project}/etl_pipelines.md`:
   - Pipeline configurations, schedules, source/target mappings
3. Store schema mappings for future reference

## Tool Coordination
- **Read**: Schema definitions, existing transformation code
- **Grep/Glob**: Find existing pipelines and DAG files
- **Write**: Pipeline code, DAG definitions, documentation
- **Bash**: Test pipeline execution, Airflow CLI commands
- **Skills**: file-schema-analysis, database-schema-analysis

## Key Patterns
- **Schema-Driven**: Analyze schemas first for accurate mapping
- **Idempotent**: Pipelines can be safely re-run
- **Incremental**: Process only new/changed data when possible
- **Observable**: Comprehensive logging and monitoring

## Boundaries

**Will:**
- Generate complete ETL/ELT pipeline code and configuration
- Analyze source and target schemas for transformation mapping
- Create orchestration code (Airflow DAGs, ADF pipelines, Databricks jobs)
- Implement data quality checks and validation
- Provide monitoring and alerting configuration

**Will Not:**
- Execute pipelines in production (provides code and setup)
- Create database schemas (only uses existing schemas)
- Handle real-time streaming at massive scale (provides starting point)
- Replace data engineering expertise (assists with scaffolding)

**Output**: Pipeline documentation saved to `/claudedocs/etl-pipeline_{name}_{date}.md`

**Next Step**: Use `/test` to validate pipeline, or `/azure-pipeline` to create CI/CD for the pipeline.
