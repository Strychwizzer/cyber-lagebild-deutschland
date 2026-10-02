/* Wissensbasis für das Dashboard (statisch, von Hand ergänzbar).
   Gruppenprofile: zusammengefasst/übersetzt nach ransomware.live (Gruppenseiten, Stand 02.10.2026).
   Taktik-Kategorien: öffentliches MITRE ATT&CK Framework (Taktik-Ebene).
   Die Beschreibungen sind bewusst auf Awareness- und Schutz-Ebene gehalten (Erkennung & Gegenmaßnahmen),
   nicht als Angriffsanleitung. Quelle der Gruppen-Gegenmaßnahmen: BSI/MITRE-Empfehlungen, allgemein. */

/* MITRE ATT&CK Taktiken (die Phasen eines Angriffs) – für die Erklärung im Actor-Profil.
   [engl. Phase, deutscher Name, was in dieser Phase passiert, typische Schutzrichtung] */
window.TACTICS = [
  ["Initial Access","Erstzugriff","Der erste Fuß in der Tür – meist über gestohlene Zugangsdaten, Phishing oder ungepatchte, aus dem Internet erreichbare Systeme.","MFA überall, externe Systeme zeitnah patchen, Angriffsfläche reduzieren, Awareness."],
  ["Execution","Ausführung","Schadcode wird auf einem System gestartet.","Anwendungs-Kontrolle, Makros blockieren, EDR."],
  ["Persistence","Persistenz","Die Angreifer sorgen dafür, dauerhaft im Netz zu bleiben – auch nach Neustarts oder Passwortwechseln.","Neu angelegte Konten/Dienste überwachen, Least Privilege."],
  ["Privilege Escalation","Rechteausweitung","Aus einem einfachen Zugang werden Administrator- oder Domänenrechte.","Patch-Management, Härtung, Tiered Admin, Monitoring privilegierter Konten."],
  ["Defense Evasion","Umgehung der Abwehr","Virenschutz, EDR und Protokolle werden ausgehebelt oder gelöscht, um unentdeckt zu bleiben.","Manipulationsschutz für EDR, zentrale & manipulationssichere Logs."],
  ["Credential Access","Zugangsdaten-Diebstahl","Passwörter und Anmelde-Tickets werden abgegriffen, um sich weiter auszubreiten.","LSASS-Schutz, lange Passwörter, MFA, keine Klartext-Passwörter."],
  ["Discovery","Erkundung","Netzwerk, Server, Nutzer und vor allem Backups werden ausgespäht.","Netzsegmentierung, Honeypots/Canaries, anomaliebasiertes Monitoring."],
  ["Lateral Movement","Seitliche Ausbreitung","Die Angreifer springen von System zu System in Richtung der wichtigen Server.","Segmentierung, RDP/SMB einschränken, Tiering."],
  ["Exfiltration","Datenabfluss","Daten werden als Druckmittel aus dem Unternehmen kopiert (Double Extortion).","Ausgehenden Verkehr überwachen (Cloud-Uploads, ungewöhnliche Mengen), DLP."],
  ["Command and Control","Fernsteuerung (C2)","Kompromittierte Systeme werden über das Internet ferngesteuert.","Proxy/Egress-Filter, bekannte C2-/Tunnel-Tools erkennen."],
  ["Impact","Schaden","Verschlüsselung, Löschen der Backups, Betriebsunterbrechung – der eigentliche Erpressungshebel.","Offline-/Immutable-Backups, getesteter Wiederanlauf, Notfallplan."]
];

/* Kurzerklärung je Technik-Grundname (auf Erkennung/Schutz ausgerichtet, nach MITRE ATT&CK).
   key = Anfang des Technik-Namens aus den Gruppen-Daten. */
