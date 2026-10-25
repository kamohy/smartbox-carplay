# Firmware 0.5.0: Build und Installationsstatus

Stand: 2026-10-25 09:36 CET

**Status: gebaut und offline validiert, nicht geflasht.** Diese Datei beschreibt keinen bestätigten Installationserfolg. Die bisher vereinbarte Voraussetzung eines verifizierten Backups und Recoverywegs ist nicht erfüllt.

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

Der normale Ersttransfer wäre ein multipart-Upload des Images an den bekannten lokalen CGI-Uploadendpunkt. Dieser Schritt kann unmittelbar einen Flash-/Neustartablauf auslösen und wurde noch nicht ausgeführt. Ohne individuellen Dump und getesteten Rückweg würde ein Fehler den Adapter möglicherweise nur mit Hardwarezugriff wiederherstellbar machen.

Für spätere Updates wird das GitHub-Manifest dauerhaft eingebettet. Der erste Eintrag ist `enabled: false`; das ist ein echter gesperrter Kandidat, keine erfundene aktuelle Herstellerfreigabe. Erst Geräteprüfung und anschließende bewusste Manifestfreigabe machen daraus ein regulär angebotenes Update.
