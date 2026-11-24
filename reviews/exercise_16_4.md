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


## Studentischer Originalreview – 21.11.2026

HUMAN REVIEW – EXERCISE 16.4

Status: SCIENTIFICALLY APPROVED

1. Intermediate Fusion

Die beiden Feature Extractors für Vibrationssignale und Wärmebilder werden frisch initialisiert. Sie erzeugen 32 beziehungsweise 64 Merkmale.

Die 96 Merkmale werden korrekt zusammengeführt und durch einen gemeinsamen Klassifikationskopf verarbeitet.

Das gesamte Modell wird gemeinsam über 60 Epochen trainiert. Es werden keine bereits trainierten Einzelmodellgewichte übernommen.

Bewertung: BESTANDEN.

2. Vergleichbarkeit

Die fünf Modelle werden anhand derselben 100 TEST-Beobachtungen aus einem gemeinsamen aktuellen Lauf verglichen.

Die historischen Ausgaben vorheriger Exercises werden nicht als unabhängige Vergleichsläufe vermischt.

Die Confusion-Matrizen und Kennzahlen sind konsistent.

Bewertung: BESTANDEN.

3. Modellergebnisse und Critical-Erkennung

Lokale TEST-Ergebnisse:

- Vibration: 58 % Accuracy, Critical 0/15
- Thermal: 72 % Accuracy, Critical 10/15
- Early Fusion: 91 % Accuracy, Critical 13/15
- Late Fusion: 79 % Accuracy, Critical 9/15
- Intermediate Fusion: 93 % Accuracy, Critical 13/15

Intermediate Fusion erreicht lokal die höchste Accuracy.

Von 15 Critical-Fällen werden 13 richtig erkannt. Zwei werden als Warning klassifiziert.

Gegenüber Early Fusion erkennt Intermediate keine zusätzlichen Critical-Fälle, reduziert aber die falschen Critical-Alarme von vier auf zwei.

Die Unterscheidung zwischen Gesamtaccuracy und Critical-Erkennung ist wissenschaftlich korrekt.

Bewertung: BESTANDEN.

4. Wissenschaftliche Grenzen

Der synthetische Datensatz, der einzelne TRAIN-/TEST-Split und die kleine Zahl kritischer Testfälle begrenzen die Aussagekraft.

Intermediate Fusion unterscheidet sich von den anderen Modellen in Architektur, Parameterzahl und Trainingsdauer. Die höhere lokale Accuracy darf deshalb nicht ausschließlich dem Fusionsverfahren zugeschrieben werden.

Die bekannten Plattformabweichungen werden transparent behandelt. Auf mindestens einem CI-Runner besteht Gleichstand zwischen Early und Intermediate Fusion.

Eine allgemeine Überlegenheit oder Sicherheitseignung für reale industrielle Anlagen wird nicht behauptet.

Bewertung: BESTANDEN.

GESAMTENTSCHEIDUNG:
SCIENTIFICALLY APPROVED.

Zusätzliche Human-Review-Prüfung:

- Alle fünf Confusion-Matrizen unabhängig aus 100 Einzelvorhersagen rekonstruiert.
- 500 Klassenvorhersagen und 1.500 exportierte Wahrscheinlichkeiten auf Konsistenz geprüft.
- Accuracy, Critical-Treffer und übersehene Critical-Fälle nachgerechnet.
- Late-Fusion-Wahrscheinlichkeitsmittelung bestätigt.
- Fünf hochgeladene Ergebnisdateien stimmen bytegenau mit den Manifestprüfsummen überein.
- Die hochgeladene PNG hat einen abweichenden Datei-Hash; die Originaldatei ist technisch erneut abzugleichen.
- GitHub-PR und erfolgreiche PR-CI geprüft.

Die vollständige Notebook- und Browserausführung wurde im Human Review nicht unabhängig wiederholt.

Keine zusätzlichen Modelloptimierungen erforderlich.
Keine Universitätseinreichung.


## Codex-Abschlussverifikation nach Human Review – 21.11.2026

**SCIENTIFICALLY APPROVED.** Originalreview wortgetreu separat in 22c1945 erhalten;
gesamter bisheriger technischer Bericht und frühere Reviews unverändert. Finale
Merge-Autorisierung fehlt.

### Original-PNG und berichtete Uploadabweichung
`outputs/ch16/exercise_16_4/01_five_confusion_matrices.png`: 139.153 Bytes,
3759 × 797 Pixel, PNG-Struktur erfolgreich geprüft. Lokale Originaldatei,
Git-Datei aus geprüftem Head 612e71e und tatsächlich über GitHub-Contents-API geladene
Datei sind **bytegenau identisch**. Alle drei stimmen mit dem Manifest überein:
`065f9a0f4a94d97d181d425f02e343b3f2ac6688a01fa2889369ce23d5a10dde`.

Der aktuelle Anhang enthält ausschließlich den Reviewtext, keine abweichende
Uploadkopie oder deren Hash. Daher ist die Ursache des berichteten anderen Upload-
Hashes **nicht festgestellt**; insbesondere keine Upload-Umwandlung ohne Beleg
behauptet. Der studentische Befund bleibt unverändert oben dokumentiert. An der
maßgeblichen Originaldatei wurde keine Hashabweichung gefunden; nichts ersetzt
oder neu gerendert.

### Tatsächliche technische Nachprüfung
Zwei vorhandene Tests erneut bestanden (13,931 s): frische Referenzinitialisierungen,
getrennte Parameter, exakte Architektur/Shapes/142.883 Parameter, gemeinsamer
Gradientenfluss und Gewichtsänderung in beiden Zweigen/Kopf, eval-Modus und stabile
Wahrscheinlichkeiten. Der vorhandene Funktionstest nutzt einen Batch mit 16 TRAIN-
Paaren/einer Epoche; keine zusätzlichen vollständigen 60-Epochen-Läufe durchgeführt.

Sieben Original-Manifesthashes (sechs Ergebnisartefakte plus Notebook), Rohdaten,
100 eindeutige TEST-Indizes/Labels, 500 Klassenvorhersagen und 1.500 Wahrscheinlichkeiten/
Argmax erneut abgeglichen. Fünf Matrizen mit 45 Zählwerten, Accuracy und Critical-
Treffer/-Fehler unabhängig nachgerechnet: korrekt 58/72/91/79/93, Critical 0/10/13/9/13;
Intermediate zwei übersehen und zwei falsche Critical-Alarme. Late-Mittelung,
TRAIN-only-Skalare und unveränderter Split bestätigt. Freigegebener 16.1–16.3-
Zellblock einschließlich Outputs/Metadaten exakt gegen Merge 3a6cc20, 26 frühere
Ergebnisartefakte und 21 Abgabearchive unverändert. Keine Änderungen an Modellen,
Notebook, HTML, Original-PNG oder numerischen Ergebnissen durch den Nachtrag.

Vorhandene Belege für zwei unabhängige frische Vierzehn-Zellen-Läufe und die visuelle/
Offline-HTML-Prüfung 900/1400 px erhalten; aktuelle konfigurierte Head-CI nach Push
vollständig abwarten. Plattformvariation/Gleichstand mit Early bleibt unverändert
sichtbar, keine plattformübergreifende Gleichheit behauptet. Keine zusätzliche
studentische Notebook-/Browserausführung erfunden.

Nach erfolgreicher aktueller Push-/PR-CI Konflikte und Kommentare/Reviewthreads prüfen;
erst danach Ready for Review, tatsächliche Links und Abschlussstatus im PR-Bericht.
PR #25 nicht mergen. Keine weitere Exercise und keine Universitätseinreichung.
