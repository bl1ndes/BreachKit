#!/bin/bash

# BreachKit One-Command Installer for Kali Linux
# This script clones the BreachKit repository and automatically installs it

echo "=====================================================
       BreachKit One-Command Installer for Kali Linux            
====================================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "[!] This script requires root privileges."
    echo "[*] Running with sudo..."
    sudo "$0" "$@"
    exit $?
fi

# Define installation directory
INSTALL_DIR="/opt/breachkit"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "[*] Git not found. Installing git..."
    apt update
    apt install -y git
fi

# Clone the repository
echo "[*] Cloning BreachKit repository to $INSTALL_DIR..."
if [ -d "$INSTALL_DIR" ]; then
    echo "[!] Directory $INSTALL_DIR already exists."
    read -p "[?] Do you want to remove it and continue? (y/n): " choice
    if [ "$choice" = "y" ] || [ "$choice" = "Y" ]; then
        rm -rf "$INSTALL_DIR"
    else
        echo "[!] Installation aborted."
        exit 1
    fi
fi

# Replace this URL with the actual BreachKit repository URL
git clone https://github.com/username/breachkit.git "$INSTALL_DIR"

if [ $? -ne 0 ]; then
    echo "[!] Failed to clone repository. Please check the URL and your internet connection."
    exit 1
fi

# Navigate to the Linux directory
cd "$INSTALL_DIR/Linux"

# Make the installation scripts executable
chmod +x install.sh auto_install.sh post-clone-setup.sh

# Run the auto_install.sh script directly
echo "[*] Running auto-installer..."
./auto_install.sh

# Create a symbolic link to make breachkit accessible from anywhere
if [ ! -f /usr/local/bin/breachkit ]; then
    ln -s "$INSTALL_DIR/breachkit.py" /usr/local/bin/breachkit
    chmod +x /usr/local/bin/breachkit
fi

echo "[+] BreachKit installation completed successfully!"
echo "[*] You can now run 'breachkit' from anywhere."
echo "[*] For help, run 'breachkit -h'"

exit 0
