# Gültigkeit der Diagnoselogs

Version: 0.4.0  
Stand: 2026-10-25 09:12 CET

Maßgeblicher geprüfter Export des bisherigen PC-Starts:

- Original: `2026-10-25-0851/logcat.encrypted`
- Gültiger Klartext: `2026-10-25-0851/logcat.validated.txt`
- Prüfmetadaten: `2026-10-25-0851/logcat-metadata.json`
- SHA-256 des gültigen Klartexts: `87AC31A4CA8DFE27CDA8BEFCB506D939C0CF281AFE236EA4169AA4B141B2B730`

`2026-10-25-strict-validated` enthält eine mit dem korrigierten Erfassungsskript erzeugte, ebenfalls vollständig CRC-geprüfte Kopie desselben gecachten Geräteexports. Sie ist keine zweite unabhängige Laufzeitsitzung.

Frühere Dateien namens `logcat.txt` in `2026-10-25-0851`, `2026-10-25-0900-validated` und `2026-10-25-continued-readonly` entstanden vor der Entdeckung des eingefügten vier Byte langen Größenfelds. Diese Salvage-Ableitungen sind verfälscht und werden nur als Arbeitsgeschichte aufbewahrt. Das Wort `validated` im alten Ordnernamen bezeichnete den damaligen Skriptlauf und ist kein Nachweis einer gültigen gzip-CRC.

Weitere identische verschlüsselte Dateien sind Wiederholungsabrufe von `/tmp/log.gz`; ihre mehrfachen Dateinamen beweisen keine neuen Ereignisse. Für eine neue Fahrzeugsitzung Adapter zuerst stromlos starten, Musik abspielen und danach erstmals Diagnose exportieren.
