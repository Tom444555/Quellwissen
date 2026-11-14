#!/usr/bin/env python3
"""Aufbereitung der Feindaten für die Weltkarte (Globus, Karte, Scheibe).

Erzeugt aus gemeinfreien Natural-Earth-Daten (50m Land/Seen, 10m Städte) und dem NASA-Höhenbild:
  welt_daten/welt_fein.json  – Küsten (Land) und Seen als quantisierte, delta-kodierte Ringe (Base64-Varint),
                               Seenamen, zusätzliche Städte (nach Zoomstufe), Meerengen/Kaps/Inseln
  welt_daten/hoehe.jpg       – Höhen-/Tiefenbild 4096×2048 (128 = Meeresspiegel, darüber Land, darunter Tiefe)
Aufruf:  python3 werkzeug/welt_daten/prep/welt_fein_prep.py <ordner-mit-rohdaten>
Rohdaten: ne_50m_land.geojson, ne_50m_lakes.geojson, ne_10m_populated_places_simple.geojson, ne_10m_rivers_lake_centerlines.geojson,
ne_10m_admin_0_boundary_lines_land.geojson, elev_bump_4k.jpg
(Natural Earth: github.com/nvkelso/natural-earth-vector, gemeinfrei; Höhenbild: NASA, gemeinfrei).
Das bisherige hoehe.jpg (2048×1024, mit Meerestiefen) muss beim ersten Lauf noch vorhanden sein; es wird als
hoehe_2k.jpg im Rohdaten-Ordner gesichert und für die Meerestiefen weiterverwendet.
"""
import json, math, os, sys, base64, shutil
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

ROH = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/scratch/weltdaten'
HIER = os.path.dirname(os.path.abspath(__file__))
WD = os.path.dirname(HIER)
Q = 100  # Quantisierung: 1/100 Grad

def dp(pts, tol):
    """Douglas-Peucker-Vereinfachung."""
    pts = np.asarray(pts, float); n = len(pts)
    if n < 5 or tol <= 0: return pts
    keep = np.zeros(n, bool); keep[0] = keep[-1] = True; st = [(0, n - 1)]
    while st:
        a, b = st.pop()
        if b <= a + 1: continue
        p = pts[a + 1:b]; A = pts[a]; d = pts[b] - A; L = math.hypot(*d)
        dist = np.hypot(*(p - A).T) if L == 0 else np.abs(d[0] * (p[:, 1] - A[1]) - d[1] * (p[:, 0] - A[0])) / L
        i = int(np.argmax(dist))
        if dist[i] > tol: keep[a + 1 + i] = True; st += [(a, a + 1 + i), (a + 1 + i, b)]
    return pts[keep]

def varint(out, v):
    v = (v << 1) ^ (v >> 63) if v < 0 else v << 1  # zigzag
    while True:
        b = v & 0x7f; v >>= 7
        if v: out.append(b | 0x80)
        else: out.append(b); return

def ringe(features, tol, minfl=0.0):
    out = bytearray(); n = 0; r = 0
    for ft in features:
        g = ft['geometry']; polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
        for p in polys:
            for k, ring in enumerate(p):
                s = dp(ring, tol)
                q = np.round(s * Q).astype(np.int64)
                q = q[np.r_[True, np.any(np.diff(q, axis=0) != 0, axis=1)]]
                if len(q) > 1 and (q[0] == q[-1]).all(): q = q[:-1]
                if len(q) < 3: continue
                x, y = q[:, 0].astype(float), q[:, 1].astype(float)
                fl = abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1))) / 2 / Q / Q
                if fl < minfl: continue
                varint(out, len(q)); varint(out, int(q[0, 0])); varint(out, int(q[0, 1]))
                for d in np.diff(q, axis=0): varint(out, int(d[0])); varint(out, int(d[1]))
                n += len(q); r += 1
    return base64.b64encode(bytes(out)).decode(), n, r

