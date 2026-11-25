"""Gemeinsame Helfer für die Themen-Ebenen (Schreiben, Runden, Vereinfachen)."""
import json, os

BASIS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROH = os.path.join(BASIS, 'roh')
FERTIG = os.path.join(BASIS, 'fertig')


def r2(x):
    """Auf 1/100 Grad runden (kompakt)."""
    v = round(float(x), 2)
    return int(v) if v == int(v) else v


def schreibe(kopf, daten):
    """kopf: dict mit id, name, gruppe, typ, einheit, legende, quellen, hinweis (+ felder)."""
    for k in ('id', 'name', 'gruppe', 'typ', 'einheit', 'legende', 'quellen', 'hinweis'):
        assert k in kopf, k
    o = dict(kopf)
    o['daten'] = daten
    p = os.path.join(FERTIG, kopf['id'] + '.json')
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(o, f, ensure_ascii=False, separators=(',', ':'))
    print(f"{kopf['id']}: {os.path.getsize(p)/1024:.1f} KB")
    return p


def vereinfache(coords, tol):
    """Douglas-Peucker über shapely; coords = [[lon,lat],...]."""
    from shapely.geometry import LineString
    if len(coords) < 3:
        return [[r2(a), r2(b)] for a, b in coords]
    ls = LineString(coords).simplify(tol, preserve_topology=False)
    out = []
    for a, b in ls.coords:
        p = [r2(a), r2(b)]
        if not out or out[-1] != p:
            out.append(p)
    return out


_LAND = None


def laender():
    """Länderflächen der App (welt_basis.json, Natural Earth) als shapely-Objekte: [(iso3, name_de, geom)]."""
    global _LAND
    if _LAND is None:
        from shapely.geometry import Polygon, MultiPolygon
        from shapely.validation import make_valid
        d = json.load(open('/home/claude/quellwissen/werkzeug/welt_daten/welt_basis.json'))
        _LAND = []
        for c in d['laender']:
            ps = [Polygon(r) for r in c['p'] if len(r) >= 3]
            if ps:
                _LAND.append((c['i'], c['n'], make_valid(MultiPolygon(ps) if len(ps) > 1 else ps[0])))
    return _LAND


def land_von(lon, lat, max_grad=2.5):
    """ISO3 des Landes am Punkt; sonst nächstes Land innerhalb max_grad (dann see=True)."""
    from shapely.geometry import Point
    p = Point(lon, lat)
    best, bd = None, 1e9
    for i, n, g in laender():
        if g.contains(p):
            return i, False
        d = g.distance(p)
        if d < bd:
            best, bd = i, d
    return (best, True) if bd <= max_grad else (None, True)
