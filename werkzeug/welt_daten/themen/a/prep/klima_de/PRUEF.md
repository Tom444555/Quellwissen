# Prüfbericht Klima-Kreisebenen (Stand 26.11.2026)

Ergebnis: `kreise_klima.json` mit allen **401 Kreisen** (AGS wie in `kreise.json`) und den Feldern
`sonne_h`, `sonne_mon_h` (12 Monatswerte), `frosttage`, `tmin_abs_c`, `zone`, `zone_kalt`, `zone_mild`, `zellen`.
Prüfdatei je Kreis: `pruef_stationen.csv`. Stationswerte: `stationen_tnabs.json`.

## 1. Verfahren

### Rasterwerte (Sonne, Frosttage)
- DWD-Raster „vieljährige Mittel 1991–2020“, 1 km × 1 km, 654 × 866 Zellen, Gauß-Krüger Zone 3 (EPSG:31467),
  Kopf `XLLCORNER/YLLCORNER` (= Ecke, Zellmitte = Ecke + 500 m), `NODATA_VALUE -999`, Zeile 1 = Norden.
- Namensgebung laut BESCHREIBUNG-PDF: `_01`…`_12` Monate, `_13` Frühling, `_14` Sommer, `_15` Herbst, `_16` Winter, `_17` Jahr.
  Jahres- und Jahreszeitenraster sind die Summe der Monatsraster.
- Einheit Sonnenscheindauer: Stunden (h), keine Skalierung (Bundesmittel des Jahresrasters 1665 h – passt zum DWD-Wert für 1991–2020).
  Frosttage: Anzahl Tage mit Tmin < 0 °C, keine Skalierung. (Die BESCHREIBUNG für 1991–2020 fehlt im Verzeichnis; geprüft wurde die für 1981–2010, gleiches Format.)
- Zellmittelpunkte mit pyproj (EPSG:31467 → EPSG:4326) umgerechnet; Kreiswert = Mittel der Zellen, deren Mittelpunkt im Kreis-Polygon liegt.
  Da die Ringe in `kreise.json` keine Löcher haben (eine kreisfreie Stadt liegt auch im äußeren Ring des umgebenden Landkreises),
  wird jede Zelle dem **kleinsten** sie enthaltenden Kreis zugeordnet. Alle 401 Kreise haben ≥ 34 Zellen (kleinster: Schweinfurt Stadt);
  der Notfall „nächste Zelle“ trat nicht auf.
- Monatswerte: Summe der 12 Kreis-Monatswerte weicht vom Jahreswert um höchstens 10 h (≤ 0,6 %) ab – vermutlich Rundung der ganzzahligen DWD-Raster; für die Anzeige unkritisch.

### Winterhärtezone
1. **Stationen:** alle Jahreswert-Dateien (annual/kl/historical) mit Zeitraum, der 1991–2020 zu ≥ 20 Jahren abdecken kann (416 Dateien).
   Feld `JA_MX_TN` (absolutes Jahresminimum), Jahre 1991–2020, Fehlwert −999 verworfen.
   **331 Stationen mit ≥ 20 gültigen Jahren**; davon 327 innerhalb des DWD-Rasters (ohne Rasterwert u. a. Helgoland) → genutzt.
   Mittelwert der Jahresminima je Station. Koordinaten/Höhe aus der Stationsliste (aktueller Standort).
