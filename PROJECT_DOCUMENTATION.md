# Projektdokumentation

Version: 0.8.2 (Wartungszwischenstand; GerÃƒÂ¤te-UI zuletzt 0.7.0)
Stand: 2026-10-25 12:53 CET

## 2026-10-25

### 12:34Ã¢â‚¬â€œ12:49 CET Ã¢â‚¬â€œ Netzteiltest und ausdrÃƒÂ¼cklich begrenzter Wartungszwischenstand

Der Nutzer bestÃƒÂ¤tigte die Versorgung am USB-Netzteil. Ein einzelner erneuter 0.8.0-Upload nach unabhÃƒÂ¤ngigem Container-/Inodevergleich wurde mit code=0 angenommen. Zuvor wurden sechs aktuelle Ringlogs erneut CRC-/SHA-geprÃƒÂ¼ft gesichert. Zustand 1 blieb ÃƒÂ¼ber mehrere Minuten bestehen; keine Recovery-/Abschlussphase beobachtet. Ein fehlerhafter HTTP-Status unterbrach den ersten Beobachter; ausschlieÃƒÅ¸lich GET-Beobachtung wurde fortgesetzt, kein erneuter POST. Danach kontrollierter API-Neustart und direkter Nachweis von UI 0.7.0/Updatezustand 0. Private Belege: `evidence/updates/2026-10-25-ui080-wall-123512/`.

Auf die Speicherfrage wurden echte Werte nachgelesen: 23.820 KiB verfÃƒÂ¼gbarer RAM und 204/512 KiB freie persistente Logpartition. Customer 3.031.040 Byte passt in 3.801.088 Byte. Dies misst nicht den freien temporÃƒÂ¤ren Dateisystemplatz und schlieÃƒÅ¸t eine Entpackgrenze nicht vollstÃƒÂ¤ndig aus. Ein kleiner fester Check der vier ÃƒÂ¼blichen Debugports fand keinen offenen Dienst; es wurde keine Anmeldung versucht. Der vorhandene Kernel enthÃƒÂ¤lt keinen auswertbaren eingebetteten Rootfs-/Updaterdump; keine fremde Firmware wurde geflasht.

Der Nutzer beschrÃƒÂ¤nkte den nÃƒÂ¤chsten Schritt auf Speicheranzeige, Fehlerprotokoll und LÃƒÂ¶schen der gesicherten Logs. DafÃƒÂ¼r wurde der separate Wartungszweig 0.8.2 aus dem gepinnten tatsÃƒÂ¤chlich installierten 0.7.0 abgeleitet. Die neue Speicherabfrage liest df-KapazitÃƒÂ¤ten fÃƒÂ¼r `/tmp`, UDISK, Customer und Root sowie Beschreibbarkeit; RAM bleibt separat. Fehlerauszug kombiniert festen Updatezustand, Mounts, Updaterprozesse und begrenzte Kernel-/Anwendungs-/vorhandene Updateprotokolle. Browserfehler bleiben begrenzt im Browser-RAM. Es entsteht kein zusÃƒÂ¤tzlicher permanenter Fehlerdateiring. Bestehende Systemlogs enthalten bereits die Rohmeldungen.

LÃƒÂ¶schen wird seriell ÃƒÂ¼ber den Recorder angefordert, bewahrt BootzÃƒÂ¤hler und fremde Daten und startet den Speicherzeitpunkt neu. Die Aufzeichnung lÃƒÂ¤uft weiter. Eine reale LÃƒÂ¶schung wurde noch nicht behauptet.

Der Zwischencontainer lÃƒÂ¤sst ausschlieÃƒÅ¸lich den unverÃƒÂ¤nderten Kernel-Imageblock und Kernelmember weg. Alle Bootenv-Phasen bleiben erhalten. FÃƒÂ¼nf Pfade ÃƒÂ¤ndern sich, alle anderen 0.7.0-Inodes/Daten bleiben unabhÃƒÂ¤ngig geprÃƒÂ¼ft. Zwei Builds sind identisch: 3.034.669 Byte, SHA-256 546416e4d2c3279142d1aa29a3e51e13780e36c0537e7459f9d3b55dc9e02cd4. 32 PythonprÃƒÂ¼fungen, drei JS-PrÃƒÂ¼fprogramme und Shell-/JS-SyntaxprÃƒÂ¼fungen bestehen. Ein einzelner Wartungsupload wurde um 12:48 angenommen; GerÃƒÂ¤tetest lÃƒÂ¤uft. Private Belege: `evidence/updates/2026-10-25-maintenance082-124809/`.

### 12:19 CET Ã¢â‚¬â€œ AbschlieÃƒÅ¸ender GerÃƒÂ¤testands- und Blockerabgleich

Erneut direkt gelesen: UI 0.7.0, Herstellerbasis 26011517.5234.2, Updatezustand 0, aud=3, LED=0, delay=0, conn=cp. Die Laufzeit von 812,67 Sekunden passt zum kontrollierten Neustart um 12:05; ein nachfolgender Kaltstart durch den angefragten Netzteilwechsel ist nicht erkennbar. Kein Flash-/Beobachtungsprozess lÃƒÂ¤uft weiter; beide frÃƒÂ¼heren Beobachtungsprozesse sind terminal. Privater Beleg: `evidence/updates/2026-10-25-ui080/final-idle-audit.json`.

Der fÃƒÂ¼r den nÃƒÂ¤chsten kontrollierten GerÃƒÂ¤teversuch angeforderte Netzteilwechsel ist weiterhin unbestÃƒÂ¤tigt. Dieser externe Schritt blieb seit dem ursprÃƒÂ¼nglichen 0.8.0-Arbeitsblock und der folgenden Offline-Diagnosevorbereitung offen. Alle notwendigen bisherigen OfflineprÃƒÂ¼fungen sind durchgefÃƒÂ¼hrt; eine GerÃƒÂ¤teinstallation, ein LED-Schalttest, die erweiterte Hardwareabfrage und die beauftragte LoglÃƒÂ¶schung sind noch nicht verifiziert. Der bereits gesicherte Fahrzeuglog bleibt erhalten. Keine weitere Installation oder LÃƒÂ¶schung wurde behauptet oder wiederholt; weitere GerÃƒÂ¤tearbeit wartet auf die RÃƒÂ¼ckmeldung zum physischen Anschluss.

### 12:11Ã¢â‚¬â€œ12:14 CET Ã¢â‚¬â€œ Offline-Messstelle fÃƒÂ¼r die 8-/16-kHz-Auswahl

Der vorherige Arbeitsblock war Fortschritt: Einstellungen und LÃƒÂ¶schung gebaut/geprÃƒÂ¼ft, Updatezustand untersucht und normaler Betrieb wiederhergestellt. Aktueller Read-only-Abgleich bestÃƒÂ¤tigt Updatezustand 0, UI 0.7.0, aud=3, LED=0, delay=0 und unverÃƒÂ¤nderte Herstellerbasis. BestÃƒÂ¤tigung des angeforderten Netzteilwechsels fehlt; es wurde kein weiterer Upload gestartet. Kein Beobachtungsprozess wird als weiterlaufender Flash ausgegeben.

