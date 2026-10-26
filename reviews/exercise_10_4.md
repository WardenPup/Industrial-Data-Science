# Aufgabe 10.4 – Human-AI-Review

Status: **AWAITING HUMAN REVIEW**.

## Auftrag und Herkunft

Die Scientific Writing Policy aus dem aktuellen Benutzerauftrag und AGENTS.md
bestimmt diesen wissenschaftlichen Erstentwurf. Es gibt noch keine studentische
Überarbeitung, endgültige Abbildungsauswahl oder Freigabe für 10.4. Frühere
Reviews betreffen 10.1–10.3 und werden nicht auf diesen Bericht übertragen.

## KI-Beiträge

Codex: Anforderungsanalyse, vollständiger deutscher Textentwurf, vorläufige Auswahl
von drei Abbildungsgruppen, Korrelationstabelle, Formeln und Quellenverwaltung,
Python-Hilfsmodul, separate Präsentationskopie des Notebooks, Quarto-Konfiguration,
Builder und unabhängige numerische Tests. Die studentischen Originaldateien
und das Originalnotebook von 10.3 wurden nicht inhaltlich bearbeitet.

Der Haupttext ist editierbar in `reports/exercise_10_4/paper.qmd`.
Die drei Darstellungen beantworten unterschiedliche Fragen; die numerische
Korrelationstabelle vermeidet eine zusätzliche Heatmap desselben Befunds.
Die notebookbasierte vollständige EDA bleibt als separater Begleitexport erhalten.

## Automatisierte Prüfung (26.10.2026)

- `scripts/uv.cmd run --offline --locked python -m unittest discover -s tests -v`:
  20 Tests erfolgreich. Zwei neue Prüfungen vergleichen Pearson mit NumPy,
  Spearman mit SciPy sowie IQR-Markierungen mit exakter Dezimalarithmetik.
- `scripts/uv.cmd run --offline --locked python scripts/validate_notebooks.py`:
  alle drei getrackten Notebooks in frischen Kerneln ausgeführt; keine Fehler.
- Datenintegrität: vorhandener Loader prüft SHA256, 10.000 Zeilen, vier Spalten,
  keine fehlenden Werte und eindeutige Kennungen. Keine Zeilen entfernt.
- Die erste HTML-Fassung enthält drei echte PNG-Abbildungen, 19 MathML-Elemente,
  einen einklappbaren Codeabschnitt und vier aufgelöste Literaturangaben.
  Abstract: 127 Wörter. Offline-Browsertest: Bilder dekodieren, Code aufklappbar.

### Tatsächliche Probleme während der Umsetzung

Der erste Quarto-Lauf scheiterte an einem nicht beschreibbaren normalen
Benutzercache; der autorisierte Lauf verwendet die regulären Werkzeugrechte.
Danach wurde ein ungültiger `execute-dir`-Wert durch `project` ersetzt und die
Projektwurzel im Python-Code explizit ermittelt. Eine visuelle HTML-Prüfung
zeigte zu breite PNG-Ausgaben; responsive Bildbreiten wurden ergänzt.
Die Präsentationskopie schreibt in einen eigenen Ausgabeordner, damit sie
keine Artefakte der freigegebenen 10.3 überschreibt.
Ein Diagnoseausdruck mit griechischem rho scheiterte allein an der Windows-
Terminalkodierung; die HTML-Tabelle selbst enthält das korrekte Zeichen.

Die vorhandene MiKTeX-Installation lieferte während der Erstinitialisierung
keinen abgeschlossenen PDF-Build (Fontdatenbank/fehlende Pakete). Der Lauf wurde
beendet; anschließend wurde Quarto TinyTeX v2026.10 ohne PATH-Änderung installiert.
Der erfolgreiche Satz verwendet LuaHBTeX 1.24.0 (TeX Live 2026).
Eine im PDF fehlende griechische Tabellenüberschrift wurde durch echtes
LaTeX-Math ersetzt. Eine zu breite IQR-Tabelle im Notebook wurde kompakter
präsentiert; die vollständigen Berechnungen bleiben im CSV erhalten.
Veraltete Statussätze aus der KI-Einleitung von 10.3 wurden in der neuen Kopie
ersetzt, damit keine 10.4-Freigabe suggeriert wird.

Zwei Prüfannahmen des neuen Builders waren zu streng: Quarto speichert echte
Notebook-Outputs zurück, und PDF-Textextraktion fügt bei Versalien manchmal
Kerning-Leerzeichen ein. Die Prüfung vergleicht nun Zellquellen statt identischer
Notebookbytes und normalisiert Leerzeichen für den Statusnachweis. Eine
Quarto-Warnung zur Bereinigung außerhalb des Projektordners wurde durch einen
internen Renderordner mit anschließender Exportkopie behoben.

### Abschlussnachweise

Die folgenden endgültigen Prüfungen sind tatsächlich ausgeführt worden:

```text
scripts/uv.cmd run --offline --locked python -m unittest discover -s tests -v
  Ran 21 tests in 0.616s: OK
scripts/uv.cmd run --offline --locked python scripts/build_exercise_10_4.py
  paper: 3 HTML-Abbildungen, 5 PDF-Seiten, 3 LaTeX-Abbildungseinbindungen
  notebook_presentation: 10 HTML-Abbildungen, 10 PDF-Seiten, 10 LaTeX-Einbindungen
  12 Notebook-Codezellen lückenlos ausgeführt; keine Fehleroutputs
  QMD-Text und Notebook-Zellquellen unverändert
scripts/uv.cmd run --offline --locked python scripts/check_exercise_10_4_html.py
  beide HTML-Dateien offline bei 1400 und 900 Pixeln geprüft: PASS
  alle 3 bzw. 10 Bilder dekodiert, Seiten/Bilder/Tabellen innerhalb des Viewports
  einklappbarer Code funktioniert, 4 Quellen aufgelöst, Abstract im Zielumfang
```

