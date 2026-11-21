# Exercise 15.4 – Technischer Bericht und Human-Review-Fragen

**AWAITING HUMAN REVIEW – 21.11.2026.** Kein studentischer Review oder Freigabe erfunden.

## Anforderungen und Umsetzung
Offizielle Aufgabe: „From exploration to a rule-based failure model“. Vier Python-Regelfunktionen aus 15.2/15.3, je eine Confusion-Matrix; je ein flacher Entscheidungsbaum und Vergleich der Erklärbarkeit. Quelle/Abrufdatum, Kriterien und Begründung im Notebook. Codex hat Anforderungen, Code, deutsche Erläuterungen, Tests, Ausführung und Export unterstützt.

Unveränderte XAI-Drilling-Daten, alle vier Fehlerlabels getrennt binär; Mehrfachlabels erhalten. BEF: vc/Kühlung, CCF: sieben beobachtete Wertebereiche, FWF: materialbezogene vc/vf-Grenzen, WDF: Material-/Bohrertyp-Paare. Keine Schwellenoptimierung. Gemeinsamer Gruppensplit Seed 42: 15.998 TRAIN / 4.002 TEST; identische Eingangsmerkmale gruppiert. Keine ID/Fehlerflags als Features. TRAIN-only One-Hot-Kodierung und Bäume Tiefe 3, ungewichtet. Keine Zusatzmodelle.

## Tatsächliche Ergebnisse
| Ziel | Regel F1 | Baum F1 | Regel FP/FN | Baum FP/FN |
|---|---:|---:|---:|---:|
| BEF | 0,266667 | 0,666667 | 319/0 | 0/29 |
| CCF | 0,032487 | 0,873950 | 3812/0 | 3/12 |
| FWF | 0,982456 | 0,953271 | 2/0 | 0/5 |
| WDF | 1,000000 | 0,000000 | 0/0 | 0/58 |

TEST-positive Fälle: 58/64/56/58. Die CCF-Merkmalsbox trennt Fehler nicht ausreichend. Der WDF-Baum sagt auf TEST ausschließlich 0 voraus; trotz flacher Struktur keine brauchbare Erkennung. Kein nachträgliches Tuning zur Ergebnisverbesserung. Kurze BEF/WDF-Regeln sind direkt erklärbar, die CCF-Box mit 14 Grenzen deutlich weniger. Die bevorzugte Erklärung für Prozessingenieure bleibt fachlich zu prüfen.

## Tatsächlich ausgeführte Validierung
- `scripts/uv.cmd run --offline --locked python -m unittest discover -s tests -p test_rule_models.py -v`: **3/3 bestanden, 1,846 s**. Regelgrenzen/labelunabhängige Funktionen; Gruppentrennung und Testlabel-Perturbation ohne Änderung trainierter Vorhersagen; sämtliche acht Confusion-Matrizen/F1 aus Einzelvorhersagen.
- `scripts/uv.cmd run --offline --locked python scripts/build_exercise_15_4.py --check-html`: **drei Codezellen frisch sequenziell**, keine Zellfehler. Nach Ergänzung konkreter Interpretation erneut ausgeführt.
- Builder prüft 16.008 Vorhersagezeilen (4 × 4.002), IDs/Labels/Regelvorhersagen, alle acht Matrizen sowie Precision/Recall/F1 unabhängig anhand CSVs. Gleicher Split und keine identischen Eingangsmerkmale in TRAIN und TEST.
- Offline-Chromium 900/1400 px: eingebettete Grafik geladen, keine Seitenfehler, fehlgeschlagenen Abrufe oder Seitenüberläufe. Vollständige Screenshots beider Breiten und Grafik visuell geprüft; Beschriftungen/Matrixorientierung und konkrete Interpretation lesbar.
- Rohdaten-SHA256 und **12 Manifesthashes** bestätigt; **21 Abgabearchive unverändert**. Frühere wissenschaftliche Dateien und Originalreviews nicht geändert. Bestehende Umgebung ohne neue Abhängigkeiten genutzt.
- Lokale Jupyter-TCP-Warnung ohne Ausführungsfehler. Kein unabhängiger realer Datentest behauptet. Aktuelle Push-/PR-CI nach Push tatsächlich prüfen; Links/Ergebnis im Draft-PR.

