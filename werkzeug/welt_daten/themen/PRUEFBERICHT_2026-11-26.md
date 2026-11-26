# Prüfbericht Kartendaten Quellwissen – unabhängige Gegenprüfung (26.11.2026)

Ich habe nur gelesen und im Repo nichts geändert. Rohdaten für die Prüfung liegen unter `/home/claude/scratch/pruef/dl/`.
Abkürzungen: ✔ = bestätigt, ✘ = Abweichung, ⚠ = Hinweis bzw. Empfehlung.

## 1. kreise.json – Klimafelder (DWD 1991–2020)

**Geprüft:** Regionalverband Saarbrücken, Neunkirchen, St. Wendel, Freiburg, Hamburg und Garmisch-Partenkirchen, dazu am Rand Oberallgäu, Hochsauerlandkreis und Landsberg. Vergleichswerte:
- frische DWD-Stationsnormalwerte 1991–2020 (Sonnenschein, Frosttage): <https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/multi_annual/mean_91-20/>
- JA_MX_TN aus den Jahreswerten, von mir selbst gemittelt (Jahre 1991–2020): <https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/annual/kl/historical/>

| Kreis | sonne_h | Stationen (h) | frost | Station | tmin_abs | Station TNabs (eigene Rechnung) | Zone |
|---|---|---|---|---|---|---|---|
| RV Saarbrücken | 1710 | Ensheim 1749, St. Johann 1719, Burbach 1713 | 65 | Ensheim 70 | −10,8 | Ensheim −11,7 (30 J.) | 8a ✔ |
| Neunkirchen | 1688 | Wellesweiler 1689 | 73 | – | −11,9 | Wellesweiler −12,4 (23 J., 7b) | 8a ⚠ (Station eine halbe Zone kälter) |
| St. Wendel | 1672 | Urweiler 1671, Hof 1678, Tholey 1681 | 74 | – | −11,7 | Tholey −10,9; Urweiler −11,6 (15 J.) | 8a ✔ |
| Freiburg i. Br. | 1777 | Freiburg 1815 | 73 | 64 | −11,8 | −11,2 (27 J.) | 8a ✔ |
| Hamburg | 1617 | Fuhlsbüttel 1617 | 62 | 64,9 | −11,4 | −11,6 (30 J.) | 8a ✔ |
| Garmisch-P. | 1711 | GAP 1689, Mittenwald 1709, Zugspitze 1903 | 145 | Mittenwald 125, Zugspitze 290 | −17,8 | GAP −16,5, Mittenwald −16,5 | 6b ⚠ |

- ✔ Die Sonnenstunden und Frosttage passen zu den Stationen. Die Abweichungen sind durch Höhe und Lage erklärbar (Freiburg mit Schauinsland, Garmisch mit Hochlagen). Monatssumme = Jahreswert ±2 h. Auch die Stationsmittel TNabs in `pruef.md` habe ich mit eigener Rechnung genau nachvollzogen (−11,7 / −11,2 / −11,6 / −16,5).
- ✔ Die Umrechnung °F → °C ist richtig: 6a −23,3 · 6b −20,6 · 7a −17,8 · 7b −15,0 · 8a −12,2 · 8b −9,4 · 9a −6,7 °C (Untergrenzen; −60 °F + 5 °F je Halbzone, (F−32)·5/9).
- ✔ Globalstrahlung: Spanne 993–1207 kWh/m², Monatssumme = Jahreswert. Das passt zu den Stichproben in `pruef.md`.
- ✔ Lizenz: Die DWD-Nutzungsbedingungen nennen „Creative Commons BY 4.0“, Stand Mai 2024: <https://opendata.dwd.de/climate_environment/CDC/Nutzungsbedingungen_German.txt>.
- ⚠ **Grenzlagen:** Die Zone wird aus dem schon auf 0,1 °C **gerundeten** Wert bestimmt. 15 Kreise liegen innerhalb von 0,06 K an einer Zonengrenze, z. B. Garmisch −17,8 (Grenze −17,78 → 6b statt 7a). Weitere Fälle: Stormarn, Region Hannover, Lüneburg, Altenkirchen, Cochem-Zell, Westerwaldkreis und Stuttgart (je −12,2, Grenze −12,22), Roth, Cottbus, Dahme-Spreewald, Ilm-Kreis und Saalfeld-Rudolstadt (je −15,0), Viersen und Herne. **Empfehlung:** Die Zone aus dem ungerundeten Wert bestimmen und Kreise mit weniger als 0,3 K Abstand zur Grenze als „Grenzlage x/y“ kennzeichnen. Garmisch ist mit 6b sachlich vertretbar, denn das Mittel über alle Flächen wird von den Hochlagen gedrückt. Für Gärten im Tal (Station −16,5 = 7a) passt der Wert aber nicht. Das steht im Hinweis zwar allgemein, beim Info-Text für Alpenkreise sollte es aber ausdrücklich stehen.

