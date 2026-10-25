# SmartBox CarPlay Adapter Analysis

Version: 0.8.2 (Wartungszwischenstand; GerÃƒÆ’Ã‚Â¤te-UI zuletzt 0.7.0)
Stand: 2026-10-25 12:53 CET

Aktueller Auftrag: ausschlieÃƒÆ’Ã…Â¸lich Speicheranzeige einschlieÃƒÆ’Ã…Â¸lich `/tmp`, Fehlerprotokoll und LÃƒÆ’Ã‚Â¶schen der gesicherten eigenen Logs. DafÃƒÆ’Ã‚Â¼r liegt ein getrennter [Wartungszwischenstand 0.8.2](maintenance.md) auf Basis der tatsÃƒÆ’Ã‚Â¤chlich installierten 0.7.0 vor. Die grÃƒÆ’Ã‚Â¶ÃƒÆ’Ã…Â¸ere EinstellungsoberflÃƒÆ’Ã‚Â¤che 0.8.0 wird in diesem Schritt nicht installiert. Das 3.034.669-Byte-Paket enthÃƒÆ’Ã‚Â¤lt nur Customer; die Bootenv-Phasen bleiben erhalten und der Kernel wird nicht mitgeschrieben. Zwei Builds sind identisch; 32 PythonprÃƒÆ’Ã‚Â¼fungen, drei JS-PrÃƒÆ’Ã‚Â¼fprogramme und Shell-/JS-SyntaxprÃƒÆ’Ã‚Â¼fungen bestehen. GerÃƒÆ’Ã‚Â¤tetest lÃƒÆ’Ã‚Â¤uft; Installation und LoglÃƒÆ’Ã‚Â¶schung sind noch nicht bestÃƒÆ’Ã‚Â¤tigt.

Vorheriger Stand: Der erste 0.8.0-Upload wurde bestÃƒÆ’Ã‚Â¤tigt, blieb aber im Vorbereitungszustand. Nach kontrolliertem Neustart lÃƒÆ’Ã‚Â¤uft weiterhin 0.7.0; der ÃƒÆ’Ã‚Â¶ffentliche 0.8.0-Updateeintrag ist bis zum GerÃƒÆ’Ã‚Â¤tetest deaktiviert. Logs sind lokal gesichert, LÃƒÆ’Ã‚Â¶schung auf dem GerÃƒÆ’Ã‚Â¤t noch offen. FÃƒÆ’Ã‚Â¼r die Audioanalyse ist zusÃƒÆ’Ã‚Â¤tzlich eine [eng begrenzte Offline-Messstelle](phone_probe.md) vorbereitet: FÃƒÆ’Ã‚Â¤higkeitsmaske und VersionsprÃƒÆ’Ã‚Â¼fwert werden protokolliert, ohne die Audioauswahl zu ÃƒÆ’Ã‚Â¤ndern. Kein neues GerÃƒÆ’Ã‚Â¤teimage 0.8.1 und kein Flash dieses Diagnosekandidaten.

0.8.0 ergÃƒÆ’Ã‚Â¤nzt verstÃƒÆ’Ã‚Â¤ndliche Einstellungen: LED-Ein/Aus-Schalter, erklÃƒÆ’Ã‚Â¤rte Telefonpuffer-Profile, Verbindungsstart mit belegter 20-Sekunden-Option und klar benannter ungeklÃƒÆ’Ã‚Â¤rter Herstelleralternative. Hardware-/Grenzenkarte, feste Hardwareabfrage, korrigierte Mikrofoneinheit, getrennte NetzwerkzÃƒÆ’Ã‚Â¤hler und begrenzte LoglÃƒÆ’Ã‚Â¶schung sind ergÃƒÆ’Ã‚Â¤nzt. Zwei identische Builds und 27 PythonprÃƒÆ’Ã‚Â¼fungen sowie drei JavaScript-PrÃƒÆ’Ã‚Â¼fprogramme bestehen. GerÃƒÆ’Ã‚Â¤teinstallation und LÃƒÆ’Ã‚Â¶schprÃƒÆ’Ã‚Â¼fung stehen fÃƒÆ’Ã‚Â¼r diese Version noch aus. Aktuelle Logs wurden zuvor separat CRC-/SHA-256-geprÃƒÆ’Ã‚Â¼ft lokal gesichert.

