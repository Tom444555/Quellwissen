# -*- coding: utf-8 -*-
# Erzeugt folge.json für „Masterpeace⎜Tom-Oliver Regenauer“ (K = masterpeace, Autor A-11 regenauer)
import json, os
K = 'masterpeace'; G = 'Masterpeace'
URL = 'https://www.youtube.com/watch?v=Uq7uKEKfH9Y'
TITEL = 'Masterpeace⎜Tom-Oliver Regenauer'
GAST = 'Tom-Oliver Regenauer'
DATUM = '2024 ❓'
DAUER = '58 Min.'

# ---------- Quellen (alle geprüft) ----------
Q = dict(
 pakt='[UN-Generalversammlung, A/RES/79/1: Pakt für die Zukunft (22.09.2024)](https://digitallibrary.un.org/record/4061879/files/A_RES_79_1-EN.pdf)',
 paktpga='[Präsident der UN-Generalversammlung: Pressemitteilung zur Annahme des Pakts für die Zukunft](https://www.un.org/pga/79/?p=281165)',
 unmit='[UN: Growth in United Nations membership](https://www.un.org/en/about-us/growth-in-un-membership)',
 ihr='[WHO (19.09.2025): Amended International Health Regulations enter into force](https://www.who.int/news/item/19-09-2025-amended-international-health-regulations-enter-into-force)',
 biz='[BIZ: History – overview](https://www.bis.org/about/history/overview)',
 bpb='[bpb, Glossar Antisemitismus: Struktureller Antisemitismus](https://www.bpb.de/themen/antisemitismus/dossier-antisemitismus/was-heisst-antisemitismus/glossar-antisemitismus/559900/struktureller-antisemitismus/)',
 repl='[UN Population Division: Replacement Migration (PDF, datiert 21.03.2000)](https://www.un.org/development/desa/pd/sites/www.un.org.development.desa.pd/files/unpd-egm_200010_un_2001_replacementmigration.pdf)',
 repl2='[UN Population Division: Replacement Migration](https://www.un.org/development/desa/pd/content/replacement-migration)',
 huxley='[Julian Huxley: UNESCO – its purpose and its philosophy (1946, PDF)](https://unesco.org.uk/site/assets/files/15161/068197engo.pdf)',
 nato='[NATO Innovation Hub / ACT: Cognitive Warfare (F. du Cluzel, Nov. 2020, PDF)](https://innovationhub-act.org/wp-content/uploads/2023/12/20210122_CW-Final.pdf)',
 cwa='[Corona-Warn-App: Solution Architecture (offizielle Dokumentation, GitHub)](https://github.com/corona-warn-app/cwa-documentation/blob/master/solution_architecture.md)',
 stat='[StatCounter: Mobile Operating System Market Share Germany (jährlich)](https://gs.statcounter.com/os-market-share/mobile/germany/)',
 diia='[Regierung der Ukraine (25.01.2024): State in a Smartphone – more than 20 million Ukrainians use Diia](https://www.kmu.gov.ua/en/news/derzhava-u-smartfoni-diieiu-korystuietsia-ponad-20-milioniv-ukraintsiv)',
 diiarp='[Rechnungskammer der Ukraine (04.02.2025): Audit von Digitalministerium und Diia](https://rp.gov.ua/en/cifrovizaciya-adminposlug-raxunkova-palata-provela-audit-diyalnosti-mincifri-ta-diyi)',
 uba='[Umweltbundesamt: Wie hoch sind die Treibhausgasemissionen pro Person in Deutschland?](https://www.umweltbundesamt.de/n88592de)',
 fabian='[Fabian Society: Our history](https://fabians.org.uk/about-us/our-history/)',
 cw='[Commonwealth Secretariat: About us](https://thecommonwealth.org/about-us)',
 cfr='[CFR: Queen Elizabeth II Was the Monarch of Fifteen Countries. What Does That Mean?](https://cfr.org/in-brief/queen-elizabeth-ii-monarch-fifteen-countries-what-does-mean)',
 wef='[WEF (03.06.2020): The Great Reset – A Unique Twin Summit to Begin 2021](https://weforum.org/press/2020/06/the-great-reset-a-unique-twin-summit-to-begin-2021)',
 blockade='[LumenLearning, World History: The British Naval Blockade](https://courses.lumenlearning.com/suny-hccc-worldhistory2/chapter/the-british-naval-blockade/)',
 sipri='[SIPRI Fact Sheet: Trends in World Military Expenditure, 2023 (April 2024)](https://www.sipri.org/sites/default/files/2024-04/2404_fs_milex_2023.pdf)',
 japan='[AP/Star-Advertiser (05.12.2022): Japan aims to boost 5-year defense spending to $318 billion](https://www.staradvertiser.com/?p=1208364)',
 bukele='[Mises Institute (14.03.2024): President Bukele Broaches Austrian Business Cycle Theory at CPAC](https://mises.org/power-market/president-bukele-broaches-austrian-business-cycle-theory-cpac)',
 destatis='[Vergabeblog (02.08.2024): Pro-Kopf-Verschuldung 2023: 28.943 EUR (Destatis-Meldung)](https://vergabeblog.de/2024-08-02/pro-kopf-verschuldung-2023-28-943-eur/)',
 bdst='[Bund der Steuerzahler (31.01.2024): Tempo 2024 – die Schuldenuhr tickt weiter viel zu schnell](https://www.steuerzahler.de/presse/detail/tempo-2024-die-schuldenuhr-tickt-weiter-viel-zu-schnell/)',
 eurostat='[Eurostat, gov_10dd_edpt1: Staatsverschuldung (Maastricht), Deutschland](https://ec.europa.eu/eurostat/databrowser/view/gov_10dd_edpt1/default/table?lang=de)',
 balfour='[The Rothschild Archive: Walter Rothschild and the Balfour Declaration](https://rothschildarchive.org/family/family_interests/walter_rothschild_and_the_balfour_declaration)',
 palest='[UN: History of the Question of Palestine](https://un.org/unispal/history2)',
 hanauer='[Wikipedia: Nick Hanauer](https://en.wikipedia.org/wiki/Nick_Hanauer)',
 superclass='[Wikipedia: Superclass (book)](https://en.wikipedia.org/wiki/Superclass_(book))',
 fedb1='[Federal Reserve History: First Bank of the United States](https://www.federalreservehistory.org/essays/first-bank-of-the-us)',
 fedb2='[Federal Reserve History: Second Bank of the United States](https://www.federalreservehistory.org/essays/second-bank-of-the-us)',
)

def ab(titel, th, *liste):
    return {"typ": "abschnitt", "titel": titel, "th": th, "liste": list(liste)}

