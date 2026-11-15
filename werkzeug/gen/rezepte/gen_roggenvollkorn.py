import json, sys
sys.path.insert(0, '/home/claude/quellwissen/werkzeug')
from bausteine import *

DGE = "https://www.dge.de/fileadmin/dok/gesunde-ernaehrung/faq/DGE-FAQ-Ballaststoffe-2021.pdf"
MRI = "https://www.mri.bund.de/fileadmin/MRI/Veroeffentlichungen/Wissenschaftliche_Einordnung/2026-06-Ballaststoffe_Einordnung_bfrei.pdf"
VZ = "https://www.verbraucherzentrale.de/wissen/lebensmittel/kennzeichnung-und-inhaltsstoffe/werbung-mit-naehrwertangaben-klare-vorgaben-fuer-die-hersteller-10478"
EU = "https://www.ernaehrungs-umschau.de/fileadmin/Ernaehrungs-Umschau/pdfs/pdf_2010/09_10/EU09_2010_B33_B37.qxd.pdf"
SP = "https://www.spektrum.de/lexikon/ernaehrung/sauerteig/7839"
DM = "https://www.dm.de/p/d/1446464/"
AEB = "https://www.aerzteblatt.de/news/fachgesellschaft-empfiehlt-lebensmittel-mit-mehr-ballaststoffen-f1e10e63-a6c4-424d-b423-053eb9ca4430"

rezept = R("rezept", "Rezept",
    illu("roggenvollkorn_bild", "Roggen-Vollkornbrot in der Kastenform, Anschnitt mit Kernen, daneben Sonnenblumenkerne, Kürbiskerne und Leinsamen"),
    tab(["Zutat", "Menge"],
        ["Roggenvollkornmehl", "350 g"],
        ["Weizenvollkornmehl", "150 g"],
        ["Trockenhefe", "1 Päckchen"],
        ["Salz", "1 TL"],
        ["Honig oder Ahornsirup", "1 TL"],
        ["Lauwarmes Wasser", "450 ml"],
        ["Sonnenblumenkerne", "2 EL"],
        ["Kürbiskerne", "2 EL"],
        ["Leinsamen", "2 EL"],
        ["Haferflocken (zum Bestreuen)", "1 EL"],
        ["Öl für die Backform", "etwas"]),
    illu("roggenvollkorn_leiste", "Mehle mischen, mit Honig und Wasser rühren, Kerne dazu, gehen lassen, in die Form, backen, auskühlen"),
    tab(["#", "Schritt", "Zeit", "Hinweis [Ergänzung]"],
        ["1", "Roggenvollkornmehl, Weizenvollkornmehl, Trockenhefe und Salz in einer großen Schüssel mischen.", "", "Gründlich durchmischen, dann verteilt sich die Hefe gleichmäßig."],
        ["2", "Honig (oder Ahornsirup) und das lauwarme Wasser dazugeben. Alles zu einem gleichmäßigen, eher klebrigen Teig verrühren.", "", "Lauwarm heißt etwa 30–35 °C. Der Teig soll weich und klebrig sein – kein Mehl nachschütten. Ein kräftiger Kochlöffel genügt; langes Kneten bringt bei Roggen wenig."],
        ["3", "Sonnenblumenkerne, Kürbiskerne und Leinsamen untermischen.", "", ""],
        ["4", "Schüssel abdecken und den Teig an einem warmen Ort gehen lassen.", "ca. 60 Min.", "Roggenteig geht weniger auf als Weizenteig: Er wird sichtbar lockerer, verdoppelt sich aber nicht unbedingt."],
        ["5", "Kastenform leicht mit Öl einfetten. Teig einfüllen, glattstreichen und mit Haferflocken oder zusätzlichen Kernen bestreuen.", "", "Mit nassem Löffel oder nasser Teigkarte glattstreichen, dann klebt nichts. Die Form höchstens zu etwa drei Vierteln füllen."],
        ["6", "Den Teig in der Form noch einmal ruhen lassen.", "ca. 20 Min.", "In dieser Zeit den Ofen vorheizen."],
        ["7", "Im vorgeheizten Ofen bei 200 °C Ober-/Unterhitze backen.", "ca. 50–55 Min.", "Mittlere oder untere Schiene. Garprobe: siehe „Tipps & Varianten“."],
        ["8", "Brot aus der Form nehmen und auf einem Kuchengitter vollständig auskühlen lassen.", "", "Roggenbrot erst ganz ausgekühlt anschneiden, am besten erst nach einigen Stunden – die Krume festigt sich noch."]),
    hin("Tipp aus der Vorlage: Das Brot in Scheiben schneiden und einfrieren; einzelne Scheiben bei Bedarf toasten. Gut verpackt hält es sich etwa 3–4 Tage. Es passt zu herzhaftem und zu süßem Belag und lässt sich gut auf Vorrat backen."))

