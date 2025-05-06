#!/bin/bash

# BreachKit Linux Auto-Installer
# This script automatically runs after cloning the repository

echo "=====================================================
             BreachKit Auto-Installer for Linux            
====================================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "[!] This script requires root privileges."
    echo "[*] Running with sudo..."
    sudo "$0" "$@"
    exit $?
fi

# Function to detect Linux distribution
detect_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        DISTRO=$ID
        VERSION=$VERSION_ID
    elif type lsb_release >/dev/null 2>&1; then
        DISTRO=$(lsb_release -si)
        VERSION=$(lsb_release -sr)
    elif [ -f /etc/lsb-release ]; then
        . /etc/lsb-release
        DISTRO=$DISTRIB_ID
        VERSION=$DISTRIB_RELEASE
    elif [ -f /etc/debian_version ]; then
        DISTRO="debian"
        VERSION=$(cat /etc/debian_version)
    else
        DISTRO=$(uname -s)
        VERSION=$(uname -r)
    fi
    
    DISTRO=$(echo "$DISTRO" | tr '[:upper:]' '[:lower:]')
    echo "[*] Detected distribution: $DISTRO $VERSION"
}

# Function to install dependencies based on distribution
install_dependencies() {
    echo "[*] Installing dependencies..."
    
    case $DISTRO in
        "kali" | "debian" | "ubuntu" | "linuxmint" | "pop")
            apt update
            apt install -y git python3 python3-pip python3-dev nmap gobuster libssl-dev libffi-dev build-essential curl wget whois dnsutils
            ;;
        "fedora" | "centos" | "rhel")
            dnf update -y
            dnf install -y git python3 python3-pip python3-devel nmap openssl-devel libffi-devel gcc gcc-c++ make curl wget whois bind-utils
            ;;
        "arch" | "manjaro")
            pacman -Syu --noconfirm
            pacman -S --noconfirm git python python-pip nmap openssl libffi gcc make curl wget whois bind-tools
            ;;
        *)
            echo "[!] Unsupported distribution: $DISTRO"
            echo "[*] Please install the following packages manually:"
            echo "    - git, python3, python3-pip, nmap, gobuster, libssl-dev, libffi-dev, build-essential"
            ;;
    esac
}

# Function to install Python dependencies
install_python_deps() {
    echo "[*] Installing Python dependencies..."
    pip3 install -r requirements.txt
}

# Function to create executable
create_executable() {
    echo "[*] Creating executable..."
    
    # Create executable script
    cat > /usr/local/bin/breachkit << 'EOF'
#!/bin/bash
if [ "$1" == "" ]; then
    python3 -m breachkit.cli
else
    python3 -m breachkit.main "$@"
fi
EOF
    
    # Make it executable
    chmod +x /usr/local/bin/breachkit
    
    echo "[+] Executable created at /usr/local/bin/breachkit"
}

# Function to set up auto-start on login (optional)
setup_autostart() {
    read -p "[?] Would you like BreachKit to start automatically at login? (y/n): " choice
    if [ "$choice" = "y" ] || [ "$choice" = "Y" ]; then
        echo "[*] Setting up autostart..."
        
        # Create desktop file
        mkdir -p /etc/xdg/autostart/
        cat > /etc/xdg/autostart/breachkit.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=BreachKit
Comment=BreachKit Security Toolkit
Exec=breachkit
Terminal=true
Categories=Security;
EOF
        
        echo "[+] Autostart configured"
    fi
}

# Main installation process
main() {
    echo "[*] Starting BreachKit installation..."
    
    # Detect distribution
    detect_distro
    
    # Install system dependencies
    install_dependencies
    
    # Install Python dependencies
    install_python_deps
    
    # Create executable
    create_executable
    
    # Setup autostart (optional)
    setup_autostart
    
    echo "[+] Installation completed successfully!"
    echo "[*] You can now run 'breachkit' from anywhere."
    echo "[*] For help, run 'breachkit -h'"
    echo ""
    
    # Ask if user wants to run BreachKit now
    read -p "[?] Would you like to run BreachKit now? (y/n): " choice
    if [ "$choice" = "y" ] || [ "$choice" = "Y" ]; then
        breachkit
    fi
}

# Execute main function
main

exit 0
