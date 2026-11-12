# -*- coding: utf-8 -*-
# Erzeugt folge.json für „Okkulte Geheimdienst-Verbindungen von RAF bis Manson | Dirk Pohlmann“
# (K = pohlmannraf, Sammelstelle A-12 realtalk, Kanal REALTALK MEDIA)
import json, os, re
K = 'pohlmannraf'; G = 'Pohlmann RAF bis Manson'
URL = 'https://www.youtube.com/watch?v=moRX3qngEHc'
TITEL = 'Okkulte Geheimdienst-Verbindungen von RAF bis Manson | Dirk Pohlmann'
GAST = 'Dirk Pohlmann'
ROLLE = 'Journalist und Dokumentarfilmer; Mitbegründer der Reihe „Geschichten aus Wikihausen“'
KANAL = 'REALTALK MEDIA'
DATUM = '2026 ❓'
DAUER = '2 Std. 7 Min.'

# ---------- Quellen (alle per Suche/Abruf geprüft) ----------
Q = dict(
 ohne='[Wikipedia (en): Killing of Benno Ohnesorg](https://en.wikipedia.org/wiki/Killing_of_Benno_Ohnesorg)',
 urbach='[Wikipedia (en): Peter Urbach](https://en.wikipedia.org/wiki/Peter_Urbach)',
 becker='[LTO (06.07.2012): OLG Stuttgart – Verena Becker wegen Beihilfe zu vier Jahren Haft verurteilt](https://www.lto.de/recht/nachrichten/n/verena-becker-wegen-beihilfe-zum-mord-zu-vier-jahren-haft-verurteilt)',
 bka='[Baumann/Stephan/Wagner: (Um-)Wege in den Rechtsstaat. Das BKA und die NS-Vergangenheit seiner Gründungsgeneration, Zeithistorische Forschungen 1/2012 (PDF)](https://zeitgeschichte-digital.de/doks/files/1614/ZF_1_2012_33_53_Baumann_Stephan_Wagner.pdf)',
 nara='[U.S. National Archives: Vietnam War U.S. Military Fatal Casualty Statistics](https://www.archives.gov/research/military/vietnam-war/casualty-statistics)',
 tonkin='[National Security Archive (01.12.2005): Tonkin Gulf Intelligence „Skewed“ – NSA-Freigabe](https://nsarchive2.gwu.edu/NSAEBB/NSAEBB132/press20051201.htm)',
 mk='[US-Senat, gemeinsame Anhörung 03.08.1977: Project MKULTRA, the CIA’s Program of Research in Behavioral Modification (PDF)](https://www.intelligence.senate.gov/sites/default/files/hearings/95mkultra.pdf)',
 lookout='[U.S. Department of Energy, Nevada: Fact Sheet Lookout Mountain Laboratory (DOE/NV-1142, Archivkopie)](https://webarchive.library.unt.edu/eot2008/20090116053031/http://www.nv.doe.gov/library/factsheets/DOENV_1142.pdf)',
 ep='[Statewatch: Entschließung des Europäischen Parlaments zu Gladio vom 22.11.1990](https://statewatch.org/statewatch-database/gladio-resolution-of-the-european-parliament)',
 btgladio='[Deutscher Bundestag, Drucksache 17/14815 (04.10.2013): Maßnahmen der Bundesregierung zur Aufdeckung der Tätigkeiten von Gladio (PDF)](https://dserver.bundestag.de/btd/17/148/1714815.pdf)',
 franco='[Wikipedia (en): Allan Francovich](https://en.wikipedia.org/wiki/Allan_Francovich)',
 schleyer='[Konrad-Adenauer-Stiftung, Geschichte der CDU: Biogramm Hanns Martin Schleyer](https://www.kas.de/de/web/geschichte-der-cdu/personen/biogramm-detail/-/content/hanns-martin-schleyer-v1)',
 stamm='[Stuttgarter Zeitung (18.01.2019): Recherchen zur Todesnacht von Stammheim](https://www.stuttgarter-zeitung.de/politik/recherchen-zur-todesnacht-von-stammheim-wie-starben-ensslin-baader-und-raspe-78916449.html)',
 npd='[BVerfG, Pressemitteilung 22/2003: Einstellung der NPD-Verbotsverfahren](https://www.bundesverfassungsgericht.de/SharedDocs/Pressemitteilungen/DE/2003/bvg03-022.html?nn=69796)',
 klette='[LTO (27.05.2026): LG Verden – Ex-RAF-Terroristin Klette zu 13 Jahren Haft verurteilt](https://www.lto.de/recht/nachrichten/n/lg-verden)',
)
HILFE = 'Wenn dich das Thema belastet: Telefonseelsorge 0800 111 0 111 (kostenlos, rund um die Uhr).'

