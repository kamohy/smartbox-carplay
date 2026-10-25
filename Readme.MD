# SmartBox CarPlay Adapter Analysis

Version: 0.5.1  
Stand: 2026-10-25 10:03 CET

## Projektvorstellung

Dieses eigenständige Projekt untersucht den günstigen SYACHI 2-in-1 Wireless-CarPlay-/Android-Auto-Adapter (Amazon-ASIN `B0G8YQZWH1`) mit Firmwarefamilie `5234`.

Projektpfad: `E:\WorkSpace\carplay`

Ziel ist, die deutlich schlechtere Audioqualität gegenüber direktem kabelgebundenem CarPlay technisch zu erklären, sichere Verbesserungen zu testen und eine belastbare Grundlage für mögliche Firmwareänderungen zu schaffen.

Fahrzeug laut Nutzer: Hyundai i30 Kombi, Baujahr 2018. Konkret bestätigtes Fehlerbild: Teams-Anrufe klingen in beiden Richtungen blechern. Derselbe Teams-Anwendungsfall am selben iPhone klingt über direktes USB-Kabel deutlich besser. Ein Musikfehler ist damit noch nicht bestätigt. Die genaue Radioausführung und aktive Telefon-Audioformate bleiben offen.

## Aktueller Stand

- Öffentliches Repository: https://github.com/kamohy/smartbox-carplay
- Eigene Oberfläche 0.5.0: dunkles Design und eingebettetes Bad-Hippo-Logo.
- Eigene Firmware `ota/5234/firmware-0.5.0.img` erfolgreich über den Geräte-Updater installiert. Normalstart und alle sechs Webdateien am realen Gerät per SHA-256 geprüft. CarPlay-/Teams-Audio wurde mit dieser UI-Version noch nicht im Fahrzeug geprüft.
- Dauerhafte neue Update-API: https://raw.githubusercontent.com/kamohy/smartbox-carplay/main/ota/5234/version.json
- Der eigene Updatekanal ist jetzt auf dem Adapter installiert; Firmware-UI 0.5.0 und Projekt-/Werkzeugstand 0.5.1 sind getrennt versioniert.

- Installierte Firmware: `26011517.5234.2`
- Plattform direkt im CRC-geprüften Gerätelog bestätigt: Allwinner V821B, 32-Bit RISC-V
- Arbeitsspeicher laut Kernel: 64 MiB
- Bluetooth-Initialisierung: Profil `RTL8723FS`; der Kernel enthält den WLAN-Treiber `RTL8733BS`. Physische Bestückung noch nicht geprüft.
- Flash laut geprüftem Startprotokoll: `xt25p1288`, 16 MiB SPI-NOR
- WLAN: 5 GHz, 802.11n; zuerst Kanal 36 beobachtet, aktuelle Konfiguration meldet Kanal 149
- Lokale Verwaltung: `http://192.168.1.101`
- USB-Emulation: Apple `VID_05AC/PID_12A8`
- Aktueller Audiomodus: Mode 2 (`aud=2`)

Das Hersteller-Update ist entschlüsselt und in SWUpdate, SquashFS, Kernel und Device Tree zerlegt. Zusätzlich ist der darin liegende `lylink`-Pack mit sechs weiteren ELF-Dateien einschließlich `rcpservice` extrahiert; jede Datei besteht ihre ZIP-CRC-Prüfung. Das Update enthält nicht sämtliche Flashpartitionen und ersetzt deshalb kein vollständiges Gerätebackup. Es wurde nichts auf den Adapter geflasht.

## Wichtigster Audiofund

Der Adapter ist kein transparenter Funk-USB-Umsetzer. Seine Firmware:

- erzeugt selbst ein USB-Audiogerät über den Kernel-Treiber `iphone_audio`,
- handelt Musik-, Telefon- und Siri-Audioformate aus,
- besitzt Routinen zum Erzwingen einer Musik-Abtastrate,
- enthält explizite Pfade für `aud=0` bis `aud=3`,
- liest und verwendet die vom Radio gemeldeten Audioformate.

Die sichtbaren Funktionen `UpdateHUSamplerate` und `DisableHUAudioFormat` sind in der stabilen Bibliothek lediglich Platzhalter. Ihre Namen allein belegen keine wirksame Stellschraube.

Für die bestätigten Teams-Anrufe steht jetzt der Telefonpfad im Vordergrund. `lylinkapp` liest eine eigene Telefonrate des Radios und besitzt außerdem bidirektionale Mikrofon-Umwandler mit intern 16 kHz, 16 Bit und Mono. Ob der Teams-Anruf diesen Pfad nutzt und welche Radioformate davor/dahinter stehen, muss ein aktiver Fahrzeuglog belegen. 16-kHz-Mono ist für Sprache nicht automatisch fehlerhaft.

Der ebenfalls gefundene Hook `/tmp/ly_force_musicrate` akzeptiert 44.100 oder 48.000 Hz, betrifft aber Musik. Er ist kein belegter Teams-Fix und hat für den aktuellen Fehler keine Priorität.

## Sicherheitsgrenze

