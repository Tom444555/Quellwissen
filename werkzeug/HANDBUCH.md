# Quellwissen – Handbuch für Claude

Nachschlagewerk zum Skill `quellwissen`. **Nie ganz lesen** – nur den gerade nötigen Abschnitt:
`grep -n '^## ' werkzeug/HANDBUCH.md`, dann `sed -n 'START,ENDEp'`.

## Struktur und Werkzeuge
- `quelle/gruenwissen.html` – **die Quelle** (nur diese bearbeiten). Sie ist zugleich die Artefakt-Datei.
- `index.html` – gebaut von `werkzeug/build.sh`. Nie direkt bearbeiten.
- `manifest.webmanifest`, `sw.js`, Icons, `fotos/`, `lib/` (three.js offline).
- `werkzeug/`:
  - `bausteine.py` – Python-Helfer für Kapiteldaten
  - `einbauen.py <bereich> <json> [nach_id]` – Eintrag einsetzen/ersetzen (Bereiche: pflanzen, selbstversorgung, getreide, biochemie, rezepte, autoren, welt)
  - `welt.js` – Weltkarten-Modul; `welt_einbauen.py` bettet Daten (`welt_daten/welt_basis.json`, `relief.jpg`) und Modul ein
  - `minis_bauen.js` – PNG-Vorschaubilder für die Startseite (`#minibilder`), macht sie auf Tablets schnell
  - `zeichnung_einbauen.py datei.js` – Zeichenfunktionen einsetzen
  - `pruefen.py` – Links, Zeichnungs-IDs und JS-Syntax prüfen
  - `alles.sh` – Realismus-Modul, plus_einbauen, welt_einbauen, minis_bauen (`NODE_PATH=$(npm root -g)`), pruefen, build (muss „OK“ melden)
  - `foto.js` – Screenshot: `node werkzeug/foto.js "#a-ganser-video" bild.png` (schreibt Zeichnungs-Ausschnitte `bild_z0.png`)
  - Karten-Screenshot: kleines Playwright-Skript, das `#welt` mit `window.QW_STANDBILD=true` öffnet und z. B. `QWWELT.grund('de_su')`, `QWWELT.bl('SN')`, `QWWELT.flieg(lon,lat,zoom)` ausführt
  - `foto3d.js` – 3D-Standbild
- Eigene Generator-Skripte (`gen_*.py`) und Zwischendateien gehören in den Scratchpad, nicht ins Repo.

## Startseite: Gruppen in Teil S

In `uebersicht()` hat Teil S feste Gruppen (`SG`). Neues S-Kapitel dort eintragen, sonst landet es unter „Weitere“. Autoren und Teil W erscheinen automatisch.
- Garten & Boden: huegelbeet, boden, mischkultur, mulch
- Anbau: aussaat, tabak, hanf
- Sammeln & Küche: knospen, blueten, kueche, hefe, einfrieren, wildgruen
- Hausapotheke: tinkturen, faktencheck
- Haus & Hof: heizen, waschmittel
- Pilze: pilze
- Ernährung & Körper: energie, fette, proteine, kohlenhydrate, abnehmen, naehrwerte, mikronaehrstoffe

## Weitere Fehlerquellen

- Auch `...]))` am Ende von `tab(...)` innerhalb einer Liste prüfen, bevor das Skript läuft.
- Rezepte im Text als Klartext nennen (kein `{{r:…}}`).
- Ids von W-Kapiteln z. B. `dgeschichte`, nicht `deutschland-politik`.

## Datenmodell

Daten stehen in `<script type="application/json" id="daten">` mit den Arrays `pflanzen` (P), `selbstversorgung` (S), `getreide` (G), `biochemie` (B), `rezepte` (R), `autoren` (A) und `welt` (W). Zurückschreiben:
```python
s=json.dumps(d,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
open(Q,'w').write(h[:m.start(2)]+s+h[m.end(2):])   # m = re.search(r'(<script type="application/json" id="daten">)(.*?)(</script>)',h,re.S)
```

**Pflanze** (`id` `p01`…, `nr` `P-01`):
- Felder: `name`, `botan`, `volksnamen[]`, `illu`, `fotos[]`, `kurz`, `steckbrief[[k,v]]`, `reiter[]`.
- Standard-Reiter: botanik (mit `standort`-Block), inhaltsstoffe, wirkung, heilkunde, rezepte, selbstversorgung, sicherheit, quellen. Dazu nach Bedarf Tradition & Storl.

