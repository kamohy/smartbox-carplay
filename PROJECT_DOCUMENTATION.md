# Projektdokumentation

Version: 0.8.0  
Stand: 2026-10-25 11:55 CET

## 2026-10-25

### 11:52–12:08 CET – Updatevorbereitung hängt, kontrollierter Normalstart, erneuter Test vorbereitet

0.8.0 wurde einmal über den vorhandenen Browser-Updater übertragen. Geräte-CGI bestätigte den Upload nach rund zwei Sekunden. Der Status blieb anschließend bei 1 und Herstellerbasis 26011517.5234.2; keine Recoveryphase 2 und kein Abschluss 3 beobachtet. Die Fortschrittsanzeige oberhalb 70 % ist im ursprünglichen cpbox.js zeitbasiert und belegt keine übertragenen Bytes oder Flashfortschritte. Der normale Oberflächen-Code wurde deshalb nach bestätigtem Upload verlassen, um automatische Abfragen zu stoppen. Kein zweiter Upload wurde automatisch gestartet.

Aktuelle Logdaten und beide Beobachtungsintervalle liegen unter `evidence/updates/2026-10-25-ui080/`. Nach länger unveränderter Vorbereitung wurde der vorhandene normale API-Neustart gezielt einmal aufgerufen. Danach läuft dasselbe Gerät wieder mit Updatezustand 0 und weiterhin UI 0.7.0. Installation und Loglöschung sind damit noch nicht erreicht. Das öffentliche 0.8.0-Manifest wurde bis zum erfolgreichen Gerätetest deaktiviert. Für einen kontrollierten neuen Versuch wurde der Nutzer gebeten, wie bei den bisherigen erfolgreichen Updates ein USB-Netzteil zu verwenden.

Parallel fragte der Nutzer nach einem Emulator als Prüfstand. Apples eigenständiger Mac-Simulator mit echtem iPhone wurde von seinem Xcode-Simulationsfenster unterschieden; LIVI/Linux setzt zusätzliche CarPlay-Authentifizierung voraus. Ein Windows-/Hyundai-Prüfstand für diesen Dongle ist noch nicht verifiziert. Es wurde keine Emulatorsoftware installiert. `hardware_limits.md` dokumentiert bestätigte Bauteile, Reserven und Grenzen. Der originale DTB wurde zusätzlich geprüft: ein Linux-CPU-Knoten, 16-KiB-I-/D-Caches, zunächst referenzierte 360–960-MHz-Tabelle und alternative Tabellen bis 1.200 MHz. Laufzeitauswahl/Takt bleiben bis zum Gerätezugriff offen.

### 11:44–11:55 CET – Verständliche Bedienung, Hardwareabfrage und begrenzte Loglöschung 0.8.0

Der Nutzer bestätigte LED Default=Ein und Mode 1=Aus und beauftragte einen Schalter, verständliche Einstellungsbeschreibungen, Hardware-/Maximalprüfung sowie Sicherung und Löschung der Logs. Vor Änderungen wurden alle sechs aktuellen gzip-Dateien samt Metadaten und frischem Systemlog unter `evidence/log-backups/2026-10-25-114454/` gesichert und CRC-/SHA-256-geprüft. Löschung ist bis zur verfügbaren geprüften Gerätefunktion noch offen.

Das neue Einstellungsmodul zeigt einen echten LED-Schalter, Telefonpuffer mit belegter Wirkung und ausdrücklich ungeklärten Profilfeinheiten sowie Verbindungsstart statt Delayed start. Im Original-rcpservice belegt der Getter 0x21520 und dessen Aufruf bei 0x141D4: delay=2 führt über 0x15068 zu sleep(20). Für delay=1 ist keine feste zusätzliche Sekundenanzahl belegt. Es wurden keine Klangversprechen oder erfundenen Zeitwerte ergänzt.

Die Hardwarekarte trennt bestätigte Startlogdaten von Treiberhinweisen. Eine feste CGI-Abfrage liest CPU-/RAM-/MTD-/Mount-/cpufreq-/USB-/SDIO-Daten und verfügbare lokale Buswerkzeuge. Der Hersteller beschreibt die V821-Familie als heterogenes CPU/MCU-System; die aktuelle Allwinner-Seite bezieht sich ausdrücklich auf V821L2-WXX, also keine ungeprüfte Taktaussage über unseren V821B. Mikrofonraten werden richtig als 8→16 kHz angezeigt, Netzwerkinterfaces getrennt erfasst. Der Recorder bewahrt frühe HU-Auswahllogs im begrenzten RAM-Verlauf auf.

