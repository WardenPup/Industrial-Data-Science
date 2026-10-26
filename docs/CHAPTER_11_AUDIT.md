# Kapitel 11 – Vollständigkeitsprüfung, 26.10.2026

KI-gestützte Prüfung der tatsächlich gelesenen offiziellen Kursseiten:
- Der im Auftrag angegebene Link `1_act1/6_self_study_session1.html` bezeichnet Kapitel 10.
- Kapitel 11: https://noxthot.github.io/ws26_industrial_datascience_manuscript/1_act1/7_self_study_session2.html

Die offizielle Seite endet nach 11.4; keine Aufgabe 11.5 vorhanden.

| Aufgabe | Offizielle Pflicht | Vorhandener Nachweis |
|---|---|---|
| 11.1 | Rohdaten laden, beide Reihen mit Kursfunktion darstellen; rollende Glättung mit begründeter Mean/Median-Wahl, gleiche Lücken, Seaborn | production_smoothing.ipynb, zwei Grafiken, zentrierter Fünfwochenmedian und Mittelwertvergleich, unveränderte 367er-Maske |
| 11.2 | Geglättete Reihe mit mehreren Methoden imputieren, Kursdarstellung, Diskussion | production_imputation.ipynb, sechs Methoden, sieben Grafiken, 367 gefüllte/677 erhaltene Werte, Langlücken-/Overshootdiskussion |
| 11.3 | Vorimputation, STL, Komponenten mit Kursfunktion, ursprüngliche Lückenreihe entsaisonalisieren, erneut imputieren und resaisonalisieren, Kursdarstellung/Diskussion | production_stl_imputation.ipynb, vier Grafiken, zwei Stufen, gleiche Maske und erhaltene Beobachtungen |
| 11.4 | Vollständiges pieces, geeignete Erkennung, Seaborn, Anzahl und Diskussion | production_outliers.ipynb, zwei Grafiken, 26 residualbasierte Kandidaten und explizite Grenzen |

Alle vier Reviewdateien enthalten tatsächliche studentische fachliche Freigaben vom
26.10.2026. Frühere ausstehende Mergehinweise bleiben historische Aufzeichnungen.
Reguläre Integration: PR #5 b7543e048a4aafac7fa2ad5ba4d18c46e72d2f68,
PR #6 84085f5fa4387a833aa13ba20ce29d0930ff4359,
PR #7 a294bc572415c585d9dc699cb17eb4de994a8111,
PR #8 d117c40d303a2b2d9c47c8bd2a15ff1d8a3d1f3c.

PR #8: aktueller Head f1f6f5d einschließlich eda8ed0/eb73b17; tatsächliche
Head-Checks erfolgreich, kein Konflikt, Ready vor Merge. Studentischer Text
gegen eda8ed0 exakt geprüft (Git-Zeilenenden normalisiert); f1f6f5d verändert
keine wissenschaftlichen Dateien, sondern nur Testtoleranz und Dokumentation.
Alle wissenschaftlichen Dateien im Merge entsprechen dem freigegebenen Head.
Auf synchronisiertem main: 40 Tests erfolgreich in 2,827 s.

Kapitel 11 ist fachlich freigegeben und integriert. Keine offenen Pflichtaufgaben
gefunden. Abgabevorbereitung folgt den ausdrücklich mitgeteilten Regeln: ein ZIP
pro Aufgabe, Notebook plus HTML, relevante Daten/Quellen/Module/Umgebung und
Reproduktionsanleitung; PDF nicht gefordert. Keine Einreichung erfolgt.