def linien(features, tol, rang):
    """Linien: je Linie varint(Rang/Art), varint(Anzahl), Start absolut, dann Deltas."""
    out = bytearray(); n = 0
    for ft in features:
        g = ft['geometry']; p = ft['properties']
        sr = rang(p) if g else None
        if sr is None: continue
        ls = g['coordinates'] if g['type'] == 'MultiLineString' else [g['coordinates']]
        for l in ls:
            q = np.round(dp(l, tol) * Q).astype(np.int64)
            q = q[np.r_[True, np.any(np.diff(q, axis=0) != 0, axis=1)]]
            if len(q) < 2: continue
            varint(out, sr); varint(out, len(q)); varint(out, int(q[0, 0])); varint(out, int(q[0, 1]))
            for d in np.diff(q, axis=0): varint(out, int(d[0])); varint(out, int(d[1]))
            n += len(q)
    return base64.b64encode(bytes(out)).decode(), n

def innenpunkt(rings):
    """Beschriftungspunkt: Punkt mit größtem Abstand zum Ufer (Raster-Abstandstransformation)."""
    a = np.asarray(rings[0]); x0, y0 = a.min(0); x1, y1 = a.max(0)
    k = max(x1 - x0, y1 - y0) / 120 or 0.01; w = int((x1 - x0) / k) + 3; h = int((y1 - y0) / k) + 3
    im = Image.new('L', (w, h), 0); dr = ImageDraw.Draw(im)
    tf = lambda r: [((x - x0) / k + 1, (y1 - y) / k + 1) for x, y in r]
    dr.polygon(tf(rings[0]), fill=1)
    for r in rings[1:]: dr.polygon(tf(r), fill=0)
    m = np.asarray(im); dt = ndimage.distance_transform_edt(m)
    j, i = np.unravel_index(np.argmax(dt), dt.shape)
    return round(x0 + (i - 1) * k, 2), round(y1 - (j - 1) * k, 2)

