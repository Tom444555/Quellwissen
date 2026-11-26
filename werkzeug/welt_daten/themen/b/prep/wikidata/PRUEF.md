# Prüfbericht Wikidata-Ebenen (Stand 26.11.2026)

Dateien: `welterbe_staetten.json`, `naturparks.json`, `heilbaeder.json`. Skripte: `sparql.sh` (Abruf), `welterbe_staetten.py`, `abgleich_welterbe.py`, `naturparks.py`, `heilbaeder_neu.py`, `geo.py` (Punkt-in-Fläche über `welt_basis.json`), `pruef_alle.py`. Abfragen: `q_*.rq`, Rohantworten in `roh/`.
Aufruf jeweils `cd /home/claude/scratch/wikidata && python3 -I <skript>.py`. Gesamtprüfung `python3 -I pruef_alle.py`: Kopf vollständig, alle Quellen mit t/u/stand/lizenz, alle Koordinaten im Bereich. Einzige Bundesland-Abweichung ist Bad Muskau (alte Datei, GeoNames; der Ort liegt an der Grenze SN/BB, die App-Umrisse sind grob).

## 1. Welterbestätten (`welterbe_staetten`, 1.273 Punkte)

**Abfragen:** `q_welterbe.rq` (alle Objekte mit P757: Bezeichnung de/en, P625, P2614, P31, P1435 = Q9259 mit P580), `q_welterbe_land.rq` (P17 → P298), `q_welterbe_name.rq` (Bezeichnung in anderer Sprache, wenn de/en fehlt), `q_ende.rq` (Welterbe-Aussage mit Endedatum oder als veraltet markiert), `q_lage_nach.rq` (Bestandteile P527 mit Koordinate), `q_krit.rq` (Kriterien-Objekte i–x).
Roh: 6.237 Kennungen an 6.414 Objekten. Zusammengefasst nach der Nummer ohne Zusätze (bis/ter/quater/rev, Teil `-001` bzw. `.594`, führende Null: 091 → 91): 1.280 Nummern.

**Ergebnis:** 1.280 − 7 = **1.273**, das entspricht der bekannten Gesamtzahl nach der 48. Sitzung. Kultur 988, Natur 240, gemischt 42, Art offen 3. Alle 1.273 Stätten haben eine Lage, 27 haben kein Jahr. 2026 sind in Wikidata alle **25 Neueintragungen** mit Jahr 2026 enthalten. Sie stimmen mit den Ländern der 48. Sitzung in `b/prep/welterbe.py` (NEU26) überein.

Herausgenommen (7 Nummern):
- gestrichen: 654 (Oman, Oryx-Schutzgebiet, 2007), 1156 (Dresdner Elbtal, 2009), 1150 (Liverpool, 2021);
- in einer anderen Nummer aufgegangen: 161 (Chambord → 933 Loiretal), 133 (Burgess Shale → 304), 291 (São Miguel das Missões → 275), **790** (Panamá Viejo → 1582 Koloniale Transisthmus-Route, 2025). Für 790 steht in Wikidata kein Endedatum. Beleg: worldheritagesite.org/list/id/1582 („is now part of“). Erst damit ergeben sich 1.273 Stätten, und Panama kommt auf 5.

Hauptobjekt je Nummer: das Objekt mit Kriterien, P31 = Welterbestätte, den meisten Kennungen und dem Startdatum. 108 Nummern haben mehrere Objekte ohne Teil-Suffix. In 5 Fällen ist das Hauptobjekt von Hand gesetzt (933 Loiretal, 1468 Herrnhuter Siedlungen, 797 Altstadt Verona, 1401 Rabat, 1087 Bremer Rathaus und Roland). `teile` gibt die Zahl der Teilobjekte in Wikidata an, nicht die amtliche Zahl. 401 Stätten haben Teile, am meisten die Felsmalereien der Levante (756).

