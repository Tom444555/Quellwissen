# Bericht: Heilbäder (BW, RP, SL, SH, MV) und Fläche Naturpark Harz

Stand der Recherche: 26.11.2026. Daten: `daten.py` (gleicher Ordner).

## Ergebnis vorab
Für keines der fünf Länder habe ich online eine **landeseigene, aktuelle Namensliste** gefunden, die ich abrufen konnte.
Darum ist die Hauptquelle ein **amtliches, länderübergreifendes Verzeichnis**:
das Beihilfe-Verzeichnis der Senatsverwaltung für Finanzen Berlin,
„Übersicht der anerkannten Heilbäder- und Kurorte (zu § 35 Abs. 1 Satz 2 LBhVO)“,
Anlage zum Rundschreiben IV Nr. 42/2026, **Stand 10/2026**:
- Anlage: https://www.berlin.de/politik-und-verwaltung/rundschreiben/download.php/4330565
- Rundschreiben (Änderungen, 09.10.2026): https://www.berlin.de/politik-und-verwaltung/rundschreiben/download.php/4330562

Gegenprobe zur Vollständigkeit: Jede Postleitzahl im Abschnitt 1 der Anlage ist in den ausgelesenen Datensätzen enthalten.
Zum Abgleich habe ich auch das ältere bayerische Heilkurorteverzeichnis (BayMBl. 2022 Nr. 126) geprüft; es hat denselben Aufbau.

**Aufgenommen:** Heilbäder mit Heilmittel, Orte mit Heilquellen-, Heilstollen- oder Peloidkurbetrieb und See- bzw. Ostsee-/Nordseeheilbäder.
**Nicht aufgenommen:** reine Seebäder, Luftkurorte, Erholungsorte, Kneippkurorte und heilklimatische Kurorte.
Kneipp- und Felke-Heilbäder sowie Zweifelsfälle stehen getrennt in `GRENZFAELLE`.

**Spalte „Art“:** Nennt das Prädikat das Heilmittel (z. B. „(Sole-)Heilbad“), ist die Art daraus übernommen.
Bei einem bloßen „Heilbad“ habe ich die Art aus allgemeiner Kenntnis ergänzt. Diese Orte stehen in `ART_ERGAENZT`; die Angabe ist nicht amtlich belegt.

## Baden-Württemberg: 34 Einträge (+1 Grenzfall)
- Quelle: Berliner Verzeichnis, Stand 10/2026. Bad Rippoldsau-Schapbach ist im Oktober 2026 gestrichen worden.
- Gesucht, aber ohne Namensliste:
  - Landtag BW, Drs. 16/6450 (Kurortegesetz 2019, nur Gesamtzahl 298 Gemeinden)
  - Drs. 17/3023 (2022, „55 höherprädikatisierte Orte“, keine Namen)
  - Drs. 17/8623 (54 Orte, keine Namen)
  - Pressemitteilung des Innenministeriums vom 13.01.2020 (38 Kurorte mit Zusatzbezeichnung, keine Namen)
- Statistisches Landesamt, LIS „Gemeindegruppen FV504–510“ (ohne Datum): **nicht brauchbar**, weil widersprüchlich. Bad Wildbad, Badenweiler und Bad Krozingen stehen dort als „Sonstige Gemeinden“.
- Auffällig:
  - Mehrere Orte sind Ortsteile: Bad Rotenfels (Gaggenau), Bad Imnau (Haigerloch), Hoheneck (Ludwigsburg), Bad Sebastiansweiler (Mössingen), Stuttgart (Berg, Bad Cannstatt).
  - Bad Schönborn ist doppelt eingetragen: Bad Mingolsheim als Heilbad, Langenbrücken mit Heilquellenkurbetrieb.
  - Grenzfall: Überlingen (Kneippheilbad).

## Rheinland-Pfalz: 10 Einträge (+4 Grenzfälle)
- Landesquelle: Stellungnahme der Landesregierung zur Enquete-Kommission Tourismus, Stand 10.07.2018, Tabelle 3.2. Sie nennt 10 Heilbäder, 2 Kneipp-Heilbäder und 1 Felke-Heilbad.
  - Link (Web-Archiv edoweb-rlp): https://wayback.edoweb-rlp.de/weltweit/20241029mp_/https:/mwvlw.rlp.de/fileadmin/mwkel/Abteilung_3/Tourismus/Gesundheitstourismus.pdf
- Mit dem Berliner Verzeichnis (10/2026) stimmen die 10 Heilbäder überein.
- Abweichungen:
  - Bad Tönisstein (Andernach/Burgbrohl) steht nur im Berliner Verzeichnis als Heilbad, nicht in der RP-Liste 2018. Deshalb Grenzfall.
  - Bad Sobernheim heißt in RP „Felke-Heilbad“, in Berlin „Heilbad“.
  - Im Berliner Verzeichnis steht bei Bad Dürkheim die PLZ 65098; richtig ist 67098.