## 2. goldreserven.json – IWF IL, RGV_REVS

**Geprüft:** frischer Abruf von 8 Ländern am 26.11.2026 über `https://api.imf.org/external/sdmx/2.1/data/IMF.STA,IL/DEU+USA+CHN+TUR+POL+IND+CHE+JPN.RGV_REVS.FTO.M?startPeriod=2026-06` (CSV).

| Land | Datei | IWF frisch (neuester Monat) |
|---|---|---|
| USA | 8.133,5 (09/2026) | 261.498.926 oz → 8.133,5 ✔ |
| DEU | 3.349,1 (09/2026) | 107.677.000 oz → 3.349,1 ✔ |
| CHN | 2.435,4 (10/2026) | 78.300.000 oz → 2.435,4 ✔ |
| CHE | 1.039,9 (09/2026) | 33.435.000 oz → 1.039,9 ✔ |
| IND | 880,5 (09/2026) | ✔ |
| JPN | 846,0 (10/2026) | ✔ |
| TUR | 797,0 (10/2026) | ✔ |
| POL | 690,0 (10/2026) | ✔ |

- ✔ Umrechnung: 1 t = 1.000.000 g ÷ 31,1034768 g = 32.150,7466 Feinunzen. Die Angabe SCALE=6 ist nur eine Anzeigeangabe, die Werte sind ganze Unzen.
- ✔ Die Angaben zur Türkei in `/home/claude/scratch/welt_global/pruef.md` stimmen: 12/2025 = 811,4 t, 02/2026 = 822,5 t, 03/2026 = 693,5 t, danach Anstieg bis 797,0 t. Die starken Sprünge sind belegt.
- ✘ **Der Türkei-Hinweis fehlt in der Datei.** In `goldreserven.json` steht er weder im Feld `hinweis` noch beim Land. Er steht nur in `scratch/welt_global/pruef.md`. **Empfehlung:** einen Satz in `hinweis` aufnehmen, z. B.: „Türkei: IWF-Reihe schwankt stark (03/2026 694 t, 10/2026 797 t), enthält vermutlich auch Gold aus Mindestreserven/Swaps; nicht direkt mit WGC-Werten vergleichbar.“ Das Wort „vermutlich“ sollte bleiben, denn einen amtlichen Beleg für die Ursache habe ich nicht geprüft.
- ✔ Nutzungsbedingungen <https://www.imf.org/en/About/copyright-and-terms>, Abschnitt „Special Terms for Statistical Data“, wörtlich bestätigt: Herunterladen, Ableiten, Veröffentlichen und Weitergeben sind erlaubt mit Quellenangabe „Source: International Monetary Fund, Database Name, <<link to the dataset>>“. Eine wesentliche Umwandlung muss genannt werden. „For any potential commercial reuse of IMF Data, email copyright@imf.org to request permission.“ Außerdem gilt: Wer die Daten als eigenes Produkt verkauft, muss darauf hinweisen, dass sie beim IWF kostenlos sind.
- ⚠ Die Datenzeilen selbst tragen das Lizenzfeld „© International Monetary Fund Copyright. All Rights Reserved.“ und verweisen auf die Bedingungen. Als Zitierlink empfiehlt der IWF `https://data.imf.org/en/datasets/IMF.STA:IL` (Feld SUGGESTED_CITATION). **Empfehlung:** Diesen Link als `u` bzw. in die Quellenangabe nehmen, die API-Adresse nur zusätzlich.
- ✘ **Alte Doku ist widersprüchlich:** `b/fertig/OFFEN.md` Zeile 12 sagt noch „weiterhin nur 22 Länder … nicht abrufbar“, Zeile 6 dagegen „157 Länder“. `b/fertig/QUELLEN.md` Z. 44–45 nennt noch BullionVault/Khaleej Times als Quelle. `b/fertig/EINBAU.md` Z. 45 hat das Info-Beispiel „3.350 t (Anfang 2026)“, jetzt gilt 3.349,1 t (09/2026). **Empfehlung:** diese Stellen nachziehen.

