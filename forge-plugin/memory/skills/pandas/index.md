# Pandas - Project Memory System

## Purpose

This directory stores project-specific knowledge learned during pandas data manipulation and analysis sessions. Each project gets its own subdirectory containing dataset schemas, transformation patterns, and performance characteristics discovered during analysis.

## Directory Structure

```
memory/skills/pandas/
├── index.md (this file)
└── {project-name}/
    ├── data_summary.md
    ├── pipeline_patterns.md
    ├── performance_notes.md
    └── transformation_history.md
```

## Project Memory Contents

### data_summary.md
- Dataset sources and file formats
- Column inventories with data types and cardinality
- Row counts and memory footprint
- Missing value profiles per column
- Key relationships between datasets
- Data quality baseline metrics

### pipeline_patterns.md
- Cleaning steps and imputation strategies used
- Transformation sequences and rationale
- GroupBy and aggregation patterns
- Merge/join keys and validation rules
- Encoding and feature engineering approaches
- Reusable function signatures

### performance_notes.md
- Memory usage benchmarks (before/after optimization)
- Execution time for key operations
- Chunked processing configurations
- Dtype optimization mappings (e.g., float64 → float32)
- Categorical conversion candidates
- Bottleneck operations and workarounds

### transformation_history.md
- Chronological log of transformations applied
- Schema evolution (columns added, renamed, dropped)
- Filter and deduplication criteria
- Output format changes over time
- Version-to-version diffs in pipeline logic

## Memory Lifecycle

### Creation
Memory is created the FIRST time a project's data is analyzed with pandas. The project name is either:
1. Derived from the repository name
2. Specified by the user
3. Extracted from the dataset or pipeline name

### Updates
Memory is UPDATED every time the skill analyzes data for the project:
- New datasets and columns are cataloged
- Transformation patterns are refined
- Performance benchmarks are refreshed
- Pipeline changes are appended to history
- Data quality baselines are updated

### Usage
Memory is READ at the START of every analysis:
- Provides historical context on datasets
- Shows which cleaning steps have been effective
- Guides performance optimization choices
- Informs merge key selection and validation
- Ensures consistency across pipeline iterations

## Best Practices

### DO:
- ✅ Update memory after every analysis session
- ✅ Track schema evolution (new columns, type changes)
- ✅ Record performance benchmarks with dataset sizes
- ✅ Document imputation and cleaning rationale
- ✅ Note which optimizations yielded measurable gains

### DON'T:
- ❌ Store actual data rows or PII values
- ❌ Include file paths or credentials
- ❌ Copy raw DataFrames or large outputs (summarize instead)
- ❌ Store temporary exploration results
- ❌ Include environment-specific configurations (local paths, server names)

## Memory vs Context

### Context (`../../context/python/`)
- **Universal knowledge**: Applies to ALL pandas projects
- **Library patterns**: pandas idioms, NumPy integration, best practices
- **Performance guides**: Vectorization rules, memory optimization techniques
- **Static**: Updated by Forge maintainers

### Memory (this directory)
- **Project-specific**: Only for ONE project's datasets and pipelines
- **Learned patterns**: Discovered during analysis sessions
- **Historical tracking**: Schema and pipeline changes over time
- **Dynamic**: Updated by the skill automatically

## Example Memory Structure

```
ecommerce-analytics/
├── data_summary.md
│   - 4 datasets: orders.parquet, customers.csv, products.csv, sessions.json
│   - orders: 3.1M rows × 14 cols, 485 MB
│   - customers: 210K rows × 22 cols, 48 MB
│   - Key join: orders.customer_id → customers.id (validated 1:many)
│   - Missing: customers.phone 34%, orders.discount_code 78%
│   - Last profiled: 2026-02-12
│
├── pipeline_patterns.md
│   - Date parsing: format='mixed' for legacy exports
│   - Dedup strategy: sort by updated_at desc, keep='first'
│   - Revenue calc: quantity × unit_price × (1 - discount_pct)
│   - Category encoding: pd.Categorical with 12 known values
│   - Monthly aggregation: resample('ME').agg(named_aggs)
│
├── performance_notes.md
│   - orders.parquet read: 2.1s (vs 18.4s for CSV equivalent)
│   - Memory after downcast: 485 MB → 198 MB (int64→int32, float64→float32)
│   - Categorical on product_category: saved 42 MB
│   - Chunked processing not needed (fits in 8GB RAM)
│   - Bottleneck: apply() on address parsing — replaced with str accessor
│
└── transformation_history.md
    - v1 (2026-01-15): Initial ETL — CSV ingest, basic cleaning
    - v2 (2026-01-28): Added YoY aggregation, switched to Parquet
    - v3 (2026-02-12): Memory optimization, categorical encoding
```

## Security Considerations

### DO Store:
- Column names, data types, and cardinality
- Aggregation patterns and pipeline logic
- Performance benchmarks and memory metrics
- Schema evolution history
- Cleaning and transformation rationale

### DON'T Store:
- Actual data values or sample rows
- Database connection strings or API keys
- PII or sensitive field values
- Production server details
- Access credentials or tokens

## Integration with Tools

Memory can inform:
- **Pipeline frameworks**: Airflow/Prefect DAG configuration from transformation history
- **Testing tools**: Expected schemas and validation rules for unit tests
- **Monitoring**: Performance baselines for alerting on regressions
- **Documentation**: Auto-generated data dictionaries from column inventories
- **ML pipelines**: Feature engineering patterns for Scikit-learn preprocessing

---

**Memory System Version**: 1.0.0
**Last Updated**: 2026-02-12
**Maintained by**: pandas skill