UnabhÃƒÂ¤ngig davon wurden die erhaltenen Fahrzeuglogs erneut auf vollstÃƒÂ¤ndige Radio-/Plugin-/FÃƒÂ¤higkeitsdaten geprÃƒÂ¼ft. Sie enthalten die gewÃƒÂ¤hlte audioFormat=4 und 8-kHz-Strecke, aber weiterhin keine verwendete vollstÃƒÂ¤ndige Maske/Plugin-Version. Die zwei bestehenden Logstellen bei 0x2BF80/0x2C088 erlauben eine eng begrenzte Beobachtung dieser EingÃƒÂ¤nge. Je ein vier Byte langer Logargumentaufbau wird durch c.lwsp a2,Offset(sp) und c.mv a3,s2 ersetzt; der vorhandene Formattext wird in-place zu BH_HU mask=%08x gate=%u. Dadurch unterscheiden sich exakt 38 Byte in drei Regionen; Audioauswahl, Branches, Logaufrufe und DateigrÃƒÂ¶ÃƒÅ¸e bleiben erhalten.

Das neue tools/prepare_phone_probe.py prÃƒÂ¼ft zuerst den gepinnten Quellhash, alle ursprÃƒÂ¼nglichen Bytes und anschlieÃƒÅ¸end jeden geÃƒÂ¤nderten Dateioffset. Capstone dekodiert die neuen Instruktionen unabhÃƒÂ¤ngig; drei lokale Tests bestehen. Kandidat: 209.188 Byte, SHA-256 2cbbaf825e8b3038ac9c53153b5ca6bd8800e121ce89d9526808846f2842fb40. Output nur unter dist/phone-probe-0.8.1, nicht integriert, nicht ausgefÃƒÂ¼hrt und nicht geflasht. phone_probe.md beschreibt Grenzen, insbesondere gate=0 als mÃƒÂ¶glicherweise ungeparsten Versionswert. Projektanalyseversion 0.8.1 ist von installiertem UI 0.7.0 und gesperrtem UI-Kandidaten 0.8.0 getrennt.

### 11:52Ã¢â‚¬â€œ12:08 CET Ã¢â‚¬â€œ Updatevorbereitung hÃƒÂ¤ngt, kontrollierter Normalstart, erneuter Test vorbereitet

0.8.0 wurde einmal ÃƒÂ¼ber den vorhandenen Browser-Updater ÃƒÂ¼bertragen. GerÃƒÂ¤te-CGI bestÃƒÂ¤tigte den Upload nach rund zwei Sekunden. Der Status blieb anschlieÃƒÅ¸end bei 1 und Herstellerbasis 26011517.5234.2; keine Recoveryphase 2 und kein Abschluss 3 beobachtet. Die Fortschrittsanzeige oberhalb 70 % ist im ursprÃƒÂ¼nglichen cpbox.js zeitbasiert und belegt keine ÃƒÂ¼bertragenen Bytes oder Flashfortschritte. Der normale OberflÃƒÂ¤chen-Code wurde deshalb nach bestÃƒÂ¤tigtem Upload verlassen, um automatische Abfragen zu stoppen. Kein zweiter Upload wurde automatisch gestartet.

Aktuelle Logdaten und beide Beobachtungsintervalle liegen unter `evidence/updates/2026-10-25-ui080/`. Nach lÃƒÂ¤nger unverÃƒÂ¤nderter Vorbereitung wurde der vorhandene normale API-Neustart gezielt einmal aufgerufen. Danach lÃƒÂ¤uft dasselbe GerÃƒÂ¤t wieder mit Updatezustand 0 und weiterhin UI 0.7.0. Installation und LoglÃƒÂ¶schung sind damit noch nicht erreicht. Das ÃƒÂ¶ffentliche 0.8.0-Manifest wurde bis zum erfolgreichen GerÃƒÂ¤tetest deaktiviert. FÃƒÂ¼r einen kontrollierten neuen Versuch wurde der Nutzer gebeten, wie bei den bisherigen erfolgreichen Updates ein USB-Netzteil zu verwenden.

Parallel fragte der Nutzer nach einem Emulator als PrÃƒÂ¼fstand. Apples eigenstÃƒÂ¤ndiger Mac-Simulator mit echtem iPhone wurde von seinem Xcode-Simulationsfenster unterschieden; LIVI/Linux setzt zusÃƒÂ¤tzliche CarPlay-Authentifizierung voraus. Ein Windows-/Hyundai-PrÃƒÂ¼fstand fÃƒÂ¼r diesen Dongle ist noch nicht verifiziert. Es wurde keine Emulatorsoftware installiert. `hardware_limits.md` dokumentiert bestÃƒÂ¤tigte Bauteile, Reserven und Grenzen. Der originale DTB wurde zusÃƒÂ¤tzlich geprÃƒÂ¼ft: ein Linux-CPU-Knoten, 16-KiB-I-/D-Caches, zunÃƒÂ¤chst referenzierte 360Ã¢â‚¬â€œ960-MHz-Tabelle und alternative Tabellen bis 1.200 MHz. Laufzeitauswahl/Takt bleiben bis zum GerÃƒÂ¤tezugriff offen.

### 11:44Ã¢â‚¬â€œ11:55 CET Ã¢â‚¬â€œ VerstÃƒÂ¤ndliche Bedienung, Hardwareabfrage und begrenzte LoglÃƒÂ¶schung 0.8.0

Der Nutzer bestÃƒÂ¤tigte LED Default=Ein und Mode 1=Aus und beauftragte einen Schalter, verstÃƒÂ¤ndliche Einstellungsbeschreibungen, Hardware-/MaximalprÃƒÂ¼fung sowie Sicherung und LÃƒÂ¶schung der Logs. Vor Ãƒâ€žnderungen wurden alle sechs aktuellen gzip-Dateien samt Metadaten und frischem Systemlog unter `evidence/log-backups/2026-10-25-114454/` gesichert und CRC-/SHA-256-geprÃƒÂ¼ft. LÃƒÂ¶schung ist bis zur verfÃƒÂ¼gbaren geprÃƒÂ¼ften GerÃƒÂ¤tefunktion noch offen.

Das neue Einstellungsmodul zeigt einen echten LED-Schalter, Telefonpuffer mit belegter Wirkung und ausdrÃƒÂ¼cklich ungeklÃƒÂ¤rten Profilfeinheiten sowie Verbindungsstart statt Delayed start. Im Original-rcpservice belegt der Getter 0x21520 und dessen Aufruf bei 0x141D4: delay=2 fÃƒÂ¼hrt ÃƒÂ¼ber 0x15068 zu sleep(20). FÃƒÂ¼r delay=1 ist keine feste zusÃƒÂ¤tzliche Sekundenanzahl belegt. Es wurden keine Klangversprechen oder erfundenen Zeitwerte ergÃƒÂ¤nzt.

