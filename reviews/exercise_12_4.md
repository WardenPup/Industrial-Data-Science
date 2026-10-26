# Aufgabe 12.4 – Human-AI Review

Status: AWAITING HUMAN REVIEW. Kein studentischer Review oder Approval vorliegend.
Technischer Bericht von Codex, 26.10.2026. Kein Merge und keine Einreichung autorisiert.

## Umsetzung und KI-Beitrag
Codex las die offizielle Exercise 12.4, Kurskapitel 9 und Primärquellen zur
Benchmarkfassung. Anforderungen/Konfiguration vor Modelltraining in 4e0f381
festgelegt; KI-gestützte Implementierung 1fb8196. Drei verlangte Regressoren:
DTW-3-NN, aeon TimeSeriesForestRegressor, eigener kompakter PyTorch-CPU-CNN-Regressor.
Kein weiteres Modell und keine Hyperparameterstudie. Bisherige Umgebung unverändert.
95 TRAIN/42 TEST, 24 Kanäle × 144 Werte, unveränderte gehashte Originalsplits.
Nur TRAIN bestimmt Kanalskalierung und CNN-Zielstandardisierung. Keine TEST-Werte
in Fit/Optimierung, keine Neuaufteilung/Imputation/Resampling. CNN-Ausgabe vor
Bewertung rücktransformiert. Benchmark-Split nicht als chronologischer Test behauptet.

## Tatsächliche Ergebnisse (kWh)
| Methode | TEST-RMSE | TEST-MAE |
|---|---:|---:|
| DTW-3-NN | 3,5092246163 | 2,7113492063 |
| Time Series Forest | 2,1091826331 | 1,6852535714 |
| CNN | 3,6146750395 | 2,6080539167 |

Forest auf diesem festen Split bei beiden Maßen niedrigster Fehler. kNN liegt
beim RMSE vor CNN, beim MAE dahinter. Keine allgemeine/signifikante Überlegenheit.
Alle drei Modelle haben null negative Vorhersagen; kein nachträgliches Abschneiden.
CNN: 5.553 Parameter, 60 feste Epochen, Seed 42, Adam 0,001, Batch 16, MSE;
lineare skalare Ausgabe. Forest 200 squared_error-Bäume, 58 Intervallziehungen/Baum,
Mindestlänge 3. kNN uniformes Mittel dreier DTW-Nachbarn, window=0,1.
Diese Ausgangskonfigurationen sind Annahmen, keine durch Tuning belegten Optima.

Ziel laut ursprünglicher TSER-Beschreibung Gesamtenergie in kWh; neue aeon-Dateien
enthalten 137 Fälle, alte Beschreibung nennt 138. UCI-Ursprung mit Wh-Zielen/19.735
Einzelzeilen nicht als identische Darstellung ausgegeben oder nochmals umgerechnet.
Quelle/Lizenz und Grenzen ausführlich in docs/APPLIANCES_SOURCE.md dokumentiert.

## Tatsächlich ausgeführte Prüfungen
Alle Befehle vom Projektstamm über `scripts/uv.cmd run --offline --locked`:
- `python -m unittest discover -s tests -q`: zuletzt 64 Tests bestanden, 6,921 s
  (erster Lauf 7,723 s). Sieben neue Tests für Rohdaten/Formen, instrumentierte
  TRAIN-only-Fit-Grenze, bekannten kNN-Nachbarmittelwert, Forest-Baumaggregation,
  CNN-Seed/echte Gewichtsänderung/lineare Ausgabe/Zielrücktransformation,
  Handrechnung der Metriken und ungültige Daten.
- `python scripts/build_exercise_12_4.py`: frischer Kernel, drei Codezellen sequenziell,
  zwei eingebettete PNGs dekodiert. RMSE/MAE aller Modelle unabhängig mit NumPy
  auf ursprünglichen TEST-Zielen nachgerechnet. Zweiter vollständiger Fit reproduziert
  alle 126 TEST-Vorhersagen innerhalb atol/rtol 1e-10 und alle 60 Verlustwerte.
  Tatsächlicher Skalierer-Aufruf genau einmal mit TRAIN instrumentiert; TRAIN-Kanal-
  und Zielstatistiken separat nachgerechnet. Für alle 42 Fälle kNN-Zielmittel aus
  drei Nachbarindizes und Forest-Mittel aus allen 200 Einzelbäumen überprüft.
  Gespeicherte CNN-NPZ-Gewichte mit allow_pickle=False geladen; alle Vorhersagen
  inklusive Zielrücktransformation bestätigt. Keine Testlabels an predict übergeben.
