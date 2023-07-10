@echo off
cd /d "%~dp0"

REM Perform a Git pull to update the repository
git pull

REM Run the Python script
python main.py