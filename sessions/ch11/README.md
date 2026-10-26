# Kapitel 11 – Self study, Session 2

Aufgabe 11.1 fachlich APPROVED nach studentischem Review vom 26.10.2026;
nach erfolgreicher CI und ausdrücklicher Erlaubnis als PR #5 regulär gemergt (b7543e0).
11.2 fachlich APPROVED (Review 26.10.2026), erneut technisch geprüft;
PR #6 nach ausdrücklicher Erlaubnis regulär gemergt (84085f5).
11.3 fachlich positiv geprüft und technisch erneut validiert:
APPROVED – AWAITING FINAL MERGE AUTHORIZATION. 11.4 nicht begonnen.
Quelle: https://noxthot.github.io/ws26_industrial_datascience_manuscript/1_act1/7_self_study_session2.html
Gelesen am 26.10.2026. Notebook: `production_smoothing.ipynb`.

Vom Projektstamm: `scripts/uv.cmd run --locked python scripts/download_production.py`,
danach offline `scripts/uv.cmd run --offline --locked python scripts/build_exercise_11_1.py`.
HTML und zwei Grafiken: `outputs/ch11/exercise_11_1/`.
Zentrierter 5-Wochen-Median, exakte Lückenmaske; keine Imputation.

11.2: `production_imputation.ipynb`, sechs Kapitel-5-Imputationsvarianten auf
dem freigegebenen Median. Export: `scripts/build_exercise_11_2.py` über uv starten;
HTML und sieben Grafiken unter `outputs/ch11/exercise_11_2/`.

11.3: `production_stl_imputation.ipynb`, zweistufige STL-Imputation.
Builder `scripts/build_exercise_11_3.py`; vier Grafiken, HTML und Tabellen unter
`outputs/ch11/exercise_11_3/`. statsmodels projektlokal im uv-Lockfile.
