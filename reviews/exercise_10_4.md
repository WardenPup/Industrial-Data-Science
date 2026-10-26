# Aufgabe 10.4 – Human-AI-Review

Status: **AWAITING FINAL HUMAN APPROVAL**.

Der folgende Erstentwurfsnachweis ist historisch. Das unveränderte studentische
Review vom 26.10.2026 und die anschließende KI-Korrektur sind unten dokumentiert.

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


# Human Review – Aufgabe 10.4

**Datum:** 26.10.2026  
**Aufgabe:** Wissenschaftlicher Bericht mit Quarto und LaTeX  
**Geprüfte Dokumente:** `paper.pdf`, `notebook_presentation.pdf`  
**KI-Unterstützung:** Codex  
**Review-Status:** CHANGES REQUESTED – Fachlich positiv, kleinere Überarbeitungen erforderlich

---

## 1. Ziel und Umfang der Prüfung

Ziel des Human Reviews ist die fachliche, wissenschaftliche und gestalterische Kontrolle der für Aufgabe 10.4 erstellten Dokumente.

Dabei wurde besonders darauf geachtet, dass der wissenschaftliche Bericht nicht nur die technischen Anforderungen erfüllt, sondern die angewandten Methoden und Ergebnisse verständlich erklärt.

Ein weiteres Ziel ist eine kompakte und nachvollziehbare Darstellung ohne unnötige Wiederholungen oder übermäßig komplexe Formulierungen.

Die Prüfung umfasst die beiden bereitgestellten PDF-Dokumente. Eine eigenständige lokale Ausführung sämtlicher Berechnungen wurde im Rahmen dieses Reviews nicht durchgeführt.

## 2. Wissenschaftlicher Aufbau des Papers

Der Hauptbericht umfasst fünf Seiten und besitzt eine nachvollziehbare wissenschaftliche Gliederung:

- Zusammenfassung und Fragestellung
- Daten und Methoden
- Ergebnisse
- Diskussion und Grenzen
- Fazit
- Transparenz, Reproduzierbarkeit und Literatur

Die Struktur ist für den Umfang der Aufgabe angemessen.

Besonders positiv ist, dass eine konkrete Fragestellung formuliert wird. Dadurch ergibt sich ein erkennbarer Zusammenhang zwischen Datenauswahl, Methodik und Ergebnissen.

Der Umfang ist sinnvoll begrenzt. Die Arbeit konzentriert sich auf drei ausgewählte Messgrößen und ihre statistischen Beziehungen, statt sämtliche verfügbaren Analysen unkommentiert zu übernehmen.

**Bewertung:** Aufbau und Umfang überzeugen. Keine grundlegende Umstrukturierung erforderlich.

## 3. Datengrundlage und Nachvollziehbarkeit

Der verwendete AI4I-Datensatz wird einschließlich Herkunft und synthetischer Natur beschrieben.

Im Paper werden 10.000 Beobachtungen und die vier Spalten UDI, Drehmoment, Drehzahl und Lufttemperatur angegeben.

Die physikalischen Einheiten sind korrekt zugeordnet:

- Drehmoment: Nm
- Drehzahl: rpm
- Lufttemperatur: K

Die Behandlung von UDI als Zeilenkennung und nicht als Zeitvariable ist wissenschaftlich richtig.

Positiv ist außerdem die Dokumentation einer SHA256-Integritätsprüfung und der Tatsache, dass keine Beobachtungen aufgrund statistischer Auffälligkeiten entfernt werden.

Die Datengrundlage ist ausreichend dokumentiert. Die angegebenen Datenkennzahlen stimmen mit den zuvor bereitgestellten Ergebnissen aus den Aufgaben 10.2 und 10.3 überein.

**Bewertung:** Fachlich nachvollziehbar und für eine reproduzierbare explorative Analyse geeignet.

## 4. Methodik und mathematische Darstellung

### 4.1 Deskriptive Statistik

Die Kombination aus Histogrammen, Boxplots, Streudiagramm und Korrelationskoeffizienten ist sinnvoll gewählt.

Jede Methode erfüllt einen erkennbaren Zweck:

Histogramme beschreiben Verteilungen, Boxplots zeigen Lage und Streuung, das Streudiagramm veranschaulicht paarweise Beziehungen und Korrelationen fassen bestimmte statistische Eigenschaften numerisch zusammen.

### 4.2 Interquartilsabstand

Die Formel

IQR = Q0,75 − Q0,25

ist korrekt und verständlich eingeführt.

Die verwendete 1,5-IQR-Regel wird nachvollziehbar erklärt. Die Unterscheidung zwischen statistisch auffälligen Werten und tatsächlich fehlerhaften Messungen ist besonders wichtig und wurde richtig umgesetzt.

Auch die Behandlung von Grenzwerten und numerischen Rundungseffekten ist dokumentiert.

### 4.3 Pearson- und Spearman-Korrelation

Die mathematische Definition des Pearson-Korrelationskoeffizienten ist korrekt dargestellt.

Die zusätzliche Verwendung der Spearman-Rangkorrelation ist sinnvoll, da zwischen Drehzahl und Drehmoment kein streng linearer Zusammenhang vorliegt.

Positiv ist die Erklärung, dass ein Unterschied zwischen Pearson und Spearman allein keinen formalen Nachweis von Nichtlinearität darstellt.

**Bewertung:** Die statistischen Methoden sind passend gewählt, korrekt erklärt und nicht unnötig kompliziert.

## 5. Prüfung der Abbildungen im Paper

### Abbildung 1 – Histogramme

Die drei Histogramme sind vollständig, gut lesbar und mit den richtigen Einheiten versehen.

Das Drehmoment zeigt eine annähernd symmetrische Verteilung mit Schwerpunkt um 40 Nm.

Die Drehzahl besitzt eine deutlich rechtsschiefe Verteilung mit wenigen sehr hohen Beobachtungswerten.

Die Lufttemperatur zeigt mehrere Häufigkeitsbereiche und keine einfache, eindeutig glockenförmige Struktur.

Die Interpretation im Text stimmt qualitativ mit den Darstellungen überein.

### Abbildung 2 – Boxplots

Die Boxplots stellen Median, Quartile und mögliche Ausreißer übersichtlich dar.

Die im Bericht genannten Ergebnisse sind:

- Drehmoment: 64 markierte Werte außerhalb der IQR-Grenzen
- Drehzahl: 418 markierte Werte
- Lufttemperatur: keine markierten Werte

Die dargestellten Unterschiede passen zu den Verteilungsformen.

Die Argumentation, dass besonders eine rechtsschiefe Verteilung zahlreiche Werte oberhalb der IQR-Grenze erzeugen kann, ist nachvollziehbar.

### Abbildung 3 – Drehmoment und Drehzahl

Diese Abbildung liefert aus meiner Sicht die wichtigste Erkenntnis des Papers.

Die Punktwolke zeigt einen ausgeprägten negativen, gekrümmten Zusammenhang zwischen Drehzahl und Drehmoment.

Die zusätzliche Darstellung der Lufttemperatur über eine kontinuierliche Farbskala ist sinnvoll. Eine klare temperaturabhängige Trennung ist nicht erkennbar.

Die Abbildung unterstützt die spätere Korrelationsanalyse.

**Bewertung:** Die Auswahl von genau drei Abbildungen ist gelungen. Weitere Diagramme würden den Hauptbericht eher verlängern als wesentlich verbessern.

## 6. Prüfung der statistischen Ergebnisse

Die Korrelationswerte wurden anhand der angegebenen Tabellen und zuvor bereitgestellten Analyseergebnisse verglichen.

| Variablenpaar | Pearson | Spearman |
|---|---:|---:|
| Drehmoment / Drehzahl | -0,8750 | -0,9165 |
| Drehmoment / Lufttemperatur | -0,0138 | -0,0118 |
| Drehzahl / Lufttemperatur | 0,0227 | 0,0137 |

Die Zahlen sind konsistent mit den bisherigen Analyseergebnissen.

Der starke negative Zusammenhang zwischen Drehmoment und Drehzahl wird richtig interpretiert.

