"""Prüfskript für alle Themen-Ebenen in fertig/: Pflichtfelder, ISO3 gegen App-Länder, Koordinaten,
Punkt-im-Land-Test (gegen die Länderumrisse der App, mit Toleranz für Küsten/kleine Inseln), Größen. Druckt eine Übersicht."""
import json, glob, os, sys, math
B = '/home/claude/scratch/themen/b'
BASIS = json.load(open('/home/claude/quellwissen/werkzeug/welt_daten/welt_basis.json'))
APP = {x['i']: x for x in BASIS['laender']}
PFLICHT = ['id', 'name', 'gruppe', 'typ', 'einheit', 'legende', 'quellen', 'hinweis', 'daten']
GRUPPEN = {'Menschen', 'Geschichte', 'Wirtschaft', 'Politik'}
TYPEN = {'punkte', 'linien', 'land-wert', 'land-kat', 'land-liste'}
fehler, warn = [], []


def ringe(c):
    p = APP[c]['p']
    # p: Liste von Polygonen oder Ringen [[lon,lat],…]
    out = []
    def walk(x):
        if x and isinstance(x[0], (int, float)): return
        if x and isinstance(x[0], list) and x[0] and isinstance(x[0][0], (int, float)): out.append(x); return
        for y in x: walk(y)
    walk(p); return out


def drin(lon, lat, ring):
    ins = False; j = len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i][0], ring[i][1]; xj, yj = ring[j][0], ring[j][1]
        if (yi > lat) != (yj > lat) and lon < (xj - xi) * (lat - yi) / (yj - yi + 1e-12) + xi: ins = not ins
        j = i
    return ins


def abstand(lon, lat, c):
    best = 1e9
    for r in ringe(c):
        for x, y in r:
            d = math.hypot((x - lon) * math.cos(math.radians(lat)), y - lat)
            best = min(best, d)
    return best


def im_land(lon, lat, c, tol=0.6):
    if c not in APP: return False
    if any(drin(lon, lat, r) for r in ringe(c)): return True
    return abstand(lon, lat, c) <= tol


def isos(obj):
    """alle ISO3-Codes einer Ebene einsammeln"""
    t, d = obj['typ'], obj['daten']
    s = []
    if t in ('land-wert', 'land-kat'): s += list(d.keys())
    if t == 'land-liste':
        for e in d:
            for k in ('l', 'mitglieder', 'partner', 'beobachter', 'kandidaten'):
                v = e.get(k)
                if isinstance(v, list): s += [x if isinstance(x, str) else x[0] for x in v]
                if isinstance(v, dict): s += list(v.keys())
    if t in ('punkte', 'linien'):
        for e in d:
            for k in ('land', 'gast', 'betreiber_iso'):
                if isinstance(e.get(k), str) and len(e[k]) == 3 and e[k].isupper(): s.append(e[k])
            for k in ('laender',):
                if isinstance(e.get(k), list): s += e[k]
    return s


def koords(obj):
    out = []
    def walk(x):
        if isinstance(x, list) and len(x) >= 2 and all(isinstance(v, (int, float)) for v in x[:2]) and not any(isinstance(v, list) for v in x):
            out.append(x[:2]); return
        if isinstance(x, list):
            for y in x: walk(y)
    for e in obj['daten'] if isinstance(obj['daten'], list) else []:
        if 'lon' in e: out.append([e['lon'], e['lat']])
        for k in ('linien', 'w'):
            if k in e: walk(e[k])
        if 'orte' in e:
            for o in e['orte']: out.append([o[1], o[2]])
    return out


zeilen, gesamt = [], 0
for p in sorted(glob.glob(B + '/fertig/*.json')):
    s = open(p).read(); kb = len(s.encode()) / 1024; gesamt += kb
    try: o = json.loads(s)
    except Exception as e: fehler.append(f'{p}: kein JSON ({e})'); continue
    i = o.get('id', os.path.basename(p))
    for k in PFLICHT:
        if k not in o: fehler.append(f'{i}: Pflichtfeld {k} fehlt')
    if o.get('gruppe') not in GRUPPEN: fehler.append(f'{i}: gruppe {o.get("gruppe")}')
    if o.get('typ') not in TYPEN: fehler.append(f'{i}: typ {o.get("typ")}')
    for q in o.get('quellen', []):
        for k in ('t', 'u', 'stand', 'lizenz'):
            if not q.get(k): fehler.append(f'{i}: Quelle ohne {k}: {q.get("t", "")[:40]}')
        if 'NC' in q.get('lizenz', '') or 'GPL' in q.get('lizenz', ''): fehler.append(f'{i}: unzulässige Lizenz {q["lizenz"]}')
    bad = sorted({c for c in isos(o) if c not in APP})
    if bad: fehler.append(f'{i}: unbekannte ISO3 {bad}')
    kk = koords(o)
    for lo, la in kk:
        if not (-180 <= lo <= 180 and -90 <= la <= 90): fehler.append(f'{i}: Koordinate außerhalb {lo},{la}')
        if round(lo, 2) != lo or round(la, 2) != la: warn.append(f'{i}: mehr als 2 Nachkommastellen {lo},{la}')
    # Punkt-im-Land-Test
    if o['typ'] == 'punkte':
        for e in o['daten']:
            c = e.get('land') or e.get('gast')
            if c and 'lon' in e and not e.get('see') and not im_land(e['lon'], e['lat'], c):
                warn.append(f'{i}: „{e.get("n")}“ liegt nicht in {c} ({e["lon"]},{e["lat"]}; Abstand {abstand(e["lon"], e["lat"], c):.2f}°)')
    if o['typ'] == 'land-liste':
        for e in o['daten']:
            if e.get('lon') is not None and e.get('l') and not any(im_land(e['lon'], e['lat'], c) for c in e['l']):
                warn.append(f'{i}: Hauptstadt von „{e.get("n")}“ liegt in keinem der gelisteten Staaten')
    n = len(o['daten'])
    zeilen.append(f"{i:18} {o.get('typ',''):10} {o.get('gruppe',''):10} {n:5} Obj. {kb:7.1f} KB  {len(kk):5} Koord.  Stand: {'; '.join(q.get('stand','') for q in o.get('quellen', []))[:70]}")

print('\n'.join(zeilen))
print(f'GESAMT {gesamt:.1f} KB (Ziel ≤ ca. 600 KB)')
if gesamt > 620: fehler.append(f'Gesamtgröße {gesamt:.0f} KB über Ziel')
print(f'\nWarnungen ({len(warn)}):'); print('\n'.join('  ' + w for w in warn[:80]))
print(f'\nFehler ({len(fehler)}):'); print('\n'.join('  ' + f for f in fehler))
sys.exit(1 if fehler else 0)
