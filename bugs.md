# Bugs und AuffÃƒÆ’Ã‚Â¤lligkeiten

Version: 0.8.2 (Wartungszwischenstand; GerÃƒÆ’Ã‚Â¤te-UI zuletzt 0.7.0)
Stand: 2026-10-25 12:53 CET

Der Nutzer begrenzt den aktuellen Schritt auf Speichermessung, Fehlerprotokoll und LoglÃƒÆ’Ã‚Â¶schung. Der zweite 0.8.0-Vollpaketversuch nach bestÃƒÆ’Ã‚Â¤tigtem Netzteilanschluss wurde ebenfalls angenommen, blieb aber in Zustand 1. Normaler API-Neustart stellte 0.7.0/Updatezustand 0 wieder her. Kein Beleg fÃƒÆ’Ã‚Â¼r ein Netzteilproblem. Zuletzt vor diesem Neustart: 23.820 KiB RAM verfÃƒÆ’Ã‚Â¼gbar, 204/512 KiB im Logspeicher frei. Freier temporÃƒÆ’Ã‚Â¤rer Dateisystemplatz ist damit noch nicht gemessen. Der Wartungskandidat 0.8.2 soll diese LÃƒÆ’Ã‚Â¼cke mit einem deutlich kleineren Customer-only-Paket schlieÃƒÆ’Ã…Â¸en; RuntimeprÃƒÆ’Ã‚Â¼fung lÃƒÆ’Ã‚Â¤uft, LÃƒÆ’Ã‚Â¶schung ist noch offen.

Die HTTP-Beobachtung erhielt einmal eine fehlerhafte Statuszeile. Das belegt keinen Firmwarefehler oder fehlgeschlagenen Upload; anschlieÃƒÆ’Ã…Â¸ende direkte Abfragen meldeten weiter Zustand 1. Die Beobachtung wurde ohne erneuten POST fortgesetzt.

Die ergÃƒÆ’Ã‚Â¤nzte Telefon-Messstelle 0.8.1 ist ausschlieÃƒÆ’Ã…Â¸lich offline geprÃƒÆ’Ã‚Â¼ft und nicht im 0.8.0-Image enthalten. Hardware-/LoglÃƒÆ’Ã‚Â¶schendpunkte und LED-Schalter sind weiterhin erst nach erfolgreicher GerÃƒÆ’Ã‚Â¤teinstallation verifizierbar.

0.8.0 ist offline geprÃƒÆ’Ã‚Â¼ft, noch nicht auf dem GerÃƒÆ’Ã‚Â¤t verifiziert. Es behebt die falsche Mikrofoneinheit im Webparser und die ausschlieÃƒÆ’Ã…Â¸liche Anzeige eines einzelnen Netzwerkinterfaces. Die nachfolgenden EintrÃƒÆ’Ã‚Â¤ge zu UI 0.7.0 bleiben bis zum echten Versionsvergleich gÃƒÆ’Ã‚Â¼ltig.

## Offen

- 0.8.0-Erstversuch: Upload bestÃƒÆ’Ã‚Â¤tigt, aber Zustand 1 blieb bestehen; keine Recovery-/Abschlussphase beobachtet. Kontrollierter API-Neustart fÃƒÆ’Ã‚Â¼hrte zurÃƒÆ’Ã‚Â¼ck zu normaler UI 0.7.0. ÃƒÆ’Ã¢â‚¬â€œffentlicher 0.8.0-Kanal bis erneuter GerÃƒÆ’Ã‚Â¤teprÃƒÆ’Ã‚Â¼fung deaktiviert. LED-Schalter und LÃƒÆ’Ã‚Â¶schfunktion noch nicht live verifiziert; Logs sind lokal gesichert.

