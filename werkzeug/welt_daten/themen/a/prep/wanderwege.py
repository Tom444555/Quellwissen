"""Bekannte deutsche Fernwanderwege als schematische Linien über benannte Orte.
Ortskoordinaten: GeoNames cities1000 (CC BY 4.0), Kopie aus pip-Paket reverse_geocoder (roh/wege/geonames_cities1000_rg.csv).
Länge, Start und Ziel: je Weg benannte Quelle (siehe QUELLEN.md). Aufruf: python3 -I prep/wanderwege.py"""
import sys, os, csv, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gemein import ROH, schreibe, r2

def norm(s):
    s = s.replace('ä', 'a').replace('ö', 'o').replace('ü', 'u').replace('Ä', 'A').replace('Ö', 'O').replace('Ü', 'U').replace('ß', 'ss')
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
GN = {}
for r in csv.DictReader(open(os.path.join(ROH, 'wege', 'geonames_cities1000_rg.csv'), encoding='utf-8')):
    if r['cc'] in ('DE', 'CH'):
        GN.setdefault(norm(r['name']), []).append((float(r['lon']), float(r['lat'])))
def kand(n):
    k = norm(n)
    for kk in (k, k.replace('ue', 'u').replace('oe', 'o').replace('ae', 'a')):
        if kk in GN:
            return GN[kk]
    raise KeyError(n)


def orte(namen):
    """Mehrdeutige Namen: Kandidat, der dem Schwerpunkt der eindeutigen Orte des Wegs am nächsten liegt."""
    ks = []
    for n in namen:   # 'Name@lon,lat' = Hinweis zur Auswahl unter gleichnamigen Orten
        if '@' in n:
            n, h = n.split('@'); hx, hy = map(float, h.split(','))
            ks.append([min(kand(n), key=lambda q: (q[0] - hx) ** 2 + (q[1] - hy) ** 2)])
        else:
            ks.append(kand(n))
    ein = [k[0] for k in ks if len(k) == 1]
    cx = sum(x for x, y in ein) / len(ein); cy = sum(y for x, y in ein) / len(ein)
    return [min(k, key=lambda q: (q[0] - cx) ** 2 + (q[1] - cy) ** 2) for k in ks]

