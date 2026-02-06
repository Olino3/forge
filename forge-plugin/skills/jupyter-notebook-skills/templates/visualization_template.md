# Data Visualization Template

## 1. Setup
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Optional: Plotly for interactive visualizations
# import plotly.express as px
# import plotly.graph_objects as go

%matplotlib inline
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)
```

## 2. Load Data
```python
df = pd.read_csv('your_data.csv')
print(f"Data shape: {df.shape}")
```

## 3. Single Variable Plots

### Numerical Distribution
```python
# Histogram with KDE
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='numerical_column', kde=True, bins=30)
plt.title('Distribution of [Variable Name]')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.show()
```

### Categorical Distribution
```python
# Bar chart
plt.figure(figsize=(10, 6))
df['categorical_column'].value_counts().plot(kind='bar')
plt.title('Distribution of [Category]')
plt.xlabel('Category')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

## 4. Two Variable Relationships

### Numerical vs Numerical
```python
# Scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(df['x_variable'], df['y_variable'], alpha=0.5)
plt.title('Relationship between X and Y')
plt.xlabel('X Variable')
plt.ylabel('Y Variable')
plt.grid(True, alpha=0.3)
plt.show()
```

### Categorical vs Numerical
```python
# Box plot
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='category_column', y='numerical_column')
plt.title('Distribution of [Numerical] by [Category]')
plt.xlabel('Category')
plt.ylabel('Value')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

## 5. Multi-Variable Visualization

### Correlation Heatmap
```python
# Correlation matrix
plt.figure(figsize=(10, 8))
numerical_cols = df.select_dtypes(include=[np.number]).columns
correlation = df[numerical_cols].corr()
sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0, 
            square=True, linewidths=1)
plt.title('Correlation Matrix')
plt.tight_layout()
plt.show()
```

### Pair Plot
```python
# Scatter matrix for multiple variables
selected_cols = ['var1', 'var2', 'var3', 'target']
sns.pairplot(df[selected_cols], hue='target', diag_kind='kde')
plt.suptitle('Pair Plot of Key Variables', y=1.02)
plt.show()
```

## 6. Time Series Visualization
```python
# Line plot over time
df['date'] = pd.to_datetime(df['date_column'])
df = df.sort_values('date')

plt.figure(figsize=(14, 6))
plt.plot(df['date'], df['value_column'], linewidth=2)
plt.title('Trend Over Time')
plt.xlabel('Date')
plt.ylabel('Value')
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

## 7. Grouped/Aggregated Visualizations
```python
# Grouped bar chart
grouped_data = df.groupby('category1')['value'].mean().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(data=grouped_data, x='category1', y='value')
plt.title('Average Value by Category')
plt.xlabel('Category')
plt.ylabel('Average Value')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

## 8. Advanced: Subplots
```python
# Multiple subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1
axes[0, 0].hist(df['var1'], bins=30, color='skyblue')
axes[0, 0].set_title('Distribution of Var1')

# Plot 2
axes[0, 1].scatter(df['var1'], df['var2'], alpha=0.5)
axes[0, 1].set_title('Var1 vs Var2')

# Plot 3
df['category'].value_counts().plot(kind='bar', ax=axes[1, 0], color='coral')
axes[1, 0].set_title('Category Distribution')

# Plot 4
axes[1, 1].boxplot([df['var1'], df['var2'], df['var3']])
axes[1, 1].set_title('Boxplot Comparison')
axes[1, 1].set_xticklabels(['Var1', 'Var2', 'Var3'])

plt.tight_layout()
plt.show()
```

## 9. Save Figures
```python
# Save high-resolution figure
fig = plt.figure(figsize=(12, 6))
# ... your plot code ...
plt.savefig('output_figure.png', dpi=300, bbox_inches='tight')
print("Figure saved!")
```