- Teams-Feldtest belegt 8-kHz-Telefonpfad trotz 16-kHz-iPhone-Anfrage, in Mode 2 und 3. Das passt zur verbleibenden DÃƒÆ’Ã‚Â¤mpfung. Auswahlursache und tatsÃƒÆ’Ã‚Â¤chliche 16-kHz-FÃƒÆ’Ã‚Â¤higkeiten des Radios sind noch offen.
- Diagnose-Webparser 0.7.0 ÃƒÆ’Ã‚Â¼bernimmt die falsche kHz-Einheit der Herstellerzeile: 8000/16000 sind hier Hz. Offlineauswertung 0.7.1 berÃƒÆ’Ã‚Â¼cksichtigt dies; GerÃƒÆ’Ã‚Â¤teanzeige noch nicht korrigiert.
- Diagnose wÃƒÆ’Ã‚Â¤hlt p2p-wlan0-0, dessen RX-/TX-BytezÃƒÆ’Ã‚Â¤hler im Feldtest null bleiben. WLAN-Verlustdiagnose daraus unzulÃƒÆ’Ã‚Â¤ssig; tatsÃƒÆ’Ã‚Â¤chliche Dateninterfaces mÃƒÆ’Ã‚Â¼ssen separat erfasst werden.

- Die Wiederverbindung am Windows-PC war nach Stromtrennung verzÃƒÆ’Ã‚Â¶gert; nach erneutem PC-Anschluss sind WLAN und GerÃƒÆ’Ã‚Â¤t wieder erreichbar. Kein fortbestehender Startfehler nachgewiesen.
- Abrupter Stromverlust kann die letzte ungespeicherte Minute verlieren. Ringlogs sind begrenzte Ausschnitte, kein lÃƒÆ’Ã‚Â¼ckenloses Archiv.
- Windows hat globale manuelle WLAN-Adressen; `.2` tauchte zusÃƒÆ’Ã‚Â¤tzlich zu `.104` wieder auf. Nach GerÃƒÆ’Ã‚Â¤tetests auf ursprÃƒÆ’Ã‚Â¼nglichen DHCP-Betrieb zurÃƒÆ’Ã‚Â¼ckstellen.
- Audioauswertung sieht nur vorhandene Meldungen im letzten passenden Logausschnitt. Fehlende Meldungen sind kein Nachweis eines falschen oder richtigen Audioformats.

- Die neue OberflÃƒÆ’Ã‚Â¤che ist auf einem eigenen Adapter installiert und geprÃƒÆ’Ã‚Â¼ft. Vollbackup, Hardware-Recovery und Fahrzeug-/Teams-Test stehen weiterhin aus.
- iPhone-/Safari-EndprÃƒÆ’Ã‚Â¼fung steht aus; Desktop-Browser auf echter GerÃƒÆ’Ã‚Â¤te-Origin wurde erfolgreich geprÃƒÆ’Ã‚Â¼ft.

- Teams-Anrufe im Hyundai i30 Kombi (2018) sind ÃƒÆ’Ã‚Â¼ber den Adapter in beiden Richtungen blechern. Derselbe Teams-Anwendungsfall auf demselben iPhone klingt ÃƒÆ’Ã‚Â¼ber direktes USB-Kabel deutlich besser. Ein entsprechender Fehler bei Musik ist nicht bestÃƒÆ’Ã‚Â¤tigt.
- Die genauen Laufzeitparameter der Modi `aud=0..3` sind noch nicht vollstÃƒÆ’Ã‚Â¤ndig einem Fahrzeug-Log und den jeweiligen Audioformaten zugeordnet.
- Ein aktiver Teams-Log ist jetzt vorhanden. Noch fehlen Radio-FÃƒÆ’Ã‚Â¤higkeitswÃƒÆ’Ã‚Â¶rter/Plugin-Version der initialen Auswahl, ein PCM-Vergleich und die Formate beim direkten Kabelbetrieb.
- Ein vollstÃƒÆ’Ã‚Â¤ndiger Flash-Backup- und Recoveryweg ist noch nicht verifiziert.
- Die Cloud-Testfirmware trÃƒÆ’Ã‚Â¤gt im Manifest die Kennung `26122515.5234.2`, ihr internes `system.json` jedoch `26051115.5234.2`. Sie darf deshalb nicht als eindeutig freigegebene Zielversion behandelt werden.
- Der CGI-Export cached `/tmp/log.gz`: Mehrere Abrufe nach derselben ersten Erfassung liefern alte Daten. FÃƒÆ’Ã‚Â¼r jeden Fahrzeugversuch ist vor der Wiedergabe ein Adapterneustart nÃƒÆ’Ã‚Â¶tig.
- Die Funktionen `UpdateHUSamplerate` und `DisableHUAudioFormat` sind in der stabilen Bibliothek nicht implementiert. FrÃƒÆ’Ã‚Â¼here Vermutungen aus ihren Namen sind damit widerlegt.
- Die im Webfrontend vorhandene ADB-Umschaltung wird fÃƒÆ’Ã‚Â¼r Plattform 5234 ausgeblendet und wurde nicht erzwungen.

