# -*- coding: utf-8 -*-
# Erzeugt folge.json für „Epstein, 9/11 & Pandemie – Zufall oder System? | Dr. Heiko Schöning“
# (K = schoening, Sammelstelle A-12 realtalk)
import json, os
K = 'schoening'; G = 'Schöning Epstein und 9/11'
URL = 'https://www.youtube.com/watch?v=Y9lDINwHK1E'
TITEL = 'Epstein, 9/11 & Pandemie – Zufall oder System? | Dr. Heiko Schöning'
GAST = 'Heiko Schöning'
DATUM = '2026 ❓'
DAUER = '1 Std. 56 Min.'
HILFE = 'Wer an Suizid denkt, findet rund um die Uhr Hilfe bei der Telefonseelsorge: 0800 111 0 111.'

# ---------- Quellen (alle geprüft) ----------
Q = dict(
 fbi='[FBI: Amerithrax or Anthrax Investigation (Famous Cases)](https://www.fbi.gov/about-us/history/famous-cases/anthrax-amerithrax)',
 doj='[US-Justizministerium (19.02.2010): Formal Conclusion of Investigation into 2001 Anthrax Attacks](https://www.justice.gov/opa/pr/2010/February/10-nsd-166.html)',
 nas='[National Academies (15.02.2011): Science Alone Does Not Establish Source of Anthrax Used in 2001 Mailings](https://www.nationalacademies.org/news/2011/02/science-alone-does-not-establish-source-of-anthrax-used-in-2001-mailings)',
 politico='[Politico Magazine (Sept. 2016), Garrett M. Graff: ‘We’re the Only Plane in the Sky’](https://www.politico.com/magazine/story/2016/09/were-the-only-plane-in-the-sky-214230)',
 politico2='[9/11 Memorial & Museum: Transkript „The Only Plane in the Sky“ (19.09.2019, PDF)](https://m.911memorial.org/sites/default/files/inline-files/Transcript%20-%20Only%20Plane%20in%20the%20Sky%2020190919.pdf)',
 heritage='[Heritage Foundation (06.04.2020): National Coronavirus Recovery Commission Launches](https://www.heritage.org/press/national-coronavirus-recovery-commission-launches-save-lives-and-livelihoods)',
 medicago='[CBC (02/2023): Quebec-based COVID-19 vaccine maker Medicago to shut down](https://www.cbc.ca/1.6735521)',
 hauerwp='[Wikipedia: Jerome Hauer](https://en.wikipedia.org/wiki/Jerome_Hauer)',
 hauerem='[Emergent BioSolutions (16.08.2023): Statement Regarding the Passing of a Director of the Board](https://www.emergentbiosolutions.com/?p=4548)',
 darkwinter='[Johns Hopkins Center for Health Security: Dark Winter (22.–23.06.2001)](https://www.centerforhealthsecurity.org/our-work/events-archive/2001_dark-winter/)',
 emergent='[US-Repräsentantenhaus, Ausschüsse (10.05.2022): Report on Emergent BioSolutions](https://oversightdemocrats.house.gov/news/press-releases/committees-report-on-emergent-biosolutions-uncovers-extensive-vaccine)',
 nist='[NIST: Questions and Answers about the NIST WTC 7 Investigation](https://www.nist.gov/property-fieldsection/questions-and-answers-about-nist-wtc-7-investigation)',
 uaf='[University of Alaska Fairbanks, INE: A Structural Reevaluation of the Collapse of World Trade Center 7](https://ine.uaf.edu/wtc7)',
 f93='[AP via Fox News (01.06.2018): Remaining wreckage of Flight 93 to be buried at memorial](https://www.foxnews.com/us/remaining-wreckage-of-flight-93-to-be-buried-at-memorial)',
 epstein='[Mississippi Free Press/AP (30.01.2026): Justice Department says it’s releasing 3 million pages from its Epstein files](https://www.mississippifreepress.org/justice-department-says-its-releasing-3-million-pages-from-its-epstein-files/)',
 cow='[Brown University, Costs of War: Human Costs](https://costsofwar.watson.brown.edu/costs/human)',
 imec='[Weißes Haus (09.09.2023): MoU on the Principles of an India–Middle East–Europe Economic Corridor](https://bidenwhitehouse.archives.gov/briefing-room/statements-releases/2023/09/09/memorandum-of-understanding-on-the-principles-of-an-india-middle-east-europe-economic-corridor/)',
 kushner='[JTA (22.01.2026): Jared Kushner presents plan for ‘New Gaza’ at Davos](https://www.jta.org/2026/01/22/israel/jared-kushner-presents-plan-for-new-gaza-at-davos-as-trump-launches-board-of-peace-with-israel-absent)',
 baud='[Berliner Zeitung (15.12.2025): EU verhängt Sanktionen gegen Schweizer Ex-Oberst Baud](https://www.berliner-zeitung.de/article/eu-verhaengt-sanktionen-gegen-schweizer-ex-oberst-baud-franzosen-und-us-amerikaner-10010377)',
 austria='[vienna.at (07.07.2022): Nationalrat – Abschaffung der Corona-Impfpflicht](https://www.vienna.at/nationalrat-abschaffung-der-corona-impfpflicht/7523020)',
 destatis='[Destatis, Pressemitteilung Nr. 056 (20.02.2026): China im Jahr 2025 wieder wichtigster Handelspartner Deutschlands](https://www.destatis.de/DE/Presse/Pressemitteilungen/2026/02/PD26_056_51.html)',
 owidmil='[Our World in Data: Military expenditure (SIPRI, konstante US-$ 2024)](https://ourworldindata.org/grapher/military-spending-sipri)',
 owiducdp='[Our World in Data: Deaths in armed conflicts by region (UCDP)](https://ourworldindata.org/grapher/deaths-in-armed-conflicts-by-region)',
)
import re
def lnk(k):
    m = re.match(r'\[(.*)\]\((.*)\)', Q[k]); return [m[1], m[2]]

WIS = '{{a:realtalk-wisnewski|Wisnewski zu 9/11}}'
REGTR = '{{a:regenauer-trump|Regenauer: Trump und Epstein}}'
POHL = '{{a:realtalk-pohlmannschmidt|Pohlmann: Geheimdienste}}'
REG = '{{a:regenauer|Tom-Oliver Regenauer (A-11)}}'
GAN = '{{a:ganser|Daniele Ganser (A-04)}}'

# ---------- Themen ----------
THEMEN = [
 {'k':'a','n':'Corona-Vorhersage & Pandemie'},
 {'k':'b','n':'9/11'},
 {'k':'c','n':'Anthrax & Bruce Ivins'},
 {'k':'d','n':'Akteure: Tubb, Hauer, Emergent'},
 {'k':'e','n':'Epstein & Erpressung'},
 {'k':'m','n':'Medien, Besitz, Zensur & Kultur'},
 {'k':'f','n':'Geopolitik: Gaza, IMEC, Deutschland'},
 {'k':'w','n':'Persönliches & Organisatorisches'},
]

# ---------- Abschnitte: (von, bis, emoji+titel, th, liste) ----------
AB = []
def ab(von, bis, titel, th, *liste):
    AB.append((von, bis, titel, th, list(liste)))

ab('0:00','0:03','🎬 Begrüßung in Kreuzberg und ein KI-Steckbrief','w',
 '**Zusammenfassung:** Der Gastgeber von REALTALK (Name im Video nicht genannt ❓) begrüßt Heiko Schöning zum ersten Mal; man kenne sich über gemeinsame Bekannte und ein Telefonat. Schöning freut sich, in seiner „alten Heimat“ Berlin-Kreuzberg 36 zu sein, und bittet, ihn nicht „Doktor“, sondern einfach Arzt zu nennen; man einigt sich auf „Du“. Der Gastgeber lässt eine KI einen Steckbrief vorlesen: Mediziner, ehemaliger Offizier, Kritiker der Corona-Maßnahmen, Mitgründer von „Ärzte für Aufklärung“, kaum Biografisches dokumentiert.',
 '📌 Der Gastgeber sagt, REALTALK sei „seit 2019“ am Start; frühere Gäste: Eva Herman, Florian Homm [0:00–0:02].',
 '📌 Die KI erwähnt laut Vorlesung auch Äußerungen zu 9/11 und „globalen Eliten“ sowie Vorwürfe, die ihm daraus gemacht würden – das ist der vorgelesene KI-Text, keine Wertung dieser Auswertung [0:03].')

ab('0:03','0:06','🔮 „Corona vorhergesagt“ – das Interview von 2018/2019','a',
 '**Zusammenfassung:** Schöning sagt, der wichtigste Punkt fehle im KI-Text: Er habe Corona Monate vorher angekündigt. In einem Interview mit Ken Jebsen (KenFM), aufgenommen im Dezember 2018 „in einem Berliner Keller“ und ausgestrahlt im September 2019, habe er gesagt, Kriminelle planten für 2020 eine weltweite Pandemie, danach heiße es, alle sollten sich impfen lassen. Der Gastgeber hat das Interview nach eigenen Worten auf Odysee ganz angesehen: Es sei „keine direkte Vorhersage“ der Ereignisse gewesen, aber „sehr nah“ an dem, was später kam.',
 '💬 „für das Jahr 2020 planen Kriminelle eine weltweite Pandemie“ (Schöning) [0:04]',
 '📌 Begründung laut Schöning: die Aufnahme sei „Lebensversicherung“ für ihn und seine Familie gewesen, weil das Thema zu brisant war [0:04] [seine Sicht].',
 '❓ Das Interview selbst wurde für diese Auswertung nicht eingesehen; Wortlaut und Datum (laut Schöning ausgestrahlt am 11.09.2019 [0:43]) sind nicht geprüft.')

ab('0:06','0:09','📺 KenFM, Apolut und Ken Jebsen','m',
 '**Zusammenfassung:** Laut Schöning wurde das Interview 300.000–400.000 Mal angesehen, bevor es gelöscht wurde. Als 2020 die Pandemie begann, sei KenFM „nicht wirklich da“ gewesen; es folgten das Rebranding zu „Apolut“ und ein Namenswechsel des Journalisten. Der Gastgeber würdigt KenFM als wichtigstes alternatives Medium und wünscht sich 2026 ein Comeback, „rasiert im Anzug, im Keller“.',
 '📌 Der Gastgeber nennt Ernst Wolff als einen der Beteiligten, die im Schatten Jebsens gestanden hätten; Jebsen trage heute seinen Passnamen [0:08].',
 '📌 Schöning: Jebsen habe vor 2019 „so viel Gutes geleistet“; er wünsche ihm „ganz konstruktiv“ alles Gute [0:07–0:08].')

ab('0:09','0:12','🔗 Warum 9/11, Anthrax und Corona zusammengehören sollen','a',
 '**Zusammenfassung:** Nach einem Exkurs zu „Herr Lehmann“ (Sven Regener; Anrede „Herr Schöning“ plus „Du“) fragt der Gastgeber, warum 9/11, Anthrax und Covid heute noch wichtig seien. Schöning antwortet mit „Effizienz“: Wer wisse, dass die Pandemie von Kriminellen geplant gewesen sei, müsse nicht zum „Hobby-Immunologen“ werden, sondern frage, wer das vorhergesagt habe und mit welchen Belegen.',
 '📌 9/11 habe „unser Leben verändert weltweit“; wer es zu deuten wisse, spare Zeit, Geld und Nerven [0:10–0:11] [seine Sicht].',
 '📌 Belege stünden „in Buchform mit ganz vielen Quellen“ – gemeint sind seine Bücher „Game Over“ [0:12].')

ab('0:12','0:15','🕵️ „Eine Mafia“ – 9/11 als Ausgangspunkt','b',
 '**Zusammenfassung:** Wenn Kriminelle dahinterstünden, könne man sich „die ganze Medizin eigentlich sparen“ – man habe es mit einer kriminellen Organisation zu tun. Das sei schon 2001 bei den Anschlägen vom 11. September so gewesen. Schöning lebte damals in Kreuzberg, sei „erst drauf reingefallen“, dann über physikalische Fragen zu Zweifeln gekommen und habe sich auf den biologischen Teil, den Erreger *Bacillus anthracis*, konzentriert. 2026 sei der 25. Jahrestag; die vier Flugzeuge und die Anthrax-Anschläge gehörten „integral zusammen“.',
 '💬 „Ich habe es eigentlich hier mit einer Mafia zu tun“ (Schöning) [0:13]',
 '📌 Der Gastgeber räumt ein, viele würden die Bücher nicht lesen, und bittet um eine kurze Zusammenfassung [0:14–0:15].')

