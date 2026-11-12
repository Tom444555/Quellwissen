# Auftrag: eine Podcast-Folge für „Quellwissen“ auswerten (Sammeleintrag A-08 {ungeskriptet} by Ben)

Du wertest GENAU EIN Transkript aus und lieferst fertige Daten-Dateien. Du änderst NICHTS im Repo
`/home/claude/quellwissen` (nur lesen). Alle deine Dateien kommen in deinen Arbeitsordner
`/home/claude/scratch/<ordner>/` (wird dir genannt). Sprache: Deutsch.

## Zuerst lesen (kurz, gezielt)
- `/home/claude/quellwissen/werkzeug/HANDBUCH.md` Zeilen 110–145 (Videos auswerten, Zeichnungen) – mit `sed -n`.
- Vorbild: `/home/claude/scratch/a08.json` (bestehender Eintrag, eingerückt). Sieh dir per kleinem Python-Skript
  die Reiter `gudwis`, `gudwisab` (2–3 Abschnitte), `gudwiszeit`, `gudwisabgleich` an (nicht alles ausgeben).
- Zeichnungs-Vorlagen: `/home/claude/quellwissen/werkzeug/z_partei.js`, `z_stat.js` (nur Anfang).
- Die Quelle `quelle/gruenwissen.html` NIE ganz lesen oder unbegrenzt greppen.

## Transkript lesen
Datei komplett lesen (in Portionen mit Read offset/limit). Zeilen haben `[hh:mm:ss] Text`
(automatische Untertitel, also Hörfehler möglich → Namen/Begriffe mit gesundem Zweifel, Unklares mit ❓ „[unklar]“).
Arbeite in drei Dritteln und schreibe je Drittel Notizen nach `notizen.md` (Abschnitte mit Zeiten, Personen, Orte,
Begriffe, Zahlen, Zeitleiste, Spannungen/Gegenfragen des Gastgebers Ben, Abgleich-Kandidaten), bevor du den Generator schreibst.

## Regeln für den Inhalt (wichtig)
- **Neutral.** Gast, Gastgeber, Quellen nicht abwerten: keine Etiketten wie „Verschwörungstheorie“, „umstritten“,
  „falsch“, „polemisch“, „Interessenkonflikt“. Wörter, die ein Sprecher selbst benutzt, dürfen als Zitat stehen.
  Abgleich = Tabelle nebeneinander: „Aussage im Gespräch | Gängige Darstellung (Mainstream) / Daten 📚 | Quelle“.
  „[seine Sicht]“/„[ihre Sicht]“ statt „[Meinung]“. Die Bewertung bleibt dem Leser.
- Was im Video gesagt wird, steht ohne Zeichen; eigene Ergänzungen 📚 bzw. „[Ergänzung]“; Unklares ❓.
- **Zitate kurz:** höchstens ~15 Wörter je Zitat, höchstens 2 Zitate je Abschnitt; sonst in eigenen Worten wiedergeben.
- **Gesundheit ehrlich:** bei Gesundheitsaussagen im Abgleich Studienlage (Leitlinie, Cochrane, RKI, DGE, BfR, WHO),
  Warnzeichen für den Arztbesuch; nichts erfinden. Keine Dosier-/Konsumanleitungen. Bei Suizid keine Methoden,
  nur kurzer Hilfehinweis (Telefonseelsorge 0800 111 0 111).
- **Quellen als geprüfte Links:** jede Quelle im Abgleich und unter Quellen anklickbar und von dir geprüft
  (WebSearch/WebFetch; amtliche/primäre Quellen bevorzugen: Destatis, Bundestag, RKI, BfR, DGE, Eurostat, OWID,
  SIPRI, UN, Gesetzestexte, Originalstudien). Was du nicht belegen konntest: als ❓ offen lassen, nicht raten.
  Wenige, gezielte Suchen (Richtwert 12–20 Suchen/Abrufe).
