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


## Studentischer Originalreview – 21.11.2026

HUMAN REVIEW – EXERCISE 16.3

Status: SCIENTIFICALLY APPROVED

1. Early und Late Fusion

Early Fusion kombiniert standardisierte Vibrationssignale und Wärmebilder vor der Klassifikation in einem zweikanaligen CNN.

Die 80 Vibrationswerte werden mit 944 Nullen auf 1.024 Werte erweitert und anschließend als Bildkanal verarbeitet.

Die künstliche räumliche Anordnung ist eine methodische Einschränkung, die korrekt dokumentiert wurde.

Late Fusion kombiniert die Wahrscheinlichkeitsvektoren der beiden bestehenden Einzelmodelle durch ungewichtete Mittelung. Es wurde kein zusätzliches Modell trainiert.

Bewertung: BESTANDEN.

2. Vergleichbarkeit

Alle vier Modelle wurden anhand derselben 100 TEST-Beobachtungen, derselben Klassenreihenfolge und desselben aktuellen Laufs verglichen.

Die historischen Ergebnisse von 16.1 und 16.2 wurden nicht als unabhängige Vergleichsläufe vermischt.

Bewertung: BESTANDEN.

3. Modellergebnisse und Critical-Erkennung

Die lokalen TEST-Ergebnisse sind:

Vibration: Accuracy 0,58; Critical 0/15.\
Thermal: Accuracy 0,72; Critical 10/15.\
Early Fusion: Accuracy 0,91; Critical 13/15.\
Late Fusion: Accuracy 0,79; Critical 9/15.

Early Fusion erreicht die höchste beobachtete Accuracy und erkennt die meisten Critical-Fälle.

Zwei Critical-Fälle bleiben jedoch übersehen. Zusätzlich werden vier Warning-Fälle als Critical klassifiziert.

Late Fusion verbessert die Gesamtaccuracy gegenüber den Einzelmodellen, erkennt aber einen Critical-Fall weniger als Thermal allein.

Die Unterschiede zwischen Accuracy und Critical-Erkennung sind korrekt interpretiert.

Bewertung: BESTANDEN.

4. Wissenschaftliche Grenzen

Der Datensatz ist synthetisch und umfasst nur 500 Beobachtungen. Die Auswertung basiert auf einem festen TRAIN-/TEST-Split.

Die Modellkapazitäten unterscheiden sich, weshalb die beobachteten Leistungsunterschiede nicht ausschließlich dem Fusionsverfahren zugeschrieben werden dürfen.

Early Fusion verwendet eine künstliche zweidimensionale Anordnung der Vibrationswerte.

Late Fusion lernt keine zusätzlichen gemeinsamen Merkmale und kann Fehler der Einzelmodelle übernehmen.

Die dokumentierten Plattformabweichungen werden transparent behandelt. Keine allgemeingültige Rangfolge oder statistische Signifikanz wird behauptet.

Bewertung: BESTANDEN.

GESAMTENTSCHEIDUNG:\
SCIENTIFICALLY APPROVED.

Zusätzliche Human-Review-Prüfung:

- Alle vier Confusion-Matrizen unabhängig nachgerechnet.
- 100 eindeutige TEST-Indizes bestätigt.
- 400 Klassenvorhersagen mit ihren exportierten Wahrscheinlichkeiten abgeglichen.
- Late-Fusion-Mittelung rechnerisch geprüft.
- Sechs hochgeladene Ergebnisartefakte stimmen mit den Manifestprüfsummen überein.
- GitHub-PR und erfolgreicher PR-CI-Lauf geprüft.

Die vollständige Notebook- und Browserausführung wurde im Human Review nicht unabhängig wiederholt.

Keine zusätzlichen Modelloptimierungen erforderlich.\
Keine Universitätseinreichung.


## Codex-Abschlussverifikation nach Human Review – 21.11.2026

**SCIENTIFICALLY APPROVED.** Originalreview wortgetreu separat in 6753432;
ursprünglicher technischer Bericht und gesamte Reviewhistorie unverändert erhalten.
Finale Merge-Autorisierung weiterhin ausstehend.

Tatsächlich erneut ausgeführt: zwei vorhandene Fusionstests bestanden (0,021 s),
ohne Testtraining. Direkter Datenabgleich in bestehender uv-Umgebung bestätigt:
100 eindeutige originale TEST-Indizes/Labels, 400 Klassenvorhersagen und 1.200
gültige Wahrscheinlichkeiten/Argmax; vier Confusion-Matrizen mit 36 Werten und
alle Vergleichstabellenwerte (58/72/91/79 korrekt, Critical 0/10/13/9 von 15).
Early-Tensoren für 400 TRAIN/100 TEST geprüft: Bildkanal unverändert, alle 80
standardisierten Signalwerte in richtiger Reihenfolge, 944 Nullen je Signal.
Late-Mittelung unabhängig rechnerisch geprüft; Split und TRAIN-Skalare unverändert.

Sieben Manifesthashes (sechs Ergebnisartefakte plus gemeinsames Notebook) und
Rohdaten-SHA256 geprüft; freigegebener 16.1/16.2-Zellblock inklusive Outputs und
Metadaten exakt gegen Merge 5b78a82 erhalten. Zwanzig frühere Ergebnisartefakte und
21 Abgabearchive unverändert. Keine Änderung an Notebook, HTML, Code, lokalen
Vorhersagen oder Ergebnistabellen durch diesen Nachtrag. Keine zusätzlichen lokalen
Trainingsläufe. Vorhandene Belege für zwei unabhängige frische Elf-Zellen-Läufe,
exakte Wiederholbarkeit innerhalb der Umgebung und visuelle/Offline-HTML-Prüfung
900/1400 px erhalten; aktuelle konfigurierte Head-CI nach Push vollständig prüfen.

Plattformvariation bleibt ausdrücklich dokumentiert: lokaler Early/Late-Vergleich
0,91/0,79; beobachtete frühere CI-Läufe Early 0,90 und Late 0,78 bzw. 0,80.
Keine plattformübergreifende Gleichheit, wissenschaftliche Überlegenheit oder
zusätzliche studentische Notebook-/Browserausführung erfunden.

Kommentare, Reviewthreads und Konfliktfreiheit nach erfolgreicher aktueller Push-/
PR-CI prüfen. Erst danach Ready for Review; tatsächlicher Abschlussstatus und Links
im PR-Bericht. Kein Merge von PR #24, keine Umsetzung von 16.4 oder Einreichung.
