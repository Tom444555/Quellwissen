"""Ebene 'kraftwerke': WRI Global Power Plant Database v1.3.0 (CC BY 4.0) – alle Kernkraftwerke, Kohle/Gas/Wasser/Öl ab 1.500 MW,
Wind/Sonne ab 300 MW; bekannte Statusänderungen nach Datenstand eingepflegt."""
import sys, pandas as pd
sys.path.insert(0, '/home/claude/scratch/themen/b/prep')
from gemein import *

d = pd.read_csv(ROH + '/gppd/gppd.csv', low_memory=False)
ART = {'Nuclear': 'kern', 'Coal': 'kohle', 'Gas': 'gas', 'Hydro': 'wasser', 'Oil': 'oel', 'Wind': 'wind', 'Solar': 'sonne'}
sel = d[(d.primary_fuel == 'Nuclear') | ((d.primary_fuel.isin(['Coal', 'Gas', 'Hydro', 'Oil'])) & (d.capacity_mw >= 1500)) |
        ((d.primary_fuel.isin(['Wind', 'Solar'])) & (d.capacity_mw >= 300))]

# Statusänderungen nach dem Datenstand (Schlüssel: gppd_idnr über Name+Land)
BASE = 'BASE (Bundesamt für die Sicherheit der nuklearen Entsorgung), Kernkraftwerke in Deutschland'
ST = {
 ('DEU', 'PHILIPPSBURG-2'): ('abgeschaltet 31.12.2019', BASE), ('DEU', 'BROKDORF'): ('abgeschaltet 31.12.2021', BASE),
 ('DEU', 'Grohnde'): ('abgeschaltet 31.12.2021', BASE), ('DEU', 'Kernkraft Gundremmingen'): ('abgeschaltet (Block B 2017, Block C 31.12.2021)', BASE),
 ('DEU', 'EMSLAND'): ('abgeschaltet 15.04.2023', BASE), ('DEU', 'ISAR-2'): ('abgeschaltet 15.04.2023', BASE), ('DEU', 'NECKARWESTHEIM-2'): ('abgeschaltet 15.04.2023', BASE),
 ('TWN', 'Chinshan'): ('abgeschaltet 2018/2019', 'Taipower'), ('TWN', 'Kuosheng'): ('abgeschaltet 2021/2023', 'Taipower'),
 ('TWN', 'Maanshan'): ('abgeschaltet 17.05.2025 (Taiwan seither ohne Kernkraft im Betrieb)', 'Taipower'),
 ('UKR', 'Zaporozhye'): ('seit März 2022 unter russischer militärischer Kontrolle; alle Blöcke abgeschaltet (Kaltabschaltung)', 'IAEA, Updates zur Lage in der Ukraine'),
 ('BEL', 'DOEL 4'): ('Doel 3 (2022), Doel 1 und 2 (2025) abgeschaltet; Doel 4 Laufzeit bis 2035 verlängert', 'Engie Electrabel; FANC'),
 ('BEL', 'TIHANGE 1N'): ('abgeschaltet 2025', 'Engie Electrabel'), ('BEL', 'TIHANGE 3'): ('Laufzeit bis 2035 verlängert (Tihange 2 abgeschaltet 2023)', 'Engie Electrabel'),
 ('USA', 'Indian Point 2'): ('abgeschaltet 30.04.2020', 'US NRC'), ('USA', 'Indian Point 3'): ('abgeschaltet 30.04.2021', 'US NRC'),
 ('USA', 'Duane Arnold Energy Center'): ('abgeschaltet 2020', 'US NRC'),
 ('USA', 'Palisades'): ('abgeschaltet 2022; Wiederinbetriebnahme genehmigt (08/2025), Netzrückkehr laut ANS 07/2026 noch ohne Termin; bis 11/2026 keine Meldung gefunden', 'US NRC; American Nuclear Society 08.07.2026'),
 ('USA', 'Vogtle'): ('seit 2023/2024 zusätzlich Blöcke 3 und 4 (je ca. 1.100 MW) in Betrieb – nicht in der Leistungsangabe', 'Georgia Power; US NRC'),
 ('GBR', 'Dungeness B'): ('abgeschaltet 2021', 'EDF Energy'), ('GBR', 'Hinkley Point B'): ('abgeschaltet 2022', 'EDF Energy'),
 ('GBR', 'Hunterston B'): ('abgeschaltet 2022', 'EDF Energy'), ('FRA', 'FESSENHEIM'): ('abgeschaltet 2020', 'EDF; ASN'),
 ('FRA', 'FLAMANVILLE'): ('Block 3 (EPR, 1.650 MW) seit 2024 am Netz – nicht in der Leistungsangabe', 'EDF'),
 ('CHE', 'Kernkraftwerk Mühleberg'): ('abgeschaltet 20.12.2019', 'BKW; ENSI'),
 ('SWE', 'Ringhals'): ('Blöcke 1 und 2 abgeschaltet 2019/2020; Leistungsangabe enthält sie noch', 'Vattenfall'),
 ('JPN', 'Fukushima Daina'): ('abgeschaltet: alle vier Blöcke, Stilllegung 07/2019 beschlossen', 'World Nuclear Association, „Nuclear Power in Japan“ (aktualisiert 22.09.2026)'),
 ('JPN', 'Genkai'): ('Blöcke 3 und 4 in Betrieb; Block 1 stillgelegt (2015)', 'World Nuclear Association, „Nuclear Power in Japan“ (aktualisiert 22.09.2026)'),
 ('JPN', 'Hamaoka'): ('kein Block in Betrieb: Block 5 betriebsfähig, aber vom Netz; Anträge für 3/4 im 09/2026 zurückgezogen; 1/2 stillgelegt (2008)', 'World Nuclear Association, „Nuclear Power in Japan“ (aktualisiert 22.09.2026)'),
 ('JPN', 'Higashi-Dori'): ('nicht in Betrieb (Wiederanfahren in Prüfung)', 'World Nuclear Association, „Nuclear Power in Japan“ (aktualisiert 22.09.2026)'),
 ('JPN', 'Ikata'): ('Block 3 in Betrieb; Blöcke 1 und 2 stillgelegt (2016/2018)', 'World Nuclear Association, „Nuclear Power in Japan“ (aktualisiert 22.09.2026)'),
 ('JPN', 'Kashiwazaki Kariwa'): ('Block 6 seit 04/2026 wieder im kommerziellen Betrieb; übrige Blöcke nicht in Betrieb', 'World Nuclear Association, „Nuclear Power in Japan“ (aktualisiert 22.09.2026)'),
 ('JPN', 'Mihama'): ('Block 3 in Betrieb; Blöcke 1 und 2 stillgelegt (2015)', 'World Nuclear Association, „Nuclear Power in Japan“ (aktualisiert 22.09.2026)'),
 ('JPN', 'Ohi'): ('Blöcke 3 und 4 in Betrieb', 'World Nuclear Association, „Nuclear Power in Japan“ (aktualisiert 22.09.2026)'),
 ('JPN', 'Onagawa'): ('Block 2 in Betrieb; Block 1 stillgelegt (2018)', 'World Nuclear Association, „Nuclear Power in Japan“ (aktualisiert 22.09.2026)'),
 ('JPN', 'Sendai'): ('Blöcke 1 und 2 in Betrieb', 'World Nuclear Association, „Nuclear Power in Japan“ (aktualisiert 22.09.2026)'),
 ('JPN', 'Shika'): ('nicht in Betrieb (Block 2 in Prüfung)', 'World Nuclear Association, „Nuclear Power in Japan“ (aktualisiert 22.09.2026)'),
 ('JPN', 'Shimane'): ('Block 2 in Betrieb; Block 1 stillgelegt (2015)', 'World Nuclear Association, „Nuclear Power in Japan“ (aktualisiert 22.09.2026)'),
 ('JPN', 'Takahama'): ('Blöcke 1–4 in Betrieb', 'World Nuclear Association, „Nuclear Power in Japan“ (aktualisiert 22.09.2026)'),
 ('JPN', 'Tokai Daini'): ('nicht in Betrieb (Wiederanfahren in Prüfung, Sicherheitsarbeiten bis 2. Hälfte FY2028)', 'World Nuclear Association, „Nuclear Power in Japan“ (aktualisiert 22.09.2026)'),
 ('JPN', 'Tomari'): ('nicht in Betrieb (Block 3: Wiederanfahren vom Gouverneur 12/2025 gebilligt, nach Fertigstellung der Flutmauer 2027)', 'World Nuclear Association, „Nuclear Power in Japan“ (aktualisiert 22.09.2026)'),
 ('JPN', 'Tsuruga'): ('nicht in Betrieb (Block 1 stillgelegt 2015; Wiederanfahren von Block 2 im 11/2024 abgelehnt)', 'World Nuclear Association, „Nuclear Power in Japan“ (aktualisiert 22.09.2026)'),
 ('CAN', 'Pickering A'): ('abgeschaltet (Block 1 am 30.09.2024, Block 4 Ende 2024; Blöcke 2 und 3 seit 1997 außer Betrieb)', 'World Nuclear News 02.01.2025'),
 ('CAN', 'Pickering B'): ('Blöcke 5–8 laut Plan seit Ende 09/2026 für die Sanierung außer Betrieb; Rückkehr Mitte der 2030er-Jahre geplant', 'American Nuclear Society 24.09.2026; World Nuclear News 02.01.2025'),
 ('PAK', 'Kanupp'): ('abgeschaltet 01.08.2021 (KANUPP-1; die neuen Blöcke K-2/K-3 am Standort sind nicht in der Leistungsangabe)', 'IAEA, Country Nuclear Power Profiles 2022 – Pakistan'),
 ('KOR', 'Kori'): ('Block 1 stillgelegt (2017); Block 2 seit 04/2026 wieder in Betrieb; Blöcke 3 und 4 nach Laufzeitverlängerung (10/2026) Wiederanfahren 1. Hälfte 2027 geplant', 'World Nuclear News 27.10.2026'),
 ('IRN', 'Bushehr'): ('in Betrieb laut Rosatom (03/2026); im März/April 2026 Einschläge in der Nähe des Geländes, keine erhöhte Strahlung (IAEA)', 'American Nuclear Society 06.04.2026 (nach IAEA); Shafaq News 19.03.2026'),
 ('ARG', 'ATUCHA I'): ('seit 29.09.2024 für die Laufzeitverlängerung außer Betrieb (geplant ca. 30 Monate)', 'World Nuclear News'),
 ('FIN', 'Olkiluoto 1'): ('Standort Olkiluoto: Block 3 (EPR, 1.600 MW) seit 16.04.2023 in regulärem Betrieb – nicht in der Leistungsangabe', 'Pohjolan Voima / TVO 04/2023'),
}
daten, gesehen = [], set()
for _, r in sel.iterrows():
    c = r.country if r.country in APP else None
    if not c: continue
    art = ART[r.primary_fuel]; mw = float(r.capacity_mw)
    gr = 3000 if art == 'kern' else 4000
    rang = 1 if mw >= gr else 2 if mw >= gr / 2 else 3
    e = {'n': r['name'], 'land': c, 'lon': r2(r.longitude), 'lat': r2(r.latitude), 'art': art, 'mw': round(mw), 'rang': rang}
    if pd.notna(r.commissioning_year): e['j'] = int(r.commissioning_year)
    k = (r.country, r['name'])
    if k in ST: e['st'], e['stq'] = ST[k]; gesehen.add(k)
    if art == 'kern' and 'st' in e and e['st'].startswith('abgeschaltet'): e['aus'] = 1
    daten.append(e)
