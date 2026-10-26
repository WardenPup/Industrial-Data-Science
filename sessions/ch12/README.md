# Kapitel 12 – Self study, Session 3

Quelle: https://noxthot.github.io/ws26_industrial_datascience_manuscript/1_act1/8_self_study_session3.html

12.1: STUDENT APPROVED, PR #9 regulär integriert. Notebook gesture_clustering.ipynb,
Datenabruf scripts/download_gestures.py, Export scripts/build_exercise_12_1.py.
Originaler Human Review bleibt unverändert erhalten.

12.2: KI-gestützte Implementierung durch Codex, studentisch wissenschaftlich freigegeben;
APPROVED – AWAITING FINAL MERGE AUTHORIZATION.
Notebook uwave_classification.ipynb; Datenabruf scripts/download_uwave.py;
Export scripts/build_exercise_12_2.py. Alle Skripte vom Projektstamm mit uv ausführen.
Anforderungen: docs/EXERCISE_12_2_REQUIREMENTS.md; Review: reviews/exercise_12_2.md.
12.3: aeon TimeSeriesForestClassifier, 200 Bäume, Seed 42; `uwave_forest.ipynb`.
HTML und CSV/JSON/PNG: `outputs/ch12/exercise_12_3`; Export: `scripts/build_exercise_12_3.py`.
Status SCIENTIFICALLY APPROVED – TECHNICALLY VALIDATED – AWAITING FINAL MERGE AUTHORIZATION. 12.4: AppliancesEnergy, 95 TRAIN/42 TEST mit 24 × 144; DTW-3-NN-, Forest- und CNN-Regressor.
Notebook `appliances_regression.ipynb`; Export `scripts/build_exercise_12_4.py`;
Originaldaten explizit über `scripts/download_appliances.py`, danach offline.
Ausgaben `outputs/ch12/exercise_12_4`; Status SCIENTIFICALLY APPROVED – TECHNICALLY VALIDATED – AWAITING FINAL MERGE AUTHORIZATION.
Quelle/Lizenz: `docs/APPLIANCES_SOURCE.md`; keine Universitätseinreichung.
Vergleich nutzt freigegebene Git-Referenz 50d3a01; Hashes und aktuelle wissenschaftliche
Werte werden geprüft, laufzeitabhängige Fit/Predict-Spalten nicht als Ergebnisse verglichen.
Ohne Git werden die unveränderten Referenzdateien aus 12.2 benötigt (siehe forest_reference.json).