Die neue Löschanforderung darf ausschließlich die sechs eigenen Logslots und eigene RAM-Snapshots entfernen, erhält Bootzähler und fremde Daten und wird seriell vom Recorder abgearbeitet. Tests prüfen diesen Umfang, Origin-/Methodengrenzen, LED-Mapping und reale Mikrofonlogeinheit. 27 Pythonprüfungen und drei JS-Prüfprogramme bestehen. Zwei Builds sind identisch: 6.199.341 Byte, SHA-256 `47276c8e59417f3346d67489f8dd14a0ff6717721797a43b2c139fab49d54f46`. Elf Pfade ändern sich; Audio-Binärdateien, Kernel und übrige Originalinodes bleiben unverändert. Geräteinstallation und reale Hardware-/Löschprüfung stehen bei diesem Eintrag noch aus.

### 11:29–11:41 CET – Erster Teams-Feldtest, 8-kHz-Engpass, Analyseversion 0.7.1

Der Nutzer meldete vorhandene Fahrzeuglogs. Der PC war zunächst nicht im Adapter-WLAN; Windows wiederholte erfolglose Sicherheitsanmeldungen. Das vorhandene Profil wurde vor einer erneuten WPA2/AES-Parametrierung lokal gesichert; es enthielt bereits AES, die angezeigte GCMP/CCMP-Auswahl blieb bestehen. Eine kausale Profilreparatur ist daher nicht bewiesen. Nach Wiederverbindung gelang der Zugriff. Nutzer stellte klar, dass das iPhone bereits getrennt war. Keine Geräte-IP, kein Audiomodus und keine Firmware wurden in diesem Block geändert.

Alle sechs Ringdateien aus Starts 5/6/7 wurden samt Hoststatus und frischem PC-Log gesichert. gzip-CRC und Gerätidentität geprüft; Rohdaten bleiben unter `evidence/field-tests/2026-10-25-113352/`. Start 5 enthält Mode 2, Start 6 Mode 3, Start 7 die PC-Sitzung. Nutzer bestätigt beide Versuche als Teams und subjektiv besseren, aber weiterhin gedämpften Ton nach Moduswechsel.

Die Fahrzeuglogs zeigen übereinstimmend Telefon-Audiotyp 8 mit 16.000 Hz/16 Bit/Mono auf iPhone-Seite und 8.000 Hz/16 Bit/Mono beim USB-Telefonstart. Die HU-Taktrückmeldungen liegen bei etwa 8.000 Hz; Mikrofonumwandlung 8.000→16.000 ist ebenfalls protokolliert. Die Herstellerbeschriftung `8000kHz -> 16000kHz` ist falsch: Konvertervariablen und Aufbau im Originalcode sind in Hz. Die installierte Webauswertung übernimmt diesen Einheitenfehler; im neuen Offlinewerkzeug ist die Auswertung korrekt. Kein PCM-/Kabelvergleich und keine vollständige Klangursache behauptet.

Der Originalcode `rcpservice` ab 0x2BEAC ruft GetHUAudioFormat/GetHUPluginVer auf. Bit 2 führt zunächst zu 8 kHz; der Versionsvergleich gegen 319 bei 0x2C06A kann die folgende Prüfung auf Bit 4/16 kHz überspringen. Weitere Zweige wählen unmittelbar 16 kHz. Die echten Eingangsmasken und Plugin-Version fehlen im Logausschnitt. Daher ist weder eine feste Hardwaregrenze noch ein sicherer Rate-Override bewiesen.

`tools/analyze_field_logs.py` prüft Archive offline, trennt Boots, dedupliziert überlappende Zeilen, hält Telefon und Audiotyp 64 auseinander und wertet Messpunkte getrennt aus. Regressionen decken echte Logformate/Einheiten, Überlappung, getrennte Starts und defekte CRC ab. 26 Pythonprüfungen und beide JavaScript-Prüfprogramme bestehen. Feldbericht `field_test_2026-10-25.md` dokumentiert Befunde, Grenzen und nächsten Schritt: initiale Fähigkeits-/Versionsdaten sichern. Projektversion 0.7.1 bezeichnet Analyse/Dokumentation, installiert und im OTA-Manifest bleibt 0.7.0. Keine Audiosoftware verändert oder geflasht.

### 10:54–10:55 CET – Echte Stromtrennung bestanden