Korrekturen:
- **Lage nachgetragen** über einen Bestandteil (P527), weil das Hauptobjekt keine Koordinate hat, Feld `lage:'Bestandteil'`: 509 Victoriafälle, 946 Mostar (Stari Most), 1567 Gedenkstätten Westfront (Douaumont), 1752 Aalto (Paimio), 1755 Katharerburgen (Carcassonne), 1759 Xiongnu (Noin-Ula), 1760 Mangghystau (Beket-Ata), 1762 Condominio-Theater (Jesi).
- **Staaten:** In der Regel gilt P17 des Hauptobjekts. Historische Staaten (DDR, SUN, Römisches Reich …) sind weggelassen. Für die Niederlande (Q55, ohne P298) ist NLD gesetzt, Kosovo XKS ist auf XKX umgesetzt. Einen weiteren Staat übernimmt das Skript nur, wenn ein Teilobjekt mit diesem P17 auch dort liegt (MOZ 914, LAO 951, XKX 724, SWE 1660). Von Hand gesetzt:
  - 1660 Ringburgen nur DNK (ein Objekt in Schweden trägt die Nummer fälschlich);
  - 588 Donaudelta nur ROU;
  - 999 Pantanal nur BRA;
  - 1411 Chersones UKR (Vertragsstaat laut UNESCO; Wikidata nennt zusätzlich RUS);
  - 148 Jerusalem ohne Staat (UNESCO: Vorschlag Jordaniens, kein Vertragsstaat).
  - Nachgetragen aus der Lage: 1393 Nachal Me'arot (ISR).
- **Namen:** 231 und 251 heißen „Rotes Fort (Delhi)“ und „Rotes Fort (Agra)“. Ersetzt wurden die fremdsprachigen oder unsinnigen Bezeichnungen von 322 Paharpur, 502 Vigan, 739 Schokland und 1269 Caral-Supe (Wikidata-Bezeichnung „שלום“). 89 Hauptobjekte haben keine deutsche Bezeichnung; dort steht der englische Name (oder ein Teilobjekt-Name).
- **Jahr:** Startdaten vor 1978 sind verworfen (Serengeti 1960 → ohne Jahr).

**Abgleich mit `b/fertig/welterbe.json`** (Zählung je ISO3, grenzüberschreitende Stätten bei jedem Staat, `abgleich_welterbe.py`): Nach den Korrekturen stimmen alle Staaten überein, bis auf die folgenden:
- Überseegebiete, die b zusätzlich zählt (BMU 1, HMD 1, NCL 1, PRI 1, PYF 2, XKX 1). Wikidata führt sie unter dem Mutterstaat.
- DNK 10 statt 13: die 3 Stätten in Grönland stehen unter GRL. NLD 12 statt 13: Willemstad steht unter CUW. Das ist die gleiche Zählweise wie bei den Überseegebieten.
- **USA 28 statt 27:** Wikidata führt bei 1468 (Herrnhuter Siedlungen, Erweiterung 2024) auch die USA (Bethlehem, Pennsylvania). b zählt die Erweiterung bei DEU und GBR mit, bei den USA aber offenbar nicht. Vermutlich ist b hier um 1 zu niedrig. **Zu prüfen.**
- Deutschland: Wikidata und b haben beide 55, darin enthalten ist 1468 wegen Herrnhut. Die KMK-Seite nennt ebenfalls 55 (abgerufen 26.11.2026).

