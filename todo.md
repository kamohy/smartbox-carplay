# Aufgaben

Version: 0.8.2 (Wartungszwischenstand; GerÃƒÂ¤te-UI zuletzt 0.7.0)
Stand: 2026-10-25 12:53 CET

## Vom Nutzer begrenzter Wartungszwischenstand 0.8.2

- [x] Netzteilwechsel vom Nutzer bestÃƒÂ¤tigt; zweiter Vollpaketversuch protokolliert. Er blieb ebenfalls in Zustand 1; kontrollierter Neustart stellte 0.7.0/Updatezustand 0 wieder her.
- [x] Aktuelle sechs Logs erneut lokal mit gÃƒÂ¼ltiger gzip-CRC und SHA-256 sichern.
- [x] Minimale Speicherabfrage fÃƒÂ¼r RAM, `/tmp`, Daten- und Systempartitionen sowie feste FehlerauszÃƒÂ¼ge implementieren.
- [x] LÃƒÂ¶schung auf eigene sechs Logslots und eigene RAM-Dateien begrenzen; BootzÃƒÂ¤hler und fremde Dateien erhalten.
- [x] Kleineres Customer-only-Paket erstellen; unverÃƒÂ¤nderte Bootenv-Phasen und sÃƒÂ¤mtliche ÃƒÂ¼brigen 0.7.0-Dateien unabhÃƒÂ¤ngig prÃƒÂ¼fen. Zwei Builds bytegleich, 32 PythonprÃƒÂ¼fungen erfolgreich.
- [ ] Wartungsinstallation und normale Wiederkehr am GerÃƒÂ¤t verifizieren.
- [ ] Echte `/tmp`-KapazitÃƒÂ¤t und Fehler-/UpdaterauszÃƒÂ¼ge lesen.
- [ ] Nach vollstÃƒÂ¤ndiger aktueller Sicherung Logs am GerÃƒÂ¤t lÃƒÂ¶schen, leere Liste und freien Platz belegen.

## Gezielte Telefonmessung 0.8.1

- [x] Zwei bestehende Logstellen im gepinnten rcpservice fÃƒÂ¼r FÃƒÂ¤higkeitswort und VersionsprÃƒÂ¼fwert lokalisieren.
- [x] Offlinekandidat mit exakt drei begrenzten Ãƒâ€žnderungsregionen, gleicher DateigrÃƒÂ¶ÃƒÅ¸e und unverÃƒÂ¤nderter Audioauswahl erzeugen.
- [x] Neue komprimierte RISC-V-Instruktionen unabhÃƒÂ¤ngig dekodieren; drei lokale Regressionen bestanden.
- [ ] Kandidat nach gesichertem Updateweg gezielt integrieren und Runtimewirkung prÃƒÂ¼fen; derzeit ausdrÃƒÂ¼cklich nicht installiert.
- [ ] Die reale BH_HU-Ausgabe beim Fahrzeugstart sichern und erst danach einen Audioformat-Versuch ableiten.

0.8.0-GerÃƒÂ¤teinstallation bleibt nach gescheiterter Vorbereitung offen. Der Nutzer hat den Netzteilanschluss bestÃƒÂ¤tigt und den nÃƒÂ¤chsten Schritt auf Wartung 0.8.2 begrenzt. Bereits gesicherte Logs wurden auf dem Dongle noch nicht gelÃƒÂ¶scht.

## VerstÃƒÂ¤ndliche Einstellungen und HardwareprÃƒÂ¼fung 0.8.0

