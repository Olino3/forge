# Machine Learning Workflow Template

## 1. Setup and Imports
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

# Import your models
from sklearn.ensemble import RandomForestClassifier
# Add more as needed
```

## 2. Load and Prepare Data
```python
# Load data
df = pd.read_csv('your_data.csv')

# Handle missing values
# Option 1: Drop rows
df = df.dropna()

# Option 2: Impute
# from sklearn.impute import SimpleImputer
# imputer = SimpleImputer(strategy='mean')
# df[numerical_cols] = imputer.fit_transform(df[numerical_cols])
```

## 3. Feature Engineering
```python
# Encode categorical variables
le = LabelEncoder()
for col in df.select_dtypes(include='object').columns:
    if col != 'target_column':  # Don't encode target yet
        df[f'{col}_encoded'] = le.fit_transform(df[col])

# Create new features if needed
# df['feature_interaction'] = df['feature1'] * df['feature2']
```

## 4. Define Features and Target
```python
# Select feature columns
feature_cols = [...]  # List your feature column names

X = df[feature_cols]
y = df['target_column']  # Modify with your target

print(f"Features: {X.shape[1]}")
print(f"Samples: {X.shape[0]}")
```

## 5. Train-Test Split
```python
# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y  # stratify for classification
)

# Scale features (important for distance-based algorithms)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"Training set: {X_train.shape[0]} samples")
print(f"Test set: {X_test.shape[0]} samples")
```

## 6. Train Models
```python
# Initialize models
models = {
    'Model1': ModelClass1(random_state=42),
    'Model2': ModelClass2(random_state=42),
}

# Train and evaluate
results = {}
for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    
    # Store results
    results[name] = {
        'model': model,
        'predictions': y_pred
    }
    
    print(f"{name} trained ✓")
```

## 7. Evaluate Models
```python
# For Classification
for name, result in results.items():
    print(f"\n{'='*60}")
    print(f"{name} Performance")
    print('='*60)
    print(classification_report(y_test, result['predictions']))
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, result['predictions'])
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title(f'Confusion Matrix - {name}')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.show()
```

## 8. Feature Importance (if applicable)
```python
# For tree-based models
best_model_name = 'YourBestModel'  # Replace with actual best model
best_model = results[best_model_name]['model']

if hasattr(best_model, 'feature_importances_'):
    importances = pd.DataFrame({
        'Feature': feature_cols,
        'Importance': best_model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=importances, x='Importance', y='Feature')
    plt.title('Feature Importance')
    plt.tight_layout()
    plt.show()
```

## 9. Save Model (Optional)
```python
import joblib

# Save the best model and scaler
joblib.dump(best_model, 'model.pkl')
joblib.dump(scaler, 'scaler.pkl')

print("Model saved successfully!")
```

## 10. Conclusions
```python
print("="*80)
print("MODEL SUMMARY")
print("="*80)
print(f"""
Best Model: {best_model_name}
Test Accuracy: [X.XX%]

Key Insights:
- [Insight 1]
- [Insight 2]

Next Steps:
- [Next step 1]
- [Next step 2]
""")
```
