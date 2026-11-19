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


---

## Studentischer Human Review – Originalwortlaut

# HUMAN REVIEW – Exercise 14.2: Overstrain Failure

**Status: SCIENTIFICALLY APPROVED – CI RESOLUTION REQUIRED**

Ich habe die bereitgestellten Grafiken, Ergebnistabellen und die wissenschaftliche Interpretation von Exercise 14.2 geprüft.

## 1. Wissenschaftliche Umsetzung

Die Aufgabenstellung wurde aus meiner Sicht verständlich und fachlich sinnvoll umgesetzt.

Die Untersuchung zeigt, wie Entscheidungsbäume eine bekannte Fehlerregel aus den AI4I-Daten nachbilden und welchen Einfluss die verwendeten Eingangsmerkmale darauf haben.

Besonders sinnvoll finde ich den schrittweisen Vergleich:

- Werkzeugverschleiß und Drehmoment als Ausgangsbasis.
- Zusätzlich das Produktmerkmal `wearadjTorque`.
- Zusätzlich die Maschinenvariante `Type`.

Damit wird anschaulich gezeigt, warum Feature Engineering bei Entscheidungsbäumen hilfreich sein kann.

## 2. Prüfung der Grafiken

**Grafik 1 – OSF-Regel nach Type**

Die Trennung nach L, M und H ist verständlich. Die eingezeichneten Hyperbeln machen sichtbar, dass für die drei Varianten unterschiedliche Grenzwerte gelten.

Die 98 OSF-Markierungen verteilen sich auf 87 L-, 9 M- und 2 H-Fälle.

Die Grafik unterstützt die Aussage, dass die dokumentierte Produktregel mit den Markierungen übereinstimmt.

**Grafik 2 – Entscheidungsgrenzen**

Die zunehmende Baumtiefe wird verständlich dargestellt.

Bei geringer Tiefe können die achsenparallelen Entscheidungsgrenzen die gekrümmte Produktregel nur grob annähern.

Mit zunehmender Tiefe entstehen feinere rechteckige Entscheidungsbereiche und die Anpassungsfehler sinken von 98 bei Tiefe 1 auf 21 bei Tiefe 8.

Die schwarze Hyperbel ist korrekt als Referenz für Type L beschriftet. Sie darf nicht als allgemeine Grenze für alle drei Varianten verstanden werden.

**Grafik 3 – Baumstrukturen**

Der Vergleich der drei Bäume ist besonders aussagekräftig.

Der Ausgangsbaum benötigt mehrere aufeinanderfolgende Entscheidungen über Verschleiß und Drehmoment.

Mit dem Produktmerkmal kann der Baum bereits früh eine passende Trennung vornehmen. Die zusätzliche Berücksichtigung von Type ermöglicht eine weitere Annäherung an die ursprüngliche Regel.

Die Baumstrukturen sind ausführlich, aber für diese Aufgabe fachlich sinnvoll.

## 3. Ergebnisse

Die bereitgestellten CSV-Dateien bestätigen für Tiefe 3 folgende Anpassungsfehler:

- Kursbasis: 43 Fehler.
- Mit Produktmerkmal: 22 Fehler.
- Mit Produktmerkmal und Type: 2 Fehler.

Für den getrennten TEST-Split ergeben sich:

- Kursbasis: 14 Fehler, F1 = 0,6111.
- Mit Produktmerkmal: 8 Fehler, F1 = 0,8000.
- Mit Produktmerkmal und Type: 1 Fehler, F1 = 0,9744.

Die Unterscheidung zwischen Anpassung auf allen Daten und dem getrennten TEST-Ergebnis ist wichtig und im Bericht nachvollziehbar dargestellt.

Der Testvergleich unterstützt die Aussage, dass die erweiterten Merkmale bei dieser konkreten Datenteilung bessere Klassifikationsergebnisse liefern.

Eine allgemeine Überlegenheit ist damit nicht bewiesen.

## 4. Verbleibende Fehler

Die zwei verbleibenden Anpassungsfehler sind nachvollziehbar eingeordnet.

Es handelt sich um die beiden positiven H-Fälle, die der verwendete Baum aufgrund seiner Struktur und der Mindestblattgröße nicht separat erkennt.

Dass zusätzliche Baumtiefe allein keine vollständig fehlerfreie Trennung garantiert, ist eine wichtige und korrekt dargestellte Einschränkung.

Die geringe Anzahl positiver Fälle sollte bei der Interpretation berücksichtigt werden.

## 5. Wissenschaftliche Grenzen

Die wesentlichen Einschränkungen wurden angemessen dokumentiert:

