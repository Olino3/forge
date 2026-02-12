# Snowflake Platform Skill Examples

This file demonstrates typical usage scenarios for the `snowflake-platform` skill.

---

## Example 1: Data Pipeline with Snowpark and Cortex AI

### Scenario

A retail analytics team needs to ingest raw product reviews, clean them with Snowpark, classify sentiment with Cortex AI COMPLETE, and surface insights via a summary table — all within Snowflake.

### User Request

"We have raw product reviews landing in S3 every hour. I need a pipeline that ingests them into Snowflake, cleans the data with Snowpark, classifies sentiment using Cortex AI, and creates a daily summary table. Use JWT auth for the service account."

### Skill Workflow

**Step 1: Initial Analysis**
- Use case: Data pipeline with AI enrichment
- Source: S3 bucket with JSON review files
- Target: Curated `review_insights` table
- Auth: JWT key-pair for service account `SVC_ETL`
- Existing: No prior Snowflake setup in this project

**Step 2: Load Memory**
- `memoryStore.getSkillMemory("snowflake-platform", "retail-analytics")` → No existing memory (first run)

**Step 3: Load Context**
- `contextProvider.getDomainIndex("schema")` → Load database design patterns, naming conventions

**Step 4: Snowflake Platform Implementation**

Generated SQL — warehouse and database setup:
```sql
-- Warehouse for ETL workloads
CREATE WAREHOUSE IF NOT EXISTS etl_wh
    WAREHOUSE_SIZE = 'SMALL'
    AUTO_SUSPEND = 120
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE;

CREATE RESOURCE MONITOR etl_budget
    WITH CREDIT_QUOTA = 500
    FREQUENCY = MONTHLY
    START_TIMESTAMP = IMMEDIATELY
    TRIGGERS
        ON 75 PERCENT DO NOTIFY
        ON 90 PERCENT DO NOTIFY
        ON 100 PERCENT DO SUSPEND;
ALTER WAREHOUSE etl_wh SET RESOURCE_MONITOR = etl_budget;

-- Database hierarchy
CREATE DATABASE IF NOT EXISTS retail;
CREATE SCHEMA IF NOT EXISTS retail.raw;
CREATE SCHEMA IF NOT EXISTS retail.staging;
CREATE SCHEMA IF NOT EXISTS retail.curated;

-- Raw landing table
CREATE TABLE IF NOT EXISTS retail.raw.product_reviews (
    review_id STRING,
    product_id STRING,
    reviewer_name STRING,
    review_text STRING,
    star_rating INT,
    review_date TIMESTAMP_LTZ,
    _loaded_at TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP()
);

-- External stage pointing to S3
CREATE OR REPLACE STAGE retail.raw.reviews_stage
    URL = 's3://retail-data/reviews/'
    STORAGE_INTEGRATION = s3_integration
    FILE_FORMAT = (TYPE = 'JSON');

-- Snowpipe for auto-ingest
CREATE OR REPLACE PIPE retail.raw.reviews_pipe
    AUTO_INGEST = TRUE
AS
    COPY INTO retail.raw.product_reviews
    FROM @retail.raw.reviews_stage
    MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;
```

Generated Snowpark — cleaning and sentiment analysis:
```python
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col, call_function, lit, concat, current_timestamp
from snowflake.snowpark.types import StringType

session = Session.builder.configs({
    "account": "RETAILORG-PROD1",
    "user": "SVC_ETL",
    "private_key_file": "/secrets/rsa_key.p8",
    "authenticator": "SNOWFLAKE_JWT",
    "warehouse": "ETL_WH",
    "database": "RETAIL",
    "schema": "STAGING",
    "role": "ETL_ROLE"
}).create()

# Read from stream (CDC on raw table)
raw_reviews = session.table("RAW.PRODUCT_REVIEWS_STREAM")

# Clean: remove nulls, trim whitespace, filter short reviews
cleaned = (
    raw_reviews
    .filter(col("REVIEW_TEXT").is_not_null())
    .filter(col("STAR_RATING").between(1, 5))
    .with_column("REVIEW_TEXT", col("REVIEW_TEXT").strip())
    .filter(col("REVIEW_TEXT").length() > 20)
)

# Classify sentiment with Cortex AI COMPLETE
enriched = cleaned.with_column(
    "SENTIMENT",
    call_function(
        "SNOWFLAKE.CORTEX.COMPLETE",
        lit("mistral-7b"),
        concat(
            lit("Classify this product review as positive, negative, or neutral. "
                "Reply with ONLY one word. Review: "),
            col("REVIEW_TEXT")
        )
    )
)

# Write to staging
enriched.write.mode("append").save_as_table("STAGING.ENRICHED_REVIEWS")
```