## 3. welterbe_staetten.json – 1.273 Punkte (Wikidata)

**Geprüft:** 15 zufällige Stätten (Seed 20261126) frisch über query.wikidata.org: 1382 Mongolischer Altai, 1293 Hegra, 97 Split, 246 Konark, 842 Cilento, 933 Loiretal, 678 Huế, 853 Pécs, 310 Altamira, 1185 Plantin-Moretus, 984 Blaenavon, 733 Ferrara, 1567 Westfront 1. Weltkrieg, 378 Mudéjar Aragón, 1548 Valongo.
- ✔ Bei allen 15 stimmen Name, Land und Art (Cilento = Kultur ist richtig), die Lage stimmt grob, und die Koordinaten sind identisch mit Wikidata.
- ⚠ 678 Huế: Das Hauptobjekt hat in Wikidata keine Koordinate. Der Punkt stammt also von einem Teilobjekt, aber `lage:'Bestandteil'` fehlt, anders als im Hinweis beschrieben. Kleinigkeit, bei Gelegenheit die Regel prüfen.

**Deutschland:** 55 Punkte mit DEU. Abgeglichen mit der vollständigen Liste nach KMK-Stand (55, einschließlich Herrnhut 2024 über 1468 und Schlösser Ludwigs II. 2025; Dresden gestrichen und nicht enthalten). Alle 55 sind vorhanden, keine fehlt, keine ist doppelt ✔. Die Jahre stichprobenartig geprüft (Wies 1983, Brühl 1984, Trier 1986, Potsdam 1990, Kölner Dom 1996, Wattenmeer 2009 usw.) ✔. Hinweis: 1468 steht mit dem Punkt Bethlehem (USA, −75,38/40,62) auch bei DEU. Auf der Deutschland-Karte erscheint Herrnhut daher nicht als Punkt. ⚠ Empfehlung: für 1468 einen Punkt in Herrnhut ergänzen oder Christiansfeld nehmen, wie in Wikidata.

**Behauptung „USA 28 statt 27“: nicht bestätigt, welterbe.json mit 27 ist richtig.**
- ✔ 1468 Herrnhuter Siedlungen mit Bethlehem (2024) gehört zu Recht zu den USA.
- ✘ **Der Fehler steckt bei 1351 „El Camino Real de Tierra Adentro“.** Wikidata (Q911953) führt als Staat USA und MEX. Die Stätte ist bei der UNESCO aber **nur für Mexiko** eingetragen. Belege: <https://www.worldheritagesite.org/list/id/1351> („Country: Mexico“, ohne Erweiterung in die USA) und <https://en.wikipedia.org/wiki/Camino_Real_de_Tierra_Adentro> (2010 nur der mexikanische Abschnitt). Die UNESCO-Seite whc.unesco.org war per curl durch Cloudflare gesperrt und ist deshalb nicht direkt geprüft. Ohne 1351 zählen die USA 27 Stätten (24 eigene, Kluane und Waterton gemeinsam mit Kanada, dazu 1468), einschließlich Okefenokee 2026 (Eintragung belegt z. B. durch <https://www.nbclosangeles.com/news/national-international/georgia-okefenokee-swamp-unesco-world-heritage-site/3922852/>).
- **Empfehlung:** In `welterbe_staetten.json` bei 1351 `iso3` auf `['MEX']` setzen und die Notiz in `scratch/wikidata/pruef.md` („USA 28 … b vermutlich zu niedrig“) streichen. `welterbe.json` mit USA 27 **nicht** ändern.

## 4. naturparks.json – 105 Parks

**Zahl:** Die VDN-Seite <https://naturparke.de/naturparke/> nennt am 26.11.2026 „104 Naturparke“. Die Länderliste ist abgeglichen. RP zeigt dort 7 Parks, Pfälzerwald ist nicht dabei ✔.

✘ **Der Naturpark Pfälzerwald ist kein Naturpark mehr.** Die „Landesverordnung über das Biosphärenreservat Pfälzerwald …“ vom 23.07.2020, § 10 Abs. 2, setzt die „Landesverordnung über den ‚Naturpark Pfälzerwald‘ … vom 22. Januar 2007“ **außer Kraft**. Beleg: <https://fileserver.naturschutz.rlp.de/rvo/bsr/BSR-7000-001.pdf>. Die Zählung 105 = 104 + 1 ist daher falsch, richtig sind **104**. **Empfehlung:** den Eintrag entfernen (oder als „seit 2020 Biosphärenreservat Pfälzerwald, kein Naturpark“ markieren, mit `aufgeloest: 2020`) und Kopf und Hinweis auf 104 ändern.

