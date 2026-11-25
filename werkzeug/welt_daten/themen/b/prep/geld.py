"""Ebenen 'staatsschulden' (IWF Fiscal Monitor 04/2026), 'goldreserven' (IWF IFS über Presse), 'waehrungen' (CLDR)."""
import sys, collections, datetime
sys.path.insert(0, '/home/claude/scratch/themen/b/prep')
from gemein import *
from babel.core import get_global
from babel import Locale

# --- Staatsschulden: IMF Fiscal Monitor April 2026, Tabellen A7, A15, A21, Spalte 2025 (Bruttoschulden Gesamtstaat, % BIP)
FM = """Australia AUS 51.0|Austria AUT 80.5|Belgium BEL 106.3|Bulgaria BGR 27.1|Canada CAN 113.5|Croatia HRV 55.9|Cyprus CYP 55.3|Czech Republic CZE 44.6|
Denmark DNK 27.5|Estonia EST 24.2|Finland FIN 89.3|France FRA 116.0|Germany DEU 62.9|Greece GRC 145.7|Hong Kong HKG 11.9|Iceland ISL 56.1|Ireland IRL 32.9|
Israel ISR 68.5|Italy ITA 137.1|Japan JPN 206.5|Korea KOR 52.3|Latvia LVA 46.9|Lithuania LTU 39.8|Luxembourg LUX 27.0|Malta MLT 46.8|Netherlands NLD 43.3|
New Zealand NZL 54.7|Norway NOR 45.0|Portugal PRT 89.9|Singapore SGP 171.3|Slovak Republic SVK 61.6|Slovenia SVN 65.9|Spain ESP 100.4|Sweden SWE 34.9|
Switzerland CHE 39.4|United Kingdom GBR 102.3|United States USA 123.9|Andorra AND 30.3|
Algeria DZA 54.1|Angola AGO 51.3|Argentina ARG 80.3|Bahrain BHR 147.6|Belarus BLR 33.1|Brazil BRA 93.3|Chile CHL 41.8|China CHN 99.2|Colombia COL 59.9|
Dominican Republic DOM 59.0|Ecuador ECU 54.4|Egypt EGY 86.8|Hungary HUN 75.2|India IND 84.1|Indonesia IDN 41.0|Iran IRN 37.3|Kazakhstan KAZ 24.6|Kuwait KWT 14.6|
Lebanon LBN 139.4|Malaysia MYS 70.7|Mexico MEX 61.8|Morocco MAR 67.1|Oman OMN 35.8|Pakistan PAK 72.8|Peru PER 30.2|Philippines PHL 59.4|Poland POL 58.8|
Qatar QAT 41.4|Romania ROU 60.6|Russia RUS 17.2|Saudi Arabia SAU 31.7|South Africa ZAF 78.6|Thailand THA 64.7|Türkiye TUR 23.5|Ukraine UKR 108.7|
United Arab Emirates ARE 34.3|Uruguay URY 65.7|Venezuela VEN 308.7|
Afghanistan AFG 8.0|Bangladesh BGD 42.0|Benin BEN 57.3|Burkina Faso BFA 52.0|Cambodia KHM 26.5|Cameroon CMR 40.4|Chad TCD 30.4|DR Congo COD 20.2|Rep. Congo COG 96.8|
Côte d'Ivoire CIV 56.3|Ethiopia ETH 43.1|Ghana GHA 48.8|Guinea GIN 48.1|Haiti HTI 12.3|Honduras HND 41.2|Kenya KEN 69.3|Kyrgyz Republic KGZ 36.0|Lao PDR LAO 80.6|
Madagascar MDG 48.7|Malawi MWI 78.4|Mali MLI 41.9|Moldova MDA 36.6|Mozambique MOZ 102.5|Myanmar MMR 51.9|Nepal NPL 48.1|Nicaragua NIC 34.8|Niger NER 45.4|
Nigeria NGA 35.5|Papua New Guinea PNG 52.1|Rwanda RWA 64.6|Senegal SEN 130.2|Sudan SDN 187.6|Tajikistan TJK 21.6|Tanzania TZA 49.7|Uganda UGA 54.2|
Uzbekistan UZB 28.6|Zambia ZMB 86.0|Zimbabwe ZWE 43.8"""
daten = {}
for t in FM.replace('\n', '').split('|'):
    *_, c, v = t.strip().split(' ')
    assert c in APP, c
    daten[c] = float(v)
