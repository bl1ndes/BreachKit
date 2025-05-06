#!/bin/bash

# BreachKit Linux Post-Clone Setup
# This script automatically runs the auto-installer after cloning the repository

echo "=====================================================
             BreachKit Post-Clone Setup for Linux            
====================================================="

# Make the auto-installer executable
chmod +x auto_install.sh

# Automatically run the auto installer
echo "[*] Repository successfully cloned!"

echo "[*] Running auto-installer..."
./auto_install.sh

# Add a Git post-merge hook to suggest running the auto-installer after pulls
if [ -d ".git" ]; then
    echo "[*] Setting up Git hooks..."
    
    mkdir -p .git/hooks
    
    cat > .git/hooks/post-merge << 'EOF'
#!/bin/bash
echo "[*] Repository updated!"
echo "[*] If there were significant changes, you might want to run the auto-installer:"
echo "    ./auto_install.sh"
EOF
    
    chmod +x .git/hooks/post-merge
    echo "[+] Git hooks configured"
fi

exit 0