DE_NAMEN = {  # gebräuchliche deutsche Namen für neu hinzugekommene Städte
 'Cologne': 'Köln', 'Hanover': 'Hannover', 'Nice': 'Nizza', 'Liège': 'Lüttich', 'Brugge': 'Brügge', 'Zaragoza': 'Saragossa',
 'Tangier': 'Tanger', 'Pizen': 'Pilsen', 'Århus': 'Aarhus', 'Zaporizhzhya': 'Saporischschja', 'Kryvyy Rih': 'Krywyj Rih',
 'Mykolayiv': 'Mykolajiw', 'Homyel': 'Homel', 'Vinnytsya': 'Winnyzja', 'Kherson': 'Cherson', 'Poltava': 'Poltawa',
 'Chernihiv': 'Tschernihiw', 'Chernivtsi': 'Czernowitz', 'Cherkasy': 'Tscherkassy', 'Rivne': 'Riwne',
 'Ivano-Frankivsk': 'Iwano-Frankiwsk', 'Lutsk': 'Luzk', 'Uzhgorod': 'Uschhorod', 'Kerch': 'Kertsch', 'Ṭarābulus': 'Tripoli (Libanon)',
 'Lemosos': 'Limassol', 'Iraklio': 'Heraklion', 'Patra': 'Patras', 'Piraeus': 'Piräus', 'Icel': 'Mersin', 'Tlimcen': 'Tlemcen',
 'Tiarat': 'Tiaret', 'Starsy Oskol': 'Stary Oskol', 'Kirovohrad': 'Kropywnyzkyj', 'Khmelnytskyy': 'Chmelnyzkyj',
 'Velikiy Novgorod': 'Weliki Nowgorod', 'Castello': 'Castellón', 'La Coruña': 'A Coruña', 'Gdańsk': 'Danzig',
 'Szczecin': 'Stettin', 'Kaliningrad': 'Kaliningrad', 'Lviv': 'Lwiw', 'Venice': 'Venedig', 'Turin': 'Turin', 'Genoa': 'Genua',
 'Padua': 'Padua', 'Seville': 'Sevilla', 'Gothenburg': 'Göteborg', 'Bruges': 'Brügge', 'Ghent': 'Gent', 'Antwerp': 'Antwerpen',
 'Strasbourg': 'Straßburg', 'Geneva': 'Genf', 'Zurich': 'Zürich', 'Bern': 'Bern', 'Luzern': 'Luzern', 'Syracuse': 'Syrakus',
 'Siracusa': 'Syrakus', 'Reggio di Calabria': 'Reggio Calabria', 'Mantova': 'Mantua', 'Thessaloniki': 'Thessaloniki',
 'Lemberg': 'Lwiw', 'Mecca': 'Mekka', 'Medina': 'Medina', 'Aleppo': 'Aleppo', 'Jerusalem': 'Jerusalem', 'Nicosia': 'Nikosia',
 'Valletta': 'Valletta', 'Corinth': 'Korinth', 'Ostrava': 'Ostrava', 'Brno': 'Brünn', 'Košice': 'Košice', 'Kraków': 'Krakau',
 'Kyiv': 'Kiew', 'Odesa': 'Odessa', 'Moscow': 'Moskau', 'Bucharest': 'Bukarest', 'Belgrade': 'Belgrad', 'Copenhagen': 'Kopenhagen',
 'Lisbon': 'Lissabon', 'Rome': 'Rom', 'Naples': 'Neapel', 'Florence': 'Florenz', 'Milan': 'Mailand', 'Vienna': 'Wien',
 'Prague': 'Prag', 'Warsaw': 'Warschau', 'Brussels': 'Brüssel', 'Munich': 'München', 'Nuremberg': 'Nürnberg',
 'The Hague': 'Den Haag', 'Algiers': 'Algier', 'Cairo': 'Kairo', 'Alexandria': 'Alexandria', 'Tripoli': 'Tripolis',
 'Damascus': 'Damaskus', 'Baghdad': 'Bagdad', 'Tehran': 'Teheran', 'Beijing': 'Peking', 'Tokyo': 'Tokio',
 'Cape Town': 'Kapstadt', 'Singapore': 'Singapur', 'Havana': 'Havanna', 'Mexico City': 'Mexiko-Stadt',
 'Arkhangelsk': 'Archangelsk', 'Nizhny Novgorod': 'Nischni Nowgorod', 'Yekaterinburg': 'Jekaterinburg',
 'Novosibirsk': 'Nowosibirsk', 'Vladivostok': 'Wladiwostok', 'Khabarovsk': 'Chabarowsk', 'Yakutsk': 'Jakutsk',
 'Murmansk': 'Murmansk', 'Kazan': 'Kasan', 'Volgograd': 'Wolgograd', 'Rostov': 'Rostow am Don', 'Samara': 'Samara',
 'Chelyabinsk': 'Tscheljabinsk', 'Omsk': 'Omsk', 'Krasnoyarsk': 'Krasnojarsk', 'Irkutsk': 'Irkutsk', 'Vladimir': 'Wladimir',
 'Kaluga': 'Kaluga', 'Smolensk': 'Smolensk', 'Tver': 'Twer', 'Yaroslavl': 'Jaroslawl', 'Vologda': 'Wologda',
 'Kostroma': 'Kostroma', 'Ivanovo': 'Iwanowo', 'Orel': 'Orjol', 'Belgorod': 'Belgorod', 'Lipetsk': 'Lipezk', 'Tambov': 'Tambow',
 'Taganrog': 'Taganrog', 'Novorossiysk': 'Noworossijsk', 'Pyatigorsk': 'Pjatigorsk', 'Vladikavkaz': 'Wladikawkas',
 'Simferopol': 'Simferopol', 'Sevastopol': 'Sewastopol', 'Vitsyebsk': 'Wizebsk', 'Mahilyow': 'Mahiljou', 'Hrodna': 'Hrodna',
 'Babruysk': 'Babrujsk', 'Baranavichy': 'Baranawitschy', 'Barysaw': 'Baryssau', 'Pinsk': 'Pinsk', 'Orsha': 'Orscha',
 'Kremenchuk': 'Krementschuk', 'Kharkiv': 'Charkiw', 'Dnipro': 'Dnipro', 'Donetsk': 'Donezk', 'Horlivka': 'Horliwka',
 'Makiyivka': 'Makijiwka', 'Luhansk': 'Luhansk', 'Lysychansk': 'Lyssytschansk', 'Sumy': 'Sumy', 'Ternopil': 'Ternopil',
 'Drohobych': 'Drohobytsch', 'Bila Tserkva': 'Bila Zerkwa', 'Melitopol': 'Melitopol', 'Nikopol': 'Nikopol',
 'Tiraspol': 'Tiraspol', 'Bălți': 'Bălți', 'Kutaisi': 'Kutaissi', 'Gyumri': 'Gjumri', 'Tartus': 'Tartus', 'Latakia': 'Latakia',
 'Hamah': 'Hama', 'Ar Raqqah': 'Rakka', 'Dayr az Zawr': 'Deir ez-Zor', 'Irbil': 'Erbil', 'Samarra': 'Samarra',
 'Qairouan': 'Kairouan', 'Bizerte': 'Bizerta', 'Kenitra': 'Kenitra', 'Antakya': 'Antakya', 'Kahramanmaraş': 'Kahramanmaraş',
 'Corum': 'Çorum', 'Afyon': 'Afyonkarahisar', 'Granada‎': 'Granada', 'Salerno': 'Salerno', 'Kingston upon Hull': 'Hull',
 'Stoke': 'Stoke-on-Trent', "'s-Hertogenbosch": 'Den Bosch', 'Velikiye Luki': 'Welikije Luki', 'Pskov': 'Pskow',
 'Petrozavodsk': 'Petrosawodsk', 'Syktyvkar': 'Syktywkar', 'Kirov': 'Kirow', 'Perm': 'Perm', 'Ufa': 'Ufa', 'Orenburg': 'Orenburg',
 'Saratov': 'Saratow', 'Penza': 'Pensa', 'Ulyanovsk': 'Uljanowsk', 'Astrakhan': 'Astrachan', 'Makhachkala': 'Machatschkala',
 'Grozny': 'Grosny', 'Tyumen': 'Tjumen', 'Tomsk': 'Tomsk', 'Barnaul': 'Barnaul', 'Novokuznetsk': 'Nowokusnezk',
 'Kemerovo': 'Kemerowo', 'Chita': 'Tschita', 'Ulan Ude': 'Ulan-Ude', 'Magadan': 'Magadan', 'Norilsk': 'Norilsk',
 'Petropavlovsk-Kamchatsky': 'Petropawlowsk-Kamtschatski', 'Yuzhno Sakhalinsk': 'Juschno-Sachalinsk', 'Anadyr': 'Anadyr',
}

