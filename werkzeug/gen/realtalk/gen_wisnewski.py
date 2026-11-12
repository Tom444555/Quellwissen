# -*- coding: utf-8 -*-
# Erzeugt folge.json für „25 Jahre 9/11: Warum die offizielle Geschichte NICHT stimmen kann | Gerhard Wisnewski“
# (REALTALK MEDIA, K = wisnewski, Sammelstelle A-12 realtalk)
import json, os
K = 'wisnewski'; G = 'Wisnewski'
URL = 'https://www.youtube.com/watch?v=1B_BqV5C88E'
TITEL = '25 Jahre 9/11: Warum die offizielle Geschichte NICHT stimmen kann | Gerhard Wisnewski'
GAST = 'Gerhard Wisnewski'
KANAL = 'REALTALK MEDIA'
DATUM = '2026 ❓'
DAUER = '2 Std. 4 Min.'

# ---------- Quellen (per Suche gefunden bzw. gelesen) ----------
Q = dict(
 cr1='[9/11 Commission Report, Kapitel 1.2 „Improvising a Homeland Defense“ (Textabschrift)](https://911.gnu-designs.com/Chapter_1.2.html)',
 oig='[US-Verkehrsministerium, Generalinspekteur: Results of OIG Investigation of 9/11 Commission Staff Referral, CC-2006-085 (31.08.2006, PDF, Archivkopie)](https://webarchive.library.unt.edu/web/20161103193523/https://www.oig.dot.gov/sites/default/files/cc2006085.pdf)',
 nist7='[NIST: Questions and Answers about the NIST WTC 7 Investigation](https://nist.gov/world-trade-center-investigation/study-faqs/wtc-7-investigation)',
 uaf='[University of Alaska Fairbanks (Hulsey u. a.): A Structural Reevaluation of the Collapse of World Trade Center 7 – Kurzfassung (PDF, auf der Seite von AE911Truth)](https://casite-398799.cloudaccess.net/images/PDFs/Abstract-A-Structural-Reevaluation-of-the-Collapse-of-World-Trade-Center-7.pdf)',
 nistrfc='[NIST: Antwort auf den Antrag auf Berichtigung 2020-001 (PDF, Kopie auf der Seite von AE911Truth)](https://casite-398799.cloudaccess.net/images/PDFs/NIST-Response-2020-001.pdf)',
 klage='[US-Bezirksgericht D.C.: Memorandum Opinion, AE911Truth u. a. gegen NIST (02.08.2022, PDF, Kopie auf der Seite von AE911Truth)](https://casite-398799.cloudaccess.net/images/PDFs/AE_v_NIST_DC_DCT_memorandum_opinion_on_IQA_case_on_Def_MTD_080222.pdf)',
 asce='[ASCE: The Pentagon Building Performance Report (Januar 2003)](https://ascelibrary.com/doi/book/10.1061/9780784406380)',
 asce2='[Government Executive (2003): Structure of Pentagon helped contain 9/11 damage, engineers say](https://govexec.com/federal-news/2003/01/structure-of-pentagon-helped-contain-911-damage-engineers-say/13296)',
 mem='[9/11 Memorial & Museum: Backgrounder 2021 (PDF)](https://www.911memorial.org/sites/default/files/inline-files/Backgrounder%202021.pdf)',
 brown='[Brown University (01.09.2021): Costs of the 20-year war on terror – $8 trillion and 900,000 deaths](https://www.brown.edu/news/2021-09-01/costsofwar)',
 crs='[Congressional Research Service R44381: Intelligence Community Spending – Trends and Issues (08.11.2016)](https://www.everycrsreport.com/files/20161108_R44381_791c6032e3a1942e415553749f62c956b65de279.html)',
 nato='[NATO: Collective defence and Article 5](https://www.nato.int/cps/en/natohq/110496.htm)',
 nato2='[NATO Review (2006): Invoking Article 5](https://www.nato.int/docu/review/articles/2006/06/01/invoking-article-5/index.html)',
 pnac='[Responsible Statecraft (11.09.2021): How 9/11 enabled a preconceived vision of an imperial US foreign policy](https://responsiblestatecraft.org/2021/09/11/how-9-11-enabled-a-preconceived-vision-of-an-imperial-us-foreign-policy/)',
 clark='[Democracy Now! (02.03.2007): Gen. Wesley Clark Weighs Presidential Bid](https://www.democracynow.org/2007/3/2/gen_wesley_clark_weighs_presidential_bid)',
 patriot='[govinfo: Public Law 107-56 (USA PATRIOT Act)](https://www.govinfo.gov/app/details/PLAW-107publ56)',
 patriot2='[govinfo: Remarks on Signing the USA PATRIOT ACT of 2001 (26.10.2001)](https://www.govinfo.gov/content/pkg/WCPD-2001-10-29/html/WCPD-2001-10-29-Pg1550.htm)',
 poll='[NBC News (2006): 9/11 conspiracy theorists multiply (Scripps-Howard/Ohio University)](https://www.nbcnews.com/news/amp/wbna14723997)',
 abc='[ABC News (2002): Were Israelis Detained on Sept. 11 Spies?](https://abcnews.go.com/amp/2020/story?id=123885)',
 wortfeld='[wortfeld.de (08.09.2003): Spiegel and 9/11 – Beyond the buzz](https://www.wortfeld.de/2003/09/spiegel_and_911_beyond_the_buzz/)',
 freitag='[der Freitag (19.09.2003): Einmal Shanksville und zurück](https://www.freitag.de/autoren/konrad-ege/einmal-shanksville-und-zuruck)',
 seiten28='[Source NM (11.09.2021): Declassifying the 9/11 investigation](https://sourcenm.com/2021/09/11/declassifying-the-9-11-investigation/)',
 fbi21='[Al Jazeera (12.09.2021): FBI releases newly declassified record on September 11 attacks](https://www.aljazeera.com/news/2021/9/12/fbi-releases-newly-declassified-record-on-september-11-attacks)',
 eo='[Executive Order 14040 vom 03.09.2021 (Zusammenfassung)](https://visualcompliance.com/newsletter/executive-order-14040-of-september-3-2021-declassification-reviews-of-certain-documents-concerning-the-terrorist-attacks-of-september-11-2001)',
 kean='[JURIST (2008): CIA obstructed 9/11 Commission probe – Kean, Hamilton](https://www.jurist.org/news/2008/01/cia-obstructed-911-commission-probe)',
)

def L(s):  # Markdown-Link -> (Titel, url)
    t, u = s[1:].split('](')
    return [t, u[:-1]]

# ---------- Abschnitte ----------
A = []
def ab(titel, von, bis, th, *liste):
    A.append(dict(titel=titel, von=von, bis=bis, th=th, liste=list(liste)))

ab('🎬 Teaser und Begrüßung bei „Good Morning Germany“', '0:00', '0:02', 'w',
 '**Zusammenfassung:** Das Video beginnt mit Ausschnitten aus dem späteren Gespräch (Shanksville, Humboldt-Universität, „Flüchtlinge von morgen“). Dann begrüßt der Gastgeber zur Sendung „Good Morning Germany“ auf REALTALK MEDIA einen „Aufklärer der ersten Stunde“ zu den Anschlägen vom 11. September 2001, die er zu den größten Terrorakten der letzten „150, wenn nicht 300 Jahre“ zählt.',
 '📌 Wegen technischer Probleme wurde ein Teil neu aufgenommen; der Gastgeber kündigt an, die Angaben von Google Gemini zu Wisnewskis Person durchzugehen [0:02].',
 '📌 Der Gastgeber nennt seinen Namen im Video nicht ❓; er stellt Wisnewski als „Qualitätsjournalist“ vor [0:02].')

ab('🪪 Lebenslauf laut Gemini – und Wisnewskis Korrektur', '0:02', '0:05', 'f',
 '**Zusammenfassung:** Der Gastgeber liest vor, was Gemini über Wisnewski ausgibt: geboren am 30.11.1959 in Krumbach (Schwaben), Schulzeit in Frankfurt am Main, Abitur 1979, Arbeit für Frankfurter Neue Presse und Bild, 1981–1990 Studium der Politikwissenschaft in München, Mitarbeit u. a. bei Abendzeitung, tz, Stern und P.M., seit 1986 freier Buch- und Filmautor, Anfang der 1990er Jahre beim WDR mit Arbeiten zur RAF bekannt geworden, 2003 Ende der Zusammenarbeit, seit 2008 vor allem beim Kopp-Verlag und bei Compact. Wisnewski bestätigt das im Kern.',
 '📌 **Korrektur durch Wisnewski:** Den Grimme-Preis habe nicht er bekommen, sondern der Spielfilm „Das Phantom“ von Regisseur Dennis Gansel, der auf seinem mit zwei Kollegen geschriebenen Buch „Das RAF-Phantom“ beruhte [0:03–0:04].',
 '📌 Er schreibe seit 2003 vor allem im „alternativen Bereich“ und gebe beim Kopp-Verlag die jährliche Buchreihe „verheimlicht – vertuscht – vergessen“ heraus [0:04].',
 '📌 Laut der vorgelesenen Gemini-Antwort sendete der WDR am 20.06.2003 den Film „Aktenzeichen 11.9. ungelöst“ von Wisnewski und Willy Brunner; nach Recherchen des Spiegel, wonach eine Interviewaussage manipuliert worden sei, habe der WDR die Zusammenarbeit beendet. Gemini nennt ihn zudem Vertreter von „Verschwörungstheorien“ – der Gastgeber spricht von „unserem Lieblingswort“ [0:05].',
 '📚 **Ergänzung:** Den Spiegel-Bericht selbst konnte ich nicht im Wortlaut prüfen ❓; belegt ist, dass der Spiegel am 08.09.2003 eine Titelgeschichte über Bücher zum 11. September brachte – siehe Abgleich.')

ab('📺 Warum der WDR die Zusammenarbeit beendete – seine Sicht', '0:05', '0:07', 'f',
 '**Zusammenfassung:** Wisnewski bestätigt die Angaben und deutet sie: Er und sein Kollege hätten mit dem Film in den USA „den amerikanischen Kriegsgrund kaputt“ gemacht, nämlich die offizielle Version. Der Film habe gezeigt, dass in Shanksville „sehr wahrscheinlich kein Flugzeug abgestürzt“ sei, „genauso wenig wie am Pentagon“. Darauf habe eine „Schmutzkampagne“ von Spiegel, Panorama und anderen Medien begonnen; der WDR sei „eingeknickt“.',
 '📌 Er verspricht sich: „zwei andere sollen im Pentagon abgestürzt sein“ – gemeint sind ein Flugzeug am Pentagon und eines bei Shanksville [0:06].',
 '🔗 Der Gastgeber nennt Mathias Bröckers und Andreas von Bülow als weitere Autoren der „ersten Welle“ und kündigt die Veranstaltung an der Humboldt-Universität an [0:07] – ausführlich ab [1:10].',
 '📌 Gastgeber: Mit den Aufklärern sei „ekelerregend“ umgegangen worden [0:07] [seine Sicht].')

ab('🔍 Der Aufwachmoment: Recherche zur „dritten Generation“ der RAF', '0:07', '0:10', 'b',
 '**Zusammenfassung:** Der Gastgeber fragt nach Wisnewskis Wendepunkt als Journalist. Der liegt laut Wisnewski im Jahr 1992: Mit zwei Kollegen habe er zur „dritten Generation“ der RAF recherchiert und die Behörden gefragt, welche Beweise es für die Täterschaft gebe – bei den Morden an Alfred Herrhausen (Deutsche Bank), Detlev Karsten Rohwedder (Treuhand) und dem Diplomaten Gerold von Braunmühl.',
 '📌 Diese Morde seien bis heute nicht aufgeklärt; die Aufklärungsquote bei Mord liege sonst bei 95 %, hier bei 0 % [0:09] [seine Sicht].',
 '📌 Nach dem Buch „Das RAF-Phantom“ habe er neun Jahre „ganz normal“ bei einem populärwissenschaftlichen Magazin gearbeitet; der 11.9.2001 habe ihn „wachgeküsst“, weil er dieselben Mechanismen wie beim „Phantomterrorismus“ wiedererkannt habe – nun auf globaler Ebene, „Behauptungen ohne jeden Beweis“ [0:09].',
 '📚 **Ergänzung:** Gerold von Braunmühl wurde am 10.10.1986, Alfred Herrhausen am 30.11.1989 und Detlev Karsten Rohwedder am 01.04.1991 ermordet; die Taten werden der RAF zugeschrieben, die Täter sind bis heute nicht ermittelt (Daten aus allgemeinen Nachschlagewerken, hier nicht eigens verlinkt).')

ab('🕵️ Generation 9/11, Peter Urbach und die Fahndungsplakate', '0:10', '0:14', 'b',
 '**Zusammenfassung:** Der Gastgeber erzählt, seine Generation sei die „Generation 9/11“; ohne den 11. September hätte er nie eigene Medien gemacht, schon 2005 habe er auf seinem Debütalbum darüber gerappt. Er fragt nach Geheimdiensten in der RAF-Geschichte und nennt Peter Urbach, einen Agenten des Verfassungsschutzes, der nach dem Attentat auf Rudi Dutschke Molotowcocktails geliefert und die Kommune 1 mit Waffen versorgt habe [0:11].',
 '💬 „das war für mich quasi eben das Erweckungserlebnis“ (Wisnewski über die RAF-Recherche) [0:12]',
 '📌 Behörden hätten Fahndungsplakate ohne Beweis aufgehängt – „Phantome“ –, genau wie nach dem 11.9. die Galerie der angeblichen Entführer. Solche Fälschungen und Anschläge seien „ein gängiges Werkzeug der Dienste“ [0:12–0:13] [seine Sicht].',
 '📌 Gastgeber: Wer sich nicht mit deutscher Geschichte befasse, sei politisch „extrem manipulierbar“ [0:14] [seine Sicht].',
 '📚 **Ergänzung:** Dass Peter Urbach als V-Mann des Berliner Verfassungsschutzes in der Berliner linken Szene tätig war, ist in der Fachliteratur beschrieben; Einzelheiten hier nicht geprüft ❓.')

