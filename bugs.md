# Bugs und Auffälligkeiten

## Aktueller Auftrag: verständliche Oberfläche 0.9.0

Stand: 2026-10-25T14:25:58+01:00

Prüfnachweis 2026-10-25T14:28:48+01:00: 34 lokale Pythonprüfungen und vier JS-Prüfprogramme erfolgreich; CI 40197644303 erfolgreich. Browser-Vorschau bestätigt Beschriftungen und LED-Schalter. Öffentliche Version 0.9.0 ist freigegeben; der reale HTTP-Header der Manifestdatei nennt Cache-Control: max-age=300. Das Handy zeigte noch die ältere gesperrte 0.8.3. Geräteinstallation bleibt offen, kein paralleler PC-Upload gestartet.

Der Nutzer meldete einen erfolgreichen Updateknopfdruck, vermutlich am Handy. Direkte Prüfung in diesem Arbeitsblock zeigt jedoch noch UI 0.7.0 und Updatezustand 0; id=space ist dort unbekannt. Ein erfolgreich installierter Zwischenstand 0.8.3 ist damit nicht bestätigt. Der genaue Auslöser des bisherigen Vorbereitungsfehlers bleibt offen; der Knopfdruck allein beweist keine abgeschlossene Installation.

0.9.0 führt die vorbereiteten verständlichen Einstellungen und die neueren Wartungskorrekturen zusammen: LED 0=Ein/1=Aus als Schalter mit Rücklesekontrolle, Telefonpuffer statt anonymer Mode-Bezeichnung, erklärte Startverzögerung (20 Sekunden für delay=2 belegt), GPS-Option ehrlich als teilweise ungeklärt. Die drei Telefonprofile bleiben unterscheidbar, ihre noch ungeklärten Unterschiede werden ausdrücklich genannt; es werden keine Qualitätsstufen erfunden. Der Resetknopf beschreibt nun korrekt die Löschung der ganzen Datenpartition einschließlich Kopplungen und verlangt eine Bestätigung.

Technikübersicht: Allwinner V821B/RISC-V, 64 MiB physischer RAM, 16 MiB SPI-NOR, 512 KiB persistente Datenpartition, belegte Realtek-Treiber-/Profilnamen mit Nachweisgrenzen. Die neue feste Liveabfrage trennt freien Datenspeicher, RAM, /tmp und schreibgeschützte Firmwarebereiche. Keine Addition überlappender RAM-/tmp-Kapazitäten. Hardware-Rohabfrage und begrenzter Fehlerauszug sind integriert. Logger läuft aus RAM und beendet sich bei erkanntem Updatebeginn.

Image: 6203437 Byte; SHA-256 `7c72d07dd55e24ac7dc641649f39a81a2624f379f1fdbfa947fbc9734fb95cb8`. Kernel und Updatebeschreibung unverändert; 12 ausdrücklich erlaubte Pfade, alle anderen ursprünglichen Inodes/Daten unabhängig geprüft. Der vollständige Herstellercontainer schreibt den unveränderten Kernel erneut. Keine Änderung an Telefon-Audioalgorithmus, CPU-Takt, Partitionslayout oder WLAN-Konfiguration. Der bestehende öffentliche Kanal bietet 0.9.0 für die ausdrücklich beauftragte Geräteprüfung an; Installation und Bedienung am Dongle sind noch zu verifizieren. Alte Fahrzeuglogs bleiben lokal gesichert. Ältere folgende Abschnitte dokumentieren die Historie.

Version: 0.9.0 (Geräteinstallation noch zu bestätigen)
Stand: 2026-10-25T14:25:58+01:00