# ---------- Abschnitte (Reihenfolge = Gesprächsverlauf) ----------
A = [
 ("0:00","0:03","Teaser, Vorstellung und das „Truman Show“-Zitat","w", ab("🎬 Teaser, Vorstellung und das „Truman Show“-Zitat [0:00–0:03]","w",
  "**Zusammenfassung:** Das Video beginnt mit einem Ausschnitt, in dem Regenauer über den UN-„Pakt für die Zukunft“ spricht (später ab [0:46] im Zusammenhang). Der Gastgeber (Name im Video nicht genannt ❓) leitet ein mit Fragen nach einer „unsichtbaren Weltregierung“, dem „Tiefen Staat“ und einer „Prädatorenkaste“ – ein Wort, das er Regenauer zuschreibt. Er stellt Regenauer als Manager, Musiker und Autor vor und lobt dessen Buch „Truman Show“, aus dem er eine längere Aufzählung vorliest (Volksvertreter, Gerichte, Universitäten, Kirchen, Green Economy, Bioethik, Medien, Banken). Leitfrage des Gesprächs: Wer steuert das?",
  "💬 „Bioethik nur Eugenik 2.0“ (aus dem Buch, vorgelesen vom Gastgeber) [0:02]",
  "📌 Der Gastgeber sagt von sich, er schreibe selbst Bücher; frühere Gäste bei Masterpeace waren laut ihm u. a. Ernst Wolff, Daniele Ganser und Jonas Tögel [0:06], [0:07], [0:13].",
  "📚 **Ergänzung:** Aufnahme vermutlich im Sommer 2024: Die Olympia-Eröffnung (26.07.2024) liegt zurück [0:11], der Zukunftsgipfel der UN (22.09.2024) steht „jetzt im September“ bevor [0:46]. Untertitel und Erscheinungsjahr des Buchs wurden hier nicht geprüft ❓.")),
 ("0:03","0:08","Wer steuert? Superclass, BIZ und UN – Nachfrage des Gastgebers","a", ab("🏦 Wer steuert? Superclass, BIZ und UN [0:03–0:08]","a",
  "**Zusammenfassung:** Regenauer: Das hänge von der Perspektive ab (finanziell, organisatorisch, juristisch). Er verweist auf David Rothkopfs Buch „Superclass“ – damals rund 6.000, heute etwa 7.000 Menschen, die „den Ton vorgeben“. Finanziell steuere das „Zentralbankenkartell“ mit Sitz in Basel, die Bank für Internationalen Zahlungsausgleich (BIZ). Organisatorisch sei es die UN. Der Streit um Pandemievertrag oder WHO-Austritt sei ein Ablenkungsmanöver, denn die Internationalen Gesundheitsvorschriften seien schon bindend; in der Corona-Krise hätten WHO-Vorgaben nationales Recht „ausgehebelt“. Die Welt werde gesteuert wie ein Konzern mit Leitplanken von oben. Richtiges Ziel sei, aus der UN auszutreten oder sie abzuschaffen.",
  "💬 „ein zutiefst korrupter undemokratischer Laden“ (Regenauer über die UN) [0:06]",
  "📌 Niemand wähle einen UN-Vertreter; Zentralbanken und UN seien „der Kern des Übels“ [seine Sicht] [0:06].",
  "📌 **Gastgeber:** Die BIZ sei geschaffen worden, um „letztendlich auch das Geld der Juden beiseite zu schaffen“ [0:06]; Regenauer greift das nicht auf. Weiter nennt der Gastgeber „Olympier“ bzw. ein „Komitee der 300“ (Quelle des Namens unklar ❓), die Militärmacht der USA und 9/11 („drei Wolkenkratzer lösen sich nicht in Staub auf“) und fragt, ob Präsidenten nur Marionetten seien [0:06–0:08].",
  "📚 **Ergänzung:** „Superclass“ erschien 2008 (nicht 2009) und nennt rund 6.000 Personen – siehe Abgleich; Gründung und Zweck der BIZ (1930, Reparationen nach dem Young-Plan) ebenfalls dort.")),
 ("0:08","0:11","Clubs ohne Protokoll – UN mit Belegen","a", ab("🎩 Clubs ohne Protokoll – die UN mit Belegen [0:08–0:11]","a",
  "**Zusammenfassung:** Präsidenten seien „austauschbare Werbeträger“, keine Entscheider. Es gebe viele Clubs – Bilderberger, WEF, Le Cercle, Trilaterale Kommission, Bohemian Grove (dort sei das Manhattan-Projekt vorbereitet worden) –, doch sie bräuchten ein „Verordnungskonstrukt“, um Beschlüsse umzusetzen. Der Nachhaltigkeitsplan einer Gemeinde komme nicht von den Bilderbergern, sondern über die UN-Nachhaltigkeitsziele von oben bis in die Gemeinde (30er-Zonen, Green Economy). Absprachen am privaten Dinner glichen Preisabsprachen im Kartell; ohne Protokoll lasse sich darüber nicht seriös berichten. Die UN liefere dagegen Belege, die vor Gericht bestehen würden.",
  "💬 „Indizien aber keine Belege und Beweise“ (Regenauer über die Clubs) [0:10]",
  "📌 Er sei selbst schon beim Bohemian Grove gewesen und habe dazu geforscht; Beispiele für Belege: RAND-Papiere zum Ukrainekrieg und das UN-Dokument „Replacement Migration“, das er auf 2003 datiert [0:10].",
  "📚 **Ergänzung:** Der UN-Bericht „Replacement Migration“ ist auf den 21.03.2000 datiert und rechnet Szenarien durch – siehe Abgleich. Dass das Manhattan-Projekt im Bohemian Grove vorbereitet wurde, wurde hier nicht geprüft ❓.")),
 ("0:11","0:13","Gastgeber: Olympia-Eröffnung, „Transenhumanismus“, NATO","b", ab("🎭 Gastgeber: Olympia-Eröffnung, „Transenhumanismus“, NATO [0:11–0:13]","b",
  "**Zusammenfassung:** Der Gastgeber verbindet das mit der Eröffnungsfeier der Olympischen Spiele 2024 (Abendmahl-Szene, blauer Bacchus, Marie Antoinette mit Kopf unter dem Arm). Er habe darüber geschrieben und nenne es „Transenhumanismus“: Eine Minderheit solle die Mehrheit dominieren, Gendern schaffe keine fairere Welt, das Normale werde pathologisiert, Kinder würden als CO2-Last gesehen. Es laufe auf eine „Atomisierung“ hinaus. Jonas Tögel habe bei Masterpeace dargelegt, die NATO unterstütze diese Agenda.",
  "💬 „das ist die sechste Dimension der Kriegsführung“ (Gastgeber über die NATO) [0:13]",
  "📌 Auf der Webseite des NATO Innovation Hub fänden sich Dokumente dazu [seine Sicht, Gastgeber] [0:13].",
  "📚 **Ergänzung:** Eine vom NATO-Kommando ACT geförderte Studie von 2020 nennt die „Human Domain“ als sechste operative Domäne; sie gibt laut Vorbemerkung nicht die Position der NATO wieder – siehe Abgleich. Ob sie eine „Atomisierung“ oder sexuelle Neutralität als Ziel nennt, wurde hier nicht geprüft ❓.")),
 ("0:13","0:16","Eugenik als britische Bewegung und Huxleys UNESCO-Schrift","b", ab("🧬 Eugenik als britische Bewegung und Huxleys UNESCO-Schrift [0:13–0:16]","b",
  "**Zusammenfassung:** Regenauer: Unter dem Schlagwort Transhumanismus verstecke sich, was früher Eugenik war – nie verschwunden, auch nach Hitler nicht, und eigentlich eine britische Bewegung (George Bernard Shaw, Bertrand Russell, Margaret Sanger). Heute heiße sie biosoziale Forschung, Bioethik, biodigitale Konvergenz und gipfle in der Verschmelzung von Mensch und Maschine der „vierten industriellen Revolution“; das ziele am Ende auf die Abschaffung der Spezies. Im Gespräch fallen dazu Elon Musks Neuralink und weitere Hirn-Chips (Gastgeber, vermutlich). Als Beleg nennt Regenauer das UNESCO-Gründungsdokument von 1946 von Julian Huxley.",
  "💬 „man muss das Undenkbare wieder denkbar machen“ (Regenauer über Huxleys Schrift, S. 21) [0:15]",
  "📌 Sanger habe auch Pro Familia in Deutschland gegründet ❓; KZs habe es schon in Afrika „durch Cecil Rhodes“ gegeben (Sprecherwechsel an dieser Stelle unklar ❓) [0:13–0:14].",
  "📌 Ein „Blackrock“-Hirnchip und ein Chip der Rockefeller Foundation werden erwähnt ❓ [0:14].",
  "📚 **Ergänzung:** Huxleys Text enthält auf S. 21 tatsächlich den Satz, Undenkbares solle „zumindest denkbar“ werden – im Zusammenhang einer Eugenik-Politik, die „für viele Jahre politisch und psychologisch unmöglich“ sei; Wortlaut im Abgleich. Die britischen Lager im Burenkrieg (1899–1902) entstanden unter Kitchener, nicht unter Rhodes.")),
 ("0:16","0:19","Biodigitale Konvergenz, Huxley gegen Orwell, Technokratie","b", ab("🤖 Biodigitale Konvergenz, Huxley gegen Orwell, Technokratie [0:16–0:19]","b",
  "**Zusammenfassung:** UNESCO, WHO, IWF und Weltbank seien keine eigenständigen Apparate, sondern Teile der UN mit „72 plus“ Unterorganisationen. UN, NATO und Wirtschaft (Elon Musk, Ray Kurzweil) hielten die biodigitale Konvergenz für ein Evolutionsziel – für Regenauer „Eugenik 2.0“, die eine unkritische Arbeiterklasse formen solle. In Huxleys „Schöne neue Welt“ seien die Kasten (Alphas bis Epsilons) genetisch zementiert, schlimmer als Orwells Überwachungsstaat, weil Widerstand physisch unmöglich werde. Technokratie sei 1919 als „Technical Alliance“ entstanden, 1933 zu „Technocracy Inc.“ geworden und heute Grundlage des Herrschaftsmodells in China.",
  "💬 „ein tausendjähriges Reich vielleicht ja 2.0“ (Regenauer) [0:17]",
  "📌 Kurzweil sei früher „Entwicklungschef“ bei Google gewesen und berate US-Präsidenten zur digitalen Transformation ❓ [0:16].",
  "📌 Ab [0:19] blendet Masterpeace einen Spendenaufruf ein (Produktionskosten).")),
 ("0:19","0:22","Bürger in 15 Jahren: Bluetooth, Diia-App, CO2-Budget","c", ab("📱 Bürger in 15 Jahren: Bluetooth, Diia-App, CO2-Budget [0:19–0:22]","c",
  "**Zusammenfassung:** Auf die Frage nach dem Bürger in 15 Jahren beschreibt Regenauer die Smart City als „Ideal der Herrschaftskaste“: Alle Smartphones hätten Bluetooth Low Energy, das untereinander kommuniziere, auch wenn man es abschalte; da 98 % der Bevölkerung iOS oder Android nutzten, sei die Bevölkerung „kartografiert“. Darüber sei auch die Corona-Warn-App gelaufen. Im Internet der Dinge wisse das System, wo man ist, was man kauft, wie man schläft und welche Medikamente man nimmt. Vorbild sei die ukrainische Diia-App („State in the Smartphone“) mit über 100 Funktionen, die 70 % der Bevölkerung nutzten. Geofencing könne den Bewegungsradius einschränken, ein CO2-Budget komme hinzu.",
  "💬 „in der Tagesschau war die Rede von eineinhalb Tonnen pro Kopf“ (Regenauer) [0:21]",
  "📌 Mit 1,5 t müsse man „obdachlos sein als Veganer“; der Bewegungsradius werde auf „15 m“ eingeschränkt (gemeint vermutlich km ❓) [0:21–0:22].",
  "📚 **Ergänzung:** Laut Umweltbundesamt liegt der Pro-Kopf-Ausstoß in Deutschland derzeit bei 10,3 t CO2e; klimaverträglich wären „deutlich unter 1 t“. Die genannte Tagesschau-Stelle wurde nicht gefunden ❓. Zu Bluetooth, Marktanteilen und Diia siehe Abgleich.")),
 ("0:22","0:25","Technokratie 1.0 und 2.0: China, Ukraine, 15-Minuten-Stadt","c", ab("🏙️ Technokratie 1.0 und 2.0: China, Ukraine, 15-Minuten-Stadt [0:22–0:25]","c",
  "**Zusammenfassung:** Künftig steuere das Smartphone oder ein Implantat das Individuum; kein Polizist müsse mehr eingreifen, weil die Smart-Home-Tür zu bleibe oder das Auto nicht starte – etwa bei einem „Klima-Lockdown“. China sei Technokratie 1.0 (Drohne am Balkon), in der Ukraine baue man 2.0 mit Amazon, Apple, Google und Microsoft; der Staat führe dort „nur noch Krieg“. Die App werde in Estland ausgerollt, in Washington diskutiert und sei Pilotprojekt für die EU. Der Gastgeber ergänzt: KI als ausführendes Organ, 15-Minuten-Stadt, digitales Zentralbankgeld (CBDC), das außerhalb der Stadt nichts wert sei, und automatische Strafzahlungen.",
  "💬 „China ist Version 1.0 der Technokratie“ (Regenauer) [0:22]",
  "📌 Gesteuert werde nicht von einer Person, sondern von „einer zentralen Datenbank“ bzw. Algorithmen [seine Sicht] [0:23].",
  "📚 **Ergänzung:** Laut ukrainischer Regierung nutzten im Januar 2024 über 20 Mio. Menschen Diia; die Rechnungskammer zählte 2024 über 18,5 Mio. App-Nutzer – siehe Abgleich und Prüfstand.")),
 ("0:25","0:28","Auswege: Zeitkonten, andere Telefone, Boykott","g", ab("🛠️ Auswege: Zeitkonten, andere Telefone, Boykott [0:25–0:28]","g",
  "**Zusammenfassung:** Das System sei zu groß und zu gut bewaffnet, um es zu stürzen; man könne aber dezentrale Netzwerke aufbauen und außerhalb des Fiat-Geldsystems handeln, etwa mit Zeitkonten in der Gemeinde (eine Stunde = 20 €). Alternative Geräte (Fairphone, „Above Phone“) entzögen einen dem „Überwachungsgrid“. Wandel fange im Kleinen an; wer weiter Google-Adresse, Netflix und iPhone nutze, sei „Teil des Problems“. Wer auf PayPal verzichte, bewege Händler irgendwann zu Alternativen.",
  "💬 „boykottieren und dem System Energie … entziehen“ (Regenauer) [0:27]",
  "📌 Jedes Smartphone schicke nachts „12 MB“ Daten an Hersteller oder Cloud-Anbieter [seine Sicht] [0:25–0:26].",
  "📚 **Ergänzung:** Eine Messung des Trinity College Dublin (Leith, 2021) fand im Leerlauf etwa 1 MB je 12 Stunden (Android an Google) bzw. 52 KB (iPhone an Apple) – siehe Prüfstand.")),
 ("0:28","0:31","Warum keine Revolution? Dritter Weg – und Widerspruch","a", ab("⚔️ Warum keine Revolution? Dritter Weg – und Widerspruch [0:28–0:31]","a",
  "**Zusammenfassung:** Den „Mistgabel-Mob“ habe Nick Hanauer vorhergesagt; Aufstände werde es geben, aber keine Revolution habe je Freiheit gebracht – das Machtvakuum fülle ein anderer Block (Beispiel Frankreich). Die heutige Sozialdemokratie beruhe auf dem Konzept der Fabian Society für einen „dritten Weg“, entwickelt von denselben Leuten wie die Eugenik; alles links und rechts werde als extremistisch diffamiert. Damit hätten Blair, Clinton und Merkel (16 Jahre) gewonnen. Gewaltsame Revolution lehnt Regenauer ab: Protest müsse friedlich sein.",
  "💬 „Protest muss friedlich sein“ (Regenauer) [0:29]",
  "📌 **Gastgeber widerspricht teilweise:** Die Französische Revolution habe den Adel entmachtet (danach kam der „Geldadel“), und vor der Weimarer Verfassung seien Knechte und Mägde nahezu rechtlos gewesen – es habe sich also etwas getan. Die Machtstruktur sei 250–300 Jahre alt; Macht sei maximal, wenn sie unsichtbar ist; wo ein Netz ist, gebe es eine Spinne – „wem nützt es?“ [0:29–0:31]",
  "📚 **Ergänzung:** Hanauer war erster familienfremder Investor bei Amazon, nicht Mitgründer; sein Text „The Pitchforks Are Coming… For Us Plutocrats“ erschien im Juni 2014 im Politico Magazine ([Wikipedia](https://en.wikipedia.org/wiki/Nick_Hanauer)). Zur Fabian Society siehe Abgleich.")),
 ("0:31","0:34","Commonwealth, Krone und Great Reset","d", ab("👑 Commonwealth, Krone und Great Reset [0:31–0:34]","d",
  "**Zusammenfassung:** Die „Spinne“ seien die rund 7.000 Namen aus Rothkopfs Buch; die Vorstellung einer kleinen Verschwörergruppe im Hinterzimmer nennt Regenauer naiv, ebenso QAnon, „White Hats“ und Trump als Erlöser („Beschäftigungstherapie“). Die Monarchie habe sich nur zurückgezogen, das britische Empire bestehe fort; das US-Militär arbeite in dessen Auftrag. Nach Rhodes, Milner, Edward Mandell House und Alfred Zimmern (Völkerbund-Papiere) habe das Empire die Welt über ein Verordnungskonstrukt statt militärisch beherrschen wollen. Heute heiße es Commonwealth: 56 Staaten, „29,4 %“ der Weltbevölkerung, 15 Staaten unter der Krone. Den Great Reset habe zuerst Charles verkündet. Die Königshäuser Spaniens, der Niederlande und Großbritanniens stammten von Graf Dietrich (932) bzw. dem Haus Wettin ab; Sachsen-Coburg und Gotha hießen die britischen Royals bis 1917.",
  "💬 „da wird niemand Präsident oder Premierminister ohne das King Charles unterschreibt“ (Regenauer) [0:32]",
  "📌 Charles habe einen „Business Council“ gegründet, der später in Club of Rome und WEF aufgegangen sei ❓ [0:33].",
  "📚 **Ergänzung:** Commonwealth 56 Mitglieder, 2,7 Mrd. Menschen; der Monarch ist Staatsoberhaupt von 15 Ländern, seine Befugnisse sind laut CFR „weitgehend symbolisch“; den Great Reset starteten am 03.06.2020 der Prince of Wales und Klaus Schwab – siehe Abgleich.")),
 ("0:34","0:38","Warum Krieg gegen Deutschland? Blockade, Zentralbanken, City of London","d", ab("⚓ Warum Krieg gegen Deutschland? Blockade, Zentralbanken, City of London [0:34–0:38]","d",
  "**Zusammenfassung:** Der Gastgeber fragt, warum die ursprünglich deutschstämmige Krone Deutschland angegriffen habe. Regenauer: Churchill habe lange vor dem Ersten Weltkrieg gesagt, die Deutschen würden ihren Krieg bekommen ❓. Das Empire sei geschwächt gewesen (Verlust der 13 Kolonien, keine dauerhafte Zentralbank in den USA: First Bank 1791 mit 20-Jahres-Lizenz, Second Bank 1816, von Andrew Jackson beendet). Deutschland sei wirtschaftlich, militärisch und gesellschaftlich am schnellsten aufgerückt, eine Annäherung an Russland gefürchtet worden. Ausgelöst hätten den Ersten Weltkrieg die Briten mit der Seeblockade; die Briten hätten zudem Japans Flotte finanziert ❓.",
  "💬 „diejenigen die den Ersten Weltkrieg ausgelöst haben waren am Ende die Briten“ (Regenauer) [0:35]",
  "📌 **Gastgeber:** Auch Frankreich habe Angst vor Deutschland gehabt, es sei um Kolonien gegangen („Platz an der Sonne“). Die City of London sei mit Geld „sogar aus Deutschland“ gegründet worden, und König Charles müsse um Erlaubnis bitten, sie zu betreten ❓ – sei das Empire nicht nur ein „Handschuh des Geldes“? Regenauer stimmt zu: Militärische Macht sei „der verlängerte ausführende Arm der Finanzmacht“; er verweist auf Rhodes' Testamente und auf Milner, der den Versailler Vertrag mitverhandelt habe [0:36–0:38].",
  "📚 **Ergänzung:** Die Blockade begann nach Kriegsausbruch im August 1914, die Nordsee wurde Anfang November 1914 zum Kriegsgebiet erklärt – siehe Abgleich. Zur First und Second Bank: [Fed History: First Bank](https://www.federalreservehistory.org/essays/first-bank-of-the-us) · [Fed History: Second Bank](https://www.federalreservehistory.org/essays/second-bank-of-the-us).")),
 ("0:38","0:41","BIZ, Rothschild, Milner – Gastgeber: Schulden und Japan","e", ab("🏛️ BIZ, Rothschild, Milner – Gastgeber: Schulden und Japan [0:38–0:41]","e",
  "**Zusammenfassung:** Darum spreche Ernst Wolff so oft über die BIZ: Die Generalversammlung mit ihren 63 Zentralbanken sei wohl das folgenschwerste Treffen des Jahres; über Zinsen, Abwertungen und Geldmenge steuere man Wirtschaft, Inflation und „am Ende auch Kriege“. Die Rothschilds hätten damals einen Großteil der Bank of England dominiert, die wiederum 80 % der First Bank of the USA besessen habe ❓. Sein Artikel heiße „Monopole, Macht und Mord“ ❓. Milner und Rhodes hätten mit der Round-Table-Bewegung die Geopolitik konzeptionell neu geordnet und den Staat zur Durchsetzung genutzt.",
  "💬 „es sind immer die Banker“ (Regenauer) [0:39]",
  "📌 **Gastgeber:** Schulden müssten durch Gewalt (Militär, Polizei, Gerichtsvollzieher) gesichert werden. Beispiel Japan: Die Zentralbank habe einen Aufschwung gepusht und die Blase platzen lassen; nun bekomme Japan einen „gigantischen Etat“ für Rüstung – „Platz 3 nach China“, „300 Milliarden pro Jahr“ [0:39–0:40].",
  "📚 **Ergänzung:** SIPRI: Japan 2023 auf Platz 10 mit 50,2 Mrd. US-$; 43 Bio. Yen (≈ 318 Mrd. US-$) ist das Ziel für fünf Jahre 2023–2027 – siehe Abgleich und Diagramme. Das Milner-Zitat wurde hier nicht geprüft ❓.")),
 ("0:41","0:44","Bukele, Staatsschulden, Zinseszins – Taiwan","e", ab("💸 Bukele, Staatsschulden, Zinseszins – Taiwan [0:41–0:44]","e",
  "**Zusammenfassung:** Nayib Bukele habe im Februar auf einer konservativen US-Konferenz das Geldsystem zusammengefasst: Bürger zahlten hohe Steuern nur, um die Illusion zu erhalten, sie finanzierten den Staat; seit dem Ende der Goldbindung finanziere sich der Staat über Anleihen „auf Papier“. Laut Bund der Steuerzahler wäre Deutschland bei einer Milliarde Tilgung pro Monat erst um 2230 schuldenfrei; pro Kopf seien es „24, 25.000“. Andrew Jackson habe eine eigene Währung ohne Zentralbank gewollt; Länder, die aus dem System wollten, „bekamen dann Besuch“. Durch den Zinseszins sei immer zu wenig Geld im System, Zentralbanken liefen auf ein Weltkriegsszenario hinaus. Japan und Australien würden gegen China aufgestellt, wie zuvor die Ukraine per NATO-Osterweiterung („Zangengriff“); Schlachtfeld sei Taiwan.",
  "💬 „es wurde Demokratie abgeworfen“ (über Staaten ohne Zentralbank) [0:42]",
  "📌 Die Sprecherwechsel sind in diesem Teil nicht eindeutig; die Zinseszins- und Weltkriegs-These äußert der Gastgeber („wie du sie nennst: Prädatorenkaste“) und fragt abschließend, ob die Elite den Dritten Weltkrieg „von langer Hand geplant“ habe [0:42–0:44].",
  "📚 **Ergänzung:** Bukeles Satz (CPAC, Februar 2024) ist belegt; Schuldenstand und Pro-Kopf-Wert im Abgleich (Destatis 2023: 28.943 € je Einwohner).")),
 ("0:44","0:48","Historische Konstante: von Versailles bis zum Pakt für die Zukunft","e", ab("🕊️ Historische Konstante: von Versailles bis zum Pakt für die Zukunft [0:44–0:48]","e",
  "**Zusammenfassung:** Regenauer: Die „Zeitenwende“ sei eine historische Konstante. Vor 1914 sei ein Weltkrieg unvorstellbar gewesen; Foch habe Versailles einen „Waffenstillstand für 20 Jahre“ genannt. Aus den Weltkriegen sei auch Israel hervorgegangen: Die Briten hätten Palästina den Arabern versprochen und dann über die Balfour-Erklärung, die „aus den Finanzeliten kam“, dem jüdischen Volk zugesprochen. Religion sei ihm egal, man müsse Menschen an Taten messen; es gehe um organisierte Kriminalität. Jeder Krieg verleihe einer Institution mehr Macht: Völkerbund, UN, Weltbank, IWF, UNESCO; für den Endausbau der Global Governance brauche es einen dritten Weltkrieg. Inkompetente Regierungen delegitimierten den Nationalstaat. Im September zünde mit dem „Pakt für die Zukunft“ die nächste Stufe – mehr Befugnisse für die UN und erstmals ein globales Steuermodell. Wahlen seien „Pluralismussimulation“ (election vs. selection). Die Finanzblase sei hundertfach größer als 2008 und werde kontrolliert kollabieren, um auf digitales Geld umzustellen.",
  "💬 „ab der Einführung einer Steuer konstituiert sich ein Staat“ (Regenauer) [0:47]",
  "💬 „mir ist Religion völlig egal“ (Regenauer) [0:45]",
  "📌 „Ordo ab Chao“ stehe auf dem Dollar [seine Sicht] ❓ [0:48].",
  "📚 **Ergänzung:** Der Pakt (A/RES/79/1) enthält Zusagen zur internationalen Steuerkooperation und einer UN-Rahmenkonvention, keine von der UN erhobene Steuer; neue Krisenbefugnisse sollen „innerhalb bestehender Befugnisse“ liegen – Wortlaut im Abgleich. Auf dem Großen Siegel der USA (Dollarschein) steht „Novus ordo seclorum“.")),
 ("0:48","0:51","Zionismus-Frage – Regenauers Unterscheidungen","f", ab("✡️ Zionismus-Frage – Regenauers Unterscheidungen [0:48–0:51]","f",
  "**Zusammenfassung:** Der Gastgeber fragt nach dem Zionismus: Biden und Trump hätten sich dazu bekannt, Trumps Schwiegersohn sei Jude, Israel sei aus dem Zweiten Weltkrieg hervorgegangen; zum orthodoxen Glauben gehöre der Wiederaufbau des Tempels auf dem Tempelberg; das klinge nach einer „Rothschildverschwörung … par excellence“. Regenauer antwortet, der Glaube sei ihm egal – auch Buddhisten würde er dann ablehnen –, es gehe um eine „kriminelle Kaste“. Er habe lange in Israel und Palästina (Gaza) gelebt und gearbeitet; auf beiden Seiten gebe es 10–20 % Extremisten (Hamas und radikale Islamisten, radikale Zionisten), die Mehrheit wolle in Frieden leben. Zionismus sei wie Technokratie ein Herrschaftsmodell, religiös begründet; in Herzls Schriften und zionistischen Dokumenten stünden „Kolonialisierungsprojekt“ und Ausrottungsabsichten ❓.",
  "💬 „Leute werfen das ja immer durcheinander“ (Regenauer über Judentum und Zionismus) [0:49]",
  "📌 **Regenauers Unterscheidung:** Israelis bzw. Israel als Staat und Regierung (die Likud-Partei nennt er rechtsradikal, „wie es auch Haaretz schreibt“ ❓) – Judentum als Glaube – orthodoxe und „normale“ Juden (er habe jüdische Freunde) – Zionisten. Antisemitismus- oder Antijudaismus-Vorwürfe weist er zurück; ein Mörder müsse unabhängig von seiner Religion verurteilt werden [0:50–0:51].",
  "📚 **Ergänzung:** Die Balfour-Erklärung vom 02.11.1917 war ein Brief an Walter Rothschild; Mandat 1922, Teilungsplan 1947, Unabhängigkeitserklärung Israels 1948 – siehe Abgleich. Welche Herzl-Schriften gemeint sind, nennt er nicht; hier nicht geprüft ❓.")),
 ("0:51","0:58","Kein Plan, keine Angst – vorleben; Schlussworte","g", ab("🌱 Kein Plan, keine Angst – vorleben; Schlussworte [0:51–0:58]","g",
  "**Zusammenfassung:** Der Gastgeber fragt nach Regenauers Plan für die nächsten 20 Jahre (er lebe seit rund 15 Jahren in der Schweiz; Scherz über einen Bunker). Regenauer: Er habe nie einen Plan, lebe im Moment; man dürfe vor allem keine Angst haben – Ohnmacht, Apathie, Agonie und Angst seien genau die Lage, in der einen das System haben wolle. Fernseher und Newsfeed aus; er selbst schaue 15–20 Minuten Nachrichten am Tag und lese Bücher. Kein „weißer Reiter“ (Trump, Merz, Musk) werde kommen; es gehe um den freien Willen: anderes Smartphone, Linux statt Apple oder Google. Wie im Management („lead by example“) wirke Vorleben ansteckend. Er nutze fast nur noch Alternativen; nur das Apple-Ökosystem (Logic als Musiker) löse er gerade ab. Der Gastgeber schließt: Macht sei der größte Feind der Freiheit, man solle nicht auf Politiker hoffen. Abspann mit Spendenaufruf für Masterpeace, „ein Projekt das den Weltfrieden fördern möchte“.",
  "💬 „frei wird man nicht frei ist man“ (Regenauer) [0:57]",
  "💬 „das Leben ist schön“ (Regenauer) [0:53]",
  "📌 Während der Corona-Krise hätten sich viele Menschen kennengelernt, die sich sonst nie getroffen hätten [0:55].")),
]