ab('⚓ „Ein neues Pearl Harbor“ – das Strategiepapier und der Kinofilm', '0:14', '0:17', 'c',
 '**Zusammenfassung:** Wisnewski beschreibt eine „Kette“: Schon vor dem 11.9. habe ein regierungsnaher Thinktank, „eine Art Schattenregierung“, ein Strategiepapier für eine neue starke Rolle der USA verfasst. Das könne lange dauern, wenn es nicht ein „katalysatorisches Ereignis“ wie den Angriff auf Pearl Harbor 1941 gebe, der den Kriegseintritt der USA auslöste.',
 '📌 Weil viele Amerikaner mit „Pearl Harbor“ wenig anfangen konnten, sei „im Juli oder so“ 2001 ein Spielfilm über den Angriff herausgebracht worden – als Liebesfilm mit Emotionen und Heldentum, ein „historisches Repetitorium“ [0:16–0:17] [seine Sicht].',
 '💬 „Das wird schon medial alles vorbereitet auf psychologisch“ (Wisnewski) [0:17]',
 '📚 **Ergänzung:** Gemeint ist das Papier „Rebuilding America’s Defenses“ des Project for the New American Century (September 2000) – siehe Abgleich. Der Film „Pearl Harbor“ kam in den USA im Mai 2001 in die Kinos, nicht im Juli ❓ (Datum nicht per Quelle geprüft).')

ab('🔁 7. Oktober, Wesley Clarks Liste und die Täter nach 48 Stunden', '0:17', '0:20', 'c',
 '**Zusammenfassung:** Der Gastgeber fragt, ob es ein Muster sei, dass nach dem 11.9. vom „neuen Pearl Harbor“ und nach dem 7. Oktober vom „neuen 9/11“ gesprochen wurde. Wisnewski nennt das einen „Stafettenlauf“ der Begriffe: Man benutze eingeschliffene Begriffe, die das Publikum verinnerlicht habe [0:18].',
 '📌 Gastgeber: Wesley Clark habe von einem Strategiepapier mit mehreren Stationen berichtet, die letzte sei der Iran; „da wären wir jetzt glaube ich 2026“ [0:18–0:19].',
 '📌 Gastgeber: Einen Tag später habe man Osama bin Laden als Drahtzieher gekannt, innerhalb von 48 Stunden die Täter mit Bildern gezeigt [0:19].',
 '💬 „das kann nur eine Schmierenkomödie sein“ (Wisnewski über die schnelle Benennung) [0:19]',
 '📌 Niemand könne in 12, 24 oder 48 Stunden die Täter eines solchen Anschlags ermitteln; für ihn sei klar gewesen, „dass es alles gelogen“ sei – die Opfer in den Türmen habe es aber „leider gegeben“ [0:19–0:20] [seine Sicht].')

ab('📚 Buchprojekte, „Operation 9/11“ und das Ende des Kalten Kriegs', '0:20', '0:26', 'c',
 '**Zusammenfassung:** Der Gastgeber kündigt eine Folge mit Mathias Bröckers an; Andreas von Bülow stehe wegen seines Alters wohl nicht mehr zur Verfügung. Er selbst arbeite an drei Büchern (Destabilisierung Deutschlands, Schattenseite der Musikindustrie, 11. September) und halte sich mit eigener Analyse zurück. Wisnewski stellt die Neuauflage seines Buchs „Operation 9/11“ vor.',
 '💬 „in Richtung Krieg, Kontrolle und Konfrontation“ (Wisnewski über die Folgen von 9/11) [0:21]',
 '📌 In den 1990ern habe es friedlich ausgesehen: Warschauer Pakt und Sowjetunion aufgelöst, Bücher wie „Das Ende der Geschichte“. Für NATO und Westen sei eine „gewaltige Sinnkrise“ entstanden, weil der Feind weg war; daher habe man sich einen neuen geschaffen – den „Kampf der Kulturen“ bzw. den Krieg gegen den Terror, gemeint gegen Afghanistan, Irak, Libyen, Syrien und Iran [0:21–0:22] [seine Sicht].',
 '📌 „Wir sind jetzt im Irankrieg“; die Agenda werde 25 Jahre danach „abgearbeitet“ [0:22]. Neu im Buch sei ein Kapitel über die Anfänge der Aufklärungsbewegung; 2003 sei das „Großkampfjahr um die Wahrheit“ gewesen [0:22–0:24].',
 '📌 Der Gastgeber fragt: „Wer hat ihn gebaut? Wer hat profitiert?“ – gemeint ist der islamistische Terror [0:25].',
 '📚 **Ergänzung:** „Das Ende der Geschichte“ ist ein Buch von Francis Fukuyama (1992). Den aktuellen Stand eines Kriegs mit Iran 2026 habe ich nicht geprüft ❓.')

ab('🧩 Al-Qaida als „Liste“ und Huntingtons „Kampf der Kulturen“', '0:26', '0:29', 'c',
 '**Zusammenfassung:** Wisnewski fragt, ob es „originären“ islamistischen Terror überhaupt gebe. Al-Qaida sei „eigentlich eine Erfindung oder eine Schöpfung der Amerikaner“: eine Liste von Leuten, die in Afghanistan gegen die Sowjets kämpfen sollten; der Name heiße nur „die Basis“ oder „die Liste“. Viele Gruppen hätten sich in US-Gefängnissen zusammengefunden.',
 '💬 „ein Kampfbegriff, ein nützlicher Begriff, um den Krieg anzuzetteln“ (Wisnewski) [0:26–0:27]',
 '📌 Samuel Huntington habe Mitte der 90er im allgemeinen Friedensgefühl einen neuen Konflikt ausgerufen, „The Clash of Civilizations“; das Buch sei „relativ langweilig“, aber global „gehypt“ worden; Huntington sei womöglich „nicht zufällig“ darauf gekommen [0:27] [seine Sicht].',
 '📌 **Gastgeber:** Die Mudschaheddin seien nach der sowjetischen Intervention („1978“) vom Westen ausgebildet und finanziert worden, daraus seien Al-Qaida, al-Nusra und der IS hervorgegangen; „diese Leute“ seien heute Präsidenten Syriens und säßen im Weißen Haus [0:28] [seine Sicht].',
 '📚 **Ergänzung:** Die sowjetische Intervention in Afghanistan begann im Dezember 1979; Huntingtons Aufsatz erschien 1993, das Buch 1996.')

ab('🛡️ Feindbildwechsel und der erste NATO-Bündnisfall', '0:29', '0:32', 'c',
 '**Zusammenfassung:** Der Gastgeber fasst zusammen: Nach Jahrzehnten Angst vor dem Atomkrieg (Kubakrise) sei der „böse Russe“ durch den islamischen Terror abgelöst worden, heute habe man beides. Wisnewski: Russland sei damals „implodiert“; der neue Konflikt sei erst durch die NATO-Einkreisung und die Absetzung des gewählten ukrainischen Präsidenten aufgebaut worden – bis dahin habe man „diese ganze Al-Qaida und 9/11-Nummer gefahren“ [0:29–0:31] [seine Sicht].',
 '📌 Kurz nach dem 11.9. sei „der amerikanische Außenminister Paul“ (Name so im Transkript ❓) im NATO-Hauptquartier in Brüssel aufgetreten; erstmals sei Artikel 5 des NATO-Vertrags aktiviert worden, man habe eine „Koalition der Willigen“ gebildet [0:31].',
 '💬 „Der Frieden ist für diese Leute eine Katastrophe.“ (Wisnewski) [0:31]',
 '🔗 Gastgeber verweist auf seine Gespräche bei „Fair Talk“ und bei Ben ({ungeskriptet}) [0:32].',
 '📚 **Ergänzung:** Der Bündnisfall wurde am 12.09.2001 erstmals ausgerufen – siehe Abgleich.')

ab('🌊 Libyen, Gaddafi und die Fluchtbewegungen', '0:32', '0:36', 'e',
 '**Zusammenfassung:** Der Gastgeber fragt nach Libyen: Ohne den Sturz Gaddafis als „Gatekeeper“ wären Flüchtlingskrise und Erstarken des Rechtspopulismus nicht möglich gewesen. Wisnewski verweist auf sein 2½-stündiges Gespräch mit seinem Sohn und eine Karte der Fluchtbewegungen nach dem 11.9.2001: Durch die Kriege sei „mit der Keule“ auf die Staaten geschlagen worden, die Flüchtlinge seien „rausgespritzt“ [0:33–0:34].',
 '📌 Libyen habe viele Flüchtlinge aus dem Inneren Afrikas aufgenommen und versorgt; Gaddafi habe gewarnt, nach seiner Beseitigung komme eine riesige Flüchtlingswelle nach Europa [0:34] [seine Sicht].',
 '📌 Es sei „regelrecht eine Art Migrationskrieg“ entstanden, wie derzeit in Ceuta; die wohlhabenden Länder Mittel- und Nordeuropas würden destabilisiert. Den Krieg gegen Libyen hätten die USA mit Großbritannien und Frankreich angezettelt [0:34–0:35] [seine Sicht].',
 '📌 **Gastgeber:** nennt Kelly M. Greenhills Buch „Weapons of Mass Migration“ (im Transkript „Carry Greenhill“) als Standardwerk und sieht beim Thema Ceuta das Muster „Abraham-Abkommen“ – leidtragend seien „immer die Unterschicht auf beiden Seiten“ [0:35–0:36] [seine Sicht].')

ab('🏗️ Bin Laden, die Bush-Familie und die fehlenden Abfangjäger', '0:36', '0:39', 'd',
 '**Zusammenfassung:** Der Gastgeber: Osama bin Laden sei wie fast alle Täter offiziell aus Saudi-Arabien gekommen, nicht aus Irak, Afghanistan oder Libyen; die Familie sei Geschäftspartner der Bush-Familie gewesen [seine Sicht]. Er erwähnt die schwer beweisbare These „Tim Osman“ und sagt, ein Bruder bin Ladens habe sich während der Anschläge mit George Bush senior getroffen [0:36–0:37].',
 '📌 Wisnewski: Bin Laden sei „praktisch ein CIA-Mann“ gewesen, Angehöriger einer der reichsten saudischen Familien mit einem riesigen Baukonzern [0:37–0:38] [seine Sicht].',
 '💬 „Das Ganze war ja eine US-Regierungsaktion“ (Wisnewski) [0:38]',
 '📌 Weicht ein Jet vom Kurs ab und bricht den Funkkontakt ab, bekomme er Routine-Begleitung durch Abfangjäger; dass das nicht stattfand, reiche allein, um „diese ganze Inszenierung“ ad absurdum zu führen [0:38–0:39] [seine Sicht].',
 '📚 **Ergänzung:** Was die 9/11-Kommission zu den Meldezeiten an die Luftverteidigung festgestellt hat, steht im Abgleich und im Prüfstand. Das genannte Treffen eines bin-Laden-Bruders mit Bush senior habe ich nicht geprüft ❓.')

ab('🪪 Ausweisfund, Flugschüler und das Pentagon', '0:39', '0:44', 'd',
 '**Zusammenfassung:** Der Gastgeber: Flugzeug und Blackbox seien „vaporisiert“, der Ausweis eines Täters aber unversehrt aufgefunden worden. Wisnewski findet das „wie aus einer schlechten Komödie“; neuerdings würden bei Terroranschlägen öfter Ausweise gefunden [0:40].',
 '💬 „der 11.9 ist ein einziges äh Kuriositätenkabinett“ (Wisnewski) [0:41]',
 '📌 Die mutmaßlichen Piloten hätten nicht einmal eine Sportmaschine fliegen können, bei Flugstunden ihr Flugzeug auf der Landebahn stehen lassen und keine Landung lernen wollen; sie hätten Spuren gelegt „wie trampelnde Elefanten“ (nach Andreas von Bülow) und laute Streitereien in Kneipen angezettelt [0:41–0:42] [seine Sicht].',
 '📌 **Gastgeber:** Der Ausweis gehörte Satam al-Suqami („heißt auch interessanterweise Satan“); Täter hätten sich in Florida in Stripclubs betrunken und Korane an der Bar vergessen [0:42–0:43]. Am Pentagon gebe es kaum Material; Gruppen wie Architects & Engineers for 9/11 Truth und Pilots for 9/11 Truth mit „tausenden“ Mitgliedern hielten das Manöver für unmöglich; auf einem Tankstellenvideo sei eine Explosion zu sehen, Turbinenteile seien zu klein [0:43–0:44] [seine Sicht].',
 '📚 **Ergänzung:** Was die amtlichen Berichte zum Pentagon (ASCE 2003) und zu WTC 7 (NIST 2008) sagen und was die Studie der University of Alaska Fairbanks dagegen hält, steht im Abgleich.')

