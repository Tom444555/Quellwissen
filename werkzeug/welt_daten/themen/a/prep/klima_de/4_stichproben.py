"""Schritt 4: Stichproben gegen DWD-Stationsnormalwerte 1991-2020 (multi_annual/mean_91-20).
Vergleicht: DWD-Stationsnormalwert | Rasterzelle am Stationsort | Kreismittel.
Aufruf: python3 -I 4_stichproben.py <roh> <kreise_klima.json> <stationen_tnabs.json>
"""
import sys, json
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import numpy as np
from raster import lies_asc, wgs_nach_gk3

roh, kk, sf = sys.argv[1:4]
proben = [(4336, "10041", "Saarbrücken-Ensheim / Regionalverband Saarbrücken"),
          (1443, "08311", "Freiburg / Freiburg im Breisgau"),
          (1975, "02000", "Hamburg-Fuhlsbüttel / Hamburg"),
          (3730, "09780", "Oberstdorf / Oberallgäu"),
          (1550, "09180", "Garmisch-Partenkirchen / LK Garmisch-Partenkirchen")]

def normal(datei):
    d = {}
    for z in open(f"{roh}/{datei}", encoding="utf-8").read().splitlines()[1:]:
        t = [x.strip() for x in z.split(";")]
        if len(t) > 15 and t[0].isdigit():
            d[int(t[0])] = [float(x) if x not in ("", "-999") else None for x in t[3:16]]
    return d

sn, fn = normal("n_Sonnenscheindauer_1991-2020.txt"), normal("n_Frosttage_1991-2020.txt")
sonne, kopf = lies_asc(f"{roh}/grids_germany_multi_annual_sunshine_duration_1991-2020_17.asc.gz")
frost, _ = lies_asc(f"{roh}/grids_germany_multi_annual_frost_days_1991-2020_17.asc.gz")
kd = json.load(open(kk))["daten"]
st = {s["id"]: s for s in json.load(open(sf))}
meta = {}
for z in open(f"{roh}/stationen.txt", encoding="utf-8").read().splitlines()[2:]:
    t = z.split()
    if len(t) > 6: meta[int(t[0])] = (float(t[4]), float(t[5]), float(t[3]))

print("| Station / Kreis | Sonne DWD-Station | Sonne Rasterzelle | Sonne Kreis | Frosttage Station | Frost Zelle | Frost Kreis | TNabs Station (Zone) | Kreis TNabs (Zone, Spanne) |")
print("|---|---|---|---|---|---|---|---|---|")
for sid, ags, txt in proben:
    lat, lon, h = meta[sid]
    x, y = wgs_nach_gk3(lon, lat)
    c = int((x - kopf["XLLCORNER"]) // kopf["CELLSIZE"]); r = int(kopf["NROWS"]) - 1 - int((y - kopf["YLLCORNER"]) // kopf["CELLSIZE"])
    k = kd[ags]; s = st.get(sid)
    def zone(tc):
        import math
        f = tc * 9 / 5 + 32; i = math.floor((f + 60) / 5); return f"{i // 2 + 1}{'ab'[i % 2]}"
    tn = f"{s['tnabs']:.1f} ({zone(s['tnabs'])}, n={s['n']})" if s else "–"
    print(f"| {txt} ({h:.0f} m) | {sn[sid][12]:.0f} | {sonne[r, c]:.0f} | {k['sonne_h']} | {(f'{fn[sid][12]:.0f}' if sid in fn else '–')} | {frost[r, c]:.0f} | {k['frosttage']} | {tn} | {k['tmin_abs_c']} ({k['zone']}, {k['zone_kalt']}–{k['zone_mild']}) |")
