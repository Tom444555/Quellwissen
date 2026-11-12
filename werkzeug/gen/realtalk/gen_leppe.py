# -*- coding: utf-8 -*-
# Erzeugt folge.json für „RICARDO LEPPE über den geheimen Lehrplan“ (K = leppe, Autor A-12 realtalk)
import json, os, re
K = 'leppe'; G = 'Leppe'
URL = 'https://www.youtube.com/watch?v=517Cf0ZCrXE'
TITEL = 'RICARDO LEPPE über den geheimen Lehrplan. Warum funktioniert Schule nicht?'
GAST = 'Ricardo Leppe'
DATUM = '2024 ❓'
DAUER = '1 Std. 58 Min.'
KANAL = 'REALTALK MEDIA'

# ---------- Quellen (alle geprüft: per Abruf gelesen oder Daten-API) ----------
Q = dict(
 pisa22='[TUM/ZIB: PISA 2022 – Zusammenfassung (Dez. 2023)](https://www.pisa.tum.de/fileadmin/w00bgi/www/Berichtsbaende_und_Zusammenfassungungen/PISA-2022-zusammenfassung.pdf)',
 pisaanh='[TUM/ZIB: PISA 2022 – Nationaler Bericht, Online-Anhang](https://www.pisa.tum.de/fileadmin/w00bgi/www/Berichtsbaende_und_Zusammenfassungungen/pisa-2022-nationaler-bericht-berichtsband-online-anhang.pdf)',
 wbmat='[Weltbank EdStats (Daten der OECD): PISA Mathematik, LO.PISA.MAT](https://api.worldbank.org/v2/country/DEU;AUT;KOR/indicator/LO.PISA.MAT?format=json&source=12)',
 wbrea='[Weltbank EdStats (Daten der OECD): PISA Lesen, LO.PISA.REA](https://api.worldbank.org/v2/country/DEU;AUT/indicator/LO.PISA.REA?format=json&source=12)',
 iqb='[KMK: IQB-Bildungstrends (Meldung 17.10.2022)](https://www.kmk.org/aktuelles-1/artikelansicht/iqb-bildungstrends.html)',
 esl='[Eurostat edat_lfse_14: Frühe Schul- und Ausbildungsabgänger (18–24 J.)](https://ec.europa.eu/eurostat/databrowser/view/edat_lfse_14/default/table?lang=de)',
 ausg='[Eurostat educ_uoe_fini04: Ausgaben je Schüler/in nach Bildungsstufe](https://ec.europa.eu/eurostat/databrowser/view/educ_uoe_fini04/default/table?lang=de)',
 scheid='[Eurostat demo_ndivind: Rohe Scheidungsziffer](https://ec.europa.eu/eurostat/databrowser/view/demo_ndivind/default/table?lang=de)',
 bverfg06='[BVerfG, Beschluss vom 31.05.2006 – 2 BvR 1693/04 (Schulpflicht)](https://www.bundesverfassungsgericht.de/SharedDocs/Entscheidungen/DE/2006/05/rk20060531_2bvr169304.html)',
 konrad='[EGMR, Konrad u. a. gegen Deutschland, Nr. 35504/03, Entscheidung 11.09.2006](https://hudoc.echr.coe.int/eng?i=001-76925)',
 bverfg21='[BVerfG, Beschluss vom 19.11.2021 – 1 BvR 971/21 (Bundesnotbremse II, Schulschließungen)](https://www.bundesverfassungsgericht.de/SharedDocs/Entscheidungen/DE/2021/11/rs20211119_1bvr097121.html)',
 bverfg21pm='[BVerfG, Pressemitteilung Nr. 100/2021: Schulschließungen waren nach der im April 2021 bestehenden Erkenntnis- und Sachlage zulässig](https://www.bundesverfassungsgericht.de/SharedDocs/Pressemitteilungen/DE/2021/bvg21-100.html)',
 gg7='[Grundgesetz, Art. 7](https://www.gesetze-im-internet.de/gg/art_7.html)',
 gg30='[Grundgesetz, Art. 30](https://www.gesetze-im-internet.de/gg/art_30.html)',
 rschpfl='[Wikipedia: Gesetz über die Schulpflicht im Deutschen Reich (1938)](https://de.wikipedia.org/wiki/Reichsschulpflichtgesetz)',
 glsr='[Wikipedia: Generallandschulreglement (1763)](https://de.wikipedia.org/wiki/Generallandschulreglement)',
 geb='[Wikipedia: General Education Board](https://en.wikipedia.org/wiki/General_Education_Board)',
 dunlosky='[Dunlosky u. a. (2013): Improving Students’ Learning With Effective Learning Techniques, Psychological Science in the Public Interest (PubMed 26173288)](https://pubmed.ncbi.nlm.nih.gov/26173288/)',
 nielsen='[Nielsen u. a. (2013): An Evaluation of the Left-Brain vs. Right-Brain Hypothesis, PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0071275)',
 finger08='[Gracia-Bafalluy & Noël (2008): Does finger training increase young children’s numerical performance?, Cortex (DOI)](https://doi.org/10.1016/j.cortex.2007.08.020)',
 finger10='[Fischer (2010): Numerical performance increased by finger training: a fallacy due to regression toward the mean?, Cortex (DOI)](https://doi.org/10.1016/j.cortex.2008.06.010)',
 finger20='[Schild u. a. (2020): A Finger-Based Numerical Training Failed to Improve Arithmetic Skills …, Frontiers in Psychology (DOI)](https://doi.org/10.3389/fpsyg.2020.00529)',
 who='[WHO/UNICEF (21.08.2020): Advice on the use of masks for children in the community in the context of COVID-19](https://www.who.int/publications/i/item/WHO-2019-nCoV-IPC_Masks-Children-2020.1)',
 orf21='[ORF (17.09.2021): Zahl der Schulabmeldungen auf 7.515 verdreifacht](https://orf.at/stories/3228947/)',
 orf25='[ORF (18.05.2025): Zahl der Schulabmeldungen wieder auf Vor-Pandemie-Niveau](https://orf.at/stories/3394155/)',
 schlager='[Wikipedia: Werner Schlager](https://de.wikipedia.org/wiki/Werner_Schlager)',
 edgley='[Wikipedia: Ross Edgley](https://en.wikipedia.org/wiki/Ross_Edgley)',
 kaiser='[Wikipedia: Gunnar Kaiser](https://de.wikipedia.org/wiki/Gunnar_Kaiser)',
 indien='[Wikipedia: Education in India (PISA 2009+)](https://en.wikipedia.org/wiki/Education_in_India)',
 wsf='[Ricardo Leppe – WissenSchafft Freiheit (Startseite)](https://wissenschafftfreiheit.com)',
 kmkbed='[KMK: Lehrkräfteeinstellungsbedarf und -angebot](https://www.kmk.org/dokumentation-statistik/statistik/schulstatistik/lehrkraefteeinstellungsbedarf-und-angebot.html)',
)
def link(k):
    m = re.match(r'\[(.*)\]\((.*)\)$', Q[k]); return [m.group(1), m.group(2)]

def ab(titel, th, liste):
    return {"typ": "abschnitt", "titel": titel, "th": th, "liste": liste}

# ======================= Reiter 2: Abschnitte =======================
TH = [("a","Herkunft & Familie"),("b","Beziehung, Mann & Frau"),("c","Lernen & Gedächtnis"),
      ("d","Talent, Motivation & Grenzen"),("e","Schulsystem & Geschichte"),("f","Medien, Vorwürfe & Corona"),
      ("g","Freie Bildung & Alternativen"),("w","Einstieg/Organisatorisches")]

A = []  # (von, bis, kurztitel, th, emoji-titel, liste)
def S(von, bis, kurz, th, emo, liste):
    A.append((von, bis, kurz, th, f"{emo} {kurz} [{von}–{bis}]", liste))