- [x] Aktuelle sechs Ringlogs und frischen Systemlog vor Ãƒâ€žnderungen lokal sichern; alle gzip-CRC prÃƒÂ¼fen.
- [x] LED-Mapping nach Nutzervorgabe 0=Ein/1=Aus als Schalter abbilden.
- [x] Telefonpuffer und Verbindungsstart verstÃƒÂ¤ndlich erklÃƒÂ¤ren; ungeklÃƒÂ¤rte Profilwirkung ausdrÃƒÂ¼cklich offen lassen.
- [x] 20-Sekunden-VerzÃƒÂ¶gerung fÃƒÂ¼r delay=2 im Originalcode nachweisen; delay=1 nicht mit einer erfundenen Zeit versehen.
- [x] Feste Hardwareabfrage und Hardware-/Grenzenkarte ergÃƒÂ¤nzen.
- [x] Mikrofon-Einheitenfehler korrigieren und Netzwerkinterfaces getrennt ausgeben.
- [x] LoglÃƒÂ¶schung ausschlieÃƒÅ¸lich eigener sechs Slots, ohne BootzÃƒÂ¤hler/fremde Daten zu lÃƒÂ¶schen, implementieren und testen.
- [x] Elf erlaubte Imagepfade unabhÃƒÂ¤ngig prÃƒÂ¼fen und zweimal identisch bauen; 27 Python- und drei JS-PrÃƒÂ¼fprogramme erfolgreich.
- [ ] Version installieren, OberflÃƒÂ¤che und LED-Schreib-/Lesepfad am GerÃƒÂ¤t prÃƒÂ¼fen.
- [ ] Reale Hardware-/Takt-/Busdaten erfassen; Leistungsreserve und nicht bewiesene Grenzen getrennt dokumentieren.
- [ ] Nach erneuter Sicherung aktuelle gespeicherte Logs auf dem GerÃƒÂ¤t lÃƒÂ¶schen und leere Liste verifizieren.

## Befund aus dem ersten Fahrzeugtest

- [x] Sechs persistente Logs sichern und vollstÃƒÂ¤ndig auf gzip-CRC prÃƒÂ¼fen; Rohdaten lokal halten.
- [x] Nutzer bestÃƒÂ¤tigt Teams-Versuche in Mode 2 und 3; aktuelle Konfiguration aud=3 gelesen, nicht verÃƒÂ¤ndert.
- [x] 16-kHz-iPhone-Anfrage gegen 8-kHz-USB-Telefonstart und gemessene 8-kHz-TaktrÃƒÂ¼ckmeldung abgleichen.
- [x] Mikrofonumwandlung 8 Ã¢â€ â€™ 16 kHz und falsche kHz-Herstellerbeschriftung belegen.
- [x] Radio-FÃƒÂ¤higkeits-/Plugin-Versionswahl fÃƒÂ¼r 8/16 kHz im Originalcode weiterverfolgen.
- [x] Offlineanalysator mit Deduplizierung, getrennten Boots/Audiotypen und CRC-FehlerfÃƒÂ¤llen ergÃƒÂ¤nzen.
- [ ] HU-FÃƒÂ¤higkeitswÃƒÂ¶rter, GetHUPluginVer und erste Formatauswahl dauerhaft erfassen; bislang im Logausschnitt nicht enthalten.
- [ ] Erst anhand der echten FÃƒÂ¤higkeiten einen Telefonformat-Versuch ableiten; VersionsprÃƒÂ¼fung nicht blind entfernen.
- [ ] kHz-Anzeige des installierten Webparsers korrigieren; aktuell 0.7.0, kein Fix geflasht.
- [ ] Alle tatsÃƒÂ¤chlichen WLAN-Datenschnittstellen getrennt messen; null Bytes auf p2p-wlan0-0 erlauben keine Verlustdiagnose.
- [ ] Telefonformat des direkten Kabelvergleichs nachweisen; hÃƒÂ¶rbaren Vergleich und Zeitzuordnung beibehalten.

## Automatische Werte und persistente Logs 0.7.0

