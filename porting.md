# Portierung und Updateweg

Version: 0.8.2 (Wartungszwischenstand; GerÃƒÂ¤te-UI zuletzt 0.7.0)
Stand: 2026-10-25 12:53 CET

0.8.2 ist ein getrennter Minimalzweig auf gepinntem 0.7.0-Image. Exakt fÃƒÂ¼nf Customer-Pfade ÃƒÂ¤ndern sich: HTML, Updatekonfiguration, zusÃƒÂ¤tzliches Wartungs-JavaScript, vorhandene Diagnose-CGI und eigener Recorder. Audio, Einstellungen und sÃƒÂ¤mtliche anderen 0.7.0-Dateien bleiben bytegleich. Der Container enthÃƒÂ¤lt `sw-description`, `customer` und Trailer. Aus der Beschreibung wird ausschlieÃƒÅ¸lich der eine Kernel-Imageblock entfernt; alle Bootenv-Phasen bleiben bytegleich. Damit wird `/dev/by-name/boot` nicht als Schreibziel angefordert. Der bestehende vollstÃƒÂ¤ndige Paketleser bleibt standardmÃƒÂ¤ÃƒÅ¸ig streng; Customer-only muss ausdrÃƒÂ¼cklich ausgewÃƒÂ¤hlt werden.

Das Paket ist 3.034.669 Byte groÃƒÅ¸, SHA-256 `546416e4d2c3279142d1aa29a3e51e13780e36c0537e7459f9d3b55dc9e02cd4`. Es reduziert die ÃƒÂ¼bertragene Nutzlast gegenÃƒÂ¼ber 0.8.0 um 3.164.672 Byte, beweist aber keine Behebung des Vorbereitungsfehlers. GerÃƒÂ¤teprÃƒÂ¼fung lÃƒÂ¤uft; keine Annahme einer bereits erfolgreichen Installation oder LoglÃƒÂ¶schung. Details und Build: [maintenance.md](maintenance.md).

0.8.1 ergÃƒÂ¤nzt ein rein offline arbeitendes Diagnose-Patchwerkzeug fÃƒÂ¼r genau das gepinnte stabile rcpservice. Es verÃƒÂ¤ndert 38 Byte in drei Regionen fÃƒÂ¼r Logargumente/-format, erhÃƒÂ¤lt DateigrÃƒÂ¶ÃƒÅ¸e, Logaufrufstellen und Audioauswahl. Die Ausgabe ist noch nicht im lylink-Paket oder einem Startoverlay integriert und wurde nicht ausgefÃƒÂ¼hrt. Ãƒâ€“ffentliche Firmwaredatei bleibt 0.8.0 und ist nach festhÃƒÂ¤ngender Vorbereitung deaktiviert; installiert ist 0.7.0.

0.8.0 ergÃƒÂ¤nzt einen elften freigegebenen Imagepfad `/ota/www/js/bh-settings.js`. Die bestehende CGI erhÃƒÂ¤lt feste GET-Hardwareabfrage und ausschlieÃƒÅ¸lich `POST id=clear` zur LoglÃƒÂ¶schanforderung. Der Recorder fÃƒÂ¼hrt diese im selben Hintergrundprozess seriell aus, lÃƒÂ¶scht nur seine festen sechs gzip-/Metadaten-/Pending-Namen sowie eigene RAM-Snapshots und bewahrt BootzÃƒÂ¤hler und fremde Dateien. Keine freie Pfad-/Befehlseingabe. Die Aufzeichnung lÃƒÂ¤uft weiter; unmittelbar nach dem LÃƒÂ¶schen bleiben fÃƒÂ¼r etwa eine Minute keine neuen gespeicherten Logs. Installation und reale LÃƒÂ¶schprÃƒÂ¼fung stehen noch aus.

0.7.1 ergÃƒÂ¤nzt ausschlieÃƒÅ¸lich Offlineauswertung und Feldtestdokumentation. Es gibt kein neu angebotenes oder installiertes 0.7.1-GerÃƒÂ¤teimage. Der Feldtest zeigt den 8-kHz-Telefonpfad; `rcpservice` wÃƒÂ¤hlt 8/16 kHz anhand von HU-FÃƒÂ¤higkeiten und Plugin-Version. Vor einem gezielten Audioexperiment mÃƒÂ¼ssen die konkreten Auswahlwerte erfasst werden. Ein 16-kHz-Codezweig ist kein Beweis, dass dieses Radio ihn unterstÃƒÂ¼tzt. Details: `field_test_2026-10-25.md`.

