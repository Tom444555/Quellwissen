# -*- coding: utf-8 -*-
"""Erzeugt folge.json für Regenauer – „Bis 2030 Totale Kontrolle?“ (BENU Solutions), Kürzel kontrolle."""
import json, os
K = "kontrolle"; G = "Bis 2030"
URL = "https://www.youtube.com/watch?v=E4N_En0tbco"
TITEL = "Tom Regenauer: Bis 2030 Totale Kontrolle? E-ID, KI, Elon Musk & Palantir"
GAST = "Tom-Oliver Regenauer"
def L(t, u): return "[%s](%s)" % (t, u)

# ---------- geprüfte Quellen ----------
Q = dict(
 lanz=L("ZDFheute (12.01.2026): Zensur-Vorwurf – Günther verteidigt sich nach Aussagen bei „Lanz“", "https://www.zdfheute.de/politik/deutschland/daniel-guenther-zensur-kritik-markus-lanz-zdf-100.html"),
 merz=L("Anadolu (15.01.2026): Germany's Merz calls nuclear phaseout 'serious strategic mistake'", "https://aa.com.tr/en/europe/germanys-merz-calls-nuclear-phaseout-serious-strategic-mistake/3800545"),
 quigley=L("LibQuotes: Carroll Quigley – Tragedy and Hope (Zitat zu den zwei Parteien)", "https://libquotes.com/carroll-quigley/works/tragedy-and-hope"),
 bernays=L("Project Gutenberg: Edward Bernays – Propaganda (1928), Volltext", "https://gutenberg.org/files/78634/78634-h/78634-h.htm"),
 wilson=L("Project Gutenberg: Woodrow Wilson – The New Freedom (1913), Volltext", "https://gutenberg.org/cache/epub/14811/pg14811-images.html"),
 urteil=L("NYSDA (25.09.2024): California federal district court rules current water fluoridation levels pose unreasonable risk", "https://www.nysdental.org/news-publications/news/2024/09/25/california-federal-district-court-rules-current-water-fluoridation-levels-pose-unreasonable-risk-of-injury"),
 ntp=L("NTP/NIEHS: Fluoride – Monographie (21.08.2024)", "https://ntp.niehs.nih.gov/go/fluoride"),
 bfr=L("BfR: Für gesunde Zähne – Fluorid-Vorbeugung bei Säuglingen und Kleinkindern (Stellungnahme 015/2018)", "https://www.bfr.bund.de/cm/343/fuer-gesunde-zaehne-fluorid-vorbeugung-bei-saeuglingen-und-kleinkindern.pdf"),
 netzwerk=L("ZR (18.05.2021): Gemeinsame Empfehlung von Zahnärzten und Pädiatern zur Fluoriddosierung", "https://www.iww.de/zr/kinderzahnheilkunde/kariesprophylaxe-gemeinsame-empfehlung-von-zahnaerzten-und-paediatern-zur-fluoriddosierung-f137966"),
 cochrane=L("Cochrane (2019): Fluoride toothpastes of different concentrations for preventing dental caries", "https://cochranelibrary.com/cdsr/doi/10.1002/14651858.CD007868.pub3/information"),
 origins=L("Origins/Ohio State (2018): Toxic Treatment – Fluoride's Transformation from Industrial Waste to Public Health Miracle", "https://origins.osu.edu/article/toxic-treatment-fluorides-transformation-industrial-waste-public-health-miracle"),
 fwin=L("Wikipedia: Fabian Window", "https://en.wikipedia.org/wiki/Fabian_Window"),
 fabian=L("Wikipedia: Fabian Society", "https://en.wikipedia.org/wiki/Fabian_Society"),
 hess=L("Britannica: Moses Hess", "https://www.britannica.com/biography/Moses-Hess"),
 hessw=L("Wikipedia: Moses Hess", "https://en.wikipedia.org/wiki/Moses_Hess"),
 sanger=L("Wikipedia: Margaret Sanger", "https://en.wikipedia.org/wiki/Margaret_Sanger"),
 gates=L("Wikipedia: William H. Gates Sr.", "https://en.wikipedia.org/wiki/William_H._Gates_Sr."),
 russell=L("Wikipedia: Bertrand Russell (Werke)", "https://en.wikipedia.org/wiki/Bertrand_Russell"),
 guterres=L("Wikipedia: António Guterres", "https://en.wikipedia.org/wiki/Ant%C3%B3nio_Guterres"),
 huxley=L("Aeon (02.12.2024): Julian S. Huxley – the man who put eugenics into UNESCO", "https://aeon.co/essays/julian-s-huxley-the-man-who-put-eugenics-into-unesco"),
 trans=L("Wikipedia: Transhumanism", "https://en.wikipedia.org/wiki/Transhumanism"),
 jbs=L("Wikipedia: Journal of Biosocial Science", "https://en.wikipedia.org/wiki/Journal_of_Biosocial_Science"),
 rte=L("RTÉ (25.10.2025): Election result in numbers", "https://www.rte.ie/news/2025/1025/1540616-election-result-in-numbers"),
 rte2=L("RTÉ (01.11.2025): Analyse der ungültigen Stimmen", "https://www.rte.ie/news/analysis-and-comment/2025/1101/1541549-spoiled-votes-analysis"),
 iepres=L("presidentialelection.ie: Presidential Elections 1938–2025", "https://www.presidentialelection.ie/wp-content/uploads/2025/12/Presidential-Elections-1938-2025.pdf"),
 repl=L("UN Population Division: Replacement Migration – Executive Summary", "https://www.un.org/en/development/desa/population/publications/pdf/ageing/replacement-es.pdf"),
 bezahl=L("beck-aktuell (12.04.2024): Bezahlkarte für Asylbewerber vom Bundestag beschlossen", "https://www.beck-aktuell.de/heute-im-recht/rechtspolitik-gesetzgebung/bezahlkarte-fuer-asylbewerber-vom-bundestag-beschlossen-2024-04-12"),
 wand=L("Destatis: Wanderungen zwischen Deutschland und dem Ausland 1950–2025", "https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Bevoelkerung/Wanderungen/Tabellen/wanderungen-zwischen-deutschland-und-dem-ausland-jahr-02.html"),
 chall=L("Challenger, Gray & Christmas (06.11.2025): October Challenger Report – 153,074 Job Cuts", "https://www.challengergray.com/?p=27438"),
 insol=L("Destatis: Insolvenzen nach Jahren", "https://www.destatis.de/DE/Themen/Branchen-Unternehmen/Unternehmen/Gewerbemeldungen-Insolvenzen/Tabellen/lrins01.html"),
 insol25=L("Destatis (03/2026): Unternehmensinsolvenzen im Jahr 2025: +10,3 % zum Vorjahr", "https://www.destatis.de/DE/Presse/Pressemitteilungen/2026/03/PD26_085_52411.html"),
 dehst=L("DEHSt: nEHS – Festpreisphase 2021 bis 2025", "https://dehst.de/EN/Topics/nEHS/Sales-trade/sale-trade_node.html"),
 tehg=L("beck-aktuell (31.01.2025): Umfassende Reform des Emissionshandels beschlossen", "https://www.beck-aktuell.de/heute-im-recht/rechtspolitik-gesetzgebung/reform-emissionshandel-bundestagsbeschluss-eu-vorgaben-2025-01-31"),
 wef=L("WEF (10.09.2025): Finance Solutions for Nature – zehn priorisierte Modelle", "https://www.weforum.org/stories/2025/09/nature-finance-sustainable-investing-priority-models"),
 nac=L("TheCorporateCounsel.net (22.01.2024): NYSE Withdraws Natural Asset Company Listing Proposal", "https://www.thecorporatecounsel.net/blog/2024/01/nyse-withdraws-natural-asset-company-listing-proposal.html"),
 bis=L("BIZ (20.06.2023): BIS builds out „game-changing“ blueprint for the future monetary and financial system", "https://www.bis.org/press/p230620.htm"),
 carst=L("FXStreet: Bank of International Settlements chief talks „absolute control“", "https://www.fxstreet.com/amp/analysis/bank-of-international-settlements-chief-talks-absolute-control-202107122101"),
 gbf=L("CBD: Kunming-Montreal Global Biodiversity Framework – Target 3", "https://www.cbd.int/gbf/targets/3"),
 ndust=L("UC Berkeley News (03.08.2016): Sprinkling of neural dust opens door to electroceuticals", "https://news.berkeley.edu/2016/08/03/sprinkling-of-neural-dust-opens-door-to-electroceuticals/"),
 imfpanel=L("IWF-Jahrestagung (19.10.2020): Cross-Border Payments – A Vision for the Future", "https://meetings.imf.org/en/2020/annual/schedule/2020/10/19/imf-cross-border-payments-a-vision-for-the-future"),
 eudi=L("netzpolitik.org (10.03.2026): FAQ zur EUDI-Wallet", "https://netzpolitik.org/2026/faq-zur-eudi-wallet-die-wichtigsten-fragen-und-antworten-zur-digitalen-brieftasche/"),
 idat=L("Bundeskanzleramt Österreich (15.12.2025): ID Austria Servicetour – 900.000 neue Registrierungen", "https://www.bundeskanzleramt.gv.at/bundeskanzleramt/nachrichten-der-bundesregierung/2025/12/id-austria-servicetour-zeigt-erfolg.html"),
 techno=L("CBC (28.06.2021): In science we trust – Technocracy Incorporated und Joshua Haldeman", "https://newsinteractives.cbc.ca/longform/technocracy-incorporated-elon-musk"),
 techw=L("Wikipedia: Technocracy movement", "https://en.wikipedia.org/wiki/Technocracy_movement"),
 kiss=L("US State Department, Office of the Historian: Rapprochement with China, 1972", "https://history.state.gov/milestones/1969-1976/rapprochement-china"),
 star=L("Scientific American (03/2026): SpaceX reaches milestone of 10,000 Starlink satellites in orbit", "https://scientificamerican.com/article/spacex-reaches-milestone-of-10-000-starlink-satellites-in-orbit/"),
 shield=L("Space.com (06.12.2022): SpaceX reveals „Starshield“ satellite project for national security use", "https://www.space.com/spacex-starshield-satellite-internet-military-starlink"),
 xai=L("DefenseScoop (14.07.2025): Pentagon AI contracts – xAI, Google, OpenAI, Anthropic", "https://defensescoop.com/2025/07/14/pentagon-ai-contracts-musk-xai-google-openai-anthropic-cdao/"),
 lifelog=L("WHYY: Facebook, a computing pioneer, a secret government program, and a strange coincidence", "https://whyy.org/segments/facebook-a-computing-pioneer-a-secret-government-program-and-a-strange-coincidence"),
 cia=L("CIA: CIA's Impact on Technology (Keyhole/In-Q-Tel)", "https://www.cia.gov/legacy/museum/exhibit/cias-impact-on-technology/"),
 google=L("CNBC (21.05.2018): Google seems to have removed most mentions of „don't be evil“", "https://www.cnbc.com/2018/05/21/google-seems-to-have-removed-most-mentions-of-dont-be-evil-from-its-code-of-conduct.html"),
 unsys=L("Vereinte Nationen: The UN System", "https://www.un.org/en/about-us/un-system"),
 sdg=L("Weltbank/UN: SDG-Metadaten Indikator 16.9.1", "https://worldbank.github.io/sdg-metadata/metadata/en/16-9-1"),
 wfp=L("The New Humanitarian (17.06.2019): UN, Yemen rebels, aid theft and biometrics", "https://www.thenewhumanitarian.org/news/2019/06/17/un-yemen-rebels-aid-theft-biometrics"),
 nato=L("NATO STO/CSO (10/2021): Cognitive Warfare – La guerre cognitive (Tagung Bordeaux 21.06.2021)", "https://innovationhub-act.org/wp-content/uploads/2023/12/NATO-CSO-CW-2021-10-26.pdf"),
 patent=L("Justia Patents: US 11,354,666 „Smart dust usage“ (Wells Fargo, erteilt 07.06.2022)", "https://patents.justia.com/patent/11354666"),
 acht=L("Fast Company: The 8-second attention span is BS – this is why", "https://www.fastcompany.com/91023619/8-second-attention-span-is-bs-this-is-why"),
 bots=L("Imperva (15.04.2025): 2025 Bad Bot Report", "https://www.imperva.com/blog/2025-imperva-bad-bot-report-how-ai-is-supercharging-the-bot-threat/"),
 os=L("StatCounter: Mobile Operating System Market Share Worldwide", "https://gs.statcounter.com/os-market-share/mobile-operating-system/worldwide"),
 online=L("Statista: Daily time spent online by internet users worldwide (Q3 2024, GWI)", "https://statista.com/statistics/1380282/daily-time-spent-online-global"),
 superc=L("Wikipedia: Superclass (book)", "https://en.wikipedia.org/wiki/Superclass_(book)"),
 unhq=L("Wikipedia: Headquarters of the United Nations", "https://en.wikipedia.org/wiki/Headquarters_of_the_United_Nations"),
 jugend=L("Wikipedia: Jugendwort des Jahres (Deutschland)", "https://de.wikipedia.org/wiki/Jugendwort_des_Jahres_(Deutschland)"),
 strong=L("Wikipedia: Maurice Strong", "https://en.wikipedia.org/wiki/Maurice_Strong"),
)

# ---------- Abschnitte ----------
A = []
def ab(emo, titel, von, bis, th, liste): A.append((emo + " " + titel, von, bis, th, liste))

ab("🎬", "Einspieler und Veranstalter-Werbung", "0:00", "0:02", "w", [
 "**Zusammenfassung:** Ein Zusammenschnitt von Sätzen aus dem späteren Vortrag (Biofeudalismus, Bernays-Zitat, Bildungstechnik in US-Schulen, E-ID, „freier Wille“) eröffnet das Video. Danach folgt ein Werbetext des Veranstalters BENU Solutions über den „Live vor Ort Kongress“.",
 "💬 Werbetext: „Warte nicht, bis andere für dich entscheiden.“ [0:01]",
 "📌 **Format:** Werbe-Einspieler des Veranstalters; inhaltlich Wiederholungen aus [0:21], [0:41], [0:47] und [1:17]."])
