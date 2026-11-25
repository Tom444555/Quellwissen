"""Heilbäder und Orte mit Heilquellen-/Sole-/Moorkurbetrieb – Teilliste aus amtlichen Landesverzeichnissen (Niedersachsen 2026, Bayern 2020, Nordrhein-Westfalen 2026, Sachsen 2019).
Koordinaten: GeoNames cities1000 (CC BY 4.0). Aufruf: python3 -I prep/heilbaeder.py"""
import sys, os, csv, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gemein import ROH, schreibe, r2

def norm(s):
    s = s.replace('ä', 'a').replace('ö', 'o').replace('ü', 'u').replace('ß', 'ss')
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower().replace('ue', 'u').replace('oe', 'o').replace('ae', 'a')
GN = {}
for r in csv.DictReader(open(os.path.join(ROH, 'wege', 'geonames_cities1000_rg.csv'), encoding='utf-8')):
    if r['cc'] == 'DE':
        GN.setdefault(norm(r['name']), []).append((float(r['lon']), float(r['lat']), r['admin1']))
LAND = {'NI': 'Lower Saxony', 'BY': 'Bavaria', 'NW': 'North Rhine-Westphalia', 'SN': 'Saxony'}
fehlt = []
# Ergänzung aus GeoNames (Paket geonamescache 3.0.2, CC BY 4.0), wo der reverse_geocoder-Auszug den Ort nicht enthält
GN_ERG = {'Salzgitter': (10.4154, 52.15705, 'Lower Saxony')}
def ort(n, land):
    for k in [n] + ([n.split(' (')[0]] if ' (' in n else []):
        c = [q for q in GN.get(norm(k), []) if q[2] == LAND[land]]
        if c:
            return c[0]
    if n in GN_ERG:
        return GN_ERG[n]
    fehlt.append(n); return None

# [Ort, Land, Prädikat laut Verzeichnis, Art (Kurzform), GeoNames-Name]
NI = [('Bad Bederkesa', 'Ort mit Moor-Kurbetrieb', 'Moor', 'Bad Bederkesa'), ('Bad Bentheim', 'Mineralheilbad', 'Mineralquelle', 'Bad Bentheim'),
      ('Bad Bevensen', 'Jod-Sole-Heilbad', 'Sole (Jod)', 'Bad Bevensen'), ('Bad Eilsen', 'Ort mit Heilquellen-Kurbetrieb', 'Heilquelle', 'Bad Eilsen'),
      ('Bad Essen', 'Ort mit Sole-Kurbetrieb', 'Sole', 'Bad Essen'), ('Bad Grund', 'Ort mit Heilstollen-Kurbetrieb', 'Heilstollen', 'Bad Grund'),
      ('Bad Harzburg', 'Soleheilbad', 'Sole', 'Bad Harzburg'), ('Bad Laer', 'Soleheilbad', 'Sole', 'Bad Laer'),
      ('Bad Nenndorf', 'Moorheilbad, Mineralheilbad, Thermalheilbad', 'Thermal, Mineral, Moor', 'Bad Nenndorf'),
      ('Bad Pyrmont', 'Moorheilbad, Mineralheilbad', 'Mineralquelle, Moor', 'Bad Pyrmont'), ('Bad Rothenfelde', 'Soleheilbad', 'Sole', 'Bad Rothenfelde'),
      ('Bad Salzdetfurth', 'Soleheilbad, Moorheilbad', 'Sole, Moor', 'Bad Salzdetfurth'), ('Bad Zwischenahn', 'Moorheilbad', 'Moor', 'Bad Zwischenahn'),
      ('Salzgitter-Bad', 'Ort mit Sole-Kurbetrieb', 'Sole', 'Salzgitter'), ('Soltau', 'Ort mit Sole-Kurbetrieb', 'Sole', 'Soltau')]
BY = [(n, 'Heilbad', 'Heilbad (Art im Verzeichnis nicht genannt)', g) for n, g in [
      ('Bad Abbach', 'Bad Abbach'), ('Bad Aibling', 'Bad Aibling'), ('Bad Alexandersbad', 'Bad Alexandersbad'), ('Bad Bayersoien', 'Bad Bayersoien'),
      ('Bad Birnbach', 'Bad Birnbach'), ('Bad Brückenau', 'Bad Bruckenau'), ('Bad Endorf', 'Bad Endorf'), ('Bad Feilnbach', 'Bad Feilnbach'),
      ('Bad Füssing', 'Bad Fussing'), ('Bad Griesbach i. Rottal', 'Bad Griesbach'), ('Bad Königshofen i. Grabfeld', 'Bad Konigshofen im Grabfeld'),
      ('Bad Kohlgrub', 'Bad Kohlgrub'), ('Bad Neualbenreuth', 'Neualbenreuth'), ('Bad Neustadt a. d. Saale', 'Bad Neustadt an der Saale'),
      ('Bad Rodach', 'Bad Rodach'), ('Bad Staffelstein', 'Bad Staffelstein'), ('Bad Tölz', 'Bad Tolz'), ('Bad Wiessee', 'Bad Wiessee'),
      ('Bad Windsheim', 'Bad Windsheim'), ('Füssen (Bad Faulenbach)', 'Fussen'), ('Bad Gögging (Neustadt a. d. Donau)', 'Neustadt an der Donau')]]
