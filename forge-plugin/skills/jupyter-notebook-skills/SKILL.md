---
name: jupyter-notebook-skills
description: Commands interactive data exploration through Jupyter Notebooks. Generates analysis code, creates visualizations, performs statistical analysis, builds ML models, and orchestrates data science workflows. Supports pandas, numpy, matplotlib, seaborn, scikit-learn, and deep learning frameworks. Like Athena guiding explorers through uncharted territories, this skill illuminates patterns hidden within data and transforms raw numbers into actionable insights.
---

# Interactive Data Exploration Commander

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: The 4-step workflow outlined in this document MUST be followed in exact order for EVERY Jupyter notebook task. Skipping steps or deviating from the procedure will result in ineffective analysis or incorrect results. This is non-negotiable.

## File Structure

- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: Usage scenarios with different data science tasks and generated notebook code
- **../../memory/skills/jupyter-notebook-skills/**: Project-specific memory storage
  - `{project-name}/`: Per-project analysis patterns, data schemas, and conventions
- **templates/**:
  - `eda_template.md`: Exploratory Data Analysis notebook template
  - `ml_template.md`: Machine Learning workflow template
  - `visualization_template.md`: Data visualization template

## Focus Areas

Jupyter notebook data exploration evaluates 7 critical dimensions:

1. **Data Loading & Inspection**: Import data from various sources (CSV, SQL, APIs), inspect structure, identify data types
2. **Data Cleaning & Preprocessing**: Handle missing values, outliers, duplicates, type conversions, feature engineering
3. **Exploratory Data Analysis (EDA)**: Statistical summaries, distributions, correlations, patterns, anomalies
4. **Visualization**: Create informative plots (matplotlib, seaborn, plotly) for data understanding and presentation
5. **Statistical Analysis**: Hypothesis testing, confidence intervals, significance tests, regression analysis
6. **Machine Learning**: Model selection, training, evaluation, hyperparameter tuning, feature importance
7. **Reproducibility**: Clear code organization, documentation, random seeds, environment specifications

**Note**: The skill generates notebook cells and code snippets for the user to execute. It does not run notebooks directly unless integrated with a Jupyter kernel.

---

## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Understand the Data Context (REQUIRED)

**YOU MUST:**
1. Determine the **data source**: CSV file, database, API, existing dataframe, web scraping
2. Identify the **analysis objective**: EDA, predictive modeling, hypothesis testing, visualization, reporting
3. Clarify the **data characteristics**: size (rows/columns), data types, known issues (missing values, outliers)
4. Assess the **user's expertise level**: beginner (needs explanations), intermediate (familiar with pandas), advanced (can customize code)
5. Identify the **environment**: Local Jupyter, JupyterLab, Google Colab, Databricks, SageMaker
6. Ask clarifying questions if context is incomplete:
   - What does your data look like? (Schema, sample rows)
   - What question are you trying to answer with this data?
   - Are there any known data quality issues?
   - Which libraries are you comfortable using?
   - What type of output do you need? (Insights, visualizations, models, reports)

**DO NOT PROCEED WITHOUT UNDERSTANDING THE DATA AND OBJECTIVE**

### ⚠️ STEP 2: Plan the Analysis Approach (REQUIRED)

**YOU MUST:**
1. **Map the data structure**: Identify target variable (for ML), features, categorical vs numerical columns
2. **Determine the analysis pipeline**:
   - **EDA**: Load → Inspect → Clean → Visualize → Summarize
   - **Predictive Modeling**: EDA → Feature Engineering → Train/Test Split → Model Selection → Evaluation
   - **Hypothesis Testing**: EDA → Assumption Checking → Statistical Test → Interpretation
   - **Time Series**: EDA → Stationarity Check → Decomposition → Forecasting
3. **Select appropriate libraries**:
   - Data manipulation: pandas, numpy
   - Visualization: matplotlib, seaborn, plotly
   - Statistics: scipy.stats, statsmodels
   - ML: scikit-learn, xgboost, tensorflow, pytorch
4. **Identify data quality steps needed**:
   - Missing value imputation (mean, median, mode, forward-fill, interpolation)
   - Outlier detection and handling (IQR, z-score, domain knowledge)
   - Encoding categorical variables (one-hot, label encoding, target encoding)
   - Feature scaling (standardization, normalization)
5. **Check project memory**: Look in `../../memory/skills/jupyter-notebook-skills/{project-name}/` for project-specific data schemas, feature engineering patterns, or modeling approaches

**DO NOT PROCEED WITHOUT A CLEAR ANALYSIS PLAN**

### ⚠️ STEP 3: Generate Notebook Code (REQUIRED)

**YOU MUST:**
1. **Structure the notebook logically** with markdown cells for narrative and code cells for execution:
   - Title and objective
   - Library imports
   - Data loading
   - Data inspection
   - Data cleaning
   - Analysis/modeling sections
   - Conclusions and next steps

2. **Write production-quality code**:
   - Clear variable names
   - Comments explaining non-obvious logic
   - Error handling for data loading
   - Reproducible random seeds for ML tasks
   - Modular functions for reusable operations
   - Type hints for Python 3.6+ (optional but recommended)

3. **For Data Loading**:
   ```python
   import pandas as pd
   import numpy as np
   
   # Load data with error handling
   try:
       df = pd.read_csv('data.csv')
       print(f"Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
   except FileNotFoundError:
       print("Error: File not found. Check the file path.")
   ```

4. **For Data Inspection**:
   ```python
   # Basic info
   print(df.info())
   print(df.describe())
   print(df.head())
   
   # Check for missing values
   print(df.isnull().sum())
   
   # Check for duplicates
   print(f"Duplicates: {df.duplicated().sum()}")
   ```

5. **For Visualizations**:
   - Use clear titles, axis labels, and legends
   - Choose appropriate plot types (scatter, histogram, box, heatmap)
   - Use color palettes that are colorblind-friendly
   - Include figure size for readability
   ```python
   import matplotlib.pyplot as plt
   import seaborn as sns
   
   plt.figure(figsize=(10, 6))
   sns.histplot(data=df, x='column_name', kde=True)
   plt.title('Distribution of Column Name')
   plt.xlabel('Column Name')
   plt.ylabel('Frequency')
   plt.show()
   ```

6. **For Machine Learning**:
   - Always use train/test split or cross-validation
   - Set random seeds for reproducibility
   - Evaluate with appropriate metrics (accuracy, precision, recall, F1, RMSE, R²)
   - Check for overfitting (compare train vs test performance)
   ```python
   from sklearn.model_selection import train_test_split
   from sklearn.ensemble import RandomForestClassifier
   from sklearn.metrics import classification_report, confusion_matrix
   
   # Split data
   X = df.drop('target', axis=1)
   y = df['target']
   X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
   
   # Train model
   model = RandomForestClassifier(random_state=42)
   model.fit(X_train, y_train)
   
   # Evaluate
   y_pred = model.predict(X_test)
   print(classification_report(y_test, y_pred))
   ```

7. **Use templates** from `templates/` for consistent notebook structure

**DO NOT GENERATE CODE WITH HARD-CODED ASSUMPTIONS ABOUT DATA**

### ⚠️ STEP 4: Validate and Document (REQUIRED)

**YOU MUST validate the notebook against these criteria:**
1. **Code quality check**:
   - [ ] Imports are at the top of the notebook
   - [ ] No unused imports or variables
   - [ ] Functions are defined before use
   - [ ] Random seeds are set for reproducibility
   - [ ] File paths are parameterized (not hard-coded)

2. **Analysis validity check**:
   - [ ] Data types are appropriate (numeric for calculations, categorical for encoding)
   - [ ] Missing value handling is appropriate for the data
   - [ ] Visualizations are clear and labeled
   - [ ] Statistical tests assumptions are checked (normality, homoscedasticity)
   - [ ] ML metrics match the problem type (classification vs regression)

3. **Reproducibility check**:
   - [ ] Random seeds set (`np.random.seed(42)`, `random_state=42`)
   - [ ] Environment can be recreated (list library versions)
   - [ ] Data source is documented
   - [ ] All cells run in order without errors

4. **Documentation**:
   - [ ] Markdown cells explain each major section
   - [ ] Code comments clarify non-obvious logic
   - [ ] Results are interpreted (not just printed)
   - [ ] Conclusions and next steps are provided

5. **Present the notebook code** to the user with clear execution instructions
6. **Offer alternatives**: Suggest alternative approaches when applicable (e.g., different models, different visualizations)

**DO NOT SKIP VALIDATION**

**OPTIONAL: Update Project Memory**

If project-specific patterns are discovered during analysis, store insights in `../../memory/skills/jupyter-notebook-skills/{project-name}/`:
- Data schema and feature descriptions
- Successful feature engineering patterns
- Model performance benchmarks
- Common data quality issues and solutions

---

## Compliance Checklist

Before completing ANY Jupyter notebook task, verify:
- [ ] Step 1: Data context understood — source, objective, characteristics, user expertise
- [ ] Step 2: Analysis approach planned — pipeline, libraries, data quality steps
- [ ] Step 3: Notebook code generated — structured, production-quality, uses templates
- [ ] Step 4: Notebook validated — code quality, analysis validity, reproducibility, documentation

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE NOTEBOOK**

---

## Common Data Science Tasks

### Exploratory Data Analysis (EDA)
- **Data profiling**: Shape, types, missing values, duplicates, unique counts
- **Descriptive statistics**: Mean, median, std, min/max, quartiles
- **Distributions**: Histograms, KDE plots, box plots
- **Correlations**: Heatmaps, scatter plots, pair plots
- **Categorical analysis**: Value counts, bar charts, grouped statistics

### Data Cleaning & Preprocessing
- **Missing values**: Drop, impute (mean/median/mode), forward-fill, interpolate
- **Outliers**: Detect (IQR, z-score), remove, cap, transform
- **Duplicates**: Identify, remove, or flag
- **Type conversion**: String to datetime, numeric to categorical
- **Feature engineering**: Create derived features, binning, scaling, encoding

### Statistical Analysis
- **Hypothesis testing**: t-test, chi-square, ANOVA, Mann-Whitney U
- **Correlation analysis**: Pearson, Spearman, Kendall
- **Regression**: Linear, polynomial, logistic regression
- **Time series**: Stationarity tests, decomposition, autocorrelation

### Machine Learning
- **Classification**: Logistic regression, decision trees, random forests, SVM, neural networks
- **Regression**: Linear regression, ridge, lasso, random forests, gradient boosting
- **Clustering**: K-means, hierarchical, DBSCAN
- **Dimensionality reduction**: PCA, t-SNE, UMAP
- **Evaluation**: Cross-validation, confusion matrix, ROC/AUC, feature importance

### Visualization
- **Univariate**: Histograms, box plots, violin plots, KDE
- **Bivariate**: Scatter plots, line plots, heatmaps
- **Multivariate**: Pair plots, parallel coordinates, 3D scatter
- **Advanced**: Interactive plots (plotly), geospatial (folium), network graphs (networkx)

---

## Library Quick Reference

### Essential Libraries
```python
import pandas as pd              # Data manipulation
import numpy as np               # Numerical computing
import matplotlib.pyplot as plt  # Basic plotting
import seaborn as sns            # Statistical visualization
```

### Statistical Analysis
```python
from scipy import stats          # Statistical functions
import statsmodels.api as sm     # Statistical models
```

### Machine Learning
```python
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.metrics import classification_report, mean_squared_error, r2_score
```

### Deep Learning
```python
import tensorflow as tf          # TensorFlow
from tensorflow import keras     # Keras (high-level API)
# OR
import torch                     # PyTorch
import torch.nn as nn
```

### Interactive Visualization
```python
import plotly.express as px      # High-level Plotly
import plotly.graph_objects as go # Low-level Plotly
```

---

## Best Practices

1. **Start with EDA**: Always explore data before building models
2. **Document assumptions**: Write down what you assume about the data
3. **Check data quality**: Missing values, outliers, and duplicates can ruin analysis
4. **Visualize early and often**: Plots reveal patterns that statistics might miss
5. **Use train/test splits**: Never evaluate a model on the same data it was trained on
6. **Set random seeds**: Makes results reproducible (`np.random.seed(42)`)
7. **Comment your code**: Explain *why*, not just *what*
8. **Use markdown cells**: Tell a story with your analysis
9. **Validate assumptions**: Check normality, homoscedasticity before statistical tests
10. **Iterate**: Analysis is rarely linear — go back and refine as you learn

---

## Environment Setup

### Local Jupyter Installation
```bash
pip install jupyter pandas numpy matplotlib seaborn scikit-learn scipy
jupyter notebook
```

### Google Colab (Cloud-based, Free)
- No installation needed
- Go to https://colab.research.google.com/
- Libraries pre-installed: pandas, numpy, matplotlib, seaborn, sklearn, tensorflow

### Conda Environment (Recommended for Data Science)
```bash
conda create -n data-science python=3.9
conda activate data-science
conda install jupyter pandas numpy matplotlib seaborn scikit-learn scipy
```

### Requirements File for Reproducibility
```
# requirements.txt
pandas==1.5.3
numpy==1.24.2
matplotlib==3.7.1
seaborn==0.12.2
scikit-learn==1.2.2
scipy==1.10.1
```

Install with: `pip install -r requirements.txt`

---

## Further Reading

Refer to official documentation and resources:
- **Libraries**:
  - pandas: https://pandas.pydata.org/docs/
  - numpy: https://numpy.org/doc/
  - matplotlib: https://matplotlib.org/stable/contents.html
  - seaborn: https://seaborn.pydata.org/
  - scikit-learn: https://scikit-learn.org/stable/
- **Learning Resources**:
  - Kaggle Learn: https://www.kaggle.com/learn
  - Python Data Science Handbook: https://jakevdp.github.io/PythonDataScienceHandbook/
  - Scikit-learn Tutorials: https://scikit-learn.org/stable/tutorial/
- **Best Practices**:
  - Reproducible Research: https://the-turing-way.netlify.app/
  - Cookiecutter Data Science: https://drivendata.github.io/cookiecutter-data-science/

---

## Version History

- v1.0.0 (2026-02-06): Initial release
  - Mandatory 4-step workflow for Jupyter notebook tasks
  - Support for EDA, statistical analysis, machine learning, visualization
  - Production-quality code generation with error handling
  - Project memory integration for pattern persistence
  - Template-based notebook structure
