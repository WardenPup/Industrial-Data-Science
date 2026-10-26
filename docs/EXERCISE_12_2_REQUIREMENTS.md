# Aufgabe 12.2 – Anforderungen und vorab festgelegter Vergleich

KI-gestützte Analyse; offizielle Aufgabenstellung vollständig per HTTPS gelesen
am 26.10.2026:
https://noxthot.github.io/ws26_industrial_datascience_manuscript/1_act1/8_self_study_session3.html
Pflicht: UWaveGestureLibrary laden, Zeitreihen-kNN und CNN klassifizieren lassen,
Ergebnisse vergleichen. Keine vorgeschriebene Architektur, Sollgenauigkeit oder PDF.
Der nachfolgende Forest-Hinweis ist keine zusätzliche Pflichtmethode für 12.2.

## Daten und Abgrenzung
Originales multivariates UCR/UEA-Archiv:
https://www.timeseriesclassification.com/aeon-toolkit/UWaveGestureLibrary.zip
Die tatsächlich gelieferten .ts-Dateien enthalten TRAIN (120,3,315), TEST
(320,3,315), acht Klassen und keine fehlenden Werte. Vollständige Dateien verwenden,
keine Teilstichprobe, kein Resampling, keine Vermischung mit UWaveGestureLibraryAll
oder einzelnen X/Y/Z-Datensätzen. Herkunft und Dateichecksummen werden dokumentiert.
Die Online-Beschreibungsseite nennt abweichend 2238/2241 Fälle; für diese Lösung
sind die tatsächlich geladenen Originaldateien mit @problemName UWaveGestureLibrary,
@dimensions 3 und @seriesLength 315 maßgeblich. Abweichung offen benennen.
Keine separate Datenlizenz oder physikalischen Einheiten erfinden.

## Faire Bedingungen und Leakage-Grenzen
Beide Modelle erhalten dieselben vollständigen TRAIN-Fälle und dieselbe gemeinsame
kanalweise Standardisierung. Mittelwert/Standardabweichung je Kanal ausschließlich
über TRAIN-Fälle und deren Zeitpositionen fitten; unverändert auf TEST anwenden.
Klassenkodierung nur auf TRAIN lernen. Jeder Fall bleibt eine dreikanalige Geste;
keine Zeitpunkte derselben Geste auf Training und Test verteilen.
Der vorgegebene Split bleibt erhalten; unbekannte Personen-/Chronologieangaben
werden nicht als bewiesene Gruppenunabhängigkeit ausgegeben.

Alle folgenden Hyperparameter werden vor der Testauswertung festgelegt; kein
Testlabeltuning, keine Suche oder Auswahl anhand von Testmetriken. Ohne separate
Validierungsstudie wird weder Hyperparameteroptimalität noch Stabilität behauptet.
Test wird erst nach vollständigem Fit beider Modelle für die Endauswertung genutzt.
Frische Wiederholung prüft Reproduktion, nicht nachträgliche Modellwahl.

## Methoden und Verständlichkeit
- aeon KNeighborsTimeSeriesClassifier: k=3, uniforme Stimmen, multivariate DTW,
  gemeinsamer Warping-Pfad aller Kanäle, window=0.1, ein CPU-Thread.
  DTW-Dynamikprogramm und Kanalbehandlung kurz erläutern.
- CNN mit PyTorch CPU: Conv1d 3→16 (Kernel 7, same), ReLU, MaxPool(2),
  Conv1d 16→32 (Kernel 5, same), ReLU, AdaptiveAvgPool(8), Flatten, Linear 256→8.
  5.000 trainierbare Parameter; acht Logits, CrossEntropyLoss, Adam lr=0.001,
  Batch 16, 60 feste Epochen, kein Early Stopping oder Test-Checkpointing.
  Seed 42, ein CPU-Thread, deterministische Algorithmen; keine GPU erforderlich.
  Die Architektur bewahrt grobe Zeitpositionen statt alle Kanäle zu verketten.

## Abnahme, Ausgaben und Tests
Originaldaten SHA256 prüfen und unverändert lassen. Leckagegrenze der Skalierung
mit künstlich verschobenen Testdaten testen; Eingabeformat und fehlende Werte
explizit prüfen. CNN-Ausgabe, Lernschritt, Seed-Reproduktion und kNN-/DTW-Verhalten
auf kleinen bekannten Fällen prüfen. Accuracy, Balanced Accuracy, Macro-F1 und
pro Klasse Precision/Recall/F1/Support berichten; zwei Confusion-Matrizen mit
explizit gleicher Klassenreihenfolge. Alle 320 Testvorhersagen exportieren.
Nur nötige Grafiken: multivariates TRAIN-Beispiel, gemeinsame Confusion-Darstellung,
CNN-Trainingsverlust. Trainingsverlust beweist keine Generalisierung.
Notebook frisch sequenziell ausführen, HTML offline bei 900/1400 px prüfen,
alle Grafiken visuell prüfen und tatsächliche Befehle/Resultate dokumentieren.
Notebook plus HTML und relevante Module/Daten-/Umgebungsangaben für spätere
ZIP-Abgabe vorsehen; kein PDF und keine Universitätseinreichung erforderlich.

## Grenzen und Review
120 Trainingsgesten, ein Seed und ein unveränderter Split liefern nur einen
begrenzten Modellvergleich; kNN und CNN besitzen unterschiedliche induktive
Annahmen und Rechenkosten. Keine allgemeine Überlegenheit, Kausalität oder
personenunabhängige Generalisierung behaupten. Keine Optimierungsstudie durchgeführt.
KI-Beiträge transparent, konkrete wissenschaftliche Reviewfragen vorbereiten.
Status nach technischer Prüfung: AWAITING HUMAN REVIEW. Kein Merge 12.2/Start 12.3.

## Gelesene Primärdokumentation
https://www.aeon-toolkit.org/en/stable/api_reference/auto_generated/aeon.classification.distance_based.KNeighborsTimeSeriesClassifier.html
https://www.aeon-toolkit.org/en/stable/api_reference/auto_generated/aeon.distances.dtw_distance.html
https://docs.pytorch.org/docs/2.9/generated/torch.nn.Conv1d.html
https://docs.pytorch.org/docs/2.9/generated/torch.nn.AdaptiveAvgPool1d.html
https://docs.pytorch.org/docs/2.9/generated/torch.nn.CrossEntropyLoss.html
