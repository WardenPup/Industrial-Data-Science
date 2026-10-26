# Aufgabe 10.4: Anforderungen und Redaktionsplan

Quelle: [offizielle Session 1](https://noxthot.github.io/ws26_industrial_datascience_manuscript/1_act1/6_self_study_session1.html), vollständig abgerufen am 26.10.2026.

## Abnahmekriterien

1. Eigenständige `.qmd` mit ausführbarem Python-Code und Abbildungen aus 10.3.
2. Chunk-Optionen für verborgenen Code und Abbildungsgrößen; einklappbarer Code in HTML.
3. Quarto-Exporte der QMD nach HTML und PDF.
4. Präsentationsfassung des bisherigen Notebooks mit ergänzenden Erläuterungen;
   auch diese direkt durch Quarto nach HTML und PDF exportieren.
5. Alle Berechnungen aus den unveränderten, SHA256-geprüften AI4I-Daten;
   bestehende Ladefunktion und IQR-Methode wiederverwenden.

## Zusätzlicher Auftrag: wissenschaftlicher Erstentwurf

Deutsch; etwa 4–6 Seiten Haupttext; Abstract mit 100–150 Wörtern; Ziel,
Daten/Methoden, Ergebnisse, Diskussion, Fazit und verifizierte Quellen.
Drei ausgewählte Abbildungen: Verteilungen, Boxplots und Drehmoment/Drehzahl.
Eine Korrelationstabelle ersetzt eine inhaltlich redundante Heatmap.
Pearson und IQR in LaTeX erläutern; Spearman als Rangmaß ergänzen.
PDF über eine echte LaTeX-Engine erzeugen, kein Browser-PDF als Ersatz.
Keine Kausalität, keine UDI-Zeitinterpretation, keine ungeprüfte Übertragung auf
reale Maschinen. Quellen und KI-Beitrag offenlegen.

Die ausführliche Scientific Writing Policy steht bereits unverändert in AGENTS.md.
Sie wird für diesen Auftrag angewendet. Text, Abbildungsauswahl und Interpretation
sind ein KI-Erstentwurf, keine eigenständige studentische Autorschaft.
Status bis zum tatsächlichen studentischen Review: **AWAITING HUMAN REVIEW**.

## Vorgehen und Abgrenzung

Branch `exercise/10.4` basiert auf dem freigegebenen Stand `c9c58ab` von 10.3.
PR #3 bleibt ungemergt: der aktuelle Auftrag enthält keine Merge-Freigabe.
Originalnotebook und studentische Reviews bleiben unverändert. Die separate
Präsentationskopie enthält die zehn Analysen, der kurze Hauptbericht nur drei
ausgewählte Figure-Gruppen. Vier Exporte sind deshalb zu prüfen.

Lokal wurden Quarto/Pandoc nicht im PATH gefunden; MiKTeX LuaLaTeX 1.24.0 ist
vorhanden. Quarto wird projektlokal eingerichtet. Erst danach werden Render- und
Layoutprüfungen protokolliert. Keine Veröffentlichung, kein Push oder neuer PR
ohne ausdrücklichen Auftrag; keine Einreichung.
