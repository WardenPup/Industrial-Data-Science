# Aufgabe 12.3 – Anforderungen und Vorgehen

Quelle: https://noxthot.github.io/ws26_industrial_datascience_manuscript/1_act1/8_self_study_session3.html
Gelesen am 26.10.2026, Exercise 12.3 „Classification using aeon's Time Series Forest Classifier“.
Offizielle Pflichten: UWaveGestureLibrary laden; aeon TimeSeriesForestClassifier
anwenden; prüfen, ob bessere Ergebnisse als mit den vorigen Algorithmen erzielt werden.
Keine bestimmte Erfolgsquote oder konkrete Metrik wird vorgeschrieben. Accuracy ist
Hauptvergleich, Balanced Accuracy und Macro-F1 ergänzen wie in 12.2 den Klassenvergleich.

Kursmaterial: Kapitel 8, insbesondere 8.1 Time Series Forests:
https://noxthot.github.io/ws26_industrial_datascience_manuscript/1_act1/4_1_timeseries_classification.html
API: https://www.aeon-toolkit.org/en/stable/api_reference/auto_generated/aeon.classification.interval_based.TimeSeriesForestClassifier.html
Zusätzlich installierten aeon-1.6.0-Quelltext geprüft (BaseIntervalForest, RandomIntervals).
Ziel: zufällige Zeitintervalle als statistische Merkmale verstehen, Forest trainieren
und den begrenzten TEST-Vergleich sachlich einordnen. Kein gewöhnlicher Forest auf
flach aneinandergereihten Rohwerten und keine Distanzmetrik als Forest-Eingabe.

## Vor dem Training festgelegte Umsetzung
- Dieselben vollständigen Originalsplits wie 12.2: 120 TRAIN/320 TEST, 3 × 315,
  acht Klassen. Quelle und SHA256 aus sessions/ch12/uwave_source.json und
  docs/UWAVE_SOURCE.md wiederverwenden. Originaldateien nicht verändern.
- Gemeinsame nur auf TRAIN geschätzte Kanalskalierung aus 12.2 wiederverwenden.
  Bäume benötigen keine Standardisierung; gleiche Eingabebedingungen halten den
  Vergleich nachvollziehbar. Kein Resampling, keine Imputation (nur endliche Werte).
- aeon TimeSeriesForestClassifier: 200 Bäume, n_intervals='sqrt', minimale Länge 3,
  keine Zeitlimitsteuerung, random_state=42, n_jobs=1, übrige Defaults. Kein Tuning.
  aeon multivariat berechnet int(sqrt(315)*sqrt(3))=30 Intervallziehungen je Baum
  (Duplikate können entfallen), nicht 17 je Kanal. Tatsächliche Counts protokollieren.
- Mittelwert, Standardabweichung (ddof=0), lineare Steigung je gezogenem Kanalintervall;
  Entropie-Entscheidungsbäume, Mittelung der Klassenwahrscheinlichkeiten.
  Keine Bootstrap-Stichproben der Trainingsfälle in diesem regulären aeon-fit.
- Vergleich ausschließlich mit unveränderten freigegebenen 12.2-Vorhersagen;
  deren Zuordnung zum identischen TEST-Split und Hashes prüfen. TEST erst nach Fit
  bewerten. Bekannte 12.2-Ergebnisse motivieren keine nachträgliche Parameterauswahl.
- Zwei kompakte Abbildungen: TRAIN-Intervallbeispiel mit Merkmalen; Forest-Confusion-
  Matrix und Accuracy/Macro-F1-Vergleich. Tabellen mit Klassenbericht, Einzelvorhersagen,
  Wahrscheinlichkeiten und gepaarten Erfolgs-/Fehlfällen. Kein Hypothesentest gefordert.
- Keine neuen Abhängigkeiten; projektlokales uv, bestehendes aeon/scikit-learn.

## Akzeptanz und spätere Abgabe
Notebook sessions/ch12/uwave_forest.ipynb mit Ziel, mathematischer Idee, Umsetzung,
Ergebnissen, Grenzen und Lernfragen auf Deutsch; HTML unter outputs/ch12/exercise_12_3.
CSV/JSON, zwei lesbare PNGs, reproduzierbare Modellkonfiguration und SHA256-Manifest.
Für eine spätere Ein-Datei-Abgabe ZIP mit Notebook + HTML, relevanten Modulen,
Datenquelle/Downloadhinweis und pyproject.toml/uv.lock; keine PDF-Pflicht. Jetzt keine
Abgabe oder Änderung bestehender Pakete. Projekt-Abgaberegeln bleiben maßgeblich.

Automatisierte Tests: TRAIN/TEST-Grenze, Merkmalsformeln gegen aeon, Seed-Reproduktion,
Wahrscheinlichkeiten/Aggregation, ungültige Werte und Metrik-Handrechnung. Frischer
Kernel mit sequenziellen Codezellen; alle TEST-Zeilen/Metriken unabhängig nachrechnen,
Forest erneut fitten, Grafiken visuell und HTML offline bei 900/1400 px prüfen.
Rohdaten-, Referenz- und Artefakthashes kontrollieren; echte Befehle/Resultate berichten.

## Wissenschaftliche Grenzen und Review-Gate
Ein Seed, nur 120 Trainingsfälle, ein bereits bekannter TEST-Split, kein separates
Validierungsset oder Hyperparameter-/Unsicherheitsvergleich. Keine allgemeine oder
signifikante Überlegenheit aus einem Lauf ableiten. Kein nachgewiesener Personensplit,
keine physikalischen Einheiten/Lizenz erfinden; Katalogabweichung bleibt dokumentiert.
Intervallstatistiken reduzieren Details, Forest richtet Muster nicht wie DTW elastisch
aus. Gemittelte Blattwahrscheinlichkeiten sind keine geprüfte Kalibrierung.
Nach technischer Prüfung: AWAITING HUMAN REVIEW – NOT MERGED. Keine 12.4/Einreichung.
KI-Unterstützung: Codex; keine studentische Freigabe für 12.3 vorliegend.
