# Aufgabe 11.3 – Human-AI-Review

Status: **AWAITING HUMAN REVIEW** (26.10.2026).
Noch kein studentisches Feedback, keine wissenschaftliche Freigabe und keine
Merge-Erlaubnis für 11.3. Keine Universitätseinreichung.

## Anforderungen und KI-Beitrag

Quellen, Lernziele, Abnahme und Abgabedateien stehen in
docs/EXERCISE_11_3_REQUIREMENTS.md (tatsächlich am 26.10.2026 gelesen).
Codex erstellte Anforderungen, Berechnung, Kursgrafik-Anpassungen, Notebook,
Export, Tests und technische Dokumentation. Keine menschlichen Beobachtungen
oder Tests erfunden. Wiederverwendet: freigegebener 11.1-Median/Hashprüfung,
lineare Interpolation aus 11.2 und Kurs-Produktionsplotfunktion.
Freigegebene Lösungen/Reviews und Rohdaten werden nicht verändert.

Zusätzlich erforderlich: statsmodels 0.15.0, ausschließlich projektlokal über
uv ergänzt und gelockt. Sechs neue Pakete einschließlich seiner Abhängigkeiten,
keine vorhandene Paketversion geändert. Beim ersten Add-Versuch interpretierte
der cmd-Wrapper die Versionszeichen als Umleitung; der Vorgang scheiterte.
Die selbst erzeugte temporäre Datei wurde entfernt, danach der vorhandene lokale
uv.exe direkt mit korrekt zitiertem Argument verwendet. Keine globalen Pakete.

## Anforderung für Anforderung

| Offizielle Aufgabe | Umsetzung |
|---|---|
| Geglättete Eingabe mit Lücken aus 11.1 | load_smoothed_input mit kanonischem Werte-/NaN-Hash |
| Vorläufig einfach imputieren | lineare Interpolation innerhalb bekannter Randwerte |
| STL zerlegen | additives STL, period 52, seasonal 13, trend 101, low_pass 53, robust True |
| Komponenten mit Kursfunktion darstellen | seasonal_decompose_seaborn, vier Teilbilder, deutsche Labels |
| Saison von lückenhafter Eingabe abziehen | source − seasonal; ursprüngliche 367-NaN-Maske erhalten |
| Saisonbereinigte Reihe imputieren | erneute lineare Interpolation, keine Wiederverwendung der gefüllten Vorstufe |
| Saison zurückaddieren | completed + seasonal, bekannte 677 Medianwerte exakt erhalten |
| Endgrafik und Diskussion | dreiteilige Kursgrafik, Zwischenstufe und Langlückenvergleich |

## Tatsächliche Ergebnisse

1.044 Wochen, 677 bekannte und 367 fehlende Medianwerte. STL-Vorstufe vollständig;
nach Saisonabzug wieder exakt 367 fehlende Werte an identischen Positionen.
Endergebnis endlich und vollständig, alle 677 bekannten Werte exakt erhalten,
keine negativen Ergänzungen. Additive Rekonstruktionsabweichung maximal
1,1368683772161603e-13 Stück pro Woche. Mittlere absolute Differenz gegenüber
einfacher Linearimputation an den 367 Fehlwochen: 9,746198652352929; Maximum:
75,2469305103034 Stück pro Woche. Diese Größen messen keine Genauigkeit.
Im 23-Wochen-Ausschnitt 11.12.2011–13.05.2012 fällt die STL-gestützte Kurve
anfangs unter den linken Stützwert und liegt später über der linearen Schätzung.
Das ist eine beobachtete Schätzform, kein Beleg für den wahren Verlauf.

## Tatsächlich ausgeführte technische Prüfung

- `scripts/uv.cmd sync --offline --locked`: 117 Pakete aufgelöst, 113 installierte geprüft.
- `scripts/uv.cmd run --offline --locked python -m unittest discover -s tests -v`:
  37 Tests, 1,331 s, OK. Vier neue Tests: bekannte Saison/analytisch linearer Trend,
  Masken/Nichtmutation, Ausrichtung/Randlücken/zu kurze Reihe, synthetische
  additive Rekonstruktion sowie reale Eingabe-/Stufeninvarianten.
- `scripts/uv.cmd run --offline --locked python scripts/build_exercise_11_3.py`:
  sieben Codezellen frisch sequenziell 1–7, vier echte eingebettete PNGs dekodiert.
  Gespeicherte CSV, Rohdaten-/Eingabehash, Maskengleichheit, bekannte Werte,
  additive Identität und Rückaddition an Fehlstellen erfolgreich geprüft.
  Nach Präzisierung des Beobachtungstextes erneut vollständig gerendert.
