import json
R={"t":"BBK: Vorsorgen für Krisen und Katastrophen (Ratgeber mit Checklisten, 1. Auflage)","u":"https://www.bbk.bund.de/SharedDocs/Downloads/DE/Mediathek/Publikationen/Buergerinformationen/Ratgeber/BBK-Vorsorgen-fuer-Krisen-und-Katastrophen.pdf?__blob=publicationFile&v=44","stand":"10/2025 (gelesen über inhaltsgleiche Kopie https://stadtarnstein.de/wp-content/uploads/2026/01/Ratgeber-Vorsorgen-fuer-Krisen-und-Katastrophen-des-BBK-ext.pdf, abgerufen 26.11.2026)"}
B15={"t":"BBK: Stromausfall – Vorsorge und Selbsthilfe (Broschüre)","u":"https://flussgebiete.nrw.de/system/files/atoms/files/bbk_stromausfall_vorsorge_u_selbsthilfe.pdf","stand":"Mai 2015"}
L={
 "Hausapotheke":[
  ("Persönliche Medikamente","Bei regelmäßigem Bedarf mindestens 10 Tage Vorrat.",10,"Tage (mindestens)"),
  ("Schmerzmittel und fiebersenkende Mittel",None,None,None),
  ("Fieberthermometer",None,None,None),
  ("Mittel gegen Durchfall, Erbrechen und Übelkeit",None,None,None),
  ("Mittel gegen Erkältungsbeschwerden",None,None,None),
  ("Elektrolyte","Zum Ausgleich von Flüssigkeitsverlust.",None,None),
  ("Wund- und Hautdesinfektionsmittel",None,None,None),
  ("Pflaster und Verbandsmaterial",None,None,None),
  ("Verbandtuch für Brandwunden",None,None,None),
  ("Einmalhandschuhe",None,None,None),
  ("Kühlkompresse",None,None,None),
  ("Mittel gegen Sonnenbrand und Insektenstiche",None,None,None),
  ("Abschwellendes, kühlendes Gel","Für kleine Sportverletzungen.",None,None),
  ("Abschwellende Nasentropfen oder Nasenspray",None,None,None),
  ("Pinzette",None,None,None),
  ("Schere",None,None,None),
  ("Brand-, Wund- und Heilsalbe",None,None,None),
 ],
 "Hygiene":[
  ("Zahnpasta und Zahnbürsten",None,None,None),
  ("Seife",None,None,None),
  ("Persönliche Hygieneartikel","Zum Beispiel Monatshygiene, Windeln.",None,None),
  ("Müllbeutel","Auch große, stabile Beutel zum Einhängen in die Toilette.",None,None),
  ("Toilettenpapier",None,None,None),
  ("Feuchttücher",None,None,None),
  ("Haushaltspapier",None,None,None),
  ("Desinfektionsmittel",None,None,None),
  ("Waschmittel",None,None,None),
  ("Haushaltshandschuhe",None,None,None),
  ("Campingtoilette",None,None,None),
 ],
 "Notgepäck":[
  ("Warme Kleidung, Regenschutz, feste Schuhe, Wechselkleidung",None,None,None),
  ("Dokumentenmappe",None,None,None),
  ("Bargeld",None,None,None),
  ("Persönliche Medikamente",None,None,None),
  ("Erste-Hilfe-Material",None,None,None),
  ("Hygieneartikel",None,None,None),
  ("Geladene Powerbank",None,None,None),
  ("Haltbare Lebensmittel",None,None,None),
  ("Wiederbefüllbare Trinkflasche",None,None,None),
  ("Schlafsack oder Decke",None,None,None),
  ("Essgeschirr",None,None,None),
  ("Taschenmesser und Dosenöffner",None,None,None),
  ("Taschenlampe",None,None,None),
  ("Batterie-, Solar- oder Kurbelradio",None,None,None),
  ("Feuerzeug oder Streichhölzer",None,None,None),
  ("Sonnencreme und Kopfbedeckung",None,None,None),
  ("Notizblock und Stift",None,None,None),
  ("Arbeitshandschuhe",None,None,None),
  ("Ersatz für Hilfsmittel","Zum Beispiel Brille oder Hörsysteme.",None,None),
 ],
 "Dokumente":[
  ("Identität","Zum Beispiel Geburtsurkunde, Personalausweis.",None,None),
  ("Besitz","Zum Beispiel Grundbuchauszüge, Kaufverträge.",None,None),
  ("Finanzielle Ansprüche","Zum Beispiel Versicherungen.",None,None),
  ("Qualifikationen","Zum Beispiel Schul- und Arbeitszeugnisse.",None,None),
  ("Rechte","Zum Beispiel Vollmachten, gerichtliche Entscheidungen.",None,None),
  ("Persönliche Informationen","Zum Beispiel Testament, Befunde, Impfausweis, Passwortlisten.",None,None),
  ("Emotionaler Wert","Zum Beispiel ausgewählte Fotos.",None,None),
  ("Aufbewahrung","In einem feuerfesten oder wasserdichten Behälter. Bei der ausstellenden Stelle klären, ob Original oder beglaubigte Kopie nötig ist.",None,None),
  ("Digitale Kopien","Zum Beispiel in einer Cloud, auf Festplatte oder USB-Stick.",None,None),
 ],
 "Licht, Radio, Energie":[
  ("Taschenlampe mit Ersatzbatterien",None,None,None),
  ("Kerzen und Feuerzeug",None,None,None),
  ("Kurbel- oder batteriebetriebenes Radio","Auch Solar- oder Autoradio; bleibt nutzbar, wenn Mobilfunk und Internet ausfallen.",None,None),
  ("Warn-App","Zum Beispiel NINA; fällt bei Netzausfall aus.",None,None),
  ("Powerbank",None,None,None),
  ("Papierliste mit wichtigen Telefonnummern",None,None,None),
  ("Offline-Karten","Auf dem Gerät speichern.",None,None),
  ("Warme Kleidung, Decken, Schlafsäcke",None,None,None),
  ("Netzunabhängige Heizgelegenheit mit Brennstoff",None,None,None),
 ],
 "Brandschutz":[
  ("Rauchwarnmelder","In allen Räumen außer Bad und Küche.",None,None),
  ("Feuerlöscher oder Löschspray","Brandklasse F für Fette, Wachs und flüssige Brennstoffe. Vorher mit dem Gerät vertraut machen.",None,None),
  ("Kohlenmonoxid-Melder",None,None,None),
  ("Fluchtwege kennen","Zu Hause, am Arbeitsplatz und in fremden Gebäuden.",None,None),
 ],
 "Essen und Trinken":[
  ("Trinkwasser","2 Liter je Person und Tag für 3, 5, 7 oder 10 Tage.",2,"Liter je Person und Tag"),
  ("Haltbare Lebensmittel","Für 3, 5, 7 oder 10 Tage.",10,"Tage (Ziel)"),
  ("Alternative Kochgelegenheit mit Brennstoff",None,None,None),
  ("Futtervorrat für Haustiere",None,None,None),
 ],
 "Sonstiges":[
  ("Wasserbehälter","Für Lösch- oder Brauchwasser.",None,None),
  ("Atemschutzmaske","Schutz vor Viren, Bakterien und Schadstoffen in der Luft.",None,None),
  ("Schutzhelm","Schutz vor Trümmern.",None,None),
  ("Zusätzliches Bargeld",None,None,None),
 ],
}
WARN={
 ("Brandschutz","Feuerlöscher oder Löschspray"):"Fett-, Wachs- und Flüssigbrennstoffbrände niemals mit Wasser löschen – es droht eine Fettexplosion.",
 ("Licht, Radio, Energie","Kerzen und Feuerzeug"):"Kerzen nie unbeaufsichtigt brennen lassen und für Lüftung sorgen (BBK 2015: erhöhtes Brandrisiko bei unbeaufsichtigtem Betrieb).",
}
pref={"Hausapotheke":"apo","Hygiene":"hyg","Notgepäck":"not","Dokumente":"dok","Licht, Radio, Energie":"lic","Brandschutz":"bra","Essen und Trinken":"ess","Sonstiges":"son"}
E=[]
for kat,items in L.items():
    for i,(t,txt,w,ein) in enumerate(items,1):
        E.append({"id":f"{pref[kat]}-{i:02d}","kategorie":kat,"titel":t,"text":(txt or f"{t} bereithalten (BBK-Checkliste {kat})."),"wert":w,"einheit":ein,"warnung":WARN.get((kat,t)),"quelle":R})