- `python scripts/check_exercise_12_4_html.py`: HTML offline bei 900/1400 px, zwei
  Bilder geladen, keine Seitenfehler und kein horizontaler Überlauf.
- Beide finalen PNGs visuell geprüft. Achsen/Einheiten/Legenden/Identitätsgeraden
  vollständig, gemeinsame Skalen in allen drei Ist-Vorhersage-Panels. Bildgrenzen
  nach erster Sichtprüfung mit bbox_inches='tight' korrigiert, danach vollständiger
  frischer Build und Offline-Prüfung wiederholt. Keine Ergebnisänderung.
- Beide Originaldateien bei Erstbezug gegen Zenodo-MD5 und bei allen Analyse-Ladevorgängen
  gegen SHA256 geprüft. Elf aktuelle Artefakthashes im Manifest separat bestätigt.
- Frühere wissenschaftliche Dateien, alle bisherigen Reviews und pyproject.toml/
  uv.lock unverändert gegenüber Merge 2e33047; alle acht Kapitel-10/11-ZIPs per
  SHA256 und CRC bestätigt. Keine Rohdaten, Umgebungen oder Binärwerkzeuge committed.

Notebook-Fit-Zeiten: {'DTW 3-NN': 0.027182099991478026, 'Time Series Forest': 7.258757299990975, 'CNN': 4.037345999997342}; Predict: {'DTW 3-NN': 1.030393599998206, 'Time Series Forest': 0.8431469999923138, 'CNN': 0.0030488000047625974} Sekunden.
Separater Audit-Fit: {'DTW 3-NN': 0.027392399992095307, 'Time Series Forest': 9.770668899989687, 'CNN': 4.320078700009617}; Predict: {'DTW 3-NN': 0.9938288999983342, 'Time Series Forest': 0.7240472999983467, 'CNN': 0.005634800007101148} Sekunden.
Zeiten sind Hardware-/Cache-/JIT-abhängig, kein allgemeiner Laufzeitvergleich.
Beobachtet: Jupyter-Warnung zu unverschlüsseltem lokalem TCP-Transport. Keine
fehlgeschlagenen numerischen Tests oder Notebook-/Offline-HTML-Prüfungen.
Aktuelle GitHub-Actions-Läufe werden nach Push tatsächlich im Draft PR dokumentiert;
vor deren Abschluss kein CI-Erfolg behauptet.

## Grenzen und konkrete Fragen für den studentischen Review
Nur 95 Trainingsfälle, ein Seed und vorgegebener Split. Kein unabhängiges
Validierungsset, keine Seed-/Hyperparameterstudie oder Signifikanzprüfung.
Trainingsverlust belegt weder Generalisierung noch allein Overfitting. Schätzung
mit vollständigem Sensorfenster ist keine validierte zukünftige Prognose. Ein Haus
und unbekannte zeitliche Split-Zuordnung begrenzen die Übertragbarkeit; keine Kausalität.

1. Sind TRAIN-only-Kanal- und Zielskalierung sowie die Rücktransformation nachvollziehbar?
2. Sind kNN-Zielmittel, Intervall-Forest und die lineare CNN-Ausgabe verständlich erklärt?
3. Ist die unterschiedliche kNN-/CNN-Reihenfolge für RMSE und MAE sachlich eingeordnet?
4. Sind beide Grafiken lesbar und die kWh-Zielgröße samt 137/138-Quellenabweichung transparent?
5. Sind kleiner Datensatz, ein Seed, fehlende Validierung und keine Zukunftsprognose klar genug?