- Bad Münster am Stein gehört seit 2014 zu Bad Kreuznach. Deshalb ist als GeoNames-Name „Bad Kreuznach“ eingetragen.

## Saarland: 0 Einträge
- Im Verzeichnis stehen nur:
  - Blieskastel-Mitte (Kneippkurort)
  - Nonnweiler (heilklimatischer Kurort)
  - Weiskirchen (heilklimatischer Kurort und Kneippkurort)
- Eine saarländische Landesliste habe ich nicht gefunden (gesucht nach Kurortegesetz, Landtag und Ministerium).

## Schleswig-Holstein: 28 Einträge
- Quelle: Berliner Verzeichnis 10/2026.
- Wichtig: Bei 12 der 13 im Rundschreiben geänderten SH-Orte zeigt die Tabellen-Anlage nur das erste Prädikat (z. B. Dahme nur „Seebad“). Die vollständigen Doppelprädikate (z. B. „Seebad, Ostseeheilbad“) stehen im Änderungsteil des Rundschreibens vom 09.10.2026. Ich habe sie von dort übernommen.
  - Betroffen: Bad Bramstedt (Moor-Heilbad), Bad Segeberg (Heilbad) und Holm/Schönberg („Seebad, Heilbad“).
  - Ohne diesen Änderungsteil würden 11 Orte fehlen.
- Nicht aufgenommen: Eutin (Luftkurort, heilklimatischer Kurort), Malente (heilklimatisch), Mölln und Gelting (Kneippkurort).
- Die SH-Landesverordnung (KurortVO vom 28.11.2019) enthält keine Ortsliste.
- Landtags-Drucksachen von landtag.ltsh.de konnte ich nicht herunterladen (Verbindung jeweils abgebrochen).
- GeoNames bei Ortsteilen:
  - Travemünde → Lubeck
  - Westerland → Sylt (bei der Verortung kann auch die Insel getroffen werden)
  - Burg → Fehmarn
  - Haffkrug → Scharbeutz

## Mecklenburg-Vorpommern: 10 Einträge
- Quelle: Berliner Verzeichnis 10/2026.
- Die Landesseite „Kur- und Erholungsorte in MV“ (regierung-mv.de) und ihre Downloads leiten derzeit auf die Startseite des Portals um (Umbau zur neuen Wahlperiode). Die Liste war deshalb nicht abrufbar.
- Landtag MV, ohne Namensliste:
  - Drs. 7/1961 (2018: 65 Kur- und Erholungsorte)
  - Drs. 8/772
  - Drs. 8/3759
  - Drs. 8/6164 (13.01.2026)
- Auffällig:
  - Das Verzeichnis führt Ahlbeck und Bansin noch als eigene Gemeinden; sie sind Ortsteile von Heringsdorf (GeoNames: Heringsdorf).
  - Bad Doberan steht zweimal: als Moorheilbad und mit Heiligendamm als Seeheilbad.
  - Bad Sülze hat das Prädikat „Peloidkurbetrieb“; als Art ist „Moor“ ergänzt.
- Nicht aufgenommen: die Seebäder (Ahrenshoop, Binz, Kühlungsborn, Prerow, Sellin, Thiessow, Warnemünde, Wustrow) sowie Feldberg und Göhren (Kneippkurort).
- Templin und Bad Wilsnack haben PLZ 17/19, liegen aber in Brandenburg und sind nicht aufgenommen.

## Naturpark Harz (Niedersachsen)
- **909 km² ist richtig.**
  - NLWKN, Tabelle „Naturparke in Niedersachsen“, Stand 31.12.2025: Harz, gegründet 1960, **90.856 ha** (Spalte „Anteil in Niedersachsen“), Träger Regionalverband Harz e. V.
    https://www.nlwkn.niedersachsen.de/naturschutz/schutzgebiete/statistischer_uberblick/naturparke/naturparke-in-niedersachsen-122305.html
  - Regionalverband Harz (Träger), Faltblatt „Drei Länder, vier Naturparke: EIN HARZ“ (2020): „Der inzwischen 909 km² große Naturpark Harz in Niedersachsen“.
    https://harzregion.de/files/rvh/content/download/sonstiges/faltblatt/Faltblatt_60_Jahre_Naturpark_Harz.pdf
- **Woher die 2.825 km² kommen:** Laut demselben Faltblatt sind es 909 km² (Niedersachsen) + 1.660 km² (Harz/Sachsen-Anhalt) + 256 km² (Mansfelder Land, seit 2012) = **genau 2.825 km²**.
  - Das ist die Summe der drei Naturparke, die der Regionalverband Harz trägt.
  - Der Naturpark Südharz in Thüringen (267 km²) ist darin nicht enthalten.
  - Der Geopark ist es ebenfalls nicht; das Faltblatt nennt für ihn keine Fläche.
- Einschränkung: Die VDN-Seite selbst konnte ich nicht abrufen (Zugriff nicht freigegeben). Die Zuordnung beruht auf der exakt passenden Summe, nicht auf einem Zitat von der VDN-Seite.