**8 Stichproben:** Wikidata frisch abgefragt (die Werte der Datei stimmen alle mit Wikidata überein), dazu die VDN-Parkseiten unter naturparke.de/naturparke/<park>/:

| Park | Land | km² Datei / VDN | Jahr Datei / VDN | Bewertung |
|---|---|---|---|---|
| Saar-Hunsrück | SL (+RP) | 2.061 / 2.055 | 1980 / 1980 | ✔ Lagepunkt 6,76/49,56 bei Weiskirchen (SL) |
| Pfälzerwald | RP | 1.798 / – | 1958 / – | ✘ siehe oben |
| Harz (NI) | NI | 909 / 2.825 | 1960 / 1960 | ⚠ VDN-Seite nennt 2.825 km² (wohl Geopark bzw. ganzer Harz); 909 km² für den NI-Park ist plausibel, nicht weiter belegt |
| Wendland.Elbe | NI | 1.159 / 1.159 | 2006 / **1968** | ✘ Jahr: VDN 1968 (Wikidata 2006 = Umbenennung bzw. Neugründung) |
| Vulkanregion Vogelsberg | HE | 883 / 880 | 1956 / **1957** | ✘ kleine Abweichung (Jahr) |
| Lüneburger Heide | NI | 1.078 / 1.070 | 1956 / 1956 | ✔ |
| Südeifel | RP | 443 / 432 | 1958 / 1958 | ✔ (Fläche ≈) |
| Hessischer Spessart | HE | 942 / 942 | 1962 / **1963** | ✘ kleine Abweichung (Jahr) |

- **Empfehlung:** Bei Abweichungen das Gründungsjahr nach VDN nehmen (Wendland.Elbe 1968, Vogelsberg 1957, Hess. Spessart 1963), oder im Hinweis sagen: „Jahr laut Wikidata, kann vom VDN abweichen“. Die Weserbergland-Fläche von 1.159 km² ist zufällig gleich der von Wendland.Elbe, laut Wikidata aber korrekt (115.897 ha). Die VDN-Seite für Weserbergland habe ich nicht gefunden. Kosmetik: „Nördlicher Teutoburger Wald-Wiehengebirge“ hat kein „Naturpark“ im Namen; beim VDN heißt er „TERRA.vita“.

## 5. heilbaeder.json – 43 neue Orte (HE 22, TH 11, ST 3, BB 7)

