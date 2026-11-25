"""Ebene 'stuetzpunkte': größere, belegte Militärstützpunkte im Ausland (gleiche Regeln für alle Staaten) + große Standorte in Deutschland."""
import sys
sys.path.insert(0, '/home/claude/scratch/themen/b/prep')
from gemein import *

Q = {'USA': 'US-Verteidigungsministerium, Base Structure Report FY2015 (gemeinfrei) und Websites der US-Streitkräfte; Status nach Presseberichten 2026',
     'RUS': 'Presseberichte (Reuters, AP, Meduza); russ. Verteidigungsministerium; zu Syrien: Memorandum Syrien–Russland laut SANA/Meduza 10.08.2026',
     'CHN': 'Chinesisches Verteidigungsministerium (Djibouti, eröffnet 2017); zu Ream: Regierung Kambodschas und Presseberichte',
     'FRA': 'Französisches Verteidigungsministerium (forces prépositionnées); Al Jazeera 17.07.2025 zu den Übergaben',
     'GBR': 'UK Ministry of Defence; UK Parliament Library (Overseas military bases)',
     'TUR': 'Türkisches Verteidigungsministerium und Presseberichte (Anadolu, Reuters)',
     'IND': 'Indisches Außenministerium (IMTRAT Bhutan); Regierungen Indiens und Mauritius’ zu Agaléga',
     'DEU': 'Bundesministerium der Verteidigung / Bundeswehr', 'JPN': 'Japanisches Verteidigungsministerium', 'ITA': 'Italienisches Verteidigungsministerium'}