Abschließender Gerätestand: Beide gezielt geänderten 0.8.3-Versuche (vor und nach dem freigegebenen Datenreset) blieben nach angenommenem Upload in Zustand 1. Nach jeweils kontrolliertem Neustart ist UI 0.7.0/Updatezustand 0 bestätigt. Die neue Oberfläche ist nicht installiert; es erfolgt kein weiterer unveränderter Upload. Letzte freie Kapazität nach neuer Aufzeichnung: 276/512 KiB; direkt nach dem Reset waren es 304 KiB. Die alten erreichbaren Logs sind entfernt und alle ursprünglichen Fahrzeuglogs lokal gesichert.

Aktueller Stand 0.8.3: Der Wartungskandidat startet den Recorder aus RAM mit Arbeitsverzeichnis / und beendet ihn bei aktivem Update. Das originale vollständige Updateformat einschließlich bytegleichem Kernel und unveränderter Beschreibung bleibt erhalten. Zwei Builds sind identisch; 34 lokale Pythonprüfungen und die drei bisherigen JS-Prüfprogramme bestehen. Geräteinstallation ist noch nicht bestätigt; installiert bleibt zuletzt UI 0.7.0. Nach ausdrücklicher Zustimmung wurde der gesamte UDISK-Inhalt einschließlich Kopplungen über rst=1 gelöscht. Alte erreichbare Logs sind entfernt und lokal gesichert; 304 statt 224 KiB frei. Neun verglichene Einstellungen sind unverändert. Der Logger legt bereits neue Dateien an.


## Historie vor der Datenlöschung

Der Nutzer begrenzte den damaligen Schritt auf Speichermessung, Fehlerprotokoll und Loglöschung. Der zweite 0.8.0-Vollpaketversuch nach bestätigtem Netzteilanschluss wurde ebenfalls angenommen, blieb aber in Zustand 1. Normaler API-Neustart stellte 0.7.0/Updatezustand 0 wieder her. Kein Beleg für ein Netzteilproblem. Zuletzt vor diesem Neustart: 23.820 KiB RAM verfügbar, 204/512 KiB im Logspeicher frei. Freier temporärer Dateisystemplatz ist damit noch nicht gemessen. Der Wartungskandidat 0.8.2 soll diese Lücke mit einem deutlich kleineren Customer-only-Paket schließen; Auch dieses Paket blieb vier Minuten in Zustand 1 ohne Abschluss. Nach kontrolliertem Neustart wurde UI 0.7.0/Updatezustand 0 direkt bestätigt. Der Löschaufruf wird mit HTTP 405 abgewiesen; Loglöschung ist noch offen.

Die HTTP-Beobachtung erhielt einmal eine fehlerhafte Statuszeile. Das belegt keinen Firmwarefehler oder fehlgeschlagenen Upload; anschließende direkte Abfragen meldeten weiter Zustand 1. Die Beobachtung wurde ohne erneuten POST fortgesetzt.

Die ergänzte Telefon-Messstelle 0.8.1 ist ausschließlich offline geprüft und nicht im 0.8.0-Image enthalten. Hardware-/Loglöschendpunkte und LED-Schalter sind weiterhin erst nach erfolgreicher Geräteinstallation verifizierbar.

0.8.0 ist offline geprüft, noch nicht auf dem Gerät verifiziert. Es behebt die falsche Mikrofoneinheit im Webparser und die ausschließliche Anzeige eines einzelnen Netzwerkinterfaces. Die nachfolgenden Einträge zu UI 0.7.0 bleiben bis zum echten Versionsvergleich gültig.

## Offen

- 0.8.0-Erstversuch: Upload bestätigt, aber Zustand 1 blieb bestehen; keine Recovery-/Abschlussphase beobachtet. Kontrollierter API-Neustart führte zurück zu normaler UI 0.7.0. Öffentlicher 0.8.0-Kanal bis erneuter Geräteprüfung deaktiviert. LED-Schalter und Löschfunktion noch nicht live verifiziert; Logs sind lokal gesichert.

