@echo off
cd /d "%~dp0"
py -3 app.py
if errorlevel 1 (
  echo Install Python 3.10 or later, including the Python launcher, then try again.
  pause
)
