# Zusätzliche Audiobelege aus Firmware 26011517.5234.2

Version: 0.4.1  
Stand: 2026-10-25 09:19 CET

Die Adressen sind ELF-Virtualadressen der archivierten stabilen Dateien, keine beobachteten Prozessadressen auf dem Gerät. Statische Codebelege sind getrennt von einem noch fehlenden Audiotest im Fahrzeug zu bewerten.

## Weitere Verpackungsschicht

`customer-root/app/lylink` enthält sechs ELF-Dateien in einem modifizierten ZIP. Die ersten 128 Byte lassen sich mit dem wiederholten Schlüssel `ya-iepc` zurückwandeln. Die lokalen Header liefern komprimierte Länge, Originallänge und CRC32; alle sechs Einträge bestehen die Prüfung in stabiler und Testversion. Das zentrale Verzeichnis/ZIP-Ende ist verändert und wird nicht ungeprüft als Standard-ZIP behandelt.

Die extrahierten Dateien liegen jeweils in `decrypted/lylink-unpacked`. `tools/extract_lypack.py` schreibt ein Manifest mit Dateihashes. Das Programm hat keine Netz- oder Gerätefunktion und lehnt bestehende Ausgabeordner ab.

## Tatsächliche Musikrate

Nach Nutzerpräzisierung betrifft der bestätigte Fehler Teams-Telefonate, beide Richtungen, bei besserem Teams-Kabelvergleich am selben iPhone. Der folgende Musik-Hook ist deshalb derzeit kein passender Fix für den bestätigten Fehler.

Datei: `customer-root/app/libwcarplay_new.so`.

- Export `ForceSetMusicSamplerate`: `0x23AB0`.
- Aufgerufene Implementierung: `0x1755C`.
- Vergleichskonstanten: `0xB000 - 0x3BC = 44100`, `0xC000 - 0x480 = 48000`.
- Nur bei diesen beiden Werten führt der Pfad ab `0x175D0` den Speicherzugriff zur globalen Musikrate aus.
- Andere Werte führen zur Meldung, dass die Rate nicht unterstützt wird; Rückgabewert null allein belegt keinen erfolgreich gesetzten Wert.

Datei: `customer-root/app/lylinkapp`.

- Optionaler Dateipfad `/tmp/ly_force_musicrate` wird in der Funktion ab `0x2264C` gelesen.
- Startpfad ruft diese Funktion bei `0x1C814` auf und übergibt das Ergebnis ab `0x1C834` an `ForceSetMusicSamplerate@plt`.

Dieser Eingriff liegt auf der drahtlosen CarPlay-Seite. Er ist keine bereits nachgewiesene Änderung der vom Radio empfangenen USB-Rate.

## Telefon- und Mikrofon-Umwandlung

Datei: `customer-root/app/lylinkapp`.

- `AudioPlayerCreate` beginnt bei `0x1D314`. Seine ursprünglichen Parameter umfassen Sample-Rate, Bittiefe, Kanalzahl, Audiotyp und `hasInput`.
- Bei aktivem Eingang wird Audiotyp 8 bei `0x1D4AC` zum Telefonzweig `0x1D50C` geleitet.
- Dieser Zweig lädt die Radio-Telefonrate aus Objektoffset `0x64` und die Kanalzahl aus `0x68`.
- Die Logmeldung bei `0x1D52C` lautet `phone call rate=%d, sz=%d`; der zweite Wert wird dabei ausdrücklich als 16 gesetzt. Er bezeichnet hier Bittiefe, keine Pufferlänge.
- Danach werden Rate, Kanalzahl, 16 Bit und Eingangsflag an den Startbefehl für den USB-Dienst übergeben.
- Siri (Audiotyp 16) nutzt die benachbarten Radiofelder `0x5C/0x60` und einen eigenen Zweig.

Der Mikrofon-/HID-Konverteraufbau liegt ab `0x164FC`:

- Ab `0x1653C` wird die gemeldete Mikrofonrate mit `0x4000 - 0x180 = 16000` verglichen.
- Bei Abweichung erzeugt `0x16548` einen Konverter vom Radioformat zu 16.000 Hz / 16 Bit / einem Kanal.
- Ab `0x1656C` wird ein zweiter Konverter für die Gegenrichtung von 16.000 Hz / 16 Bit / Mono zurück zum Radioformat eingerichtet.
- Ab `0x165AC` wird entsprechend Siri gegen `0x6000 - 0x240 = 24000` geprüft und bei Bedarf ein weiteres Konverterpaar erzeugt.
- Die tatsächlichen FFmpeg-Optionen `in_sample_rate`, `out_sample_rate`, Sampleformat und Kanalbelegung werden durch die Methoden ab `0x237C0` und `0x236F4` gesetzt.
- Die Informationsmeldung `mSysInfo.siriSR =%d, siri chls=%d` stammt aus dem Empfang von Radio-Systeminformationen ab `0x16794`; anschließend wird der Konverteraufbau bei `0x167C8` aufgerufen.

Damit ist die zusätzliche Umrechnung direkt belegt. Der bisherige PC-Log enthält jedoch keinen aktiven Teams-Anruf. Er beweist deshalb weder die in diesem Anruf genutzte Radio-Mikrofonrate noch, dass genau die 16-kHz-Konvertierung den hörbaren Unterschied verursacht. 16-kHz-Mono ist für Telefonie an sich ein reguläres Format.

Auch die Testfirmware besitzt in `AudioPlayerCreate` ab `0x1D5FC` weiterhin den gesonderten Telefonzweig (ab `0x1D7F4`) und die Vorgabe 16 Bit. Allein der Hinweis `phone voice issue!` belegt keine behobene Ursache.

## Zwei irreführende Exportnamen

