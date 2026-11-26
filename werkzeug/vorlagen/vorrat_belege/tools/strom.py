import json
Q={
 "sw_ps":{"t":"Stiftung Warentest: Mobile Stromspeicher im Test (Powerstations)","u":"https://www.test.de/news/Mobile-Stromspeicher-im-Test-Beste-Powerstation-im-Test-kostet-nur-520-Euro-6273250-0/","stand":"07.01.2026 (Tests aus 2023)"},
 "sw_pb":{"t":"Notebookcheck: Powerbanks im Warentest (Bericht über test 02/2022)","u":"https://www.notebookcheck.com/Powerbanks-im-Warentest-Das-sind-die-besten-Zusatzakkus-fuer-Handy-Tablet-und-Notebook.595602.0.html","stand":"26.01.2022"},
 "techtest":{"t":"Techtest.org: mAh- und Wh-Angabe bei Powerbanks (3,7 V oder 5 V)","u":"https://techtest.org/mah-und-wh-angabe-bei-powerbanks-37v-oder-5v/","stand":"19.06.2022"},
 "vzrlp_router":{"t":"Verbraucherzentrale Rheinland-Pfalz: Internetrouter – Netz in der Nacht?","u":"https://www.verbraucherzentrale-rlp.de/20-prozent-weniger-stromverbrauch-nr4-internetrouter-netz-in-der-nacht-82406","stand":"ohne Datum (© 2026), abgerufen 26.11.2026"},
 "vzrlp_pumpe":{"t":"Verbraucherzentrale Rheinland-Pfalz: Energietipp Heizungspumpe (veröffentlicht von VG Lingenfeld)","u":"https://www.vg-lingenfeld.de/neuigkeiten/2025/mai/energietipp-hohes-einsparpotenzial-beim-tausch-der-alten-heizungspumpe/","stand":"Pressemitteilung 20.05.2025"},
 "oeko":{"t":"Öko-Institut / Verbraucherzentrale RLP: Energieverbrauch von Kühl- und Gefriergeräten (Infoblatt)","u":"https://www.oeko.de/uploads/oeko/forschung_beratung/themen/nachhaltiger_konsum/infoblatt_kuehlschrank.pdf","stand":"09/2012 (alte Effizienzklassen A+++ bis A)"},
 "uba_kuehl":{"t":"Umweltbundesamt: Umwelttipps Kühlschrank","u":"https://umweltbundesamt.de/umwelttipps-fuer-den-alltag/elektrogeraete/kuehlschrank","stand":"14.07.2026"},
 "uba_gefrier":{"t":"Umweltbundesamt: Umwelttipps Gefriertruhe, Gefrierschrank","u":"https://www.umweltbundesamt.de/umwelttipps-fuer-den-alltag/elektrogeraete/gefriertruhe-gefrierschrank","stand":"14.07.2026"},
 "uba_lampen":{"t":"Umweltbundesamt: Lampen und Leuchten (Energieverbrauchskennzeichnung)","u":"https://www.umweltbundesamt.de/themen/klima-energie/energiesparen/energieverbrauchskennzeichnung/lampen-leuchten","stand":"09.08.2024"},
 "vz_steckersolar":{"t":"Verbraucherzentrale: FAQ zu Steckersolar-Geräten","u":"https://www.verbraucherzentrale.de/wissen/energie/erneuerbare-energien/faq-zu-steckersolargeraeten-das-sind-die-haeufigsten-fragen-86652","stand":"06.03.2026"},
 "bbk2015":{"t":"BBK: Stromausfall – Vorsorge und Selbsthilfe (Broschüre)","u":"https://flussgebiete.nrw.de/system/files/atoms/files/bbk_stromausfall_vorsorge_u_selbsthilfe.pdf","stand":"Mai 2015"},
 "hd":{"t":"Feuerwehr Heidelberg: Stromausfall","u":"https://www.heidelberg.de/Feuerwehr,Len/feuerwehr/Berufsfeuerwehr/stromausfall.html","stand":"ohne Datum, abgerufen 26.11.2026"},
 "bern":{"t":"Kanton Bern, Amt für Bevölkerungsschutz, Sport und Militär: Technische Daten Notstromaggregat klein (Inverter-Benzinstromerzeuger 1,8 kW)","u":"https://www.bsm.sid.be.ch/content/dam/bsm_sid/dokumente/de/bev%C3%B6lkerungsschutz/ntp/material/Technische-Daten_Notstromaggregat_klein_Honda-EU22i-de.pdf","stand":"ohne Datum, abgerufen 26.11.2026"},
 "bbkstrom":{"t":"BBK: Vorsorge und Handeln bei Stromausfall (Webseite)","u":"https://www.bbk.bund.de/DE/Warnung-Vorsorge/Vorsorge/Stromausfall/stromausfall_node.html","stand":"ohne Datum, abgerufen 26.11.2026"},
}
def e(id,titel,text,q,wert=None,einheit=None,warnung=None,kat=None):
    return {"id":id,"kategorie":kat,"titel":titel,"text":text,"wert":wert,"einheit":einheit,"warnung":warnung,"quelle":Q[q]}
