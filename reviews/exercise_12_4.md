# Aufgabe 12.4 – Human-AI Review

Status: AWAITING HUMAN REVIEW. Kein studentischer Review oder Approval vorliegend.
Technischer Bericht von Codex, 26.10.2026. Kein Merge und keine Einreichung autorisiert.

## Umsetzung und KI-Beitrag
Codex las die offizielle Exercise 12.4, Kurskapitel 9 und Primärquellen zur
Benchmarkfassung. Anforderungen/Konfiguration vor Modelltraining in 4e0f381
festgelegt; KI-gestützte Implementierung 1fb8196. Drei verlangte Regressoren:
DTW-3-NN, aeon TimeSeriesForestRegressor, eigener kompakter PyTorch-CPU-CNN-Regressor.
Kein weiteres Modell und keine Hyperparameterstudie. Bisherige Umgebung unverändert.
95 TRAIN/42 TEST, 24 Kanäle × 144 Werte, unveränderte gehashte Originalsplits.
Nur TRAIN bestimmt Kanalskalierung und CNN-Zielstandardisierung. Keine TEST-Werte
in Fit/Optimierung, keine Neuaufteilung/Imputation/Resampling. CNN-Ausgabe vor
Bewertung rücktransformiert. Benchmark-Split nicht als chronologischer Test behauptet.

## Tatsächliche Ergebnisse (kWh)
| Methode | TEST-RMSE | TEST-MAE |
|---|---:|---:|
| DTW-3-NN | 3,5092246163 | 2,7113492063 |
| Time Series Forest | 2,1091826331 | 1,6852535714 |
| CNN | 3,6146750395 | 2,6080539167 |

Forest auf diesem festen Split bei beiden Maßen niedrigster Fehler. kNN liegt
beim RMSE vor CNN, beim MAE dahinter. Keine allgemeine/signifikante Überlegenheit.
Alle drei Modelle haben null negative Vorhersagen; kein nachträgliches Abschneiden.
CNN: 5.553 Parameter, 60 feste Epochen, Seed 42, Adam 0,001, Batch 16, MSE;
lineare skalare Ausgabe. Forest 200 squared_error-Bäume, 58 Intervallziehungen/Baum,
Mindestlänge 3. kNN uniformes Mittel dreier DTW-Nachbarn, window=0,1.
Diese Ausgangskonfigurationen sind Annahmen, keine durch Tuning belegten Optima.

Ziel laut ursprünglicher TSER-Beschreibung Gesamtenergie in kWh; neue aeon-Dateien
enthalten 137 Fälle, alte Beschreibung nennt 138. UCI-Ursprung mit Wh-Zielen/19.735
Einzelzeilen nicht als identische Darstellung ausgegeben oder nochmals umgerechnet.
Quelle/Lizenz und Grenzen ausführlich in docs/APPLIANCES_SOURCE.md dokumentiert.

## Tatsächlich ausgeführte Prüfungen
Alle Befehle vom Projektstamm über `scripts/uv.cmd run --offline --locked`:
- `python -m unittest discover -s tests -q`: zuletzt 64 Tests bestanden, 6,921 s
  (erster Lauf 7,723 s). Sieben neue Tests für Rohdaten/Formen, instrumentierte
  TRAIN-only-Fit-Grenze, bekannten kNN-Nachbarmittelwert, Forest-Baumaggregation,
  CNN-Seed/echte Gewichtsänderung/lineare Ausgabe/Zielrücktransformation,
  Handrechnung der Metriken und ungültige Daten.
- `python scripts/build_exercise_12_4.py`: frischer Kernel, drei Codezellen sequenziell,
  zwei eingebettete PNGs dekodiert. RMSE/MAE aller Modelle unabhängig mit NumPy
  auf ursprünglichen TEST-Zielen nachgerechnet. Zweiter vollständiger Fit reproduziert
  alle 126 TEST-Vorhersagen innerhalb atol/rtol 1e-10 und alle 60 Verlustwerte.
  Tatsächlicher Skalierer-Aufruf genau einmal mit TRAIN instrumentiert; TRAIN-Kanal-
  und Zielstatistiken separat nachgerechnet. Für alle 42 Fälle kNN-Zielmittel aus
  drei Nachbarindizes und Forest-Mittel aus allen 200 Einzelbäumen überprüft.
  Gespeicherte CNN-NPZ-Gewichte mit allow_pickle=False geladen; alle Vorhersagen
  inklusive Zielrücktransformation bestätigt. Keine Testlabels an predict übergeben.