Studentisches Feedback und Freigabe stehen aus. Status AWAITING HUMAN REVIEW.
Keine weitere Aufgabe beginnen, keine automatische Freigabe/kein Merge/kein Upload.

## KI-Nachtrag – tatsächliche plattformübergreifende CI-Beobachtung

Der erste PR-CI-Lauf 40411236019 am Head 3f2eb74 bestand vollständig. Im tatsächlichen
Linux-Protokoll: DTW RMSE/MAE 3,509225/2,711349, Forest 2,109183/1,685254,
CNN 3,625036/2,613754 kWh. Lokal Windows: CNN 3,614675/2,608054 kWh.
Die jeweils zweite vollständige Ausführung auf derselben Plattform bestand die
Vorhersage-/Verlustvergleichstoleranz 1e-10. Plattformübergreifende numerische
Identität ist damit nicht belegt; identischer Seed allein garantiert sie nicht.
Die Ursache der konkreten Differenz wurde nicht isoliert nachgewiesen. Keine
Parameter oder Modellvorhersagen wurden angepasst, um die Plattformwerte anzugleichen.

Ein fest eingetragener Windows-Zahlenabsatz im Notebook wurde entfernt, damit
Linux-Exporte keine veralteten Vergleichszahlen im Fließtext enthalten. Dynamische
Metriktabelle und Ergebnistext zeigen stets den tatsächlich berechneten Lauf.
Windows-Notebook/HTML wurden nach dieser Präzisierung erneut frisch geprüft.
Dies ist eine dokumentierte Reproduzierbarkeitsgrenze, keine Seed-/Validierungsstudie.
CI warnte zusätzlich über nicht beschreibbares .local (IPython nutzt temporären
Ordner) und unverschlüsselten Jupyter-TCP-Transport; keine numerischen Testfehler.
Der Push-Lauf dieses alten Heads wartete bei der Browserinstallation; sein Erfolg
wird hier nicht behauptet. Neue aktuelle Head-CI wird im PR separat nachgeprüft.

Zusätzliche Human-Reviewfrage: Ist die auf beiden Plattformen qualitativ gleiche
Rangfolge mit offengelegter CNN-Zahlendifferenz für diesen begrenzten Vergleich
angemessen eingeordnet? Keine allgemeine oder bitgenaue Reproduktion behauptet.


# Human Review – Exercise 12.4
**Industrial Data Science – Time Series Regression**

**Reviewer:** Studentischer Human Review  
**Datum:** 26.10.2026  
**Status:** SCIENTIFICALLY APPROVED – AWAITING TECHNICAL FINAL VERIFICATION  
**Merge-Autorisierung:** Nicht erteilt

## 1. Gesamtbeurteilung

Die Umsetzung von Exercise 12.4 ist wissenschaftlich nachvollziehbar und erfüllt nach den vorliegenden Unterlagen das Ziel, drei unterschiedliche Verfahren zur Regression multivariater Zeitreihen zu vergleichen.

Die Arbeit behandelt DTW-3-NN, Time Series Forest und ein eindimensionales CNN. Besonders positiv ist, dass die Modelle auf denselben ursprünglichen TRAIN-/TEST-Daten ausgewertet werden und die Ergebnisse sowohl durch Kennzahlen als auch durch grafische Darstellungen verglichen werden.

Die Interpretation bleibt auf den tatsächlich untersuchten Datensatz beschränkt. Ich sehe anhand der vorgelegten Ergebnisse keinen fachlichen Grund für eine grundlegende Überarbeitung.

## 2. Datengrundlage und Vorverarbeitung

Die Daten bestehen aus 95 TRAIN- und 42 TEST-Fällen mit jeweils 24 Kanälen und 144 Zeitpunkten.

Die dokumentierte Standardisierung verwendet ausschließlich die Trainingsdaten zur Bestimmung der Skalierungsparameter. Dieses Vorgehen ist für einen unverfälschten TEST-Vergleich wesentlich und methodisch angemessen.

Auch die Zielwerte werden für das CNN standardisiert. Die Rücktransformation auf die ursprüngliche kWh-Skala ist erforderlich, damit alle drei Verfahren mit denselben physikalischen Einheiten verglichen werden können.

