"""Ebenen 'energie_leitungen' (schematische Öl-/Gas-Pipelines) und 'energie_engstellen' (Seewege/Engstellen nach US EIA)."""
import sys
sys.path.insert(0, '/home/claude/scratch/themen/b/prep')
from gemein import *

P = []


def pl(n, stoff, jahr, kap, status, st, laender, teile, t, rang, q):
    P.append({'n': n, 'stoff': stoff, 'jahr': jahr, 'kap': kap, 'status': status, 'st': st, 'laender': laender.split(),
              'linien': [[[r2(a), r2(b)] for a, b in tl] for tl in teile], 't': t, 'rang': rang, 'schema': True, 'q': q})


# st: in Betrieb | eingeschränkt | außer Betrieb | zerstört | geplant | im Bau
BAL = [(26.0, 60.0), (23.0, 59.6), (21.0, 58.9), (19.9, 57.8), (18.8, 56.5), (16.5, 55.6), (15.6, 55.1), (14.5, 54.6)]
pl('Nord Stream 1', 'gas', 2011, '55 Mrd. m³/Jahr (2 Stränge)', 'Seit 31.08.2022 keine Lieferung; am 26.09.2022 beide Stränge durch Explosionen bei Bornholm zerstört.', 'zerstört',
   'RUS DEU', [[(28.7, 60.55)] + BAL + [(13.65, 54.14)]], 'Gasleitung durch die Ostsee von Wyborg nach Lubmin.', 1, 'Nord Stream AG; Bundesregierung; schwedische und dänische Behörden 2022/2024')
pl('Nord Stream 2', 'gas', 2021, '55 Mrd. m³/Jahr (2 Stränge)', 'Nie in Betrieb genommen (Zertifizierung im Februar 2022 gestoppt); am 26.09.2022 ein Strang zerstört, ein Strang intakt.', 'außer Betrieb',
   'RUS DEU', [[(28.3, 59.68), (26.0, 59.85)] + BAL[1:] + [(13.65, 54.14)]], 'Zweite Ostsee-Leitung von Ust-Luga nach Lubmin.', 1, 'Nord Stream 2 AG; Bundesnetzagentur 2022')
pl('OPAL', 'gas', 2011, '36 Mrd. m³/Jahr', 'Anschlussleitung von Nord Stream; seit 2022 kaum genutzt.', 'eingeschränkt',
   'DEU CZE', [[(13.65, 54.14), (14.0, 52.9), (14.3, 51.5), (13.6, 50.9), (13.42, 50.56)]], 'Ostsee-Pipeline-Anbindungsleitung von Lubmin zur tschechischen Grenze.', 3, 'GASCADE')
pl('Jamal–Europa', 'gas', 1999, '33 Mrd. m³/Jahr', 'Seit 2022 kein russisches Gas mehr in Richtung Westen.', 'außer Betrieb',
   'RUS BLR POL DEU', [[(34.97, 57.04), (30.5, 54.5), (26.67, 53.22), (23.5, 52.6), (19.0, 52.4), (14.55, 52.35)]], 'Gasleitung über Belarus und Polen nach Deutschland.', 2, 'Gazprom; EuRoPol GAZ')
pl('Ukrainisches Transitsystem (Bruderschaft)', 'gas', 1967, 'bis über 100 Mrd. m³/Jahr (historisch)', 'Russischer Gastransit durch die Ukraine endete am 01.01.2025 mit Ablauf des Transitvertrags.', 'außer Betrieb',
   'RUS UKR SVK', [[(35.53, 51.19), (31.0, 50.2), (26.5, 49.5), (22.29, 48.62), (21.95, 48.5)]], 'Leitungsnetz von der russischen Grenze (Sudscha) nach Uschhorod und in die Slowakei.', 2, 'Gas Transmission System Operator of Ukraine; EU-Kommission 2025')
