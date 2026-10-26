# Aufgabe 10.3 – Anforderungen und Akzeptanzkriterien

Quelle: [Exercise 10.3, offizielle Session 1](https://noxthot.github.io/ws26_industrial_datascience_manuscript/1_act1/6_self_study_session1.html), vollständig gelesen am 26.10.2026.

| Teil | Akzeptanzkriterium |
|---|---|
| Daten | Validiertes AI4I aus 10.2; drei Messgrößen Torque, Rotational speed, Air temperature; UDI ausschließlich als Kennung für die Linie |
| Linie | Seaborn-Linie Torque über UDI, keine unbemerkte Aggregation |
| Histogramme | Je ein Histogramm aller drei Messgrößen |
| Boxplots | Je ein Boxplot aller drei Messgrößen; Streuung und auffällige Werte erläutert |
| Violinplots | Je ein Violinplot; Unterschiede zu Boxplots diskutiert |
| Scatter | `sns.scatterplot`: Torque gegen Rotational speed, Air temperature als hue |
| Pairplot | `sns.pairplot` aller drei Messgrößen mit Diagonalverteilungen |
| Heatmap | `sns.heatmap` der Drei-Variablen-Korrelation; stärkstes Paar diskutiert |
| Jointplot | Torque gegen Air temperature mit Regressionsgerade |
| Strip/Swarm | Stripplot mit Torque und nach `pd.cut` gebinnter Rotational speed, farbig nach Bins |
| Countplot | Beobachtungszahlen in zehn Torque-Intervallen |
| Beobachtungen | Auffällige Werte, stärkste Beziehung, mögliche Nichtlinearität und Verteilungsformen anhand tatsächlicher Ergebnisse diskutieren |
| Verständlichkeit | Titel, Einheiten, Achsen und erforderliche Legenden; kurze deutsche Markdown-Erläuterungen |
| Reproduktion | Alle Zeilen, unveränderte Rohdaten, definierte Bins/Seed, sauberer Kernel, echte Bildausgaben und Prüfergebnisse |
| Export | HTML mit allen zehn Figurengruppen. 10.3 selbst fordert keinen PDF-Export; daher kein zusätzlicher PDF-Auftrag und keine 10.4-Quarto-Arbeit |

## Geplanter Ablauf und Wiederverwendung

`load_ai4i()` aus `sessions/ch10/ai4i_data.py` prüft SHA256, Spalten, Anzahl,
UDI-Sequenz und fehlende Werte. Pandas/Matplotlib/Jupyter und der Downloader sind
vorhanden. Seaborn und SciPy für KDE/Regression werden zur uv-Konfiguration ergänzt.
Das neue Notebook heißt `sessions/ch10/ai4i_seaborn.ipynb`.
Die drei Histogramme/Boxplots/Violinplots werden jeweils als eine Figur mit drei
Teilachsen dargestellt; dies erfüllt alle Einzelvariablen-Anforderungen.

Keine Zeilen werden entfernt oder gesampelt. Gleiche Breite für drei Speed-Bins
und zehn Torque-Bins; Grenzen und Häufigkeiten werden ausgegeben. Ein fester Seed
reproduziert Stripplot-Jitter. Pearson und ergänzend Spearman werden berechnet;
IQR-Markierungen sind Heuristiken und keine nachgewiesenen Messfehler. Regression
ist rein deskriptiv, ohne ungeprüfte Unabhängigkeits-/Kausalitätsannahme.

UDI ist kein Zeitstempel, die Daten sind synthetisch, KDE/Bins beeinflussen den
visuellen Eindruck, dichte Punktwolken überlagern sich. Keine Kausalitätsaussagen.
Der aktuelle Auftrag autorisiert den Plan und die technische Umsetzung. Keine
studentische Freigabe von 10.3, kein Merge, keine Abgabe und kein Beginn von 10.4.