window.TECH_NOTES = {
  "Valid Accounts":"Anmeldung mit echten, zuvor gestohlenen Zugangsdaten – fällt kaum auf. Schutz: MFA, Abgleich mit Leak-Datenbanken, Anomalie-Erkennung bei Logins.",
  "Exploit Public-Facing Application":"Ausnutzen bekannter Lücken in VPN, Firewall, Mail- oder Webservern. Schutz: externe Systeme priorisiert patchen, CERT-Warnungen verfolgen.",
  "External Remote Services":"Nutzung offener Fernzugänge (RDP, VPN, Citrix). Schutz: kein RDP ins Internet, VPN nur mit MFA.",
  "Phishing":"Präparierte E-Mails mit Link/Anhang. Schutz: Awareness, E-Mail-Sandbox, phishing-resistente MFA (FIDO2).",
  "Drive-by Compromise":"Infektion über manipulierte Webseiten / gefälschte Updates. Schutz: Browser aktuell halten, Web-Filter.",
  "Windows Management Instrumentation":"Missbrauch bordeigener Windows-Verwaltung. Schutz: WMI-Aktivität überwachen, Scripting einschränken.",
  "Command and Scripting Interpreter":"Missbrauch von PowerShell / Eingabeaufforderung. Schutz: PowerShell-Logging & Constrained Language Mode, Application Control.",
  "Scheduled Task":"Geplante Aufgaben als Startmechanismus. Schutz: neu angelegte Tasks überwachen.",
  "Create Account":"Anlegen eigener Konten, um Zugriff zu behalten. Schutz: Alarm bei neuen (Admin-)Konten.",
  "Account Manipulation":"Verändern bestehender Konten/Rechte. Schutz: Änderungen an privilegierten Gruppen überwachen.",
  "Boot or Logon Autostart":"Automatischer Start beim Hochfahren/Anmelden. Schutz: Autostart-Einträge prüfen.",
  "Access Token Manipulation":"Übernahme von Rechte-Token anderer Prozesse. Schutz: EDR, Härtung.",
  "Exploitation for Privilege Escalation":"Ausnutzen lokaler Schwachstellen für höhere Rechte. Schutz: zügiges Patchen auch intern.",
  "Rootkit":"Tiefes Verstecken im System. Schutz: Secure Boot, EDR mit Kernel-Schutz.",
  "Obfuscated Files or Information":"Verschleierter/gepackter Schadcode gegen Erkennung. Schutz: verhaltensbasiertes EDR statt nur Signaturen.",
  "Impair Defenses":"Abschalten von Virenschutz/EDR/Logs. Schutz: Manipulationsschutz, Alarm bei deaktivierten Schutzdiensten.",
  "Indicator Removal":"Löschen von Spuren und Ereignisprotokollen. Schutz: Logs sofort zentral & unveränderbar sichern.",
  "Masquerading":"Tarnen als legitime Datei/Prozess. Schutz: Application Control, Signaturprüfung.",
  "Modify Registry":"Ändern der Windows-Registry zur Tarnung/Persistenz. Schutz: kritische Schlüssel überwachen.",
  "OS Credential Dumping":"Abgreifen von Passwörtern aus dem Arbeitsspeicher (z. B. LSASS). Schutz: Credential Guard, LSASS-Schutz.",
  "Input Capture":"Mitschneiden von Tastatureingaben. Schutz: EDR, Härtung der Endpunkte.",
  "Brute Force":"Automatisiertes Durchprobieren von Passwörtern. Schutz: lange Passphrasen, Sperren, MFA.",
  "Credentials from Password Stores":"Auslesen gespeicherter Passwörter (Browser, Tools). Schutz: Passwort-Manager absichern, keine Klartext-Ablage.",
  "Credentials from Web Browsers":"Passwörter aus Browsern abgreifen. Schutz: Browser-Passwortspeicher einschränken.",
  "Network Service Discovery":"Scannen des Netzwerks nach Diensten. Schutz: Segmentierung, IDS, Canary-Hosts.",
  "Remote System Discovery":"Auffinden weiterer Systeme. Schutz: Netzwerk-Monitoring.",
  "System Information Discovery":"Ausspähen von Systeminfos. Schutz: Anomalie-Erkennung.",
  "Domain Trust Discovery":"Erkunden der AD-Struktur. Schutz: AD-Tiering, Monitoring von Enumerations-Tools.",
  "Remote Services":"Seitliche Bewegung über RDP/SMB/SSH. Schutz: interne Segmentierung, RDP einschränken.",
  "Lateral Tool Transfer":"Kopieren von Werkzeugen auf andere Systeme. Schutz: Application Control, SMB-Überwachung.",
  "Data from Local System":"Sammeln lokaler Daten vor dem Abzug. Schutz: DLP, Zugriffskontrolle.",
  "Archive Collected Data":"Packen der Daten (oft 7-Zip/WinRAR) vor dem Abfluss. Schutz: ungewöhnliche Archiv-Erstellung erkennen.",
  "Data Staged":"Zwischenlagern der Daten. Schutz: Monitoring großer Datenbewegungen.",
  "Exfiltration Over C2 Channel":"Datenabzug über denselben Kanal wie die Fernsteuerung. Schutz: Egress-Filter, Verkehrsanalyse.",
  "Exfiltration Over Alternative Protocol":"Datenabzug über andere Protokolle. Schutz: ausgehenden Verkehr beschränken.",
  "Exfiltration Over Web Service":"Hochladen zu Cloud-Diensten (z. B. MEGA). Schutz: Cloud-Uploads kontrollieren/blocken.",
  "Transfer Data to Cloud Account":"Kopieren in fremde Cloud-Konten. Schutz: Cloud-Egress-Kontrolle, DLP.",
  "Application Layer Protocol":"C2 getarnt in normalem Web-Verkehr. Schutz: Proxy mit Inspektion, Threat-Intel-Feeds.",
  "Proxy":"Verschleiern der Herkunft/C2. Schutz: bekannte Tunnel-/Proxy-Tools erkennen.",
  "Protocol Tunneling":"Tunneln von Datenverkehr. Schutz: anomalen Verkehr erkennen.",
  "Remote Access Software":"Missbrauch legitimer Fernwartung (AnyDesk, TeamViewer u. a.). Schutz: nur freigegebene RMM-Tools zulassen (Allowlist).",
  "Remote Access Tools":"Einsatz von Fernzugriffs-Werkzeugen. Schutz: RMM-Allowlist, Monitoring.",
  "Ingress Tool Transfer":"Nachladen von Werkzeugen aus dem Internet. Schutz: Egress-Filter, Download-Kontrolle.",
  "Data Encrypted for Impact":"Verschlüsselung der Systeme – der eigentliche Ransomware-Schaden. Schutz: Offline-/Immutable-Backups, getesteter Wiederanlauf.",
  "Inhibit System Recovery":"Löschen von Schattenkopien/Backups, um Wiederherstellung zu verhindern. Schutz: unveränderbare, getrennte Backups.",
  "Service Stop":"Stoppen wichtiger Dienste (z. B. Datenbanken) vor der Verschlüsselung. Schutz: Monitoring kritischer Dienste.",
  "Data Destruction":"Gezieltes Löschen von Daten. Schutz: Backups außerhalb der Reichweite der Angreifer.",
  "Financial Theft":"Direkte finanzielle Bereicherung/Erpressung. Schutz: Incident-Response-Plan, Strafverfolgung einbinden."
};

