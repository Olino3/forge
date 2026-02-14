---
name: pandas
## description: Advanced data manipulation and analysis with pandas. Provides expert guidance on DataFrame operations, data cleaning, ETL pipelines, aggregation, merging, reshaping, time series analysis, and performance optimization. Supports integration with NumPy, Matplotlib, Scikit-learn, and SQL databases. Use for data profiling, transformation workflows, large dataset handling, and analytical reporting.

# Pandas Data Manipulation Expert

### Step 1: Initial Analysis

Gather inputs and understand the task:
- Determine project scope and requirements
- Identify target files or components
- Clarify user objectives and constraints

### Step 2: Generate Output

Create deliverables and save to `/claudedocs/`:
- Follow OUTPUT_CONVENTIONS.md naming: `pandas_{project}_{YYYY-MM-DD}.md`
- Include all required sections
- Provide clear, actionable recommendations

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: The 5-step workflow outlined in this document MUST be followed in exact order for EVERY pandas analysis or transformation task. Skipping steps or deviating from the procedure will result in incomplete and unreliable analysis. This is non-negotiable.

## File Structure

- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: Analysis and transformation scenarios with code examples
- **Context**: Python and data analysis patterns loaded via `contextProvider.getDomainIndex("python")`. See [ContextProvider Interface](../../interfaces/context_provider.md).
- **Memory**: Project-specific memory accessed via `memoryStore.getSkillMemory("pandas", "{project-name}")`. See [MemoryStore Interface](../../interfaces/memory_store.md).

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Focus Areas

Pandas data manipulation covers 8 critical dimensions:

1. **Data Ingestion**: Reading CSV, Excel, Parquet, JSON, SQL, HDF5, and streaming sources
2. **Data Profiling**: Shape, dtypes, missing values, cardinality, distributions, summary statistics
3. **Data Cleaning**: Handling nulls, duplicates, type coercion, string normalization, outlier detection
4. **Transformation**: Column operations, apply/map, vectorized transforms, categorical encoding, feature engineering
5. **Aggregation & Grouping**: GroupBy, pivot tables, cross-tabulations, rolling/expanding windows, resampling
6. **Merging & Reshaping**: Joins, concatenation, melt/pivot, stack/unstack, MultiIndex operations
7. **Performance Optimization**: Vectorization, chunked processing, memory reduction (downcasting, categoricals), query/eval
8. **Time Series Analysis**: DatetimeIndex, resampling, shifting, rolling statistics, period conversion

---

## Purpose

[TODO: Add purpose description]


## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Identify Target Data and Task (REQUIRED)

**YOU MUST:**
1. Ask the user about their data and goals:
   - Data sources (CSV files, databases, APIs, in-memory objects)
   - Data volume (row count, column count, file size)
   - File format and encoding details
   - Specific columns or fields of interest
   - Desired output format (DataFrame, CSV, database table, visualization)
2. Clarify the task:
   - Data cleaning / ETL pipeline?
   - Exploratory analysis / profiling?
   - Aggregation / reporting?
   - Merging multiple datasets?
   - Performance optimization of existing code?
   - Time series analysis?
3. Identify constraints:
   - Memory limits (can the data fit in RAM?)
   - Performance requirements (latency, throughput)
   - pandas version and Python version
   - Downstream consumers (dashboards, ML models, exports)

**DO NOT PROCEED WITHOUT IDENTIFYING TARGET DATA AND TASK**

### ⚠️ STEP 2: Load Project Memory & Context (REQUIRED)

**YOU MUST:**
1. **CHECK PROJECT MEMORY FIRST**:
   - Identify the project name from the repository root or ask the user
   - Use `memoryStore.getSkillMemory("pandas", "{project-name}")` to load existing project memory. See [MemoryStore Interface](../../interfaces/memory_store.md).
   - If memory exists, review previously analyzed datasets, transformation patterns, and project-specific context
   - If no memory exists, you will create it later in this process

2. **USE CONTEXT INDEXES FOR EFFICIENT LOADING**:
   - Use `contextProvider.getDomainIndex("python")` to discover available Python context files. See [ContextProvider Interface](../../interfaces/context_provider.md).
   - Use `contextProvider.getAlwaysLoadFiles("python")` to load foundational Python patterns
   - Use `contextProvider.getConditionalContext("python", detection)` to load data-analysis-specific patterns
   - If analyzing ML integration, use `contextProvider.getCrossDomainContext("python", {"data-science": true})` for ML context

3. **Ask clarifying questions** in Socratic format:
   - What is the ultimate goal of this data manipulation?
   - Will this be a one-off analysis or a recurring pipeline?
   - Are there data quality issues you are already aware of?
   - What does the downstream consumption look like?
   - Are there performance bottlenecks in existing code?
   - Do you need reproducibility (fixed random seeds, versioned outputs)?

