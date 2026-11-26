import json
Q={
 "ratgeber":{"t":"BBK: Vorsorgen für Krisen und Katastrophen (Ratgeber, 1. Auflage)","u":"https://www.bbk.bund.de/SharedDocs/Downloads/DE/Mediathek/Publikationen/Buergerinformationen/Ratgeber/BBK-Vorsorgen-fuer-Krisen-und-Katastrophen.pdf?__blob=publicationFile&v=44","stand":"10/2025 (gelesen über inhaltsgleiche Kopie stadtarnstein.de, abgerufen 26.11.2026)"},
 "warntag":{"t":"Bundesregierung: Bundesweiter Warntag","u":"https://www.bundesregierung.de/breg-de/aktuelles/bundesweiter-warntag-2383690","stand":"21.09.2026"},
 "vz_cb":{"t":"Verbraucherzentrale: Cell Broadcast – neues Warnsystem","u":"https://www.verbraucherzentrale.de/wissen/digitale-welt/mobilfunk-und-festnetz/cell-broadcast-neues-warnsystem-fuer-katastrophen-in-deutschland-77578","stand":"15.09.2026"},
 "nbg":{"t":"Stadt Nürnberg: Warn-Apps (NINA, KATWARN)","u":"https://www.nuernberg.de/internet/notfallvorsorge_katastrophenschutz/warn_apps.html","stand":"25.06.2026"},
 "sbkg":{"t":"SBKG – Saarländisches Brand- und Katastrophenschutzgesetz, §§ 2, 17 (nicht-amtliche Fassung, sadaba.de)","u":"https://www.sadaba.de/GSLT_SBKG.html","stand":"Fassung nach Änderung vom 26.06.2013, Seite aktualisiert 01.02.2014"},
 "rvsb":{"t":"Regionalverband Saarbrücken: Notfallvorsorge","u":"https://www.regionalverband-saarbruecken.de/verwaltung-politik/energie/notfallvorsorge","stand":"10.10.2025"},
 "sb_strom":{"t":"Landeshauptstadt Saarbrücken: Strom- und Gasausfall","u":"https://www.saarbruecken.de/leben_in_saarbruecken/gesundheit_sicherheit/energie/strom_und_gasausfall","stand":"ohne Datum (© 2026), abgerufen 26.11.2026"},
 "swsb":{"t":"Saarbrücker Stadtwerke: Soforthilfemaßnahmen – Stromversorgung ausgefallen","u":"https://www.saarbruecker-stadtwerke.de/media/download-636cf3281b83d","stand":"ohne Datum, abgerufen 26.11.2026"},
 "heusweiler":{"t":"Gemeinde Heusweiler: Wichtige Rufnummern","u":"https://www.heusweiler.de/rathaus-service/buergerservice/wichtige-rufnummern/","stand":"02.05.2024"},
 "quierschied":{"t":"Gemeinde Quierschied: (Öffentliche) Einrichtungen","u":"https://www.quierschied.de/rathaus-service/oeffentliche-einrichtungen","stand":"ohne Gesamtdatum, abgerufen 26.11.2026"},
 "spk_flyer":{"t":"Saarpfalz-Kreis / Arbeitsgruppe Stromausfall: Flyer Stromausfall","u":"https://www.saarpfalz-kreis.de/images/SicherheitOrdnungBauenVerkehr/Notfaelle/pdf/Stromausfall_Flyer.pdf","stand":"04/2019"},
 "homburg":{"t":"Kreis- und Universitätsstadt Homburg: Anlaufstellen der Feuerwehr bei längerem Stromausfall (Pressemitteilung)","u":"https://www.homburg.de/rathaus/aktuelle-informationen/pressemitteilungen/wie-bekomme-ich-hilfe-bei-einem-langeren-stromausfall-die-feuerwehr-bietet-anlaufstellen-fur-das-absetzen-von-notrufen/","stand":"23.12.2020"},
 "nk":{"t":"Landkreis Neunkirchen: Notfallnummern","u":"https://www.landkreis-neunkirchen.de/familien-kinder-jugendliche-senioren/notfallnummern","stand":"ohne Datum, abgerufen 26.11.2026"},
 "wd":{"t":"Wissenschaftliche Dienste des Bundestages: Katastrophenschutz in den Bundesländern – Struktur und Organisation (WD 3 - 3000 - 112/22)","u":"https://www.bundestag.de/resource/blob/916926/a4a75c813172c7ccdca7290c4c97dc82/WD-3-112-22-pdf-data.pdf","stand":"15.08.2022"},
 "bfr_giz":{"t":"BfR: Giftinformationszentren in Deutschland","u":"https://www.bfr.bund.de/deutsches-produktregister-depro/giftinformationszentren-in-deutschland/","stand":"22.07.2026"},
}
def e(id,titel,text,q,gebiet,wert=None,einheit=None,warnung=None,kat=None):
    return {"id":id,"gebiet":gebiet,"kategorie":kat,"titel":titel,"text":text,"wert":wert,"einheit":einheit,"warnung":warnung,"quelle":Q[q]}
