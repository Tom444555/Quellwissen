# -*- coding: utf-8 -*-
# Erzeugt folge.json für „Tom-Oliver Regenauer: Warum es jetzt gefährlich wird – Iran, Energiekrise & die wahren Drahtzieher“
# K = iran, Autor A-11 regenauer
import json, os
K = 'iran'; G = 'Iran und Energiekrise'
URL = 'https://www.youtube.com/watch?v=wwJX6gdF3Bc'
TITEL = 'Tom-Oliver Regenauer: Warum es jetzt gefährlich wird – Iran, Energiekrise & die wahren Drahtzieher'
GAST = 'Tom-Oliver Regenauer'
KANAL = 'REALTALK MEDIA'
DATUM = 'April 2026 ❓'
DAUER = '1 Std. 50 Min.'

# ---------- Quellen (alle in diesem Lauf bzw. im Vorlauf reg1 geprüft) ----------
Q = dict(
 ieatr='[IEA: 2026 Energy Crisis Policy Response Tracker](https://www.iea.org/data-and-statistics/data-tools/2026-energy-crisis-policy-response-tracker)',
 iea='[IEA: IEA launches tracker to monitor policy responses to energy market impacts of Middle East conflict](https://www.iea.org/news/iea-launches-tracker-to-monitor-policy-responses-to-energy-market-impacts-of-middle-east-conflict)',
 start='[Unione Sarda (01.03.2026): Teheran bestätigt Khamenei getötet – neue Angriffswelle gegen den Iran](https://www.unionesarda.it/de/welt/teheran-bestatigt-khamenei-getotet-neue-angriffswelle-gegen-den-iran-raketenangriffe-auf-israel-und-die-golfstaaten-trump-gute-kandidaten-fur-die-fuhrung-des-landes-jqwfjmhg)',
 bt='[Business Today (14.04.2026): Iran war was said to be ceasing – a timeline](https://www.businesstoday.in/world/story/iran-war-was-said-to-be-ceasing-is-it-now-set-to-flare-up-again-a-timeline-525555-2026-04-14)',
 paris='[Bundesregierung (17.04.2026): Für Stabilität im Nahen Osten – Kanzler in Paris](https://www.bundesregierung.de/breg-de/aktuelles/kanzler-paris-hormus-2421808)',
 ja='[Jüdische Allgemeine (16.04.2026): Auch während des Kriegs Rüstungsexporte nach Israel genehmigt](https://www.juedische-allgemeine.de/politik/auch-waehrend-kriegs-ruestungsexporte-nach-israel-genehmigt/)',
 hrana='[Al-Monitor (27.01.2026): Rights group says confirmed Iran protest toll over 6,000](https://www.al-monitor.com/originals/2026/01/rights-group-says-confirmed-iran-protest-toll-over-6000)',
 wallet='[Namirial (2026): Auf Kurs Richtung 2. Januar 2027 – der aktuelle Stand der deutschen EUDI-Wallet](https://focus.namirial.com/de/der-aktuelle-stand-der-deutschen-eudi-wallet/)',
 eia='[EIA, Today in Energy (16.06.2025): Amid regional conflict, the Strait of Hormuz remains critical oil chokepoint](https://eia.gov/todayinenergy/detail.php?id=65504)',
 brent='[FRED / IMF: Global price of Brent Crude (POILBREUSDA), Jahreswerte](https://fred.stlouisfed.org/data/POILBREUSDA)',
 burmah='[Wikipedia: Burmah Oil](https://en.wikipedia.org/wiki/Burmah_Oil)',
 cia='[Al Jazeera (20.08.2013): CIA admits organising 1953 Iran coup](https://aljazeera.com/news/2013/8/20/cia-admits-organising-1953-iran-coup)',
 ford='[American Jewish Archives: Henry Ford and Antisemitism – the notorious „Dearborn Independent“](https://www.americanjewisharchives.org/snapshots/henry-ford-and-antisemitism-the-notorious-dearborn-independent)',
 kellogg='[History.com: Dr. John Kellogg – cereal, wellness and wacky sanitarium treatments](https://www.history.com/news/dr-john-kellogg-cereal-wellness-wacky-sanitarium-treatments)',
 rbf='[Wikipedia: Race Betterment Foundation](https://en.wikipedia.org/wiki/Race_Betterment_Foundation)',
 carney='[CTV News (29.04.2025): Mark Carney, crisis-fighting central banker, to lead Canada through US trade war](https://www.ctvnews.ca/federal-election-2025/article/mark-carney-crisis-fighting-central-banker-to-lead-canada-through-us-trade-war/)',
 iaea='[Al Jazeera (12.06.2025): UN nuclear watchdog board finds Iran not complying with obligations](https://www.aljazeera.com/news/2025/6/12/un-nuclear-watchdog-says-iran-non-compliant-of-nuclear-safeguards)',
 ns='[LTO: Vom Generalbundesanwalt mit Haftbefehl gesucht – Nord-Stream-Verdächtiger in Polen festgenommen](https://www.lto.de/recht/nachrichten/n/generalbundesanwalt-nord-stream-haftbefehl-polen-ukraine-russland)',
 icc='[UN Nordic Office (21.11.2024): ICC issues arrest warrants for Netanyahu, Gallant and Hamas commander](https://un.dk/icc-issues-arrest-warrants-for-netanyahu-gallant-and-hamas-commander/)',
 deezer='[Music Business Worldwide (29.01.2026): 60,000 AI tracks hit Deezer daily](https://www.musicbusinessworldwide.com/60000-ai-tracks-hit-deezer-daily-as-platform-moves-to-license-detection-tech-to-wider-music-industry/)',
 bpb='[bpb, Glossar Antisemitismus: Struktureller Antisemitismus](https://www.bpb.de/themen/antisemitismus/dossier-antisemitismus/was-heisst-antisemitismus/glossar-antisemitismus/559900/struktureller-antisemitismus/)',
 fedb1='[Federal Reserve History: First Bank of the United States](https://www.federalreservehistory.org/essays/first-bank-of-the-us)',
 fedb2='[Federal Reserve History: Second Bank of the United States](https://www.federalreservehistory.org/essays/second-bank-of-the-us)',
)
def url(k):
    s = Q[k]; return s[s.rfind('(')+1:-1]
def tit(k):
    s = Q[k]; return s[1:s.rfind('](')]

def ab(titel, th, zus, *rest):
    return {"typ": "abschnitt", "titel": titel, "th": th, "liste": ["**Zusammenfassung:** " + zus] + list(rest)}

# ---------- Abschnitte (von, bis, Kurztitel, th, Block) ----------
A = []
def S(von, bis, kurz, th, emoji, titel, zus, *rest):
    A.append((von, bis, kurz, th, ab(f"{emoji} {titel} [{von}–{bis}]", th, zus, *rest)))

S('0:00','0:04','Teaser und Nachrichtenblock I','w','🎬','Teaser und Nachrichtenblock: Strafanzeige, Waffenexporte, Paris-Konferenz',
  "Das Video beginnt mit Ausschnitten aus dem späteren Gespräch (Energiezufuhr, Orwells ewiger Krieg, „Trumps Gestapo“, Grundeinkommen). Dann eröffnet der Gastgeber seine Sendung „Good Morning Germany“ mit einem satirisch moderierten Nachrichtenblock: Das European Legal Support Center (ELSC) unterstütze laut Meldung vom 14. April eine Strafanzeige in Deutschland gegen Regierungsbeamte und Rüstungsmanager wegen Beihilfe zu Verbrechen in Gaza; Deutschland sei nach den USA zweitgrößter Waffenlieferant Israels. Es folgen Meldungen von MintPress News (Rückgang des Publikums von Ben Shapiro um rund 85 %, ein israelisches Laborschokoladen-Produkt), Waffenexporte nach Israel auch während des Iran-Kriegs und die Pariser Konferenz zur Straße von Hormus.",
  "📌 Merz habe in Paris eine deutsche Beteiligung an Minenräumung und Seeaufklärung in Aussicht gestellt; der Gastgeber kommentiert spöttisch [0:03].",
  "📚 **Ergänzung:** Die Konferenz fand am 17.04.2026 statt; die Bundesregierung nennt als Bedingungen ein Ende der Kämpfe, eine Rechtsgrundlage (etwa ein Mandat des UN-Sicherheitsrats) und ein Bundestagsmandat – siehe Abgleich. Für Rüstungsexport-Genehmigungen nach Israel während des Iran-Kriegs nennt das Wirtschaftsministerium 6,6 Mio. € (28.02.–27.03.2026).",
  "❓ Die ELSC-Strafanzeige und die MintPress-Zahlen wurden nicht eigens geprüft.")
S('0:04','0:07','Nachrichtenblock II','w','📰','Nachrichtenblock: Nord Stream, Netanjahu, Milei, Palantir',
  "Weitere Meldungen des Gastgebers: Heino gehe juristisch gegen eine AfD-Wahlkampfaktion vor; Sahra Wagenknecht habe gepostet, Selenskyj solle die Nord-Stream-Sprengung persönlich genehmigt haben. Ein Comedian (Name im Transkript unklar ❓) habe gesagt, Netanjahu habe nichts mit dem Judentum zu tun. Der Gastgeber zeigt ein Video, in dem der Leiter des Presseamts von Netanjahu (Eli Hasan, Schreibweise ❓) sage, Fakten seien nicht mehr wichtig; er nennt das „Hasbara“. Es folgen Javier Milei an der Klagemauer, eine ganzseitige Palantir-Anzeige in der New York Times und eine Aussage über drei US-Präsidenten.",
  "📌 **Gastgeber:** Drei US-Präsidenten hätten in 23 Jahren neun Länder überfallen und dabei 11 Mio. Zivilisten getötet; keiner sei im Gefängnis [0:06] [seine Sicht].",
  "📌 Die Nord-Stream-Sprengung hätte man als „Kriegsakt gegen die deutsche Nation“ werten müssen (Gastgeber) [0:04].",
  "📚 **Ergänzung:** Zu Nord Stream ermittelt der Generalbundesanwalt; 2025 wurden zwei ukrainische Verdächtige in Italien und Polen festgenommen. Eine Genehmigung durch Selenskyj ist in den geprüften Quellen nicht festgestellt ❓ – siehe Abgleich.",
  "❓ Die Zahl „11 Millionen Zivilisten“ und der Wortlaut des Hasan-Videos (Hebräisch, im Transkript unverständlich) wurden nicht geprüft.")
S('0:07','0:11','Vorstellung, Logo und Brüssel','c','🎙️','Vorstellung, Senderlogo und das „Demokratie“-Banner in Brüssel',
  "Der Gastgeber stellt Regenauer als häufigen Gast seines Formats „100% Real Talk“ vor, erstmals bei „Good Morning Germany“, und lobt dessen Auftritt beim Kanal von Simo (Regenauer: damals rund 700.000 Aufrufe). Der Gastgeber erklärt sein Logo: das Orwell’sche Auge in den deutschen Farben, als Zeichen, dass man in einer Überwachungsgesellschaft lebe. Regenauer berichtet von einem riesigen Banner mit der Aufschrift „Demokratie“ am EU-Gebäude in Brüssel (geschätzt 20 m) – für ihn „orwellesk“, weil dort niemand gewählt sei.",
  "💬 „Zeit wird knapp“ – mehr Menschen sollten sich vorbereiten (Regenauer) [0:09].",
  "📌 Das Banner erinnere an Orwell, die Sowjetunion oder den Nationalsozialismus [seine Sicht] [0:10].",
  "❓ Gebäude, Datum und Größe des Banners wurden nicht geprüft.")
S('0:11','0:14','IEA-Tracker, Raffinerien, Hormus','b','⛽','IEA-Maßnahmen-Tracker, brennende Raffinerien und die „Blockade“',
  "Kernthema sei die aufziehende Energiekrise durch den Iran-Krieg. Ernst werde es, wenn die Internationale Energieagentur (IEA) eine eigene Webseite mit einem Tracker für Maßnahmen einrichte – von Preisdeckeln über Rationierung bis Homeoffice und Klimaanlagen bis 25 °C in Asien. IEA-Chef Fatih Birol sei seit Jahren ein „Net-Zero“-Verfechter; daher sei das nichts Kurzfristiges. In den letzten Wochen hätten auffällig viele Raffinerien gebrannt (Indien, eine Drohne in Russland) – er habe rund 45 Ereignisse, davon etwa 15–20 Raffinerien und Verarbeitungsanlagen, in einer Tabelle gesammelt.",
  "📌 Die „niemals blockierte“ Straße werde von den Amerikanern blockiert, „um eine Blockade zu verhindern“ – „völlig grotesk“ [0:13] [seine Sicht].",
  "📌 Ziel sei das Abschneiden der Energiezufuhr, die Mobilität, Wirtschaft und Sozialleben trage [0:13].",
  "📚 **Ergänzung:** Die IEA spricht von der größten Versorgungsstörung in der Geschichte des Ölmarkts; ihr Tracker erfasst Maßnahmen zur Energieeinsparung und zur Entlastung von Verbrauchern. Seit 13.04.2026 blockiert das US-Militär den Schiffsverkehr von und zu iranischen Häfen – siehe Abgleich.",
  "❓ Die Liste der rund 45 Raffinerie-Ereignisse wurde nicht geprüft.")