ab('✈️ Als Touristen in die USA – Anfang 2003', '0:44', '0:47', 'd',
 '**Zusammenfassung:** 2003, in der „Vorkriegszeit“ vor dem Irakkrieg, hatten Wisnewski und Brunner einen WDR-Auftrag für eine Dokumentation über Zweifel am 11.9. Sie reisten als Touristen mit einer besseren Amateurkamera ein, ohne Fernsehausrüstung. In diesen Wochen seien Dutzende ausländische Journalisten mit vollem Equipment an US-Flughäfen festgenommen, über Nacht eingesperrt und zurückgeschickt worden [0:45–0:46].',
 '📌 Sie trafen die Gruppe hinter unansweredquestions.org und fuhren zu den Orten: Ground Zero war bereits geräumt, man bereitete den Neubau vor [0:45–0:46].',
 '📌 **Pentagon:** Das Gebäude sei flach und liege in einer Senke hinter einem Hügel; eine Boeing 757 sei „kein Kampfjet“ und könne ein solches bodennahes Manöver nicht fliegen – „absolut lächerlich“ [0:46–0:47] [seine Sicht].',
 '📌 Er verspricht sich: „wobei wir da noch viel mehr Belege haben, dass dort eine Maschine reingeflogen ist“ – gemeint ist offenbar das Gegenteil ❓ [0:47].')

ab('🌾 Shanksville: „Da war kein Flugzeug“', '0:47', '0:50', 'd',
 '**Zusammenfassung:** In Shanksville sei Flug 93 abgestürzt – nach offizieller Darstellung, weil Passagiere die Entführer überwältigen wollten. Wisnewski nennt das „eine schöne Legende, eine tolle Propagandageschichte“. Er traf Bürgermeister Ernie Stull, zugleich Feuerwehrmann.',
 '💬 „da kam sie dahin und da war kein Flugzeug“ (Wisnewski gibt Stull wieder) [0:49]',
 '📌 Er habe dreimal nachgefragt; Stull habe ihm ein Foto des Kraters ohne erkennbare Wrackteile gezeigt und gesagt, das sei die Absturzstelle, „aber da war nichts drin“ [0:49–0:50].',
 '📌 Zwei Tage vor Kriegsbeginn hätten sie die USA mit dem Material verlassen [0:50].',
 '📚 **Ergänzung:** Laut 9/11-Kommission stürzte Flug 93 um 10:03:11 Uhr bei Shanksville ab; ein Bericht im Freitag (2003) ordnet die Bürgermeister-Aussage als Beschreibung des ersten Moments eines tagelangen Geschehens ein – siehe Abgleich. Ob Stull seine Aussage später anders darstellte, habe ich nicht im Original geprüft ❓.')

ab('⚔️ Vor dem Irakkrieg – Massenvernichtungswaffen und Iran-Irak-Krieg', '0:50', '0:53', 'e',
 '**Zusammenfassung:** Der Gastgeber spricht die Stimmung kurz vor einem Krieg an. Wisnewski: Bis dahin sei die Einreise für Journalisten problemlos gewesen, die Festnahmen seien Ausdruck der „Nervosität“ vor dem Krieg; sie seien „ungehelligt“ wieder herausgekommen [0:51].',
 '📌 **Gastgeber:** Die „Lüge“ um Saddam Husseins Massenvernichtungswaffen; Saddam sei im Iran-Irak-Krieg von den USA mit Waffen und Geld unterstützt worden, damit ein Krieg, der nach acht Wochen vorbei gewesen wäre, acht Jahre dauerte und über eine Million Tote forderte [0:52] [seine Sicht].',
 '📌 Der Gastgeber sagt, er sei Flüchtling aus dieser Zeit; Saddam sei ein „Vasall“ der westlichen Strukturen gewesen [0:52].',
 '📚 **Ergänzung:** Der Iran-Irak-Krieg dauerte von 1980 bis 1988. Zur Opferzahl gibt es nur Schätzungen; hier nicht geprüft ❓.')

ab('📷 Gastgeber: die „tanzenden Israelis“ – dann der Film', '0:53', '0:55', 'd',
 '**Zusammenfassung:** Der Gastgeber knüpft an die Festnahmen an und spricht von Männern, die mit Kameras „tanzend“ um das World Trade Center erwischt worden seien – „die israelischen Tanzbären“.',
 '📌 **Gastgeber:** Es habe nach den Anschlägen bis zu 100 Verhaftungen von Israelis rund um New York gegeben; ein Teil sei als israelische Agenten „entlarvt“ und heimgeschickt worden; man habe das nicht veröffentlicht, um die Beziehungen zwischen Israel und den USA nicht zu gefährden – „mit zweierlei Maß“ [0:53–0:54] [seine Sicht]. Wisnewski geht darauf nicht ein.',
 '📌 Dann bestätigt Wisnewski den Titel des Films: „Aktenzeichen 11.9. ungelöst“ [0:54].',
 '📚 **Ergänzung:** Was ABC News 2002 über fünf festgenommene Israelis berichtete, steht im Abgleich; die Zahl „bis zu 100“ habe ich nicht belegt gefunden ❓.')

ab('📰 Die „Bombe“ im Programm und der Spiegel-Titel', '0:55', '1:00', 'f',
 '**Zusammenfassung:** Wisnewski habe gespürt, dass er „eine Bombe zünden“ würde, wegen „Gleichschaltung“ und des Chors aus Medien und Politik. Im Film hätten sie „eigentlich nichts behauptet“, sondern Fragen gestellt und Zweifel gezeigt.',
 '💬 „als würden sie in der … vollbesetzten Kirche plötzlich einen Knaller zünden“ (Wisnewski) [0:55]',
 '📌 Der Spiegel sei ein „Hinrichtungsmagazin“; er habe einen Titel über sie gemacht und die WTC-Türme kopfüber abgebildet. Vier Leute seien „an den Pranger“ gestellt worden: Wisnewski, Andreas von Bülow, Mathias Bröckers und der französische Journalist Thierry Meyssan – als „Verdreher, Spinner, Verfälscher“ [0:56–0:58] [seine Sicht].',
 '📌 Er habe die Verflechtung der Medien mit der Atlantik-Brücke schon beim RAF-Buch beobachtet, die er ein „außenpolitisches Steuerungs- und Einflussinstrument“ der USA nennt; Kritik an den USA sei „vollkommen tabu“ gewesen [0:58–0:59] [seine Sicht].',
 '📚 **Ergänzung:** Die Titelgeschichte erschien am 08.09.2003; neben Wisnewski, von Bülow und Meyssan wurden dort Bröckers und Andreas Hauß behandelt – siehe Abgleich.')

ab('📡 Operation Mockingbird – und die Einladung des WDR', '1:00', '1:03', 'f',
 '**Zusammenfassung:** Der Gastgeber nennt Operation Mockingbird als in den 1970ern „bewiesenen“ Einfluss der CIA auf US-Medien, zitiert sinngemäß den früheren CIA-Mitarbeiter John Kiriakou (heute übernehme man den „CIA-Newsletter“ ohne Bestechung) und sagt, nach 1945 seien in Deutschland u. a. Axel Springer über Lizenzen „gezielt groß gemacht“ worden [1:00–1:01] [seine Sicht].',
 '📌 Wisnewski: In groben Zügen sei ihm das bewusst gewesen; auch bei den RAF-Anschlägen wiesen „einige Spuren in die Vereinigten Staaten“ [1:01] [seine Sicht].',
 '📌 Seine Redaktion beim WDR habe ihn zu einer Gesprächsrunde eingeladen – „so auf die demokratische Tour“, sodass man nicht Nein sagen könne [1:02].',
 '📚 **Ergänzung:** Die Untersuchungen des Church-Ausschusses des US-Senats (1975/76) befassten sich u. a. mit Kontakten der CIA zu Journalisten; den Namen „Mockingbird“ und Einzelheiten habe ich hier nicht eigens geprüft ❓.')

ab('🎙️ Die WDR-Runde als „Tribunal“ – und eine ZDF-Doku', '1:03', '1:10', 'f',
 '**Zusammenfassung:** Der WDR habe „180 Grad zurückgerudert“ und für den eigenen Mitarbeiter eine Runde veranstaltet: fünf „Experten“, ein Journalist (Name im Transkript unklar ❓) und der Moderator, dazu sechs Einspielfilme – „zehn oder elf Faktoren gegen einen“. Man habe auf schwer zu haltenden Schaukelstühlen gesessen; es werde „wie live“ gesendet, nichts geschnitten [1:03–1:04].',
 '💬 „es war ein stalinistisches Tribunal“ (Wisnewski) [1:05]',
 '📌 Die anderen hätten sich vorher abgesprochen; als er hereinkam, sei die Atmosphäre „eisig“ geworden [1:06] [seine Sicht].',
 '🔗 Gastgeber vergleicht mit Eva Hermans Auftritt bei Kerner; Wisnewski sieht dasselbe Muster bei Lanz [1:05].',
 '📌 **Gastgeber:** zeigt eine aktuelle Dokumentation zum 25. Jahrestag aus der ZDF-Mediathek (Sendername im Transkript „CTF Info“ ❓), kritisiert die Autorin scharf und lädt sie zu einer Diskussion auf den Kanal ein; zugleich nennt er sie „eigentlich eine nette“ [1:07–1:09].',
 '📚 **Ergänzung:** Laut Freitag (19.09.2003) lief beim WDR am 10. September die Sendung „Wahrheit oder Täuschung? Verschwörungstheorien zum 11. September“ – vermutlich die beschriebene Runde ❓.')

ab('🏛️ Humboldt-Universität: „Der inszenierte Terrorismus“ und Horst Mahler', '1:10', '1:14', 'f',
 '**Zusammenfassung:** Die Veranstaltung „Der inszenierte Terrorismus“ im Audimax sei ein Beispiel lebendiger Fragekultur gewesen: Wisnewski, Bröckers, von Bülow und der RAF-Mitautor (im Transkript „Ecke Harzeker“, vermutlich Ekkehard Sieker ❓) hielten je einen Vortrag, der Saal war überfüllt.',
 '📌 Mitten im Publikum habe Horst Mahler gesessen, „breitbeinig und grinsend“ – früher RAF, später Neonazi. Dann sei ein Mann hereingestürmt und habe „Nazi“ gerufen, die Antifa sei „aus dem Hut gezaubert“ worden; draußen seien Büchertische umgeworfen worden [1:11–1:14].',
 '📌 So sei die Veranstaltung als „rechtsradikal geframed“ worden – über „Kontaktschuld“, eine „übliche Methode von Geheimdiensten“ [1:13–1:14] [seine Sicht].',
 '📌 Wisnewski sagt, Mahler sei inzwischen verstorben – nicht geprüft ❓.')

ab('🎞️ Die Einblendung: von Bülows Antwort und die Antifa-Frage', '1:14', '1:17', 'f',
 '**Zusammenfassung:** Der Gastgeber lobt, wie souverän Andreas von Bülow reagiert habe, und blendet einen Ausschnitt ein (Wisnewski verweist auf das Zitatrecht).',
 '💬 „In der Regel werden solche Zwischenfälle organisiert“ (von Bülow im Ausschnitt) [1:16]',
 '📌 Von Bülow im Ausschnitt: Es gehe nicht um Argumente; man wisse nicht, von wem solche Leute instrumentalisiert würden; das letzte NPD-Verfahren habe Hinweise gegeben, wie Organisationen zustande kämen [1:16].',
 '📌 Auf die Frage, woher die Antifa so schnell kam: nicht recherchiert; es sei ihm vorgekommen, als sei die Antifa „der linke Arm des Spiegel“ – eine Abteilung des „Propagandakonzerns“ neben Spiegel, Panorama und vielleicht der Antifa [1:16–1:17] [seine Sicht].',
 '📚 **Ergänzung:** Das erste NPD-Verbotsverfahren stellte das Bundesverfassungsgericht 2003 ein, weil V-Leute des Verfassungsschutzes in Führungsgremien der Partei tätig waren (BVerfG, 2 BvB 1/01, 18.03.2003; hier nicht verlinkt).')

ab('🏙️ Gastgeber: Kreuzberg, Gangs und ein Gespräch mit der Antifa', '1:17', '1:21', 'w',
 '**Zusammenfassung:** Der Gastgeber erzählt aus seiner Jugend in Kreuzberg: Dort habe nicht die Antifa dominiert, sondern migrantische Gangs (mindestens zehn große mit teils 100 Mitgliedern). Nach 1989 hätten die Gangs gemeinsam Neonazis von den Straßen vertrieben, nicht die Antifa [1:17–1:19] [seine Sicht].',
 '📌 Mit einem Antifa-Funktionär sei er wegen 9/11 aneinandergeraten; der habe Dietrich Eckart, Rudolf von Sebottendorf und die Thule-Gesellschaft nicht gekannt [1:19–1:20].',
 '📌 Die Basis der Antifa suche eine Ersatzfamilie; in den oberen Strukturen vermute er eine Politisierung durch Finanzierung [1:20–1:21] [seine Sicht].')

ab('📞 Beschäftigungsverbot per Anruf – und der Gastgeber über Broder', '1:21', '1:24', 'f',
 '**Zusammenfassung:** **Gastgeber:** In der Corona-Zeit habe eine Antifa-Gruppe in Kanada in einem Video gefordert, George Soros solle ihr Geld überweisen (nicht geprüft ❓). Dann fragt er, wie Wisnewski vom Ende beim WDR erfuhr.',
 '📌 Ein Spiegel-Reporter habe ihn angerufen: Der WDR habe ein „Beschäftigungsverbot“ verhängt, den Redaktionen also verboten, ihm und Willy Brunner Aufträge zu geben; danach habe es nur noch E-Mails mit „WDR-Bossen“ gegeben [1:22] [seine Sicht].',
 '📌 **Gastgeber:** nennt Henryk M. Broder einen „zionistischen Gatekeeper“ und „Propagandisten“; Broder habe im Interview bei Flavio von Witzleben das „Projekt Groß-Israel“ als Idee zweier Knesset-Abgeordneter (im Transkript „Smodridge und Giren“, vermutlich Smotrich und Ben-Gvir ❓) abgetan [1:23] [seine Sicht].',
 '📚 **Ergänzung:** Das zitierte Interview habe ich nicht geprüft ❓; Aussagen über Broder stehen hier nur als Wiedergabe.')

