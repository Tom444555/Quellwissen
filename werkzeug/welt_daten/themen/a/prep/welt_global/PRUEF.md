# Prüfbericht Welt-Ebenen (global) – Stand 26.11.2026

Dateien: `goldreserven.json` (ersetzt b/fertig/goldreserven.json), `boeden.json`, `sonneneinstrahlung.json`; Skripte in `skripte/` (`holen.sh` lädt Rohdaten, dann `gold_json.py`, `boeden.py`, `sonne.py`; `sonne.py` speichert Zwischenstände unter roh/power – Ordner vorher anlegen). Rohdaten nach Gebrauch gelöscht. Formatprüfung mit Kopien von `a/prep/pruefen.py` und `b/prep/pruefen.py`: keine Fehler, keine Warnungen.

## 1. Goldreserven (id `goldreserven`, land-wert, Tonnen)
- **Quelle:** IWF, Datensatz *International Liquidity (IL)* (die frühere IFS-Liquiditätstabelle, Schema IRFCL), Reihe `RGV_REVS` „Gold reserves (volume)“, Einheit FTO = Feinunzen. Abruf SDMX 2.1: `https://api.imf.org/external/sdmx/2.1/data/IMF.STA,IL/.RGV_REVS.FTO.M` (dazu Q und A, ältere Jahre ab 1990). Einen eigenen Datensatz „IRFCL“ oder „IFS“ gibt es in der neuen Schnittstelle nicht mehr. Den Code RAFAGOLDV_OZT gibt es dort nicht.
- **Verfahren:** Für jedes Land die neueste Beobachtung aus Monats-, Quartals- und Jahresreihe. Umrechnung: t = Unzen ÷ 32.150,7466, gerundet auf 0,1 t (unter 1 t auf 0,01 t). Das Attribut SCALE=6 ist nur eine Anzeigeangabe, die Werte sind ganze Unzen (USA 261.498.926 oz = 8.133,5 t).
- **Ergebnis:** 157 Länder (vorher 22), davon 117 mit Bestand > 0. Ein Wert von 0 heißt, dass das Land meldet, kein Gold zu halten (z. B. Kanada, Norwegen). Feld `stand` je Land (meist 09 oder 10/2026).
- **Euroraum:** jede nationale Zentralbank einzeln. Das Aggregat G163 (Euroraum) ist nicht enthalten. EZB (508,4 t), IWF (2.814,1 t), BIZ (316,9 t), BEAC (4,7 t) und BCEAO (36,5 t; WAEMU-Reihe G759, 03/2025) stehen unter `daten_institutionen` und nicht als Land.
- **Zuordnungen:** CWX (Zentralbank Curaçao und Sint Maarten) → CUW mit Hinweis; KOS → XKX; WBG → PSE. Ländergruppen (G001, GX010 usw.) und alte Codes (ANT, CSK, YUG, YAR, G758) sind verworfen.
- **Weggelassen, weil letzte Meldung vor 2015:** Syrien (06/2011, 25,8 t), Jemen (07/2014, 1,6 t), Iran (1995, 150,6 t), Tansania, Ruanda, Turkmenistan, Vanuatu (je 0). Ohne IWF-Meldung: u. a. Nordkorea, Myanmar, Kuba.
- **Veraltete Meldungen (enthalten, `stand` beachten):** Venezuela 06/2018 (161,2 t), Afghanistan 05/2021, Laos 02/2020, Vietnam 05/2020 (0), Russland 11/2025, Libanon 03/2025, Tadschikistan 02/2023.
- **Stichproben gegen die alte Datei:**

| Land | alt | IWF neu | Stand neu | Bewertung |
|---|---|---|---|---|
| USA | 8.133,5 | 8.133,5 | 09/2026 | gleich |
| DEU | 3.350,3 | 3.349,1 | 09/2026 | IWF-Reihe bis 03/2026 genau 3.350,3, danach leichte Abnahme (Goldmünzen) |
| ITA | 2.451,8 | 2.451,9 | 09/2026 | Rundung |
| FRA | 2.437,0 | 2.437,0 | 09/2026 | gleich |
| CHN | 2.306,3 (amtl. 2.331 im Mai) | 2.435,4 | 10/2026 | IWF 12/2025 = 2.306,3 und 05/2026 = 2.331,5, also beide alten Werte bestätigt; seither monatliche Käufe |

  Weitere Länder weichen ab, weil sich der Bestand geändert hat: POL 614 → 690,0 (laufende Käufe der NBP, Monatsreihe steigt stetig); CZE 71,6 → 90,0; RUS gleich (2.326,5). **TUR 614,3 → 797,0:** Die IWF-Reihe liegt schon 12/2025 bei 811 t und schwankt stark (03/2026: 693 t). Die Türkei meldet vermutlich mehr als nur das Eigengold der Zentralbank (Gold aus Mindestreserven der Banken, Swaps). Der Wert ist amtlich, aber nicht direkt mit dem Wert des World Gold Council vergleichbar.