tipps = R("tipps", "Tipps & Varianten",
    abs_("Garprobe [Ergänzung]", [
        "**Klopfprobe:** Brot aus der Form stürzen und von unten daraufklopfen – klingt es hohl, ist es durch.",
        "**Kerntemperatur:** mit einem Thermometer in der Mitte gemessen etwa 96–98 °C.",
        "Wird die Oberfläche zu früh dunkel, die letzten 15 Min. mit Backpapier oder Alufolie abdecken.",
        "Für mehr Kruste: das Brot die letzten 5–10 Min. ohne Form auf dem Rost fertig backen."]),
    abs_("Mit etwas Säure wird die Krume sicherer [Ergänzung]", [
        "Die Vorlage arbeitet nur mit Hefe. Die Backlehre gibt für Teige mit viel Roggen zusätzlich Säure an (Sauerteig oder Teigsäuerung) – warum, steht im Reiter „Warum es klappt“.",
        "**Einfachste Lösung:** 1–2 EL Apfelessig ins Wasser geben. Man schmeckt ihn im fertigen Brot kaum.",
        "**Milchsauer:** einen Teil des Wassers (etwa 150 ml) durch Buttermilch oder Naturjoghurt ersetzen.",
        "**Klassisch:** mit Sauerteig backen – das braucht mehr Zeit und ein anderes Rezept. Wie man ihn ansetzt: {{g:brot|Getreide & Brot}}, Reiter „Hefe & Sauerteig“.",
        "Ob das Brot auch ganz ohne Säure schnittfest wird, hängt vom Mehl ab; die Enzymaktivität des Roggens schwankt je nach Erntejahr."]),
    abs_("Kerne, Mehl und Gewürze abwandeln [Ergänzung]", [
        "**Kerne anrösten:** Sonnenblumen- und Kürbiskerne ohne Fett in der Pfanne kurz rösten und abkühlen lassen – das gibt mehr Aroma.",
        "**Quellstück:** Kerne und Leinsamen 30 Min. in einem Teil des abgemessenen Wassers quellen lassen. So entziehen sie der Krume später kein Wasser.",
        "**Leinsamen:** ganz bleibt er im Brot sichtbar und knackig; geschrotet bindet er mehr Wasser.",
        "**Dinkel statt Weizen:** Weizenvollkornmehl lässt sich 1:1 durch Dinkelvollkornmehl ersetzen.",
        "**Brotgewürz:** 1–2 TL Kümmel, Fenchel und Koriander (ganz oder gemahlen) passen gut zu Roggen."]),
    abs_("Aufbewahren und einfrieren", [
        "Laut Vorlage gut verpackt etwa 3–4 Tage haltbar; in Scheiben einfrieren und einzeln toasten.",
        "[Ergänzung] Bei Zimmertemperatur im Brotkasten, Tontopf oder in ein Tuch gewickelt lagern – nicht im Kühlschrank, dort wird Brot schneller altbacken.",
        "[Ergänzung] Eingefroren hält es etwa 3 Monate. Mehr: {{s:einfrieren|Einfrieren}}."]),
    tab(["Problem [Ergänzung]", "Ursache", "Abhilfe"],
        ["Krume klebt am Messer, wirkt nass", "zu früh angeschnitten, zu kurz gebacken oder Teig ohne Säure", "ganz auskühlen lassen, Garprobe machen, beim nächsten Mal 1–2 EL Apfelessig zugeben"],
        ["Brot fällt in der Mitte ein", "zu lange oder zu warm gegangen (Übergare)", "Gehzeit verkürzen; die Form nicht zu voll füllen"],
        ["Brot bleibt flach und sehr dicht", "Hefe zu alt oder Wasser zu heiß", "frische Trockenhefe nehmen; Wasser nur lauwarm"],
        ["Oberfläche reißt stark auf", "zu kurz gegangen oder Oberfläche angetrocknet", "abgedeckt gehen lassen; vor dem Backen mit Wasser bestreichen"],
        ["Kerne fallen beim Schneiden ab", "Streu haftet nicht", "Oberfläche vor dem Bestreuen mit Wasser bestreichen, Kerne leicht andrücken"]))