Der Nutzer bestätigte den erneuten Anschluss diesmal am PC. Nach verzögerter Windows-WLAN-Wiederverbindung ist derselbe Adapter erreichbar, Recorder aktiv und Bootzähler 3. Beide Boot-1-Logs stimmen weiterhin SHA-256-genau mit den vor Software-Neustart und Stromtrennung geladenen Dateien überein; gzip-CRC gültig. Fünf Dateien aus drei Starts sind vorhanden, 252 von 512 KiB frei. Die Liveanzeige aktualisiert sich wieder automatisch, weiterhin ohne Browseraufzeichnung. Der zuvor offene Kaltstartpunkt ist erledigt. Kein weiterer Flash war nötig. Beleg: `persistence.after-power.json` und `installed-diagnostics.png` im lokalen Updateordner; öffentliche Nachweise enthalten keine Rohlogs/Gerätekennungen. Der Fahrzeug-/Teams-Test und jede behauptete Audioverbesserung bleiben ausdrücklich offen.

### 10:48–10:53 CET – Echte Installation und Software-Neustartprüfung 0.7.0

Das öffentlich geladene Image wurde vorab per Größe/SHA-256 geprüft und einmal über den echten Browser-Updater übertragen. Zustand 1→2→3 und anschließender Normalstart sind beobachtet. Sieben statische Webdateien stimmen mit dem Build überein. Der CGI meldet 58.124 KiB nutzbaren RAM, CPU im Messintervall etwa 3,4–6 % und echte 512 KiB Datenspeicher, zunächst 304 KiB frei. Der Logger läuft und erzeugt CRC-gültige 13-KiB-gzip-Dateien mit Messpunkten.

Zwei Browserbeobachtungen im Abstand von 22 Sekunden zeigen aktualisierte Laufzeit/Abfragezeit bei weiterhin null aufgezeichneten Browsermesspunkten: automatische Anzeige ist unabhängig vom Aufzeichnungsstart bestätigt. Sofortspeicherung per Schaltfläche und Audioauswertung aus dem gespeicherten Slot funktionieren. Anschließend blieben beide Boot-1-Dateien über einen kontrollierten Neustart SHA-256-identisch. Der neue Start zählt korrekt auf Boot 2 hoch. GitHub CI 40182107570 erfolgreich.

Der Nutzer trennte auf Anforderung den Strom und bestätigte erneuten Anschluss. Danach ist das Adapter-WLAN bisher nicht wieder sichtbar; der Kaltstartvergleich ist noch offen. Keine weitere Firmwareübertragung wurde wiederholt. Individuelle Belege bleiben lokal unter `evidence/updates/2026-10-25-105000-ui070/`.

### 10:16–10:47 CET – Geräteprüfung 0.6.0, Liveanzeige und persistente Logs 0.7.0

0.6.0 wurde über den eingebetteten öffentlichen Updatekanal heruntergeladen, geprüft und installiert. Recovery 2→3, kontrollierter Normalstart, Herstellerbasis 26011517.5234.2 und sieben Webdateihashes sind bestätigt. Der CGI lieferte echte Werte, einen frischen 60.935-Byte-Log und korrekte Methodengrenzen. Belege: `evidence/updates/2026-10-25-101652-ui060/`. Der historische offene Installationspunkt ist erledigt.

Idle-Jiffies blieben auf dem echten Gerät stehen, obwohl `/proc/uptime` Idle-Sekunden weiterzählte. Der Fix nutzt Laufzeit, Idle-Sekunden und CPU-Anzahl: reales Vergleichspaar 64,3939 % statt falscher 100 %. Die zweimal gebaute Zwischenversion 0.6.1 wurde weder veröffentlicht noch installiert; der Fix geht in 0.7.0 ein.

Der Nutzer beauftragte persistente Systemlogs und automatische CPU/RAM/Laufzeit. Browser-JavaScript fragt alle zwei Sekunden ab, unabhängig von optionaler Aufzeichnung. Das native Shellskript startet über das minimal ergänzte originale `lyLink.sh`, außerhalb Recovery. Es prüft den RW-Datenmount und freien Platz, hält Status alle fünf Sekunden in RAM und schreibt etwa alle 60 Sekunden gzip-Snapshots. Drei Startslots mit je zwei Dateien bis 24 KiB und 64 KiB Mindestreserve begrenzen den Platz. Neue Dateien werden CRC-geprüft, synchronisiert und atomar umbenannt. Kein Formatieren/Mounten/Rohflashzugriff.

Die Seite ergänzt Speicherstatus, Downloads, Sofortspeicher-Anforderung und Audioauswertung früherer Logs. Nur feste IDs sind zugelassen. Das echte Skript besteht Tests zu vier Starts, CRC, fremden Dateien, RAM-/RO-/fehlenden Mounts, Platzmangel und übergroßen Logs. 24 Pythonprüfungen und beide JavaScriptprogramme bestehen. Zwei Builds sind identisch: 6.199.341 Byte, SHA-256 `32e395c7ff22fcf40eb019748126e554694786974d261f70ab4fe07171e6aeb4`. Zehn erlaubte Dateien ändern sich; alle anderen Originalinodes und Kernel bleiben erhalten. Geräteinstallation und echter Persistenztest stehen bei diesem Eintrag noch aus.