**Kapitel S/G** (`id` frei, `nr` `S-08`…):
- Felder: `titel`, `illu`, `fotos[]`, `text`, `stichworte[]`, `pflanzen[]` (Links wie `"p03#rezepte"`), `kurz`, `steckbrief`, `reiter[]`.
- Einträge ohne `reiter` sind kurze Verfahren und erscheinen nur in der Übersicht.

**Welt** (`w`, `nr` `W-01`…): wie Kapitel S. Route `#w-<id>-<reiter>`, Link `{{w:id|Text}}`. **Ids ohne Bindestrich** (sonst bricht die Route). Titel von Teil W steht im Objekt mit `W:['Teil W',…]`; kein `&` im Titel (wird doppelt maskiert).

**Biochemie** (`b`): `id`, `titel`, `text`, `stichworte`, `pflanzen`, optional `reiter`.

**Rezepte** (`r`, `nr` `R-01`…): wie Kapitel, mit Zutaten, Schritten (Tabelle), Bildleiste (`rezept_leiste`) und Tipps. Kleinere Rezepte können auch als `karten("rezept",[rez(…)])` in einem Kapitel-Reiter stehen (z. B. S-17 Pilze).

**Autoren** (`a`, `nr` `A-01`…): Felder `id`, `nr`, `name`, `botan` (Beruf), `volksnamen[]`, `kurz`, `steckbrief[[k,v]]`, `reiter[]`.
- Bestand: A-01 nehls, A-02 storl, A-03 krall, A-04 ganser, A-05 goethe, A-06 kowallik, A-07 wolff (Christian Wolf, More Nutrition), A-08 ungeskriptet (Podcast-Sammeleintrag: Reiter kanal, folgen, dann je Folge vier Reiter mit Gast-Kürzel, z. B. gudwis, gudwisab, gudwiszeit, gudwisabgleich; Generator-Vorlage gen_ungeskriptet.py; Transkripte holt Tom mit transkript.py in a-Shell) (mit Werkverzeichnis, Politik & Weltbild, Zitate, Reisen auf der Karte).
- **Einheitliche Reiter** (jeder Autor bekommt alle, die es hergibt):
  1. `person` – Werdegang, Kurz zusammengefasst
  2. `buecher` – `karten` mit `art:"buch"` (id, titel, kat "alle", jahr, verlag, kurz, zutaten = Eckdaten, schritte = Kernpunkte); Jahre der Erstausgabe als [Ergänzung]
  3. `kernideen` – 5–6 nummerierte Abschnitte
  4. `praxis` – Tabelle „Empfehlung | So beschreibt X es | Fundstelle“ (keine W/T/A-Kürzel, die werten), optional Umsetzungsschritte
  5. Video-Reiter (siehe unten)
  6. `einordnung` mit Titel **„Abgleich“** bzw. `pruefung` „Video: Abgleich & offene Fragen“
  7. `web` – „Web & Videos“: Tabelle 🌐 Kanal | Link (Webseite, YouTube, Podcast, Telegram …) und Tabelle ▶️ Video | Art/Kanal | [ansehen](url). Nur geprüfte Links (Webseite per WebFetch, Videos per WebSearch mit `allowed_domains:["youtube.com"]`).
  8. `quellen` – `q([titel,url],…)` plus Textzeile zur Grundlage

**Blocktypen** in `reiter[].bloecke[]`:

| typ | Felder |
|---|---|
| text | text |
| hinweis | text, optional storl:true |
| abschnitt | titel, liste[] oder nummern[] |
| tabelle | kopf[], zeilen[[...]] |
| karten | art (anwendung/rezept/buch), filter[[k,label]], eintraege[] (id, titel, kat, beleg W/T/A, teil, kurz, zutaten[], schritte[], hinweis, tipp; rezept: menge, zeit; buch: jahr, verlag) |
| quellen | eintraege[[titel,url]] – Einträge ohne URL werden als Klartext gezeigt |
| illu | id (Zeichnungsname), titel |
| standort | licht, wasser, naehrstoffe (1–5), ph, boden, ellenberg, hinweis |
| baum | titel, wurzel, unter, knoten[{t, h?, i?, k:[…]}] – Ast-Titel dürfen mit Emoji beginnen (Abzeichen nimmt `Array.from(t)[0]`, Emoji wird im Label entfernt) |
| schichten, nachbarcheck | Spezialblöcke |
| naehrdiagramm | titel, start (k/e/f/s/c/b/ed/mix oder Mikro ca/mg/ka/fe/zn/jo/va/vd/ve/vk/vc/fo/b12), daten[] (nur in S-25 Reiter `naehrliste`) oder quelle:"naehrliste" |
| karten art:"naehrstoff" | wie anwendung, zusätzlich ref (Referenzwert in der Kopfzeile); Labels „Auf einen Blick“/„Im Detail“ |
| kurs | Verlauf im Börsenkurs-Stil (nur echte Zeitreihen über Jahre, keine Kategorienvergleiche): id (Speicherschlüssel), titel, reihen[{name, kurz?, einheit, dez?, farbe?, hoeherGut? (true/false/null), punkte[[jahr,wert],…]}], hoeherGut (Standard für alle Reihen; false = Anstieg rot), zeitraum[] (Jahre, sonst automatisch z. B. 10/25/50 + Max), schnitt (gleitender Ø in Jahren, Knopf „Ø n J.“), vergleich:false (schaltet „Vergleichen“ = Index Start = 100 ab), quelle, hinweis. Lücken in den Jahren werden gestrichelt. Beispiel: W-04 `verlauf` |
| energierechner | titel (Eingaben in localStorage `qw-energie`, Tagesziel für naehrrechner) |
| naehrrechner | titel, quelle:"naehrliste", vorlagen[{n,z:[[name,g]]}] (gespeichert in `qw-mahlzeiten`) |

