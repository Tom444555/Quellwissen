import json
Q={
 "ratgeber":{"t":"BBK: Vorsorgen für Krisen und Katastrophen (Ratgeber, 1. Auflage)","u":"https://www.bbk.bund.de/SharedDocs/Downloads/DE/Mediathek/Publikationen/Buergerinformationen/Ratgeber/BBK-Vorsorgen-fuer-Krisen-und-Katastrophen.pdf?__blob=publicationFile&v=44","stand":"10/2025 (gelesen über inhaltsgleiche Kopie stadtarnstein.de, abgerufen 26.11.2026)"},
 "bbk2013":{"t":"BBK: Ratgeber für Notfallvorsorge und richtiges Handeln in Notsituationen (bereitgestellt vom Sächsischen Staatsministerium des Innern)","u":"https://www.bevoelkerungsschutz.sachsen.de/download/2013_08_Ratgeber_BBK.pdf","stand":"1. Auflage, 08/2013"},
 "bbk2015":{"t":"BBK: Stromausfall – Vorsorge und Selbsthilfe (Broschüre)","u":"https://flussgebiete.nrw.de/system/files/atoms/files/bbk_stromausfall_vorsorge_u_selbsthilfe.pdf","stand":"Mai 2015"},
 "juh":{"t":"Johanniter-Unfall-Hilfe (Landesverband Nord): Der Familien-Notfallplan","u":"https://www.johanniter.de/juh/lv-nord/unsere-jahresthemen-im-norden/bereit-fuer-alle-faelle/so-sind-sie-gut-vorbereitet/der-familien-notfallplan/","stand":"ohne Datum, abgerufen 26.11.2026"},
 "asb":{"t":"Arbeiter-Samariter-Bund: Tipps für Notlagen","u":"https://www.asb.de/unsere-angebote/asb-rettungsdienst-katastrophenschutz/tipps-fuer-notlagen","stand":"ohne Datum (© 2026), abgerufen 26.11.2026"},
 "bfr_giz":{"t":"BfR: Giftinformationszentren in Deutschland","u":"https://www.bfr.bund.de/deutsches-produktregister-depro/giftinformationszentren-in-deutschland/","stand":"22.07.2026"},
}
def f(id,titel,text,q,feldtyp,wert=None,einheit=None,warnung=None):
    return {"id":id,"feldtyp":feldtyp,"titel":titel,"text":text,"wert":wert,"einheit":einheit,"warnung":warnung,"quelle":Q[q]}