ab('0:15','0:18','✉️ Lebenslauf und die Anthrax-Briefe von 2001','c',
 '**Zusammenfassung:** Schöning stellt sich vor: aufgewachsen in einer Hansestadt in Westdeutschland, Bundeswehr mit abgeschlossener Offiziersausbildung, Medizinstudium an der Charité, Stationen in Australien und England, Notfallmedizin. Dann erklärt er die Anthrax-Anschläge (Milzbrand): Sporen als weißes Pulver in Briefen an Medienleute und Parlamentarier, fünf Tote, Schließung von Parlamentsgebäuden, anfangs Verdacht gegen den Irak. 2008 habe das FBI einen Einzeltäter benannt, der sich zuvor das Leben genommen habe.',
 '📌 Fünf Tote [0:16] – deckt sich mit den Angaben des FBI (siehe Abgleich).',
 '📌 Die vier Flugzeuge: WTC 1 und 2, Pentagon, Shanksville [0:17]; die Anthrax-Briefe seien „zeitgleich“ gewesen [0:17–0:18] [seine Sicht].',
 '📚 **Ergänzung:** Das FBI schloss den Fall „Amerithrax“ am 19.02.2010 formell ab (Täter laut FBI: Bruce Ivins). Hinweis: Schöning spricht hier und später ausführlich über die Umstände von Ivins’ Tod; die Auswertung gibt dazu bewusst keine Einzelheiten wieder. ' + HILFE)

ab('0:18','0:21','🧪 Bruce Ivins und der Zweifel des Arztes','c',
 '**Zusammenfassung:** Die Briefe hätten weltweit Panik ausgelöst; sogar eine ältere Frau „in der Provinz“ sei gestorben. Als Arzt habe er an der amtlichen Darstellung gezweifelt: Ein Mikrobiologe aus einem Biowaffenlabor wähle diese Todesart nicht – er vergleicht das mit einem Formel-1-Fahrer, der mit dem Fahrrad gegen einen Baum fährt. Der Mann sei Dr. Bruce Ivins gewesen; dessen Foto sei schon im KenFM-Interview gezeigt worden, das als DVD im Buch „Game Over“ liege.',
 '📌 Er habe die FBI-Daten über Jahre gesammelt und den „verdächtigen Selbstmord aufgeklärt“ [0:20] [seine Sicht].',
 '📌 Nebenbei: „Bill Gates, Microsoft … alle mit dabei damals schon“ [0:19] – was damit gemeint ist, bleibt offen ❓.',
 '📚 **Ergänzung:** Laut FBI nahm sich Ivins das Leben, bevor Anklage erhoben werden konnte. ' + HILFE)

ab('0:21','0:24','⚖️ Schönings Einwände – und ein Vorwurf an Edwin Meese','c',
 '**Zusammenfassung:** Schöning trägt Einwände gegen die amtliche Darstellung von Ivins’ Tod vor (Statistik, Krankheitsverlauf, Behandlung; Einzelheiten werden hier bewusst nicht wiedergegeben). Das FBI habe Ivins seit Monaten rund um die Uhr überwacht und „ihn da sterben lassen“. Weil er belegen könne, wer den Fall vertuscht habe, werde er „unkenntlich gemacht“ – der Gastgeber habe erst vor Wochen von ihm erfahren.',
 '📌 Schöning nennt als Verantwortlichen für die Vertuschung Edwin Meese, den er als „de facto Personalchef von Donald Trump“ bezeichnet [0:23] [seine Sicht] – ein Vorwurf gegen eine lebende Person; Belege dafür wurden in den geprüften Quellen nicht gefunden ❓.',
 '💬 „das Vertuschen ist eine aktive Tat“ (Schöning) [0:22]',
 '📚 **Ergänzung:** Die National Academies stellten 2011 fest, Wissenschaft allein könne die Herkunft der Sporen nicht abschließend klären (siehe Abgleich). ' + HILFE)

ab('0:24','0:27','🛰️ Überwachung nach 9/11 und die Frage nach dem Motiv','b',
 '**Zusammenfassung:** Der Gastgeber verweist auf ein früheres Gespräch Schönings bei {ungeskriptet}: Ohne 9/11 gäbe es Programme wie „Total Information Awareness“ nicht, die bis zu Palantir, Überwachung und Transhumanismus führten. Schöning erklärt ABC-Waffen und betont, er sei Arzt und Reserveoffizier mit Offizierspatent. Auf die Frage, warum er als Arzt Mordfälle aufklären wolle, antwortet er: „Relevanz“ – und eigentlich sei er „faul“.',
 '📌 Gastgeber: „Wir wissen alle ganz genau, dass da die Geheimdienste dahinter gesteckt haben“ (zu Überwachungsprogrammen) [0:24] [seine Sicht].',
 '🔗 Zu Geheimdiensten im Kompendium: ' + POHL + '.')

ab('0:27','0:30','🎭 „Marionetten“, Familie und die Angst vor dem Unbekannten','w',
 '**Zusammenfassung:** Schöning sieht Politiker wie Lauterbach, Merz oder Scholz als „Marionetten“; er kenne Abgeordnete und Minister persönlich, gute Leute gebe es „nicht so weit oben“. Horst Seehofer habe einmal gesagt, in der Politik gebe es keine Freundschaften. Als Vater habe er seine Kinder schützen können, weil er von der Planung gewusst habe; sie seien „angstfrei“ aufgewachsen. Wissen nehme Angst; die Mächtigen seien „Mittelmaß“, wie Mafia-Familien.',
 '📌 Er sei seit fast 20 Jahren glücklich verheiratet; der öffentliche Druck auf die Familie sei groß gewesen [0:29].')

ab('0:30','0:33','📚 Whitney Webb und die Epstein-Akten','e',
 '**Zusammenfassung:** Der Gastgeber grüßt Schönings Frau Gesa Schöning, die Whitney Webb interviewt hat, und empfiehlt Webbs „One Nation Under Blackmail“ (deutsch „Eine Nation unter Erpressung“, zwei Bände) als „Standardwerk“: Erpressungsstrukturen beherrschten die Welt seit mindestens 150–200 Jahren. Schöning: Seine Frau habe das Werk übersetzen lassen und im eigenen Verlag herausgebracht. Die von der Trump-Regierung freigegebenen „Millionen Seiten“ der Epstein-Akten nennt er „Opium und Hopium fürs Volk“ – das Wichtige stehe nicht drin.',
 '💬 „Das ist kein gerichtetes Feuer“ (Schöning über die Aktenflut) [0:33]',
 '📚 **Ergänzung:** Das US-Justizministerium veröffentlichte am 30.01.2026 mehr als 3 Mio. Seiten, über 2.000 Videos und 180.000 Bilder; Teile wurden zum Schutz möglicher Opfer und laufender Ermittlungen zurückgehalten oder geschwärzt.',
 '🔗 Siehe auch ' + REGTR + '.')

ab('0:33','0:39','🗝️ Erpressung, Präsidenten – und die Bücher „Game Over“','e',
 '**Zusammenfassung:** Statt Millionen Seiten lieber zweimal 500 Seiten Webb lesen: Band 1 erkläre, woher das Netzwerk um Epstein komme, Band 2 das Sexualnetzwerk und die Erpressungsmethoden. Der Gastgeber vermutet, US-Präsidenten, die nicht „eine Kugel in den Kopf bekommen“ hätten (er nennt Andrew Jackson und Abraham Lincoln als Gegenbeispiele), gehörten zum Erpressungskomplex; auch Trump könne erpressbar sein. Ein Irankrieg stehe „vor der Haustür“, die Zeichen stünden „auf orange-rot“. Schöning bewirbt seine Bücher „Game Over“ (Band 1: Covid-19 und Anthrax; Band 2: „Angriff aufs Mikrobiom“) samt DVDs im Buchdeckel.',
 '📌 Gastgeber: Sensationslust gelte Namen wie Jay-Z, Beyoncé oder „P. Diddy“ (Hörfehler im Transkript ❓); die Bücher gingen tiefer [0:36].',
 '📌 Schöning: Dieselben Strukturen erklärten Gaza, Israel und warum Europa „runtergefahren“ werde [0:36–0:37] [seine Sicht].',
 '📌 Band 2 handle von Bakterien und Antibiotika; das Thema Mikrobiom wird auf ein späteres Gespräch verschoben [0:37], [1:53].')

ab('0:39','0:42','💽 Schweigen statt Widerlegung – Besitz statt Cloud','m',
 '**Zusammenfassung:** Schöning sagt, in seinen Büchern sei „kein großer Fehler“ nachgewiesen worden; stattdessen werde geschwiegen, „Zersetzung wie Stasi“. Andere Journalisten und Podcaster ruft er zu mehr Mut auf. Der Gastgeber knüpft an: Bücher und DVDs bedeuteten Besitz; mit Blick auf Klaus Schwabs „Ihr werdet nichts besitzen“ erklärt er das an Spielen (Super-Nintendo-Modul statt Cloud), Musik (Schallplatte) und Filmen (Kauf bei Amazon Prime als bloße Lizenz).',
 '📌 Der Gastgeber nennt Manova als Partnermedium und REALTALK als Plattform für Jüngere [0:40].')

ab('0:42','0:48','🚫 Sanktionierte Publizisten, Maduro und abschaltbare Technik','m',
 '**Zusammenfassung:** Bücher seien „wichtiger als je zuvor, solange man sie noch kaufen darf“. Schöning nennt Thomas Röper, Alina Lipp und den Schweizer Ex-Offizier Jacques Baud: deren Bücher dürfe man nicht mehr verkaufen, niemand dürfe ihnen helfen – „ohne Gerichtsurteil“, per Dekret der EU-Kommission. Als Beispiel für abschaltbare Technik nennt er die Festnahme des venezolanischen Präsidenten Maduro im Januar 2026: Russische und chinesische Abwehrsysteme hätten „digital“ nicht funktioniert – „nur mit Verrat“ möglich. Der Gastgeber ergänzt Grundeinkommen, Social-Credit-Systeme und erzählt die „Black Mirror“-Folge über Bewertungspunkte nach.',
 '📌 Laut Schöning flogen „angeblich 150“ Fluggeräte nach Venezuela, rund 100 Menschen seien getötet worden [0:44] – Zahlen hier nicht geprüft ❓.',
 '📚 **Ergänzung:** Die Sanktionen gegen Baud beschloss am 15.12.2025 der Rat der EU (Einreiseverbot, Einfrieren von Vermögen); für Röper und Lipp wurde die Listung hier nicht geprüft ❓.',
 '💬 „Online gehört uns nicht“ (Schöning) [0:43]')

ab('0:48','0:51','♟️ „Kein Prophet, ich bin Arzt“ – Rudern und Schach','w',
 '**Zusammenfassung:** Auf den Begriff „prophezeit“ entgegnet Schöning, er habe nur seine kriminalistischen Recherchen dargelegt und Personen und Firmen benannt – „mehr Mathematik als Prophezeiung“. Er sei „Sitzsportler“: Ruderer (gerade bei den Deutschen Ruder-Ergometer-Meisterschaften gewesen) und Schachspieler; je komplizierter ein Fall, desto mehr reize er ihn. Es gehe um „Erwachsensein“ statt Ablenkung wie mit einer Babyrassel.',
 '📌 Kartenspiel: Schöning verweist auf ein Kartenspiel mit Personen aus seinen Büchern [0:49], [1:07], [1:40].')

ab('0:51','0:54','🔥 „Biochemischer Reichstagsbrand“ und Patriot Act','c',
 '**Zusammenfassung:** Ken Jebsen habe im Dezember 2018 gefragt, ob ein „biochemischer Reichstagsbrand“ bevorstehe. Schöning deutet den Reichstagsbrand 1933 als „Anschlag unter falscher Flagge“ mit einem bestraften Einzeltäter – wie Ivins bei Anthrax. Auf die Anthrax-Briefe sei ein „quasi Ermächtigungsgesetz“ gefolgt, der Patriot Act von 2001, rund 500 Seiten, ungelesen unterschrieben; zwei Senatoren hätten sich geweigert und dann Anthrax-Briefe erhalten.',
 '📌 Teile des Patriot Act beschnitten bis heute Bürgerrechte [0:53] [seine Sicht].',
 '📚 **Ergänzung:** Der Patriot Act wurde am 26.10.2001 unterzeichnet. Die Deutung des Reichstagsbrands als „falsche Flagge“ ist Schönings Sicht; die Frage der Täterschaft (Einzeltäter Marinus van der Lubbe oder Beteiligung der NSDAP) wird in der Forschung bis heute diskutiert ❓ (hier nicht vertieft).')