- Seltene OSF-Fälle und starke Klassenungleichheit.
- Nur eine feste TRAIN-/TEST-Aufteilung.
- Keine unabhängige Untersuchung weiterer Maschinen.
- Kein kausaler Nachweis eines realen Ausfallmechanismus.
- Synthetische und durch eine bekannte Regel definierte Zielvariable.
- Modellparameter beeinflussen die erlernten Entscheidungsgrenzen.

Ich halte keine zusätzliche Modellstudie für notwendig, sofern sie nicht ausdrücklich verlangt wird.

## 6. Technische Einschränkung

Die lokale Validierung wurde laut Prüfbericht erfolgreich durchgeführt.

Die GitHub-Actions-Läufe sind allerdings wegen eines HTTPS-Zertifikatsproblems beim UCI-Download fehlgeschlagen.

Daher kann ich noch keine vollständige technische Abschlussfreigabe erteilen.

Die SSL-Zertifikatsprüfung darf nicht deaktiviert oder umgangen werden.

Ich empfehle, den bestehenden geprüften Originaldatensatz über eine sichere, reproduzierbare Datenquelle beziehungsweise einen bereits vorhandenen checksumgeprüften Projektbestand für CI bereitzustellen.

Nach der Korrektur müssen die tatsächlichen CI-Prüfungen erneut erfolgreich durchlaufen.

## 7. Abschließende Bewertung

Die wissenschaftliche Umsetzung von Exercise 14.2 ist aus meiner Sicht gelungen.

Die Methode ist verständlich erklärt, die Grafiken zeigen den Nutzen des Feature Engineerings und die Ergebnisse werden ausreichend kritisch interpretiert.

Die vorhandenen wissenschaftlichen Ergebnisse und Grafiken müssen nicht grundlegend verändert werden.

**SCIENTIFICALLY APPROVED.**

**TECHNICAL APPROVAL PENDING SUCCESSFUL CI.**

Mein Originalreview ist unverändert zu erhalten. Technische Präzisierungen sind separat zu dokumentieren.

Ich erteile mit diesem Review keine Merge-Autorisierung.

---

## Codex-Verifikation nach Human Review – 19.11.2026

Aktueller Stand: SCIENTIFICALLY APPROVED; technische GitHub-Freigabe bis zum
erfolgreichen Abschluss der neuen Head-CI ausstehend. Kein Merge autorisiert.
Originalreview unverändert separat in d2525b8 gesichert; vorheriger Bericht erhalten.

Sichere CI-Korrektur: vorhandene Original-CSV (522.048 Bytes, unveränderter SHA256
dc6630cd9b1f0f853922fad78a1b6436570d3f1ec863f1dd5c4340ac56bc8a8e)
unter data/raw versioniert; Herkunft/CC BY 4.0 und Grund im dortigen README ergänzt.
Der bestehende Downloader bestätigt den Bestand ohne Netzabruf. Keine TLS-Ausnahme,
keine geänderte Quelle, keine geänderten Daten oder Modellparameter. Die früheren
CI-Fehlläufe 44607242799/44607347699 bleiben sichtbar.

Tatsächlich erneut bestanden:
- `scripts/uv.cmd run --offline --locked python scripts/download_ai4i.py`: lokaler Originalbestand SHA256-bestätigt, kein Download.
- `scripts/uv.cmd run --offline --locked python -m unittest discover -s tests -p test_overstrain.py -v`: 3/3 bestanden, 1,765 s.
- `scripts/uv.cmd run --offline --locked python scripts/build_exercise_14_2.py --check-html`: 3 frische sequenzielle Zellen; 3 eingebettete Bilder; Offline-HTML 900/1400 px ohne Seitenfehler, fehlgeschlagene Anfragen oder Überlauf.
- Zusätzlicher Artefaktabgleich: 98 OSF = 87/9/2 nach L/M/H, 21 Anpassungsfehler des Zwei-Merkmal-Baums bei Tiefe 8; beide Fehler des Produkt+Type-Kursbaums bei Tiefe 3 sind positive H-Fälle. Alle CSV/JSON/PNG/Text-Ergebnisse bytegleich mit 4de7a9d; 21 Archive unverändert.

Technische Präzisierungen zum unveränderten studentischen Text: Type bezeichnet die
**Produktvariante**. Die Grafik der Entscheidungsgrenzen nutzt nur Verschleiß und
Drehmoment; der separat verglichene Kursbasisbaum nutzt die sieben im Notebook
genannten Eingaben. Die Zahlen 43/22/2 beziehen sich auf diesen Kursbasisvergleich.
Keine Änderung des studentischen Wortlauts oder seiner wissenschaftlichen Bewertung.
Bekannte lokale Jupyter-TCP-Warnung erneut ohne Ausführungsfehler. Keine zusätzliche
Modellstudie oder neue Testsuite; aktuelle CI-Nachweise werden im bestehenden PR #15
am tatsächlichen Head dokumentiert. Finale Merge-Autorisierung bleibt ausstehend.
