# Integrierte Adapter-Diagnose

Version: 0.6.0  
Stand: 2026-10-25 10:16 CET

Die Diagnosekarte sitzt direkt auf der Einstellungsseite. Sie ist ein lesender Bereich; die bisherigen Hersteller-Einstellungen bleiben separat bedienbar.

- **Werte aktualisieren:** CPU über zwei Zählerstände, belegter/gesamter RAM, Laufzeit, USB-Gadget-Zustand und kumulative WLAN-Zähler.
- **Aufzeichnung starten/stoppen:** alle zwei Sekunden einen Statuspunkt im Browser erfassen, maximal 30 Minuten. Nach Neuladen der Seite sind ungespeicherte Messpunkte weg.
- **Sitzung speichern:** Aufzeichnung, ausgewählte Konfiguration und zuletzt ausgewertetes Audiofragment als lokale JSON-Datei speichern.
- **Audio-Log auswerten:** die letzten 200 passenden Logzeilen frisch auslesen. Telefon-Ausgabe (`phone call rate=…, sz=…`), Anfrage für Audiotyp 8, protokollierte Mikrofonumwandlung und Pufferwarnungen getrennt anzeigen.
- **Frisches Geräteprotokoll speichern:** proc-Daten, dmesg und logcat direkt als lokale Textdatei laden. Keine OEM-Cloudübertragung und kein Zugriff auf den alten Logexport-Cache.

Unbekannte Werte bleiben unbekannt. Eine 48-kHz-Musikmeldung wird nicht als Telefonrate gewertet. Mono/16 kHz allein sind bei Telefonie kein Fehlernachweis. WLAN-Drops sind kumulative Schnittstellenwerte und keine gemessene CarPlay-Paketverlustrate. Logzeilenzähler beweisen weder Fehlerfreiheit noch die Ursache des blechernen Tons.

Für den Teams-Versuch: Adapter im Fahrzeug neu starten, Diagnose öffnen und Aufzeichnung starten, den hörbar betroffenen Teams-Anruf durchführen, danach Audio-Log auswerten, Aufzeichnung stoppen sowie Sitzung und frisches Geräteprotokoll speichern. Original-Kabelvergleich am selben iPhone beibehalten. Die Diagnose kann nur Meldungen anzeigen, die die Firmware tatsächlich protokolliert; sie ergänzt keine nativen Audio-Debughooks.

Der neue CGI akzeptiert nur GET mit exakt `id=status`, `id=audio` oder `id=logs`. Es gibt keine frei wählbaren Befehle/Dateipfade, keinen Logpuffer-Reset und keine persistenten Geräteschreibvorgänge. Dateien können Gerätekennungen enthalten und werden nicht automatisch veröffentlicht.