Generated SQL — daily summary task:
```sql
-- Stream on raw reviews
CREATE OR REPLACE STREAM retail.raw.product_reviews_stream
    ON TABLE retail.raw.product_reviews
    APPEND_ONLY = TRUE;

-- Daily summary task
CREATE OR REPLACE TASK retail.curated.daily_review_summary
    WAREHOUSE = etl_wh
    SCHEDULE = 'USING CRON 0 6 * * * America/New_York'
AS
    MERGE INTO retail.curated.review_insights AS target
    USING (
        SELECT
            product_id,
            CURRENT_DATE() AS summary_date,
            COUNT(*) AS review_count,
            AVG(star_rating) AS avg_rating,
            COUNT_IF(TRIM(sentiment) = 'positive') AS positive_count,
            COUNT_IF(TRIM(sentiment) = 'negative') AS negative_count,
            SNOWFLAKE.CORTEX.SUMMARIZE(
                LISTAGG(review_text, ' | ') WITHIN GROUP (ORDER BY review_date DESC)
            ) AS daily_summary
        FROM retail.staging.enriched_reviews
        WHERE review_date >= DATEADD('day', -1, CURRENT_DATE())
        GROUP BY product_id
    ) AS source
    ON target.product_id = source.product_id AND target.summary_date = source.summary_date
    WHEN MATCHED THEN UPDATE SET
        review_count = source.review_count,
        avg_rating = source.avg_rating,
        positive_count = source.positive_count,
        negative_count = source.negative_count,
        daily_summary = source.daily_summary
    WHEN NOT MATCHED THEN INSERT VALUES (
        source.product_id, source.summary_date, source.review_count,
        source.avg_rating, source.positive_count, source.negative_count,
        source.daily_summary
    );

ALTER TASK retail.curated.daily_review_summary RESUME;
```

**Step 5: Generate Output**
- Saved to `/claudedocs/snowflake-platform_retail-analytics_2025-07-14.md`
- Includes: SQL scripts, Snowpark code, deployment commands, resource monitor setup

**Step 6: Update Memory**
- `account_config.md` — Account `RETAILORG-PROD1`, JWT auth, `ETL_WH` warehouse, `ETL_ROLE` role
- `data_pipelines.md` — Snowpipe `reviews_pipe`, stream `product_reviews_stream`, task `daily_review_summary`
- `cortex_patterns.md` — `mistral-7b` for sentiment classification, `SUMMARIZE` for daily summaries
- `snowpark_models.md` — Cleaning pipeline with sentiment enrichment, session config pattern

### Expected Output

A complete data pipeline with:
- Auto-ingest from S3 via Snowpipe
- CDC tracking with streams
- Snowpark cleaning and Cortex AI sentiment classification
- Daily MERGE summary with SUMMARIZE
- Resource monitors and cost controls
- JWT authentication for CI/CD

---

## Example 2: Building a Native App for Marketplace Publishing

### Scenario

A data analytics company wants to package their anomaly detection algorithm as a Snowflake Native App and publish it to the Marketplace so customers can run it on their own data without sharing raw data.

### User Request

"We have an anomaly detection model written in Python. I want to package it as a Snowflake Native App that customers install from the Marketplace. It should run on their data, show results in a Streamlit dashboard, and never move their data outside their account."

### Skill Workflow