pl('TurkStream', 'gas', 2020, '31,5 Mrd. m³/Jahr (2 Stränge)', 'In Betrieb; seit 2025 einziger Weg für russisches Pipelinegas in die EU.', 'in Betrieb',
   'RUS TUR BGR SRB HUN', [[(37.3, 44.9), (33.0, 43.5), (29.0, 41.9), (28.1, 41.63)], [(28.1, 41.63), (26.9, 42.2), (23.3, 43.3), (21.0, 44.8), (20.07, 46.28)]],
   'Gasleitung durch das Schwarze Meer in die Türkei, ein Strang weiter über Bulgarien und Serbien nach Ungarn.', 1, 'TurkStream (South Stream Transport B.V.); Gazprom')
pl('Blue Stream', 'gas', 2003, '16 Mrd. m³/Jahr', 'In Betrieb.', 'in Betrieb', 'RUS TUR', [[(38.7, 44.32), (37.5, 43.0), (36.33, 41.29), (32.85, 39.93)]], 'Gasleitung durch das Schwarze Meer nach Samsun und Ankara.', 3, 'Gazprom; BOTAŞ')
pl('Südkaukasus-Pipeline – TANAP – TAP (Südlicher Gaskorridor)', 'gas', 2020, 'TANAP 16, TAP 10 Mrd. m³/Jahr', 'In Betrieb; Erweiterung von TAP läuft.', 'in Betrieb',
   'AZE GEO TUR GRC ALB ITA', [[(49.47, 40.18), (47.0, 41.0), (44.79, 41.72), (42.73, 41.5), (41.27, 39.9), (36.0, 39.5), (30.5, 39.78), (26.37, 40.92)],
                               [(26.37, 40.92), (24.5, 41.0), (22.5, 40.7), (20.5, 40.6), (19.56, 40.72), (18.37, 40.27)]],
   'Gas aus dem Kaspischen Meer (Schah Denis) über Georgien und die Türkei nach Griechenland, Albanien und Italien.', 1, 'TANAP; TAP AG; bp')
pl('Baku–Tiflis–Ceyhan (BTC)', 'oel', 2006, 'ca. 1,2 Mio. Barrel/Tag', 'In Betrieb.', 'in Betrieb', 'AZE GEO TUR',
   [[(49.47, 40.18), (47.0, 41.0), (44.79, 41.72), (42.7, 41.1), (41.27, 39.9), (38.3, 38.4), (35.8, 36.88)]], 'Ölleitung vom Kaspischen Meer zum Mittelmeer.', 1, 'bp (Betreiber BTC Co.)')
pl('Druschba', 'oel', 1964, 'ca. 1,2–2 Mio. Barrel/Tag (je nach Abschnitt)', 'Südstrang nach Ungarn und Slowakei: nach Unterbrechung Anfang 2026 seit April 2026 wieder in Betrieb. Nordstrang: Deutschland bezieht seit 2023 kein russisches Öl, über die Leitung kommt kasachisches Öl nach Schwedt. Tschechien bezieht seit April 2025 kein russisches Öl mehr (Versorgung über TAL).', 'eingeschränkt',
   'RUS BLR POL DEU UKR SVK HUN CZE', [[(52.3, 54.9), (42.0, 53.5), (32.67, 52.85), (29.25, 52.05), (23.7, 52.1), (19.7, 52.55), (14.27, 53.08)],
                                      [(29.25, 52.05), (25.15, 50.08), (22.29, 48.62), (21.0, 48.5), (18.92, 47.32)], [(21.0, 48.5), (17.1, 48.15)], [(17.1, 48.15), (16.9, 48.8), (14.31, 50.24)]],
   'Längstes Ölleitungssystem der Welt, von Tatarstan nach Mitteleuropa.', 1, 'Transneft; The Moscow Times 16.02.2026 (Unterbrechung ab 27.01.2026); intellinews 04.06.2026 (Lieferungen seit April, im Mai normal); OSW 18.04.2025 / tschechische Regierung (Tschechien)')
