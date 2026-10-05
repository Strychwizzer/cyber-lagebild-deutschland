#!/bin/bash
# macOS/Linux: aktualisiert die Daten und oeffnet dann das Dashboard.
# Doppelklick (macOS) bzw. ausfuehren (Linux) statt index.html direkt oeffnen.
cd "$(dirname "$0")"
echo "============================================================"
echo "  Cyber-Lagebild Deutschland - wird gestartet"
echo "============================================================"
echo
echo "[1/2] Daten werden aktualisiert (benoetigt Internet)..."
python3 update_data.py || python update_data.py
echo
echo "[2/2] Dashboard wird im Browser geoeffnet..."
if command -v open >/dev/null 2>&1; then open index.html
elif command -v xdg-open >/dev/null 2>&1; then xdg-open index.html
else echo "Bitte index.html manuell im Browser oeffnen."; fi
