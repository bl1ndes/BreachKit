#!/usr/bin/env python3

import argparse
import socket
import sys
import os
import nmap
import requests
import json
import whois
import dns.resolver
import concurrent.futures
import ipaddress
import subprocess
import tempfile
from datetime import datetime
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# Banner
BANNER = '''
=======================================================
                       BREACH KIT                      
=======================================================
[*] Advanced Network Vulnerability Scanner
[*] Version: 1.0.0
'''

class BreachKit:
    """BreachKit - Advanced Vulnerability Scanner
    A comprehensive tool for network reconnaissance and vulnerability assessment
    """
    def __init__(self):
        self.banner = BANNER
        self.parser = self._create_parser()
        self.args = None
        self.target = None
        self.nm = nmap.PortScanner()
        self.results = {}
        self.output_file = None

    def _create_parser(self):
        parser = argparse.ArgumentParser(
            description='NexusProbe - Advanced Network Vulnerability Scanner',
            epilog='Example: nexusprobe -t 192.168.1.1 -p 1-1000 -v -o results.json'
        )
        parser.add_argument('-t', '--target', required=True, help='Target IP address, URL, or CIDR range')
        parser.add_argument('-p', '--ports', default='1-1000', help='Port range to scan (default: 1-1000)')
        parser.add_argument('-s', '--speed', default='3', choices=['1', '2', '3', '4', '5'], 
                            help='Scan speed (1-5, where 1 is slowest and 5 is fastest)')
        parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
        parser.add_argument('-o', '--output', help='Output file for scan results (JSON format)')
        parser.add_argument('--web-scan', action='store_true', help='Perform web vulnerability scan')
        parser.add_argument('--full-scan', action='store_true', help='Perform a comprehensive scan (includes all scan types)')
        parser.add_argument('--no-ping', action='store_true', help='Skip ping scan (assume all hosts are up)')
        parser.add_argument('--threads', type=int, default=5, help='Number of threads for parallel scanning')
        parser.add_argument('--timeout', type=int, default=10, help='Timeout for requests in seconds')
        parser.add_argument('--dir-scan', action='store_true', help='Perform directory scanning with gobuster')
        parser.add_argument('--wordlist', help='Path to wordlist for directory scanning (default: built-in common.txt)')
        return parser

    def print_banner(self):
        print(self.banner)

    def parse_arguments(self):
        self.args = self.parser.parse_args()
        self.target = self.args.target
        if self.args.output:
            self.output_file = self.args.output
        return self.args

    def normalize_target(self):
        """Normalize target to IP address(es)"""
        # Check if target is a URL
        if self.target.startswith(('http://', 'https://', 'www.')):
            parsed_url = urlparse(self.target)
            if not parsed_url.netloc:
                parsed_url = urlparse(f'http://{self.target}')
            hostname = parsed_url.netloc
            try:
                ip = socket.gethostbyname(hostname)
                self.results['original_target'] = self.target
                self.results['hostname'] = hostname
                self.target = ip
                print(f"[+] Resolved {hostname} to {ip}")
            except socket.gaierror:
                print(f"[-] Could not resolve hostname {hostname}")
                sys.exit(1)
        
        # Check if target is a CIDR range
        try:
            if '/' in self.target:
                network = ipaddress.ip_network(self.target, strict=False)
                if network.num_addresses > 256 and not self.args.no_ping:
                    print(f"[!] Warning: Scanning large network ({network.num_addresses} hosts). This may take a long time.")
                    response = input("Do you want to continue? (y/n): ")
                    if response.lower() != 'y':
                        sys.exit(0)
                return True
            else:
                # Validate if it's a valid IP address
                ipaddress.ip_address(self.target)
                return True
        except ValueError:
            # Not a valid IP or CIDR, but might be a hostname
            try:
                ip = socket.gethostbyname(self.target)
                self.results['original_target'] = self.target
                self.results['hostname'] = self.target
                self.target = ip
                print(f"[+] Resolved {self.target} to {ip}")
                return True
            except socket.gaierror:
                print(f"[-] Invalid target: {self.target}. Please provide a valid IP, URL, or CIDR range.")
                return False

    def get_whois_info(self):
        """Get WHOIS information for the target"""
        print(f"\n[*] Getting WHOIS information...")
        try:
            # If target is an IP address
            w = whois.whois(self.results.get('hostname', self.target))
            self.results['whois'] = {
                'domain_name': w.domain_name,
                'registrar': w.registrar,
                'creation_date': str(w.creation_date),
                'expiration_date': str(w.expiration_date),
                'name_servers': w.name_servers,
                'status': w.status,
                'emails': w.emails,
                'dnssec': w.dnssec,
                'name': w.name,
                'org': w.org,
                'address': w.address,
                'city': w.city,
                'state': w.state,
                'zipcode': w.zipcode,
                'country': w.country
            }
            
            if self.args.verbose:
                print(f"[+] Domain: {w.domain_name}")
                print(f"[+] Registrar: {w.registrar}")
                print(f"[+] Creation Date: {w.creation_date}")
                print(f"[+] Expiration Date: {w.expiration_date}")
                print(f"[+] Organization: {w.org}")
                print(f"[+] Country: {w.country}")
        except Exception as e:
            print(f"[!] WHOIS lookup failed: {str(e)}")
            self.results['whois'] = {'error': str(e)}

    def get_dns_info(self):
        """Get DNS information for the target"""
        if 'hostname' not in self.results:
            return
            
        print(f"\n[*] Getting DNS information...")
        hostname = self.results['hostname']
        dns_records = {}
        
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME']
        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(hostname, record_type)
                records = [str(answer) for answer in answers]
                dns_records[record_type] = records
                if self.args.verbose:
                    print(f"[+] {record_type} Records: {', '.join(records)}")
            except Exception:
                dns_records[record_type] = []
        
        self.results['dns_records'] = dns_records

    def scan_ports(self, ip, port_range):
        """Scan ports on the target IP"""
        try:
            print(f"\n[*] Scanning ports {port_range} on {ip}...")
            arguments = f"-p {port_range} -sV -sS --script=banner,version,vuln -T{self.args.speed}"
            if self.args.no_ping:
                arguments += " -Pn"
                
            self.nm.scan(ip, arguments=arguments)
            
            if ip not in self.nm.all_hosts():
                print(f"[-] Host {ip} seems to be down or not responding to scans")
                return {}
                
            host_results = {
                'status': self.nm[ip].state(),
                'ports': {}
            }
            
            # Check if 'tcp' key exists in the scan results
            if 'tcp' in self.nm[ip]:
                for port, port_info in self.nm[ip]['tcp'].items():
                    host_results['ports'][port] = {
                        'state': port_info['state'],
                        'service': port_info['name'],
                        'product': port_info.get('product', ''),
                        'version': port_info.get('version', ''),
                        'extrainfo': port_info.get('extrainfo', ''),
                        'reason': port_info.get('reason', ''),
                        'cpe': port_info.get('cpe', '')
                    }
                    
                    # Check for vulnerabilities in script output
                    if 'script' in port_info:
                        host_results['ports'][port]['vulnerabilities'] = port_info['script']
                    
                    # Print port information
                    if port_info['state'] == 'open':
                        service_info = f"{port_info['name']}"
                        if port_info.get('product'):
                            service_info += f" - {port_info['product']}"
                        if port_info.get('version'):
                            service_info += f" {port_info['version']}"
                        print(f"[+] Port {port}/tcp open: {service_info}")
                        
                        # Print vulnerability information if available
                        if 'script' in port_info:
                            for script_name, output in port_info['script'].items():
                                if 'VULNERABLE' in output:
                                    print(f"[!] Vulnerability found: {script_name}")
                                    print(f"{output}")
            
            return host_results
            
        except Exception as e:
            print(f"[-] Error scanning ports: {str(e)}")
            return {'error': str(e)}

    def run_gobuster(self, url):
        """Run gobuster directory scanning"""
        print(f"\n[*] Starting gobuster directory scan on {url}...")
        
        # Create a default wordlist if none is provided
        wordlist_path = self.args.wordlist
        if not wordlist_path:
            # Create a temporary file with common directories
            common_dirs = [
                "admin", "login", "wp-admin", "administrator", "phpmyadmin", "dashboard",
                "wp-content", "upload", "uploads", "files", "images", "img", "css", "js",
                "backup", "backups", "bak", "old", "new", "test", "dev", "development",
                "staging", "stage", "prod", "production", "api", "v1", "v2", "beta",
                "config", "configuration", "setup", "install", "wp-includes", "include",
                "includes", "cgi-bin", "bin", "app", "applications", "tools", "temp",
                "tmp", "private", "public", "src", "source", "log", "logs", "admin.php",
                "index.php", "login.php", "wp-login.php", "robots.txt", "sitemap.xml",
                "server-status", ".git", ".svn", ".htaccess", ".htpasswd", "console",
                "webmail", "mail", "email", "cpanel", "ftp", "ssh", "webdav", "backup-db",
                "database", "db", "sql", "mysql", "oracle", "shop", "store", "cart",
                "checkout", "payment", "pay", "billing", "bill", "account", "profile",
                "settings", "setting", "config.php", "configuration.php", "wp-config.php",
                "forum", "forums", "blog", "blogs", "portal", "site", "sites", "host",
                "hosting", "cloud", "about", "contact", "feedback", "support", "help",
                "faq", "career", "careers", "job", "jobs", "newsletter", "press", "media",
                "download", "downloads", "content", "assets", "static", "data", "docs",
                "documentation", "wiki", "status", "stats", "statistics", "analytics",
                "report", "reports", "login.aspx", "admin.aspx", "index.aspx", "default.aspx",
                "login.jsp", "admin.jsp", "index.jsp", "home", "index", "default", "search"
            ]
            
            fd, wordlist_path = tempfile.mkstemp(suffix=".txt")
            with os.fdopen(fd, 'w') as f:
                for directory in common_dirs:
                    f.write(f"{directory}\n")
            print(f"[+] Created temporary wordlist with {len(common_dirs)} common entries")
        
        # Run gobuster using subprocess
        gobuster_results = {}
        try:
            # Prepare the command
            cmd = [
                "gobuster", "dir",
                "-u", url,
                "-w", wordlist_path,
                "-q",  # Quiet mode
                "-t", str(self.args.threads),  # Threads
                "-o", f"gobuster_{urlparse(url).netloc.replace(':', '_')}.txt"  # Output file
            ]
            
            # Add status codes to look for
            cmd.extend(["-s", "200,204,301,302,307,401,403"])
            
            # Run the command and capture output
            print(f"[*] Running: {' '.join(cmd)}")
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            
            # Process the output
            if process.returncode == 0:
                # Parse the results
                found_dirs = []
                for line in stdout.splitlines():
                    if line.strip():
                        found_dirs.append(line.strip())
                        print(f"[+] {line.strip()}")
                
                gobuster_results = {
                    "status": "success",
                    "command": " ".join(cmd),
                    "found_directories": found_dirs,
                    "output_file": f"gobuster_{urlparse(url).netloc.replace(':', '_')}.txt"
                }
                
                print(f"[+] Gobuster scan completed. Found {len(found_dirs)} directories.")
                print(f"[+] Results saved to {gobuster_results['output_file']}")
            else:
                print(f"[-] Gobuster scan failed with error: {stderr}")
                gobuster_results = {
                    "status": "failed",
                    "command": " ".join(cmd),
                    "error": stderr
                }
        except Exception as e:
            print(f"[-] Error running gobuster: {str(e)}")
            gobuster_results = {
                "status": "error",
                "error": str(e)
            }
            
            # If gobuster is not installed, provide installation instructions
            if "No such file or directory" in str(e) or "not recognized" in str(e):
                print(f"[!] Gobuster does not appear to be installed.")
                print(f"[!] Installation instructions:")
                print(f"[!] - Go to https://github.com/OJ/gobuster")
                print(f"[!] - Follow the installation instructions for your platform")
                print(f"[!] - Alternatively, install with Go: go install github.com/OJ/gobuster/v3@latest")
        
        # Clean up temporary wordlist if we created one
        if not self.args.wordlist and os.path.exists(wordlist_path):
            try:
                os.remove(wordlist_path)
            except Exception:
                pass
                
        return gobuster_results

    def scan_web_vulnerabilities(self, ip, ports):
        """Scan for web vulnerabilities on open HTTP/HTTPS ports"""
        web_results = {}
        web_ports = []
        
        # Find potential web ports
        if 'ports' in ports:
            for port, port_info in ports['ports'].items():
                if port_info['state'] == 'open' and port_info['service'] in ['http', 'https']:
                    web_ports.append((port, port_info['service']))
                elif port_info['state'] == 'open' and port in [80, 443, 8080, 8443]:
                    service = 'https' if port in [443, 8443] else 'http'
                    web_ports.append((port, service))
        
        if not web_ports:
            print(f"[!] No web services detected on {ip}")
            return {}
            
        print(f"\n[*] Scanning web vulnerabilities on {ip}...")
        
        for port, service in web_ports:
            url = f"{service}://{ip}:{port}"
            print(f"[*] Checking {url}")
            web_results[url] = {}
            
            try:
                # Make request with a custom user agent
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                }
                response = requests.get(url, headers=headers, timeout=self.args.timeout, verify=False)
                web_results[url]['status_code'] = response.status_code
                web_results[url]['headers'] = dict(response.headers)
                
                # Parse response for potential vulnerabilities
                soup = BeautifulSoup(response.text, 'html.parser')
                web_results[url]['title'] = soup.title.string if soup.title else None
                
                # Check for common security headers
                security_headers = {
                    'Strict-Transport-Security': 'Missing HSTS header',
                    'Content-Security-Policy': 'Missing Content-Security-Policy header',
                    'X-Content-Type-Options': 'Missing X-Content-Type-Options header',
                    'X-Frame-Options': 'Missing X-Frame-Options header',
                    'X-XSS-Protection': 'Missing X-XSS-Protection header',
                    'Referrer-Policy': 'Missing Referrer-Policy header',
                    'Feature-Policy': 'Missing Feature-Policy/Permissions-Policy header',
                }
                
                missing_headers = []
                for header, message in security_headers.items():
                    if header not in response.headers:
                        missing_headers.append(message)
                        print(f"[!] {message}")
                
                web_results[url]['missing_security_headers'] = missing_headers
                
                # Check for server information disclosure
                if 'Server' in response.headers:
                    server = response.headers['Server']
                    print(f"[!] Server header reveals: {server}")
                    web_results[url]['server_disclosure'] = server
                
                # Check for potential form vulnerabilities
                forms = soup.find_all('form')
                form_issues = []
                for form in forms:
                    # Check for CSRF protection
                    csrf_tokens = form.find_all('input', attrs={'name': ['csrf', 'csrf_token', '_token', 'token']})
                    if not csrf_tokens:
                        issue = "Form without CSRF protection detected"
                        form_issues.append(issue)
                        print(f"[!] {issue}")
                    
                    # Check for insecure methods
                    if form.get('method', '').lower() != 'post':
                        issue = "Form using GET method instead of POST"
                        form_issues.append(issue)
                        print(f"[!] {issue}")
                
                web_results[url]['form_issues'] = form_issues
                
                # Check for common CMS and frameworks
                cms_signatures = {
                    'WordPress': ['wp-content', 'wp-includes', 'wp-admin'],
                    'Joomla': ['com_content', 'com_users', 'Joomla!'],
                    'Drupal': ['Drupal.settings', 'drupal.js', '/sites/default/files'],
                    'Magento': ['Mage.', 'magento', 'Magento_'],
                    'Django': ['csrfmiddlewaretoken', '__admin', 'django'],
                    'Laravel': ['laravel', 'csrf-token', 'XSRF-TOKEN'],
                    'ASP.NET': ['__VIEWSTATE', '__EVENTVALIDATION', 'ASP.NET'],
                    'PHP': ['PHPSESSID'],
                }
                
                detected_cms = []
                page_text = response.text.lower()
                for cms, signatures in cms_signatures.items():
                    for signature in signatures:
                        if signature.lower() in page_text:
                            detected_cms.append(cms)
                            print(f"[+] Detected {cms} framework")
                            break
                
                web_results[url]['detected_cms'] = detected_cms
                
                # Check for common JS libraries and their versions
                js_libraries = []
                scripts = soup.find_all('script', src=True)
                for script in scripts:
                    src = script['src']
                    for lib in ['jquery', 'bootstrap', 'angular', 'react', 'vue']:
                        if lib in src.lower():
                            js_libraries.append(src)
                            print(f"[+] Detected JS library: {src}")
                
                web_results[url]['js_libraries'] = js_libraries
                
                print(f"[+] Completed scan of {url} (Status: {response.status_code})")
                
                # Run gobuster directory scan if requested
                if self.args.dir_scan or self.args.full_scan:
                    gobuster_results = self.run_gobuster(url)
                    web_results[url]['gobuster_scan'] = gobuster_results
                
            except requests.exceptions.RequestException as e:
                print(f"[-] Error scanning {url}: {str(e)}")
                web_results[url]['error'] = str(e)
        
        return web_results

    def scan_target(self):
        """Scan a single IP address"""
        # Initialize results dictionary
        self.results['scan_info'] = {
            'target': self.target,
            'start_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'scan_type': 'full' if self.args.full_scan else 'custom',
        }
        
        # Get WHOIS information if hostname is available
        if 'hostname' in self.results or not self.target.replace('.', '').isdigit():
            self.get_whois_info()
            self.get_dns_info()
        
        # Scan ports
        port_results = self.scan_ports(self.target, self.args.ports)
        self.results['port_scan'] = port_results
        
        # Scan web vulnerabilities if requested or if full scan
        if self.args.web_scan or self.args.full_scan:
            web_results = self.scan_web_vulnerabilities(self.target, port_results)
            self.results['web_scan'] = web_results
        
        # Record end time
        self.results['scan_info']['end_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return self.results

    def scan_network(self):
        """Scan a network range (CIDR notation)"""
        network = ipaddress.ip_network(self.target, strict=False)
        print(f"[*] Scanning network {network} ({network.num_addresses} hosts)...")
        
        self.results['scan_info'] = {
            'target': str(network),
            'start_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'scan_type': 'network',
            'total_hosts': network.num_addresses
        }
        
        self.results['hosts'] = {}
        
        # Use a thread pool for parallel scanning
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.args.threads) as executor:
            futures = {}
            for ip in network.hosts():
                ip_str = str(ip)
                futures[executor.submit(self.ping_host, ip_str)] = ip_str
            
            live_hosts = []
            for future in concurrent.futures.as_completed(futures):
                ip = futures[future]
                if future.result():
                    live_hosts.append(ip)
            
            print(f"[+] Found {len(live_hosts)} live hosts")
            
            # Now scan each live host
            scan_futures = {}
            for ip in live_hosts:
                scan_futures[executor.submit(self.scan_ports, ip, self.args.ports)] = ip
            
            for future in concurrent.futures.as_completed(scan_futures):
                ip = scan_futures[future]
                port_results = future.result()
                self.results['hosts'][ip] = {'port_scan': port_results}
                
                # Scan web vulnerabilities if requested
                if self.args.web_scan or self.args.full_scan:
                    web_results = self.scan_web_vulnerabilities(ip, port_results)
                    self.results['hosts'][ip]['web_scan'] = web_results
        
        # Record end time
        self.results['scan_info']['end_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.results['scan_info']['live_hosts'] = len(self.results['hosts'])
        
        return self.results

    def ping_host(self, ip):
        """Check if a host is up using Nmap ping scan"""
        if self.args.no_ping:
            return True
            
        try:
            result = self.nm.scan(ip, arguments="-sn")
            if 'scan' in result and ip in result['scan'] and 'status' in result['scan'][ip]:
                if result['scan'][ip]['status']['state'] == 'up':
                    print(f"[+] Host {ip} is up")
                    return True
            return False
        except Exception:
            return False

    def save_results(self):
        """Save scan results to a file"""
        if not self.output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.output_file = f"nexusprobe_scan_{timestamp}.json"
        
        try:
            with open(self.output_file, 'w') as f:
                json.dump(self.results, f, indent=4)
            print(f"[+] Results saved to {self.output_file}")
            return True
        except Exception as e:
            print(f"[-] Error saving results: {str(e)}")
            return False

    def run(self):
        """Run the scanner"""
        self.print_banner()
        self.parse_arguments()
        
        # Normalize and validate target
        if not self.normalize_target():
            return False
        
        # Scan based on target type
        try:
            if '/' in self.target:  # CIDR notation
                self.scan_network()
            else:  # Single IP
                self.scan_target()
            
            # Save results
            self.save_results()
            
            print(f"\n[+] Scan completed successfully!")
            return True
            
        except KeyboardInterrupt:
            print(f"\n[!] Scan interrupted by user")
            self.save_results()
            return False
        except Exception as e:
            print(f"\n[-] Error during scan: {str(e)}")
            return False

def main():
    # Suppress InsecureRequestWarning
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    scanner = NexusProbe()
    scanner.run()

if __name__ == "__main__":
    main()
