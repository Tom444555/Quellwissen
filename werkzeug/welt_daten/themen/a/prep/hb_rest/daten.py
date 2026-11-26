# -*- coding: utf-8 -*-
"""Staatlich anerkannte Heilbäder / Orte mit Heilmittel-Prädikat in BW, RP, SL, SH, MV.

Hauptquelle (alle fünf Länder): Senatsverwaltung für Finanzen Berlin,
"Übersicht der anerkannten Heilbäder- und Kurorte (zu § 35 Abs. 1 Satz 2 LBhVO)",
Anlage zum Rundschreiben IV Nr. 42/2026, Stand 10/2026 (amtliches Beihilfe-Verzeichnis,
länderübergreifend). Für RP gegengeprüft mit der Stellungnahme der Landesregierung RP (2018).
Für SH wurden die Prädikate aus dem Änderungsteil des Rundschreibens (09.10.2026) übernommen,
weil die Tabellen-Anlage bei diesen Orten nur das erste Prädikat zeigt.

Tupel: (Ortsname wie im Verzeichnis, Prädikat wörtlich, Art-Kurzform, GeoNames-Name der Gemeinde)
Art-Kurzform: steht das Heilmittel im Prädikat (z. B. "(Sole-)Heilbad"), ist es daraus übernommen;
sonst ergänzt aus allgemeiner Kenntnis -> diese Orte stehen in ART_ERGAENZT (nicht amtlich belegt).
Nicht aufgenommen: reine Seebäder, Luftkurorte, Erholungsorte, Kneippkurorte, heilklimatische Kurorte.
Kneipp-/Felke-Heilbäder und Zweifelsfälle stehen getrennt in GRENZFAELLE.
"""

BW = [
    ('Röthardt (Aalen)', 'Ort mit Heilstollen-Kurbetrieb', 'Heilstollen', 'Aalen'),
    ('Baden-Baden', 'Heilbad', 'Thermal', 'Baden-Baden'),
    ('Badenweiler', 'Heilbad', 'Thermal', 'Badenweiler'),
    ('Bad Bellingen', '(Mineral-)Heilbad', 'Mineralquelle', 'Bad Bellingen'),
    ('Beuren', 'Ort mit Heilquellenkurbetrieb', 'Heilquelle', 'Beuren'),
    ('Bad Boll', 'Ort mit Heilquellenkurbetrieb', 'Heilquelle', 'Bad Boll'),
    ('Bad Buchau', '(Thermal- und Moor-)Heilbad', 'Thermal, Moor', 'Bad Buchau'),
    ('Bad Ditzenbach', 'Heilbad', 'Mineralquelle', 'Bad Ditzenbach'),
    ('Bad Dürrheim', '(Sole-)Heilbad, heilklimatischer Kurort u. Kneippkurort', 'Sole', 'Bad Durrheim'),
    ('Freiburg, Ortsbereich „An den Heilquellen“', 'Ort mit Heilquellen-Kurbetrieb', 'Heilquelle', 'Freiburg'),
    ('Bad Rotenfels (Gaggenau)', 'Ort mit Heilquellen-Kurbetrieb', 'Heilquelle', 'Gaggenau'),
    ('Bad Imnau (Haigerloch)', 'Ort mit Heilquellen-Kurbetrieb', 'Heilquelle', 'Haigerloch'),
    ('Bad Herrenalb', 'Heilbad u. heilklimatischer Kurort', 'Thermal', 'Bad Herrenalb'),
    ('Bad Krozingen', 'Heilbad', 'Thermal', 'Bad Krozingen'),
    ('Bad Liebenzell', 'Heilbad', 'Thermal', 'Bad Liebenzell'),
    ('Hoheneck (Ludwigsburg)', 'Ort mit Heilquellenkurbetrieb', 'Heilquelle', 'Ludwigsburg'),
    ('Bad Mergentheim', 'Heilbad', 'Mineralquelle', 'Bad Mergentheim'),
    ('Bad Sebastiansweiler (Mössingen)', 'Ort mit Heilquellen-Kurbetrieb', 'Heilquelle', 'Mossingen'),
    ('Münstertal/Schwarzwald', 'Ort mit Heilstollen Kurbetrieb', 'Heilstollen', 'Munstertal/Schwarzwald'),
    ('Bad Peterstal-Griesbach', '(Mineral- und Moor-)Heilbad, Kneippkurort', 'Mineralquelle, Moor', 'Bad Peterstal-Griesbach'),
    ('Bad Rappenau', '(Sole-)Heilbad', 'Sole', 'Bad Rappenau'),
    ('Bad Säckingen', 'Heilbad', 'Thermal', 'Bad Sackingen'),
    ('Bad Saulgau', 'Heilbad', 'Thermal', 'Bad Saulgau'),
    ('Bad Mingolsheim (Bad Schönborn)', 'Heilbad', 'Schwefel', 'Bad Schonborn'),
    ('Langenbrücken (Bad Schönborn)', 'Ort mit Heilquellenkurbetrieb', 'Heilquelle', 'Bad Schonborn'),
    ('Stuttgart (Berg, Bad Cannstatt)', 'Ort mit Heilquellenkurbetrieb', 'Heilquelle', 'Stuttgart'),
    ('Bad Teinach (Bad Teinach-Zavelstein)', 'Heilbad', 'Mineralquelle', 'Bad Teinach-Zavelstein'),
    ('Bad Überkingen', 'Heilbad', 'Mineralquelle', 'Bad Uberkingen'),
    ('Bad Urach', 'Heilbad', 'Thermal', 'Bad Urach'),
    ('Waldbronn (Busenbach, Reichenbach)', 'Ort mit Heilquellenkurbetrieb', 'Heilquelle', 'Waldbronn'),
    ('Bad Waldsee', '(Moor-)Heilbad u. Kneippkurort', 'Moor', 'Bad Waldsee'),
    ('Bad Wildbad', 'Heilbad', 'Thermal', 'Bad Wildbad'),
    ('Bad Wimpfen', '(Sole-)Heilbad', 'Sole', 'Bad Wimpfen'),
    ('Bad Wurzach', '(Moor-)Heilbad', 'Moor', 'Bad Wurzach'),
]

