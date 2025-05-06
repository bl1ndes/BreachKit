# BreachKit for Linux - Usage Examples

This document provides practical examples of how to use BreachKit on Linux systems.

## Basic Usage

### Starting BreachKit Interface

```bash
breachkit -t 192.168.1.1 -p 1-1000
```

### Menu Interface

```bash
# Launch the menu-driven interface
breachkit

# Launch with command-line arguments
breachkit -t example.com -p 80,443 -s basic
```

## Scanning Examples

### Basic Port Scan

```bash
breachkit -t 192.168.1.1 -p 1-1000
```

### Full Network Scan

```bash
breachkit -t 192.168.1.0/24 --full-scan
```

### Vulnerability Scan

```bash
breachkit -t example.com -s vuln
```

### Network Range Scan

```bash
breachkit -t 192.168.1.0/24 -p 22,80,443
```

## Information Gathering Examples

### DNS Information

```bash
# Get DNS information for a domain
breachkit -t example.com --dns-info

# Enumerate subdomains
breachkit -t example.com --subdomain-enum --wordlist /path/to/subdomains.txt
```

### WHOIS Lookup

```bash
breachkit -t example.com --whois-info
```

## Web Application Analysis Examples

### Directory Enumeration

```bash
# Basic directory scan
breachkit -t http://example.com --dir-scan

# With custom wordlist and file extensions
breachkit -t http://example.com --dir-scan --wordlist /path/to/wordlist.txt --extensions php,html,js

# With increased threads for faster scanning
breachkit -t http://example.com --dir-scan --threads 50
```

### Web Application Scan

```bash
breachkit -t https://example.com -s webapp
```

### Comprehensive Scan

```bash
breachkit -t example.com -p- -s comprehensive
```

## SQL Injection Examples

```bash
# Basic SQL injection scan
breachkit -t http://example.com/page.php?id=1 --sqli-scan

# Using the menu interface
# 1. Launch breachkit
# 2. Select "SQL Injection Tools"
# 3. Choose the appropriate tool (e.g., SQLMap)
# 4. Follow the on-screen instructions
```

## Tool Management Examples

```bash
# Check tool installation status
breachkit --check-tools

# Update all tools
breachkit --update-tools

# Install a specific tool
breachkit --install-tool sqlmap
```

## Advanced Usage

### Output Options

```bash
# Save results to a file
breachkit -t 192.168.1.1 -p 1-1000 -o results.txt

# Output in JSON format
breachkit -t 192.168.1.1 -p 1-1000 --json -o results.json

# Output in XML format
breachkit -t 192.168.1.1 -p 1-1000 --xml -o results.xml
```

### Proxy and Anonymity

```bash
# Use a proxy
breachkit -t example.com --web-scan --proxy http://127.0.0.1:8080

# Use Tor (if installed)
breachkit -t example.com --web-scan --tor
```

### Custom Wordlist

```bash
breachkit -t example.com -s dirb --wordlist /path/to/wordlist.txt
```

### Using Proxies

```bash
breachkit -t example.com --proxy socks5://127.0.0.1:9050
```

### JSON Output

```bash
breachkit -t example.com -o report.json --json
```

### Automation and Scripting

```bash
# Bash script to scan multiple targets
#!/bin/bash
targets=("192.168.1.1" "192.168.1.2" "example.com")

for target in "${targets[@]}"; do
    echo "Scanning $target..."
    breachkit -t $target -p 1-1000 --web-scan -o "$target-results.txt"
    echo "Scan completed for $target"
    echo "------------------------"
done
```

### Scheduled Scanning

```bash
# Add to crontab to run daily at 2 AM
0 2 * * * /usr/local/bin/breachkit -t example.com --full-scan -o /var/log/breachkit/$(date +\%Y\%m\%d).log
```

## Integration with Other Tools

### Piping Results

```bash
# Pipe results to grep
breachkit -t 192.168.1.0/24 -p 80 | grep "Apache"

# Save and process results
breachkit -t 192.168.1.0/24 -p 1-1000 -o scan.txt && cat scan.txt | grep "open" > open-ports.txt
```

### Using with Other Security Tools

```bash
# Scan with BreachKit and pass vulnerable URLs to another tool
breachkit -t example.com --web-scan --output-format=urls -o vulnerable-urls.txt && another-tool --url-file vulnerable-urls.txt
```

## Performance Optimization

```bash
# Faster scanning with reduced accuracy
breachkit -t 192.168.1.0/24 -p 1-1000 --fast

# More thorough but slower scanning
breachkit -t 192.168.1.0/24 -p 1-1000 --thorough
```

## Docker Examples

### Basic Docker Usage

```bash
docker run -it --rm breachkit -t example.com
```

### Docker with Volume Mounting

```bash
docker run -it --rm -v $(pwd)/reports:/reports breachkit -t example.com -o /reports/output.txt
```

These examples demonstrate the versatility and power of BreachKit on Linux systems. For more detailed information, refer to the full documentation.
