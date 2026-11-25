# Prüfbericht Themen-Ebenen (unabhängige Gegenprüfung, 25.11.2026)

Vorgehen: Jede Angabe gegen eine benannte, unabhängige Quelle (amtliche Seite bevorzugt) geprüft; Korrekturen in `prep/*.py` eingetragen, `fertig/` mit `bash prep/alle.sh` neu erzeugt, `prep/pruefen.py` ohne Fehler. Lagen: Abgleich gegen Natural Earth 10m (Flughäfen, Häfen, Orte) und GeoNames (`geonamescache` 3.0.2) bzw. Nachschlagen; Schwelle 0,2°.
Nicht bestätigte Angaben stehen im Datensatz mit dem Zusatz „nicht bestätigt“ im Text/`hinweis` (EINBAU.md kennt kein eigenes Feld dafür).

## 1. Bündnisse (`buendnisse.json`) – 18 Listen geprüft

| Bündnis | Ergebnis | Quelle (abgerufen 25.11.2026) |
|---|---|---|
| NATO | 32 Mitglieder, alle Beitrittsjahre bestätigt | nato.int „NATO member countries“ (Seite aktualisiert 11.03.2024) <https://www.nato.int/fr/about-us/organization/nato-member-countries?selectedLocale=en> |
| EU | 27 Mitglieder; 9 Kandidaten + Kosovo als potenzieller Kandidat bestätigt | <https://european-union.europa.eu/principles-countries-history/eu-enlargement_en> |
| Eurozone | 21 (Bulgarien 01.01.2026) bestätigt | EZB-Pressemitteilung 01.01.2026 (wie bisher) |
| Schengen | 29 (25 EU + ISL, NOR, CHE, LIE), BGR/ROU 01.01.2025 bestätigt; Hinweis zu Irland/Zypern präzisiert | <https://home-affairs.ec.europa.eu/policies/schengen/schengen-area_en> |
| BRICS | 11 Mitglieder, 10 Partner bestätigt; Erklärung Neu-Delhi 12.09.2026 nennt keine Neuaufnahmen | Business Today 10.09.2026; pmindia.gov.in (New Delhi Declaration) |
| SOZ | 10 Mitglieder, 2 Beobachter, 15 Dialogpartner (mit Laos) bestätigt; Beschluss Tianjin 2025 „SCO Partner“, Alt-Status gilt bis Inkrafttreten | eng.sectsco.org 06.03.2026 und 01.09.2026 |
| OVKS | Armenien: Stimmrecht am 11.11.2026 entzogen, Mitgliedschaft bleibt – bestätigt | The Moscow Times 18.11.2026 |
| EAWU | 5 Mitglieder bestätigt. **Ergänzt:** Beobachter Moldau (2018), Usbekistan, Kuba (2020), Iran (26.12.2024) | eec.eaeunion.org (Observer state status); intellinews (Iran) |
| OPEC / OPEC+ | VAE-Austritt zum 01.05.2026 bestätigt, 11 OPEC-Mitglieder. **Ergänzt:** Brasilien als Mitglied der Kooperations-Charta 2025 (`partner`) | Enerdata; opec.org Pressemitteilung 18.02.2025 |
| ASEAN | 11 (Timor-Leste 26.10.2025) bestätigt; Quellenadresse auf ASEAN-Meldung umgestellt | <https://asean.org/forging-a-new-era-timor-leste-admitted-into-asean/> |
| AU | 55 Mitglieder; Suspendierungen BFA, GNB, MDG, MLI, NER, SDN (Stand 26.02.2026), Aufhebung Guinea 22.01.2026 bestätigt; bis 11/2026 keine weitere Änderung gefunden (Sudan-Antrag 02/2026 abgelehnt) | Amani Africa 26.02.2026; AllAfrica 13.02.2026 |
| Arabische Liga | 22 Mitglieder, alle Beitrittsjahre bestätigt | Britannica „Arab League“ |
| G7, G20, AUKUS | unverändert, bestätigt (G20: US-Vorsitz 2026 ohne Einladung Südafrikas, formale Mitgliedschaft unverändert) | bisherige Belege |
| Five Eyes | **Korrigiert:** Kanada 1948 → 1949 (Hinweis auf NSA-Dokumente mit 1948 ergänzt) | GCHQ „A brief history of UKUSA“ <https://www.gchq.gov.uk/information/brief-history-of-ukusa> |
| Mercosur | Vertragsstaaten, Suspendierung Venezuelas, 7 assoziierte Staaten bestätigt; Hinweis Venezuela (Protokoll 2006, Vollmitglied 2012) ergänzt | <https://betaweb.mercosur.int/en?p=36341> |

Summe: 18 geprüft, 15 unverändert bestätigt, 3 korrigiert/ergänzt (Five Eyes, EAWU, OPEC+), 0 entfernt. Offen: OVKS-Beitrittsjahr Georgiens (1993/1994, je nach Zählung Unterzeichnung/Inkrafttreten) nicht an amtlicher Seite geprüft.

