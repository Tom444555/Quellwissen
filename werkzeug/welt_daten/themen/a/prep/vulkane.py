"""Vulkane: NOAA NCEI Global Volcano Locations (Kopie in plotly/datasets) + NOAA NCEI Significant Volcanic Eruptions (Kopie in leestott/intro-Datascience).
Aufruf: python3 -I prep/vulkane.py"""
import csv, sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gemein import ROH, r2, schreibe
import pycountry

D = os.path.join(ROH, 'vulkane')
loc = list(csv.DictReader(open(os.path.join(D, 'noaa_volcano_locations_plotly.csv'), encoding='latin-1')))
sig = list(csv.DictReader(open(os.path.join(D, 'noaa_significant_eruptions.csv'), encoding='latin-1')))

ZEIT = {'D1': (1, '1964 oder später'), 'D2': (2, '1900–1963'), 'D3': (3, '1800–1899'), 'D4': (4, '1700–1799'),
        'D5': (5, '1500–1699'), 'D6': (6, '1–1499 n. Chr.'), 'D7': (7, 'v. Chr. (Holozän)'),
        'U': (8, 'undatiert (wohl Holozän)'), '?': (9, 'unsicher (Holozän)'), 'Q': (9, 'nur hydrothermal im Holozän')}
TYP = {'Stratovolcano': 'Schichtvulkan', 'Stratovolcanoes': 'Schichtvulkan', 'Shield volcano': 'Schildvulkan', 'Shield volcanoes': 'Schildvulkan',
       'Submarine volcano': 'Unterseevulkan', 'Submarine volcanoes': 'Unterseevulkan', 'Submarine volcano?': 'Unterseevulkan',
       'Volcanic field': 'Vulkanfeld', 'Caldera': 'Caldera', 'Cinder cone': 'Schlackenkegel', 'Cinder cones': 'Schlackenkegel',
       'Scoria cone': 'Schlackenkegel', 'Scoria cones': 'Schlackenkegel', 'Complex volcano': 'Vulkankomplex', 'Volcanic complex': 'Vulkankomplex',
       'Compound volcano': 'Vulkankomplex', 'Lava dome': 'Lavadom', 'Lava domes': 'Lavadom', 'Pyroclastic cone': 'Aschenkegel',
       'Pyroclastic cones': 'Aschenkegel', 'Maar': 'Maar', 'Maars': 'Maar', 'Fissure vent': 'Spaltenvulkan', 'Fissure vents': 'Spaltenvulkan',
       'Crater rows': 'Kraterreihe', 'Tuff cone': 'Tuffkegel', 'Tuff rings': 'Tuffring', 'Pyroclastic shield': 'Schildvulkan',
       'Somma volcano': 'Sommavulkan', 'Subglacial volcano': 'subglazialer Vulkan', 'Lava cone': 'Lavakegel', 'Explosion crater': 'Explosionskrater',
       'Fumarole field': 'Fumarolenfeld', 'Pumice cone': 'Bimskegel', 'Cone': 'Kegel', 'Hydrothermal field': 'Hydrothermalfeld', 'Mud volcano': 'Schlammvulkan'}
