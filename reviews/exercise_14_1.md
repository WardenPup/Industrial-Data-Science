> Aktueller Stand 19.11.2026: **SCIENTIFICALLY APPROVED – TECHNICALLY VALIDATED – AWAITING FINAL MERGE AUTHORIZATION**.
> Der folgende Erstbericht bleibt als historische Dokumentation erhalten.
> Studentischer Originalreview und nachfolgende Codex-Verifikation sind getrennt.

# Exercise 14.1 – Technischer Bericht für den Human Review

**Status: AWAITING HUMAN REVIEW.** 19.11.2026. Studentische Bewertung/Freigabe
steht aus. Codex erstellte Notebook, deskriptive Hilfsfunktionen, Tests und Export.
Anforderungen stehen direkt im Notebook; kein zusätzlicher Anforderungsbericht.

## Umsetzung und Ergebnisse

Die offizielle Aufgabe verlangt den Abgleich der TWF-Beschreibung aus 13.1.7
mit 13.1.6.1/13.1.6.2. Aufgabe und Kontext wurden frisch per HTTPS gelesen;
das Webwerkzeug selbst war nicht erreichbar. UCI-Herkunft/CC BY 4.0 dokumentiert.
Keine Modelle trainiert, keine Methoden aus 14.2–14.4 vorweggenommen.

- Unveränderte AI4I-CSV: 10.000 × 14, keine fehlenden Werte/Duplikate,
  zwölf numerische Spalten und zwei als object geladene Kategorien/IDs.
- **46 TWF-Markierungen statt der beschriebenen 51**; Verschleiß 198–253 min.
- 43 TWF-Fälle innerhalb von 200–240 min; außerhalb UDI 1997/2865/5402
  bei 198/246/253 min. Ein weiterer TWF-Fall liegt genau bei 200 min.
- Kursgrenze bestätigt: 2 TWF unter 9.328 Fällen bei ≤202,5 min,
  44 unter 672 darüber. Hoher Verschleiß ist kein deterministischer TWF-Nachweis.
- Alle 46 TWF-Fälle haben Machine failure=1; weitere 293 allgemeine Fehler
  haben TWF=0. Fehlendes TWF-Flag bedeutet nicht allgemeine Fehlerfreiheit.
- Drei kleine Ergebnistabellen, Datentyp-/Fehlwerttabelle und ein Histogramm
  ausschließlich der TWF-Markierungen. Histogramm ist keine Ausfallwahrscheinlichkeit.

## Tatsächlich ausgeführte Prüfungen

Im bestehenden uv-Lockfile/Environment, Python 3.12.15, keine neuen Pakete:

| Befehl (nach `scripts/uv.cmd run --offline --locked`) | Ergebnis |
|---|---|
| `python -m unittest discover -s tests -p test_tool_wear.py -v` | **3 Tests bestanden**, 0,149 s: Intervallgrenzen/Nichtmutation, ungültige Eingaben, Originaldaten und unabhängig festgelegte Zahlen |
| `python scripts/build_exercise_14_1.py --check-html` | **3 Codezellen im frischen Kernel sequenziell**, keine Fehler; unabhängige Zählungen, Tabellenkonsistenz und eingebettetes PNG geprüft |
| Derselbe Build, Offline-Chromium | **900/1400 px bestanden**: Bild geladen, keine Seitenfehler, fehlgeschlagenen Anfragen oder horizontalen Seitenüberläufe |

Codex sichtete das PNG und die vollständige HTML-Fassung anhand der Browserbilder:
Titel, Minuten-Einheit, Häufigkeiten, Bereichsschattierung, Tabellen und Schlussfolgerung
lesbar. Rohdaten-SHA256 und acht erzeugte Quellen-/Artefakthashes im Manifest geprüft.
Frühere wissenschaftliche Dateien/Originalreviews/Abgabearchive bleiben unverändert.
Keine gesamte alte Testsuite oder wiederholte frühere Modelltrainings ausgeführt.

Beobachtete Warnung: lokaler Jupyter-TCP-Transport unverschlüsselt; keine dadurch
fehlgeschlagene Ausführung. Git interpretiert unverändert erhaltene CRLF-Bytes
zunächst als Leerzeichen; Whitespace-Prüfung mit `cr-at-eol` berücksichtigt dies.
GitHub-Checks werden am gepushten Head separat im Draft-PR nachgewiesen;
vor ihrem tatsächlichen Abschluss wird hier kein CI-Erfolg behauptet.

