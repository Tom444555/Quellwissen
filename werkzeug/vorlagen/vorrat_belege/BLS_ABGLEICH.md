# BLS 4.0 – Lizenzprüfung und Abgleich mit dem Vorrats-Katalog

Stand der Prüfung: 26.11.2026. Arbeitsordner: /home/claude/scratch/bls/

## 1. Lizenz und Bezug

**Bezug:** frei, ohne Anmeldung. Die ZIP-Datei liegt unter https://www.blsdb.de/assets/uploads/BLS_4_0_2025_DE.zip (14,3 MB). Sie enthält:
- BLS_4_0_Daten_2025_DE.xlsx (7.140 Lebensmittel, 138 Nährstoffe, zu jedem Wert Datenherkunft und Referenz)
- BLS_4_0_Components_DE_EN.xlsx (Nährstoffcodes, Einheiten, Formeln)
- BLS_4_0_Dokumentation_DE.pdf

Ich habe mich nirgends registriert und keine Bedingungen per Klick akzeptiert.

**Lizenz, Wortlaut der Download-Seite (blsdb.de/download):**
> „Die Daten des Bundeslebensmittelschlüssels (BLS) stehen als Open Data zur freien Verfügung. Die Nutzung ist unter der Lizenz CC BY 4.0 (Creative Commons Namensnennung 4.0 International) gestattet. Bei Verwendung ist das Max Rubner-Institut als Herausgeber zu nennen."
>
> Zitierweise: „Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0 — Deutsche Nährstoffdatenbank. Karlsruhe. DOI: 10.25826/Data20251217-134202-0"

**FAQ Nr. 17 (blsdb.de/faq):**
> „Der BLS 4.0 wird kostenfrei und ohne Lizenzbarrieren bereitgestellt. Die Daten können frei genutzt werden – für wissenschaftliche Forschung und Lehre, Ernährungsberatung und -planung, App- und Softwareentwicklung sowie in der Lebensmittelindustrie."

Die mitgelieferte Dokumentation sagt dasselbe.

**Was CC BY 4.0 für die App bedeutet:**
- **Kommerzielle Nutzung:** erlaubt. CC BY hat keine NC-Klausel, und das MRI nennt App-Entwicklung und Industrie ausdrücklich. Eine verkaufte App ist also zulässig.
- **Bearbeitung:** erlaubt, also Umrechnen, Auswählen, Runden und Mischen mit USDA-Werten. Änderungen müssen kenntlich gemacht werden.
- **Weitergabe einzelner Werte oder Auszüge in der App:** erlaubt. CC BY 4.0 deckt auch das Datenbank-Herstellerrecht (sui generis) ab.
- **Pflichten:**
  1. Das MRI als Urheber nennen, am besten mit der Zitierweise oben.
  2. Die Lizenz nennen und verlinken (CC BY 4.0, https://creativecommons.org/licenses/by/4.0/deed.de).
  3. Angeben, dass Werte verändert oder ausgewählt wurden.
  4. Nicht den Eindruck erwecken, das MRI unterstütze die App.
  5. Keine technischen oder vertraglichen Zusatzbeschränkungen, die anderen die lizenzierte Nutzung genau dieser Daten verbieten. Ein normaler App-Store-Vertrieb ist unproblematisch.
- **Umsetzungsvorschlag:** In der App eine Seite „Quellen“ mit diesem Text: „Nährwerte teilweise aus: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS) 4.0, DOI 10.25826/Data20251217-134202-0, Lizenz CC BY 4.0; Werte ausgewählt/gerundet.“ Dazu je Lebensmittel das Quellenkennzeichen, das es mit q/vq schon gibt.

**Version und Stand:** BLS 4.0, Dokumentation „Stand: Dezember 2025“. Die DOI ist auf den 17.12.2025 datiert. Ein neuerer Stand ist auf blsdb.de nicht genannt.

## 2. Zuordnung

- **Zuordnungsquote:** 154 von 157 Einträgen (98 %).
  - 137 Einträge passen direkt, mit gleichem Zustand (roh, trocken, Konserve abgetropft usw.).
  - 17 Einträge sind nur als Näherung zugeordnet und in abgleich.json mit `hinweis` markiert. Beispiele:
    - Sardinen in Öl → Sardine roh, weil der BLS keine Ölkonserve führt
    - Makrele → Makrele im eigenen Saft
    - Erbseneintopf, Chili, Gulasch, Baby-Menü → Rezepturen statt Konserven
    - Kaffee → nur als Getränk vorhanden (der Katalog setzt den Kaffee ohnehin mit 0 an)
    - Hartkäse → Bergkäse 45 %
    - Mischbrot → Roggenmischbrot
    - Müsli → Knuspermüsli gesüßt
    - Hack und Hähnchen → roh statt tiefgekühlt