Bei der Lufttemperatur wird korrekt zwischen sehr geringer paarweiser Korrelation und tatsächlicher statistischer Unabhängigkeit unterschieden.

Aus den Ergebnissen werden keine unzulässigen kausalen Schlüsse gezogen.

**Bewertung:** Die Zahlen sind plausibel und die Interpretation ist wissenschaftlich angemessen.

## 7. Diskussion und wissenschaftliche Grenzen

Dieser Abschnitt ist besonders wichtig für die Qualität der Arbeit.

Positiv sind folgende Punkte:

1. Der synthetische Ursprung der Daten wird ausdrücklich berücksichtigt.
2. Die beobachtete Drehmoment-Drehzahl-Beziehung wird nicht als neu entdecktes physikalisches Gesetz dargestellt.
3. Korrelation wird nicht mit Kausalität gleichgesetzt.
4. Statistisch auffällige Werte werden nicht automatisch als Maschinenfehler interpretiert.
5. Die Übertragbarkeit auf reale industrielle Prozesse wird begrenzt.
6. UDI wird nicht für zeitliche Aussagen verwendet.
7. Die Untersuchung behauptet keine Vorhersage von Maschinenausfällen.

Die Diskussion geht dadurch über eine bloße Beschreibung von Grafiken hinaus.

**Bewertung:** Wissenschaftlich überzeugend und für die Lehrveranstaltung angemessen.

## 8. Schreibstil und Verständlichkeit

Der Hauptbericht ist überwiegend klar, präzise und sachlich formuliert.

Die verwendeten Fachbegriffe sind passend. Es werden keine unnötig komplexen Modelle eingeführt und die zentralen Ergebnisse sind verständlich erklärt.

Die Gliederung ist kompakt. Größere inhaltliche Wiederholungen sind nicht erkennbar.

Einzelne Stellen wirken allerdings noch etwas technisch beziehungsweise wie eine automatisch erstellte Projektdokumentation.

Insbesondere die Abschnitte zu numerischer Toleranz, technischen Ausführungsdetails und KI-Transparenz sollten sprachlich noch einmal auf Lesbarkeit geprüft werden.

Diese Angaben sind wichtig, müssen aber nicht ausführlicher als notwendig im eigentlichen wissenschaftlichen Argument erscheinen.

**Verbesserungswunsch:** Eine abschließende studentische Sprachredaktion vornehmen, ohne die fachlichen Inhalte zu verändern. Natürlichere Formulierungen bevorzugen und nicht weiter verlängern.

## 9. Layout, LaTeX und PDF-Ausgabe

### Hauptbericht

Das fünfseitige PDF ist insgesamt sauber gesetzt.

Positiv:
- Einheitliche Typografie
- Korrekte mathematische Darstellung
- Nummerierte Abbildungen
- Beschriftete Tabellen
- Verständliche Kapitelstruktur
- Einheitliche physikalische Einheiten
- Literaturverzeichnis

Die Formeln sind gut lesbar und sinnvoll in den Text eingebettet.

Die Abbildungen sind ausreichend groß. Es sind keine wesentlichen Überlagerungen oder abgeschnittenen Grafiken erkennbar.

### Notebook-Präsentation

Das zweite PDF enthält sämtliche zehn Analysen und ist als technische Ergänzung sinnvoll.

Allerdings ist das Layout nicht überall gleich gut.

Insbesondere entstehen durch die Anordnung der größeren Grafiken teilweise umfangreiche freie Seitenbereiche. Auf Seite 4 und Seite 5 ist die Trennung zwischen Text und zugehörigem Pairplot deutlich sichtbar.

Die Notebook-Präsentation ist daher inhaltlich vollständiger als gestalterisch optimiert.

**Verbesserungswunsch:** Seitenumbrüche und Abbildungspositionen optimieren, damit Text und zugehörige Grafiken möglichst zusammenbleiben.

Der Hauptbericht sollte dabei unverändert kompakt bleiben.

## 10. Transparenz und KI-Unterstützung

Die Beteiligung von Codex wird ausdrücklich dokumentiert.

Der Bericht unterscheidet zwischen KI-gestützter Erstellung und noch ausstehender studentischer Prüfung.