## 2. Militärstützpunkte (`stuetzpunkte.json`) – 92 Einträge

**Lage:** alle 92 automatisch gegen Natural Earth 10m (airports, ports), Natural Earth populated places und GeoNames (geonamescache 3.0.2, Orte ≥ 1.000 Ew.) abgeglichen (nächster passender Flugplatz/Hafen/Ort, Namensabgleich von Hand). 90 innerhalb 0,1°, Baikonur (Startgelände, nicht Stadt) und Pine Gap plausibel.
- **Korrigiert:** Al-Watiya (Libyen) 12,03° O → 11,90° O (Wikipedia „Al-Watiya Air Base“: 32°28′20″N 11°54′E; Abweichung 0,13°, unter der Schwelle, aber eindeutig).
- **Nicht bestätigt:** Lage des türkischen Stützpunkts in Katar (Tariq bin Ziyad) – im Text als „Lage nicht bestätigt“ gekennzeichnet.

**Status/Betreiber geprüft (Websuche, 25.11.2026):**
| Eintrag | Ergebnis | Quelle |
|---|---|---|
| Al-Tanf | bestätigt: US-Abzug, Übernahme durch syrische Armee 12.02.2026 | Al Jazeera 12.02.2026 |
| Hmeimim, Tartus | bestätigt, Text präzisiert: Memorandum 09.08.2026, Umwandlung in gemeinsame Ausbildungszentren binnen 3 Monaten; ziviler Flughafen bzw. 4. Liegeplatz an Syrien | The National 09.08.2026 |
| Diego Garcia | bestätigt, Text präzisiert: Vertrag 22.05.2025, nicht in Kraft (10/2026) | Al Jazeera 02.10.2026 |
| **Baschika (Irak)** | **korrigiert:** Status „aktiv“ → „Übergabe vereinbart 09/2026“ (Vereinbarung 23.09.2026, ohne Zeitplan) | Al Jazeera 24.09.2026; FDD 07.10.2026 |
| **Al-Watiya** | **korrigiert:** „aktiv“ → „nicht bestätigt“ (Nutzung 2020 belegt, danach Teilabzug; heutiger Umfang ohne Beleg) | Wikipedia (Ereignisse 2020) |
| **Rose Barracks Vilseck** | **ergänzt:** Abzugsankündigung 5.000 US-Soldaten (01.05.2026); Betroffenheit des 2. Kavallerieregiments amtlich nicht bestätigt | OSW 05.05.2026; Stars and Stripes 14.05.2026 |
| **BATUS Suffield** | **korrigiert:** „aktiv“ → „aktiv (eingeschränkt)“; weitere Nutzung laut MOD offen | UK Defence Journal 27.01.2026 |
| Akrotiri, Dhekelia, Gibraltar, Mount Pleasant, Ascension | bestätigt | gov.uk „Integrated Global Defence Network“ (aktualisiert 28.08.2026) |
| BATUK (Nanyuki), Belize, Brunei (Seria), Tapa (Estland) | bestätigt | British Army „Where we are“ |
| Ream | Status „umstritten“ bestätigt (beide Regierungen bestreiten einen chinesischen Stützpunkt; chinesische Schiffe dauerhaft präsent laut AMTI) | AMTI/CSIS; Military Times 06.02.2026 |
| US-Präsenz Europa allgemein | keine amtlich bekanntgegebene Schließung eines der 30 geführten Standorte; DoD-Überprüfung seit 18.06.2026 | CRS IF11130 (30.06.2026) |
| Frankreich Afrika (4) | wie bisher belegt (Al Jazeera 17.07.2025) | – |

Summe: 92 geprüft (Lage), davon Status einzeln per Quelle 26; korrigiert 5 (Al-Watiya Lage+Status, Baschika, BATUS, Vilseck-Text), präzisiert 3 (Hmeimim, Tartus, Diego Garcia), entfernt 0.
Offen: Status der übrigen ~66 lange bestehenden Standorte (v. a. US in Japan, Korea, Golf, Italien, Spanien; Russland in Zentralasien/Kaukasus; Türkei Katar/Somalia) nicht einzeln an amtlicher Quelle 2026 geprüft – keine Hinweise auf Änderungen gefunden. Der DoD Base Structure Report (FY2015) bleibt die letzte öffentliche Gesamtliste.

## 3a. Frühe Stätten (`fruehe_staetten.json`) – 78 Einträge

**Lage:** alle 78 gegen den nächstgelegenen GeoNames-Ort bzw. den namengebenden Nachbarort geprüft; alle innerhalb 0,25° des Nachbarorts und im richtigen Land (Abweichungsmarken im Prüflauf nur durch gleichnamige Orte in anderen Ländern). Keine Lagekorrektur nötig. Chauvet zusätzlich gegen Wikipedia-Koordinaten (44,39/4,41) bestätigt.