Die grafische Darstellung eines Trainingsfalls zeigt drei der insgesamt 24 Eingangskanäle. Das ist zur Veranschaulichung ausreichend. Sie darf jedoch nicht als vollständige Darstellung aller Eingangsdaten interpretiert werden.

**Beurteilung:** Die Vorverarbeitung ist nachvollziehbar. Die korrekte Implementierung der TRAIN-only-Skalierung und Rücktransformation soll in der abschließenden technischen Prüfung nochmals bestätigt werden.

## 3. Bewertung der Regressionsverfahren

### DTW-3-NN

Das Verfahren verwendet drei Nachbarn und Dynamic Time Warping als Distanzmaß. Die DTW-Fensterbeschränkung von 0,1 ist dokumentiert.

Der Ansatz ist für Zeitreihen verständlich, da er zeitlich verschobene Signalverläufe miteinander vergleichen kann.

Der RMSE von 3,509225 kWh und der MAE von 2,711349 kWh zeigen allerdings, dass einzelne Vorhersagen stärker von den tatsächlichen Werten abweichen.

Die Vorhersagen liegen teilweise relativ dicht beieinander, obwohl die tatsächlichen Zielwerte stärker variieren. Das ist mit der Mittelwertbildung über die Nachbarzielwerte vereinbar. Eine allgemeine Ursache für die Fehler lässt sich daraus nicht eindeutig bestimmen.

### Time Series Forest

Der Forest verwendet 200 Bäume und zufällig ausgewählte Zeitintervalle.

Mit einem RMSE von 2,109183 kWh und einem MAE von 1,685254 kWh erzielt er auf dem untersuchten TEST-Split die kleinsten Fehler beider Kennzahlen.

Auch grafisch liegen viele Vorhersagen vergleichsweise nahe an der Identitätslinie.

Ich halte die Aussage für gerechtfertigt, dass der Forest in diesem konkreten Experiment die beste gemessene Regressionsleistung zeigt.

Eine allgemeine Überlegenheit gegenüber den anderen Verfahren ist damit nicht nachgewiesen.

### CNN

Das CNN wurde mit Seed 42 über 60 Epochen trainiert und besitzt laut Ergebnisdatei 5.553 trainierbare Parameter.

Die Trainingsverlustkurve sinkt von ungefähr 1,003 auf 0,0061. Das zeigt, dass das Modell die Trainingsdaten zunehmend gut approximiert.

Allerdings wird ausschließlich der Trainingsverlust dargestellt. Daraus kann weder eine gute Generalisierungsleistung noch ein nachgewiesenes Overfitting abgeleitet werden.

Der TEST-RMSE beträgt 3,614675 kWh und liegt damit etwas über dem Wert des DTW-3-NN. Gleichzeitig ist der MAE mit 2,608054 kWh geringer.

Diese unterschiedliche Reihenfolge der Kennzahlen ist plausibel: Der RMSE gewichtet größere Fehler stärker, während der MAE die durchschnittliche absolute Abweichung beschreibt.

Die CNN-Vorhersagen enthalten einige deutlichere Fehler, die das schlechtere RMSE-Ergebnis erklären können.

## 4. Numerische Ergebnisprüfung

Die bereitgestellten 42 TEST-Vorhersagen wurden unabhängig anhand der Formeln für RMSE und MAE nachgerechnet.

| Verfahren | RMSE [kWh] | MAE [kWh] |
|---|---:|---:|
| DTW-3-NN | 3,509225 | 2,711349 |
| Time Series Forest | 2,109183 | 1,685254 |
| CNN | 3,614675 | 2,608054 |

Die errechneten Ergebnisse stimmen mit der gelieferten Metrikdatei überein.

Die mittleren Vorhersageabweichungen (Vorhersage minus Istwert) betragen:

- DTW-3-NN: −0,264841 kWh
- Time Series Forest: −0,077742 kWh
- CNN: −0,825579 kWh

Alle drei Verfahren unterschätzen den mittleren Zielwert auf diesem TEST-Split geringfügig beziehungsweise beim CNN deutlicher. Eine systematische Unterschätzung in anderen Datensätzen ist daraus nicht ableitbar.

