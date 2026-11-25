"""Ebene 'welterbe': Zahl der UNESCO-Welterbestätten je Land (Kultur/Natur/gemischt) aus dem CIA World Factbook (gemeinfrei).
Einzelstätten mit Lage werden NICHT geliefert: die UNESCO-Daten dürfen nur mit vorheriger schriftlicher Erlaubnis
weiterveröffentlicht werden (whc.unesco.org/en/faq/126)."""
import json, glob, re, sys, html
sys.path.insert(0, '/home/claude/scratch/themen/b/prep')
from gemein import *

daten, fehl = {}, []
for f in sorted(glob.glob(ROH + '/fb/repo/*/*.json')):
    code = f.split('/')[-1][:-5].upper(); c = FIPS.get(code)
    if not c or c not in APP: continue
    nh = json.load(open(f)).get('Government', {}).get('National heritage', {})
    t = nh.get('total World Heritage Sites', {}).get('text', '')
    if not t: continue
    t = html.unescape(t)
    m = re.match(r'\s*(\d+)', t)
    if not m: fehl.append((c, t)); continue
    e = {'n': int(m.group(1))}
    for k, rx in (('k', r'(\d+)\s*cultural'), ('nat', r'(\d+)\s*natural'), ('gem', r'(\d+)\s*mixed')):
        mm = re.search(rx, t)
        if mm: e[k] = int(mm.group(1))
    if sum(e.get(k, 0) for k in ('k', 'nat', 'gem')) not in (0, e['n']): fehl.append((c, 'Summe? ' + t))
    if c in daten: daten[c]['n'] += e['n']; continue
    daten[c] = e
# --- Gegenprüfung 25.11.2026 ---
# 1) Abgleich mit UNESCO „States Parties – statistics“ (Stand nach der 47. Sitzung 2025): abweichende Zahlen der Vertragsstaaten
#    werden auf den UNESCO-Wert gesetzt (Aufteilung Kultur/Natur dann entfernt, weil nicht belegt).
#    Gebiete mit eigener Fläche in der App (GRL, PYF, NCL, PRI, CUW, BMU, HMD, XKX) behalten ihre Factbook-Zahl (Lage-Prinzip).
UST = json.load(open(ROH + '/unesco_welterbe_stat_vor2026.json'))
korr = []
for c, v in UST.items():
    if c not in APP: continue
    if c in daten and daten[c]['n'] == v: continue
    if v == 0 and c not in daten: continue
    korr.append((c, daten.get(c, {}).get('n'), v)); daten[c] = {'n': v}
# 2) Neueintragungen der 48. Sitzung (Busan, 19.–29.07.2026), 25 Stätten (Time Out 27.07.2026; UN News 07/2026; KMK)
NEU26 = {'k': 'FIN IRN BRA IND JPN FRA FRA POL CHN LBN KAZ PSE UZB MNG COM STP ITA TUN THA', 'nat': 'JOR SSD USA DNK ARE', 'gem': 'GRC'}
for art, l in NEU26.items():
    for c in l.split():
        e = daten.setdefault(c, {'n': 0})
        e['n'] += 1
        if art in e or not any(k in e for k in ('k', 'nat', 'gem')) and e['n'] == 1: e[art] = e.get(art, 0) + 1
        elif any(k in e for k in ('k', 'nat', 'gem')): e[art] = e.get(art, 0) + 1
for c, e in daten.items():
    if any(k in e for k in ('k', 'nat', 'gem')) and sum(e.get(k, 0) for k in ('k', 'nat', 'gem')) != e['n']:
        for k in ('k', 'nat', 'gem'): e.pop(k, None)
print('korrigiert nach UNESCO:', korr)
print(len(daten), 'Länder; Summe Stätten (mit Mehrfachzählung grenzüberschreitender):', sum(d['n'] for d in daten.values()))
print(fehl)
for c in ('DEU', 'ITA', 'CHN', 'FRA', 'ESP', 'IND', 'MEX', 'USA', 'RUS'): print(c, daten.get(c))
obj = {'id': 'welterbe', 'name': 'UNESCO-Welterbe je Land', 'gruppe': 'Geschichte', 'typ': 'land-wert', 'einheit': 'Welterbestätten',
       'legende': {'min': 0, 'max': max(d['n'] for d in daten.values()), 'stufen': ['0', '10', '30', '60']},
       'quellen': [{'t': 'CIA World Factbook, Feld „National heritage – total World Heritage Sites“, letzte Ausgabe (Archiv factbook/factbook.json); Zahlen der Vertragsstaaten gegengeprüft mit UNESCO „States Parties – statistics“ und um die 25 Neueintragungen der 48. Sitzung (Juli 2026) ergänzt',
                    'u': 'https://github.com/factbook/factbook.json', 'stand': 'Welterbeliste nach der 48. Sitzung des Komitees (Busan, Juli 2026; 1.273 Stätten)',
                    'lizenz': 'gemeinfrei (Werk der US-Regierung); Einzelkorrekturen als Fakten'},
                   {'t': 'UNESCO World Heritage Centre, States Parties – statistics (Gegenprüfung, Stand nach der 47. Sitzung); KMK „Welterbe“ (Deutschland 55, 2026 nur Erweiterung „Siedlungen der Berliner Moderne“); Time Out 27.07.2026 und UN News 07/2026 (Neueintragungen 2026)',
                    'u': 'https://whc.unesco.org/en/statesparties/stat', 'stand': '11/2026', 'lizenz': 'nur als Beleg zitiert'}],
       'hinweis': 'Nur Anzahl je Land (Kultur/Natur/gemischt, wo belegt). Grenzüberschreitende Stätten zählen bei jedem beteiligten Land. Stand nach der 48. Sitzung (Juli 2026). '
                  'Staaten: Zahl laut UNESCO je Vertragsstaat (einschließlich Überseegebieten); Gebiete mit eigener Fläche in der Karte (z. B. Grönland, Französisch-Polynesien, Bermuda, Kosovo) zeigen zusätzlich die dort gelegenen Stätten. '
                  'Die Stätte „Mittelalterliche Denkmäler im Kosovo“ führt die UNESCO unter Serbien; sie liegt im Kosovo. Einzelne Stätten mit Lage: siehe OFFEN.md (UNESCO-Nutzungsbedingungen).',
       'felder': {'n': 'Zahl gesamt', 'k': 'Kultur', 'nat': 'Natur', 'gem': 'gemischt'}, 'daten': daten}
schreibe(obj)