## Behoben oder geklÃƒÆ’Ã‚Â¤rt

- 2026-10-25 11:41 CET: Erster Teams-Fahrzeuglog gesichert und dedupliziert. Mode 2/3 nutzen beide 8 kHz im Telefon-USB-Pfad; ein reiner Musikratenwechsel trifft den beobachteten Engpass nicht. Projektanalyse 0.7.1, GerÃƒÆ’Ã‚Â¤t unverÃƒÆ’Ã‚Â¤ndert auf UI 0.7.0.

- 2026-10-25 10:55 CET: Auch echte Stromtrennung bestanden. Nutzer bestÃƒÆ’Ã‚Â¤tigt erneuten PC-Anschluss, Recorder zÃƒÆ’Ã‚Â¤hlt Boot 3. Beide Boot-1-Logs sind weiterhin SHA-256-identisch und gzip-CRC-gÃƒÆ’Ã‚Â¼ltig. Kaltstart und persistente Speicherung damit auf diesem Adapter belegt.

- 2026-10-25 10:53 CET: 0.7.0 normal gestartet, sieben Webdateihashes passend. Reale 512-KiB-Datenpartition mit zunÃƒÆ’Ã‚Â¤chst 304 KiB frei, Logger aktiv. CPU-Messung liefert plausible 3,4ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“6 % statt falscher 100 %. Liveanzeige lief ohne Browseraufzeichnung; Sofortspeicherung und Auswertung gespeicherter Logs funktionieren. Beide Boot-1-Logs nach Software-Neustart unverÃƒÆ’Ã‚Â¤ndert und CRC-geprÃƒÆ’Ã‚Â¼ft.

- 2026-10-25 10:47 CET: 0.6.0 per eingebettetem GitHub-Updater installiert; sieben statische Dateien und funktionaler CGI bestÃƒÆ’Ã‚Â¤tigt. Idle-Jiffies blieben trotz laufender Idle-Sekunden stehen. 0.7.0 nutzt zwei Laufzeit-/Idle-Messungen; reale Gegenprobe und RÃƒÆ’Ã‚Â¼cksetzfÃƒÆ’Ã‚Â¤lle sind getestet.
- 2026-10-25 10:47 CET: Liveanzeige startet automatisch, unabhÃƒÆ’Ã‚Â¤ngig von optionaler Browseraufzeichnung.

- 2026-10-25 10:03 CET: Firmware 0.5.0 angenommen, Updaterzustand 2ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢3 beobachtet, anschlieÃƒÆ’Ã…Â¸end mit `id=set&conn=cp` normal neu gestartet. Alle sechs neuen/geÃƒÆ’Ã‚Â¤nderten Webdateien stimmen per SHA-256 mit dem Build ÃƒÆ’Ã‚Â¼berein. Einstellungen `aud=2`, `mic=0`, `sig=149` erhalten; `conn=cp` ist der protokollierte Neustart-/CarPlayaufruf.
- 2026-10-25 10:03 CET: WÃƒÆ’Ã‚Â¤hrend des Updates lÃƒÆ’Ã‚Â¤uft nur die Recovery-Verwaltung mit Versionsanzeige `00000000.5234.2`; fehlende statische Dateien und `no QUERY STRING` waren in dieser Phase kein endgÃƒÆ’Ã‚Â¼ltiger Installationsbefund.
- 2026-10-25 10:03 CET: PC-WLAN musste von APIPA auf eine passende feste Clientadresse umgestellt werden. Eine zusÃƒÆ’Ã‚Â¤tzlich verbliebene Adresse und zeitweise unbrauchbare Route behinderten den Preflight. Nach Nutzerkorrektur auf `.104` war der Transfer erfolgreich. Kein fehlgeschlagener Preflight hat Firmwarebytes ÃƒÆ’Ã‚Â¼bertragen.
- 2026-10-25 10:03 CET: Funkchip-Aussage korrigiert: Bluetooth-Profil `RTL8723FS`, WLAN-Treiber im Kernel `RTL8733BS`; PlatinenbestÃƒÆ’Ã‚Â¼ckung bleibt unbestÃƒÆ’Ã‚Â¤tigt.

