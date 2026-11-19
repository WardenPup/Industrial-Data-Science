Unveränderte Originaldaten mit Herkunft, Abrufdatum und Lizenz ablegen.
Aufgabe 10.1 benötigt keine externen Daten.

Für 10.2: `uv run python scripts/download_ai4i.py` lädt `ai4i2020.csv` unverändert
aus dem offiziellen UCI-Archiv. Die CSV bleibt Git-ignoriert.

- Quelle: https://archive.ics.uci.edu/dataset/601/ai4i+2020+predictive+maintenance+dataset
- Archiv: https://archive.ics.uci.edu/static/public/601/ai4i%2B2020%2Bpredictive%2Bmaintenance%2Bdataset.zip
- DOI: https://doi.org/10.24432/C5HS5C
- Datensatz: AI4I 2020 Predictive Maintenance Dataset (2020), UCI Machine Learning Repository
- Lizenz: CC BY 4.0; https://creativecommons.org/licenses/by/4.0/
- Abruf: 26.10.2026; synthetische Daten, keine gemessenen Maschinenzeitreihen
- CSV: 522048 Bytes, 10000 Zeilen, 14 Originalspalten
- SHA256: `dc6630cd9b1f0f853922fad78a1b6436570d3f1ec863f1dd5c4340ac56bc8a8e`

Das Skript prüft diese feste Prüfsumme vor dem Speichern bzw. Wiederverwenden.
Abweichungen erfordern Untersuchung; bestehende Dateien werden nicht überschrieben.
Die vier ausgewählten Spalten behalten ihre originalen Einheiten im Namen.

## CI-Bestand seit 19.11.2026

Die Aussage „Git-ignoriert“ oben beschreibt den bisherigen Stand. Für den nach
studentischem Review geforderten sicheren CI-Betrieb wird genau diese bereits am
26.10.2026 bezogene Original-CSV nun unverändert versioniert (CC BY 4.0, Quelle und
SHA256 wie oben). Keine neue Datenquelle und keine Änderungen der Originalbytes.
Grund: abgelaufenes HTTPS-Zertifikat beim offiziellen UCI-Download in beiden
14.2-CI-Läufen. Der bestehende Downloader prüft bei vorhandenem Bestand dessen
festen SHA256 und beendet sich ohne Netzabruf. TLS-Prüfung bleibt unverändert aktiv;
keine Zertifikatsausnahme, keine Rücksetzung der Zeit und kein anderer Datensatz.