Die Hardwarekarte trennt bestÃƒÂ¤tigte Startlogdaten von Treiberhinweisen. Eine feste CGI-Abfrage liest CPU-/RAM-/MTD-/Mount-/cpufreq-/USB-/SDIO-Daten und verfÃƒÂ¼gbare lokale Buswerkzeuge. Der Hersteller beschreibt die V821-Familie als heterogenes CPU/MCU-System; die aktuelle Allwinner-Seite bezieht sich ausdrÃƒÂ¼cklich auf V821L2-WXX, also keine ungeprÃƒÂ¼fte Taktaussage ÃƒÂ¼ber unseren V821B. Mikrofonraten werden richtig als 8Ã¢â€ â€™16 kHz angezeigt, Netzwerkinterfaces getrennt erfasst. Der Recorder bewahrt frÃƒÂ¼he HU-Auswahllogs im begrenzten RAM-Verlauf auf.

Die neue LÃƒÂ¶schanforderung darf ausschlieÃƒÅ¸lich die sechs eigenen Logslots und eigene RAM-Snapshots entfernen, erhÃƒÂ¤lt BootzÃƒÂ¤hler und fremde Daten und wird seriell vom Recorder abgearbeitet. Tests prÃƒÂ¼fen diesen Umfang, Origin-/Methodengrenzen, LED-Mapping und reale Mikrofonlogeinheit. 27 PythonprÃƒÂ¼fungen und drei JS-PrÃƒÂ¼fprogramme bestehen. Zwei Builds sind identisch: 6.199.341 Byte, SHA-256 `47276c8e59417f3346d67489f8dd14a0ff6717721797a43b2c139fab49d54f46`. Elf Pfade ÃƒÂ¤ndern sich; Audio-BinÃƒÂ¤rdateien, Kernel und ÃƒÂ¼brige Originalinodes bleiben unverÃƒÂ¤ndert. GerÃƒÂ¤teinstallation und reale Hardware-/LÃƒÂ¶schprÃƒÂ¼fung stehen bei diesem Eintrag noch aus.

### 11:29Ã¢â‚¬â€œ11:41 CET Ã¢â‚¬â€œ Erster Teams-Feldtest, 8-kHz-Engpass, Analyseversion 0.7.1

Der Nutzer meldete vorhandene Fahrzeuglogs. Der PC war zunÃƒÂ¤chst nicht im Adapter-WLAN; Windows wiederholte erfolglose Sicherheitsanmeldungen. Das vorhandene Profil wurde vor einer erneuten WPA2/AES-Parametrierung lokal gesichert; es enthielt bereits AES, die angezeigte GCMP/CCMP-Auswahl blieb bestehen. Eine kausale Profilreparatur ist daher nicht bewiesen. Nach Wiederverbindung gelang der Zugriff. Nutzer stellte klar, dass das iPhone bereits getrennt war. Keine GerÃƒÂ¤te-IP, kein Audiomodus und keine Firmware wurden in diesem Block geÃƒÂ¤ndert.

Alle sechs Ringdateien aus Starts 5/6/7 wurden samt Hoststatus und frischem PC-Log gesichert. gzip-CRC und GerÃƒÂ¤tidentitÃƒÂ¤t geprÃƒÂ¼ft; Rohdaten bleiben unter `evidence/field-tests/2026-10-25-113352/`. Start 5 enthÃƒÂ¤lt Mode 2, Start 6 Mode 3, Start 7 die PC-Sitzung. Nutzer bestÃƒÂ¤tigt beide Versuche als Teams und subjektiv besseren, aber weiterhin gedÃƒÂ¤mpften Ton nach Moduswechsel.

Die Fahrzeuglogs zeigen ÃƒÂ¼bereinstimmend Telefon-Audiotyp 8 mit 16.000 Hz/16 Bit/Mono auf iPhone-Seite und 8.000 Hz/16 Bit/Mono beim USB-Telefonstart. Die HU-TaktrÃƒÂ¼ckmeldungen liegen bei etwa 8.000 Hz; Mikrofonumwandlung 8.000Ã¢â€ â€™16.000 ist ebenfalls protokolliert. Die Herstellerbeschriftung `8000kHz -> 16000kHz` ist falsch: Konvertervariablen und Aufbau im Originalcode sind in Hz. Die installierte Webauswertung ÃƒÂ¼bernimmt diesen Einheitenfehler; im neuen Offlinewerkzeug ist die Auswertung korrekt. Kein PCM-/Kabelvergleich und keine vollstÃƒÂ¤ndige Klangursache behauptet.

Der Originalcode `rcpservice` ab 0x2BEAC ruft GetHUAudioFormat/GetHUPluginVer auf. Bit 2 fÃƒÂ¼hrt zunÃƒÂ¤chst zu 8 kHz; der Versionsvergleich gegen 319 bei 0x2C06A kann die folgende PrÃƒÂ¼fung auf Bit 4/16 kHz ÃƒÂ¼berspringen. Weitere Zweige wÃƒÂ¤hlen unmittelbar 16 kHz. Die echten Eingangsmasken und Plugin-Version fehlen im Logausschnitt. Daher ist weder eine feste Hardwaregrenze noch ein sicherer Rate-Override bewiesen.

`tools/analyze_field_logs.py` prÃƒÂ¼ft Archive offline, trennt Boots, dedupliziert ÃƒÂ¼berlappende Zeilen, hÃƒÂ¤lt Telefon und Audiotyp 64 auseinander und wertet Messpunkte getrennt aus. Regressionen decken echte Logformate/Einheiten, ÃƒÅ“berlappung, getrennte Starts und defekte CRC ab. 26 PythonprÃƒÂ¼fungen und beide JavaScript-PrÃƒÂ¼fprogramme bestehen. Feldbericht `field_test_2026-10-25.md` dokumentiert Befunde, Grenzen und nÃƒÂ¤chsten Schritt: initiale FÃƒÂ¤higkeits-/Versionsdaten sichern. Projektversion 0.7.1 bezeichnet Analyse/Dokumentation, installiert und im OTA-Manifest bleibt 0.7.0. Keine Audiosoftware verÃƒÂ¤ndert oder geflasht.

### 10:54Ã¢â‚¬â€œ10:55 CET Ã¢â‚¬â€œ Echte Stromtrennung bestanden

Der Nutzer bestÃƒÂ¤tigte den erneuten Anschluss diesmal am PC. Nach verzÃƒÂ¶gerter Windows-WLAN-Wiederverbindung ist derselbe Adapter erreichbar, Recorder aktiv und BootzÃƒÂ¤hler 3. Beide Boot-1-Logs stimmen weiterhin SHA-256-genau mit den vor Software-Neustart und Stromtrennung geladenen Dateien ÃƒÂ¼berein; gzip-CRC gÃƒÂ¼ltig. FÃƒÂ¼nf Dateien aus drei Starts sind vorhanden, 252 von 512 KiB frei. Die Liveanzeige aktualisiert sich wieder automatisch, weiterhin ohne Browseraufzeichnung. Der zuvor offene Kaltstartpunkt ist erledigt. Kein weiterer Flash war nÃƒÂ¶tig. Beleg: `persistence.after-power.json` und `installed-diagnostics.png` im lokalen Updateordner; ÃƒÂ¶ffentliche Nachweise enthalten keine Rohlogs/GerÃƒÂ¤tekennungen. Der Fahrzeug-/Teams-Test und jede behauptete Audioverbesserung bleiben ausdrÃƒÂ¼cklich offen.