BY += [('Bad Kissingen', 'Bayerisches Staatsbad, Mineral- und Moorbad', 'Mineralquelle, Moor', 'Bad Kissingen'),
       ('Bad Bocklet', 'Bayerisches Staatsbad, Mineral- und Moorbad', 'Mineralquelle, Moor', 'Bad Bocklet'),
       ('Bad Reichenhall', 'Bayerisches Staatsbad, Mineral- und Moorbad', 'Mineralquelle, Moor', 'Bad Reichenhall'),
       ('Bad Steben', 'Bayerisches Staatsbad, Mineral- und Moorbad', 'Mineralquelle, Moor', 'Bad Steben'),
       ('Treuchtlingen', 'Ort mit Heilquellenkurbetrieb (Altmühltherme, Lambertusbad)', 'Heilquelle', 'Treuchtlingen'),
       ('Bayreuth', 'Ort mit Heilquellenkurbetrieb (Lohengrin Therme)', 'Heilquelle', 'Bayreuth'),
       ('Weißenstadt', 'Ort mit Heilquellenkurbetrieb (Kurzentrum)', 'Heilquelle', 'Weissenstadt')]
# Nordrhein-Westfalen: Verzeichnis der staatlichen Anerkennungen von Kurorten, Erholungsorten und Heilbrunnen (recht.nrw.de, Fassung bis 22.07.2026).
# Nur „Heilbad“ und „Ort mit Heilquellenkurbetrieb“; Kneipp-Heilbäder (Bad Berleburg, Bad Fredeburg, Bad Laasphe, Bad Münstereifel, Bad Salzuflen,
# Bad Wünnenberg, Brilon, Olsberg) wie in NI/BY weggelassen. Ortsteile ohne GeoNames-Eintrag: Lage der Gemeinde.
NW = [('Bad Waldliesborn (Lippstadt)', 'Heilbad', 'Heilbad (Art im Verzeichnis nicht genannt)', 'Lippstadt'),
      ('Bad Sassendorf', 'Heilbad', 'Heilbad (Art im Verzeichnis nicht genannt)', 'Bad Sassendorf'),
      ('Bad Westernkotten (Erwitte)', 'Heilbad', 'Heilbad (Art im Verzeichnis nicht genannt)', 'Erwitte'),
      ('Bad Driburg', 'Heilbad', 'Heilbad (Art im Verzeichnis nicht genannt)', 'Bad Driburg'),
      ('Bad Lippspringe', 'Heilbad; Heilklimatischer Kurort', 'Heilbad (Art im Verzeichnis nicht genannt)', 'Bad Lippspringe'),
      ('Bad Holzhausen (Preußisch Oldendorf)', 'Heilbad', 'Heilbad (Art im Verzeichnis nicht genannt)', 'Preussisch Oldendorf'),
      ('Aachen (Monheimsallee und Burtscheid)', 'Heilbad', 'Heilbad (Art im Verzeichnis nicht genannt)', 'Aachen'),
      ('Kevelaer', 'Ort mit Heilquellenkurbetrieb', 'Heilquelle', 'Kevelaer')]
# Sachsen: Staatlich anerkannte Kurorte im Freistaat Sachsen, Liste 1 (REVOSax, Stand 11.09.2019). Bad Gottleuba (Moorheilbad) ohne GeoNames-Eintrag.
SN = [('Bad Brambach', 'Mineralheilbad', 'Mineralquelle', 'Bad Brambach'), ('Bad Elster', 'Mineral- und Moorheilbad', 'Mineralquelle, Moor', 'Bad Elster'),
      ('Bad Düben', 'Moorheilbad', 'Moor', 'Bad Duben'), ('Bad Gottleuba (Bad Gottleuba-Berggießhübel)', 'Moorheilbad', 'Moor', 'Bad Gottleuba'),
      ('Bad Lausick', 'Heilbad', 'Heilbad (Art im Verzeichnis nicht genannt)', 'Bad Lausick'),
      ('Bad Schlema (Aue-Bad Schlema)', 'Heilbad', 'Heilbad (Art im Verzeichnis nicht genannt)', 'Schlema'),
      ('Wildbach (Aue-Bad Schlema)', 'Heilbad', 'Heilbad (Art im Verzeichnis nicht genannt)', 'Aue'),
      ('Thermalbad Wiesenbad', 'Ort mit Heilquellenkurbetrieb', 'Heilquelle', 'Thermalbad Wiesenbad'),
      ('Warmbad (Wolkenstein)', 'Heilbad', 'Heilbad (Art im Verzeichnis nicht genannt)', 'Wolkenstein'),
      ('Bad Muskau', 'Ort mit Moorkurbetrieb', 'Moor', 'Bad Muskau')]