Der Forest besitzt außerdem die kleinste maximale absolute Einzelabweichung der drei untersuchten Modelle.

## 5. Bewertung der Abbildungen

### Eingangsdaten und Trainingsverlauf

Die erste Abbildung zeigt einen beispielhaften multivariaten Signalverlauf und den Trainingsverlust des CNN.

Die Achsen sind verständlich beschriftet. Die drei dargestellten Eingangskanäle lassen sich gut unterscheiden.

Der Trainingsverlust verläuft insgesamt fallend. Kleinere Schwankungen sind sichtbar und werden nicht durch eine künstlich geglättete Kurve verdeckt.

Die Darstellung ist für eine studentische Ausarbeitung ausreichend.

### Vorhersagen gegen tatsächliche Zielwerte

Die zweite Abbildung stellt die TEST-Vorhersagen aller drei Verfahren gegenüber.

Besonders sinnvoll ist die gemeinsame Achsenskalierung. Dadurch lässt sich die Streuung um die Identitätslinie direkt vergleichen.

Die RMSE-Werte in den Überschriften erleichtern die Interpretation.

Ich würde die Grafik unverändert beibehalten.

## 6. Reproduzierbarkeit und wissenschaftliche Grenzen

Die technische Dokumentation berichtet über 64 bestandene Tests, frische Notebook-Ausführung, reproduzierte Vorhersagen und erfolgreiche CI-Läufe.

Die hochgeladenen Ergebnisdateien sind numerisch konsistent. Die Prüfung der vollständigen Notebook-Implementierung, der ursprünglichen Rohdaten und sämtlicher CI-Protokolle ist jedoch von dieser unabhängigen Ergebnisprüfung zu unterscheiden.

Besonders relevant bleibt die Abweichung zwischen Windows und Linux beim CNN. Die Linux-Ergebnisse von 3,626400 kWh RMSE und 2,613485 kWh MAE liegen geringfügig über den lokalen Windows-Werten.

Diese Abweichung muss nicht zwingend auf einen Implementierungsfehler hinweisen. Sie kann durch unterschiedliche numerische Ausführung entstehen. Eine konkrete Ursache ist damit aber noch nicht nachgewiesen.

Positiv ist, dass die Abweichung nicht verschwiegen wird.

Weitere Einschränkungen sind die geringe Stichprobengröße, die Auswertung mit einem Seed, das Fehlen einer unabhängigen Validierungsstudie und die Diskrepanz zwischen der angegebenen Kataloggröße von 138 Reihen und den tatsächlich verwendeten 137 Fällen.

Eine statistisch abgesicherte Rangfolge der Modelle wird nicht beansprucht.

## 7. Schlussfolgerung

Die Ergebnisse zeigen, dass der Time Series Forest auf dem vorliegenden TEST-Split sowohl den geringsten RMSE als auch den geringsten MAE erreicht.

DTW-3-NN und CNN weisen größere Vorhersagefehler auf. Ihre unterschiedliche Reihenfolge bei RMSE und MAE zeigt, weshalb mehrere Bewertungskennzahlen sinnvoll sind.

Das Experiment verdeutlicht, dass ein komplexeres neuronales Modell bei einer kleinen Trainingsmenge nicht automatisch bessere TEST-Ergebnisse erzielen muss.

Die wissenschaftliche Darstellung ist verständlich, ausreichend kritisch und für eine studentische Übungsaufgabe angemessen.

## 8. Finale wissenschaftliche Entscheidung

**SCIENTIFICALLY APPROVED**

Ich befürworte die wissenschaftliche Freigabe der vorliegenden Exercise 12.4 unter Beibehaltung der dokumentierten Grenzen.

Es sind keine zusätzlichen Experimente allein zur Erhöhung des Umfangs erforderlich.

Die abschließende technische Prüfung soll insbesondere die Datenintegrität, Zielwert-Rücktransformation, Konsistenz der Vorhersagen und die dokumentierten Unterschiede zwischen Windows und Linux bestätigen.

Der Originalreview soll unverändert archiviert werden. Technische Ergänzungen sind separat zu dokumentieren.

