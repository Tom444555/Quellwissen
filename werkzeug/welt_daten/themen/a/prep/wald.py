"""Waldanteil je Land 2020 (FAO FRA 2020, aufbereitet von Our World in Data; GitHub owid/owid-datasets). Aufruf: python3 -I prep/wald.py"""
import sys, os, csv, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gemein import ROH, schreibe
import pycountry
SONDER = {'Democratic Republic of Congo': 'COD', 'Congo': 'COG', 'Cape Verde': 'CPV', "Cote d'Ivoire": 'CIV', 'Russia': 'RUS', 'Iran': 'IRN',
          'Turkey': 'TUR', 'Bolivia': 'BOL', 'Venezuela': 'VEN', 'Vietnam': 'VNM', 'Laos': 'LAO', 'Syria': 'SYR', 'Tanzania': 'TZA',
          'South Korea': 'KOR', 'North Korea': 'PRK', 'Moldova': 'MDA', 'Micronesia (country)': 'FSM', 'Brunei': 'BRN', 'Timor': 'TLS',
          'East Timor': 'TLS', 'Czechia': 'CZE', 'Macedonia': 'MKD', 'North Macedonia': 'MKD', 'Eswatini': 'SWZ', 'Swaziland': 'SWZ', 'Palestine': 'PSE',
          'Kosovo': 'XKX', 'Taiwan': 'TWN', 'Curacao': 'CUW', 'Saint Martin (French part)': 'MAF', 'Sint Maarten (Dutch part)': 'SXM',
          'United States Virgin Islands': 'VIR', 'British Virgin Islands': 'VGB', 'Falkland Islands': 'FLK', 'Reunion': 'REU', 'Vatican': 'VAT'}
werte = {}
for r in csv.DictReader(open(glob.glob(os.path.join(ROH, 'wald', '*.csv'))[0])):
    if r['Year'] != '2020' or not r['Forest cover']:
        continue
    e = r['Entity']
    i = SONDER.get(e)
    if not i:
        try:
            i = pycountry.countries.lookup(e).alpha_3
        except LookupError:
            continue   # Regionen/Aggregate
    werte[i] = round(float(r['Forest cover']), 1)
print(len(werte), werte.get('DEU'), werte.get('FIN'), werte.get('BRA'), werte.get('EGY'))
schreibe({
    'id': 'waldanteil', 'name': 'Waldanteil', 'gruppe': 'Natur', 'typ': 'land-wert', 'einheit': '% der Landfläche · 2020', 'jahr': 2020,
    'legende': [[0, '#f0e6c8'], [25, '#a8d08a'], [50, '#4aa060'], [75, '#1f6a3a']],
    'skala': 'linear 0–80 %',
    'quellen': [{'t': 'FAO Global Forest Resources Assessment 2020, aufbereitet von Our World in Data („Forest land, deforestation and change (FAO, 2020)“, Spalte Forest cover)',
                 'u': 'https://github.com/owid/owid-datasets/tree/master/datasets/Forest%20land%2C%20deforestation%20and%20change%20(FAO%2C%202020)', 'stand': '2020', 'lizenz': 'CC BY 4.0 (Our World in Data); Urdaten FAO FRA 2020'}],
    'hinweis': 'ISO3 → Waldfläche in % der Landfläche (FAO-Walddefinition: > 0,5 ha, Bäume > 5 m, Kronendeckung > 10 %).'
}, werte)
