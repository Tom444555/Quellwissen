"""Ebene 'buendnisse': Bündnisse und Zusammenschlüsse, Mitglieder als ISO3 mit Beitrittsjahr, Stand 25.11.2026."""
import sys
sys.path.insert(0, '/home/claude/scratch/themen/b/prep')
from gemein import *


def jl(s):  # "1949: USA CAN …; 1952: GRC TUR" -> {ISO: Jahr}
    out = {}
    for teil in s.split(';'):
        j, l = teil.split(':')
        for c in l.split(): out[c] = int(j)
    return out


B = []


def bund(id, n, voll, gegr, t, c, mitglieder, q, **kw):
    e = {'id': id, 'n': n, 'voll': voll, 'gegr': gegr, 't': t, 'c': c, 'mitglieder': mitglieder, 'q': q}
    e.update(kw); B.append(e)


bund('nato', 'NATO', 'Nordatlantikvertrags-Organisation', 1949, 'Militärbündnis mit Beistandspflicht (Artikel 5).', '#4a8ae8',
     jl('1949: USA CAN GBR FRA BEL NLD LUX DNK NOR ISL ITA PRT; 1952: GRC TUR; 1955: DEU; 1982: ESP; 1999: CZE HUN POL;'
        '2004: BGR EST LVA LTU ROU SVK SVN; 2009: ALB HRV; 2017: MNE; 2020: MKD; 2023: FIN; 2024: SWE'),
     {'t': 'NATO, NATO member countries (Seite abgerufen 25.11.2026, zuletzt aktualisiert 11.03.2024)', 'u': 'https://www.nato.int/fr/about-us/organization/nato-member-countries?selectedLocale=en', 'stand': '11/2026 (32 Mitglieder, alle Beitrittsjahre bestätigt)'},
     hinweis_mitglieder='Deutschland 1955 (Bundesrepublik), Gebiet der früheren DDR seit 1990.')
bund('eu', 'EU', 'Europäische Union', 1958, 'Staatenverbund mit Binnenmarkt; Vorläufer EWG 1958. Großbritannien trat 2020 aus.', '#3a6ad8',
     jl('1958: BEL DEU FRA ITA LUX NLD; 1973: DNK IRL; 1981: GRC; 1986: ESP PRT; 1995: AUT FIN SWE ALA;'
        '2004: CYP CZE EST HUN LVA LTU MLT POL SVK SVN; 2007: BGR ROU; 2013: HRV'),
     {'t': 'Europäische Union, EU-Länder; „What is enlargement?“ (9 Kandidaten, Kosovo potenzieller Kandidat, abgerufen 25.11.2026)', 'u': 'https://european-union.europa.eu/principles-countries-history/eu-enlargement_en', 'stand': '11/2026 (27 Mitglieder)'},
     kandidaten=['ALB', 'BIH', 'GEO', 'MDA', 'MNE', 'MKD', 'SRB', 'TUR', 'UKR'], moeglich=['XKX'],
     ehemalig={'GBR': '1973–2020'},
     hinweis_mitglieder='ALA (Åland) gehört zu Finnland. Im Norden Zyperns (CYN) ist EU-Recht ausgesetzt; Grönland und Färöer (zu Dänemark) sind nicht in der EU.')
bund('euro', 'Eurozone', 'Euro-Währungsgebiet', 1999, 'EU-Staaten mit dem Euro als Währung (Bargeld seit 2002).', '#2a9ad8',
     jl('1999: AUT BEL FIN FRA DEU IRL ITA LUX NLD PRT ESP ALA; 2001: GRC; 2007: SVN; 2008: CYP MLT; 2009: SVK; 2011: EST;'
        '2014: LVA; 2015: LTU; 2023: HRV; 2026: BGR'),
     {'t': 'Europäische Zentralbank, Pressemitteilung „Bulgaria joins the euro“ (1.1.2026)', 'u': 'https://www.ecb.europa.eu/press/pr/date/2026/html/ecb.pr260101~c830245e42.en.html', 'stand': '01/2026 (21 Mitglieder)'},
     euro_ohne_eu=['AND', 'MCO', 'SMR', 'VAT', 'MNE', 'XKX'],
     hinweis_mitglieder='euro_ohne_eu: Andorra, Monaco, San Marino und Vatikanstadt per Abkommen; Montenegro und Kosovo nutzen den Euro einseitig.')
