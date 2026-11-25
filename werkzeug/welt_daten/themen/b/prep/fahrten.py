"""Ebene 'entdeckungsfahrten': schematische Routen großer Reisen (ergänzt ERF = Erfindungen und WANDER = Wanderungen;
dort gibt es keine Einzelreisen, nur die Wikinger allgemein)."""
import sys
sys.path.insert(0, '/home/claude/scratch/themen/b/prep')
from gemein import *

F = []


def fahrt(n, wer, von, bis, t, c, rang, teile, orte, q):
    lin = [[[r2(lo), r2(la)] for lo, la in tl] for tl in teile]
    F.append({'n': n, 'wer': wer, 'von': von, 'bis': bis, 't': t, 'c': c, 'rang': rang, 'schema': True, 'linien': lin,
              'orte': [[o, r2(lo), r2(la)] for o, lo, la in orte], 'q': q})


fahrt('Erste Fahrt des Kolumbus', 'Christoph Kolumbus', 1492, 1493,
      'Mit drei Schiffen von Spanien westwärts; Landung am 12. Oktober 1492 auf den Bahamas (Guanahani), danach Kuba und Hispaniola.', '#ffcf5a', 1,
      [[(-6.89, 37.23), (-12, 33), (-17.11, 28.09), (-40, 27), (-65, 25.5), (-74.5, 24.05), (-77, 21.6), (-72, 19.9)],
       [(-72, 19.9), (-68, 19.8), (-55, 33), (-25.1, 36.95), (-9.14, 38.71), (-6.89, 37.23)]],
      [('Palos de la Frontera', -6.89, 37.23), ('La Gomera (Kanaren)', -17.11, 28.09), ('Guanahani (Bahamas)', -74.5, 24.05),
       ('Kuba', -77, 21.6), ('La Navidad (Hispaniola)', -72, 19.9), ('Azoren', -25.1, 36.95), ('Lissabon', -9.14, 38.71)],
      'Britannica „Christopher Columbus“')
fahrt('Bartolomeu Dias umrundet das Kap', 'Bartolomeu Dias', 1487, 1488,
      'Erste europäische Umsegelung der Südspitze Afrikas bis zur Algoa-Bucht; Rückkehr am Kap der Guten Hoffnung vorbei.', '#ffa86a', 3,
      [[(-9.14, 38.71), (-17, 25), (-18, 12), (-16, 8), (-12, 4.5), (-7.5, 3.8), (-2, 4.2), (5, 1), (9.5, -5), (11.5, -12), (11, -18), (14.5, -22.95), (15, -30), (19, -36), (22.14, -34.18), (26.6, -33.7)]],
      [('Lissabon', -9.14, 38.71), ('Walvis-Bucht', 14.5, -22.95), ('Mossel Bay', 22.14, -34.18), ('Kwaaihoek (Algoa-Bucht)', 26.6, -33.7)],
      'Britannica „Bartolomeu Dias“')
fahrt('Seeweg nach Indien', 'Vasco da Gama', 1497, 1499,
      'Erste Seefahrt von Europa um Afrika nach Indien; Ankunft in Kalikut im Mai 1498.', '#ff8a5a', 1,
      [[(-9.14, 38.71), (-17, 25), (-23.5, 15), (-28, 0), (-25, -18), (-10, -30), (18, -32.7), (18.47, -35), (22.14, -34.6), (27, -34.5), (31.5, -31.5), (33, -30), (36, -25), (38, -20),
        (40.73, -15.03), (41.2, -11), (40.2, -6.5), (39.67, -4.05), (40.12, -3.22), (55, 6), (70, 11), (75.78, 11.25)]],
      [('Lissabon', -9.14, 38.71), ('Kapverden', -23.5, 15), ('St.-Helena-Bucht', 18, -32.7), ('Mosambik', 40.73, -15.03),
       ('Mombasa', 39.67, -4.05), ('Malindi', 40.12, -3.22), ('Kalikut', 75.78, 11.25)],
      'Britannica „Vasco da Gama“')
fahrt('Erste Weltumsegelung', 'Ferdinand Magellan, nach dessen Tod Juan Sebastián Elcano', 1519, 1522,
      'Fünf Schiffe brechen auf, eines kehrt 1522 zurück; Magellan fällt 1521 auf den Philippinen.', '#6ad0ff', 1,
      [[(-6.35, 36.78), (-16.25, 28.47), (-25, 5), (-35, -10), (-43.17, -22.9), (-47.5, -28), (-52.5, -34.5), (-56, -35.2), (-56.5, -38.5), (-62, -42.5), (-65.5, -46.5), (-67.72, -49.31), (-67.6, -52.3), (-70.9, -53.3),
        (-76, -52), (-80, -30), (-120, -15), (-180, 5)],
       [(180, 5), (144.75, 13.45), (130, 11), (123.98, 10.3), (125, 5), (127.4, 0.68), (124.5, -9.5), (110, -18), (80, -30), (40, -37),
        (18.47, -35.5), (5, -20), (-15, 0), (-23.5, 15), (-15, 30), (-6.35, 36.78)]],
      [('Sanlúcar de Barrameda', -6.35, 36.78), ('Rio de Janeiro', -43.17, -22.9), ('Puerto San Julián', -67.72, -49.31),
       ('Magellanstraße', -70.9, -53.3), ('Guam', 144.75, 13.45), ('Mactan (Tod Magellans)', 123.98, 10.3), ('Tidore (Molukken)', 127.4, 0.68),
       ('Kap der Guten Hoffnung', 18.47, -34.36)],
      'Britannica „Ferdinand Magellan“')
