"""Ebene 'handelswege': schematische Linien historischer Handelswege über benannte Wegpunkte."""
import sys
sys.path.insert(0, '/home/claude/scratch/themen/b/prep')
from gemein import *

# Orte (Name -> lon, lat); Lage nach gängigen Ortskoordinaten (Wikipedia/GeoNames), auf 1/100 Grad
O = {
 "Chang'an (Xi'an)": (108.94, 34.27), 'Lanzhou': (103.83, 36.06), 'Dunhuang': (94.66, 40.14), 'Turfan': (89.19, 42.95),
 'Kucha': (82.96, 41.72), 'Kaschgar': (75.99, 39.47), 'Hotan': (79.92, 37.11), 'Samarkand': (66.96, 39.65),
 'Buchara': (64.42, 39.77), 'Merw': (61.83, 37.66), 'Rey (Teheran)': (51.43, 35.6), 'Hamadan': (48.51, 34.8),
 'Ktesiphon': (44.58, 33.09), 'Palmyra': (38.27, 34.55), 'Antiochia': (36.16, 36.2), 'Konstantinopel': (28.98, 41.01),
 'Tyros': (35.2, 33.27), 'Kabul': (69.18, 34.53), 'Taxila': (72.83, 33.75),
 'Guangzhou': (113.26, 23.13), 'Quanzhou': (118.59, 24.87), 'Palembang': (104.75, -2.99), 'Malakka': (102.25, 2.19),
 'Galle': (80.22, 6.03), 'Kalikut': (75.78, 11.25), 'Hormus': (56.46, 27.1), 'Basra': (47.81, 30.51), 'Aden': (45.03, 12.79),
 'Berenike': (35.48, 23.91), 'Alexandria': (29.92, 31.2), 'Venedig': (12.33, 45.44), 'Ternate (Molukken)': (127.38, 0.79),
 'Banda-Inseln': (129.9, -4.53), 'Lissabon': (-9.14, 38.71), 'Kap der Guten Hoffnung': (18.47, -34.36),
 'Ilha de Moçambique': (40.73, -15.03), 'Malindi': (40.12, -3.22), 'Kilwa': (39.51, -8.96), 'Goa': (73.82, 15.5),
 'Salala (Dhofar)': (54.1, 17.02), 'Schabwa': (47.02, 15.36), 'Marib': (45.33, 15.42), 'Nadschran': (44.13, 17.49),
 'Mekka': (39.83, 21.42), 'Yathrib (Medina)': (39.61, 24.47), 'Hegra (Mada’in Salih)': (37.95, 26.79), 'Petra': (35.44, 30.33),
 'Gaza': (34.45, 31.5),
 'Samland (Ostseeküste)': (20.3, 54.85), 'Kalisz': (18.09, 51.76), 'Carnuntum': (16.86, 48.11), 'Poetovio (Ptuj)': (15.87, 46.42),
 'Emona (Ljubljana)': (14.51, 46.05), 'Aquileia': (13.37, 45.77),
 'Sidschilmasa': (-4.25, 31.28), 'Teghaza': (-5.0, 23.6), 'Walata': (-7.03, 17.18), 'Timbuktu': (-3.0, 16.77), 'Gao': (-0.04, 16.27),
 'Tripolis': (13.19, 32.89), 'Ghadames': (9.5, 30.13), 'Mursuk (Fessan)': (13.92, 25.92), 'Bilma': (12.92, 18.69),
 'Tschadsee (Kanem)': (14.4, 13.4), 'Wargla': (5.33, 31.95), 'Tadmekka (Essouk)': (1.15, 18.85), 'Assiut': (31.18, 27.18),
 'Charga': (30.55, 25.45), 'El Fascher (Darfur)': (25.35, 13.63), 'Fès': (-5.0, 34.03), 'Kairouan': (10.1, 35.68),
 'Lüneburg': (10.41, 53.25), 'Mölln': (10.69, 53.63), 'Lübeck': (10.69, 53.87), 'Rom': (12.48, 41.89),
 'Castrum Truentinum (Adria)': (13.9, 42.9), 'Passau': (13.46, 48.57), 'Prachatitz': (14.0, 49.01), 'Bad Reichenhall': (12.88, 47.72),
 'Hallein': (13.1, 47.68), 'Hallstatt': (13.65, 47.56), 'Salzburg': (13.05, 47.8),
 'Liverpool': (-2.99, 53.41), 'Nantes': (-1.55, 47.22), 'Bristol': (-2.59, 51.45), 'Ouidah': (2.09, 6.36), 'Elmina': (-1.35, 5.08),
 'Luanda': (13.23, -8.84), 'Gorée': (-17.4, 14.67), 'Bridgetown (Barbados)': (-59.62, 13.1), 'Port Royal (Jamaika)': (-76.84, 17.94),
 'Salvador da Bahia': (-38.5, -12.97), 'Charleston': (-79.93, 32.78),
 'Capua': (14.21, 41.08), 'Benevent': (14.78, 41.13), 'Tarent': (17.24, 40.47), 'Brindisi': (17.94, 40.64),
 'Pisa': (10.4, 43.72), 'Genua': (8.93, 44.41), 'Arelate (Arles)': (4.63, 43.68), 'Dyrrachium (Durrës)': (19.45, 41.32),
 'Lychnidos (Ohrid)': (20.8, 41.12), 'Thessaloniki': (22.94, 40.64), 'Philippi': (24.29, 41.01), 'Byzantion': (28.98, 41.01),
 'Altinum': (12.4, 45.55), 'Tridentum (Trient)': (11.12, 46.07), 'Reschenpass': (10.52, 46.83), 'Foetes (Füssen)': (10.7, 47.57),
 'Augusta Vindelicum (Augsburg)': (10.9, 48.37), 'Ariminum (Rimini)': (12.57, 44.06), 'Lugdunum (Lyon)': (4.83, 45.76),
 'Andemantunnum (Langres)': (5.33, 47.86), 'Divodurum (Metz)': (6.18, 49.12), 'Augusta Treverorum (Trier)': (6.64, 49.75),
 'Colonia (Köln)': (6.96, 50.94), 'Nemausus (Nîmes)': (4.36, 43.84), 'Narbo (Narbonne)': (3.0, 43.18), 'Pyrenäenpass (Le Perthus)': (2.86, 42.46),
 'Mons Matrona (Montgenèvre)': (6.72, 44.93),
}
# Hanse-Städte [Name, lon, lat, rang, Rolle]
HANSE = [
 ['Lübeck', 10.69, 53.87, 1, 'Haupt der Hanse, Ort der Hansetage'], ['Hamburg', 9.99, 53.55, 1, 'Hansestadt'], ['Köln', 6.96, 50.94, 1, 'Hansestadt'],
 ['Danzig', 18.65, 54.35, 1, 'Hansestadt'], ['Visby', 18.29, 57.64, 1, 'Hansestadt (Gotland)'], ['Riga', 24.11, 56.95, 1, 'Hansestadt'],
 ['Bremen', 8.8, 53.08, 2, 'Hansestadt'], ['Rostock', 12.1, 54.09, 2, 'Hansestadt'], ['Wismar', 11.46, 53.89, 2, 'Hansestadt'],
 ['Stralsund', 13.09, 54.31, 2, 'Hansestadt; Frieden von Stralsund 1370'], ['Reval (Tallinn)', 24.75, 59.44, 2, 'Hansestadt'],
 ['Dortmund', 7.47, 51.51, 2, 'Hansestadt'], ['Braunschweig', 10.52, 52.27, 2, 'Hansestadt'], ['Magdeburg', 11.63, 52.13, 2, 'Hansestadt'],
 ['Lüneburg', 10.41, 53.25, 2, 'Hansestadt (Salz)'], ['Stettin', 14.55, 53.43, 3, 'Hansestadt'], ['Königsberg', 20.51, 54.71, 3, 'Hansestadt'],
 ['Thorn (Toruń)', 18.6, 53.01, 3, 'Hansestadt'], ['Krakau', 19.94, 50.06, 3, 'Hansestadt'], ['Dorpat (Tartu)', 26.72, 58.38, 3, 'Hansestadt'],
 ['Soest', 8.11, 51.57, 3, 'Hansestadt'], ['Münster', 7.63, 51.96, 3, 'Hansestadt'],
 ['London (Stalhof)', -0.09, 51.51, 1, 'Kontor'], ['Brügge', 3.22, 51.21, 1, 'Kontor'], ['Bergen (Bryggen)', 5.32, 60.39, 1, 'Kontor'],
 ['Nowgorod (Peterhof)', 31.27, 58.52, 1, 'Kontor'],
]


