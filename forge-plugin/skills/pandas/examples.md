# pandas Examples

## Usage Scenarios

This document provides practical examples of using the `pandas` skill in various contexts.

---

## Example 1: Data Cleaning and ETL Pipeline

### Scenario
You have a messy CSV export from a legacy CRM system with inconsistent formatting, missing values, and duplicate records. You need to clean it and load it into a PostgreSQL database.

### User Request
```
Please use skill:pandas to clean our CRM export (crm_customers.csv) and prepare it for loading into PostgreSQL.
```

### Skill Workflow

**Step 1**: Data Identification
- Identifies CSV file with ~500K rows, 28 columns
- Target: PostgreSQL `customers` table
- Key issues: mixed date formats, duplicate emails, inconsistent state abbreviations

**Step 2**: Socratic Questions
```
I've located the CRM export file. Before proceeding:

1. Are there specific columns that are required (non-nullable) in the target database?
2. How should duplicate customers be handled — keep first, last, or merge?
3. Are there known data quality issues (e.g., test records, bad emails)?
4. What date format does the source system use (MM/DD/YYYY, YYYY-MM-DD, mixed)?
5. Should I preserve the original data alongside the cleaned version?
```

**User Response**:
```
1. email, first_name, last_name, and created_date are required
2. Keep the most recent record by updated_date
3. Rows with email containing "test" or "@example.com" are test data
4. Mixed — some MM/DD/YYYY, some YYYY-MM-DD
5. Yes, keep a raw copy before transformations
```

**Step 3**: Data Profiling
```python
import pandas as pd
import numpy as np

df = pd.read_csv('crm_customers.csv', low_memory=False)

print(f"Shape: {df.shape}")           # (487_231, 28)
print(f"Memory: {df.memory_usage(deep=True).sum() / 1e6:.1f} MB")  # 312.4 MB
print(f"Duplicates: {df.duplicated(subset=['email']).sum()}")       # 12,847
print(f"Null summary:\n{df.isnull().sum().sort_values(ascending=False).head(10)}")

# Key findings:
# - phone: 34% null
# - state: 8% null, 47 unique values (should be 50 + DC)
# - created_date: mixed formats, 0.2% unparseable
# - email: 12,847 duplicates, 523 test records
```

**Step 4**: Cleaning Pipeline
```python
def clean_crm_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean CRM customer data for database loading."""
    raw = df.copy()

    # 1. Remove test records
    test_mask = (
        df['email'].str.contains(r'test|@example\.com', case=False, na=False)
    )
    df = df[~test_mask]

    # 2. Parse dates with mixed formats
    df['created_date'] = pd.to_datetime(
        df['created_date'], format='mixed', dayfirst=False, errors='coerce'
    )
    df['updated_date'] = pd.to_datetime(
        df['updated_date'], format='mixed', dayfirst=False, errors='coerce'
    )

    # 3. Drop rows missing required fields
    required = ['email', 'first_name', 'last_name', 'created_date']
    df = df.dropna(subset=required)

    # 4. Normalize strings
    df['email'] = df['email'].str.strip().str.lower()
    df['first_name'] = df['first_name'].str.strip().str.title()
    df['last_name'] = df['last_name'].str.strip().str.title()
    df['state'] = df['state'].str.strip().str.upper()

    # 5. Deduplicate — keep most recent by updated_date
    df = (
        df.sort_values('updated_date', ascending=False)
          .drop_duplicates(subset=['email'], keep='first')
    )

    # 6. Standardize state abbreviations
    state_map = {'CALIFORNIA': 'CA', 'NEW YORK': 'NY', 'TEXAS': 'TX'}
    df['state'] = df['state'].replace(state_map)
    valid_states = [
        'AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL',
        'IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT',
        'NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI',
        'SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY','DC',
    ]
    df.loc[~df['state'].isin(valid_states), 'state'] = np.nan

    # 7. Downcast numerics for memory efficiency
    for col in df.select_dtypes(include=['int64']).columns:
        df[col] = pd.to_numeric(df[col], downcast='integer')
    for col in df.select_dtypes(include=['float64']).columns:
        df[col] = pd.to_numeric(df[col], downcast='float')

    return df

df_clean = clean_crm_data(df)
print(f"Cleaned: {df_clean.shape[0]} rows ({df.shape[0] - df_clean.shape[0]} removed)")
```

