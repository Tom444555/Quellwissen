"""Prüft alle Themen-Dateien in fertig/: Pflichtfelder im Kopf, Quellen, Koordinatenbereiche, Rasterlängen, Größe.
Aufruf: python3 -I prep/pruefen.py   (Rückgabe 1 bei Fehlern)"""
import json, os, glob, base64, sys

BASIS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PFLICHT = ['id', 'name', 'gruppe', 'typ', 'einheit', 'legende', 'quellen', 'hinweis', 'daten']
GRUPPEN = {'Natur', 'Himmel', 'Deutschland'}
TYPEN = {'punkte', 'linien', 'flaechen', 'raster', 'land-wert', 'land-kat', 'kreise', 'himmel'}
fehler = []


def F(datei, text):
    fehler.append(f'{datei}: {text}')


def lonlat(datei, lon, lat, wo, de=False):
    if lon is None and lat is None:
        return 0
    if not (-180 <= lon <= 180 and -90 <= lat <= 90):
        F(datei, f'Koordinate außerhalb {wo}: {lon},{lat}')
    if de and not (5.5 <= lon <= 15.5 and 47 <= lat <= 55.2):
        F(datei, f'außerhalb Deutschlands {wo}: {lon},{lat}')
    return 1


def pruefe(p):
    d = json.load(open(p, encoding='utf-8'))
    n = os.path.basename(p)
    for k in PFLICHT:
        if k not in d:
            F(n, f'Pflichtfeld fehlt: {k}')
    if d.get('gruppe') not in GRUPPEN:
        F(n, f"gruppe ungültig: {d.get('gruppe')}")
    if d.get('typ') not in TYPEN:
        F(n, f"typ ungültig: {d.get('typ')}")
    for q in d.get('quellen', []):
        for k in ('t', 'u', 'stand', 'lizenz'):
            if not q.get(k):
                F(n, f'Quelle ohne {k}: {q.get("t", "?")[:40]}')
    D, i, de = d['daten'], d['id'], d.get('gruppe') == 'Deutschland'
    obj = 0
    if i == 'vulkane':
        for v in D: lonlat(n, v[1], v[2], v[0]); assert v[6] in (1, 2, 3)
        obj = len(D)
    elif i == 'erdbeben':
        for v in D:
            lonlat(n, v[1], v[2], v[0])
            if not (7 <= v[3] <= 10): F(n, f'Magnitude {v[3]}')
        obj = len(D)
    elif i == 'platten':
        for v in D:
            c = v[4]
            if len(v[3]) != len(c) // 2 - 1: F(n, f'codes passen nicht: {v[0]}')
            for k in range(0, len(c), 2): lonlat(n, c[k], c[k + 1], v[0])
        for pl in d['daten_platten']: lonlat(n, pl['lon'], pl['lat'], pl['n'])
        obj = len(D) + len(d['daten_platten'])
    elif i in ('meeresstroemungen', 'sonnenfinsternisse'):
        for v in D:
            for t in v['p']:
                for x, y in t: lonlat(n, x, y, v.get('n', v.get('datum')))
            if i == 'sonnenfinsternisse': lonlat(n, v['lon'], v['lat'], v['datum'])
        obj = len(D)
    elif i == 'windguertel':
        for v in D:
            if not (-90 <= v[1] < v[2] <= 90): F(n, f'Band {v[0]}')
        for m in d['daten_monsun']:
            a, b, c2, e = m[1]; lonlat(n, a, b, m[0]); lonlat(n, c2, e, m[0])
        obj = len(D) + len(d['daten_monsun'])
    elif d['typ'] == 'raster':
        r = d['raster']; soll = r['zeilen'] * r['spalten']
        bloecke = D.values() if isinstance(D, dict) else [D]
        for b in bloecke:
            if len(base64.b64decode(b)) != soll: F(n, 'Rasterlänge falsch')
        obj = soll
    elif d['typ'] == 'land-wert':
        for k, v in D.items():
            if len(k) != 3 or not isinstance(v, (int, float)): F(n, f'Eintrag {k}')
        obj = len(D)
    elif i == 'pflanzen_heimat':
        for k, v in D.items():
            for c in v['heimat'] + v['eingeb']:
                if len(c) != 3: F(n, f'ISO3 {c}')
        obj = len(D)
    elif i == 'sternbilder':
        for s in d['daten_sterne']:
            if not (0 <= s[0] < 360 and -90 <= s[1] <= 90): F(n, f'Stern {s}')
        for c in D:
            for seg in c['l']:
                for a, b in seg:
                    if not (0 <= a < 360 and -90 <= b <= 90): F(n, f'Linie {c["k"]}')
        if sum(1 for s in d['daten_sterne'] if s[5]) != 1: F(n, 'Polarstern nicht genau einmal')
        obj = len(D) + len(d['daten_sterne'])
    elif i == 'kreise':
        for k in D:
            lonlat(n, k[6], k[7], k[1], True)
            for rg in k[8]:
                x, y = rg[0], rg[1]
                for j in range(2, len(rg), 2): x += rg[j]; y += rg[j + 1]
                lonlat(n, rg[0] / 100, rg[1] / 100, k[1], True)
        obj = len(D)
    elif i == 'wanderwege':
        for w in D:
            for x, y, o in w['p']: lonlat(n, x, y, o, True)
            if not w.get('schema'): F(n, f'schema fehlt: {w["n"]}')
        obj = len(D)
    elif isinstance(D, list):   # Punktlisten mit lon/lat
        for v in D: obj += 1; lonlat(n, v.get('lon'), v.get('lat'), v.get('n'), de)
        for v in d.get('daten_hopfen', []): obj += 1; lonlat(n, v['lon'], v['lat'], v['n'], de)
    kb = os.path.getsize(p) / 1024
    return i, d['gruppe'], d['typ'], obj, kb


zeilen = [pruefe(p) for p in sorted(glob.glob(os.path.join(BASIS, 'fertig', '*.json')))]
print(f"{'id':22} {'Gruppe':12} {'Typ':10} {'Objekte':>8} {'KB':>7}")
for i, g, t, o, kb in zeilen:
    print(f'{i:22} {g:12} {t:10} {o:8d} {kb:7.1f}')
ges = sum(z[4] for z in zeilen)
print(f"{'Summe':57} {ges:7.1f}")
if ges > 620:
    fehler.append(f'Gesamtgröße {ges:.0f} KB über Ziel (ca. 600 KB)')
print('\n'.join(['FEHLER: ' + f for f in fehler]) if fehler else 'Keine Fehler.')
sys.exit(1 if fehler else 0)
