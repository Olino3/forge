# Data Science Patterns (Pandas/NumPy)

Quick reference for reviewing data science code. For detailed examples, see official documentation.

---

## Pandas Performance Anti-Patterns

| Anti-Pattern | What to Look For | Better Approach | Learn More |
|--------------|------------------|-----------------|------------|
| **Using `iterrows()`** | `for index, row in df.iterrows():` | Use vectorized operations or `.apply()` with `raw=True` | [Pandas performance](https://pandas.pydata.org/docs/user_guide/enhancingperf.html) |
| **Unnecessary `apply()`** | `df.apply(lambda x: x['a'] * x['b'])` | Use vectorized: `df['a'] * df['b']` | [Pandas basics](https://pandas.pydata.org/docs/user_guide/basics.html) |
| **Chained indexing** | `df[df['A'] > 5]['B'] = 10` (SettingWithCopyWarning) | Use `.loc[]`: `df.loc[df['A'] > 5, 'B'] = 10` | [Indexing](https://pandas.pydata.org/docs/user_guide/indexing.html#returning-a-view-versus-a-copy) |
| **Growing DataFrames** | `df.append()` in loop | Build list, then `pd.concat()` once | [Merge/concat](https://pandas.pydata.org/docs/user_guide/merging.html) |
| **Not using categorical** | String column with few unique values | Use `pd.Categorical` or `.astype('category')` | [Categorical data](https://pandas.pydata.org/docs/user_guide/categorical.html) |
| **Loading all data** | `pd.read_csv('huge.csv')` | Use `chunksize` or `usecols` parameter | [IO tools](https://pandas.pydata.org/docs/user_guide/io.html#io-chunking) |
| **Not using method chaining** | Multiple separate operations | Chain with `.pipe()`, `.assign()`, `.query()` | [Method chaining](https://tomaugspurger.github.io/method-chaining) |

---

## NumPy Performance Anti-Patterns

| Anti-Pattern | What to Look For | Better Approach | Learn More |
|--------------|------------------|-----------------|------------|
| **Python loops** | `for i in range(len(arr)):` | Use vectorized operations or `np.vectorize()` | [NumPy broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html) |
| **Wrong dtype** | `np.array([1, 2, 3], dtype=float)` for integers | Use appropriate dtype: `int64`, `float32`, etc. | [Data types](https://numpy.org/doc/stable/user/basics.types.html) |
| **Creating unnecessary copies** | `arr.copy()` when not needed | Use views when possible | [Copies and views](https://numpy.org/doc/stable/user/basics.copies.html) |
| **Not using broadcasting** | Manual element-wise operations | Let NumPy broadcast automatically | [Broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html) |
| **Inefficient indexing** | Repeated fancy indexing | Use boolean indexing or `np.where()` | [Indexing](https://numpy.org/doc/stable/user/basics.indexing.html) |

---

## Data Validation Issues

| Issue | What to Look For | Best Practice | Learn More |
|-------|------------------|---------------|------------|
| **Missing value handling** | No check for `NaN` or `None` | Use `.isna()`, `.notna()`, `.fillna()` | [Missing data](https://pandas.pydata.org/docs/user_guide/missing_data.html) |
| **Type assumptions** | No dtype validation | Check dtypes, use `.astype()` with error handling | [dtypes](https://pandas.pydata.org/docs/user_guide/basics.html#dtypes) |
| **Duplicate rows** | No duplicate check | Use `.duplicated()`, `.drop_duplicates()` | [Duplicates](https://pandas.pydata.org/docs/user_guide/duplicates.html) |
| **Outliers** | No outlier detection | Use IQR, z-score, or domain knowledge | [Outlier detection](https://scikit-learn.org/stable/modules/outlier_detection.html) |
| **Date parsing** | String dates not parsed | Use `pd.to_datetime()` with format parameter | [Time series](https://pandas.pydata.org/docs/user_guide/timeseries.html) |

---

## Memory Management Issues

| Issue | What to Look For | Solution | Learn More |
|-------|------------------|----------|------------|
| **Large object dtypes** | `object` dtype for strings | Use `string` dtype or `category` | [String dtype](https://pandas.pydata.org/docs/user_guide/text.html) |
| **Not freeing memory** | Large DataFrames not deleted | Use `del df` and `gc.collect()` | [Memory usage](https://pandas.pydata.org/docs/user_guide/scale.html) |
| **Reading entire file** | `pd.read_csv()` without limits | Use `nrows`, `chunksize`, or `usecols` | [Large datasets](https://pandas.pydata.org/docs/user_guide/scale.html#scaling-to-large-datasets) |
| **Copying unnecessarily** | `df.copy()` everywhere | Use `inplace=True` or avoid copies | [Copy performance](https://pandas.pydata.org/docs/user_guide/copy_on_write.html) |

---

## Common Detection Patterns

```python
# Pandas anti-patterns
for index, row in df.iterrows():  # ❌ Slow iteration
df['col'] = df.apply(lambda x: ...)  # ❌ Often unnecessary
df[df['A'] > 5]['B'] = 10  # ❌ Chained indexing (SettingWithCopyWarning)
for i in range(len(df)):  # ❌ Using range() with DataFrames
    df = df.append(...)  # ❌ Growing DataFrame in loop

# NumPy anti-patterns
for i in range(len(arr)):  # ❌ Python loop instead of vectorization
    arr[i] = arr[i] * 2
new_arr = arr.copy()  # ❌ Unnecessary copy
result = np.array([], dtype=int)  # ❌ Growing array
for item in data:
    result = np.append(result, item)

# Missing validation
df = pd.read_csv('file.csv')
# ❌ No dtype check, no missing value check, no duplicate check
result = df['A'] * df['B']  # May fail or give unexpected results
```

---

## Best Practices Checklist

- [ ] Use vectorized operations instead of loops
- [ ] Use `.loc[]` and `.iloc[]` for indexing (avoid chained indexing)
- [ ] Check for missing values and handle them appropriately
- [ ] Validate data types after loading
- [ ] Use categorical dtypes for low-cardinality string columns
- [ ] Use method chaining for readability
- [ ] Avoid growing DataFrames/arrays in loops
- [ ] Use appropriate data types (don't default to `float64`)
- [ ] Check for and handle duplicates
- [ ] Use chunking for large datasets
- [ ] Profile memory usage for large datasets

---

## Key Pandas Methods

| Operation | Method | Example |
|-----------|--------|---------|
| Filter rows | `.loc[]`, `.query()` | `df.loc[df['age'] > 18]` |
| Select columns | `.loc[]`, `[]` | `df[['col1', 'col2']]` |
| Group and aggregate | `.groupby()`, `.agg()` | `df.groupby('category').agg({'value': 'sum'})` |
| Merge/join | `.merge()`, `.join()` | `pd.merge(df1, df2, on='key')` |
| Reshape | `.pivot()`, `.melt()` | `df.pivot(index='date', columns='type')` |
| Apply function | `.apply()`, `.map()`, `.applymap()` | `df['col'].map(lambda x: x*2)` |

See [Pandas API reference](https://pandas.pydata.org/docs/reference/index.html)

---

## Tools for Data Quality

- **pandas-profiling**: Automatic EDA reports - [pandas-profiling](https://github.com/ydataai/ydata-profiling)
- **Great Expectations**: Data validation framework - [Great Expectations](https://greatexpectations.io/)
- **pandera**: Statistical data validation - [pandera](https://pandera.readthedocs.io/)
- **Dask**: Parallel computing for larger-than-memory datasets - [Dask](https://dask.org/)

---

## Official Documentation

- **Pandas**: https://pandas.pydata.org/docs/
- **NumPy**: https://numpy.org/doc/stable/
- **Pandas Performance**: https://pandas.pydata.org/docs/user_guide/enhancingperf.html
- **NumPy Performance**: https://numpy.org/doc/stable/user/performance.html
- **SciPy**: https://docs.scipy.org/doc/scipy/
- **Matplotlib**: https://matplotlib.org/stable/contents.html
- **Seaborn**: https://seaborn.pydata.org/

---

**Version**: 1.0.0 (Compacted)
**Last Updated**: 2025-11-14
**Maintained For**: python-code-review skill
