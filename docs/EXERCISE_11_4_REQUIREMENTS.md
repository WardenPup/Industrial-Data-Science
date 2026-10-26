# Aufgabe 11.4 – Anforderungen

KI-gestützte Analyse, Quellenabruf 26.10.2026:
https://noxthot.github.io/ws26_industrial_datascience_manuscript/1_act1/7_self_study_session2.html
Methodenbeispiel im Manuskript:
https://noxthot.github.io/ws26_industrial_datascience_manuscript/1_act1/2_1_timeseries_decomposition.html

## Offizielle Anforderungen
Die vollständige Originalspalte `pieces` verwenden, mit einer geeigneten Methode
Ausreißer identifizieren, Originalreihe und Ausreißer mit Seaborn visualisieren,
die Anzahl bestimmen und das Ergebnis diskutieren. Es wird keine Sollanzahl genannt.

## Lernziel und Umsetzung
Trend und Saison von ungewöhnlichen Abweichungen unterscheiden. Robuste additive
STL auf den unveränderten 1.044 Originalwochen; anschließend Drei-Sigma-Regel
auf den Residuen wie im Methodenbeispiel (Stichprobenstandardabweichung, ddof=1,
strikte Grenzüberschreitung). Keine Glättung oder Imputation aus 11.1–11.3 als Eingabe.
STL-Annahmen: Periode 52, Saisonfenster 13, Trendfenster 101, Tiefpass 53,
robust=True; keine behauptete Parameteroptimalität. Vorhandene Bibliotheken genügen.

## Daten, Ergebnisse und Abnahme
Unveränderte checksumgeprüfte `data/raw/sss1_production_data.csv`, Herkunft und
Lizenzgrenzen in `data/raw/PRODUCTION_SOURCE.md`. Erwartet werden eine Seaborn-Grafik
der Originalreihe mit markierten Kandidaten sowie eine Residuen-Grafik mit Grenzen,
eine Kandidatentabelle und die tatsächlich berechnete Anzahl. Keine vorgegebene Anzahl.
Tests prüfen Grenzlogik, Indexzuordnung, additive Identität und Datenintegrität.
Notebook frisch sequenziell ausführen, beide Grafiken visuell prüfen, HTML offline
öffnen und Checksummen dokumentieren. Frühere Lösungen bleiben unverändert.

## Grenzen
Die Drei-Sigma-Regel ist eine Heuristik, kein Fehlernachweis oder kalibrierter Test.
Residualverteilung, Abhängigkeit, Randbereiche und STL-Parameter beeinflussen die
Markierungen. 52 Wochen approximieren ein Jahr. Keine bekannte Fehler-Ground-Truth,
keine automatische Entfernung, keine Prognose oder kausale Erklärung.

## Abgabe
Eine Datei pro Aufgabe; bei mehreren Dateien ZIP. Jedes eingereichte Notebook muss
seinen HTML-Export enthalten. Notebook, HTML und erforderliche lokale Python-Module
sowie Datenquelle/Umgebungsangaben sind zusammen zu berücksichtigen. Die Aufgabe
fordert kein PDF. Aktuell nur Entwicklungsartefakte; kein Upload, kein Abgabepaket.

Status: REQUIREMENTS ANALYZED; Human Review ausstehend.