- `scripts/uv.cmd run --offline --locked python scripts/check_exercise_11_3_html.py`:
  Offline-Chromium bei 900/1400 px: vier Bilder geladen, keine Seitenfehler und
  kein horizontaler Überlauf. Alle vier PNGs visuell kontrolliert; Datum,
  Stück-pro-Woche-Einheiten, Legenden und unterschiedliche Komponentenskalen geprüft.
- Abschlussaudit vor Veröffentlichung: freigegebene Dateien/Originalreviews,
  Kapitel-10-ZIPs, Manifesthashes und unveränderte alte Paketversionen kontrolliert.

Bekannter lokaler Jupyter-TCP-Hinweis beim Kernelstart. Kein Test-, Notebook-
oder Exportfehler. GitHub-CI wird am tatsächlichen neuen PR-Head geprüft und
erst nach tatsächlichem Abschluss im PR als erfolgreich verlinkt.

## Artefakte

- sessions/ch11/production_stl_imputation.ipynb; neue Module stl_imputation.py / stl_plots.py.
- outputs/ch11/exercise_11_3/: production_stl_imputation.html,
  01_stl_components.png, 02_deseasonalized_gaps.png, 03_final_imputation.png,
  04_long_gap_comparison.png, components.csv, stage_missing_counts.csv,
  summary.json, validation_manifest.json.
- data/processed/exercise_11_3_stages.csv: lokale vollständige Stufenableitung,
  Git-ignoriert, mit dem Builder reproduzierbar.
- Bestehende Rohdatenquelle/Lizenzgrenze, aktualisierte Abhängigkeitsspezifikation;
  kein PDF gefordert. Kein Abgabepaket oder Upload erstellt.

## Grenzen und konkrete wissenschaftliche Reviewfragen

STL schätzt die Saison aus teilweise vorläufig imputierten Werten. Das Ergebnis
hängt von diesen Annahmen, langen Lücken, Rändern und LOESS-Fenstern ab.
52 Wochen approximieren ein Kalenderjahr; seasonal=13 ist ein LOESS-Fenster
auf saisonalen Teilreihen, kein 13-Wochen-Zyklus. Additivität und Fenster sind
nicht statistisch optimiert. Robuste Gewichtung und Rekonstruktionsidentität
beweisen keine inhaltlich richtige Zerlegung. Keine fehlerfreie Ground Truth,
Genauigkeitsverbesserung oder Unsicherheitsintervalle behauptet. Rückblickende
Analyse, keine unverändert zulässige Echtzeitprognose.

1. Ist die Trennung von vorläufiger Imputation und erneutem Arbeiten auf den
   ursprünglichen 367 Fehlstellen nachvollziehbar?
2. Sind additive Saison, 52-Wochen-Näherung und explizite LOESS-Fenster für den
   Bericht fachlich angemessen und verständlich begründet?
3. Wird klar zwischen Rekonstruktionsidentität, Methodenunterschied und
   unbekannter Genauigkeit unterschieden?
4. Welche Aussagen über die 23-Wochen-Lücke wären im Managementbericht vertretbar?

Keine Arbeit an 11.4, keine Freigabe für 11.3, kein Merge und keine Universitätseinreichung.


# Human Review – Aufgabe 11.3

**Datum:** 26.10.2026  
**Aufgabe:** Saisonbereinigte Imputation einer Produktionszeitreihe mit STL  
**KI-Unterstützung:** Codex  
**Review-Status:** APPROVED – Fachliche Prüfung positiv

## 1. Ziel und Umfang der Prüfung

Ziel der Aufgabe ist es, fehlende Beobachtungen einer wöchentlichen Produktionszeitreihe unter Berücksichtigung saisonaler Schwankungen zu ergänzen.

Dazu wird die STL-Zerlegung (*Seasonal and Trend decomposition using LOESS*) verwendet.

Die fachliche Prüfung umfasst die methodische Umsetzung, die Wahl der STL-Parameter, die Datenintegrität, die vier bereitgestellten Visualisierungen und die Interpretation der Ergebnisse.

Besonders wichtig ist die Unterscheidung zwischen einer plausiblen Rekonstruktion und einer tatsächlich nachgewiesenen Imputationsgenauigkeit.

## 2. Datenbasis und Datenintegrität

Die verwendete Produktionszeitreihe umfasst insgesamt 1.044 Wochen.

Davon enthalten 677 Wochen ursprünglich bekannte Werte, während 367 Wochen fehlen.

