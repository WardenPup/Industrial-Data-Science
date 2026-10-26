# Aufgabe 12.3 – Human-AI Review

Status: AWAITING HUMAN REVIEW – NOT MERGED.
Technischer Bericht von Codex, 26.10.2026. Kein studentischer Review, keine
studentischen Beobachtungen oder Freigabe für 12.3 vorliegend.

## Umsetzung und KI-Beitrag
Codex las die offizielle Exercise 12.3, Kursabschnitt 8.1, aeon API und installierten
1.6.0-Quelltext. Anforderungen wurden vor Training separat in 78610e0 festgelegt;
Implementierung d9ba2c8. TRAIN-only-Kanalskalierung und Rohdatenlader aus 12.2
wiederverwendet, frühere Lösungen/Reviews nicht verändert. Keine neue Abhängigkeit.
200 TimeSeriesForestClassifier-Bäume, 30 Kanalintervallziehungen/Baum, Mindestlänge 3,
Seed 42, n_jobs=1, kein Zeitlimit oder Tuning. Tatsächliche Intervallanzahl 29–30.
Merkmale Mittelwert, Populationsstandardabweichung und OLS-Steigung; Entropiebäume,
Mittelung der Klassenwahrscheinlichkeiten, erster argmax bei Gleichstand.
Keine Bootstrap-Fallauswahl und keine DTW-Distanz im Forest. Annahmen, keine Optima.

## Tatsächliche Ergebnisse
120 TRAIN-/320 TEST-Gesten, je 3 × 315, acht Klassen, null fehlende Werte.
- Forest: 277/320 korrekt, Accuracy/Balanced Accuracy 0,865625, Macro-F1 0,8638843023800332.
- Freigegebener DTW-3-NN: 291/320, Accuracy 0,909375, Macro-F1 0,9085926338042423.
- Freigegebenes CNN: 271/320, Accuracy 0,846875, Macro-F1 0,8465046609503573.
Forest gegenüber CNN +6 Fälle/+1,8750 Prozentpunkte, gegenüber kNN −14/−4,3750.
Auch Macro-F1 liegt dazwischen; besseres Ergebnis hier nur gegenüber CNN.
Gepaart zu kNN: beide richtig 270, nur Forest richtig 7, nur kNN richtig 21,
beide falsch 22. Zu CNN: 261,16,10,33. Keine Signifikanzbehauptung.
Klasse 4→5 elfmal, Klasse 4 richtig 25/40. Keine kausale Erklärung daraus.

Erstes tatsächliches Intervall: TRAIN-Fall 0, Kanal 3, [85,146), Schritt 1.
Mittelwert −0,1652857742, Standardabweichung 1,2753812990, Steigung 0,0625554358
je Abtastschritt; gegen tatsächlich verwendete aeon-Funktionen geprüft.

## Ausgeführte technische Prüfungen
Befehle vom Projektstamm mit `scripts/uv.cmd run --offline --locked`:
1. `python -m unittest discover -s tests -q`: zuletzt 57 Tests erfolgreich in 6,900 s
   (erster vollständiger Lauf 8,063 s). Fünf neue Tests: Intervallformeln gegen aeon,
   instrumentierter TRAIN-only-Fit, Multikanal-Seed-Reproduktion/Probability-Aggregation,
   ungültige Daten/Labels und gehashte Referenz mit TEST-Reihenfolge.
2. `python scripts/build_exercise_12_3.py`: frischer Kernel, drei Codezellen sequenziell;
   zwei eingebettete PNGs dekodiert. Alle drei Metriken und 24 Klassenberichtzeilen
   unabhängig aus den 960 Einzelvorhersagen nachgerechnet, Forest-Confusion-Matrix
   und gepaarte Vergleiche nachgezählt. Zweiter vollständiger Forest-Fit reproduziert
   alle 320 Labels und Wahrscheinlichkeiten. Alle 200 Baumwahrscheinlichkeiten separat
   auf den jeweiligen Intervallmerkmalen berechnet und Mittelung bestätigt.
3. `python scripts/check_exercise_12_3_html.py`: offline 900 und 1400 px, beide Bilder
   geladen, keine Seitenfehler und kein horizontaler Überlauf.
4. Beide PNGs visuell geprüft: tatsächliches TRAIN-Intervall mit korrekter exklusiver
   Endgrenze; Confusion-Matrix mit wahren Zeilen/vorhergesagten Spalten und 0–40-Skala;
   Vergleich auf 0–1-Skala mit Legende. Keine unbelegten physikalischen Einheiten.
5. Beide Rohdatenhashes beim Laden geprüft. Fünf unveränderte freigegebene Referenz-
   artefakte gegen Git-Bytes von 50d3a01 gehasht; aktuelle wissenschaftliche Werte
   zusätzlich verglichen. Frühere CI-Schritte erzeugen ggf. andere Laufzeiten/Zeilenenden;
   diese ändern keine Referenzwerte. Dreizehn neue Artefakthashes im Manifest geprüft.
6. Frühere Ergebnisse, sämtliche bestehenden Human Reviews, pyproject.toml/uv.lock
   unverändert gegen a216fdc. Alle acht Kapitel-10/11-ZIPs per SHA256 und CRC bestätigt.

Letzter Notebook-Fit 5.6534 s, Predict 0.9894 s;
separater Fit 5.8589 s, Predict 1.1296 s.
Prediction-Zeit umfasst den offiziellen predict-Aufruf einschließlich modellinterner
Intervalltransformation; die externe Kanalskalierung erfolgt vor der Zeitmessung.
der zusätzliche Probability-Diagnoseaufruf ist nicht enthalten. Hardware/Cache/JIT
beeinflussen Laufzeiten. Keine Rechenkostenrangfolge mit alten 12.2-Laufzeiten.
Tatsächlich beobachtet: Jupyter-Warnung über unverschlüsselten lokalen TCP-Transport.
Keine numerischen/Test-/Offline-HTML-Fehler in den ausgeführten 12.3-Prüfungen.
GitHub Actions werden am gepushten aktuellen Head separat im Draft PR dokumentiert;
vor Abschluss keine erfolgreiche CI behauptet.

## Grenzen und Fragen für den studentischen Review
Ein bekannter Split, nur 120 Trainingsfälle, Seed 42 und keine separate Validierungs-
oder Hyperparameterstudie. Keine Signifikanz, optimale Parameter, Personenunabhängigkeit
oder geprüfte Kalibrierung behaupten. Intervallstatistiken verlieren Details, keine
elastische Ausrichtung wie DTW. Ursprünglich feste Länge 315, physikalische Auflösung
unbekannt. Katalogfallzahlen weichen vom Originalarchiv ab; Quelle/Lizenzgrenzen siehe
`docs/UWAVE_SOURCE.md`. Keine nachträgliche Optimierung auf TEST vorgenommen.

1. Sind Intervallmerkmale und deren Einheit anhand der ersten Grafik verständlich?
2. Ist der Unterschied zwischen diesem Forest, gewöhnlichem Random Forest und DTW klar?
3. Ist die Antwort „über CNN, unter kNN auf diesem Split“ durch Tabellen/Grafik nachvollziehbar?
4. Wie beurteilst du Klasse 4→5 und die gepaarten Unterschiede ohne kausale Überinterpretation?
5. Sind ein Seed, fehlende Validierungsstudie und unbekannter Personensplit ausreichend eingeordnet?

Keine Änderungen/Feedback des Studenten vorweggenommen. Kein Merge 12.3, kein Beginn
von 12.4, keine bestehenden Abgabepakete verändert und keine Universitätseinreichung.