ab("🎙️", "Anmoderation: Leben wir in einer Simulation?", "0:02", "0:08", "a", [
 "**Zusammenfassung:** Der Moderator (im Transkript „Herr Tichi“, vermutlich Roland Tichy ❓) eröffnet die Nachmittagssitzung mit der Frage, ob wir „in einer Simulation“ leben. Als Beispiel nennt er die Lanz-Sendung, in der Daniel Günther auf die Frage nach einem Verbot kritischer Portale „Ja“ gesagt und das später bestritten habe; Bovenschulte habe zugestimmt, Söder abgewiegelt. Mit Monika Maron spricht er über die Pflicht, eine Person mit dem gewünschten Geschlecht anzusprechen. Merz nenne den Atomausstieg einen schweren Fehler, ändere aber nichts – Watzlawicks „mehr desselben“.",
 "💬 Moderator: „Am Ende gewinnt die Realität.“ [0:06]",
 "📌 Übergabe: Regenauers Buch frage sinngemäß „Sind wir alle blöd?“ [0:07]",
 "📚 **Ergänzung:** Die Lanz-Sendung lief am 07.01.2026; Günther antwortete auf die Frage nach Verbot oder Zensur mit „Ja“ und erklärte danach, er habe ein Social-Media-Verbot für unter 16-Jährige gemeint – " + Q['lanz'] + ". Merz sprach am 14.01.2026 vom „serious strategic mistake“ – " + Q['merz'] + ". Daraus folgt eine Aufnahme um den 16./17.01.2026.",
 "❓ Im Transkript werden „Herr Kujat“ [0:02] und „Herr Guat“ [0:06] angesprochen – vermutlich Gäste des Kongresses, nicht geklärt."])
ab("👤", "Wer er ist: Bühl, Illuminaten-Buch, Plattenlabel, IT-Chef", "0:08", "0:13", "a", [
 "**Zusammenfassung:** Regenauer, Jahrgang 1978, stammt aus Bühl bei Baden-Baden. Er war früh stellvertretender Fertigungsleiter und Betriebsleiter einer Werbe- und Siebdruckerei und meldete mit 18 ein Gewerbe an. Mit 15 oder 16 las er Umberto Ecos „Das Foucaultsche Pendel“ (1988) und danach ein dünnes Buch über Illuminaten, Zentralbanken und „Lohnsklaverei“ – Ausgangspunkt von über 30 Jahren Recherche. Ein Plattenlabel mit politischen Texten brachte kein Geld; danach arbeitete er als SAP-Berater, Projektleiter, Programmmanager und IT-Chef in Konzernen in über 20 Ländern.",
 "💬 „seit über 30 Jahren recherchiere und Bücher lese“ [0:10]",
 "📌 Songtexte von 2001 drucke er in seinen Büchern ab, weil darin stehe, was heute passiere – „fast prophetisch“. [0:11] [seine Sicht]",
 "📌 Die USA seien in weiten Teilen ein „Entwicklungsland“; Reisen erweiterten den Blick (Humboldt zugeschriebener Satz). [0:12] [seine Sicht]"])
ab("📚", "Blog, Bücher, Magazin – und die Gliederung „Polykrise“", "0:13", "0:18", "a", [
 "**Zusammenfassung:** Er lebt in der Schweiz, weil er früh aus der EU wollte. 2021 gründete er den Blog regenauer.press, auf dem alle Texte und Bücher frei abrufbar seien; seit 2024 erscheint das Print-Magazin „Gegendruck“. Er verlegt im eigenen Verlag, übersetzte ein Buch von James Corbett und kündigt „Degeneration X“ an (u. a. „dunkle Aufklärung“, Thiel, Bukele, Technate, Satellitenüberwachung, Tokenisierung). Die Folien mit Quellen stellt er zum Herunterladen bereit.",
 "💬 „Glauben Sie mir also nichts, sondern gucken Sie selber nach“ [0:16]",
 "📌 Die EU sei in einem Bericht von 1944 „von Ex-Nazis und deutschen Industriellen“ als „viertes Reich“ bezeichnet worden. [0:15] [seine Sicht] ❓ Welcher Bericht gemeint ist, sagt er nicht.",
 "📌 **Gliederung:** Die „Polykrise“ bestehe aus Demokratie, Migration, Wirtschaft, Technokratie, Global Governance und Social Engineering. [0:17]",
 "🔗 Ausführlicher zu seiner Person: {{a:ungeskriptet-regenauer|Regenauer bei {ungeskriptet}}}."])
ab("🗳️", "Demokratie: Quigleys Zwei-Parteien-Satz", "0:18", "0:21", "b", [
 "**Zusammenfassung:** Nach einem Hinweis auf seine getönte Brille (Unfall) beginnt der erste Block. Die Demokratie sei nicht am Ende, sondern tue genau, was sie solle. Als Beleg zitiert er den Historiker Carroll Quigley („Tragedy and Hope“, rund 1.300 Seiten), der als Einziger Zugang zu den Unterlagen der Round-Table-Gruppe gehabt habe. Auf S. 1247 stehe sinngemäß: Gegensätzliche Parteien seien eine törichte Idee; die beiden Parteien sollten nahezu gleich sein, damit Wahlen keine tiefgreifenden Politikwechsel bringen.",
 "💬 „Demokratie ist eine Selektion.“ [0:20]",
 "📌 Links gegen rechts sei „Beschäftigungstherapie“; man wähle nur, von wem man beherrscht werde. [0:20–0:21] [seine Sicht]",
 "📚 **Ergänzung:** Das Buch erschien 1966 (er nennt 1974). Der Satz steht im Buch; Quigley beschreibt dort, wie Parteien aus Sicht dieser Denkschule sein „sollten“ – " + Q['quigley'] + "."])
ab("📣", "Bernays, „Propaganda“ und die Fluorid-Geschichte; Wilson", "0:21", "0:26", "b", [
 "**Zusammenfassung:** Edward Bernays, Neffe Sigmund Freuds und „Vater der PR“, beschreibe im ersten Absatz von „Propaganda“ (1928) die Manipulation der Massen als Teil der Demokratie und eine „unsichtbare Regierung“. Bernays habe Seife per Schnitzwettbewerb verkauft und – nach seiner Darstellung – für Alcoa die Idee entwickelt, Fluorid aus der Aluminiumherstellung in Zahnpasta zu mischen. Ein US-Gericht habe „Anfang 25“ festgestellt, Fluorid senke bei Kindern den IQ um 2 bis 5 Punkte; er rät von fluoridhaltiger Zahnpasta ab. Zudem zitiert er Woodrow Wilsons „The New Freedom“ (1913) über eine unbenannte, allgegenwärtige Macht und nennt Wall Street und Bankenkartelle als naheliegend.",
 "💬 „die wahre herrschende Macht unseres Landes“ (Bernays-Zitat, vorgelesen) [0:21]",
 "📌 Der Satz „eine Lüge muss man nur oft genug wiederholen“ stamme aus diesem Buch; Goebbels und Hitler hätten es genutzt. [0:23–0:24] [seine Sicht]",
 "📌 In den 1930ern habe die Wall Street in den USA einen Diktator installieren wollen und danach die NSDAP finanziert – „belegte, offiziell zugängliche Dokumente“. [0:25] [seine Sicht]",
 "📚 **Ergänzung:** Im Buchtext steht der Seifen-Wettbewerb (Ivory), aber weder Fluorid noch der „Lüge“-Satz – " + Q['bernays'] + ". Zum Urteil (Trinkwasser, nicht Zahnpasta; 2024) siehe Abgleich. Wilson nennt die Macht nicht beim Namen – " + Q['wilson'] + ".",
 "📚 **Gesundheit:** Zu Fluorid in Zahnpasta empfehlen deutsche Fachstellen altersgerechte Mengen; Fragen dazu gehören in die Zahnarzt- oder Kinderarztpraxis."])
ab("🐺", "Fabian Society und Moses Hess", "0:26", "0:29", "b", [
 "**Zusammenfassung:** Die Fabian Society gebe es noch heute; sie habe 1900 an der Wiege der Labour Party gestanden, alle sozialdemokratischen Premierminister Großbritanniens seien Mitglied gewesen, ihr Wappen ein Wolf im Schafspelz. Ihr Programm sei die Unterwanderung politischer, wirtschaftlicher und kultureller Strömungen. Für Deutschland nennt er Moses Hess (Bonn, „Rom und Jerusalem“), den die SPD als Vater der deutschen Sozialdemokratie bezeichne und den er „Vater des imperialistischen Zionismus“ nennt. Hess habe die „Rheinische Zeitung“ gegründet, in der Marx seinen ersten Text veröffentlicht habe, und Marx und Engels geprägt.",
 "💬 „ein Wolf im Schafspelz“ [0:26]",
 "📌 Hess habe den Vorläufer des Kommunistischen Manifests geschrieben; Marx habe „am wenigsten“ dazu beigetragen. [0:28] [seine Sicht]",
 "📚 **Ergänzung:** Der Wolf im Schafspelz ist ein Emblem auf dem 1910 von Shaw entworfenen „Fabian Window“ (heute LSE), als Sinnbild des schrittweisen Vorgehens – " + Q['fwin'] + ". Hess: geb. 1812 in Bonn, „Rom und Jerusalem“ erschien 1862 – " + Q['hess'] + "."])
ab("🧬", "Eugenik, Huxley, UNESCO – und was daraus wurde", "0:29", "0:33", "b", [
 "**Zusammenfassung:** Die Fabian Society sei von Anhängern der Eugenik gegründet worden; er nennt Milner, Rhodes, Margaret Sanger (Planned Parenthood; Bill Gates' Vater dort Direktor; Pro Familia von ihr gegründet), H. G. Wells, George Bernard Shaw und Bertrand Russell („Principles of Social Reconstruction“, 1916, mit Weltregierung, Weltarmee, Weltwährung). UN-Generalsekretär Guterres sei Chef der Sozialistischen Internationale gewesen. Julian Huxley, Direktor der Eugenik-Gesellschaft, sei erster UNESCO-Generaldirektor gewesen und habe im Gründungsdokument die Eugenik in „Transhumanismus“ umbenennen wollen; heute heiße das „biodigitale Konvergenz“. Die „Eugenics Review“ heiße heute „Journal of Biosocial Science“ (Cambridge).",
 "💬 „Man hat's einfach umbenannt.“ [0:31]",
 "📌 Bioethik, biodigitale Konvergenz und Transhumanismus seien „nichts anderes als Eugenik“. [0:31–0:32] [seine Sicht]",
 "📚 **Ergänzung:** Guterres war 1999–2005 Präsident der Sozialistischen Internationale – " + Q['guterres'] + ". Huxley war laut Aeon Vizepräsident der Eugenics Society; seine Schrift von 1946 wurde von der UNESCO-Vorbereitungskommission als persönliche Ansicht zurückgewiesen – " + Q['huxley'] + ". Den Begriff „Transhumanismus“ machte er 1957 bekannt – " + Q['trans'] + "."])
ab("🇮🇪", "Irland 2025: Rekord an ungültigen Stimmen", "0:33", "0:35", "b", [
 "**Zusammenfassung:** Laut Irish Times vom Oktober 2025 hätten bei einer Wahl in Irland teils über 20 % der Wähler ungültig gestimmt, bei nur 40–41 % Beteiligung; früher seien es höchstens 4 % gewesen, „vor 80 Jahren“. Politiker hätten danach nicht gewusst, wie sie eine legitime Regierung bilden sollten; der Parlamentssprecher habe das im Fernsehen erklären müssen.",
 "💬 „würde man das für eine Comedy Sendung halten“ [0:34]",
 "📚 **Ergänzung:** Es war die Präsidentschaftswahl vom 24.10.2025 (Sieg Catherine Connolly). Beteiligung 45,8 %, ungültig 12,9 % (213.738) – " + Q['rte'] + ". Eine Regierung wird bei dieser Wahl nicht gebildet; die Szene mit dem Parlamentssprecher ist ❓ nicht geklärt."])
ab("🧳", "Migration: Bezahlkarte, „Replacement Migration“, Teile und herrsche", "0:35", "0:39", "c", [
 "**Zusammenfassung:** Migration bringe Probleme, werde aber wie links/rechts als „Spaltpilz“ benutzt. Die Bezahlkarte für Migranten sei ein Testlauf für E-ID und Bürger-Wallet. Der UN-Bericht „Replacement Migration“ (März 2000) habe die Zahl der nötigen Einwanderer bis 2025 vorausberechnet; 18 Monate später folgten der 11. September und der „Krieg gegen den Terror“, der den Nahen Osten destabilisiert und Fluchtbewegungen ausgelöst habe. Er zitiert Huntingtons „Kampf der Kulturen“ (1996): Der Westen habe die Welt durch organisierte Gewalt erobert. Statt sich spalten zu lassen, solle man Brücken bauen – auch zu Migranten, die in Berlin dem Corona-Kurs kritischer gegenüberstanden hätten.",
 "💬 „Migration als Waffe“ (Schlagzeile der Süddeutschen, 03.03.2016, nach ihm) [0:36]",
 "📌 Medien bliesen Probleme auf – nach einer Meldung über Paris sei dort am nächsten Tag nichts davon zu sehen gewesen. [0:38] [seine Sicht]",
 "📚 **Ergänzung:** Der UN-Bericht rechnet Szenarien und betont, sie seien keine Empfehlungen; für Deutschland ergäben sich bei konstanter Erwerbsbevölkerung im Schnitt 487.000 Zuwanderer pro Jahr – " + Q['repl'] + ". Die Bezahlkarte wurde am 12.04.2024 bundesrechtlich beschlossen – " + Q['bezahl'] + "."])
ab("🏭", "Wirtschaft: Insolvenzen und Entlassungen durch KI", "0:39", "0:41", "d", [
 "**Zusammenfassung:** Bis 2030 kämen drastische sozioökonomische Veränderungen – „der Endspurt zur Agenda 2030“. Insolvenzen stiegen in Deutschland und Österreich wegen Beschaffungs- und Energiekosten und Handelskriegen. In den USA seien im Oktober 2025 rund 1,1 Mio. Menschen wegen KI entlassen worden – nicht nur Programmierer, auch Lager- und künftig Lieferfahrer. Das Handwerk sei weniger betroffen.",
 "💬 „das fängt gerade erst an“ [0:40]",
 "📚 **Ergänzung:** Laut Challenger-Bericht gab es im Oktober 2025 153.074 angekündigte Stellenstreichungen, 1.099.500 seit Jahresbeginn; KI wurde im Oktober für 31.039 und im Jahr für 48.414 genannt – " + Q['chall'] + ". Unternehmensinsolvenzen in Deutschland 2025: 24.064 – " + Q['insol25'] + "."])
