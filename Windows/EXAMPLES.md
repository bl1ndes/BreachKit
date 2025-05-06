# BreachKit for Windows - Usage Examples

This document provides practical examples of how to use BreachKit on Windows systems.

## Basic Usage

### Command-Line Interface

```cmd
# Basic port scan
breachkit -t 192.168.1.1 -p 1-1000

# Full network scan
breachkit -t 192.168.1.0/24 --full-scan

# Web vulnerability scan
breachkit -t example.com --web-scan -v

# Directory enumeration
breachkit -t example.com --dir-scan --wordlist C:\path\to\wordlist.txt
```

### Menu Interface

```cmd
# Launch the menu interface
breachkit
```

## Information Gathering Examples

### Network Scanning

```powershell
# Comprehensive network scan
breachkit -t 192.168.1.0/24 -p 1-1000 --service-detection --os-detection -v

# Scan specific ports
breachkit -t 192.168.1.1 -p 22,80,443,3306,8080
```

### DNS Information

```powershell
# Get DNS information for a domain
breachkit -t example.com --dns-info

# Enumerate subdomains
breachkit -t example.com --subdomain-enum --wordlist C:\path\to\subdomains.txt
```

### WHOIS Lookup

```powershell
# Get WHOIS information
breachkit -t example.com --whois-info
```

## Web Application Analysis Examples

### Directory Enumeration

```powershell
# Basic directory scan
breachkit -t http://example.com --dir-scan

# With custom wordlist and file extensions
breachkit -t http://example.com --dir-scan --wordlist C:\path\to\wordlist.txt --extensions php,html,js

# With increased threads for faster scanning
breachkit -t http://example.com --dir-scan --threads 50
```

### Web Vulnerability Scanning

```powershell
# Basic web vulnerability scan
breachkit -t http://example.com --web-scan

# Comprehensive web scan
breachkit -t http://example.com --web-scan --xss-scan --sqli-scan --lfi-scan
```

## SQL Injection Examples

```powershell
# Basic SQL injection scan
breachkit -t http://example.com/page.php?id=1 --sqli-scan

# Using the menu interface
# 1. Launch breachkit
# 2. Select "SQL Injection Tools"
# 3. Choose the appropriate tool (e.g., SQLMap)
# 4. Follow the on-screen instructions
```

## Tool Management Examples

```powershell
# Check tool installation status
breachkit --check-tools

# Update all tools
breachkit --update-tools

# Install a specific tool
breachkit --install-tool sqlmap
```

## Advanced Usage

### Output Options

```powershell
# Save results to a file
breachkit -t 192.168.1.1 -p 1-1000 -o results.txt

# Output in JSON format
breachkit -t 192.168.1.1 -p 1-1000 --json -o results.json

# Output in XML format
breachkit -t 192.168.1.1 -p 1-1000 --xml -o results.xml
```

### Proxy and Anonymity

```powershell
# Use a proxy
breachkit -t example.com --web-scan --proxy http://127.0.0.1:8080

# Use Tor (if installed)
breachkit -t example.com --web-scan --tor
```

### Automation and Scripting

```powershell
# PowerShell script to scan multiple targets
$targets = @("192.168.1.1", "192.168.1.2", "example.com")

foreach ($target in $targets) {
    Write-Host "Scanning $target..."
    breachkit -t $target -p 1-1000 --web-scan -o "$target-results.txt"
    Write-Host "Scan completed for $target"
    Write-Host "------------------------"
}
```

### Scheduled Scanning

```powershell
# Create a scheduled task using Task Scheduler
# 1. Open Task Scheduler
# 2. Create a new task
# 3. Set the trigger (e.g., daily at 2 AM)
# 4. Add a new action with the following settings:
#    - Program/script: breachkit
#    - Arguments: -t example.com --full-scan -o C:\path\to\logs\scan.log
```

## Integration with Other Tools

### Piping Results

```powershell
# Pipe results to find
breachkit -t 192.168.1.0/24 -p 80 | findstr "Apache"

# Save and process results
breachkit -t 192.168.1.0/24 -p 1-1000 -o scan.txt && type scan.txt | findstr "open" > open-ports.txt
```

### Using with Other Security Tools

```powershell
# Scan with BreachKit and pass vulnerable URLs to another tool
breachkit -t example.com --web-scan --output-format=urls -o vulnerable-urls.txt && another-tool --url-file vulnerable-urls.txt
```

## Performance Optimization

```powershell
# Faster scanning with reduced accuracy
breachkit -t 192.168.1.0/24 -p 1-1000 --fast

# More thorough but slower scanning
breachkit -t 192.168.1.0/24 -p 1-1000 --thorough
```

## Administrator Privileges

Some scanning operations require administrator privileges:

```powershell
# Run Command Prompt as Administrator, then:
breachkit -t 192.168.1.0/24 --full-scan
```

## Docker Examples

```powershell
# Run BreachKit in Docker
docker run -it --rm breachkit -t example.com -p 1-1000

# Mount volumes for persistent data
docker run -it --rm -v %cd%\results:/opt/breachkit/results breachkit -t example.com -o /opt/breachkit/results/scan.txt
```

These examples demonstrate the versatility and power of BreachKit on Windows systems. For more detailed information, refer to the full documentation.