**Step 1: Initial Analysis**
- Use case: Native App for Marketplace distribution
- Core logic: Python anomaly detection (isolation forest)
- UI: Streamlit dashboard
- Key constraint: Data stays in customer account

**Step 2: Load Memory**
- `memoryStore.getSkillMemory("snowflake-platform", "anomaly-detector-app")` → No existing memory

**Step 3: Load Context**
- `contextProvider.getDomainIndex("schema")` → Load Native App patterns, Snowpark UDF conventions

**Step 4: Snowflake Platform Implementation**

Generated project structure:
```
anomaly-detector/
├── snowflake.yml
├── app/
│   ├── manifest.yml
│   ├── setup_script.sql
│   ├── README.md
│   └── streamlit/
│       └── anomaly_dashboard.py
└── src/
    └── detect_anomalies.py
```

**snowflake.yml**:
```yaml
definition_version: 2
entities:
  anomaly_detector_pkg:
    type: application package
    stage: app.stage
    manifest: app/manifest.yml
    artifacts:
      - src: app/*
        dest: ./
      - src: src/*
        dest: src/
  anomaly_detector:
    type: application
    from:
      target: anomaly_detector_pkg
    debug: true
```

**app/manifest.yml**:
```yaml
manifest_version: 1
version:
  name: v1
  label: "1.0.0"
  comment: "Anomaly detection for time-series data"
artifacts:
  setup_script: setup_script.sql
  readme: README.md
  default_streamlit: streamlit/anomaly_dashboard.py
configuration:
  log_level: INFO
  trace_level: OFF
privileges:
  - CREATE DATABASE:
      description: "Store anomaly detection results"
  - EXECUTE TASK:
      description: "Run scheduled anomaly scans"
references:
  - consumer_table:
      label: "Source data table"
      description: "Table with time-series data to analyze"
      privileges:
        - SELECT
      object_type: TABLE
      multi_valued: false
      register_callback: core.register_reference
```

**app/setup_script.sql**:
```sql
CREATE APPLICATION ROLE IF NOT EXISTS app_user;
CREATE APPLICATION ROLE IF NOT EXISTS app_admin;

CREATE SCHEMA IF NOT EXISTS core;
CREATE SCHEMA IF NOT EXISTS results;
GRANT USAGE ON SCHEMA core TO APPLICATION ROLE app_user;
GRANT USAGE ON SCHEMA results TO APPLICATION ROLE app_user;
GRANT USAGE ON SCHEMA core TO APPLICATION ROLE app_admin;

-- Register consumer table reference
CREATE OR REPLACE PROCEDURE core.register_reference(ref_name STRING, operation STRING, ref_or_alias STRING)
RETURNS STRING
LANGUAGE SQL
AS $$
BEGIN
    CASE (operation)
        WHEN 'ADD' THEN SELECT SYSTEM$SET_REFERENCE(:ref_name, :ref_or_alias);
        WHEN 'REMOVE' THEN SELECT SYSTEM$REMOVE_REFERENCE(:ref_name);
        WHEN 'CLEAR' THEN SELECT SYSTEM$REMOVE_REFERENCE(:ref_name);
    END CASE;
    RETURN 'OK';
END;
$$;

-- Anomaly detection UDF (vectorized for performance)
CREATE OR REPLACE FUNCTION core.detect_anomalies(
    values ARRAY, timestamps ARRAY, sensitivity FLOAT
)
RETURNS VARIANT
LANGUAGE PYTHON
RUNTIME_VERSION = '3.11'
PACKAGES = ('scikit-learn', 'pandas', 'numpy')
IMPORTS = ('/src/detect_anomalies.py')
HANDLER = 'detect_anomalies.run';

-- Run analysis procedure
CREATE OR REPLACE PROCEDURE core.run_analysis(sensitivity FLOAT DEFAULT 0.05)
RETURNS TABLE (ts TIMESTAMP_LTZ, value FLOAT, is_anomaly BOOLEAN, anomaly_score FLOAT)
LANGUAGE SQL
AS $$
DECLARE
    res RESULTSET;
BEGIN
    res := (
        SELECT
            ts, value,
            anomaly_result:"is_anomaly"::BOOLEAN AS is_anomaly,
            anomaly_result:"score"::FLOAT AS anomaly_score
        FROM (
            SELECT
                ts, value,
                core.detect_anomalies(
                    ARRAY_AGG(value) OVER (ORDER BY ts ROWS BETWEEN 99 PRECEDING AND CURRENT ROW),
                    ARRAY_AGG(ts) OVER (ORDER BY ts ROWS BETWEEN 99 PRECEDING AND CURRENT ROW),
                    :sensitivity
                ) AS anomaly_result
            FROM REFERENCE('consumer_table')
        )
    );
    RETURN TABLE(res);
END;
$$;

GRANT USAGE ON FUNCTION core.detect_anomalies(ARRAY, ARRAY, FLOAT) TO APPLICATION ROLE app_user;
GRANT USAGE ON PROCEDURE core.run_analysis(FLOAT) TO APPLICATION ROLE app_user;
```

