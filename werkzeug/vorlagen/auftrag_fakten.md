# Auftrag: belegte Seite zu einem Gespräch (Kompendium „Quellwissen“)

Du lieferst NUR die belegte Seite zu einem Video-Gespräch: was Fachstellen, Studien, Ämter und Gerichte zu den
genannten Themen sagen. Die Nacherzählung des Gesprächs schreibt jemand anderes – du gibst KEINE Aussagen der
Gäste wieder und bewertest sie nicht. Du änderst NICHTS im Repo `/home/claude/quellwissen` (nur lesen).
Alle Dateien in deinen Arbeitsordner. Sprache: Deutsch, schlicht, ohne Wertungswörter
(„Verschwörung“, „umstritten“, „falsch“, „Skandal“, „Mythos“ usw. nicht verwenden – einfach sagen, was die Quelle sagt).

## Abzugeben
1. `fakten.json`:
```json
{"video":{"datum":"TT.MM.JJJJ oder 'JJJJ ❓'","gastgeber":"Name oder ❓","beleg":"[Titel](url) oder ''"},
 "zeilen":[{"k":"<Themen-Schlüssel aus deiner Liste>","thema":"3–8 Wörter",
            "fakt":"2–5 Sätze: was Fachstellen/Studien/Ämter sagen – mit Jahr und Zahl; wo die Lage offen ist: ❓ und sagen, was fehlt",
            "quelle":"[Titel](https://…) · [Titel](https://…)"}],
 "diagramme":[ …fertige Blöcke kurs/balken/vergleich… ],
 "zeitachse":[{"z":"1949","j":1949,"t":"Ereignis in einem Satz","e":true}],
 "quellen":[["Titel","url"]],
 "web":[["Bezeichnung","url"]]}
```
   - Zu JEDEM Themen-Schlüssel deiner Liste genau eine Zeile (wenn nichts belegbar: Zeile mit „❓ nicht belegt gefunden“ und was du gesucht hast).
   - Gleicher Maßstab: Stützt eine Quelle das im Gespräch Gesagte, steht das genauso klar da wie das Gegenteil.
   - Gesundheit nur auf Laien-Ebene; keine Empfehlungen, keine Dosierungen als Rat. Bei Suizid keine Methoden.
   - Personen: zu lebenden, namentlich genannten Personen nur, was Gerichte, Ämter, Parlamentsunterlagen oder große Medien belegen.
   - **Nur geprüfte Links** (per WebSearch gefunden und, wo möglich, per WebFetch gelesen). Amtliche/primäre Quellen bevorzugen
     (RKI, PEI, STIKO, EMA, BfR, BfS, EFSA, WHO, UKHSA, CDC, FDA, Destatis, ECDC, Cochrane, Originalstudien, Gerichte, Bundestag).
     Zahlen nie schätzen.
   - Diagramme: Formate exakt wie die Blöcke `kurs`, `balken`, `vergleich` im Reiter `schoeningabgleich` des Autors `realtalk`
     (ansehen mit: `cd /home/claude/quellwissen && python3 -c "import sys;sys.path.insert(0,'/home/claude/scratch');from q import *;r=next(r for r in A('realtalk')['reiter'] if r['id']=='schoeningabgleich');[print(json.dumps(b,ensure_ascii=False)[:1500]) for b in r['bloecke'] if b['typ'] in('kurs','balken','vergleich')]"`).
     `kurs`: id „<K>-…“, nur echte Zeitreihen mit mind. 6 Stützpunkten aus EINER geprüften Quelle, Punkte aufsteigend, `quelle` mit Stand,
     `hinweis` „Bezug zum Gespräch [h:mm]: …“ (sachlich, eine Zeile). `vergleich`: nur wo die im Gespräch genannte Zahl (steht in deiner
     Themenliste) und der Datenwert dieselbe Größe messen. Ziel: 4–6 Diagramme.
2. `pruefstand.json` nach `/home/claude/quellwissen/werkzeug/vorlagen/auftrag_pruefstand.md` (ganz lesen), Format:
   `{"eintraege":[{"autor":"<AUTOR>","reiter":"<K>abgleich","staat":[[Punkt, Was belegt ist, "[Titel](url)"]],"datenluecken":[[…]],"fragen":["…"],"autor_zeilen":[],"fazit":"…"}]}`
   – 5–8 `staat`-Zeilen zu Themen dieses Gesprächs (belegte Versäumnisse, Korrekturen, geänderte Empfehlungen, spät Veröffentlichtes
   auf Seiten von Staat, Behörden, Fachgesellschaften, Herstellern unter Aufsicht; Entlastendes aus derselben Quelle im selben Satz),
   0–3 `datenluecken`, 3–5 `fragen` (echte Fragen, ohne Motive zu unterstellen), `autor_zeilen` leer lassen, `fazit` 2–4 Sätze ohne Urteil.
3. `z_<K>.js` – zwei neutrale Skizzen (Themen stehen im Einzelauftrag) im Format aus
   `/home/claude/quellwissen/werkzeug/vorlagen/auftrag_folge.md`, Abschnitt „Zwei Zeichnungen“ (nur diesen Abschnitt lesen);
   Vorbild: `/home/claude/quellwissen/werkzeug/gen/realtalk/z_schoening.js`. Funktionsnamen `<K>_<name>`. Mit `node` und Ersatz-Helfern
   testen (läuft, gültiges SVG, nichts überlappt oder ist abgeschnitten; Beschriftungen kurz). Nur belegte Zahlen in der Daten-Skizze.
4. `notizen.md` – kurz: was offen blieb.

## Selbstprüfung am Ende
JSON lädt; jede Zeile hat k/thema/fakt/quelle mit mindestens einem Markdown-Link (außer ❓-Zeilen); kurs-Punkte aufsteigend;
Zeichnungen laufen. Richtwert: 25–40 gezielte Suchen/Abrufe, parallel wo möglich.

## Rückmeldung (kurz, keine Inhalte)
Veröffentlichungsdatum/Gastgeber (gefunden oder ❓), Zahl der Zeilen/Diagramme/Prüfstand-Zeilen, welche Schlüssel offen blieben.