S('0:14','0:18','Technokratie, Tour, Preise','b','🏭','Energie als Kern der Technokratie – Tour, neues Buch, 5 € pro Liter?',
  "Regenauer rechnet damit, dass ab Sommer „der Sommerurlaub für alle“ ausfällt. Die Krise sei „Teil 2 dieses Reset“: Kern der Technokratie der 1930er sei das Management der Energieversorgung auf Mikro- und Makroebene gewesen – jede Person und jedes Produkt nach Energieverbrauch bepreist. Das lasse sich am besten über Energiemangel einführen. Seine Tour im Mai (letzter Termin um den 2. Juni) halte er noch für machbar, im September sei er unsicher, nächstes Jahr halte er für „ziemlich ausgeschlossen“. Sein Buch „Degeneration X“ erscheine am 1. Juni im Handel, auf der Tour vorab.",
  "📌 Analoge Treffen dienten dem Vernetzen mit Menschen aus dem Umkreis von etwa 50 km [0:17].",
  "📌 Die Preise würden zuerst steigen; Europa sei nach Asien die zweite betroffene Region; 5 € pro Liter im Sommer seien möglich [0:17–0:18] [seine Sicht].",
  "🔗 Technokratie und Energiebuchhaltung kommen auch im {{a:regenauer-kontrolle|Vortrag „Bis 2030“}} vor.",
  "📚 **Ergänzung:** Laut EIA gingen 2024 rund 84 % des Rohöls und 83 % des LNG durch Hormus nach Asien – siehe Abgleich.")
S('0:18','0:20','Rationierung, Wallet, UN-ID','c','📲','Kontingente per App: Bürger-Wallet und die UN-ID für Essensrationen',
  "Statt die Preise steigen zu lassen, könne rationiert werden – als Beispiel nennt Regenauer 20 l für Private und 200 l für Gewerbe (Zeitraum offen). An der Tankstelle müsse man dann die Bürger-Wallet oder einen QR-Code vorzeigen; die deutsche Wallet komme „am 5.1.27“. Das passe „perfekt zur Timeline“, denn eine App, die niemand wolle, setze man nur durch, indem man Bedarf herstelle. Die UN mache das in Hungergebieten Afrikas schon: Essensrationen gebe es nur mit digitaler UN-ID.",
  "💬 „entweder scannen oder hungern“ (Regenauer über UN-Essensausgaben) [0:19]",
  "📌 Gastgeber: Treffen werde es wieder „die Normalos“, nicht die Eliten [0:19].",
  "📚 **Ergänzung:** Der Start der deutschen EUDI-Wallet ist für den 2. Januar 2027 angekündigt; zum Start dienen Personalausweis bzw. Aufenthaltstitel zur Identifizierung, der Führerschein soll speicherbar sein – siehe Abgleich.",
  "❓ Welches UN-Programm mit welcher ID gemeint ist, bleibt offen.")
S('0:20','0:23','Trading Desk Weißes Haus','a','🎰','Iran-Krieg als Bühne: der Schreibtisch im Weißen Haus als „Trading Desk“',
  "Der Gastgeber, der den Iran seine Heimat nennt, berichtet von abgesagten Friedensgesprächen in Pakistan, einer gebrochenen Waffenruhe und einem gekaperten Schiff; das sei die „geopolitische Bühne“, eine tägliche Telenovela. Regenauer rät, sich vom täglichen Hin und Her nicht nervös machen zu lassen. Der Schreibtisch im Weißen Haus sei ein „Trading Desk“: Kurz vor Pressekonferenzen würden Hunderte Millionen Dollar platziert, etwa bei Polymarket – er nennt das offen kriminellen Insiderhandel und vermutet Trumps Sohn oder das Umfeld dahinter.",
  "📌 Trump widerspreche sich in wenigen Minuten dreimal; das sei „nur Marktmanipulation“ [0:21] [seine Sicht].",
  "📌 Märkte seien inzwischen abgestumpft; Gold- und Silberpreis seien relativ konstant [0:22].",
  "📌 Die Masse an Informationen solle davon ablenken, den IEA-Tracker und dessen Folgen zu sehen [0:22].",
  "📚 **Ergänzung:** Waffenruhe ab 08.04.2026, Gespräche in Islamabad am 11.04. ohne Ergebnis – siehe Abgleich. ❓ Für den Insiderhandel-Vorwurf gegen namentlich vermutete Personen nennt Regenauer keinen Beleg; geprüft wurde er nicht.")
S('0:23','0:26','Kein Zurück, vorbereiten','b','🧭','„Nicht mehr abzufangen“ – Düngemittel, Raffinerien und Vorbereitung',
  "Selbst wenn morgen alles wieder offen und repariert wäre, dauere es mindestens sechs Monate bis zum früheren Versorgungsniveau. Düngemittel seien schon jetzt zu knapp; die Energieversorgung werde einbrechen – offen sei nur, wie schlimm und wie lange. Die vielen Raffineriebrände wirkten „sehr mutwillig“. Wer sich vorbereiten wolle, brauche mehr als zwei Spritkanister: Generator, Solarzellen, vor allem Menschen im Umfeld, um nicht Essen per ID an einem LKW abholen zu müssen.",
  "💬 „Die Frage ist nur noch, wie schlimm es wird“ (Regenauer) [0:24]",
  "📌 In den nächsten Jahren werde jeder beweisen, was für ein Mensch er sei – bei Covid hätten das viele „vergeigt“ (Schlusssatz eines eigenen Textes von vor etwa zwei Wochen) [0:25].",
  "📌 Endprodukt der Krise sei die völlige Abhängigkeit von einem System, das Essen und Energie zuteilt [0:26] [seine Sicht].",
  "📚 **Ergänzung:** Die IEA nennt einen Rückgang des LNG-Angebots um rund 20 % und eine Freigabe von 400 Mio. Barrel Notfallreserven. ❓ Zahlen zu Düngemitteln wurden nicht geprüft.")
S('0:26','0:28','8000 gegen 8 Milliarden','a','⚖️','Gastgeber: 8.000 gegen 8 Milliarden – Team Rot gegen Team Blau',
  "Der Gastgeber nennt es die größte Blamage der Menschheit, dass sich 8 Milliarden von 8.000 Menschen versklaven ließen. Corona sei ein Test für Hörigkeit gewesen. Derzeit gebe es Lagerbildung wie im Sport: Team Israel/USA („angelsächsisch-israelisches Imperium“) gegen Team BRICS; der Iran sei plötzlich populär, Israel das „am meisten gehasste Land“ – so einfach sei es aber nicht. Mit Ernst Wolff habe er besprochen, dass der Iran und andere BRICS-Staaten neben den angeblichen Feinden in der BIZ säßen.",
  "📌 „Jede Zivilisation kriegt genau die Regierung, die sie verdient“ (Gastgeber) [0:26].",
  "🔗 Zur BIZ siehe das {{a:regenauer-masterpeace|Masterpeace-Gespräch}}.",
  "❓ Ob die Zentralbank des Iran Mitglied der BIZ ist, wurde nicht geprüft.")
S('0:28','0:31','Iran nicht Gegenpol; Burmah Oil','d','🛢️','Iran als Teil derselben Agenda – Burmah Oil, Anglo-Persian, BP',
  "Regenauer: Auf der „2D-Politikebene“ wirke es wie ein Krieg des islamischen Terroristen gegen den Wertewesten, so sei es aber nicht. Der Iran habe laut einer Studie von 2023 eine Impfquote von 76,1 %, seit 2022 eine aktive Zentralbank-Digitalwährung und eine verpflichtende E-ID ab 15 Jahren – in diesen Punkten sei er „weiter als der Werte-Westen“; in Russland laufe es genauso. Historisch: Burmah Oil (von ihm auf 1883 datiert) habe exklusive Förderrechte im Iran bekommen und die Anglo-Persian Oil Company gegründet, die heutige BP; Burmah habe auch Castrol.",
  "📌 Der Iran sei seit etwa 1860 „integraler Bestandteil des anglo-amerikanischen Empire“ [0:30] [seine Sicht].",
  "📌 Von den Öl-Deals hätten Oligarchen, die britische Regierung und die iranische Führungskaste profitiert [0:30].",
  "📚 **Ergänzung:** Burmah Oil wurde 1886 in Glasgow gegründet, hielt 97 % an der Anglo-Persian Oil Company, übernahm 1966 Castrol und wurde 2000 von BP Amoco gekauft – siehe Abgleich.",
  "❓ Impfquote, Digitalwährung und E-ID-Pflicht im Iran wurden in diesem Lauf nicht geprüft.")
S('0:31','0:33','Schah, Rockefeller, Israel-Waffen','d','🤝','Schah und Rockefeller – Israels Waffen für den Iran',
  "Der Schah (Pahlavi) habe eng mit David Rockefeller kooperiert; Rockefeller habe ihm nach seiner Ausweisung zur Einreise in die USA verholfen und beschreibe die Freundschaft stolz in seinen Memoiren. Rockefeller habe das Weiße Haus „praktisch gemanagt“, solange er die Chase Manhattan Bank führte. Im Iran-Irak-Krieg seien die Israelis der größte Waffenlieferant des Iran gewesen; das sei geheim gehalten worden und herausgekommen. Darum nenne er es nicht mehr das anglo-amerikanische, sondern das „zionistisch-anglo-amerikanische Imperium“.",
  "💬 „das zionistisch anglo-amerikanische Imperium“ (Regenauer, eigene Bezeichnung) [0:32]",
  "📌 Regenauer: Das seien „alles Zionisten und Eugeniker“ und – im Sinne ausgrenzender Herrschaftsideologien – Faschisten gewesen [0:32–0:33]; er nennt Netanjahu und dessen Partei (im Transkript „Liquid“, vermutlich Likud ❓), die Terrororganisationen finanziert hätten [0:32].",
  "📚 **Ergänzung:** Die Bundeszentrale für politische Bildung beschreibt es als Merkmal von strukturellem Antisemitismus, wenn komplexe Zusammenhänge einer kleinen Personengruppe mit böswilliger Absicht zugeschrieben werden (bpb, siehe Quellen). Regenauer verwendet hier eine politische Kategorie (Zionisten), keine Aussage über Juden insgesamt.",
  "❓ Umfang der israelischen Waffenlieferungen an den Iran in den 1980er-Jahren und die Rockefeller-Stellen wurden nicht geprüft.")
S('0:33','0:36','Fasces, Liechtenstein, Moses Hess','d','🏛️','Fasces, Liechtenstein und Moses Hess',
  "Gastgeber und Gast sprechen über die römischen Fasces als Symbol der Machtbündelung; die USA hätten die WHO demonstrativ verlassen. Regenauer erzählt, Liechtenstein habe als einziges Herrschaftsgebiet nicht anerkannt, dass die Habsburger das (Heilige) Römische Reich für beendet erklärten, und dürfe daher einen neuen Kaiser ausrufen – „wird nicht viel ausrichten“. Der Gastgeber fasst frühere Folgen zusammen: Marxismus, Kommunismus und modernes Kapitalsystem gingen auf Geheimgesellschaften zurück.",
  "📌 Regenauer: Sozialdemokratie, Sozialismus und Kommunismus gingen „alle zurück auf“ Moses Hess; das sei gut dokumentiert, auch bei Wikipedia [0:34–0:35].",
  "📌 Sozialdemokratie sei „nicht besser als der vorherige Feudalismus“, weil man sich frei glaube [0:35] [seine Sicht].",
  "📌 Gastgeber: Die Schule lasse die interessantesten Aspekte der Geschichte weg; Eugenik sei nach dem Nationalsozialismus als Transhumanismus „reframed“ worden [0:35].",
  "🔗 Moses Hess und Eugenik kommen auch bei {{a:ungeskriptet-regenauer|Regenauer bei {ungeskriptet}}} vor.",
  "❓ Die Liechtenstein-Behauptung und die Moses-Hess-These wurden nicht geprüft.")
S('0:36','0:39','Kellogg, Shaw, Ford','d','🥣','Gastgeber: Kellogg, Shaw, Russell – Henry Ford und „The International Jew“',
  "Der Gastgeber fragt, warum Kellogg’s noch in den Regalen stehe: John Harvey Kellogg sei ein bekennender Eugeniker gewesen, habe 40 Jungen adoptiert, Patienten Joghurt-Einläufe verabreicht, Masturbation verteufelt und Beschneidung ohne Betäubung befürwortet; Cornflakes habe er erfunden, um den Sexualtrieb zu dämpfen. In seinem Sanatorium seien Rockefellers und Fords zu Gast gewesen. Regenauer ergänzt George Bernard Shaw und Bertrand Russell, die von Kellogg beeinflusst gewesen seien, und Henry Ford.",
  "📌 Regenauer: Henry Ford habe mit „The International Jew“ die Vorlage für „Mein Kampf“ geliefert; Hitler habe „die meisten Teile“ abgeschrieben [0:37] [seine Sicht].",
  "📚 **Ergänzung:** Belegt sind Kelloggs Gründung der Race Betterment Foundation (1914), seine Empfehlung der Beschneidung ohne Betäubung und Joghurt-Einläufe; Ford finanzierte den „Dearborn Independent“ (1920–1927) mit der Serie „The International Jew“, Hitler lobte Ford in „Mein Kampf“. Dass große Teile abgeschrieben seien, tragen die geprüften Quellen nicht – siehe Abgleich.",
  "❓ „40 adoptierte Jungen“ und der genannte Zweck der Cornflakes wurden nicht belegt.")
S('0:39','0:42','Kolonialgewalt, 1953, Schmidt','d','⚓','Kolonialgewalt, Putsch 1953 und der Sturz von Helmut Schmidt',
  "Der Gastgeber beschreibt ein Foto aus der Kolonialzeit (von ihm Südafrika um 1880/90 und den Briten zugeordnet): Ein Mann blickt auf Hand und Fuß seiner Tochter, abgehackt als Strafe für eine verfehlte Tagesquote. Der Iran sei seit Anfang des 20. Jahrhunderts eine „Ölkolonie des Westens“ gewesen; 1953 habe die Operation Ajax Mossadegh gestürzt und den Schah gestärkt. Unter dem Schah habe es ebenfalls schwere Gewalt gegen Regimekritiker gegeben. Die „47 Jahre Unterdrückung“ würden nur ab 1979 gezählt.",
  "📌 Gastgeber (nach Dirk Pohlmann): Helmut Schmidt sei nach einem großen Erdgas-Röhren-Geschäft mit der Sowjetunion auf Druck der Reagan-Regierung gestürzt worden; FDP-Leute seien bestochen worden [0:40–0:41] [seine Sicht].",
  "📌 Gastgeber: Der Schah habe Israel in einem „60 Minutes“-Interview scharf kritisiert [0:41].",
  "📚 **Ergänzung:** Die CIA-Rolle beim Putsch 1953 ist durch eine 2013 freigegebene interne CIA-Geschichte belegt – siehe Abgleich. Das bekannte Foto eines Vaters mit Hand und Fuß seiner Tochter stammt nach verbreiteter Darstellung aus dem Kongo-Freistaat (1904) ❓ – nicht geprüft.",
  "❓ Bestechungsvorwurf zum Misstrauensvotum 1982 nicht geprüft.")