ab("🌳", "Biofeudalismus: 30×30, Tokenisierung, CO2-Budget", "0:41", "0:43", "d", [
 "**Zusammenfassung:** Unter „Biofeudalismus“ versteht er die Monetarisierung der globalen Gemeingüter: Das Ziel „30×30“ (30 % unter Schutz bis 2030) bedeute Privatisierung und Gebühren. Jedem Baum, jeder Wiese, jedem Kubikmeter Wasser werde ein Token zugewiesen. In Südamerika überwachten Satelliten den CO2-Ausstoß von Pflanzen und schickten Bauern Rechnungen („Green Plus“ ❓). Die Green Economy sei der größte Markt aller Zeiten. Ein Experte habe in der Tagesschau ein CO2-Budget von etwa 1.500 kg pro Person genannt.",
 "💬 „Das ist eine globale Agenda aller 193 UN-Mitgliedstaaten.“ [0:42]",
 "📌 18 % der europäischen Küstenstreifen stünden schon unter Naturschutz. [0:41] ❓ Quelle nicht genannt.",
 "📚 **Ergänzung:** Das 30×30-Ziel ist Ziel 3 des Kunming-Montreal-Rahmens (Dezember 2022): Schutz und Management von mindestens 30 % der Flächen, unter Achtung der Rechte indigener Völker – " + Q['gbf'] + "; ❓ Sendung und Experte zum CO2-Budget nicht ermittelt."])
ab("🏦", "Geld: Bargeld, Digitalwährung und das „Universal Ledger“ der BIZ", "0:43", "0:46", "d", [
 "**Zusammenfassung:** Es folgten Social Impact Finance und „Human Capital Performance Bonds“. Bargeld werde abgeschafft, an seine Stelle träten private Bank-Coins oder Zentralbankgeld, im Hintergrund in einer Datenbank zusammengeführt. Daten seien das Gold der Zeit. Staatsschulden seien nie zur Tilgung gedacht gewesen. Die BIZ in Basel baue dafür ein „Universal Ledger“ auf exterritorialem Gebiet; dort könnten etwa Bücher auf eine Sperrliste kommen oder das Tiefkühlregal bei verbrauchtem CO2-Budget verschlossen bleiben. BIZ-Chef Carstens habe das so erklärt.",
 "💬 „Daten … das ist das Gold unserer Zeit“ [0:43]",
 "📌 Ob Trump Zentralbankwährungen verbiete, sei „völlig irrelevant“, weil die Bank-Coins ohnehin zentral abgeglichen würden. [0:44] [seine Sicht]",
 "📚 **Ergänzung:** Die BIZ stellte das „unified ledger“ am 20.06.2023 als Konzept vor (tokenisiertes Zentralbankgeld und tokenisierte Einlagen auf einer Plattform) – " + Q['bis'] + ". Belegt ist ein Carstens-Satz von 2020 über „absolute control“ der Zentralbank über die Regeln einer CBDC – " + Q['carst'] + "; Sperrlisten für Bücher oder CO2-Budgets nennt die BIZ-Mitteilung nicht."])
ab("🎒", "Kinder als Anlageobjekt? EdTech und E-ID", "0:46", "0:49", "d", [
 "**Zusammenfassung:** Kombiniere man SDG-Ziele wie hochwertige Bildung und Wirtschaftswachstum, lande man beim „Human Capital Performance Bond“. In US-Schulen erfasse Lernsoftware (EdTech) Noten, Fähigkeiten und Verhalten der Kinder; auf diese Daten könne man wie auf Aktien wetten. Wer auf ein Scheitern setze, habe ein Interesse, dem Kind Fördermittel zu entziehen. Mit der E-ID – in Deutschland ab Ende 2026/Anfang 2027, in Österreich schon vorhanden – würden auch Erwachsene „handelbar“.",
 "💬 „Das macht dann das Kind … zum Investment Asset.“ [0:47–0:48]",
 "📌 Das laufe in Amerika bereits („Spekulationsobjekt Leben“, eigener Artikel). [0:48] [seine Sicht] ❓ Einen konkreten Fall nennt er nicht.",
 "📚 **Ergänzung:** Die EUDI-Wallet stützt sich auf die Verordnung (EU) 2024/1183; Deutschland plant den Start am 02.01.2027; die Nutzung ist freiwillig – " + Q['eudi'] + "."])
ab("🌍", "WEF-Bericht September 2025 und der CO2-Preis", "0:49", "0:51", "d", [
 "**Zusammenfassung:** Ein WEF-Bericht vom September 2025 nenne zehn Hebel, darunter Natural Asset Companies, Debt-for-Nature Swaps, Zahlungen für Ökosystemleistungen und interne Umweltbepreisung. Seine Lesart: Großkonzerne und Vermögensverwalter polsterten sich gegenseitig ab, der Mittelstand gehe an den Kosten zugrunde, der Steuerzahler zahle, Staaten strukturierten Schulden über Klimaauflagen um. Der Bundestag habe im Februar 2025 „im Windschatten der Migrationsdebatte“ eine drastische CO2-Preiserhöhung beschlossen.",
 "💬 „Die Weichen sind gestellt“ [0:51]",
 "📚 **Ergänzung:** Der WEF-Bericht „Finance Solutions for Nature“ (mit McKinsey) definiert NACs als Unternehmen, die den Wert der Natur über Eigenkapital in Erträge umwandeln – " + Q['wef'] + ". Am 30.01.2025 beschloss der Bundestag die TEHG-Novelle zur Umsetzung des EU-Emissionshandels – " + Q['tehg'] + "; die nationalen CO2-Festpreise (2025: 55 €/t) waren schon vorher festgelegt – " + Q['dehst'] + "."])
ab("⚙️", "Technokratie: Technocracy Inc., Musks Großvater, Kissinger", "0:51", "0:54", "e", [
 "**Zusammenfassung:** Technokratie sei nicht Digitalisierung, sondern ein „faschistoides Herrschaftsmodell“: 1919 Technical Alliance, dann Committee on Technocracy und Howard Scotts Technocracy Inc., einst mit einer halben Million Mitgliedern. Musks Großvater habe die Bewegung in Kanada geleitet. Kissinger sei 1971 nicht aus kulturellen Gründen nach China gereist, sondern um im Auftrag der Rockefellers Kapital für Chinas Aufbau zu öffnen. In der Technokratie gebe es kein Geld, sondern Energiezertifikate nach Herstellungsaufwand.",
 "💬 „Kissinger hat nicht für die US-Regierung gearbeitet“ [0:53] [seine Sicht]",
 "📌 Leseempfehlung: David Rockefellers Erinnerungen („Erinnerungen eines Weltbankiers“). [0:53]",
 "📚 **Ergänzung:** Technocracy Inc. wurde 1933 in New York gegründet; Joshua Haldeman war 1936–1941 eine Führungsfigur in Kanada; die Energiezertifikate sollten nicht handelbar sein – " + Q['techno'] + ". Kissinger reiste 1971 zweimal als Sicherheitsberater Nixons nach Peking – " + Q['kiss'] + "."])
ab("🛰️", "Technokratie heute: Musk, Khanna, Trump", "0:54", "0:57", "e", [
 "**Zusammenfassung:** CO2-Bepreisung sei dasselbe wie die Energiepunkte der Technokraten – nur heute dank Rechenleistung und Smartphones in Echtzeit umsetzbar. Regiert werde von Bürgerräten und Experten. Musk sei Fan der Technokratie und wolle sie auf dem Mars erproben. Parag Khanna habe 2017 eine „direkte Technokratie“ für die USA skizziert; Trump folge solchen Modellen sowie Curtis Yarvin und Nick Land. Die Familie Musk stamme aus einem Dorf im Berner Hinterland. Er schließt mit Konrad Zuse: Gefährlicher als ein menschenähnlicher Computer sei ein computerähnlicher Mensch.",
 "💬 „was damals nicht machbar war … das ist heute alles machbar“ [0:54]",
 "📌 Der „New Yorker“ nenne diese Herrschaftsform faschistoid. [0:55] ❓ Artikel nicht ermittelt.",
 "❓ Schweizer Herkunft der Familie Musk nicht geprüft."])
ab("📱", "Smartphone: Bots, Monopol, sieben Stunden am Tag", "0:57", "0:59", "f", [
 "**Zusammenfassung:** Das Stadtbild sei voll von „Zombies“ mit leuchtendem Brett vor dem Kopf. Mindestens 70 % des Datenverkehrs würden automatisch erzeugt, auf sozialen Plattformen über 85 %. 98 % der Smartphones liefen mit Android oder iOS. 16- bis 64-Jährige verbrächten weltweit 6 Std. 58 Min. täglich am Gerät. Er nennt Phänomene wie Phantomvibration und FOMO und sagt, die Aufmerksamkeitsspanne sei seit 2007 von 16–18 auf 8–11 Sekunden gesunken.",
 "💬 „Das Stadtbild ist voll von Zombies“ [0:57]",
 "📚 **Ergänzung:** Automatisierter Verkehr 2024: 51 % des Webverkehrs (Imperva) – " + Q['bots'] + "; Android 72,36 %, iOS 27,61 % (Okt. 2026) – " + Q['os'] + "; Online-Zeit Q3 2024: 6 Std. 38 Min. – " + Q['online'] + ". Die 8-Sekunden-Zahl ließ sich laut BBC-Recherche (2017) auf keine Studie zurückführen – " + Q['acht'] + "."])
ab("🪪", "Die E-ID als „hill to die on“", "0:59", "1:02", "f", [
 "**Zusammenfassung:** Die E-ID sei der Punkt, an dem man Widerstand leisten müsse. Smartphones speicherten Tasteneingaben (Keylogging), bevor sie im Messenger landeten – Signal oder Telegram nützten daher nichts. Mit der E-ID hingen am persönlichen Netzwerkgraphen Bonität, Führungszeugnis, Patientenakte, Führerschein und digitales Geld; alles lasse sich beobachten, steuern und abschalten. In Österreich hätten 50 % die ID; ohne sie bekämen Bauern keine Förderung, Lehrer könnten keine Noten eingeben.",
 "💬 „Wenn das Ding einmal ausgerollt ist, kommen Sie nicht mehr zurück.“ [1:01]",
 "📌 Über die E-ID werde selbst in neuen Medien am wenigsten gesprochen. [1:01] [seine Sicht]",
 "📚 **Ergänzung:** ID Austria: rund 4,8 Mio. Registrierungen (Dez. 2025) – " + Q['idat'] + ". In der EU darf niemand benachteiligt werden, der die Wallet nicht nutzt (Art. 5a Abs. 15) – " + Q['eudi'] + ". Ein allgemeines Keylogging aller Smartphones ist ❓ nicht belegt.",
 "❓ „Josef Vater“ [1:01] – Anspielung (Kabarett?) unklar."])
ab("📡", "Starlink, Starshield und xAI", "1:02", "1:04", "f", [
 "**Zusammenfassung:** Nicht mehr die Funkmasten seien das Problem, sondern Satelliten im (sehr) niedrigen Orbit wie Starlink; bis 2030 werde die Erde davon umhüllt („Prison Planet“). Diese seien mit Starshield, der militärischen Variante, verbunden – dort gehe es um Laser und gerichtete Energie. Musks Firmen hingen an xAI, das Twitter gekauft habe und vom Pentagon genutzt werde. Wer mit KI über „Verschwörungstheorien“ chatte, trainiere das System, das ihn später überwache.",
 "💬 „etwa so gesund, wie wenn Sie den Kopf in die Mikrowelle stecken“ [1:02] [seine Sicht]",
 "📚 **Ergänzung:** Am 17.03.2026 waren 10.020 Starlink-Satelliten aktiv (McDowell) – " + Q['star'] + ". Starshield (vorgestellt Dez. 2022): Erdbeobachtung, Kommunikation, Nutzlasten, Laser-Interoperabilität mit Starlink; „directed energy“ wird dort nicht genannt – " + Q['shield'] + ". xAI erhielt am 14.07.2025 wie Google, OpenAI und Anthropic einen Pentagon-Rahmenvertrag bis 200 Mio. $ – " + Q['xai'] + ".",
 "📚 **Gesundheit:** Eine Gesundheitsgefahr durch Starlink-Terminals belegt er nicht; Fragen zu Funkstrahlung beantwortet in Deutschland das Bundesamt für Strahlenschutz."])
ab("👁️", "Wer hinter den Tech-Konzernen steht: In-Q-Tel, LifeLog, Google", "1:04", "1:07", "e", [
 "**Zusammenfassung:** Smartphones hörten zu (Katzenfutter-Werbung, Anzug-Werbung). Für Google, Facebook und andere sei das erste Kapital von DARPA, CIA, In-Q-Tel, FBI oder Pentagon gekommen. Das DARPA-Projekt LifeLog, das Profile aller US-Bürger anlegen sollte, sei am 04.02.2004 eingestellt worden – am selben Tag sei Facebook online gegangen. Google habe sein Motto „Don't be evil“ gestrichen; Palantir sei noch schlimmer.",
 "💬 „Nur geben Sie jetzt die Daten selber ein“ [1:06]",
 "📚 **Ergänzung:** In-Q-Tel investierte 2003 in Keyhole, das Google 2004 kaufte (Grundlage von Google Earth) – " + Q['cia'] + ". LifeLog endete am 04.02.2004, dem Facebook-Starttag; eine Beteiligung der DARPA an Facebook ist laut WHYY nicht belegt – " + Q['lifelog'] + ". „Don't be evil“ steht seit 2018 nur noch als letzter Satz im Verhaltenskodex – " + Q['google'] + "."])
ab("🏛️", "Global Governance: Pyramide, Club of Rome, Nachhaltigkeitspläne", "1:07", "1:10", "g", [
 "**Zusammenfassung:** Regiert werde über öffentlich-private Partnerschaften – was Mussolini Korporatismus nannte. Seine Pyramide: oben Banken, darunter Policy Makers und Thinktanks, dann UN und IWF, nationale Regierungen, Propaganda-Medien, ganz unten die Öffentlichkeit. Das Klima-Narrativ stamme vom Club of Rome („Limits to Growth“, laut ihm in der Rockefeller-Villa bei Bellagio geschrieben); über Maurice Strong, UNEP, die COP-Konferenzen und Gro Harlem Brundtland sei es in 50 Jahren bis ins Bürgermeisteramt durchgesickert – daher Tempo 30 und Nachhaltigkeitspläne.",
 "💬 „bis man von oben die gesamte Struktur usurpiert hat“ [1:09]",
 "📌 Wählen wirke nur auf die unterste Ebene, „die uns was im Fernsehen vortanzen“. [1:09] [seine Sicht]",
 "📚 **Ergänzung:** UNEP wurde 1972 gegründet, Strong war ihr erster Leiter – " + Q['strong'] + ". ❓ Entstehungsort von „Limits to Growth“ nicht geprüft."])
