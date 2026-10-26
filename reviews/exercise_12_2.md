# Aufgabe 12.2 – Human-AI Review

Status: AWAITING HUMAN REVIEW

## KI-Beitrag
Codex analysierte die offiziellen Anforderungen, prüfte das multivariate Originalarchiv,
implementierte gemeinsame TRAIN-Skalierung, DTW-3-NN und das 1D-CNN samt Notebook,
Export und technischer Prüfung. Keine studentische Rückmeldung oder Freigabe vorliegend.

## Konkrete Entscheidungen
120 TRAIN-/320 TEST-Gesten, drei Kanäle und 315 Werte, acht Klassen. Kein Resampling.
Die Katalogseite nennt abweichende Fallzahlen; tatsächliche Original-.ts-Dateien und
Hashes sind maßgeblich (docs/UWAVE_SOURCE.md), keine Stichprobenauswahl.
Trainingsstandardisierung gemeinsam für beide Methoden, kein Fit auf TEST.
kNN: k=3, uniforme Stimmen, DTW mit window=0.1. CNN: zwei Faltungen, 5.000 Parameter,
Adam 0,001, Batch 16, 60 feste Epochen, Seed 42, CPU. Keine Hyperparameteroptimierung.

## Ergebnisse der ersten tatsächlichen Ausführung
DTW-3-NN: Accuracy/Balanced Accuracy 0,909375, Macro-F1 0,908593.
CNN: Accuracy/Balanced Accuracy 0,846875, Macro-F1 0,846505.
Korrekt 291/320 bzw. 271/320. Keine Aussage über allgemeine Überlegenheit.

## Fragen an den studentischen Review
1. Ist die gemeinsame nur auf TRAIN geschätzte Kanalskalierung nachvollziehbar?
2. Sind DTW mit gemeinsamem Pfad und die CNN-Architektur inklusive Pooling verständlich?
3. Welche Verwechslungen zeigen die Confusion-Matrizen, und stützen sie den Vergleich?
4. Ist die Trennung von Trainingsverlust, Testleistung und fehlender Validierungsstudie klar?
5. Sind ein Seed, nur 120 Trainingsfälle, unbestätigte Gruppenunabhängigkeit und die
   abweichenden Katalogzahlen ausreichend transparent eingeordnet?

## Grenzen
Keine Seed-/Hyperparametersuche oder Signifikanzprüfung. Feste Annahmen, ein Split;
TRAIN-Verlust belegt keine Generalisierung. Keine bewiesenen unbekannten Personen
oder zukünftigen Daten im TEST. Keine physikalischen Einheiten oder Lizenz erfinden.

## Technische Validierung
Tatsächlich ausgeführt am 26.10.2026, projektlokales uv, --offline --locked:
- `python -m unittest discover -s tests -v`: 52 Tests erfolgreich in 17,195 s;
  darunter sieben neue Tests für Skalierung ohne TEST-Fit, fehlende/ungültige Werte,
  Rohdatenchecksum, bekannte multivariate DTW-Nachbarn, CNN-Shape/5.000 Parameter,
  Kreuzentropie/Lernschritt, Seed-Reproduktion, Fit/Predict-Grenze und Handmetriken.
- `python scripts/build_exercise_12_2.py`: frischer Kernel, drei sequenzielle Codezellen,
  zwei dekodierte eingebettete PNGs. Confusion-Matrizen manuell aus allen 320
  Vorhersagen aufgebaut, Accuracy/Recall/Precision/Macro-F1 und Klassenberichte
  daraus unabhängig nachgerechnet. TRAIN-Skalierer separat nachgerechnet.
  Gespeicherte CNN-Gewichte ohne Pickle geladen und alle CNN-Vorhersagen bestätigt.
- `python scripts/check_exercise_12_2_html.py`: offline bei 900/1400 px, zwei Bilder
  geladen, keine Seitenfehler und kein horizontaler Überlauf.
- Beide Abbildungen mit vier Teilplots visuell geprüft: Kanalbeispiel,
  Trainingsverlust, beide korrekt beschrifteten Confusion-Matrizen mit gleicher Skala.
- Alle 640 Modellvorhersagen stimmen exakt mit der ersten Ausführung überein;
  keine Hyperparameter nach Kenntnis der Testergebnisse verändert.
- Beide Rohdateihashes und zwölf Manifest-Artefakte geprüft. Alle acht Kapitel-10/11-
  ZIPs unverändert (SHA256/CRC), frühere wissenschaftliche Ergebnisse und Reviews erhalten.

