"""Naturparks in Deutschland aus Wikidata (CC0) -> naturparks.json; Abgleich mit der VDN-Liste (naturparke.de).
Eingaben: roh/naturparks.json (q_naturparks.rq: Klasse Q20354035 „Naturpark in Deutschland“ + Q728904 „Naturpark“ mit Staat
Deutschland), roh/vdn/liste.html -> roh/vdn/vdn_namen.json, roh/vdn/vdn_laender.json.
Aufruf: cd /home/claude/scratch/wikidata && python3 -I naturparks.py"""
import json, re, sys, collections, unicodedata
sys.path.insert(0, '/home/claude/scratch/wikidata')
import geo

STAND = '26.11.2026'
B = json.load(open('roh/naturparks.json'))['results']['bindings']
VDN = json.load(open('roh/vdn/vdn_namen.json'))
VDN_L = json.load(open('roh/vdn/vdn_laender.json'))
KUERZ = {'Baden-Württemberg': 'BW', 'Bayern': 'BY', 'Berlin': 'BE', 'Brandenburg': 'BB', 'Hessen': 'HE',
         'Mecklenburg-Vorpommern': 'MV', 'Niedersachsen': 'NI', 'Nordrhein-Westfalen': 'NW', 'Rheinland-Pfalz': 'RP',
         'Saarland': 'SL', 'Sachsen': 'SN', 'Sachsen-Anhalt': 'ST', 'Schleswig-Holstein': 'SH', 'Thüringen': 'TH',
         'Bremen': 'HB', 'Hamburg': 'HH'}
VDN_LAND = collections.defaultdict(list)
for l, slugs in VDN_L.items():
    for s in slugs: VDN_LAND[s].append(KUERZ[l])

it = {}
for b in B:
    q = b['i']['value'].rsplit('/', 1)[1]
    x = it.setdefault(q, {'n': b.get('de', {}).get('value') or b.get('en', {}).get('value'), 'c': [], 'f': set(),
                          'g': set(), 'a': set(), 'k': set()})
    if 'coord' in b:
        m = re.match(r'Point\(([-\d.eE]+) ([-\d.eE]+)\)', b['coord']['value'])
        c = (float(m[1]), float(m[2]))
        if c not in x['c']: x['c'].append(c)
    if 'flaeche' in b: x['f'].add((float(b['flaeche']['value']), b['einheit']['value'].rsplit('/', 1)[1]))
    if 'gruend' in b: x['g'].add(int(b['gruend']['value'][:4]))
    if 'aufl' in b: x['a'].add(b['aufl']['value'][:10])
    x['k'].add(b['klasse']['value'])

# Nur Klasse „Naturpark in Deutschland“ (Q20354035). Aus der allgemeinen Klasse nur geprüft: dort stehen Dachobjekte
# grenzüberschreitender Parks (deutscher Teil ist eigenes Objekt der DE-Klasse) und Fremdes.
NICHT = {'Q1201800': 'Dachobjekt Deutsch-Luxemburgischer Naturpark (deutscher Teil = Naturpark Südeifel)',
         'Q1747379': 'Dachobjekt Maas-Schwalm-Nette (deutscher Teil = Naturpark Schwalm-Nette)',
         'Q317524': 'Dachobjekt Hohes Venn-Eifel (deutscher Teil eigenes Objekt)',
         'Q872763': 'Doppel zu Q115596723 (Bourtanger Moor-Bargerveen)',
         'Q1260267': 'Doppel zu Q115649191 (Nagelfluhkette)',
         'Q1203595': 'Sammelbegriff', 'Q1737740': 'Programm der DDR, kein Park', 'Q61082617': 'Kressepark Erfurt (kein Naturpark nach § 27 BNatSchG)',
         'Q123581313': 'Hüttener Berge/Schlei: unklares Objekt ohne Beschreibung (1.165 ha, 2008); beide Parks einzeln vorhanden'}