def W(*namen_oder_punkte):
    out = []
    for x in namen_oder_punkte:
        lo, la = O[x] if isinstance(x, str) else x
        out.append([r2(lo), r2(la)])
    return out


def orte(linien_namen):
    s = []
    for x in linien_namen:
        if isinstance(x, str) and x not in s: s.append(x)
    return [[n, r2(O[n][0]), r2(O[n][1])] for n in s]


WEGE = []


def weg(n, zeit, von, bis, waren, t, c, rang, teile, quelle):
    alle = [x for tl in teile for x in tl]
    WEGE.append({'n': n, 'zeit': zeit, 'von': von, 'bis': bis, 'waren': waren, 't': t, 'c': c, 'rang': rang, 'schema': True,
                 'linien': [W(*tl) for tl in teile], 'orte': orte(alle), 'q': quelle})


weg('Seidenstraße (Landweg)', 'ca. 130 v. Chr.–15. Jh.', -130, 1450, 'Seide, Porzellan, Papier, Gewürze, Pferde, Glas, Silber, Wolle',
    'Netz von Karawanenwegen zwischen China und dem Mittelmeer; Waren wechselten unterwegs oft den Besitzer.', '#ffcf5a', 1,
    [["Chang'an (Xi'an)", 'Lanzhou', 'Dunhuang', 'Turfan', 'Kucha', 'Kaschgar'], ['Dunhuang', 'Hotan', 'Kaschgar'],
     ['Kaschgar', 'Samarkand', 'Buchara', 'Merw', 'Rey (Teheran)', 'Hamadan', 'Ktesiphon', 'Palmyra', 'Antiochia'],
     ['Antiochia', 'Konstantinopel'], ['Palmyra', 'Tyros'], ['Samarkand', 'Kabul', 'Taxila']], 'Britannica „Silk Road“; UNESCO Silk Roads Programme')