bund('schengen', 'Schengen-Raum', 'Schengen-Raum ohne Binnengrenzkontrollen', 1995, 'Reisen ohne Personenkontrollen an den Binnengrenzen (zeitweise Kontrollen möglich).', '#5ab0e8',
     jl('1995: BEL FRA DEU LUX NLD PRT ESP; 1997: AUT ITA; 2000: GRC; 2001: DNK FIN ISL NOR SWE ALA;'
        '2007: CZE EST HUN LVA LTU MLT POL SVK SVN; 2008: CHE; 2011: LIE; 2023: HRV; 2025: BGR ROU'),
     {'t': 'Europäische Kommission, Schengen Area (25 EU-Staaten + Island, Norwegen, Schweiz, Liechtenstein; BGR/ROU 01.01.2025; abgerufen 25.11.2026)', 'u': 'https://home-affairs.ec.europa.eu/policies/schengen/schengen-area_en', 'stand': '11/2026 (29 Staaten)'},
     hinweis_mitglieder='Jahr = volle Anwendung. Irland (Opt-out) und Zypern (Integration laufend, Binnenkontrollen noch nicht aufgehoben) sind EU-Mitglieder ohne volle Schengen-Anwendung. Bulgarien und Rumänien: Luft/See 2024, Land 2025.')
bund('brics', 'BRICS', 'BRICS-Staatengruppe', 2006, 'Zusammenschluss großer Schwellenländer; seit 2024 erweitert, seit 2025 mit Partnerländern.', '#e8a050',
     jl('2006: BRA RUS IND CHN; 2011: ZAF; 2024: EGY ETH IRN ARE SAU; 2025: IDN'),
     {'t': 'BRICS Brasil (Vorsitz 2025), FAQ „Frequently Asked Questions about the BRICS“; Business Today 10.09.2026', 'u': 'https://brics.br/en/about-the-brics/frequently-asked-questions-about-the-brics', 'stand': '09/2026'},
     partner=['BLR', 'BOL', 'CUB', 'KAZ', 'MYS', 'NGA', 'THA', 'UGA', 'UZB', 'VNM'],
     hinweis_mitglieder='Saudi-Arabien wird auf der BRICS-Seite als Mitglied geführt; eine formelle Bestätigung des Beitritts durch Saudi-Arabien ist dort nicht vermerkt.')
bund('soz', 'SOZ', 'Shanghaier Organisation für Zusammenarbeit', 2001, 'Regionale Organisation für Sicherheit, Wirtschaft und Zusammenarbeit in Eurasien.', '#d86a6a',
     jl('2001: CHN RUS KAZ KGZ TJK UZB; 2017: IND PAK; 2023: IRN; 2024: BLR'),
     {'t': 'SCO-Sekretariat, Bericht zum Gipfel 01.09.2026; Mitgliederliste SCO', 'u': 'https://eng.sectsco.org/20260306/2185663.html', 'stand': '09/2026 (10 Mitglieder; Beobachter/Dialogpartner laut SCO-Sekretariat 06.03.2026, Laos Memorandum 10.07.2026)'},
     beobachter=['MNG', 'AFG'], partner=['ARM', 'AZE', 'BHR', 'KHM', 'EGY', 'KWT', 'MDV', 'MMR', 'NPL', 'QAT', 'SAU', 'LKA', 'TUR', 'ARE', 'LAO'],
     hinweis_mitglieder='Afghanistan: Beobachterstatus seit 2021 ruhend. Die SOZ hat 2025 beschlossen, Beobachter und Dialogpartner zu einer Partnerstufe zusammenzulegen.')
bund('ovks', 'OVKS', 'Organisation des Vertrags über kollektive Sicherheit', 2002, 'Militärbündnis früherer Sowjetrepubliken (Vertrag von 1992).', '#b04a4a',
     jl('1992: RUS ARM KAZ KGZ TJK; 1993: BLR'),
     {'t': 'The Moscow Times, „CSTO strips Armenia of voting rights“ (18.11.2026); Armenpress', 'u': 'https://www.themoscowtimes.com/2026/11/18/csto-strips-armenia-of-voting-rights', 'stand': '11/2026'},
     ausgesetzt={'ARM': 'Teilnahme seit 2024 von Armenien eingefroren; Stimmrecht am 11.11.2026 wegen offener Beiträge entzogen, Mitgliedschaft formal fortbestehend'},
     ehemalig={'AZE': '1993–1999', 'GEO': '1994–1999', 'UZB': '1992–1999, 2006–2012'})
