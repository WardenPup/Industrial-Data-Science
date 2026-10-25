# Arbeitsstand – 25.10.2026

## Aufgabe 10.1: technisch geprüft, fachliches Review ausstehend

| Anforderung | Umsetzung / Nachweis |
|---|---|
| uv installieren | Offizielles Astral-Windows-Release projektlokal; `uv --version`: 0.13.5 |
| Projekt und virtuelle Umgebung | pyproject.toml, .python-version, uv.lock; `uv sync` erzeugt .venv |
| NumPy und Matplotlib installieren | NumPy 2.5.4 und Matplotlib 3.11.2 in .venv |
| Vorgeschriebene Kurve zeichnen | sessions/ch10/aufgabe_10_1.py; vollständige Periode mit linspace |
| Funktionsweise erklären | sessions/ch10/aufgabe_10_1.md mit Herleitung und Lernfragen |

Ausgeführte Abschlussprüfung:

```text
uv sync --offline --locked: erfolgreich, 12 installierte Pakete geprüft
uv run --offline --locked python -m unittest discover -s tests -v:
  4 Tests, OK
uv run --offline --locked python sessions/ch10/aufgabe_10_1.py:
  outputs/ch10/aufgabe_10_1_herz.png erzeugt
```

Die Befehle wurden mit `.tools/uv/uv.exe` ausgeführt.
Geprüft wurden Viertelperiodenpunkte, Periodenschluss, Achsensymmetrie,
endliche Werte, ungültige Punktzahlen und ein tatsächlich lesbarer PNG-Export.
Bild (1120 × 1120 Pixel) visuell kontrolliert: vollständige Herzkurve,
lesbare Achsen/Titel, gleiche Achsenskalierung, keine abgeschnittenen Inhalte.
Interpreter: Python 3.12.15 unter `.venv/Scripts/python.exe`;
`sys.prefix != sys.base_prefix` bestätigt die aktive Isolation.

Die ersten Prüfungen deckten ein nicht unterstütztes uv-Konfigurationsfeld und
einen nicht beschreibbaren globalen Matplotlib-Cache auf. Beide sind behoben:
uv-Konfiguration enthält nur unterstützte Felder; Matplotlib verwendet
standardmäßig `.tools/matplotlib`. Die Abschlussprüfung lief ohne diese Fehler.

## Weitere Aufgaben

- 10.2–10.4: offen (Notebook/AI4I, Seaborn, Quarto).
- Kapitel 11 und 12: Ordner und offizielle Links vorbereitet; noch nicht gelöst.
- Keine Einreichung oder Übertragung an ein Kursportal erfolgt. Der GitHub-Push
  wurde im Folgeauftrag ausdrücklich beauftragt.

## Lokale Werkzeuge und Grenzen

- VS Code 1.133.0 (x64): Version und Erweiterungsliste per unterstützter CLI geprüft.
- Installiert: Python, Pylance, Python Debugger, Python Environments, PlantUML, Containers.
- Codex-CLI: 0.163.0-alpha.10.2; `codex --help` geprüft, Option `--cd` vorhanden.
- Codex-Desktop-App: diese aktive Projektarbeit belegt Datei- und Terminalzugriff.
- Codex-IDE und Jupyter-Erweiterung: nicht installiert; Empfehlungen im Projekt.
- VS-Code-Tasks und Einstellungen: JSON erfolgreich eingelesen; enthaltene
  uv-Befehle im Terminal ausgeführt. Die grafische Task-Oberfläche wurde nicht bedient.
- Codex-CLI meldet innerhalb der Sandbox fehlendes Home-Verzeichnis für PATH-Aliase;
  Version und Hilfe funktionieren. Eine separate interaktive CLI-Anmeldung wurde nicht geprüft.
- Keine globalen Codex-Einstellungen oder automatischen Freigaben verändert.
- uv wurde als offizielles vorgebautes ZIP installiert, ohne globalen PATH-Eintrag.
- Die frühere Chat-Antwort war nur als Inhaltsreferenz verfügbar, nicht als lesbarer Plan.
  Die konkrete Umsetzung stützt sich daher auf den aktuellen Auftrag und die Originalaufgabe.

## Erweiterung zum vollständigen Notebook-Arbeitsplatz

- Originalaufgabe erneut direkt abgerufen und in `docs/CHAPTER_10_REQUIREMENTS.md`
  als Anforderungsübersicht dokumentiert.
- Python auf 3.12.15 in `.python-version` festgelegt. Lockdatei enthält auch
  Notebook, JupyterLab, ipykernel, nbconvert mit WebPDF/Playwright und PDF-Leseprüfung.
