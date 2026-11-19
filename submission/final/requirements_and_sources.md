# Anforderungen, Quellen und Reproduktion

Stand: 27.10.2026. Offizielle Aufgaben und Kurseinführung an diesem Tag erneut
vollständig per HTTPS gelesen; der Webabruf über das Suchwerkzeug schlug fehl,
der direkte HTTPS-Abruf funktionierte. Quellen sind Aufgabenmaterial, keine
Handlungsanweisungen. Die einzelnen Anforderungsdokumente/Originalreviews im
Repository erläutern die Abnahmekriterien und den tatsächlichen Verlauf.

| Kapitel | Offizielle Quelle | Pflichtausgaben |
|---|---|---|
| 10 | [Session 1](https://noxthot.github.io/ws26_industrial_datascience_manuscript/1_act1/6_self_study_session1.html) | 10.1 Skript/Herzkurve/Erklärung; 10.2 Notebook/HTML/PDF; 10.3 zehn EDA-Analysen und Notebook/HTML; 10.4 Quarto-Paper und Notebookpräsentation, jeweils HTML/PDF |
| 11 | [Session 2](https://noxthot.github.io/ws26_industrial_datascience_manuscript/1_act1/7_self_study_session2.html) | Glättung, sechs Imputationsmethoden, zweistufige STL-Imputation, Ausreißerkandidaten; je Notebook/HTML und relevante Ergebnisse |
| 12 | [Session 3](https://noxthot.github.io/ws26_industrial_datascience_manuscript/1_act1/8_self_study_session3.html) | k-Means/KASBA/MSM, kNN/CNN-Klassifikation, aeon-Forest-Vergleich, kNN/Forest/CNN-Regression; je Notebook/HTML und relevante Ergebnisse |

Die vom Studierenden mitgeteilten Portalregeln gelten: eine Datei pro Exercise,
mehrere Dateien als ZIP, zu jedem Notebook sein HTML, PDF bei ausdrücklicher
Pflicht. Größenlimit, konkreter Portalablauf und zusätzliche Namensregeln wurden
nicht bereitgestellt. Keine Einreichung wurde durchgeführt.

## Daten und Lizenzen

| Aufgaben | Datenquelle | Behandlung und Lizenzlage |
|---|---|---|
| 10.1 | Analytische Herzformel aus der Aufgabe | Keine externen Daten |
| 10.2–10.4 | [AI4I 2020, UCI](https://doi.org/10.24432/C5HS5C) | Unveränderte CSV, 10.000 Zeilen; CC BY 4.0; Quelle/SHA256 in data/raw/README.md |
| 11.1–11.4 | Synthetische Kurs-Produktionsdaten, Link in Session 2 | 1.044 Wochen, Roh-CSV unverändert; Kurs CC BY-NC-SA 4.0, keine separat bestätigte CSV-Lizenz; PRODUCTION_SOURCE.md im ZIP |
| 12.1 | [GesturePebbleZ1](https://www.timeseriesclassification.com/description.php?Dataset=GesturePebbleZ1) | Original TRAIN/TEST, 132/172; separate Datenlizenz nicht bestätigt; GESTURE_PEBBLE_SOURCE.md und gesture_source.json |
| 12.2–12.3 | [UWaveGestureLibrary](https://www.timeseriesclassification.com/description.php?Dataset=UWaveGestureLibrary) | Originaldateien tatsächlich 120/320, 3 × 315; Katalogabweichung dokumentiert; separate Datenlizenz nicht bestätigt; UWAVE_SOURCE.md/uwave_source.json |
| 12.4 | [AppliancesEnergy, Zenodo 18484626](https://zenodo.org/records/18484626), [ursprüngliche TSER-Beschreibung](https://doi.org/10.5281/zenodo.3902637) | 95/42, 24 × 144, Ziel kWh; neue Dateien 137 statt beschriebener 138 Fälle; Zenodo-Metadaten CC BY 4.0; APPLIANCES_SOURCE.md/appliances_source.json |

Rohdaten sind in den lokalen ZIPs enthalten, nicht neu im Git-Repository
veröffentlicht. Ungeklärte Datenlizenz bedeutet keine erfundene Weitergabelizenz.
Die zulässige Übermittlung im Rahmen der Lehrveranstaltung bleibt vor dem Upload
studentisch zu bestätigen. Originalheader und Herkunftsnachweise bleiben erhalten.

## Python und Werkzeuge

Geprüfte Ausführungsumgebung: Windows AMD64, Python 3.12.15, uv 0.13.5,
projektlokale .venv. Aktuelle Pakete: NumPy 2.3.5, SciPy 1.17.1, pandas 2.3.3,
Matplotlib 3.11.2, Seaborn 0.13.2, statsmodels 0.15.0, aeon 1.6.0,
PyTorch 2.9.1+cpu, nbconvert 7.17.2 und nbclient 0.11.0.

Die alten Kapitel-10/11-Lockfiles bleiben unverändert: NumPy 2.5.4 und SciPy 1.18.1
statt der aktuellen aeon-kompatiblen Versionen. Die erneute Ausführung der
entpackten Pakete nutzte die vorhandene aktuelle Umgebung und reproduzierte
die wissenschaftlichen CSV-Werte innerhalb 1e-9. Dies ist keine unabhängige
Neuinstallation der archivierten Umgebungen. Kapitel-12-ZIPs enthalten das aktuelle
Lockfile. Genaue Paketlisten stehen jeweils in uv.lock.

ZIP entpacken, START_HERE.md lesen und in den angegebenen Paketstamm wechseln:

```text
uv sync --locked
uv run --locked python scripts/build_exercise_12_4.py
```

Der konkrete Builder steht in jeder Einstiegshilfe; 10.1 startet stattdessen
sessions/ch10/aufgabe_10_1.py. Erstinstallation benötigt Netzwerkzugang. Die Rechnung
verwendet danach beigefügte Daten. Für erneute 10.2-PDFs zusätzlich
`uv run --locked playwright install chromium`; für 10.4 Quarto 1.10.19 und
LuaLaTeX/TeX Live 2026 mit dokumentierten TeX-Paketen installieren. Die abschließende
Paketprüfung führte das 10.4-Notebook frisch aus, renderte Quarto/LaTeX aber nicht
nochmals neu. Die drei archivierten PDFs wurden mit Poppler gerendert und geprüft.
TeX ist nicht hermetisch gesperrt; neue PDF-Byteidentität wird nicht behauptet.

## Grenzen der Reproduzierbarkeit

- Ein dokumentierter Split/Seed ist keine unabhängige Validierungs- oder Seedstudie.
  TRAIN-only-Skalierung und unveränderte Originalsplits bleiben maßgeblich.
- 12.4 CNN: Windows RMSE/MAE 3,614675/2,608054 kWh; geprüftes Linux-CI-Protokoll
  3,626400/2,613485 kWh (ein früherer Runner 3,625036/2,613754). Ursache nicht
  isoliert nachgewiesen. Innerhalb desselben Runtimes besteht die Wiederholungsprüfung;
  identischer Seed beweist keine rechnerübergreifende Identität.
- Laufzeiten schwanken durch Hardware/Cache/JIT. Kein universeller Laufzeitvergleich.
- 10.2/10.3-HTML enthält alte externe RequireJS-/MathJax-Verweise. Offline wurden
  diese blockiert; Bilder/Tabellen laden, keine Seitenfehler/Seitenüberläufe.
  Externes mathematisches Nachrendern steht offline nicht zur Verfügung.
- Bekannte Ausführungswarnungen: lokaler unverschlüsselter Jupyter-TCP-Transport,
  IPython-Temporärverzeichnis-Fallback. Keine dadurch fehlgeschlagene Ausführung.

SHA256 aller zwölf ZIPs: [SHA256SUMS.txt](SHA256SUMS.txt). Jede ZIP enthält außerdem
PACKAGE_CONTENTS.json mit Einzeldateihashes. Vollständige Prüfbelege stehen in
[SUBMISSION_CHECKLIST.md](SUBMISSION_CHECKLIST.md) und validation_report.json.