# Themen
THEMEN = [{"k":"a","n":"Macht & Global Governance"},{"k":"b","n":"Transhumanismus & Eugenik"},{"k":"c","n":"Digitale Kontrolle"},
          {"k":"d","n":"Empire, Krone & Weltkriege"},{"k":"e","n":"Geld, Schulden & Krieg"},{"k":"f","n":"Israel, Zionismus & Religion"},
          {"k":"g","n":"Auswege & Haltung"},{"k":"w","n":"Einstieg/Organisatorisches"}]
teile = [{"von":v,"bis":b,"t":t,"th":th} for v,b,t,th,_ in A]
abschnitte = [x[4] for x in A]
NA = len(abschnitte)

# ---------- Reiter 1: Überblick ----------
kern = [
 ["1","Die Welt werde von oben nach unten gesteuert: finanziell über die Zentralbanken mit der BIZ an der Spitze, organisatorisch über die UN.","Konzern-Analogie; Superclass; Nachhaltigkeitspläne bis in die Gemeinde","[0:03–0:10]","★★★"],
 ["2","Die UN sei undemokratisch; richtig wäre Austritt oder Abschaffung.","Niemand wähle UN-Vertreter; IHR seien schon bindend","[0:04–0:06]","★★"],
 ["3","Clubs wie Bilderberg oder Bohemian Grove liefern keine gerichtsfesten Belege – UN-Dokumente schon.","Replacement Migration, RAND-Papiere, SDGs","[0:08–0:11]","★★"],
 ["4","Transhumanismus sei Eugenik 2.0, schon im UNESCO-Gründungstext angelegt.","Huxley 1946, S. 21; britische Eugenik-Bewegung; biodigitale Konvergenz","[0:13–0:19]","★★★"],
 ["5","Die Smart City mit Smartphone, App und CO2-Budget werde ein unsichtbares Gefängnis; Diia in der Ukraine sei der Pilot.","Bluetooth Low Energy, 98 % iOS/Android, Diia, China","[0:19–0:25]","★★★"],
 ["6","Eine Revolution werde nicht stattfinden; Auswege seien dezentrale Netze, Alternativen und Boykott – friedlich.","Zeitkonten, Fairphone, Linux; „Dritter Weg“ der Fabians","[0:25–0:31]","★★"],
 ["7","Das britische Empire bestehe als Commonwealth und über Finanzmacht fort; die US-Hegemonie arbeite in seinem Auftrag.","56 Staaten, 15 Realms, Great Reset, Rhodes/Milner","[0:31–0:34]","★★"],
 ["8","Die Briten hätten den Ersten Weltkrieg mit der Seeblockade ausgelöst, aus Angst vor Deutschlands Aufstieg.","Churchill, Zentralbankfrage USA, Japans Flotte","[0:34–0:38]","★★"],
 ["9","Kriege seien eine historische Konstante, gesteuert über Geld; jede Krise stärke supranationale Institutionen – nächste Stufe: Pakt für die Zukunft.","BIZ, Foch, Balfour, Weltkriege → UN; globale Steuer","[0:38–0:48]","★★★"],
 ["10","Zionismus sei ein Herrschaftsmodell; davon zu trennen seien Judentum, Israelis und der Staat Israel.","Erfahrungen in Israel und Gaza; Herzl; Likud","[0:48–0:51]","★★"],
]
baum = {"typ":"baum","titel":"🌳 Themenbaum des Gesprächs","wurzel":TITEL,"unter":f"{GAST} · Masterpeace (YouTube-Kanal {GAST}) · {DATUM} · {DAUER}","knoten":[
 {"t":"🏦 Wer steuert? [0:03–0:11]","k":[{"t":"📕 Superclass: 6.000–7.000 Menschen [0:03]"},{"t":"🏦 BIZ in Basel als Zentrale [0:04]"},{"t":"🇺🇳 UN als Verordnungskonstrukt [0:05]"},{"t":"🩺 Gesundheitsvorschriften der WHO [0:05]"},{"t":"🎩 Clubs ohne Protokoll [0:08–0:10]"}]},
 {"t":"🧬 Eugenik & Transhumanismus [0:11–0:19]","k":[{"t":"🎭 Olympia-Eröffnung 2024 (Gastgeber) [0:11]"},{"t":"🪖 NATO: „sechste Dimension“ [0:13]"},{"t":"🇬🇧 Britische Eugenik-Bewegung [0:13]"},{"t":"📜 Huxleys UNESCO-Schrift 1946 [0:15]"},{"t":"🤖 Biodigitale Konvergenz, Technokratie [0:16–0:18]"}]},
 {"t":"📱 Digitale Kontrolle [0:19–0:25]","k":[{"t":"📶 Bluetooth Low Energy [0:20]"},{"t":"🇺🇦 Diia: Staat im Smartphone [0:20–0:21]"},{"t":"🌡️ CO2-Budget 1,5 t [0:21]"},{"t":"🇨🇳 Technokratie 1.0 und 2.0 [0:22]"},{"t":"💳 15-Minuten-Stadt und CBDC [0:24]"}]},
 {"t":"🛠️ Auswege [0:25–0:31]","k":[{"t":"⏱️ Zeitkonten, dezentrale Netze [0:25]"},{"t":"📵 Fairphone, Linux, Boykott [0:25–0:27]"},{"t":"⚔️ Keine Revolution, friedlicher Protest [0:28–0:29]"},{"t":"🔄 Gastgeber: Fortschritte seit 1918 [0:29–0:30]"}]},
 {"t":"👑 Empire & Weltkriege [0:31–0:38]","k":[{"t":"🌐 Commonwealth: 56 Staaten [0:32]"},{"t":"🔄 Great Reset und Charles [0:32]"},{"t":"🏰 Wettiner, Sachsen-Coburg-Gotha [0:33]"},{"t":"⚓ Seeblockade 1914 [0:35]"},{"t":"🏙️ City of London (Gastgeber) [0:36]"}]},
 {"t":"💸 Geld, Schulden & Krieg [0:38–0:48]","k":[{"t":"🏛️ BIZ: 63 Zentralbanken [0:38]"},{"t":"🇯🇵 Japan rüstet auf (Gastgeber) [0:40]"},{"t":"🇸🇻 Bukele zu Steuern [0:41]"},{"t":"📉 Staatsschulden, Zinseszins [0:42]"},{"t":"🌍 Pakt für die Zukunft [0:46]"}]},
 {"t":"✡️ Israel & Zionismus [0:44–0:51]","k":[{"t":"📜 Balfour-Erklärung [0:45]"},{"t":"❓ Frage des Gastgebers [0:48]"},{"t":"🧭 Regenauers Unterscheidungen [0:49–0:50]"}]},
 {"t":"🌱 Haltung [0:51–0:58]","k":[{"t":"🕊️ Keine Angst, im Moment leben [0:52]"},{"t":"📚 Bücher statt Newsfeed [0:53]"},{"t":"👣 Vorleben [0:54]"},{"t":"🗽 „Frei ist man“ [0:57]"}]},
]}
ueberblick = [
 {"typ":"folge","k":K,"titel":TITEL,"gast":GAST,"rolle":"Autor, früher Musiker und Manager; lebt in der Schweiz","kanal":"Masterpeace",
  "datum":DATUM,"dauer":DAUER,"url":URL,
  "thema":"Tom-Oliver Regenauer erklärt bei Masterpeace, wer die Welt aus seiner Sicht steuert – Zentralbanken mit der BIZ, die UN als Verordnungsapparat, das fortbestehende britische Empire – und spricht über Eugenik und Transhumanismus, digitale Kontrolle, Kriege, Zionismus und persönliche Auswege.",
  "kacheln":[[str(NA),"Abschnitte"],["10","Kernaussagen"],["18","Abgleich-Punkte"],["37","Zeitachse"],["5","Diagramme"]]},
 {"typ":"hinweis","text":"Auswertung nach dem Transkript (automatische Untertitel): Gesagtes ohne Zeichen, Ergänzungen 📚, Unklares ❓. Fundstellen [Stunde:Minute] springen ins Video. Die Bewertung bleibt dem Leser."},
 {"typ":"abschnitt","titel":"⚡ In Kürze","liste":[
  f"**Wer:** {GAST}, Autor, im Gespräch mit dem (im Video nicht namentlich genannten ❓) Gastgeber von Masterpeace; hochgeladen auf Regenauers YouTube-Kanal, aufgenommen vermutlich im Sommer 2024, 58 Minuten. Zu seinem langen Gespräch bei {{ungeskriptet}} siehe {{{{a:ungeskriptet-regenauer|Regenauer bei {{ungeskriptet}}}}}}.",
  "**Steuerung:** Finanziell steuere ein „Zentralbankenkartell“ um die BIZ in Basel, organisatorisch die UN, deren Vorgaben bis in die Gemeinde durchgereicht würden; private Clubs lieferten keine Belege [0:03–0:11].",
  "**Eugenik:** Transhumanismus und biodigitale Konvergenz seien „Eugenik 2.0“; als Beleg dient Julian Huxleys UNESCO-Schrift von 1946 [0:13–0:19].",
  "**Digitale Kontrolle:** Smartphones, Bluetooth, Apps wie die ukrainische Diia und ein CO2-Budget könnten ein unsichtbares Gefängnis bilden [0:19–0:25].",
  "**Auswege:** Keine Revolution, sondern friedlicher Rückzug: Zeitkonten, alternative Geräte, Boykott; der Gastgeber widerspricht teilweise mit sozialen Fortschritten seit 1918 [0:25–0:31].",
  "**Empire und Kriege:** Das britische Empire lebe im Commonwealth fort; die Briten hätten den Ersten Weltkrieg mit der Seeblockade ausgelöst; Kriege dienten dem Ausbau supranationaler Institutionen bis zum „Pakt für die Zukunft“ [0:31–0:48].",
  "**Zionismus:** Auf die Frage des Gastgebers trennt Regenauer Judentum, Israelis, Staat und Zionismus und nennt letzteren ein Herrschaftsmodell [0:48–0:51].",
  "**Haltung:** Keine Angst, im Moment leben, vorleben – „frei wird man nicht, frei ist man“ [0:51–0:58]."]},
 {"typ":"abschnitt","titel":"🔦 Aus Regenauers Sicht – der rote Faden","liste":[
  "[seine Sicht] Macht ist am größten, wo sie unsichtbar ist; sichtbare Politiker sind austauschbare Werbeträger, entschieden wird über Geld und über Regelwerke.",
  "[seine Sicht] Weil sich private Absprachen nicht belegen lassen, schaut er auf das, was dokumentiert ist: Zentralbanken mit der BIZ und die UN mit ihren Unterorganisationen, deren Vorgaben von oben nach unten durchgereicht werden.",
  "[seine Sicht] Dieselbe Linie sieht er historisch: vom britischen Empire über Rhodes und Milner, Weltkriege und Völkerbund bis zur UN – jede Krise verleihe supranationalen Institutionen mehr Macht, als Nächstes über den Pakt für die Zukunft und digitales Geld.",
  "[seine Sicht] Technik gibt dem alten Ziel der Eugenik heute die Mittel: Smartphones, Apps und Implantate können Verhalten steuern, ohne dass ein Polizist eingreifen muss.",
  "[seine Sicht] Deshalb setzt er nicht auf Revolution oder einen Retter, sondern auf den Einzelnen: Angst ablegen, Alternativen nutzen, dem System Geld und Aufmerksamkeit entziehen und ein gutes Leben vorleben."]},
 {"typ":"text","text":"🎯 **Kernaussagen** – die zehn wichtigsten Thesen des Gesprächs:"},
 {"typ":"tabelle","kopf":["#","Aussage","Begründung im Gespräch","Fundstelle","Gewicht"],"zeilen":kern},
 baum,
 {"typ":"illu","id":"masterpeace_ebenen","titel":"Skizze: Wie gesteuert wird – drei Ebenen (Darstellung laut Regenauer, schematisch)"},
 {"typ":"illu","id":"masterpeace_institutionen","titel":"Skizze: Institutionen und Dokumente, die im Gespräch vorkommen – Gründungs- und Erscheinungsjahre (belegte Daten)"},
 {"typ":"tabelle","kopf":["🧭 Steckbrief",""],"schmal":True,"zeilen":[
  ["**Thema in einem Satz**","Wer die Welt aus Regenauers Sicht steuert – Zentralbanken, UN, Empire – und was der Einzelne tun kann."],
  ["**Titel**",f"{TITEL} – Produktion von Masterpeace, hochgeladen auf dem YouTube-Kanal {GAST}"],
  ["**Format**","Video-Interview, frei gesprochen; eingeblendete Spendenaufrufe von Masterpeace [0:19], [0:57]; keine Werbeblöcke"],
  ["**Sprecher**","👤 **Tom-Oliver Regenauer** – Gast, Autor · 🎙️ **Gastgeber** von Masterpeace – Name im Video nicht genannt ❓; spricht selbst längere Passagen (u. a. [0:06–0:08], [0:11–0:13], [0:29–0:31], [0:39–0:44], [0:48])"],
  ["**Dauer**","58 Min. (58:04)"],
  ["**Datum**","Veröffentlichung nicht ermittelt (2024 ❓); aufgenommen vermutlich zwischen 26.07. und 22.09.2024 📚"],
  ["**Grundton**","ruhig, zustimmend; der Gastgeber teilt die Grundsicht, widerspricht nur einmal ausdrücklich [0:29]"],
  ["**Hinweis**","Aussagen beider Sprecher sind als ihre Sicht wiedergegeben; daneben steht im Abgleich, was Quellen belegen. Aussagen zu Judentum, Zionismus und Israel sind wörtlich nah und mit Sprecher wiedergegeben."]]},
]