S("0:00","0:03","Widmung an Gunnar Kaiser – „Bildungsevolutionär“ statt Revolutionär","w","🎬",[
 "**Zusammenfassung:** Der Gastgeber (Name im Video nicht genannt ❓) begrüßt Ricardo Leppe, den er aus einem Gespräch mit Flavio von Witzleben kennt, und widmet die Sendung „Gona Kaiser“ – gemeint ist der verstorbene Autor Gunnar Kaiser (Hörfehler im Untertitel). Leppe stellt sich als Zauberer vor; „Bildungsevolutionär“ hätten ihn Mütter genannt. Evolution, weil er für etwas und nicht gegen etwas stehen wolle: Wer die staatliche Schule möchte, solle sie behalten.",
 "💬 „Neun von zehn Kinder finden es nun mal kacke.“ (Leppe) [0:01]",
 "📌 Er habe hunderte Schulen besucht; im staatlichen System gebe es keine Alternative – das sei das Problem [seine Sicht] [0:02].",
 "📚 Gunnar Kaiser starb am 12.10.2023 – " + Q['kaiser'] + ".",
])
S("0:03","0:06","Der Vater: Schuppenflechte, Kloster in Japan, Reisen","a","🧘",[
 "**Zusammenfassung:** Leppes Eltern hätten unter dem Schulsystem gelitten. Der Vater sei mit Anfang 20 an schwerer Schuppenflechte erkrankt, laut Medizin unheilbar, und habe die Welt bereist. Ein Mönch in einem japanischen Kloster habe ihm zwei Änderungen in der Ernährung (Milchprodukte, gewisse Fette) und eine seelische (Trennungskonflikt mit dem eigenen Vater) genannt; drei Wochen später sei alles weg gewesen und nie wiedergekommen. Danach Meditation (10–12 Stunden täglich), Kampfsport, 13 Monate zu Pferd durch Indien, Pakistan, Tibet, Nepal; als Leppe fünf war, ging die Familie für drei Jahre nach Peru.",
 "📌 Heilungsbericht als Erfahrung des Vaters wiedergegeben [seine Sicht]; Details in einem eigenen Video [0:05].",
 "📚 [Ergänzung, Laien-Ebene] Schuppenflechte (Psoriasis) ist eine chronisch-entzündliche Erkrankung mit wechselndem Verlauf; Auslöser und Behandlung gehören in fachärztliche Hand (Dermatologie). Keine Empfehlung aus diesem Abschnitt ableiten.",
])
S("0:06","0:09","Drei Jahre Peru, Streit mit der Geschichtslehrerin, Eltern ohne Streit","a","🏔️",[
 "**Zusammenfassung:** In Peru sei der jüngste Bruder geboren; Leppe sei in dieser Zeit nicht zur Schule gegangen, sondern habe frei gelernt – in Österreich sei Homeschooling erlaubt. Mit 14/15 habe er mit seiner Geschichtslehrerin über die Inka gestritten: Er habe dort gelebt, sie nur studiert. Der Vater habe aussteigen und Zeit mit den Kindern haben wollen. Die Eltern seien 40 Jahre verheiratet; Streit habe er nie erlebt.",
 "💬 „Wenn ich iranische haben möchte, spreche mit Iranern.“ (Leppe über Geschichte) [0:07]",
 "📌 Geschichte lieber vor Ort und bei den Menschen selbst lernen als aus dem Schulbuch [seine Sicht] [0:07].",
 "🔗 Gastgeber: Eine Kindheit ohne Streit der Eltern sei „ein sehr krasses Privileg“ [0:08].",
])
S("0:09","0:12","Rollenbild der Mutter – Gastgeber über Familienwandel","b","👪",[
 "**Zusammenfassung:** Der Gastgeber fragt, ob Kritiker die Mutter für unterwürfig halten könnten. Leppe verneint: Was die Mutter sich vornehme, geschehe; die Eltern hätten die Rollen getauscht – seit 20 Jahren sei der Vater zuhause, die Mutter leite einen Secondhand-Laden. Seiner Frau habe er alle Lebensmodelle zum Ausprobieren angeboten. Der Gastgeber meint, das konservative Frauenbild gelte als rückschrittlich; Geburtenrate und Scheidungen hätten sich seit den 60er-Jahren negativ entwickelt.",
 "📌 Gastgeber: mehr Scheidungen als in den 60ern, „das ist statistisch bewiesen“ [0:11].",
 "📚 Rohe Scheidungsziffer Deutschland (je 1.000 Einwohner): 0,9 (1960), Höchststand 2,6 (2003/2004), 1,7 (2021) – " + Q['scheid'] + "; Diagramm im Reiter Abgleich.",
])
S("0:12","0:15","Vaterlose Familien, warum Ehen zerbrechen","b","💍",[
 "**Zusammenfassung:** Der Gastgeber nennt für die schwarze Bevölkerung der USA eine Umkehr von 75 % auf vielleicht 25 % Kinder mit verheirateten Eltern; Väter seien wegen Drogengesetzen oft im Gefängnis gelandet. Leppe: Früher habe man zusammengehalten und oft keine Wahl gehabt; heute gebe es zu viel Angebot und Medien. Paare bänden sich über Äußerlichkeiten, ohne zu besprechen, was sie im Leben wollen. Er habe mit seiner Frau im ersten Jahr vor allem über alte Muster gesprochen und anfangs bewusst auf Körperlichkeit verzichtet.",
 "📌 Zahlen des Gastgebers zu US-Familien nicht geprüft ❓ [0:12].",
 "💬 „seitdem wird's immer nur besser“ (Leppe über die Zeit nach dem ersten Jahr) [0:15]",
])
S("0:15","0:18","Mann und Frau verstehen: lösen oder gehört werden","b","💬",[
 "**Zusammenfassung:** Durch die Arbeit mit vielen Müttern und Mädchen habe Leppe sich mit Gehirn, Lernen und Geschlechterunterschieden beschäftigt: anderes Blickfeld, andere Zyklen – Frauen hätten „zwei Hormonzyklen“. Beispiel: Seine Frau Vanessa habe bei Problemen gehört werden wollen, er habe sie lösen wollen; heute höre er zu und frage am Ende, ob noch etwas gelöst werden solle. Umgekehrt lasse sie ihn bei Problemen allein und stelle ihm Essen ins Büro.",
 "📌 Biologische Aussagen zu Hormonzyklen und Blickfeld als Laien-Darstellung wiedergegeben, nicht geprüft ❓ [0:15–0:16].",
 "🔗 Gastgeber: Hauptproblem sei Pauschalisierung; es gebe Tendenzen, aber z. B. „maskulinere Frauen“ und „feminine Männer“ [0:18].",
])
S("0:18","0:21","Externistenprüfung und 30 Minuten Lernen pro Woche","c","📝",[
 "**Zusammenfassung:** In den ersten Schuljahren sei Leppe nie in der Schule gewesen, habe einmal im Jahr die Externistenprüfungen abgelegt und samstags 30 Minuten gelernt. Der Gastgeber nennt sich einen großen Gamer; Leppe: Kinder merkten sich Städte-, Schwerter- und Zaubernamen oder Serienszenen viel besser als Physikformeln – wer weiß, wie das Gehirn Informationen aufnimmt, spare viel Zeit.",
 "📌 30 Minuten pro Woche gehe nicht mit jedem, aber „eine Stunde am Tag geht mit jeden“ – aus zehn Jahren Erfahrung [seine Sicht] [0:21].",
 "📚 In Österreich gilt Unterrichts-, nicht Schulpflicht; wer häuslich unterrichtet wird, legt am Ende des Schuljahres eine Externistenprüfung ab – " + Q['orf25'] + ".",
])
S("0:21","0:24","Namensgedächtnis wie ein Bizeps – Lernen nach eigenem Takt","c","💪",[
 "**Zusammenfassung:** Es gebe kein schlechtes, nur ein untrainiertes Namensgedächtnis – wie beim Bizeps. Nach ein, zwei Monaten Training sagten alle, sie hätten ein Supergedächtnis. Kinder wollten lernen, wenn man sie nicht zwinge: Er selbst habe mit vier lesen lernen wollen, sein Bruder erst mit neun oder zehn. Später ging Leppe aufs Gymnasium; wenn er keine Lust hatte, habe die Mutter die Tür wieder geschlossen, manchmal sei er nach der dritten Stunde gegangen.",
 "💬 „Jeder Mensch möchte lernen, aber möchte es selber bestimmen dürfen.“ (Leppe) [0:22]",
 "🔗 Gastgeber fragt, ob das in Deutschland ginge; Leppe: in Österreich angenehmer, wenn die Eltern unterschreiben; seine guten Noten hätten Drohungen ins Leere laufen lassen [0:23–0:24].",
])
S("0:24","0:30","Talent, Genetik und Mentalität – vom Zauberer zum Bildungsprojekt","d","🥋",[
 "**Zusammenfassung:** Der Gastgeber bringt dünne Waden und den Kämpfer Jon Jones („John Jones“) ins Spiel: Genetik setze Grenzen. Leppe: Dick heiße nicht stark; jeder komme mit etwa „100 Verteilungspunkten“, verteilt auf verschiedene Fähigkeiten – ein Spitzentalent werde man ohne Begabung nicht, gutes Niveau aber schon. Der Gastgeber nennt Michael Bisping, Leppe einen österreichischen Tischtennis-Weltmeister (Werner Schlager). Entscheidend sei die Motivation, besonders die innere: Mit 19 sei er gegen alle Warnungen Berufszauberer geworden, mit 26 habe er angekündigt, weltweit ein neues Bildungssystem aufzubauen.",
 "💬 „verlieb dich in der Sprache in jemanden“ (Leppe über Motivation) [0:28]",
 "📌 Schlager sei „einziger Tischtennisweltmeister Europas der letzten … 30 Jahre“ [0:27].",
 "📚 Werner Schlager wurde 2003 in Paris Weltmeister und ist laut Stand Januar 2026 der letzte Nicht-Chinese mit diesem Titel – " + Q['schlager'] + ".",
])
S("0:30","0:33","Ross Edgley, Grenzen im Kopf – und der Rückhalt der Eltern","d","🌊",[
 "**Zusammenfassung:** Leppe erzählt von Ross Edgley: ein halbes Jahr täglich bis zu 14 Stunden im Meer rund um Großbritannien, bis zu 15.000 Kalorien am Tag, später 500 km den Yukon hinauf, ein Triathlon mit Baumstamm, die Höhe des Mount Everest am Seil. Der Gastgeber vermutet bei solchen Extremen oft eine „Beweispsychose“ aus fehlender Anerkennung in der Kindheit; Leppe stimmt teilweise zu. Grenzen würden meist in der Bildung gesetzt – eine Lehrerin habe ihm mit 16 gesagt, Zauberer gehe nicht.",
 "💬 „Papa, ich will Drogendealer werden.“ – und er schmeißt mich trotzdem nicht raus (Leppe über bedingungslosen Rückhalt) [0:32]",
 "📚 Edgley schwamm 2018 in 157 Tagen rund 1.780 Meilen (2.860 km) um Großbritannien – " + Q['edgley'] + ".",
])
S("0:33","0:36","Matura nach einem Tag Lernen – Noten fragt niemand","e","🎓",[
 "**Zusammenfassung:** Leppe hat die Matura (vergleichbar dem Abitur) mit gutem Ergebnis abgelegt und dafür nach eigener Aussage nur einen Tag intensiv gelernt; Noten würde er nie wieder haben wollen. Nach seinem Zeugnis habe ihn in seinem ganzen Leben nur die Oma gefragt – obwohl er an Schulen, Universitäten, im indischen Parlament und zwei Monate mit Vorträgen in Vietnam gewesen sei. Firmen wollten in freie Schulen investieren; im Auswendiglernen schlage jeder USB-Stick den Menschen, gefragt seien Kommunikation, Empathie, Auftreten.",
 "📌 Eine „kleine Studie“ in Deutschland habe 25-Jährigen mit Abitur den Schulstoff erneut vorgelegt: Im Schnitt hätten sie noch etwa 1,5 % gekonnt [seine Sicht] [0:35–0:36].",
 "❓ Eine solche Studie ließ sich nicht finden; Quelle im Gespräch nicht genannt.",
])
S("0:36","0:42","Instagram-Umfrage, „da musst du durch“ – und was fürs Leben fehlt","e","📊",[
 "**Zusammenfassung:** Leppe vergleicht: Eine Musikausbildung, nach der man 1,5 % behält, würde niemand machen; bei der Schule akzeptiere man Sätze wie „da musst du durch“. Der Gastgeber nennt eine eigene Instagram-Umfrage (ausdrücklich nicht wissenschaftlich): nützlicher Schulstoff unter 5 % – 28 %, 5–20 % – 48 %, 20–50 % – 19 %, über 50 % – 5 %. Am Markt würde Schule nicht überleben. Leppe: Lesen, Schreiben, Grundrechenarten seien sehr sinnvoll; Oberstufenmathematik brauchten 99,999 % nie wieder, dafür fehlten Kochen, Garten, Steuern, Geld, Reifenwechsel, Umgang mit Emotionen und dem anderen Geschlecht. Der Gastgeber zieht Bruce Lee und Jeet Kune Do heran: Training ums Individuum herum.",
 "💬 „Die kriegst du nicht rausgetreten“ – Kinder wollen Lebenspraktisches lernen (Leppe) [0:40]",
 "🔗 Gastgeber meint, Bruce Lee sei „leider wahrscheinlich ermordet“ worden [seine Sicht] [0:40] ❓.",
])
S("0:42","0:45","Keine dummen Kinder – wer bestimmt, was Wissen wert ist?","e","🎻",[
 "**Zusammenfassung:** Es gebe keine blöden Kinder, nur unterschiedliche Stärken. Sein Cousin, ein Profi-Violinist, sei für schwache Mathenoten herabgesetzt worden; Leppe selbst sei als Genie gelobt worden, weil er Mathe konnte. Ein früherer Ski-Weltmeister habe ihm erzählt, Lehrer hätten ihn mit 14 für seinen Berufswunsch verspottet. Jedes Kind interessiere sich für Geometrie, wenn es ein Baumhaus baue. Auf die Frage, wer den Wert festlege, verweist der Gastgeber auf „Theorien“ um Rockefeller; Leppe: Offiziell bestimme jemand in Berlin, doch frühere Bildungsminister hätten ihm gesagt, sie hätten „gar nichts zu bestimmen“.",
 "💬 „Es gibt einen unsichtbaren Lehrplan im Hintergrund.“ (Leppe) [0:44]",
 "📚 Schulwesen ist in Deutschland Ländersache (Art. 30 GG) und steht unter staatlicher Aufsicht (Art. 7 Abs. 1 GG) – " + Q['gg30'] + ", " + Q['gg7'] + ".",
])
S("0:45","0:48","Gehorsam, Arbeiter und Soldaten – das Gesetz von 1938","e","🏛️",[
 "**Zusammenfassung:** Leppe empfiehlt einen ehemaligen Arzt („Reikabe“ im Untertitel, vermutlich Raik Garve ❓), der über unsichtbaren Lehrplan und „schwarze Pädagogik“ aufkläre. Kurzfassung: Schule sei nie für Kinder gemacht worden, sondern um Menschen zu unterdrücken und Kinder zu brechen – gebraucht habe man Arbeiter und Soldaten. In Deutschland sei das Schulsystem Kirche und Militär untergeordnet, Schulen seien ehemalige Kasernen; das deutsche Schulgesetz stamme von 1938. Die Profiteure nennt er „Parasiten“ statt Elite – militärisch-industrieller Komplex, Schattenherrschaft, „such dir was aus“.",
 "💬 „Es ging immer um gehorsam und um nichts anderes.“ (Leppe) [0:46]",
 "📚 Das Reichsschulpflichtgesetz vom 6. Juli 1938 regelte die Schulpflicht reichsweit; mit dem Grundgesetz ging die Materie in Landesrecht über – " + Q['rschpfl'] + ". Ältere Wurzeln: Preußisches Edikt 1717 (5–12 Jahre) und Generallandschulreglement 1763 – " + Q['glsr'] + ".",
 "🔗 Der Gastgeber erinnert an einen MDR-Bericht, der Leppe zu „Verschwörungstheoretikern“ zählte, die das Bildungssystem „infiltrieren“ [0:47].",
])
S("0:48","0:51","Vorwürfe: Sekte, Rassismus, Antisemitismus – was dahinter stehe","f","📰",[
 "**Zusammenfassung:** Leppe sagt, der MDR habe aus 1,5 Stunden Interview etwa 17 Sekunden verwendet, Namen, Firma und Schullaufbahn falsch dargestellt und verweigere das Gespräch. Er habe nie Drogen, Alkohol oder Gewalt gehabt. Einziger substanzieller Vorwurf: seine öffentliche Aussage, wer Kleinkindern eine Maske aufzwinge, sei ein Verbrecher – dazu stehe er. Den Vorwurf des Antisemitismus führt er auf ein Interview mit einer 16-jährigen deutschen Austauschschülerin an einer russischen Schule zurück, deren Leiter vor 30 Jahren antisemitische Aussagen getätigt haben „soll“; er betont „soll“. Er verweist auf Projekte im arabischen Raum, in Pakistan, Indien, Myanmar, Afrika, Südamerika und auf Einladungen jüdischer Projekte.",
 "📌 Die Darstellung des MDR-Berichts ist Leppes Sicht; der Bericht selbst wurde hier nicht gefunden/geprüft ❓.",
 "📚 WHO und UNICEF rieten 2020, Kindern bis fünf Jahre keine Maske vorzuschreiben – " + Q['who'] + ".",
])
S("0:51","0:54","Das Video zum Zweiten Weltkrieg – alles hinterfragen","f","🔍",[
 "**Zusammenfassung:** Der Gastgeber nennt ein Auto-Video aus dem MDR-Bericht, in dem Leppe Dinge zum Zweiten Weltkrieg anzweifle. Leppe: Sein Großvater habe dort beide Brüder verloren und erzählt, die Russen hätten die Deutschen „am Boden“ ernährt. Darum solle man über Details der Geschichtsschreibung diskutieren – ausdrücklich „nicht das Gesamtkonstrukt, nicht was in den Kammern passiert“. Er bringe Kindern bei, alles zu hinterfragen, auch ihn selbst; das nenne sich Wissenschaft.",
 "📌 Leppe grenzt selbst ab: keine Zweifel an der Existenz des Krieges oder an den Gaskammern [0:51].",
 "💬 „ein Volk per se ist schlecht oder gut. Das ist idiotisch“ (Leppe) [0:52]",
 "🔗 Afghanistan und Pakistan seien nicht wegen „dummer“ Menschen zurück, sondern vom Westen „zurückgebombt“ worden (ironisch: „von Friedensbewegungen“) [seine Sicht] [0:52–0:53].",
])
S("0:54","0:57","Ausladung in der Schweiz – gemeinsam mit Daniele Ganser","f","🇨🇭",[
 "**Zusammenfassung:** Leppe habe allen Kritikern angeboten, rassistische oder antisemitische Videos offline zu nehmen und sich zu entschuldigen, wenn man ihm die Stelle nenne – das sei bis heute nicht geschehen. In der Schweiz sei ein gemeinsames Wochenende mit Daniele Ganser geplant gewesen; nach wochenlanger Presse („die Elite des Bösen trifft sich“) sei er ausgeladen worden, Ganser habe auftreten dürfen. Rund 400 Mütter hätten der Zeitung in Zürich geschrieben. Die Absage habe ihn in den Emiraten am Tisch mit einem Vietnamesen, Pakistaner, Araber und Türken erreicht.",
 "💬 „du nimmst mir die Chance zu wachsen oder mich zu entschuldigen“ (Leppe) [0:55]",
 "🔗 Zu Ganser siehe {{a:ganser|Daniele Ganser (A-04)}}. Name und Datum der Zeitung („NZ“ im Untertitel) nicht geprüft ❓ [0:55].",
])
S("0:57","1:00","Gegenwind seit den Masken – und der kostenlose Kurs","f","😷",[
 "**Zusammenfassung:** Leppe hält die Angriffe für Absicht: Schulen mit Glücksunterricht, Persönlichkeitsentwicklung und Steuerkunde wären das Ende des Systems. Er sei gegen Masken bei Kindern gewesen, nicht gegen die Impfung, solange sie freiwillig sei. Vor Corona habe er nur positive Presse gehabt; 48 Stunden nach seiner Masken-Äußerung sei es losgegangen. 90 % des Gegenwinds kämen aus Deutschland, wo das Schulsystem am härtesten sei. Sein WSF-Kurs sei der größte kostenlose Onlinekurs: rund 400 Videos mit Arbeitsbüchern, anonym herunterladbar und frei weiterzugeben.",
 "📌 Mandela habe gesagt, Bildung sei die größte Macht, die Welt zu verändern [0:57] (Zitat nicht im Wortlaut geprüft ❓).",
 "📌 Mitarbeiter aus Ministerien und Politiker sprächen „unter der Hand“ mit ihm [seine Sicht] [0:59–1:00].",
])
S("1:00","1:03","Wie statt was – und wovon Leppe lebt","g","🪄",[
 "**Zusammenfassung:** Leppe zeige, wie man lernt, nicht was; darum gebe es keine „Ricardo-Leppe-Schule“. Der Gastgeber fragt nach seinem Einkommen und betont, gute Arbeit dürfe gut bezahlt sein. Leppe: Auf der Website gebe es nichts zu kaufen; die Inhalte seien so gut, dass Menschen freiwillig fragten, wie sie spenden könnten. Geld verdiene er mit Firmenvorträgen und Zaubershows – Zauberei sei Luxus, Basisbildung ein Menschenrecht.",
 "💬 „Basisbildung ist für mich ein Menschenrecht“ (Leppe) [1:02–1:03]",
 "🔗 Die Website nennt als Vision u. a. „Bildung als Menschenrecht“ und „Freier kostenloser Zugang zu Bildung“ – " + Q['wsf'] + ".",
])
S("1:03","1:09","Verein, Online-Schule mit Kinder-Lehrenden, Kinder als „Kunden“","g","🧒",[
 "**Zusammenfassung:** Im Verein sei alles spendenbasiert; seit er im Oktober Vater werde, gebe er seine Zeit nicht mehr umsonst her. Er lebe einfach (Secondhand, kein Alkohol, kein Fernseher). Die Online-Schule biete täglich drei bis zehn Angebote, teils von Kindern unterrichtet – die jüngste Lehrende sei sieben; im Sommer sei Pause, ab September wieder. Der Gastgeber erzählt, wie er mit zehn Jahren im Kaufhaus Mütter zu Videospielen beraten habe. Kriterium für Lehrende sei, wie die Zuschauer – meist Kinder – sie bewerten. Der Gastgeber wendet als „Devil's Advocate“ ein, Kinder könnten aus Antipathie urteilen; Leppe: Es gebe Grundregeln und Gründe zähle mehr als Mehrheit.",
 "💬 „Wer ist der Kunde hier?“ (Leppe über Schule) [1:07]",
 "🔗 Gastgeber: Seine 4. Klasse habe sich verschworen, um eine strenge Englischlehrerin bei einer Kontrolle loszuwerden [1:10].",
])
S("1:09","1:12","Lernen über Beziehung – der ehrliche Physiklehrer","e","🤝",[
 "**Zusammenfassung:** Lernen gehe über die Beziehungsebene: Lehrer, die Fehler zugeben, hätten bei Kindern „ein Brett im Stein“. Es gebe tolle Lehrer, aber viele, die aus falschen Gründen Lehrer würden – keine schlechten Menschen, aber schlechte Lehrer. Ein Physiklehrer habe ihn vor die Tür gebeten: Vieles sei veraltet, aber er habe Kredit, zwei kleine Kinder und Ärger mit dem Direktor – bitte keine Fragen mehr vor der Klasse. Leppe habe ihn danach verteidigt, weil er ehrlich gewesen sei.",
 "💬 „ein toller Lehrer ist das Beste, was dein Kind … passieren kann“ (Leppe) [1:10]",
])
S("1:12","1:15","Der Schulweg des Gastgebers – Montessori und Waldorf als Übergang","e","🗺️",[
 "**Zusammenfassung:** Der Gastgeber will ein Buch über seine Schulzeit schreiben: neun Klassen, sechs Schulen in fast zwölf Jahren, vom Iran nach Metzingen im „konservativen Baden-Württemberg“, dann Neukölln und Kreuzberg. Er will über die Geschichte des Schulsystems und über Bildung versus Intelligenz sprechen. Leppe: Montessori- und Waldorfschulen seien besser als staatliche, ein guter Übergang – sein eigenes Kind würde er trotzdem nirgends hinschicken.",
 "📌 Eine staatliche Kreuzberger Schule könne gut geführt sein, eine freie schlecht – Leitung und Lehrkräfte entschieden [1:13].",
])
S("1:15","1:18","Vor- und Nachteile freier Schulen – Steiner und Anthroposophie","g","🌱",[
 "**Zusammenfassung:** Vorteile: mehr Freiheit, Gleitzeit, Praxis (Nähen, Garten), weniger Noten- und Leistungsdruck, motivierte Lehrkräfte. Nachteile: manche ließen alles schleifen, Kinder bekämen keine Grenzen, und auch dort gebe es Menschen, die nicht Lehrer sein sollten. Zu Rudolf Steiner und Anthroposophie will Leppe mangels Erfahrung nicht urteilen. Der Gastgeber sieht sie wegen der Herkunft aus der Theosophie (Helena Blavatsky) skeptisch, spricht von Bezügen zu „satanischen Kulten“ und verweist auf einen „ehemaligen Satanisten“ (Alexander Stier ❓) zu Demeter.",
 "📌 Gastgeber-Aussagen zu Okkultismus, Demeter-Logo („drei Sechsen“) [seine Sicht], nicht geprüft ❓ [1:17–1:18].",
 "💬 „ich rede ungern über Dinge, wenn ich nicht wirklich viel Erfahrungen“ habe (Leppe) [1:16]",
])
S("1:18","1:21","Woher die Schule komme – Kirche, Rockefeller, Ruskin und Rhodes","e","⛪",[
 "**Zusammenfassung:** Der Gastgeber: Das moderne Schulsystem sei katholisch-kirchlich geprägt, mit großem Einfluss der Jesuiten; Schulen gab es schon in Sumer, Ägypten, Griechenland, Rom. Die Rockefeller-Familie sei eine der einflussreichsten für Schulen, Universitäten und Lehrpläne der letzten 200 Jahre; über Oxford und Cambridge, John Ruskin und Cecil Rhodes kommt er zu Leuten, die „diese Welt vergewaltigt“ hätten – „historisch belegbare Fakten“. Leppe: Er gebe Werkzeuge, keine Philosophie vor; auf seiner Website stünden drei Ziele plus „eine freie Menschheit“.",
 "📚 Das General Education Board wurde 1902 mit einer Spende John D. Rockefellers von 1 Mio. US-$ gegründet; die Familie gab insgesamt über 180 Mio. US-$ – " + Q['geb'] + ".",
 "🔗 Zu Rhodes, Milner und dem britischen Empire siehe {{a:regenauer|Tom-Oliver Regenauer (A-11)}}.",
])
S("1:21","1:24","Dezentral, frei wählbar, kostenlos – und das eigene Kind","g","🗳️",[
 "**Zusammenfassung:** Erstens Dezentralisierung von Bildungsmacht: Gemeinden, besser Schulen, Lehrer und Eltern als Rat mit den Kindern sollen entscheiden; Hilfe von oben ja, Weisung nein. Zweitens freie Bildungsentscheidung wie in den USA – staatlich, privat, Montessori, Waldorf, freie Schule, Homeschooling, Freilernen. Drittens kostenlose Basisbildung, gerade für Menschen ohne Chancen; er wolle seinen Kurs verdoppeln bis verdreifachen, inklusive Selbstlernprogrammen für Lesen und Schreiben. Sein eigenes Kind dürfe in die Schule gehen, auch nach Kreuzberg.",
 "💬 „Wie will ich das für andere Menschen bestimmen?“ (Leppe) [1:23]",
 "📚 In Deutschland gilt Schulpflicht; das BVerfG (2006) sah sie als verhältnismäßig, u. a. wegen des Interesses, „Parallelgesellschaften“ entgegenzuwirken – " + Q['bverfg06'] + "; der EGMR wies 2006 die Beschwerde einer Homeschooling-Familie als unzulässig ab – " + Q['konrad'] + ".",
])
S("1:24","1:27","Abschluss bei Bedarf – Schule der Zukunft, Schritt 1","c","🚀",[
 "**Zusammenfassung:** Leppe sagt nicht, man solle bei Unlust fernbleiben – so sei nur sein eigener Weg gewesen. Wer etwas studieren wolle, solle den Abschluss schnell machen: Ein Freilerner (Familie lebte auf Teneriffa) habe mit Anfang 20 Arzt werden wollen und das Abitur in einem Jahr nachgeholt. Der Gastgeber: Man wisse nicht früh, was ein Kind später braucht. Schritt 1 der „Schule der Zukunft“: Lehrplan bleibt, aber mit Lerntechniken lerne man den Stoff 50–90 % schneller und nutze die gewonnene Zeit für Sport, Musik, Kunst oder Interessen.",
 "📌 50–90 % Zeitersparnis „kann ich über die Jahre sagen“ [seine Sicht] [1:26].",
])
S("1:27","1:30","Ein Gymnasium im Münchner Süden – bildhaft, lustig, emotional, verknüpft","c","🏫",[
 "**Zusammenfassung:** Ein Mathelehrer in Deutschland habe nach zwei Jahren 50 % der Zeit eingespart, bei gleichen oder besseren Ergebnissen. Eine Schulleiterin eines Gymnasiums im südlichen Münchner Raum habe vor fast sieben Jahren umgestellt: erstes Jahr Katastrophe, im dritten und vierten Jahr sei der Jahresstoff Ende Oktober durch gewesen; danach Theater, Trommelworkshops, mehr draußen. Auf Nachfrage, ob dafür Stoff wegfalle: nein. Die Essenz: Lernen gehe über Beziehung, Vorbild, Bilder, Lustiges, Emotionales und Verknüpftes.",
 "📌 Schule und Schulleiterin werden nicht genannt; nicht überprüfbar ❓ [1:28].",
 "📚 Eine Übersichtsarbeit zu zehn Lerntechniken bewertet Abfragen/Üben mit Tests und verteiltes Lernen als hoch wirksam, bildhafte Merkhilfen (Schlüsselwort-Mnemonik, Bilder zu Texten) als gering nützlich – " + Q['dunlosky'] + ".",
])
S("1:30","1:33","„Frosch ist Mückengulasch“ – Hirnhälften und Kupplung","c","🐸",[
 "**Zusammenfassung:** Beispiele: F = m·g als „Frosch ist Mückengulasch“. Leppe erklärt, die linke Hirnhälfte sei für Neues zuständig und könne nicht zwei Dinge gegengleich steuern; die rechte arbeite über Bilder, Emotionen und Verknüpfungen. Als Hauptredner einer österreichischen Fahrschullehrertagung habe er das Kupplungsspiel so erklärt: Ein Pedal werde über ein lustiges, bekanntes Bild (ein zurückgehaltener Furz) der rechten Hälfte übergeben – das verkürze das Lernen massiv.",
 "📌 Fingerübung: beide Hände gleich bewegen ist leicht, gegengleich schwer – Erklärung über Hirnhälften [seine Sicht] [1:31].",
 "📚 Eine Studie mit Ruhe-fMRT von über 1.000 Menschen fand keine Belege dafür, dass Menschen insgesamt „linkshirnig“ oder „rechtshirnig“ arbeiten – " + Q['nielsen'] + ".",
])
S("1:33","1:36","Die Neunerreihe mit den Fingern – live vorgeführt","c","✋",[
 "**Zusammenfassung:** Schwierig sei beim Einmaleins fast immer der Bereich ab 6 × 6, besonders Siebener- und Neunerreihe. Leppe führt mit dem Gastgeber (Spitzname „Bello“) den Fingertrick vor: Für 9 × n den n-ten Finger einklappen; links davon stehen die Zehner, rechts die Einer (9 × 2 = 18, 9 × 4 = 36, 9 × 8 = 72). Mit drei solchen Handhaltungen sei das ganze Einmaleins abgedeckt.",
 "💬 „das ist ein geiler Zaubertrick“ (Gastgeber) [1:35]",
 "📚 [Ergänzung] Der Neuner-Fingertrick ist rechnerisch korrekt für 9 × 1 bis 9 × 10.",
])
S("1:36","1:39","Fingerrechnen erlaubt? – 10.000 Zahlen in wenigen Minuten","c","🔢",[
 "**Zusammenfassung:** Manche Lehrer in Deutschland verböten das Rechnen mit den Händen; dafür gebe es weder Studien noch Gesetze. Länder, die in Mathe besser seien – Indien, Südkorea –, seien „Fingerrechen-Länder“; er rate Kindern, bei Nervosität unter dem Tisch zu rechnen. Zweite Übung: die Zahlwörter bis 10.000 einer asiatischen Sprache lernen. Der Gastgeber schätzt eine Woche bzw. einen Tag; Leppe: mit 70.000 Menschen zwischen 6 und 80 Jahren gemacht, Durchschnitt bei Kindern 6–7, bei Erwachsenen 7–8 Minuten, mit Körperbewegungen.",
 "📌 Durchschnittszeiten und 70.000 Teilnehmende [seine Sicht], nicht unabhängig belegt ❓ [1:37].",
 "📚 Südkorea erreichte in PISA 2022 in Mathematik 527 Punkte (Deutschland 475) – " + Q['pisa22'] + ". Indien nahm nur 2009 mit zwei Bundesstaaten teil; beide lagen am Ende der Tabelle – " + Q['indien'] + ".",
])
S("1:39","1:42","Lehrkräfte auswählen wie Polizisten – und besser bezahlen","e","⚖️",[
 "**Zusammenfassung:** Leppe kündigt an, er könne zeigen, dass es in jeder Rechnung eine Prüfziffer gebe ❓. Der Gastgeber fasst zusammen: Entscheidend sei die Passung zwischen Lehrer und Kind; Lehrer, Polizisten und Politiker sollten am strengsten ausgewählt werden. Leppe: Politiker bräuchte es gar nicht; Lehrkräfte sollten hoch angesehen, deutlich besser bezahlt, bestmöglich ausgebildet und unter Beteiligung von Kindern ausgewählt werden.",
 "💬 „Die Leute sollten sich darum reißen, ein Lehrer zu sein“ (Leppe) [1:42]",
])
S("1:42","1:45","Lehrermangel, Drive statt Zeugnis, „du wirst nichts“","d","🔥",[
 "**Zusammenfassung:** Viele – von 16-jährigen Mädchen bis zu Omas – wollten Lehrer werden, „aber nicht unter diesen Bedingungen“; den Lehrermangel könne man „in null Komma nichts“ beheben. Der Gastgeber nennt einen Freund mit Hauptschulabschluss, der heute Agenturen aufkaufe, und eine Bekannte mit Tiermedizin-Studium, die putzen gegangen sei. Entscheidend sei der Drive. Sein Lehrer in der 4. Klasse habe ihm regelmäßig gesagt, er werde nichts.",
 "📌 Leppe: Darum Chancengleichheit [1:45].",
 "📚 Die KMK veröffentlicht regelmäßig Modellrechnungen zu Lehrkräftebedarf und -angebot nach Lehramtstypen – " + Q['kmkbed'] + ".",
])
S("1:45","1:48","Die fünf Hauptfächer – und warum die Medien nur die Person angreifen","g","🖐️",[
 "**Zusammenfassung:** Leppes fünf Hauptfächer: 1. Lesen, Schreiben, Grundrechenarten (tiefer als heute), 2. den Körper kennenlernen (Sport, Musik, Kunst, Ernährung), 3. sich seelisch kennenlernen (Emotionen, Kommunikation, Menschentypen), 4. mit der Natur in Symbiose leben, 5. Lernen lernen. Der Gastgeber: Leppe verkörpere, was eigentlich normal sein sollte. Leppe: Die Medien sprächen nie über seine Lerninhalte, nur über ihn.",
 "💬 „Ich möchte die Möglichkeiten schaffen.“ (Leppe) [1:47]",
])
S("1:48","1:51","Was die Angriffe mit ihm machten – „hört auf zu meckern“","f","🫀",[
 "**Zusammenfassung:** Die Angriffe hätten wehgetan, besonders als Bekannte aus Kindergartenzeiten sich auf Berichte beriefen; vor 2020 habe er keine grauen Haare gehabt. Der Gastgeber meint, es habe ihn stärker gemacht. Botschaft zum Schluss: Wer meckert, bleibe Teil des Problems; alle hätten aktiv oder passiv mitgemacht. Die heutigen Schulen seien mit Druck, Angst und Strafe erschaffen worden – mit Vision und Liebe lasse sich anderes erschaffen.",
 "💬 „Solange du meckerst, bist du immer noch ein Teil dieses Problems.“ (Leppe) [1:50]",
])
S("1:51","1:54","Corona-Homeschooling: Katastrophe oder „schönste Zeit“?","g","🏠",[
 "**Zusammenfassung:** Der Gastgeber fragt nach Social Media und den Lockdowns: Für Familien in Städten sei das Zuhausebleiben eine Katastrophe gewesen – soziale Kontakte weg, mehr Bildschirm. Leppe: Wer nie Homeschooling erlebt oder sich damit beschäftigt habe und zuhause den Schuldruck nachspiele, scheitere; er habe in den Lockdowns bis zu 500 E-Mails am Tag bekommen, und viele Informierte hätten es als schönste Zeit erlebt und seien geblieben.",
 "📚 Das BVerfG leitete 2021 aus dem Grundgesetz ein „Recht auf schulische Bildung“ ab, hielt die Schulschließungen der Bundesnotbremse (April–Juni 2021) aber für zulässig; die Länder mussten Präsenz- nach Möglichkeit durch Distanzunterricht ersetzen – " + Q['bverfg21pm'] + ".",
 "📚 In Österreich verdreifachten sich die Abmeldungen zum häuslichen Unterricht 2021/22 auf 7.515 Kinder – " + Q['orf21'] + ".",
])
S("1:54","1:58","Soziale Kontakte, Bildschirm, Vorbild statt Verbot – Abschied","g","🕯️",[
 "**Zusammenfassung:** Der Gastgeber: Homeschooling brauche bewusste Eltern und soziale Kontakte außerhalb der Schule. Leppe: Manche brauchten viele Menschen, manche kaum – er selbst könne drei Jahre mit Büchern auf einer Berghütte sitzen; Kinder wünschten sich ein bis acht Freunde, keines eine Klasse mit 30. Zu Social Media: Von Kindern könne man nichts verlangen, was man selbst nicht tut; sein Vater habe ihm mit drei Jahren eine Kerze und einen kalten Lappen hingestellt statt Feuer zu verbieten. Der Gastgeber widerspricht dem Vergleich mit Waffen und Messern: Social Media habe Suchtpotenzial und wirke auf die Psyche. Leppe: An den Spielen erkenne er, welche Emotion einem Kind in der Realität fehle. Kontakt: wissenschafftfreiheit.com, Telegram, YouTube, Instagram.",
 "🔗 Gastgeber: „Dopaminrushes“, Depression durch Konsum [seine Sicht] [1:56]; Laien-Ebene, nicht geprüft ❓.",
])

