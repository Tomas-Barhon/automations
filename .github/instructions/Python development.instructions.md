---
applyTo: '**/*.py'
---
# Python Code Standards & Best Practices

## Project Context
- **Dependency Management**: uv
- **Code Formatter**: ruff
- **Python Version**: 3.11+
- **Primary Domain**: Data Science (scikit-learn, TensorFlow, PyTorch, Darts)

## Code Quality Principles

### PEP 8 Compliance
- Strictly follow PEP 8 guidelines
- Use ruff for automatic formatting and linting
- Maximum line length: 88 characters (Black-compatible)
- Use meaningful variable names - avoid single letters except in comprehensions/loops

### Type Hints (Non-Negotiable)
- All function signatures MUST include type hints
- Use modern Python 3.11+ syntax: `list[str]`, `dict[str, int]`, not `List[str]`, `Dict[str, int]`
- Use `Optional[T]` or `T | None` for nullable types
- Use `collections.abc` types for abstract collections when appropriate

```python
def process_data(data: list[float], threshold: float = 0.5) -> dict[str, float]:
    """Process numerical data above threshold."""
    ...
```

### Object-Oriented Programming

#### SOLID Principles
1. **Single Responsibility**: Each class/function does ONE thing well
2. **Open/Closed**: Open for extension, closed for modification
3. **Liskov Substitution**: Subtypes must be substitutable for base types
4. **Interface Segregation**: Many specific interfaces over one general interface
5. **Dependency Inversion**: Depend on abstractions, not concretions

#### Class Design
- Prefer composition over inheritance
- Use abstract base classes (`abc.ABC`) for interfaces
- Keep classes focused and cohesive
- Avoid "god classes" - split complex classes into smaller, specialized ones
- Use dataclasses for simple data containers

```python
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class DataConfig:
    """Configuration for data processing."""
    threshold: float
    normalize: bool = True

class DataProcessor(ABC):
    """Abstract base for data processors."""

    @abstractmethod
    def process(self, data: list[float]) -> list[float]:
        """Process the input data."""
        pass
```

### Function Design
- Functions should be small and focused (ideally < 20 lines)
- Extract complex logic into separate helper functions
- Avoid deeply nested code (max 2-3 levels)
- Use early returns to reduce nesting
- Business logic should be in separate, testable functions

```python
# Good: Flat structure with early returns
def validate_and_process(data: list[float]) -> list[float]:
    """Validate and process data."""
    if not data:
        return []

    if not all(isinstance(x, (int, float)) for x in data):
        raise ValueError("All elements must be numeric")

    return [x * 2 for x in data if x > 0]
```

### Documentation Standards

#### Docstrings (Numpy Style - Required)
- All public modules, classes, methods, and functions MUST have docstrings
- Use Numpy-style docstrings

```python
def train_model(X: np.ndarray, y: np.ndarray, epochs: int = 100) -> Model:
    """
    Train a machine learning model on provided data.

    Parameters
    ----------
    X : np.ndarray
        Training features of shape (n_samples, n_features).
    y : np.ndarray
        Target values of shape (n_samples,).
    epochs : int, optional
        Number of training epochs, by default 100.

    Returns
    -------
    Model
        Trained model instance.

    Raises
    ------
    ValueError
        If X and y have incompatible shapes.

    Examples
    --------
    >>> X = np.random.rand(100, 5)
    >>> y = np.random.rand(100)
    >>> model = train_model(X, y, epochs=50)
    """
    ...
```

#### Self-Documenting Code
- Prefer clear variable/function names over comments
- Use comments only for "why", not "what"
- Extract complex expressions into well-named variables

```python
# Good: Self-documenting
outlier_threshold = mean + 3 * std
is_outlier = value > outlier_threshold

# Avoid: Needs comments to understand
threshold = m + 3 * s  # Check if value exceeds 3 standard deviations
```

### Logging Standards

#### Global Logger Configuration
- Define ONE global logger per project in a central module
- Import and use this logger across all modules
- NO print statements for logging purposes

```python
# src/config/logging_config.py
import logging
import sys
from datetime import datetime

def setup_logger(name: str = "project_logger") -> logging.Logger:
    """
    Configure and return global logger.

    Parameters
    ----------
    name : str, optional
        Logger name, by default "project_logger".

    Returns
    -------
    logging.Logger
        Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

# Global logger instance
logger = setup_logger()
```

