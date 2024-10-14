@echo off
SETLOCAL

:: Define variables
set REPO_URL=https://github.com/Snowythevulpix/Re-Tanpopo/archive/refs/heads/master.zip
set REPO_NAME=Re-Tanpopo
set ZIP_FILE=%CD%\%REPO_NAME%.zip
set EXTRACTED_FOLDER=%CD%\%REPO_NAME%-master

:: Check for Python installation
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo You haven't got Python installed or it isn't correctly added to your PATH.
    echo Here’s a guide on how to install it and add it to the PATH:
    echo https://python.org
    echo https://realpython.com/add-python-to-path/
    pause
    exit /b
) ELSE (
    echo Python is already installed.
)

:: Check for PowerShell installation
powershell -command "exit" >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo PowerShell is not installed. Please install PowerShell first.
    pause
    exit /b
) ELSE (
    echo PowerShell is already installed.
)

:: Download the repository as a ZIP file
echo Downloading repository...
powershell -command "Invoke-WebRequest -Uri '%REPO_URL%' -OutFile '%ZIP_FILE%'"

:: Check if the download was successful
IF NOT EXIST "%ZIP_FILE%" (
    echo Failed to download the repository. Please check the URL and try again.
    pause
    exit /b
)

:: Unzip the downloaded ZIP file
echo Unzipping the repository...
powershell -command "Expand-Archive -Path '%ZIP_FILE%' -DestinationPath '%CD%' -Force"

:: Check if unzipping was successful
IF NOT EXIST "%EXTRACTED_FOLDER%" (
    echo Failed to unzip the repository. Please check the downloaded file.
    pause
    exit /b
)

:: Change to the repository directory
cd "%EXTRACTED_FOLDER%"

:: Check if requirements.txt exists and install packages
IF EXIST requirements.txt (
    echo Installing required packages from requirements.txt...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
) ELSE (
    echo No requirements.txt found. Skipping package installation.
)

:: Clean up the ZIP file
del "%ZIP_FILE%"

:: Return to the original directory
cd ..

echo Installation complete.
pause
