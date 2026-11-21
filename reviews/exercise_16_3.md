# Exercise 16.3 – Technischer Prüfbericht und Human Review

**AWAITING HUMAN REVIEW – 21.11.2026.** Keine studentische Bewertung/Freigabe erfunden.
Codex: offizielle Vorlage gelesen, vorgegebene Fusion ergänzt, Tests/Ausführung,
Zahlen-/Grafik-/Offline-Prüfung. Vorhandene uv-/PyTorch-Umgebung, keine neuen Pakete.

## Anforderungen und Umsetzung
Offiziell „Combine the raw inputs, combine the predictions“, Milestone 3:
Early Fusion mit vorgegebenem as_image_channel, zweikanaliger ThermalCNN und 30
Epochen; Late Fusion als einfaches Wahrscheinlichkeitsmittel; TEST-Matrizen und
Viermodellvergleich. Nutzerergänzung: Tabelle mit Accuracy, korrekter Anzahl und
richtig erkannten Critical-Fällen. Quellen/Abrufdatum/Kriterien im Notebook.
Keine Fusion-Optimierung, keine Architekturstudie, keine Umsetzung von 16.4.

80 TRAIN-standardisierte Vibrationswerte + 944 Nullen → 32×32; Kanal 0 Wärmebild,
Kanal 1 Vibration. TRAIN (400,2,32,32), TEST (100,2,32,32); ThermalCNN(in_channels=2),
136.275 Parameter. Adam lr 0,001, CrossEntropyLoss, Batch 16, 30 Epochen, Seed 42,
ein CPU-Thread. Bestehender gepaarter Split und TRAIN-Modalskalare unverändert,
keine Diagnoselevels als Input. Late: (ts_test_probs+img_test_probs)/2, dann Argmax;
kein neues Training, Gewichtstuning oder Kalibrierung.

Alle vier Vergleichsmodelle stammen aus derselben aktuellen Ausführung und
denselben TEST-Indizes/Klassenreihenfolge. Alte gespeicherte Ausgaben sind historische
Referenzen, keine Eingaben für Late oder den neuen Vergleich.

## Tatsächlicher lokaler Vergleich
| Modell | Accuracy | Korrekt / 100 | Critical erkannt / 15 |
|---|---:|---:|---:|
| Vibration | 0,58 | 58 | 0 |
| Thermal | 0,72 | 72 | 10 |
| Early | 0,91 | 91 | 13 |
| Late | 0,79 | 79 | 9 |

Early-Matrix: [[48,0,0],[3,30,4],[0,2,13]]. Late-Matrix:
[[44,4,0],[8,26,3],[0,6,9]]. Zeilen wahr, Spalten vorhergesagt,
Reihenfolge Normal/Warning/Critical. Alle vier Matrizen in einer beschrifteten
Vergleichsgrafik und als CSV. Early führt hier, aber zwei Critical-Fälle bleiben
übersehen. Late insgesamt besser als beide Einzelmodelle, jedoch ein Critical-Treffer
weniger als Thermal; eine Kombination hilft nicht jeder Klasse gleichermaßen.
Keine allgemeine Rangfolge, statistische Signifikanz oder Kausalität behauptet.

## Tatsächlich ausgeführte technische Prüfung
- `scripts/uv.cmd run --offline --locked python -m unittest discover -s tests -p test_fusion.py -v`: **2/2 bestanden, 0,174 s**. Alle 80 Werte je Zeile und 944 Paddingnullen erhalten, Kanalreihenfolge/Stichprobenordnung, zweikanaliger Netzinput/Shapes/Parameterzahl; exakte ungewichtete Mittelung/Argmax, ungültige Formen/Wahrscheinlichkeiten abgewiesen. Kein zusätzliches Testtraining.
- `scripts/uv.cmd run --offline --locked python scripts/build_exercise_16_3.py --check-html`: **elf Zellen zweimal unabhängig frisch sequenziell**, drei CNNs je 30 Epochen; Late ohne neues Modell. Sämtliche vier Vorhersagen einschließlich Wahrscheinlichkeiten in beiden Läufen exakt identisch innerhalb dieser Umgebung.
- Builder: 100 Original-TEST-Indizes/Labels, 400 Modellvorhersagen/1.200 Wahrscheinlichkeiten, vier Matrizen (36 Werte), alle vier Tabellenzeilen/Accuracy/Critical-Treffer, korrekte Late-Mittelung, TRAIN-Skalare und Early-Konfiguration unabhängig nachgerechnet. Vibration/Thermal-Probs zusätzlich mit den jeweiligen frischen Vorstufen-CSV-Dateien aus demselben Lauf abgeglichen.
- Gesamtes Notebook unverändert im temporären Arbeitsordner ausgeführt; nur neue 16.3-Artefakte übernommen. Gesamter freigegebener 16.1/16.2-Zellblock inklusive Text/Code/Outputs/Metadaten exakt erhalten, ebenso zwanzig frühere Ergebnisartefakte und beide historischen Manifeste. Der alte Gesamtnotebookhash gehört zur früheren Version; neuer Gesamthash plus eingefrorener Zellblockhash sichern die Erweiterung ab.
- Viermodellgrafik und HTML bei **900/1400 px visuell geprüft**; vier eingebettete Grafiken geladen, keine Seitenfehler/fehlgeschlagenen Abrufe/Seitenüberläufe. Originalauflösung der PNGs im Export zugänglich.
- Konkrete lokale Interpretation anschließend nur im Markdown ergänzt; bedeutungslose write_text-Zählerausgabe durch Zuweisung unterdrückt. HTML erneut exportiert/offline geprüft, ohne unnötige weitere Trainingsläufe; finale Quelle wird zusätzlich in CI ausgeführt. Keine wissenschaftlichen Ergebnisse verändert.
- Rohdaten-SHA256 und **sieben Manifesthashes** bestätigt; **21 Abgabearchive** unverändert. Lokale Jupyter-TCP-Warnung ohne Zellfehler. Keine plattformübergreifende Gleichheit verlangt; ursprüngliche Klassen-/Wahrscheinlichkeitsabweichungen der Vorstufe werden protokolliert, nicht in alte Artefakte zurückgeschrieben.
- Aktuelle Push-/PR-CI nach Push vollständig abwarten und tatsächliche Ergebnisse im Draft-PR verlinken.

## Wissenschaftliche Grenzen und vier Reviewfragen
Kleine synthetische Stichprobe, ein fester Split und Seed, bekannte numerische
Plattformvariation. Nur Wiederholbarkeit innerhalb derselben Umgebung geprüft.
Unterschiedliche Modellkapazitäten verhindern die Deutung als isolierter Effekt
allein des Fusionsprinzips. Early nutzt künstliche 2D-Nachbarschaften und viel
Padding; Late lernt keine neuen modalitätsübergreifenden Merkmale und übernimmt
auch Unsicherheiten der Einzelmodelle. Keine externe Validierung oder nachträgliche
TEST-Optimierung. Beobachtete Verwechslungen bleiben offen dokumentiert.

1. Sind Early und Late Fusion sowie das künstliche Padding/Bildformat nachvollziehbar erklärt?
2. Ist klar, dass der Viermodellvergleich nur Vorhersagen desselben aktuellen Laufs verwendet?
3. Sind die 13/15 bzw. 9/15 Critical-Treffer und die Grenzen einer höheren Gesamtaccuracy verständlich interpretiert?
4. Sind Modellkapazität, Plattformvariation und fehlende allgemeine Übertragbarkeit ausreichend berücksichtigt?

Kein Merge von 16.3, keine Umsetzung von 16.4 und keine Universitätseinreichung.
