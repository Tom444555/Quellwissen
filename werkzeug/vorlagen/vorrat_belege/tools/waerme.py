import json
Q={
 "ratgeber":{"t":"BBK: Vorsorgen für Krisen und Katastrophen (Ratgeber, 1. Auflage)","u":"https://www.bbk.bund.de/SharedDocs/Downloads/DE/Mediathek/Publikationen/Buergerinformationen/Ratgeber/BBK-Vorsorgen-fuer-Krisen-und-Katastrophen.pdf?__blob=publicationFile&v=44","stand":"10/2025 (gelesen über inhaltsgleiche Kopie stadtarnstein.de, abgerufen 26.11.2026)"},
 "bbkstrom":{"t":"BBK: Vorsorge und Handeln bei Stromausfall (Webseite)","u":"https://www.bbk.bund.de/DE/Warnung-Vorsorge/Vorsorge/Stromausfall/stromausfall_node.html","stand":"ohne Datum, abgerufen 26.11.2026"},
 "bbk2015":{"t":"BBK: Stromausfall – Vorsorge und Selbsthilfe (Broschüre)","u":"https://flussgebiete.nrw.de/system/files/atoms/files/bbk_stromausfall_vorsorge_u_selbsthilfe.pdf","stand":"Mai 2015"},
 "lichtenberg":{"t":"Bezirksamt Lichtenberg (Berlin): Warmes Essen trotz Stromausfall","u":"https://www.berlin.de/ba-lichtenberg/politik-und-verwaltung/beauftragte/katastrophenschutz/nachrichten/artikel.1673057.php","stand":"03.11.2026"},
 "vzn":{"t":"Verbraucherzentrale Niedersachsen: Verpflegung bei Stromausfall","u":"https://www.verbraucherzentrale-niedersachsen.de/wissen/lebensmittel/auswaehlen-zubereiten-aufbewahren/verpflegung-bei-stromausfall-vorraete-sichern-tiefkuehlkost-retten-und-ohne-strom-kochen-124714","stand":"04.08.2026"},
 "plettenberg":{"t":"Stadt Plettenberg: Notfall-Ratgeber Energieausfall","u":"https://www.plettenberg.de/krise/notfall-ratgeber/energieausfall","stand":"ohne Datum, abgerufen 26.11.2026"},
 "dachau":{"t":"Kreisbrandinspektion Dachau: Gefahren durch Kohlenstoffmonoxid","u":"https://www.kbi-dachau.de/gefahren-durch-kohlenmonoxid.html","stand":"ohne Datum, abgerufen 26.11.2026"},
 "lfstat":{"t":"Bayerisches Landesamt für Statistik: Heizwerte der Energieträger (Energiebilanz 2015)","u":"https://www.StMWi.bayern.de/fileadmin/user_upload/stmwi/Energie/Energiedaten/Energiebilanz_2015/heizwerte.pdf","stand":"21.11.2018"},
 "greet":{"t":"Argonne National Laboratory, GREET: Lower and Higher Heating Values of Gas, Liquid and Solid Fuels (Kursunterlage Univ. Illinois)","u":"https://courses.grainger.illinois.edu/npre470/sp2018/web/Lower_and_Higher_Heating_Values_of_Gas_Liquid_and_Solid_Fuels.pdf","stand":"26.08.2010"},
 "lwf":{"t":"Bayerische Landesanstalt für Wald und Forstwirtschaft: Merkblatt 20 Scheitholz","u":"https://lwf.bayern.de/mam/cms04/service/dateien/mb20_scheitholz_2025_rz_web_bf.pdf","stand":"07/2025"},
 "uds":{"t":"Universität des Saarlandes, Physik: Arbeitsblatt Wärmekapazität","u":"https://www.uni-saarland.de/fileadmin/upload/fachrichtung/physik/Schule/Waermekapazitaet-Schueler.pdf","stand":"ohne Datum, abgerufen 26.11.2026"},
 "bzfe":{"t":"BZfE (Bundeszentrum für Ernährung): Energie sparen mit der Kochkiste","u":"https://www.bzfe.de/presse/pressemeldungen-archiv/energie-sparen-mit-der-kochkiste","stand":"03.01.2023"},
 "bzfe2":{"t":"BZfE: Beim Kochen Energie und Wasser sparen","u":"https://www.bzfe.de/presse/pressemeldungen-archiv/beim-kochen-energie-und-wasser-sparen","stand":"16.10.2024"},
}
def e(id,titel,text,q,wert=None,einheit=None,warnung=None,kat=None):
    return {"id":id,"kategorie":kat,"titel":titel,"text":text,"wert":wert,"einheit":einheit,"warnung":warnung,"quelle":Q[q]}
