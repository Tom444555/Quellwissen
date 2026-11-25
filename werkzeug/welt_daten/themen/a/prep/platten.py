"""Plattengrenzen nach Art + Plattennamen: Bird (2003) PB2002, Aufbereitung Hugo Ahlenius (GitHub fraxen/tectonicplates, ODC-BY 1.0).
Aufruf: python3 -I prep/platten.py"""
import sys, os, collections, statistics
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gemein import ROH, r2, schreibe, vereinfache
import shapefile
from shapely.geometry import shape

D = os.path.join(ROH, 'platten')
ART = {'OSR': 'auseinander', 'CRB': 'auseinander', 'SUB': 'zusammen', 'OCB': 'zusammen', 'CCB': 'zusammen', 'OTF': 'seitlich', 'CTF': 'seitlich'}
ARTTXT = {'OSR': 'Mittelozeanischer Rücken', 'CRB': 'Kontinentaler Grabenbruch', 'SUB': 'Subduktionszone', 'OCB': 'Ozeanische Kollisionszone',
          'CCB': 'Kontinentale Kollisionszone', 'OTF': 'Ozeanische Transformstörung', 'CTF': 'Kontinentale Transformstörung'}
DE = {'Africa': 'Afrikanische Platte', 'Antarctica': 'Antarktische Platte', 'Somalia': 'Somalische Platte', 'India': 'Indische Platte',
      'Australia': 'Australische Platte', 'Eurasia': 'Eurasische Platte', 'North America': 'Nordamerikanische Platte', 'South America': 'Südamerikanische Platte',
      'Nazca': 'Nazca-Platte', 'Pacific': 'Pazifische Platte', 'Arabia': 'Arabische Platte', 'Sunda': 'Sunda-Platte', 'Caribbean': 'Karibische Platte',
      'Cocos': 'Cocos-Platte', 'Okhotsk': 'Ochotskische Platte', 'Juan de Fuca': 'Juan-de-Fuca-Platte', 'Philippine Sea': 'Philippinische Platte',
      'Amur': 'Amur-Platte', 'Scotia': 'Scotia-Platte', 'Anatolia': 'Anatolische Platte', 'Aegean Sea': 'Ägäische Platte', 'Yangtze': 'Jangtse-Platte',
      'Caroline': 'Karolinen-Platte', 'Burma': 'Burma-Platte', 'Tonga': 'Tonga-Platte', 'Kermadec': 'Kermadec-Platte', 'Mariana': 'Marianen-Platte',
      'Okinawa': 'Okinawa-Platte', 'Rivera': 'Rivera-Platte', 'Panama': 'Panama-Platte', 'North Andes': 'Nordanden-Platte', 'Altiplano': 'Altiplano-Platte',
      'Easter': 'Osterinsel-Platte', 'Galapagos': 'Galápagos-Platte', 'Juan Fernandez': 'Juan-Fernández-Platte', 'Sandwich': 'Sandwich-Platte',
      'Shetland': 'Shetland-Platte', 'Timor': 'Timor-Platte', 'Banda Sea': 'Bandasee-Platte', 'Molucca Sea': 'Molukkensee-Platte', 'Birds Head': 'Vogelkop-Platte',
      'Maoke': 'Maoke-Platte', 'Woodlark': 'Woodlark-Platte', 'Solomon Sea': 'Salomonensee-Platte', 'North Bismarck': 'Nordbismarck-Platte',
      'South Bismarck': 'Südbismarck-Platte', 'Manus': 'Manus-Platte', 'New Hebrides': 'Neue-Hebriden-Platte', 'Futuna': 'Futuna-Platte',
      'Niuafo\'ou': 'Niuafoʻou-Platte', 'Conway Reef': 'Conway-Riff-Platte', 'Balmoral Reef': 'Balmoral-Riff-Platte'}
GROSS = {'AF', 'AN', 'AU', 'EU', 'NA', 'SA', 'PA'}          # 7 Hauptplatten
MITTEL = {'IN', 'NZ', 'AR', 'CA', 'CO', 'JF', 'PS', 'SC', 'SO', 'SU', 'OK', 'AM', 'AT', 'YA'}

