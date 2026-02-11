---
id: "python/ml_patterns"
domain: python
title: "Machine Learning Patterns"
type: framework
estimatedTokens: 1050
loadingStrategy: onDemand
version: "1.0.0"
lastUpdated: "2026-02-10"
sections:
  - name: "Common Anti-Patterns"
    estimatedTokens: 102
    keywords: [anti-patterns]
  - name: "Data Preparation Issues"
    estimatedTokens: 61
    keywords: [data, preparation, issues]
  - name: "Model Training Issues"
    estimatedTokens: 66
    keywords: [model, training, issues]
  - name: "Evaluation Issues"
    estimatedTokens: 54
    keywords: [evaluation, issues]
  - name: "Common Detection Patterns"
    estimatedTokens: 144
    keywords: [detection, patterns]
  - name: "Framework-Specific Patterns"
    estimatedTokens: 78
    keywords: [framework-specific, patterns]
  - name: "Reproducibility Checklist"
    estimatedTokens: 39
    keywords: [reproducibility, checklist]
  - name: "Tools"
    estimatedTokens: 46
    keywords: [tools]
  - name: "Official Resources"
    estimatedTokens: 24
    keywords: [official, resources]
tags: [python, ml, pytorch, tensorflow, sklearn, reproducibility, training]
---

# Machine Learning Patterns

Quick reference for ML best practices with PyTorch, TensorFlow, and scikit-learn. For detailed examples, see official documentation.

---

## Common Anti-Patterns

