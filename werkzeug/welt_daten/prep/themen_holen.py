#!/usr/bin/env python3
"""Themen-Ebenen der Weltkarte einsammeln und kompakt ablegen.

Aufruf:  python3 -I werkzeug/welt_daten/prep/themen_holen.py <ordner-a> <ordner-b> [ne_10m_admin_0_disputed_areas.geojson]

Liest alle Ebenen-Dateien (*.json mit Kopf {id, name, gruppe, typ, …, daten}) aus den Ordnern und schreibt
werkzeug/welt_daten/welt_themen.json:
  {v, stand, index:[{id,name,gruppe,typ,einheit,stand,anz,wahl?}], strittig:{…}, ebenen:{id:{Kopf…, daten…}}}
Kompakt gemacht wird nur die Form, nie der Inhalt:
  - Linienzüge/Ringe ([[lon,lat],…] bzw. Listen davon) -> {"_l": Base64-Varint} (1/100 Grad, delta-kodiert)
  - Listen gleichartiger Objekte (>= 8) -> {"_r": [Feldnamen], "d": [[Werte],…]}
  - platten.koord_flach und kreise.ringe werden vorher in Linienzüge umgewandelt.
welt_einbauen.py bettet `index` + `strittig` als #weltthemen-index ein und `ebenen` als #weltthemen
(gelesen erst, wenn eine Themen-Ebene eingeschaltet wird).
Umstrittene Gebiete: aus Natural Earth (NOTE_BRK „Admin. by …; Claimed by …“) -> deutsche Sätze „verwaltet von … · beansprucht von …“.
Ohne dritten Parameter bleibt der vorhandene Block `strittig` erhalten.
"""
import sys, os, json, glob, base64, re, math

HIER = os.path.dirname(os.path.abspath(__file__))
ZIEL = os.path.join(HIER, '..', 'welt_themen.json')
BASIS = os.path.join(HIER, '..', 'welt_basis.json')

# ---------- Varint-Kodierung (wie welt_fein: zigzag, 7 Bit je Byte) ----------
def zz(v): return v * 2 if v >= 0 else -v * 2 - 1
def varint(out, v):
    while True:
        b = v & 127; v >>= 7
        if v: out.append(b | 128)
        else: out.append(b); return

def enc_linien(linien):
    """Liste von Linienzügen [[lon,lat],…] -> Base64; je Linie: Anzahl, Start relativ zum Ende der vorigen, dann Schritte."""
    out = bytearray(); lx = ly = 0
    for l in linien:
        varint(out, len(l))
        for x, y in l:
            xi, yi = int(round(x * 100)), int(round(y * 100))
            varint(out, zz(xi - lx)); varint(out, zz(yi - ly)); lx, ly = xi, yi
    return base64.b64encode(bytes(out)).decode()

def ist_zahl(v): return isinstance(v, (int, float)) and not isinstance(v, bool)
def ist_linie(v): return isinstance(v, list) and len(v) >= 2 and all(isinstance(p, list) and len(p) == 2 and ist_zahl(p[0]) and ist_zahl(p[1]) for p in v)
def ist_linien(v): return isinstance(v, list) and len(v) >= 1 and all(ist_linie(l) for l in v)

def kompakt(v):
    if isinstance(v, dict): return {k: kompakt(x) for k, x in v.items()}
    if isinstance(v, list):
        if ist_linien(v): return {'_l': enc_linien(v)}
        if len(v) >= 8 and all(isinstance(x, dict) for x in v):
            felder = []
            for x in v:
                for k in x:
                    if k not in felder: felder.append(k)
            return {'_r': felder, 'd': [[kompakt(x.get(k)) for k in felder] for x in v]}
        return [kompakt(x) for x in v]
    if isinstance(v, float):
        r = round(v, 4); return int(r) if r == int(r) and abs(r) < 1e15 else r
    return v

def vorbereiten(e):
    """Sonderformen in Linienzüge umwandeln (nur Form, keine Inhalte)."""
    if e['id'] == 'platten':
        f = e.get('felder') or []
        if 'koord_flach' in f:
            i = f.index('koord_flach')
            for z in e['daten']:
                k = z[i]; z[i] = [[[k[j], k[j + 1]] for j in range(0, len(k) - 1, 2)]]
    if e['typ'] == 'kreise':
        f = e.get('felder') or []
        if 'ringe' in f:
            i = f.index('ringe')
            for z in e['daten']:
                neu = []
                for r in z[i]:
                    x, y = r[0], r[1]; pts = [[x / 100, y / 100]]
                    for j in range(2, len(r) - 1, 2): x += r[j]; y += r[j + 1]; pts.append([x / 100, y / 100])
                    neu.append(pts)
                z[i] = neu
    return e