# ---------- Reiter 2: Gespräch im Detail ----------
detail = [{"typ":"text","text":f"🔎 Detaillierte Auswertung in der Reihenfolge des Gesprächs – {NA} Abschnitte. Lesehilfe: 💬 Zitat, 📌 Aussage/Zahl/Beispiel, 🔗 Bezug, 📚 Ergänzung, ❓ unklar. Video: [{TITEL}]({URL})"},
 {"typ":"gespraech","titel":"🧭 Gesprächsverlauf – wann worüber gesprochen wird","dauer":"0:58","themen":THEMEN,"teile":teile}] + abschnitte

# ---------- Reiter 3: Zeitachse & Verzeichnisse ----------
Z = [
 ("932",932,"Graf Dietrich – laut Regenauer Ahnherr der Wettiner und heutiger Königshäuser","[0:33]",False),
 ("1600",1600,"Gründung der britischen Ostindien-Kompanie („seit 16…“)","[0:32]",True),
 ("1783",1783,"Großbritannien verliert die 13 Kolonien (Frieden von Paris)","[0:35]",True),
 ("1791",1791,"First Bank of the United States, Lizenz für 20 Jahre","[0:35]",False),
 ("1816",1816,"Second Bank of the United States gegründet","[0:35]",False),
 ("1832–1836",1832,"Andrew Jackson: Veto gegen Verlängerung, Charter der Second Bank endet 1836","[0:35], [0:42]",True),
 ("1884",1884,"Gründung der Fabian Society","[0:28]",True),
 ("1891",1891,"Kreis um Cecil Rhodes und Alfred Milner (Vorläufer des Round Table)","[0:31], [0:39]",True),
 ("1899–1902",1899,"Burenkrieg mit britischen Lagern (unter Kitchener)","[0:14]",True),
 ("Aug./Nov. 1914",1914,"Kriegsbeginn; britische Seeblockade, Nordsee im November zum Kriegsgebiet erklärt","[0:35]",True),
 ("02.11.1917",1917,"Balfour-Erklärung (Brief an Walter Rothschild)","[0:45]",True),
 ("1917",1917,"Britisches Königshaus Sachsen-Coburg und Gotha heißt fortan Windsor","[0:33]",False),
 ("1919",1919,"Versailler Vertrag; Foch: „Waffenstillstand für 20 Jahre“","[0:37], [0:44]",True),
 ("1919",1919,"„Technical Alliance“ gegründet","[0:18]",False),
 ("1920",1920,"Völkerbund nimmt Arbeit auf","[0:32], [0:46]",True),
 ("1922",1922,"Völkerbund-Mandat für Palästina an Großbritannien","[0:45]",True),
 ("1930",1930,"Gründung der BIZ in Basel (Haager Konferenz, Young-Plan)","[0:04], [0:38]",True),
 ("1933",1933,"„Technocracy Inc.“","[0:18]",False),
 ("1939",1939,"Zweiter Weltkrieg – „ziemlich genau 20 Jahre später“","[0:44]",True),
 ("1945",1945,"Gründung der UN mit 51 Mitgliedern","[0:46]",True),
 ("1946",1946,"Julian Huxley: „UNESCO – its purpose and its philosophy“","[0:15]",False),
 ("1947",1947,"UN-Teilungsplan für Palästina (Resolution 181)","[0:45]",True),
 ("1948",1948,"Unabhängigkeitserklärung Israels","[0:45], [0:48]",True),
 ("1971",1971,"Ende der Goldbindung des Dollars","[0:41]",True),
 ("21.03.2000",2000,"UN-Bericht „Replacement Migration“ (im Gespräch: 2003)","[0:10]",True),
 ("11.09.2001",2001,"Anschläge vom 11. September","[0:07]",False),
 ("2005",2005,"Internationale Gesundheitsvorschriften (IHR 2005)","[0:05]",True),
 ("2008",2008,"Rothkopf: „Superclass“ (im Gespräch: 2009); Finanzkrise","[0:03], [0:47]",True),
 ("06/2014",2014,"Nick Hanauer: „The Pitchforks Are Coming“","[0:28]",True),
 ("03.06.2020",2020,"Prince of Wales und Klaus Schwab starten den „Great Reset“","[0:32]",True),
 ("06/2020",2020,"Start der Corona-Warn-App","[0:20]",True),
 ("11/2020",2020,"NATO-ACT-Studie „Cognitive Warfare“ (Human Domain)","[0:13]",True),
 ("12/2022",2022,"Japan: Fünfjahresplan 43 Bio. Yen Verteidigung (2023–2027)","[0:40]",True),
 ("02/2024",2024,"Bukele auf der CPAC über Steuern und Geld","[0:41]",False),
 ("26.07.2024",2024,"Eröffnungsfeier der Olympischen Spiele in Paris","[0:11]",True),
 ("22.09.2024",2024,"UN-Generalversammlung nimmt den „Pakt für die Zukunft“ an","[0:46]",True),
 ("19.09.2025",2025,"Geänderte Gesundheitsvorschriften (IHR) treten in Kraft","[0:05]",True),
]
Z.sort(key=lambda e: e[1])
zeitachse = {"typ":"zeitachse","titel":"📅 Zeitachse – Ereignisse, die im Gespräch vorkommen","eintraege":[{"z":z,"j":j,"t":t,"f":f,"e":e} for z,j,t,f,e in Z]}
personen = [
 ["Tom-Oliver Regenauer","Autor, früher Musiker und Manager; lebt laut Gastgeber seit rund 15 Jahren in der Schweiz","Gast","[0:02], [0:51]"],
 ["Gastgeber (Masterpeace)","Name im Video nicht genannt ❓; schreibt laut eigener Aussage selbst Bücher","Fragen, eigene längere Thesen","durchgehend"],
 ["David Rothkopf","Autor von „Superclass“ (2008)","Liste der globalen Machtelite","[0:03], [0:31]"],
 ["Ernst Wolff","Publizist, früherer Masterpeace-Gast","spricht oft über die BIZ","[0:04], [0:06], [0:38]"],
 ["Daniele Ganser","Historiker, früherer Masterpeace-Gast","9/11","[0:07]"],
 ["Jonas Tögel","Propagandaforscher, früherer Masterpeace-Gast","NATO und „sechste Dimension“","[0:13]"],
 ["Julian Huxley","Biologe, erster Generaldirektor der UNESCO","Schrift von 1946","[0:15]"],
 ["Aldous Huxley","Schriftsteller, „Schöne neue Welt“","Kastenwelt, Vergleich mit Orwell","[0:15–0:18]"],
 ["George Orwell","Schriftsteller","Überwachungsstaat","[0:17]"],
 ["George Bernard Shaw · Bertrand Russell · Margaret Sanger","im Gespräch als Eugeniker genannt","britische Eugenik-Bewegung","[0:13]"],
 ["Elon Musk · Ray Kurzweil","Unternehmer · Futurist","biodigitale Konvergenz","[0:14], [0:16]"],
 ["Nick Hanauer","US-Investor (früh bei Amazon)","„Mistgabeln“","[0:28]"],
 ["Tony Blair · Bill Clinton · Angela Merkel","Regierungschefs","„Dritter Weg“, Politik der Mitte","[0:29]"],
 ["Cecil Rhodes · Alfred Milner","britische Imperialpolitiker","Round Table, Empire, Versailles","[0:14], [0:31], [0:34], [0:37]"],
 ["Edward Mandell House · Alfred Zimmern","Berater Wilsons · britischer Völkerbund-Vordenker","Völkerbund und UN","[0:31–0:32], [0:37]"],
 ["King Charles III","britischer König","Commonwealth, Great Reset","[0:32], [0:36]"],
 ["Klaus Schwab","WEF-Gründer","Great Reset","[0:32]"],
 ["Winston Churchill · Jan Smuts","britischer Politiker · südafrikanischer Politiker","Vorgeschichte des Ersten Weltkriegs","[0:34–0:35]"],
 ["Andrew Jackson","US-Präsident","beendete die Second Bank","[0:35], [0:42]"],
 ["Rothschild (Familie)","Bankiers","Bank of England, Balfour-Erklärung","[0:38], [0:48]"],
 ["Nayib Bukele","Präsident von El Salvador","Zitat zu Steuern","[0:41]"],
 ["Ferdinand Foch","französischer Marschall","„Waffenstillstand für 20 Jahre“","[0:44]"],
 ["Theodor Herzl","Begründer des politischen Zionismus","Schriften","[0:49–0:50]"],
 ["Joe Biden · Donald Trump","US-Präsidenten","Bekenntnis zum Zionismus (Gastgeber)","[0:48]"],
]
orte = [
 ["Basel","Sitz der BIZ","[0:04]"],["Bohemian Grove (Kalifornien)","Clubtreffen; Regenauer war dort","[0:08–0:10]"],
 ["Paris","Olympia-Eröffnung 2024","[0:11]"],["Ukraine","Diia-App, „Technokratie 2.0“","[0:20–0:23]"],["Estland","Ausrollen der App","[0:23]"],
 ["China","„Technokratie 1.0“, Taiwan","[0:18], [0:22], [0:43]"],["Washington","Präsidentenmacht, Panels zur App","[0:07], [0:23]"],
 ["Großbritannien / City of London","Empire, Krone, Finanzplatz","[0:31–0:38]"],["Kanada · Australien","Realms unter der Krone","[0:32]"],
 ["Japan · Australien · Taiwan","Aufrüstung gegen China","[0:40], [0:43]"],["Palästina / Israel / Gaza","Balfour, Staat Israel, Regenauers Aufenthalte","[0:45], [0:48–0:51]"],
 ["Schweiz","Wohnort Regenauers","[0:51]"],
]
begriffe = [
 ["BIZ (Bank für Internationalen Zahlungsausgleich)","1930 gegründete Bank der Zentralbanken in Basel","[0:04], [0:38]"],
 ["Internationale Gesundheitsvorschriften (IHR)","Regelwerk der WHO für Gesundheitsnotlagen; 196 Vertragsstaaten","[0:05]"],
 ["Pandemievertrag","WHO-Abkommen zur Pandemievorsorge; laut Regenauer Ablenkung","[0:04–0:05]"],
 ["Global Governance","Steuerung über supranationale Institutionen","[0:10], [0:46]"],
 ["SDGs / Nachhaltigkeitsziele","17 UN-Ziele der Agenda 2030","[0:09]"],
 ["Replacement Migration","UN-Bericht (2000) über Zuwanderungsszenarien","[0:10]"],
 ["Transhumanismus / „Transenhumanismus“","Verbesserung des Menschen durch Technik; zweites ist eine Wortschöpfung des Gastgebers","[0:11], [0:13]"],
 ["Eugenik","Lehre von der „Verbesserung“ des Erbguts","[0:13–0:17]"],
 ["Biodigitale Konvergenz","Verschmelzung von Biologie und Digitaltechnik","[0:14], [0:16]"],
 ["Technokratie","Herrschaft nach technischen Kriterien; Technical Alliance 1919, Technocracy Inc. 1933","[0:18]"],
 ["Bluetooth Low Energy","energiesparender Funkstandard; Grundlage der Kontaktmessung der Corona-Warn-App","[0:20]"],
 ["Diia","ukrainische Staats-App und Portal („State in a Smartphone“)","[0:20–0:23]"],
 ["Geofencing","digitale Ortsgrenze, an die Funktionen gebunden sind","[0:21]"],
 ["CBDC","digitales Zentralbankgeld","[0:24]"],
 ["15-Minuten-Stadt","Stadtplanung mit kurzen Wegen","[0:24]"],
 ["Dritter Weg","Politik der Mitte zwischen Markt und Sozialstaat (Blair, Clinton)","[0:28]"],
 ["Commonwealth / Realm","Staatenbund von 56 Ländern / Staat mit dem britischen Monarchen als Staatsoberhaupt","[0:32]"],
 ["Pluralismussimulation","Regenauers Wort für Wahlen ohne echte Auswahl („election vs. selection“)","[0:00], [0:41], [0:47]"],
 ["Pakt für die Zukunft","UN-Resolution vom 22.09.2024 mit 56 „Actions“","[0:46]"],
 ["Zionismus","Bewegung für einen jüdischen Staat; für Regenauer ein Herrschaftsmodell","[0:48–0:51]"],
]
zahlen = [
 ["„Superclass“","6.000 damals, heute ~7.000 Menschen","[0:03]"],["UN-Unterorganisationen","„72 plus“","[0:16]"],
 ["Smartphones mit iOS oder Android","98 % der Bevölkerung","[0:20]"],["Diia","„100 plus“ Funktionen, 70 % haben sie geladen","[0:20–0:21]"],
 ["CO2-Budget (Tagesschau)","1,5 t pro Kopf","[0:21]"],["Bewegungsradius","„15 m“","[0:21]"],["Zeitkonto","1 Stunde = 20 €","[0:25]"],
 ["Datenversand eines Smartphones","„12 MB“ pro Nacht","[0:25]"],["Extremisten","10–20 % auf beiden Seiten","[0:49]"],
 ["Commonwealth","56 Staaten, 29,4 % der Weltbevölkerung, 15 unter der Krone","[0:32]"],["Machtstruktur","250–300 Jahre alt (Gastgeber)","[0:30]"],
 ["BIZ-Generalversammlung","63 Zentralbanken","[0:38]"],["First Bank","80 % im Besitz der Bank of England (laut Regenauer)","[0:39]"],
 ["Japan Rüstung","„300 Milliarden pro Jahr“, „Platz 3“ (Gastgeber)","[0:40]"],
 ["Staatsschulden Deutschland","Tilgung bis 2230 bei 1 Mrd./Monat; 24–25.000 € pro Kopf","[0:42]"],
 ["Finanzblase","„hundertfach“ größer als 2008","[0:47]"],["Nachrichtenkonsum Regenauer","15–20 Min. am Tag","[0:53]"],
]
zeit = [zeitachse,
 {"typ":"tabelle","kopf":["👤 Person","Wer / was","Rolle im Gespräch","Fundstelle"],"zeilen":personen},
 {"typ":"tabelle","kopf":["🗺️ Ort","Rolle","Fundstelle"],"zeilen":orte},
 {"typ":"tabelle","kopf":["📖 Begriff","Erklärung","Fundstelle"],"zeilen":begriffe},
 {"typ":"tabelle","kopf":["📊 Zahl im Gespräch","Angabe","Fundstelle"],"zeilen":zahlen}]

