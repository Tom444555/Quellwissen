# Bericht: Saarland-Ergänzungen Vorrats-/Blackout-Planer (abgerufen 26.11.2026)

Ergebnis: `neu.json` mit 30 Einträgen (Anlaufstellen 9, Störungsnummern 12, Zuständigkeit 1, Warnwege 8).

## 1. Anlaufstellen / Notfalltreffpunkte
**Gefunden (1 Gemeinde):**
- **Saarwellingen** – Projekt „Leuchtturm“: Bei großflächigem Stromausfall ab ca. 1 Stunde sind die notstromgespeisten Feuerwehrgerätehäuser im betroffenen Ortsteil besetzt. Quelle: Handakte Stromausfall (PDF, Stand März 2022). Die Adressen stammen von feuerwehrsaarwellingen.de/kontakt: Saarwellingen (Schloßstraße 31-33), Schwarzenholz (Dorfstraße 20), Reisbach (Kirchenstraße 73).

**Keine Liste gefunden („nicht gefunden“-Einträge):** Landkreis Neunkirchen, Landkreis St. Wendel (Kreis-Website und Blackout-Flyer der Kreisstadt), Merzig-Wadern (KatS-Plan Stromausfall laut Seite „in Bearbeitung“), Saarpfalz-Kreis (alter Flyer-Link gibt 404 zurück), Regionalverband Saarbrücken und Landeshauptstadt Saarbrücken. Für Landkreis Saarlouis besteht bereits `sls-liste`. Auch dort wurde nichts Neues gefunden.

**Gemeinden geprüft (Startseite und Sitemap-Stichwortsuche, 49 von 52 erreicht):** Keine Notfalltreffpunkt-Liste gefunden außer bei Saarwellingen. Erwähnenswert, aber kein Eintrag:
- Überherrn: „Überherrn sorgt vor“. Das sind ehrenamtliche Notfallvorsorgehelfer zur Beratung, keine Anlaufstellen. Kontakt 06836-7248100.
- Gersheim: Pressetext des Saarpfalz-Kreises zum AK Stromausfall. Die Krisenplanung geht von einem Stromausfall ab 2 Stunden und 10.000 Betroffenen aus.
- Ottweiler, Eppelborn, Kleinblittersdorf und St. Ingbert („Notfallmonitor“): nur Vorsorge-Tipps.

**Nicht erreichbar:** neunkirchen.de, nohfelden.de und kirkel.de (TLS-/Serverfehler), losheim(amsee).de, sulzbach-saar.de (Stadt-Site stadt-sulzbach.de dagegen geprüft).

**Grenzen:** Die Websuche lieferte kaum saarländische Treffer. Seiten, die ihren Inhalt erst per JavaScript nachladen, sowie Amtsblätter als PDF wurden nicht vollständig durchsucht. Gemeinden mit 1-Eintrag-Sitemap wurden nur über die Startseite geprüft.

## 2. Störungsnummern
Gefunden mit Beleg: VSE Verteilnetz, Pfalzwerke Netz, KEW Neunkirchen, Stadtwerke Saarlouis, Völklingen Netz, Homburg, St. Ingbert, Dillingen (swd-saar.de), Merzig, Bexbach, Sulzbach.
- Ausdrücklich „rund um die Uhr/jederzeit“: KEW, Saarlouis, Völklingen, Dillingen, Sulzbach.
- Ohne Zeitangabe: VSE, Pfalzwerke, Homburg, St. Ingbert, Merzig, Bexbach. Das steht jeweils im Feld `warnung`.
- **WVW St. Wendel:** www.wvw-wnd.de war nicht abrufbar (DNS-/Freigabefehler). Eingetragen ist nur die allgemeine Nummer 06851/8003-0 aus einer WVW-Kundeninformation von 2020 auf tholey.de, als „nicht gefunden“ markiert.
- Weitere Kreis- oder Kommunalwerke wurden nicht gezielt gesucht.

## 3. Warnwege / Zuständigkeit
- Aktueller Ministeriumsname: **Ministerium für Inneres, Bauen und Sport**. Bestätigt auf der MIBS-Startseite saarland.de/mibs. Die Rolle als oberste Katastrophenschutzbehörde steht auf der Katastrophenschutz-Seite des Landkreises Neunkirchen.
- **Eine Aussage des Landes zu den Warnmitteln konnte nicht gelesen werden.** saarland.de blockiert den automatischen Abruf (Bot-Schutz/403). Die Medieninformation „Warntag 2026: Saarland zieht positive Bilanz …“ vom 10.09.2026 ist nur aus dem Suchindex bekannt. Dafür gibt es einen „nicht gefunden“-Eintrag (`saar-warnwege-land`). Bitte von Hand im Browser prüfen.
- Ersatzweise aufgenommen (Kreis-Ebene, belegt):
  - Regionalverband: Cell Broadcast, NINA, KATWARN, Sirene, Radio, Lautsprecher, mit Sirenensignalen.
  - Landkreis Neunkirchen: NINA, KATWARN, warnung.bund.de, Sirene, Radio.
  - Merzig-Wadern: Sirenennetz, NINA.
- BIWAPP wurde auf keiner geprüften Seite genannt.

## 4. SR-UKW-Frequenzen
Die Frequenzen stammen von den Frequenzseiten des SR, gelesen per Direktabruf. Der WebFetch-Abruf von sr.de war gesperrt, deshalb wurde curl benutzt.
- SR 1: Göttelborner Höhe 88,0; Bliestal 92,3; Moseltal 91,9; Merzig 89,3; Mettlach 98,6; Saarbrücken-Halberg 98,2 MHz (Seite vom 02.03.2022).
- SR 3: Göttelborner Höhe 95,5; Bliestal 89,1; Moseltal 96,1; Merzig 98,0; Mettlach 96,0 MHz (Seite vom 27.10.2026).
- SR kultur: Göttelborner Höhe/Saarbrücken 91,3; Homburg 98,6; Moseltal 88,6; Merzig 92,1; Mettlach 88,5 MHz (Seite vom 21.01.2026).
- AntenneSaar: nur DAB+ (Block 9A) und Stream, keine UKW-Frequenz.
- „Schoenberg“ und „Spiegelberg“ stehen nicht in den SR-Listen. Bundesnetzagentur und Landesmedienanstalt wurden nicht geprüft. DASDING (SWR-Seite) wurde nicht aufgenommen.

## Suchwege (kurz)
WebSearch (ergab für das Saarland wenig), WebFetch, curl mit Textauszug, rekursive Stichwortsuche in den Sitemaps der Gemeinden, PDF-Auswertung mit pdftotext und Seitenbildern (Saarwellingen-Handakte, St.-Wendel-Flyer, KatS-Plan Merzig-Wadern).
