# Exercise 14.3 – Technischer Prüfbericht

**AWAITING HUMAN REVIEW**, 19.11.2026. Studentische Bewertung/Freigabe ausstehend.
Codex hat Anforderungen gelesen, Code und Notebook erstellt, Tests/Exporte ausgeführt
und die Ergebnisse technisch geprüft. Kein studentischer Review vorweggenommen.

## Aufgabe und Umsetzung
Offizielle Aufgabe: „Engineered features and model performance“ – Tiefenvergleich
für HDF und PWF mit/ohne temp_diff bzw. power; F1 statt Accuracy und Erklärung der
Klassenungleichheit. Quelle/Abrufdatum und Abnahmepunkte direkt im Notebook.

Fünf ursprüngliche Messgrößen als Basis, je Ziel genau ein Zusatzmerkmal.
Temperaturdifferenz in K; Leistung = Drehmoment × Drehzahl × 2π/60 in W.
Tiefen 1–8, Seed 42, Mindestblatt-/Teilungsgrößen 5 aus Kurs/14.2. Pro Ziel fester
stratifizierter 80/20-Split; beide Varianten/alle Tiefen identisch geteilt. Nur TRAIN
beim Fit. Keine Skalierung oder TEST-basierte Auswahl. Eine F1-Grafik mit zwei Panels,
64 TRAIN-/TEST-Metrikzeilen und 4.000 exportierte TEST-Zeilen für die feste Kurstiefe 3.

HDF: 115 positive Fälle, davon 92 TRAIN/23 TEST. PWF: 95, davon 76/19.
TEST bei Tiefe 3: HDF F1 0,611111 → 0,930233, FP/FN 2/12 → 0/3;
PWF F1 0,789474 → 1,000000, FP/FN 4/4 → 0/0.
HDF mit temp_diff: Tiefe 2 F1 0,978723, Tiefe 3 0,930233 – keine monotone
Verbesserung. PWF mit power erreicht hier ab Tiefe 2 TEST-F1=1. Kein allgemeiner
Überlegenheitsnachweis; es werden keine besten TEST-Modelle gewählt.

## Tatsächlich ausgeführte Prüfungen
Bestehende uv-Umgebung/Lockfile, keine neuen Pakete:
- `scripts/uv.cmd run --offline --locked python -m unittest discover -s tests -p test_engineered_features.py -v`: **3/3 bestanden**, 3,329 s. Physikalische Formeln/Nichtmutation/Anzahlen, alle 32 Fits ausschließlich auf den festgelegten TRAIN-Indizes mit gleichen Parametern und richtigen Merkmalen; unabhängige F1-Formel und Vorhersage-/FP-/FN-Abgleich.
- `scripts/uv.cmd run --offline --locked python scripts/build_exercise_14_3.py --check-html`: **3 frische sequenzielle Codezellen**, keine Zellfehler; 64 Metrikzeilen, vier Tiefe-3-Vorhersagegruppen und Rohdaten unabhängig geprüft; ein eingebettetes PNG.
- Offline-Chromium **900/1400 px bestanden**: Bild geladen, keine Seitenfehler/fehlgeschlagenen Anfragen/horizontalen Seitenüberläufe. PNG und beide vollständigen Browseransichten visuell kontrolliert (Achsen, Legenden, Tabellen, Interpretationen).
- **7 Manifesthashes** und ursprünglicher CSV-SHA256 geprüft; **21 Abgabearchive** unverändert. Vorherige wissenschaftliche Dateien und Originalreviews unverändert; CI-YAML eingelesen.

Kleine Darstellungskorrektur: ungewollte Ausgabe des Rückgabewerts eines Schreibaufrufs
unterdrückt, anschließend frisch ausgeführt und HTML erneut geprüft. Keine Änderung von
Modellparametern oder Ergebnissen. Bekannte Warnung: lokaler Jupyter-TCP-Transport
unverschlüsselt; keine Ausführungsfehler. Aktuelle GitHub-Actions-Ergebnisse werden erst
nach tatsächlichem Abschluss im Draft-PR am aktuellen Head dokumentiert.

