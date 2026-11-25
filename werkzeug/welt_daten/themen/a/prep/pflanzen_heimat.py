"""Natürliche Heimat der App-Pflanzen nach WCVP (Kew, CC BY 4.0), Schnappschuss v16 (04.06.2026) aus GitHub matildabrown/rWCVPdata;
Botanische Länder (WGSRPD Stufe 3) → ISO3 über WGSRPD Stufe 4 (GitHub tdwg/wgsrpd). Aufruf: python3 -I prep/pflanzen_heimat.py
Rohauszug: roh/wcvp/verbreitung_auswahl.csv, verbreitung_extra.csv, namen_auswahl.csv, akzeptiert.csv, wgsrpd_l4.csv"""
import sys, os, csv, json, re, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gemein import ROH, schreibe
import pycountry

W = os.path.join(ROH, 'wcvp')
# App-Pflanzen
h = open('/home/claude/quellwissen/quelle/gruenwissen.html', encoding='utf-8').read()
P = json.loads(re.search(r'<script type="application/json" id="daten">(.*?)</script>', h, re.S).group(1))['pflanzen']
# Zuordnung App-ID → akzeptierte WCVP-Namen (plant_name_id)
ZU = {'p01': [2448560], 'p02': [2623499], 'p03': [2916959], 'p04': [2486519], 'p05': [2910167], 'p06': [2569834], 'p07': [2908230],
      'p08': [516286], 'p09': [2922622], 'p10': [2569743], 'p11': [2566490], 'p12': [2454940, 2453401, 2453334], 'p14': [380126],
      'p15': [199236], 'p16': [2909600], 'p17': [2331834], 'p18': [273361], 'p19': [235249], 'p20': [2475636], 'p21': [2382275, 2382315],
      'p22': [2696480], 'p23': [298116], 'p24': [2929189]}
namen = {}
for f in ('akzeptiert.csv', 'namen_extra.csv'):
    for r in csv.DictReader(open(os.path.join(W, f))):
        namen[int(float(r['plant_name_id']))] = (r['taxon_name'], r.get('taxon_authors', ''), r['geographic_area'])
vb = collections.defaultdict(list)
for f in ('verbreitung_auswahl.csv', 'verbreitung_extra.csv'):
    for r in csv.DictReader(open(os.path.join(W, f))):
        vb[int(float(r['plant_name_id']))].append(r)
# L3 → ISO3
l3iso = collections.defaultdict(set)
for r in csv.DictReader(open(os.path.join(W, 'wgsrpd_l4.csv'))):
    i2 = r['iso2'].strip()
    if not i2:
        continue
    alt = {'UK': 'GBR', 'TP': 'TLS', 'Kosovo': 'XKX', 'Montenegro': 'MNE', 'Serbia': 'SRB', 'Bonaire': 'BES', 'Curaçao': 'CUW', 'Netherlands Leeward Is.': 'BES'}
    if i2 in alt or r['l4name'] in alt:
        l3iso[r['l3'].strip()].add(alt.get(r['l4name'], alt.get(i2))); continue
    try:
        l3iso[r['l3'].strip()].add(pycountry.countries.get(alpha_2=i2).alpha_3)
    except AttributeError:
        print('ISO2 unbekannt', i2, r['l4name'])
daten, fehlt = {}, []
for p in P:
    pid = p['id']
    if pid not in ZU:
        fehlt.append(p['name']); continue
    heim, eing, l3n, wnam = set(), set(), set(), []
    for nid in ZU[pid]:
        wnam.append(namen[nid][0])
        for r in vb[nid]:
            l3 = r['area_code_l3']
            if float(r['extinct'] or 0) == 1 or float(r['location_doubtful'] or 0) == 1:
                continue
            if float(r['introduced'] or 0) == 0:
                heim |= l3iso.get(l3, set()); l3n.add(l3)
            else:
                eing |= l3iso.get(l3, set())
    eing -= heim
    daten[pid] = {'n': p['name'], 'wcvp': ' / '.join(wnam), 'heimat': sorted(heim), 'eingeb': sorted(eing), 'l3': sorted(l3n),
                  'gebiet_en': ' | '.join(namen[nid][2] for nid in ZU[pid])}
    print(pid, p['name'], len(heim), 'heimisch,', len(eing), 'eingebürgert', 'DEU' in heim)
print('ohne Daten:', fehlt)
schreibe({
    'id': 'pflanzen_heimat', 'name': 'Heimat der Heilpflanzen', 'gruppe': 'Natur', 'typ': 'land-kat', 'einheit': '',
    'felder': {'n': 'Name in der App', 'wcvp': 'akzeptierter Name in WCVP', 'heimat': 'ISO3 der Länder mit ursprünglichem Vorkommen',
               'eingeb': 'ISO3 der Länder, in denen die Art nur eingeführt/eingebürgert ist', 'l3': 'WGSRPD-Stufe-3-Codes (botanische Länder) der Heimat',
               'gebiet_en': 'Kurzbeschreibung des Areals in WCVP (englisch, zum Nachprüfen/Übersetzen)'},
    'legende': [['ursprünglich heimisch', '#5ad08a'], ['eingeführt / eingebürgert', '#e8c860']],
    'quellen': [{'t': 'Govaerts R (ed.) 2026: WCVP – World Checklist of Vascular Plants, Royal Botanic Gardens, Kew, doi:10.34885/nswv-8994 (v16, Stand 04.06.2026); Schnappschuss aus GitHub matildabrown/rWCVPdata (data/wcvp_names.rda, wcvp_distributions.rda); dieselben Daten zeigt POWO',
                 'u': 'https://github.com/matildabrown/rWCVPdata', 'stand': '2026 (v16)', 'lizenz': 'WCVP-Daten: CC BY 4.0 (Kew); R-Paket selbst GPL ≥ 3 – nur Daten übernommen'},
                {'t': 'TDWG: World Geographical Scheme for Recording Plant Distributions (WGSRPD), 2. Aufl. 2001, Stufe 4 mit ISO-Codes (GitHub tdwg/wgsrpd)',
                 'u': 'https://github.com/tdwg/wgsrpd', 'stand': '2001', 'lizenz': 'TDWG-Standard, frei zugänglich (keine ausdrückliche Lizenz; nur Code-Zuordnung übernommen)'}],
    'hinweis': 'Ein Land gilt als Heimat, wenn mindestens ein botanisches Land (WGSRPD Stufe 3) darin als ursprünglich geführt ist; große Länder (USA, Russland, China …) sind dadurch oft nur teilweise Heimat. Löwenzahn: WCVP führt T. officinale als Synonym von Taraxacum sect. Taraxacum. Königskerze und Tabak: mehrere Arten zusammengefasst. Fliegenpilz fehlt (Pilz, nicht in WCVP).'
}, daten)