def anzahl(e):
    d = e.get('daten')
    if isinstance(d, (list, dict)): return len(d)
    return None

# ---------- Umstrittene Gebiete ----------
EN = {  # englische Namen in Natural Earth NOTE_BRK -> ISO3 der App (deutscher Name kommt aus welt_basis.json)
 'India':'IND','Pakistan':'PAK','China':'CHN','South Sudan':'SSD','Israel':'ISR','Syria':'SYR','Somalia':'SOM','Suriname':'SUR','France':'FRA',
 'Guyana':'GUY','Morocco':'MAR','Western Sahara':'ESH','Georgia':'GEO','Venezuela':'VEN','Azer.':'AZE','Nepal':'NPL','Brazil':'BRA','Uruguay':'URY',
 'Spain':'ESP','Portugal':'PRT','Moldova':'MDA','Ukraine':'UKR','Russia':'RUS','U.K.':'GBR','Sudan':'SDN','Cyprus':'CYP','Kazakhstan':'KAZ','Chile':'CHL',
 'Argentina':'ARG','Bhutan':'BTN','Lebanon':'LBN','Egypt':'EGY','Palestine':'PSE','Taiwan':'TWN','Saudi Arabia':'SAU','Madagascar':'MDG','Comoros':'COM',
 'Mauritius':'MUS','Seychelles':'SYC','the Seychelles':'SYC','Japan':'JPN','Vietnam':'VNM','U.S.A.':'USA','U.S.A':'USA','the United States':'USA','United States':'USA',
 'Tokelau':'NZL','Malaysia':'MYS','the Philippines':'PHL','Philippines':'PHL','Brunei':'BRN','Marshall Islands':'MHL','Ireland':'IRL','Denmark':'DNK','Iceland':'ISL',
 'Haiti':'HTI','UAE':'ARE','Colombia':'COL','Jamaica':'JAM','Nicaragua':'NIC','Honduras':'HND','Guatemala':'GTM','Canada':'CAN','Equatorial Guinea':'GNQ',
 'Djibouti':'DJI','Eritrea':'ERI','Gabon':'GAB','Kenya':'KEN','Iran':'IRN','Cuba':'CUB','South Korea':'KOR','Belize':'BLZ','Vanuatu':'VUT','Mali':'MLI'}
NAME_KORR = {'Spratly Is.':'Spratly-Inseln', 'Tiran and Sanafir Is.':'Tiran und Sanafir'}   # offensichtlich falsches NAME_DE in der Quelle
WEG = {'Israel', 'Belize'}          # ganze Staatsfläche – Grenzen stehen schon in der Grundkarte
WEG_ART = ('overlay',)              # UN-Pufferzonen/Demarkationsstreifen: keine Gebietsansprüche

def ring_vereinfachen(r, tol=0.015):
    if len(r) < 8: return r
    def dp(a, b):
        ax, ay = r[a]; bx, by = r[b]; dx, dy = bx - ax, by - ay; L = math.hypot(dx, dy) or 1e-12; best = -1; bi = -1
        for i in range(a + 1, b):
            d = abs(dy * (r[i][0] - ax) - dx * (r[i][1] - ay)) / L
            if d > best: best, bi = d, i
        if best > tol: return dp(a, bi)[:-1] + dp(bi, b)
        return [r[a], r[b]]
    out = dp(0, len(r) - 1)
    return out if len(out) >= 4 else r

def strittig_bauen(pfad, laender):
    g = json.load(open(pfad)); name = lambda iso: laender.get(iso, iso)
    def teile(s):
        s = s.replace(' and ', ', ').replace(' & ', ', ')
        return [x.strip() for x in s.split(',') if x.strip()]
    def land(t):
        if t in EN: return name(EN[t])
        return t
    geb = []
    for f in g['features']:
        p = f['properties']; nm = p.get('NAME') or ''
        if nm in WEG or (any(w in (p.get('TYPE') or '').lower() for w in WEG_ART) and 'leased' not in (p.get('NOTE_BRK') or '').lower()): continue
        note = (p.get('NOTE_BRK') or '').strip(); verw = ''; ansp = ''; satz = []
        for teil in [t.strip() for t in note.split(';') if t.strip()]:
            m = re.match(r'(?i)admin\.? by (.+)', teil)
            if m:
                x = m.group(1)
                m2 = re.match(r'(.+?) for (.+)', x)
                verw = ' für '.join(land(y) for y in (m2.groups() if m2 else [x])); continue
            m = re.match(r'(?i)self admin\.?', teil)
            if m: verw = 'selbst verwaltet'; continue
            m = re.match(r'(?i)claimed by (.+)', teil)
            if m:
                xs = teil[len('claimed by '):]
                if xs.strip().lower() == 'multiple': ansp = 'mehrere Staaten'
                else: ansp = ', '.join(land(y) for y in teile(xs))
                continue
            m = re.match(r'(?i)leased to (.+?) by (.+)', teil)
            if m: satz.append(f'verpachtet von {land(m.group(2).strip())} an {land(m.group(1).strip())}'); continue
            m = re.match(r'(?i)ceded to (.+?) by (.+)', teil)
            if m: satz.append(f'von {land(m.group(2).strip())} an {land(m.group(1).strip())} abgetreten'); continue
            satz.append(teil)   # unverändert (englisch) übernehmen, nicht umdeuten
        nd = NAME_KORR.get(nm) or p.get('NAME_DE') or nm
        geo = f['geometry']; polys = geo['coordinates'] if geo['type'] == 'MultiPolygon' else [geo['coordinates']]
        ringe = []
        for poly in polys:
            r = [[round(x, 2), round(y, 2)] for x, y in poly[0]]
            r = ring_vereinfachen(r)
            ringe.append(r)
        geb.append({'n': nd, 'ne': nm, 'v': verw, 'a': ansp, 's': '; '.join(satz), 'art': p.get('TYPE') or '', 'l': {'_l': enc_linien(ringe)}})
    return geb

