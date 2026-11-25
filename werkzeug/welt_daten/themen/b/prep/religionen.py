"""Ebene 'religionen': größte Religionsgruppe und Anteile je Land aus dem CIA World Factbook (letzte Ausgabe, gemeinfrei)."""
import json, glob, re, sys, collections, html
sys.path.insert(0, '/home/claude/scratch/themen/b/prep')
from gemein import *

GRUPPEN = [  # Reihenfolge = Vorrang bei der Zuordnung eines Teilstücks
    ('and', r'no response|refused|don.t know|not applicable|no answer|objected|believer \(not|^\s*believer'),
    ('kein', r'nothing in particular|non-?believer|humanist|\bnone\b|unaffiliated|no religion|atheis|agnostic|non-?religious|nonbeliever|irreligi|without religion|secular'),
    ('jud', r'jew|juda'),
    ('mus', r'bektashi|musl|islam|sunni|shia|shi\'a|ibadhi|ahmadi'),
    ('hin', r'hindu'),
    ('bud', r'buddh|lamais|theravada|mahayana'),
    ('chr', r'christ|cathol|protest|orthodox|anglican|evangel|pentecost|luther|method|baptist|adventist|jehovah|mormon|latter-day|presbyter|reformed|coptic|apostolic|church|kimbangu|zionist|calvin|episcop|congregation|moravian|mennonit|uniting|salvation army|gregorian|armenian|maronite|melkite|uniate|greek|nazarene|brethren|quaker|unitarian|salutist|zion|assembly of god|kingdom of god|\bmana\b|ekalesia|latter day|worship centre|iglesia ni cristo|old believer'),
    ('volk', r'folk|traditional|animis|indigenous|ethnic relig|shinto|tao|confuc|vodou|voodoo|spiritis|chinese relig|cao dai|hoa hao|ancestor|african relig|syncretic|tribal|nature wor|shaman|tengri|candombl|umbanda|santer|rastaf|kirant|kirat|bon\b|badimo|customary|maori|modekngei|pagan|winti|spirtism|umbanda'),
    ('and', r'sikh|bahai|baha\'i|jain|zoroast|druze|yazid|other|mixed|unspecified|unknown|not stated|no answer|undeclared|did not'),
]
NAME = {'chr': 'Christentum', 'mus': 'Islam', 'hin': 'Hinduismus', 'bud': 'Buddhismus', 'jud': 'Judentum',
        'volk': 'Volks- und traditionelle Religionen (inkl. Shinto, Daoismus)', 'kein': 'Ohne Religionszugehörigkeit',
        'and': 'Andere / ohne Angabe'}
FARBE = {'chr': '#6aa8e8', 'mus': '#5ac87a', 'hin': '#ff9a4a', 'bud': '#e8d05a', 'jud': '#9a8aff',
         'volk': '#d87ab0', 'kein': '#8a96a8', 'and': '#5a6070'}


def gruppe(s):
    s = s.lower()
    for k, rx in GRUPPEN:
        if re.search(rx, s): return k
    return None


def ohne_klammern(t):
    while True:
        n = re.sub(r'\([^()]*\)', '', t)
        if n == t: return t
        t = n


