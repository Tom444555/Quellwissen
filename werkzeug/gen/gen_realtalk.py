# Rahmen für A-12 REALTALK MEDIA (Kanal-Sammelstelle). Aufruf: python3 gen_realtalk.py → realtalk.json
import json
YT="[Beispiel-Video des Kanals (YouTube)](https://www.youtube.com/watch?v=wwJX6gdF3Bc)"
def ab(t,*l): return {"typ":"abschnitt","titel":t,"liste":list(l)}
def tx(t): return {"typ":"text","text":t}
person=[
 tx("**REALTALK MEDIA** ist ein deutschsprachiger YouTube-Kanal mit langen Gesprächen von meist eineinhalb bis zweieinhalb Stunden. Zu Gast sind Autoren, Publizisten, Ärzte und Politiker; die Themen reichen von Geopolitik und Geheimdiensten über Geldsystem und Digitalisierung bis zu Gesundheit und Bildung. Wer den Kanal betreibt und wer die Gespräche führt, ließ sich bisher nicht aus einer prüfbaren Quelle belegen ❓ – in den Videos selbst fällt der Name des Gastgebers meist nicht."),
 tx("Dieser Eintrag ist als **Sammelstelle für ausgewertete Gespräche** angelegt: Jedes Gespräch bekommt eigene Reiter (Überblick, Gespräch im Detail, Zeitachse, Abgleich & Daten). Links steht, was im Gespräch gesagt wird, rechts daneben die gängige Darstellung bzw. die Daten mit Quelle – und darunter der Prüfstand für Staat und Institutionen. Die Bewertung bleibt dem Leser."),
 {"typ":"tabelle","kopf":["🧭 Was","Stand","Quelle"],"zeilen":[
  ["Kanal","REALTALK MEDIA (YouTube)","Angabe im Kopf der Transkripte"],
  ["Sendungsnamen im Gespräch","„100% Real Talk“ und „Good Morning Germany“ werden in einem Gespräch genannt","{{a:regenauer-iran|Regenauer: Iran und Energiekrise}}"],
  ["Gastgeber","Name bisher nicht belegt ❓; in einem Gespräch nennt er den Iran seine Heimat","{{a:regenauer-iran|ebenda}}"],
  ["Betreiber, Sitz, Gründung","nicht geprüft ❓","–"]],"stapel":True},
 ab("📂 Wo Gespräche des Kanals sonst stehen","Gäste mit eigener Sammelstelle stehen dort: {{a:regenauer|Tom-Oliver Regenauer (A-11)}} mit den Gesprächen „Iran und Energiekrise“, „Sozialismus und Zionismus“ und „Trump und Epstein“.","Alle übrigen Gespräche des Kanals kommen hierher."),
]
folgen=[tx("Alle hier ausgewerteten Gespräche von REALTALK MEDIA. Eine Karte antippen öffnet die Auswertung; oben in der Leiste lässt sich jedes Gespräch auch direkt wählen."),{"typ":"folgenkarten"}]
web=[tx("Kanal und Videos. Stand: November 2026; YouTube-Titel sind die Originaltitel."),
 {"typ":"tabelle","kopf":["🌐 Seite","Link"],"zeilen":[["YouTube (Kanal-Adresse nicht geprüft ❓)",YT]]},
 {"typ":"tabelle","kopf":["🎬 Video","Kanal","Link"],"zeilen":[]}]
quellen=[{"typ":"quellen","eintraege":[["REALTALK MEDIA – Beispiel-Video (YouTube)","https://www.youtube.com/watch?v=wwJX6gdF3Bc"]]}]
A={"id":"realtalk","nr":"A-12","name":"REALTALK MEDIA","botan":"YouTube-Kanal mit langen Gesprächen","volksnamen":[],
 "kurz":"REALTALK MEDIA ist ein YouTube-Kanal mit langen Gesprächen zu Politik, Geheimdiensten, Geld, Gesundheit und Bildung. Hier gesammelt: ausgewertete Gespräche – je Gespräch Überblick, Verlauf im Detail, Zeitachse und Abgleich mit Daten samt Prüfstand.",
 "steckbrief":[["Format","Lange Gespräche (meist 1,5–2,5 Stunden) auf YouTube"],["Gastgeber","Name nicht belegt ❓"],["Themen","Geopolitik, Geheimdienste, Geldsystem, Digitalisierung, Gesundheit, Bildung"],["Ausgewertete Folgen","0 (Stand 12.11.2026)"]],
 "reiter":[{"id":"person","titel":"Kanal & Macher","bloecke":person},{"id":"folgen","titel":"Folgen","bloecke":folgen},{"id":"web","titel":"Web","bloecke":web},{"id":"quellen","titel":"Quellen","bloecke":quellen}]}
json.dump(A,open('realtalk.json','w'),ensure_ascii=False); print('ok')
