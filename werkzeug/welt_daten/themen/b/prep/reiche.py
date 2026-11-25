"""Ebene 'reiche': alte Reiche zur größten Ausdehnung – schematisch nach heutigen Staaten."""
import sys
sys.path.insert(0, '/home/claude/scratch/themen/b/prep')
from gemein import *

# [Name, Bestand, Jahr größte Ausdehnung, Fläche Mio km² (Text), Hauptstadt, lon, lat, heutige Staaten (ganz/teilweise), Text, Farbe]
R = [
 ['Perserreich (Achämeniden)', '550–330 v. Chr.', -500, '5,5', 'Persepolis', 52.89, 29.93,
  'IRN IRQ KWT SYR LBN ISR PSE JOR EGY LBY TUR CYP ARM AZE GEO AFG PAK TKM UZB TJK BGR GRC MKD',
  'Reich der Achämeniden von Ägypten und Thrakien bis zum Indus; Verwaltung in Satrapien, Königsstraße von Sardes nach Susa.', '#d8a050'],
 ['Alexanderreich', '336–323 v. Chr.', -323, '5,2', 'Babylon', 44.42, 32.54,
  'GRC MKD BGR ALB TUR CYP SYR LBN ISR PSE JOR EGY LBY IRQ KWT IRN AFG PAK TKM UZB TJK',
  'Alexander der Große erobert das Perserreich bis zum Indus; nach seinem Tod 323 v. Chr. zerfällt es in die Diadochenreiche.', '#e8c86a'],
 ['Maurya-Reich', 'ca. 322–185 v. Chr.', -250, '3,4–5,0 (je nach Schätzung)', 'Pataliputra (heute Patna)', 85.14, 25.61,
  'IND PAK AFG BGD NPL', 'Erstes Großreich auf dem indischen Subkontinent; unter Ashoka Förderung des Buddhismus.', '#ff9a6a'],
 ['Han-Dynastie', '206 v. Chr.–220 n. Chr.', 100, '6,5 (Östliche Han)', 'Luoyang', 112.45, 34.62,
  'CHN VNM PRK', 'Chinesisches Kaiserreich; unter den Han entstehen die Handelswege der Seidenstraße nach Westen.', '#e86a6a'],
 ['Römisches Reich', '27 v. Chr.–476 n. Chr. (Westrom)', 117, '5,0', 'Rom', 12.48, 41.89,
  'ITA VAT SMR MLT FRA MCO ESP AND PRT GBR BEL NLD LUX DEU CHE LIE AUT SVN HRV BIH SRB MNE XKX ALB MKD GRC BGR ROU HUN TUR CYP SYR LBN ISR PSE JOR EGY LBY TUN DZA MAR IRQ ARM',
  'Größte Ausdehnung unter Kaiser Trajan 117 n. Chr.; Mesopotamien und Armenien nur kurz als Provinzen (114–117).', '#c84a4a'],
 ['Byzantinisches Reich (Ostrom)', '395–1453', 555, '2,7–2,8', 'Konstantinopel', 28.98, 41.01,
  'TUR GRC BGR MKD ALB SRB MNE XKX HRV ITA MLT TUN DZA ESP EGY LBY ISR PSE JOR LBN SYR CYP GEO UKR',
  'Größte Ausdehnung nach den Rückeroberungen unter Kaiser Justinian (Italien, Nordafrika, Südspanien).', '#b07ad8'],
 ['Kalifat der Umayyaden', '661–750', 720, '11,1', 'Damaskus', 36.29, 33.51,
  'ESP PRT FRA MAR DZA TUN LBY EGY ISR PSE JOR LBN SYR IRQ SAU YEM OMN ARE QAT BHR KWT IRN AFG PAK TKM UZB TJK ARM AZE GEO TUR',
  'Von der Iberischen Halbinsel bis an den Indus und nach Zentralasien.', '#5ac87a'],
 ['Heiliges Römisches Reich', '962–1806', 1050, '1,0', 'keine feste Hauptstadt (Krönungsort Aachen)', 6.08, 50.78,
  'DEU AUT CHE LIE NLD BEL LUX FRA ITA CZE SVN',
  'Reich der römisch-deutschen Kaiser in Mitteleuropa, um 1050 mit Reichsitalien und Burgund; 1806 aufgelöst.', '#d8d86a'],
 ['Mongolenreich', '1206–1368', 1270, '24,0', 'Karakorum', 102.83, 47.2,
  'MNG CHN RUS KAZ KGZ UZB TKM TJK AFG IRN IRQ AZE ARM GEO UKR TUR PAK KOR PRK',
  'Größtes zusammenhängendes Landreich der Geschichte; um 1260 in vier Teilreiche (Khanate) zerfallen.', '#ff6a6a'],
 ['Mali-Reich', 'ca. 1235–1670', 1380, '1,1', 'Niani (Lage umstritten)', -8.38, 11.37,
  'MLI SEN GMB GIN GNB MRT', 'Westafrikanisches Reich, reich durch Gold und Transsahara-Handel; Mansa Musa pilgerte 1324 nach Mekka.', '#e8b04a'],
 ['Inka-Reich', 'ca. 1438–1533', 1527, '2,0', 'Cusco', -71.97, -13.53,
  'PER ECU BOL CHL ARG COL', 'Reich Tawantinsuyu entlang der Anden mit rund 40.000 km Straßennetz; 1532–1533 von Spaniern erobert.', '#4ad0c8'],
 ['Aztekenreich (Dreibund)', '1428–1521', 1520, '0,22', 'Tenochtitlan (heute Mexiko-Stadt)', -99.13, 19.43,
  'MEX', 'Dreibund von Tenochtitlan, Texcoco und Tlacopan in Zentralmexiko; 1521 von Spaniern und verbündeten Völkern erobert.', '#6ad08a'],
 ['Osmanisches Reich', '1299–1922', 1683, '5,2', 'Konstantinopel (Istanbul)', 28.98, 41.01,
  'TUR GRC BGR ROU MDA UKR HUN SVK SRB MNE BIH HRV MKD ALB XKX CYP SYR LBN ISR PSE JOR IRQ SAU YEM EGY LBY TUN DZA GEO',
  'Größte Ausdehnung zur Zeit der zweiten Belagerung Wiens 1683; Ende 1922, Nachfolger Republik Türkei 1923. Das heutige Armenien und Aserbaidschan gehörten 1683 zum Safawidenreich.', '#5a9ae8'],
 ['Mogulreich', '1526–1857', 1690, '4,0', 'Delhi (Shahjahanabad)', 77.23, 28.66,
  'IND PAK BGD AFG', 'Muslimische Dynastie in Nordindien; größte Ausdehnung unter Aurangzeb.', '#a8c84a'],
 ['Spanisches Kolonialreich', '1492–1976', 1810, '13,7', 'Madrid', -3.7, 40.42,
  'ESP MEX USA GTM HND SLV NIC CRI PAN COL VEN ECU PER BOL CHL ARG URY PRY CUB DOM PRI PHL GUM MNP FSM PLW GNQ',
  'Größte Ausdehnung um 1810, kurz vor der Unabhängigkeit der Staaten Lateinamerikas.', '#ffcf5a'],
 ['Russisches Reich', '1721–1917', 1895, '22,8', 'Sankt Petersburg', 30.31, 59.94,
  'RUS UKR BLR MDA EST LVA LTU POL FIN GEO ARM AZE KAZ UZB TKM TJK KGZ TUR',
  'Zarenreich von Polen und Finnland bis zum Pazifik; Alaska wurde 1867 an die USA verkauft.', '#9a7ad8'],
 ['Britisches Empire', 'ca. 1600–1997', 1920, '35,5', 'London', -0.13, 51.51,
  'GBR IRL CAN AUS NZL ZAF IND PAK BGD MMR LKA MYS SGP BRN EGY SDN SSD KEN UGA TZA ZMB ZWE MWI BWA LSO SWZ NAM NGA GHA SLE GMB CMR TGO SOL IRQ JOR ISR PSE CYP MLT GUY BLZ JAM BHS BRB TTO ATG KNA LCA VCT GRD DMA BMU FLK PNG FJI SLB TON KIR TUV NRU WSM YEM ARE QAT BHR KWT MDV SYC MUS HKG',
  'Größtes Reich der Geschichte, um 1920 mit Dominions, Kolonien, Protektoraten und Völkerbundmandaten rund ein Viertel der Landfläche.', '#e85a7a'],
]
daten = []
for n, best, j, fl, hs, lo, la, l, t, c in R:
    l = l.split()
    for i in l: assert i in APP, (n, i)
    daten.append({'n': n, 'zeit': best, 'j': j, 'fl': fl, 'hs': hs, 'lon': r2(lo), 'lat': r2(la), 'l': l, 'schema': True,
                  't': t, 'c': c})