**app/streamlit/anomaly_dashboard.py**:
```python
import streamlit as st
from snowflake.snowpark.context import get_active_session

session = get_active_session()

st.title("🔍 Anomaly Detector")
st.markdown("Detect anomalies in your time-series data without moving it outside your account.")

sensitivity = st.slider("Sensitivity", 0.01, 0.20, 0.05, 0.01,
                        help="Lower = more anomalies detected")

if st.button("Run Analysis"):
    with st.spinner("Analyzing..."):
        results = session.call("core.run_analysis", sensitivity)
        df = results.to_pandas()

    st.metric("Total Records", len(df))
    st.metric("Anomalies Found", df["IS_ANOMALY"].sum())

    st.subheader("Anomaly Timeline")
    st.line_chart(df.set_index("TS")["VALUE"])

    anomalies = df[df["IS_ANOMALY"]]
    if not anomalies.empty:
        st.subheader("Detected Anomalies")
        st.dataframe(anomalies[["TS", "VALUE", "ANOMALY_SCORE"]]
                     .sort_values("ANOMALY_SCORE", ascending=False))
```

Development and deployment commands:
```bash
# Initialize and test locally
snow app run --connection dev

# Validate before publishing
snow app deploy
snow sql -q "CALL anomaly_detector.core.run_analysis(0.05)"

# Create version for Marketplace
snow app version create v1 --skip-git-check

# Publish via Provider Studio (Snowsight UI)
# 1. Go to Data Products → Provider Studio → Listings
# 2. Create listing → Select anomaly_detector_pkg
# 3. Set description, sample queries, documentation
# 4. Publish to Marketplace
```

**Step 5: Generate Output**
- Saved to `/claudedocs/snowflake-platform_anomaly-detector-app_2025-07-14.md`

**Step 6: Update Memory**
- `native_apps.md` — App package `anomaly_detector_pkg`, version v1, Streamlit UI, consumer references
- `snowpark_models.md` — `detect_anomalies` UDF with scikit-learn, vectorized execution

### Expected Output

A complete Native App package with:
- `snowflake.yml` project definition
- `manifest.yml` with privileges and consumer references
- Setup script with application roles, UDFs, and stored procedures
- Streamlit dashboard for interactive analysis
- Deployment and Marketplace publishing workflow

---

## Example 3: JWT Authentication Setup with snow CLI for CI/CD

### Scenario

A DevOps team needs to set up automated Snowflake deployments from GitHub Actions. They need JWT key-pair authentication (no passwords), connection profiles for dev/staging/prod, and a deployment script that uses snow CLI.

### User Request

"Set up snow CLI with JWT authentication for our CI/CD pipeline in GitHub Actions. We have three environments: dev, staging, and prod. Each has its own Snowflake account. I need the key generation steps, connection config, and a GitHub Actions workflow that deploys SQL migrations."

### Skill Workflow

**Step 1: Initial Analysis**
- Use case: CI/CD authentication and deployment
- Environments: dev, staging, prod (separate Snowflake accounts)
- CI/CD platform: GitHub Actions
- Auth: JWT key-pair (no passwords)
- Deployment: SQL migration scripts via snow CLI

