# Exercise 16.2 – Technischer Bericht und Human Review

**AWAITING HUMAN REVIEW – 21.11.2026.** Kein studentischer Review/Freigabe erfunden.
Codex: genaue offizielle Vorlage gelesen, Architektur ergänzt, gemeinsame Ausführung,
Tests, Export und tatsächliche numerische/visuelle Prüfung. Keine neuen Abhängigkeiten.

## Anforderungen und Methode
„Build and train the image network“: ThermalCNN gemäß Tabelle 16.3, Shapes prüfen,
30 Epochen, TEST-Confusion-Matrix, Thermal-Level gegen wahren/vorhergesagten Status;
Grenzen einer einzigen Modalität erklären. Quelle/Kriterien im gemeinsamen Notebook.
Nur 16.2 angehängt, keine Fusion und keine Umsetzung von 16.3/16.4.

Conv2d(1,16,3,same)+ReLU+MaxPool2d(2), Conv2d(16,32,3,same)+ReLU+MaxPool2d(2),
Flatten, Linear(2048,64)+ReLU+Dropout(0,3), Linear(64,3); **136.131 Parameter**.
`in_channels=1` wie vorgegeben; Features (4,64), Logits (4,3). Unveränderte 400/100-
Zuordnung und TRAIN-Modalskalare aus 16.1. Nur standardisierte Bilder als Inputs,
Labels als Trainingsziel; keine Diagnoselevels. Unveränderte train_model/predict_proba:
Adam lr=0,001, CrossEntropyLoss, 30 Epochen, Batch 16, Seed 42, ein CPU-Thread.
Keine Optimierung oder Modellwahl anhand TEST.

## Tatsächliche Ergebnisse
**72/100 korrekt, Accuracy 0,72**; 16.1 bleibt bei 58/100. Nur derselbe feste Split,
keine statistische Signifikanz oder allgemeine Überlegenheit behauptet.
Zeilen wahr, Spalten vorhergesagt:

| | Normal | Warning | Critical |
|---|---:|---:|---:|
| Normal | 42 | 6 | 0 |
| Warning | 13 | 20 | 4 |
| Critical | 0 | 5 | 10 |

Thermal-Level 0: wahr 48/13/0, vorhergesagt 54/7/0; Level 1: wahr 0/24/5,
vorhergesagt 1/24/4; Level 2: wahr 0/0/10, vorhergesagt 0/0/10.
Fünf Critical-Fälle übersehen; die zehn Thermal-Level-2-Fälle hier korrekt.
Thermal-Level 0 und 1 bestimmen den Gesundheitsstatus laut Definition nicht allein,
weil zusätzlich das Vibrationslevel zählt. Last/Lage erschweren reine Bildinterpretation.
Keine perfekte Rekonstruktion verborgener Levels behauptet.

## Tatsächlich ausgeführte Prüfungen
- `scripts/uv.cmd run --offline --locked python -m unittest discover -s tests -p test_thermal_cnn.py -v`: **2/2 bestanden, 3,685 s**. Exakte Schichtkonfiguration/Shapes; ein Trainingsdurchlauf mit Gewichtsänderung, eval-/Dropout-Modus, stabile und normalisierte Wahrscheinlichkeiten, Wiederholung desselben Seeds mit identischem Ergebnis. Dieser fokussierte Test nutzt eine Epoche auf 16 TRAIN-Bildern, kein zusätzliches Modell-/Optimierungsexperiment.
- Bestehende 16.1-Tests einschließlich Split- und TRAIN-only-Perturbationsprüfung unmittelbar vor dessen autorisiertem Merge erneut bestanden: 3/3, 2,600 s; unveränderte Datenaufbereitung für 16.2 wiederverwendet.
- `scripts/uv.cmd run --offline --locked python scripts/build_exercise_16_2.py --check-html`: **acht Codezellen frisch sequenziell**, einschließlich beider vollständigen 30-Epochen-Trainings; nach Ergänzung tatsächlicher Interpretation erneut ausgeführt. Alle sechs numerischen CSV/JSON-Exporte von 16.2 zwischen beiden lokalen Läufen bytegleich.
- Alle Originalzellen unverändert in temporärem Arbeitsordner ausgeführt, damit relative Schreibpfade keine alten Ergebnisse überschreiben. Erneute 16.1-Vorhersagen/Labels/Indizes abgeglichen (Wahrscheinlichkeiten mit numerischer Toleranz). Freigegebene Zellen einschließlich Text, Code, Outputs und Metadaten im gespeicherten Notebook exakt erhalten; alle zwölf bisherigen Ergebnisartefakte bytegleich. Das erweiterte Notebook erhält erwartungsgemäß einen neuen Gesamthash; der alte Notebookhash im 16.1-Manifest bezieht sich weiterhin auf dessen damaligen Stand. Neuer Manifesthash und zusätzlicher Hash des freigegebenen Zellblocks dokumentieren die Erweiterung.
- Builder: 100 TEST-Indizes/Labels, 300 Wahrscheinlichkeiten/Argmax, Confusion-Matrix/Accuracy, beide Thermal-Level-Kreuztabellen, identische Split-CSV und TRAIN-Skalare unabhängig nachgerechnet/abgeglichen.
- Neue Confusion-Matrix und HTML bei **900/1400 px visuell geprüft**; drei eingebettete Grafiken geladen, offline keine Seitenfehler/fehlgeschlagenen Abrufe/Seitenüberläufe. 16.2-Abschnitt lesbar; PNGs in Originalauflösung öffnbar.
- Rohdaten-SHA256 und **neun Manifesthashes**, geschützte 16.1-Zellen/Ergebnisartefakte sowie **21 unveränderte Archive** bestätigt. Vorhandenes PyTorch 2.9.1+cpu und uv benutzt. Lokale Jupyter-TCP-Warnung ohne Ausführungsfehler. Aktuelle Push-/PR-CI nach Push tatsächlich abwarten und im Draft-PR verlinken.