abschnitte = [ab(t, th, l) for (_, _, _, th, t, l) in A]
teile = [{"von": v, "bis": b, "t": k, "th": th} for (v, b, k, th, _, _) in A]

# ======================= Reiter 1: Überblick =======================
kurz = {"typ": "abschnitt", "titel": "⚡ In Kürze", "liste": [
 "**Wer:** Ricardo Leppe – österreichischer Zauberer und Bildungsaktivist („WissenSchafft Freiheit“) – im Gespräch mit dem Gastgeber von REALTALK MEDIA (Name im Video nicht genannt ❓), rund zwei Stunden, Aufnahme vermutlich im Sommer ❓.",
 "**Herkunft:** Ein reisender Vater, drei Jahre Peru, Freilernen mit Externistenprüfungen und samstags 30 Minuten Lernen; später Gymnasium und Matura nach einem Lerntag [0:03–0:36].",
 "**Kernthese:** Schule sei historisch auf Gehorsam angelegt („Arbeiter und Soldaten“), es gebe einen „unsichtbaren Lehrplan“; der meiste Stoff werde vergessen [0:33–0:48].",
 "**Lernen anders:** Bildhaft, lustig, emotional, verknüpft; Fingertricks fürs Einmaleins; Stoff 50–90 % schneller lernen und die Zeit für Sport, Musik, Kunst nutzen [1:24–1:39].",
 "**Vorwürfe:** MDR-Bericht, Ausladung in der Schweiz neben Daniele Ganser, Antisemitismus- und Rassismus-Vorwürfe – Leppe bestreitet sie und nennt seine Masken-Aussage als einzigen belegten Punkt [0:45–1:00].",
 "**Ziele:** Dezentralisierung von Bildungsmacht, freie Bildungsentscheidung, kostenlose Basisbildung; fünf eigene Hauptfächer [1:18–1:24], [1:45].",
 "**Gastgeber:** bringt eigene Themen ein – Familienwandel, Rockefeller, Jesuiten, Ruskin/Rhodes, Anthroposophie – und spielt zeitweise „Devil's Advocate“ [0:09–0:15], [1:06], [1:15–1:21].",
 "**Abgleich:** PISA und IQB zeigen sinkende Leistungen in Deutschland; Heimunterricht ist in Österreich erlaubt, in Deutschland durch Schulpflicht ausgeschlossen (BVerfG, EGMR); einzelne Lern- und Hirnthesen decken sich nicht mit der Studienlage.",
]}
roter = {"typ": "abschnitt", "titel": "🔦 Aus Sicht von Ricardo Leppe – der rote Faden", "liste": [
 "[seine Sicht] Jedes Kind will lernen, aber selbst bestimmen, wann und was – Zwang schließt das Gehirn, Motivation öffnet es.",
 "[seine Sicht] Die staatliche Schule sei nie für Kinder gemacht worden, sondern für Gehorsam; darum lernten Kinder viel und behielten wenig.",
 "[seine Sicht] Lernen gehe über Beziehung, Vorbild, Bilder, Humor, Gefühl und Verknüpfung – so werde derselbe Stoff in einem Bruchteil der Zeit gelernt.",
 "[seine Sicht] Er wolle nichts abschaffen, sondern Wahlfreiheit, Dezentralisierung und kostenlose Basisbildung – und Werkzeuge, die jede Familie frei nutzen kann.",
 "[seine Sicht] Die Angriffe gegen ihn hätten mit seiner Kritik an Masken bei Kindern begonnen und zielten auf seine Person, nicht auf seine Lerninhalte.",
]}
kern = {"typ": "tabelle", "kopf": ["#", "Aussage", "Begründung im Gespräch", "Fundstelle", "Gewicht"], "zeilen": [
 ["1", "Kinder wollen von sich aus lernen – wenn man sie selbst bestimmen lässt.", "Eigene Kindheit, Bruder las erst mit 9–10, Fragen der Kinder", "[0:21–0:22]", "★★★"],
 ["2", "Schule sei auf Gehorsam angelegt: Arbeiter und Soldaten statt kreativer Menschen.", "„unsichtbarer Lehrplan“, Gesetz von 1938, Kirche und Militär", "[0:44–0:46]", "★★★"],
 ["3", "Der meiste Schulstoff werde vergessen und nie gebraucht.", "„1,5 %“-Studie, Instagram-Umfrage, Oberstufenmathe", "[0:35–0:40]", "★★★"],
 ["4", "Mit gehirngerechten Techniken lasse sich derselbe Stoff 50–90 % schneller lernen.", "Mathelehrer, Gymnasium bei München, Fahrschule, Fingertricks", "[1:25–1:39]", "★★★"],
 ["5", "Lernen gehe über Beziehung – ein ehrlicher Lehrer gewinne Kinder.", "Physiklehrer, Klassenkomplott des Gastgebers", "[1:09–1:12]", "★★"],
 ["6", "Gedächtnis ist trainierbar wie ein Muskel; Talent setzt nur Spitzengrenzen.", "Bizeps-Vergleich, „100 Verteilungspunkte“", "[0:21–0:27]", "★★"],
 ["7", "Motivation und Mentalität entscheiden mehr als Zeugnisse.", "Zauberer mit 19, Matura fragt niemand, Ross Edgley", "[0:27–0:34]", "★★"],
 ["8", "Bildung gehöre dezentral, frei wählbar und als Basis kostenlos.", "Website-Ziele, USA als Vorbild, eigenes Kind", "[1:18–1:24]", "★★★"],
 ["9", "Die Vorwürfe gegen ihn seien erfunden und begannen mit seiner Masken-Kritik.", "MDR (17 Sekunden), Schweiz-Ausladung, Antisemitismus-Vorwurf", "[0:47–1:00]", "★★"],
 ["10", "Homeschooling sei nur mit Wissen und Vorbereitung gut – sonst wie im Lockdown eine Katastrophe.", "500 E-Mails am Tag, „schönste Zeit“ für Informierte", "[1:51–1:54]", "★"],
]}
baum = {"typ": "baum", "titel": "🌳 Themenbaum des Gesprächs", "wurzel": TITEL,
 "unter": f"Ricardo Leppe · {KANAL} · {DATUM} · {DAUER}", "knoten": [
 {"t": "👨‍👩‍👦 Herkunft & Familie [0:03–0:12]", "k": [{"t": "🧘 Vater: Kloster in Japan [0:04]"}, {"t": "🏔️ Drei Jahre Peru [0:05]"}, {"t": "📜 Streit über Inka-Geschichte [0:07]"}, {"t": "🏪 Rollentausch der Eltern [0:10]"}]},
 {"t": "💞 Beziehung & Geschlechter [0:09–0:18]", "k": [{"t": "📉 Familienwandel laut Gastgeber [0:11–0:12]"}, {"t": "🗣️ Erst reden, dann Nähe [0:14]"}, {"t": "👂 Lösen oder gehört werden [0:16–0:18]"}]},
 {"t": "🧠 Lernen & Gedächtnis [0:18–0:24], [1:24–1:39]", "k": [{"t": "📝 Externistenprüfung, 30 Minuten [0:19]"}, {"t": "💪 Gedächtnis wie Bizeps [0:21]"}, {"t": "🐸 Frosch ist Mückengulasch [1:30]"}, {"t": "🚗 Hirnhälften und Kupplung [1:31–1:33]"}, {"t": "✋ Neunerreihe mit Fingern [1:34–1:35]"}, {"t": "🔢 10.000 Zahlen in Minuten [1:37]"}]},
 {"t": "🔥 Talent & Motivation [0:24–0:33], [1:42]", "k": [{"t": "🦵 Genetik und dünne Waden [0:24]"}, {"t": "🏓 Werner Schlager [0:27]"}, {"t": "🪄 Zauberer mit 19 [0:29]"}, {"t": "🌊 Ross Edgley [0:30–0:31]"}, {"t": "🙅 „du wirst nichts“ [1:44]"}]},
 {"t": "🏛️ Schulsystem & Geschichte [0:33–0:48], [1:18]", "k": [{"t": "🎓 Matura, Noten, KI [0:33–0:35]"}, {"t": "📊 1,5 % und Instagram-Umfrage [0:35–0:37]"}, {"t": "🕵️ „unsichtbarer Lehrplan“ [0:44]"}, {"t": "🪖 Gehorsam, Gesetz 1938 [0:45]"}, {"t": "⛪ Kirche, Rockefeller, Rhodes [1:18–1:19]"}]},
 {"t": "📰 Medien & Vorwürfe [0:47–1:00], [1:48]", "k": [{"t": "📺 MDR: 17 Sekunden [0:48]"}, {"t": "😷 Masken bei Kleinkindern [0:48], [0:58]"}, {"t": "🕍 Antisemitismus-Vorwurf [0:49–0:51]"}, {"t": "🇨🇭 Ausladung neben Ganser [0:54–0:55]"}, {"t": "🫀 graue Haare seit 2020 [1:49]"}]},
 {"t": "🌱 Freie Bildung [1:00–1:09], [1:12–1:24]", "k": [{"t": "💻 WSF-Kurs, 400 Videos [0:59]"}, {"t": "🧒 Online-Schule mit Kinder-Lehrenden [1:04]"}, {"t": "🏫 Montessori und Waldorf [1:14–1:17]"}, {"t": "🗳️ Dezentral, frei, kostenlos [1:20–1:22]"}]},
 {"t": "🏠 Zukunft & Alltag [1:39–1:58]", "k": [{"t": "⚖️ Lehrkräfte auswählen [1:40–1:42]"}, {"t": "🖐️ Fünf Hauptfächer [1:45–1:46]"}, {"t": "🏠 Corona-Homeschooling [1:51–1:54]"}, {"t": "📱 Social Media und Vorbild [1:55–1:57]"}]},
]}
steck = {"typ": "tabelle", "kopf": ["🧭 Steckbrief", ""], "schmal": True, "zeilen": [
 ["**Thema in einem Satz**", "Warum Schule aus Ricardo Leppes Sicht nicht funktioniert, woher sie kommt und wie Lernen schneller, freier und lebensnäher gehen soll."],
 ["**Titel**", TITEL + " – Kanal REALTALK MEDIA (YouTube @REALTALK-GERMANY)"],
 ["**Format**", "Studio-Gespräch zu zweit, frei gesprochen, mit Live-Übung (Neunerreihe); keine Werbeblöcke im Transkript"],
 ["**Sprecher**", "👤 **Ricardo Leppe** – Gast, Zauberer, Bildungsaktivist (Österreich) · 🎙️ **Gastgeber** von REALTALK MEDIA – Name im Video nicht genannt ❓; laut eigener Aussage aus dem Iran, aufgewachsen in Metzingen, Neukölln, Kreuzberg"],
 ["**Dauer**", DAUER],
 ["**Datum**", "Veröffentlichung nicht ermittelt ❓; Aufnahme nach dem Tod von Gunnar Kaiser (12.10.2023), vermutlich im Sommer (Online-Schule „gerade in Pause“, „ab September wieder“)"],
 ["**Grundton**", "Freundlich, zustimmend; der Gastgeber bringt eigene Thesen ein und fragt gelegentlich kritisch nach (Talent, Kinder als Bewerter, Homeschooling im Lockdown, Social Media)"],
 ["**Hinweis**", "Automatische Untertitel mit Hörfehlern (z. B. „Gona Kaiser“, „Werschlager“, „Reikabe“); Namen geprüft oder mit ❓ markiert."],
]}

