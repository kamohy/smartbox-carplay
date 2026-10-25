# Aufgaben

Version: 0.8.1 (Analyse; Geräte-UI 0.7.0)  
Stand: 2026-10-25 12:14 CET

## Gezielte Telefonmessung 0.8.1

- [x] Zwei bestehende Logstellen im gepinnten rcpservice für Fähigkeitswort und Versionsprüfwert lokalisieren.
- [x] Offlinekandidat mit exakt drei begrenzten Änderungsregionen, gleicher Dateigröße und unveränderter Audioauswahl erzeugen.
- [x] Neue komprimierte RISC-V-Instruktionen unabhängig dekodieren; drei lokale Regressionen bestanden.
- [ ] Kandidat nach gesichertem Updateweg gezielt integrieren und Runtimewirkung prüfen; derzeit ausdrücklich nicht installiert.
- [ ] Die reale BH_HU-Ausgabe beim Fahrzeugstart sichern und erst danach einen Audioformat-Versuch ableiten.

0.8.0-Geräteinstallation bleibt nach gescheiterter Vorbereitung offen; Bestätigung des Netzteilwechsels steht aus. Bereits gesicherte Logs wurden auf dem Dongle noch nicht gelöscht.

## Verständliche Einstellungen und Hardwareprüfung 0.8.0

- [x] Aktuelle sechs Ringlogs und frischen Systemlog vor Änderungen lokal sichern; alle gzip-CRC prüfen.
- [x] LED-Mapping nach Nutzervorgabe 0=Ein/1=Aus als Schalter abbilden.
- [x] Telefonpuffer und Verbindungsstart verständlich erklären; ungeklärte Profilwirkung ausdrücklich offen lassen.
- [x] 20-Sekunden-Verzögerung für delay=2 im Originalcode nachweisen; delay=1 nicht mit einer erfundenen Zeit versehen.
- [x] Feste Hardwareabfrage und Hardware-/Grenzenkarte ergänzen.
- [x] Mikrofon-Einheitenfehler korrigieren und Netzwerkinterfaces getrennt ausgeben.
- [x] Loglöschung ausschließlich eigener sechs Slots, ohne Bootzähler/fremde Daten zu löschen, implementieren und testen.
- [x] Elf erlaubte Imagepfade unabhängig prüfen und zweimal identisch bauen; 27 Python- und drei JS-Prüfprogramme erfolgreich.
- [ ] Version installieren, Oberfläche und LED-Schreib-/Lesepfad am Gerät prüfen.
- [ ] Reale Hardware-/Takt-/Busdaten erfassen; Leistungsreserve und nicht bewiesene Grenzen getrennt dokumentieren.
- [ ] Nach erneuter Sicherung aktuelle gespeicherte Logs auf dem Gerät löschen und leere Liste verifizieren.

## Befund aus dem ersten Fahrzeugtest

- [x] Sechs persistente Logs sichern und vollständig auf gzip-CRC prüfen; Rohdaten lokal halten.
- [x] Nutzer bestätigt Teams-Versuche in Mode 2 und 3; aktuelle Konfiguration aud=3 gelesen, nicht verändert.
- [x] 16-kHz-iPhone-Anfrage gegen 8-kHz-USB-Telefonstart und gemessene 8-kHz-Taktrückmeldung abgleichen.
- [x] Mikrofonumwandlung 8 → 16 kHz und falsche kHz-Herstellerbeschriftung belegen.
- [x] Radio-Fähigkeits-/Plugin-Versionswahl für 8/16 kHz im Originalcode weiterverfolgen.
- [x] Offlineanalysator mit Deduplizierung, getrennten Boots/Audiotypen und CRC-Fehlerfällen ergänzen.
- [ ] HU-Fähigkeitswörter, GetHUPluginVer und erste Formatauswahl dauerhaft erfassen; bislang im Logausschnitt nicht enthalten.
- [ ] Erst anhand der echten Fähigkeiten einen Telefonformat-Versuch ableiten; Versionsprüfung nicht blind entfernen.
- [ ] kHz-Anzeige des installierten Webparsers korrigieren; aktuell 0.7.0, kein Fix geflasht.
- [ ] Alle tatsächlichen WLAN-Datenschnittstellen getrennt messen; null Bytes auf p2p-wlan0-0 erlauben keine Verlustdiagnose.
- [ ] Telefonformat des direkten Kabelvergleichs nachweisen; hörbaren Vergleich und Zeitzuordnung beibehalten.

## Automatische Werte und persistente Logs 0.7.0

