# Exercise 15.1 – Technischer Prüfbericht

**AWAITING HUMAN REVIEW – KAGGLE-REGISTRIERUNG OFFEN**, 21.11.2026.
Keine studentische wissenschaftliche Bewertung/Freigabe erfunden. Student bestätigte
am 21.11.2026 ausdrücklich: noch kein Kaggle-Konto. Codex legte kein Konto an und
verwendete keine Zugangsdaten. Die offizielle Registrierungsanforderung ist **nicht
erledigt**; der öffentliche Download ersetzt sie nicht. Die Datenanalyse ist technisch geprüft.

## Anforderungen, Methode und Ergebnisse
Offizielle Aufgabe: „Register and download the dataset“ – Registrierung, Beschreibung
lesen, Download, Struktur/Typen/Probleme/Ziele/Klassenhäufigkeiten; Hauptflag gegen
Untergruppen-ODER, Mehrfachfehler und begründeter Umgang bei künftigem Training.
Anforderungen, Quellen und Abrufdatum direkt im Notebook, separater Anforderungencommit.
Codex: Lektüre, öffentlicher Download, Code, Notebook, Zählungen/Grafik, technische QA.

Originaler XAI Drilling Dataset, Kaggle Version 1, CC BY-NC-SA 4.0, 1.107.906 Bytes;
Quelle/Lizenz und feste SHA256 unter data/raw/XAI_DRILLING_SOURCE.md. CSV unverändert
für netzunabhängige Reproduktion versioniert. Keine Pakete ergänzt, kein Modell trainiert.
Pandas-Zählungen/logische ODER-Prüfung reichen aus, ein Häufigkeitsdiagramm ergänzt Tabellen.

20.000 × 15, 13 numerische und zwei object-Spalten; keine Fehlwerte, nichtendlichen
Zahlen oder vollen Duplikate. ID 1–20.000 eindeutig. Ohne ID **2 zusätzliche identische
Zeilen**, vier betroffene IDs 3152/6070/7196/18565; nichts gelöscht. Cooling hat fünf
Stufen, während die Beschreibung „four distinct states“ schreibt, selbst aber fünf
aufzählt. Einheiten aus der Quelle übernommen, nicht experimentell validiert.

Main Failure **1.001 (5,005 %)**; BEF/CCF/FWF/WDF **215/344/278/300**. Die Zielklassen
sind selten und nicht disjunkt. Hauptflag = Untergruppen-ODER in allen Zeilen,
**0 Widersprüche**. 18.999 Zeilen ohne Untergruppen; 887 mit einer, 92 mit zwei,
22 mit drei und keine mit vier: **114 Mehrfachfehler**. Summe der Untergruppen 1.137
ist deshalb kein Widerspruch zur Zahl der Fehlerzeilen.

Mehrfachlabels erhalten, nicht willkürlich auf eine Klasse reduzieren. Bei späteren
Widersprüchen Herkunft/Semantik prüfen, Originale erhalten und begründete Ableitungen
separat dokumentieren. Fehlerflags nicht als Modelleingaben für Fehlerziele verwenden;
identische Beobachtungen vor späterem Split beachten. Keine Modell-/15.2-Analyse vorweggenommen.

## Tatsächlich ausgeführte Prüfungen
- Öffentlicher offizieller Kaggle-Version-1-Download ohne Anmeldung tatsächlich erfolgreich; Dateiname, Größe, Version und SHA256 geprüft. Registrierung weiterhin offen.
- `scripts/uv.cmd run --offline --locked python -m unittest discover -s tests -p test_drilling_data.py -v`: **3/3 bestanden**, 0,331 s. Originalhash/Schema/Zahlen, gezielt widersprüchliches und mehrfach markiertes Testbeispiel/Nichtmutation, ungültige Labels nicht still zählen.
- `scripts/uv.cmd run --offline --locked python scripts/build_exercise_15_1.py --check-html`: **3 frische sequenzielle Codezellen**, keine Zellfehler; unabhängige Originaldaten-/Tabellenzählungen und ein eingebettetes PNG.
- Offline-Chromium **900/1400 px bestanden**: Bild geladen, keine Seitenfehler/fehlgeschlagenen Anfragen oder horizontalen Seitenüberläufe. Grafik und beide vollständigen HTML-Ansichten visuell geprüft; Tabellen, Einheiten/Labels, Häufigkeiten und Grenzen lesbar.
- Rohdaten-SHA256 und **11 Manifesthashes** geprüft, **21 Abgabearchive** unverändert. Frühere Daten, Lösungen und Originalreviews unverändert. Fokussierte CI-YAML eingelesen; aktuelle Head-CI erst nach tatsächlichem Abschluss im Draft-PR verlinkt.

Konkreter technischer Fehler beim ersten Exportprüfer: eine wiederverwendete Variable
zählte fünf Tabellenzeilen statt drei ausgeführter Codezellen für die Meldung/das
Manifest. Variable getrennt, frische Ausführung/HTML wiederholt: korrekt drei Zellen.
Keine wissenschaftlichen Ergebniswerte geändert. Bekannte lokale Jupyter-TCP-Warnung
ohne Verschlüsselung, keine Ausführungsfehler. Keine zusätzliche Testsuite oder Installation.