# ---------- Reiter 4: Abgleich & Daten ----------
abg = [
 ["UN als Steuerzentrale; mit dem Pakt für die Zukunft erhalte sie „deutlich mehr Machtbefugnis“ und erstmals werde über ein globales Steuermodell gesprochen; niemand wähle UN-Vertreter [0:05–0:06], [0:46–0:47]",
  "Die UN hat 193 Mitgliedstaaten (seit 2011). Der Pakt wurde am 22.09.2024 als Resolution der Generalversammlung angenommen (A/RES/79/1), mit Anhängen Globaler Digitaler Pakt und Erklärung zu künftigen Generationen. Zu Steuern sagt er (Action 4): internationale Steuerkooperation fördern, sich „konstruktiv“ am Prozess zu einer UN-Rahmenkonvention über internationale Steuerkooperation beteiligen und Optionen zur Besteuerung sehr vermögender Personen „in den geeigneten Foren“ prüfen. Eine von der UN selbst erhobene Steuer sieht der Text nicht vor. Für „komplexe globale Schocks“ (Action 54) soll der Generalsekretär Ansätze prüfen – „innerhalb bestehender Befugnisse“ und in Absprache mit den Mitgliedstaaten.",
  Q['pakt']+" · "+Q['paktpga']+" · "+Q['unmit']],
 ["Die Internationalen Gesundheitsvorschriften seien schon bindend; in der Corona-Krise hätten WHO-Vorgaben nationales Recht ausgehebelt [0:04–0:05]",
  "Die IHR gelten für 196 Vertragsstaaten. Die 2024 im Konsens beschlossenen Änderungen (neue Warnstufe „Pandemic Emergency“) traten am 19.09.2025 in Kraft; 11 Staaten lehnten sie ab, für sie gilt die alte Fassung. Die WHO schreibt: Staaten haben das souveräne Recht, Gesundheitsgesetze zu erlassen; die WHO sei Sekretariat „ohne Befugnis, Staaten zum Handeln zu zwingen“. Lockdowns wurden in Deutschland durch Bundes- und Landesrecht angeordnet 📚.",
  Q['ihr']],
 ["BIZ in Basel als Spitze eines „Zentralbankenkartells“ [0:04], [0:38]; Gastgeber: Die BIZ sei geschaffen worden, um „das Geld der Juden beiseite zu schaffen“ [0:06]",
  "Die BIZ wurde 1930 gegründet (Abkommen der Haager Konferenz vom 20.01.1930) im Zusammenhang mit dem Young-Plan: Sie übernahm Einzug, Verwaltung und Verteilung der deutschen Reparationszahlungen und sollte die Zusammenarbeit der Zentralbanken fördern; heute gehören ihr 63 Zentralbanken an. Ein Gründungszweck, wie ihn der Gastgeber nennt, steht in der Darstellung der BIZ nicht. Die Bundeszentrale für politische Bildung beschreibt es als Merkmal von strukturellem Antisemitismus, wenn komplexe wirtschaftliche Zusammenhänge vereinfacht und einer kleinen (geheimen) Personengruppe mit böswilliger Absicht zugeschrieben werden.",
  Q['biz']+" · "+Q['bpb']],
 ["UN-Dokument „Replacement Migration“ von „2003“: wie viele Millionen Menschen wann wo einwandern sollen [0:10]",
  "Der Bericht der UN-Bevölkerungsabteilung ist auf den 21.03.2000 datiert. Er rechnet für acht Länder (u. a. Deutschland, Frankreich, USA) und zwei Regionen für 1995–2050 Szenarien durch: wie viel Zuwanderung nötig wäre, um Bevölkerungszahl, Erwerbsbevölkerung oder das Verhältnis von Erwerbstätigen zu Älteren zu halten. Der Titel ist als Frage formuliert („Is It a Solution …?“); es sind Rechenszenarien, keine Vorgaben.",
  Q['repl']+" · "+Q['repl2']],
 ["UNESCO-Gründungsdokument 1946 (Julian Huxley): Dutzende Male „Eugenik“; S. 21: Undenkbares wieder denkbar machen [0:15]",
  "Belegt: In „UNESCO – its purpose and its philosophy“ (1946) schreibt Huxley auf S. 21, eine radikale Eugenik-Politik sei „für viele Jahre politisch und psychologisch unmöglich“, die UNESCO solle aber darauf achten, dass das „eugenische Problem“ sorgfältig geprüft und die Öffentlichkeit informiert werde, „so that much that now is unthinkable may at least become thinkable“. Im selben Abschnitt nennt er die Bewahrung menschlicher Vielfalt als eines von zwei Hauptzielen der Eugenik. Das Wort kommt im Text mindestens rund ein Dutzend Mal vor. Es war Huxleys Schrift, nicht die UNESCO-Verfassung.",
  Q['huxley']],
 ["Gastgeber: Laut Tögel unterstütze die NATO die „Atomisierung“; auf der Seite des NATO Innovation Hub heiße das „sechste Dimension der Kriegsführung“ [0:13]",
  "Eine von NATO Allied Command Transformation geförderte Studie (François du Cluzel, November 2020) schlägt die „Human Domain“ als „sixth operational domain“ vor und beschreibt das Gehirn als Schauplatz kognitiver Kriegsführung. Laut Vorbemerkung geben die Inhalte die Diskussionen des Innovation Hub wieder, nicht die Position von ACT oder der Mitgliedstaaten. Ob dort eine „Atomisierung“ als Ziel steht, wurde hier nicht geprüft ❓.",
  Q['nato']],
 ["Alle Smartphones funken per Bluetooth Low Energy, auch wenn man es abschaltet; darüber lief die Corona-Warn-App, die eine nicht einsehbare Schnittstelle auslese [0:20]",
  "Die Corona-Warn-App nutzte das Exposure Notification Framework von Apple und Google über Bluetooth Low Energy: Geräte senden zeitweise wechselnde Kennungen aus, die täglich neu aus einem Schlüssel abgeleitet werden; die Risikoberechnung läuft auf dem Gerät, Begegnungsdaten bleiben laut Dokumentation auf dem Telefon. Der Quellcode und die Architektur sind öffentlich dokumentiert. Ob BLE nach dem Abschalten weiter sendet, ist in dieser Quelle nicht behandelt ❓.",
  Q['cwa']],
 ["98 % der Bevölkerung nutzen iOS oder Android [0:20]",
  "Laut StatCounter entfielen 2024 in Deutschland 65,0 % der mobilen Seitenaufrufe auf Android und 34,1 % auf iOS, zusammen 99,1 % (weltweit 71,7 % + 27,9 %). Gemessen werden Seitenaufrufe, nicht Personen.",
  Q['stat']],
 ["Ukraine: Diia-App „State in the Smartphone“ mit über 100 Funktionen; 70 % haben sie geladen; Pilot für die EU [0:20–0:23]",
  "Die ukrainische Regierung verwendet selbst den Slogan „State in a Smartphone“; im Januar 2024 nutzten laut ihr über 20 Mio. Menschen Diia („jeder zweite“), mit 14 digitalen Dokumenten und über 30 Diensten in der App. Die Rechnungskammer der Ukraine zählte 2024 über 18,5 Mio. App-Nutzer und 209 Dienste im Gesamtsystem (Portal und App). Ein Beschluss, Diia in Estland oder der EU einzuführen, wurde hier nicht gefunden ❓.",
  Q['diia']+" · "+Q['diiarp']],
 ["CO2-Budget von 1,5 t pro Kopf laut Tagesschau – damit müsste man „obdachlos sein als Veganer“ [0:21]",
  "Laut Umweltbundesamt liegt der Treibhausgas-Ausstoß pro Person in Deutschland derzeit bei 10,3 t CO2e im Jahr (inkl. Im- und Export); klimaverträglich wären „deutlich unter 1 t“, also eine Minderung um über 90 %. Ein verbindliches persönliches CO2-Budget gibt es in Deutschland nicht 📚. Die genannte Tagesschau-Stelle wurde nicht gefunden ❓.",
  Q['uba']],
 ["Die Sozialdemokratie beruhe auf dem Konzept der Fabian Society für einen „dritten Weg“; dieselben Leute hätten die Eugenik entwickelt [0:28]",
  "Die Fabian Society wurde am 04.01.1884 gegründet, beteiligte sich 1900 an der Gründung der Labour Party und ist ihr bis heute angeschlossen. Dass der „Dritte Weg“ der 1990er-Jahre (Blair, Clinton) auf ein Fabian-Konzept zurückgeht, ist in dieser Quelle nicht belegt ❓. Mehrere frühe Fabians (u. a. G. B. Shaw) vertraten eugenische Ideen 📚.",
  Q['fabian']],
 ["Commonwealth: 56 Staaten, „29,4 %“ der Weltbevölkerung (2024), 15 unter der Krone; niemand werde dort Premierminister ohne Unterschrift von King Charles [0:32]",
  "Das Commonwealth hat 56 Mitglieder mit rund 2,7 Mrd. Menschen; der König ist „Head of the Commonwealth“, laut Sekretariat eine vor allem symbolische Rolle, die nicht erblich ist. Staatsoberhaupt ist der Monarch in 15 Ländern (Vereinigtes Königreich und 14 Realms); laut CFR sind seine Befugnisse „weitgehend symbolisch“, wichtigste formale Aufgabe ist die Bestätigung neuer Regierungen, außerhalb Großbritanniens über Generalgouverneure. Bei rund 8 Mrd. Weltbevölkerung entsprächen 2,7 Mrd. etwa einem Drittel 📚.",
  Q['cw']+" · "+Q['cfr']],
 ["Den Great Reset habe nicht Schwab, sondern zuerst Charles verkündet [0:32]",
  "Übereinstimmend: Die Initiative „The Great Reset“ wurde am 03.06.2020 vom damaligen Prince of Wales und von Klaus Schwab (WEF) vorgestellt; UN-Generalsekretär Guterres und IWF-Chefin Georgieva gaben Stellungnahmen ab.",
  Q['wef']],
 ["Die Briten hätten den Ersten Weltkrieg ausgelöst: Ihre Seeblockade habe Deutschland ausgehungert, die Kaiserliche Marine habe reagieren müssen [0:35]",
  "Der Krieg zwischen Großbritannien und Deutschland begann im August 1914; die britische Seeblockade setzte nach Kriegsausbruch ein, Anfang November 1914 wurde die Nordsee zum Kriegsgebiet erklärt. Die Blockade dauerte bis 1919; das Reichsgesundheitsamt bezifferte die zivilen Todesopfer durch Hunger und Krankheiten bis Dezember 1918 auf 763.000, eine Studie von 1928 auf 424.000. In der gängigen Darstellung war die Blockade eine Folge, nicht der Auslöser des Krieges.",
  Q['blockade']],
 ["Gastgeber: Japan rüste auf, nun „Platz 3 nach China“ mit „300 Milliarden pro Jahr“ [0:40]",
  "SIPRI: Japan gab 2023 50,2 Mrd. US-$ für Militär aus (+11 %, stärkster Anstieg seit 1972) und lag auf Platz 10; China auf Platz 2 mit geschätzt 296 Mrd. US-$. Rund 300 Mrd. US-$ sind Japans Ziel für fünf Jahre: 43 Bio. Yen (≈ 318 Mrd. US-$) für 2023–2027, beschlossen im Dezember 2022.",
  Q['sipri']+" · "+Q['japan']],
 ["Bukele (CPAC, „Februar 22“): Bürger zahlten hohe Steuern nur, um die Illusion zu erhalten, den Staat zu finanzieren [0:41]",
  "Übereinstimmend: Bukele sagte auf der CPAC im Februar 2024, Amerikaner zahlten hohe Steuern „only to uphold the illusion that you are funding the government, which you are not“; der Staat finanziere sich über Anleihen, die zum großen Teil die Fed mit neu geschaffenem Geld kaufe. Es ist seine Deutung, keine amtliche Darstellung.",
  Q['bukele']],
 ["Deutschland wäre bei 1 Mrd. € Tilgung pro Monat erst um 2230 schuldenfrei (Bund der Steuerzahler); pro Kopf „24, 25.000“ € Schulden, „neuer Rekord“ [0:42]",
  "Der Bund der Steuerzahler nannte im Januar 2024 rund 2.500 Mrd. € Staatsschulden und 3.393 € Neuverschuldung pro Sekunde für 2024. Rechnerisch dauerte die Tilgung von 2.500 Mrd. € bei 12 Mrd. € im Jahr rund 208 Jahre, also bis etwa 2232 (ohne Zinsen, eigene Rechnung 📚). Destatis: Ende 2023 war der Öffentliche Gesamthaushalt mit 2.445,1 Mrd. € verschuldet, 28.943 € je Einwohner. Nach Maastricht-Abgrenzung (Eurostat) 2024: 2.694 Mrd. €, 61,4 % des BIP.",
  Q['bdst']+" · "+Q['destatis']+" · "+Q['eurostat']],
 ["Palästina sei den Arabern versprochen, dann über die Balfour-Erklärung „aus den Finanzeliten“ dem jüdischen Volk zugesprochen worden; Herzls Schriften enthielten „faschistoides Zeug“, zionistische Dokumente sprächen von Kolonialisierung [0:45], [0:49–0:50]",
  "Die Balfour-Erklärung vom 02.11.1917 war ein Brief des Außenministers Arthur Balfour an Walter Rothschild, der sie den zionistischen Kreisen übermitteln sollte: Die Regierung sehe eine „national home for the Jewish people“ in Palästina mit Wohlwollen, ohne die bürgerlichen und religiösen Rechte der nichtjüdischen Gemeinschaften zu beeinträchtigen. Das Völkerbund-Mandat von 1922 übernahm die Erklärung; 1947 schlug die UN die Teilung vor, 1948 erklärte Israel seine Unabhängigkeit. Britische Zusagen an arabische Führer (McMahon-Hussein-Korrespondenz 1915/16) werden dort nicht behandelt ❓. Welche Herzl-Texte und Dokumente gemeint sind, sagt Regenauer nicht; hier nicht geprüft ❓.",
  Q['balfour']+" · "+Q['palest']],
]

