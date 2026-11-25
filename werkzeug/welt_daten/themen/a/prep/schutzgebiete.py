"""Nationalparks (16) und Biosphärenreservate (18) in Deutschland.
Lage: Wikidata (CC0) über GitHub Abrechen2/TravStats (curated_places.*.csv, Abruf 01.09.2026). Flächen: BfN-Übersichten Stand März 2025.
Gründungs-/Anerkennungsjahre: BfN-Tabelle Biosphärenreservate 2021; Nationalparks nach lernhelfer.de (Duden Schülerlexikon) + Landesangaben.
Aufruf: python3 -I prep/schutzgebiete.py"""
import sys, os, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gemein import ROH, schreibe, r2

S = os.path.join(ROH, 'schutzgebiete')
wd = {}
for f in ('curated_places.nationalparks.csv', 'curated_places.biosphere.csv'):
    for r in csv.DictReader(open(os.path.join(S, f))):
        if r['isoCountryCode'] == 'DE':
            wd[r['name']] = (float(r['lon']), float(r['lat']), r['id'].split(':')[1])
# [Name, Wikidata-Name, Länder, Jahr, Fläche ha (BfN 3/2025), Text]
NP = [
    ['Schleswig-Holsteinisches Wattenmeer', 'Nationalpark Schleswig-Holsteinisches Wattenmeer', 'SH', '1985', 441500, 'Größter Nationalpark Deutschlands; Watt, Priele und Halligen, Teil des Weltnaturerbes Wattenmeer.'],
    ['Hamburgisches Wattenmeer', 'Nationalpark Hamburgisches Wattenmeer', 'HH', '1990', 13750, 'Watt um die Inseln Neuwerk, Scharhörn und Nigehörn vor der Elbmündung.'],
    ['Niedersächsisches Wattenmeer', 'Nationalpark Niedersächsisches Wattenmeer', 'NI', '1986', 345000, 'Watt, Salzwiesen und Ostfriesische Inseln von Dollart bis Cuxhaven.'],
    ['Vorpommersche Boddenlandschaft', 'Nationalpark Vorpommersche Boddenlandschaft', 'MV', '1990', 78600, 'Bodden, Haken und Dünen um Darß, Zingst und Westrügen; Kranichrastplatz.'],
    ['Jasmund', 'Nationalpark Jasmund', 'MV', '1990', 3070, 'Kleinster Nationalpark: Kreidefelsen und alte Buchenwälder auf Rügen.'],
    ['Müritz', 'Nationalpark Müritz', 'MV', '1990', 32200, 'Seen, Moore und Wälder der Mecklenburgischen Seenplatte.'],
    ['Unteres Odertal', 'Nationalpark Unteres Odertal', 'BB', '1995', 10323, 'Auenlandschaft an der Oder an der Grenze zu Polen.'],
    ['Harz', 'Nationalpark Harz', 'NI, ST', '1990/1994, vereinigt 2006', 24732, 'Bergwälder, Moore und Granitklippen rund um den Brocken.'],
    ['Kellerwald-Edersee', 'Nationalpark Kellerwald-Edersee', 'HE', '2004', 7688, 'Alte Rotbuchenwälder am Edersee, Teil des Weltnaturerbes Buchenwälder.'],
    ['Eifel', 'Nationalpark Eifel', 'NW', '2004', 10770, 'Buchenwälder, Bachtäler und Stauseen in der Nordeifel.'],
    ['Hainich', 'Nationalpark Hainich', 'TH', '1997', 7513, 'Großes zusammenhängendes Laubwaldgebiet, Teil des Weltnaturerbes Buchenwälder.'],
    ['Sächsische Schweiz', 'Nationalpark Sächsische Schweiz', 'SN', '1990', 9350, 'Sandstein-Tafelberge und Felsriffe im Elbsandsteingebirge.'],
    ['Hunsrück-Hochwald', 'Nationalpark Hunsrück-Hochwald', 'RP, SL', '2015', 10230, 'Wälder und Hangmoore um den Erbeskopf, länderübergreifend mit dem Saarland.'],
    ['Schwarzwald', 'Nationalpark Schwarzwald', 'BW', '2014', 10062, 'Bergmischwälder, Grinden und Karseen im Nordschwarzwald.'],
    ['Bayerischer Wald', 'Nationalpark Bayerischer Wald', 'BY', '1970', 24980, 'Erster deutscher Nationalpark; Bergwälder an der Grenze zu Tschechien.'],
    ['Berchtesgaden', 'Nationalpark Berchtesgaden', 'BY', '1978', 20804, 'Einziger Alpen-Nationalpark Deutschlands, mit Watzmann und Königssee.'],
]
BR = [
    ['Schleswig-Holsteinisches Wattenmeer und Halligen', 'Biosphärenreservat Schleswig-Holsteinisches Wattenmeer und Halligen', 'SH', 1990, 443100, True],
    ['Hamburgisches Wattenmeer', 'Biosphärenreservat Hamburgisches Wattenmeer', 'HH', 1992, 11700, True],
    ['Niedersächsisches Wattenmeer', 'Biosphärenreservat Niedersächsisches Wattenmeer', 'NI', 1992, 417131, True],
    ['Schaalsee', 'Biosphärenreservat Schaalsee', 'MV', 2000, 31000, True],
    ['Flusslandschaft Elbe', 'Biosphärenreservat Flusslandschaft Elbe', 'BB, MV, NI, SH, ST', 1997, 282250, True],
    ['Südost-Rügen', 'Biosphärenreservat Südost-Rügen', 'MV', 1991, 22800, True],
    ['Schorfheide-Chorin', 'Biosphärenreservat Schorfheide-Chorin', 'BB', 1990, 129160, True],
    ['Drömling', None, 'ST', None, 45220, False],
    ['Karstlandschaft Südharz', None, 'ST', None, 30034, False],
    ['Spreewald', 'Biosphärenreservat Spreewald', 'BB', 1991, 47624, True],
    ['Oberlausitzer Heide- und Teichlandschaft', 'Biosphärenreservat Oberlausitzer Heide- und Teichlandschaft', 'SN', 1996, 30102, True],
    ['Thüringer Wald', 'Biosphärenreservat Thüringer Wald', 'TH', 1979, 33672, True],
    ['Rhön', 'Biosphärenreservat Rhön', 'BY, HE, TH', 1991, 243323, True],
    ['Bliesgau', 'Biosphärenreservat Bliesgau', 'SL', 2009, 36152, True],
    ['Pfälzerwald-Nordvogesen', 'Biosphärenreservat Pfälzerwald-Nordvogesen', 'RP', 1992, 178496, True],
    ['Schwäbische Alb', 'Biosphärengebiet Schwäbische Alb', 'BW', 2009, 85269, True],
    ['Schwarzwald', 'Biosphärengebiet Schwarzwald', 'BW', 2017, 63236, True],
    ['Berchtesgadener Land', 'Biosphärenreservat Berchtesgadener Land', 'BY', 1990, 83984, True],
]
daten = []
for n, w, l, j, f, t in NP:
    lo, la, q = wd[w]
    daten.append({'art': 'Nationalpark', 'n': 'Nationalpark ' + n, 'land': l, 'jahr': j, 'ha': f, 'lon': r2(lo), 'lat': r2(la), 'wd': q, 'text': t})
