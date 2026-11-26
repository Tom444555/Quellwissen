"""Welterbestätten mit Lage aus Wikidata (CC0) -> welterbe_staetten.json
Eingaben (Abfragen *.rq, abgerufen mit sparql.sh): roh/welterbe.json (q_welterbe.rq), roh/welterbe_land.json
(q_welterbe_land.rq), roh/welterbe_name.json (q_welterbe_name.rq), roh/ende.json (q_ende.rq).
Aufruf: cd /home/claude/scratch/wikidata && python3 -I welterbe_staetten.py [mehrfach]"""
import json, re, sys, collections
sys.path.insert(0, '/home/claude/scratch/wikidata')
import geo

STAND = '26.11.2026'
B = json.load(open('roh/welterbe.json'))['results']['bindings']
KRIT = {'Q23038972': 1, 'Q23038976': 2, 'Q23038977': 3, 'Q23038978': 4, 'Q23038979': 5, 'Q23038980': 6,
        'Q23038981': 7, 'Q23038983': 8, 'Q23038985': 9, 'Q23038986': 10}
# Nummern, die nicht mehr als eigene Stätte bestehen (Endedatum der Welterbe-Aussage in Wikidata, q_ende.rq):
WEG = {'654': 'gestrichen 2007 (Oman, Oryx-Schutzgebiet)', '1156': 'gestrichen 2009 (Dresdner Elbtal)',
       '1150': 'gestrichen 2021 (Liverpool)', '161': 'aufgegangen in 933 (Chambord -> Loiretal, 2000)',
       '133': 'aufgegangen in 304 (Burgess Shale -> Kanadische Rocky Mountains, 1984)',
       '790': 'aufgegangen in 1582 (Panamá Viejo -> Koloniale Transisthmus-Route, 2025; worldheritagesite.org/list/id/1582)',
       '291': 'aufgegangen in 275 (São Miguel das Missões -> Jesuitenmissionen der Guaraní, 1984)'}
# Staaten-Korrekturen: offensichtliche Wikidata-Fehler bzw. strittige Gebiete wie in b/welterbe.json (UNESCO-Zuordnung)
ISO_SETZ = {'100': (['MNE'], 'Durmitor: Wikidata-P17 nennt zusätzlich BIH (Tara-Schlucht-Objekt)'),
            '999': (['BRA'], 'Pantanal-Schutzgebiet liegt nur in Brasilien'),
            '588': (['ROU'], 'Donaudelta-Welterbe nur rumänischer Teil'),
            '1411': (['UKR'], 'Chersones: UNESCO-Vertragsstaat Ukraine (Wikidata nennt auch RUS)'),
            '1660': (['DNK'], 'Wikingerzeitliche Ringburgen: nur Dänemark (schwedisches Trelleborg-Objekt trägt fälschlich die Nummer)'),
            '148': ([], 'Altstadt von Jerusalem: UNESCO führt die Stätte ohne Vertragsstaat (Vorschlag Jordaniens)')}
# Hauptobjekt von Hand, wo Wikidata mehrere Objekte mit derselben Nummer ohne Suffix führt und die Rangregel
# ein Einzelobjekt statt der Gesamtstätte wählt
HAUPT_SETZ = {'933': 'Q2789507', '1468': 'Q128009257', '797': 'Q3678423', '1401': 'Q65926560', '1087': 'Q15238169'}
# Stätten ohne Koordinate in Wikidata: Lage eines Bestandteils (P527 des Hauptobjekts, q_lage_nach.rq)
LAGE_SETZ = {'509': 'Q43278', '946': 'Q188528', '1567': 'Q705054', '1752': 'Q368706', '1755': 'Q79501011',
             '1759': 'Q4822100', '1760': 'Q25490231', '1762': 'Q592228'}
_LN = {}
for b in json.load(open('roh/lage_nach.json'))['results']['bindings']:
    m = re.match(r'Point\(([-\d.eE]+) ([-\d.eE]+)\)', b['coord']['value'])
    _LN.setdefault(b['o']['value'].rsplit('/', 1)[1], (float(m[1]), float(m[2]), b.get('ol', {}).get('value')))
NAME_SETZ = {'322': 'Ruinen des buddhistischen Vihara in Paharpur', '502': 'Historische Stadt Vigan',
             '1269': 'Heilige Stadt Caral-Supe', '739': 'Schokland und Umgebung', '231': 'Rotes Fort (Delhi)', '251': 'Rotes Fort (Agra)'}

it = collections.defaultdict(lambda: {'ids': set(), 'de': None, 'en': None, 'xx': None, 'c': [], 'iso': set(),
                                      'k': set(), 'start': set(), 'p31': set()})