**Datierung:** Stichprobe von 15 Stätten gegen Fachquellen; die übrigen 63 entsprechen der gängigen Darstellung (nicht einzeln belegt).
| Stätte | alt | neu | Quelle |
|---|---|---|---|
| Höhle von Lascaux | ca. 17.000–15.000 v. Chr. | ca. 21.500–21.000 Jahre vor heute (ca. 19.500–19.000 v. Chr.); ältere Schätzung 17.000–18.000 Jahre vermerkt | frz. Kulturministerium, „Dating the figures of Lascaux“ (Projekt LAsCO) <https://archeologie.culture.gouv.fr/lascaux/en/dating-figures-lascaux> |
| Grotte Chauvet | ca. 36.000–28.000 v. Chr. (Jahre vor heute als v. Chr. gelesen) | 37.000–33.500 und 31.000–28.000 Jahre vor heute (ca. 35.000–26.000 v. Chr.) | Quiles u. a., PNAS 2016 (Wiedergabe Wikipedia „Chauvet Cave“) |
| Höhle von Altamira | ca. 36.000–13.000 v. Chr. | 35.000–15.200 Jahre vor heute (ca. 33.000–13.200 v. Chr.) | CENIEH, Pressemitteilung U-Serien-Datierung <https://www.cenieh.es/en/press/news/uranium-series-dating-confirms-20000-years-cave-art-altamira> |
| Çatalhöyük | ca. 7100–5700 v. Chr. | Osthügel ca. 7400–6200 v. Chr., Westhügel jünger | Türkisches Kulturministerium (Museen), UNESCO-Beschreibung <https://turkishmuseums.com/blog/detail/unesco-sites-of-turkiye-catalhoyuk-neolithic-site/10076/4> |
| Palenque | Feld `von` 500 (Text 600–800) | `von` 600 (innerer Widerspruch behoben) | eigener Text |
| Cairn von Barnenez | 4500–3900 v. Chr. | bestätigt | Tourisme Bretagne (Regionalamt) |
| Hohlenstein-Stadel, Hohle Fels | ca. 40.000 Jahre | bestätigt (Feld −38.000 = Jahre v. Chr.) | Welterbe Höhlen der Schwäbischen Alb |
| Göbekli Tepe, Stonehenge, Avebury, Newgrange, Giza, Ur, Liangzhu, Nan Madol | wie bisher | bestätigt (gängige Darstellung) | – |

Summe: 78 geprüft (Lage), 15 Datierungen einzeln belegt, 5 korrigiert, 0 entfernt. Offen: Einzelbelege für die übrigen Datierungen.

## 3b. Engstellen (`energie_engstellen.json`) – 10 Einträge

Alle Öl- und LNG-Werte gegen EIA „World Oil Transit Chokepoints“ (aktualisiert 03.03.2026), Tabelle 1 und LNG-Tabelle, Spalte 1H25 geprüft: **alle 9 bezifferten Werte bestätigt** (Malakka 23,2/9,2; Hormus 20,9/11,4; Suez+SUMED 4,9/0,9; Bab al-Mandab 4,2/0,0; Dänische Meerengen 4,9/1,6; Bosporus 3,3 (Tab. 6, kein LNG); Dardanellen 3,7/0,6; Panama 2,3 (Fiskaljahr 2025, LNG < 0,3); Kap der Guten Hoffnung 9,1/5,7). Gibraltar ohne EIA-Wert (richtig). Hormus-Text 2026 gegen EIA Today in Energy 19.11.2026 bestätigt (2. Quartal stark eingeschränkt, 3. Quartal +19 % für die drei Nahost-Engstellen zusammen; Quartalszahlen nur in Grafik). Lagen plausibel (Punkte auf See). 10 geprüft, 0 korrigiert.

## 4. Öl- und Gasleitungen (`energie_leitungen.json`) – 34 Leitungen

**Verlauf:** alle 34 Linienzüge automatisch in 0,05°-Schritten gegen die Länderumrisse der App geprüft (durchquerte Staaten vs. Feld `laender`). Danach **11 Verläufe korrigiert**:
| Leitung | Fehler | Korrektur |
|---|---|---|
| Nord Stream 1/2 | Wegpunkt (15,0/55,2) lag auf Bornholm | Umgehung östlich von Bornholm (15,6/55,1) |
| Kirkuk–Ceyhan | Linie lief durch Syrien | Wegpunkte nördlich der Grenze über Fishkhabur–Mardin–Gaziantep |
| Habshan–Fudschaira (ADCOP) | Linie lief durch Oman (Buraimi) | Wegpunkte über emiratisches Gebiet |
| Zentralasien–China | Linie lief durch Kirgistan | über Taras–Schu–Kaptschagai (Kasachstan) |
| ESPO | Linie schnitt chinesisches Gebiet am Amur | entlang der Transsib: Belogorsk–Archara–Birobidschan–Chabarowsk |
| Kraft Sibiriens | Linie schnitt China nördlich des Amur und querte das Gelbe Meer | Skoworodino–Blagoweschtschensk; in China über Land (Shenyang–Qinhuangdao–Shandong–Jiangsu) |
| CPC | Linie lief über das Kaspische Meer | nördlich am Ufer entlang |
| Arabische Gaspipeline | Linie lief über israelisches Gebiet (Eilat) | Unterwasserabschnitt Taba–Akaba im Golf |
| TurkStream | Endpunkt in Serbien, Ungarn fehlte | Endpunkt Kiskundorozsma (Ungarn) |
| OPAL | Endpunkt vor der Grenze, Tschechien fehlte | Endpunkt Brandov (Tschechien) |
| Druschba | Schwedt lag im polnischen Umriss, Tschechien ohne Linie | Endpunkt Schwedt korrigiert; Abzweig Bratislava–Kralupy ergänzt |
| Dolphin | Oman ohne Linie | Ras Laffan–Taweelah, Taweelah–Fudschaira, Al Ain–Oman (Oil & Gas Journal 06.11.2008) |
| Langeled, Baltic Pipe | Endpunkte knapp auf See | an Land gesetzt (Easington, Niechorze) |
Verbleibend erklärbar: Baltic Pipe beginnt im norwegischen Nordsee-Sektor (Norwegen ohne Landberührung).