ab("🇺🇳", "Die UN: Organigramm, WFP-Biometrie, Ziel 16.9", "1:10", "1:12", "g", [
 "**Zusammenfassung:** Wer aus der WHO austreten wolle, ziele zu kurz: Die UN bestehe aus vielen Unterorganisationen, zu denen auch IWF und Weltbank gehörten. Das Welternährungsprogramm gebe in Afrika Nahrung nur noch gegen biometrische ID. SDG-Ziel 16.9 sehe bis 2030 eine Identität mit Geburtsurkunde für jeden vor – „das ist die E-ID“. Die UN stehe auf einem Grundstück der Rockefellers und sei anfangs weitgehend von ihnen bezahlt worden.",
 "💬 „Also man muss nicht die WHO abschaffen, sondern die UN“ [1:11] [seine Sicht]",
 "📚 **Ergänzung:** IWF und Weltbankgruppe sind Sonderorganisationen im UN-System – " + Q['unsys'] + ". Indikator 16.9.1 misst registrierte Geburten unter 5-Jähriger; digitale ID wird darin nicht genannt – " + Q['sdg'] + ". Biometrie-Streit WFP/Huthis im Jemen 2019 – " + Q['wfp'] + ". John D. Rockefeller Jr. stiftete 8,5 Mio. $ für das Grundstück – " + Q['unhq'] + "."])
ab("🧠", "Social Engineering: Smombies und kognitive Kriegsführung", "1:12", "1:14", "f", [
 "**Zusammenfassung:** Seine „Devolutionsskala“ führt von Zeitung über Radio und Fernsehen zum Smartphone. Das NATO Innovation Hub befasse sich mit kognitiver Kriegsführung als „sechster Dimension“ – mit Konferenzen im Herbst 2020 und Juni 2021. Der Dritte Weltkrieg habe längst begonnen, und zwar zwischen den Ohren. Die meisten Menschen seien Werkzeug ihres Smartphones; Meinungen stammten aus der Timeline statt aus eigenem Nachdenken.",
 "💬 „Das Smartphone ist kein Werkzeug.“ [1:13]",
 "📚 **Ergänzung:** „Smombie“ war Jugendwort 2015 (er: 2017) – " + Q['jugend'] + ". Der NATO-Tagungsband (Bordeaux, 21.06.2021) diskutiert die kognitive als mögliche sechste Domäne und hält die Abgrenzung für offen – " + Q['nato'] + "."])
ab("✨", "Smart Dust", "1:14", "1:17", "f", [
 "**Zusammenfassung:** Es gebe „Smart Dust“ – intelligenten Nanostaub, in der Industrie seit über 15 Jahren für Lieferketten im Einsatz; auf der Webseite des Bundesinnenministeriums heiße es, er sei Teil der Smart City. Jedes Partikel sei ein kleiner Computer; ein Produkt („Neurosform 3“ ❓) lasse sich injizieren und Gehirnsignale auslesen. Der Anfang sei 1997 die Firma Dust Networks gewesen (heute Analog Devices); ein Wells-Fargo-Patent vom Juni 2022 beschreibe Bezahl-Authentifizierung mit Smart Dust. Wann und gegen wen das eingesetzt werde, wisse man nicht.",
 "💬 „Ich will Ihnen nur zeigen, dass es diese Technologie gibt.“ [1:14]",
 "📚 **Ergänzung (Stand der Technik):** Belegt ist das Patent US 11,354,666 „Smart dust usage“ (Wells Fargo, angemeldet 2016, erteilt 07.06.2022): Sensorschwarm aus MEMS sammelt biometrische Daten zur Freigabe einer Zahlung – " + Q['patent'] + ". Die ersten implantierbaren „Neural Dust“-Sensoren (Berkeley 2016) waren 3 mm lang, wurden Ratten an Nerven und Muskeln implantiert und per Ultraschall versorgt und ausgelesen – " + Q['ndust'] + "; ein einatembarer oder unbemerkt injizierbarer Staub zum Auslesen des Gehirns ist nicht belegt. ❓ BMI-Seite nicht gefunden."])
ab("🧭", "Fazit: Es geht um den freien Willen", "1:17", "1:19", "h", [
 "**Zusammenfassung:** Es gehe nicht mehr um Meinungsfreiheit, sondern um den Erhalt des freien Willens – den er einem großen Teil der Bevölkerung abspricht, weil er sich von Bildschirm und Algorithmus lenken lasse. Man solle niemandem glauben, auch ihm nicht, sondern Bauchgefühl und Intuition folgen: „kognitive Souveränität“. Das konkrete Ziel des Widerstands sei die E-ID – wer sie zulasse, mache das Leben seiner Kinder und Enkel kaputt.",
 "💬 „Sie sollten ausschließlich sich selbst glauben“ [1:17]",
 "📌 Man könne Menschen mit Technik „über die Luft“ manipulieren – „Das sind alles Dinge, die laufen.“ [1:18] [seine Sicht]"])
ab("🛠️", "Lösungen: anderes Telefon, Linux, RSS, OnlyOffice", "1:19", "1:22", "h", [
 "**Zusammenfassung:** Er empfiehlt ein Smartphone ohne Apple- oder Google-System (er nutzt Above Phone; er reise zu dessen Gründer nach Mexiko), sichere Browser wie Mullvad, einen VPN ohne Protokolle, Linux statt Windows, einen RSS-Reader für selbst gewählte Seiten (regenauer.press, manova.news, Tichys Einblick) und OnlyOffice statt Microsoft. Das Problem sei die Bequemlichkeit.",
 "💬 „Sie sind der Chef Ihres Lebens“ [1:21]",
 "📌 Above sei die einzige Firma, der er vertraue, weil er Gründer und Code kenne. [1:19] [seine Sicht]",
 "🔗 Werbebezug: Er erwähnt eigene Produkte (Magazin „Gegendruck“, Büchertisch) und eine Partnerfirma; Bewertung bleibt dem Leser."])
ab("❔", "Fragerunde: Wer sind „die“?", "1:22", "1:24", "h", [
 "**Zusammenfassung:** Der Moderator scherzt über die gekürzte Kaffeepause und fragt, wer „die“ seien. Regenauer nennt verschiedene Gruppen: Finanzkartelle im Hintergrund, Großinvestoren und Philanthropen wie Peter Thiel, „der die US-Regierung unter der Fuchtel hat“, sowie „Strömungen wie Technokraten und Zionisten“ mit großem Einfluss. Einzelne Namen zu nennen sei aber „meistens falsch, weil es eigentlich unseriös ist“. Er verweist auf David Rothkopfs „Superclass“ mit einer Liste von „7 bis 10.000“ Menschen.",
 "💬 „die zu benennen ist meistens falsch“ [1:23]",
 "📚 **Ergänzung:** Rothkopf spricht von rund 6.000 Personen – " + Q['superc'] + "."])
ab("🇨🇭", "Frage: Schweiz und wie man sich vor der E-ID schützt", "1:24", "1:26", "h", [
 "**Zusammenfassung:** Er lebt im Tessin, „wie Italien, nur mit Schweizer Infrastruktur“. Dass BIZ, Gavi, Club of Rome, Großbanken und FIFA ihren Sitz in der Schweiz hätten, habe Gründe. Eine Zuhörerin erwähnt Impfvorgaben in St. Gallen ❓. Die E-ID abzulehnen werde schwerer als der Widerstand gegen 2G/3G – bis zum Verlust von Bankzugang und Arbeit; man brauche mentale, finanzielle und soziale Reserven, wie von der EU sanktionierte Journalisten.",
 "💬 „das war ein Kinderspiel gegen das“ [1:25]",
 "📌 Ob die Schweiz die EU-Verträge unterschreibt, sei offen; „der Trend geht schlecht“. [1:24] [seine Sicht]"])
ab("👧", "Frage: Kinder, Schulpflicht, Homeschooling", "1:26", "1:28", "h", [
 "**Zusammenfassung:** Ein Zuhörer fragt, wie man Kinder und Enkel schützen könne. Regenauer: wenig Druck, viel Liebe, einen moralischen Kodex mitgeben – „je länger die Leine, desto glücklicher das Kind“. In einigen Schweizer Kantonen sei Hausunterricht möglich, ebenso in den USA; er nennt eine freie Schule in der Schweiz mit kleinen Klassen.",
 "💬 „möglichst wenig Druck und viel Liebe“ [1:27]"])
ab("🕊️", "Einwand: die friedlichste Zeit der Geschichte?", "1:28", "1:31", "h", [
 "**Zusammenfassung:** Der Moderator wirft ein, gemessen an Kriegstoten lebe die Menschheit in einer der friedlichsten Zeiten. Ein Zuhörer fragt, wie man optimistisch nach Hause gehen könne. Regenauer zitiert Sunzi und sagt, die wahre Revolution sei ein glückliches Leben; man solle nicht deprimiert, sondern „wutentbrannt“ nach Hause gehen und aktiv werden. Dem Moderator widerspricht er: Der Blick auf kinetische Kriege sei „veraltet“, der Krieg finde heute im Kopf statt und sei „in weiten Teilen schon lange verloren“.",
 "💬 Moderator: „in den friedlichsten Zeiten in der Geschichte der Menschheit“ [1:29]",
 "💬 Regenauer: „die wahre Revolution ist ein glückliches Leben zu führen“ [1:30]"])
ab("🗺️", "Frage: Trump, Austritte, multipolare Welt", "1:31", "1:35", "h", [
 "**Zusammenfassung:** Ein Zuhörer fragt, ob Trumps Austritt aus vielen internationalen Organisationen zeige, dass „die“ uneins seien. Regenauer: Es gebe Gerangel um den Platz am Kopfende, doch das Ziel sei eine multipolare Welt mit Währungsunionen nach EU-Vorbild. Trump baue mit Thiel ein Pilotprojekt für eine Technokratie („Freedom City“, Stablecoins) und wolle deshalb Grönland – wie die Technate-Karte der 1930er. Putin bekomme wohl einen Teil der Ukraine, China Taiwan; die Pax Americana und der Dollar als Leitwährung gingen zu Ende, die Welt teile sich wie bei Orwell in drei Blöcke.",
 "💬 „wie bei George Orwell drei Blöcke“ [1:34]",
 "📚 **Ergänzung:** Die US-Regierung ordnete am 07.01.2026 den Austritt aus 66 internationalen Organisationen an (Meldungen vom 07./08.01.2026) ❓ Primärquelle nicht abgerufen. Die Technate-Pläne reichten laut CBC „von Panama bis zum Nordpol“ – " + Q['techno'] + ".",
 "📌 **Ende:** Kaffeepause, Hinweis auf den Büchertisch. [1:35]"])

THEMEN = [{"k":"a","n":"Anmoderation & Person"},{"k":"b","n":"Demokratie & Geschichte"},{"k":"c","n":"Migration"},
 {"k":"d","n":"Wirtschaft, Geld & Klima"},{"k":"e","n":"Technokratie & Tech-Konzerne"},{"k":"f","n":"Smartphone, E-ID & Überwachung"},
 {"k":"g","n":"Global Governance & UN"},{"k":"h","n":"Fazit, Lösungen & Fragerunde"},{"k":"w","n":"Werbung/Organisatorisches"}]

def kurz(t):  # Teil-Text ohne Emoji
    return t.split(" ",1)[1]
teile = [{"von":v,"bis":b,"t":kurz(t),"th":th} for (t,v,b,th,_) in A]
abschnitte = [{"typ":"abschnitt","titel":"%s [%s–%s]"%(t,v,b),"th":th,"liste":li} for (t,v,b,th,li) in A]

