# Exercise 15.2 – Technischer Bericht für den Human Review

**AWAITING HUMAN REVIEW**, 21.11.2026. Keine studentische Beurteilung/Freigabe vorweggenommen.
Codex: offizielle Anforderungen gelesen, Implementierung, Auswertung, Grafiken/Export und technische QA.

## Anforderungen und Methode
„Explore the dataset“: Statistiken je Merkmal/Fehlertyp, mindestens zwei geeignete
Visualisierungen, Datenbefunde und gegebenenfalls beobachtete Schwellen festhalten,
Vergleich mit Subgroup failures. Quelle/Abrufdatum im Notebook. Die Beschreibung war
bereits seit 15.1 bekannt; eine vorgetäuschte Blindanalyse wird ausdrücklich vermieden.

Unveränderte Original-CSV und geprüfter Loader aus 15.1. Sieben numerische/ordinale
Merkmale: count, mean, std (n−1), min, Quartile/Median, max für Flag 0/1 je Untergruppe;
zwei nominale Merkmale mit Häufigkeiten/Anteilen. ID separat als Kennung geprüft.
Vier überlappende Untergruppen, keine Umwandlung in disjunkte Klassen. 56 numerische,
48 kategoriale Zusammenfassungszeilen, 28 beobachtete positive Bereiche, Material-
und Kategoriepaartabellen. Zwei Grafiken: sechs Boxplot-Panels und WDF-Paar-Heatmap.
Keine Modelle, Regeln oder Confusion-Matrizen; kein TRAIN/TEST-Fit/keine Optimierung.

## Wichtigste Ergebnisse
- BEF: positive Schnittgeschwindigkeit 16,33–22,00 m/min, Kühlung 0/25 %. Vereinbar mit niedriger Geschwindigkeit und geringer Kühlung; keine vollständige Regel validiert.
- CCF: Vorschubmedian 121 → 133 mm/min, Kühlungsmedian 50 → 25 %. Starke Überlappungen; Zwei-von-drei-Faktor-Beschreibung wird nicht durch univariate Boxplots bewiesen.
- FWF: insgesamt höherer Geschwindigkeitsmedian 29,60 statt 22,59 m/min, aber 270/278 positive Zeilen gehören zu Material N. Innerhalb jedes Materials niedrigerer Geschwindigkeits- und höherer Vorschubmedian. N: 29,60 statt 30,01 m/min; 222,5 statt 194 mm/min. K/P haben nur 3/5 positive Fälle.
- WDF: in P/N, K/H, N/W keine Markierungen; in sechs anderen Material/Bohrertyp-Paaren alle Zeilen markiert (insgesamt 300). Das stützt die beschriebene Paar-Unverträglichkeit innerhalb dieses Datensatzes.
- positive_bounds.csv und fwf_material_summary.csv dokumentieren beobachtete Bereiche für spätere Aufgaben. Keine allgemeinen Auslösewerte oder unabhängig geprüften Vorhersageregeln behauptet.

## Tatsächlich ausgeführte Prüfungen
- `scripts/uv.cmd run --offline --locked python -m unittest discover -s tests -p test_drilling_exploration.py -v`: **3/3 bestanden**, 0,705 s. Abdeckung aller Prozessmerkmale/Flaggruppen/Nichtmutation; handrechenbares Statistik-Fixture einschließlich Stichproben-std/Quartilen; Material-/WDF-Paarzählungen und bekannte Bereichswerte.
- `scripts/uv.cmd run --offline --locked python scripts/build_exercise_15_2.py --check-html`: **3 frische sequenzielle Codezellen**, keine Zellfehler, zwei eingebettete PNGs. Alle 56 numerischen Tabellenzeilen aus Originalgruppen erneut abgeglichen, alle 48 Kategoriezeilen/Zählungen/Anteile kontrolliert; Fallzahlen und Materialzählungen bestätigt.
- HTML offline Chromium **900/1400 px bestanden**: beide Bilder geladen, keine Seitenfehler/fehlgeschlagenen Anfragen/horizontalen Seitenüberläufe. Beide PNGs und vollständige Browseransichten visuell geprüft: Achsen/Einheiten, Gruppen/Anzahlen, Heatmap-Legende, Tabellen und Interpretation lesbar. Hochauflösende PNGs separat verfügbar.
- Originaldaten-SHA256 und **11 Manifesthashes** bestätigt. **21 Abgabearchive** unverändert; frühere Originalreviews und freigegebene Dateien/15.1-Artefakte nicht geändert. Neue fokussierte CI-YAML eingelesen. Keine Installation oder zusätzliche Testsuite.

Bekannte lokale Jupyter-TCP-Warnung ohne Verschlüsselung; keine dadurch fehlgeschlagene
Ausführung. Keine neuen technischen Fehler oder wissenschaftlichen Ergebnisänderungen.
Aktuelle Head-CI wird erst nach tatsächlichem Abschluss im Draft-PR dokumentiert.