/* Zusätzliche Erläuterung je Gruppe (ergänzt die aus ransomware.live gezogenen Daten).
   model = Geschäftsmodell, note = Einordnung für den Kunden. */
window.GROUP_META = {
  safepay:{model:"Geschlossene Gruppe (kein RaaS)",note:"Sehr aktiv gegen den deutschen Mittelstand – zeitweise die #1-Gruppe für DE. Nutzt überwiegend gültige Zugangsdaten und RDP."},
  qilin:{model:"Ransomware-as-a-Service",note:"Weltweit die reichweitenstärkste RaaS-Plattform, auch in DE sehr präsent. Breites Werkzeugarsenal, Double Extortion."},
  thegentlemen:{model:"Ransomware-as-a-Service",note:"2025 neu aufgetaucht, extrem schnell gewachsen; 90 % Gewinnbeteiligung für Affiliates. Deutschland unter den Top-Zielländern."},
  akira:{model:"Ransomware-as-a-Service",note:"Mutmaßlich aus dem Conti-Umfeld. Trifft stark den Mittelstand und Fertigung; Zugang oft über VPN ohne MFA."},
  lockbit5:{model:"Ransomware-as-a-Service",note:"Neuauflage von LockBit nach der Zerschlagung 2024. Plattformübergreifend (Windows/Linux/ESXi)."},
  dragonforce:{model:"RaaS / „Kartell“",note:"Bekannt durch Angriffe auf britische Einzelhändler; positioniert sich als Ransomware-Kartell."},
  incransom:{model:"Ransomware-as-a-Service",note:"Zielt systematisch auf Gesundheit, Verwaltung, Bildung und Fertigung."},
  payoutsking:{model:"Double Extortion",note:"Jüngere Gruppe mit auffällig vielen deutschen Opfern im Mittelstand."},
  zawoo:{model:"Datendiebstahl-Erpressung",note:"2026 neu; Deutschland ist das häufigste Zielland. Oft Sammel-Leaks vieler kleiner Firmen an einem Tag."},
  play:{model:"Geschlossene Gruppe",note:"Langjährig aktiv, Double Extortion. Zugang oft über ungepatchte, externe Systeme."},
  krybit:{model:"Ransomware-as-a-Service",note:"Erst 2026 gestartet, sehr schnelle Veröffentlichung nach dem Angriff (kurze Verzögerung)."},
  coinbasecartel:{model:"Reine Datendiebstahl-Erpressung",note:"Verschlüsselt nicht, sondern erpresst ausschließlich mit gestohlenen Daten."},
  lamashtu:{model:"Datendiebstahl-Erpressung",note:"2026 neu; Deutschland unter den Top-Zielen. Noch nicht bestätigt, ob echte Verschlüsselung erfolgt."},
  settra:{model:"Datendiebstahl-Erpressung",note:"2026 neu, international aktiv, Deutschland an zweiter Stelle."},
  aurora:{model:"Go-basierte Schadsoftware",note:"Seit 2026 als Erpressergruppe aktiv; auch als Infostealer/Botnet bekannt."},
  rhysida:{model:"Ransomware-as-a-Service",note:"Trifft häufig Bildung, Gesundheit und öffentliche Einrichtungen; Zugang oft über Phishing."},
  cloak:{model:"Ransomware-as-a-Service",note:"Fokussiert ausdrücklich auf kleine und mittlere Unternehmen in Europa, besonders Deutschland."},
  clop:{model:"Datendiebstahl-Erpressung",note:"Berüchtigt für Massen-Ausnutzung von Zero-Days in Datei-Transfer-Software (z. B. MOVEit)."},
  lockbit3:{model:"Ransomware-as-a-Service",note:"Ehemals größte RaaS-Plattform; seit der Zerschlagung 2024 kaum noch neue DE-Opfer."},
  blackbasta:{model:"Ransomware-as-a-Service",note:"2024 sehr aktiv; seit Anfang 2025 keine neuen Opfer mehr gelistet (vermutlich zerfallen)."},
  ransomhub:{model:"Ransomware-as-a-Service",note:"2024 eine der größten Plattformen; seit Frühjahr 2025 keine neuen Opfer mehr gelistet."}
};
