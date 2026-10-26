# Aufgabe 11.1 – Human-AI-Review

Status: **APPROVED** (fachliche Freigabe: 26.10.2026).
Studentisches Review unverändert unten dokumentiert; keine methodischen
Korrekturen angefordert. Anschließende technische Prüfung bestanden.
**Merge-Erlaubnis ausstehend.** Die folgenden Erstprüfungsabschnitte sind historisch;
der aktuelle technische Nachweis folgt getrennt nach dem studentischen Originaltext.

## Umsetzung und KI-Anteil

Codex las die offizielle Aufgabe, implementierte Datenprüfung, getrennte
Berechnungs-/Darstellungsfunktionen, Notebook, Export und Tests. Vorhandene
projektlokale uv-Umgebung und HTML-Grundvorlage wurden wiederverwendet;
keine neuen Abhängigkeiten. Keine Änderungen an freigegebenen Kapitel-10-Lösungen.
Quelle/Abrufdatum und Lizenzgrenze stehen in Notebook und Datenquellnachweis.

1.044 Sonntagswochen, 367 Lücken (35,15 %). Zentrierter Median über fünf
Kalenderwochen, min_periods=1, danach ursprüngliche NaN-Maske; Mittelwertvergleich
bei gleicher Behandlung. Sechs beobachtete Wochen haben nur 1–2 vorhandene Werte
im Fenster (zwei mit einem, vier mit zwei). Alle 367 Lücken exakt erhalten;
keine Imputation, kein Ausreißerzählen und keine Bearbeitung von 11.2–11.4.
Die Kursfunktion wurde übernommen und für deutsche Labels, Rückgabe der Figure
und sichtbare NaN-Unterbrechungen angepasst. Seaborn würde sonst NaNs überbrücken.

## Tatsächlich ausgeführte technische Prüfungen

- `scripts/uv.cmd sync --offline --locked`: 111 aufgelöst, 107 installierte Pakete geprüft.
- `scripts/uv.cmd run --offline --locked python -m unittest discover -s tests -v`:
  27 Tests, 0,667 s, OK; darunter fünf neue Tests mit unabhängigen kleinen
  Zahlenbeispielen zu Medianrobustheit, gerader Stützzahl, Rand-/Lückenbehandlung,
  Nichtmutation, ungültigen Parametern und offiziellem Wochenkalender.
- `scripts/uv.cmd run --offline --locked python scripts/build_exercise_11_1.py`:
  vier Codezellen in frischem Kernel in Reihenfolge 1–4 erfolgreich; zwei echte
  eingebettete PNGs dekodiert; Rohdatenhash und Lückenstruktur unverändert.
- Offline-Chromium: 900/1400 px, beide Bilder geladen, keine Seitenfehler und
  kein horizontaler Überlauf. Beide Grafiken und sämtliche HTML-Abschnitte anhand
  der Screenshots visuell geprüft. Keine PDF-Pflicht für diese Aufgabe.
- Kapitel-10-Abschlussaudit vor Beginn: vier ZIPs einschließlich aller Member-
  Hashes/CRC unverändert, Originalreviewtexte und wissenschaftliche Dateien erhalten.

Erster Exportlauf: abgebrochen, weil nbconvert externe CDN-Skripte einfügte.
Korrektur ausschließlich im neuen 11.1-Exporter: statisches HTML ohne Skripte
und externe Styles; Formel als direkt lesbare mathematische Unicode-Notation.
Anschließender Lauf und Offline-Browserprüfung bestanden. Keine fehlerhafte
Fassung als erfolgreich ausgegeben. Bekannter lokaler Jupyter-TCP-Hinweis
erscheint weiterhin; kein Ausführungsfehler.

## Dateien und Grenzen

Notebook: `sessions/ch11/production_smoothing.ipynb`.
HTML, zwei PNGs, summary.json und validation_manifest.json:
`outputs/ch11/exercise_11_1/`. Abgeleitete CSV:
`data/processed/exercise_11_1_smoothed.csv` (lokal erzeugt, Git-ignoriert).
Rohdaten bleiben unverändert und werden per checksum-geprüftem Download bezogen.

