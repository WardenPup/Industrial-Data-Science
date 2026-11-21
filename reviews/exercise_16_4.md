# Exercise 16.4 – Technischer Bericht für Human Review

**AWAITING HUMAN REVIEW – 21.11.2026.** Keine studentische Freigabe erfunden.
Codex: offizielle Vorgaben gelesen, Klasse/Notebook ergänzt, Tests, Ausführung,
Zahlen-/Grafik-/Offline-Prüfung. Bestehende uv-/PyTorch-Umgebung, keine neuen Pakete.

## Anforderungen und Methode
Offiziell „Build and train the multimodal network“: frische Bild-/Vibrationsfeatures,
96er Konkatenation und gemeinsamer Kopf; end-to-end 60 Epochen; fünf Matrizen
nebeneinander, Accuracyvergleich und tatsächliche Rangfolge diskutieren. Nutzer
fordert zusätzlich korrekte und übersehene Critical-Fälle. Quelle/Kriterien im Notebook.

MultimodalNet: ThermalCNN().features (64), TimeSeriesCNN().features (32), torch.cat
(dim=1), Linear(96,32)+ReLU+Dropout(0,3)+Linear(32,3). **142.883 Parameter**.
Keine trainierten Einzelmodellgewichte übernommen; Zweige und Kopf werden gemeinsam
optimiert. Shapes (4,64)/(4,32)/(4,96)/(4,3) bestätigt. Unveränderter gepaarter Split
400/100 und TRAIN-only-Modalskalare. TensorDataset(img_train_tensor,
ts_train_tensor,y_train_tensor), Adam lr 0,001, CrossEntropyLoss, Batch 16,
60 Epochen, Seed 42, ein CPU-Thread. Keine Diagnoselevels als Inputs, keine Optimierung.

## Tatsächlicher lokaler Fünfmodellvergleich desselben Laufs
| Modell | Accuracy | Korrekt/100 | Critical erkannt/15 | Critical übersehen |
|---|---:|---:|---:|---:|
| Vibration | 0,58 | 58 | 0 | 15 |
| Thermal | 0,72 | 72 | 10 | 5 |
| Early | 0,91 | 91 | 13 | 2 |
| Late | 0,79 | 79 | 9 | 6 |
| Intermediate | 0,93 | 93 | 13 | 2 |

Intermediate-Matrix: [[48,0,0],[3,32,2],[0,2,13]], Zeilen wahr/Spalten vorhergesagt,
Normal/Warning/Critical. Alle 48 Normal-Fälle korrekt, 32/37 Warning und 13/15
Critical. Drei Warning→Normal, zwei Warning→Critical und zwei Critical→Warning.
Intermediate hier tatsächlich höchste Accuracy; gleich viele Critical-Treffer wie
Early, aber weniger falsche Critical-Alarme (2 statt 4). Keine allgemeine Rangfolge
oder isolierter kausaler Fusionsvorteil behauptet. Alle fünf aktuellen Matrizen und
Metriken im neuen Abschnitt; historische frühere Ausgaben nicht als Vergleich vermischt.

