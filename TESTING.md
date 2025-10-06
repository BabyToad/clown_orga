# Testing Guide

This document describes how to run and write tests for the Workshop Allocation Tool.

## Running Tests

### Prerequisites

Install test dependencies:
```bash
pip install -r requirements.txt
```

### Quick Start

Run all tests:
```bash
# On Linux/Mac
./run_tests.sh

# On Windows
run_tests.bat

# Or directly with pytest
python -m pytest -v
```

### Running Specific Tests

Run a specific test file:
```bash
python -m pytest test_config.py -v
```

Run a specific test class:
```bash
python -m pytest test_data_handler.py::TestDataHandler -v
```

Run a specific test function:
```bash
python -m pytest test_optimizer.py::TestWorkshopOptimizer::test_basic_optimization -v
```

### Coverage Reports

Generate coverage report:
```bash
python -m pytest --cov=. --cov-report=html
```

View the report by opening `htmlcov/index.html` in your browser.

## Test Structure

### Unit Tests

- **test_config.py** - Tests for configuration management
  - Default values
  - Save/load functionality
  - Config persistence
  - Error handling

- **test_data_handler.py** - Tests for Excel import/export
  - Valid file import
  - Data validation
  - Error detection (missing columns, invalid data)
  - Workshop extraction
  - Excel export functionality

- **test_optimizer.py** - Tests for optimization algorithm
  - Basic optimization
  - Constraint satisfaction
  - Statistics calculation
  - Edge cases (empty students, popular workshops)

### Integration Tests

- **test_integration.py** - End-to-end workflow tests
  - Complete workflow (import → optimize → export)
  - Custom configurations
  - Large datasets
  - Data consistency

## Test Coverage

Current test coverage by module:

| Module | Coverage | Tests |
|--------|----------|-------|
| config.py | ~95% | 13 tests |
| data_handler.py | ~90% | 18 tests |
| optimizer.py | ~85% | 15 tests |
| Integration | ~80% | 12 tests |

**Total: 58+ comprehensive tests**

## Creating Test Data

Generate test Excel files:
```bash
python create_test_data.py
```

This creates:
- `example_students.xlsx` - 30 realistic students
- `test_small.xlsx` - 5 students for quick testing
- `test_incomplete.xlsx` - Missing wishes
- `test_duplicates.xlsx` - Duplicate wishes
- `test_large.xlsx` - 100 students
- `test_popular.xlsx` - Popular workshop scenario

## Writing New Tests

### Test Naming Convention

- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`

### Example Test

```python
import pytest
from your_module import YourClass

class TestYourClass:
    @pytest.fixture
    def instance(self):
        """Create test instance."""
        return YourClass()

    def test_feature(self, instance):
        """Test a specific feature."""
        result = instance.do_something()
        assert result == expected_value
```

### Best Practices

1. **Use fixtures** for setup/teardown
2. **Test edge cases** (empty input, null values, etc.)
3. **Use descriptive names** (`test_import_with_missing_columns`)
4. **One assertion per test** (generally)
5. **Mock external dependencies** (if needed)
6. **Use tmp_path** for file operations

### Testing Excel Files

Always use `tmp_path` fixture for temporary files:

```python
def test_excel_export(tmp_path):
    file_path = tmp_path / "test.xlsx"
    # ... create and test Excel file
    assert file_path.exists()
```

## Continuous Testing

For development, use pytest-watch to auto-run tests:
```bash
pip install pytest-watch
ptw
```

## Troubleshooting

### Import Errors

If you get import errors, make sure you're running pytest from the project root:
```bash
cd /path/to/clown_orga
python -m pytest
```

### Missing Dependencies

Install all dependencies:
```bash
pip install -r requirements.txt
```

### Slow Tests

Skip slow tests:
```bash
python -m pytest -m "not slow"
```

## Test Philosophy

Our tests follow these principles:

1. **Comprehensive** - Cover happy paths, edge cases, and error conditions
2. **Fast** - Unit tests run in milliseconds
3. **Independent** - Tests don't depend on each other
4. **Deterministic** - Same input always produces same output
5. **Readable** - Tests serve as documentation

## Adding New Features

When adding new features:

1. Write tests first (TDD)
2. Ensure existing tests still pass
3. Aim for >80% code coverage
4. Add integration tests for workflows
5. Update this documentation