E.append({"id":"bra-verhalten","kategorie":"Brandschutz","titel":"Verhalten im Brandfall","text":"Nur löschen, wenn keine Gefahr besteht. Sonst Raum verlassen, Tür schließen, andere warnen, Gebäude verlassen, 112 rufen, Nachbarn warnen. Nie durch verrauchte Räume flüchten; bei verrauchtem Fluchtweg am Fenster bemerkbar machen.","wert":112,"einheit":"Notruf Feuerwehr","warnung":"Niemals durch verrauchte Räume flüchten.","quelle":R})
E.append({"id":"lic-batterien","kategorie":"Licht, Radio, Energie","titel":"Ersatzbatterien fürs Radio","text":"Batteriebetriebene Radios mit ausreichend Ersatzbatterien oder Geräte mit Dynamo- bzw. Kurbelantrieb bereithalten.","wert":None,"einheit":None,"warnung":None,"quelle":B15})
data={"thema":"Ausrüstung und Checklisten (BBK)","stand":"26.11.2026","eintraege":E,"quellen":[R,B15],
 "hinweis":"Alle Positionen aus den Checklisten des BBK-Ratgebers (10/2025), je Position eine Zeile. Der Ratgeber nennt für Hygieneartikel keine Mengen und für Lampen/Radios keine Laufzeiten – daher hier keine Werte (siehe OFFEN.md). Die Checkliste Hausapotheke ersetzt keine ärztliche Beratung; Medikamente nach Packungsbeilage bzw. ärztlicher Anweisung."}
json.dump(data,open('/home/claude/scratch/vorrat2/fakten/ausruestung.json','w'),ensure_ascii=False,indent=1)
print(len(E))