# ---------- Abschnitte (von, bis, th, Titel, Liste) ----------
A = [
("0:00","0:02","w","🎬 Teaser und Begrüßung bei „Good Morning Germany“",[
 "**Zusammenfassung:** Das Video beginnt mit vier Ausschnitten aus dem späteren Gespräch (BKA und SS, Prügelperser, Überfall-Muster bei Entführungen, „warum nehmen die uns nicht hoch?“). Der Gastgeber (Name im Video nicht genannt ❓) begrüßt zu „Good Morning Germany“ und stellt Dirk Pohlmann vor, der zum zweiten Mal zu Gast ist. Thema: die späten 1960er – 68er, Gründung der RAF, transatlantische Verbindungen, Hippie-Bewegung, Vietnam, Hollywood und Musik, „Okkultismus als Gewürz“.",
 "💬 „einen der besten Journalisten Deutschlands“ (Gastgeber über Pohlmann) [0:01]",
 "📌 Der Gastgeber sagt, er habe sich in den letzten ein, zwei Tagen eingelesen; Pohlmann sei der „beste Tanzpartner“ für das Thema [0:01].",
 "🔗 Zum anderen Gespräch derselben Reihe: Pohlmann über Geheimdienste, Epstein und Helmut Schmidt (zweites Gespräch, siehe Überblick)."]),
("0:02","0:09","a","🇮🇷 Drittes Reich als Ausgangspunkt, Schahbesuch und „Prügelperser“",[
 "**Zusammenfassung:** Der Gastgeber setzt beim Dritten Reich an: Ohne den Zweiten Weltkrieg und die vielen Altnazis im Apparat hätten die 60er nicht so gewirkt; er nennt Gladio, Dutschke, Vietnam. Dann der Schahbesuch 1967 – heute rede man im „Iran-Krieg“ von „47 Jahren Terrorherrschaft“, als sei davor alles gut gewesen. Pohlmann war 1967 acht Jahre alt: Er erinnert sich an eine ARD-Reportage, in der eine Kiste mit der Aufschrift „bitte nicht stürzen“ durchs Bild geschoben wurde, und an die „Prügelperser“: SAVAK-Leute hätten mit langen Stöcken auf Studenten eingeschlagen, die deutsche Polizei habe zugesehen. Schah und SAVAK seien damals stets zusammen genannt worden.",
 "📌 Pohlmann war Ende 1978/1979 bei der Bundeswehr (Marineflieger), als die Revolution im Iran begann; er verglich am Tisch Iran mit Vietnam, ein Bootsmann nannte ihn einen „Verräter“ [0:07].",
 "📌 Es habe nicht mit der RAF angefangen, sondern mit der Bewegung 2. Juni; der Eindruck „tolerierter Brutalität“ habe die Studenten geprägt [0:08] [seine Sicht].",
 "💬 „die sogenannten Prügelperser“ (Pohlmann) [0:05]"]),
("0:09","0:12","a","🕯️ Benno Ohnesorg, Notstandsgesetze, „Muff von 1000 Jahren“, Dutschke",[
 "**Zusammenfassung:** Pohlmann: Benno Ohnesorg sei von einem Polizisten „hingerichtet“ worden; das sei damals verschleiert worden. Ohnesorg gehörte zu einer eher protestantisch-christlich geprägten Gruppe, keine Kommunisten; die Sängerin Katja Ebstein (im Transkript „Epstein“) sei dabei gewesen und spreche offen darüber. Für die Studenten habe der Staat sein „wahres Gesicht“ gezeigt; Notstandsgesetze, „Unter den Talaren Muff von 1000 Jahren“, Sprüche wie „die gehören ins Lager“. Rudi Dutschke kam aus der DDR, war christlich geprägt – Pohlmann nennt ihn einen frühen „Befreiungstheologen“; Gretchen Dutschke brachte Einflüsse der US-Bürgerrechtsbewegung mit.",
 "📌 „Hingerichtet“ ist Pohlmanns Wort [seine Sicht]; 📚 Kurras wurde 1967 freigesprochen; 2012 berichtete der Spiegel nach Recherchen mit der Bundesanwaltschaft, der Schuss sei nicht in Notwehr gefallen (siehe Abgleich).",
 "🔗 Dutschke sei „verhasst“ gewesen bei einem großen Teil der älteren Öffentlichkeit [0:12]."]),
("0:12","0:16","a","🥊 Dutschke und Muhammad Ali – zwei Bewunderte",[
 "**Zusammenfassung:** Der Gastgeber nennt Dutschke den „brillantesten Geist“ der modernen deutschen Politik und vergleicht ihn mit Muhammad Ali, der als Wehrdienstverweigerer verhasst gewesen sei. Pohlmann stimmt zu: Ali sei unbestechlich und ein Intellektueller gewesen; er habe als Kind jeden Kampf mit seiner Mutter gesehen, im deutschen TV sei Ali als „Großmaul“ dargestellt worden. Dutschkes Engagement für Vietnam sei aus Liebe zu den Menschen, nicht aus Hass gekommen; er sei am Anfang der Grünen dabei gewesen, „da waren die Grünen noch was ganz anderes“.",
 "💬 „angefeuert von der Bild-Zeitung“ (Pohlmann über die Schüsse auf Dutschke) [0:16]",
 "📌 Empfehlung: Dutschke und Ali im Original anhören, um die Zeit zu verstehen [0:15–0:16]."]),
("0:16","0:19","c","🕵️ Gastgeber: Kurras als Stasi-Mann – alles Geheimdienstoperationen?",[
 "**Zusammenfassung:** Der Gastgeber skizziert den Bogen: Black Panthers, Hippies, Charles Manson, MKUltra, „Helter Skelter“ – Morde, die den Black Panthers in die Schuhe geschoben werden sollten. Dann zurück zu 1967: Karl-Heinz Kurras, der Ohnesorg erschoss, sei 2009 als Stasi-Spion (Deckname „Otto“) enttarnt worden. Seine These: Das alles seien Geheimdienstoperationen gewesen, Verfassungsschutz-Leute hätten als Provokateure gewirkt. Dutschke sei nach dem Attentat „angeblich“ zehn Jahre später an Spätfolgen gestorben – das wisse er nicht genau ❓.",
 "📌 Frage an Pohlmann: Hatte der Verfassungsschutz bei den Ausschreitungen vor dem Springer-Haus „die Finger im Spiel“? [0:18–0:19]",
 "📚 Laut Ermittlungen gibt es keinen Beleg, dass Kurras auf Stasi-Befehl schoss; die Ermittlungen wurden 2011 eingestellt (siehe Abgleich)."]),
("0:19","0:21","c","💣 Pohlmann: Pudding-Attentat, erste Waffen über V-Leute, FBI und Black Panthers",[
 "**Zusammenfassung:** Pohlmann: „Das sieht schwer danach aus.“ Aus der „Spaßguerilla“ – etwa dem Pudding-Attentat auf den US-Vizepräsidenten – sei es weitergegangen: Die ersten Sprengstoffe und Schusswaffen seien über Verfassungsschutz-Agenten in die Studentengruppen gekommen. Das erinnere an die USA, wo das FBI versucht habe, Bürgerrechtsbewegung und Black Panthers zu unterwandern und in Richtung Gewalt zu schieben; dort sei das nachgewiesen und die Dokumente seien größtenteils freigegeben. Vietnam sei den Amerikanern mit der Domino-Theorie erklärt worden.",
 "💬 „Das sieht schwer danach aus.“ (Pohlmann) [0:19]",
 "📌 Den Namen des Mannes, der die Waffen brachte, findet Pohlmann im Moment nicht; später nennt der Gastgeber Peter Urbach [0:19], [0:33].",
 "🔗 COINTELPRO wird später vom Gastgeber genannt [1:31]."]),
("0:21","0:24","b","🇻🇳 Ho Chi Minh und die französische Kolonialherrschaft",[
 "**Zusammenfassung:** Pohlmann holt aus: Die USA hätten Vietnams bester Freund sein können. Ho Chi Minh stamme aus einer aristokratischen Familie eines der rund 60 Völker Vietnams (Museum in Hanoi), sei sanft und gebildet gewesen, habe sich vom Kommunismus die Unabhängigkeit erhofft. Unter französischer Herrschaft in Indochina habe in jedem größeren Dorf eine Guillotine gestanden ❓; bei rund 25 Mio. Einwohnern habe es „4 Millionen Hungertote“ gegeben, weil Reis für Schnaps nach Frankreich gegangen sei ❓. Ho habe als Schiffsjunge und Tellerwäscher die Welt gesehen und in Paris heimlich Vorlesungen gehört.",
 "📌 Zahlen (60 Volksgruppen, 25 Mio. Einwohner, 4 Mio. Hungertote) [seine Angaben] – hier nicht geprüft ❓.",
 "💬 „die USA hätten der beste Freund von Vietnam sein können“ (Pohlmann) [0:22]"]),
("0:24","0:28","b","🤝 OSS, General Giap und die Unabhängigkeitserklärung",[
 "**Zusammenfassung:** Ho sei beeindruckt von amerikanischer Revolution und Verfassung gewesen. In einer kleinen Gruppe von sieben Revolutionären – darunter Giap, ein Geschichtslehrer – kämpfte er gegen die japanische Besatzung (Pohlmann: „in Japan“, gemeint wohl im Grenzgebiet ❓). Die USA schickten drei OSS-Offiziere, die die Viet Minh militärisch ausbildeten (Anekdote: Giap wollte in das Rohr des Granatwerfers schauen). Auf die Frage, ob er Kommunist sei, habe Ho geantwortet: ja, aber was sei der Unterschied zwischen ihm und George Washington? Nach dem Sieg über Japan verlas Ho die Unabhängigkeitserklärung – mit Teilen der amerikanischen Erklärung und der Erklärung der Menschenrechte von 1789 –, der OSS-Offizier neben ihm.",
 "💬 „Was ist denn eigentlich der Unterschied zwischen mir und George Washington?“ (Ho laut Pohlmann) [0:27]",
 "📌 Pohlmann beruft sich auf eine Dokumentation mit den drei OSS-Offizieren [0:30] (Titel ❓)."]),
("0:28","0:31","b","⚖️ Potsdam, Rückkehr Frankreichs – „You don't understand politics, son“",[
 "**Zusammenfassung:** Auf der Potsdamer Konferenz sei Vietnam den Briten zugeschlagen worden, die es nicht wollten; dann kehrten die Franzosen zurück. Ho und die OSS-Offiziere seien gleichermaßen fassungslos gewesen; einem OSS-Offizier sei gesagt worden: „You don't understand politics, son.“ Die USA lieferten Überschusswaffen an Frankreich. Ho habe keinen Krieg mehr gewollt, aber keinen anderen Weg gesehen und die Amerikaner danach nur noch „Banditen“ genannt. Das habe Dutschke gewusst.",
 "📌 Die drei OSS-Offiziere hätten in der Doku gesagt, die Vietnamesen wären „unsere besten Freunde in Asien“ gewesen [0:30].",
 "📚 Laut gängiger Darstellung wurde Vietnam in Potsdam am 16. Breitengrad geteilt: der Norden an China, der Süden an Großbritannien zur Entwaffnung der Japaner (Quelle hier nicht geprüft ❓)."]),
("0:31","0:34","b","💥 58.000 gegen drei Millionen – Krieg, Hollywood und Iran",[
 "**Zusammenfassung:** Die Vietnamesen hätten nacheinander Franzosen, Amerikaner und China „und die Malaria“ besiegt. Auf Vietnam seien mehr Bomben gefallen als im ganzen Zweiten Weltkrieg ❓; die Arroganz erinnere an den heutigen Krieg gegen Iran, wo man sich ebenfalls verrechne (Verweis auf Mohammad Marandi). 58.000 Amerikaner seien gestorben, ihre Namen stünden an einer Wand; in Hollywood-Filmen (außer „Good Morning, Vietnam“) seien Vietnamesen nur Staffage. Drei Millionen Vietnamesen seien umgekommen – „und kein Schwein interessiert sich dafür“. Der Gastgeber fragt, wer da eigentlich gewonnen habe, und vermutet die Rüstungsindustrie.",
 "📌 Pohlmann: Dutschke „wusste, was er gerufen hat“ („Ho Ho Ho Chi Minh“) [0:33].",
 "📚 US-Gefallene laut National Archives: 58.220 (siehe Abgleich und Diagramm).",
 "❓ Zahl der vietnamesischen Toten und Bombentonnage hier nicht geprüft."]),
("0:34","0:37","c","🔥 Gastgeber: Peter Urbach, Springer-Blockade – war auch die Hippie-Bewegung eine Operation?",[
 "**Zusammenfassung:** Der Gastgeber fasst zusammen: Ohnesorg von einem Stasi-Mann erschossen, ein Jahr später Kopfschuss auf Dutschke, Ausschreitungen. Peter Urbach („S-Bahn-Peter“) vom Verfassungsschutz habe die Kommune 1 als angeblicher Handwerker infiltriert, Waffen verkauft und vor dem Springer-Haus Molotowcocktails mitgebracht und gezeigt, wie man Lieferwagen umkippt. Er schreibe an seinem ersten Buch „Die Destabilisierung von Deutschland“. Seine Frage: Könnte die Hippie-Gegenkultur selbst eine Geheimdienstoperation gewesen sein, um legitimen Protest zu diskreditieren, und die RAF instrumentalisiert worden sein?",
 "💬 „ja, ja, äh, viel ja, äh, etwas nein“ (Pohlmann auf die These) [0:37]",
 "📚 Urbach war V-Mann des Berliner Verfassungsschutzes; 2005 wurde bekannt, dass er die Bombe für den Anschlagsversuch auf das Jüdische Gemeindehaus am 9.11.1969 lieferte (siehe Abgleich)."]),
("0:37","0:40","c","🏛️ Geheimdienst im grauen Feld, Adenauer-Staat und das BKA",[
 "**Zusammenfassung:** Pohlmann erklärt, wie so etwas funktioniere: Anders als die Polizei arbeite der Geheimdienst im grauen und schwarzen Feld. Westdeutschland sei verlogen gewesen, weil Adenauer (selbst „kein Nazi“) die vielen Belasteten einbaute, um einen Bürgerkrieg zu vermeiden. Beispiel BKA (aus seiner Doku): Erster Chef Paul Dickopf habe einen SS-Dienstgrad gehabt, drei Viertel der Führung seien ehemalige SS-Leute gewesen; ein Mann, der für die Verfolgung der Sinti und Roma zuständig gewesen sei, habe ein Referat geleitet. Für diese Leute sei der Krieg ein Kampf gegen den Kommunismus gewesen, den man nun fortführte.",
 "📌 Das Zitat „Wir haben das falsche Schwein geschlachtet“ werde Churchill zugeschrieben – „hat er übrigens nicht gesagt“ (Pohlmann selbst) [0:40].",
 "📌 Infiltration diene zwei Zwecken: herausfinden, was los ist, und Gruppen radikalisieren, damit man sie „abräumen“ kann [0:40] [seine Sicht].",
 "📚 Studie im Auftrag des BKA (2011/2012): Ende der 1950er waren etwa drei Viertel der Führung frühere NSDAP-, zwei Drittel frühere SS-Mitglieder; Josef Ochs wirkte 1940 an der Deportation von Sinti mit und vertrat später die BKA-Interessen „im Umgang mit Sinti und Roma“ (siehe Abgleich)."]),
("0:40","0:42","d","🧱 Bommi Baumann und die „Haschrebellen“",[
 "**Zusammenfassung:** Pohlmann erzählt eine Anekdote aus Gesprächen mit Michael „Bommi“ Baumann, den er als „grundehrlichen Menschen“ schätzte: Betonfacharbeiter, „einziger Proletarier“ unter Studenten, Mitglied des „Zentralrats der umherschweifenden Haschrebellen“, später Bewegung 2. Juni, kannte Ohnesorg und alle RAF-Leute; Buch „Wie alles anfing“. Sein Freund Georg von Rauch wurde von der Polizei erschossen – Baumann habe gesagt, Rauch werde die Waffe wohl gezogen haben.",
 "📌 Baumann sei nach der Haft von Volker Weingraber Edler von Grodeck (Schreibweise ❓) abgeholt worden [0:42]."]),
("0:42","0:46","d","🏠 Die Wohnung des Agenten: Weingraber, Verena Becker, Yachtclub-Bombe",[
 "**Zusammenfassung:** Weingraber habe eine große Wohnung in Berlin gehabt, eine Art Kommune; dort habe sich nach Ohnesorgs Tod die gesamte Szene getroffen, aus der Bewegung 2. Juni und RAF hervorgingen (Pohlmann nennt Anwesende, u. a. Inge Viett; ob Otto Schily mit seiner ersten Frau dort war, ist hier nicht geprüft ❓). Baumann habe gesagt, er habe Verena Becker „angeschleppt“, die Bomben in Bahnhofsschließfächern vorgeschlagen habe [Baumanns Bericht laut Pohlmann ❓]. Becker sei später Verfassungsschutz-Agentin gewesen, „wir wissen nicht genau, ab wann“. Nach der Bombe im britischen Yachtclub, bei der ein Hausmeister starb ❓, sei Baumann ausgestiegen. Jahrzehnte später sei Weingraber in einem Prozess als Verfassungsschutz-, dann BND-Agent enttarnt worden und habe als Abfindung ein Weingut in der Toskana (über 1 Mio. DM) erhalten ❓.",
 "💬 „Diese ganze Raffscheiße hat angefangen in der Wohnung von einem …“ (Baumann laut Pohlmann) [0:45]",
 "📚 Zu Becker: OLG Stuttgart 2012 – vier Jahre wegen Beihilfe zum Mord an Generalbundesanwalt Buback; Informationen an den Verfassungsschutz Anfang der 1980er in der Haft gegen Geld und Vergünstigungen; weitergehende Vorwürfe sah das Gericht nicht belegt (siehe Abgleich).",
 "❓ Weingrabers Rolle, die Abfindung und die Yachtclub-Angaben konnten hier nicht mit Quelle geprüft werden."]),
("0:46","0:49","c","🪖 Benjamin Fischer, die Stasi-Ausbildung und die Peacenik-Bewegung",[
 "**Zusammenfassung:** Die Lehre: Terror wird nicht von Anfang an geplant, man greift die Leute ab und schaut, wie man sie nutzen kann. Pohlmann wollte den damaligen CIA-Chefhistoriker Benjamin Fischer interviewen; der habe zugesagt und dann abgesagt. Fischer habe in einem Aufsatz geschrieben, dass Führungsleute der zweiten RAF-Generation in der DDR (Spreewald) ausgebildet wurden und im Kriegsfall zusammen mit in der DDR geschulten DKP-Gruppen („AGMS“ ❓) Sabotage und gezielte Tötungen ausführen sollten ❓. Auch die Friedensbewegung, „verweiblicht“ und anders als der Kurzhaar-Amerikaner, habe man unterwandern wollen – entweder als Untergang des Abendlandes darstellen oder als gefährlich: „Das ist dann Charles Manson.“",
 "📌 Leary sei nicht der Böse gewesen; Bewusstseinserweiterung habe vom kapitalistischen Weltbild weggeführt und sei dann „genutzt“ worden [0:48].",
 "❓ Fischers Aufsatz (Titel, Ort) konnte hier nicht gefunden werden."]),
("0:49","0:52","c","🌿 Pläne funktionieren nie – Rote Brigaden, Grüne und die „Epstein-Klasse“",[
 "**Zusammenfassung:** Pohlmann warnt vor der Vorstellung eines Plans, der genau abläuft – Pläne müssten ständig nachjustiert werden. Beispiel Syrien: Erst sei der IS das Schlimmste gewesen, heute sei ein früherer Dschihadisten-Anführer Präsident, Assad sei dagegen „zu weich“ gewesen. Dahinter stehe die „Epstein-Klasse“, ein „bösartiger Moloch“, zu dem CIA und – amateurhafter – der Verfassungsschutz gehörten. Ein italienischer Historiker habe ihm gesagt, die Roten Brigaden seien von SISMI, CIA und etwas KGB unterwandert gewesen. Gefährlich seien glaubwürdige Führungsfiguren – Petra Kelly, Antje Vollmer, Dutschke, Beuys; 40 Jahre später seien die Grünen die kriegsfreudigste Fraktion: „erfolgreiche CIA-Politik“ [seine Sicht].",
 "📌 Jutta Ditfurth beschreibe eine USA-Reise, bei der ihr gesagt worden sei, ohne „uns“ gäbe es die Grünen nicht (laut Pohlmann ❓).",
 "💬 „an ihren Früchten sollt ihr sie erkennen“ (Pohlmann, Bibelwort) [0:50]"]),
("0:52","0:55","c","🚕 Bürgerinitiativen, der Film „Carlos“ und Italiens Taxifahrer",[
 "**Zusammenfassung:** Jede erfolgreiche Bürgerinitiative, etwa ein Kanal mit 200.000 Followern, werde irgendwann „bearbeitet“. Der Regisseur des Films „Carlos“ habe gesagt: Wer der Spur des Terrorismus folgt, landet an der Tür eines Geheimdienstes. In Italien wisse das jeder Taxifahrer; in Deutschland gelte man als Verschwörungstheoretiker und werde nicht ins ZDF eingeladen – ein „tiefes Tal der arroganten Ahnungslosen“. Der Gastgeber: Es sei „ja bewiesen“, dass der Verfassungsschutz Waffen geliefert, zu Anschlägen angestiftet und die RAF durchgehend überwacht habe; schwerer greifbar sei das internationale Zusammenspiel. Auch Hip-Hop sei „wahrscheinlich“ eine CIA-Operation, nicht als solche geboren, aber vereinnahmt [seine Sicht].",
 "💬 „landest du immer an der Tür eines Geheimdienstes“ (Regisseur von „Carlos“ laut Pohlmann) [0:54]",
 "📚 Belegt sind Einzelfälle wie Urbach und Becker; eine durchgehende Steuerung ist damit nicht belegt (siehe Abgleich)."]),
("0:55","0:58","f","🌼 Gastgeber: Hippies, Laurel Canyon und okkulte Ebene",[
 "**Zusammenfassung:** Der Gastgeber führt die „rituelle, okkulte Ebene“ ein – spätestens seit Epstein sei das „nicht mehr anzufechten“. Die Hippie-Bewegung sei „sehr fragwürdig“: Bands wie The Byrds („Birds“) und The Mamas and the Papas, Schauspieler wie die Fondas, Jack Nicholson, Marlon Brando, Regisseur Roman Polanski. Anton LaVey habe die Church of Satan gegründet, Sammy Davis Jr. sei Mitglied gewesen; Aleister Crowley habe „das Cover der Beatles gezeichnet“ ❓, Jimmy Page (Led Zeppelin) habe später Crowleys Anwesen gekauft. Alles sei in Los Angeles, im Laurel Canyon, Ende der 60er kultiviert worden.",
 "📌 Crowley habe sich selbst den „bösesten Menschen der Welt“ genannt (Gastgeber) [0:57].",
 "📚 Crowley ist auf dem Cover von „Sgt. Pepper's“ abgebildet; dass er es gezeichnet habe, ist nicht belegt (Quelle hier nicht geprüft ❓)."]),
("0:58","1:01","f","🎥 Lookout Mountain, MKUltra-Behauptungen und der Mord an Sharon Tate",[
 "**Zusammenfassung:** Der Gastgeber: Auf dem Lookout Mountain habe es eine geheime Militärbasis gegeben, später ein Studio, das „10.000 Filme“ produziert habe – Pohlmann ergänzt, ein Bekannter sei dort gewesen, dort seien die Atomtests gefilmt worden; der Gastgeber meint, dort seien proportional die meisten Hollywood-Filme gedreht worden ❓. Es habe Drogenhandel gegeben, „Runaways“ seien angezogen worden; bei MKUltra sei offiziell zugegeben, dass man Experimente mit Kindern gemacht habe, „die wahrscheinlich nicht vermisst wurden“ ❓. Dann der Tate-Mord: Polanskis Film „Rosemary's Baby“ handle von einer Schwangeren, die den Antichristen austrägt; seine schwangere Frau Sharon Tate wurde von der Manson Family ermordet – laut Gastgeber deute alles auf eine „okkulte Operation“ [seine Sicht].",
 "📚 Laut US-Energieministerium drehte das Lookout Mountain Laboratory in 22 Jahren über 6.500 Filme für die Atomenergiekommission und andere Behörden; Personal kam aus Hollywood-Studios (siehe Abgleich).",
 "📚 Die Senatsanhörung 1977 nennt 149 Unterprojekte und 80 Einrichtungen; von Experimenten an Kindern ist dort in den geprüften Teilen nicht die Rede ❓."]),
("1:01","1:04","f","☮️ „Ewige Blumenkraft“, Peace-Zeichen, Bücher und der Golf von Tonkin",[
 "**Zusammenfassung:** Der Gastgeber: New Age, die Beatles mit „Kali-Anbetung“, „Flower Power“ – „Ewige Blumenkraft“ sei der Slogan des Illuminatenordens gewesen (Pohlmann kannte das nicht) ❓; Adam Weishaupt sei von Jesuiten unterrichtet worden. Das Peace-Zeichen sei ein umgedrehtes Kreuz ❓. Polanskis Freund Wojciech Frykowski habe vor dem Mord vor dem Ort gewarnt ❓; dessen Sohn sei 1999 ähnlich getötet worden ❓ (Zahlenspiel mit 6). Buchtipps: David McGowan „Weird Scenes Inside the Canyon“ und Tom O'Neill „Chaos“. Polanski sei kurz darauf wegen sexuellen Missbrauchs einer 13-Jährigen im Haus Jack Nicholsons „überführt“ worden (Aussage des Gastgebers; Stand des Verfahrens hier nicht geprüft ❓). Jim Morrisons Vater sei Admiral beim „Fake-Angriff“ im Golf von Tonkin gewesen.",
 "💬 „Unfassbar komplex, aber … übertrieben spannend“ (Gastgeber) [1:03]",
 "📚 NSA-Freigabe 2005: Den Angriff vom 4.8.1964 gab es nicht; den Angriff auf die USS Maddox vom 2.8.1964 gab es (siehe Abgleich)."]),
("1:04","1:07","g","🍄 Pohlmann: LSD, Albert Hofmann und die Mysterien von Eleusis",[
 "**Zusammenfassung:** Pohlmann: Manson habe eine Verbindung zu MKUltra gehabt, er sei „ein Objekt“ gewesen ❓. LSD stamme vom Schweizer Chemiker Albert Hofmann, der einen ganz anderen Zugang hatte (Verweis auf Mathias Bröckers). Es gebe eine Verbindung zu Eleusis, dem wichtigsten Mysterium der Antike über 1.000 Jahre – Platon sei fünfmal dort gewesen ❓; dort sei wohl Mutterkorn genutzt worden. In Eleusis hätten Menschen durch Initiation erfahren, dass sie Seele und Geist in einem vergänglichen Körper sind; ähnlich heute Ayahuasca (DMT). Hofmann habe Schizophrenie bekämpfen wollen ❓, sei über 100 geworden und ein „untadeliger“ Mensch gewesen.",
 "📌 Mutterkorn enthalte „Lysergsäure-Ethylamid“, LSD sei „Lysergsäure-Diethylamid“ (Pohlmann) – chemische Angabe hier nicht geprüft ❓.",
 "📌 Keine Konsumanleitung; Gesundheitsfragen zu Psychedelika gehören zu Fachstellen."]),
("1:07","1:10","g","🧪 CIA-Experimente, LSD in der Tschechoslowakei",[
 "**Zusammenfassung:** Die CIA habe gesehen, was man mit LSD anfangen könne, und ohne Verantwortung experimentiert – mit Prostituierten und Leuten von der Straße, die nicht wussten, was mit ihnen geschah ❓. Auch die Sowjetunion habe sich interessiert (laut Gesprächspartnern seiner Doku); die Tschechoslowakei sei zeitweise größter LSD-Produzent der Welt gewesen und habe mit Filmakademien zusammengearbeitet – vielleicht auch mit Łódź, wo Polanski lernte ❓. Man habe LSD an eine Raketenabteilung der tschechischen Armee gegeben, um zu testen, ab welcher Dosis keine Befehle mehr möglich sind ❓.",
 "📚 Belegt ist, dass die CIA unter MKUltra 1953–1964 verhaltensändernde Substanzen erforschte (Senatsanhörung 1977); Einzelheiten zur ČSSR hier nicht geprüft ❓."]),
("1:10","1:16","g","🕯️ Rituale, eine schwarze Messe und Remote Viewing",[
 "**Zusammenfassung:** Pohlmann kündigt eine eigene Sendung zu Drittem Reich und Okkultismus an. Die „Epstein-Klasse“ – extrem einflussreich oder reich – suche nach Steigerung; in Ritualen seien Erfahrungen von Macht möglich, die real seien oder als real erlebt würden. Anekdote: Ein Kommilitone (Exilpole) habe aus Spaß in der Pfalz eine schwarze Messe gefeiert; eine junge Frau aus katholischem Elternhaus sei „ausgeflippt“, man habe abgebrochen. Folgerung: „da ist etwas“ – man solle sich spirituell erden. Epstein müsse wie der Kennedy-Mord aufgearbeitet werden, mit Konsequenzen. Remote Viewing funktioniere „nicht 100 %, aber so gut“, dass er nicht glaube, es sei nach 23 Jahren beendet worden ❓. Dazu Filme wie „Der Exorzist“, Pornografisierung und Vereinzelung.",
 "📌 Lob an den Gastgeber: gute „Spürnase“, aber „pass auf, dass du dich nicht wegtragen lässt“ [1:15].",
 "📌 Hollywood-Filme seien „perfekt gemacht, aber tot“ – sie schütteln von außen statt innerlich zu bewegen [1:16] [seine Sicht].",
 "❓ Pohlmann nennt das OSS einen „britischen Geheimdienst“ [1:13] – das OSS war ein US-Dienst (📚 allgemein bekannt)."]),
("1:16","1:20","h","🛸 Indien, das Buch Henoch, Blue Beam und „unsere Demokratie“",[
 "**Zusammenfassung:** Das Interesse der 68er an Indien vergleicht Pohlmann mit der China-Begeisterung Europas im 17./18. Jahrhundert – richtig, aber ein Gang auf schmalem Pfad. In der UFO-Debatte verwiesen Leute aus dem US-Kongress auf das Buch Henoch (äthiopische Bibel) ❓; erstaunlich sei, dass Gläubige damit besser zurechtkämen als Ungläubige. Der Gastgeber schlägt eine eigene Sendung über UFOs, Henoch und „Project Blue Beam“ vor. Pohlmann: gesundes Misstrauen, dass Mächtige solche Dinge nutzen, um zu führen; wer „unsere Demokratie“ sage, meine „ihre“.",
 "💬 „Ich werde keine Anweisung ausführen und nichts einfach glauben“ (Pohlmann) [1:20]"]),
("1:20","1:25","f","🐇 Gastgeber: Zauberer von Oz, Alice im Wunderland, Wonderland Avenue",[
 "**Zusammenfassung:** Pohlmann: Projektion als Idee – etwa eine Marienerscheinung vor Kuba für eine Konterrevolution ❓. Der Gastgeber schließt ab: MKUltra-Überlebende berichteten von Elektroschocks, Misshandlung, gezielter Persönlichkeitsspaltung; fast alle Akten seien vernichtet, „10 %“ übrig. Viele erzählten, ihnen seien „Der Zauberer von Oz“ und „Alice im Wunderland“ gezeigt worden. Die nach Manson zweitbekanntesten Morde („Four on the Floor“ ❓) seien in der Wonderland Avenue geschehen; Lewis Carroll sei „wahrscheinlich pädophil“ gewesen ❓. „Das muss nicht sein, dass es alles zusammenhängt. Es kann aber.“",
 "📌 Pohlmann kennt „Four on the Floor“ nicht [1:24].",
 "📚 Laut Senatsanhörung 1977 wurden die MKUltra-Akten im Januar 1973 vernichtet; 1977 fand man sieben Kisten (vor allem Finanzunterlagen, rund 8.000 Seiten) – eine Quote von 10 % nennt die Anhörung nicht ❓."]),
("1:25","1:31","h","🔎 „Verschwörungssachverständiger“ – Caesar, Suez, 9/11 und Haaretz",[
 "**Zusammenfassung:** Pohlmann: Er sei kein Verschwörungstheoretiker, sondern „Verschwörungssachverständiger“ – nüchtern bleiben, „den inneren Sherlock Holmes anschalten“. Ein CIA-Mann habe ihm gesagt, er habe sein ganzes Berufsleben mit Verschwörungen verbracht, sie aufzudecken oder auszudenken. Xavier Naidoo habe mit dem Kompass „vielleicht 10 Grad daneben“ gelegen, aber die Richtung habe gestimmt (Epstein-Files) [seine Sicht]. Geschichte stecke voller Verschwörungen: Caesar, der Suez-Krieg 1956 (Absprache Großbritannien, Frankreich, Israel). Wer sich mit 9/11 beschäftige, dessen Karriere sei beendet. Vor 14 Jahren habe er in einer Doku gezeigt, dass Deutschland Israels Atomprogramm bezahlt habe – das gelte als Verschwörungstheorie, bis es in Haaretz stand ❓. Lieblingsfilm: „Der Name der Rose“.",
 "💬 „ich bin Verschwörungssachverständiger“ (Pohlmann) [1:25]",
 "📌 Der Gastgeber fasst zusammen (Ohnesorg-Täter freigesprochen und Stasi-Spitzel, Operation CHAOS, COINTELPRO, Schleyer, Moro) und bittet um eine Gesamterklärung [1:30–1:31].",
 "❓ Der Haaretz-Artikel und Pohlmanns Doku sind hier nicht geprüft."]),
("1:31","1:35","e","🇮🇹 Italien: Angleton, Gladio, Mafia und der „historische Kompromiss“",[
 "**Zusammenfassung:** Italien biete viel Drama, aber die Aufklärung sei viel besser gelaufen als in Deutschland, dem „stinkenden Tümpel“. Nach dem Krieg hätten fast die Kommunisten die erste Wahl gewonnen; das habe die CIA unter James Jesus Angleton verhindert, dazu sei Gladio aufgebaut worden – „jedes Verbrechen ist erlaubt“ gegen den Kommunismus. Im Krieg hätten die USA die Mafia genutzt (Lucky Luciano) und nach Italien zurückgebracht. Aldo Moro (Democrazia Cristiana, selbst nicht mafianah) habe die Mafia bekämpfen, eine nicht-imperiale Mittelmeerpolitik betreiben (wie Enrico Mattei) und mit den Kommunisten den „compromesso storico“ schließen wollen. Die USA hätten gewarnt: In Italien mit der 6. Flotte und starkem Gladio-Netz (wie in der Türkei) komme kein Kommunist in die Regierung.",
 "📚 Das Europäische Parlament verlangte am 22.11.1990 die Aufklärung und Auflösung geheimer paramilitärischer Netze (siehe Abgleich).",
 "❓ Angletons Rolle 1948 hier nicht mit Quelle geprüft."]),
("1:35","1:40","e","☎️ Kissinger-Warnung, die BBC-Serie „Gladio“ und der Maulwurf bei den Roten Brigaden",[
 "**Zusammenfassung:** Moros Witwe habe im Untersuchungsausschuss ausgesagt, Kissinger habe ihn persönlich gewarnt; in einem anderen Telefonat seien „physische Konsequenzen“ angedroht worden ❓. Moro wurde von den Roten Brigaden entführt. Pohlmann empfiehlt die dreiteilige BBC-Dokumentation „Gladio“: Deren Regisseur sei bei der Einreise in die USA am Zoll tot zusammengebrochen, während er an einer Lockerbie-Doku arbeitete; ein CIA-Mann habe ihm erzählt, man habe ihn mit einem „Binärgift“ getötet [Behauptung, die Pohlmann wiedergibt; nach eigenen Worten „nicht nachweisbar“]. In der Doku erzähle Rote-Brigaden-Gründer Franceschini: Man habe Leute entführen, verhören und die Verhöre veröffentlichen wollen; Hardliner hätten Morde gefordert. Nach einem Hinweis auf einen Maulwurf seien drei der vier Anführer verhaftet worden, der vierte sei Chef geworden ❓.",
 "📚 Allan Francovich starb am 17.04.1997 im Zollbereich des Flughafens Houston; angegebene Ursache: Herzinfarkt (siehe Abgleich).",
 "❓ Aussage von Eleonora Moro und Einzelheiten zur Verhaftung hier nicht geprüft."]),
("1:40","1:42","e","🎯 Moros Tod, gleiche Handschrift wie bei Schleyer, „deutsche Kommandos“",[
 "**Zusammenfassung:** Moro habe in der Haft verstanden, dass er geopfert werden sollte; seine Leiche sei genau auf halbem Weg zwischen den Zentralen von Christdemokraten und Kommunisten abgelegt worden – „ein kleiner Hinweis“. Er habe Briefe geschrieben („Mein Blut wird über euch kommen“ ❓). Auf die Frage des Gastgebers nach deutschen Befehlen: Der Überfall auf Moro sei eine Kopie des Überfalls auf Schleyer gewesen – Kinderwagen auf die Straße, Auto bremst, ein zweites blockiert, Feuer aus Maschinenpistolen, Entführung, Verhör. Bei Recherchen um 1989 ❓ im Stasi-Archiv (Abteilung für Terrorabwehr) habe er Zeugenaussagen gefunden: sehr gute Schützen, offenbar militärisch geschult, Verfassungsschutz-Leute vor Ort, deutsche Kommandos gerufen ❓.",
 "💬 „Ich habe nicht mehr alles immer in meinem Kopf“ (Pohlmann zur Aktenlage) [1:42]",
 "📚 Schleyer wurde am 5.9.1977 in Köln entführt; dabei wurden sein Fahrer und drei Polizeibeamte erschossen (siehe Abgleich)."]),
("1:42","1:46","d","👂 „Warum nehmen die uns nicht hoch?“ – Überwachung, Stammheim, Wahrheitskommission",[
 "**Zusammenfassung:** Die übliche Version – kluge Terroristen, gutwillige, aber „stoffelige“ Polizei – sei „Bullshit“. Die dritte Generation habe gewusst, dass sie überwacht wurde, und sich gefragt, warum man sie nicht festnimmt; sie habe sich „Beschützungstheorien“ gebastelt (etwa Schutz durch die DDR). Stammheim sei komplett abgehört worden. In seinem Buch über den Herrhausen-Mord (noch unveröffentlicht) gehe es auch darum. Sein Vorschlag: eine Wahrheitskommission wie in Südafrika – Straffreiheit für wahre Aussagen, volle Härte bei nachgewiesener Lüge.",
 "💬 „nicht Verschwörungstheorien, sondern Beschützungstheorien“ (Pohlmann) [1:44]",
 "📌 Er habe „viele Probleme“ damit, was „mit mir gemacht werden soll“, bevor er das Buch veröffentliche [1:46]."]),
("1:46","1:50","h","🕊️ Südafrika, Olof Palme, die Amish – und „Geschichts-Alzheimer“",[
 "**Zusammenfassung:** In Südafrika hätten Aussagende vor der Wahrheitskommission von Plänen gegen Olof Palme berichtet („Long Reach“ ❓); Schweden habe an der Einzeltäter-Version festgehalten. RAF-Leute seien heute Rentner; zu wissen, was war, sei so wichtig wie für die USA der Kennedy-Mord, „das Urverbrechen“. Christliches Motiv: Reue, Aussage, Vergebung – Anekdote von Amish, die einen reuigen Mörder unter Aufsicht versteckten ❓. RAF-Mitglieder seien zum Teil für Taten verurteilt, die sie nicht begangen hätten ❓; da Mord nicht verjährt, schwiegen sie. Fragen an eine Kommission: Wie viel geschah im Auftrag des Staates, wie ehrlich war der Kampf gegen den Terror?",
 "💬 „der erleidet an Geschichts-Alzheimer“ (Pohlmann über fehlende Mustererkennung) [1:50]",
 "📌 Wer bei „Überwachung gegen Kinderpornografie“ kein Alarmlicht habe, habe die Geschichte verschlafen [1:50] [seine Sicht]."]),
("1:50","1:54","d","🔫 Gastgeber: Alles False Flags? Daniela Klette und die Panzerfaust",[
 "**Zusammenfassung:** Der Gastgeber: Je mehr er sich beschäftige, desto mehr scheine fast jede Terrorgruppe mit Geheimdiensten zu tun zu haben – von den Mudschaheddin 1978 bis Al-Qaida; nun sei „der Typ“ Präsident Syriens. Daniela Klette, RAF-Mitglied der dritten Generation, sei im Haus eines Freundes von ihm festgenommen worden; man habe eine Kalaschnikow und eine „Panzerfaustgranate“ gefunden – was wolle eine alte Dame damit? Pohlmann würde in Deutschland zum Prozess gehen; ihm falle die Ähnlichkeit zwischen Militärs („I serve my country“) und Terroristen (Gerechtigkeit) auf. Aufgabe der Älteren: beide dazu bringen, gemeinsam ein Heim für Straßenkinder in Peru zu bauen.",
 "📚 LG Verden, 27.05.2026: 13 Jahre Haft für Raubüberfälle 1999–2016; gefunden wurden u. a. Waffen, Munition und eine „Panzerfaust-Attrappe“; die RAF-Anschläge 1990–1993 sind Gegenstand einer gesonderten Anklage (siehe Abgleich)."]),
("1:54","1:58","d","🧭 Drei RAF-Generationen, Bandung und die Todesnacht von Stammheim",[
 "**Zusammenfassung:** Den Film „Der Baader Meinhof Komplex“ nennt Pohlmann ein „Geschieße“ mit Action-Charakter, die Szenen seien aber richtig. Generation 1 seien Intellektuelle gewesen, die den Staat „demaskieren“ und so den Aufstand auslösen wollten; Vorbild sei die Bandung-Konferenz der blockfreien Staaten gewesen, deren Signet die Bewegung 2. Juni übernommen habe ❓. Generation 2 seien Unterstützer der Gefangenen gewesen, die in der Nacht von Stammheim „unter Umständen, die man guten Gewissens als dubios bezeichnen kann“ umkamen [seine Sicht]; er empfiehlt ein forensisches Buch zur „Todesnacht von Stammheim“ (Versuch mit ausgehöhlter Akte).",
 "📚 Amtlich gilt der Tod von Baader, Ensslin und Raspe am 18.10.1977 als Suizid; ein Antrag auf Wiederaufnahme der Todesermittlungen wurde 2012 abgelehnt (siehe Abgleich). " + HILFE]),
("1:58","2:02","d","🏭 Schleyers SS-Vergangenheit, Waffen aus Tschechien, Herrhausen",[
 "**Zusammenfassung:** Generation 2 sei hart und ausgebildet gewesen (Christian Klar und Gudrun Ensslin nennt er „sehr klug“); die Stasi habe sie „zu verrückt“ gefunden, in Palästinenser-Lagern sei das Sonnenbaden „mit blankem Busen“ schlecht angekommen. Generation 3 seien „Angeschwemmte“ aus der Wohlstandsgesellschaft, ständig überwacht; kein einziger ihrer Morde sei kriminalistisch gelöst. Schleyer sei SS-Mann gewesen, in Prag unter Heydrich in der Wirtschaft tätig; diese Rolle werde bis heute heruntergespielt, und was die RAF im Verhör erfuhr, sei nie veröffentlicht worden. Tschechische Waffen aus deutscher Produktion hätten nach 1945 Israel ausgerüstet. Den Herrhausen-Mord nennt er „hellen Wahnsinn“, er sei „nur im amerikanischen Interesse“ gewesen [seine Sicht].",
 "📚 Schleyer trat 1933 der SS bei (zuletzt Untersturmführer), ab 1943 beim Zentralverband der Industrie für Böhmen und Mähren in Prag, 1973 BDA-Präsident (siehe Abgleich).",
 "❓ Die Aussage, kein Mord der dritten Generation sei gelöst, ist hier nicht im Einzelnen geprüft; der Herrhausen-Mord (1989) gilt als ungeklärt (📚, Quelle nicht geprüft)."]),
("2:02","2:07","h","🎭 Schluss: NPD und V-Leute, Skull and Bones, Ukraine und „wir Plebejer“",[
 "**Zusammenfassung:** Der Gastgeber zieht Bilanz: Alles gehe auf Nationalsozialismus und Zweiten Weltkrieg zurück; Parallelen zwischen RAF und Manson/Hippies; man konzentriere sich auf Schleyers NS-Vergangenheit, aber nicht auf die Verfassungsschutz-Leute beim Dutschke-Anschlag. Die NPD sei bei ihrer Gründung „zu einem Drittel“ in den Vorständen vom Verfassungsschutz oder BND besetzt gewesen; Hegel'sche Dialektik: Extreme würden orchestriert [seine Sicht]. Pohlmann: Bei Skull and Bones stehe „War“ an der Tempelwand ❓ – gemeint sei, zwei Seiten aufeinander zu hetzen, wie heute in der Ukraine-Eskalation; die Zeche zahlten junge Männer. Ausblick auf eine Sendung zu Thule-Gesellschaft, Germanenorden und Operation Paperclip.",
 "💬 „dass wir Plebejer … zusammen besser unterwegs wären“ (Pohlmann) [2:06]",
 "📚 BVerfG 2003: V-Leute machten im NPD-Bundesvorstand „unter fünfzehn Prozent“ aus, in Landesvorständen im Schnitt ein bis zwei; das Verbotsverfahren wurde eingestellt (siehe Abgleich)."]),
]
NA = len(A)

