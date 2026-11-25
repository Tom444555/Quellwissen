"""Ebene 'sprachen': Amtssprachen (CLDR) + Sprachfamilie der meistgesprochenen Sprache (Glottolog 5.4)."""
import csv, sys, collections
from babel.core import get_global, get_cldr_version
from babel import Locale
import pycountry
sys.path.insert(0, '/home/claude/scratch/themen/b/prep')
from gemein import *

csv.field_size_limit(10**9)
G = ROH + '/glotto/'
name, iso3g = {}, {}
for r in csv.DictReader(open(G + 'languages.csv')):
    name[r['ID']] = r['Name']
    if r['ISO639P3code']: iso3g[r['ISO639P3code']] = r['ID']
klass = {}
for r in csv.DictReader(open(G + 'values.csv')):
    if r['Parameter_ID'] == 'classification': klass[r['Language_ID']] = r['Value'].split('/')

FAM_DE = {'indo1319': 'Indogermanisch', 'afro1255': 'Afroasiatisch', 'sino1245': 'Sinotibetisch',
          'atla1278': 'Atlantik-Kongo (Niger-Kongo)', 'aust1307': 'Austronesisch', 'turk1311': 'Turksprachen',
          'ural1272': 'Uralisch', 'drav1251': 'Dravidisch', 'japo1237': 'Japonisch', 'kore1284': 'Koreanisch',
          'taik1256': 'Tai-Kadai', 'aust1305': 'Austroasiatisch', 'kart1248': 'Kartwelisch',
          'mong1329': 'Mongolisch', 'nucl1709': 'Papua (Trans-Neuguinea)', 'nilo1247': 'Nilotisch',
          'cent2225': 'Zentralsudanisch', 'mand1469': 'Mande', 'quec1387': 'Quechua', 'tupi1275': 'Tupí',
          'ayma1253': 'Aymara', 'pidg1258': 'Pidgin', 'basq1248': 'Isoliert (Baskisch)',
          'east2328': 'Ostsudanisch', 'nort2843': 'Nordwestkaukasisch', 'nakh1245': 'Nachisch-Dagestanisch',
          'khoe1240': 'Khoe-Kwadi', 'eski1264': 'Eskimo-Aleutisch', 'mong1349': 'Mongolisch', 'otom1299': 'Otomangue', 'maya1287': 'Maya', 'gong1255': 'Gong'}
ZWEIG_DE = {'germ1287': 'germanisch', 'ital1284': 'romanisch', 'balt1263': 'baltoslawisch', 'indo1320': 'indoiranisch',
            'gree1276': 'griechisch', 'alba1267': 'albanisch', 'arme1241': 'armenisch', 'celt1248': 'keltisch',
            'anat1257': 'anatolisch', 'toch1238': 'tocharisch'}
SLAW = 'slav1255'
de = Locale('de')


MACRO = {'ar': 'arb', 'fa': 'pes', 'zh': 'cmn', 'ms': 'zsm', 'sw': 'swh', 'et': 'ekk', 'az': 'azj', 'mg': 'plt',
         'gn': 'gug', 'uz': 'uzn', 'lv': 'lvs', 'sq': 'als', 'ne': 'npi', 'or': 'ory', 'om': 'gaz', 'ku': 'kmr',
         'ps': 'pbu', 'mn': 'khk', 'no': 'nob', 'qu': 'quz', 'ay': 'ayr', 'kr': 'knc', 'ff': 'fuf', 'kg': 'kng',
         'sc': 'src', 'ik': 'esk', 'iu': 'ike', 'cr': 'crk', 'oj': 'ojg', 'yi': 'ydd', 'kv': 'kpv', 'ak': 'twi', 'lah': 'pnb'}


def gcode(lang):
    base = lang.split('_')[0]
    base = MACRO.get(base, base)
    if len(base) == 2:
        l = pycountry.languages.get(alpha_2=base)
        base = l.alpha_3 if l else base
    return iso3g.get(base)


def fam(lang):
    g = gcode(lang)
    if not g: return None, None
    path = klass.get(g, [])
    if not path: return 'Isolierte Sprache', None
    f = path[0]
    if f == 'crea1234':
        return 'Kreolsprache', None
    zw = None
    if f == 'indo1319':
        for n in path[1:]:
            if n in ZWEIG_DE: zw = ZWEIG_DE[n]; break
        if zw == 'baltoslawisch' and SLAW in path: zw = 'slawisch'
        elif zw == 'baltoslawisch': zw = 'baltisch'
    return FAM_DE.get(f, name.get(f, f)), zw


def dname(lang):
    base = lang.split('_')[0]
    return de.languages.get(lang) or de.languages.get(base) or base


tl = get_global('territory_languages')
daten, fehlt = {}, []
for a2, langs in tl.items():
    c = A2.get(a2)
    if not c or c in daten: continue
    amt = [l for l, v in langs.items() if v.get('official_status') in ('official', 'de_facto_official')]
    if not langs: continue
    pp = lambda kv: kv[1].get('population_percent') or 0
    allg = max(langs.items(), key=pp)[0]
    amtl = [kv for kv in langs.items() if kv[1].get('official_status')]
    top = max(amtl, key=pp)[0] if amtl else allg
    f, zw = fam(top)
    if not f: fehlt.append((c, top))
    e = {'amt': [dname(l) for l in amt], 'top': dname(top), 'p': langs[top].get('population_percent'), 'fam': f}
    if zw: e['zw'] = zw
    if allg != top: e['allg'] = dname(allg); e['pa'] = langs[allg].get('population_percent')
    if not amt: e['amt'] = []
    daten[c] = e