# [Name, km, Länder, Rang, Kurztext, [Wegpunkte (Anzeige-Name, GeoNames-Name)], Quelle-Kürzel, Hinweis]
W = [
 ['Rennsteig', 168.3, 'TH, BY', 1, 'Ältester bekannter Kammweg Deutschlands über Thüringer Wald, Schiefergebirge und Frankenwald.',
  [('Hörschel (Eisenach)', 'Eisenach'), ('Ruhla', 'Ruhla'), ('Oberhof', 'Oberhof'), ('Schmiedefeld am Rennsteig', 'Schmiedefeld am Rennsteig'), ('Neuhaus am Rennsteig', 'Neuhaus am Rennweg'), ('Blankenstein', 'Blankenstein')], 'ruhla', 'Orte laut Stadt Ruhla; Hörschel als Punkt Eisenach; Lehesten fehlt in GeoNames-Auszug.'],
 ['Westweg', 280, 'BW', 1, 'Ältester Fernwanderweg im Schwarzwald, von Nord nach Süd über die Höhen.',
  [('Pforzheim', 'Pforzheim'), ('Dobel', 'Dobel'), ('Forbach', 'Forbach'), ('Freudenstadt', 'Freudenstadt'), ('Hausach', 'Hausach'), ('Schonach', 'Schonach im Schwarzwald'), ('Titisee', 'Titisee-Neustadt'), ('Hinterzarten', 'Hinterzarten'), ('Kandern', 'Kandern'), ('Basel', 'Basel')], 'westweg', 'Orte laut Factsheet (Tourist-Infos am Weg, West-/Ostvariante gemischt).'],
 ['Rheinsteig', 320, 'HE, RP, NW', 1, 'Über die Höhen am rechten Rheinufer durch Rheingau und Mittelrheintal.',
  [('Wiesbaden-Biebrich', 'Wiesbaden'), ('Rüdesheim', 'Rudesheim am Rhein'), ('Kaub', 'Kaub'), ('St. Goarshausen', 'Sankt Goarshausen'), ('Lahnstein', 'Lahnstein'), ('Koblenz-Ehrenbreitstein', 'Koblenz'), ('Neuwied', 'Neuwied'), ('Linz am Rhein', 'Linz am Rhein'), ('Königswinter', 'Konigswinter'), ('Bonn', 'Bonn')], 'wikivoyage+adac', 'Zwischenorte am rechten Rheinufer nach Lage gesetzt (nicht einzeln belegt).'],
 ['Saar-Hunsrück-Steig', 415, 'SL, RP', 1, 'Von der Mosel bei Perl über Saarschleife und Hunsrück an den Rhein; Abstecher nach Trier.',
  [('Perl', 'Perl'), ('Mettlach', 'Mettlach'), ('Weiskirchen', 'Weiskirchen'), ('Idar-Oberstein', 'Idar-Oberstein'), ('Morbach', 'Morbach'), ('Boppard', 'Boppard')], 'shs', 'Start, Ziel, Idar-Oberstein und Länge laut Projektbüro; Mettlach, Weiskirchen, Morbach nach Lage gesetzt. Zubringer Trier nicht gezeichnet.'],
 ['Goldsteig', 660, 'BY', 1, 'Längster Qualitätsweg Deutschlands durch Oberpfälzer und Bayerischen Wald.',
  [('Marktredwitz', 'Marktredwitz'), ('Bärnau', 'Barnau'), ('Waldmünchen', 'Waldmunchen'), ('Furth im Wald', 'Furth im Wald'), ('Bayerisch Eisenstein', 'Bayerisch Eisenstein'), ('Mauth', 'Mauth'), ('Passau', 'Passau')], 'wikivoyage+adac', 'Zwischenorte nach Lage gesetzt (Nordvariante), nicht einzeln belegt.'],
 ['Malerweg', 116, 'SN', 2, 'Rundweg durch das Elbsandsteingebirge zu Bastei, Schrammsteinen, Festung Königstein und Pfaffenstein.',
  [('Pirna-Liebethal', 'Pirna'), ('Lohmen', 'Lohmen'), ('Hohnstein', 'Hohnstein'), ('Bad Schandau', 'Bad Schandau'), ('Königstein', 'Konigstein'), ('Pirna', 'Pirna')], 'malerweg', 'Länge und Höhepunkte laut Tourismusverband; Orte nach Lage gesetzt.'],
 ['Heidschnuckenweg', 223, 'HH, NI', 2, 'Durch die Lüneburger Heide von Hamburg nach Celle.',
  [('Hamburg', 'Hamburg'), ('Undeloh', 'Undeloh'), ('Bispingen', 'Bispingen'), ('Celle', 'Celle')], 'adac', 'Start Hamburg-Fischbek liegt südwestlich des gezeichneten Punkts; Zwischenorte nach Lage.'],
 ['Albsteig (Schwäbische-Alb-Nordrand-Weg)', 350, 'BY, BW', 2, 'Am Albtrauf entlang von Donauwörth bis Tuttlingen.',
  [('Donauwörth', 'Donauwoerth'), ('Aalen', 'Aalen'), ('Heubach', 'Heubach'), ('Geislingen an der Steige', 'Geislingen an der Steige'), ('Bad Urach', 'Bad Urach'), ('Albstadt', 'Albstadt'), ('Tuttlingen', 'Tuttlingen')], 'adac', 'Zwischenorte nach Lage gesetzt.'],
 ['Eifelsteig', 313, 'NW, RP', 2, 'Von Aachen-Kornelimünster durch die Eifel bis Trier.',
  [('Aachen-Kornelimünster', 'Aachen'), ('Monschau', 'Monschau'), ('Blankenheim', 'Blankenheim'), ('Gerolstein', 'Gerolstein'), ('Daun', 'Daun'), ('Manderscheid', 'Manderscheid@6.81,50.1'), ('Trier', 'Trier')], 'wikivoyage+adac', 'Zwischenorte nach Lage gesetzt.'],
 ['Rothaarsteig', 158, 'NW, HE', 2, 'Über den Kamm des Rothaargebirges von Brilon nach Dillenburg.',
  [('Brilon', 'Brilon'), ('Winterberg', 'Winterberg'), ('Dillenburg', 'Dillenburg')], 'adac', 'Winterberg nach Lage gesetzt.'],
 ['Kammweg Erzgebirge–Vogtland', 288, 'SN, TH, BY', 2, 'Über den Kamm von Erzgebirge und Vogtland bis zum Rennsteig-Ende in Blankenstein.',
  [('Altenberg-Geising', 'Altenberg'), ('Oberwiesenthal', 'Kurort Oberwiesenthal'), ('Johanngeorgenstadt', 'Johanngeorgenstadt'), ('Klingenthal', 'Klingenthal'), ('Blankenstein', 'Blankenstein')], 'adac', 'Zwischenorte nach Lage gesetzt.'],
 ['Hochrhöner', 180, 'BY, HE, TH', 3, 'Durch die Rhön von Bad Kissingen nach Bad Salzungen.',
  [('Bad Kissingen', 'Bad Kissingen'), ('Bad Salzungen', 'Bad Salzungen')], 'wikivoyage+adac', 'Nur Start und Ziel; Länge je nach Variante 120–180 km.'],
]
daten = []
for n, km, l, rg, t, pts, q, h in W:
    p = [[r2(lo), r2(la), anz] for (anz, gn), (lo, la) in zip(pts, orte([g for a, g in pts]))]
    daten.append({'n': n, 'km': km, 'land': l, 'rang': rg, 'text': t, 'schema': True, 'q': q, 'hinweis': h, 'p': p})