Erster Fahrzeuglog ausgewertet: Bei Teams fordert das iPhone in Mode 2 und Mode 3 16 kHz an, der Telefonpfad zum Radio lÃƒÆ’Ã‚Â¤uft jedoch mit 8 kHz. Die Mikrofonumwandlung 8 ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ 16 kHz ist ebenfalls protokolliert. Der Moduswechsel verbessert laut Nutzer den Klang, die DÃƒÆ’Ã‚Â¤mpfung bleibt. Eine feste Hardwaregrenze ist noch nicht bewiesen; die Firmware besitzt eine von RadiofÃƒÆ’Ã‚Â¤higkeiten und Plugin-Version abhÃƒÆ’Ã‚Â¤ngige 16-kHz-Auswahl. [Feldtest und Grenzen](field_test_2026-10-25.md). Kein neuer Flash in diesem Analyseblock.

0.7.0 ist ÃƒÆ’Ã‚Â¼ber den eigenen Browser-Updater installiert und direkt am GerÃƒÆ’Ã‚Â¤t geprÃƒÆ’Ã‚Â¼ft: automatische Livewerte alle zwei Sekunden, korrigierte CPU-Berechnung und begrenzte, komprimierte Systemlogs. Datenpartition: tatsÃƒÆ’Ã‚Â¤chlich 512 KiB, nach dem ersten Log 304 KiB frei. Logger und Sofortspeicherung funktionieren. Zwei Logs ÃƒÆ’Ã‚Â¼berstanden sowohl einen Software-Neustart als auch tatsÃƒÆ’Ã‚Â¤chliche Stromtrennung mit erneutem PC-Anschluss byteidentisch. Details: [diagnostics.md](diagnostics.md).

## Projektvorstellung

Dieses eigenstÃƒÆ’Ã‚Â¤ndige Projekt untersucht den gÃƒÆ’Ã‚Â¼nstigen SYACHI 2-in-1 Wireless-CarPlay-/Android-Auto-Adapter (Amazon-ASIN `B0G8YQZWH1`) mit Firmwarefamilie `5234`.

Projektpfad: `E:\WorkSpace\carplay`

Ziel ist, die deutlich schlechtere AudioqualitÃƒÆ’Ã‚Â¤t gegenÃƒÆ’Ã‚Â¼ber direktem kabelgebundenem CarPlay technisch zu erklÃƒÆ’Ã‚Â¤ren, sichere Verbesserungen zu testen und eine belastbare Grundlage fÃƒÆ’Ã‚Â¼r mÃƒÆ’Ã‚Â¶gliche FirmwareÃƒÆ’Ã‚Â¤nderungen zu schaffen.

Fahrzeug laut Nutzer: Hyundai i30 Kombi, Baujahr 2018. Konkret bestÃƒÆ’Ã‚Â¤tigtes Fehlerbild: Teams-Anrufe klingen in beiden Richtungen blechern. Derselbe Teams-Anwendungsfall am selben iPhone klingt ÃƒÆ’Ã‚Â¼ber direktes USB-Kabel deutlich besser. Ein Musikfehler ist damit noch nicht bestÃƒÆ’Ã‚Â¤tigt. Die genaue RadioausfÃƒÆ’Ã‚Â¼hrung und aktive Telefon-Audioformate bleiben offen.

## Aktueller Stand

- ÃƒÆ’Ã¢â‚¬â€œffentliches Repository: https://github.com/kamohy/smartbox-carplay
- Eigene OberflÃƒÆ’Ã‚Â¤che: dunkles Design, eingebettetes Bad-Hippo-Logo und integrierte Diagnosewerkzeuge.
- Diagnose 0.7.0: automatische CPU/RAM/Laufzeit/USB-Anzeige, WLAN-ZÃƒÆ’Ã‚Â¤hler, optionale Browseraufzeichnung, persistente Systemlogs und Auswertung vorhandener Telefon-/Mikrofonmeldungen. Keine Messung hÃƒÆ’Ã‚Â¶rbarer KlangqualitÃƒÆ’Ã‚Â¤t.
- Eigene Firmware `ota/5234/firmware-0.7.0.img` erfolgreich ÃƒÆ’Ã‚Â¼ber den GerÃƒÆ’Ã‚Â¤te-Updater installiert. Normalstart und sieben statische Webdateihashes sowie CGI/Recorder am realen GerÃƒÆ’Ã‚Â¤t geprÃƒÆ’Ã‚Â¼ft. CarPlay-/Teams-Audio bleibt im Fahrzeug zu prÃƒÆ’Ã‚Â¼fen.
- Dauerhafte neue Update-API: https://raw.githubusercontent.com/kamohy/smartbox-carplay/main/ota/5234/version.json
- Der eigene Updatekanal ist auf dem Adapter installiert; Herstellerkennung und eigene UI-Version sind getrennt.