### 10:07–10:16 CET – Integrierte Diagnose, Version 0.6.0

Der Nutzer fragte nach Analysewerkzeugen und bestätigte ausdrücklich die Integration in die Einstellungsseite. Ergänzt wurden eine sichtbare Diagnosekarte und ein eng begrenzter Shell-CGI mit ausschließlich festen GET-Abfragen für Status, Audioausschnitt und lokalen Logdownload. POST, zusätzliche Parameter, Kommandos und Dateipfade werden abgewiesen. Der CGI liest proc/sys, dmesg und `logcat -d`; er löscht keine Puffer, schreibt nicht in den Flash und nutzt nicht den alten `/tmp/log.gz`-Cache.

Die Oberfläche berechnet CPU aus zwei Zählerständen, zeigt Speicher und Laufzeit, USB-Zustand und kumulative WLAN-Drops. Aufzeichnung erfolgt im Browser mit höchstens 900 Messpunkten bei zwei Sekunden Abstand. JSON- und Logexport bleiben lokal. Telefon-Ausgabe und Mikrofonumwandlung werden ausschließlich aus konkret vorhandenen Hersteller-Logformaten gelesen. Insbesondere wird 48-kHz-Musik nicht als Telefonrate ausgegeben und fehlende Daten werden nicht durch Annahmen ersetzt.

Der SquashFS-Patcher setzt ausschließlich den neuen Diagnose-CGI auf ausführbaren Modus 0755; alle ursprünglichen Dateimetadaten bleiben erhalten. Zwei neue Builds sind byteidentisch: 6.195.245 Byte, SHA-256 `af5c80bca12b13eca5f14481ef30b9955cd1d711d7a49199ca209f8edd2c5bdb`. Acht Dateien werden ergänzt/ersetzt, Kernel und Updatebeschreibung bleiben original. 19 Pythonprüfungen und beide JavaScript-Prüfprogramme bestehen. Die Shelltests wurden unter Git-for-Windows mit LF-Fixtures ausgeführt; Windows-CRLF in künstlichen sysfs-Dateien wurde in den Fixtures korrigiert.

Die Geräteinstallation dieser Version steht zum Zeitpunkt dieses Eintrags noch aus. Ziel ist der echte eigene GitHub-Updatekanal der bereits installierten 0.5.0-Oberfläche.

### 09:39–10:03 CET – Rückweg untersucht, ausdrückliche Risikofreigabe, echte Installation, Version 0.5.1

Die vorherige Fortsetzung war Fortschritt: echter Kandidat und öffentliches Repository waren vorhanden. Upstream-xfel 1.4.0 wurde aus der originalen Windowsfreigabe geladen, gegen den Releasehash und zusätzlich EXE-/DLL-Hashes geprüft. Die reale Probe meldet kein FEL-Gerät. Ein lesendes Zwei-Pass-Backupwerkzeug wurde ergänzt und gegen kurze, abweichende und beschädigte Daten getestet. Diese synthetischen Prüfungen behaupten weder einen realen Dump noch einen Restore. Der aktuelle CatPlay-Weg `cpbox2fel.py` wurde nur gelesen: Er flasht zuerst ein modifiziertes OTA und hat keinen ly5234-Preset. Deshalb ist er kein unabhängiger Backupweg vor dem ersten Flash.

Die Hardwarebewertung wurde präzisiert: `RTL8723FS` stammt aus dem Bluetooth-Initialisierungspfad, der eigene Kernel enthält `8733bs`/`RTL8733B` als WLAN-Treiber. Frühere historische Formulierungen „Funkchip RTL8723FS“ sind damit eingeschränkt, kein physischer WLAN-Chipnachweis.

Der Nutzer schloss Platinenzugang aus und wies ausdrücklich an, den Updatepfad zu verwenden; einen möglichen zerstörten Dongle und Ersatzkauf akzeptiert er. Damit wurde die ursprüngliche Backup-Voraussetzung für den ersten gezielten Updateversuch aufgehoben. Es erfolgte keine erneute Nachfrage nach dieser Risikofreigabe.

Der Adapter war zeitweise abgesteckt; nach erneutem Anschluss bekam Windows zunächst nur APIPA. Die WLAN-IP-Änderung scheiterte im Agentprozess an fehlenden Administratorrechten. Der Nutzer setzte eine statische Adresse und korrigierte sie später auf `.104`; eine alte zusätzliche `.2` wurde entfernt. Zwischenzeitlich wurden USB-Netzteilversorgung und erneute WLAN-Verbindung getestet. Sämtliche bis dahin gescheiterten Versuche brachen im lesenden Preflight ab. Es gab nur einen echten Firmwareupload.

