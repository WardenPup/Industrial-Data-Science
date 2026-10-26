# Industrial Data Science

Self-Study Exercises – Chapters 10–12

Wintersemester 2026/27

**Studentischer Autor:** Nicolas Jacobs  
**Hochschule:** MCI  
**Erstellt:** 27.10.2026 (Europe/Berlin)

Zwölf wissenschaftlich freigegebene und in main integrierte Lösungen. Die hier
ergänzten Abgabeversionen erhalten keine erfundene neue studentische Paketfreigabe.
Gesamtstatus bis zu dieser organisatorischen Abschlussentscheidung:
**SUBMISSION PREPARATION INCOMPLETE**. Technische Ergebnisse stehen in der
[Checkliste](SUBMISSION_CHECKLIST.md). Keine automatische Hochschuleinreichung.

| Kapitel | Exercise | Thema | ZIP-Datei | Zentrale Ergebnisdatei im entpackten ZIP | Freigabestatus |
|---|---|---|---|---|---|
| 10 | 10.1 | Isolierte Umgebung und Herzkurve | [Industrial_Data_Science_Exercise_10_1.zip](chapter_10/Industrial_Data_Science_Exercise_10_1.zip) | `exercise_10_1/sessions/ch10/aufgabe_10_1.md` | Lösung APPROVED/in main; neue Paketfassung PENDING |
| 10 | 10.2 | Jupyter und AI4I-Grundstatistik | [Industrial_Data_Science_Exercise_10_2.zip](chapter_10/Industrial_Data_Science_Exercise_10_2.zip) | `exercise_10_2/outputs/ch10/exercise_10_2/ai4i_explore.html` | Lösung APPROVED/in main; neue Paketfassung PENDING |
| 10 | 10.3 | Explorative Analyse mit Seaborn | [Industrial_Data_Science_Exercise_10_3.zip](chapter_10/Industrial_Data_Science_Exercise_10_3.zip) | `exercise_10_3/outputs/ch10/exercise_10_3/ai4i_seaborn.html` | Lösung APPROVED/in main; neue Paketfassung PENDING |
| 10 | 10.4 | Wissenschaftlicher Bericht mit Quarto | [Industrial_Data_Science_Exercise_10_4.zip](chapter_10/Industrial_Data_Science_Exercise_10_4.zip) | `exercise_10_4/outputs/ch10/exercise_10_4/paper.html` | Lösung APPROVED/in main; neue Paketfassung PENDING |
| 11 | 11.1 | Rollende Glättung mit erhaltener Lückenmaske | [Industrial_Data_Science_Exercise_11_1.zip](chapter_11/Industrial_Data_Science_Exercise_11_1.zip) | `outputs/ch11/exercise_11_1/production_smoothing.html` | Lösung APPROVED/in main; neue Paketfassung PENDING |
| 11 | 11.2 | Vergleich von sechs Imputationsmethoden | [Industrial_Data_Science_Exercise_11_2.zip](chapter_11/Industrial_Data_Science_Exercise_11_2.zip) | `outputs/ch11/exercise_11_2/production_imputation.html` | Lösung APPROVED/in main; neue Paketfassung PENDING |
| 11 | 11.3 | Zweistufige STL-Imputation | [Industrial_Data_Science_Exercise_11_3.zip](chapter_11/Industrial_Data_Science_Exercise_11_3.zip) | `outputs/ch11/exercise_11_3/production_stl_imputation.html` | Lösung APPROVED/in main; neue Paketfassung PENDING |
| 11 | 11.4 | STL-basierte Ausreißerkandidaten | [Industrial_Data_Science_Exercise_11_4.zip](chapter_11/Industrial_Data_Science_Exercise_11_4.zip) | `outputs/ch11/exercise_11_4/production_outliers.html` | Lösung APPROVED/in main; neue Paketfassung PENDING |
| 12 | 12.1 | Zeitreihen-Clustering: k-Means und KASBA | [Industrial_Data_Science_Exercise_12_1.zip](chapter_12/Industrial_Data_Science_Exercise_12_1.zip) | `outputs/ch12/exercise_12_1/gesture_clustering.html` | Lösung APPROVED/in main; neue Paketfassung PENDING |
| 12 | 12.2 | Gestenklassifikation: DTW-3-NN und CNN | [Industrial_Data_Science_Exercise_12_2.zip](chapter_12/Industrial_Data_Science_Exercise_12_2.zip) | `outputs/ch12/exercise_12_2/uwave_classification.html` | Lösung APPROVED/in main; neue Paketfassung PENDING |
| 12 | 12.3 | Gestenklassifikation mit Time Series Forest | [Industrial_Data_Science_Exercise_12_3.zip](chapter_12/Industrial_Data_Science_Exercise_12_3.zip) | `outputs/ch12/exercise_12_3/uwave_forest.html` | Lösung APPROVED/in main; neue Paketfassung PENDING |
| 12 | 12.4 | Multivariate Energieregression | [Industrial_Data_Science_Exercise_12_4.zip](chapter_12/Industrial_Data_Science_Exercise_12_4.zip) | `outputs/ch12/exercise_12_4/appliances_regression.html` | Lösung APPROVED/in main; neue Paketfassung PENDING |