### 10:48Ã¢â‚¬â€œ10:53 CET Ã¢â‚¬â€œ Echte Installation und Software-NeustartprÃƒÂ¼fung 0.7.0

Das ÃƒÂ¶ffentlich geladene Image wurde vorab per GrÃƒÂ¶ÃƒÅ¸e/SHA-256 geprÃƒÂ¼ft und einmal ÃƒÂ¼ber den echten Browser-Updater ÃƒÂ¼bertragen. Zustand 1Ã¢â€ â€™2Ã¢â€ â€™3 und anschlieÃƒÅ¸ender Normalstart sind beobachtet. Sieben statische Webdateien stimmen mit dem Build ÃƒÂ¼berein. Der CGI meldet 58.124 KiB nutzbaren RAM, CPU im Messintervall etwa 3,4Ã¢â‚¬â€œ6 % und echte 512 KiB Datenspeicher, zunÃƒÂ¤chst 304 KiB frei. Der Logger lÃƒÂ¤uft und erzeugt CRC-gÃƒÂ¼ltige 13-KiB-gzip-Dateien mit Messpunkten.

Zwei Browserbeobachtungen im Abstand von 22 Sekunden zeigen aktualisierte Laufzeit/Abfragezeit bei weiterhin null aufgezeichneten Browsermesspunkten: automatische Anzeige ist unabhÃƒÂ¤ngig vom Aufzeichnungsstart bestÃƒÂ¤tigt. Sofortspeicherung per SchaltflÃƒÂ¤che und Audioauswertung aus dem gespeicherten Slot funktionieren. AnschlieÃƒÅ¸end blieben beide Boot-1-Dateien ÃƒÂ¼ber einen kontrollierten Neustart SHA-256-identisch. Der neue Start zÃƒÂ¤hlt korrekt auf Boot 2 hoch. GitHub CI 40182107570 erfolgreich.

Der Nutzer trennte auf Anforderung den Strom und bestÃƒÂ¤tigte erneuten Anschluss. Danach ist das Adapter-WLAN bisher nicht wieder sichtbar; der Kaltstartvergleich ist noch offen. Keine weitere FirmwareÃƒÂ¼bertragung wurde wiederholt. Individuelle Belege bleiben lokal unter `evidence/updates/2026-10-25-105000-ui070/`.

### 10:16Ã¢â‚¬â€œ10:47 CET Ã¢â‚¬â€œ GerÃƒÂ¤teprÃƒÂ¼fung 0.6.0, Liveanzeige und persistente Logs 0.7.0

0.6.0 wurde ÃƒÂ¼ber den eingebetteten ÃƒÂ¶ffentlichen Updatekanal heruntergeladen, geprÃƒÂ¼ft und installiert. Recovery 2Ã¢â€ â€™3, kontrollierter Normalstart, Herstellerbasis 26011517.5234.2 und sieben Webdateihashes sind bestÃƒÂ¤tigt. Der CGI lieferte echte Werte, einen frischen 60.935-Byte-Log und korrekte Methodengrenzen. Belege: `evidence/updates/2026-10-25-101652-ui060/`. Der historische offene Installationspunkt ist erledigt.

Idle-Jiffies blieben auf dem echten GerÃƒÂ¤t stehen, obwohl `/proc/uptime` Idle-Sekunden weiterzÃƒÂ¤hlte. Der Fix nutzt Laufzeit, Idle-Sekunden und CPU-Anzahl: reales Vergleichspaar 64,3939 % statt falscher 100 %. Die zweimal gebaute Zwischenversion 0.6.1 wurde weder verÃƒÂ¶ffentlicht noch installiert; der Fix geht in 0.7.0 ein.

Der Nutzer beauftragte persistente Systemlogs und automatische CPU/RAM/Laufzeit. Browser-JavaScript fragt alle zwei Sekunden ab, unabhÃƒÂ¤ngig von optionaler Aufzeichnung. Das native Shellskript startet ÃƒÂ¼ber das minimal ergÃƒÂ¤nzte originale `lyLink.sh`, auÃƒÅ¸erhalb Recovery. Es prÃƒÂ¼ft den RW-Datenmount und freien Platz, hÃƒÂ¤lt Status alle fÃƒÂ¼nf Sekunden in RAM und schreibt etwa alle 60 Sekunden gzip-Snapshots. Drei Startslots mit je zwei Dateien bis 24 KiB und 64 KiB Mindestreserve begrenzen den Platz. Neue Dateien werden CRC-geprÃƒÂ¼ft, synchronisiert und atomar umbenannt. Kein Formatieren/Mounten/Rohflashzugriff.

Die Seite ergÃƒÂ¤nzt Speicherstatus, Downloads, Sofortspeicher-Anforderung und Audioauswertung frÃƒÂ¼herer Logs. Nur feste IDs sind zugelassen. Das echte Skript besteht Tests zu vier Starts, CRC, fremden Dateien, RAM-/RO-/fehlenden Mounts, Platzmangel und ÃƒÂ¼bergroÃƒÅ¸en Logs. 24 PythonprÃƒÂ¼fungen und beide JavaScriptprogramme bestehen. Zwei Builds sind identisch: 6.199.341 Byte, SHA-256 `32e395c7ff22fcf40eb019748126e554694786974d261f70ab4fe07171e6aeb4`. Zehn erlaubte Dateien ÃƒÂ¤ndern sich; alle anderen Originalinodes und Kernel bleiben erhalten. GerÃƒÂ¤teinstallation und echter Persistenztest stehen bei diesem Eintrag noch aus.

### 10:07Ã¢â‚¬â€œ10:16 CET Ã¢â‚¬â€œ Integrierte Diagnose, Version 0.6.0

Der Nutzer fragte nach Analysewerkzeugen und bestÃƒÂ¤tigte ausdrÃƒÂ¼cklich die Integration in die Einstellungsseite. ErgÃƒÂ¤nzt wurden eine sichtbare Diagnosekarte und ein eng begrenzter Shell-CGI mit ausschlieÃƒÅ¸lich festen GET-Abfragen fÃƒÂ¼r Status, Audioausschnitt und lokalen Logdownload. POST, zusÃƒÂ¤tzliche Parameter, Kommandos und Dateipfade werden abgewiesen. Der CGI liest proc/sys, dmesg und `logcat -d`; er lÃƒÂ¶scht keine Puffer, schreibt nicht in den Flash und nutzt nicht den alten `/tmp/log.gz`-Cache.

