# Industrial Data Science – Self-Study Kapitel 10–12

Lokales Lernprojekt. Aufgaben 10.1–10.4 sind nach studentischen Reviews,
ausdrücklichen Freigaben und technischen Prüfungen vollständig in main integriert.
Die offizielle Aufgabenstellung hat Vorrang vor eigenen Zusammenfassungen.

## Start in PowerShell

Nach dem Klonen im Projektstamm einmal ausführen (Windows x64, Internet nötig):

```powershell
.\scripts\bootstrap.cmd
```

Das Skript installiert uv 0.13.5 aus dem offiziellen Astral-Release projektlokal,
erzeugt Python/.venv aus dem Lockfile und installiert Chromium für PDF-Exporte.
Es ändert keinen globalen PATH. Danach:

```powershell
.\scripts\uv.cmd sync --locked
.\scripts\uv.cmd run --locked python sessions/ch10/aufgabe_10_1.py
.\scripts\uv.cmd run --locked python scripts/download_ai4i.py
.\scripts\uv.cmd run --locked python -m unittest discover -s tests -v
```

Die ersten Downloads benötigen Internet. Danach kann mit `--offline` gearbeitet werden,
sofern Python und Pakete bereits lokal vorhanden sind. `uv.toml` hält den
Cache im Projekt. Der Wrapper `scripts/uv.cmd` setzt lokale Pfade für verwaltetes
Python, Chromium und Jupyter. Er verwendet projektlokales uv oder ersatzweise uv aus PATH.
`.venv` ist die isolierte Laufzeit; `uv.lock` fixiert Paketversionen.
Beim Umzug auf einen anderen Rechner .venv neu durch `sync` erzeugen, nicht kopieren.

Auf Linux/macOS uv gemäß offizieller Anleitung installieren, dann `uv sync --locked`.
Vor Browserinstallation und Export `PLAYWRIGHT_BROWSERS_PATH="$PWD/.tools/playwright"`
setzen und `uv run --locked playwright install chromium` ausführen.
Die Windows-Einrichtung wird lokal geprüft; Linux/macOS sind hier nicht getestet.

## Jupyter und Exporte

```powershell
.\scripts\uv.cmd run --locked jupyter lab
# Alternativ: klassisches Notebook-Frontend
.\scripts\uv.cmd run --locked jupyter notebook
# Kernel-Ausführung und HTML/PDF-Export mit synthetischem Testnotebook prüfen
.\scripts\uv.cmd run --locked python scripts/check_notebook_tools.py
```

In VS Code `.venv` als Notebook-Kernel wählen. JupyterLab verwendet bereits die
projektlokale Umgebung; eine globale Kernel-Registrierung ist nicht nötig.
Der Werkzeugtest schreibt ausschließlich nach `outputs/tooling-smoke/` (Git-ignoriert).
Für spätere, bereits ausgeführte Notebooks stehen folgende Exporte bereit:

```powershell
.\scripts\uv.cmd run --locked jupyter nbconvert --to html path/to/notebook.ipynb
.\scripts\uv.cmd run --locked jupyter nbconvert --to webpdf path/to/notebook.ipynb
```

`webpdf` nutzt Playwright/Chromium und benötigt keine LaTeX-Installation.
Der getrennte `--to pdf`-Exporter benötigt Pandoc/XeLaTeX und ist hier nicht eingerichtet.
Quarto und dessen HTML/PDF-Werkzeugkette werden für Aufgabe 10.4 separat eingerichtet.
Notebook-Server nur lokal verwenden; automatisch erzeugte Zugangstoken nicht veröffentlichen.

## Aufgabe 10.2 reproduzieren

```powershell
.\scripts\uv.cmd run --locked python scripts/download_ai4i.py
.\scripts\uv.cmd run --offline --locked python scripts/build_exercise_10_2.py
.\scripts\uv.cmd run --offline --locked python scripts/validate_notebooks.py
```