**Step 5**: Load to Database and Report
```python
from sqlalchemy import create_engine

engine = create_engine('postgresql://user:pass@host/dbname')
df_clean.to_sql('customers', engine, if_exists='replace', index=False, method='multi')
print(f"Loaded {len(df_clean)} rows to PostgreSQL")
```

```markdown
# CRM Data Cleaning Report

## Summary
- **Input**: 487,231 rows, 28 columns (312.4 MB)
- **Output**: 471,502 rows, 28 columns (198.7 MB)
- **Removed**: 15,729 rows (523 test, 12,847 duplicates, 2,359 missing required)

## Transformations Applied
1. Removed 523 test records (email pattern filter)
2. Parsed mixed-format dates (coerced 973 unparseable to NaT)
3. Dropped 2,359 rows missing required fields
4. Normalized strings (trim, case standardization)
5. Deduplicated by email (kept most recent)
6. Standardized 47 → 51 valid state codes
7. Downcasted numerics (saved 113.7 MB)
```

---

## Example 2: Advanced Aggregation and Pivot Analysis

### Scenario
You have e-commerce transaction data and need to produce a monthly sales report with pivot tables, year-over-year comparisons, and rolling averages.

### User Request
```
Analyze our sales transactions (2 years of data, ~3M rows) and create monthly aggregations with YoY trends.
```

### Skill Workflow

**Step 1**: Data Identification
- Parquet file with 3.1M rows, 14 columns
- Date range: 2024-01-01 to 2025-12-31
- Key columns: order_date, product_category, region, revenue, quantity

**Step 2**: Context and Memory Loading
- Loads project memory for prior analysis patterns
- Loads Python context for best practices

**Step 3**: Data Profiling
```python
df = pd.read_parquet('sales_transactions.parquet')
print(f"Shape: {df.shape}")           # (3_102_487, 14)
print(f"Date range: {df['order_date'].min()} to {df['order_date'].max()}")
print(f"Categories: {df['product_category'].nunique()}")  # 12
print(f"Regions: {df['region'].nunique()}")                # 5
print(f"Total revenue: ${df['revenue'].sum():,.2f}")       # $284,391,502.37
```

**Step 4**: Aggregation and Analysis
```python
# 1. Monthly revenue summary
df['order_month'] = df['order_date'].dt.to_period('M')
monthly = (
    df.groupby('order_month')
      .agg(
          total_revenue=('revenue', 'sum'),
          total_orders=('order_id', 'nunique'),
          avg_order_value=('revenue', 'mean'),
          total_quantity=('quantity', 'sum'),
      )
      .reset_index()
)
monthly['order_month'] = monthly['order_month'].dt.to_timestamp()

# 2. Year-over-year comparison
monthly['year'] = monthly['order_month'].dt.year
monthly['month'] = monthly['order_month'].dt.month
yoy = monthly.pivot_table(
    index='month',
    columns='year',
    values='total_revenue',
    aggfunc='sum',
)
yoy['yoy_change_pct'] = ((yoy[2025] - yoy[2024]) / yoy[2024] * 100).round(1)

# 3. Category × Region pivot table
category_region = pd.pivot_table(
    df,
    index='product_category',
    columns='region',
    values='revenue',
    aggfunc='sum',
    margins=True,
    margins_name='Total',
).round(2)

# 4. Rolling 3-month average
monthly = monthly.sort_values('order_month')
monthly['rolling_3m_revenue'] = (
    monthly['total_revenue'].rolling(window=3, min_periods=1).mean()
)

# 5. Top products by category
top_products = (
    df.groupby(['product_category', 'product_name'])
      .agg(revenue=('revenue', 'sum'), quantity=('quantity', 'sum'))
      .reset_index()
      .sort_values(['product_category', 'revenue'], ascending=[True, False])
      .groupby('product_category')
      .head(5)
)
```

