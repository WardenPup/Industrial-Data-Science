# Exercise 16.1 – Technischer Bericht für Human Review

**AWAITING HUMAN REVIEW – 21.11.2026.** Kein studentischer Review/Freigabe erfunden.
Codex: vollständige offizielle Vorlage gelesen; vorhandenes uv/PyTorch genutzt;
Daten geladen, Architektur ergänzt, Notebook/Auswertung/Tests erstellt und geprüft.

## Anforderungen und Umsetzung
Offizielle Aufgabe „Explore the data and train a 1D CNN on the vibration signals“:
Formen/Klassen prüfen; pro Klasse Signal und Wärmebild (gemeinsame Farbskala);
gepaarter stratifizierter 80/20-Split; TRAIN-only-Skalierung; alle Formen; Dropout,
train/eval und Pooling erklären; exakte Tabelle-16.2-Architektur; 30 Epochen mit
vorgegebenem Trainingsrahmen; TEST-Confusion-Matrix und Kreuztabellen mit verborgenem
Vibrationslevel interpretieren. Quellen/Abrufdatum und Kriterien direkt im Notebook.
Gemeinsames Kapitel-16-Notebook enthält ausschließlich 16.1. Offizielle Namen erhalten:
load_multimodal_data, TimeSeriesCNN/features/classifier, train_model, predict_proba,
levels_vs_status und Array-/Tensornamen. Keine ThermalCNN oder Fusion implementiert.

Originales Kurs-JSON (3.511.225 Bytes), SHA256/Herkunft/Lizenz in
`data/raw/MULTIMODAL_SOURCE.md`. 500 × 80 Signale, 500 × 32 × 32 Bilder, 500 Labels,
500 × 2 Diagnoselevels; alle numerischen Werte endlich. Gesundheitsdefinition gegen
alle Levels geprüft. Klassen 240/185/75; TRAIN 192/148/60, TEST 48/37/15.
Ein TRAIN-Mittelwert/eine TRAIN-Standardabweichung je Modalität (ddof=0).
Mittelwerte: Vibration 0,1016439375, Bild 22,671155273437503; Standardabweichungen
1,2208887651397633 und 5,979883910684651. Verborgene Levels nie Modelleingaben.

Exakte CNN-Architektur, 3.843 Parameter; Features (4,32), Logits (4,3).
Adam Standard-lr 0,001, CrossEntropyLoss, Batch 16, 30 Epochen, Seed 42,
CPU/ein Thread, deterministische Algorithmen; Seed direkt vor Modellinitialisierung.
Keine Optimierung, kein zusätzlicher Modellvergleich oder Validierungsdatensatz.

## Ergebnisse
TEST-Accuracy **0,58 (58/100)**. Matrix: Zeilen wahr, Spalten vorhergesagt,
Reihenfolge Normal/Warning/Critical:

| Wahr | Normal | Warning | Critical |
|---|---:|---:|---:|
| Normal | 36 | 12 | 0 |
| Warning | 15 | 22 | 0 |
| Critical | 5 | 10 | 0 |

Keine Critical-Vorhersage; alle 15 Critical-Fälle übersehen. Level 0: 50-mal Normal,
Level 1: 6-mal Normal/23-mal Warning, Level 2: 21-mal Warning. Wahre Klassen je
Level gemischt. Vibration allein fehlt die thermische Information; der Lauf ist für
eine zuverlässige Critical-Erkennung unzureichend. Keine universelle Unmöglichkeit
jeder Critical-Vorhersage behauptet. Erstes TRAIN-Beispiel je Klasse (Indices
203/336/56) bewusst deterministisch, kein statistischer Repräsentativitätsnachweis.
Gemeinsame Wärmebildskala 11,4–68,6 °C; keine Skalierungsinformation daraus genutzt.
Bauteilzuordnung aus Kursbeschreibung, variierende Lage/Last und Überlagerung beachten.