**Status 11/2026 geprüft:**
| Leitung | Ergebnis | Quelle |
|---|---|---|
| Druschba | bestätigt (Unterbrechung ab 27.01.2026, Wiederaufnahme April, Mai normal); **ergänzt:** Tschechien seit April 2025 ohne russisches Öl | The Moscow Times 16.02.2026; bne intellinews 04.06.2026; OSW 18.04.2025, tschech. Regierung |
| **Kirkuk–Ceyhan** | **korrigiert:** Status „Wiederaufnahme 09/2025 berichtet“ → Unterbrechung Anfang März 2026, seit Einigung 17.03.2026 rund 250.000 b/Tag; Kapazität „bis 1,6 Mio.“ → „ca. 1,2 Mio. b/Tag (Reuters)“ | The National 16./18.03.2026; Shafaq News 20.03.2026 |
| CPC | bestätigt „in Betrieb“ (Angriff 06.04.2026 auf Anlegeboje, Export laut Kasachstan stabil); Text „2025 mehrfach beeinträchtigt“ bleibt richtig | MarineLink/Reuters 07.04.2026 |
| TurkStream | bestätigt in Betrieb (Lieferungen Jan.–Aug. 2026 11,9 Mrd. m³) | tks.ru 01.09.2026 |
| East-West-Pipeline | **gekennzeichnet:** Kapazität „ca. 5 Mio. (EIA)“ → „Auslegung, nicht amtlich bestätigt“; EIA nennt nur zusammen mit ADCOP 4,7 Mio. b/Tag Umgehungskapazität | EIA World Oil Transit Chokepoints (03.03.2026) |
| SUMED | 2,5 Mio. b/Tag bestätigt | EIA |
| Nord Stream 1/2, Jamal, ukrain. Transit, GME | Status wie bisher (Ereignisse 2021–2025, keine Änderung 2026 gefunden) | bisherige Belege |

Summe: 34 geprüft (Verlauf), 13 Verläufe korrigiert, 3 Status/Kapazitäten korrigiert bzw. gekennzeichnet, 0 entfernt. Offen: Kapazitäten der übrigen 29 Leitungen sind Betreiberangaben aus dem Wissensbestand, plausibel, aber nicht einzeln an den Betreiberseiten abgerufen. Das Format hat kein Längenfeld; Längen wurden nicht geprüft.

## 5. Handelswege, Entdeckungsfahrten, Reiche

**Reiche (`reiche.json`, 17):** Fläche und Jahr der größten Ausdehnung für alle 17 gegen Wikipedia „List of largest empires“ (abgerufen 25.11.2026) geprüft – **alle bestätigt** (z. B. Britisches Empire 35,5 Mio. km² 1920, Mongolen 24,0 1270, Rom 5,0 117). Hauptstadt-Lagen plausibel. Länderlisten auf grobe Fehler geprüft: **korrigiert** Osmanisches Reich 1683 – Armenien und Aserbaidschan entfernt (1683 safawidisch, Hinweis im Text), Kuwait entfernt (Gebiet um 1670 an die Banu Chalid verloren; keine Quelle für osmanische Herrschaft 1683). Übrige Listen ohne groben Fehler (bleiben „schematisch“). `schema:true` bei allen 17.

