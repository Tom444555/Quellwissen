"""Hilfsfunktionen: DWD-ASCII-Raster lesen, Zellmittelpunkte nach WGS84, Kreismasken."""
import gzip, json
import numpy as np
from pyproj import Transformer
from matplotlib.path import Path

def lies_asc(pfad):
    kopf = {}
    with gzip.open(pfad, "rt") as f:
        for _ in range(6):
            k, v = f.readline().split()
            kopf[k.upper()] = float(v)
        a = np.loadtxt(f)
    nd = kopf["NODATA_VALUE"]
    a = np.where(a == nd, np.nan, a)
    assert a.shape == (int(kopf["NROWS"]), int(kopf["NCOLS"]))
    return a, kopf

def zell_mitten(kopf):
    """Rechts-/Hochwert der Zellmittelpunkte (Zeile 0 = Norden). Ecke = XLLCORNER/YLLCORNER."""
    nr, nc, cs = int(kopf["NROWS"]), int(kopf["NCOLS"]), kopf["CELLSIZE"]
    if "XLLCORNER" in kopf:
        x0, y0 = kopf["XLLCORNER"] + cs / 2, kopf["YLLCORNER"] + cs / 2
    else:
        x0, y0 = kopf["XLLCENTER"], kopf["YLLCENTER"]
    xs = x0 + cs * np.arange(nc)
    ys = y0 + cs * (nr - 1 - np.arange(nr))
    return np.meshgrid(xs, ys)

_tr = Transformer.from_crs("EPSG:31467", "EPSG:4326", always_xy=True)
_tr_inv = Transformer.from_crs("EPSG:4326", "EPSG:31467", always_xy=True)

def gk3_nach_wgs(x, y):
    return _tr.transform(x, y)

def wgs_nach_gk3(lon, lat):
    return _tr_inv.transform(lon, lat)

def lies_kreise(pfad):
    d = json.load(open(pfad, encoding="utf-8"))
    f = d["felder"]
    kreise = []
    for z in d["daten"]:
        r = dict(zip(f, z))
        ringe = []
        for ring in r["ringe"]:
            x, y = ring[0], ring[1]
            pts = [(x, y)]
            for i in range(2, len(ring), 2):
                x += ring[i]; y += ring[i + 1]
                pts.append((x, y))
            ringe.append(np.array(pts, float) / 100.0)
        r["ringe_dec"] = ringe
        kreise.append(r)
    return kreise

def kreis_zellen(kreise, lon, lat, gueltig):
    """Je AGS: Indizes (flach) der gueltigen Zellen, deren Mittelpunkt im Kreis liegt.
    Ohne Treffer: naechste gueltige Zelle zum Kreis-Mittelpunkt (lon/lat aus kreise.json)."""
    lonf, latf = lon.ravel(), lat.ravel()
    ok = np.flatnonzero(gueltig.ravel())
    pts = np.column_stack([lonf[ok], latf[ok]])
    erg = {}
    for k in kreise:
        idx = []
        for ring in k["ringe_dec"]:
            mn, mx = ring.min(0), ring.max(0)
            sel = np.flatnonzero((pts[:, 0] >= mn[0]) & (pts[:, 0] <= mx[0]) & (pts[:, 1] >= mn[1]) & (pts[:, 1] <= mx[1]))
            if len(sel):
                drin = Path(ring).contains_points(pts[sel])
                idx.extend(ok[sel[drin]].tolist())
        erg[k["ags"]] = set(idx)
    # Ringe sind ohne Loecher: eingeschlossene Kreise (z. B. kreisfreie Stadt im Landkreis)
    # liegen auch im aeusseren Ring. Zelle -> Kreis mit kleinster Flaeche.
    besitzer = {}
    fl = {k["ags"]: k["flaeche_km2"] for k in kreise}
    for a, s in erg.items():
        for i in s:
            if i not in besitzer or fl[a] < fl[besitzer[i]]:
                besitzer[i] = a
    neu = {}
    for k in kreise:
        idx = sorted(i for i in erg[k["ags"]] if besitzer[i] == k["ags"])
        notfall = False
        if not idx:
            d2 = ((pts[:, 0] - k["lon"]) * np.cos(np.radians(k["lat"]))) ** 2 + (pts[:, 1] - k["lat"]) ** 2
            idx = [int(ok[np.argmin(d2)])]
            notfall = True
        neu[k["ags"]] = (np.array(idx), notfall)
    return neu