- Veröffentlichungsdatum des Videos per WebSearch ermitteln (sonst „2026“ + ❓).
- Querverweise ins Kompendium, wo es wirklich passt: `{{a:kowallik|Fabian Kowallik (A-06)}}`, `{{a:ganser|Daniele Ganser}}`,
  `{{a:krall|Markus Krall}}`, `{{a:nehls|Michael Nehls}}`, `{{a:storl|Wolf-Dieter Storl}}`, `{{w:kriege|Kriege}}`, `{{w:geld|Geld}}`,
  `{{w:demenz|Demenz}}`, `{{w:suizid|…}}`, `{{w:deutschland|Deutschland in Zahlen}}`, `{{w:politik|…}}`, `{{w:dgeschichte|…}}`,
  `{{w:grundgesetz|…}}`. Storl/Nehls nur, wo Belegtes passt (Hinweis-Block `{"typ":"hinweis","storl":true,"text":"**Storl-Bezug:** …"}`).
- Inline-Formate: `**fett**`, `[Titel](https://…)`, interne Links wie oben. In `baum`-Knoten KEINE `{{…}}`-Links.
- Fundstellen immer als `[h:mm]` oder `[h:mm–h:mm]` (Halbgeviertstrich –). Die App macht daraus Sprungmarken ins Video.

## Neuer Aufbau je Folge: vier Reiter (Kürzel `K` wird dir genannt; Gast-Präfix `G` = Nachname)
Reiter-Titel beginnen IMMER mit „G: “.

### 1. Reiter `K` – Titel „G: Überblick“
Bausteine in dieser Reihenfolge:
1. `{"typ":"folge","k":K,"titel":<Originaltitel>,"gast":<Name>,"rolle":<Beruf/Rolle kurz>,"kanal":"{ungeskriptet} by Ben",
   "datum":"TT.MM.JJJJ","dauer":"2 Std. 35 Min.","url":"https://www.youtube.com/watch?v=…","thema":<ein Satz>,
   "kacheln":[["41","Abschnitte"],["10","Kernaussagen"],["22","Abgleich-Punkte"],["6","Verläufe & Diagramme"],["38","Quellen"]]}`
2. `{"typ":"hinweis","text":"Auswertung nach dem Transkript (automatische Untertitel): Gesagtes ohne Zeichen, Ergänzungen 📚, Unklares ❓. Fundstellen [Stunde:Minute] springen ins Video. Die Bewertung bleibt dem Leser."}`
3. `abschnitt` „⚡ In Kürze“ – `liste` mit 6–8 Sätzen (das Gespräch in einer Minute).
4. `text` „🎯 **Kernaussagen** – die zehn wichtigsten Thesen des Gesprächs:“ + `tabelle` kopf
   `["#","Aussage","Begründung im Gespräch","Fundstelle","Gewicht"]` (10 Zeilen, Gewicht ★–★★★ = Raum im Gespräch).
5. `baum` „🌳 Themenbaum des Gesprächs“: `{"typ":"baum","titel":…,"wurzel":<Videotitel>,"unter":"Gast · Kanal · Datum · Dauer",
   "knoten":[{"t":"🧬 Ast","k":[{"t":"Unterpunkt [0:19]"},…]},…]}` – 6–9 Äste mit Emoji, je 3–6 Unterpunkte mit Fundstelle.
6. Zwei `illu`-Bausteine: `{"typ":"illu","id":"<K>_<name>","titel":"Skizze: … (schematisch / Darstellung laut <Gast> / belegte Daten)"}`.
7. `tabelle` Steckbrief: kopf `["🧭 Steckbrief",""]`, Zeilen: Thema in einem Satz, Titel, Format (inkl. Werbeblöcke),
   Sprecher, Dauer, Datum, Grundton, Hinweis. Feld `"schmal":true`.

