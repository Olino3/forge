# Data Science Patterns (Pandas/NumPy)

This file contains patterns and best practices for reviewing data science code using Pandas, NumPy, and related libraries.

## Pandas Performance Patterns

### Avoid iterrows() - Use Vectorization

**Anti-Pattern**:
```python
# WRONG - Very slow (100x slower than vectorized)
import pandas as pd

df = pd.DataFrame({'A': range(10000), 'B': range(10000)})

results = []
for index, row in df.iterrows():
    if row['A'] > 50:
        results.append(row['A'] * row['B'])
    else:
        results.append(0)
df['C'] = results
```

**Good Pattern**:
```python
# CORRECT - Vectorized operation (100x faster)
df['C'] = (df['A'] * df['B']).where(df['A'] > 50, 0)

# Alternative with numpy.where
import numpy as np
df['C'] = np.where(df['A'] > 50, df['A'] * df['B'], 0)

# Alternative with loc
df['C'] = 0
df.loc[df['A'] > 50, 'C'] = df['A'] * df['B']
```

### Avoid apply() When Possible

**Anti-Pattern**:
```python
# SLOW - apply() with lambda
df['total'] = df.apply(lambda row: row['price'] * row['quantity'], axis=1)

# SLOW - String operations with apply
df['upper_name'] = df['name'].apply(lambda x: x.upper())
```

**Good Pattern**:
```python
# FAST - Direct vectorized operation
df['total'] = df['price'] * df['quantity']

# FAST - Built-in string methods
df['upper_name'] = df['name'].str.upper()

# When apply() is necessary, use raw=True for numpy arrays
df['result'] = df.apply(lambda x: custom_function(x), axis=1, raw=True)
```

### Use Categorical Data Types

**Anti-Pattern**:
```python
# WRONG - String/object dtype uses too much memory
df = pd.DataFrame({
    'category': ['A', 'B', 'A', 'C', 'B', 'A'] * 10000  # Stores each string
})
# Memory: ~600 KB
```

**Good Pattern**:
```python
# CORRECT - Categorical dtype (much less memory)
df = pd.DataFrame({
    'category': pd.Categorical(['A', 'B', 'A', 'C', 'B', 'A'] * 10000)
})
# Memory: ~60 KB (10x reduction)

# Convert existing column
df['category'] = df['category'].astype('category')

# Check memory usage
print(df.memory_usage(deep=True))
```

---

## Data Loading and I/O

### Efficient CSV Reading

**Anti-Pattern**:
```python
# WRONG - Loads entire file into memory
df = pd.read_csv('large_file.csv')  # OOM for large files!
```

**Good Pattern**:
```python
# CORRECT - Specify dtypes to reduce memory
dtypes = {
    'user_id': 'int32',  # int64 by default
    'category': 'category',
    'price': 'float32',  # float64 by default
}
df = pd.read_csv('large_file.csv', dtype=dtypes)

# CORRECT - Read in chunks for very large files
chunk_size = 10000
chunks = []
for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    processed = process_chunk(chunk)
    chunks.append(processed)
df = pd.concat(chunks, ignore_index=True)

# CORRECT - Use usecols to read only needed columns
df = pd.read_csv('file.csv', usecols=['user_id', 'timestamp', 'value'])

# CORRECT - Parse dates during load
df = pd.read_csv('file.csv', parse_dates=['timestamp'])
```

### Efficient Data Export

**Good Pattern**:
```python
# For large datasets, use parquet (compressed, columnar)
df.to_parquet('data.parquet', compression='snappy', index=False)

# Reading parquet (much faster than CSV)
df = pd.read_parquet('data.parquet')

# For CSV, disable index if not needed
df.to_csv('data.csv', index=False)

# Use compression
df.to_csv('data.csv.gz', compression='gzip', index=False)
```

---

## DataFrame Operations

### Chaining Methods

**Good Pattern**:
```python
# READABLE - Method chaining with line breaks
result = (df
    .query('age > 18')
    .groupby('category')
    ['sales']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

# Use assign() for new columns in chains
result = (df
    .assign(
        total=lambda x: x['price'] * x['quantity'],
        discount=lambda x: x['total'] * 0.1
    )
    .query('total > 100')
)
```

### Copy vs View

**Anti-Pattern**:
```python
# WRONG - SettingWithCopyWarning
subset = df[df['age'] > 18]
subset['category'] = 'adult'  # May or may not modify df!
```

