# Testing Guide for News Application Server

This directory contains comprehensive unit tests for the News Application server components.

## Directory Structure

```
tests/
├── __init__.py              # Makes tests a Python package
├── conftest.py              # Pytest configuration and fixtures
├── test_admin_service.py    # Tests for AdminService
├── test_base_service.py     # Tests for BaseService
└── README.md               # This file
```

## Prerequisites

1. **Install Python dependencies for testing:**
   ```bash
   pip install -r requirements-test.txt
   ```

2. **Make sure you're in the server directory:**
   ```bash
   cd NewsApplication/NewsApp/server
   ```

## Running Tests

### Method 1: Using the Test Runner Script (Recommended)

The `run_tests.py` script provides a convenient way to run tests with various options:

#### Basic Usage
```bash
# Run all tests
python run_tests.py

# Run with verbose output
python run_tests.py -v

# Run with coverage report
python run_tests.py -c

# Run specific test file
python run_tests.py -f admin_service

# Run specific test function
python run_tests.py -f admin_service -t test_get_external_servers_success

# Run tests with specific markers
python run_tests.py -m unit

# Run tests in parallel
python run_tests.py -p

# Generate HTML test report
python run_tests.py --html
```

#### Advanced Usage Examples
```bash
# Run admin service tests with coverage and verbose output
python run_tests.py -v -c -m admin

# Run base service tests and generate HTML report
python run_tests.py -f base_service --html

# Run all unit tests in parallel with coverage
python run_tests.py -m unit -p -c
```

### Method 2: Using pytest directly

```bash
# Run all tests
python -m pytest

# Run with verbose output
python -m pytest -v

# Run specific test file
python -m pytest tests/test_admin_service.py

# Run specific test function
python -m pytest tests/test_admin_service.py::TestAdminService::test_get_external_servers_success

# Run tests with coverage
python -m pytest --cov=services --cov=utils --cov=repositories --cov-report=html:htmlcov

# Run tests with specific markers
python -m pytest -m unit

# Run tests in parallel
python -m pytest -n auto
```

## Test Categories

### Unit Tests
- **AdminService Tests**: Test all methods of the AdminService class
- **BaseService Tests**: Test utility methods in the BaseService class

### Test Coverage
The tests cover:
- ✅ Success scenarios
- ✅ Error handling
- ✅ Edge cases
- ✅ Input validation
- ✅ Response format consistency
- ✅ Exception handling

## Test Fixtures

The `conftest.py` file provides common test fixtures:

- `mock_admin_repository`: Mocked AdminRepository for testing
- `sample_external_servers`: Sample external servers data
- `sample_categories`: Sample categories data
- `sample_keywords`: Sample keywords data

## Understanding Test Results

### Successful Test Run
```
============================= test session starts ==============================
platform win32 -- Python 3.x.x, pytest-7.4.3, pluggy-1.3.0
rootdir: C:\...\NewsApplication\NewsApp\server
plugins: cov-4.1.0, mock-3.12.0, html-4.1.1, xdist-3.3.1
collected 25 items

tests/test_admin_service.py ................. [ 68%]
tests/test_base_service.py ........ [100%]

============================== 25 passed in 2.34s ==============================
```

### Coverage Report
```
---------- coverage: platform win32, python 3.x.x-final-0 -----------
Name                           Stmts   Miss  Cover
--------------------------------------------------
services/admin_service.py         31      0   100%
services/base_service.py          27      0   100%
utils/custom_exceptions.py         7      0   100%
--------------------------------------------------
TOTAL                             65      0   100%
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Make sure you're in the server directory
   cd NewsApplication/NewsApp/server
   ```

2. **Module Not Found**
   ```bash
   # Install test dependencies
   pip install -r requirements-test.txt
   ```

3. **Permission Errors (Windows)**
   ```bash
   # Run PowerShell as Administrator or use
   python run_tests.py
   ```

### Debugging Tests

```bash
# Run with maximum verbosity
python run_tests.py -v -v

# Run specific failing test
python run_tests.py -f admin_service -t test_update_external_server_failure

# Run with print statements visible
python -m pytest -s tests/test_admin_service.py
```

## Adding New Tests

1. **Create a new test file** following the naming convention: `test_<service_name>.py`
2. **Import required modules** and use the fixtures from `conftest.py`
3. **Follow the test structure**:
   ```python
   class TestYourService:
       def setup_method(self):
           # Setup code
           pass
       
       def test_method_name(self, mock_repository):
           # Arrange
           # Act
           # Assert
           pass
   ```

4. **Run your new tests**:
   ```bash
   python run_tests.py -f your_service
   ```

## Continuous Integration

The test setup is designed to work with CI/CD pipelines. The `pytest.ini` file configures:
- Test discovery patterns
- Coverage reporting
- HTML test reports
- Parallel test execution

## Best Practices

1. **Test Naming**: Use descriptive test names that explain the scenario
2. **Arrange-Act-Assert**: Structure tests with clear sections
3. **Mocking**: Use mocks to isolate units under test
4. **Edge Cases**: Test boundary conditions and error scenarios
5. **Documentation**: Add docstrings to test methods explaining the test purpose 