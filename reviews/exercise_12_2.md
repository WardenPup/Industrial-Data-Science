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
