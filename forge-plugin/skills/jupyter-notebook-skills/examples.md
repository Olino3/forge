# Jupyter Notebook Skills Examples

This file contains example scenarios demonstrating how to use the jupyter-notebook-skills skill to perform common data science tasks in Jupyter notebooks.

---

## Example 1: Basic Exploratory Data Analysis (EDA)

### Scenario
User has a CSV file with customer purchase data and wants to understand the data before building a predictive model.

### User Prompt
```
I have a customer_purchases.csv file with columns: customer_id, age, income, purchase_amount, purchase_date, product_category. Help me explore this data and find interesting patterns.
```

### Skill Execution

**Step 1 - Understand Context**:
- **Data source**: CSV file (customer_purchases.csv)
- **Objective**: Exploratory Data Analysis to find patterns
- **Data characteristics**: 6 columns (mix of numeric and categorical)
- **User expertise**: Intermediate (familiar with pandas basics)
- **Environment**: Local Jupyter

**Step 2 - Plan Analysis**:
- **Pipeline**: Load → Inspect → Clean → Visualize → Summarize
- **Libraries**: pandas, numpy, matplotlib, seaborn
- **Focus areas**: Distribution of purchase amounts, age groups, category preferences, temporal patterns

**Step 3 - Generate Code**:

### Generated Notebook Cells

#### Cell 1: Imports and Setup
```python
# Data manipulation and analysis
import pandas as pd
import numpy as np

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns

# Configure plotting
%matplotlib inline
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)

print("Libraries loaded successfully!")
```

#### Cell 2: Load Data
```python
# Load the dataset
try:
    df = pd.read_csv('customer_purchases.csv')
    print(f"✅ Data loaded successfully!")
    print(f"   Rows: {df.shape[0]:,}")
    print(f"   Columns: {df.shape[1]}")
except FileNotFoundError:
    print("❌ Error: File 'customer_purchases.csv' not found.")
    print("   Please check the file path.")
```

#### Cell 3: Initial Data Inspection
```python
# Display first few rows
print("📊 First 5 rows of the dataset:")
display(df.head())

print("\n" + "="*80 + "\n")

# Data types and non-null counts
print("📋 Dataset Information:")
print(df.info())

print("\n" + "="*80 + "\n")

# Basic statistics
print("📈 Summary Statistics:")
display(df.describe())
```

#### Cell 4: Data Quality Check
```python
# Check for missing values
print("🔍 Missing Values:")
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
missing_df = pd.DataFrame({
    'Missing Count': missing,
    'Percentage': missing_pct
})
print(missing_df[missing_df['Missing Count'] > 0])

print("\n" + "="*80 + "\n")

# Check for duplicates
duplicates = df.duplicated().sum()
print(f"🔁 Duplicate Rows: {duplicates} ({duplicates/len(df)*100:.2f}%)")

print("\n" + "="*80 + "\n")

# Unique values in categorical columns
print("🏷️ Unique Values in Categorical Columns:")
for col in df.select_dtypes(include='object').columns:
    print(f"  {col}: {df[col].nunique()} unique values")
```

#### Cell 5: Visualize Purchase Amount Distribution
```python
# Distribution of purchase amounts
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Histogram with KDE
sns.histplot(data=df, x='purchase_amount', kde=True, ax=axes[0])
axes[0].set_title('Distribution of Purchase Amounts', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Purchase Amount ($)')
axes[0].set_ylabel('Frequency')

# Box plot to identify outliers
sns.boxplot(data=df, y='purchase_amount', ax=axes[1])
axes[1].set_title('Purchase Amount Outliers', fontsize=14, fontweight='bold')
axes[1].set_ylabel('Purchase Amount ($)')

plt.tight_layout()
plt.show()

# Print statistics
print(f"Mean Purchase: ${df['purchase_amount'].mean():.2f}")
print(f"Median Purchase: ${df['purchase_amount'].median():.2f}")
print(f"Std Dev: ${df['purchase_amount'].std():.2f}")
```

