# Gezielte Messstelle für die Telefonformatauswahl

Analyse-/Werkzeugversion: 0.8.1  
Stand: 2026-10-25 12:14 CET

Die Fahrzeuglogs beweisen den 8-kHz-Telefonpfad, enthalten aber weder die vollständige verwendete Fähigkeitsmaske noch den Wert der Versionsprüfung. Der neue Offlinekandidat ergänzt diese Angaben an zwei bereits vorhandenen Logstellen im originalen `rcpservice`. Er ist nicht in einem Geräteimage integriert, nicht ausgeführt und nicht geflasht. Installierte Geräte-UI bleibt 0.7.0; das getrennte UI-Paket 0.8.0 wartet auf erfolgreiche Geräteprüfung.

## Exakt begrenzte Änderung

- Quellbinary: 209.188 Byte, SHA-256 `0d0d6c885dde39205074e7d9989f339561b69202182f26d33a5d1e71cbf37cc9`.
- Bei ELF-Adresse `0x2BF80` wird der Logparameter aus Stackoffset `0x28` geladen; bei `0x2C088` entsprechend aus Offset `0x04`. Das sind die in den jeweiligen Strukturzweigen benutzten Fähigkeitswörter.
- In derselben ursprünglichen Vier-Byte-Lücke wird zusätzlich Register `s2` als zweiter Logparameter übergeben. Es enthält den ersten numerisch ausgewerteten Plugin-Versionsteil, beziehungsweise null, wenn der betreffende Code ihn nicht geparst hat.
- Der bereits referenzierte Formattext bei `0x3EADC` wird in-place durch `BH_HU mask=%08x gate=%u` ersetzt. Keine Vergrößerung und keine Verschiebung von Code/Dateiteilen.
- Audioauswahl, Versionsvergleich, Branches, Logaufrufadressen und Formatzeiger bleiben unverändert. Insgesamt unterscheiden sich 38 Byte in exakt drei erlaubten Regionen.

Kandidat-SHA-256: `2cbbaf825e8b3038ac9c53153b5ca6bd8800e121ce89d9526808846f2842fb40`.

`tools/prepare_phone_probe.py` lehnt jede andere Quelldatei ab. Capstone dekodiert die neuen komprimierten RISC-V-Instruktionen unabhängig als `c.lwsp a2,...(sp)` und `c.mv a3,s2`. Drei lokale Regressionen prüfen Instruktionen/Offsets, Ablehnung fremder Quellen und den begrenzten realen Dateiunterschied. Das beweist statische Plausibilität und Byteumfang, noch keinen erfolgreichen Runtimeeinsatz.

## Was die spätere Ausgabe klären kann

Im bereits verfolgten Auswahlpfad kennzeichnet Bit 2 die 8-kHz- und Bit 4 die 16-kHz-Alternative. Wenn beide gesetzt sind, kann der Versionsvergleich gegen 319 die 16-kHz-Auswahl verhindern. Fehlt Bit 4, gibt es in diesem Wort keinen entsprechenden 16-kHz-Hinweis. Ein gesetztes Bit beweist weder ein fehlerfrei arbeitendes Radioformat noch bessere hörbare Qualität. `gate=0` ist nicht automatisch eine echte Plugin-Version null.

Die Messung soll eine gezielte Entscheidung zwischen fehlender Formatanzeige, Versionsregel und möglicher späterer Umstellung ermöglichen. Sie ersetzt keinen vollständigen CarPlay-/Hyundai-Emulator. Eine Integration benötigt zusätzlich einen eng begrenzten Start-/Dateipfad und eine Aufbewahrung der neuen `BH_HU`-Zeile; beides wurde hier noch nicht in die laufende Firmware aufgenommen.

```powershell
.\.venv\Scripts\python.exe tools\prepare_phone_probe.py
.\.venv\Scripts\python.exe -m unittest tests.test_phone_probe -v
```

Lokale Binärausgabe: `dist/phone-probe-0.8.1/`. Das Werkzeug enthält keine Netzwerk-, Upload- oder Geräteausführungsfunktion.
