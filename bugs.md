# Bugs und Auffälligkeiten

Version: 0.5.0  
Stand: 2026-10-25 09:36 CET

## Offen

- Der gebaute UI-Kandidat 0.5.0 ist noch nicht auf dem Adapter installiert; Annahme durch den separaten Updater, Recovery und Bootfähigkeit sind unbestätigt. Die lokale Vorschau ist kein Nachweis einer Geräteinstallation.
- Die GitHub-Updateadresse ist in den neuen Webdateien hinterlegt, erreicht das Gerät aber erst mit einer erfolgreichen Erstinstallation. Das erste Manifest ist absichtlich nicht zur Installation freigegeben.
- Browser-/CORS-Endprüfung des späteren echten Firmware-Downloads auf der Geräte-Origin steht aus.

- Teams-Anrufe im Hyundai i30 Kombi (2018) sind über den Adapter in beiden Richtungen blechern. Derselbe Teams-Anwendungsfall auf demselben iPhone klingt über direktes USB-Kabel deutlich besser. Ein entsprechender Fehler bei Musik ist nicht bestätigt.
- Die genauen Laufzeitparameter der Modi `aud=0..3` sind noch nicht vollständig einem Fahrzeug-Log und den jeweiligen Audioformaten zugeordnet.
- Es fehlt ein Diagnoseprotokoll aus einem aktiven Teams-Anruf; damit sind die benutzten Telefon-Ein-/Ausgabeformate, Umwandlungen und Pufferparameter noch unbekannt.
- Ein vollständiger Flash-Backup- und Recoveryweg ist noch nicht verifiziert.
- Die Cloud-Testfirmware trägt im Manifest die Kennung `26122515.5234.2`, ihr internes `system.json` jedoch `26051115.5234.2`. Sie darf deshalb nicht als eindeutig freigegebene Zielversion behandelt werden.
- Der CGI-Export cached `/tmp/log.gz`: Mehrere Abrufe nach derselben ersten Erfassung liefern alte Daten. Für jeden Fahrzeugversuch ist vor der Wiedergabe ein Adapterneustart nötig.
- Die Funktionen `UpdateHUSamplerate` und `DisableHUAudioFormat` sind in der stabilen Bibliothek nicht implementiert. Frühere Vermutungen aus ihren Namen sind damit widerlegt.
- Die im Webfrontend vorhandene ADB-Umschaltung wird für Plattform 5234 ausgeblendet und wurde nicht erzwungen.

## Behoben oder geklärt

- 2026-10-25 09:36 CET: Logo und dunkles Design implementiert; Firmwarecontainer bytegenau rückverpackt und zweimal identisch gebaut. Kernel, `sw-description`, alle 66 ursprünglichen Dateisystemeinträge und `/dev/console` bleiben erhalten; exakt sechs UI-Dateien ändern sich/kommen hinzu.
- 2026-10-25 09:36 CET: Logo liegt unter `/css/`, weil `lyUpdate.sh` beim Start nur `index.html`, `css`, `js`, `lan` und CGI in den aktiven Webroot einbindet. Ein neuer Ordner `/assets/` allein wäre dort nicht erreichbar.
- 2026-10-25 09:36 CET: Vergleichskonstante von Andes BEQC/BNEC korrekt als unsigned 7-Bit dekodiert; Konstanten ab 64 werden nicht mehr irrtümlich negativ dargestellt. Kleine bestehende Audio-Vergleiche bleiben unverändert.

- 2026-10-25 08:39 CET: Audiomodus von `Mode 1` auf den adaptiven `Mode 2` umgestellt und nach Neustart verifiziert.
- 2026-10-25 08:52 CET: Herstellerabbild entschlüsselt, Hersteller-MD5 geprüft und SWUpdate-Container extrahiert.
- 2026-10-25 08:54 CET: SquashFS-Dateisysteme der stabilen und der Testfirmware sicher extrahiert.
- 2026-10-25 08:56 CET: Kernel, Device Tree und Plattformmerkmale aus beiden Bootabbildern gewonnen.
- 2026-10-25 08:58 CET: Die vier Audiomodi als reale, getrennte Programmwerte im RISC-V-Code bestätigt.
- 2026-10-25 08:59 CET: Konkreten Sample-Rate-Hook `/tmp/ly_force_musicrate` und den Aufruf `ForceSetMusicSamplerate()` belegt.
- 2026-10-25 09:00 CET: Reproduzierbares, rein lesendes Erfassungsskript für Fahrzeugtests erfolgreich geprüft.
- 2026-10-25 09:07 CET: Vermeintlich beschädigtes Gerätelog vollständig rekonstruiert. Ursache war ein bisher nicht entferntes vier Byte langes Längenfeld bei Offset `0x333`; gzip-CRC und Endlänge bestehen jetzt vollständig. Frühere Salvage-Klartexte sind historische, unzuverlässige Ableitungen.
- 2026-10-25 09:07 CET: V821B-Untervariante, 16 MiB Flash und vollständige Partitionstabelle direkt im geprüften eigenen Gerätelog bestätigt.
- 2026-10-25 09:05 CET: Zusätzliches `lylink`-Paket beider Updates mit je sechs Dateien entschlüsselt und jede einzelne CRC geprüft.
- 2026-10-25 09:18 CET: Nutzer bestätigt Teams, beide Richtungen und besseren Teams-Klang per Kabel am selben iPhone. Diagnose auf bidirektionalen Telefonpfad eingegrenzt; Musik-Sample-Rate-Hook ist kein belegter Ansatz für diesen Fehler.

