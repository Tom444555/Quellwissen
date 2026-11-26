"""Punkt-in-Fläche mit matplotlib.path über die App-Länder (welt_basis.json, Natural Earth) und Bundesländer (bl)."""
import json
from matplotlib.path import Path
_B = json.load(open('/home/claude/quellwissen/werkzeug/welt_daten/welt_basis.json'))

def _bau(liste):
    out = []
    for c in liste:
        ps = [Path(r) for r in c['p'] if len(r) >= 3]
        out.append((c['i'], c['n'], ps))
    return out
LAENDER = _bau(_B['laender'])
def _fl(e):
    return sum((p.get_extents().width * p.get_extents().height) for p in e[2])
# kleinere Flächen zuerst (Löcher wie Berlin in Brandenburg, Enklaven wie Lesotho/Vatikan sind nicht ausgespart)
BL = sorted(_bau(_B['bl']), key=_fl)
LAENDER = sorted(LAENDER, key=_fl)

def _dist(ps, x, y):
    import math
    best = 1e9
    for p in ps:
        for vx, vy in p.vertices[::max(1, len(p.vertices)//400)]:
            d = math.hypot(vx - x, vy - y)
            if d < best: best = d
    return best

def finde(liste, lon, lat, max_grad=0.5):
    """Code der Fläche am Punkt; sonst nächste innerhalb max_grad (Abstand grob über Stützpunkte). -> (code, innen)"""
    for i, n, ps in liste:
        if any(p.contains_point((lon, lat)) for p in ps):
            return i, True
    best, bd = None, 1e9
    for i, n, ps in liste:
        d = _dist(ps, lon, lat)
        if d < bd: best, bd = i, d
    return (best, False) if bd <= max_grad else (None, False)

def land(lon, lat, m=0.5): return finde(LAENDER, lon, lat, m)
def bundesland(lon, lat, m=0.2): return finde(BL, lon, lat, m)
