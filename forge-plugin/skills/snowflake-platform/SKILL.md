---
name: snowflake-platform
description: Build on Snowflake's AI Data Cloud with snow CLI, Cortex AI (COMPLETE, SUMMARIZE, AI_FILTER), Native Apps, and Snowpark. Covers JWT auth, account identifiers, Marketplace publishing. Prevents 11 errors. Triggers: snowflake, snow cli, snowflake connection
version: "1.0.0"
context:
  primary_domain: "schema"
  always_load_files: []
  detection_required: false
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [account_config.md, data_pipelines.md, cortex_patterns.md, snowpark_models.md, native_apps.md]
    - type: "shared-project"
##       usage: "reference"

# Skill: snowflake-platform

**Version**: 1.0.0
**Purpose**: Build on Snowflake's AI Data Cloud with snow CLI, Cortex AI, Native Apps, and Snowpark
**Author**: The Forge
**Last Updated**: 2025-07-14

---

## Purpose

Build on Snowflake's AI Data Cloud with snow CLI, Cortex AI (COMPLETE, SUMMARIZE, AI_FILTER), Native Apps, and Snowpark. Covers JWT auth, account identifiers, Marketplace publishing. Prevents 11 errors. Triggers: snowflake, snow cli, snowflake connection


## Title

**Snowflake Platform** — Build, deploy, and operate on Snowflake's AI Data Cloud

---

## File Structure

```
forge-plugin/skills/snowflake-platform/
├── SKILL.md                  # This file - mandatory workflow
└── examples.md               # Usage scenarios and examples
```

---

## Required Reading

**Before executing this skill**, load context and memory via interfaces:

1. **Context**: Use `contextProvider.getDomainIndex("schema")` for relevant domain context. See [ContextProvider Interface](../../interfaces/context_provider.md).