**bausteine.py:** `tab(kopf,*zeilen)`, `txt`, `hin`, `abs_(titel, liste=/nummern=)`, `illu`, `std(...)`, `karten`, `anw(id,titel,kat,beleg,teil,kurz,zut,schr,hinweis,tipp)`, `rez(id,titel,kat,menge,zeit,kurz,zut,schr,tipp,hinweis)`, `q(...)`, `R(id,titel,*bloecke)`. Für Themenbäume im Generator: `baum(t,w,u,kn)` und `n(t,*k)` selbst definieren (Vorlage `gen_goethe.py`).

**Belegstufen:** W = wissenschaftlich/amtlich, T = traditionell, A = alternative Quelle (nur bei Pflanzen-Anwendungen; bei Autoren-Aussagen weglassen).

**Inline-Text:** `**fett**`, Markdown-Links `[Titel](url)`, interne Links `{{p:p03|Löwenzahn}}`, `{{p:p02#rezepte-pesto|Pesto}}`, `{{s:…}}`, `{{b:…}}`, `{{g:…}}`, `{{w:…}}`, `{{a:krall-video|…}}`.

**Hash-Routen:** `#p05`, `#p05-rezepte`, `#s-hanf-licht`, `#g-brot`, `#b-lithium-nehls`, `#r-<id>`, `#a-<id>-<reiter>`, `#w-<id>-<reiter>`, `#teil-S`, `#welt`, `#welt-<ebene>` (z. B. `#welt-de_su`, `#welt-staat`, `#welt-goethe`).

**Bestand (Stand 26.10.2026 – aktuellen Stand immer per Python aus dem Daten-JSON ermitteln):**
- Pflanzen p01–p24 (u. a. Brennnessel … Hanf, p23 Aloe vera, p24 Rainfarn).
- Selbstversorgung S-01–S-17: huegelbeet, boden, mischkultur, knospen, tabak, hanf, blueten, tinkturen, aussaat, kueche, einfrieren, wildgruen, mulch, faktencheck, heizen (Obstbaumholz), hefe, pilze. Verfahren: jauche, auszug, trocknen, einfrieren, samen.
- Getreide: brot, mais, bier. Rezepte R-01–R-15 (… Aufstriche, R-15 Baumstriezel).
- Biochemie: rund 55 Stoffe (u. a. lithium, lignin, gaerung, pilzgifte).
- Autoren A-01–A-05.
- Welt W-01–W-11: geld, erfindungen, kriege (mit Sicht Ganser), suizid, demenz, kriminalitaet, deutschland (Deutschland in Zahlen), politik (Staatsformen), dgeschichte (politische Geschichte & System), grundgesetz, partei (Partei gründen).

## Videos und Transkripte auswerten

- **Ohne Transkript nichts auswerten.** YouTube liefert in der Sandbox weder Transkript noch Untertitel (WebFetch nur Titel, Kanal, Datum, Kapitel; pip/YouTube gesperrt). Eckdaten holen, dann den Nutzer um das Transkript als Datei bitten (YouTube-App: „…“ → „Transkript anzeigen“).
- **Transkript verdichten** (spart Lesevolumen): Zeilen `[hh:mm:ss] Text` in 3-Minuten-Blöcke zusammenfassen und die Datei komplett lesen, bevor geschrieben wird:
  ```python
  for l in L: m=re.match(r'\[(\d+):(\d+):(\d+)\] ?(.*)',l); s=int(m[1])*3600+int(m[2])*60+int(m[3]); B.setdefault(s//180,[]).append(m[4])
  ```
