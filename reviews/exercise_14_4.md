> Stand 21.11.2026: **SCIENTIFICALLY APPROVED – TECHNICALLY VALIDATED – AWAITING FINAL MERGE AUTHORIZATION**.
> Erstbericht, Originalreview und folgende Codex-Verifikation sind getrennt dokumentiert.

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


---

## Studentischer Human Review – Originalwortlaut, übergeben am 21.11.2026

Die interaktive Parallelkoordinatenvisualisierung erfüllt die fachlichen Ziele von Exercise 14.4.

Die acht kontinuierlichen Merkmale, kategorialen Fehlerflags und die Typklassifizierung sind verständlich dargestellt.

Die HDF- und PWF-Auswahlen sind plausibel und stimmen mit den dokumentierten Ergebnissen überein.

Bestätigte Ergebnisse:

- 10.000 Datensätze.
- HDF: 115 markierte Fälle.
- PWF: 95 markierte Fälle.
- TWF: 46 markierte Fälle.
- HDF: Temperaturdifferenz maximal 8,6 K und Drehzahl maximal 1.379 rpm.
- PWF: Keine markierten Fälle innerhalb 3.500–9.000 W.

Brushing, Achsenumordnung und Dropdown-Auswahl sind nachvollziehbar dokumentiert.

Die Darstellung enthält bei 10.000 Linien unvermeidbare Überlagerungen. Brushing reduziert diese Einschränkung.

Die Ergebnisse beschreiben Muster synthetischer Daten. Sie beweisen keine kausalen Zusammenhänge und liefern keine Ausfallwahrscheinlichkeiten.

Es besteht kein wissenschaftlicher Änderungsbedarf.

Gesamturteil: SCIENTIFICALLY APPROVED.


---

## Codex-Abschlussverifikation – 21.11.2026

Studentischer Originalreview aus dem Nutzerauftrag wortgetreu separat in **72eac4f**
gesichert. Keine zusätzlichen studentischen Tests, Aussagen oder Merge-Freigaben
erfunden. Offizielle Aufgabe 14.4 am 21.11.2026 erneut direkt per HTTPS gelesen und
alle Anforderungen gegen Implementierung/Prüfroutinen abgeglichen.

Tatsächlich erneut ausgeführt:
- `scripts/uv.cmd run --offline --locked python -m unittest discover -s tests -p test_parallel_coordinates.py -v`: **3/3 bestanden**, 8,206 s (zuvor 7,323 s). Originalwerte/Featureformeln, alle Dimensionen/Kategorien/Type-Farben und realer Jupyter-Dropdown-Callback geprüft.
- `scripts/uv.cmd run --offline --locked python scripts/build_exercise_14_4.py --check-html`: **3 Codezellen frisch sequenziell**, fehlerfrei. Notebook-HTML offline **900/1400 px**, alle sechs Dropdown-/Maus-Brushing-/Reset-Fälle und Achsenumordnung bestanden; Standalone ohne Notebook/Python-Server geprüft. **16 Interaktionsprotokolle**; keine fehlgeschlagenen Netzabrufe/Seitenfehler oder horizontalen Seitenüberläufe. Zwei PNGs und beide Browseransichten visuell kontrolliert.
- Separater direkter Vergleich Original-CSV/Diagramm/CSV/JSON: 10.000 Zeilen, Zählungen Machine failure/TWF/HDF/PWF/OSF/RNF = **339/46/115/95/98/19**. Alle acht kontinuierlichen Diagrammdimensionen stimmen mit Originalmesswerten bzw. festen physikalischen Ableitungen überein. HDF maximal rund **8,6 K** (Gleitkommawert 8,599999999999966), **1.379 rpm**; kein markierter PWF innerhalb **3.500–9.000 W**.
- Bestehende **8 Manifesthashes vor Regeneration** bestätigt; danach sämtliche acht aktuellen Hashes und Rohdaten-SHA256 geprüft. Wissenschaftliche CSV, JSON und Standalone-Plot-HTML sind **bytegleich mit 908bb68**. 21 Abgabearchive unverändert, frühere Aufgaben/Originalreviews nicht geändert.

Keine wissenschaftlichen Abweichungen oder Korrekturen erforderlich. Nur Status-/
Prüfdokumentation und frische Exporte aktualisiert; irreführenden kopierten Builder-
Docstring (HDF/PWF) auf Parallelkoordinaten präzisiert. Kein neuer Test, keine
Zusatzanalyse oder Installation. Bekannte lokale Jupyter-TCP-Warnung erneut ohne
Ausführungsfehler. Lokaler Windows-Prozessstart erforderte wegen eines Zugriffsfehlers
einen erneuten Start; die fachlichen Prüfungen selbst liefen danach erfolgreich.

Bekannte Grenzen bleiben bestehen: Überlagerung/progressives WebGL-Rendering,
horizontaler Grafik-Scrollbereich bei schmalem Fenster, synthetische Daten ohne
Kausalitäts- oder Wahrscheinlichkeitsnachweis. Der Jupyter-Callback benötigt einen
Kernel und baut neu auf; die geprüfte Browserauswahl funktioniert offline und erhält
die Reihenfolge. Kein zusätzlicher vollständiger Jupyter-Frontend-Klicktest behauptet.

Aktuelle CI-/Review-/Konfliktprüfung wird nach Push am tatsächlichen Head im PR #17
belegt. Ready erst nach Erfolg beider Läufe und fehlenden Reviewblockern.
**Kein Merge, keine Arbeit an 15.1, keine Universitätseinreichung.**