kurs_schulden = {"typ":"kurs","id":"masterpeace-schulden","titel":"📈 Staatsverschuldung Deutschlands (Maastricht-Abgrenzung)",
 "reihen":[
  {"name":"Schuldenstand des Staates","kurz":"Mrd. €","einheit":"Mrd. €","dez":0,"hoeherGut":False,"punkte":[]},
  {"name":"Schuldenquote","kurz":"% BIP","einheit":"%","dez":1,"hoeherGut":False,"punkte":[]}],
 "hoeherGut":False,"vergleich":False,
 "quelle":Q['eurostat']+" (gov_10dd_edpt1, Sektor Staat, abgerufen über die Eurostat-Schnittstelle), Stand 21.10.2026",
 "hinweis":"Bezug zum Gespräch [0:42]: Tilgung „bis 2230“, „neuer Rekord“. Maastricht-Abgrenzung (Bund, Länder, Gemeinden, Sozialversicherung); Destatis weist für den Öffentlichen Gesamthaushalt etwas andere Werte aus (2023: 2.445,1 Mrd. €, 28.943 € je Einwohner)."}
mio = {2000:1261584.7,2001:1274759.0,2002:1330083.1,2003:1419426.0,2004:1489670.9,2005:1561020.5,2006:1610903.7,2007:1619064.6,2008:1687442.0,2009:1804696.0,2010:2119241.8,2011:2155875.7,2012:2234802.5,2013:2220281.0,2014:2224559.5,2015:2197473.8,2016:2182375.0,2017:2132783.9,2018:2086432.0,2019:2075789.9,2020:2347992.2,2021:2501742.5,2022:2569654.6,2023:2630764.7,2024:2694319.5,2025:2845970.1}
pc = {2000:59.2,2001:58.1,2002:59.8,2003:63.3,2004:65.0,2005:67.1,2006:66.4,2007:63.7,2008:65.2,2009:72.4,2010:81.0,2011:78.5,2012:79.8,2013:77.4,2014:74.4,2015:71.0,2016:68.1,2017:63.7,2018:60.5,2019:58.3,2020:67.5,2021:67.4,2022:64.1,2023:61.8,2024:61.4,2025:62.8}
kurs_schulden["reihen"][0]["punkte"] = [[y, round(v/1000)] for y,v in sorted(mio.items())]
kurs_schulden["reihen"][1]["punkte"] = [[y, v] for y,v in sorted(pc.items())]