Die Analyse verwendet die aus Aufgabe 11.1 freigegebene geglättete Produktionsreihe mit ihrer ursprünglichen Lückenstruktur.

Die mitgelieferte Ergebnisübersicht bestätigt:

- 1.044 Zeitpunkte insgesamt.
- 677 ursprünglich beobachtete Werte.
- 367 ursprünglich fehlende Wochen.
- Keine fehlenden Werte nach der vorläufigen linearen Interpolation.
- 367 fehlende Werte nach Wiederherstellung der ursprünglichen Lücken in der saisonbereinigten Reihe.
- Keine fehlenden Werte im Endergebnis.
- Sämtliche 677 bekannten Werte bleiben exakt erhalten.
- Keine negativen imputierten Produktionswerte.

Diese Ergebnisse sind für die Datenintegrität wesentlich. Die Imputation verändert ausschließlich ursprünglich fehlende Beobachtungen.

**Prüfergebnis:** Die dokumentierten Datenintegritätsbedingungen sind erfüllt.

## 3. Prüfung des zweistufigen STL-Verfahrens

Die Implementierung folgt einer nachvollziehbaren zweistufigen Vorgehensweise.

### Stufe 1 – Vorläufige Ergänzung und STL-Zerlegung

Zunächst werden die fehlenden Wochen durch lineare Interpolation vorläufig ergänzt.

Dieser Schritt ist notwendig, weil das verwendete STL-Verfahren eine vollständige Zeitreihe benötigt.

Anschließend wird die vorläufig vervollständigte Reihe additiv in Trend, Saisonkomponente und Residuum zerlegt.

Mathematisch wird angenommen:

Y(t) = T(t) + S(t) + R(t)

Dabei bezeichnet T(t) den langfristigen Trend, S(t) die saisonale Komponente und R(t) den verbleibenden Rest.

Die vorläufig interpolierten Werte dienen nur der Schätzung dieser Komponenten. Sie werden nicht ungeprüft als endgültige Ergänzung übernommen.

### Stufe 2 – Saisonbereinigung und finale Imputation

Von der ursprünglich lückenhaften geglätteten Produktionsreihe wird die geschätzte Saisonkomponente subtrahiert.

Dadurch entsteht eine saisonbereinigte Zeitreihe, in der die ursprünglichen 367 Lücken weiterhin vorhanden sind.

Diese Lücken werden anschließend linear interpoliert.

Im letzten Schritt wird die saisonale Komponente wieder addiert.

Die ursprünglichen 677 bekannten Werte werden für die endgültige Ausgabe beibehalten.

**Prüfergebnis:** Die Trennung der beiden Verfahrensstufen ist methodisch nachvollziehbar und fachlich sinnvoll umgesetzt.

## 4. STL-Parametrisierung

Die verwendete Konfiguration lautet:

| Parameter | Wert |
|---|---:|
| Periodenlänge | 52 Wochen |
| Seasonal LOESS | 13 |
| Trend LOESS | 101 |
| Low-pass LOESS | 53 |
| Robust STL | Aktiviert |

Die Periodenlänge von 52 Wochen ist eine sinnvolle Näherung für eine jährlich wiederkehrende saisonale Struktur in wöchentlichen Produktionsdaten.

Sie entspricht allerdings nicht exakt jedem Kalenderjahr. Diese Vereinfachung muss bei der Interpretation berücksichtigt werden.

Die saisonale Glättung mit einem Fenster von 13 ermöglicht die Schätzung wiederkehrender saisonaler Muster.

Das Trendfenster von 101 unterstützt die Trennung des langfristigen Produktionsanstiegs von kurzfristigen Schwankungen.

Die robuste STL-Variante reduziert den Einfluss einzelner auffälliger Beobachtungen auf die Zerlegung.

Die Parameterwahl ist für eine explorative Untersuchung vertretbar. Eine optimale Wahl wurde jedoch nicht durch eine systematische Parametersuche nachgewiesen.

**Prüfergebnis:** Die Konfiguration ist nachvollziehbar begründet. Die Ergebnisse bleiben von den gewählten Parametern abhängig.

## 5. Visuelle Prüfung

### 5.1 STL-Komponenten

Die erste Grafik zeigt die vorläufig ergänzte Produktionsreihe und die drei geschätzten STL-Komponenten.

Der Trend steigt über den betrachteten Zeitraum deutlich an.

Die Saisonkomponente zeigt eine regelmäßig wiederkehrende jährliche Struktur. Ihre absolute Größenordnung verändert sich im Verhältnis zum Gesamtanstieg nur begrenzt.