print('Schulden:', len(daten))
schreibe({'id': 'staatsschulden', 'name': 'Staatsschulden', 'gruppe': 'Wirtschaft', 'typ': 'land-wert', 'einheit': '% der Wirtschaftsleistung (BIP) · 2025',
          'legende': {'palette': 'rot', 'skala': 'linear 0–200 (darüber gekappt)', 'stufen': ['0 %', '60 %', '120 %', '200 %+']},
          'quellen': [{'t': 'IWF, Fiscal Monitor April 2026, Statistischer Anhang, Tabellen A7 (Industrieländer), A15 (Schwellenländer), A21 (Entwicklungsländer mit niedrigem Einkommen): Bruttoschulden des Gesamtstaats, Spalte 2025',
                       'u': 'https://www.imf.org/-/media/files/publications/fiscal-monitor/2026/april/english/msa.pdf', 'stand': '04/2026 (Werte 2025, teils Schätzung)',
                       'lizenz': 'IMF Copyright and Usage: Weitergabe mit Quellenangabe „Source: International Monetary Fund, Fiscal Monitor April 2026“ erlaubt; kommerzielle Weiterverwendung nur nach Genehmigung (copyright@imf.org)'}],
          'hinweis': 'Bruttoschulden des Gesamtstaats in % des BIP 2025 laut IWF. Länder, die im Fiscal-Monitor-Anhang nicht stehen, fehlen (z. B. kleine Staaten); '
                     'Sri Lanka und Jemen ohne Wert in der Quelle. Our World in Data war aus der Arbeitsumgebung nicht abrufbar, daher direkt die IWF-Tabellen.',
          'daten': daten})

# --- Goldreserven
GOLD = [('USA', 8133.5, 'Anfang 2026'), ('DEU', 3350.3, 'Anfang 2026'), ('ITA', 2451.8, 'Anfang 2026'), ('FRA', 2437.0, 'Anfang 2026'),
        ('RUS', 2326.5, 'Anfang 2026'), ('CHN', 2306.3, 'Anfang 2026 (amtlich 2.331 t im Mai 2026)'), ('CHE', 1039.9, 'Anfang 2026'), ('IND', 880.3, 'Anfang 2026'),
        ('JPN', 846.0, 'Anfang 2026'), ('TUR', 614.3, 'Anfang 2026'), ('NLD', 612.5, 'Anfang 2026'), ('POL', 614.0, '2026 (ungefähr)'), ('GBR', 310.3, 'Anfang 2026'),
        ('HUN', 110.0, 'Anfang 2026'), ('CZE', 71.6, 'Mai 2026'), ('IRL', 12.0, 'Anfang 2026'), ('GEO', 7.1, 'Anfang 2026'), ('ZWE', 4.1, 'Anfang 2026'),
        ('SAU', 323.0, 'Mitte 2025 (ca.)'), ('LBN', 286.0, 'Mitte 2025'), ('DZA', 174.0, 'Mitte 2025'), ('EGY', 126.0, 'Mitte 2025')]
gd = {c: {'t': v, 'stand': s} for c, v, s in GOLD}
schreibe({'id': 'goldreserven', 'name': 'Goldreserven der Zentralbanken', 'gruppe': 'Wirtschaft', 'typ': 'land-wert', 'einheit': 'Tonnen',
          'legende': {'palette': 'gold', 'skala': 'Wurzel 0–8.200 t (Kreisgröße)', 'stufen': ['100 t', '1.000 t', '8.000 t']},
          'quellen': [{'t': 'BullionVault, „Which country owns the most gold?“ – nach IWF International Financial Statistics (Meldungen der Zentralbanken, Ende Dezember 2025, teils neuere Zentralbankangaben)',
                       'u': 'https://www.bullionvault.com/gold-news/infographics/which-country-owns-most-gold-gold-reserves-nation', 'stand': 'Anfang 2026', 'lizenz': 'Fakten (IWF-Meldedaten)'},
                      {'t': 'Khaleej Times, „Global gold reserves: US dominates as India, UAE gain ground“ (24.08.2025), nach World Gold Council – nur SAU, LBN, DZA, EGY',
                       'u': 'https://www.khaleejtimes.com/business/global-gold-reserves-us-dominates-as-india-uae-gain-ground', 'stand': 'Mitte 2025', 'lizenz': 'Fakten'}],
          'hinweis': 'Nur Länder mit belegter Tonnenzahl (22). Stand je Land im Feld „stand“. Amtliche Angaben sind Selbstauskünfte der Zentralbanken. '
                     'Die vollständige Tabelle des World Gold Council darf laut dessen Nutzungsbedingungen ohne schriftliche Erlaubnis nicht weiterverbreitet werden.',
          'daten': gd})