bund('eawu', 'EAWU', 'Eurasische Wirtschaftsunion', 2015, 'Zollunion und Binnenmarkt im postsowjetischen Raum.', '#c88a5a',
     jl('2015: RUS BLR KAZ ARM KGZ'),
     {'t': 'Eurasische Wirtschaftskommission, Observer state status at the EAEU; Iran: Beschluss des Obersten Rats 26.12.2024 (intellinews)', 'u': 'https://eec.eaeunion.org/en/comission/department/dep_razv_integr/mezhdunarodnoe-sotrudnichestvo/o-statuse-gosudarstva-nablyudatelya.php', 'stand': '11/2026 (5 Mitglieder, 4 Beobachter)'},
     beobachter=['MDA', 'UZB', 'CUB', 'IRN'],
     hinweis_mitglieder='Beobachter: Moldau 2018, Usbekistan und Kuba 2020, Iran 2024. Armenien seit 02.01.2015, Kirgistan seit 12.08.2015.')
bund('opec', 'OPEC', 'Organisation erdölexportierender Länder', 1960, 'Kartell erdölexportierender Staaten; Sitz Wien.', '#ff8a3d',
     jl('1960: IRN IRQ KWT SAU VEN; 1962: LBY; 1969: DZA; 1971: NGA; 1975: GAB; 2017: GNQ; 2018: COG'),
     {'t': 'Al Jazeera, „What are OPEC and OPEC+, and why has the UAE quit?“ (28.04.2026); US EIA, Today in Energy (23.06.2026)', 'u': 'https://www.aljazeera.com/economy/2026/4/28/what-are-opec-and-opec-and-why-has-the-uae-quit', 'stand': '11/2026 (11 Mitglieder)'},
     ehemalig={'ARE': '1967–2026 (Austritt zum 1. Mai 2026)', 'QAT': '1961–2019', 'AGO': '2007–2024', 'ECU': '1973–1992, 2007–2020', 'IDN': '1962–2008, 2016'},
     hinweis_mitglieder='Gabun war 1995–2016 nicht Mitglied.')
bund('opecplus', 'OPEC+', 'OPEC und Partner (Kooperationserklärung 2016)', 2016, 'OPEC-Staaten und weitere Förderländer stimmen Fördermengen ab.', '#ffb070',
     {**{c: 2016 for c in ['IRN', 'IRQ', 'KWT', 'SAU', 'VEN', 'LBY', 'DZA', 'NGA', 'GAB', 'GNQ', 'COG']},
      **{c: 2016 for c in ['RUS', 'AZE', 'KAZ', 'BHR', 'BRN', 'MYS', 'MEX', 'OMN', 'SSD', 'SDN']}},
     {'t': 'Al Jazeera (28.04.2026) nach OPEC; OPEC-Pressemitteilungen 2026', 'u': 'https://www.aljazeera.com/economy/2026/4/28/what-are-opec-and-opec-and-why-has-the-uae-quit', 'stand': '11/2026'},
     nicht_opec=['RUS', 'AZE', 'KAZ', 'BHR', 'BRN', 'MYS', 'MEX', 'OMN', 'SSD', 'SDN'], ehemalig={'ARE': 'mit OPEC-Austritt 2026 auch aus OPEC+'},
     partner=['BRA'],
     hinweis_mitglieder='Brasilien: seit 2025 Mitglied der Kooperations-Charta (Charter of Cooperation, OPEC-Pressemitteilung 18.02.2025), nicht Teil der Fördermengen-Absprachen. Jahr = Kooperationserklärung (Dezember 2016) bzw. OPEC-Mitgliedschaft; GNQ und COG kamen 2017/2018 als OPEC-Mitglieder hinzu.')
bund('asean', 'ASEAN', 'Verband Südostasiatischer Nationen', 1967, 'Regionale Zusammenarbeit in Südostasien.', '#4ad0a0',
     jl('1967: IDN MYS PHL SGP THA; 1984: BRN; 1995: VNM; 1997: LAO MMR; 1999: KHM; 2025: TLS'),
     {'t': 'ASEAN-Sekretariat, „Forging a New Era: Timor-Leste Admitted into ASEAN“ (Gipfel 26.10.2025)', 'u': 'https://asean.org/forging-a-new-era-timor-leste-admitted-into-asean/', 'stand': '11/2026 (11 Mitglieder)'},
     beobachter=['PNG'])