## Wissenschaftliche Grenzen
Die Schwellen wurden bereits anhand aller Daten in 15.2/15.3 betrachtet; damit ist TEST für die Regeln kein unabhängiger Holdout. Auch der Gesamtvergleich ist retrospektiv, keine unverzerrte externe Güteschätzung. Die ausschließlich auf TRAIN angepassten Bäume ändern daran nichts. Synthetische Daten, seltene Teilgruppen, überlappende Labels und ein fester Split begrenzen Aussagen. F1=1 für WDF belegt nur Übereinstimmung mit den ausgewerteten Labels. Keine Kausalität oder Ausfallwahrscheinlichkeit behauptet. Kaggle-Registrierung weiterhin formal offen.

## Vier Fragen für den studentischen Human Review
1. Sind die vier Regeln und ihre Herkunft aus 15.2/15.3 nachvollziehbar?
2. Ist klar, warum die CCF-Bereichsregel viele Fehlalarme erzeugt und der WDF-Baum hier alle Fehler übersieht?
3. Welche Darstellung würdest du einem Prozessingenieur erklären: kurze Regeln oder Baumtexte, und weshalb?
4. Sind die Grenzen durch vorherige Gesamtdatenexploration, seltene Fehler und den festen Split ausreichend deutlich?

Kein Merge von 15.4, keine weitere Aufgabe und keine Universitätseinreichung.


## Studentischer Originalreview – 21.11.2026

Status: SCIENTIFICALLY APPROVED.

1. Die vier Regeln und ihre Herkunft aus Exercise 15.2/15.3 sind nachvollziehbar dokumentiert.

Bewertung: BESTANDEN.

2. Die Confusion-Matrizen und F1-Werte sind korrekt. Die zahlreichen Fehlalarme der CCF-Regel sowie die vollständig übersehenen WDF-Fehler des Entscheidungsbaums sind verständlich erklärt.

Bewertung: BESTANDEN.

3. Für Prozessingenieure sind einfache Regeln zunächst besonders verständlich. Entscheidungsbäume ermöglichen ergänzende Vergleiche, müssen aber anhand der tatsächlichen Fehlklassifikationen beurteilt werden.

Bewertung: BESTANDEN.

4. Die wissenschaftlichen Grenzen sind ausreichend dokumentiert. Besonders wichtig ist, dass die Regeln aus der vorherigen Gesamtdatenexploration stammen und der retrospektive Test keine unabhängige Validierung der Regeln darstellt.

Bewertung: BESTANDEN.

GESAMTENTSCHEIDUNG:\
SCIENTIFICALLY APPROVED.

Zusätzliche Prüfung im Human Review:

- Alle acht Confusion-Matrizen unabhängig aus den exportierten Vorhersagen nachgerechnet: korrekt.
- 4.002 eindeutige Test-IDs mit jeweils vier Fehlerauswertungen bestätigt.
- Elf hochgeladene Ergebnisartefakte stimmen mit den dokumentierten SHA-256-Prüfsummen überein.
- GitHub-PR und erfolgreiche CI geprüft.

Keine zusätzlichen Modelle oder Optimierungen erforderlich.


## Codex-Abschlussabgleich – 21.11.2026

**APPROVED (wissenschaftlich); Kaggle-Registrierung weiterhin offen.** Student hat den regulären Merge nach erfolgreicher Abschlussprüfung ausdrücklich autorisiert. Originalreview oben unverändert, frühere Prüfberichte als historische Einträge erhalten.

Erneut tatsächlich geprüft: acht Confusion-Matrizen und F1 aus 16.008 Vorhersagezeilen; 4.002 eindeutige IDs mit jeweils vier Fehlerauswertungen; zwölf Manifesthashes (elf Ergebnisartefakte plus Notebook) und 21 unveränderte Abgabearchive. Keine wissenschaftlichen Änderungen, keine zusätzliche Ausführung behauptet. Aktuelle Head-CI und Reviewthreads werden unmittelbar vor dem Merge überprüft; tatsächliche Merge-SHA und CI-Links im PR-Abschluss und Abschlussbericht. Keine Universitätseinreichung oder weitere Aufgabe.