ab('💧 Die „Bücherversenkung“ im Brunnen', '1:24', '1:28', 'f',
 '**Zusammenfassung:** Broder habe im öffentlich-rechtlichen Fernsehen eine Reihe gehabt, in der er militärisch kostümiert in einem bunten Fahrzeug Kritiker besuchte. Wisnewski lehnte ein Interview ab. Zum Thema 9/11 – „glaube ich dann zum 10-Jahres“ ❓ – habe Broder einen Stapel 9/11-Bücher in einen Brunnen geworfen und von „Bücherversenkung“ gesprochen [1:24–1:26].',
 '📌 Wisnewski sieht darin die „nasse Version der Bücherverbrennung“; die großen Bestseller von 2003 (seins, Bröckers, von Bülow) seien nicht dabei gewesen, nur ein Buch von Wolfgang Eggert mit seinem Vorwort [1:25–1:26] [seine Sicht].',
 '📌 Broder sei auch bei der Humboldt-Veranstaltung „an vorderster Stelle“ dabei gewesen; ob er Kontakt zur Antifa oder zu Mahler hatte, „kann ich natürlich nicht behaupten“ [1:27].',
 '📌 Veranstalter hätten mit Plakaten geworben; er selbst sei nicht Veranstalter gewesen [1:27–1:28].')

ab('📊 Jebsen, „65 %“ und das Wort „Verschwörungstheoretiker“', '1:28', '1:31', 'f',
 '**Zusammenfassung:** Der Gastgeber sagt, Broder habe auch zum Ende von Ken Jebsen bei RBB/Fritz beigetragen; heute gebe es ein anderes Bewusstsein. 65 % der US-Bevölkerung hätten 2006 die Regierungsdarstellung des 11. September abgelehnt [1:29].',
 '📌 Wisnewski: Schmähkampagne, „Tribunal“, Spiegel-Titel, Humboldt-Uni – „alles organisiert“, der „große Gegenschlag“ [1:30] [seine Sicht].',
 '💬 „der beweist eigentlich nur, dass er keine Argumente hat“ (Wisnewski über Nutzer des Begriffs „Verschwörungstheoretiker“) [1:30]',
 '📌 **Gastgeber:** Der Begriff sei seit JFK vermehrt durch Geheimdienste verbreitet worden; „Wer heutzutage kein Verschwörungstheoretiker ist, begeht Verrat an seiner Bevölkerung“ [1:30–1:31] [seine Sicht].',
 '📚 **Ergänzung:** Die Umfrage von Scripps-Howard/Ohio University (2006) ergab 36 % – siehe Abgleich.')

ab('💔 Die Folgen für ihn und Willy Brunner', '1:31', '1:34', 'f',
 '**Zusammenfassung:** Auf die Frage nach den psychischen Folgen: Als „kleiner Journalist“ seien die „ganz großen Glocken der Republik“ – Panorama, Spiegel, WDR, wohl auch die Süddeutsche – wie „bissige Hunde“ auf ihn losgegangen [1:32].',
 '💬 „Das hat uns traumatisiert. Ganz klar.“ (Wisnewski) [1:32]',
 '📌 Beide hätten keine Fernseharbeit mehr machen können bzw. wollen; Brunner habe seine Existenz als TV-Produzent verloren; er selbst habe sich über die gut verkauften Bücher gehalten [1:32–1:33].',
 '📌 Gastgeber: Dies sei Teil 1 der „9/11 Chronicles“; als Nächstes komme Bröckers [1:34].')

ab('📜 Krieg, Konfrontation, Kontrolle – Patriot Act und die Länderliste', '1:34', '1:37', 'g',
 '**Zusammenfassung:** Die Ergebnisse des 11.9. seien „Krieg, Konfrontation und Kontrolle“ – Kontrolle nach innen, Krieg nach außen. Nach dem 11.9. seien „stapelweise“ Antiterrorgesetze verabschiedet worden, „euphemistisch Patriot Act 1 und 2“; das erste sei ein „345-Seiten-Konvolut“ gewesen, vom Kongress „durchgewinkt“ [1:34–1:35].',
 '📌 Dazu gehörten Hausdurchsuchungen ohne Wissen der Betroffenen, Maßnahmen in der Luftfahrt, Ausweis- und biometrische Kontrollen – „ein absolut demokratischer Albtraum“ [1:35] [seine Sicht].',
 '📌 Der Iran habe auf der „Liste der sieben Länder“ gestanden, die jetzt „abgearbeitet“ werde; wir lebten in der „Post-9/11-Welt“ [1:35–1:36].',
 '💬 „Das war die Tür in den neuen Wahnsinn.“ (Wisnewski) [1:36]',
 '📚 **Ergänzung:** Der USA PATRIOT Act wurde am 26.10.2001 unterzeichnet (Public Law 107-56); die Seitenzahl habe ich nicht geprüft ❓. Clarks Liste umfasste laut seinem Interview 2007 sieben Länder – siehe Abgleich.')

ab('🛰️ Gastgeber: Von „Total Information Awareness“ zu Palantir', '1:37', '1:40', 'g',
 '**Zusammenfassung:** Der Gastgeber sieht Technokratie, Peter Thiel und Palantir als „direkte Ergebnisse“ von 9/11: Das Programm „Total Information Awareness“ sei „nahtlos“ zu Palantir geworden [1:37] [seine Sicht].',
 '📌 **Gastgeber:** Er schlägt einen Bogen zum Film über die Nord-Stream-Sprengung (Filmemacher im Transkript „Moritz Enders“ ❓) und zum Erdgas-Röhren-Geschäft unter Helmut Schmidt, das die Reagan-Regierung mit Richard Perle torpediert habe; laut Dirk Pohlmann sei der Wechsel zu Helmut Kohl ein „Putsch“ gewesen [1:37–1:38] [seine Sicht].',
 '📌 **Gastgeber:** Perle habe nach der Ablehnung des Überwachungsprogramms durch den Kongress dessen Übertragung in den Privatsektor betrieben und mit John Poindexter Alex Karp und Peter Thiel kontaktiert – „so wurde Palantir geboren“ [1:38–1:39] [seine Sicht]. Für diese Darstellung habe ich keine Quelle geprüft ❓.',
 '📌 Er nennt Gotham und VeRA (Palantir-Software bei der Polizei) und erwartet, eine AfD-Regierung werde Deutschland „palantirisieren“ [1:39] [seine Sicht].')

ab('🤖 Die „Schnüffelindustrie“ und die KI, die für uns denkt', '1:40', '1:43', 'g',
 '**Zusammenfassung:** Wisnewski: Die „ganze Schnüffelindustrie“ habe durch den 11.9. einen Schub bekommen, vor allem einen „Legitimationsschub“; große Sicherheitskonzerne seien heute „die größte demokratische Bedrohung“ – auch durch künstliche Intelligenz, die anfange, „für uns zu denken“ (Google, Perplexity, ChatGPT) [1:40–1:41] [seine Sicht].',
 '📌 Die Maßnahmen täten nicht weh, sie seien bequem – „Honigfallen“ (im Transkript „Honigballen“); das Handy sei eine „Wanze, die wir mit uns rumtragen“ (im Transkript „Wand zu“ ❓) [1:41].',
 '📌 **Gastgeber:** ein globaler Überwachungsapparat von Iran über Russland bis China; Smart-Wall-Systeme fingen bei Flüchtlingen an. Er fragt, ob Anschläge in Deutschland (Anis Amri, Solingen, „jetzt vor kurzem“ der CSD) jeweils zu neuen Gesetzespaketen führten [1:41–1:43].')

ab('🛸 „Sicherheit vor dem Staat“, Drohnen und „Flüchtlinge von morgen“', '1:43', '1:47', 'g',
 '**Zusammenfassung:** Der Begriff Sicherheit sei „schillernd“.',
 '💬 „das ist die Sicherheit vor dem Staat“ (Wisnewski) [1:43]',
 '📌 Gemeint sei Sicherheit vor dem Staat und „den kriminellen Netzwerken, die den Staat beherrschen“. Jeder Mausklick werde erfasst; wer sich mit Google auf fremden Seiten anmelde, verrate, wo er Konten habe [1:43–1:44] [seine Sicht].',
 '📌 Datenpakete ließen sich mit „kinetischen“ Technologien koppeln: KI erkläre jemanden für gefährlich, eine Drohne suche ihn. Drohnennetze über Straßen gebe es im Ukraine-Krieg; Deutschland und Europa würden „ausgeliefert“ – „Wir sind wahrscheinlich die Flüchtlinge von morgen“ [1:44–1:46] [seine Sicht].',
 '📌 Gegen diese Dystopie sei Orwells „1984“ „eine kleine Einschlafgeschichte“; „die Zeichen sind an der Wand“ [1:46].')

ab('🗳️ Demokratie, AfD und ein Gewerkschafter', '1:47', '1:51', 'h',
 '**Zusammenfassung:** Der Gastgeber fragt nach dem parlamentarischen System, einem möglichen Krieg mit Russland und ob Wisnewski noch wählt. Wisnewski: Die Demokratie werde „in dem Moment abgeschafft, indem die falschen Parteien gewählt werden“ – Kandidaten würden nicht zugelassen, der AfD würden Ausschussvorsitze verwehrt [1:47–1:48] [seine Sicht].',
 '📌 Die AfD werde durch die „CDU-SPD-FDP-Einheitspartei“ indirekt gefördert – ein „dialektischer Prozess“; das System sei „dysfunktional“, sonst wären die Meinungen der AfD vorher abgebildet worden; es brauche „unbedingt“ eine Reform [1:48–1:50] [seine Sicht].',
 '📌 Ein Funktionär der Gewerkschaft der Polizei (Name im Transkript unklar ❓) habe für den Fall eines AfD-Wahlsiegs in Sachsen-Anhalt „durch die Blume“ mit einem Putsch gedroht und sei zurückgetreten [1:48–1:49] [seine Sicht]. Den Vorgang habe ich nicht geprüft ❓.',
 '📌 **Gastgeber:** Nach dem Anschlag auf den CSD habe ihm ein AfD-Mitglied geschrieben, damit „holen wir uns jetzt Sachsen-Anhalt“ [1:50]. Nicht geprüft ❓.')

ab('🔥 Anschläge in Deutschland, „Failed State“ und Solingen', '1:51', '1:55', 'h',
 '**Zusammenfassung:** Auf die Frage nach islamistischen Anschlägen, von denen die AfD profitiere: Je mehr Anschläge, desto mehr Stimmen für eine Partei, die weniger Migration verspricht. Dass Anschläge bewusst inszeniert würden, um die AfD hochzubringen, „kann ich jetzt nicht unbedingt unterschreiben“ [1:51–1:52].',
 '📌 Es gehe eher um einen herbeigeführten Bürgerkrieg: Die Eliten wollten Deutschland und Europa zum „Failed State“ machen; man warte „sehnlichst auf einen Deutschen, der ausrastet“, um dann mit Repression gegen „die deutsche Restbevölkerung“ vorzugehen [1:52–1:53] [seine Sicht].',
 '📌 **Gastgeber:** erinnert an „Solingen 1992“: Täter hätten 15 Jahre abgesessen und danach gesagt, sie seien es nicht gewesen; Verfassungsschutz und Dienste hätten womöglich „auf beiden Seiten“ die Finger im Spiel [1:53–1:54] [seine Sicht]. Er sieht den Gegensatz „Unterschicht gegen Elite“, nicht links gegen rechts [1:54].',
 '📚 **Ergänzung:** Der Brandanschlag von Solingen war am 29.05.1993; fünf Menschen türkischer Herkunft starben, das Oberlandesgericht Düsseldorf verurteilte 1995 vier Täter (allgemeine Nachschlagewerke, hier nicht verlinkt).')

ab('🪖 Krieg mit Russland? – Abschied', '1:55', '1:59', 'h',
 '**Zusammenfassung:** Auf die nachgereichte Frage nach einem Krieg mit Russland: Deutschland werde nicht „kriegsfähig“, wie Pistorius es wünsche – es gebe keine brauchbare Armee, keine Bereitschaft und keine nationale Identität, die über Jahrzehnte „vernichtet“ worden sei [1:54–1:55] [seine Sicht].',
 '📌 Er sehe schon Lieferwagen junge Männer „einsacken“ – als „Kanonenfutter“, um Material an die Front zu fahren [1:55] [seine Sicht].',
 '📌 Die Politik denke „nicht rational“ bzw. im Sinne anderer Ziele, etwa Deutschland zum „Failed State“ zu machen; Russland zeige „eine Art Schafsgeduld“. Baerbock habe behauptet, man befinde sich im Krieg mit Russland; Deutschland liefere Waffen und finanziere den Krieg – Atombomben erwarte er wegen des Westwinds nicht [1:56–1:57] [seine Sicht].',
 '📌 Der Gastgeber dankt, zählt Wisnewski zur „heldenhaftesten Fraktion“ des deutschen Journalismus und erwähnt seine Iran-Reise 2012, Mondlandung und Titanic [1:57–1:58].')