daten, probleme = {}, []
for f in sorted(glob.glob(ROH + '/fb/repo/*/*.json')):
    code = f.split('/')[-1][:-5].upper(); c = FIPS.get(code)
    if not c or c not in APP: continue
    d = json.load(open(f))
    t = d.get('People and Society', {}).get('Religions', {}).get('text', '')
    if not t: continue
    t = html.unescape(t).replace('\xa0', ' ')
    segs = [x for x in re.split(r'<br\s*/?>\s*(?:<br\s*/?>)?', t) if x.strip()]
    mitjahr = [x for x in segs if re.search(r'\d{4}', x)]
    t = (mitjahr[-1] if mitjahr else segs[0]) if segs else ''
    t = re.sub(r'<[^>]+>', ' ', t)
    jahr = re.search(r'\((?:[^()]*?)(\d{4})(?:[^()]*?)est\.?\)', t) or re.search(r'\((\d{4})\)', t)
    haupt = re.split(r';\s*note|<strong>note', t)[0]
    m = re.search(r'\([^()]*\d{4}[^()]*\)', haupt)
    if m: haupt = haupt[:m.start()]
    flach = ohne_klammern(haupt)
    teile = re.findall(r'([^,;%]+?)\s*(about\s+|approximately\s+|less than\s+|<\s*)?([\d.]+(?:-[\d.]+)?)\s*%', flach)
    ant = collections.defaultdict(float)
    spanne = {}
    for name, kl, p in teile:
        if kl.strip() in ('<', 'less than'): continue  # „unter 0,1 %“ wird nicht gezählt
        g = gruppe(name)
        if '-' in p:
            lo, hi = p.split('-'); v = float(lo)
            spanne[g or 'and'] = f'{lo}–{hi}'
        else:
            try: v = float(p.rstrip('.'))
            except ValueError: continue
        if g is None: probleme.append((c, name.strip())); g = 'and'
        ant[g] += v
    e = {'j': int(jahr.group(1)) if jahr else None}
    if ant:
        summe = sum(ant.values())
        if summe > 103: probleme.append((c, f'Summe {summe:.0f}%: ' + flach[:90]))
        e['a'] = {k: round(v, 1) for k, v in sorted(ant.items(), key=lambda kv: -kv[1]) if v >= 0.1}
        kand = {k: v for k, v in ant.items() if k != 'and'} or ant
        e['g'] = max(kand, key=kand.get)
        if spanne: e['sp'] = spanne
    else:  # nur Aufzählung ohne Zahlen: erste erkannte Gruppe, ohne Anteil
        for s in re.split(r',', flach):
            g = gruppe(s)
            if g and g != 'and': e['g'] = g; e['ohne_zahl'] = 1; break
    e['t'] = haupt.strip()[:220]  # Originalangabe (englisch) zur Nachprüfung
    if 'g' in e: daten[c] = e
    else: probleme.append((c, 'keine Gruppe: ' + haupt[:80]))

print('Länder', len(daten)); print('Probleme', len(probleme))
for p in probleme[:60]: print(' ', p)
for c in ('DEU', 'USA', 'IND', 'CHN', 'JPN', 'NGA', 'ISR', 'LBN', 'KOR', 'CZE', 'VNM', 'BIH', 'FRA', 'NLD'):
    print(c, {k: v for k, v in daten.get(c, {}).items() if k != 't'})
kat = collections.Counter(e['g'] for e in daten.values())
print(kat)
for e in daten.values(): e.pop('t', None)
obj = {'id': 'religionen', 'name': 'Religionen', 'gruppe': 'Menschen', 'typ': 'land-kat', 'einheit': '% der Bevölkerung',
       'legende': [{'k': k, 'n': NAME[k], 'c': FARBE[k], 'z': kat.get(k, 0)} for k in NAME if kat.get(k)],
       'quellen': [{'t': 'CIA World Factbook, Feld „Religions“, letzte Ausgabe (Archiv factbook/factbook.json)',
                    'u': 'https://github.com/factbook/factbook.json', 'stand': 'Ausgabe 02/2026 (eingestellt); Schätzjahr je Land in „j“',
                    'lizenz': 'gemeinfrei (Werk der US-Regierung); Archiv CC0'}],
       'hinweis': 'Anteile wie im Factbook angegeben (Selbstauskunft/Zensus/Schätzung, Jahr je Land verschieden); '
                  'Untergruppen sind zusammengefasst. Größte Gruppe ohne „Andere/ohne Angabe“. '
                  'Wo das Factbook keine Prozentzahlen nennt, steht nur die erstgenannte Gruppe (ohne_zahl).',
       'felder': {'g': 'größte Gruppe (Kategorie)', 'a': 'Anteile je Gruppe in %', 'j': 'Schätz-/Erhebungsjahr',
                  'ohne_zahl': '1 = keine Prozentangabe in der Quelle', 'sp': 'Spanne laut Quelle (in „a“ steht der untere Wert)'},
       'gruppen': NAME, 'daten': daten}
schreibe(obj)