- **Aufbau beim Autor** (Vorbild `gen_krall.py` / `gen_ganser.py`):
  - Reiter `video` „Video: <Originaltitel>“: Einleitungstext (Titel, Kanal, Datum, Dauer, Kennzeichnung) + A 🧭 Steckbrief (Thema in einem Satz, Titel, Format inkl. Werbeblöcke, Sprecher, Dauer, Datum, Kapitel, Grundton, Hinweis) + B 🌳 `baum` (Wurzel = Videotitel, `unter` = Gast · Kanal · Datum · Dauer, Äste mit Emoji und Fundstellen) + Piktogramm-Legende + C 🎯 Kernaussagen (# | Aussage | Begründung | Fundstelle | ★–★★★) + I 🗂️ Ein-Seiten-Zusammenfassung.
  - Reiter `abschnitte` „Video: Abschnitte“: D je Abschnitt `ab(titel, zusammenfassung, zitate, aussagen, bezug, ergaenzungen)` → Zusammenfassung, 💬 Zitate, 📌 Fakt/Behauptung/Meinung/Beispiel, 🔗 Bezüge, 📚 Ergänzungen. Fundstellen `[h:mm]`.
  - Reiter `zeitleiste` „Video: Zeitleiste & Verzeichnisse“: E Zeitleiste (📚 für ergänzte Daten), F1 👤 Personen, F2 🗺️ Orte, F3 📖 Begriffe – jeweils mit Fundstelle.
  - Reiter `pruefung` „Video: Abgleich & offene Fragen“: neutraler Satz + Tabelle „Aussage | Gängige Darstellung (Mainstream) / Daten 📚 | Quelle“, 🧩 Spannungen im Gespräch (Gegenfragen des Gastgebers), 💡 Was man mitnehmen kann, ❓ Offen, 🔎 Weiter recherchieren.
  - Quellen: Video-Link mit Originaltitel und Kanal zuerst.
- Bei Autoren ohne Zeitstempel (Nehls, Storl) diese Teile als Abschnitte im Reiter `videos` (Steckbrief, Kernaussagen, Zusammenfassung, Zeitleiste, Verzeichnis, Offen) und vermerken, dass Fundstellen fehlen.
- Neuer Autor: Generator schreibt `a_<id>.json`, dann `python3 werkzeug/einbauen.py autoren a_<id>.json <vorheriger_autor>`.

## Zeichnungen (Modul `IL`, Objekt `Z`)

Jede Zeichnung ist eine Funktion `name(){ seed=…; let g=''; …; return {vb:'0 0 B H', breit:true, leg:[], svg:g}; },`. Sie wird über `illu`-Blöcke oder das `illu`-Feld eines Kapitels eingebunden.

**Helfer:**
- `blatt(x,y,len,breit,winkel,{teeth,heart,fill,deep})`, `stiel(pfad,breite,farbe)`
- `korb`, `stern`, `jblute`, `fieder`, `hblatt`, `kolben`, `pfahl`, `rhizom`, `trieb`, `haare`, `fasern`, `erde`
- `rot(punkte,cx,cy,winkel)`, `R()` (runden), `rnd()` (mit `seed` gesetzt)
- `mk(x,y,n)` (Nummernkreis), `lbl`/`lbl2`/`wrap` (Beschriftung)
- `vign(i,titel,inner)` (150 px breite Felder mit Untertitel), `rahmen`
- **Rezept-Bildleiste:** `rezept_leiste([[icon,titel,opts]])` mit Icons schuessel, kneten, warm, kalt, topf, kasten, ofen (opts: inhalt topf/kasten, kalt, t), mixer, kartoffel, einweichen, pinsel, teilen (n, t), kerne, gitter.
- **Kalender:** `ak_tafel(rows, titel, sd)` – Monatsbalken mit Marker für den aktuellen Monat (Aussaatkalender).
- Vor dem Einsetzen testen: `node -e` mit Ersatz-Helfern (`lg`, `shade`, `rnd`) die Funktionen aufrufen und `vb` ausgeben.

**Stil:**
- `lg(c0,c1,winkel)` und `vg(farbe)` liefern Verlaufs-URLs; `shade(farbe,±x)` hellt auf oder dunkelt ab – Werte als Bruch (z. B. `-0.3`), nicht ganzzahlig.
- Der Nachbearbeiter `stil()` macht aus jeder Hex-Füllung einen Verlauf und ergänzt dunkle Konturen. Große Figuren bekommen einen Bleistift-Filter. Darum einfach mit natürlichen Hex-Farben zeichnen.

Beschriftungen bekommen genug linken Rand und kurze Texte; nach dem Screenshot abgeschnittene oder überlappende Beschriftungen durch Verschieben/Kürzen beheben (z. B. Beschriftungen abwechselnd oben/unten in mehreren Höhen). Texte mit `paint-order:stroke;stroke:var(--surface)` lesbar halten. Farben für Text: `var(--ink)`, `var(--muted)`, `var(--line)`.

## Statistik-Diagramme

Balken- und Säulendiagramme als Zeichnungsfunktionen (Vorlage `werkzeug/z_stat.js`, `z_stat2.js`): horizontale Länder-Balken mit Bundesdurchschnitt als gestrichelte Linie (hinter den Balken), gestapelte Säulen (Männer/Frauen), runde Achsenschritte (`[1,1.5,2,2.5,3,4,5,6,7.5,8,10]`), Achse bei Bedarf nicht ab 0 (`b0`), Balken wachsen per `<animate>`. Weitere Vorlagen: `z_politik.js` (Zeitleiste Staatsformen, Kanzler-Balken, Bundestag-Halbkreis, Welt-Zeitstrahl), `z_gg.js` (Aufbau Grundgesetz), `z_partei.js` (Schritt-Kacheln), `z_pilze.js` (Pilzaufbau, Hutunterseiten, Doppelgänger), `z_welt.js` (Geld- und Erfindungs-Zeitstrahl).

## Weltkarte (`werkzeug/welt.js`, Objekt `window.QWWELT`)

- Dunkles Dashboard: Canvas-Globus (orthografisch) oder flache Karte, Zoom bis 40, Relief-Textur pixelweise (inkl. **Meerestiefen** aus Natural-Earth-Bathymetrie), Beschriftung mit Kollisionsprüfung (`text()`/`frei()`), Info-Karte rechts, Legende unten links.
- **Grundkarten** in `GRUND` (Gruppen Natur, Menschen, Wirtschaft, Politik, Deutschland): Werte-Ebenen mit `p` (Palette), `s` (Skala 0–1), `lg` (Legende); Raster-Ebenen `r`; Kategorie-Ebene `kat` (Staatsform, `STAAT`-Listen nach ISO3); Bundesländer-Ebenen `de:1` mit `q` (Quelle) und `l` (Kapitel-Link) – Daten `DE`, `DEX`, Werte über `deWert(code,key)`, Info mit Rangliste `balken()`; beim Wählen fliegt die Karte nach Deutschland.
- **Overlays** `S.ov`: namen, staedte, grenzen, fluesse, landschaft, gipfel, tiefen, nacht, kriege, wander, erf, geld, goethe, Getreide, Rohstoffe (ROH), pfl, rez, aut.
- **Daten:** Natural Earth (Länder, Städte, Flüsse, Seen, Regionen, Gipfel, admin_1 für Bundesländer, Bathymetrie), OWID (Bevölkerung, Energie, Gesellschaft), eigene kuratierte Listen in `welt.js` (KRIEGE, GANSER, WANDER, ERF, GELD, GOETHE, TIEFEN …). Aufbereitung im Scratchpad mit `dash/prep2.py` → `welt_daten/` (Natural-Earth-Repo per sparse checkout von GitHub, npm ist gesperrt).
- **API:** `QWWELT.oeffne(root,ebene)`, `waehle(iso)`, `flieg(lon,lat,z)`, `hist(art,i)`, `grund(k)`, `bl(code)`, `zustand`, `zeichne()`, `legende()`.
- Neue Ebene: Daten + `GRUND`-Eintrag + ggf. Info/Legende ergänzen, `welt_einbauen.py` (läuft in `alles.sh`), Screenshot prüfen.

## 3D-Ansichten (Modul `window.QW3D`)

- **Laden:** three.js wird erst beim Klick geladen, zuerst aus `lib/`, dann vom CDN.
- **Knopf:** „◈ 3D: …“ unter dem Kurztext jeder Seite, über `d3Leiste(p,teil)`. Das Boden-Kapitel zeigt zwei Knöpfe (Boden, Kompost). Das Hanf-Kapitel nutzt das Pflanzenmodell p22.
- **Baupläne** stehen in `K`:
  ```js
  p05:{n:'Ringelblume',wuchs:'staude',H:0.45,knoten:8,stellung:'wechsel',
       blatt:{form:'spatel',l:0.1,br:0.22,farbe:[0x2f5a20,0x7ab050]},
       aeste:true,astAb:0.35,astL:0.18,
       bluete:{typ:'korb',r:0.035,n:22,ringe:2,farbe:[0xd86a10,0xf59a2a],mitte:0x8a4a10},
       wurzel:{typ:'pfahl',l:0.35,r:0.008,farbe:0xd8c8a0},
       info:'Kurzer Text unten in der Ansicht.'}
  ```
  - `wuchs`: staude, rosette, kriech, strauch, baum, pilz, schilf, gras, mais, hanf
  - `blatt.form`: oval, lanzett, herz, spatel, band, fein, rund, fieder, drei; dazu zahn, lappen/lappenN, stiel, wolb, dick (Sukkulenten)
  - `bluete.typ`: korb, stern, dolde, aehre, rispe, glocke, kaetzchen
  - `wurzel.typ`: pfahl, faser, flach, rhizom, myzel
- **Szenen:** `huegelbeet`, `boden`, `kompost` mit `szene:'…'` und einer HTML-Legende der Schichten.
- **Abgenommener Stil** (nicht ändern): Bodenfarben roh (`MR`), Pflanzenfarben linear (`lin`); ACES-Tonemapping bei Belichtung 0,88, Hemisphärenlicht 0,7, weiche Schatten.
- **Leistung:** `verschmelze()` fasst Pflanzen zu wenigen Meshes zusammen; `plattDruecken()` legt Wurzeln auf die Schnittfläche.
- **Licht, Wasser, Nährstoffe** kommen automatisch aus dem `standort`-Block.

### Realistische Optik
- **Modul:** `werkzeug/qw3d-plus.js` (ES-Modul, three r170+), eingebettet als `<script type="text/plain" id="qw3d-plus">`, beim ersten 3D-Klick per Blob-`import()` geladen; sonst greift die alte r128-Optik.
- **Importmap** oben in der Quelle zeigt auf `cdn.jsdelivr.net/npm/three@0.170.0`; `build.sh` schreibt sie für GitHub auf `./lib/three/` um (Werte müssen mit `./` beginnen).
- **Inhalt:** physikalischer Himmel, warme tiefe Sonne, Nebel, Erde mit Krümel- und Mulch-Texturen, Graswiese aus Instanzen, Blätter mit Adern-Textur und Durchlicht, Stengel mit Riefen und Härchen, schwaches GTAO (Blend 0,4, Radius 0,06), Bloom, Farb- und Vignettenpass.
- **Hooks:** `window.QW3D_PLUS(ctx)` → `{render, ende}`; `window.QW3D_PLUS_P(gruppe)` veredelt Pflanzen; `window.QW3D_STANDBILD = true` + `QW3D_AKTIV.zeichne()` für Screenshots.
- **Wurzeln** (`QW3D_PLUS_W`): sich verjüngende 3D-Röhren mit 3 Verzweigungsebenen und Wurzelhaaren, als Relief in der Schnittfläche.
- **Hügelbeet, Bodenprofil, Kompost:** plastische Schnittflächen mit Schichtdetails (`veredleHuegel`, `schnittRelief`, `sicht.schnitt`).
- **Qualität:** Bei ≤ 4 Kernen oder ≤ 3 GB RAM schlanker (18 000 Halme, Schatten 1024, keine Nachbearbeitung). Test-Parameter `?hoch`, `?noao`.
- **Testen:** per `python3 -m http.server` ausliefern, `QW3D.oeffne('p22',…)`; Software-Rendering 1–2 Minuten pro Standbild.
- **Fallen:** Skalierung nie auf `InstancedMesh`; `PCFSoftShadowMap` gibt es ab r180 nicht mehr (`PCFShadowMap` + `shadow.radius`); ab r152 sind `Color(hex)`-Werte linear.

## Weitere Bausteine der App

- **Suche:** über `stichworte`, Namen und Volksnamen.
- **Fotos:** Nutzer können eigene Fotos hinzufügen; sie werden lokal gespeichert.
- **Startseite:** Vorschaubilder als PNG (`#minibilder`, von `minis_bauen.js`), keine animierten SVGs dort – sonst lädt sie auf Tablets langsam.
- **PWA:** Ein Update zeigt „Neue Version geladen“. iPad: Safari → „Teilen“ → „Zum Home-Bildschirm“; Android: Chrome-Menü → „App installieren“.
- **Ziel Buch:** Struktur und Zeichnungen druckfähig halten (SVG, keine fremden Bildrechte). Bildvorlagen aus dem Netz nur nachzeichnen und als Anregung nennen.

## Offene Wünsche

- Ernährung (S-20–S-25, Nov. 2026): Nährwerte sind gerundete USDA-/Etikettenwerte – bei Gelegenheit gegen BLS 4.0 prüfen (blsdb.de in der Sandbox gesperrt); Video-Transkripte von Kowallik/Wolf auswerten, wenn Tom sie schickt.

- Storls Bücher einzeln zusammenfassen (je Buch eine Karte mit Themenbaum).
- Landkreis-Karten (Suizid, Kriminalität), sobald eine amtliche Kreistabelle vorliegt (Nutzer schickt Datei).
- Teil W evtl. in „Geschichte & Politik“ und „Statistik“ teilen, wenn er zu voll wird.
- Buch-Layout und Druckfassung.

## Kurs-Diagramm (Komponente `QWKurs`)

- Eine Komponente für alle Verläufe: `<script id="kurs-modul">` + CSS zwischen `/* KURS-ANFANG */` und `/* KURS-ENDE */` in `quelle/gruenwissen.html`.
- `QWKurs.mount(el, cfg)` zeichnet direkt (cfg wie Blocktyp `kurs`, zusätzlich `kompakt`, `marke` (Jahr-Linie), `zustand` (geteiltes Objekt für Zeitraum/Reihenwahl), `anim:false`). `QWKurs.block(b)` liefert den Platzhalter, `QWKurs.init(main)` bindet alle (läuft nach jedem Seitenaufbau).
- Anzeige: großer aktueller Wert, ▲/▼ seit Zeitraumbeginn und zum Vorwert (grün = gut, rot = schlecht, Reihenfarbe = neutral), Verlaufsfläche, ▲ Hoch/▼ Tief, Antippen/Ziehen/Pfeiltasten → Tooltip + Kopfwert, Kacheln Hoch/Tief/Schnitt/Start→Ende. Mehrere Reihen: gleiche Einheit → gemeinsam ein-/ausblenden; verschiedene Einheiten → Chips wählen eine Reihe, „Vergleichen“ zeigt mehrere als Index.
- Weltkarte: `kursLand()` in `werkzeug/welt.js` baut für das angetippte Land die OWID-Reihen (Bevölkerung, Lebenserwartung, Geburten, Kindersterblichkeit, Suizid, Zufriedenheit, Unterernährung, Energie, Erneuerbar, Öl/Gas/Kohle) und nutzt `window.QWKurs` (kompakt, Jahr-Marke = Zeitregler); ohne Komponente fällt sie auf die alte Sparkline zurück.
- Farben kommen aus den App-Variablen (`--ink`, `--muted`, `--line`, `--surface`, `--w` …) plus `--ku-gut`/`--ku-schlecht`; in der Weltkarte überschreibt `.qwk .kurs` sie für das dunkle Design. `prefers-reduced-motion` schaltet die Einblend-Animation ab.
- Vergleichsdiagramme (Purin, Nährwerte) nutzen `QWKurs.balken(figure,{gut, vor, seg, chips})`: Kopf (Wert + ▲/▼ zum Schnitt der Gruppe, Purin mit Ampel), Ø-Linie, ▲ Hoch/▼ Tief an den Zeilen, Stats-Kacheln; `draw()` ruft danach `KB.update({L:[{k,n,g,w}],einheit,kurz,gruppe,X,extra})`. `QWKurs.seg(gruppe)` macht aus Knopfgruppen mit `aria-pressed` ein Segmented Control mit gleitender Pille; die Sortier-Auswahl wird automatisch zu Segmenten (das `<select>` bleibt versteckt und steuert weiter). Daten und Filterlogik bleiben unverändert.
- Weltkarte kompakt: im „Verlauf“ wählt ein Auswahlmenü die Reihe, in „Vergleichen“ umbrechende Chips (kein seitliches Wischen).

## Übersicht, Gruppen, Neuigkeiten erweitern (QW_KONFIG, seit 11.11.2026)
Alles steht an **einer** Stelle: `quelle/gruenwissen.html`, Skript `<script id="qw-konfig">` (Objekt `window.QW_KONFIG`, mit Kommentaren). Das Daten-JSON bleibt unberührt.
- **Neues Kapitel in eine Gruppe:** in `teile` beim passenden Teil die `id` in `gruppen[].ids` eintragen. Ohne Eintrag erscheint es automatisch unter „Weitere“ (oder in der Gruppe mit `rest:true`).
- **Neue Gruppe:** `{t:'Name', ids:[…]}` in `gruppen` einfügen. Reihenfolge der Liste = Reihenfolge der Anzeige.
- **Neuer Teil:** einen Block in `teile` anhängen (`k`, `titel`, `kurz`, `lang`, `quelle`, `farbe`, `symbol`, `text`, `gruppen`). Startseite, Themen-Blatt, Kopfzeile, Teil-Seite und Routen (`#teil-K`, `#k-id`) entstehen daraus.
- **Was ist neu:** in `neu` oben einen Eintrag einfügen: `{d:'2026-11-12', t:'Titel', k:'Ein Satz', h:'#sprungziel', art:'Kapitel'}`. `h` darf fehlen. Die Startseite zeigt die drei neuesten.
- **Neuer Skill:** in `skills` anhängen: `{n:'name', i:'🧩', t:'Titel', s:'Ein Satz', w:['Stichwort'], tipp:'optional'}`.
- **Neue Podcast-Folge (A-08):** Reiter-Titel mit „<Gast>: …“ beginnen – die Folgen-Auswahl entsteht von selbst (ab zwei Reitern mit gleichem Anfang und mindestens acht Reitern).
- **Tabellen:** `stapel:true` erzwingt Karten auf dem Handy, `schmal:true` verhindert sie; sonst entscheidet die App (ab 3 Spalten und im Schnitt über 70 Zeichen je Zeile).
- **Neuer Blocktyp:** wie bisher eine Zeile in `block()`; Karten-Optik kommt über die gemeinsamen Klassen.
- `werkzeug/pruefen.py` prüft jetzt auch die Syntax von `qw-konfig`.
- Optik seit 11.11.2026: Leiste unten (Start · Themen · Karte · Neu · Mehr), Schalter Automatisch/Hell/Dunkel, Seiten `#neu` und `#skills`, Folgen-Auswahl bei Sammel-Einträgen. Die Gruppenliste `SG` im Code ist durch `QW_KONFIG.teile` ersetzt.
- Zeichnungen und Verläufe nachgeholt am 11.11.2026 (Autoren, Kriege, Verfahren, 54 Biochemie-Tafeln über `bio_tafel`, Teil W). Biochemie-Einträge und Verfahren ohne Reiter zeigen das Feld `illu`.
- Video-Folgen: Notizen je Transkript-Drittel, dann Generator nach Vorbild `gen_ungeskriptet.py` (Reiter <gast>, <gast>ab, <gast>zeit, <gast>abgleich); Abgleich immer mit geprüften Quellenlinks, zwei Zeichnungen und Kurs-Blöcken; Video oben und unter Quellen verlinken.
- Weltkarte seit 11.11.2026 (Runde 2): Globus, Scheibe und flache Karte werden mit WebGL gezeichnet (eigenes kleines Programm in `werkzeug/welt.js`, ohne three.js), mit automatischem Rückfall auf Canvas (Test: `?canvas`); Schalter „Wolken“ (`#welt-wolken`); Themen-Ebenen nutzen ein entsättigtes Grundbild. Beschriftung in Alegreya (Länder gesperrte Kapitälchen, Meere kursiv). Farb-Tokens der Seite: `--tc` (Bereichsfarbe), `--surface-2`, `--nacht`; Bereichsfarben P/S/G/R/B/W/A als abgestimmte Familie.

## Übergabe 11.11.2026 (Abend)
- Stand: Commit „Erde in neuer Qualität …“ auf main; Artefakt Version 70. A-08 `ungeskriptet` enthält Gudwis, Merscher, Regenauer. Zeichnungen und Verläufe überall nachgeholt, neue Optik, QW_KONFIG, Seiten `#neu` und `#skills`, Weltkarte mit WebGL.
- Wartet auf Transkripte von Tom (a-Shell, `python3 transkript.py <ID>`): KPeTQYdof7Q, T4GHSolVGyE, KlDkL8W2kPk. Ob sie zu {ungeskriptet} gehören, erst am Transkript-Kopf prüfen; sonst eigener Autor oder neuer Sammeleintrag.
- Ablauf je Video (bewährt): Transkript in drei Teile, je Teil Notizen (Abschnitte, Personen, Orte, Begriffe, Zahlen, Zeitleiste, Spannungen, Abgleich-Kandidaten); daraus Generator nach Vorbild Gudwis (vier Reiter mit Gast-Kürzel, „<Gast>: …“ im Titel), Abgleich mit geprüften Quellenlinks, zwei Zeichnungen, Kurs-Blöcke; Zeile in „Folgen“, Eintrag in `QW_KONFIG.neu`.
- Offen: Veröffentlichungsdatum bei Merscher und Regenauer (steht „2026“); mit ❓ markierte Angaben in deren Abgleich; Demenz-Verlauf in W-05 (Destatis-GENESIS braucht Anmeldung); Weltkarte auf echtem iPad/Android testen (Leistung, Akku), bei Bedarf Wolken/Auflösung drosseln; Projekt-Dokument „Selbstversorgung/Pflanzenkunde“ nicht aktualisiert; Strukturformeln der Stoff-Tafeln nicht gegen Nachschlagewerk geprüft.
- Die Generator-Skripte und Notizen dieser Sitzung lagen nur im Scratchpad und sind weg; Vorbild ist der fertige Eintrag A-08 im Daten-JSON.