0.7.0 erweitert die freigegebenen Buildpfade um exakt `/app/lyLink.sh` und `/app/bh-log-recorder.sh`. Das originale Startskript erhÃƒÂ¤lt nur einen Hintergrundstart auÃƒÅ¸erhalb des Updatemodus. Der Recorder prÃƒÂ¼ft den tatsÃƒÂ¤chlichen RW-Datenmount `/mnt/UDISK` und freien Platz, schreibt ausschlieÃƒÅ¸lich `bh-logs/` und verÃƒÂ¤ndert keine Partitionierung. Das ist mehr als eine WebdateiÃƒÂ¤nderung; alle anderen Originaldateien und der Kernel bleiben erhalten.

Die Liveanzeige benÃƒÂ¶tigt Browser-JavaScript, keinen Node-Server. CPU nutzt wegen angehaltener Idle-Jiffies `/proc/uptime` und CPU-Anzahl. Der Recorder sammelt alle fÃƒÂ¼nf Sekunden Status im RAM und schreibt ungefÃƒÂ¤hr jede Minute einen begrenzten gzip-Snapshot. Reale 512-KiB-Datenpartition, freier Platz, Loggerstart sowie bytegleicher Logerhalt nach Software-Neustart und echter Stromtrennung sind fÃƒÂ¼r 0.7.0 geprÃƒÂ¼ft. Normalboot und Browser-/CORS-Update sind ebenfalls belegt.

Der erste Kandidat gilt ausschlieÃƒÅ¸lich fÃƒÂ¼r Plattform `ly5234` und die bytegenau geprÃƒÂ¼fte Herstellerbasis `26011517.5234.2`. Kein Crossflash auf andere Plattformen, keine ÃƒÅ“bernahme der widersprÃƒÂ¼chlich bezeichneten Testfirmware. Audio-Bibliotheken werden in dieser Version nicht geÃƒÂ¤ndert.

Die Startdatei `app/lyUpdate.sh` setzt den aktiven Webroot unter `/tmp/ota/www` aus der SystemoberflÃƒÂ¤che und dem Customer-Overlay zusammen. Sie bindet `index.html`, CGI und die Ordner `css`, `js`, `lan` ein. Das neue SVG liegt deshalb unter `css/bad-hippo-logo.svg`, die Updatekonfiguration unter `js/bh-update-config.json`.

Das Logo wird lokal mitgeliefert; im Fahrzeug ist kein Abruf von fdn.bad-hippo.com nÃƒÂ¶tig. Originalquelle: https://fdn.bad-hippo.com/assets/logo.svg. SVG-SHA-256: `410ba4061bf6e9b8cee1ccda855285dd888ce8fd4e420a9bfdd143248aab7fe2`.

Herstellerquelle: https://cpbox-abroad.oss-us-west-1.aliyuncs.com/5234/version.json. Die dort angebotene stabile Datei ist https://cpbox-abroad.oss-us-west-1.aliyuncs.com/5234/update.img. DNS am 25.10.2026: `47.254.114.108`; diese IP ist kein dauerhaft stabiler Vertrag.

Die HerstelleroberflÃƒÂ¤che lÃƒÂ¤dt Manifest und Image **im Browser**. Danach sendet `upload_fw()` die Datei als multipart/FormData an `POST /cgi-bin/index.cgi?id=upload` des Adapters. Deshalb ist kein transparenter HTTPS-/DNS-Eingriff erforderlich, um eine andere Datei zuzufÃƒÂ¼hren. Der Transferweg allein sagt nichts ÃƒÂ¼ber weitere PrÃƒÂ¼fungen im GerÃƒÂ¤t aus.

Eigene permanente Manifestadresse: https://raw.githubusercontent.com/kamohy/smartbox-carplay/main/ota/5234/version.json. Die Firmware enthÃƒÂ¤lt dazu Plattform, Herstellerbasis und eigene UI-Version getrennt. Der Browser prÃƒÂ¼ft Projektversion numerisch, Plattform/Basis, Freigabestatus, Downloadpfad, LÃƒÂ¤nge und SHA-256. Diese SHA-256 ist eine Transport-/IntegritÃƒÂ¤tsprÃƒÂ¼fung, keine unabhÃƒÂ¤ngige Signatur gegen ein kompromittiertes Repository.