Die OberflÃƒÂ¤che berechnet CPU aus zwei ZÃƒÂ¤hlerstÃƒÂ¤nden, zeigt Speicher und Laufzeit, USB-Zustand und kumulative WLAN-Drops. Aufzeichnung erfolgt im Browser mit hÃƒÂ¶chstens 900 Messpunkten bei zwei Sekunden Abstand. JSON- und Logexport bleiben lokal. Telefon-Ausgabe und Mikrofonumwandlung werden ausschlieÃƒÅ¸lich aus konkret vorhandenen Hersteller-Logformaten gelesen. Insbesondere wird 48-kHz-Musik nicht als Telefonrate ausgegeben und fehlende Daten werden nicht durch Annahmen ersetzt.

Der SquashFS-Patcher setzt ausschlieÃƒÅ¸lich den neuen Diagnose-CGI auf ausfÃƒÂ¼hrbaren Modus 0755; alle ursprÃƒÂ¼nglichen Dateimetadaten bleiben erhalten. Zwei neue Builds sind byteidentisch: 6.195.245 Byte, SHA-256 `af5c80bca12b13eca5f14481ef30b9955cd1d711d7a49199ca209f8edd2c5bdb`. Acht Dateien werden ergÃƒÂ¤nzt/ersetzt, Kernel und Updatebeschreibung bleiben original. 19 PythonprÃƒÂ¼fungen und beide JavaScript-PrÃƒÂ¼fprogramme bestehen. Die Shelltests wurden unter Git-for-Windows mit LF-Fixtures ausgefÃƒÂ¼hrt; Windows-CRLF in kÃƒÂ¼nstlichen sysfs-Dateien wurde in den Fixtures korrigiert.

Die GerÃƒÂ¤teinstallation dieser Version steht zum Zeitpunkt dieses Eintrags noch aus. Ziel ist der echte eigene GitHub-Updatekanal der bereits installierten 0.5.0-OberflÃƒÂ¤che.

### 09:39Ã¢â‚¬â€œ10:03 CET Ã¢â‚¬â€œ RÃƒÂ¼ckweg untersucht, ausdrÃƒÂ¼ckliche Risikofreigabe, echte Installation, Version 0.5.1

Die vorherige Fortsetzung war Fortschritt: echter Kandidat und ÃƒÂ¶ffentliches Repository waren vorhanden. Upstream-xfel 1.4.0 wurde aus der originalen Windowsfreigabe geladen, gegen den Releasehash und zusÃƒÂ¤tzlich EXE-/DLL-Hashes geprÃƒÂ¼ft. Die reale Probe meldet kein FEL-GerÃƒÂ¤t. Ein lesendes Zwei-Pass-Backupwerkzeug wurde ergÃƒÂ¤nzt und gegen kurze, abweichende und beschÃƒÂ¤digte Daten getestet. Diese synthetischen PrÃƒÂ¼fungen behaupten weder einen realen Dump noch einen Restore. Der aktuelle CatPlay-Weg `cpbox2fel.py` wurde nur gelesen: Er flasht zuerst ein modifiziertes OTA und hat keinen ly5234-Preset. Deshalb ist er kein unabhÃƒÂ¤ngiger Backupweg vor dem ersten Flash.

Die Hardwarebewertung wurde prÃƒÂ¤zisiert: `RTL8723FS` stammt aus dem Bluetooth-Initialisierungspfad, der eigene Kernel enthÃƒÂ¤lt `8733bs`/`RTL8733B` als WLAN-Treiber. FrÃƒÂ¼here historische Formulierungen Ã¢â‚¬Å¾Funkchip RTL8723FSÃ¢â‚¬Å“ sind damit eingeschrÃƒÂ¤nkt, kein physischer WLAN-Chipnachweis.

Der Nutzer schloss Platinenzugang aus und wies ausdrÃƒÂ¼cklich an, den Updatepfad zu verwenden; einen mÃƒÂ¶glichen zerstÃƒÂ¶rten Dongle und Ersatzkauf akzeptiert er. Damit wurde die ursprÃƒÂ¼ngliche Backup-Voraussetzung fÃƒÂ¼r den ersten gezielten Updateversuch aufgehoben. Es erfolgte keine erneute Nachfrage nach dieser Risikofreigabe.

Der Adapter war zeitweise abgesteckt; nach erneutem Anschluss bekam Windows zunÃƒÂ¤chst nur APIPA. Die WLAN-IP-Ãƒâ€žnderung scheiterte im Agentprozess an fehlenden Administratorrechten. Der Nutzer setzte eine statische Adresse und korrigierte sie spÃƒÂ¤ter auf `.104`; eine alte zusÃƒÂ¤tzliche `.2` wurde entfernt. Zwischenzeitlich wurden USB-Netzteilversorgung und erneute WLAN-Verbindung getestet. SÃƒÂ¤mtliche bis dahin gescheiterten Versuche brachen im lesenden Preflight ab. Es gab nur einen echten Firmwareupload.

Um 09:59:44 CET wurde das vollstÃƒÂ¤ndig geprÃƒÂ¼fte 6.187.053-Byte-Image einmal per multipart hochgeladen und mit `code=0 / upload successful` bestÃƒÂ¤tigt. Original und Kandidat nutzen XZ-CRC32 (Check-ID 1). Danach wurden GerÃƒÂ¤teidentitÃƒÂ¤t und UpdaterzustÃƒÂ¤nde 2 und 3 beobachtet. Im Recoveryzustand meldete der CGI `00000000.5234.2` und lieferte keine normale statische OberflÃƒÂ¤che. Das GerÃƒÂ¤t wurde erst nach bestÃƒÂ¤tigtem Zustand 3 ÃƒÂ¼ber den dokumentierten Herstelleraufruf `id=set&conn=cp` neu gestartet.

Nach dem Normalstart meldet das eigene GerÃƒÂ¤t wieder `26011517.5234.2`, Updater 0, `aud=2`, `mic=0`, `sig=149`, `conn=cp`. Alle sechs UI-Dateien wurden direkt ÃƒÂ¼ber `192.168.1.101` abgerufen und per SHA-256 mit dem Build abgeglichen. Die echte GerÃƒÂ¤teoberflÃƒÂ¤che wurde im Browser geÃƒÂ¶ffnet. Die eigene Firmware-UI bleibt 0.5.0; Projekt-/Werkzeugfixstand ist 0.5.1. Audio-/Fahrzeugfunktion und Wiederherstellung bleiben ungetestet.

Lokale individuelle Belege liegen unter `evidence/updates/2026-10-25-095944/` und bleiben vom ÃƒÂ¶ffentlichen Repository ausgeschlossen. Der ÃƒÂ¶ffentliche Nachweis enthÃƒÂ¤lt nur Dateihashes, Status und erhaltene Einstellungen. Der Nutzer beauftragte anschlieÃƒÅ¸end einen eigenen lesenden Diagnosebereich; diese Erweiterung wird getrennt versioniert.