**Step 5**: Report Output
```markdown
# Monthly Sales Analysis Report

## Year-over-Year Revenue Comparison

| Month | 2024 Revenue | 2025 Revenue | YoY Change |
|-------|-------------|-------------|------------|
| Jan   | $10.2M      | $11.8M      | +15.7%     |
| Feb   | $9.8M       | $11.1M      | +13.3%     |
| Mar   | $11.5M      | $13.2M      | +14.8%     |
| ...   | ...         | ...         | ...        |
| Dec   | $14.1M      | $16.3M      | +15.6%     |

## Category × Region Pivot

| Category    | East    | West    | Central | South   | Total   |
|-------------|---------|---------|---------|---------|---------|
| Electronics | $22.4M  | $19.8M  | $15.2M  | $12.1M  | $69.5M  |
| Apparel     | $18.3M  | $21.1M  | $11.7M  | $9.4M   | $60.5M  |
| ...         | ...     | ...     | ...     | ...     | ...     |

## Key Insights
1. Consistent 13-16% YoY growth across all months
2. West region leads in Apparel; East leads in Electronics
3. Q4 spike driven by Electronics (+22% vs Q3)
4. Rolling 3-month average smooths seasonal volatility
```

---

## Example 3: Performance Optimization for Large Datasets

### Scenario
An existing pandas pipeline processes a 15GB log file and runs out of memory. You need to optimize it to run on a machine with 16GB RAM.

### User Request
```
Our log processing pipeline crashes with MemoryError on a 15GB CSV. Help optimize it to run on 16GB RAM.
```

### Skill Workflow

**Step 1**: Identify Constraints
- Source: 15GB CSV, ~120M rows, 22 columns
- Available RAM: 16GB
- Current code loads entire file with `pd.read_csv()`
- Output: aggregated hourly metrics per service

**Step 2**: Load Memory and Context
- Reviews project memory for prior optimization patterns
- Loads Python performance context

**Step 3**: Profile Current Pipeline
```python
# Current (broken) approach — loads entire file
# df = pd.read_csv('app_logs.csv')  # MemoryError!

# Profile a sample to understand the data
sample = pd.read_csv('app_logs.csv', nrows=100_000)
print(sample.dtypes)
print(sample.memory_usage(deep=True))

# Key findings:
# - timestamp: object (should be datetime64)
# - service_name: object with 12 unique values (should be categorical)
# - log_level: object with 5 unique values (should be categorical)
# - response_time_ms: float64 (can downcast to float32)
# - request_id: object UUID (64 bytes avg — not needed for aggregation)
# - message: object (avg 200 chars — not needed for aggregation)
#
# Estimated memory for full load: ~38GB (2.4x available RAM)
```

