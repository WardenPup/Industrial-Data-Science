# Kapitel 10 – Abgaberegeln und Quellen

Stand: 26.10.2026. Kein Upload und keine automatische Universitätseinreichung.

## Tatsächlich vorliegende Abgaberegeln

Im aktuellen Nutzerauftrag wurden folgende Hochschulvorgaben ausdrücklich mitgeteilt:
1. Genau eine Abgabedatei pro Aufgabe.
2. Bei mehreren benötigten Dateien ein ZIP verwenden.
3. Jedes eingereichte `.ipynb` benötigt seinen HTML-Export.
4. PDF-Exporte beilegen, wenn die Aufgabe sie ausdrücklich fordert.

Daraus folgen vier ZIP-Dateien für 10.1–10.4. Jedes Paket behält die ursprünglichen
relativen Projektpfade und enthält eine aufgabenspezifische README mit Ausführung,
Abhängigkeiten und KI-Transparenz. Nur direkt relevante Lösungen, Reproduktions-
dateien, Exporte und Originaldaten/Lizenznachweise werden aufgenommen.
Virtuelle Umgebungen, Caches, Git-Metadaten, temporäre Builds, Zugangsdaten,
Binärwerkzeuge und unnötige interne Entwicklungsskripte sind ausgeschlossen.

## Offizielle Aufgaben und tatsächlich gelesene Quellen

- Kapitel 10: https://noxthot.github.io/ws26_industrial_datascience_manuscript/1_act1/6_self_study_session1.html
- Kurseinführung: https://noxthot.github.io/ws26_industrial_datascience_manuscript/0_introduction/0_introduction.html
- Kursindex: https://noxthot.github.io/ws26_industrial_datascience_manuscript/

Alle drei Seiten am 26.10.2026 tatsächlich über HTTPS gelesen; lokale Abrufkopien
unter `.tools/` sind Prüfnachweise, kein Bestandteil der Abgabe. Das Webwerkzeug
konnte die Seiten nicht öffnen, der normale Python-HTTPS-Abruf war erfolgreich.
Die öffentlich verfügbaren Seiten enthalten keine weiteren konkreten Portalregeln.
Eine Portal-URL, Dateigrößenlimits, Fristen oder zusätzliche Namensvorgaben wurden
nicht bereitgestellt; hierzu werden keine Angaben erfunden. Die ausdrücklich
mitgeteilten Regeln sind für diese Vorbereitung maßgeblich.

10.1 benötigt Python-Skript, Herleitung und erzeugte Grafik. 10.2 verlangt das
Notebook sowie HTML und PDF. 10.3 verlangt die zehn EDA-Analysen; der beigefügte
HTML-Export erfüllt zusätzlich die Notebook-Abgaberegel, PDF ist nicht gefordert.
10.4 enthält QMD und Präsentationsnotebook, jeweils mit HTML und PDF.

## Daten und Reproduktion

UCI: https://archive.ics.uci.edu/dataset/601/ai4i+2020+predictive+maintenance+dataset
DOI: https://doi.org/10.24432/C5HS5C . Lizenz: CC BY 4.0,
https://creativecommons.org/licenses/by/4.0/ . Quellen-/Lizenzseite am
26.10.2026 erneut tatsächlich gelesen. Die unveränderte CSV ist in 10.2–10.4
enthalten, einschließlich Quellenangabe und SHA256. 10.1 benötigt keine Rohdaten.
`pyproject.toml`, `uv.lock`, uv-Konfiguration und Python-Version erhalten die
bestehende Umgebungsspezifikation. Nur unmittelbar benötigte Reproduktionsskripte
und wissenschaftliche Hilfsmodule sind beigefügt; installierte Werkzeuge fehlen
absichtlich. Quarto/LuaLaTeX sind externe Voraussetzungen für erneutes Rendern.

Die vollständige Dateiliste steht in `submission/chapter_10/CHECKLIST.md`, jede
Archivdatei mit Bytezahl und SHA256 in `submission_manifest.json`. Die ZIPs werden
aus dem wissenschaftlich geprüften Merge-Snapshot 740ed55 erstellt; nachfolgende
Dokumentationscommits verändern ihre fachlichen Inhalte nicht.