S('0:42','0:45','Truman Show, kein echter Krieg','a','🎭','„Truman Show“: Prognosen, Bohemian Grove und warum es kein „richtiger Krieg“ sei',
  "Regenauer verweist auf sein Buch „Truman Show“ (2024): Alles sei eine Bühne. Helmut Schmidt beschreibe in seinem letzten Buch („Menschen und Mächte“ oder ähnlich), wie gern er beim Bohemian Grove gewesen sei. Schon im November 2024 habe er in einem Text einen US-Angriff auf den Iran angekündigt; Greg Reese habe ihm vor über einem Jahr Angriff, Regimewechsel und die Einsetzung von Pahlavis Sohn vorhergesagt. Ein richtiger Krieg sehe anders aus – wie der Golfkrieg mit Koalition, Panzern, Bodeninvasion und eingebetteten Reportern.",
  "💬 „ein richtiger Krieg sieht anders aus“ (Regenauer) [0:44]",
  "📌 Getroffen würden „nur strategische Ziele“, die die Energieversorgung kosten, keine militärischen [0:44] [seine Sicht].",
  "📚 **Ergänzung:** Der Krieg begann am 28.02.2026 mit israelischen und US-Angriffen; am 01.03. bestätigte das iranische Staatsfernsehen den Tod von Ali Chamenei – siehe Abgleich.",
  "❓ Welches Schmidt-Buch die Bohemian-Grove-Stelle enthält, wurde nicht geprüft.")
S('0:45','0:48','Orwells Krieg, Opferzahlen','a','💣','Orwells ewiger Krieg – Gastgeber zu Opferzahlen und Atombombe',
  "Was man vom Krieg sehe, sei großteils „KI-Slop“; man wisse nicht, wer wem Bomben auf den Kopf werfe. Das sei Orwells Szenario eines ewigen Kriegs, der nicht gewonnen, sondern geführt werden solle, weil er alles andere rechtfertige. Regenauer fürchtet dennoch viele Tote, wie in der Ukraine. Der Gastgeber: Im Golfkrieg seien in der härtesten Phase 2.000 Menschen pro Tag gestorben; das Narrativ, die iranische Regierung habe in 48 Stunden 40.000 bis 90.000 Menschen der eigenen Bevölkerung getötet, halte er für Propaganda.",
  "📌 Gastgeber: Für solche Zahlen brauche man eine Kriegsmaschinerie über die Bombardierung Dresdens hinaus; er würde Harald Kujat fragen [0:47] [seine Sicht].",
  "📌 Gastgeber: Auch das „Narrativ der Atombombe, die kurz vor dem Abschluss“ stand, sei Propaganda [0:47].",
  "📚 **Ergänzung:** Zu den Protesten im Januar 2026 nennen Quellen sehr unterschiedliche Zahlen: offiziell 3.117, HRANA 6.126 bestätigt (+17.091 in Prüfung), Iran International über 36.500 (nicht überprüfbar). Der IAEA-Gouverneursrat stellte im Juni 2025 eine Nichteinhaltung von Sicherungspflichten fest – siehe Abgleich und Diagramm.",
  "❓ „2.000 Tote pro Tag“ im Golfkrieg nicht geprüft.")
S('0:48','0:52','Gerüchte geprüft','e','🧪','Gerüchte geprüft: Netanjahu und Milei, Albert Pike, Deagel, Guidestones',
  "Der Gastgeber erzählt ein Gerücht aus einem Video: Netanjahus Vater (Ben-Zion Mileikowsky) habe einen zweiten Sohn in Argentinien, Javier Milei. Regenauer: Der erste Teil (der Familienname Mileikowsky) stimme, die Milei-Geschichte diskreditiere sich selbst. Belegt sei dagegen Mileis Treffen mit Netanjahu. Regenauer räumt dann selbst mit drei Erzählungen auf: Den Albert-Pike-Brief über einen Dritten Weltkrieg gebe es in dieser Form nicht (er verweist auf James Corbetts Corbett Report), die Deagel-Liste sei „Schwachsinn“, die Georgia Guidestones seien von zwei lokalen Bankern aufgestellt worden – „nicht die Eliten“.",
  "📌 Regenauer: Im Pike-Text stünden Begriffe, die es zu Pikes Lebzeiten noch nicht gab; die Nennung eines „dritten“ Weltkriegs setze Kenntnis der ersten beiden voraus [0:49–0:50].",
  "📌 Gastgeber widerspricht teilweise: Die Pike-Sache sei komplizierter; Material aus den 1800ern sei wohl 1953 weiter ausgeschmückt worden [0:51].",
  "📌 Gastgeber: An Resten der Berliner Mauer sei eine große Israel-Fahne angebracht worden [0:48].",
  "❓ Herkunft der Guidestones (Auftraggeber „R. C. Christian“, Bankier vor Ort) wurde nicht geprüft.")
S('0:52','0:54','Spanien, Merz und Hormus','a','🇪🇸','Spaniens Nein zum Krieg – und Merz’ Hormus-Forderung',
  "Nach einem Hinweis auf Walter Veith (im Transkript „Fight“) spricht der Gastgeber über Milei, der als Anti-Establishment dargestellt worden sei, und über Spaniens Regierung, die sich gegen den Krieg ausgesprochen habe und dafür von Trump vor laufenden Kameras gemaßregelt worden sei. Regenauer erinnert daran, dass dieselbe Regierung Lockdowns befürwortet und wenige Tage später Altersverifikation fürs Internet und eine E-ID angekündigt habe. Der Gastgeber nennt Merz’ Forderung, die Straße von Hormus wieder zu öffnen, nachdem er dem „Regime“ kurz zuvor nur noch drei Tage gegeben habe.",
  "📌 Gastgeber: Politiker auf der Weltbühne seien „Memenspiele“, ein Theater, in dem alle ihre Rolle erfüllen [0:53] [seine Sicht].",
  "❓ Wortlaut und Datum der Merz-Äußerung „drei Tage“ wurden nicht geprüft.")
S('0:54','0:57','EU als Technate','c','🗺️','Deutschlands Rolle: die EU als erstes „Technate“',
  "Deutschland habe wegen Lage und Größe eine Führungsrolle. Von der Leyen reiße Kompetenzen an sich und gründe einen eigenen Geheimdienst – darauf habe auch Martin Sonneborn hingewiesen. Die EU sei das Pilotprojekt für einen Block mit einer Währung, Schuldenausgleich und Privatisierung von Volksvermögen an BlackRock, Vanguard und Fidelity – „das erste Technate“. Trump baue mit Grönland, Kanada und eventuell Kuba das ursprüngliche Technate der 1930er-Karte nach; dazu passe das Zehn-Regionen-Modell des Club of Rome.",
  "📌 Merz („BlackRock-Merz“) und von der Leyen wüssten, was sie tun; andere seien Unterhaltungsapparat, um das Vertrauen in den Nationalstaat zu zerstören [0:56] [seine Sicht].",
  "🔗 Technate und Club of Rome kommen auch im {{a:regenauer-kontrolle|Vortrag „Bis 2030“}} vor.",
  "❓ Die Geheimdienst-Pläne der Kommission und der Sonneborn-Post wurden nicht geprüft.")
S('0:57','0:59','USA-Überwachung, digitaler Gulag','c','🔒','Überwachung in den USA, „digitaler Gulag“ und Grundeinkommen',
  "Die USA seien auf dem Weg zum Überwachungsstaat mit Flock-Kameras, Palantir, Biometrie, Real ID und der Einwanderungsbehörde ICE – „Trumps Gestapo“. In Deutschland würden Wallet, Energiekontingent, digitaler Führerschein, elektronische Patientenakte und digitaler Euro verknüpft; bei einem Finanzkollaps gebe es Übergangsgeld von 500 oder 1.000 € digital auf die Wallet. Das sei der „digitale Gulag“. Ein Grundeinkommen von einem System, das einen unterdrücke, führe in völlige Abhängigkeit.",
  "💬 „das digitale Gulag … von dem ich schon die ganze Zeit rede“ (Regenauer) [0:58]",
  "📌 Führungspersonal stamme oft aus deutschen Familien: Kissinger, Trumps Vorfahren, die Rockefellers („aus Rockenfeld“), Musk mit Vorfahren im Berner Oberland [0:58].",
  "📚 **Ergänzung:** Die geprüfte Quelle zur deutschen Wallet beschreibt Identifizierung und Führerschein, keine Kopplung an Energie- oder Geldzuteilung – das bleibt Regenauers Szenario.")
S('0:59','1:02','Thiel gegen Zuckerberg','c','🧠','Peter Thiel gegen Mark Zuckerberg – LifeLog und TIA',
  "Der Gastgeber nennt ein neues Buch über Peter Thiel (Autor im Transkript „Tarik Hübsch“ ❓) und meint, die wirklich Mächtigen sehe man nicht. Facebook sei die private Fortführung des eingestellten Pentagon-Projekts LifeLog, Palantir gehe auf TIA (Total Information Awareness) zurück. Regenauer: Zuckerberg halte er für nicht besonders intelligent, einen Nutznießer, der sein Fähnchen nach dem Wind drehe; Thiel dagegen sage seit Jahrzehnten dasselbe und habe ein klares, „von Eugenik geprägtes, von Apartheid beflügeltes“ Weltbild.",
  "📌 Thiel und Alex Karp seien ein „dynamisches Duo“; Iain Davis nenne sie „Neo-Nerds“; Karp habe in Frankfurt studiert [1:01] [seine Sicht].",
  "📌 Regenauer: Zuckerberg komme aus einer Familie „mit CIA-Hintergrund“ (Transkript „C Hintergrund“ ❓) [1:01].",
  "❓ LifeLog/TIA-Bezüge und die Familienbehauptung wurden nicht geprüft.")
S('1:02','1:05','Karp-Buch und Orsini','d','📜','Karps Thesen, Varoufakis – und die Familie Orsini',
  "Palantir habe auf X Auszüge aus Karps Buch gepostet – rund 22 Thesen, die Regenauer als Akzelerationismus und „dunkle Aufklärung“ beschreibt; Yanis Varoufakis habe sie eingeordnet. Die wirklich Mächtigen säßen aber nicht im Fernsehen. Als Beispiel nennt Regenauer die Familie Orsini: Familienarchiv ab 1153, drei Päpste, 60 Kardinäle, Senatoren; sie verstünden sich gut mit Rothschilds und Rockefellers und heirateten untereinander.",
  "📌 Von den Orsini gebe es keine Fotos, Videos oder Interviews; dass sie seit fast 1.000 Jahren reich seien, zeige ihren Einfluss [1:04] [seine Sicht].",
  "📌 Gastgeber: Die Trilaterale Kommission sei durch Epstein-Akten und ein Interview mit Steve Bannon wieder bekannt geworden [1:05].",
  "❓ Die Orsini-Angaben und Karps 22 Punkte wurden nicht geprüft.")
S('1:05','1:08','Chatham House, Carney','d','🏰','Wo die Macht endet: Chatham House, Carney und das Bail-in',
  "Der Gastgeber nennt Frankfurt einen Knotenpunkt (Karp studierte dort, Thiel sei dort geboren, die Rothschild-Bankendynastie gegründet) und fragt nach der Hierarchie. Regenauer: Auf der Liste der zehn einflussreichsten Thinktanks stünden Council on Foreign Relations und RAND, aber nicht Chatham House – weil Chatham House (gegründet aus dem Kreis Round Table, Cecil Rhodes, Milner) alle zehn direkt oder indirekt gegründet habe. Mark Carney sei Vorsitzender von Chatham House, früher Chef der kanadischen und britischen Zentralbank und beim Financial Stability Board (FSB).",
  "📌 Carney habe nach 2008 über das FSB eingeführt, dass es bei der nächsten Krise kein Bail-out, sondern ein Bail-in gebe: Guthaben weg, Kredit bleibe [1:07–1:08] [seine Sicht].",
  "📌 Carney regiere Kanada als „ungewählter Präsident“, während Trump es annektieren wolle [1:08].",
  "📚 **Ergänzung:** Carneys Liberale Partei gewann die Unterhauswahl am 28.04.2025 – siehe Abgleich.",
  "❓ Carneys Vorsitz bei Chatham House und die Thinktank-Liste wurden nicht geprüft.")
S('1:08','1:11','Banker hinter dem Adel','d','🏦','Banker hinter dem Adel – und die Grenze des Belegbaren',
  "Über dem Adel oder gleichberechtigt stünden die Banker, die Kriege finanzierten: Napoleon habe erst mit einer eigenen Zentralbank Krieg führen können; die Geschichte der Zentralbanken reiche bis zur Hamburger Bank zurück. Bei der ersten Zentralbank der USA (von ihm „1832“ datiert) sei 70–80 % des Geldes aus Großbritannien gekommen, ein großer Teil von den Rothschilds; später habe J. P. Morgan das US-Finanzsystem zweimal gerettet. Er schreibe an einem Artikel über den Malteserorden.",
  "💬 „Reptiloiden … interdimensionale Wesen“ – betrachte er „eher als Entertainment“ (Regenauer) [1:10–1:11]",
  "📌 Journalistisch belegbar sei es bis zur Ebene von Bankgründungen, Finanzflüssen und Eigentümern; mit echten Dokumenten komme man etwa bis 1820/30 zurück [1:09–1:11].",
  "📚 **Ergänzung:** Die First Bank of the United States wurde 1791 gegründet; 1832 legte Präsident Jackson sein Veto gegen die Verlängerung der Second Bank ein – siehe Abgleich.",
  "❓ Die Eigentumsanteile aus Großbritannien wurden nicht geprüft.")