#### Cell 6: Analyze Product Categories
```python
# Product category analysis
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Category counts
category_counts = df['product_category'].value_counts()
sns.barplot(x=category_counts.values, y=category_counts.index, ax=axes[0])
axes[0].set_title('Purchase Count by Category', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Number of Purchases')
axes[0].set_ylabel('Product Category')

# Average purchase amount by category
category_avg = df.groupby('product_category')['purchase_amount'].mean().sort_values(ascending=False)
sns.barplot(x=category_avg.values, y=category_avg.index, ax=axes[1])
axes[1].set_title('Average Purchase Amount by Category', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Average Purchase Amount ($)')
axes[1].set_ylabel('Product Category')

plt.tight_layout()
plt.show()
```

#### Cell 7: Age Demographics Analysis
```python
# Create age groups
df['age_group'] = pd.cut(df['age'], bins=[0, 25, 35, 45, 55, 100], 
                         labels=['18-25', '26-35', '36-45', '46-55', '56+'])

# Purchases by age group
age_analysis = df.groupby('age_group').agg({
    'purchase_amount': ['count', 'mean', 'sum']
}).round(2)

age_analysis.columns = ['Purchase Count', 'Avg Amount', 'Total Spent']
print("👥 Purchases by Age Group:")
display(age_analysis)

# Visualize
fig, ax = plt.subplots(figsize=(10, 6))
age_analysis['Avg Amount'].plot(kind='bar', ax=ax, color='skyblue')
ax.set_title('Average Purchase Amount by Age Group', fontsize=14, fontweight='bold')
ax.set_xlabel('Age Group')
ax.set_ylabel('Average Purchase Amount ($)')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
plt.tight_layout()
plt.show()
```

#### Cell 8: Correlation Analysis
```python
# Correlation heatmap for numerical features
numerical_cols = df.select_dtypes(include=[np.number]).columns

plt.figure(figsize=(8, 6))
correlation_matrix = df[numerical_cols].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, 
            square=True, linewidths=1, cbar_kws={"shrink": 0.8})
plt.title('Correlation Matrix of Numerical Features', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

# Print top correlations with purchase_amount
correlations = correlation_matrix['purchase_amount'].sort_values(ascending=False)
print("\n📊 Correlations with Purchase Amount:")
print(correlations)
```

#### Cell 9: Key Findings Summary
```python
print("=" * 80)
print("🎯 KEY FINDINGS")
print("=" * 80)

findings = f"""
1. Dataset Overview:
   - Total Customers: {df['customer_id'].nunique():,}
   - Total Purchases: {len(df):,}
   - Date Range: {df['purchase_date'].min()} to {df['purchase_date'].max()}

2. Purchase Behavior:
   - Average Purchase: ${df['purchase_amount'].mean():.2f}
   - Most Popular Category: {df['product_category'].mode()[0]}
   - Highest Spending Age Group: {age_analysis['Total Spent'].idxmax()}

3. Recommendations for Further Analysis:
   - Investigate outliers in purchase amounts (potential high-value customers)
   - Analyze temporal trends (seasonal patterns, day-of-week effects)
   - Build customer segmentation model based on purchase behavior
   - Create retention analysis to identify churning customers
"""

print(findings)
```

**Step 4 - Validate**:
- ✅ All imports at top
- ✅ Error handling for file loading
- ✅ Clear visualizations with titles and labels
- ✅ Markdown cells explain each section (not shown here, but should be added)
- ✅ Results are interpreted, not just printed

---

## Example 2: Building a Classification Model

### Scenario
User wants to predict customer churn based on usage data.

### User Prompt
```
Build a machine learning model to predict customer churn. Dataset has: tenure, monthly_charges, total_charges, contract_type, and churn (yes/no).
```

### Skill Execution

**Step 1 - Understand Context**:
- **Data source**: Assumed to be loaded in df
- **Objective**: Binary classification (churn prediction)
- **Features**: Mix of numerical (tenure, charges) and categorical (contract_type)
- **Target**: churn (yes/no)
- **User expertise**: Intermediate

**Step 2 - Plan Analysis**:
- **Pipeline**: EDA → Feature Engineering → Train/Test Split → Model Training → Evaluation
- **Libraries**: scikit-learn for ML, pandas for preprocessing
- **Models to try**: Logistic Regression, Random Forest, Gradient Boosting

