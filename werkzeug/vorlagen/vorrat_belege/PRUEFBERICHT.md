# PRÜFBERICHT – Gegenprüfung Vorrat & Blackout-Planer

Stand: 26.11.2026. Alle genannten Seiten am 26.11.2026 geöffnet (WebFetch).

## Die drei wichtigsten Befunde
1. **Kochkiste/Hygiene (waerme_kochen.json, kk-hygiene):** Die Vorgabe „70 °C für 2 Minuten“ steht nicht in der BfR-Stellungnahme 016/2024 – dort heißt es **72 °C für 2 Minuten** (für Gemeinschaftsverpflegung). 70 °C/2 min nennt das BfR in seiner FAQ „Vorkochen“ für Privathaushalte. Beide jetzt mit Quelle genannt; 60 °C Heißhalten bestätigt. Das BZfE nennt zur Kochkiste selbst keine Hygieneregel – ob 2–3 h Nachgaren in der Kiste mit „mindestens 60 °C“ vereinbar ist, belegt keine Quelle.
2. **Giftnotruf Saarland:** Nur 06131 19240 (GIZ Mainz) ist durch die aktuelle BfR-Liste (22.07.2026) gedeckt. 06841 19240 (Homburg) steht nur auf älteren Kreis-/Gemeindeseiten und in keiner aktuellen Bundesliste – vor Veröffentlichung klären, bis dahin nicht als gleichwertige Nummer zeigen.
3. **Viele Sicherheitstexte waren über die Quelle hinaus „ergänzt“:** z. B. „Toilettenspülung/Duschen ohne Abkochen“ (UBA nennt sie im Anhang A.3 nicht; dort: nur im Ausnahmefall, kurz, mit leicht erhöhtem Infektionsrisiko), Stromerzeuger „nicht in Garage/Keller“ (BBK: „nicht in Innenräumen“), erfundene Reihenfolge der CO-Symptome, Planungsfaktor Powerbank 0,75, „normal 120 l Wasser“. Alles auf den Quellwortlaut gekürzt. Außerdem **Widerspruch Kraftstofflagerung** (BBK 2015: 10 kg Benzin/20 kg Diesel im Keller vs. Feuerwehr Heidelberg: 20 l/200 l, Keller ungeeignet) – beide genannt.

## Übersicht
| Datei | geprüft | bestätigt | korrigiert | entfernt | nicht nachprüfbar |
|---|---|---|---|---|---|
| wasser.json | 31 | 12 | 19 | 0 | 0 |
| waerme_kochen.json | 34 | 12 | 22 | 0 | 0 |
| ablauf.json | 36 | 6 | 30 | 0 | 0 |
| strom.json | 30 | 10 | 20 | 0 | 0 |
| naehrstoffe.json | 41 | 18 | 23 | 0 | 0 |
| notfallplan.json (nur Nummern/Notruf) | 11 von 26 | 1 | 10 | 0 | 0 |
| region_saarland.json (nur Nummern/Warnwege) | 35 von 43 | 17 | 17 | 0 | 1 (KATWARN im Saarland) |

Kein Eintrag wurde entfernt: Bei jedem ließ sich ein belegter Kern halten. „Korrigiert“ heißt oft nur: Wortlaut an die Quelle angepasst, Zusätze gestrichen.

**Grenzen der Prüfung:** Die Original-PDFs beim BBK (Ratgeber 10/2025, Stromausfall 2015) lieferten per WebFetch nur Metadaten. Geprüft wurde deshalb an inhaltsgleichen Kopien (stadtarnstein.de, flussgebiete.nrw.de). dge.de, 116117.de, 115.de und telefonseelsorge.de waren nicht freigegeben, deshalb wurde an anderen amtlichen Seiten geprüft (BMG, verwaltung.bund.de, Bundesregierung, verbraucherzentrale.de).

---

## wasser.json (31 Einträge)
- Geprüft: 31 · bestätigt ohne Änderung: 12 · korrigiert: 19 · entfernt: 0 · nicht nachprüfbar: 0