S('1:11','1:14','Malteser, Bohemian Grove','e','🕯️','Malteser-Artikel, Bohemian Grove und Rituale',
  "Für den Malteser-Artikel habe er 600–800 Quellen, sonst etwa 100 pro Text; vielleicht werde ein Buch oder Mehrteiler daraus. Der Gastgeber bringt Bohemian Grove ins Spiel (Alex-Jones-Video, Gestalten in weißen Roben) und Rituale bei Musikshows und Super-Bowl-Halbzeitshows; das habe eine okkultistische Ebene. Regenauer: Es könne auch sein, dass man glauben machen wolle, mit einer größeren Macht verbunden zu sein – am Ende seien es „8 bis 10.000 normale Leute“.",
  "📌 Regenauer lobt erstmals einen Song von Kollegah zum Thema Zionismus: „alte Männer ohne Muskeln und Moral“ (zitiert) [1:14].",
  "❓ Wer 2025 im Bohemian Grove gefilmt haben soll („Jumper“), bleibt unklar.")
S('1:14','1:17','Gegner nicht überschätzen','e','🪞','Image-Design statt Übermacht – den Gegner nicht überschätzen',
  "Rituale wie die „Cremation of Care“ dienten womöglich dem Image-Design und dem sektenartigen Charakter; es seien „profane“ Leute. Der Gastgeber widerspricht teilweise: Ritualistik gebe es seit Sabbatai Zvi, den Frankisten, dem Illuminatenorden und dem Mittelalter, also lange vor Medienwirksamkeit; er sucht „eine Mitte“. Regenauer: Wer den Gegner überschätze, fühle sich ohnmächtig – „wir sind mehr“.",
  "💬 „Der Gegner wird völlig überschätzt“ (Regenauer) [1:16]",
  "📌 Gastgeber: David Rockefeller, „der König von Amerika“, habe gebrochen und unsicher gewirkt; Eliten würden als Kinder missbraucht, auch durch MK-Ultra-Programme [1:16–1:17] [seine Sicht – ohne Beleg im Gespräch].",
  "❓ Die Missbrauchs- und MK-Ultra-Behauptungen über Elitefamilien bleiben im Gespräch unbelegt.")
S('1:17','1:20','Erziehung, Voluntarismus','f','📒','Erziehung – und das Buch „Organisiert euch“',
  "Der Gastgeber: Mit Macht konfrontiert, könnten auch „wir“ schlimmer werden; Regenauers Mutter habe Wert auf Erziehung gelegt, Elitekinder seien wie Dreck behandelt worden. Regenauer scherzt über Montgomery Burns (Vorlage Rockefeller oder Rothschild?) und stellt das gelbe Buch „Organisiert euch“ vor, das er vor drei, vier Wochen herausgebracht habe: eine Autorin (später „Silvia Lorenzen“, Schreibweise ❓) über Voluntarismus. Menschen hätten Jahrtausende ohne Staat in spontaner Ordnung gelebt.",
  "📌 Straßen bauten und bezahlten ohne Staat dieselben Leute – ohne „korrupten Mittelmann“, der Kosten über Ausschreibungen verdreifache [1:19–1:20] [seine Sicht].",
  "📌 90–95 % des Lebens organisierten Menschen ohnehin selbst – Schulfest, Sportfest, Scheune bauen [1:20].")
S('1:20','1:23','Staat, Realitätsformung, KI-Kunst','f','🎨','Staat seit 150 Jahren, „Realitätsformung“ und KI-Musik',
  "Den Staat in heutiger Form gebe es erst seit etwa 150 Jahren; das Buch (130 Seiten, Untertitel „Denkschrift für eine selbstbestimmte Ordnung“) solle Vorstellungskraft wecken. Der Gastgeber: Jeder sei an der „Realitätsformung“ beteiligt; wer sie manipuliere, sei ein „Schwarzmagier“ mit ultimativer Macht – darum seien soziale Medien für die psychologische Kriegsführung so wichtig. Regenauer stimmt zu und zeigt das Buch „Ohne Worte“ mit handgemalten Zeichnungen einer Künstlerin, für das er ein Vorwort schrieb.",
  "📌 Bei Spotify würden täglich 60.000 KI-Titel hochgeladen; in zwei Jahren gebe es kaum noch menschliche Kunst [1:22] [seine Sicht].",
  "💬 „Das fehlt nämlich das Wichtigste – Seele“ (Regenauer über KI-Musik) [1:23]",
  "📚 **Ergänzung:** Die Zahl 60.000 pro Tag meldete im Januar 2026 Deezer (nicht Spotify): rund 39 % der täglichen Uploads, bis 3 % der Streams – siehe Abgleich.")
S('1:23','1:26','Taten statt Kommentare','f','🔨','„Information interessiert nur da, wo sie zu Taten führt“ – Isolationspandemie',
  "Aus einem alten Rap-Text zitiert Regenauer seinen Leitsatz: Information zähle nur, wenn sie zu Taten führe. Ein Buch mit einer Künstlerin verändere wenig, aber das eigene Leben und das einiger Menschen. Wer nur Twitter-Kommentare schreibe, tue, was das System erwarte; soziale Medien seien ein „Überdruckventil“. Wir hätten eine „Isolationspandemie“: Vereine, Traditionen und Ehrenamt stürben aus, die Jugend fehle.",
  "💬 „Information interessiert nur da, wo sie zu Taten führt“ (Regenauer) [1:23]",
  "📌 In zwei, drei Generationen sei die auf Freiwilligkeit beruhende Zivilgesellschaft tot [1:25] [seine Sicht].",
  "📌 Prüfstein: Wer von den Online-Kontakten helfe, wenn morgen das Brot fehle oder der Strom ausfalle? [1:26]")
S('1:26','1:28','Harari, lokale Netze','f','🌾','Ready Player One, Harari – und das Netz aus zehn Leuten',
  "Der Gastgeber nennt Spielbergs „Ready Player One“ als Zukunftsbild des „nutzlosen Fressers“, der mit Videospielen stillgelegt werde. Regenauer: Harari sei nicht sympathisch, habe aber mit vielem Recht – Menschen könnten mit virtuellen Welten, KI und „Soma-Drogen“ beschäftigt werden. Er ruft dazu auf, lokale Kunst zu unterstützen, freiwillige Netzwerke und Vereine zu gründen und Kontakte zu suchen.",
  "📌 Bild für den Ernstfall: zehn Leute – einer hat Mehl, einer kann Brot backen, einer holt Wasser aus einer Quelle, einer repariert einen Generator [1:27].",
  "🔗 Ähnliche Auswege nennt Regenauer im {{a:regenauer-masterpeace|Masterpeace-Gespräch}}.")
S('1:28','1:34','Telefone ohne Big Tech','f','📵','Telefone ohne Big Tech: GrapheneOS-Geräte und Boykott',
  "Der Gastgeber fragt nach Regenauers Kooperation mit einer Telefonfirma. Regenauer: Es sei keine gewöhnliche Smartphone-Firma, sondern das Projekt von Hakim (Nachname im Transkript unklar ❓), der für US-Journalisten wie James Corbett, Whitney Webb und Derrick Broze Technik bereitgestellt und Telefone mit GrapheneOS eingerichtet habe. Daraus seien Geräte mit vorinstallierten Open-Source-Apps, eigener Mail, VPN und bald einer lokal laufenden KI geworden. Er selbst nutze seit zwei Jahren ein solches Telefon und einen angepassten Linux-Laptop; Microsoft, PayPal und Big Tech habe er gekündigt.",
  "📌 Das Ziel sei nicht, viele Telefone zu verkaufen, sondern Big Tech abzulösen [1:29–1:30] [seine Sicht].",
  "📌 Vertrieb: Warteliste über seine Webseite, Import auf eigene Rechnung, Versand per FedEx, Auslieferung in der Schweiz, Deutschland und Österreich, ohne Shop und ohne Gewerbe; es bleibe wenig hängen [1:31–1:33].",
  "📌 Das iPhone habe er als Musiker wegen Logic Pro auf dem Mac gehabt [1:31].",
  "📚 **Ergänzung:** Regenauer vertreibt die Geräte selbst; hier liegt ein eigenes wirtschaftliches Interesse vor, das er offen anspricht.")
S('1:34','1:38','Werkzeug oder Sklave','f','🧰','Technik als Werkzeug – Smartphone-Zombies, Aufmerksamkeit und KI',
  "Der Gastgeber fragt, ob Regenauer Technik differenziert sehe – frühere Neuerungen wie Drumcomputer oder E-Gitarre seien auch verteufelt worden. Regenauer: Technik sei ein Werkzeug, die meisten würden aber zum Werkzeug ihrer Technik. Er nutze sein Telefon gezielt, ohne Newsfeeds und rote Benachrichtigungspunkte. Wer ChatGPT oder Grok nutze, trainiere das System, das einen unterdrücken werde; Sendungen, in denen man mit ChatGPT über „Verschwörungstheorien“ spreche (sein Wort), hält er für „unintelligent“.",
  "📌 Laut einer Studie sei die Aufmerksamkeitsspanne seit 2007 von 16–19 auf 9–11 Sekunden gesunken [1:35–1:36] [seine Sicht; Studie nicht genannt].",
  "📌 Er nutze keine KI; Lesen sei Training wie im Fitnessstudio [1:37].",
  "❓ Die genannte Studie zur Aufmerksamkeitsspanne wurde nicht gefunden.")
S('1:38','1:41','Altersverifikation, Kinder','f','🧒','Brillen, Altersverifikation und Kinder',
  "Der Gastgeber: Nächster Schritt seien Implantate; Regenauer: Erst kämen Kamerabrillen. Der Gastgeber räumt ein, dass Kinder durch Smartphones gefährdet seien (Pornos, Enthauptungsvideos in Grundschulen und Kitas), Regulierung sei richtig – aber zu welchem Preis. Regenauer: Verbote bewirkten bei Kindern das Gegenteil; in Australien seien Kinder trotz Altersgrenze per VPN genauso online. Altersverifikation sei ein Kontrollinstrument; aufs Leben bereite nur vernünftige Erziehung vor.",
  "💬 „die Welt bekommt Zugang zum Kind“ (Spruch, vom Gastgeber zitiert) [1:38]",
  "📌 Eltern mit Smartphone am Kinderwagen – das sei „der Untergang des Abendlandes“ [1:40] [seine Sicht].",
  "❓ Die Wirkung der australischen Altersgrenze wurde nicht geprüft.")
S('1:41','1:45','Prinzipien und die Waage','f','⚖️','Gamer, KI-Faszination, Prinzipien – das Prinzip der Waage',
  "Der Gastgeber bekennt sich als Gamer und findet KI-Bild- und Videogenerierung faszinierend, ohne die Schattenseiten auszublenden; im Kinderwagen liege heute oft ein Tablet. Regenauer: Wer Prinzipien habe – ein moralisches, ethisches, logikbasiertes Koordinatensystem –, dem schade auch ein dystopisches Werkzeug nicht; Eltern müssten Prinzipien vermitteln. Der Gastgeber nennt sein „Prinzip der Waage“: digital und analog im Gleichgewicht.",
  "📌 Gastgeber: Hollywood, „Predictive Programming“, KI, Social Media und Videospiele seien gefährlich, aber „unser Raum“; man müsse den Einfluss zurückgewinnen [1:44].",
  "📌 Der Gastgeber verweist auf ein früheres Gespräch mit einer Autorin („Caroline Rasch“, Buch „Wie aus Gott Google wurde“ – Name und Titel unklar ❓) [1:44].")
S('1:45','1:49','Abschied und Werbung','w','👋','Abschied, Tour ohne Aufzeichnung, Werbung und Patreon',
  "Das Gespräch dauerte länger als geplant; Regenauer sitzt im Tessin. Seine Tour werde dieses Jahr nicht aufgezeichnet – „man kann es nur live sehen“; Termine stünden auf seiner Webseite. Der Gastgeber lobt Regenauer ausdrücklich und verweist auf regenauer.press. Danach wirbt er für ein Nahrungsergänzungsmittel (Glutamin) eines Sponsors mit Rabattcode und eigenen Gesundheitsversprechen sowie für seinen Patreon-Kanal.",
  "📌 Regenauer: Es sei „wahrscheinlich vorerst die letzte Runde“ [1:46].",
  "📚 **Ergänzung:** Die Werbung enthält Gesundheits- und Mengenangaben des Gastgebers, die hier bewusst nicht wiedergegeben werden; anhaltende Magen-Darm-Beschwerden gehören ärztlich abgeklärt ❓ (Fachstellen-Prüfung nicht erfolgt).")

THEMEN = [{"k":"a","n":"Iran-Krieg & Weltbühne"},{"k":"b","n":"Energiekrise"},{"k":"c","n":"Digitale Kontrolle & Technokratie"},
          {"k":"d","n":"Empire, Geschichte & Dynastien"},{"k":"e","n":"Erzählungen prüfen"},{"k":"f","n":"Gegenwehr, Gemeinschaft & Technik"},
          {"k":"w","n":"Nachrichten, Werbung & Organisatorisches"}]

