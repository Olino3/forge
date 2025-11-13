# Machine Learning Patterns (PyTorch/TensorFlow/sklearn)

This file contains ML-specific patterns and best practices for PyTorch, TensorFlow, and scikit-learn code.

## General ML Best Practices

### Data Split and Reproducibility

**Good Pattern**:
```python
import numpy as np
import random
import torch

# Set seeds for reproducibility
def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    # For deterministic behavior (may impact performance)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

set_seed(42)

# Proper train/val/test split
from sklearn.model_selection import train_test_split

X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
)
```

---

## PyTorch Patterns

### Model Definition

**Good Pattern**:
```python
import torch
import torch.nn as nn

class MyModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(MyModel, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(p=0.5)
        self.fc2 = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.dropout(out)
        out = self.fc2(out)
        return out

# Initialize model
model = MyModel(input_size=784, hidden_size=256, num_classes=10)

# Move to device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)
```

**Anti-Pattern**:
```python
# WRONG - No proper module structure
class BadModel:
    def __init__(self):
        self.w1 = torch.randn(784, 256)
        self.w2 = torch.randn(256, 10)

    def forward(self, x):
        h = torch.matmul(x, self.w1)
        return torch.matmul(h, self.w2)
# Weights won't be tracked, can't use optimizer!
```

### Training Loop

**Good Pattern**:
```python
def train_epoch(model, dataloader, criterion, optimizer, device):
    model.train()  # Set to training mode
    total_loss = 0
    correct = 0
    total = 0

    for batch_idx, (data, target) in enumerate(dataloader):
        data, target = data.to(device), target.to(device)

        # Zero gradients
        optimizer.zero_grad()

        # Forward pass
        output = model(data)
        loss = criterion(output, target)

        # Backward pass
        loss.backward()

        # Optional: Gradient clipping
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

        # Update weights
        optimizer.step()

        # Track metrics
        total_loss += loss.item()
        _, predicted = output.max(1)
        total += target.size(0)
        correct += predicted.eq(target).sum().item()

    return total_loss / len(dataloader), 100. * correct / total

def validate(model, dataloader, criterion, device):
    model.eval()  # Set to evaluation mode
    total_loss = 0
    correct = 0
    total = 0

    with torch.no_grad():  # Disable gradient computation
        for data, target in dataloader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            loss = criterion(output, target)

            total_loss += loss.item()
            _, predicted = output.max(1)
            total += target.size(0)
            correct += predicted.eq(target).sum().item()

    return total_loss / len(dataloader), 100. * correct / total
```

**Anti-Patterns**:
```python
# WRONG - Not calling model.train()/model.eval()
# WRONG - Not using torch.no_grad() during validation
# WRONG - Not moving data to device
# WRONG - Forgetting to zero_grad()
# WRONG - Using loss instead of loss.item() (memory leak)
```

### Saving and Loading Models

**Good Pattern**:
```python
# Save checkpoint
checkpoint = {
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss,
    'config': model_config
}
torch.save(checkpoint, 'checkpoint.pt')

# Load checkpoint
checkpoint = torch.load('checkpoint.pt', map_location=device)
model.load_state_dict(checkpoint['model_state_dict'])
optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
epoch = checkpoint['epoch']
loss = checkpoint['loss']

# For inference only
torch.save(model.state_dict(), 'model_weights.pt')
model.load_state_dict(torch.load('model_weights.pt'))
model.eval()
```

**Anti-Pattern**:
```python
# WRONG - Saving entire model (less flexible)
torch.save(model, 'model.pt')  # Not recommended

# WRONG - Not using map_location (fails if saved on GPU, loaded on CPU)
model = torch.load('model.pt')  # May crash!
```

### DataLoader Best Practices

**Good Pattern**:
```python
from torch.utils.data import Dataset, DataLoader

class CustomDataset(Dataset):
    def __init__(self, data, targets, transform=None):
        self.data = data
        self.targets = targets
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        sample = self.data[idx]
        target = self.targets[idx]

        if self.transform:
            sample = self.transform(sample)

        return sample, target

# Create DataLoader
train_loader = DataLoader(
    train_dataset,
    batch_size=64,
    shuffle=True,  # Shuffle training data
    num_workers=4,  # Parallel data loading
    pin_memory=True,  # Faster data transfer to GPU
    drop_last=True  # Drop incomplete last batch
)

val_loader = DataLoader(
    val_dataset,
    batch_size=64,
    shuffle=False,  # Don't shuffle validation data
    num_workers=4,
    pin_memory=True
)
```

