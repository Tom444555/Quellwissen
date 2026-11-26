# OFFEN – nicht belegt, Widersprüche, jährlich prüfen

Stand: 26.11.2026

## 1. Nicht belegt (bewusst weggelassen)

### ablauf.json
- Feste Zeitabschnitte („Erste Stunde“, „Tag 2–3“ …) gibt keine Behörde vor. Die Zuordnung ist redaktionell, die Inhalte sind belegt.
- Es gibt keine amtliche Angabe, wie lange Kühlschrankware nach dem Ausfall noch sicher ist (außer: VZ Niedersachsen nennt 4–6 h Kühlung, Verbrauch solange unter 7 °C).

### wasser.json
- Lagerdauer von selbst abgefülltem Leitungswasser: Keine deutsche Behörde gefunden. Belegt ist nur CDC (USA): alle 6 Monate tauschen. Die Angabe „BBK empfiehlt 6 Monate“ stand nur auf einer Privatseite (notfallvorsorgeplan.de) und war nicht prüfbar.
- Wasserbedarf je WC-Spülung (Liter), Eignung von Regenwasser für die Toilettenspülung: keine amtliche Quelle geöffnet.
- Hersteller-unabhängige Angaben zu Silber-Konservierungsmitteln (nur haltbar machen, nicht entkeimen): nicht belegt.
- Deutsche Behördenaussagen zu Wasserfiltern: keine gefunden, es gibt nur CDC.

### strom.json
- **PVGIS-Monatswerte (Winter/Sommer) für Südwestdeutschland fehlen.** PVGIS war weder per WebFetch noch aus der Shell erreichbar. Vorschlag für die Nachrecherche im Browser: `https://re.jrc.ec.europa.eu/api/v5_3/PVcalc?lat=49.24&lon=6.99&peakpower=1&loss=14&angle=35&aspect=0&outputformat=json` (Saarbrücken, 1 kWp, Süd, 35°). Liefert E_m je Monat in kWh/kWp, für 100 Wp durch 10 teilen.
- Typische Leistungen von LED-Lampe (W), Batterieradio (W), Laptop (W) und Smartphone-Akku (Wh) gibt es nicht aus amtlicher Quelle. Smartphone ~15 Wh und Laptop ~50 Wh je Ladung sind aus dem Warentest-Beispiel abgeleitet (500 Wh ≙ 33 bzw. 10 Ladungen).
- Strombedarf einer Gastherme bzw. Steuerung (W): Es wurde keine Hersteller- oder Verbraucherzentralenquelle geöffnet. Belegt ist nur die Umwälzpumpe (15 W bzw. 60–100 W).
- Nutzbarer Anteil von Powerstations in % (Wechselrichterverlust): keine Prozentzahl aus Warentest oder Behörde, nur qualitativ („Stromwandlung frisst Energie“).
- Kühlgeräte nach neuen Energielabelklassen (A–G, seit 2021) in kWh je Tag: Es gibt nur Werte von 2012 nach alten Klassen.
- Kraftstoffverbrauch des Stromerzeugers (≈0,6 l/kWh) ist aus einem Datenblatt abgeleitet (Tank ÷ Laufzeit × Leistung), es gibt keine direkte Herstellerangabe in l/kWh.

### waerme_kochen.json
- Brenndauer von Gaskartuschen (190/230/450 g) hängt vom Brenner ab; es gibt keinen neutralen Wert. Angegeben ist nur der gerechnete Energieinhalt.
- Trockenbrennstoff (Esbit/Hexamin): Heizwert und Brenndauer nicht belegt.
- Holzkohle: Heizwert nicht in den geöffneten Tabellen.
- Garen in der Thermoskanne und Topf über Glut: keine seriöse Quelle (BZfE, VZ) gefunden.
- Kochkiste: Hygienegrenze (z. B. nicht unter 65 °C abkühlen lassen) steht nicht im BZfE-Text. Das sollte vor der Veröffentlichung beim BfR oder BZfE geklärt werden.
- Faustwerte „Gas je Mahlzeit“ wurden nicht belegt, deshalb gibt es nur den theoretischen Wert je Liter Wasser.

