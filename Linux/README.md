# BreachKit for Linux

This directory contains everything you need to install and run BreachKit on Linux systems, with a focus on Kali Linux.

## Directory Structure

```
Linux/
├── install.sh            # Linux installation script
├── auto_install.sh        # Automatic installation script
├── post-clone-setup.sh    # Post-clone setup script
├── requirements.txt       # Linux dependencies
├── README.md             # This file
├── EXAMPLES.md           # Usage examples
├── CONTRIBUTING.md       # Contribution guidelines
├── ETHICAL_USAGE.md      # Ethical usage guidelines
├── CHANGELOG.md          # Version history
└── LICENSE               # MIT license
```

> **Note:** Docker is available as an optional installation method. See the [Docker section](#docker-optional) below for more information.

## Installation

### Automatic Installation

## One-Command Installation for Kali Linux

For the fastest installation on Kali Linux, you can use our one-command installer that will clone the repository and automatically install BreachKit:

```bash
curl -sSL https://github.com/bl1ndes/breachkit/blob/main/install_breachkit.sh | sudo bash
```

Or if you've already cloned the repository:

```bash
sudo ./install_breachkit.sh
```

This will automatically install all dependencies and make BreachKit available system-wide.

## Usage

### Menu-Driven Interface

To start BreachKit with the interactive menu:
   ```bash
breachkit
```

### Direct Scanning

To run BreachKit directly for scanning:
   ```bash
breachkit -t example.com -p 1-1000 -v
```

## Features

BreachKit includes the following features:

- **Information Gathering Tools**: nmap, RED HAWK, ReconSpider, Infoga, ReconDog, etc.
- **Vulnerability Scanning**: Web vulnerabilities, network vulnerabilities, etc.
- **Web Application Analysis**: Directory enumeration, web crawling, etc.
- **Network Tools**: Port scanning, network sniffing, etc.
- **SQL Injection Tools**: SQLMap, NoSQLMap, DSSS, SQLScan, etc.
- **Wordlist Generator**: Cupp, WordlistCreator, Goblin Word Generator, etc.
- **And many more security tools**

## System Requirements

- Kali Linux (latest version recommended)
- Python 3.6 or higher
- Internet connection (for downloading tools)
- Root privileges (for installation)

## Troubleshooting

If you encounter any issues during installation:

1. Make sure you have root privileges
2. Ensure all dependencies are installed
3. Check if Python 3 is properly installed
4. Verify that pip3 is working correctly

For any other issues, please report them on our GitHub repository.

## Docker Installation (Optional)

BreachKit can also be run in a Docker container, which provides an isolated environment with all dependencies pre-installed.

### Using Docker with Linux

1. Make sure Docker is installed on your system:
   ```bash
sudo apt update
sudo apt install docker.io docker-compose
sudo systemctl enable docker --now
sudo usermod -aG docker $USER  # Log out and back in after this
```

2. Navigate to the Docker directory:
   ```bash
cd ../../docker
```

3. Build the Docker image:
   ```bash
docker build -t breachkit -f ../docker/Dockerfile ..
```

4. Run BreachKit in a container:
   ```bash
docker run -it --rm breachkit
```

Alternatively, you can use Docker Compose:
   ```bash
cd ../docker
docker-compose up
```

For more detailed information about using Docker with BreachKit, see the [docker/README.md](../../docker/README.md) file.

## Contributing

Contributions to BreachKit are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