# ---------- Reiter 1: Überblick ----------
NAB = len(A)
KERN = [
 ["1","Die Energiekrise durch den Iran-Krieg sei kein kurzfristiges Ereignis, sondern führe zu Rationierung und Kontingenten.","IEA-Maßnahmen-Tracker, Raffineriebrände, Düngemittel; mindestens sechs Monate bis zur Normalisierung.","[0:11–0:26]","★★★"],
 ["2","Energiemangel sei der Hebel zur Technokratie: Zuteilung über Bürger-Wallet, E-ID und digitales Geld („digitaler Gulag“).","Technokratie der 1930er, Wallet ab 2027, UN-ID für Essensrationen.","[0:14–0:20], [0:57–0:59]","★★★"],
 ["3","Der Iran-Krieg sei eine Bühne („Truman Show“), kein konventioneller Krieg.","Golfkrieg-Vergleich, kaum Bilder, Ziele nur in der Energieversorgung.","[0:42–0:47]","★★"],
 ["4","Der Iran sei kein Gegenpol zum Westen, sondern Teil derselben Agenda.","Impfquote, Digitalwährung, E-ID; Burmah Oil/BP, Schah und Rockefeller, Israels Waffen im Iran-Irak-Krieg.","[0:28–0:33]","★★★"],
 ["5","Trumps Ankündigungen seien Marktmanipulation; man solle sich aufs Wesentliche konzentrieren.","Polymarket-Wetten vor Pressekonferenzen, Widersprüche binnen Minuten.","[0:20–0:23]","★★"],
 ["6","Die EU sei das Pilotprojekt eines „Technate“; Deutschland komme eine Schlüsselrolle zu.","Einheitswährung, Schuldenausgleich, Privatisierung; Technate-Karte der 1930er; Club of Rome.","[0:54–0:57]","★★"],
 ["7","Die wirklich Mächtigen sehe man nicht – belegbar sei Macht nur bis zur Ebene von Banken und Thinktanks.","Chatham House, Carney/FSB, Orsini, Banker hinter dem Adel.","[1:02–1:11]","★★"],
 ["8","Manche populären Erzählungen hielten einer Prüfung nicht stand.","Albert-Pike-Brief, Deagel-Liste, Georgia Guidestones, Netanjahu-Milei-Gerücht.","[0:48–0:52]","★★"],
 ["9","Den Gegner nicht überschätzen: Es seien wenige tausend gewöhnliche Menschen.","Rituale als Image-Design; „wir sind mehr“.","[1:11–1:17]","★★"],
 ["10","Gegenwehr heiße lokal handeln: Netzwerke, Vereine, Kunst, Technik ohne Big Tech, Erziehung mit Prinzipien.","Bücher „Organisiert euch“ und „Ohne Worte“, GrapheneOS-Telefone, Isolationspandemie.","[1:17–1:45]","★★★"],
]
BAUM = {"typ":"baum","titel":"🌳 Themenbaum des Gesprächs","wurzel":TITEL,"unter":f"{GAST} · {KANAL} · {DATUM} · {DAUER}","knoten":[
 {"t":"⛽ Energiekrise","k":[{"t":"IEA-Maßnahmen-Tracker [0:11]"},{"t":"Raffineriebrände, 45 Ereignisse [0:12]"},{"t":"Sommerurlaub fällt aus, 5 € pro Liter? [0:14–0:18]"},{"t":"Düngemittel, sechs Monate [0:23]"}]},
 {"t":"📲 Zuteilung und Kontrolle","k":[{"t":"Kontingente 20 l / 200 l [0:18]"},{"t":"Bürger-Wallet 2027 [0:18]"},{"t":"UN-ID für Essensrationen [0:19]"},{"t":"Digitaler Gulag, Grundeinkommen [0:58]"},{"t":"USA: Flock, Palantir, Real ID [0:57]"}]},
 {"t":"🎭 Iran-Krieg als Bühne","k":[{"t":"Trading Desk Weißes Haus [0:21]"},{"t":"Truman Show, Prognosen [0:42]"},{"t":"Kein richtiger Krieg [0:44]"},{"t":"Orwells ewiger Krieg [0:45]"},{"t":"Spanien, Merz und Hormus [0:52–0:54]"}]},
 {"t":"🛢️ Iran und Empire","k":[{"t":"Impfquote, Digitalwährung, E-ID [0:28]"},{"t":"Burmah Oil, Anglo-Persian, BP [0:29]"},{"t":"Schah und Rockefeller [0:31]"},{"t":"Israels Waffen für den Iran [0:32]"},{"t":"Putsch 1953 [0:39]"}]},
 {"t":"🏛️ Geschichte und Dynastien","k":[{"t":"Moses Hess [0:34]"},{"t":"Kellogg, Shaw, Ford [0:36–0:39]"},{"t":"Orsini [1:04]"},{"t":"Chatham House, Carney [1:06]"},{"t":"Banker hinter dem Adel [1:09]"}]},
 {"t":"🗺️ EU und Technate","k":[{"t":"Von der Leyens Kompetenzen [0:55]"},{"t":"EU als erstes Technate [0:55]"},{"t":"Technate-Karte, Club of Rome [0:55–0:56]"},{"t":"Thiel, Karp, Zuckerberg [0:59–1:03]"}]},
 {"t":"🧪 Erzählungen geprüft","k":[{"t":"Netanjahu und Milei [0:48]"},{"t":"Albert-Pike-Brief [0:49]"},{"t":"Deagel-Liste, Guidestones [0:50]"},{"t":"Rituale als Image-Design [1:14]"}]},
 {"t":"🌾 Gegenwehr","k":[{"t":"Organisiert euch, Voluntarismus [1:19]"},{"t":"Information nur mit Taten [1:23]"},{"t":"Isolationspandemie [1:25]"},{"t":"Telefone ohne Big Tech [1:28]"},{"t":"Prinzipien statt Verbote [1:39–1:43]"}]},
]}
R1 = [
 {"typ":"folge","k":K,"titel":TITEL,"gast":GAST,"rolle":"Autor und Publizist (regenauer.press), früher Musiker und Manager; lebt in der Schweiz","kanal":KANAL,"datum":DATUM,"dauer":DAUER,"url":URL,
  "thema":"Tom-Oliver Regenauer erwartet als Folge des Iran-Kriegs eine lange Energiekrise mit Rationierung und digitaler Zuteilung, ordnet den Iran in die Geschichte des britisch-amerikanischen Ölzugriffs ein, prüft verbreitete Erzählungen und wirbt für lokale Netzwerke statt Ohnmacht.",
  "kacheln":[[str(NAB),"Abschnitte"],["10","Kernaussagen"],["__AB__","Abgleich-Punkte"],["__ZA__","Zeitachse"],["5","Diagramme"]]},
 {"typ":"hinweis","text":"Auswertung nach dem Transkript (automatische Untertitel): Gesagtes ohne Zeichen, Ergänzungen 📚, Unklares ❓. Fundstellen [Stunde:Minute] springen ins Video. Die Bewertung bleibt dem Leser."},
 {"typ":"abschnitt","titel":"⚡ In Kürze","liste":[
  "**Wer:** Tom-Oliver Regenauer, Autor, zu Gast in der Sendung „Good Morning Germany“ von REALTALK MEDIA; der Gastgeber (Name im Video nicht eindeutig ❓) nennt den Iran seine Heimat. Aufgenommen etwa um den 20. April 2026, rund 1 Std. 50 Min.",
  "**Energiekrise:** Regenauer sieht im IEA-Maßnahmen-Tracker und in vielen Raffineriebränden Zeichen einer langen Krise – mit Rationierung, Kontingenten und Zuteilung über die Bürger-Wallet ab 2027 [0:11–0:20].",
  "**Krieg als Bühne:** Der Iran-Krieg sei eine „Truman Show“; Trumps Ankündigungen dienten der Marktmanipulation; ein „richtiger Krieg“ sehe anders aus [0:20–0:47].",
  "**Iran kein Gegenpol:** Hohe Impfquote, Digitalwährung und E-ID; seit Burmah Oil und der Anglo-Persian Oil Company sei der Iran Teil des britisch-amerikanischen Zugriffs – Regenauer spricht vom „zionistisch-anglo-amerikanischen Imperium“ [0:28–0:33].",
  "**Prüfen statt glauben:** Albert-Pike-Brief, Deagel-Liste, Georgia Guidestones und ein Netanjahu-Milei-Gerücht weist Regenauer zurück [0:48–0:52].",
  "**Macht:** EU als erstes „Technate“, Chatham House und Carney, Banker hinter dem Adel; belegbar sei Macht nur bis zu Banken und Thinktanks [0:54–1:11].",
  "**Auswege:** Gegner nicht überschätzen, lokal vernetzen, Vereine, Kunst, Telefone ohne Big Tech, Prinzipien in der Erziehung [1:14–1:45].",
  "**Im Abgleich:** Kriegsbeginn 28.02.2026, IEA-Daten, US-Blockade, Paris-Konferenz, Wallet-Start, Opferzahlen der Proteste, Burmah Oil/BP, Putsch 1953, Ford, Kellogg, Carney, Deezer – mit Quellen."]},
 {"typ":"abschnitt","titel":"🔦 Aus Regenauers Sicht – der rote Faden","liste":[
  "[seine Sicht] Die Weltpolitik ist eine Bühne; entscheidend sind die Folgen, nicht die täglichen Ankündigungen.",
  "[seine Sicht] Der Iran-Krieg dient vor allem dazu, Energie zu verknappen – und Energiemangel ist der Hebel, um Menschen über Kontingente, Wallet und digitales Geld zu steuern.",
  "[seine Sicht] Der Iran ist kein Gegenmodell: Er setzt dieselbe digitale Agenda um und ist seit über 100 Jahren mit dem britisch-amerikanischen Ölzugriff verflochten.",
  "[seine Sicht] Wer wirklich Macht hat, zeigt sich nicht; belegen lässt sich Macht über Banken, Thinktanks und Dokumente – alles darüber hinaus ist Spekulation.",
  "[seine Sicht] Ohnmacht ist der größte Fehler: Wer sich lokal vernetzt, Dinge schafft und Prinzipien lebt, bleibt unabhängig, wenn Zuteilung kommt."]},
 {"typ":"text","text":"🎯 **Kernaussagen** – die zehn wichtigsten Thesen des Gesprächs:"},
 {"typ":"tabelle","kopf":["#","Aussage","Begründung im Gespräch","Fundstelle","Gewicht"],"zeilen":KERN},
 BAUM,
 {"typ":"illu","id":"iran_hebel","titel":"Skizze: Vom Krieg zur Zuteilung – die Kette laut Regenauer (Darstellung laut Regenauer, schematisch)"},
 {"typ":"illu","id":"iran_hormus","titel":"Skizze: Straße von Hormus – Mengen und Ablauf Februar bis April 2026 (belegte Daten)"},
 {"typ":"tabelle","kopf":["🧭 Steckbrief",""],"schmal":True,"zeilen":[
  ["**Thema in einem Satz**","Warum Regenauer nach dem Iran-Krieg eine lange Energiekrise mit digitaler Zuteilung erwartet – und was der Einzelne tun kann."],
  ["**Titel**",TITEL],
  ["**Format**","Video-Gespräch (Fernschaltung) in der Sendung „Good Morning Germany“; davor ein Nachrichtenblock des Gastgebers [0:00–0:07], am Ende Werbung für ein Nahrungsergänzungsmittel und Patreon-Aufruf [1:46–1:49]"],
  ["**Sprecher**","👤 **Tom-Oliver Regenauer** – Gast, Autor · 🎙️ **Gastgeber** von REALTALK MEDIA („Good Morning Germany“, „100% Real Talk“) – Name im Transkript nicht eindeutig ❓; spricht selbst lange Passagen (u. a. [0:00–0:07], [0:36–0:42], [0:45–0:48], [1:14–1:19])"],
  ["**Dauer**","1 Std. 50 Min. (1:49:33)"],
  ["**Datum**","Veröffentlichung nicht ermittelt (April 2026 ❓); aufgenommen nach der Paris-Konferenz vom 17.04.2026, vermutlich zwischen 18. und 25.04.2026 📚"],
  ["**Grundton**","eindringlich, warnend; der Gastgeber stimmt meist zu und widerspricht nur bei Ritualen und beim Pike-Brief teilweise"],
  ["**Hinweis**","Aussagen beider Sprecher sind als ihre Sicht wiedergegeben; daneben steht im Abgleich, was Quellen belegen. Aussagen zu Zionismus, Israel, Rothschild und Ford sind mit Sprecher und Fundstelle wiedergegeben. Regenauer vertreibt selbst Telefone, über die er spricht."]]},
]

# ---------- Reiter 2: Gespräch im Detail ----------
R2 = [
 {"typ":"text","text":f"🔎 Detaillierte Auswertung in der Reihenfolge des Gesprächs – {NAB} Abschnitte. Lesehilfe: 💬 Zitat, 📌 Aussage/Zahl/Beispiel, 🔗 Bezug, 📚 Ergänzung, ❓ unklar. Video: [{TITEL}]({URL})"},
 {"typ":"gespraech","titel":"🧭 Gesprächsverlauf – wann worüber gesprochen wird","dauer":"1:49","themen":THEMEN,
  "teile":[{"von":v,"bis":b,"t":k,"th":th} for (v,b,k,th,_) in A]},
] + [blk for (_,_,_,_,blk) in A]