# Korrekturen nach CIA World Factbook (letzte Ausgabe, gemeinfrei), wo CLDR landesweite Amtssprachen nur regional führt
KORR = {'ZAF': ['Zulu', 'Xhosa', 'Afrikaans', 'Nord-Sotho', 'Tswana', 'Englisch', 'Süd-Sotho', 'Tsonga', 'Swazi', 'Venda',
                'Süd-Ndebele', 'Südafrikanische Gebärdensprache'],
        'BOL': ['Spanisch', 'Quechua', 'Aymara', 'Guaraní', '(alle indigenen Sprachen)'],
        'IRQ': ['Arabisch', 'Kurdisch'],
        # Gegenprüfung 25.11.2026 (Stichprobe): CLDR führt Schweizerdeutsch statt Rätoromanisch, Yoruba als Amtssprache Nigerias, Arabisch in Israel als Amtssprache
        'CHE': ['Deutsch', 'Französisch', 'Italienisch', 'Rätoromanisch'], 'NGA': ['Englisch'], 'ISR': ['Hebräisch', 'Arabisch (Sonderstatus)']}
for c, l in KORR.items():
    daten[c]['amt'] = l; daten[c]['q'] = 'CIA World Factbook'
kat = collections.Counter(d['fam'] for d in daten.values())
print(kat.most_common()); print('ohne Familie:', fehlt)
print('Länder:', len(daten), 'App ohne Daten:', [c for c in APP if c not in daten])
for c in ('DEU', 'CHE', 'IND', 'PHL', 'NGA', 'BRA', 'BEL', 'ESP', 'CAN', 'ZAF', 'ETH', 'IRN', 'PAK'):
    print(c, daten.get(c))

FARBE = {'Indogermanisch': '#6aa8e8', 'Afroasiatisch': '#e8b04a', 'Sinotibetisch': '#e86a6a',
         'Atlantik-Kongo (Niger-Kongo)': '#7ac86a', 'Austronesisch': '#4ad0c8', 'Turksprachen': '#c87ad8',
         'Uralisch': '#a0d8ff', 'Dravidisch': '#ff9a6a', 'Japonisch': '#ff7ab0', 'Koreanisch': '#d88aa0',
         'Tai-Kadai': '#d8d86a', 'Austroasiatisch': '#a8c84a', 'Kartwelisch': '#b09070', 'Mongolisch': '#d0a0ff',
         'Kreolsprache': '#9aa8b8', 'Pidgin': '#9aa8b8'}
leg = [{'k': k, 'n': k, 'c': FARBE.get(k, '#8a8a8a'), 'z': n} for k, n in kat.most_common()]
obj = {'id': 'sprachen', 'name': 'Sprachen', 'gruppe': 'Menschen', 'typ': 'land-kat', 'einheit': '',
       'legende': leg,
       'quellen': [
           {'t': f'Unicode CLDR {get_cldr_version()} (Territory-Language Information, über Python-Paket babel {__import__("babel").__version__})',
            'u': 'https://github.com/unicode-org/cldr', 'stand': '2025 (CLDR 47)', 'lizenz': 'Unicode License v3 (frei, mit Namensnennung)'},
           {'t': 'Glottolog 5.4 (Hammarström, Forkel, Haspelmath, Bank), Sprachklassifikation',
            'u': 'https://github.com/glottolog/glottolog-cldf', 'stand': '11/2026', 'lizenz': 'CC BY 4.0'},
           {'t': 'CIA World Factbook, letzte Ausgabe (Archiv factbook/factbook.json) – nur Amtssprachen ZAF, BOL, IRQ, CHE, NGA, ISR',
            'u': 'https://github.com/factbook/factbook.json', 'stand': '02/2026 (eingestellt)', 'lizenz': 'gemeinfrei (US-Regierung)'}],
       'hinweis': 'Amtssprachen = Status „official“/„de facto official“ in CLDR (landesweit, ohne regionale). '
                  'Maßgebliche Sprache = die verbreitetste Sprache mit amtlichem Status (auch regional) nach CLDR-Sprecheranteil '
                  '(Erst- und Zweitsprache zusammen); ist eine andere Sprache insgesamt verbreiteter, steht sie zusätzlich unter „allg“. '
                  'Familie nach Glottolog; bei Indogermanisch zusätzlich der Zweig.',
       'felder': {'amt': 'Amtssprachen', 'top': 'verbreitetste Sprache mit Amtsstatus', 'p': 'Sprecheranteil in % (CLDR)', 'allg': 'insgesamt verbreitetste Sprache, falls abweichend', 'pa': 'deren Anteil in %',
                  'fam': 'Sprachfamilie (Kategorie)', 'zw': 'Zweig (nur Indogermanisch)'},
       'daten': daten}
schreibe(obj)
