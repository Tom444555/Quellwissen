"""Schritt 5: Globalstrahlung 1991-2020 (DWD-Raster radiation_global, kWh/m2) je Kreis
in kreise_klima.json ergaenzen (strahl_kwh, strahl_m) + Stichprobe gegen DWD-Stationsmessungen
(daily/solar, FG_STRAHL in J/cm2; 1 J/cm2 = 1/360 kWh/m2).
Achtung: Das Strahlungsraster hat einen eigenen Kopf ([header] + ESRI-ASCII) und eine
andere Ecke (XLLCORNER 3280500) als die uebrigen DWD-Raster -> eigene Kreismasken.
Aufruf: python3 -I 5_strahlung.py <roh/strahl> <kreise.json> <kreise_klima.json>
"""
import sys, json, zipfile, io
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import numpy as np
from raster import zell_mitten, gk3_nach_wgs, wgs_nach_gk3, lies_kreise, kreis_zellen

roh, kf, kk = sys.argv[1:4]

def lies_zip(pfad):
    with zipfile.ZipFile(pfad) as z:
        n = [x for x in z.namelist() if x.endswith(".asc")][0]
        zeilen = z.read(n).decode("latin1").splitlines()
    i = next(j for j, l in enumerate(zeilen) if l.strip().upper().startswith("NCOLS"))
    kopf = {}
    for l in zeilen[i:i + 6]:
        a, b = l.split(); kopf[a.upper()] = float(b)
    a = np.loadtxt(io.StringIO("\n".join(zeilen[i + 6:])))
    assert a.shape == (int(kopf["NROWS"]), int(kopf["NCOLS"]))
    return np.where(a == kopf["NODATA_VALUE"], np.nan, a), kopf

jahr, kopf = lies_zip(f"{roh}/grids_germany_multi_annual_radiation_global_1991_2020.zip")
mon = []
for m in range(1, 13):
    a, k2 = lies_zip(f"{roh}/grids_germany_multi_monthly_radiation_global_1991_2020_{m:02d}.zip")
    assert all(k2[x] == kopf[x] for x in ("XLLCORNER", "YLLCORNER", "CELLSIZE", "NCOLS", "NROWS"))
    mon.append(a)
X, Y = zell_mitten(kopf)
LON, LAT = gk3_nach_wgs(X, Y)
kreise = lies_kreise(kf)
zellen = kreis_zellen(kreise, LON, LAT, ~np.isnan(jahr))

d = json.load(open(kk, encoding="utf-8"))
for k in kreise:
    idx, _ = zellen[k["ags"]]
    e = d["daten"][k["ags"]]
    e["strahl_kwh"] = int(round(float(np.nanmean(jahr.ravel()[idx]))))
    e["strahl_m"] = [round(float(np.nanmean(a.ravel()[idx])), 1) for a in mon]
ids = [f["id"] for f in d["felder"]]
for fid, t in (("strahl_kwh", "Globalstrahlung Jahressumme 1991–2020 auf die horizontale Ebene (kWh/m², Mittel)"),
               ("strahl_m", "Globalstrahlung je Monat Jan–Dez 1991–2020 (kWh/m²), 12 Werte")):
    if fid not in ids:
        d["felder"].append({"id": fid, "t": t})
q = {"t": "DWD Climate Data Center (CDC): Rasterdaten der vieljährigen mittleren Monatssummen und der vieljährigen mittleren Jahressumme für die Globalstrahlung auf die horizontale Ebene für Deutschland basierend auf Boden- und Satellitenmessungen, Version V003 (1991–2020)",
     "u": "https://opendata.dwd.de/climate_environment/CDC/grids_germany/multi_annual/radiation_global/",
     "stand": "26.11.2026",
     "lizenz": "CC BY 4.0 (DWD-Nutzungsbedingungen, Stand Mai 2024); Quellenvermerk: „Datenbasis: Deutscher Wetterdienst, Einzelwerte gemittelt“"}
if not any(x["u"] == q["u"] for x in d["quellen"]):
    d["quellen"].insert(1, q)
zus = (" Globalstrahlung (strahl_kwh, strahl_m): DWD-Raster 1991–2020 (V003, aus Boden- und Satellitenmessungen) auf die "
       "horizontale Ebene, gleiches Kreis-Mittelungsverfahren; DWD-Unsicherheit ca. ±6 % (Jahr), ±5 % (Sommer) bis ±15 % (Winter). "
       "Für geneigte, nach Süden ausgerichtete PV-Module liegt die Einstrahlung je nach Neigung etwa 10–15 % höher.")
if "Globalstrahlung" not in d["hinweis"]:
    d["hinweis"] = d["hinweis"].replace(" Datenbasis: Deutscher Wetterdienst", zus + " Datenbasis: Deutscher Wetterdienst")
json.dump(d, open(kk, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))

# --- Stichprobe gegen Stationsmessung (Tageswerte FG_STRAHL), Jahre mit >= 95 % gueltigen Tagen
meta = {4336: (49.2128, 7.1077, "10041", "Saarbrücken-Ensheim / Regionalverband Saarbrücken"),
        1443: (48.0232, 7.8343, "08311", "Freiburg / Freiburg im Breisgau"),
        1975: (53.6332, 9.9881, "02000", "Hamburg-Fuhlsbüttel / Hamburg")}
print("| Station / Kreis | Station gemessen (kWh/m², Jahre) | Rasterzelle | Kreis | Abw. Zelle |")
print("|---|---|---|---|---|")
for sid, (lat, lon, ags, txt) in meta.items():
    with zipfile.ZipFile(f"{roh}/tageswerte_ST_{sid:05d}_row.zip") as z:
        n = [x for x in z.namelist() if x.startswith("produkt")][0]
        zl = z.read(n).decode("latin1").splitlines()
    kp = [x.strip() for x in zl[0].split(";")]; iv = kp.index("FG_STRAHL")
    jsum, jn = {}, {}
    for l in zl[1:]:
        t = [x.strip() for x in l.split(";")]
        y = int(t[1][:4])
        if 1991 <= y <= 2020 and float(t[iv]) >= 0:
            jsum[y] = jsum.get(y, 0) + float(t[iv]) / 360.0; jn[y] = jn.get(y, 0) + 1
    gut = [y for y in jsum if jn[y] >= 347]
    st = np.mean([jsum[y] for y in gut]) if gut else float("nan")
    x, y = wgs_nach_gk3(lon, lat)
    c = int((x - kopf["XLLCORNER"]) // 1000); r = int(kopf["NROWS"]) - 1 - int((y - kopf["YLLCORNER"]) // 1000)
    print(f"| {txt} | {st:.0f} ({len(gut)} J.) | {jahr[r, c]:.0f} | {d['daten'][ags]['strahl_kwh']} | {(jahr[r, c] / st - 1) * 100:+.1f} % |")
w = np.array([v["strahl_kwh"] for v in d["daten"].values()])
s = max(abs(sum(v["strahl_m"]) - v["strahl_kwh"]) for v in d["daten"].values())
print("Kreise", len(w), "min", w.min(), "max", w.max(), "max |Summe Monate - Jahr|", round(s, 1))