chemie = R("chemie", "Warum es klappt",
    abs_("Roggen backt anders als Weizen [Ergänzung]", [
        "Weizen bildet beim Kneten aus {{b:gluten|Gluten}} ein elastisches Klebernetz, das die Gärgase hält. Im Roggen entsteht dieses Netz kaum – seine quellfähigen {{b:schleimstoffe|Schleimstoffe}} (Pentosane) stehen dem im Weg.",
        "Die Pentosane übernehmen dafür selbst einen Teil der Arbeit: Sie binden ein Vielfaches ihres Gewichts an Wasser. Roggenmehl enthält davon etwa doppelt so viel wie Weizenmehl ([Ernährungs-Umschau 9/2010](" + EU + ")).",
        "Darum verträgt dieser Teig so viel Wasser (450 ml auf 500 g Mehl), ist klebrig und wird gerührt statt geknetet. Die Kastenform gibt ihm den Halt, den beim Weizenbrot das Klebernetz liefert.",
        "Die 150 g Weizenvollkornmehl bringen etwas Kleber mit und machen die Krume lockerer als bei reinem Roggenbrot."]),
    abs_("Warum die Backlehre bei Roggen Säure vorsieht [Ergänzung]", [
        "Roggen enthält viele stärkeabbauende Enzyme ({{b:amylasen|Amylasen}}). Im Ofen arbeiten sie besonders schnell, bevor die Hitze sie ausschaltet.",
        "Ohne Säure können sie so viel {{b:staerke|Stärke}} abbauen, dass die Krume klebrig bleibt. Säure bremst die Enzyme und verbessert die Quellung der Pentosane ([Spektrum, Lexikon der Ernährung: Sauerteig](" + SP + ")).",
        "Als Faustregel nennt die Ernährungs-Umschau: Teige mit etwa 20 % Roggenmehl und mehr brauchen Sauerteig oder ein Teigsäuerungsmittel. Dieses Rezept hat 70 % Roggen und kommt in der Vorlage ohne aus – darum der Vorschlag mit dem Apfelessig unter „Tipps & Varianten“.",
        "Mehr dazu: {{g:brot|Getreide & Brot}}, Reiter „Kleber & Chemie“."]),
    abs_("Hefe, Honig und Salz [Ergänzung]", [
        "{{s:hefe|Hefe}} vergärt Zucker zu Kohlendioxid und etwas Alkohol ({{b:gaerung|Gärung}}); das Gas lockert den Teig. Am wohlsten fühlt sie sich bei etwa 26–35 °C, darum lauwarmes Wasser und ein warmer Platz.",
        "Der Teelöffel Honig oder Ahornsirup gibt der Hefe einen schnellen Start und hilft der Kruste beim Bräunen.",
        "Salz würzt und bremst die Gärung etwas, sodass der Teig gleichmäßiger aufgeht."]),
    abs_("Kerne, Leinsamen und Haferflocken [Ergänzung]", [
        "Leinsamen bildet mit Wasser eine Schleimschicht ({{b:schleimstoffe|Schleimstoffe}}). Sie hält Feuchtigkeit in der Krume – das Brot bleibt länger saftig.",
        "Leinsamen enthält außerdem die pflanzliche Omega-3-Fettsäure ALA ({{b:omega3|Omega-3}}). Ganze Körner werden beim Essen oft nicht zerkaut; geschrotet ist der Inhalt besser zugänglich.",
        "Haferflocken bringen {{b:beta-glucane|Beta-Glucane}} mit, Sonnenblumen- und Kürbiskerne Fett, Eiweiß und beim Backen Röstaroma auf der Kruste."]),
    abs_("Warum das Auskühlen dazugehört [Ergänzung]", [
        "Direkt aus dem Ofen ist die verkleisterte Stärke noch weich und die Krume sehr feucht. Beim Abkühlen ordnet sich die Stärke neu und wird fest, die Feuchtigkeit verteilt sich.",
        "Wer zu früh schneidet, drückt die Krume zusammen – sie wirkt dann nass, obwohl das Brot durchgebacken ist."]))