**Step 3 - Generate Code**:

### Generated Notebook Cells

#### Cell 1: Prepare Data for Modeling
```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve

# Create a copy for modeling
df_model = df.copy()

# Encode categorical variables
le = LabelEncoder()
df_model['contract_type_encoded'] = le.fit_transform(df_model['contract_type'])
df_model['churn_encoded'] = le.fit_transform(df_model['churn'])  # yes=1, no=0

# Select features and target
feature_cols = ['tenure', 'monthly_charges', 'total_charges', 'contract_type_encoded']
X = df_model[feature_cols]
y = df_model['churn_encoded']

print(f"Features: {X.shape[1]}")
print(f"Samples: {X.shape[0]}")
print(f"Churn Rate: {y.mean()*100:.2f}%")
```

#### Cell 2: Train-Test Split
```python
# Split data: 80% train, 20% test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Scale numerical features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"Training set: {X_train.shape[0]} samples")
print(f"Test set: {X_test.shape[0]} samples")
print(f"Train churn rate: {y_train.mean()*100:.2f}%")
print(f"Test churn rate: {y_test.mean()*100:.2f}%")
```

#### Cell 3: Train Multiple Models
```python
# Dictionary to store models and their scores
models = {
    'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
    'Random Forest': RandomForestClassifier(random_state=42, n_estimators=100),
    'Gradient Boosting': GradientBoostingClassifier(random_state=42, n_estimators=100)
}

results = {}

print("🔧 Training models...\n")

for name, model in models.items():
    # Train
    model.fit(X_train_scaled, y_train)
    
    # Predict
    y_pred = model.predict(X_test_scaled)
    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
    
    # Evaluate
    auc = roc_auc_score(y_test, y_pred_proba)
    
    results[name] = {
        'model': model,
        'y_pred': y_pred,
        'y_pred_proba': y_pred_proba,
        'auc': auc
    }
    
    print(f"✅ {name}")
    print(f"   AUC Score: {auc:.4f}\n")
```

#### Cell 4: Evaluate Best Model
```python
# Find best model by AUC
best_model_name = max(results, key=lambda x: results[x]['auc'])
best_result = results[best_model_name]

print(f"🏆 Best Model: {best_model_name}")
print(f"   AUC: {best_result['auc']:.4f}\n")

# Detailed classification report
print("📊 Classification Report:")
print(classification_report(y_test, best_result['y_pred'], 
                          target_names=['No Churn', 'Churn']))

# Confusion matrix
print("\n🔲 Confusion Matrix:")
cm = confusion_matrix(y_test, best_result['y_pred'])
print(cm)
print("\n   [[True Neg  False Pos]")
print("    [False Neg  True Pos]]")
```

#### Cell 5: Visualize Model Performance
```python
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# ROC Curves for all models
for name, result in results.items():
    fpr, tpr, _ = roc_curve(y_test, result['y_pred_proba'])
    axes[0].plot(fpr, tpr, label=f"{name} (AUC={result['auc']:.3f})")

axes[0].plot([0, 1], [0, 1], 'k--', label='Random Classifier')
axes[0].set_xlabel('False Positive Rate')
axes[0].set_ylabel('True Positive Rate')
axes[0].set_title('ROC Curves', fontsize=14, fontweight='bold')
axes[0].legend()
axes[0].grid(True)

# Confusion Matrix Heatmap for best model
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[1],
            xticklabels=['No Churn', 'Churn'],
            yticklabels=['No Churn', 'Churn'])
axes[1].set_title(f'Confusion Matrix - {best_model_name}', fontsize=14, fontweight='bold')
axes[1].set_ylabel('Actual')
axes[1].set_xlabel('Predicted')

plt.tight_layout()
plt.show()
```