weg('Seidenstraße (Seeweg)', 'ca. 2. Jh. v. Chr.–16. Jh.', -200, 1550, 'Seide, Porzellan, Gewürze, Edelsteine, Baumwolle, Weihrauch',
    'Seeverbindung von Südchina über Südostasien und Indien zum Persischen Golf und zum Roten Meer, getragen vom Monsun.', '#ffe08a', 1,
    [['Quanzhou', 'Guangzhou', (112, 20), (109.5, 12), (106, 5), (104.2, 1.3), 'Malakka', (98, 5.6), (88, 6), 'Galle', (76.5, 8), 'Kalikut'],
     ['Guangzhou', (110, 15), (108, 5), (106, -1.5), 'Palembang'],
     ['Kalikut', (67, 20), (58.5, 23.5), 'Hormus', (51.5, 27), 'Basra'],
     ['Kalikut', (60, 13.5), (51, 12.2), 'Aden', (43.3, 12.7), (40, 17.5), (37, 21.5), 'Berenike']], 'Britannica „Silk Road“; UNESCO Silk Roads Programme')
weg('Weihrauchstraße', 'ca. 7. Jh. v. Chr.–2. Jh. n. Chr.', -700, 200, 'Weihrauch, Myrrhe, Gewürze',
    'Karawanenweg von Südarabien zum Mittelmeer; Weihrauch aus Dhofar und Jemen.', '#e8a070', 2,
    [['Salala (Dhofar)', 'Schabwa', 'Marib', 'Nadschran', 'Mekka', 'Yathrib (Medina)', 'Hegra (Mada’in Salih)', 'Petra', 'Gaza']],
    'UNESCO-Welterbe „Incense Route – Desert Cities in the Negev“; Britannica „Incense route“')
weg('Bernsteinstraße', 'ca. 1. Jh. v. Chr.–4. Jh. n. Chr. (römische Zeit)', -50, 400, 'Bernstein, Pelze, Sklaven; Wein, Glas, Metallwaren',
    'Weg von der Ostseeküste über Pannonien nach Aquileia an der Adria.', '#ffb347', 2,
    [['Samland (Ostseeküste)', 'Kalisz', 'Carnuntum', 'Poetovio (Ptuj)', 'Emona (Ljubljana)', 'Aquileia']], 'Britannica „Amber Road“; Plinius d. Ä., Naturalis historia 37')
weg('Hanse – Hauptrouten', 'ca. 1150–1669', 1150, 1669, 'Pelze, Wachs, Getreide, Stockfisch, Salz, Tuch, Bier, Holz, Teer',
    'Bund niederdeutscher Kaufleute und Städte; Kontore in London, Brügge, Bergen und Nowgorod. Letzter Hansetag 1669.', '#8ab8ff', 1,
    [[(-0.09, 51.51), (1.5, 51.6), (4.5, 53.0), (8.0, 54.0), (9.99, 53.55)], [(3.22, 51.21), (3.3, 51.6), (4.5, 53.0)],
     [(9.99, 53.55), (10.69, 53.87)], [(10.69, 53.87), (11.46, 53.89), (12.1, 54.09), (13.09, 54.31), (14.3, 54.7), (18.65, 54.35)],
     [(13.09, 54.31), (16.5, 56.5), (18.29, 57.64), (21.0, 57.8), (24.11, 56.95)], [(18.29, 57.64), (22.0, 59.3), (24.75, 59.44), (28.0, 59.9), (30.0, 59.95), (31.27, 58.52)],
     [(5.32, 60.39), (5.0, 58.5), (8.6, 57.8), (10.8, 57.9), (11.5, 56.5), (12.6, 55.6), (12.0, 54.5), (10.69, 53.87)],
     [(6.96, 50.94), (7.47, 51.51), (8.11, 51.57), (10.52, 52.27), (11.63, 52.13)], [(10.69, 53.87), (10.41, 53.25)]],
    'Britannica „Hanseatic League“; Europäisches Hansemuseum Lübeck')