CO="Offenes Feuer und Verbrennung in Innenräumen können unsichtbares, geruchloses Kohlenmonoxid bilden – Lebensgefahr."
E=[
 # Brennstoffe
 e("b-fluessiggas","Flüssiggas (Kartuschen)","Flüssiggas hat einen Heizwert von rund 45,4 MJ je kg, das sind etwa 12,6 kWh je kg (umgerechnet).","lfstat",12.6,"kWh je kg",kat="Brennstoffe"),
 e("b-butan","Butan","n-Butan: 45,3 MJ je kg (unterer Heizwert), etwa 12,6 kWh je kg.","greet",12.6,"kWh je kg",kat="Brennstoffe"),
 e("b-kartusche-190","Gaskartusche 190 g","Bei 12,6 kWh je kg enthalten 190 g Gas rechnerisch etwa 2,4 kWh (Richtwert, gerechnet; die Brenndauer hängt vom Brenner ab).","lfstat",2.4,"kWh (gerechnet)",kat="Brennstoffe"),
 e("b-kartusche-230","Gaskartusche 230 g","230 g Gas enthalten rechnerisch etwa 2,9 kWh (Richtwert, gerechnet).","lfstat",2.9,"kWh (gerechnet)",kat="Brennstoffe"),
 e("b-kartusche-450","Gaskartusche 450 g","450 g Gas enthalten rechnerisch etwa 5,7 kWh (Richtwert, gerechnet).","lfstat",5.7,"kWh (gerechnet)",kat="Brennstoffe"),
 e("b-ethanol","Brennspiritus (Ethanol)","Ethanol: 27,0 MJ je kg (unterer Heizwert), etwa 7,5 kWh je kg. Brennspiritus ist vergälltes Ethanol mit etwas Wasser; der Wert ist daher eine Obergrenze.","greet",7.5,"kWh je kg (Obergrenze)",kat="Brennstoffe"),
 e("b-petroleum","Petroleum","Petroleum: 42,8 MJ je kg, etwa 11,9 kWh je kg (umgerechnet).","lfstat",11.9,"kWh je kg",kat="Brennstoffe"),
 e("b-holz-kg","Brennholz je kg","Lufttrockenes Holz mit 20 % Wassergehalt: Fichte/Kiefer etwa 4,0 kWh je kg, Buche/Birke etwa 3,9 kWh je kg.","lwf",3.9,"kWh je kg (Buche, 20 % Wasser)",kat="Brennstoffe"),
 e("b-holz-rm","Brennholz je Raummeter","Bei 20 % Wassergehalt: Buche etwa 1.885 kWh, Birke 1.777, Kiefer 1.516, Fichte 1.333 kWh je Raummeter.","lwf",1885,"kWh je Raummeter (Buche)",kat="Brennstoffe"),
 e("b-holz-trocken","Nur trockenes Holz","Nur naturbelassenes, lufttrockenes Holz mit höchstens 20 % Wassergehalt verbrennen. Ungespaltenes Holz braucht bis zu 2 Jahre zum Trocknen.","lwf",20,"% Wassergehalt (höchstens)",kat="Brennstoffe"),
 e("b-wasser-1l","Energie für 1 Liter Wasser","Zum Erwärmen von 1 kg Wasser um 1 K sind 4.190 J nötig. Von 15 auf 100 °C sind das rund 356 kJ = 0,1 kWh je Liter (gerechnet, ohne Verluste; mit Kocher-Verlusten deutlich mehr).","uds",0.1,"kWh je Liter von 15 auf 100 °C (ohne Verluste)",kat="Brennstoffe"),
 e("b-gas-je-liter","Gas je Liter Wasser (Richtwert)","Rechnerisch reichen 0,1 kWh Wärme für 1 Liter; das entspricht etwa 8 g Gas ohne Verluste. Campingkocher nutzen nur einen Teil der Wärme, daher in der Praxis deutlich mehr einplanen (Richtwert, gerechnet).","lfstat",8,"g Gas je Liter (theoretisch, ohne Verluste)",kat="Brennstoffe"),
 # Innen / außen
 e("k-innen","In Innenräumen möglich","Stövchen mit Teelicht, Fondue-Set mit Brennpaste und Gaskocher, die ausdrücklich für Innenräume zugelassen sind. Ein Gasherd kann oft weiter genutzt werden.","ratgeber",kat="Kochen",warnung=CO),
 e("k-aussen","Nur im Freien","Campingkocher mit Gaskartusche, Gas- und Holzkohlegrill nur im Freien verwenden.","ratgeber",kat="Kochen",warnung="Nicht in der Wohnung oder im Haus grillen – es besteht Erstickungsgefahr."),
 e("k-haftung","Herstellerangabe beachten","Ein Gerät, das der Hersteller nur für außen zugelassen hat, drinnen zu betreiben, kann im Schadensfall als grob fahrlässig gewertet werden.","vzn",kat="Kochen"),
 e("k-gerichte","Energiesparend kochen","Eintopfgerichte mit kurzer Garzeit wählen, z. B. Getreideflocken, Couscous, Bulgur oder geschälte Hülsenfrüchte.","vzn",kat="Kochen"),
 e("k-deckel","Mit Deckel kochen","Bei fest geschlossenem Deckel entweicht kaum Dampf; Kartoffeln, Reis und Eier garen deutlich schneller.","bzfe2",kat="Kochen"),
 e("k-lueften","Lüften beim Kochen","Bei Kerzen oder Gaskochern regelmäßig lüften und offenes Feuer nie unbeobachtet lassen.","plettenberg",kat="Kochen"),
 # Kochkiste
 e("kk-prinzip","Kochkiste: Prinzip","Das Gericht kurz ankochen und im fest verschlossenen Topf in einer gut isolierten Kiste ohne weitere Energie nachgaren. Nichts brennt an oder kocht über.","bzfe",kat="Kochkiste"),
 e("kk-erbsen","Kochkiste: Erbsensuppe","Etwa 15 Minuten kochen, dann 2 bis 3 Stunden in der Kiste garen.","bzfe",15,"Minuten ankochen (dann 2–3 h Kiste)",kat="Kochkiste"),
 e("kk-milchreis","Kochkiste: Milchreis","Reis in kochende Milch einrühren und etwa 1 Stunde in der Kiste garen.","bzfe",1,"Stunde in der Kiste",kat="Kochkiste"),
 e("kk-geeignet","Kochkiste: geeignet","Geeignet sind u. a. Reis, Hirse, Quinoa, Maisgrieß, Kartoffeln, Rotkohl, Hülsenfrüchte, Hühner- und Rindfleischsuppe und Gulasch.","bzfe",kat="Kochkiste"),
 # Heizen
 e("h-kleidung","Warm bleiben","Warme Kleidung, Schuhe, Wolldecken und eine Wärmflasche bereithalten. Heiße Getränke helfen beim Aufwärmen.","plettenberg",kat="Heizen"),
 e("h-ein-raum","Nur einen Raum nutzen","Nur einen Raum beheizen, Fenster und Türen abdichten und geschlossen halten. Gelegentlich lüften, aber Zugluft vermeiden.","plettenberg",kat="Heizen"),
 e("h-lueften","Lüften trotz Kälte","Regelmäßig für wenige Minuten weit lüften – besonders bei Kerzen und Öfen.","ratgeber",kat="Heizen"),
 e("h-zugelassen","Zugelassene Geräte","Für Innenräume zugelassene Gasheizer, Ethanolkamine und Petroleumöfen funktionieren ohne Strom. Gasbetriebene Geräte brauchen Sicherheitseinrichtungen.","ratgeber",kat="Heizen",warnung="Keine Gas- oder Petroleum-Heizquellen nutzen, die nicht für Innenräume zugelassen sind."),
 e("h-kamin","Kamin- und Kachelofen","Wer einen Kamin oder Ofen hat, legt einen Vorrat an Holz, Briketts oder Kohle an. Alternative Heizquellen von Fachleuten prüfen lassen.","bbkstrom",kat="Heizen"),
 e("h-teelichtofen","Keine Teelichtöfen","Teelichtöfen nicht verwenden – es droht ein Wachsbrand.","plettenberg",kat="Heizen",warnung="Brandgefahr durch Wachsbrand."),
 e("h-grill-heizstrahler","Kein Grill und kein Heizstrahler drinnen","Holzkohlegrill oder Heizstrahler unter keinen Umständen in Wohnung oder Garage nutzen.","dachau",kat="Heizen",warnung=CO),
 e("h-elektro","Elektroheizer nicht sofort","Fällt nur die Heizung aus, elektrische Heizgeräte nicht sofort einschalten – wenn viele das gleichzeitig tun, droht eine Überlastung des Stromnetzes.","plettenberg",kat="Heizen"),
 e("co-melder","Kohlenmonoxid-Melder","Ein geprüfter CO-Melder erhöht die Sicherheit. Empfohlen sind Geräte nach EN 50291; Montage an der Decke mit mindestens 30 cm Abstand zur Wand, nicht direkt über Ofen oder Kamin.","dachau",30,"cm Abstand zur Wand (mindestens)",kat="Heizen"),
 e("co-symptome","Anzeichen einer CO-Vergiftung","Kopfschmerzen, Benommenheit und Übelkeit, später Schwindel, Verwirrtheit, Herzrasen bis Bewusstlosigkeit.","dachau",kat="Heizen"),
 e("co-alarm","Bei CO-Alarm","Gebäude sofort mit allen Personen verlassen, wenn möglich Türen und Fenster öffnen, über 112 Feuerwehr und Rettungsdienst rufen. Draußen warten, nicht zurückgehen.","dachau",kat="Heizen",warnung="Nicht ins Haus zurückgehen."),
]
data={"thema":"Wärme und Kochen ohne Strom","stand":"26.11.2026","eintraege":E,"quellen":list(Q.values()),
 "hinweis":"Energieinhalte der Kartuschen und der Wasserbedarf sind aus Heizwert bzw. Wärmekapazität gerechnet (Richtwert); tatsächliche Brenndauern hängen vom Brenner ab und stehen im Herstellerdatenblatt. Heizwerte sind untere Heizwerte. Für Trockenbrennstoff, Thermoskannen-Garen und Topf über Glut fand sich keine seriöse Quelle (siehe OFFEN.md)."}
json.dump(data,open('/home/claude/scratch/vorrat2/fakten/waerme_kochen.json','w'),ensure_ascii=False,indent=1)
print(len(E))