RP = [
    ('Bad Bertrich', 'Heilbad', 'Thermal', 'Bad Bertrich'),
    ('Bad Breisig', 'Heilbad', 'Thermal', 'Bad Breisig'),
    ('Bad Dürkheim', 'Heilbad', 'Sole', 'Bad Durkheim'),
    ('Bad Ems', 'Heilbad', 'Thermal', 'Bad Ems'),
    ('Bad Hönningen', 'Heilbad', 'Thermal', 'Bad Honningen'),
    ('Bad Kreuznach', 'Heilbad', 'Sole', 'Bad Kreuznach'),
    ('Bad Münster am Stein (Bad Kreuznach)', '(Mineral-)Heilbad u. heilklimatischer Kurort', 'Mineralquelle', 'Bad Kreuznach'),
    ('Bad Neuenahr (Bad Neuenahr-Ahrweiler)', 'Heilbad', 'Thermal', 'Bad Neuenahr-Ahrweiler'),
    ('Bad Salzig (Boppard)', 'Heilbad', 'Mineralquelle', 'Boppard'),
    ('Bad Wildstein (Traben-Trarbach)', 'Heilbad', 'Thermal', 'Traben-Trarbach'),
]

SL = []  # Saarland: kein Ort mit Heilmittel-Prädikat im Verzeichnis (nur Kneippkurort/heilklimatische Kurorte)