- Teams-Feldtest belegt 8-kHz-Telefonpfad trotz 16-kHz-iPhone-Anfrage, in Mode 2 und 3. Das passt zur verbleibenden Dämpfung. Auswahlursache und tatsächliche 16-kHz-Fähigkeiten des Radios sind noch offen.
- Diagnose-Webparser 0.7.0 übernimmt die falsche kHz-Einheit der Herstellerzeile: 8000/16000 sind hier Hz. Offlineauswertung 0.7.1 berücksichtigt dies; Geräteanzeige noch nicht korrigiert.
- Diagnose wählt p2p-wlan0-0, dessen RX-/TX-Bytezähler im Feldtest null bleiben. WLAN-Verlustdiagnose daraus unzulässig; tatsächliche Dateninterfaces müssen separat erfasst werden.

- Die Wiederverbindung am Windows-PC war nach Stromtrennung verzögert; nach erneutem PC-Anschluss sind WLAN und Gerät wieder erreichbar. Kein fortbestehender Startfehler nachgewiesen.
- Abrupter Stromverlust kann die letzte ungespeicherte Minute verlieren. Ringlogs sind begrenzte Ausschnitte, kein lückenloses Archiv.
- Windows hat globale manuelle WLAN-Adressen; `.2` tauchte zusätzlich zu `.104` wieder auf. Nach Gerätetests auf ursprünglichen DHCP-Betrieb zurückstellen.
- Audioauswertung sieht nur vorhandene Meldungen im letzten passenden Logausschnitt. Fehlende Meldungen sind kein Nachweis eines falschen oder richtigen Audioformats.

- Die Oberfläche 0.7.0 ist auf einem eigenen Adapter installiert und geprüft. Der erste Fahrzeug-/Teams-Test ist ausgewertet; Vollbackup, Hardware-Recovery und bestätigter Audiofix stehen weiterhin aus.
- iPhone-/Safari-Endprüfung steht aus; Desktop-Browser auf echter Geräte-Origin wurde erfolgreich geprüft.

- Teams-Anrufe im Hyundai i30 Kombi (2018) sind über den Adapter in beiden Richtungen blechern. Derselbe Teams-Anwendungsfall auf demselben iPhone klingt über direktes USB-Kabel deutlich besser. Ein entsprechender Fehler bei Musik ist nicht bestätigt.
- Die genauen Laufzeitparameter der Modi `aud=0..3` sind noch nicht vollständig einem Fahrzeug-Log und den jeweiligen Audioformaten zugeordnet.
- Ein aktiver Teams-Log ist jetzt vorhanden. Noch fehlen Radio-Fähigkeitswörter/Plugin-Version der initialen Auswahl, ein PCM-Vergleich und die Formate beim direkten Kabelbetrieb.
- Ein vollständiger Flash-Backup- und Recoveryweg ist noch nicht verifiziert.
- Die Cloud-Testfirmware trägt im Manifest die Kennung `26122515.5234.2`, ihr internes `system.json` jedoch `26051115.5234.2`. Sie darf deshalb nicht als eindeutig freigegebene Zielversion behandelt werden.
- Der CGI-Export cached `/tmp/log.gz`: Mehrere Abrufe nach derselben ersten Erfassung liefern alte Daten. Für jeden Fahrzeugversuch ist vor der Wiedergabe ein Adapterneustart nötig.
- Die Funktionen `UpdateHUSamplerate` und `DisableHUAudioFormat` sind in der stabilen Bibliothek nicht implementiert. Frühere Vermutungen aus ihren Namen sind damit widerlegt.
- Die im Webfrontend vorhandene ADB-Umschaltung wird für Plattform 5234 ausgeblendet und wurde nicht erzwungen.

## Behoben oder geklärt

- 2026-10-25 11:41 CET: Erster Teams-Fahrzeuglog gesichert und dedupliziert. Mode 2/3 nutzen beide 8 kHz im Telefon-USB-Pfad; ein reiner Musikratenwechsel trifft den beobachteten Engpass nicht. Projektanalyse 0.7.1, Gerät unverändert auf UI 0.7.0.

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

