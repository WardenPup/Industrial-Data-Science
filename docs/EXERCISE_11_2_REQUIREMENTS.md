# Aufgabe 11.2 – Anforderungen und Umsetzungsplan

Offizielle Quellen, vollständig per HTTPS gelesen am 26.10.2026:
- https://noxthot.github.io/ws26_industrial_datascience_manuscript/1_act1/7_self_study_session2.html
- https://noxthot.github.io/ws26_industrial_datascience_manuscript/1_act1/1_0_data_imputation.html

KI-gestützte Zusammenfassung. Der aktuelle Nutzerauftrag autorisiert Analyse und
vollständige Umsetzung bis zum menschlichen Review; keine fachliche Freigabe.

## Exakte Aufgabe in eigenen Worten

1. Die geglättete Reihe mit Lücken aus 11.1 als Eingabe verwenden.
2. Mit verschiedenen in Kapitel 5 besprochenen Imputationsmethoden experimentieren.
3. Ergebnisse mit der bereitgestellten plot_production_data-Funktion visualisieren.
4. Ergebnisse und Grenzen diskutieren.

Kapitel 5 demonstriert Forward Fill, Backward Fill, lineare Interpolation,
Polynominterpolation Grad 2 und 5 sowie PCHIP. Der Vergleich umfasst alle sechs
Varianten. Kein erneutes Glätten, keine STL-Zerlegung und keine Aufgabe 11.3/11.4.
11.2 selbst fordert keinen PDF-Export. Notebook plus HTML erfüllen die bestehende
Projekt-/Abgaberegel für Notebooks; keine Universitätseinreichung.

## Daten und Wiederverwendung

Unveränderte synthetische Wochen-CSV und Hashprüfung aus production.py;
smooth_with_gaps reproduziert exakt den freigegebenen 5-Wochen-Median mit 367 NaNs.
Zusätzlich den Hash der in main freigegebenen 11.1-Eingabereihe prüfen.
Bereits vorhandene pandas/SciPy/Seaborn/Matplotlib/nbconvert reichen aus;
pyproject.toml, uv.lock und .venv bleiben Grundlage. Keine neuen Pakete.
Die Kursfunktion wird über eine 11.2-spezifische Anpassung wiederverwendet:
Imputierte Werte nur an ursprünglichen Fehlstellen, sichtbare NaN-Unterbrechungen
und eindeutige deutsche Labels. Freigegebene 11.1-Dateien bleiben unangetastet.

## Umsetzung und Abnahme

- Berechnung und Darstellung in getrennten Modulen, Notebook vom Projektstamm.
- Eingabemaske, geordnete Wochen, Lückenlängen und Randlücken explizit prüfen.
- Bekannte Werte durch alle Verfahren unverändert lassen; nur fehlende ergänzen.
- Lineare/Polynom-/PCHIP-Interpolation nur innerhalb bekannter Stützstellen;
  keine stille Extrapolation oder nachträgliche Begrenzung negativer Ergebnisse.
  ffill/bfill können richtungsbedingt Randlücken behalten; tatsächliche Zahl melden.
- Je Verfahren die dreiteilige Kursgrafik, dazu gemeinsamer Detailvergleich an
  einer deterministisch gewählten längsten Lücke. Achsen: Datum/Stück pro Woche.
- Numerische Tabelle: gefüllt/verbleibend, Min/Max ergänzter Werte und außerhalb
  lokaler Randwerte liegende Interpolationen. Letzteres ist ein Diagnoseindikator,
  kein Nachweis falscher Messwerte. pieces nicht als fehlerfreie Ground Truth nutzen.
- Deutsche Definitionen, konkrete Beobachtungen und Grenzen; keine unbelegten
  Genauigkeitsranglisten. Historischer Bericht: spätere Stützwerte zulässig;
  keine direkte Verwendung dieser Pipeline für Echtzeitprognosen.
- Unabhängige kleine Testfälle für Werte, Randlücken, Masken/Nichtmutation,
  tatsächliche Datenintegrität; alle Tests und frischer Notebooklauf.
- Eigenständiges HTML, dekodierte Grafiken, Offline-Browser und visuelle Prüfung;
  echte Ergebnisse und Hashes dokumentieren. Separate sinnvolle Commits und Draft-PR.
- Status AWAITING HUMAN REVIEW. Reviewfragen zu Methodenwahl, langen Lücken und
  Überschwingern; keine studentische Beobachtung oder Zustimmung erfinden.