def ts(v,b): return f"[{v}–{b}]"
detail = [
 {"typ":"text","text":f"🔎 Detaillierte Auswertung in der Reihenfolge des Gesprächs – {NA} Abschnitte. Lesehilfe: 💬 Zitat, 📌 Aussage/Zahl/Beispiel, 🔗 Bezug, 📚 Ergänzung, ❓ unklar. Video: [{TITEL}]({URL})"},
 {"typ":"gespraech","titel":"🧭 Gesprächsverlauf – wann worüber gesprochen wird","dauer":"2:07",
  "themen":[{"k":"a","n":"68er, Schah & Ohnesorg"},{"k":"b","n":"Vietnam & Ho Chi Minh"},{"k":"c","n":"Geheimdienste & Unterwanderung"},
            {"k":"d","n":"RAF, Bewegung 2. Juni & Stammheim"},{"k":"e","n":"Italien: Gladio & Moro"},{"k":"f","n":"Hippies, Manson & Okkultes"},
            {"k":"g","n":"LSD, MKUltra & Rituale"},{"k":"h","n":"Verschwörung, Wahrheit & Haltung"},{"k":"w","n":"Einstieg/Organisatorisches"}],
  "teile":[{"von":v,"bis":b,"t":re.sub(r'^\S+\s','',t),"th":th} for v,b,th,t,_ in A]},
] + [{"typ":"abschnitt","titel":f"{t} {ts(v,b)}","th":th,"liste":L} for v,b,th,t,L in A]

