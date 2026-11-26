"""Schritt 3: Kreiswerte erzeugen -> kreise_klima.json und pruef_stationen.csv
- Sonnenscheindauer 1991-2020 (DWD-Raster, h): Jahr (_17) + Monate (_01.._12)
- Frosttage 1991-2020 (DWD-Raster, Tage/Jahr)
- Mittleres absolutes Jahresminimum 1991-2020 + USDA-Winterhaertezone:
  Stationswerte (Schritt 1) -> Regression auf DWD-Raster Januar-Tmin 1991-2020
  + inverse Distanzgewichtung (8 naechste Stationen, Potenz 2) der Residuen, je 1-km-Zelle;
  Kreiswert = Mittel der Zellen.
Aufruf: python3 -I 3_kreise_klima.py <roh> <kreise.json> <stationen_tnabs.json> <ausgabe-Verzeichnis>
"""
import sys, json, math, csv
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import numpy as np
from raster import lies_asc, zell_mitten, gk3_nach_wgs, wgs_nach_gk3, lies_kreise, kreis_zellen

roh, kf, sf, aus = sys.argv[1:5]
K_IDW, P_IDW = 8, 2
S = "grids_germany_multi_annual_sunshine_duration_1991-2020_%02d.asc.gz"

jahr, kopf = lies_asc(f"{roh}/{S % 17}")
monate = [lies_asc(f"{roh}/{S % m}")[0] for m in range(1, 13)]
frost, kf2 = lies_asc(f"{roh}/grids_germany_multi_annual_frost_days_1991-2020_17.asc.gz")
tjan, kf3 = lies_asc(f"{roh}/grids_germany_multi_annual_air_temp_min_1991-2020_01.asc.gz")
tjan = tjan / 10.0  # 1/10 degC laut Beschreibung
for kk in (kf2, kf3):
    assert all(abs(kk[a] - kopf[a]) < 1e-6 for a in ("NCOLS", "NROWS", "XLLCORNER", "YLLCORNER", "CELLSIZE"))

X, Y = zell_mitten(kopf)
LON, LAT = gk3_nach_wgs(X, Y)
gueltig = ~np.isnan(jahr) & ~np.isnan(frost) & ~np.isnan(tjan)
kreise = lies_kreise(kf)
zellen = kreis_zellen(kreise, LON, LAT, gueltig)