Dies spricht für die Vertretbarkeit einer additiven Modellierung.

Im Residuum bleiben kurzfristige Schwankungen und einzelne deutliche Ausschläge erkennbar.

Die Teilgrafiken verwenden unterschiedliche y-Achsenskalen. Dies ist sinnvoll, weil Trend, Saison und Residuum unterschiedliche Größenordnungen besitzen.

Die Achsen und Einheiten sind korrekt beschriftet.

### 5.2 Saisonbereinigte Reihe mit ursprünglichen Lücken

Die zweite Grafik stellt die ursprünglich lückenhafte geglättete Zeitreihe der saisonbereinigten Zeitreihe gegenüber.

Nach der Saisonbereinigung sind die wiederkehrenden Schwankungen deutlich reduziert.

Der langfristige Produktionsanstieg bleibt weiterhin sichtbar.

Besonders wichtig ist, dass die ursprünglichen Datenlücken in beiden Darstellungen erhalten bleiben.

Die Saisonbereinigung wird somit nicht mit einer bereits abgeschlossenen Imputation verwechselt.

### 5.3 Finale STL-gestützte Imputation

Die dritte Grafik zeigt die vollständige Ausgangsreihe, die freigegebene Medianreihe mit Lücken und ausschließlich die durch das STL-gestützte Verfahren ergänzten Wochen.

Die drei Datenzustände sind klar voneinander getrennt.

Die imputierten Werte zeigen sowohl den langfristigen Anstieg als auch eine wiederkehrende saisonale Struktur.

Im Vergleich zu einer einfachen linearen Interpolation können dadurch innerhalb längerer Lücken zusätzliche Schwankungen entstehen.

Diese Schwankungen sind geschätzte Modellbestandteile und keine tatsächlich beobachteten Produktionswerte.

### 5.4 Vergleich der längsten Datenlücke

Die vierte Grafik zeigt die erste längste Datenlücke mit 23 Wochen.

Dargestellt werden:

- Einfache lineare Interpolation.
- STL-gestützte Imputation.
- Bekannte Randbeobachtungen.
- Die Differenz der beiden Methoden an den ursprünglich fehlenden Wochen.

Die lineare Interpolation verbindet die bekannten Randwerte geradlinig.

Die STL-gestützte Methode zeigt dagegen eine zusätzliche saisonale Variation.

Zu Beginn der Lücke liegt die STL-Schätzung unter der linearen Verbindung, später überwiegend darüber.

Die Gegenüberstellung macht die methodischen Unterschiede deutlich und eignet sich besonders gut zur fachlichen Erklärung.

**Prüfergebnis:** Alle vier Visualisierungen sind verständlich, gut lesbar und unterstützen die methodische Interpretation.

## 6. Prüfung der numerischen Ergebnisse

Die Ergebnisdatei `summary.json` enthält folgende Kennzahlen:

| Kennzahl | Ergebnis |
|---|---:|
| Fehlende Werte vor Imputation | 367 |
| Fehlende Werte nach Imputation | 0 |
| Erhaltene Originalwerte | 677 |
| Mittlere absolute Methodendifferenz an Lücken | 9,7462 Stück/Woche |
| Maximale absolute Methodendifferenz an Lücken | 75,2469 Stück/Woche |
| Negative imputierte Werte | 0 |

Die additive Rekonstruktion der STL-Komponenten weist eine maximale numerische Abweichung von ungefähr 1,14 × 10⁻¹³ auf.

Diese sehr geringe Abweichung liegt im Bereich der numerischen Gleitkommapräzision.

Die Rekonstruktion ist damit rechnerisch konsistent.

Die Differenzen zur einfachen linearen Interpolation sind ebenfalls nachvollziehbar. Sie zeigen, dass die saisonale Modellierung die geschätzten Werte beeinflusst.

Allerdings stellen diese Differenzen keine Fehlermaße gegenüber tatsächlichen Referenzwerten dar.

**Prüfergebnis:** Die numerischen Ergebnisse sind konsistent und werden wissenschaftlich angemessen interpretiert.

## 7. Fachliche Interpretation der 23-Wochen-Lücke

Die längste Lücke ist der wichtigste Vergleichsfall der Aufgabe.

Bei der einfachen linearen Interpolation wird eine gleichmäßige Veränderung zwischen den bekannten Randwerten angenommen.

Die STL-gestützte Methode ergänzt dagegen ein zuvor geschätztes saisonales Muster.

Dadurch entsteht ein differenzierterer Verlauf.