SH = [
    ('Bad Bramstedt', 'Luftkurort, (Moor-Heilbad)', 'Moor', 'Bad Bramstedt'),
    ('Büsum', 'Nordseeheilbad', 'Seeheilbad', 'Busum'),
    ('Burg (Fehmarn)', 'Ostseeheilbad', 'Seeheilbad', 'Fehmarn'),
    ('Dahme', 'Seebad, Ostseeheilbad', 'Seeheilbad', 'Dahme'),
    ('Damp (Damp 2000)', 'Ostseeheilbad', 'Seeheilbad', 'Damp'),
    ('Friedrichskoog-Spitze (Friedrichskoog)', 'Nordseeheilbad, Prädikat gilt nur für den OT Friedrichskoog-Spitze', 'Seeheilbad', 'Friedrichskoog'),
    ('Glücksburg', 'Seebad, Ostseeheilbad', 'Seeheilbad', 'Glucksburg'),
    ('Grömitz', 'Seebad, Ostseeheilbad', 'Seeheilbad', 'Gromitz'),
    ('Großenbrode', 'Ostseeheilbad', 'Seeheilbad', 'Grossenbrode'),
    ('Haffkrug (Scharbeutz)', 'Seebad, Ostseeheilbad', 'Seeheilbad', 'Scharbeutz'),
    ('Heiligenhafen', 'Ostseeheilbad', 'Seeheilbad', 'Heiligenhafen'),
    ('Helgoland', 'Nordseeheilbad', 'Seeheilbad', 'Helgoland'),
    ('Hohwacht', 'Seebad, Ostseeheilbad', 'Seeheilbad', 'Hohwacht'),
    ('Kellenhusen', 'Seebad, Ostseeheilbad', 'Seeheilbad', 'Kellenhusen'),
    ('Norddorf/Amrum', 'Nordseeheilbad', 'Seeheilbad', 'Norddorf'),
    ('Nordstrand', 'Nordseeheilbad', 'Seeheilbad', 'Nordstrand'),
    ('Pellworm', 'Nordseeheilbad', 'Seeheilbad', 'Pellworm'),
    ('Scharbeutz (OT Scharbeutz)', 'Seebad, Ostseeheilbad', 'Seeheilbad', 'Scharbeutz'),
    ('Holm (Schönberg)', 'Seebad, Heilbad', 'Seeheilbad', 'Schonberg'),
    ('Bad Schwartau', '(Jodsole- u. Moor-)Heilbad', 'Sole, Moor', 'Bad Schwartau'),
    ('Bad Segeberg', 'Luftkurort, Heilbad', 'Heilbad', 'Bad Segeberg'),
    ('St. Peter-Ording', 'Nordseeheilbad u. Schwefelbad', 'Seeheilbad, Schwefel', 'Sankt Peter-Ording'),
    ('Timmendorfer Strand (Timmendorfer Strand, Niendorf)', 'Seebad, Ostseeheilbad', 'Seeheilbad', 'Timmendorfer Strand'),
    ('Travemünde (Lübeck)', 'Ostseeheilbad', 'Seeheilbad', 'Lubeck'),
    ('Wenningstedt/Sylt', 'Nordseeheilbad', 'Seeheilbad', 'Wenningstedt-Braderup'),
    ('Westerland (Sylt)', 'Nordseeheilbad', 'Seeheilbad', 'Sylt'),
    ('Wittdün/Amrum', 'Nordseeheilbad', 'Seeheilbad', 'Wittdun'),
    ('Wyk a. F.', 'Nordseeheilbad', 'Seeheilbad', 'Wyk auf Fohr'),
]

MV = [
    ('Ahlbeck (Heringsdorf)', 'Ostseeheilbad', 'Seeheilbad', 'Heringsdorf'),
    ('Bansin (Heringsdorf)', 'Ostseeheilbad', 'Seeheilbad', 'Heringsdorf'),
    ('Ostseebad Boltenhagen', 'Ostseeheilbad', 'Seeheilbad', 'Boltenhagen'),
    ('Bad Doberan', '(Moor-)Heilbad', 'Moor', 'Bad Doberan'),
    ('Heiligendamm (Bad Doberan)', 'Seeheilbad', 'Seeheilbad', 'Bad Doberan'),
    ('Graal-Müritz', 'Ostseeheilbad', 'Seeheilbad', 'Graal-Muritz'),
    ('Heringsdorf', 'Ostseeheilbad u. (Sole-) Heilbad', 'Seeheilbad, Sole', 'Heringsdorf'),
    ('Bad Sülze', 'Peloidkurbetrieb', 'Moor', 'Bad Sulze'),
    ('Waren/Müritz', '(Sole-)Heilbad', 'Sole', 'Waren'),
    ('Ostseebad Zingst', 'Ostseeheilbad', 'Seeheilbad', 'Zingst'),
]

