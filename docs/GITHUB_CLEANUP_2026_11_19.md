# GitHub-Bereinigung – 19.11.2026

Codex, ausschließlich administrative Pflege nach ausdrücklichem Nutzerauftrag.
Remote exakt: https://github.com/WardenPup/Industrial-Data-Science.git .
main unverändert: `1d8c583186dfa8a9691204a6902a50f10c086a74`.

## Tatsächlich entfernt

Alle folgenden Branch-Spitzen waren vor der atomaren Löschung Vorfahren von origin/main,
ihre zugehörigen PRs gemergt, keine offenen PRs zu diesen Branches, nicht geschützt.
Gelöscht wurden nur Remote-Verweise; lokale Branches und sämtliche Commits bleiben erhalten.

| Remote-Branch | Erhaltener Head | Gemergter PR |
|---|---|---|
| exercise/10.1 | `88d623e016e127cad5e14a9853cf0bb72469b1de` | #1 |
| exercise/10.2 | `793f961ec6fd6399bd6bd77dcf3d9e6951609e34` | #2 |
| exercise/10.3 | `c9c58ab85821e3f8cd24a3490d8c7c7d1bf4796b` | #3 |
| exercise/10.4 | `608c0fa67088e5000967188e9abb9785204b70c3` | #4 |
| exercise/11.1 | `ef7451f5eaafa605e693fdcd43dc50af75df9ae0` | #5 |
| exercise/11.2 | `00842a15c3542ca750203edaa7c861608aa830fe` | #6 |
| exercise/11.3 | `d20340062d4a65ac2b20478e7e10ecf60a41cb21` | #7 |
| exercise/11.4 | `f1f6f5d5628e0cf4d2b75ecca806e49e15d458a3` | #8 |
| exercise/12.1 | `96d58bef27b21836e110912f6b0449b3e6482b38` | #9 |
| exercise/12.2 | `50d3a014fb42b055b12e60188df2df82ea5918f5` | #10 |
| exercise/12.3 | `efc7d46bf1ce65c58baf52c024433d00889ff6e4` | #11 |
| exercise/12.4 | `98641c9555d6589590d144c3918ad873c4411796` | #12 |

## Erhalten und offen

Remote verbleiben main und submission/final-preparation.
[PR #13](https://github.com/WardenPup/Industrial-Data-Science/pull/13): offen, Draft, konfliktfrei;
bei Prüfung null Review-/Gesprächskommentare und keine eingereichten Reviews.
Bisheriger Head `1dc0e99b208aa8a2279a05592ad26ca34d92caa7`:
[PR-CI 40422141330](https://github.com/WardenPup/Industrial-Data-Science/actions/runs/40422141330)
tatsächlich completed/success. Kein Push-Lauf für submission/** konfiguriert.
Die kleine Statuskorrektur im selben offenen Branch erhält eine neue PR-CI;
deren Ergebnis ist am aktuellen Head zu lesen, nicht vom früheren Erfolg abzuleiten.
Keine Paketfreigabe oder Merge-Autorisierung erfunden; PR bleibt Draft.

## Erhaltungsprüfung

21 vorhandene ZIP-/RAR-Archive vor und nach der Branchlöschung SHA256-identisch.
Die nicht versionierte lokale RAR-Datei blieb unangetastet und wurde nicht committed.
Keine Änderungen an Berechnungen, Notebooks, Ergebnissen oder Originalreviews.
Nur aktuelle Einstieg-/Statusdokumentation aktualisiert; historische Reviewprotokolle bleiben bestehen.
Prüfungen: GitHub-PR-/Branch-/CI-Abfrage, git fetch --prune, git ls-remote,
git merge-base --is-ancestor, atomarer normaler Git-Delete-Push und Archivhashvergleich.
Kein Force-Push, keine Historienumschreibung, kein Merge und keine Hochschuleinreichung.
Keine wissenschaftlichen Tests wiederholt: ausschließlich Branch-/Dokumentationsänderungen.

## Nächster offizieller Self-Study-Schritt

Kursindex am 19.11.2026 per HTTPS gelesen (Webwerkzeug nicht erreichbar, direkter Abruf erfolgreich):
https://noxthot.github.io/ws26_industrial_datascience_manuscript/ .
Nach Kapitel 12 folgt im Index **Kapitel 14 – Self-Study Session 1 (Act 2)**:
https://noxthot.github.io/ws26_industrial_datascience_manuscript/2_act2/1_self_study_session1.html .
Nur Indexreihenfolge festgestellt; keine Aufgabenanalyse oder Implementierung begonnen.
