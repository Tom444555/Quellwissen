# Offene Punkte, Unsicherheiten, Prüfumfang (Stand 25.11.2026, nach unabhängiger Gegenprüfung)

Einzelheiten der Gegenprüfung (geprüft/bestätigt/korrigiert/entfernt je Ebene, mit Quellen): `PRUEFBERICHT.md`.

## Nicht geliefert
- **Welterbe-Einzelstätten mit Lage:** UNESCO verlangt für Weiterveröffentlichung ihrer Daten eine schriftliche Genehmigung (FAQ <https://whc.unesco.org/en/faq/126>). Wikidata (CC0) war nicht abrufbar. Geliefert wird nur die **Anzahl je Land** (Factbook, gegen UNESCO-Statistik geprüft, Stand nach der 48. Sitzung Juli 2026).
- **Seekabel:** TeleGeography steht unter CC BY-NC-SA → ausgeschlossen; keine frei lizenzierte Alternative gefunden.
- **Goldreserven vollständig:** weiterhin nur 22 Länder. Die WGC-Tabelle „World Official Gold Holdings“ darf laut WGC-Bedingungen ohne schriftliche Erlaubnis nicht weiterverbreitet werden; der IWF-Datensatz (IFS/IRFCL, mit Quellenangabe frei) war aus der Arbeitsumgebung nicht abrufbar (data.imf.org nur als Skriptseite, IWF-Länderseiten antworteten nicht, DBnomics-Kopie Stand 08/2025). → Vervollständigen über IWF IFS von einem Rechner mit Zugang zu data.imf.org.

## Rechtliches vor Veröffentlichung
- **IWF-Daten (Staatsschulden):** Weitergabe mit Quellenangabe erlaubt; **kommerzielle Weiterverwendung nur mit Genehmigung (copyright@imf.org)**. Falls App oder Buch verkauft werden: vorher anfragen oder die Ebene in der Bezahlfassung weglassen.
- Unicode License v3 (CLDR): frei mit Hinweis (Pflicht-Namensnennung in QUELLEN.md).
- Wikipedia-Zusammenstellung (Reiche): nur Fakten übernommen.

## Offen nach der Gegenprüfung
- **Bündnisse:** alle 18 Listen an amtlichen bzw. benannten Seiten geprüft. Offen: OVKS-Beitrittsjahr Georgien (1993 Unterzeichnung / 1994 Inkrafttreten). AU-Suspendierungen zuletzt amtsnah belegt 02/2026 (bis 11/2026 keine Änderung gefunden).
- **Stützpunkte:** alle 92 Lagen gegen Natural Earth/GeoNames geprüft; Status von 26 Einträgen einzeln belegt. Die übrigen ~66 lange bestehenden Standorte nicht einzeln an amtlicher Quelle 2026 geprüft (keine Hinweise auf Änderungen). Nicht bestätigt (im Datensatz gekennzeichnet): Lage Tariq bin Ziyad (Katar), heutige türkische Präsenz in Al-Watiya. Vilseck: Betroffenheit vom angekündigten US-Abzug amtlich offen. Weiterhin weggelassen: US-Präsenz im Irak, russisches „Africa Corps“, Radaranlagen Belarus, indischer Standort Tadschikistan.
- **Frühe Stätten:** Lagen alle plausibel; Datierungen von 15 Stätten einzeln belegt (5 korrigiert), übrige 63 gängige Darstellung ohne Einzelbeleg. Pömmelte weiterhin weggelassen.
- **Leitungen:** Verläufe korrigiert (keine Linie mehr durch falsche Staaten/Meere, außer Baltic Pipe: Beginn im norwegischen Sektor). Kapazitäten der meisten Leitungen sind Betreiberangaben aus dem Wissensbestand, nicht einzeln abgerufen; East-West-Pipeline-Kapazität als „nicht amtlich bestätigt“ gekennzeichnet. Kein Längenfeld im Format.
- **Engstellen:** EIA-Werte 1. Hj. 2025 alle bestätigt; Zahlen für 2026 gibt die EIA noch nicht in der Tabelle an.
- **Reiche, Handelswege, Fahrten:** schematisch; grobe Fehler behoben. Feinheiten der Länderlisten (Grenzfälle) bleiben vereinfacht.
- **Staatsschulden:** 44 von 114 Werten direkt in der IWF-Tabelle geprüft (alle G20, alle Nachbarn Deutschlands) – alle richtig; übrige 70 aus derselben Tabelle, nicht einzeln abgelesen.
- **Währungen:** Liberia – US-Dollar laut älteren Berichten (2017) gesetzliches Zahlungsmittel neben dem Liberianischen Dollar; aktueller Rechtsstand nicht bestätigt, daher wie CLDR nur LRD.
- **Kraftwerke:** IAEA PRIS war nicht abrufbar (Weiterleitung auf Skript-Anwendung). Status von 41 Kernkraftwerks-Standorten belegt (Deutschland, Japan, Kanada, Korea, Pakistan, Iran, Argentinien, Taiwan, Belgien, Einzelanlagen). Übrige ~156 Standorte (v. a. USA, Frankreich, Russland, China, Indien) nicht einzeln gegen PRIS geprüft; Teil-Stilllegungen an weiterbetriebenen Standorten stecken noch in `mw`. WRI-Datenbank seit 2021 nicht fortgeschrieben – neue Anlagen (z. B. Rooppur, Akkuyu, chinesische Neubauten) fehlen.
- **Sprachen:** Stichprobe 34 Länder, 3 Amtssprachen korrigiert (Schweiz, Nigeria, Israel). Nicht stichprobengeprüfte Länder können ähnliche CLDR-Eigenheiten haben (regionale Amtssprachen, Dialekte als Amtssprache) → bei Gelegenheit alle Länder automatisch gegen „(official)“ im Factbook abgleichen.
- **Religionen:** Stichprobe 20 Länder, Zuordnung korrekt. Factbook-Schätzjahre teils alt (USA 2014, Russland 2006); Pew Research 2025 wäre neuer (Bedingungen nicht geprüft).
- **Welterbe:** Zählweise: Vertragsstaaten nach UNESCO (inkl. Überseegebiete), Gebiete mit eigener Fläche zusätzlich (Lage-Prinzip). Bei 11 korrigierten Ländern fehlt die Aufteilung Kultur/Natur.

## Vorbehalte (unverändert gültig)
- **Sprachen:** CLDR-Sprecheranteile zählen Zweitsprachler mit; „verbreitetste Sprache“ = Sprache mit Amtsstatus und höchstem Anteil (Abweichungen in `allg`).
- **Religionen:** Prozentzahlen automatisch aus dem Factbook-Freitext; Libanon summiert laut Quelle auf 105 %; Tschechien mit hohem Anteil „ohne Angabe“. Factbook im Februar 2026 eingestellt.
- **Koordinaten von Hand** (frühe Stätten, Stützpunkte, Wegpunkte): jetzt gegen Natural Earth/GeoNames gegengeprüft (Schwelle 0,2°). Erklärbare Prüfwarnungen: Osterinsel, Ascension, Agaléga (zu klein für den Umriss), Offshore-Windparks, zwei Küstenkraftwerke Taiwans, Sewastopol (liegt in der App-Karte im RUS-Polygon; Datensatz führt `gast:'UKR'` mit neutraler Beschreibung).
