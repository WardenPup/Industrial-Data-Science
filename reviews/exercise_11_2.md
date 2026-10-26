# Aufgabe 11.2 – Human-AI-Review

Status: **APPROVED** (fachliche Freigabe vom 26.10.2026).
Studentischer Originalreview unverändert unten dokumentiert; keine methodischen
Korrekturen angefordert. Erneute technische Prüfung bestanden. Merge-Erlaubnis
weiterhin ausstehend. Keine Universitätseinreichung. Die Erstprüfungsabschnitte
sind historisch; aktueller KI-Nachweis getrennt nach dem studentischen Text.

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


# Human Review – Aufgabe 11.2

**Datum:** 26.10.2026  
**Aufgabe:** Vergleich von sechs Imputationsverfahren für fehlende Produktionsdaten  
**KI-Unterstützung:** Codex  
**Status:** APPROVED – Fachliche Prüfung abgeschlossen

## 1. Ziel der Prüfung

Ziel der Aufgabe ist der Vergleich von sechs Verfahren zur Imputation fehlender Wochenwerte in einer Produktionszeitreihe.

Geprüft wurde insbesondere,

- ob die ursprünglichen beobachteten Werte erhalten bleiben,
- ob alle fehlenden Wochen ergänzt werden,
- wie sich die verschiedenen Verfahren bei kurzen und langen Lücken verhalten,
- und ob die Grenzen der Verfahren wissenschaftlich korrekt dokumentiert sind.

Die Bewertung erfolgt bewusst qualitativ. Es liegt keine fehlerfreie Referenz für die fehlenden Wochen vor.

## 2. Datenbasis und Integrität

Die Aufgabe baut auf der in 11.1 freigegebenen geglätteten Zeitreihe mit Lücken auf.

Die Zeitreihe umfasst insgesamt 1.044 Wochen. Davon fehlen 367 Wochen, während 677 Wochen beobachtet vorliegen.

Laut technischer Validierung und begleitender Dokumentation gilt:

- alle sechs Verfahren ergänzen die 367 fehlenden Wochen,
- alle 677 ursprünglich vorhandenen Werte bleiben unverändert,
- die Zeitachse bleibt vollständig erhalten,
- die Imputationen sind von den beobachteten Werten klar unterscheidbar.

Diese Bedingungen sind fachlich wesentlich und wurden erfüllt.

## 3. Verwendete Verfahren

Die sechs betrachteten Imputationsverfahren sind:

1. Forward Fill  
2. Backward Fill  
3. Lineare Interpolation  
4. PCHIP  
5. Polynominterpolation Grad 2  
6. Polynominterpolation Grad 5  

Die Verfahren repräsentieren unterschiedliche Grundideen:

- **Forward Fill** und **Backward Fill** übertragen vorhandene Nachbarwerte stufenförmig in Lücken.
- **Lineare Interpolation** verbindet Stützstellen geradlinig.
- **PCHIP** erzeugt eine glatte, formtreue Interpolation ohne unnötige Schwingungen.
- **Polynominterpolation Grad 2 und 5** erzeugt glatte Kurven, kann jedoch stärker auf Randbedingungen und Lückenlängen reagieren.

Die Auswahl der Verfahren ist für die Aufgabe sinnvoll und didaktisch gut geeignet.

## 4. Prüfung der Visualisierungen

Die bereitgestellten Grafiken sind verständlich beschriftet und methodisch sinnvoll aufgebaut.

### 4.1 Gesamtvergleich der imputierten Wochen

Für jedes Verfahren wird im oberen Teil die vollständige Originalreihe `pieces` gezeigt, darunter die freigegebene 5‑Wochen-Medianreihe mit Lücken, und im unteren Teil ausschließlich die ergänzten Wochen des jeweiligen Verfahrens.

Diese Darstellung ist sehr hilfreich, weil die imputierten Werte nicht mit den beobachteten Werten vermischt werden.

Die Originaldaten, die lückenhafte Ausgangsreihe und die ergänzten Werte sind visuell klar getrennt.

### 4.2 Beobachtete Unterschiede zwischen den Verfahren

#### Forward Fill

Forward Fill erzeugt abschnittsweise konstante Plateaus, da fehlende Werte mit dem jeweils letzten bekannten Wert fortgeschrieben werden.

Das Verfahren ist einfach und stabil, bildet jedoch innerhalb längerer Lücken keinerlei Zwischenentwicklung ab.

