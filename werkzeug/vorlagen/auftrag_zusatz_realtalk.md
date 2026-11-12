# Zusatzauftrag: Video für die Sammelstelle A-12 `realtalk` (Kanal REALTALK MEDIA)

Du wertest GENAU EIN Video-Transkript für das Kompendium „Quellwissen“ aus und lieferst fertige Daten-Dateien. Arbeite exakt nach `/home/claude/quellwissen/werkzeug/vorlagen/auftrag_folge.md` (ganz lesen) und liefere im selben Lauf den Prüfstand nach `/home/claude/quellwissen/werkzeug/vorlagen/auftrag_pruefstand.md` (ganz lesen). Du änderst NICHTS im Repo `/home/claude/quellwissen` (nur lesen). Sprache: Deutsch.

## Abweichungen von der Vorlage (Ziel ist NICHT A-08)
- `folge.kanal` = „REALTALK MEDIA“; Gastgeber per Suche klären, sonst ❓. Veröffentlichungsdatum per Suche (YouTube selbst ist vom Server nicht abrufbar), sonst Jahr + ❓; Aufnahmezeit aus Bezügen im Gespräch eingrenzen.
- Interner Link in `folgen_zeile`: `{{a:realtalk-<K>|hier: <G>}}`; `neu.h` = `#a-realtalk-<K>`, `neu.d` = „2026-11-12“, `neu.art` = „Video“; Quellen-Zeile „Video: … – REALTALK MEDIA (YouTube)“.
- Querverweise nur auf vorhandene Einträge, wo es wirklich passt: `{{a:regenauer|Tom-Oliver Regenauer (A-11)}}`, `{{a:ganser|Daniele Ganser (A-04)}}`, `{{a:lausen|Tom Lausen (A-09)}}`, `{{a:wikihausen|Geschichten aus Wikihausen (A-10)}}`. Keine `{{a:<gast>|…}}`-Links für Gäste ohne eigenen Eintrag.
- Vorbild für Aufbau und Ton: das fertige Ergebnis `/home/claude/scratch/reg1/folge.json` und `/home/claude/scratch/reg1/pruefstand.json` (nur Ausschnitte per Python ansehen) sowie `/home/claude/scratch/reg1/z_masterpeace.js` für die Zeichnungen. Handbuch-Abschnitt „Folgen-Modul“ nur gezielt mit `sed -n` lesen.
- Zusätzlich im Überblick (nach „⚡ In Kürze“) ein `abschnitt` „🔦 Aus Sicht des Gastes – der rote Faden“ (Titel mit dem Namen des Gastes) (`liste`, 4–6 Sätze, klar als seine Sicht).
- Umfang bei rund zwei Stunden: 28–36 Abschnitte, 18–26 Abgleich-Zeilen, 35–50 Zeitachsen-Einträge, 5–8 Diagramme (kurs/balken/vergleich) nur mit geprüften amtlichen/primären Zahlen, zwei Zeichnungen.
- Hörfehler bei Namen: siehe die Liste in deinem Einzelauftrag; Namen immer gegen eine Quelle prüfen, sonst ❓.

## Regeln, die hier besonders zählen
- Neutral in beide Richtungen: Aussagen von Gast und Gastgeber sachlich wiedergeben, als „[seine Sicht]“ kennzeichnen, keine Etiketten. Rechts im Abgleich die gängige Darstellung bzw. Daten mit geprüfter Quelle.
- Aussagen zu Judentum, Zionismus, Israel, Rothschild, Nationalsozialismus: knapp und genau so wiedergeben, wie sie gesagt werden (wer sagt was, mit Fundstelle), ohne eigene Verallgemeinerungen über Menschen oder Gruppen; Unterscheidungen, die der Sprecher selbst trifft, festhalten. Daneben belegte Fakten mit Quelle (z. B. Haavara-Abkommen 1933, Balfour-Erklärung, Gründung Israels – nur was Quellen tragen) und, wo Fachstellen (bpb, Yad Vashem, USHMM, Bundesarchiv) solche Deutungen einordnen, deren Einordnung als deren Aussage mit Quelle.
- Vorwürfe gegen lebende, namentlich genannte Personen (Straftaten, Missbrauch, Mord, Geheimdienst-Tätigkeit): nur als Aussage des Sprechers mit Fundstelle wiedergeben, nichts ausschmücken; im Abgleich daneben, was Gerichte, Ermittlungsakten oder amtliche Stellen dazu festgestellt haben – und klar ❓, wo nichts belegt ist. Bei Todesfällen von Prominenten: amtliche Todesursache mit Quelle nennen; bei Suizid keine Methoden, nur kurzer Hilfehinweis (Telefonseelsorge 0800 111 0 111).
- Gesundheit/Medizin nur auf Laien-Ebene und mit Fachstellen im Abgleich; keine Empfehlungen.
- Zitate höchstens ~12 Wörter, höchstens 2 je Abschnitt; sonst eigene Worte.
- Was du nicht belegen kannst: ❓ offen lassen, nicht raten. Sparsam arbeiten: 12–20 gezielte Suchen/Abrufe.

## Prüfstand (`pruefstand.json` im Arbeitsordner)
Format: `{"eintraege":[{"autor":"realtalk","reiter":"<K>abgleich","staat":[[Punkt, Was belegt ist, "[Titel](url)"],…],"datenluecken":[[…]],"fragen":["…"],"autor_zeilen":[[…]],"fazit":"…"}]}` – 5–8 `staat`-Zeilen zu Themen dieses Gesprächs (Gerichte, Rechnungshöfe, Untersuchungsausschüsse, amtliche Berichte, Behörden), 0–3 `datenluecken`, 3–5 `fragen` (echte Fragen, ohne Motive zu unterstellen), 0–4 `autor_zeilen`, `fazit` 2–4 Sätze ohne Urteil. Nur geprüfte Links, keine Wertungswörter.

## Abzugeben im Arbeitsordner
`notizen.md`, `gen.py` (erzeugt `folge.json`), `folge.json`, `z_<K>.js` (zwei Funktionen `<K>_…`), `pruefstand.json`. Selbstprüfung der Vorlage ausführen (JSON lädt, Reiter-Ids `<K>`, `<K>ab`, `<K>zeit`, `<K>abgleich`, Titel beginnen mit „<G>: “, teile = Abschnitte mit gleichen Zeitspannen, alle `th` in `themen`, kurs-Punkte aufsteigend, keine `{{…}}` in Baum-Knoten, illu-ids = Funktionsnamen, Zeichnungen laufen mit node und Ersatz-Helfern).

## Rückmeldung (kurz, keine Inhalte)
Veröffentlichungsdatum und Gastgeber (gefunden oder ❓), Zahl der Abschnitte/Abgleich-Zeilen/Diagramme/Prüfstand-Zeilen, was offen blieb, und ob du bewusst gekürzt oder ausgelassen hast.
