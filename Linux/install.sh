#!/bin/bash

# BreachKit Installation Script for Kali Linux
echo "====================================================="
echo "         BreachKit Installer for Kali Linux            "
echo "====================================================="

# Check if running as root
if [ "$(id -u)" -ne 0 ]; then
    echo "[!] This script must be run as root. Please use sudo."
    exit 1
fi

# Set installation directory
INSTALL_DIR="/opt/breachkit"
BIN_DIR="/usr/local/bin"

# Create directories
echo "[*] Creating installation directories..."
mkdir -p $INSTALL_DIR
mkdir -p $BIN_DIR

# Copy files
echo "[*] Copying files..."
cp -r ../* $INSTALL_DIR/
rm -rf $INSTALL_DIR/Windows  # Remove Windows-specific files

# Install Python dependencies
echo "[*] Installing Python dependencies..."
pip3 install -r requirements.txt

# Install Kali Linux specific dependencies
echo "[*] Installing Kali Linux dependencies..."
apt-get update
apt-get install -y nmap gobuster python3-dev python3-pip libssl-dev libffi-dev build-essential

# Create executable in /usr/local/bin
echo "[*] Creating executable..."
echo '#!/bin/bash
if [ "$1" == "" ]; then
    python3 -m breachkit.cli
else
    python3 -m breachkit.main "$@"
fi' > /usr/local/bin/breachkit
chmod +x /usr/local/bin/breachkit

echo "[+] Installation completed successfully!"
echo "[*] You can now run 'breachkit' from anywhere."
echo "[*] For help, run 'breachkit -h'"