- [x] CPU anhand realer Daten auf Laufzeit-/Idle-Sekunden umstellen; angehaltene Idle-Jiffies nicht als 100 % Last interpretieren.
- [x] Liveanzeige automatisch alle zwei Sekunden, unabhängig von Browseraufzeichnung; Hintergrundpause.
- [x] Native Shellaufzeichnung in vorhandenen Startpfad einbinden; kein Node-Runtime erforderlich.
- [x] Echter RW-Datenmount, drei Startslots mit je zwei gzip-Dateien bis 24 KiB, mindestens 64 KiB Reserve.
- [x] CRC, Bootrotation, Platzmangel, übergroße Logs, RAM-/RO-Mounts und fremde Dateien mit echtem Skript prüfen.
- [x] Zweimal byteidentisch bauen; Kernel und alle nicht freigegebenen Originaldateien erhalten.
- [x] Freien Speicher, Daemon, CPU und automatische Anzeige am Gerät prüfen; 512 KiB gesamt, zunächst 304 KiB frei, sieben Webdateihashes passend.
- [x] Log sichern, neu starten und beide bisherigen Dateien erneut mit gleichem Hash laden; gzip-CRC gültig.
- [x] Erhalt nach echtem Abziehen der Stromversorgung und erneutem PC-Anschluss bestätigen; beide Boot-1-Dateien SHA-256-identisch, neue Logs unter Boot 3.

## Integrierte Diagnose 0.6.0

- [x] Lesendes CGI für Betriebssystemwerte, Audio-Logausschnitt und frischen Logexport ergänzen.
- [x] Diagnosekarte direkt in die Einstellungsseite integrieren; Browseraufzeichnung und lokalen JSON-Export ergänzen.
- [x] Unbekannte Audiowerte ausdrücklich unbekannt lassen; bekannte Hersteller-Logformate auswerten.
- [x] CGI-Abfrage-/Methodengrenzen, echte Shellausführung mit proc/sys-Fixtures und CPU-/Audioparser prüfen.
- [x] Neues Image zweimal byteidentisch bauen; CGI-Ausführungsmodus und Erhalt aller ursprünglichen Einträge unabhängig prüfen.
- [x] 0.6.0 über eigenen Updatekanal installieren und am Gerät prüfen; CPU-Jiffies-Anzeige als fehlerhaft erkannt.
- [x] Aktive Teams-Telefonpfade im Fahrzeug mit den neuen Werkzeugen erfassen (Starts 5/6, Mode 2/3).

## Oberfläche und eigener Updatekanal

- [x] Bad-Hippo-SVG einbetten; Oberfläche und Dialoge dunkel gestalten.
- [x] Öffentliches GitHub-Repository `kamohy/smartbox-carplay` anlegen; Geräteexporte ausschließen.
- [x] Herstellerquelle und tatsächlichen Browser-Download-/Uploadablauf identifizieren.
- [x] Dauerhafte GitHub-Updateadresse in eigene Firmware aufnehmen; keine DNS-/TLS-Umleitung nötig.
- [x] UI-Kandidat 0.5.0 bauen, zweimal reproduzieren und alle originalen Inodes sowie Kernel unabhängig abgleichen.
- [x] Eigenen Updater gegen falsche Plattform, falschen Downloadpfad, beschädigte Nutzlast und nicht freigegebene Pakete prüfen.
- [ ] Vollbackup und Recovery verifizieren. Nutzer hat den ersten UI-Updateversuch ausdrücklich ohne diese Voraussetzung und mit möglichem Geräteverlust freigegeben.
- [ ] Den eigenen `/sbin/update`-/Recovery-Prüfpfad vollständig untersuchen; neu berechnete MD5/CPIO-Prüfsummen allein beweisen keine Annahme durch den Geräte-Updater.
- [x] Erstinstallation, anschließenden Normalstart und Auslieferung aller sechs UI-Dateien direkt am Adapter per SHA-256 verifiziert.
- [x] GitHub-/CORS-Download unter echter Geräte-HTTP-Origin end-to-end geprüft (0.5.0 → 0.6.0).
- [ ] Update zusätzlich unter iPhone/Safari prüfen.
- [x] Nach Geräteprüfung UI-Version 0.5.0 im eigenen Manifest freigeben; kein Audio-/Fahrzeugerfolg behauptet.

## Nächster sicherer Schritt

- [x] Eigenen frischen Logexport ergänzen, der den OEM-Cache umgeht; altes Erfassungsskript nutzt weiterhin Herstellerexport.
- [x] Teams-Anruf im Hyundai i30 Kombi (2018) mit Mode 2/3 protokolliert: 16-kHz-Anfrage, 8-kHz-USB-Telefonpfad, Mikrofonumwandlung.
- [ ] Als Abgrenzung einen normalen Telefonanruf über den Adapter prüfen: ebenfalls beidseitig blechern oder nur Teams?
- [ ] Musik zusätzlich als Kontrolle prüfen; derzeit ist nur der Teams-Fehler ausdrücklich bestätigt.
- [ ] Prüfen, ob das Radio parallel direkt per Bluetooth mit dem iPhone verbunden ist; nur diese Verbindung für den Vergleich trennen, Bluetooth und die SmartBox-Kopplung am iPhone eingeschaltet lassen.
- [ ] Nach dem ersten Telefonlog einen gezielten Modusvergleich planen. Im bereits nachvollzogenen Telefon-Pufferpfad verhalten sich 1/2/3 gleich; Default vs. Mode 2 ist dort der tatsächlich sichtbare Unterschied.
- [x] Telefon-Ein-/Ausgaberaten und 8→16-kHz-Mono-Umwandlung gegenübergestellt; kein vollständiger PCM-/Kabelvergleich vorhanden.
- [ ] Gemeldeten HU-Hersteller und Modellkennung aus dem Fahrzeuglog ermitteln und auf den tatsächlichen Modellpfad abbilden.
- [ ] Bei Teams ist ein Sprach-/Telefonpfad erwartbar; Mono oder 16 kHz allein beweisen keinen Fehler. Die konkrete Verschlechterung gegenüber Kabel muss durch ausgehandelte Formate/Verarbeitung erklärt werden.