STAND = {'NI': '13.04.2026', 'BY': '02.01.2020', 'NW': '22.07.2026', 'SN': '11.09.2019'}
# Bad Brückenau steht zusätzlich als Staatsbad; Bad Tölz zusätzlich Moorheilbad
ZUSATZ = {'Bad Brückenau': 'Heilbad; Bayerisches Staatsbad (Mineral- und Moorbad)', 'Bad Tölz': 'Heilbad, Moorheilbad'}
daten = []
for land, L in (('NI', NI), ('BY', BY), ('NW', NW), ('SN', SN)):
    for n, praed, art, g in L:
        q = ort(g, land)
        if q is None:
            continue
        daten.append({'n': n, 'land': land, 'praedikat': ZUSATZ.get(n, praed), 'art': 'Mineralquelle, Moor' if n == 'Bad Brückenau' else ('Moor' if n == 'Bad Tölz' else art),
                      'lon': r2(q[0]), 'lat': r2(q[1]), 'stand': STAND[land]})
print(len(daten), 'Orte; nicht gefunden:', fehlt)
schreibe({
    'id': 'heilbaeder', 'name': 'Heilbäder und Heilquellen (Teilliste)', 'gruppe': 'Deutschland', 'typ': 'punkte', 'einheit': '',
    'legende': [['Sole', '#7ad0ff'], ['Thermal', '#ff8a5a'], ['Mineralquelle', '#c8a0ff'], ['Moor', '#8a6a3a'], ['Heilbad (Art offen)', '#d0d0d0']],
    'quellen': [
        {'t': 'Niedersächsisches Sozialministerium: Staatlich anerkannte Kur- und Erholungsorte in Niedersachsen', 'u': 'https://www.ms.niedersachsen.de/download/48949/Staatlich_anerkannte_Kur-_und_Erholungsorte_in_Niedersachsen.pdf', 'stand': '13.04.2026', 'lizenz': 'amtliches Verzeichnis (Fakten)'},
        {'t': 'Bayerisches Staatsministerium des Innern: Verzeichnis der Kurorte (Heilbäder, Staatsbäder, Orte mit Heilquellen-/Peloidkurbetrieb)', 'u': 'https://stmi.bayern.de/assets/stmi/kub/aktuelles_verzeichnis_kurorte_stand_januar_2020.pdf', 'stand': '02.01.2020', 'lizenz': 'amtliches Verzeichnis (Fakten)'},
        {'t': 'Nordrhein-Westfalen: Verzeichnis der staatlichen Anerkennungen von Kurorten, Erholungsorten und Heilbrunnen (Bekanntmachung vom 28.07.2003, laufend fortgeschrieben)', 'u': 'https://recht.nrw.de/lrmb/bekanntmachung/verzeichnis-der-staatlichen-anerkennungen-von-kurorten-erholungsorten-und/', 'stand': '22.07.2026 (letzte Änderung)', 'lizenz': 'amtliches Verzeichnis (Fakten)'},
        {'t': 'Sachsen: Staatlich anerkannte Kurorte im Freistaat Sachsen (Anlage, REVOSax)', 'u': 'https://revosax.sachsen.de/attachments/32309', 'stand': '11.09.2019', 'lizenz': 'amtliches Verzeichnis (Fakten)'},
        {'t': 'GeoNames cities1000 (Ortskoordinaten)', 'u': 'https://www.geonames.org/', 'stand': 'Paketstand reverse_geocoder', 'lizenz': 'CC BY 4.0'}],
    'hinweis': 'Niedersachsen, Bayern, Nordrhein-Westfalen und Sachsen (amtliche Landesverzeichnisse); Nordseeheil-, Kneipp- (auch Kneipp-Heilbäder) und reine heilklimatische Orte weggelassen. Ortsteile ohne eigenen GeoNames-Eintrag mit der Lage der Gemeinde. Art der Quelle nur, soweit das Prädikat sie nennt; bayerische „Heilbäder“ ohne Artangabe. Bayern-Liste Stand 2020 (neuere Fassung 2024 war nicht abrufbar). Sachsen-Liste Stand 2019. Weitere Länder (u. a. Baden-Württemberg, Hessen, Rheinland-Pfalz, Thüringen, Schleswig-Holstein, Saarland, Brandenburg, Mecklenburg-Vorpommern, Sachsen-Anhalt) fehlen (OFFEN.md).'
}, daten)