**Bestätigt:** bedarf-trinken, bedarf-kochen, bedarf-vorrat, bedarf-beispiel, bedarf-ohne, quelle-wannen, quelle-eis, lager-tausch, lager-behaelter, wc-beutel, wc-spuelen, wc-behaelter (BBK-Webseite, BBK-Ratgeber 10/2025, Brandenburg 2016, CDC).
Hinweis: Der BBK-Ratgeber (Original-PDF bbk.bund.de) war per WebFetch nicht lesbar (nur Metadaten); geprüft an der Kopie stadtarnstein.de (Impressum „10/2025, 1. Auflage“, Herausgeber BBK). Vor Veröffentlichung einmal im Browser am Original gegenlesen.

**Korrigiert:**
- auf-ausnahmen: „Toilettenspülung, Duschen, Wäsche ab 40 °C, Spülmaschine ab 60 °C kommen kurzzeitig ohne Abkochen aus“ → UBA A.3 nennt Toilette/Duschen dort nicht; richtig: „im Ausnahmefall für kurze Zeit, bei leicht erhöhtem Infektionsrisiko“: Spülmaschine ≥ 60 °C bzw. Heißtrocknung, Waschmaschine ≥ 40 °C, Körperpflege/Reinigung (nicht Kleinkinder, Kranke, Immungeschwächte); Toilettenspülung nur im UBA-Mustertext A.4. (UBA, S. 94–95, 98)
- auf-wofuer: Liste an UBA-Wortlaut angepasst (Obst, Gemüse, Getränke, ungekochte Nahrungsmittel; Körperpflege „zumindest“ bei Kleinkindern/Kranken/Immungeschwächten).
- auf-abkochen: „mindestens 10 Minuten abkühlen“ bestätigt; Text auf UBA-Wortlaut („langsam über mindestens 10 Minuten“, „handelsübliche Wasserkocher“), Verbrühungswarnung wortgetreu. Quelle-Stand: 11.02.2026 statt „Februar 2026“.
- auf-abkochen-international: 6500 Fuß ergänzt, „oder absetzen lassen“ ergänzt (CDC).
- auf-tabletten: Präzisiert: Iod und Chlor töten Cryptosporidien nicht, nur Chlordioxid; Iod-Warnung wortgetreu („nicht länger als einige Wochen am Stück“). Keine Dosierung.
- auf-filter: Warnung „Filter machen chemisch verunreinigtes Wasser nicht sicher“ entfernt – steht so nicht in der CDC-Quelle (CDC sagt das nur für Abkochen/Entkeimen; siehe quelle-chemie). Giardien/Cryptosporidien ergänzt.
- bedarf-notbrunnen: Satz „Normal sind es etwa 120 Liter“ entfernt – steht nicht auf der BBK-Seite.
- bedarf-sphere: „für den Haushalt“ → „für Trinken, Kochen und Körperpflege im Haushalt“ (Sphere-Wortlaut).
- bedarf-who-hygiene: „bei längerer Notlage“ → „mittelfristige Notlage (insgesamt 15–20 l)“ (WHO TN 9, Tabelle 1).
- bedarf-toilette: Handlungsratschlag „sparsam spülen oder Alternativen nutzen“ entfernt (nicht in Quelle).
- bedarf-who-ueberleben, bedarf-who-hygiene, bedarf-toilette: Quelle von slideshare auf inhaltsgleiche Kopie bei medbox.org umgestellt (eine who.int-Fassung war nicht auffindbar; beides nicht amtliche Kopien).
- quelle-boiler: Warnung „Wasser aus Heizkörpern … niemals“ → CDC-Aussage: nur Trinkwasser-Warmwasserspeicher, nicht Speicher der Heizungsanlage.
- quelle-spuelkasten: „keine färbenden Reinigungsmittel“ → „nicht chemisch mit Toilettenreinigern behandelt“ (CDC).
- quelle-regen: „im Freien“ → „außerhalb des Hauses“; CDC-Hinweis zu Treibstoff/Chemikalien ergänzt.
- quelle-pool: „Whirlpools“ präzisiert (CDC: „spas“).
- quelle-chemie: Warnung „nicht zum Waschen“ entfernt (nicht in Quelle) → „nicht verwenden; abgefülltes Wasser oder andere Quelle; Gesundheitsamt fragen“.
- auf-gefaesse, lager-ort (°F-Bereich ergänzt), lager-mineral (Wortlaut BBK: „gewisser Anteil“, Säfte zählen mit): sprachlich an Quelle angepasst.