**Good Pattern**:
```python
# CORRECT - Explicit copy
subset = df[df['age'] > 18].copy()
subset['category'] = 'adult'  # Safe

# CORRECT - Use loc for modifications
df.loc[df['age'] > 18, 'category'] = 'adult'
```

### Merging and Joining

**Anti-Pattern**:
```python
# WRONG - Multiple sequential merges (slow)
result = df1.merge(df2, on='id')
result = result.merge(df3, on='id')
result = result.merge(df4, on='id')
```

**Good Pattern**:
```python
# CORRECT - Merge multiple at once with reduce
from functools import reduce

dfs = [df1, df2, df3, df4]
result = reduce(lambda left, right: pd.merge(left, right, on='id'), dfs)

# CORRECT - Use appropriate merge type
# Inner join (default)
df1.merge(df2, on='id', how='inner')

# Left join (keep all from df1)
df1.merge(df2, on='id', how='left')

# Validate merge to catch errors
df1.merge(df2, on='id', validate='one_to_one')  # Ensures no duplicates
```

---

## GroupBy Operations

### Efficient Aggregation

**Anti-Pattern**:
```python
# WRONG - Slow apply with custom function
df.groupby('category').apply(lambda x: x['sales'].sum())
```

**Good Pattern**:
```python
# CORRECT - Use built-in aggregation
df.groupby('category')['sales'].sum()

# Multiple aggregations
df.groupby('category').agg({
    'sales': ['sum', 'mean', 'count'],
    'profit': 'sum',
    'quantity': 'max'
})

# Named aggregations (Pandas 0.25+)
df.groupby('category').agg(
    total_sales=('sales', 'sum'),
    avg_price=('price', 'mean'),
    num_transactions=('id', 'count')
)

# Custom aggregation only when necessary
df.groupby('category')['sales'].agg(
    lambda x: x.quantile(0.95)
)
```

### Transform vs Apply

**Good Pattern**:
```python
# Use transform() to broadcast results back to original shape
df['sales_pct_of_category'] = (
    df['sales'] / df.groupby('category')['sales'].transform('sum')
)

# Use apply() for operations that change the shape
category_stats = df.groupby('category').apply(
    lambda x: pd.Series({
        'mean': x['sales'].mean(),
        'std': x['sales'].std(),
        'count': len(x)
    })
)
```

---

## Memory Optimization

### Downcast Numeric Types

**Good Pattern**:
```python
# Check current memory usage
print(df.memory_usage(deep=True).sum() / 1024**2, "MB")

# Downcast integers
df['user_id'] = pd.to_numeric(df['user_id'], downcast='integer')

# Downcast floats
df['price'] = pd.to_numeric(df['price'], downcast='float')

# Function to optimize all numeric columns
def optimize_dtypes(df):
    for col in df.select_dtypes(include=['int']).columns:
        df[col] = pd.to_numeric(df[col], downcast='integer')

    for col in df.select_dtypes(include=['float']).columns:
        df[col] = pd.to_numeric(df[col], downcast='float')

    for col in df.select_dtypes(include=['object']).columns:
        if df[col].nunique() / len(df) < 0.5:  # Less than 50% unique
            df[col] = df[col].astype('category')

    return df

df = optimize_dtypes(df)
print(df.memory_usage(deep=True).sum() / 1024**2, "MB")
```

---

## NumPy Patterns

### Vectorization

**Anti-Pattern**:
```python
# WRONG - Python loop (very slow)
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
result = []
for x in arr:
    result.append(x ** 2 + 2 * x + 1)
result = np.array(result)
```

**Good Pattern**:
```python
# CORRECT - Vectorized operation (100x faster)
result = arr ** 2 + 2 * arr + 1

# CORRECT - Use numpy functions
result = np.sqrt(arr)
result = np.exp(arr)
result = np.sin(arr)
```

### Broadcasting

**Good Pattern**:
```python
# Add scalar to array
arr = np.array([1, 2, 3])
result = arr + 10  # [11, 12, 13]

# Matrix + row vector
matrix = np.array([[1, 2, 3], [4, 5, 6]])
row = np.array([10, 20, 30])
result = matrix + row  # Broadcasting happens automatically

# Matrix + column vector
col = np.array([[10], [20]])
result = matrix + col
```

### Efficient Array Operations

**Anti-Pattern**:
```python
# WRONG - Growing arrays in loop
result = np.array([])
for i in range(1000):
    result = np.append(result, i)  # Creates new array each time!
```

