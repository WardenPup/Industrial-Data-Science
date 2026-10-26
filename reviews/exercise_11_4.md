# Exercise 11.4 – Human-AI Review

Status: APPROVED – AWAITING FINAL MERGE AUTHORIZATION

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
Fachliche Freigabe vom 26.10.2026 im unveränderten studentischen Review unten.
Keine finale Merge-Autorisierung erteilt.

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


## KI-gestützte Abschlussprüfung nach studentischem Review – 26.10.2026

40 Tests erfolgreich (2,248 s): `scripts/uv.cmd run --offline --locked python -m unittest discover -s tests -v`.
Weitere tatsächlich ausgeführte Befehle mit gleichem uv-Präfix:
- `python scripts/build_exercise_11_4.py`: frischer Kernel, drei sequenzielle Codezellen,
  zwei eingebettete PNGs, keine Notebookfehler.
- `python scripts/check_exercise_11_4_html.py`: offline 900/1400 px, beide Bilder geladen,
  keine Seitenfehler oder horizontalen Überläufe.
- `python scripts/check_exercise_11_4_review.py`: tatsächliche STL-Argumente kontrolliert,
  direkte STL-Referenz mit derselben Bibliothek; Schwellenarithmetik separat mit
  math.fsum und ddof=1 nachgerechnet. Beide CSVs und je 26 Plot-Marker zugeordnet.

Ergebnisse: 1.044 Originalwerte, keine Lücken, exakt unveränderte Eingabe; 26 negative
und null positive Kandidaten (2,4904214559 %). Residuenmittel −4,540957783,
Stichprobenstandardabweichung 26,820479374; Grenzen −85,002395904/75,920480338
Stück/Woche. Maximale additive Rekonstruktionsabweichung 9,9475983006e-14.
Alle numerischen und methodischen Reviewaussagen bestätigt; keine Diskrepanz.
Beide Grafiken erneut visuell geprüft, Beschriftungen und Markierungen korrekt.
Rohdaten und sieben Manifest-Artefakte checksumgeprüft; Prüfdetails zusätzlich in
human_review_verification.json. Keine Änderung der Berechnung oder STL-Parameter.
Notebook um die ausdrücklich angefragte Einordnung von Asymmetrie und möglichen
realen Ereignissen präzisiert, ohne konkrete Ursachen zu behaupten.

Transparente Werkzeugkorrekturen: Ein erster Builder-Aufruf scheiterte nach der
Statusänderung an einer Windows-Dateikodierung; UTF-8 wiederhergestellt und erneut
gebaut. Der neue Markercheck griff zunächst auf die Seaborn-Liniencollection zu;
er wählt jetzt die beschriftete Kandidatencollection. Wiederholte Prüfung erfolgreich.
Bekannte lokale Jupyter-Warnung: TCP-Kernelkommunikation unverschlüsselt.
STL- und Schwellenwahl bleiben Annahmen; Kandidaten sind keine bewiesenen Messfehler.
Die wissenschaftliche Freigabe ist dokumentiert, Merge-Autorisierung bleibt ausstehend.

### Plattformübergreifende CI-Korrektur
Die ersten Head-Läufe 40366278175/40366285690 scheiterten ausschließlich an einer
zu engen Prüfung des Rekonstruktionsrundungsfehlers (Abstand zum lokalen Wert
kleiner 1e-16). Notebook, 26 Kandidaten und Offline-HTML waren erfolgreich.
Der Reviewcheck verwendet nun 16 × float64-Maschinengenauigkeit × maximale
Datengröße als absolute Schranke. Das prüft numerische Rekonstruktionskonsistenz,
ohne identische Rundungsreste verschiedener Plattformen zu verlangen. Die lokale
Angabe 9,9475983006e-14 bleibt korrekt. Keine Änderung der Berechnung oder Daten.
CI meldete außerdem IPython-Temporärverzeichnis-Fallback, Jupyter-TCP-Warnung,
setup-python@v5/Node-20-Deprecation und Ubuntu-Runner-Migrationshinweis.

# Human Review – Exercise 11.4

**Datum:** 26.10.2026  
**Aufgabe:** Ausreißererkennung in einer wöchentlichen Produktionszeitreihe  
**Methode:** Robuste STL-Zerlegung und Drei-Sigma-Regel  
**KI-Unterstützung:** Codex  
**Review-Status:** APPROVED – vorbehaltlich abschließender technischer Prüfung