- Installierte Firmware: `26011517.5234.2`
- Plattform direkt im CRC-geprÃƒÆ’Ã‚Â¼ften GerÃƒÆ’Ã‚Â¤telog bestÃƒÆ’Ã‚Â¤tigt: Allwinner V821B, 32-Bit RISC-V
- Arbeitsspeicher laut Kernel: 64 MiB
- Bluetooth-Initialisierung: Profil `RTL8723FS`; der Kernel enthÃƒÆ’Ã‚Â¤lt den WLAN-Treiber `RTL8733BS`. Physische BestÃƒÆ’Ã‚Â¼ckung noch nicht geprÃƒÆ’Ã‚Â¼ft.
- Flash laut geprÃƒÆ’Ã‚Â¼ftem Startprotokoll: `xt25p1288`, 16 MiB SPI-NOR
- WLAN: 5 GHz, 802.11n; zuerst Kanal 36 beobachtet, aktuelle Konfiguration meldet Kanal 149
- Lokale Verwaltung: `http://192.168.1.101`
- USB-Emulation: Apple `VID_05AC/PID_12A8`
- Aktueller Audiomodus: Mode 2 (`aud=2`)

Das Hersteller-Update ist entschlÃƒÆ’Ã‚Â¼sselt und in SWUpdate, SquashFS, Kernel und Device Tree zerlegt. ZusÃƒÆ’Ã‚Â¤tzlich ist der darin liegende `lylink`-Pack mit sechs weiteren ELF-Dateien einschlieÃƒÆ’Ã…Â¸lich `rcpservice` extrahiert; jede Datei besteht ihre ZIP-CRC-PrÃƒÆ’Ã‚Â¼fung. Das Update enthÃƒÆ’Ã‚Â¤lt nicht sÃƒÆ’Ã‚Â¤mtliche Flashpartitionen und ersetzt deshalb kein vollstÃƒÆ’Ã‚Â¤ndiges GerÃƒÆ’Ã‚Â¤tebackup. Eigene OberflÃƒÆ’Ã‚Â¤chen 0.5.0 und 0.6.0 wurden installiert; Audiobibliotheken wurden dabei nicht verÃƒÆ’Ã‚Â¤ndert.

## Wichtigster Audiofund

Der Adapter ist kein transparenter Funk-USB-Umsetzer. Seine Firmware:

- erzeugt selbst ein USB-AudiogerÃƒÆ’Ã‚Â¤t ÃƒÆ’Ã‚Â¼ber den Kernel-Treiber `iphone_audio`,
- handelt Musik-, Telefon- und Siri-Audioformate aus,
- besitzt Routinen zum Erzwingen einer Musik-Abtastrate,
- enthÃƒÆ’Ã‚Â¤lt explizite Pfade fÃƒÆ’Ã‚Â¼r `aud=0` bis `aud=3`,
- liest und verwendet die vom Radio gemeldeten Audioformate.

Die sichtbaren Funktionen `UpdateHUSamplerate` und `DisableHUAudioFormat` sind in der stabilen Bibliothek lediglich Platzhalter. Ihre Namen allein belegen keine wirksame Stellschraube.

FÃƒÆ’Ã‚Â¼r die bestÃƒÆ’Ã‚Â¤tigten Teams-Anrufe steht jetzt der Telefonpfad im Vordergrund. `lylinkapp` liest eine eigene Telefonrate des Radios und besitzt auÃƒÆ’Ã…Â¸erdem bidirektionale Mikrofon-Umwandler mit intern 16 kHz, 16 Bit und Mono. Ob der Teams-Anruf diesen Pfad nutzt und welche Radioformate davor/dahinter stehen, muss ein aktiver Fahrzeuglog belegen. 16-kHz-Mono ist fÃƒÆ’Ã‚Â¼r Sprache nicht automatisch fehlerhaft.