ab('0:54','0:57','🏛️ Daschle, Leahy, Powell – und WTC 7 als Einstieg','b',
 '**Zusammenfassung:** Die beiden Senatoren seien Tom Daschle und Patrick Leahy gewesen; „danach haben die zugestimmt“. Den Anthrax-Fall habe man dem Irak zugeschrieben; 2003 habe Colin Powell im UN-Sicherheitsrat ein Röhrchen hochgehalten (Schöning nennt ihn „Verteidigungsminister“ – Powell war Außenminister 📚). Der Gastgeber leitet zu 9/11 über und fragt, ob Schöning glaube, dass kein Flugzeug ins Pentagon flog. Schöning empfiehlt als „einfachsten Weg“ WTC 7: kein Flugzeug, 180 m hohes Stahlskelett, Einsturz im „freien Fall“.',
 '💬 „Ich bin hundertprozentig unabhängig“ (Schöning) [0:55]',
 '📌 Gastgeber: Durch Epstein-Veröffentlichungen fielen auch Begriffe wie Israel und Geheimdienstoperationen im Zusammenhang mit 9/11 [0:56] [seine Sicht].')

ab('0:57','1:00','🏢 Fallzeit von WTC 7 und das Loch in Shanksville','b',
 '**Zusammenfassung:** Ein Gegenstand falle aus 180 m in etwa 7 Sekunden; WTC 7 sei in etwa 7½ Sekunden eingestürzt – ohne Gegendruck, „bis auf den Grundriss“. Zu Flug 93 bei Shanksville (Pennsylvania): Das Loch sei kleiner als ein Flugzeug gewesen; ein WDR-Journalist habe den Bürgermeister interviewt, der gesagt habe, es sei kein Flugzeug zu sehen gewesen. Auch der Coroner habe keine Leichen gesehen; die offizielle Version, das Flugzeug sei wie „ins Moor“ eingedrungen, hält er für unglaubwürdig.',
 '📌 Größtes Wrackteil „so groß wie ein Telefonbuch“, laut Polizisten und Lokaljournalisten [1:00] [seine Sicht].',
 '📚 **Ergänzung:** NIST misst für die Nordfassade 5,4 Sekunden für 18 Stockwerke, darin 2,25 Sekunden freier Fall; die Überreste aller 40 Menschen an Bord von Flug 93 wurden identifiziert (siehe Abgleich).')

ab('1:00','1:03','📰 Wisnewski, Heritage Foundation und eine Corona-Kommission','b',
 '**Zusammenfassung:** Die WDR-Reportage sei rund eine Million Mal gesehen, aber nie wiederholt worden; der Journalist sei „fertig gemacht“ und entlassen worden, der „Spiegel“ habe nachgelegt – gemeint ist Gerhard Wisnewski. Der Gastgeber sagt, Christoph Hörstel habe ihm Wisnewski empfohlen. Schöning: Edwin Meese und die Heritage Foundation hätten auch eine Pandemie vorbereitet; im April 2020 habe Heritage eine Coronavirus-Kommission gebildet (Website „coronaviruscommission.com“, später gelöscht) mit einem Fahrplan zu Lockdown, Masken und Wiedereröffnung. Mitglied: Dr. Richard Tubb.',
 '📌 Die Kommission habe „Vorwissen“ gehabt [1:02] [seine Sicht].',
 '📚 **Ergänzung:** Heritage gab die „National Coronavirus Recovery Commission“ am 06.04.2020 bekannt; Tubb steht auf der Liste („Retired Brigadier General; White House Physician Emeritus“), Meese nicht. Die genannte Website und die Löschung wurden nicht geprüft ❓.',
 '🔗 Wisnewski im Kompendium: ' + WIS + '.')

ab('1:03','1:06','✈️ Richard Tubb und das Antibiotikum an Bord der Air Force One','d',
 '**Zusammenfassung:** Für Schöning ist dies „der wichtigste Punkt“: Tubb, Leibarzt von George W. Bush, sei am 11.09.2001 in der Air Force One von Sitz zu Sitz gegangen und habe den Mitarbeitern das Antibiotikum Ciprofloxacin gegen Anthrax gegeben – wegen eines möglichen Anthrax-Risikos in der Schule in Florida, die Bush besucht hatte. Quelle sei Politico („The Only Plane in the Sky“). Niemand habe damals von Anthrax wissen können; erst Wochen später sei der Erreger beim ersten Opfer gefunden worden. Daraus folgert er „kriminelles Vorwissen“.',
 '💬 „Das habe ich mir nicht zusammen konfabuliert“ (Schöning zur Quelle) [1:05]',
 '📌 Laut Schöning eine Ration für „60 Tage“ [1:04] [seine Sicht].',
 '📚 **Ergänzung:** In der Politico-Oral-History sagt Tubb, er habe sich am meisten um einen „biologischen“ Angriff gesorgt und allen an Bord „eine Woche“ Cipro gegeben; ein Mitarbeiter zitiert ihn mit „In case it’s anthrax“. Vorwürfe gegen Tubb: Aussage Schönings, keine Feststellung einer Behörde oder eines Gerichts bekannt ❓.')

ab('1:06','1:12','💉 Vom Leibarzt zur Tabakfirma? Medicago und der Pflanzen-Impfstoff','d',
 '**Zusammenfassung:** Das erste Anthrax-Opfer sei am „6. Oktober 2001“ gestorben (📚 Robert Stevens, gest. 05.10.2001). Das Antibiotikum habe starke Nebenwirkungen, man gebe es der Regierung „nur mit einem gesichertem Verdacht“ [seine Sicht]. Tubb sei danach Wissenschaftsvorstand bei British American Tobacco geworden und habe die Biotech-Firma Medicago gekauft, die aus Tabakpflanzen einen Corona-Impfstoff herstellte. Der Impfstoff sei zugelassen worden, die Firma dann an Mitsubishi verkauft und „eingestampft“ worden – trotz möglicher Milliardengewinne.',
 '📌 Schöning nennt Tubb die „Hauptfigur“; der Gastgeber sagt, die Verbindung Tubb–Covid höre er zum ersten Mal [1:08], [1:11].',
 '📚 **Ergänzung:** Laut CBC gehörte Medicago zuletzt ganz Mitsubishi Tanabe Pharma; Philip Morris International war Anteilseigner und verkaufte Ende 2022. Health Canada ließ den Impfstoff 2022 zu, die WHO lehnte eine Notfallzulassung wegen der Tabakverbindung ab; Anfang 2023 kündigte Mitsubishi Chemical die Schließung an. Eine Tätigkeit Tubbs bei British American Tobacco wurde in den geprüften Quellen nicht gefunden ❓.',
 '📚 Bei Fragen zu Nebenwirkungen von Arzneimitteln: Arzt oder Apotheke; Verdachtsfälle können über nebenwirkungen.bund.de gemeldet werden.')

ab('1:12','1:15','🧾 Der Gastgeber fasst 9/11 zusammen','b',
 '**Zusammenfassung:** Der Gastgeber zählt auf, was ihn an der offiziellen Darstellung zweifeln lässt: Mohammed Atta und seine überwiegend saudischen Komplizen hätten am Vorabend in einem Strip-Club gefeiert und mit dem Angriff geprahlt, Korane liegen lassen, Attas Koffer sei nicht ins Flugzeug gekommen, ein Lehrvideo zum Fliegen gefunden worden, ein Pass habe den Einsturz überstanden. Außerdem seien Israelis festgenommen worden („über 100“), darunter die sogenannten „Dancing Israelis“, die das Geschehen gefilmt hätten. Am Vortag habe Rumsfeld 2,3 Billionen Dollar als „fehlend“ gemeldet; ins Pentagon sei „ziemlich offensichtlich eine Rakete“ eingeschlagen.',
 '📌 Alles hier: Aussagen des Gastgebers [1:12–1:15] [seine Sicht]; für die Zahl „über 100“ festgenommener Israelis fand sich in dieser Auswertung keine geprüfte Quelle ❓.',
 '📌 Er verweist auf Seiten von Piloten und Architekten sowie auf Mathias Bröckers [1:14–1:15].',
 '📚 **Ergänzung:** Gemeint ist eine Rede Rumsfelds vom 10.09.2001; nach verbreiteter Darstellung ging es um Buchungen im Verteidigungsministerium, die sich nicht nachverfolgen ließen, nicht um verschwundenes Geld – Quelle hier nicht geprüft ❓.')

ab('1:15','1:18','🏗️ Hulsey-Studie, Afghanistan und die Folgekriege','b',
 '**Zusammenfassung:** Der Gastgeber nennt die Architektenvereinigung AE911Truth und die Studie von Leroy Hulsey (University of Alaska Fairbanks): Nur eine kontrollierte Sprengung erkläre den Einsturz von WTC 7; die NIST-Erklärung „thermische Ausdehnung“ sei „erfunden“. Er verbindet 9/11 mit Afghanistan (Mudschahedin, CIA, pakistanischer ISI, sowjetische Intervention „1978“ provoziert) und der Bin-Laden- und Bush-Familie. Die Kriegskette habe „schätzungsweise 5 Millionen“ Menschen im Nahen Osten das Leben gekostet; Saudi-Arabien sei nicht angegriffen worden. Schöning stimmt zu und kündigt Tucker Carlsons 9/11-Serie an.',
 '📌 „es gibt tausende“ Beweise (Gastgeber) [1:17] [seine Sicht].',
 '📚 **Ergänzung:** Die sowjetische Intervention in Afghanistan begann im Dezember 1979. Costs of War (Brown University) schätzt für die Kriegsgebiete nach 9/11 mindestens 4,5–4,7 Mio. Tote, davon über 940.000 durch direkte Gewalt.',
 '🔗 Zu 9/11 im Kompendium auch ' + GAN + '.')

ab('1:18','1:21','🚢 Trümmer nach China – und Jerome Hauer','d',
 '**Zusammenfassung:** Tucker Carlson habe in einer fünfteiligen Serie WTC 7 gezeigt und die offizielle Geschichte angezweifelt, lenke aber auf China: Die Trümmer seien nach China verschifft und eingeschmolzen worden. Schöning nennt das Ablenkung („die wollen 9/11 die Schuld China in die Schuhe schieben“). Den Mann, den Carlson nicht genannt habe, nennt er: Jerome Hauer sei „Tatortchef“ gewesen und habe den Abtransport veranlasst; später sei er Direktor bei Emergent BioSolutions gewesen.',
 '📌 Carlson stamme „von der Heritage Foundation, von Edwin Meese“ [1:17] [seine Sicht] – nicht geprüft ❓.',
 '📚 **Ergänzung:** Hauer leitete laut Wikipedia das New Yorker Katastrophenschutzamt (OEM) von 1996 bis Februar 2000; am 11.09.2001 war er für Kroll und das US-Gesundheitsministerium tätig. Emergent schreibt dagegen in seinem Nachruf, er sei während der Anschläge „erster Direktor“ des OEM gewesen. Hauer starb am 11.08.2023 und war langjähriges Mitglied des Emergent-Verwaltungsrats.')

ab('1:21','1:24','🏭 Emergent BioSolutions, Spuren in Florida und TRIPOD','d',
 '**Zusammenfassung:** Emergent sei die eigentliche Produktionsstätte der Covid-Impfstoffe; AstraZeneca, Johnson & Johnson und andere setzten nur ihre Marke darauf. Hauer habe mit Rudy Giuliani zusammengearbeitet (über den Schöning abfällige Bemerkungen zu dessen Gesundheit macht – ohne Beleg ❓). Die Entführer hätten in Florida Flugstunden genommen, dort sei auch das erste Anthrax-Opfer gewesen; einer habe einen Arzt wegen eines dunklen Hautflecks aufgesucht – für Schöning gelegte Spuren zu Anthrax. Hauer habe am 10./11. September eine Biowaffen-Übung „Tripod 2“ angesetzt.',
 '📌 „die Schlüsselfigur zwischen 9/11, Dark Winter … Antrags und Covid“ (Schöning über Hauer) [1:24] [seine Sicht].',
 '📚 **Ergänzung:** Laut Bericht von Ausschüssen des US-Repräsentantenhauses (10.05.2022) stellte Emergent in Baltimore für J&J und AstraZeneca her; rund 400 Mio. Dosen mussten wegen Qualitätsmängeln vernichtet werden. Pfizer/Moderna werden dort nicht als Kunden genannt ❓. Die Übung „TRIPOD“ war nach verbreiteten Angaben für den 12.09.2001 geplant – hier nicht geprüft ❓.')

ab('1:24','1:27','🌍 Dark Winter, „Limited Hangout“ und der Handel mit China','f',
 '**Zusammenfassung:** Auch an der Übung „Dark Winter“ habe Hauer teilgenommen. Carlsons Serie sei ein „Limited Hangout“ (Webbs Seite heiße „Unlimited Hangout“): Man solle „böses China“ denken. Schöning warnt, ohne Handel mit China gehe es Deutschland und Europa wirtschaftlich schlechter; mit Russland sei der Handel samt Gas schon gekappt. Statt „New Normal“ oder Rückkehr zum „Old Normal“ fordert er ein „Better Normal“.',
 '💬 „ein besseres Normal, nicht zurück zu dem Old Normal“ (Schöning) [1:26]',
 '📚 **Ergänzung:** Bei „Dark Winter“ (22.–23.06.2001, Pockenszenario) spielte Hauer den FEMA-Direktor. China war 2025 laut Destatis wieder Deutschlands wichtigster Handelspartner (251,8 Mrd. €).')

