# AppliancesEnergy – verwendete Benchmarkfassung

Abruf 26.10.2026. Offizielle Aufgabe 12.4 nennt UCI Appliances Energy Prediction
und empfiehlt aeon.datasets.load_regression. aeon 1.6.0 verweist für AppliancesEnergy
auf https://zenodo.org/records/18484626 (API-Metadaten: CC-BY-4.0).
Die beiden originalen .ts-Dateien wurden unverändert gespeichert; Zenodo-MD5 bei
Erstbezug geprüft, SHA256/URLs/Formen in sessions/ch12/appliances_source.json.
95 TRAIN + 42 TEST, 24 Kanäle, 144 Werte/Kanal, kontinuierliches Target, keine NaNs.
Kein Download von beliebigen UCI-Zeilen und kein selbst erfundener Fenster-Split.

Ursprüngliche TSER-Datenbeschreibung und Attribution:
Tan, Bergmeir, Petitjean und Webb (2020), Appliances Energy Dataset,
https://doi.org/10.5281/zenodo.3902637. Sie beschreibt Gesamtenergieverbrauch in kWh
als Ziel und Temperatur-/Feuchte-/Wetterkanäle, nennt aber 138 Zeitreihen. In den
aktuell vom offiziellen Loader referenzierten Dateien sind tatsächlich 137 Fälle.
Keine zusätzliche Reihe erzeugt oder stillschweigend ausgewählt. Die Header der
neuen Dateien enthalten keine Datums-/Kanalnamen; keine gesicherte Chronologie oder
exakte physikalische Kanalzuordnung erfinden. TRAIN/TEST werden wie geliefert genutzt.

UCI-Ursprung: Candanedo, Feldheim und Deramaix (2017), Data driven prediction models
of energy use of appliances in a low-energy house, Energy and Buildings 140, 81–97.
https://archive.ics.uci.edu/dataset/374/appliances+energy+prediction
UCI DOI https://doi.org/10.24432/C5VC8G, CC-BY-4.0; 19.735 Zeilen, 10-Minuten-Messungen
über etwa 4,5 Monate aus einem Haus. Dort ist Appliances in Wh angegeben; die TSER-
Zielgröße ist laut TSER-Beschreibung aggregierte Energie in kWh. Kein erneutes
Wh→kWh-Umrechnen der bereits gelieferten Zielwerte. Vorhersage aus vollständigen
Sensorfenstern ist extrinsische Regression, keine belegte zukünftige Energieprognose.

Originale unter data/raw/AppliancesEnergy nicht ins Git aufnehmen oder ändern.
Reproduktion: scripts/uv.cmd run --locked python scripts/download_appliances.py;
danach alle Analysen offline. Keine neuen globalen Pakete nötig.
