# Changelog

Alle nennenswerten Änderungen an diesem Projekt werden hier festgehalten.
Format angelehnt an [Keep a Changelog](https://keepachangelog.com/de/1.1.0/).
Datumsangaben im Format JJJJ-MM-TT (Zeitzone Europe/Berlin).

## [0.3.0] – 2026-10-21

### Hinzugefügt
- **Exploit-Verfügbarkeit (Exploit-DB):** CVEs mit öffentlichem Exploit-DB-Eintrag erhalten in der
  KEV- und der CERT-Bund-Tabelle eine rote **„Exploit"-Markierung** (Link zur Exploit-DB-Suche).
- **Filter „Mit Exploit"** im KEV-Bereich sowie ein Zähler in der Kopfzeile
  („X mit öffentlichem Exploit").
- **Sploitus-Lupe** je CVE für die manuelle Exploit-/PoC-Recherche.
- **Funktionsüberblick** im README (Tabelle „Bereich → Inhalt") und Changelog der Ergänzungen;
  Nahaufnahme-Screenshot der Exploit-/Sploitus-Markierung.
- Neue Datendatei `data_exploits.js` (speichert ausschließlich CVE-Kennungen, **kein** Exploit-Code);
  `update_data.py` baut sie als vierte Quelle aus der Exploit-DB-CSV.

### Hinweise
- Sploitus wird bewusst **nur als Nachschlage-Link** eingebunden, nicht als automatisches Ja/Nein:
  Sploitus aggregiert massenhaft auto-generierte PoC-Stubs (selbst erfundene CVEs liefern „Treffer"),
  wäre als Flag also irreführend. Die zuverlässige Markierung stammt aus der kuratierten Exploit-DB.

## [0.2.0] – 2026-10-05

### Hinzugefügt
- **Deutschlandkarte** in der Übersicht: Vorfälle werden geografisch als Marker verortet
  (Bundesländer-Umriss als Inline-SVG, Ortserkennung über ein Städte-/Bundesland-Verzeichnis).
  Markergröße = Anzahl Vorfälle am Ort; Klick filtert die Vorfalltabelle.
- **Ein-Klick-Starter** `Dashboard starten.bat` (Windows) und `dashboard-starten.command`
  (macOS/Linux): aktualisiert beim Start die Daten und öffnet dann das Dashboard.
- **Alters-Anzeige** in der Seitenleiste mit Hinweis bei veralteten Daten.

### Geändert
- **ransomware.live** wird jetzt über die offizielle **PRO-API** (optionaler Token) geladen, mit
  HTML-Länderseite als Fallback – die frühere kostenlose v2-API ist abgeschaltet. Der Token wird
  nur lokal gespeichert (`ransomware_token.txt`, per `.gitignore` ausgeschlossen).

### Behoben
- **KEV-Umschalter „Nur Ransomware / Alle KEV"** zeigte scheinbar keine Wirkung; die Tabelle wird
  nun nach Datum sortiert, sodass „Alle KEV" oben sofort andere Einträge zeigt.

## [0.1.0] – 2026-10-02

### Hinzugefügt
- Erste Version des lokalen Single-File-Dashboards (HTML/CSS/Vanilla-JS, Inline-SVG-Charts) im
  dunklen Design.
- **Übersicht** mit Kennzahlen und Diagrammen.
- **Sicherheitsvorfälle** (Quelle: security-incidents.de) als durchsuchbare Tabelle.
- **Schwachstellen (CERT-Bund)**: aktuelle BSI-/CVE-Meldungen.
- **Bedrohungsakteure**: aktivste Ransomware-Gruppen mit anklickbaren Profilen
  (MITRE ATT&CK, Werkzeuge, Schutz-Fazit) – Quellen ransomware.live und Security-Insider.
- **Aktiv ausgenutzt (CISA KEV)** mit Ransomware-Kennzeichnung.
- `update_data.py` zum Aktualisieren der Quellen; README mit Screenshots; MIT-Lizenz.

[0.3.0]: https://github.com/Strychwizzer/cyber-lagebild-deutschland/releases/tag/v0.3.0
[0.2.0]: https://github.com/Strychwizzer/cyber-lagebild-deutschland/releases/tag/v0.2.0
[0.1.0]: https://github.com/Strychwizzer/cyber-lagebild-deutschland/releases/tag/v0.1.0