**Offen:** keine deutsche Behördenangabe zur Lagerdauer von abgefülltem Leitungswasser (nur CDC) – wie in OFFEN.md.

---

## waerme_kochen.json (34 Einträge)
- Geprüft: 34 · bestätigt ohne Änderung: 12 · korrigiert: 22 · entfernt: 0 · nicht nachprüfbar: 0

**Bestätigt:** b-fluessiggas (45 355 kJ/kg), b-kartusche-190/-230/-450 (Rechnung 2,39/2,90/5,67 kWh nachgerechnet), b-petroleum (42 803 kJ/kg), b-holz-rm, b-holz-trocken, b-wasser-1l (4190 J/(kg·K); 356 kJ ≈ 0,099 kWh), b-gas-je-liter (≈ 7,9 g), h-ein-raum, h-teelichtofen, h-elektro.

**Korrigiert – wichtig:**
- kk-hygiene: „mindestens 70 °C für 2 Minuten“ war der BfR-Stellungnahme 016/2024 zugeschrieben – dort steht **72 °C für 2 Minuten** (S. 22, Korrekturmaßnahme für Gemeinschaftsverpflegung); 70 °C/2 min steht in der BfR-FAQ „Vorkochen für mehrere Tage“ (Privathaushalt). Beide jetzt genannt. 60 °C Heißhalten „an allen Stellen bis zum Verzehr“ bestätigt (Stellungnahme 016/2024 vom 19.03.2024). Nicht belegte Ratschläge („gleich essen“, „Reste nicht in der Kiste stehen lassen“) entfernt; Warnung jetzt BfR-belegt (unter 57 °C deutliche Keimvermehrung binnen 4 h; vorgebildete Gifte nicht hitzezerstörbar). Hinweis: Das BZfE nennt zur Kochkiste keine Hygieneregel – ein Konflikt zwischen 2–3 h Garzeit in der Kiste und der 60-°C-Regel ist damit nicht amtlich aufgelöst.
- k-innen: Stövchen nur zum **Aufwärmen**, Fondue nur **kleine Mengen** (BBK-Ratgeber); Warnung „unsichtbares, geruchloses CO“ auf BBK-Wortlaut umgestellt.
- k-aussen: Warnung „Nicht in der Wohnung grillen – Erstickungsgefahr“ stammt von der BBK-Webseite, nicht aus dem zitierten Ratgeber → durch Ratgeber-Wortlaut (CO lebensgefährlich) ersetzt. (Die Grill-Warnung steht weiter in h-grill-heizstrahler.)
- co-symptome: erfundene Abfolge („zuerst …, später …“) entfernt; Liste der Quelle übernommen (inkl. Druck auf der Brust, Sehstörungen).
- co-melder: BBK-Aussage („geprüfte und zugelassene“) und KBI-Dachau-Empfehlung (EN 50291) getrennt; Montagehinweise bestätigt.
- h-zugelassen, h-kamin, h-lueften: an BBK-Wortlaut angepasst („Sicherungsmechanismen“; Fachberatung zur Installation; Stoßlüften – „besonders bei Kerzen und Öfen“ stand nicht im Ratgeber).
- b-butan: „n-Butan“ → „Butan“ (Tabelle nennt nur Butane, 45,277 MJ/kg).
- b-ethanol: Spekulation „Brennspiritus … daher Obergrenze“ → „Wert gilt für reines Ethanol“.
- k-deckel: Aussage bestätigt; Topfgröße-Hinweis aus derselben BZfE-Meldung ergänzt.
- kk-prinzip, kk-erbsen, kk-milchreis, kk-geeignet, k-gerichte, k-haftung („könnte“ statt „kann“), k-lueften, h-kleidung, h-grill-heizstrahler (Heizpilz; CO-Warnung nach KBI), co-alarm, b-holz-kg: Wortlaut angepasst.

**Quellenbewertung:** KBI Dachau (Kreisbrandinspektion, Landkreis-Feuerwehr) und Stadt Plettenberg sind kommunale Stellen; Plettenberg nennt keine Herkunft seiner Texte. GREET-Tabelle liegt nur als Kursunterlage der Univ. Illinois vor.