def main():
    if len(sys.argv) < 3: print(__doc__); sys.exit(1)
    ordner = sys.argv[1:3]; ne = sys.argv[3] if len(sys.argv) > 3 else None
    laender = {c['i']: c['n'] for c in json.load(open(BASIS))['laender']}
    ebenen = {}; index = []
    for o in ordner:
        for f in sorted(glob.glob(os.path.join(o, '*.json'))):
            try: e = json.load(open(f))
            except Exception as ex: print('übersprungen (kein JSON):', f, ex); continue
            if not isinstance(e, dict) or not all(k in e for k in ('id', 'name', 'gruppe', 'typ')) or not any(k.startswith('daten') for k in e):
                print('übersprungen (kein Ebenen-Kopf):', f); continue
            e = vorbereiten(e)
            q = (e.get('quellen') or [{}])[0]
            ix = {'id': e['id'], 'name': e['name'], 'gruppe': e['gruppe'], 'typ': e['typ'], 'einheit': e.get('einheit', ''), 'stand': q.get('stand', ''), 'anz': anzahl(e)}
            d = e.get('daten')
            if e['typ'] == 'land-liste' and isinstance(d, list):
                ix['wahl'] = [[x.get('id') or str(i), x.get('n', '')] for i, x in enumerate(d)]
            elif e['typ'] == 'land-kat' and isinstance(d, dict) and all(isinstance(x, dict) and 'heimat' in x for x in d.values()):
                ix['wahl'] = [[k, x.get('n', k)] for k, x in d.items()]
            # Kategorie-Feld einer Land-Kategorie-Ebene: das Feld, dessen Werte die Legenden-Schlüssel sind
            if e['typ'] == 'land-kat' and isinstance(e.get('legende'), list) and isinstance(d, dict):
                ks = {x.get('k') for x in e['legende'] if isinstance(x, dict)}; best = None; bn = 0
                felder = {k for x in d.values() if isinstance(x, dict) for k in x}
                for fe in felder:
                    n = sum(1 for x in d.values() if isinstance(x, dict) and not isinstance(x.get(fe), (list, dict)) and x.get(fe) in ks)
                    if n > bn: best, bn = fe, n
                if best: e['katfeld'] = best
            ebenen[e['id']] = kompakt(e); index.append(ix)
    alt = {}
    if os.path.exists(ZIEL):
        try: alt = json.load(open(ZIEL))
        except Exception: alt = {}
    if ne:
        strittig = {'q': 'Natural Earth 1:10 Mio., Admin-0 Disputed Areas (gemeinfrei)', 'u': 'https://github.com/nvkelso/natural-earth-vector',
                    'stand': 'Natural Earth ' + (open(os.path.join(os.path.dirname(ne), 'VERSION')).read().strip() if os.path.exists(os.path.join(os.path.dirname(ne), 'VERSION')) else 'v5'),
                    'g': strittig_bauen(ne, laender)}
    else: strittig = alt.get('strittig')
    stand = max((x['stand'] for x in index if x['stand']), default='')
    out = {'v': 1, 'index': index, 'strittig': strittig, 'ebenen': ebenen}
    s = json.dumps(out, ensure_ascii=False, separators=(',', ':'))
    open(ZIEL, 'w').write(s)
    print(f'{len(index)} Ebenen, {len(s.encode()) // 1024} KB -> {os.path.normpath(ZIEL)}' + (f'; {len(strittig["g"])} umstrittene Gebiete' if strittig else ''))
    for e in index: print(f"  {e['gruppe']:<12} {e['typ']:<10} {e['id']:<20} {e['anz']}")

if __name__ == '__main__': main()