obj = {'id': 'reiche', 'name': 'Alte Reiche', 'gruppe': 'Geschichte', 'typ': 'land-liste', 'einheit': 'Mio. km²',
       'legende': [{'n': d['n'], 'c': d['c']} for d in daten],
       'quellen': [
           {'t': 'Flächen und Jahr der größten Ausdehnung: Wikipedia „List of largest empires“ (Zusammenstellung nach Taagepera 1978/1979/1997, Turchin u. a. 2006 u. a.)',
            'u': 'https://en.wikipedia.org/wiki/List_of_largest_empires', 'stand': '11/2026',
            'lizenz': 'nur Einzelwerte (Fakten) übernommen; Artikeltext CC BY-SA 4.0'},
           {'t': 'R. Taagepera: Size and Duration of Empires, Social Science Research 7 (1978), 8 (1979); International Studies Quarterly 41 (1997)',
            'u': 'https://doi.org/10.1111/0020-8833.00053', 'stand': '1997', 'lizenz': 'Fachliteratur (zitiert)'}],
       'hinweis': 'Schematisch nach heutigen Grenzen: Liste der heutigen Staaten, die ganz oder teilweise zum Reich gehörten '
                  '(nur grobe Zuordnung, Teilgebiete werden als ganzes Land gefärbt). Flächen sind Schätzungen der Fachliteratur.',
       'felder': {'n': 'Name', 'zeit': 'Bestand', 'j': 'Jahr der größten Ausdehnung (negativ = v. Chr.)', 'fl': 'Fläche Mio. km² (Text)',
                  'hs': 'Hauptstadt', 'lon/lat': 'Lage der Hauptstadt', 'l': 'heutige Staaten (ISO3)', 'schema': 'schematisch', 't': 'Info-Text', 'c': 'Farbvorschlag'},
       'daten': daten}
schreibe(obj)
