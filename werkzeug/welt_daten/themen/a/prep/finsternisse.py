"""Totale und ringförmige Sonnenfinsternisse 2026–2040: Zeitpunkt/Ort des Maximums und Mittellinie, selbst gerechnet mit
astronomy-engine (pip, Don Cross, MIT). Mittellinie = Schnittpunkt der Schattenachse (Sonne→Mond) mit dem WGS84-Ellipsoid, minütlich.
Aufruf: python3 -I prep/finsternisse.py"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gemein import schreibe, r2
import astronomy as A

KM = A.KM_PER_AU
EA, EB = 6378.137 / KM, 6356.752 / KM


def achse_schnitt(t):
    """Schnittpunkt der Schattenachse mit der Erde (EQD-Rahmen, AU) oder None."""
    rot = A.Rotation_EQJ_EQD(t)
    m = A.RotateVector(rot, A.GeoMoon(t))
    s = A.RotateVector(rot, A.GeoVector(A.Body.Sun, t, True))
    d = [m.x - s.x, m.y - s.y, m.z - s.z]
    n = math.sqrt(sum(c * c for c in d)); d = [c / n for c in d]
    # Ellipsoid: z skalieren
    k = EA / EB
    p0 = [m.x, m.y, m.z * k]; dd = [d[0], d[1], d[2] * k]
    a = sum(c * c for c in dd); b = 2 * sum(x * y for x, y in zip(p0, dd)); c = sum(x * x for x in p0) - EA * EA
    disc = b * b - 4 * a * c
    if disc < 0:
        return None
    u = (-b - math.sqrt(disc)) / (2 * a)
    return A.Vector(m.x + u * d[0], m.y + u * d[1], m.z + u * d[2], t)


def ort(t):
    v = achse_schnitt(t)
    if v is None:
        return None
    o = A.VectorObserver(v, True)
    lon = ((o.longitude + 180) % 360) - 180
    return lon, o.latitude


ART = {A.EclipseKind.Total: 'total', A.EclipseKind.Annular: 'ringförmig'}
raus = []
e = A.SearchGlobalSolarEclipse(A.Time.Make(2026, 1, 1, 0, 0, 0))
while e.peak.Utc().year <= 2040:
    if e.kind in ART:
        # Mittellinie
        pts, t0 = [], e.peak.AddDays(-4 / 24)
        for i in range(0, 8 * 60 + 1):
            t = t0.AddDays(i / 1440)
            p = ort(t)
            if p:
                pts.append([r2(p[0]), r2(p[1])])
        # an der Datumsgrenze teilen
        teile, cur = [], []
        for p in pts:
            if cur and abs(p[0] - cur[-1][0]) > 180:
                teile.append(cur); cur = []
            cur.append(p)
        if cur: teile.append(cur)
        # Dauer am Maximum
        obs = A.Observer(e.latitude, e.longitude, 0)
        loc = A.SearchLocalSolarEclipse(e.peak.AddDays(-0.5), obs)
        dauer = None
        if loc.total_begin and loc.total_end:
            dauer = round((loc.total_end.time.ut - loc.total_begin.time.ut) * 86400)
        u = e.peak.Utc()
        raus.append({'datum': f'{u.year:04d}-{u.month:02d}-{u.day:02d}', 'max_utc': f'{u.hour:02d}:{u.minute:02d}:{u.second:02.0f}'.replace(':60', ':59'),
                     'art': ART[e.kind], 'lon': r2(e.longitude), 'lat': r2(e.latitude), 'dauer_s': dauer,
                     'dauer': f'{dauer // 60} min {dauer % 60:02d} s' if dauer else None, 'p': teile})
        print(raus[-1]['datum'], raus[-1]['max_utc'], raus[-1]['art'], raus[-1]['lat'], raus[-1]['lon'], raus[-1]['dauer'], sum(len(x) for x in teile), 'Punkte')
    e = A.NextGlobalSolarEclipse(e.peak)
# Linien ausdünnen: jeden 3. Punkt (3 min) behalten, Enden immer
for r in raus:
    r['p'] = [[q for i, q in enumerate(t) if i % 3 == 0 or i == len(t) - 1] for t in r['p']]
schreibe({
    'id': 'sonnenfinsternisse', 'name': 'Sonnenfinsternisse 2026–2040', 'gruppe': 'Himmel', 'typ': 'linien', 'einheit': '',
    'legende': [['totale Finsternis', '#ffffff'], ['ringförmige Finsternis', '#ffb84a'], ['hybrid', '#ffe08a'], ['Ort des Maximums', '#ff4a4a']],
    'quellen': [{'t': 'astronomy-engine (Don Cross), Python-Paket „astronomy-engine“ (pip), Funktionen SearchGlobalSolarEclipse/SearchLocalSolarEclipse; Mittellinie selbst berechnet (prep/finsternisse.py)',
                 'u': 'https://github.com/cosinekitty/astronomy', 'stand': 'Paket 2.1.x, gerechnet 11/2026', 'lizenz': 'MIT (Software); Ergebnisse eigene Rechnung'},
                {'t': 'Prüfung: NASA Eclipse Web Site (F. Espenak), Fünf-Jahrtausend-Katalog der Sonnenfinsternisse', 'u': 'https://eclipse.gsfc.nasa.gov/SEdecade/SEdecade2021.html', 'stand': 'abgerufen 11/2026', 'lizenz': 'gemeinfrei (NASA), nur zum Abgleich'}],
    'hinweis': 'Nur totale, ringförmige und hybride Finsternisse (partielle fehlen). Maximum = Ort, wo die Schattenachse der Erdmitte am nächsten kommt (UTC). Dauer = totale bzw. ringförmige Phase am Ort des Maximums. Mittellinie in 3-Minuten-Schritten, an der Datumsgrenze geteilt; Breite des Schattenpfads ist nicht enthalten. Abweichung zu NASA in Stichproben siehe OFFEN.md.'
}, raus)