## Tatsächlich bestandene technische Prüfungen
- `scripts/uv.cmd run --offline --locked python -m unittest discover -s tests -p test_multimodal_vibration.py -v`: **3/3 bestanden, 19,693 s**. Originalhash/Formen/Labeldefinition; exakte offizielle Split-Zuordnung, TEST-Perturbation ohne Einfluss auf TRAIN-Skalare und Tensorformen; vollständige Schichtkonfiguration, Shapes, ein Trainingsschritt mit Gewichtsänderung und eval-/Dropout-Modus sowie stabile Wahrscheinlichkeiten.
- `scripts/uv.cmd run --offline --locked python scripts/build_exercise_16_1.py --check-html`: **fünf Codezellen frisch sequenziell**, vollständiges 30-Epochen-Training; nach konkreter Ergebnisinterpretation erneut frisch ausgeführt. Neun numerische CSV/JSON-Exporte bytegleich zwischen beiden Läufen.
- Builder: 100 Original-TEST-Indices/Labels, alle 300 Wahrscheinlichkeiten (endlich, gültiger Bereich, Summe 1), Argmax-Vorhersagen, Confusion-Matrix/Accuracy, TRAIN-Skalare, Klassenhäufigkeiten, Split-CSV und beide Level-Kreuztabellen unabhängig abgeglichen.
- Beide Grafiken und vollständige HTML-Ansichten visuell geprüft. Offline-Chromium 900/1400 px: beide eingebetteten Bilder geladen, keine Seitenfehler/fehlgeschlagenen Abrufe oder Seitenüberläufe; PNGs im Export in Originalauflösung öffnbar.
- Rohdaten-SHA256 und **13 Manifesthashes** geprüft, **21 Abgabearchive unverändert**; frühere wissenschaftliche Dateien/Reviews nicht geändert. Vorhandene PyTorch 2.9.1+cpu/uv-Umgebung; keine neuen Abhängigkeiten. CI auf 16.1 begrenzt und YAML gelesen, aktuelle Push-/PR-CI im Draft-PR nach Abschluss dokumentieren.
- Lokale Jupyter-TCP-Warnung ohne Ausführungsfehler. Bei erster reiner Datensichtung enthielt das JSON zusätzlich beschreibende Zeichenketten; Endlichkeitsprüfung danach korrekt ausschließlich auf vier numerische Arrays angewendet. Kein Datensatz- oder Trainingsergebnis geändert.

## Wissenschaftliche Grenzen und vier Reviewfragen
Synthetische Daten, 500 Beobachtungen, ein fester Split und ein Seed; kein Nachweis
realer Übertragbarkeit oder externer Validierung. Kein Overfitting-Nachweis ohne
Validierungsdaten. Numerische Reproduzierbarkeit auf dieser CPU-Umgebung geprüft,
keine plattformübergreifende Bitgleichheit versprochen. Vibrationseinheit/Abtastrate
nicht vorgegeben; deshalb keine erfundenen physikalischen Achseneinheiten.

1. Sind CNN, Dropout, train/eval und die beiden Pooling-Arten verständlich erklärt?
2. Sind Wärmebildbeispiele mit gemeinsamer Skala und Bauteilzuordnung vorsichtig genug interpretiert?
3. Erklären Confusion-Matrix und Level-Kreuztabellen nachvollziehbar, warum alle Critical-Fälle übersehen werden und Vibration allein begrenzt ist?
4. Sind Split-/TRAIN-only-Vorverarbeitung und wissenschaftliche Grenzen ausreichend klar?

Kein Merge von 16.1, keine Bearbeitung von 16.2–16.4 und keine Universitätseinreichung.


## Studentischer Originalreview – 21.11.2026

HUMAN REVIEW – EXERCISE 16.1

Status: SCIENTIFICALLY APPROVED

1. Methoden

Das 1D-CNN entspricht der offiziellen Architektur. Faltung, Max Pooling, Average Pooling und Dropout sind verständlich und fachlich korrekt erklärt.

Die Funktionen model.train() und model.eval() werden korrekt eingesetzt.

Bewertung: BESTANDEN.

2. Datenvisualisierung

Die Vibrationssignale und Wärmebilder sind nachvollziehbar dargestellt. Die gemeinsame Temperaturskala ermöglicht einen direkten Vergleich.

Die Interpretation berücksichtigt, dass einzelne Beispiele keine zuverlässige Klassentrennung beweisen.

Bewertung: BESTANDEN.

3. Modellergebnisse

Die TEST-Accuracy beträgt 0,58 (58 von 100 richtig).

Das Modell erkennt keinen der 15 Critical-Fälle.

Die Confusion-Matrix und die Kreuztabellen mit dem verborgenen Vibrationslevel machen die begrenzte Aussagekraft der Vibrationsdaten nachvollziehbar.

Es wird nicht behauptet, dass Critical grundsätzlich nicht anhand von Vibration erkannt werden kann.

Bewertung: BESTANDEN.

4. Wissenschaftliche Grenzen

Der stratifizierte 80/20-Split, die TRAIN-only-Standardisierung und die getrennte Behandlung verborgener Zustandsstufen sind korrekt.

Synthetische Daten, kleine Teststichprobe und fehlende externe Validierung werden angemessen berücksichtigt.

Bewertung: BESTANDEN.

GESAMTENTSCHEIDUNG:
SCIENTIFICALLY APPROVED.

Zusätzlicher Human Review:
Die 100 exportierten Einzelvorhersagen, die Confusion-Matrix und zwölf hochgeladene Artefaktprüfsummen wurden kontrolliert.

Die vollständige Notebook- und Browserausführung wurde im Human Review nicht unabhängig wiederholt.

Die schlechte Critical-Erkennung bleibt als relevantes Ergebnis dokumentiert. Keine nachträgliche Modelloptimierung erforderlich.

Keine Universitätseinreichung.