ab('👋 Schlusswort: Kommentare, das Gespräch mit dem Sohn, Ausblick', '1:59', '2:04', 'w',
 '**Zusammenfassung:** Der Gastgeber dankt der Community für faire Kommentare (Beispiel: ein Podcast mit Caroline Rage ❓, inzwischen „über 95 %“ Zustimmung). Wisnewski verweist auf sein Gespräch mit seinem Sohn über die Anfänge der Bewegung auf seinem YouTube-Kanal (Teil 2 sicher, Teil 3 später) und auf seinen Telegram-Kanal [1:59–2:02].',
 '📌 Der Zugang über die Menschen sei wichtig, weil schon „so viele Fakten hin und her geworfen“ worden seien (Kerosin, Stahl, Temperaturen) [2:01].',
 '📌 **Gastgeber:** Sein Buch werde Neues seit der „Generation Wisnewski“ behandeln – Epstein-Akten, Verbindungen zu Technokratie, Thiel und Musk, Hollywood – und noch im Jubiläumsjahr erscheinen; nächster Gast der Reihe: Mathias Bröckers [2:03–2:04].')

# ---------- Themen ----------
THEMEN = [dict(k='f', n='Werdegang, Medien & Gegenwind'), dict(k='b', n='RAF & Geheimdienste'),
          dict(k='c', n='Vorgeschichte & Krieg gegen den Terror'), dict(k='d', n='Der 11. September – Ablauf & Zweifel'),
          dict(k='e', n='Kriege & Migration'), dict(k='g', n='Überwachung & Technik'),
          dict(k='h', n='Deutschland heute'), dict(k='w', n='Gastgeber & Organisatorisches')]

def kurztitel(t):
    return t.split(' ', 1)[1]

# ---------- Reiter 1: Überblick ----------
KERN = [
 ['1', 'Die offizielle Darstellung des 11. September könne nicht stimmen; der Tag sei eine „US-Regierungsaktion“ gewesen.', 'Keine Abfangjäger trotz Routineverfahren; Täter binnen 48 Stunden benannt; „Kuriositätenkabinett“.', '[0:19], [0:38], [0:41]', '★★★'],
 ['2', 'In Shanksville und am Pentagon sei „sehr wahrscheinlich“ kein Flugzeug abgestürzt.', 'Aussage des Bürgermeisters Ernie Stull; Topografie am Pentagon, Boeing 757 „kein Kampfjet“.', '[0:06], [0:46–0:50]', '★★★'],
 ['3', 'Dasselbe Muster wie beim „Phantomterrorismus“ der RAF-Spätzeit.', 'Ungeklärte Morde an Herrhausen, Rohwedder, von Braunmühl; Fahndungsplakate ohne Beweis.', '[0:08–0:13]', '★★'],
 ['4', 'Der 11.9. wurde begrifflich vorbereitet („neues Pearl Harbor“).', 'PNAC-Papier 2000; Kinofilm „Pearl Harbor“ 2001 als „Repetitorium“; „Stafettenlauf der Begriffe“.', '[0:15–0:18]', '★★'],
 ['5', 'Nach dem Kalten Krieg brauchte der Westen einen neuen Feind – den islamistischen Terror.', 'Sinnkrise der NATO; Huntington; Al-Qaida als „Liste“; erster NATO-Bündnisfall.', '[0:21–0:31]', '★★'],
 ['6', 'Die Kriege nach 9/11 lösten Fluchtbewegungen nach Europa aus.', 'Libyen und Gaddafis Warnung; „Migrationskrieg“; Karte im Gespräch mit dem Sohn.', '[0:33–0:35]', '★★'],
 ['7', '2003 sei das „Großkampfjahr um die Wahrheit“ gewesen – mit organisiertem Gegenschlag der Medien.', 'Spiegel-Titel, WDR-„Tribunal“, Humboldt-Uni mit Horst Mahler, Beschäftigungsverbot.', '[0:55–1:30]', '★★★'],
 ['8', 'Ergebnis von 9/11: Krieg, Konfrontation und Kontrolle.', 'Patriot Act, Kontrollen, Liste der sieben Länder; „Post-9/11-Welt“.', '[0:21], [1:34–1:36]', '★★'],
 ['9', 'Die Überwachungsindustrie habe durch 9/11 einen Legitimationsschub bekommen; KI und Drohnen verschärften das.', '„Schnüffelindustrie“, Google-Login, Drohnennetze; „Sicherheit vor dem Staat“.', '[1:40–1:46]', '★★'],
 ['10', 'Deutschland solle zum „Failed State“ werden; die Demokratie sei „dysfunktional“.', 'Umgang mit der AfD, „dialektischer Prozess“, Migration, keine Kriegsfähigkeit.', '[1:47–1:57]', '★★'],
]

BAUM = [
 {'t': '🪪 Person & Werdegang', 'k': [{'t': 'Lebenslauf laut Gemini [0:02]'}, {'t': 'Grimme-Preis ging an den Film [0:03]'}, {'t': 'WDR-Film „Aktenzeichen 11.9. ungelöst“ [0:05]'}, {'t': 'Ende beim WDR aus seiner Sicht [0:06]'}]},
 {'t': '🔍 RAF als Schlüssel', 'k': [{'t': 'Recherche 1992 zur dritten Generation [0:08]'}, {'t': 'Aufklärungsquote 0 % [0:09]'}, {'t': 'Peter Urbach (Gastgeber) [0:11]'}, {'t': 'Fahndungsplakate als Phantome [0:12]'}]},
 {'t': '⚓ Vorgeschichte', 'k': [{'t': 'Strategiepapier und Pearl Harbor [0:15]'}, {'t': 'Kinofilm als Repetitorium [0:16]'}, {'t': 'Stafettenlauf der Begriffe [0:18]'}, {'t': 'Ende des Kalten Kriegs, neuer Feind [0:21]'}, {'t': 'Al-Qaida und Huntington [0:25–0:28]'}]},
 {'t': '✈️ Der 11. September', 'k': [{'t': 'Täter in 48 Stunden [0:19]'}, {'t': 'Keine Abfangjäger [0:38]'}, {'t': 'Ausweisfund und Flugschüler [0:40–0:42]'}, {'t': 'Pentagon-Topografie [0:46]'}, {'t': 'Shanksville: kein Flugzeug [0:49]'}]},
 {'t': '🌍 Kriege & Migration', 'k': [{'t': 'NATO-Bündnisfall [0:31]'}, {'t': 'Libyen und Gaddafi [0:33]'}, {'t': 'Irakkrieg und Iran-Irak-Krieg [0:52]'}, {'t': 'Liste der sieben Länder [1:35]'}]},
 {'t': '📰 Medien 2003', 'k': [{'t': 'Spiegel-Titel [0:56]'}, {'t': 'WDR-Runde als Tribunal [1:03]'}, {'t': 'Humboldt-Uni und Horst Mahler [1:10]'}, {'t': 'Beschäftigungsverbot [1:22]'}, {'t': 'Bücherversenkung [1:25]'}, {'t': 'Trauma und Folgen [1:32]'}]},
 {'t': '🛰️ Überwachung', 'k': [{'t': 'Patriot Act [1:35]'}, {'t': 'TIA und Palantir (Gastgeber) [1:37]'}, {'t': 'Schnüffelindustrie und KI [1:40]'}, {'t': 'Drohnen und Sicherheit vor dem Staat [1:43–1:46]'}]},
 {'t': '🇩🇪 Deutschland heute', 'k': [{'t': 'Demokratie und AfD [1:47]'}, {'t': 'Anschläge und Failed State [1:51]'}, {'t': 'Krieg mit Russland? [1:54]'}]},
]

STECK = [
 ['**Thema in einem Satz**', 'Gerhard Wisnewski erklärt zum 25. Jahrestag, warum er die offizielle Darstellung des 11. September für falsch hält, und erzählt von seinem Film 2003 und dem Gegenwind, der darauf folgte.'],
 ['**Titel**', TITEL],
 ['**Format**', 'Video-Interview in der Sendung „Good Morning Germany“, Teil 1 der Reihe „9/11 Chronicles“; nach technischen Problemen teils neu aufgenommen [0:02]; eingeblendeter Ausschnitt von der Humboldt-Universität [1:15–1:16] und Bildschirmfreigabe einer ZDF-Doku [1:07]; Hinweise auf Buch und Links in der Beschreibung, keine Werbeblöcke'],
 ['**Sprecher**', '👤 **Gerhard Wisnewski** – Gast, Buch- und Filmautor · 🎙️ **Gastgeber** von REALTALK MEDIA – Name im Video nicht genannt ❓; spricht selbst längere Passagen (u. a. [0:10–0:11], [0:36–0:37], [1:17–1:21], [1:37–1:39])'],
 ['**Dauer**', '2 Std. 4 Min. (2:04:34)'],
 ['**Datum**', 'Veröffentlichung nicht ermittelt (2026 ❓); aufgenommen vermutlich im Spätsommer 2026 zum 25. Jahrestag, vor der im Gespräch noch bevorstehenden Landtagswahl in Sachsen-Anhalt ❓'],
 ['**Grundton**', 'zustimmend; der Gastgeber teilt die Grundsicht, widerspricht nicht, ergänzt eigene Thesen und lobt den Gast'],
 ['**Hinweis**', 'Aussagen beider Sprecher sind als ihre Sicht wiedergegeben; daneben steht im Abgleich, was amtliche Berichte und Quellen sagen. Aussagen über lebende Personen stehen nur als Wiedergabe mit Fundstelle.'],
]

INKUERZE = [
 '**Wer:** Gerhard Wisnewski (geb. 1959), Buch- und Filmautor, früher freier Mitarbeiter des WDR, im Gespräch mit dem (namentlich nicht genannten ❓) Gastgeber von REALTALK MEDIA – Teil 1 der Reihe „9/11 Chronicles“ zum 25. Jahrestag.',
 '**Ausgangspunkt:** Seine Recherche zur RAF-Spätzeit ab 1992 – ungeklärte Morde, Fahndungsplakate ohne Beweis – habe ihn gelehrt, dieselben Muster am 11.9. zu erkennen [0:08–0:13].',
 '**Vorgeschichte:** Ein Strategiepapier (2000) sprach von einem Ereignis „wie Pearl Harbor“; nach dem Kalten Krieg habe der Westen mit dem islamistischen Terror einen neuen Feind gebraucht [0:15–0:31].',
 '**Der Tag:** Täter binnen 48 Stunden benannt, keine Abfangjäger, ein unversehrter Ausweis, ungeschickte Flugschüler – für ihn ein „Kuriositätenkabinett“ [0:19–0:44].',
 '**Vor Ort 2003:** Am Pentagon hält er das Flugmanöver für unmöglich; in Shanksville habe ihm der Bürgermeister gesagt, „da war kein Flugzeug“ [0:46–0:50].',
 '**Gegenwind:** Spiegel-Titel, eine WDR-Runde, die er „Tribunal“ nennt, Störung an der Humboldt-Universität mit Horst Mahler im Saal, Ende beim WDR [0:55–1:33].',
 '**Folgen:** „Krieg, Konfrontation und Kontrolle“ – Patriot Act, Überwachungsindustrie, KI und Drohnen; für Deutschland sieht er die Gefahr eines „Failed State“ [1:34–1:57].',
 '**Im Abgleich:** Zeiten und Abläufe laut 9/11-Kommission, NIST und ASCE, Gegenstimmen (UAF-Studie) und was amtliche Stellen später selbst an Fehlern und Freigaben festhielten.',
]

ROTER = [
 '[seine Sicht] Geheimdienste inszenieren Anschläge und liefern die Täter gleich mit – das habe er bei der RAF gelernt und am 11.9. auf globaler Ebene wiedererkannt.',
 '[seine Sicht] Der 11.9. sei vorbereitet worden, begrifflich („neues Pearl Harbor“) wie politisch, um nach dem Ende des Kalten Kriegs einen neuen Feind und neue Kriege zu rechtfertigen.',
 '[seine Sicht] Die offiziellen Abläufe – fehlende Abfangjäger, Pentagon, Shanksville – seien physikalisch und organisatorisch nicht stimmig.',
 '[seine Sicht] Wer 2003 Fragen stellte, sei von Leitmedien und Sender in einer abgestimmten Kampagne beschädigt worden; er und sein Kollege hätten das mit der Fernsehkarriere bezahlt.',
 '[seine Sicht] Heute lebe man in der „Post-9/11-Welt“: Überwachung, KI und Drohnen bedrohten die Freiheit mehr als jeder Terror – nötig sei „Sicherheit vor dem Staat“.',
]