2. **Übertragung auf die Fläche** – drei Verfahren per Leave-one-out-Kreuzvalidierung geprüft (`2_kreuzvalidierung.py`):

   | Verfahren (8 nächste Stationen, Potenz 2) | MAE | RMSE | Fehler > 2,8 K (= 1 ganze Zone) |
   |---|---|---|---|
   | A reine IDW | 1,05 K | 1,46 K | 6 % |
   | B IDW + feste Höhenkorrektur −0,5 K/100 m | 1,21 K | 1,57 K | 7 % |
   | **C Regression auf DWD-Raster Januar-Tmin + IDW der Residuen** | **0,82 K** | **1,06 K** | **1 %** |

   Die feste Höhenkorrektur macht es **schlechter** (der beobachtete Gradient der Extremminima ist nur −0,43 K/100 m
   und wird von Kaltluftseen in Tälern/Mulden überlagert) → verworfen.
   Gewählt: **C**. Regression `TNabs = −10,93 + 1,35 · Tmin_Jan` (R² = 0,79), wobei `Tmin_Jan` das DWD-Raster
   „mittleres tägliches Minimum Januar 1991–2020“ ist (1/10 °C, enthält Höhe und Lage über das DWD-Verfahren).
   Die Stationsabweichungen von der Regression werden je 1-km-Zelle per IDW (8 nächste Stationen, Potenz 2, Mindestabstand 1 km)
   interpoliert. Kreiswert = Mittel aller Zellen; dazu kälteste/mildeste Zelle (`zone_kalt`, `zone_mild`).
3. **Zonen (USDA):** 10 °F je Zone, a/b je 5 °F, exakt umgerechnet: z. B. 6a −23,3…−20,6 °C, 6b −20,6…−17,8, 7a −17,8…−15,0,
   7b −15,0…−12,2, 8a −12,2…−9,4, 8b −9,4…−6,7 °C (vollständige Tabelle in `zonen_grenzen_c`).
   Zone wird aus dem auf 0,1 °C gerundeten Kreismittel bestimmt.
   Verteilung: 6b 5 Kreise, 7a 81, 7b 167, 8a 136, 8b 12.

## 2. Stichproben gegen DWD-Stationsnormalwerte 1991–2020
Vergleichswerte: DWD `observations_germany/climate/multi_annual/mean_91-20` (Sonnenscheindauer, Frosttage).
„Zelle“ = Rasterwert am Stationsort, „Kreis“ = Kreismittel.

| Station / Kreis | Sonne Station | Sonne Zelle | Sonne Kreis | Frost Station | Frost Zelle | Frost Kreis | TNabs Station (Zone) | Kreis TNabs (Zone, Spanne) |
|---|---|---|---|---|---|---|---|---|
| Saarbrücken-Ensheim (319 m) / Regionalverband Saarbrücken | 1749 | 1744 | 1710 | 70 | 70 | 65 | −11,7 (8a) | −10,8 (8a, 8a–8a) |
| Freiburg (237 m) / Freiburg i. Br. | 1815 | 1807 | 1777 | 64 | 64 | 73 | −11,2 (8a) | −11,8 (8a, 7a–8a) |
| Hamburg-Fuhlsbüttel (11 m) / Hamburg | 1617 | 1614 | 1617 | 65 | 64 | 62 | −11,6 (8a) | −11,4 (8a, 8a–8a) |
| Oberstdorf (806 m) / Oberallgäu | 1622 | 1626 | 1741 | 144 | 143 | 142 | −21,7 (6a) | −19,8 (6b, 5a–7a) |
| Garmisch-Partenkirchen (719 m) / LK Garmisch-P. | 1689 | 1687 | 1711 | – | 131 | 145 | −16,5 (7a) | −17,8 (6b, 5a–7a) |

Bewertung:
- **Raster am Stationsort** stimmt mit den DWD-Normalwerten auf 0–8 h (< 0,5 %) bzw. 0–1 Frosttag überein →
  Georeferenzierung (Ecke/Zellmitte, Zeilenrichtung, Projektion) ist korrekt.
- **Kreismittel** weichen erwartungsgemäß vom Einzelort ab: Freiburg (Schauinsland-Hochlagen: mehr Frost, weniger Sonne),
  Oberallgäu (Hochlagen über dem Nebel sonniger als der Talort Oberstdorf), Saarbrücken (Stadt/Saartal etwas milder als der Flughafen Ensheim auf 319 m).
- Winterhärte: Stationen und Kreismittel liegen in derselben Zone (Saarbrücken, Freiburg, Hamburg). Oberstdorf ist als
  Kaltluft-Talstation kälter als das Kreismittel (6a vs. 6b), Garmisch-Ort milder als das Kreismittel (Hochlagen/Zugspitze ziehen das Mittel herunter).

