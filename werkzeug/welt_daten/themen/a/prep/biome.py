"""Biome (Vegetationszonen) als 2°-Raster aus RESOLVE Ecoregions 2017 (Dinerstein et al. 2017, CC BY 4.0),
vereinfachte TopoJSON-Fassung aus GitHub CG-SO/mfl-living-landscapes (data/ecoregions.js). Je Zelle Mehrheit aus 4×4 Stichpunkten.
Aufruf: python3 -I prep/biome.py"""
import sys, os, json, base64, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gemein import ROH, schreibe
from shapely.geometry import Polygon, MultiPolygon, Point
from shapely.strtree import STRtree
from shapely.validation import make_valid

s = open(os.path.join(ROH, 'biome', 'ecoregions.js')).read()
t = json.loads(s[s.index('{'):].rstrip().rstrip(';'))
sc, tr = t['transform']['scale'], t['transform']['translate']
arcs = []
for a in t['arcs']:
    x = y = 0; pts = []
    for dx, dy in a:
        x += dx; y += dy; pts.append((x * sc[0] + tr[0], y * sc[1] + tr[1]))
    arcs.append(pts)


def ring(idx):
    out = []
    for i in idx:
        p = arcs[i] if i >= 0 else arcs[~i][::-1]
        out.extend(p if not out else p[1:])
    return out


geoms, biom = [], []
for g in t['objects']['Ecoregions2017']['geometries']:
    polys = []
    if g['type'] == 'Polygon':
        polys = [g['arcs']]
    elif g['type'] == 'MultiPolygon':
        polys = g['arcs']
    for P in polys:
        rings = [ring(r) for r in P]
        if len(rings[0]) < 4:
            continue
        geoms.append(make_valid(Polygon(rings[0], [r for r in rings[1:] if len(r) >= 4])))
        biom.append(g['properties']['b'])
tree = STRtree(geoms)
NAMEN = {1: 'Tropischer und subtropischer Feuchtwald', 2: 'Tropischer und subtropischer Trockenwald', 3: 'Tropischer und subtropischer Nadelwald',
         4: 'Gemäßigter Laub- und Mischwald', 5: 'Gemäßigter Nadelwald', 6: 'Borealer Nadelwald (Taiga)', 7: 'Tropisches Grasland und Savanne',
         8: 'Gemäßigtes Grasland (Steppe, Prärie)', 9: 'Überflutetes Grasland', 10: 'Gebirgsgrasland und -gebüsch', 11: 'Tundra',
         12: 'Mittelmeerwald und Hartlaubgebüsch', 13: 'Wüste und Trockengebüsch', 14: 'Mangroven'}
FARBE = {1: '#1f8a3a', 2: '#7aa83a', 3: '#4a9a6a', 4: '#3aa050', 5: '#2f7a5a', 6: '#1f5a5a', 7: '#c8b840', 8: '#b8c86a', 9: '#5ab0b0',
         10: '#a08a68', 11: '#9aa890', 12: '#8aa850', 13: '#e8c88a', 14: '#2a8a8a'}
buf = bytearray(); zahl = collections.Counter()
for la in range(89, -90, -2):
    for lo in range(-179, 180, 2):
        c = collections.Counter()
        for dy in (-0.75, -0.25, 0.25, 0.75):
            for dx in (-0.75, -0.25, 0.25, 0.75):
                p = Point(lo + dx, la + dy)
                for k in tree.query(p):
                    if geoms[k].contains(p):
                        c[biom[k]] += 1; break
        if c and sum(c.values()) >= 4:          # mind. 1/4 der Zelle Land mit Biom
            b = c.most_common(1)[0][0]
        else:
            b = 0
        buf.append(b); zahl[b] += 1
print(zahl)
def bei(la, lo): return buf[((89 - la) // 2) * 180 + (lo + 179) // 2]
for n, la, lo in [('Deutschland', 51, 9), ('Sahara', 23, 5), ('Amazonas', -3, -61), ('Sibirien', 61, 101), ('Serengeti', -3, 35), ('Spanien', 39, -5)]:
    print(n, NAMEN.get(bei(la, lo)))
schreibe({
    'id': 'biome', 'name': 'Vegetationszonen (Biome)', 'gruppe': 'Natur', 'typ': 'raster', 'einheit': '',
    'raster': {'zellen': '2°', 'zeilen': 90, 'spalten': 180, 'start_lat': 89, 'start_lon': -179, 'schritt': 2,
               'reihenfolge': 'wie klima_raster: Index = ((89-lat)/2)*180 + (lon+179)/2', 'kodierung': 'Base64, 1 Byte = Biom-Nummer (0 = Meer, Eis/Fels oder keine Angabe)'},
    'klassen': {str(k): [NAMEN[k], FARBE[k]] for k in NAMEN},
    'legende': [[NAMEN[k], FARBE[k]] for k in NAMEN],
    'quellen': [{'t': 'Dinerstein, E. et al. (2017): An Ecoregion-Based Approach to Protecting Half the Terrestrial Realm. BioScience 67(6):534–545 – RESOLVE Ecoregions 2017; vereinfachte TopoJSON-Fassung in GitHub CG-SO/mfl-living-landscapes (data/ecoregions.js, mit mapshaper vereinfacht)',
                 'u': 'https://github.com/CG-SO/mfl-living-landscapes', 'stand': '2017', 'lizenz': 'CC BY 4.0 – Nennung: RESOLVE Ecoregions 2017 (Dinerstein et al. 2017)'}],
    'hinweis': '14 Biome nach RESOLVE/WWF. Je 2°-Zelle das häufigste Biom aus 16 Stichpunkten (Zelle zählt, wenn mind. 4 Punkte auf einer Ökoregion liegen). Ersetzt bzw. verfeinert das bisherige Vegetations-Schema (VEGN). Wälder = Biome 1–6 und 14.'
}, base64.b64encode(bytes(buf)).decode())