print('nicht gefunden:', set(ST) - gesehen)
# Nach 2019 in Betrieb gegangene Kernkraftwerke an neuen Standorten (nicht in der GPPD) – Auswahl
NEU = [
 ['Barakah', 'ARE', 52.24, 23.97, 5600, 2020, 'vier Blöcke 2020–2024 in Betrieb genommen', 'ENEC (Emirates Nuclear Energy Corporation)'],
 ['Belarussisches KKW (Astrawez)', 'BLR', 26.09, 54.76, 2400, 2020, 'zwei Blöcke 2020/2023 in Betrieb genommen', 'IAEA PRIS; Belarus Energieministerium'],
]
for n, c, lo, la, mw, j, st, q in NEU:
    daten.append({'n': n, 'land': c, 'lon': r2(lo), 'lat': r2(la), 'art': 'kern', 'mw': mw, 'rang': 1 if mw >= 3000 else 2, 'j': j, 'st': st, 'stq': q, 'neu': 1})
import collections
print(len(daten), collections.Counter(e['art'] for e in daten))
NAME = {'kern': ['Kernkraft', '#ffe14a'], 'kohle': ['Kohle', '#8a7a6a'], 'gas': ['Erdgas', '#5fb8ff'], 'wasser': ['Wasserkraft', '#4a8ae8'],
        'oel': ['Öl', '#ff8a3d'], 'wind': ['Wind', '#9ae0c0'], 'sonne': ['Sonne', '#ffb84a']}