Um 09:59:44 CET wurde das vollständig geprüfte 6.187.053-Byte-Image einmal per multipart hochgeladen und mit `code=0 / upload successful` bestätigt. Original und Kandidat nutzen XZ-CRC32 (Check-ID 1). Danach wurden Geräteidentität und Updaterzustände 2 und 3 beobachtet. Im Recoveryzustand meldete der CGI `00000000.5234.2` und lieferte keine normale statische Oberfläche. Das Gerät wurde erst nach bestätigtem Zustand 3 über den dokumentierten Herstelleraufruf `id=set&conn=cp` neu gestartet.

Nach dem Normalstart meldet das eigene Gerät wieder `26011517.5234.2`, Updater 0, `aud=2`, `mic=0`, `sig=149`, `conn=cp`. Alle sechs UI-Dateien wurden direkt über `192.168.1.101` abgerufen und per SHA-256 mit dem Build abgeglichen. Die echte Geräteoberfläche wurde im Browser geöffnet. Die eigene Firmware-UI bleibt 0.5.0; Projekt-/Werkzeugfixstand ist 0.5.1. Audio-/Fahrzeugfunktion und Wiederherstellung bleiben ungetestet.

Lokale individuelle Belege liegen unter `evidence/updates/2026-10-25-095944/` und bleiben vom öffentlichen Repository ausgeschlossen. Der öffentliche Nachweis enthält nur Dateihashes, Status und erhaltene Einstellungen. Der Nutzer beauftragte anschließend einen eigenen lesenden Diagnosebereich; diese Erweiterung wird getrennt versioniert.

### 09:20–09:37 CET – Eigene Oberfläche, Firmwarekandidat und GitHub, Version 0.5.0

Der Nutzer beauftragte ein lokales Bad-Hippo-SVG und dunkles Design in den Geräteeinstellungen, anschließend ausdrücklich die Untersuchung des Firmware-Downloads, den Bau eines veränderten Updates und eine dauerhaft eigene Updateadresse. Als Hostingwunsch wurde zunächst ein privates GitHub-Repository genannt und anschließend ausdrücklich auf öffentlich geändert. `kamohy/smartbox-carplay` wurde entsprechend angelegt und die öffentliche Sichtbarkeit verifiziert. Der GitHub-Connector bietet kein Anlegen von Repositories; dafür wurde die bereits angemeldete GitHub-CLI desselben Kontos genutzt.

Die echte Herstelleradresse wurde aus `cpbox_init()`/`cpbox_geturl()` und dem Live-Manifest bestätigt: `cpbox-abroad.oss-us-west-1.aliyuncs.com/5234/`. Das aktuelle Manifest ist byteidentisch mit dem Archiv. DNS lieferte zu diesem Zeitpunkt `47.254.114.108`. Der Browser lädt die Firmware und sendet sie dann per multipart an `id=upload`; es ist kein DNS-/TLS-Abfangen nötig. Die im CGI sichtbaren HMAC-SHA1-Begriffe gehören zum Cloud-/STS-Kontext und wurden nicht als Firmware-Signatur behauptet. Der separate Updater-/Recoverypfad ist noch nicht vollständig prüfbar.

Die HTML-Struktur der Herstellerfunktionen bleibt erhalten; ergänzt sind Header, lokal gespeichertes Logo, dunkles CSS und eigene Update-JavaScripts. Ein wichtiger Laufzeitpunkt wurde berücksichtigt: `lyUpdate.sh` bindet keinen beliebigen neuen `/assets`-Ordner ein. Das SVG liegt deshalb in `/css`, die neue Updatekonfiguration in `/js`.

Die feste neue Manifestadresse lautet `https://raw.githubusercontent.com/kamohy/smartbox-carplay/main/ota/5234/version.json`. Ein öffentliches Repository braucht keinen eingebetteten GitHub-Zugangsschlüssel. Der eigene Updater prüft Plattform, Herstellerbasis, numerische Projektversion, Freigabestatus, erlaubten Downloadpfad, Länge und SHA-256. Die erste Version wird als nicht freigegebener Kandidat geführt.

Ein eng begrenzter Rust-Helfer auf Basis von Backhand 0.25.5 verändert nur Dateien unter `/ota/www/`. Der Python-Builder prüft zuerst das fest gepinnte Original und reproduziert dessen vollständigen XOR-/MD5-/CRC-CPIO-Container byteidentisch. Das neue SquashFS wird unabhängig mit Dissect gelesen. Alle 66 originalen Einträge einschließlich Dateimodi, Eigentümern, Zeitstempeln und `/dev/console` bleiben erhalten. Kernel und `sw-description` sind byteidentisch. Exakt sechs UI-Dateien sind ersetzt/ergänzt; Audio-Programme wurden nicht verändert.