2. **Skill memory**: Use `memoryStore.getSkillMemory("snowflake-platform", "{project-name}")` for previous configurations. See [MemoryStore Interface](../../interfaces/memory_store.md).

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Shared Patterns**: [Shared Loading Patterns](../../interfaces/shared_loading_patterns.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

---

## Snowflake Platform Reference

### Account Identifiers

Snowflake uses the `ORGNAME-ACCOUNTNAME` format for account identifiers:

```
-- Connection format
<orgname>-<accountname>.snowflakecomputing.com

-- Examples
MYORG-ACCOUNT1.snowflakecomputing.com
MYORG-ACCOUNT1.privatelink.snowflakecomputing.com  -- Private Link
```

**Key rules**:
- Account identifiers are case-insensitive
- Org name and account name are separated by a hyphen
- Legacy locator format (`xy12345.us-east-1`) is deprecated — always use `ORGNAME-ACCOUNTNAME`
- Private Link endpoints append `.privatelink` before `.snowflakecomputing.com`

### snow CLI

The Snowflake CLI (`snow`) manages Snowflake objects, Snowpark apps, and Native Apps from the terminal.

```bash
# Installation
pip install snowflake-cli-labs

# Connection management
snow connection add --connection-name dev --account ORGNAME-ACCOUNTNAME
snow connection test --connection-name dev
snow connection set-default dev

# Object management
snow sql -q "SELECT CURRENT_WAREHOUSE(), CURRENT_DATABASE()"
snow sql -f setup.sql --connection dev

# Snowpark
snow snowpark build
snow snowpark deploy --replace
snow snowpark execute function "my_udf(42)"

# Native Apps
snow app init my_app --template basic
snow app run        # deploy + install in dev
snow app deploy     # stage files only
snow app teardown   # remove dev app + package

# Streamlit
snow streamlit deploy --replace
```

**Connection config** (`~/.snowflake/config.toml`):
```toml
[connections.dev]
account = "ORGNAME-ACCOUNTNAME"
user = "MY_USER"
authenticator = "SNOWFLAKE_JWT"
private_key_file = "~/.snowflake/rsa_key.p8"
warehouse = "COMPUTE_WH"
database = "MY_DB"
schema = "PUBLIC"
role = "SYSADMIN"
```

### JWT Key-Pair Authentication

Preferred for CI/CD and service accounts — no passwords to rotate.

```bash
# 1. Generate 2048-bit RSA key pair
openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out rsa_key.p8 -nocrypt

# 2. Extract public key
openssl rsa -in rsa_key.p8 -pubout -out rsa_key.pub

# 3. Assign public key to Snowflake user (strip PEM headers)
ALTER USER my_service_user SET RSA_PUBLIC_KEY='MIIBIjAN...';

# 4. Verify fingerprint
DESC USER my_service_user;
-- RSA_PUBLIC_KEY_FP = 'SHA256:...'
```

**CI/CD environment variables**:
```bash
SNOWFLAKE_ACCOUNT=ORGNAME-ACCOUNTNAME
SNOWFLAKE_USER=SVC_DEPLOY
SNOWFLAKE_PRIVATE_KEY_PATH=/secrets/rsa_key.p8
SNOWFLAKE_AUTHENTICATOR=SNOWFLAKE_JWT
```

### Cortex AI Functions

Cortex AI provides serverless AI functions that run inside Snowflake — no data leaves the platform.

#### COMPLETE — LLM text generation

```sql
-- Basic completion
SELECT SNOWFLAKE.CORTEX.COMPLETE(
    'mistral-large2',
    'Summarize the key trends in this sales data'
) AS response;

-- Structured prompt with system + user messages
SELECT SNOWFLAKE.CORTEX.COMPLETE(
    'mistral-large2',
    [
        {'role': 'system', 'content': 'You are a data analyst.'},
        {'role': 'user', 'content': 'Explain why Q3 revenue dropped 15%.'}
    ]::ARRAY(OBJECT(role STRING, content STRING)),
    {'temperature': 0.3, 'max_tokens': 1024}
) AS analysis;

-- Per-row completion over a table
SELECT
    product_name,
    SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-large2',
        CONCAT('Write a 50-word marketing blurb for: ', product_name, ' — ', description)
    ) AS blurb
FROM products
LIMIT 100;
```

**Available models**: `mistral-large2`, `llama3.1-70b`, `llama3.1-8b`, `mistral-7b`, `gemma-7b`, `mixtral-8x7b`

#### SUMMARIZE — Condense text

```sql
SELECT SNOWFLAKE.CORTEX.SUMMARIZE(support_ticket_text) AS summary
FROM support_tickets
WHERE created_at > DATEADD('day', -7, CURRENT_TIMESTAMP());
```

#### AI_FILTER — Boolean classification

```sql
-- Filter rows using natural language
SELECT *
FROM customer_reviews
WHERE SNOWFLAKE.CORTEX.AI_FILTER(
    review_text,
    'The customer mentions a product defect or safety concern'
);
```

#### EMBED — Vector embeddings

```sql
-- Generate embeddings for semantic search
SELECT
    doc_id,
    SNOWFLAKE.CORTEX.EMBED('e5-base-v2', content) AS embedding
FROM documents;

-- Semantic similarity search
SELECT doc_id, content,
    VECTOR_COSINE_SIMILARITY(
        embedding,
        SNOWFLAKE.CORTEX.EMBED('e5-base-v2', 'quarterly revenue forecast')
    ) AS similarity
FROM documents
ORDER BY similarity DESC
LIMIT 10;
```

### Snowpark (Python / Java / Scala)

Snowpark pushes computation to Snowflake — data never leaves the platform.

```python
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col, udf, sproc
from snowflake.snowpark.types import IntegerType, StringType

# Create session
session = Session.builder.configs({
    "account": "ORGNAME-ACCOUNTNAME",
    "user": "MY_USER",
    "private_key_file": "rsa_key.p8",
    "authenticator": "SNOWFLAKE_JWT",
    "warehouse": "COMPUTE_WH",
    "database": "MY_DB",
    "schema": "PUBLIC",
    "role": "SYSADMIN"
}).create()

# DataFrame API (lazy evaluation)
df = session.table("sales")
result = (
    df.filter(col("region") == "EMEA")
      .group_by("product_category")
      .agg({"revenue": "sum", "quantity": "count"})
      .sort(col("sum(revenue)").desc())
)
result.show()

# User-Defined Function (UDF)
@udf(name="classify_sentiment", is_permanent=True,
     stage_location="@my_stage", replace=True,
     input_types=[StringType()], return_type=StringType(),
     packages=["textblob"])
def classify_sentiment(text: str) -> str:
    from textblob import TextBlob
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.1:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    return "neutral"

# Stored Procedure
@sproc(name="daily_etl", is_permanent=True,
       stage_location="@my_stage", replace=True,
       packages=["snowflake-snowpark-python"])
def daily_etl(session: Session) -> str:
    raw = session.table("raw_events")
    cleaned = raw.filter(col("event_type").is_not_null())
    cleaned.write.mode("append").save_as_table("clean_events")
    return f"Processed {cleaned.count()} rows"
```

### Native Apps Framework

Package and distribute applications through the Snowflake Marketplace.

```
my_native_app/
├── snowflake.yml              # Project definition
├── app/
│   ├── manifest.yml           # App manifest
│   ├── setup_script.sql       # Runs on install
│   ├── README.md              # Marketplace listing
│   └── streamlit/
│       └── dashboard.py       # UI component
└── scripts/
    └── deploy.sql             # Deployment helper
```

**snowflake.yml**:
```yaml
definition_version: 2
entities:
  my_app_pkg:
    type: application package
    stage: app.stage
    manifest: app/manifest.yml
    artifacts:
      - src: app/*
        dest: ./
  my_app:
    type: application
    from:
      target: my_app_pkg
    debug: false
```

**manifest.yml**:
```yaml
manifest_version: 1
version:
  name: v1
  label: "1.0.0"
  comment: "Initial release"
artifacts:
  setup_script: setup_script.sql
  readme: README.md
  default_streamlit: streamlit/dashboard.py
configuration:
  log_level: INFO
  trace_level: OFF
privileges:
  - CREATE DATABASE:
      description: "Store application data"
  - EXECUTE TASK:
      description: "Run scheduled jobs"
```

**setup_script.sql**:
```sql
CREATE APPLICATION ROLE IF NOT EXISTS app_user;
CREATE SCHEMA IF NOT EXISTS core;
GRANT USAGE ON SCHEMA core TO APPLICATION ROLE app_user;

CREATE OR REPLACE PROCEDURE core.configure(config VARIANT)
RETURNS STRING
LANGUAGE SQL
AS $$
BEGIN
    -- Application initialization logic
    RETURN 'Configuration complete';
END;
$$;

GRANT USAGE ON PROCEDURE core.configure(VARIANT) TO APPLICATION ROLE app_user;
```

### Marketplace Publishing

```sql
-- 1. Create application package
CREATE APPLICATION PACKAGE my_app_pkg;

-- 2. Upload artifacts to stage
PUT file://app/* @my_app_pkg.app.stage AUTO_COMPRESS=FALSE OVERWRITE=TRUE;

-- 3. Create version
ALTER APPLICATION PACKAGE my_app_pkg
    ADD VERSION v1 USING '@my_app_pkg.app.stage';

-- 4. Set release directive
ALTER APPLICATION PACKAGE my_app_pkg
    SET DEFAULT RELEASE DIRECTIVE
    VERSION = v1 PATCH = 0;

-- 5. Create listing (via Snowsight UI or Provider Studio)
-- Set visibility, pricing, sample queries, usage examples
```

### Data Sharing & Collaboration

```sql
-- Create a share
CREATE SHARE analytics_share;
GRANT USAGE ON DATABASE analytics_db TO SHARE analytics_share;
GRANT USAGE ON SCHEMA analytics_db.public TO SHARE analytics_share;
GRANT SELECT ON TABLE analytics_db.public.kpi_summary TO SHARE analytics_share;

-- Add consumer accounts
ALTER SHARE analytics_share ADD ACCOUNTS = CONSUMER_ORG-CONSUMER_ACCT;

-- Consumer side: create database from share
CREATE DATABASE shared_analytics FROM SHARE PROVIDER_ORG-PROVIDER_ACCT.analytics_share;
```

### Warehouses, Databases & Schemas

```sql
-- Warehouse management
CREATE WAREHOUSE IF NOT EXISTS etl_wh
    WAREHOUSE_SIZE = 'MEDIUM'
    AUTO_SUSPEND = 300
    AUTO_RESUME = TRUE
    MIN_CLUSTER_COUNT = 1
    MAX_CLUSTER_COUNT = 3
    SCALING_POLICY = 'STANDARD'
    INITIALLY_SUSPENDED = TRUE;

-- Resource monitor
CREATE RESOURCE MONITOR monthly_budget
    WITH CREDIT_QUOTA = 1000
    FREQUENCY = MONTHLY
    START_TIMESTAMP = IMMEDIATELY
    TRIGGERS
        ON 75 PERCENT DO NOTIFY
        ON 90 PERCENT DO NOTIFY
        ON 100 PERCENT DO SUSPEND;
ALTER WAREHOUSE etl_wh SET RESOURCE_MONITOR = monthly_budget;

-- Database + schema
CREATE DATABASE IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS analytics.staging;
CREATE SCHEMA IF NOT EXISTS analytics.curated;
```

### Streams, Tasks & Pipes (CDC)

```sql
-- Stream: track changes on a table
CREATE OR REPLACE STREAM raw_events_stream ON TABLE raw_events
    APPEND_ONLY = TRUE;

-- Task: process stream on schedule
CREATE OR REPLACE TASK process_events
    WAREHOUSE = etl_wh
    SCHEDULE = '5 MINUTE'
    WHEN SYSTEM$STREAM_HAS_DATA('raw_events_stream')
AS
    INSERT INTO clean_events
    SELECT event_id, event_type, payload, created_at
    FROM raw_events_stream
    WHERE event_type IS NOT NULL;

ALTER TASK process_events RESUME;

-- Snowpipe: auto-ingest from stage
CREATE OR REPLACE PIPE ingest_pipe
    AUTO_INGEST = TRUE
AS
    COPY INTO raw_events
    FROM @external_stage
    FILE_FORMAT = (TYPE = 'JSON');

-- Get SQS notification channel for auto-ingest
SHOW PIPES LIKE 'ingest_pipe';
-- Use notification_channel value to configure S3 event notifications
```

### Time Travel & Cloning

```sql
-- Query historical data (up to 90 days on Enterprise)
SELECT * FROM sales AT(OFFSET => -3600);            -- 1 hour ago
SELECT * FROM sales AT(TIMESTAMP => '2025-01-15 09:00:00'::TIMESTAMP_LTZ);
SELECT * FROM sales BEFORE(STATEMENT => '<query_id>');

-- Restore dropped table
UNDROP TABLE accidentally_dropped_table;

-- Zero-copy clone (instant, no storage cost until divergence)
CREATE TABLE sales_backup CLONE sales;
CREATE SCHEMA staging_clone CLONE production AT(TIMESTAMP => '2025-07-01'::TIMESTAMP_LTZ);
CREATE DATABASE dev_copy CLONE production;
```

---

## Instructions

## Mandatory Workflow

### MANDATORY STEPS (Must Execute in Order)

---

#### **Step 1: Initial Analysis**

**Purpose**: Understand the Snowflake workload and requirements

**Actions**:
1. Identify the Snowflake use case (data pipeline, Cortex AI, Native App, Snowpark, administration)
2. Check for existing Snowflake configuration (snow CLI config, connection files, `snowflake.yml`)
3. Determine the account identifier format in use
4. Review existing SQL scripts, Snowpark code, or Native App manifests
5. Note the authentication method (password, JWT key-pair, SSO)

**Output**: Clear understanding of project's Snowflake footprint and requirements

---

#### **Step 2: Load Memory**

**Purpose**: Retrieve previous Snowflake configurations for this project

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="snowflake-platform"` and `domain="schema"`.

**Actions**:
1. Use `memoryStore.getSkillMemory("snowflake-platform", "{project-name}")` to load project memory
2. If memory exists, review:
   - `account_config.md` — Account identifiers, warehouses, roles, connection profiles
   - `data_pipelines.md` — Streams, tasks, pipes, ETL patterns
   - `cortex_patterns.md` — Cortex AI function usage, model selections, prompt templates
   - `snowpark_models.md` — UDFs, stored procedures, DataFrame patterns
   - `native_apps.md` — App packages, versions, Marketplace listings
3. If not exists, note this is first-time setup

**Output**: Understanding of project Snowflake history or recognition of new project

---

#### **Step 3: Load Context**

**Purpose**: Load relevant database and platform knowledge

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `schema` domain. Stay within the file budget declared in frontmatter.

**Actions**:
1. Use `contextProvider.getDomainIndex("schema")` to identify relevant context files
2. Load database design patterns, naming conventions, and best practices
3. Cross-reference with Snowflake-specific patterns from memory

**Output**: Comprehensive understanding of applicable patterns and conventions

---

#### **Step 4: Snowflake Platform Implementation**

**Purpose**: Execute the core Snowflake task

**Actions**:

**A. For Data Pipelines**:
1. Design warehouse sizing and auto-suspend strategy
2. Create database/schema hierarchy
3. Configure streams for CDC on source tables
4. Build tasks with appropriate schedules and WHEN conditions
5. Set up Snowpipe for continuous ingestion from cloud storage
6. Apply resource monitors and cost controls

**B. For Cortex AI**:
1. Select appropriate model for the task (COMPLETE, SUMMARIZE, AI_FILTER, EMBED)
2. Design prompt templates with system/user message structure
3. Implement batch processing with row-level functions
4. Set up vector storage and similarity search if using EMBED
5. Configure temperature, max_tokens, and other inference parameters

**C. For Snowpark Development**:
1. Set up session configuration with JWT authentication
2. Build DataFrame transformations (lazy evaluation)
3. Create UDFs with proper type annotations and package dependencies
4. Create stored procedures for complex ETL workflows
5. Deploy via `snow snowpark deploy --replace`

**D. For Native Apps**:
1. Initialize project with `snow app init`
2. Define `manifest.yml` with version, privileges, and artifacts
3. Create `setup_script.sql` with application roles and schemas
4. Add Streamlit UI components if needed
5. Test with `snow app run` in development
6. Prepare for Marketplace listing

**E. For Administration**:
1. Configure snow CLI connections with JWT key-pair auth
2. Set up role hierarchy (ACCOUNTADMIN → SYSADMIN → custom roles)
3. Create resource monitors with credit quotas and triggers
4. Enable time travel retention policies
5. Configure data sharing with consumer accounts

**Output**: Complete Snowflake implementation artifacts

---

#### **Step 5: Generate Output**

**Purpose**: Produce deliverable artifacts

**Actions**:
1. Save output to `/claudedocs/snowflake-platform_{project}_{YYYY-MM-DD}.md`
2. Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
3. Include:
   - SQL scripts with comments
   - Snowpark Python code with type hints
   - snow CLI commands for deployment
   - Configuration files (`snowflake.yml`, `config.toml`, `manifest.yml`)
   - Resource monitor and cost control setup
   - Testing and validation queries

**Output**: Complete, deployable Snowflake artifacts

---

#### **Step 6: Update Memory**

**Purpose**: Store configuration for future reference

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="snowflake-platform"`. Store any newly learned patterns, conventions, or project insights.

**Actions**:
1. Use `memoryStore.update(layer="skill-specific", skill="snowflake-platform", project="{project-name}", ...)` to store:
2. **account_config.md**: Account identifiers, warehouse inventory, role hierarchy, connection profiles, authentication method
3. **data_pipelines.md**: Stream/task/pipe definitions, ETL schedules, data flow diagrams, Snowpipe configurations
4. **cortex_patterns.md**: Model selections per use case, prompt templates, inference parameters, embedding strategies
5. **snowpark_models.md**: UDF registry, stored procedure inventory, DataFrame patterns, package dependencies
6. **native_apps.md**: App package versions, Marketplace listings, release directives, privilege requirements

**Output**: Memory stored for future skill invocations

---

## 11 Common Snowflake Errors to Prevent

### 1. Wrong Account Identifier Format
- **Error**: `HTTP 403: Forbidden` or connection timeout
- **Cause**: Using legacy locator (`xy12345.us-east-1`) instead of `ORGNAME-ACCOUNTNAME`
- **Fix**: Always use `ORGNAME-ACCOUNTNAME` format; check with `SHOW ORGANIZATION ACCOUNTS`

### 2. JWT Authentication Failure
- **Error**: `JWT token is invalid` or `Authentication token has expired`
- **Cause**: Mismatched public key, wrong key format, or key not assigned to user
- **Fix**: Verify fingerprint with `DESC USER`; ensure PKCS#8 format; strip PEM headers when assigning

### 3. Warehouse Suspended During Query
- **Error**: `Warehouse 'X' is suspended` or queries hang indefinitely
- **Cause**: `AUTO_RESUME = FALSE` or warehouse not started
- **Fix**: Set `AUTO_RESUME = TRUE`; verify with `SHOW WAREHOUSES`

### 4. Cortex AI Model Not Available
- **Error**: `Unknown model` or `Model not available in this region`
- **Cause**: Not all models are available in every Snowflake region
- **Fix**: Check model availability for your region; use `mistral-large2` as the safest default

### 5. Stream Staleness
- **Error**: `Stream has become stale`
- **Cause**: Stream not consumed within the data retention period
- **Fix**: Ensure tasks consume streams regularly; increase `DATA_RETENTION_TIME_IN_DAYS` on source table

### 6. Snowpark Package Not Available
- **Error**: `Package 'X' is not available in Snowflake Anaconda channel`
- **Cause**: Not all PyPI packages are available in Snowflake's curated Anaconda channel
- **Fix**: Check available packages with `session.get_available_packages()`; use imports from staged files as fallback

### 7. Native App Privilege Escalation
- **Error**: `Insufficient privileges` during app installation
- **Cause**: Setup script requests privileges not declared in `manifest.yml`
- **Fix**: Declare all required privileges in `manifest.yml` under `privileges`; request at install time

### 8. Snowpipe File Reprocessing
- **Error**: Duplicate records from Snowpipe ingestion
- **Cause**: File notification sent multiple times or files re-uploaded with same name
- **Fix**: Use unique file names with timestamps; check `COPY_HISTORY` for load status; use `FORCE = FALSE` (default)

### 9. Time Travel Exceeded Retention
- **Error**: `Cannot perform time travel beyond retention period`
- **Cause**: Trying to access data beyond `DATA_RETENTION_TIME_IN_DAYS` (default: 1 day, max: 90 on Enterprise)
- **Fix**: Increase retention before you need it; use `CREATE TABLE ... CLONE ... AT(...)` for important snapshots

### 10. Resource Monitor Credit Exhaustion
- **Error**: Warehouse suspended by resource monitor
- **Cause**: Credit quota exceeded; `ON 100 PERCENT DO SUSPEND` triggered
- **Fix**: Set staged alerts (75%, 90%, 100%); use `SUSPEND_IMMEDIATE` only for hard limits; adjust quota with `ALTER RESOURCE MONITOR`

### 11. Data Sharing Cross-Region Failure
- **Error**: `Cannot share data to account in different region`
- **Cause**: Direct shares only work within the same cloud region
- **Fix**: Use database replication for cross-region sharing; or use Listings (Marketplace) for cross-cloud/cross-region distribution

---

## Best Practices

### Cost Control
1. **Always set AUTO_SUSPEND** — 60–300 seconds for interactive, 0 for batch
2. **Use resource monitors** — staged alerts at 75%, 90%, 100%
3. **Right-size warehouses** — start small, scale up based on query profiles
4. **Use multi-cluster warehouses** — for concurrency, not for faster single queries
5. **Monitor with ACCOUNT_USAGE** — `WAREHOUSE_METERING_HISTORY` and `QUERY_HISTORY`

### Security
1. **JWT key-pair for services** — no passwords in CI/CD
2. **Network policies** — restrict IP ranges
3. **Role hierarchy** — least-privilege access; never use ACCOUNTADMIN for applications
4. **Dynamic data masking** — protect PII in shared datasets
5. **Encryption** — customer-managed keys (Tri-Secret Secure) for sensitive workloads

### Cortex AI
1. **Choose the right model** — `mistral-large2` for quality, `mistral-7b` for speed/cost
2. **Batch with care** — Cortex functions have concurrency limits
3. **Cache results** — store COMPLETE/SUMMARIZE outputs to avoid re-computation
4. **Use EMBED + VECTOR_COSINE_SIMILARITY** — for semantic search instead of LIKE/ILIKE

### Snowpark
1. **Lazy evaluation** — chain transformations before calling `.collect()` or `.show()`
2. **Permanent UDFs for production** — `is_permanent=True` with `stage_location`
3. **Specify packages explicitly** — don't rely on implicit imports
4. **Use vectorized UDFs** — for better performance on large datasets

---

## Compliance Checklist

Before completing, verify:

- [ ] All mandatory workflow steps executed in order
- [ ] Standard Memory Loading pattern followed (Step 2)
- [ ] Standard Context Loading pattern followed (Step 3)
- [ ] Output saved with standard naming convention
- [ ] Standard Memory Update pattern followed (Step 6)
- [ ] Account identifier uses `ORGNAME-ACCOUNTNAME` format (not legacy locator)
- [ ] JWT key-pair used for service accounts (no hardcoded passwords)
- [ ] Resource monitors configured for all warehouses
- [ ] No sensitive credentials stored in memory or output files
- [ ] Cortex AI model availability verified for target region
- [ ] Native App privileges declared in manifest.yml

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-07-14 | Initial release — snow CLI, Cortex AI, Native Apps, Snowpark, JWT auth, CDC patterns, 11 error prevention rules |

---

## Related Skills

- **database-schema-analysis**: For analyzing existing Snowflake schemas
- **generate-azure-pipelines**: For CI/CD pipelines that deploy to Snowflake
- **generate-python-unit-tests**: For testing Snowpark UDFs and stored procedures

---

## References

- [Snowflake Documentation](https://docs.snowflake.com/)
- [snow CLI Reference](https://docs.snowflake.com/en/developer-guide/snowflake-cli/index)
- [Cortex AI Functions](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions)
- [Snowpark Python Developer Guide](https://docs.snowflake.com/en/developer-guide/snowpark/python/index)
- [Native Apps Framework](https://docs.snowflake.com/en/developer-guide/native-apps/native-apps-about)
- [Snowflake Marketplace](https://docs.snowflake.com/en/developer-guide/native-apps/marketplace)