---

## TensorFlow/Keras Patterns

### Model Definition

**Good Pattern**:
```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Functional API (recommended for complex models)
def create_model(input_shape, num_classes):
    inputs = keras.Input(shape=input_shape)
    x = layers.Dense(256, activation='relu')(inputs)
    x = layers.Dropout(0.5)(x)
    x = layers.Dense(128, activation='relu')(x)
    outputs = layers.Dense(num_classes, activation='softmax')(x)

    model = keras.Model(inputs=inputs, outputs=outputs, name='my_model')
    return model

model = create_model(input_shape=(784,), num_classes=10)

# Compile model
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Sequential API (for simple models)
model = keras.Sequential([
    layers.Dense(256, activation='relu', input_shape=(784,)),
    layers.Dropout(0.5),
    layers.Dense(128, activation='relu'),
    layers.Dense(10, activation='softmax')
])
```

### Training with Callbacks

**Good Pattern**:
```python
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau

# Callbacks
callbacks = [
    # Save best model
    ModelCheckpoint(
        'best_model.h5',
        monitor='val_loss',
        save_best_only=True,
        mode='min'
    ),

    # Early stopping
    EarlyStopping(
        monitor='val_loss',
        patience=10,
        restore_best_weights=True
    ),

    # Learning rate reduction
    ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=5,
        min_lr=1e-6
    ),

    # TensorBoard
    tf.keras.callbacks.TensorBoard(
        log_dir='./logs',
        histogram_freq=1
    )
]

# Train
history = model.fit(
    X_train, y_train,
    batch_size=64,
    epochs=100,
    validation_data=(X_val, y_val),
    callbacks=callbacks,
    verbose=1
)
```

### Custom Training Loop

**Good Pattern**:
```python
@tf.function  # Compile to graph for performance
def train_step(model, x, y, loss_fn, optimizer):
    with tf.GradientTape() as tape:
        predictions = model(x, training=True)
        loss = loss_fn(y, predictions)

    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))

    return loss

@tf.function
def val_step(model, x, y, loss_fn):
    predictions = model(x, training=False)
    loss = loss_fn(y, predictions)
    return loss

# Training loop
epochs = 100
for epoch in range(epochs):
    # Training
    train_loss = []
    for x_batch, y_batch in train_dataset:
        loss = train_step(model, x_batch, y_batch, loss_fn, optimizer)
        train_loss.append(loss)

    # Validation
    val_loss = []
    for x_batch, y_batch in val_dataset:
        loss = val_step(model, x_batch, y_batch, loss_fn)
        val_loss.append(loss)

    print(f"Epoch {epoch}: Train Loss: {np.mean(train_loss):.4f}, "
          f"Val Loss: {np.mean(val_loss):.4f}")
```

---

## scikit-learn Patterns

### Pipeline Pattern

**Good Pattern**:
```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier

# Create pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('pca', PCA(n_components=50)),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Fit pipeline
pipeline.fit(X_train, y_train)

# Predict
y_pred = pipeline.predict(X_test)

# Evaluate
from sklearn.metrics import classification_report, confusion_matrix
print(classification_report(y_test, y_pred))
```

### Cross-Validation

**Good Pattern**:
```python
from sklearn.model_selection import cross_val_score, StratifiedKFold

# K-fold cross-validation
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=cv, scoring='accuracy')

print(f"Cross-validation scores: {scores}")
print(f"Mean accuracy: {scores.mean():.3f} (+/- {scores.std() * 2:.3f})")

# Grid search with cross-validation
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=5,
    scoring='accuracy',
    n_jobs=-1,
    verbose=1
)

grid_search.fit(X_train, y_train)
print(f"Best parameters: {grid_search.best_params_}")
print(f"Best score: {grid_search.best_score_:.3f}")
```

### Feature Engineering

**Good Pattern**:
```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# Define transformers for different column types
numeric_features = ['age', 'income', 'score']
categorical_features = ['category', 'location']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

# Create pipeline with preprocessing
full_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier())
])

full_pipeline.fit(X_train, y_train)
```

---

## Common ML Anti-Patterns

### Data Leakage

**Anti-Pattern**:
```python
# WRONG - Scaling before split (data leakage!)
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # Uses information from entire dataset!
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y)
```

**Good Pattern**:
```python
# CORRECT - Split first, then scale
X_train, X_test, y_train, y_test = train_test_split(X, y)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # Fit only on training data
X_test_scaled = scaler.transform(X_test)  # Transform test data with training stats
```