Der ebenfalls gefundene Hook `/tmp/ly_force_musicrate` akzeptiert 44.100 oder 48.000 Hz, betrifft aber Musik. Er ist kein belegter Teams-Fix und hat fÃƒÆ’Ã‚Â¼r den aktuellen Fehler keine PrioritÃƒÆ’Ã‚Â¤t.

## Sicherheitsgrenze

Vollbackup und verifizierter Recoveryweg fehlen weiterhin. Der Nutzer hat am 25.10.2026 Platinenzugang ausgeschlossen und ausdrÃƒÆ’Ã‚Â¼cklich den Updateweg auch bei mÃƒÆ’Ã‚Â¶glichem GerÃƒÆ’Ã‚Â¤teverlust freigegeben. Auf dieser Grundlage wurde der gezielte UI-Updateversuch erfolgreich durchgefÃƒÆ’Ã‚Â¼hrt. Ein erfolgreicher UI-Flash ist kein Beweis fÃƒÆ’Ã‚Â¼r einen funktionierenden Vollrestore oder eine Audioverbesserung. Die Cloud-Testfirmware wird weiterhin nur offline analysiert.

## Dokumente

- `analysis_report.md`: technischer Gesamtbefund und Optimierungsplan
- `PROJECT_DOCUMENTATION.md`: chronologisches Arbeitsprotokoll
- `porting.md`: Plattform-, Webserver- und Updategrenzen
- `firmware_installation.md`: Build, Updateweg und Installationsstatus
- `diagnostics.md`: Bedienung, Messumfang und Grenzen der Diagnosewerkzeuge
- `field_test_2026-10-25.md`: erster Teams-Fahrzeuglog, 8-kHz-Engpass und nÃƒÆ’Ã‚Â¤chste gezielte PrÃƒÆ’Ã‚Â¼fung
- `todo.md`: offene und erledigte Aufgaben
- `bugs.md`: bekannte Fehler, Risiken und geklÃƒÆ’Ã‚Â¤rte Punkte
- `evidence/SHA256SUMS.txt`: Hashliste zentraler Original- und Analyseartefakte

## Werkzeuge

- `tools/capture_device_state.ps1`: Status und Diagnoseprotokoll im Fahrzeug lesend sichern
- `tools/analyze_field_logs.py`: persistente Snapshots offline prÃƒÆ’Ã‚Â¼fen, pro Start deduplizieren und Telefon-/USB-/Mikrofonformate getrennt auswerten
- `tools/decrypt_firmware.py`: Herstellerabbild entschlÃƒÆ’Ã‚Â¼sseln und MD5 prÃƒÆ’Ã‚Â¼fen
- `tools/build_ui_firmware.py`: UI-Kandidat vollstÃƒÆ’Ã‚Â¤ndig offline bauen und unabhÃƒÆ’Ã‚Â¤ngig prÃƒÆ’Ã‚Â¼fen
- `tools/smartbox-squashfs`: eng begrenzter SquashFS-Patcher auf Basis von Backhand 0.25.5
- `tools/preview_settings.py`: lokale Vorschau; GerÃƒÆ’Ã‚Â¤testatus lesen, Schreibzugriffe sperren
- `tools/capture_fel_backup.py`: nur lesende FEL-Probe und optional zwei volle 16-MiB-Reads; kein realer Backup-/Restoreerfolg vorhanden
- `tools/upload_ui_candidate.py`: einmaliger, gepinnter Upload mit Preflight und explizitem Risiko-Opt-in; kein automatischer Wiederholungsversuch
- `tools/extract_squashfs.py`: SquashFS ohne unsichere Symlink-Erstellung extrahieren
- `tools/extract_lypack.py`: sechs im `lylink`-Pack enthaltene Programme/Bibliotheken CRC-geprÃƒÆ’Ã‚Â¼ft extrahieren
- `tools/unpack_android_boot.py`: Android-Boot-v2-Abbild in Kernel und DTB zerlegen
- `tools/decrypt_logcat.py`: XOR und eingebettetes LÃƒÆ’Ã‚Â¤ngenfeld entfernen, vollstÃƒÆ’Ã‚Â¤ndige gzip-CRC prÃƒÆ’Ã‚Â¼fen
- `tools/compare_binary_strings.py`, `search_binary_strings.py`, `find_string_xrefs.py`: BinÃƒÆ’Ã‚Â¤ranalyse
- `tools/disassemble_riscv_andes.py`: RISC-V/Andes-Codepfade einschlieÃƒÆ’Ã…Â¸lich `ADDIGP` untersuchen