#### Backward Fill

Backward Fill zeigt dasselbe Prinzip in umgekehrter Richtung: Fehlende Wochen erhalten den jeweils nächsten späteren bekannten Wert.

Auch hier entstehen konstante Stufen. Die Methode kann bei längeren Lücken zu unplausiblen frühzeitigen Sprüngen führen.

#### Lineare Interpolation

Die lineare Interpolation verbindet die bekannten Randpunkte durch gerade Linien.

Das Verfahren ist leicht interpretierbar und erzeugt keine übermäßigen Schwingungen. Allerdings werden Krümmungen, saisonale Muster oder Zwischenereignisse in längeren Lücken nur sehr vereinfacht abgebildet.

#### PCHIP

PCHIP liefert glatte Verläufe, die den beobachteten Randverlauf gut aufnehmen und zugleich vergleichsweise zurückhaltend bleiben.

Im Vergleich zur linearen Interpolation wirkt PCHIP natürlicher, ohne so stark zu überschwingen wie höhergradige Polynomverfahren.

#### Polynom Grad 2

Die quadratische Interpolation erzeugt glatte, gebogene Verläufe und reagiert bereits sichtbar stärker auf größere Lücken als lineare Verfahren.

Sie bleibt jedoch insgesamt noch relativ kontrolliert.

#### Polynom Grad 5

Die Polynominterpolation fünften Grades zeigt die stärksten Krümmungen und die deutlichste Empfindlichkeit gegenüber Lückenstruktur und Randpunkten.

In mehreren Lücken entstehen stärker ausgeprägte Bögen und lokale Verläufe, die zwar mathematisch glatt, aber nicht automatisch inhaltlich plausibel sind.

## 5. Längste Lücke: 23 Wochen

Die wichtigste Vergleichsgrafik zeigt die erste längste Lücke mit 23 Wochen.

Hier werden die Verfahrensunterschiede besonders deutlich.

### Beobachtungen

- **Forward Fill** bleibt über fast die gesamte Lücke konstant auf dem letzten bekannten Niveau und springt erst am Ende auf den nächsten beobachteten Bereich.
- **Backward Fill** setzt bereits zu Beginn der Lücke den späteren Zielwert und bleibt dann weitgehend konstant.
- **Lineare Interpolation** verläuft als direkte Verbindung zwischen Anfangs- und Endniveau.
- **PCHIP** folgt einem glatten ansteigenden Verlauf, der die Randwerte formtreu verbindet.
- **Polynom Grad 2** zeigt ebenfalls einen glatten Anstieg mit merklicher Krümmung.
- **Polynom Grad 5** fällt zunächst stark ab und steigt später wieder deutlich an. Dadurch entsteht ein ausgeprägter nichtmonotoner Verlauf mit erkennbarem Überschwingen.

### Fachliche Bewertung

Diese Grafik ist sehr gelungen, weil sie anschaulich macht, dass das Ergebnis der Imputation stark von der Methode abhängt.

Gerade bei langen Lücken lässt sich nicht begründen, dass ein optisch glatter oder mathematisch anspruchsvollerer Verlauf automatisch besser ist.

Besonders die Polynominterpolation fünften Grades illustriert nachvollziehbar die im Bericht erwähnte Gefahr von Überschwingern.

## 6. Fachliche Interpretation

Die Aufgabe wird fachlich korrekt interpretiert.

Positiv ist insbesondere:

1. Es wird **keine Genauigkeitsrangliste** behauptet.
2. Es wird klar gemacht, dass ohne bekannte wahre Werte in den Lücken keine echte Genauigkeitsbewertung möglich ist.
3. Die Unterschiede zwischen den Verfahren werden **qualitativ** diskutiert.
4. Die lange Lücke wird als kritischer Fall besonders hervorgehoben.
5. Mögliche Polynomüberschwinger werden nicht verschwiegen.

Das ist wissenschaftlich sauber.

Eine vollständig imputierte Zeitreihe ist nicht mit einer tatsächlich beobachteten Zeitreihe gleichzusetzen. Die Aufgabe behandelt diesen Punkt angemessen.

## 7. Grenzen der Verfahren

Die dokumentierten Grenzen sind fachlich angemessen und aus den Grafiken nachvollziehbar:

- Lücken von bis zu 23 Wochen sind lang genug, dass alle Verfahren mit erheblicher Unsicherheit arbeiten.
- Stufenverfahren wie Forward Fill und Backward Fill ignorieren Zwischenentwicklungen.
- Lineare Interpolation kann saisonale oder gekrümmte Verläufe glätten.
- PCHIP ist formtreu, aber ebenfalls nur eine Schätzung.
- Höhergradige Polynome können unplausible Zwischenwerte oder starke Krümmungen erzeugen.
- Eine qualitative Plausibilität ersetzt keine quantitative Gütebewertung.

Diese Grenzen wurden insgesamt überzeugend berücksichtigt.

## 8. Technische Validierung

Laut Codex wurden folgende Prüfungen erfolgreich durchgeführt:

| Prüfung | Ergebnis |
|---|---|
| Automatisierte Tests | 33 bestanden |
| Notebook-Codezellen | 10 sequenziell ausgeführt |
| Visualisierungen | 7 visuell geprüft |
| HTML-Prüfung | 900 px und 1400 px bestanden |
| GitHub Push-CI | erfolgreich |
| GitHub PR-CI | erfolgreich |
| Pull Request #6 | konfliktfrei, nicht gemergt |

Diese technischen Prüfungen werden als KI-gestützte beziehungsweise automatisierte Validierung dokumentiert.

Eine zusätzliche unabhängige lokale Testausführung durch den Studierenden wird nicht behauptet.

## 9. Gesamtbewertung

Die Aufgabe ist fachlich überzeugend umgesetzt.

Die sechs Imputationsverfahren werden nachvollziehbar verglichen, ohne ihre Aussagekraft zu übertreiben. Die Integrität der vorhandenen Daten bleibt erhalten, alle fehlenden Wochen werden ergänzt und die Visualisierungen machen die methodischen Unterschiede gut sichtbar.

Besonders positiv ist die explizite Darstellung der 23‑Wochen-Lücke und der Verzicht auf eine unbegründete Genauigkeitsrangliste.

Bei der Durchsicht der bereitgestellten Ergebnisse wurden keine wesentlichen fachlichen Fehler festgestellt.

**Human Review: APPROVED**

Keine inhaltlichen Korrekturen erforderlich. Der Pull Request bleibt bis zur ausdrücklichen Merge-Freigabe ungemergt.


---

## KI-Nachprüfung nach studentischem Review – 26.10.2026

Originalwortlaut des studentischen Reviews vollständig und unverändert erhalten.
Git-Diff gegen e06d2f2: 190 angehängte Zeilen, separat als 452843a committed.
Vorherige Inhalte blieben im Reviewcommit unverändert; keine Überschreibung
von Autor-/Committermetadaten. Codex führte den Commit aus, der Text stammt
nach ausdrücklicher Bestätigung vom Studierenden. Fachliche Freigabe APPROVED,
keine methodische Korrekturanforderung; Merge-Erlaubnis weiterhin ausstehend.

### Aussagenabgleich und präzisierter Langlückenbefund

| Reviewaussage | Tatsächliche Nachprüfung |
|---|---|
| Sechs Methoden auf 11.1-Eingabe | Hash des freigegebenen Medians bestätigt; ffill/bfill/linear/Polynom 2/5/PCHIP |
| 1.044 Wochen, 367 fehlend, 677 beobachtet | alle Zahlen bestätigt; Zeitachse in CSV und allen Ergebnisreihen identisch |
| Alle Fehlwochen ergänzt | pro Verfahren 367 neue endliche Werte, 0 NaNs verbleibend |
| Vorhandene Werte unverändert | alle 677 Werte in jedem berechneten Ergebnis exakt gleich, zusätzlich CSV-Rundungsprüfung |
| Langlücke 23 Wochen | erste längste Lücke 11.12.2011–13.05.2012, 32 Lücken insgesamt |
| Stufen bei Forward/Backward Fill | jeweils konstanter linker/rechter Randwert innerhalb der Lücke |
| Linear/PCHIP zurückhaltend | lineare Referenz bestätigt; PCHIP in dieser Lücke monoton, ohne Überschreiten der Randwerte |
| Ausgeprägter Grad-5-Rückgang | Minimum 357,9956960057037 bei Randwerten 473,54887536096425 / 606,8249557703607 |
| Polynomüberschwinger dokumentiert | 78 / 189 Werte außerhalb der bekannten Lückenrandwerte bei Grad 2 / 5, sonst null |
| 33 Tests / 10 Zellen / 7 Grafiken | erneut ausgeführt bzw. geprüft; tatsächliche Ergebnisse unten |