---

## ablauf.json (36 Einträge)
- Geprüft: 36 · bestätigt ohne Änderung: 6 · korrigiert: 30 · entfernt: 0 · nicht nachprüfbar: 0
- Reihenfolge (Erste Stunde → Tag 4–10 → Strom wieder da) ist redaktionell, aber plausibel; nichts Gefährliches gefunden. Viele Texte enthielten kleine Zusätze, die in der Quelle nicht stehen – auf Belegtes gekürzt.

**Bestätigt:** h1-pruefen (Stadtwerke Saarbrücken, 0681 587-0), h1-kuehlgeraete-zu (VZ Nds: 4–6 h), t1-gefrier (VZ Nds: bis 48 h, −18 → −12 °C laut BfR), t1-trinken, t410-vorrat, t410-wasser.
BBK-Broschüre „Stromausfall“ (Mai 2015): Original-PDF bei bbk.bund.de per WebFetch nicht lesbar (nur Metadaten), geprüft an der Kopie flussgebiete.nrw.de (Ausgabe 1, Stand Mai 2015).

**Korrigiert – wichtig:**
- t410-kraftstoff: **Widerspruch** – BBK 2015: Keller höchstens 10 kg Benzin / 20 kg Diesel, Gas nicht im Keller; Feuerwehr Heidelberg: zu Hause höchstens 20 l Benzin / 200 l Diesel, Keller und Wohnräume ungeeignet. Beide genannt, nicht entschieden.
- t1-nicht-generator: Warnung „niemals in Wohnung, Keller oder Garage“ → BBK-Wortlaut „nicht in Innenräumen“ (Garage nennt die Quelle nicht); Brandgefahr beim Betanken/heiße Teile bestätigt.
- h1-geraete-aus: „Heizdecken und Heizlüfter“ und Warnung „Brand bei Stromrückkehr“ standen nicht in der Quelle → BBK-Liste (Herd, Ofen, Bügeleisen, Kaffeemaschine, Wasserkocher) und Begründung „unkontrollierter Betrieb“.
- h1-telefon: „110 und 112 … nicht für Auskünfte“ nicht in BBK 2015 → „Notrufstellen nur in wirklichen Notfällen“; „Stromausfall an sich ist kein Notfall“ (Saarpfalz-Flyer).
- t1-nachbarn: „ältere, pflegebedürftige, allein lebende Menschen“ nicht in Quelle → „vielleicht benötigen sie Hilfe oder können helfen“.
- t23-medikamente: „Rechtzeitig nachfragen“ nicht belegt → entfernt; Widerspruch 10 Tage (BBK 2025) / 1 Woche (Brandenburg 2016) genannt.
- t410-gemeinschaft: 93 % = „gehen davon aus, dass Nachbarschaftshilfe zur Verfügung steht“ (nicht „erwarten“); „Notfalltreffpunkte nutzen“ → BBK 2015: bei Gemeinde erfragen, wo Notruf ohne Telefonnetz möglich.
- t410-lueften: „mehrmals täglich“ nicht belegt → BBK-Wortlaut.
- n-vorrat: „Powerbanks laden, BBK-Checkliste nutzen“ nicht belegt (Ratgeber empfiehlt keine regelmäßige Prüfung ausdrücklich) → Saarpfalz-Flyer „verbrauchte Vorräte ergänzen“, Quelle umgestellt.
- n-geraete-pruefen: Brandenburg beschreibt keine Prüfung nach Rückkehr, nur, dass nicht ausgeschaltete Geräte sich wieder einschalten → Text angepasst.
- n-gefrier: „durchgehend gefroren prüfen“ nicht in VZ-Text → Saarpfalz-Wortlaut + VZ-Hinweise.
- h1-wasser-sichern: „Eimer, Töpfe“ nicht in Quelle → entfernt.
- h1-anzeige: Begründung korrigiert (Flyer: Netzüberlastung bei Rückkehr, Radio/Lampe als „Stromkontrollgerät“).
- h1-radio, h1-akkus, h1-licht, t1-kochen (Stövchen nur Aufwärmen), t1-waerme, t1-bargeld (Kartenzahlung laut Ratgeber), t1-pflege, t1-lebensmittel, t1-nicht-heizer, t23-toilette, t23-hygiene, t23-kuehlgut-pruefen, t23-angetaut, t23-informiert, h1-ruhe, n-nacheinander, n-feucht: Wortlaut an Quelle angepasst bzw. Herkunft je Satz angegeben.