# ---------- Reiter 3: Zeitachse & Verzeichnisse ----------
ZEIT = [
 ('7.12.1941', 1941, 'Japanischer Angriff auf Pearl Harbor; Kriegseintritt der USA', '[0:15]', False),
 ('30.11.1959', 1959, 'Gerhard Wisnewski in Krumbach (Schwaben) geboren (laut Gemini, von ihm bestätigt)', '[0:02]', False),
 ('1962', 1962, 'Kubakrise – Sinnbild der Atomkriegsangst im Kalten Krieg', '[0:29]', True),
 ('11.4.1968', 1968, 'Attentat auf Rudi Dutschke; danach laut Gastgeber Molotowcocktails durch V-Mann Peter Urbach', '[0:11]', True),
 ('1970er', 1975, 'Operation Mockingbird laut Gastgeber aufgedeckt', '[1:00]', False),
 ('1979', 1979, 'Abitur; Arbeit für Frankfurter Neue Presse und Bild Frankfurt', '[0:03]', False),
 ('Dez. 1979', 1979, 'Sowjetische Intervention in Afghanistan (im Gespräch „1978“)', '[0:28]', True),
 ('1980–1988', 1980, 'Iran-Irak-Krieg; laut Gastgeber über eine Million Tote', '[0:52]', True),
 ('1981–1990', 1981, 'Studium der Politikwissenschaft in München', '[0:03]', False),
 ('1986', 1986, 'Wisnewski wird freier Buch- und Filmautor', '[0:03]', False),
 ('10.10.1986', 1986, 'Mord an Gerold von Braunmühl (RAF zugeschrieben)', '[0:09]', True),
 ('30.11.1989', 1989, 'Mord an Alfred Herrhausen (RAF zugeschrieben)', '[0:08]', True),
 ('1989', 1989, 'Mauerfall; laut Gastgeber danach Neonazi-Aufmärsche in Berlin', '[1:18]', False),
 ('1.4.1991', 1991, 'Mord an Detlev Karsten Rohwedder (RAF zugeschrieben)', '[0:09]', True),
 ('1991', 1991, 'Auflösung von Warschauer Pakt und Sowjetunion', '[0:21]', True),
 ('1992', 1992, 'Beginn der Recherche zur „dritten Generation“ der RAF', '[0:08]', False),
 ('1992', 1992, 'Fukuyama: „Das Ende der Geschichte“', '[0:21]', True),
 ('29.5.1993', 1993, 'Brandanschlag von Solingen (im Gespräch „1992“)', '[1:53]', True),
 ('1996', 1996, 'Huntington: „The Clash of Civilizations“ (Buch; im Gespräch „Mitte der 90er“)', '[0:27]', True),
 ('Sept. 2000', 2000, 'PNAC-Papier „Rebuilding America’s Defenses“ mit dem Pearl-Harbor-Satz', '[0:15]', True),
 ('2000', 2000, 'Film „Das Phantom“ nach dem Buch „Das RAF-Phantom“ wird ausgezeichnet', '[0:03]', False),
 ('2001', 2001, 'Kinofilm „Pearl Harbor“ (laut Wisnewski „im Juli oder so“; US-Start Mai 2001 ❓)', '[0:16]', False),
 ('11.9.2001', 2001, 'Anschläge in New York, am Pentagon und bei Shanksville', '[0:05]', False),
 ('12.9.2001', 2001, 'NATO ruft erstmals den Bündnisfall nach Artikel 5 aus', '[0:31]', True),
 ('7.10.2001', 2001, 'Beginn des Kriegs in Afghanistan', '[0:19]', True),
 ('26.10.2001', 2001, 'USA PATRIOT Act unterzeichnet', '[1:35]', True),
 ('Anfang 2003', 2003, 'Dreharbeiten in den USA als Touristen: Ground Zero, Pentagon, Shanksville', '[0:44–0:50]', False),
 ('20.3.2003', 2003, 'Beginn des Irakkriegs; Wisnewski reist laut eigener Angabe zwei Tage vorher aus', '[0:50]', True),
 ('20.6.2003', 2003, 'WDR sendet „Aktenzeichen 11.9. ungelöst“ (laut Gemini)', '[0:05]', False),
 ('8.9.2003', 2003, 'Spiegel-Titelgeschichte über 9/11-Bücher', '[0:56]', True),
 ('10.9.2003', 2003, 'WDR-Sendung „Wahrheit oder Täuschung?“ (vermutlich die „Tribunal“-Runde ❓)', '[1:03]', True),
 ('2003', 2003, 'Veranstaltung „Der inszenierte Terrorismus“ an der Humboldt-Universität (Datum ❓)', '[1:10]', False),
 ('2003', 2003, 'Ende der Zusammenarbeit mit dem WDR', '[0:05], [1:22]', False),
 ('2005', 2005, 'Debütalbum des Gastgebers mit 9/11-Bezug', '[0:11]', False),
 ('2006', 2006, 'Umfrage: laut Gastgeber 65 % der US-Bürger lehnen die Regierungsdarstellung ab', '[1:29]', False),
 ('2.3.2007', 2007, 'Wesley Clark berichtet von „sieben Ländern in fünf Jahren“', '[0:18]', True),
 ('2007/08', 2007, 'Kanal des Gastgebers wegen „Free Palestine“ gesperrt (seine Angabe)', '[1:58]', False),
 ('2008', 2008, 'Seitdem publiziert Wisnewski vor allem außerhalb etablierter Medien (Kopp-Verlag, Compact)', '[0:03]', False),
 ('2011', 2011, 'Krieg gegen Libyen; Sturz Gaddafis', '[0:33–0:35]', True),
 ('2011 ❓', 2011, 'Broders „Bücherversenkung“ (laut Wisnewski wohl zum 10. Jahrestag)', '[1:25]', False),
 ('2012', 2012, 'Wisnewski im Iran (laut Gastgeber)', '[1:58]', False),
 ('19.12.2016', 2016, 'Anschlag am Breitscheidplatz (Anis Amri)', '[1:42]', True),
 ('7.10.2023', 2023, 'Hamas-Angriff auf Israel – laut Gastgeber das „neue 9/11“', '[0:17]', True),
 ('23.8.2024', 2024, 'Messeranschlag in Solingen', '[1:42]', True),
 ('2026', 2026, '25. Jahrestag; Neuauflage von „Operation 9/11“; laut Wisnewski „Irankrieg“', '[0:21–0:22]', False),
 ('2026 ❓', 2026, 'Anschlag auf einen CSD und Debatte um die Landtagswahl in Sachsen-Anhalt (laut Gesprächspartnern)', '[1:42], [1:50]', False),
]

PERS = [
 ['Gerhard Wisnewski', 'Buch- und Filmautor, geb. 1959; „Das RAF-Phantom“, „Operation 9/11“, Jahrbuch „verheimlicht – vertuscht – vergessen“', 'Gast', '[0:02]–[2:02]'],
 ['Gastgeber', 'Moderator von REALTALK MEDIA („Good Morning Germany“); Name nicht genannt ❓', 'Gastgeber, eigene längere Thesen', 'durchgehend'],
 ['Willy Brunner', 'Mitautor von „Aktenzeichen 11.9. ungelöst“', 'verlor laut Wisnewski seine Existenz als TV-Produzent', '[0:05], [1:22], [1:32]'],
 ['Dennis Gansel', 'Regisseur des Films „Das Phantom“', 'Grimme-Preis', '[0:04]'],
 ['Mathias Bröckers', 'Autor zu 9/11', 'erste Welle; nächster Gast der Reihe', '[0:07], [0:20], [2:03]'],
 ['Andreas von Bülow', 'früherer Bundesminister, Autor zu 9/11', 'erste Welle; Ausschnitt Humboldt-Uni', '[0:07], [0:42], [1:16]'],
 ['Thierry Meyssan', 'französischer Journalist', 'im Spiegel-Titel genannt', '[0:57]'],
 ['Ekkehard Sieker ❓', 'Mitautor „Das RAF-Phantom“ (im Transkript „Ecke Harzeker“)', 'Vortrag Humboldt-Uni', '[1:11]'],
 ['Alfred Herrhausen, Detlev Karsten Rohwedder, Gerold von Braunmühl', 'RAF zugeschriebene Mordopfer', 'Beispiele ungeklärter Taten', '[0:08–0:09]'],
 ['Peter Urbach', 'V-Mann des Verfassungsschutzes', 'Beispiel des Gastgebers', '[0:11]'],
 ['Osama bin Laden', 'Al-Qaida-Anführer', 'laut Wisnewski „praktisch ein CIA-Mann“', '[0:19], [0:36–0:38]'],
 ['George H. W. Bush', 'früherer US-Präsident', 'angebliches Treffen mit bin-Laden-Bruder (Gastgeber) ❓', '[0:37]'],
 ['Satam al-Suqami, Mohammed Atta', 'Entführer laut 9/11-Kommission', 'Ausweisfund', '[0:40–0:42]'],
 ['Ernie Stull', 'Bürgermeister von Shanksville 2003', '„da war kein Flugzeug“', '[0:48–0:50], [0:55]'],
 ['Saddam Hussein, Muammar al-Gaddafi', 'Staatschefs Irak, Libyen', 'Kriege nach 9/11', '[0:33], [0:52]'],
 ['Samuel Huntington', 'US-Politikwissenschaftler', '„Clash of Civilizations“', '[0:27]'],
 ['Kelly M. Greenhill', 'Politikwissenschaftlerin („Weapons of Mass Migration“)', 'vom Gastgeber genannt', '[0:35]'],
 ['Wesley Clark', 'früherer NATO-Oberbefehlshaber', 'Länderliste', '[0:18]'],
 ['John Kiriakou', 'früherer CIA-Mitarbeiter', 'vom Gastgeber zitiert', '[1:00]'],
 ['Eva Herman', 'Moderatorin', 'Vergleich Kerner-Show', '[1:05]'],
 ['Horst Mahler', 'früher RAF, später Rechtsextremist', 'saß im Publikum der Humboldt-Uni', '[1:11–1:13]'],
 ['Henryk M. Broder', 'Publizist', '„Bücherversenkung“; Kritik des Gastgebers', '[1:23–1:29]'],
 ['Wolfgang Eggert ❓', 'Autor (im Transkript „Wolfgang Edgar“)', 'Buch mit Wisnewskis Vorwort', '[1:26]'],
 ['Ken Jebsen (Kayvan Soufi-Siavash)', 'früher RBB/Fritz', 'Gastgeber war dort Gast', '[1:28]'],
 ['Richard Perle, John Poindexter, Alex Karp, Peter Thiel', 'US-Politiker bzw. Palantir', 'Erzählung des Gastgebers zu Palantir', '[1:38–1:39]'],
 ['Helmut Schmidt, Helmut Kohl', 'Bundeskanzler', 'Erdgas-Röhren-Geschäft (Gastgeber)', '[1:37–1:38]'],
 ['Dirk Pohlmann', 'Filmemacher', 'Quelle des Gastgebers', '[0:10], [1:38]'],
 ['Boris Pistorius, Annalena Baerbock', 'Bundespolitiker', '„kriegsfähig“; Russland-Aussage', '[1:54–1:56]'],
 ['Dietrich Eckart, Rudolf von Sebottendorf', 'völkische Akteure, Thule-Gesellschaft', 'Gesprächsepisode des Gastgebers', '[1:20]'],
 ['Wisnewskis Sohn', '—', 'Video-Gespräch über die Anfänge der Bewegung', '[0:08], [0:33], [2:01]'],
]

ORTE = [
 ['Krumbach (Schwaben)', 'Geburtsort Wisnewskis', '[0:02]'],
 ['Frankfurt am Main, München', 'Schulzeit, Studium', '[0:03]'],
 ['New York, Ground Zero', 'Anschlagsort; 2003 bereits geräumt', '[0:46]'],
 ['Pentagon (Arlington)', 'Anschlagsort; Topografie im Gespräch', '[0:46–0:47]'],
 ['Shanksville (Pennsylvania)', 'Absturzort Flug 93', '[0:48–0:50]'],
 ['Florida', 'Aufenthalt der Täter (Gastgeber)', '[0:43]'],
 ['Brüssel, NATO-Hauptquartier', 'Bündnisfall 2001', '[0:31]'],
 ['Humboldt-Universität Berlin, Audimax', 'Veranstaltung 2003', '[1:10–1:14]'],
 ['Berlin-Kreuzberg, Wedding', 'Jugend des Gastgebers', '[1:17–1:19]'],
 ['Afghanistan, Irak, Libyen, Syrien, Iran', 'Kriege nach 9/11', '[0:21–0:22], [1:35]'],
 ['Saudi-Arabien', 'Herkunft der meisten Täter', '[0:36]'],
 ['Ceuta (Spanien)', 'Beispiel „Migrationskrieg“', '[0:34]'],
 ['Pearl Harbor (Hawaii)', 'Angriff 1941', '[0:15–0:16]'],
 ['Ukraine', 'Drohnennetze; Präsidentenwechsel 2014', '[0:30], [1:45]'],
 ['Sachsen-Anhalt', 'bevorstehende Landtagswahl', '[1:48–1:50]'],
 ['Solingen', 'Anschläge 1993 und 2024', '[1:42], [1:53]'],
]

BEGR = [
 ['Phantomterrorismus', 'Wisnewskis Begriff für Anschläge mit behaupteten, aber nicht bewiesenen Tätern', '[0:09], [0:13]'],
 ['RAF, „dritte Generation“', 'Rote Armee Fraktion; Mordanschläge 1985–1993 mit größtenteils unbekannten Tätern', '[0:08]'],
 ['„katalysierendes Ereignis“', 'Formulierung im PNAC-Papier 2000 („like a new Pearl Harbor“)', '[0:15]'],
 ['Stafettenlauf der Begriffe', 'Wisnewskis Bild: „Pearl Harbor“ → „9/11“ → „7. Oktober“', '[0:18]'],
 ['Krieg gegen den Terror', 'Sammelbegriff der USA für Militäreinsätze nach 9/11', '[0:22]'],
 ['Al-Qaida', 'arabisch „die Basis“; laut Wisnewski ursprünglich eine Liste', '[0:25–0:28]'],
 ['Clash of Civilizations', 'Huntingtons These vom „Kampf der Kulturen“', '[0:27]'],
 ['Artikel 5 NATO-Vertrag', 'Beistandsklausel; 2001 erstmals angewandt', '[0:31]'],
 ['Weapons of Mass Migration', 'Buch von K. M. Greenhill über Migration als Druckmittel', '[0:35]'],
 ['unansweredquestions.org', 'US-Gruppe mit Fragen zu 9/11, 2003 besucht', '[0:45]'],
 ['Architects & Engineers for 9/11 Truth, Pilots for 9/11 Truth', 'Vereinigungen, die die amtlichen Berichte bestreiten', '[0:43]'],
 ['Atlantik-Brücke', 'deutsch-amerikanischer Verein; laut Wisnewski Steuerungsinstrument', '[0:58]'],
 ['Operation Mockingbird', 'laut Gastgeber CIA-Einfluss auf Medien', '[1:00]'],
 ['Kontaktschuld', 'Schluss von einer anwesenden Person auf alle Beteiligten', '[1:13]'],
 ['USA PATRIOT Act', 'US-Antiterrorgesetz vom Oktober 2001', '[1:35]'],
 ['Total Information Awareness', 'Überwachungsprogramm des Pentagons; laut Gastgeber Vorläufer von Palantir', '[1:37]'],
 ['Gotham, VeRA', 'Palantir-Software bzw. Analyseplattform bei der Polizei', '[1:39]'],
 ['Failed State', 'gescheiterter Staat; laut Wisnewski Ziel der „Eliten“', '[1:52], [1:56]'],
 ['9/11 Chronicles', 'Gesprächsreihe des Kanals zum 25. Jahrestag', '[1:34], [2:03]'],
]

