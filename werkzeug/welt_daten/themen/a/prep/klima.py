"""Klima-Raster 2° (gleiche Zellmitten wie DAT.raster der App): Jahresmitteltemperatur, Mittel des kältesten und wärmsten Monats
(NCEP/NCAR Reanalysis 1, Langzeitmittel 1981–2010, NOAA PSL; Kopie in GitHub bird-house/birdhouse-workshop) und Jahresniederschlag
(GPCP v2.2, Monatsmittel 1979–2010, NASA GSFC; Kopie in GitHub NCAR/geocat-datafiles). Aufruf: python3 -I prep/klima.py"""
import sys, os, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gemein import ROH, schreibe
import numpy as np, netCDF4 as N

D = os.path.join(ROH, 'klima')
a = N.Dataset(os.path.join(D, 'air.mon.ltm.nc'))
T = np.array(a['air'][:], dtype=float)            # (12,73,144) °C
tlat, tlon = np.array(a['lat'][:]), np.array(a['lon'][:])
g = N.Dataset(os.path.join(D, 'V22_GPCP.1979-2010.nc'))
P = np.ma.filled(g['PREC'][:], np.nan).astype(float)  # mm/Tag
P[P < 0] = np.nan
plat, plon = np.array(g['lat'][:]), np.array(g['lon'][:])
pd = np.nanmean(P, axis=0) * 365.25                 # mm/Jahr (Mittel aller Monate 1979–2010)
tj, tmin, tmax = T.mean(0), T.min(0), T.max(0)


def bilin(feld, lats, lons, la, lo):
    lo = lo % 360
    if lats[0] > lats[-1]:
        lats, feld = lats[::-1], feld[::-1]
    i = np.clip(np.searchsorted(lats, la) - 1, 0, len(lats) - 2)
    fy = (la - lats[i]) / (lats[i + 1] - lats[i])
    dl = lons[1] - lons[0]
    j = int(np.floor((lo - lons[0]) / dl)) % len(lons); j2 = (j + 1) % len(lons)
    fx = ((lo - lons[0]) / dl) - np.floor((lo - lons[0]) / dl)
    v = (feld[i, j] * (1 - fx) * (1 - fy) + feld[i, j2] * fx * (1 - fy) + feld[i + 1, j] * (1 - fx) * fy + feld[i + 1, j2] * fx * fy)
    return v


bt, bk, bw, bp = bytearray(), bytearray(), bytearray(), bytearray()
for la in range(89, -90, -2):
    for lo in range(-179, 180, 2):
        for arr, buf in ((tj, bt), (tmin, bk), (tmax, bw)):
            v = bilin(arr, tlat, tlon, la, lo)
            buf.append(255 if np.isnan(v) else int(np.clip(round(v) + 70, 0, 254)))
        v = bilin(pd, plat, plon, la, lo)
        bp.append(255 if np.isnan(v) else int(np.clip(round(v / 20), 0, 254)))
b64 = lambda b: base64.b64encode(bytes(b)).decode()
# Stichproben
def wert(la, lo):
    k = ((89 - la) // 2) * 180 + (lo + 179) // 2
    return bt[k] - 70, bk[k] - 70, bw[k] - 70, bp[k] * 20
for n, la, lo in [('Frankfurt', 51, 9), ('Sahara', 23, 5), ('Amazonas', -3, -61), ('Jakutsk', 61, 129), ('Mumbai', 19, 73)]:
    print(n, wert(la, lo))
schreibe({
    'id': 'klima_raster', 'name': 'Temperatur und Niederschlag', 'gruppe': 'Natur', 'typ': 'raster', 'einheit': '°C bzw. mm/Jahr',
    'raster': {'zellen': '2°', 'zeilen': 90, 'spalten': 180, 'start_lat': 89, 'start_lon': -179, 'schritt': 2,
               'reihenfolge': 'Zeile für Zeile von Nord (lat 89) nach Süd, je Zeile von West (lon -179) nach Ost; Index = ((89-lat)/2)*180 + (lon+179)/2',
               'kodierung': 'Base64, 1 Byte je Zelle; 255 = keine Angabe. Temperatur: Byte − 70 = °C (gerundet). Niederschlag: Byte × 20 = mm/Jahr (ab 5.080 gekappt).'},
    'ebenen': {'t_jahr': 'Jahresmitteltemperatur 1981–2010', 't_kalt': 'Mittel des kältesten Monats 1981–2010', 't_warm': 'Mittel des wärmsten Monats 1981–2010', 'niederschlag': 'Jahresniederschlag 1979–2010'},
    'legende': {'t_jahr': [[-30, '#3a4cc0'], [0, '#b8d0f0'], [10, '#f0e8b0'], [20, '#f5a050'], [30, '#c02020']], 'niederschlag': [[0, '#f0dca0'], [250, '#d8e090'], [750, '#70c070'], [1500, '#2a9a9a'], [3000, '#1a4aa0']]},
    'quellen': [
        {'t': 'NCEP/NCAR Reanalysis 1, Monthly Long Term Mean air.sig995 (1981–2010), NOAA PSL; Kopie in GitHub bird-house/birdhouse-workshop (data/air.mon.ltm.nc)', 'u': 'https://psl.noaa.gov/data/gridded/data.ncep.reanalysis.derived.html', 'stand': '1981–2010 (Datei 2014)', 'lizenz': 'NOAA PSL, frei ohne Einschränkung (US-Regierungswerk); Nennung: NCEP Reanalysis data provided by the NOAA PSL, Boulder, Colorado, USA'},
        {'t': 'GPCP Version 2.2 Combined Precipitation (Huffman et al. 2009, doi:10.1029/2009GL040000), NASA GSFC; Kopie in GitHub NCAR/geocat-datafiles (netcdf_files/V22_GPCP.1979-2010.nc)', 'u': 'https://github.com/NCAR/geocat-datafiles', 'stand': '1979–2010', 'lizenz': 'gemeinfrei (NASA); Zitierung erbeten'}],
    'hinweis': 'Grobes Modell-/Satellitenraster (2,5°, auf 2° umgerechnet): gut für Großräume, nicht für einzelne Orte; Gebirge erscheinen zu warm/zu glatt (Temperatur auf ca. 40 m über Modellgelände). Über Meer: Lufttemperatur über dem Meer.'
}, {'t_jahr': b64(bt), 't_kalt': b64(bk), 't_warm': b64(bw), 'niederschlag': b64(bp)})