# ---------- Reiter 1: Überblick ----------
uberblick = [
 {"typ":"folge","k":K,"titel":TITEL,"gast":GAST,"rolle":"Autor, Verleger und Blogger (regenauer.press), früher IT-Manager",
  "kanal":"BENU Solutions","art":"Vortrag","karte":"BENU Solutions · Kongressvortrag mit Fragerunde",
  "datum":"2026 ❓","dauer":"1 Std. 35 Min.","url":URL,
  "thema":"Kongressvortrag „Polykrise“: Regenauer verbindet Demokratie, Migration, Geld, Technokratie, UN und Smartphone zu einem Bild wachsender Kontrolle bis 2030 – mit der E-ID als Kernpunkt; danach Fragen aus dem Publikum.",
  "wege":[[K+"ab","📖","Vortrag im Detail","Abschnitt für Abschnitt, mit Zitaten"],[K+"zeit","📅","Zeitachse & Verzeichnisse","Ereignisse, Personen, Orte, Begriffe, Zahlen"],[K+"abgleich","⚖️","Abgleich & Daten","Diagramme, Aussagen neben Daten, Quellen"]],
  "kacheln":[]},
 {"typ":"hinweis","text":"Auswertung nach dem Transkript (automatische Untertitel): Gesagtes ohne Zeichen, Ergänzungen 📚, Unklares ❓. Fundstellen [Stunde:Minute] springen ins Video. Die Bewertung bleibt dem Leser."},
 {"typ":"abschnitt","titel":"⚡ In Kürze","liste":[
  "**Wer:** Tom-Oliver Regenauer (Jg. 1978, lebt in der Schweiz), Autor und Verleger, auf einem Kongress von BENU Solutions; angekündigt vom Moderator (vermutlich Roland Tichy ❓). Aufnahme um den 16./17.01.2026 📚.",
  "**These:** Die „Polykrise“ aus Demokratie, Migration, Wirtschaft, Technokratie, Global Governance und Social Engineering sei kein Zufall, sondern laufe auf Kontrolle bis 2030 hinaus [0:17].",
  "**Demokratie:** Mit Quigley, Bernays und Wilson begründet er, dass gewählte Politiker nicht die eigentliche Macht seien; Fabian Society, Moses Hess und Eugenik zeichnet er als Linie bis zum Transhumanismus [0:18–0:33].",
  "**Geld und Natur:** Gemeingüter würden tokenisiert, Bargeld durch zentral abgeglichene Digitalwährungen ersetzt (BIZ), Kinder über Bildungsdaten zu Anlageobjekten [0:41–0:51].",
  "**Technik:** Technokratie (Technocracy Inc., Musk, Thiel), Starlink/xAI, Tech-Konzerne mit Geheimdienst-Startkapital, Smartphones als „Taschenspion“ und Smart Dust [0:51–1:17].",
  "**Kern:** Die E-ID sei der Punkt des Widerstands – „that's the hill to die on“ [0:59–1:02], [1:18].",
  "**Ausweg:** Andere Geräte und Software, eigene Informationswege, „kognitive Souveränität“ und ein glückliches Leben als „wahre Revolution“ [1:19–1:31].",
  "**Daten dazu:** Viele Dokumente, die er nennt, existieren; einzelne Zahlen und Zuschreibungen weichen von den Quellen ab (Irland-Wahl, KI-Entlassungen, Fluorid-Urteil) – siehe Abgleich."]},
 {"typ":"abschnitt","titel":"🔦 Aus Regenauers Sicht – der rote Faden","liste":[
  "Seine Sicht: Wahlen ändern wenig, weil die eigentliche Macht nach Quigley, Bernays und Wilson außerhalb der Parlamente liegt – bei Banken, Stiftungen und Netzwerken.",
  "Seine Sicht: Diese Netzwerke hätten ihre Ziele seit über 100 Jahren offen aufgeschrieben (Fabianer, Eugenik, Club of Rome, UN-Ziele) und nur die Begriffe gewechselt.",
  "Seine Sicht: Krisen – Migration, Klima, Wirtschaft – dienten dazu, die Gesellschaft zu spalten und neue Strukturen durchzusetzen: Tokenisierung der Natur, digitales Geld, CO2-Budgets.",
  "Seine Sicht: Technisch werde das erst jetzt möglich – Smartphone, Satelliten, KI und E-ID verbinden alle Daten eines Menschen zu einem steuerbaren Profil.",
  "Seine Sicht: Darum gehe es nicht mehr um Meinungsfreiheit, sondern um den freien Willen; jeder müsse selbst prüfen, sich technisch unabhängig machen und die E-ID verweigern."]},
 {"typ":"text","text":"🎯 **Kernaussagen** – die zehn wichtigsten Thesen des Vortrags:"},
 {"typ":"tabelle","kopf":["#","Aussage","Begründung im Vortrag","Fundstelle","Gewicht"],"zeilen":[
  ["1","Die E-ID ist der entscheidende Punkt, an dem Widerstand nötig ist.","Verknüpft Bonität, Akten, Geld; in Österreich schon Pflicht für vieles","[0:59–1:02], [1:18], [1:25]","★★★"],
  ["2","Demokratie ist „Selektion“; gewählte Politiker sind nicht die eigentliche Macht.","Quigley S. 1247, Bernays, Wilson","[0:18–0:26]","★★★"],
  ["3","Sozialdemokratie und Eugenik haben gemeinsame Wurzeln, die heute nur umbenannt sind.","Fabian Society, Hess, Huxley, Eugenics Review","[0:26–0:33]","★★"],
  ["4","Migration wird als Spaltkeil benutzt; die Bezahlkarte ist ein Testlauf für die E-ID.","UN-Bericht 2000, Krieg gegen den Terror, Huntington","[0:35–0:39]","★★"],
  ["5","Natur und Gemeingüter werden tokenisiert und privatisiert („Biofeudalismus“).","30×30, WEF-Bericht 2025, CO2-Budgets","[0:41–0:51]","★★★"],
  ["6","Bargeld verschwindet; ein Zentralregister der BIZ steuert künftig, wofür man zahlen darf.","Universal Ledger, Carstens","[0:43–0:46]","★★"],
  ["7","Technokratie ist ein Herrschaftsmodell, das Musk, Thiel und Trump heute umsetzen.","Technocracy Inc., Haldeman, Khanna, Grönland","[0:51–0:57], [1:31–1:35]","★★"],
  ["8","Smartphones und Tech-Konzerne dienen der Überwachung; ihr Startkapital kam oft aus Militär und Geheimdiensten.","Keylogging, LifeLog/Facebook, In-Q-Tel","[0:57–1:07]","★★★"],
  ["9","Die UN, nicht die WHO, ist die zentrale Struktur der Global Governance.","Organigramm, SDG 16.9, WFP-Biometrie","[1:07–1:12]","★★"],
  ["10","Es geht um den freien Willen; Abhilfe sind eigene Technik und „kognitive Souveränität“.","NATO-Papiere, Smart Dust, Lösungsliste","[1:12–1:22]","★★"]]},
 {"typ":"baum","titel":"🌳 Themenbaum des Vortrags","wurzel":TITEL,"unter":GAST+" · BENU Solutions · 2026 · 1 Std. 35 Min.","knoten":[
  {"t":"🎙️ Rahmen & Person","k":[{"t":"Anmoderation: Simulation, Lanz [0:02]"},{"t":"Herkunft, IT-Laufbahn [0:08]"},{"t":"Blog, Magazin, Bücher [0:13]"},{"t":"Gliederung Polykrise [0:17]"}]},
  {"t":"🗳️ Demokratie & Geschichte","k":[{"t":"Quigley S. 1247 [0:20]"},{"t":"Bernays „Propaganda“ [0:21]"},{"t":"Wilson „New Freedom“ [0:24]"},{"t":"Fabian Society, Hess [0:26]"},{"t":"Eugenik, Huxley [0:29]"},{"t":"Irland-Wahl 2025 [0:33]"}]},
  {"t":"🧳 Migration","k":[{"t":"Bezahlkarte [0:35]"},{"t":"Replacement Migration 2000 [0:35]"},{"t":"Huntington [0:37]"},{"t":"Brücken bauen [0:38]"}]},
  {"t":"🏦 Wirtschaft & Geld","k":[{"t":"Insolvenzen, KI-Entlassungen [0:39]"},{"t":"Biofeudalismus, 30×30 [0:41]"},{"t":"BIZ Universal Ledger [0:44]"},{"t":"Bildungsdaten als Anlage [0:46]"},{"t":"WEF-Bericht, CO2-Preis [0:49]"}]},
  {"t":"⚙️ Technokratie & Tech","k":[{"t":"Technocracy Inc. [0:51]"},{"t":"Kissinger, China [0:52]"},{"t":"Khanna, Trump [0:55]"},{"t":"LifeLog, In-Q-Tel [1:05]"}]},
  {"t":"📱 Überwachung & E-ID","k":[{"t":"Bots, Monopol, Bildschirmzeit [0:57]"},{"t":"E-ID, Österreich [0:59]"},{"t":"Starlink, xAI [1:02]"},{"t":"Kognitive Kriegsführung [1:12]"},{"t":"Smart Dust [1:14]"}]},
  {"t":"🇺🇳 Global Governance","k":[{"t":"Pyramide, Club of Rome [1:07]"},{"t":"UN-System, SDG 16.9 [1:10]"},{"t":"Rockefeller-Grundstück [1:12]"}]},
  {"t":"🛠️ Lösungen & Fragen","k":[{"t":"Freier Wille [1:17]"},{"t":"Telefon, Linux, RSS [1:19]"},{"t":"Wer sind „die“? [1:22]"},{"t":"Kinder, Schule [1:26]"},{"t":"Multipolare Welt [1:31]"}]}]},
 {"typ":"illu","id":"kontrolle_pyramide","titel":"Skizze: Die Pyramide der Global Governance (Darstellung laut Regenauer, schematisch)"},
 {"typ":"illu","id":"kontrolle_eudi","titel":"Skizze: Der Weg zur EU-Wallet – Zeitplan und Regeln (belegte Daten)"},
 {"typ":"tabelle","kopf":["🧭 Steckbrief",""],"schmal":True,"zeilen":[
  ["**Thema in einem Satz**","Regenauers Kongressvortrag „Polykrise“ über Demokratie, Migration, Geld, Technokratie, UN und digitale Kontrolle – mit der E-ID als Kernpunkt."],
  ["**Titel**",TITEL+" – BENU Solutions (YouTube)"],
  ["**Format**","Kongressvortrag mit Folien [0:08–1:22], Anmoderation [0:02–0:08], Fragerunde aus dem Publikum [1:22–1:35]; Werbe-Einspieler des Veranstalters [0:00–0:02]; Hinweise auf eigene Bücher, Magazin und Büchertisch"],
  ["**Sprecher**","👤 **Tom-Oliver Regenauer** – Referent · 🎙️ **Moderator** (im Transkript „Herr Tichi“, vermutlich Roland Tichy ❓) · Zuhörer mit Fragen"],
  ["**Dauer**","1 Std. 35 Min."],
  ["**Datum**","Veröffentlichung 2026 ❓ (nicht ermittelt); Aufnahme um den 16./17.01.2026 📚 (Lanz-Sendung 07.01.2026 „vor zehn Tagen“, Merz-Satz 14.01.2026 „vorgestern“)"],
  ["**Grundton**","pointiert, düster, mit ironischen Einschüben; Aufruf zum Selberprüfen"],
  ["**Hinweis**","Folien mit Quellen laut Referent auf regenauer.press; Zahlen und Zitate im Abgleich geprüft. Querverweis: {{a:ungeskriptet-regenauer|Regenauer bei {ungeskriptet}}}"]]},
]

# ---------- Reiter 2 ----------
detail = [{"typ":"text","text":"🔎 Detaillierte Auswertung in der Reihenfolge des Vortrags – %d Abschnitte. Lesehilfe: 💬 Zitat, 📌 Aussage/Zahl/Beispiel, 🔗 Bezug, 📚 Ergänzung, ❓ unklar. Video: [%s](%s)." % (len(A), TITEL, URL)},
 {"typ":"gespraech","titel":"🧭 Vortragsverlauf – wann worüber gesprochen wird","dauer":"1:35","themen":THEMEN,"teile":teile}] + abschnitte