# Deutsche Namen (gebräuchliche Exonyme bzw. Schreibweise mit Sonderzeichen)
DEN = {'Vesuvius': 'Vesuv', 'Etna': 'Ätna', 'St. Helens': 'Mount St. Helens', 'Kilimanjaro': 'Kilimandscharo', 'Tenerife': 'Teide (Teneriffa)',
       'Popocatepetl': 'Popocatépetl', 'Kilauea': 'Kīlauea', 'West Eifel Volc Field': 'Vulkaneifel (Westeifel)', 'Chaine des Puys': 'Chaîne des Puys',
       'Eyjafjallajokull': 'Eyjafjallajökull', 'Grimsvotn': 'Grímsvötn', 'Kliuchevskoi': 'Kljutschewskaja Sopka', 'Lengai, Ol Doinyo': 'Ol Doinyo Lengai',
       'Cameroon, Mt.': 'Kamerunberg', 'Fournaise, Piton de la': 'Piton de la Fournaise', 'Misti, El': 'El Misti', 'Orizaba, Pico de': 'Pico de Orizaba (Citlaltépetl)',
       'Ruiz': 'Nevado del Ruiz', 'Pelee': 'Mont Pelée', 'Sakura-jima': 'Sakurajima', 'Soufriere Hills': 'Soufrière Hills', 'Soufriere St. Vincent': 'La Soufrière (St. Vincent)',
       'Soufriere Guadeloupe': 'La Soufrière (Guadeloupe)', 'Egmont': 'Taranaki (Egmont)', 'Paricutin Volcanic Field': 'Paricutín', 'Lassen Volc Center': 'Lassen Peak',
       'Hood': 'Mount Hood', 'Rainier': 'Mount Rainier', 'Shasta': 'Mount Shasta', 'Baker': 'Mount Baker', 'Ojos del Salado, Nevados': 'Ojos del Salado',
       'Toluca, Nevado de': 'Nevado de Toluca', 'Chachani, Nevado': 'Chachani', 'Hunga Tonga-Hunga Ha\'apai': 'Hunga Tonga-Hunga Haʻapai',
       'Erebus': 'Mount Erebus', 'Elbrus': 'Elbrus', 'Ararat': 'Ararat', 'Damavand': 'Damavand', 'Santorini': 'Santorin', 'Lascar': 'Láscar',
       'Chillan, Nevados de': 'Nevados de Chillán', 'Galeras': 'Galeras', 'Tolbachik': 'Tolbatschik', 'Shiveluch': 'Schiwelutsch', 'Bezymianny': 'Besymjanny',
       'Askja': 'Askja', 'Hekla': 'Hekla', 'White Island': 'Whakaari (White Island)', 'Mauna Loa': 'Mauna Loa', 'Mauna Kea': 'Mauna Kea'}
LAND_SONDER = {'Antarctica': 'ATA', 'Bouvet I.': 'BVT', 'Congo, DRC': 'COD', 'French Southern & Antarctic Lands': 'ATF', 'Heard I. & McDonald Is.': 'HMD',
               'Jan Mayen': 'SJM', 'Reunion': 'REU', 'Sao Tome & Principe': 'STP', 'Solomon Is.': 'SLB', 'St. Kitts & Nevis': 'KNA', 'St. Lucia': 'LCA',
               'St. Vincent & the Grenadines': 'VCT', 'Trinidad': 'TTO', 'Wallis & Futuna': 'WLF', 'Turkey': 'TUR', 'Iran': 'IRN', 'Russia': 'RUS',
               'North Korea': 'PRK', 'South Korea': 'KOR', 'Taiwan': 'TWN', 'Vietnam': 'VNM', 'Syria': 'SYR', 'Tanzania': 'TZA', 'Bolivia': 'BOL',
               'Cape Verde': 'CPV', 'United States': 'USA', 'United Kingdom': 'GBR', 'Libya': 'LBY', 'Congo': 'COG'}


def iso3(land):
    if land in ('Pacific Ocean', 'Atlantic Ocean', 'Indian Ocean', 'Arctic Ocean'):
        return None
    if land in LAND_SONDER:
        return LAND_SONDER[land]
    try:
        return pycountry.countries.lookup(land).alpha_3
    except LookupError:
        print('ohne ISO3:', land)
        return None


# Bedeutende Ausbrüche je Vulkan (Name + Koordinaten)
SIG = collections.defaultdict(list)
for e in sig:
    try:
        SIG[(e['Name'].strip(), round(float(e['Latitude']), 1), round(float(e['Longitude']), 1))].append(e)
    except ValueError:
        pass


def jt(j):
    return f'{-j} v. Chr.' if j < 0 else (f'{j} n. Chr.' if j < 1000 else str(j))


def zahl(s):
    try:
        return float(s)
    except (ValueError, TypeError):
        return None


