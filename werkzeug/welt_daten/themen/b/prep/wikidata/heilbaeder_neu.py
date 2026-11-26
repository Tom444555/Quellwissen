"""Heilbäder: ergänzt a/fertig/heilbaeder.json (NI, BY, NW, SN – unverändert übernommen) um Hessen, Thüringen,
Sachsen-Anhalt und Brandenburg aus amtlichen Quellen; Lage aus Wikidata (CC0).
Schritt 1: python3 -I heilbaeder_neu.py abfrage  -> q_heilbaeder_orte.rq (dann ./sparql.sh q_heilbaeder_orte.rq roh/heilbaeder_orte.json)
Schritt 2: python3 -I heilbaeder_neu.py           -> heilbaeder.json"""
import json, sys, re, collections
sys.path.insert(0, '/home/claude/scratch/wikidata')

ALT = '/home/claude/quellwissen/werkzeug/welt_daten/themen/a/fertig/heilbaeder.json'
OFFEN = 'Heilbad (Art im Verzeichnis nicht genannt)'
# (Name in der Datei, Land, Prädikat laut Quelle, Art-Kurzform, Wikidata-Bezeichnung für die Lage)
HE = [('Bad Arolsen', 'Heilbad', OFFEN, 'Bad Arolsen'),
      ('Sand (Bad Emstal)', 'Heilbad', OFFEN, 'Bad Emstal'),
      ('Bad Endbach', 'Heilbad; Kneippheilbad', OFFEN, 'Bad Endbach'),
      ('Bad Hersfeld', 'Heilbad', OFFEN, 'Bad Hersfeld'),
      ('Bad Homburg v. d. Höhe', 'Heilbad', OFFEN, 'Bad Homburg vor der Höhe'),
      ('Bad Karlshafen', 'Heilbad', OFFEN, 'Bad Karlshafen'),
      ('Bad König', 'Heilbad', OFFEN, 'Bad König'),
      ('Bad Nauheim', 'Heilbad; Kneippheilbad', OFFEN, 'Bad Nauheim'),
      ('Bad Orb', 'Heilbad', OFFEN, 'Bad Orb'),
      ('Bad Salzschlirf', 'Heilbad', OFFEN, 'Bad Salzschlirf'),
      ('Bad Schwalbach', 'Heilbad; Kneippkurort', OFFEN, 'Bad Schwalbach'),
      ('Bad Soden-Salmünster', 'Heilbad', OFFEN, 'Bad Soden-Salmünster'),
      ('Bad Sooden-Allendorf', 'Heilbad', OFFEN, 'Bad Sooden-Allendorf'),
      ('Bad Wildungen (mit Reinhardshausen)', 'Heilbad', OFFEN, 'Bad Wildungen'),
      ('Herbstein', 'Heilbad; Luftkurort', OFFEN, 'Herbstein'),
      ('Bad Wilhelmshöhe (Kassel)', 'Heilbad; Kneippheilbad', OFFEN, 'Bad Wilhelmshöhe'),
      ('Bad Salzhausen (Nidda)', 'Heilbad', OFFEN, 'Bad Salzhausen'),
      ('Schlangenbad', 'Heilbad', OFFEN, 'Schlangenbad'),
      ('Wiesbaden', 'Heilbad', OFFEN, 'Wiesbaden'),
      ('Bad Soden am Taunus', 'Ort mit Heilquellenkurbetrieb', 'Heilquelle', 'Bad Soden am Taunus'),
      ('Bad Vilbel', 'Ort mit Heilquellenkurbetrieb', 'Heilquelle', 'Bad Vilbel'),
      ('Bad Zwesten', 'Ort mit Heilquellenkurbetrieb; Luftkurort', 'Heilquelle', 'Bad Zwesten')]
TH = [('Bad Berka', 'Ort mit Heilquellenkurbetrieb', 'Heilquelle', 'Bad Berka'),
      ('Bad Colberg (Bad Colberg-Heldburg)', 'Ort mit Heilquellenkurbetrieb', 'Heilquelle', 'Bad Colberg'),
      ('Bad Frankenhausen', 'Soleheilbad', 'Sole', 'Bad Frankenhausen/Kyffhäuser'),
      ('Bad Klosterlausnitz', 'Heilbad', OFFEN, 'Bad Klosterlausnitz'),
      ('Bad Langensalza', 'Schwefel-Sole-Heilbad', 'Sole (Schwefel)', 'Bad Langensalza'),
      ('Bad Liebenstein', 'Heilbad', OFFEN, 'Bad Liebenstein'),
      ('Bad Lobenstein', 'Moorheilbad', 'Moor', 'Bad Lobenstein'),
      ('Bad Salzungen', 'Soleheilbad', 'Sole', 'Bad Salzungen'),
      ('Bad Sulza', 'Soleheilbad', 'Sole', 'Bad Sulza'),
      ('Bad Tennstedt', 'Ort mit Heilquellenkurbetrieb', 'Heilquelle', 'Bad Tennstedt'),
      ('Heilbad Heiligenstadt', 'Soleheilbad', 'Sole', 'Heilbad Heiligenstadt')]
