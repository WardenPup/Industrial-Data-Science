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