raus, gesehen = [], set()
for v in loc:
    name = v['Volcano Name'].strip()
    try:
        lat, lon = float(v['Latitude']), float(v['Longitude'])
    except ValueError:
        continue
    if v['Type'] == 'Not Volcanic':
        continue
    key = (name, round(lat, 1), round(lon, 1))
    if key in gesehen:
        continue
    gesehen.add(key)
    code = v['Last Known'].strip()
    zk, ztext = ZEIT.get(code, (9, 'unbekannt'))
    ev = SIG.get(key, [])
    jahre = [int(e['Year']) for e in ev if e['Year'].lstrip('-').isdigit()]
    letzt_sig = max(jahre) if jahre else None
    if letzt_sig is not None and letzt_sig >= 1964 and zk > 1:   # Liste älter als Ausbruchsliste: Zeitklasse nachziehen
        zk, ztext = 1, '1964 oder später'
    vei = max([int(zahl(e['VEI'])) for e in ev if zahl(e['VEI']) is not None], default=None)
    tote = max([zahl(e['TOTAL_DEATHS']) or zahl(e['DEATHS']) or 0 for e in ev], default=0)
    # Rang: 1 = VEI>=4 und aktiv seit 1900, oder VEI>=5, oder >=300 Tote, oder bekannter Name; 2 = aktiv seit 1900 oder bedeutender Ausbruch; 3 = Ausbruch seit 1800 oder Höhe >= 4500 m
    elev = zahl(v['Elev'])
    if (vei is not None and vei >= 4 and zk <= 2) or (vei is not None and vei >= 5) or tote >= 300 or name in DEN:
        rang = 1
    elif zk <= 2 or ev:
        rang = 2
    elif zk <= 3 or (elev is not None and elev >= 4500):
        rang = 3
    else:
        continue
    txt = ''
    if ev:
        stark = max(ev, key=lambda e: (zahl(e['VEI']) or -1, -abs(int(e['Year']) if e['Year'].lstrip('-').isdigit() else 0)))
        teile = []
        if vei is not None:
            j = int(stark['Year'])
            teile.append(f"Stärkster erfasster Ausbruch {jt(j)} (VEI {vei})")
        if tote >= 1:
            schwer = max(ev, key=lambda e: zahl(e['TOTAL_DEATHS']) or zahl(e['DEATHS']) or 0)
            j = int(schwer['Year'])
            teile.append(f"meiste Todesopfer {jt(j)}: {int(tote):,}".replace(',', '.'))
        if teile:
            txt = '; '.join(teile) + ' (NOAA).'
    raus.append([DEN.get(name, name), r2(lon), r2(lat), TYP.get(v['Type'], v['Type']), int(elev) if elev is not None else None,
                 zk, rang, iso3(v['Country']), letzt_sig, txt])

raus.sort(key=lambda x: (x[6], x[5]))
print(collections.Counter(x[6] for x in raus))
schreibe({
    'id': 'vulkane', 'name': 'Vulkane', 'gruppe': 'Natur', 'typ': 'punkte', 'einheit': 'm Höhe',
    'felder': ['name', 'lon', 'lat', 'typ', 'hoehe_m', 'zeit', 'rang', 'iso3', 'letzter_bedeutender_ausbruch', 'text'],
    'zeit': {str(k): t for k, t in sorted({z[0]: z[1] for z in ZEIT.values()}.items())},
    'legende': [['Ausbruch seit 1964', '#ff4a2a'], ['1900–1963', '#ff9a3a'], ['1500–1899', '#ffd27a'], ['älter / undatiert', '#c8b8a8']],
    'quellen': [
        {'t': 'NOAA NCEI: Global Volcano Locations Database (doi:10.7289/V5JW8BSH), Daten nach Smithsonian GVP; Kopie in GitHub plotly/datasets (volcano_db.csv)',
         'u': 'https://raw.githubusercontent.com/plotly/datasets/master/volcano_db.csv', 'stand': 'ca. 2010 (Datei-Stand), Zeitklassen D1–D7',
         'lizenz': 'CC0 1.0 (laut catalog.data.gov)'},
        {'t': 'NOAA NCEI/WDS Global Significant Volcanic Eruptions Database (doi:10.7289/V5JW8BSH); Kopie in GitHub leestott/intro-Datascience',
         'u': 'https://raw.githubusercontent.com/leestott/intro-Datascience/main/Data/noaa_volerup.csv', 'stand': 'bis 2019',
         'lizenz': 'US-Regierungswerk, gemeinfrei / CC0'}],
    'hinweis': 'Letzter Ausbruch als Zeitklasse (NOAA-Code); Jahr nur, wenn ein bedeutender Ausbruch in der NOAA-Liste steht (bis 2019). Ausbrüche nach 2019 (z. B. Hunga Tonga 2022, Reykjanes ab 2021) fehlen.'
}, raus)