**Entdeckungsfahrten (`entdeckungsfahrten.json`, 9):** Jahre und Stationen gegen die gängige Darstellung (Britannica-Artikel je Reise) geprüft – keine Jahresfehler. Linien in 0,05°-Schritten gegen Länderumrisse geprüft; **korrigiert:**
- Cook (1768–71): Endpunkt −1,4° (Binnenland bei Andover) → **+1,4° O (The Downs, Kent)**; Seeweg an Queensland, Java (über Savu und die Sundastraße) und Südamerika (Le-Maire-Straße) nicht mehr über Land.
- Dias, da Gama: Linien liefen quer durch Westafrika, Angola, Südafrika, Mosambik, Tansania → Küstenwegpunkte auf See ergänzt.
- Magellan: Linie lief durch Brasilien, Uruguay, Patagonien → Küstenwegpunkte (Río de la Plata, Golf San Matías, Cabo Vírgenes).
Verbleibende Berührungen nur kleiner Inseln/Kaps (Madeira, Kapverden, Sokotra, Inselketten) – für schematische Linien belassen. `schema:true` bei allen 9.

**Handelswege (`handelswege.json`, 10):** Zeiträume plausibel (z. B. Via Appia 312 v. Chr., letzter Hansetag 1669, letzte Sklavenfahrt 1866/67). Orte gegen GeoNames: alle abgelegenen Orte (Ktesiphon, Berenike, Schabwa, Hegra, Teghaza, Tadmekka, Banda) an ihrer bekannten Lage. **Korrigiert:** Gewürzroute (Kaproute) und Atlantischer Dreieckshandel liefen über Land (Südafrika, Mosambik, Westafrika-Küste, Kuba, Irland) → Küstenwegpunkte ergänzt. `schema:true` bei allen 10.

Summe: 36 Objekte geprüft, 7 korrigiert (Osmanen, Cook, Dias, da Gama, Magellan, Gewürzroute, Dreieckshandel), 0 entfernt.

## 6. Staatsschulden, Goldreserven, Währungen