---

## strom.json (30 Einträge)
- Geprüft: 30 · bestätigt ohne Änderung: 10 · korrigiert: 20 · entfernt: 0 · nicht nachprüfbar: 0

**Bestätigt:** v-smartphone (33 Ladungen), v-laptop (10), v-lichterkette (65 h) – Warentest 07.01.2026; v-kgk-neu (157 kWh), v-kgk-alt (392 kWh), v-kuehl-klein (knapp 100 kWh), v-gefriertruhe (12 %) – Infoblatt VZ RLP/Öko-Institut 09/2012; v-pumpe-alt (60–100 W), v-pumpe-neu (15 W) – VZ-RLP-Pressemitteilung 20.05.2025 (nur über VG Lingenfeld abrufbar; die UBA-Seite „Heizungsumwälzpumpe“, Stand 04.11.2026, nennt keine Watt, sondern > 200 kWh/Jahr alt bzw. ≈ 40 kWh/Jahr hocheffizient); pv-stromausfall (VZ: Wechselrichter braucht Netzverbindung – Balkonkraftwerk funktioniert bei Netzausfall nicht).

**Korrigiert – wichtig:**
- s-powerbank-real: Eigene Planungsempfehlung „zwei Drittel bis drei Viertel ansetzen“ (wert 0,75) war nicht belegt → entfernt; wert auf niedrigsten Messwert 0,73 (Messwerte 8.400/9.010/14.760/17.680 mAh nachgerechnet: 73–90 %).
- g-draussen: Warnung „niemals in Wohnung, Haus, Keller oder Garage“ → BBK-Wortlaut „nicht in Innenräumen“.
- g-tanken: **Widerspruch** BBK 2015 (10 kg Benzin/20 kg Diesel im Keller) vs. Feuerwehr Heidelberg (20 l Benzin/200 l Diesel, Keller ungeeignet) – beide genannt.
- v-medizin: „klärt mit Arzt, Pflegedienst und Hersteller“ / Warnung „keine Bastellösungen“ stehen nicht in BBK 2015 → auf Belegtes gekürzt (Beatmungsgeräte lebensnotwendig; Pflegedienste fragen). Empfehlung: für einen Arzt-/Hersteller-Hinweis eine eigene Quelle suchen.
- v-waermegeraete: „zu viel für die meisten Notstromlösungen“ nicht belegt → ersetzt durch BBK-Hinweis zur Eignung für empfindliche Geräte.
- pv-ertrag-jahr: „1.000 kWh je kWp (Deutschland)“ nicht in Quelle → „umgerechnet ≈ 100 kWh je 100 Wp“, Hinweis auf Ausrichtung/Verschattung.
- g-einspeisen: „über einen Umschalter“ → „manuell oder automatisch“; „vorher informieren“ präzisiert.
- v-led (Umrechnung als solche gekennzeichnet), v-temp, v-gefrier-hoch, v-router, s-formel (10.000 mAh = 37 Wh ist eigene Rechnung), s-powerstation-solar, pv-speicher, pv-grenzen („aktuell“), g-verbrauch (0,597 l/kWh nachgerechnet; „Ökoschaltung“), g-laerm, g-heidelberg, a-akkus: Wortlaut.

**Offen:** PVGIS-Monatswerte weiter offen (nicht Gegenstand dieser Prüfung).

---

## naehrstoffe.json (41 Einträge)
- Geprüft: 41 · bestätigt ohne Änderung: 18 · korrigiert: 23 (davon viele nur Wortlaut/Stand) · entfernt: 0 · nicht nachprüfbar: 0