# ---------- Reiter 3: Zeitachse & Verzeichnisse ----------
ZA = [
 ("1153",1153,"Beginn des Familienarchivs der Orsini (laut Regenauer)","[1:04]",False),
 ("1619",1619,"Gründung der Hamburger Bank – von Regenauer als früher Anfang der Zentralbank-Geschichte genannt","[1:09]",True),
 ("1791",1791,"Gründung der First Bank of the United States (Regenauer: „1832“)","[1:09]",True),
 ("1800",1800,"Napoleon und „seine Zentralbank“ (Banque de France, Jahr ergänzt)","[1:09]",True),
 ("1832",1832,"Veto von Präsident Jackson gegen die Verlängerung der Second Bank of the United States","[1:09]",True),
 ("1871",1871,"Angeblicher Brief Albert Pikes über drei Weltkriege – laut Regenauer in dieser Form nicht existent","[0:49]",True),
 ("1886",1886,"Gründung von Burmah Oil in Glasgow (Regenauer: „1883“)","[0:29]",True),
 ("1901",1901,"Ölkonzession für William Knox D’Arcy in Persien","[0:29]",True),
 ("1909",1909,"Gründung der Anglo-Persian Oil Company, später BP","[0:29]",True),
 ("1914",1914,"Kellogg gründet die Race Betterment Foundation","[0:36]",True),
 ("1920–1927",1920,"Fords „Dearborn Independent“ mit der Serie „The International Jew“","[0:37]",True),
 ("1930er",1933,"Technocracy-Bewegung: Energiebuchhaltung und Karte des „Technate“","[0:14], [0:55]",True),
 ("1953",1953,"Putsch gegen Mossadegh (Operation Ajax)","[0:39]",False),
 ("1966",1966,"Burmah Oil übernimmt Castrol","[0:30]",True),
 ("1974",1974,"Club of Rome: Weltmodell mit zehn Regionen („Mankind at the Turning Point“)","[0:55]",True),
 ("1979",1979,"Islamische Revolution; der Schah kommt mit Hilfe David Rockefellers in die USA","[0:31], [0:40]",True),
 ("1980–1988",1980,"Iran-Irak-Krieg; laut Regenauer Israel größter Waffenlieferant des Iran","[0:32]",True),
 ("1980",1980,"Errichtung der Georgia Guidestones","[0:50]",True),
 ("1982",1982,"Sturz Helmut Schmidts durch konstruktives Misstrauensvotum","[0:40]",True),
 ("1991",1991,"Golfkrieg – von Regenauer als Beispiel eines „richtigen Kriegs“ genannt","[0:43]",True),
 ("2000",2000,"BP Amoco kauft Burmah Castrol","[0:30]",True),
 ("2007",2007,"Erstes iPhone – Regenauer datiert den Rückgang der Aufmerksamkeit ab hier","[1:36]",True),
 ("2013",2013,"Freigabe der internen CIA-Geschichte zum Putsch 1953","[0:39]",True),
 ("2022",2022,"Laut Regenauer aktive Zentralbank-Digitalwährung im Iran ❓","[0:28]",False),
 ("2023",2023,"Studie mit 76,1 % Impfquote im Iran (laut Regenauer) ❓","[0:28]",False),
 ("2024",2024,"Regenauers Buch „Truman Show“","[0:42]",False),
 ("21.11.2024",2024,"IStGH erlässt Haftbefehle gegen Netanjahu und Gallant","[0:05], [0:46]",True),
 ("Nov. 2024",2024,"Regenauer kündigt in einem Text einen US-Angriff auf den Iran an","[0:43]",False),
 ("2025",2025,"Gespräch mit Greg Reese: Vorhersage von Angriff und Regimewechsel","[0:43]",False),
 ("28.04.2025",2025,"Unterhauswahl in Kanada: Liberale unter Carney gewinnen","[1:08]",True),
 ("12.06.2025",2025,"IAEA-Gouverneursrat stellt Nichteinhaltung durch den Iran fest","[0:47]",True),
 ("08.08.–24.11.2025",2025,"Teilstopp deutscher Rüstungsexporte nach Israel für Gaza-taugliche Güter","[0:02]",True),
 ("8./9.01.2026",2026,"Niederschlagung der Proteste im Iran; Opferzahlen je nach Quelle sehr unterschiedlich","[0:46]",True),
 ("28.02.2026",2026,"Beginn israelischer und US-Angriffe auf den Iran","[0:19]",True),
 ("01.03.2026",2026,"Iranisches Staatsfernsehen bestätigt Tod Ali Chameneis; Straße von Hormus gesperrt","[0:13]",True),
 ("11.03.2026",2026,"IEA-Mitglieder einigen sich auf Freigabe von 400 Mio. Barrel Notfallreserven","[0:11]",True),
 ("08.04.2026",2026,"Waffenruhe angekündigt","[0:19]",True),
 ("11.04.2026",2026,"Gespräche in Islamabad ohne Ergebnis","[0:19]",True),
 ("13.04.2026",2026,"US-Blockade des Schiffsverkehrs von und zu iranischen Häfen","[0:13]",True),
 ("14.04.2026",2026,"ELSC meldet Unterstützung einer Strafanzeige in Deutschland","[0:01]",False),
 ("17.04.2026",2026,"Paris-Konferenz zur Straße von Hormus; Merz bietet Minenräumung und Seeaufklärung an","[0:02]",True),
 ("Mai–Juni 2026",2026,"Regenauers Tour („vorerst letzte“), ohne Videoaufzeichnung","[0:15], [1:46]",False),
 ("01.06.2026",2026,"Erscheinen von Regenauers Buch „Degeneration X“ im Handel","[0:16]",False),
 ("02.01.2027",2027,"Geplanter Start der deutschen EUDI-Wallet (Regenauer: „5.1.27“)","[0:18]",True),
]
ZEIT = {"typ":"zeitachse","titel":"📅 Zeitachse – Ereignisse, die im Gespräch vorkommen","eintraege":[
  {"z":z,"j":j,"t":t,"f":f,"e":e} for (z,j,t,f,e) in sorted(ZA, key=lambda x:(x[1], ZA.index(x)))]}
R3 = [ZEIT,
 {"typ":"tabelle","kopf":["👤 Person","Wer / was","Rolle im Gespräch","Fundstelle"],"zeilen":[
  ["Tom-Oliver Regenauer","Autor (regenauer.press), lebt in der Schweiz (Tessin)","Gast","durchgehend"],
  ["Gastgeber (REALTALK MEDIA)","Moderator von „Good Morning Germany“ und „100% Real Talk“; nennt den Iran seine Heimat; Name nicht eindeutig ❓","Gastgeber, Nachrichtenblock, eigene Thesen","[0:00–0:07], [0:19]"],
  ["Friedrich Merz","Bundeskanzler","Paris-Konferenz, „BlackRock-Merz“","[0:02], [0:53], [0:56]"],
  ["Donald Trump","US-Präsident","„Trading Desk“, Widersprüche, Technate","[0:21], [0:55], [0:57]"],
  ["Benjamin Netanjahu","Israels Ministerpräsident","Gegenstand von Gerüchten, IStGH-Haftbefehl","[0:05], [0:46–0:48]"],
  ["Javier Milei","Präsident Argentiniens","Treffen mit Netanjahu, Gerücht","[0:05], [0:48], [0:52]"],
  ["Fatih Birol","Exekutivdirektor der IEA","„Net-Zero-Verfechter“","[0:12]"],
  ["Mohammad Reza Pahlavi","Schah des Iran bis 1979","Rockefeller-Freundschaft, 60-Minutes-Interview","[0:31], [0:40–0:41]"],
  ["David Rockefeller","Bankier (Chase Manhattan)","Schah, Memoiren, Wirkung","[0:31], [1:16]"],
  ["Mohammad Mossadegh","Premier des Iran, 1953 gestürzt","Operation Ajax","[0:39]"],
  ["Moses Hess","Frühsozialist, Vordenker des Zionismus","Ursprung von Sozialdemokratie/Kommunismus laut Regenauer","[0:34]"],
  ["John Harvey Kellogg","Arzt, Sanatorium Battle Creek","Eugenik, Cornflakes (Gastgeber)","[0:36–0:38]"],
  ["Henry Ford","Autoindustrieller","„The International Jew“","[0:37]"],
  ["George Bernard Shaw, Bertrand Russell","Schriftsteller, Philosoph","Eugenik-Bezüge","[0:36]"],
  ["Helmut Schmidt","Bundeskanzler 1974–1982","Sturz 1982, Bohemian Grove","[0:40], [0:42]"],
  ["Dirk Pohlmann","Journalist","Quelle des Gastgebers zum Schmidt-Sturz","[0:40]"],
  ["Greg Reese","US-Videojournalist (früher Infowars)","Prognose zum Iran-Angriff","[0:43]"],
  ["Ernst Wolff","Finanzautor","BIZ-Hinweis","[0:27]"],
  ["Harald Kujat","General a. D.","vom Gastgeber genannt","[0:47]"],
  ["Albert Pike","Freimaurer (19. Jh.)","angeblicher Brief","[0:49]"],
  ["James Corbett","Corbett Report","Quelle zum Pike-Brief, Telefonprojekt","[0:49], [1:28]"],
  ["Walter Veith","Vortragsredner (im Transkript „Fight“)","früherer Gast","[0:52]"],
  ["Ursula von der Leyen","EU-Kommissionspräsidentin","Kompetenzausbau","[0:55]"],
  ["Martin Sonneborn","EU-Abgeordneter","Post zur Kommission","[0:55]"],
  ["Peter Thiel","Investor, Palantir-Mitgründer","Weltbild, Frankfurt","[0:59–1:02], [1:05]"],
  ["Alex Karp","Palantir-Chef","Buch, Frankfurt","[1:01–1:03]"],
  ["Mark Zuckerberg","Meta-Chef","Vergleich mit Thiel","[1:00–1:01]"],
  ["Yanis Varoufakis","Ökonom","ordnete Karps Thesen ein","[1:03]"],
  ["Mark Carney","Premier Kanadas, früher Zentralbankchef","Chatham House, FSB, Bail-in","[1:07–1:08]"],
  ["Cecil Rhodes, Alfred Milner","Round Table","Umfeld der Chatham-House-Gründung","[1:06]"],
  ["Napoleon","Kaiser der Franzosen","Zentralbank finanziert Krieg","[1:09]"],
  ["J. P. Morgan","Bankier","rettete das US-Finanzsystem","[1:10]"],
  ["Kollegah","Rapper","Song zum Zionismus","[1:14]"],
  ["Yuval Noah Harari","Historiker","„hat in vielem Recht“","[1:27]"],
  ["Hakim (Nachname unklar ❓)","Programmierer, Aktivist","Telefonprojekt","[1:28–1:30]"],
  ["Whitney Webb, Derrick Broze","Journalisten","nutzen die Telefone","[1:28], [1:30]"],
  ["Silvia Lorenzen (Schreibweise ❓)","Autorin","Buch „Organisiert euch“","[1:19], [1:23]"],
 ]},
 {"typ":"tabelle","kopf":["🗺️ Ort","Rolle","Fundstelle"],"zeilen":[
  ["Straße von Hormus","Engpass für Öl und LNG, Sperrung und Blockade","[0:02], [0:13], [0:53]"],
  ["Iran","Kriegsschauplatz; Heimat des Gastgebers","durchgehend"],
  ["Paris","Konferenz zur Hormus-Mission","[0:02]"],
  ["Islamabad (Pakistan)","Friedensgespräche","[0:19]"],
  ["Brüssel","„Demokratie“-Banner am EU-Gebäude","[0:10]"],
  ["Indien, Russland","Raffineriebrände","[0:12]"],
  ["Asien","erste von der Energiekrise betroffene Region","[0:15], [0:17]"],
  ["Afrika (Hungergebiete)","UN-Essensausgabe per ID","[0:19]"],
  ["Liechtenstein","Römisches Reich nicht für beendet erkannt (laut Regenauer)","[0:33]"],
  ["Battle Creek (Michigan)","Kelloggs Sanatorium","[0:37]"],
  ["Bohemian Grove (Kalifornien)","Sommerlager; Schmidt, Rituale","[0:42], [1:12]"],
  ["Berlin","Israel-Fahne an Mauerresten","[0:48]"],
  ["Spanien","Regierung gegen den Krieg","[0:52]"],
  ["Grönland, Kanada, Kuba","Technate-Pläne Trumps (laut Regenauer)","[0:55]"],
  ["Frankfurt am Main","Thiel, Karp, Rothschild","[1:01], [1:05]"],
  ["London (Chatham House)","Thinktank","[1:06]"],
  ["Australien","Altersgrenze für soziale Medien","[1:40]"],
  ["Tessin","Aufenthaltsort Regenauers","[1:45]"],
 ]},
 {"typ":"tabelle","kopf":["📖 Begriff","Erklärung","Fundstelle"],"zeilen":[
  ["IEA-Maßnahmen-Tracker","„2026 Energy Crisis Policy Response Tracker“ der Internationalen Energieagentur","[0:11], [0:22]"],
  ["Technokratie / Technate","Bewegung der 1930er: Steuerung nach Energiebuchhaltung; „Technate“ = geplanter nordamerikanischer Großraum","[0:14], [0:55]"],
  ["Bürger-Wallet / EUDI-Wallet","staatliche App für Ausweis und Nachweise nach eIDAS 2.0","[0:18], [0:58]"],
  ["E-ID","elektronischer Identitätsnachweis","[0:28], [0:52]"],
  ["Zentralbank-Digitalwährung (CBDC)","digitales Zentralbankgeld","[0:28], [0:58]"],
  ["Polymarket","Wettplattform auf Ereignisse","[0:21]"],
  ["BRICS","Staatengruppe um Brasilien, Russland, Indien, China, Südafrika; seit 2024 auch Iran","[0:27]"],
  ["BIZ","Bank für Internationalen Zahlungsausgleich, Basel","[0:27]"],
  ["Operation Ajax","Deckname des Putsches 1953 gegen Mossadegh","[0:39]"],
  ["Fasces","römisches Rutenbündel mit Beil, Symbol der Amtsgewalt","[0:33]"],
  ["Hasbara","israelische Öffentlichkeitsarbeit (Begriff des Gastgebers)","[0:05]"],
  ["Embedded journalism","Reporter, die mit Truppen mitreisen (Golfkrieg)","[0:44]"],
  ["Deagel-Liste","Bevölkerungsprognosen einer Webseite – laut Regenauer unseriös","[0:50]"],
  ["Georgia Guidestones","Granitmonument von 1980, 2022 zerstört","[0:50]"],
  ["Financial Stability Board (FSB)","internationales Gremium für Finanzstabilität","[1:07]"],
  ["Bail-in","Beteiligung von Gläubigern/Einlegern an Bankrettungen statt Steuergeld","[1:08]"],
  ["Cremation of Care","Eröffnungsritual im Bohemian Grove","[1:14]"],
  ["Voluntarismus","Ordnung auf Grundlage freiwilliger Zusammenarbeit ohne Staat","[1:19]"],
  ["Isolationspandemie","Regenauers Begriff für den Rückgang echter sozialer Kontakte","[1:25]"],
  ["GrapheneOS","quelloffenes, auf Datenschutz ausgerichtetes Android-Betriebssystem","[1:28]"],
  ["Predictive Programming","Vorstellung, Filme bereiteten auf künftige Ereignisse vor (Gastgeber)","[1:44]"],
 ]},
 {"typ":"tabelle","kopf":["📊 Zahl im Gespräch","Angabe","Fundstelle"],"zeilen":[
  ["Publikum Ben Shapiro","−85 % seit 7.10.2023 (MintPress, Gastgeber)","[0:01]"],
  ["US-Kriege","3 Präsidenten, 9 Länder, 23 Jahre, 11 Mio. Zivilisten (Gastgeber)","[0:06]"],
  ["Simo-Interview","~700.000 Aufrufe","[0:09]"],
  ["Raffinerie-Ereignisse","~45, davon 15–20 Anlagen","[0:12]"],
  ["Klimaanlagen in Asien","bis 25 °C","[0:11]"],
  ["Benzinpreis","evtl. 5 € pro Liter im Sommer","[0:17]"],
  ["Kontingente (Beispiel)","20 l privat, 200 l Gewerbe","[0:18]"],
  ["Erholung der Versorgung","mindestens 6 Monate","[0:23]"],
  ["Elite","8.000 Menschen gegen 8 Mrd. (Gastgeber); 8–10.000 (Regenauer)","[0:26], [1:13]"],
  ["Impfquote Iran","76,1 % (Studie 2023)","[0:28]"],
  ["E-ID-Pflicht Iran","ab 15 Jahren","[0:28]"],
  ["Golfkrieg","2.000 Tote pro Tag (Gastgeber)","[0:46]"],
  ["Proteste Iran","„40 bis 90.000“ in 48 Stunden (vom Gastgeber genanntes Narrativ)","[0:46]"],
  ["Orsini","3 Päpste, 60 Kardinäle, Archiv ab 1153","[1:04]"],
  ["Thinktanks","Liste der 10 einflussreichsten","[1:06]"],
  ["First Bank of the US","70–80 % des Geldes aus Großbritannien","[1:09]"],
  ["Quellen Malteser-Artikel","600–800 (sonst ~100)","[1:12]"],
  ["Übergangsgeld (Szenario)","500 oder 1.000 € digital","[0:58]"],
  ["Staat in heutiger Form","seit ~150 Jahren","[1:20]"],
  ["Selbstorganisation","90–95 % des Lebens","[1:20]"],
  ["KI-Musik","60.000 Uploads pro Tag","[1:22]"],
  ["Aufmerksamkeit","von 16–19 auf 9–11 Sekunden seit 2007","[1:35–1:36]"],
  ["Buch „Organisiert euch“","130 Seiten","[1:21]"],
 ]},
]