fahrt('Erste Südseereise James Cooks', 'James Cook', 1768, 1771,
      'Fahrt der Endeavour: Venusdurchgang auf Tahiti 1769, Karte Neuseelands, Ostküste Australiens.', '#8ab8ff', 2,
      [[(-4.14, 50.37), (-16.9, 32.65), (-30, 0), (-43.17, -22.9), (-47, -30), (-55, -40), (-62, -48), (-63, -52), (-65.2, -54.8), (-67.27, -56.5), (-75, -60), (-90, -45), (-130, -25), (-149.43, -17.65),
        (-165, -25), (-180, -32)],
       [(180, -32), (178, -38.7), (174.8, -36.5), (172.7, -34.4), (174, -41.3), (166.5, -46), (160, -40), (151.2, -34), (153.8, -28), (154, -25), (150, -20), (146.5, -17),
        (145.25, -15.46), (144, -14), (143.6, -11.5), (142.5, -10.7), (130, -10.5), (121.9, -10.6), (110, -9), (105.5, -6.6), (106.8, -6.13), (105.5, -6.6), (104, -8), (100, -15), (60, -30), (18.47, -35), (-5.7, -15.95), (-20, 10), (-15, 40), (-6, 49), (-1, 50.3), (1.4, 51.2)]],
      [('Plymouth', -4.14, 50.37), ('Rio de Janeiro', -43.17, -22.9), ('Tahiti', -149.43, -17.65), ('Poverty Bay (Neuseeland)', 178, -38.7),
       ('Botany Bay', 151.2, -34), ('Endeavour River', 145.25, -15.46), ('Batavia (Jakarta)', 106.8, -6.13)],
      'Britannica „James Cook“; Royal Museums Greenwich')
fahrt('Siebte Flottenfahrt Zheng Hes', 'Zheng He', 1431, 1433,
      'Letzte von sieben Fahrten der Ming-Flotte (1405–1433) über Südostasien und Indien bis Arabien und Ostafrika.', '#ff6a6a', 1,
      [[(118.78, 32.06), (121.5, 30), (119.52, 25.96), (114, 20), (109.2, 13.8), (107, 5), (112.75, -6.5), (106, -4), (104.75, -2.99),
        (104.2, 1.3), (102.25, 2.19), (97.5, 5.6), (88, 6), (80.22, 6.03), (76.5, 8), (75.78, 11.25), (66, 20), (58.5, 23.8), (56.46, 27.1)],
       [(75.78, 11.25), (60, 13), (51, 12.2), (45.03, 12.79), (43.3, 12.7), (39.17, 21.49)],
       [(80.22, 6.03), (60, 2), (45.34, 2.04), (40.12, -3.22)]],
      [('Nanjing', 118.78, 32.06), ('Changle', 119.52, 25.96), ('Champa (Qui Nhơn)', 109.2, 13.8), ('Java', 112.75, -6.5), ('Malakka', 102.25, 2.19),
       ('Galle (Sri Lanka)', 80.22, 6.03), ('Kalikut', 75.78, 11.25), ('Hormus', 56.46, 27.1), ('Aden', 45.03, 12.79), ('Dschidda', 39.17, 21.49),
       ('Mogadischu', 45.34, 2.04), ('Malindi', 40.12, -3.22)],
      'Britannica „Zheng He“')
fahrt('Leif Eriksson nach Vinland', 'Leif Eriksson', 1000, 1000,
      'Von Grönland über Helluland und Markland nach Vinland; Wikingersiedlung bei L’Anse aux Meadows archäologisch belegt (um 1021 Holzbearbeitung datiert).', '#a8c8ff', 2,
      [[(-45.5, 61.15), (-55, 63), (-65, 63), (-61, 56.5), (-57, 53), (-55.53, 51.6)]],
      [('Brattahlíð (Grönland)', -45.5, 61.15), ('Helluland (Baffininsel)', -65, 63), ('Markland (Labrador)', -61, 56.5), ('L’Anse aux Meadows', -55.53, 51.6)],
      'Parks Canada „L’Anse aux Meadows“; Kuitems u. a., Nature 601 (2022)')