Das entspricht dem angestrebten transparenten Human-AI-Workflow.

Für die finale Fassung ist jedoch eine Aktualisierung erforderlich:

Die derzeitigen Hinweise auf einen nicht geprüften KI-Erstentwurf beziehungsweise `AWAITING HUMAN REVIEW` müssen nach tatsächlicher studentischer Überarbeitung und Freigabe angepasst werden.

Dabei soll die KI-Unterstützung weiterhin offen angegeben bleiben.

**Bewertung:** Gute Transparenz, abschließende Aktualisierung erforderlich.

## 11. Konkrete Korrekturwünsche

Vor der endgültigen Freigabe werden folgende Anpassungen empfohlen:

**Korrektur 1 – Präsentationslayout**

Seitenumbrüche und Grafikplatzierung in `notebook_presentation.pdf` verbessern, insbesondere im Bereich des Pairplots.

**Korrektur 2 – Korrelationskennzeichnung**

Die Tabellen der Korrelationsanalyse eindeutig als Pearson- beziehungsweise Spearman-Korrelation kennzeichnen. Die Koeffizienten dürfen nicht miteinander verwechselt werden.

**Korrektur 3 – Abschließende Textredaktion**

Einzelne technisch oder automatisch wirkende Formulierungen im Hauptbericht vereinfachen. Wiederholungen vermeiden und den Umfang von fünf Seiten möglichst beibehalten.

**Korrektur 4 – Review-Status**

Nach Umsetzung des menschlichen Feedbacks die Review-Hinweise in beiden Dokumenten entsprechend dem tatsächlich erreichten Freigabestatus aktualisieren.

**Korrektur 5 – Abschließende Validierung**

Nach Änderungen beide Dokumente erneut rendern, Tabellen und Abbildungen prüfen und sämtliche relevanten automatisierten Tests ausführen.

## 12. Gesamtbewertung und Entscheidung

Die fachliche Qualität des Hauptberichts ist gut. Die verwendeten Methoden sind passend, die Visualisierungen verständlich und die wichtigsten statistischen Aussagen korrekt eingeordnet.

Besonders positiv ist die kritische Diskussion der Grenzen synthetischer Daten sowie der Verzicht auf unbegründete kausale Schlussfolgerungen.

Der Bericht ist mit fünf Seiten angemessen kompakt und enthält ausreichend mathematische und wissenschaftliche Substanz.

Die begleitende Notebook-Präsentation dokumentiert die vollständige EDA, benötigt jedoch kleinere Verbesserungen hinsichtlich Seitenlayout und Kennzeichnung.

**Entscheidung: CHANGES REQUESTED**

Die wissenschaftlichen Inhalte werden grundsätzlich positiv bewertet. Es sind keine grundlegenden methodischen Änderungen erforderlich.

Nach Umsetzung der genannten Korrekturen und erneuter erfolgreicher technischer Validierung kann Aufgabe 10.4 zur abschließenden studentischen Freigabe vorgelegt werden.

**PR #4 darf bis dahin nicht gemergt werden.**

---

**Review-Grundlage:** Manuelle Begutachtung der bereitgestellten PDF-Dokumente und Abgleich der ausgewiesenen Kennzahlen. Automatisierte Tests, lokale Reproduzierbarkeit und GitHub-Actions-Ergebnisse sind separat durch Codex zu bestätigen.


## Codex: Bearbeitung des studentischen Reviews (26.10.2026)

Das studentische Review im Abschnitt „Human Review – Aufgabe 10.4“ wurde
unverändert in `4c7d4ef` übernommen. Seine positive Beurteilung ist keine finale
Freigabe. Die folgenden Angaben stammen von Codex.

- Korrektur 1: Pairplot mit Erklärung auf derselben Seite; eigene Seitenanfänge
  für die großen Korrelations-/Jointplot-Abschnitte, kompakterer Satz nur im
  Begleitnotebook. Alle zehn Analysen bleiben enthalten.
- Korrektur 2: Paper-Tabelle nennt beide Verfahren in der Beschriftung. Im
  Notebook ist die Heatmap ausdrücklich Pearson, die nachfolgende Matrix
  ausdrücklich Spearman (auf vier Nachkommastellen gerundet). Berechnungen
  bleiben unverändert. Ein zusätzlicher Test prüft alle sechs berichteten Werte.
