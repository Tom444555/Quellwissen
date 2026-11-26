import json
Q={
 "protein":{"t":"DGE: FAQ Protein (Referenzwerte)","u":"https://www.dge.de/fileadmin/dok/gesunde-ernaehrung/faq/DGE-FAQ-Protein-2021.pdf","stand":"2021 (Ableitung 2017)"},
 "khfett":{"t":"DGE: Position – Richtwerte für die Energiezufuhr aus Kohlenhydraten und Fett","u":"https://www.dge.de/fileadmin/dok/wissenschaft/positionen/DGE-Positionspapier-Richtwerte-Energiezufuhr-KH-und-Fett.pdf","stand":"01/2011"},
 "ballast":{"t":"DGE: FAQ Ballaststoffe","u":"https://www.dge.de/fileadmin/dok/gesunde-ernaehrung/faq/DGE-FAQ-Ballaststoffe-2021.pdf","stand":"11/2021"},
 "vitc":{"t":"DGE/ÖGE/SGE: New Reference Values for Vitamin C Intake (Ann Nutr Metab 67:13)","u":"https://karger.com/anm/article/67/1/13/41887/New-Reference-Values-for-Vitamin-C-Intake","stand":"2015"},
 "vitcfaq":{"t":"DGE: FAQ Vitamin C","u":"https://www.dge.de/fileadmin/dok/gesunde-ernaehrung/faq/DGE-FAQ-Vitamin_C-2015.pdf","stand":"02/2015"},
 "ca":{"t":"DGE/ÖGE/SGE: New Reference Values for Calcium (Ann Nutr Metab 63:186)","u":"https://karger.com/anm/article/63/3/186/41929/New-Reference-Values-for-Calcium","stand":"2013"},
 "cafaq":{"t":"DGE: FAQ Calcium","u":"https://www.dge.de/fileadmin/dok/gesunde-ernaehrung/faq/DGE-FAQ-Calcium-2013.pdf","stand":"2013"},
 "vz_min":{"t":"Verbraucherzentrale NRW: Empfehlungen für die Mineralstoff-Versorgung (nach DGE/ÖGE-Referenzwerten, Stand 16.08.2024)","u":"https://www.verbraucherzentrale.de/sites/default/files/2024-08/empfehlungen-fuer-die-mineralstoff-versorgung-2024_08_ac.pdf","stand":"08/2024"},
 "eisen_preg":{"t":"Apotheke adhoc: Neue DGE-Referenzwerte Eisen (Schwangere, Stillende)","u":"https://www.apotheke-adhoc.de/nachrichten/detail/pta-live/weniger-eisen-fuer-schwangere-und-stillende/","stand":"05.04.2024"},
 "energie":{"t":"DGE: FAQ Energie (Richtwerte für die Energiezufuhr)","u":"https://www.dge.de/fileadmin/dok/gesunde-ernaehrung/faq/DGE-FAQ-Energie-2015.pdf","stand":"2015"},
 "ble":{"t":"BLE / ernaehrungsvorsorge.de: Vorratstabelle Mischkost (1 Person, 10 Tage)","u":"https://www.ernaehrungsvorsorge.de/fileadmin/SITE_MASTER/content/Dokumente/Anhang_3.1_Vorratstabelle_Mischkost_-_DIN_A4.pdf","stand":"2024"},
 "bevorraten":{"t":"BBK: Essen und Trinken bevorraten (Webseite)","u":"https://www.bbk.bund.de/DE/Warnung-Vorsorge/Vorsorge/So-koennen-Sie-sich-vorbereiten/Bevorraten/bevorraten_node.html","stand":"ohne Datum, abgerufen 26.11.2026"},
 "bfr":{"t":"BfR: FAQ Vitamin C steckt nicht nur in Obst und Gemüse","u":"https://www.bfr.bund.de/fragen-und-antworten/thema/vitamin-c-steckt-nicht-nur-in-obst-und-gemuese/","stand":"16.03.2026"},
 "lfl_kart":{"t":"LfL Bayern: Inhaltsstoffe Kartoffel/Süßkartoffel (Werte aus Bundeslebensmittelschlüssel BLS 3.02)","u":"https://www.lfl.bayern.de/mam/cms07/iem/dateien/inhaltsstoffe_kartoffel_süßkartoffel_kurz.pdf","stand":"27.05.2020"},
 "lfl_kohl":{"t":"LfL Bayern: Merkblatt Kohl/Sauerkraut","u":"https://www.lfl.bayern.de/mam/cms07/publikationen/daten/merkblaetter/p_20114.pdf","stand":"ohne Datum, abgerufen 26.11.2026"},
 "sw_wild":{"t":"Stiftung Warentest: Wildfrüchte – Die Vitamin-C-Bomben","u":"https://www.test.de/Wildfruechte-Die-Vitamin-C-Bomben-4137000-0/","stand":"23.09.2010, geändert 26.05.2015"},
}
def e(id,titel,text,q,wert=None,einheit=None,warnung=None,kat=None,gruppe=None):
    return {"id":id,"kategorie":kat,"gruppe":gruppe,"titel":titel,"text":text,"wert":wert,"einheit":einheit,"warnung":warnung,"quelle":Q[q]}