# ---------- Überblick ----------
kern = [
 ["1","Geheimdienste unterwandern Protestbewegungen, um sie zu beobachten, zu radikalisieren und zu nutzen – ohne festen Masterplan.","Pläne müssten ständig nachjustiert werden; Beispiele Deutschland, Italien, USA, Syrien","[0:37–0:52]","★★★"],
 ["2","Die Anfänge des westdeutschen Terrorismus lagen im Umfeld von V-Leuten.","Urbach (Waffen, Molotowcocktails), Weingraber-Wohnung, Becker","[0:19], [0:34–0:46]","★★★"],
 ["3","NS-Kontinuität im Apparat erklärt Härte des Staates und Radikalisierung der Studenten.","Prügelperser, Ohnesorg, BKA-Führung mit SS-Vergangenheit","[0:04–0:12], [0:37–0:40]","★★"],
 ["4","Die USA verspielten nach 1945 die Freundschaft Ho Chi Minhs; der Vietnamkrieg war Verrat und Massensterben.","OSS-Ausbildung, Unabhängigkeitserklärung, Rückkehr Frankreichs, 58.000 vs. 3 Mio. Tote","[0:21–0:34]","★★★"],
 ["5","In Italien wurden Rote Brigaden unterwandert; Moros Tod verhinderte den historischen Kompromiss.","Gladio, Angleton, Kissinger-Warnung laut Witwe, Maulwurf, Lage der Leiche","[1:31–1:42]","★★★"],
 ["6","Die Entführungen Moros und Schleyers folgten demselben Muster; Stasi-Akten enthielten Hinweise auf deutsche Kommandos.","eigene Recherche im Stasi-Archiv","[1:40–1:42]","★★"],
 ["7","Die dritte RAF-Generation stand unter Überwachung, Stammheim wurde abgehört; ihre Morde sind ungelöst.","„Warum nehmen die uns nicht hoch?“","[1:42–1:45], [1:58]","★★"],
 ["8","Eine Wahrheitskommission nach südafrikanischem Vorbild soll die RAF-Zeit aufklären.","Straffreiheit gegen Wahrheit; Beispiele Palme, Amish","[1:44–1:50]","★★"],
 ["9","Gastgeber: Hippie-Gegenkultur, Laurel Canyon und Manson-Morde haben eine geheimdienstliche und okkulte Ebene; Pohlmann: Rituale entfalten reale Wirkung, die CIA nutzte LSD.","Lookout Mountain, Tate-Mord, MKUltra, schwarze Messe","[0:55–1:25]","★★★"],
 ["10","Schleyers SS-Rolle wird heruntergespielt; der Herrhausen-Mord lag nur im amerikanischen Interesse.","Prag unter Heydrich; Herrhausen mit Gorbatschow","[1:58–2:02]","★★"],
]
baum = {"typ":"baum","titel":"🌳 Themenbaum des Gesprächs","wurzel":TITEL,"unter":f"{GAST} · {KANAL} · {DATUM} · {DAUER}","knoten":[
 {"t":"🇮🇷 1967: Schah, Ohnesorg, Dutschke [0:02–0:19]","k":[{"t":"👊 Prügelperser und SAVAK [0:05]"},{"t":"🕯️ Ohnesorg erschossen [0:09]"},{"t":"✝️ Dutschke christlich geprägt [0:11]"},{"t":"🥊 Vergleich mit Muhammad Ali [0:13]"},{"t":"🕵️ Kurras als Stasi-Mann [0:18]"}]},
 {"t":"🇻🇳 Vietnam [0:21–0:34]","k":[{"t":"📜 Ho Chi Minh und Washington [0:27]"},{"t":"🤝 OSS bildet Viet Minh aus [0:25]"},{"t":"⚖️ Potsdam und Frankreichs Rückkehr [0:28]"},{"t":"💥 58.000 gegen 3 Mio. Tote [0:32]"}]},
 {"t":"🕵️ V-Leute und Unterwanderung [0:34–0:55]","k":[{"t":"🔥 Peter Urbach und Springer [0:34]"},{"t":"🏛️ BKA und SS-Vergangenheit [0:39]"},{"t":"🏠 Weingrabers Wohnung [0:42]"},{"t":"🪖 Stasi-Ausbildung, Fischer [0:46]"},{"t":"🌿 Grüne und Rote Brigaden [0:50]"}]},
 {"t":"🌼 Hippies, Manson, Okkultes [0:55–1:04]","k":[{"t":"🎸 Laurel Canyon und Stars [0:57]"},{"t":"🎥 Lookout Mountain [0:58]"},{"t":"🔪 Mord an Sharon Tate [1:00]"},{"t":"☮️ Blumenkraft und Peace-Zeichen [1:01]"},{"t":"📚 O'Neill: Chaos [1:03]"}]},
 {"t":"🧪 LSD, MKUltra, Rituale [1:04–1:25]","k":[{"t":"🍄 Hofmann und Eleusis [1:05]"},{"t":"🧪 CIA und ČSSR [1:07–1:09]"},{"t":"🕯️ Schwarze Messe [1:11]"},{"t":"👁️ Remote Viewing [1:13]"},{"t":"🐇 Oz, Alice, Wonderland [1:24]"}]},
 {"t":"🇮🇹 Italien: Gladio und Moro [1:31–1:42]","k":[{"t":"🗳️ Angleton und die Wahl [1:33]"},{"t":"🤝 Compromesso storico [1:34]"},{"t":"☎️ Kissinger-Warnung [1:36]"},{"t":"📺 BBC-Serie Gladio [1:36]"},{"t":"🎯 Muster wie bei Schleyer [1:40]"}]},
 {"t":"⭐ RAF-Generationen [1:42–2:02]","k":[{"t":"👂 Überwacht und nicht gefasst [1:43]"},{"t":"🔫 Klette und die Panzerfaust [1:53]"},{"t":"🧭 Generation 1 bis 3 [1:55–1:58]"},{"t":"🏭 Schleyer und Prag [1:59]"},{"t":"🏦 Herrhausen [2:00]"}]},
 {"t":"🔎 Haltung und Aufklärung [1:25–2:07]","k":[{"t":"🧐 Verschwörungssachverständiger [1:25]"},{"t":"⚖️ Wahrheitskommission [1:45]"},{"t":"🕊️ Palme und Südafrika [1:47]"},{"t":"🗳️ NPD und V-Leute [2:04]"},{"t":"🤝 Wir Plebejer [2:06]"}]},
]}
steck = {"typ":"tabelle","kopf":["🧭 Steckbrief",""],"schmal":True,"zeilen":[
 ["**Thema in einem Satz**","Wie Geheimdienste laut Dirk Pohlmann Protest- und Terrorgruppen von den 68ern über RAF und Rote Brigaden bis zur Hippie-Szene unterwanderten und nutzten – mit einem vom Gastgeber eingebrachten Teil über Manson, MKUltra und Okkultes."],
 ["**Titel**",f"„{TITEL}“ – Kanal {KANAL}, Format „Good Morning Germany“"],
 ["**Format**","Video-Gespräch, frei gesprochen, ohne Kapitel; keine Werbeblöcke im Transkript erkennbar; Teaser aus späteren Stellen am Anfang [0:00–0:01]"],
 ["**Sprecher**","👤 **Dirk Pohlmann** – Gast, Journalist und Dokumentarfilmer, Mitbegründer von {{a:wikihausen|Geschichten aus Wikihausen (A-10)}} · 🎙️ **Gastgeber** von REALTALK MEDIA – Name im Video nicht genannt ❓; spricht längere eigene Passagen (u. a. [0:16–0:19], [0:34–0:37], [0:55–1:04], [1:20–1:25], [1:50–1:54], [2:02–2:05])"],
 ["**Dauer**","2 Std. 7 Min. (2:07:21)"],
 ["**Datum**","Veröffentlichung nicht ermittelt (2026 ❓); aufgenommen vermutlich in der ersten Hälfte 2026: „47 Jahre“ seit der iranischen Revolution, Klette-Festnahme „letztes Jahr“, Prozess offenbar noch laufend (Urteil 27.05.2026) 📚"],
 ["**Grundton**","freundschaftlich, gegenseitig lobend; Pohlmann stimmt den Thesen des Gastgebers „viel ja, etwas nein“ zu und warnt vor Masterplan-Denken und vor dem „Wegtragen-Lassen“ [0:37], [0:48], [1:15]"],
 ["**Hinweis**","Vorwürfe gegen namentlich genannte Personen stehen als Aussage des jeweiligen Sprechers mit Fundstelle; daneben im Abgleich, was Gerichte und amtliche Stellen festgestellt haben. Weiteres Gespräch: {{a:realtalk-pohlmannschmidt|zweites Gespräch mit Dirk Pohlmann}}."],
]}
ueberblick = [
 {"typ":"folge","k":K,"titel":TITEL,"gast":GAST,"rolle":ROLLE,"kanal":KANAL,"datum":DATUM,"dauer":DAUER,"url":URL,
  "thema":"Dirk Pohlmann erzählt bei REALTALK MEDIA, wie Geheimdienste aus seiner Sicht Protest- und Terrorgruppen unterwanderten und nutzten – von Schahbesuch und Ohnesorg über V-Leute in der Berliner Szene, Vietnam, Rote Brigaden und Moro bis zu den drei RAF-Generationen –, während der Gastgeber Hippie-Szene, Manson, MKUltra und Okkultes einbringt.",
  "kacheln":[[str(NA),"Abschnitte"],["10","Kernaussagen"],["ABG","Abgleich-Punkte"],["5","Verläufe & Diagramme"],["QN","Quellen"]]},
 {"typ":"hinweis","text":"Auswertung nach dem Transkript (automatische Untertitel): Gesagtes ohne Zeichen, Ergänzungen 📚, Unklares ❓. Fundstellen [Stunde:Minute] springen ins Video. Die Bewertung bleibt dem Leser."},
 {"typ":"abschnitt","titel":"⚡ In Kürze","liste":[
  "**Wer:** Dirk Pohlmann, Journalist und Dokumentarfilmer, zum zweiten Mal bei „Good Morning Germany“ auf REALTALK MEDIA; Gastgeber im Video nicht namentlich genannt ❓; 2 Std. 7 Min., vermutlich 2026 aufgenommen.",
  "**Ausgangspunkt:** Schahbesuch 1967, „Prügelperser“ und der Tod Benno Ohnesorgs; Kurras wurde 2009 als Stasi-Mitarbeiter bekannt [0:02–0:19].",
  "**Vietnam:** Pohlmann erzählt, wie Ho Chi Minh mit dem OSS gegen Japan kämpfte und sich nach 1945 von den USA verraten sah [0:21–0:34].",
  "**V-Leute:** Peter Urbach, die Wohnung Volker Weingrabers und Verena Becker stehen für seine These, dass der Staat die Szene früh durchdrang und nutzte [0:34–0:46].",
  "**Hippies & Okkultes:** Der Gastgeber bringt Laurel Canyon, Manson, Lookout Mountain und MKUltra ein; Pohlmann spricht über LSD, Eleusis, Rituale und Remote Viewing [0:55–1:25].",
  "**Italien:** Gladio, Rote Brigaden und der Mord an Aldo Moro – laut Pohlmann nach demselben Muster wie die Schleyer-Entführung [1:31–1:42].",
  "**RAF heute:** Drei Generationen, Stammheim, Schleyers SS-Vergangenheit, Klette; Forderung nach einer Wahrheitskommission [1:42–2:02].",
  "**Abgleich:** Mehrere Punkte sind amtlich belegt (Urbach, Becker als bezahlte Quelle, BKA-Studie, NSA zu Tonkin, MKUltra-Anhörung, NPD-Verfahren); andere Zahlen weichen ab oder bleiben offen ❓."]},
 {"typ":"abschnitt","titel":"🔦 Aus Pohlmanns Sicht – der rote Faden","liste":[
  "[seine Sicht] Geheimdienste arbeiten im grauen Feld: Wo eine Bewegung entsteht, wird sie infiltriert – erst um zu wissen, was los ist, dann um sie zu radikalisieren und zu nutzen.",
  "[seine Sicht] Es gibt keinen Masterplan, der aufgeht; Pläne werden ständig nachjustiert, aber wer Terroristen sieht, fragt sofort, wie man sie gebrauchen kann.",
  "[seine Sicht] Im Westdeutschland der 60er trafen eine moralisch motivierte Jugend und ein Apparat mit NS-Vergangenheit aufeinander; der Konflikt war „unausweichlich“.",
  "[seine Sicht] Italien hat diese Geschichte viel besser aufgearbeitet als Deutschland; für die RAF braucht es eine Wahrheitskommission, die Straffreiheit gegen Wahrheit tauscht.",
  "[seine Sicht] Man soll sich auch dunkle Themen nüchtern ansehen – als „Verschwörungssachverständiger“, mit innerem Sherlock Holmes und spiritueller Erdung."]},
 {"typ":"text","text":"🎯 **Kernaussagen** – die zehn wichtigsten Thesen des Gesprächs:"},
 {"typ":"tabelle","kopf":["#","Aussage","Begründung im Gespräch","Fundstelle","Gewicht"],"zeilen":kern},
 baum,
 {"typ":"illu","id":f"{K}_muster","titel":"Skizze: Beobachten – radikalisieren – nutzen (Darstellung laut Pohlmann, schematisch)"},
 {"typ":"illu","id":f"{K}_belege","titel":"Skizze: Was amtlich belegt ist – Freigaben, Urteile und Berichte 1964–2026 (belegte Daten)"},
 steck,
]