for b in B:
    q = b['i']['value'].rsplit('/', 1)[1]
    x = it[q]
    x['ids'].add(b['id']['value'])
    if 'de' in b: x['de'] = b['de']['value']
    if 'en' in b: x['en'] = b['en']['value']
    if 'coord' in b:
        m = re.match(r'Point\(([-\d.eE]+) ([-\d.eE]+)\)', b['coord']['value'])
        if m and (float(m[1]), float(m[2])) not in x['c']: x['c'].append((float(m[1]), float(m[2])))
    if 'krit' in b:
        k = b['krit']['value'].rsplit('/', 1)[1]
        if k in KRIT: x['k'].add(KRIT[k])
    if 'start' in b and b['start']['value'][:4].isdigit() and int(b['start']['value'][:4]) >= 1978:
        x['start'].add(int(b['start']['value'][:4]))
    if 'typ' in b: x['p31'].add(b['typ']['value'].rsplit('/', 1)[1])
Q = set(it)
ISO_FIX = {'Q55': 'NLD'}   # Niederlande trägt in Wikidata kein P298
for b in json.load(open('roh/welterbe_land.json'))['results']['bindings']:
    q = b['i']['value'].rsplit('/', 1)[1]; c = b['c']['value'].rsplit('/', 1)[1]
    iso = ISO_FIX.get(c) or b.get('iso', {}).get('value')
    if q not in Q or iso in (None, 'DDR', 'SUN'): continue   # historische Staaten weglassen
    it[q]['iso'].add({'XKS': 'XKX'}.get(iso, iso))
for b in json.load(open('roh/welterbe_name.json'))['results']['bindings']:
    q = b['i']['value'].rsplit('/', 1)[1]
    if q in Q: it[q]['xx'] = b['lab']['value']


def basis(i):
    m = re.match(r'(\d+)', i)
    return str(int(m[1])) if m else None   # führende Null (091 -> 91)


grp = collections.defaultdict(lambda: {'haupt': set(), 'teile': set()})
for q, x in it.items():
    for i in x['ids']:
        bn = basis(i)
        if bn is None: continue
        # Hauptobjekt: Kennung ohne Teil-Suffix ("-001", ".594")
        (grp[bn]['haupt'] if re.fullmatch(r'\d+[a-z]*', i) else grp[bn]['teile']).add(q)


def rang(q):
    x = it[q]
    return (bool(x['k']), ('Q9259' in x['p31']), len(x['ids']), bool(x['start']), bool(x['c']), -int(q[1:]))


def name(x, fremd=False):
    return x['de'] or x['en'] or (x['xx'] if fremd else None)


lage_nach = []
daten, ohne_lage, warn, weg, iso_plus, iso_lage, korr = [], [], [], [], [], [], []
for bn in sorted(grp, key=int):
    g = grp[bn]
    if bn in WEG: weg.append((bn, WEG[bn])); continue
    haupt = sorted(g['haupt'], key=rang, reverse=True)
    teile = sorted(g['teile'] - g['haupt'], key=lambda q: int(q[1:]))
    hq = HAUPT_SETZ.get(bn) or (haupt[0] if haupt else teile[0])
    h = it[hq]
    alle = haupt + teile
    lage = h['c'][0] if h['c'] else next((it[q]['c'][0] for q in alle if it[q]['c']), None)
    lage_teil = None
    if not lage and bn in LAGE_SETZ:
        x0 = _LN[LAGE_SETZ[bn]]; lage = x0[:2]; lage_teil = f'{LAGE_SETZ[bn]} {x0[2]}'; lage_nach.append((bn, lage_teil))
    # Staaten: Hauptobjekt; weitere Staaten aus anderen Objekten derselben Nummer nur, wenn deren Lage im Staat liegt
    iso = set(h['iso'])
    for q in alle:
        if q == hq: continue
        for c in it[q]['c'][:1]:
            if lage and abs(c[0] - lage[0]) + abs(c[1] - lage[1]) > 10: continue   # falsch zugeordnete Objekte (z. B. 102, 736)
            l, innen = geo.land(c[0], c[1], 0.3)
            for s in it[q]['iso']:
                if s == l and s not in iso: iso.add(s); iso_plus.append((bn, s, q))
    if not iso and lage:
        l, _ = geo.land(lage[0], lage[1], 1.0)
        if l: iso = {l}; iso_lage.append((bn, l))
    if bn in ISO_SETZ:
        korr.append((bn, sorted(iso), ISO_SETZ[bn][0], ISO_SETZ[bn][1])); iso = set(ISO_SETZ[bn][0])
    k = set(h['k']) or set().union(*[it[q]['k'] for q in haupt]) or set().union(*[it[q]['k'] for q in teile])
    art = None
    if k:
        kul, nat = any(c <= 6 for c in k), any(c >= 7 for c in k)
        art = 'gemischt' if kul and nat else ('Kultur' if kul else 'Natur')
    jahre = h['start'] or set().union(*[it[q]['start'] for q in haupt])
    jahr = min(jahre) if jahre else None
    nm = NAME_SETZ.get(bn) or name(h) or next((name(it[q]) for q in alle if name(it[q])), None) or name(h, True)
    e = {'n': nm, 'id': int(bn), 'art': art, 'jahr': jahr, 'iso3': sorted(iso), 'teile': len(teile),
         'lon': round(lage[0], 2) if lage else None, 'lat': round(lage[1], 2) if lage else None, 'wd': hq}
    if lage_teil: e['lage'] = 'Bestandteil'
    if not lage: ohne_lage.append((bn, nm))
    else:
        l, innen = geo.land(lage[0], lage[1], 1.0)
        if iso and l not in iso: warn.append((bn, nm, sorted(iso), l, innen, e['lon'], e['lat']))
    daten.append(e)