**Good Pattern**:
```python
# CORRECT - Preallocate array
result = np.zeros(1000)
for i in range(1000):
    result[i] = compute_value(i)

# BETTER - Use vectorization or list comprehension + conversion
result = np.array([compute_value(i) for i in range(1000)])

# BEST - Fully vectorized if possible
indices = np.arange(1000)
result = compute_value_vectorized(indices)
```

---

## Data Cleaning Patterns

### Handling Missing Values

**Good Pattern**:
```python
# Check for missing values
print(df.isnull().sum())
print(df.isnull().sum() / len(df) * 100)  # Percentage

# Drop rows with any missing values
df_clean = df.dropna()

# Drop rows where specific columns are missing
df_clean = df.dropna(subset=['important_column'])

# Fill missing values
df['age'].fillna(df['age'].median(), inplace=True)
df['category'].fillna('Unknown', inplace=True)

# Forward/backward fill
df['value'].fillna(method='ffill', inplace=True)

# Interpolate
df['value'].interpolate(method='linear', inplace=True)
```

### Handling Duplicates

**Good Pattern**:
```python
# Check for duplicates
print(f"Duplicates: {df.duplicated().sum()}")

# Drop duplicates
df_clean = df.drop_duplicates()

# Drop duplicates based on specific columns
df_clean = df.drop_duplicates(subset=['user_id', 'timestamp'])

# Keep last occurrence instead of first
df_clean = df.drop_duplicates(subset=['user_id'], keep='last')
```

### Data Type Conversions

**Good Pattern**:
```python
# Convert to datetime
df['date'] = pd.to_datetime(df['date'])
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

# Handle errors during conversion
df['date'] = pd.to_datetime(df['date'], errors='coerce')  # Invalid -> NaT

# Convert to numeric
df['value'] = pd.to_numeric(df['value'], errors='coerce')  # Invalid -> NaN

# Extract datetime components
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day_of_week'] = df['date'].dt.dayofweek
```

---

## Common Anti-Patterns to Flag

### Pandas
- [ ] Using iterrows() instead of vectorization
- [ ] Using apply() when built-in methods exist
- [ ] Not specifying dtypes when reading CSV
- [ ] Loading entire large files into memory
- [ ] Using object dtype for categorical data
- [ ] Chained indexing (df[condition][column] = value)
- [ ] Growing DataFrames in loop (append in loop)
- [ ] Not using copy() when needed
- [ ] Multiple sequential merges instead of reduce
- [ ] Using apply() for simple operations

### NumPy
- [ ] Growing arrays in loops with append
- [ ] Python loops instead of vectorization
- [ ] Not using broadcasting
- [ ] Creating unnecessary copies
- [ ] Using lists instead of arrays for numeric data

### Performance
- [ ] Reading full dataset when only subset needed
- [ ] Not using categorical dtype for low-cardinality strings
- [ ] Not downcasting numeric types
- [ ] Using CSV when parquet would be better
- [ ] Not processing data in chunks for large files

## Performance Optimization Checklist

1. **Use vectorized operations** instead of loops
2. **Use appropriate dtypes** (categorical, int32 instead of int64)
3. **Read only necessary columns** with usecols
4. **Process large files in chunks**
5. **Use parquet format** for storage
6. **Avoid chained indexing** (use loc/iloc)
7. **Use query()** for complex filters
8. **Cache expensive computations**
9. **Use numba or cython** for custom operations that can't be vectorized
10. **Profile code** with %timeit in Jupyter or cProfile

## Useful Pandas Functions Often Overlooked

```python
# query() - SQL-like filtering
df.query('age > 18 and city == "NYC"')

# eval() - Efficient column operations
df.eval('total = price * quantity')

# pipe() - Chain custom functions
df.pipe(remove_outliers).pipe(normalize).pipe(add_features)

# assign() - Add columns in method chains
df.assign(total=lambda x: x['price'] * x['quantity'])

# explode() - Expand list-like column
df.explode('tags')

# melt() - Wide to long format
df.melt(id_vars=['id'], value_vars=['jan', 'feb', 'mar'])

# pivot_table() - Long to wide with aggregation
df.pivot_table(values='sales', index='date', columns='category', aggfunc='sum')
```

## References

- Pandas Documentation: https://pandas.pydata.org/docs/
- NumPy Documentation: https://numpy.org/doc/
- Pandas Performance: https://pandas.pydata.org/docs/user_guide/enhancingperf.html
- Effective Pandas by Matt Harrison
- Python for Data Analysis by Wes McKinney
