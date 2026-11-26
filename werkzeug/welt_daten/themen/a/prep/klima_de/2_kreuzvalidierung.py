"""Schritt 2: Leave-one-out-Pruefung der Uebertragungsverfahren fuer das absolute Jahresminimum.
A  reine IDW (k naechste Stationen, Potenz 2)
B  IDW + feste Hoehenkorrektur -0,5 K/100 m (nur Station->Station pruefbar)
C  Regression auf DWD-Raster Januar-Tmin 1991-2020 (Zelle der Station) + IDW der Residuen
Aufruf: python3 -I 2_kreuzvalidierung.py <roh> <stationen_tnabs.json>
"""
import sys, json
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import numpy as np
from raster import lies_asc, wgs_nach_gk3

roh, sf = sys.argv[1], sys.argv[2]
st = json.load(open(sf))
tmin, kopf = lies_asc(f"{roh}/grids_germany_multi_annual_air_temp_min_1991-2020_01.asc.gz")
tmin = tmin / 10.0
x, y = wgs_nach_gk3(np.array([s["lon"] for s in st]), np.array([s["lat"] for s in st]))
col = ((x - kopf["XLLCORNER"]) // kopf["CELLSIZE"]).astype(int)
row = (int(kopf["NROWS"]) - 1 - (y - kopf["YLLCORNER"]) // kopf["CELLSIZE"]).astype(int)
g = tmin[row, col]
v = np.array([s["tnabs"] for s in st]); h = np.array([s["h"] for s in st])
ok = ~np.isnan(g)
print("Stationen mit Rasterwert:", ok.sum(), "von", len(st))

def idw(i, werte, k=6, p=2, maske=None):
    d = np.hypot(x - x[i], y - y[i]); d[i] = np.inf
    if maske is not None: d[~maske] = np.inf
    n = np.argsort(d)[:k]
    w = 1 / np.maximum(d[n], 1000) ** p
    return n, (w * werte[n]).sum() / w.sum()

for k in (4, 6, 8):
    eA, eB, eC = [], [], []
    for i in np.flatnonzero(ok):
        n, a = idw(i, v, k, maske=ok); eA.append(a - v[i])
        n, b = idw(i, v + 0.005 * h, k, maske=ok); eB.append(b - 0.005 * h[i] - v[i])
        m = ok.copy(); m[i] = False
        A = np.column_stack([np.ones(m.sum()), g[m]]); c, *_ = np.linalg.lstsq(A, v[m], rcond=None)
        res = v - (c[0] + c[1] * g)
        n, r = idw(i, res, k, maske=m); eC.append(c[0] + c[1] * g[i] + r - v[i])
    f = lambda e: f"MAE {np.mean(np.abs(e)):.2f} K, RMSE {np.sqrt(np.mean(np.square(e))):.2f} K, |F|>2,8K: {np.mean(np.abs(e)>2.8)*100:.0f} %"
    print(f"k={k}  A reine IDW: {f(eA)}\n      B IDW+0,5K/100m: {f(eB)}\n      C Raster-Regression+IDW-Residuen: {f(eC)}")

A = np.column_stack([np.ones(ok.sum()), g[ok]]); c, *_ = np.linalg.lstsq(A, v[ok], rcond=None)
r = v[ok] - A @ c
print(f"Regression: TNabs = {c[0]:.2f} + {c[1]:.2f} * Tmin_Jan ; R^2 = {1 - r.var() / v[ok].var():.2f}")
A2 = np.column_stack([np.ones(ok.sum()), h[ok]]); c2, *_ = np.linalg.lstsq(A2, v[ok], rcond=None)
print(f"Nur Hoehe: Gradient {c2[1]*100:.2f} K/100 m")
