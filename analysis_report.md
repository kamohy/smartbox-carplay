# Technischer Analysebericht – SmartBox 5234

Version: 0.7.1  
Stand: 2026-10-25 11:41 CET

## Neuer Laufzeitbefund

Der erste Fahrzeugtest ist jetzt vorhanden. Nutzer bestätigt Teams in Mode 2 und Mode 3. Beide Logs zeigen 16-kHz-Telefonanforderung des iPhones, 8-kHz-Telefonstart am USB-Dienst, Taktrückmeldung um 8 kHz und Mikrofonumwandlung 8 → 16 kHz. Das ist ein konkreter Formatengpass, der zum weiterhin gedämpften Klang passt. Die subjektive Verbesserung durch den Moduswechsel ändert diese Rate nicht. Ausführliche Belege und Grenzen: [Feldtest](field_test_2026-10-25.md).

Noch nicht bewiesen sind vollständige hörbare Kausalität, Telefonformat beim direkten Kabelvergleich und eine feste Hardwaregrenze. `rcpservice` enthält eine von gemeldeten HU-Fähigkeiten und Plugin-Version abhängige Wahl von 8/16 kHz. Die konkreten Eingangswerte dieser Wahl fehlen im aufbewahrten Ausschnitt; sie sind der nächste Prüfpunkt. Die folgenden älteren Aussagen „kein Fahrzeuglog“ beschreiben den historischen Stand vor diesem Feldtest.

## Kurzurteil

Konkrete Eingriffspunkte in der Firmware sind belegt; eine hörbare Verbesserung ist noch nicht nachgewiesen. Das Fahrzeug ist ein Hyundai i30 Kombi von 2018. Der Nutzer bestätigt Teams-Anrufe mit blechernem Ton in beiden Richtungen und deutlich besseren Teams-Klang per direktem USB-Kabel am selben iPhone. Ein Fehler bei Musik ist bislang nicht bestätigt.

Der Adapter und seine zusätzliche Telefon-Audiostrecke sind damit ein starker Verdacht. Die Fehlerursache ist noch nicht gemessen: Telefon-Ein-/Ausgabeformate, die Umwandlung zwischen Radio und iPhone sowie Sprachverarbeitung kommen infrage. Ein Telefonpfad, Mono oder 16 kHz sind bei einem Telefonat grundsätzlich erwartbar und allein kein Fehlernachweis. Der Musik-Hook für 44,1/48 kHz hat für diesen Teams-Befund keine Priorität.

Backup und Recovery fehlen, und die verfügbare Testfirmware ist intern widersprüchlich versioniert. Der nächste Schritt ist daher ein Log des tatsächlich betroffenen Teams-Anrufs, danach ein anhand dieses Logs ausgewählter Konfigurationstest.

## Eingrenzung auf Teams und Telefonie

UI-Firmware 0.5.0 mit Logo, dunklem Design und eigenem GitHub-Updatekanal wurde nach ausdrücklicher Freigabe des Geräteverlustrisikos installiert. Normalstart und sechs UI-Dateien sind direkt auf dem Gerät geprüft. Audiobibliotheken wurden nicht verändert; der Teams-Befund bleibt offen. Einzelheiten: `firmware_installation.md`, `porting.md` und `ota/5234/build-report.json`.

`lylinkapp::AudioPlayerCreate` behandelt Telefon-Audiotyp 8 getrennt. Ab `0x1D50C` liest die Software die Telefonrate und Kanalzahl des Radios aus und übergibt sie mit 16 Bit an den USB-Dienst. Die Logmeldung `phone call rate=%d, sz=%d` zeigt dabei Rate und fest vorgegebene Bittiefe; `sz` ist hier keine Pufferlänge.

Ein zweiter konkreter Befund liegt im Mikrofon-/HID-Pfad ab `0x164FC`: Wenn die Radio-Mikrofonrate von 16.000 Hz abweicht, erzeugt die Firmware zwei FFmpeg-SWResample-Konverter zwischen Radioformat und intern 16.000 Hz / 16 Bit / Mono. Für Siri existieren analoge Konverter mit 24.000 Hz. Das ist ein nachgewiesener zusätzlicher Verarbeitungsschritt. Ob er im betroffenen Teams-Anruf aktiv ist und die Verschlechterung erklärt, bleibt ohne dessen Log offen.