E=[
 # Verbraucher
 e("v-smartphone","Smartphone-Ladung","Eine Powerstation mit 500 Wh lädt laut Stiftung Warentest ein Smartphone rund 33-mal. Daraus ergeben sich etwa 15 Wh je Ladung einschließlich Verlusten (abgeleiteter Richtwert).","sw_ps",15,"Wh je Ladung (Richtwert, abgeleitet)",kat="Verbraucher"),
 e("v-laptop","Laptop-Ladung","Dieselbe 500-Wh-Powerstation lädt einen Laptop etwa 10-mal – rund 50 Wh je Ladung einschließlich Verlusten (abgeleiteter Richtwert). Der genaue Wert hängt vom Akku ab (auf dem Akku oder im Datenblatt in Wh angegeben).","sw_ps",50,"Wh je Ladung (Richtwert, abgeleitet)",kat="Verbraucher"),
 e("v-lichterkette","Lichterkette","Eine Lichterkette leuchtet an einer 500-Wh-Powerstation laut Warentest-Berechnung 65 Stunden.","sw_ps",65,"Stunden an 500 Wh",kat="Verbraucher"),
 e("v-led","LED-Lampe","Der Verbrauch steht auf Verpackung oder Energielabel in kWh je 1.000 Stunden; dieser Wert entspricht der Leistung in Watt. Zum Vergleich: Eine 60-W-Glühlampe gibt rund 710 Lumen ab, LED-Lampen brauchen dafür deutlich weniger.","uba_lampen",kat="Verbraucher"),
 e("v-router","WLAN-Router","Ein Internetrouter braucht etwa 10 bis 20 Watt, im Dauerbetrieb rund 90 bis 180 kWh im Jahr. Das sind etwa 0,24 bis 0,48 kWh am Tag (umgerechnet).","vzrlp_router",15,"W (Bereich 10–20 W)",kat="Verbraucher"),
 e("v-kgk-neu","Kühl-Gefrier-Kombi, sparsam","Eine sparsame Kühl-Gefrierkombination (250 l/90 l, alte Klasse A+++) brauchte 157 kWh im Jahr, also etwa 0,43 kWh am Tag (umgerechnet).","oeko",0.43,"kWh je Tag",kat="Verbraucher"),
 e("v-kgk-alt","Kühl-Gefrier-Kombi, Altgerät","Ein etwa 12 Jahre altes Gerät gleicher Größe brauchte 392 kWh im Jahr, also etwa 1,07 kWh am Tag (umgerechnet).","oeko",1.07,"kWh je Tag",kat="Verbraucher"),
 e("v-kuehl-klein","Kleiner Kühlschrank, sparsam","Kleine Kühlgeräte der besten (alten) Klasse A+++ lagen bei knapp 100 kWh im Jahr, etwa 0,27 kWh am Tag (umgerechnet).","oeko",0.27,"kWh je Tag",kat="Verbraucher"),
 e("v-gefrier-hoch","Gefrierschrank mit hohem Verbrauch","Das UBA rät, einen Gefrierschrank ab etwa 430 kWh im Jahr (ökologisch) bzw. 570 kWh (wirtschaftlich) zu ersetzen. 430 kWh entsprechen rund 1,2 kWh am Tag (umgerechnet).","uba_gefrier",1.18,"kWh je Tag (Schwellenwert, umgerechnet)",kat="Verbraucher"),
 e("v-gefriertruhe","Truhe statt Schrank","Gefriertruhen sind etwa 12 % sparsamer als Gefrierschränke.","oeko",12,"% weniger Verbrauch",kat="Verbraucher"),
 e("v-temp","Temperaturen","7 °C im Kühlschrank und −18 °C im Gefriergerät reichen aus.","uba_kuehl",7,"°C Kühlschrank (−18 °C Gefriergerät)",kat="Verbraucher"),
 e("v-pumpe-alt","Heizungspumpe, alt","Alte, ungeregelte Heizungsumwälzpumpen brauchen 60 bis 100 Watt.","vzrlp_pumpe",80,"W (Bereich 60–100 W)",kat="Verbraucher"),
 e("v-pumpe-neu","Heizungspumpe, Hocheffizienz","Hocheffizienzpumpen brauchen durchschnittlich etwa 15 Watt.","vzrlp_pumpe",15,"W (Durchschnitt)",kat="Verbraucher"),
 e("v-waermegeraete","Wärmegeräte","Wärmeerzeugende Geräte (Heizlüfter, Wasserkocher, Herdplatte) brauchen je Gerät schnell 1.500 bis 2.000 Watt – zu viel für die meisten Notstromlösungen.","bbk2015",2000,"W (1.500–2.000 W je Gerät)",kat="Verbraucher"),
 e("v-medizin","Medizinische Geräte","Wer auf strombetriebene Geräte angewiesen ist (z. B. Atemtherapie-, Sauerstoff- oder Absauggeräte), klärt Laufzeit, Akku und Notstromlösung mit Arzt, Pflegedienst und Hersteller. Die App nennt dafür bewusst keine Werte.","bbk2015",kat="Verbraucher",warnung="Keine eigenen Bastellösungen für lebenswichtige Geräte – Absprache mit Arzt und Hersteller."),
 # Speicher
 e("s-formel","Powerbank: mAh in Wh","Powerbanks werden meist in mAh bei 3,7 V Zellspannung angegeben. Umrechnung: Wh = mAh × 3,7 ÷ 1.000. Beispiel: 10.000 mAh = 37 Wh.","techtest",3.7,"V (Zellspannung für Umrechnung)",kat="Speicher"),
 e("s-powerbank-real","Powerbank: tatsächlich nutzbar","Im Warentest (2022) lieferten Powerbanks mit 10.000 bzw. 20.100 mAh Nennkapazität 8.400 bis 17.680 mAh – rund 73 bis 90 % der Angabe (umgerechnet). Für Planungen etwa zwei Drittel bis drei Viertel ansetzen (Richtwert).","sw_pb",0.75,"Faktor nutzbar (Richtwert, gemessen 0,73–0,90)",kat="Speicher"),
 e("s-powerstation-usb","Powerstation: lieber USB als Steckdose","Die Umwandlung in 230-V-Wechselstrom frisst Energie. Geräte daher möglichst per USB laden – das bedeutet geringere Wandlungsverluste.","sw_ps",kat="Speicher"),
 e("s-powerstation-solar","Powerstation und Solar","Alle getesteten Powerstations lassen sich mit Solarmodulen laden. Als Zwischenspeicher für Balkonkraftwerke sind sie wenig geeignet, weil sie nicht ins Hausnetz einspeisen.","sw_ps",kat="Speicher"),
 # Solar
 e("pv-ertrag-jahr","Solarertrag im Jahr","Ein 400-Wp-Modul liefert bei optimaler, unverschatteter Südausrichtung und 30° Neigung rund 400 kWh im Jahr – also etwa 100 kWh je 100 Wp bzw. 1.000 kWh je kWp (Richtwert, Deutschland).","vz_steckersolar",100,"kWh je 100 Wp und Jahr (Richtwert)",kat="Solar"),
 e("pv-stromausfall","Balkonkraftwerk bei Stromausfall","Ohne Netz funktioniert ein Steckersolargerät nicht: Der Wechselrichter braucht die Netzverbindung und schaltet ab.","vz_steckersolar",kat="Solar"),
 e("pv-speicher","Inselbetrieb nur mit Speicher","Manche Batteriespeicher können bei Netzausfall in den Inselbetrieb umschalten und sich weiter mit den Modulen laden. Für Anwendungen ganz ohne Netz braucht es Inselsysteme mit Batterie und Laderegler.","vz_steckersolar",kat="Solar"),
 e("pv-grenzen","Erlaubte Größe","Der Wechselrichter darf höchstens 800 Watt abgeben; die Modulleistung darf bis 2.000 Wp betragen.","vz_steckersolar",800,"W Wechselrichter (Module bis 2.000 Wp)",kat="Solar"),
 # Notstrom
 e("g-verbrauch","Stromerzeuger: Kraftstoff je kWh","Beispiel-Datenblatt eines kleinen Inverter-Stromerzeugers: 1,8 kW Dauerleistung, 3,6 l Tank, 3,35 Stunden Laufzeit bei Dauerleistung. Das ergibt rund 0,6 Liter Benzin je kWh unter Volllast (abgeleiteter Richtwert); im Sparbetrieb läuft eine Tankfüllung 10,5 Stunden.","bern",0.6,"l Benzin je kWh (Richtwert, abgeleitet)",kat="Notstrom"),
 e("g-draussen","Stromerzeuger nur im Freien","Stromerzeuger nur an einem gut belüfteten, trockenen Platz im Freien betreiben.","bbk2015",kat="Notstrom",warnung="Niemals in Wohnung, Haus, Keller oder Garage betreiben – giftige Abgase, Erstickungsgefahr."),
 e("g-tanken","Betanken","Beim Betanken und durch heiße Anlagenteile besteht Brandgefahr. Im Keller höchstens 10 kg Benzin bzw. 20 kg Diesel in geeigneten Kanistern lagern, Gas gar nicht.","bbk2015",10,"kg Benzin im Keller höchstens (Diesel 20 kg)",warnung="Brandgefahr beim Betanken und an heißen Anlagenteilen.",kat="Notstrom"),
 e("g-einspeisen","Einspeisung ins Hausnetz","Die Einspeisung in die Hausinstallation darf nur ein Elektrofachbetrieb einrichten, über einen Umschalter; Netzbetreiber und Stromlieferant sind vorher zu informieren. Einzelne Geräte können über Verlängerungskabel angeschlossen werden.","bbk2015",kat="Notstrom",warnung="Einspeisung ins Hausnetz nur durch einen Elektrofachbetrieb mit Umschalter."),
 e("g-laerm","Lärm","In dicht besiedelten Gebieten oder Mehrfamilienhäusern ein leises Gerät wählen.","bbk2015",kat="Notstrom"),
 e("g-heidelberg","Feuerwehr-Hinweis","Campingkocher und Stromerzeuger nur im Freien benutzen.","hd",kat="Notstrom"),
 e("a-akkus","Akkus vorab laden","Akkus von Laptops, Handys und Telefonen geladen halten; Solar-Ladegeräte oder Powerbanks bereithalten.","bbkstrom",kat="Speicher"),
]
data={"thema":"Strom ohne Netz – Verbrauch, Speicher, Solar, Notstrom","stand":"26.11.2026","eintraege":E,"quellen":list(Q.values()),
 "hinweis":"Werte mit 'abgeleitet' oder 'umgerechnet' sind aus den Quellangaben gerechnet (z. B. Jahres- in Tageswerte, 500 Wh ÷ 33 Ladungen) und als Richtwert zu kennzeichnen. Kühlgeräte-Werte stammen von 2012 mit alten Effizienzklassen (A+++ bis A); neue Klassen A–G (seit 2021) sind nicht direkt vergleichbar. Monatliche Solarerträge (Winter/Sommer, Südwestdeutschland) aus PVGIS fehlen noch – siehe OFFEN.md. Gerätename im Stromerzeuger-Datenblatt bewusst weggelassen (keine Markenempfehlung)."}
json.dump(data,open('/home/claude/scratch/vorrat2/fakten/strom.json','w'),ensure_ascii=False,indent=1)
print(len(E))