## Wissenschaftliche Grenzen

Die beschriebene Anzahl von 69 Austauschen und die zufällige Zuweisung sind ohne
eigene Austauschmarkierung nicht direkt verifizierbar. Die Ursache der Abweichungen
ist nicht nachgewiesen; Originalwerte/Labels werden nicht „korrigiert“.
Synthetische Daten, keine neue Kausalitäts-/Generalisierungsbehauptung. Kein TRAIN/TEST
nötig für diese reine Bestandszählung ohne Modell-/Parametersuche. 202,5 min stammt
aus dem Kurs und wird hier nicht gelernt. Keine unabhängige studentische Ausführung behauptet.

## Vier Fragen für deine fachliche Prüfung

1. Kannst du die Abweichungen bei Anzahl und Zeitbereich erklären und von der
   weiterhin zutreffenden Häufung bei hohem Verschleiß unterscheiden?
2. Ist verständlich, warum TWF=0 keine allgemeine Fehlerfreiheit bedeutet?
3. Erklären Tabelle und Grafik ausreichend, warum eine Verschleißgrenze allein
   kein sicherer Ausfallnachweis ist?
4. Ist klar, warum sich die 69 Austausche und die Ursache der Diskrepanz mit
   diesen Daten nicht belegen lassen?

Kein Merge, keine wissenschaftliche Freigabe, kein Beginn von 14.2, keine Einreichung.


---

## Studentischer Human Review – Originalwortlaut aus dem Nutzerauftrag

# Human Review – Exercise 14.1: Tool Wear Failure

**Bewertung: SCIENTIFICALLY APPROVED**

Ich habe die Ergebnisse, die Darstellung und die Interpretation von Exercise 14.1 fachlich geprüft.

## 1. Aufgabenverständnis und Vorgehensweise

Die Aufgabe wurde nachvollziehbar umgesetzt. Ziel war es, die Beschreibung des Werkzeugverschleißfehlers (TWF) mit den tatsächlich vorhandenen Daten zu vergleichen.

Die Entscheidung für eine deskriptive Analyse ohne zusätzliches Machine-Learning-Modell halte ich für richtig. Für diese Fragestellung reichen die Auswertung der vorhandenen Fehlermarkierungen, einfache Häufigkeitsvergleiche und eine passende Grafik aus.

## 2. Ergebnisse

Die wichtigsten Ergebnisse sind nachvollziehbar:

- Der Datensatz enthält 10.000 Beobachtungen mit insgesamt 46 TWF-Markierungen. Das weicht von den 51 Fällen in der Beschreibung ab.
- Von den 46 markierten Fällen liegen 43 im beschriebenen Bereich zwischen 200 und 240 Minuten.
- Drei Fälle liegen außerhalb dieses Bereichs, und zwar bei 198, 246 und 253 Minuten.
- Bei einem Werkzeugverschleiß bis einschließlich 202,5 Minuten sind 2 von 9.328 Fällen als TWF markiert. Oberhalb dieser Grenze sind es 44 von 672.

Damit wird deutlich, dass TWF-Markierungen vor allem bei höheren Verschleißwerten auftreten. Gleichzeitig zeigen die Ergebnisse, dass der beschriebene Bereich keine ausnahmslos gültige Grenze darstellt.

Wichtig finde ich außerdem die Unterscheidung zwischen TWF und dem allgemeinen Maschinenfehler. Ein fehlendes TWF-Flag bedeutet nicht automatisch, dass die Maschine fehlerfrei war.

## 3. Bewertung der Grafik

Das Histogramm ist übersichtlich und für die Aufgabe passend.

Die grüne Markierung macht den beschriebenen Bereich von 200 bis 240 Minuten direkt erkennbar. Gleichzeitig fallen die drei außerhalb liegenden TWF-Werte auf.

Die Darstellung unterstützt damit die zentrale Aussage der Untersuchung.

Wichtig ist nur, dass die Balkenhöhen die Anzahl der TWF-Markierungen darstellen und keine Ausfallwahrscheinlichkeit. Diese Unterscheidung wurde in der Ausarbeitung berücksichtigt.

## 4. Wissenschaftliche Interpretation

Die Interpretation halte ich für angemessen und ausreichend vorsichtig.

Besonders wichtig ist, dass die Abweichung zwischen 46 und 51 Fällen nicht einfach als Datenfehler bezeichnet wird. Die tatsächliche Ursache lässt sich mit den vorhandenen Informationen nicht feststellen.