## Tatsächlich ausgeführte technische Prüfung
- `scripts/uv.cmd run --offline --locked python -m unittest discover -s tests -p test_intermediate_fusion.py -v`: **2/2 bestanden, 2,802 s**. Zweige unter festem Seed exakt frischen Referenzarchitekturen entsprechend und ohne geteilte Parameter; Kopf/Shapes/Parameterzahl; ein Trainingsdurchlauf mit Gradienten und Gewichtsänderung in beiden Zweigen sowie Kopf, eval-Modus und stabile Wahrscheinlichkeiten. Der gezielte Trainingscheck nutzt eine Epoche auf 16 TRAIN-Paaren, keine zusätzliche Modellstudie.
- `scripts/uv.cmd run --offline --locked python scripts/build_exercise_16_4.py --check-html`: **14 Zellen zweimal unabhängig frisch sequenziell**; drei vorherige CNNs je 30 Epochen, Intermediate 60 Epochen. Alle fünf Vorhersage-/Wahrscheinlichkeitsreihen innerhalb derselben Umgebung exakt identisch. Late ohne neues Modelltraining.
- Builder: 100 TEST-Indizes/Labels, 500 Klassenvorhersagen/1.500 Wahrscheinlichkeiten, Argmax und Mittelung, alle 45 Matrixwerte und fünf Metrikzeilen unabhängig geprüft; aktuelle Einzel-/Early-/Late-Probs gegen die jeweiligen frischen Vorstufen abgeglichen. TRAIN-Skalare, Klassenreihenfolge, Shapes und Konfiguration bestätigt. Übersehene Critical-Fälle zusätzlich aus allen Matrizen nachgerechnet.
- Gesamtes Notebook in temporärem Arbeitsordner ausgeführt; genehmigter 16.1–16.3-Zellblock einschließlich Text/Code/Outputs/Metadaten exakt erhalten. 26 frühere Ergebnisartefakte und historische Manifeste unverändert; neuer Gesamtnotebookhash für absichtliche Erweiterung plus Hash des eingefrorenen Blocks.
- Fünfmatrixgrafik und HTML bei **900/1400 px visuell geprüft**, linkes und rechtes Ende der horizontalen Matrixzeile kontrolliert. Alle fünf eingebetteten Grafiken geladen; keine Seitenfehler/fehlgeschlagenen Abrufe/Seitenüberläufe. Matrizengrafik im eigenen scrollbaren Bereich, PNG in Originalauflösung verlinkt.
- Konkrete lokale Interpretation/Parameterzahl danach nur im Markdown ergänzt; HTML erneut exportiert und offline geprüft, ohne unnötiges zusätzliches Training. Finale Quelle in aktueller CI ausführen.
- Rohdaten-SHA256, **sieben Manifesthashes** und **21 unveränderte Archive** bestätigt. Bestehende PyTorch 2.9.1+cpu/uv-Umgebung. Bekannte lokale Jupyter-TCP-Warnung ohne Ausführungsfehler. Keine plattformübergreifende Bitgleichheit verlangt; Unterschiede zum gespeicherten Plattformstand sichtbar protokolliert.
- Aktuelle Push-/PR-CI nach Push vollständig abwarten, Ergebnisse/Links im Draft-PR dokumentieren.

## Grenzen und vier Fragen für den Human Review
Kleine synthetische Stichprobe, ein Split/Seed, bekannte Plattformvariation. Exakte
Wiederholbarkeit nur innerhalb derselben Umgebung geprüft. Unterschiedliche Kapazität
und 60 statt 30 Epochen erlauben keine Zuschreibung der Unterschiede allein zum
Fusionsverfahren. Einzelmodelle sehen nur einen Teil der Zustandsinformation; Late
lernt keine gemeinsamen Merkmale, Early hat künstliche räumliche Signalnachbarschaft.
Intermediate kann passende Zweigmerkmale gemeinsam anpassen, garantiert aber keine
universelle Überlegenheit, externe Validierung oder Sicherheitseignung. Keine
statistische Signifikanz oder TEST-basierte Optimierung behauptet.

1. Sind frische Featurezweige, 96er Konkatenation und gemeinsames end-to-end-Training verständlich erklärt?
2. Ist klar, dass alle fünf Modelle im neuen Vergleich aus demselben aktuellen Lauf stammen?
3. Sind 13/15 Critical-Treffer, zwei übersehene Fälle und zwei falsche Critical-Alarme angemessen interpretiert?
4. Ist die eingeschränkte Aussagekraft der Rangfolge durch Kapazität, Trainingsdauer und Plattformvariation ausreichend deutlich?

Kein Merge von 16.4, keine weiteren Exercises und keine Universitätseinreichung.


## Tatsächlicher CI-Befund: Gleichstand statt allgemeinem Vorsprung

Head ced5d88: Push 44916904691 und PR 44916981444 erfolgreich. Jeweils zwei
unabhängige frische vollständige Vierzehn-Zellen-Läufe mit exakt identischen
Vorhersagen/Wahrscheinlichkeiten innerhalb des Runners; Offline-HTML bestanden.
Beide CI-Runner: Vibration 0,58, Thermal 0,70, Early 0,90, Late 0,80,
Intermediate 0,90. Intermediate liegt dort gleichauf mit Early, nicht eindeutig davor.
Zum gespeicherten 16.1-Lauf null abweichende Klassen, maximale Wahrscheinlichkeits-
abweichung ca. 1,5e-7. Lokal bleibt der beobachtete Vergleich 0,58/0,72/0,91/0,79/0,93.

Dieser tatsächliche Unterschied ist als Grenze in Notebook/HTML ergänzt. Kein
Vorsprung erzwungen, kein Ergebnis ausgetauscht und keine zusätzliche Optimierung.
Keine geplante Mehrfachlauf-/Seedstudie oder Unsicherheitsschätzung behauptet.
Nur Markdown/HTML ergänzt und offline erneut geprüft, kein weiteres lokales Training.
Die dokumentierten lokalen Matrizen und frühere freigegebene Abschnitte bleiben
unverändert. Aktuelle CI nach diesem reinen Dokumentationscommit erneut prüfen.