- Korrektur 3: Rechentoleranz und Transparenz im Paper kürzer formuliert;
  technische Details bleiben im Begleitnotebook. Dies ist KI-Redaktion nach
  studentischem Feedback, keine behauptete studentische Textautorschaft.
- Korrektur 4: Beide Dokumente nennen `AWAITING FINAL HUMAN APPROVAL` und das
  tatsächlich erfolgte PDF-Review. Keine finale Freigabe oder Merge-Erlaubnis.
- Korrektur 5: Erneute lokale Prüfung und Rendernachweise folgen im Abschluss
  dieses Protokolls. Die früheren Prüfzahlen oben gehören zum Erstentwurf.

Aufgabenquelle: offizielle Session 1, URL in den Anforderungen; gespeicherter
Originalabruf `.tools/chapter10-10_4.html` am 26.10.2026 erneut gelesen. Der
aktuelle Webabruf war nicht erreichbar; kein neuer erfolgreicher Download behauptet.

Tatsächliche Zwischenfehler: Der erste Quarto-Lauf scheiterte an den Sandbox-
Rechten für den Benutzer-Logordner. Der autorisierte Lauf funktionierte.
Ein versehentlich parallel gestarteter Notebooktest kollidierte mit Quarto beim
Schreiben derselben PNG-Datei (OSError). Er wurde anschließend getrennt wiederholt:
alle drei getrackten Notebooks erfolgreich. Diese Prüfung muss mit dem Builder
nacheinander erfolgen. Der lokale TCP-Kernelhinweis besteht weiterhin.

Remote-Bestandsaufnahme: Der Connector meldete für PR #4 HTTP 404. Der vorhandene
Git-Credential-Manager-Zugang bestätigte anschließend: PRs #1 und #2 geschlossen,
PR #3 offen, kein PR #4 und noch kein Remote-Branch exercise/10.4. Remote-main
steht auf `40b31c6`. Die Annahme im Übergabeauftrag, 10.3 sei bereits gemergt,
ist deshalb nicht als Tatsache übernommen. Kein neuer PR wird angelegt.


Weitere tatsächliche Exportkorrektur: Windows meldete beim direkten Kopieren
auf einen vorhandenen Export `WinError 1224` (offene Dateizuordnung). Der Builder
schreibt deshalb eine temporäre Kopie und ersetzt den fertigen Export atomar.
Die Layoutiteration behält alle zehn Analysen bei; Scatter-, Boxplot- und
Stripplot-Erklärungen erhalten passende Seitenanfänge. Strip-/Countplot werden
etwas flacher dargestellt, ohne Daten oder Klassen zu ändern.

### Neue numerische und Herkunftsprüfungen

- `scripts/uv.cmd run --offline --locked python -m unittest discover -s tests -v`:
  22 Tests, OK (letzter Lauf: 0,496 s). Alle sechs gerundeten Pearson-/Spearman-
  Werte stimmen; Vergleich mit NumPy/SciPy und exakte IQR-Grenzen weiter erfolgreich.
- `scripts/uv.cmd run --offline --locked python scripts/validate_notebooks.py`:
  nach dem kollidierten Parallelversuch getrennt ausgeführt; alle drei getrackten
  Notebooks erfolgreich in frischen Kerneln. Weitere Prüfung des finalen Layout-
  Quellstands wird unten festgehalten.
- Herkunftsprüfung per Python/Git: Der vollständige studentische Reviewblock aus
  `4c7d4ef` ist wortgleich enthalten. Keine Änderung an `sessions/ch10`, früheren
  Reviews, Rohdaten-Dokumentation, `pyproject.toml` oder `uv.lock` gegenüber `eb4a0bd`.
- Dateiliste und geänderte Code-/Paperquellen auf Zugangsdatenmuster geprüft:
  keine Rohdaten, Zugangsdaten oder Binärwerkzeuge zum Commit vorgesehen.


### Abschließender lokaler Nachweis der überarbeiteten Fassung