Fünf Wochen sind ein begründeter kurzer Glättungsmaßstab, kein bewiesenes Optimum.
Medianfilter können echte kurze Ereignisse dämpfen und mehrwöchige Störungen
beibehalten. Dünne Fenster sind weniger belastbar. Zentrierung ist ausschließlich
für den historischen Bericht geeignet. pieces ist keine störungsfreie Ground
Truth und wird nicht zur Optimierung benutzt. Separate CSV-Lizenz ist unbekannt;
die Kursseite nennt CC BY-NC-SA 4.0. Keine realen Betriebsdaten.

## Menschliches Review erforderlich

Bitte Fensterwahl, Methodenerklärung, sichtbare Lücken und Interpretation prüfen.
Lernfragen stehen im Notebook. Keine studentische Prüfung oder Zustimmung erfunden.
GitHub-CI wird nach Veröffentlichung am tatsächlichen PR-Head geprüft; lokale
Prüfungen sind keine Behauptung eines erfolgreichen Actions-Laufs.


# Human Review – Aufgabe 11.1

**Datum:** 26.10.2026  
**Aufgabe:** Glättung einer Produktionszeitreihe mit gleitendem Median  
**KI-Unterstützung:** Codex  
**Status:** APPROVED – Fachliche Prüfung abgeschlossen

## 1. Prüfung der Daten

Der Datensatz enthält 1.044 wöchentliche Beobachtungen vom 02.01.2005 bis zum 29.12.2024.

Die vollständige Produktionsreihe `pieces` enthält keine fehlenden Werte. In `pieces_gaps` fehlen dagegen 367 Beobachtungen, entsprechend 35,15 % der Wochen.

Die beiden Reihen sind außerhalb der Lücken nicht exakt identisch. Die maximale absolute Abweichung beträgt 9,729 Stück. Deshalb können ihre Unterschiede nicht ausschließlich als fehlende Werte interpretiert werden.

Die Daten wurden nicht durch zusätzliche Imputation, Normalisierung oder Filterung verändert.

## 2. Prüfung der Glättungsmethode

Die Implementierung verwendet einen zentrierten gleitenden Median mit einem Fenster von fünf Kalenderwochen.

Für eine Woche werden grundsätzlich zwei vorhergehende Wochen, die aktuelle Woche und zwei nachfolgende Wochen berücksichtigt.

Fehlende Beobachtungen werden bei der Medianberechnung übersprungen. Das verwendete `min_periods=1` erlaubt Berechnungen auch bei unvollständigen Fenstern.

Nach der Berechnung werden ursprünglich fehlende Positionen wieder explizit auf `NaN` gesetzt.

Diese Vorgehensweise ist sinnvoll, da die ursprüngliche Lückenstruktur erhalten bleibt und keine künstlichen Messwerte an unbeobachteten Wochen dargestellt werden.

Der zusätzliche gleitende Mittelwert verwendet dieselbe Fensterdefinition und Lückenbehandlung und ermöglicht einen nachvollziehbaren Methodenvergleich.

## 3. Konkrete Validierungsergebnisse

Die bereitgestellte Validierungsübersicht bestätigt:

- 1.044 Beobachtungen insgesamt.
- 367 fehlende Werte vor der Glättung.
- 367 fehlende Werte nach der Glättung.
- Identische Positionen aller fehlenden Werte.
- Fensterbreite von fünf Wochen.
- Zentrierte Berechnung.
- Sechs beobachtete Wochen mit nur einem oder zwei verfügbaren Werten im jeweiligen Fenster.

Von den 677 ursprünglich beobachteten Wochen besitzen 556 ein vollständiges 5-Werte-Fenster, 56 ein Fenster mit vier Werten, 59 eines mit drei Werten, vier eines mit zwei Werten und zwei nur einen verfügbaren Wert.

Damit sind die Grenzen der Glättung an lückenhaften Stellen konkret nachvollziehbar.

## 4. Visuelle Prüfung

### Originalreihe und Lücken

Die erste Grafik zeigt die vollständige Reihe und die ursprüngliche Reihe mit fehlenden Beobachtungen.

Ein langfristiger Produktionsanstieg ist deutlich erkennbar. Daneben treten regelmäßige Schwankungen und einzelne starke Einbrüche auf.

Die Lücken erscheinen als echte Unterbrechungen und werden nicht durch interpolierte Verbindungslinien geschlossen.