Zwei unabhängige Buildausgaben sind byteidentisch: 6.187.053 Byte, SHA-256 `3b1d45b1ca75b9462bfc53974b5d34c6f28aef9b4f0761c746f1cb0923074581`. Customer bleibt mit 3.018.752 Byte unter der 3.801.088-Byte-Partitionsgrenze. Elf Pythonprüfungen bestehen; JavaScript-SHA-256 wurde gegen Node-Krypto bis zu 1.000.000 Byte sowie an Paddinggrenzen geprüft. Versionen, Fremdplattformen, URL-Regeln, gesperrte Updates und beschädigte Downloads sind abgedeckt.

Der Andes-Decoder wurde zusätzlich korrigiert: BEQC/BNEC-Konstanten sind unsigned 7-Bit. Ein externer Opcodevektor mit Konstante 64 sichert diesen Fall ab; bisherige kleine Audio-Vergleichswerte ändern sich nicht.

Die lokale Vorschau verwendet echten lesenden Hoststatus und sperrt Schreib-/Uploadzugriffe. Ein HTTP-Hashvergleich bestätigt die unveränderte Originalseite auf dem Adapter. Keine neue Geräteeinstellung wurde in diesem Arbeitsblock geschrieben, keine Firmware hochgeladen oder geflasht. Die laufende Untersuchung bleibt vor einem Flash an den noch fehlenden vollständigen Backup-/Recoveryweg gebunden. Der Firmwarekandidat belegt den Bau, noch nicht den erfolgreichen Erststart.

### 09:15–09:19 CET – Teams-Vergleich präzisiert, Version 0.4.1

Der Nutzer präzisierte, dass der blecherne Klang bei Telefonaten mindestens über Teams auftritt. Auf Nachfrage bestätigte er beide Richtungen und deutlich besseren Teams-Klang am selben iPhone per direktem USB-Kabel. Die bisherige Annahme eines primären Musikfehlers wurde daher zurückgenommen. Die weitere Diagnose priorisiert den bidirektionalen Telefonpfad; die 44,1-/48-kHz-Musikmodifikation ist kein belegter Teams-Fix.

Im stabilen `lylinkapp` wurde der Telefonzweig von `AudioPlayerCreate` ab `0x1D50C` verfolgt: Eigene Radio-Telefonrate/Kanalzahl, fest 16 Bit. Der Mikrofon-/HID-Pfad ab `0x164FC` erzeugt bei abweichendem Radioformat zwei Umwandler zu/von intern 16.000 Hz, 16 Bit, Mono; der Siri-Pfad verwendet 24.000 Hz. Die zugehörigen FFmpeg-Funktionen für Eingabe-/Ausgaberate und Kanalbelegung wurden direkt im Code bestätigt. Das ist ein zusätzlicher Verarbeitungsschritt, aber ohne aktives Teams-Log noch keine bewiesene Ursache.

Die Fahrzeuganleitung wurde auf Teams-Ausgabe und Mikrofonqualität umgestellt. Eine generelle Stereo-Forderung ist bei Telefonaten falsch; Mono und Sprach-Sample-Raten sind zunächst regulär. Geprüft werden muss die konkrete Verschlechterung gegenüber dem bestätigten Kabelvergleich. Keine Geräteeinstellungen wurden verändert und keine Firmware geflasht.

### 09:00–09:12 CET – Weitere Programme, valide Logs und Version 0.4.0

Der vorherige Turn war Fortschritt: Projektdateien waren verschoben und der Stand 0.3.0 geprüft. Der Adapter wurde erneut lesend erreicht; er meldet weiter Firmware `26011517.5234.2`, `aud=2` und WLAN-Konfiguration 149. Es wurde in dieser Fortsetzung keine Konfiguration verändert oder Firmware übertragen.

Das Analysewerkzeug dekodiert jetzt GP-relative Andes-Lade-/Speicherbefehle und unmittelbare Vergleichssprünge. Die ADDIGP-Maske wurde korrigiert: Bit 14 gehört zum Offset und darf nicht als festes Opcodebit behandelt werden. Referenz ist der vom Andes-Entwickler veröffentlichte XAndesPerf-binutils-Patch.

Eine weitere Verpackungsschicht wurde in `customer/app/lylink` identifiziert. `tools/extract_lypack.py` entfernt die 128-Byte-Kopfmaskierung, verarbeitet lokale ZIP-Header und prüft jeden Deflate-Stream einschließlich CRC32. Aus beiden Updates wurden je sechs zusätzliche ELF-Dateien gewonnen, darunter die bisher nicht zugänglichen Programme `rcpservice`, `librcarplay.so` und `liblylinkpcm.so`. Zwischen stabiler und Testversion ändern sich drei dieser sechs Dateien.

