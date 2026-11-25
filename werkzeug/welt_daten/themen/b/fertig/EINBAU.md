# Einbau der Themen-Ebenen in die Weltkarte (`werkzeug/welt.js`)

Stand 25.11.2026 (nach Gegenprüfung, siehe `PRUEFBERICHT.md`) · 16 Dateien in `fertig/`, zusammen ca. 298 KB kompaktes JSON · Prüfung: `python3 prep/pruefen.py` (0 Fehler, 10 erklärbare Warnungen) · neu bauen: `prep/alle.sh`.

## Gemeinsames Format

Jede Datei: `{id, name, gruppe, typ, einheit, legende, quellen:[{t,u,stand,lizenz}], hinweis, felder, daten}`.
- `typ:'land-kat'` → `daten = {ISO3: {…, Kategorie-Feld}}`, passt als Kategorie-Ebene wie `GRUND.staat` (Farbe je Kategorie aus `legende[].c`). In `farbe(i)` statt `STAAT[staatVon(i)][1]` die Farbe der Kategorie des Landes nehmen.
- `typ:'land-wert'` → `daten = {ISO3: Zahl}` oder `{ISO3: {…}}`, passt als Werte-Ebene wie `GRUND.le` (`p` Palette, `s` Skala, `lg` Legende).
- `typ:'land-liste'` → Liste von Gruppen mit ISO3-Listen (Mitglieder/Staaten); Auswahl einer Gruppe färbt deren Länder (wie eine Kategorie-Ebene mit Auswahlknöpfen).
- `typ:'punkte'` → Liste mit `n, lon, lat, rang (1–3), t`; zeichnen wie `ERF`/`GELD` (Overlay in `S.ov`).
- `typ:'linien'` → Liste mit `linien:[[[lon,lat],…],…]` (Teilstrecken) und `orte:[[Name,lon,lat],…]`; zeichnen wie `WANDER` (`w[6].forEach(p=>…)`), aber als Linie statt Pfeil. Alle selbst gezeichneten Linien tragen `schema:true` → in der Info-Karte „schematisch“ anzeigen, gestrichelt zeichnen.
- Koordinaten auf 1/100 Grad. Jahre negativ = v. Chr. (wie `ERF`). `rang`: 1 ab Zoom 1, 2 ab Zoom ~2, 3 ab Zoom ~3,5 (wie `MEERE`-Staffelung).
- Info-Karte: Titel `n`, Text `t`, darunter Detailfelder und als letzte Zeile die Quellenzeile `quellen[0].t + ' · Stand ' + quellen[0].stand`. Bei `schema:true` den Zusatz „schematisch“.
- ISO3 sind die Codes der App (`welt_basis.json`: z. B. `XKX` Kosovo, `CYN` Nordzypern, `SOL` Somaliland). Gebiete ohne eigenes Polygon (Gibraltar) haben `gast:null` + `gebiet`.

## Ebenen