## 3. Lizenz / Namensnennung
- DWD-Nutzungsbedingungen (opendata.dwd.de/climate_environment/CDC/Nutzungsbedingungen_German.txt, Stand Mai 2024):
  „Es gelten die Bedingungen der Lizenz Creative Commons BY 4.0 "CC BY 4.0".“
- DWD-Vorgaben für den Quellenvermerk (dwd.de → Rechtliche Hinweise → Vorlagen Quellenangabe): Textform „Quelle: Deutscher Wetterdienst“;
  bei veränderten Daten z. B. „Datenbasis: Deutscher Wetterdienst, Einzelwerte gemittelt“; unmittelbar an der Information platzieren.
- **Empfohlene Nennung an der Kartenebene:** „Datenbasis: Deutscher Wetterdienst, Einzelwerte gemittelt (CC BY 4.0)“.
  Zitierform der Raster laut BESCHREIBUNG: „DWD Climate Data Center (CDC), Vieljähriges Mittel der Raster der Sonnenscheindauer für Deutschland 1991–2020, Version v1.0“ (analog Frosttage).
- USDA-Zonen: nur die Definition (°F-Grenzen) übernommen, keine USDA-Daten.

## 4. Grenzen der Methode
- **Kreismittel ≠ Gartenstandort:** In Kreisen mit Mittelgebirge/Alpen reicht die Spanne bis zu 2–3 Zonen (siehe `zone_kalt`/`zone_mild`).
  Lokale Kaltluftmulden, Stadtwärmeinseln und Hanglagen sind im 1-km-Raster nur teilweise enthalten.
- **Klimawandel:** Das Mittel 1991–2020 ist deutlich milder als ältere Zonenkarten (oft auf 1976–2005); daher überwiegend 7b/8a.
  Einzelne kalte Winter liegen mehrere Kelvin unter diesem Mittel – die USDA-Zone ist ein Mittel, kein Sicherheitswert.
- Jahresminimum je **Kalenderjahr** (DWD-Feld), nicht je Winter; Unterschied für ein 30-Jahres-Mittel gering.
- Stationsstandorte: aktuelle Koordinaten aus der Stationsliste; Verlegungen innerhalb 1991–2020 sind nicht einzeln berücksichtigt.
- Stationen mit 20–29 Jahren können durch fehlende (z. B. kalte) Jahre leicht verzerrt sein (keine Lückenergänzung).
- Kreisgrenzen sind vereinfacht (1/100 Grad ≈ 0,7–1,1 km); an Grenzen können einzelne Zellen dem Nachbarkreis zugeordnet sein.
  Überlappungen durch die Vereinfachung werden dem kleineren Kreis zugeschlagen.
- Sonnenscheindauer ≠ Solarertrag: für PV ist die **Globalstrahlung** (`strahl_kwh`) die bessere Größe (siehe Abschnitt 7).

## 5. Offenes / Vorschläge
- Optional weitere Raster ohne Mehraufwand: Eistage, Sommertage, heiße Tage, Vegetationsbeginn/-ende, Niederschlag.
- Die Seite www.dwd.de/copyright wurde per curl gelesen (Weiterleitung auf „Rechtliche Hinweise“); ein Abruf per Web-Werkzeug war nicht freigegeben.

## 6. Dateien und Ablauf
```
sh   skripte/0_laden.sh roh                       # DWD-Rohdaten laden (~10 MB, danach löschbar)
python3 -I skripte/1_stationen.py roh stationen_tnabs.json
python3 -I skripte/2_kreuzvalidierung.py roh stationen_tnabs.json
python3 -I skripte/3_kreise_klima.py roh <quellwissen>/werkzeug/welt_daten/themen/a/fertig/kreise.json stationen_tnabs.json .
python3 -I skripte/4_stichproben.py roh kreise_klima.json stationen_tnabs.json
python3 -I skripte/5_strahlung.py roh/strahl <quellwissen>/werkzeug/welt_daten/themen/a/fertig/kreise.json kreise_klima.json
```
`skripte/raster.py` = Hilfsfunktionen (ASC lesen, Projektion, Kreismasken). Benötigt: numpy, pyproj, matplotlib.
Rohdaten (`roh/`) wurden nach dem Lauf gelöscht.

