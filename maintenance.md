# Minimaler Wartungszwischenstand

Version: 0.8.3 (Kandidat; Geräte-UI zuletzt 0.7.0)
Stand: 2026-10-25 14:07 CET

Abschließender Gerätestand: Beide gezielt geänderten 0.8.3-Versuche (vor und nach dem freigegebenen Datenreset) blieben nach angenommenem Upload in Zustand 1. Nach jeweils kontrolliertem Neustart ist UI 0.7.0/Updatezustand 0 bestätigt. Die neue Oberfläche ist nicht installiert; es erfolgt kein weiterer unveränderter Upload. Letzte freie Kapazität nach neuer Aufzeichnung: 276/512 KiB; direkt nach dem Reset waren es 304 KiB. Die alten erreichbaren Logs sind entfernt und alle ursprünglichen Fahrzeuglogs lokal gesichert.

Der aktuelle Auftrag bleibt auf Speicheranzeige, Fehlerprotokoll und Loglöschung begrenzt. Das freigegebene Leeren des gesamten UDISK-Datenspeichers wurde am 2026-10-25 um 14:00 einmal ausgeführt: alte erreichbare Logs entfernt, neue Aufzeichnung mit Bootzähler 1, 304 statt 224 KiB frei und neun verglichene Einstellungen unverändert. Gespeicherte Kopplungen waren ausdrücklich in der Zustimmung enthalten; das iPhone muss gegebenenfalls neu gekoppelt werden. Die originalen Fahrzeuglogs bleiben lokal gesichert.

Die neuen Webfunktionen sind bislang nicht auf dem Dongle installiert. Der vorherige Customer-only-Kandidat 0.8.2 blieb nach dem Upload in der Vorbereitung hängen. 0.8.3 verwendet wieder die vollständige ursprüngliche Paketstruktur. Kernel und Updatebeschreibung bleiben bytegleich zur geprüften 0.7.0-Basis; der vollständige Updateweg schreibt den unveränderten Kernel erneut. Sechs Customer-Pfade werden verändert, alle anderen ursprünglichen Inodes und Daten unabhängig geprüft.

Der neue Recorder wird nach `/tmp/bh-recorder.sh` kopiert, startet mit Arbeitsverzeichnis `/` und nutzt die RAM-Kopie der Diagnose-CGI. Bei aktivem Updatezustand startet er nicht beziehungsweise beendet einen bereits laufenden Prozess mit PID-Aufräumen. Damit soll er die Customer-Partition beim Update nicht mehr offen halten. Diese Korrektur ersetzt keinen bereits laufenden alten 0.7.0-Recorder; Geräteinstallation steht noch aus.

- `GET /cgi-bin/bh-diagnostics.cgi?id=space`: verfügbarer RAM und feste Dateisystemkapazitäten für `/tmp`, `/mnt/UDISK`, `/mnt/customer`, `/` sowie Beschreibbarkeit. Freie Bytes auf schreibgeschütztem SquashFS sind kein Nutzspeicher.
- `GET /cgi-bin/bh-diagnostics.cgi?id=errors`: begrenzte lokale Auszüge aus Updatezustand, Mounts, Updaterprozessen, Kernel-/Anwendungsfehlern und vorhandenen festen Updateprotokollen. Kein beliebiger Dateipfad oder Befehl.
- `POST /cgi-bin/bh-diagnostics.cgi?id=clear`: ausschließlich die sechs eigenen Logslots und eigene RAM-Snapshots. Bootzähler und fremde Dateien bleiben erhalten; die Aufzeichnung läuft weiter. Diese begrenzte Funktion ist vom gesondert freigegebenen vollständigen OEM-Datenreset zu unterscheiden.

Das Fehlerpanel schreibt keinen zusätzlichen permanenten Flashring. Gespeicherte Systemlogs enthalten ebenfalls die Rohmeldungen; Browserfehler bleiben auf höchstens 40 gekürzte Einträge dieser Seite begrenzt.

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_maintenance -v
.\.venv\Scripts\python.exe -m tools.build_maintenance_firmware --output dist/maintenance-0.8.3-new
```

Zwei Builds sind bytegleich: 6.199.341 Byte; SHA-256 `6537c1c1c9c899439dc5c485d5037f29e46c1ec13c75aefab897a79369b76adb`. 34 lokale Pythonprüfungen, drei JS-Prüfprogramme und Shell-/JS-Syntaxprüfungen bestehen. Der öffentliche Updatekanal bleibt bis zum erfolgreichen Gerätenachweis gesperrt.