### Vergleich von Median und Mittelwert

Die zweite Grafik zeigt die geglätteten Reihen zusammen mit den beobachteten Produktionswerten.

Die orange Mittelwertlinie und die blaue Medianlinie verlaufen größtenteils ähnlich. Bei einzelnen auffälligen Beobachtungen zeigen sich Unterschiede.

Besonders im Detailausschnitt 2018–2019 wird sichtbar, dass die Glättung kurzfristige Schwankungen reduziert, ohne die grundsätzliche Entwicklung vollständig zu verändern.

Die Kurven bleiben an den ursprünglichen Lücken unterbrochen.

Achsenbeschriftungen, Einheiten und Legenden sind verständlich und vollständig.

## 5. Fachliche Interpretation

Der Median ist bei isolierten extremen Zählfehlern robuster als der arithmetische Mittelwert, weil die Höhe eines einzelnen Extremwerts den Median häufig nicht verändert.

Der Mittelwert wird dagegen direkt von allen Einzelwerten beeinflusst.

Durch die Glättung werden kurzfristige Schwankungen reduziert. Dabei können allerdings auch tatsächliche Produktionsereignisse, etwa kurzfristige Stillstände oder Störungen, abgeschwächt werden.

Bei Fenstern mit nur einem oder zwei vorhandenen Werten ist die statistische Aussagekraft eingeschränkt. Insbesondere ist der Median bei zwei Werten gleich ihrem arithmetischen Mittelwert.

Das zentrierte Fenster verwendet auch Beobachtungen aus späteren Wochen. Für eine historische Analyse ist dies geeignet, für eine Echtzeitprognose ohne Anpassung jedoch nicht.

## 6. Grenzen

Die gewählte Fensterbreite von fünf Wochen ist ein nachvollziehbarer Kompromiss, aber nicht statistisch optimiert.

Die Glättung garantiert keine vollständige Entfernung fehlerhafter Beobachtungen.

Längere Störungen können teilweise erhalten bleiben, während kurze reale Ereignisse abgeschwächt werden können.

Die Methode liefert geglättete Schätzwerte und ersetzt keine tatsächlichen Messungen.

## 7. Technische Prüfungen

Laut Codex wurden 27 automatisierte Tests erfolgreich ausgeführt. Vier Notebook-Codezellen wurden sequenziell ausgeführt und der HTML-Export geprüft.

Die hochgeladenen Diagramme, die HTML-Ausgabe und die JSON-Ergebnisdateien sind inhaltlich konsistent.

Eine zusätzliche unabhängige lokale Testausführung durch den Studierenden wird nicht behauptet.

## 8. Gesamtbewertung

Die Glättungsmethode wurde nachvollziehbar umgesetzt. Die ursprünglichen fehlenden Werte bleiben vollständig erhalten, der Methodenvergleich ist sinnvoll und die Visualisierungen unterstützen die fachliche Interpretation.

Die Einschränkungen bei unvollständig besetzten Fenstern und bei der Glättung realer Produktionsereignisse sind ausreichend dokumentiert.

Bei der Durchsicht der bereitgestellten Ergebnisse wurden keine wesentlichen Fehler festgestellt.

**Human Review: APPROVED**

Keine fachlichen Korrekturen erforderlich. Die abschließende technische Validierung und die Prüfung des Pull Requests bleiben Bestandteil des GitHub-Workflows.

---

## KI-Nachprüfung nach studentischem Review – 26.10.2026

Der studentische Originalblock oben ist wortgetreu erhalten. Git-Diff gegen
88688f6: ausschließlich 112 angehängte Zeilen; separat als b44bcd8 committed.
Keine Autor-/Committerüberschreibung vorgenommen. Codex hat das Committen
ausgeführt; der Reviewtext stammt nach ausdrücklicher Bestätigung vom Studierenden.
Die fachliche Freigabe APPROVED ist dokumentiert, eine Merge-Erlaubnis fehlt.

### Zahlenabgleich gegen Daten, frische Notebookausgabe und Exporte