#### Cell 6: Feature Importance (for tree-based models)
```python
if best_model_name in ['Random Forest', 'Gradient Boosting']:
    # Get feature importances
    importances = best_result['model'].feature_importances_
    feature_importance_df = pd.DataFrame({
        'Feature': feature_cols,
        'Importance': importances
    }).sort_values('Importance', ascending=False)
    
    # Plot
    plt.figure(figsize=(10, 6))
    sns.barplot(data=feature_importance_df, x='Importance', y='Feature')
    plt.title(f'Feature Importance - {best_model_name}', fontsize=14, fontweight='bold')
    plt.xlabel('Importance')
    plt.tight_layout()
    plt.show()
    
    print("📊 Feature Importance Ranking:")
    display(feature_importance_df)
```

**Step 4 - Validate**:
- ✅ Train/test split with stratification (preserves class distribution)
- ✅ Feature scaling for algorithms that need it
- ✅ Random seeds set for reproducibility
- ✅ Multiple models compared
- ✅ Appropriate metrics (AUC, precision, recall for imbalanced classification)
- ✅ Visualizations clearly labeled

---

## Example 3: Time Series Analysis and Visualization

### Scenario
User has daily sales data and wants to identify trends and seasonality.

### User Prompt
```
I have daily sales data for 2 years in a 'date' and 'sales' column. Show me trends, seasonality, and forecast the next 30 days.
```

### Skill Execution

**Step 1 - Understand Context**:
- **Data source**: DataFrame with date and sales columns
- **Objective**: Time series analysis and forecasting
- **Data characteristics**: Daily frequency, 2 years = ~730 data points
- **User expertise**: Intermediate

**Step 2 - Plan Analysis**:
- **Pipeline**: Convert to datetime → Visualize trends → Decompose → Simple forecast
- **Libraries**: pandas for time series, statsmodels for decomposition, matplotlib for viz

**Step 3 - Generate Code**:

### Generated Notebook Cells

#### Cell 1: Prepare Time Series Data
```python
from statsmodels.tsa.seasonal import seasonal_decompose
from datetime import timedelta

# Ensure date is datetime type
df['date'] = pd.to_datetime(df['date'])

# Set date as index
df_ts = df.set_index('date').sort_index()

# Check for missing dates
date_range = pd.date_range(start=df_ts.index.min(), end=df_ts.index.max(), freq='D')
missing_dates = date_range.difference(df_ts.index)

print(f"📅 Time Series Overview:")
print(f"   Start Date: {df_ts.index.min()}")
print(f"   End Date: {df_ts.index.max()}")
print(f"   Total Days: {len(df_ts)}")
print(f"   Missing Dates: {len(missing_dates)}")

if len(missing_dates) > 0:
    print(f"\n⚠️ Warning: {len(missing_dates)} missing dates detected")
    print("   Consider filling gaps with interpolation or forward-fill")
```

#### Cell 2: Visualize Overall Trend
```python
fig, axes = plt.subplots(2, 1, figsize=(14, 8))

# Raw time series
axes[0].plot(df_ts.index, df_ts['sales'], linewidth=1, color='steelblue')
axes[0].set_title('Daily Sales Over Time', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Date')
axes[0].set_ylabel('Sales ($)')
axes[0].grid(True, alpha=0.3)

# 7-day moving average to smooth out noise
df_ts['sales_ma7'] = df_ts['sales'].rolling(window=7, center=True).mean()
axes[1].plot(df_ts.index, df_ts['sales'], alpha=0.3, label='Daily Sales', linewidth=0.5)
axes[1].plot(df_ts.index, df_ts['sales_ma7'], label='7-Day Moving Avg', linewidth=2, color='red')
axes[1].set_title('Sales with 7-Day Moving Average', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Date')
axes[1].set_ylabel('Sales ($)')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

#### Cell 3: Seasonal Decomposition
```python
# Decompose time series into trend, seasonal, and residual components
# Using additive model (sales = trend + seasonal + residual)
decomposition = seasonal_decompose(df_ts['sales'], model='additive', period=7)

# Plot decomposition
fig, axes = plt.subplots(4, 1, figsize=(14, 10))

decomposition.observed.plot(ax=axes[0], title='Observed', color='steelblue')
axes[0].set_ylabel('Sales')

decomposition.trend.plot(ax=axes[1], title='Trend', color='green')
axes[1].set_ylabel('Trend')