### 2. Reiter `K+"ab"` – Titel „G: Gespräch im Detail“
1. `text`: ein Satz Einleitung (Anzahl Abschnitte, Lesehilfe 💬 Zitat, 📌 Aussage, 🔗 Bezug, 📚 Ergänzung, ❓ unklar).
2. `{"typ":"gespraech","titel":"🧭 Gesprächsverlauf – wann worüber gesprochen wird","dauer":"2:35",
   "themen":[{"k":"a","n":"Krieg & Frieden"},…  (5–8 Themen, kurze Namen)],
   "teile":[{"von":"0:00","bis":"0:03","t":"Teaser und Vorstellung","th":"a"},…]}` – EIN Teil je Abschnitt, lückenlos,
   gleiche Reihenfolge und gleiche Zeiten wie die Abschnitte. Werbeblöcke bekommen ein eigenes Thema „Werbung/Organisatorisches“.
3. Je Abschnitt (Richtwert: alle 4–6 Minuten ein Abschnitt, also 30–50; die 4½-Stunden-Folge 50–60) ein Baustein
   `{"typ":"abschnitt","titel":"🧬 Titel [0:19–0:26]","th":"a","liste":[ "<Zusammenfassung 2–4 Sätze>",
   "💬 „kurzes Zitat“ (Sprecher) [0:21]", "📌 Aussage/Zahl/Beispiel … [seine Sicht]", "🔗 Bezug …", "📚 Ergänzung …" ]}`.
   Titel beginnt mit Emoji und endet mit der Zeitspanne in eckigen Klammern. Detailliert und vollständig –
   auch Gegenfragen und Widerspruch von Ben festhalten („Ben: …“).

### 3. Reiter `K+"zeit"` – Titel „G: Zeitachse & Verzeichnisse“
1. `{"typ":"zeitachse","titel":"📅 Zeitachse – Ereignisse, die im Gespräch vorkommen","eintraege":[
   {"z":"1914–1918","j":1914,"t":"Erster Weltkrieg …","f":"[0:42]","e":false}, …]}` – chronologisch sortiert;
   `j` = Jahreszahl als Zahl (v. Chr. negativ; unbekannt: weglassen), `e:true` = von dir ergänztes Datum (📚),
   `f` = Fundstelle. 25–50 Einträge. Auch Lebensstationen des Gastes.
2. `tabelle` `["👤 Person","Wer / was","Rolle im Gespräch","Fundstelle"]`
3. `tabelle` `["🗺️ Ort","Rolle","Fundstelle"]`
4. `tabelle` `["📖 Begriff","Erklärung","Fundstelle"]`
5. `tabelle` `["📊 Zahl im Gespräch","Angabe","Fundstelle"]`

### 4. Reiter `K+"abgleich"` – Titel „G: Abgleich & Daten“
1. `text`: „Neutraler Abgleich: links die Aussage im Gespräch, rechts die gängige Darstellung bzw. Daten mit Quelle. Die Bewertung bleibt dem Leser.“
2. `tabelle` kopf `["Aussage im Gespräch","Gängige Darstellung (Mainstream) / Daten 📚","Quelle"]`, `"stapel":true`,
   18–28 Zeilen, Quelle jeweils als `[Titel](url)`, Aussage mit Fundstelle.
3. **Mehr Auswertungen und Diagramme als bisher** – Ziel 6–9 Diagramme zu den besprochenen Themen, alle mit amtlicher/primärer Quelle + Stand:
   - `kurs` (Verlauf über Jahre im Börsenkurs-Stil, nur echte Zeitreihen, mind. 6 Stützpunkte; Felder wie im Vorbild
     `gudwisabgleich`: id „<K>-…“, titel „📈 …“, reihen[{name,kurz,einheit,dez,hoeherGut,punkte[[jahr,wert]]}], hoeherGut, vergleich,
     quelle (mit Stand), hinweis „Bezug zum Gespräch [h:mm]: …“). Ziel 3–5 Stück. Werte NUR aus geprüften Quellen, keine Schätzwerte.
   - `{"typ":"balken","titel":"📊 …","einheit":"%","dez":1,"zeilen":[["Label",12.3],…],"quelle":"[Titel](url), Stand …","hinweis":"Bezug zum Gespräch [h:mm]: …"}`
     – Vergleich von Kategorien/Ländern/Gruppen (keine Zeitreihe). Ziel 1–3 Stück.
   - `{"typ":"vergleich","titel":"⚖️ Zahlen im Gespräch und Daten nebeneinander","la":"Im Gespräch genannt","lb":"Daten laut Quelle",
     "zeilen":[{"n":"Was","a":80,"b":62.5,"einheit":"%","f":"[0:33]","q":"[Quelle](url)"},…]}` – nur wo Gast-Zahl und Datenwert
     dieselbe Größe messen (3–8 Zeilen). Neutral, ohne Wertung.