## Grenzen und Human-Review-Fragen
Synthetische, regelbasierte Daten; nur ein Split pro Ziel, keine externen Maschinen,
zusätzlichen Seeds oder zeitlichen Validierungen. Wenige positive TEST-Fälle. F1
berücksichtigt keine Fehlerkosten und keine richtig negativen Fälle, daher FP/FN
zusätzlich. TRAIN-F1 ist kein unabhängiger Gütenachweis. Das Betrachten aller TEST-Kurven
dient dem geforderten Vergleich, nicht einer Optimierung; spätere Modellwahl bräuchte
eine getrennte Validierung. Keine Kausalitätsbehauptung oder weitere Modellstudie.

1. Ist verständlich, warum ein Immer-negativ-Modell fast 99 % Accuracy und trotzdem F1=0 haben kann?
2. Sind Temperaturdifferenz und Leistungsformel mit Einheiten sowie ihr Nutzen für Baumschnitte nachvollziehbar?
3. Ist klar, warum größere Tiefe nicht immer besseren TEST-F1 liefert und weshalb PWF-F1=1 hier keine allgemeine Garantie ist?
4. Sind TRAIN/TEST-Trennung, seltene Fehler und die getrennten Ziel-spezifischen Splits ausreichend erklärt?

Kein Merge, kein Beginn von 14.4, keine Universitätseinreichung.


---

## Studentischer Human Review – Originalwortlaut

# HUMAN REVIEW – EXERCISE 14.3

**Entscheidung: SCIENTIFICALLY APPROVED**

## 1. Aufgabenverständnis

Die Aufgabe wurde fachlich nachvollziehbar umgesetzt.

Der Vergleich von Entscheidungsbäumen mit unterschiedlichen Baumtiefen zeigt, welchen Einfluss zusätzlich berechnete Merkmale auf die Erkennung von Heat Dissipation Failure (HDF) und Power Failure (PWF) haben.

Die Betrachtung der Baumtiefen 1 bis 8 ist angemessen. Die Verwendung identischer TRAIN-/TEST-Aufteilungen ermöglicht einen direkten Vergleich der jeweiligen Modellvarianten.

## 2. Feature Engineering

Die Ergänzung von `temp_diff` für HDF und `power` für PWF ist fachlich sinnvoll.

Beide Merkmale verknüpfen vorhandene Messgrößen und können dadurch Zusammenhänge sichtbar machen, die ein flacher Entscheidungsbaum mit den ursprünglichen Einzelmerkmalen nicht ebenso einfach darstellen kann.

Die Ergebnisse zeigen deutlich, dass zusätzliche fachlich begründete Merkmale bereits bei vergleichsweise geringer Baumtiefe einen erheblichen Nutzen haben können.

Diese Verbesserung ist nicht automatisch auf andere Datensätze übertragbar. Insbesondere bei synthetischen Daten können solche Merkmale die zugrunde liegenden Regeln besonders gut abbilden.

## 3. Überprüfung der Ergebnisse

Die bereitgestellten Einzelvorhersagen und Ergebnistabellen wurden rechnerisch kontrolliert.

**HDF bei Baumtiefe 3:**

- Basismodell: F1 = 0,611111
- Mit `temp_diff`: F1 = 0,930233
- Basismodell: 2 False Positives und 12 False Negatives
- Mit Zusatzmerkmal: 0 False Positives und 3 False Negatives

**PWF bei Baumtiefe 3:**

- Basismodell: F1 = 0,789474
- Mit `power`: F1 = 1,000000
- Basismodell: 4 False Positives und 4 False Negatives
- Mit Zusatzmerkmal: keine Fehlklassifikationen

Die aus den 4.000 bereitgestellten Vorhersagezeilen erneut berechneten Werte stimmen mit den Ergebnistabellen überein.