ab('1:27','1:30','🏛️ John J. McCloy – „der Erbauer des Pentagons“','f',
 '**Zusammenfassung:** Der Gastgeber erwähnt, sieben der 19 Entführer hätten sich später lebend gemeldet, und vergleicht das mit einem Foto der Schauspielerin Jenna Ortega unter angeblichen Toten im Iran; Nahost gehe es um Öl, Gas und Wiederaufbau. Schöning stellt John J. McCloy vor: stellvertretender Kriegsminister im Zweiten Weltkrieg, habe das Pentagon bauen lassen, in den 1920er/30er Jahren den Faschismus in Italien und Deutschland „aufgebaut“, in Hitlers Ehrenloge gesessen, die Bombardierung der Gleise nach Auschwitz verhindert, sei Anwalt der IG Farben, Weltbank-Präsident und als Hoher Kommissar „König von Deutschland“ gewesen.',
 '📌 Alles hier Aussagen Schönings [1:28–1:30] [seine Sicht]; einzelne Punkte (Weltbank-Präsident 1947–1949, Hoher Kommissar 1949–1952) sind gängige Biografie-Daten 📚, andere („Agent“, Faschismus „aufgebaut“) wurden nicht belegt ❓.',
 '📚 **Ergänzung:** Die Ablehnung einer Bombardierung von Auschwitz durch das US-Kriegsministerium 1944 ist in der Holocaust-Forschung dokumentiert und wird dort unterschiedlich eingeordnet ❓ (Quelle hier nicht geprüft).')

ab('1:30','1:33','⚓ McCloy und Adenauer – Gaza und der Korridor IMEC','f',
 '**Zusammenfassung:** McCloy und Konrad Adenauer seien verwandt: Beide hätten eine Frau Zinsser geheiratet, Cousinen. Dann zu Gaza: Dort werde Fläche „freigeräumt“ für einen großen Container- und Gashafen. Dahinter stehe der Handelskorridor IMEC (Indien–Nahost–Europa), aufgebaut von „George Biden“ (gemeint: Joe Biden), von der Leyen und Indien, offiziell über Haifa – dort fehle aber Platz. IMEC solle China mit seiner Neuen Seidenstraße isolieren. Das habe er schon im Sommer 2025 bei AUF1 gesagt; von der Leyen sei „in den letzten Tagen“ in Indien gewesen.',
 '📌 „Die wollen China isolieren, abschneiden“ [1:32] [seine Sicht].',
 '📚 **Ergänzung:** Das IMEC-Memorandum (09.09.2023) beschreibt eine Bahnverbindung mit Schiff-Schiene-Umschlag zwischen Indien, VAE, Saudi-Arabien, Jordanien, Israel und Europa sowie Leitungen für Strom, Daten und „sauberen Wasserstoff“; Gaza wird darin nicht genannt.')

ab('1:33','1:36','🗺️ Kushner in Davos, „Board of Peace“ und das Gasfeld','f',
 '**Zusammenfassung:** Im Januar 2026 habe Jared Kushner in Davos eine Präsentation gezeigt – mit Hafen, „Transportation Hub“ und Schiene. Trumps „Board of Peace“ hole Tony Blair zurück, den Schöning wegen des Irakkriegs 2003 scharf angreift und als prominentes Mitglied der Fabian Society nennt. In Haifa fehle Fläche, der „40 km“ lange Gazastreifen werde „platt gemacht“. Außerdem sei um 2016 im Persischen Golf zwischen Iran und Katar das größte Gasfeld der Welt entdeckt worden.',
 '📌 „Der Hamburger Hafen ist größer als Monaco“ [1:34] – Vergleich nicht geprüft ❓.',
 '📚 **Ergänzung:** Kushner stellte am 22.01.2026 in Davos einen Plan für ein „New Gaza“ vor – mit Seehafen, Flughafen und Tourismus, Kosten mindestens 25 Mrd. US-$. Das Gasfeld South Pars/North Dome ist seit Jahrzehnten bekannt, nicht erst seit 2016 ❓ (Quelle hier nicht geprüft).')

ab('1:36','1:39','🛢️ Pipeline, Syrien und zwei Fraktionen','f',
 '**Zusammenfassung:** Um 2016 hätten der Emir von Katar und der türkische Ministerpräsident bei Assad eine Pipeline durch Syrien angefragt; Assad habe abgelehnt, weil er mit dem Iran baue – Monate später hätten die Probleme in Syrien begonnen. Russische Abwehrraketen hätten Syrien geschützt, bis der Schutz „klick abgestellt“ worden sei; Assad sei nach Moskau gegangen, Maduro sei entführt worden. Es gebe zwei Fraktionen mit gleichem Ziel: die „chinesische“ mit den Demokraten (Neue Seidenstraße) und die Trump-Fraktion (IMEC), dazwischen Palästina.',
 '📌 „Untereinander geht es letztendlich halt um Anteile der Beute“ [1:37] [seine Sicht].',
 '📚 **Ergänzung:** Der Krieg in Syrien begann 2011, nicht nach 2016; Assad floh im Dezember 2024 nach Moskau ❓ (Quellen hier nicht geprüft).')

ab('1:39','1:42','🃏 „Kreuz gegen Karo“ – Deutschland als Schlüssel','f',
 '**Zusammenfassung:** Zur Frage nach Deutschlands Rolle zeigt Schöning sein Kartenspiel: „Kreuz gegen Karo“, die Trump-Fraktion gegen die andere, Ziel in beiden Fällen die Weltherrschaft. Asien, Afrika und Amerika seien entschieden; Europa sei ein „Swing-Kontinent“, England gehöre eher zu den USA. Ohne Deutschland und Frankreich kein Europa, ohne Europa nicht die Welt – darum dürften „sie“ in Deutschland nicht gewinnen. Bei Corona habe man das an der Impfpflicht gesehen.',
 '💬 „Europa ist ein Swingkontinent“ (Schöning) [1:41]',
 '📌 Gaza: Er sei Notfallarzt, Hautfarbe oder Herkunft seien ihm „völlig egal“; es gehe um Lebensqualität [1:39–1:40].')

ab('1:42','1:45','🇦🇹 Impfpflicht in Österreich und Vielfalt als Stärke','a',
 '**Zusammenfassung:** Die Impfpflicht habe man nicht durchsetzen können: „Berlin war fast verloren“, aber in Wien habe man gewonnen – weil Österreich die vom Parlament beschlossene Impfpflicht „mit internationaler Hilfe“ gekippt habe, sei sie auch in Deutschland nicht durchsetzbar gewesen. Europas Stärke sei seine Vielfalt (Österreich, Bulgarien, Dänemark, Schweden mit offenen Schulen), Deutschlands Stärke ebenso: Menschen aus Kriegsgebieten, aus dem früheren Jugoslawien, aus arabischen Staaten und Osteuropa, die wüssten, was Diktatur sei.',
 '📌 Über Künstler, „den guten Rap-Song“ und Videos könne man Menschen zusammenbringen [1:44–1:45] [seine Sicht].',
 '📚 **Ergänzung:** Österreichs Impfpflicht galt ab Anfang Februar 2022, wurde ausgesetzt und am 07.07.2022 vom Nationalrat abgeschafft. Fragen zur eigenen Impfung gehören in die ärztliche Beratung; Verdachtsfälle von Nebenwirkungen lassen sich über nebenwirkungen.bund.de melden.')

ab('1:45','1:51','🎤 Der Gastgeber widerspricht: Hip-Hop und Musikindustrie','m',
 '**Zusammenfassung:** Der Gastgeber widerspricht: Über Rap-Songs lasse sich heute nichts mehr bewegen, die Kultur sei „abgeschafft“ – womöglich geplant, Hip-Hop sei von Anfang an geheimdienstlich gesteuert gewesen und heute voller okkulter Symbolik. Er verweist auf Webb, auf „Julius Caesar Stein“ (📚 Jules C. Stein, Gründer von MCA) und Al Capone sowie auf den Rapper Haftbefehl, der nach einem Gaza-Song gesagt habe, das mache er nie wieder. Podcasts seien heute der eigentliche Hip-Hop; er selbst habe „erfolglos 16 Alben“ veröffentlicht. Schöning: Künstler sollten etwas Neues erfinden; als Beispiel nennt er Tom-Oliver Regenauer.',
 '💬 „Macht sie neu. Künstler erfindet was Neues.“ (Schöning) [1:48]',
 '📌 Gastgeber: Vor 15 Jahren sei es unmöglich gewesen, öffentlich über solche Themen zu sprechen [1:48] [seine Sicht].',
 '🔗 ' + REG + '.')

ab('1:51','1:56','🌿 Verlag, „glücklich und maßvoll“ – Patreon und Abschied','w',
 '**Zusammenfassung:** Schöning empfiehlt die Seite des Verlags (im Transkript „Etika.media“, Schreibweise und Adresse nicht geprüft ❓; „das Gute, Schöne und Mutige“) und seinen Telegram-Kanal; gesund lebe man „glücklich und maßvoll“. Er habe zehn Jahre in Berlin gelebt, davon sieben in Kreuzberg. Das Thema Mikrobiom wird auf ein weiteres Gespräch verschoben; Zuschauer sollen Ausschnitte verbreiten. Der Gastgeber wirbt für Patreon (4,99 € im Monat: Fragen an Gäste, werbefrei, Bonusinhalte) und bittet um einen sachlichen Chat.',
 '💬 „glücklich äh zu leben und maßvoll“ (Schöning) [1:52]',
 '📌 Publikumsfragen gibt es nur für Patreon-Unterstützer [1:53–1:54].')

assert len(AB) == 34, len(AB)

