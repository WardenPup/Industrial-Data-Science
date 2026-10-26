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


# Human Review – Exercise 12.1

**Datum:** 26.10.2026  
**Aufgabe:** GesturePebbleZ1 – Time Series Clustering  
**Status:** Fachlich positiv beurteilt, technische Abschlussprüfung ausstehend  
**KI-Unterstützung:** Codex (Implementierung und automatisierte Tests), ChatGPT (Unterstützung bei der Ergebnisinterpretation)

## 1. Daten und Vorverarbeitung

Die Datenexploration zeigt, dass die Gesten unterschiedlich lange Zeitreihen besitzen. Im Trainingsdatensatz reichen die Längen von 115 bis 455 Messwerten, im Testdatensatz von 100 bis 375.

Die Anpassung auf 128 Werte ist für den Methodenvergleich nachvollziehbar, da die Verfahren damit dieselbe Eingabedimension verwenden können.

Die z-Normalisierung halte ich ebenfalls für sinnvoll. Dadurch wird verhindert, dass unterschiedliche absolute Sensorwerte den Distanzvergleich dominieren.

Allerdings gehen bei der Längenanpassung Informationen über die ursprüngliche Dauer und möglicherweise kurze Bewegungsdetails verloren. Durch die Normalisierung werden außerdem absolute Amplitudenunterschiede entfernt. Beide Schritte können die Clusterbildung beeinflussen.

## 2. Wahl der Clusteranzahl

Die Wahl von k = 6 ist nachvollziehbar, da der Datensatz sechs bekannte Gestenklassen enthält.

Die Clusterbildung selbst erfolgt ohne Verwendung dieser Klassenlabels. Die Labels dienen anschließend zur externen Bewertung.

Damit untersuchen wir, wie gut die gefundenen Gruppen mit den bekannten Klassen übereinstimmen. Die Ergebnisse beweisen allerdings nicht, dass sechs Cluster auch unabhängig von den Labels die optimale Wahl darstellen.

## 3. Euklidisches k-Means

Die dargestellten Clusterzentren sind nachvollziehbar. Einige typische Signalformen werden erkannt, andere Klassen verteilen sich jedoch auf mehrere Cluster.

Besonders die Klassen 1, 4 und 5 werden teilweise vermischt. Das ist auch in den Heatmaps erkennbar.

Eine mögliche Erklärung ist, dass die euklidische Distanz die einzelnen Abtastpositionen direkt vergleicht und gegenüber zeitlich verschobenen Signalmerkmalen empfindlich ist.

Auf dem Testdatensatz erreicht das Verfahren:

- ARI = 0,489671
- NMI = 0,592963

Das Ergebnis zeigt eine erkennbare, aber keine eindeutige Übereinstimmung zwischen Clustern und Gestenklassen.

## 4. KASBA mit MSM

Bei KASBA fällt die deutlich klarere Trennung der Signalformen auf.

In den Clusterzentren sind mehrere charakteristische Gestenverläufe gut erkennbar. Auch die Heatmaps zeigen, dass die meisten Beobachtungen einer Klasse jeweils demselben Cluster zugeordnet werden.

Auf dem Testdatensatz erreicht KASBA:

- ARI = 0,948216
- NMI = 0,954753

Damit liefert KASBA in diesem Versuch eine wesentlich bessere Übereinstimmung mit den bekannten Klassen als das euklidische k-Means.

MSM berücksichtigt beim Distanzvergleich Änderungen der zeitlichen Zuordnung durch Move-, Split- und Merge-Operationen. Das ist bei unterschiedlich ausgeführten Gesten plausibel vorteilhaft.

Die höhere Clusterqualität gilt für diese konkrete Auswertung. Daraus lässt sich keine allgemeine Überlegenheit von KASBA für beliebige Zeitreihendaten ableiten.

## 5. MSM-Beispiel

Die kleine Kostenmatrix verdeutlicht den Grundgedanken der Move-Split-Merge-Distanz.

Das Zusammenführen zweier aufeinanderfolgender Einsen wird im Beispiel mit Kosten 1 dargestellt. Die kumulierten Kosten veranschaulichen, wie aus lokalen Operationen eine Gesamtdistanz entsteht.

Das Beispiel ist als didaktische Erklärung hilfreich. Für die technische Abschlussprüfung sollte noch bestätigt werden, dass die gesamte Matrix genau der verwendeten MSM-Rekurrenz und Kostenfunktion entspricht.

## 6. Vergleich und Aussagegrenzen

Die verwendeten ARI- und NMI-Werte eignen sich zur Bewertung der Clusterzuordnungen, weil die willkürliche Nummerierung der Cluster keinen Einfluss auf diese Kennzahlen hat.

Trotzdem bestehen Einschränkungen:

- Die Untersuchung verwendet nur einen dokumentierten Zufallsseed.
- Die Ergebnisse hängen von der gewählten Normalisierung, Resampling-Länge und Clusteranzahl ab.
- Die Untersuchung einer weiteren Initialisierung oder eines alternativen Seeds wäre für eine Robustheitsbewertung sinnvoll.
- Da beide Sessions dieselben Personen betreffen, ist der Testsplit nicht automatisch ein unabhängiger Nachweis der Übertragbarkeit auf neue Personen.

Außerdem fällt auf, dass KASBA im Testsplit bessere Werte als im Trainingssplit erreicht. Das ist nicht zwingend ein Fehler, sollte aber nicht als allgemeiner Vorteil auf ungesehenen Daten interpretiert werden.

## 7. Grafische Darstellung und Nachvollziehbarkeit

Alle vier Abbildungen sind lesbar und die Achsen weitgehend verständlich beschriftet.

Die ursprünglichen Signallängen, Clusterzentren und Klassen-Cluster-Häufigkeiten werden sinnvoll gegenübergestellt.

Die getrennte Darstellung von TRAIN und TEST unterstützt die Interpretation.

Die relativen Zeitachsen und die dimensionslosen normalisierten Sensorwerte sind nachvollziehbar.

Die Rohdaten und exportierten Kennzahlen sind für eine spätere Überprüfung dokumentiert.

## 8. Gesamturteil

Die Aufgabe ist fachlich nachvollziehbar umgesetzt. Die Ergebnisse zeigen anschaulich den Unterschied zwischen punktweisem euklidischem Distanzvergleich und dem elastischeren MSM-Ansatz.

Die deutlich höheren ARI- und NMI-Werte von KASBA stimmen mit der erkennbar klareren Clustertrennung in den Heatmaps überein.

Die wesentlichen wissenschaftlichen Grenzen sind bekannt und sollten in der endgültigen Dokumentation erhalten bleiben.

**Fachliches Urteil: Positiv.**

Ich sehe auf Grundlage der vorliegenden Ergebnisse keinen grundlegenden fachlichen Fehler. Vor der abschließenden Freigabe sollen die MSM-Rekurrenz, die Trennung von Training und Test sowie die dokumentierte technische Validierung noch einmal geprüft werden.

**Finale Merge-Freigabe: PENDING.**

Dieser Review dokumentiert die fachliche Beurteilung der vorliegenden Ergebnisse. Er ersetzt keine unabhängige Neuausführung des Codes.