# ---------- Reiter 4: Abgleich & Daten ----------
AB = [
 ["Der Iran-Krieg sei „das Thema überhaupt“; Hormus werde blockiert [0:13], [0:19].",
  "Der Krieg begann am 28.02.2026 mit israelischen und US-Angriffen; am 01.03.2026 bestätigte das iranische Staatsfernsehen den Tod von Ali Chamenei; die Straße von Hormus war gesperrt, mindestens 150 Öl- und LNG-Tanker lagen vor Anker.",
  Q['start']+" · "+Q['iea']],
 ["Die IEA habe eine eigene Webseite und einen Tracker für Maßnahmen wie Preisdeckel, Rationierung, Homeoffice, Klimaanlagen eingerichtet; das sei nichts Kurzfristiges [0:11–0:12].",
  "Die IEA betreibt den „2026 Energy Crisis Policy Response Tracker“; erfasst werden Maßnahmen zur Energieeinsparung und zur Entlastung von Verbrauchern. Die IEA nennt die Störung „die größte in der Geschichte des Ölmarkts“; ihre Mitglieder einigten sich am 11.03. auf die bisher größte Freigabe von Notfallreserven (400 Mio. Barrel).",
  Q['ieatr']+" · "+Q['iea']],
 ["Die „niemals blockierte“ Straße werde von den Amerikanern blockiert, um eine Blockade zu verhindern [0:13].",
  "Nach Kriegsbeginn war die Durchfahrt durch Hormus stark eingeschränkt; seit 13.04.2026 blockiert das US-Zentralkommando zusätzlich den Schiffsverkehr von und zu iranischen Häfen.",
  Q['bt']+" · "+Q['iea']],
 ["Gastgeber: Friedensgespräche in Pakistan abgesagt, Waffenruhe gebrochen [0:19].",
  "Trump kündigte am 08.04.2026 eine Waffenruhe an; Delegationen der USA und des Iran verhandelten am 11.04. in Islamabad 21 Stunden ohne Ergebnis.",
  Q['bt']],
 ["Merz habe in Paris eine deutsche Beteiligung (Minenräumung, Seeaufklärung) in Aussicht gestellt [0:02–0:03], [0:53].",
  "Am 17.04.2026 erklärte Merz in Paris die Bereitschaft zu Minenräumung und Seeaufklärung – erst nach Ende der Kampfhandlungen, mit sicherer Rechtsgrundlage (etwa UN-Sicherheitsratsresolution), Kabinettsbeschluss und Bundestagsmandat.",
  Q['paris']],
 ["Deutschland habe auch während des Iran-Kriegs Waffenexporte nach Israel genehmigt (Nachrichtenblock) [0:02].",
  "Laut Antworten des Wirtschaftsministeriums an MdB Ulrich Thoden wurden vom 28.02. bis 27.03.2026 Ausfuhren von rund 6,6 Mio. € genehmigt; nach Aufhebung des Teilstopps (08.08.–24.11.2025) waren es in vier Monaten rund 166,95 Mio. €, nur „sonstige Rüstungsgüter“, keine Kriegswaffen.",
  Q['ja']],
 ["Europa sei nach Asien die zweite betroffene Region [0:17].",
  "2024 flossen rund 20 Mio. Barrel Öl pro Tag durch Hormus (≈ 20 % des Weltverbrauchs, über ein Viertel des Seehandels) sowie etwa ein Fünftel des LNG-Welthandels, vor allem aus Katar; 84 % des Rohöls und 83 % des LNG gingen nach Asien.",
  Q['eia']],
 ["Die deutsche Bürger-Wallet komme „am 5.1.27“; an sie würden Energiekontingente geknüpft [0:18], [0:58].",
  "Als Start der deutschen EUDI-Wallet wird der 02.01.2027 genannt; zum Start dienen Personalausweis bzw. Aufenthaltstitel zur Identifizierung, der Führerschein soll speicherbar sein. Eine Kopplung an Energiekontingente sehen die geprüften Angaben nicht vor.",
  Q['wallet']],
 ["Burmah Oil (Regenauer: 1883) habe die Anglo-Persian Oil Company gegründet, heute BP; Burmah habe auch Castrol [0:29–0:30].",
  "Burmah Oil wurde 1886 in Glasgow gegründet, gründete die Anglo-Persian Oil Company (97 % Anteil), übernahm 1966 Castrol und wurde 2000 von BP Amoco gekauft.",
  Q['burmah']],
 ["Gastgeber: 1953 Operation Ajax – Mossadegh abgesetzt, Schah gestärkt [0:39].",
  "Eine 2013 vom National Security Archive per Informationsfreiheitsgesetz erlangte interne CIA-Geschichte hält fest, der Putsch sei „unter CIA-Leitung“ als Akt der US-Außenpolitik erfolgt; Großbritannien wollte die Verstaatlichung der Anglo-Iranian Oil Company abwenden.",
  Q['cia']],
 ["Regenauer: Hitler habe „die meisten Teile“ von „Mein Kampf“ aus Fords „The International Jew“ abgeschrieben [0:37].",
  "Belegt: Ford finanzierte 1920–1927 den „Dearborn Independent“ mit der Serie „The International Jew“ (Auflage ab 1926 mindestens 900.000), in Deutschland von Theodor Fritsch als Buch verbreitet; Hitler lobte Ford in „Mein Kampf“ als einzigen Amerikaner. Ein Abschreiben großer Teile tragen die geprüften Quellen nicht.",
  Q['ford']],
 ["Gastgeber: Kellogg sei bekennender Eugeniker gewesen, habe Beschneidung ohne Betäubung und Joghurt-Einläufe propagiert, 40 Jungen adoptiert [0:36–0:38].",
  "Kellogg gründete 1914 die Race Betterment Foundation (Eugenik-Register mit dem Eugenics Record Office); er empfahl gegen Masturbation u. a. Beschneidung ohne Betäubung und befürwortete Joghurt-Einläufe. Die Zahl „40 adoptierte Jungen“ ist in den geprüften Quellen nicht belegt ❓.",
  Q['rbf']+" · "+Q['kellogg']],
 ["Gastgeber: Narrativ, die iranische Regierung habe 40.000–90.000 Menschen in 48 Stunden getötet – er hält es für Propaganda [0:46–0:47].",
  "Zu den Protesten im Januar 2026 (Schwerpunkt 8./9.01.): Behörden nannten 3.117 Tote; HRANA bestätigte bis 27.01. 6.126 Tote (5.777 Demonstrierende) und prüfte 17.091 weitere Fälle; Iran Human Rights dokumentierte mindestens 3.428 und hielt bis zu 25.000 für möglich; Iran International meldete über 36.500 für den 8./9.01., nicht unabhängig überprüfbar.",
  Q['hrana']],
 ["Gastgeber: das „Narrativ der Atombombe, die kurz vor dem Abschluss war“ [0:47].",
  "Der IAEA-Gouverneursrat stellte am 12.06.2025 (19 Ja, 3 Nein, 11 Enthaltungen) fest, dass der Iran seit 2019 bei nicht deklariertem Material nicht ausreichend kooperiert und damit Sicherungspflichten nicht einhält; der Iran wies die Resolution als ohne Grundlage zurück. Eine Aussage über den Stand einer Waffe enthält die Quelle nicht ❓.",
  Q['iaea']],
 ["Gastgeber: Netanjahu werde international gesucht – „wegen Völkermord“ bzw. „Kinderschänderei, Massenmord, Genozid“ [0:05], [0:46].",
  "Der Internationale Strafgerichtshof erließ am 21.11.2024 Haftbefehle gegen Netanjahu und Gallant wegen des Kriegsverbrechens des Aushungerns sowie Verbrechen gegen die Menschlichkeit (Mord, Verfolgung, andere unmenschliche Handlungen), Zeitraum 08.10.2023–20.05.2024; zugleich gegen Hamas-Kommandeur Deif. Völkermord ist nicht Gegenstand der Haftbefehle; für den Vorwurf „Kinderschänderei“ gibt es in den geprüften Quellen keinen Beleg.",
  Q['icc']],
 ["Wagenknecht (vom Gastgeber zitiert): Selenskyj solle die Nord-Stream-Sprengung persönlich genehmigt haben [0:04].",
  "Der Generalbundesanwalt ermittelt wegen Herbeiführens einer Sprengstoffexplosion und verfassungsfeindlicher Sabotage; 2025 wurden auf deutschen Haftbefehl ukrainische Verdächtige in Italien (Serhij K.) und Polen (Wolodymyr Z.) festgenommen. Eine Genehmigung durch Selenskyj ist in den geprüften Quellen nicht festgestellt ❓.",
  Q['ns']],
 ["Carney regiere Kanada als „ungewählter Präsident“ [1:08].",
  "Carney ist Premierminister (nicht Präsident); seine Liberale Partei gewann die Unterhauswahl am 28.04.2025. Sein Vorsitz bei Chatham House wurde nicht geprüft ❓.",
  Q['carney']],
 ["Die erste Zentralbank der USA (Regenauer: „1832“) sei zu 70–80 % mit britischem Geld finanziert gewesen [1:09].",
  "Die First Bank of the United States wurde 1791 gegründet (Lizenz bis 1811); 1832 legte Präsident Jackson sein Veto gegen die Verlängerung der Second Bank ein. Die Anteile ausländischer Eigner wurden nicht geprüft ❓.",
  Q['fedb1']+" · "+Q['fedb2']],
 ["Bei Spotify würden täglich 60.000 KI-Titel hochgeladen [1:22].",
  "Die Zahl stammt von Deezer: Im Januar 2026 erhielt die Plattform täglich über 60.000 vollständig KI-erzeugte Titel, rund 39 % der eingehenden Musik; sie machten bis zu 3 % der Streams aus. Für Spotify liegt keine geprüfte Zahl vor ❓.",
  Q['deezer']],
 ["Regenauer spricht vom „zionistisch-anglo-amerikanischen Imperium“; „das waren alles Zionisten und Eugeniker“ [0:32]; der Gastgeber nennt Frankfurt als Ursprung der Rothschild-Dynastie [1:05].",
  "Die Bundeszentrale für politische Bildung beschreibt es als Merkmal von strukturellem Antisemitismus, wenn komplexe wirtschaftliche oder politische Zusammenhänge vereinfacht und einer kleinen Personengruppe mit böswilliger Absicht zugeschrieben werden. Regenauer verwendet hier eine politische Kategorie („Zionisten“); zu seinen eigenen Unterscheidungen siehe das {{a:regenauer-masterpeace|Masterpeace-Gespräch}}.",
  Q['bpb']],
]

