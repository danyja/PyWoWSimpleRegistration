@echo off
setlocal enabledelayedexpansion

:: Set color
color 0A
title Python Environment Setup Tool

:: Force switch to script directory
set "script_dir=%~dp0"
cd /d "%script_dir%"
echo Current working directory: %cd%

:: Check Python installation
echo Checking Python installation...
for /f "tokens=*" %%a in ('where python 2^>nul') do (
    set "python_path=%%a"
)

if not defined python_path (
    echo.
    echo Error: Python installation not detected.
    echo Please download and install Python from https://www.python.org/downloads/
    echo and make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

:: Get Python version
for /f "tokens=*" %%v in ('"%python_path%" --version 2^>^&1') do (
    set "python_version=%%v"
)

:: Check if Python version >=3.10
echo Detected Python version: %python_version%
python -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)" && (
    echo Python version meets >= 3.10 requirement
) || (
    echo Error: Python >= 3.10 is required
    pause
    exit /b 1
)

:: Check if pip is available
echo Checking pip availability...
"%python_path%" -m pip --version > nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo Error: pip is not available
    echo Please ensure Python is installed correctly or try running: "%python_path%" -m ensurepip --upgrade
    echo.
    pause
    exit /b 1
)

:: Check venv module
echo Checking venv module...
"%python_path%" -c "import venv" 2>&1
if %errorlevel% neq 0 (
    echo.
    echo Error: venv module is not available
    echo Try to fix with: "%python_path%" -m ensurepip --upgrade
    echo Or reinstall Python and make sure all optional components are selected
    echo.
    pause
    exit /b 1
)

:: Create virtual environment
set "venv_dir=venv"
if exist "%venv_dir%" (
    echo [WARN] Virtual environment directory already exists
    choice /c YN /m "Do you want to recreate the virtual environment?"
    if /i !errorlevel! == 1 (
        echo Removing old virtual environment...
        rmdir /s /q "%venv_dir%"
        if exist "%venv_dir%" (
            echo.
            echo Error: Failed to delete virtual environment directory
            echo Please manually delete the %venv_dir% folder and try again
            echo.
            pause
            exit /b 1
        ) else (
            echo Successfully deleted
        )
    ) else (
        echo Using existing virtual environment
        goto activate_venv
    )
) else (
    echo Virtual environment directory doesn't exist, creating new one
)

echo Creating virtual environment...
"%python_path%" -m venv "%venv_dir%"
if %errorlevel% neq 0 (
    echo.
    echo Error: Failed to create virtual environment
    echo Possible reasons:
    echo 1. Insufficient permissions - try running as administrator
    echo 2. Antivirus blocking - temporarily disable antivirus
    echo 3. Corrupted Python installation - try repairing Python installation
    echo.
    pause
    exit /b 1
)

:activate_venv
:: Activate virtual environment and install dependencies
echo Activating virtual environment...
call "%venv_dir%\Scripts\activate.bat"
if %errorlevel% neq 0 (
    echo.
    echo Error: Failed to activate virtual environment
    echo Please check if %venv_dir%\Scripts\activate.bat exists
    echo.
    pause
    exit /b 1
)

:: Check if requirements.txt exists
if not exist "requirements.txt" (
    echo.
    echo Warning: requirements.txt file not found
    echo Skipping dependency installation step
    echo.
    goto success
)

echo Installing dependencies from requirements.txt...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo Error: Dependency installation failed
    echo Try running: %venv_dir%\Scripts\python.exe -m pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

:success
echo.
echo Environment setup completed!
echo Python path: %python_path%
echo Python version: %python_version%
echo Virtual environment created at: %cd%\%venv_dir%
echo Current working directory: %cd%

pause