- **Lizenz:** IWF Copyright and Usage, Abschnitt „Special Terms for Statistical Data“ (abgerufen 26.11.2026, <https://www.imf.org/en/About/copyright-and-terms>). Herunterladen, Ableiten, Veröffentlichen und Weitergeben sind erlaubt. Bedingungen: Quellenangabe „Source: International Monetary Fund, …, <Link>“, eine Umrechnung muss genannt werden (Unzen → Tonnen steht im Kopf), und Nutzer der weitergegebenen Daten sind auf diese Bedingungen hinzuweisen. **„For any potential commercial reuse of IMF Data, email copyright@imf.org to request permission.“** Das ist im Kopf (`lizenz`, `hinweis`) vermerkt. Vor dem Verkauf der App oder des Buchs anfragen, wie bei den Staatsschulden.

## 2. Böden (id `boeden`, Natur, raster, Kategorien)
- **Quelle:** ISRIC SoilGrids, WRB-Referenzbodengruppen, wahrscheinlichste Klasse (`MostProbable.vrt`, 250 m). Gelesen wurde die mitgelieferte Übersichtsdatei `MostProbable.vrt.ovr` (32 MB), Stufe 1/30°. Ein Abruf über HTTP-Range war nicht nötig. Die Klassenliste stammt aus `MostProbable.rat.json` (30 Gruppen nach WRB 2006). Zitat: Hengl et al. 2017, PLoS ONE 12(2): e0169748.
- **Lizenz:** CC BY 4.0. Belegt durch das README unter files.isric.org/soilgrids/latest/data („publicly available under the CC-BY 4.0 License“) und die ISRIC-Datenrichtlinie 2023 („CC-BY 4.0 for derivative predictions/visualisations (e.g. SoilGrids)“).
- **Verfahren:** Je 2°-Zelle (60 × 60 Bildpunkte) wird die häufigste Gruppe genommen. Die Zelle wird nur gefüllt, wenn mindestens 25 % Boden-Bildpunkte vorhanden sind; sonst steht 255 (Meer, Eis, Antarktis, nördlich von 84° N). Byte = Klassen-Nr. 1–30 (= ISRIC-Wert + 1). Der Kopf `klassen` enthält je Nummer [deutscher Name, Farbe, Erklärung, WRB-Name]. Die Legende zeigt nur die 27 Gruppen, die vorkommen (Durisole, Stagnosole und Umbrisole werden nirgends vorherrschend). 4.015 Zellen haben einen Wert. Im Mittel nimmt die Hauptgruppe 68 % der Zelle ein.
- **Stichproben (plausibel):** Ukraine: Schwarzerden · Amazonas und Kongo: Ferralsole · Saarland: Cambisole (Braunerden) · Finnland: Podsole · Sibirien: Cryosole · Dekkan: Vertisole · Saskatchewan: Kastanozeme · Pampa: Phaeozeme · Sahara: Leptosole · Island: Cambisole · Grönland: leer. Borneo ergibt Nitisole (gängige Karten zeigen eher Acrisole). So steht es in SoilGrids, es wurde nicht korrigiert.
- **Offen/Vorbehalt:** Die Namen folgen WRB 2006 (Albeluvisole heißen heute Retisole). Deutsche Namen, Farben und Erklärungen sind eigene Fassung. Die Daten sind ein Modell (maschinelles Lernen) und keine Kartierung. Das alte Schema `BODEN` kann ersetzt werden.

## 3. Sonnenscheindauer → Sonneneinstrahlung (id `sonneneinstrahlung`, Natur, raster)
- **CRU CL 2.0 (sunp) geprüft und ausgeschlossen:** Laut CRU-Datenseite (crudata.uea.ac.uk/cru/data/hrg/) gilt für die Datensätze die „Open Database License … Database Contents License under the conditions of Attribution and Share-Alike“. ODbL mit „Weitergabe unter gleichen Bedingungen“ ist keine der erlaubten Lizenzen (wie bei OSM). Die Daten sind daher nicht verwendet.
- **Ersatz:** NASA POWER, Klimatologie `ALLSKY_SFC_SW_DWN` (Globalstrahlung, CERES SYN1deg, 1°). Gelesen wurde die ganze Weltkarte in **einem** Zarr-Zugriff auf den offiziellen Bucket `s3://nasa-power` (syn1deg/temporal/power_syn1deg_climatology_temporal_lst.zarr). Die POWER-API ließe nur 10°-Kacheln zu, das wären 648 Anfragen gewesen. Gegenprobe Saarbrücken: Die API liefert für den Punkt dieselben Werte (3,1519 kWh/m²·Tag).
- **Lizenz:** Der Daten-Bucket enthält `LICENSE.txt` = **CC BY 4.0**, `CITATION.cff` nennt „license: CC-BY-4.0“. Die Daten sind also nicht „gemeinfrei“ wie bisher angenommen, aber frei. Die Nennung steht im Kopf.
- **Zeitraum:** Laut API-Kopf 01/2001–12/2025. Die Zarr-Metadaten nennen noch 2001–2020, die Werte sind aber identisch mit der API.
- **Verfahren:** W/m² × 24/1000 = kWh/m² pro Tag. Je 2°-Zelle wird über vier 1°-Felder gemittelt. Byte ÷ 20 = kWh/m²·Tag. Ebenen: `jahr`, `jun`, `dez`. Alle Zellen sind gefüllt (auch Meer und Eis).
- **Stichproben** (Jahresmittel, kWh/m²·Tag; Vergleich PVGIS 5.3 der EU-JRC, SARAH-3, 2005–2023, Ortswert):

| Ort | 2°-Zelle | 1°-Feld | PVGIS | Jahressumme Zelle |
|---|---|---|---|---|
| Saarbrücken | 3,22 | 3,15 | 3,22 (1.175 kWh/m²) | 1.175 |
| Madrid | 4,56 | 4,70 | 4,87 (1.779) | 1.664 |
| Kairo | 5,58 | 5,71 | 5,97 (2.180) | 2.037 |
| Oslo | 2,75 | 2,66 | 2,60 (949) | 1.004 |

  Die Abweichung der 2°-Zelle beträgt bis ca. 7 %. Das liegt an der Mittelung über rund 220 × 220 km (Madrid mit Gebirge, Kairo mit Küste und Nil) und an der unterschiedlichen Satellitenquelle.
- **Nicht geliefert:** Sonnenstunden (Sonnenscheindauer). Eine frei lizenzierte Weltkarte wurde nicht gefunden: CRU = ODbL, WorldClim hat keine Sonnenstunden. Die id ist bewusst `sonneneinstrahlung` und nicht `sonnenstunden`, weil der Inhalt eine andere Größe ist. Beim Einbau bei Bedarf umbenennen.

## Seekabel (nur Prüfung)
- TeleGeography: CC BY-NC-SA, ausgeschlossen (wie bekannt).
- EMODnet Human Activities, Telecom cables: Die Daten stammen von TeleGeography/PriMetrica, die Wiederverwendung braucht laut Eintrag die Zustimmung von PriMetrica. Der Datensatz deckt nur EU-Gewässer ab. Ausgeschlossen.
- Greg's Cable Map (über Ifremer-Katalog): „Open and Free“, aber ohne benannte Lizenz und ohne Datenrichtlinie der Quellen, Stand 2016. Nicht verwendbar.
- NOAA/Marine Cadastre „Submarine Cable Areas“: gemeinfrei, aber nur US-Gewässer.
- OpenStreetMap: ODbL, ausgeschlossen.
- **Ergebnis:** keine frei lizenzierte weltweite Seekabelkarte.

## Für OFFEN.md / EINBAU.md (Vorschläge)
- b/OFFEN „Goldreserven vollständig“ → erledigt (IWF IL über api.imf.org). Der Vorbehalt zur kommerziellen Nutzung bleibt (copyright@imf.org).
- a/OFFEN „Sonnenstunden“ → Ersatz Globalstrahlung geliefert; „Böden“ → geliefert (SoilGrids, CC BY 4.0).
- EINBAU **boeden**: `GRUND`-Eintrag als Kategorien-Raster wie `biome` (Farbe aus `klassen[n][1]`, scharf zeichnen ohne Interpolation). Info: „Schwarzerden (Chernozeme) – <Erklärung>“. Quelle: „SoilGrids, ISRIC (CC BY 4.0)“.
- EINBAU **sonneneinstrahlung**: `GRUND`-Eintrag wie `klima` (weich zeichnen), Palette `legende.jahr`. Info (Beispiel Saarbrücken-Zelle): „ca. 3,2 kWh/m² pro Tag ≈ 1.170 kWh/m² im Jahr (Juni 5,75 · Dezember 0,75)“; Byte-Stufen 0,05. Quelle: „NASA POWER / CERES (CC BY 4.0)“.
- EINBAU **goldreserven**: unverändert (land-wert, `daten[ISO3].t`). Neu ist `daten_institutionen` (optional in Info/Liste: „EZB 508 t, IWF 2.814 t …“). Die Legende kann bleiben (Maximum 8.133,5 t).
