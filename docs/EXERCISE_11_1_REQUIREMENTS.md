# Aufgabe 11.1 – Anforderungen und Abnahmekriterien

Offizielle Quelle: https://noxthot.github.io/ws26_industrial_datascience_manuscript/1_act1/7_self_study_session2.html
Tatsächlich über HTTPS gelesen am 26.10.2026. KI-gestützte Zusammenfassung,
keine zusätzliche studentische Freigabe. Der aktuelle Nutzerauftrag autorisiert
Analyse und Umsetzung bis zum Human-Review-Gate.

1. Offizielle CSV unverändert laden; Date als geordneten Wochenindex prüfen.
2. pieces und pieces_gaps mit der bereitgestellten plot_production_data-Funktion darstellen.
3. pieces_gaps rollend glätten, Fenster und Mittelwert/Median begründet wählen.
4. Ursprüngliche Lücken exakt erhalten; geglättete Reihe mit Seaborn darstellen.
5. Deutsche Erklärung von Ziel, Mathematik, Umsetzung, Beobachtung, Grenzen und Lernfragen.
6. Reproduzierbares ausgeführtes Notebook und HTML-Export; keine PDF-Pflicht in 11.1.
7. Datenquelle, Lizenzhinweis, SHA256, technische Prüfungen und KI-Beitrag dokumentieren.

Geplant: zentrierter 5-Wochen-Median für den historischen Managementbericht,
Mittelwertvergleich bei gleichem Fenster. min_periods=1 und erneutes Maskieren
erhalten alle ursprünglichen NaNs ohne zusätzliche Lücken. Zahl tatsächlich
vorliegender Nachbarn offenlegen: dünn besetzte Fenster sind weniger belastbar.
Die Wahl erfolgt anhand der Robustheit und zeitlichen Auflösung, nicht über
Optimierung an pieces. Kein Forecast, kein Train/Test-Split erforderlich;
zentrierte Fenster würden für Echtzeitprognosen zukünftige Werte verwenden.
Kein Imputieren, STL oder Ausreißerzählen aus 11.2–11.4.

Abnahme: unabhängige kleine Zahlenbeispiele für Robustheit/Ränder/NaNs,
Datums-/Schema-/Hashprüfung, frischer sequenzieller Notebooklauf, eingebettete
HTML-Grafiken, visuelle Kontrolle und unveränderte Kapitel-10-Artefakte.
Status nach erfolgreicher Technikprüfung: AWAITING HUMAN REVIEW, kein Merge.