CNN-Training: mittlere Kreuzentropie von etwa 2,0311 auf 0,003105 gesunken;
das ist Trainingsoptimierung, keine separate Validierung. Auf TEST werden die
Klassen 7.0/8.0 von kNN je 40/40, vom CNN je 36/40 richtig erkannt. Beide Methoden
verwechseln elf Gesten von 4.0 mit 5.0; keine kausale Erklärung daraus abgeleitet.

Umgebung: sieben notwendige neue Pakete (torch 2.9.1+cpu, filelock, fsspec,
mpmath, networkx, setuptools, sympy), keine bestehenden Paketversionen geändert,
keine CUDA-Pakete. CPU-Index explizit nur für torch. Cache-Konfiguration aus uv.toml
nach pyproject.toml übernommen. Ein erster Konfigurationsversuch mit Index in uv.toml
wurde von uv als undeclared index abgewiesen; korrigiert, danach locked/offline sync
erfolgreich. uv meldete temporäre Cache-Rename-Retries, Installation erfolgreich.
Tatsächliche Warnungen: Numba uint64→int64 bei DTW und lokale unverschlüsselte
Jupyter-TCP-Kommunikation; keine fehlgeschlagenen numerischen Tests.

Keine studentische Prüfung oder Freigabe behauptet. Wissenschaftlicher Review ausstehend.



# Human Review – Exercise 12.2

**Reviewer:** Student  
**Aufgabe:** Exercise 12.2 – Zeitreihenklassifikation mit DTW-kNN und CNN  
**Status:** SCIENTIFICALLY APPROVED – AWAITING TECHNICAL RECONCILIATION

## 1. Gesamtbeurteilung

Ich habe die Ergebnisse, die beiden Abbildungen und die bereitgestellten Ergebnisdateien geprüft. Die Umsetzung ist nachvollziehbar, die Darstellungen sind verständlich und der Methodenvergleich beantwortet die wesentlichen Fragestellungen der Aufgabe.

Die Auswertung verwendet 120 TRAIN- und 320 TEST-Gesten mit jeweils drei Sensorkanälen und 315 Abtastwerten. Beide Verfahren werden auf demselben TEST-Split bewertet.

Ich beurteile die Aufgabe aus studentischer Sicht positiv. Die bekannten methodischen Einschränkungen müssen in der Dokumentation erhalten bleiben.

## 2. Vorverarbeitung und Datenaufteilung

Die Standardisierung der drei Sensorkanäle ist für den Vergleich nachvollziehbar. Die dargestellte Beispielgeste zeigt, dass trotz der Transformation unterschiedliche zeitliche Signalverläufe erhalten bleiben.

Die Skalierungsparameter wurden laut technischem Prüfbericht ausschließlich auf TRAIN bestimmt und anschließend auf TEST angewendet. Diese Trennung ist wichtig, damit keine Informationen des TEST-Splits in die Vorverarbeitung einfließen.

Die feste Länge von 315 Abtastwerten ermöglicht eine gemeinsame Eingabeform für beide Modelle. Dabei können Unterschiede in der ursprünglichen zeitlichen Auflösung beziehungsweise Bewegungsdauer an Bedeutung verlieren. Diese Einschränkung sollte ausdrücklich dokumentiert bleiben.

## 3. Bewertung von DTW-3-NN

Das Verfahren erreicht auf den 320 TEST-Gesten eine Accuracy von 90,9375 % und einen Macro-F1-Wert von 0,908593.

291 Gesten werden richtig, 29 falsch klassifiziert.

DTW erlaubt den Vergleich zeitlich unterschiedlich verlaufender Signalformen. Die Verwendung von drei Nachbarn und eines begrenzten DTW-Fensters ist als Modellkonfiguration nachvollziehbar, stellt aber keine nachgewiesen optimale Parameterwahl dar.

Besonders positiv fällt auf, dass die Klassen 2, 7 und 8 vollständig richtig klassifiziert werden. Bei Klasse 4 werden dagegen nur 28 von 40 Gesten korrekt erkannt. Elf werden Klasse 5 zugeordnet.

## 4. Bewertung des CNN

Das CNN erreicht eine Accuracy von 84,6875 % und einen Macro-F1-Wert von 0,846505.

271 Gesten werden richtig, 49 falsch klassifiziert.

