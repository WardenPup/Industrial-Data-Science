# Aufgabe 12.4 – Anforderungen und vorab festgelegtes Vorgehen

Offizielle Quelle, gelesen 26.10.2026:
https://noxthot.github.io/ws26_industrial_datascience_manuscript/1_act1/8_self_study_session3.html
Exercise 12.4 „Regression of multivariate time series“ verlangt genau:
1. AppliancesEnergy laden.
2. Zeitreihen-kNN zur Vorhersage des Energieverbrauchs anwenden.
3. Zeitreihen-Random-Forest-Tree-Regressor anwenden.
4. CNN-Regressor anwenden.
5. Ergebnisse vergleichen.
Der benachbarte Hinweis empfiehlt aeon.datasets.load_regression mit originalen
TRAIN/TEST-Splits. Keine konkrete Architektur, Zielgüte, weitere Modelle oder
Metriken vorgeschrieben. Kurskapitel 9 nutzt RMSE nach Rücktransformation der Ziele:
https://noxthot.github.io/ws26_industrial_datascience_manuscript/1_act1/5_1_timeseries_regression.html

## Datenbefund vor Modelltraining
Installiertes aeon 1.6.0 verweist auf Zenodo 18484626, Originaldateien unverändert
unter data/raw/AppliancesEnergy; MD5 gegen Zenodo geprüft, SHA256 in
sessions/ch12/appliances_source.json. Tatsächlich 95 TRAIN und 42 TEST, je 24 Kanäle
und 144 Abtastwerte. y ist kontinuierlich (TRAIN 5,34–26,28; TEST 9,33–24,12).
Keine Neuaufteilung, kein Resampling oder Imputation. Die alte TSER-Beschreibung
(https://zenodo.org/records/3902637) nennt Gesamtenergie in kWh und 138 Zeitreihen;
die tatsächlich geladenen neuen Dateien enthalten zusammen 137. Keine fehlenden
Fälle erfinden. UCI-Ursprung hat 19.735 Zeilen und Ziel Appliances in Wh; dies ist
nicht die fertige TSER-Darstellung und wird nicht stillschweigend ausgetauscht.
Zeit-/Gebäudeunabhängigkeit des Benchmark-Splits ist nicht durch .ts belegt.

## Festgelegte Modelle, keine TEST-Optimierung
- Ein gemeinsamer TRAIN-only-Kanalskalierer (Mittelwert/Populationsstandardabweichung)
  aus der geprüften 12.2-Funktion; unverändert auf TEST. Bäume benötigen keine
  Skalierung, erhalten aber dieselbe Darstellung. Kein Target als Eingabekanal.
- aeon KNeighborsTimeSeriesRegressor: k=3, uniforme Gewichte, DTW mit window=0.1,
  ein Thread. Zielvorhersage Mittelwert der Nachbarziele, keine Klassifikation.
- aeon TimeSeriesForestRegressor: 200 Bäume, sqrt-Intervalle, Mindestlänge 3,
  random_state=42, n_jobs=1, kein Zeitlimit. aeon 1.6 nutzt squared_error-Bäume
  auf Intervallmittelwert/Standardabweichung/Steigung; gemittelte Vorhersagen.
- PyTorch-CPU-CNN mit Conv1d 24→16 (Kernel 7, same), ReLU, MaxPool 2,
  Conv1d 16→32 (Kernel 5, same), ReLU, AdaptiveAvgPool 8, Flatten, Linear 256→1.
  Eine lineare kontinuierliche Ausgabe, kein Softmax. Adam 0,001, MSE,
  Batch 16, 60 feste Epochen, Seed 42, deterministischer CPU-Lauf/ein Thread.
  TRAIN-only-Zielstandardisierung für CNN und Rücktransformation vor Bewertung.
  Ein kompakter eigener CNN-Regressor erfüllt die Methode ohne zusätzliche
  TensorFlow-Abhängigkeit; Architektur aus 12.2 sachgerecht zur Regression angepasst.
Alle Parameter sind Modellannahmen, keine als optimal belegten Einstellungen.
Keine zusätzliche Modell-, Seed-, Hyperparameter- oder Validierungsstudie beauftragt.

## Ausgaben und Akzeptanz
RMSE als Hauptmetrik (kWh), MAE (kWh) als verständliche Ergänzung; beide selbst
arithmetisch nachrechnen. Drei Modelle auf identischen TEST-Zielen vergleichen.
Keine Accuracy/Confusion-Matrix für kontinuierliche Ziele. Zwei kompakte Figuren:
TRAIN-Signalbeispiel/CNN-Trainingsverlust sowie drei Ist-Vorhersage-Panels mit
Identitätsgerade und gemeinsamer Skala. Keine unbestellten Zusatzanalysen.
Notebook sessions/ch12/appliances_regression.ipynb, lesbarer Offline-HTML-Export,
PNG/CSV/JSON/NPZ unter outputs/ch12/exercise_12_4, SHA256-Manifest.
Nach späterer Genehmigung ein ZIP mit Notebook+HTML, relevanten Modulen, Datenquelle
und pyproject.toml/uv.lock möglich; kein PDF verlangt. Jetzt keine Abgabe erstellen.

Tests zu TRAIN-only-Skalierung/Zielrücktransformation, kNN-Mittelwert, Forest-
Aggregation, CNN-Output/Lernschritt/Seed, Rohdaten und unabhängigen Metriken.
Frischen Kernel sequenziell ausführen; zweiten vollständigen Fit zum Reproduzieren
aller TEST-Vorhersagen; gespeicherte CNN-Gewichte ohne Pickle laden und prüfen.
Beide Figuren visuell, HTML offline 900/1400 px, Hashes und frühere Ergebnisse/
Reviews/acht Abgabe-ZIPs prüfen. Tatsächliche Kommandos/Warnungen dokumentieren.

## Grenzen und Review
Nur 95 TRAIN-Fälle, ein Seed/ein gegebener Split, kein separates Validierungsset.
Keine allgemeine oder signifikante Überlegenheit, kein Kalibrierungs-/Kausalitäts-
oder Zukunftsprognosenachweis. Messungen aus einem Haus erlauben keine Aussage
zu anderen Gebäuden. Niedriger Trainingsverlust beweist weder Generalisierung
noch Overfitting. Rangfolge nach TEST bleibt deskriptiv, nicht Tuning-Kriterium.
KI-Unterstützung: Codex. Nach technischer Prüfung AWAITING HUMAN REVIEW; keine
studentische Freigabe, kein Merge/Upload. Keine bisherigen Lösungen verändern.
