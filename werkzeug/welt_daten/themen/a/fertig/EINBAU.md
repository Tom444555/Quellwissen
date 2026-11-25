# Einbau der Themen-Ebenen in `welt.js`

Alle Dateien: kompaktes JSON, Kopf `{id, name, gruppe, typ, einheit, legende, quellen:[{t,u,stand,lizenz}], hinweis, daten}`; Arrays statt Objekte, wo viele Einträge – Feldnamen stehen dann im Kopf unter `felder`. Koordinaten in Grad (1/100). Prüfen: `python3 -I prep/pruefen.py`. Quellenzeile in der Legende jeweils aus `quellen[].t` kürzen (Vorschlag unten). Raster-Zellen = gleiche Mitten wie `DAT.raster` (2°, lon −179…179, lat 89…−89), Index `((89-lat)/2)*180 + (lon+179)/2`.

Vorschlag Einordnung: Natur-Punkte/-Linien als neue Schalter in `S.ov` (wie `tiefen`, `kriege`); Raster/Länderwerte als `GRUND`-Einträge (wie `klima` bzw. `le`); Deutschland-Ebenen mit `de:1` (Flug nach Deutschland).

## Natur

**vulkane** (`typ:'punkte'`, 647) – `felder: name, lon, lat, typ, hoehe_m, zeit, rang, iso3, letzter_bedeutender_ausbruch, text`. `zeit` 1–9 = Zeitklasse des letzten Ausbruchs (Kopf `zeit` gibt den Text, 1 = „1964 oder später“). Zeigen: Rang 1 immer, Rang 2 ab Zoom ≈ 2, Rang 3 ab Zoom ≈ 4. Zeichen: kleines Dreieck (wie `gipfel`), Farbe nach `zeit` (Legende: #ff4a2a / #ff9a3a / #ffd27a / #c8b8a8), Name ab Zoom 2,5. Info-Karte: „Name – Typ, Höhe m · Land (DAT.idx[iso3].n) · letzter Ausbruch: <zeit-Text> · text“. Legende „Vulkane nach letztem Ausbruch“. Quelle: „NOAA NCEI Volcano Locations / Significant Eruptions (CC0)“.

**erdbeben** (`punkte`, 1.604) – `felder: datum, lon, lat, magnitude, tiefe_km, iso3, meer, rang`. Rang 1 = M ≥ 8 (100), 2 = 7,5–7,9, 3 = 7,0–7,4. Zeigen: Rang 1 immer, 2 ab Zoom 1,5, 3 ab Zoom 3; Kreis mit Radius ~ 10^(M−7)·k (z. B. `2+3*(M-7)**1.5` px), halbtransparent (#ff3b30 / #ff9500 / #ffd60a, globalAlpha .7). Optional Zeitfilter über `S.jahr`/Epoche. Info: „Erdbeben M 9,5 · 22.05.1960 · Chile · Herdtiefe 25 km“. Quelle: „USGS ComCat (gemeinfrei)“. Gut mit **platten** kombinierbar.

**platten** (`linien`) – `daten`: 217 Grenzen `[pb, v_mm_jahr, rang, codes, koord_flach]`; je Teilstrecke i (Punkt i→i+1) ein Buchstabe in `codes` (R/G = auseinander, S/O/K = zusammen, T/C = seitlich; Bedeutung im Kopf `codes`). Zeichnen: Teilstrecken nach Art einfärben (#ff6b4a / #4ac8ff / #ffd24a), Linienbreite 1,6; Subduktion optional mit kleinen Zähnen. `daten_platten`: 52 Platten `{c, n, lon, lat, rang}` als kursive Beschriftung (Rang 1 ab Zoom 1, Rang 2 ab 2,5, Rang 3 ab 4) – Lagepunkt ist ein Punkt in der Platte, nicht der Schwerpunkt. Info beim Antippen: „Subduktionszone zwischen Nazca- und Südamerikanischer Platte, ca. 80 mm/Jahr“ (Wert `v` aus der Datei). Quelle: „Bird 2003 (PB2002), Aufbereitung H. Ahlenius/Nordpil, ODC-BY“.

**meeresstroemungen** (`linien`, 33) – `{n, art: warm|kalt|neutral, meer, rang, text, schema:true, p:[[[lon,lat],…],…]}` (an der Datumsgrenze geteilt). Zeichnen: gestrichelte Bögen mit Pfeilspitze am Ende jedes Teilstücks, warm #ff6a4a, kalt #4aa8ff, neutral #c8d0d8; Rang 1 immer, 2 ab Zoom 1,8, 3 ab 3. Name entlang der Linie ab Zoom 2. Legende mit Zusatz „schematisch“. Quelle: „NOAA (Auswahl, warm/kalt-Regel); Verlauf schematisch“.

**windguertel** (`flaechen`) – `daten`: 9 Bänder `[name, lat_von, lat_bis, richtung, pfeil_wohin_grad, rang, text]` (für Nord- und Südhalbkugel je eigener Eintrag); `daten_monsun`: 6 Rechtecke. Zeichnen: Bänder als sehr helle Streifen (Alpha .12) mit Pfeilreihen in `pfeil_wohin_grad` (0 = Nord, 90 = Ost), Kalmen/Rossbreiten grau ohne Pfeile; Monsun-Rechtecke gestrichelt #5ad08a mit abgerundeten Ecken. Info: `text`. Gut als Ergänzung zur Scheibe (Breitenkreise). Hinweis „schematisch, wandert mit den Jahreszeiten“ in der Legende.

**klima_raster** (`raster`, 4 Ebenen × 16.200 Zellen) – `daten.{t_jahr, t_kalt, t_warm, niederschlag}` je Base64, 1 Byte/Zelle (255 = leer; Temperatur Byte−70 °C, Niederschlag Byte×20 mm/Jahr). Als `GRUND`-Einträge wie `klima` (r-Raster), Palette aus `legende.t_jahr` bzw. `legende.niederschlag`. Weich zeichnen (Zellen 2°, bilinear im Shader oder als 180×90-Textur mit LINEAR-Filter). Info beim Antippen: „Jahresmittel 9 °C · kältester Monat 0 °C · wärmster 18 °C · Niederschlag ca. 1.100 mm“. Quelle: „NCEP/NCAR Reanalysis 1981–2010 (NOAA PSL), GPCP v2.2 1979–2010 (NASA)“. Hinweis: grob, nicht für einzelne Orte.

**biome** (`raster`) – Base64, 1 Byte = Biom 1–14 (0 = keins); Klassen/Farben im Kopf `klassen` (an `VEGN`-Farben angelehnt). Kann `veg` ersetzen (genauer als das bisherige Schema) oder als eigener Eintrag `GRUND.biom`. Info: Biom-Name. Quelle: „RESOLVE Ecoregions 2017 (Dinerstein et al.), CC BY 4.0“.

**waldanteil** (`land-wert`) – `daten`: ISO3 → % Wald 2020. `GRUND`-Eintrag: `{n:'Waldanteil', g:'Natur', u:'% der Landfläche · 2020', p:GRN, s:v=>v/80, lg:['0 %','40 %','80 %']}`. Quelle: „FAO FRA 2020 über Our World in Data (CC BY)“.

**pflanzen_heimat** (`land-kat`) – `daten[pflanzen-id]`: `{n, wcvp, heimat:[ISO3], eingeb:[ISO3], l3:[WGSRPD], gebiet_en}`. Einbau: wenn eine Pflanze gewählt ist (`S.pflanze`), Länder in `heimat` grün (#5ad08a, Alpha .55) und `eingeb` gelb (#e8c860, Alpha .35) füllen – ersetzt/ergänzt die groben Rechtecke in `PFL`. Info-Zeile: „Heimat laut WCVP (Kew): 73 Länder · eingebürgert in 19“. Quelle: „WCVP v16 (Kew), CC BY 4.0“. Fliegenpilz (p13) fehlt.

## Himmel

**sternbilder** (`himmel`) – Koordinaten äquatorial J2000, `ra` in Grad 0–360. `daten`: 89 Sternbilder `{k, n (deutsch), lat (lateinisch), rang, ra, dec (Beschriftungspunkt), l:[[[ra,dec],…],…]}`; `daten_sterne`: 921 Sterne `[ra, dec, mag, name, bezeichnung, polarstern]`. Auf Globus/Scheibe legen: Bildpunkt eines Himmelspunkts zur Zeit t: `lat = dec`, `lon = ra − 15·GAST(t)` (GAST in Stunden; `lon` auf −180…180 bringen); für die „Kuppel“ der 3D-Scheibe direkt `dec` als Höhe über dem Äquator verwenden. Sterngröße `r = max(0.6, 3.2 − 0.55·mag)` px, Farbe #c8d8ff, Linien #6a8ac8 Alpha .6, Namen ab Zoom 2 für benannte Sterne; Polarstern (`polarstern=1`) immer mit Ring #ffe14a und Beschriftung. Quelle: „d3-celestial (O. Frohn, BSD-3), Hipparcos/XHIP, IAU“ – BSD-Hinweis (Copyright (c) 2015 Olaf Frohn) im Impressum/Quellenverzeichnis mitführen.

**sonnenfinsternisse** (`linien`, 22) – `{datum, max_utc, art (total|ringförmig), lon, lat (Maximum), dauer_s, dauer, p:[[[lon,lat],…]]}`. Zeichnen: Mittellinie 2 px (total #ffffff, ringförmig #ffb84a), Maximum als roter Punkt; Beschriftung „12.08.2026 total · 2 min 21 s“ am Maximum ab Zoom 1,5; Filter nach Jahr möglich. Info: „Totale Sonnenfinsternis am 12. August 2026, Maximum 17:45 UTC über dem Nordatlantik (65,2° N, 25,3° W), Dauer 2 min 21 s“. Hinweis: nur Mittellinie, Pfadbreite fehlt. Quelle: „eigene Rechnung mit astronomy-engine, geprüft an NASA (Espenak)“.

**Sonnenstand (Formel, kein JSON)** – `welt.js` hat `sonne()` mit einfacher Deklination und ohne Zeitgleichung (Fehler bis ca. 4° in Länge). Genauer (NOAA „General Solar Position Calculations“, nach Spencer 1971; gegen astronomy-engine geprüft: Abweichung ≤ 0,2° Länge, ≤ 0,45° Breite, `prep/sonnenstand.py`):

```js
function sonne(d){ d=d||new Date(); const y=d.getUTCFullYear(), n=Math.floor((Date.UTC(y,d.getUTCMonth(),d.getUTCDate())-Date.UTC(y,0,1))/864e5)+1,
  tage=(y%4===0&&(y%100!==0||y%400===0))?366:365, h=d.getUTCHours()+d.getUTCMinutes()/60+d.getUTCSeconds()/3600,
  g=2*Math.PI/tage*(n-1+(h-12)/24),
  eqt=229.18*(0.000075+0.001868*Math.cos(g)-0.032077*Math.sin(g)-0.014615*Math.cos(2*g)-0.040849*Math.sin(2*g)),   // Minuten
  dek=0.006918-0.399912*Math.cos(g)+0.070257*Math.sin(g)-0.006758*Math.cos(2*g)+0.000907*Math.sin(2*g)-0.002697*Math.cos(3*g)+0.00148*Math.sin(3*g); // rad
  let lon=-15*(h-12+eqt/60); lon=((lon+180)%360+360)%360-180; return [lon, dek*180/Math.PI]; }
```

## Deutschland

**kreise** (`kreise`, 401) – `felder: ags, name, art, land, einwohner_2024, flaeche_km2, lon, lat, ringe`; Ringe delta-kodiert in 1/100 Grad (Dekodieren: `x=r[0],y=r[1]; for(i=2;…;i+=2){x+=r[i];y+=r[i+1]}`, dann /100). Als Deutschland-Ebene (`de:1`) mit Wert = Einwohner/km² (`einwohner_2024/flaeche_km2`), Palette MAGMA log, Grenzlinien dünn (#ffffff Alpha .25) ab Zoom 4; Namen ab Zoom 7. Info: „Landkreis Saarlouis (SL) · 205.129 Ew. · 459 km² · 447 Ew./km²“ (Werte aus der Datei) mit Rangliste wie `balken()`. Hanau (06415) ohne Werte. Quelle: „© GeoBasis-DE / BKG (2026), dl-de/by-2-0 (vereinfacht); Einwohner: Statistisches Bundesamt 31.12.2024“.

**schutzgebiete** (`punkte`, 34) – `{art, n, land, jahr, ha, lon, lat, wd, text?, unesco?}`. Zeichen: Nationalpark = grünes Blatt/Quadrat #4ad07a, Biosphärenreservat = blauer Kreis #5ab8e8 (national #8ab0c8); Kreisgröße √ha; Namen ab Zoom 5. Zwei Einträge ohne Lage (lon/lat null) nicht zeichnen, aber in Liste/Info führen. Info: „Nationalpark Hainich (TH) · seit 1997 · 7.513 ha“. Quelle: „BfN 2025; Lage: Wikidata (CC0)“.

**wanderwege** (`linien`, 12) – `{n, km, land, rang, text, schema:true, q, hinweis, p:[[lon,lat,Ort],…]}`. Zeichnen: gestrichelt #ffb86a 2 px, kleine Punkte an den Orten, Name an Linienmitte ab Zoom 5; Rang 3 ab Zoom 6. Info: „Rennsteig · 168,3 km · Hörschel → Blankenstein (schematisch)“. Quellenzeile je Weg aus `quellen_wege[q]`.

**wein_hopfen** (`punkte`) – `daten`: 13 Weinanbaugebiete `{n, ha, tsd_hl_2025, land, ort, lon, lat}`; `daten_hopfen`: 5 Hopfengebiete `{n, ha, land, ort, lon, lat, text}`. Zeichen: Kreis ∝ √ha (Wein #b04a7a, Hopfen #8ad04a), passt zu den vorhandenen Schaltern `hopfen`/Getreide. Info: „Pfalz · 23.787 ha Rebfläche (2024) · 1,87 Mio. hl Wein (2025)“. Quelle: „DWI/Destatis; Verband Deutscher Hopfenpflanzer“.

**heilbaeder** (`punkte`, 57, Teilliste NI + BY + NW + SN) – `{n, land, praedikat, art, lon, lat, stand}`. Zeichen: Tropfen/Kreis nach `art` (Sole #7ad0ff, Thermal #ff8a5a, Mineral #c8a0ff, Moor #8a6a3a, offen #d0d0d0), ab Zoom 5. Info: „Bad Nenndorf · Moorheilbad, Mineralheilbad, Thermalheilbad“. Quelle: „Landesverzeichnisse NI (2026), BY (2020), NW (2026), SN (2019)“. Legende „Teilliste“.