## Grenzen und vier Fragen für den Human Review
Kleine synthetische Stichprobe, nur ein Split und Seed, keine externe Validierung.
Kein Overfitting-Nachweis ohne Validierungsdaten, keine plattformübergreifende
Bitgleichheit versprochen. Die Modalitäten enthalten jeweils nur einen Teil der
Zustandsinformation; 72 % sind keine Eignungsbestätigung für Sicherheitsüberwachung.
Historische Statusangaben im unveränderten 16.1-Abschnitt sind im neuen Abschnitt
klar als ursprünglicher Entwicklungsstand eingeordnet.

1. Sind 2D-Faltung, Pooling und die 64-Feature-Architektur verständlich erklärt?
2. Sind die verbleibenden Verwechslungen und fünf übersehenen Critical-Fälle klar dargestellt?
3. Erklärt die Thermal-Level-Tabelle nachvollziehbar, weshalb das Bild allein nicht immer ausreicht?
4. Ist der Vergleich mit 16.1 ausreichend auf diesen Split begrenzt und die unveränderte Vorverarbeitung transparent?

Kein Merge von 16.2, keine Fusion/16.3/16.4 und keine Universitätseinreichung.


## Tatsächlicher CI-Befund und minimale Prüferkorrektur

Erster Head 8685f6d: Push-CI erfolgreich, PR-CI 44909083863 fehlgeschlagen.
Ursache laut Traceback: ergänzende plattformübergreifende Wahrscheinlichkeitstoleranz
von 1e-5 für die neu ausgeführte 16.1-Vorstufe überschritten. Indizes, Labels und
sämtliche Klassen waren bereits identisch; keine Änderung der wissenschaftlichen
Modelle oder gespeicherten Ergebnisse. Die ohnehin ausgeschlossene Zusicherung
plattformübergreifender Wahrscheinlichkeitsgleichheit war im Prüfer zu streng umgesetzt.

Prüfer erfasst nun die maximale Abweichung ausdrücklich in Log/Manifest, warnt bei
Überschreitung und prüft weiter identische Klassen/Indizes/Labels, gültige normalisierte
Wahrscheinlichkeiten und unveränderte Originalartefakte. Lokale Wiederholbarkeit
bleibt separat anhand zweier vollständiger Läufe geprüft. Keine beliebig aufgeweitete
Toleranz oder nachträgliche Modelloptimierung. Aktuelle CI nach Korrektur abwarten.
Weitere CI-Warnungen: IPython verwendet bei nicht vorhandenem beschreibbarem Elternordner
einen temporären Ordner; setup-python@v5 meldet veraltete Node-20-Zielversion bei
Ausführung auf Node 24. Kein wissenschaftlicher Einfluss daraus abgeleitet.

Nach der Prüferkorrektur lokal erneut acht Zellen frisch und HTML offline 900/1400 px bestanden. 16.1-Wahrscheinlichkeitsabweichung lokal 0, sämtliche Klassen identisch; sechs numerische 16.2-Exporte weiterhin bytegleich zum ersten Lauf. Neun neue Artefakthashes und 21 unveränderte Archive erneut bestätigt. Keine wissenschaftlichen Änderungen.


### Weiterer tatsächlicher Plattformbefund

Head 546efd5: beide CI-Läufe scheiterten nun am zusätzlich verlangten Vergleich
der neu ausgeführten 16.1-Klassen mit dem gespeicherten Windows-Lauf. Damit ist
auch Klassenidentität zwischen beliebigen Runner-CPUs nicht zugesichert. Dieser
Befund wird nicht als wissenschaftliche Ergebnisänderung verdeckt.
Der finale Prüfer fordert stattdessen **zwei vollständige frische Ausführungen auf
demselben Runner** mit exakt identischen Vorhersage-CSV-Dateien beider Modelle
(einschließlich Wahrscheinlichkeiten). Indizes/Labels müssen weiter mit dem Original
übereinstimmen. Abweichende Klassen/Wahrscheinlichkeiten gegenüber dem gespeicherten
Plattformstand werden separat gezählt/protokolliert, nicht als gleich behauptet.
Die dokumentierte Matrix/72 % beziehen sich ausdrücklich auf die lokale Umgebung;
CI-Neuberechnungen können abweichen. Die früheren Einträge beschreiben jeweils den
damaligen Prüfstand. Beide aktuellen CI-Läufe nach dieser Änderung erneut abwarten.

