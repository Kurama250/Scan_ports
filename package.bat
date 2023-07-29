@echo off

REM Vérifier si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed on your system.
    exit /b 1
)

REM Installer les modules Python
python -m pip install tqdm

if %errorlevel% equ 0 (
    echo Installation completed successfully !
) else (
    echo An error occurred while installing Python modules.
)
