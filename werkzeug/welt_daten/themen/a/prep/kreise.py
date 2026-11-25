"""Landkreise und kreisfreie Städte: Grenzen VG250 (Stand 01.01.2026, © GeoBasis-DE / BKG 2026, dl-de/by-2-0) aus GitHub
c9wy4794zz-cmyk/kreisgrenzen; Einwohner 31.12.2024 und amtliche Fläche aus Destatis-Gemeindeverzeichnis (GV-ISys) über GitHub Chillchamp1/lab.
Kodierung: je Ring Ganzzahlen in 1/100 Grad, erster Punkt absolut, dann Differenzen. Aufruf: python3 -I prep/kreise.py"""
import sys, os, json, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gemein import ROH, schreibe
from shapely.geometry import shape, Polygon

K = os.path.join(ROH, 'kreise')
meta = {k['id']: k for k in json.load(open(os.path.join(K, 'kreise.json')))}
gj = json.load(open(os.path.join(K, 'kreise.geojson')))
fl = json.load(open(os.path.join(K, 'destatis_stammdaten_flaeche.json')))
ew = {r['kreis_ags']: int(r['bevoelkerung']) for r in csv.DictReader(open(os.path.join(K, 'destatis_bev_2024.csv')))}
BL = {'01': 'SH', '02': 'HH', '03': 'NI', '04': 'HB', '05': 'NW', '06': 'HE', '07': 'RP', '08': 'BW', '09': 'BY', '10': 'SL', '11': 'BE', '12': 'BB', '13': 'MV', '14': 'SN', '15': 'ST', '16': 'TH'}
TOL, MINFL = 0.006, 0.0004     # Grad; kleine Inseln < ca. 3 km² weg (außer größter Teil)


def ring_kod(coords):
    out, px, py = [], None, None
    for x, y in coords:
        ix, iy = round(x * 100), round(y * 100)
        if px is None:
            out += [ix, iy]
        elif (ix, iy) != (px, py):
            out += [ix - px, iy - py]
        else:
            continue
        px, py = ix, iy
    return out


daten = []
for f in gj['features']:
    i = f['properties']['id']; m = meta[i]
    g = shape(f['geometry'])
    polys = list(g.geoms) if g.geom_type == 'MultiPolygon' else [g]
    polys.sort(key=lambda p: -p.area)
    ringe = []
    for k, p in enumerate(polys):
        if k > 0 and p.area < MINFL:
            continue
        q = p.simplify(TOL, preserve_topology=True)
        if q.is_empty:
            continue
        for qq in (list(q.geoms) if q.geom_type == 'MultiPolygon' else [q]):
            r = ring_kod(list(qq.exterior.coords)[:-1])
            if len(r) >= 6:
                ringe.append(r)
    name = m['label']
    daten.append([i, name, m['bez'], BL[i[:2]], ew.get(i), fl.get(i, {}).get('flaeche'), round(m['lon'], 2), round(m['lat'], 2), ringe])
print(len(daten), 'Kreise;', sum(len(r) for d in daten for r in d[8]) // 2, 'Punkte; ohne Einwohner:', [d[1] for d in daten if d[4] is None])
print('Summe Einwohner', sum(d[4] or 0 for d in daten), 'Fläche', round(sum(d[5] or 0 for d in daten)))
schreibe({
    'id': 'kreise', 'name': 'Landkreise und kreisfreie Städte', 'gruppe': 'Deutschland', 'typ': 'kreise', 'einheit': 'Einwohner, km²',
    'felder': ['ags', 'name', 'art', 'land', 'einwohner_2024', 'flaeche_km2', 'lon', 'lat', 'ringe'],
    'kodierung': 'ringe = Liste äußerer Ringe (ohne Löcher); je Ring [x0,y0,dx1,dy1,…] in 1/100 Grad (lon×100, lat×100), erster Punkt absolut, dann Differenzen; Ring ist geschlossen zu denken.',
    'legende': [['Einwohner je km²: < 100', '#2a3a5a'], ['100–300', '#4a6a9a'], ['300–1.000', '#8aa8d8'], ['> 1.000', '#e0ecff']],
    'quellen': [{'t': 'Verwaltungsgebiete 1:250 000 (VG250), Stand 01.01.2026 – © GeoBasis-DE / BKG (2026); vereinfacht von GitHub c9wy4794zz-cmyk/kreisgrenzen (data/kreise.geojson, kreise.json), hier weiter vereinfacht',
                 'u': 'https://github.com/c9wy4794zz-cmyk/kreisgrenzen', 'stand': '01.01.2026', 'lizenz': 'Datenlizenz Deutschland – Namensnennung – 2.0 (dl-de/by-2-0); Nennung „© GeoBasis-DE / BKG (2026)“, Daten verändert (vereinfacht)'},
                {'t': 'Statistisches Bundesamt, Gemeindeverzeichnis (GV-ISys): Kreisfreie Städte und Landkreise nach Fläche, Bevölkerung und Bevölkerungsdichte, Stand 31.12.2024 (Bevölkerung auf Basis Zensus 2022); übernommen aus GitHub Chillchamp1/lab (bevoelkerung-kreise)',
                 'u': 'https://github.com/Chillchamp1/lab/tree/main/bevoelkerung-kreise', 'stand': '31.12.2024', 'lizenz': 'Datenlizenz Deutschland – Namensnennung – 2.0; Quelle: Statistisches Bundesamt (Destatis)'}],
    'hinweis': 'Gebietsstand 01.01.2026: 401 Kreise. Hanau (06415) ist seit 01.01.2026 kreisfrei; Einwohner/Fläche Stand 2024 gibt es dafür noch nicht, sie stecken im Main-Kinzig-Kreis (06435), dessen Werte damit zu hoch sind. Grenzen vereinfacht (Toleranz ca. 500 m, Koordinaten auf ca. 1 km gerundet), nur zur Übersicht.'
}, daten)