#### Usage in Modules
```python
# src/models/train.py
from src.config.logging_config import logger

def train_model(data: pd.DataFrame) -> Model:
    """Train model on provided data."""
    logger.info("Starting model training")
    logger.debug(f"Training data shape: {data.shape}")

    try:
        model = fit_model(data)
        logger.info("Model training completed successfully")
        return model
    except Exception as e:
        logger.error(f"Training failed: {e}")
        raise
```

#### Log Levels
- **DEBUG**: Detailed diagnostic information
- **INFO**: General informational messages (default for important steps)
- **WARNING**: Warning messages for unexpected but handled situations
- **ERROR**: Error messages for failures
- **CRITICAL**: Critical errors requiring immediate attention

### Error Handling
- Use specific exception types, not bare `except:`
- Raise custom exceptions for domain-specific errors
- Log errors before re-raising
- Provide helpful error messages with context

```python
class DataValidationError(Exception):
    """Raised when data validation fails."""
    pass

def validate_data(data: pd.DataFrame) -> None:
    """
    Validate input data structure.

    Parameters
    ----------
    data : pd.DataFrame
        Input data to validate.

    Raises
    ------
    DataValidationError
        If data validation fails.
    """
    if data.empty:
        logger.error("Received empty dataframe")
        raise DataValidationError("Data cannot be empty")

    required_columns = {'feature_1', 'feature_2', 'target'}
    missing = required_columns - set(data.columns)

    if missing:
        logger.error(f"Missing required columns: {missing}")
        raise DataValidationError(f"Missing columns: {missing}")
```

### Testing Standards
- Focus on unit tests with pytest
- Test public interfaces, not implementation details
- Use fixtures for common test setup
- Aim for meaningful test coverage, not 100%
- Test edge cases and error conditions

```python
import pytest
from src.models.processor import DataProcessor

@pytest.fixture
def sample_data() -> list[float]:
    """Provide sample data for tests."""
    return [1.0, 2.0, 3.0, 4.0, 5.0]

def test_processor_filters_negative(sample_data: list[float]) -> None:
    """Test that processor removes negative values."""
    processor = DataProcessor(threshold=0.0)
    result = processor.process(sample_data + [-1.0, -2.0])
    assert all(x >= 0 for x in result)
```

### Data Science Specific Standards

#### Reproducibility
- Set random seeds for reproducibility
- Log hyperparameters and configuration
- Version datasets when possible

```python
import numpy as np
import random
import tensorflow as tf

def set_seeds(seed: int = 42) -> None:
    """Set random seeds for reproducibility."""
    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)
    logger.info(f"Random seeds set to {seed}")
```

#### Data Validation
- Validate data early in the pipeline
- Check for NaN, infinity, and data types
- Log data statistics during processing

#### Notebook vs Module Organization
- **Notebooks** (`notebooks/`): Exploratory analysis, visualizations, final results
- **Modules** (`src/`): Reusable logic, classes, data processing, model training
- Import from `src/` into notebooks - don't duplicate logic

### Project Structure
```
project/
├── data/
│   ├── raw/
│   ├── processed/
│   └── external/
├── notebooks/
│   ├── exploratory/
│   └── final/
├── src/
│   ├── __init__.py
│   ├── config/
│   │   └── logging_config.py
│   ├── data/
│   │   └── preprocessing.py
│   ├── models/
│   │   ├── train.py
│   │   └── evaluate.py
│   └── utils/
│       └── helpers.py
├── tests/
│   └── test_models/
├── scripts/
├── IMPROVEMENTS.md
├── pyproject.toml
└── README.md
```

### Code Review & Improvements
- Maintain `IMPROVEMENTS.md` for tracking technical debt
- Document issues with affected files and priority
- Update after addressing items

### Import Organization
- Group imports: standard library, third-party, local
- Use absolute imports from project root
- Sort alphabetically within groups

```python
# Standard library
import logging
from pathlib import Path

# Third-party
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

# Local
from src.config.logging_config import logger
from src.data.preprocessing import clean_data
```

## Summary
Write code that is:
- **Readable**: Self-documenting with clear names
- **Maintainable**: Modular, tested, and well-organized
- **Type-safe**: Comprehensive type hints
- **Professional**: Enterprise-grade OOP principles
- **Debuggable**: Proper logging, no print statements