json.dump({'ohne_lage': ohne_lage, 'warn': warn, 'weg': weg, 'iso_plus': iso_plus, 'iso_lage': iso_lage, 'korr': korr, 'lage_nach': lage_nach},
          open('roh/welterbe_bericht.json', 'w'), ensure_ascii=False, indent=0)

if __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == 'mehrfach':
    for bn in sorted(grp, key=int):
        h = sorted(grp[bn]['haupt'], key=rang, reverse=True)
        if len(h) > 1: print(bn, '->', h[0], [(q, name(it[q], True)) for q in h])
    sys.exit()

ac = collections.Counter(e['art'] for e in daten)
kopf = {
    'id': 'welterbe_staetten', 'name': 'Welterbestätten (Lage)', 'gruppe': 'Geschichte', 'typ': 'punkte', 'einheit': '',
    'legende': [['Kultur', '#e8a04a'], ['Natur', '#4ad07a'], ['gemischt', '#5ab8e8'], ['Art offen', '#c8c8c8']],
    'quellen': [{'t': 'Wikidata: Objekte mit Welterbe-Kennung (P757), Koordinate (P625), Staat (P17 -> ISO 3166-1 alpha-3 P298), '
                      'Welterbe-Kriterien (P2614), Eintragungsjahr (P1435 = Welterbe, Qualifikator Startzeit P580); SPARQL-Abfrage',
                 'u': 'https://query.wikidata.org/', 'stand': STAND, 'lizenz': 'CC0 1.0'},
                {'t': 'Gesamtzahl 1.273 Stätten nach der 48. Sitzung (Juli 2026) – Abgleich wie in welterbe.json (Länderzählung)',
                 'u': 'https://whc.unesco.org/en/list/', 'stand': '07/2026', 'lizenz': 'nur Zahl als Beleg, keine UNESCO-Daten übernommen'}],
    'hinweis': ('Ein Punkt je Welterbe-Nummer (Lage des Hauptobjekts in Wikidata, sonst eines Teilobjekts); bei seriellen und '
                'grenzüberschreitenden Stätten ist der Punkt nur ein Teil der Stätte, `teile` = Zahl der Teilobjekte in Wikidata '
                '(nicht die amtliche Zahl der Bestandteile); `lage:\'Bestandteil\'` = Hauptobjekt ohne Koordinate, Punkt eines Bestandteils (Wikidata P527). Art aus den Kriterien (i–vi Kultur, vii–x Natur, beides gemischt). '
                'Staaten laut Wikidata; Jerusalem ohne Staat und Chersones unter Ukraine wie bei der UNESCO; Kosovo-Denkmäler '
                'laut Wikidata unter Serbien. Gestrichene Stätten (Dresden, Liverpool, Oman) nicht enthalten. ' +
                (f'{len(daten)} Stätten (= 1.273 nach der 48. Sitzung); ' if len(daten) == 1273 else f'{len(daten)} Stätten statt 1.273; ') +
                'Abweichungen, Korrekturen und Lücken siehe pruef.md. Daten aus Wikidata (CC0), '
                'keine Übernahme aus der UNESCO-Datenbank.'),
    'felder': {'n': 'Name (deutsch, sonst englisch)', 'id': 'Welterbe-Nummer (ohne bis/ter/rev)', 'art': 'Kultur|Natur|gemischt|null',
               'jahr': 'Eintragungsjahr laut Wikidata', 'iso3': 'Staaten', 'teile': 'Teilobjekte in Wikidata',
               'lon': 'Länge', 'lat': 'Breite', 'wd': 'Wikidata-Objekt', 'lage': 'nur gesetzt, wenn Punkt eines Bestandteils'},
    'zahlen': {'staetten': len(daten), 'kultur': ac['Kultur'], 'natur': ac['Natur'], 'gemischt': ac['gemischt'], 'art_offen': ac[None],
               'ohne_lage': len(ohne_lage)},
}
o = dict(kopf); o['daten'] = daten
json.dump(o, open('welterbe_staetten.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('Stätten', len(daten), 'Art', dict(ac), 'ohne Lage', len(ohne_lage), 'Warnungen', len(warn))
print('Jahr fehlt', sum(1 for e in daten if not e['jahr']), 'Staat fehlt', [e['id'] for e in daten if not e['iso3']])
print('Jahre', {y: sum(1 for e in daten if e['jahr'] == y) for y in (2023, 2024, 2025, 2026)})