pl('Kraft Sibiriens (Power of Siberia)', 'gas', 2019, '38 Mrd. m³/Jahr', 'In Betrieb. „Kraft Sibiriens 2“ über die Mongolei ist geplant.', 'in Betrieb', 'RUS CHN',
   [[(108.5, 60.9), (115.5, 58.5), (123.9, 54.0), (127.0, 51.5), (127.53, 50.26), (126.0, 46.0), (123.4, 41.8), (119.6, 39.9), (117.0, 38.0), (118.0, 36.0), (119.0, 34.0), (120.3, 32.0), (121.47, 31.23)]], 'Gasleitung aus Ostsibirien nach Nordostchina.', 1, 'Gazprom; CNPC')
pl('Zentralasien–China', 'gas', 2009, 'ca. 55 Mrd. m³/Jahr (Linien A–C)', 'In Betrieb.', 'in Betrieb', 'TKM UZB KAZ CHN',
   [[(62.3, 37.4), (64.4, 39.8), (69.3, 41.3), (69.6, 42.3), (71.4, 42.9), (73.8, 43.6), (75.5, 43.9), (77.1, 43.9), (80.4, 44.2), (87.6, 43.8)]], 'Gas aus Turkmenistan über Usbekistan und Kasachstan nach China.', 2, 'CNPC')
pl('Ostsibirien–Pazifik (ESPO)', 'oel', 2009, 'ca. 1,6 Mio. Barrel/Tag', 'In Betrieb.', 'in Betrieb', 'RUS CHN',
   [[(98.0, 55.94), (108.0, 56.8), (115.0, 57.5), (123.9, 54.0), (128.47, 50.92), (130.08, 49.42), (131.05, 49.0), (132.93, 48.79), (135.07, 48.48), (134.0, 46.0), (133.07, 42.73)], [(123.9, 54.0), (124.5, 50.0), (125.0, 46.6)]],
   'Ölleitung von Taischet zum Pazifikhafen Kosmino mit Abzweig nach Daqing (China).', 2, 'Transneft')
pl('Kaspisches Pipeline-Konsortium (CPC)', 'oel', 2001, 'ca. 1,5 Mio. Barrel/Tag', 'In Betrieb; 2025 mehrfach durch Drohnenangriffe beeinträchtigt.', 'in Betrieb', 'KAZ RUS',
   [[(53.38, 46.15), (51.9, 47.1), (50.0, 47.25), (48.0, 46.9), (47.0, 46.3), (42.0, 45.0), (37.77, 44.72)]], 'Ölleitung vom Tengis-Feld zum Schwarzmeerhafen Noworossijsk.', 2, 'CPC')
pl('Kasachstan–China (Öl)', 'oel', 2006, 'ca. 0,4 Mio. Barrel/Tag', 'In Betrieb.', 'in Betrieb', 'KAZ CHN', [[(51.9, 47.1), (57.2, 48.2), (65.5, 46.4), (74.0, 46.0), (82.57, 45.17)]], 'Ölleitung von Atyrau nach Alashankou.', 3, 'KazTransOil; CNPC')
pl('Myanmar–China', 'beides', 2013, 'Gas 12 Mrd. m³/Jahr, Öl ca. 0,44 Mio. Barrel/Tag', 'In Betrieb.', 'in Betrieb', 'MMR CHN',
   [[(93.55, 19.43), (94.8, 20.6), (96.08, 21.97), (97.85, 24.0), (100.2, 25.6), (102.71, 25.04)]], 'Parallele Öl- und Gasleitung vom Golf von Bengalen nach Kunming.', 3, 'CNPC')
pl('Transmed', 'gas', 1983, 'ca. 33 Mrd. m³/Jahr', 'In Betrieb.', 'in Betrieb', 'DZA TUN ITA',
   [[(3.27, 32.93), (6.0, 34.5), (9.0, 35.5), (11.05, 37.07), (12.59, 37.65), (13.8, 38.3), (15.6, 38.2), (16.5, 40.0), (14.0, 42.0), (11.5, 44.6)]],
   'Gasleitung von Algerien über Tunesien und Sizilien nach Italien.', 2, 'Sonatrach; Eni/Snam')