# ======================= Reiter 3: Zeitachse & Verzeichnisse =======================
ZA = [
 ("1717", 1717, "Preußisches Edikt: Schulpflicht für Kinder von 5 bis 12 Jahren", "[0:45]", True),
 ("1763", 1763, "Preußisches Generallandschulreglement", "[0:45]", True),
 ("1902", 1902, "General Education Board mit Rockefeller-Geld gegründet", "[0:44], [1:18]", True),
 ("1938", 1938, "Reichsschulpflichtgesetz (6. Juli) – laut Leppe Grundlage des heutigen Schulgesetzes", "[0:45]", False),
 ("1939–1945", 1939, "Zweiter Weltkrieg – Leppes Großvater verliert zwei Brüder", "[0:51]", False),
 ("1949", 1949, "Grundgesetz: Schulpflicht wird Landesrecht", "[0:45]", True),
 ("1960er", 1960, "Laut Gastgeber Ausgangspunkt für Familien- und Scheidungsstatistik", "[0:11–0:12]", False),
 ("1970er", 1970, "Bruce Lee und Jeet Kune Do (Gastgeber)", "[0:40]", False),
 ("2000", 2000, "Erste PISA-Runde mit Deutschland", "[1:36]", True),
 ("2003", 2003, "Werner Schlager wird in Paris Tischtennis-Weltmeister", "[0:27]", True),
 ("2006", 2006, "BVerfG bestätigt Schulpflicht; EGMR weist Homeschooling-Beschwerde (Konrad) ab", "[0:23]", True),
 ("2009", 2009, "Indien nimmt mit zwei Bundesstaaten an PISA 2009+ teil", "[1:36]", True),
 ("2018", 2018, "Ross Edgley schwimmt in 157 Tagen um Großbritannien", "[0:30]", True),
 ("vor ~7 Jahren ❓", None, "Schulleiterin bei München stellt ihr Gymnasium um", "[1:27–1:28]", False),
 ("2020", 2020, "Corona: Leppe kritisiert Masken bei Kleinkindern; Angriffe beginnen „48 Stunden später“", "[0:48], [0:58]", False),
 ("2020", 2020, "Lockdowns: bis zu 500 E-Mails am Tag an Leppe", "[1:52]", False),
 ("2021", 2021, "IQB-Bildungstrend Grundschule: mehr Kinder unter Mindeststandard", "[1:33]", True),
 ("2021", 2021, "BVerfG Bundesnotbremse II: Recht auf schulische Bildung", "[1:51]", True),
 ("2021/22", 2021, "Österreich: 7.515 Kinder im häuslichen Unterricht", "[0:06], [1:51]", True),
 ("2022", 2022, "PISA 2022: Deutschland Mathematik 475, Lesen 480 Punkte", "[1:36]", True),
 ("12.10.2023", 2023, "Tod von Gunnar Kaiser, dem die Sendung gewidmet wird", "[0:00]", True),
 ("2024", 2024, "Ross Edgley schwimmt den Yukon (laut Leppe „letztens“)", "[0:31]", True),
 ("Oktober ❓", None, "Leppe wird nach eigener Aussage Vater", "[1:03]", False),
 ("Sommer ❓", None, "Aufnahme des Gesprächs (Online-Schule in Sommerpause)", "[1:04]", False),
 ("Leben Leppe", None, "Mit 5 Jahren nach Peru (3 Jahre)", "[0:05]", False),
 ("Leben Leppe", None, "Mit 4 Jahren lesen gelernt", "[0:22]", False),
 ("Leben Leppe", None, "Mit 14/15 Streit mit der Geschichtslehrerin", "[0:06]", False),
 ("Leben Leppe", None, "Mit 16: Lehrerin sagt, Zauberer gehe nicht", "[0:32]", False),
 ("Leben Leppe", None, "Mit 18/19 Matura", "[0:22], [0:33]", False),
 ("Leben Leppe", None, "Mit 19 Berufszauberer für Erwachsene", "[0:29]", False),
 ("Leben Leppe", None, "Mit 26: Ziel, weltweit ein neues Bildungssystem aufzubauen", "[0:29]", False),
 ("seit ~10 Jahren", None, "Lernprojekte an Schulen", "[0:21]", False),
 ("Leben Gastgeber", None, "Als Asylbewerber aus dem Iran nach Metzingen, dann Neukölln und Kreuzberg", "[1:06], [1:12]", False),
 ("Leben Gastgeber", None, "4. Klasse: Klasse verschwört sich gegen Englischlehrerin", "[1:10]", False),
 ("Leben Gastgeber", None, "6. Klasse: erster Lehrer, „der kein Arschloch war“", "[1:10]", False),
 ("Leben Gastgeber", None, "Mit etwa 10: berät Mütter beim Spielekauf", "[1:06]", False),
]
def sortkey(e):
    return (0, e[1]) if e[1] is not None else (1, 0)