### 09:20Ã¢â‚¬â€œ09:37 CET Ã¢â‚¬â€œ Eigene OberflÃƒÂ¤che, Firmwarekandidat und GitHub, Version 0.5.0

Der Nutzer beauftragte ein lokales Bad-Hippo-SVG und dunkles Design in den GerÃƒÂ¤teeinstellungen, anschlieÃƒÅ¸end ausdrÃƒÂ¼cklich die Untersuchung des Firmware-Downloads, den Bau eines verÃƒÂ¤nderten Updates und eine dauerhaft eigene Updateadresse. Als Hostingwunsch wurde zunÃƒÂ¤chst ein privates GitHub-Repository genannt und anschlieÃƒÅ¸end ausdrÃƒÂ¼cklich auf ÃƒÂ¶ffentlich geÃƒÂ¤ndert. `kamohy/smartbox-carplay` wurde entsprechend angelegt und die ÃƒÂ¶ffentliche Sichtbarkeit verifiziert. Der GitHub-Connector bietet kein Anlegen von Repositories; dafÃƒÂ¼r wurde die bereits angemeldete GitHub-CLI desselben Kontos genutzt.

Die echte Herstelleradresse wurde aus `cpbox_init()`/`cpbox_geturl()` und dem Live-Manifest bestÃƒÂ¤tigt: `cpbox-abroad.oss-us-west-1.aliyuncs.com/5234/`. Das aktuelle Manifest ist byteidentisch mit dem Archiv. DNS lieferte zu diesem Zeitpunkt `47.254.114.108`. Der Browser lÃƒÂ¤dt die Firmware und sendet sie dann per multipart an `id=upload`; es ist kein DNS-/TLS-Abfangen nÃƒÂ¶tig. Die im CGI sichtbaren HMAC-SHA1-Begriffe gehÃƒÂ¶ren zum Cloud-/STS-Kontext und wurden nicht als Firmware-Signatur behauptet. Der separate Updater-/Recoverypfad ist noch nicht vollstÃƒÂ¤ndig prÃƒÂ¼fbar.

Die HTML-Struktur der Herstellerfunktionen bleibt erhalten; ergÃƒÂ¤nzt sind Header, lokal gespeichertes Logo, dunkles CSS und eigene Update-JavaScripts. Ein wichtiger Laufzeitpunkt wurde berÃƒÂ¼cksichtigt: `lyUpdate.sh` bindet keinen beliebigen neuen `/assets`-Ordner ein. Das SVG liegt deshalb in `/css`, die neue Updatekonfiguration in `/js`.

Die feste neue Manifestadresse lautet `https://raw.githubusercontent.com/kamohy/smartbox-carplay/main/ota/5234/version.json`. Ein ÃƒÂ¶ffentliches Repository braucht keinen eingebetteten GitHub-ZugangsschlÃƒÂ¼ssel. Der eigene Updater prÃƒÂ¼ft Plattform, Herstellerbasis, numerische Projektversion, Freigabestatus, erlaubten Downloadpfad, LÃƒÂ¤nge und SHA-256. Die erste Version wird als nicht freigegebener Kandidat gefÃƒÂ¼hrt.

Ein eng begrenzter Rust-Helfer auf Basis von Backhand 0.25.5 verÃƒÂ¤ndert nur Dateien unter `/ota/www/`. Der Python-Builder prÃƒÂ¼ft zuerst das fest gepinnte Original und reproduziert dessen vollstÃƒÂ¤ndigen XOR-/MD5-/CRC-CPIO-Container byteidentisch. Das neue SquashFS wird unabhÃƒÂ¤ngig mit Dissect gelesen. Alle 66 originalen EintrÃƒÂ¤ge einschlieÃƒÅ¸lich Dateimodi, EigentÃƒÂ¼mern, Zeitstempeln und `/dev/console` bleiben erhalten. Kernel und `sw-description` sind byteidentisch. Exakt sechs UI-Dateien sind ersetzt/ergÃƒÂ¤nzt; Audio-Programme wurden nicht verÃƒÂ¤ndert.

Zwei unabhÃƒÂ¤ngige Buildausgaben sind byteidentisch: 6.187.053 Byte, SHA-256 `3b1d45b1ca75b9462bfc53974b5d34c6f28aef9b4f0761c746f1cb0923074581`. Customer bleibt mit 3.018.752 Byte unter der 3.801.088-Byte-Partitionsgrenze. Elf PythonprÃƒÂ¼fungen bestehen; JavaScript-SHA-256 wurde gegen Node-Krypto bis zu 1.000.000 Byte sowie an Paddinggrenzen geprÃƒÂ¼ft. Versionen, Fremdplattformen, URL-Regeln, gesperrte Updates und beschÃƒÂ¤digte Downloads sind abgedeckt.

Der Andes-Decoder wurde zusÃƒÂ¤tzlich korrigiert: BEQC/BNEC-Konstanten sind unsigned 7-Bit. Ein externer Opcodevektor mit Konstante 64 sichert diesen Fall ab; bisherige kleine Audio-Vergleichswerte ÃƒÂ¤ndern sich nicht.

Die lokale Vorschau verwendet echten lesenden Hoststatus und sperrt Schreib-/Uploadzugriffe. Ein HTTP-Hashvergleich bestÃƒÂ¤tigt die unverÃƒÂ¤nderte Originalseite auf dem Adapter. Keine neue GerÃƒÂ¤teeinstellung wurde in diesem Arbeitsblock geschrieben, keine Firmware hochgeladen oder geflasht. Die laufende Untersuchung bleibt vor einem Flash an den noch fehlenden vollstÃƒÂ¤ndigen Backup-/Recoveryweg gebunden. Der Firmwarekandidat belegt den Bau, noch nicht den erfolgreichen Erststart.

### 09:15Ã¢â‚¬â€œ09:19 CET Ã¢â‚¬â€œ Teams-Vergleich prÃƒÂ¤zisiert, Version 0.4.1

Der Nutzer prÃƒÂ¤zisierte, dass der blecherne Klang bei Telefonaten mindestens ÃƒÂ¼ber Teams auftritt. Auf Nachfrage bestÃƒÂ¤tigte er beide Richtungen und deutlich besseren Teams-Klang am selben iPhone per direktem USB-Kabel. Die bisherige Annahme eines primÃƒÂ¤ren Musikfehlers wurde daher zurÃƒÂ¼ckgenommen. Die weitere Diagnose priorisiert den bidirektionalen Telefonpfad; die 44,1-/48-kHz-Musikmodifikation ist kein belegter Teams-Fix.

