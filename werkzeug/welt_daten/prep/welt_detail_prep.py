#!/usr/bin/env python3
"""Detaildaten für die Weltkarte (Globus, Karte, Scheibe) – werden erst beim Hineinzoomen dekodiert.

Erzeugt  welt_daten/welt_detail.json  (eingebettet als <script id="weltdetail">) aus
  * Natural Earth 1:10 Mio. (gemeinfrei, github.com/nvkelso/natural-earth-vector, Ordner geojson/)
  * GeoNames cities15000/cities5000 (CC BY 4.0, geonames.org; Abzug von 2020 aus dem PyPI-Paket geonamescache)
Aufruf:
  python3 werkzeug/welt_daten/prep/welt_detail_prep.py <ordner-natural-earth> <cities5000.json> <countries.json>
  (Standard: /home/claude/scratch/weltdaten/ne2, …/gn/whl/geonamescache/data/cities5000.json, …/countries.json)
Kodierung: Ringe/Linien als Base64 (1/100 Grad bzw. Q aus 'q', Startpunkt zigzag-Varint, Schritte bis ±7 in einem Byte); Orte als
Namensliste ('|') + Varint-Strom (Delta-Koordinaten, Einwohner, Land, Stufe/Hauptstadt), nach 2°-Zellen sortiert.
"""
import json, math, os, re, sys, base64, unicodedata
import numpy as np
HIER = os.path.dirname(os.path.abspath(__file__)); WD = os.path.dirname(HIER)
sys.path.insert(0, HIER)
from welt_fein_prep import dp, varint, ringe, linien, innenpunkt, DE_NAMEN

NE = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/scratch/weltdaten/ne2'
GN = sys.argv[2] if len(sys.argv) > 2 else '/home/claude/scratch/weltdaten/gn/whl/geonamescache/data/cities5000.json'
GC = sys.argv[3] if len(sys.argv) > 3 else os.path.join(os.path.dirname(GN), 'countries.json')
ALT = '/home/claude/scratch/weltdaten'  # Rohdaten der Feindaten (10m-Flüsse)

def lade(n):
    for d in (NE, ALT):
        p = os.path.join(d, n + '.geojson')
        if os.path.exists(p): return json.load(open(p))['features']
    raise FileNotFoundError(n)

def uvarint(out, v):
    while True:
        b = v & 0x7f; v >>= 7
        if v: out.append(b | 0x80)
        else: out.append(b); return
def b64(out): LETZT[0] = LETZT[1] = 0; return base64.b64encode(bytes(out)).decode()
def dp3(pts, tol):
    pts = np.asarray(pts, float)
    if len(pts) < 3: return pts
    if len(pts) < 5: pts = np.vstack([pts[:1], pts[1:-1], pts[1:-1], pts[-1:]]) if len(pts) == 3 else pts
    r = dp(np.vstack([pts, pts[-1:]]) if len(pts) < 5 else pts, tol)
    return r[np.r_[True, np.any(np.diff(r, axis=0) != 0, axis=1)]]
def norm(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z]', '', s)
def nm(p, *keys):
    for k in keys:
        v = p.get(k)
        if v and str(v).strip(): return ' '.join(str(v).replace('‎', '').split())
    return None

def linienN(features, tol, rang, Q=100):
    """wie linien(), aber jede Linie mit Rang aus rang(p); Quantisierung Q je Grad"""
    out = bytearray(); n = 0
    for ft in features:
        g = ft['geometry']; p = ft['properties']; sr = rang(p) if g else None
        if sr is None: continue
        ls = g['coordinates'] if g['type'] == 'MultiLineString' else [g['coordinates']]
        for l in ls:
            q = np.round(dp3(l, tol) * Q).astype(np.int64)
            q = q[np.r_[True, np.any(np.diff(q, axis=0) != 0, axis=1)]]
            if len(q) < 2: continue
            varint(out, sr); punkte(out, q)
            n += len(q)
    return b64(out), n

