# Minimaler Wartungszwischenstand

Version: 0.8.2
Stand: 2026-10-25 12:53 CET

Der Nutzer hat den laufenden Auftrag auf Speicheranzeige, Fehlerprotokoll und LÃƒÂ¶schen der lokal gesicherten eigenen Logs begrenzt. Dieser getrennte Overlayzweig basiert auf dem gepinnten 0.7.0-Image. Die grÃƒÂ¶ÃƒÅ¸ere 0.8.0-EinstellungsoberflÃƒÂ¤che und die Offline-Telefonmessstelle 0.8.1 sind nicht enthalten. GerÃƒÂ¤teinstallation und LÃƒÂ¶schung sind noch nicht bestÃƒÂ¤tigt.

- `GET /cgi-bin/bh-diagnostics.cgi?id=space`: verfÃƒÂ¼gbarer RAM und feste DateisystemkapazitÃƒÂ¤ten fÃƒÂ¼r `/tmp`, `/mnt/UDISK`, `/mnt/customer`, `/`; Beschreibbarkeit aus dem tatsÃƒÂ¤chlichen Mount. Freie Bytes auf schreibgeschÃƒÂ¼tztem SquashFS sind kein Nutzspeicher.
- `GET /cgi-bin/bh-diagnostics.cgi?id=errors`: begrenzter Auszug aus Updatezustand, Dateisystemen, Updaterprozessen, Kernel-/Anwendungsfehlern und vorhandenen festen Updateprotokollen. Kein beliebiger Dateipfad oder Befehl. Rohdaten bleiben lokal und kÃƒÂ¶nnen Kennungen enthalten.
- `POST /cgi-bin/bh-diagnostics.cgi?id=clear`: fester serieller LÃƒÂ¶schauftrag fÃƒÂ¼r die sechs eigenen Logslots plus eigene RAM-Snapshots. BootzÃƒÂ¤hler und fremde Dateien bleiben bestehen; die Aufzeichnung lÃƒÂ¤uft weiter. Fremde Origins und zusÃƒÂ¤tzliche Queryparameter werden verworfen.

Das Fehlerpanel schreibt keinen zusÃƒÂ¤tzlichen permanenten Flashring. Bereits gespeicherte Systemlogs enthalten ebenfalls Fehlermeldungen; Browserfehler bleiben auf hÃƒÂ¶chstens 40 gekÃƒÂ¼rzte EintrÃƒÂ¤ge dieser Seite begrenzt.

Der neue Builder entfernt aus der Updatebeschreibung exakt den Kernel-Imageblock und lÃƒÂ¤sst den unverÃƒÂ¤nderten Kernelmember weg. Bootenv-Phasen und Customer-Ziel bleiben erhalten. Das halbiert die zu ÃƒÂ¼bertragende Nutzlast, ist aber vor erfolgreichem GerÃƒÂ¤teabschluss keine bestÃƒÂ¤tigte LÃƒÂ¶sung des Vorbereitungsfehlers.

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_maintenance -v
.\.venv\Scripts\python.exe -m tools.build_maintenance_firmware --output dist/maintenance-0.8.2-new
```

Zwei Builds: 3.034.669 Byte; SHA-256 `546416e4d2c3279142d1aa29a3e51e13780e36c0537e7459f9d3b55dc9e02cd4`. Der Builder prÃƒÂ¼ft alle ursprÃƒÂ¼nglichen 0.7.0-Inodes und unverÃƒÂ¤nderte Daten unabhÃƒÂ¤ngig. Ãƒâ€“ffentlicher Updatemanifest bleibt bis realem GerÃƒÂ¤tenachweis gesperrt.