ZA_sorted = sorted([e for e in ZA if e[1] is not None], key=lambda e: e[1]) + [e for e in ZA if e[1] is None]
zeitachse = {"typ": "zeitachse", "titel": "📅 Zeitachse – Ereignisse, die im Gespräch vorkommen", "eintraege": [
    ({"z": z, "j": j, "t": t, "f": f, "e": e} if j is not None else {"z": z, "t": t, "f": f, "e": e}) for (z, j, t, f, e) in ZA_sorted]}

personen = {"typ": "tabelle", "kopf": ["👤 Person", "Wer / was", "Rolle im Gespräch", "Fundstelle"], "zeilen": [
 ["Ricardo Leppe", "Zauberer, Bildungsaktivist aus Österreich, Initiative „WissenSchafft Freiheit“", "Gast", "durchgehend"],
 ["Gastgeber (REALTALK MEDIA)", "Name im Video nicht genannt ❓; aus dem Iran, aufgewachsen in Metzingen und Berlin", "Fragen, eigene Thesen, „Devil's Advocate“", "durchgehend"],
 ["Gunnar Kaiser", "Autor, Webvideoproduzent, † 12.10.2023 (im Untertitel „Gona Kaiser“)", "Widmung der Sendung", "[0:00]"],
 ["Flavio von Witzleben", "Moderator; führte ein Interview mit Leppe", "Anlass, frühere Aussagen Leppes", "[0:00], [1:12], [1:24]"],
 ["Leppes Vater", "Reisender, früher Lebensmittelindustrie, bald 70", "Heilungsgeschichte, Erziehung", "[0:03–0:10], [1:55]"],
 ["Leppes Mutter", "Leitet einen Secondhand-Laden", "Rollenbild, Rückendeckung beim Schwänzen", "[0:07–0:10], [0:22]"],
 ["Vanessa", "Leppes Frau", "Beispiel für Kommunikation in der Beziehung", "[0:16]"],
 ["Jon Jones", "UFC-Kämpfer (im Untertitel „John Jones“)", "dünne Waden als Genetik-Beispiel", "[0:24]"],
 ["Michael Bisping", "Früherer UFC-Champion", "harte Arbeit statt Talent", "[0:26]"],
 ["Anderson Silva", "UFC-Kämpfer", "Talent-Beispiel", "[0:26]"],
 ["Werner Schlager", "Österreichischer Tischtennis-Weltmeister 2003 (im Untertitel „Werschlager“)", "Denker statt Athlet", "[0:27]"],
 ["Ross Edgley", "Britischer Extremschwimmer", "mentale Stärke", "[0:30–0:31]"],
 ["Bruce Lee", "Kampfkünstler, Jeet Kune Do (im Untertitel „der h Lee“)", "Individualität im Training (Gastgeber)", "[0:40]"],
 ["„Reikabe“", "Ehemaliger Arzt, vermutlich Raik Garve ❓", "Empfehlung zum „unsichtbaren Lehrplan“", "[0:45]"],
 ["Daniele Ganser", "Schweizer Historiker", "gemeinsames Wochenende, Ausladung", "[0:54–0:55]"],
 ["Nelson Mandela", "Südafrikanischer Präsident", "Zitat über Bildung", "[0:57]"],
 ["Gerald Hüther", "Neurobiologe", "Baustein für eigene Schulkonzepte", "[0:49]"],
 ["Vera F. Birkenbihl", "Lernexpertin (im Untertitel „Birkenbild“)", "Baustein für eigene Schulkonzepte", "[0:49]"],
 ["Rudolf Steiner", "Begründer der Anthroposophie", "Waldorf-Frage", "[1:15–1:17]"],
 ["Helena Blavatsky", "Theosophin (im Untertitel „Blazki“)", "Gastgeber zur Herkunft der Anthroposophie", "[1:17]"],
 ["Alexander Stier ❓", "Laut Gastgeber „ehemaliger Satanist“", "Gast in einem anderen Format (Name unklar)", "[1:17]"],
 ["John D. Rockefeller / Familie", "Stifter u. a. des General Education Board", "Einfluss auf Schulen (Gastgeber)", "[0:44], [1:18]"],
 ["John Ruskin · Cecil Rhodes", "Oxford-Professor · Kolonialpolitiker (im Untertitel „Ceel Rads“)", "Gastgeber zur Geschichte", "[1:19]"],
]}
orte = {"typ": "tabelle", "kopf": ["🗺️ Ort", "Rolle", "Fundstelle"], "zeilen": [
 ["Österreich", "Leppes Heimat; häuslicher Unterricht erlaubt, Matura", "[0:06], [0:23], [0:33]"],
 ["Japan (Kloster)", "Heilungsgeschichte des Vaters", "[0:04]"],
 ["Indien · Pakistan · Tibet · Nepal", "Reisen des Vaters", "[0:05]"],
 ["Peru", "drei Jahre Familienleben „unter den Inkas“", "[0:05–0:07]"],
 ["USA", "Familienstatistik (Gastgeber); Vorbild für freie Schulwahl", "[0:12], [0:58], [1:21]"],
 ["Indien (Parlament) · Vietnam", "Vorträge Leppes", "[0:34]"],
 ["Berlin", "„Sesselfurzer in Berlin“ entscheide über Lehrpläne", "[0:44], [1:20]"],
 ["Schweiz / Zürich", "Ausladung, Zeitungsberichte", "[0:54–0:55]"],
 ["Vereinigte Arabische Emirate", "Ort, an dem Leppe die Absage erreichte", "[0:56]"],
 ["Thailand", "burmesische Flüchtlingskinder", "[0:53]"],
 ["Iran · Metzingen · Neukölln · Kreuzberg", "Schulweg des Gastgebers", "[1:12]"],
 ["Gymnasium im südlichen Münchner Raum", "Umstellung der Lernmethoden", "[1:27–1:28]"],
 ["Teneriffa", "Freilerner-Familie, Abitur nachgeholt", "[1:24]"],
 ["Großbritannien · Yukon", "Edgleys Schwimm-Rekorde", "[0:30–0:31]"],
 ["Südkorea · Indien", "„Fingerrechen-Länder“, besser in Mathe", "[1:36]"],
]}
begriffe = {"typ": "tabelle", "kopf": ["📖 Begriff", "Erklärung", "Fundstelle"], "zeilen": [
 ["Bildungsevolutionär", "Leppes Selbstbezeichnung: entwickeln statt umstürzen", "[0:01–0:02]"],
 ["Freilernen", "Lernen ohne Schule und Lehrplan, nach eigenem Interesse", "[0:06], [1:24]"],
 ["Externistenprüfung", "Prüfung für häuslich unterrichtete Kinder in Österreich am Schuljahresende", "[0:19]"],
 ["Unterrichtspflicht / Schulpflicht", "Österreich: Pflicht zum Unterricht (auch zuhause); Deutschland: Pflicht zum Schulbesuch", "[0:23]"],
 ["Matura", "Österreichische Reifeprüfung, entspricht dem Abitur", "[0:33]"],
 ["„Bulimie-Lernen“", "Reinstopfen, rauskotzen, vergessen", "[0:35]"],
 ["Unsichtbarer / geheimer Lehrplan", "Laut Leppe verborgene Ziele hinter dem Schulsystem (Gehorsam)", "[0:44–0:45]"],
 ["Schwarze Pädagogik", "Erziehung durch Zwang, Strafe und Demütigung", "[0:45]"],
 ["WSF-Kurs", "Kostenloser Onlinekurs von „WissenSchafft Freiheit“, rund 400 Videos", "[0:59]"],
 ["Schule der Zukunft (Schritt 1)", "Lehrplan bleibt, Stoff mit Lerntechniken schneller lernen", "[1:25–1:29]"],
 ["Jeet Kune Do", "Kampfkunst-Konzept von Bruce Lee", "[0:40]"],
 ["Anthroposophie / Theosophie", "Weltanschauung Steiners / ihre Vorläuferin", "[1:15–1:17]"],
 ["Demeter", "Anbauverband der biologisch-dynamischen Landwirtschaft", "[1:17–1:18]"],
 ["Loci-Methode", "📚 Klassische Gedächtnistechnik mit Orten/Wegen; Leppes „Körperliste“ ist ein ähnliches Prinzip", "[1:39]"],
 ["Fünf Hauptfächer", "Lesen/Schreiben/Rechnen, Körper, Seele, Natur, Lernen lernen", "[1:45–1:46]"],
]}
zahlen = {"typ": "tabelle", "kopf": ["📊 Zahl im Gespräch", "Angabe", "Fundstelle"], "zeilen": [
 ["Kinder, die Schule ablehnen", "9 von 10", "[0:01], [1:18]"],
 ["Heilung des Vaters", "nach 3 Wochen", "[0:04]"],
 ["Indien zu Pferd", "13 Monate", "[0:05]"],
 ["Ehe der Eltern", "40 Jahre", "[0:08]"],
 ["US-Familien mit verheirateten Eltern (Gastgeber)", "75 % → ~25 %", "[0:12]"],
 ["Lernen in den ersten Jahren", "30 Minuten pro Woche", "[0:19]"],
 ["„geht mit jedem“", "1 Stunde am Tag", "[0:21]"],
 ["Behaltener Schulstoff (Studie)", "1,5 %", "[0:36]"],
 ["Instagram-Umfrage (Gastgeber)", "<5 %: 28 % · 5–20 %: 48 % · 20–50 %: 19 % · >50 %: 5 %", "[0:37]"],
 ["Oberstufenmathe nie gebraucht", "99,999 %", "[0:39]"],
 ["MDR-Interview", "1,5 Std. → 17 Sekunden", "[0:48]"],
 ["Gegenwind aus Deutschland", "90 %", "[0:58]"],
 ["WSF-Kurs", "400 Videos (übliche Kurse 17–21)", "[0:59]"],
 ["Schreibende Mütter (Schweiz)", "400", "[0:55]"],
 ["Lernzeit-Ersparnis", "50–90 %", "[1:25]"],
 ["Zahlwörter bis 10.000", "Ø 6–7 Min. (Kinder), 7–8 Min. (Erwachsene), 70.000 Teilnehmende", "[1:37]"],
 ["E-Mails im Lockdown", "bis zu 500 am Tag", "[1:52]"],
 ["Gewünschte Freunde", "1 bis 8", "[1:55]"],
 ["Ross Edgley", "½ Jahr, 14 Std./Tag, bis 15.000 kcal, Yukon 500 km, Baumstamm 52 kg", "[0:30–0:31]"],
]}