pl('Medgaz', 'gas', 2011, '10,5 Mrd. m³/Jahr', 'In Betrieb.', 'in Betrieb', 'DZA ESP', [[(3.27, 32.93), (0.5, 34.0), (-1.39, 35.3), (-2.46, 36.84)]], 'Gasleitung von Algerien direkt nach Almería.', 3, 'Medgaz S.A.')
pl('Maghreb–Europa (GME)', 'gas', 1996, '12 Mrd. m³/Jahr', 'Algerisches Gas fließt seit November 2021 nicht mehr; seit 2022 Lieferungen von Spanien nach Marokko in Gegenrichtung.', 'eingeschränkt',
   'DZA MAR ESP', [[(3.27, 32.93), (-1.0, 34.0), (-5.0, 34.5), (-5.8, 35.7), (-5.6, 36.0), (-6.0, 37.0)]], 'Gasleitung über Marokko und die Straße von Gibraltar nach Spanien.', 3, 'Enagás; Reuters 2021/2022')
pl('Greenstream', 'gas', 2004, '8 Mrd. m³/Jahr', 'In Betrieb (unregelmäßig).', 'in Betrieb', 'LBY ITA', [[(12.2, 32.87), (13.5, 35.0), (14.25, 37.07)]], 'Gasleitung von Mellitah (Libyen) nach Gela (Sizilien).', 3, 'Eni')
pl('Langeled', 'gas', 2007, 'ca. 25 Mrd. m³/Jahr', 'In Betrieb.', 'in Betrieb', 'NOR GBR', [[(6.97, 62.83), (4.5, 61.0), (2.5, 58.5), (1.5, 56.0), (0.05, 53.66)]], 'Gasleitung von Nyhamna nach Easington.', 3, 'Gassco')
pl('Norpipe / Europipe', 'gas', 1977, 'Europipe I+II je ca. 18–24, Norpipe 16 Mrd. m³/Jahr', 'In Betrieb.', 'in Betrieb', 'NOR DEU',
   [[(3.2, 56.5), (5.5, 55.0), (7.2, 53.36)], [(5.5, 59.27), (4.0, 57.5), (5.8, 55.0), (7.43, 53.65)]], 'Gasleitungen von norwegischen Feldern nach Emden und Dornum.', 2, 'Gassco')
pl('Baltic Pipe', 'gas', 2022, '10 Mrd. m³/Jahr', 'In Betrieb seit Oktober 2022.', 'in Betrieb', 'NOR DNK POL',
   [[(4.6, 57.0), (8.2, 55.6), (10.0, 55.4), (12.0, 55.25), (13.5, 54.9), (15.08, 54.06)]], 'Gasleitung von der Nordsee über Dänemark nach Polen.', 3, 'Energinet; GAZ-SYSTEM')
pl('Arabische Gaspipeline', 'gas', 2003, '10 Mrd. m³/Jahr', 'Teilweise in Betrieb.', 'eingeschränkt', 'EGY JOR SYR LBN',
   [[(33.8, 31.13), (34.5, 30.0), (34.85, 29.45), (35.0, 29.53), (36.0, 31.5), (36.3, 32.6), (36.72, 34.73), (35.9, 34.45)]], 'Gasleitung von Ägypten über Jordanien nach Syrien und in den Libanon.', 3, 'EIA Country Analysis Brief Egypt')