LETZT = [0, 0]
def punkte(out, q):
    """Anzahl, Startpunkt (zigzag, als Abstand zum Endpunkt der vorigen Linie/des vorigen Rings), dann Schritte: |dx|,|dy| <= 7 als ein Byte (dx+7)*15+(dy+7), sonst 225 + zwei zigzag-Varints"""
    varint(out, len(q)); varint(out, int(q[0, 0]) - LETZT[0]); varint(out, int(q[0, 1]) - LETZT[1])
    LETZT[0], LETZT[1] = int(q[-1, 0]), int(q[-1, 1])
    for dx, dy in np.diff(q, axis=0):
        dx = int(dx); dy = int(dy)
        if -7 <= dx <= 7 and -7 <= dy <= 7: out.append((dx + 7) * 15 + dy + 7)
        else: out.append(225); varint(out, dx); varint(out, dy)

def ringeQ(features, tol, minfl=0.0, Q=100):
    """wie ringe() aus welt_fein_prep, aber mit wählbarer Quantisierung Q je Grad"""
    out = bytearray(); n = 0; r = 0
    for ft in features:
        for p in polys(ft['geometry']):
            for ring in p:
                q = np.round(dp3(ring, tol) * Q).astype(np.int64)
                q = q[np.r_[True, np.any(np.diff(q, axis=0) != 0, axis=1)]]
                if len(q) > 1 and (q[0] == q[-1]).all(): q = q[:-1]
                if len(q) < 3: continue
                x, y = q[:, 0].astype(float), q[:, 1].astype(float)
                if abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1))) / 2 / Q / Q < minfl: continue
                punkte(out, q)
                n += len(q); r += 1
    return b64(out), n, r

def polys(g):
    return g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]

def achse(ring):
    """Beschriftungswinkel (Grad, gegen den Uhrzeigersinn ab Osten) für langgestreckte Flächen, sonst None"""
    a = np.asarray(ring, float); la = a[:, 1].mean(); x = (a[:, 0] - a[:, 0].mean()) * math.cos(math.radians(la)); y = a[:, 1] - la
    c = np.cov(np.vstack([x, y])); w, v = np.linalg.eigh(c)
    if w[0] <= 0 or math.sqrt(w[1] / max(w[0], 1e-12)) < 2.3: return None
    ang = math.degrees(math.atan2(v[1, 1], v[0, 1]))
    if ang > 90: ang -= 180
    if ang <= -90: ang += 180
    return int(round(ang)) if abs(ang) > 4 else None

def flaeche_km2(ring):
    a = np.asarray(ring, float); la = a[:, 1].mean()
    f = abs(np.dot(a[:, 0], np.roll(a[:, 1], 1)) - np.dot(a[:, 1], np.roll(a[:, 0], 1))) / 2
    return f * 111.2 ** 2 * math.cos(math.radians(la))

