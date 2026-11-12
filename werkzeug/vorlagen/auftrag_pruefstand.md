# Auftrag: „Staat und Institutionen im Prüfstand“ für das Kompendium Quellwissen

## Worum es geht
Das Kompendium wertet Autoren und Podcast-Gespräche aus. Bisher steht in jedem Abgleich: links die Aussage des Autors,
rechts die „gängige Darstellung / Daten“ mit Quelle. Der Besitzer (Tom) möchte **denselben strengen Maßstab für beide Seiten**:
Auch Staat, Behörden und Institutionen sollen dort, wo es **belegt** ist, kritisch sichtbar werden – nicht als Meinung,
sondern als nachprüfbare Tatsache. Ziel ist ein Bild, aus dem sich jeder selbst eine Meinung bilden kann.

Du bearbeitest die dir genannten Reiter. Du änderst NICHTS im Repo `/home/claude/quellwissen`. Deine Ausgabe ist EINE Datei
`/home/claude/scratch/staat/<name>.json` (Name wird dir genannt).

## Material
`/home/claude/scratch/staat/bestand.json` (eingerückt): je Autor-Id die Reiter mit ihren Tabellen/Abschnitten
(`bestand[autor][reiter]["bloecke"]`). Lies NUR deine Reiter per kleinem Python-Skript (nicht die ganze Datei ausgeben).
Die Abgleich-Tabelle ist der Baustein mit `kopf` „Aussage … | Gängige Darstellung … | Quelle“.

## Was du je Reiter lieferst
1. **`staat`** – 4 bis 8 Zeilen `[Punkt, Was belegt ist, Quelle]` zu Themen, die in genau diesem Eintrag vorkommen:
   belegte Versäumnisse, Korrekturen, Widersprüche, Dokumentationslücken oder spät/erst auf Klage veröffentlichte Unterlagen
   auf Seiten von Staat, Behörden, öffentlich-rechtlichen oder überstaatlichen Institutionen (auch große Fachgesellschaften,
   wenn sie Empfehlungen später geändert haben).
   - „Punkt“: 3–8 Wörter. „Was belegt ist“: 1–3 Sätze, mit Jahr und Zahl, sachlich, ohne Adjektive der Wertung.
   - „Quelle“: `[Titel](https://…)`, mehrere mit „ · “ getrennt. **Nur geprüfte Links** (per WebSearch gefunden / WebFetch gelesen).
   - Zulässige Belege: Bundesrechnungshof und Landesrechnungshöfe, Gerichtsurteile (BVerfG, BVerwG, EuGH, EGMR …),
     amtliche Evaluations- und Untersuchungsberichte (Untersuchungsausschüsse, Enquete-Kommissionen, Sachverständigenausschuss
     nach § 5 Abs. 9 IfSG, Wehrbeauftragte, Datenschutzbeauftragte …), Parlamentsdrucksachen und Antworten der Bundesregierung,
     Statistikämter, Behörden selbst (RKI, PEI, BfR, BaFin …), Fachzeitschriften mit Begutachtung, Deutsches Ärzteblatt,
     ausnahmsweise große Zeitungen/Sender als Beleg für einen Vorgang.
   - Nicht zulässig: Vermutungen, Motive unterstellen, Etiketten. Nur was die Quelle trägt.
   - Wenn ein Punkt die Sicht des Autors stützt, darf das so dastehen. Wenn die Quelle zugleich etwas enthält, das die
     Staatsseite entlastet, gehört das in denselben Satz (gleicher Maßstab).
2. **`autor`** – 0 bis 4 Zeilen `[Punkt, Was belegt ist, Quelle]`: Stellen, an denen Aussagen des Autors/Gastes durch Daten
   NICHT gedeckt sind und das im bestehenden Abgleich noch nicht klar steht. Nur wenn nötig; nichts doppelt.
3. **`korrekturen`** – 0 bis 6 Einträge für bestehende Abgleich-Zeilen, in denen die rechte Spalte etwas als gesichert
   darstellt, das laut Quellenlage offen ist, später amtlich korrigiert wurde oder nur eine von mehreren fachlichen
   Positionen ist – ODER in denen umgekehrt der Autor ungeprüft Recht bekommt:
   `{"alt": "<exakter, eindeutiger Textausschnitt aus der bestehenden Zelle, 40–160 Zeichen, wörtlich kopiert>",
     "neu": "<Ersatztext für genau diesen Ausschnitt>", "grund": "<1 Satz>"}`.
   Der `alt`-Text muss in der Zelle wörtlich und genau einmal vorkommen (per Python prüfen!). Quellenlinks im `neu`-Text
   als `[Titel](url)`.
4. **`fazit`** – 2 bis 4 Sätze „Stand der Belege“: was auf beiden Seiten belegt ist und was offen bleibt. Keine Wertung,
   keine Empfehlung, kein Urteil darüber, wer Recht hat.

Wenn zu einem Reiter nichts Belegbares passt: `staat: []` und im `fazit` kurz sagen, warum.

## Regeln
- Deutsch, schlichte Sprache. Keine Wörter wie „Verschwörungstheorie“, „umstritten“, „Skandal“ (außer im Titel einer Quelle),
  „versagt“, „dreist“. Stattdessen sagen, was geschah: „stellte fest“, „rügte“, „korrigierte“, „veröffentlichte erst nach Klage“,
  „Daten wurden nicht erhoben“.
- Gesundheit: nichts schreiben, was als Behandlungs- oder Dosierempfehlung gelesen werden kann. Bei Impfung, Ernährung,
  Arzneien stets den Stand der Fachstellen korrekt wiedergeben; belegte Mängel (z. B. Datenlücken, geänderte Empfehlungen,
  Gerichtsurteile, Rechnungshof) dürfen genannt werden.
- Zahlen nur mit Quelle. Nichts ableiten oder schätzen.
- Inline-Format: `**fett**`, `[Titel](url)`. Keine `{{…}}`-Links nötig.
- Richtwert: 6–10 Suchen/Abrufe je Reiter, parallel wo möglich.

## Ausgabeformat (JSON)
```json
{"eintraege": [
  {"autor": "ungeskriptet", "reiter": "jebsenabgleich",
   "staat": [["Punkt", "Was belegt ist", "[Titel](url)"]],
   "autor_zeilen": [["Punkt", "Was belegt ist", "[Titel](url)"]],
   "korrekturen": [{"alt": "…", "neu": "…", "grund": "…"}],
   "fazit": "…"}
]}
```
(Achtung: der Schlüssel für Punkt 2 heißt `autor_zeilen`.)
Am Ende selbst prüfen: Datei lädt als JSON; jede Zeile hat 3 Felder; jeder `alt`-Text kommt in bestand.json im richtigen
Reiter genau einmal vor; jede Quelle ist ein Markdown-Link.

## Rückmeldung an mich (kurz)
Je Reiter eine Zeile: Zahl der Staat-Zeilen / Autor-Zeilen / Korrekturen und das Wichtigste, was du NICHT belegen konntest.
Keine Inhalte wiederholen.