# ---------- Reiter 3 ----------
Z = lambda z,j,t,f,e=False: {"z":z,"j":j,"t":t,"f":f,"e":e}
zeit = [
 Z("1812",1812,"Moses Hess in Bonn geboren 📚","[0:27]",True),
 Z("1842",1842,"Rheinische Zeitung: Hess als Mitarbeiter, Marx stößt hinzu","[0:28]"),
 Z("1862",1862,"Hess: „Rom und Jerusalem“ (im Vortrag 1860)","[0:27]"),
 Z("1875",1875,"Hess stirbt in Paris; 1961 Umbettung nach Israel 📚","[0:27]",True),
 Z("1884",1884,"Gründung der Fabian Society 📚","[0:26]",True),
 Z("1899–1902",1899,"Burenkrieg mit Lagern in Südafrika","[0:31]"),
 Z("1900",1900,"Fabianer an der Gründung der Labour-Vorläuferin beteiligt","[0:26]"),
 Z("1909",1909,"„Eugenics Review“ erscheint (bis 1968) 📚","[0:31]",True),
 Z("1910",1910,"Shaw entwirft das „Fabian Window“ mit Wolf im Schafspelz 📚","[0:26]",True),
 Z("1913",1913,"Wilson: „The New Freedom“; Gründung der Federal Reserve","[0:24]"),
 Z("1916",1916,"Russell: „Principles of Social Reconstruction“","[0:29]"),
 Z("1919",1919,"Technical Alliance (Anfang der Technokratie-Bewegung)","[0:51]"),
 Z("1928",1928,"Bernays: „Propaganda“","[0:21]"),
 Z("1933",1933,"Technocracy Inc. von Howard Scott gegründet 📚","[0:52]",True),
 Z("1936–1941",1936,"Joshua Haldeman führt Technocracy in Kanada 📚","[0:52]",True),
 Z("1944",1944,"Bericht über Pläne deutscher Industrieller („viertes Reich“) ❓","[0:15]"),
 Z("1945",1945,"Irland: 4,4 % ungültige Stimmen bei der Präsidentenwahl 📚","[0:33]",True),
 Z("1946",1946,"Huxley erster UNESCO-Generaldirektor, Grundsatzschrift; Rockefeller stiftet UN-Grundstück","[0:31], [1:12]"),
 Z("1957",1957,"Huxley macht den Begriff „Transhumanismus“ bekannt 📚","[0:32]",True),
 Z("1966",1966,"Quigley: „Tragedy and Hope“ (im Vortrag 1974)","[0:18]"),
 Z("1969",1969,"„Eugenics Review“ wird „Journal of Biosocial Science“ 📚","[0:31]",True),
 Z("1971",1971,"Kissinger reist zweimal nach Peking","[0:52]"),
 Z("1972",1972,"„Limits to Growth“ (Club of Rome); UNEP gegründet, Leitung Maurice Strong","[1:08]"),
 Z("1978",1978,"Regenauer geboren (Bühl)","[0:08]"),
 Z("1987",1987,"Brundtland-Bericht 📚","[1:08]",True),
 Z("1988",1988,"Eco: „Das Foucaultsche Pendel“","[0:09]"),
 Z("1996",1996,"Huntington: „Kampf der Kulturen“","[0:36]"),
 Z("2000",2000,"UN-Bericht „Replacement Migration“ (März)","[0:35]"),
 Z("2001",2001,"11. September, Beginn des „Kriegs gegen den Terror“","[0:35]"),
 Z("2003",2003,"In-Q-Tel investiert in Keyhole (später Google Earth) 📚","[1:05]",True),
 Z("2004",2004,"04.02.: LifeLog eingestellt, Facebook startet","[1:05]"),
 Z("2007",2007,"Smartphone-Ära (iPhone) – Beginn der Aufmerksamkeitsthese","[0:58]"),
 Z("2015",2015,"„Smombie“ Jugendwort des Jahres (im Vortrag 2017) 📚","[1:12]",True),
 Z("2016",2016,"03.03.: SZ-Überschrift „Migration als Waffe“","[0:36]"),
 Z("2017",2017,"Khanna: „Technocracy in America“","[0:55]"),
 Z("2020",2020,"Herbst: NATO-Veranstaltungen zu kognitiver Kriegsführung; Carstens-Satz zur CBDC (19.10.)","[1:13], [0:45]"),
 Z("2021",2021,"Regenauer gründet seinen Blog; NATO-Tagung Bordeaux (Juni)","[0:13], [1:13]"),
 Z("2022",2022,"07.06.: Wells-Fargo-Patent „Smart dust usage“ erteilt; Dez.: Kunming-Montreal-Rahmen (30×30) und Starshield","[1:16], [0:41], [1:02]"),
 Z("2023",2023,"20.06.: BIZ stellt „unified ledger“ vor","[0:44]"),
 Z("2024",2024,"12.04.: Bundestag beschließt Bezahlkarte; Magazin „Gegendruck“ startet; eIDAS-2.0-Verordnung","[0:35], [0:13], [0:48]"),
 Z("2025",2025,"30.01.: TEHG-Novelle; 14.07.: Pentagon-Verträge mit xAI u. a.; 10.09.: WEF-Bericht; 24.10.: Irland-Wahl; Okt.: US-Stellenabbau 153.074","[0:50], [1:03], [0:49], [0:33], [0:39]"),
 Z("2026",2026,"07.01.: Lanz/Günther und US-Austritt aus 66 Organisationen; 14.01.: Merz zum Atomausstieg; Vortrag um 16./17.01.","[0:02], [1:31], [0:06]"),
 Z("2027",2027,"02.01.: geplanter Start der deutschen EUDI-Wallet 📚","[0:48]",True),
 Z("2030",2030,"Zieljahr: Agenda 2030, 30×30, SDG 16.9","[0:39], [0:41], [1:11]"),
]
zeit.sort(key=lambda e: e["j"])
personen = [
 ["Tom-Oliver Regenauer","Autor, Verleger (Jg. 1978), lebt im Tessin","Referent","durchgehend"],
 ["Moderator („Herr Tichi“) ❓","vermutlich Roland Tichy, Publizist","Anmoderation, Einwände","[0:02–0:08], [1:22–1:35]"],
 ["Markus Lanz, Daniel Günther","ZDF-Moderator; Ministerpräsident Schleswig-Holstein","Beispiel „Simulation“","[0:02–0:05]"],
 ["Andreas Bovenschulte, Markus Söder","Regierungschefs Bremen und Bayern","Reaktionen auf Günther","[0:03]"],
 ["Monika Maron","Schriftstellerin","Zitat zum Sprachgebrauch","[0:05]"],
 ["Friedrich Merz","Bundeskanzler","Atomausstieg; „Stadtbild“","[0:06], [0:57]"],
 ["Paul Watzlawick","Kommunikationsforscher","„mehr desselben“","[0:06]"],
 ["Umberto Eco","Schriftsteller","„Das Foucaultsche Pendel“","[0:09]"],
 ["James Corbett, Whitney Webb","Journalisten","Vorbilder; Corbett-Buch übersetzt","[0:13]"],
 ["Peter Thiel","Investor","„dunkle Aufklärung“, Einfluss auf US-Regierung","[0:14], [1:22], [1:32]"],
 ["Nayib Bukele","Präsident El Salvadors","Thema im nächsten Buch","[0:14]"],
 ["Carroll Quigley","US-Historiker","Zwei-Parteien-Zitat","[0:18–0:20]"],
 ["Edward Bernays","PR-Pionier, Neffe Freuds","„Propaganda“, Seife, Fluorid","[0:21–0:24]"],
 ["Woodrow Wilson","US-Präsident 1913–1921","„The New Freedom“","[0:24]"],
 ["Moses Hess","Publizist (1812–1875)","Sozialdemokratie, Zionismus, Marx","[0:27–0:28]"],
 ["Karl Marx, Friedrich Engels","Theoretiker","Rheinische Zeitung","[0:28]"],
 ["Alfred Milner, Cecil Rhodes","britische Imperialpolitiker","Fabian-Umfeld laut ihm","[0:29]"],
 ["Margaret Sanger","Gründerin von Planned Parenthood","Eugenik-Bezug","[0:29]"],
 ["William H. Gates Sr.","Anwalt, Vater von Bill Gates","Planned Parenthood","[0:29]"],
 ["H. G. Wells, George Bernard Shaw","Schriftsteller, Fabianer","Eugenik-Zitate","[0:29]"],
 ["Bertrand Russell","Philosoph","Buch 1916","[0:29]"],
 ["António Guterres","UN-Generalsekretär","früher Präsident der Sozialistischen Internationale","[0:30]"],
 ["Julian Huxley","Biologe, erster UNESCO-Chef","Eugenik, Transhumanismus","[0:31–0:32]"],
 ["Samuel P. Huntington","Politikwissenschaftler","„Kampf der Kulturen“","[0:36]"],
 ["Agustín Carstens","BIZ-Generaldirektor (bis 2025)","CBDC-Aussagen","[0:45]"],
 ["Howard Scott","Gründer Technocracy Inc.","Technokratie","[0:52]"],
 ["Joshua N. Haldeman","Großvater Elon Musks","Technocracy in Kanada","[0:52]"],
 ["Elon Musk","Unternehmer","Technokratie, Starlink, xAI","[0:52–0:56], [1:02–1:03]"],
 ["Henry Kissinger, David Rockefeller","Sicherheitsberater; Bankier","China-Öffnung laut ihm","[0:52–0:53]"],
 ["Parag Khanna, Curtis Yarvin, Nick Land","Autoren","Technokratie-Modelle","[0:55]"],
 ["Donald Trump","US-Präsident","Technate, Grönland, Austritte","[0:55], [1:31–1:33]"],
 ["Konrad Zuse","Computerpionier","Zitat Mensch/Computer","[0:56]"],
 ["Mark Zuckerberg","Facebook-Gründer","LifeLog-Vergleich","[1:06]"],
 ["Maurice Strong, Gro Harlem Brundtland","UNEP-Chef; norwegische Premierministerin","Klima-Agenda laut ihm","[1:08]"],
 ["Benito Mussolini","Diktator","Korporatismus","[1:07]"],
 ["David Rothkopf","Autor „Superclass“","Elite-Liste","[1:23]"],
 ["Sunzi","Militärstratege","„Die Kunst des Krieges“","[1:29]"],
 ["George Orwell","Schriftsteller","drei Machtblöcke","[1:34]"],
]
orte = [
 ["Bühl / Baden-Baden","Herkunft","[0:08]"],["Tessin (Schweiz)","Wohnort","[0:12], [1:24]"],
 ["Bonn","Geburtsort von Moses Hess","[0:27]"],["Irland","Präsidentschaftswahl 2025","[0:33]"],
 ["Berlin, Paris","Beispiele zu Migration und Medien","[0:38]"],["Basel (BIZ)","„Universal Ledger“, Sitz der BIZ","[0:44]"],
 ["USA (Schulen)","EdTech, Bildungsdaten","[0:47]"],["Österreich","E-ID im Alltag","[0:48], [1:01]"],
 ["Kanada","Technocracy-Bewegung","[0:52]"],["China / Peking","Kissinger 1971","[0:52]"],
 ["Mars","Musks Technokratie-Idee","[0:55]"],["Berner Hinterland","Herkunft der Musks laut ihm ❓","[0:56]"],
 ["Winterthur, Bellagio","Club of Rome","[1:08]"],["New York (UN)","Rockefeller-Grundstück","[1:12]"],
 ["Afrika / Jemen","WFP-Biometrie","[1:11]"],["Mexiko","Reise zu Above Phone","[1:19]"],
 ["Grönland, Alaska","Technate, Trump","[1:33]"],["Ukraine, Taiwan","Geopolitik","[1:33]"]]
begriffe = [
 ["Polykrise","Bündel gleichzeitiger Krisen; bei ihm sechs Felder","[0:17]"],
 ["Round Table","britisches Netzwerk um Milner, laut Quigley Vorläufer des CFR","[0:19]"],
 ["Fabian Society","britische sozialistische Gesellschaft (1884), schrittweiser Ansatz","[0:26]"],
 ["Eugenik","Lehre von der „Verbesserung“ des Erbguts einer Bevölkerung","[0:29–0:31]"],
 ["Transhumanismus / biodigitale Konvergenz","Überwindung menschlicher Grenzen durch Technik; bei ihm Fortsetzung der Eugenik","[0:32]"],
 ["Bezahlkarte","Guthabenkarte statt Bargeld für Asylbewerber (Gesetz 2024)","[0:35]"],
 ["Replacement Migration","UN-Rechenszenarien 2000 zu Zuwanderung bei Alterung","[0:35]"],
 ["Biofeudalismus","sein Begriff für die Monetarisierung der Gemeingüter","[0:41]"],
 ["30×30","Ziel, bis 2030 30 % der Land- und Meeresflächen zu schützen","[0:41]"],
 ["Tokenisierung","digitale Abbildung eines Werts als Token (z. B. auf Blockchain)","[0:41]"],
 ["CBDC / Stablecoin","digitales Zentralbankgeld / an Währung gekoppelte Kryptomünze","[0:43]"],
 ["Unified (Universal) Ledger","BIZ-Konzept einer gemeinsamen programmierbaren Plattform","[0:44]"],
 ["Human Capital Performance Bond / Social Impact Bond","Finanzierung, deren Rendite an soziale Ergebnisse gekoppelt ist","[0:43], [0:46]"],
 ["EdTech","Bildungstechnik, Lernsoftware","[0:47]"],
 ["Natural Asset Company","Unternehmen, das Naturwerte über Eigenkapital in Erträge umwandelt","[0:49]"],
 ["Debt-for-Nature Swap","Schuldenerleichterung gegen Naturschutzzusagen","[0:49]"],
 ["Technokratie / Technate","Herrschaft von Technikern; Technate = geplanter nordamerikanischer Großraum","[0:51], [1:33]"],
 ["Energiezertifikat","geplantes Technokratie-Zahlungsmittel nach Energieaufwand","[0:53]"],
 ["E-ID / EUDI-Wallet","elektronische Identität; EU-Brieftasche für Ausweis und Nachweise","[0:48], [0:59]"],
 ["Keylogging","Mitschneiden von Tasteneingaben","[0:59]"],
 ["LEO / VLEO","niedrige / sehr niedrige Erdumlaufbahn","[1:02]"],
 ["Starshield","staatliche/militärische Satellitensparte von SpaceX","[1:02]"],
 ["In-Q-Tel","Wagniskapitalfirma der CIA (1999)","[1:05]"],
 ["LifeLog","DARPA-Projekt zur Erfassung des gesamten Lebens","[1:05]"],
 ["Public-private Partnership","Zusammenarbeit von Staat und Unternehmen","[1:07]"],
 ["SDG 16.9","UN-Unterziel: rechtliche Identität für alle, Geburtsregistrierung","[1:11]"],
 ["Kognitive Kriegsführung","Beeinflussung von Wahrnehmung und Entscheidungen des Gegners","[1:13]"],
 ["Smart Dust","winzige vernetzte Sensoren (MEMS)","[1:14]"],
 ["Kognitive Souveränität","sein Begriff: eigenständiges Urteilen","[1:18]"],
 ["Smombie","Smartphone + Zombie","[1:12]"]]
zahlen = [
 ["Seiten „Tragedy and Hope“","ca. 1.300 (Zitat S. 1247)","[0:19]"],
 ["IQ-Verlust durch Fluorid","2–5 Punkte bei Kindern","[0:23]"],
 ["Ungültige Stimmen Irland","„teilweise mehr als 20 %“; früher max. 4 %","[0:32–0:33]"],
 ["Wahlbeteiligung Irland","40–41 %","[0:33]"],
 ["Entlassungen USA Okt. 2025 „wegen KI“","1,1 Mio.","[0:39]"],
 ["Geschützte europäische Küsten","18 %","[0:41]"],
 ["CO2-Budget pro Person (TV-Experte)","ca. 1.500 kg","[0:42]"],
 ["UN-Mitgliedstaaten","193","[0:42]"],
 ["Mitglieder Technocracy Inc.","½ Mio.","[0:52]"],
 ["Automatisierter Datenverkehr","≥ 70 %; Social Media ≥ 85 %","[0:57]"],
 ["Smartphones mit Android/iOS","98 %","[0:57]"],
 ["Tägliche Bildschirmzeit 16–64 J.","6 Std. 58 Min.","[0:58]"],
 ["Aufmerksamkeitsspanne","16–18 s → 8–11 s seit 2007","[0:58]"],
 ["Österreicher mit E-ID","50 %","[1:01]"],
 ["UN-Unterorganisationen","72","[1:10]"],
 ["„Superclass“","7.000–10.000 Personen","[1:23]"],
 ["Austritte der USA","66 Organisationen","[1:32]"]]
zeitreiter = [
 {"typ":"zeitachse","titel":"📅 Zeitachse – Ereignisse, die im Vortrag vorkommen","eintraege":zeit},
 {"typ":"tabelle","kopf":["👤 Person","Wer / was","Rolle im Vortrag","Fundstelle"],"zeilen":personen},
 {"typ":"tabelle","kopf":["🗺️ Ort","Rolle","Fundstelle"],"zeilen":orte},
 {"typ":"tabelle","kopf":["📖 Begriff","Erklärung","Fundstelle"],"zeilen":begriffe},
 {"typ":"tabelle","kopf":["📊 Zahl im Vortrag","Angabe","Fundstelle"],"zeilen":zahlen}]