## Firmwareforschung

- [ ] Startskript-Modifikation für einen ausschließlich kontrollierten Offline-Test von `/tmp/ly_force_musicrate` entwerfen.
- [ ] Musik-Hook erst weiterverfolgen, falls auch Musik betroffen ist; für Teams den Telefon-/Mikrofonpfad priorisieren.
- [x] Deterministischen SWUpdate-/CPIO-/SquashFS-Repacker gebaut und zweimal offline mit identischem Ergebnis geprüft (0.5.0).
- [ ] Signatur-, Prüfsummen- und Bootphasenverhalten vollständig dokumentieren.
- [ ] Flash-Chip-Backup und Hardware-Recoveryverfahren entwickeln und verifizieren.
- [ ] Erst danach eine modifizierte Firmware auf einem zweiten Adapter testen.
- [ ] Scharfe Fotos beider Platinenseiten erstellen, um Flash-Zugriff, mögliche Recoverykontakte und Spannungspegel zu bestimmen.

## Erledigt

- [x] 2026-10-25 10:03 CET: Echte UI-Firmware über den normalen Updateweg erfolgreich installiert; Originale, Uploadquittung, Zwischenzustände und Nachher-Dateivergleich lokal archiviert.
- [x] 2026-10-25 10:03 CET: Windows-xfel 1.4.0 samt SHA-256 geprüft; kein FEL-Gerät erreichbar. Ein unabhängiger Rückweg wurde damit nicht bestätigt.
- [x] 2026-10-25 10:03 CET: Lesendes Zwei-Pass-Backupwerkzeug und eng begrenzten Einmal-Uploader mit unabhängiger MIME-Payloadprüfung ergänzt.

- [x] 2026-10-25 08:25 CET: USB-Identität und Windows-Treiberstatus erfasst.
- [x] 2026-10-25 08:36 CET: 5-GHz-WLAN und lokalen Verwaltungszugang identifiziert.
- [x] 2026-10-25 08:39 CET: `aud=2` gesetzt und nach Neustart verifiziert.
- [x] 2026-10-25 08:47 CET: Weboberfläche, stabile Firmware und Cloud-Testabbild bytegenau archiviert.
- [x] 2026-10-25 08:52 CET: Hersteller-XOR-Transformation reproduziert und beide Abbilder mit eingebetteter MD5-Prüfung entschlüsselt.
- [x] 2026-10-25 08:54 CET: SWUpdate-Mitglieder und beide SquashFS-Dateisysteme extrahiert.
- [x] 2026-10-25 08:56 CET: Android-Boot-v2-Header, Kernel und Device Tree zerlegt.
- [x] 2026-10-25 08:57 CET: 13 geänderte Dateien zwischen stabiler und Testfirmware identifiziert.
- [x] 2026-10-25 08:58 CET: V821-Plattformpfad, RTL8723FS, 64 MiB RAM und Audio-Gadget-Code belegt.
- [x] 2026-10-25 08:59 CET: Audiomodi und erzwingbare Musik-Abtastrate im Binärcode lokalisiert.
- [x] 2026-10-25 09:00 CET: Logentschlüsselung mit Salvage-Modus und Fahrzeug-Erfassungsskript geprüft.
- [x] 2026-10-25 09:00 CET: Projektstand 0.3.0 samt Hashbelegen dokumentiert.
- [x] 2026-10-25 09:05 CET: Versteckten `lylink`-Pack beider Abbilder einschließlich `rcpservice` und `librcarplay.so` CRC-geprüft extrahiert.
- [x] 2026-10-25 09:07 CET: Vollständig valide Logrekonstruktion einschließlich eingebettetem Größenfeld umgesetzt und Cache-Verhalten aus dem CGI belegt.
- [x] 2026-10-25 09:09 CET: Hyundai-Sonderfall als exakte Kennung `Tinnos / MISTRA` eingegrenzt; kein belegter i30-Fix.
- [x] 2026-10-25 09:11 CET: Sieben Prüfungen gegen reale Archive, CRC-Fehlerfälle und externe Andes-Instruktionsvektoren bestanden.