## Fahrzeugerfassung

Mit 0.7.0 lÃƒÆ’Ã‚Â¤uft der native Recorder ohne offene Webseite. Nach dem Teams-Test noch etwa eine Minute eingeschaltet lassen. Logs fÃƒÆ’Ã‚Â¼r bis zu drei GerÃƒÆ’Ã‚Â¤testarts kÃƒÆ’Ã‚Â¶nnen spÃƒÆ’Ã‚Â¤ter am PC von der Einstellungsseite geladen werden. Die letzte ungespeicherte Minute kann beim Abziehen fehlen. Der folgende ÃƒÆ’Ã‚Â¤ltere PC-Erfassungsweg verwendet weiterhin den OEM-Export; die frischen eigenen Downloads sind davon unabhÃƒÆ’Ã‚Â¤ngig.

Wichtig: Der Adapter cached den ersten Export in `/tmp/log.gz`. FÃƒÆ’Ã‚Â¼r jeden neuen Versuch den Adapter zuerst stromlos machen und neu verbinden. AnschlieÃƒÆ’Ã…Â¸end den Teams-Anruf mit hÃƒÆ’Ã‚Â¶rbarem Fehler durchfÃƒÆ’Ã‚Â¼hren und erst danach das Log abrufen. Zwischen Neustart und Telefonat keinen frÃƒÆ’Ã‚Â¼heren Diagnoseexport auslÃƒÆ’Ã‚Â¶sen.

WÃƒÆ’Ã‚Â¤hrend beziehungsweise nach dem Teams-Anruf den PC mit dem Adapter-WLAN verbinden und aus dem Projektordner ausfÃƒÆ’Ã‚Â¼hren:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\tools\capture_device_state.ps1
```

Das Skript schreibt Status, verschlÃƒÆ’Ã‚Â¼sseltes Originalprotokoll, CRC-geprÃƒÆ’Ã‚Â¼ften Klartext, PrÃƒÆ’Ã‚Â¼fmetadaten und SHA-256-Werte nach `evidence\logs\<Zeitstempel>`. Ein identischer frÃƒÆ’Ã‚Â¼herer Export lÃƒÆ’Ã‚Â¶st eine Cache-Warnung aus. Die A/B-Anleitung und ein iPhone-Downloadweg stehen in `vehicle_test.md`.

Technische Detailbelege: `evidence/audio_code_findings.md`. RegressionsprÃƒÆ’Ã‚Â¼fung: `.\.venv\Scripts\python.exe -m unittest discover -s tests -v`.

## OberflÃƒÆ’Ã‚Â¤che und Build

Die lokale Vorschau startet mit `.\.venv\Scripts\python.exe tools/preview_settings.py` unter `http://127.0.0.1:8354`. Sie ist ausdrÃƒÆ’Ã‚Â¼cklich keine Installation auf dem Adapter. Die ausgelieferte HTML-Datei enthÃƒÆ’Ã‚Â¤lt diesen Vorschau-Sperrcode nicht.

```powershell
cargo build --release --locked --manifest-path tools/smartbox-squashfs/Cargo.toml
.\.venv\Scripts\python.exe tools/build_ui_firmware.py --output dist/new-build
node tests/test_update.js
```

Das lokal gesicherte Original wird anhand seines fest vorgegebenen SHA-256 geprÃƒÆ’Ã‚Â¼ft. Es wird nicht durch einen fremden GerÃƒÆ’Ã‚Â¤tedump ersetzt. Originalfirmware und individuelle Logs sind nicht Teil dieses ÃƒÆ’Ã‚Â¶ffentlichen Repositories. Tests, die solche lokalen Belege benÃƒÆ’Ã‚Â¶tigen, werden in einem frischen Clone ausdrÃƒÆ’Ã‚Â¼cklich ÃƒÆ’Ã‚Â¼bersprungen. Das Kandidatenpaket enthÃƒÆ’Ã‚Â¤lt Herstellerprogramme; deren Rechte verbleiben bei den jeweiligen Rechteinhabern. Eigener Code und Firmware-Bestandteile dÃƒÆ’Ã‚Â¼rfen nicht pauschal als einheitlich neu lizenziert behandelt werden.