ST = [('Bad Salzelmen (Schönebeck)', 'Soleheilbad', 'Sole', 'Bad Salzelmen'),
      ('Bad Kösen (Naumburg)', 'Soleheilbad', 'Sole', 'Bad Kösen'),
      ('Bad Schmiedeberg', 'Moor- und Mineralheilbad; Kneipp-Heilbad', 'Mineralquelle, Moor', 'Bad Schmiedeberg')]
BB = [('Bad Belzig', 'Thermalsoleheilbad', 'Thermal, Sole', 'Bad Belzig'),
      ('Bad Freienwalde (Oder)', 'Moorheilbad', 'Moor', 'Bad Freienwalde (Oder)'),
      ('Bad Liebenwerda', 'Ort mit Peloid-Kurbetrieb', 'Moor', 'Bad Liebenwerda'),
      ('Bad Saarow', 'Thermalsole- und Moorheilbad', 'Thermal, Sole, Moor', 'Bad Saarow'),
      ('Bad Wilsnack', 'Thermalsole- und Moorheilbad', 'Thermal, Sole, Moor', 'Bad Wilsnack'),
      ('Burg (Spreewald)', 'Thermalsoleheilbad', 'Thermal, Sole', 'Burg (Spreewald)'),
      ('Templin', 'Thermalsoleheilbad', 'Thermal, Sole', 'Templin')]
NEU = {'HE': HE, 'TH': TH, 'ST': ST, 'BB': BB}
STAND = {'HE': '30.04.2026', 'TH': '01.01.2017', 'ST': '04.03.2024', 'BB': '17.07.2026'}

if len(sys.argv) > 1 and sys.argv[1] == 'abfrage':
    namen = sorted({x[3] for L in NEU.values() for x in L})
    q = ('SELECT ?i ?l ?coord ?typ WHERE { VALUES ?l { %s } ?i rdfs:label ?l ; wdt:P17 wd:Q183 ; wdt:P625 ?coord . '
         'OPTIONAL { ?i wdt:P31 ?typ } }' % ' '.join('"%s"@de' % n for n in namen))
    open('q_heilbaeder_orte.rq', 'w').write(q); print(len(namen), 'Namen'); sys.exit()

import geo
B = json.load(open('roh/heilbaeder_orte.json'))['results']['bindings']
# bevorzugte Klassen: Stadt/Gemeinde/Ortsteil/Kurort in Deutschland
GUT = {'Q42744322', 'Q262166', 'Q1187811', 'Q253019', 'Q116457956', 'Q15284', 'Q486972', 'Q1549591', 'Q3957', 'Q532',
       'Q2264924', 'Q123705', 'Q5084', 'Q15632617', 'Q1115575', 'Q106658', 'Q22865', 'Q1906268', 'Q1867183', 'Q19953632'}
kand = collections.defaultdict(dict)
for b in B:
    q = b['i']['value'].rsplit('/', 1)[1]
    m = re.match(r'Point\(([-\d.eE]+) ([-\d.eE]+)\)', b['coord']['value'])
    k = kand[b['l']['value']].setdefault(q, {'c': (float(m[1]), float(m[2])), 't': set()})
    if 'typ' in b: k['t'].add(b['typ']['value'].rsplit('/', 1)[1])

alt = json.load(open(ALT))
daten = list(alt['daten'])
fehlt, wahl = [], []
for land, L in NEU.items():
    for n, praed, art, wdn in L:
        cs = [(q, v) for q, v in kand.get(wdn, {}).items() if geo.bundesland(v['c'][0], v['c'][1], 0.05)[0] == land]
        cs.sort(key=lambda a: (not (a[1]['t'] & GUT), int(a[0][1:])))
        if not cs: fehlt.append((n, land)); continue
        q, v = cs[0]
        wahl.append((n, land, q, sorted(v['t'] & GUT)[:2], len(cs)))
        daten.append({'n': n, 'land': land, 'praedikat': praed, 'art': art, 'lon': round(v['c'][0], 2), 'lat': round(v['c'][1], 2),
                      'stand': STAND[land]})