Die PDF-Metadaten weisen beide Dateien als `LuaTeX-1.24.0` aus. Der Bericht
enthält teilweise Vektorgrafiken: Die Anzahl eingebetteter Rasterbilder ist
deshalb kein verlässlicher Zähler der Abbildungen. Der Builder prüft zusätzlich
die LaTeX-Einbindungen und die drei Bildunterschriften. Alle fünf Berichtsseiten
und alle zehn Notebookseiten wurden mit Poppler nach PNG gerendert und von
Codex visuell kontrolliert: Formeln, Tabellen, Diagramme, Farbskala, Bildunterschriften
und Literatur sind lesbar; die zuvor gefundenen Überläufe sind behoben.
Die mehrseitige Häufigkeitstabelle im Begleitnotebook wiederholt ihren Kopf.
Dies ist eine KI-Sichtprüfung, keine studentische Beobachtung.

Die vier Exporte und ihre Prüfsummen stehen in `validation_manifest.json`.
`tex_packages.tsv` dokumentiert 326 installierte Paketrevisionen aus der lokalen
TeX-Live-Paketdatenbank; die optionale `tlmgr --data`-Abfrage scheiterte zuvor
an der Windows-Aufrufsyntax und wurde nicht als erfolgreicher Nachweis gewertet.
Die letzte vollständige Ausgabe ist fehlerfrei. Der lokale Kernel meldet weiterhin
den bekannten Hinweis auf unverschlüsselten lokalen TCP-Transport.
`git diff --cached --check` meldete ausschließlich von Quarto erzeugte
Leerzeichen am Zeilenende in den beiden HTML-Exporten. Diese Artefakte bleiben
unverändert, damit ihre Prüfsummen stimmen; die Prüfung aller übrigen Dateien
mit `git diff --cached --check -- . ':(exclude)outputs/ch10/exercise_10_4/*.html'`
war erfolgreich. Es werden keine wissenschaftlichen Fehler dadurch ausgenommen.

Alle offiziellen Kriterien sind technisch abgedeckt: QMD mit ausgeführtem Code,
verborgenem Code und Abbildungsgrößen, aufklappbarer HTML-Code, HTML/PDF der QMD
sowie ergänzte Notebook-Präsentation direkt mit Quarto nach HTML/PDF.
Der kurze Bericht umfasst fünf Seiten insgesamt, drei Abbildungen, eine
Korrelationstabelle und die geforderten wissenschaftlichen Abschnitte.

### Grenzen der technischen Freigabe

Die Python-Umgebung ist gesperrt, Quarto auf 1.10.19 festgelegt; die TeX-
Paketrevisionen sind dokumentiert, jedoch nicht hermetisch installiert oder
automatisch gegen ein historisches Paketarchiv gesperrt. Bitidentische PDFs
auf anderen Rechnern werden nicht behauptet. Die bestehenden GitHub Actions
decken Python/Notebooks ab, nicht diesen neuen Quarto-/LaTeX-Export. Für den
rein lokalen Branch wurde kein neuer Hosted-CI-Lauf ausgelöst oder behauptet.
Institutionelle Detailvorgaben zur KI-Kennzeichnung wurden nicht zusätzlich
bereitgestellt; die vorliegende Offenlegung folgt AGENTS.md und dem Auftrag.

## Studentisches Review – noch offen

Hier werden noch keine studentischen Beobachtungen oder Freigaben festgehalten.
Bitte den Entwurf selbst überarbeiten und insbesondere beurteilen:

1. Entspricht die Fragestellung Ihrem Verständnis und Ihrer Schwerpunktsetzung?
2. Tragen Verteilungen, Boxplots und Streudiagramm jeweils eine eigene Aussage?
   Möchten Sie eine Abbildung ersetzen oder entfernen? Eine Heatmap ist bewusst
   zugunsten der präziseren Korrelationstabelle entfallen.
3. Können Sie Pearson gegenüber Spearman und den Umgang mit exakten IQR-Grenzen
   in eigenen Worten erklären? Sind die Formeln und Einheiten verständlich?
4. Sind die Aussagen zu Krümmung, schwacher Temperaturkorrelation und fehlendem
   Kausalitätsnachweis angemessen vorsichtig?
5. Überarbeiten Sie insbesondere Fragestellung, Ergebnisinterpretationen,
   Diskussion und Fazit so, dass sie Ihre eigenen fachlichen Entscheidungen
   und Formulierungen widerspiegeln. Bestätigen oder ändern Sie die Auswahl
   der drei Abbildungen und die Grenzen der synthetischen Daten.
6. Sind Formeln, Diagramme, Tabelle, Bildunterschriften und Quellen in beiden
   Exportformaten gut lesbar? Gibt es zusätzliche Hochschulregeln zur KI-Nutzung,
   Zitierweise oder Namensangabe, die ergänzt werden müssen?

## Git und Veröffentlichung

Eigener Branch `exercise/10.4`, abhängig vom unverändert erhaltenen 10.3-Stand
`c9c58ab`. PR #3 bleibt ungemergt. Für diesen Auftrag ist weder ein Push noch
eine neue Pull Request oder Universitätseinreichung genehmigt. Lokale Commits
tragen `AI-Assistance: Codex` und `Human-Review: Pending`.
Keine Freigabe von 10.4, kein fingiertes Review, keine Historienumschreibung.