E=[
 f("treffpunkt-nah","Treffpunkt in der Nähe","Ein sicherer Treffpunkt nahe der Wohnung, z. B. ein Park oder öffentlicher Platz – für den Fall, dass nicht alle zu Hause sind und Netze ausfallen.","juh","text"),
 f("treffpunkt-fern","Treffpunkt weiter entfernt","Ein zweiter, weiter entfernter Treffpunkt für den Fall, dass die ganze Nachbarschaft geräumt wird.","juh","text"),
 f("anlaufstelle","Örtliche Anlaufstelle","Vorab wissen, wo man vor Ort Informationen bekommt, z. B. Rathaus oder Notfalltreffpunkt der Gemeinde.","ratgeber","text"),
 f("fluchtwege","Fluchtwege und Erreichbarkeiten","Mit der Familie Fluchtwege, Treffpunkte und Erreichbarkeiten besprechen.","bbk2013","text"),
 f("kontaktzeiten","Vereinbarte Kontaktzeiten","Bei Stromausfall feste Zeiten vereinbaren, zu denen man sich bei Angehörigen meldet.","asb","text"),
 f("kontakte","Kontaktliste","Familie, Freunde, Nachbarn, Kita, Schule, Arbeitsplatz. Nicht nur im Smartphone speichern.","asb","liste"),
 f("kontakte-papier","Kontaktliste auf Papier","Jedes Familienmitglied trägt eine Papierkopie bei sich, z. B. im Portemonnaie. Regelmäßig aktualisieren.","juh","haken",warnung="Smartphones und Netze können ausfallen – Papierliste ist Pflicht."),
 f("kinder-einrichtung","Kinder: Kita und Schule","Sicherstellen, dass Kita oder Schule die Familie erreichen kann, und deren Evakuierungspläne kennen: Wo wird das Kind nach einer Räumung abgeholt?","juh","text"),
 f("kinder-wer","Wer holt die Kinder?","Festlegen, wer sich um Kinder, ältere Angehörige und Haustiere kümmert.","asb","person"),
 f("kinder-ausweis","Notfallkarte für Kinder","Für Kinder einen Brustbeutel oder eine Kapsel mit Name, Geburtsdatum und Anschrift.","bbk2013","haken"),
 f("pflege","Pflegebedürftige Angehörige","Besondere Bedürfnisse, Medikamente und barrierefreie Wege einplanen. Klären, ob Hausnotruf, Pflegedienst oder Essen auf Rädern bei längerem Ausfall weiter verfügbar sind.","bbk2015","text"),
 f("notfallausweis","Notfallausweis","Angaben zu Krankheiten, Allergien, Hilfsmitteln und Notfallkontakten – auch digital auf dem Smartphone möglich.","ratgeber","text"),
 f("haustiere","Haustiere","Futter, Wasser, stabile Transportbox, Impfpass und tierärztliche Bescheinigungen bereithalten. Für größere Tiere eine Unterbringung überlegen.","juh","text"),
 f("nachbarn","Nachbarschaft","Nachbarn als Kontaktpersonen einbeziehen. Für den Ausfall von Telefon und Mobilfunk Zeichen mit Nachbarn absprechen.","bbk2013","liste"),
 f("aufgaben","Aufgabenverteilung","Jedem Familienmitglied Aufgaben geben, z. B. Kontakte aktualisieren oder Notfallausrüstung prüfen. Plan regelmäßig gemeinsam überprüfen.","juh","liste"),
 f("dokumente-ort","Ort der Dokumentenmappe","Alle Familienmitglieder wissen, wo die Dokumentenmappe liegt.","bbk2013","text"),
 f("nr-112","Notruf Feuerwehr und Rettungsdienst","112 – europaweit und kostenfrei.","ratgeber","nummer",wert=112),
 f("nr-110","Notruf Polizei","110.","ratgeber","nummer",wert=110),
 f("nr-115","Behördenrufnummer","115.","ratgeber","nummer",wert=115),
 f("nr-116117","Ärztlicher Bereitschaftsdienst","116117.","ratgeber","nummer",wert=116117),
 f("nr-gift-saar","Giftnotruf (Saarland)","Zuständig für das Saarland ist das Giftinformationszentrum Mainz: 06131 19240.","bfr_giz","nummer",wert="06131 19240"),
 f("nr-gift-andere","Giftnotruf (andere Länder)","Zuständiges Giftinformationszentrum je Bundesland aus der BfR-Liste eintragen.","bfr_giz","nummer"),
 f("nr-eigene","Eigene Nummern","Platz für Krankentransport, Apothekenbereitschaft, Stadtwerke/Netzbetreiber, Stadt- oder Gemeindeverwaltung.","ratgeber","liste"),
 f("nr-seelsorge","Telefonseelsorge","Rund um die Uhr, kostenlos, auf Wunsch anonym: 0800 111 0 111, 0800 111 0 222, 116 123.","ratgeber","nummer",wert="0800 111 0 111"),
 f("ohne-netz","Wenn 110 und 112 nicht erreichbar sind","Zur nächsten Polizeiwache oder zu einem Krankenhaus gehen.","ratgeber","haken"),
 f("nora","Notruf ohne Sprechen","Die offizielle Notruf-App nora ermöglicht einen Notruf ohne Sprechen.","ratgeber","haken"),
]
data={"thema":"Familien-Notfallplan (Felder für die App)","stand":"26.11.2026","eintraege":E,"quellen":list(Q.values()),
 "hinweis":"Feld 'feldtyp' (text, liste, person, nummer, haken) ist ein Vorschlag für die Eingabemaske und eine Ergänzung zum Grundformat. Das DRK-Angebot zum Notfallplan konnte nicht geöffnet werden; ersatzweise Johanniter und ASB (ebenfalls anerkannte Hilfsorganisationen). Die Empfehlung einer Kontaktperson außerhalb der Region ist in den gelesenen Quellen nicht enthalten."}
json.dump(data,open('/home/claude/scratch/vorrat2/fakten/notfallplan.json','w'),ensure_ascii=False,indent=1)
print(len(E))