un = [(1945,51),(1946,55),(1947,57),(1948,58),(1949,59),(1950,60),(1955,76),(1956,80),(1957,82),(1958,82),(1960,99),(1961,104),(1962,110),(1963,113),(1964,115),(1965,117),(1966,122),(1967,123),(1968,126),(1970,127),(1971,132),(1973,135),(1974,138),(1975,144),(1976,147),(1977,149),(1978,151),(1979,152),(1980,154),(1981,157),(1983,158),(1984,159),(1990,159),(1991,166),(1992,179),(1993,184),(1994,185),(1999,188),(2000,189),(2002,191),(2006,192),(2011,193)]
kurs_un = {"typ":"kurs","id":"masterpeace-unmitglieder","titel":"📈 Mitgliedstaaten der Vereinten Nationen","reihen":[
  {"name":"UN-Mitgliedstaaten","kurz":"Staaten","einheit":"Staaten","dez":0,"hoeherGut":None,"punkte":[[y,v] for y,v in un]}],
 "hoeherGut":None,"vergleich":False,"quelle":Q['unmit']+", Stand 2011 (seitdem unverändert 193)",
 "hinweis":"Bezug zum Gespräch [0:05–0:06], [0:46]: UN als „Verordnungskonstrukt“ über den Nationalstaaten. Die Sprünge 1955, 1960 und 1991–1993 gehen auf Dekolonisierung und das Ende der Sowjetunion und Jugoslawiens zurück 📚."}

