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