- [x] CPU anhand realer Daten auf Laufzeit-/Idle-Sekunden umstellen; angehaltene Idle-Jiffies nicht als 100 % Last interpretieren.
- [x] Liveanzeige automatisch alle zwei Sekunden, unabhÃƒÂ¤ngig von Browseraufzeichnung; Hintergrundpause.
- [x] Native Shellaufzeichnung in vorhandenen Startpfad einbinden; kein Node-Runtime erforderlich.
- [x] Echter RW-Datenmount, drei Startslots mit je zwei gzip-Dateien bis 24 KiB, mindestens 64 KiB Reserve.
- [x] CRC, Bootrotation, Platzmangel, ÃƒÂ¼bergroÃƒÅ¸e Logs, RAM-/RO-Mounts und fremde Dateien mit echtem Skript prÃƒÂ¼fen.
- [x] Zweimal byteidentisch bauen; Kernel und alle nicht freigegebenen Originaldateien erhalten.
- [x] Freien Speicher, Daemon, CPU und automatische Anzeige am GerÃƒÂ¤t prÃƒÂ¼fen; 512 KiB gesamt, zunÃƒÂ¤chst 304 KiB frei, sieben Webdateihashes passend.
- [x] Log sichern, neu starten und beide bisherigen Dateien erneut mit gleichem Hash laden; gzip-CRC gÃƒÂ¼ltig.
- [x] Erhalt nach echtem Abziehen der Stromversorgung und erneutem PC-Anschluss bestÃƒÂ¤tigen; beide Boot-1-Dateien SHA-256-identisch, neue Logs unter Boot 3.

## Integrierte Diagnose 0.6.0

- [x] Lesendes CGI fÃƒÂ¼r Betriebssystemwerte, Audio-Logausschnitt und frischen Logexport ergÃƒÂ¤nzen.
- [x] Diagnosekarte direkt in die Einstellungsseite integrieren; Browseraufzeichnung und lokalen JSON-Export ergÃƒÂ¤nzen.
- [x] Unbekannte Audiowerte ausdrÃƒÂ¼cklich unbekannt lassen; bekannte Hersteller-Logformate auswerten.
- [x] CGI-Abfrage-/Methodengrenzen, echte ShellausfÃƒÂ¼hrung mit proc/sys-Fixtures und CPU-/Audioparser prÃƒÂ¼fen.
- [x] Neues Image zweimal byteidentisch bauen; CGI-AusfÃƒÂ¼hrungsmodus und Erhalt aller ursprÃƒÂ¼nglichen EintrÃƒÂ¤ge unabhÃƒÂ¤ngig prÃƒÂ¼fen.
- [x] 0.6.0 ÃƒÂ¼ber eigenen Updatekanal installieren und am GerÃƒÂ¤t prÃƒÂ¼fen; CPU-Jiffies-Anzeige als fehlerhaft erkannt.
- [x] Aktive Teams-Telefonpfade im Fahrzeug mit den neuen Werkzeugen erfassen (Starts 5/6, Mode 2/3).

## OberflÃƒÂ¤che und eigener Updatekanal

- [x] Bad-Hippo-SVG einbetten; OberflÃƒÂ¤che und Dialoge dunkel gestalten.
- [x] Ãƒâ€“ffentliches GitHub-Repository `kamohy/smartbox-carplay` anlegen; GerÃƒÂ¤teexporte ausschlieÃƒÅ¸en.
- [x] Herstellerquelle und tatsÃƒÂ¤chlichen Browser-Download-/Uploadablauf identifizieren.
- [x] Dauerhafte GitHub-Updateadresse in eigene Firmware aufnehmen; keine DNS-/TLS-Umleitung nÃƒÂ¶tig.
- [x] UI-Kandidat 0.5.0 bauen, zweimal reproduzieren und alle originalen Inodes sowie Kernel unabhÃƒÂ¤ngig abgleichen.
- [x] Eigenen Updater gegen falsche Plattform, falschen Downloadpfad, beschÃƒÂ¤digte Nutzlast und nicht freigegebene Pakete prÃƒÂ¼fen.
- [ ] Vollbackup und Recovery verifizieren. Nutzer hat den ersten UI-Updateversuch ausdrÃƒÂ¼cklich ohne diese Voraussetzung und mit mÃƒÂ¶glichem GerÃƒÂ¤teverlust freigegeben.
- [ ] Den eigenen `/sbin/update`-/Recovery-PrÃƒÂ¼fpfad vollstÃƒÂ¤ndig untersuchen; neu berechnete MD5/CPIO-PrÃƒÂ¼fsummen allein beweisen keine Annahme durch den GerÃƒÂ¤te-Updater.
- [x] Erstinstallation, anschlieÃƒÅ¸enden Normalstart und Auslieferung aller sechs UI-Dateien direkt am Adapter per SHA-256 verifiziert.
- [x] GitHub-/CORS-Download unter echter GerÃƒÂ¤te-HTTP-Origin end-to-end geprÃƒÂ¼ft (0.5.0 Ã¢â€ â€™ 0.6.0).
- [ ] Update zusÃƒÂ¤tzlich unter iPhone/Safari prÃƒÂ¼fen.
- [x] Nach GerÃƒÂ¤teprÃƒÂ¼fung UI-Version 0.5.0 im eigenen Manifest freigeben; kein Audio-/Fahrzeugerfolg behauptet.