os_de = {2015:(68.01,28.46),2016:(67.47,29.31),2017:(67.7,30.28),2018:(68.07,30.66),2019:(70.95,28.21),2020:(68.98,30.4),2021:(63.24,35.66),2022:(59.79,37.68),2023:(60.08,38.95),2024:(65.02,34.05),2025:(62.09,37.02)}
kurs_os = {"typ":"kurs","id":"masterpeace-smartphone","titel":"📈 Mobile Betriebssysteme in Deutschland – Anteil an Seitenaufrufen","reihen":[
  {"name":"Android","kurz":"Android","einheit":"%","dez":1,"hoeherGut":None,"punkte":[[y,a] for y,(a,i) in sorted(os_de.items())]},
  {"name":"iOS","kurz":"iOS","einheit":"%","dez":1,"hoeherGut":None,"punkte":[[y,i] for y,(a,i) in sorted(os_de.items())]}],
 "hoeherGut":None,"vergleich":False,"quelle":Q['stat']+" (Jahreswerte, CSV-Export), abgerufen 12.11.2026",
 "hinweis":"Bezug zum Gespräch [0:20]: „98 % … iOS … oder Android“. 2024 zusammen 99,1 %. Gemessen werden Seitenaufrufe mobiler Geräte, nicht Nutzerzahlen."}

balken_sipri = {"typ":"balken","titel":"📊 Militärausgaben 2023 – die zehn größten (Mrd. US-$)","einheit":"Mrd. US-$","dez":1,
 "zeilen":[["USA",916],["China (geschätzt)",296],["Russland (geschätzt)",109],["Indien",83.6],["Saudi-Arabien (geschätzt)",75.8],["Vereinigtes Königreich",74.9],["Deutschland",66.8],["Ukraine",64.8],["Frankreich",61.3],["Japan",50.2]],
 "quelle":Q['sipri']+", Stand April 2024 (laufende Preise und Wechselkurse)",
 "hinweis":"Bezug zum Gespräch [0:40]: Der Gastgeber nennt für Japan „Platz 3“ und „300 Milliarden pro Jahr“. Japans Fünfjahresplan 2023–2027 umfasst 43 Bio. Yen (≈ 318 Mrd. US-$) insgesamt."}

vergleich = {"typ":"vergleich","titel":"⚖️ Zahlen im Gespräch und Daten nebeneinander","la":"Im Gespräch genannt","lb":"Daten laut Quelle","zeilen":[
 {"n":"Mitglieder der „Superclass“ laut Rothkopf","a":6000,"b":6000,"einheit":"Personen","f":"[0:03]","q":Q['superclass']},
 {"n":"Anteil iOS + Android (Deutschland, 2024)","a":98,"b":99.1,"einheit":"%","f":"[0:20]","q":Q['stat']},
 {"n":"Mitgliedstaaten des Commonwealth","a":56,"b":56,"einheit":"Staaten","f":"[0:32]","q":Q['cw']},
 {"n":"Staaten mit dem britischen Monarchen als Staatsoberhaupt","a":15,"b":15,"einheit":"Staaten","f":"[0:32]","q":Q['cfr']},
 {"n":"Zentralbanken in der BIZ","a":63,"b":63,"einheit":"Zentralbanken","f":"[0:38]","q":Q['biz']},
 {"n":"Militärausgaben Japans pro Jahr (2023)","a":300,"b":50.2,"einheit":"Mrd. US-$","f":"[0:40]","q":Q['sipri']},
 {"n":"Staatsschulden je Einwohner (Ende 2023, Öffentlicher Gesamthaushalt)","a":24500,"b":28943,"einheit":"€","f":"[0:42]","q":Q['destatis']},
]}

abgleich = [
 {"typ":"text","text":"Neutraler Abgleich: links die Aussage im Gespräch, rechts die gängige Darstellung bzw. Daten mit Quelle. Die Bewertung bleibt dem Leser."},
 {"typ":"tabelle","kopf":["Aussage im Gespräch","Gängige Darstellung (Mainstream) / Daten 📚","Quelle"],"stapel":True,"zeilen":abg},
 kurs_schulden, kurs_un, kurs_os, balken_sipri, vergleich,
 {"typ":"abschnitt","titel":"🧩 Spannungen im Gespräch","liste":[
  "Der Gastgeber widerspricht nur einmal ausdrücklich: Revolutionen hätten durchaus etwas verändert (Entmachtung des Adels, Rechte für Knechte und Mägde seit der Weimarer Verfassung) [0:29–0:30].",
  "Regenauer hält die Vorstellung einer kleinen Verschwörergruppe im Hinterzimmer für naiv und nennt QAnon „Beschäftigungstherapie“ [0:31]; der Gastgeber fragt dagegen nach der „Spinne“ im Netz und einem „Komitee der 300“ [0:06], [0:30].",
  "Regenauer betont, er berichte nur, was sich belegen lasse, und lasse Clubs mangels Protokoll beiseite [0:10]; an anderen Stellen nennt er Zahlen und Zitate ohne Quelle (Churchill, Milner, 80 % der First Bank, 12 MB pro Nacht).",
  "Zur BIZ-Aussage des Gastgebers über „das Geld der Juden“ [0:06] und zur Frage nach einer „Rothschildverschwörung“ [0:48] äußert sich Regenauer nicht zustimmend; er verweist darauf, dass ihm Religion egal sei, und trennt Judentum, Israelis, Staat und Zionismus [0:45], [0:49–0:51].",
  "Regenauer lehnt Gewalt ab und empfiehlt friedlichen Protest und Boykott [0:29], [0:27] – zugleich beschreibt er das System als bewaffnet und skrupellos."]},
 {"typ":"abschnitt","titel":"💡 Was man mitnehmen kann","liste":[
  "Mehrere genannte Dokumente gibt es tatsächlich und sind frei lesbar: Huxleys UNESCO-Schrift (1946), der UN-Bericht „Replacement Migration“ (2000), der Pakt für die Zukunft (2024), die NATO-ACT-Studie zur kognitiven Kriegsführung (2020).",
  "Was sie enthalten, weicht teils von der Wiedergabe ab: Der UN-Bericht rechnet Szenarien, der Pakt sieht Steuerkooperation statt einer UN-Steuer vor, die NATO-Studie ist keine offizielle NATO-Position.",
  "Einige Zahlen stimmen genau (56 Commonwealth-Staaten, 15 Realms, 63 BIZ-Zentralbanken, Bukeles Satz, Great Reset 2020), andere nicht (Japan 300 Mrd. pro Jahr, Ursache des Ersten Weltkriegs, „2003“).",
  "Zu Smartphones: Dass Telefone im Leerlauf regelmäßig Daten an Hersteller senden, ist gemessen – in kleinerem Umfang als im Gespräch genannt (siehe Prüfstand).",
  "Wer die Auswege prüfen will: Zeitbanken, quelloffene Betriebssysteme und datensparsame Geräte gibt es; ihr Nutzen hängt vom eigenen Bedarf ab."]},
 {"typ":"abschnitt","titel":"❓ Offen","liste":[
  "Wer ist der Gastgeber von Masterpeace, und wann wurde das Video veröffentlicht?",
  "Welche Tagesschau-Sendung nannte 1,5 t CO2 pro Kopf [0:21]?",
  "Welche Schriften Herzls und welche „zionistischen Dokumente“ meint Regenauer [0:50]?",
  "Woher stammen das Churchill-Zitat („die Deutschen werden ihren Krieg bekommen“) und das Milner-Zitat [0:34], [0:39]?",
  "Belege für: Bank of England besaß 80 % der First Bank [0:39]; Briten finanzierten Japans Flotte [0:36]; Charles' „Business Council“ als Vorläufer von Club of Rome und WEF [0:33]; Manhattan-Projekt im Bohemian Grove vorbereitet [0:08].",
  "Wer ist „holg“, der über die „Olympier“ schreibe [0:06] (Hörfehler im Transkript)?"]},
 {"typ":"abschnitt","titel":"🔎 Weiter recherchieren","liste":[
  "Pakt für die Zukunft (A/RES/79/1), besonders Action 4 und 54; Stand der UN-Rahmenkonvention über internationale Steuerkooperation.",
  "IHR 2005 und Änderungen 2024: Wortlaut, Umsetzung in Deutschland.",
  "Julian Huxley, „UNESCO – its purpose and its philosophy“ (1946), S. 21 im Zusammenhang lesen.",
  "Leith (2021): Telemetrie von iOS und Android; Dokumentation der Corona-Warn-App.",
  "Rechnungskammer der Ukraine zu Diia (2025); Eurostat und Destatis zu Staatsschulden.",
  f"Zum Vergleich: Regenauers längeres Gespräch bei {{{{a:ungeskriptet-regenauer|Regenauer bei {{ungeskriptet}}}}}}; zu Geld und Kriegen {{{{w:geld|Geld}}}}, {{{{w:kriege|Kriege}}}}, {{{{a:ganser|Daniele Ganser}}}}."]},
]

reiter = [
 {"id":K,"titel":f"{G}: Überblick","bloecke":ueberblick},
 {"id":K+"ab","titel":f"{G}: Gespräch im Detail","bloecke":detail},
 {"id":K+"zeit","titel":f"{G}: Zeitachse & Verzeichnisse","bloecke":zeit},
 {"id":K+"abgleich","titel":f"{G}: Abgleich & Daten","bloecke":abgleich},
]

def link_teile(s):  # Markdown-Link -> [Titel, url]
    import re
    return [[m.group(1), m.group(2)] for m in re.finditer(r'\[([^\]]+)\]\((https?://[^)]+)\)', s)]

quellen = [[f"Video: {TITEL} – Masterpeace (YouTube)", URL]]
seen = {URL}
for v in Q.values():
    for t,u in link_teile(v):
        if u not in seen: seen.add(u); quellen.append([t,u])

out = {"k":K,"gast":GAST,"reiter":reiter,
 "folgen_zeile":[DATUM,f"{GAST} (Autor)",TITEL,"UN & Global Governance, BIZ, Eugenik/Transhumanismus, digitale Kontrolle, Empire & Weltkriege, Staatsschulden, Zionismus, Auswege","{{a:regenauer-masterpeace|hier: Masterpeace}}",f"[ansehen]({URL})"],
 "baum_ast":{"gruppe":"🏛️ Macht & Geschichte","t":"👤 Tom-Oliver Regenauer bei Masterpeace – UN, BIZ, Eugenik, digitale Kontrolle, Empire, Zionismus"},
 "neu":{"d":"2026-11-12","t":"Regenauer – Masterpeace-Gespräch","k":f"Wer steuert die Welt? Regenauer über UN, BIZ, Eugenik, digitale Kontrolle und Empire – {NA} Abschnitte, Abgleich mit Quellen, 5 Diagramme.","h":"#a-regenauer-masterpeace","art":"Video"},
 "quellen":quellen,
 "web":[["Tom-Oliver Regenauer – YouTube-Kanal","https://www.youtube.com/@tomregenauer"]]}

here = os.path.dirname(os.path.abspath(__file__))
json.dump(out, open(os.path.join(here,'folge.json'),'w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', NA, 'Abschnitte,', len(abg), 'Abgleich-Zeilen,', len(Z), 'Zeitachse,', len(quellen), 'Quellen')