# ---------- Reiter 4: Abgleich ----------
AB = [
 ["Quigley: Die beiden Parteien „sollten nahezu identisch sein“ (S. 1247) [0:20]","Der Satz steht in „Tragedy and Hope“ (1966, nicht 1974). Quigley gibt dort wieder, wie die Parteien aus Sicht dieser Denkschule sein sollten; ob er damit eine geheime Absprache belegt oder eine Meinung beschreibt, ist Deutungssache.",Q['quigley']],
 ["Bernays, „Propaganda“, Kap. 1: „unsichtbare Regierung“ als wahre herrschende Macht [0:21]","Das Zitat steht so im ersten Kapitel des Buches von 1928. Den Satz „eine Lüge muss man nur oft genug wiederholen“ enthält das Buch nicht; es beschreibt aber, dass Wiederholung Überzeugung erzeuge. Der Ivory-Seifen-Schnitzwettbewerb ist im Buch beschrieben.",Q['bernays']],
 ["Bernays habe für Alcoa Fluorid in Zahnpasta gebracht [0:23]","Im Buch „Propaganda“ kommt Fluorid nicht vor. Belegt ist: Alcoa-Chemiker fanden 1930 hohe Fluoridwerte im Wasser von Bauxite (Arkansas); Alcoa lieferte Natriumfluorid aus der Aluminiumproduktion an Wasserwerke; die Trinkwasserfluoridierung begann 1945 in Grand Rapids. Eine Rolle Bernays' nennt der Artikel nicht ❓.",Q['bernays']+" · "+Q['origins']],
 ["US-Gericht „Anfang 25 höchstrichterlich“: Fluorid senke den IQ von Kindern um 2–5 Punkte [0:23]","Ein Bundesbezirksgericht (N.D. California) entschied im September 2024 im Fall Food & Water Watch v. EPA, dass Trinkwasserfluoridierung mit 0,7 mg/L ein „unreasonable risk“ für den IQ darstelle und die EPA reagieren müsse – ohne festzustellen, dass Fluoridierung die Gesundheit sicher schädigt; es ging um Trinkwasser, nicht um Zahnpasta. Die NTP-Monographie (08/2024) sieht mit mittlerer Sicherheit einen Zusammenhang bei über 1,5 mg/L; für 0,7 mg/L reichten die Daten nicht.",Q['urteil']+" · "+Q['ntp']],
 ["Man solle keine Zahnpasta mit Fluorid benutzen [0:23]","Fachstellen in Deutschland empfehlen Fluorid-Zahnpasta in altersgerechter Menge: Netzwerk Gesund ins Leben (2021) z. B. ab 12 Monaten zweimal täglich eine reiskorngroße Menge mit 1.000 ppm; das BfR (2018) rät, Fluorid-Tabletten wegzulassen, sobald mit Fluorid-Zahnpasta geputzt wird. Cochrane (2019): Zahnpasta mit 1.000–1.250 ppm senkt Karies bei Kindern gegenüber Placebo. Bei Fragen: Zahnarzt- oder Kinderarztpraxis.",Q['netzwerk']+" · "+Q['bfr']+" · "+Q['cochrane']],
 ["Wilson nenne eine allgegenwärtige Macht, vor der Geschäftsleute sich fürchten [0:24]","Der Satz steht in Kapitel I von „The New Freedom“ (1913). Wilson benennt die Macht nicht; im Zusammenhang geht es um große Trusts und Zugang zu Kredit.",Q['wilson']],
 ["Fabian Society: „Wappen“ Wolf im Schafspelz; alle Labour-Premiers Mitglied [0:26]","Der Wolf im Schafspelz ist ein Emblem auf dem „Fabian Window“ (Entwurf Shaw 1910, heute LSE) als Sinnbild des schrittweisen Vorgehens; ein offizielles Wappen ist nicht belegt. Die Society war 1900 Gründungsorganisation des Labour Representation Committee; laut eigener Angabe waren alle Labour-Premierminister Fabianer.",Q['fwin']+" · "+Q['fabian']],
 ["Moses Hess: „Rom und Jerusalem“ 1860, Gründer der Rheinischen Zeitung, Marx-Prägung [0:27–0:28]","Hess (geb. 1812 in Bonn) war Journalist und Paris-Korrespondent der Rheinischen Zeitung (1842–43) und prägte Marx' frühes Denken; „Rom und Jerusalem“ erschien 1862 und gilt als früher zionistischer Text. Marx verspottete Hess' Sozialismus später im Manifest (1848). Grab: zunächst Köln-Deutz, 1961 nach Israel überführt; ein von der SPD bezahlter Grabstein und ein Bonner Denkmal sind ❓ nicht geprüft.",Q['hess']+" · "+Q['hessw']],
 ["Sanger, Planned Parenthood, Gates Sr., Pro Familia [0:29]","Sanger gründete die Organisationen, aus denen Planned Parenthood und die International Planned Parenthood Federation hervorgingen. William H. Gates Sr. saß im Vorstand von Planned Parenthood. Pro Familia ist Mitglied der IPPF; eine Gründung durch Sanger selbst ❓ nicht belegt.",Q['sanger']+" · "+Q['gates']],
 ["Guterres war Chef der Sozialistischen Internationale [0:30]","Stimmt: Präsident der Sozialistischen Internationale 1999–2005.",Q['guterres']],
 ["Huxley: Eugenik-Direktor, schrieb das UNESCO-Gründungsdokument, wollte Eugenik in Transhumanismus umbenennen [0:31–0:32]","Huxley war 1946 erster UNESCO-Generaldirektor und Vizepräsident der Eugenics Society; seine Schrift von 1946 enthielt eugenische Vorschläge, wurde aber von der Vorbereitungskommission als persönliche Ansicht zurückgewiesen. Den Begriff Transhumanismus machte er 1957 in einem Aufsatz bekannt.",Q['huxley']+" · "+Q['trans']],
 ["„Eugenics Review“ heißt heute „Journal of Biosocial Science“ [0:31]","Stimmt: Die Zeitschrift setzt seit 1969 die „Eugenics Review“ (1909–1968) fort und erscheint bei Cambridge University Press.",Q['jbs']],
 ["Irland Okt. 2025: über 20 % ungültig, 40–41 % Beteiligung, Regierung nicht bildbar [0:33]","Präsidentschaftswahl 24.10.2025: Beteiligung 45,8 %, ungültig 213.738 Stimmen = 12,9 % (Rekord; 2018: 1,2 %; 1945: 4,4 %). Gewählt wurde die Präsidentin (Catherine Connolly, 63,4 %), keine Regierung.",Q['rte']+" · "+Q['iepres']],
 ["UN-Bericht „Replacement Migration“ (2000) habe Migrantenzahlen bis 2025 vorausgesagt [0:35]","Der Bericht rechnet sechs Szenarien für 2000–2050 und betont, sie seien keine Empfehlungen. Für Deutschland: konstante Erwerbsbevölkerung bräuchte im Schnitt 487.000 Zuwanderer pro Jahr. Tatsächlicher Wanderungssaldo laut Destatis z. B. 2015: 1.139.402, 2022: 1.462.089, 2024: 430.183.",Q['repl']+" · "+Q['wand']],
 ["Bezahlkarte als Vorläufer von E-ID und Bürger-Wallet [0:35]","Der Bundestag beschloss am 12.04.2024 eine bundesweite Rechtsgrundlage: Teile der Leistungen als Kartenguthaben, Bargeld eingeschränkt, keine Überweisungen ins Ausland. Eine technische Verbindung zur EUDI-Wallet ist ❓ nicht belegt.",Q['bezahl']],
 ["USA Okt. 2025: 1,1 Mio. Menschen wegen KI entlassen [0:39]","Challenger: im Oktober 2025 153.074 angekündigte Stellenstreichungen; 1.099.500 von Januar bis Oktober. Mit KI begründet: 31.039 im Oktober, 48.414 im Jahr; häufigster Jahresgrund: „DOGE Impact“ (293.753).",Q['chall']],
 ["Insolvenzen steigen massiv [0:39]","Unternehmensinsolvenzen in Deutschland: 2023: 17.814, 2024: 21.812, 2025: 24.064 – höchster Stand seit 2014 (24.085), unter dem Krisenjahr 2009 (32.687).",Q['insol']+" · "+Q['insol25']],
 ["„30×30“ heiße Privatisierung der Gemeingüter [0:41]","Ziel 3 des Kunming-Montreal-Rahmens (Dez. 2022) sieht vor, 30 % der Land- und Meeresflächen bis 2030 wirksam zu schützen, unter Achtung indigener Rechte; eine Eigentumsübertragung nennt der Zieltext nicht. Börsennotierte „Natural Asset Companies“ scheiterten in den USA: Die NYSE zog ihren Antrag im Januar 2024 nach Widerstand zurück.",Q['gbf']+" · "+Q['nac']],
 ["WEF-Bericht Sept. 2025: NACs, Debt-for-Nature Swaps, Zahlungen für Ökosystemleistungen, interne Bepreisung [0:49]","Stimmt: „Finance Solutions for Nature“ (WEF mit McKinsey) nennt zehn Modelle, darunter diese vier; Beispiel für einen Swap: Barbados 2024. Seine Folgerung (Mittelstand ruiniert, Steuerzahler zahlt) ist seine Deutung.",Q['wef']],
 ["Bundestag Feb. 2025: drastische CO2-Preiserhöhung im Windschatten der Migrationsdebatte [0:50]","Am 30.01.2025 beschloss der Bundestag die TEHG-Novelle zur Umsetzung der EU-Emissionshandelsrichtlinie (u. a. Seeverkehr). Die nationalen Festpreise standen schon fest: 25 € (2021), 30 € (2022/23), 45 € (2024), 55 € (2025) je Tonne.",Q['tehg']+" · "+Q['dehst']],
 ["BIZ „Universal Ledger“; Carstens habe Kontrolle offen erklärt [0:44–0:45]","Die BIZ stellte am 20.06.2023 das „unified ledger“ als Konzept vor (tokenisiertes Zentralbankgeld und Einlagen auf einer Plattform), nicht als laufendes System. Carstens sagte 2020 auf einem IWF-Panel, bei einer CBDC habe die Zentralbank „absolute control on the rules and regulations“. Sperrlisten für Bücher oder CO2-Budgets für Einkäufe nennt die BIZ nicht.",Q['bis']+" · "+Q['carst']+" · "+Q['imfpanel']],
 ["E-ID in Deutschland Ende 2026/Anfang 2027; wer sie verweigert, verliert Zugang zu Leistungen [0:48], [1:25]","EUDI-Wallet nach Verordnung (EU) 2024/1183; Deutschland plant den Start am 02.01.2027. Die Nutzung ist freiwillig, Benachteiligung von Nichtnutzern ist untersagt (Art. 5a Abs. 15); Banken und sehr große Plattformen müssen sie akzeptieren. netzpolitik.org verweist auf Druck durch geplante Altersprüfungen für soziale Medien.",Q['eudi']],
 ["Österreich: 50 % haben die E-ID; ohne sie keine Förderung, keine Noteneingabe [1:01]","ID Austria: rund 4,8 Mio. Registrierungen (Dezember 2025). Ob Förderanträge oder Lehrerportale ausschließlich mit ID Austria möglich sind, ❓ nicht geprüft.",Q['idat']],
 ["Musks Großvater leitete Technocracy Inc. in Kanada; Bewegung mit ½ Mio. Mitgliedern [0:52]","Joshua Haldeman war 1936–1941 eine Führungsfigur der Bewegung in Kanada und wurde 1940 nach dem Verbot angeklagt. CBC nennt „Hunderttausende“ Interessierte, keine genaue Mitgliederzahl.",Q['techno']],
 ["Kissinger reiste nicht aus kulturellen Gründen nach China, sondern im Auftrag Rockefellers [0:52–0:53]","Laut US-Außenministerium reiste Kissinger 1971 zweimal als Nationaler Sicherheitsberater nach Peking, um die Normalisierung vorzubereiten. Ein Auftrag der Rockefellers ist in dieser Quelle nicht belegt [seine Sicht].",Q['kiss']],
 ["70 % des Datenverkehrs automatisch, 98 % Android/iOS, 6 Std. 58 Min. am Gerät [0:57–0:58]","Imperva: 51 % des Webverkehrs 2024 automatisiert (37 % bösartige Bots). StatCounter (Okt. 2026): Android 72,36 %, iOS 27,61 %. Online-Zeit weltweit Q3 2024: 6 Std. 38 Min. (alle Geräte, GWI).",Q['bots']+" · "+Q['os']+" · "+Q['online']],
 ["Aufmerksamkeit seit 2007 von 16–18 auf 8–11 Sekunden „biologisch messbar“ gesunken [0:58]","Die verbreitete 8-Sekunden-Zahl (Microsoft Kanada 2015) führte eine BBC-Recherche 2017 auf Statistic Brain zurück, das keine Studie nennen konnte. Eine biologische Messung ist nicht belegt.",Q['acht']],
 ["Starlink umhüllt die Erde; Starshield mit Laser und gerichteter Energie [1:02]","10.020 aktive Starlink-Satelliten am 17.03.2026, rund zwei Drittel aller aktiven Satelliten. Starshield: Erdbeobachtung, Kommunikation, gehostete Nutzlasten, Laser-Kommunikation mit Starlink; „directed energy“ nennt SpaceX dort nicht.",Q['star']+" · "+Q['shield']],
 ["xAI wird vom Pentagon und anderen US-Behörden genutzt [1:03]","Stimmt im Kern: Das Pentagon (CDAO) vergab am 14.07.2025 Verträge bis je 200 Mio. $ an xAI, OpenAI, Anthropic und Google; „Grok for Government“ können Bundesbehörden über die GSA beziehen.",Q['xai']],
 ["LifeLog endete am Tag des Facebook-Starts; Tech-Konzerne mit Geheimdienst-Startkapital [1:05–1:06]","LifeLog wurde am 04.02.2004 eingestellt, dem Starttag von Facebook; eine Beteiligung von DARPA oder Diensten an Facebook ist laut WHYY nicht belegt. Belegt ist die In-Q-Tel-Investition in Keyhole (2003), die Google 2004 kaufte (Google Earth).",Q['lifelog']+" · "+Q['cia']],
 ["Google habe „Don't be evil“ gestrichen [1:06]","2018 wurde das Motto im Verhaltenskodex weitgehend entfernt; es steht nur noch im letzten Satz.",Q['google']],
 ["IWF und Weltbank sind Teil der UN; SDG 16.9 sei die E-ID; WFP zwinge zur ID [1:10–1:11]","IWF und Weltbankgruppe sind Sonderorganisationen im UN-System (eigenständig, über Abkommen verbunden). Ziel 16.9: „rechtliche Identität für alle, einschließlich Geburtsregistrierung“; der Indikator misst registrierte Geburten, digitale ID wird nicht genannt. Das WFP verlangte 2019 im Jemen biometrische Registrierung, um Zweckentfremdung zu verhindern.",Q['unsys']+" · "+Q['sdg']+" · "+Q['wfp']],
 ["NATO: kognitive Kriegsführung als sechste Dimension [1:13]","Der NATO-Tagungsband (Bordeaux, 21.06.2021) beschreibt kognitive Kriegsführung als Beeinflussung von Wahrnehmung und Entscheidungen des Gegners und diskutiert eine sechste („kognitive“ bzw. „menschliche“) Domäne als offene Frage.",Q['nato']],
 ["Smart Dust injizierbar, liest das Gehirn; Wells-Fargo-Patent Juni 2022 [1:15–1:16]","Patent US 11,354,666 (Wells Fargo, erteilt 07.06.2022): MEMS-Sensorschwarm sammelt biometrische Daten zur Zahlungsfreigabe – ein Patent, kein belegtes Produkt im Einsatz. Ein unbemerkt einatembarer oder injizierbarer Staub zum Auslesen des Gehirns ist nicht belegt; „Neurosform 3“ ❓ nicht gefunden.",Q['patent']],
 ["„Superclass“: 7.000 bis 10.000 Menschen steuern die Welt [1:23]","Rothkopf (2008) spricht von rund 6.000 Personen mit großem Einfluss.",Q['superc']],
]