Die Architektur mit 5.000 trainierbaren Parametern ist für einen überschaubaren Modellvergleich angemessen. Die Lernkurve zeigt einen kontinuierlichen Rückgang des Trainingsverlusts von ungefähr 2,031 auf 0,0031 innerhalb von 60 Epochen.

Daraus folgt, dass sich das Modell sehr stark an die Trainingsdaten anpasst. Da keine separate Validierungsverlustkurve dargestellt ist, lässt sich daraus allein aber keine sichere Aussage über Overfitting ableiten.

Auch das CNN verwechselt elf Gesten der Klasse 4 mit Klasse 5. Insgesamt werden bei Klasse 4 nur 25 von 40 Gesten korrekt erkannt. Weitere Fehler betreffen unter anderem die Klassen 1, 3, 7 und 8.

## 5. Methodenvergleich

DTW-3-NN liefert in diesem konkreten Experiment das bessere Klassifikationsergebnis.

Der Unterschied beträgt 6,25 Prozentpunkte in der Accuracy. DTW-3-NN klassifiziert 20 zusätzliche TEST-Gesten korrekt.

Das bedeutet nicht, dass DTW grundsätzlich jedem CNN überlegen ist. Das Ergebnis gilt für die verwendeten Daten, die gewählten Hyperparameter, die feste Trainingskonfiguration und den dokumentierten Seed.

Die deutlich unterschiedlichen Rechenzeiten zeigen außerdem, dass Modellanpassung und Vorhersageaufwand getrennt betrachtet werden müssen. Der kleine Trainingsaufwand des kNN darf nicht mit einer grundsätzlich geringeren Gesamtrechenzeit gleichgesetzt werden.

## 6. Bewertung der Abbildungen

Die Darstellung der standardisierten Beispielgeste ist gut lesbar. Die drei Kanäle sind farblich unterscheidbar und die Achsen nachvollziehbar beschriftet.

Die Trainingsverlustkurve zeigt die Entwicklung über alle 60 Epochen ohne offensichtliche Unterbrechung.

Die beiden Confusion-Matrizen ermöglichen einen direkten Vergleich der Klassifikationsergebnisse. Die Achsen stellen tatsächliche und vorhergesagte Klassen korrekt getrennt dar.

Die Häufung der Verwechslungen zwischen Klasse 4 und Klasse 5 ist klar erkennbar.

Ich halte die vorhandenen Grafiken für ausreichend. Zusätzliche Abbildungen sind für die Beantwortung der Aufgabe nicht erforderlich.

## 7. Wissenschaftliche Einschränkungen

Die folgenden Grenzen bleiben ausdrücklich bestehen:

- Es liegt nur eine dokumentierte Trainingskonfiguration mit Seed 42 vor.
- Die Hyperparameter wurden nicht systematisch hinsichtlich ihrer Robustheit untersucht.
- Der TEST-Split darf nicht nachträglich zur Modellauswahl verwendet werden.
- Die kleine TRAIN-Menge von 120 Gesten begrenzt die Aussagekraft des CNN-Ergebnisses.
- Der niedrige Trainingsverlust ist kein eigenständiger Beweis guter Generalisierung.
- Die Verwechslung von Klasse 4 und Klasse 5 ist beobachtet, ihre physikalische beziehungsweise bewegungsbezogene Ursache jedoch nicht nachgewiesen.
- Die Laufzeiten gelten für die dokumentierte Ausführungsumgebung und sind kein allgemeiner Hardwarevergleich.
- Die Aussagekraft des Ergebnisses ist auf diesen Datensatz und die gewählte Versuchsanordnung begrenzt.

## 8. Abschließendes Urteil

Die Aufgabenstellung ist aus meiner Sicht fachlich nachvollziehbar umgesetzt. Die wesentlichen Ergebnisse lassen sich anhand der Grafiken und Ergebnisdateien erklären.

Die beiden Methoden wurden unter vergleichbaren dokumentierten Bedingungen bewertet. Der höhere TEST-Erfolg von DTW-3-NN ist eindeutig erkennbar, ohne dass daraus eine allgemeine Überlegenheit abgeleitet wird.

Ich sehe auf Grundlage der geprüften Materialien keinen wissenschaftlichen Grund für eine grundlegende Überarbeitung.

**Studentische Entscheidung: APPROVED.**

Die technische Abschlussprüfung, der Abgleich mit dem Repository und die finale Merge-Autorisierung bleiben getrennte Schritte.

Keine automatische Merge- oder Einreichungsfreigabe.
