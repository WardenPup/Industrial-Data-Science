# Kapitel 12 – Prioritätsplan

KI-gestützte Analyse am 26.10.2026. Exakte offizielle Quelle:
https://noxthot.github.io/ws26_industrial_datascience_manuscript/1_act1/8_self_study_session3.html
Deadline laut Auftrag: 27.10.2026, 23:59 Europe/Berlin.

| Reihenfolge | Pflicht und Daten | Aufwandsschätzung, keine Zeitgarantie |
|---|---|---|
| 12.1 jetzt | GesturePebbleZ1 (univariat, variabel lang); visuelle Exploration, Zeitreihen-k-Means und KASBA vergleichen; KASBA-Unterschied und MSM-Rechnung erklären | 2–4 h einschließlich Abhängigkeiten, Tests und Export |
| 12.2 nach gesondertem Auftrag | UWaveGestureLibrary multivariat; Zeitreihen-kNN und CNN-Klassifikation vergleichen | 3–5 h, Trainingslaufzeit hardwareabhängig |
| 12.3 danach | Derselbe Datensatz; aeon TimeSeriesForestClassifier, Vergleich mit 12.2 | 1–2 h |
| 12.4 zuletzt | AppliancesEnergy; Zeitreihen-kNN, Random-Forest-Tree-Regressor und CNN-Regressor vergleichen | 3–5 h, Trainingslaufzeit hardwareabhängig |

Nur 12.1 ist zur Umsetzung autorisiert. 12.2–12.4 werden hier ausschließlich
analysiert. Keine Trainings- oder Downloadläufe dafür. 12.3 hängt inhaltlich vom
Vergleich aus 12.2 ab; 12.4 kann Daten-/Metrikgrundlagen wiederverwenden, erfordert
aber eigenes Regressionsreview. Je Aufgabe Notebook plus HTML und relevante
Abhängigkeiten/Datenquellen; keine PDF-Pflicht auf der offiziellen Seite.

Priorität: Pflichtmethoden, korrekte Formate/Splits, echte Vergleichsmetriken,
reproduzierbare Seeds und verständliche Darstellung. Keine zusätzlichen Modelle
oder Hyperparameterstudien vor Erfüllung der Pflicht. Human Review nach jeder
technischen Validierung; keine automatische Freigabe, Zusammenführung oder Abgabe.

12.1: Beide aeon-Clusterer benötigen laut API gleich lange Reihen. Gemeinsame
lineare Resampling-Darstellung und dokumentierte Normalisierung ermöglichen den
Vergleich; ursprüngliche Längen erhalten und Informationsverlust diskutieren.
Klassenlabels dienen nur nachträglichen externen Clustermetriken; keine Anpassung
an Testlabels. Originalsplits nicht vermischen. KASBA nutzt MSM als Metrik,
elastische stochastische Baryzentren und beschleunigte Zuordnung; keine pauschale
Geschwindigkeits-/Qualitätsbehauptung aus einem Einzellauf.

Umgebungsrisiko: aeon 1.6 verlangt numpy<2.5 und scipy<1.18. Vor einer nötigen
Umgebungsänderung werden Kapitel-11-Pakete mit dem bisherigen uv.lock versiegelt.
Die neue projektlokale Umgebung muss danach sämtliche Regressionstests bestehen;
frühere wissenschaftliche Artefakte und Abgabepakete bleiben unverändert.
