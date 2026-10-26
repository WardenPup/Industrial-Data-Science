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