# [Name, Betreiber, Gastland (ISO3 der App oder None), lon, lat, Art, rang, Status, Text]
S = [
 # USA – Deutschland
 ['Ramstein Air Base', 'USA', 'DEU', 7.6, 49.44, 'luft', 1, 'aktiv', 'Größter US-Luftwaffenstützpunkt außerhalb der USA; Hauptquartier der US-Luftstreitkräfte in Europa und Afrika.'],
 ['Spangdahlem Air Base', 'USA', 'DEU', 6.69, 49.97, 'luft', 2, 'aktiv', 'US-Kampfflugzeuggeschwader in der Eifel.'],
 ['Truppenübungsplatz Grafenwöhr', 'USA', 'DEU', 11.94, 49.7, 'heer', 1, 'aktiv', 'Größter Truppenübungsplatz der US-Armee in Europa.'],
 ['Rose Barracks Vilseck', 'USA', 'DEU', 11.8, 49.62, 'heer', 3, 'aktiv', 'Standort des 2. US-Kavallerieregiments. Im Mai 2026 kündigte das Pentagon den Abzug von rund 5.000 Soldaten aus Deutschland an; ob dieses Regiment betroffen ist, ist amtlich nicht bestätigt.'],
 ['Hohenfels (JMRC)', 'USA', 'DEU', 11.84, 49.22, 'ausbildung', 3, 'aktiv', 'Übungszentrum der US-Armee für multinationale Manöver.'],
 ['Clay Kaserne Wiesbaden', 'USA', 'DEU', 8.33, 50.05, 'fuehrung', 2, 'aktiv', 'Hauptquartier der US-Armee in Europa und Afrika.'],
 ['Patch Barracks / Kelley Barracks Stuttgart', 'USA', 'DEU', 9.08, 48.73, 'fuehrung', 1, 'aktiv', 'Sitz der US-Regionalkommandos für Europa (EUCOM) und Afrika (AFRICOM).'],
 ['Landstuhl Regional Medical Center', 'USA', 'DEU', 7.56, 49.4, 'sanitaet', 3, 'aktiv', 'Größtes US-Militärkrankenhaus außerhalb der USA.'],
 ['Baumholder', 'USA', 'DEU', 7.33, 49.65, 'heer', 3, 'aktiv', 'US-Garnison mit Truppenübungsplatz.'],
 ['Katterbach / Ansbach', 'USA', 'DEU', 10.61, 49.31, 'luft', 3, 'aktiv', 'Standort einer Heeresfliegerbrigade.'],
 ['Fliegerhorst Büchel', 'DEU', 'DEU', 7.07, 50.17, 'luft', 2, 'aktiv', 'Bundeswehr-Geschwader für die nukleare Teilhabe der NATO; dort gelagerte US-Atomwaffen werden berichtet, amtlich aber nicht bestätigt.'],
 # USA – übriges Europa
 ['Aviano Air Base', 'USA', 'ITA', 12.6, 46.03, 'luft', 2, 'aktiv', 'US-Luftwaffengeschwader in Norditalien.'],
 ['Caserma Ederle Vicenza', 'USA', 'ITA', 11.57, 45.54, 'heer', 3, 'aktiv', 'Standort einer US-Luftlandebrigade.'],
 ['Naval Support Activity Neapel', 'USA', 'ITA', 14.29, 40.88, 'marine', 2, 'aktiv', 'Hauptquartier der US-Seestreitkräfte in Europa und Afrika, 6. Flotte.'],
 ['Sigonella', 'USA', 'ITA', 14.92, 37.4, 'marine', 2, 'aktiv', 'Marineflieger- und Logistikstützpunkt auf Sizilien.'],
 ['Naval Station Rota', 'USA', 'ESP', -6.35, 36.64, 'marine', 2, 'aktiv', 'Spanisch-amerikanischer Marinestützpunkt mit US-Zerstörern für die Raketenabwehr.'],
 ['Morón Air Base', 'USA', 'ESP', -5.62, 37.17, 'luft', 3, 'aktiv', 'Spanischer Luftwaffenstützpunkt mit US-Marineinfanterie-Einheit.'],
 ['Incirlik Air Base', 'USA', 'TUR', 35.43, 37.0, 'luft', 1, 'aktiv', 'Türkischer Luftwaffenstützpunkt mit US-Präsenz.'],
 ['RAF Lakenheath', 'USA', 'GBR', 0.56, 52.41, 'luft', 2, 'aktiv', 'Britischer Stützpunkt, genutzt von einem US-Kampfgeschwader.'],
 ['RAF Mildenhall', 'USA', 'GBR', 0.49, 52.36, 'luft', 3, 'aktiv', 'Tank- und Spezialflugzeuge der US-Luftwaffe.'],
 ['RAF Menwith Hill', 'USA', 'GBR', -1.69, 54.01, 'aufkl', 3, 'aktiv', 'Abhör- und Satellitenstation (NSA/GCHQ).'],
 ['Redzikowo (Aegis Ashore)', 'USA', 'POL', 17.11, 54.48, 'raketenabwehr', 3, 'aktiv', 'Landgestützte Raketenabwehranlage der NATO-Raketenabwehr.'],
 ['Powidz', 'USA', 'POL', 17.85, 52.38, 'heer', 3, 'aktiv', 'Lager für vorgehaltenes US-Gerät.'],
 ['Deveselu (Aegis Ashore)', 'USA', 'ROU', 24.41, 44.08, 'raketenabwehr', 3, 'aktiv', 'Raketenabwehranlage, seit 2016 in Betrieb.'],
 ['Mihail Kogălniceanu', 'USA', 'ROU', 28.49, 44.36, 'luft', 3, 'aktiv', 'Rumänischer Stützpunkt mit rotierenden US-Truppen.'],
 ['Souda Bay', 'USA', 'GRC', 24.15, 35.53, 'marine', 3, 'aktiv', 'Marine- und Luftstützpunkt auf Kreta.'],
 ['Camp Bondsteel', 'USA', 'XKX', 21.25, 42.36, 'heer', 3, 'aktiv', 'US-Lager im Rahmen der NATO-Mission KFOR.'],
 ['Lajes Field (Azoren)', 'USA', 'PRT', -27.09, 38.76, 'luft', 3, 'aktiv', 'Portugiesischer Stützpunkt mit US-Einheit im Atlantik.'],
 ['Pituffik Space Base', 'USA', 'GRL', -68.7, 76.53, 'aufkl', 2, 'aktiv', 'Raketenfrühwarnung und Weltraumüberwachung in Grönland (autonomer Teil des Königreichs Dänemark).'],
 ['Keflavík', 'USA', 'ISL', -22.61, 63.99, 'luft', 3, 'aktiv', 'Isländischer Flughafen mit rotierender US- und NATO-Präsenz (U-Boot-Jagd).'],
 # USA – Asien/Pazifik
 ['Yokosuka', 'USA', 'JPN', 139.67, 35.29, 'marine', 1, 'aktiv', 'Heimathafen der 7. US-Flotte.'],
 ['Kadena Air Base (Okinawa)', 'USA', 'JPN', 127.77, 26.36, 'luft', 1, 'aktiv', 'Größter US-Luftwaffenstützpunkt im Pazifik.'],
 ['Yokota Air Base', 'USA', 'JPN', 139.35, 35.75, 'luft', 2, 'aktiv', 'Hauptquartier der US-Streitkräfte in Japan.'],
 ['Misawa Air Base', 'USA', 'JPN', 141.37, 40.7, 'luft', 3, 'aktiv', 'Gemeinsam mit Japan genutzter Stützpunkt in Nordjapan.'],
 ['MCAS Iwakuni', 'USA', 'JPN', 132.24, 34.15, 'luft', 3, 'aktiv', 'Flugplatz der US-Marineinfanterie.'],
 ['Sasebo', 'USA', 'JPN', 129.72, 33.16, 'marine', 3, 'aktiv', 'Marinestützpunkt für Landungsschiffe.'],
 ['Camp Humphreys', 'USA', 'KOR', 127.03, 36.96, 'heer', 1, 'aktiv', 'Größter US-Stützpunkt im Ausland nach Fläche; Hauptquartier der US-Streitkräfte in Korea.'],
 ['Osan Air Base', 'USA', 'KOR', 127.03, 37.09, 'luft', 2, 'aktiv', 'Hauptquartier der 7. US-Luftflotte.'],
 ['Kunsan Air Base', 'USA', 'KOR', 126.62, 35.9, 'luft', 3, 'aktiv', 'US-Kampfgeschwader an der Westküste.'],
 ['Pine Gap', 'USA', 'AUS', 133.74, -23.8, 'aufkl', 2, 'aktiv', 'Gemeinsam von Australien und den USA betriebene Satellitenbodenstation.'],
 # USA – Nahost/Afrika/Amerika
 ['Naval Support Activity Bahrain', 'USA', 'BHR', 50.61, 26.21, 'marine', 1, 'aktiv', 'Hauptquartier der 5. US-Flotte.'],
 ['Al Udeid Air Base', 'USA', 'QAT', 51.31, 25.12, 'luft', 1, 'aktiv', 'Größter US-Stützpunkt im Nahen Osten, vorgeschobenes Hauptquartier von CENTCOM.'],
 ['Camp Arifjan', 'USA', 'KWT', 48.1, 28.9, 'heer', 2, 'aktiv', 'Logistik- und Führungsstützpunkt der US-Armee.'],
 ['Al Dhafra Air Base', 'USA', 'ARE', 54.55, 24.25, 'luft', 2, 'aktiv', 'Emiratischer Luftwaffenstützpunkt mit US-Einheiten.'],
 ['Prince Sultan Air Base', 'USA', 'SAU', 47.58, 24.06, 'luft', 2, 'aktiv', 'Saudischer Stützpunkt mit US-Präsenz (seit 2019 wieder).'],
 ['Muwaffaq Salti Air Base', 'USA', 'JOR', 36.78, 31.83, 'luft', 3, 'aktiv', 'Jordanischer Luftwaffenstützpunkt mit US-Einheiten.'],
 ['Al-Tanf', 'USA', 'SYR', 38.62, 33.5, 'heer', 3, 'geräumt 02/2026', 'Bis Februar 2026 US-Stützpunkt; Übergabe an die syrische Armee.'],
 ['Camp Lemonnier', 'USA', 'DJI', 43.15, 11.55, 'gemischt', 1, 'aktiv', 'Einziger ständiger US-Stützpunkt in Afrika.'],
 ['Camp Simba (Manda Bay)', 'USA', 'KEN', 40.91, -2.25, 'luft', 3, 'aktiv', 'Kenianischer Marinestützpunkt mit US-Einheit.'],
 ['Soto Cano Air Base', 'USA', 'HND', -87.62, 14.38, 'luft', 3, 'aktiv', 'Honduranischer Stützpunkt mit US-Einsatzgruppe Joint Task Force-Bravo.'],
 ['Guantánamo Bay', 'USA', 'CUB', -75.13, 19.9, 'marine', 2, 'aktiv', 'US-Marinestützpunkt auf Kuba, gepachtet seit 1903; Kuba betrachtet die Nutzung als unrechtmäßig.'],
 # Russland
 ['102. Militärbasis Gjumri', 'RUS', 'ARM', 43.85, 40.79, 'heer', 2, 'aktiv', 'Russischer Stützpunkt in Armenien, Vertrag bis 2044.'],
 ['Luftwaffenbasis Kant', 'RUS', 'KGZ', 74.85, 42.85, 'luft', 3, 'aktiv', 'Russischer Luftwaffenstützpunkt in Kirgisistan (OVKS).'],
 ['201. Militärbasis Duschanbe', 'RUS', 'TJK', 68.78, 38.56, 'heer', 2, 'aktiv', 'Größter russischer Landstützpunkt im Ausland.'],
 ['Operative Gruppe Transnistrien', 'RUS', 'MDA', 29.62, 46.84, 'heer', 3, 'aktiv', 'Russische Truppen in Transnistrien (Teil Moldaus, nicht von Moldau kontrolliert); Moldau fordert den Abzug.'],
 ['Gudauta (Abchasien)', 'RUS', 'GEO', 40.63, 43.11, 'heer', 3, 'aktiv', 'Russischer Stützpunkt in Abchasien; Russland erkennt Abchasien an, international überwiegend als Teil Georgiens betrachtet.'],
 ['Zchinwali (Südossetien)', 'RUS', 'GEO', 43.96, 42.23, 'heer', 3, 'aktiv', 'Russischer Stützpunkt in Südossetien; Russland erkennt Südossetien an, international überwiegend als Teil Georgiens betrachtet.'],
 ['Sewastopol (Schwarzmeerflotte)', 'RUS', 'UKR', 33.52, 44.62, 'marine', 1, 'aktiv', 'Hauptstützpunkt der russischen Schwarzmeerflotte auf der Krim; die Krim wurde 2014 von Russland annektiert und wird international überwiegend als Teil der Ukraine anerkannt.'],
 ['Hmeimim', 'RUS', 'SYR', 35.95, 35.4, 'luft', 2, 'Umbau vereinbart 08/2026', 'Russischer Luftwaffenstützpunkt; laut Memorandum vom 09.08.2026 wird er binnen drei Monaten zu einem gemeinsamen Ausbildungszentrum, der zivile Flughafen geht an den syrischen Staat.'],
 ['Tartus', 'RUS', 'SYR', 35.87, 34.9, 'marine', 2, 'Umbau vereinbart 08/2026', 'Russischer Marine-Versorgungspunkt; laut Memorandum vom 09.08.2026 Umwandlung in ein gemeinsames Ausbildungszentrum, der 4. Handelsliegeplatz geht schrittweise an die syrische Zivilverwaltung.'],
 ['Kosmodrom Baikonur', 'RUS', 'KAZ', 63.31, 45.92, 'raumfahrt', 2, 'aktiv', 'Von Russland gepachteter Raumfahrtbahnhof (Pacht bis 2050).'],
 # China
 ['Stützpunkt Dschibuti', 'CHN', 'DJI', 43.08, 11.59, 'marine', 1, 'aktiv', 'Erster Auslandsstützpunkt der chinesischen Volksbefreiungsarmee, 2017 eröffnet.'],
 ['Marinestützpunkt Ream', 'CHN', 'KHM', 103.52, 10.5, 'marine', 3, 'umstritten', 'Kambodschanischer Stützpunkt, mit chinesischer Hilfe ausgebaut; chinesische Kriegsschiffe lagen dort; Kambodscha und China bestreiten einen exklusiven chinesischen Stützpunkt.'],
 # Frankreich
 ['Französische Streitkräfte Dschibuti', 'FRA', 'DJI', 43.16, 11.54, 'gemischt', 1, 'aktiv', 'Größter französischer Auslandsstützpunkt, künftig Hauptquartier für Afrika.'],
 ['Französische Streitkräfte VAE (Abu Dhabi)', 'FRA', 'ARE', 54.38, 24.52, 'marine', 2, 'aktiv', 'Marine-, Luft- und Heeresstützpunkt seit 2009.'],
 ['Camp de Gaulle Libreville', 'FRA', 'GAB', 9.43, 0.41, 'heer', 3, 'gemeinsam genutzt seit 2025', 'Ehemaliger französischer Stützpunkt, seit 2025 gemeinsames Lager mit Gabun.'],
 ['Kossei (N’Djamena)', 'FRA', 'TCD', 15.04, 12.13, 'luft', 3, 'geräumt 01/2025', 'Im Januar 2025 an den Tschad übergeben.'],
 ['Port-Bouët (Abidjan)', 'FRA', 'CIV', -3.93, 5.25, 'heer', 3, 'geräumt 02/2025', 'Im Februar 2025 an die Elfenbeinküste übergeben.'],
 ['Camp Geille (Dakar)', 'FRA', 'SEN', -17.49, 14.74, 'heer', 3, 'geräumt 07/2025', 'Am 17. Juli 2025 an Senegal übergeben.'],
 # Großbritannien
 ['RAF Akrotiri', 'GBR', 'CYP', 32.99, 34.59, 'luft', 1, 'aktiv', 'Britische Militärbasis mit Hoheitsrecht (Sovereign Base Area) auf Zypern.'],
 ['Dhekelia', 'GBR', 'CYP', 33.72, 34.99, 'heer', 3, 'aktiv', 'Zweite britische Sovereign Base Area auf Zypern.'],
 ['Diego Garcia', 'GBR', 'IOT', 72.41, -7.31, 'gemischt', 1, 'aktiv', 'Britisch-amerikanischer Stützpunkt im Chagos-Archipel; von Mauritius beansprucht. Vertrag über die Übergabe der Souveränität an Mauritius am 22.05.2025 unterzeichnet (Stützpunkt bliebe 99 Jahre unter britischer Verwaltung), bis 10/2026 nicht in Kraft.'],
 ['Mount Pleasant (Falklandinseln)', 'GBR', 'FLK', -58.45, -51.82, 'luft', 2, 'aktiv', 'Britischer Stützpunkt; die Inseln werden von Argentinien beansprucht.'],
 ['Gibraltar', 'GBR', None, -5.35, 36.14, 'marine', 3, 'aktiv', 'Marinestützpunkt im britischen Überseegebiet Gibraltar; Spanien beansprucht das Gebiet.'],
 ['British Army Training Unit Kenya (Nanyuki)', 'GBR', 'KEN', 37.07, 0.02, 'ausbildung', 3, 'aktiv', 'Britisches Übungszentrum in Kenia.'],
 ['BATUS Suffield', 'GBR', 'CAN', -111.17, 50.27, 'ausbildung', 3, 'aktiv (eingeschränkt)', 'Britisches Übungsgelände in Kanada; laut Verteidigungsministerium 2025/26 nur wenige Übungen, weitere Nutzung offen (Stand 01/2026).'],
 ['HMS Jufair (Bahrain)', 'GBR', 'BHR', 50.61, 26.2, 'marine', 3, 'aktiv', 'Britischer Marinestützpunkt, 2018 eröffnet.'],
 ['Duqm (Oman)', 'GBR', 'OMN', 57.7, 19.65, 'marine', 3, 'aktiv', 'Britisches Logistikzentrum im Hafen Duqm.'],
 ['Seria (Brunei)', 'GBR', 'BRN', 114.32, 4.61, 'heer', 3, 'aktiv', 'Britisches Gurkha-Bataillon in Brunei.'],
 ['BATSUB (Belize)', 'GBR', 'BLZ', -88.33, 17.54, 'ausbildung', 3, 'aktiv', 'Britische Dschungel-Ausbildungseinheit.'],
 ['RAF Ascension', 'GBR', 'SHN', -14.39, -7.97, 'luft', 3, 'aktiv', 'Flugplatz auf Ascension (britisches Überseegebiet), auch von den USA genutzt.'],
 ['Tapa (Estland)', 'GBR', 'EST', 25.96, 59.26, 'heer', 3, 'aktiv', 'Britisch geführte NATO-Kampfgruppe in Estland.'],
 # Türkei
 ['Türkische Streitkräfte in Nordzypern', 'TUR', 'CYN', 33.35, 35.2, 'heer', 2, 'aktiv', 'Türkische Truppen seit 1974; die Türkische Republik Nordzypern wird nur von der Türkei anerkannt und gilt völkerrechtlich als Teil der Republik Zypern.'],
 ['Stützpunkt Tariq bin Ziyad (Katar)', 'TUR', 'QAT', 51.43, 25.2, 'heer', 2, 'aktiv', 'Türkischer Stützpunkt bei Doha seit 2015/2017. Lage nicht bestätigt (nur ungefähr).'],
 ['Camp TURKSOM Mogadischu', 'TUR', 'SOM', 45.29, 2.01, 'ausbildung', 2, 'aktiv', 'Größtes türkisches Ausbildungszentrum im Ausland, seit 2017.'],
 ['Baschika (Irak)', 'TUR', 'IRQ', 43.35, 36.45, 'heer', 3, 'Übergabe vereinbart 09/2026', 'Türkisches Lager nahe Mossul seit 2015; am 23.09.2026 vereinbarten Irak und Türkei die schrittweise Übergabe an Bagdad (ohne festen Zeitplan).'],
 ['Al-Watiya (Libyen)', 'TUR', 'LBY', 11.9, 32.47, 'luft', 3, 'nicht bestätigt', 'Libyscher Luftwaffenstützpunkt; türkische Nutzung seit 2020 belegt, nach einem Luftangriff im Juli 2020 Teilabzug. Heutiger Umfang der türkischen Präsenz nicht bestätigt.'],
 # Indien
 ['IMTRAT (Bhutan)', 'IND', 'BTN', 89.28, 27.39, 'ausbildung', 3, 'aktiv', 'Indisches Militärausbildungsteam in Bhutan seit 1961/62.'],
 ['Agaléga', 'IND', 'MUS', 56.6, -10.4, 'luft', 3, 'umstritten', 'Mit Indien gebaute Landebahn und Pier; Indien und Mauritius sprechen von Einrichtungen zur Seeüberwachung, nicht von einem Stützpunkt.'],
 # weitere Staaten
 ['Panzerbrigade 45 (Litauen)', 'DEU', 'LTU', 25.28, 54.69, 'heer', 2, 'aktiv', 'Erste dauerhaft im Ausland stationierte Brigade der Bundeswehr, 2025 aufgestellt.'],
 ['Japanische Selbstverteidigungskräfte Dschibuti', 'JPN', 'DJI', 43.15, 11.56, 'luft', 3, 'aktiv', 'Einziger Auslandsstützpunkt Japans, seit 2011.'],
 ['Italienische Basis Dschibuti (BMIS)', 'ITA', 'DJI', 43.1, 11.57, 'gemischt', 3, 'aktiv', 'Italienischer Stützpunkt seit 2013.'],
]
QX = {'Rose Barracks Vilseck': 'OSW, „The United States’ planned reduction of its military presence in Germany“ (05.05.2026); Stars and Stripes 14.05.2026',
      'Diego Garcia': 'Al Jazeera, „UK-Mauritius Chagos sovereignty deal stalls“ (02.10.2026); gov.uk Integrated Global Defence Network (28.08.2026)',
      'BATUS Suffield': 'UK Defence Journal, „Future of BATUS training use tied to Defence Investment Plan“ (27.01.2026, nach Antwort des MOD)',
      'Baschika (Irak)': 'Al Jazeera, „Turkiye agrees to gradual handover of Bashiqa base to Iraq“ (24.09.2026); FDD 07.10.2026',
      'Al-Watiya (Libyen)': 'Lage: Wikipedia „Al-Watiya Air Base“ (32°28′20″N 11°54′E)',
      'Hmeimim': 'The National, „Syria and Russia agree to transform military bases into joint training centres“ (09.08.2026)',
      'Tartus': 'The National, „Syria and Russia agree to transform military bases into joint training centres“ (09.08.2026)',
      'Al-Tanf': 'Al Jazeera, „Syrian army takes control of al-Tanf military base as US troops pull out“ (12.02.2026)'}
