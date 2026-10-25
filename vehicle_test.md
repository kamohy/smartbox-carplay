# Fahrzeugtest – Hyundai i30 Kombi 2018

Version: 0.4.1  
Stand: 2026-10-25 09:19 CET

Bestätigt: Teams-Anrufe klingen mit dem Adapter in beiden Richtungen blechern. Derselbe Teams-Anwendungsfall am selben iPhone klingt direkt per USB deutlich besser. Ziel ist die Eingrenzung der zusätzlichen Telefon-Audiostrecke. Der Versuch erfolgt im geparkten Fahrzeug.

## Erster aussagekräftiger Versuch

1. Den SmartBox-Adapter kurz vom Fahrzeug-USB trennen und neu einstecken. Mode 2 bleibt zunächst eingestellt.
2. Nur eine eventuell parallel aktive direkte Bluetooth-Verbindung zwischen iPhone und Hyundai trennen. Bluetooth am iPhone und die SmartBox-Kopplung bleiben aktiv.
3. Die CarPlay-Verbindung vollständig aufbauen lassen und einen Teams-Anruf durchführen, bei dem der Fehler auftritt. Beide Richtungen beurteilen: Wiedergabe im Auto und Mikrofon beim Gesprächspartner.
4. Vermerken, ob das Stummschalten des eigenen Teams-Mikrofons den Klang der Gegenstelle im Auto verändert. Das hilft, einen Zusammenhang mit dem bidirektionalen Sprachpfad beziehungsweise Echoverarbeitung zu erkennen.
5. Erst nach diesem Fehlerfall erstmals Diagnose exportieren. Dazu den PC mit dem SmartBox-WLAN verbinden und aus `E:\WorkSpace\carplay` ausführen:

```powershell
.\tools\capture_device_state.ps1
```

Der neue Unterordner in `evidence\logs` enthält Original, geprüften Klartext und Metadaten. Entscheidend sind Telefonrate, Radio-Ein-/Ausgabeformate und Resampling; die Musikrate ist hier kein Ersatz.

## Ohne PC im Auto

Falls Safari auf dem per CarPlay verbundenen iPhone die Adapteroberfläche erreicht, nach dem betroffenen Anruf direkt diesen Diagnoseexport öffnen und die Datei in „Dateien“ sichern:

`http://192.168.1.101/cgi-bin/index.cgi?id=logcat`

Es ist normal, dass diese Datei zunächst unlesbar ist. Die Entschlüsselung und CRC-Prüfung erfolgen anschließend hier im Projekt. Falls die Adresse über die aktive CarPlay-Verbindung nicht erreichbar ist, den PC-Weg verwenden; ein erster früherer Diagnoseabruf darf nicht vorgeschaltet werden.

## Warum die Reihenfolge wichtig ist

Der Adapter erstellt `/tmp/log.gz` beim ersten Diagnoseabruf und verwendet diese Datei danach erneut. Ein Abruf unmittelbar nach dem Einschalten enthält ein späteres Telefonat nicht. Eine Cache-Warnung im Erfassungsskript bedeutet, dass der Export bereits bekannt ist. Dann den Adapter vor dem nächsten Telefonat erneut stromlos starten.

## Gegenproben

Einen normalen Telefonanruf über denselben Adapter prüfen. Ist er ebenfalls beidseitig blechern, betrifft es vermutlich einen gemeinsamen Telefonpfad; klingt nur Teams schlechter, ist die appabhängige Routenauswahl beziehungsweise Verarbeitung besonders relevant. Die konkrete Ursache ist in beiden Fällen noch zu messen.

Musik separat als Kontrollfall testen. Einwandfreie Musik bei schlechten Anrufen würde die Trennung von Musik- und Telefonpfad bestätigen. Der bessere Teams-Kabelvergleich ist bereits vom Nutzer bestätigt; bei Bedarf lässt er sich im selben Gespräch erneut abgrenzen.

Weitere Audiomodi erst anhand des ersten Telefonlogs auswählen. Der bisher nachvollzogene Telefon-Pufferpfad unterscheidet Default von 1/2/3, behandelt 1/2/3 dort aber gleich. Ein pauschaler Wechsel auf Mode 3 wäre kein gezielter Fix.

## Auswertung

- Welchen Hersteller und welches Modell meldet das Radio (`huInfo`)?
- Welche Rate/Kanalzahl meldet `media phone audio`? Welche Radio-Mikrofonformate werden gemeldet?
- Was steht in `AudioPlayerCreate`, `phone call rate`, `mSysInfo.siriSR` und den Resampler-Meldungen?
- Welche ursprüngliche Rate kommt von der iPhone-Seite, welche wird für den USB-Dienst gesetzt?
- Ändert Stummschalten den Klang? Betrifft es native Telefonanrufe ebenfalls?
- Gibt es Paket-, Puffer-, Underrun- oder Formatfehler?

Mono und 16-kHz-Sprachformate sind bei Telefonaten regulär und allein kein Fehler. Entscheidend ist, ob der Adapter gegenüber der direkten USB-Verbindung unnötig Bandbreite reduziert, falsch umrechnet oder Sprachverarbeitung ungünstig kombiniert. Für die Hyundai-Zuordnung genügt das Baujahr nicht; entscheidend ist die vom Radio gemeldete Kennung.