MARKEN = [  # Meerengen (m), Kaps (k), Inseln (i): [Name, Länge, Breite, Stufe, Art]
 ['Straße von Gibraltar', -5.6, 35.95, 5.5, 'm'], ['Bosporus', 29.07, 41.12, 7, 'm'], ['Dardanellen', 26.4, 40.2, 7, 'm'],
 ['Ärmelkanal', -2.5, 50.0, 5, 'm'], ['Straße von Dover', 1.45, 51.0, 7, 'm'], ['Skagerrak', 9.0, 57.9, 6, 'm'],
 ['Kattegat', 11.4, 56.9, 6.5, 'm'], ['Öresund', 12.7, 55.85, 8, 'm'], ['Straße von Messina', 15.62, 38.2, 8, 'm'],
 ['Straße von Otranto', 18.9, 40.3, 7, 'm'], ['Straße von Hormus', 56.4, 26.55, 6, 'm'], ['Bab al-Mandab', 43.35, 12.6, 6.5, 'm'],
 ['Straße von Malakka', 100.0, 3.8, 5.5, 'm'], ['Sundastraße', 105.8, -6.0, 7, 'm'], ['Taiwanstraße', 119.6, 24.2, 6, 'm'],
 ['Koreastraße', 129.2, 34.4, 6.5, 'm'], ['Beringstraße', -168.9, 65.8, 5.5, 'm'], ['Magellanstraße', -70.6, -53.3, 6.5, 'm'],
 ['Drakestraße', -63.5, -58.5, 4.5, 'm'], ['Bass-Straße', 146.0, -39.6, 6, 'm'], ['Cookstraße', 174.5, -41.2, 7, 'm'],
 ['Floridastraße', -80.6, 24.0, 6, 'm'], ['Yucatánstraße', -85.7, 21.6, 6.5, 'm'], ['Davisstraße', -58.0, 66.5, 5, 'm'],
 ['Dänemarkstraße', -27.5, 67.0, 5, 'm'], ['Straße von Mosambik', 41.0, -18.0, 4.5, 'm'], ['Palkstraße', 79.7, 10.1, 7, 'm'],
 ['Tatarensund', 141.6, 50.5, 6.5, 'm'], ['Straße von Kertsch', 36.55, 45.3, 8, 'm'], ['Suezkanal', 32.35, 30.45, 7.5, 'm'],
 ['Panamakanal', -79.75, 9.1, 7.5, 'm'], ['Nordkanal', -5.6, 55.2, 7.5, 'm'], ['Straße von Belle Isle', -56.6, 51.6, 7.5, 'm'],
 ['Kap Hoorn', -67.27, -55.98, 6, 'k'], ['Kap der Guten Hoffnung', 18.47, -34.36, 6, 'k'], ['Kap Agulhas', 20.0, -34.83, 7.5, 'k'],
 ['Nordkap', 25.78, 71.17, 6.5, 'k'], ['Kap Finisterre', -9.27, 42.88, 7.5, 'k'], ['Kap São Vicente', -8.99, 37.02, 8, 'k'],
 ['Kap Tscheljuskin', 104.3, 77.72, 6.5, 'k'], ['Kap Deschnjow', -169.65, 66.08, 7, 'k'], ['Kap York', 142.53, -10.69, 7, 'k'],
 ['Kap Komorin', 77.54, 8.08, 7, 'k'], ['Kap Verde (Cap-Vert)', -17.51, 14.72, 7.5, 'k'], ['Kap Farvel', -43.9, 59.77, 7, 'k'],
 ['Kap Guardafui', 51.27, 11.83, 7, 'k'], ['Kap Cod', -70.2, 41.75, 7.5, 'k'], ['Kap Canaveral', -80.6, 28.45, 8, 'k'],
 ['Grönland', -41.0, 74.0, 3.5, 'i'], ['Madagaskar', 46.7, -19.5, 4.5, 'i'], ['Borneo', 114.0, 0.8, 4.5, 'i'],
 ['Sumatra', 101.5, -0.3, 5, 'i'], ['Java', 110.0, -7.4, 5.5, 'i'], ['Neuguinea', 141.0, -5.0, 4.5, 'i'],
 ['Honshū', 138.5, 36.4, 6, 'i'], ['Hokkaidō', 142.8, 43.4, 6.5, 'i'], ['Sachalin', 142.8, 50.5, 6, 'i'],
 ['Tasmanien', 146.6, -42.0, 6, 'i'], ['Nordinsel', 175.6, -38.8, 6.5, 'i'], ['Südinsel', 170.5, -43.8, 6.5, 'i'],
 ['Hispaniola', -71.5, 19.0, 6.5, 'i'], ['Neufundland', -56.0, 48.7, 6, 'i'], ['Baffininsel', -71.0, 69.0, 5, 'i'],
 ['Ellesmere-Insel', -79.0, 79.8, 5.5, 'i'], ['Victoria-Insel', -110.0, 71.0, 5.5, 'i'], ['Spitzbergen', 16.5, 78.6, 5.5, 'i'],
 ['Nowaja Semlja', 56.0, 74.0, 5.5, 'i'], ['Sizilien', 14.1, 37.55, 6.5, 'i'], ['Sardinien', 9.0, 40.05, 6.5, 'i'],
 ['Korsika', 9.1, 42.15, 7, 'i'], ['Kreta', 24.9, 35.22, 7, 'i'], ['Mallorca', 2.95, 39.62, 8, 'i'], ['Feuerland', -68.5, -54.2, 6.5, 'i'],
 ['Kanarische Inseln', -15.6, 28.3, 7, 'i'], ['Azoren', -28.0, 38.6, 6.5, 'i'], ['Hawaii', -155.5, 19.6, 6, 'i'],
 ['Luzon', 121.0, 16.5, 6.5, 'i'], ['Mindanao', 125.0, 7.6, 6.5, 'i'], ['Sulawesi', 120.5, -2.0, 6, 'i'], ['Hainan', 109.7, 19.2, 6.5, 'i'],
 ['Großbritannien', -1.8, 53.6, 7.5, 'i'], ['Kamtschatka', 159.0, 56.5, 5.5, 'i'], ['Sewernaja Semlja', 98.0, 79.4, 6, 'i'],
 ['Franz-Josef-Land', 55.0, 80.8, 6.5, 'i'], ['Galápagos-Inseln', -90.5, -0.6, 7, 'i'], ['Färöer', -6.9, 62.05, 8, 'i'],
 ['Shetlandinseln', -1.3, 60.35, 8, 'i'], ['Lofoten', 13.9, 68.2, 8, 'i'], ['Gotland', 18.5, 57.45, 8, 'i'],
]

