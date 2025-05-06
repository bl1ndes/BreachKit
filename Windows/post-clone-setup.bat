@echo off
echo =====================================================
echo             BreachKit Post-Clone Setup for Windows            
echo =====================================================

:: Check if running in a Git repository
if not exist ".git" (
    echo [*] Repository successfully cloned!
) else (
    echo [*] Repository detected!
)

:: Ask user if they want to run the auto-installer now
set /p RUN_NOW="[?] Would you like to run the auto-installer now? (y/n): "
if /i "%RUN_NOW%"=="y" (
    echo [*] Running auto-installer...
    call auto_install.bat
) else (
    echo [*] You can run the auto-installer later with:
    echo     auto_install.bat
)

:: Set up Git hooks if in a Git repository
if exist ".git" (
    echo [*] Setting up Git hooks...
    
    if not exist ".git\hooks" mkdir ".git\hooks"
    
    echo @echo off > ".git\hooks\post-merge.bat"
    echo echo [*] Repository updated! >> ".git\hooks\post-merge.bat"
    echo echo [*] If there were significant changes, you might want to run the auto-installer: >> ".git\hooks\post-merge.bat"
    echo echo     auto_install.bat >> ".git\hooks\post-merge.bat"
    
    echo [+] Git hooks configured
)

pause