# ---------- Zeitachse & Verzeichnisse ----------
Z = [
 ("44 v. Chr.",-44,"Ermordung Caesars – Beispiel einer „klassischen Verschwörung“","[1:28]",True),
 ("1776",1776,"US-Unabhängigkeitserklärung – Vorbild für Ho Chi Minh","[0:27]",True),
 ("1789",1789,"Erklärung der Menschen- und Bürgerrechte – Teile in Vietnams Unabhängigkeitserklärung","[0:27]",False),
 ("1933",1933,"Hanns Martin Schleyer tritt der SS bei","[1:58]",True),
 ("1940",1940,"Josef Ochs (später BKA) wirkt in Köln an der Deportation von Sinti mit","[0:39]",True),
 ("1943–1945",1943,"Schleyer beim Zentralverband der Industrie für Böhmen und Mähren in Prag","[1:59]",True),
 ("1945",1945,"OSS-Offiziere bilden die Viet Minh aus; Ho Chi Minh verliest die Unabhängigkeitserklärung","[0:25–0:28]",True),
 ("1945",1945,"Potsdamer Konferenz; Frankreich kehrt nach Indochina zurück","[0:28]",True),
 ("1948",1948,"Erste Wahl in Italien nach dem Krieg – laut Pohlmann von der CIA beeinflusst","[1:33]",True),
 ("1953–1964",1953,"CIA-Programm MKUltra (so Admiral Turner 1977)","[0:59], [1:22]",True),
 ("1956",1956,"Suez-Krieg – Absprache Großbritanniens, Frankreichs und Israels","[1:28]",True),
 ("1959",1959,"BKA-Führung: etwa drei Viertel frühere NSDAP-, zwei Drittel frühere SS-Mitglieder","[0:39]",True),
 ("1964",1964,"Golf von Tonkin: Angriff am 2.8. auf die USS Maddox; den gemeldeten Angriff am 4.8. gab es nicht","[1:03]",True),
 ("1965–1968",1965,"Höchste US-Verluste in Vietnam (1968: 16.899 Gefallene)","[0:32]",True),
 ("1967",1967,"Schahbesuch in West-Berlin; „Prügelperser“; Pohlmann ist acht Jahre alt","[0:04–0:06]",False),
 ("1967",1967,"2. Juni: Benno Ohnesorg wird von Karl-Heinz Kurras erschossen","[0:09], [0:17]",False),
 ("1967",1967,"27.11.: Kurras wird freigesprochen","[1:31]",True),
 ("1968",1968,"Attentat auf Rudi Dutschke; Ausschreitungen vor dem Springer-Haus","[0:33–0:36]",False),
 ("1969",1969,"Mord an Sharon Tate und weiteren durch die Manson Family","[1:00]",True),
 ("1969",1969,"9.11.: Bombe im Jüdischen Gemeindehaus Berlin – von V-Mann Urbach geliefert (bekannt seit 2005)","[0:34]",True),
 ("1971",1971,"Urbach wird nach einer Aussage vor Gericht enttarnt und erhält eine neue Identität","[0:33]",True),
 ("1973",1973,"Januar: MKUltra-Akten werden auf Anweisung vernichtet","[1:22]",True),
 ("1973",1973,"Schleyer wird Präsident der Arbeitgeberverbände (BDA)","[1:59]",True),
 ("1977",1977,"3.8.: Senatsanhörung zu MKUltra (149 Unterprojekte, 80 Einrichtungen)","[0:59]",True),
 ("1977",1977,"5.9.: Entführung Schleyers in Köln, vier Begleiter getötet; 18.10.: Schleyer ermordet","[1:40], [1:58]",True),
 ("1977",1977,"18.10.: Tod von Baader, Ensslin und Raspe in Stammheim","[1:55]",True),
 ("1978",1978,"Entführung und Ermordung Aldo Moros durch die Roten Brigaden","[1:36–1:40]",True),
 ("1978–1979",1978,"Pohlmann bei der Bundeswehr (Marineflieger); Revolution im Iran","[0:07]",False),
 ("1980er",1981,"Verena Becker liefert in der Haft Informationen an den Verfassungsschutz","[0:43]",True),
 ("um 1989 ❓",1989,"Pohlmann recherchiert wochenlang im Stasi-Archiv (Jahr im Transkript unklar)","[1:42]",False),
 ("1989",1989,"Mord an Alfred Herrhausen","[1:45], [2:00]",True),
 ("1990",1990,"22.11.: Entschließung des Europäischen Parlaments zu Gladio","[1:33]",True),
 ("1992",1992,"BBC2/Timewatch zeigt Allan Francovichs dreiteilige Serie „Gladio“","[1:36]",True),
 ("1997",1997,"17.04.: Francovich stirbt im Zollbereich des Flughafens Houston (Herzinfarkt)","[1:37]",True),
 ("2003",2003,"18.03.: BVerfG stellt NPD-Verbotsverfahren wegen V-Leuten in Vorständen ein","[2:04]",True),
 ("2005",2005,"NSA gibt Dokumente zum Golf von Tonkin frei","[1:03]",True),
 ("2009",2009,"Kurras als Stasi-Mitarbeiter und SED-Mitglied bekannt","[0:18]",False),
 ("2011",2011,"Ermittlungen zu einem möglichen Stasi-Auftrag im Fall Ohnesorg eingestellt; Urbach stirbt","[0:18]",True),
 ("2012",2012,"06.07.: OLG Stuttgart verurteilt Verena Becker wegen Beihilfe zum Buback-Mord","[0:43]",True),
 ("2012",2012,"Antrag auf Wiederaufnahme der Stammheim-Todesermittlungen abgelehnt","[1:55]",True),
 ("2013",2013,"Bundesregierung zu Gladio (BT-Drs. 17/14815): Einzelheiten als „Geheim“ eingestuft","[0:04]",True),
 ("2024",2024,"Daniela Klette in Berlin festgenommen","[1:52]",False),
 ("2026",2026,"27.05.: LG Verden verurteilt Klette zu 13 Jahren Haft (Raubüberfälle)","[1:53]",True),
 ("2026 ❓",2026,"Aufnahme des Gesprächs (vermutlich erste Jahreshälfte)","[0:04]",True),
]
Z.sort(key=lambda r:r[1])
zeit = [
 {"typ":"zeitachse","titel":"📅 Zeitachse – Ereignisse, die im Gespräch vorkommen","eintraege":[{"z":z,"j":j,"t":t,"f":f,"e":e} for z,j,t,f,e in Z]},
 {"typ":"tabelle","kopf":["👤 Person","Wer / was","Rolle im Gespräch","Fundstelle"],"zeilen":[
  ["Dirk Pohlmann","Journalist, Dokumentarfilmer; 1967 acht Jahre alt; Ende der 70er bei der Marine","Gast","durchgehend"],
  ["Gastgeber (REALTALK MEDIA)","Name im Video nicht genannt ❓; schreibt an einem Buch „Die Destabilisierung von Deutschland“","Fragen, längere eigene Thesen","durchgehend"],
  ["Rudi Dutschke","Wortführer der Studentenbewegung, aus der DDR, christlich geprägt","Leitfigur, bewundert","[0:11–0:16]"],
  ["Gretchen Dutschke","seine Frau, aus den USA","Einfluss der Bürgerrechtsbewegung","[0:11]"],
  ["Benno Ohnesorg","Student, 2.6.1967 erschossen","Auslöser der Radikalisierung","[0:09], [0:17]"],
  ["Karl-Heinz Kurras","West-Berliner Polizist, Stasi-Mitarbeiter (2009 bekannt)","Todesschütze","[0:18], [1:31]"],
  ["Katja Ebstein","Sängerin (Transkript: „Epstein“)","bei der Demonstration 1967 dabei","[0:09]"],
  ["Muhammad Ali","Boxer, Wehrdienstverweigerer","Vergleich mit Dutschke","[0:13–0:15]"],
  ["Peter Urbach","V-Mann des Berliner Verfassungsschutzes","Waffen und Molotowcocktails","[0:19], [0:33–0:36]"],
  ["Paul Dickopf","BKA, Vizepräsident ab 1953, Präsident 1965–1971","Beispiel NS-Kontinuität","[0:39]"],
  ["Michael „Bommi“ Baumann","Bewegung 2. Juni, Autor von „Wie alles anfing“","Pohlmanns Gesprächspartner","[0:40–0:45]"],
  ["Georg von Rauch","Haschrebellen, von Polizei erschossen","Baumanns Freund","[0:41]"],
  ["Volker Weingraber Edler von Grodeck","laut Pohlmann V-Mann, später BND (❓ nicht geprüft)","Wohnung als Treffpunkt der Szene","[0:42–0:45]"],
  ["Verena Becker","Bewegung 2. Juni/RAF; 2012 verurteilt (Beihilfe Buback-Mord)","laut Pohlmann Verfassungsschutz-Agentin","[0:43]"],
  ["Inge Viett · Otto Schily","in Weingrabers Wohnung genannt (Schily ❓)","Anwesende","[0:42]"],
  ["Benjamin Fischer","früherer CIA-Historiker","Aufsatz zur RAF-Ausbildung in der DDR ❓","[0:46]"],
  ["Ho Chi Minh · Võ Nguyên Giáp","vietnamesische Revolutionsführer","Vietnam-Exkurs","[0:21–0:31]"],
  ["Petra Kelly · Antje Vollmer · Joseph Beuys · Jutta Ditfurth","Grüne der Anfangszeit","Beispiele für Unterwanderung [seine Sicht]","[0:50–0:51]"],
  ["Charles Manson","Anführer der „Manson Family“","Mord an Sharon Tate; MKUltra-Bezug ❓","[0:16], [1:00], [1:04]"],
  ["Roman Polanski · Sharon Tate","Regisseur; seine 1969 ermordete Frau","Hollywood-Bezug","[0:57–1:03]"],
  ["Wojciech Frykowski","Freund Polanskis, 1969 ermordet","Zahlenspiel des Gastgebers ❓","[1:02–1:03]"],
  ["Anton LaVey · Aleister Crowley · Jimmy Page","Church of Satan; Okkultist; Gitarrist","okkulte Ebene laut Gastgeber","[0:57]"],
  ["Albert Hofmann · Timothy Leary","LSD-Entdecker; LSD-Propagandist","LSD-Exkurs","[1:04–1:07]"],
  ["Tom O'Neill · David McGowan","Autoren von „Chaos“ und „Weird Scenes Inside the Canyon“","Buchtipps des Gastgebers","[1:03]"],
  ["Jim Morrison","Sänger der Doors; Vater Admiral","Golf-von-Tonkin-Bezug","[1:03]"],
  ["Xavier Naidoo","Sänger","„Kompass 10 Grad daneben“","[1:10], [1:27]"],
  ["Aldo Moro","italienischer Christdemokrat, 1978 ermordet","Italien-Exkurs","[1:31–1:41]"],
  ["Henry Kissinger","US-Außenpolitiker","Warnung an Moro laut Witwe ❓","[1:36]"],
  ["James Jesus Angleton","CIA-Spionageabwehrchef","Italien-Wahl","[1:33]"],
  ["Alberto Franceschini","Mitgründer der Roten Brigaden","Zeuge in der BBC-Serie","[1:37]"],
  ["Allan Francovich","Regisseur der BBC-Serie „Gladio“","Tod 1997","[1:36–1:37]"],
  ["Hanns Martin Schleyer","Arbeitgeberpräsident, früher SS","1977 entführt und ermordet","[1:39–2:01]"],
  ["Reinhard Heydrich","SS-Führer, Stellvertretender Reichsprotektor","Schleyers Umfeld in Prag","[1:59]"],
  ["Alfred Herrhausen","Chef der Deutschen Bank, 1989 ermordet","Pohlmanns Buchprojekt","[1:45], [2:00]"],
  ["Christian Klar · Gudrun Ensslin","RAF-Mitglieder","„sehr klug“ (Pohlmann)","[1:57]"],
  ["Daniela Klette","RAF, 3. Generation; 2026 verurteilt (Raubüberfälle)","Festnahme im Haus eines Freundes des Gastgebers","[1:52–1:54]"],
  ["Olof Palme","schwedischer Ministerpräsident, 1986 ermordet","Beispiel Wahrheitskommission","[1:47]"],
 ]},
 {"typ":"tabelle","kopf":["🗺️ Ort","Rolle","Fundstelle"],"zeilen":[
  ["West-Berlin","Schahbesuch, Ohnesorg, Kommune 1, Springer-Haus, Weingrabers Wohnung","[0:04–0:45]"],
  ["Hanoi","Völkerkundemuseum","[0:22]"],["Paris","Ho Chi Minhs Lehrjahre","[0:23]"],["Potsdam","Konferenz 1945","[0:28]"],
  ["Spreewald","Ausbildung der RAF durch die Stasi laut Fischer ❓","[0:46]"],
  ["Los Angeles · Laurel Canyon · Lookout Mountain","Hippie-Szene, Filmstudio der Luftwaffe","[0:57–0:59]"],
  ["Wonderland Avenue","Ort der Morde von 1981 laut Gastgeber ❓","[1:24]"],
  ["Eleusis","antike Mysterien","[1:05]"],["Tschechoslowakei · Łódź","LSD-Produktion, Filmakademie","[1:08–1:09]"],
  ["Pfalz","schwarze Messe des Kommilitonen","[1:11]"],
  ["Italien · Rom","Gladio, Moro","[1:31–1:41]"],["Houston","Tod Francovichs","[1:36]"],
  ["Stammheim","Gefängnis der ersten RAF-Generation","[1:44], [1:55]"],
  ["Prag","Schleyers Tätigkeit unter Heydrich","[1:59]"],["Südafrika · Schweden","Wahrheitskommission, Palme","[1:45–1:47]"],
  ["Iran · Syrien · Ukraine","Gegenwartsbezüge","[0:04], [0:49], [2:05]"],
 ]},
 {"typ":"tabelle","kopf":["📖 Begriff","Erklärung","Fundstelle"],"zeilen":[
  ["SAVAK","Geheimdienst des Schahs","[0:06]"],["„Prügelperser“","Schah-Anhänger, die 1967 Demonstranten schlugen","[0:05]"],
  ["Bewegung 2. Juni","nach Ohnesorgs Todestag benannte Gruppe","[0:08]"],["RAF","Rote Armee Fraktion, drei Generationen","[0:36], [1:55–1:58]"],
  ["Kommune 1","Berliner Wohnkommune, „Spaßguerilla“ (Pudding-Attentat)","[0:19], [0:33]"],
  ["Haschrebellen","„Zentralrat der umherschweifenden Haschrebellen“","[0:41]"],
  ["V-Mann","Vertrauensperson eines Nachrichtendienstes in einer beobachteten Gruppe","[0:19], [0:33]"],
  ["OSS","US-Kriegsgeheimdienst, Vorläufer der CIA","[0:25], [0:34]"],["Viet Minh","vietnamesische Unabhängigkeitsbewegung","[0:25]"],
  ["Domino-Theorie","Annahme, ein kommunistisches Land ziehe die Nachbarn nach","[0:21]"],
  ["Gladio / Stay-behind","geheime NATO-Netze für den Besatzungsfall","[0:04], [1:33]"],
  ["Compromesso storico","geplante Zusammenarbeit von DC und PCI","[1:34]"],["Rote Brigaden","italienische Untergrundgruppe","[0:50], [1:36]"],
  ["SISMI","italienischer Militärgeheimdienst","[0:50]"],["COINTELPRO · Operation CHAOS","FBI- und CIA-Programme gegen Protestbewegungen","[1:31]"],
  ["MKUltra","CIA-Forschung zu Bewusstseinsbeeinflussung 1953–1964","[0:59], [1:22]"],
  ["Remote Viewing","„Fernwahrnehmung“, von US-Diensten erforscht","[1:13]"],
  ["Church of Satan","1966 von Anton LaVey gegründet","[0:57]"],["Project Blue Beam","Theorie einer inszenierten Himmelserscheinung","[1:19]"],
  ["Buch Henoch","Schrift der äthiopischen Bibel","[1:18]"],["Wahrheitskommission","Aufklärung gegen Straffreiheit (Südafrika)","[1:45]"],
  ["„Epstein-Klasse“","Pohlmanns Wort für eine einflussreiche, reiche Oberschicht","[0:49], [1:10]"],
 ]},
 {"typ":"tabelle","kopf":["📊 Zahl im Gespräch","Angabe","Fundstelle"],"zeilen":[
  ["Pohlmanns Alter 1967","8 Jahre","[0:04]"],["Iran-Herrschaft","„47 Jahre“","[0:04]"],
  ["BKA-Führung mit SS-Vergangenheit","„drei Viertel“","[0:39]"],["Volksgruppen in Vietnam","60","[0:22]"],
  ["Vietnam: Einwohner / Hungertote","25 Mio. / 4 Mio.","[0:22]"],["Revolutionäre um Ho","sieben","[0:24]"],
  ["OSS-Offiziere","drei","[0:25]"],["US-Tote Vietnam","58.000","[0:32]"],["Vietnamesische Tote","3 Mio.","[0:33]"],
  ["Weingut-Abfindung","über 1 Mio. DM","[0:45]"],["Follower einer Initiative","200.000","[0:52]"],
  ["Lookout Mountain","„10.000 Filme“","[0:58]"],["Erhaltene MKUltra-Akten","„10 %“","[1:22]"],
  ["Remote Viewing","„nach 23 Jahren beendet“","[1:13]"],["Haaretz-Bericht","„vor 14 Jahren“ Doku","[1:29]"],
  ["Klette versteckt","15 Jahre","[1:52]"],["NPD-Vorstände","„zu einem Drittel“ V-Leute","[2:04]"],
 ]},
]