# --- Währungen (CLDR)
tc = get_global('territory_currencies'); de = Locale('de')
heute = datetime.date(2026, 11, 25)
wd = {}
for a2, lst in tc.items():
    c = A2.get(a2)
    if not c or c in wd: continue
    akt = [cur for cur, von, bis, tender in lst if tender and (bis is None or datetime.date(*bis) > heute) and (von is None or datetime.date(*von) <= heute)]
    if not akt: continue
    wd[c] = akt
# Bulgarien: Euro seit 01.01.2026 (EZB) – CLDR 47 kennt das noch nicht
wd['BGR'] = ['EUR']
zahl = collections.Counter(x[0] for x in wd.values())
UNION = {'EUR': 'Euro', 'XOF': 'CFA-Franc BCEAO (Westafrika)', 'XAF': 'CFA-Franc BEAC (Zentralafrika)', 'XCD': 'Ostkaribischer Dollar', 'USD': 'US-Dollar (allein oder neben eigener Währung)'}
daten = {}
for c, l in wd.items():
    h = l[0]
    if 'USD' in l: h = 'USD'
    kat = h if h in UNION else ('gemeinsam' if zahl[h] > 1 else 'eigen')
    e = {'w': [de.currencies.get(x) or {'ZWG': 'Simbabwe-Gold (ZiG)', 'XCG': 'Karibischer Gulden'}.get(x, x) for x in l], 'code': l, 'kat': kat}
    daten[c] = e
# Gebiete ohne CLDR-Eintrag (eigene Polygone der App): Nordzypern nutzt die Türkische Lira, Somaliland den Somaliland-Schilling (ohne ISO-Code)
daten['CYN'] = {'w': ['Türkische Lira'], 'code': ['TRY'], 'kat': 'gemeinsam'}
daten['SOL'] = {'w': ['Somaliland-Schilling'], 'code': [], 'kat': 'eigen'}
leg = [{'k': k, 'n': n, 'z': sum(1 for e in daten.values() if e['kat'] == k)} for k, n in UNION.items()] + \
      [{'k': 'gemeinsam', 'n': 'andere Währung mehrerer Gebiete (z. B. Australischer Dollar, Rand, Schweizer Franken)', 'z': sum(1 for e in daten.values() if e['kat'] == 'gemeinsam')},
       {'k': 'eigen', 'n': 'eigene Landeswährung', 'z': sum(1 for e in daten.values() if e['kat'] == 'eigen')}]
FARB = {'EUR': '#3a6ad8', 'XOF': '#e8a050', 'XAF': '#d8804a', 'XCD': '#4ad0c8', 'USD': '#5ac87a', 'gemeinsam': '#9a7ad8', 'eigen': '#5a6070'}
for x in leg: x['c'] = FARB[x['k']]
print({x['k']: x['z'] for x in leg})
for c in ('DEU', 'BGR', 'ZWE', 'ECU', 'SEN', 'CMR', 'LIE', 'MNE', 'XKX', 'PAN', 'CUB', 'TLS'): print(c, daten.get(c))
schreibe({'id': 'waehrungen', 'name': 'Währungen & Währungsräume', 'gruppe': 'Wirtschaft', 'typ': 'land-kat', 'einheit': '',
          'legende': leg,
          'quellen': [{'t': f'Unicode CLDR 47 (territory currencies, gesetzliche Zahlungsmittel), über Python-Paket babel {__import__("babel").__version__}', 'u': 'https://github.com/unicode-org/cldr',
                       'stand': '2025 (CLDR 47); Bulgarien auf Euro (01.01.2026) nachgetragen', 'lizenz': 'Unicode License v3'},
                      {'t': 'EZB, „Bulgaria joins the euro“ (01.01.2026)', 'u': 'https://www.ecb.europa.eu/press/pr/date/2026/html/ecb.pr260101~c830245e42.en.html', 'stand': '01/2026', 'lizenz': 'Fakten'}],
          'hinweis': 'Gültige gesetzliche Zahlungsmittel je Gebiet (bei mehreren: alle in „w“, die erste bestimmt die Kategorie). Kategorie = Währungsunion bzw. von mehreren Gebieten genutzte Währung.',
          'felder': {'w': 'Währungen (deutsch)', 'code': 'ISO-4217-Codes', 'kat': 'Kategorie'},
          'daten': daten})