ZAHL = [
 ['Aufklärungsquote bei Mord', 'sonst 95 %, bei der RAF-Spätzeit 0 %', '[0:09]'],
 ['Zeit bis zur Benennung der Täter', '„innerhalb von 48 Stunden“', '[0:19]'],
 ['Terrorakte der Geschichte', '„größte“ der letzten 150 bis 300 Jahre (Gastgeber)', '[0:02]'],
 ['Gespräch mit dem Sohn', 'zweieinhalb Stunden', '[0:33]'],
 ['Iran-Irak-Krieg', '8 Jahre statt 8 Wochen, über 1 Mio. Tote (Gastgeber)', '[0:52]'],
 ['Verhaftungen von Israelis', '„bis zu 100“ (Gastgeber)', '[0:53]'],
 ['Personen im Spiegel-Titel', 'vier', '[0:57]'],
 ['WDR-Runde', '5 Experten + Journalist + Moderator + 6 Einspieler – „10 oder 11“ gegen einen', '[1:03]'],
 ['Gangs in Kreuzberg', 'mindestens zehn, teils 100 Mitglieder (Gastgeber)', '[1:18]'],
 ['Ablehnung der Regierungsdarstellung (USA 2006)', '65 % (Gastgeber)', '[1:29]'],
 ['Patriot Act', '345 Seiten', '[1:35]'],
 ['Länderliste nach 9/11', 'sieben Länder', '[1:35]'],
 ['Zustimmung zu einem Podcast', 'über 95 % (Gastgeber)', '[2:00]'],
]

# ---------- Reiter 4: Abgleich ----------
AB = [
 ['WDR-Film und Spiegel 2003: Der Film habe den Kriegsgrund „kaputt“ gemacht, darauf sei eine „Schmutzkampagne“ gefolgt [0:05–0:07], [0:56–0:58].',
  'Der Spiegel brachte am 08.09.2003 eine Titelgeschichte über Bücher zum 11. September; behandelt wurden u. a. Thierry Meyssan, Andreas von Bülow, Gerhard Wisnewski sowie Mathias Bröckers und Andreas Hauß. Den Wortlaut zur angeblich „manipulierten“ Interviewaussage (Gemini-Angabe [0:05]) habe ich nicht im Original geprüft ❓.',
  Q['wortfeld']],
 ['WDR-Runde als „Tribunal“ [1:03–1:06].',
  'Der WDR strahlte am 10. September 2003 die Sendung „Wahrheit oder Täuschung? Verschwörungstheorien zum 11. September“ aus; ob es sich um die beschriebene Runde handelt, ist naheliegend, aber nicht bestätigt ❓.',
  Q['freitag']],
 ['Shanksville: Laut Bürgermeister „kein Flugzeug“ [0:48–0:50].',
  'Laut 9/11-Kommission stürzte United 93 um 10:03:11 Uhr bei Shanksville ab, 125 Meilen von Washington entfernt; die Luftverteidigung (NEADS) erfuhr erst um 10:07 Uhr davon. Der Freitag (2003) ordnet den Satz des Bürgermeisters als ersten Eindruck eines tagelangen Bergungsgeschehens ein.',
  Q['cr1'] + ' · ' + Q['freitag']],
 ['Pentagon: Eine Boeing 757 könne das bodennahe Manöver nicht fliegen; kaum Material, kleine Trümmerteile [0:43–0:47].',
  'Die 9/11-Kommission gibt den Einschlag von American 77 im Pentagon mit 9:37:46 Uhr an. Ein Ingenieurteam der ASCE untersuchte das Gebäude und veröffentlichte im Januar 2003 den Pentagon Building Performance Report; danach half die Bauweise, die Schäden nach dem Flugzeugeinschlag zu begrenzen.',
  Q['cr1'] + ' · ' + Q['asce'] + ' · ' + Q['asce2']],
 ['Keine Abfangjäger, obwohl Kursabweichungen Routine-Begleitung auslösen [0:38–0:39].',
  'Laut 9/11-Kommission erhielt NEADS beim ersten Flugzeug neun Minuten vor dem Einschlag Nachricht; von United 93 erfuhr NEADS erst nach dem Absturz. Die Kommission meldete 2004 zudem ungenaue Angaben von FAA und NORAD über Meldezeiten an die Generalinspekteure (siehe Prüfstand).',
  Q['cr1'] + ' · ' + Q['oig']],
 ['Zeitablauf: vier Flugzeuge, „ohne dass man abgefangen wird“ [0:38].',
  'Einschläge laut Kommission: American 11 um 8:46 Uhr (Nordturm), United 175 um 9:03 Uhr (Südturm), American 77 um 9:37:46 Uhr (Pentagon), United 93 um 10:03:11 Uhr (Shanksville).',
  Q['cr1']],
 ['Architects & Engineers for 9/11 Truth: „so hat es nicht stattgefunden“ [0:43].',
  'Zu WTC 7 (im Gespräch nicht eigens genannt): NIST nennt Feuer als Hauptursache; durch Wärmeausdehnung versagte Säule 79, es folgte ein fortschreitender Einsturz um 17:20:52 Uhr. NIST fand keine Hinweise auf Sprengungen und hielt Thermit für „highly unlikely“; einen Abschnitt von rund 2,25 Sekunden im freien Fall räumt NIST im Endbericht (23.11.2008) ein.',
  Q['nist7']],
 ['(Gegenstimme zu WTC 7) – passend zu [0:43].',
  'Eine Studie der University of Alaska Fairbanks (Leitung J. Leroy Hulsey, finanziert von AE911Truth) kommt zu dem Ergebnis, Feuer habe den Einsturz von WTC 7 nicht verursacht; sie spricht von einem fast gleichzeitigen Versagen aller Säulen. NIST wies einen darauf gestützten Antrag auf Berichtigung (2020) zurück; die anschließende Klage gegen NIST beschied ein Bundesgericht im August 2022 (Abweisung; Begründung hier nicht im Einzelnen geprüft ❓).',
  Q['uaf'] + ' · ' + Q['nistrfc'] + ' · ' + Q['klage']],
 ['Ein Strategiepapier sprach vom Bedarf eines „katalysatorischen Ereignisses“ wie Pearl Harbor [0:15].',
  'Das Papier „Rebuilding America’s Defenses“ des Project for the New American Century (September 2000) enthält den Satz, die Umgestaltung werde ohne ein „catastrophic and catalyzing event – like a new Pearl Harbor“ lange dauern. Mehrere Mitglieder wurden später Regierungsmitglieder.',
  Q['pnac']],
 ['Wesley Clark: Liste mit mehreren Stationen, die letzte sei Iran [0:18], [1:35].',
  'Clark sagte 2007 in einem Interview, ihm sei 2001 im Pentagon ein Papier erwähnt worden, „sieben Länder in fünf Jahren“ anzugreifen: Irak, Syrien, Libanon, Libyen, Somalia, Sudan und Iran. Ein solches Papier wurde nicht veröffentlicht.',
  Q['clark']],
 ['Erstmals in der Geschichte sei Artikel 5 des NATO-Vertrags aktiviert worden [0:31].',
  'Bestätigt: Die NATO rief den Bündnisfall nach Artikel 5 am 12.09.2001 erstmals aus und bestätigte ihn am 02.10.2001, nachdem die USA Belege zur Urheberschaft vorgelegt hatten.',
  Q['nato'] + ' · ' + Q['nato2']],
 ['Patriot Act als „345-Seiten-Konvolut“, vom Kongress „durchgewinkt“ [1:35].',
  'Der USA PATRIOT Act (Public Law 107-56) wurde am 26.10.2001 von Präsident Bush unterzeichnet, rund sechs Wochen nach den Anschlägen. Die genannte Seitenzahl habe ich nicht geprüft ❓.',
  Q['patriot'] + ' · ' + Q['patriot2']],
 ['„Täter binnen 48 Stunden mit Bildern“ – das könne nur gelogen sein [0:19].',
  'Die 9/11-Kommission (Abschlussbericht 2004) ordnet die Anschläge 19 Entführern im Auftrag von Al-Qaida zu und stützt das u. a. auf Passagierlisten, Ermittlungen und Aussagen von Inhaftierten. Wann FBI-Fahndungsfotos erstmals veröffentlicht wurden, habe ich nicht geprüft ❓.',
  Q['cr1']],
 ['Ausweis eines Täters (Satam al-Suqami) unversehrt gefunden [0:40–0:42].',
  'Dass ein Pass al-Suqamis in der Nähe des WTC gefunden wurde, wird in Unterlagen der 9/11-Kommission erwähnt; den genauen Fundbericht habe ich nicht im Original geprüft ❓.',
  '❓ nicht geprüft'],
 ['Gastgeber: bis zu 100 Verhaftungen von Israelis, ein Teil als Agenten „entlarvt“ [0:53–0:54].',
  'ABC News berichtete 2002 über fünf Israelis, die am 11.9. in New Jersey festgenommen, wochenlang festgehalten und wegen Verstößen gegen das Einwanderungsrecht abgeschoben wurden; laut Bericht fanden US-Behörden keine Belege für ein Vorwissen. Eine Zahl von „bis zu 100“ habe ich nicht belegt gefunden ❓.',
  Q['abc']],
 ['Gastgeber: 65 % der US-Bürger lehnten 2006 die Regierungsdarstellung ab [1:29].',
  'Eine Umfrage von Scripps-Howard und der Ohio University (2006) ergab, dass 36 % es für sehr oder etwas wahrscheinlich hielten, dass Regierungsvertreter die Anschläge zuließen oder ausführten. Andere Umfragen fragten anders und kamen zu anderen Werten.',
  Q['poll']],
 ['Die Opfer „hat’s leider gegeben in den Türmen“ [0:20].',
  'Bei den Anschlägen starben 2.977 Menschen: 2.753 in New York, 184 am Pentagon, 40 an Bord von Flug 93; darunter 441 Einsatzkräfte (343 der New Yorker Feuerwehr).',
  Q['mem']],
 ['Folgen: „Krieg, Konfrontation und Kontrolle“; Kriege in Afghanistan, Irak, Libyen, Syrien [0:21–0:22], [1:34].',
  'Das Costs-of-War-Projekt der Brown University schätzt 2021 die direkten Todesopfer der Kriege nach 9/11 auf 897.000 bis 929.000 und die US-Kosten auf rund 8 Billionen US-Dollar.',
  Q['brown']],
 ['Die „Schnüffelindustrie“ habe durch den 11.9. einen Schub bekommen [1:40].',
  'Das US-Budget für das National Intelligence Program lag laut CRS 1998 bei 26,7 Mrd. US-$, 2006 bei 40,9 Mrd. und 2010 bei 53,1 Mrd. US-$ (nominal); für 1999–2004 liegen keine veröffentlichten Werte vor. Der Bericht selbst schreibt den Anstieg nicht ausdrücklich dem 11.9. zu.',
  Q['crs']],
]

DIA = []
DIA.append({'typ': 'kurs', 'id': 'wisnewski-nip', 'titel': '📈 US-Geheimdienstbudget (National Intelligence Program), nominal',
  'reihen': [{'name': 'National Intelligence Program', 'kurz': 'Mrd. US-$', 'einheit': 'Mrd. US-$', 'dez': 1, 'hoeherGut': None,
    'punkte': [[1998, 26.7], [2005, 39.8], [2006, 40.9], [2007, 43.5], [2008, 47.5], [2009, 49.8], [2010, 53.1], [2011, 54.6], [2012, 53.9], [2013, 49.0], [2014, 50.5], [2015, 50.3], [2016, 53.0]]}],
  'hoeherGut': None, 'vergleich': False,
  'quelle': Q['crs'] + ', Tabelle der bewilligten Mittel, Stand Nov. 2016 (1999–2004 nicht veröffentlicht; 2013 nach Sequestrierung)',
  'hinweis': 'Bezug zum Gespräch [1:40]: „Schnüffelindustrie“ mit Legitimationsschub durch 9/11. Gezeigt ist nur das zivile NIP-Budget (ohne Military Intelligence Program); die Lücke 1999–2004 ist im Verlauf überbrückt.'})