**Dieser Human Review erteilt keine Autorisierung zum Merge, zur Änderung früherer Aufgaben oder zur Universitätseinreichung.**
altext
oben, separat in d9e4000 gesichert. Auch frühere technische Berichte bleiben vollständig
erhalten. Keine weiteren studentischen Ausführungen oder Freigaben behauptet.
Keine Merge-Autorisierung; PR #12 darf nicht gemergt werden.

### Code- und Zahlenabgleich
Offizielle Exercise 12.4 erneut mit implementierten DTW-kNN-, Forest- und CNN-
Regressoren abgeglichen. Keine zusätzliche Methode/Seed-Studie. Gegebene 95 TRAIN-
und 42 TEST-Fälle mit 24 × 144 endlichen Werten, Zielzuordnung case=0…41 bestätigt.
Alle Methoden werden gegen dieselben 42 ursprünglichen kWh-Zielwerte ausgewertet.
`fit_regressors` nimmt nur TRAIN-Eingaben/-Ziele an; sämtliche 24 Kanalstatistiken
werden daraus bestimmt. TEST erhält nur transform/predict; TEST-Ziele gelangen
nicht in Optimierung oder Verlust. Der CNN-Zielmittelwert 14,1655789474 und die
Populationsstandardabweichung 4,2899583401 stammen ausschließlich aus TRAIN.
Rücktransformation vor allen Metriken und beim separaten Gewichts-Ladetest geprüft.
Konfiguration bereits vor Training in 4e0f381 festgelegt, keine TEST-Parametersuche
im geprüften Code. Ursprünglicher Benchmark-Split ist keine belegte Zukunftsvalidierung.

Aus allen 126 gespeicherten Vorhersagen unabhängig mit NumPy rekonstruiert:
| Methode | RMSE | MAE | Mittel Vorhersage−Ist | Max. absoluter Fehler |
|---|---:|---:|---:|---:|
| DTW-3-NN | 3,5092246163 | 2,7113492063 | −0,2648412698 | 10,390000 |
| Forest | 2,1091826331 | 1,6852535714 | −0,0777416667 | 6,338100 |
| CNN | 3,6146750395 | 2,6080539167 | −0,8255793428 | 11,011297 |
Alle Werte in kWh. Sämtliche numerischen Aussagen des Human Reviews bestätigt;
keine sachliche Diskrepanz. Forest auf diesem Split kleinster RMSE/MAE/Maximalfehler;
kNN kleinerer RMSE als CNN, aber CNN kleinerer MAE. Kein allgemeines Modellranking.
TRAIN-Verlust 1,0031529276→0,0061136114, mit sichtbaren Schwankungen; ausschließlich
TRAIN, kein Nachweis von Generalisierung oder Overfitting. Quellenabweichung
138 beschriebene versus 137 tatsächliche Fälle bleibt ausdrücklich dokumentiert.

### Tatsächlich erneut ausgeführte technische Prüfungen
Projektstamm, `scripts/uv.cmd run --offline --locked`:
- `python -m unittest discover -s tests -q`: 64 Tests bestanden, 7,145 s.
- `python scripts/build_exercise_12_4.py`: drei Codezellen im frischen Kernel
  sequenziell ausgeführt, zwei eingebettete PNGs dekodiert. Zweiter vollständiger
  Fit reproduziert alle 126 Vorhersagen und 60 Verlustwerte (atol/rtol 1e-10).
  Alle Nachbarzielmittel (k=3, uniform, DTW window=0,1) sowie die Mittel sämtlicher
  200 Forest-Bäume für alle 42 TEST-Fälle nachgerechnet. Gespeicherte CNN-Gewichte
  ohne Pickle geladen, alle rücktransformierten Vorhersagen geprüft.
  5.553 tatsächliche Parameter, CPU, Seed 42, 60 Epochen bestätigt.
- `python scripts/check_exercise_12_4_html.py`: offline 900/1400 px, beide Bilder
  geladen, keine Seitenfehler oder horizontaler Überlauf.
