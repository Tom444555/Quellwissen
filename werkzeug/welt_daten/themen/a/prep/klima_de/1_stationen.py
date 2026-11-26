"""Schritt 1: DWD-Jahreswerte (annual/kl/historical) auswerten.
Je Station: Mittel des absoluten Jahresminimums JA_MX_TN 1991-2020,
nur Stationen mit >= 20 gueltigen Jahren. Ausgabe: stationen_tnabs.json
Aufruf: python3 -I 1_stationen.py <roh-Verzeichnis> <ausgabe.json>
"""
import sys, os, zipfile, io, json, glob

roh, aus = sys.argv[1], sys.argv[2]

# Stationsliste (fest formatiert, Spalten per Leerzeichen; Name kann Leerzeichen enthalten)
meta = {}
with open(os.path.join(roh, "stationen.txt"), encoding="utf-8") as f:
    for z in f.readlines()[2:]:
        t = z.split()
        if len(t) < 7:
            continue
        sid = int(t[0])
        # Name = alles zwischen Laenge und Bundesland; Bundesland/Abgabe am Ende
        # Bundesland kann zweiteilig sein (z. B. "Nordrhein-Westfalen" einteilig, aber "Mecklenburg-Vorpommern" ok)
        rest = t[6:]
        abgabe = rest[-1]
        land = rest[-2]
        name = " ".join(rest[:-2])
        meta[sid] = dict(h=float(t[3]), lat=float(t[4]), lon=float(t[5]), name=name, land=land)

ergeb = {}
for zp in sorted(glob.glob(os.path.join(roh, "jahr", "*.zip"))):
    with zipfile.ZipFile(zp) as z:
        pn = [n for n in z.namelist() if n.startswith("produkt_")][0]
        txt = z.read(pn).decode("latin1").splitlines()
    kopf = [k.strip() for k in txt[0].split(";")]
    i_j, i_tn, i_q = kopf.index("MESS_DATUM_BEGINN"), kopf.index("JA_MX_TN"), kopf.index("QN_6")
    werte = {}
    sid = None
    for z in txt[1:]:
        t = [x.strip() for x in z.split(";")]
        if len(t) < len(kopf) - 1:
            continue
        sid = int(t[0])
        jahr = int(t[i_j][:4])
        if not (1991 <= jahr <= 2020):
            continue
        v = float(t[i_tn])
        if v == -999 or v < -60 or v > 15:
            continue
        werte[jahr] = v
    if sid is None or len(werte) < 20 or sid not in meta:
        continue
    m = meta[sid]
    ergeb[sid] = dict(id=sid, name=m["name"], land=m["land"], h=m["h"], lat=m["lat"], lon=m["lon"],
                      n=len(werte), tnabs=round(sum(werte.values()) / len(werte), 2))

json.dump(list(ergeb.values()), open(aus, "w"), ensure_ascii=False, indent=0)
print(len(ergeb), "Stationen mit >= 20 Jahren")