# ======================= Reiter 4: Abgleich =======================
abg = [
 ["„Neun von zehn Kinder“ fänden Schule schlecht [0:01], [1:18]", "Eine repräsentative Zahl dazu wurde für diese Auswertung nicht geprüft ❓. Belegt ist der Leistungsrückgang: In PISA 2022 erreichte Deutschland in Mathematik 475 Punkte (2012: 514), 30 % lagen unter Kompetenzstufe II.", Q['pisa22'] + " · " + Q['wbmat']],
 ["Studie: 25-Jährige mit Abitur könnten nur noch etwa 1,5 % des Schulstoffs [0:35–0:36]", "Eine Studie mit diesem Aufbau und Ergebnis ließ sich nicht finden; im Gespräch wird keine Quelle genannt ❓.", "❓ keine Quelle gefunden"],
 ["Das deutsche Schulgesetz stamme von 1938 [0:45]", "Das Reichsschulpflichtgesetz vom 6. Juli 1938 regelte die Schulpflicht reichsweit; mit dem Grundgesetz ging die Materie in die Landesgesetzgebung über. Heute haben die Länder eigene Schulgesetze.", Q['rschpfl'] + " · " + Q['gg30']],
 ["Schule diene seit jeher Gehorsam – „Arbeiter und Soldaten“ [0:45–0:46]", "Die Schulpflicht in Preußen geht auf ein Edikt von 1717 (Kinder von 5 bis 12 Jahren) und das Generallandschulreglement von 1763 unter Friedrich II. zurück. Über Ziele und Motive gibt es verschiedene Deutungen; die Gehorsams-These ist Leppes Sicht.", Q['glsr']],
 ["Das Schulsystem sei in Deutschland Kirche und Militär untergeordnet [0:45]", "Laut Grundgesetz steht das gesamte Schulwesen unter der Aufsicht des Staates; Religionsunterricht ist an öffentlichen Schulen ordentliches Lehrfach (außer an bekenntnisfreien Schulen), Privatschulen sind gewährleistet.", Q['gg7']],
 ["Ein „Sesselfurzer in Berlin“ bestimme über Millionen Kinder; Minister hätten „nichts zu bestimmen“ [0:44], [1:20]", "Bildung ist in Deutschland Sache der Länder; der Bund hat für Schulen keine allgemeine Zuständigkeit. Die Aussage über Ex-Minister ist nicht überprüfbar ❓.", Q['gg30'] + " · " + Q['gg7']],
 ["Rockefeller-Familie präge Schulen, Universitäten und Lehrpläne (Gastgeber) [0:44], [1:18]", "Das General Education Board wurde 1902 mit 1 Mio. US-$ von John D. Rockefeller gegründet; die Familie gab insgesamt über 180 Mio. US-$. Es förderte v. a. Bildung im Süden der USA und wurde 1964 geschlossen. Ein Einfluss auf heutige deutsche Lehrpläne ist damit nicht belegt ❓.", Q['geb']],
 ["In Österreich sei Homeschooling „ganz normal“ möglich, mit jährlicher Externistenprüfung [0:06], [0:19]", "Österreich kennt Unterrichts-, keine Schulpflicht. Vor der Pandemie wurden jährlich 2.300–2.600 Kinder (≈ 0,3 %) abgemeldet, 2021/22 7.515 (≈ 1 %), 2022/23 4.083, 2024/25 rund 1.800; seit der Verschärfung ist ein Reflexionsgespräch Pflicht.", Q['orf21'] + " · " + Q['orf25']],
 ["Ob man in Deutschland frei lernen dürfe (Gastgeber fragt) [0:23]; Wunsch nach freier Bildungsentscheidung [1:21]", "In Deutschland gilt Schulpflicht. Das BVerfG (2006) hielt sie für verhältnismäßig, u. a. wegen des Interesses, „Parallelgesellschaften“ entgegenzuwirken; der EGMR erklärte 2006 die Beschwerde einer Homeschooling-Familie (Konrad) für unzulässig.", Q['bverfg06'] + " · " + Q['konrad']],
 ["Leppe: Wer Kleinkindern eine Maske aufzwinge, sei ein Verbrecher [0:48]", "WHO und UNICEF rieten im August 2020, Kindern bis fünf Jahre keine Maske vorzuschreiben; für 6–11 Jahre empfahlen sie eine Abwägung nach Lage, ab 12 Jahren dieselben Regeln wie für Erwachsene. Die Wertung im Gespräch ist Leppes Sicht.", Q['who']],
 ["Corona-Homeschooling sei für viele eine Katastrophe gewesen (Gastgeber) [1:51–1:52]", "Das BVerfG leitete 2021 ein „Recht auf schulische Bildung“ ab, hielt die Schulschließungen der Bundesnotbremse (April–Juni 2021) aber für zulässig; Länder mussten Distanzunterricht anbieten. Der IQB-Bildungstrend 2021 fand in allen Bereichen signifikant mehr Viertklässler unter dem Mindeststandard als 2016 (Lesen +6, Mathe +6 Prozentpunkte).", Q['bverfg21pm'] + " · " + Q['iqb']],
 ["Mit Lerntechniken (bildhaft, lustig, emotional, verknüpft) lerne man den Stoff 50–90 % schneller [1:25–1:30]", "Die Übersichtsarbeit von Dunlosky u. a. (2013) zu zehn Techniken bewertet Üben mit Tests und verteiltes Lernen als hoch nützlich, Schlüsselwort-Mnemonik und Bilder zu Texten als gering nützlich (oft nur bei bestimmtem Material). Eine Zeitersparnis von 50–90 % für ganzen Schulstoff ist dort nicht belegt.", Q['dunlosky']],
 ["Linke Hirnhälfte sei für Neues, die rechte für Bilder und Emotionen zuständig [1:31–1:33]", "Bestimmte Funktionen sind lateralisiert (z. B. Sprache links). Eine Studie mit Ruhe-fMRT-Daten von über 1.000 Personen fand aber keine Belege, dass Menschen insgesamt „linkshirnig“ oder „rechtshirnig“ arbeiten. Die Aufteilung „links neu, rechts Bild“ ist in dieser Form nicht belegt ❓.", Q['nielsen']],
 ["Gegen Fingerrechnen gebe es „keine Studien“ [1:36]", "Studien zeigen ein gemischtes Bild: 2008 verbesserte ein Fingertraining bei Erstklässlern Zahlenleistungen; 2010 wurde das als möglicher Regressionseffekt kritisiert; 2020 brachte ein fingerbasiertes Training im Kindergarten keinen Vorteil gegenüber einer aktiven Kontrollgruppe. Ein Verbot wird durch diese Studien nicht gestützt, ein starker Nutzen aber auch nicht.", Q['finger08'] + " · " + Q['finger10'] + " · " + Q['finger20']],
 ["Indien und Südkorea seien in Mathe besser – „Fingerrechen-Länder“ [1:36]", "Südkorea: PISA 2022 Mathematik 527 Punkte (Deutschland 475, OECD 472). Indien nahm nur 2009 mit Tamil Nadu und Himachal Pradesh teil; beide lagen nahe am Tabellenende, rund 200 Punkte unter dem OECD-Schnitt.", Q['pisa22'] + " · " + Q['indien']],
 ["Zahlwörter bis 10.000 einer Fremdsprache in Ø 6–8 Minuten, getestet mit 70.000 Menschen [1:37]", "Eine unabhängige Untersuchung dieser Übung wurde nicht gefunden ❓. Gedächtnistechniken mit Orten oder Körperstellen (Loci-Prinzip) sind bekannt; Dunlosky u. a. stufen bildhafte Mnemonik insgesamt als gering nützlich für schulisches Lernen ein.", Q['dunlosky']],
 ["Gastgeber: Mehr Scheidungen als in den 60er-Jahren, „statistisch bewiesen“ [0:11]", "Rohe Scheidungsziffer Deutschland: 0,9 je 1.000 Einwohner (1960), Höchststand 2,6 (2003/2004), 1,7 (2021). Gegenüber 1960 höher, seit 2004 rückläufig.", Q['scheid']],
 ["Gastgeber: Schwarze US-Familien – 75 % „intakt“ in den 60ern, heute „vielleicht 25 %“ [0:12]", "Für diese Auswertung nicht geprüft ❓.", "❓ nicht geprüft"],
 ["Werner Schlager sei „einziger Tischtennisweltmeister Europas der letzten … 30 Jahre“ [0:27]", "Schlager wurde 2003 Weltmeister; er ist (Stand Januar 2026) der letzte Nicht-Chinese mit diesem Titel. Vor ihm gewannen auch andere Europäer (z. B. Jan-Ove Waldner 1997) – „einziger seit 30 Jahren“ trifft daher nicht genau zu.", Q['schlager']],
 ["Ross Edgley sei „ein halbes Jahr“ um Großbritannien geschwommen [0:30]", "2018: rund 1.780 Meilen (2.860 km) in 157 Tagen – gut fünf Monate; 2024 folgte der Yukon.", Q['edgley']],
 ["Das Gespräch ist Gunnar Kaiser gewidmet [0:00]", "Gunnar Kaiser, Autor und Webvideoproduzent, starb am 12. Oktober 2023.", Q['kaiser']],
 ["„Wir haben Steuergeld dort hingegeben“ – Schule sei teuer und bringe wenig [1:49], [0:39]", "Ausgaben je Schüler/in im Primarbereich (alle Träger): Deutschland 6.086 € (2012) → 9.228 € (2023), Österreich 8.033 € → 12.529 €. Der Anteil früher Schulabgänger (18–24 J. ohne Abschluss Sek. II, nicht in Ausbildung) lag 2024 in Deutschland bei 13,5 % (Zeitreihenbruch 2021), in Österreich bei 8,1 %, EU 9,6 %.", Q['ausg'] + " · " + Q['esl']],
]
abgleich_tab = {"typ": "tabelle", "kopf": ["Aussage im Gespräch", "Gängige Darstellung (Mainstream) / Daten 📚", "Quelle"], "stapel": True, "zeilen": abg}

