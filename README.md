# BreachKit - All-In-One Security & Penetration Testing Toolkit

## Overview

BreachKit is a comprehensive security and penetration testing toolkit that combines the capabilities of numerous security tools into a single, unified interface for network reconnaissance, vulnerability assessment, exploitation, and more.

## Project Structure

This repository is organized as follows:

```
breachkit/
├── __init__.py         # Package initialization
├── cli.py              # Command-line interface
├── main.py             # Core functionality
├── menu.py             # Menu-driven interface
├── common/             # Common utilities and shared code
├── Linux/              # Linux-specific implementation
│   ├── install.sh      # Linux installation script
│   ├── auto_install.sh # Automatic installation script
│   ├── post-clone-setup.sh # Post-clone setup script
│   ├── requirements.txt # Linux dependencies
│   └── README.md       # Linux-specific documentation
└── Windows/            # Windows-specific implementation
    ├── install.bat     # Windows installation script
    ├── auto_install.bat # Automatic installation script
    ├── post-clone-setup.bat # Post-clone setup script
    ├── windows_adapter.py # Windows compatibility layer
    ├── requirements.txt # Windows dependencies
    └── README.md       # Windows-specific documentation
```

## Platform-Specific Installation

BreachKit is available for both Linux and Windows platforms:

- **[Linux/](./Linux/)** - For Kali Linux and other Linux distributions
- **[Windows/](./Windows/)** - For Windows 10/11 systems

Please navigate to the appropriate directory for your operating system and follow the installation instructions in the README.md file.

## Features

BreachKit includes a wide range of security tools and features:

- **Information Gathering**
  - Network scanning (Nmap)
  - DNS information gathering
  - WHOIS lookup
  - Email harvesting
  - Subdomain enumeration
  - And more...

- **Vulnerability Scanning**
  - Web vulnerability scanning
  - Network vulnerability assessment
  - CMS vulnerability detection
  - SSL/TLS vulnerability scanning
  - SQL injection detection
  - XSS scanning

- **Web Application Analysis**
  - Directory enumeration
  - Web crawling
  - Web fuzzing
  - CMS detection
  - API scanning

- **Tool Management**
  - Automatic tool installation
  - Tool updates
  - Dependency management
  - Tool status monitoring
  - Search functionality

## System Requirements

### Linux
- Kali Linux (recommended) or other Linux distribution
- Python 3.6 or higher
- Root privileges (for installation)
- Internet connection (for downloading tools)

### Windows
- Windows 10/11 (64-bit recommended)
- Python 3.6 or higher
- Administrator privileges (for installation)
- Internet connection (for downloading tools)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

BreachKit is designed for legal security testing and educational purposes only. Users are responsible for complying with applicable laws and regulations. The developers assume no liability for misuse or damage caused by this tool.
