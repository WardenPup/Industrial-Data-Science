# Exercise 10.3 review

Status: AWAITING HUMAN REVIEW
Human review: Pending

## Requirements and provenance

Official instructions and acceptance criteria: `docs/EXERCISE_10_3_REQUIREMENTS.md`.
Starting commit: merged main `40b31c64b88d9441be3ac9eb71433bdb49b7e4f9`.
PR #2 was merged only after explicit student merge authorization and inspection
of both successful current-head checks. Its commits and student text are preserved.

Codex performs requirements analysis, implementation and technical checks for 10.3.
No student review, feedback or approval of this exercise has been received.

## Verification

Actual local verification on 2026-10-26, Python 3.12.15, pandas 2.3.3,
Matplotlib 3.11.2, Seaborn 0.13.2, SciPy 1.18.1:

| Command | Actual outcome |
|---|---|
| `scripts/uv.cmd run --offline --locked python scripts/download_ai4i.py` | Existing official CSV SHA256 verified |
| `scripts/uv.cmd sync --offline --locked` | 107 installed packages checked |
| `scripts/uv.cmd run --offline --locked python -m unittest discover -s tests -v` | Initially 17 passed; after the IQR regression test, all 18 passed |
| `scripts/uv.cmd run --offline --locked python scripts/build_exercise_10_3.py` | 12 code cells executed sequentially; ten real notebook PNG outputs and ten embedded HTML figures |
| `scripts/uv.cmd run --offline --locked python scripts/validate_notebooks.py` | Both tracked notebooks validated and executed in fresh kernels |
| `.venv/Scripts/python.exe .tools/check_exercise3_html.py` | Offline browser render succeeded; all ten images decoded; tables and page fit a 1400-pixel viewport |

The task-local HTML helper also captured representative page sections, which
Codex inspected. All ten PNG figures were separately inspected for titles,
units, labels, legends, clipping and interpretability. Histogram/box/violin
figures each contain all three measurement panels; the pairplot contains the
three-variable grid. PNG sizes/nonblank content and all ten manifest checksums
were verified. A fresh notebook rerun reproduces the saved PNG checksums.
No notebook error or stderr output is saved. The existing local TCP kernel
warning is still emitted externally during kernel startup.

### Actual computed results and limits

All 10000 rows are retained; `numeric` has only the three measurement columns.
Torque/speed is the strongest pair: Pearson −0.8750270863, Spearman −0.9164741739.
The scatter/pairplot shows a curved negative monotonic relation. Temperature
correlations are small, which is not proof of independence or no physical effect.
Torque is roughly symmetric/bell-shaped, speed right-skewed, and temperature
irregular/multihumped. No normality or causal claim is made.

IQR flags with explicit floating-point tolerance: 64 Torque, 418 speed, 0 air.
Skewness: −0.0095166 / 1.9931710 / 0.1142739 respectively.
Equal-width speed-bin counts: 8965 / 975 / 60; ten torque-bin counts sum to 10000.
Correlations, IQR statistics, counts and exact bin edges are saved as CSV/JSON.
The plotted regression is descriptive, without an inferential confidence band.
Bins, KDE bandwidth, overplotting, arbitrary row ordering and the synthetic
source constrain the interpretation. UDI is not a timestamp.

### Genuine correction during validation

The first execution generated all plots and passed its existing tests. Manual
numerical inspection then found that decimal values on theoretical IQR fences
were flagged because 12.8 differs from 12.800000000000011 (and likewise 67.2).
Four lower-boundary and one upper-boundary values changed the naive torque
count from 69 to 64. An explicit absolute 1e-10 comparison tolerance and a tiny
boxplot-whisker expansion resolve this; a new boundary regression test passes.
The notebook discloses the choices. Stripplot color contrast was improved.
No test failure or student feedback is invented; this was AI technical correction.

### Outputs and requirement coverage

`sessions/ch10/ai4i_seaborn.ipynb` is executed. `outputs/ch10/exercise_10_3/`
contains the HTML, ten named PNGs, plot manifest, IQR/correlation tables and
bin counts/edges. Every figure group and observation question from the official
assignment is covered; see `docs/EXERCISE_10_3_REQUIREMENTS.md`.
No PDF is generated because Exercise 10.3 does not request it. Exercise 10.4
and its Quarto reporting work have not begun. Hosted checks must be inspected
on the draft PR after push; local results do not imply hosted success.

## Questions for student review

1. Do all requested plots and three-variable panels appear clearly in the notebook/HTML?
2. Can you distinguish a boxplot from a KDE violin and explain why an IQR flag is not a proven error?
3. What do Pearson, Spearman and the curved point cloud each describe about torque/speed?
4. How do unequal bin counts, jitter, KDE bandwidth and overplotting affect interpretation?
5. Which conclusions are precluded by synthetic data, absent timestamps and purely descriptive analysis?

## Human review and approval

Pending. Do not merge 10.3, start 10.4 or submit coursework.


# Human Review – Aufgabe 10.3

**Datum:** 26.10.2026  
**Aufgabe:** Explorative Datenanalyse des AI4I-Datensatzes mit Seaborn  
**KI-Unterstützung:** Codex  
**Review-Status:** Fachlich geprüft, Freigabe nach abschließender CI-Kontrolle