**DO NOT PROCEED WITHOUT COMPLETING THIS STEP**

### ⚠️ STEP 3: Data Exploration and Profiling (REQUIRED)

**YOU MUST:**
1. **Profile the dataset**:
   ```python
   df.shape               # rows × columns
   df.dtypes              # column data types
   df.info(memory_usage='deep')  # memory footprint
   df.describe(include='all')    # summary statistics
   df.isnull().sum()      # missing value counts
   df.duplicated().sum()  # duplicate row count
   df.nunique()           # cardinality per column
   ```

2. **Assess data quality**:
   - Identify columns with high null percentages
   - Detect mixed types within columns
   - Flag potential parsing issues (dates stored as strings, numeric strings)
   - Check for inconsistent categorical values (whitespace, casing)
   - Identify outliers using IQR or z-score methods

3. **Document initial findings**:
   - Total rows, columns, and memory usage
   - Data type distribution (numeric, categorical, datetime, text)
   - Missing value summary with imputation recommendations
   - Cardinality analysis for categorical columns
   - Distribution shape for numeric columns

**DO NOT PROCEED WITHOUT PROFILING THE DATA**

### ⚠️ STEP 4: Deep Analysis and Transformation (REQUIRED)

**YOU MUST perform analysis and transformation covering ALL relevant aspects:**

#### 4.1 Data Cleaning
- **Handle missing values**: dropna, fillna (forward/backward fill, interpolation, mean/median/mode)
- **Remove duplicates**: `drop_duplicates()` with subset and keep strategy
- **Fix data types**: `astype()`, `pd.to_datetime()`, `pd.to_numeric(errors='coerce')`
- **Normalize strings**: `.str.strip()`, `.str.lower()`, regex replacements
- **Handle outliers**: Capping, winsorization, removal with documented thresholds

#### 4.2 Transformation and Feature Engineering
- **Column operations**: Vectorized arithmetic, `np.where()`, `pd.cut()`, `pd.qcut()`
- **Apply and map**: `.apply()` vs vectorized alternatives, `.map()` for lookups
- **Encoding**: One-hot (`pd.get_dummies()`), label encoding, ordinal encoding
- **Date features**: Extract year, month, day, weekday, quarter from datetime columns
- **Custom transforms**: Lambda functions, `pipe()` for method chaining

#### 4.3 Aggregation and Grouping
- **GroupBy operations**: `groupby().agg()` with named aggregations
- **Pivot tables**: `pd.pivot_table()` with margins and custom aggfuncs
- **Cross-tabulations**: `pd.crosstab()` for frequency analysis
- **Window functions**: `rolling()`, `expanding()`, `ewm()` for moving statistics
- **Resampling**: Time-based aggregation with `resample()`

#### 4.4 Merging and Reshaping
- **Joins**: `pd.merge()` with how='inner/left/right/outer', validate parameter
- **Concatenation**: `pd.concat()` along axis 0 (rows) or axis 1 (columns)
- **Reshape**: `melt()` for wide-to-long, `pivot()` for long-to-wide
- **MultiIndex**: `set_index()`, `reset_index()`, `stack()`, `unstack()`
- **Merge validation**: Check for unexpected row multiplication, key uniqueness

#### 4.5 Performance Optimization
- **Vectorization**: Replace loops with vectorized pandas/NumPy operations
- **Memory optimization**: Downcast numerics, convert to categoricals, use sparse types
- **Chunked processing**: `pd.read_csv(chunksize=...)` for out-of-core workflows
- **Query optimization**: `df.query()` and `df.eval()` for expression evaluation
- **Copy avoidance**: Use `inplace` judiciously, chain with `.pipe()`
- **Alternative backends**: Consider Polars, Dask, or Modin for very large datasets

**DO NOT PROCEED WITHOUT COMPREHENSIVE ANALYSIS**

### ⚠️ STEP 5: Generate Report and Update Memory (REQUIRED)

**YOU MUST:**

1. **Generate analysis report** including:
   - Data summary (shape, types, quality metrics)
   - Transformation pipeline documentation
   - Code snippets with explanations
   - Performance benchmarks (before/after if optimizing)
   - Visualization recommendations

2. **Provide production-ready code**:
   - Clean, well-commented pandas code
   - Error handling for edge cases
   - Type hints and docstrings
   - Logging for pipeline steps

3. **UPDATE PROJECT MEMORY**:
   - Use `memoryStore.update(layer="skill-specific", skill="pandas", project="{project-name}", ...)` to store:
   - Dataset schemas and column inventories
   - Cleaning and transformation patterns used
   - Performance characteristics and bottlenecks
   - Pipeline configurations and parameters
   - Timestamps and staleness tracking are handled automatically by MemoryStore. See [MemoryStore Interface](../../interfaces/memory_store.md).