# ---------- Reiter 1: Überblick ----------
kern = [
 ['1','Die Anschläge vom 11.09.2001, die Anthrax-Briefe und die Corona-Pandemie hingen zusammen; dahinter stünden Kriminelle.','Gleiche Personen in Übungen, Firmen und Kommissionen; „Effizienz“ des Erkennens','[0:09–0:18], [1:24]','★★★'],
 ['2','Er habe die Pandemie für 2020 im KenFM-Interview (aufgenommen 12/2018) vorhergesagt.','„mehr Mathematik als Prophezeiung“; Gastgeber: keine direkte Vorhersage, aber nah dran','[0:03–0:06], [0:48–0:49]','★★★'],
 ['3','Bruce Ivins sei nicht der Anthrax-Täter gewesen; die Suizid-Darstellung halte er für unhaltbar.','Ärztliche Einwände, FBI-Überwachung; Bücher „Game Over“','[0:15–0:24]','★★★'],
 ['4','Richard Tubb habe am 11.09.2001 an Bord der Air Force One ein Anthrax-Antibiotikum verteilt – Zeichen für Vorwissen.','Politico-Oral-History; erstes Anthrax-Opfer erst im Oktober','[1:03–1:08]','★★★'],
 ['5','Tubb sitze 2020 in der Corona-Kommission der Heritage Foundation und sei über Medicago mit einem Corona-Impfstoff verbunden.','Kommissionsliste; Tabakfirma, Pflanzen-Impfstoff','[1:01–1:11]','★★'],
 ['6','Jerome Hauer sei die Schlüsselfigur: Tatortchef am 11.09., Übungen TRIPOD und Dark Winter, später bei Emergent BioSolutions.','Trümmer nach China; Emergent als Impfstoff-Hersteller','[1:18–1:25]','★★★'],
 ['7','WTC 7 und Shanksville zeigten, dass die offizielle 9/11-Darstellung nicht stimme (Gastgeber und Gast).','Fallzeit, Loch ohne Trümmer; Hulsey-Studie; Israelis, Rumsfeld','[0:56–1:00], [1:12–1:18]','★★'],
 ['8','Die Epstein-Akten seien Ablenkung; Webbs „One Nation Under Blackmail“ erkläre die Erpressungsstrukturen.','„Opium und Hopium fürs Volk“; 500 Seiten statt Millionen','[0:30–0:36]','★★'],
 ['9','In Gaza gehe es um einen Container- und Gashafen für den Korridor IMEC gegen Chinas Seidenstraße.','AUF1-Interview 2025; Kushner-Präsentation in Davos 2026','[1:30–1:39]','★★'],
 ['10','Deutschland sei der Schlüssel zu Europa; Vielfalt und Aufklärung könnten ein „Better Normal“ schaffen.','„Kreuz gegen Karo“; Impfpflicht in Österreich gekippt','[1:26], [1:39–1:45]','★★'],
]
baum = {'typ':'baum','titel':'🌳 Themenbaum des Gesprächs','wurzel':TITEL,
 'unter':f'{GAST} · REALTALK MEDIA · {DATUM} · {DAUER}',
 'knoten':[
  {'t':'🔮 Vorhersage & Pandemie [0:03–0:12]','k':[{'t':'🎥 KenFM-Interview 12/2018 [0:04]'},{'t':'📺 Gelöscht, Apolut, Odysee [0:06–0:07]'},{'t':'🧩 „mehr Mathematik als Prophezeiung“ [0:49]'},{'t':'🇦🇹 Impfpflicht in Österreich [1:42]'}]},
  {'t':'✉️ Anthrax & Ivins [0:15–0:24]','k':[{'t':'💀 Fünf Tote, Briefe an Medien und Senat [0:16]'},{'t':'🧪 Bruce Ivins, FBI 2008 [0:16–0:19]'},{'t':'⚖️ Einwände gegen die Suizid-Version [0:21–0:23]'},{'t':'👤 Vorwurf an Edwin Meese [0:23]'},{'t':'🔥 Reichstagsbrand-Vergleich, Patriot Act [0:51–0:54]'}]},
  {'t':'🏢 9/11 [0:54–1:18]','k':[{'t':'🏗️ WTC 7 und freier Fall [0:56–0:58]'},{'t':'🌾 Shanksville [0:58–1:00]'},{'t':'📰 Wisnewski und der WDR [1:00]'},{'t':'🧾 Zusammenfassung des Gastgebers [1:12–1:15]'},{'t':'🏛️ Hulsey-Studie, Folgekriege [1:15–1:17]'}]},
  {'t':'👥 Akteure [1:01–1:25]','k':[{'t':'🏛️ Heritage-Kommission 2020 [1:01–1:03]'},{'t':'✈️ Tubb und das Antibiotikum [1:03–1:06]'},{'t':'🌱 Medicago [1:08–1:11]'},{'t':'🚢 Hauer und die Trümmer [1:19–1:22]'},{'t':'🏭 Emergent, TRIPOD, Dark Winter [1:21–1:24]'}]},
  {'t':'🗝️ Epstein & Erpressung [0:30–0:39]','k':[{'t':'📚 Whitney Webb, zwei Bände [0:30–0:34]'},{'t':'📂 Millionen Seiten Akten [0:32]'},{'t':'🇺🇸 Präsidenten und Erpressbarkeit [0:34–0:35]'},{'t':'📀 Game Over 1 und 2 [0:37–0:39]'}]},
  {'t':'📱 Medien, Besitz & Zensur [0:39–0:48]','k':[{'t':'💽 Besitz statt Cloud [0:40–0:42]'},{'t':'🚫 Röper, Lipp, Baud [0:42]'},{'t':'🇻🇪 Maduro, abgeschaltete Abwehr [0:44–0:45]'},{'t':'📺 Black Mirror, Social Credit [0:46–0:48]'}]},
  {'t':'🌍 Geopolitik [1:24–1:45]','k':[{'t':'🇨🇳 China-Handel, Better Normal [1:25–1:26]'},{'t':'🏛️ John J. McCloy [1:28–1:30]'},{'t':'⚓ Gaza und IMEC [1:30–1:33]'},{'t':'🗺️ Kushner in Davos [1:33]'},{'t':'🃏 Kreuz gegen Karo [1:40–1:42]'}]},
  {'t':'🎤 Kultur & Persönliches [0:27–1:56]','k':[{'t':'🎭 Politiker als Marionetten [0:27]'},{'t':'🚣 Rudern und Schach [0:49–0:50]'},{'t':'🎧 Hip-Hop und Musikindustrie [1:45–1:50]'},{'t':'🌿 Glücklich und maßvoll [1:52]'}]},
 ]}

rot = [
 '[seine Sicht] Wer weiß, wer eine Krise geplant hat, muss nicht jede Einzelheit verstehen – er spart Zeit, Geld und Nerven und hat weniger Angst.',
 '[seine Sicht] Der Schlüssel ist der 11.09.2001: Flugzeuge und Anthrax-Briefe gehörten zusammen, und Bruce Ivins sei als Einzeltäter vorgeschoben worden.',
 '[seine Sicht] Dieselben Personen tauchten später wieder auf – Richard Tubb mit Antibiotika an Bord der Air Force One und in einer Corona-Kommission, Jerome Hauer bei Übungen und bei Emergent BioSolutions.',
 '[seine Sicht] Darum habe er für 2020 eine Pandemie ankündigen können; die Strukturen dahinter erklärten Whitney Webbs Bücher über Erpressung und Epstein.',
 '[seine Sicht] Heute kämpften zwei rivalisierende „Clans“ um die Handelswege zwischen Asien und Europa – Gaza und IMEC gegen Chinas Seidenstraße –, und Deutschland sei der Schlüssel, um beiden ein „Game Over“ zu bereiten.',
]

steck = [
 ['**Thema in einem Satz**','Heiko Schöning verbindet 9/11, die Anthrax-Briefe von 2001 und die Corona-Pandemie zu einem kriminellen Zusammenhang und spannt den Bogen zu Epstein, Gaza und Deutschlands Rolle.'],
 ['**Titel**',TITEL+' – REALTALK MEDIA (YouTube)'],
 ['**Format**','Studio-Gespräch in Berlin-Kreuzberg, frei gesprochen; Buch- und DVD-Hinweise im Gespräch [0:30–0:40]; Patreon-Aufruf am Ende [1:53–1:56]; keine Werbeblöcke'],
 ['**Sprecher**','👤 **Heiko Schöning** – Gast, Arzt, Reserveoffizier, Autor („Game Over“) · 🎙️ **Gastgeber** von REALTALK – Name im Video nicht genannt ❓; spricht selbst längere Passagen (u. a. [0:39–0:42], [0:46–0:48], [1:12–1:17], [1:45–1:51])'],
 ['**Dauer**','rund 1 Std. 56 Min.'],
 ['**Datum**','Veröffentlichung nicht ermittelt (2026 ❓); aufgenommen vermutlich Anfang Februar 2026 📚: Maduros Festnahme (Januar 2026), Kushners Davos-Auftritt (22.01.2026) und die Epstein-Freigabe (30.01.2026, „vor ein paar Tagen“) liegen zurück, ein Irankrieg wird erst befürchtet [0:35]'],
 ['**Grundton**','zustimmend und vertraut; der Gastgeber ergänzt eigene Thesen und widerspricht nur einmal ausdrücklich (Musik als Hebel [1:45])'],
 ['**Hinweis**','Gesundheitsthemen nur auf Laien-Ebene; keine Empfehlungen. Vorwürfe gegen namentlich genannte Personen sind Aussagen der Sprecher mit Fundstelle. Einzelheiten zum Tod von Bruce Ivins sind bewusst ausgelassen. ' + HILFE],
]

r1 = [
 {'typ':'folge','k':K,'titel':TITEL,'gast':GAST,'rolle':'Arzt, Reserveoffizier, Autor („Game Over“); Mitgründer „Ärzte für Aufklärung“','kanal':'REALTALK MEDIA',
  'datum':DATUM,'dauer':DAUER,'url':URL,
  'thema':'Heiko Schöning verbindet bei REALTALK die Anschläge vom 11. September, die Anthrax-Briefe von 2001 und die Corona-Pandemie zu einem kriminellen Zusammenhang, nennt dafür Personen wie Bruce Ivins, Richard Tubb und Jerome Hauer und spricht über Epstein, Gaza und den Korridor IMEC sowie Deutschlands Rolle.',
  'kacheln':[[str(len(AB)),'Abschnitte'],['10','Kernaussagen'],['__AG__','Abgleich-Punkte'],['__ZA__','Zeitachse'],['5','Diagramme']]},
 {'typ':'hinweis','text':'Auswertung nach dem Transkript (automatische Untertitel): Gesagtes ohne Zeichen, Ergänzungen 📚, Unklares ❓. Fundstellen [Stunde:Minute] springen ins Video. Die Bewertung bleibt dem Leser.'},
 {'typ':'abschnitt','titel':'⚡ In Kürze','liste':[
  '**Wer:** Heiko Schöning, Arzt und Autor, im Gespräch mit dem (im Video nicht namentlich genannten ❓) Gastgeber von REALTALK MEDIA in Berlin-Kreuzberg; aufgenommen vermutlich Anfang Februar 2026, rund zwei Stunden.',
  '**Vorhersage:** Schöning sagt, er habe im Dezember 2018 bei KenFM eine für 2020 geplante weltweite Pandemie angekündigt; der Gastgeber nennt das keine direkte Vorhersage, aber „sehr nah“ [0:03–0:06].',
  '**Anthrax:** Die Briefe von 2001 (fünf Tote) gehörten zu 9/11; Bruce Ivins sei nicht der Täter gewesen, den Fall habe laut Schöning Edwin Meese vertuscht – ein Vorwurf ohne geprüften Beleg [0:15–0:24].',
  '**9/11:** WTC 7, Shanksville, die Hulsey-Studie und eine lange Zusammenfassung des Gastgebers stellen die offizielle Darstellung infrage [0:56–1:18].',
  '**Personen:** Richard Tubb (Antibiotikum an Bord der Air Force One, Heritage-Kommission 2020, Medicago) und Jerome Hauer (Trümmer, Übungen, Emergent BioSolutions) seien die Verbindung zu Corona [1:01–1:25].',
  '**Epstein:** Die freigegebenen Millionen Seiten seien Ablenkung; Whitney Webbs Bücher erklärten die Erpressungsstrukturen [0:30–0:36].',
  '**Geopolitik:** In Gaza gehe es um einen Hafen für den Korridor IMEC gegen Chinas Seidenstraße; Deutschland sei der Schlüssel zu Europa [1:30–1:45].',
  '**Ausblick:** Statt „New Normal“ ein „Better Normal“; der Gastgeber widerspricht nur bei der Rolle von Musik [1:26], [1:45].']},
 {'typ':'abschnitt','titel':'🔦 Aus Schönings Sicht – der rote Faden','liste':rot},
 {'typ':'text','text':'🎯 **Kernaussagen** – die zehn wichtigsten Thesen des Gesprächs:'},
 {'typ':'tabelle','kopf':['#','Aussage','Begründung im Gespräch','Fundstelle','Gewicht'],'zeilen':kern},
 baum,
 {'typ':'illu','id':'schoening_kette','titel':'Skizze: Der rote Faden 2001–2026 (Darstellung laut Schöning, schematisch)'},
 {'typ':'illu','id':'schoening_daten','titel':'Skizze: Belegte Daten zu den Themen des Gesprächs, 2001–2026 (belegte Daten)'},
 {'typ':'tabelle','kopf':['🧭 Steckbrief',''],'schmal':True,'zeilen':steck},
]

# ---------- Reiter 2: Gespräch im Detail ----------
def bis_txt(t): return t
teile = [{'von':v,'bis':b,'t':re.sub(r'^\S+\s','',t),'th':th} for v,b,t,th,_ in AB]
r2 = [
 {'typ':'text','text':f'🔎 Detaillierte Auswertung in der Reihenfolge des Gesprächs – {len(AB)} Abschnitte. Lesehilfe: 💬 Zitat, 📌 Aussage/Zahl/Beispiel, 🔗 Bezug, 📚 Ergänzung, ❓ unklar. Video: [{TITEL}]({URL})'},
 {'typ':'gespraech','titel':'🧭 Gesprächsverlauf – wann worüber gesprochen wird','dauer':'1:56','themen':THEMEN,'teile':teile},
]
for v,b,t,th,liste in AB:
    r2.append({'typ':'abschnitt','titel':f'{t} [{v}–{b}]','th':th,'liste':liste})

