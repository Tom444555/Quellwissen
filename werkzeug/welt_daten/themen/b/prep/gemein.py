"""Gemeinsame Helfer für die Themen-Ebenen (Länder-Codes der App, Schreiben, Runden)."""
import json, os

B = '/home/claude/scratch/themen/b'
ROH = B + '/roh'
FERTIG = B + '/fertig'
APP = json.load(open(ROH + '/app_laender.json'))          # ISO3-Code der App -> deutscher Name
_NE = json.load(open(ROH + '/ne/adm0.geojson'))['features']


def _appcode(p):
    a = p['ADM0_A3']
    if a in APP: return a
    if p['ISO_A3'] in APP: return p['ISO_A3']
    return {'KOS': 'XKX'}.get(a)


A2 = {}    # ISO alpha-2 -> App-Code
FIPS = {}  # GEC/FIPS-10 (CIA Factbook) -> App-Code
for f in _NE:
    p = f['properties']; c = _appcode(p)
    if not c: continue
    for k in ('ISO_A2', 'ISO_A2_EH'):
        v = p.get(k)
        if v and v != '-99' and v not in A2: A2[v] = c
    if p.get('FIPS_10') and p['FIPS_10'] != '-99': FIPS[p['FIPS_10']] = c
A2.setdefault('XK', 'XKX'); FIPS.setdefault('KV', 'XKX'); FIPS.setdefault('OD', 'SSD')
FIPS.update({'IS': 'ISR', 'NO': 'NOR', 'UC': 'CUW'}); FIPS.setdefault('WE', 'PSE'); FIPS.setdefault('WI', 'ESH')


def r2(x):
    return round(float(x), 2)


def schreibe(obj):
    os.makedirs(FERTIG, exist_ok=True)
    p = f"{FERTIG}/{obj['id']}.json"
    s = json.dumps(obj, ensure_ascii=False, separators=(',', ':'))
    open(p, 'w').write(s)
    print(f"{obj['id']}: {len(s)/1024:.1f} KB")
    return p