Vollbackup und verifizierter Recoveryweg fehlen weiterhin. Der Nutzer hat am 25.10.2026 Platinenzugang ausgeschlossen und ausdrücklich den Updateweg auch bei möglichem Geräteverlust freigegeben. Auf dieser Grundlage wurde der gezielte UI-Updateversuch erfolgreich durchgeführt. Ein erfolgreicher UI-Flash ist kein Beweis für einen funktionierenden Vollrestore oder eine Audioverbesserung. Die Cloud-Testfirmware wird weiterhin nur offline analysiert.

## Dokumente

- `analysis_report.md`: technischer Gesamtbefund und Optimierungsplan
- `PROJECT_DOCUMENTATION.md`: chronologisches Arbeitsprotokoll
- `porting.md`: Plattform-, Webserver- und Updategrenzen
- `firmware_installation.md`: Build, Updateweg und Installationsstatus
- `todo.md`: offene und erledigte Aufgaben
- `bugs.md`: bekannte Fehler, Risiken und geklärte Punkte
- `evidence/SHA256SUMS.txt`: Hashliste zentraler Original- und Analyseartefakte

## Werkzeuge

- `tools/capture_device_state.ps1`: Status und Diagnoseprotokoll im Fahrzeug lesend sichern
- `tools/decrypt_firmware.py`: Herstellerabbild entschlüsseln und MD5 prüfen
- `tools/build_ui_firmware.py`: UI-Kandidat vollständig offline bauen und unabhängig prüfen
- `tools/smartbox-squashfs`: eng begrenzter SquashFS-Patcher auf Basis von Backhand 0.25.5
- `tools/preview_settings.py`: lokale Vorschau; Gerätestatus lesen, Schreibzugriffe sperren
- `tools/capture_fel_backup.py`: nur lesende FEL-Probe und optional zwei volle 16-MiB-Reads; kein realer Backup-/Restoreerfolg vorhanden
- `tools/upload_ui_candidate.py`: einmaliger, gepinnter Upload mit Preflight und explizitem Risiko-Opt-in; kein automatischer Wiederholungsversuch
- `tools/extract_squashfs.py`: SquashFS ohne unsichere Symlink-Erstellung extrahieren
- `tools/extract_lypack.py`: sechs im `lylink`-Pack enthaltene Programme/Bibliotheken CRC-geprüft extrahieren
- `tools/unpack_android_boot.py`: Android-Boot-v2-Abbild in Kernel und DTB zerlegen
- `tools/decrypt_logcat.py`: XOR und eingebettetes Längenfeld entfernen, vollständige gzip-CRC prüfen
- `tools/compare_binary_strings.py`, `search_binary_strings.py`, `find_string_xrefs.py`: Binäranalyse
- `tools/disassemble_riscv_andes.py`: RISC-V/Andes-Codepfade einschließlich `ADDIGP` untersuchen

## Fahrzeugerfassung

Wichtig: Der Adapter cached den ersten Export in `/tmp/log.gz`. Für jeden neuen Versuch den Adapter zuerst stromlos machen und neu verbinden. Anschließend den Teams-Anruf mit hörbarem Fehler durchführen und erst danach das Log abrufen. Zwischen Neustart und Telefonat keinen früheren Diagnoseexport auslösen.

Während beziehungsweise nach dem Teams-Anruf den PC mit dem Adapter-WLAN verbinden und aus dem Projektordner ausführen:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\tools\capture_device_state.ps1
```

Das Skript schreibt Status, verschlüsseltes Originalprotokoll, CRC-geprüften Klartext, Prüfmetadaten und SHA-256-Werte nach `evidence\logs\<Zeitstempel>`. Ein identischer früherer Export löst eine Cache-Warnung aus. Die A/B-Anleitung und ein iPhone-Downloadweg stehen in `vehicle_test.md`.

Technische Detailbelege: `evidence/audio_code_findings.md`. Regressionsprüfung: `.\.venv\Scripts\python.exe -m unittest discover -s tests -v`.

## Oberfläche und Build

Die lokale Vorschau startet mit `.\.venv\Scripts\python.exe tools/preview_settings.py` unter `http://127.0.0.1:8354`. Sie ist ausdrücklich keine Installation auf dem Adapter. Die ausgelieferte HTML-Datei enthält diesen Vorschau-Sperrcode nicht.

```powershell
cargo build --release --locked --manifest-path tools/smartbox-squashfs/Cargo.toml
.\.venv\Scripts\python.exe tools/build_ui_firmware.py --output dist/new-build
node tests/test_update.js
```

Das lokal gesicherte Original wird anhand seines fest vorgegebenen SHA-256 geprüft. Es wird nicht durch einen fremden Gerätedump ersetzt. Originalfirmware und individuelle Logs sind nicht Teil dieses öffentlichen Repositories. Tests, die solche lokalen Belege benötigen, werden in einem frischen Clone ausdrücklich übersprungen. Das Kandidatenpaket enthält Herstellerprogramme; deren Rechte verbleiben bei den jeweiligen Rechteinhabern. Eigener Code und Firmware-Bestandteile dürfen nicht pauschal als einheitlich neu lizenziert behandelt werden.

