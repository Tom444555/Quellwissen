"""Sternbilder (Linien, Namen) und helle Sterne bis Größe 4,5 aus d3-celestial (Olaf Frohn, BSD-3-Clause).
Sterndaten nach XHIP/Hipparcos, Sternbild-Linien und -Namen nach IAU bzw. d3-celestial. Aufruf: python3 -I prep/sternbilder.py"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gemein import ROH, schreibe

H = os.path.join(ROH, 'himmel')
ra = lambda x: round(x % 360, 2)          # d3-celestial: Länge −180…180 = Rektaszension in Grad
de = lambda x: round(x, 2)
C = json.load(open(os.path.join(H, 'constellations.json')))['features']
L = {f['id']: f['geometry']['coordinates'] for f in json.load(open(os.path.join(H, 'constellations.lines.json')))['features']}
S = json.load(open(os.path.join(H, 'stars.6.json')))['features']
N = json.load(open(os.path.join(H, 'starnames.json')))
# eigene deutsche Formen gebräuchlicher Sternnamen (sonst IAU-Name)
DEN = {'Polaris': 'Polarstern', 'Vega': 'Wega', 'Altair': 'Atair', 'Betelgeuse': 'Beteigeuze', 'Canopus': 'Kanopus', 'Achernar': 'Achernar',
       'Rigil Kentaurus': 'Toliman (Alpha Centauri)', 'Fomalhaut': 'Fomalhaut', 'Arcturus': 'Arktur', 'Antares': 'Antares', 'Pollux': 'Pollux'}
sb = []
for f in C:
    p = f['properties']; g = f['geometry']['coordinates']
    lines = [[[ra(a), de(b)] for a, b in seg] for seg in L.get(f['id'], [])]
    sb.append({'k': f['id'], 'n': p['de'].replace(' ', ' '), 'lat': p['name'], 'rang': int(p['rank']), 'ra': ra(g[0]), 'dec': de(g[1]), 'l': lines})
st = []
for f in S:
    m = f['properties']['mag']
    if m > 4.5:
        continue
    nm = N.get(str(f['id']), {})
    name = nm.get('name', '') if m <= 2.6 or nm.get('name') == 'Polaris' else ''
    name = DEN.get(name, name)
    bez = (nm.get('bayer') or nm.get('flam') or '') + (' ' + nm['c'] if nm.get('c') and (nm.get('bayer') or nm.get('flam')) else '')
    st.append([ra(f['geometry']['coordinates'][0]), de(f['geometry']['coordinates'][1]), m, name, bez, 1 if f['id'] == 11767 else 0])
st.sort(key=lambda r: r[2])
pol = [s for s in st if s[5]][0]
print(len(sb), 'Sternbilder', sum(len(x['l']) for x in sb), 'Linienzüge;', len(st), 'Sterne; Polarstern', pol, '; benannt', sum(1 for s in st if s[3]))
schreibe({
    'id': 'sternbilder', 'name': 'Sternbilder und helle Sterne', 'gruppe': 'Himmel', 'typ': 'himmel', 'einheit': 'scheinbare Helligkeit (mag)',
    'koordinaten': 'äquatorial J2000: ra = Rektaszension in Grad (0–360, = 15 × Stunden), dec = Deklination in Grad',
    'felder_sterne': ['ra', 'dec', 'mag', 'name', 'bezeichnung', 'polarstern'],
    'legende': [['helle Sterne (< 1 mag)', '#ffffff'], ['bis 4,5 mag', '#c8d8ff'], ['Sternbild-Linien', '#6a8ac8'], ['Polarstern', '#ffe14a']],
    'quellen': [{'t': 'd3-celestial (Olaf Frohn), Dateien constellations.json, constellations.lines.json, stars.6.json, starnames.json; Sterne nach XHIP (Anderson & Francis 2012, Hipparcos), Sternbilder nach IAU',
                 'u': 'https://github.com/ofrohn/d3-celestial', 'stand': 'Repo-Stand 2026 (Epoche J2000)',
                 'lizenz': 'BSD-3-Clause, Copyright (c) 2015 Olaf Frohn – Hinweis mit Lizenztext muss bei Weitergabe erhalten bleiben'}],
    'hinweis': 'Serpens ist zweigeteilt (Kopf/Schwanz) → 89 Einträge für 88 Sternbilder. Sternnamen: IAU-Eigennamen für Sterne heller als 2,6 mag, einige in gebräuchlicher deutscher Form; deutsche Sternbildnamen aus d3-celestial (nach Wikipedia). Für Globus/Scheibe: Bildpunkt eines Sterns = Ort, über dem er im Zenit steht: lat = dec, lon = ra − 15 × Sternzeit Greenwich (in Stunden).',
    'daten_sterne': st
}, sb)