einordnung = R("einordnung", "Was drin steckt",
    txt("Die Bildtafel der Vorlage beschreibt das Brot als „darmfreundlich“, „reich an Ballaststoffen“, „proteinreich“ und „leicht & bekömmlich“ mit „100 % natürlichen Zutaten“. Hier steht daneben, was Nährwertangaben und Fachstellen zu diesen Punkten sagen. Die Werte für das fertige Brot sind ein eigener Überschlag aus den Zutaten [Ergänzung] – keine Laboranalyse."),
    {"typ": "balken", "titel": "📊 Ballaststoffe je 100 g – zum Vergleich", "einheit": "g", "dez": 1,
     "zeilen": [["Leinsamen, geschrotet (DGE)", 22], ["Roggenvollkornmehl (Packungsangabe)", 13],
                ["Dieses Brot (eigener Überschlag)", 7.5], ["Vollkornnudeln, gekocht (DGE)", 5],
                ["Helle Nudeln, gekocht (DGE)", 2]],
     "quelle": "[DGE: Fragen und Antworten zu Ballaststoffen (2021)](" + DGE + ") · [dm: Roggen-Vollkornmehl, Nährwerte](" + DM + ") · Brot: Überschlag aus den Zutaten des Rezepts",
     "hinweis": "Überschlag für das Brot: rund 70 g Ballaststoffe aus Mehl und Kernen in etwa 900 g fertigem Brot. Je nach Mehl und Backverlust weicht der Wert ab."},
    tab(["Angabe der Vorlage", "Was Nährwertangaben und Fachstellen dazu sagen", "Quelle"],
        ["„Reich an Ballaststoffen“",
         "Roggenvollkornmehl enthält laut Packungsangaben rund 13 g Ballaststoffe je 100 g, geschroteter Leinsamen 22 g. Überschlag für dieses Brot [Ergänzung]: etwa 7–8 g je 100 g, also rund 3–4 g in einer Scheibe von 50 g. Als ballaststoffreich gilt Brot ab 6 g je 100 g.",
         "[dm, Nährwerte](" + DM + ") · [DGE](" + DGE + ") · [Ernährungs-Umschau 9/2010](" + EU + ")"],
        ["„Proteinreich“",
         "Roggenvollkornmehl enthält rund 9,5 g Eiweiß je 100 g. Überschlag für dieses Brot [Ergänzung]: etwa 7 g je 100 g, das sind grob 12–14 % des Brennwerts. Die EU-Regeln für Werbung im Handel setzen „Proteinquelle“ ab 12 % und „hoher Proteingehalt“ ab 20 % des Brennwerts an. Für ein privates Rezept gelten diese Regeln nicht; sie dienen hier nur als Maßstab.",
         "[dm, Nährwerte](" + DM + ") · [Verbraucherzentrale: Werbung mit Nährwertangaben](" + VZ + ")"],
        ["„Gut für deinen Darm“, „darmfreundlich“",
         "Die DGE nennt für Erwachsene mindestens 30 g Ballaststoffe am Tag; im Schnitt werden 18 g (Frauen) und 19 g (Männer) erreicht. Brot ist in Deutschland die wichtigste Ballaststoffquelle. Laut DGE sinkt bei genug Flüssigkeit das Risiko für Verstopfung. ❓ Eine Untersuchung zu genau diesem Rezept gibt es nicht.",
         "[DGE](" + DGE + ") · [Max Rubner-Institut, Einordnung Ballaststoffe (Juni 2026)](" + MRI + ") · [Ärzteblatt](" + AEB + ")"],
        ["„Leicht & bekömmlich“",
         "Dafür gibt es keinen festen Maßstab; wie gut Vollkorn vertragen wird, ist von Mensch zu Mensch verschieden. [Ergänzung] Vollkorn, Roggen und Kerne können bei empfindlichem Darm blähen. Eine lange Teigführung baut einen Teil der schwer verdaulichen Zucker ab – dieses Rezept geht mit 80 Min. vergleichsweise kurz.",
         "{{g:brot|Getreide & Brot}}, Reiter „Gesundheit“"],
        ["„100 % natürliche Zutaten“",
         "Die Zutatenliste besteht aus Mehl, Hefe, Salz, Honig oder Ahornsirup, Wasser, Kernen, Haferflocken und etwas Öl. Zusatzstoffe oder Backmischungen kommen nicht vor.",
         "Bildschirmfotos des Nutzers"]),
    hin("**Gut zu wissen:** Roggen und Weizen enthalten Gluten – bei Zöliakie ist das Brot nicht geeignet. Wer bisher wenig Ballaststoffe isst, steigert die Menge am besten langsam und trinkt genug. Anhaltende Bauchschmerzen, Blut im Stuhl, ungewollter Gewichtsverlust oder über Wochen veränderter Stuhlgang gehören ärztlich abgeklärt."))

