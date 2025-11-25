# Contributing to Alexa Roomba

Thank you for your interest in contributing to the Alexa Roomba project! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)
- [Community](#community)

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Git
- Basic understanding of Python and robotics
- (Optional) iRobot Roomba with serial interface

### First Steps

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/alexa_roomba.git
   cd alexa_roomba
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/antigenius0910/alexa_roomba.git
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Run tests** to ensure everything works:
   ```bash
   pytest
   ```

## How to Contribute

There are many ways to contribute to this project:

### 🐛 Reporting Bugs

Found a bug? Please check if it's already reported in [Issues](https://github.com/antigenius0910/alexa_roomba/issues). If not, create a new issue using the bug report template.

### 💡 Suggesting Enhancements

Have an idea for improvement? Open an issue using the feature request template to discuss it with the maintainers.

### 📝 Improving Documentation

Documentation improvements are always welcome! This includes:
- Fixing typos or clarifying existing docs
- Adding examples or tutorials
- Improving API documentation
- Translating documentation

### 💻 Contributing Code

Code contributions can include:
- Bug fixes
- New features
- Performance improvements
- Code refactoring
- Test coverage improvements

### 🧪 Testing

Help test the project:
- Test on different platforms (Windows, macOS, Linux, Raspberry Pi)
- Test with different Roomba models
- Add test cases for uncovered code paths
- Report hardware compatibility

## Development Setup

### Local Development Environment

1. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install development dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install pre-commit hooks** (optional but recommended):
   ```bash
   pip install pre-commit
   pre-commit install
   ```

### Running the Project

Without hardware:
```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=roomba --cov-report=html
```

With hardware:
```bash
# Set up environment variables
export ROOMBA_PORT=/dev/ttyUSB0

# Run examples
python examples/alexa_roomba.py
```

### Project Structure

```
alexa_roomba/
├── roomba/              # Core library
│   ├── __init__.py     # Main Create class
│   ├── commands.py     # Command constants
│   ├── music.py        # Music note definitions
│   ├── sensors.py      # Sensor definitions
│   └── utils.py        # Utility functions
├── examples/           # Example scripts
├── tests/              # Test suite
├── docs/               # Documentation
├── config.py           # Configuration
└── fauxmo/            # Fauxmo integration
```

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with some modifications:

- **Line length**: 100 characters (soft limit)
- **Indentation**: 4 spaces (no tabs)
- **Quotes**: Single quotes for strings, double quotes for docstrings
- **Imports**: Group in order: standard library, third-party, local

### Code Quality Tools

Run these before submitting:

```bash
# Code formatting (if using black)
black roomba/ tests/

# Linting (if using flake8)
flake8 roomba/ tests/

# Type checking (if using mypy)
mypy roomba/
```

### Documentation Standards

- **Docstrings**: Use Google-style docstrings
- **Comments**: Explain why, not what
- **Type hints**: Use for function signatures (Python 3.7+)

Example:
```python
def go(self, velocity: int, spin: int) -> None:
    """Move the robot with specified velocity and spin.

    Args:
        velocity: Forward velocity in cm/s (-50 to 50)
        spin: Rotational velocity in deg/s (-180 to 180)

    Raises:
        ValueError: If velocity or spin are out of range

    Example:
        >>> robot.go(20, 0)  # Move forward at 20 cm/s
    """
```

### Best Practices

1. **Keep functions small**: One function, one responsibility
2. **Avoid global state**: Use parameters and return values
3. **Handle errors gracefully**: Don't let exceptions crash the robot
4. **Write self-documenting code**: Clear variable and function names
5. **Add comments for complex logic**: Especially hardware protocols
6. **Test your changes**: Write tests for new features

## Testing Guidelines

### Writing Tests

- **Coverage**: Aim for 85%+ coverage for new code
- **Independence**: Tests should not depend on each other
- **Mocking**: Mock hardware dependencies (serial port)
- **Markers**: Use appropriate markers (@pytest.mark.unit, etc.)

### Test Structure

```python
import pytest
from roomba import Create

class TestFeature:
    """Tests for specific feature."""

    @pytest.mark.unit
    def test_basic_case(self):
        """Test description."""
        # Arrange
        expected = 42

        # Act
        result = function_under_test()

        # Assert
        assert result == expected
```

### Running Tests

```bash
# All tests
pytest

# Unit tests only (fast)
pytest -m unit

# With coverage
pytest --cov=roomba --cov-report=term-missing

# Specific test file
pytest tests/test_utils.py

# Specific test
pytest tests/test_utils.py::TestBitOfByte::test_extract_bit_0
```

See [docs/TESTING.md](docs/TESTING.md) for comprehensive testing guide.

## Commit Guidelines

### Commit Message Format

Use clear, descriptive commit messages:

```
<type>: <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `chore`: Maintenance tasks
- `style`: Formatting changes

**Example**:
```
feat: Add support for Roomba 900 series

Implements OI mode commands for Roomba 900 series robots.
Adds new sensor packet IDs for advanced sensors.

Closes #123
```

### Commit Best Practices

- **Atomic commits**: One logical change per commit
- **Present tense**: "Add feature" not "Added feature"
- **Imperative mood**: "Fix bug" not "Fixes bug"
- **Reference issues**: Use "Closes #123" or "Fixes #456"
- **Explain why**: Body should explain why the change was made

## Pull Request Process

### Before Submitting

1. **Update from upstream**:
   ```bash
   git fetch upstream
   git rebase upstream/master
   ```

2. **Run tests**:
   ```bash
   pytest
   ```

3. **Check code style**:
   ```bash
   flake8 roomba/ tests/  # If using flake8
   ```

4. **Update documentation**:
   - Update README if adding features
   - Add docstrings for new functions/classes
   - Update relevant docs in `docs/`

### Creating a Pull Request

1. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create PR on GitHub**:
   - Use a clear, descriptive title
   - Fill out the PR template
   - Reference related issues
   - Add screenshots/videos if applicable

3. **PR title format**:
   ```
   [Type] Brief description
   ```
   Example: `[Feature] Add wall-following algorithm`

### PR Review Process

1. **Automated checks**: CI tests must pass
2. **Code review**: Maintainer will review your code
3. **Address feedback**: Make requested changes
4. **Approval**: Once approved, PR will be merged

### PR Checklist

- [ ] Code follows project style guidelines
- [ ] Tests added/updated for changes
- [ ] All tests pass locally
- [ ] Documentation updated
- [ ] Commit messages follow guidelines
- [ ] No merge conflicts with master
- [ ] PR description clearly explains changes

## Reporting Issues

### Bug Reports

Use the bug report template and include:

- **Description**: Clear description of the bug
- **Steps to reproduce**: Exact steps to trigger the bug
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Environment**:
  - OS and version
  - Python version
  - Roomba model
  - Serial adapter info
- **Logs**: Relevant error messages or logs
- **Screenshots**: If applicable

### Feature Requests

Use the feature request template and include:

- **Description**: Clear description of the feature
- **Use case**: Why is this feature needed?
- **Proposed solution**: How should it work?
- **Alternatives**: Other solutions you've considered
- **Additional context**: Any other relevant information

### Security Issues

**Do not report security vulnerabilities in public issues.**

See [SECURITY.md](SECURITY.md) for how to report security issues privately.

## Community

### Getting Help

- **Documentation**: Check [docs/](docs/) first
- **Issues**: Search existing issues for similar questions
- **Discussions**: Use GitHub Discussions for questions
- **Examples**: See [examples/](examples/) for usage examples

### Communication

- Be respectful and constructive
- Follow the Code of Conduct
- Stay on topic
- Help others when you can

### Recognition

Contributors are recognized in several ways:

- Listed in CHANGELOG.md for releases
- Mentioned in commit messages
- GitHub contributor statistics
- Special recognition for significant contributions

## Development Workflow

### Typical Workflow

1. **Find or create an issue** to work on
2. **Comment on the issue** to claim it
3. **Create a branch** from master:
   ```bash
   git checkout -b feature/issue-123-description
   ```
4. **Make changes** and commit regularly
5. **Write tests** for your changes
6. **Update documentation** as needed
7. **Push to your fork** and create PR
8. **Respond to review feedback**
9. **Celebrate** when merged! 🎉

### Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring
- `test/description` - Test improvements

### Staying Up to Date

Keep your fork synchronized:

```bash
# Fetch upstream changes
git fetch upstream

# Update your master
git checkout master
git merge upstream/master
git push origin master

# Rebase your feature branch
git checkout feature/your-feature
git rebase master
```

## Release Process

(For maintainers)

1. Update CHANGELOG.md
2. Bump version in `__init__.py`
3. Create release commit
4. Tag release: `git tag -a v1.2.3 -m "Release 1.2.3"`
5. Push tags: `git push --tags`
6. Create GitHub release
7. (Optional) Publish to PyPI

## Additional Resources

- [README.md](README.md) - Project overview
- [docs/API.md](docs/API.md) - API documentation
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - Architecture guide
- [docs/TESTING.md](docs/TESTING.md) - Testing guide
- [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) - Troubleshooting
- [iRobot Create 2 OI Spec](https://www.irobot.com/create-2) - Official documentation

## Questions?

If you have questions not covered here:

1. Check the documentation in [docs/](docs/)
2. Search existing [issues](https://github.com/antigenius0910/alexa_roomba/issues)
3. Open a new issue with your question
4. Use GitHub Discussions for general questions

Thank you for contributing to Alexa Roomba! 🤖✨