E=[
 # Einordnung
 e("prio-wasser","Was in 10 Tagen zuerst zählt: Wasser","Ein Mensch kann unter Umständen drei Wochen ohne Nahrung auskommen, aber nur vier Tage ohne Flüssigkeit. Wasser hat daher Vorrang.","bevorraten",4,"Tage ohne Flüssigkeit",kat="Einordnung"),
 e("prio-energie","Dann: genug Energie","Die BLE-Vorratstabelle für 10 Tage rechnet mit durchschnittlich 2.200 kcal je Person und Tag und 20 Litern Getränken.","ble",2200,"kcal je Person und Tag (Planungswert)",kat="Einordnung"),
 e("prio-vitamine","Vitamine: erst bei längerer Dauer kritisch","Ein Vitamin-C-Mangel ist hierzulande äußerst selten; erste Anzeichen sind Müdigkeit, Abwehrschwäche und Muskelschmerzen, später Zahnfleischbluten. Der Körperbestand Erwachsener liegt bei 1,5 bis 2 g Vitamin C, der tägliche Verlust bei etwa 3 % davon.","vitc",3,"% des Körperbestands Verlust je Tag (ohne Zufuhr, Größenordnung)",kat="Einordnung"),
 e("prio-skorbut","Skorbut-Schutz","Schon etwa 10 mg Vitamin C am Tag verhindern Skorbut (DGE-FAQ); die Fachveröffentlichung der DGE nennt 7 mg.","vitcfaq",10,"mg je Tag",kat="Einordnung"),
 # Energie
 e("en-m65","Energie Männer ab 65","Richtwert bei geringer körperlicher Aktivität (PAL 1,4): 2.000 kcal am Tag.","energie",2000,"kcal je Tag (PAL 1,4)",kat="Energie",gruppe="Männer ab 65"),
 e("en-w65","Energie Frauen ab 65","Richtwert bei PAL 1,4: 1.600 kcal am Tag.","energie",1600,"kcal je Tag (PAL 1,4)",kat="Energie",gruppe="Frauen ab 65"),
 e("en-j1519","Energie Jungen 15–19","Richtwert bei PAL 1,4: 2.600 kcal am Tag.","energie",2600,"kcal je Tag (PAL 1,4)",kat="Energie",gruppe="Jungen 15 bis unter 19"),
 e("en-m14","Energie Mädchen 1–4","Richtwert bei PAL 1,4: 1.100 kcal am Tag.","energie",1100,"kcal je Tag (PAL 1,4)",kat="Energie",gruppe="Mädchen 1 bis unter 4"),
 # Protein
 e("p-1-4","Eiweiß Kinder 1–4","1,0 g Eiweiß je kg Körpergewicht und Tag.","protein",1.0,"g je kg Körpergewicht und Tag",kat="Eiweiß",gruppe="Kinder 1 bis unter 4"),
 e("p-4-19","Eiweiß Kinder und Jugendliche 4–19","Der Wert sinkt mit dem Wachstum je nach Alter und Geschlecht auf 0,8 g je kg Körpergewicht und Tag.","protein",0.8,"g je kg Körpergewicht und Tag (Endwert)",kat="Eiweiß",gruppe="4 bis unter 19"),
 e("p-19-65","Eiweiß Erwachsene 19–65","0,8 g Eiweiß je kg Körpergewicht und Tag (bei Normalgewicht).","protein",0.8,"g je kg Körpergewicht und Tag",kat="Eiweiß",gruppe="Erwachsene 19 bis unter 65"),
 e("p-65","Eiweiß ab 65","1,0 g Eiweiß je kg Körpergewicht und Tag (Schätzwert).","protein",1.0,"g je kg Körpergewicht und Tag",kat="Eiweiß",gruppe="ab 65"),
 # Fett/KH/Ballast
 e("f-erw","Fettanteil Erwachsene","30 % der Energie aus Fett, bei körperlich Aktiven bis 35 %.","khfett",30,"% der Energie (30–35)",kat="Makronährstoffe",gruppe="Erwachsene"),
 e("kh-erw","Kohlenhydratanteil Erwachsene","Mehr als 50 % der Energie aus Kohlenhydraten.","khfett",50,"% der Energie (mehr als)",kat="Makronährstoffe",gruppe="Erwachsene"),
 e("b-erw","Ballaststoffe Erwachsene","Mindestens 30 g am Tag. Dazu ausreichend trinken; die Menge bei ungewohnter Kost langsam steigern.","ballast",30,"g je Tag (mindestens)",kat="Makronährstoffe",gruppe="Erwachsene"),
 e("b-kind","Ballaststoffe Kinder","Kein eigener Richtwert; zur Orientierung 14,6 g je 1.000 kcal wie bei Erwachsenen.","ballast",14.6,"g je 1.000 kcal",kat="Makronährstoffe",gruppe="Kinder und Jugendliche"),
 # Vitamin C
 e("c-1-4","Vitamin C 1–4 Jahre","20 mg am Tag.","vitc",20,"mg je Tag",kat="Vitamin C",gruppe="1 bis unter 4"),
 e("c-4-7","Vitamin C 4–7 Jahre","30 mg am Tag.","vitc",30,"mg je Tag",kat="Vitamin C",gruppe="4 bis unter 7"),
 e("c-7-10","Vitamin C 7–10 Jahre","45 mg am Tag.","vitc",45,"mg je Tag",kat="Vitamin C",gruppe="7 bis unter 10"),
 e("c-10-13","Vitamin C 10–13 Jahre","65 mg am Tag.","vitc",65,"mg je Tag",kat="Vitamin C",gruppe="10 bis unter 13"),
 e("c-13-15","Vitamin C 13–15 Jahre","85 mg am Tag.","vitc",85,"mg je Tag",kat="Vitamin C",gruppe="13 bis unter 15"),
 e("c-15-19-m","Vitamin C Jungen 15–19","105 mg am Tag.","vitc",105,"mg je Tag",kat="Vitamin C",gruppe="männlich 15 bis unter 19"),
 e("c-15-19-w","Vitamin C Mädchen 15–19","90 mg am Tag.","vitc",90,"mg je Tag",kat="Vitamin C",gruppe="weiblich 15 bis unter 19"),
 e("c-m","Vitamin C Männer","110 mg am Tag (Raucher 155 mg).","vitc",110,"mg je Tag",kat="Vitamin C",gruppe="Männer"),
 e("c-w","Vitamin C Frauen","95 mg am Tag (Raucherinnen 135 mg, Schwangere ab 4. Monat 105 mg, Stillende 125 mg).","vitc",95,"mg je Tag",kat="Vitamin C",gruppe="Frauen"),
 # Calcium
 e("ca-1-4","Calcium 1–4 Jahre","600 mg am Tag.","ca",600,"mg je Tag",kat="Calcium",gruppe="1 bis unter 4"),
 e("ca-4-7","Calcium 4–7 Jahre","750 mg am Tag.","cafaq",750,"mg je Tag",kat="Calcium",gruppe="4 bis unter 7"),
 e("ca-10-13","Calcium 10–13 Jahre","1.100 mg am Tag.","cafaq",1100,"mg je Tag",kat="Calcium",gruppe="10 bis unter 13"),
 e("ca-13-19","Calcium 13–19 Jahre","1.200 mg am Tag.","ca",1200,"mg je Tag",kat="Calcium",gruppe="13 bis unter 19"),
 e("ca-erw","Calcium Erwachsene","1.000 mg am Tag.","ca",1000,"mg je Tag",kat="Calcium",gruppe="Erwachsene"),
 # Eisen
 e("fe-m","Eisen Männer","11 mg am Tag.","vz_min",11,"mg je Tag",kat="Eisen",gruppe="Männer"),
 e("fe-w-prae","Eisen Frauen vor den Wechseljahren","16 mg am Tag.","vz_min",16,"mg je Tag",kat="Eisen",gruppe="Frauen prämenopausal"),
 e("fe-w-post","Eisen Frauen nach den Wechseljahren","14 mg am Tag; Frauen ohne Menstruation 11 mg.","vz_min",14,"mg je Tag",kat="Eisen",gruppe="Frauen postmenopausal"),
 e("fe-schwanger","Eisen Schwangere und Stillende","Schwangere 27 mg, Stillende 16 mg am Tag (DGE-Werte seit 2024).","eisen_preg",27,"mg je Tag (Schwangere)",kat="Eisen",gruppe="Schwangere"),
 # Vitamin-C-Quellen
 e("q-paprika","Rote Paprika","Etwa 140 mg Vitamin C je 100 g – mehr als der Tagesbedarf eines Erwachsenen. Vitamin C wird durch Licht bei der Lagerung und starkes Erhitzen abgebaut.","bfr",140,"mg je 100 g",kat="Vitamin-C-Quellen"),
 e("q-kartoffel-roh","Kartoffeln (lagerfähig)","Rohe, ungeschälte Kartoffeln: 18,8 mg je 100 g; geschält und gegart 14,9 mg (Bundeslebensmittelschlüssel).","lfl_kart",18.8,"mg je 100 g (roh)",kat="Vitamin-C-Quellen"),
 e("q-weisskohl","Weißkohl (lagerfähig)","Roher Weißkohl: 45 mg je 100 g. Wintersorten halten im Keller bis zu 6 Monate.","lfl_kohl",45,"mg je 100 g (roh)",kat="Vitamin-C-Quellen"),
 e("q-sanddorn","Sanddorn","Durchschnittlich 450 mg je 100 g; Sanddornsaft gehört zu den Lebensmitteln mit über 100 mg je 100 g.","sw_wild",450,"mg je 100 g",kat="Vitamin-C-Quellen"),
 e("q-hagebutte","Hagebutte","Über 1.000 mg je 100 g (frisch).","sw_wild",1000,"mg je 100 g (mehr als)",kat="Vitamin-C-Quellen"),
 e("q-portion","Beispiel-Portion","Eine halbe rote Paprika (75 g) und ein kleines Glas Orangensaft (125 ml) liefern zusammen über 155 mg Vitamin C.","vitcfaq",155,"mg (mehr als)",kat="Vitamin-C-Quellen"),
 e("q-zusatz","Zugesetztes Vitamin C","Vitamin C wird manchen Konserven, Marmeladen sowie Fleisch- und Wurstwaren als Antioxidationsmittel zugesetzt (Zutatenliste: Ascorbinsäure, E 300); Mengen werden dabei nicht angegeben.","bfr",kat="Vitamin-C-Quellen"),
]
data={"thema":"Nährstoffe im Notvorrat","stand":"26.11.2026","eintraege":E,"quellen":list(Q.values()),
 "hinweis":"Referenzwerte der DGE (D-A-CH) für gesunde Menschen; nicht für Kranke oder als Therapie. Feld 'gruppe' ist eine Ergänzung zum Grundformat. Energie-Richtwerte nur für die vier im DGE-FAQ genannten Gruppen; vollständige Tabelle und Eisen-Werte für Kinder fehlen (siehe OFFEN.md). Sauerkraut, Trockenfrüchte und Säfte ohne belegten Vitamin-C-Wert."}
json.dump(data,open('/home/claude/scratch/vorrat2/fakten/naehrstoffe.json','w'),ensure_ascii=False,indent=1)
print(len(E))