**Step 2: Load Memory**
- `memoryStore.getSkillMemory("snowflake-platform", "dataops-pipeline")` → No existing memory

**Step 3: Load Context**
- `contextProvider.getDomainIndex("schema")` → Load authentication patterns, CI/CD best practices

**Step 4: Snowflake Platform Implementation**

Key generation script:
```bash
#!/bin/bash
set -euo pipefail

# Generate key pairs for each environment
for ENV in dev staging prod; do
    echo "=== Generating keys for ${ENV} ==="

    # Generate encrypted private key (PKCS#8 format)
    openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM \
        -out "snowflake_${ENV}_rsa_key.p8" -nocrypt

    # Extract public key
    openssl rsa -in "snowflake_${ENV}_rsa_key.p8" -pubout \
        -out "snowflake_${ENV}_rsa_key.pub"

    # Extract public key body (strip headers) for Snowflake ALTER USER
    PUBLIC_KEY_BODY=$(grep -v "PUBLIC KEY" "snowflake_${ENV}_rsa_key.pub" | tr -d '\n')
    echo ""
    echo "Run in Snowflake (${ENV}):"
    echo "ALTER USER SVC_DEPLOY SET RSA_PUBLIC_KEY='${PUBLIC_KEY_BODY}';"
    echo ""

    chmod 600 "snowflake_${ENV}_rsa_key.p8"
done

echo "=== Done ==="
echo "Add private keys to GitHub Actions secrets:"
echo "  SNOWFLAKE_DEV_PRIVATE_KEY     = contents of snowflake_dev_rsa_key.p8"
echo "  SNOWFLAKE_STAGING_PRIVATE_KEY = contents of snowflake_staging_rsa_key.p8"
echo "  SNOWFLAKE_PROD_PRIVATE_KEY    = contents of snowflake_prod_rsa_key.p8"
```

Snowflake user setup (run once per environment):
```sql
-- Run as ACCOUNTADMIN in each environment
USE ROLE ACCOUNTADMIN;

-- Create deployment role
CREATE ROLE IF NOT EXISTS DEPLOY_ROLE;
GRANT ROLE DEPLOY_ROLE TO ROLE SYSADMIN;

-- Grant necessary privileges
GRANT USAGE ON WAREHOUSE DEPLOY_WH TO ROLE DEPLOY_ROLE;
GRANT ALL ON DATABASE app_db TO ROLE DEPLOY_ROLE;
GRANT CREATE SCHEMA ON DATABASE app_db TO ROLE DEPLOY_ROLE;

-- Create service user (no password — JWT only)
CREATE USER IF NOT EXISTS SVC_DEPLOY
    DEFAULT_ROLE = DEPLOY_ROLE
    DEFAULT_WAREHOUSE = DEPLOY_WH
    MUST_CHANGE_PASSWORD = FALSE
    TYPE = SERVICE;

GRANT ROLE DEPLOY_ROLE TO USER SVC_DEPLOY;

-- Assign public key (from key generation output)
ALTER USER SVC_DEPLOY SET RSA_PUBLIC_KEY='MIIBIjAN...';

-- Verify
DESC USER SVC_DEPLOY;
-- Check RSA_PUBLIC_KEY_FP matches expected fingerprint
```

snow CLI connection config (`config.toml`):
```toml
# Template for CI/CD — actual values come from environment variables

[connections.dev]
account = "MYORG-DEV1"
user = "SVC_DEPLOY"
authenticator = "SNOWFLAKE_JWT"
private_key_file = "/tmp/snowflake_key.p8"
warehouse = "DEPLOY_WH"
database = "APP_DB"
schema = "PUBLIC"
role = "DEPLOY_ROLE"

[connections.staging]
account = "MYORG-STAGING1"
user = "SVC_DEPLOY"
authenticator = "SNOWFLAKE_JWT"
private_key_file = "/tmp/snowflake_key.p8"
warehouse = "DEPLOY_WH"
database = "APP_DB"
schema = "PUBLIC"
role = "DEPLOY_ROLE"

[connections.prod]
account = "MYORG-PROD1"
user = "SVC_DEPLOY"
authenticator = "SNOWFLAKE_JWT"
private_key_file = "/tmp/snowflake_key.p8"
warehouse = "DEPLOY_WH"
database = "APP_DB"
schema = "PUBLIC"
role = "DEPLOY_ROLE"
```

