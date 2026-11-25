"""Meeresströmungen (schematisch) und Windgürtel (schematisch nach Breitengraden).
Namen/Auswahl: NOAA (noaa.gov/node/10499, 25 windgetriebene Oberflächenströmungen) + Ergänzungen aus Wikipedia „Ocean current“.
Warm/kalt nach der NOAA-Regel: warm = trägt Wasser aus Äquatornähe polwärts, kalt = trägt kaltes Wasser äquatorwärts;
äquatoriale Ströme warm; west-östliche Ströme der mittleren Breiten ohne eindeutige Angabe = 'neutral'.
Wegpunkte selbst gesetzt (schema:true), nur als Richtungsskizze. Aufruf: python3 -I prep/stroemungen.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gemein import schreibe

# [Name, Art, Meer, Rang, Kurztext, Wegpunkte in Fließrichtung]
S = [
 ['Golfstrom', 'warm', 'Atlantik', 1, 'Warme Strömung entlang der US-Ostküste nach Nordosten; Teil des Nordatlantikwirbels.', [[-80, 25], [-79.5, 30], [-75, 35], [-70, 38], [-60, 40], [-50, 41.5]]],
 ['Nordatlantikstrom', 'warm', 'Atlantik', 1, 'Fortsetzung des Golfstroms nach Nordosten; mildert das Klima West- und Nordeuropas.', [[-50, 42], [-40, 46], [-30, 50], [-20, 53], [-10, 56]]],
 ['Norwegischer Strom', 'warm', 'Atlantik', 2, 'Führt warmes Atlantikwasser entlang der norwegischen Küste ins Nordmeer.', [[-8, 58], [0, 62], [8, 65], [14, 69], [20, 72]]],
 ['Kanarenstrom', 'kalt', 'Atlantik', 1, 'Kühle Strömung vor Nordwestafrika nach Süden.', [[-15, 40], [-14, 35], [-17, 28], [-19, 21], [-21, 15]]],
 ['Nordäquatorialstrom (Atlantik)', 'warm', 'Atlantik', 2, 'Fließt nördlich des Äquators von Ost nach West.', [[-20, 14], [-35, 15], [-50, 15], [-62, 15]]],
 ['Äquatorialer Gegenstrom (Atlantik)', 'warm', 'Atlantik', 3, 'Fließt zwischen den beiden Äquatorialströmen nach Osten.', [[-45, 6], [-30, 7], [-18, 6]]],
 ['Guineastrom', 'warm', 'Atlantik', 3, 'Warme Strömung im Golf von Guinea nach Osten.', [[-15, 6], [-8, 4.5], [0, 4], [8, 3.5]]],
 ['Südäquatorialstrom (Atlantik)', 'warm', 'Atlantik', 2, 'Fließt am und südlich des Äquators von Ost nach West.', [[5, -2], [-10, -3], [-25, -5], [-34, -7]]],
 ['Brasilstrom', 'warm', 'Atlantik', 1, 'Warme Strömung entlang der Küste Brasiliens nach Süden.', [[-35, -10], [-38, -18], [-42, -24], [-48, -30], [-53, -36]]],
 ['Benguelastrom', 'kalt', 'Atlantik', 1, 'Kalte Strömung vor Südwestafrika nach Norden; Grund für die Küstenwüste Namib.', [[15, -34], [12, -28], [11, -22], [9, -15], [5, -8]]],
 ['Südatlantikstrom', 'neutral', 'Atlantik', 3, 'Südlicher Ast des Südatlantikwirbels nach Osten.', [[-50, -38], [-35, -38], [-20, -37], [-5, -36], [10, -35]]],
 ['Falklandstrom', 'kalt', 'Atlantik', 2, 'Kalte Strömung vor Argentinien nach Norden.', [[-62, -55], [-58, -50], [-56, -45], [-55, -39]]],
 ['Labradorstrom', 'kalt', 'Atlantik', 1, 'Kalte Strömung vor Labrador nach Süden; bringt Eisberge bis Neufundland.', [[-62, 62], [-58, 56], [-53, 50], [-50, 45]]],
 ['Ostgrönlandstrom', 'kalt', 'Atlantik', 2, 'Kalte Strömung aus dem Nordpolarmeer entlang Ostgrönlands nach Süden.', [[-15, 78], [-20, 72], [-27, 67], [-36, 63], [-43, 60]]],
 ['Kuroshio', 'warm', 'Pazifik', 1, 'Warme Strömung vor Japan nach Nordosten; Gegenstück zum Golfstrom.', [[122, 22], [124, 26], [130, 30], [136, 33], [142, 35.5], [150, 36]]],
 ['Oyashio', 'kalt', 'Pazifik', 2, 'Kalte Strömung aus dem Beringmeer vor den Kurilen und Nordjapan nach Süden.', [[165, 58], [160, 52], [152, 46], [146, 42]]],
 ['Nordpazifikstrom', 'neutral', 'Pazifik', 2, 'Fließt in mittleren Breiten von Japan nach Osten über den Pazifik.', [[152, 38], [170, 41], [-170, 43], [-150, 45], [-135, 46]]],
 ['Alaskastrom', 'warm', 'Pazifik', 2, 'Relativ warme Strömung im Golf von Alaska nach Nordwesten.', [[-135, 48], [-138, 54], [-145, 58], [-152, 58]]],
 ['Kalifornienstrom', 'kalt', 'Pazifik', 1, 'Kühle Strömung vor der Westküste Nordamerikas nach Süden.', [[-128, 48], [-125, 40], [-120, 33], [-115, 25], [-110, 20]]],
 ['Nordäquatorialstrom (Pazifik)', 'warm', 'Pazifik', 2, 'Fließt nördlich des Äquators von Ost nach West.', [[-110, 15], [-140, 14], [-170, 13], [160, 13], [130, 14]]],
 ['Äquatorialer Gegenstrom (Pazifik)', 'warm', 'Pazifik', 3, 'Fließt zwischen den Äquatorialströmen nach Osten.', [[130, 6], [160, 6], [-170, 7], [-130, 7], [-90, 6]]],
 ['Südäquatorialstrom (Pazifik)', 'warm', 'Pazifik', 2, 'Fließt am und südlich des Äquators von Ost nach West.', [[-82, -3], [-100, -3], [-130, -5], [-160, -8], [170, -10], [150, -12]]],
 ['Humboldtstrom (Perustrom)', 'kalt', 'Pazifik', 1, 'Kalte Strömung vor Chile und Peru nach Norden; sehr fischreich.', [[-75, -45], [-74, -35], [-72, -25], [-77, -15], [-82, -5]]],
 ['Ostaustralstrom', 'warm', 'Pazifik', 2, 'Warme Strömung vor der Ostküste Australiens nach Süden.', [[155, -15], [154, -25], [153.5, -30], [152, -35], [152, -38]]],
 ['Südpazifikstrom', 'neutral', 'Pazifik', 3, 'Südlicher Ast des Südpazifikwirbels nach Osten.', [[160, -42], [175, -45], [-160, -45], [-120, -43], [-85, -42]]],
 ['Mosambikstrom', 'warm', 'Indik', 2, 'Warme Strömung in der Straße von Mosambik nach Süden.', [[42, -12], [40, -17], [36, -22], [35, -25]]],
 ['Agulhasstrom', 'warm', 'Indik', 1, 'Warme, schnelle Strömung vor Südostafrika nach Südwesten.', [[35, -26], [32, -30], [28, -34], [22, -37]]],
 ['Südäquatorialstrom (Indik)', 'warm', 'Indik', 2, 'Fließt südlich des Äquators von Ost nach West.', [[100, -12], [80, -12], [60, -14], [50, -15]]],
 ['Südindischer Strom', 'neutral', 'Indik', 3, 'Südlicher Ast des Indikwirbels nach Osten.', [[20, -40], [50, -40], [80, -40], [110, -38]]],
 ['Westaustralstrom', 'kalt', 'Indik', 2, 'Kühle Strömung vor Westaustralien nach Norden.', [[112, -36], [109, -30], [106, -24], [100, -18]]],
 ['Somalistrom', 'warm', 'Indik', 3, 'Strömung vor Somalia; kehrt sich mit dem Monsun um (hier Sommerrichtung nach Nordosten).', [[42, -2], [45, 3], [50, 8], [53, 12]]],
 ['Antarktischer Zirkumpolarstrom (Westwinddrift)', 'kalt', 'Südpolarmeer', 1, 'Umfließt die Antarktis von West nach Ost; die wasserreichste Meeresströmung.', [[-180, -55], [-150, -57], [-120, -58], [-90, -58], [-65, -58], [-40, -52], [-10, -50], [20, -48], [50, -48], [80, -50], [110, -52], [140, -53], [170, -55], [180, -55]]],
 ['Antarktischer Küstenstrom (Ostwinddrift)', 'kalt', 'Südpolarmeer', 3, 'Fließt dicht an der Antarktis von Ost nach West.', [[180, -72], [150, -67], [120, -65], [90, -65], [60, -66], [30, -69], [0, -70], [-30, -73], [-60, -70], [-90, -72], [-120, -73], [-150, -76], [-180, -72]]],
]


def teile(p):
    """An der Datumsgrenze (Sprung > 180°) aufteilen."""
    out, cur = [], [p[0]]
    for a, b in zip(p, p[1:]):
        if abs(b[0] - a[0]) > 180:
            out.append(cur); cur = [b]
        else:
            cur.append(b)
    out.append(cur)
    return [c for c in out if len(c) >= 2] or [p]


daten = [{'n': n, 'art': a, 'meer': m, 'rang': r, 'text': t, 'schema': True, 'p': teile(p)} for n, a, m, r, t, p in S]
schreibe({
    'id': 'meeresstroemungen', 'name': 'Meeresströmungen', 'gruppe': 'Natur', 'typ': 'linien', 'einheit': '',
    'legende': [['warme Strömung', '#ff6a4a'], ['kalte Strömung', '#4aa8ff'], ['ohne klare Zuordnung', '#c8d0d8']],
    'quellen': [
        {'t': 'NOAA: Ocean currents – Karte der 25 großen windgetriebenen Oberflächenströmungen; Regel „warm = rot, kalt = blau, trägt kaltes Wasser zum Äquator“', 'u': 'https://noaa.gov/node/10499', 'stand': 'abgerufen 11/2026', 'lizenz': 'gemeinfrei (US-Bundesbehörde)'},
        {'t': 'NOAA Ocean Service: What are the trade winds?', 'u': 'https://oceanservice.noaa.gov/facts/tradewinds.html', 'stand': 'abgerufen 11/2026', 'lizenz': 'gemeinfrei'},
        {'t': 'Wikipedia (en): Ocean current – Liste der Strömungen je Ozean (Ergänzungen Falkland-, Guinea-, Mosambik-, Somali-, Agulhasstrom; dort als warm/kalt markierte)', 'u': 'https://www.wikiwand.com/en/Ocean_current', 'stand': 'abgerufen 11/2026', 'lizenz': 'CC BY-SA 4.0 (nur Fakten übernommen, kein Text)'}],
    'hinweis': 'Schematisch: Verläufe selbst aus Wegpunkten gezeichnet (schema:true), nur zur Richtungsanzeige; Pfeilspitze am letzten Punkt. Linien an der Datumsgrenze geteilt (p = Liste von Teilstücken).'
}, daten)

# Windgürtel: Bänder nach Breite (Nord und Süd), Richtung als Windrichtung (woher), Pfeilwinkel = wohin (0 = Nord, 90 = Ost)
W = [
    ['Innertropische Konvergenzzone (Kalmen)', -5, 5, None, None, 1, 'Etwa 10° breiter Gürtel um den Äquator, wo die Passate zusammentreffen; schwache Winde, aufsteigende Luft, viel Regen. Wandert mit dem Sonnenstand.'],
    ['Nordost-Passat', 5, 30, 'aus Nordost', 225, 1, 'Beständiger Wind zwischen den Rossbreiten und dem Äquator, auf der Nordhalbkugel aus Nordost.'],
    ['Südost-Passat', -30, -5, 'aus Südost', 315, 1, 'Beständiger Wind zwischen den Rossbreiten und dem Äquator, auf der Südhalbkugel aus Südost.'],
    ['Rossbreiten (Nord)', 25, 35, None, None, 2, 'Hochdruckgürtel um 30° Breite: absinkende Luft, wenig Wind und wenig Regen; hier liegen viele Wüsten.'],
    ['Rossbreiten (Süd)', -35, -25, None, None, 2, 'Hochdruckgürtel um 30° Breite: absinkende Luft, wenig Wind und wenig Regen.'],
    ['Westwindzone (Nord)', 35, 60, 'aus West bis Südwest', 45, 1, 'Vorherrschende Westwinde der mittleren Breiten mit wandernden Tiefs; Deutschland liegt in dieser Zone.'],
    ['Westwindzone (Süd)', -60, -35, 'aus West bis Nordwest', 135, 1, 'Vorherrschende Westwinde der mittleren Breiten; über dem offenen Südmeer besonders stark („Brüllende Vierziger“).'],
    ['Polare Ostwinde (Nord)', 60, 90, 'aus Ost bis Nordost', 250, 2, 'Kalte Winde, die vom polaren Hoch nach Süden und Westen wehen.'],
    ['Polare Ostwinde (Süd)', -90, -60, 'aus Ost bis Südost', 290, 2, 'Kalte Winde, die vom antarktischen Hoch nach Norden und Westen wehen.'],
]
# Monsungebiete nach IPCC AR6 WGI Annex V (Namen); Umrisse als grobe Rechtecke selbst gesetzt [lon_min, lat_min, lon_max, lat_max]
M = [
    ['Südasiatischer Monsun', [65, 5, 100, 30], 'Sommer feucht (Südwestmonsun), Winter trocken (Nordostmonsun).'],
    ['Ostasiatischer Monsun', [105, 20, 135, 45], 'Feuchte Sommer mit Südwinden, trockene, kalte Winter mit Nordwinden.'],
    ['Westafrikanischer Monsun', [-18, 5, 15, 18], 'Regenzeit im Nordsommer, wenn feuchte Luft vom Golf von Guinea landeinwärts strömt.'],
    ['Australisch-maritimer Monsun', [95, -20, 150, 0], 'Regenzeit im Südsommer (Dezember bis März) über Nordaustralien und Indonesien.'],
    ['Nordamerikanischer Monsun', [-115, 18, -103, 35], 'Sommerliche Gewitterzeit in Nordwestmexiko und im Südwesten der USA.'],
    ['Südamerikanischer Monsun', [-70, -25, -40, -5], 'Regenzeit im Südsommer über Zentralbrasilien.'],
]
schreibe({
    'id': 'windguertel', 'name': 'Windgürtel und Monsun', 'gruppe': 'Natur', 'typ': 'flaechen', 'einheit': '',
    'felder_baender': ['name', 'lat_von', 'lat_bis', 'richtung', 'pfeil_wohin_grad', 'rang', 'text'],
    'felder_monsun': ['name', 'rechteck_lonmin_latmin_lonmax_latmax', 'text'],
    'legende': [['Passate', '#ffd27a'], ['Westwinde', '#7ad0ff'], ['Polare Ostwinde', '#c8e0ff'], ['Kalmen/Rossbreiten (windschwach)', '#a0a0a0'], ['Monsungebiet', '#5ad08a']],
    'quellen': [
        {'t': 'NOAA JetStream: Global Atmospheric Circulations (Hochdruck um 30°, Westwinde 35°–60°, Tiefdruck am Äquator und bei 50°–60°)', 'u': 'https://www.noaa.gov/jetstream/global-circulations', 'stand': 'abgerufen 11/2026', 'lizenz': 'gemeinfrei'},
        {'t': 'NOAA Ocean Service: What are the trade winds? (Passate bis etwa 30°, Kalmen/ITCZ etwa 5° N bis 5° S, Richtungen je Halbkugel)', 'u': 'https://oceanservice.noaa.gov/facts/tradewinds.html', 'stand': 'abgerufen 11/2026', 'lizenz': 'gemeinfrei'},
        {'t': 'IPCC AR6 WGI, Annex V: Monsoons (Gliederung der regionalen Monsune)', 'u': 'https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Annex_V.pdf', 'stand': '2021', 'lizenz': 'nur Namen/Gliederung übernommen (Fakten); Umrisse selbst gesetzt'}],
    'hinweis': 'Schematisch (schema:true): feste Breitenbänder, in Wirklichkeit wandern sie mit den Jahreszeiten um etwa 5–10°. Grenzen der polaren Ostwinde (60°) und Rossbreiten-Breite (±5° um 30°) als übliche Lehrbuchwerte gesetzt. Monsun-Rechtecke nur grobe Lage.',
    'schema': True,
    'daten_monsun': M
}, W)
