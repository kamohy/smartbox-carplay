# Minimaler Wartungszwischenstand

Version: 0.8.2
Stand: 2026-10-25 12:56 CET

Der Nutzer hat den laufenden Auftrag auf Speicheranzeige, Fehlerprotokoll und Löschen der lokal gesicherten eigenen Logs begrenzt. Dieser getrennte Overlayzweig basiert auf dem gepinnten 0.7.0-Image. Die größere 0.8.0-Einstellungsoberfläche und die Offline-Telefonmessstelle 0.8.1 sind nicht enthalten. Der reale Upload wurde angenommen, blieb aber vier Minuten in Zustand 1 ohne Abschluss. Nach kontrolliertem Neustart läuft 0.7.0/Updatezustand 0. Die aktive Version lehnt den Löschaufruf mit HTTP 405 ab. Logs sind gesichert, aber noch nicht gelöscht. Ein vollständiger Stromreset ist der nächste Abgrenzungstest.

- `GET /cgi-bin/bh-diagnostics.cgi?id=space`: verfügbarer RAM und feste Dateisystemkapazitäten für `/tmp`, `/mnt/UDISK`, `/mnt/customer`, `/`; Beschreibbarkeit aus dem tatsächlichen Mount. Freie Bytes auf schreibgeschütztem SquashFS sind kein Nutzspeicher.
- `GET /cgi-bin/bh-diagnostics.cgi?id=errors`: begrenzter Auszug aus Updatezustand, Dateisystemen, Updaterprozessen, Kernel-/Anwendungsfehlern und vorhandenen festen Updateprotokollen. Kein beliebiger Dateipfad oder Befehl. Rohdaten bleiben lokal und können Kennungen enthalten.
- `POST /cgi-bin/bh-diagnostics.cgi?id=clear`: fester serieller Löschauftrag für die sechs eigenen Logslots plus eigene RAM-Snapshots. Bootzähler und fremde Dateien bleiben bestehen; die Aufzeichnung läuft weiter. Fremde Origins und zusätzliche Queryparameter werden verworfen.

Das Fehlerpanel schreibt keinen zusätzlichen permanenten Flashring. Bereits gespeicherte Systemlogs enthalten ebenfalls Fehlermeldungen; Browserfehler bleiben auf höchstens 40 gekürzte Einträge dieser Seite begrenzt.

Der neue Builder entfernt aus der Updatebeschreibung exakt den Kernel-Imageblock und lässt den unveränderten Kernelmember weg. Bootenv-Phasen und Customer-Ziel bleiben erhalten. Das halbiert die zu übertragende Nutzlast, ist aber vor erfolgreichem Geräteabschluss keine bestätigte Lösung des Vorbereitungsfehlers.

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_maintenance -v
.\.venv\Scripts\python.exe -m tools.build_maintenance_firmware --output dist/maintenance-0.8.2-new
```

Zwei Builds: 3.034.669 Byte; SHA-256 `546416e4d2c3279142d1aa29a3e51e13780e36c0537e7459f9d3b55dc9e02cd4`. Der Builder prüft alle ursprünglichen 0.7.0-Inodes und unveränderte Daten unabhängig. Öffentlicher Updatemanifest bleibt bis realem Gerätenachweis gesperrt.
