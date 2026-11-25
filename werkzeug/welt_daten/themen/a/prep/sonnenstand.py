"""Prüft die Formel für den Sonnen-Bildpunkt (NOAA „General Solar Position Calculations“) gegen astronomy-engine.
Aufruf: python3 -I prep/sonnenstand.py"""
import math, datetime as dt
import astronomy as A


def bildpunkt(d):
    """d: datetime UTC → (lon, lat) des Punkts, über dem die Sonne im Zenit steht."""
    n = d.timetuple().tm_yday
    tage = 366 if (d.year % 4 == 0 and (d.year % 100 != 0 or d.year % 400 == 0)) else 365
    h = d.hour + d.minute / 60 + d.second / 3600
    g = 2 * math.pi / tage * (n - 1 + (h - 12) / 24)
    eqt = 229.18 * (0.000075 + 0.001868 * math.cos(g) - 0.032077 * math.sin(g) - 0.014615 * math.cos(2 * g) - 0.040849 * math.sin(2 * g))
    dekl = (0.006918 - 0.399912 * math.cos(g) + 0.070257 * math.sin(g) - 0.006758 * math.cos(2 * g) + 0.000907 * math.sin(2 * g)
            - 0.002697 * math.cos(3 * g) + 0.00148 * math.sin(3 * g))
    lon = -15 * (h - 12 + eqt / 60)
    lon = ((lon + 180) % 360) - 180
    return lon, math.degrees(dekl)


def referenz(d):
    t = A.Time.Make(d.year, d.month, d.day, d.hour, d.minute, d.second)
    eq = A.Equator(A.Body.Sun, t, A.Observer(0, 0, 0), True, True)
    gast = A.SiderealTime(t)
    lon = ((eq.ra - gast) * 15 + 180) % 360 - 180
    return lon, eq.dec


mx_lon = mx_lat = 0
for i in range(0, 366 * 4, 7):
    d = dt.datetime(2026, 1, 1) + dt.timedelta(hours=6 * i + 1.3)
    a, b = bildpunkt(d), referenz(d)
    dl = abs(((a[0] - b[0]) + 180) % 360 - 180)
    mx_lon, mx_lat = max(mx_lon, dl), max(mx_lat, abs(a[1] - b[1]))
print(f'größte Abweichung über ein Jahr: Länge {mx_lon:.3f}°, Breite {mx_lat:.3f}°')
for d in [dt.datetime(2026, 6, 21, 12), dt.datetime(2026, 12, 21, 12), dt.datetime(2026, 11, 3, 12)]:
    print(d, 'Formel', [round(x, 2) for x in bildpunkt(d)], 'astronomy-engine', [round(x, 2) for x in referenz(d)])