## NÃƒÂ¤chster sicherer Schritt

- [x] Eigenen frischen Logexport ergÃƒÂ¤nzen, der den OEM-Cache umgeht; altes Erfassungsskript nutzt weiterhin Herstellerexport.
- [x] Teams-Anruf im Hyundai i30 Kombi (2018) mit Mode 2/3 protokolliert: 16-kHz-Anfrage, 8-kHz-USB-Telefonpfad, Mikrofonumwandlung.
- [ ] Als Abgrenzung einen normalen Telefonanruf ÃƒÂ¼ber den Adapter prÃƒÂ¼fen: ebenfalls beidseitig blechern oder nur Teams?
- [ ] Musik zusÃƒÂ¤tzlich als Kontrolle prÃƒÂ¼fen; derzeit ist nur der Teams-Fehler ausdrÃƒÂ¼cklich bestÃƒÂ¤tigt.
- [ ] PrÃƒÂ¼fen, ob das Radio parallel direkt per Bluetooth mit dem iPhone verbunden ist; nur diese Verbindung fÃƒÂ¼r den Vergleich trennen, Bluetooth und die SmartBox-Kopplung am iPhone eingeschaltet lassen.
- [ ] Nach dem ersten Telefonlog einen gezielten Modusvergleich planen. Im bereits nachvollzogenen Telefon-Pufferpfad verhalten sich 1/2/3 gleich; Default vs. Mode 2 ist dort der tatsÃƒÂ¤chlich sichtbare Unterschied.
- [x] Telefon-Ein-/Ausgaberaten und 8Ã¢â€ â€™16-kHz-Mono-Umwandlung gegenÃƒÂ¼bergestellt; kein vollstÃƒÂ¤ndiger PCM-/Kabelvergleich vorhanden.
- [ ] Gemeldeten HU-Hersteller und Modellkennung aus dem Fahrzeuglog ermitteln und auf den tatsÃƒÂ¤chlichen Modellpfad abbilden.
- [ ] Bei Teams ist ein Sprach-/Telefonpfad erwartbar; Mono oder 16 kHz allein beweisen keinen Fehler. Die konkrete Verschlechterung gegenÃƒÂ¼ber Kabel muss durch ausgehandelte Formate/Verarbeitung erklÃƒÂ¤rt werden.

## Firmwareforschung

- [ ] Startskript-Modifikation fÃƒÂ¼r einen ausschlieÃƒÅ¸lich kontrollierten Offline-Test von `/tmp/ly_force_musicrate` entwerfen.
- [ ] Musik-Hook erst weiterverfolgen, falls auch Musik betroffen ist; fÃƒÂ¼r Teams den Telefon-/Mikrofonpfad priorisieren.
- [x] Deterministischen SWUpdate-/CPIO-/SquashFS-Repacker gebaut und zweimal offline mit identischem Ergebnis geprÃƒÂ¼ft (0.5.0).
- [ ] Signatur-, PrÃƒÂ¼fsummen- und Bootphasenverhalten vollstÃƒÂ¤ndig dokumentieren.
- [ ] Flash-Chip-Backup und Hardware-Recoveryverfahren entwickeln und verifizieren.
- [ ] Erst danach eine modifizierte Firmware auf einem zweiten Adapter testen.
- [ ] Scharfe Fotos beider Platinenseiten erstellen, um Flash-Zugriff, mÃƒÂ¶gliche Recoverykontakte und Spannungspegel zu bestimmen.