4. `abschnitt` „🧩 Spannungen im Gespräch“ (Gegenfragen/Widerspruch des Gastgebers, offene Enden), „💡 Was man mitnehmen kann“,
   „❓ Offen“, „🔎 Weiter recherchieren“ (je `liste`).

## Zwei Zeichnungen (`z_<K>.js`)
Datei mit genau zwei Funktionen im Format (4 Leerzeichen Einrückung vor dem Namen, endet mit `},`):
```
    <K>_name(){ seed=4101; let g=''; … return {vb:'0 0 760 300', breit:true, leg:[], svg:g}; },
```
Verfügbare Helfer in der App: `lg(c0,c1,winkel)`, `shade(farbe,±bruch)`, `rnd()`, `R()`. Text mit
`style="fill:var(--ink);font:700 11px var(--label);text-anchor:middle"`; Farben für Text `var(--ink)`, `var(--muted)`, Linien `var(--line)`.
Stil: Feldbuch/Buntstift, warme natürliche Hex-Farben, klare Beschriftung, nichts überlappend oder abgeschnitten
(genug Rand, kurze Texte, lange Texte umbrechen). Gern kleine Einblend-Animation (`<animate>`), wie in `z_partei.js`.
Inhalt: eine erklärende Skizze zum Kerngedanken des Gastes (als „schematisch“/„Darstellung laut <Gast>“ betitelt)
und eine zu belegten Daten oder Abläufen. Seeds: nimm die dir genannte Seed-Basis.
Teste mit `node -e` und Ersatz-Helfern, dass beide Funktionen laufen und gültiges SVG liefern
(z. B. Ergebnis in eine .svg schreiben; wenn möglich mit einem Blick prüfen).

## Abzugeben (in deinem Arbeitsordner)
- `notizen.md`
- `gen.py` – erzeugt `folge.json`:
  ```json
  {"k":K,"gast":"…","reiter":[<4 Reiter-Objekte {"id":…,"titel":…,"bloecke":[…]}>],
   "folgen_zeile":["TT.MM.JJJJ","Gast (Rolle)","Originaltitel","Themen kurz","{{a:ungeskriptet-K|hier: G}}","[ansehen](url)"],
   "baum_ast":{"gruppe":"🧬 Passende Themengruppe","t":"👤 Gast – Stichworte"},
   "neu":{"d":"2026-11-11","t":"{ungeskriptet} – Gast","k":"Ein Satz: Thema – n Abschnitte, Abgleich mit Quellen, n Diagramme.","h":"#a-ungeskriptet-K","art":"Podcast"},
   "quellen":[["Video: Originaltitel – {ungeskriptet} by Ben (YouTube)","url"],["Titel","url"],…],
   "web":[["Gast – Webseite/Kanal","url"],…]}
  ```
  Du darfst `sys.path.insert(0,'/home/claude/quellwissen/werkzeug'); from bausteine import *` nutzen oder die dicts direkt schreiben.
- `z_<K>.js`
- Am Ende selbst prüfen: `folge.json` lädt als JSON; Reiter-Ids/Titel stimmen; jede `teile`-Zeile hat einen Abschnitt mit gleicher
  Zeitspanne; alle `th` kommen in `themen` vor; `kurs`-Punkte aufsteigend nach Jahr; kein `{{…}}` in Baum-Knoten; die zwei illu-ids = Funktionsnamen.

## Rückmeldung an mich (kurz!)
Nur: Gastname + Kürzel, Veröffentlichungsdatum, Zahl der Abschnitte/Abgleich-Zeilen/Diagramme, was offen blieb (❓),
was du nicht belegen konntest. Keine Inhalte, keine Rohdaten zurückgeben.