WEGE[-1]['orte'] = [[n, r2(lo), r2(la), rg, rolle] for n, lo, la, rg, rolle in HANSE]
weg('Römerstraßen (Auswahl)', '312 v. Chr. (Via Appia) bis Spätantike', -312, 476, 'Truppen, Post (cursus publicus), Handel',
    'Wichtige Fernstraßen des Römischen Reiches: Via Appia, Aurelia, Flaminia, Egnatia, Claudia Augusta, Domitia, Agrippa.', '#d87a6a', 2,
    [['Rom', 'Capua', 'Benevent', 'Tarent', 'Brindisi'], ['Rom', 'Pisa', 'Genua', 'Arelate (Arles)'], ['Rom', 'Ariminum (Rimini)'],
     ['Dyrrachium (Durrës)', 'Lychnidos (Ohrid)', 'Thessaloniki', 'Philippi', 'Byzantion'],
     ['Altinum', 'Tridentum (Trient)', 'Reschenpass', 'Foetes (Füssen)', 'Augusta Vindelicum (Augsburg)'],
     ['Mons Matrona (Montgenèvre)', 'Nemausus (Nîmes)', 'Narbo (Narbonne)', 'Pyrenäenpass (Le Perthus)'],
     ['Lugdunum (Lyon)', 'Andemantunnum (Langres)', 'Divodurum (Metz)', 'Augusta Treverorum (Trier)', 'Colonia (Köln)']],
    'Britannica „Roman road system“; Pleiades-Gazetteer (CC BY 3.0) für Orte')
WEGE[-1]['teilnamen'] = ['Via Appia', 'Via Aurelia', 'Via Flaminia', 'Via Egnatia', 'Via Claudia Augusta', 'Via Domitia', 'Via Agrippa']
weg('Transsahara-Handel', 'ca. 8.–16. Jh.', 750, 1600, 'Gold, Salz, Sklaven, Elfenbein, Kupfer, Textilien, Bücher',
    'Kamelkarawanen verbanden Nordafrika mit den Reichen Ghana, Mali, Songhai und Kanem-Bornu.', '#e8c070', 1,
    [['Fès', 'Sidschilmasa', 'Teghaza', 'Walata', 'Timbuktu'], ['Timbuktu', 'Gao'], ['Kairouan', 'Wargla', 'Tadmekka (Essouk)', 'Gao'],
     ['Tripolis', 'Ghadames', 'Mursuk (Fessan)', 'Bilma', 'Tschadsee (Kanem)'], ['Assiut', 'Charga', 'El Fascher (Darfur)']],
    'Britannica „Trans-Saharan trade“; UNESCO „Ancient ksour of Ouadane, Chinguetti, Tichitt and Oualata“')
WEGE[-1]['teilnamen'] = ['Westroute', 'Niger', 'Mittlere Route', 'Fessan-Route', 'Darb al-Arbain (Vierzig-Tage-Weg)']
weg('Gewürzroute', 'Mittelalter bis 17. Jh. (Kaproute ab 1498)', 900, 1700, 'Nelken, Muskat, Pfeffer, Zimt, Ingwer',
    'Gewürze von den Molukken und aus Indien über Arabien und Ägypten nach Venedig; ab 1498 auch um Afrika herum nach Lissabon.', '#ff8a5a', 1,
    [['Banda-Inseln', (127, -5), (120, -6.5), (110, -5.5), (106.5, -3.5), (105, 0), 'Malakka'], ['Ternate (Molukken)', (125, -1.5), (120, -6.5)],
     ['Malakka', (98, 5.6), (88, 6), 'Galle', (76.5, 8), 'Kalikut', 'Goa'],
     ['Kalikut', (60, 13.5), (51, 12.2), 'Aden', (43.3, 12.7), (38, 20), (33.5, 28), (32.5, 30), 'Alexandria', (25, 34), (19, 38), (18.7, 40.3), (14, 44.4), 'Venedig'],
     ['Lissabon', (-17, 25), (-23, 5), (-10, -20), (10, -33), 'Kap der Guten Hoffnung', (22.14, -34.6), (27, -34.5), (31.5, -31.5), (35, -30), (36, -25), (38, -20), 'Ilha de Moçambique', (41.2, -11), 'Kilwa', (40.2, -6.5), 'Malindi', (55, 5), 'Kalikut']],
    'Britannica „spice trade“')
