@echo off
echo =====================================================
echo             BreachKit Auto-Installer for Windows            
echo =====================================================

:: Check for administrator privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] This script requires administrator privileges.
    echo [!] Attempting to restart with administrator privileges...
    
    :: Restart script with admin privileges
    powershell -Command "Start-Process -FilePath '%0' -Verb RunAs"
    exit /b
)

:: Set installation directory
set INSTALL_DIR=%ProgramFiles%\BreachKit
set PYTHON_PATH=python

echo [*] Starting BreachKit installation...

:: Check if Python is installed
%PYTHON_PATH% --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] Python is not installed or not in PATH.
    
    :: Ask if user wants to install Python
    set /p INSTALL_PYTHON="[?] Would you like to install Python now? (y/n): "
    if /i "%INSTALL_PYTHON%"=="y" (
        echo [*] Downloading Python installer...
        powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.10.8/python-3.10.8-amd64.exe' -OutFile 'python-installer.exe'"
        
        echo [*] Installing Python...
        python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
        del python-installer.exe
        
        echo [*] Python installation completed.
        echo [*] Please restart this script after installation.
        pause
        exit /b
    ) else (
        echo [!] Please install Python 3.6+ and make sure it's in your PATH.
        echo [!] Then run this script again.
        pause
        exit /b 1
    )
)

:: Create installation directory
echo [*] Creating installation directory...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
if not exist "%INSTALL_DIR%\tools" mkdir "%INSTALL_DIR%\tools"

:: Copy files to installation directory
echo [*] Copying files...
xcopy /E /I /Y ".\" "%INSTALL_DIR%"

:: Install Python dependencies
echo [*] Installing Python dependencies...
%PYTHON_PATH% -m pip install -r requirements.txt

:: Check if Nmap is installed
where nmap >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] Nmap is not installed or not in PATH.
    
    :: Check if Chocolatey is installed
    where choco >nul 2>&1
    if %errorLevel% neq 0 (
        echo [!] Chocolatey is not installed.
        
        :: Ask if user wants to install Chocolatey
        set /p INSTALL_CHOCO="[?] Would you like to install Chocolatey now? (y/n): "
        if /i "%INSTALL_CHOCO%"=="y" (
            echo [*] Installing Chocolatey...
            powershell -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
            
            echo [*] Installing Nmap using Chocolatey...
            choco install nmap -y
        ) else (
            echo [!] Please install Nmap manually from https://nmap.org/download.html
        )
    ) else (
        echo [*] Installing Nmap using Chocolatey...
        choco install nmap -y
    )
)

:: Create a shortcut in the Start Menu
echo [*] Creating Start Menu shortcut...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%ProgramData%\Microsoft\Windows\Start Menu\Programs\BreachKit.lnk'); $Shortcut.TargetPath = '%PYTHON_PATH%'; $Shortcut.Arguments = '-m breachkit.cli'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'BreachKit Security Toolkit'; $Shortcut.Save()"

:: Create a batch file to run Reconic
echo [*] Creating executable batch file...
echo @echo off > "%INSTALL_DIR%\breachkit.bat"
echo cd /d "%INSTALL_DIR%" >> "%INSTALL_DIR%\breachkit.bat"
echo if "%%1"=="" ( >> "%INSTALL_DIR%\breachkit.bat"
echo     %PYTHON_PATH% -m breachkit.cli >> "%INSTALL_DIR%\breachkit.bat"
echo ) else ( >> "%INSTALL_DIR%\breachkit.bat"
echo     %PYTHON_PATH% -m breachkit.main %%* >> "%INSTALL_DIR%\breachkit.bat"
echo ) >> "%INSTALL_DIR%\breachkit.bat"

:: Add to PATH
echo [*] Adding Reconic to PATH...
setx PATH "%PATH%;%INSTALL_DIR%" /M

:: Ask if user wants to create a desktop shortcut
set /p CREATE_DESKTOP="[?] Would you like to create a desktop shortcut? (y/n): "
if /i "%CREATE_DESKTOP%"=="y" (
    echo [*] Creating desktop shortcut...
    powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut([System.Environment]::GetFolderPath('Desktop') + '\BreachKit.lnk'); $Shortcut.TargetPath = '%PYTHON_PATH%'; $Shortcut.Arguments = '-m breachkit.cli'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'BreachKit Security Toolkit'; $Shortcut.Save()"
)

echo [+] Installation completed successfully!
echo [*] You can now run 'breachkit' from anywhere.
echo [*] For help, run 'breachkit -h'
echo [*] You can also find BreachKit in the Start Menu.

:: Ask if user wants to run Reconic now
set /p RUN_NOW="[?] Would you like to run BreachKit now? (y/n): "
if /i "%RUN_NOW%"=="y" (
    "%INSTALL_DIR%\breachkit.bat"
)

pause
