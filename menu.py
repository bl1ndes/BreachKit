#!/usr/bin/env python3

import os
import sys
import subprocess
import json
import platform
import tempfile
import webbrowser
import requests
import shutil
import git
import time
from datetime import datetime
from urllib.parse import urlparse

# Import the main scanner
from breachkit.main import main as scanner_main

# Banner
BANNER = '''
=======================================================
                      BREACH KIT                       
=======================================================
[*] All-In-One Security & Penetration Testing Toolkit
[*] Version: 1.0.0
'''

# Global variables
TOOLS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools")
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

# Tool repositories
TOOL_REPOS = {
    "information_gathering": {
        "nmap": "https://github.com/nmap/nmap",
        "red_hawk": "https://github.com/Tuhinshubhra/RED_HAWK",
        "reconspider": "https://github.com/bhavsec/reconspider",
        "infoga": "https://github.com/m4ll0k/Infoga",
        "recondog": "https://github.com/s0md3v/ReconDog",
        "striker": "https://github.com/s0md3v/Striker",
        "secretfinder": "https://github.com/m4ll0k/SecretFinder",
        "shodanfy": "https://github.com/m4ll0k/Shodanfy.py",
        "breacher": "https://github.com/s0md3v/Breacher"
    },
    "wordlist_generator": {
        "cupp": "https://github.com/Mebus/cupp.git",
        "wordlistcreator": "https://github.com/Z4nzu/wlcreator",
        "goblin": "https://github.com/UndeadSec/GoblinWordGenerator.git"
    },
    "wireless_testing": {
        "wifipumpkin3": "https://github.com/P0cL4bs/wifipumpkin3",
        "pixiewps": "https://github.com/wiire/pixiewps",
        "bluepot": "https://github.com/andrewmichaelsmith/bluepot",
        "fluxion": "https://github.com/thehackingsage/Fluxion",
        "wifiphisher": "https://github.com/wifiphisher/wifiphisher",
        "wifite": "https://github.com/derv82/wifite2"
    },
    "sql_injection": {
        "sqlmap": "https://github.com/sqlmapproject/sqlmap",
        "nosqlmap": "https://github.com/codingo/NoSQLMap",
        "dsss": "https://github.com/stamparm/DSSS",
        "sqlscan": "https://github.com/Cvar1984/sqlscan"
    },
    "phishing": {
        "zphisher": "https://github.com/htr-tech/zphisher",
        "shellphish": "https://github.com/suljot/shellphish",
        "socialfish": "https://github.com/UndeadSec/SocialFish"
    },
    "web_attack": {
        "webdav": "https://github.com/hacdias/webdav",
        "xsstrike": "https://github.com/s0md3v/XSStrike",
        "brutespray": "https://github.com/x90skysn3k/brutespray"
    },
    "post_exploitation": {
        "weevely": "https://github.com/epinna/weevely3",
        "beef": "https://github.com/beefproject/beef"
    },
    "forensic": {
        "autopsy": "https://github.com/sleuthkit/autopsy",
        "bulk_extractor": "https://github.com/simsong/bulk_extractor"
    },
    "payload_creator": {
        "metasploit": "https://github.com/rapid7/metasploit-framework",
        "venom": "https://github.com/r00t-3xp10it/venom"
    },
    "ddos": {
        "slowloris": "https://github.com/gkbrk/slowloris",
        "hammer": "https://github.com/cyweb/hammer"
    },
    "steganography": {
        "steghide": "https://github.com/StefanoDeVuono/steghide",
        "stegcracker": "https://github.com/Paradoxis/StegCracker"
    }
}