# ---------- Reiter 3: Zeitachse & Verzeichnisse ----------
ZA = [
 ('1933','1933','Reichstagsbrand – laut Schöning „Anschlag unter falscher Flagge“','[0:52]',False),
 ('1941–1945','1941','John J. McCloy stellvertretender Kriegsminister der USA (Assistant Secretary of War)','[1:28]',True),
 ('1944','1944','US-Kriegsministerium lehnt Bombardierung von Auschwitz ab (laut Schöning McCloy)','[1:29]',True),
 ('1947–1949','1947','McCloy Präsident der Weltbank','[1:29]',True),
 ('1949','1949','Gründung der Bundesrepublik; McCloy Hoher Kommissar (bis 1952), Adenauer Bundeskanzler','[1:29–1:30]',True),
 ('Dez. 1979','1979','Sowjetische Intervention in Afghanistan (im Gespräch „1978“)','[1:15]',True),
 ('Feb. 1996–Feb. 2000','1996','Jerome Hauer leitet das New Yorker Katastrophenschutzamt OEM','[1:19]',True),
 ('22.–23.06.2001','2001','Übung „Dark Winter“ (Pockenszenario); Hauer spielt den FEMA-Direktor','[1:24]',True),
 ('10.09.2001','2001','Rumsfeld-Rede zu 2,3 Billionen Dollar im Verteidigungsministerium (laut Gastgeber „fehlend“)','[1:14]',False),
 ('11.09.2001','2001','Anschläge auf WTC 1 und 2, Pentagon; Absturz von Flug 93 bei Shanksville; Einsturz von WTC 7','[0:17], [0:56]',False),
 ('11.09.2001','2001','Richard Tubb gibt an Bord der Air Force One Ciprofloxacin aus (laut Politico eine Wochenration)','[1:03–1:05]',False),
 ('12.09.2001','2001','Geplante Bioterror-Übung „TRIPOD“ in New York (laut Schöning 10./11.09.) ❓','[1:23]',True),
 ('Sept./Okt. 2001','2001','Anthrax-Briefe an Medien und an die Senatoren Daschle und Leahy; 5 Tote, 17 Erkrankte','[0:16], [0:54]',False),
 ('05.10.2001','2001','Erstes Anthrax-Todesopfer in Florida (im Gespräch „6. Oktober“)','[1:06]',True),
 ('26.10.2001','2001','USA PATRIOT Act unterzeichnet','[0:52]',True),
 ('05.02.2003','2003','Colin Powell vor dem UN-Sicherheitsrat (Röhrchen)','[0:55]',True),
 ('2003','2003','Beginn des Irakkriegs (Tony Blair, laut Schöning „Antrags-Massenvernichtungswaffen alles gelogen“)','[1:34]',True),
 ('2008','2008','FBI benennt Bruce Ivins als Täter; Ivins war zuvor gestorben (laut FBI Suizid)','[0:16]',False),
 ('23.11.2008','2008','NIST-Abschlussbericht zu WTC 7: Einsturz durch Brände','[1:16]',True),
 ('19.02.2010','2010','US-Justizministerium und FBI schließen Amerithrax formell ab','[0:16]',True),
 ('15.02.2011','2011','National Academies: Wissenschaft allein klärt Herkunft der Sporen nicht','[0:22]',True),
 ('Dez. 2018','2018','Aufnahme des Interviews Schönings mit Ken Jebsen (KenFM)','[0:04]',False),
 ('Sept. 2019','2019','Ausstrahlung des KenFM-Interviews (laut Schöning 11.09.2019)','[0:04], [0:43]',False),
 ('2019','2019','Start von REALTALK (laut Gastgeber)','[0:00], [1:50]',False),
 ('März 2020','2020','Hulsey-Studie der University of Alaska Fairbanks zu WTC 7 abgeschlossen','[1:15]',True),
 ('06.04.2020','2020','Heritage Foundation gründet „National Coronavirus Recovery Commission“ (u. a. Richard Tubb)','[1:01–1:02]',False),
 ('Nov. 2021','2021','US-Gesundheitsministerium kündigt Emergents Impfstoffvertrag','[1:21]',True),
 ('Feb. 2022','2022','Health Canada lässt Medicagos Pflanzen-Impfstoff zu','[1:09]',True),
 ('Anfang Feb. 2022','2022','Impfpflicht in Österreich tritt in Kraft','[1:42]',True),
 ('10.05.2022','2022','Bericht von Ausschüssen des US-Repräsentantenhauses zu Emergent BioSolutions','[1:21]',True),
 ('07.07.2022','2022','Österreichischer Nationalrat schafft die Impfpflicht ab','[1:42]',True),
 ('Anfang 2023','2023','Mitsubishi Chemical kündigt Schließung von Medicago an','[1:10]',True),
 ('11.08.2023','2023','Tod von Jerome Hauer','[1:19]',True),
 ('09.09.2023','2023','Memorandum zum Korridor IMEC am Rande des G20-Gipfels','[1:31]',True),
 ('Sommer 2025','2025','Schöning spricht bei AUF1 über Gaza und einen Hafen','[1:31]',False),
 ('15.12.2025','2025','Rat der EU sanktioniert u. a. Jacques Baud','[0:42]',True),
 ('Jan. 2026','2026','Festnahme des venezolanischen Präsidenten Maduro durch die USA','[0:44–0:45]',False),
 ('22.01.2026','2026','Kushner stellt in Davos den „New Gaza“-Plan vor; Start des „Board of Peace“','[1:33]',False),
 ('Ende Jan. 2026','2026','Ursula von der Leyen in Indien („in den letzten Tagen“)','[1:32]',False),
 ('30.01.2026','2026','US-Justizministerium veröffentlicht über 3 Mio. Seiten der Epstein-Akten','[0:32]',True),
 ('Anfang Feb. 2026 ❓','2026','Vermutliche Aufnahme dieses Gesprächs','[0:35], [0:50]',True),
 ('11.09.2026','2026','25. Jahrestag von 9/11 („Jubiläumsjahr“)','[0:13], [0:56]',False),
]
zeit = []
for z,j,t,f,e in ZA:
    d = {'z':z,'j':int(j),'t':t,'f':f,'e':e}
    zeit.append(d)
zeit.sort(key=lambda d:(d['j']))
personen = [
 ['Heiko Schöning','Arzt, Reserveoffizier, Autor „Game Over“ (2 Bände); Mitgründer „Ärzte für Aufklärung“ (laut KI-Text)','Gast','durchgehend'],
 ['Gastgeber (REALTALK MEDIA)','Name im Video nicht genannt ❓; laut eigener Aussage Rapper mit 16 Alben, Podcast seit 2019','Fragen, eigene längere Thesen','durchgehend'],
 ['Gesa Schöning','Ehefrau, Verlegerin; Interview mit Whitney Webb','Gruß des Gastgebers','[0:30], [0:32]'],
 ['Ken Jebsen (Kayvan Soufi-Siavash)','Journalist, KenFM/Apolut','Interviewer 2018','[0:04–0:09], [0:51]'],
 ['Bruce Ivins','Mikrobiologe eines US-Biowaffenlabors; laut FBI Täter der Anthrax-Briefe, gestorben 2008','Kern des Anthrax-Teils','[0:16–0:23], [0:52]'],
 ['Edwin Meese','Früherer US-Justizminister, Heritage Foundation','Vorwurf Schönings (Vertuschung) ❓','[0:23], [1:01], [1:17]'],
 ['Richard Tubb','Arzt des Weißen Hauses unter G. W. Bush, später Brigadegeneral a. D.','„Hauptfigur“ laut Schöning','[1:02–1:11]'],
 ['Jerome Hauer (1952–2023)','Katastrophenschutz-Experte, OEM New York 1996–2000, Emergent-Verwaltungsrat','„Schlüsselfigur“ laut Schöning','[1:19–1:25]'],
 ['Rudy Giuliani','Früherer Bürgermeister von New York','Erwähnt mit Hauer','[1:22]'],
 ['Whitney Webb','Journalistin, „One Nation Under Blackmail“, „Unlimited Hangout“','Empfohlene Autorin','[0:30–0:34], [1:11], [1:25]'],
 ['Jeffrey Epstein','Finanzier, verurteilter Sexualstraftäter, gestorben 2019','Epstein-Akten','[0:32–0:35]'],
 ['Donald Trump','US-Präsident','Epstein-Freigabe, „Trump-Fraktion“','[0:32], [0:35], [1:38]'],
 ['Tucker Carlson','US-Moderator','9/11-Serie laut Schöning Ablenkung auf China','[1:17–1:20]'],
 ['Gerhard Wisnewski','Journalist, Autor; WDR-Reportage zu 9/11','Shanksville','[1:00]'],
 ['Tom Daschle, Patrick Leahy','US-Senatoren, Empfänger von Anthrax-Briefen 2001','Patriot Act','[0:54]'],
 ['Colin Powell','US-Außenminister 2001–2005','UN-Rede 2003','[0:55]'],
 ['Mohammed Atta','Einer der Attentäter vom 11.09.2001','Zusammenfassung des Gastgebers','[1:12–1:13]'],
 ['John J. McCloy','US-Jurist und Beamter, Hoher Kommissar in Deutschland 1949–1952','„Erbauer des Pentagons“ laut Schöning','[1:28–1:30]'],
 ['Konrad Adenauer','Erster Bundeskanzler','Verwandtschaft mit McCloy','[1:30]'],
 ['Jared Kushner','Schwiegersohn Trumps','Gaza-Plan in Davos','[1:33], [1:39]'],
 ['Tony Blair','Früherer britischer Premierminister','„Board of Peace“','[1:34]'],
 ['Ursula von der Leyen','Präsidentin der EU-Kommission','Sanktionen, IMEC, Indienreise','[0:42], [1:31–1:32]'],
 ['Nicolás Maduro','Präsident Venezuelas bis Januar 2026','Festnahme','[0:44–0:45], [1:37]'],
 ['Thomas Röper, Alina Lipp, Jacques Baud','Publizisten bzw. Schweizer Ex-Oberst','„gecancelt“, EU-Sanktionen','[0:42]'],
 ['Leroy Hulsey','Bauingenieur, University of Alaska Fairbanks','WTC-7-Studie','[1:15]'],
 ['Tom-Oliver Regenauer','Autor, Musiker','Beispiel für Künstler mit Inhalten','[1:50–1:51]'],
]
orte = [
 ['Berlin-Kreuzberg (SO 36)','Aufnahmeort, Schönings frühere Heimat','[0:00], [1:53]'],
 ['New York (WTC 1, 2, 7)','Anschläge 11.09.2001','[0:17], [0:56]'],
 ['Shanksville (Pennsylvania)','Absturzort von Flug 93','[0:58–1:00]'],
 ['Pentagon (Arlington)','Anschlag; laut Gastgeber Rakete','[1:12–1:14], [1:28]'],
 ['Florida','Bush in einer Schule am 11.09.; Flugstunden der Attentäter; erstes Anthrax-Opfer','[1:04], [1:22]'],
 ['Venezuela','Festnahme Maduros','[0:44–0:45]'],
 ['Gaza','Laut Schöning Fläche für Container- und Gashafen','[1:31–1:35]'],
 ['Haifa','Offizieller IMEC-Hafen laut Schöning','[1:31], [1:34]'],
 ['Davos','Kushners Präsentation 01/2026','[1:33]'],
 ['Persischer Golf (Iran/Katar)','Großes Gasfeld','[1:35]'],
 ['Syrien','Pipeline-Streit, Krieg','[1:36–1:37]'],
 ['Österreich / Wien','Impfpflicht','[1:42]'],
 ['Alaska (Fairbanks)','Hulsey-Studie','[1:15]'],
]
begriffe = [
 ['Anthrax / Milzbrand','Erkrankung durch das Bakterium *Bacillus anthracis*; 2001 als Sporen in Briefen verschickt','[0:16]'],
 ['Amerithrax','FBI-Name der Ermittlungen zu den Anthrax-Briefen 2001','[0:16]'],
 ['Patriot Act','US-Gesetz vom Oktober 2001 mit erweiterten Überwachungsbefugnissen','[0:52–0:54]'],
 ['WTC 7','47-stöckiges Gebäude neben den Zwillingstürmen, eingestürzt am Nachmittag des 11.09.2001','[0:56–0:58]'],
 ['Freier Fall','Fall ohne Widerstand; NIST räumt für WTC 7 eine Phase von 2,25 s ein','[0:57]'],
 ['Ciprofloxacin (Cipro)','Antibiotikum, 2001 auch zur Vorbeugung nach Anthrax-Kontakt eingesetzt','[1:04]'],
 ['Dark Winter','Planspiel 2001 zu einem Pocken-Anschlag','[1:24]'],
 ['TRIPOD','Für den 12.09.2001 geplante Bioterror-Übung in New York ❓','[1:23]'],
 ['Event 201','Pandemie-Planspiel (Oktober 2019) von Johns Hopkins, WEF und Gates-Stiftung 📚','[1:24]'],
 ['Limited Hangout','Teilweise Preisgabe von Informationen, um Wichtigeres zu verdecken (Begriff aus der Geheimdienstsprache)','[1:25]'],
 ['IMEC','India–Middle East–Europe Economic Corridor, Memorandum von 2023','[1:31–1:33]'],
 ['Neue Seidenstraße','Chinas Infrastruktur- und Handelsinitiative','[1:32], [1:38]'],
 ['Board of Peace','Von Trump im Januar 2026 vorgestellter Friedensrat für Gaza','[1:34]'],
 ['Better Normal','Schönings Gegenbegriff zu „New Normal“','[1:26], [1:44]'],
 ['Social Credit','Bewertungssystem für Verhalten; Beispiel „Black Mirror“','[0:46–0:48]'],
 ['Game Over','Schönings Buchreihe: Bd. 1 Covid-19 und Anthrax, Bd. 2 „Angriff aufs Mikrobiom“','[0:37–0:38]'],
]
zahlen = [
 ['Tote durch Anthrax-Briefe','5','[0:16]'],
 ['Aufrufe des KenFM-Interviews','300.000–400.000','[0:07]'],
 ['Fallzeit WTC 7 (laut Schöning)','etwa 7½ s; Höhe 180 m','[0:57]'],
 ['Antibiotika-Ration an Bord (laut Schöning)','60 Tage','[1:04]'],
 ['Rumsfeld, „fehlend“','2,3 Billionen US-$','[1:14]'],
 ['Tote der Kriege im Nahen Osten (Gastgeber)','„schätzungsweise 5 Millionen“','[1:17]'],
 ['Epstein-Akten','„Millionen“ bzw. „3,5 Millionen“ Seiten','[0:32]'],
 ['Fluggeräte beim Maduro-Einsatz (laut Schöning)','150; 100 Tote ❓','[0:44]'],
 ['Gazastreifen','„40 km“','[1:34]'],
 ['Entführer, die noch lebten (Gastgeber)','7 von 19','[1:27]'],
 ['Medicago-Gewinn, auf den verzichtet worden sei','„10 Milliarden“ ❓','[1:10]'],
 ['Patreon','4,99 € im Monat','[1:54]'],
]
r3 = [
 {'typ':'zeitachse','titel':'📅 Zeitachse – Ereignisse, die im Gespräch vorkommen','eintraege':zeit},
 {'typ':'tabelle','kopf':['👤 Person','Wer / was','Rolle im Gespräch','Fundstelle'],'zeilen':personen},
 {'typ':'tabelle','kopf':['🗺️ Ort','Rolle','Fundstelle'],'zeilen':orte},
 {'typ':'tabelle','kopf':['📖 Begriff','Erklärung','Fundstelle'],'zeilen':begriffe},
 {'typ':'tabelle','kopf':['📊 Zahl im Gespräch','Angabe','Fundstelle'],'zeilen':zahlen},
]

