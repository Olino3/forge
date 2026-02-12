# Snowflake Platform - Project Memory System

## Purpose

This directory stores project-specific knowledge learned during Snowflake platform skill sessions. Each project gets its own subdirectory containing account configurations, pipeline designs, Cortex AI patterns, Snowpark models, and Native App details discovered during implementation.

## Directory Structure

```
memory/skills/snowflake-platform/
├── index.md (this file)
└── {project-name}/
    ├── account_config.md
    ├── data_pipelines.md
    ├── cortex_patterns.md
    ├── snowpark_models.md
    └── native_apps.md
```

## Project Memory Contents

### account_config.md
- Account identifiers (ORGNAME-ACCOUNTNAME format)
- Warehouse inventory and sizing
- Role hierarchy and grants
- Connection profiles (dev, staging, prod)
- Authentication method (JWT key-pair, SSO)
- Resource monitor configurations
- Network policy settings

### data_pipelines.md
- Stream definitions and source tables
- Task schedules and WHEN conditions
- Snowpipe configurations and notification channels
- ETL data flow diagrams
- Stage definitions (internal and external)
- File format specifications
- CDC patterns in use

### cortex_patterns.md
- Model selections per use case (COMPLETE, SUMMARIZE, AI_FILTER, EMBED)
- Prompt templates with system/user message structure
- Inference parameters (temperature, max_tokens)
- Embedding strategies and vector storage tables
- Batch processing patterns and concurrency limits
- Semantic search configurations

### snowpark_models.md
- UDF registry (name, types, packages, stage location)
- Stored procedure inventory
- DataFrame transformation patterns
- Session configuration templates
- Package dependencies and Anaconda availability
- Vectorized UDF patterns

### native_apps.md
- Application package names and versions
- Manifest configuration (privileges, references)
- Setup script structure
- Streamlit UI components
- Release directives and patch levels
- Marketplace listing details
- Consumer reference patterns

## Memory Lifecycle

### Creation
Memory is created the FIRST time a project's Snowflake environment is configured. The project name is either:
1. Specified by the user
2. Derived from the repository name
3. Extracted from the Snowflake database name

### Updates
Memory is UPDATED every time the skill works with the project:
- Account configuration changes are tracked
- New pipelines and tasks are recorded
- Cortex AI patterns are refined
- Snowpark UDFs and procedures are inventoried
- Native App versions are appended
- Resource monitor adjustments are noted

### Usage
Memory is READ at the START of every session:
- Provides account and connection context
- Shows existing pipeline topology
- Guides Cortex AI model and prompt selection
- Informs Snowpark package availability
- Ensures Native App version consistency
- Prevents duplicate resource creation

## Best Practices

### DO:
- ✅ Update memory after every implementation session
- ✅ Track warehouse sizing changes and their rationale
- ✅ Document Cortex AI model choices and prompt iterations
- ✅ Record Snowpark package availability findings
- ✅ Note Native App version history and release directives
- ✅ Track resource monitor quota adjustments

### DON'T:
- ❌ Store private keys or passwords
- ❌ Include connection strings with credentials
- ❌ Copy full SQL DDL dumps (summarize instead)
- ❌ Store actual data values or PII
- ❌ Include environment-specific secrets
- ❌ Store OAuth tokens or session tokens

## Memory vs Context

### Context (`../../context/schema/`)
- **Universal knowledge**: Applies to ALL Snowflake deployments
- **Platform patterns**: SQL syntax, Cortex AI functions, Snowpark API
- **Best practices**: Industry standards, cost optimization, security
- **Static**: Updated by Forge maintainers

### Memory (this directory)
- **Project-specific**: Only for ONE Snowflake project
- **Learned patterns**: Discovered during implementation
- **Historical tracking**: Account changes, pipeline evolution, app versions
- **Dynamic**: Updated by the skill automatically

## Example Memory Structure

```
retail-analytics/
├── account_config.md
│   - Account: RETAILORG-PROD1
│   - Auth: JWT key-pair (SVC_ETL user)
│   - Warehouses: ETL_WH (SMALL), ANALYTICS_WH (MEDIUM), STREAMLIT_WH (XSMALL)
│   - Role hierarchy: ACCOUNTADMIN → SYSADMIN → ETL_ROLE, ANALYST_ROLE
│   - Resource monitors: etl_budget (500 credits), analytics_budget (300 credits)
│   - Last configured: 2025-07-14
│
├── data_pipelines.md
│   - Snowpipe: reviews_pipe (S3 → raw.product_reviews, AUTO_INGEST)
│   - Stream: product_reviews_stream (APPEND_ONLY on raw.product_reviews)
│   - Task: daily_review_summary (CRON 0 6 * * *, ETL_WH)
│   - Task: hourly_inventory_sync (5 MINUTE, ETL_WH)
│   - Flow: S3 → Snowpipe → raw → Stream → Snowpark clean → staging → Task → curated
│
├── cortex_patterns.md
│   - Sentiment classification: mistral-7b, single-word response, temp=0.1
│   - Daily summaries: SUMMARIZE on LISTAGG of review texts
│   - Product search: EMBED e5-base-v2 + VECTOR_COSINE_SIMILARITY
│   - Batch size: 1000 rows per COMPLETE call
│
├── snowpark_models.md
│   - UDF: classify_sentiment(STRING) → STRING, packages=[textblob], @etl_stage
│   - Procedure: daily_etl(Session) → STRING, permanent, @etl_stage
│   - Pattern: filter nulls → trim → length check → Cortex enrich → write
│   - Available packages verified: textblob, pandas, numpy, scikit-learn
│
└── native_apps.md
    - (none for this project)
```

## Security Considerations

### DO Store:
- Account identifiers (ORGNAME-ACCOUNTNAME)
- Warehouse names and sizes
- Role names and hierarchy
- Pipeline topology and schedules
- Cortex AI model selections and prompts
- UDF signatures and package lists
- Native App version history

### DON'T Store:
- Private keys or key file contents
- Passwords or connection credentials
- OAuth tokens or session tokens
- Actual data values or query results
- PII from any Snowflake table
- Network policy IP addresses
- Service account secrets

## Integration with Tools

Memory can inform:
- **CI/CD pipelines**: Connection profiles and deployment targets
- **Cost monitoring**: Warehouse sizing history and resource monitor baselines
- **Schema migrations**: Existing database/schema hierarchy
- **Cortex AI tuning**: Historical model performance and prompt iterations
- **Native App releases**: Version history and release directive tracking
- **Code generators**: Snowpark session config and UDF patterns

---

**Memory System Version**: 1.0.0
**Last Updated**: 2025-07-14
**Maintained by**: snowflake-platform skill