Technische Präzisierung durch Codex, keine zusätzliche studentische Beobachtung:
Der im Review genannte Anstieg von Grad 2 beschreibt die Gesamtentwicklung über
23 Wochen. Die Kurve ist nicht streng monoton: am Anfang ein kleiner Rückgang,
kleinster Wochenschritt einschließlich Randpunkten -1,407807929401372 Stück.
Das Originalreview bleibt unverändert; kein methodischer Korrekturbedarf entsteht.
Subjektive Plausibilitätsbewertungen im menschlichen Review bleiben als solche
stehen und werden nicht als rechnerisch bewiesene Genauigkeit ausgegeben.

`scripts/check_exercise_11_2_review.py` nutzt separate Referenzberechnungen:
Indexsuche für Forward/Backward Fill, NumPy interp für linear, direkte SciPy-
Spline-/PCHIP-Aufrufe auf relativen Wochenpositionen für die weiteren Verfahren.
Übereinstimmung ist innerhalb dokumentierter numerischer Toleranz geprüft;
diese API-Gegenprüfung ist kein unabhängiger Nachweis unbekannter wahrer Werte.
Ein separater Positionsscan prüft alle Lücken. Gespeicherte Notebooktabellen,
Ausgabeströme, Lücken-/Methoden-CSV, summary.json und alle 13 Manifesthashes stimmen.
Die tatsächlichen Linienpfade sämtlicher 18 Kurs-Teilbilder und der sechs
Vergleichslinien wurden gegen beobachtete/ergänzte Werte und NaN-Masken geprüft.

### Tatsächlich ausgeführte technische Prüfungen

- `scripts/uv.cmd sync --offline --locked`: 111 aufgelöst, 107 installierte geprüft.
- `scripts/uv.cmd run --offline --locked python -m unittest discover -s tests -v`:
  33 Tests, 0,581 s, OK.
- `scripts/uv.cmd run --offline --locked python scripts/build_exercise_11_2.py`:
  zehn Codezellen in neuem Kernel sequenziell 1–10; sieben eingebettete echte PNGs,
  Rohdaten-/Eingabehash, CSV-Invarianten und lineare NumPy-Referenz erfolgreich.
- `scripts/uv.cmd run --offline --locked python scripts/check_exercise_11_2_review.py`:
  alle obigen Aussagen, Ergebnisse, Linienpfade und Hashes erfolgreich geprüft;
  human_review_verification.json enthält die tatsächlich berechneten Zahlen.
- `scripts/uv.cmd run --offline --locked python scripts/check_exercise_11_2_html.py`:
  offline bei 900/1400 px, sieben Bilder geladen, keine Seitenfehler/Überläufe.
- Alle sieben erneut erzeugten PNGs visuell geprüft und bytegleich mit e06d2f2;
  Achsen, Einheiten, Legenden und Lückentrennung unverändert. HTML-Freigabehinweise
  anhand der Browserbilder geprüft, wissenschaftliche Aussagen unverändert.

Der erste Lauf des neuen Nachprüfers scheiterte wegen eines Spaltenzugriffs
`results.ffill`, der die DataFrame-Methode statt der Spalte adressierte.
Auf expliziten Spaltenzugriff korrigiert; keine Änderung am wissenschaftlichen
Imputationscode. Ein Hinweis zu pandas/NumPy-Zeiteinheiten im Nachprüfer wurde
mit positionsbasierter Auswahl des identischen Wochenfensters behoben. Der
vollständige abschließende Nachprüfer bestand ohne diese Fehler/Hinweise.
Bekannter lokaler Jupyter-TCP-Hinweis beim Kernelstart; keine Notebookfehler.

Keine zusätzlichen studentischen Tests oder Beobachtungen behauptet. Die
bekannten Grenzen bleiben: unbekannter Verlauf langer Lücken, mögliche Polynom-
überschwinger, keine fehlerfreie Ground Truth und keine Echtzeitprognose.
GitHub-CI wird am neuen Head geprüft und mit tatsächlichen Ergebnissen im PR
verlinkt. Keine Arbeit an 11.3, kein Merge und keine Universitätseinreichung.