decomposition.seasonal.plot(ax=axes[2], title='Seasonality (7-day pattern)', color='orange')
axes[2].set_ylabel('Seasonal')

decomposition.resid.plot(ax=axes[3], title='Residuals', color='red')
axes[3].set_ylabel('Residual')

for ax in axes:
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

#### Cell 4: Day-of-Week Analysis
```python
# Extract day of week
df_ts['day_of_week'] = df_ts.index.dayofweek
df_ts['day_name'] = df_ts.index.day_name()

# Average sales by day of week
day_avg = df_ts.groupby('day_name')['sales'].mean().reindex(
    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
)

# Plot
plt.figure(figsize=(10, 6))
day_avg.plot(kind='bar', color='skyblue')
plt.title('Average Sales by Day of Week', fontsize=14, fontweight='bold')
plt.xlabel('Day of Week')
plt.ylabel('Average Sales ($)')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.show()

print("📊 Average Sales by Day:")
print(day_avg)
```

#### Cell 5: Simple Forecast (Naive Method with Seasonality)
```python
# Simple forecast: use average of last 4 weeks for each day of week
forecast_days = 30
last_4_weeks = df_ts.tail(28)  # Last 4 weeks

# Calculate average for each day of week from last 4 weeks
forecast_values = []
forecast_dates = []

last_date = df_ts.index.max()
for i in range(1, forecast_days + 1):
    future_date = last_date + timedelta(days=i)
    day_name = future_date.day_name()
    
    # Average sales for this day of week from last 4 weeks
    avg_sales = last_4_weeks[last_4_weeks['day_name'] == day_name]['sales'].mean()
    
    forecast_values.append(avg_sales)
    forecast_dates.append(future_date)

# Create forecast dataframe
forecast_df = pd.DataFrame({
    'date': forecast_dates,
    'forecast': forecast_values
}).set_index('date')

# Plot historical + forecast
plt.figure(figsize=(14, 6))
plt.plot(df_ts.index[-90:], df_ts['sales'].tail(90), label='Historical (Last 90 Days)', linewidth=2)
plt.plot(forecast_df.index, forecast_df['forecast'], label='Forecast (Next 30 Days)', 
         linewidth=2, linestyle='--', color='red')
plt.axvline(x=last_date, color='gray', linestyle=':', linewidth=1, label='Forecast Start')
plt.title('Sales Forecast - Next 30 Days', fontsize=14, fontweight='bold')
plt.xlabel('Date')
plt.ylabel('Sales ($)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print("📈 Forecast Summary:")
print(f"   Average Forecast: ${forecast_df['forecast'].mean():.2f}")
print(f"   Range: ${forecast_df['forecast'].min():.2f} - ${forecast_df['forecast'].max():.2f}")
```

**Step 4 - Validate**:
- ✅ Datetime conversion handled
- ✅ Missing dates checked
- ✅ Decomposition reveals trend and seasonality
- ✅ Simple forecast method explained (naive with day-of-week averaging)
- ⚠️ Note: For production forecasting, recommend ARIMA, Prophet, or LSTM models

---

## Summary of Common Tasks

1. **Exploratory Data Analysis (EDA)**: Inspect, clean, visualize, summarize
2. **Classification Model**: Preprocess, train, evaluate, interpret
3. **Time Series Analysis**: Decompose, identify patterns, forecast

## Best Practices Demonstrated

- **Clear structure**: Each cell has a specific purpose
- **Error handling**: File loading checks for errors
- **Reproducibility**: Random seeds, scaled features saved
- **Visualization**: Clear titles, labels, legends
- **Interpretation**: Results are explained, not just shown
- **Documentation**: Comments explain non-obvious steps
- **Validation**: Models evaluated on holdout test set

## Next Steps for Users

After running these examples, consider:
1. **Hyperparameter tuning**: Use GridSearchCV or RandomizedSearchCV
2. **Advanced models**: Try XGBoost, LightGBM, neural networks
3. **Cross-validation**: Use k-fold CV for more robust evaluation
4. **Feature engineering**: Create interaction terms, polynomial features
5. **Deployment**: Save models with joblib/pickle for production use
