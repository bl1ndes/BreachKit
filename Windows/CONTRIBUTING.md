# Contributing to BreachKit for Windows

Thank you for your interest in contributing to BreachKit for Windows! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

By participating in this project, you agree to abide by the BreachKit Code of Conduct. Please read it before contributing.

## How Can I Contribute?

### Reporting Bugs

Before creating a bug report:

1. Check the [issue tracker](https://github.com/yourusername/breachkit-Windows/issues) to see if the problem has already been reported
2. If you're unable to find an open issue addressing the problem, create a new one

When creating a bug report, include as much information as possible:

- A clear and descriptive title
- Steps to reproduce the issue
- Expected behavior vs. actual behavior
- Screenshots (if applicable)
- Your Windows version
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

## Development Setup

### Prerequisites

- Windows 10/11
- Python 3.6 or higher
- Git
- Nmap
- Other dependencies listed in requirements.txt

### Setting Up Development Environment

1. Clone your fork of the repository:
   ```cmd
   git clone https://github.com/yourusername/breachkit-Windows.git
   cd breachkit-Windows
   ```

2. Create a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Install development dependencies:
   ```powershell
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

- Update documentation when changing code
- Use clear and consistent language
- Include examples where appropriate

## Testing

Before submitting a pull request, run the test suite to ensure your changes don't break existing functionality:

```powershell
pytest
```

## Windows-Specific Considerations

When contributing to BreachKit for Windows, keep in mind:

1. **Path Handling**: Use `os.path` or `pathlib` to handle paths in a Windows-compatible way
2. **Administrator Privileges**: Be clear about which features require administrator privileges
3. **Command Prompt vs PowerShell**: Provide examples for both when relevant
4. **Windows Defender**: Consider potential conflicts with Windows security features
5. **File System Restrictions**: Be mindful of Windows file system restrictions and permissions

## Adding New Tools

When adding a new tool to Reconic:

1. Create a new module in the appropriate directory
2. Update the tool mapping in `menu.py`
3. Add any new dependencies to `requirements.txt`
4. Document the tool in the README.md
5. Add usage examples to `EXAMPLES.md`
6. Ensure the tool works properly on Windows

## Project Structure

Understanding the project structure will help you contribute effectively:

```
reconic-windows/
├── install.bat          # Installation script
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

## Windows Compatibility

When adding new features or tools, consider Windows compatibility:

1. **Linux-Only Tools**: If a tool only works on Linux, consider:
   - Finding a Windows-compatible alternative
   - Creating a Windows-specific implementation
   - Clearly documenting the limitation

2. **Command Execution**: Use `subprocess` with appropriate parameters for Windows

3. **File Paths**: Use forward slashes or raw strings with backslashes

4. **Terminal Colors**: Use the `colorama` package for terminal colors on Windows

## Getting Help

If you need help with contributing, you can:

1. Open an issue with your question
2. Contact the maintainers directly
3. Join our community chat (if available)

Thank you for contributing to BreachKit for Windows!
