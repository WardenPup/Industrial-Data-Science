# Aufgabe 11.1 – Human-AI-Review

Status: **AWAITING HUMAN REVIEW** (26.10.2026).
Studentisches Feedback: noch nicht eingegangen. Keine fachliche Freigabe,
keine Merge-Erlaubnis. Die Umsetzung wurde ausdrücklich beauftragt.

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