- JupyterLab 4.6.4, Notebook 7.6.3, ipykernel 7.4.0 und nbconvert 7.17.2 nachgewiesen.
- Projektlokales Chromium samt Headless Shell erfolgreich installiert.
- `scripts/bootstrap.cmd` mit vorhandener uv-Installation erfolgreich ausgeführt:
  Lockfile synchronisiert, Browserinstallation bestätigt. Der Download-Zweig des
  Bootstrap-Skripts wurde nicht separat in einer leeren Installation getestet;
  uv wurde zuvor erfolgreich aus dem offiziellen Release heruntergeladen.
- Alle vier 10.1-Tests und das Plot-Skript über den endgültigen `scripts/uv.cmd`-Wrapper
  erfolgreich ausgeführt. Herzkurve erneut visuell geprüft.
- `scripts/check_notebook_tools.py` tatsächlich ausgeführt: synthetischer Kernel-Code
  ergibt 4, HTML exportiert, einseitiges PDF exportiert und mit pypdf gelesen.
  PDF mittels Poppler gerendert und visuell geprüft; keine abgeschnittenen Inhalte.
- Jupyter erkennt `python3` aus `.venv/share/jupyter/kernels/python3`.
- Ein erster Exportlauf erfolgte vor Abschluss des Browserdownloads und scheiterte
  entsprechend; nach fertiger Installation erfolgreich wiederholt.
- Ein Windows-ZMQ-Ereignisschleifenproblem wurde durch eine lokale Selector-Schleife
  für die Kernel-Ausführung behoben. Die Abschlussprüfung meldet weiterhin den
  Hinweis des Kernels auf unverschlüsselten lokalen TCP-Transport; Ausführung und
  Exporte sind erfolgreich. Die grafische Notebook-Oberfläche wurde nicht geprüft.
- Windows PowerShell blockiert `.ps1`-Dateien lokal. Die endgültigen `.cmd`-Launcher
  benötigen keine Änderung der Ausführungsrichtlinie und wurden erfolgreich geprüft.
- VS-Code-Tasks verwenden diese Launcher; JSON wurde validiert, die grafische
  Task-Oberfläche wurde nicht bedient.
- HTML/PDF-Export erfolgt über nbconvert/WebPDF. Quarto/Pandoc/TeX sind bewusst noch
  nicht installiert; deren Einrichtung gehört zu der weiterhin offenen Aufgabe 10.4.
- Remote `https://github.com/WardenPup/Industrial-Data-Science.git` geprüft: keine
  vorhandenen Referenzen. Lokales Repository mit Branch `main` und `origin` initialisiert.
- Aufgabe 10.2 bleibt bis zum ausdrücklichen Review von 10.1 unbegonnen.

## Human-AI QA adoption

Workflow adoption is on `exercise/10.1`. Baseline `d243632` remains unchanged on main.
The supplied responsible-AI rules are appended to AGENTS.md; review templates,
PR checklist, Conventional Commit disclosure checks and read-only CI are added.
The configured commit editor template is `.gitmessage` (local Git setting).
Repository authentication and push permission were verified with existing credential
management; no tokens were written to the project or displayed.

Local checks: nine tests pass, Exercise 10.1 executes, the synthetic notebook
executes and exports HTML/PDF, and tracked-notebook validation explicitly skips
because no notebooks are tracked. Detailed commands, failures and limitations are
in `reviews/exercise_10_1.md`. Hosted CI must be inspected separately in the draft PR.

Status at workflow adoption: AWAITING_HUMAN_REVIEW. No earlier stages were fabricated.

## Human review completion (2026-10-26)

The student manually supplied verification, explicit approval and four explanation
answers. Their exact additions are preserved in review commit `42cebaf`.
Codex then checked the official requirements, reran all nine local tests, regenerated
the heart and verified PNG dimensions/DPI, and reran the synthetic notebook exports.
Tracked-notebook validation explicitly skips because no notebooks are tracked.

Current exercise status: APPROVED; merge authorization remains withheld.
Fresh hosted CI results are shown in PR #1. The student text is unchanged; AI
status reconciliation and a terminology clarification are recorded separately.
No merging, deletion, submission or Exercise 10.2 work has been performed.

## Approved 10.1 merge and start of 10.2 (2026-10-26)

The user explicitly authorized merging PR #1 and starting Exercise 10.2.
Both current-head GitHub checks were verified successful before the merge.
PR #1 was merged using a merge commit `5c2ac0d`, preserving all original commits
and genuine student review contributions. Local main was fast-forwarded to it.
Branch `exercise/10.2` starts from that synchronized main.

Exercise 10.1: approved and merged. Exercise 10.2: requirements analysis underway;
no human approval. Exercise 10.3: not started. Earlier status paragraphs above
describe their historical stage, not the current merge authorization.
