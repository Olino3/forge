# Exploratory Data Analysis Template

## 1. Setup and Imports
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

%matplotlib inline
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)
```

## 2. Load Data
```python
# Load dataset
df = pd.read_csv('your_data.csv')  # Modify path
print(f"Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
```

## 3. Initial Inspection
```python
# First few rows
display(df.head())

# Dataset info
print(df.info())

# Summary statistics
display(df.describe())
```

## 4. Data Quality Checks
```python
# Missing values
print("Missing Values:")
print(df.isnull().sum())

# Duplicates
print(f"\nDuplicates: {df.duplicated().sum()}")

# Unique values in categorical columns
for col in df.select_dtypes(include='object').columns:
    print(f"{col}: {df[col].nunique()} unique values")
```

## 5. Univariate Analysis
```python
# Distribution of numerical features
numerical_cols = df.select_dtypes(include=[np.number]).columns

for col in numerical_cols:
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    sns.histplot(df[col], kde=True)
    plt.title(f'Distribution of {col}')
    
    plt.subplot(1, 2, 2)
    sns.boxplot(y=df[col])
    plt.title(f'Boxplot of {col}')
    
    plt.tight_layout()
    plt.show()
```

## 6. Categorical Analysis
```python
# Value counts for categorical features
categorical_cols = df.select_dtypes(include='object').columns

for col in categorical_cols:
    plt.figure(figsize=(10, 6))
    df[col].value_counts().plot(kind='bar')
    plt.title(f'Distribution of {col}')
    plt.xlabel(col)
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
```

## 7. Correlation Analysis
```python
# Correlation heatmap
plt.figure(figsize=(10, 8))
correlation_matrix = df[numerical_cols].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Matrix')
plt.tight_layout()
plt.show()
```

## 8. Key Findings
```python
# Summarize insights
print("="*80)
print("KEY FINDINGS")
print("="*80)
print("""
1. [Finding 1]
2. [Finding 2]
3. [Finding 3]

Recommendations:
- [Recommendation 1]
- [Recommendation 2]
""")
```
