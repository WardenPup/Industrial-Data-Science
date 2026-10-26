# Aufgabe 11.3 – Human-AI-Review

Status: **AWAITING HUMAN REVIEW** (26.10.2026).
Noch kein studentisches Feedback, keine wissenschaftliche Freigabe und keine
Merge-Erlaubnis für 11.3. Keine Universitätseinreichung.

## Anforderungen und KI-Beitrag

Quellen, Lernziele, Abnahme und Abgabedateien stehen in
docs/EXERCISE_11_3_REQUIREMENTS.md (tatsächlich am 26.10.2026 gelesen).
Codex erstellte Anforderungen, Berechnung, Kursgrafik-Anpassungen, Notebook,
Export, Tests und technische Dokumentation. Keine menschlichen Beobachtungen
oder Tests erfunden. Wiederverwendet: freigegebener 11.1-Median/Hashprüfung,
lineare Interpolation aus 11.2 und Kurs-Produktionsplotfunktion.
Freigegebene Lösungen/Reviews und Rohdaten werden nicht verändert.

Zusätzlich erforderlich: statsmodels 0.15.0, ausschließlich projektlokal über
uv ergänzt und gelockt. Sechs neue Pakete einschließlich seiner Abhängigkeiten,
keine vorhandene Paketversion geändert. Beim ersten Add-Versuch interpretierte
der cmd-Wrapper die Versionszeichen als Umleitung; der Vorgang scheiterte.
Die selbst erzeugte temporäre Datei wurde entfernt, danach der vorhandene lokale
uv.exe direkt mit korrekt zitiertem Argument verwendet. Keine globalen Pakete.

## Anforderung für Anforderung

| Offizielle Aufgabe | Umsetzung |
|---|---|
| Geglättete Eingabe mit Lücken aus 11.1 | load_smoothed_input mit kanonischem Werte-/NaN-Hash |
| Vorläufig einfach imputieren | lineare Interpolation innerhalb bekannter Randwerte |
| STL zerlegen | additives STL, period 52, seasonal 13, trend 101, low_pass 53, robust True |
| Komponenten mit Kursfunktion darstellen | seasonal_decompose_seaborn, vier Teilbilder, deutsche Labels |
| Saison von lückenhafter Eingabe abziehen | source − seasonal; ursprüngliche 367-NaN-Maske erhalten |
| Saisonbereinigte Reihe imputieren | erneute lineare Interpolation, keine Wiederverwendung der gefüllten Vorstufe |
| Saison zurückaddieren | completed + seasonal, bekannte 677 Medianwerte exakt erhalten |
| Endgrafik und Diskussion | dreiteilige Kursgrafik, Zwischenstufe und Langlückenvergleich |

## Tatsächliche Ergebnisse

1.044 Wochen, 677 bekannte und 367 fehlende Medianwerte. STL-Vorstufe vollständig;
nach Saisonabzug wieder exakt 367 fehlende Werte an identischen Positionen.
Endergebnis endlich und vollständig, alle 677 bekannten Werte exakt erhalten,
keine negativen Ergänzungen. Additive Rekonstruktionsabweichung maximal
1,1368683772161603e-13 Stück pro Woche. Mittlere absolute Differenz gegenüber
einfacher Linearimputation an den 367 Fehlwochen: 9,746198652352929; Maximum:
75,2469305103034 Stück pro Woche. Diese Größen messen keine Genauigkeit.
Im 23-Wochen-Ausschnitt 11.12.2011–13.05.2012 fällt die STL-gestützte Kurve
anfangs unter den linken Stützwert und liegt später über der linearen Schätzung.
Das ist eine beobachtete Schätzform, kein Beleg für den wahren Verlauf.

## Tatsächlich ausgeführte technische Prüfung