Das Flashformat bleibt Hersteller-XOR, davor MD5 ÃƒÂ¼ber die SWUpdate-Nutzlast, darin CRC-CPIO und SquashFS 4.0/XZ mit 256-KiB-BlÃƒÂ¶cken. Der Kernel und die originale `sw-description` sind byteidentisch ÃƒÂ¼bernommen. Dadurch wÃƒÂ¼rde der ursprÃƒÂ¼ngliche Updateablauf weiterhin auch die Bootpartition beschreiben; ein UI-Update ist nicht automatisch ein risikoloser Dateiupload.

Backhand 0.25.5 dient als Dateisystemschreiber; Dissect SquashFS 1.12 liest das Ergebnis unabhÃƒÂ¤ngig. Dateiinhalte, Modus, EigentÃƒÂ¼mer, Zeitstempel und GerÃƒÂ¤tedatei werden abgeglichen. Der komplette Quellcontainer lÃƒÂ¤sst sich vor Ãƒâ€žnderungen byteidentisch wiederherstellen. Zwei Kandidatenbuilds ergaben dasselbe SHA-256.

`.gitattributes` schaltet Zeilenendennormalisierung fÃƒÂ¼r die eingebetteten Webdateien aus. Dadurch stimmen Repositorybytes, lokale Overlaydateien und das gebaute Image auch bei einem Windows-Checkout ÃƒÂ¼berein.

Noch offen: vollstÃƒÂ¤ndiger individueller 16-MiB-Dump, Wiederherstellung ÃƒÂ¼ber einen verifizierten Hardware-/Recoveryweg und vollstÃƒÂ¤ndige Analyse der GerÃƒÂ¤te-Updater-PrÃƒÂ¼fungen. Die vorhandenen ÃƒÂ¶ffentlichen Herstellerdateien enthalten keine vollstÃƒÂ¤ndige Sicherung von U-Boot, Rootfs, Recovery, Environment oder privaten GerÃƒÂ¤tedaten.

Aktualisierung 0.5.1: Nach ausdrÃƒÂ¼cklicher Nutzerfreigabe trotz mÃƒÂ¶glichen GerÃƒÂ¤teverlusts wurde das geprÃƒÂ¼fte 0.5.0-Paket erfolgreich geflasht. Auf Updaterzustand 3 folgte der normale Neustart mit `id=set&conn=cp`; die sechs Webdateien stimmen anschlieÃƒÅ¸end direkt auf dem GerÃƒÂ¤t mit dem Build ÃƒÂ¼berein. Damit ist der Erststart auf genau diesem Adapter belegt. Vollbackup, Restore und Fahrzeug-/Audiotest bleiben offen. Der Windows-xfel-Probeversuch war negativ; kein FEL-Modus vorhanden. CatPlay-`cpbox2fel` ist selbst ein vorgeschalteter Flash und enthÃƒÂ¤lt im geprÃƒÂ¼ften Stand keinen ly5234-Preset.

Quellen: [xfel V821-Code](https://github.com/xboot/xfel/blob/445e8aefe6914c85817cc9bd1d201629364b0ec6/chips/v821.c), [CatPlay cpbox2fel](https://github.com/catplay-labs/catplay-firmware/blob/aca307bb24efc7b1bcf624625e609a6666970761/meta-sunxi/recipes-kernel/sunxi-flasher/files/cpbox2fel.py). Windowsarchiv-SHA-256: `f00c3ab96149ee63abe3e5f015a1f69aae9fdadf35e999cf110d1d5a36923fbc`.

0.6.0 ergÃƒÂ¤nzt `/ota/www/cgi-bin/bh-diagnostics.cgi` mit Modus 0755 und ein neues Frontendmodul. Der vorhandene Startpfad kopiert neue CGI-Dateien in den aktiven Webroot. Die CGI-Datei wird dort ausgefÃƒÂ¼hrt und kann deshalb bei einer HTTP-PrÃƒÂ¼fung nicht wie eine statische Datei bytegehasht werden; dafÃƒÂ¼r sind Offline-Payload-/ModusprÃƒÂ¼fung und echte funktionale Endpointtests erforderlich. Die ÃƒÂ¼brigen sieben UI-Dateien bleiben per HTTP/SHA-256 prÃƒÂ¼fbar.
