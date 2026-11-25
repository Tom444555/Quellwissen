# Quellen der Themen-Ebenen

Rohdaten liegen unter `roh/<thema>/`, Aufbereitung unter `prep/<thema>.py`. Alle Adressen am 25.11.2026 abgerufen bzw. geklont.

| Ebene | Quelle | Adresse | Stand | Lizenz | Was daraus stammt |
|---|---|---|---|---|---|
| vulkane | NOAA NCEI Global Volcano Locations Database (doi:10.7289/V5JW8BSH; Inhalt nach Smithsonian GVP), Kopie `volcano_db.csv` in plotly/datasets | https://raw.githubusercontent.com/plotly/datasets/master/volcano_db.csv | Datei ca. 2010 | CC0 1.0 (laut catalog.data.gov) | Name, Lage, Typ, Höhe, Zeitklasse letzter Ausbruch |
| vulkane | NOAA NCEI/WDS Significant Volcanic Eruptions, Kopie `noaa_volerup.csv` in leestott/intro-Datascience | https://github.com/leestott/intro-Datascience | bis 2019 | US-Regierungswerk, gemeinfrei | Jahr bedeutender Ausbrüche, VEI, Todesopfer, Rang |
| vulkane | Code-Bedeutungen D1–D7/U/? | https://ccgm.org/wp-content/uploads/2013/06/cms_Volcanoes-World_Physiography-Map.pdf | 2013 | Fakten | Zeitklassen-Texte |
| erdbeben | USGS ANSS ComCat, Abfrage M ≥ 7 ab 1900, Schnappschüsse in christophmark/bayesloop | https://github.com/christophmark/bayesloop/tree/master/docs/source/examples/data/web/earthquakes | bis 08.12.2025 | gemeinfrei (USGS) | Datum, Lage, Magnitude, Tiefe |
| erdbeben, Länderzuordnung | Länderflächen der App (`welt_basis.json`, Natural Earth) | – | – | gemeinfrei | iso3 per Punkt-in-Fläche |
| platten | Bird (2003) PB2002, doi:10.1029/2001GC000252; Shapefiles von Hugo Ahlenius/Nordpil | https://github.com/fraxen/tectonicplates | 2003/2014 | ODC-BY 1.0 – Nennung „Hugo Ahlenius, Nordpil und Peter Bird“ | Grenzen, Art, Geschwindigkeit, Platten |
| meeresstroemungen | NOAA Ocean currents (Liste der 25 Strömungen, Warm/kalt-Regel) | https://noaa.gov/node/10499 | 11/2026 | gemeinfrei | Auswahl, Namen, warm/kalt |
| meeresstroemungen | Wikipedia (en) „Ocean current“ (Liste je Ozean, einige warm/kalt-Angaben) | https://www.wikiwand.com/en/Ocean_current | 11/2026 | CC BY-SA 4.0 – nur Fakten | Ergänzungen (Falkland, Guinea, Mosambik, Somali, Alaska warm) |
| windguertel | NOAA JetStream „Global Atmospheric Circulations“ | https://www.noaa.gov/jetstream/global-circulations | 11/2026 | gemeinfrei | Westwinde 35–60°, Hochdruck 30°, Tiefdruck 0°/50–60° |
| windguertel | NOAA Ocean Service „What are the trade winds?“ | https://oceanservice.noaa.gov/facts/tradewinds.html | 11/2026 | gemeinfrei | Passate, Richtungen, Kalmen ±5° |
| windguertel | IPCC AR6 WGI Annex V „Monsoons“ | https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Annex_V.pdf | 2021 | nur Gliederung/Namen | 6 Monsunregionen |
| klima_raster | NCEP/NCAR Reanalysis 1, Monthly LTM air.sig995 1981–2010 (NOAA PSL), Kopie in bird-house/birdhouse-workshop | https://github.com/bird-house/birdhouse-workshop (data/air.mon.ltm.nc) | 1981–2010 | NOAA PSL, ohne Einschränkung; Nennung „NCEP Reanalysis data provided by the NOAA PSL, Boulder, Colorado, USA“ | Temperaturen |
| klima_raster | GPCP v2.2 (Huffman et al. 2009), Kopie in NCAR/geocat-datafiles | https://github.com/NCAR/geocat-datafiles (netcdf_files/V22_GPCP.1979-2010.nc) | 1979–2010 | gemeinfrei (NASA), Zitierung erbeten | Niederschlag |
| biome | RESOLVE Ecoregions 2017 (Dinerstein et al. 2017, BioScience 67:534), vereinfachte TopoJSON in CG-SO/mfl-living-landscapes | https://github.com/CG-SO/mfl-living-landscapes (data/ecoregions.js) | 2017 | CC BY 4.0 | Biom je 2°-Zelle |
| waldanteil | FAO FRA 2020 über Our World in Data | https://github.com/owid/owid-datasets (Forest land, deforestation and change (FAO, 2020)) | 2020 | CC BY 4.0 (OWID) | Waldanteil % |
| pflanzen_heimat | WCVP v16 (Govaerts 2026, Kew, doi:10.34885/nswv-8994), Schnappschuss in matildabrown/rWCVPdata | https://github.com/matildabrown/rWCVPdata | 04.06.2026 | Daten CC BY 4.0 (Kew); R-Paket GPL – nur Daten genutzt | Heimat/eingebürgert je Art |
| pflanzen_heimat | TDWG WGSRPD 2. Aufl. (Stufe 4 mit ISO-Codes) | https://github.com/tdwg/wgsrpd | 2001 | TDWG-Standard (keine ausdrückliche Lizenz) | Zuordnung botanisches Land → ISO3 |
| sternbilder | d3-celestial (Olaf Frohn), Daten nach XHIP/Hipparcos und IAU | https://github.com/ofrohn/d3-celestial | Repo 2026, J2000 | BSD-3-Clause, Copyright (c) 2015 Olaf Frohn | Sterne, Linien, deutsche Sternbildnamen |
| sonnenfinsternisse | astronomy-engine (Don Cross), pip-Paket | https://github.com/cosinekitty/astronomy | Paket 2.1.x | MIT (Software), Ergebnis eigene Rechnung | alle Werte |
| sonnenfinsternisse (Prüfung) | NASA Eclipse Web Site (F. Espenak): Eclipses During 2026 / 2027 | https://eclipse.gsfc.nasa.gov/OH/OH2026.html , https://eclipse.gsfc.nasa.gov/OH/OH2027.html | 11/2026 | gemeinfrei | Abgleich |
| Sonnenstand-Formel | NOAA GML „General Solar Position Calculations“ (Spencer 1971) | https://gml.noaa.gov/grad/solcalc/ (Adresse nicht abgerufen, aus Kenntnis) | – | gemeinfrei | Formel – Koeffizienten durch Vergleich mit astronomy-engine bestätigt |
| kreise | VG250 Stand 01.01.2026, © GeoBasis-DE / BKG (2026), vereinfacht in c9wy4794zz-cmyk/kreisgrenzen | https://github.com/c9wy4794zz-cmyk/kreisgrenzen | 01.01.2026 | dl-de/by-2-0 | Grenzen, Namen, Art |
| kreise | Destatis Gemeindeverzeichnis (GV-ISys) „Kreisfreie Städte und Landkreise nach Fläche, Bevölkerung …“, übernommen in Chillchamp1/lab | https://github.com/Chillchamp1/lab/tree/main/bevoelkerung-kreise | 31.12.2024 | dl-de/by-2-0, Quelle Statistisches Bundesamt | Einwohner, amtliche Fläche |
| schutzgebiete | BfN Nationalparke 2025 / Biosphärenreservate 2025 (Übersichten) | https://www.bfn.de/sites/default/files/2025-03/Nationalparke2025_pac.pdf , https://www.bfn.de/sites/default/files/2025-03/Biosph%C3%A4renreservate2025_pac.pdf | März 2025 | amtl. Fakten | Flächen |
| schutzgebiete | BfN Tabelle Biosphärenreservate 2021 | https://www.bfn.de/sites/default/files/2021-07/BR_Tab_01_2021_bf.pdf | 2021 | amtl. Fakten | Länder, UNESCO-Jahr |
| schutzgebiete | lernhelfer.de (Duden) Nationalparks | https://www.lernhelfer.de/schuelerlexikon/biologie/artikel/nationalparks | 11/2026 | nur Jahreszahlen | Gründungsjahre (Schwarzwald 2014, Hunsrück-Hochwald 2015 nach Land BW/Wikipedia) |
| schutzgebiete | Wikidata, abgefragt 01.09.2026, in Abrechen2/TravStats | https://github.com/Abrechen2/TravStats (backend/src/seedData) | 01.09.2026 | CC0 | Lagepunkte, Q-Nummern |
| wanderwege | GeoNames cities1000 (Kopie im pip-Paket reverse_geocoder) | https://www.geonames.org/ | Paketstand | CC BY 4.0 | Ortskoordinaten |
| wanderwege | Stadt Ruhla (Rennsteig), Top Trails of Germany (Westweg-Factsheet), Projektbüro Saar-Hunsrück-Steig, Tourismusverband Sächsische Schweiz (Malerweg), ADAC „16 schönste Wanderwege“, Wikivoyage „Wandern in Deutschland“ | siehe `quellen_wege` in wanderwege.json | 11/2026 | nur Fakten | Länge, Start/Ziel, belegte Orte |
| wein_hopfen | DWI „Deutscher Wein Statistik 2025“, Übersicht 3 (nach Destatis) | https://www.deutscheweine.de/fileadmin/DWI/News_Medien/Publikationen/Deutscher_Wein_Statistik/Statistik_2025.pdf | 03.06.2024 | Fakten (Destatis dl-de/by-2-0) | Rebflächen |
| wein_hopfen | Destatis Weinerzeugung 2025 nach Anbaugebieten | https://www.destatis.de/EN/Themes/Economic-Sectors-Enterprises/Agriculture-Forestry-Fisheries/Wine/Tables/wine-production-abg.html | 30.03.2026 | dl-de/by-2-0 | Weinmengen |
| wein_hopfen | Verband Deutscher Hopfenpflanzer „Der Hopfen“ (04/2026), Pressestatement 12/2025 | https://www.deutscher-hopfen.de/wp-content/uploads/2026/04/Der-Hopfen.pdf | 2025 | nur Zahlen | Hopfenflächen |
| heilbaeder | Nds. Sozialministerium: Staatlich anerkannte Kur- und Erholungsorte | https://www.ms.niedersachsen.de/download/48949/Staatlich_anerkannte_Kur-_und_Erholungsorte_in_Niedersachsen.pdf | 13.04.2026 | amtl. Verzeichnis | Orte, Prädikate |
| heilbaeder | Bayer. StMI: Verzeichnis der Kurorte | https://stmi.bayern.de/assets/stmi/kub/aktuelles_verzeichnis_kurorte_stand_januar_2020.pdf | 02.01.2020 | amtl. Verzeichnis | Orte, Prädikate |
| heilbaeder | NRW: Verzeichnis der staatlichen Anerkennungen von Kurorten, Erholungsorten und Heilbrunnen | https://recht.nrw.de/lrmb/bekanntmachung/verzeichnis-der-staatlichen-anerkennungen-von-kurorten-erholungsorten-und/ | 22.07.2026 (letzte Änderung) | amtl. Verzeichnis | Orte, Prädikate |
| heilbaeder | Sachsen: Staatlich anerkannte Kurorte im Freistaat Sachsen (REVOSax, Anlage) | https://revosax.sachsen.de/attachments/32309 | 11.09.2019 | amtl. Verzeichnis | Orte, Prädikate |

Nicht verwendet (Lizenz): Smithsonian GVP direkt (Nutzungsbedingungen verbieten kommerzielle Nutzung), Berkeley-Earth-Länderwerte (CC BY-NC), WorldClim (nur nicht kommerziell), Stellarium-Sternnamen-Übersetzungen (GPL; deshalb eigene deutsche Formen nur für 10 bekannte Sterne).
