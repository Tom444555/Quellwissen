import json
Q={
 "ratgeber":{"t":"BBK: Vorsorgen für Krisen und Katastrophen (Ratgeber, 1. Auflage)","u":"https://www.bbk.bund.de/SharedDocs/Downloads/DE/Mediathek/Publikationen/Buergerinformationen/Ratgeber/BBK-Vorsorgen-fuer-Krisen-und-Katastrophen.pdf?__blob=publicationFile&v=44","stand":"10/2025 (gelesen über inhaltsgleiche Kopie stadtarnstein.de, abgerufen 26.11.2026)"},
 "bevorraten":{"t":"BBK: Essen und Trinken bevorraten (Webseite)","u":"https://www.bbk.bund.de/DE/Warnung-Vorsorge/Vorsorge/So-koennen-Sie-sich-vorbereiten/Bevorraten/bevorraten_node.html","stand":"ohne Datum, abgerufen 26.11.2026"},
 "wassi":{"t":"BBK: Maßnahmen der Wassersicherstellung (Webseite)","u":"https://www.bbk.bund.de/DE/Themen/Kritische-Infrastrukturen/Sektoren-Branchen/Wasser/Wassersicherstellung/wassersicherstellung_node.html","stand":"ohne Datum, abgerufen 26.11.2026"},
 "bbkflyer":{"t":"BBK: Flyer Trinkwasser-Notversorgung (bereitgestellt von der Feuerwehr Mainz)","u":"https://www.mainz.de/microsite/feuerwehr/medien/bindata/Flyer_Trinkwasser.pdf","stand":"© BBK 2016"},
 "who":{"t":"WHO/SEARO Technical Note for Emergencies No. 9: Minimum water quantity needed for domestic uses (B. J. Reed, WEDC)","u":"https://www.slideshare.net/slideshow/who5-minimum-water-quantity-needed-for-domestic-use/48638611","stand":"ohne Jahresangabe im Dokument, abgerufen 26.11.2026"},
 "sphere":{"t":"Sphere-Standards: Water supply standard 1 (Mindestwassermenge)","u":"https://interactive.spherestandards.org/","stand":"ohne Jahresangabe auf der Seite, abgerufen 26.11.2026"},
 "uba":{"t":"Umweltbundesamt: Empfehlungen zum Umgang mit Abweichungen nach Trinkwasserverordnung (Vollzug §§ 62–68 TrinkwV), Anhang A.3 Empfehlung Abkochgebot","u":"https://www.umweltbundesamt.de/system/files/document/260417_UBA_Empfehlungen_%C2%A7%C2%A762-68_nach_Freigabe_final_clean.pdf","stand":"Februar 2026 (redaktionelle Änderungen 04/2026)"},
 "cdcsafe":{"t":"CDC (USA): How to Make Water Safe in an Emergency","u":"https://cdc.gov/water-emergency/about","stand":"19.09.2024"},
 "cdcstore":{"t":"CDC (USA): How to Create and Store an Emergency Water Supply","u":"https://cdc.gov/water-emergency/about/how-to-create-and-store-an-emergency-water-supply.html","stand":"geprüft 27.06.2025"},
 "cdcfind":{"t":"CDC (USA): How to Find Clean Water in an Emergency","u":"https://www.cdc.gov/water-emergency/about/how-to-find-clean-water-in-an-emergency.html","stand":"25.06.2025"},
 "bb":{"t":"Ministerium des Innern und für Kommunales Brandenburg: Wenn der Strom ausfällt … (Ratgeber)","u":"https://mik.brandenburg.de/sixcms/media.php/9/Broschure_Blackout.pdf","stand":"April 2016"},
}
def e(id,titel,text,q,wert=None,einheit=None,warnung=None,kat=None):
    return {"id":id,"kategorie":kat,"titel":titel,"text":text,"wert":wert,"einheit":einheit,"warnung":warnung,"quelle":Q[q]}
