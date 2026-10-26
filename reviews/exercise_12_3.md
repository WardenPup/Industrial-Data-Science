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


# HUMAN REVIEW – EXERCISE 12.3
Datum: 26.10.2026
Status: SCIENTIFICALLY APPROVED WITH MINOR DOCUMENTATION CLARIFICATION
Merge-Autorisierung: NEIN
Repository: WardenPup/Industrial-Data-Science
PR: #11 (Draft)
Gegenstand: Time Series Forest Classification (aeon)

## 1. Umfang und Prüfgrundlage
Ich habe die beiden bereitgestellten Abbildungen sowie metrics.csv, classification_report.csv, confusion_forest.csv, forest_probabilities.csv, paired_comparison.csv, predictions.csv, summary.json und validation_manifest.json geprüft. Der HTML-Export wurde als zusätzliches Artefakt bereitgestellt. Die nachstehenden Rechnungen beruhen auf den angehängten Ergebnisdateien und ersetzen keine unabhängige erneute Modelltrainingsprüfung, keinen kompletten Quellcode-Audit und keine selbst durchgeführte GitHub-CI-Prüfung. Die Angaben zu 57 bestandenen Tests, drei frisch ausgeführten Notebook-Zellen, Offline-HTML-Tests und erfolgreicher CI stammen aus dem technischen Abschlussbericht von Codex.

## 2. Daten und Versuchsaufbau
Es sind 120 TRAIN- und 320 TEST-Gesten mit jeweils drei Kanälen und 315 Abtastwerten dokumentiert. Der TEST-Split enthält acht Klassen mit jeweils 40 Fällen. Der fest konfigurierte TimeSeriesForestClassifier wird mit 200 Bäumen, random_state=42, n_intervals='sqrt', min_interval_length=3 und n_jobs=1 beschrieben. Die beschriebene Skalierung nutzt ausschließlich TRAIN-Statistiken. Diese Entscheidung ist richtig, weil TEST-Informationen nicht in die Modellbildung einfließen dürfen. Die vollständige Pipeline und das Ausbleiben jeder TEST-gestützten Modellauswahl sollen bei der technischen Schlussprüfung nochmals anhand des Codes bestätigt werden.

## 3. Numerische Prüfung
Die Konfusionsmatrix summiert sich auf 320 TEST-Fälle. Die Diagonalsumme beträgt exakt 277, also 277/320 = 0,865625 bzw. 86,5625 % Accuracy; 43 Fälle wurden fehlklassifiziert. Die übermittelte Macro-F1 beträgt 0,863884. Die Klassen sind gleich häufig, daher ist Balanced Accuracy in diesem Fall mit der gewöhnlichen Accuracy identisch.

Der Vergleich auf demselben TEST-Split lautet:
- DTW-3-NN: 291/320 korrekt, Accuracy 0,909375, Macro-F1 0,908593.
- CNN: 271/320 korrekt, Accuracy 0,846875, Macro-F1 0,846505.
- Time Series Forest: 277/320 korrekt, Accuracy 0,865625, Macro-F1 0,863884.

Der Forest liegt somit 1,875 Prozentpunkte über dem CNN und 4,375 Prozentpunkte unter DTW-3-NN. Diese Unterschiede gelten ausschließlich für den untersuchten festen Split und die dokumentierten Konfigurationen; daraus folgt kein allgemeiner Rang der Verfahren.

Die Paardaten sind ebenfalls rechnerisch konsistent:
- Forest vs. DTW-3-NN: 270 beide korrekt, 7 nur Forest korrekt, 21 nur DTW korrekt, 22 beide falsch.
- Forest vs. CNN: 261 beide korrekt, 16 nur Forest korrekt, 10 nur CNN korrekt, 33 beide falsch.

Die 320 Forest-Wahrscheinlichkeitsvektoren summieren sich je Fall innerhalb der numerischen Gleitkommatoleranz auf 1. Die jeweils wahrscheinlichste Klasse stimmt in allen 320 Fällen mit dem exportierten Forest-Label überein. Dies belegt die interne Konsistenz der vorliegenden Exporte, nicht die Kalibrierung der Wahrscheinlichkeiten.

## 4. Wissenschaftliche Interpretation der Fehler
Die deutlichste systematische Verwechslung ist Klasse 4 -> 5 mit 11 von 40 Fällen. Für Klasse 4 werden 25 von 40 Gesten korrekt erkannt. Klasse 6 wird 31-mal korrekt klassifiziert und zeigt weitere Verwechslungen mit Klassen 1, 3 und 4. Diese Beobachtungen sind quantitativ belegbar, aber ihre Ursachen lassen sich aus der Konfusionsmatrix allein nicht beweisen. Es wäre unzulässig, daraus unmittelbar Sensorfehler, bestimmte Gestenähnlichkeiten oder ein Overfitting abzuleiten.