## Grenzen und vier fachliche Reviewfragen
Die Gruppierungen überlappen; Flag=0 bedeutet nicht allgemein fehlerfrei. Materialmix
beeinflusst Gesamtvergleiche. Sehr kleine K/P-FWF-Gruppen, gleiche Beobachtungen ohne ID,
synthetische Daten und vorbekannte Beschreibung begrenzen Aussagen. Boxplot-Ausreißer
sind nur ausgeblendet, nicht gelöscht; CSV-Minima/Maxima enthalten alle Zeilen.
Beobachtete Intervalle sind keine identifizierten universellen Schwellen. WDF-Paaranteile
sind Bestandszählungen, keine allgemeine Fehlerwahrscheinlichkeit oder Kausalität.

1. Ist verständlich, warum der FWF-Gesamtvergleich ohne Materialtrennung irreführend ist?
2. Sind die Schwellenhinweise klar als beobachtete Stichprobenbereiche statt geprüfter Entscheidungsregeln gekennzeichnet?
3. Sind überlappende Fehlergruppen, Flag=0 und der Vergleich mit der bereits bekannten Beschreibung angemessen erklärt?
4. Unterstützen Boxplots und WDF-Heatmap die Interpretation, ohne seltene Fälle oder kausale Grenzen zu übergehen?

Kaggle-Registrierung aus 15.1 weiterhin formal offen. Kein Konto angelegt, keine
studentische Freigabe erfunden. Kein Merge von 15.2, kein Beginn 15.3, keine Einreichung.


---

## Studentischer Originalreview – übergeben am 21.11.2026

HUMAN REVIEW – EXERCISE 15.2

Status: SCIENTIFICALLY APPROVED

1. Materialeffekt bei FWF

Der beobachtete Materialeffekt ist nachvollziehbar. Der Gesamtvergleich der Schnittgeschwindigkeit ist durch die ungleiche Materialzusammensetzung verzerrt.

Innerhalb aller drei Materialien liegt der Schnittgeschwindigkeitsmedian FWF-markierter Fälle niedriger.

Die kleinen Teilgruppen K (n=3) und P (n=5) werden angemessen vorsichtig interpretiert.

Bewertung: BESTANDEN.

2. Stichprobengrenzen und Entscheidungsregeln

Die dokumentierten Bereiche werden korrekt als beobachtete Stichprobengrenzen verstanden.

Sie sind weder validierte Entscheidungsregeln noch allgemeingültige technische Fehlergrenzen.

Bewertung: BESTANDEN.

3. Überlappende Fehlergruppen

Die mögliche gleichzeitige Kennzeichnung mehrerer Fehlergruppen ist berücksichtigt.

Flag=0 für einen bestimmten Fehlertyp bedeutet nicht zwangsläufig, dass keine andere Fehlerart vorliegt.

Bewertung: BESTANDEN.

4. Visualisierungen

Die numerischen Boxplots zeigen die Unterschiede und Überschneidungen der Merkmalsverteilungen.

Die WDF-Heatmap macht den Zusammenhang zwischen Material, Bohrertyp und Fehlerkennzeichnung deutlich.

Die grafischen Ergebnisse unterstützen die vorsichtige Interpretation.

Bewertung: BESTANDEN.

5. Wissenschaftliche Grenzen

Die Analysen sind deskriptiv.

Aus den beobachteten Zusammenhängen ergeben sich keine validierten kausalen Aussagen oder universellen Fehlerregeln.

Eine unabhängige erneute Notebook-Ausführung war nicht Bestandteil dieses Human Reviews.

GESAMTENTSCHEIDUNG:
SCIENTIFICALLY APPROVED.

Keine zusätzlichen wissenschaftlichen Analysen erforderlich.

Die aus Exercise 15.1 weiterhin offene Kaggle-Registrierung bleibt dokumentiert.

Keine Universitätseinreichung.


---

## Codex-Abschlussprüfung / autorisierter Merge – 21.11.2026

Originalreview vollständig und wortgetreu in 32f2342 gesichert. Wissenschaftlich
SCIENTIFICALLY APPROVED; keine zusätzlichen studentischen Tests erfunden.
Drei bestehende Tests erneut bestanden (0,522 s), drei frische sequenzielle Codezellen,
HTML offline 900/1400 px und beide eingebetteten PNGs geprüft. Alle 56 numerischen
und 48 kategorialen Ergebniszeilen erneut aus Originaldaten abgeglichen. Elf
Manifesthashes bestätigt; wissenschaftliche CSV/JSON und beide PNGs bytegleich
mit 3334424. 21 Abgabearchive unverändert. Keine neuen Analysen oder wissenschaftlichen
Änderungen; nur Status und Prüfdokumentation. Bekannte lokale Jupyter-TCP-Warnung
ohne Zellfehler. Registrierung aus 15.1 bleibt ausdrücklich formal offen.

Der aktuelle Nutzerauftrag autorisiert den regulären Merge von PR #19 nach beiden
erfolgreichen aktuellen Head-CI-Läufen, Konflikt-/Kommentarprüfung und Erhalt aller
Reviews. Kein Merge in diesem Eintrag vorweggenommen; tatsächlicher SHA folgt im
Projektstatus. Keine Einreichung; 15.3 erst nach erfolgreichem Merge implementieren.