**Bestätigt (Zahlen):** prio-wasser; Energie 2.000/1.600/2.600/1.100 kcal (DGE-FAQ Energie 2015); Eiweiß 1,0/0,8/1,0 g/kg (DGE-FAQ Protein 01/2021); Fett 30–35 %, KH > 50 % (DGE 01/2011); Ballaststoffe ≥ 30 g, 14,6 g/1.000 kcal (DGE 11/2021); Vitamin C alle Altersgruppen 20/30/45/65/85/105/90/110/95 mg, Raucher 155/135, Schwangere ab 4. Monat 105, Stillende 125 (DGE/ÖGE/SGE 2015); Calcium 600 (Karger 2013), 750, 1.100 (DGE-FAQ 06/2013), 1.200, 1.000; Eisen Männer 11, Frauen prämenopausal 16, postmenopausal 14, ohne Menstruation 11 (VZ-PDF 08/2024); Paprika 140 mg (BfR 16.03.2026); Kartoffel 18,76/14,86 mg (BLS 3.02); Weißkohl 45 mg; Sanddorn 450 mg; Hagebutte > 1.000 mg; Portion > 155 mg (DGE-FAQ).

**Korrigiert:**
- fe-schwanger: Quelle war ein Fachportal (apotheke-adhoc) → ersetzt durch verbraucherzentrale.de (Stand 21.07.2026, D-A-CH-Werte, Ableitung 2023): Schwangere 27 mg, Frauen auch in der Stillzeit 16 mg. Werte bestätigt. (dge.de selbst war nicht abrufbar – Seite nicht freigegeben.)
- q-sanddorn: „Sanddornsaft … über 100 mg je 100 g“ steht nicht im Warentest-Artikel → entfernt.
- q-hagebutte: „(frisch)“ steht nicht in der Quelle → „frisch oder getrocknet nicht angegeben“.
- q-weisskohl: „bis zu 6 Monate“ → „bis zu einem halben Jahr bei knapp über 0 °C und hoher Luftfeuchte“ (LfL).
- prio-vitamine: Mangelzeichen stammen vom BfR, nicht aus der zitierten Karger-Arbeit → Herkunft je Satz angegeben; Körperbestand gilt laut Quelle für erwachsene Männer.
- prio-skorbut: Widerspruch 10 mg (DGE-FAQ) / 7 mg (DGE/ÖGE/SGE) bleibt, beide genannt.
- q-zusatz: „Mengen werden nicht angegeben“ ist keine BfR-Aussage → entfernt; Beispiele nach BfR-Wortlaut.
- prio-energie: „20 Liter Getränke“ → „20 Liter Mineralwasser (1,5 + 0,5 l je Tag)“.
- en-*: Stand 2015 im Text ergänzt; p-19-65 (BMI 18,5–24,9), p-65 („Schätzwert für angemessene Zufuhr“), p-4-19 (von 1,0 auf 0,8), f-erw (30 % = sitzende Tätigkeit), b-erw, b-kind, c-m/c-w (auch ab 65), fe-w-post, q-kartoffel-roh, q-portion: Wortlaut präzisiert.

**Offen:** Calcium 7–<10 Jahre und Eisen für Kinder weiter ohne Beleg (dge.de nicht abrufbar). Energiewerte nach FAQ 2015 – prüfen, ob die DGE inzwischen neue Energiewerte veröffentlicht hat.

---

## notfallplan.json + region_saarland.json – Telefonnummern, Notruf, Warnwege
Geprüft wurden nur die Nummern-, Notruf- und Warn-Einträge (Auftrag Punkt 6): notfallplan 11 von 26, region_saarland 35 von 43. Nicht geprüft (nicht Auftrag): Treffpunkt-/Familienplan-Felder und SBKG-Zuständigkeiten (z-*, *-liste).