SL="Saarland"
E=[
 # Warnwege allgemein
 e("w-sirene-warnung","Sirene: Warnung","1 Minute auf- und abschwellender Heulton: Gefahr – Radio einschalten und informieren.","ratgeber",SL,1,"Minute Heulton",kat="Warnwege"),
 e("w-sirene-entwarnung","Sirene: Entwarnung","1 Minute Dauerton: Gefahr vorbei.","ratgeber",SL,1,"Minute Dauerton",kat="Warnwege"),
 e("w-radio","Radio","Radio bleibt auch bei Ausfall von Mobilfunk und Internet nutzbar; Auto-, Kurbel- und Batterieradios funktionieren ohne Stromnetz.","ratgeber",SL,kat="Warnwege"),
 e("w-nina","Warn-App NINA","Amtliche Warnungen direkt aufs Gerät, auch Wetterwarnungen des DWD. Fällt bei Netzausfall aus.","ratgeber",SL,kat="Warnwege"),
 e("w-katwarn","Warn-App KATWARN","Übermittelt amtliche Warnungen und Verhaltenshinweise für selbst gewählte Orte; „Kritischer Alarm“ ertönt bei höchster Warnstufe auch bei stummgeschaltetem Gerät. Ob alle saarländischen Behörden KATWARN nutzen, ist nicht belegt.","nbg",SL,kat="Warnwege"),
 e("w-cellbroadcast","Cell Broadcast","Warnungen kommen als Nachricht an alle eingeschalteten Handys in der Funkzelle – ohne App und Anmeldung. Meist fünfmal im Abstand von etwa zwei Minuten; keine nachträgliche Zustellung. Reine WLAN-Tablets empfangen nichts.","vz_cb",SL,5,"Wiederholungen (meist)",kat="Warnwege"),
 e("w-cb-iphone","Cell Broadcast am iPhone","Einstellungen → Mitteilungen → ganz unten „Cell Broadcast Warnungen“. Empfang nicht abschalten.","vz_cb",SL,kat="Warnwege"),
 e("w-cb-android","Cell Broadcast bei Android","App „Nachrichten“ → Menü → Einstellungen → (Erweitert) → „Notfallbenachrichtigungen an Mobilfunkgeräte“; Bezeichnungen je nach Hersteller verschieden.","vz_cb",SL,kat="Warnwege"),
 e("w-warntag","Bundesweiter Warntag","Jährlich am zweiten Donnerstag im September gegen 11 Uhr Probewarnung, Entwarnung gegen 11:45 Uhr. Nächster Termin: 9. September 2027.","warntag",SL,11,"Uhr (Probewarnung)",kat="Warnwege"),
 e("w-anlaufstelle","Wo es vor Ort Informationen gibt","Vorab wissen, wo man vor Ort Informationen erhält, z. B. Rathaus oder Notfalltreffpunkte.","ratgeber",SL,kat="Warnwege"),
 # Zuständigkeit
 e("z-oberste","Oberste Katastrophenschutzbehörde","Das für Inneres zuständige Ministerium des Saarlandes (im Gesetzestext von 2013: Ministerium für Inneres und Sport).","sbkg",SL,kat="Zuständigkeit",warnung="Ministeriumsname kann sich geändert haben – beim Land prüfen."),
 e("z-untere","Untere Katastrophenschutzbehörden","Die Landkreise (Saarlouis, Neunkirchen, St. Wendel, Saarpfalz-Kreis, Merzig-Wadern); im Regionalverband Saarbrücken die Landeshauptstadt Saarbrücken.","sbkg",SL,kat="Zuständigkeit"),
 e("z-gemeinden","Gemeinden","Gemeinden stellen die Feuerwehr; die kommunalen Feuerwehren wirken im Katastrophenschutz mit.","sbkg",SL,kat="Zuständigkeit"),
 e("z-giftnotruf","Giftnotruf für das Saarland","Laut BfR ist das Giftinformationszentrum Mainz für das Saarland zuständig: 06131 19240.","bfr_giz",SL,"06131 19240",kat="Notrufnummern",warnung="Der Landkreis Neunkirchen nennt zusätzlich 06841 19240 – Abweichung, siehe OFFEN.md."),
 # Regionalverband Saarbrücken
 e("rv-kontakt","Regionalverband Saarbrücken","Schlossplatz 12, 66119 Saarbrücken, Telefon 0681 506-0. Seite Notfallvorsorge mit Links zu BBK und Vorratskalkulator; keine Liste von Notfalltreffpunkten veröffentlicht (Stand 10.10.2025).","rvsb","Regionalverband Saarbrücken",kat="Kontakt"),
 e("rv-vorrat","Vorratsempfehlung Regionalverband","Der Regionalverband empfiehlt Vorräte für 14 Tage (BBK: möglichst 10 Tage).","rvsb","Regionalverband Saarbrücken",14,"Tage",kat="Kontakt"),
 e("sb-stoerung","Saarbrücken: Störungshotline Stadtwerke Saarbrücken Netz","24-Stunden-Störungshotline: 0681 587-0.","sb_strom","Landeshauptstadt Saarbrücken","0681 587-0",kat="Störungsnummern"),
 e("sb-erst","Saarbrücken: Erst prüfen","Ruhe bewahren, Sicherungen prüfen und Nachbarn fragen. Ist das ganze Haus oder Wohngebiet betroffen, die Störungshotline anrufen.","swsb","Landeshauptstadt Saarbrücken",kat="Störungsnummern"),
 e("sb-treffpunkte","Saarbrücken: Notfalltreffpunkte","Auf der Seite „Strom- und Gasausfall“ der Landeshauptstadt sind keine Notfalltreffpunkte genannt; bei längerer Gasunterbrechung wird empfohlen, bei Freunden oder Verwandten unterzukommen.","sb_strom","Landeshauptstadt Saarbrücken",kat="Anlaufstellen"),
 e("heu-strom","Heusweiler: energis Störung Strom","0681 9069-2611.","heusweiler","Heusweiler","0681 9069-2611",kat="Störungsnummern"),
 e("heu-gas","Heusweiler: energis Störung Erdgas","0681 9069-2610.","heusweiler","Heusweiler","0681 9069-2610",kat="Störungsnummern"),
 e("heu-wasser","Heusweiler: Wasser","Gemeindewerke Heusweiler (06806) 98777-0; Rufbereitschaft Wasserversorgung 0681 587-5050.","heusweiler","Heusweiler","0681 587-5050",kat="Störungsnummern"),
 e("heu-leitstelle","Regionalverband: Rettungsleitstelle","Krankentransport/Rettungsleitstelle 19222 (vom Handy 0681 19222); Notruf 112.","heusweiler","Regionalverband Saarbrücken","0681 19222",kat="Notrufnummern"),
 e("qui-werke","Quierschied: Gemeindewerke Notfall","Gemeindewerke Quierschied, Rathausstraße 9: außerhalb der Arbeitszeit 06897 961-201 oder 0171 4258714. Zentrale Rathaus 06897 961-0.","quierschied","Quierschied","06897 961-201",kat="Störungsnummern"),
 e("qui-treffpunkte","Quierschied: Anlaufstellen","Die Gemeinde veröffentlicht keine Notfalltreffpunkte. Feuerwehrgerätehäuser: Löschbezirk Quierschied (Schumannstraße), Fischbach-Camphausen (Quierschieder Straße, hinter der Fischbachhalle) – deren Telefonnummern sind nicht für Alarmierungen; Notruf immer 112.","quierschied","Quierschied",kat="Anlaufstellen"),
 # Saarpfalz-Kreis
 e("spk-anlauf","Saarpfalz-Kreis: Feuerwehrgerätehaus als Anlaufstelle","Bei Stromausfall ist das Feuerwehrgerätehaus im eigenen Ort Anlaufstelle für Information und Kommunikation.","spk_flyer","Saarpfalz-Kreis",kat="Anlaufstellen"),
 e("spk-buergertelefon","Saarpfalz-Kreis: Bürgertelefon","Bürgertelefon des Saarpfalz-Kreises: 06841 104-7000. Notrufnummern nur für Notfälle, nicht für Auskünfte.","spk_flyer","Saarpfalz-Kreis","06841 104-7000",kat="Kontakt",warnung="Angabe von 2019 – vor Veröffentlichung prüfen."),
 e("spk-licht","Saarpfalz-Kreis: Lampe als Anzeige","Heiz- und Kochgeräte ausschalten, nur ein Radio oder eine Lampe als Anzeige eingeschaltet lassen. Nach dem Ausfall Geräte einzeln einschalten, feucht gewordene Geräte nicht benutzen.","spk_flyer","Saarpfalz-Kreis",kat="Anlaufstellen"),
 e("hom-mitte","Homburg: Feuerwache Homburg-Mitte","Am Hochrech 3 – Anlaufstelle zum Absetzen von Notrufen, besetzt bei großflächigem Stromausfall länger als 30 Minuten.","homburg","Homburg (Saarpfalz-Kreis)",30,"Minuten Ausfall bis zur Besetzung",kat="Anlaufstellen",warnung="Angabe von 2020 – Aktualität bei der Stadt prüfen."),
 e("hom-einoed","Homburg: Feuerwehrgerätehaus Einöd","Im Wieschen 1 a.","homburg","Homburg (Saarpfalz-Kreis)",kat="Anlaufstellen"),
 e("hom-jaegersburg","Homburg: Feuerwehrgerätehaus Jägersburg","St.-Josef-Str. 9.","homburg","Homburg (Saarpfalz-Kreis)",kat="Anlaufstellen"),
 e("hom-kirrberg","Homburg: Feuerwehrgerätehaus Kirrberg","Am Dorfplatz 8.","homburg","Homburg (Saarpfalz-Kreis)",kat="Anlaufstellen"),
 e("hom-woerschweiler","Homburg: Feuerwehrgerätehaus Wörschweiler","Bierbacher Str. 41.","homburg","Homburg (Saarpfalz-Kreis)",kat="Anlaufstellen"),
 e("hom-fahrzeuge","Homburg: Feuerwehrfahrzeuge mit Blaulicht","Zusätzlich Fahrzeuge in Reiskirchen (Am Denkmal), Bruchhof-Sanddorf (Ortsmitte), Beeden (Ortsmitte), Ingweiler (Ortsmitte), Altbreitenfeld/Websweiler.","homburg","Homburg (Saarpfalz-Kreis)",kat="Anlaufstellen"),
 # Neunkirchen
 e("nk-gift","Landkreis Neunkirchen: Giftnotruf laut Kreis","Der Landkreis nennt Giftnotruf 06841 19240 und Giftinformationszentrum 06131 19240. Zentrale Landkreis: 06824 906-0.","nk","Landkreis Neunkirchen","06824 906-0",kat="Kontakt",warnung="Abweichung zur BfR-Liste (nur Mainz) – siehe OFFEN.md."),
 # Landkreise ohne gefundene Liste
 e("sls-liste","Landkreis Saarlouis","Untere Katastrophenschutzbehörde ist der Landkreis. Eine amtliche Liste von Notfalltreffpunkten wurde nicht gefunden (Stand 26.11.2026) – bei Kreis oder Gemeinde nachfragen.","sbkg","Landkreis Saarlouis",kat="Anlaufstellen"),
 e("wnd-liste","Landkreis St. Wendel","Untere Katastrophenschutzbehörde ist der Landkreis. Eine amtliche Liste von Notfalltreffpunkten wurde nicht gefunden (Stand 26.11.2026).","sbkg","Landkreis St. Wendel",kat="Anlaufstellen"),
 e("mzg-liste","Landkreis Merzig-Wadern","Untere Katastrophenschutzbehörde ist der Landkreis. Eine amtliche Liste von Notfalltreffpunkten bei Stromausfall wurde nicht gefunden (Stand 26.11.2026).","sbkg","Landkreis Merzig-Wadern",kat="Anlaufstellen"),
 e("nk-liste","Landkreis Neunkirchen: Treffpunkte","Eine amtliche Liste von Notfalltreffpunkten wurde nicht gefunden (Stand 26.11.2026).","sbkg","Landkreis Neunkirchen",kat="Anlaufstellen"),
 # andere Bundesländer
 e("ab-gemeinde","Andere Bundesländer: Gemeinde fragen","Anlaufstellen (Rathaus, Notfalltreffpunkte) erfährt man bei der eigenen Stadt- oder Gemeindeverwaltung bzw. deren Internetseite; Behördennummer 115.","ratgeber","andere Bundesländer",115,"Behördennummer",kat="Andere Bundesländer"),
 e("ab-warn","Andere Bundesländer: Warnwege","NINA, Cell Broadcast, Radio und Sirenen gelten bundesweit; Sirenensignale sind gleich (1 Minute Heulton = Warnung, 1 Minute Dauerton = Entwarnung).","ratgeber","andere Bundesländer",kat="Andere Bundesländer"),
 e("ab-kats","Andere Bundesländer: Katastrophenschutzbehörde","Katastrophenschutz ist Ländersache; jedes Land hat eigenes Recht. Zuständig sind vor allem die unteren Katastrophenschutzbehörden, typischerweise Landkreise und kreisfreie Städte (Abweichungen z. B. Berlin, Bremen).","wd","andere Bundesländer",kat="Andere Bundesländer"),
 e("ab-gift","Andere Bundesländer: Giftnotruf","Zuständiges Giftinformationszentrum nach BfR-Liste: z. B. Berlin 030 19240, Bonn 0228 19240, Freiburg 0761 19240, Göttingen 0551 19240, Mainz 06131 19240, München 089 19240, Erfurt 0361 730730.","bfr_giz","andere Bundesländer",kat="Andere Bundesländer"),
]
data={"thema":"Region Saarland – Warnung, Anlaufstellen, Zuständigkeiten","stand":"26.11.2026","eintraege":E,"quellen":list(Q.values()),
 "hinweis":"Felder 'gebiet' und 'kategorie' sind Ergänzungen zum Grundformat. Amtliche SR-Frequenzangaben konnten nicht geöffnet werden – daher keine UKW-Frequenzen in dieser Datei (Kandidaten aus nicht-amtlicher Liste in OFFEN.md). Für Saarlouis, St. Wendel, Merzig-Wadern, Neunkirchen und die meisten Gemeinden des Regionalverbands wurde keine veröffentlichte Treffpunkt-Liste gefunden. Telefonnummern vor Veröffentlichung jährlich prüfen."}
json.dump(data,open('/home/claude/scratch/vorrat2/fakten/region_saarland.json','w'),ensure_ascii=False,indent=1)
print(len(E))