quellen = [x for x in alt['quellen'] if 'GeoNames' not in x['t']] + [
    {'t': 'Regierungspräsidium Kassel: Prädikatisierte Orte und Ortsteile in Hessen (Kur-, Erholungs- und Tourismusorte)',
     'u': 'https://rp-kassel.hessen.de/sites/rp-kassel.hessen.de/files/2026-05/2026-internet.pdf', 'stand': '30.04.2026', 'lizenz': 'amtliches Verzeichnis (Fakten)'},
    {'t': 'Thüringer Landtag, Drucksache 6/3368 (Antwort der Landesregierung „Kur- und Erholungsorte in Thüringen“), Anlage 2: Kurorte zum 01.01.2017',
     'u': 'https://parldok.thueringer-landtag.de/ParlDok/dokument/61255/kur-und-erholungsorte-in-th', 'stand': '01.01.2017', 'lizenz': 'amtliche Angaben (Fakten)'},
    {'t': 'Landesverwaltungsamt Sachsen-Anhalt, Pressemitteilung 22/2024 „45 Kur- und Erholungsorte in Sachsen-Anhalt im dauerhaften Qualitätscheck“ (3 Heilbäder)',
     'u': 'https://presse.sachsen-anhalt.de/wp-content/uploads/pdf/lvwa_04_03_2024_Pressemitteilung_45-kur-und-erholungsorte-in-sachsen-anhalt-im-dauerhaften-qualitaetscheck.pdf',
     'stand': '04.03.2024', 'lizenz': 'amtliche Angaben (Fakten)'},
    {'t': 'Brandenburg, Ministerium für Gesundheit und Soziales: Pressemitteilung 182/2025 (Liste der acht staatlich anerkannten Kurorte); MASGZ Pressemitteilung 071/2026 (Bad Wilsnack)',
     'u': 'https://mgs.brandenburg.de/sixcms/media.php/9/182_25_Buckow_wird_Kneipp_Heilbad_MGS_2025_16_12.pdf', 'stand': '16.12.2025 / 17.07.2026', 'lizenz': 'amtliche Angaben (Fakten)'},
    {'t': 'GeoNames cities1000 (Ortskoordinaten NI, BY, NW, SN)', 'u': 'https://www.geonames.org/', 'stand': 'Paketstand reverse_geocoder', 'lizenz': 'CC BY 4.0'},
    {'t': 'Wikidata (Ortskoordinaten HE, TH, ST, BB), SPARQL-Abfrage', 'u': 'https://query.wikidata.org/', 'stand': '26.11.2026', 'lizenz': 'CC0 1.0'}]
kopf = {k: v for k, v in alt.items() if k != 'daten'}
kopf['quellen'] = quellen
kopf['hinweis'] = ('Niedersachsen, Bayern, Nordrhein-Westfalen, Sachsen, Hessen, Thüringen, Sachsen-Anhalt und Brandenburg (amtliche '
                   'Landesverzeichnisse bzw. amtliche Angaben der Landesregierungen); Seeheil-, Kneipp- (auch Kneipp-Heilbäder) und reine '
                   'heilklimatische Orte weggelassen (Zweitprädikate in `praedikat` genannt). Ortsteile ohne eigene Koordinate mit der Lage der '
                   'Gemeinde. Art der Quelle nur, soweit das Prädikat sie nennt; bayerische, hessische und Teile der thüringischen „Heilbäder“ ohne '
                   'Artangabe. Stände: NI 04/2026, BY 01/2020, NW 07/2026, SN 09/2019, HE 04/2026, TH 01/2017, ST 03/2024, BB 07/2026. '
                   'Lage NI/BY/NW/SN aus GeoNames, HE/TH/ST/BB aus Wikidata. Es fehlen Baden-Württemberg, Rheinland-Pfalz, Saarland, '
                   'Schleswig-Holstein und Mecklenburg-Vorpommern (keine amtliche Liste abrufbar, siehe pruef.md).')
kopf['legende'] = alt['legende']
o = dict(kopf); o['daten'] = daten
json.dump(o, open('heilbaeder.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
json.dump({'wahl': wahl, 'fehlt': fehlt}, open('roh/heilbaeder_bericht.json', 'w'), ensure_ascii=False, indent=0)
print(len(daten), 'Orte', collections.Counter(e['land'] for e in daten)); print('fehlt', fehlt)
for w in wahl: print(w)
