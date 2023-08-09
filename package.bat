@echo off

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed on your system. Installing Python...

    exit /b 1
)

python -m pip show tqdm >nul 2>&1
if %errorlevel% neq 0 (
    echo tqdm module is not installed. Installing tqdm...
    python -m pip install tqdm
    if %errorlevel% equ 0 (
        echo Installation of tqdm completed successfully!
    ) else (
        echo An error occurred while installing the tqdm module.
    )
) else (
    echo tqdm module is already installed.
)

echo All necessary components are installed.
echo You can now proceed with your tasks.

pause