print(len(daten), 'Wege')
Q = {'ruhla': {'t': 'Stadt Ruhla: Rennsteig – Fakten', 'u': 'https://www.ruhla.de/en/tourism//facts.html', 'stand': 'abgerufen 11/2026'},
     'westweg': {'t': 'Top Trails of Germany: Westweg Factsheet', 'u': 'https://top-trails-of-germany.de/fileadmin/documents/FactSheets/Westweg_Factsheet_ausfA__hrlich.pdf', 'stand': 'abgerufen 11/2026'},
     'wikivoyage+adac': {'t': 'Wikivoyage „Wandern in Deutschland“ und ADAC „Die 16 schönsten Wanderwege in Deutschland“', 'u': 'https://de.wikivoyage.org/wiki/Wandern_in_Deutschland ; https://www.adac.de/reise-freizeit/tipps/deutschland/schoenste-wanderwege-deutschland/', 'stand': 'abgerufen 11/2026'},
     'adac': {'t': 'ADAC: Die 16 schönsten Wanderwege in Deutschland', 'u': 'https://www.adac.de/reise-freizeit/tipps/deutschland/schoenste-wanderwege-deutschland/', 'stand': 'abgerufen 11/2026'},
     'shs': {'t': 'Projektbüro Saar-Hunsrück-Steig: Infos zu den Etappen', 'u': 'https://saar-hunsrueck-steig.de/en/legs/infos', 'stand': 'abgerufen 11/2026'},
     'malerweg': {'t': 'Tourismusverband Sächsische Schweiz: Malerweg', 'u': 'https://www.saechsische-schweiz.de/en/vacation/hiking/malerweg-hiking-path', 'stand': 'abgerufen 11/2026'}}
schreibe({
    'id': 'wanderwege', 'name': 'Fernwanderwege', 'gruppe': 'Deutschland', 'typ': 'linien', 'einheit': 'km',
    'legende': [['Fernwanderweg (schematisch)', '#ffb86a']],
    'quellen_wege': Q,
    'quellen': [{'t': 'GeoNames cities1000 (Ortskoordinaten), Kopie im pip-Paket reverse_geocoder', 'u': 'https://www.geonames.org/', 'stand': 'Paketstand', 'lizenz': 'CC BY 4.0 (GeoNames)'}] +
               [dict(v, lizenz='nur Länge/Start/Ziel/Orte (Fakten) übernommen') for v in Q.values()],
    'hinweis': 'Schematisch (schema:true): gerade Verbindungen zwischen Ortsmittelpunkten, nicht der echte Wegverlauf. p = [lon, lat, Ortsname]. Längen laut Quelle q (Varianten möglich). Europäische Fernwanderwege (E1 usw.) fehlen, siehe OFFEN.md.'
}, daten)