- 2026-10-25 09:36 CET: Logo und dunkles Design implementiert; Firmwarecontainer bytegenau rÃƒÆ’Ã‚Â¼ckverpackt und zweimal identisch gebaut. Kernel, `sw-description`, alle 66 ursprÃƒÆ’Ã‚Â¼nglichen DateisystemeintrÃƒÆ’Ã‚Â¤ge und `/dev/console` bleiben erhalten; exakt sechs UI-Dateien ÃƒÆ’Ã‚Â¤ndern sich/kommen hinzu.
- 2026-10-25 09:36 CET: Logo liegt unter `/css/`, weil `lyUpdate.sh` beim Start nur `index.html`, `css`, `js`, `lan` und CGI in den aktiven Webroot einbindet. Ein neuer Ordner `/assets/` allein wÃƒÆ’Ã‚Â¤re dort nicht erreichbar.
- 2026-10-25 09:36 CET: Vergleichskonstante von Andes BEQC/BNEC korrekt als unsigned 7-Bit dekodiert; Konstanten ab 64 werden nicht mehr irrtÃƒÆ’Ã‚Â¼mlich negativ dargestellt. Kleine bestehende Audio-Vergleiche bleiben unverÃƒÆ’Ã‚Â¤ndert.

- 2026-10-25 08:39 CET: Audiomodus von `Mode 1` auf den adaptiven `Mode 2` umgestellt und nach Neustart verifiziert.
- 2026-10-25 08:52 CET: Herstellerabbild entschlÃƒÆ’Ã‚Â¼sselt, Hersteller-MD5 geprÃƒÆ’Ã‚Â¼ft und SWUpdate-Container extrahiert.
- 2026-10-25 08:54 CET: SquashFS-Dateisysteme der stabilen und der Testfirmware sicher extrahiert.
- 2026-10-25 08:56 CET: Kernel, Device Tree und Plattformmerkmale aus beiden Bootabbildern gewonnen.
- 2026-10-25 08:58 CET: Die vier Audiomodi als reale, getrennte Programmwerte im RISC-V-Code bestÃƒÆ’Ã‚Â¤tigt.
- 2026-10-25 08:59 CET: Konkreten Sample-Rate-Hook `/tmp/ly_force_musicrate` und den Aufruf `ForceSetMusicSamplerate()` belegt.
- 2026-10-25 09:00 CET: Reproduzierbares, rein lesendes Erfassungsskript fÃƒÆ’Ã‚Â¼r Fahrzeugtests erfolgreich geprÃƒÆ’Ã‚Â¼ft.
- 2026-10-25 09:07 CET: Vermeintlich beschÃƒÆ’Ã‚Â¤digtes GerÃƒÆ’Ã‚Â¤telog vollstÃƒÆ’Ã‚Â¤ndig rekonstruiert. Ursache war ein bisher nicht entferntes vier Byte langes LÃƒÆ’Ã‚Â¤ngenfeld bei Offset `0x333`; gzip-CRC und EndlÃƒÆ’Ã‚Â¤nge bestehen jetzt vollstÃƒÆ’Ã‚Â¤ndig. FrÃƒÆ’Ã‚Â¼here Salvage-Klartexte sind historische, unzuverlÃƒÆ’Ã‚Â¤ssige Ableitungen.
- 2026-10-25 09:07 CET: V821B-Untervariante, 16 MiB Flash und vollstÃƒÆ’Ã‚Â¤ndige Partitionstabelle direkt im geprÃƒÆ’Ã‚Â¼ften eigenen GerÃƒÆ’Ã‚Â¤telog bestÃƒÆ’Ã‚Â¤tigt.
- 2026-10-25 09:05 CET: ZusÃƒÆ’Ã‚Â¤tzliches `lylink`-Paket beider Updates mit je sechs Dateien entschlÃƒÆ’Ã‚Â¼sselt und jede einzelne CRC geprÃƒÆ’Ã‚Â¼ft.
- 2026-10-25 09:18 CET: Nutzer bestÃƒÆ’Ã‚Â¤tigt Teams, beide Richtungen und besseren Teams-Klang per Kabel am selben iPhone. Diagnose auf bidirektionalen Telefonpfad eingegrenzt; Musik-Sample-Rate-Hook ist kein belegter Ansatz fÃƒÆ’Ã‚Â¼r diesen Fehler.