# Wikidata-Objekt -> VDN-Seite (Namen weichen ab)
ZU_VDN = {'Q883865': 'naturpark-bergstrasse-odenwald', 'Q1970537': 'geo-naturpark-frau-holle-land',
          'Q1970695': 'natur-und-sternenpark-westhavelland', 'Q1969869': 'natur-und-geopark-terra-vita',
          'Q896254': 'naturpark-spessart', 'Q874609': 'naturpark-fraenkische-schweiz-frankenjura',
          'Q478200': 'naturpark-flaemingsachsen-anhalt', 'Q1970499': 'naturpark-harz-sachsen-anhaltmansfelder-land',
          'Q1970503': 'naturpark-harzsachsen-anhalt', 'Q72973': 'naturpark-solling-vogler-im-weserbergland',
          'Q1970692': 'naturpark-weserbergland', 'Q115597434': 'deutsch-belgischer-naturpark-hohes-venn-eifel',
          'Q1970426': 'arnsberger-wald', 'Q1170784': 'naturpark-thueringer-schiefergebirge-obere-saale',
          'Q779899': 'naturpark-teutoburger-waldeggegebirge', 'Q1714728': 'naturpark-nossentiner-schwinzer-heide',
          'Q1970481': 'naturpark-erzgebirgevogtland', 'Q884467': 'naturpark-schwarzwald-mittenord',
          'Q115596723': 'naturpark-bourtanger-moor-bargerveen', 'Q883875': 'naturpark-augsburg-westliche-waelder'}
# Flächen, deren Einheit/Dezimalzeichen in Wikidata offensichtlich falsch ist (Plausibilität: 20–5.000 km²)
FL_FIX = {'Q1970481': (1495, '1.495 km² (Tausenderpunkt als Dezimalpunkt eingetragen)'),
          'Q1970695': (1315, '1.315 km² (Tausenderpunkt als Dezimalpunkt eingetragen)'),
          'Q1698580': (593.75, '59.375 mit Einheit km² eingetragen, gemeint ha'),
          'Q1970519': (874.32, '87.432 mit Einheit km² eingetragen, gemeint ha'),
          'Q1970670': (None, '114,86 mit Einheit m² eingetragen – nicht sicher deutbar, weggelassen')}


def norm(s):
    s = unicodedata.normalize('NFKD', s.lower()).encode('ascii', 'ignore').decode()
    s = re.sub(r'\b(naturpark|geo|natur und|internationaler|deutsch-belgischer)\b', ' ', s)
    return re.sub(r'[^a-z]', '', s)


VNORM = {norm(n): s for s, n in VDN.items()}
VNORM.update({norm(s.replace('-', ' ')): s for s in VDN})

daten, weg, aufgeloest, fl_korr, warn, ohne = [], [], [], [], [], []
benutzt = collections.Counter()
for q, x in sorted(it.items(), key=lambda a: a[1]['n'] or ''):
    if q in NICHT: weg.append((q, x['n'], NICHT[q])); continue
    if 'DE' not in x['k']: weg.append((q, x['n'], 'nicht in Klasse Q20354035, ungeprüft')); continue
    if x['a']: aufgeloest.append((q, x['n'], sorted(x['a'])[0])); continue
    slug = ZU_VDN.get(q) or VNORM.get(norm(x['n']))
    if slug: benutzt[slug] += 1
    # Fläche in km²
    fl = None
    if x['f']:
        w, e = sorted(x['f'])[0]
        fl = w / 100 if e == 'Q35852' else (w if e == 'Q712226' else w / 1e6)
    if q in FL_FIX:
        fl_korr.append((q, x['n'], fl, FL_FIX[q][0], FL_FIX[q][1])); fl = FL_FIX[q][0]
    if fl is not None and not (20 <= fl <= 5000): warn.append((q, x['n'], f'Fläche {fl} km² unplausibel'))
    c = x['c'][0] if x['c'] else None
    land = None
    if c:
        land, innen = geo.bundesland(c[0], c[1], 0.15)
        if not innen: warn.append((q, x['n'], f'Punkt nicht in einem Bundesland ({c}), nächstes {land}'))
        vl = VDN_LAND.get(slug, [])
        if vl and land not in vl: warn.append((q, x['n'], f'Punkt in {land}, VDN führt {vl}'))
    else:
        ohne.append((q, x['n']))
    laender = sorted(set(VDN_LAND.get(slug, [])) | ({land} if land else set()))
    e = {'n': x['n'], 'land': land, 'laender': laender, 'km2': round(fl) if fl and fl >= 100 else (round(fl, 1) if fl else None),
         'jahr': min(x['g']) if x['g'] else None, 'lon': round(c[0], 2) if c else None, 'lat': round(c[1], 2) if c else None,
         'wd': q, 'vdn': bool(slug)}
    daten.append(e)