### naehrstoffe.json
- Eisen-Referenzwerte für Kinder und Jugendliche (DGE 2024): nicht gefunden. Calcium 7–<10 Jahre: fehlt.
- Vollständige DGE-Energietabelle (alle Altersgruppen, PAL 1,4/1,6/1,8): Es sind nur 4 Gruppen belegt.
- Vitamin-C-Gehalte von Sauerkraut, Trockenobst, Konserven und Säften (BLS/USDA): nicht geöffnet (USDA-Seiten nicht erreichbar).
- Wie viele Wochen ohne Vitamin C bis zum Skorbut vergehen: nicht belegt.

### ausruestung.json
- Der BBK-Ratgeber nennt keine Mengen für Hygieneartikel und keine Laufzeiten für Lampen oder Radios. Auch der BBK-Ratgeber 2013 nennt nur Einheiten (Rollen, Stück), keine Mengen.

### notfallplan.json
- Die DRK-Seite zum Familien-Notfallplan wurde nicht gefunden bzw. nicht geöffnet. Ersatzweise wurden Johanniter und ASB genutzt.
- „Kontaktperson außerhalb der Region“ wird in den gelesenen Quellen nicht empfohlen.
- Vollmacht zur Abholung von Kindern aus Kita oder Schule: nicht belegt.

### region_saarland.json
- **UKW-Frequenzen der SR-Programme: keine amtliche SR-Seite gefunden.** Kandidaten aus einer nicht amtlichen Liste (bandscan.de, ohne Datum) sind NICHT in die JSON übernommen und müssen vor der Nutzung mit sr.de abgeglichen werden:
  - SR 1: 88,0 (Göttelborner Höhe), 89,3 (Merzig), 91,9 (Moseltal), 92,3 (Bliestal), 98,2 (Saarbrücken/Halberg), 98,6 (Mettlach)
  - SR kultur/SR 2: 91,3 (Göttelborner Höhe), 88,5 (Mettlach), 88,6 (Moseltal), 92,1 (Merzig)
  - SR 3: 95,5 (Göttelborner Höhe), 89,1 (Bliestal), 96,0 (Mettlach), 96,1 (Moseltal), 98,0 (Merzig)
  - UNSERDING: 103,7 (Saarbrücken/Schoksberg), 90,3 (St. Wendel), 98,6 (Homburg)
- Notfalltreffpunkte bzw. Katastrophenschutz-Leuchttürme: Für Saarlouis, St. Wendel, Merzig-Wadern, Neunkirchen und für die Gemeinden des Regionalverbands außer Homburg (Saarpfalz) wurde keine veröffentlichte Liste gefunden. Regionalverband, Landeshauptstadt Saarbrücken, Quierschied und Heusweiler veröffentlichen auf den geprüften Seiten keine Liste.
- saarland.de (Innenministerium) war nicht abrufbar (Client-Fehler). Ob das Land KATWARN nutzt und wie der aktuelle Ministeriumsname lautet, ist nicht geprüft.
- Störungsnummern der Netzbetreiber: Belegt sind nur Stadtwerke Saarbrücken Netz (0681 587-0) sowie energis Strom und Gas (über die Gemeinde Heusweiler). Nicht belegt sind VSE Verteilnetz, Pfalzwerke Netz, KEW Neunkirchen, Stadtwerke Saarlouis, Völklingen, St. Ingbert und Wasserversorger anderer Gemeinden.
- Die Merzig-Wadern-Dokumente „Notfallplan zur Evakuierung“ und „Notfallplan für die saarländische Umgebung“ (vermutlich zum Kernkraftwerk Cattenom) wurden nicht geöffnet. Sie könnten Sammelstellen enthalten.

### technik.json
- Minimierte Ladegrößen von barcode-detector (JS-Teil), jsQR und quagga2: Es wurden nur die entpackten npm-Paketgrößen ermittelt.
- Weitere Open-Food-Facts-Nährwertfelder (proteins_100g, fat_100g, fiber_100g, salt_100g, vitamin-c_100g) sind in den gelesenen Doku-Seiten nicht gezeigt. Vor der Nutzung an einer Live-Antwort prüfen.
- iPhone: ob eine .ics-Datei direkt aus einem Safari-Download übernommen wird und ob ein VALARM erhalten bleibt, ist nicht belegt. Android: Laut Google-Hilfe gibt es keinen Import in der Kalender-App, nur am Computer. Das Verhalten beim Öffnen einer .ics-Datei über den Browser ist nicht belegt.

