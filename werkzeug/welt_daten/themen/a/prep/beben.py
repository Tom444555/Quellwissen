"""Starke Erdbeben M>=7 seit 1900: USGS ComCat (Abfrage-Schnappschüsse in GitHub christophmark/bayesloop, Stand Juni 2026).
Aufruf: python3 -I prep/beben.py"""
import csv, sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gemein import ROH, r2, schreibe, land_von

rows = list(csv.DictReader(open(os.path.join(ROH, 'beben', 'usgs_m7_1900.csv'))))
raus = []
for x in rows:
    if x['type'] != 'earthquake':
        continue
    m = float(x['mag'])
    if m < 7:
        continue
    lon, lat = float(x['longitude']), float(x['latitude'])
    iso, see = land_von(lon, lat)
    rang = 1 if m >= 8 else 2 if m >= 7.5 else 3
    raus.append([x['time'][:10], r2(lon), r2(lat), m, round(float(x['depth'])) if x['depth'] else None, iso, 1 if see else 0, rang])
raus.sort(key=lambda r: (r[7], r[0]))
print(len(raus), collections.Counter(r[7] for r in raus), raus[0][0], max(r[0] for r in raus))
schreibe({
    'id': 'erdbeben', 'name': 'Starke Erdbeben seit 1900', 'gruppe': 'Natur', 'typ': 'punkte', 'einheit': 'Magnitude (Mw u. a.)',
    'felder': ['datum', 'lon', 'lat', 'magnitude', 'tiefe_km', 'iso3', 'meer', 'rang'],
    'legende': [['Magnitude 8 und mehr', '#ff3b30'], ['7,5–7,9', '#ff9500'], ['7,0–7,4', '#ffd60a']],
    'quellen': [{'t': 'U.S. Geological Survey, ANSS Comprehensive Catalog (ComCat), Abfrage minmagnitude=7.0 ab 1900-01-01; Schnappschüsse in GitHub christophmark/bayesloop (docs/source/examples/data/web/earthquakes)',
                 'u': 'https://raw.githubusercontent.com/christophmark/bayesloop/master/docs/source/examples/data/web/earthquakes/manifest.json',
                 'stand': '1900 bis 08.12.2025 (Abruf Juni 2026)', 'lizenz': 'gemeinfrei (US-Bundesbehörde USGS)'}],
    'hinweis': 'iso3 = Land am Epizentrum, bei Beben im Meer (meer=1) das nächste Land im Umkreis von 2,5°; Ländergrenzen aus der App (Natural Earth). Erstes Beben M7+ im Katalog: 1903.'
}, raus)