- `python scripts/check_exercise_12_4_html.py`: HTML offline bei 900/1400 px, zwei
  Bilder geladen, keine Seitenfehler und kein horizontaler Überlauf.
- Beide finalen PNGs visuell geprüft. Achsen/Einheiten/Legenden/Identitätsgeraden
  vollständig, gemeinsame Skalen in allen drei Ist-Vorhersage-Panels. Bildgrenzen
  nach erster Sichtprüfung mit bbox_inches='tight' korrigiert, danach vollständiger
  frischer Build und Offline-Prüfung wiederholt. Keine Ergebnisänderung.
- Beide Originaldateien bei Erstbezug gegen Zenodo-MD5 und bei allen Analyse-Ladevorgängen
  gegen SHA256 geprüft. Elf aktuelle Artefakthashes im Manifest separat bestätigt.
- Frühere wissenschaftliche Dateien, alle bisherigen Reviews und pyproject.toml/
  uv.lock unverändert gegenüber Merge 2e33047; alle acht Kapitel-10/11-ZIPs per
  SHA256 und CRC bestätigt. Keine Rohdaten, Umgebungen oder Binärwerkzeuge committed.

Notebook-Fit-Zeiten: {'DTW 3-NN': 0.027182099991478026, 'Time Series Forest': 7.258757299990975, 'CNN': 4.037345999997342}; Predict: {'DTW 3-NN': 1.030393599998206, 'Time Series Forest': 0.8431469999923138, 'CNN': 0.0030488000047625974} Sekunden.
Separater Audit-Fit: {'DTW 3-NN': 0.027392399992095307, 'Time Series Forest': 9.770668899989687, 'CNN': 4.320078700009617}; Predict: {'DTW 3-NN': 0.9938288999983342, 'Time Series Forest': 0.7240472999983467, 'CNN': 0.005634800007101148} Sekunden.
Zeiten sind Hardware-/Cache-/JIT-abhängig, kein allgemeiner Laufzeitvergleich.
Beobachtet: Jupyter-Warnung zu unverschlüsseltem lokalem TCP-Transport. Keine
fehlgeschlagenen numerischen Tests oder Notebook-/Offline-HTML-Prüfungen.
Aktuelle GitHub-Actions-Läufe werden nach Push tatsächlich im Draft PR dokumentiert;
vor deren Abschluss kein CI-Erfolg behauptet.

## Grenzen und konkrete Fragen für den studentischen Review
Nur 95 Trainingsfälle, ein Seed und vorgegebener Split. Kein unabhängiges
Validierungsset, keine Seed-/Hyperparameterstudie oder Signifikanzprüfung.
Trainingsverlust belegt weder Generalisierung noch allein Overfitting. Schätzung
mit vollständigem Sensorfenster ist keine validierte zukünftige Prognose. Ein Haus
und unbekannte zeitliche Split-Zuordnung begrenzen die Übertragbarkeit; keine Kausalität.

1. Sind TRAIN-only-Kanal- und Zielskalierung sowie die Rücktransformation nachvollziehbar?
2. Sind kNN-Zielmittel, Intervall-Forest und die lineare CNN-Ausgabe verständlich erklärt?
3. Ist die unterschiedliche kNN-/CNN-Reihenfolge für RMSE und MAE sachlich eingeordnet?
4. Sind beide Grafiken lesbar und die kWh-Zielgröße samt 137/138-Quellenabweichung transparent?
5. Sind kleiner Datensatz, ein Seed, fehlende Validierung und keine Zukunftsprognose klar genug?

Studentisches Feedback und Freigabe stehen aus. Status AWAITING HUMAN REVIEW.
Keine weitere Aufgabe beginnen, keine automatische Freigabe/kein Merge/kein Upload.