GB = {'RAF Akrotiri', 'Dhekelia', 'Gibraltar', 'Mount Pleasant (Falklandinseln)', 'RAF Ascension'}
daten = []
for n, b, g, lo, la, art, rg, st, t in S:
    assert b in APP and (g is None or g in APP), (n, b, g)
    e = {'n': n, 'betreiber': b, 'gast': g, 'lon': r2(lo), 'lat': r2(la), 'art': art, 'rang': rg, 'status': st, 't': t, 'q': Q[b] + ('; ' + QX[n] if n in QX else '') + ('; gov.uk „Integrated Global Defence Network“ (28.08.2026)' if n in GB else '')}
    if g is None: e['gebiet'] = 'Gibraltar'
    daten.append(e)
FARBE = {'USA': '#5a9ae8', 'RUS': '#e85a5a', 'CHN': '#ffcf5a', 'FRA': '#9a7ad8', 'GBR': '#4ad0c8', 'TUR': '#ff8a3d', 'IND': '#7ac86a',
         'DEU': '#d8d8d8', 'JPN': '#ff7ab0', 'ITA': '#a8c84a'}
import collections
z = collections.Counter(d['betreiber'] for d in daten); print(z, len(daten))
obj = {'id': 'stuetzpunkte', 'name': 'Militärstützpunkte im Ausland', 'gruppe': 'Politik', 'typ': 'punkte', 'einheit': '',
       'legende': [{'k': k, 'n': APP[k], 'c': FARBE[k], 'z': z[k]} for k in FARBE],
       'quellen': [{'t': v, 'u': {'USA': 'https://www.acq.osd.mil/eie/Downloads/BSI/Base%20Structure%20Report%20FY15.pdf', 'RUS': 'https://meduza.io/en/news/2026/08/10/russia-and-syria-agree-to-turn-russian-military-bases-into-joint-training-centers',
                                       'CHN': 'http://eng.mod.gov.cn/', 'FRA': 'https://www.aljazeera.com/news/2025/7/17/former-colonial-ruler-france-hands-over-its-last-military-bases-in-senegal',
                                       'GBR': 'https://commonslibrary.parliament.uk/', 'TUR': 'https://www.msb.gov.tr/', 'IND': 'https://www.mea.gov.in/',
                                       'DEU': 'https://www.bundeswehr.de/', 'JPN': 'https://www.mod.go.jp/en/', 'ITA': 'https://www.difesa.it/'}[k],
                    'stand': '11/2026', 'lizenz': 'Fakten aus amtlichen Angaben/Presse; US-Bericht gemeinfrei'} for k, v in Q.items()]
                  + [{'t': 'Lage: Koordinaten nach Wikipedia/Wikidata, gerundet; Gegenprüfung 25.11.2026 gegen Natural Earth 10m (Flughäfen, Häfen) und GeoNames, Abweichung je Punkt ≤ 0,2°', 'u': 'https://www.naturalearthdata.com/', 'stand': '11/2026', 'lizenz': 'CC0 / gemeinfrei (Natural Earth), CC BY 4.0 (GeoNames, nur Abgleich)'}],
       'hinweis': 'Auswahl größerer, öffentlich belegter Standorte nach denselben Regeln für alle Staaten (eigenes Personal dauerhaft oder rotierend im Gastland). '
                  'Gemeinsam genutzte Stützpunkte des Gastlandes sind dabei, wenn der Betreiber dort eigene Einheiten hat. Umstrittene Gebiete sind im Text benannt. '
                  'Keine vollständige Liste; geheime oder unbelegte Standorte fehlen.',
       'felder': {'betreiber': 'ISO3 des betreibenden Staates', 'gast': 'ISO3 des Gebiets laut App-Karte', 'art': 'luft, marine, heer, fuehrung, aufkl, raketenabwehr, raumfahrt, ausbildung, sanitaet, gemischt',
                  'status': 'aktiv / geräumt MM/JJJJ / umstritten …', 'rang': '1–3', 'q': 'Beleg'},
       'daten': daten}
schreibe(obj)