DIAG = []
DIAG.append({"typ": "kurs", "id": "leppe-pisamathe", "titel": "📈 PISA Mathematik – Deutschland, Österreich, Südkorea",
 "reihen": [
  {"name": "Deutschland", "kurz": "DE", "einheit": "Punkte", "dez": 0, "hoeherGut": True, "punkte": [[2003, 503], [2006, 504], [2009, 513], [2012, 514], [2015, 506], [2018, 500], [2022, 475]]},
  {"name": "Österreich", "kurz": "AT", "einheit": "Punkte", "dez": 0, "hoeherGut": True, "punkte": [[2003, 506], [2006, 505], [2009, 496], [2012, 506], [2015, 497], [2018, 499], [2022, 487]]},
  {"name": "Südkorea", "kurz": "KR", "einheit": "Punkte", "dez": 0, "hoeherGut": True, "punkte": [[2003, 542], [2006, 548], [2009, 546], [2012, 554], [2015, 524], [2018, 526], [2022, 527]]}],
 "hoeherGut": True, "vergleich": True,
 "quelle": Q['wbmat'] + " (2003–2018, gerundet) · " + Q['pisa22'] + " (2022), abgerufen 12.11.2026",
 "hinweis": "Bezug zum Gespräch [1:36]: Leppe nennt Südkorea als Land, das in Mathe besser sei. Werte gerundet; 2022 aus dem nationalen PISA-Bericht."})
DIAG.append({"typ": "kurs", "id": "leppe-pisalesen", "titel": "📈 PISA Lesen – Deutschland und Österreich",
 "reihen": [
  {"name": "Deutschland", "kurz": "DE", "einheit": "Punkte", "dez": 0, "hoeherGut": True, "punkte": [[2003, 491], [2006, 495], [2009, 497], [2012, 508], [2015, 509], [2018, 498], [2022, 480]]},
  {"name": "Österreich", "kurz": "AT", "einheit": "Punkte", "dez": 0, "hoeherGut": True, "punkte": [[2003, 491], [2006, 490], [2009, 470], [2012, 490], [2015, 485], [2018, 484], [2022, 480]]}],
 "hoeherGut": True, "vergleich": True,
 "quelle": Q['wbrea'] + " (2003–2018, gerundet) · " + Q['pisaanh'] + " (2022), abgerufen 12.11.2026",
 "hinweis": "Bezug zum Gespräch [0:35–0:40]: These, Schule vermittle wenig Bleibendes. Der Einbruch Österreichs 2009 ist ungeklärt ❓ (Vergleichbarkeit hier nicht geprüft)."})
def es_series(d):
    return [[int(y), v] for y, v in d]
esl_de = [(2000,14.6),(2001,12.3),(2002,12.5),(2003,12.8),(2004,12.1),(2005,13.5),(2006,13.7),(2007,12.5),(2008,11.8),(2009,11.1),(2010,11.8),(2011,11.6),(2012,10.5),(2013,9.8),(2014,9.5),(2015,10.1),(2016,10.3),(2017,10.1),(2018,10.3),(2019,10.3),(2020,10.1),(2021,12.3),(2022,12.5),(2023,13.0),(2024,13.5),(2025,13.1)]
esl_at = [(2000,10.2),(2001,10.2),(2002,9.5),(2003,9.0),(2004,9.8),(2005,9.3),(2006,10.0),(2007,10.8),(2008,10.2),(2009,8.8),(2010,8.3),(2011,8.5),(2012,7.8),(2013,7.5),(2014,7.0),(2015,7.3),(2016,6.9),(2017,7.4),(2018,7.3),(2019,7.8),(2020,8.1),(2021,8.0),(2022,8.4),(2023,8.6),(2024,8.1),(2025,10.0)]
esl_eu = [(2002,16.9),(2003,16.4),(2004,16.0),(2005,15.6),(2006,15.2),(2007,14.7),(2008,14.3),(2009,14.0),(2010,13.8),(2011,13.2),(2012,12.6),(2013,11.8),(2014,11.1),(2015,11.0),(2016,10.6),(2017,10.5),(2018,10.5),(2019,10.1),(2020,10.0),(2021,9.7),(2022,9.6),(2023,9.6),(2024,9.6),(2025,9.1)]
DIAG.append({"typ": "kurs", "id": "leppe-abbrecher", "titel": "📈 Frühe Schul- und Ausbildungsabgänger (18–24 Jahre)",
 "reihen": [
  {"name": "Deutschland", "kurz": "DE", "einheit": "%", "dez": 1, "hoeherGut": False, "punkte": es_series(esl_de)},
  {"name": "Österreich", "kurz": "AT", "einheit": "%", "dez": 1, "hoeherGut": False, "punkte": es_series(esl_at)},
  {"name": "EU-27", "kurz": "EU", "einheit": "%", "dez": 1, "hoeherGut": False, "punkte": es_series(esl_eu)}],
 "hoeherGut": False, "vergleich": True,
 "quelle": Q['esl'] + ", Stand Abruf 12.11.2026 (Deutschland: Zeitreihenbruch 2021)",
 "hinweis": "Bezug zum Gespräch [0:33–0:42], [1:24]: Leppe hält Abschlüsse für überbewertet, rät aber, sie bei Bedarf nachzuholen. Anteil der 18- bis 24-Jährigen ohne Abschluss der Sekundarstufe II, die nicht in Ausbildung sind."})