Notebook: [ai4i_explore.ipynb](sessions/ch10/ai4i_explore.ipynb).
Ausgaben unter `outputs/ch10/exercise_10_2/`: `ai4i_explore.html`, `ai4i_explore.pdf`,
`torque_over_udi.png` und `summary_statistics.csv`.
Das Buildskript führt einen frischen Kernel aus und aktualisiert das Notebook
mit echten Ausgaben. JupyterLab wurde lokal gestartet und per authentifiziertem
HTTP-Aufruf geprüft; danach wurde der temporäre Server gestoppt.
Rohdaten sind nicht enthalten: Download aus UCI mit fester SHA256-Prüfung,
Herkunft und CC-BY-4.0-Lizenz unter `data/raw/README.md`.
UDI ist kein Zeitstempel; die 10.000 synthetischen Zeilen erlauben keine
unbegründeten Aussagen über reale Maschinen oder Kausalität.

Der ursprüngliche Infrastrukturtest ist weiterhin synthetisch und getrennt von 10.2.

## Aufgabe 10.3 reproduzieren

```powershell
.\scripts\uv.cmd sync --locked
.\scripts\uv.cmd run --locked python scripts/download_ai4i.py
.\scripts\uv.cmd run --offline --locked python scripts/build_exercise_10_3.py
.\scripts\uv.cmd run --offline --locked python -m unittest discover -s tests -v
```

[Seaborn-Notebook](sessions/ch10/ai4i_seaborn.ipynb) und HTML unter
`outputs/ch10/exercise_10_3/ai4i_seaborn.html`; dort liegen auch zehn PNG-Figuren,
Korrelations-/IQR-Tabellen, Bin-Häufigkeiten, Grenzen und ein Bildmanifest.
Die drei Histogramme, Boxplots und Violinplots sind jeweils als drei Teilachsen
zusammengefasst. Die offizielle 10.3-Aufgabe verlangt keinen PDF-Export.
[Review 10.3](reviews/exercise_10_3.md): APPROVED nach bestätigter CI-Bedingung.
PR #3 wurde nach ausdrücklicher Erlaubnis und erfolgreichen Head-Checks regulär gemergt.

## VS Code

Ordner über **Datei → Ordner öffnen** öffnen. Als Interpreter
`.venv/Scripts/python.exe` auswählen, falls VS Code eine Auswahl verlangt.
Über **Terminal → Task ausführen** stehen Synchronisierung, Plot und Tests bereit.
Die Python-Erweiterung ist lokal installiert. Jupyter und Codex werden in
`.vscode/extensions.json` empfohlen; das ist keine automatische Installation.
Die vorhandene Codex-Desktop-App/CLI kann bereits mit diesem Projekt arbeiten.
Für die IDE-Erweiterung ist eine eigene Anmeldung in VS Code erforderlich.

## Aufbau

- `AGENTS.md`: dauerhafte Arbeitsregeln für KI-Unterstützung.
- `sessions/ch10/`: freigegebene 10.1-Lösung und 10.2-Notebook mit Datenprüfung.
- `sessions/ch11/`, `sessions/ch12/`: vorbereitete Kapitel mit Quellenlinks.
- `tests/`: mathematische Prüfungen und echter PNG-Export.
- `outputs/ch10/`: erzeugte Herzkurve sowie 10.2-HTML/PDF, Grafik und Statistik.
- `data/raw/`, `data/processed/`: spätere Originaldaten und Ableitungen.
- `docs/`: Status, Umgebung und wiederverwendbarer Arbeitsauftrag.
- `scripts/`: Bootstrap, uv-Wrapper und Notebook-/Export-Werkzeugtest.

GitHub-Commit/Push nur bei ausdrücklichem Auftrag; nie automatische Universitätsabgabe.
Virtuelle Umgebungen, Browser, Caches, Zugangsdaten und Rohdaten sind nicht Teil des Commits.

## Human-AI review

Use `exercise/<number>` branches and the cycle documented in
[Human-AI workflow](docs/HUMAN_AI_WORKFLOW.md). Start review records from
[the template](reviews/TEMPLATE.md). The current [10.1 review](reviews/exercise_10_1.md)
records genuine provenance, technical evidence and explicit approval.
The [10.2 review](reviews/exercise_10_2.md) records explicit student approval;
PR #2 was subsequently merged after explicit authorization.
Conventional Commits include explicit AI-Assistance and Human-Review metadata.
Configure the editor template with `git config --local commit.template .gitmessage`.

GitHub Actions runs Python and QA tests, the 10.1 script, prospective commit-message
checks, tracked notebook validation/execution and a synthetic HTML/PDF export check.
All tracked notebooks are executed in fresh kernels; required exports are also checked.
Green checks never imply student approval. The workflow neither approves nor merges.
The original solution already exists on main; its published history is preserved.