quellen = R("quellen", "Quellen",
    q(["genussglück.design.block (Pinterest): „Roggen-Vollkornbrot – saftig & einfach“ – Rezept nach fünf Bildschirmfotos des Nutzers vom 15.11.2026; Originalseite nicht aufgerufen", ""],
      ["DGE: Ausgewählte Fragen und Antworten zu Ballaststoffen (2021)", DGE],
      ["Max Rubner-Institut: Wissenschaftliche Einordnung Ballaststoffe (Stand Juni 2026)", MRI],
      ["Deutsches Ärzteblatt: Fachgesellschaft empfiehlt Lebensmittel mit mehr Ballaststoffen", AEB],
      ["Verbraucherzentrale: Werbung mit Nährwertangaben – Vorgaben für die Hersteller", VZ],
      ["Ernährungs-Umschau 9/2010: Brot und Kleingebäck (Pentosane, Säuerung ab etwa 20 % Roggen, ballaststoffreiches Brot)", EU],
      ["Spektrum, Lexikon der Ernährung: Sauerteig", SP],
      ["dm: Roggen-Vollkornmehl, Nährwertangaben auf der Packung", DM]),
    txt("Zutaten, Mengen, Zeiten, Temperatur, der Einfrier-Tipp und die Haltbarkeit stammen aus den Bildschirmfotos des Nutzers. Die fünf Arbeitsschritte der Vorlage sind hier in acht Einzelschritte aufgeteilt und neu formuliert. Die Kaufempfehlung der Vorlage für eine Backform wurde nicht übernommen. Mit [Ergänzung] markiertes – Brotgewicht, Gesamtzeit, Hinweise zu den Schritten, Garprobe, Säure-Tipp, Varianten, Problemtabelle, Backchemie und die Überschlagsrechnung zu Ballaststoffen und Eiweiß – stammt aus allgemeinem Back- und Lebensmittelwissen und den genannten Quellen. Mehr zum Thema: {{g:brot|Getreide & Brot}}."))

e = {
    "id": "roggenvollkorn", "nr": "R-22", "titel": "Roggen-Vollkornbrot mit Kernen",
    "illu": "roggenvollkorn_bild", "fotos": [],
    "text": "Saftiges Kastenbrot aus Roggen- und Weizenvollkornmehl mit Sonnenblumenkernen, Kürbiskernen und Leinsamen. Der Teig wird nur gerührt: mischen, 60 Min. gehen lassen, in die Form füllen, 20 Min. ruhen und 50–55 Min. bei 200 °C backen.",
    "stichworte": ["Roggenbrot", "Roggen-Vollkornbrot", "Roggenvollkornbrot", "Vollkornbrot", "Körnerbrot", "Kernebrot", "Saatenbrot", "Roggenvollkornmehl", "Weizenvollkornmehl", "Trockenhefe", "Sonnenblumenkerne", "Kürbiskerne", "Leinsamen", "Haferflocken", "Kastenform", "Kastenbrot", "Brot backen", "Brot ohne Kneten", "Ballaststoffe", "darmfreundlich", "genussglück", "Pinterest"],
    "pflanzen": ["g-brot"],
    "kurz": "Roggenvollkornmehl, Weizenvollkornmehl, Trockenhefe und Salz mischen. Honig und lauwarmes Wasser zugeben und zu einem klebrigen Teig verrühren, Sonnenblumenkerne, Kürbiskerne und Leinsamen untermischen. Abgedeckt 60 Min. warm gehen lassen, in die geölte Kastenform füllen, glattstreichen, mit Haferflocken bestreuen und 20 Min. ruhen lassen. Bei 200 °C Ober-/Unterhitze 50–55 Min. backen und auf dem Gitter ganz auskühlen lassen.",
    "steckbrief": [
        ["Menge", "1 Kastenbrot [Ergänzung: ca. 900 g, geschätzt]"],
        ["Gesamtzeit", "ca. 15 Min. Vorbereitung + 60 Min. Gehzeit + 20 Min. Ruhe + 50–55 Min. Backen [Ergänzung: zusammen rund 2½ Std., dazu das Auskühlen]"],
        ["Backen", "200 °C Ober-/Unterhitze, ca. 50–55 Min., vorgeheizt"],
        ["Teig", "weicher, klebriger Rührteig aus 70 % Roggen- und 30 % Weizenvollkornmehl mit Trockenhefe, ohne Sauerteig"],
        ["Geräte", "große Schüssel, Kochlöffel, Kastenform (leicht geölt) [Ergänzung: etwa 25–30 cm lang], Tuch, Kuchengitter"],
        ["Aufbewahrung", "gut verpackt ca. 3–4 Tage; in Scheiben einfrieren"],
        ["Quelle", "genussglück.design.block auf Pinterest (Bildschirmfotos des Nutzers)"]],
    "reiter": [rezept, tipps, chemie, einordnung, quellen]}
json.dump(e, open('/home/claude/scratch/roggen/roggenvollkorn.json', 'w'), ensure_ascii=False)
print('ok', len(json.dumps(e, ensure_ascii=False)))
