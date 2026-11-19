# Exercise 14.4 – Technischer Bericht für Human Review

**AWAITING HUMAN REVIEW**, 19.11.2026. Keine studentische Bewertung/Freigabe erhalten.
Codex: offizielle Aufgabe/Kurskontext gelesen, Implementierung, tatsächliche technische
und visuelle Prüfungen. Quellen/Abrufdatum und Anforderungen direkt im Notebook.

## Umsetzung und beobachtete Ergebnisse
Offizielle Aufgabe: Plotly-Parallelkoordinaten aller kontinuierlichen Variablen,
gewähltes kategoriales Fehlerflag, kategoriales Type und Type-Farbe; Jupyter-Dropdown,
Achsenumordnung und Brushing tatsächlich nutzen. Keine zusätzliche Modellstudie.

Alle 10.000 Zeilen; fünf Originalmessgrößen plus Kursmerkmale temp_diff [K]/power [W]
und bereits geprüftes wearadjTorque [min·Nm]. UDI/Product ID sind Kennungen, keine
Messachsen. Feste diskrete Type-Farben und Flag-Ticks 0/1; Kategoriencodes ohne
metrische Zwischenbedeutung. Fünf Fehlertypen und allgemeines Machine failure wie
in ERROR_VARS des Kurses auswählbar. Kein neues Training, daher kein TRAIN/TEST nötig.

Gebürstete positive Zeilen: Machine failure 339, TWF 46, HDF 115, PWF 95,
OSF 98, RNF 19. HDF verteilt sich auf Type L/M/H 76/31/8, PWF auf 59/31/5.
TWF-Verschleiß 198–253 min. HDF: ΔT maximal rund 8,6 K und Drehzahl maximal
1.379 rpm. Kein markierter PWF-Fall innerhalb 3.500–9.000 W. Diese nachgezählten
Beobachtungen stützen die visuelle Betrachtung; keine neuen Kausalitätsbehauptungen.

## Tatsächlich geprüfte Bedienung und Reproduzierbarkeit
- `scripts/uv.cmd run --offline --locked python -m unittest discover -s tests -p test_parallel_coordinates.py -v`: **3/3 bestanden**, 7,323 s. Originalwerte/physikalische Formeln, kategoriale Datentypen, vollständige Dimensionen/Type-Farben und echter Jupyter-Dropdown-Callback bei Auswahlwechsel geprüft.
- `scripts/uv.cmd run --offline --locked python scripts/build_exercise_14_4.py --check-html`: **3 Codezellen frisch sequenziell**, keine Zellfehler; selbstständiges Plot-HTML und vollständiger Notebook-HTML-Export.
- Netzwerkgesperrtes Chromium, **900 und 1400 px**: je alle sechs Fehlerflags über das tatsächliche Dropdown gewählt, mit Maus auf 1 gebürstet, gezählte Zeilen/positive Fälle geprüft, zurückgesetzt. HDF-Achse per Maus hinter ΔT gezogen, geänderte Reihenfolge geprüft und erneut 115 HDF ausgewählt. Keine direkten API-Aufrufe als Ersatz für die geprüften Mausaktionen.
- Standalone-Plot ohne Notebook/Python-Server geöffnet. Drehzahlachse per Maus neben ΔT gezogen; HDF und PWF gebürstet. Zwei PNG-Ansichten für direkte Beurteilung; Aktionen/Achsenreihenfolge/Type-Zahlen in interaction_checks.json.
- Offline-Seiten: keine Seitenfehler/fehlgeschlagenen Netzabrufe oder horizontalen **Seiten**überläufe. Die vollständige Grafik nutzt bewusst einen eigenen horizontal scrollbaren Bereich; schmale Ansichten zeigen nicht alle Achsen gleichzeitig.
- Rohdaten-SHA256, **8 Manifesthashes**, **16 tatsächliche Interaktionsprotokolle** und unveränderte 21 Abgabearchive geprüft. Aktuelle CI wird erst nach tatsächlichem Abschluss im bestehenden Draft-PR verlinkt.

Nur erforderliche Abhängigkeiten ergänzt: Plotly 7.1.0 und ipywidgets 8.1.9 mit ihren
Widget-Komponenten, im uv-Lockfile festgehalten. Keine globalen Installationen.

## Bekannte Grenzen und tatsächliche Schwierigkeiten
Der erste vollständige Browserdurchlauf wurde wegen langsamer Software-WebGL-Renderung
abgebrochen. Weniger Maus-Zwischenbewegungen beschleunigen die Prüfung; weder Zeilen
noch fachliche Prüfkriterien wurden reduziert. Die großen Datenmengen und eingebettete
Plotly-Bibliothek machen Dateien/Neudarstellung größer als statische Grafiken.
Brushing wird progressiv gezeichnet; Review-Screenshots lassen eine kurze Renderzeit zu.
Bekannte lokale Jupyter-TCP-Warnung ohne Verschlüsselung, keine Zellfehler. uv meldete
bei Auflösung eine normalisierte ältere Versionsangabe; keine zusätzliche fachliche
Abhängigkeit oder Änderung früherer Ergebnisse daraus.

Im Notebook wird der reale Python-Widget-Callback getestet; ein vollständiger
Jupyter-Frontend-Klicktest wurde nicht zusätzlich durchgeführt. Die eigentlichen
Plotly-Interaktionen wurden im Offline-Browser tatsächlich bedient. Das äußere
Jupyter-Dropdown benötigt einen Kernel und erstellt die Grafik neu (auch Reihenfolge
zurückgesetzt). Die Browserauswahl funktioniert ohne Python, setzt nur Filter zurück
und erhält die Achsenreihenfolge. Der Export ersetzt den Python-Widgetbereich daher
durch die gleichwertige eingebettete Browseransicht, ohne CDN-Abhängigkeit.

Überlagerung, Achsenskalierung/-reihenfolge und Kategoriencodes beeinflussen den
visuellen Eindruck. Auswahlzählungen sind keine Ausfallwahrscheinlichkeiten.
Synthetische Daten, keine Verallgemeinerung auf reale Maschinen, kein Beweis eines
Zufallsmechanismus bei RNF. Frühere Lösungen und Reviews bleiben unverändert.

## Vier Fragen zur studentischen Prüfung
1. Sind alle Messgrößen, Einheiten, Kategorien und die Type-Farblegende verständlich und vollständig?
2. Kannst du mit Fehlertypwahl, Brushing und Achsenumordnung die beschriebenen TWF-/HDF-/PWF-/OSF-Muster nachvollziehen?
3. Ist klar, warum die Auswahlzahlen weder Ausfallwahrscheinlichkeiten noch Kausalitätsbelege sind?
4. Sind Offline-Bedienung, horizontales Scrollen sowie Unterschiede zum Jupyter-Dropdown verständlich und praktikabel?

Kein studentischer Review erfunden. Kein Merge, kein Beginn Kapitel 15, keine Einreichung.