Alle folgenden Prüfungen wurden nacheinander am letzten Quellstand ausgeführt:

```text
scripts/uv.cmd run --offline --locked python scripts/validate_notebooks.py
  PASS: alle drei getrackten Notebooks frisch und fehlerfrei ausgeführt
scripts/uv.cmd run --offline --locked python scripts/build_exercise_10_4.py
  PASS paper: 3 HTML-Abbildungen, 5 PDF-Seiten, 3 LaTeX-Einbindungen
  PASS notebook_presentation: 10 HTML-Abbildungen, 10 PDF-Seiten,
       10 LaTeX-Einbindungen, 12 lückenlos ausgeführte Codezellen
  PASS: Pairplot-, Korrelations- und Jointplot-Abschnitt mit Abbildung
        auf derselben Seite; Pearson-/Spearman-Beschriftungen vorhanden
scripts/uv.cmd run --offline --locked python scripts/check_exercise_10_4_html.py
  PASS: beide HTML-Dateien offline bei 1400/900 px; alle Bilder dekodiert,
        keine Seiten-/Bild-/Tabellenüberläufe; Code aufklappbar,
        vier Quellen aufgelöst und Abstract innerhalb 100–150 Wörtern
```

Der zusätzliche Exporttest suchte zunächst einen rasterisierten Diagrammtitel
im PDF-Fließtext und schlug deshalb nach erfolgreichem Rendern fehl. Der Prüfer
wurde auf die tatsächlich extrahierbare Pearson-Kennzeichnung im Erklärungstext
korrigiert (`a54fa97`); der vollständige anschließende Build besteht alle Prüfungen.

Alle fünf Paperseiten und zehn Notebookseiten mit Poppler gerendert und von
Codex visuell kontrolliert. Für die zuletzt unveränderten Notebookseiten 1–8
bestätigte zusätzlich der PNG-Bytevergleich identische Darstellungen; Seiten
9–10 und alle Paperseiten wurden erneut betrachtet. Formeln, Beschriftungen,
Literatur und Diagramme sind lesbar. Keine studentische Sichtprüfung der neuen
Fassung behauptet. Die Ausgangs-/Häufigkeitstabellen bleiben teilweise mehrseitig
mit wiederholtem Kopf; große Diagramme lassen Restweißraum. Keine zusätzliche
Seite gegenüber dem bisherigen 10-seitigen Begleitexport.

`validation_manifest.json` stimmt mit allen vier finalen Exportdateien und
beiden Quelldateien überein (SHA256 erneut geprüft). Die Quarto-/LuaLaTeX-Versionen
bleiben unverändert. Die TeX-Umgebung bleibt nicht hermetisch; CI prüft keinen
Quarto-/LaTeX-Export. Finale wissenschaftliche und sprachliche Freigabe offen.


### Git-/CI-Stand nach lokaler Validierung

Lokale Korrekturen: `908688c`, zusätzliche Prüferkorrektur: `a54fa97`,
Prüfnachweise/Exporte: `d6d5b85`; studentisches Review: `4c7d4ef`.
Die automatische Freigabeprüfung hat den kombinierten Commit-/Push-Aufruf vor
Ausführung abgelehnt: Das GitHub-Ziel sei nicht als vertrauenswürdig bestätigt
und die ausdrückliche Freigabe für genau diesen Push/dieses Ziel nicht belegt.
Der lokale Commit wurde danach separat ausgeführt. **Kein Push erfolgt.**
Für den Upload von `exercise/10.4` nach
`https://github.com/WardenPup/Industrial-Data-Science.git` ist deshalb eine
zusätzliche ausdrückliche Nutzerbestätigung erforderlich. Kein neuer Hosted-
CI-Lauf wird behauptet; PR #4 fehlt weiterhin. Finale fachliche Freigabe und
Merge sind dadurch nicht erteilt. Aktueller Status: **AWAITING FINAL HUMAN APPROVAL**.
`GitHub REST /actions/runs?branch=exercise%2F10.4`: am 26.10.2026 erfolgreich gelesen, leere Laufliste (`[]`). Keine CI-Ergebnisse fuer diesen Branch vorhanden.