# ---------- Reiter 4: Abgleich & Daten ----------
AG = [
 ['Anthrax-Briefe 2001: fünf Tote, Panik, Parlament geschlossen; 2008 habe das FBI einen Einzeltäter benannt [0:15–0:18]',
  'Laut FBI wurden fünf Menschen getötet und 17 erkrankt – die schwersten biologischen Anschläge der US-Geschichte. Das FBI sieht Bruce Ivins als alleinigen Täter; die Ermittlungen wurden am 19.02.2010 formell abgeschlossen.', Q['fbi']+' · '+Q['doj']],
 ['Ivins sei nicht der Täter gewesen; die Darstellung seines Todes sei unhaltbar, das FBI habe ihn „sterben lassen“ [0:18–0:23]',
  'Laut FBI nahm sich Ivins das Leben, bevor Anklage erhoben werden konnte; ein Gerichtsverfahren gab es daher nicht. Schönings medizinische Einwände sind seine Sicht; eine amtliche Stelle hat sie nach den hier geprüften Quellen nicht aufgegriffen ❓. ' + HILFE, Q['fbi']],
 ['Er habe den Fall wissenschaftlich-kriminalistisch aufgeklärt [0:20–0:22]',
  'Die National Academies (2011) prüften die wissenschaftlichen Methoden des FBI: Die Daten lieferten Spuren, schlossen andere Quellen aber nicht aus; „it is not possible to reach a definitive conclusion about the origins of the anthrax“.', Q['nas']],
 ['Edwin Meese habe den Anthrax-Fall „aktiv“ vertuscht [0:23]',
  'Aussage Schönings über eine lebende Person. In den geprüften amtlichen Quellen (FBI, Justizministerium, National Academies) kommt Meese nicht vor; Feststellungen eines Gerichts oder einer Behörde dazu sind nicht bekannt ❓.', Q['fbi']+' · '+Q['doj']],
 ['Zwei Senatoren hätten sich gegen den Patriot Act gestellt, Anthrax-Briefe erhalten und „danach zugestimmt“ [0:53–0:54]',
  'Belegt ist, dass Anthrax-Briefe an Senator Leahy (und Senator Daschle) adressiert waren; das FBI führt Unterlagen zum Leahy-Brief vom November 2001. Ein Zusammenhang mit dem Abstimmungsverhalten ist eine Deutung Schönings ❓.', Q['fbi']],
 ['WTC 7: 180 m Stahlskelett, ohne Flugzeug „im freien Fall“ in etwa 7½ s eingestürzt [0:56–0:58]',
  'NIST: 47-stöckiges Gebäude; unkontrollierte Brände erhitzten Träger, eine Schlüsselstütze (Säule 79) versagte, der Einsturz schritt fort. Die Nordfassade fiel 18 Stockwerke in 5,4 s, darin eine Phase von 2,25 s „essentially in free fall“. NIST fand keine Hinweise auf Sprengungen.', Q['nist']],
 ['Hulsey-Studie: Nur eine kontrollierte Sprengung erkläre WTC 7; „thermische Ausdehnung“ sei erfunden (Gastgeber) [1:15–1:16]',
  'Die Studie von J. Leroy Hulsey u. a. (University of Alaska Fairbanks, Abschluss März 2020) kommt zu dem Schluss, dass Feuer den Einsturz nicht verursacht habe; finanziert wurde sie von Architects & Engineers for 9/11 Truth (316.153 US-$). NIST hält an seiner Erklärung fest.', Q['uaf']+' · '+Q['nist']],
 ['Shanksville: kein Flugzeug, keine Leichen, „kein Tropfen Blut“ [0:58–1:00]',
  'Laut AP wurden die Überreste aller 40 Menschen an Bord von Flug 93 identifiziert (Zahnbefund, DNA, Fingerabdrücke); das Wrack wurde in Containern gelagert und 2018 auf dem Gelände der Gedenkstätte beigesetzt. Die zitierten Aussagen von Bürgermeister und Coroner wurden hier nicht geprüft ❓.', Q['f93']],
 ['Tubb habe am 11.09. an Bord der Air Force One allen eine 60-Tage-Ration Antibiotika gegen Anthrax gegeben – Zeichen für „kriminelles Vorwissen“ [1:03–1:07]',
  'In der Politico-Oral-History sagt Tubb, er habe sich am meisten um einen „biologischen“ Angriff gesorgt und vorsorglich allen an Bord „eine Woche“ Cipro gegeben; ein Mitarbeiter zitiert ihn mit Bezug auf die besuchte Schule: „In case it’s anthrax“. Tubb war damals Oberst. Die Deutung als Vorwissen ist Schönings Sicht; eine behördliche Feststellung dazu ist nicht bekannt ❓.', Q['politico']+' · '+Q['politico2']],
 ['Heritage Foundation (mit Edwin Meese) habe im April 2020 eine Coronavirus-Kommission gebildet, Tubb sei Mitglied gewesen [1:01–1:03]',
  'Heritage gab die „National Coronavirus Recovery Commission“ am 06.04.2020 bekannt (erste Sitzung 09.04.2020); auf der Liste steht „Dr. Richard J. Tubb, Retired Brigadier General; White House Physician Emeritus“. Edwin Meese steht nicht auf der Liste (wohl aber Heritage-Gründer Edwin Feulner). Eine Website „coronaviruscommission.com“ wird dort nicht genannt ❓.', Q['heritage']],
 ['Tubb sei Wissenschaftsvorstand bei British American Tobacco gewesen und habe Medicago gekauft [1:08–1:09]',
  'Laut CBC gehörte Medicago zuletzt vollständig Mitsubishi Tanabe Pharma; Philip Morris International war Anteilseigner und verkaufte seine Anteile Ende 2022. Eine Tätigkeit Tubbs bei British American Tobacco oder ein Kauf Medicagos durch ihn wurde in den geprüften Quellen nicht gefunden ❓.', Q['medicago']],
 ['Medicagos Impfstoff sei zugelassen, die Firma dann „sang- und klanglos“ verkauft und eingestellt worden [1:09–1:11]',
  'Health Canada ließ den Impfstoff 2022 zu; Kanada hatte 2020 173 Mio. CAD investiert und 20 Mio. Dosen bestellt. Die WHO lehnte eine Notfallzulassung wegen der Verbindung zur Tabakindustrie ab. Anfang 2023 kündigte Mitsubishi Chemical die Schließung an.', Q['medicago']],
 ['Jerome Hauer sei am 11.09.2001 „Tatortchef“ gewesen und habe den Abtransport der Trümmer veranlasst [1:19–1:22]',
  'Laut Wikipedia leitete Hauer das New Yorker OEM von Februar 1996 bis Februar 2000 und war am 11.09.2001 für Kroll und das US-Gesundheitsministerium tätig. Emergent BioSolutions schreibt dagegen im Nachruf (2023), er sei während der Anschläge „erster Direktor“ des OEM gewesen. Für eine Zuständigkeit Hauers für den Abtransport fand sich kein Beleg ❓.', Q['hauerwp']+' · '+Q['hauerem']],
 ['Hauer sei Teilnehmer von „Dark Winter“ gewesen [1:24]',
  'Bei „Dark Winter“ (22.–23.06.2001, Andrews Air Force Base; Pocken-Szenario) spielte Hauer den Direktor der FEMA. Veranstalter waren CSIS, das Johns Hopkins Center for Civilian Biodefense Studies, ANSER und MIPT.', Q['darkwinter']],
 ['Hauer sei Direktor bei Emergent BioSolutions gewesen [1:20–1:22]',
  'Emergent bezeichnet Hauer als langjähriges Mitglied des Verwaltungsrats; er starb am 11.08.2023.', Q['hauerem']],
 ['Emergent sei die eigentliche Produktionsstätte der Covid-Impfstoffe, andere setzten nur ihren Markennamen darauf [1:21]',
  'Emergent hatte Herstellungsverträge mit Johnson & Johnson (482 Mio. US-$) und AstraZeneca (174 Mio. US-$) für sein Werk Bayview in Baltimore. Laut Bericht von Ausschüssen des US-Repräsentantenhauses (10.05.2022) mussten dort fast 400 Mio. Dosen wegen Qualitätsmängeln vernichtet werden. Pfizer oder Moderna werden in dem Bericht nicht als Kunden genannt ❓.', Q['emergent']],
 ['Die Trump-Regierung habe „Millionen Seiten“ Epstein-Akten freigegeben – das Wichtige stehe nicht drin, alles geschwärzt [0:32]',
  'Das US-Justizministerium veröffentlichte am 30.01.2026 nach dem Epstein Files Transparency Act mehr als 3 Mio. Seiten, über 2.000 Videos und 180.000 Bilder. Material wurde zurückgehalten, wenn es laufende Ermittlungen gefährden oder mögliche Opfer erkennbar machen könnte.', Q['epstein']],
 ['Die Kriege nach 9/11 hätten „schätzungsweise 5 Millionen“ Menschen im Nahen Osten das Leben gekostet (Gastgeber) [1:17]',
  'Costs of War (Brown University): über 940.000 Tote durch direkte Kriegsgewalt in Irak, Afghanistan, Syrien, Jemen und Pakistan (2001–2023), davon über 432.000 Zivilisten; dazu geschätzt 3,6–3,8 Mio. indirekte Todesfälle – insgesamt mindestens 4,5–4,7 Mio.', Q['cow']],
 ['IMEC solle über einen neuen Container- und Gashafen in Gaza laufen; Haifa fehle die Fläche [1:30–1:35]',
  'Das IMEC-Memorandum (09.09.2023) sieht eine Bahnverbindung mit Schiff-Schiene-Umschlag zwischen Indien, VAE, Saudi-Arabien, Jordanien, Israel und Europa vor, dazu Leitungen für Strom, Daten und „clean hydrogen“. Gaza und ein Gashafen werden darin nicht genannt.', Q['imec']],
 ['Kushner habe im Januar 2026 in Davos Hafen, Schiene und einen Gasturm gezeigt [1:33], [1:39]',
  'Kushner stellte am 22.01.2026 in Davos einen „New Gaza“-Plan vor: Seehafen, Flughafen, Tourismus, Kosten mindestens 25 Mrd. US-$. Bahn- oder Gasanlagen werden im geprüften Bericht nicht erwähnt ❓.', Q['kushner']],
 ['Röper, Lipp und Baud seien „ohne Gerichtsurteil“ per Dekret der EU-Kommission sanktioniert worden [0:42]',
  'Die Sanktionen gegen Jacques Baud beschloss am 15.12.2025 der Rat der EU (nicht die Kommission): Einreiseverbot und Einfrieren von Vermögen in der EU, neben 13 weiteren Personen und zwei Organisationen. Es handelt sich um einen Rechtsakt des Rates, nicht um ein Gerichtsurteil. Die Listung von Röper und Lipp wurde hier nicht geprüft ❓.', Q['baud']],
 ['Österreich habe die vom Parlament beschlossene Impfpflicht „gekippt“ [1:42]',
  'Österreichs Corona-Impfpflicht trat Anfang Februar 2022 in Kraft, wurde ausgesetzt und am 07.07.2022 vom Nationalrat abgeschafft – also durch das Parlament selbst.', Q['austria']],
 ['Ohne Handel mit China gehe es Deutschland wirtschaftlich schlechter [1:26]',
  'China war 2025 mit 251,8 Mrd. € wieder Deutschlands wichtigster Handelspartner (2016–2023 ebenfalls, 2024 die USA). Importen von 170,6 Mrd. € standen Exporte von 81,3 Mrd. € gegenüber.', Q['destatis']],
]