## Erledigt

- [x] 2026-10-25 10:03 CET: Echte UI-Firmware ÃƒÂ¼ber den normalen Updateweg erfolgreich installiert; Originale, Uploadquittung, ZwischenzustÃƒÂ¤nde und Nachher-Dateivergleich lokal archiviert.
- [x] 2026-10-25 10:03 CET: Windows-xfel 1.4.0 samt SHA-256 geprÃƒÂ¼ft; kein FEL-GerÃƒÂ¤t erreichbar. Ein unabhÃƒÂ¤ngiger RÃƒÂ¼ckweg wurde damit nicht bestÃƒÂ¤tigt.
- [x] 2026-10-25 10:03 CET: Lesendes Zwei-Pass-Backupwerkzeug und eng begrenzten Einmal-Uploader mit unabhÃƒÂ¤ngiger MIME-PayloadprÃƒÂ¼fung ergÃƒÂ¤nzt.

- [x] 2026-10-25 08:25 CET: USB-IdentitÃƒÂ¤t und Windows-Treiberstatus erfasst.
- [x] 2026-10-25 08:36 CET: 5-GHz-WLAN und lokalen Verwaltungszugang identifiziert.
- [x] 2026-10-25 08:39 CET: `aud=2` gesetzt und nach Neustart verifiziert.
- [x] 2026-10-25 08:47 CET: WeboberflÃƒÂ¤che, stabile Firmware und Cloud-Testabbild bytegenau archiviert.
- [x] 2026-10-25 08:52 CET: Hersteller-XOR-Transformation reproduziert und beide Abbilder mit eingebetteter MD5-PrÃƒÂ¼fung entschlÃƒÂ¼sselt.
- [x] 2026-10-25 08:54 CET: SWUpdate-Mitglieder und beide SquashFS-Dateisysteme extrahiert.
- [x] 2026-10-25 08:56 CET: Android-Boot-v2-Header, Kernel und Device Tree zerlegt.
- [x] 2026-10-25 08:57 CET: 13 geÃƒÂ¤nderte Dateien zwischen stabiler und Testfirmware identifiziert.
- [x] 2026-10-25 08:58 CET: V821-Plattformpfad, RTL8723FS, 64 MiB RAM und Audio-Gadget-Code belegt.
- [x] 2026-10-25 08:59 CET: Audiomodi und erzwingbare Musik-Abtastrate im BinÃƒÂ¤rcode lokalisiert.
- [x] 2026-10-25 09:00 CET: LogentschlÃƒÂ¼sselung mit Salvage-Modus und Fahrzeug-Erfassungsskript geprÃƒÂ¼ft.
- [x] 2026-10-25 09:00 CET: Projektstand 0.3.0 samt Hashbelegen dokumentiert.
- [x] 2026-10-25 09:05 CET: Versteckten `lylink`-Pack beider Abbilder einschlieÃƒÅ¸lich `rcpservice` und `librcarplay.so` CRC-geprÃƒÂ¼ft extrahiert.
- [x] 2026-10-25 09:07 CET: VollstÃƒÂ¤ndig valide Logrekonstruktion einschlieÃƒÅ¸lich eingebettetem GrÃƒÂ¶ÃƒÅ¸enfeld umgesetzt und Cache-Verhalten aus dem CGI belegt.
- [x] 2026-10-25 09:09 CET: Hyundai-Sonderfall als exakte Kennung `Tinnos / MISTRA` eingegrenzt; kein belegter i30-Fix.
- [x] 2026-10-25 09:11 CET: Sieben PrÃƒÂ¼fungen gegen reale Archive, CRC-FehlerfÃƒÂ¤lle und externe Andes-Instruktionsvektoren bestanden.

