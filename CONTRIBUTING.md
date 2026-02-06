# Contributing to gmd_api

Thank you for your interest in contributing to gmd_api! This document provides guidelines and instructions for contributing to the project.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- A virtual environment tool (venv, conda, micromamba, etc.)

### Setting Up Your Development Environment

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/gmd_api.git
   cd gmd_api
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install the package in development mode:
   ```bash
   pip install -e .
   ```

5. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

## Development Workflow

### Making Changes

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes, following the code style guidelines below

3. Add or update tests for your changes

4. Run the test suite to ensure everything passes:
   ```bash
   pytest
   ```

5. Run linters to check code quality:
   ```bash
   black .
   isort .
   flake8 .
   mypy gmd_api
   ```

6. Commit your changes with a clear commit message:
   ```bash
   git add .
   git commit -m "Add feature: description of your changes"
   ```

7. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

8. Open a Pull Request on GitHub

## Code Style Guidelines

### Python Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use [Black](https://github.com/psf/black) for code formatting
- Use [isort](https://pycqa.github.io/isort/) for import sorting
- Maximum line length: 100 characters
- Use type hints for function parameters and return values

### Documentation

- Add docstrings to all public classes, methods, and functions
- Use Google-style docstrings format
- Include examples in docstrings when appropriate
- Update README.md if adding new features

### Example of Good Documentation

```python
def move_to(self, x: float, y: float) -> Self:
    """Move the object to the specified position.
    
    Args:
        x: The x-coordinate position in the level.
        y: The y-coordinate position in the level.
    
    Returns:
        Self: Returns self for method chaining.
        
    Example:
        >>> obj = LevelObject(211)
        >>> obj.move_to(100, 200)
    """
    return self.set(POS_X, x).set(POS_Y, y)
```

## Testing

### Writing Tests

- Place tests in the `tests/` directory
- Name test files as `test_*.py`
- Use descriptive test function names that explain what is being tested
- Test both success and error cases
- Use pytest fixtures for common setup

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_level.py

# Run with coverage report
pytest --cov=gmd_api --cov-report=html
```

## Project Structure

```
gmd_api/
├── gmd_api/           # Main package directory
│   ├── __init__.py    # Package initialization and exports
│   ├── level.py       # Level class for GMD files
│   ├── level_object.py # LevelObject class for in-game objects
│   ├── level_string.py # InnerLevelString for level data
│   ├── color.py       # ColorChannel for color definitions
│   └── keys/          # Constants for GMD format keys
├── tests/             # Test directory
├── examples/          # Example scripts
├── README.md          # Project documentation
├── CONTRIBUTING.md    # This file
├── setup.py           # Package setup configuration
├── pyproject.toml     # Modern Python project configuration
└── requirements-dev.txt # Development dependencies
```

## Understanding the GMD Format

GMD (Geometry Dash Level) files are XML-based files that contain level data:

- **Level properties**: Name, description, song ID, etc.
- **Inner level string**: Compressed and encoded level data containing:
  - Objects: Game objects with properties (position, rotation, color, etc.)
  - Color channels: Color definitions for the level
  - Settings: Background, ground, platformer mode, etc.

### Key Concepts

- **Properties**: Key-value pairs stored as dictionaries
- **Method chaining**: Most methods return `self` for fluent API usage
- **Encoding**: Inner level string is gzip-compressed and base64-encoded
- **Keys**: Numeric or string keys defined in `gmd_api/keys/` modules

## Common Contribution Areas

### Adding New Object Properties

If you want to add support for a new object property:

1. Add the constant to `gmd_api/keys/objects.py`
2. Add a helper method to `LevelObject` class if appropriate
3. Add documentation and examples
4. Add tests

### Adding New Level Properties

If you want to add support for a new level property:

1. Add the constant to `gmd_api/keys/level.py`
2. Add a helper method to `Level` class if appropriate
3. Add documentation and examples
4. Add tests

## Reporting Issues

When reporting issues, please include:

- Python version
- gmd_api version
- Clear description of the issue
- Minimal code example that reproduces the issue
- Expected vs actual behavior
- Error messages or stack traces

## Questions?

If you have questions about contributing, feel free to:

- Open an issue with the "question" label
- Check existing issues and discussions
- Review the README.md for usage examples

## License

By contributing to gmd_api, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing! 🚀