Ein früherer Befund wurde korrigiert: `UpdateHUSamplerate` und `DisableHUAudioFormat` sind in der stabilen Bibliothek nur Platzhalter. `ForceSetMusicSamplerate` ist implementiert und akzeptiert ausschließlich 44.100 oder 48.000 Hz. Der `/tmp/ly_force_musicrate`-Hook bleibt eine mögliche spätere Modifikation, aber noch kein bewiesener Klang-Fix.

Die vermeintlichen gzip-Schäden im Log wurden auf den CGI-Exportcode zurückgeführt. Der Webserver fügt bei Byte 819 ein vier Byte langes Little-Endian-Größenfeld ein. Nach dessen Entfernung bestehen CRC32 und Endlänge vollständig. Der geprüfte Klartext ist 170.868 Byte groß und liegt zusätzlich als `logcat.validated.txt` vor. Frühere, fehlerhafte Salvage-Ableitungen wurden zur Nachvollziehbarkeit nicht überschrieben.

Der valide eigene Startlog bestätigt V821B, 64 MiB RAM, XT25P1288 mit 16 MiB Flash, Realtek RTL8723FS und alle zehn Flashpartitionen. Gleichzeitig wurde belegt, dass der CGI `/tmp/log.gz` nur einmal erzeugt und danach cached. Das Erfassungsskript prüft jetzt strikt, schreibt Prüfmetadaten und warnt bei einem bereits bekannten Export. Bestehende Ausgabeordner werden nicht überschrieben.

Der Nutzer konkretisierte das Fahrzeug als Hyundai i30 Kombi von 2018 und den Ton als „blechern“. Der Mingtu-44,1-kHz-Sonderfall prüft exakt `Tinnos` und `MISTRA`; `HYUNDAI MOBIS` ist ein anderer Modellindex. Eine Übertragung auf den i30 wäre unbelegt. Modellkennung, Musik-/Telefonpfad und Kanalzuordnung sind die nächsten Prüfschwerpunkte.

Sieben Regressionsprüfungen gegen externe Andes-Vektoren, reale Log-/Packdateien, beschädigte CRCs und kurze gepaddete Exporte bestehen. Die hörbare Ursache bleibt mangels aktiver Fahrzeugsitzung unbewiesen; Backup und Recovery sind weiterhin vor jedem Flash erforderlich.

### 08:50–09:00 CET – Firmwarezerlegung und Version 0.3.0

Die folgenden Aussagen geben den damaligen Zwischenstand wieder. Die Log-Trailer- und API-Bewertung wurde mit 0.4.0 ausdrücklich korrigiert.

Die zuvor nur als hochentropisch erkannte Herstellerfirmware wurde reproduzierbar entschlüsselt. Grundlage ist eine öffentlich dokumentierte 256-Byte-XOR-Tabelle der verwandten CPBox-/V821-Firmwarefamilie. Das eigene Werkzeug `tools/decrypt_firmware.py` prüft zusätzlich die vom Hersteller eingebettete MD5-Summe, bevor die SWUpdate-Nutzlast gespeichert wird.

Beide Abbilder wurden ausschließlich offline verarbeitet:

- stabile Firmware `26011517.5234.2`
- seriennummergebundene Cloud-Testfirmware mit äußerer Kennung `26122515.5234.2`

Die entschlüsselten Dateien sind SWUpdate-/CPIO-Container mit identischer `sw-description`. Sie schreiben `kernel` nach `/dev/by-name/boot` und `customer` nach `/dev/by-name/customer` und verändern währenddessen U-Boot-Umgebungsphasen. Der `customer`-Teil ist SquashFS; das Bootabbild folgt Android Boot Image v2.

`tools/extract_squashfs.py` extrahiert das Dateisystem ohne Symlinks auf dem Host anzulegen. Jedes Abbild enthält 12 Verzeichnisse, 52 reguläre Dateien und einen speziellen Eintrag. Die SquashFS-Erstellungszeiten lauten:

- stabil: 2026-01-15 10:41:24 CET
- Test: 2026-05-11 10:28:52 CEST

Zwischen beiden Dateisystemen unterscheiden sich exakt 13 Dateien. Betroffen sind insbesondere `lylinkapp`, `libwcarplay_new.so`, `libiap_new.so`, `liblyctrl.so`, `btapp`, `lyLink.sh`, `system.json`, CGI und Weboberfläche. Die Testversion ergänzt in `lyLink.sh` den Parameter `-k1` für Dienste und verändert deutlich den CarPlay-Code. Das ist ein Entwicklungszweig, aber kein Nachweis besserer Audioqualität.

