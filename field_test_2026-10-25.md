# Fahrzeuglog: Telefonpfad mit 8 kHz

Projekt-/Analyseversion: 0.7.1  
Installierte Geräteoberfläche: 0.7.0  
Stand: 2026-10-25 11:41 CET

## Ergebnis

Der erste Fahrzeugtest enthält einen konkreten Engpass: Das iPhone fordert für Telefon-Audiotyp 8 jeweils 16.000 Hz, 16 Bit und Mono an. Der Adapter startet denselben Telefonpfad zum Radio mit 8.000 Hz, 16 Bit und Mono. Dies ist in Mode 2 und Mode 3 belegt. Die USB-/Head-Unit-Taktrückmeldung liegt während dieser Abschnitte ebenfalls bei ungefähr 8.000 Hz. Im Mikrofonpfad ist die zusätzliche Umwandlung 8.000 → 16.000 Hz protokolliert.

Der Nutzer bestätigt für beide Modustests Teams. Nach dem Moduswechsel sei der Klang besser, aber weiterhin merkwürdig gedämpft. Die 8-kHz-Strecke passt zu diesem verbleibenden Verlust an Sprachbandbreite in beiden Richtungen. Sie ist ein gemessener Formatengpass, noch kein vollständiger Nachweis sämtlicher hörbarer Fehlerursachen. Ein digitaler Kabelvergleich mit Format-/PCM-Daten fehlt weiterhin.

## Auswertung

| Merkmal | Start 5, Mode 2 | Start 6, Mode 3 |
|---|---:|---:|
| iPhone-Telefonanfrage | 16.000 Hz / 16 Bit / Mono | 16.000 Hz / 16 Bit / Mono |
| USB-Telefonstart | 8.000 Hz / 16 Bit / Mono | 8.000 Hz / 16 Bit / Mono |
| Taktrückmeldung nach Telefonstart | 7.999,975–8.000,014 Hz | 7.999,964–8.000,040 Hz |
| Mikrofonumwandlung | 8.000 → 16.000 Hz | 8.000 → 16.000 Hz |
| Eindeutige Telefon-Audiostarts | 3 | 2 |
| `underrun`/`overrun`/`xrun` im erfassten Ausschnitt | 0 | 0 |

Audiostarts sind keine Anrufzählung: Ein Anruf kann den Audiopfad mehrfach starten. Überlappende Snapshots und die zusätzliche Audiosektion wurden pro Gerätestart zeilenweise dedupliziert. Musik-/Neben-Audiotyp 64 mit 48 kHz wurde getrennt gehalten.

Sechs gzip-Dateien aus den Starts 5, 6 und 7 wurden lokal gesichert; alle bestehen die vollständige gzip-CRC-Prüfung. Start 7 ist die anschließende PC-Sitzung ohne Telefon-Audiostart. Rohdaten und individuelle Kennungen bleiben unter `evidence/field-tests/2026-10-25-113352/` und werden nicht veröffentlicht. `manifest.json` enthält Dateihashes, `analysis-0.7.1.json` die reproduzierbare Offlineauswertung.

## Bedeutung für eine Verbesserung

Eine 8-kHz-Abtastrate kann Frequenzen oberhalb von 4 kHz nicht übertragen; spätere Umrechnung auf 16 kHz stellt diesen verlorenen Inhalt nicht wieder her. Eine höhere Musikrate oder ein Wechsel zwischen Mode 2 und 3 hebt den hier beobachteten Telefonengpass nicht auf.

Eine feste Hardwaregrenze von 8 kHz ist damit nicht bewiesen. Im unveränderten `rcpservice` wird die Telefonrate anhand von `GetHUAudioFormat` und `GetHUPluginVer` ausgewählt. Die Funktion ab `0x2BEAC` enthält sowohl 8- als auch 16-kHz-Zweige:

- `0x2BEE0/0x2BEE4`: Aufruf `GetHUAudioFormat`.
- `0x2BEF4/0x2BEF8`: Aufruf `GetHUPluginVer`; ab `0x2C164` wird dessen erster Zahlenteil mit `strtoul` ausgewertet.
- `0x2BF58` beziehungsweise `0x2C03C`: Auswahl des betreffenden Fähigkeitsworts.
- Bit 2 führt bei `0x2C058` zunächst zu 8.000 Hz und Mono.
- `0x2C06A`: Ein Versionsvergleich gegen 319 kann die anschließende 16-kHz-Auswahl überspringen.
- `0x2C06E` prüft Bit 4; `0x2C072` beziehungsweise `0x2C13C` setzen 16.000 Hz und Mono.

Das sind statische Auswahlpfade, keine bereits gemessenen 16-kHz-Fähigkeiten dieses Radios. Die tatsächlichen Fähigkeitswörter und die konkrete Plugin-Version fehlen im erhaltenen Logausschnitt. Die Versionssperre oder die Rate blind zu überschreiben wäre deshalb noch kein belegter Fix. Nächster gezielter Schritt ist, diese Anfangsdaten dauerhaft mitzuerfassen und daraus einen auf tatsächlich unterstützte Telefonformate begrenzten Versuch abzuleiten.

## Weitere Grenzen der Diagnose

- Die Herstellerzeile `HidClient mic times = 1, rate = 8000kHz -> 16000kHz` hat eine falsche Einheit. Der überprüfte Konvertercode arbeitet mit 8.000 und 16.000 **Hz**. Die installierte Webauswertung 0.7.0 übernimmt diese falsche kHz-Beschriftung; der Offlineanalysator interpretiert die Werte anhand des geprüften Codes korrekt.
- Die ausgewählte Netzwerkschnittstelle `p2p-wlan0-0` meldet in diesen Messpunkten null RX-/TX-Bytes. Daraus lässt sich keine CarPlay-Verlustrate ableiten. Für weitere Tests müssen die tatsächlich Daten übertragenden Schnittstellen getrennt erfasst werden.
- CPU-Median der erfassten Intervalle: etwa 65,3 % beziehungsweise 70,6 %; Spitzen bis 99,5 % beziehungsweise 93,5 %. Mindestens etwa 16,7 beziehungsweise 20,0 MiB RAM waren verfügbar. Diese Daten schließen einzelne Echtzeitprobleme nicht aus.
- Fehlende Pufferwarnungen im begrenzten Ausschnitt beweisen keine störungsfreie Audioübertragung. Die Kalenderzeit der Gerätezeilen ist nicht verlässlich; sie beginnen am 1. Januar.

## Wiederholen

```powershell
.\.venv\Scripts\python.exe tools\analyze_field_logs.py evidence\field-tests\2026-10-25-113352
.\.venv\Scripts\python.exe -m unittest tests.test_field_logs -v
```

In diesem Arbeitsblock wurde weder eine neue Firmware geflasht noch der Audiomodus geändert. Beim Auslesen war `aud=3`, `mic=0`, Kanal 149 und `conn=cp` aktiv. Projektversion 0.7.1 bezeichnet Analysewerkzeug und Dokumentation; installierte UI und öffentlich angebotene Firmware bleiben 0.7.0.
