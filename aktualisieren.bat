@echo off
REM Aktualisiert die Daten des Cyber-Lagebild-Dashboards (benoetigt Python 3)
cd /d "%~dp0"
python update_data.py || py update_data.py
pause
