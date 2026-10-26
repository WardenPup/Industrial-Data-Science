# Aufgabe 12.1 – Human-AI Review

Status: AWAITING HUMAN REVIEW

## KI-Beitrag
Codex analysierte die offizielle Aufgabe, implementierte Datenprüfung,
Vorverarbeitung, euklidisches Zeitreihen-k-Means und KASBA/MSM, Notebook und Export.
Kein studentischer Review und keine Freigabe für 12.1 vorliegend.

## Entscheidungen und Grenzen
132 TRAIN-/172 TEST-Fälle, getrennte Aufnahmesessions derselben Personen.
128 relative Zeitpositionen, je Reihe z-Normalisierung; keine physikalischen
Einheiten erfunden. Seed 42, k=6 als bekannter Klassenumfang, kein Testlabeltuning.
ARI/NMI sind externe Clustermetriken, keine Klassifikationsgenauigkeit.
Resampling entfernt Dauer-/Feinstruktur; Normalisierung Amplitudeninformation.
Ein Seed belegt keine Stabilität. KASBA-Vergleich ändert Distanz und Optimierung;
Laufzeiten können JIT enthalten. Ungeklärte Datenlizenz transparent dokumentiert.

## Konkrete studentische Reviewfragen
1. Sind relative Zeit und je-Reihe-Normalisierung für den Gestenvergleich sinnvoll,
   und ist der Verlust von Dauer/Niveau/Amplitude verständlich eingeordnet?
2. Ist k=6 als Benchmarkannahme ausreichend begründet, ohne natürliche Cluster zu behaupten?
3. Sind die besseren externen KASBA-Werte anhand der Kreuztabellen nachvollziehbar,
   einschließlich Klassen-/Cluster-Unterscheidung und Sessiongrenzen?
4. Können Move, Split, Merge und die MSM-Beispielmatrix nachvollzogen werden?
5. Sind geschätzte Zentren und transformierte Messungen in der Grafik klar getrennt?

## Technische Validierung
Am 26.10.2026 tatsächlich im projektlokalen uv-Environment ausgeführt:
- `scripts/uv.cmd run --offline --locked python -m unittest discover -s tests -v`:
  45 Tests erfolgreich in 10,307 s. Darunter analytisches Resampling/Normalisierung,
  konstante/ungültige Daten, MSM-Handrechnung und Bibliotheksreferenz, Originalsplits,
  tatsächliche Estimator-Fits mit festem Seed und Vorhersagefähigkeit.
- `scripts/uv.cmd run --offline --locked python scripts/build_exercise_12_1.py`:
  fünf frische sequenzielle Codezellen, vier dekodierte eingebettete Bilder.
  Alle 132/172 Fälle erhalten; CSV-Labels und ARI/NMI separat nachgerechnet.
- `scripts/uv.cmd run --offline --locked python scripts/check_exercise_12_1_html.py`:
  offline 900/1400 px, vier geladene Bilder, keine Seitenfehler oder Überläufe.
- Alle vier PNGs visuell kontrolliert: Achsen/Einheiten, Rohbeispiele,
  transformierte Mitglieder/geschätzte Zentren, beschriftete Kreuztabellen und MSM-Matrix.
- Zweiter vollständiger Fit im frischen Notebook liefert dieselben ARI/NMI-Werte
  wie die erste Ausführung (Vergleichstoleranz 1e-9); keine Zeitidentität behauptet.
- Beide Rohdatei-SHA256 und 16 Artefakthashes geprüft. Alle acht Kapitel-10/11-ZIPs
  mit SHA256/CRC und alle Kapitel-11-Archivmitglieder mit SHA256 erneut geprüft.
  Frühere wissenschaftliche Dateien unverändert.

Tatsächliche Ergebnisse (TRAIN / TEST):
- Euklidisches k-Means: ARI 0,545136 / 0,489671; NMI 0,669094 / 0,592963.
- KASBA/MSM: ARI 0,815324 / 0,948216; NMI 0,882120 / 0,954753.
- Je sechs belegte Cluster, 10 bzw. 6 Iterationen (unter Limit 30).
- Originale Längen: TRAIN 115–455, TEST 100–375. Keine fehlenden Werte.
- MSM-Beispiel (1,1,3) gegen (1,3): Distanz 1, unabhängig mit aeon bestätigt.

Umgebung: aeon 1.6.0, NumPy 2.3.5, SciPy 1.17.1, scikit-learn 1.9.1,
Numba 0.63.1. Die notwendigen NumPy-/SciPy-Anpassungen werden nicht auf die
versiegelten Kapitel-11-Pakete übertragen; deren ursprünglicher Lockfile bleibt erhalten.
Warnungen: lokale unverschlüsselte Jupyter-TCP-Kommunikation; erster Numba-JIT-Lauf
meldete uint64→int64-Castwarnung bei der euklidischen Distanz. Keine fehlgeschlagenen
numerischen Tests. uv meldete einmal einen temporären Cache-Rename-Retry, danach
Installation erfolgreich. Keine zusätzlichen studentischen Tests behauptet.