## 1. Ziel der Prüfung

In dieser Aufgabe wird die ursprüngliche Produktionsreihe `pieces` auf auffällige Beobachtungen untersucht.

Dabei soll zwischen normalen saisonalen Schwankungen und ungewöhnlich starken Abweichungen unterschieden werden.

Ich habe die bereitgestellten Ergebnisse und beide Grafiken auf Plausibilität, Nachvollziehbarkeit und wissenschaftliche Interpretation beurteilt.

## 2. Methodische Bewertung

Die Verwendung einer robusten STL-Zerlegung ist für diese Zeitreihe sinnvoll.

Die Produktionszahlen zeigen einen deutlichen langfristigen Anstieg und regelmäßig wiederkehrende saisonale Schwankungen. Eine direkte Ausreißererkennung auf den ursprünglichen Produktionswerten wäre deshalb problematisch.

Durch die STL-Zerlegung werden Trend und Saisonkomponente berücksichtigt. Die verbleibenden Residuen beschreiben die Abweichungen vom modellierten Verlauf.

Die Drei-Sigma-Regel verwendet den Mittelwert und die Standardabweichung der Residuen:

\[
r_i < \bar r - 3s
\quad \text{oder} \quad
r_i > \bar r + 3s
\]

Die Methode ist einfach, reproduzierbar und für eine explorative Ausreißeranalyse geeignet.

Die gewählte STL-Konfiguration mit einer Periodenlänge von 52 Wochen sowie den LOESS-Fenstern 13, 101 und 53 ist nachvollziehbar. Diese Parameter sind allerdings Modellannahmen und nicht nachweislich optimal.

## 3. Numerische Ergebnisse

Die bereitgestellte Auswertung liefert folgende Ergebnisse:

| Kennzahl | Ergebnis |
|---|---:|
| Beobachtungen insgesamt | 1.044 |
| Fehlende Beobachtungen | 0 |
| Ausreißerkandidaten | 26 |
| Anteil der Kandidaten | 2,49 % |
| Negative Kandidaten | 26 |
| Positive Kandidaten | 0 |
| Mittelwert der Residuen | −4,541 Stück/Woche |
| Standardabweichung | 26,820 Stück/Woche |
| Untere Grenze | −85,002 Stück/Woche |
| Obere Grenze | +75,920 Stück/Woche |

Die Grenzen sind rechnerisch mit der verwendeten Drei-Sigma-Regel konsistent.

Die Rekonstruktionsabweichung der additiven STL-Zerlegung liegt mit ungefähr \(9,95 \times 10^{-14}\) im Bereich numerischer Gleitkommapräzision.

Bemerkenswert ist, dass sämtliche erkannten Kandidaten negative Abweichungen aufweisen. Die auffälligen Ereignisse betreffen somit ausschließlich Produktionswerte, die deutlich unter dem modellierten Verlauf liegen.

Diese Asymmetrie sollte bei der Interpretation berücksichtigt werden.

## 4. Visuelle Prüfung

### Abbildung 1 – Originalproduktion und Ausreißerkandidaten

Die erste Grafik zeigt die ursprüngliche Produktionsreihe mit den 26 markierten Kandidaten.

Der langfristige Produktionsanstieg ist deutlich erkennbar. Ebenso zeigt die Zeitreihe regelmäßig wiederkehrende saisonale Schwankungen.

Die roten Markierungen liegen an ungewöhnlich starken lokalen Produktionsrückgängen.

Besonders auffällig ist der starke Einbruch um das Jahr 2008. Auch in späteren Jahren treten einzelne deutliche Produktionsabfälle auf.

Die Darstellung ist verständlich. Achsen, Einheiten und Legende sind korrekt bezeichnet.

Die Markierungen zeigen auffällige Beobachtungen und nicht automatisch fehlerhafte Messwerte.

### Abbildung 2 – Residuen mit Drei-Sigma-Grenzen

Die zweite Grafik stellt die STL-Residuen und die beiden berechneten Schwellenwerte dar.

Die meisten Residuen liegen nahe null. Daneben sind vereinzelte starke negative Ausschläge erkennbar.

Die 26 rot markierten Kandidaten unterschreiten die untere Drei-Sigma-Grenze.

Positive Überschreitungen sind nicht vorhanden.