## 5. Abbildung 1: Tatsächliches Intervall des ersten Forest-Baums
Die Abbildung zeigt anschaulich einen standardisierten Sensorverlauf und den im Modell verwendeten Ausschnitt [85, 146). Die halboffene Schreibweise bedeutet die Indizes 85 bis 145, also 61 Abtastwerte. Der Ausschnitt deckt einen lokalen Übergang von negativen Werten zu einem deutlichen Maximum ab. Das ist ein erklärendes Beispiel für intervallbasierte Merkmale und keine globale Aussage über die Wichtigkeit dieser Position für das gesamte Forest-Modell.

Kleine Dokumentationskorrektur: In der Abbildung steht 'Kanal 3', während summary.json 'channel': 2 enthält. Das ist bei menschenlesbarer Nummerierung 1–3 und nullbasierten Python-Indizes 0–2 konsistent. Bitte die Umrechnung im Notebook bzw. direkt an der Grafik ausdrücklich erklären. Keine nachträgliche Änderung am Modell ist dafür nötig.

## 6. Abbildung 2: Konfusionsmatrix und Modellvergleich
Die Konfusionsmatrix ist vollständig und in ihrer Zeilen-/Spaltenorientierung eindeutig ('Wahre Klasse' versus 'Vorhergesagte Klasse'). Alle acht Klassen sowie die absoluten Häufigkeiten sind lesbar. Die Balkengrafik vergleicht Accuracy und Macro-F1 für DTW-3-NN, CNN und Forest ohne irreführende stark abgeschnittene y-Achse. Die Darstellung ist geeignet. Für das Verständnis sollte der Text ausdrücklich sagen, dass alle Werte auf demselben TEST-Split und mit fixierten Konfigurationen entstanden.

## 7. Wissenschaftliche Grenzen
Der Datensatz ist mit 120 TRAIN-Beispielen klein. Die Bewertung stammt aus einem einzigen Split und einer einzigen Forest-Seed-Konfiguration. Es wurden keine Wiederholungen über Seeds, keine Konfidenzintervalle, keine unabhängige externe Validierung und keine nachgewiesene statistische Signifikanz des Verfahrensvergleichs vorgelegt. Solche Studien dürfen nicht nachträglich als durchgeführt ausgegeben werden. Die feste Zeitreihenlänge und die Skalierung können relevante Form- und Amplitudeninformation beeinflussen; auch dies ist als Methodenentscheidung zu beschreiben. Trainings- und Testgesten müssen als vorhandene Split-Struktur respektiert werden.

## 8. Formulierungsqualität und Umfang
Die Ausarbeitung sollte technisch korrekt, aber auf studentischem Niveau knapp bleiben. Nötig sind eine verständliche Beschreibung der zufällig gewählten Intervalle und ihrer Merkmale, die feste Modellkonfiguration, eine tabellarische Ergebnisgegenüberstellung, die beiden Abbildungen sowie eine vorsichtige Diskussion der Grenzen. Zusätzliche repetitiv beschriebene Diagramme oder unnötige KI-typische Standardpassagen sind nicht erforderlich.

## 9. Freigabeentscheidung
Ich bewerte Exercise 12.3 auf Grundlage der bereitgestellten Ergebnisse als fachlich gelungen. Die präsentierten Metriken, die Konfusionsmatrix, Wahrscheinlichkeiten und paarweisen Vergleiche sind untereinander konsistent. Die beiden Grafiken sind aussagekräftig. Ich bitte nur um die kleine textliche Präzisierung zur Kanalnummerierung (Kanal 3 entspricht Python-Index 2), sofern sie nicht bereits eindeutig im Notebook steht.

Wissenschaftlicher Human Review: APPROVED WITH MINOR DOCUMENTATION CLARIFICATION.
Technische Abschlussprüfung und CI sollen den aktuellsten Stand noch einmal kontrollieren.
Dies ist KEINE Merge-Autorisierung. PR #11 darf nicht gemergt werden.
Exercise 12.4 darf noch nicht begonnen werden. Keine Universitätseinreichung.


---

## KI-/technische Abschlussanmerkung – Codex, 26.10.2026

Aktueller Status: SCIENTIFICALLY APPROVED – TECHNICALLY VALIDATED – AWAITING FINAL MERGE AUTHORIZATION.
Die studentische Freigabe mit kleiner Dokumentationspräzisierung stammt aus dem
Originalreview oben, separat unverändert in fb85fa2 gesichert. Auch der frühere
technische Bericht bleibt als Historie unverändert. Keine zusätzlichen studentischen
Tests, Code-Audits oder CI-Prüfungen behauptet. Keine Merge-Autorisierung erteilt.

### Tatsächliche Korrektur und Codeprüfung
Ein knapper Satz erklärt nun im Notebook/HTML: Kanal 3 entspricht Python-Index 2.
Die Grafik verwendet nachweislich `Kanal {channel+1}`, die Datenadressierung
`[0,channel]`. summary.json enthält channel=2, Intervall [85,146), also 61 Werte.
Kein Modell-, Daten- oder Grafikwechsel. Das Intervall bleibt ausdrücklich ein
Merkmalsbeispiel, keine globale Feature-Importance. Gleicher TEST-Split, feste
Konfigurationen, keine allgemeine/signifikante Überlegenheit und keine kausale
Deutung von 4→5 werden im Notebook ausdrücklich erklärt.

