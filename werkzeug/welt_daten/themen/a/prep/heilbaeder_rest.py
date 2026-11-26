"""Heilbäder BW, RP, SH, MV (SL: kein Ort mit Heilmittel-Prädikat) ergänzen – nach dem Beihilfe-Verzeichnis der Senatsverwaltung
für Finanzen Berlin (Anlage zum RS IV Nr. 42/2026, Stand 10/2026), Daten in hb_rest/daten.py, Bericht hb_rest/BERICHT.md.
Wie bisher weggelassen: Seeheil-, Kneipp-, Felke- und reine heilklimatische Orte. Die Art steht nur, wenn das Prädikat sie nennt.
Lage: GeoNames cities1000 (zwei Orte Wikidata) (CC BY 4.0) aus roh/wege/geonames_cities1000_rg.csv (Kopie aus dem Paket reverse_geocoder 1.5.1).
Aufruf (einmal, hängt an fertig/heilbaeder.json an): python3 -I prep/heilbaeder_rest.py"""
import sys, os, csv, json, unicodedata
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, 'hb_rest'))
import daten as D
F = os.path.join(H, '..', 'fertig', 'heilbaeder.json'); ROH = os.path.join(H, '..', 'roh', 'wege', 'geonames_cities1000_rg.csv')
def norm(s):
    s = s.replace('ä', 'a').replace('ö', 'o').replace('ü', 'u').replace('ß', 'ss')
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower().replace('ue', 'u').replace('oe', 'o').replace('ae', 'a')
LAND = {'BW': 'Baden-Wuerttemberg', 'RP': 'Rheinland-Pfalz', 'SH': 'Schleswig-Holstein', 'MV': 'Mecklenburg-Vorpommern'}
GN = {}
# GeoNames-Schreibweisen bzw. fehlende Orte (Lage aus Wikidata Q306405 Bad Schönborn, Q542533 Waldbronn, abgerufen 26.11.2026)
ALIAS = {'Bad Boll': 'Boll', 'Bad Saulgau': 'Saulgau', 'Heringsdorf': 'Seebad Heringsdorf'}
FEST = {'Bad Schonborn': (8.6475, 49.2022), 'Waldbronn': (8.4758, 48.9244)}
for r in csv.DictReader(open(ROH, encoding='utf-8')):
    if r['cc'] == 'DE': GN.setdefault(norm(r['name']), []).append((float(r['lon']), float(r['lat']), r['admin1']))
d = json.load(open(F, encoding='utf-8'))
assert not any(x['land'] in LAND for x in d['daten']), 'schon ergänzt'
neu, fehlt = [], []
for land in LAND:
    for n, praed, art, g in getattr(D, land):
        if art in ('Seeheilbad', 'Kneipp', 'Felke'): continue
        c = [(FEST[g][0], FEST[g][1], LAND[land])] if g in FEST else [q for q in GN.get(norm(ALIAS.get(g, g)), []) if q[2] == LAND[land]]
        if not c: fehlt.append((land, n, g)); continue
        if n in D.ART_ERGAENZT.get(land, []): art = 'Heilbad (Art im Verzeichnis nicht genannt)'
        neu.append({'n': n, 'land': land, 'praedikat': praed, 'art': art, 'lon': round(c[0][0], 2), 'lat': round(c[0][1], 2), 'stand': '10/2026'})
assert not fehlt, fehlt
d['daten'] += neu
q = D.QUELLEN['BW']
d['quellen'].insert(len(d['quellen']) - 2, {'t': q['t'] + ' (für Baden-Württemberg, Rheinland-Pfalz, Saarland, Schleswig-Holstein, Mecklenburg-Vorpommern)', 'u': q['u'], 'stand': q['stand'], 'lizenz': 'amtliches Verzeichnis (Fakten)'})
d['quellen'][-2]['t'] = d['quellen'][-2]['t'].replace('NI, BY, NW, S', 'NI, BY, NW, SN, BW, RP, SH, MV').replace('SN, BW, RP, SH, MVN', 'SN, BW, RP, SH, MV')
h = d['hinweis']
h = h.replace('Sachsen-Anhalt und Brandenburg (amtliche', 'Sachsen-Anhalt, Brandenburg, Baden-Württemberg, Rheinland-Pfalz, Schleswig-Holstein und Mecklenburg-Vorpommern (amtliche')
h = h.replace(', BB 07/2026.', ', BB 07/2026, BW/RP/SH/MV 10/2026 (Beihilfe-Verzeichnis des Landes Berlin, das alle Länder aufführt).')
h = h.replace('Lage NI/BY/NW/SN aus GeoNames', 'Lage NI/BY/NW/SN/BW/RP/SH/MV aus GeoNames')
h = h.replace('Es fehlen Baden-Württemberg, Rheinland-Pfalz, Saarland, Schleswig-Holstein und Mecklenburg-Vorpommern (keine amtliche Liste abrufbar, siehe pruef.md).', 'Das Saarland hat keinen Ort mit Heilmittel-Prädikat (nur Kneipp- bzw. heilklimatische Kurorte). Bad Tönisstein (nur im Berliner Verzeichnis, nicht in der Liste des Landes Rheinland-Pfalz von 2018) ist weggelassen.')
d['hinweis'] = h
json.dump(d, open(F, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':') if '", "' not in open(F).read(300) else None)
print(len(neu), 'Orte ergänzt; je Land', {l: sum(1 for x in neu if x['land'] == l) for l in LAND})
