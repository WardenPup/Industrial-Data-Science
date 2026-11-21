# Nächste Self-Study-Aufgaben

Stand/Abruf: **19.11.2026**. Status: **14.1 APPROVED und integriert; 14.2 APPROVED und integriert; 14.3 APPROVED und integriert; 14.4 APPROVED und integriert; 15.1 wissenschaftlich freigegeben und integriert, Registrierung offen; 15.2 APPROVED und integriert; 15.3 AWAITING HUMAN REVIEW; übrige Übungen nur geplant**.
Codex: Quellenprüfung, Anforderungsübersicht und Workflowvorschlag. Keine neuen
studentischen Prüfungen oder Freigaben behauptet; bisherige Lösungen bleiben erhalten.

## Quellen und Umfang

Der [offizielle Kursindex](https://noxthot.github.io/ws26_industrial_datascience_manuscript/)
und alle sechs folgenden Self-Study-Seiten wurden vollständig per HTTPS gelesen.
Das Webwerkzeug konnte sie nicht öffnen; der direkte HTTPS-Abruf funktionierte.
Ergebnis: **20 Übungen in Kapitel 14–16 und 22–23, zusätzlich 27.1 ausdrücklich optional**.
Kapitel 13 sowie 17–21 und 24–26 nicht als weitere Self-Study-Aufgaben erfinden.

| Kürzel | Offizielle Aufgabenquelle | Daten / fachliche Voraussetzung |
|---|---|---|
| S14 | [Kapitel 14](https://noxthot.github.io/ws26_industrial_datascience_manuscript/2_act2/1_self_study_session1.html) | AI4I 2020, vollständige 14-Spalten-CSV; [Kapitel 13](https://noxthot.github.io/ws26_industrial_datascience_manuscript/2_act2/0_0_predictive_maintenance.html), insbesondere 13.1.6–13.1.7 |
| S15 | [Kapitel 15](https://noxthot.github.io/ws26_industrial_datascience_manuscript/2_act2/2_self_study_session2.html) | [Explainable AI (XAI) Drilling Dataset](https://www.kaggle.com/datasets/raphaelwallsberger/xai-drilling-dataset/); Kaggle-Registrierung/Download gemäß Aufgabe; Konzepte aus Kapitel 13 |
| S16 | [Kapitel 16](https://noxthot.github.io/ws26_industrial_datascience_manuscript/2_act2/3_self_study_session3.html) | [Kurs-JSON](https://noxthot.github.io/ws26_industrial_datascience_manuscript/data/assets/act2/selfstudysessions/sss3_multimodal.json): 500 synthetische Fälle, Vibration mit 80 Werten, Wärmebilder 32 × 32, drei Zustandsklassen; kein Drilling-Datensatz |
| S22 | [Kapitel 22](https://noxthot.github.io/ws26_industrial_datascience_manuscript/3_act3/5_self_study_session1.html) | [Kapitel 20](https://noxthot.github.io/ws26_industrial_datascience_manuscript/3_act3/3_0_process_optimization_sensor_data.html): simulated_machine_data.csv und simulated_inspection_data.csv aus [Knifes-Simulator v1.0.4](https://github.com/noxthot/industrial_datascience_sim_machine_knifes/tree/v1.0.4), später eigene Simulations-CSV |
| S23 | [Kapitel 23](https://noxthot.github.io/ws26_industrial_datascience_manuscript/3_act3/6_self_study_session2.html) | [Kapitel 21](https://noxthot.github.io/ws26_industrial_datascience_manuscript/3_act3/4_0_live_feedback.html): simulated_opcua_machinedata.csv und simulated_opcua_postinspection.csv, über cycle verknüpft; [Live-Simulator v1.1.1](https://github.com/noxthot/industrial_datascience_live_machine/tree/v1.1.1) |
| S27 | [Kapitel 27, optional](https://noxthot.github.io/ws26_industrial_datascience_manuscript/4_act4/3_self_study_session.html) | Literatur: [Klaeger, Gottschall und Oehm (2021)](https://doi.org/10.3390/challe12010002); kein Rechendatensatz |

Die Kontextabschnitte aus Kapitel 13, 20 und 21 wurden für die Planung ebenfalls
nachgelesen. Daten und Simulatoren wurden nicht heruntergeladen oder ausgeführt.
Komplexität unten ist eine Codex-Einschätzung, keine offizielle Einstufung/Zeitgarantie.

## Anforderungen pro Übung

Englische Titel sind unverändert aus der jeweiligen Aufgabenüberschrift übernommen.
Jede Checkbox bleibt offen, bis die betreffende Anforderung tatsächlich erfüllt ist.
Notebook/HTML sind unser Abgabestandard, keine zusätzlich behauptete Dateivorgabe
der Kursseiten. Pflichtartefakte wie Screenshots und Skripte sind separat genannt.

### Kapitel 14 – S14, Daten: AI4I 2020

**14.1 — Tool wear failure — APPROVED, PR #14 integriert — low**
- [x] Die TWF-Beschreibung in 13.1.7 mit den Befunden aus 13.1.6.1/13.1.6.2 vergleichen und den konkreten Widerspruch belegen. Ergebnis: kurze begründete Gegenüberstellung; keine neue Modellstudie verlangt. Voraussetzung: diese Kursbefunde lesen, keine vorangehende neue Übung nötig.

**14.2 — Overstrain failure — APPROVED, PR #15 integriert — medium**
- [x] OSF-Zusammenhang Torque × Tool wear und Type-abhängige Grenzen 11.000/12.000/13.000 min·Nm visualisieren.
- [x] Bäume der Tiefen 1/2/4/8 ausschließlich auf Torque und Tool wear fitten; Grenzen mit `DecisionBoundaryDisplay` und der 11.000-Hyperbel vergleichen. Anschließend Kursbaum um `wearadjTorque` und Type ergänzen; Struktur, kleinste nahezu trennende Tiefe und gelernte Grenze berichten. Voraussetzung: Kursbaum 13.1.6.2, nicht das Ergebnis von 14.1.

**14.3 — Engineered features and model performance — APPROVED, PR #16 integriert — medium**
- [x] Tiefenvergleich für HDF/PWF mit und ohne `temp_diff` beziehungsweise `power`; F1 statt Accuracy auswerten und Klassenungleichgewicht erklären. Ergebnis: kompakter Leistungsvergleich; Vorgehen aus 14.2 wiederverwenden, Featuredefinitionen aus Kapitel 13 prüfen.

**14.4 — Parallel coordinates plots — APPROVED, PR #17 integriert — medium**
- [x] Plotly-Parallelkoordinaten: alle verfügbaren kontinuierlichen Variablen, gewählter Fehlertyp und Type; Fehlertyp kategorial, Linienfarbe nach Type. Jupyter-Dropdown zur Fehlertypwahl; Achsen umordnen und Brushing tatsächlich nutzen, erkannte Muster dokumentieren. Voraussetzung: AI4I/Kapitel-13-Muster; 14.1–14.3 liefern Vergleich, sind keine neue Datenquelle.

### Kapitel 15 – S15, Daten: XAI Drilling

**15.1 — Register and download the dataset — SCIENTIFICALLY APPROVED, integriert; Registrierung offen — low**
- [ ] Kaggle registrieren/Zugang klären, Beschreibung lesen, Daten laden; Form, Typen, Probleme, Ziele und Klassenhäufigkeiten prüfen. Hauptflag gegen Vereinigung der Untergruppen sowie Mehrfachfehler prüfen und Umgang erläutern. Ergebnis: Daten-/Labelprüfung technisch durchgeführt (20.000 × 15, 0 Labelwidersprüche, 114 Mehrfachfehler). **Registrierung bleibt offen: Student hat noch kein Konto.** Öffentlicher Download möglich; keine Zugangsdaten im Repository.

**15.2 — Explore the dataset — APPROVED, PR #19 integriert — medium**
- [x] Nach 15.1 Merkmale je Fehlertyp statistisch und mit mindestens zwei geeigneten Grafiken untersuchen; Befunde/Schwellen notieren und mit „Subgroup failures“ vergleichen. Bereits gelesene Beschreibung nicht als ungelesen ausgeben; explorative Betrachtung und anschließenden Vergleich transparent trennen.

**15.3 — Visualize failure patterns with plotly — APPROVED / INTEGRIERT — medium**
- [x] Auf Daten aus 15.1 aufbauen: Parallelkoordinaten, Dropdown nach Fehlertyp, Brushing je Fehlertyp; ungefähre Schwellen und neue Muster/Anomalien festhalten. Ergebnis: interaktive Darstellung mit kurzen Befunden, Schwellen für 15.4; 15.2 als Vergleich.

**15.4 — From exploration to a rule-based failure model — APPROVED — medium**
- [x] Schwellen aus 15.2 und/oder 15.3 in je eine Python-Regelfunktion pro Fehlertyp übersetzen; je Confusion-Matrix berechnen. Flachen Baum pro Fehlertyp fitten, mit Regeln vergleichen und Erklärbarkeit für Prozessingenieure diskutieren. Abhängigkeit: 15.1 und die tatsächlich ermittelten Schwellen.

### Kapitel 16 – S16, Daten: multimodales Kurs-JSON

**Verbindliche Ausnahme:** ein gemeinsames Notebook für **16.1–16.4**, mit getrennten
Exercise-Überschriften, vorgegebenen Codeframe-Namen und wiederverwendeten Funktionen.
Übungen trotzdem nacheinander bearbeiten/reviewen; frühere freigegebene Abschnitte bewahren.
Gemeinsamer Rahmen: 80/20-Split, `random_state=42`, stratifiziert; gepaarte Modalitäten
zusammen halten, Skalierung nur auf TRAIN. Versteckte Levels ausschließlich zur
Diagnose, niemals als Input. Kursrahmen: Adam/Kreuzentropie, Batch 16, Seed dokumentieren.

**16.1 — Explore the data and train a 1D CNN on the vibration signals — APPROVED / INTEGRIERT — medium**
- [x] Shapes/Klassenverteilung und pro Zustand Signal + Wärmebild mit gemeinsamer Farbskala zeigen; vorbereitete Array-/Tensorformen prüfen. Dropout, train/eval sowie Average-/Max-Pooling erklären.
- [x] `TimeSeriesCNN` nach Tabelle 16.2 vervollständigen (32 Features, drei Logits), 30 Epochen; TEST-Confusion-Matrix und Kreuztabellen mit verstecktem Vibrationslevel interpretieren. Erste Stufe, keine Abhängigkeit von Drilling-Ergebnissen.

**16.2 — Build and train the image network — AWAITING HUMAN REVIEW — medium**
- [x] `ThermalCNN` gemäß Tabelle 16.3 (64 Features, drei Logits), Shapes prüfen, 30 Epochen; TEST-Confusion-Matrix und thermische Level vergleichen. Grenzen einer einzelnen Modalität erläutern. Nutzt Datenaufbereitung und Trainingsrahmen aus 16.1.

**16.3 — Combine the raw inputs, combine the predictions — medium**
- [ ] Early Fusion: 80 standardisierte Signalwerte auf 1.024 auffüllen, 32 × 32 formen, als zweiten Bildkanal stapeln; zweikanalige `ThermalCNN`, 30 Epochen. Late Fusion: Klassenwahrscheinlichkeiten aus 16.1/16.2 mitteln. Beide Confusion-Matrizen, Viermodellvergleich und Grenzen der Fusion erläutern. Benötigt beide unimodalen Modelle.

**16.4 — Build and train the multimodal network — high**
- [ ] Frische untrainierte Featurezweige aus 16.1/16.2 end-to-end verbinden: 64 + 32 Features, gemeinsamer Kopf 96→32→3 mit ReLU/Dropout 0,3; 60 Epochen. Fünf Confusion-Matrizen nebeneinander und Accuracyübersicht; tatsächlich gemessene Rangfolge und Grenzen erklären, keine universelle Rangfolge versprechen. Benötigt 16.1–16.3.

### Kapitel 22 – S22, Daten: Knifes-Simulator

**22.1 — Investigating the blow-out step — high**
- [ ] Druck beim Ausblasen (`process_step_index=2`, nullbasiert) der **vorherigen** Iteration dem aktuellen NOK_4-Befund zuordnen; Zusammenhang untersuchen. Ergebnis: nachvollziehbare zeitliche Zuordnung und geeignete Auswertung/Grafik. Voraussetzung: Daten-/Prozessverständnis aus Kapitel 20.

**22.2 — Fine-tuning the machine parameters — high**
- [ ] Simulator-README lesen; Parameter zur Fehlerreduktion variieren, Nachtschicht und `NUM_PIECES=5000` beibehalten. Neue CSVs untersuchen und mit Originalverteilung vergleichen (OK/NOK_1/2/3/4: 4631/84/1/4/280). Konfigurationen und tatsächlich gemessene Ergebnisse protokollieren; kein Fehlerfreiheitsversprechen. Baut auf Kapitel 20 und 22.1 auf.

**22.3 — Try the machine on day shift — medium**
- [ ] Die Parameter aus 22.2 mit 5.000 Teilen auf Tagschicht anwenden; mit Nacht vergleichen und Unterschiede anhand der CSVs untersuchen. Ergebnis: Schichtvergleich mit belegter Ursachenanalyse, keine bloße Vermutung als Nachweis.

**22.4 — Fine-tune the parameters to work well for both shifts — high**
- [ ] Auf 22.2/22.3 aufbauen; Parameterkompromiss für beide Schichten, Fehlerzahl und Produktionsdauer suchen, immer 5.000 Teile. Temperatur-/Geschwindigkeits-/Druckbeziehungen berücksichtigen; Qualität und Dauer gemeinsam dokumentieren. Kein globales Optimum ohne Nachweis behaupten.

### Kapitel 23 – S23, Daten: Pick-and-place / OPC UA

**23.1 — Train a model to predict placement error — high**
- [ ] Daten aus Kapitel 21 auf TRAIN/TEST, gegebenenfalls Validierung teilen; `error_x`/`error_y` aus rechtzeitig verfügbaren Merkmalen der Zeilen `Process step=1` vorhersagen. TEST-Metriken (z. B. MAE), Fehler-/Residuenvisualisierung; Modell und gegebenenfalls Skalierer speichern. Voraussetzung: Kapitel-21-Daten, noch kein Livebetrieb.

**23.2 — First encounter with the live machine simulator — medium**
- [ ] Server starten; Ausgabe der ersten fünf Zyklen sichern. OPC-UA-Client verbinden (`opc.tcp://localhost:4840`); Screenshots von Variablenbaum, position_x-Attributen, Subscriptions (position_x/position_y/cycle), error_x/error_y-Graph liefern.
- [ ] Korrekturwert schreiben und Wirkung im Graph sowie Serverlog festhalten (zwei weitere Screenshots). Graph-Polling 1 s von Subscriptions unterscheiden. Simulator-README erforderlich; Modell aus 23.1 wird hier noch nicht verwendet.

**23.3 — Set up an OPC UA client in Python — medium**
- [ ] Vorgegebenes `opc-ua-client.py` (`main`, `SubHandler`) kurz erklären und am laufenden Simulator ausführen; echten Screenshot empfangener Änderungen sichern. Benötigt Server-/Variablenverständnis aus 23.2.

**23.4 — Integrate the trained model into the live feedback system — high**
- [ ] Die zehn markierten Client-Teile ergänzen: Modell/Skalierer laden, identische Featurefolge, Skalierung/Prediction/Korrektur, Rückschreiben und Aktivierung; Benachrichtigungs-Logspam entfernen. Tatsächlichen Livebetrieb prüfen.
- [ ] Screenshots der gesendeten Korrekturen, Serverwirkung und eines Graphen **vor/nach** Zuschalten der Rückkopplung sichern. Benötigt gespeichertes Modell aus 23.1 und Client/Server aus 23.2/23.3. Client-/Serverskripte gehören zusätzlich zum Notebook zur Lösung.

### Kapitel 27 – S27, optional

**27.1 — Data Science on Industrial Data – Today’s Challenges in Brown Field Applications — medium**
- [ ] Klaeger et al. (2021) kritisch lesen; Datenfluss Maschine→Speicher, Brownfield-Hürden, Ground Truth, Maschinenlebenszyklen und Datenvorbereitungsaufwand diskutieren. Ergebnis: kurze nachvollziehbare Literaturdiskussion; kein Modell/Datensatz verlangt. Als reine Leseaufgabe genügt ein kompakter Text statt eines künstlichen Implementierungsnotebooks; keine Verlagsbewertung ungeprüft übernehmen.

## Reihenfolge und wissenschaftliche Leitplanken

Empfehlung: **14.1 → 14.2 → 14.3 → 14.4 → 15.1–15.4 → 16.1–16.4 →
22.1–22.4 → 23.1–23.4 → optional 27.1**. Vor Kapitel 22/23 die referenzierten
Kapitel 20/21 verstehen; daraus keine zusätzlichen erfundenen Self-Study-Aufgaben machen.
Kapitel 16 ist datenseitig unabhängig von 15; 27.1 kann separat gelesen werden.

Zusätzliche methodische Absicherung, nicht als wörtliche Kursanforderung ausgeben:
bei Modell-/Schwellenwahl TEST zurückhalten, Vorverarbeitung nur auf TRAIN fitten;
bei Zyklusdaten ganze Zyklen zusammen und sinnvolle zeitliche Reihenfolge erhalten.
UDI ist kein gesicherter Zeitstempel. Deskriptive Regelrekonstruktion und unabhängige
Generalisation getrennt ausweisen. Wiederholte Simulatorläufe sind stochastisch;
beobachtete Korrelation nicht automatisch als kausalen Beweis behandeln.
Es gibt keine hier zugesagten Modellgüten oder selbst erfundenen Sollmetriken.

## Wiederverwendung statt Neuaufbau

| Vorhanden | Sinnvolle Nutzung / Grenze |
|---|---|
| `pyproject.toml`, `uv.lock`, `.venv`, `scripts/uv.cmd` | Python 3.12.15, NumPy/pandas/Matplotlib/Seaborn, scikit-learn 1.9.1, PyTorch 2.9.1+cpu und Notebookwerkzeuge vorhanden; keine neue Umgebung für 14–16 ohne Bedarf |
| `scripts/download_ai4i.py`, `sessions/ch10/ai4i_data.py` | Download und SHA256-Prüfung wiederverwenden. **`load_ai4i()` liefert nur vier Spalten**; für 14 die unveränderte Roh-CSV vollständig in einem neuen aufgabenspezifischen Loader lesen, alte Funktion nicht umschreiben |
| `sessions/ch10/ai4i_eda.py`, `sessions/ch11/*_plots.py` | Stil, Einheiten, getrennte Rechnung/Darstellung und transparente Fehlstellenbehandlung übernehmen; keine alten Ergebniszahlen ungeprüft übertragen |
| `sessions/ch12/classification.py`, `regression.py` | TRAIN-only-Prinzip, Seed-/CNN-/Metrikmuster als Referenz; deren Sensor-Skalierer oder Netze **nicht** blind für tabellarische Daten/Bilder einsetzen. Kapitel 16 nutzt seinen offiziellen Rahmen |
| `tests/` | `unittest`, kleine analytische Fälle, Hash-/Schema-, Leakage-, Shape- und Metriktests als Muster; künftig gezielt betroffene Tests statt jedes Mal alle alten Notebooktrainings |
| `scripts/build_exercise_12_4.py`, `templates/notebook_export.html.j2` | Frischer `NotebookClient`, sequenzielle Zellen, `HTMLExporter`, eingebettete Bilder; nur kleinen benötigten Teil übernehmen, keine 12.4-spezifischen Voll-Doppelfits kopieren |
| `scripts/execute_submission_notebook.py`, `check_exercise_12_4_html.py` | Einzelnotebook-Ausführung bzw. Offline-Browserprüfung als Muster. `validate_notebooks.py` führt dagegen **alle** getrackten Notebooks aus und ist für die schlanke Einzelprüfung nicht der Standard |
| `.github/workflows/quality.yml` | Vorhandene gesperrte Installation, Tests, Commitprüfung, PR-Checks; derzeit globale Tests plus mehrere vollständige Notebookläufe. Vorschlag: künftig gezielte neue Jobs/Pfadfilter, ohne Altprüfungen still abzuschalten; heute nichts geändert |
| `reviews/TEMPLATE.md` | Auf einen knappen aufgabenspezifischen Review reduzieren: Ergebnis, tatsächliche Checks, Grenzen, 2–3 Fachfragen, echte studentische Entscheidung; Originalwortlaut erhalten |

Seit 14.4 im Lockfile vorhanden: **Plotly/ipywidgets** (für 15.3 wiederverwendet). Noch fehlend: OPC-UA-/GUI-Pakete
wie **opcua-client/pyqtgraph** und gegebenenfalls **asyncua** (erst konkretes Simulator-
README prüfen). Nur bei Bedarf per uv ergänzen. Interaktive Dropdowns müssen im
Notebook funktionieren; ein statischer nbconvert-Export garantiert das nicht.
Für offline lesbares HTML nötige Plotly-Assets und eine verständliche statische
Ansicht oder tatsächlich eigenständige Browser-Interaktion vorsehen und prüfen.
Kein zusätzlicher PDF-Export ohne Pflicht. Bei mehreren Abgabedateien weiterhin ZIP;
zu jedem abgegebenen Notebook sein HTML, gemäß vorhandener Projekt-Abgaberegel.

Kapitel 23 empfiehlt für den GUI-Weg Python **3.13**; das bestehende Projekt verlangt
`>=3.12,<3.13`. Deshalb dort früh Kompatibilität prüfen und nötigenfalls eine separate
uv-Umgebung für Simulator/GUI vorsehen, statt die freigegebene Umgebung zu ersetzen.
Keine zusätzlichen Pakete, Accounts oder Simulatorprozesse wurden jetzt angelegt.

## Vorgeschlagener schlanker Standardablauf

1. **Eine Übung / ein Branch:** Quelle kurz prüfen, wenige Abnahmepunkte direkt im
   Notebook; `exercise/<Nummer>`. Kein zusätzlicher Anforderungsbericht pro Übung nötig.
2. **Eine kompakte Lösung:** Ziel, Methode/Annahmen, Code, nötige Grafiken/Tabellen,
   Interpretation/Grenzen auf verständlichem Deutsch; offizielle Ausnahmen oben beachten.
3. **Ein technischer Durchlauf:** betroffene Tests, frischer Kernel, sequenzielle
   Ausführung, rechnerische Plausibilitäts-/Datenprüfung, HTML und visuelle Kontrolle.
   Nur bei Änderung/Fehler wiederholen; Befehle, Warnungen und Grenzen knapp protokollieren.
4. **Transparenter Git-Stand:** sinnvolle echte Commits mit KI-Offenlegung; keine
   künstlichen Phasen-/Leercommits. Nach autorisiertem Push ein Draft-PR, relevante CI.
5. **Ein kurzer Human Review:** tatsächliches studentisches Feedback unverändert
   sichern; nur echte Korrekturen durchführen und betroffene Prüfungen wiederholen.
6. **Freigabegate:** `AWAITING HUMAN REVIEW` bis zur studentischen Entscheidung;
   technische Erfolge ersetzen sie nicht. Merge erst nach ausdrücklicher Autorisierung.

Der Nutzer hat den **vereinfachten Ablauf für 14.1 ausdrücklich beauftragt**,
einschließlich gemeinsamer Anforderungen/Implementierung und separater Validierung.
Diese aktuellen Vorgaben gelten für 14.1; AGENTS.md und die frühere Historie bleiben
erhalten. Die CI wurde für 14.1 gezielt begrenzt; Integrität, Originalreviews und
das ausdrückliche Mergegate bleiben bestehen.
Ursprüngliche Planung ohne Implementierung; seit dem ausdrücklichen Folgeauftrag
ist 14.1 technisch bearbeitet. Kein Modelltraining, Simulatorstart, Universitätseinreichen
oder studentische Übungsfreigabe erfolgt.

**Aktuelles Gate: Human Review für Exercise 14.1 – Tool wear failure. 14.2 bleibt unbegonnen.**
