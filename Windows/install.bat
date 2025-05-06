@echo off
echo =====================================================
echo             BreachKit Installer for Windows            
echo =====================================================

:: Check for administrator privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] This script requires administrator privileges.
    echo [!] Please run as administrator.
    pause
    exit /b 1
)

:: Set installation directory
set INSTALL_DIR=%ProgramFiles%\BreachKit
set PYTHON_PATH=python

:: Check if Python is installed
%PYTHON_PATH% --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] Python is not installed or not in PATH.
    echo [!] Please install Python 3.6+ and make sure it's in your PATH.
    pause
    exit /b 1
)

:: Create installation directory
echo [*] Creating installation directory...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
if not exist "%INSTALL_DIR%\tools" mkdir "%INSTALL_DIR%\tools"

:: Copy files
echo [*] Copying files...
xcopy /E /I /Y "..\*" "%INSTALL_DIR%"
rd /S /Q "%INSTALL_DIR%\Linux" >nul 2>&1

:: Install Python dependencies
echo [*] Installing Python dependencies...
%PYTHON_PATH% -m pip install -r requirements.txt

:: Check if Nmap is installed
where nmap >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] Nmap is not installed or not in PATH.
    echo [*] Attempting to install Nmap using Chocolatey...
    
    :: Check if Chocolatey is installed
    where choco >nul 2>&1
    if %errorLevel% neq 0 (
        echo [!] Chocolatey is not installed.
        echo [!] Please install Nmap manually from https://nmap.org/download.html
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

echo [+] Installation completed successfully!
echo [*] You can now run 'breachkit' from anywhere.
echo [*] For help, run 'breachkit -h'
echo [*] You can also find BreachKit in the Start Menu.
pause