## 7. Nachtrag: Globalstrahlung (`strahl_kwh`, `strahl_m`)
- Quelle: DWD-Raster `grids_germany/multi_annual/radiation_global`, **Zeitraum 1991–2020 vorhanden**, Version V003
  (aus Boden- und Satellitenmessungen), Globalstrahlung auf die **horizontale** Ebene, Einheit **kWh/m²** (laut Header und BESCHREIBUNG, keine Skalierung).
  Jahr: `..._multi_annual_..._1991_2020.zip`, Monate: `..._multi_monthly_..._1991_2020_01..12.zip`.
- Besonderheiten: Die Dateien sind ZIP-Archive mit 22 Zeilen `[header]` vor dem ESRI-ASCII-Teil; die Ecke ist
  `XLLCORNER 3280500` (die übrigen DWD-Raster: 3280414,7, also ~86 m versetzt) → eigene Zellmittelpunkte und Kreismasken
  (`skripte/5_strahlung.py`). Sonst gleiches Verfahren wie bei den Sonnenstunden (Mittel der Zellen, kleinster Kreis gewinnt).
- Ergebnis: 993 kWh/m² (05958 Hochsauerlandkreis) bis 1207 kWh/m² (09181 Landsberg am Lech); Monatssumme = Jahreswert ± 0,7 kWh/m².
- DWD-Unsicherheit laut BESCHREIBUNG: ±6 % Jahr, ±5 % (Sommer) bis ±15 % (Winter) Monat. Gilt für freien Horizont (Hindernisse < 5°).
  Geneigte, nach Süden ausgerichtete Module erhalten je nach Neigung grob 10–15 % mehr (im Hinweis vermerkt, nicht gerechnet).

**Stichprobe** gegen DWD-Stationsmessungen (Tageswerte `daily/solar`, `FG_STRAHL` in J/cm², ÷ 360 → kWh/m²;
nur Jahre 1991–2020 mit ≥ 347 gültigen Tagen):

| Station / Kreis | Station gemessen (Jahre) | Rasterzelle | Kreismittel | Abw. Zelle |
|---|---|---|---|---|
| Saarbrücken-Ensheim / Regionalverband Saarbrücken | 1125 (25) | 1139 | 1135 | +1,2 % |
| Freiburg / Freiburg i. Br. | 1128 (18) | 1181 | 1175 | +4,7 % |
| Hamburg-Fuhlsbüttel / Hamburg | 1021 (13) | 1005 | 1008 | −1,5 % |

Alle Abweichungen innerhalb der DWD-Unsicherheit (±6 %). Freiburg und Hamburg haben nur 18 bzw. 13 vollständige
Messjahre im Zeitraum – der Stationswert ist dort selbst unsicherer (andere Jahre als das 30-Jahres-Raster).

## Nachtrag 26.11.2026 (nachmittags): Zone aus dem ungerundeten Wert
Schritte 1 und 3 mit frisch geladenen DWD-Daten wiederholt (gleiche 327 Stationen, Regression −10,933 + 1,352 · Tjan, alle 401 Kreiswerte `tmin_abs_c`, `zone_kalt`, `zone_mild` unverändert). Die Zone wird jetzt aus dem **ungerundeten** Kreismittel bestimmt. Dadurch ändern sich sechs Kreise: Cochem-Zell 8a → 7b (−12,225 °C), Roth, Cottbus, Dahme-Spreewald, Ilm-Kreis und Saalfeld-Rudolstadt 7b → 7a (−15,000 bis −15,037 °C). Die übrigen neun Grenzlagen aus dem Prüfbericht (u. a. Garmisch, Stormarn, Stuttgart, Viersen, Herne) bleiben in ihrer Zone. Die App weist bei Werten bis 0,1 K an einer Grenze weiter auf die Nachbarzone hin.