4. **Provide actionable recommendations**:
   - Prioritized list of data quality improvements
   - Performance optimization opportunities
   - Pipeline architecture suggestions
   - Testing and validation strategies

**MEMORY UPDATE IS MANDATORY - DO NOT SKIP**

---

## Output Requirements

### Analysis Report Must Include:

1. **Data Overview**
   - Source format and size
   - Row and column counts
   - Memory usage before and after optimization

2. **Data Quality Assessment**
   - Missing value analysis per column
   - Duplicate detection results
   - Type consistency report
   - Outlier summary

3. **Transformation Pipeline**
   - Step-by-step transformation code
   - Rationale for each operation
   - Before/after comparisons

4. **Aggregation Results**
   - Summary statistics
   - GroupBy outputs
   - Pivot tables or cross-tabulations

5. **Performance Metrics**
   - Execution time benchmarks
   - Memory usage comparisons
   - Scalability assessment

6. **Code Artifacts**
   - Reusable functions and pipelines
   - Configuration parameters
   - Test cases for validation

---

## Socratic Prompting Guidelines

When interacting with users, ask clarifying questions such as:

**Understanding Intent:**
- "What decisions will this analysis inform?"
- "Is this a one-off exploration or a recurring ETL pipeline?"
- "Who consumes the output — analysts, ML models, dashboards?"

**Data Understanding:**
- "How many rows and columns are in your dataset?"
- "What percentage of missing values is acceptable for your use case?"
- "Are there natural keys or identifiers in the data?"
- "What time granularity do you need (daily, hourly, per-event)?"

**Technical Constraints:**
- "How much memory is available on your target environment?"
- "Do you need to process the data in chunks or can it fit in RAM?"
- "What pandas version are you using? Any plans to upgrade?"
- "Are there downstream schema requirements for the output?"

**Quality Standards:**
- "Do you have a data dictionary or schema specification?"
- "Are there known data quality issues I should watch for?"
- "What validation rules apply to the output?"

---

## Quality Standards

### Your analysis MUST:
- ✅ Profile the dataset **completely** before transformation
- ✅ Use **vectorized operations** over loops wherever possible
- ✅ Handle **missing values** explicitly with documented strategy
- ✅ Validate **merge results** to prevent silent row duplication
- ✅ Document **data type choices** and casting rationale
- ✅ Provide **memory-efficient** solutions for large datasets
- ✅ Include **error handling** for production pipelines
- ✅ Update **project memory** for future reference

### Your analysis MUST NOT:
- ❌ Use iterative row-by-row processing when vectorized alternatives exist
- ❌ Ignore missing values or silently drop rows without documentation
- ❌ Produce code with SettingWithCopyWarning or chained indexing
- ❌ Merge DataFrames without validating key uniqueness
- ❌ Hardcode file paths or environment-specific configurations

---

## Integration with Other Skills

**Combine with:**
- `python-code-review`: For reviewing pandas pipeline code quality and style
- `generate-python-unit-tests`: To create tests for transformation functions
- `python-dependency-management`: For managing pandas, NumPy, and related packages
- `database-schema-analysis`: When loading data from or writing to databases
- `file-schema-analysis`: For validating input/output file schemas (CSV, JSON, Parquet)
- `documentation-generator`: To create pipeline documentation and data dictionaries

---

## Supported Features and Libraries

### Core pandas Operations
- ✅ DataFrame and Series manipulation
- ✅ GroupBy aggregations and transforms
- ✅ Merge, join, and concatenation
- ✅ Pivot tables and cross-tabulations
- ✅ Time series and resampling
- ✅ String and categorical operations
- ✅ MultiIndex and hierarchical indexing
- ✅ Window functions (rolling, expanding, ewm)

### Integration Libraries
- ✅ NumPy — vectorized computation and array operations
- ✅ Matplotlib / Seaborn — visualization of DataFrames
- ✅ Scikit-learn — preprocessing pipelines and feature engineering
- ✅ SQLAlchemy — database read/write with `pd.read_sql()` / `df.to_sql()`
- ✅ Apache Arrow / Parquet — high-performance columnar storage
- ✅ openpyxl / xlsxwriter — Excel file I/O
- ✅ Dask / Modin — scaling pandas to larger-than-memory datasets

---

## Version History

- **v1.0.0** (2026-02-12): Initial release
  - Comprehensive pandas data manipulation workflow
  - Data profiling, cleaning, and transformation guidance
  - Performance optimization patterns (vectorization, chunking, memory reduction)
  - Integration with NumPy, Matplotlib, Scikit-learn, and SQL databases
  - Project memory integration via MemoryStore interface

---

**Last Updated**: 2026-02-12
**Maintained by**: The Forge