def main():
    land = json.load(open(os.path.join(ROH, 'ne_50m_land.geojson')))['features']
    seen = json.load(open(os.path.join(ROH, 'ne_50m_lakes.geojson')))['features']
    L, nl, rl = ringe(land, 0.01)
    # Seen: Natural-Earth-Seen ohne Stauseen-Duplikate, kleinste Flächen fallen weg
    S, ns, rs = ringe(seen, 0.01, 0.004)
    print('Land', rl, 'Ringe', nl, 'Punkte', len(L) // 1024, 'KB  Seen', rs, ns, len(S) // 1024, 'KB')
    sn = []
    for ft in seen:
        p = ft['properties']; n = p.get('name_de') or p.get('name')
        if not n or p.get('featurecla') == 'Reservoir' and (p.get('scalerank') or 9) > 3: continue
        g = ft['geometry']; polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
        big = max(polys, key=lambda pp: len(pp[0]))
        lo, la = innenpunkt(big)
        a = np.asarray(big[0]); fl = abs(np.dot(a[:, 0], np.roll(a[:, 1], 1)) - np.dot(a[:, 1], np.roll(a[:, 0], 1))) / 2
        km2 = fl * 111.2 ** 2 * math.cos(math.radians(la))
        st = round(min(9.5, max(3.6, 9.4 - 1.7 * math.log10(max(km2, 50) / 100))), 1)
        n = {'Oberer': 'Oberer See'}.get(n.strip(), n.strip())
        sn.append([n, lo, la, st])
    sn.sort(key=lambda s: s[3])
    print('Seenamen', len(sn))
    # Städte: alle 10m-Orte, die noch nicht in welt_basis stehen
    basis = json.load(open(os.path.join(WD, 'welt_basis.json')))
    alt = basis['staedte']
    ne = [f['properties'] for f in json.load(open(os.path.join(ROH, 'ne_10m_populated_places_simple.geojson')))['features']]
    ax = np.array([[s[1], s[2]] for s in alt])
    neu = []
    for p in ne:
        d = np.hypot(ax[:, 0] - p['longitude'], ax[:, 1] - p['latitude']).min()
        if d < 0.02: continue
        n = ' '.join(p['name'].replace('‎', '').split())
        n = DE_NAMEN.get(n, n)
        mz = p['min_zoom'] if p['min_zoom'] else 9
        neu.append([n, round(p['longitude'], 2), round(p['latitude'], 2), round(max(p['pop_max'], 0) / 1e6, 3), mz, 1 if p['adm0cap'] else 0])
    neu.sort(key=lambda s: (s[4], -s[3]))
    print('Städte neu', len(neu))
    fl, nf = linien(json.load(open(os.path.join(ROH, 'ne_10m_rivers_lake_centerlines.geojson')))['features'], 0.015,
                    lambda p: int(p.get('scalerank') or 9) if p.get('featurecla') == 'River' else None)
    print('Flüsse', nf, 'Punkte', len(fl) // 1024, 'KB')
    # Landgrenzen (ohne Küsten): 0 = Staatsgrenze, 1 = umstritten/unbestimmt (gestrichelt)
    gr, ng = linien(json.load(open(os.path.join(ROH, 'ne_10m_admin_0_boundary_lines_land.geojson')))['features'], 0.02,
                    lambda p: 0 if p.get('FEATURECLA', '').startswith('International') else None if p.get('FEATURECLA', '').startswith(('Overlay', 'Lease')) else 1)
    print('Grenzen', ng, 'Punkte', len(gr) // 1024, 'KB')
    fein = {'land': L, 'seen': S, 'fluesse': fl, 'grenzen': gr, 'seeN': sn, 'staedte': neu, 'marken': MARKEN}
    json.dump(fein, open(os.path.join(WD, 'welt_fein.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
    print('welt_fein.json', os.path.getsize(os.path.join(WD, 'welt_fein.json')) // 1024, 'KB')

    # Höhenbild 4096×2048: Land aus elev_bump_4k (über Kennlinie auf die bisherige Skala), Meer aus dem alten Bild
    alt2k = os.path.join(ROH, 'hoehe_2k.jpg')
    if not os.path.exists(alt2k): shutil.copy(os.path.join(WD, 'hoehe.jpg'), alt2k)
    h2 = np.asarray(Image.open(alt2k).convert('L')).astype(np.float32)
    b4 = np.asarray(Image.open(os.path.join(ROH, 'elev_bump_4k.jpg')).convert('L')).astype(np.float32)
    # Kennlinie Bump -> Höhenwert aus den Landpixeln (2k-Vergleich)
    b2 = np.asarray(Image.fromarray(b4.astype(np.uint8)).resize((2048, 1024), Image.BILINEAR)).astype(np.float32)
    m = h2 > 133
    lut = np.zeros(256, np.float32)
    for v in range(256):
        sel = m & (np.abs(b2 - v) < 1.5)
        lut[v] = np.median(h2[sel]) if sel.sum() > 30 else np.nan
    ok = ~np.isnan(lut); lut = np.interp(np.arange(256), np.arange(256)[ok], lut[ok])
    lut = np.maximum.accumulate(np.clip(lut, 130, 255))
    land4 = lut[np.clip(b4, 0, 255).astype(int)]
    land4 = ndimage.gaussian_filter(land4, 0.6)
    meer4 = np.asarray(Image.fromarray(h2.astype(np.uint8)).resize((4096, 2048), Image.BICUBIC)).astype(np.float32)
    meer4 = np.minimum(meer4, 126)
    # Landmaske 50m (vektor) in 4096
    im = Image.new('L', (4096 * 2, 2048 * 2), 0); dr = ImageDraw.Draw(im)
    tf = lambda r: [((x + 180) / 360 * 8192, (90 - y) / 180 * 4096) for x, y in r]
    for ft in land:
        g = ft['geometry']; polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
        for p in polys:
            dr.polygon(tf(p[0]), fill=255)
            for r in p[1:]: dr.polygon(tf(r), fill=0)
    mk = np.asarray(im.resize((4096, 2048), Image.BOX)).astype(np.float32) / 255
    mk = ndimage.gaussian_filter(mk, 0.7)
    out = meer4 * (1 - mk) + land4 * mk
    Image.fromarray(np.clip(out + 0.5, 0, 255).astype(np.uint8)).save(os.path.join(WD, 'hoehe.jpg'), quality=82, optimize=True)
    print('hoehe.jpg', os.path.getsize(os.path.join(WD, 'hoehe.jpg')) // 1024, 'KB')

if __name__ == '__main__':
    main()