bund('au', 'Afrikanische Union', 'Afrikanische Union', 2002, 'Zusammenschluss aller 55 afrikanischen Staaten (Vorläufer OAU 1963).', '#7ac86a',
     {c: 2002 for c in 'DZA AGO BEN BWA BFA BDI CPV CMR CAF TCD COM COG COD CIV DJI EGY GNQ ERI SWZ ETH GAB GMB GHA GIN GNB KEN LSO LBR LBY MDG MWI MLI MRT MUS MOZ NAM NER NGA RWA ESH STP SEN SYC SLE SOM ZAF SSD SDN TZA TGO TUN UGA ZMB ZWE'.split()} | {'MAR': 2017, 'SSD': 2011},
     {'t': 'Amani Africa, „Informal Consultation with Member States in Political Transition“ (26.02.2026); Afrikanische Union', 'u': 'https://amaniafrica-et.org/informal-consultation-with-member-states-in-political-transition/', 'stand': '02/2026 (Suspendierungen); bis 11/2026 keine Änderung gefunden'},
     ausgesetzt={c: 'von den Aktivitäten der AU suspendiert (verfassungswidriger Regierungswechsel)' for c in ['BFA', 'GNB', 'MDG', 'MLI', 'NER', 'SDN']},
     hinweis_mitglieder='ESH: Mitglied ist die Demokratische Arabische Republik Sahara (seit 1982 in der OAU); das Gebiet wird von Marokko beansprucht und größtenteils verwaltet. '
                       'Marokko trat 1984 aus der OAU aus und 2017 der AU bei. Somaliland (SOL) erklärt sich für unabhängig, ist aber kein AU-Mitglied (Mitglied ist Somalia). '
                       'Jahr 2002 = Gründung der AU. Guinea: Suspendierung am 22.01.2026 aufgehoben, Gabun 2025.')
bund('liga', 'Arabische Liga', 'Liga der Arabischen Staaten', 1945, 'Zusammenschluss arabischer Staaten; Sitz Kairo.', '#5aa87a',
     jl('1945: EGY IRQ JOR LBN SAU SYR YEM; 1953: LBY; 1956: SDN; 1958: MAR TUN; 1961: KWT; 1962: DZA; 1971: BHR OMN QAT ARE; 1973: MRT; 1974: SOM; 1976: PSE; 1977: DJI; 1993: COM'),
     {'t': 'Encyclopaedia Britannica, „Arab League“ (Beitrittsjahre; Suspendierung Syriens 11/2011–2023); Liga der Arabischen Staaten', 'u': 'https://www.britannica.com/topic/Arab-League', 'stand': '11/2026 (22 Mitglieder)'},
     hinweis_mitglieder='Syrien war 2011–2023 suspendiert. Palästina als Mitglied (PLO seit 1976). Jahr 1945 für Gründungsmitglieder.')
bund('g7', 'G7', 'Gruppe der Sieben', 1975, 'Treffen großer Industrienationen; die EU nimmt teil. Russland war 1997–2014 dabei (G8).', '#a0a0ff',
     jl('1975: FRA DEU ITA JPN GBR USA; 1976: CAN'),
     {'t': 'G7 (Vorsitz Frankreich 2026)', 'u': 'https://www.elysee.fr/en/g7-evian', 'stand': '11/2026'}, ehemalig={'RUS': 'G8 1997–2014'})
bund('g20', 'G20', 'Gruppe der Zwanzig', 1999, '19 Staaten, die EU und (seit 2023) die Afrikanische Union.', '#c0c0ff',
     {**{c: 1999 for c in 'ARG AUS BRA CAN CHN FRA DEU IND IDN ITA JPN KOR MEX RUS SAU ZAF TUR GBR USA'.split()}},
     {'t': 'G20; Berichte zum Vorsitz USA 2026 (Tribune India, The Statesman)', 'u': 'https://www.tribuneindia.com/news/world/us-unveils-new-g20-for-2026-excludes-south-africa-over-politics-of-grievance', 'stand': '11/2026'},
     hinweis_mitglieder='Unter dem US-Vorsitz 2026 wurde Südafrika nicht zu den Treffen eingeladen und Polen als Gast eingeladen; an der formalen Mitgliedschaft ist keine Änderung beschlossen.')
