"""Weinbau (13 Anbaugebiete: Rebfläche 2024, Weinerzeugung 2025) und Hopfen (Anbaugebiete, Fläche 2025).
Lagepunkt = bekannter Ort im Gebiet (GeoNames-Koordinate), nur als Markierung (schema:true). Aufruf: python3 -I prep/wein_hopfen.py"""
import sys, os, csv, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gemein import ROH, schreibe, r2

def norm(s):
    s = s.replace('ä', 'a').replace('ö', 'o').replace('ü', 'u').replace('ß', 'ss')
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower().replace('ue', 'u').replace('oe', 'o').replace('ae', 'a')
GN = {}
for r in csv.DictReader(open(os.path.join(ROH, 'wege', 'geonames_cities1000_rg.csv'), encoding='utf-8')):
    if r['cc'] == 'DE':
        GN.setdefault(norm(r['name']), []).append((float(r['lon']), float(r['lat'])))
def ort(n, hint):
    return min(GN[norm(n)], key=lambda q: (q[0] - hint[0]) ** 2 + (q[1] - hint[1]) ** 2)

# [Gebiet, Rebfläche ha 03.06.2024 (DWI/Destatis), Weinerzeugung 2025 in 1.000 hl (Destatis), Länder, Lageort, Hinweis-Koordinate]
WEIN = [['Rheinhessen', 27671, 2306.2, 'RP', 'Alzey', (8.1, 49.75)], ['Pfalz', 23787, 1871.3, 'RP', 'Landau in der Pfalz', (8.12, 49.2)],
        ['Baden', 15454, 996.7, 'BW', 'Breisach am Rhein', (7.6, 48.0)], ['Württemberg', 11179, 739.9, 'BW, BY', 'Heilbronn', (9.2, 49.1)],
        ['Mosel', 8445, 743.4, 'RP, SL', 'Bernkastel-Kues', (7.07, 49.9)], ['Franken', 6128, 382.1, 'BY', 'Würzburg', (9.9, 49.8)],
        ['Nahe', 4234, 271.3, 'RP', 'Bad Kreuznach', (7.87, 49.84)], ['Rheingau', 3180, 168.9, 'HE', 'Eltville', (8.12, 50.03)],
        ['Saale-Unstrut', 858, 58.9, 'ST, TH, BB', 'Freyburg', (11.77, 51.21)], ['Ahr', 533, 33.7, 'RP', 'Bad Neuenahr-Ahrweiler', (7.12, 50.54)],
        ['Sachsen', 529, 29.5, 'SN', 'Meissen', (13.47, 51.16)], ['Hessische Bergstraße', 456, 25.7, 'HE', 'Heppenheim an der Bergstrasse', (8.64, 49.64)],
        ['Mittelrhein', 451, 21.0, 'RP, NW', 'Bacharach', (7.77, 50.06)]]
HOPFEN = [['Hallertau', 15680, 'BY', 'Wolnzach', (11.62, 48.6), 'Größtes Hopfenanbaugebiet der Welt (laut Verband 83 % der deutschen Fläche).'],
          ['Tettnang', 1526, 'BW', 'Tettnang', (9.59, 47.67), ''], ['Elbe-Saale', 1379, 'ST, TH, SN', 'Halle (Saale)', (11.97, 51.48), 'Anbaugebiet über drei Länder verteilt; Punkt nur grobe Lage.'],
          ['Spalt', 360, 'BY', 'Spalt', (10.92, 49.17), ''], ['Rheinpfalz/Bitburg', 17, 'RP', 'Bitburg', (6.53, 49.97), '']]
wein = []
for n, ha, hl, l, o, h in WEIN:
    lo, la = ort(o, h)
    wein.append({'n': n, 'ha': ha, 'tsd_hl_2025': hl, 'land': l, 'ort': o.replace('Meissen', 'Meißen').replace('Heppenheim an der Bergstrasse', 'Heppenheim'), 'lon': r2(lo), 'lat': r2(la), 'schema': True})
hopf = []
for n, ha, l, o, h, t in HOPFEN:
    k = GN.get(norm(o)) or GN.get(norm('Halle (Saale)')) or GN.get(norm('Halle'))
    lo, la = min(k, key=lambda q: (q[0] - h[0]) ** 2 + (q[1] - h[1]) ** 2)
    hopf.append({'n': n, 'ha': ha, 'land': l, 'ort': o, 'lon': r2(lo), 'lat': r2(la), 'text': t, 'schema': True})
print('Wein', sum(w['ha'] for w in wein), 'ha; Hopfen', sum(h['ha'] for h in hopf), 'ha')
for x in wein + hopf: print(' ', x['n'], x['ort'], x['lon'], x['lat'])
schreibe({
    'id': 'wein_hopfen', 'name': 'Weinbau und Hopfen', 'gruppe': 'Deutschland', 'typ': 'punkte', 'einheit': 'ha',
    'legende': [['Weinanbaugebiet (Kreisgröße = Rebfläche)', '#b04a7a'], ['Hopfenanbaugebiet (Kreisgröße = Fläche)', '#8ad04a']],
    'quellen': [
        {'t': 'Deutsches Weininstitut: Deutscher Wein Statistik 2025, Übersicht 3 „Bestockte Rebflächen … nach Anbaugebieten 2024“ (Stichtag 03.06.2024, nach Statistischem Bundesamt)', 'u': 'https://www.deutscheweine.de/fileadmin/DWI/News_Medien/Publikationen/Deutscher_Wein_Statistik/Statistik_2025.pdf', 'stand': '03.06.2024', 'lizenz': 'Fakten aus amtlicher Statistik (Destatis, dl-de/by-2-0); DWI als Herausgeber nennen'},
        {'t': 'Statistisches Bundesamt: Weinerzeugung 2025 nach Anbaugebieten (Stand 30.03.2026)', 'u': 'https://www.destatis.de/EN/Themes/Economic-Sectors-Enterprises/Agriculture-Forestry-Fisheries/Wine/Tables/wine-production-abg.html', 'stand': '2025', 'lizenz': 'dl-de/by-2-0, Quelle: Statistisches Bundesamt (Destatis)'},
        {'t': 'Verband Deutscher Hopfenpflanzer: „Der Hopfen“ (Wolnzach, April 2026) – Flächen je Anbaugebiet; Summe = 18.961 ha laut Pressestatement 12/2025', 'u': 'https://www.deutscher-hopfen.de/wp-content/uploads/2026/04/Der-Hopfen.pdf', 'stand': '2025', 'lizenz': 'nur Zahlen (Fakten) übernommen'},
        {'t': 'GeoNames cities1000 (Koordinaten der Lageorte)', 'u': 'https://www.geonames.org/', 'stand': 'Paketstand reverse_geocoder', 'lizenz': 'CC BY 4.0'}],
    'hinweis': 'Punkt = ein bekannter Ort im Gebiet (schema:true), keine Gebietsgrenze. Rebflächen-Summe der 13 Gebiete 102.905 ha (Deutschland gesamt 103.295 ha).',
    'daten_hopfen': hopf
}, wein)