E=[
 # Bedarf
 e("bedarf-trinken","Trinken","Ein Erwachsener braucht mindestens 1,5 Liter Flüssigkeit am Tag.","bevorraten",1.5,"Liter je Person und Tag (Minimum)",kat="Bedarf"),
 e("bedarf-kochen","Kochen","Wer kochen möchte, plant 0,5 Liter Wasser zusätzlich ein.","bevorraten",0.5,"Liter je Person und Tag",kat="Bedarf"),
 e("bedarf-vorrat","Vorratsrichtwert BBK","Richtwert für den Vorrat: 2 Liter je Person und Tag (Trinken und Kochen). Haustiere zusätzlich einplanen.","ratgeber",2,"Liter je Person und Tag (Richtwert)",kat="Bedarf"),
 e("bedarf-beispiel","Beispiel 3 Personen","Für 3 Personen: 18 Liter für 3 Tage, 30 Liter für 5 Tage, 60 Liter für 10 Tage.","ratgeber",60,"Liter (3 Personen, 10 Tage)",kat="Bedarf"),
 e("bedarf-ohne","Ohne Flüssigkeit","Ein Mensch kann unter Umständen drei Wochen ohne Nahrung auskommen, aber nur vier Tage ohne Flüssigkeit.","bevorraten",4,"Tage (ohne Flüssigkeit, Größenordnung)",kat="Bedarf"),
 e("bedarf-who-ueberleben","Überlebensmenge (international)","Die WHO nennt als Mindestmenge für wenige Tage 7 Liter je Person und Tag: 3–4 Liter zum Trinken und 2–3 Liter für Essenszubereitung.","who",7,"Liter je Person und Tag (nur wenige Tage)",kat="Bedarf"),
 e("bedarf-who-hygiene","Körperpflege","Für die Körperpflege rechnet die WHO bei längerer Notlage mit 6–7 Litern je Person und Tag, für Wäsche mit 4–6 Litern.","who",6,"Liter je Person und Tag (6–7, Körperpflege)",kat="Bedarf"),
 e("bedarf-sphere","Mindestmenge in Hilfseinsätzen","Internationale Hilfsstandards (Sphere) sehen mindestens 15 Liter je Person und Tag für den Haushalt vor.","sphere",15,"Liter je Person und Tag",kat="Bedarf"),
 e("bedarf-notbrunnen","Notversorgung in Deutschland","Die staatliche Trinkwasser-Notversorgung (z. B. Notbrunnen) plant mit 15 Litern je Person und Tag. Normal sind es etwa 120 Liter.","wassi",15,"Liter je Person und Tag (Notversorgung)",kat="Bedarf"),
 e("bedarf-toilette","Spültoilette braucht viel Wasser","Toiletten mit Wasserspülung brauchen laut WHO bis zu 70 Liter je Person und Tag. In der Notlage daher sparsam spülen oder Alternativen nutzen.","who",70,"Liter je Person und Tag (bis zu, Spültoilette)",kat="Bedarf"),
 # Notquellen
 e("quelle-wannen","Wasser auffangen, solange es fließt","Badewanne und saubere, lebensmittelechte Kanister füllen. Badewannenwasser vor allem für die Toilettenspülung.","bb",kat="Notquellen"),
 e("quelle-boiler","Warmwasserspeicher","Wasser aus dem Warmwasserspeicher der Trinkwasseranlage ist eine Notquelle. Nicht gemeint ist der Kessel bzw. die Heizungsanlage.","cdcfind",kat="Notquellen",warnung="Wasser aus Heizkörpern oder dem Heizkessel niemals zum Trinken, Kochen oder für die Körperpflege verwenden."),
 e("quelle-spuelkasten","Spülkasten","Wasser aus dem Spülkasten (nicht aus dem WC-Becken) ist nutzbar, wenn es klar ist und keine Reinigungsmittel enthält, die das Wasser färben.","cdcfind",kat="Notquellen"),
 e("quelle-eis","Eiswürfel","Geschmolzene Eiswürfel sind nutzbar, wenn sie aus einwandfreiem Wasser hergestellt wurden.","cdcfind",kat="Notquellen"),
 e("quelle-regen","Regenwasser","Regenwasser und andere Wasserquellen im Freien müssen vor dem Trinken behandelt werden, damit Krankheitserreger abgetötet werden.","cdcfind",kat="Notquellen"),
 e("quelle-pool","Pool-Wasser","Wasser aus Pools und Whirlpools ist für Körperpflege und Reinigung nutzbar, aber nicht zum Trinken.","cdcfind",kat="Notquellen"),
 e("quelle-chemie","Verunreinigtes Wasser","Wasser mit Treibstoff, giftigen Chemikalien oder radioaktiven Stoffen lässt sich durch Abkochen oder Entkeimen nicht trinkbar machen.","cdcsafe",kat="Notquellen",warnung="Solches Wasser nicht trinken und nicht zum Waschen verwenden; anderes Wasser nutzen und das Gesundheitsamt fragen."),
 # Aufbereitung
 e("auf-abkochen","Abkochen","Wasser einmal sprudelnd aufkochen und danach mindestens 10 Minuten abkühlen lassen. Ein Wasserkocher eignet sich gut.","uba",10,"Minuten abkühlen (nach sprudelndem Aufkochen)",kat="Aufbereitung",warnung="Erst handwarm verwenden: Kinder, alte und kranke Menschen bemerken heißes Wasser oft nicht – Verbrühungsgefahr."),
 e("auf-abkochen-international","Abkochen – internationale Angabe","Die US-Gesundheitsbehörde CDC empfiehlt, klares Wasser 1 Minute sprudelnd kochen zu lassen (oberhalb von etwa 2000 m Höhe 3 Minuten). Trübes Wasser vorher durch ein sauberes Tuch oder einen Kaffeefilter gießen.","cdcsafe",1,"Minute sprudelnd kochen",kat="Aufbereitung"),
 e("auf-wofuer","Wofür abgekochtes Wasser","Bei Abkochgebot abgekocht verwenden für: Trinken, Zähneputzen, Eiswürfel, Waschen und Zubereiten von Obst, Gemüse und ungekochten Speisen sowie Körperpflege bei Kleinkindern, Kranken und Immungeschwächten.","uba",kat="Aufbereitung"),
 e("auf-ausnahmen","Wofür nicht zwingend","Toilettenspülung, Duschen, Wäsche ab 40 °C und Spülmaschine ab 60 °C kommen nach UBA kurzzeitig ohne Abkochen aus. Offene Wunden beim Waschen wasserdicht abdecken, Hände gründlich mit Seife waschen.","uba",kat="Aufbereitung"),
 e("auf-tabletten","Entkeimungstabletten","Chlor-, Chlordioxid- oder Iodtabletten genau nach Packungsangabe verwenden. Sie töten Bakterien und Viren, aber nicht unbedingt Parasiten; gegen Cryptosporidien wirkt nur Chlordioxid bei richtiger Anwendung.","cdcsafe",kat="Aufbereitung",warnung="Dosierung ausschließlich nach Packungsangabe. Iod nicht in der Schwangerschaft, bei Schilddrüsenerkrankungen oder Iod-Überempfindlichkeit, und von niemandem länger als einige Wochen."),
 e("auf-filter","Wasserfilter","Tragbare Filter mit absoluter Porengröße von 1 Mikrometer oder kleiner halten Parasiten zurück, 0,3 Mikrometer oder kleiner auch Bakterien. Viren entfernen sie nicht – danach zusätzlich chemisch entkeimen.","cdcsafe",1,"Mikrometer Porengröße (höchstens, gegen Parasiten)",kat="Aufbereitung",warnung="Filter machen chemisch verunreinigtes Wasser nicht sicher."),
 e("auf-gefaesse","Aufbereitetes Wasser aufbewahren","Abgekochtes oder entkeimtes Wasser in sauberen, desinfizierten Behältern mit dicht schließendem Deckel aufbewahren.","cdcsafe",kat="Aufbereitung"),
 # Lagern
 e("lager-tausch","Leitungswasser lagern","Selbst abgefülltes Leitungswasser alle 6 Monate austauschen. Gekauftes Wasser nach Mindesthaltbarkeitsdatum.","cdcstore",6,"Monate (Austauschintervall)",kat="Lagern"),
 e("lager-behaelter","Geeignete Behälter","Am besten lebensmittelechte Behälter mit dicht schließendem Deckel, aus bruchsicherem Material (kein Glas), möglichst mit enger Öffnung.","cdcstore",kat="Lagern",warnung="Keine Behälter verwenden, in denen giftige Stoffe (z. B. Bleichmittel, Pflanzenschutzmittel) waren."),
 e("lager-ort","Lagerort","Kühl (etwa 10–21 °C), ohne direkte Sonne und entfernt von Benzin, Pflanzenschutzmitteln und anderen giftigen Stoffen lagern.","cdcstore",21,"°C (höchstens, Bereich 10–21 °C)",kat="Lagern"),
 e("lager-mineral","Ein Teil als Mineralwasser","Ein Teil des Vorrats sollte aus gekauftem (Mineral-)Wasser bestehen.","bevorraten",kat="Lagern"),
 # Toilette
 e("wc-beutel","Toilette ohne Wasser","Große, stabile Müllbeutel in die Toilette einhängen oder eine Campingtoilette nutzen. Toilettenpapier, Feuchttücher und Haushaltshandschuhe bereithalten.","ratgeber",kat="Toilette"),
 e("wc-spuelen","Mit Brauchwasser spülen","Die Toilette lässt sich mit gesammeltem Brauchwasser, z. B. aus der Badewanne, spülen.","bb",kat="Toilette"),
 e("wc-behaelter","Wasserbehälter für Brauchwasser","Das BBK nennt Wasserbehälter für Lösch- oder Brauchwasser in seiner Checkliste.","ratgeber",kat="Toilette"),
]
data={"thema":"Wasser im Notfall","stand":"26.11.2026","eintraege":E,"quellen":list(Q.values()),
 "hinweis":"Deutsche Behörden (BBK, UBA) zuerst; wo diese zu Notquellen, Filtern und Lagerdauer keine Angaben machen, wurde die US-Gesundheitsbehörde CDC sowie WHO/Sphere herangezogen – in der App als internationale Angabe kennzeichnen. Abkochen: UBA nennt sprudelndes Aufkochen ohne Mindestdauer plus mindestens 10 Minuten Abkühlen; CDC nennt 1 Minute sprudelnd kochen. Feld 'kategorie' ist eine Ergänzung zum Grundformat. Keine Dosierangaben für Entkeimungsmittel – immer nach Packungsangabe."}
json.dump(data,open('/home/claude/scratch/vorrat2/fakten/wasser.json','w'),ensure_ascii=False,indent=1)
print(len(E))