Finaler lokaler Prüfer: zwei unabhängige frische Acht-Zellen-Ausführungen mit exakt identischen Vorhersage-CSV-Dateien für beide Modelle bestanden. Lokal erneut Vibration 0,58 / Thermal 0,72, null abweichende 16.1-Klassen und maximale Wahrscheinlichkeitsabweichung 0. HTML offline 900/1400 px bestanden; sechs numerische 16.2-Exporte unverändert. Die aktuellen CI-Ergebnisse folgen im Draft-PR.


## Erfolgreiche CI und beobachtete Plattformstreuung (Head 2c8be3a)

Beide vollständigen Läufe erfolgreich: Push 44909914982 und PR 44909918774.
Jeweils zwei frische vollständige Acht-Zellen-Läufe mit exakt identischen
Vorhersagen/Wahrscheinlichkeiten innerhalb des Runners und Offline-HTML bestanden.
PR-Runner: Vibration 0,58 / Thermal 0,70, null abweichende 16.1-Klassen, maximale
16.1-Wahrscheinlichkeitsabweichung 0,0000164 gegenüber gespeichertem Windows-Stand.
Push-Runner: Vibration 0,59 / Thermal 0,73, eine abweichende 16.1-Klasse, maximale
Wahrscheinlichkeitsabweichung 0,0065171. Lokal weiterhin 0,58 / 0,72.

Diese tatsächlichen Nebenbefunde sind keine geplante Mehrfachlauf-/Seedstudie oder
Unsicherheitsschätzung. Keine bestmögliche Kennzahl ausgewählt, keine Optimierung
oder Änderung gespeicherter Matrizen. Abschnitt 16.2 und HTML um diese Grenze ergänzt;
nur Markdown neu exportiert, danach Offline-HTML 900/1400 px erneut geprüft.
Keine neue Trainingsexekution für die reine Textergänzung behauptet.
Zusätzliche Reviewfrage innerhalb Frage 4: Ist die Unterscheidung zwischen lokaler
Wiederholbarkeit und beobachteter Plattformstreuung ausreichend deutlich?


## Studentischer Originalreview – 21.11.2026

HUMAN REVIEW – EXERCISE 16.2

Status: SCIENTIFICALLY APPROVED

1. CNN-Architektur und Methode

Das 2D-CNN entspricht der offiziellen Vorgabe. Zwei Faltungs-/Pooling-Blöcke verarbeiten die Wärmebilder und erzeugen anschließend 64 Merkmale für die Klassifikation.

Dropout, Trainingsmodus und Auswertungsmodus sind korrekt berücksichtigt.

Bewertung: BESTANDEN.

2. Modellergebnisse

Die lokale TEST-Accuracy beträgt 0,72 (72 von 100 korrekt).

Das Thermal-CNN erkennt zehn der 15 Critical-Fälle. Fünf Critical-Fälle werden als Warning klassifiziert.

Vier tatsächliche Warning-Fälle werden fälschlich als Critical eingestuft.

Die Confusion-Matrix ist korrekt und verständlich interpretiert.

Bewertung: BESTANDEN.

3. Thermal-Level-Analyse

Alle zehn Fälle mit Thermal-Level 2 werden korrekt als Critical erkannt.

Thermal-Level 0 und 1 erlauben keine vollständige Bestimmung des Gesundheitszustands, weil zusätzlich das Vibrationslevel relevant ist.

Die Grenzen einer einzelnen Sensormodalität werden nachvollziehbar erklärt.

Bewertung: BESTANDEN.

4. Vorverarbeitung, Vergleich und wissenschaftliche Grenzen

Der ursprüngliche TRAIN-/TEST-Split und die TRAIN-only-Standardisierung wurden beibehalten.

Das Thermal-CNN verbessert die lokale Accuracy gegenüber dem Vibrationsmodell von 0,58 auf 0,72, also um 14 Prozentpunkte.

Diese Differenz ist ein Ergebnis des vorliegenden Splits und kein statistischer Nachweis allgemeiner Überlegenheit.

Die Abweichungen zwischen CI-Runnern (Thermal-Accuracy 0,70 beziehungsweise 0,73) sind transparent dokumentiert.

Die identische Wiederholbarkeit innerhalb derselben Umgebung wurde bestätigt; plattformübergreifende Bitgleichheit wird nicht behauptet.

Bewertung: BESTANDEN.

GESAMTENTSCHEIDUNG:\
SCIENTIFICALLY APPROVED.

Zusätzlicher Human Review:\
Die acht hochgeladenen Ergebnisartefakte wurden erfolgreich anhand der Manifestprüfsummen kontrolliert. Die 100 Einzelvorhersagen, Argmax-Werte, TEST-Indizes und Confusion-Matrix wurden unabhängig rechnerisch abgeglichen.

Die vollständige Notebook- und Browserausführung wurde im Human Review nicht unabhängig wiederholt.

Keine weitere Modelloptimierung erforderlich.\
Keine Universitätseinreichung.