Datei: `customer-root/app/libwcarplay_new.so`.

| Export | Adresse | Tatsächlicher Code |
|---|---:|---|
| `UpdateHUSamplerate` | `0x23BBC` | Logmeldung, dann Rückgabe null |
| `DisableHUAudioFormat` | `0x23BE0` | Logmeldung, dann Rückgabe null |

Beide referenzieren ausdrücklich `%s %d:not implement api,should not be called`. Die ältere Einstufung als zusätzliche nutzbare Konfigurationshebel ist damit korrigiert.

## Audiomodus im USB-Dienst

Datei: `lylink-unpacked/rcpservice`.

- Parser ab `0x21618` liest `aud=0..3` aus der privaten Partition.
- Konstruktor ab `0x2183C` speichert den Wert am CCore-Objektoffset `0x10`.
- Getter `0x2151C` lädt diesen Wert.
- Nachverfolgter Verbraucher ab `0x2E5E4`: Sondermodell 39 liefert eins, ansonsten wird `getAudioMode() != 0` gebildet.
- Aufruf bei `0x2BD60` liegt im Zweig für Audiotyp 8; der Dienst bezeichnet diesen Typ an anderer Stelle als `AudioTypeMainTelephony`.
- Weitere Aufrufe `0x2C4EC` und `0x2C574` beeinflussen den Empfangs-/Pufferpfad.

In diesem konkreten Pfad sind Mode 1, 2 und 3 gleichwertig ungleich null; Default ist null. Das ist kein Vollständigkeitsbeweis über sämtliche Firmwarepfade und keine Bestätigung von drei unterschiedlichen Musik-DSP-Profilen.

## Hyundai-Erkennung

Datei: `lylink-unpacked/rcpservice`.

- Head-Unit-Abfrage ab `0x2D958`, Logmeldung `huInfo name=%s,manufacturer=[%s],model=[%s]`.
- Exakter Vergleich Hersteller `Tinnos` bei `0x2DB74` und Modell `MISTRA` bei `0x2DB86` setzt Modellindex 6.
- Modellindex 6 wird bei `0x2BFA4` beziehungsweise `0x2C0AC` auf den 44,1-kHz-Sonderpfad geleitet; Logmeldung: `mingtu force media sr=44100`.
- Exakter Herstellervergleich `HYUNDAI MOBIS` bei `0x2E2C8` setzt dagegen Modellindex 48.

Der Nutzer fährt einen i30 Kombi von 2018. Ohne HU-Kennung aus dessen aktiver Sitzung ist keiner dieser konkreten Zweige als tatsächlich aktiv belegt.

## Vollständig validierter Logcontainer

Datei: `customer-root/ota/www/cgi-bin/index.cgi`.

- `send_file` liest zunächst `0x333` Byte gzip-Daten (`0x11970`).
- Bei `0x11920` wird die ursprüngliche gzip-Länge als vier Byte Little Endian zwischen diese und die folgenden Daten geschrieben.
- Ab `0x11958` erfolgt die XOR-Maskierung mit `liaoyuan.tech\0`, zurückgesetzt pro 1024 Ausgabebyte.
- Erst XOR rückgängig machen, dann vier Zusatzbyte entfernen; bei kurzen Antworten zusätzlich Padding auf die ursprüngliche Länge kürzen.
- Der eigene Export ist 25.425 Byte groß, das eingebettete gzip 25.421 Byte, der vollständig CRC-geprüfte Klartext 170.868 Byte.

Bei `0x11A8C` prüft die Logfunktion `/tmp/log.gz`. Existiert die Datei, wird der bestehende Stand ausgegeben. Nur wenn sie fehlt, wird ein neuer `dmesg`-/`logcat`-Snapshot erstellt. Ein erneuter HTTP-Abruf ist daher keine neue Laufzeitaufnahme.

Maßgeblicher Klartext: `logs/2026-10-25-0851/logcat.validated.txt`. Die früheren Salvage-Dateien enthalten durch das fehlende Entpacken des Längenfelds verfälschte Daten und sind keine gültigen Messbelege.

## Direkt bestätigte Flashkarte

Quelle: CRC-geprüfter Startlog des eigenen Geräts. Einheit: Byte; Endadresse exklusiv.

| MTD | Partition | Start | Ende |
|---:|---|---:|---:|
| 0 | uboot | `0x000000` | `0x060000` |
| 1 | boot | `0x060000` | `0x370000` |
| 2 | recovery | `0x370000` | `0x680000` |
| 3 | rootfs | `0x680000` | `0xB00000` |
| 4 | customer | `0xB00000` | `0xEA0000` |
| 5 | env | `0xEA0000` | `0xEB0000` |
| 6 | env-redund | `0xEB0000` | `0xEC0000` |
| 7 | private | `0xEC0000` | `0xED0000` |
| 8 | logo | `0xED0000` | `0xF80000` |
| 9 | UDISK | `0xF80000` | `0x1000000` |

Ein Hersteller-Update von Boot und Customer enthält keine individuelle private Partition. Vor einer Firmwaremodifikation ist ein eigener vollständiger Dump nötig; ein Image eines fremden Adapters wäre dafür kein Ersatz.

## Wiederholung und Referenz

```powershell
.\.venv\Scripts\python.exe tools\disassemble_riscv_andes.py evidence\firmware\26011517.5234.2\decrypted\customer-root\app\libwcarplay_new.so --start 0x23bbc --length 0x48
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Opcode-Masken und Offsetfelder wurden mit dem [vom Andes-Entwickler veröffentlichten binutils-Patch](https://sourceware.org/pipermail/binutils/2025-November/145934.html) abgeglichen. Das ist die Instruktionsreferenz; die gerätespezifischen Audiobefunde stammen aus den eigenen archivierten Binärdateien.
