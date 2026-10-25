# Bugs und Auffälligkeiten

Version: 0.7.0  
Stand: 2026-10-25 10:55 CET

## Offen

- Die Wiederverbindung am Windows-PC war nach Stromtrennung verzögert; nach erneutem PC-Anschluss sind WLAN und Gerät wieder erreichbar. Kein fortbestehender Startfehler nachgewiesen.
- Abrupter Stromverlust kann die letzte ungespeicherte Minute verlieren. Ringlogs sind begrenzte Ausschnitte, kein lückenloses Archiv.
- Windows hat globale manuelle WLAN-Adressen; `.2` tauchte zusätzlich zu `.104` wieder auf. Nach Gerätetests auf ursprünglichen DHCP-Betrieb zurückstellen.
- Audioauswertung sieht nur vorhandene Meldungen im letzten passenden Logausschnitt. Fehlende Meldungen sind kein Nachweis eines falschen oder richtigen Audioformats.

- Die neue Oberfläche ist auf einem eigenen Adapter installiert und geprüft. Vollbackup, Hardware-Recovery und Fahrzeug-/Teams-Test stehen weiterhin aus.
- iPhone-/Safari-Endprüfung steht aus; Desktop-Browser auf echter Geräte-Origin wurde erfolgreich geprüft.

- Teams-Anrufe im Hyundai i30 Kombi (2018) sind über den Adapter in beiden Richtungen blechern. Derselbe Teams-Anwendungsfall auf demselben iPhone klingt über direktes USB-Kabel deutlich besser. Ein entsprechender Fehler bei Musik ist nicht bestätigt.
- Die genauen Laufzeitparameter der Modi `aud=0..3` sind noch nicht vollständig einem Fahrzeug-Log und den jeweiligen Audioformaten zugeordnet.
- Es fehlt ein Diagnoseprotokoll aus einem aktiven Teams-Anruf; damit sind die benutzten Telefon-Ein-/Ausgabeformate, Umwandlungen und Pufferparameter noch unbekannt.
- Ein vollständiger Flash-Backup- und Recoveryweg ist noch nicht verifiziert.
- Die Cloud-Testfirmware trägt im Manifest die Kennung `26122515.5234.2`, ihr internes `system.json` jedoch `26051115.5234.2`. Sie darf deshalb nicht als eindeutig freigegebene Zielversion behandelt werden.
- Der CGI-Export cached `/tmp/log.gz`: Mehrere Abrufe nach derselben ersten Erfassung liefern alte Daten. Für jeden Fahrzeugversuch ist vor der Wiedergabe ein Adapterneustart nötig.
- Die Funktionen `UpdateHUSamplerate` und `DisableHUAudioFormat` sind in der stabilen Bibliothek nicht implementiert. Frühere Vermutungen aus ihren Namen sind damit widerlegt.
- Die im Webfrontend vorhandene ADB-Umschaltung wird für Plattform 5234 ausgeblendet und wurde nicht erzwungen.

## Behoben oder geklärt

- 2026-10-25 10:55 CET: Auch echte Stromtrennung bestanden. Nutzer bestätigt erneuten PC-Anschluss, Recorder zählt Boot 3. Beide Boot-1-Logs sind weiterhin SHA-256-identisch und gzip-CRC-gültig. Kaltstart und persistente Speicherung damit auf diesem Adapter belegt.

- 2026-10-25 10:53 CET: 0.7.0 normal gestartet, sieben Webdateihashes passend. Reale 512-KiB-Datenpartition mit zunächst 304 KiB frei, Logger aktiv. CPU-Messung liefert plausible 3,4–6 % statt falscher 100 %. Liveanzeige lief ohne Browseraufzeichnung; Sofortspeicherung und Auswertung gespeicherter Logs funktionieren. Beide Boot-1-Logs nach Software-Neustart unverändert und CRC-geprüft.

- 2026-10-25 10:47 CET: 0.6.0 per eingebettetem GitHub-Updater installiert; sieben statische Dateien und funktionaler CGI bestätigt. Idle-Jiffies blieben trotz laufender Idle-Sekunden stehen. 0.7.0 nutzt zwei Laufzeit-/Idle-Messungen; reale Gegenprobe und Rücksetzfälle sind getestet.
- 2026-10-25 10:47 CET: Liveanzeige startet automatisch, unabhängig von optionaler Browseraufzeichnung.

- 2026-10-25 10:03 CET: Firmware 0.5.0 angenommen, Updaterzustand 2→3 beobachtet, anschließend mit `id=set&conn=cp` normal neu gestartet. Alle sechs neuen/geänderten Webdateien stimmen per SHA-256 mit dem Build überein. Einstellungen `aud=2`, `mic=0`, `sig=149` erhalten; `conn=cp` ist der protokollierte Neustart-/CarPlayaufruf.
- 2026-10-25 10:03 CET: Während des Updates läuft nur die Recovery-Verwaltung mit Versionsanzeige `00000000.5234.2`; fehlende statische Dateien und `no QUERY STRING` waren in dieser Phase kein endgültiger Installationsbefund.
- 2026-10-25 10:03 CET: PC-WLAN musste von APIPA auf eine passende feste Clientadresse umgestellt werden. Eine zusätzlich verbliebene Adresse und zeitweise unbrauchbare Route behinderten den Preflight. Nach Nutzerkorrektur auf `.104` war der Transfer erfolgreich. Kein fehlgeschlagener Preflight hat Firmwarebytes übertragen.
- 2026-10-25 10:03 CET: Funkchip-Aussage korrigiert: Bluetooth-Profil `RTL8723FS`, WLAN-Treiber im Kernel `RTL8733BS`; Platinenbestückung bleibt unbestätigt.

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