Die Darstellung erklärt damit nachvollziehbar, warum die Ausreißererkennung ausschließlich negative Kandidaten identifiziert.

Die beiden Diagramme ergänzen sich sinnvoll: Die erste Grafik zeigt die betroffenen Produktionswerte, während die zweite Grafik das statistische Erkennungskriterium sichtbar macht.

## 5. Fachliche Interpretation

Aus meiner Sicht sind die markierten Beobachtungen plausible Ausreißerkandidaten.

Sie unterscheiden sich deutlich vom langfristigen Trend und von den gewöhnlichen saisonalen Schwankungen.

Ein kurzfristiger Produktionsrückgang kann beispielsweise durch einen Maschinenstillstand, Wartungsarbeiten, Materialmangel oder andere betriebliche Ereignisse verursacht werden.

Diese möglichen Ursachen lassen sich aus der vorhandenen Zeitreihe allein jedoch nicht bestätigen.

Die 26 auffälligen Wochen dürfen deshalb nicht als nachgewiesene Messfehler bezeichnet werden.

Insbesondere bei industriellen Produktionsdaten können ungewöhnliche Werte reale Ereignisse darstellen, die für eine spätere Analyse relevant sind.

Daher halte ich es für richtig, die Originaldaten unverändert zu lassen und die Kandidaten zunächst nur zu kennzeichnen.

## 6. Grenzen der Methode

Die Drei-Sigma-Regel hat mehrere Einschränkungen.

Erstens setzt die einfache statistische Interpretation eine geeignete Residualverteilung voraus. Die dargestellten Residuen zeigen jedoch starke negative Ausschläge und damit eine deutliche Asymmetrie.

Zweitens können extreme Residuen selbst den Mittelwert und die Standardabweichung beeinflussen. Dadurch kann sich die Erkennungsschwelle verändern.

Drittens hängen die Ergebnisse von der STL-Parametrisierung ab. Andere Glättungsfenster oder eine andere Periodenlänge könnten zu einer veränderten Kandidatenmenge führen.

Viertens ist eine statistisch auffällige Beobachtung nicht automatisch ein fehlerhafter Datenpunkt.

Auch die robuste STL-Zerlegung beseitigt diese Einschränkungen nicht vollständig.

Eine weiterführende Untersuchung könnte alternative robuste Schwellenwerte oder zusätzliche Betriebsinformationen berücksichtigen. Für die vorliegende explorative Aufgabe ist das jedoch nicht zwingend erforderlich.

## 7. Technische Validierung und KI-Unterstützung

Die technische Umsetzung wurde mit Codex erstellt und automatisiert geprüft.

Laut technischem Prüfbericht wurden 40 Tests erfolgreich ausgeführt. Die Notebook-Ausführung, beide Diagramme, der HTML-Export sowie die Daten- und Exportprüfsummen wurden überprüft.

Diese Angaben beziehen sich auf die dokumentierte technische Validierung. Sie sind nicht als eigenständig vom Studierenden ausgeführte Tests zu verstehen.

Mein fachlicher Review bezieht sich auf die nachvollziehbare Methode, die dargestellten Ergebnisse und deren Interpretation.

Die KI-Unterstützung bei Implementierung und Verifikation bleibt transparent dokumentiert.

## 8. Gesamtbewertung

Die Aufgabe ist inhaltlich nachvollziehbar umgesetzt.

Die robuste STL-Zerlegung berücksichtigt den langfristigen Trend und die saisonalen Schwankungen. Die anschließende Drei-Sigma-Regel identifiziert 26 auffällige Wochen.

Beide Grafiken sind klar beschriftet und zeigen die Ergebnisse verständlich.

Die auffälligen Produktionsrückgänge sind plausibel als Ausreißerkandidaten eingeordnet. Ihre tatsächlichen Ursachen bleiben unbekannt.

Besonders wichtig finde ich, dass die Analyse keine automatische Korrektur oder Löschung dieser Beobachtungen vornimmt.

Die Grenzen der Methode sind ausreichend erkennbar und wissenschaftlich erklärbar.

**Gesamturteil: APPROVED**

Aus fachlicher Sicht sind keine grundlegenden Änderungen erforderlich.

Die technische Abschlussprüfung und die finale Merge-Freigabe erfolgen anschließend getrennt. PR #8 bleibt bis zur ausdrücklichen Autorisierung ungemergt.