Lage geprüft (Punkt im Staat laut App-Umrissen): 32 Punkte liegen außerhalb des eigenen Staats. Alle sind erklärbar: kleine Inseln, die im Umriss fehlen (z. B. Aldabra, Lord Howe, St Kilda, Rapa Nui, Bikini), Überseegebiete (PRI, BMU, NCL, PYF, ATF, HMD, PCN, MAC), Grenzlagen (Müstair, Saint-Louis, Al-Maghtas, Battir, Bahá'í-Zentrum Haifa, Gibraltar), Vatikan im ITA-Umriss, Jerusalem im PSE-Umriss sowie Chersones und Kosovo, deren Lage in der App so dargestellt ist.

**Offen bzw. unsicher:**
- 1743 Höhle von Kapowa (2025): In Wikidata ist die Welterbe-Aussage als veraltet markiert. Die Stätte ist trotzdem enthalten, weil b Russland mit 33 Stätten zählt und die Zahl dann aufgeht.
- 3 Stätten ohne Art (180 Haiti, 1121 Kaffeelandschaft Kolumbien, 1671 Yogyakarta): In Wikidata fehlen die Kriterien. Alle drei sind Kulturstätten, das wird aber nicht abgeleitet.
- 27 Stätten ohne Jahr (u. a. Taj Mahal, Große Mauer, Victoriafälle).
- 2023 hat 43 Einträge statt 42, 2024 hat 24 statt 26: Die Jahresangaben in Wikidata sind bei Erweiterungen teils verschoben. Das Jahr ist deshalb nur als Anhalt zu verstehen.
- Englische Namen könnten bei Bedarf übersetzt werden; das ist nicht gemacht.

## 2. Naturparks (`naturparks`, 105 Punkte)

**Klasse:** Q20354035 „Naturpark in Deutschland“ (110 Objekte). Zusätzlich wurden 8 Objekte der allgemeinen Klasse Q728904 mit Staat Deutschland geprüft (`q_np_klassen.rq`, `q_naturparks.rq`).
- Weggelassen: Dachobjekte grenzüberschreitender Parks (Deutsch-Luxemburgischer Naturpark, Maas-Schwalm-Nette, Hohes Venn-Eifel international); Doppel (Bourtanger Moor Q872763, Nagelfluhkette Q1260267); Sammelbegriff, DDR-Programm, Kressepark Erfurt.
- Weggelassen wurde auch Q123581313 „Hüttener Berge/Schlei“ (unklar; beide Parks gibt es einzeln).
- Aufgelöst seit 2015 (P576) und nicht enthalten: Ebbegebirge, Homert, Rothaargebirge (→ Sauerland-Rothaargebirge), Mecklenburgisches Elbetal.

**Abgleich VDN** (naturparke.de/naturparke/, abgerufen 26.11.2026: „104 Naturparke“, 104 Parkseiten): **Alle 104 VDN-Parks sind in Wikidata gefunden** (20 von Hand zugeordnet, weil die Namen abweichen, z. B. TERRA.vita = Nördlicher Teutoburger Wald-Wiehengebirge, Spessart = Bayerischer Spessart, Fränkische Schweiz-Frankenjura = Fränkische Schweiz-Veldensteiner Forst). Zusätzlich enthält Wikidata den **Naturpark Pfälzerwald** (RP, 1958, 1.798 km²), der in der VDN-Liste nicht steht (`vdn:false`). Daher 105 = 104 + 1.
- Ohne Lage: keiner. Ohne Fläche: 1 (Südharz). Ohne Gründungsjahr: keiner.
- **Flächen berichtigt** (Plausibilität 20–5.000 km²): Erzgebirge/Vogtland 1.495 km² und Westhavelland 1.315 km² (in Wikidata als 1,495 bzw. 1,315 eingetragen); Dahme-Heideseen 594 km² und Lahn-Dill-Bergland 874 km² (ha-Werte mit Einheit km²). Südharz: 114,86 m² ist nicht deutbar und deshalb weggelassen.
- Bundesland: `land` ist das Land des Lagepunkts, `laender` ergänzt die Länder aus der VDN-Länderliste (z. B. Harz, Diemelsee, Dübener Heide, TERRA.vita). Kein Lagepunkt widerspricht der VDN-Länderzuordnung. Usedom liegt knapp vor der App-Küstenlinie und wird MV zugeordnet.
- Grenzüberschreitende Parks (Nagelfluhkette, Bourtanger Moor, Hohes Venn-Eifel, Schwalm-Nette, Südeifel): Fläche und Lage sind die des deutschen Objekts in Wikidata.

## 3. Heilbäder (`heilbaeder`, 100 Orte: bisher 57 + 43 neu)

Die bisherigen 57 Orte (NI, BY, NW, SN) sind unverändert übernommen. Neu hinzugekommen sind 4 Länder, alle aus amtlichen Quellen und mit Lage aus Wikidata (Stadt-, Gemeinde- oder Ortsteil-Objekt im richtigen Bundesland, alle 43 gefunden):
- **Hessen (22):** Regierungspräsidium Kassel, Liste „prädikatisierte Orte und Ortsteile“, Stand 30.04.2026. Die Summenzeile („19 Heilbäder, 3 Orte mit Heilquellenkurbetrieb“) stimmt mit den Einträgen überein. Bad Wildungen und Reinhardshausen haben ein gemeinsames Prädikat und erscheinen als 1 Punkt. Sand liegt in Bad Emstal (Lage der Gemeinde). Die Art nennt die Liste nicht.
- **Thüringen (11):** Landtag Drs. 6/3368, Anlage 2, Kurorte zum 01.01.2017 (Antwort der Landesregierung; als Bild-PDF von Hand abgelesen). Weggelassen sind heilklimatische Kurorte, Luftkurorte und das Kneippheilbad Tabarz. **Der Stand ist alt.** Saalfeld (Feengrotten, Heilstollen) ist laut einer Pressemitteilung des Ministeriums neu anerkannt. Die Datei auf feengrotten.de war nicht abrufbar, deshalb fehlt Saalfeld.
- **Sachsen-Anhalt (3):** Landesverwaltungsamt, Pressemitteilung 22/2024 vom 04.03.2024: „3 Orte mit dem staatlichen Prädikat Heilbad“ (Bad Salzelmen, Bad Kösen, Bad Schmiedeberg).
- **Brandenburg (7):** MGS-Pressemitteilung 182/2025 vom 16.12.2025 mit der Liste der 8 Kurorte, ohne das Kneipp-Heilbad Buckow. Bestätigt durch die Pressemitteilungen zu Bad Saarow (12/2022), Bad Belzig (02/2023), Bad Liebenwerda (11/2024), Burg (05/2025) und Bad Wilsnack (07/2026).

**Weiter offen (keine amtliche Liste gefunden, nichts geraten):**
- **Baden-Württemberg:** Die Landtag-Drucksachen 17/8623 und 17/3023 nennen nur Zahlen (54 bzw. 55 höherprädikatisierte Orte) und die Mineral- und Thermalbäder laut Heilbäderverband, aber keine Prädikatsliste. Der Gesetzentwurf 16/6450 enthält keine Liste.
- **Rheinland-Pfalz:** Ministerium-Vorlage 18/1788 ohne Liste. Die Statistik nennt nur die Summe der Gemeindegruppe „Heilbäder“.
- **Saarland:** Gesetz ohne Ortsliste. Eine amtliche Liste wurde nicht gefunden.
- **Schleswig-Holstein:** Kurortverordnung ohne Liste. Die Landtag-PDFs waren aus der Arbeitsumgebung nicht abrufbar.
- **Mecklenburg-Vorpommern:** Die Liste der Landesregierung (regierung-mv.de, Download-IDs 1677587/1681556/1687945) leitet auf das neue Landesportal um und war nicht abrufbar. Der Gesetzentwurf Drs. 8/6164 (01/2026) hat keine Liste. Es gäbe nur die Liste des Bäderverbands (nicht amtlich).
- Seeheilbäder (SH, MV, NI) bleiben wie bisher bewusst weggelassen.
- Sachsen: Auf REVOSax gibt es nur die Liste von 2006 (älter als die bisher genutzte von 2019), deshalb bleibt die Fassung von 2019. Bayern hat weiter Stand 2020.

## Lizenzen
Wikidata CC0. Die amtlichen Verzeichnisse und Pressemitteilungen sind nur als Fakten genutzt (Ort, Prädikat). Vom VDN sind nur Zahl, Namen und Länder als Abgleich übernommen. UNESCO-Daten sind nicht übernommen, nur die Gesamtzahl als Prüfwert. worldheritagesite.org dient nur als Beleg für die Zusammenlegung 790 → 1582.