Die Hersteller-Testversion trägt den Hinweis `phone voice issue!`. Das passt zum Fehlerbereich, ist aber keine bestätigte Freigabe oder Fehlerbehebung für dieses Gerät. Auch in ihrem `AudioPlayerCreate` bleibt der eigene Telefonzweig vorhanden.

Als allgemeiner Architekturkontext: Microsoft unterstützt [Teams-Audioanrufe über CarPlay](https://support.microsoft.com/en-us/teams/calls-devices/place-microsoft-teams-calls-with-apple-carplay). Apple beschreibt für [Voice-Chat-Audiositzungen](https://developer.apple.com/documentation/avfaudio/avaudiosession/mode-swift.struct/voicechat) gesonderte Sprach-Routen und Sprachverarbeitung. Diese Dokumente belegen nicht, welche konkrete Route die installierte Teams-Version auf diesem iPhone gewählt hat.

## Bestätigte Geräteidentität

- Verkaufsname: SYACHI 2-in-1 Wireless CarPlay & Android Auto Adapter
- Amazon-ASIN: `B0G8YQZWH1`
- WLAN: gerätespezifisches `smartBox-*`-Netz; individuelle Kennung bleibt lokal
- Firmware: `26011517.5234.2`
- Projekt-/Plattformkennung: `ly5234`
- SoC direkt im CRC-geprüften eigenen Gerätelog: Allwinner V821B, 32-Bit RISC-V
- Kernel: Linux `5.4.220`
- RAM laut Kerneladressraum: 64 MiB
- Bluetooth-Profil im Startlog: `RTL8723FS`; im eigenen Kernel vorhandener WLAN-Treiber: `RTL8733BS`. Kein physischer Chipnachweis.
- Flash: `xt25p1288`, 16 MiB SPI-NOR
- USB-Emulation: Apple `VID_05AC/PID_12A8`
- Webverwaltung: `http://192.168.1.101`, nur TCP-Port 80 beobachtet

## Der tatsächliche Audioweg

Der Adapter ist ein aktiver CarPlay-Proxy:

1. Das iPhone entdeckt und initialisiert Wireless CarPlay.
2. Audio, Video und Steuerdaten laufen anschließend über das 5-GHz-WLAN des Adapters.
3. Die Firmware verarbeitet die CarPlay-Audioformate und deren Abtastraten.
4. Der Kernel stellt über `iphone_audio` beziehungsweise den sichtbaren `HOLTEK B-LINK USB Audio`-Pfad das Audio zum Radio bereit.

Eine zusätzliche direkte Bluetooth-Verbindung zwischen iPhone und Hyundai soll beim Test getrennt werden, um das Routing eindeutig zu halten. Bluetooth am iPhone und die SmartBox-Kopplung bleiben dabei aktiv.

## Bedeutung der vier Audio-Modi

Die Werte `aud=0..3` werden im RISC-V-Code als vier Indizes gelesen. Die folgenden Strategiebeschreibungen stammen aus der allgemeinen Herstellerdokumentation; ihre vollständige Umsetzung in genau dieser 5234-Version ist noch nicht bestätigt:

| Wert | Oberfläche | Allgemeine Herstellerbeschreibung |
|---:|---|---|
| 0 | Default | festes Hersteller-Standardprofil |
| 1 | Mode 1 | alternatives festes Kompatibilitätsprofil |
| 2 | Mode 2 | adaptive Einstellungen anhand gemeldeter Head-Unit-Parameter |
| 3 | Mode 3 | möglichst unveränderte beziehungsweise durchgereichte Audioausgabeeinstellungen |

Vor der Untersuchung war `aud=1` aktiv. Seit 2026-10-25 08:39 CET ist `aud=2` gespeichert. Für den bestätigten Teams-Fehler wird zunächst dieser Istzustand protokolliert; ein Wechsel auf Mode 3 ist anhand des bisher nachvollzogenen Telefoncodes noch nicht begründet.

Der zusätzlich ausgepackte USB-Dienst `rcpservice` zeigt einen konkreten Verbraucher: Ein Telefon-Pufferpfad unterscheidet `aud=0` von jedem Wert ungleich null. In genau diesem Pfad wirken 1, 2 und 3 gleich. Das beweist weder identische Wirkung im gesamten System noch drei unterschiedliche Musik-Klangprofile. Eine Empfehlung ausschließlich nach den Modusnamen ist deshalb zu schwach.

## Konkreter Firmware-Eingriffspunkt

`lylinkapp` prüft beim Start auf:

```text
/tmp/ly_force_musicrate
```

Wird dort eine Ganzzahl gelesen, protokolliert die Firmware `force music rate = %d` und ruft `ForceSetMusicSamplerate()` aus `libwcarplay_new.so` auf. Die tatsächliche Implementierung akzeptiert ausschließlich 44.100 und 48.000 Hz und speichert den Wert in einer internen globalen Variablen. Weitere sichtbare Routinen sind:

- `ForceSetAltAudioSamplerate`
- `DisableHUAudioFormat` – in dieser stabilen Bibliothek ausdrücklich nicht implementiert
- `UpdateHUSamplerate` – in dieser stabilen Bibliothek ausdrücklich nicht implementiert
- `COMMAD_HU_SAMPLERATE`

Die Binärdateien enthalten unter anderem folgende unterstützte Formate:

- AAC-LC: 44,1 und 48 kHz, Stereo
- AAC-ELD: 16, 24, 32, 44,1 und 48 kHz in mehreren Varianten
- Opus: 16, 24 und 48 kHz, Mono
- PCM: 16/24 Bit, Mono/Stereo, 16 bis 48 kHz

Die Platzhalter melden selbst `not implement api,should not be called`. Eine erzwungene CarPlay-Musikrate von 44.100 oder 48.000 Hz ist dagegen ein echter Ansatzpunkt. Sie garantiert noch keine identische USB-Ausgaberate. Erst das aktive Fahrzeuglog muss beide Seiten zeigen.

## Hyundai-spezifischer Befund

`rcpservice` liest den vom Radio gemeldeten Hersteller und das Modell. Der 44,1-kHz-Sonderfall mit der Logmeldung `mingtu force media sr=44100` ist exakt an Hersteller `Tinnos` und Modell `MISTRA` gebunden. Die separate Kennung `HYUNDAI MOBIS` wird als anderer Modellindex behandelt. Aus dem Fahrzeugnamen i30 folgt daher nicht, dass der Mingtu-Patch passend wäre.

Für die nächste Auswertung sind `huInfo name=...,manufacturer=[...],model=[...]`, `media main audio rate`, `media phone audio rate` und `AudioPlayerCreate` die entscheidenden Logstellen. Ohne diese Angaben bleibt die Auswahl des tatsächlichen i30-Codepfads offen.

## Firmwarestruktur

Das Herstellerabbild verwendet eine veröffentlichte 256-Byte-XOR-Transformation. Nach deren reproduzierbarer Umkehr und der eingebetteten MD5-Prüfung ergibt sich:

- äußerer Container mit MD5 und SWUpdate-Nutzlast,
- SWUpdate/CPIO mit `sw-description`, `customer` und `kernel`,
- `customer` als SquashFS-Dateisystem,
- `kernel` als Android-Boot-v2-Abbild mit gzip-Kernel und Device Tree.

Innerhalb von `customer/app/lylink` steckt zusätzlich ein modifiziertes ZIP-Paket. Die ersten 128 Byte sind mit `ya-iepc` XOR-maskiert; das zentrale Verzeichnis und der Trailer sind ebenfalls verändert. Die lokalen ZIP-Header und die CRC32-Werte erlauben eine vollständig geprüfte Extraktion von `libriap2.so`, `librcarplay.so`, `libx264.so.159`, `liblyx264.so`, `rcpservice` und `liblylinkpcm.so`.

Das Hersteller-Update enthält nur Boot und Customer. U-Boot, Recovery, Rootfs, private Gerätedaten und weitere Partitionen sind damit noch nicht gesichert.

## Korrigierter Logexport und Cache

Der CGI-Webserver fügt bei Offset `0x333` vier Byte mit der ursprünglichen gzip-Länge ein und XOR-maskiert danach die Ausgabe. Nach korrekter Entfernung besteht das eigene Log die vollständige gzip-CRC- und Längenprüfung: 25.421 Byte gzip ergeben 170.868 Byte Klartext. SHA-256 des validierten Klartexts: `87AC31A4CA8DFE27CDA8BEFCB506D939C0CF281AFE236EA4169AA4B141B2B730`.

Die frühere Aussage eines defekten Hersteller-Trailers war ein Analysefehler. Alte Salvage-Klartexte bleiben als historische Ableitungen erhalten; maßgeblich ist `evidence/logs/2026-10-25-0851/logcat.validated.txt`.

Der CGI erzeugt `/tmp/log.gz` nur, wenn die Datei fehlt. Deshalb liefern wiederholte Abrufe denselben alten Stand. Für jeden Fahrzeugversuch muss der Adapter vor der Wiedergabe neu starten; erst nach dem Auftreten des Fehlers wird der erste Export abgerufen. Das vorhandene PC-Log enthält keine aktive CarPlay-Audiowiedergabe.

Die stabile Firmware wurde mit folgenden zentralen Hashes verifiziert:

- Original `update.img`: `7AFFF8E6A6387662AA10D84D5F8745E8406B91FB704AA4942F6E416393B10F63`
- entschlüsselte SWUpdate-Nutzlast: `396D3533697A39BC65D097B8087050E7A3191AB08021B32515BA15910A090DFD`
- SquashFS `customer`: `A8C0BDCFE019F9B5CD9F6432243FC5A23D9CF9B75CEFB136B5C6FFAB06CF9362`
- Bootabbild `kernel`: `63F4B217E98B75B39580CFAA566C10E24920C9384A27BCB63ED8A48A0A381B27`

Alle zentralen Artefakte stehen in `evidence/SHA256SUMS.txt`.

## Vergleich mit der Cloud-Testfirmware

Zwischen stabiler und Testfirmware unterscheiden sich exakt 13 Dateien, darunter:

- `app/lylinkapp`
- `app/libwcarplay_new.so`
- `app/libiap_new.so`
- `app/liblyctrl.so`
- `app/btapp`
- `app/lyLink.sh`
- `app/system.json`
- Weboberfläche und CGI

Die Testversion ändert also gerade den CarPlay-/Audio- und Verbindungsbereich. Sie ist dennoch kein sicherer Qualitäts-Fix:

- Cloud-Manifest: `26122515.5234.2`
- internes `system.json`: `26051115.5234.2`
- Herstellerhinweis: `phone voice issue!`
- Verteilung ist seriennummergebunden

Auch im eingebetteten Paket ändern sich `libriap2.so`, `librcarplay.so` und `rcpservice`; die PCM-Bibliothek und beide x264-Bibliotheken bleiben byteidentisch. Geänderter Code beweist weiterhin keine bessere Klangqualität. Das Testabbild bleibt reine Vergleichsbasis und wird nicht installiert.

## Empfohlene Optimierungsreihenfolge

1. Adapter im Fahrzeug neu starten und den blechern klingenden Teams-Anruf mit Mode 2 reproduzieren. Nur eine zusätzliche direkte iPhone-Hyundai-Bluetooth-Verbindung trennen. Erst nach dem Anruf erstmals das Log sichern.
2. Einen normalen Telefonanruf als Gegenprobe durchführen: Ist auch dieser betroffen oder nur Teams? Musik separat als Kontrollfall prüfen.
3. Hersteller-/Modellerkennung, Telefonrate und Kanalzahl auf beiden Seiten, Mikrofon-Resampling und Paket-/Pufferfehler auswerten.
4. Erst danach einen gezielten Konfigurations-/Telefonpfad-Patch entwerfen. Im bekannten Telefonpuffer ist Default vs. ungleich null relevant; 1/2/3 sind dort gleich. Den Musik-Hook nur bei zusätzlich bestätigtem Musikfehler verfolgen.
5. Repacker, komplettes Flashbackup und Hardware-Recovery offline verifizieren.
6. Modifizierte Firmware zunächst nur auf einem zweiten Adapter testen.

## Aktuelle Grenze

Die Firmware ist analysierbar und der Audiohebel ist gefunden. Noch nicht bewiesen ist, welche konkrete Sample-Rate- oder Formatentscheidung die schlechte Qualität im Fahrzeug verursacht. Ohne dieses Laufzeitergebnis wäre jede feste 44,1-/48-kHz-Vorgabe ein Blindflug.

