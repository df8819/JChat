@echo off
cd /d "%~dp0"

REM Perform a Git pull to update the repository
git pull

REM Install dependencies from requirements.txt using pip
pip install -r requirements.txt

REM Function to rename the file
:RENAME_FILE
IF EXIST temp.apikey.json (
  ren temp.apikey.json apikey.json
)

REM Run the Python script
python main.py