s = shapefile.Reader(os.path.join(D, 'PB2002_steps'))
recs = sorted(s.records(), key=lambda r: r['SEQNUM'])
CODE = {'OSR': 'R', 'CRB': 'G', 'SUB': 'S', 'OCB': 'O', 'CCB': 'K', 'OTF': 'T', 'CTF': 'C'}
# Ketten: zusammenhängende Schritte derselben Plattengrenze; darin Läufe gleicher Klasse
ketten, cur = [], None
for r in recs:
    a, b = (r['STARTLONG'], r['STARTLAT']), (r['FINALLONG'], r['FINALLAT'])
    pb, cl = r['PLATEBOUND'], r['STEPCLASS']
    anschluss = cur and cur['pb'] == pb and abs(cur['laeufe'][-1][1][-1][0] - a[0]) < 1e-6 and abs(cur['laeufe'][-1][1][-1][1] - a[1]) < 1e-6 and abs(a[0] - b[0]) < 90
    if not anschluss:
        cur = {'pb': pb, 'laeufe': [], 'v': []}
        ketten.append(cur)
    if cur['laeufe'] and cur['laeufe'][-1][0] == cl and anschluss:
        cur['laeufe'][-1][1].append(b)
    else:
        cur['laeufe'].append([cl, [a, b]])
    cur['v'].append(r['VELOCITYLE'])
daten = []
for K in ketten:
    pb = K['pb']
    p1, p2 = pb.replace('\\', '-').replace('/', '-').split('-')[:2]
    rang = 1 if (p1 in GROSS and p2 in GROSS) else 2 if (p1 in GROSS | MITTEL and p2 in GROSS | MITTEL) else 3
    flach, codes = [], ''
    for cl, pts in K['laeufe']:
        q = vereinfache(pts, 0.08)
        if len(q) < 2:
            q = [[r2(pts[0][0]), r2(pts[0][1])], [r2(pts[-1][0]), r2(pts[-1][1])]]
        if flach and flach[-2:] == q[0]:
            q = q[1:]
        elif flach:   # Lücke durch Rundung: Punkt trotzdem übernehmen
            pass
        for x, y in q:
            flach += [x, y]
        codes += CODE[cl] * (len(q) if len(codes) else len(q) - 1)
    # codes: je Teilstrecke (zwischen Punkt i und i+1) ein Buchstabe
    codes = codes[:len(flach) // 2 - 1]
    daten.append([pb, round(statistics.mean(K['v'])), rang, codes, flach])
print('Ketten', len(daten), sum(len(d[4]) // 2 for d in daten), 'Punkte', collections.Counter(c for d in daten for c in d[3]))
pl = shapefile.Reader(os.path.join(D, 'PB2002_plates'))
platten = {}
for sr in pl.iterShapeRecords():
    g = shape(sr.shape.__geo_interface__)
    c, n = sr.record['Code'], sr.record['PlateName']
    if c not in platten or g.area > platten[c][1].area:
        platten[c] = (n, g)
pdat = []
for c, (n, g) in platten.items():
    pt = g.representative_point()
    pdat.append({'c': c, 'n': DE.get(n, n), 'lon': r2(pt.x), 'lat': r2(pt.y), 'rang': 1 if c in GROSS else 2 if c in MITTEL else 3})
schreibe({
    'id': 'platten', 'name': 'Plattengrenzen', 'gruppe': 'Natur', 'typ': 'linien', 'einheit': 'mm/Jahr Relativbewegung',
    'felder': ['pb', 'v_mm_jahr', 'rang', 'codes', 'koord_flach'],
    'codes': {'R': ['auseinander', ARTTXT['OSR']], 'G': ['auseinander', ARTTXT['CRB']], 'S': ['zusammen', ARTTXT['SUB']], 'O': ['zusammen', ARTTXT['OCB']], 'K': ['zusammen', ARTTXT['CCB']], 'T': ['seitlich', ARTTXT['OTF']], 'C': ['seitlich', ARTTXT['CTF']]},
    'legende': [['auseinander (Rücken, Graben)', '#ff6b4a'], ['zusammen (Subduktion, Kollision)', '#4ac8ff'], ['seitlich (Transformstörung)', '#ffd24a']],
    'quellen': [{'t': 'Bird, P. (2003): An updated digital model of plate boundaries. G³ 4(3), 1027, doi:10.1029/2001GC000252 – Modell PB2002; Shapefiles aufbereitet von Hugo Ahlenius, Nordpil (GitHub fraxen/tectonicplates)',
                 'u': 'https://github.com/fraxen/tectonicplates', 'stand': '2003 (Aufbereitung 2014)', 'lizenz': 'Open Data Commons Attribution License (ODC-BY 1.0) – Nennung: Hugo Ahlenius, Nordpil und Peter Bird'}],
    'hinweis': 'Je Eintrag eine zusammenhängende Grenze aus den PB2002-Schritten (5.824), Läufe gleicher Art je für sich vereinfacht (0,08°). koord_flach = [lon0,lat0,lon1,lat1,…]; codes = je Teilstrecke ein Buchstabe (siehe codes). pb = Plattenpaar (Kürzel nach Bird; „/“ bzw. „\\“ zeigt bei Subduktion die Richtung), v = mittlere Relativgeschwindigkeit mm/Jahr.',
    'daten_platten': pdat
}, daten)
