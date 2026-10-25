# Industrial Data Science – Self-Study Kapitel 10–12

Lokales Lernprojekt. Aufgabe 10.1 ist implementiert; weitere Aufgaben folgen einzeln.
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

Aufgabe 10.2 wird erst nach Review von 10.1 begonnen. Der Infrastrukturtest enthält
keine AI4I-Daten und ist keine Lösung zu 10.2.

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
- `sessions/ch10/`: Skript und erläuterte Lösung zu 10.1.
- `sessions/ch11/`, `sessions/ch12/`: vorbereitete Kapitel mit Quellenlinks.
- `tests/`: mathematische Prüfungen und echter PNG-Export.
- `outputs/ch10/`: erzeugte Herzkurve.
- `data/raw/`, `data/processed/`: spätere Originaldaten und Ableitungen.
- `docs/`: Status, Umgebung und wiederverwendbarer Arbeitsauftrag.
- `scripts/`: Bootstrap, uv-Wrapper und Notebook-/Export-Werkzeugtest.

GitHub-Commit/Push nur bei ausdrücklichem Auftrag; nie automatische Universitätsabgabe.
Virtuelle Umgebungen, Browser, Caches, Zugangsdaten und Rohdaten sind nicht Teil des Commits.

## Human-AI review

Use `exercise/<number>` branches and the cycle documented in
[Human-AI workflow](docs/HUMAN_AI_WORKFLOW.md). Start review records from
[the template](reviews/TEMPLATE.md). The current [10.1 review](reviews/exercise_10_1.md)
records genuine provenance, technical evidence and pending human decisions.
Conventional Commits include explicit AI-Assistance and Human-Review metadata.
Configure the editor template with `git config --local commit.template .gitmessage`.

GitHub Actions runs Python and QA tests, the 10.1 script, prospective commit-message
checks, tracked notebook validation/execution and a synthetic HTML/PDF export check.
No tracked notebooks currently exist: that check reports SKIP, not a notebook pass.
Green checks never imply student approval. The workflow neither approves nor merges.
The original solution already exists on main; its published history is preserved.

## Quellen

- [Offizielle Session 1 / Kapitel 10](https://noxthot.github.io/ws26_industrial_datascience_manuscript/1_act1/6_self_study_session1.html), abgerufen 25.10.2026.
- [uv: Installation](https://docs.astral.sh/uv/getting-started/installation/) und [Projekte](https://docs.astral.sh/uv/guides/projects/).
- [nbconvert: Export-Abhängigkeiten](https://nbconvert.readthedocs.io/en/latest/install.html).
- [Codex IDE-Erweiterung](https://learn.chatgpt.com/docs/codex/ide).
- [OpenAI: Projektanweisungen mit AGENTS.md](https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex).