weg('Salzstraßen (Auswahl)', 'Antike bis Neuzeit', -500, 1800, 'Salz',
    'Alte Salzstraße Lüneburg–Lübeck, Via Salaria bei Rom, Goldener Steig von Passau nach Böhmen, Salzwege der Ostalpen.', '#e8e8e8', 2,
    [['Lüneburg', 'Mölln', 'Lübeck'], ['Rom', 'Castrum Truentinum (Adria)'], ['Passau', 'Prachatitz'], ['Bad Reichenhall', 'Salzburg', 'Passau'],
     ['Hallstatt', 'Hallein', 'Salzburg']], 'Britannica „Via Salaria“; Stadt Lüneburg „Alte Salzstraße“')
WEGE[-1]['teilnamen'] = ['Alte Salzstraße', 'Via Salaria', 'Goldener Steig', 'Salzach/Inn-Weg', 'Salzkammergut']
weg('Atlantischer Dreieckshandel', 'ca. 16.–19. Jh.', 1550, 1867, 'Europa→Afrika: Textilien, Waffen, Alkohol, Metallwaren; Afrika→Amerika: versklavte Menschen; Amerika→Europa: Zucker, Tabak, Baumwolle, Rum',
    'Handelsdreieck Europa–Westafrika–Amerika; Kern war die Verschleppung versklavter Menschen (vgl. Ebene Wanderungen).', '#ff8a8a', 2,
    [['Liverpool', (-5, 53), (-6, 51), (-10, 45), (-18, 25), 'Gorée', (-18, 11), (-15, 7.5), (-12, 4.5), (-7.5, 3.8), (-4, 4.5), 'Elmina', (0.5, 5.4), 'Ouidah'], ['Nantes', (-10, 42)], ['Lissabon', (-18, 25)],
     ['Ouidah', (1, 5.2), (-5, 3.5), (-10, 3), (-20, 5), (-45, 12), 'Bridgetown (Barbados)', 'Port Royal (Jamaika)'], ['Luanda', (-15, -12), 'Salvador da Bahia'],
     ['Port Royal (Jamaika)', (-74.2, 20.0), (-75.5, 24), (-79, 27.5), 'Charleston', (-60, 38), (-30, 48), (-8, 51), (-5.5, 52.5), 'Liverpool'], ['Salvador da Bahia', (-30, 10), (-20, 35), 'Lissabon']],
    'Slave Voyages (Trans-Atlantic Slave Trade Database); Britannica „triangular trade“')
for w in WEGE:
    for l in w['linien']:
        for lo, la in l: assert -180 <= lo <= 180 and -90 <= la <= 90
obj = {'id': 'handelswege', 'name': 'Historische Handelswege', 'gruppe': 'Geschichte', 'typ': 'linien', 'einheit': '',
       'legende': [{'n': w['n'], 'c': w['c']} for w in WEGE],
       'quellen': [{'t': 'Verlauf schematisch nach Encyclopaedia Britannica (Artikel je Weg, siehe Feld q) und UNESCO-Beschreibungen; Ortslagen nach Wikipedia/GeoNames',
                    'u': 'https://www.britannica.com/', 'stand': '11/2026', 'lizenz': 'eigene schematische Zeichnung (Fakten), keine fremden Geodaten'},
                   {'t': 'UNESCO Silk Roads Programme', 'u': 'https://en.unesco.org/silkroad/', 'stand': '11/2026', 'lizenz': 'nur als Beleg zitiert'}],
       'hinweis': 'Alle Linien sind schematisch: gerade Verbindungen zwischen belegten Hauptorten (Seewege mit Hilfspunkten auf See). '
                  'Tatsächliche Wege waren Netze mit vielen Varianten.',
       'felder': {'n': 'Name', 'zeit': 'Zeitraum (Text)', 'von/bis': 'Jahre (negativ = v. Chr.)', 'waren': 'gehandelte Waren', 'linien': 'Liste von Linienzügen [[lon,lat],…]',
                  'orte': '[Name, lon, lat(, rang, Rolle)]', 'teilnamen': 'Namen der Teilstrecken (gleiche Reihenfolge wie linien)', 'rang': '1–3', 'q': 'Beleg'},
       'daten': WEGE}
schreibe(obj)