KURS = {"typ":"kurs","id":"iran-brent","titel":"📈 Ölpreis Brent – Jahresdurchschnitt","reihen":[
  {"name":"Brent (Jahresdurchschnitt)","kurz":"US-$/Barrel","einheit":"US-$ je Barrel","dez":1,"hoeherGut":None,"punkte":[
   [2000,28.8],[2001,24.7],[2002,25.1],[2003,28.8],[2004,38.2],[2005,54.7],[2006,65.6],[2007,72.7],[2008,97.3],[2009,61.6],
   [2010,79.8],[2011,111.5],[2012,112.0],[2013,109.0],[2014,99.3],[2015,53.0],[2016,45.1],[2017,54.9],[2018,71.6],[2019,64.2],
   [2020,43.3],[2021,70.8],[2022,99.0],[2023,82.3],[2024,79.9],[2025,68.3]]}],
  "hoeherGut":None,"vergleich":False,
  "quelle":Q['brent']+" (Internationaler Währungsfonds, Primary Commodity Prices), Stand 24.03.2026",
  "hinweis":"Bezug zum Gespräch [0:11–0:18], [0:21]: Energiekrise, Preise „erst nach oben“, Märkte reagierten auf Ankündigungen. Jahreswerte bis 2025 – der Preisverlauf seit Kriegsbeginn (28.02.2026) ist darin noch nicht enthalten."}
B_HORMUS = {"typ":"balken","titel":"📊 Straße von Hormus 2024 – Anteile in Prozent","einheit":"%","dez":0,"zeilen":[
  ["Anteil am weltweiten Verbrauch von Ölflüssigkeiten",20],["Anteil am seegestützten Ölhandel (über)",25],["Anteil am LNG-Welthandel (etwa)",20],
  ["davon Rohöl mit Ziel Asien",84],["davon LNG mit Ziel Asien",83],["Rohöl nach China, Indien, Japan, Südkorea",69]],
  "quelle":Q['eia']+", Stand Juni 2025 (Daten 2024)",
  "hinweis":"Bezug zum Gespräch [0:13], [0:17]: Hormus-Blockade; Asien zuerst, Europa als zweite betroffene Region. Insgesamt flossen 2024 rund 20 Mio. Barrel pro Tag; Umgehungspipelines Saudi-Arabiens und der VAE könnten im Notfall etwa 2,6 Mio. Barrel pro Tag aufnehmen."}
B_OPFER = {"typ":"balken","titel":"📊 Proteste im Iran, Januar 2026 – gemeldete Todeszahlen je Quelle","einheit":"Tote","dez":0,"zeilen":[
  ["Iranische Behörden (erste offizielle Zahl)",3117],["Iran Human Rights (dokumentiert)",3428],["HRANA (bestätigt, Stand 27.01.)",6126],
  ["HRANA (bestätigt + in Prüfung)",23217],["Iran International (8./9.01., nicht überprüfbar)",36500]],
  "quelle":Q['hrana']+", Stand 27.01.2026",
  "hinweis":"Bezug zum Gespräch [0:46–0:47]: Der Gastgeber nennt das Narrativ „40 bis 90.000 in 48 Stunden“ und hält es für Propaganda. Die Zahlen messen Verschiedenes (bestätigt, dokumentiert, gemeldet); HRANA „bestätigt + in Prüfung“ ist die Summe 6.126 + 17.091."}
B_RUEST = {"typ":"balken","titel":"📊 Genehmigte Rüstungsexporte nach Israel – drei Zeiträume (Mio. €)","einheit":"Mio. €","dez":2,"zeilen":[
  ["Teilstopp 08.08.–24.11.2025 (trotzdem genehmigt)",10.44],["Vier Monate nach Aufhebung ab 24.11.2025",166.95],["Iran-Krieg 28.02.–27.03.2026",6.6]],
  "quelle":Q['ja']+" (Antworten des Bundeswirtschaftsministeriums an MdB Ulrich Thoden), Stand 16.04.2026",
  "hinweis":"Bezug zum Gespräch [0:01–0:02]: Nachrichtenblock – Deutschland genehmige auch während des Iran-Kriegs Waffenexporte nach Israel. Die Zeiträume sind unterschiedlich lang; nach Aufhebung des Teilstopps nur „sonstige Rüstungsgüter“, keine Kriegswaffen."}
VGL = {"typ":"vergleich","titel":"⚖️ Zahlen im Gespräch und Daten nebeneinander","la":"Im Gespräch genannt","lb":"Daten laut Quelle","zeilen":[
  {"n":"Gründungsjahr Burmah Oil","a":1883,"b":1886,"einheit":"Jahr","f":"[0:29]","q":Q['burmah']},
  {"n":"Gründungsjahr der ersten US-Zentralbank (First Bank)","a":1832,"b":1791,"einheit":"Jahr","f":"[1:09]","q":Q['fedb1']},
  {"n":"KI-Musiktitel pro Tag (Gespräch: Spotify; Daten: Deezer)","a":60000,"b":60000,"einheit":"Titel","f":"[1:22]","q":Q['deezer']},
  {"n":"Tote bei den Protesten im Iran (Gespräch: untere Zahl des Narrativs; Daten: HRANA bestätigt)","a":40000,"b":6126,"einheit":"Tote","f":"[0:46]","q":Q['hrana']},
  {"n":"Start der deutschen EUDI-Wallet (Tag im Januar 2027)","a":5,"b":2,"einheit":"Januar","f":"[0:18]","q":Q['wallet']}]}

R4 = [
 {"typ":"text","text":"Neutraler Abgleich: links die Aussage im Gespräch, rechts die gängige Darstellung bzw. Daten mit Quelle. Die Bewertung bleibt dem Leser."},
 {"typ":"tabelle","kopf":["Aussage im Gespräch","Gängige Darstellung (Mainstream) / Daten 📚","Quelle"],"stapel":True,"zeilen":AB},
 KURS, B_HORMUS, B_OPFER, B_RUEST, VGL,
 {"typ":"abschnitt","titel":"🧩 Spannungen im Gespräch","liste":[
  "Der Gastgeber widerspricht beim Albert-Pike-Brief teilweise: Die Sache sei „komplizierter“, Material aus den 1800ern sei 1953 ausgeschmückt worden [0:51]; Regenauer bleibt dabei, ohne Original existiere der Brief nicht.",
  "Bei Ritualen sucht der Gastgeber „eine Mitte“ (alte Ritualistik seit Sabbatai Zvi und den Frankisten), Regenauer betont Image-Design und warnt, den Gegner zu überschätzen [1:14–1:16].",
  "Regenauer hält Prognosen sonst für unseriös, macht hier aber ausdrücklich eine (Sommerurlaub fällt aus, Tour nächstes Jahr „ziemlich ausgeschlossen“) und hofft, sich zu irren [0:14], [0:16], [0:26].",
  "Regenauer weist mehrere populäre Erzählungen zurück (Pike, Deagel, Guidestones, Netanjahu-Milei), stützt andere Thesen aber selbst auf nicht genannte Studien (Impfquote, Aufmerksamkeitsspanne) [0:28], [1:36].",
  "Der Gastgeber nennt die Opferzahl der Proteste Propaganda, während unabhängige Menschenrechtsgruppen tausende bestätigte Tote dokumentieren – siehe Diagramm.",
  "Regenauer kritisiert Big Tech und Konsum, verkauft aber selbst Telefone; er legt das offen und betont, es bleibe wenig hängen [1:30–1:33].",
  "Gegen Altersverifikation argumentiert Regenauer mit der Umgehung per VPN; der Gastgeber hält Regulierung grundsätzlich für richtig, fragt aber nach dem Preis [1:39–1:40]."]},
 {"typ":"abschnitt","titel":"💡 Was man mitnehmen kann","liste":[
  "Der IEA-Tracker ist öffentlich einsehbar; er zeigt, welche Länder welche Spar- und Entlastungsmaßnahmen ergreifen.",
  "Für die Abhängigkeit von Hormus gibt es klare Zahlen der EIA: rund ein Fünftel des Weltölverbrauchs und des LNG-Handels, ganz überwiegend für Asien.",
  "Historische Punkte im Gespräch sind teils gut belegt (Burmah Oil/BP, Putsch 1953 unter CIA-Leitung, Fords „The International Jew“, Kelloggs Eugenik), teils weichen Jahreszahlen ab (Burmah 1886, First Bank 1791).",
  "Opferzahlen in Kriegen und Aufständen unterscheiden sich je nach Quelle stark – es lohnt sich, zwischen bestätigt, gemeldet und geschätzt zu unterscheiden.",
  "Regenauers praktischer Kern ist unabhängig von der Deutung: lokale Kontakte, Vereine, Selbstorganisation und ein bewusster Umgang mit Smartphone und KI."]},
 {"typ":"abschnitt","titel":"❓ Offen","liste":[
  "Wer ist der Gastgeber von REALTALK MEDIA, und wann wurde das Video veröffentlicht?",
  "Welche Studie nennt 76,1 % Impfquote im Iran (2023)? Ist die iranische Digitalwährung seit 2022 aktiv, gilt eine E-ID-Pflicht ab 15?",
  "Welche rund 45 Raffinerie-Ereignisse meint Regenauer, und wie viele davon sind Angriffe, Unfälle oder Brände?",
  "In welchem Umfang lieferte Israel in den 1980er-Jahren Waffen an den Iran (Iran-Contra-Zusammenhang)?",
  "Trifft die Liechtenstein-Behauptung zum Ende des Heiligen Römischen Reichs zu?",
  "Ist Mark Carney Vorsitzender von Chatham House? Welche Thinktank-Liste meint Regenauer?",
  "Welches Buch Helmut Schmidts beschreibt Bohemian Grove?",
  "Welche Studie zur Aufmerksamkeitsspanne (16–19 → 9–11 Sekunden) ist gemeint?",
  "Woher stammt das vom Gastgeber beschriebene Kolonial-Foto (Südafrika oder Kongo-Freistaat)?",
  "Für den Insiderhandel-Vorwurf rund um Ankündigungen Trumps nennt Regenauer keine Belege; Ermittlungen dazu wurden nicht geprüft."]},
 {"typ":"abschnitt","titel":"🔎 Weiter recherchieren","liste":[
  "IEA: 2026 Energy Crisis Policy Response Tracker und Oil Market Reports ab März 2026.",
  "EIA: Daten zu Hormus-Flüssen 2025/2026; Preisreihen Brent monatlich seit Februar 2026.",
  "Bundesregierung/Bundestag: Mandat für eine Hormus-Mission; Antworten zu Rüstungsexporten nach Israel.",
  "Gesetz und Zeitplan der EUDI-Wallet (eIDAS 2.0) in Deutschland; Freiwilligkeit der Nutzung.",
  "Technocracy Inc. (1930er): Energiebuchhaltung und „Technate“-Karte; Club of Rome, „Mankind at the Turning Point“ (1974).",
  "Iran-Contra-Ermittlungen (Tower Commission, Kongressbericht 1987) zu Waffenlieferungen an den Iran.",
  "Financial Stability Board: „Key Attributes of Effective Resolution Regimes“ (2011) und EU-Bankenabwicklungsrichtlinie (BRRD) zum Bail-in.",
  "Zum Vertiefen im Kompendium: {{a:regenauer-kontrolle|Vortrag „Bis 2030“}}, {{a:regenauer-masterpeace|Masterpeace-Gespräch}}, {{a:ungeskriptet-regenauer|Regenauer bei {ungeskriptet}}}, {{w:kriege|Kriege}}, {{w:geld|Geld}}."]},
]

# Platzhalter in den Kacheln füllen
for kl in R1[0]['kacheln']:
    if kl[0] == '__AB__': kl[0] = str(len(AB))
    if kl[0] == '__ZA__': kl[0] = str(len(ZA))

REITER = [
 {"id":K,"titel":f"{G}: Überblick","bloecke":R1},
 {"id":K+"ab","titel":f"{G}: Gespräch im Detail","bloecke":R2},
 {"id":K+"zeit","titel":f"{G}: Zeitachse & Verzeichnisse","bloecke":R3},
 {"id":K+"abgleich","titel":f"{G}: Abgleich & Daten","bloecke":R4},
]
QUELLEN = [[f"Video: {TITEL} – {KANAL} (YouTube)", URL]] + [[tit(k), url(k)] for k in Q]
OUT = {"k":K,"gast":GAST,"reiter":REITER,
 "folgen_zeile":[DATUM, f"{GAST} (Autor)", TITEL,
   "Iran-Krieg, Energiekrise & Rationierung, Bürger-Wallet, Iran & Empire (Burmah Oil, 1953), Technate, Chatham House, Gerüchte geprüft, lokale Netzwerke",
   f"{{{{a:regenauer-{K}|hier: {G}}}}}", f"[ansehen]({URL})"],
 "baum_ast":{"gruppe":"🏛️ Macht & Geschichte","t":"👤 Tom-Oliver Regenauer bei REALTALK MEDIA – Iran-Krieg, Energiekrise, digitale Zuteilung, Empire"},
 "neu":{"d":"2026-11-12","t":"Regenauer – Iran und Energiekrise","k":f"Warum es jetzt gefährlich wird: Regenauer über Iran-Krieg, Energiekrise und digitale Zuteilung – {NAB} Abschnitte, Abgleich mit Quellen, 5 Diagramme.","h":f"#a-regenauer-{K}","art":"Video"},
 "quellen":QUELLEN,
 "web":[["Tom-Oliver Regenauer – YouTube-Kanal","https://www.youtube.com/@tomregenauer"]]}
json.dump(OUT, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'folge.json'),'w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', NAB, 'Abschnitte,', len(AB), 'Abgleich,', len(ZA), 'Zeitachse')