Im stabilen `lylinkapp` wurde der Telefonzweig von `AudioPlayerCreate` ab `0x1D50C` verfolgt: Eigene Radio-Telefonrate/Kanalzahl, fest 16 Bit. Der Mikrofon-/HID-Pfad ab `0x164FC` erzeugt bei abweichendem Radioformat zwei Umwandler zu/von intern 16.000 Hz, 16 Bit, Mono; der Siri-Pfad verwendet 24.000 Hz. Die zugehÃƒÂ¶rigen FFmpeg-Funktionen fÃƒÂ¼r Eingabe-/Ausgaberate und Kanalbelegung wurden direkt im Code bestÃƒÂ¤tigt. Das ist ein zusÃƒÂ¤tzlicher Verarbeitungsschritt, aber ohne aktives Teams-Log noch keine bewiesene Ursache.

Die Fahrzeuganleitung wurde auf Teams-Ausgabe und MikrofonqualitÃƒÂ¤t umgestellt. Eine generelle Stereo-Forderung ist bei Telefonaten falsch; Mono und Sprach-Sample-Raten sind zunÃƒÂ¤chst regulÃƒÂ¤r. GeprÃƒÂ¼ft werden muss die konkrete Verschlechterung gegenÃƒÂ¼ber dem bestÃƒÂ¤tigten Kabelvergleich. Keine GerÃƒÂ¤teeinstellungen wurden verÃƒÂ¤ndert und keine Firmware geflasht.

### 09:00Ã¢â‚¬â€œ09:12 CET Ã¢â‚¬â€œ Weitere Programme, valide Logs und Version 0.4.0

Der vorherige Turn war Fortschritt: Projektdateien waren verschoben und der Stand 0.3.0 geprÃƒÂ¼ft. Der Adapter wurde erneut lesend erreicht; er meldet weiter Firmware `26011517.5234.2`, `aud=2` und WLAN-Konfiguration 149. Es wurde in dieser Fortsetzung keine Konfiguration verÃƒÂ¤ndert oder Firmware ÃƒÂ¼bertragen.

Das Analysewerkzeug dekodiert jetzt GP-relative Andes-Lade-/Speicherbefehle und unmittelbare VergleichssprÃƒÂ¼nge. Die ADDIGP-Maske wurde korrigiert: Bit 14 gehÃƒÂ¶rt zum Offset und darf nicht als festes Opcodebit behandelt werden. Referenz ist der vom Andes-Entwickler verÃƒÂ¶ffentlichte XAndesPerf-binutils-Patch.

Eine weitere Verpackungsschicht wurde in `customer/app/lylink` identifiziert. `tools/extract_lypack.py` entfernt die 128-Byte-Kopfmaskierung, verarbeitet lokale ZIP-Header und prÃƒÂ¼ft jeden Deflate-Stream einschlieÃƒÅ¸lich CRC32. Aus beiden Updates wurden je sechs zusÃƒÂ¤tzliche ELF-Dateien gewonnen, darunter die bisher nicht zugÃƒÂ¤nglichen Programme `rcpservice`, `librcarplay.so` und `liblylinkpcm.so`. Zwischen stabiler und Testversion ÃƒÂ¤ndern sich drei dieser sechs Dateien.

Ein frÃƒÂ¼herer Befund wurde korrigiert: `UpdateHUSamplerate` und `DisableHUAudioFormat` sind in der stabilen Bibliothek nur Platzhalter. `ForceSetMusicSamplerate` ist implementiert und akzeptiert ausschlieÃƒÅ¸lich 44.100 oder 48.000 Hz. Der `/tmp/ly_force_musicrate`-Hook bleibt eine mÃƒÂ¶gliche spÃƒÂ¤tere Modifikation, aber noch kein bewiesener Klang-Fix.

Die vermeintlichen gzip-SchÃƒÂ¤den im Log wurden auf den CGI-Exportcode zurÃƒÂ¼ckgefÃƒÂ¼hrt. Der Webserver fÃƒÂ¼gt bei Byte 819 ein vier Byte langes Little-Endian-GrÃƒÂ¶ÃƒÅ¸enfeld ein. Nach dessen Entfernung bestehen CRC32 und EndlÃƒÂ¤nge vollstÃƒÂ¤ndig. Der geprÃƒÂ¼fte Klartext ist 170.868 Byte groÃƒÅ¸ und liegt zusÃƒÂ¤tzlich als `logcat.validated.txt` vor. FrÃƒÂ¼here, fehlerhafte Salvage-Ableitungen wurden zur Nachvollziehbarkeit nicht ÃƒÂ¼berschrieben.

Der valide eigene Startlog bestÃƒÂ¤tigt V821B, 64 MiB RAM, XT25P1288 mit 16 MiB Flash, Realtek RTL8723FS und alle zehn Flashpartitionen. Gleichzeitig wurde belegt, dass der CGI `/tmp/log.gz` nur einmal erzeugt und danach cached. Das Erfassungsskript prÃƒÂ¼ft jetzt strikt, schreibt PrÃƒÂ¼fmetadaten und warnt bei einem bereits bekannten Export. Bestehende Ausgabeordner werden nicht ÃƒÂ¼berschrieben.

Der Nutzer konkretisierte das Fahrzeug als Hyundai i30 Kombi von 2018 und den Ton als Ã¢â‚¬Å¾blechernÃ¢â‚¬Å“. Der Mingtu-44,1-kHz-Sonderfall prÃƒÂ¼ft exakt `Tinnos` und `MISTRA`; `HYUNDAI MOBIS` ist ein anderer Modellindex. Eine ÃƒÅ“bertragung auf den i30 wÃƒÂ¤re unbelegt. Modellkennung, Musik-/Telefonpfad und Kanalzuordnung sind die nÃƒÂ¤chsten PrÃƒÂ¼fschwerpunkte.

Sieben RegressionsprÃƒÂ¼fungen gegen externe Andes-Vektoren, reale Log-/Packdateien, beschÃƒÂ¤digte CRCs und kurze gepaddete Exporte bestehen. Die hÃƒÂ¶rbare Ursache bleibt mangels aktiver Fahrzeugsitzung unbewiesen; Backup und Recovery sind weiterhin vor jedem Flash erforderlich.

### 08:50Ã¢â‚¬â€œ09:00 CET Ã¢â‚¬â€œ Firmwarezerlegung und Version 0.3.0

Die folgenden Aussagen geben den damaligen Zwischenstand wieder. Die Log-Trailer- und API-Bewertung wurde mit 0.4.0 ausdrÃƒÂ¼cklich korrigiert.

Die zuvor nur als hochentropisch erkannte Herstellerfirmware wurde reproduzierbar entschlÃƒÂ¼sselt. Grundlage ist eine ÃƒÂ¶ffentlich dokumentierte 256-Byte-XOR-Tabelle der verwandten CPBox-/V821-Firmwarefamilie. Das eigene Werkzeug `tools/decrypt_firmware.py` prÃƒÂ¼ft zusÃƒÂ¤tzlich die vom Hersteller eingebettete MD5-Summe, bevor die SWUpdate-Nutzlast gespeichert wird.

Beide Abbilder wurden ausschlieÃƒÅ¸lich offline verarbeitet:

- stabile Firmware `26011517.5234.2`
- seriennummergebundene Cloud-Testfirmware mit ÃƒÂ¤uÃƒÅ¸erer Kennung `26122515.5234.2`