pl('Dolphin', 'gas', 2007, 'ca. 2 Mrd. Kubikfuß/Tag', 'In Betrieb.', 'in Betrieb', 'QAT ARE OMN', [[(51.53, 25.9), (53.0, 25.2), (54.7, 24.77)], [(54.7, 24.77), (55.3, 24.75), (55.8, 25.1), (56.33, 25.12)], [(54.7, 24.77), (55.75, 24.22), (55.8, 24.25)]], 'Gasleitung von Ras Laffan (Katar) nach Taweelah (Abu Dhabi), weiter nach Fudschaira und über Al Ain nach Oman.', 3, 'Dolphin Energy; Oil & Gas Journal 06.11.2008 (Oman über Al Ain)')
pl('East-West-Pipeline (Petroline)', 'oel', 1981, 'ca. 5 Mio. Barrel/Tag (Auslegung, nicht amtlich bestätigt); laut EIA mit ADCOP zusammen rund 4,7 Mio. Barrel/Tag zur Umgehung von Hormus verfügbar', 'In Betrieb; Umgehung der Straße von Hormus zum Roten Meer.', 'in Betrieb', 'SAU',
   [[(49.68, 25.93), (46.7, 24.7), (42.0, 24.5), (38.06, 24.09)]], 'Ölleitung von Abqaiq nach Yanbu.', 1, 'EIA World Oil Transit Chokepoints; Saudi Aramco')
pl('Habshan–Fudschaira (ADCOP)', 'oel', 2012, 'ca. 1,5 Mio. Barrel/Tag', 'In Betrieb; Umgehung der Straße von Hormus.', 'in Betrieb', 'ARE',
   [[(53.6, 23.8), (54.6, 24.3), (55.3, 24.75), (55.8, 25.1), (56.33, 25.12)]], 'Ölleitung zum Hafen Fudschaira am Golf von Oman.', 2, 'EIA World Oil Transit Chokepoints')
pl('SUMED', 'oel', 1977, 'ca. 2,5 Mio. Barrel/Tag', 'In Betrieb; Alternative zum Suezkanal.', 'in Betrieb', 'EGY', [[(32.35, 29.6), (31.2, 30.2), (29.68, 31.08)]], 'Ölleitung vom Golf von Suez zum Mittelmeer.', 3, 'EIA World Oil Transit Chokepoints')
pl('Kirkuk–Ceyhan', 'oel', 1977, 'ca. 1,2 Mio. Barrel/Tag (Reuters)', 'Exporte 03/2023–09/2025 gestoppt; Anfang März 2026 erneut unterbrochen, nach Einigung Bagdad–Erbil vom 17.03.2026 wieder rund 250.000 Barrel/Tag (Stand 20.03.2026).', 'eingeschränkt', 'IRQ TUR',
   [[(44.39, 35.47), (43.1, 36.6), (42.45, 37.2), (42.0, 37.4), (41.2, 37.4), (40.0, 37.45), (38.8, 37.35), (37.4, 37.25), (36.3, 37.1), (35.8, 36.88)]], 'Ölleitung aus dem Nordirak zum türkischen Mittelmeerhafen.', 3, 'The National 16./18.03.2026 (nach Reuters); Shafaq News 20.03.2026 (North Oil Company)')
pl('Tschad–Kamerun', 'oel', 2003, 'ca. 0,23 Mio. Barrel/Tag', 'In Betrieb.', 'in Betrieb', 'TCD CMR', [[(16.85, 8.66), (14.5, 7.0), (12.0, 4.5), (9.9, 2.94)]], 'Ölleitung von Doba zum Atlantikhafen Kribi.', 3, 'Weltbank-Projektunterlagen; TOTCO/COTCO')
pl('Trans-Alaska-Pipeline', 'oel', 1977, 'ausgelegt ca. 2,1 Mio. Barrel/Tag, heute rund 0,5 Mio.', 'In Betrieb.', 'in Betrieb', 'USA',
   [[(-148.34, 70.26), (-148.7, 68.0), (-149.5, 65.5), (-147.7, 64.8), (-145.7, 63.0), (-146.35, 61.13)]], 'Ölleitung von Prudhoe Bay nach Valdez.', 1, 'Alyeska Pipeline Service Co.')
