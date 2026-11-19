# Exercise 14.2 – Technischer Prüfbericht

**AWAITING HUMAN REVIEW**, 19.11.2026. Keine studentische Bewertung oder Freigabe liegt vor.
Codex: Aufgaben-/Kontextlektüre, Implementierung, Tests, Notebook, Grafiken, HTML und Dokumentation.

## Anforderungen, Methode und Ergebnisse
Offizielle Aufgabe und Kontext: Links/Abrufdatum direkt im Notebook. OSF-Regel visualisiert,
Entscheidungsgrenzen für Tiefen 1/2/4/8 mit DecisionBoundaryDisplay und 11.000-Hyperbel;
Kursbaum um wearadjTorque und Type ergänzt. Kursparameter Seed 42, Mindestblattgröße 5,
Mindestteilungsgröße 5 übernommen. Type durch feste Indikatoren, keine Fehlerflags/IDs als Eingaben.

10.000 Zeilen, 98 OSF (L/M/H: 87/9/2). Beschriebene Type-Regel ohne Abweichung.
Bei Kurstiefe 3: 43 / 22 / 2 Anpassungsfehler (Basis / + Produkt / + Type).
Unter Tiefen 1–8 ist 3 die kleinste mit höchstens zwei Fehlern; dies ist ausdrücklich
unsere Definition von „nahezu perfekt“, keine offizielle Vorgabe. Erste Produktschwelle
10.998,5 min·Nm, M-Schwelle 12.128,5. H erhält keine eigene Schwelle; zwei H-OSF verfehlt.

Fester stratifizierter 80/20-Split: TRAIN 8.000/78 OSF, TEST 2.000/20 OSF. Tiefe 3
vorab aus Kurs übernommen, keine TEST-Optimierung. Fehler 14/8/1, F1 0,611111/0,8/0,974359.
Erklärende Gesamtanpassung und separate TEST-Prüfung klar getrennt. Keine Skalierung/
gelernten Vorverarbeitungsschritte; zeilenweise physikalische Features. Keine Aufgabe 14.3/14.4 vorweggenommen.

## Tatsächlich ausgeführte Prüfungen
Im bestehenden uv-Lockfile/Environment, keine neuen Abhängigkeiten:
- `scripts/uv.cmd run --offline --locked python -m unittest discover -s tests -p test_overstrain.py -v`: **3 Tests bestanden**, zuletzt 1,171 s. Featureformeln/Nichtmutation, Regel/Ergebnisse, TRAIN/TEST-Disjunktheit und ausschließlich TRAIN beim Fit der drei separaten TEST-Modelle.
- `scripts/uv.cmd run --offline --locked python scripts/build_exercise_14_2.py --check-html`: **3 Codezellen frisch sequenziell**, keine Zellfehler, drei eingebettete PNGs; unabhängige Regelzählung und Tabellenkonsistenz.
- HTML offline Chromium bei **900/1400 px**: drei Bilder geladen, keine Seitenfehler/fehlgeschlagenen Anfragen/horizontalen Seitenüberläufe. Alle PNGs und HTML-Ansichten visuell kontrolliert. Detaillierte Baumknoten bei 900 px klein: Original-PNG und Textausgabe stehen zusätzlich bereit.
- Rohdaten-SHA256 und **9 Manifesthashes** geprüft; **21 Archive** unverändert. Frühere Lösungen/Reviews und Abgabedateien unverändert. YAML der erweiterten fokussierten Branch-CI erfolgreich eingelesen.

Erster Exportversuch scheiterte an fehlenden Inlinebildern unter Agg. Explizites Einbetten
korrigiert, anschließend frische Ausführung/HTML bestanden. Mathematisches Produkt als
Unicode dargestellt, damit kein Online-MathJax erforderlich ist. Bekannte Warnung: lokaler
Jupyter-TCP-Transport unverschlüsselt; keine Ausführung dadurch fehlgeschlagen.
Head-CI wird erst nach Push tatsächlich geprüft und im Draft-PR verlinkt.

## Grenzen und vier Fragen zum Human Review
Synthetische Daten und nur ein fester Split; keine externe Validierung oder Seed-Studie.
Seltene OSF, besonders nur zwei H-Fälle. Mindestblattgröße verhindert hier perfekte
Anpassung; Gesamtanpassungszahlen sind kein unabhängiger Gütenachweis. Keine Kausalität
oder allgemeine Überlegenheit behauptet. Type-L-Hyperbel gilt nicht für alle Varianten.

1. Ist die Trennung zwischen beschriebener Regel, erklärender Anpassung und TEST-Ergebnis nachvollziehbar?
2. Erklären Treppengrenzen und Produktmerkmal verständlich, warum die Baumstruktur einfacher wird?
3. Sind „nahezu perfekt“, die gelernten Schwellen und die verbleibenden zwei H-Fehler ausreichend vorsichtig erklärt?
4. Sind Abbildungen, Tabellen und Einschränkungen für dich mündlich erklärbar und fachlich vollständig?

Kein positiver Human Review vorweggenommen; kein Merge, kein Beginn von 14.3 und keine Einreichung.