obj = {'id': 'kraftwerke', 'name': 'Große Kraftwerke & alle Kernkraftwerke', 'gruppe': 'Wirtschaft', 'typ': 'punkte', 'einheit': 'MW',
       'legende': [{'k': k, 'n': v[0], 'c': v[1]} for k, v in NAME.items()],
       'quellen': [{'t': 'World Resources Institute (WRI), Global Power Plant Database v1.3.0 (Byers u. a.)', 'u': 'https://github.com/wri/global-power-plant-database',
                    'stand': 'Version 1.3.0 (06/2021), Leistungsdaten überwiegend 2017–2019', 'lizenz': 'CC BY 4.0 – Namensnennung: „Global Power Plant Database, WRI“'},
                   {'t': 'Statusänderungen: BASE (Deutschland), IAEA, US NRC, Betreiber (Feld stq je Anlage)', 'u': 'https://www.base.bund.de/DE/themen/kt/kta-deutschland/kta-deutschland_node.html',
                    'stand': '11/2026', 'lizenz': 'Fakten aus amtlichen Angaben'}],
       'hinweis': 'ACHTUNG Datenstand: Grunddaten aus der WRI-Datenbank (Stand 2019–2021, seit 2021 nicht fortgeschrieben) – viele neue Anlagen fehlen, Leistungen sind nicht aktuell. '
                  'Status der Kernkraftwerke am 25.11.2026 für Deutschland, Japan, Kanada, Korea, Pakistan, Iran, Argentinien, Taiwan, Belgien und Einzelanlagen geprüft (Feld st/stq), sonst ohne Gewähr. '
                  'Auswahl: alle Kernkraftwerke der Datenbank, Kohle/Gas/Wasser/Öl ab 1.500 MW, Wind/Sonne ab 300 MW; '
                  'bekannte Abschaltungen und einige neue Kernkraftwerke sind nachgetragen (Felder st/aus/neu), sonst keine Aktualisierung. Kernkraftwerke in Deutschland: alle seit spätestens 15.04.2023 abgeschaltet.',
       'felder': {'n': 'Name (wie in der Quelle)', 'land': 'ISO3', 'art': 'kern, kohle, gas, wasser, oel, wind, sonne', 'mw': 'installierte Leistung in MW', 'j': 'Inbetriebnahme (bei mehreren Blöcken gemittelt in der Quelle)',
                  'st': 'Statusänderung nach Datenstand', 'stq': 'Beleg dazu', 'aus': '1 = abgeschaltet', 'neu': '1 = nachgetragen, nicht aus der WRI-Datenbank', 'rang': '1–3'},
       'daten': daten}
schreibe(obj)