Alle 43 gegen die Belegdokumente geprüft. Die Quellenlinks HE, ST und BB habe ich frisch abgerufen (HTTP 200, PDF; BB ist identisch mit der Kopie in `roh/hb`).
- ✔ **HE (22):** Abgleich mit RP Kassel, Stand 30.04.2026 (<https://rp-kassel.hessen.de/sites/rp-kassel.hessen.de/files/2026-05/2026-internet.pdf>). Es gibt 19 Heilbäder, Wildungen und Reinhardshausen haben ein gemeinsames Prädikat, dazu 3 Orte mit Heilquellenkurbetrieb (Bad Soden a. Ts., Bad Vilbel, Bad Zwesten). Alle sind vorhanden, keiner zu viel. Die Zweitprädikate habe ich nachgesehen (Bad Nauheim und Bad Endbach Kneippheilbad, Herbstein Luftkurort, Bad Schwalbach Kneippkurort) ✔.
- ✔ **TH (11):** Drs. 6/3368, Anlage 2, Stand 01.01.2017 (Bild `roh/hb/thB-12.png`; Quelle <https://parldok.thueringer-landtag.de/ParlDok/dokument/61255/kur-und-erholungsorte-in-th>). Die Prädikate stimmen wörtlich überein (z. B. Langensalza „Schwefel-Sole-Heilbad“, Lobenstein „Moorheilbad“). Weggelassen sind wie angegeben Finsterbergen, Masserberg und Neustadt/Harz (heilklimatisch), Friedrichroda, Stützerbach und Tambach-Dietharz (Luftkurort) sowie Tabarz (Kneippheilbad). ⚠ Der Stand ist 9 Jahre alt (das ist bekannt).
- ✔ **ST (3):** In der PM 22/2024 stehen „3 Orte mit dem staatlichen Prädikat ‚Heilbad‘“ (Salzelmen, Kösen, Schmiedeberg). Die Arten stimmen mit dem Text überein.
- ✔ **BB (7):** In der PM 182/2025 sind die 8 Kurorte namentlich genannt, ohne Buckow (Kneipp). Die Prädikate stimmen mit den Einzel-PMs überein (Belzig, Saarow, Liebenwerda, Burg, Wilsnack). Templin und Freienwalde sind nur durch die Sammelliste belegt, das reicht.
- ✔ Die Lage ist grob plausibel (alle Punkte liegen am Ort im richtigen Land, stichprobenartig angesehen).
- ⚠ Bad Liebenwerda („Ort mit Peloid-Kurbetrieb“) ist streng genommen kein Heilbad. Die Aufnahme ist aber gleich behandelt wie die „Orte mit Heilquellenkurbetrieb“ in HE und TH, also in Ordnung.

## 6. boeden.json (SoilGrids) und sonneneinstrahlung.json (NASA POWER)

- ✔ **Lizenz Böden:** Das README unter <https://files.isric.org/soilgrids/latest/data/README.md> sagt: „The SoilGrids maps are publicly available under the CC-BY 4.0 License“. Die Nennung im Kopf passt.
- ✔ **Lizenz Strahlung:** <https://nasa-power.s3.amazonaws.com/LICENSE.txt> ist der Text „Attribution 4.0 International“ (CC BY 4.0). Die Angabe im Kopf ist richtig.
- **5 Stichproben-Zellen.** Böden: Klasse aus der Datei. Strahlung: Datei gegen frischen POWER-API-Abruf (Klimatologie, Mittel der vier 1°-Punkte der Zelle, kWh/m²·Tag, je Jahr / Juni / Dezember):

| Zelle (Mitte) | Boden | Strahlung Datei | POWER-API frisch | |
|---|---|---|---|---|
| 49° N 7° O (Saarland) | Cambisole | 3,20 / 5,75 / 0,75 | 3,22 / 5,75 / 0,73 | ✔ |
| 49° N 31° O (Ukraine) | Schwarzerden | 3,45 / 6,30 / 0,70 | 3,47 / 6,30 / 0,72 | ✔ |
| 3° S 59° W (Amazonas) | Ferralsole | 4,70 / 4,65 / 4,30 | 4,69 / 4,67 / 4,30 | ✔ |
| 25° N 5° O (Sahara) | Leptosole | 6,30 / 7,60 / 4,40 | 6,31 / 7,58 / 4,42 | ✔ |
| 61° N 25° O (Finnland) | Podsole | 2,50 / 5,30 / 0,15 | 2,52 / 5,31 / 0,13 | ✔ |

  Am Rand geprüft: Dekkan = Vertisole, Saskatchewan = Luvisole (Parabraunerden; plausibel, Kastanozeme liegen weiter südlich), Riad = Regosole. Alles plausibel. Die Abweichung der Strahlung liegt nur in der Byte-Stufe (0,05).
- ⚠ **Widerspruch in der Doku zu Böden:** Die Datei kodiert „keine Angabe“ als **0** (12.185 Zellen mit 0, keine mit 255; 4.015 Zellen mit Wert, wie angegeben). `scratch/welt_global/pruef.md` §2 sagt aber „sonst steht 255“. Die Datei ist in sich stimmig, nur `pruef.md` und gegebenenfalls EINBAU sollten auf 0 korrigiert werden.
- ⚠ Den Zeitraum der POWER-Klimatologie (2001–2025 laut Kopf) liefert die API im Kopf nicht als Feld. Das habe ich nicht unabhängig bestätigt.

## Wichtigste Punkte zum Umsetzen
1. **Naturparks:** Pfälzerwald entfernen bzw. als aufgelöst markieren (LVO 2020); dann sind es 104, nicht 105.
2. **Welterbe:** Bei 1351 Camino Real nur MEX eintragen. Die USA haben 27 Stätten, `welterbe.json` ist richtig, die Notiz „USA 28“ ist falsch.
3. **Gold:** Den Türkei-Hinweis in `goldreserven.json` aufnehmen; OFFEN, QUELLEN und EINBAU in b nachziehen; als Zitierlink data.imf.org/en/datasets/IMF.STA:IL nehmen.
4. **Klima:** Die Zone aus dem ungerundeten Wert bestimmen und Grenzlagen kennzeichnen (15 Kreise, u. a. Garmisch 6b/7a).
5. **Naturparks:** Die Gründungsjahre weichen in 3 von 8 Stichproben vom VDN ab (Wendland.Elbe 1968, Vogelsberg 1957, Hess. Spessart 1963).
