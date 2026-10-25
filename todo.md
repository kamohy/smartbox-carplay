# Aufgaben

Version: 0.5.0  
Stand: 2026-10-25 09:36 CET

## Oberfläche und eigener Updatekanal

- [x] Bad-Hippo-SVG einbetten; Oberfläche und Dialoge dunkel gestalten.
- [x] Öffentliches GitHub-Repository `kamohy/smartbox-carplay` anlegen; Geräteexporte ausschließen.
- [x] Herstellerquelle und tatsächlichen Browser-Download-/Uploadablauf identifizieren.
- [x] Dauerhafte GitHub-Updateadresse in eigene Firmware aufnehmen; keine DNS-/TLS-Umleitung nötig.
- [x] UI-Kandidat 0.5.0 bauen, zweimal reproduzieren und alle originalen Inodes sowie Kernel unabhängig abgleichen.
- [x] Eigenen Updater gegen falsche Plattform, falschen Downloadpfad, beschädigte Nutzlast und nicht freigegebene Pakete prüfen.
- [ ] Vollbackup und Recovery verifizieren, bevor der bislang ungeprüfte Kandidat geflasht wird.
- [ ] Den eigenen `/sbin/update`-/Recovery-Prüfpfad vollständig untersuchen; neu berechnete MD5/CPIO-Prüfsummen allein beweisen keine Annahme durch den Geräte-Updater.
- [ ] Erstinstallation, anschließenden Start und dauerhafte Auslieferung der neuen Oberfläche direkt am Adapter verifizieren.
- [ ] GitHub-/CORS-Download unter Safari und unter der echten Geräte-HTTP-Origin end-to-end prüfen.
- [ ] Nach Geräteprüfung eine installierbare Version über `enabled: true` freigeben.

## Nächster sicherer Schritt

- [ ] Vor jedem Fahrzeugtest Adapter stromlos neu starten; erst nach dem hörbar betroffenen Teams-Anruf den ersten Logexport auslösen, um den CGI-Cache zu umgehen.
- [ ] Teams-Anruf im Hyundai i30 Kombi (2018) mit `Mode 2` protokollieren: Telefonraten, Aufnahme/Wiedergabe, Formate und Resampler.
- [ ] Als Abgrenzung einen normalen Telefonanruf über den Adapter prüfen: ebenfalls beidseitig blechern oder nur Teams?
- [ ] Musik zusätzlich als Kontrolle prüfen; derzeit ist nur der Teams-Fehler ausdrücklich bestätigt.
- [ ] Prüfen, ob das Radio parallel direkt per Bluetooth mit dem iPhone verbunden ist; nur diese Verbindung für den Vergleich trennen, Bluetooth und die SmartBox-Kopplung am iPhone eingeschaltet lassen.
- [ ] Nach dem ersten Telefonlog einen gezielten Modusvergleich planen. Im bereits nachvollzogenen Telefon-Pufferpfad verhalten sich 1/2/3 gleich; Default vs. Mode 2 ist dort der tatsächlich sichtbare Unterschied.
- [ ] Telefon-Ein-/Ausgaberaten und interne 16-kHz-Mono-Umwandlung sowie Fehlermeldungen gegenüberstellen.
- [ ] Gemeldeten HU-Hersteller und Modellkennung aus dem Fahrzeuglog ermitteln und auf den tatsächlichen Modellpfad abbilden.
- [ ] Bei Teams ist ein Sprach-/Telefonpfad erwartbar; Mono oder 16 kHz allein beweisen keinen Fehler. Die konkrete Verschlechterung gegenüber Kabel muss durch ausgehandelte Formate/Verarbeitung erklärt werden.

## Firmwareforschung

- [ ] Startskript-Modifikation für einen ausschließlich kontrollierten Offline-Test von `/tmp/ly_force_musicrate` entwerfen.
- [ ] Musik-Hook erst weiterverfolgen, falls auch Musik betroffen ist; für Teams den Telefon-/Mikrofonpfad priorisieren.
- [ ] Einen deterministischen SWUpdate-/CPIO-/SquashFS-Repacker bauen und ausschließlich offline gegen entpackte Kopien prüfen.
- [ ] Signatur-, Prüfsummen- und Bootphasenverhalten vollständig dokumentieren.
- [ ] Flash-Chip-Backup und Hardware-Recoveryverfahren entwickeln und verifizieren.
- [ ] Erst danach eine modifizierte Firmware auf einem zweiten Adapter testen.
- [ ] Scharfe Fotos beider Platinenseiten erstellen, um Flash-Zugriff, mögliche Recoverykontakte und Spannungspegel zu bestimmen.

## Erledigt

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

