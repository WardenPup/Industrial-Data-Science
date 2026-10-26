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
Wird nach tatsächlichen Prüfläufen ergänzt. Keine studentischen Tests behauptet.