### Not Handling Class Imbalance

**Good Pattern**:
```python
# Check class distribution
from collections import Counter
print(Counter(y_train))

# Option 1: Class weights
from sklearn.utils.class_weight import compute_class_weight

class_weights = compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)
class_weight_dict = dict(enumerate(class_weights))

model.fit(X_train, y_train, class_weight=class_weight_dict)

# Option 2: Resampling (for sklearn)
from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

# Option 3: stratify in train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, stratify=y, test_size=0.2
)
```

### Memory Leaks in Training

**Anti-Pattern - PyTorch**:
```python
# WRONG - Accumulates computation graph
for epoch in range(epochs):
    for data, target in dataloader:
        output = model(data)
        loss = criterion(output, target)
        losses.append(loss)  # DON'T store tensors!
```

**Good Pattern**:
```python
# CORRECT - Store only values
for epoch in range(epochs):
    for data, target in dataloader:
        output = model(data)
        loss = criterion(output, target)
        losses.append(loss.item())  # Detach from graph
```

### Not Using Proper Evaluation Metrics

**Good Pattern**:
```python
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report
)

# For binary classification
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")
print(f"Precision: {precision_score(y_test, y_pred):.3f}")
print(f"Recall: {recall_score(y_test, y_pred):.3f}")
print(f"F1: {f1_score(y_test, y_pred):.3f}")
print(f"ROC-AUC: {roc_auc_score(y_test, y_pred_proba):.3f}")

# Detailed report
print(classification_report(y_test, y_pred))

# For regression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
```

---

## ML Code Review Checklist

### Data Handling
- [ ] Train/val/test split done correctly (no data leakage)
- [ ] Random seed set for reproducibility
- [ ] Data preprocessing fit only on training data
- [ ] Class imbalance addressed
- [ ] Missing values handled properly
- [ ] Feature scaling applied when necessary

### Model
- [ ] Model architecture is appropriate for task
- [ ] Regularization used (dropout, L1/L2, early stopping)
- [ ] Activation functions appropriate
- [ ] Loss function matches the task
- [ ] Optimizer and learning rate reasonable

### Training
- [ ] Proper train/validation split or cross-validation
- [ ] model.train()/model.eval() used correctly (PyTorch)
- [ ] torch.no_grad() used during validation
- [ ] Gradients zeroed before backward pass
- [ ] Model checkpointing implemented
- [ ] Early stopping to prevent overfitting
- [ ] Learning rate scheduling considered

### Evaluation
- [ ] Appropriate metrics for the task
- [ ] Model evaluated on held-out test set
- [ ] Results include confidence intervals or std dev
- [ ] Confusion matrix analyzed for classification
- [ ] Residual plots checked for regression

### Code Quality
- [ ] Seeds set for reproducibility
- [ ] Device management (CPU/GPU) handled
- [ ] Memory leaks avoided (use .item(), detach())
- [ ] Code is modular and reusable
- [ ] Logging of metrics and hyperparameters
- [ ] Model and data versioning considered

### Production Considerations
- [ ] Model serialization/deserialization tested
- [ ] Inference latency acceptable
- [ ] Model size reasonable for deployment
- [ ] Input validation in inference code
- [ ] Error handling for edge cases
- [ ] Monitoring and logging in place

## Performance Optimization

### GPU Utilization
```python
# Check GPU availability
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

# Move model and data to GPU
model = model.to(device)
data = data.to(device)

# Use mixed precision training (faster, less memory)
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

for data, target in dataloader:
    optimizer.zero_grad()

    with autocast():
        output = model(data)
        loss = criterion(output, target)

    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```

### Batch Size Tuning
```python
# Larger batches = faster training but more memory
# Smaller batches = better generalization

# Find optimal batch size
def find_batch_size(model, sample_data):
    batch_size = 1
    while True:
        try:
            batch = sample_data[:batch_size].to(device)
            output = model(batch)
            loss = criterion(output, targets[:batch_size])
            loss.backward()
            batch_size *= 2
        except RuntimeError:  # OOM
            return batch_size // 2
```

## References

- PyTorch Documentation: https://pytorch.org/docs/
- TensorFlow Documentation: https://www.tensorflow.org/api_docs
- scikit-learn Documentation: https://scikit-learn.org/stable/
- Deep Learning by Ian Goodfellow
- Hands-On Machine Learning by Aurélien Géron
