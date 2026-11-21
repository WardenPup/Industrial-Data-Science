# Exercise 15.3 – Technischer Bericht für Human Review

**AWAITING HUMAN REVIEW**, 21.11.2026. Keine studentische Bewertung/Freigabe erfunden.
Codex: offizielle Aufgabe gelesen, vorhandene Offline-/Widget-Struktur wiederverwendet,
Code/Notebook erstellt, tatsächliche Interaktionen und technische/visuelle Prüfung.

## Offizielle Anforderungen und Umsetzung
„Visualize failure patterns with plotly“: Parallelkoordinaten, Dropdown-Auswahl nach
Fehlertyp, Brushing für jeden Fehlertyp, ungefähre Schwellen festhalten und neue
Muster/Anomalien dokumentieren. Quelle/Abrufdatum und Abnahmepunkte im Notebook.

Unveränderter XAI-Drilling-Originalbestand und Loader aus 15.1, Merkmalsdefinitionen
und Erkenntnisse aus 15.2, Offline-/Widget-Ansatz aus 14.4. Alle 20.000 Zeilen, sieben
numerische/ordinale Merkmale, Material/Bohrertyp kategorial und das gewählte Flag.
Farbe nach Material. Auswahl bestimmt die Fehlerdimension; Brushing auf 1 filtert
markierte Zeilen, weitere Kategorienfilter sind kombinierbar. Keine Modelle,
Regelfunktionen, Confusion-Matrizen, Optimierung oder 15.4-Arbeit.

## Tatsächlich beobachtete Ergebnisse
BEF/CCF/FWF/WDF: 215/344/278/300 markierte Zeilen. Je vier Fehlertypen tatsächlich
im Browser ausgewählt und gebürstet; **28 Wertebereiche** (vier × sieben Merkmale)
aus der Auswahl ausgelesen und gegen Originaldaten/15.2 geprüft.
- BEF: vc ungefähr 16,3–22,0 m/min, Kühlung 0/25 %. Beobachtete obere Grenzen 22 und 25 sind keine allein hinreichende Regel.
- CCF: vf 62–243 mm/min, Kühlung 0–100 %, daher keine einzelne isolierende Grenze. Keine Mehrfaktorregel validiert.
- FWF in Material N: 270 Fälle, vc 29,08–29,70 m/min, vf 206–250 mm/min. K/P bleiben mit nur 3/5 Fällen vorsichtig interpretiert.
- WDF: Kategorienpaar statt numerischer Schwelle, konsistent mit bekannten Paaren aus 15.2.

Zusätzliche kombinierte Auswahl: FWF=1 + Material N = **270**, dazu Bohrertyp N/H =
**9**. Alle neun tragen auch WDF (und in dieser Auswahl auch CCF). Bei CCF=1 tragen
**106/344** zusätzlich WDF. Das konkretisiert die bekannten Mehrfachlabels; kein
Labelkonflikt oder Kausalitätsnachweis. Keine darüber hinausgehende belastbare neue
Anomalie festgestellt. Keine vorgetäuschte Blindanalyse: Beschreibung bereits bekannt.

## Tatsächlich bestandene Prüfungen
- `scripts/uv.cmd run --offline --locked python -m unittest discover -s tests -p test_interactive_patterns.py -v`: **3/3 bestanden**, 8,107 s. Originalwerte/Kategorien/vollständige Diagrammdimensionen/Farben, Material-/Mehrfachauswahlen und realer Jupyter-Dropdown-Callback.
- `scripts/uv.cmd run --offline --locked python scripts/build_exercise_15_3.py --check-html`: **3 Codezellen frisch sequenziell**, fehlerfrei; Notebook-HTML und direkter Plot eigenständig exportiert.
- Offline-Chromium **900/1400 px**: je alle vier Dropdown-/Maus-Brushing-/Reset-Fälle, tatsächliches Ziehen der Flagachse hinter Kühlung, kombinierte Material-/Bohrertyp-Brushing-Auswahl. Korrekte Zählungen und Übereinstimmung der 28 Grenzen mit Originaldaten. Keine direkten Plotly-API-Aufrufe als Ersatz für geprüfte Mausgesten. Insgesamt **16 Interaktionsprotokolle** einschließlich Standalone-Bedienung ohne Notebook/Python-Server.
- Keine Seitenfehler/fehlgeschlagenen Netzabrufe oder horizontalen Seitenüberläufe. Grafik bewusst in eigenem horizontal scrollbarem Bereich. Beide vollständigen Browseransichten und zwei gebürstete PNGs visuell geprüft (Einheiten, Labels, Kategorien/Farblegende, Auswahlzahlen und Muster).
- Rohdaten-SHA256 und **9 Manifesthashes** bestätigt; **21 Archive**, frühere Daten/Originalreviews/Ergebnisse unverändert. Vorhandene Plotly/ipywidgets und uv-Umgebung genutzt, **keine Installation**. Fokussierte CI-YAML eingelesen; echte aktuelle Head-CI nach Push im Draft-PR dokumentiert.

## Grenzen / vier wissenschaftliche Reviewfragen
20.000 überlagerte Linien und progressive Software-WebGL-Renderung erschweren das
Ablesen; Screenshots lassen kurze Renderzeit zu. Bei schmalem Fenster horizontal
scrollen. Originaleinheiten nur übernommen. Synthetische Daten, überlappende Labels,
sehr kleine Materialgruppen und vorbekannte Beschreibung begrenzen Aussagen.
Minima/Maxima sind Auswahl-/Stichprobengrenzen, keine allgemeingültigen technischen
Schwellen; Auswahlzahlen keine Ausfallwahrscheinlichkeiten. Keine externe Validierung.

Bekannte lokale Jupyter-TCP-Warnung, keine Zellfehler. Jupyter-Callback benötigt
Kernel und erneuert die Grafik; Browser-Dropdown funktioniert ohne Python/Internet
und erhält die Reihenfolge. Kein zusätzlicher vollständiger Jupyter-Frontend-Klicktest
behauptet; echter Callback und tatsächliche Plotly-Browserbedienung geprüft.

1. Kannst du alle vier Fehlertypen durch Auswahl und Brushing nachvollziehbar isolieren?
2. Sind die notierten Bereiche klar von validierten Fehlerregeln oder universellen Schwellen getrennt?
3. Erklärt die kombinierte FWF-/Material-/Bohrertyp-Auswahl die Mehrfachlabels und den Materialeffekt verständlich?
4. Sind Beschriftungen, Offline-Bedienung und vorsichtige Interpretation ausreichend klar für deine fachliche Prüfung?

Kaggle-Registrierung bleibt formal offen. Kein Merge von 15.3, kein Beginn 15.4,
keine Universitätseinreichung. Auf tatsächlichen studentischen Review warten.