Die entschlÃƒÂ¼sselten Dateien sind SWUpdate-/CPIO-Container mit identischer `sw-description`. Sie schreiben `kernel` nach `/dev/by-name/boot` und `customer` nach `/dev/by-name/customer` und verÃƒÂ¤ndern wÃƒÂ¤hrenddessen U-Boot-Umgebungsphasen. Der `customer`-Teil ist SquashFS; das Bootabbild folgt Android Boot Image v2.

`tools/extract_squashfs.py` extrahiert das Dateisystem ohne Symlinks auf dem Host anzulegen. Jedes Abbild enthÃƒÂ¤lt 12 Verzeichnisse, 52 regulÃƒÂ¤re Dateien und einen speziellen Eintrag. Die SquashFS-Erstellungszeiten lauten:

- stabil: 2026-01-15 10:41:24 CET
- Test: 2026-05-11 10:28:52 CEST

Zwischen beiden Dateisystemen unterscheiden sich exakt 13 Dateien. Betroffen sind insbesondere `lylinkapp`, `libwcarplay_new.so`, `libiap_new.so`, `liblyctrl.so`, `btapp`, `lyLink.sh`, `system.json`, CGI und WeboberflÃƒÂ¤che. Die Testversion ergÃƒÂ¤nzt in `lyLink.sh` den Parameter `-k1` fÃƒÂ¼r Dienste und verÃƒÂ¤ndert deutlich den CarPlay-Code. Das ist ein Entwicklungszweig, aber kein Nachweis besserer AudioqualitÃƒÂ¤t.

Die Android-Boot-v2-Abbilder tragen den Namen `sun300i_riscv32`, enthalten keinen Ramdisk-Teil und liefern Linux 5.4.220 sowie einen Device Tree. Der stabile Kernel wurde am 18.12.2025, der Testkernel am 06.05.2026 gebaut.

Kernel- und Startprotokolle belegen:

- 32-Bit RISC-V mit Andes-Erweiterungen
- Allwinner-V821-Plattformpfad
- 64 MiB adressierbaren RAM
- Realtek `RTL8723FS` als Funkchip
- Flashkennung `xt25p1288`
- USB-Audiogadget `iphone_audio`

FÃƒÂ¼r die RISC-V-BinÃƒÂ¤ranalyse wurde der Andes-Befehl `ADDIGP` anhand der ÃƒÂ¶ffentlich verfÃƒÂ¼gbaren Andes-Erweiterungsimplementierung dekodiert. Dadurch konnten echte Codeverweise statt bloÃƒÅ¸er Texttreffer bestÃƒÂ¤tigt werden: `aud0`, `aud1`, `aud2` und `aud3` werden als vier getrennte Werte geparst.

Der wichtigste Audiofund liegt in `lylinkapp`: Die Software liest optional eine Ganzzahl aus `/tmp/ly_force_musicrate` und ruft anschlieÃƒÅ¸end `ForceSetMusicSamplerate()` in `libwcarplay_new.so` auf. AuÃƒÅ¸erdem sind Routinen fÃƒÂ¼r alternative Audio-Sample-Rate, Deaktivierung des HU-Audioformats und Aktualisierung der HU-Sample-Rate vorhanden. UnterstÃƒÂ¼tzte Klartextformate umfassen AAC-LC, AAC-ELD, Opus und PCM bis 48 kHz.

Das GerÃƒÂ¤tediagnoselog wurde mit dem SchlÃƒÂ¼ssel `liaoyuan.tech\0` blockweise entschlÃƒÂ¼sselt. Der Herstellerdatenstrom besitzt einen ungÃƒÂ¼ltigen gzip-Trailer: Rohdaten sind weitgehend rettbar, das Dateiende ist jedoch nicht integritÃƒÂ¤tsgesichert. Das gerettete Log bestÃƒÂ¤tigt den aktuell aktiven Modus `aud=2`. Es stammt nicht aus einer aktiven Fahrzeugsitzung und enthÃƒÂ¤lt deshalb noch keine belastbaren Musik-Sample-Raten.

`tools/capture_device_state.ps1` wurde erstellt und gegen den eingeschalteten Adapter erfolgreich geprÃƒÂ¼ft. Es liest Hoststatus und Log, entschlÃƒÂ¼sselt dieses im Salvage-Modus und erzeugt lokale SHA-256-Werte. Keine Firmware wurde hochgeladen oder geflasht.

### 08:46Ã¢â‚¬â€œ08:49 CET Ã¢â‚¬â€œ Projektverlagerung und Version 0.2.0

Der Chat wurde dem eigenstÃƒÂ¤ndigen lokalen Projekt `Autoradio - Carplay` mit dem Pfad `E:\WorkSpace\carplay` zugeordnet. Dokumentation, Analysewerkzeuge, Webbelege und Firmwareartefakte wurden aus dem fachfremden Projektordner verschoben.

Stabile Firmware, lokale WeboberflÃƒÂ¤che und seriennummergebundenes Testabbild wurden bytegenau archiviert. Die damalige Entropie- und Blockstrukturanalyse zeigte bereits eine sektorweise Transformation, konnte sie zu diesem Zeitpunkt aber noch nicht umkehren.

### 08:25Ã¢â‚¬â€œ08:42 CET Ã¢â‚¬â€œ USB, Funk, WeboberflÃƒÂ¤che und Audiomodus

Windows erkennt den Adapter als:

- `Apple Mobile Device USB Composite Device`
- USB-ID `VID_05AC/PID_12A8`
- `Apple USB Multiplexor`
- `Apple Mobile Device Ethernet`

Der Adapter stellt ein gerÃƒÂ¤tespezifisches 5-GHz-Netz `smartBox-*` bereit; individuelle Kennungen bleiben in den lokalen Originalbelegen. ZunÃƒÂ¤chst wurde 802.11n auf Kanal 36 beobachtet. Die lokale OberflÃƒÂ¤che unter `192.168.1.101` nutzt `/cgi-bin/index.cgi` mit `id=host`, `id=set`, `id=logcat`, `id=upload`, `id=sts` und `id=aa`.

Vor der Untersuchung war `aud=1` aktiv. Als erster reversibler QualitÃƒÂ¤tstest wurde `aud=2` gesetzt; die API antwortete mit `code=0`, der Adapter startete neu und meldete anschlieÃƒÅ¸end `aud=2`. ZusÃƒÂ¤tzlich belegt der eigene Export den spÃƒÂ¤teren API-Aufruf `id=set&wifi=149`; die Funkkonfiguration wurde damit ebenfalls verÃƒÂ¤ndert. Die frÃƒÂ¼here pauschale Aussage, es habe keine weiteren SchreibvorgÃƒÂ¤nge gegeben, war falsch. Es wurde keine Firmware geflasht.

Die installierte Version `26011517.5234.2` wurde mit der stabilen Hersteller-Metadatei abgeglichen. Das Testabbild wurde nur zur Offlineanalyse gesichert.