`fit_forest` erhält ausschließlich x_train/y_train; der Skalierer berechnet
Mittelwert/Standardabweichung nur daraus, anschließend fit auf diesen transformierten
120 Fällen. TEST wird mit festem TRAIN-Skalierer transformiert; Labels werden erst
in Auswertung/Referenz-Zuordnungsprüfung benutzt. Keine TEST-basierte Suche oder
Auswahl im geprüften Notebook/Kerncode. Konfiguration bereits vor Training in
78610e0 festgelegt. Bestehender instrumentierter TRAIN-Fit-Test erneut bestanden.
Der TEST-Benchmark war durch 12.2 bereits bekannt; kein neuer unabhängiger Testdatensatz.

### Tatsächlich erneut ausgeführte Befehle und Resultate
Mit `scripts/uv.cmd run --offline --locked` vom Projektstamm:
- `python -m unittest discover -s tests -q`: alle 57 Tests bestanden, 6,710 s.
- `python scripts/build_exercise_12_3.py`: frischer Kernel, drei Codezellen sequenziell,
  beide PNGs dekodiert. Zweiter vollständiger Forest-Fit bestätigt alle 320 Labels
  und Probability-Vektoren; Mittelung aller 200 Baumwahrscheinlichkeiten geprüft.
  Metriken/24 Klassenberichtzeilen separat aus allen 960 Modellvorhersagen gerechnet.
  Zusätzliche explizite Assertions sichern die konkreten Reviewzahlen und Kanalzuordnung.
- `python scripts/check_exercise_12_3_html.py`: offline 900/1400 px, beide Bilder
  geladen, keine Seitenfehler oder horizontaler Überlauf. Beide PNGs visuell geprüft.
- 120 TRAIN/320 TEST, 3 × 315, 200 Bäume, acht TEST-Klassen zu je 40 Fällen bestätigt.
  Forest 277 korrekt/43 falsch, Accuracy 0,865625, Macro-F1 0,8638843023800332;
  Referenzen DTW 291 und CNN 271 korrekt. Beide Paarvergleiche bestätigt:
  DTW 270/7/21/22, CNN 261/16/10/33 (beide/nur Forest/nur Referenz richtig/beide falsch).
  Alle 320 × 8 Wahrscheinlichkeiten endlich, nicht negativ, Zeilensumme 1 innerhalb
  Gleitkommatoleranz, argmax in jedem Fall gleich exportiertem Forest-Label.
- Forest-Diagonale [35,39,35,25,37,31,36,39]; Fehler je Klasse
  [5,1,5,15,3,9,4,1]. Klasse 4→5 elfmal. Klasse 6: 31 richtig, Fehler nach
  1/3/4: 4/4/1. Alle Matrixzellen stimmen mit Einzelvorhersagen und Bericht überein.
- Beide unveränderten Original-.ts-Dateien gegen Quellen-SHA256 geprüft, fünf
  Referenzhashes gegen freigegebenen Git-Stand 50d3a01 und 13 aktuelle Artefakthashes
  geprüft. Originalquelle/Archivherkunft dokumentiert in docs/UWAVE_SOURCE.md.
  Kein erneuter Netzwerkdownload oder erneute Archivprüfung behauptet.
- Acht wissenschaftliche 12.3-Artefakte (zwei PNGs, Metriken, Vorhersagen, Bericht,
  Matrix, Wahrscheinlichkeiten, Paare) bytegleich mit 4b4f197. Frühere Lösungen,
  Reviews, Umgebung und alle acht Abgabe-ZIPs (SHA256/CRC) unverändert.

Notebook-Fit/Predict: 6.2079/0.9835 s;
separater Audit: 5.5775/0.9087 s.
Abweichungen zu historischen Laufzeiten ändern keine wissenschaftlichen Ergebnisse;
Hardware/Cache/JIT können Zeiten beeinflussen. Jupyter warnte tatsächlich über
unverschlüsselten lokalen TCP-Transport. Keine fehlgeschlagenen numerischen,
Notebook- oder Offline-HTML-Prüfungen. Ein Konsolen-Leseversuch scheiterte an cp1252
bei griechischen Zeichen; erneutes Lesen mit UTF-8 erfolgreich, Artefakte unbeschädigt.

Grenzen unverändert: ein fester bekannter Split, ein Seed, 120 Trainingsfälle,
keine zusätzliche Seed-/externe Validierungsstudie, keine Konfidenzintervalle,
Signifikanz oder Kalibrierung belegt; physikalische Auflösung/Personensplit unbekannt.
Aktuelle Head-CI und PR-Reviewpunkte werden nach Push separat im PR dokumentiert;
Ready for review nur bei beiden erfolgreichen Läufen. Kein Merge, keine 12.4/Einreichung.
