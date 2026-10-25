# Aufgabe 10.2 – Anforderungen und Vorgehen

Quelle: [offizielle Session 1, Exercise 10.2](https://noxthot.github.io/ws26_industrial_datascience_manuscript/1_act1/6_self_study_session1.html), abgerufen 26.10.2026.

| Anforderung | Akzeptanzkriterium |
|---|---|
| Jupyter aus der uv-Umgebung verwenden | JupyterLab/Notebook und ipykernel vorhanden; Notebook in frischem Projektkernel ausführbar |
| `ai4i_explore.ipynb` erstellen | Datei unter `sessions/ch10/`, strukturierte deutsche Erläuterungen |
| AI4I in einen pandas DataFrame laden | Offizielles UCI-CSV, Quelle/Lizenz/Prüfsumme dokumentiert |
| Nur UDI, Torque, Rotational speed, Air temperature behalten | Exakt vier Spalten, Originalnamen mit Einheiten; keine Zielvariablen in der Analyse |
| Erste zehn Zeilen und Grundstatistik | `head(10)` und `describe()` sichtbar im ausgeführten Notebook und in Exporten |
| Liniendiagramm Torque über UDI | Matplotlib, UDI auf x, Drehmoment mit Nm auf y; Grafik gespeichert |
| Zelltypen erproben | Code, Markdown und Raw tatsächlich vorhanden und erläutert |
| HTML und PDF exportieren | Ausgeführtes Notebook, eigenständiges HTML mit eingebetteter Grafik und lesbares PDF |
| Nachvollziehbarkeit | Datenvalidierung, sequentielle Kernel-Ausführung, echte Prüfergebnisse und offene Human-Review-Fragen |

## Datenquelle und methodische Grenzen

[UCI AI4I 2020 Predictive Maintenance Dataset](https://archive.ics.uci.edu/dataset/601/ai4i+2020+predictive+maintenance+dataset),
DOI 10.24432/C5HS5C, CC BY 4.0. UCI beschreibt 10.000 synthetische Datensätze.
UDI ist eine eindeutige Zeilenkennung, kein Zeitstempel. Die Darstellung nach UDI
begründet keine zeitliche Dynamik oder Kausalität. Daten werden nicht imputiert,
normalisiert oder modelliert. Keine Inhalte aus 10.3 werden vorweggenommen.

## Wiederverwendung und autorisierter Plan

Vorhanden: Python 3.12.15, uv-Lockdatei, NumPy/Matplotlib, JupyterLab/Notebook,
ipykernel, nbformat/nbclient und nbconvert mit Chromium-WebPDF. Ergänzung: pandas.
Vorhandene QA-Skripte, Git-Konventionen und Review-Vorlage werden weiterverwendet.
Rohdaten bleiben Git-ignoriert; ein Downloadskript verifiziert die feste Prüfsumme.
CI lädt dieselbe Quelle vor Tests/Notebookausführung.

Der aktuelle Nutzerauftrag autorisiert Analyse, Implementierung, automatisierte
Prüfung, Exporte, Commits, Push und Draft-PR. Keine zusätzliche Planfreigabe nötig.
Die studentische Prüfung und ausdrückliche Freigabe von 10.2 wurden anschließend
am 26.10.2026 bestätigt. Merge-Erlaubnis steht weiterhin aus. Keine Abgabe oder Merge.

## Einreichung

Die Aufgabe fordert Notebook-Exporte; ein konkretes Kursportalformat oder Termin
ist hier nicht festgelegt. Es erfolgt keine automatische Einreichung.
