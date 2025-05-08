# Development Guide

This guide covers how to contribute to the `evrmore-rpc` package.

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment (recommended)
- Evrmore node with RPC enabled

### Clone the Repository

```bash
git clone https://github.com/manticoretechnologies/evrmore-rpc-dev.git
cd evrmore-rpc
```

### Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

### Install Dependencies

```bash
# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

## Code Style

### Python Style Guide

We follow PEP 8 style guide for Python code. Use the following tools to ensure code quality:

```bash
# Run linter
flake8

# Run type checker
mypy

# Run formatter
black .

# Run isort
isort .
```

### Pre-commit Hooks

The following pre-commit hooks are configured:

- `black`: Code formatting
- `isort`: Import sorting
- `flake8`: Linting
- `mypy`: Type checking
- `pytest`: Unit tests

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_client.py

# Run tests with coverage
pytest --cov=evrmore_rpc

# Run tests with verbose output
pytest -v
```

### Writing Tests

- Place test files in the `tests` directory
- Name test files with `test_` prefix
- Use descriptive test names
- Follow the Arrange-Act-Assert pattern
- Use fixtures for common setup

Example test:

```python
import pytest
from evrmore_rpc import EvrmoreClient

def test_get_blockchain_info():
    # Arrange
    client = EvrmoreClient()
    
    # Act
    info = client.getblockchaininfo()
    
    # Assert
    assert info.blocks >= 0
    assert info.headers >= 0
    assert info.bestblockhash is not None
```

## Documentation

### Building Documentation

```bash
# Install documentation dependencies
pip install -e ".[docs]"

# Build documentation
cd docs
make html
```

### Writing Documentation

- Use Markdown for documentation files
- Follow the existing documentation structure
- Include code examples
- Add type hints to all functions
- Document all parameters and return values
- Keep documentation up to date with code changes

Example docstring:

```python
def get_block(height: int) -> Block:
    """Get block information by height.
    
    Args:
        height: Block height to retrieve.
        
    Returns:
        Block object containing block information.
        
    Raises:
        EvrmoreRPCError: If the RPC call fails.
        BlockNotFoundError: If the block is not found.
    """
    pass
```

## Pull Requests

### Creating a Pull Request

1. Create a new branch for your changes
2. Make your changes
3. Run tests and ensure they pass
4. Update documentation if needed
5. Create a pull request

### Pull Request Checklist

- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Code style follows project guidelines
- [ ] All tests pass
- [ ] Pre-commit hooks pass
- [ ] Type hints added/updated
- [ ] Changelog updated

## Release Process

### Versioning

We follow semantic versioning (MAJOR.MINOR.PATCH):

- MAJOR: Breaking changes
- MINOR: New features, backward compatible
- PATCH: Bug fixes, backward compatible

### Creating a Release

1. Update version in `setup.py`
2. Update changelog
3. Create release tag
4. Build and upload to PyPI

```bash
# Update version
sed -i 's/version=".*"/version="1.0.0"/' setup.py

# Create tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# Build and upload
python -m build
twine upload dist/*
```

## Project Structure

```
evrmore-rpc/
├── docs/                  # Documentation
├── evrmore_rpc/          # Source code
│   ├── __init__.py
│   ├── client.py         # Main client
│   ├── zmq.py            # ZMQ client
│   ├── websocket.py      # WebSocket client
│   └── models.py         # Data models
├── tests/                # Test files
├── setup.py             # Package setup
├── pyproject.toml       # Project configuration
├── README.md            # Project readme
└── CHANGELOG.md         # Version history
```

## See Also

- [Getting Started](getting-started.md) for basic usage
- [API Reference](api-reference.md) for detailed API docs
- [Examples](examples.md) for code samples
- [Advanced Usage](advanced.md) for production patterns 