# ---------- Abgleich ----------
abg = [
 ["Ohnesorg sei „hingerichtet“ worden; der Täter Kurras sei freigesprochen worden und ein Stasi-Spitzel gewesen [0:09], [0:18], [1:31]",
  "Kurras wurde am 27.11.1967 freigesprochen. 2009 zeigten Stasi-Akten, dass er inoffizieller Mitarbeiter und SED-Mitglied war; ein Stasi-Auftrag für den Schuss fand sich nicht, die Ermittlungen wurden 2011 eingestellt (Unterlagen der HVA waren 1989/90 offenbar vernichtet). 2012 berichtete der Spiegel nach Recherchen mit der Bundesanwaltschaft, der Schuss sei geplant und nicht in Notwehr gefallen und es habe Vertuschung gegeben.",Q['ohne']],
 ["Die ersten Sprengstoffe und Schusswaffen seien über Verfassungsschutz-Agenten in die Gruppen gekommen [0:19]; Urbach habe vor dem Springer-Haus Molotowcocktails gebracht [0:35]",
  "Peter Urbach war V-Mann des Berliner Verfassungsschutzes, hatte Kontakt zur Kommune 1 und versorgte die Szene mit Waffen, Molotowcocktails und Bomben. 2005 wurde bekannt, dass er die Bombe für den Anschlagsversuch auf das Jüdische Gemeindehaus am 9.11.1969 lieferte, die nicht explodierte. Zur Springer-Blockade im April 1968 nennt die Quelle keine Einzelheiten ❓.",Q['urbach']],
 ["Urbach sei „überführt“ worden, einer der prominentesten Geheimdienstler [0:33]",
  "Urbach wurde 1971 nach einer Zeugenaussage in einem Terrorprozess enttarnt, erhielt eine neue Identität, lebte später in Kalifornien und starb am 3.5.2011.",Q['urbach']],
 ["Verena Becker sei Verfassungsschutz-Agentin gewesen, „wir wissen nicht genau ab wann“ [0:43]",
  "Laut OLG Stuttgart gab Becker Anfang der 1980er in der Haft Informationen an den Verfassungsschutz und erhielt dafür Geld und Vergünstigungen; weitergehende Vorwürfe sah das Gericht nicht belegt. Am 6.7.2012 wurde sie wegen Beihilfe zum Mord an Generalbundesanwalt Buback (1977) zu vier Jahren verurteilt (zweieinhalb galten als verbüßt). Die unmittelbaren Täter und den Schützen konnte das Gericht nicht feststellen; für die These, Becker sei von höherer Stelle geschützt worden, ergab der Prozess laut Vorsitzendem keine Belege.",Q['becker']],
 ["BKA: erster Chef Dickopf mit SS-Dienstgrad, „drei Viertel“ der Führung ehemalige SS-Leute [0:39]",
  "Laut Studie (Baumann/Stephan/Wagner 2012) waren Ende der 1950er etwa drei Viertel der BKA-Führung (Präsident und 33 Leitende) vor 1945 der NSDAP beigetreten, zwei Drittel hatten der SS angehört; 1969 mindestens 40 % frühere Parteigenossen, ein Viertel frühere SS-Mitglieder; 1980 hatten nur 3 von 112 Leitenden vor 1945 Polizeidienst getan. Dickopf war ab 1953 Vizepräsident, 1965–1971 Präsident.",Q['bka']],
 ["Ein für die Verfolgung der Sinti und Roma Zuständiger habe im BKA ein Referat geleitet [0:39]",
  "Die Studie nennt Josef Ochs: SS seit 1938, 1940 an der Deportation westdeutscher Sinti aus Köln beteiligt, vertrat später die kriminalpolitischen Interessen des BKA „im Umgang mit Sinti und Roma“. Das Fahndungsmerkmal „ZN“ wurde erst 1983 abgeschafft.",Q['bka']],
 ["58.000 Amerikaner seien in Vietnam gestorben [0:32]",
  "Die National Archives zählen 58.220 US-Gefallene; die meisten 1968 (16.899). Nach Teilstreitkräften: Army 38.224, Marine Corps 14.844, Air Force 2.586, Navy 2.559, Coast Guard 7.",Q['nara']],
 ["Gastgeber: Fake-Angriff im Golf von Tonkin als Kriegsanlass [1:03]",
  "Die NSA gab am 1.12.2005 Dokumente frei: Laut NSA-Historiker Hanyok gab es den gemeldeten Angriff vom 4.8.1964 nicht, die Aufklärung wurde „verzerrt“ weitergegeben; den Angriff nordvietnamesischer Boote auf die USS Maddox am 2.8.1964 gab es. Einen Beleg für gezielte Vertuschung fand er nicht. Zur Rolle von Admiral Morrison sagt die Quelle nichts ❓.",Q['tonkin']],
 ["MKUltra: fast alle Akten vernichtet, „10 %“ übrig [1:22]",
  "Laut Senatsanhörung vom 3.8.1977 wurden die Akten im Januar 1973 auf Anweisung bzw. mit Genehmigung des damaligen CIA-Direktors vernichtet; 1977 fanden sich sieben Kisten (rund 8.000 Seiten, vor allem Finanzunterlagen). Eine Quote von 10 % wird nicht genannt ❓.",Q['mk']],
 ["MKUltra sei „hochoffiziell“ zugegeben worden, auch Experimente mit Kindern [0:59]",
  "Admiral Turner bestätigte 1977 das Programm (1953–1964) mit 149 Unterprojekten, 185 nichtstaatlichen Forschern und 80 Einrichtungen, darunter 44 Hochschulen, 12 Kliniken und 3 Gefängnisse. Experimente an Kindern sind in den geprüften Teilen der Anhörung nicht genannt ❓.",Q['mk']],
 ["Lookout Mountain: geheime Basis, „10.000 Filme“, dort die meisten Hollywood-Filme gedreht [0:58]",
  "Laut US-Energieministerium drehte das Lookout Mountain Laboratory in 22 Jahren über 6.500 Filme für die Atomenergiekommission und andere Behörden, vor allem zu Atomtests; viele sind bis heute geheim. Personal kam aus Studios wie MGM, Warner Bros. und RKO. Kommerzielle Hollywood-Produktionen nennt die Quelle nicht.",Q['lookout']],
 ["Gladio als Netz gegen den Kommunismus, besonders stark in Italien und der Türkei [1:33–1:35]",
  "Das Europäische Parlament verlangte am 22.11.1990 eine vollständige Untersuchung, gerichtliche und parlamentarische Aufklärung und die Auflösung aller geheimen militärischen und paramilitärischen Netze; es protestierte gegen US-Militärs bei SHAPE und NATO, die solche Netze gefördert hätten.",Q['ep']],
 ["Gastgeber: Gladio als Teil der Geheimarmeen in Europa – auch in Deutschland [0:04]",
  "Die Bundesregierung nannte 2013 zwei Lager mit Ausrüstung im früheren britischen Sektor Berlins, sechs Übungen oder Operationen laut alten BND-Akten; Einzelheiten seien als „Geheim“ eingestuft. Belege für eine Beteiligung am Oktoberfest-Attentat 1980 fanden sich laut Regierung in den Akten nicht, die Prüfung des Generalbundesanwalts lief damals noch.",Q['btgladio']],
 ["Der Regisseur der BBC-Serie „Gladio“ sei am Zoll tot zusammengebrochen; ein CIA-Mann habe von „Binärgift“ gesprochen [1:36–1:37]",
  "Allan Francovich starb am 17.04.1997 mit 56 Jahren im Zollbereich des Flughafens Houston bei der Einreise aus England; angegeben wird ein Herzinfarkt. Die Serie lief 1992 in drei Teilen bei BBC2 (Timewatch); seine Lockerbie-Doku „The Maltese Double Cross“ erschien 1994. Für die Gift-Behauptung gibt es keine geprüfte Quelle ❓.",Q['franco']],
 ["Schleyer: SS-Mann, Wirtschaftsführer in Prag unter Heydrich; die NS-Rolle werde heruntergespielt [1:58–2:00]",
  "Schleyer trat 1933 der SS bei (zuletzt Untersturmführer), war ab 1943 beim Zentralverband der Industrie für Böhmen und Mähren in Prag, bis 1945 Leiter des Präsidialbüros; 1973 BDA-Präsident, 1977 zusätzlich BDI-Präsident. Am 5.9.1977 in Köln entführt (sein Fahrer und drei Polizeibeamte erschossen), am 18.10.1977 ermordet, im Elsass (Mulhouse) aufgefunden.",Q['schleyer']],
 ["Die Toten von Stammheim seien unter „dubiosen“ Umständen umgekommen [1:55]",
  "Amtlich wurde der Tod von Baader, Ensslin und Raspe am 18.10.1977 als Suizid eingestuft; Irmgard Möller überlebte. Ein Antrag auf Wiederaufnahme der Todesermittlungen wurde 2012 abgelehnt; Michael Buback fordert seit Jahren die Freigabe aller RAF-Akten. " + HILFE,Q['stamm']],
 ["Gastgeber: Die NPD sei bei der Gründung „zu einem Drittel“ in den Vorständen mit Verfassungsschutz/BND besetzt gewesen [2:04]",
  "Das BVerfG stellte das Verbotsverfahren am 18.3.2003 ein: V-Leute machten im Bundesvorstand zu drei Stichtagen „unter fünfzehn Prozent“ aus, in Landesvorständen im Schnitt ein bis zwei. Drei Richter sahen darin ein nicht behebbares Verfahrenshindernis, vier nicht; die nötige Zweidrittelmehrheit für die Fortsetzung kam nicht zustande. Zur Gründungszeit 1964 sagt die Entscheidung nichts.",Q['npd']],
 ["Gastgeber: Bei Klette seien eine Kalaschnikow und eine „Panzerfaustgranate“ gefunden worden [1:53]",
  "Laut LTO fanden sich in der Berliner Wohnung Waffen, Munition, eine „Panzerfaust-Attrappe“, falsche Papiere und rund 240.000 € Bargeld. Das LG Verden verurteilte Klette am 27.05.2026 zu 13 Jahren Haft für Raubüberfälle (1999–2016); die Beteiligung an drei RAF-Anschlägen 1990–1993 ist eine gesonderte Anklage (OLG Frankfurt).",Q['klette']],
 ["Pohlmann: Von der dritten Generation sei kein Mord kriminalistisch gelöst [1:58]",
  "Die Bundesanwaltschaft hat Klette wegen Beteiligung an drei RAF-Anschlägen 1990–1993 angeklagt; über die Zulassung entscheidet das OLG Frankfurt. Eine Gesamtübersicht über aufgeklärte und ungeklärte Taten der dritten Generation lag hier nicht geprüft vor ❓.",Q['klette']],
]
NABG = len(abg)