fahrt('Amerikareise Alexander von Humboldts', 'Alexander von Humboldt, Aimé Bonpland', 1799, 1804,
      'Forschungsreise durch Venezuela, Kuba, Kolumbien, Ecuador, Peru und Mexiko; Besteigungsversuch des Chimborazo 1802.', '#9ae0c0', 2,
      [[(-8.4, 43.37), (-16.25, 28.47), (-40, 15), (-64.17, 10.46), (-66.9, 10.5)],
       [(-66.9, 10.5), (-67.5, 7.9), (-67.6, 5.6), (-66.5, 2.5), (-64.5, 4), (-63.55, 8.12), (-64.17, 10.46)],
       [(-64.17, 10.46), (-75, 16), (-82.36, 23.13), (-79, 15), (-75.51, 10.39), (-74.07, 4.71), (-76.6, 2.44), (-78.47, -0.18), (-78.82, -1.47),
        (-79.2, -4), (-78.5, -7.16), (-77.04, -12.05)],
       [(-77.04, -12.05), (-80, -6), (-79.9, -2.19), (-88, 8), (-99.88, 16.85), (-99.13, 19.43), (-96.13, 19.2), (-82.36, 23.13), (-79, 30),
        (-75.16, 39.95), (-77.04, 38.9)], [(-75.16, 39.95), (-40, 45), (-0.58, 44.84)]],
      [('La Coruña', -8.4, 43.37), ('Teneriffa', -16.25, 28.47), ('Cumaná', -64.17, 10.46), ('Casiquiare (Orinoco–Amazonas)', -66.5, 2.5),
       ('Havanna', -82.36, 23.13), ('Bogotá', -74.07, 4.71), ('Quito', -78.47, -0.18), ('Chimborazo', -78.82, -1.47), ('Lima', -77.04, -12.05),
       ('Mexiko-Stadt', -99.13, 19.43), ('Philadelphia', -75.16, 39.95), ('Bordeaux', -0.58, 44.84)],
      'Britannica „Alexander von Humboldt“; Humboldt, „Reise in die Äquinoktial-Gegenden“')
fahrt('Reise Marco Polos', 'Marco Polo (mit Vater Niccolò und Onkel Maffeo)', 1271, 1295,
      'Landweg nach China zum Hof Kublai Khans, Rückreise über den Seeweg; Bericht „Il Milione“.', '#e8c86a', 2,
      [[(12.33, 45.44), (19, 38), (25, 34.5), (35.07, 32.93), (35.79, 36.77), (46.29, 38.08), (52.5, 29.6), (56.46, 27.1), (59.6, 36.3),
        (66.9, 36.76), (73.5, 37.5), (75.99, 39.47), (79.92, 37.11), (94.66, 40.14), (103.83, 36.06), (116.18, 42.36), (116.4, 39.9)],
       [(116.4, 39.9), (118.59, 24.87), (113, 18), (109.2, 13.8), (106, 5), (104.2, 1.3), (98, 5.6), (80.22, 6.03), (76.5, 8),
        (66, 20), (58.5, 23.8), (56.46, 27.1)],
       [(56.46, 27.1), (52.5, 29.6), (46.29, 38.08), (39.72, 41.0), (28.98, 41.01), (25, 36), (19, 38), (12.33, 45.44)]],
      [('Venedig', 12.33, 45.44), ('Akkon', 35.07, 32.93), ('Täbris', 46.29, 38.08), ('Hormus', 56.46, 27.1), ('Balch', 66.9, 36.76),
       ('Kaschgar', 75.99, 39.47), ('Dunhuang', 94.66, 40.14), ('Shangdu (Xanadu)', 116.18, 42.36), ('Khanbaliq (Peking)', 116.4, 39.9),
       ('Quanzhou', 118.59, 24.87), ('Trapezunt', 39.72, 41.0)],
      'Britannica „Marco Polo“')
obj = {'id': 'entdeckungsfahrten', 'name': 'Entdeckungs- und Forschungsreisen', 'gruppe': 'Geschichte', 'typ': 'linien', 'einheit': '',
       'legende': [{'n': f['n'], 'c': f['c']} for f in F],
       'quellen': [{'t': 'Verlauf schematisch nach Encyclopaedia Britannica (Artikel je Reise, Feld q) und weiteren genannten Belegen',
                    'u': 'https://www.britannica.com/', 'stand': '11/2026', 'lizenz': 'eigene schematische Zeichnung (Fakten)'}],
       'hinweis': 'Schematische Linien über belegte Stationen; Seestrecken mit Hilfspunkten. Linien am 180. Längengrad sind geteilt. '
                  'Ergänzt die Ebenen „Wanderungen“ (u. a. Wikinger allgemein) und „Erfindungen“.',
       'felder': {'n': 'Name', 'wer': 'Reisende', 'von/bis': 'Jahre', 'linien': 'Linienzüge [[lon,lat],…]', 'orte': '[Name, lon, lat]', 'rang': '1–3', 'q': 'Beleg'},
       'daten': F}
schreibe(obj)
