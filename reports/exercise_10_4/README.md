# Wissenschaftlicher Erstentwurf – Aufgabe 10.4

Status: **AWAITING HUMAN REVIEW**. Keine studentische Endredaktion behauptet.

`paper.qmd` ist der kurze, direkt editierbare Bericht. Die ergänzende
`notebook_presentation.ipynb` ist eine eigenständige Präsentationskopie der
zehn Analysen aus 10.3. Das Originalnotebook bleibt unverändert. Beide Quellen
werden mit Quarto nach HTML und PDF gerendert, nicht mit nbconvert/WebPDF.

## Reproduzieren (Projektstamm)

Voraussetzungen: gesperrte Python-Umgebung (`scripts/bootstrap.cmd`), verifizierte
Rohdaten (`scripts/uv.cmd run python scripts/download_ai4i.py`), Quarto **1.10.19**
und eine funktionsfähige LuaLaTeX-Installation mit den von Quarto benötigten
Paketen. Lokaler Nachweis: MiKTeX 25.12, LuaHBTeX 1.24.0.
Quarto enthält Pandoc. Python-Pakete werden ausschließlich projektlokal verwaltet.

```powershell
scripts/uv.cmd run --offline --locked python scripts/build_exercise_10_4.py
scripts/uv.cmd run --offline --locked python -m unittest discover -s tests -v
```

Der Builder verwendet `.tools/quarto/bin/quarto.exe`, sonst `quarto` im PATH.
Er setzt den Projektinterpreter explizit und rendert jedes Dokument frisch mit
`--execute`. Ausgaben stehen unter `outputs/ch10/exercise_10_4/`.
`validation_manifest.json` hält Quarto-/Python-Version und Dateiprüfsummen fest.
Das LaTeX-Zwischenformat bleibt zur Kontrolle des Satzwegs erhalten.

Offizielles portables Windows-Release:
https://github.com/quarto-dev/quarto-cli/releases/tag/v1.10.19
SHA256 des verwendeten ZIP:
`a9c62e4fef34ea05d4dd9175d905f80f0542414a1ae17a9d45698f6646c01173`
mit der offiziellen Prüfsummenliste verglichen. Binärwerkzeuge bleiben Git-ignoriert.

Die vorhandene TeX-Distribution ist eine externe Systemvoraussetzung; sämtliche
TeX-Pakete sind nicht im Python-Lockfile enthalten. Dies ist keine hermetische
TeX-Umgebung. Zur Werkzeugbedienung wurden die offiziellen Quarto-Dokumentationen
zu Jupyter, Chunk-Optionen und PDF geprüft (26.10.2026).

HTML demonstriert einklappbaren Code; im Hauptteil ist Code verborgen.
Mathematik wird für HTML als MathML und im PDF mit LuaLaTeX gesetzt.
Die endgültige Abbildungsauswahl, fachliche Interpretation und sprachliche
Überarbeitung müssen im studentischen Review bestätigt oder geändert werden.
