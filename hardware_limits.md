# Hardware, Reserven und sinnvolle Verbesserungen

Version: 0.8.0  
Stand: 2026-10-25 11:57 CET

## Was auf diesem Adapter belegt ist

| Bauteil/Bereich | Belegter Stand | Grenze der Aussage |
|---|---|---|
| SoC | Allwinner V821B, RISC-V laut geprüftem eigenen Bootlog | Konkrete Laufzeit-Taktwerte werden mit 0.8.0 zusätzlich abgefragt. |
| RAM | 64 MiB adressiert, 58.124 KiB für Linux sichtbar | Keine frei aufrüstbare Softwaregröße. |
| Flash | XT25P1288, 16 MiB SPI-NOR | Bezeichnung aus realer Flash-Erkennung, keine Platinenaufnahme. |
| Datenpartition | 512 KiB; eigener begrenzter Logring | Freier Platz ändert sich mit Logs und Dateisystemverwaltung. |
| WLAN | 5 GHz/802.11n im Betrieb; RTL8733BS-Treiber im Kernel | Treibername beweist noch nicht die genaue Modul-/Platinenvariante. |
| Bluetooth | Realtek-Initialisierungsprofil RTL8723FS | Profilname ist kein unabhängiger physischer Chipnachweis. |
| Telefon-Audio | iPhone-Anfrage 16 kHz, USB-Telefonpfad 8 kHz, Mikrofon 8→16 kHz | Beide Teams-Modi 2/3 so gemessen; Radiofähigkeit für 16 kHz noch offen. |

Die neue feste Hardwareabfrage ergänzt CPUinfo, cpufreq (falls vorhanden), Speicher-/Partitionstabelle und USB-/SDIO-Kennungen. Fehlende sysfs-Angaben werden nicht aus BogoMIPS oder Produktwerbung ersetzt. Rohdaten bleiben lokal. Ohne Platinenzugang sind nicht alle Chipaufdrucke, Antennen und die elektrische Beschaltung prüfbar.

Zusätzlich wurde der originale Device Tree tatsächlich ausgewertet: Er deklariert einen Linux-CPU-Knoten und je 16 KiB Instruktions-/Datencache. Die zunächst referenzierte OPP-Tabelle bietet 360–960 MHz; 1.000/1.008 MHz sind dort deaktiviert. Eine zweite Tabelle enthält Stufen bis 1.200 MHz. Das sind Firmwaretabellen für unterschiedliche Konfigurationen, kein Beweis für den aktuell aktiven Takt oder eine sichere Übertaktungsreserve. Lokaler Hash-/Strukturbeleg: `evidence/hardware/2026-10-25/device-tree-cpu.json`.