GitHub Actions workflow (`.github/workflows/snowflake-deploy.yml`):
```yaml
name: Snowflake Deploy

on:
  push:
    branches: [main]
    paths: ['migrations/**']
  pull_request:
    branches: [main]
    paths: ['migrations/**']

env:
  SNOW_VERSION: "2.x"

jobs:
  validate:
    name: Validate SQL Migrations
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install snow CLI
        run: pip install snowflake-cli-labs

      - name: Write private key
        run: |
          echo "${{ secrets.SNOWFLAKE_DEV_PRIVATE_KEY }}" > /tmp/snowflake_key.p8
          chmod 600 /tmp/snowflake_key.p8

      - name: Setup snow config
        run: |
          mkdir -p ~/.snowflake
          cp .snowflake/config.toml ~/.snowflake/config.toml

      - name: Test connection
        run: snow connection test --connection dev

      - name: Dry-run migrations
        run: |
          for f in migrations/*.sql; do
            echo "=== Validating: $f ==="
            snow sql -f "$f" --connection dev --dry-run || exit 1
          done

  deploy-staging:
    name: Deploy to Staging
    needs: validate
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4

      - name: Install snow CLI
        run: pip install snowflake-cli-labs

      - name: Write private key
        run: |
          echo "${{ secrets.SNOWFLAKE_STAGING_PRIVATE_KEY }}" > /tmp/snowflake_key.p8
          chmod 600 /tmp/snowflake_key.p8

      - name: Setup snow config
        run: |
          mkdir -p ~/.snowflake
          cp .snowflake/config.toml ~/.snowflake/config.toml

      - name: Run migrations
        run: |
          for f in migrations/*.sql; do
            echo "=== Running: $f ==="
            snow sql -f "$f" --connection staging
          done

      - name: Verify deployment
        run: |
          snow sql -q "SELECT CURRENT_DATABASE(), CURRENT_SCHEMA(), CURRENT_TIMESTAMP()" \
            --connection staging

  deploy-prod:
    name: Deploy to Production
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4

      - name: Install snow CLI
        run: pip install snowflake-cli-labs

      - name: Write private key
        run: |
          echo "${{ secrets.SNOWFLAKE_PROD_PRIVATE_KEY }}" > /tmp/snowflake_key.p8
          chmod 600 /tmp/snowflake_key.p8

      - name: Setup snow config
        run: |
          mkdir -p ~/.snowflake
          cp .snowflake/config.toml ~/.snowflake/config.toml

      - name: Create pre-deployment clone
        run: |
          snow sql -q "CREATE DATABASE app_db_pre_deploy_backup CLONE app_db" \
            --connection prod

      - name: Run migrations
        run: |
          for f in migrations/*.sql; do
            echo "=== Running: $f ==="
            snow sql -f "$f" --connection prod
          done

      - name: Verify deployment
        run: |
          snow sql -q "SELECT CURRENT_DATABASE(), CURRENT_SCHEMA(), CURRENT_TIMESTAMP()" \
            --connection prod

      - name: Drop backup clone (if successful)
        if: success()
        run: |
          snow sql -q "DROP DATABASE IF EXISTS app_db_pre_deploy_backup" \
            --connection prod
```

**Step 5: Generate Output**
- Saved to `/claudedocs/snowflake-platform_dataops-pipeline_2025-07-14.md`

**Step 6: Update Memory**
- `account_config.md` — Three accounts (MYORG-DEV1, MYORG-STAGING1, MYORG-PROD1), JWT auth, `SVC_DEPLOY` user, `DEPLOY_ROLE`
- `data_pipelines.md` — SQL migration workflow, GitHub Actions deployment stages