## Wissenschaftlicher Quarto-Bericht (10.4)

Der editierbare deutsche Erstentwurf liegt unter
[`reports/exercise_10_4/paper.qmd`](reports/exercise_10_4/paper.qmd).
Eine separate Präsentationskopie erhält die vollständige EDA aus 10.3.
[Render-Anleitung](reports/exercise_10_4/README.md),
[Anforderungen](docs/EXERCISE_10_4_REQUIREMENTS.md) und
[offene Reviewfragen](reviews/exercise_10_4.md) dokumentieren die Trennung von
KI-Erstentwurf, tatsächlichen technischen Prüfungen und studentischer Redaktion.
Status: **APPROVED** nach zwei studentischen PDF-Reviews,
KI-gestützten Korrekturen und erfolgreicher technischer Prüfung.
Finale wissenschaftliche Freigabe und Merge-Erlaubnis: 26.10.2026.
PR #4 ist nach PR #3 regulär gemergt; sämtliche Reviewcommits sind erhalten. Die Exporte liegen unter
`outputs/ch10/exercise_10_4/`; PDF wird über Quarto und LuaLaTeX erzeugt.
Die bestehenden Actions prüfen Python und Notebooks. Die zusätzliche Quarto-/TeX-
Exportprüfung erfolgt lokal und ist nicht Bestandteil der bisherigen CI.

## Quellen

- [Offizielle Session 1 / Kapitel 10](https://noxthot.github.io/ws26_industrial_datascience_manuscript/1_act1/6_self_study_session1.html), abgerufen 25.10.2026.
- [uv: Installation](https://docs.astral.sh/uv/getting-started/installation/) und [Projekte](https://docs.astral.sh/uv/guides/projects/).
- [nbconvert: Export-Abhängigkeiten](https://nbconvert.readthedocs.io/en/latest/install.html).
- [Codex IDE-Erweiterung](https://learn.chatgpt.com/docs/codex/ide).
- [OpenAI: Projektanweisungen mit AGENTS.md](https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex).


## Kapitel 10 abgeben – noch kein Upload

Vier geprüfte lokale ZIP-Dateien liegen unter `submission/chapter_10/`.
Die [Abgabecheckliste](submission/chapter_10/CHECKLIST.md) nennt jede enthaltene
Datei sowie ZIP-Größen und SHA256. [Abgaberegeln](docs/SUBMISSION_RULES_CHAPTER_10.md)
unterscheiden die ausdrücklich mitgeteilten Hochschulregeln von den offiziellen
Aufgabenquellen. Der reproduzierbare Packager liest den geprüften Git-Snapshot:

```powershell
scripts/uv.cmd run --offline --locked python scripts/prepare_chapter_10_submission.py --source-ref 740ed55675d7b12830941700d860d3f5bd17a405
```

Er prüft Archive und führt die entpackten Notebooks in der vorhandenen gesperrten
Projektumgebung aus. Poppler und das vorhandene Playwright-Chromium werden für
PDF-/Offline-HTML-QA benötigt. ZIPs enthalten direkt relevante Quellen, Exporte,
Reproduktionsdateien und UCI-Daten mit Lizenz; keine installierten Werkzeuge.
Die vorbereiteten ZIPs sind lokal Git-ignoriert und werden nicht automatisch
an die Universität übermittelt.

## Aufgabe 11.1 – rollende Glättung

Kapitel 10 bleibt unverändert freigegeben. Der ausdrücklich autorisierte
Kapitel-11-Start umfasst nur 11.1: [Notebook](sessions/ch11/production_smoothing.ipynb),
[Anforderungen](docs/EXERCISE_11_1_REQUIREMENTS.md),
[Review](reviews/exercise_11_1.md). Status: **AWAITING HUMAN REVIEW**.

```powershell
scripts/uv.cmd run --locked python scripts/download_production.py
scripts/uv.cmd run --offline --locked python scripts/build_exercise_11_1.py
```

HTML und zwei Grafiken liegen unter `outputs/ch11/exercise_11_1/`, die abgeleitete
CSV unter `data/processed/`. Median und Mittelwert werden mit fünf zentrierten
Wochen verglichen; alle 367 ursprünglichen Lücken bleiben erhalten.
Keine Imputation, keine Arbeit an 11.2 und kein Merge vor studentischem Review.