**Bestätigt (Nummer an amtlicher bzw. Stellen-eigener Seite):**
- 112, 110, 115, 116117, Telefonseelsorge (BBK-Ratgeber; zusätzlich BMG, verwaltung.bund.de, Bundesregierung)
- GIZ-Liste BfR (Stand 22.07.2026): Berlin 030 19240, Bonn 0228 19240, Freiburg 0761 19240, Göttingen 0551 19240, Mainz 06131 19240 (zuständig für RLP, Hessen, Saarland), München 089 19240, Erfurt 0361 730730
- Stadtwerke Saarbrücken Netz 0681 587-0 (Stadt Saarbrücken und Stadtwerke-PDF)
- energis Strom 0681 9069-2611, Erdgas 0681 9069-2610, Wasser-Rufbereitschaft 0681 587-5050, Rettungsleitstelle 19222 / 0681 19222 (Heusweiler, 02.05.2024)
- Gemeindewerke Quierschied 06897 961-201 / 0171 4258714, Rathaus 06897 961-0
- Regionalverband 0681 506-0; Landkreis Neunkirchen 06824 906-0; Bürgertelefon Saarpfalz-Kreis 06841 104-7000 (Flyer 04/2019 – Aktualität offen)
- Homburger Anlaufstellen (alle Adressen, „großflächig, länger als 30 Minuten“; Pressemitteilung 23.12.2020 – Aktualität offen)
- Sirenen (BBK-Ratgeber: 1 min an-/abschwellend = Warnung, 1 min Dauerton = Entwarnung), Warntag (2. Donnerstag im September, ~11 Uhr / ~11:45 Uhr, nächster 09.09.2027 – Bundesregierung 21.09.2026), Cell Broadcast (5-mal/2 min, keine Nachlieferung, WLAN-Tablets – VZ 15.09.2026), nora.

**Korrigiert – wichtig:**
- **Giftnotruf Saarland:** 06841 19240 (Homburg) steht nur noch auf Kreis-/Gemeindeseiten (Neunkirchen ohne Datum, Heusweiler 2024, Saarpfalz-Merkblatt „Stand 2017“). Die aktuelle BfR-Liste kennt Homburg nicht; das GIZ Mainz bezeichnet sich als zuständig „für das Saarland“; die Uni des Saarlandes (KlinTox) verweist für Vergiftungsberatung an das „nächstgelegene Giftinformationszentrum“. → In nr-gift-saar, z-giftnotruf, nk-gift einheitliche Warnung: Mainz verwenden, Homburg-Nummer vor Veröffentlichung beim Land/GIZ Mainz klären. Nicht entschieden, aber deutlich gemacht.
- heu-leitstelle: „Krankentransport 19222“ → Heusweiler nennt 19222 für „medizinische Notfälle im Regionalverband“ (Rettungsleitstelle Winterberg); 112 und 110 ergänzt.
- heu-wasser: Vorwahl „(06806)“ stand nicht auf der Seite → als „Ortsvorwahl nicht angegeben“ gekennzeichnet.
- nr-112: „kostenfrei“ nicht belegt → „europaweit einheitlich“ (BMG), Lebensgefahr-Beispiele.
- nr-115: Erreichbarkeit Mo–Fr 8–18 Uhr, Ortstarif ergänzt (verwaltung.bund.de).
- nr-116117: „deutschlandweit, kostenfrei; bei Lebensgefahr 112“ (BMG 2019).
- nr-seelsorge: Bundesregierung bestätigt 0800 111 0 111 / 0800 111 0 222 („kostenfrei, anonym, rund um die Uhr“); 116 123 nur im BBK-Ratgeber.
- w-sirene-warnung: „Radio einschalten“ → BBK-Wortlaut „Es besteht Gefahr – informieren Sie sich“.
- w-nina: DWD-Wetterwarnungen standen nicht im zitierten Ratgeber → Quelle Bundesregierung (2021); Ausfall bei Netzausfall laut BBK-Ratgeber.
- w-katwarn: „Kritischer Alarm ertönt bei höchster Warnstufe“ → muss in der App aktiviert werden, gilt für „hohe Warnstufe (violett)“, nicht für Unwetter. Nutzung von KATWARN im Saarland weiter **nicht nachprüfbar** (saarland.de nicht abrufbar, keine Landesquelle gefunden).
- w-cb-iphone/-android, w-cellbroadcast, w-radio, spk-buergertelefon, spk-licht, sb-erst, ab-warn, ab-gift (Erfurt einsortiert), ohne-netz, nora, nr-eigene, notfallausweis: Wortlaut.

**Hinweis Landkreis Neunkirchen:** Auf der Seite verweist der Telefon-Link des GIZ auf „06131 1920“, angezeigt wird 06131 19240 – Fehler auf der Kreisseite, nicht in unserer Datei.