### Expected Output

A complete CI/CD authentication and deployment setup:
- RSA key-pair generation script for three environments
- Snowflake user/role creation SQL
- snow CLI connection config (no passwords)
- GitHub Actions workflow with validate → staging → prod pipeline
- Pre-deployment zero-copy clone for rollback safety
- All secrets managed via GitHub Actions secrets (never in code)

---

## Common Patterns

### Pattern 1: Cortex AI Batch Processing

```sql
-- Process rows in batches to respect concurrency limits
CREATE OR REPLACE PROCEDURE batch_classify(batch_size INT DEFAULT 1000)
RETURNS STRING
LANGUAGE SQL
AS $$
DECLARE
    total_processed INT DEFAULT 0;
    batch_count INT;
BEGIN
    LOOP
        SELECT COUNT(*) INTO batch_count
        FROM reviews
        WHERE sentiment IS NULL
        LIMIT :batch_size;

        IF (batch_count = 0) THEN
            BREAK;
        END IF;

        UPDATE reviews
        SET sentiment = SNOWFLAKE.CORTEX.COMPLETE(
            'mistral-7b',
            CONCAT('Classify as positive/negative/neutral: ', review_text)
        )
        WHERE review_id IN (
            SELECT review_id FROM reviews WHERE sentiment IS NULL LIMIT :batch_size
        );

        total_processed := total_processed + batch_count;
    END LOOP;
    RETURN 'Processed ' || total_processed || ' reviews';
END;
$$;
```

### Pattern 2: Semantic Search with EMBED

```sql
-- One-time: generate embeddings
CREATE TABLE doc_embeddings AS
SELECT doc_id, content,
    SNOWFLAKE.CORTEX.EMBED('e5-base-v2', content) AS embedding
FROM documents;

-- Search function
CREATE OR REPLACE FUNCTION semantic_search(query STRING, top_k INT DEFAULT 5)
RETURNS TABLE (doc_id STRING, content STRING, score FLOAT)
AS $$
    SELECT doc_id, content,
        VECTOR_COSINE_SIMILARITY(
            embedding,
            SNOWFLAKE.CORTEX.EMBED('e5-base-v2', query)
        ) AS score
    FROM doc_embeddings
    ORDER BY score DESC
    LIMIT top_k
$$;
```

### Pattern 3: Environment-Aware Connection

```python
import os
from snowflake.snowpark import Session

def get_session(env: str = "dev") -> Session:
    """Create a Snowpark session using JWT auth from environment variables."""
    return Session.builder.configs({
        "account": os.environ[f"SNOWFLAKE_{env.upper()}_ACCOUNT"],
        "user": os.environ.get("SNOWFLAKE_USER", "SVC_DEPLOY"),
        "private_key_file": os.environ.get("SNOWFLAKE_PRIVATE_KEY_PATH", "/tmp/snowflake_key.p8"),
        "authenticator": "SNOWFLAKE_JWT",
        "warehouse": os.environ.get("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
        "database": os.environ.get("SNOWFLAKE_DATABASE", "APP_DB"),
        "schema": os.environ.get("SNOWFLAKE_SCHEMA", "PUBLIC"),
        "role": os.environ.get("SNOWFLAKE_ROLE", "DEPLOY_ROLE"),
    }).create()
```

---

## Tips for Using This Skill

1. **Start with connection setup**: Always verify `snow connection test` before writing SQL
2. **Use JWT for everything automated**: Passwords are for humans; keys are for machines
3. **Right-size warehouses**: Run `SHOW WAREHOUSES` and review `ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY`
4. **Test Cortex models**: Try `mistral-7b` first for speed, upgrade to `mistral-large2` if quality is insufficient
5. **Clone before migrating**: `CREATE DATABASE ... CLONE` is instant and free until data diverges
6. **Monitor costs early**: Set resource monitors on day one, not after the first bill
7. **Use streams + tasks for CDC**: Avoid polling patterns; let Snowflake track changes natively
8. **Validate Native Apps locally**: Always `snow app run` before creating a version for Marketplace