class ReconicMenu:
    def __init__(self):
        self.os_type = platform.system().lower()
        self.create_tools_dir()
        self.load_config()
        self.check_dependencies()
    
    def create_tools_dir(self):
        """Create tools directory if it doesn't exist"""
        if not os.path.exists(TOOLS_DIR):
            os.makedirs(TOOLS_DIR)
            # Create category directories
            for category in TOOL_REPOS.keys():
                category_dir = os.path.join(TOOLS_DIR, category)
                if not os.path.exists(category_dir):
                    os.makedirs(category_dir)
    
    def load_config(self):
        """Load configuration from config file"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    self.config = json.load(f)
            except:
                self.config = self.default_config()
                self.save_config()
        else:
            self.config = self.default_config()
            self.save_config()
    
    def save_config(self):
        """Save configuration to config file"""
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def default_config(self):
        """Create default configuration"""
        return {
            "installed_tools": [],
            "last_scan": None,
            "default_wordlist": None,
            "proxy": None,
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
    
    def check_dependencies(self):
        """Check if required dependencies are installed"""
        try:
            import git
        except ImportError:
            print("[!] GitPython is not installed. Installing...")
            self.run_command("pip install gitpython")
        
        # Check for system dependencies
        if self.os_type == "linux":
            # Check if apt or yum is available
            apt_available = self.run_command("which apt", silent=True)
            yum_available = self.run_command("which yum", silent=True)
            pacman_available = self.run_command("which pacman", silent=True)
            
            if apt_available:
                self.package_manager = "apt"
            elif yum_available:
                self.package_manager = "yum"
            elif pacman_available:
                self.package_manager = "pacman"
            else:
                self.package_manager = None
                print("[!] No supported package manager found. You may need to install dependencies manually.")
        elif self.os_type == "windows":
            # Check if chocolatey is available
            choco_available = self.run_command("where choco", silent=True)
            if choco_available:
                self.package_manager = "choco"
            else:
                self.package_manager = None
                print("[!] Chocolatey not found. You may need to install dependencies manually.")
        else:
            # macOS
            brew_available = self.run_command("which brew", silent=True)
            if brew_available:
                self.package_manager = "brew"
            else:
                self.package_manager = None
                print("[!] Homebrew not found. You may need to install dependencies manually.")
    
    def clear_screen(self):
        """Clear the terminal screen"""
        if self.os_type == "windows":
            os.system('cls')
        else:
            os.system('clear')
    
    def print_banner(self):
        """Print the NexusProbe banner"""
        self.clear_screen()
        print(BANNER)
    
    def print_menu(self):
        """Print the main menu"""
        self.print_banner()
        print("[*] Select a category:")
        print("\n[1] Information Gathering")
        print("[2] Vulnerability Scanning")
        print("[3] Web Application Analysis")
        print("[4] Network Tools")
        print("[5] Exploitation Tools")
        print("[6] Password Attacks")
        print("[7] Wireless Testing")
        print("[8] Anonymity & Privacy")
        print("[9] Forensics Tools")
        print("[10] Social Engineering")
        print("[11] Steganography")
        print("[12] OSINT Tools")
        print("[13] Reverse Engineering")
        print("[14] Malware Analysis")
        print("[15] Settings")
        print("[16] Wordlist Generator")
        print("[17] SQL Injection Tools")
        print("[0] Exit")
        
        choice = input("\n[?] Select an option: ")
        self.handle_main_menu(choice)
    
    def handle_main_menu(self, choice):
        """Handle main menu selection"""
        if choice == "1":
            self.information_gathering_menu()
        elif choice == "2":
            self.vulnerability_scanning_menu()
        elif choice == "3":
            self.web_application_menu()
        elif choice == "4":
            self.network_tools_menu()
        elif choice == "5":
            self.exploitation_tools_menu()
        elif choice == "6":
            self.password_attacks_menu()
        elif choice == "7":
            self.wireless_testing_menu()
        elif choice == "8":
            self.anonymity_menu()
        elif choice == "9":
            self.forensics_menu()
        elif choice == "10":
            self.social_engineering_menu()
        elif choice == "11":
            self.steganography_menu()
        elif choice == "12":
            self.osint_menu()
        elif choice == "13":
            self.reverse_engineering_menu()
        elif choice == "14":
            self.malware_analysis_menu()
        elif choice == "15":
            self.settings_menu()
        elif choice == "16":
            self.wordlist_generator_menu()
        elif choice == "17":
            self.sql_injection_menu()
        elif choice == "0":
            print("\n[*] Thank you for using NexusProbe!")
            sys.exit(0)
        else:
            print("\n[!] Invalid option. Press Enter to continue...")
            input()
            self.print_menu()
    
    def back_to_main_menu(self):
        """Return to main menu"""
        print("\n[*] Press Enter to return to the main menu...")
        input()
        self.print_menu()
    
    def run_command(self, command, cwd=None, silent=False):
        """Run a system command"""
        try:
            if silent:
                result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
                return result.returncode == 0
            else:
                subprocess.run(command, shell=True, check=True, cwd=cwd)
                return True
        except subprocess.CalledProcessError as e:
            if not silent:
                print(f"[!] Command failed: {e}")
            return False
        except Exception as e:
            if not silent:
                print(f"[!] Error: {e}")
            return False
    
    def download_tool(self, category, tool_name, repo_url):
        """Download a tool from its repository"""
        tool_dir = os.path.join(TOOLS_DIR, category, tool_name)
        
        # Check if tool directory already exists
        if os.path.exists(tool_dir):
            print(f"[*] {tool_name} is already downloaded. Updating...")
            try:
                # Try to update the repository
                repo = git.Repo(tool_dir)
                origin = repo.remotes.origin
                origin.pull()
                print(f"[+] {tool_name} updated successfully!")
                return True
            except Exception as e:
                print(f"[!] Failed to update {tool_name}: {e}")
                print(f"[*] Removing existing directory and re-downloading...")
                shutil.rmtree(tool_dir, ignore_errors=True)
        
        # Clone the repository
        print(f"[*] Downloading {tool_name} from {repo_url}...")
        try:
            git.Repo.clone_from(repo_url, tool_dir)
            print(f"[+] {tool_name} downloaded successfully!")
            return True
        except Exception as e:
            print(f"[!] Failed to download {tool_name}: {e}")
            return False
    
    def install_system_dependencies(self, dependencies):
        """Install system dependencies using the appropriate package manager"""
        if not self.package_manager:
            print("[!] No package manager available. Please install dependencies manually.")
            print(f"[*] Required dependencies: {', '.join(dependencies)}")
            return False
        
        if self.package_manager == "apt":
            cmd = f"apt update && apt install -y {' '.join(dependencies)}"
        elif self.package_manager == "yum":
            cmd = f"yum install -y {' '.join(dependencies)}"
        elif self.package_manager == "pacman":
            cmd = f"pacman -Sy --noconfirm {' '.join(dependencies)}"
        elif self.package_manager == "brew":
            cmd = f"brew install {' '.join(dependencies)}"
        elif self.package_manager == "choco":
            cmd = f"choco install -y {' '.join(dependencies)}"
        else:
            print("[!] Unsupported package manager.")
            return False
        
        print(f"[*] Installing system dependencies: {', '.join(dependencies)}")
        if self.os_type != "windows" and os.geteuid() != 0:
            print("[!] Root privileges required to install system dependencies.")
            cmd = f"sudo {cmd}"
        
        return self.run_command(cmd)
    
    def install_python_dependencies(self, requirements_file=None, packages=None):
        """Install Python dependencies using pip"""
        if requirements_file and os.path.exists(requirements_file):
            print(f"[*] Installing Python dependencies from {requirements_file}...")
            return self.run_command(f"pip install -r {requirements_file}")
        elif packages:
            print(f"[*] Installing Python packages: {', '.join(packages)}...")
            return self.run_command(f"pip install {' '.join(packages)}")
        return False
    
    def install_tool(self, category, tool_name):
        """Install a tool"""
        if category not in TOOL_REPOS or tool_name not in TOOL_REPOS[category]:
            print(f"[!] Tool {tool_name} not found in category {category}.")
            return False
        
        repo_url = TOOL_REPOS[category][tool_name]
        tool_dir = os.path.join(TOOLS_DIR, category, tool_name)
        
        # Download the tool
        if not self.download_tool(category, tool_name, repo_url):
            return False
        
        # Check for requirements.txt and install dependencies
        requirements_file = os.path.join(tool_dir, "requirements.txt")
        if os.path.exists(requirements_file):
            self.install_python_dependencies(requirements_file=requirements_file)
        
        # Check for setup.py and install the tool
        setup_file = os.path.join(tool_dir, "setup.py")
        if os.path.exists(setup_file):
            print(f"[*] Installing {tool_name} using setup.py...")
            self.run_command(f"pip install -e .", cwd=tool_dir)
        
        # Add to installed tools list
        tool_id = f"{category}/{tool_name}"
        if tool_id not in self.config["installed_tools"]:
            self.config["installed_tools"].append(tool_id)
            self.save_config()
        
        print(f"[+] {tool_name} installed successfully!")
        return True
    
    def check_tool(self, tool_name, tool_command):
        """Check if a tool is installed"""
        try:
            result = subprocess.run(f"{tool_command} --version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                return True
            return False
        except:
            return False
    
    def install_tool(self, tool_name, install_command):
        """Install a tool"""
        print(f"[*] Installing {tool_name}...")
        if self.run_command(install_command):
            print(f"[+] {tool_name} installed successfully!")
            if tool_name not in self.config["installed_tools"]:
                self.config["installed_tools"].append(tool_name)
                self.save_config()
            return True
        else:
            print(f"[!] Failed to install {tool_name}")
            return False
    
    def run_tool(self, category, tool_name, args=None):
        """Run a tool, install if needed"""
        tool_id = f"{category}/{tool_name}"
        tool_dir = os.path.join(TOOLS_DIR, category, tool_name)
        
        # Check if tool is installed
        if tool_id not in self.config["installed_tools"]:
            print(f"[!] {tool_name} is not installed.")
            choice = input(f"[?] Do you want to install {tool_name}? (y/n): ")
            if choice.lower() == "y":
                if not self.install_tool(category, tool_name):
                    return False
            else:
                return False
        
        # Check if tool directory exists
        if not os.path.exists(tool_dir):
            print(f"[!] Tool directory for {tool_name} not found. Reinstalling...")
            if not self.install_tool(category, tool_name):
                return False
        
        # Determine how to run the tool
        print(f"[*] Running {tool_name}...")
        
        # Look for main executable files in order of preference
        executables = [
            os.path.join(tool_dir, tool_name + ".py"),
            os.path.join(tool_dir, "main.py"),
            os.path.join(tool_dir, "__main__.py"),
            os.path.join(tool_dir, tool_name),  # For compiled tools
            os.path.join(tool_dir, tool_name.lower()),  # For compiled tools with lowercase name
        ]
        
        # Check for setup.py installed tools
        if os.path.exists(os.path.join(tool_dir, "setup.py")):
            # Try to run as an installed package
            cmd = f"{tool_name} {args if args else ''}"
            if self.run_command(cmd, silent=True):
                return True
        
        # Try each executable
        for exe in executables:
            if os.path.exists(exe):
                # Check if file is executable
                if self.os_type != "windows" and not os.access(exe, os.X_OK):
                    self.run_command(f"chmod +x {exe}")
                
                # Run the tool
                if exe.endswith(".py"):
                    cmd = f"python {exe} {args if args else ''}"
                else:
                    cmd = f"{exe} {args if args else ''}"
                
                return self.run_command(cmd, cwd=tool_dir)
        
        # If no executable found, try running with python
        if os.path.exists(tool_dir):
            # Find any Python files
            py_files = [f for f in os.listdir(tool_dir) if f.endswith(".py") and not f.startswith("__")]
            if py_files:
                # Use the first Python file found
                cmd = f"python {os.path.join(tool_dir, py_files[0])} {args if args else ''}"
                return self.run_command(cmd, cwd=tool_dir)
        
        print(f"[!] Could not find a way to run {tool_name}. Please run it manually.")
        return False
    
    # Information Gathering Menu
    def information_gathering_menu(self):
        self.print_banner()
        print("[*] Information Gathering Tools:")
        print("\n[1] Network Scanning (Nmap)")
        print("[2] RED HAWK (All-In-One Scanner)")
        print("[3] ReconSpider (OSINT Framework)")
        print("[4] Infoga (Email OSINT)")
        print("[5] ReconDog (Reconnaissance Tool)")
        print("[6] Striker (Web Vulnerability Scanner)")
        print("[7] SecretFinder (API Key Finder)")
        print("[8] Shodanfy (Shodan Search)")
        print("[9] Breacher (Admin Panel Finder)")
        print("[10] NexusProbe Scanner")
        print("[0] Back to Main Menu")
        
        choice = input("\n[?] Select an option: ")
        
        if choice == "1":
            self.run_nmap_scan()
        elif choice == "2":
            self.run_red_hawk()
        elif choice == "3":
            self.run_reconspider()
        elif choice == "4":
            self.run_infoga()
        elif choice == "5":
            self.run_recondog()
        elif choice == "6":
            self.run_striker()
        elif choice == "7":
            self.run_secretfinder()
        elif choice == "8":
            self.run_shodanfy()
        elif choice == "9":
            self.run_breacher()
        elif choice == "10":
            self.run_nexusprobe_scan()
        elif choice == "0":
            self.print_menu()
        else:
            print("\n[!] Invalid option. Press Enter to continue...")
            input()
            self.information_gathering_menu()
    
    def run_nmap_scan(self):
        """Run Nmap scan using the integrated nmap tool"""
        target = input("\n[?] Enter target IP/domain: ")
        scan_type = input("[?] Select scan type (1: Basic, 2: Comprehensive, 3: Vulnerability): ")
        
        if scan_type == "1":
            args = f"-sV -T4 -F {target}"
        elif scan_type == "2":
            args = f"-sV -sC -T4 -A -p- {target}"
        elif scan_type == "3":
            args = f"-sV -sC -T4 -A --script vuln -p- {target}"
        else:
            print("[!] Invalid scan type. Using basic scan.")
            args = f"-sV -T4 -F {target}"
        
        self.run_tool("information_gathering", "nmap", args)
        self.back_to_main_menu()
    
    def run_red_hawk(self):
        """Run RED HAWK scanner"""
        target = input("\n[?] Enter target website (e.g., example.com): ")
        self.run_tool("information_gathering", "red_hawk", target)
        self.back_to_main_menu()
    
    def run_reconspider(self):
        """Run ReconSpider OSINT framework"""
        self.run_tool("information_gathering", "reconspider")
        self.back_to_main_menu()
    
    def run_infoga(self):
        """Run Infoga email OSINT tool"""
        target = input("\n[?] Enter target email or domain: ")
        args = f"-d {target} -v 2"
        self.run_tool("information_gathering", "infoga", args)
        self.back_to_main_menu()
    
    def run_recondog(self):
        """Run ReconDog reconnaissance tool"""
        self.run_tool("information_gathering", "recondog")
        self.back_to_main_menu()
    
    def run_striker(self):
        """Run Striker web vulnerability scanner"""
        target = input("\n[?] Enter target website (e.g., example.com): ")
        self.run_tool("information_gathering", "striker", target)
        self.back_to_main_menu()
    
    def run_secretfinder(self):
        """Run SecretFinder API key finder"""
        target = input("\n[?] Enter target URL: ")
        args = f"-u {target} -o cli"
        self.run_tool("information_gathering", "secretfinder", args)
        self.back_to_main_menu()
    
    def run_shodanfy(self):
        """Run Shodanfy for Shodan searches"""
        target = input("\n[?] Enter target IP or domain: ")
        self.run_tool("information_gathering", "shodanfy", target)
        self.back_to_main_menu()
    
    def run_breacher(self):
        """Run Breacher admin panel finder"""
        target = input("\n[?] Enter target URL (e.g., http://example.com): ")
        self.run_tool("information_gathering", "breacher", target)
        self.back_to_main_menu()
    
    def run_nexusprobe_scan(self):
        """Run NexusProbe's built-in scanner"""
        target = input("\n[?] Enter target IP/domain: ")
        scan_type = input("[?] Select scan type (1: Basic, 2: Comprehensive, 3: Vulnerability): ")
        
        if scan_type == "1":
            command = f"nexusprobe -t {target} -p 1-1000"
        elif scan_type == "2":
            command = f"nexusprobe -t {target} -p 1-65535 --full-scan"
        elif scan_type == "3":
            command = f"nexusprobe -t {target} -p 1-65535 --full-scan --web-scan"
        else:
            print("[!] Invalid scan type. Using basic scan.")
            command = f"nexusprobe -t {target} -p 1-1000"
        
        self.run_command(command)
        self.back_to_main_menu()
    
    # Wordlist Generator Menu
    def wordlist_generator_menu(self):
        self.print_banner()
        print("[*] Wordlist Generator Tools:")
        print("\n[1] Cupp (Common User Passwords Profiler)")
        print("[2] WordlistCreator")
        print("[3] Goblin Word Generator")
        print("[0] Back to Main Menu")
        
        choice = input("\n[?] Select an option: ")
        
        if choice == "1":
            self.run_cupp()
        elif choice == "2":
            self.run_wordlistcreator()
        elif choice == "3":
            self.run_goblin()
        elif choice == "0":
            self.print_menu()
        else:
            print("\n[!] Invalid option. Press Enter to continue...")
            input()
            self.wordlist_generator_menu()
    
    def run_cupp(self):
        """Run Cupp password profiler"""
        self.run_tool("wordlist_generator", "cupp")
        self.back_to_main_menu()
    
    def run_wordlistcreator(self):
        """Run WordlistCreator"""
        self.run_tool("wordlist_generator", "wordlistcreator")
        self.back_to_main_menu()
    
    def run_goblin(self):
        """Run Goblin Word Generator"""
        self.run_tool("wordlist_generator", "goblin")
        self.back_to_main_menu()
    
    # Vulnerability Scanning Menu
    def vulnerability_scanning_menu(self):
        self.print_banner()
        print("[*] Vulnerability Scanning Tools:")
        print("\n[1] Web Vulnerability Scan")
        print("[2] Network Vulnerability Scan")
        print("[3] CMS Vulnerability Scan")
        print("[4] SSL/TLS Vulnerability Scan")
        print("[5] SQL Injection Scanner")
        print("[6] XSS Scanner")
        print("[7] Directory Traversal Scanner")
        print("[8] File Inclusion Scanner")
        print("[9] Command Injection Scanner")
        print("[10] CORS Misconfiguration Scanner")
        print("[0] Back to Main Menu")
        
        choice = input("\n[?] Select an option: ")
        
        if choice == "1":
            self.run_web_vuln_scan()
        elif choice == "2":
            self.run_network_vuln_scan()
        elif choice == "3":
            self.run_cms_vuln_scan()
        elif choice == "4":
            self.run_ssl_vuln_scan()
        elif choice == "5":
            self.run_sqli_scanner()
        elif choice == "6":
            self.run_xss_scanner()
        elif choice == "7":
            self.run_dir_traversal_scanner()
        elif choice == "8":
            self.run_file_inclusion_scanner()
        elif choice == "9":
            self.run_command_injection_scanner()
        elif choice == "10":
            self.run_cors_scanner()
        elif choice == "0":
            self.print_menu()
        else:
            print("\n[!] Invalid option. Press Enter to continue...")
            input()
            self.vulnerability_scanning_menu()
    
    # SQL Injection Menu
    def sql_injection_menu(self):
        self.print_banner()
        print("[*] SQL Injection Tools:")
        print("\n[1] SQLMap")
        print("[2] NoSQLMap")
        print("[3] Damn Small SQLi Scanner (DSSS)")
        print("[4] SQLScan")
        print("[0] Back to Main Menu")
        
        choice = input("\n[?] Select an option: ")
        
        if choice == "1":
            self.run_sqlmap()
        elif choice == "2":
            self.run_nosqlmap()
        elif choice == "3":
            self.run_dsss()
        elif choice == "4":
            self.run_sqlscan()
        elif choice == "0":
            self.print_menu()
        else:
            print("\n[!] Invalid option. Press Enter to continue...")
            input()
            self.sql_injection_menu()
    
    def run_sqlmap(self):
        """Run SQLMap"""
        target = input("\n[?] Enter target URL: ")
        args = f"-u {target} --batch --dbs"
        self.run_tool("sql_injection", "sqlmap", args)
        self.back_to_main_menu()
    
    def run_nosqlmap(self):
        """Run NoSQLMap"""
        self.run_tool("sql_injection", "nosqlmap")
        self.back_to_main_menu()
    
    def run_dsss(self):
        """Run Damn Small SQLi Scanner"""
        target = input("\n[?] Enter target URL: ")
        self.run_tool("sql_injection", "dsss", target)
        self.back_to_main_menu()
    
    def run_sqlscan(self):
        """Run SQLScan"""
        self.run_tool("sql_injection", "sqlscan")
        self.back_to_main_menu()
    
    def run_sqli_scanner(self):
        """Run SQL Injection Scanner"""
        target = input("\n[?] Enter target URL: ")
        command = f"nexusprobe -t {target} --web-scan --sql-scan -v"
        self.run_command(command)
        self.back_to_main_menu()
    
    def run_web_vuln_scan(self):
        """Run Web Vulnerability Scan"""
        target = input("\n[?] Enter target URL: ")
        command = f"nexusprobe -t {target} --web-scan -v"
        self.run_command(command)
        self.back_to_main_menu()
        
    # Web Application Analysis Menu
    def web_application_menu(self):
        self.print_banner()
        print("[*] Web Application Analysis Tools:")
        print("\n[1] Directory Enumeration (Gobuster)")
        print("[2] Web Crawler")
        print("[3] Web Fuzzer")
        print("[4] CMS Detector")
        print("[5] Web Technology Detector")
        print("[6] API Scanner")
        print("[7] Web Parameter Scanner")
        print("[8] Web Cache Scanner")
        print("[9] Web Screenshot Tool")
        print("[10] Web Archive Scanner")
        print("[0] Back to Main Menu")
        
        choice = input("\n[?] Select an option: ")
        
        if choice == "1":
            self.run_directory_enum()
        elif choice == "2":
            self.run_web_crawler()
        elif choice == "3":
            self.run_web_fuzzer()
        elif choice == "4":
            self.run_cms_detector()
        elif choice == "5":
            self.run_tech_detector()
        elif choice == "6":
            self.run_api_scanner()
        elif choice == "7":
            self.run_param_scanner()
        elif choice == "8":
            self.run_cache_scanner()
        elif choice == "9":
            self.run_web_screenshot()
        elif choice == "10":
            self.run_web_archive()
        elif choice == "0":
            self.print_menu()
        else:
            print("\n[!] Invalid option. Press Enter to continue...")
            input()
            self.web_application_menu()
    
    def run_directory_enum(self):
        """Run Directory Enumeration"""
        target = input("\n[?] Enter target URL: ")
        wordlist = input("[?] Enter wordlist path (leave empty for default): ")
        
        if not wordlist:
            command = f"nexusprobe -t {target} --web-scan --dir-scan -v"
        else:
            command = f"nexusprobe -t {target} --web-scan --dir-scan --wordlist {wordlist} -v"
        
        self.run_command(command)
        self.back_to_main_menu()
    
    # Network Tools Menu
    def network_tools_menu(self):
        self.print_banner()
        print("[*] Network Tools:")
        print("\n[1] Port Scanner")
        print("[2] Network Sniffer")
        print("[3] ARP Scanner")
        print("[4] DNS Lookup")
        print("[5] Traceroute")
        print("[6] Banner Grabber")
        print("[7] MAC Address Changer")
        print("[8] Network Mapper")
        print("[9] Packet Analyzer")
        print("[10] Network Traffic Generator")
        print("[0] Back to Main Menu")
        
        choice = input("\n[?] Select an option: ")
        
        if choice == "1":
            self.run_port_scanner()
        elif choice == "2":
            self.run_network_sniffer()
        elif choice == "3":
            self.run_arp_scanner()
        elif choice == "4":
            self.run_dns_lookup()
        elif choice == "5":
            self.run_traceroute()
        elif choice == "6":
            self.run_banner_grabber()
        elif choice == "7":
            self.run_mac_changer()
        elif choice == "8":
            self.run_network_mapper()
        elif choice == "9":
            self.run_packet_analyzer()
        elif choice == "10":
            self.run_traffic_generator()
        elif choice == "0":
            self.print_menu()
        else:
            print("\n[!] Invalid option. Press Enter to continue...")
            input()
            self.network_tools_menu()
    
    def run_port_scanner(self):
        """Run Port Scanner"""
        target = input("\n[?] Enter target IP/domain: ")
        port_range = input("[?] Enter port range (e.g., 1-1000): ")
        
        if not port_range:
            port_range = "1-1000"
        
        command = f"nexusprobe -t {target} -p {port_range} -v"
        self.run_command(command)
        self.back_to_main_menu()
    
    # Settings Menu
    def settings_menu(self):
        self.print_banner()
        print("[*] Settings:")
        print("\n[1] Set Default Wordlist")
        print("[2] Configure Proxy")
        print("[3] Set User Agent")
        print("[4] View Installed Tools")
        print("[5] Check for Updates")
        print("[6] Import/Export Configuration")
        print("[7] Reset Configuration")
        print("[8] Tool Installation Status")
        print("[0] Back to Main Menu")
        
        choice = input("\n[?] Select an option: ")
        
        if choice == "1":
            self.set_default_wordlist()
        elif choice == "2":
            self.configure_proxy()
        elif choice == "3":
            self.set_user_agent()
        elif choice == "4":
            self.view_installed_tools()
        elif choice == "5":
            self.check_for_updates()
        elif choice == "6":
            self.import_export_config()
        elif choice == "7":
            self.reset_config()
        elif choice == "8":
            self.check_tool_status()
        elif choice == "0":
            self.print_menu()
        else:
            print("\n[!] Invalid option. Press Enter to continue...")
            input()
            self.settings_menu()
    
    def set_default_wordlist(self):
        """Set default wordlist"""
        print("\n[*] Current default wordlist:", self.config["default_wordlist"])
        new_wordlist = input("[?] Enter path to new default wordlist (leave empty to keep current): ")
        
        if new_wordlist:
            if os.path.exists(new_wordlist):
                self.config["default_wordlist"] = new_wordlist
                self.save_config()
                print("[+] Default wordlist updated successfully!")
            else:
                print("[!] Wordlist file not found.")
        
        self.back_to_main_menu()
    
    def view_installed_tools(self):
        """View installed tools"""
        print("\n[*] Installed Tools:")
        if not self.config["installed_tools"]:
            print("[!] No tools installed yet.")
        else:
            for i, tool in enumerate(self.config["installed_tools"], 1):
                print(f"[{i}] {tool}")
        
        self.back_to_main_menu()
    
    def check_tool_status(self):
        """Check installation status of all tools"""
        self.print_banner()
        print("[*] Tool Installation Status:")
        print("\n{:<5} {:<20} {:<15} {:<40}".format("#", "Category", "Tool", "Status"))
        print("-" * 80)
        
        # Count variables
        installed_count = 0
        update_available_count = 0
        not_installed_count = 0
        total_count = 0
        
        # Process each category and tool
        tool_index = 1
        for category, tools in TOOL_REPOS.items():
            for tool_name, repo_url in tools.items():
                total_count += 1
                tool_id = f"{category}/{tool_name}"
                tool_dir = os.path.join(TOOLS_DIR, category, tool_name)
                
                # Check if tool is installed
                if tool_id in self.config["installed_tools"] and os.path.exists(tool_dir):
                    # Check if update is available
                    try:
                        repo = git.Repo(tool_dir)
                        origin = repo.remotes.origin
                        origin.fetch()
                        commits_behind = len(list(repo.iter_commits('HEAD..origin/master'))) or len(list(repo.iter_commits('HEAD..origin/main')))
                        
                        if commits_behind > 0:
                            status = f"Installed (Update available: {commits_behind} commits behind)"
                            update_available_count += 1
                        else:
                            status = "Installed (Up to date)"
                            installed_count += 1
                    except Exception:
                        status = "Installed"
                        installed_count += 1
                else:
                    status = "Not installed"
                    not_installed_count += 1
                
                print("{:<5} {:<20} {:<15} {:<40}".format(
                    tool_index, category.replace("_", " ").title(), 
                    tool_name, status
                ))
                tool_index += 1
        
        # Print summary
        print("\n[*] Summary:")
        print(f"    Total tools: {total_count}")
        print(f"    Installed (up to date): {installed_count}")
        print(f"    Updates available: {update_available_count}")
        print(f"    Not installed: {not_installed_count}")
        
        # Ask if user wants to install or update tools
        print("\n[*] Options:")
        print("[1] Install all missing tools")
        print("[2] Update all tools")
        print("[3] Install/update specific tool")
        print("[4] Search for tools")
        print("[5] Check tool dependencies")
        print("[6] View tool documentation")
        print("[0] Back to Settings Menu")
        
        choice = input("\n[?] Select an option: ")
        
        if choice == "1":
            self.install_all_tools()
        elif choice == "2":
            self.update_all_tools()
        elif choice == "3":
            self.install_specific_tool()
        elif choice == "4":
            self.search_tools()
        elif choice == "5":
            self.check_tool_dependencies()
        elif choice == "6":
            self.view_tool_documentation()
        elif choice == "0":
            self.settings_menu()
        else:
            print("\n[!] Invalid option. Press Enter to continue...")
            input()
            self.check_tool_status()
    
    def install_all_tools(self):
        """Install all missing tools"""
        print("\n[*] Installing all missing tools...")
        
        for category, tools in TOOL_REPOS.items():
            for tool_name, repo_url in tools.items():
                tool_id = f"{category}/{tool_name}"
                tool_dir = os.path.join(TOOLS_DIR, category, tool_name)
                
                if tool_id not in self.config["installed_tools"] or not os.path.exists(tool_dir):
                    print(f"\n[*] Installing {tool_name} from category {category}...")
                    self.install_tool(category, tool_name)
        
        print("\n[+] All tools have been installed or attempted to install.")
        self.back_to_main_menu()
    
    def update_all_tools(self):
        """Update all installed tools"""
        print("\n[*] Updating all installed tools...")
        
        for tool_id in self.config["installed_tools"]:
            try:
                category, tool_name = tool_id.split("/")
                tool_dir = os.path.join(TOOLS_DIR, category, tool_name)
                
                if os.path.exists(tool_dir):
                    print(f"\n[*] Updating {tool_name}...")
                    try:
                        repo = git.Repo(tool_dir)
                        origin = repo.remotes.origin
                        origin.pull()
                        print(f"[+] {tool_name} updated successfully!")
                    except Exception as e:
                        print(f"[!] Failed to update {tool_name}: {e}")
            except Exception as e:
                print(f"[!] Error processing {tool_id}: {e}")
        
        print("\n[+] All tools have been updated or attempted to update.")
        self.back_to_main_menu()
    
    def install_specific_tool(self):
        """Install or update a specific tool"""
        print("\n[*] Available tools:")
        
        # List all tools with index
        tool_list = []
        for category, tools in TOOL_REPOS.items():
            for tool_name in tools.keys():
                tool_list.append((category, tool_name))
                print(f"[{len(tool_list)}] {category.replace('_', ' ').title()} - {tool_name}")
        
        # Get user selection
        try:
            selection = int(input("\n[?] Enter tool number to install/update (0 to cancel): "))
            if selection == 0:
                self.check_tool_status()
                return
            
            if 1 <= selection <= len(tool_list):
                category, tool_name = tool_list[selection - 1]
                print(f"\n[*] Installing/updating {tool_name}...")
                self.install_tool(category, tool_name)
                print("\n[+] Operation completed.")
            else:
                print("\n[!] Invalid selection.")
        except ValueError:
            print("\n[!] Invalid input. Please enter a number.")
        
        self.back_to_main_menu()
    
    def search_tools(self):
        """Search for tools by name or category"""
        self.print_banner()
        print("[*] Search for Tools")
        
        search_term = input("\n[?] Enter search term (tool name, category, or keyword): ").lower()
        if not search_term:
            print("[!] Search term cannot be empty.")
            time.sleep(1)
            self.check_tool_status()
            return
        
        print("\n[*] Search Results:")
        print("\n{:<5} {:<20} {:<15} {:<40}".format("#", "Category", "Tool", "Status"))
        print("-" * 80)
        
        # Search for matching tools
        tool_index = 1
        results = []
        
        for category, tools in TOOL_REPOS.items():
            category_display = category.replace("_", " ").title()
            if search_term in category.lower() or search_term in category_display.lower():
                # Category matches, include all tools
                for tool_name, repo_url in tools.items():
                    tool_id = f"{category}/{tool_name}"
                    tool_dir = os.path.join(TOOLS_DIR, category, tool_name)
                    status = self.get_tool_status(tool_id, tool_dir)
                    results.append((category, tool_name, status))
            else:
                # Check individual tools
                for tool_name, repo_url in tools.items():
                    if search_term in tool_name.lower():
                        tool_id = f"{category}/{tool_name}"
                        tool_dir = os.path.join(TOOLS_DIR, category, tool_name)
                        status = self.get_tool_status(tool_id, tool_dir)
                        results.append((category, tool_name, status))
        
        # Display results
        if not results:
            print("[!] No tools found matching your search term.")
        else:
            for category, tool_name, status in results:
                print("{:<5} {:<20} {:<15} {:<40}".format(
                    tool_index, category.replace("_", " ").title(), 
                    tool_name, status
                ))
                tool_index += 1
        
        # Options
        print("\n[*] Options:")
        print("[1] Install/update a tool from search results")
        print("[2] New search")
        print("[0] Back to Tool Status")
        
        choice = input("\n[?] Select an option: ")
        
        if choice == "1" and results:
            try:
                selection = int(input("\n[?] Enter tool number to install/update (0 to cancel): "))
                if selection == 0:
                    self.search_tools()
                    return
                
                if 1 <= selection <= len(results):
                    category, tool_name, _ = results[selection - 1]
                    print(f"\n[*] Installing/updating {tool_name}...")
                    self.install_tool(category, tool_name)
                    print("\n[+] Operation completed.")
                else:
                    print("\n[!] Invalid selection.")
            except ValueError:
                print("\n[!] Invalid input. Please enter a number.")
            
            time.sleep(1)
            self.check_tool_status()
        elif choice == "2":
            self.search_tools()
        else:
            self.check_tool_status()
    
    def get_tool_status(self, tool_id, tool_dir):
        """Get the status of a tool"""
        if tool_id in self.config["installed_tools"] and os.path.exists(tool_dir):
            # Check if update is available
            try:
                repo = git.Repo(tool_dir)
                origin = repo.remotes.origin
                origin.fetch()
                commits_behind = len(list(repo.iter_commits('HEAD..origin/master'))) or len(list(repo.iter_commits('HEAD..origin/main')))
                
                if commits_behind > 0:
                    return f"Installed (Update available: {commits_behind} commits behind)"
                else:
                    return "Installed (Up to date)"
            except Exception:
                return "Installed"
        else:
            return "Not installed"
    
    def check_tool_dependencies(self):
        """Check dependencies for installed tools"""
        self.print_banner()
        print("[*] Tool Dependency Check")
        
        # List installed tools
        print("\n[*] Select a tool to check dependencies:")
        installed_tools = []
        
        for i, tool_id in enumerate(self.config["installed_tools"], 1):
            try:
                category, tool_name = tool_id.split("/")
                installed_tools.append((category, tool_name))
                print(f"[{i}] {category.replace('_', ' ').title()} - {tool_name}")
            except:
                continue
        
        if not installed_tools:
            print("[!] No tools installed yet.")
            time.sleep(1)
            self.check_tool_status()
            return
        
        # Get user selection
        try:
            selection = int(input("\n[?] Enter tool number to check dependencies (0 to cancel): "))
            if selection == 0:
                self.check_tool_status()
                return
            
            if 1 <= selection <= len(installed_tools):
                category, tool_name = installed_tools[selection - 1]
                self.check_dependencies_for_tool(category, tool_name)
            else:
                print("\n[!] Invalid selection.")
                time.sleep(1)
                self.check_tool_dependencies()
        except ValueError:
            print("\n[!] Invalid input. Please enter a number.")
            time.sleep(1)
            self.check_tool_dependencies()
    
    def check_dependencies_for_tool(self, category, tool_name):
        """Check dependencies for a specific tool"""
        print(f"\n[*] Checking dependencies for {tool_name}...")
        tool_dir = os.path.join(TOOLS_DIR, category, tool_name)
        
        if not os.path.exists(tool_dir):
            print(f"[!] Tool directory not found: {tool_dir}")
            time.sleep(1)
            self.check_tool_dependencies()
            return
        
        # Check Python dependencies
        requirements_file = os.path.join(tool_dir, "requirements.txt")
        python_deps = []
        if os.path.exists(requirements_file):
            try:
                with open(requirements_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            python_deps.append(line)
            except Exception as e:
                print(f"[!] Error reading requirements.txt: {e}")
        
        # Check for setup.py
        setup_file = os.path.join(tool_dir, "setup.py")
        has_setup = os.path.exists(setup_file)
        
        # Look for README or documentation files
        readme_files = []
        for file in os.listdir(tool_dir):
            if file.lower().startswith('readme') or file.lower() == 'install' or file.lower() == 'requirements':
                readme_files.append(file)
        
        # Display results
        print("\n[*] Dependency Information:")
        print(f"\nTool: {tool_name} (Category: {category.replace('_', ' ').title()})")
        print(f"Location: {tool_dir}")
        
        if python_deps:
            print("\nPython Dependencies:")
            for dep in python_deps:
                print(f"  - {dep}")
        else:
            print("\nNo Python dependencies found in requirements.txt")
        
        if has_setup:
            print("\nSetup.py found - tool may have additional dependencies")
        
        if readme_files:
            print("\nDocumentation Files:")
            for file in readme_files:
                print(f"  - {file}")
        
        # Options
        print("\n[*] Options:")
        print("[1] Install Python dependencies")
        print("[2] View README/documentation")
        print("[0] Back to Tool Dependencies")
        
        choice = input("\n[?] Select an option: ")
        
        if choice == "1" and python_deps:
            print("\n[*] Installing Python dependencies...")
            self.install_python_dependencies(requirements_file=requirements_file)
            print("\n[+] Dependencies installed.")
            time.sleep(1)
            self.check_dependencies_for_tool(category, tool_name)
        elif choice == "2" and readme_files:
            self.view_readme_files(tool_dir, readme_files)
            self.check_dependencies_for_tool(category, tool_name)
        else:
            self.check_tool_dependencies()
    
    def view_readme_files(self, tool_dir, readme_files):
        """View README or documentation files"""
        print("\n[*] Select a file to view:")
        
        for i, file in enumerate(readme_files, 1):
            print(f"[{i}] {file}")
        
        print("[0] Back")
        
        try:
            selection = int(input("\n[?] Enter file number: "))
            if selection == 0:
                return
            
            if 1 <= selection <= len(readme_files):
                file_path = os.path.join(tool_dir, readme_files[selection - 1])
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                    
                    # Display file content with pagination
                    print(f"\n[*] Contents of {readme_files[selection - 1]}:")
                    print("\n" + "=" * 80)
                    
                    lines = content.split('\n')
                    page_size = 20
                    total_pages = (len(lines) + page_size - 1) // page_size
                    
                    for page in range(total_pages):
                        start = page * page_size
                        end = min((page + 1) * page_size, len(lines))
                        
                        print("\n" + "\n".join(lines[start:end]))
                        
                        if page < total_pages - 1:
                            choice = input(f"\n[*] Page {page + 1}/{total_pages}. Press Enter for next page, 'q' to quit: ")
                            if choice.lower() == 'q':
                                break
                    
                    print("\n" + "=" * 80)
                except Exception as e:
                    print(f"[!] Error reading file: {e}")
            else:
                print("[!] Invalid selection.")
        except ValueError:
            print("[!] Invalid input. Please enter a number.")
    
    def view_tool_documentation(self):
        """View documentation for tools"""
        self.print_banner()
        print("[*] Tool Documentation")
        
        # List all tools with index
        tool_list = []
        for category, tools in TOOL_REPOS.items():
            for tool_name in tools.keys():
                tool_list.append((category, tool_name))
                print(f"[{len(tool_list)}] {category.replace('_', ' ').title()} - {tool_name}")
        
        if not tool_list:
            print("[!] No tools available.")
            time.sleep(1)
            self.check_tool_status()
            return
        
        # Get user selection
        try:
            selection = int(input("\n[?] Enter tool number to view documentation (0 to cancel): "))
            if selection == 0:
                self.check_tool_status()
                return
            
            if 1 <= selection <= len(tool_list):
                category, tool_name = tool_list[selection - 1]
                tool_dir = os.path.join(TOOLS_DIR, category, tool_name)
                
                # Check if tool is installed
                if not os.path.exists(tool_dir):
                    print(f"\n[!] Tool {tool_name} is not installed. Installing...")
                    self.install_tool(category, tool_name)
                
                # Look for documentation files
                readme_files = []
                for file in os.listdir(tool_dir):
                    if file.lower().startswith('readme') or file.lower() == 'documentation' or file.lower() == 'docs':
                        readme_files.append(file)
                
                if readme_files:
                    self.view_readme_files(tool_dir, readme_files)
                else:
                    # If no documentation files found, try to fetch from GitHub
                    repo_url = TOOL_REPOS[category][tool_name]
                    print(f"\n[*] No documentation files found locally. Opening GitHub repository: {repo_url}")
                    
                    # Ask if user wants to open in browser
                    choice = input("\n[?] Open in web browser? (y/n): ")
                    if choice.lower() == 'y':
                        try:
                            webbrowser.open(repo_url)
                            print("[+] Repository opened in web browser.")
                        except Exception as e:
                            print(f"[!] Error opening web browser: {e}")
            else:
                print("\n[!] Invalid selection.")
        except ValueError:
            print("\n[!] Invalid input. Please enter a number.")
        
        time.sleep(1)
        self.check_tool_status()

def main():
    """Main function"""
    menu = ReconicMenu()
    menu.print_menu()

if __name__ == "__main__":
    main()