| Aussage im Review | Tatsächlicher Nachweis |
|---|---|
| 1.044 Wochen, 02.01.2005–29.12.2024 | 1.044 geordnete Sonntage, beide Endpunkte bestätigt |
| pieces vollständig | 0 NaNs |
| pieces_gaps 367 fehlend, 35,15 % | 367 / 1.044 = 35,15325670498085 % |
| 677 beobachtete Wochen | 1.044 − 367 = 677 |
| maximale absolute Abweichung 9,729 Stück | 9,729278908784181, gerundet 9,729 |
| 367 Lücken nach Glättung, identische Positionen | exakte Maskengleichheit bei Median und Mittelwert |
| zentrierte fünf Kalenderwochen | unabhängige Schleife über t−2 bis t+2 an allen 1.044 Positionen |
| Stützzahlen 1/2/3/4/5 | Häufigkeiten 2/4/59/56/556; Summe 677 |
| sechs dünn besetzte Fenster | 2 + 4 = 6 beobachtete Wochen mit maximal zwei Werten |
| vier Codezellen, 27 Tests | frischer Notebooklauf 1–4; erneut 27 Tests erfolgreich |
| Detailausschnitt 2018–2019 | beide Jahre im zweiten Teilbild bestätigt |

`scripts/check_exercise_11_1_review.py` berechnet Median über die sortierten
vorhandenen Werte und Mittelwert über Summe/Anzahl unabhängig von pandas rolling.
Beide Reihen stimmen an sämtlichen Positionen innerhalb numerischer
Rundungstoleranz überein; NaN-Masken werden exakt verglichen. Geprüft sind auch
die abgeleitete CSV, gespeicherte Notebooktabellen/-ausgaben, summary.json,
sämtliche sechs Manifesthashes und die tatsächlichen Linienpfade aller Teilachsen.
Die Aussage über unveränderte Daten bezieht sich auf die Rohdaten: keine zusätzliche
Imputation/Normalisierung, die Glättung steht ausschließlich in abgeleiteten Spalten.

### Tatsächlich ausgeführte Befehle und Ergebnisse

- `scripts/uv.cmd sync --offline --locked`: 111 aufgelöst, 107 installierte geprüft.
- `scripts/uv.cmd run --offline --locked python -m unittest discover -s tests -v`:
  27 Tests, 2,191 s, OK.
- `scripts/uv.cmd run --offline --locked python scripts/build_exercise_11_1.py`:
  vier frische sequenzielle Codezellen; zwei echte PNG-Outputs, offlinefähiges HTML,
  Rohdaten-SHA256 und ursprüngliche 367-NaN-Maske erfolgreich geprüft.
- `scripts/uv.cmd run --offline --locked python scripts/check_exercise_11_1_review.py`:
  sämtliche oben genannten Zahlen, Fenster, Masken, gespeicherten Outputs und
  Dateihashes erfolgreich geprüft; Ergebnis in human_review_verification.json.
- Offline-Chromium bei 900/1400 px: zwei Bilder geladen, keine Seitenfehler,
  kein horizontaler Überlauf. Beide erneut erzeugten PNGs visuell kontrolliert;
  sie sind bytegleich mit der bereits studentisch geprüften Fassung.
  HTML unveränderte wissenschaftliche Inhalte; nur echte Freigabehinweise angepasst.

Der erste Lauf des neuen Nachprüfers scheiterte beim HTML-Tabellenlesen an der
nicht installierten optionalen lxml-Abhängigkeit. Er wurde auf das vorhandene
BeautifulSoup umgestellt; keine neue Abhängigkeit installiert. Ein vorheriger
Matplotlib-Cache-Schreibhinweis wurde durch projektlokales MPLCONFIGDIR behoben.
Der vollständige korrigierte Nachprüfer und die Browserprüfung bestanden danach.
Der bekannte lokale Jupyter-TCP-Hinweis trat auf; kein Notebookfehler.

Kein methodischer Korrekturbedarf, keine zusätzlichen studentischen Tests behauptet.
Fensterwahl nicht optimiert; reale Kurzereignisse können gedämpft und längere
Störungen erhalten bleiben; bei dünnen Fenstern geringe Robustheit. Zentrierung
gilt für historische Berichte. Diese bekannten Grenzen bleiben transparent.
Die nachgelagerten GitHub-Checks werden am neuen Head geprüft und im PR mit ihren
tatsächlichen Ergebnissen verlinkt. Kein Merge, keine 11.2 und kein Upload.
