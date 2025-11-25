# Testing Guide

Comprehensive testing documentation for the Alexa Roomba project.

## Table of Contents

- [Overview](#overview)
- [Test Infrastructure](#test-infrastructure)
- [Running Tests](#running-tests)
- [Test Organization](#test-organization)
- [Code Coverage](#code-coverage)
- [Writing Tests](#writing-tests)
- [CI/CD Integration](#cicd-integration)
- [Troubleshooting](#troubleshooting)

## Overview

This project uses pytest for comprehensive testing with the following features:

- **Unit Tests**: Fast tests for individual functions and classes
- **Integration Tests**: Tests for component interactions (with mocked hardware)
- **Hardware Tests**: Tests requiring actual Roomba hardware (marked but skipped by default)
- **Code Coverage**: Branch and line coverage analysis
- **Mocking**: Hardware-independent testing using mocks

### Test Statistics

- **280+ total tests** across 5 test modules
- **Unit tests**: 220+ tests for core functionality
- **Integration tests**: 40+ tests for robot control
- **Coverage**: Configured for branch and line coverage

## Test Infrastructure

### Dependencies

Install test dependencies:

```bash
pip install -r requirements.txt
```

Test dependencies include:
- `pytest>=7.0.0` - Testing framework
- `pytest-cov>=4.0.0` - Coverage plugin
- `pytest-mock>=3.10.0` - Mocking utilities

### Configuration

Test configuration is in `pytest.ini`:

```ini
[pytest]
testpaths = tests
addopts =
    -v                      # Verbose output
    --strict-markers        # Enforce marker registration
    --tb=short             # Short traceback format
    --cov=roomba           # Coverage for roomba package
    --cov-report=term-missing  # Show missing lines
    --cov-report=html      # HTML coverage report
    --cov-branch           # Branch coverage
```

### Test Markers

Tests are categorized with markers:

- `@pytest.mark.unit` - Unit tests (fast, no external dependencies)
- `@pytest.mark.integration` - Integration tests (mocked serial)
- `@pytest.mark.hardware` - Requires actual hardware (skipped by default)
- `@pytest.mark.slow` - Slow-running tests

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test Categories

```bash
# Run only unit tests (fast)
pytest -m unit

# Run only integration tests
pytest -m integration

# Run unit and integration tests
pytest -m "unit or integration"

# Skip slow tests
pytest -m "not slow"

# Skip hardware tests (default behavior)
pytest -m "not hardware"
```

### Run Specific Test Files

```bash
# Run utils tests only
pytest tests/test_utils.py

# Run multiple specific files
pytest tests/test_utils.py tests/test_sensors.py

# Run specific test class
pytest tests/test_utils.py::TestBitOfByte

# Run specific test method
pytest tests/test_utils.py::TestBitOfByte::test_extract_bit_0
```

### Verbose Output

```bash
# Show detailed test names
pytest -v

# Show even more detail (print statements, etc.)
pytest -vv

# Show test output even for passing tests
pytest -s
```

### Stop on First Failure

```bash
# Stop after first failure
pytest -x

# Stop after N failures
pytest --maxfail=3
```

### Parallel Execution

For faster test execution (requires pytest-xdist):

```bash
pip install pytest-xdist

# Run tests in parallel (auto-detect CPU count)
pytest -n auto

# Run with specific number of workers
pytest -n 4
```

## Test Organization

### Test Structure

```
tests/
├── __init__.py              # Test package initialization
├── conftest.py              # Shared fixtures and configuration
├── test_utils.py            # Utils module unit tests (91 tests)
├── test_sensors.py          # Sensors module unit tests (50+ tests)
├── test_music.py            # Music module unit tests (60+ tests)
├── test_create.py           # Create class integration tests (40+ tests)
└── test_config.py           # Config module tests (40+ tests)
```

### Test Modules

#### test_utils.py
Tests utility functions for bit operations and conversions:
- Mode string conversion
- Bit extraction from bytes
- Two's complement conversion
- Unsigned byte conversion
- Signed integer parsing
- Roundtrip conversion tests

#### test_sensors.py
Tests sensor constants and SensorFrame class:
- Sensor ID definitions
- SensorFrame initialization
- Sensor value ranges
- Bit mask interpretation
- Battery calculations

#### test_music.py
Tests MIDI note constants and durations:
- Note constant values
- Octave relationships
- Duration constants
- Song composition
- Music theory intervals

#### test_create.py
Integration tests for Create robot class:
- Robot initialization
- Movement commands
- Sensor reading
- Music playback
- Mode switching
- Error handling
- Real-world scenarios

#### test_config.py
Tests configuration module:
- Default values
- Platform detection
- Environment variables
- Logging configuration
- Constant validation

## Code Coverage

### Viewing Coverage

After running tests, coverage reports are generated:

```bash
# Run tests with coverage (automatic with pytest.ini)
pytest

# View terminal report (shows missing lines)
# Output appears after test results

# Open HTML coverage report
open htmlcov/index.html
```

### Coverage Reports

**Terminal Report** shows:
- Coverage percentage per module
- Line numbers of uncovered code
- Branch coverage statistics

**HTML Report** (`htmlcov/index.html`) provides:
- Interactive file browser
- Line-by-line coverage highlighting
- Branch coverage details
- Filterable by coverage percentage

### Coverage Goals

Target coverage metrics:
- **Overall**: 85%+ line coverage
- **Core modules**: 90%+ line coverage
- **Branch coverage**: 80%+ for critical paths

### Excluding Code from Coverage

To exclude code from coverage analysis:

```python
# Exclude single line
code_line()  # pragma: no cover

# Exclude block
if debug:  # pragma: no cover
    debug_code()
```

Common exclusions:
- Debugging code
- Platform-specific unreachable code
- Abstract methods meant to be overridden

## Writing Tests

### Test Structure

Follow this pattern for test organization:

```python
"""
Module docstring describing what is tested.
"""

import pytest
from module import function_to_test


class TestFeatureName:
    """Test class for a specific feature."""

    @pytest.mark.unit
    def test_basic_case(self):
        """Test basic functionality."""
        result = function_to_test(input)
        assert result == expected

    @pytest.mark.unit
    @pytest.mark.parametrize("input,expected", [
        (1, 2),
        (2, 4),
        (3, 6),
    ])
    def test_multiple_inputs(self, input, expected):
        """Test with multiple inputs."""
        result = function_to_test(input)
        assert result == expected
```

### Using Fixtures

Fixtures provide reusable test components:

```python
@pytest.fixture
def sample_robot(mock_serial, monkeypatch):
    """Create a robot instance for testing."""
    monkeypatch.setattr('serial.Serial', lambda *args, **kwargs: mock_serial)
    robot = Create('/dev/ttyUSB0')
    return robot


def test_robot_movement(sample_robot):
    """Test using the robot fixture."""
    sample_robot.go(20, 0)
    assert sample_robot.ser.write.called
```

### Available Fixtures

Defined in `conftest.py`:

- **mock_serial**: Mocked serial port (no hardware needed)
- **sample_sensor_data**: Dictionary of sample sensor values
- **mock_create_instance**: Pre-configured Create instance with mocked serial
- **temp_config_file**: Temporary configuration file for testing

### Parametrized Tests

Test multiple inputs efficiently:

```python
@pytest.mark.unit
@pytest.mark.parametrize("velocity,expected_high,expected_low", [
    (0, 0, 0),
    (1, 0, 1),
    (500, 1, 244),
    (-500, 254, 12),
])
def test_velocity_conversion(velocity, expected_high, expected_low):
    """Test velocity to bytes conversion."""
    high, low = _toTwosComplement2Bytes(velocity)
    assert high == expected_high
    assert low == expected_low
```

### Mocking Serial Communication

For hardware-dependent code:

```python
from unittest.mock import Mock

def test_sensor_read(mock_create_instance):
    """Test reading sensors without hardware."""
    robot = mock_create_instance

    # Mock sensor response
    robot.ser.read = Mock(return_value=b'\x09\xC4')

    # Read sensors
    robot.sensors([BATTERY_CHARGE])

    # Verify command was sent
    assert robot.ser.write.called
```

### Testing Exceptions

```python
import pytest

def test_invalid_input():
    """Test that invalid input raises ValueError."""
    with pytest.raises(ValueError):
        function_with_validation(invalid_input)

def test_exception_message():
    """Test exception message content."""
    with pytest.raises(ValueError, match="Invalid port"):
        create_with_bad_port()
```

### Best Practices

1. **One assertion per test** (generally)
   - Makes failures easier to diagnose
   - Exception: Parametrized tests may have multiple related assertions

2. **Test names should describe what is tested**
   ```python
   def test_forward_movement_sends_drive_command()  # Good
   def test_1()  # Bad
   ```

3. **Use docstrings** to explain test purpose
   ```python
   def test_battery_percentage(self):
       """Test battery percentage calculation with various charge levels."""
   ```

4. **Arrange-Act-Assert pattern**
   ```python
   def test_something(self):
       # Arrange: Set up test data
       robot = Create('/dev/test')

       # Act: Execute the code being tested
       result = robot.go(20, 0)

       # Assert: Verify the result
       assert result is not None
   ```

5. **Mock external dependencies**
   - Serial ports
   - File I/O
   - Network calls
   - Time-dependent code

6. **Test edge cases**
   - Boundary values (0, -1, max, min)
   - Empty inputs
   - Null/None values
   - Invalid inputs

## CI/CD Integration

### GitHub Actions

Example workflow (`.github/workflows/test.yml`):

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.7, 3.8, 3.9, '3.10', '3.11']

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run tests
      run: |
        pytest -m "not hardware"

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

### Travis CI

Example `.travis.yml`:

```yaml
language: python
python:
  - "3.7"
  - "3.8"
  - "3.9"
  - "3.10"
  - "3.11"

install:
  - pip install -r requirements.txt

script:
  - pytest -m "not hardware"

after_success:
  - codecov
```

### Pre-commit Hooks

Run tests before committing:

```bash
# .git/hooks/pre-commit
#!/bin/bash
echo "Running tests..."
pytest -m unit --quiet
if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi
```

## Troubleshooting

### Common Issues

#### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'roomba'`

**Solution**:
```bash
# Install package in development mode
pip install -e .

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

#### Fixture Not Found

**Problem**: `fixture 'mock_serial' not found`

**Solution**: Ensure `conftest.py` is in the tests directory and properly formatted.

#### Coverage Not Working

**Problem**: Coverage shows 0% or missing files

**Solution**:
```bash
# Ensure pytest-cov is installed
pip install pytest-cov

# Run with explicit coverage
pytest --cov=roomba --cov-report=term-missing
```

#### Tests Hang or Timeout

**Problem**: Tests appear to hang indefinitely

**Solution**:
- Check for blocking serial operations
- Ensure all serial calls are mocked
- Add timeout to long-running tests:
  ```python
  @pytest.mark.timeout(5)  # Requires pytest-timeout
  def test_something():
      ...
  ```

#### Platform-Specific Failures

**Problem**: Tests pass on one platform but fail on another

**Solution**:
```python
import platform
import pytest

@pytest.mark.skipif(platform.system() == "Windows", reason="Unix-only test")
def test_unix_specific():
    ...
```

### Debugging Failed Tests

#### Verbose Output

```bash
# Show more details
pytest -vv

# Show print statements
pytest -s

# Show local variables in tracebacks
pytest -l
```

#### Run Single Test

```bash
# Run just the failing test
pytest tests/test_utils.py::TestBitOfByte::test_extract_bit_0 -vv
```

#### Enter Debugger on Failure

```bash
# Drop into pdb on failure
pytest --pdb

# Drop into pdb on first failure
pytest -x --pdb
```

#### Use Print Debugging

```python
def test_something(self):
    result = function()
    print(f"DEBUG: result = {result}")  # Will show with -s flag
    assert result == expected
```

### Getting Help

If tests fail and you need help:

1. **Check test output** for specific error messages
2. **Run with `-vv`** for detailed output
3. **Check coverage report** to see what code is being tested
4. **Review test documentation** in test docstrings
5. **Check TROUBLESHOOTING.md** for known issues
6. **Open an issue** on GitHub with test output

## Hardware Tests

### Running Hardware Tests

Hardware tests require an actual Roomba connected via serial port:

```bash
# Run hardware tests (requires connected Roomba)
pytest -m hardware

# Run specific hardware test
pytest tests/test_hardware.py -m hardware -v
```

**Note**: Hardware tests are marked to skip by default. They should only be run when hardware is available.

### Writing Hardware Tests

```python
@pytest.mark.hardware
@pytest.mark.skip(reason="Requires actual Roomba hardware")
def test_real_robot_movement():
    """Test robot movement with actual hardware."""
    robot = Create('/dev/ttyUSB0')  # Real port
    robot.go(10, 0)
    time.sleep(1)
    robot.stop()
    robot.close()
```

### Safety Considerations

When running hardware tests:
- Ensure robot is on the floor or on a stand
- Clear the area around the robot
- Be ready to pick up the robot if needed
- Start with slow speeds for movement tests
- Always stop and close robot connection after tests

## Continuous Testing

### Watch Mode

For continuous testing during development (requires pytest-watch):

```bash
pip install pytest-watch

# Run tests on file changes
ptw
```

### VS Code Integration

Add to `.vscode/settings.json`:

```json
{
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.testing.pytestArgs": [
        "tests",
        "-v"
    ]
}
```

### PyCharm Integration

1. Go to Preferences → Tools → Python Integrated Tools
2. Set Testing → Default test runner to "pytest"
3. Right-click on tests directory → Run 'pytest in tests'

## Summary

- **Run all tests**: `pytest`
- **Run unit tests only**: `pytest -m unit`
- **Run with coverage**: `pytest --cov=roomba`
- **View HTML coverage**: `open htmlcov/index.html`
- **Add new tests**: Follow patterns in existing test files
- **Use fixtures**: Leverage `conftest.py` fixtures for common setup
- **CI/CD**: Integrate with GitHub Actions or Travis CI

For more information, see:
- [API Documentation](API.md)
- [Architecture Guide](ARCHITECTURE.md)
- [Troubleshooting](TROUBLESHOOTING.md)
- [pytest documentation](https://docs.pytest.org/)