**Sprachen (`sprachen.json`, Menschen, land-kat).** Färbung nach `fam` (Sprachfamilie der verbreitetsten Sprache mit Amtsstatus; Indogermanisch zusätzlich Zweig `zw` – Vorschlag: Zweige als Abstufungen eines Blaus: germanisch #6aa8e8, romanisch #8ac0ff, slawisch #4a7ac8, indoiranisch #a0b8ff, sonst #6aa8e8). Ab Zoom 1. Info: „Amtssprachen: Deutsch · Verbreitetste Sprache: Deutsch (91 % sprechen sie) · Sprachfamilie: Indogermanisch (germanisch)“, bei `allg` zusätzlich „insgesamt am verbreitetsten: Englisch (59 %)“. Legende: Familien mit Farbe (aus `legende`). Quellenzeile: „Unicode CLDR 47; Glottolog 5.4 (CC BY 4.0)“.

**Religionen (`religionen.json`, Menschen, land-kat).** Färbung nach `g` (größte Gruppe), Farben in `legende`; Deckkraft optional nach Anteil `a[g]` (z. B. 0,45 + 0,55·Anteil/100). Info: Balken je Gruppe aus `a` (Namen aus `gruppen`), dazu „Stand: j“; bei `sp` „laut Quelle 81–90 %“; bei `ohne_zahl` „Quelle nennt keine Prozentzahlen“. Quellenzeile: „CIA World Factbook (letzte Ausgabe 2026), Jahr je Land“.

**Alte Reiche (`reiche.json`, Geschichte, land-liste).** Auswahlliste der 17 Reiche (Jahr aufsteigend), gewähltes Reich färbt die Länder in `l` mit `c` (halbtransparent, schraffiert = schematisch), Hauptstadt als Kronen-/Punktsymbol bei `lon/lat` mit Name `hs`. Passt zum Epochen-Filter (`S.epoche`) über `j`. Info: „Römisches Reich · größte Ausdehnung 117 n. Chr. · ca. 5,0 Mio. km² · Hauptstadt Rom“ + `t` + „schematisch nach heutigen Grenzen“. Quellenzeile: „Flächen nach Taagepera u. a. (Zusammenstellung Wikipedia)“.

**Handelswege (`handelswege.json`, Geschichte, linien).** Gestrichelte Linien in `c`, Breite 2 px; Orte als kleine Punkte ab Zoom 2,5, Hanse-Orte mit eigenem `rang` und Rolle (Kontor hervorheben). `teilnamen` als Beschriftung der Teilstrecken (Römerstraßen, Transsahara, Salzstraßen). Info: Name, Zeitraum, „Waren: …“, Text. Epoche über `von`. Legende: Name + Farbe.

**UNESCO-Welterbe je Land (`welterbe.json`, Geschichte, land-wert).** Werte-Ebene `n` (Anzahl), Palette z. B. `GRN`/`TEAL`, Skala `s:v=>Math.sqrt(v/62)` (bzw. `legende.max`), `lg:['0','15','60']`. Info: „55 Welterbestätten“ (Aufteilung Kultur/Natur nur, wenn `k`/`nat`/`gem` vorhanden). Hinweis in der Legende: „Stand Juli 2026 (48. Sitzung), ohne Einzelstätten“.

**Megalithen, Pyramiden & frühe Kultstätten (`fruehe_staetten.json`, Geschichte, punkte).** Symbol je `art` (Pyramide = Dreieck, Steinkreis = Ring, Grab = Halbkreis, Höhle = Bogen, Siedlung = Quadrat), Farbe aus `legende`. Beschriftung ab Zoom 2,2 bzw. nach `rang`. Info: Name, Land, `dat` (Datierungstext, bei strittigen Fällen steht das dort), Text. Epochenfilter über `von`.

**Entdeckungsfahrten (`entdeckungsfahrten.json`, Geschichte, linien).** Linien mit Pfeilspitze am Ende jeder Teilstrecke (wie `pfeil()` in WANDER), Farbe `c`; Stationen (`orte`) als Punkte. Linien am 180. Längengrad sind bereits geteilt. Info: Name, „wer“, Jahre, Text.

**Bündnisse (`buendnisse.json`, Politik, land-liste).** Knopfleiste mit den 18 Bündnissen; Mitglieder in `c` füllen, Partner/Beobachter/Kandidaten heller bzw. schraffiert, `ausgesetzt` mit gestricheltem Rand, `ehemalig` nur in der Info. Info je Land: „Mitglied seit 1955“ bzw. „Partnerland“, dazu `hinweis_mitglieder`. Länderinfo (Klick auf Land) optional: Liste aller Bündnisse des Landes. Quellenzeile: Feld `q` des Bündnisses (Stand 11/2026).

**Militärstützpunkte (`stuetzpunkte.json`, Politik, punkte).** Kleines Rautensymbol in Farbe des Betreibers (`legende`), geräumte Standorte (`status` beginnt mit „geräumt“) hohl/grau, „umstritten“ und „nicht bestätigt“ mit Fragezeichen-Rand. Ab Zoom 1 nur `rang` 1. Filter nach Betreiber möglich. Info: „Betreiber: USA · Gastland: Deutschland · Luftwaffe · Status“ + Text + Beleg `q`. Neutral: gleicher Stil für alle Betreiber.

**Öl- und Gasleitungen (`energie_leitungen.json`, Wirtschaft, linien).** Gas blau `#5fb8ff`, Öl orange `#ff8a3d`, beides violett; `st` „zerstört“/„außer Betrieb“ grau gestrichelt, „eingeschränkt“ halbtransparent. Info: Name, Inbetriebnahme, Kapazität, Status (mit Datum), durchquerte Länder, „schematischer Verlauf“.

**Seewege & Engstellen (`energie_engstellen.json`, Wirtschaft, punkte).** Kreis mit Fläche nach `oel` (Mio. Barrel/Tag), Farbe `#ffcf5a`, Gibraltar ohne Wert als kleiner Ring. Info: „20,9 Mio. Barrel Öl/Tag · 11,4 Mrd. Kubikfuß LNG/Tag (1. Hj. 2025)“ + Text. Quellenzeile: „US EIA (gemeinfrei)“.

**Kraftwerke (`kraftwerke.json`, Wirtschaft, punkte).** Kreisfläche nach `mw` (Wurzel), Farbe nach `art`; `aus:1` als hohler Kreis mit Strich. Kernkraftwerke ab Zoom 1 sichtbar, übrige nach `rang`. Info: Name, Land, Art, „5.200 MW“, Inbetriebnahme `j`, Status `st` mit Beleg `stq`. Pflicht-Namensnennung in der Quellenzeile: „Global Power Plant Database, WRI (CC BY 4.0)“.

**Staatsschulden (`staatsschulden.json`, Wirtschaft, land-wert).** Palette `ROT`, `s:v=>Math.min(v,200)/200`, `lg:['0 %','100 %','200 %+']`. Info: „62,9 % des BIP (2025, IWF)“. Länder ohne Wert grau.

**Goldreserven (`goldreserven.json`, Wirtschaft, land-wert).** Wie die Rohstoff-Blasen (`blase()` am Landesmittelpunkt), Goldverlauf wie GELD-Münzen, Radius ~ √Tonnen. Info: „3.350 t (Anfang 2026)“.

**Währungen (`waehrungen.json`, Wirtschaft, land-kat).** Färbung nach `kat` (Euro, CFA-Franc West/Zentral, Ostkaribischer Dollar, US-Dollar, andere gemeinsame, eigene), Farben in `legende`. Info: „Währung: Euro (EUR)“; bei mehreren Währungen alle. Ergänzt GELD (Geldgeschichte).

## Neutralität (bitte im Einbau beibehalten)
- Texte enthalten keine Wertungen; umstrittene Gebiete heißen „beansprucht von …“, „verwaltet von …“ (Westsahara, Krim, Abchasien/Südossetien, Transnistrien, Nordzypern, Chagos, Falklandinseln, Gibraltar, Golan).
- Hinweis für den Einbau: In der App-Grundkarte liegt die Krim im Polygon `RUS` (Punkt Sewastopol). Die Stützpunkt-Ebene führt Sewastopol mit `gast:'UKR'` und dem Text „2014 von Russland annektiert, international überwiegend als Teil der Ukraine anerkannt“. Die Darstellung der Krim in der Grundkarte sollte unabhängig davon geprüft werden.