Auch die beschriebenen 69 Werkzeugwechsel können ohne eine entsprechende Markierung im Datensatz nicht unabhängig überprüft werden.

Der Zusammenhang zwischen höherem Verschleiß und häufiger auftretenden TWF-Markierungen wird nachvollziehbar beschrieben, ohne daraus einen sicheren oder kausalen Ausfallmechanismus abzuleiten.

## 5. Grenzen

Die wissenschaftlichen Grenzen sind ausreichend dokumentiert:

- Es handelt sich um einen synthetischen Datensatz.
- Die dokumentierte Fehlerbeschreibung stimmt nicht vollständig mit den vorhandenen Markierungen überein.
- Die tatsächlichen Werkzeugwechsel sind nicht separat beobachtbar.
- Aus dem Verschleißwert allein lässt sich kein sicherer Werkzeugausfall bestimmen.

Weitere Modelle oder statistische Untersuchungen halte ich für Exercise 14.1 nicht für notwendig.

## 6. Abschließende Bewertung

Die Aufgabenstellung wurde aus meiner Sicht vollständig und verständlich bearbeitet.

Die Auswertung ist kompakt, die Grafik sinnvoll und die Interpretation nachvollziehbar. Besonders positiv finde ich, dass Widersprüche zur Beschreibung offengelegt und nicht durch unbegründete Annahmen aufgelöst werden.

Ich sehe keinen fachlichen Korrekturbedarf.

**Finale wissenschaftliche Bewertung: APPROVED.**

Die technische Abschlussprüfung und die finale Merge-Freigabe bleiben separate Schritte.


---

## Codex-Verifikation nach studentischem Review – 19.11.2026

Der oben vollständig übernommene studentische Wortlaut wurde gegen den Nutzerauftrag
verglichen; der frühere Bericht ist erhalten. Keine zusätzliche studentische Prüfung
oder Merge-Autorisierung wird daraus abgeleitet. Originalreview separat: `086ba13`.

Erneut tatsächlich ausgeführt im bestehenden uv-Environment:
- `scripts/uv.cmd run --offline --locked python -m unittest discover -s tests -p test_tool_wear.py -v`: **3/3 bestanden**, 0,063 s (vorher 0,149 s; keine Zeitgarantie).
- `scripts/uv.cmd run --offline --locked python scripts/build_exercise_14_1.py --check-html`: **3 frische sequenzielle Codezellen**, keine Ausführungsfehler; HTML offline bei **900/1400 px** ohne Seitenfehler, fehlgeschlagene Anfragen oder Seitenüberlauf.
- PNG und beide vollständigen Browseransichten visuell geprüft: Titel, Minutenachse, Häufigkeitsachse, Bereich 200–240 min und Ausreißer lesbar. Histogramm zählt TWF-Markierungen, keine Ausfallwahrscheinlichkeiten.
- Unabhängige CSV-Selektoren bestätigen 10.000 Zeilen, 46 statt beschriebener 51 TWF, 43 innerhalb 200–240 min, genau drei außerhalb bei 198/246/253 min; bei ≤202,5 min 2/9.328, darüber 44/672. Alle 46 TWF sind allgemeine Fehler; weitere 293 allgemeine Fehler haben TWF=0.
- Rohdaten-SHA256 und alle **acht** Manifesthashes stimmen. Wissenschaftliche CSV/JSON/PNG sind bytegleich mit `2a20221`; wissenschaftliche Zellquellen unverändert. **21 Abgabearchive** stimmen mit dem bestehenden SHA256-Snapshot überein. Frühere Aufgaben/Originalreviews unverändert.

Keine fachlichen Korrekturen erforderlich. Nur Statusangaben und Prüfdokumentation
aktualisiert, Notebook/HTML frisch erzeugt. Die 69 Austausche bleiben ausdrücklich
als nicht unabhängig prüfbare Beschreibungsangabe gekennzeichnet. Ursache der
Diskrepanz unbekannt; synthetische Daten, keine Kausalitätsbehauptung.

Warnung erneut: lokaler Jupyter-TCP-Transport ohne Verschlüsselung; Ausführung
erfolgreich. Keine zusätzlichen Analysen, Modelle oder Tests eingeführt. Aktuelle
GitHub-Checks und Review-/Konfliktprüfung werden nach Push am tatsächlichen Head
im bestehenden PR #14 dokumentiert. **Kein Merge autorisiert oder durchgeführt.**