kurs_tote = {"typ":"kurs","id":f"{K}-vietnam","titel":"📈 US-Gefallene im Vietnamkrieg je Jahr",
 "reihen":[{"name":"US-Gefallene (Todes- bzw. Ereignisjahr)","kurz":"Tote","einheit":"Tote","dez":0,"hoeherGut":False,
  "punkte":[[1960,5],[1961,16],[1962,53],[1963,122],[1964,216],[1965,1928],[1966,6350],[1967,11363],[1968,16899],[1969,11780],[1970,6173],[1971,2414],[1972,759],[1973,68],[1974,1],[1975,62]]}],
 "hoeherGut":False,"vergleich":False,
 "quelle":Q['nara']+", Stand des Abrufs 12.11.2026 (Datensatzzählung, laut NARA keine amtliche Statistik)",
 "hinweis":"Bezug zum Gespräch [0:32]: „58.000 Amerikaner sind gestorben“. Summe aller Jahre laut NARA 58.220 (auch 1956–1959: 4; nach 1975 einzelne Nachträge)."}
balken_waffe = {"typ":"balken","titel":"📊 US-Gefallene in Vietnam nach Teilstreitkraft","einheit":"Tote","dez":0,
 "zeilen":[["Army",38224],["Marine Corps",14844],["Air Force",2586],["Navy",2559],["Coast Guard",7]],
 "quelle":Q['nara']+", Stand des Abrufs 12.11.2026",
 "hinweis":"Bezug zum Gespräch [0:32]: Pohlmann über die US-Verluste und das Denkmal mit allen Namen."}