- **Ohne Treffer (3):** Säuglingsmilch-Pulver, Getreidebrei-Pulver für Babys, Obstbrei im Glas. Der BLS 4.0 führt keine solchen Fertigprodukte.
- **Folat:** Der BLS führt „FOL Folat-Äquivalent“ in µg/100 g, berechnet als FOL = Nahrungsfolat + 1,7 × synthetische Folsäure. Die Einheit ist also dieselbe wie im Katalog (µg) und entspricht dem DFE-Konzept der USDA. Bei nicht angereicherten Lebensmitteln ist der Wert gleich dem Nahrungsfolat.
- **Ballaststoffe:** Der BLS 4.0 misst nach der neuen Codex-Methode, die niedermolekulare Ballaststoffe wie Fructane mitzählt. Die Werte liegen deshalb systematisch höher: 71 von 112 Vergleichen sind höher, der Median liegt bei +12 %. Extremfall ist Knoblauch mit 28,3 g statt 2,1 g. Das ist eine Methodenfrage, kein Fehler.
- **Kennzeichnung in abgleich.json:** Eine Abweichung gilt als markiert, wenn sie über 25 % liegt und zusätzlich eine Mindestdifferenz überschreitet:
  - kcal 20
  - Eiweiß, Fett und Ballaststoffe je 1 g
  - Vitamin C 3 mg, Calcium 20 mg, Eisen 0,5 mg, Magnesium 10 mg, Zink 0,4 mg
  - Folat 10 µg, B12 0,3 µg

  Das trifft auf 109 Einträge zu, die meisten bei Mikronährstoffen: Folat 52, Eisen 44, Ballaststoffe 37. Wo der Katalog 0 hat und der BLS einen Wert, steht `neu>0`.

## 3. Größte Abweichungen (Top 25, nach Bedeutung, Näherungen ausgeklammert)

Ein Feld „kat → BLS“ zeigt den Katalogwert und den BLS-Wert. „Besser“ heißt: die Quelle, die für deutsche Ware passender ist.

| # | Lebensmittel | Feld: kat → BLS | Einschätzung | Besser |
|---|---|---|---|---|
| 1 | Backpulver | Ca 7364 → 18 mg; Fe 11,3 → 0,9 | US-Backpulver enthält Calciumphosphat, deutsches Natron/Diphosphat | BLS |
| 2 | Salzstangen | Folat 166 → 0 µg | US-Mehl wird mit Folsäure angereichert, in DE nicht | BLS |
| 3 | Kartoffelpüree-Flocken | Vit C 81 → 0; Folat 46 → 0 | USDA-Produkt angereichert. BLS „übernommener Wert“ 0 ist eher zu niedrig | BLS (Tendenz) |
| 4 | Weizenmehl 405 | Folat 29 → 14 µg | US-Anreicherung | BLS |
| 5 | Jagdwurst | kcal 308 → 204; Fett 24,6 → 15,8; Vit C 0,8 → 40 | US-Bologna statt Jagdwurst; Ascorbat als Pökelhilfe | BLS |
| 6 | Salami, Leberwurst | Vit C 0 → 14 bzw. 10,5 mg | Ascorbat-Zusatz in deutscher Wurst | BLS |
| 7 | Frühstücksfleisch | kcal 334 → 198; Fett 30 → 16 | SPAM-Typ gegen deutsche Konserve | BLS |
| 8 | Corned Beef | kcal 250 → 159; Fett 14,9 → 6,4 | deutsches Corned Beef (mit Schwarte, mager) | BLS |
| 9 | Senf | kcal 60 → 111; Fett 3,3 → 7,0 | US-Yellow-Mustard gegen mittelscharfen deutschen Senf | BLS |
| 10 | Cracker | Fett 8,6 → 24,1 g | Saltines gegen typischen deutschen Cracker | BLS |
| 11 | Gemüsebrühe-Pulver | Eiweiß 16,7 → 5,8; Fett 13,9 → 5,8 | deutsche Brühe ist überwiegend Salz/Stärke | BLS |
| 12 | Gewürzgurken | kcal 12 → 33 | deutsche Gurken sind süß-sauer (Zucker im Aufguss) | BLS |
| 13 | Rote Bete (Glas) | kcal 31 → 70 | gesäuert mit Zucker | BLS |
| 14 | Rotkohl (Glas) | kcal 29 → 56 | küchenfertig mit Zucker/Fett/Apfel | BLS |
| 15 | Roggenvollkornmehl | Eiweiß 15,9 → 9,0 g | US-„dark rye“ ist eiweißreicher | BLS |
| 16 | Dinkelmehl | Mg 136 → 28; Fe 4,4 → 1,1 | Katalog = Dinkel-Vollkorn (USDA), BLS = Type 630. Erst klären, welches Produkt gemeint ist (BLS hat auch Dinkel-Vollkornmehl C235000) | Zuordnung klären |
| 17 | Kakaopulver | kcal 228 → 311 | USDA rechnet anders; BLS nutzt die EU-Formel wie auf deutschen Etiketten | BLS |
| 18 | Eier | B12 0,89 → 2,7 µg | BLS nach neuerer Literatur (UK 2013) | BLS |
| 19 | Lachs (Dose) | Ca 283 → 10 mg | mit oder ohne Gräten; hängt vom Produkt ab | Produkt prüfen |
| 20 | Knoblauch | Ca 181 → 14; Folat 3 → 81; Ballaststoffe 2,1 → 28,3 | Ballaststoffe: Codex-Methode (Fructane). Ca und Folat stark gegensätzlich | gemischt |
| 21 | Linsen / weiße Bohnen (trocken) | Folat 479 → 116 bzw. 388 → 130 µg | USDA analysiert, BLS per Formel. Literatur stützt eher hohe Werte | USDA |
| 22 | Mandeln | Ca 268 → 85 mg | BLS-Analysewert weicht stark von der üblichen Literatur (ca. 250–270) ab | USDA |
| 23 | Spinat (TK) | Vit C 5,5 → 58,8 mg | BLS-Rezeptberechnung, für Tiefkühlware unplausibel hoch | USDA |
| 24 | Reis, weiß | Zn 1,09 → 3,03 mg | BLS-Einzelanalyse, ungewöhnlich hoch | USDA |
| 25 | Leberwurst | B12 13,5 → 2,6 µg | BLS „übernommener Wert“ wirkt bei 20–30 % Leberanteil niedrig | unklar |

