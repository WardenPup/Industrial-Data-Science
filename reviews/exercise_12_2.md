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
Wird nach tatsächlichen Prüfungen ergänzt. Keine studentischen Tests behauptet.