Die [Allwinner-Produktseite](https://www.allwinnertech.com/index.php?c=product&id=136) nennt für die V821-Familie eine heterogene RISC-V-CPU/MCU-Architektur, macht aber ausdrücklich eine Untermodell-Einschränkung auf V821L2-WXX. Die dort beworbenen Höchsttakte sind daher kein Beweis für Takt oder zusätzliche nutzbare Linux-Kerne unseres V821B. Eine MCU wäre auch kein automatisch frei zuschaltbarer zweiter Linux-Kern.

Ein [RTL8733BS-Modul von Fn-Link](https://fr.fn-link.com/amp/Module-Wi-Fi-6233A-SRB-pd47285459.html) wird mit 1T1R, 802.11a/b/g/n und bis zu 150 Mbit/s beschrieben. Das ordnet die Treiberfamilie ein, identifiziert jedoch nicht das tatsächlich verlötete Modul dieses Dongles. Eine Umstellung auf Wi-Fi 6 allein durch eine andere Einstellungsseite ist daraus nicht ableitbar.

## Sind wir am Maximum?

**Eine vollständige Ausreizung der Hardware ist nicht nachgewiesen. Ein pauschaler Prozentgewinn ist ebenso wenig nachgewiesen.** Die gemessenen Grenzen sind getrennt zu bewerten:

- **Telefonbandbreite:** Im Originalcode existiert eine Auswahl für 16 statt 8 kHz. Falls das Radio den passenden 16-kHz-Telefonmodus unterstützt und nur die Auswahl ungünstig ist, wäre dieser Pfad ein konkreter Verbesserungsansatz. Das verdoppelt die Abtastrate; es bedeutet weder doppelte wahrgenommene Klangqualität noch einen bereits sicheren Fix.
- **Mikrofonverarbeitung:** Bei übereinstimmenden 16-kHz-Formaten könnte eine zusätzliche 8↔16-kHz-Umrechnung entfallen. Das ist erst nach Prüfung der echten Radioformate und des Datenpfads belegbar.
- **CPU:** Im Fahrzeuglog lagen die Mediane der erfassten Intervalle bei etwa 65,3 %/70,6 %, mit Spitzen bis 99,5 %/93,5 %. Durchschnittsreserve ist kein garantierter Echtzeitspielraum. Ein Leistungsgewinn durch Takterhöhung ist damit nicht belegt.
- **RAM:** Mindestens etwa 16,7 beziehungsweise 20,0 MiB waren in den erfassten Fahrzeugpunkten verfügbar. Es gibt dort keinen Beleg für einen dauerhaft vollständig belegten RAM. Mehr RAM allein hebt keine 8-kHz-Formatwahl auf.
- **WLAN:** Die bisherigen p2p-Bytezähler zeigen nicht den realen Datenverkehr. Vor einer Funkoptimierung müssen die tatsächlichen Schnittstellen und Fehler getrennt gemessen werden. 16-kHz-Mono mit 16 Bit benötigt rechnerisch nur 256 kbit/s unkomprimiert je Richtung; trotzdem können Funkstörungen oder Zeitverhalten relevant sein.
- **Flash:** Der größte Teil der 16 MiB ist durch Boot, Recovery, Rootfs und Customer belegt. Freie Bytes in der schreibgeschützten Customer-Partition werden nicht automatisch zu freiem Logspeicher. Ein neues Partitionslayout ist kein notwendiger Schritt für die aktuelle Audioverbesserung.

## Was als Nächstes Gewissheit bringt

1. Reale Takt-/Bus-/Chipinformationen aus der festen Hardwareabfrage sichern.
2. Beim nächsten Fahrzeugstart die frühe Radio-/Plugin-/Formatauswahl erhalten. 0.8.0 bewahrt passende Anfangsmeldungen zusätzlich begrenzt auf; die vollständigen Fähigkeitsmasken müssen gegebenenfalls noch gezielt instrumentiert werden.
3. Erst daraus eine auf tatsächlich unterstützte Telefonformate beschränkte Änderung ableiten.
4. Direkten Kabelbetrieb und Adapterbetrieb hörbar sowie, soweit erfassbar, anhand ihrer Formate vergleichen. Keine Musikratenänderung als Telefon-Fix ausgeben.

## Emulator als zusätzlicher Prüfstand

Der Nutzer fragte während des Updates nach einem Emulator. [Apples eigenständiger CarPlay Simulator auf dem Mac](https://developer.apple.com/videos/play/wwdc2022/10016/) arbeitet mit einem echten iPhone; er ist vom reinen CarPlay-Fenster des Xcode-iOS-Simulators zu unterscheiden. [LIVI](https://f-io.github.io/LIVI/) bietet eine native Head-Unit-Implementierung für Linux/macOS und setzt für CarPlay zusätzliche Authentifizierung voraus. Ein kompatibler Windows-Prüfstand für genau diesen SmartBox-Dongle ist noch nicht verifiziert.

Ein gezielter Prüfstand könnte 8-/16-kHz-Angebote, Versionsangaben und Verbindungsabläufe reproduzierbar variieren. Ein Offline-Modell allein prüft dagegen nur die nachgebildete Logik. Weder die vollständige Hyundai-Emulation noch ein direktes USB-Zwischengerät auf dem vorhandenen Windows-PC sind damit bereits bewiesen. Es wurde hierfür keine Fremdsoftware installiert und der laufende Firmwaretransfer nicht neu gestartet.
