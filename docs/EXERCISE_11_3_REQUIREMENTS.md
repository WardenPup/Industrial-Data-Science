# Aufgabe 11.3 – Anforderungen und Abnahmekriterien

Offizielle Aufgaben-/Methodenquellen, tatsächlich per HTTPS gelesen am 26.10.2026:
- https://noxthot.github.io/ws26_industrial_datascience_manuscript/1_act1/7_self_study_session2.html
- https://noxthot.github.io/ws26_industrial_datascience_manuscript/1_act1/2_1_timeseries_decomposition.html
- https://www.statsmodels.org/stable/generated/statsmodels.tsa.seasonal.STL.html

KI-gestützte Analyse; Umsetzung bis zum Human-Review-Gate ausdrücklich beauftragt.

## Lernziel und genau geforderte Schritte

STL (Seasonal and Trend decomposition using LOESS) zur saisonbereinigten
Imputation einer Wochenreihe nachvollziehen, ohne unbekannte Werte als Messung
auszugeben. Die offizielle Aufgabe fordert:
1. Geglättete Reihe mit Lücken aus 11.1 als Eingabe.
2. Einfache vorläufige Imputation, damit STL vollständige Daten erhält.
3. STL-Zerlegung in Trend, Saison und Residuum.
4. Darstellung mit der bereitgestellten seasonal_decompose_seaborn-Funktion.
5. Saison von der ursprünglichen geglätteten Reihe mit Lücken abziehen.
6. Diese weiterhin lückenhafte saisonbereinigte Reihe einfach imputieren.
7. Geschätzte Saisonkomponente wieder addieren.
8. Endergebnis mit plot_production_data darstellen und diskutieren.

## Daten, Verfahren und geplante Ergebnisse

Unveränderte offizielle synthetische Produktions-CSV; gleiche Hash-/Kalender-
prüfung und freigegebener 5-Wochen-Median aus 11.1. Reuse load_smoothed_input
und lineare impute_series aus 11.2. Kein Lesen/Optimieren anhand unbekannter
Ground Truth. Vorhandene 10.x-/11.1-/11.2-Lösungsdateien bleiben unverändert.
statsmodels ist zusätzlich für die ausdrücklich geforderte STL nötig und wird
ausschließlich projektlokal über uv/pyproject.toml/uv.lock ergänzt.

Geplant: linear ergänzen, additives STL mit period=52, seasonal=13, trend=101,
low_pass=53 und robust=True; dokumentierte Iterationen. 52 Wochen approximieren
ein Jahr, sind keine exakt kalenderjährliche Saison. seasonal=13 ist das
LOESS-Fenster der saisonalen Teilreihen, nicht ein 13-Wochen-Jahreszyklus.
Nach Saisonabzug erneut linear innerhalb bekannter Randwerte ergänzen. Bekannte
Medianwerte explizit erhalten, um Rundungsänderungen durch Subtraktion/Addition
zu vermeiden. Kein erneutes Glätten und keine iterative STL-Optimierung.

Die Aufgabe nennt keine festen STL-Zielzahlen. Erwartete Invarianten aus der
tatsächlichen Eingabe: 1.044 Wochen; vorab 367 NaNs und 677 bekannte Werte;
STL-Eingabe und Endergebnis endlich; nach Saisonabzug identische 367-NaN-Maske;
alle 677 vorhandenen Werte unverändert. Additive Rekonstruktionsidentität und
tatsächliche Änderungen gegenüber einfacher Linearimputation berechnen, ohne
diese als Genauigkeitsgewinn zu bezeichnen.

Visualisierungen: vierteilige STL-Kursgrafik; Zwischenstufe mit Lücken;
dreiteilige Produktions-Kursgrafik; gezielter Vergleich an der ersten längsten
23-Wochen-Lücke. Achsen Datum und Stück pro Woche, getrennte Teilachsenskalen
offenlegen. Tabellen/CSV für Komponenten, Stufenprüfung und Differenzdiagnostik.

## Wissenschaftliche Grenzen

Saison wird auch aus vorläufig imputierten Werten geschätzt. Lange Ausfälle,
Periodenannahme, LOESS-Fenster und Ränder beeinflussen das Ergebnis. Robustheit
garantiert keine korrekte Rekonstruktion. Additivität ist eine Annahme; keine
Ground-Truth-Rangliste und keine unmittelbare Echtzeitprognose. Keine Arbeit an
11.4, insbesondere keine Ausreißerzählung der vollständigen Originalreihe.

## Abnahme und Abgabe

Analytische Tests für Maskenerhalt/Rundsaison-Schritte, künstliche additive
Referenz für STL-Identität, echte Daten-/Hashprüfung; alle relevanten bestehenden
Tests, Notebook frisch sequenziell, alle Figuren visuell und HTML offline prüfen.
Echte Befehle/Ergebnisse, KI-Beiträge und offene Grenzen in reviews/exercise_11_3.md.
Separate Analyse-, Implementierungs- und Prüfcommits, Draft-PR gegen main.
Status AWAITING HUMAN REVIEW; keine studentische Zustimmung erfinden.

Universitätsdateien: ausgeführtes ipynb plus HTML (bestehende Notebookregel),
direkt relevante Berechnungs-/Darstellungsdateien, CSV/Abbildungen, Quellen- und
Abhängigkeitsspezifikation für Reproduktion; bei späterer Abgabe mehrere Dateien
als ein ZIP. 11.3 fordert keinen PDF-Export. Noch kein Abgabepaket/Upload beauftragt.