## Lesen und Ausführen

1. Das ZIP der betreffenden Exercise vollständig in einen eigenen Ordner entpacken.
2. START_HERE.md im Archivstamm öffnen; dort sind Lesedatei, HTML und Befehle genannt.
3. HTML direkt im Browser lesen; dafür wird kein Python benötigt. 10.1 hat stattdessen
   eine Herleitung und eine PNG-Herzkurve. 10.2 und 10.4 enthalten außerdem die geforderten PDFs.
4. Das Notebook in VS Code oder Jupyter öffnen und die beschriebene Python-Umgebung wählen.
5. Im angegebenen Paketstamm `uv sync --locked` ausführen. Die Erstinstallation
   benötigt uv, Python und Netzwerkzugang. Danach den in START_HERE genannten Builder starten.
6. Abbildungen und Tabellen liegen unter outputs/, Kapitel-11-Ableitungen zusätzlich
   unter data/processed/. Die Pakete enthalten erforderliche lokale Daten und Quellmodule.

Die Tabelle verlinkt die realen ZIP-Dateien relativ; innere Dateipfade werden nach
dem Entpacken verwendet. Markdown kann keine Datei innerhalb eines ZIPs öffnen.

## Nachvollziehbarkeit

- [Autorenschaft und KI](AUTHORSHIP_AND_AI.md)
- [Anforderungen, Quellen und Umgebung](requirements_and_sources.md)
- [Endprüfung und manuelle Uploadkontrolle](SUBMISSION_CHECKLIST.md)
- [Zwölf SHA256-Prüfsummen](SHA256SUMS.txt)
- [Paketinhalt und Einzeldateihashes](package_manifest.json)
- [Tatsächliche PR-Integration und Head-CI](github_integration_audit.json)
- [Einreichungsnachweis zum späteren Ausfüllen](SUBMISSION_RECEIPT_TEMPLATE.md)

Die Übungen behandeln Visualisierung/Berichte, Glättung/Imputation/Ausreißer sowie
Zeitreihen-Clustering, Klassifikation und Regression. Ergebnisse und wissenschaftliche
Grenzen werden in den jeweiligen Lösungen erläutert. Es wurden keine neuen
wissenschaftlichen Experimente für die Abgabe begonnen.

## Herkunft der Abgabeversionen

Die acht ursprünglichen Kapitel-10/11-ZIPs bleiben unverändert unter den bisherigen
submission/chapter_10- bzw. submission/chapter_11-Ordnern des Projekts erhalten.
Diese finalen Fassungen ergänzen ausschließlich START_HERE.md, AUTHORSHIP_AND_AI.md
und PACKAGE_CONTENTS.json; jedes bisherige Archivmitglied bleibt bytegleich.
Die neuen Kapitel-12-ZIPs enthalten freigegebene wissenschaftliche Dateien und
die für eigenständige Reproduktion erforderlichen Daten/Module/Referenzdateien.

Zwei Quellen-Metadaten benötigen die im bestehenden Manifest erwarteten CRLF-Bytes:
12.3 forest_reference.json ausschließlich in der Paketkopie, 12.4 appliances_source.json
zusätzlich als technischer Folgecommit 7eb767f auf dem Vorbereitungsbranch.
JSON-Werte, Rohdaten und wissenschaftliche Ergebnisse ändern sich dadurch nicht.
Die ursprünglichen Reviews bleiben unverändert. Details stehen im Paketmanifest.

ZIPs bleiben wie die bisherigen Abgabepakete lokal und Git-ignoriert. GitHub enthält
Paketierer, Dateilisten, Prüfsummen und Prüfbericht; es erfolgt keine neue öffentliche
Rohdatenveröffentlichung. Die tatsächlichen Uploaddateien sind genau die zwölf ZIPs
in chapter_10/, chapter_11/ und chapter_12/, nicht der gesamte Projektordner.

Die ergänzte Paketfassung und konkrete Lehrveranstaltungs-/KI-/Datenweitergaberegeln
sind vor dem Upload studentisch zu bestätigen. Diese organisatorische Prüfung
ändert die dokumentierten wissenschaftlichen Freigaben nicht.