pl('Keystone', 'oel', 2010, 'ca. 0,62 Mio. Barrel/Tag', 'In Betrieb; die Erweiterung Keystone XL wurde 2021 aufgegeben.', 'in Betrieb', 'CAN USA',
   [[(-111.3, 52.67), (-104.0, 49.0), (-97.02, 40.0), (-95.0, 39.0), (-89.1, 38.75)], [(-97.02, 40.0), (-96.77, 35.98), (-95.5, 31.5), (-93.93, 29.88)]],
   'Ölleitung von Alberta nach Illinois und an den Golf von Mexiko.', 2, 'TC Energy / South Bow')
pl('Trans Mountain', 'oel', 1953, 'ca. 0,89 Mio. Barrel/Tag (seit Erweiterung 2024)', 'In Betrieb.', 'in Betrieb', 'CAN',
   [[(-113.49, 53.55), (-118.0, 53.0), (-120.33, 50.67), (-122.95, 49.28)]], 'Ölleitung von Edmonton an die Pazifikküste bei Vancouver.', 3, 'Trans Mountain Corporation')
pl('Colonial Pipeline', 'oel', 1963, 'ca. 2,5 Mio. Barrel/Tag (Ölprodukte)', 'In Betrieb.', 'in Betrieb', 'USA',
   [[(-95.37, 29.76), (-91.0, 30.5), (-86.8, 33.5), (-84.4, 33.75), (-80.8, 35.2), (-77.4, 37.5), (-76.6, 39.3), (-74.24, 40.63)]], 'Größte Produktenleitung der USA (Benzin, Diesel, Kerosin) von Houston nach New Jersey.', 3, 'Colonial Pipeline Co.')
print(len(P))
obj = {'id': 'energie_leitungen', 'name': 'Öl- und Gasleitungen', 'gruppe': 'Wirtschaft', 'typ': 'linien', 'einheit': '',
       'legende': [{'k': 'gas', 'n': 'Gasleitung', 'c': '#5fb8ff'}, {'k': 'oel', 'n': 'Ölleitung', 'c': '#ff8a3d'}, {'k': 'beides', 'n': 'Öl und Gas', 'c': '#d0a0ff'},
                   {'k': 'zerstört', 'n': 'zerstört/außer Betrieb (gestrichelt)', 'c': '#8a8a8a'}],
       'quellen': [{'t': 'Betreiberangaben (Feld q je Leitung); US EIA World Oil Transit Chokepoints (gemeinfrei)', 'u': 'https://www.eia.gov/international/content/analysis/special_topics/World_Oil_Transit_Chokepoints',
                    'stand': '11/2026', 'lizenz': 'Fakten; EIA gemeinfrei'},
                   {'t': 'Druschba-Status: intellinews / The Moscow Times (April 2026)', 'u': 'https://www.themoscowtimes.com/2026/04/23/druzhba-oil-flow-to-slovakia-resumed-thursday-officials-say-a92580/pdf', 'stand': '04/2026', 'lizenz': 'Fakten'}],
       'hinweis': 'Alle Verläufe schematisch über grobe Wegpunkte (keine Trassendaten). Kapazitäten = Auslegung laut Betreiber, nicht tatsächlicher Durchfluss.',
       'felder': {'stoff': 'gas | oel | beides', 'jahr': 'Inbetriebnahme', 'kap': 'Kapazität (Text)', 'status': 'Status-Text mit Datum', 'st': 'Status-Schlüssel',
                  'laender': 'durchquerte Staaten (ISO3)', 'linien': 'Linienzüge', 'rang': '1–3', 'q': 'Beleg'},
       'daten': P}
schreibe(obj)

