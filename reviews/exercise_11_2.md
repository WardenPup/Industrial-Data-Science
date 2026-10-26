# Aufgabe 11.2 – Human-AI-Review

Status: **AWAITING HUMAN REVIEW** (26.10.2026).
Kein studentisches Feedback, keine wissenschaftliche Freigabe und keine
Merge-Erlaubnis für 11.2. Keine Universitätseinreichung.

## Anforderungen und Umsetzung

Die offizielle Aufgabe und Kapitel 5 wurden am 26.10.2026 vollständig gelesen;
Quellen und Abnahmekriterien: docs/EXERCISE_11_2_REQUIREMENTS.md.
Codex erstellte Anforderungen, Berechnungs-/Darstellungsfunktionen, Notebook,
Testfälle, HTML-Exporter und technische Nachweise. Keine neuen Abhängigkeiten.
Wiederverwendet: unveränderte Rohdaten/Hashprüfung, freigegebener 11.1-Median
und Kurs-Plotfunktion. Die 11.2-Anpassung der Plotfunktion erfolgt in einem
neuen Modul; keine Änderung freigegebener 11.1-Lösungsdateien.

| Offizielle Anforderung | Umsetzung/Nachweis |
|---|---|
| Geglättete Reihe mit Lücken aus 11.1 | deterministische Reproduktion plus kanonischer SHA256 über Werte/NaN-Maske |
| Verschiedene Methoden aus Kapitel 5 | ffill, bfill, linear, polynomial Grad 2/5, PCHIP |
| Darstellung mit Kursfunktion | sechs dreiteilige Figuren, nur Ergänzungen im dritten Teilbild |
| Diskussion | konkrete Diagnostik, gemeinsamer Langlückenausschnitt, Annahmen und Grenzen |
| Notebook-Abgaberegel | ausgeführtes Notebook plus eigenständiges HTML; kein PDF in 11.2 gefordert |

## Tatsächliche Ergebnisse

1.044 Wochen, 677 vorhandene und 367 fehlende geglättete Werte. 32 Lückenblöcke,
Längen 3–23 Wochen, keine Randlücken. Erste längste Lücke: 11.12.2011–13.05.2012.
Alle sechs Verfahren ergänzen die 367 fehlenden Wochen vollständig; alle 677
vorhandenen Werte bleiben unverändert. Keine negativen Ergänzungen.
Außerhalb der unmittelbar bekannten Lückenrandwerte liegen bei Polynom Grad 2
78 und bei Grad 5 189 Ergänzungen, sonst jeweils null. Dies ist eine Formdiagnose,
keine Genauigkeitsbewertung. Vollständige Zahlen: method_summary.csv und gaps.csv.

## Ausgeführte technische Prüfungen

- `scripts/uv.cmd sync --offline --locked`: 111 Pakete aufgelöst, 107 installierte geprüft.
- `scripts/uv.cmd run --offline --locked python -m unittest discover -s tests -v`:
  33 Tests, final 0,723 s, OK; sechs neue Tests mit analytischer linearer Rampe,
  quadratischer Referenz, Randlückenpolitik, Nichtmutation, Lücken-/Randdiagnostik,
  ungültigen Parametern und vollständiger offizieller Datenprüfung.
- `scripts/uv.cmd run --offline --locked python scripts/build_exercise_11_2.py`:
  zehn Codezellen frisch sequenziell in einem neuen Kernel; sieben echte PNG-
  Outputs und sieben eingebettete HTML-Bilder dekodiert. Gespeicherte CSV gegen
  Eingabe/Masken geprüft, lineare Ergebnisse unabhängig gegen NumPy interp;
  alle sechs Reihen endlich, unveränderte bekannte Werte, Rohdatenhash und
  kanonischer freigegebener Eingabehash bestätigt.
- `scripts/uv.cmd run --offline --locked python scripts/check_exercise_11_2_html.py`:
  Offline-Chromium bei 900/1400 px, sieben Bilder geladen, keine Seitenfehler,
  kein horizontaler Überlauf. Alle sieben PNGs visuell geprüft; HTML-Formeln,
  Tabellen, Diskussion und Reviewfragen anhand der Browserbilder kontrolliert.
- Originaldaten und freigegebene 10.x-/11.1-Resultate bleiben unverändert;
  Kapitel-10-ZIPs und Checksummen werden vor Veröffentlichung erneut verglichen.

Im ersten Testlauf erschien ein DeprecationWarning zur pandas/NumPy-
Zeitabstandskonvertierung. Auf explizite NumPy datetime64[ns]/timedelta64-Tage
umgestellt; vollständiger Testlauf ohne diesen Hinweis und Notebook erneut
erfolgreich ausgeführt. Der bekannte lokale Jupyter-TCP-Hinweis erschien;
kein Test- oder Notebookfehler. Ein vorläufiges internes Datensichtungshelfer-
skript benötigte einen expliziten Projektimportpfad; finale Skripte setzen ROOT
selbst und laufen vom Projektstamm. Keine globalen Pakete installiert.

## Dateien und Reproduktion

- Notebook: sessions/ch11/production_imputation.ipynb.
- Neue Berechnung/Darstellung: sessions/ch11/imputation.py, imputation_plots.py.
- outputs/ch11/exercise_11_2/: production_imputation.html, ffill.png, bfill.png,
  linear.png, polynomial2.png, polynomial5.png, pchip.png,
  longest_gap_comparison.png, gaps.csv, method_summary.csv, summary.json,
  validation_manifest.json.
- data/processed/exercise_11_2_imputed.csv: lokal erzeugte vollständige Ableitung,
  Git-ignoriert. Rohdatenbeschaffung wie 11.1 über scripts/download_production.py.
- Bestehende gesperrte uv-Umgebung; Export-/Prüfbefehle oben, keine PDF-Pflicht.

## Wissenschaftliche Grenzen und konkrete Reviewfragen

Historischer Bericht, keine Prognose. Schon die zentrierte Eingabe nutzt spätere
Werte; ffill macht die Gesamtpipeline nicht kausal. Interpolation nur innerhalb
von Stützstellen, keine stille Extrapolation. ffill/bfill könnten bei anderen
Datensätzen richtungsbedingt Randlücken behalten. Keine zusätzliche Glättung.
Lange Lücken können unbekannte saisonale Ereignisse enthalten. Die ursprüngliche
vollständige Spalte pieces ist selbst gestört und keine fehlerfreie Referenz;
keine unbelegte Genauigkeitsrangliste oder optimierte Parameterwahl.

1. Ist die visuelle Trennung beobachteter und ergänzter Werte verständlich?
2. Sind Linear/PCHIP als einfache Ausgangspunkte nachvollziehbar begründet,
   einschließlich der anhand der Polynomvarianten sichtbaren Grenzen?
3. Wie sollte der Bericht die Unsicherheit der bis zu 23 Wochen langen Lücken ausdrücken?
4. Ist die Abgrenzung zu Genauigkeitsnachweis und Echtzeitprognose klar?

Keine Arbeit an 11.3. GitHub-CI wird am tatsächlichen neuen PR-Head geprüft;
lokale Ergebnisse behaupten keinen erfolgreichen Actions-Lauf.
