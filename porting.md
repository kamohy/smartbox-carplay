# Portierung und Updateweg

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


0.8.2 ist ein getrennter Minimalzweig auf gepinntem 0.7.0-Image. Exakt fünf Customer-Pfade ändern sich: HTML, Updatekonfiguration, zusätzliches Wartungs-JavaScript, vorhandene Diagnose-CGI und eigener Recorder. Audio, Einstellungen und sämtliche anderen 0.7.0-Dateien bleiben bytegleich. Der Container enthält `sw-description`, `customer` und Trailer. Aus der Beschreibung wird ausschließlich der eine Kernel-Imageblock entfernt; alle Bootenv-Phasen bleiben bytegleich. Damit wird `/dev/by-name/boot` nicht als Schreibziel angefordert. Der bestehende vollständige Paketleser bleibt standardmäßig streng; Customer-only muss ausdrücklich ausgewählt werden.

Das Paket ist 3.034.669 Byte groß, SHA-256 `546416e4d2c3279142d1aa29a3e51e13780e36c0537e7459f9d3b55dc9e02cd4`. Es reduziert die übertragene Nutzlast gegenüber 0.8.0 um 3.164.672 Byte, beweist aber keine Behebung des Vorbereitungsfehlers. Geräteversuch blieb vier Minuten in Zustand 1 ohne Abschluss. Nach kontrolliertem Neustart läuft 0.7.0/Updatezustand 0. Die aktive Version weist den Löschaufruf mit HTTP 405 ab; Installation und Löschung bleiben offen. Details und Build: [maintenance.md](maintenance.md).

0.8.1 ergänzt ein rein offline arbeitendes Diagnose-Patchwerkzeug für genau das gepinnte stabile rcpservice. Es verändert 38 Byte in drei Regionen für Logargumente/-format, erhält Dateigröße, Logaufrufstellen und Audioauswahl. Die Ausgabe ist noch nicht im lylink-Paket oder einem Startoverlay integriert und wurde nicht ausgeführt. Öffentliche Firmwaredatei bleibt 0.8.0 und ist nach festhängender Vorbereitung deaktiviert; installiert ist 0.7.0.

0.8.0 ergänzt einen elften freigegebenen Imagepfad `/ota/www/js/bh-settings.js`. Die bestehende CGI erhält feste GET-Hardwareabfrage und ausschließlich `POST id=clear` zur Loglöschanforderung. Der Recorder führt diese im selben Hintergrundprozess seriell aus, löscht nur seine festen sechs gzip-/Metadaten-/Pending-Namen sowie eigene RAM-Snapshots und bewahrt Bootzähler und fremde Dateien. Keine freie Pfad-/Befehlseingabe. Die Aufzeichnung läuft weiter; unmittelbar nach dem Löschen bleiben für etwa eine Minute keine neuen gespeicherten Logs. Installation und reale Löschprüfung stehen noch aus.

0.7.1 ergänzt ausschließlich Offlineauswertung und Feldtestdokumentation. Es gibt kein neu angebotenes oder installiertes 0.7.1-Geräteimage. Der Feldtest zeigt den 8-kHz-Telefonpfad; `rcpservice` wählt 8/16 kHz anhand von HU-Fähigkeiten und Plugin-Version. Vor einem gezielten Audioexperiment müssen die konkreten Auswahlwerte erfasst werden. Ein 16-kHz-Codezweig ist kein Beweis, dass dieses Radio ihn unterstützt. Details: `field_test_2026-10-25.md`.

0.7.0 erweitert die freigegebenen Buildpfade um exakt `/app/lyLink.sh` und `/app/bh-log-recorder.sh`. Das originale Startskript erhält nur einen Hintergrundstart außerhalb des Updatemodus. Der Recorder prüft den tatsächlichen RW-Datenmount `/mnt/UDISK` und freien Platz, schreibt ausschließlich `bh-logs/` und verändert keine Partitionierung. Das ist mehr als eine Webdateiänderung; alle anderen Originaldateien und der Kernel bleiben erhalten.

Die Liveanzeige benötigt Browser-JavaScript, keinen Node-Server. CPU nutzt wegen angehaltener Idle-Jiffies `/proc/uptime` und CPU-Anzahl. Der Recorder sammelt alle fünf Sekunden Status im RAM und schreibt ungefähr jede Minute einen begrenzten gzip-Snapshot. Reale 512-KiB-Datenpartition, freier Platz, Loggerstart sowie bytegleicher Logerhalt nach Software-Neustart und echter Stromtrennung sind für 0.7.0 geprüft. Normalboot und Browser-/CORS-Update sind ebenfalls belegt.

Der erste Kandidat gilt ausschließlich für Plattform `ly5234` und die bytegenau geprüfte Herstellerbasis `26011517.5234.2`. Kein Crossflash auf andere Plattformen, keine Übernahme der widersprüchlich bezeichneten Testfirmware. Audio-Bibliotheken werden in dieser Version nicht geändert.

Die Startdatei `app/lyUpdate.sh` setzt den aktiven Webroot unter `/tmp/ota/www` aus der Systemoberfläche und dem Customer-Overlay zusammen. Sie bindet `index.html`, CGI und die Ordner `css`, `js`, `lan` ein. Das neue SVG liegt deshalb unter `css/bad-hippo-logo.svg`, die Updatekonfiguration unter `js/bh-update-config.json`.

