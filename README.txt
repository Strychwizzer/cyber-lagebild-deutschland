Cyber-Lagebild Deutschland – lokale Demo
=========================================

Öffnen:      index.html per Doppelklick im Browser öffnen (Chrome/Edge/Firefox).
Aktualisieren: aktualisieren.bat doppelklicken (Windows) oder
             python3 update_data.py ausführen (macOS/Linux), danach F5 im Browser.
             Benötigt Python 3 (ohne Zusatzpakete) und Internetzugang.

Dateien
  index.html          Dashboard
  data.js             Vorfälle & CERT-Bund-Schwachstellen (Update-Skript überschreibt)
  data_ransomware.js  Ransomware-Opfer & Gruppen-Statistik (Update-Skript überschreibt)
  data_actors.js      Profile der Ransomware-Gruppen (Beschreibung, TTPs, Tools) – von Hand gepflegt
  data_knowledge.js   Erklärungen der Angriffsmethoden & Gruppen-Einordnung – von Hand gepflegt
  data_secinsider.js  Chronik benannter Fälle (Security-Insider) – von Hand gepflegt
  data_kev.js         Aktiv ausgenutzte Lücken / CISA KEV (Update-Skript überschreibt)
  update_data.py      Lädt security-incidents.de, CERT-Bund, ransomware.live und CISA KEV
  aktualisieren.bat   Windows-Starter für das Update

Quellen
  - security-incidents.de  (Sicherheitsvorfälle, benannte Betroffene)
  - BSI CERT-Bund WID       (aktuelle Schwachstellen / CVEs)
  - ransomware.live         (Ransomware-Gruppen, Opfer, Angriffsmethoden/TTPs)
  - Security-Insider        (redaktionelle Chronik 2026)
  - CISA KEV                (aktiv ausgenutzte Lücken, Ransomware-Kennzeichnung)
  - MITRE ATT&CK            (Erklärung der Angriffsmethoden)

Bedrohungsakteure
  Die Sektion "Bedrohungsakteure" zeigt die aktivsten Ransomware-Gruppen gegen
  deutsche Ziele. Klick auf eine Karte öffnet ein Profil mit Vorgehen
  (MITRE ATT&CK, aufklappbar je Phase), eingesetzten Werkzeugen, bevorzugten
  Branchen, Zielländern, Schutzmaßnahmen und den zuletzt betroffenen DE-Firmen.
  Hinweis: Die freie ransomware.live-API liefert zeitweise keine Daten; dann
  bleibt der mitgelieferte Schnappschuss (data_ransomware.js) erhalten.

Tipps für Kundentermine
  - "Präsentieren" (oben rechts): Vollbild ohne Seitenleiste, ESC beendet.
  - "Namen ausblenden" (Seitenleiste): verwischt Betroffenennamen, falls nötig.
  - Strg+K: Schnellsuche über Vorfälle und Schwachstellen (z. B. eine Branche oder ein Produkt des Kunden).
  - Klick auf einen Vorfall öffnet Details mit Link zur Quelle; Klick auf eine Schwachstelle öffnet die BSI-Meldung.

Hinweis: Die Datenbank enthält nur öffentlich bekannt gewordene Fälle. Viele kleinere
Betroffene sind dort bereits anonymisiert (z. B. "IT-Dienstleister").
Die Daten stammen von Drittanbietern – bitte Quellen bei Präsentationen nennen.