balken_mk = {"typ":"balken","titel":"📊 MKUltra: beteiligte Einrichtungen laut CIA-Direktor Turner (1977)","einheit":"Einrichtungen","dez":0,
 "zeilen":[["Hochschulen und Universitäten",44],["Forschungsstiftungen, Chemie- und Pharmafirmen",15],["Krankenhäuser und Kliniken",12],["Gefängnisse",3]],
 "quelle":Q['mk']+", Anhörung vom 03.08.1977",
 "hinweis":"Bezug zum Gespräch [0:59], [1:22]: MKUltra sei „hochoffiziell zugegeben“ worden. Turner nannte 80 Einrichtungen; die Teilgruppen ergeben 74, die Differenz erklärt die Anhörung nicht. Dazu 149 Unterprojekte und 185 nichtstaatliche Forscher."}
balken_bka = {"typ":"balken","titel":"📊 BKA-Führung mit NS-Vergangenheit (Anteile, gerundet)","einheit":"%","dez":0,
 "zeilen":[["1959: frühere NSDAP-Mitglieder (etwa)",75],["1959: frühere SS-Mitglieder (etwa)",67],["1969: frühere NSDAP-Mitglieder (mindestens)",40],["1969: frühere SS-Mitglieder (etwa)",25]],
 "quelle":Q['bka']+" (Studie im Auftrag des BKA)",
 "hinweis":"Bezug zum Gespräch [0:39]: „drei Viertel sind ehemalige SS-Leute“. Die Studie nennt Anteile in Worten („etwa drei Viertel“, „zwei Drittel“, „mindestens 40 Prozent“, „ein Viertel“); die Prozentwerte sind daraus umgerechnet. 1959: Präsident plus 33 Leitende."}
vergl = {"typ":"vergleich","titel":"⚖️ Zahlen im Gespräch und Daten nebeneinander","la":"Im Gespräch genannt","lb":"Daten laut Quelle","zeilen":[
 {"n":"Frühere SS-Mitglieder in der BKA-Führung (Ende 1950er)","a":75,"b":67,"einheit":"%","f":"[0:39]","q":Q['bka']},
 {"n":"US-Gefallene im Vietnamkrieg","a":58000,"b":58220,"einheit":"Tote","f":"[0:32]","q":Q['nara']},
 {"n":"Filme des Lookout Mountain Laboratory","a":10000,"b":6500,"einheit":"Filme (Quelle: „mehr als“)","f":"[0:58]","q":Q['lookout']},
 {"n":"V-Leute im NPD-Bundesvorstand (Gast: Gründungszeit; Quelle: 1990er/2000er-Stichtage)","a":33,"b":15,"einheit":"% (Quelle: „unter“)","f":"[2:04]","q":Q['npd']},
]}

abgleich = [
 {"typ":"text","text":"Neutraler Abgleich: links die Aussage im Gespräch, rechts die gängige Darstellung bzw. Daten mit Quelle. Die Bewertung bleibt dem Leser."},
 {"typ":"tabelle","kopf":["Aussage im Gespräch","Gängige Darstellung (Mainstream) / Daten 📚","Quelle"],"stapel":True,"zeilen":abg},
 kurs_tote, balken_waffe, balken_mk, balken_bka, vergl,
 {"typ":"abschnitt","titel":"🧩 Spannungen im Gespräch","liste":[
  "Pohlmann bremst die Masterplan-These des Gastgebers: „viel ja, etwas nein“ – Unterwanderung und Nutzung ja, ein von Anfang an durchgeplanter Ablauf nein [0:37], [0:48].",
  "Den okkulten Teil bringt fast vollständig der Gastgeber ein (Laurel Canyon, Illuminaten-Slogan, Peace-Zeichen, Zahlenspiel, Wonderland Avenue); Pohlmann kennt zwei der Bezüge nicht („Ewige Blumenkraft“, „Four on the Floor“) [1:01], [1:24].",
  "Pohlmann mahnt den Gastgeber, sich „nicht wegtragen“ zu lassen und nüchtern zu bleiben, lobt zugleich dessen „Spürnase“ [1:15], [1:25–1:30].",
  "Der Gastgeber nennt manches „bewiesen“ (Waffenlieferungen, Anstiftung, lückenlose Überwachung) [0:55]; belegt sind Einzelfälle wie Urbach und Becker, nicht eine durchgehende Steuerung.",
  "Beim Tod Dutschkes ist sich der Gastgeber selbst unsicher („weiß ich nicht genau“) [0:18].",
  "Pohlmann gibt die Gift-Behauptung zu Francovich wieder, nennt sie aber selbst „nicht nachweisbar“ [1:36]."]},
 {"typ":"abschnitt","titel":"💡 Was man mitnehmen kann","liste":[
  "Mehrere Kernpunkte sind amtlich oder gerichtlich belegt: Urbach als V-Mann mit Waffen und Bomben, Becker als bezahlte Quelle des Verfassungsschutzes, die NS-Belastung der frühen BKA-Führung, der nicht stattgefundene Tonkin-Angriff vom 4.8.1964, das MKUltra-Programm, V-Leute in NPD-Vorständen.",
  "Einige Zahlen weichen ab: 6.500 statt 10.000 Lookout-Filme, unter 15 % statt „ein Drittel“ V-Leute im NPD-Bundesvorstand, eine Panzerfaust-Attrappe statt einer Granate.",
  "Gerichte haben in mehreren Fällen ausdrücklich festgehalten, was sie nicht feststellen konnten (Buback-Schütze, Stasi-Auftrag bei Kurras) – das trennt Belegtes von Vermutetem.",
  "Für Gladio, MKUltra und Stammheim gilt: Teile der Akten sind vernichtet oder eingestuft; offene Fragen sind damit nicht beantwortet, aber auch nicht im Sinne einer These entschieden."]},
 {"typ":"abschnitt","titel":"❓ Offen","liste":[
  "Wer ist der Gastgeber, und wann wurde das Video veröffentlicht?",
  "Rolle Volker Weingrabers (V-Mann, BND, Abfindung) – keine geprüfte Quelle gefunden.",
  "Benjamin Fischers Aufsatz zur Ausbildung der zweiten RAF-Generation in der DDR [0:46].",
  "Aussage von Eleonora Moro zu Kissinger [1:36]; Ablauf der Verhaftung der Rote-Brigaden-Führung [1:38].",
  "Pohlmanns Zahlen zu Vietnam (4 Mio. Hungertote, 3 Mio. Tote, Bombenmenge) [0:22], [0:32].",
  "Behauptungen des Gastgebers zu Polanski, Frykowski, Crowley, Peace-Zeichen, Lewis Carroll und den Wonderland-Morden [0:57–1:24] – hier nicht geprüft.",
  "Stasi-Akten mit Hinweisen auf „deutsche Kommandos“ beim Moro-Überfall [1:41–1:42] – Fundstelle im Archiv nicht genannt.",
  "Remote Viewing „nach 23 Jahren beendet“ [1:13]; Haaretz-Bericht zur Finanzierung des israelischen Atomprogramms [1:29]."]},
 {"typ":"abschnitt","titel":"🔎 Weiter recherchieren","liste":[
  "BKA-Studie „Schatten der Vergangenheit“ (2011) und der Aufsatz in Zeithistorische Forschungen 1/2012.",
  "Urteil des OLG Stuttgart (2012) und BGH 3 StR 92/13 zu Verena Becker.",
  "Senatsanhörung zu MKUltra (1977); Church Committee (1975/76) – im Gespräch nicht genannt, aber Grundlage für COINTELPRO und Operation CHAOS.",
  "Gladio/Stay-behind: Bericht der Bundesregierung 1990, BT-Drs. 17/14815 (2013), Ermittlungen des Generalbundesanwalts zum Oktoberfest-Attentat (Einstellung 2020) – im Gespräch nicht behandelt.",
  "Italienische Untersuchungskommission zum Fall Moro; Tom O'Neill, „Chaos“ (2019).",
  "Zum Hintergrund: {{a:ganser|Daniele Ganser (A-04)}} zu Gladio; {{a:wikihausen|Geschichten aus Wikihausen (A-10)}}; {{a:realtalk-pohlmannschmidt|zweites Gespräch mit Dirk Pohlmann}}."]},
]

# Kacheln füllen
ueberblick[0]['kacheln'][2][0] = str(NABG)


reiter = [
 {"id":K,"titel":f"{G}: Überblick","bloecke":ueberblick},
 {"id":K+"ab","titel":f"{G}: Gespräch im Detail","bloecke":detail},
 {"id":K+"zeit","titel":f"{G}: Zeitachse & Verzeichnisse","bloecke":zeit},
 {"id":K+"abgleich","titel":f"{G}: Abgleich & Daten","bloecke":abgleich},
]

def link_teile(s):
    return [[m.group(1), m.group(2)] for m in re.finditer(r'\[([^\]]+)\]\((https?://[^)]+)\)', s)]

quellen = [[f"Video: {TITEL} – {KANAL} (YouTube)", URL]]
seen = {URL}
for v in Q.values():
    for t,u in link_teile(v):
        if u not in seen: seen.add(u); quellen.append([t,u])

ueberblick[0]['kacheln'][4][0] = str(len(quellen))
out = {"k":K,"gast":GAST,"reiter":reiter,
 "folgen_zeile":[DATUM,f"{GAST} (Journalist, Dokumentarfilmer)",TITEL,"68er & Ohnesorg, Vietnam, V-Leute & RAF, Gladio & Moro, Hippies/Manson & MKUltra, Stammheim, Wahrheitskommission",f"{{{{a:realtalk-{K}|hier: {G}}}}}",f"[ansehen]({URL})"],
 "baum_ast":{"gruppe":"🏛️ Macht & Geschichte","t":"👤 Dirk Pohlmann bei REALTALK MEDIA – Geheimdienste, RAF, Gladio, Manson"},
 "neu":{"d":"2026-11-12","t":"REALTALK – Pohlmann: von RAF bis Manson","k":f"Geheimdienste, V-Leute und Terror von den 68ern bis zur RAF, Gladio und Manson – {NA} Abschnitte, Abgleich mit Quellen, 5 Diagramme.","h":f"#a-realtalk-{K}","art":"Video"},
 "quellen":quellen,
 "web":[]}

here = os.path.dirname(os.path.abspath(__file__))
json.dump(out, open(os.path.join(here,'folge.json'),'w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', NA, 'Abschnitte,', NABG, 'Abgleich-Zeilen,', len(Z), 'Zeitachse,', len(quellen), 'Quellen')