- `scripts/uv.cmd sync --offline --locked`: 117 Pakete aufgelöst, 113 installierte geprüft.
- `scripts/uv.cmd run --offline --locked python -m unittest discover -s tests -v`:
  37 Tests, 1,331 s, OK. Vier neue Tests: bekannte Saison/analytisch linearer Trend,
  Masken/Nichtmutation, Ausrichtung/Randlücken/zu kurze Reihe, synthetische
  additive Rekonstruktion sowie reale Eingabe-/Stufeninvarianten.
- `scripts/uv.cmd run --offline --locked python scripts/build_exercise_11_3.py`:
  sieben Codezellen frisch sequenziell 1–7, vier echte eingebettete PNGs dekodiert.
  Gespeicherte CSV, Rohdaten-/Eingabehash, Maskengleichheit, bekannte Werte,
  additive Identität und Rückaddition an Fehlstellen erfolgreich geprüft.
  Nach Präzisierung des Beobachtungstextes erneut vollständig gerendert.
- `scripts/uv.cmd run --offline --locked python scripts/check_exercise_11_3_html.py`:
  Offline-Chromium bei 900/1400 px: vier Bilder geladen, keine Seitenfehler und
  kein horizontaler Überlauf. Alle vier PNGs visuell kontrolliert; Datum,
  Stück-pro-Woche-Einheiten, Legenden und unterschiedliche Komponentenskalen geprüft.
- Abschlussaudit vor Veröffentlichung: freigegebene Dateien/Originalreviews,
  Kapitel-10-ZIPs, Manifesthashes und unveränderte alte Paketversionen kontrolliert.

Bekannter lokaler Jupyter-TCP-Hinweis beim Kernelstart. Kein Test-, Notebook-
oder Exportfehler. GitHub-CI wird am tatsächlichen neuen PR-Head geprüft und
erst nach tatsächlichem Abschluss im PR als erfolgreich verlinkt.

## Artefakte

- sessions/ch11/production_stl_imputation.ipynb; neue Module stl_imputation.py / stl_plots.py.
- outputs/ch11/exercise_11_3/: production_stl_imputation.html,
  01_stl_components.png, 02_deseasonalized_gaps.png, 03_final_imputation.png,
  04_long_gap_comparison.png, components.csv, stage_missing_counts.csv,
  summary.json, validation_manifest.json.
- data/processed/exercise_11_3_stages.csv: lokale vollständige Stufenableitung,
  Git-ignoriert, mit dem Builder reproduzierbar.
- Bestehende Rohdatenquelle/Lizenzgrenze, aktualisierte Abhängigkeitsspezifikation;
  kein PDF gefordert. Kein Abgabepaket oder Upload erstellt.

## Grenzen und konkrete wissenschaftliche Reviewfragen

STL schätzt die Saison aus teilweise vorläufig imputierten Werten. Das Ergebnis
hängt von diesen Annahmen, langen Lücken, Rändern und LOESS-Fenstern ab.
52 Wochen approximieren ein Kalenderjahr; seasonal=13 ist ein LOESS-Fenster
auf saisonalen Teilreihen, kein 13-Wochen-Zyklus. Additivität und Fenster sind
nicht statistisch optimiert. Robuste Gewichtung und Rekonstruktionsidentität
beweisen keine inhaltlich richtige Zerlegung. Keine fehlerfreie Ground Truth,
Genauigkeitsverbesserung oder Unsicherheitsintervalle behauptet. Rückblickende
Analyse, keine unverändert zulässige Echtzeitprognose.

1. Ist die Trennung von vorläufiger Imputation und erneutem Arbeiten auf den
   ursprünglichen 367 Fehlstellen nachvollziehbar?
2. Sind additive Saison, 52-Wochen-Näherung und explizite LOESS-Fenster für den
   Bericht fachlich angemessen und verständlich begründet?
3. Wird klar zwischen Rekonstruktionsidentität, Methodenunterschied und
   unbekannter Genauigkeit unterschieden?
4. Welche Aussagen über die 23-Wochen-Lücke wären im Managementbericht vertretbar?

Keine Arbeit an 11.4, keine Freigabe für 11.3, kein Merge und keine Universitätseinreichung.