DIA.append({'typ': 'balken', 'titel': '📊 Todesopfer der Anschläge vom 11. September 2001 nach Ort', 'einheit': 'Menschen', 'dez': 0,
  'zeilen': [['New York (World Trade Center)', 2753], ['Pentagon', 184], ['Flug 93 (Shanksville)', 40]],
  'quelle': Q['mem'] + ', Stand 2021', 'hinweis': 'Bezug zum Gespräch [0:20], [0:48]: insgesamt 2.977 Tote; dazu 6 Tote des Anschlags von 1993, die ebenfalls auf dem Memorial stehen.'})
DIA.append({'typ': 'balken', 'titel': '📊 Getötete Einsatzkräfte am 11. September 2001', 'einheit': 'Menschen', 'dez': 0,
  'zeilen': [['Feuerwehr New York (FDNY)', 343], ['Polizei der Port Authority', 37], ['Polizei New York (NYPD)', 23]],
  'quelle': Q['mem'] + ', Stand 2021', 'hinweis': 'Bezug zum Gespräch [0:20]. Insgesamt starben laut Memorial 441 Einsatzkräfte aus über 30 Behörden.'})
DIA.append({'typ': 'balken', 'titel': '📊 Ablauf am 11. September 2001 – Minuten nach dem ersten Einschlag (8:46 Uhr)', 'einheit': 'Minuten', 'dez': 0,
  'zeilen': [['United 175 trifft den Südturm (9:03)', 16], ['American 77 trifft das Pentagon (9:37:46)', 51], ['United 93 stürzt bei Shanksville ab (10:03:11)', 77], ['NEADS erfährt von United 93 (10:07)', 80], ['Einsturz von WTC 7 (17:20:52)', 514]],
  'quelle': Q['cr1'] + ' · ' + Q['nist7'], 'hinweis': 'Bezug zum Gespräch [0:38–0:39], [0:48]: gerechnet ab 8:46:40 Uhr (American 11, Nordturm), auf ganze Minuten gerundet.'})
DIA.append({'typ': 'balken', 'titel': '📊 US-Kosten der Kriege nach 9/11 (Schätzung, Bio. US-$)', 'einheit': 'Bio. US-$', 'dez': 2,
  'zeilen': [['Afghanistan/Pakistan', 2.3], ['Irak/Syrien', 2.1], ['Künftige Versorgung von Veteranen', 2.2], ['Weitere Einsätze (u. a. Somalia, Afrika)', 0.355]],
  'quelle': Q['brown'], 'hinweis': 'Bezug zum Gespräch [0:21–0:22], [1:34]: Gesamtschätzung rund 8 Bio. US-$ einschließlich Zinsen; die Teilposten addieren sich nicht vollständig zur Summe.'})

SPANN = [
 'Der Gastgeber widerspricht an keiner Stelle; er stellt Fragen, ergänzt aber oft eigene Thesen (Urbach, Bin-Laden-Familie, „tanzende Israelis“, Palantir, Broder), die Wisnewski meist nicht aufgreift [0:11], [0:37], [0:53], [1:37], [1:23].',
 'Wisnewski selbst grenzt ab: Eine gezielte Inszenierung von Anschlägen, um die AfD zu stärken, „kann ich jetzt nicht unbedingt unterschreiben“ [1:52]; ob Broder mit Antifa oder Mahler in Kontakt stand, „kann ich natürlich nicht behaupten“ [1:27].',
 'Wisnewski betont, 2003 habe man „eigentlich nichts behauptet“, nur Fragen gestellt [0:55] – im heutigen Gespräch nennt er den 11.9. dagegen ausdrücklich eine „US-Regierungsaktion“ [0:38].',
 'Zwei Versprecher lassen den Sinn offen: „zwei andere sollen im Pentagon abgestürzt sein“ [0:06] und „noch viel mehr Belege …, dass dort eine Maschine reingeflogen ist“ [0:47] ❓.',
 'Der Gastgeber kündigt an, sich mit eigener Analyse zurückzuhalten [0:20], [0:24], spricht dann aber längere Passagen selbst.',
]
MIT = [
 'Die Zeiten des 11. September (Einschläge, Meldungen an die Luftverteidigung) sind im Bericht der 9/11-Kommission minutengenau nachlesbar – auch, dass NEADS von United 93 erst nach dem Absturz erfuhr.',
 'Auch amtliche Stellen haben Mängel festgehalten: ungenaue FAA/NORAD-Angaben (DOT-Generalinspekteur 2006), zurückgehaltene CIA-Bänder (Kean/Hamilton 2008), spät freigegebene „28 Seiten“ (2016) und FBI-Unterlagen (2021) – siehe Prüfstand.',
 'Zu WTC 7 gibt es einen amtlichen Bericht (NIST 2008) und eine universitäre Gegenstudie (UAF 2020); beide sind frei zugänglich und lassen sich nebeneinander lesen.',
 'Für die Medienseite 2003 sind Spiegel-Titel (08.09.2003) und WDR-Sendung (10.09.2003) datierbar; die Sicht der Gegenseite fehlt im Gespräch.',
]
OFFEN = [
 'Wer ist der Gastgeber von REALTALK MEDIA, und wann genau wurde das Video veröffentlicht?',
 'Was genau warf der Spiegel 2003 dem Film vor – und wie äußerte sich Ernie Stull später selbst zu seiner Aussage?',
 'Wann fand die Veranstaltung „Der inszenierte Terrorismus“ an der Humboldt-Universität statt, und wann lief Broders „Bücherversenkung“?',
 'Welche Quellen gibt es für die vom Gastgeber genannten 100 Verhaftungen, das Treffen eines bin-Laden-Bruders mit Bush senior und die Entstehung von Palantir aus TIA?',
 'Welcher Gewerkschafter und welcher CSD-Anschlag sind gemeint [1:42], [1:48–1:50]?',
]
WEITER = [
 '9/11 Commission Report (2004), Kapitel 1 und 9; Staff Statements zu FAA/NORAD und zu den Entführern.',
 'NIST NCSTAR 1 (Türme, 2005) und NCSTAR 1A (WTC 7, 2008) samt Kommentaren; UAF-Abschlussbericht (2020) und NISTs Antwort.',
 'ASCE: The Pentagon Building Performance Report (2003).',
 'Freigegebene „28 Seiten“ (2016) und FBI-Dokumente nach Executive Order 14040 (ab 2021).',
 'Spiegel 37/2003 und die WDR-Sendung vom 10.09.2003 im Archiv; Wisnewskis „Operation 9/11“ (Neuauflage 2026).',
 'Querverweis: {{a:ganser|Daniele Ganser (A-04)}} zu denselben Fragen (WTC 7, NATO, verdeckte Kriegsführung).',
]

# ---------- Zusammenbau ----------
def T(s): return f'{G}: {s}'
abschnitte = [dict(typ='abschnitt', titel=f"{a['titel']} [{a['von']}–{a['bis']}]", th=a['th'], liste=a['liste']) for a in A]
teile = [dict(von=a['von'], bis=a['bis'], t=kurztitel(a['titel']), th=a['th']) for a in A]
n_ab = len(A)
n_dia = len(DIA)
zeit = [dict(z=z, j=j, t=t, f=f, e=e) for (z, j, t, f, e) in ZEIT]
zeit.sort(key=lambda x: x['j'])

r1 = dict(id=K, titel=T('Überblick'), bloecke=[
 dict(typ='folge', k=K, titel=TITEL, gast=GAST, rolle='Buch- und Filmautor, früher freier Mitarbeiter des WDR', kanal=KANAL,
      datum=DATUM, dauer=DAUER, url=URL,
      thema='Gerhard Wisnewski erklärt bei REALTALK MEDIA zum 25. Jahrestag, warum er die offizielle Darstellung des 11. September für falsch hält – von der RAF-Recherche über Pentagon und Shanksville bis zum Gegenwind 2003 und den Folgen für Überwachung, Krieg und Deutschland.',
      kacheln=[[str(n_ab), 'Abschnitte'], ['10', 'Kernaussagen'], [str(len(AB)), 'Abgleich-Punkte'], [str(len(zeit)), 'Zeitachse'], [str(n_dia), 'Diagramme']]),
 dict(typ='hinweis', text='Auswertung nach dem Transkript (automatische Untertitel): Gesagtes ohne Zeichen, Ergänzungen 📚, Unklares ❓. Fundstellen [Stunde:Minute] springen ins Video. Die Bewertung bleibt dem Leser.'),
 dict(typ='abschnitt', titel='⚡ In Kürze', liste=INKUERZE),
 dict(typ='abschnitt', titel='🔦 Aus Wisnewskis Sicht – der rote Faden', liste=ROTER),
 dict(typ='text', text='🎯 **Kernaussagen** – die zehn wichtigsten Thesen des Gesprächs:'),
 dict(typ='tabelle', kopf=['#', 'Aussage', 'Begründung im Gespräch', 'Fundstelle', 'Gewicht'], zeilen=KERN),
 dict(typ='baum', titel='🌳 Themenbaum des Gesprächs', wurzel=TITEL, unter=f'{GAST} · {KANAL} · {DATUM} · {DAUER}', knoten=BAUM),
 dict(typ='illu', id='wisnewski_muster', titel='Skizze: Das wiederkehrende Muster – von der RAF bis zum 11. September (Darstellung laut Wisnewski, schematisch)'),
 dict(typ='illu', id='wisnewski_ablauf', titel='Skizze: Der Vormittag des 11. September 2001 – Einschläge und Meldungen an die Luftverteidigung (belegte Daten)'),
 dict(typ='tabelle', kopf=['🧭 Steckbrief', ''], schmal=True, zeilen=STECK),
])
r2 = dict(id=K + 'ab', titel=T('Gespräch im Detail'), bloecke=[
 dict(typ='text', text=f'🔎 Detaillierte Auswertung in der Reihenfolge des Gesprächs – {n_ab} Abschnitte. Lesehilfe: 💬 Zitat, 📌 Aussage/Zahl/Beispiel, 🔗 Bezug, 📚 Ergänzung, ❓ unklar. Video: [{TITEL}]({URL})'),
 dict(typ='gespraech', titel='🧭 Gesprächsverlauf – wann worüber gesprochen wird', dauer='2:04', themen=THEMEN, teile=teile),
] + abschnitte)
r3 = dict(id=K + 'zeit', titel=T('Zeitachse & Verzeichnisse'), bloecke=[
 dict(typ='zeitachse', titel='📅 Zeitachse – Ereignisse, die im Gespräch vorkommen', eintraege=zeit),
 dict(typ='tabelle', kopf=['👤 Person', 'Wer / was', 'Rolle im Gespräch', 'Fundstelle'], zeilen=PERS),
 dict(typ='tabelle', kopf=['🗺️ Ort', 'Rolle', 'Fundstelle'], zeilen=ORTE),
 dict(typ='tabelle', kopf=['📖 Begriff', 'Erklärung', 'Fundstelle'], zeilen=BEGR),
 dict(typ='tabelle', kopf=['📊 Zahl im Gespräch', 'Angabe', 'Fundstelle'], zeilen=ZAHL),
])
r4 = dict(id=K + 'abgleich', titel=T('Abgleich & Daten'), bloecke=[
 dict(typ='text', text='Neutraler Abgleich: links die Aussage im Gespräch, rechts die gängige Darstellung bzw. Daten mit Quelle. Die Bewertung bleibt dem Leser.'),
 dict(typ='tabelle', kopf=['Aussage im Gespräch', 'Gängige Darstellung (Mainstream) / Daten 📚', 'Quelle'], stapel=True, zeilen=AB),
] + DIA + [
 dict(typ='abschnitt', titel='🧩 Spannungen im Gespräch', liste=SPANN),
 dict(typ='abschnitt', titel='💡 Was man mitnehmen kann', liste=MIT),
 dict(typ='abschnitt', titel='❓ Offen', liste=OFFEN),
 dict(typ='abschnitt', titel='🔎 Weiter recherchieren', liste=WEITER),
])

quellen = [[f'Video: {TITEL} – {KANAL} (YouTube)', URL]]
seen = set()
for v in Q.values():
    t, u = L(v)
    if u not in seen:
        seen.add(u); quellen.append([t, u])

out = dict(k=K, gast=GAST, reiter=[r1, r2, r3, r4],
 folgen_zeile=[DATUM, 'Gerhard Wisnewski (Buch- und Filmautor)', TITEL,
   '25 Jahre 9/11, RAF-Phantom, Pentagon & Shanksville, WDR & Spiegel 2003, Krieg gegen den Terror, Überwachung, Deutschland heute',
   f'{{{{a:realtalk-{K}|hier: {G}}}}}', f'[ansehen]({URL})'],
 baum_ast={'gruppe': '🏛️ Macht & Geschichte', 't': '👤 Gerhard Wisnewski bei REALTALK MEDIA – 25 Jahre 9/11, Pentagon, Shanksville, Medien 2003, Überwachung'},
 neu={'d': '2026-11-12', 't': 'REALTALK MEDIA – Gerhard Wisnewski', 'k': f'25 Jahre 9/11: Wisnewski über seinen Film von 2003, Pentagon, Shanksville und die Folgen – {n_ab} Abschnitte, Abgleich mit amtlichen Berichten, {n_dia} Diagramme.', 'h': '#a-realtalk-wisnewski', 'art': 'Video'},
 quellen=quellen,
 web=[['Gerhard Wisnewski – Buch „Operation 9/11“ (Neuauflage, Buchhandel)', 'https://www.ebook.de/de/product/54027611/gerhard_wisnewski_operation_9_11.html']])

here = os.path.dirname(os.path.abspath(__file__))
json.dump(out, open(os.path.join(here, 'folge.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', n_ab, 'Abschnitte,', len(AB), 'Abgleich,', n_dia, 'Diagramme,', len(zeit), 'Zeitachse,', len(quellen), 'Quellen')