# --- Stationen, Regression
st = json.load(open(sf))
sx, sy = wgs_nach_gk3(np.array([s["lon"] for s in st]), np.array([s["lat"] for s in st]))
col = ((sx - kopf["XLLCORNER"]) // kopf["CELLSIZE"]).astype(int)
row = (int(kopf["NROWS"]) - 1 - (sy - kopf["YLLCORNER"]) // kopf["CELLSIZE"]).astype(int)
inn = (col >= 0) & (col < tjan.shape[1]) & (row >= 0) & (row < tjan.shape[0])
g = np.full(len(st), np.nan); g[inn] = tjan[row[inn], col[inn]]
ok = ~np.isnan(g)
st = [s for s, o in zip(st, ok) if o]; sx, sy, g = sx[ok], sy[ok], g[ok]
v = np.array([s["tnabs"] for s in st])
A = np.column_stack([np.ones(len(v)), g]); c, *_ = np.linalg.lstsq(A, v, rcond=None)
res = v - A @ c

def idw_res(px, py):
    d = np.hypot(sx[None, :] - px[:, None], sy[None, :] - py[:, None])
    n = np.argsort(d, axis=1)[:, :K_IDW]
    dn = np.take_along_axis(d, n, 1)
    w = 1 / np.maximum(dn, 1000) ** P_IDW
    return (w * res[n]).sum(1) / w.sum(1), n

def zone(tc):
    f = tc * 9 / 5 + 32
    i = math.floor((f + 60) / 5)
    return f"{i // 2 + 1}{'ab'[i % 2]}"

def zgrenzen():
    out = []
    for i in range(4, 20):  # 3a .. 10b
        lo = -60 + 5 * i
        out.append([f"{i // 2 + 1}{'ab'[i % 2]}", round((lo - 32) * 5 / 9, 1), round((lo + 5 - 32) * 5 / 9, 1)])
    return out

daten, pruef = {}, []
Xf, Yf = X.ravel(), Y.ravel()
for k in kreise:
    idx, notfall = zellen[k["ags"]]
    r, nb = idw_res(Xf[idx], Yf[idx])
    tz = c[0] + c[1] * tjan.ravel()[idx] + r
    tm = float(tz.mean())
    genutzt = sorted(set(nb.ravel().tolist()))
    # naechste Stationen zum Kreismittelpunkt (fuer die Pruefdatei)
    mx, my = wgs_nach_gk3(k["lon"], k["lat"])
    dm = np.hypot(sx - mx, sy - my); nn = np.argsort(dm)[:K_IDW]
    daten[k["ags"]] = {
        "sonne_h": int(round(float(np.nanmean(jahr.ravel()[idx])))),
        "sonne_mon_h": [int(round(float(np.nanmean(m.ravel()[idx])))) for m in monate],
        "frosttage": int(round(float(np.nanmean(frost.ravel()[idx])))),
        "tmin_abs_c": round(tm, 1),
        "zone": zone(tm),  # aus dem ungerundeten Kreismittel (Korrektur 26.11.2026 nachmittags)
        "zone_kalt": zone(float(tz.min())),
        "zone_mild": zone(float(tz.max())),
        "zellen": int(len(idx)),
    }
    pruef.append([k["ags"], k["name"], len(idx), "ja" if notfall else "", round(tm, 1), zone(round(tm, 1)),
                  round(float(tz.min()), 1), round(float(tz.max()), 1), len(genutzt),
                  " | ".join(f"{st[j]['name']} ({st[j]['id']}, {dm[j]/1000:.0f} km, {st[j]['tnabs']:.1f})" for j in nn)])

felder = [
    ["sonne_h", "Sonnenscheindauer Jahr 1991–2020 (Mittel, h)"],
    ["sonne_mon_h", "Sonnenscheindauer je Monat Jan–Dez 1991–2020 (h), 12 Werte"],
    ["frosttage", "Frosttage je Jahr 1991–2020 (Tmin < 0 °C, Mittel)"],
    ["tmin_abs_c", "Mittleres absolutes Jahresminimum der Lufttemperatur 1991–2020 (°C), Kreismittel"],
    ["zone", "USDA-Winterhärtezone aus tmin_abs_c (Kreismittel)"],
    ["zone_kalt", "Zone der kältesten 1-km-Zelle im Kreis"],
    ["zone_mild", "Zone der mildesten 1-km-Zelle im Kreis"],
    ["zellen", "Zahl der 1-km-Rasterzellen im Kreis (1 = nächste Zelle, Kreis zu klein)"],
]
heute = "26.11.2026"
lz = "CC BY 4.0 (DWD-Nutzungsbedingungen, Stand Mai 2024); Quellenvermerk: „Datenbasis: Deutscher Wetterdienst, Einzelwerte gemittelt“"
out = {
    "felder": [{"id": a, "t": b} for a, b in felder],
    "zonen_grenzen_c": zgrenzen(),
    "daten": daten,
    "quellen": [
        {"t": "DWD Climate Data Center (CDC), Vieljähriges Mittel der Raster der Sonnenscheindauer für Deutschland 1991–2020, Version v1.0 (Monate _01–_12, Jahr _17)",
         "u": "https://opendata.dwd.de/climate_environment/CDC/grids_germany/multi_annual/sunshine_duration/", "stand": heute, "lizenz": lz},
        {"t": "DWD Climate Data Center (CDC), Vieljähriges Mittel der Raster der Anzahl der Frosttage für Deutschland 1991–2020, Version v1.0",
         "u": "https://opendata.dwd.de/climate_environment/CDC/grids_germany/multi_annual/frost_days/", "stand": heute, "lizenz": lz},
        {"t": "DWD Climate Data Center (CDC), Jahreswerte Stationsmessungen Klima (KL), historical: JA_MX_TN (absolutes Jahresminimum) 1991–2020",
         "u": "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/annual/kl/historical/", "stand": heute, "lizenz": lz},
        {"t": "DWD Climate Data Center (CDC), Vieljährige mittlere Raster der monatlich gemittelten Lufttemperaturminima (2 m) für Deutschland 1991–2020, Version v1.0 (Januar, als Hilfsgröße)",
         "u": "https://opendata.dwd.de/climate_environment/CDC/grids_germany/multi_annual/air_temperature_min/", "stand": heute, "lizenz": lz},
        {"t": "USDA Plant Hardiness Zone Map (Zonendefinition: 10 °F je Zone, a/b je 5 °F)",
         "u": "https://planthardiness.ars.usda.gov/", "stand": heute, "lizenz": "nur Definition übernommen"},
    ],
    "hinweis": (
        "Kreiswert = Mittel aller 1-km-Rasterzellen (DWD, Gauß-Krüger Zone 3), deren Mittelpunkt im Kreis liegt; "
        "sehr kleine Kreise ohne Zelle: nächste Zelle. Winterhärtezone: mittleres absolutes Jahresminimum aus "
        f"{len(st)} DWD-Stationen mit ≥ 20 gültigen Jahren 1991–2020, übertragen über eine Regression auf das "
        f"DWD-Raster Januar-Tmin (TNabs = {c[0]:.2f} + {c[1]:.2f}·Tmin_Jan) plus inverse Distanzgewichtung der "
        f"Stations-Abweichungen ({K_IDW} nächste Stationen, Potenz 2); Höhe und Lage gehen so über das DWD-Raster ein. "
        "Eine feste Höhenkorrektur (−0,5 K/100 m) wurde geprüft und verworfen (in der Kreuzvalidierung schlechter). "
        "Kreismittel – in Tal- und Muldenlagen (Kaltluft) und in Hochlagen kann es lokal eine halbe bis ganze Zone kälter sein "
        "(siehe zone_kalt). Zone nach USDA-Grenzen in °F, exakt in °C umgerechnet (z. B. 7b: −15,0 bis −12,2 °C; 8a: −12,2 bis −9,4 °C). "
        "Datenbasis: Deutscher Wetterdienst, Einzelwerte gemittelt (CC BY 4.0)."
    ),
}
json.dump(out, open(f"{aus}/kreise_klima.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
with open(f"{aus}/pruef_stationen.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["ags", "name", "zellen", "notfall_naechste_zelle", "tmin_abs_c", "zone", "kaelteste_zelle_c",
                "mildeste_zelle_c", "anzahl_stationen_genutzt", "8_naechste_stationen_zum_mittelpunkt (id, km, TNabs)"])
    w.writerows(pruef)
print("Regression", c, "Stationen", len(st), "Kreise", len(daten), "Notfall", sum(1 for p in pruef if p[3]))