E = 'US EIA, World Oil Transit Chokepoints (Stand 03.03.2026), Tabelle 1'
ENG = [
 ['Straße von Hormus', 'IRN', 56.45, 26.57, 20.9, 11.4, 1, 'Wichtigste Öl-Engstelle der Welt, rund ein Fünftel des weltweiten Ölverbrauchs. 2026: im 2. Quartal nach Beginn des Konflikts mit Iran stark eingeschränkt, im 3. Quartal wieder steigend (EIA, 19.11.2026).'],
 ['Straße von Malakka', 'MYS', 101.0, 2.6, 23.2, 9.2, 1, 'Kürzester Seeweg zwischen Indischem Ozean und Pazifik; nach Ölmenge größte Engstelle.'],
 ['Suezkanal und SUMED-Pipeline', 'EGY', 32.35, 30.6, 4.9, 0.9, 1, 'Seit den Angriffen im Roten Meer ab Ende 2023 stark gesunken (2023: 8,8 Mio. b/Tag).'],
 ['Bab al-Mandab', 'YEM', 43.33, 12.58, 4.2, 0.0, 1, 'Meerenge zwischen Jemen und Dschibuti/Eritrea; seit 2024 viele Schiffe umgeleitet (2023: 9,3 Mio. b/Tag).'],
 ['Dänische Meerengen', 'DNK', 10.95, 55.35, 4.9, 1.6, 2, 'Ausgang der Ostsee, wichtig für russische Ölexporte.'],
 ['Türkische Meerengen – Bosporus', 'TUR', 29.05, 41.12, 3.3, None, 2, 'Verbindung Schwarzes Meer–Mittelmeer; Flüssiggastanker dürfen den Bosporus nicht passieren.'],
 ['Türkische Meerengen – Dardanellen', 'TUR', 26.4, 40.2, 3.7, 0.6, 3, 'Südlicher Teil der Türkischen Meerengen.'],
 ['Panamakanal', 'PAN', -79.75, 9.1, 2.3, 0.3, 2, 'Wert für das Fiskaljahr 2025 (Oktober–September); LNG unter 0,3 Mrd. Kubikfuß/Tag.'],
 ['Kap der Guten Hoffnung', 'ZAF', 18.47, -34.6, 9.1, 5.7, 1, 'Keine Engstelle, aber Ausweichroute um Afrika; seit 2024 deutlich mehr Verkehr.'],
 ['Straße von Gibraltar', 'ESP', -5.6, 35.96, None, None, 2, 'Einfahrt ins Mittelmeer; von der EIA nicht gesondert beziffert.'],
]
daten = []
for n, c, lo, la, oel, lng, rg, t in ENG:
    daten.append({'n': n, 'land': c, 'lon': r2(lo), 'lat': r2(la), 'oel': oel, 'lng': lng, 'jahr': '1. Halbjahr 2025', 'rang': rg, 't': t, 'see': True})
obj = {'id': 'energie_engstellen', 'name': 'Seewege & Engstellen (Öl/LNG)', 'gruppe': 'Wirtschaft', 'typ': 'punkte', 'einheit': 'Öl: Mio. Barrel/Tag; LNG: Mrd. Kubikfuß/Tag',
       'legende': {'groesse': 'Kreisfläche nach Öldurchfluss', 'c': '#ffcf5a'},
       'quellen': [{'t': E, 'u': 'https://www.eia.gov/international/content/analysis/special_topics/World_Oil_Transit_Chokepoints', 'stand': '03/2026 (Werte 1. Halbjahr 2025)', 'lizenz': 'gemeinfrei (US-Regierung)'},
                   {'t': 'US EIA, Today in Energy „Oil flows through Middle East chokepoints increased in the third quarter“ (19.11.2026)', 'u': 'https://www.eia.gov/todayinenergy/detail.php?id=68485', 'stand': '11/2026', 'lizenz': 'gemeinfrei (US-Regierung)'}],
       'hinweis': 'Öl = Rohöl und Ölprodukte (Mio. Barrel/Tag), LNG = Flüssigerdgas (Mrd. Kubikfuß/Tag), jeweils 1. Halbjahr 2025 laut EIA. Seekabel nicht enthalten (siehe OFFEN.md).',
       'felder': {'oel': 'Mio. Barrel/Tag', 'lng': 'Mrd. Kubikfuß/Tag (null = nicht angegeben)', 'land': 'angrenzender Staat (nur Zuordnung)', 'see': 'Punkt liegt auf See'},
       'daten': daten}
schreibe(obj)
