#!/usr/bin/env python3

import os
import sys
import platform
import subprocess
import ctypes
import winreg

def is_admin():
    """Check if the script is running with administrator privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def run_as_admin():
    """Restart the script with administrator privileges"""
    if not is_admin():
        print("[!] This operation requires administrator privileges.")
        print("[*] Attempting to restart with administrator privileges...")
        
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
            sys.exit(0)
        except:
            print("[!] Failed to restart with administrator privileges.")
            print("[!] Please run the script as administrator manually.")
            sys.exit(1)

def check_windows_dependencies():
    """Check if required Windows dependencies are installed"""
    dependencies = {
        "Python": False,
        "Nmap": False,
        "Git": False
    }
    
    # Check Python
    try:
        python_version = platform.python_version()
        if python_version:
            dependencies["Python"] = True
            print(f"[+] Python {python_version} is installed")
    except:
        print("[!] Python check failed")
    
    # Check Nmap
    try:
        result = subprocess.run(["nmap", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            dependencies["Nmap"] = True
            nmap_version = result.stdout.split('\n')[0]
            print(f"[+] {nmap_version}")
    except:
        print("[!] Nmap is not installed or not in PATH")
    
    # Check Git
    try:
        result = subprocess.run(["git", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            dependencies["Git"] = True
            git_version = result.stdout.strip()
            print(f"[+] {git_version}")
    except:
        print("[!] Git is not installed or not in PATH")
    
    return dependencies

def install_dependency(dependency):
    """Attempt to install a dependency using various methods"""
    if dependency == "Nmap":
        # Try using chocolatey
        try:
            print("[*] Attempting to install Nmap using Chocolatey...")
            subprocess.run(["choco", "install", "nmap", "-y"], check=True)
            return True
        except:
            print("[!] Failed to install Nmap using Chocolatey")
            print("[*] Please install Nmap manually from https://nmap.org/download.html")
            return False
    
    elif dependency == "Git":
        # Try using chocolatey
        try:
            print("[*] Attempting to install Git using Chocolatey...")
            subprocess.run(["choco", "install", "git", "-y"], check=True)
            return True
        except:
            print("[!] Failed to install Git using Chocolatey")
            print("[*] Please install Git manually from https://git-scm.com/download/win")
            return False
    
    return False

def add_to_path(path):
    """Add a directory to the Windows PATH environment variable"""
    if not os.path.exists(path):
        print(f"[!] Path does not exist: {path}")
        return False
    
    try:
        # Open the registry key
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Environment",
            0,
            winreg.KEY_READ | winreg.KEY_WRITE
        )
        
        # Get the current PATH value
        current_path, _ = winreg.QueryValueEx(key, "PATH")
        
        # Check if the path is already in PATH
        if path.lower() in current_path.lower():
            print(f"[*] {path} is already in PATH")
            return True
        
        # Add the path to PATH
        new_path = current_path + ";" + path
        winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path)
        winreg.CloseKey(key)
        
        # Notify the system about the change
        subprocess.run(["setx", "PATH", new_path], check=True)
        
        print(f"[+] Added {path} to PATH")
        return True
    except Exception as e:
        print(f"[!] Failed to add to PATH: {e}")
        return False

def create_shortcut(target_path, shortcut_path, working_directory=None, description=None):
    """Create a Windows shortcut"""
    try:
        import win32com.client
        
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.TargetPath = target_path
        
        if working_directory:
            shortcut.WorkingDirectory = working_directory
        
        if description:
            shortcut.Description = description
        
        shortcut.Save()
        print(f"[+] Created shortcut: {shortcut_path}")
        return True
    except Exception as e:
        print(f"[!] Failed to create shortcut: {e}")
        return False

def windows_tool_adapter(tool_name, tool_dir, args=None):
    """Adapt tool execution for Windows environment"""
    # Map of special handling for specific tools
    tool_handlers = {
        "nmap": run_nmap,
        "sqlmap": run_sqlmap,
        "gobuster": run_gobuster,
    }
    
    # Check if tool has a special handler
    if tool_name in tool_handlers:
        return tool_handlers[tool_name](tool_dir, args)
    
    # Default handling
    return False

def run_nmap(tool_dir, args):
    """Run Nmap with appropriate Windows settings"""
    try:
        # Check if Nmap is in PATH
        result = subprocess.run(["where", "nmap"], capture_output=True, text=True)
        if result.returncode == 0:
            nmap_path = result.stdout.strip().split('\n')[0]
            print(f"[*] Using Nmap from: {nmap_path}")
            
            # Run Nmap with the provided arguments
            command = f"nmap {args}" if args else "nmap -h"
            print(f"[*] Running: {command}")
            
            # Use subprocess.Popen to keep the console window open
            process = subprocess.Popen(command, shell=True)
            process.wait()
            return True
        else:
            print("[!] Nmap is not installed or not in PATH")
            choice = input("[?] Do you want to install Nmap? (y/n): ")
            if choice.lower() == 'y':
                if install_dependency("Nmap"):
                    return run_nmap(tool_dir, args)
            return False
    except Exception as e:
        print(f"[!] Error running Nmap: {e}")
        return False

def run_sqlmap(tool_dir, args):
    """Run SQLMap with Windows-specific adaptations"""
    try:
        # Check if Python is available
        python_path = sys.executable
        
        # Look for SQLMap main script
        sqlmap_script = os.path.join(tool_dir, "sqlmap.py")
        if not os.path.exists(sqlmap_script):
            print(f"[!] SQLMap script not found: {sqlmap_script}")
            return False
        
        # Run SQLMap with the provided arguments
        command = f'"{python_path}" "{sqlmap_script}" {args}' if args else f'"{python_path}" "{sqlmap_script}" --help'
        print(f"[*] Running: {command}")
        
        # Use subprocess.Popen to keep the console window open
        process = subprocess.Popen(command, shell=True, cwd=tool_dir)
        process.wait()
        return True
    except Exception as e:
        print(f"[!] Error running SQLMap: {e}")
        return False

def run_gobuster(tool_dir, args):
    """Run a Python-based alternative to Gobuster for Windows"""
    try:
        # Since Gobuster might not work well on Windows, use a Python alternative
        print("[*] Using Python-based directory scanner for Windows")
        
        # Parse arguments to extract target and wordlist
        target = None
        wordlist = None
        
        if args:
            args_parts = args.split()
            for i, part in enumerate(args_parts):
                if part == "-u" and i+1 < len(args_parts):
                    target = args_parts[i+1]
                elif part == "-w" and i+1 < len(args_parts):
                    wordlist = args_parts[i+1]
        
        if not target:
            target = input("[?] Enter target URL: ")
        
        if not wordlist:
            wordlist = input("[?] Enter wordlist path: ")
        
        if not os.path.exists(wordlist):
            print(f"[!] Wordlist not found: {wordlist}")
            return False
        
        # Run a simple Python-based directory scanner
        print(f"[*] Scanning directories on {target} using {wordlist}")
        
        import requests
        from urllib.parse import urljoin
        
        with open(wordlist, 'r') as f:
            directories = [line.strip() for line in f if line.strip()]
        
        for directory in directories:
            url = urljoin(target, directory)
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    print(f"[+] Found: {url} (Status: {response.status_code})")
                elif response.status_code != 404:
                    print(f"[*] Potential: {url} (Status: {response.status_code})")
            except Exception as e:
                print(f"[!] Error scanning {url}: {e}")
        
        return True
    except Exception as e:
        print(f"[!] Error running directory scanner: {e}")
        return False

if __name__ == "__main__":
    print("Reconic Windows Adapter")
    print("This module is not meant to be run directly.")
    print("It provides Windows-specific functionality for Reconic.")
    
    # If run directly, show dependency status
    print("\nChecking Windows dependencies:")
    dependencies = check_windows_dependencies()
    
    missing = [dep for dep, installed in dependencies.items() if not installed]
    if missing:
        print(f"\n[!] Missing dependencies: {', '.join(missing)}")
        print("[*] Please install these dependencies to ensure Reconic works properly.")
    else:
        print("\n[+] All dependencies are installed.")