- Beide Grafiken visuell geprüft: Beschriftungen, kWh-Einheiten, gemeinsame Skala,
  Identitätsgeraden und ausschließlich TRAIN-Verlust korrekt. Keine Grafikkorrektur nötig.
- Neue review_verification.json protokolliert Mean-Bias/Maximalfehler, Umgebung und
  Reproduzierbarkeitsgrenzen; zwölf aktuelle Artefakthashes separat geprüft.
  Beide Original-.ts-SHA256 stimmen. Keine erneute Netzwerkbeschaffung behauptet.
- Sechs wissenschaftliche Artefakte (PNGs, Kennzahlen, Vorhersagen, Verlauf, Gewichte)
  bytegleich zu d407b55. Frühere Kapiteldateien/Reviews/Umgebung unverändert,
  acht Kapitel-10/11-Abgabe-ZIPs per SHA256 und CRC bestätigt.

### Plattformbefund und Grenzen
Historisches Linux-PR-Protokoll 40412456174 erneut gelesen: PyTorch 2.9.1+cpu,
CNN RMSE/MAE 3,626400/2,613485. Windows erneut 3,614675/2,608054. Beide verwenden
dieselbe Implementierung und denselben Parameterplan auf CPU; kein GPU-Vergleich.
Lokal Windows AMD64: torch 2.9.1+cpu, Intra-Op num_threads=1, Inter-Op=4 (Default),
deterministic_algorithms=True, MKLDNN aktiviert. Die Ein-Thread-Einstellung bezieht
sich auf Intra-Op; eine pauschale Ein-Thread-Garantie für alle internen Aktivitäten
wird nicht behauptet. CPU/Build-/Threadinformationen stehen in review_verification.json.
`torch.manual_seed(42)` initialisiert das Netz, separater DataLoader-Generator mit
Seed 42, num_workers=0; Forest random_state=42. Keine weitere Seed-Studie.

Innerhalb desselben Runtimes besteht die vollständige Wiederholungsprüfung;
exakte Gleichheit zwischen Plattformen oder unterschiedlichen Runnern ist nicht belegt.
PyTorch 2.9 weist ausdrücklich auf diese Grenze hin:
https://docs.pytorch.org/docs/2.9/notes/randomness.html (gelesen 26.10.2026).
Mögliche Build-/Hardware-/Gleitkommaeffekte sind keine nachgewiesene konkrete Ursache.
Die Differenz wurde weder verschwiegen noch durch Parameteränderungen angeglichen.
Tatsächliche lokale Warnung: Jupyter-TCP unverschlüsselt; keine numerischen,
Notebook- oder HTML-Fehler. Historische CI meldete temporären IPython-Ordner.
Kleine Trainingsmenge, ein Split, fehlende unabhängige Validierung und keine
Signifikanz bleiben Grenzen. Neue aktuelle Head-CI wird nach Push separat im PR
belegt; Ready for review nur bei Erfolg. Kein Merge, weitere Aufgabe oder Upload.


---

## KI-Vermerk – ausdrückliche finale Merge-Autorisierung, 26.10.2026

Der Student hat nach der wissenschaftlichen Freigabe ausdrücklich beauftragt:
„wenn du fertig bist. kannst du es mergen“.
Dies autorisiert den regulären Merge von PR #12 nach vollständig erfolgreicher
technischer Abschlussprüfung einschließlich beider Checks am endgültigen Head.
Die frühere ausstehende Merge-Autorisierung ist damit für diesen Abschluss ersetzt;
der Originalreview und sämtliche früheren Berichte bleiben unverändert erhalten.

Wissenschaftlicher Status: APPROVED. Finale Merge-Autorisierung: erteilt, unter
Bedingung erfolgreicher aktueller Head-CI und fehlender Konflikte/Reviewblocker.
Codex dokumentiert diese tatsächlich erhaltene Entscheidung; kein zusätzlicher
studentischer Test behauptet. Kein Squash/Rebase, keine Universitätseinreichung.
Der tatsächliche Merge wird erst nach Erfüllung der Bedingungen ausgeführt und
mit seinem vollständigen SHA im PR und Abschlussbericht dokumentiert.