## 1. Prüfung der Visualisierungen

Die zehn bereitgestellten Diagrammgruppen wurden auf Verständlichkeit, Achsenbeschriftungen, Einheiten und Plausibilität geprüft.

- **Liniendiagramm:** Das Drehmoment schwankt über die UDI-Reihenfolge, ohne einen eindeutigen Trend. UDI wird korrekt als Zeilenkennung und nicht als Zeit interpretiert.
- **Histogramme:** Das Drehmoment ist annähernd symmetrisch um 40 Nm verteilt. Die Drehzahl zeigt eine rechtsschiefe Verteilung mit einzelnen hohen Werten. Die Lufttemperatur weist mehrere Häufigkeitsbereiche auf.
- **Boxplots:** Median, Quartile und Ausreißer sind erkennbar. Besonders bei der Drehzahl treten zahlreiche Werte außerhalb der 1,5-IQR-Grenzen auf.
- **Violinplots:** Die geglätteten Verteilungen stimmen qualitativ mit den Histogrammen überein. Im Gegensatz zu Boxplots machen sie die Verteilungsdichte sichtbar.
- **Scatterplot und Pairplot:** Zwischen Drehzahl und Drehmoment besteht ein deutlich negativer, nichtlinearer Zusammenhang. Für die Lufttemperatur ist kein vergleichbar ausgeprägter Zusammenhang erkennbar.
- **Korrelationsmatrix:** Die Pearson-Korrelation zwischen Drehmoment und Drehzahl beträgt -0,875. Die Korrelationen mit der Lufttemperatur liegen nahe null (-0,014 bzw. 0,023).
- **Regressionsdarstellung:** Die nahezu horizontale Regressionslinie zwischen Lufttemperatur und Drehmoment entspricht der sehr schwachen linearen Korrelation.
- **Stripplot:** Die Einteilung in drei Drehzahlbereiche zeigt abnehmende Drehmomentwerte bei steigender Drehzahl.
- **Countplot:** Die meisten Drehmomentwerte liegen in den mittleren Intervallen. Sehr kleine und sehr große Werte kommen deutlich seltener vor.

Die Abbildungen sind insgesamt gut lesbar und sinnvoll beschriftet.

## 2. Fachliches Verständnis

**Boxplot und Violinplot:**  
Ein Boxplot zeigt Median, Quartile, Streuung und mögliche Ausreißer nach der 1,5-IQR-Regel. Ein Violinplot ergänzt Informationen über die geschätzte Verteilungsdichte. Seine Form hängt von der verwendeten Glättung ab.

**Korrelation und Nichtlinearität:**  
Die starke negative Pearson-Korrelation zwischen Drehmoment und Drehzahl zeigt einen deutlichen statistischen Zusammenhang. Der Scatterplot verdeutlicht zusätzlich dessen nichtlineare Form. Eine Pearson-Korrelation beschreibt nur die lineare Komponente eines Zusammenhangs.

**Ausreißer:**  
Werte außerhalb der 1,5-IQR-Grenzen sind statistisch auffällig, aber nicht automatisch Messfehler. Sie sollten ohne weitere Begründung nicht entfernt werden.

**Binning:**  
Die Einteilung in Intervalle erleichtert Vergleiche und Häufigkeitsdarstellungen. Allerdings gehen dabei Detailinformationen verloren. Die Ergebnisse hängen von den gewählten Intervallgrenzen ab.

## 3. Grenzen der Analyse

Der AI4I-Datensatz enthält synthetische Daten. Die beobachteten Zusammenhänge lassen sich deshalb nicht ohne Weiteres auf reale Maschinen übertragen.

Die Diagramme und Korrelationskoeffizienten beschreiben statistische Muster, beweisen aber keine kausalen Wirkungen. UDI ist keine Zeitvariable.

Auch die Wahl der Histogrammintervalle, Drehzahlklassen und KDE-Glättung beeinflusst die Darstellung.

## 4. Technische Validierung

Laut Codex wurden folgende Prüfungen durchgeführt:

- 18 automatisierte Tests erfolgreich.
- 12 Code-Zellen nacheinander ausgeführt.
- Zehn Diagrammgruppen erzeugt und visuell geprüft.
- HTML-Export mit eingebetteten Abbildungen erstellt.
- GitHub Actions für den Branch erfolgreich.

Die separat gestartete Pull-Request-CI war zum Zeitpunkt des Codex-Berichts noch nicht abgeschlossen.

Diese technischen Ergebnisse werden als KI-gestützte beziehungsweise automatisierte Prüfungen dokumentiert, nicht als eigenständig lokal ausgeführte studentische Tests.

## 5. Gesamtbewertung

Die bereitgestellten Visualisierungen sind nachvollziehbar und fachlich plausibel. Die statistischen Ergebnisse passen zu den dargestellten Verteilungen und Zusammenhängen.

Die Grenzen der Aussagekraft wurden berücksichtigt. Bei der fachlichen Prüfung der bereitgestellten Ergebnisse wurden keine wesentlichen Fehler festgestellt.

**Human Review: Fachlich positiv.**

Die endgültige Freigabe erfolgt nach erfolgreicher Kontrolle aller GitHub-Actions-Prüfungen. Bis dahin bleibt Pull Request #3 ungemergt.