| Anti-Pattern | What to Look For | Better Approach | Learn More |
|--------------|------------------|-----------------|------------|
| **No random seed** | Missing `random.seed()`, `np.random.seed()` | Set seeds for reproducibility | [Reproducibility](https://pytorch.org/docs/stable/notes/randomness.html) |
| **Data leakage** | Fit scaler/encoder on entire dataset | Fit only on training data | [Data leakage](https://scikit-learn.org/stable/common_pitfalls.html#data-leakage) |
| **No train/val/test split** | Training and testing on same data | Split data properly | [train_test_split](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html) |
| **Loading full dataset** | `pd.read_csv()` for large files | Use chunking or Dask | [Dask](https://dask.org/) |
| **Not saving models** | No model checkpointing | Save checkpoints during training | [Model saving](https://pytorch.org/tutorials/beginner/saving_loading_models.html) |
| **Ignoring class imbalance** | No handling of imbalanced datasets | Use class weights or resampling | [Imbalanced-learn](https://imbalanced-learn.org/) |
| **No validation metrics** | Only training loss/accuracy | Track validation metrics | [Metrics](https://scikit-learn.org/stable/modules/model_evaluation.html) |

---

## Data Preparation Issues

| Issue | Detection Pattern | Best Practice |
|-------|-------------------|---------------|
| **No normalization** | Raw features to model | Scale/normalize features |
| **Fit scaler on test data** | `scaler.fit(X_test)` | Fit only on training data |
| **Missing value handling** | No `.fillna()` or `.dropna()` | Handle missing values explicitly |
| **Data leakage in pipelines** | Transform before split | Split first, then transform |
| **Not using pipelines** | Manual transformation steps | Use `sklearn.pipeline.Pipeline` |

[Data preprocessing](https://scikit-learn.org/stable/modules/preprocessing.html)

---

## Model Training Issues

| Issue | Detection Pattern | Recommended Fix |
|-------|-------------------|-----------------|
| **No early stopping** | Training for fixed epochs | Use early stopping with patience |
| **No learning rate scheduling** | Static learning rate | Use LR schedulers |
| **Overfitting** | Train acc >> Val acc | Add regularization, dropout, data augmentation |
| **Not shuffling data** | Sequential training | Shuffle data each epoch |
| **Gradient explosion/vanishing** | NaN loss, very small gradients | Use gradient clipping, batch norm |

[Training neural networks](https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html)

---

## Evaluation Issues

| Issue | Detection Pattern | Best Practice |
|-------|-------------------|---------------|
| **Only using accuracy** | No precision/recall/F1 | Use appropriate metrics for task |
| **No cross-validation** | Single train/test split | Use k-fold cross-validation |
| **Test data in hyperparameter tuning** | GridSearch on test set | Use separate validation set |
| **Not tracking experiments** | No logging of results | Use MLflow, Weights & Biases, TensorBoard |

[Model evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html)

---

## Common Detection Patterns

```python
# ❌ No random seed
from sklearn.model_selection import train_test_split
X_train, X_test = train_test_split(X, y)  # Different split each time!

# ✅ With random seed
X_train, X_test = train_test_split(X, y, random_state=42)
np.random.seed(42)
torch.manual_seed(42)

# ❌ Data leakage (scaler fit on all data)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test = train_test_split(X_scaled, y)

# ✅ Proper scaling
X_train, X_test = train_test_split(X, y)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # Fit on train only
X_test_scaled = scaler.transform(X_test)        # Transform test

# ❌ No validation set
model.fit(X_train, y_train)
score = model.score(X_test, y_test)  # Using test for validation!

# ✅ Separate validation set
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5)

model.fit(X_train, y_train)
val_score = model.score(X_val, y_val)  # Validation
test_score = model.score(X_test, y_test)  # Final test

# ❌ Not using pipelines
X_scaled = scaler.fit_transform(X_train)
X_selected = selector.fit_transform(X_scaled, y_train)
model.fit(X_selected, y_train)

# ✅ Using pipeline
from sklearn.pipeline import Pipeline

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('selector', SelectKBest(k=10)),
    ('model', RandomForestClassifier())
])
pipeline.fit(X_train, y_train)

# ❌ No model saving
model.fit(X_train, y_train)
# Model lost if process crashes!

# ✅ Save model
import joblib
joblib.dump(model, 'model.pkl')
# Or PyTorch:
torch.save(model.state_dict(), 'model.pth')
```

---

## Framework-Specific Patterns

### PyTorch

```python
# ❌ Not calling .train() / .eval()
model(data)  # Uses training mode always

# ✅ Proper mode switching
model.train()
output = model(train_data)

model.eval()
with torch.no_grad():
    output = model(test_data)

# ❌ Not zeroing gradients
for epoch in range(epochs):
    output = model(data)
    loss.backward()  # Gradients accumulate!
    optimizer.step()

# ✅ Zero gradients
for epoch in range(epochs):
    optimizer.zero_grad()
    output = model(data)
    loss.backward()
    optimizer.step()
```

[PyTorch best practices](https://pytorch.org/tutorials/beginner/former_torchies/nn_tutorial.html)

### TensorFlow/Keras

```python
# ❌ No callbacks
model.fit(X_train, y_train, epochs=100)  # May overfit

# ✅ With callbacks
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

callbacks = [
    EarlyStopping(patience=10, restore_best_weights=True),
    ModelCheckpoint('best_model.h5', save_best_only=True)
]
model.fit(X_train, y_train, validation_data=(X_val, y_val), callbacks=callbacks)
```

[Keras callbacks](https://www.tensorflow.org/api_docs/python/tf/keras/callbacks)

---

## Reproducibility Checklist

- [ ] Set random seeds (`random`, `numpy`, `torch`/`tensorflow`)
- [ ] Use deterministic algorithms where possible
- [ ] Log library versions
- [ ] Save data preprocessing steps
- [ ] Document train/val/test split strategy
- [ ] Save model architecture and hyperparameters
- [ ] Track experiments (MLflow, W&B)

---

## Tools

| Tool | Purpose | Link |
|------|---------|------|
| **MLflow** | Experiment tracking | [MLflow](https://mlflow.org/) |
| **Weights & Biases** | Experiment tracking, visualization | [W&B](https://wandb.ai/) |
| **TensorBoard** | Visualization for TensorFlow/PyTorch | [TensorBoard](https://www.tensorflow.org/tensorboard) |
| **DVC** | Data version control | [DVC](https://dvc.org/) |
| **Optuna** | Hyperparameter optimization | [Optuna](https://optuna.org/) |
| **SHAP** | Model interpretability | [SHAP](https://shap.readthedocs.io/) |

---

## Official Resources

- **scikit-learn**: https://scikit-learn.org/stable/
- **PyTorch**: https://pytorch.org/docs/
- **TensorFlow**: https://www.tensorflow.org/api_docs
- **Keras**: https://keras.io/api/
- **MLOps best practices**: https://ml-ops.org/
- **Papers with Code**: https://paperswithcode.com/

---

**Version**: 1.0.0 (Compacted)
**Last Updated**: 2025-11-14
**Maintained For**: python-code-review skill