## 2. Widersprüche zwischen Quellen
- **Vorratsdauer:** BBK (Ratgeber 10/2025, Webseite) empfiehlt möglichst **10 Tage** (mindestens 3). Der Regionalverband Saarbrücken (Stand 10.10.2025) und der Saarpfalz-Kreis-Flyer (2019) nennen **14 Tage**, die Brandenburger Broschüre (2016) **zwei Wochen**. Für die App wird der BBK-Wert als Standard vorgeschlagen und der regionale Hinweis zusätzlich gezeigt.
- **Trinkwasser je Person:** Das BBK nennt 2 l/Tag (1,5 l Trinken + 0,5 l Kochen). Die WHO nennt 7 l/Tag als Überleben für wenige Tage (3–4 l Trinken). Sphere und die staatliche Notversorgung nennen 15 l/Tag (alle Zwecke). Die CDC rechnet mit 1 Gallone ≈ 3,8 l/Tag. Das sind unterschiedliche Bezugsgrößen, kein echter Fehler.
- **Abkochen:** Das UBA nennt „einmal sprudelnd aufkochen, mindestens 10 Minuten abkühlen“ ohne Kochdauer. Die CDC nennt „1 Minute sprudelnd kochen (über ~2.000 m: 3 Minuten)“.
- **Skorbut-Schwelle:** Die DGE-FAQ (2015) nennt **10 mg/Tag**, die DGE/ÖGE/SGE-Fachveröffentlichung (2015) **7 mg/Tag**.
- **Giftnotruf Saarland:** Das BfR (Stand 22.07.2026) nennt für das Saarland nur **GIZ Mainz 06131 19240**. Der Landkreis Neunkirchen und die Gemeinde Heusweiler nennen zusätzlich bzw. stattdessen **06841 19240** (Homburg). Vor der Veröffentlichung beim Land oder beim BfR klären. Die App nutzt vorerst den BfR-Wert.
- **Medikamentenvorrat:** Das BBK (2025) nennt mindestens 10 Tage, Brandenburg (2016) mindestens eine Woche.
- **Gefriergerät:** Die VZ Niedersachsen nennt „bis zu 48 Stunden“ für ein geschlossenes, volles Gerät. Andere amtliche Zahlen wurden nicht gefunden. Die Angabe ist nicht widersprüchlich, aber nur eine einzige Quelle.

## 3. Jährlich prüfen (Vorschlag: jeweils im Herbst vor dem Warntag)
- BBK-Ratgeber: neue Auflage? (aktuell 1. Auflage 10/2025)
- Termin des bundesweiten Warntags (nächster: 9. September 2027, 11 Uhr)
- Alle Telefonnummern in region_saarland.json und notfallplan.json (Bürgertelefon Saarpfalz-Kreis von 2019, Homburger Anlaufstellen von 2020, Störungsnummern, Giftnotruf)
- Neue Notfalltreffpunkt-Listen der Landkreise und Gemeinden im Saarland
- SBKG und Ministeriumsname (der gelesene Gesetzestext ist eine nicht amtliche Fassung von 2013)
- DGE-Referenzwerte (3. Auflage 2025; Eisen 2024 neu abgeleitet)
- caniuse/WebKit: BarcodeDetector in Safari standardmäßig aktiv?
- Open Food Facts: Abfragegrenzen (aktuell 15 Produkte bzw. 10 Suchen je Minute) und API-Version (v2/v3)
- Versionen von barcode-detector, zxing-wasm, lean-qr und jsqr (Lizenz unverändert?)
- Steckersolar-Regeln (800 W / 2.000 Wp) und VZ-Angaben
- Gefahrenhinweise (CO, Stromerzeuger) unverändert übernehmen, falls BBK-Texte neu formuliert werden
