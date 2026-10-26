# Aufgabe 12.1 – Anforderungen und Abnahme

KI-gestützte Analyse, Quellen tatsächlich gelesen am 26.10.2026:
- https://noxthot.github.io/ws26_industrial_datascience_manuscript/1_act1/8_self_study_session3.html
- https://www.timeseriesclassification.com/description.php?Dataset=GesturePebbleZ1
- https://www.aeon-toolkit.org/en/stable/api_reference/auto_generated/aeon.clustering.TimeSeriesKMeans.html
- https://www.aeon-toolkit.org/en/stable/api_reference/auto_generated/aeon.clustering.KASBA.html
- https://www.aeon-toolkit.org/en/stable/api_reference/auto_generated/aeon.distances.msm_distance.html
- Holder/Bagnall: https://arxiv.org/abs/2411.17838, publizierte Fassung DOI 10.1007/s10618-026-01189-9.

## Offizielle Pflichten und Lernziele
GesturePebbleZ1 laden (variabel lange univariate Reihen, geeignete Listenstruktur),
visuell explorieren und für die Algorithmen formatieren. Zeitreihen-k-Means und
KASBA anwenden; nützliche Grafiken erstellen und Ergebnisse vergleichen. Erklären,
wie KASBA sich von gewöhnlichem k-Means unterscheidet und MSM berechnet wird.
Die sktime-Ladefunktion ist ein optionales Beispiel, keine Bibliothekspflicht.

## Konkrete Umsetzung und Modellannahmen
Originale UCR/UEA-Train-/Testdateien unverändert unter data/raw, Quelle und SHA256
festhalten. aeon-Loader liefert variabel lange Reihen als Liste von (1,L)-Arrays.
Train/Test-Sessions getrennt halten; Modelle ausschließlich auf TRAIN fitten.
Lineare Interpolation auf 128 relative Zeitpositionen für beide Algorithmen,
anschließend jede Reihe separat z-normalisieren (ddof=0). Ursprüngliche Längen
und Rohverläufe zeigen; keine Nullauffüllung und keine Änderung der Quelldateien.
Diese Umsetzung ist eine dokumentierte Wahl, keine offizielle optimale Länge.

Gleiche Darstellung (n,1,128), Seed 42, k=6 als bekannter Benchmark-Klassenumfang,
keine Optimierung anhand Testlabels. Baseline: aeon TimeSeriesKMeans mit euklidischer
Distanz, arithmetischem Mittel und drei Initialisierungen; KASBA mit MSM(c=1),
metrischer Zuordnungsbeschleunigung und stochastischen elastischen Baryzentren.
Beide maximal 30 Iterationen; tatsächliche Konvergenz/Iteration berichten.
Labels nur nachträglich für ARI/NMI und Kreuztabellen, nicht als Clustering-Input.
Train- und Test-ARI/NMI getrennt, Clustergrößen und Laufzeiten berichten;
Laufzeit enthält ggf. Numba-JIT, keine allgemeine Geschwindigkeitsbehauptung.
MSM mit kleinem unabhängig nachgerechneten Dynamikprogramm illustrieren und
gegen aeon prüfen, inklusive Move-/Split-/Merge-Kosten und Randinitialisierung.

## Abnahmekriterien und Ausgaben
Vollständige beide Splits, endliche Werte, Längenverteilung und Beispielgrafiken;
keine labels im Fit. Notwendige Formatanpassung ausdrücklich beantworten.
Vergleichstabelle, Clusterzentren mit Mitgliedern und Klassen/Cluster-Kreuztabellen;
MSM-Beispielmatrix. Reproduzierbarer Seed, Rohdatenchecksummen, frischer
Notebook-Kernel, sinnvolle Tests und visuelle Prüfung aller Grafiken.
Notebook plus eigenständiger Offline-HTML-Export (Projekt-Abgaberegel), CSV/JSON
für Zahlen und Zuordnungen, keine PDF-Pflicht. Kein Upload/Abgabepaket für 12.1.

## Grenzen und Human Review
Resampling entfernt Dauerinformation und kann Details glätten; Normalisierung
entfernt absolutes Niveau und Amplitude. Unbekannte Zeiteinheit der Abtastwerte
nicht erfinden. Klassenlabels sind ein externer Vergleich, keine zwingend wahren
Cluster. Ein Seed und k=6 belegen weder Stabilität noch globale Optimalität.
KASBA-Vergleich umfasst Distanz UND Optimierung; kein isolierter Beschleunigungstest.
Kein Prognose-/Kausalitätsanspruch. Testsplit nur einmal zur Auswertung verwenden.
Nach technischer Prüfung: AWAITING HUMAN REVIEW; keine menschliche Freigabe erfunden.