Der Nutzen der Zusatzmerkmale ist damit für den untersuchten TEST-Split eindeutig nachgewiesen.

## 4. Bewertung der Grafik

Die Darstellung ist verständlich und ausreichend beschriftet.

Besonders positiv:

- TRAIN und TEST sind durch unterschiedliche Linienstile unterscheidbar.
- Basis- und erweiterte Modelle sind farblich getrennt.
- HDF und PWF werden separat dargestellt.
- Die Unterschiede zwischen den Baumtiefen sind gut erkennbar.

Die Grafik zeigt außerdem, dass eine größere Baumtiefe nicht zwangsläufig zu einem besseren TEST-F1 führt.

Es besteht kein zwingender Bedarf für weitere Abbildungen.

## 5. Accuracy und F1

Die Verwendung des F1-Scores ist angemessen, da positive Fehlerfälle in diesem Datensatz selten sind.

Von 10.000 Datenpunkten sind lediglich 115 HDF-positiv und 95 PWF-positiv.

Ein Modell könnte daher sehr viele Fälle korrekt als fehlerfrei klassifizieren und trotzdem einen großen Teil der tatsächlichen Fehler übersehen.

Der F1-Score berücksichtigt sowohl übersehene Fehler als auch falsche Fehlermeldungen und ist deshalb für diesen Vergleich aussagekräftiger als Accuracy allein.

## 6. Wissenschaftliche Einschränkungen

Folgende Grenzen müssen in der Ausarbeitung erkennbar bleiben:

1. Es wurde nur eine feste TRAIN-/TEST-Aufteilung untersucht.
2. Die positiven TEST-Fälle sind mit 23 HDF- und 19 PWF-Fällen sehr selten.
3. Ein F1-Wert von 1,0 bedeutet lediglich, dass auf diesem TEST-Split alle Fälle korrekt klassifiziert wurden.
4. Die Ergebnisse belegen keine allgemeine Überlegenheit der erweiterten Modelle bei anderen Daten.
5. Die Untersuchung der Baumtiefen auf TEST darf nicht als unabhängige Hyperparameteroptimierung interpretiert werden.
6. Die Zusatzmerkmale können bei synthetischen Daten besonders stark mit den Regeln zur Labelerzeugung zusammenhängen.

Eine zusätzliche Kreuzvalidierung oder umfangreiche Parameterstudie ist für diese Übung nicht zwingend erforderlich.

## 7. Technische Nachvollziehbarkeit

Die bereitgestellten CSV-Dateien sind untereinander konsistent.

Die berechneten F1-Werte, Fehlerzahlen und Klassenzählungen stimmen überein. Die SHA256-Prüfsummen der sechs bereitgestellten Ergebnisartefakte entsprechen dem Validierungsmanifest.

Die gemeldeten drei erfolgreichen Tests, die frische Notebook-Ausführung und die GitHub-CI-Ergebnisse werden als technische Validierungsnachweise anerkannt. Sie wurden im Rahmen dieses Human Reviews nicht eigenständig erneut ausgeführt.

## 8. Abschließende Bewertung

Die Aufgabe erfüllt ihren wesentlichen wissenschaftlichen Zweck.

Es wird nachvollziehbar demonstriert, dass fachlich begründetes Feature Engineering die Fehlererkennung eines Entscheidungsbaums erheblich verbessern kann, ohne dass dafür zwingend eine große Baumtiefe benötigt wird.

Die erzielten Ergebnisse sind plausibel, rechnerisch konsistent und verständlich dargestellt.

**Human-Review-Ergebnis: APPROVED**

Keine verpflichtenden wissenschaftlichen Änderungen.

Die bereits dokumentierten Einschränkungen sollen erhalten bleiben.

Die Freigabe gilt für die fachliche Ausarbeitung. Der technische Abschluss und der Merge sind weiterhin separat zu prüfen und freizugeben.