Die Android-Boot-v2-Abbilder tragen den Namen `sun300i_riscv32`, enthalten keinen Ramdisk-Teil und liefern Linux 5.4.220 sowie einen Device Tree. Der stabile Kernel wurde am 18.12.2025, der Testkernel am 06.05.2026 gebaut.

Kernel- und Startprotokolle belegen:

- 32-Bit RISC-V mit Andes-Erweiterungen
- Allwinner-V821-Plattformpfad
- 64 MiB adressierbaren RAM
- Realtek `RTL8723FS` als Funkchip
- Flashkennung `xt25p1288`
- USB-Audiogadget `iphone_audio`

Für die RISC-V-Binäranalyse wurde der Andes-Befehl `ADDIGP` anhand der öffentlich verfügbaren Andes-Erweiterungsimplementierung dekodiert. Dadurch konnten echte Codeverweise statt bloßer Texttreffer bestätigt werden: `aud0`, `aud1`, `aud2` und `aud3` werden als vier getrennte Werte geparst.

Der wichtigste Audiofund liegt in `lylinkapp`: Die Software liest optional eine Ganzzahl aus `/tmp/ly_force_musicrate` und ruft anschließend `ForceSetMusicSamplerate()` in `libwcarplay_new.so` auf. Außerdem sind Routinen für alternative Audio-Sample-Rate, Deaktivierung des HU-Audioformats und Aktualisierung der HU-Sample-Rate vorhanden. Unterstützte Klartextformate umfassen AAC-LC, AAC-ELD, Opus und PCM bis 48 kHz.

Das Gerätediagnoselog wurde mit dem Schlüssel `liaoyuan.tech\0` blockweise entschlüsselt. Der Herstellerdatenstrom besitzt einen ungültigen gzip-Trailer: Rohdaten sind weitgehend rettbar, das Dateiende ist jedoch nicht integritätsgesichert. Das gerettete Log bestätigt den aktuell aktiven Modus `aud=2`. Es stammt nicht aus einer aktiven Fahrzeugsitzung und enthält deshalb noch keine belastbaren Musik-Sample-Raten.

`tools/capture_device_state.ps1` wurde erstellt und gegen den eingeschalteten Adapter erfolgreich geprüft. Es liest Hoststatus und Log, entschlüsselt dieses im Salvage-Modus und erzeugt lokale SHA-256-Werte. Keine Firmware wurde hochgeladen oder geflasht.

### 08:46–08:49 CET – Projektverlagerung und Version 0.2.0

Der Chat wurde dem eigenständigen lokalen Projekt `Autoradio - Carplay` mit dem Pfad `E:\WorkSpace\carplay` zugeordnet. Dokumentation, Analysewerkzeuge, Webbelege und Firmwareartefakte wurden aus dem fachfremden Projektordner verschoben.

Stabile Firmware, lokale Weboberfläche und seriennummergebundenes Testabbild wurden bytegenau archiviert. Die damalige Entropie- und Blockstrukturanalyse zeigte bereits eine sektorweise Transformation, konnte sie zu diesem Zeitpunkt aber noch nicht umkehren.

### 08:25–08:42 CET – USB, Funk, Weboberfläche und Audiomodus

Windows erkennt den Adapter als:

- `Apple Mobile Device USB Composite Device`
- USB-ID `VID_05AC/PID_12A8`
- `Apple USB Multiplexor`
- `Apple Mobile Device Ethernet`

Der Adapter stellt ein gerätespezifisches 5-GHz-Netz `smartBox-*` bereit; individuelle Kennungen bleiben in den lokalen Originalbelegen. Zunächst wurde 802.11n auf Kanal 36 beobachtet. Die lokale Oberfläche unter `192.168.1.101` nutzt `/cgi-bin/index.cgi` mit `id=host`, `id=set`, `id=logcat`, `id=upload`, `id=sts` und `id=aa`.

Vor der Untersuchung war `aud=1` aktiv. Als erster reversibler Qualitätstest wurde `aud=2` gesetzt; die API antwortete mit `code=0`, der Adapter startete neu und meldete anschließend `aud=2`. Zusätzlich belegt der eigene Export den späteren API-Aufruf `id=set&wifi=149`; die Funkkonfiguration wurde damit ebenfalls verändert. Die frühere pauschale Aussage, es habe keine weiteren Schreibvorgänge gegeben, war falsch. Es wurde keine Firmware geflasht.

Die installierte Version `26011517.5234.2` wurde mit der stabilen Hersteller-Metadatei abgeglichen. Das Testabbild wurde nur zur Offlineanalyse gesichert.

