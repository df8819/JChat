@echo off
cd /d "%~dp0"

REM Function to rename the file
:RENAME_FILE
IF EXIST temp.apikey.json (
  ren temp.apikey.json apikey.json
)

REM Run the Python script
python main.py