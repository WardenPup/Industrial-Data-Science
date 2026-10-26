# Exercise 11.4 – Human-AI Review

Status: AWAITING HUMAN REVIEW

## KI-Beitrag
Codex hat die offiziellen Anforderungen analysiert, die robuste STL mit residualer
Drei-Sigma-Regel implementiert und Notebook, Tests und Exporte erstellt.
Originalspalte pieces unverändert; kein Rückgriff auf imputierte Werte.

## Wissenschaftliche Einordnung
26 Kandidaten (2,4904 %), alle negative Residuen. Modellabhängige Markierungen,
keine gesicherten Messfehler. Parameter und Grenzen siehe Notebook und Anforderungen.

## Fragen an den studentischen Review
1. Ist die residualbasierte Abgrenzung gegenüber saisonal hohen/niedrigen Werten nachvollziehbar?
2. Stimmen die markierten Wochen in beiden Grafiken überein und wirken sie fachlich plausibel?
3. Sind Drei-Sigma-Heuristik, geschätzte Komponenten und fehlende Fehlerlabels klar unterschieden?
4. Sind die gewählten STL-Annahmen und ihre Grenzen angemessen erklärt?

## Studentische Rückmeldung
Noch nicht erhalten. Keine studentische Prüfung oder Freigabe behauptet.

## Technische Prüfung
Am 26.10.2026 tatsächlich ausgeführt (projektlokales uv, --offline --locked):
- python -m unittest discover -s tests -v: 40 Tests erfolgreich, 2,740 s.
- python scripts/build_exercise_11_4.py: frischer Kernel, drei sequenzielle Codezellen,
  zwei dekodierte eingebettete Bilder, keine Ausführungsfehler. Grenzen unabhängig
  mit NumPy nachgerechnet; additive Identität und unveränderte Eingabe geprüft.
- python scripts/check_exercise_11_4_html.py: offline bei 900/1400 px, beide Bilder
  geladen, keine Seitenfehler und kein horizontaler Überlauf.
- Beide PNGs visuell geprüft: lesbare Titel, Achsen, Einheiten und Marker;
  Residuenlegende nach außen verschoben, damit sie keine Kandidaten verdeckt.
- Rohdaten-SHA256 und sieben Artefaktchecksummen im validation_manifest.json.
- Warnung: lokaler Jupyter-Kernel kommuniziert über unverschlüsseltes TCP;
  keine Ausführungsfehler. Keine neue Abhängigkeit.
Kein Merge und keine Abgabe. GitHub-CI wird nach Push separat geprüft.
