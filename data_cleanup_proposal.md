# Umfang der verfügbaren Hersteller-Löschung

Version: 0.8.3
Stand: 2026-10-25 14:00 CET

Die installierte Oberfläche 0.7.0 besitzt keinen eigenen Log-Löschendpunkt. Die vorbereitete begrenzte Löschfunktion ist wegen des festhängenden Updaters noch nicht installiert.

Der originale CGI-Code enthält eine alternative Datenlöschung. Die Analyse der eigenen gepinnten 5234-Basis zeigt bei Funktion 0x13420:

- Bei `rst=1` wird der Inhalt von `/mnt/UDISK` vollständig gelöscht und anschließend neu gestartet.
- Die zusätzliche Löschung des privaten Einstellungsbereichs wird ausschließlich bei `rst=2` aufgerufen. Diese Variante ist nicht vorgeschlagen.
- Der feste Shellbefehl lautet `rm -rf /mnt/UDISK/* /mnt/UDISK/.*`. Er begrenzt sich nicht auf `bh-logs`.
- Die eigenen Programme referenzieren auf dieser Partition unter anderem `btapp.db`, Telefon-/Bluetoothdateien und Start-/Modusmarker. Gespeicherte Kopplungen würden mitgelöscht; das iPhone müsste anschließend gegebenenfalls neu gekoppelt werden.
- Firmwaredateien und Kernel werden von `rst=1` nicht neu geschrieben. Die bekannten privaten Audio-/LED-/WLAN-Einstellungen werden vorher gesichert und nachher verglichen.

Die vorgeschlagene Anfrage ist nur als Code dargestellt, damit sie nicht versehentlich über einen Link ausgelöst wird:

```text
GET /cgi-bin/index.cgi?id=set&rst=1
```

**Nach ausdrücklicher Nutzerfreigabe am 2026-10-25 um 14:00 ausgeführt und verifiziert.** Alte erreichbare Logs entfernt; 304 statt 224 KiB frei; neun verglichene Einstellungen unverändert; neue Aufzeichnung mit Bootzähler 1 aktiv. Die vorherige Vorschlagsbeschreibung bleibt zur Nachvollziehbarkeit stehen. Diese zusätzliche Zustimmung wurde vor der Ausführung ausdrücklich eingeholt. Die ursprüngliche Beauftragung betraf nur Logs. Alle über die Diagnose erreichbaren aktuellen Logdateien wurden vor der Ausführung nochmals CRC-/SHA-256-geprüft lokal gesichert. Weitere fremde UDISK-Dateien sind über die aktive API nicht vollständig auflistbar oder gesichert.

Die Anfrage wurde nach der Freigabe genau einmal gesendet. Bei unklarer Antwort wird sie nicht automatisch wiederholt. Nach dem Neustart werden Gerätezustand, Einstellungen, freie Kapazität und das Verschwinden der alten Logdateien überprüft. Die automatische Aufzeichnung kann anschließend neue Logs anlegen; eine dauerhaft leere Liste ist daher kein zugesagter Zustand.