# Art-Kurzform NICHT aus dem Verzeichnis, sondern aus allgemeiner Kenntnis ergänzt (bitte bei Bedarf prüfen)
ART_ERGAENZT = {
    'BW': ['Baden-Baden', 'Badenweiler', 'Bad Ditzenbach', 'Bad Herrenalb', 'Bad Krozingen', 'Bad Liebenzell',
           'Bad Mergentheim', 'Bad Säckingen', 'Bad Saulgau', 'Bad Mingolsheim (Bad Schönborn)',
           'Bad Teinach (Bad Teinach-Zavelstein)', 'Bad Überkingen', 'Bad Urach', 'Bad Wildbad'],
    'RP': ['Bad Bertrich', 'Bad Breisig', 'Bad Dürkheim', 'Bad Ems', 'Bad Hönningen', 'Bad Kreuznach',
           'Bad Neuenahr (Bad Neuenahr-Ahrweiler)', 'Bad Salzig (Boppard)', 'Bad Wildstein (Traben-Trarbach)'],
    'SH': ['Holm (Schönberg)', 'Bad Segeberg'],
    'MV': ['Bad Sülze'],
}

# Bewusst nicht in den Hauptlisten: Kneipp-/Felke-Heilbäder (kein ortsgebundenes Heilmittel) und Zweifelsfälle
GRENZFAELLE = {
    'BW': [('Überlingen', 'Kneippheilbad', 'Kneipp', 'Uberlingen')],
    'RP': [
        ('Bad Bergzabern', 'Kneippheilbad u. heilklimatischer Kurort', 'Kneipp', 'Bad Bergzabern'),
        ('Bad Marienberg', 'Kneippheilbad', 'Kneipp', 'Bad Marienberg'),
        ('Bad Sobernheim', 'Heilbad (Berlin 2026) / Felke-Heilbad (RP 2018)', 'Felke', 'Bad Sobernheim'),
        ('Bad Tönisstein (Andernach / Burgbrohl)', 'Heilbad (nur im Berliner Verzeichnis, fehlt in RP-Liste 2018)', 'Heilquelle', 'Andernach'),
    ],
    'SL': [],
    'SH': [],
    'MV': [],
}

QUELLEN = {
    'BW': {'t': 'Senatsverwaltung für Finanzen Berlin: Übersicht der anerkannten Heilbäder- und Kurorte (zu § 35 Abs. 1 Satz 2 LBhVO), Anlage zum RS IV Nr. 42/2026',
           'u': 'https://www.berlin.de/politik-und-verwaltung/rundschreiben/download.php/4330565',
           'stand': '10/2026 (Rundschreiben vom 09.10.2026; Bad Rippoldsau-Schapbach gestrichen)'},
    'RP': {'t': 'Stellungnahme der Landesregierung RP zum Anhörverfahren „Gesundheitstourismus“, Enquete-Kommission Tourismus (Tabelle 3.2), gegengeprüft mit Berliner Verzeichnis 10/2026',
           'u': 'https://wayback.edoweb-rlp.de/weltweit/20241029mp_/https:/mwvlw.rlp.de/fileadmin/mwkel/Abteilung_3/Tourismus/Gesundheitstourismus.pdf ; https://www.berlin.de/politik-und-verwaltung/rundschreiben/download.php/4330565',
           'stand': 'RP-Liste 10.07.2018; Berliner Verzeichnis 10/2026'},
    'SL': {'t': 'Senatsverwaltung für Finanzen Berlin: Übersicht der anerkannten Heilbäder- und Kurorte, Anlage zum RS IV Nr. 42/2026',
           'u': 'https://www.berlin.de/politik-und-verwaltung/rundschreiben/download.php/4330565',
           'stand': '10/2026 (keine saarländische Landesliste gefunden)'},
    'SH': {'t': 'Senatsverwaltung für Finanzen Berlin: RS IV Nr. 42/2026 (Änderungsteil SH) + Anlage Übersicht der anerkannten Heilbäder- und Kurorte',
           'u': 'https://www.berlin.de/politik-und-verwaltung/rundschreiben/download.php/4330562 ; https://www.berlin.de/politik-und-verwaltung/rundschreiben/download.php/4330565',
           'stand': '10/2026'},
    'MV': {'t': 'Senatsverwaltung für Finanzen Berlin: Übersicht der anerkannten Heilbäder- und Kurorte, Anlage zum RS IV Nr. 42/2026',
           'u': 'https://www.berlin.de/politik-und-verwaltung/rundschreiben/download.php/4330565',
           'stand': '10/2026 (Landesliste MV nicht abrufbar)'},
}

if __name__ == '__main__':
    for k, v in (('BW', BW), ('RP', RP), ('SL', SL), ('SH', SH), ('MV', MV)):
        print(k, len(v))