Kürbiskerne (Folat 58 → 0) und Salzstangen zeigen außerdem: Eine **0 im BLS bei „Formelberechnung“** bedeutet oft, dass Teilwerte fehlen, nicht dass wirklich kein Nährstoff enthalten ist.

## 4. Fazit: Welche Quelle passt für deutsche Ware?

- **Rezepturabhängige und verarbeitete Produkte:** Hier passt der **BLS** klar besser. Das betrifft Wurst, Konserven mit Aufguss, Senf, Brühe, Backpulver, Brot und Gebäck, Mehltypen und alles, was in den USA angereichert wird (Folsäure, Eisen, Vitamin C). Auch die Energiewerte nach EU-Formel passen zu deutschen Etiketten.
- **Mikronährstoffe naturbelassener Grundstoffe:** Bei Hülsenfrüchten, Nüssen und Gemüse ist **USDA SR Legacy** oft solider. Viele BLS-Werte sind dort per Formel berechnet, rezeptberechnet oder übernommen, und einzelne Ausreißer fallen auf (Mandel-Calcium, TK-Spinat Vitamin C, Reis-Zink).
- **Empfehlung:**
  - Makros und Energie bei verarbeiteten Produkten auf BLS umstellen.
  - Mikronährstoffe pro Feld wählen, nach der BLS-Spalte „Datenherkunft“: Analyse oder Literatur bevorzugen, bei Formelberechnung mit 0 oder Rezeptberechnung lieber USDA nehmen.
  - Die Quelle je Wert im Feld q/vq kennzeichnen.
- **Ballaststoffe nicht zwischen den Quellen mischen,** weil die Methoden verschieden sind (siehe Abschnitt 2). Am besten eine Quelle durchgehend nutzen.

## Dateien

- `/home/claude/scratch/bls/abgleich.json`: pro Eintrag i, n, bls_code, bls_name, werte_bls, abweichung (in %), markiert (Liste der Felder) und gegebenenfalls hinweis
- `/home/claude/scratch/bls/roh/`: Rohdaten (ZIP, entpackt, HTML-Seiten)
- `/home/claude/scratch/bls/skripte/`: Umwandlungs- und Abgleichskript (Zuordnungstabelle im Skript)
- `/home/claude/scratch/bls/zwischen/`: BLS als JSON und Namensliste