bund('fiveeyes', 'Five Eyes', 'Geheimdienstverbund Five Eyes (UKUSA)', 1946, 'Zusammenarbeit der Nachrichtendienste (Fernmeldeaufklärung).', '#8a8aa8',
     jl('1946: USA GBR; 1949: CAN; 1956: AUS NZL'),
     {'t': 'GCHQ, „A brief history of UKUSA“ (Abkommen 05.03.1946, Kanada 1949, Australien/Neuseeland 1956); NSA, UKUSA Agreement Release 1940–1956', 'u': 'https://www.gchq.gov.uk/information/brief-history-of-ukusa', 'stand': '11/2026'},
     hinweis_mitglieder='Jahre nach GCHQ. Kanada: in den freigegebenen NSA-Dokumenten teils schon 1948 einbezogen.')
bund('aukus', 'AUKUS', 'Sicherheitspartnerschaft Australien–Großbritannien–USA', 2021, 'Sicherheitspakt, u. a. atomgetriebene U-Boote für Australien.', '#6a6ac8',
     jl('2021: AUS GBR USA'),
     {'t': 'Australian Government, AUKUS', 'u': 'https://www.pmc.gov.au/aukus', 'stand': '11/2026'})
bund('mercosur', 'Mercosur', 'Gemeinsamer Markt Südamerikas', 1991, 'Zollunion in Südamerika.', '#ffcf5a',
     jl('1991: ARG BRA PRY URY; 2012: VEN; 2024: BOL'),
     {'t': 'Mercosur, „MERCOSUR countries“ (Vertragsstaaten, Venezuela suspendiert, assoziierte Staaten; abgerufen 25.11.2026); Buenos Aires Times (19.05.2026)', 'u': 'https://betaweb.mercosur.int/en?p=36341', 'stand': '11/2026'},
     ausgesetzt={'VEN': 'suspendiert seit 2016/2017; Rückkehr wurde 2026 erörtert'}, partner=['CHL', 'COL', 'ECU', 'PER', 'GUY', 'SUR', 'PAN'],
     hinweis_mitglieder='Venezuela: Beitrittsprotokoll 2006, Vollmitglied 2012. Bolivien: Ratifikation Juli 2024, Vollmitglied mit Übergangsfrist. partner = assoziierte Staaten.')

for b in B:
    for k in ('mitglieder', 'partner', 'beobachter', 'kandidaten', 'ausgesetzt', 'ehemalig', 'nicht_opec', 'euro_ohne_eu', 'moeglich'):
        v = b.get(k)
        if v:
            for c in (v if isinstance(v, list) else v.keys()): assert c in APP, (b['id'], c)
    print(b['id'], len(b['mitglieder']))
obj = {'id': 'buendnisse', 'name': 'Bündnisse & Zusammenschlüsse', 'gruppe': 'Politik', 'typ': 'land-liste', 'einheit': '',
       'legende': [{'k': b['id'], 'n': b['n'], 'c': b['c']} for b in B],
       'quellen': [{'t': b['q']['t'], 'u': b['q']['u'], 'stand': b['q']['stand'], 'lizenz': 'Fakten (Mitgliederlisten), eigene Zusammenstellung'} for b in B],
       'hinweis': 'Mitglieder mit Beitrittsjahr; Partner, Beobachter, Kandidaten, Suspendierte und Ehemalige getrennt. Stand 25.11.2026. '
                  'Nicht anerkannte oder umstrittene Gebiete (z. B. Somaliland, Nordzypern) werden nicht als Mitglieder gefärbt.',
       'felder': {'mitglieder': '{ISO3: Beitrittsjahr}', 'partner': 'Partner/assoziierte Staaten', 'beobachter': 'Beobachter', 'kandidaten': 'Beitrittskandidaten',
                  'ausgesetzt': '{ISO3: Text} Mitgliedschaft ruht/suspendiert (bleibt in mitglieder)', 'ehemalig': '{ISO3: Zeitraum}', 'q': 'Beleg je Bündnis', 'c': 'Farbvorschlag'},
       'daten': B}
schreibe(obj)