## Grenzen und vier Fragen für den Human Review
Synthetische Daten, interne Konsistenz ist kein Ursachen- oder Modellgütenachweis.
Seltene Fehler, Mehrfachlabels, Duplikate und ungeprüfte Originaleinheiten sind bei
späterem Training zu beachten. Die vollständige Datensatzbeschreibung wurde bereits
gelesen; spätere Exploration ist nicht blind gegenüber den Subgroup-failures-Angaben.

1. Ist der Unterschied zwischen Hauptflag, Untergruppen-ODER und gleichzeitig auftretenden Mehrfachfehlern verständlich?
2. Sind Klassenhäufigkeiten und ihre Konsequenzen für spätere Modellbewertungen nachvollziehbar?
3. Ist der vorgeschlagene Umgang mit Mehrfachlabels, möglichen Widersprüchen und identischen Beobachtungen fachlich angemessen, ohne Originaldaten zu verändern?
4. Sind Datentypen/Einheiten, Zielvariablen und die Grenzen der internen Konsistenzprüfung klar erklärt?

Offener studentischer Schritt: Kaggle registrieren und bestätigen. Kein Human Review
oder Merge vorweggenommen. Keine Arbeit an 15.2, keine Universitätseinreichung.


---

## Studentischer Human Review – Originalwortlaut, übergeben am 21.11.2026

HUMAN REVIEW – EXERCISE 15.1
Industrial Data Science – XAI Drilling

Status: SCIENTIFICALLY APPROVED – FORMAL REQUIREMENT PENDING

Die Ergebnisse der Aufgabe 15.1 wurden anhand der bereitgestellten Auswertungen und Visualisierung wissenschaftlich geprüft.

1. Datenverständnis und Datenqualität

Der Datensatz umfasst 20.000 Beobachtungen mit 15 Spalten. Es wurden keine fehlenden Werte festgestellt.

Die Untersuchung der Duplikate ist nachvollziehbar. Unter Berücksichtigung der ID gibt es keine vollständig identischen Zeilen. Ohne ID existieren zwei zusätzliche Duplikate, die jeweils zu einer Gruppe aus zwei identischen Beobachtungen gehören.

Die Entscheidung, diese Zeilen zunächst unverändert zu erhalten, ist angemessen.

2. Fehlerklassen und Klassenungleichgewicht

Die Verteilung der Fehlerlabels ist korrekt dargestellt:

- Main Failure: 1.001 Fälle (5,005 %)
- BEF: 215 Fälle (1,075 %)
- CCF: 344 Fälle (1,720 %)
- FWF: 278 Fälle (1,390 %)
- WDF: 300 Fälle (1,500 %)

Die Grafik verdeutlicht, dass Fehlerfälle gegenüber fehlerfreien Beobachtungen selten sind.

Für spätere Klassifikationsaufgaben ist deshalb eine Bewertung über geeignete Kennzahlen wie Precision, Recall und F1 sinnvoll. Accuracy allein könnte irreführend sein.

3. Labelkonsistenz und Mehrfachfehler

Die Hauptfehlermarkierung stimmt in allen 20.000 Zeilen mit der logischen ODER-Verknüpfung der vier Fehleruntergruppen überein.

Es wurden keine widersprüchlichen Labels gefunden.

Die 114 Mehrfachfehler sind keine Labelkonflikte:

- 92 Beobachtungen tragen zwei Fehlerlabels.
- 22 Beobachtungen tragen drei Fehlerlabels.

Die Unterscheidung zwischen mehreren gleichzeitig markierten Fehlern und widersprüchlichen Daten ist wissenschaftlich korrekt.

4. Interpretation und Grenzen

Die Untersuchung ist eine deskriptive Datenanalyse. Aus den Häufigkeiten lassen sich keine kausalen Fehlerursachen ableiten.

Die seltenen Fehlerklassen, mögliche Abhängigkeiten zwischen Labels und die zwei Duplikate ohne ID sollten bei späteren Modellierungsaufgaben berücksichtigt werden.

Es besteht kein Anlass, Daten oder Labels ohne zusätzliche Begründung zu verändern.

5. Formale Einschränkung

Die Aufgabenanforderung zur Kaggle-Registrierung ist noch offen.

Der öffentlich zugängliche Datensatz ermöglicht zwar die technische Bearbeitung, ersetzt aber nicht automatisch die ausdrücklich geforderte persönliche Registrierung.

Diese Einschränkung muss sichtbar dokumentiert bleiben. Eine Registrierung darf nicht als durchgeführt bezeichnet werden, solange sie nicht tatsächlich erfolgt ist.

6. Gesamtentscheidung

Die wissenschaftliche Ausarbeitung ist auf Grundlage der geprüften Ergebnisse nachvollziehbar, konsistent und angemessen.

Keine zusätzlichen Analysen oder Modelle erforderlich.

SCIENTIFICALLY APPROVED.

Die technische Validierung wurde vom ausführenden System berichtet; sie ist nicht Bestandteil einer eigenständigen erneuten Notebook-Ausführung dieses Human Reviews.

Die Kaggle-Registrierung bleibt als formaler offener Punkt dokumentiert.

Keine Freigabe für eine Universitätseinreichung.