aus_de = [(2012,6086.4),(2013,6298.8),(2014,6581.9),(2015,6716.8),(2016,6902.2),(2017,7088.8),(2018,7437.4),(2019,7978.0),(2020,8400.8),(2021,9006.0),(2022,9080.2),(2023,9227.7)]
aus_at = [(2012,8032.8),(2013,8659.3),(2014,8875.6),(2015,9339.9),(2016,9708.1),(2017,9825.2),(2018,10048.1),(2019,9688.7),(2020,10470.2),(2021,10998.0),(2022,11836.0),(2023,12529.2)]
DIAG.append({"typ": "kurs", "id": "leppe-ausgaben", "titel": "📈 Ausgaben je Schüler/in im Primarbereich (Grundschule)",
 "reihen": [
  {"name": "Deutschland", "kurz": "DE", "einheit": "€", "dez": 0, "hoeherGut": None, "punkte": es_series(aus_de)},
  {"name": "Österreich", "kurz": "AT", "einheit": "€", "dez": 0, "hoeherGut": None, "punkte": es_series(aus_at)}],
 "hoeherGut": None, "vergleich": True,
 "quelle": Q['ausg'] + " (ISCED 1, alle Träger, Euro, laufende Preise), Stand Abruf 12.11.2026",
 "hinweis": "Bezug zum Gespräch [1:49]: „wir haben Steuergeld dort hingegeben“. Nominalwerte, nicht inflationsbereinigt."})
sch = [(1960,0.9),(1965,1.0),(1970,1.3),(1975,1.7),(1980,1.6),(1985,2.1),(1990,1.9),(1995,2.1),(2000,2.4),(2003,2.6),(2004,2.6),(2005,2.4),(2010,2.3),(2015,2.0),(2018,1.8),(2019,1.8),(2020,1.7),(2021,1.7)]
DIAG.append({"typ": "kurs", "id": "leppe-scheidungen", "titel": "📈 Ehescheidungen in Deutschland je 1.000 Einwohner",
 "reihen": [{"name": "Rohe Scheidungsziffer", "kurz": "je 1.000", "einheit": "je 1.000 Einw.", "dez": 1, "hoeherGut": None, "punkte": es_series(sch)}],
 "hoeherGut": None, "vergleich": False,
 "quelle": Q['scheid'] + " (Auswahl von Jahren), Stand Abruf 12.11.2026",
 "hinweis": "Bezug zum Gespräch [0:11]: Der Gastgeber sagt, seit den 60er-Jahren gebe es mehr Scheidungen. Gebietsstand laut Eurostat „Deutschland“."})
DIAG.append({"typ": "balken", "titel": "📊 PISA 2022 Mathematik – Punkte im Vergleich", "einheit": "Punkte", "dez": 0,
 "zeilen": [["Japan", 536], ["Südkorea", 527], ["Österreich", 487], ["Deutschland", 475], ["OECD-Durchschnitt", 472]],
 "quelle": Q['pisa22'] + ", Stand Dezember 2023",
 "hinweis": "Bezug zum Gespräch [1:36]: „die ganzen Länder, die Mathematik besser sind“. Indien nahm an PISA 2022 nicht teil."})
DIAG.append({"typ": "balken", "titel": "📊 Häuslicher Unterricht in Österreich – Kinder zu Schulbeginn", "einheit": "Kinder", "dez": 0,
 "zeilen": [["vor 2020 (je Jahr, ca.)", 2400], ["2020/21 (ca.)", 2600], ["2021/22", 7515], ["2022/23", 4083], ["2024/25 (ca.)", 1800]],
 "quelle": Q['orf21'] + " · " + Q['orf25'] + " (Zahlen des Bildungsministeriums)",
 "hinweis": "Bezug zum Gespräch [0:06], [1:51–1:54]: In Österreich sei Homeschooling „ganz normal“ möglich; Lockdown-Erfahrungen. 2024/25: Stand Mai 2025 laut parlamentarischer Anfragebeantwortung."})

spann = {"typ": "abschnitt", "titel": "🧩 Spannungen im Gespräch", "liste": [
 "Der Gastgeber wendet ein, Genetik setze Grenzen (dünne Waden); Leppe stimmt für das Spitzenniveau zu, nicht für den Alltag [0:24–0:26].",
 "Als „Devil's Advocate“ fragt der Gastgeber, ob Kinder Lehrende nicht aus Antipathie abwählen würden; Leppe nennt Grundregeln und Gründe statt Mehrheit [1:06–1:09].",
 "Der Gastgeber fragt, ob ein Abschluss nicht doch nötig sei; Leppe stellt klar, er rate nicht zum Fernbleiben, nur zum Nachholen bei Bedarf [1:24].",
 "Zum Corona-Homeschooling bringt der Gastgeber die Gegenperspektive (Katastrophe in der Stadt); Leppe sieht den Grund in fehlender Vorbereitung der Eltern [1:51–1:54].",
 "Den Vergleich von Social Media mit Messer und Waffe lehnt der Gastgeber ab – wegen Suchtpotenzial [1:56].",
 "Zur Anthroposophie hält sich Leppe zurück, der Gastgeber äußert weitreichende Vermutungen über Okkultismus ❓ [1:15–1:18].",
 "Leppe betont, alles solle hinterfragt werden; mehrere seiner Zahlen (1,5 %, 70.000 Teilnehmende, 50–90 %) nennt er ohne überprüfbare Quelle.",
]}
mit = {"typ": "abschnitt", "titel": "💡 Was man mitnehmen kann", "liste": [
 "Die Rechtslage unterscheidet sich klar: Österreich erlaubt häuslichen Unterricht mit Prüfungen, Deutschland verlangt den Schulbesuch – von BVerfG und EGMR bestätigt.",
 "Sinkende Schulleistungen sind amtlich belegt (PISA 2022, IQB-Bildungstrend 2021) – die Ursachen werden unterschiedlich gedeutet.",
 "Zu Lerntechniken gibt es belastbare Forschung: Üben mit Abfragen und verteiltes Lernen gelten als besonders wirksam.",
 "Der Neuner-Fingertrick ist rechnerisch korrekt; die Studienlage zum Fingerrechnen ist gemischt, ein Verbot stützt sie nicht.",
 "Leppes Ziele (Dezentralisierung, freie Wahl, kostenlose Basisbildung) stehen auch auf seiner Website.",
]}
offen = {"typ": "abschnitt", "titel": "❓ Offen", "liste": [
 "Veröffentlichungsdatum des Videos und Name des Gastgebers.",
 "Die „1,5 %“-Studie zum behaltenen Schulstoff.",
 "Der MDR-Bericht und der Schweizer Zeitungsbericht über die Ausladung (Titel, Datum, genauer Inhalt).",
 "Wer „Reikabe“ und „Alexander Stier“ genau sind (Hörfehler möglich).",
 "Unabhängige Belege für 50–90 % Zeitersparnis und die Zahlen-Übung mit 70.000 Teilnehmenden.",
]}
weiter = {"typ": "abschnitt", "titel": "🔎 Weiter recherchieren", "liste": [
 "PISA- und IQB-Berichte im Original: " + Q['pisa22'] + ", " + Q['iqb'] + ".",
 "Dunlosky u. a. (2013) zu Lerntechniken: " + Q['dunlosky'] + ".",
 "Rechtslage Heimunterricht: " + Q['bverfg06'] + ", " + Q['konrad'] + ".",
 "Leppes eigene Inhalte: " + Q['wsf'] + ".",
 "Zur Geschichte der Schulpflicht: " + Q['glsr'] + ", " + Q['rschpfl'] + ".",
]}

# ======================= Zusammenbau =======================
reiter = [
 {"id": K, "titel": f"{G}: Überblick", "bloecke": [
  {"typ": "folge", "k": K, "titel": TITEL, "gast": GAST, "rolle": "Zauberer und Bildungsaktivist („WissenSchafft Freiheit“), Österreich",
   "kanal": KANAL, "datum": DATUM, "dauer": DAUER, "url": URL,
   "thema": "Ricardo Leppe erzählt bei REALTALK MEDIA von seiner Freilerner-Kindheit, erklärt, warum Schule aus seiner Sicht auf Gehorsam angelegt ist, zeigt Lerntechniken wie den Neuner-Fingertrick, spricht über die Vorwürfe gegen ihn und über Wahlfreiheit, Dezentralisierung und kostenlose Basisbildung.",
   "kacheln": []},
  {"typ": "hinweis", "text": "Auswertung nach dem Transkript (automatische Untertitel): Gesagtes ohne Zeichen, Ergänzungen 📚, Unklares ❓. Fundstellen [Stunde:Minute] springen ins Video. Die Bewertung bleibt dem Leser."},
  kurz, roter,
  {"typ": "text", "text": "🎯 **Kernaussagen** – die zehn wichtigsten Thesen des Gesprächs:"}, kern, baum,
  {"typ": "illu", "id": "leppe_lernweg", "titel": "Skizze: Schule heute und „Schule der Zukunft“ – Lernen nach Leppe (Darstellung laut Leppe, schematisch)"},
  {"typ": "illu", "id": "leppe_pflicht", "titel": "Skizze: Schulpflicht und Unterrichtspflicht – Stationen von 1717 bis 2025 (belegte Daten)"},
  steck]},
 {"id": K + "ab", "titel": f"{G}: Gespräch im Detail", "bloecke": [
  {"typ": "text", "text": f"🔎 Detaillierte Auswertung in der Reihenfolge des Gesprächs – {len(abschnitte)} Abschnitte. Lesehilfe: 💬 Zitat, 📌 Aussage/Zahl/Beispiel, 🔗 Bezug, 📚 Ergänzung, ❓ unklar. Video: [{TITEL}]({URL})"},
  {"typ": "gespraech", "titel": "🧭 Gesprächsverlauf – wann worüber gesprochen wird", "dauer": "1:58",
   "themen": [{"k": k, "n": n} for k, n in TH], "teile": teile}] + abschnitte},
 {"id": K + "zeit", "titel": f"{G}: Zeitachse & Verzeichnisse", "bloecke": [zeitachse, personen, orte, begriffe, zahlen]},
 {"id": K + "abgleich", "titel": f"{G}: Abgleich & Daten", "bloecke": [
  {"typ": "text", "text": "Neutraler Abgleich: links die Aussage im Gespräch, rechts die gängige Darstellung bzw. Daten mit Quelle. Die Bewertung bleibt dem Leser."},
  abgleich_tab] + DIAG + [spann, mit, offen, weiter]},
]

quellen = [[f"Video: {TITEL} – {KANAL} (YouTube)", URL]] + [link(k) for k in Q]
reiter[0]["bloecke"][0]["kacheln"] = [[str(len(abschnitte)), "Abschnitte"], ["10", "Kernaussagen"], [str(len(abg)), "Abgleich-Punkte"],
                                      [str(len(DIAG)), "Verläufe & Diagramme"], [str(len(quellen)), "Quellen"]]

out = {"k": K, "gast": GAST, "reiter": reiter,
 "folgen_zeile": [DATUM, "Ricardo Leppe (Zauberer, Bildungsaktivist)", TITEL,
   "Freilernen, Schulgeschichte & „unsichtbarer Lehrplan“, Lerntechniken, Vorwürfe & Medien, Wahlfreiheit & Dezentralisierung",
   "{{a:realtalk-leppe|hier: Leppe}}", f"[ansehen]({URL})"],
 "baum_ast": {"gruppe": "🎓 Bildung & Lernen", "t": "👤 Ricardo Leppe bei REALTALK MEDIA – Freilernen, Schulgeschichte, Lerntechniken, freie Bildung"},
 "neu": {"d": "2026-11-12", "t": "REALTALK MEDIA – Ricardo Leppe",
   "k": f"Warum Schule aus Leppes Sicht nicht funktioniert, Lerntechniken und freie Bildung – {len(abschnitte)} Abschnitte, Abgleich mit Quellen, {len(DIAG)} Diagramme.",
   "h": "#a-realtalk-leppe", "art": "Video"},
 "quellen": quellen,
 "web": [["Ricardo Leppe – WissenSchafft Freiheit", "https://wissenschafftfreiheit.com"],
         ["REALTALK MEDIA – YouTube-Kanal", "https://www.youtube.com/@REALTALK-GERMANY"]]}

here = os.path.dirname(os.path.abspath(__file__))
json.dump(out, open(os.path.join(here, "folge.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", len(abschnitte), "Abschnitte,", len(abg), "Abgleich,", len(DIAG), "Diagramme,", len(quellen), "Quellen,", len(ZA), "Zeitachse")
