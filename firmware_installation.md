# Firmware: Build und Installationsstatus

Dokumentstand: 0.7.0 / 2026-10-25 10:47 CET

0.7.0 ergänzt automatische Livewerte und begrenzten nativen Logrecorder. Paket: `ota/5234/firmware-0.7.0.img`, 6.199.341 Byte, SHA-256 `32e395c7ff22fcf40eb019748126e554694786974d261f70ab4fe07171e6aeb4`. Reproduzierbarer Zweitbuild und lokale Prüfungen bestanden; Installation/Persistenztest stehen noch aus. Der Builder erlaubt nun zehn Dateien, darunter exakt zwei native Recorder-Startpfade. Alle anderen Originaldateien bleiben erhalten.

0.6.0 wurde inzwischen per echtem Browser-Updater installiert. Normalstart, sieben statische Webdateien und CGI-Endpunkte sind geprüft. Die CPU-Jiffies-Anzeige war fehlerhaft; 0.7.0 enthält den anhand realer Messdaten geprüften Fix. Nachfolgend bleibt der historische Ersttransfer 0.5.0 dokumentiert; die alten Angaben zu sechs Dateien betreffen ausschließlich 0.5.0.

**Status: auf dem eigenen ly5234-Adapter installiert und im Normalstart geprüft.** Der Nutzer hat den Versuch ausdrücklich ohne vollständiges Backup/Recovery und mit akzeptiertem Geräteverlust freigegeben. Das ist kein geprüfter Rückweg und kein bestätigter Audio-Fix.

Kandidat: `ota/5234/firmware-0.5.0.img`, 6.187.053 Byte. SHA-256: `3b1d45b1ca75b9462bfc53974b5d34c6f28aef9b4f0761c746f1cb0923074581`.

Enthalten: dunkle Weboberfläche, lokal gespeichertes Bad-Hippo-Logo und eigener öffentlicher GitHub-Updatekanal. Kein bestätigter Audio-Fix. Installierte Herstellerkennung wird nicht künstlich umdatiert; die eigene UI-Version ist separat 0.5.0.

Das Original `update.img` muss lokal unter `evidence/firmware/26011517.5234.2/` liegen und SHA-256 `7afff8e6a6387662aa10d84d5f8745e8406b91fb704aa4942f6e416393b10f63` besitzen. Abhängigkeiten: Python mit `requirements-analysis.txt` und Rust/Cargo. Das Cargo-Lockfile ist mitzuliefern.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-analysis.txt
cargo build --release --locked --manifest-path tools/smartbox-squashfs/Cargo.toml
.\.venv\Scripts\python.exe tools/build_ui_firmware.py --output dist/new-build
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
node tests/test_update.js
```

Der Builder verändert ausschließlich eine Kopie. Er implementiert keinen Upload. Der erzeugte Bericht nennt alle sechs geänderten/ergänzten Webdateien, Original-/Zielhash, Partitionsgrenzen und die fehlende Geräteprüfung. Er bricht bei unerwarteten Änderungen außerhalb der Oberfläche ab.

Der Ersttransfer war ein einmaliger multipart-Upload an den bekannten lokalen CGI-Uploadendpunkt. Um 09:59:44 CET bestätigte der Adapter `upload successful`. Es folgten Zustand 2, Zustand 3 und erst danach der normale Neustart. Alle sechs Webdateien wurden anschließend direkt vom Gerät per SHA-256 geprüft. `aud=2`, `mic=0` und `sig=149` blieben erhalten; der Neustart setzt `conn=cp`. Individuelle Originalbelege liegen lokal unter `evidence/updates/2026-10-25-095944/`.

Das GitHub-Manifest ist dauerhaft eingebettet. Der erste Eintrag wurde nach dem Gerätevergleich für die eigene Oberfläche freigegeben. Der eigene Updater vergleicht die separate UI-Version; die unveränderte Herstellerbasis bleibt `26011517.5234.2`. Eine zukünftige Erweiterung benötigt einen neuen Build, ein neues SHA-256 und eine höhere UI-Version.
