@echo off
chcp 65001 >nul
cd /d "%~dp0"
REM Aktualisiert zuerst die Daten und oeffnet dann das Dashboard im Standardbrowser.
REM Doppelklick auf diese Datei statt auf index.html -> bei jedem Start frische Daten.

set PY=python
where python >nul 2>&1 || set PY=py

echo ============================================================
echo   Cyber-Lagebild Deutschland - wird gestartet
echo ============================================================
echo.
echo [1/2] Daten werden aktualisiert (benoetigt Internet, dauert kurz)...
%PY% update_data.py
echo.
echo [2/2] Dashboard wird im Browser geoeffnet...
start "" "index.html"
echo.
echo Fertig. Dieses Fenster kann geschlossen werden.
timeout /t 4 >nul