Das Logo wird lokal mitgeliefert; im Fahrzeug ist kein Abruf von fdn.bad-hippo.com nötig. Originalquelle: https://fdn.bad-hippo.com/assets/logo.svg. SVG-SHA-256: `410ba4061bf6e9b8cee1ccda855285dd888ce8fd4e420a9bfdd143248aab7fe2`.

Herstellerquelle: https://cpbox-abroad.oss-us-west-1.aliyuncs.com/5234/version.json. Die dort angebotene stabile Datei ist https://cpbox-abroad.oss-us-west-1.aliyuncs.com/5234/update.img. DNS am 25.10.2026: `47.254.114.108`; diese IP ist kein dauerhaft stabiler Vertrag.

Die Herstelleroberfläche lädt Manifest und Image **im Browser**. Danach sendet `upload_fw()` die Datei als multipart/FormData an `POST /cgi-bin/index.cgi?id=upload` des Adapters. Deshalb ist kein transparenter HTTPS-/DNS-Eingriff erforderlich, um eine andere Datei zuzuführen. Der Transferweg allein sagt nichts über weitere Prüfungen im Gerät aus.

Eigene permanente Manifestadresse: https://raw.githubusercontent.com/kamohy/smartbox-carplay/main/ota/5234/version.json. Die Firmware enthält dazu Plattform, Herstellerbasis und eigene UI-Version getrennt. Der Browser prüft Projektversion numerisch, Plattform/Basis, Freigabestatus, Downloadpfad, Länge und SHA-256. Diese SHA-256 ist eine Transport-/Integritätsprüfung, keine unabhängige Signatur gegen ein kompromittiertes Repository.

Das Flashformat bleibt Hersteller-XOR, davor MD5 über die SWUpdate-Nutzlast, darin CRC-CPIO und SquashFS 4.0/XZ mit 256-KiB-Blöcken. Der Kernel und die originale `sw-description` sind byteidentisch übernommen. Dadurch würde der ursprüngliche Updateablauf weiterhin auch die Bootpartition beschreiben; ein UI-Update ist nicht automatisch ein risikoloser Dateiupload.

Backhand 0.25.5 dient als Dateisystemschreiber; Dissect SquashFS 1.12 liest das Ergebnis unabhängig. Dateiinhalte, Modus, Eigentümer, Zeitstempel und Gerätedatei werden abgeglichen. Der komplette Quellcontainer lässt sich vor Änderungen byteidentisch wiederherstellen. Zwei Kandidatenbuilds ergaben dasselbe SHA-256.

`.gitattributes` schaltet Zeilenendennormalisierung für die eingebetteten Webdateien aus. Dadurch stimmen Repositorybytes, lokale Overlaydateien und das gebaute Image auch bei einem Windows-Checkout überein.

Noch offen: vollständiger individueller 16-MiB-Dump, Wiederherstellung über einen verifizierten Hardware-/Recoveryweg und vollständige Analyse der Geräte-Updater-Prüfungen. Die vorhandenen öffentlichen Herstellerdateien enthalten keine vollständige Sicherung von U-Boot, Rootfs, Recovery, Environment oder privaten Gerätedaten.

Aktualisierung 0.5.1: Nach ausdrücklicher Nutzerfreigabe trotz möglichen Geräteverlusts wurde das geprüfte 0.5.0-Paket erfolgreich geflasht. Auf Updaterzustand 3 folgte der normale Neustart mit `id=set&conn=cp`; die sechs Webdateien stimmen anschließend direkt auf dem Gerät mit dem Build überein. Damit ist der Erststart auf genau diesem Adapter belegt. Vollbackup, Restore und Fahrzeug-/Audiotest bleiben offen. Der Windows-xfel-Probeversuch war negativ; kein FEL-Modus vorhanden. CatPlay-`cpbox2fel` ist selbst ein vorgeschalteter Flash und enthält im geprüften Stand keinen ly5234-Preset.

Quellen: [xfel V821-Code](https://github.com/xboot/xfel/blob/445e8aefe6914c85817cc9bd1d201629364b0ec6/chips/v821.c), [CatPlay cpbox2fel](https://github.com/catplay-labs/catplay-firmware/blob/aca307bb24efc7b1bcf624625e609a6666970761/meta-sunxi/recipes-kernel/sunxi-flasher/files/cpbox2fel.py). Windowsarchiv-SHA-256: `f00c3ab96149ee63abe3e5f015a1f69aae9fdadf35e999cf110d1d5a36923fbc`.

0.6.0 ergänzt `/ota/www/cgi-bin/bh-diagnostics.cgi` mit Modus 0755 und ein neues Frontendmodul. Der vorhandene Startpfad kopiert neue CGI-Dateien in den aktiven Webroot. Die CGI-Datei wird dort ausgeführt und kann deshalb bei einer HTTP-Prüfung nicht wie eine statische Datei bytegehasht werden; dafür sind Offline-Payload-/Modusprüfung und echte funktionale Endpointtests erforderlich. Die übrigen sieben UI-Dateien bleiben per HTTP/SHA-256 prüfbar.
