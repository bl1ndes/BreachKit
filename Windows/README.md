# BreachKit for Windows

This directory contains everything you need to install and run BreachKit on Windows systems.

## Directory Structure

```
Windows/
├── install.bat           # Windows installation script
├── auto_install.bat      # Automatic installation script
├── post-clone-setup.bat  # Post-clone setup script
├── windows_adapter.py    # Windows compatibility layer
├── requirements.txt      # Windows dependencies
├── README.md             # This file
├── EXAMPLES.md           # Usage examples
├── CONTRIBUTING.md       # Contribution guidelines
├── ETHICAL_USAGE.md      # Ethical usage guidelines
├── CHANGELOG.md          # Version history
└── LICENSE               # MIT license
```

> **Note:** Docker is available as an optional installation method. See the [Docker section](#docker-optional) below for more information.

## Installation

1. Right-click on `install.bat` and select "Run as administrator"
2. Follow the on-screen instructions to complete the installation
3. After installation, you can run BreachKit from anywhere using:
   - The Start Menu
   - Command Prompt by typing `breachkit`
   - The installation directory by running `breachkit.bat`

## Features

BreachKit for Windows includes:

- **Information Gathering Tools**: Network scanning, DNS information, WHOIS lookup, etc.
- **Vulnerability Scanning**: Web vulnerabilities, network vulnerabilities, etc.
- **Web Application Analysis**: Directory enumeration, web crawling, etc.
- **Network Tools**: Port scanning, network sniffing, etc.
- **SQL Injection Tools**: SQLMap, NoSQLMap, DSSS, SQLScan, etc.
- **Wordlist Generator**: Cupp, WordlistCreator, Goblin Word Generator, etc.
- **Tool Management**: Install, update, and manage security tools

## System Requirements

- Windows 10/11 (64-bit recommended)
- Python 3.6 or higher
- Administrator privileges (for installation)
- Internet connection (for downloading tools)
- Nmap (will be installed automatically if Chocolatey is available)

## Troubleshooting

If you encounter any issues during installation:

1. Make sure you have administrator privileges
2. Ensure Python is properly installed and in your PATH
3. Check if pip is working correctly
4. Install Nmap manually if the automatic installation fails

For any other issues, please report them on our GitHub repository.

## Windows-Specific Notes

Some tools may have limited functionality on Windows compared to their Linux counterparts. We've made the following adaptations:

1. Tools that require specific Linux binaries have been replaced with Windows-compatible alternatives
2. Some network scanning features may require additional permissions on Windows
3. The tool uses Windows-specific paths and environment variables

## Running Tools

When running tools that require administrator privileges, you may need to:

1. Right-click on Command Prompt and select "Run as administrator"
2. Then run BreachKit from the elevated command prompt

This is particularly important for network scanning and vulnerability assessment tools.

## Docker (Optional)

BreachKit can also be run using Docker on Windows, which provides an isolated environment with all dependencies pre-installed. This can be especially useful on Windows to avoid compatibility issues with certain tools.

### Using Docker with Windows

1. Install Docker Desktop for Windows:
   - Download from [Docker Hub](https://hub.docker.com/editions/community/docker-ce-desktop-windows/)
   - Follow the installation instructions
   - Make sure to enable WSL 2 if prompted

2. Open PowerShell or Command Prompt and navigate to the Docker directory:
   ```powershell
   cd ..\..\docker
   ```

3. Build the Docker image:
   ```cmd
   docker build -t breachkit -f ..\docker\Dockerfile ..
   ```

4. Run BreachKit in a container:
   ```powershell
   # For the menu interface
   breachkit
   
   # For direct scanning
   breachkit -t example.com -p 1-1000 -v
   ```

5. For network scanning on Windows, you may need to use host networking (only works with WSL 2 backend):
   ```powershell
   docker run -it --rm --network host breachkit
   ```

6. Alternatively, use Docker Compose:
   ```powershell
   docker-compose up
   ```

7. To mount volumes for persistent data:
   ```powershell
   docker run -it --rm -v ${PWD}\results:/opt/breachkit/results breachkit
   ```

### Windows-Specific Docker Notes

- Docker on Windows uses WSL 2 by default, which provides better Linux compatibility
- Some network scanning tools may have limited functionality when run in Docker on Windows
- For best results with network scanning tools, consider using the native Windows installation

For more detailed information about using Docker with BreachKit, see the [docker/README.md](../../docker/README.md) file.