def main():
    basis = json.load(open(os.path.join(WD, 'welt_basis.json'))); fein = json.load(open(os.path.join(WD, 'welt_fein.json')))
    D = {'v': 1}
    # ---------- 1. Orte (GeoNames) ----------
    gn = list(json.load(open(GN)).values()); co = json.load(open(GC))
    A = set('DE AT CH LI LU NL BE DK PL CZ FR'.split())
    gn = [c for c in gn if c['population'] >= 15000 or (c['countrycode'] in A and c['population'] >= 5000)]
    alt = basis['staedte'] + fein['staedte']
    ax = np.array([[s[1], s[2]] for s in alt]); an = [norm(s[0]) for s in alt]
    de_rueck = {}
    for k, v in DE_NAMEN.items(): de_rueck.setdefault(norm(k), v)
    hst = {}
    for c in co.values():
        if c.get('capital'): hst[c['iso']] = norm(c['capital'])
    laender = {c['iso']: [c['iso3'], c['name']] for c in co.values()}
    neu = []; dub = 0
    gn.sort(key=lambda c: -c['population'])
    hs_da = set()
    for c in gn:
        lo, la = c['longitude'], c['latitude']; n = ' '.join(c['name'].split()); nn = norm(n)
        n = DE_NAMEN.get(n, n)
        d = np.hypot((ax[:, 0] - lo) * math.cos(math.radians(la)), ax[:, 1] - la); j = np.where(d < 0.12)[0]
        doppelt = any(d[i] < 0.02 for i in j)
        for i in j:
            a = an[i]; b = norm(n)
            if a == b or a == nn or (len(a) > 3 and len(b) > 3 and (a.startswith(b) or b.startswith(a) or a[:6] == b[:6] or a[:6] == nn[:6])): doppelt = True; break
        if doppelt: dub += 1; continue
        hs = 1 if (c['countrycode'] not in hs_da and hst.get(c['countrycode']) == nn) else 0
        if hs: hs_da.add(c['countrycode'])
        p = c['population']; mz = 7 + 1.5 * (6 - math.log10(max(p, 1000)))
        mz = round(max(6.5, min(11, mz)), 1)
        neu.append([n, round(lo, 2), round(la, 2), p, c['countrycode'], mz, hs])
    # Sortierung: 2°-Zelle, innerhalb nach Stufe (= Größe)
    zelle = lambda s: (int((s[1] + 180) // 2), int((s[2] + 90) // 2))
    neu.sort(key=lambda s: (zelle(s), s[5], -s[3]))
    import collections
    lc = [k for k, _ in collections.Counter(s[4] for s in neu).most_common()]; li = {k: i for i, k in enumerate(lc)}
    out = bytearray(); px = py = 0
    for s in neu:  # je Ort: dx, dy (zigzag), Einwohner, Landindex (nach Häufigkeit), ohne Vorzeichen
        x, y = int(round(s[1] * 100)), int(round(s[2] * 100))
        varint(out, x - px); varint(out, y - py); px, py = x, y
        uvarint(out, s[3]); uvarint(out, li[s[4]])
    D['orte'] = {'n': '|'.join(s[0] for s in neu), 'k': b64(out), 'l': [laender.get(k, [k, k]) for k in lc],
                 'h': [i for i, s in enumerate(neu) if s[6]]}
    print('Orte', len(neu), 'neu,', dub, 'Dubletten entfernt;', (len(D['orte']['n']) + len(D['orte']['k'])) // 1024, 'KB')

    # ---------- 2. Flüsse (Zusatzsätze) + Flussnamen ----------
    rang = lambda p: int(p.get('scalerank') or 12) if p.get('featurecla') in ('River', 'River (Intermittent)', 'Intermittent River', 'Canal') else None
    reg = lade('ne_10m_rivers_europe') + lade('ne_10m_rivers_north_america') + lade('ne_10m_rivers_australia')
    D['fluesse'], nf = linienN(reg, 0.02, rang)
    print('Flüsse (Zusatz)', nf, 'Punkte', len(D['fluesse']) // 1024, 'KB')
    haupt = lade('ne_10m_rivers_lake_centerlines')
    fn = []
    for ft in haupt + reg:
        p = ft['properties']; g = ft['geometry']
        if not g or rang(p) is None: continue
        n = nm(p, 'name_de', 'name', 'name_en')
        if not n: continue
        sr = rang(p); st = float(p.get('min_label') or (sr + 2)); schritt = 6 if sr <= 4 else 4 if sr <= 8 else 2.2
        for l in (g['coordinates'] if g['type'] == 'MultiLineString' else [g['coordinates']]):
            a = np.asarray(l, float)
            if len(a) < 2: continue
            seg = np.hypot(np.diff(a[:, 0]) * np.cos(np.radians(a[:-1, 1])), np.diff(a[:, 1])); s = np.r_[0, np.cumsum(seg)]; L = s[-1]
            if L < schritt * .5: continue
            k = max(1, int(L / schritt));
            for t in ((np.arange(k) + .5) * L / k):
                i = int(np.searchsorted(s, t)); i = max(1, min(len(a) - 1, i))
                i0 = int(np.searchsorted(s, t - .12)); i1 = int(np.searchsorted(s, t + .12)); i0 = max(0, min(i0, len(a) - 1)); i1 = max(0, min(i1, len(a) - 1))
                if i1 == i0: i1 = min(len(a) - 1, i0 + 1); i0 = max(0, i1 - 1)
                f = (t - s[i - 1]) / max(s[i] - s[i - 1], 1e-9); P = a[i - 1] + (a[i] - a[i - 1]) * f
                dx = (a[i1, 0] - a[i0, 0]) * math.cos(math.radians(P[1])); dy = a[i1, 1] - a[i0, 1]
                ang = math.degrees(math.atan2(dy, dx))
                if ang > 90: ang -= 180
                if ang <= -90: ang += 180
                fn.append([n, round(P[0], 2), round(P[1], 2), int(round(ang)), round(max(st, 3), 1)])
    fn.sort(key=lambda f: f[4])
    D['flussN'] = fn
    print('Flussnamen', len(fn), len(json.dumps(fn, ensure_ascii=False)) // 1024, 'KB')

    # ---------- 3. Land, Inseln, Seen, Eis, Salz, Riffe ----------
    D['land'], n1, r1 = ringeQ(lade('ne_10m_land'), 0.016, 0.0004)
    D['inseln'], n2, r2 = ringeQ(lade('ne_10m_minor_islands'), 0.006, 0.00005)
    seen = lade('ne_10m_lakes') + lade('ne_10m_lakes_europe') + lade('ne_10m_lakes_north_america')
    D['seen'], n3, r3 = ringeQ(seen, 0.012, 0.0004)
    D['eis'], n4, r4 = ringeQ(lade('ne_10m_glaciated_areas'), 0.02, 0.001)
    D['schelf'], n5, r5 = ringeQ(lade('ne_10m_antarctic_ice_shelves_polys'), 0.02, 0.001)
    D['salz'], n6, r6 = ringeQ(lade('ne_10m_playas'), 0.01, 0.0005)
    D['riffe'], n7 = linienN(lade('ne_10m_reefs'), 0.01, lambda p: 0)
    for k, r, n in [('land', r1, n1), ('inseln', r2, n2), ('seen', r3, n3), ('eis', r4, n4), ('schelf', r5, n5), ('salz', r6, n6)]:
        print(k, r, 'Ringe', n, 'Punkte', len(D[k]) // 1024, 'KB')
    print('riffe', n7, len(D['riffe']) // 1024, 'KB')
    alteSeen = {norm(s[0]) for s in fein['seeN']}; sx = np.array([[s[1], s[2]] for s in fein['seeN']])
    sn = []
    for ft in seen:
        p = ft['properties']; n = nm(p, 'name_de', 'name')
        if not n: continue
        if p.get('name_de') and n.endswith('er') and ' ' not in n and n != p.get('name'): n += ' See'  # „Comer“ → „Comer See“
        big = max(polys(ft['geometry']), key=lambda pp: len(pp[0]))
        lo, la = innenpunkt(big)
        if any(s[0] == n for s in sn) or norm(n) in alteSeen or np.hypot(sx[:, 0] - lo, sx[:, 1] - la).min() < 0.05: continue
        km2 = flaeche_km2(big[0])
        st = round(min(11, max(6, 9.6 - 1.5 * math.log10(max(km2, 5) / 100))), 1)
        if km2 < 12: continue
        sn.append([n, lo, la, st])
    sn.sort(key=lambda s: s[3]); D['seeN'] = sn
    print('Seenamen neu', len(sn))

    # ---------- 4. Landschaften, Meere, Gipfel ----------
    ART = {'Range/mtn': 'g', 'Plateau': 'g', 'Foothills': 'g', 'Desert': 'w', 'Plain': 'e', 'Lowland': 'e', 'Basin': 'e', 'Depression': 'e', 'Valley': 'e', 'Tundra': 'e',
           'Wetlands': 'e', 'Delta': 'e', 'Gorge': 'e', 'Geoarea': 'e', 'Peninsula': 'h', 'Pen/cape': 'h', 'Isthmus': 'h', 'Coast': 'h', 'Island': 'i', 'Island group': 'i'}
    altR = [(norm(r[0]), r[2], r[3]) for r in basis['regionen']] + [(norm(m[0]), m[1], m[2]) for m in fein['marken']]
    meere_js = re.findall(r"\['([^']+)',(-?[\d.]+),(-?[\d.]+),", open(os.path.join(WD, '..', 'welt.js')).read().split('const MEERE=')[1].split(';')[0])
    altR += [(norm(n), float(a), float(b)) for n, a, b in meere_js]
    def schon(n, lo, la, r=3.0):
        a = norm(n)
        return any(a == b and abs(lo - x) < r * 3 and abs(la - y) < r * 2 for b, x, y in altR)
    geo = []
    for ft in lade('ne_10m_geography_regions_polys'):
        p = ft['properties']; art = ART.get(p.get('FEATURECLA'))
        if not art: continue
        n = nm(p, 'NAME_DE', 'NAME'); big = max(polys(ft['geometry']), key=lambda pp: len(pp[0]))
        lo, la = innenpunkt(big)
        if schon(n, lo, la): continue
        st = float(p.get('MIN_LABEL') or 6); w = achse(big[0]) if art in 'gwe' else None
        geo.append([n, lo, la, round(st, 1), art] + ([w] if w is not None else []))
    for ft in lade('ne_10m_geography_regions_points'):
        p = ft['properties']; fc = p.get('featurecla'); art = {'island': 'i', 'island group': 'i', 'cape': 'k', 'waterfall': 'f', 'plain': 'e'}.get(fc)
        if not art: continue
        n = nm(p, 'name_de', 'name'); lo, la = ft['geometry']['coordinates']
        if schon(n, lo, la, 1): continue
        geo.append([n, round(lo, 2), round(la, 2), float(p.get('min_zoom') or 6), art])
    MA = {'sea': 'm', 'gulf': 'b', 'bay': 'b', 'strait': 's', 'sound': 's', 'channel': 's', 'lagoon': 'b', 'fjord': 'b', 'inlet': 'b', 'generic': 'm', 'reef': 'b'}
    for ft in lade('ne_10m_geography_marine_polys'):
        p = ft['properties']; art = MA.get(p.get('featurecla'))
        if not art: continue
        n = nm(p, 'name_de', 'name')
        if not n: continue
        big = max(polys(ft['geometry']), key=lambda pp: len(pp[0])); lo, la = innenpunkt(big)
        if schon(n, lo, la): continue
        st = float(p.get('min_label') or (p.get('scalerank') or 5) + 1); w = achse(big[0])
        geo.append([n, lo, la, round(max(st, 2.5), 1), art] + ([w] if w is not None else []))
    geo.sort(key=lambda g: g[3]); D['geo'] = geo
    print('Landschafts-/Meeresnamen', len(geo), len(json.dumps(geo, ensure_ascii=False)) // 1024, 'KB')
    ag = np.array([[g[1], g[2]] for g in basis['gipfel']]); gi = []
    for ft in lade('ne_10m_geography_regions_elevation_points'):
        p = ft['properties']; lo, la = ft['geometry']['coordinates']; hm = p.get('elevation')
        if hm is None or p.get('featurecla') not in ('mountain', 'spot elevation', 'depression', 'pass', 'plateau'): continue
        if np.hypot(ag[:, 0] - lo, ag[:, 1] - la).min() < 0.15: continue
        n = nm(p, 'name_de', 'name')
        if not n: continue
        gi.append([n, round(lo, 2), round(la, 2), int(hm), float(p.get('min_zoom') or 7)])
    gi.sort(key=lambda g: g[4]); D['gipfel'] = gi
    print('Gipfel neu', len(gi))

    # ---------- 5. Innere Grenzen, umstrittene Grenzen ----------
    a1 = [f for f in lade('ne_10m_admin_1_states_provinces_lines') if f['properties']['FEATURECLA'] in ('Admin-1 boundary', 'Unrecognized Admin-1 boundary')]
    D['a1'], na = linienN(a1, 0.05, lambda p: int(p.get('SCALERANK') or 9), 50)
    print('Gliedstaaten-Grenzen', len(a1), na, 'Punkte', len(D['a1']) // 1024, 'KB')
    a1n = []
    for ft in lade('ne_10m_admin_1_states_provinces'):
        p = ft['properties']; n = nm(p, 'name_de', 'name')
        if not n or p.get('latitude') is None: continue
        n = re.sub(r'^(Département|Departement|Provinz|Region|Gouvernement|Woiwodschaft|Kreis|Oblast|Distrikt) ', '', n)
        st = float(p.get('min_label') or 9)
        if st > 9.5: continue
        a1n.append([n, round(p['longitude'], 2), round(p['latitude'], 2), round(st, 1)])
    a1n.sort(key=lambda a: a[3]); D['a1N'] = a1n
    print('Gliedstaaten-Namen', len(a1n))
    D['strittig'], ns = linienN(lade('ne_10m_admin_0_boundary_lines_disputed_areas'), 0.01, lambda p: 0)
    print('umstrittene Linien', ns)

    # ---------- 6. Verkehr, Siedlung, Zeitzonen ----------
    D['strassen'], nr = linienN(lade('ne_10m_roads'), 0.04, lambda p: int(p['scalerank']) if p.get('featurecla') == 'Road' and (p.get('scalerank') or 99) <= 4 else None, 50)
    D['bahn'], nb = linienN(lade('ne_10m_railroads'), 0.04, lambda p: int(p['scalerank']) if (p.get('scalerank') or 99) <= 6 else None, 50)
    print('Straßen', nr, len(D['strassen']) // 1024, 'KB  Bahn', nb, len(D['bahn']) // 1024, 'KB')
    D['haefen'] = sorted([[nm(f['properties'], 'name'), round(f['geometry']['coordinates'][0], 2), round(f['geometry']['coordinates'][1], 2), int(f['properties']['scalerank'])] for f in lade('ne_10m_ports') if nm(f['properties'], 'name')], key=lambda x: x[3])
    fl = []
    for f in lade('ne_10m_airports'):
        p = f['properties']; n = nm(p, 'name_de', 'name')
        if not n: continue
        fl.append([n, round(f['geometry']['coordinates'][0], 2), round(f['geometry']['coordinates'][1], 2), int(p['scalerank']), p.get('iata_code') or ''])
    D['flug'] = sorted(fl, key=lambda x: x[3])
    urb = [f for f in lade('ne_10m_urban_areas') if (f['properties'].get('area_sqkm') or 0) >= 50]
    D['stadtfl'], nu, ru = ringeQ(urb, 0.012, 0.0008, 50)
    print('Häfen', len(D['haefen']), 'Flughäfen', len(fl), 'bebaute Flächen', ru, nu, len(D['stadtfl']) // 1024, 'KB')
    tz = lade('ne_10m_time_zones'); D['zonen'], nz, rz = ringeQ(tz, 0.05, 0.01, 20)
    zn = []
    for f in tz:
        p = f['properties']; big = max(polys(f['geometry']), key=lambda pp: flaeche_km2(pp[0]))
        if flaeche_km2(big[0]) < 2e5: continue
        lo, la = innenpunkt(big); zn.append([p.get('time_zone') or p.get('name'), lo, la])
    D['zonenN'] = zn
    print('Zeitzonen', rz, len(D['zonen']) // 1024, 'KB', len(zn), 'Namen')
    D['q'] = {'a1': 50, 'strassen': 50, 'bahn': 50, 'stadtfl': 50, 'zonen': 20}  # Quantisierung (sonst 100 je Grad)
    D['stand'] = 'Natural Earth 10m (v5) · GeoNames cities15000/5000 (Abzug 2020)'
    p = os.path.join(WD, 'welt_detail.json')
    json.dump(D, open(p, 'w'), ensure_ascii=False, separators=(',', ':'))
    print('welt_detail.json', os.path.getsize(p) // 1024, 'KB')
    for k, v in D.items(): print('  ', k, len(json.dumps(v, ensure_ascii=False)) // 1024, 'KB')

if __name__ == '__main__':
    main()