**Staatsschulden (`staatsschulden.json`, 114 Länder):** 44 Werte (Spalte 2025) direkt gegen IWF Fiscal Monitor April 2026, Statistischer Anhang <https://www.imf.org/-/media/files/publications/fiscal-monitor/2026/april/english/msa.pdf> (Tab. A7, A15, A21) abgelesen – **alle 44 bestätigt**, 0 Abweichungen:
- alle G20-Staaten mit Wert: ARG 80,3 · AUS 51,0 · BRA 93,3 · CAN 113,5 · CHN 99,2 · FRA 116,0 · DEU 62,9 · IND 84,1 · IDN 41,0 · ITA 137,1 · JPN 206,5 · KOR 52,3 · MEX 61,8 · RUS 17,2 · SAU 31,7 · ZAF 78,6 · TUR 23,5 · GBR 102,3 · USA 123,9
- alle Nachbarn Deutschlands: DNK 27,5 · POL 58,8 · CZE 44,6 · AUT 80,5 · CHE 39,4 · LUX 27,0 · BEL 106,3 · NLD 43,3 (FRA s. o.)
- weitere: ESP 100,4 · GRC 145,7 · SGP 171,3 · HUN 75,2 · EGY 86,8 · LBN 139,4 · BHR 147,6 · UKR 108,7 · VEN 308,7 · ROU 60,6 · PAK 72,8 · NGA 35,5 · SEN 130,2 · SDN 187,6 · KEN 69,3 · MOZ 102,5 · LAO 80,6
Zusammen mit den 4 bereits gegengeprüften Ländern (JPN, DEU, SGP, USA) sind 44 von 114 Werten belegt geprüft; die übrigen 70 stammen aus derselben Tabelle, nicht einzeln abgelesen.
**Nutzungsbedingungen IWF geklärt** (IMF Copyright and Usage, <https://www.imf.org/en/about/copyright-and-terms>): Herunterladen, Weitergeben und Veröffentlichen der Daten erlaubt, wenn unverändert und mit Quellenangabe („Source: International Monetary Fund, …“); wesentliche Umrechnungen kenntlich machen; **kommerzielle Weiterverwendung nur nach Anfrage/Genehmigung (copyright@imf.org)**; keine automatisierte Massenabfrage. Lizenzzeile im Datensatz entsprechend angepasst.

**Goldreserven (`goldreserven.json`, 22):** Die 10 größten Werte gegen die WGC-Tabelle nach IWF IFS (Stand 02/2026, Auszug bei goldreporter.de) geprüft: USA 8.133,5 · DEU 3.350,3 · FRA 2.437,0 · RUS 2.326,5 · CHN 2.306,3 · CHE 1.039,9 · JPN 846,0 bestätigt; ITA 2.451,8 (WGC 2.451,9) und IND 880,3 (WGC 880,2) – Rundungsunterschied, belassen. Die übrigen 18 Länder sind gegen BullionVault (17.08.2026, nach IWF IFS) bestätigt.
**Nicht vervollständigt:** Die vollständige Tabelle „World Official Gold Holdings“ ist nur als Download nach Anmeldung erhältlich, und die **WGC-Nutzungsbedingungen verbieten Kopie/Weiterverbreitung ohne vorherige schriftliche Erlaubnis** (<https://gold.org/terms-and-conditions>); deshalb nicht übernommen. Der IWF-Datensatz IRFCL/IFS war nur über data.imf.org (Skriptseite) bzw. DBnomics (Stand 31.08.2025, veraltet) erreichbar, die IWF-Länderseiten antworteten nicht. Hinweis zu den WGC-Bedingungen im Datensatz ergänzt. Offen: Vervollständigung über IWF IFS (erlaubt mit Quellenangabe) von einem Rechner mit Zugang zu data.imf.org.

**Währungen (`waehrungen.json`):** Währungsunionen gegen bekannte Mitgliedschaften geprüft: Euro (21 Eurozone + 4 per Abkommen + MNE/XKX einseitig + Überseegebiete) ✓, CFA-Franc BCEAO 8 (BEN BFA CIV GNB MLI NER SEN TGO) ✓, BEAC 6 (CAF CMR COG GAB GNQ TCD) ✓, Ostkaribischer Dollar 8 ✓, US-Dollar als (Mit-)Währung 18 (u. a. ECU, SLV, PAN, TLS, ZWE, FSM, MHL, PLW) ✓, Gemeinsames Währungsgebiet Rand (LSO, NAM), Indische Rupie in Bhutan ✓. **Korrigiert:** Curaçao/Sint Maarten Anzeige „XCG“ → „Karibischer Gulden“; **ergänzt:** Nordzypern (Türkische Lira) und Somaliland (Somaliland-Schilling, kein ISO-Code) – beide fehlten. Haiti steht wie in CLDR/ISO 4217 mit Gourde und US-Dollar. Offen: Liberia – laut älteren Berichten ist der US-Dollar neben dem Liberianischen Dollar gesetzliches Zahlungsmittel (FrontPage Africa 2017); aktueller Rechtsstand nicht bestätigt, daher wie CLDR nur LRD.

## 7. Kraftwerke (`kraftwerke.json`) – 197 Kernkraftwerks-Standorte

IAEA PRIS war nicht abrufbar (pris.iaea.org leitet auf eine Skript-Anwendung pris-stats.iaea.org um, die das Abrufwerkzeug nicht laden darf). Ersatzweise: IAEA Country Nuclear Power Profiles, World Nuclear Association (Länderprofile nach PRIS/Betreibern), World Nuclear News, American Nuclear Society.

| Standort(e) | Ergebnis | Quelle |
|---|---|---|
| **Japan (16 Standorte)** | **neu gepflegt:** Status je Standort (in Betrieb: Sendai 1–2, Genkai 3–4, Ikata 3, Takahama 1–4, Ohi 3–4, Mihama 3, Onagawa 2, Shimane 2, Kashiwazaki-Kariwa 6 seit 04/2026; nicht in Betrieb: Hamaoka, Higashi-Dori, Shika, Tokai Daini, Tomari, Tsuruga); Fukushima Daini als abgeschaltet markiert (`aus`) | WNA „Nuclear Power in Japan“ (22.09.2026) |
| **Pickering A (CAN)** | **korrigiert:** in Betrieb → abgeschaltet (Block 1 30.09.2024, Block 4 Ende 2024) | World Nuclear News 02.01.2025 |
| **Pickering B (CAN)** | **ergänzt:** Blöcke 5–8 laut Plan seit Ende 09/2026 zur Sanierung außer Betrieb | ANS 24.09.2026 |
| **Kanupp (PAK)** | **korrigiert:** in Betrieb → abgeschaltet 01.08.2021 | IAEA Country Nuclear Power Profiles 2022 |
| **Kori (KOR)** | **ergänzt:** Block 1 stillgelegt 2017, Block 2 seit 04/2026 wieder in Betrieb, Blöcke 3/4 Wiederanfahren 2027 | World Nuclear News 27.10.2026 |
| **Bushehr (IRN)** | **ergänzt:** laut Rosatom in Betrieb (03/2026), Einschläge in der Nähe März/April 2026 | ANS 06.04.2026 (nach IAEA); Shafaq 19.03.2026 |
| **Atucha I (ARG)** | **ergänzt:** seit 29.09.2024 für Laufzeitverlängerung außer Betrieb | World Nuclear News |
| **Olkiluoto (FIN)** | **ergänzt:** Block 3 seit 16.04.2023 in Betrieb (nicht in MW) | Pohjolan Voima/TVO |
| Palisades (USA) | bestätigt: Neustart ohne Termin (07/2026), bis 11/2026 keine Rückkehr gemeldet | ANS 08.07.2026 |
| Deutschland (7), Taiwan (3), Belgien (3), Saporischschja, Indian Point, Duane Arnold, Fessenheim, Mühleberg, Dungeness B, Hinkley Point B, Hunterston B, Vogtle, Flamanville, Ringhals | wie bisher (amtlich/Betreiber, bekannt); in dieser Prüfung nicht erneut abgerufen | BASE, Taipower, Engie, IAEA, NRC, EDF |

**Standhinweis** im Datensatz verdeutlicht („ACHTUNG Datenstand … 2019–2021 … viele neue Anlagen fehlen“, Liste der geprüften Länder).
Summe: 197 Standorte, davon 41 mit amtlichem/Fachquellen-Status (davon 23 in dieser Prüfung neu oder korrigiert: 16 Japan, 2 Pickering, Kanupp, Kori, Bushehr, Atucha I, Olkiluoto). Offen: Status der übrigen ~156 Standorte (v. a. USA 55, Frankreich 17, Russland 10, China 12, Indien 9) nicht einzeln gegen PRIS geprüft; Teil-Stilllegungen an weiterbetriebenen Standorten (z. B. Kursk 1–2, Leningrad 1–2, Novovoronezh, Kozloduy 1–4, Oskarshamn 1–2, Wolsong 1) sind in `mw` noch enthalten. Fehlende neue Standorte (z. B. Rooppur, Akkuyu, Kakrapar-Erweiterung, chinesische Neubauten) nicht ergänzt.

## 8. Sprachen, Religionen, Welterbe

**Sprachen (`sprachen.json`):** Stichprobe 34 Länder (DEU FRA CHE BEL LUX AUT ITA ESP POL CZE USA CAN MEX BRA IND CHN JPN RUS TUR IRN EGY NGA ZAF ETH KEN IDN PHL PAK BOL PRY IRL FIN SAU ISR) gegen das Feld „Languages“ des CIA World Factbook (lokales Archiv, letzte Ausgabe). **3 korrigiert** (Amtssprachen):
- Schweiz: „Deutsch, Schweizerdeutsch, Französisch, Italienisch“ → „Deutsch, Französisch, Italienisch, Rätoromanisch“ (Rätoromanisch fehlte, Schweizerdeutsch ist keine Amtssprache).
- Nigeria: „Englisch, Yoruba“ → „Englisch“ (Yoruba ist eine verbreitete, aber keine Amtssprache).
- Israel: „Hebräisch, Arabisch“ → „Hebräisch, Arabisch (Sonderstatus)“ (Factbook: „Arabic (special status under Israeli law)“).
Übrige 31 bestätigt (Hinweis: „verbreitetste Sprache“ folgt der CLDR-Zählweise mit Zweitsprachlern, wie in OFFEN.md beschrieben).

**Religionen (`religionen.json`):** Stichprobe 20 Länder (DEU CHE NGA ISR CHN TUR EGY RUS JPN USA IND IDN BRA MEX FRA POL CZE LBN NLD KOR): Zuordnung der Factbook-Freitexte zu den Hauptgruppen nachgerechnet – **alle 20 richtig** (z. B. USA Christentum 46,5+20,8+1,6+0,9+0,8 = 70,6 %). Anmerkung: Brasilien – Spiritismus (Kardecismus) ist mit Umbanda/Candomblé unter „Volks- und traditionelle Religionen“ gezählt (Abgrenzungsfrage, 1,8 %). Offen bleibt das Alter der Factbook-Schätzungen (z. B. USA 2014, Russland 2006).

**Welterbe (`welterbe.json`):**
- **Deutschland: 55** (nicht 56). Belege: KMK „Welterbe“ (55 Stätten, davon 10 grenzüberschreitend; 2026 keine Neueintragung, nur Erweiterung „Siedlungen der Berliner Moderne“ um die Waldsiedlung Zehlendorf), Auswärtiges Amt/Ständige Vertretung bei der UNESCO („Germany's 55th World Heritage Site“, Schlösser Ludwigs II., 12.07.2025), UNESCO-Statistik (Germany: 55).
- **48. Sitzung fand statt** (Busan, 19.–29.07.2026): 25 Neueintragungen, Liste jetzt 1.273 Stätten in 173 Staaten (The Peninsula 30.07.2026, UN News). Alle 25 (Time Out 27.07.2026) eingearbeitet: FIN, IRN, BRA, IND, JPN, FRA (2), POL, CHN, LBN, KAZ, PSE, UZB, MNG, COM, STP, ITA, TUN, THA (Kultur); JOR, SSD, USA, DNK, ARE (Natur); GRC (gemischt). Erstmals mit Welterbe: Komoren, São Tomé und Príncipe, Südsudan.
- **Alle 196 Vertragsstaaten** gegen UNESCO „States Parties – statistics“ (<https://whc.unesco.org/en/statesparties/stat>, Stand nach der 47. Sitzung) abgeglichen: 185 stimmten, **11 korrigiert** (alt → neu): BRA 24→25, PRK 2→3, DMA –→1, DEU 56→55, LAO 3→4, MOZ 1→2, PAN 6→5, SAU 7→8, SRB 4→5, PSE 4→5, GBR 33→35. Bei diesen ist die Aufteilung Kultur/Natur entfernt (nicht belegt). Gebiete mit eigener Fläche (GRL, PYF, NCL, PRI, CUW, BMU, HMD, XKX) behalten zusätzlich ihre Lage-Zahl; Hinweis zur Zählweise und zu „Mittelalterliche Denkmäler im Kosovo“ (UNESCO: unter Serbien) im Datensatz.
- Neue Höchstzahl: Italien 62 (Legende `max` jetzt automatisch).

## 9. Paket a (`/home/claude/scratch/themen/a/`)

**Heilbäder (`heilbaeder.json`): 39 → 57 Orte.** `a/prep/heilbaeder.py` ergänzt, Datei neu erzeugt, `a/prep/pruefen.py`: keine Fehler.
- **Nordrhein-Westfalen (8):** amtliches „Verzeichnis der staatlichen Anerkennungen von Kurorten, Erholungsorten und Heilbrunnen“ (recht.nrw.de, fortgeschrieben bis 22.07.2026): Heilbad – Bad Waldliesborn, Bad Sassendorf, Bad Westernkotten, Bad Driburg, Bad Lippspringe, Bad Holzhausen (Preußisch Oldendorf), Aachen (Monheimsallee/Burtscheid); Ort mit Heilquellenkurbetrieb – Kevelaer. Die 8 Kneipp-Heilbäder wie in NI/BY nicht aufgenommen. Bad Oeynhausen steht im Verzeichnis nur mit Kurgebietsgrenzen, nicht als Heilbad – daher nicht aufgenommen.
- **Sachsen (9 mit Lage):** „Staatlich anerkannte Kurorte im Freistaat Sachsen“ (REVOSax, Stand 11.09.2019): Bad Brambach (Mineralheilbad), Bad Elster (Mineral- und Moorheilbad), Bad Düben (Moorheilbad), Bad Lausick, Bad Schlema, Wildbach, Warmbad (Heilbad), Thermalbad Wiesenbad (Heilquellenkurbetrieb), Bad Muskau (Moorkurbetrieb). Bad Gottleuba (Moorheilbad) ohne GeoNames-Eintrag → ohne Lage.
- Art der Quelle nur, wenn das Prädikat sie nennt; sonst „Heilbad (Art im Verzeichnis nicht genannt)“. Lage aus GeoNames cities1000; Ortsteile ohne Eintrag mit der Lage der Gemeinde. Salzgitter(-Bad) jetzt über GeoNames (geonamescache) verortet.
- **Offen:** Baden-Württemberg (Landtag Drs. 17/8623: 54 höherprädikatisierte Heilbäder/Kurorte, aber keine Liste), Hessen (Anerkennungen nur im Staatsanzeiger), Rheinland-Pfalz, Thüringen, Schleswig-Holstein, Saarland, Brandenburg, Mecklenburg-Vorpommern, Sachsen-Anhalt; ein Gesamtverzeichnis des Deutschen Heilbäderverbands war nicht abrufbar.

**Naturparks:** nicht ergänzt. Eine Liste mit Name/Fläche/Jahr existiert (BfN, VDN), aber eine belegbare Lage je Park fehlt (GeoNames-Parkpunkte nicht im verfügbaren Paket, Wikidata nicht erreichbar). `a/fertig/OFFEN.md`, `QUELLEN.md`, `EINBAU.md` entsprechend aktualisiert.

## Gesamtübersicht

| Ebene | geprüft | korrigiert/ergänzt | entfernt | offen |
|---|---|---|---|---|
| Bündnisse | 18 Listen | 3 (Five Eyes, EAWU-Beobachter, OPEC+-Partner) + Präzisierungen | 0 | Georgien/OVKS-Jahr |
| Stützpunkte | 92 Lagen, 26 Status | 5 (+3 präzisiert) | 0 | Status von ~66 |
| Frühe Stätten | 78 Lagen, 15 Datierungen | 5 | 0 | 63 Datierungen ohne Einzelbeleg |
| Engstellen | 10 | 0 | 0 | – |
| Leitungen | 34 Verläufe, 7 Status | 13 Verläufe, 3 Status/Kapazität | 0 | Kapazitäten von 29 |
| Reiche/Handel/Fahrten | 36 | 7 | 0 | Grenzfälle der Länderlisten |
| Staatsschulden | 44 Werte + Lizenz | 0 Werte, Lizenztext | 0 | 70 Werte nicht einzeln |
| Goldreserven | 22 | 0 | 0 | Vervollständigung (Rechte/Zugang) |
| Währungen | Unionen + Dollar-Länder | 3 (Karib. Gulden, Nordzypern, Somaliland) | 0 | Liberia |
| Kraftwerke (Kern) | 41 Standorte | 23 | 0 | ~156 Standorte ohne PRIS-Abgleich |
| Sprachen | 34 Länder | 3 | 0 | übrige Länder |
| Religionen | 20 Länder | 0 | 0 | Alter der Schätzungen |
| Welterbe | 196 Staaten + 25 Neueintragungen 2026 | 11 Staaten + 24 Staaten um Neueintragungen | 0 | – |
| Paket a Heilbäder | 2 Länder neu | +18 Orte | 0 | 9 Länder |

Build: `bash prep/alle.sh` (b) und `python3 -I prep/pruefen.py` (a) – jeweils **0 Fehler** (b: 10 bekannte, erklärbare Warnungen).