WEG=("Wilson nenne","Guterres war","„Eugenics Review“ heißt","Google habe","„Superclass“:","Sanger, Planned","Insolvenzen steigen","xAI wird","WEF-Bericht Sept.")
AB=[z for z in AB if not z[0].startswith(WEG)]
kurs_insol = {"typ":"kurs","id":"kontrolle-insolvenzen","titel":"📈 Unternehmensinsolvenzen in Deutschland","reihen":[{"name":"Unternehmensinsolvenzen","kurz":"Fälle","einheit":"Fälle","dez":0,"hoeherGut":False,
  "punkte":[[2010,31998],[2011,30099],[2012,28297],[2013,25995],[2014,24085],[2015,23101],[2016,21518],[2017,20093],[2018,19302],[2019,18749],[2020,15841],[2021,13993],[2022,14590],[2023,17814],[2024,21812],[2025,24064]]}],
  "hoeherGut":False,"vergleich":False,"quelle":Q['insol']+" · "+Q['insol25']+", Stand 03/2026",
  "hinweis":"Bezug zum Vortrag [0:39]: „massiv steigende Insolvenzzahlen“. Seit 2021 steigen die Zahlen jedes Jahr; 2025 höchster Stand seit 2014, aber unter den Werten von 2010–2013."}
kurs_irl = {"typ":"kurs","id":"kontrolle-irland","titel":"📈 Irland: Präsidentschaftswahlen – Beteiligung und ungültige Stimmen","reihen":[
  {"name":"Wahlbeteiligung","kurz":"Beteiligung","einheit":"%","dez":1,"hoeherGut":True,"punkte":[[1945,63.0],[1959,58.4],[1966,65.3],[1973,62.2],[1990,64.1],[1997,46.7],[2011,56.1],[2018,43.9],[2025,45.8]]},
  {"name":"Ungültige Stimmen","kurz":"ungültig","einheit":"%","dez":1,"hoeherGut":False,"punkte":[[1945,4.4],[1959,2.5],[1966,0.9],[1973,0.6],[1990,0.6],[1997,0.8],[2011,1.0],[2018,1.2],[2025,12.9]]}],
  "hoeherGut":None,"vergleich":True,"quelle":Q['iepres']+" · "+Q['rte']+", Stand 12/2025",
  "hinweis":"Bezug zum Vortrag [0:33]: Er nennt über 20 % ungültig, früher höchstens 4 % „vor 80 Jahren“, und 40–41 % Beteiligung. Der frühere Höchstwert 4,4 % (1945) passt; 2025 waren es 12,9 % bei 45,8 % Beteiligung. Nur umkämpfte Wahlen."}
kurs_wand = {"typ":"kurs","id":"kontrolle-wanderung","titel":"📈 Wanderungssaldo Deutschlands (Zuzüge minus Fortzüge)","reihen":[{"name":"Wanderungssaldo","kurz":"Saldo","einheit":"Personen","dez":0,"hoeherGut":None,
  "punkte":[[2010,127677],[2011,279330],[2012,368945],[2013,428607],[2014,550483],[2015,1139402],[2016,499944],[2017,416080],[2018,399680],[2019,327060],[2020,220251],[2021,329163],[2022,1462089],[2023,662964],[2024,430183],[2025,235000]]}],
  "hoeherGut":None,"vergleich":False,"quelle":Q['wand']+", Stand 2026 (2025 vorläufig, gerundet)",
  "hinweis":"Bezug zum Vortrag [0:35]: UN-Bericht „Replacement Migration“ (2000). Dessen Szenario „konstante Erwerbsbevölkerung“ rechnete für Deutschland mit im Schnitt 487.000 pro Jahr (2000–2050) – eine Rechnung, keine Prognose. Spitzen 2015 (Asyl) und 2022 (Ukraine)."}
balk_co2 = {"typ":"balken","titel":"📊 Nationaler CO2-Preis (BEHG) für Heizen und Tanken, € je Tonne","einheit":"€/t","dez":0,"zeilen":[["2021",25],["2022",30],["2023",30],["2024",45],["2025",55]],
  "quelle":Q['dehst']+", Stand 2025","hinweis":"Bezug zum Vortrag [0:50]: „drastische CO2-Preiserhöhung“ Februar 2025. Die Preise der Festpreisphase waren gesetzlich vorab festgelegt; ab 2027 gilt der EU-Emissionshandel ETS 2."}
balk_os = {"typ":"balken","titel":"📊 Mobile Betriebssysteme weltweit (Anteil an Seitenaufrufen)","einheit":"%","dez":2,"zeilen":[["Android",72.36],["iOS",27.61],["Linux",0.01],["KaiOS",0.01]],
  "quelle":Q['os']+", Stand Oktober 2026","hinweis":"Bezug zum Vortrag [0:57]: „98 % laufen auf Android und iOS“. Laut StatCounter sind es zusammen 99,97 %."}
balk_ch = {"typ":"balken","titel":"📊 USA, Oktober 2025: angekündigte Stellenstreichungen nach Grund","einheit":"Stellen","dez":0,"zeilen":[["Kostensenkung",50437],["Künstliche Intelligenz",31039],["Markt- und Wirtschaftslage",21104]],
  "quelle":Q['chall']+", Stand 06.11.2025","hinweis":"Bezug zum Vortrag [0:39]: „1,1 Millionen … aufgrund von KI“. Insgesamt im Oktober 153.074; 1.099.500 ist die Summe Januar–Oktober über alle Gründe."}
vergl = {"typ":"vergleich","titel":"⚖️ Zahlen im Vortrag und Daten nebeneinander","la":"Im Vortrag genannt","lb":"Daten laut Quelle","zeilen":[
  {"n":"Ungültige Stimmen Irland 2025","a":20,"b":12.9,"einheit":"%","f":"[0:33]","q":Q['rte']},
  {"n":"Wahlbeteiligung Irland 2025","a":40.5,"b":45.8,"einheit":"%","f":"[0:33]","q":Q['rte']},
  {"n":"US-Stellenabbau wegen KI (Okt. 2025)","a":1100000,"b":31039,"einheit":"Stellen","f":"[0:39]","q":Q['chall']},
  {"n":"Automatisierter Anteil am Datenverkehr","a":70,"b":51,"einheit":"%","f":"[0:57]","q":Q['bots']},
  {"n":"Smartphones mit Android oder iOS","a":98,"b":99.97,"einheit":"%","f":"[0:57]","q":Q['os']},
  {"n":"Tägliche Online-Zeit (Std.)","a":6.97,"b":6.63,"einheit":"Std.","f":"[0:58]","q":Q['online']},
  {"n":"Personen der „Superclass“","a":7000,"b":6000,"einheit":"Personen","f":"[1:23]","q":Q['superc']}]}

abgleich = [
 {"typ":"text","text":"Neutraler Abgleich: links die Aussage im Vortrag, rechts die gängige Darstellung bzw. Daten mit Quelle. Die Bewertung bleibt dem Leser."},
 {"typ":"tabelle","kopf":["Aussage im Gespräch","Gängige Darstellung (Mainstream) / Daten 📚","Quelle"],"stapel":True,"zeilen":AB},
 kurs_insol, kurs_irl, kurs_wand, balk_co2, balk_ch, balk_os, vergl,
 {"typ":"abschnitt","titel":"🧩 Spannungen im Gespräch","liste":[
  "Der Moderator hält dagegen, die Menschheit lebe gemessen an Kriegstoten in einer der friedlichsten Zeiten; Regenauer nennt diesen Blick „veraltet“ und verweist auf kognitive Kriegsführung [1:28–1:31].",
  "Ein Zuhörer fragt, wie man nicht deprimiert nach Hause gehe; Regenauer: glücklich leben, aber „wutentbrannt“ aktiv werden [1:29–1:30].",
  "Er sagt, Namen zu nennen sei „unseriös“, zählt aber Gruppen wie Finanzkartelle, Technokraten und „Zionisten“ auf [1:22–1:23].",
  "Er ruft dazu auf, ihm nichts zu glauben und alles nachzuprüfen [0:16], [1:17] – mehrere Zahlen im Vortrag weichen von den Quellen ab (Abgleich).",
  "Ein Zuhörer fragt, ob Trumps Austritte nicht zeigten, dass „die“ uneins seien; Regenauer: Gerangel ja, Ziel aber eine multipolare Ordnung [1:31–1:33]."]},
 {"typ":"abschnitt","titel":"💡 Was man mitnehmen kann","liste":[
  "Viele Dokumente, die er zeigt, gibt es tatsächlich (Quigley, Bernays, Wilson, UN-Bericht 2000, WEF-Bericht 2025, BIZ-Konzept, Wells-Fargo-Patent, NATO-Tagungsband) – die Deutung als gemeinsamer Plan ist seine Sicht.",
  "Bei Zahlen lohnt der Blick auf die Quelle: Irland 12,9 % statt über 20 % ungültig; 31.039 statt 1,1 Mio. KI-Entlassungen im Oktober 2025.",
  "Zur EUDI-Wallet ist rechtlich festgelegt, dass sie freiwillig ist; ob das in der Praxis so bleibt, ist auch unter Datenschützern ein Thema.",
  "Zu Fluorid: Das US-Urteil betrifft Trinkwasser, nicht Zahnpasta; deutsche Fachstellen empfehlen Fluorid-Zahnpasta in altersgerechter Menge.",
  "Seine praktischen Tipps (eigene Informationswege, andere Software) lassen sich unabhängig von seiner Gesamtdeutung prüfen."]},
 {"typ":"abschnitt","titel":"❓ Offen","liste":[
  "Wann wurde das Video veröffentlicht, und ist der Moderator Roland Tichy?",
  "Welcher Bericht von 1944 nennt die EU ein „viertes Reich“ [0:15]?",
  "Woher stammt die Angabe zu Bernays und Alcoa [0:23]?",
  "Welche Sendung und welcher Experte nannten ein CO2-Budget von ca. 1.500 kg [0:42]? Woher die 18 % geschützten Küsten [0:41]?",
  "Was ist „Green Plus“ in Südamerika [0:41] und „Neurosform 3“ [1:15]?",
  "Wo steht Smart Dust auf der Webseite des Bundesinnenministeriums [1:14]?",
  "Sind Fördermittel für Landwirte in Österreich ohne ID Austria (z. B. über Bevollmächtigte) erreichbar [1:01]?"]},
 {"typ":"abschnitt","titel":"🔎 Weiter recherchieren","liste":[
  "Primärtexte: Quigley „Tragedy and Hope“ (1966), Bernays „Propaganda“ (1928), Wilson „The New Freedom“ (1913), UN „Replacement Migration“ (2000).",
  "Verordnung (EU) 2024/1183 (eIDAS 2.0), Art. 5a; Zeitplan der deutschen EUDI-Wallet.",
  "BIZ Annual Economic Report 2023, Kapitel III („unified ledger“); WEF „Finance Solutions for Nature“ (2025).",
  "Food & Water Watch v. EPA (N.D. Cal. 2024); NTP-Monographie Fluorid (2024).",
  "Suchbegriffe: „Technocracy Incorporated Haldeman“, „DARPA LifeLog“, „In-Q-Tel Keyhole“, „NATO cognitive warfare Bordeaux 2021“.",
  "Querverweise: {{a:ungeskriptet-regenauer|Regenauer bei {ungeskriptet}}}, {{w:geld|Geld}}, {{w:politik|Politik}}, {{w:deutschland|Deutschland in Zahlen}}, {{a:krall|Markus Krall}} (Geldsystem)."]},
]

reiter = [
 {"id":K,"titel":G+": Überblick","bloecke":uberblick},
 {"id":K+"ab","titel":G+": Vortrag im Detail","bloecke":detail},
 {"id":K+"zeit","titel":G+": Zeitachse & Verzeichnisse","bloecke":zeitreiter},
 {"id":K+"abgleich","titel":G+": Abgleich & Daten","bloecke":abgleich}]
dia = sum(1 for r in reiter for b in r["bloecke"] if b["typ"] in ("kurs","balken","vergleich","illu"))
uberblick[0]["kacheln"] = [[str(len(A)),"Abschnitte"],["10","Kernaussagen"],[str(len(AB)),"Abgleich-Punkte"],[str(len(zeit)),"Zeitachse"],[str(dia),"Skizzen & Diagramme"]]

quellen = [["Video: "+TITEL+" – BENU Solutions (YouTube)", URL]]
for v in Q.values():
    t, u = v[1:].split("](", 1); quellen.append([t, u[:-1]])
out = {"k":K,"gast":GAST,"reiter":reiter,
 "folgen_zeile":["2026 ❓","Tom-Oliver Regenauer (Autor, Verleger)",TITEL,"Polykrise, Demokratie, Migration, Geld, Technokratie, UN, E-ID","{{a:regenauer-kontrolle|hier: Bis 2030}}","[ansehen](%s)"%URL],
 "baum_ast":{"gruppe":"🌐 Macht, Geld & Überwachung","t":"👤 Regenauer – Polykrise, E-ID, Technokratie"},
 "neu":{"d":"2026-11-12","t":"Regenauer – Bis 2030 Totale Kontrolle?","k":"Kongressvortrag zu Polykrise, Technokratie und E-ID – %d Abschnitte, %d Abgleich-Punkte mit Quellen, %d Diagramme." % (len(A), len(AB), sum(1 for b in abgleich if b['typ'] in ('kurs','balken','vergleich'))),"h":"#a-regenauer-kontrolle","art":"Video"},
 "quellen":quellen,
 "web":[["Tom-Oliver Regenauer – Blog und Bücher","https://www.regenauer.press"]]}
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"folge.json"),"w"), ensure_ascii=False, indent=1)
print("Abschnitte",len(A),"Abgleich",len(AB),"Zeitachse",len(zeit),"Diagramme+Illu",dia)