for n, w, l, j, f, u in BR:
    lo, la, q = wd[w] if w else (None, None, None)
    daten.append({'art': 'Biosphärenreservat', 'n': 'Biosphärenreservat ' + n, 'land': l, 'jahr': j, 'ha': f, 'unesco': u,
                  'lon': r2(lo) if lo is not None else None, 'lat': r2(la) if la is not None else None, 'wd': q})
print(len(daten), 'Gebiete;', 'ohne Lage:', [d['n'] for d in daten if d['lon'] is None])
schreibe({
    'id': 'schutzgebiete', 'name': 'Nationalparks und Biosphärenreservate', 'gruppe': 'Deutschland', 'typ': 'punkte', 'einheit': 'ha',
    'legende': [['Nationalpark', '#4ad07a'], ['Biosphärenreservat (UNESCO)', '#5ab8e8'], ['Biosphärenreservat (nur national)', '#8ab0c8']],
    'quellen': [
        {'t': 'Bundesamt für Naturschutz: Nationalparke in Deutschland (Übersicht, Stand März 2025) – Flächen', 'u': 'https://www.bfn.de/sites/default/files/2025-03/Nationalparke2025_pac.pdf', 'stand': 'März 2025', 'lizenz': 'amtliche Angaben (Fakten), Quelle BfN'},
        {'t': 'Bundesamt für Naturschutz: Biosphärenreservate in Deutschland (Übersicht, Stand März 2025) – Flächen', 'u': 'https://www.bfn.de/sites/default/files/2025-03/Biosph%C3%A4renreservate2025_pac.pdf', 'stand': 'März 2025', 'lizenz': 'amtliche Angaben (Fakten), Quelle BfN'},
        {'t': 'Bundesamt für Naturschutz: Tabelle Biosphärenreservate (BR_Tab_01_2021) – Länder, Jahr der UNESCO-Anerkennung', 'u': 'https://www.bfn.de/sites/default/files/2021-07/BR_Tab_01_2021_bf.pdf', 'stand': '2021', 'lizenz': 'amtliche Angaben (Fakten), Quelle BfN'},
        {'t': 'Duden Learnattack / lernhelfer.de Schülerlexikon: Nationalparks (Gründungsjahre, Länder); Schwarzwald 2014 und Hunsrück-Hochwald 2015 nach Land Baden-Württemberg („Zehn Jahre Nationalpark Schwarzwald“) und Wikipedia', 'u': 'https://www.lernhelfer.de/schuelerlexikon/biologie/artikel/nationalparks', 'stand': 'abgerufen 11/2026', 'lizenz': 'nur Jahreszahlen (Fakten) übernommen'},
        {'t': 'Wikidata (Koordinaten, Q-Nummern), abgefragt am 01.09.2026, gespeichert in GitHub Abrechen2/TravStats (backend/src/seedData/curated_places.nationalparks.csv, curated_places.biosphere.csv)', 'u': 'https://github.com/Abrechen2/TravStats', 'stand': '01.09.2026', 'lizenz': 'CC0 1.0'}],
    'hinweis': 'Lagepunkt = Wikidata-Koordinate (ein Punkt im Gebiet bzw. Verwaltungssitz-Nähe), keine Grenze. Drömling und Karstlandschaft Südharz ohne Lage (in Wikidata-Auszug nicht enthalten) und laut BfN 2021 nicht UNESCO-anerkannt; Drömling-Fläche 2025 größer als 2021. Naturparks fehlen (siehe OFFEN.md).'
}, daten)