vdn_fehlt = [(s, VDN[s]) for s in VDN if not benutzt[s]]
doppelt = [s for s, n in benutzt.items() if n > 1]
bericht = {'weg': weg, 'aufgeloest': aufgeloest, 'fl_korr': fl_korr, 'warn': warn, 'ohne_lage': ohne,
           'vdn_fehlt_in_wikidata': vdn_fehlt, 'vdn_doppelt': doppelt,
           'nicht_vdn': [(e['wd'], e['n']) for e in daten if not e['vdn']]}
json.dump(bericht, open('roh/naturparks_bericht.json', 'w'), ensure_ascii=False, indent=1)

kopf = {
    'id': 'naturparks', 'name': 'Naturparks in Deutschland', 'gruppe': 'Deutschland', 'typ': 'punkte', 'einheit': 'km²',
    'legende': [['Naturpark', '#8ad06a'], ['Naturpark (nicht in der VDN-Liste)', '#b8d0a0']],
    'quellen': [{'t': 'Wikidata: Objekte der Klasse „Naturpark in Deutschland“ (Q20354035) – Name, Koordinate (P625), Fläche (P2046), '
                      'Gründung (P571), Auflösung (P576); SPARQL-Abfrage', 'u': 'https://query.wikidata.org/', 'stand': STAND, 'lizenz': 'CC0 1.0'},
                {'t': 'Verband Deutscher Naturparke (VDN): Naturparke in Deutschland (Liste, 104 Naturparke, Zuordnung zu Bundesländern) – nur Abgleich der Zahl, Namen und Länder',
                 'u': 'https://naturparke.de/naturparke/', 'stand': 'abgerufen ' + STAND, 'lizenz': 'nur Fakten (Namen, Anzahl) übernommen'},
                {'t': 'Bundesländer-Umrisse der App (welt_basis.json, bl) für das Land des Lagepunkts', 'u': 'welt_basis.json',
                 'stand': 'App-Stand', 'lizenz': 'wie welt_basis.json'}],
    'hinweis': ('Lagepunkt laut Wikidata (ein Punkt im oder am Gebiet, oft Mitte oder Verwaltungssitz-Nähe), keine Gebietsgrenze. '
                '`land` = Bundesland des Lagepunkts; `laender` = zusätzlich die Länder, unter denen der VDN den Park führt. '
                'Fläche laut Wikidata in km² (gerundet; bei grenzüberschreitenden Parks je nach Objekt nur der deutsche Teil), '
                'fünf offensichtliche Einheitenfehler berichtigt bzw. weggelassen (pruef.md). Jahr = Gründung laut Wikidata. '
                'Aufgelöste bzw. zusammengelegte Parks (Ebbegebirge, Homert, Rothaargebirge → Sauerland-Rothaargebirge 2015; '
                'Mecklenburgisches Elbetal 2015) nicht enthalten. `vdn:false` = nicht in der VDN-Liste (z. B. Pfälzerwald). '
                f'{len(daten)} Parks; VDN nennt 104 (Abgleich pruef.md).'),
    'felder': {'n': 'Name', 'land': 'Bundesland des Lagepunkts', 'laender': 'beteiligte Bundesländer (VDN + Lagepunkt)',
               'km2': 'Fläche km²', 'jahr': 'Gründungsjahr', 'lon': 'Länge', 'lat': 'Breite', 'wd': 'Wikidata', 'vdn': 'in VDN-Liste'},
}
o = dict(kopf); o['daten'] = daten
json.dump(o, open('naturparks.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('Parks', len(daten), 'davon VDN', sum(e['vdn'] for e in daten), 'ohne Lage', len(ohne), 'ohne Fläche',
      sum(1 for e in daten if e['km2'] is None), 'ohne Jahr', sum(1 for e in daten if not e['jahr']))
print(json.dumps({k: v for k, v in bericht.items() if k != 'weg'}, ensure_ascii=False, indent=0))