mil = [[2000,583.1],[2001,587.8],[2002,660.0],[2003,751.2],[2004,818.8],[2005,856.5],[2006,868.8],[2007,892.0],[2008,956.9],[2009,1032.2],[2010,1061.7],[2011,1049.1],[2012,990.8],[2013,914.6],[2014,858.4],[2015,838.9],[2016,836.3],[2017,827.7],[2018,852.6],[2019,901.0],[2020,943.4],[2021,933.3],[2022,922.6],[2023,943.0],[2024,1004.9],[2025,929.2]]
ucdp = [[1989,1725],[1990,3995],[1991,25591],[1992,2910],[1993,3576],[1994,7021],[1995,5531],[1996,5127],[1997,4499],[1998,2254],[1999,1538],[2000,540],[2001,642],[2002,1059],[2003,8653],[2004,5235],[2005,4365],[2006,6675],[2007,5747],[2008,4262],[2009,4271],[2010,2926],[2011,9086],[2012,59227],[2013,81816],[2014,100280],[2015,81372],[2016,72194],[2017,55273],[2018,29459],[2019,16458],[2020,14340],[2021,26961],[2022,6503],[2023,31384],[2024,31237],[2025,21438]]

r4 = [
 {'typ':'text','text':'Neutraler Abgleich: links die Aussage im Gespräch, rechts die gängige Darstellung bzw. Daten mit Quelle. Die Bewertung bleibt dem Leser.'},
 {'typ':'tabelle','kopf':['Aussage im Gespräch','Gängige Darstellung (Mainstream) / Daten 📚','Quelle'],'stapel':True,'zeilen':AG},
 {'typ':'kurs','id':'schoening-militaer','titel':'📈 Militärausgaben der USA (konstante US-$ von 2024)',
  'reihen':[{'name':'Militärausgaben der USA','kurz':'Mrd. US-$','einheit':'Mrd. US-$','dez':0,'hoeherGut':None,'punkte':mil}],
  'hoeherGut':None,'vergleich':False,
  'quelle':Q['owidmil']+' – Daten: SIPRI Military Expenditure Database, Stand 2026 (abgerufen 12.11.2026)',
  'hinweis':'Bezug zum Gespräch [1:16–1:17]: „Kette von Kriegsevents“ nach 9/11. Der Anstieg 2002–2010 fällt in die Kriege in Afghanistan und Irak; Werte inflationsbereinigt.'},
 {'typ':'kurs','id':'schoening-konflikttote','titel':'📈 Tote in bewaffneten Konflikten im Nahen Osten (UCDP)',
  'reihen':[{'name':'Konflikttote Nahost (beste Schätzung)','kurz':'Tote','einheit':'Tote','dez':0,'hoeherGut':False,'punkte':ucdp}],
  'hoeherGut':False,'vergleich':False,
  'quelle':Q['owiducdp']+' – Daten: Uppsala Conflict Data Program, Stand 2026 (abgerufen 12.11.2026; 2026 unvollständig, nicht gezeigt)',
  'hinweis':'Bezug zum Gespräch [1:17], [1:36–1:37]: Kriege in Irak, Syrien, Jemen. UCDP zählt nur direkt in Kampfhandlungen Getötete der Region „Middle East“ (ohne Afghanistan); indirekte Todesfälle sind nicht enthalten.'},
 {'typ':'balken','titel':'📊 Tote der Kriege nach 9/11 laut Costs of War (Mio.)','einheit':'Mio.','dez':2,
  'zeilen':[['Direkte Kriegsgewalt (über)',0.94],['davon Zivilisten (über)',0.432],['Indirekte Todesfälle (untere Schätzung)',3.6],['Insgesamt (untere Schätzung)',4.5]],
  'quelle':Q['cow']+', Stand 2023 (Irak, Afghanistan, Syrien, Jemen, Pakistan; 2001–2023)',
  'hinweis':'Bezug zum Gespräch [1:17]: Der Gastgeber nennt „schätzungsweise 5 Millionen“. Die obere Schätzung liegt bei 4,7 Mio. insgesamt bzw. 3,8 Mio. indirekt.'},
 {'typ':'balken','titel':'📊 Deutschlands größte Handelspartner 2025 (Außenhandelsumsatz, Mrd. €)','einheit':'Mrd. €','dez':1,
  'zeilen':[['China',251.8],['Vereinigte Staaten',240.5],['Niederlande',209.1]],
  'quelle':Q['destatis']+', Stand 20.02.2026',
  'hinweis':'Bezug zum Gespräch [1:25–1:26]: Schöning warnt davor, den Handel mit China zu kappen. China war auch 2016–2023 wichtigster Handelspartner, 2024 die USA.'},
 {'typ':'vergleich','titel':'⚖️ Zahlen im Gespräch und Daten nebeneinander','la':'Im Gespräch genannt','lb':'Daten laut Quelle','zeilen':[
  {'n':'Tote durch die Anthrax-Briefe 2001','a':5,'b':5,'einheit':'Tote','f':'[0:16]','q':Q['fbi']},
  {'n':'Antibiotika-Ration an Bord der Air Force One','a':60,'b':7,'einheit':'Tage','f':'[1:04]','q':Q['politico']},
  {'n':'Tote der Kriege nach 9/11 (untere Schätzung)','a':5,'b':4.5,'einheit':'Mio.','f':'[1:17]','q':Q['cow']},
  {'n':'Veröffentlichte Seiten der Epstein-Akten (Gastgeber)','a':3.5,'b':3,'einheit':'Mio. Seiten (Quelle: „mehr als“)','f':'[0:32]','q':Q['epstein']},
 ]},
 {'typ':'abschnitt','titel':'🧩 Spannungen im Gespräch','liste':[
  'Der Gastgeber relativiert gleich zu Beginn: Das KenFM-Interview sei „keine direkte Vorhersage von den detaillierten Events“ gewesen, aber nah dran [0:05].',
  'Einziger ausdrücklicher Widerspruch: Schöning setzt auf Künstler und „den guten Rap-Song“, der Gastgeber hält die Musikkultur für „abgeschafft“ und Podcasts für den besseren Hebel [1:44–1:50].',
  'Schöning betont, alles sei „schriftlich niedergelegt … mit ganz vielen Quellen“ [0:12]; an mehreren Stellen nennt er Zahlen und Daten, die von den geprüften Quellen abweichen (60 statt 7 Tage Cipro, Hauers Amt am 11.09., Medicagos Eigentümer, Datum des ersten Anthrax-Todes, Gasfeld „2016“).',
  'Schöning nennt Tucker Carlsons 9/11-Kritik eine Ablenkung auf China [1:18–1:20], während der Gastgeber vorher selbst viele Einwände gegen die offizielle Darstellung aufzählt [1:12–1:17]; die beiden ergänzen sich, ohne die Quellen zu den einzelnen Punkten zu nennen.',
  'Vorwürfe gegen lebende Personen (Meese, Tubb, Giuliani) stehen ohne Gegenstimme im Raum; der Gastgeber fragt nicht nach Belegen, sagt aber, der Tubb-Bezug sei für ihn neu [1:11].']},
 {'typ':'abschnitt','titel':'💡 Was man mitnehmen kann','liste':[
  'Mehrere Kernangaben lassen sich in Primärquellen nachlesen: Tubbs Cipro-Ausgabe (Politico, 2016), die Heritage-Kommission mit Tubb (2020), Hauers Rolle bei „Dark Winter“ (2001) und im Emergent-Verwaltungsrat, die Qualitätsprobleme bei Emergent (Kongressbericht 2022).',
  'Andere weichen ab: Tubb gab laut eigener Aussage eine Wochenration aus; Hauer leitete das OEM laut Wikipedia nur bis 2000 (Emergent schreibt anderes); Medicago gehörte Mitsubishi Tanabe und zeitweise Philip Morris.',
  'Beim Anthrax-Fall sind beide Seiten dokumentiert: FBI und Justizministerium sehen Ivins als Täter, die National Academies sahen die Wissenschaft allein als nicht beweiskräftig.',
  'Zu WTC 7 liegen zwei Untersuchungen mit gegensätzlichem Ergebnis vor (NIST 2008, Hulsey/UAF 2020) – mit unterschiedlicher Finanzierung.',
  'Gesundheitsfragen (Impfung, Antibiotika, Nebenwirkungen) gehören in die ärztliche Beratung; Verdachtsfälle von Nebenwirkungen können über nebenwirkungen.bund.de gemeldet werden.']},
 {'typ':'abschnitt','titel':'❓ Offen','liste':[
  'Wer ist der Gastgeber von REALTALK MEDIA, und wann wurde das Video veröffentlicht?',
  'Welche Belege hat Schöning für eine Beteiligung Edwin Meeses an den Amerithrax-Ermittlungen [0:23]? In welchem Amt bzw. welcher Rolle soll Meese „Personalchef“ Trumps gewesen sein?',
  'Welche Funktion hatte Jerome Hauer am 11.09.2001 tatsächlich – die Quellen (Wikipedia, Emergent) widersprechen sich [1:19].',
  'Gab es eine Website „coronaviruscommission.com“ und einen dort veröffentlichten Fahrplan [1:02]? War Tubb bei British American Tobacco tätig [1:08]?',
  'Woher stammen die Angaben zu „über 100“ festgenommenen Israelis [1:13] und zu sieben noch lebenden Entführern [1:27]?',
  'Welche Belege gibt es für Schönings Aussagen über John J. McCloy („Agent“, Faschismus „aufgebaut“, Ehrenloge) [1:28–1:29]?',
  'Wurde Wisnewski nach der WDR-Reportage entlassen, und wie lautete die Stellungnahme des WDR [1:00]?']},
 {'typ':'abschnitt','titel':'🔎 Weiter recherchieren','liste':[
  'FBI/Justizministerium: Amerithrax Investigative Summary (2010); National Academies: Review of the Scientific Approaches … (2011); GAO-Bericht zu den Methoden (2014).',
  'G. M. Graff: „The Only Plane in the Sky“ (Politico 2016, Buch 2019) im Zusammenhang lesen.',
  'NIST NCSTAR 1A (2008) und die UAF-Studie (2020) nebeneinander lesen.',
  'Kongressbericht zu Emergent BioSolutions (Mai 2022); Health Canada und WHO zu Medicago.',
  'IMEC-Memorandum (2023) und der „New Gaza“-Plan (2026) im Wortlaut.',
  'Im Kompendium: ' + WIS + ', ' + REGTR + ', ' + POHL + ', ' + GAN + '.']},
]

# Kacheln nachtragen
r1[0]['kacheln'][2][0] = str(len(AG))
r1[0]['kacheln'][3][0] = str(len(zeit))

reiter = [
 {'id':K,'titel':f'{G}: Überblick','bloecke':r1},
 {'id':K+'ab','titel':f'{G}: Gespräch im Detail','bloecke':r2},
 {'id':K+'zeit','titel':f'{G}: Zeitachse und Verzeichnisse','bloecke':r3},
 {'id':K+'abgleich','titel':f'{G}: Abgleich und Daten','bloecke':r4},
]

quellen = [['Video: '+TITEL+' – REALTALK MEDIA (YouTube)', URL]] + [lnk(k) for k in Q]

folge = {
 'k':K,'gast':GAST,'reiter':reiter,
 'folgen_zeile':[DATUM,'Heiko Schöning (Arzt, Autor)',TITEL,'9/11, Anthrax-Briefe 2001 & Bruce Ivins, Corona-Vorhersage, Tubb/Hauer/Emergent, Epstein-Akten, Gaza & IMEC, Deutschlands Rolle',
   '{{a:realtalk-'+K+'|hier: '+G+'}}','[ansehen]('+URL+')'],
 'baum_ast':{'gruppe':'🏛️ Macht & Geschichte','t':'👤 Heiko Schöning bei REALTALK – 9/11, Anthrax, Corona, Epstein, Gaza'},
 'neu':{'d':'2026-11-12','t':'REALTALK – Heiko Schöning','k':f'9/11, Anthrax-Briefe und Pandemie aus Sicht von Heiko Schöning, dazu Epstein und Gaza – {len(AB)} Abschnitte, Abgleich mit Quellen, 5 Diagramme.','h':'#a-realtalk-'+K,'art':'Video'},
 'quellen':quellen,
 'web':[],
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)),'folge.json')
json.dump(folge, open(out,'w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', len(AB), 'Abschnitte,', len(AG), 'Abgleich,', len(zeit), 'Zeitachse')