**Step 4**: Optimized Pipeline
```python
import pandas as pd
import numpy as np

def process_logs_chunked(
    filepath: str,
    chunksize: int = 500_000,
) -> pd.DataFrame:
    """Process large log files in chunks with minimal memory usage."""

    # Only read columns needed for aggregation
    usecols = [
        'timestamp', 'service_name', 'log_level',
        'response_time_ms', 'status_code',
    ]

    # Specify dtypes upfront for memory efficiency
    dtype_spec = {
        'service_name': 'category',
        'log_level': 'category',
        'response_time_ms': 'float32',
        'status_code': 'int16',
    }

    aggregated_chunks = []

    for i, chunk in enumerate(pd.read_csv(
        filepath,
        chunksize=chunksize,
        usecols=usecols,
        dtype=dtype_spec,
        parse_dates=['timestamp'],
    )):
        # Floor timestamp to hour for aggregation
        chunk['hour'] = chunk['timestamp'].dt.floor('h')

        # Aggregate within chunk
        agg = (
            chunk.groupby(['hour', 'service_name', 'log_level'])
                 .agg(
                     request_count=('response_time_ms', 'count'),
                     avg_response_ms=('response_time_ms', 'mean'),
                     p95_response_ms=('response_time_ms', lambda x: np.percentile(x, 95)),
                     p99_response_ms=('response_time_ms', lambda x: np.percentile(x, 99)),
                     error_count=('status_code', lambda x: (x >= 500).sum()),
                 )
                 .reset_index()
        )
        aggregated_chunks.append(agg)

        if (i + 1) % 10 == 0:
            print(f"Processed {(i + 1) * chunksize:,} rows...")

    # Combine chunk aggregations and re-aggregate
    combined = pd.concat(aggregated_chunks, ignore_index=True)
    result = (
        combined.groupby(['hour', 'service_name', 'log_level'])
                .agg(
                    request_count=('request_count', 'sum'),
                    avg_response_ms=('avg_response_ms', 'mean'),
                    p95_response_ms=('p95_response_ms', 'max'),
                    p99_response_ms=('p99_response_ms', 'max'),
                    error_count=('error_count', 'sum'),
                )
                .reset_index()
                .sort_values(['hour', 'service_name'])
    )
    return result

result = process_logs_chunked('app_logs.csv')
print(f"Output: {result.shape[0]} rows, {result.memory_usage(deep=True).sum() / 1e6:.1f} MB")
```

**Additional optimization — vectorized replacement for loops:**
```python
# BEFORE: Slow iterative approach (found in existing codebase)
# for idx, row in df.iterrows():
#     if row['status_code'] >= 500:
#         df.at[idx, 'is_error'] = True

# AFTER: Vectorized — 100x faster
df['is_error'] = df['status_code'] >= 500

# BEFORE: Apply with Python function
# df['hour'] = df['timestamp'].apply(lambda x: x.replace(minute=0, second=0))

# AFTER: Vectorized datetime operation — 50x faster
df['hour'] = df['timestamp'].dt.floor('h')
```

**Step 5**: Performance Report
```markdown
# Log Pipeline Optimization Report

## Before vs After

| Metric               | Before       | After            |
|----------------------|--------------|------------------|
| Peak memory          | 38 GB (OOM)  | 1.2 GB           |
| Runtime              | N/A (crash)  | 4 min 32 sec     |
| Columns loaded       | 22           | 5                |
| Processing mode      | Full load    | Chunked (500K)   |
| Output size          | N/A          | 18,432 rows      |

## Optimizations Applied
1. **Column selection**: 22 → 5 columns (usecols) — 77% memory reduction
2. **Dtype specification**: category + float32 — 60% reduction on loaded columns
3. **Chunked processing**: 500K rows per chunk — constant 1.2GB peak memory
4. **Pre-aggregation per chunk**: Reduces combine step memory
5. **Vectorized operations**: Replaced iterrows/apply with dt accessor — 50-100x faster

## Recommendations
1. Convert source to Parquet for 5x faster reads and 3x smaller files
2. Consider Dask for parallelized chunk processing on multi-core machines
3. Schedule pipeline during off-peak hours for consistent performance
4. Add monitoring for chunk processing times to detect data growth issues
```

---

## Common Patterns

### Pattern: Data Profiling
```
Profile this dataset — show shape, types, missing values, distributions, and quality issues
```

### Pattern: ETL Pipeline
```
Build a pandas pipeline to extract from CSV, clean, transform, and load into PostgreSQL
```

### Pattern: Aggregation Report
```
Create monthly/quarterly aggregations with year-over-year comparisons and rolling averages
```

### Pattern: Merge and Enrich
```
Join these three DataFrames on customer_id and enrich with demographic data
```

### Pattern: Performance Optimization
```
This pandas code is too slow / uses too much memory — optimize it
```

### Pattern: Time Series Analysis
```
Analyze this time series data — resample to daily, compute rolling statistics, detect trends
```

---

**Last Updated**: 2026-02-12
**Maintained by**: The Forge
