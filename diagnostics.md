# Integrierte Adapter-Diagnose

Version: 0.7.0  
Stand: 2026-10-25 10:47 CET

## Neuer Stand 0.7.0

CPU/RAM/Laufzeit aktualisieren sich alle zwei Sekunden automatisch bei sichtbarer Seite. Kein Startknopf und kein Node-Runtime erforderlich. CPU nutzt Laufzeit-/Idle-Sekunden, weil die Idle-Jiffies auf dem echten Gerät stehenblieben. Die optionale Browseraufzeichnung ist davon unabhängig.

Der native Recorder startet ohne offene Webseite. Ausschließlich `bh-logs/` auf dem vorhandenen RW-Datenmount `/mnt/UDISK` wird beschrieben. Alle fünf Sekunden werden höchstens 120 Statuspunkte im RAM gehalten. Ungefähr jede Minute entsteht ein gzip-Snapshot mit Messpunkten, Kernelmeldungen, begrenztem logcat und letzten passenden Audiozeilen. Drei Starts mit je zwei Dateien bis 24 KiB begrenzen die Nutzlast auf 144 KiB plus Metadaten; mindestens 64 KiB bleiben frei. Bei Platzmangel bleiben vorhandene vollständige Logs erhalten. Es wird nicht partitioniert/formatiert. Die jüngste noch nicht gespeicherte Minute kann beim Abziehen fehlen; der Ring ist kein lückenloses Dauerarchiv.

Die Seite zeigt tatsächlichen Speicherstatus, lokale Downloads und eine begrenzte Sofortspeicher-Anforderung. Für Audioauswertung kann ein früherer Start gewählt werden. Der CGI akzeptiert zusätzlich feste Archiv-/Speicher-GETs und ausschließlich `POST id=save` als Schreibanforderung. Fremde Origins, zusätzliche Parameter und frei wählbare Befehle/Dateipfade werden abgewiesen. Keine automatische Veröffentlichung lokaler Logs.

0.7.0 muss noch realen Mount/Platz, Recorderstart und Erhalt nach Neustart/Stromtrennung bestätigen. 0.6.0 wurde installiert und funktional geprüft; dort waren Logs ausschließlich im RAM. Nach erfolgreicher Recorderprüfung: Teams-Anruf durchführen und noch etwa eine Minute eingeschaltet lassen; gespeicherte Logs später am PC von derselben Seite laden.

## Historischer Bedienumfang 0.6.0

Die Diagnosekarte sitzt direkt auf der Einstellungsseite. Sie ist ein lesender Bereich; die bisherigen Hersteller-Einstellungen bleiben separat bedienbar.

- **Werte aktualisieren:** CPU über zwei Zählerstände, belegter/gesamter RAM, Laufzeit, USB-Gadget-Zustand und kumulative WLAN-Zähler.
- **Aufzeichnung starten/stoppen:** alle zwei Sekunden einen Statuspunkt im Browser erfassen, maximal 30 Minuten. Nach Neuladen der Seite sind ungespeicherte Messpunkte weg.
- **Sitzung speichern:** Aufzeichnung, ausgewählte Konfiguration und zuletzt ausgewertetes Audiofragment als lokale JSON-Datei speichern.
- **Audio-Log auswerten:** die letzten 200 passenden Logzeilen frisch auslesen. Telefon-Ausgabe (`phone call rate=…, sz=…`), Anfrage für Audiotyp 8, protokollierte Mikrofonumwandlung und Pufferwarnungen getrennt anzeigen.
- **Frisches Geräteprotokoll speichern:** proc-Daten, dmesg und logcat direkt als lokale Textdatei laden. Keine OEM-Cloudübertragung und kein Zugriff auf den alten Logexport-Cache.

Unbekannte Werte bleiben unbekannt. Eine 48-kHz-Musikmeldung wird nicht als Telefonrate gewertet. Mono/16 kHz allein sind bei Telefonie kein Fehlernachweis. WLAN-Drops sind kumulative Schnittstellenwerte und keine gemessene CarPlay-Paketverlustrate. Logzeilenzähler beweisen weder Fehlerfreiheit noch die Ursache des blechernen Tons.

Für den Teams-Versuch: Adapter im Fahrzeug neu starten, Diagnose öffnen und Aufzeichnung starten, den hörbar betroffenen Teams-Anruf durchführen, danach Audio-Log auswerten, Aufzeichnung stoppen sowie Sitzung und frisches Geräteprotokoll speichern. Original-Kabelvergleich am selben iPhone beibehalten. Die Diagnose kann nur Meldungen anzeigen, die die Firmware tatsächlich protokolliert; sie ergänzt keine nativen Audio-Debughooks.

Der neue CGI akzeptiert nur GET mit exakt `id=status`, `id=audio` oder `id=logs`. Es gibt keine frei wählbaren Befehle/Dateipfade, keinen Logpuffer-Reset und keine persistenten Geräteschreibvorgänge. Dateien können Gerätekennungen enthalten und werden nicht automatisch veröffentlicht.