Der zusätzliche Verlauf ist jedoch nicht automatisch genauer. Während der 23 fehlenden Wochen sind die tatsächlichen Produktionswerte unbekannt.

Es lässt sich deshalb nicht nachweisen, ob die saisonalen Schwankungen in diesem Zeitraum tatsächlich so aufgetreten sind.

Die Aussage, dass die STL-Methode saisonale Struktur berücksichtigt, ist fachlich gerechtfertigt.

Eine Aussage, dass sie die tatsächliche Produktion besser rekonstruiert, wäre ohne zusätzliche Validierung nicht gerechtfertigt.

**Prüfergebnis:** Die Darstellung der langen Lücke ist methodisch aussagekräftig, sofern keine unbegründete Genauigkeitsbehauptung erfolgt.

## 8. Wissenschaftliche Einschränkungen

### Abhängigkeit von der vorläufigen Imputation

Die STL-Zerlegung basiert auf der zunächst linear vervollständigten Zeitreihe.

Daher können die anfänglichen interpolierten Werte die geschätzten Trend- und Saisonkomponenten beeinflussen.

Das Verfahren ist keine unabhängige Rekonstruktion der fehlenden Werte.

### Annahme einer additiven Saison

Die additive Modellierung unterstellt, dass saisonale Effekte näherungsweise als absolute Zu- oder Abschläge beschrieben werden können.

Falls die saisonale Schwankungsbreite tatsächlich proportional zum Produktionsniveau wächst, könnte eine andere Modellierung besser geeignet sein.

### Periodenlänge

Die Annahme einer festen 52-Wochen-Periode ist eine praktische Näherung.

Kalenderabweichungen und mögliche zeitliche Veränderungen der saisonalen Struktur werden dadurch nur eingeschränkt berücksichtigt.

### Lange Lücken

Eine Lücke von 23 Wochen umfasst einen erheblichen Teil eines Jahres.

Ihre Ergänzung ist stark von den geschätzten Komponenten und den bekannten Randwerten abhängig.

### Fehlende Genauigkeitsreferenz

Für ursprünglich fehlende Wochen liegen keine bekannten tatsächlichen Werte vor.

Deshalb kann kein belastbarer Nachweis geführt werden, dass die STL-gestützte Methode genauer als die einfache lineare Interpolation ist.

Diese Einschränkung ist für die wissenschaftliche Bewertung zentral.

## 9. Technische Validierung

Laut Codex wurden folgende Prüfungen durchgeführt:

| Prüfung | Gemeldetes Ergebnis |
|---|---|
| Automatisierte Tests | 37 bestanden |
| Notebook-Codezellen | 7 sequenziell ausgeführt |
| Visualisierungen | 4 geprüft |
| HTML-Export | Offline bei 900 und 1400 px geprüft |
| GitHub Push-CI | Erfolgreich |
| GitHub PR-CI | Erfolgreich |
| Pull Request #7 | Konfliktfrei, ungemergt |

Das bereitgestellte Validierungsmanifest dokumentiert außerdem die verwendeten STL-Parameter, die exportierten Dateien und deren Prüfsummen.

Die technischen Prüfungen werden als von Codex beziehungsweise automatisierten Werkzeugen durchgeführte Validierung ausgewiesen.

Eine unabhängige lokale Testausführung durch den Studierenden wird nicht behauptet.

## 10. Gesamtbewertung

Die zweistufige STL-Imputation ist nachvollziehbar implementiert und wissenschaftlich sinnvoll erläutert.

Die ursprünglichen Beobachtungen bleiben erhalten und alle fehlenden Wochen werden ergänzt.

Die vier Visualisierungen zeigen die STL-Komponenten, die Saisonbereinigung, die finale Imputation und den Methodenvergleich bei der längsten Lücke.

Besonders positiv ist die klare Trennung zwischen methodischen Unterschieden und tatsächlicher Imputationsgenauigkeit.

Die wichtigsten Grenzen des Verfahrens werden berücksichtigt. Die Parameterwahl und die Abhängigkeit von der vorläufigen Interpolation sind ausreichend nachvollziehbar.

Bei der Prüfung der bereitgestellten Ergebnisse wurden keine wesentlichen fachlichen Fehler festgestellt.

**Human Review: APPROVED – Fachlich positiv**

Keine grundlegenden methodischen Korrekturen erforderlich.

Die abschließende technische Nachprüfung und die GitHub-Freigabe bleiben Teil des dokumentierten Human-AI-Workflows.

Pull Request #7 darf erst nach ausdrücklicher Merge-Autorisierung in `main` integriert werden.
