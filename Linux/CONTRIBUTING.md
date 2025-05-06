# Contributing to BreachKit for Linux

Thank you for your interest in contributing to BreachKit for Linux! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

By participating in this project, you agree to abide by the BreachKit Code of Conduct. Please read it before contributing.

## How Can I Contribute?

### Reporting Bugs

Before creating a bug report:

1. Check the [issue tracker](https://github.com/yourusername/breachkit-linux/issues) to see if the problem has already been reported
2. If you're unable to find an open issue addressing the problem, create a new one

When creating a bug report, include as much information as possible:

- A clear and descriptive title
- Steps to reproduce the issue
- Expected behavior vs. actual behavior
- Screenshots (if applicable)
- Your Linux distribution and version
- Your BreachKit version
- Any error messages or logs

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

1. Use a clear and descriptive title
2. Provide a detailed description of the proposed enhancement
3. Explain why this enhancement would be useful
4. Include any relevant examples or mockups

### Pull Requests

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes
4. Run tests to ensure your changes don't break existing functionality
5. Submit a pull request

## Development Environment Setup

To set up a development environment for BreachKit:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/breachkit-linux.git
   cd breachkit-linux
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

## Coding Guidelines

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use 4 spaces for indentation (not tabs)
- Keep line length to a maximum of 79 characters
- Use meaningful variable and function names
- Add docstrings to all functions, classes, and modules

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests after the first line

### Documentation

Documentation is a crucial part of BreachKit. Please follow these guidelines when updating documentation:

- Update documentation when changing code
- Use clear and consistent language
- Include examples where appropriate

## Testing

Before submitting a pull request, run the test suite to ensure your changes don't break existing functionality:

```bash
pytest
```

## Linux-Specific Considerations

When contributing to BreachKit for Linux, keep in mind:

1. **Distribution Compatibility**: Ensure your code works on various Linux distributions, not just Kali Linux
2. **Permission Handling**: Be mindful of permission requirements, especially for network scanning tools
3. **Path Conventions**: Follow Linux path conventions (e.g., `/usr/local/bin`, `/opt`, etc.)
4. **Dependency Management**: Clearly document any new system dependencies

## Adding New Tools

When adding a new tool to Reconic:

1. Create a new module in the appropriate directory
2. Update the tool mapping in `menu.py`
3. Add any new dependencies to `requirements.txt`
4. Document the tool in the README.md
5. Add usage examples to `EXAMPLES.md`

## Project Structure

Understanding the project structure will help you contribute effectively:

```
reconic-linux/
├── install.sh           # Installation script
├── reconic/             # Main package
│   ├── __init__.py      # Package initialization
│   ├── cli.py           # Command-line interface
│   ├── main.py          # Core functionality
│   ├── menu.py          # Menu-driven interface
│   └── utils/           # Utility functions
├── docs/                # Documentation
├── tests/               # Test suite
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

## Getting Help

If you need help with contributing, you can:

1. Open an issue with your question
2. Contact the maintainers directly
3. Join our community chat (if available)

Thank you for contributing to BreachKit for Linux!
