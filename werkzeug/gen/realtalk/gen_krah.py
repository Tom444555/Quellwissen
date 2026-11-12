# -*- coding: utf-8 -*-
# Erzeugt folge.json für „MAXIMILIAN KRAH über Nazi-Vorwürfe, Pädophilie & die digitale Zukunft“ (K = krah, Sammelstelle A-12 realtalk)
import json, os
K = 'krah'; G = 'Krah'
URL = 'https://www.youtube.com/watch?v=3bZNy46G1kY'
TITEL = 'MAXIMILIAN KRAH über Nazi-Vorwürfe, Pädophilie & die digitale Zukunft'
GAST = 'Maximilian Krah'
KANAL = 'REALTALK MEDIA'
DATUM = '2025 ❓'
DAUER = '2 Std. 4 Min.'
ROLLE = 'AfD-Bundestagsabgeordneter (seit 2025), Jurist; 2019–2025 Mitglied des Europäischen Parlaments'

# ---------- Quellen (alle geprüft) ----------
Q = dict(
 zdf='[ZDFheute (08.05.2025): AfD-Verfahren – Verfassungsschutz gibt Stillhaltezusage](https://www.zdfheute.de/politik/deutschland/afd-verfassungsschutz-stillhaltezusage-bundesverfassungsgericht-100.html)',
 srf='[SRF News (26.02.2026): Teilerfolg vor Gericht – AfD gewinnt in Eilverfahren um Einstufung als rechtsextrem](https://www.srf.ch/news/international/teilerfolg-vor-gericht-afd-gewinnt-in-eilverfahren-um-einstufung-als-rechtsextrem)',
 lto='[LTO (11.09.2025): Bundestag hebt Maximilian Krahs Immunität auf – Ermittlungen wegen Bestechlichkeit und Geldwäsche](https://www.lto.de/recht/nachrichten/n/aufhebung-immunitaet-bundestag-abgeordneter-maximilian-krah-ermittlungen-bestechlichkeit-geldwaesche)',
 beckjg='[beck-aktuell (30.09.2025): Ehemaliger Krah-Mitarbeiter wegen Spionage verurteilt](https://www.beck-aktuell.de/heute-im-recht/rechtsprechung/ehemaliger-krah-mitarbeiter-wegen-spionage-verurteilt-2025-09-30)',
 wiki='[Wikipedia (engl.): Maximilian Krah](https://en.wikipedia.org/wiki/Maximilian_Krah)',
 wk162='[Bundeswahlleiterin: Bundestagswahl 2025, Wahlkreis 162 Chemnitzer Umland – Erzgebirgskreis II](https://bundeswahlleiterin.de/bundestagswahlen/2025/ergebnisse/bund-99/land-14/wahlkreis-162.html)',
 wk115='[IT.NRW: Bundestagswahl 2025, Wahlkreis 115 Duisburg II (PDF)](https://wahlergebnisse.nrw/bundestagswahlen/2025/aktuell/pdf/a115bw25.pdf)',
 eufert='[Eurostat, demo_find: Fertility indicators – Total fertility rate (DE, TR)](https://ec.europa.eu/eurostat/databrowser/view/demo_find/default/table?lang=de)',
 destgeb='[Destatis, Pressemitteilung Nr. 230 (01.07.2026): Zusammengefasste Geburtenziffer sinkt im Jahr 2025 auf 1,32 Kinder je Frau](https://www.destatis.de/DE/Presse/Pressemitteilungen/2026/07/PD26_230_12.html)',
 eusoz='[Eurostat, tps00098: Expenditure on social protection as percentage of GDP (DE)](https://ec.europa.eu/eurostat/databrowser/view/tps00098/default/table?lang=de)',
 destod='[Destatis, Pressemitteilung (Juni 2025): Öffentlicher Dienst 2024 – Mehr Beschäftigte für Bildung und Kinderbetreuung](https://www.destatis.de/DE/Presse/Pressemitteilungen/2025/06/PD25_212_741.html)',
 nato='[NATO: Defence Expenditure of NATO Countries (2014–2025), PDF, Datenstand 03.06.2025](https://nato.int/content/dam/nato/webready/documents/finance/def-exp-2025-en.pdf)',
 bmvg='[BMVg (25.06.2025): NATO-Gipfel 2025 – historischer Beschluss zu Verteidigungsausgaben](https://www.bmvg.de/de/aktuelles/nato-gipfel-2025-historischer-beschluss-verteidigungsausgaben-5952094)',
 hib='[Bundestag, hib 388/2025 (05.09.2025): Verteidigungsetat im Haushaltsausschuss](https://www.bundestag.de/presse/hib/kurzmeldungen-1107332)',
 lage='[beck-aktuell (21.08.2025): Bundeslagebild Sexualdelikte gegen Kinder und Jugendliche 2024](https://www.beck-aktuell.de/heute-im-recht/rechtsgeschehen/sexuelle-gewalt-kinder-jugendliche-bundeslagebild-2024-bka-bmi-2025-08-21)',
 mhg='[evangelisch.de (25.09.2018): Zentrale Ergebnisse der MHG-Studie zur sexuellen Gewalt in der katholischen Kirche](https://www.evangelisch.de/inhalte/152463/25-09-2018/zentrale-ergebnisse-der-grossen-studie-zur-sexuellen-gewalt-der-katholischen-kirche)',
 wd='[Wissenschaftliche Dienste des Bundestages, WD 7 - 3000 - 055/21: Einzelfragen zur Strafbarkeit sexueller Gewalt gegen Kinder (18.06.2021, PDF)](https://www.bundestag.de/resource/blob/852858/f1894cd188fba4f08f2246b5d1763907/WD-7-055-21-pdf-data.pdf)',
 parit='[Der Paritätische: Umbenennung per Erlass – BZgA wird zum Bundesinstitut für Öffentliche Gesundheit (BIÖG)](https://www.der-paritaetische.de/alle-meldungen/umbenennung-per-erlass-bzga-wird-zum-bundesinstitut-fuer-oeffentliche-gesundheit-bioeg/)',
 bioeg='[Bundesgesundheitsministerium (13.02.2025): BZgA in Bundesinstitut für Öffentliche Gesundheit (BIÖG) umbenannt](https://www.bundesgesundheitsministerium.de/presse/pressemitteilungen/bzga-in-bundesinstitut-fuer-oeffentliche-gesundheit-bioeg-umbenannt-pm-13-02-25.html)',
 thiel='[The Nation (30.06.2025): Peter Thiel and the billionaires abandoning humanity](https://www.thenation.com/article/society/peter-thiel-billionaires-abandoning-humanity/)',
 columbia='[Axios (24.07.2025): Columbia agrees to pay $200 million fine to settle Trump admin dispute](https://www.axios.com/2025/07/24/columbia-trump-federal-funding-deal)',
)
L = lambda k: Q[k]
def url(k): return Q[k].split('](')[1][:-1]
def tit(k): return Q[k].split('](')[0][1:]

# ---------- Abschnitte (von, bis, Titel, Kurztitel, Thema, Liste) ----------
S = []
def ab(von, bis, titel, kurz, th, *liste):
    S.append((von, bis, titel, kurz, th, list(liste)))

ab('0:00','0:03','🎬 Begrüßung in Kreuzberg und viele Absagen','Begrüßung in Kreuzberg, Absagen anderer Politiker','w',
 '**Zusammenfassung:** Der Gastgeber (Name im Video nicht genannt ❓) begrüßt „Dr. Maximilian Krah“ auf einer, wie beide betonen, „nicht fremdfinanzierten Plattform“. Er erzählt, der Kanal komme aus Kreuzberg, er sei im linken Milieu aufgewachsen und habe viele Politiker eingeladen – etwa Sahra Wagenknecht und Richard David Precht (❓, „Prächt“) –, aber keine Zusagen bekommen. Schon früher habe der Kanal als erste Hip-Hop-Plattform einen AfD-Politiker zu Gast gehabt, in einem Streitgespräch mit Marcus Staiger (❓, „Markus Steiger“).',
 '💬 „Wir müssen Leute überraschen.“ (Krah) [0:01]',
 '📌 Krah: Wenn dieses Gespräch gut laufe, kämen auch die anderen [0:02] [seine Sicht].',
 '🔗 Der Gastgeber kündigt an, er werde anderen niemandem „hinterherrennen“, aber jeden höflich empfangen [0:02–0:03].')
ab('0:03','0:05','📱 Von der „Boomer-Partei“ zur Jugendpartei','AfD als Jugendpartei – TikTok und Europawahl 2024','a',
 '**Zusammenfassung:** Der Gastgeber nennt Krah den „Shootingstar“, der die AfD über TikTok zu jungen Wählern gebracht habe. Krah bestätigt: Mit der Europakampagne 2024 sei die AfD eine Jugendpartei geworden; ein paar ältere Wähler seien dabei verloren gegangen, der Gewinn bei Jungen gleiche das aus. Heidi Reichinnek (Linke, „Reichineck“) dürfe der AfD bei Jungen nicht den Rang ablaufen.',
 '📌 Der Gastgeber stellt sich selbst vor: Wer den Kanal kenne, wisse, dass er „eher der Verschwörungstheoretiker“ sei, der nicht an den Staat glaube; heute nehme er bewusst die klassische Interviewer-Rolle ein [0:04].',
 '🔗 Zu Krahs Rolle 2024 als Spitzenkandidat zur Europawahl siehe Abgleich 📚.')
ab('0:05','0:09','🏷️ „Wie viel Nazi steckt in der AfD?“','Nazi-Vorwurf und die „Wellen“ der AfD','a',
 '**Zusammenfassung:** Auf die „provokanteste Frage“ antwortet Krah: „gar kein“. Der Begriff werde für alles benutzt, was man nicht mag. Jede Partei habe Leute, die man nicht treffen wolle, auch die CDU, in der er früher war. Die AfD sei in Wellen gewachsen: Wirtschaftsprofessoren gegen die Euro-Rettung, dann Kritiker der Grenzöffnung (dazu zähle er sich), dann Corona-Kritiker – alle hätten „recht behalten“. Der Nazi-Vorwurf diene dazu, sich mit Argumenten nicht auseinanderzusetzen.',
 '💬 „komische Leute gibt’s überall, ist eine gaußsche Kurve“ (Krah) [0:07]',
 '📌 Der Gastgeber: Es gebe echte Neonazis; viele davon fänden die AfD „nicht radikal genug“. Krah: Er bekomme derzeit viel Gegenwind von Anhängern der früheren NPD („Heimat“); man ziehe eine Linie – nicht wegen Jugendsünden, sondern weil diese Leute „nichts zu bieten“ hätten [0:07–0:09] [seine Sicht].',
 '📚 Amtliche Einstufung der AfD durch den Verfassungsschutz und die Gerichtsentscheidungen dazu: siehe Abgleich.')
ab('0:09','0:11','🧭 Herrschaft als Leadership','Herrschaft = Menschen zum Wandel bewegen','b',
 '**Zusammenfassung:** Gefragt nach seinem Verständnis von Herrschaft, sagt Krah: Sie sei notwendig, man müsse sagen, „wo es lang geht“. In den USA ausgebildet, übersetze er „Leadership“ mit Herrschaft. Die alte Form „ich sage, du gehorchst“ funktioniere nicht mehr, weil Menschen individuell geworden seien.',
 '💬 „die Fähigkeit, Menschen zum Wandel zu motivieren“ (Krah über Leadership) [0:10]',
 '📌 Ziel: Menschen sollten einsehen, dass ihre heutige Lage nicht trägt, und „mit ihm mitlaufen“ [0:10–0:11] [seine Sicht].')
ab('0:11','0:13','🪑 Hinterbänkler mit Ideen','Einfacher Abgeordneter, Medienecho, Buch','a',
 '**Zusammenfassung:** Nach der Europawahl sei er nicht mehr für den Parteivorstand angetreten und jetzt „einfacher Abgeordneter“; er setze sich absichtlich nach hinten, um sich Neues ausdenken zu können. Sein Buch über die Zukunft sei zwei Monate überfällig. Trotzdem stehe er ständig in der Zeitung – nicht wegen Fehlverhaltens, sondern weil er Ideen habe; FAZ und Welt hätten positiv über eine Diskussion von ihm geschrieben (❓, nicht geprüft).',
 '📌 „Ich bin interessanterweise drin, weil ich [Ideen] habe“ – sinngemäß [0:12] [seine Sicht].',
 '📚 Krah gewann 2025 das Direktmandat im Wahlkreis 162 (44,2 % der Erststimmen); gegen ihn läuft seit Mai 2025 ein Ermittlungsverfahren – siehe Abgleich.')
ab('0:13','0:16','👶 Demografie und KI als Überlebensfrage','Demografie, KI, autonome Busse und Bahn, Golfstaaten','c',
 '**Zusammenfassung:** Erste Idee: Die Demografie treffe Deutschland in fünf bis zehn Jahren „massiv“. Bis Ende des Jahrzehnts bekomme eine Frau im Schnitt nur noch ein Kind; die Gen Z gehe als erste Generation mehrheitlich als Single durchs Leben (❓). Daher sei KI „überlebensnotwendig“. Statt Busfahrer in Kenia anzuwerben (Bezug auf Olaf Scholz ❓) solle man in autonome Busse investieren, statt fehlender Lehrer KI-Privatlehrer nach Art von Duolingo nutzen, und die Bahn solle autonom fahren.',
 '💬 „Die Zukunft findet auch in Dubai statt und nicht in Düsseldorf.“ (Krah) [0:15]',
 '📌 Zweite Idee: Die Welt werde nicht mehr am Nordatlantik entschieden; Friedensgespräche fänden in Katar oder Saudi-Arabien statt, Mohammed bin Salman und Recep Tayyip Erdoğan seien mächtig geworden [0:15] [seine Sicht].',
 '📚 Geburtenziffer 2025 laut Destatis: 1,32 Kinder je Frau (Verlauf im Abgleich).')
ab('0:16','0:18','🤖 Wer steuert die KI?','Schattenseiten: Vance-Rede, Manipulation, KI-Puppen','c',
 '**Zusammenfassung:** Der Gastgeber fragt nach Technokratie und Transhumanismus als „geschaffene Alternative eines geschaffenen Problems“. Krah stimmt zu: JD Vance habe in Paris gesagt, Europa solle bei amerikanischer KI mitmachen und keine chinesische kaufen (❓, nicht geprüft). Wenn alles KI-gesteuert sei, stelle sich die Frage, wer die KI steuert. Als Beispiel schildert er vernetzte KI-Sexpuppen, über deren Updates einsame Männer zum Kauf virtueller Geschenke gebracht werden könnten.',
 '💬 „Wenn alles KI-gesteuert ist, wer steuert die KI?“ (Krah) [0:16]',
 '📌 Am Ende entstehe eine Oligarchie [0:18] [seine Sicht].')
ab('0:18','0:21','💻 Von der Wall Street zu den „Tech Bros“','Macht wandert zur Westküste: Thiel, Bezos','c',
 '**Zusammenfassung:** Vor zehn Jahren habe die Wall Street die US-Politik dominiert, mit Trumps zweiter Amtszeit gehe das auf die „Tech Bros“ über. Interessanter als ein Bank-Chef (Krah nennt Jamie Dimon, „Diamond“, und Morgan Stanley – Dimon leitet JPMorgan Chase 📚) sei Peter Thiel. Jeff Bezos habe „die Vogue gekauft“ (❓, nicht belegt) und sei mit Lauren Sánchez zusammen. Thiel sei im „Posthumanismus“ angekommen; Krah sieht sich als einzigen, der in Deutschland seriös über solche Themen spreche.',
 '📌 Der Klassenbeste träume heute nicht mehr vom Investmentbanker, sondern vom Start-up im Silicon Valley [0:20] [seine Sicht].',
 '🔗 Gastgeber: Zwischen Wall Street und Tech-Industrie sehe er „keine große Trennung“ [0:20].')
ab('0:21','0:24','🕵️ Geheimdienste, Palantir und Thiels Gefahrenliste','Gastgeber: Geheimdienste, Palantir; Thiels drei Gefahren','c',
 '**Zusammenfassung:** Der Gastgeber sagt, Geheimdienste seien immer beteiligt gewesen; BCCI und In-Q-Tel seien durch die CIA gegründete Banken, Palantir komme „daher“ (❓, nicht geprüft). Thiel sei Mentor von JD Vance. Krah fasst Thiel so zusammen: Von drei Gefahren – Kommunistische Partei Chinas, Islam, „woker Linksliberalismus“ – halte Thiel Letzteren für die größte. Krah stimmt zu: Ihn und seine Kinder bedrohten eher Leute, die Kindern einredeten, ihr Geschlecht ändern zu können, als ein ferner Islamgelehrter [seine Sicht].',
 '📌 Gastgeber: Thiel wolle mehr als Geschlechtsumwandlung – das Hochladen des Bewusstseins in eine Cloud [0:23] (Darstellung des Gastgebers ❓).',
 '📚 Belegt ist ein langes Thiel-Interview mit Ross Douthat (New York Times, 26.06.2025) – siehe Abgleich.')
ab('0:24','0:26','✝️ Posthumanismus gegen Leib und Seele','Posthumanismus vs. „Auferstehung des Fleisches“','c',
 '**Zusammenfassung:** Krah: Thiel wolle den Geist vom Körper lösen; das sei ein Fehler, denn jeder Gedanke und jedes Gefühl habe eine messbare körperliche Entsprechung. Über das Glaubensbekenntnis („Auferstehung des Fleisches“) habe er durch Thiel verstanden, dass Körper und Seele zusammengehören. Er höre jedes Thiel-Interview, Thiel habe „unheimlich kluge Gedanken“ und biege dann ab.',
 '💬 „Ich glaube daran, dass Geist und Körper untrennbar sind.“ (Krah) [0:25]',
 '📌 Er wünsche sich eine lebhaftere Debatte; ein „Monopol“ sei zwar schön, die deutsche Debatte aber „boring“ [0:26] [seine Sicht].')
ab('0:26','0:28','❓ Karp und Thiel – und was heißt libertär?','Karp und Thiel; Weidel, Thiel und „libertär“','b',
 '**Zusammenfassung:** Der Gastgeber verweist auf Palantir-Mitgründer Alex Karp („K“), der sich als Neomarxist bezeichne und den Rechtsextremismus in Europa bekämpfen wolle. Krah: Karp habe in Frankfurt promoviert, „über Adorno, glaube ich“ (❓); er wirke in Vorträgen „unheimlich aggressiv“; den Neomarxismus halte er für eine intellektuelle Spielerei. Wie Karp und Thiel zusammenpassen, frage er sich selbst.',
 '📌 Gastgeber: Alice Weidel nenne die AfD „libertär“, Thiel gelte als Libertärer, halte aber freien Wettbewerb „für Loser“ und baue mit dem Staat Palantir [0:27] (Darstellung des Gastgebers ❓).',
 '🔗 Überleitung zu Krahs eigener Position: „Nein, wir sind rechts“ [0:28].')
ab('0:28','0:32','🏛️ „Wille zum Staat“: Preußen und Dubai','Kein Libertärer – Preußen, Dubai, starker schlanker Staat','b',
 '**Zusammenfassung:** Krah lehnt den Begriff „libertär“ ab. Er wolle den Staat aus vielem heraushaben, aber nicht abschaffen: Militär, historische Bibliotheken oder Orchester könne der Markt nicht tragen; der Markt gebe „auch einem Auftragskiller“ einen Preis. Sein Vorbild sei der preußische Staat – klar, stark, mit Richtung, ohne ins tägliche Leben einzugreifen. Dubai sei kein libertäres Projekt, lasse aber viel Freiraum und greife bei Regelverstößen hart durch.',
 '💬 „Preußentum ist der Wille zum Staat.“ (Krah, zitiert eine Definition) [0:31]',
 '📌 Ein Staat, der sich überall einmische, sei schwach, nicht stark [0:31] [seine Sicht].',
 '📌 Auch Thiel sei kein Libertärer, weil er mit dem Staat kooperiere; Elon Musk verdanke sein Geld Regulierung zugunsten von Elektroautos [0:32] [seine Sicht].')
ab('0:32','0:35','💳 Digitales Geld, digitale ID, Gesichtserkennung','Digitales Geld, Krypto, digitale ID, Kameras','b',
 '**Zusammenfassung:** Der Gastgeber: Staatliches (CBDC) und privates Digitalgeld seien dasselbe; „Public Private Partnership“ nennten manche Faschismus. Krah: Es werde nicht besser, wenn ein Großkonzern unterdrücke; er sei für mehr Freiheit für Kryptowährungen, um dem Staat zu zeigen, dass es anders geht. Die Twitter-Sperre gegen Trump sei nicht besser gewesen, weil ein Privater sie verhängte. Digitales Geld und digitale ID hätten Vor- und Nachteile; verhindern lasse sich das kaum.',
 '📌 Beispiel: In der Kiewer Metro sei er bestohlen worden; in Singapur hätte Gesichtserkennung den Täter am selben Tag ermittelt; so ließe sich auch der Görlitzer Park („Girly“) in den Griff bekommen [0:34–0:35] [seine Sicht].',
 '📌 Zugleich: Der Staat sammle „endlos Daten“ und mache uns dadurch verwundbar [0:35].')
ab('0:35','0:40','🩺 Patientenakte, Landarzt und der Preis des Fortschritts','E-Patientenakte, Landarzt der Zukunft – Gegenrede','c',
 '**Zusammenfassung:** Die elektronische Patientenakte werde kommen, weil sonst die Versorgung auf dem Land nicht zu halten sei. Krah schildert, wie ein Arztbesuch künftig aussehen könnte: automatische Blutabnahme, Analyse vor Ort, Computer mit gesamter Krankenakte schlägt Diagnose vor – in zehn Minuten. Der Preis sei eine „Datenkrake“. Er führe keine Entweder-oder-Debatte, sondern frage, ob sich „der Preis drücken“ lasse.',
 '📌 Gastgeber: Ein empathischer Hausarzt sei besser, wenn die Welt nicht von Pharmaindustrie und Ärzteschaft „korrupt“ wäre; sein Bruder sei Arzt; die breite Masse bekomme Termine erst nach Wochen [0:38–0:39] (seine Sicht).',
 '📌 Krah: Die Wahl bestehe nicht zwischen perfekter Welt und Digitalisierung, sondern zwischen einer absehbar schlechter werdenden Lage und der digitalen Lösung; dass keine Kinder mehr geboren würden, „liegt auch an uns selbst“ [0:39–0:40] [seine Sicht].',
 '📚 Medizinische Aussagen hier nur als Zukunftsbild im Gespräch, keine Empfehlung.')
ab('0:40','0:43','🎩 Politikerqualität und die Grenzen des Möglichen','Politikerqualität, „geschaffene Probleme“, Grenzen der Politik','b',
 '**Zusammenfassung:** Der Gastgeber vergleicht Bundestagsdebatten der 80er mit heute und fragt, ob Vertrauen in die Politik „mit Absicht zerstört“ werde, um ein neues System einzuführen – ein Gedanke aus „Schwurblerkreisen“, wie er selbst sagt. Krah: Wähler wählten heute keine älteren Herren im Dreiteiler mehr; unter jungen, gebildeten Frauen habe Reichinnek mehr Zustimmung als er. Das sei nicht die Schuld „geheimnisvoller Mächte“.',
 '💬 „Ich kann zwar das Gesetz ändern, aber ich kann ja nicht ändern …“ (Krah) [0:42]',
 '📌 Deutschland habe verlernt, zwischen dem Wünschenswerten und dem Möglichen zu unterscheiden; vielen Kindern sei erzählt worden, alles sei machbar [0:42–0:43] [seine Sicht].')
ab('0:43','0:47','🗂️ Neoliberal? Sozialstaat und Beamte','Sozialstaat 30 %, Beamtenstellen, KI-Bescheide, Behörden abschaffen','d',
 '**Zusammenfassung:** Zum Vorwurf, die AfD sei neoliberal: Neoliberalismus stamme aus der Zeit von Thatcher und Reagan und bedeute Rückbau des Sozialstaats. Eine liberale Partei sei die AfD nicht, aber der „extrem ausgedehnte Sozialstaat“ schaffe die Probleme, die er beheben wolle: Rund 30 % der Wirtschaftsleistung flössen hinein, trotzdem würden mehr Menschen arm; profitieren würden „Sozialindustrie und Sozialbürokratie“.',
 '📌 Vorschläge: nur jede zweite Beamtenstelle nach Pensionierung neu besetzen; Routinen durch Computer ersetzen; ein Drittel der Beamtenstellen sei schon heute ersetzbar, absehbar die Hälfte; Umweltbundesamt und Teile der Arbeitsverwaltung könne man abschaffen [0:44–0:47] [seine Sicht].',
 '📌 Beispiel: Ein Sachbearbeiter einer Krankenkasse habe ihm erzählt, bald schrieben Computer Bescheide, Widersprüche und Urteile „gegenseitig“ [0:44–0:45].',
 '📌 In der „Ampelzeit“ seien 100.000 neue Stellen im öffentlichen Dienst entstanden [0:47].',
 '📚 Sozialschutzausgaben 2024 laut Eurostat: 30,9 % des BIP; öffentlicher Dienst 2024: +95.900 Beschäftigte (Destatis) – siehe Abgleich.')
ab('0:47','0:50','👷 Talent falsch eingesetzt, Deindustrialisierung','Fachkräfte, Handwerk, Deindustrialisierung „gewollt“?','d',
 '**Zusammenfassung:** Jobverluste seien kein Problem, weil es immer weniger Menschen gebe; Mangel herrsche in Handwerk, Gastronomie, Pflege und Gesundheit, während der öffentliche Dienst wachse. Talent werde falsch eingesetzt, etwa in Genderwissenschaften; Handwerksbetriebe fänden keine Nachfolger.',
 '📌 Gastgeber: Deutschland sei an einem Punkt der „Deindustrialisierung“, die „gewollt“ sei; Krah stimmt zu („Ein Großteil ist politisch gewollt“), die EU spiele eine „unrühmliche Rolle“ [0:48–0:49] [seine Sicht].',
 '🔗 Gastgeber fragt, ob Deutschland bei KI überhaupt mithalten könne oder nur „guter Kunde“ sein solle [0:49].')
ab('0:50','0:53','🛡️ Rüstung als schlechteste Konjunkturpolitik','Rüstung ökonomisch schwach; europäische Tech-Kooperation','d',
 '**Zusammenfassung:** Rüstung sei unter allen Wegen, Wachstum mit Staatsgeld zu erzeugen, „die schlechteste“: Eine Baumaschine arbeite ihr ganzes Leben, ein Panzer stehe im Depot. Für die Tech-Industrie seien alle europäischen Länder zu klein; er sei Gegner der EU, aber für eine neue, rein wirtschaftliche Kooperation.',
 '📌 Die US-Regierung (Trump, Vance) habe eine Sympathie für Deutschland; Deutschland könne in Europa eine Vorreiterrolle übernehmen und andere einladen – die alte „Reichsidee“ (Krah räumt ein: „klingt furchtbar altbacken“) [0:51–0:52] [seine Sicht].',
 '📌 Europa sei „ein Raum von über 200 Millionen Menschen“ [0:52] (❓; Zahl nicht geprüft).',
 '💬 „mehr Mut zur Technik, mehr Mut zur Zukunft“ (Krah) [0:53]')
ab('0:53','0:57','💶 Das 5-%-Ziel und das US-Handelsdefizit','5-%-Ziel, Bundeshaushalt, Handelsdefizit, Zölle','d',
 '**Zusammenfassung:** Der Gastgeber erinnert an die Weimarer Zeit: Militarisierung habe wirtschaftlich geholfen, aber man habe „den Sprint gewonnen und den Marathon tödlich verloren“. Krah: Beim 5-%-Ziel würden 40 % des Bundeshaushalts in Rüstung fließen, dazu rund 30 % für die Rentenkasse – das sei „nicht finanzierbar“. Trump nenne 5 %, um sich auf 3 % zu einigen; „wir sind jetzt bei zwei“.',
 '📌 Ziel der USA sei, ihr Handelsdefizit durch Rüstungsverkäufe auszugleichen; über Zölle wolle Trump den Staat finanzieren und Steuern senken [0:55–0:56] [seine Sicht].',
 '📌 Krah kritisiert Bundeskanzler Friedrich Merz („März“) scharf: Er habe die Forderung sofort angenommen; am Ende stünden Überschuldung und volle Depots [0:55–0:56] [seine Sicht].',
 '📚 NATO-Beschluss Den Haag (Juni 2025): 3,5 % Kernverteidigung + 1,5 % verteidigungsrelevante Ausgaben bis 2035 – siehe Abgleich.')
ab('0:57','1:01','🪖 Kriegsangst, Wehrdienst, Wilson und die Lusitania','Medizintechnik statt Rüstung; Kriegsangst; Wehrdienst','e',
 '**Zusammenfassung:** Potenzial sieht Krah in Medizintechnik und Robotik („Mechanik können die Deutschen“). Der Gastgeber befürchtet, die Aufrüstung bereite einen Krieg vor; für die USA sei Krieg „Geschäftsmodell“, Mainstream-Artikel schrieben, die Wall Street hänge am Drogenhandel (❓); Woodrow Wilson sei als Friedenspräsident gewählt worden, dann kam die Lusitania. Krah: Kriege brauche Soldaten, die bereit sind zu sterben – Familien mit einem Kind schickten ihre Söhne nicht an die Front.',
 '💬 „Du stirbst nicht für eine Regenbogenfahne.“ (Krah) [0:58]',
 '📌 Krah sagt, er habe als einer der wenigen Politiker Wehrdienst geleistet. Er nennt mehrere CDU-Politiker, die nicht bei der Bundeswehr gewesen seien und jetzt die Wehrpflicht wollten [0:59–1:00] (Aussage des Sprechers; nicht geprüft ❓).',
 '📌 Die US-Forderung nach 5 % sei „industriepolitisch motiviert“, nicht auf einen großen Krieg gerichtet; Rüstung zu begrenzen sei immer gut [1:00] [seine Sicht].')
ab('1:01','1:05','🧭 Souveränität als Stufenleiter','Souveränität: Schröder, Merkel, Scholz, Merz, Türkei','e',
 '**Zusammenfassung:** Souveränität gebe es nicht als Ja/Nein; voll souverän seien höchstens USA, China und – mit Mühe – Russland, der Rest sei eine Abstufung. Unter Gerhard Schröder sei Deutschland souveräner gewesen: Er habe beim Kosovokrieg mitgemacht, deshalb beim Irakkrieg Nein sagen und Nord Stream bauen können. Merkel habe das „schleifen lassen“, Scholz sei „in den Keller“ gefahren, Merz bleibe gern dort. Gegenbeispiel sei die Türkei unter Erdoğan.',
 '📌 Deutschland werde nie Supermacht – „das haben wir versucht im Ersten Weltkrieg 1914“ –, solle aber seinen Spielraum nutzen: „sei nicht Merkel, sei nicht Scholz und sei nicht Merz“ [1:03–1:04] [seine Sicht].',
 '📌 Auf die Frage, ob Deutschland ein „Vasallenstaat“ sei: Unter Schröder nicht, heute sei die Lage „beschämend“ [1:04].')
ab('1:05','1:07','🤝 Diplomatie aus Brüsseler Sicht','Diplomatie ohne Belehrung – Delegationen in Brüssel','e',
 '**Zusammenfassung:** Diplomatie sei „kein Wünsch-dir-was“; man müsse auch mit Saudi-Arabien reden, ohne zu belehren, und in Katar keine „sinnlose Regenbogenbinde“ tragen (Bezug auf Nancy Faeser, WM 2022). In seinem Brüsseler Büro habe er ausländischen Delegationen gesagt, er sei nicht gewählt, um ihr Land zu regieren, und nach ihren echten Interessen gefragt.',
 "💬 „I'm not in the business to run your country.“ (Krah) [1:06]",
 '📌 So habe er erfahren, dass Ägypten wegen der Russland-Sanktionen keinen Dünger mehr bekomme und die Lebensmittelpreise stiegen [1:06] (Aussage des Sprechers ❓).')
ab('1:07','1:10','🇹🇷 Türkische Wähler und die Geburtenrate','Türkeistämmige AfD-Wähler, Duisburg-Marxloh, Geburtenrate Türkei','f',
 '**Zusammenfassung:** Der Gastgeber bezieht sich auf ein Gespräch Krahs bei „Meet Your Mentor“ (Gastgeber „Simo“ ❓) über türkische AfD-Wähler. Krah: Im Wahlkreis „Duisburg Nord“ mit Marxloh sei die AfD bei den Zweitstimmen stärkste Kraft – das gehe „ohne die türkischen Stimmen nicht“. Er wünsche sich bei der nächsten NRW-Landtagswahl mehrere Ruhrgebietswahlkreise für die AfD, um der SPD ihre „Herzkammer“ zu nehmen.',
 '📌 Konservative Einwanderer wünschten meist weitere Einwanderung; das gelte für Türken nicht mehr, weil die Türkei mit rund 1,4 Kindern je Frau schrumpfe; neu ankommende Syrer konkurrierten mit ihnen um Wohnungen [1:08–1:09] [seine Sicht].',
 '📌 Die Türkei werde außenpolitisch wichtiger – „Anker der Stabilität“, das sage inzwischen auch Merz [1:09].',
 '📚 Wahlkreis 115 Duisburg II (2025): SPD 25,3 %, AfD 24,8 % der Zweitstimmen; Türkei 2024: 1,48 Kinder je Frau (Eurostat) – siehe Abgleich.')
ab('1:10','1:13','🧩 Einwanderergruppen unterscheiden','Gruppen unterscheiden: Japaner, Afghanen; Krieg und Trauma','f',
 '**Zusammenfassung:** Gemeinsame Gegner verbänden: Kritik an Einwanderung, an „woken“ Schulen, am wirtschaftlichen Niedergang. Mit Spätaussiedlern und Einwanderern vom Balkan sei die Annäherung gelungen. Man müsse genau schauen, wer kommt: Japaner in Düsseldorf fielen nicht auf, Afghanen seien bei Sexualstraftaten „grob überrepräsentiert“ (Behauptung des Sprechers; nicht geprüft ❓).',
 '📌 Gastgeber: Aus Kriegsgebieten komme oft die Unterschicht; vor den 70ern sei Afghanistan ein anderes Land gewesen. Krah: Es gehe um einen Ehrbegriff und um Radikalisierung durch Jahrzehnte Krieg; Afghanen, die vor 1980 kamen, seien „in der Regel ganz liebe Menschen“ [1:11–1:12] [seine Sicht].',
 '💬 „Ich will es einfach nicht haben.“ (Krah, zur Aufnahme traumatisierter Menschen) [1:12]')
ab('1:13','1:17','💣 Afghanistan der 80er und die MAGA-Erzählung','Afghanistan der 80er, Carlson–Ronzheimer, Informationen auf Englisch','e',
 '**Zusammenfassung:** Der Gastgeber: Migration werde als Waffe genutzt; Kriegsherde und islamistische Gruppen gingen oft auf US- und britische Geheimdienste zurück. Krah stimmt zu: Der Kern sei der Afghanistankrieg der 80er, als man gegen die Sowjetunion einen „Dschihad-Spielplatz“ aufgebaut habe. Das sei Teil der MAGA-Erzählung und „keine Verschwörungstheorie“.',
 '📌 Paul Ronzheimer (Bild) sei bei Tucker Carlson gewesen; Carlson habe ihm gesagt, Deutschlands Lage liege an Merz und Merkel, nicht an Putin [1:15–1:16] (Wiedergabe durch Krah ❓).',
 '📌 Wer kein Englisch könne, habe es schwer, sich zu informieren, weil hier „alles unglaublich gefiltert“ sei [1:16] [seine Sicht].')
ab('1:17','1:22','👗 Trump und der Kulturwandel','Kulturwandel: Nike, Leavitt, Vogue, Columbia und Harvard','e',
 '**Zusammenfassung:** Trump führe zu einem kulturellen Wandel: Nike-Werbung 2023 („Mann im BH“) gegenüber 2025 (Golfer mit Sohn), Mode, Pressesprecherin Karoline Leavitt. Der Gastgeber hält dagegen: ESG und DEI seien schon vor Trump von Leuten wie Larry Fink für beendet erklärt worden. Krah: Man brauche eine Galionsfigur – „das Kind, das ruft: der Kaiser ist nackt“; Beispiel sei Trumps Antwort „Only Rosie O’Donnell“ in der TV-Debatte 2015.',
 '📌 Trump 2 erreiche, dass auch Eliten mitmachten: Bezos habe dafür gesorgt, dass die Washington Post keine Wahlempfehlung für Biden abgab (❓, nicht geprüft); Columbia – Krahs „Alma Mater“ – verhandle nach gestrichenen Bundesmitteln über ein Ende ihrer DEI-Programme, Harvard weigere sich [1:21–1:22] [seine Sicht].',
 '💬 „bin ich immer noch ein großer Trump-Fan“ (Krah) [1:22]',
 '📚 Columbia einigte sich am 23.07.2025 mit der US-Regierung – siehe Abgleich.')
ab('1:22','1:26','🏢 Widerspruch: Machen die Eliten Trump?','Gastgeber widerspricht: Eliten bestimmen Trump – Einigung','e',
 '**Zusammenfassung:** Der Gastgeber widerspricht „respektvoll“: Nicht Trump ändere die Eliten, die Eliten sagten Trump, was er zu sagen habe; sie kennten kein links oder rechts. Krah: Innerhalb der Eliten gebe es eine Spannbreite; wer heimlich „vom Woken träumt“, schweige jetzt, andere machten mit. Beide einigen sich auf eine „Verschiebung“ innerhalb der Milliardärsklasse.',
 '📌 Bezos sei ein Beispiel; zu Vance gehöre „Peter Thiel im Paket“ [1:24] [seine Sicht].',
 '💬 „Wer einfach sagt, Nazi, der will nicht denken“ (Krah) [1:24]',
 '📌 Gastgeber: Elon Musk sei ein „Blatt im Wind“, ein Opportunist [1:25].')
ab('1:26','1:30','🧒 Pubertät, Identität und Schutzalter','Pubertät, Geschlechtsidentität, Frühsexualisierung, Schutzalter','g',
 '**Zusammenfassung:** Der Gastgeber knüpft an ein früheres Gespräch an, in dem Krah Pädophilie erwähnt habe, und fragt nach dem Umgang damit; Geschlechtsumwandlungen bei Kindern lehne auch er ab. Krah: Immer mehr Teenager täten sich schwer, ihre Geschlechtsidentität zu finden – wegen fehlender Vorbilder, Trennungen der Eltern, Mobbing; statt zuzuhören, bestärke sie eine „Industrie“, an der auch die Pharmaindustrie verdiene [seine Sicht].',
 '📌 Er kritisiert Auftritte externer Gruppen (Drag-Queens, „Sex-NGOs“) in Kitas und Grundschulen und unterstellt dabei Motive; Belege nennt er nicht [1:28] (❓).',
 '📌 Deutschland habe ein „extrem geringes Schutzalter“: Ab 14 sei man „aus dem strafrechtlichen Schutz raus“; Grundschulen sollten „sexfrei“ sein [1:28–1:29] [seine Sicht].',
 '📚 Rechtslage (§ 176, § 182, § 174 StGB) laut Wissenschaftlichem Dienst des Bundestages: siehe Abgleich.')
ab('1:30','1:34','🏫 Sexualkunde, BZgA und Zugang zu Pornografie','Kein externer Sexualkundeunterricht, BZgA, Altersnachweis','g',
 '**Zusammenfassung:** Der Gastgeber fasst zusammen: Frühsexualisierung öffne der Pädophilie „Tür und Tor“. Krah: Organisierte Ringe wie im Epstein-Fall in Deutschland könne er nicht beurteilen. Seine Stellschrauben: kein externer Sexualkundeunterricht an Grundschulen, Themen vorher am Elternabend, nicht vor der dritten oder vierten Klasse; die Bundeszentrale für gesundheitliche Aufklärung „gehört erstmal abgeschafft“; Altersnachweis für Pornografie.',
 '📌 Eines seiner erfolgreichsten Videos habe jungen Männern geraten, keine Pornos zu schauen und nicht Grün zu wählen [1:32].',
 '📌 Normale, einvernehmliche Sexualität habe mit Pornografie nichts zu tun; die Generation habe „eine völlig falsche Vorstellung“ [1:33] [seine Sicht].',
 '📚 Die BZgA heißt seit 13.02.2025 Bundesinstitut für Öffentliche Gesundheit (BIÖG) – siehe Abgleich.')
ab('1:34','1:37','💍 Treue als Stärke – und Krahs Familienleben','Treue als Stärke; Krahs eigenes Familienleben','g',
 '**Zusammenfassung:** Man solle für einvernehmliche Sexualität werben, im Unterricht auf Verbundenheit setzen und den Mut haben, Treue zu empfehlen. Der Gastgeber fragt nach Krahs Privatleben („acht Kinder von verschiedenen Frauen“). Krah: Er sei verwitwet, habe Fehler gemacht, sich mit seiner Partnerin versöhnt; das sei gut für seine zwei kleinen Kinder gewesen.',
 '💬 „Treue ist ein Zeichen von Stärke.“ (Krah) [1:34]',
 '📌 Als öffentliche Person sei auch sein Lebenswandel Gegenstand politischer Kritik – „von mir aus meine 5 kg Übergewicht“ [1:37].')
ab('1:37','1:42','⚖️ Sexualstrafrecht und Missbrauch in der Kirche','Sexualstrafrecht, „Überfallvergewaltigung“, Kirche','g',
 '**Zusammenfassung:** Der Gastgeber nennt „glaube ich 60 Missbrauchsfälle pro Tag“ und fragt nach Gesetzen und nach Missbrauch in der katholischen Kirche. Krah: Das Sexualstrafrecht sei „viel zu lasch“; zugleich müsse man auf Falschbeschuldigungen achten, die Gerichte seien aber „treffsicher“. Besonders verhängnisvoll seien Überfälle durch Fremde; 2015 habe ihm ein Dresdner Vorsitzender Richter gesagt, solche Fälle habe er nie gehabt – zwei Wochen später gab es den ersten (Anekdote des Sprechers ❓).',
 '📌 Kirche: Es habe ein „Schweigekartell“ gegeben – Eltern glaubten Kindern nicht, Bistümer deckten Täter und versetzten sie; heute sei das Problem nach seinem Eindruck „im Griff“ [1:40–1:42] [seine Sicht].',
 '📚 MHG-Studie 2018: 1.670 beschuldigte Kleriker, 3.677 Betroffene (1946–2014); Lagebild 2024: 16.354 Fälle – siehe Abgleich.')
ab('1:42','1:46','🛑 Zuhören, Strafmaß und Rückfallschutz','Kindern zuhören; Strafmaß; Rückfallschutz','g',
 '**Zusammenfassung:** Wichtig sei, Kindern zuzuhören, Andeutungen ernst zu nehmen und „Ärger zu wollen“. Beim Strafrahmen gebe es Schutzlücken, weil das Gesetz nach Alter und nicht nach Reife gehe. Bei wiederholtem Missbrauch eines Kindes nennt Krah „auf keinen Fall unter fünf Jahre“; bei Wiederholungstätern sollte man über medikamentöse Mittel nachdenken, wie in einigen US-Bundesstaaten (❓, nicht geprüft).',
 '📌 Gastgeber: Jede Tat an einem Kind solle automatisch die Höchststrafe bekommen; Krah stimmt zu, besonders bei Körperverletzung mit Todesfolge [1:45–1:46] [seine Sicht].',
 '📚 Gesundheit: Hier werden nur Positionen wiedergegeben; zur Behandlung äußern sich Fachstellen, die hier nicht geprüft wurden ❓.')
ab('1:46','1:50','➡️ Was heißt rechts?','Rechts als Begriff: „leben als das, was ich bin“','a',
 '**Zusammenfassung:** Krah habe sich früher „konservativ“ genannt – ein „Schnarchbegriff“, den auch Armin Laschet beanspruche. „Rechts“ habe er gewählt, weil ihn sonst niemand offen beanspruche; dann könne er bestimmen, was es heißt. Rechts bedeute: leben als das, was man objektiv ist – Kind seiner Eltern, Mann, Deutscher – und daraus die Umgebung gestalten.',
 '💬 „Ich will leben als das, was ich bin.“ (Krah) [1:48]',
 '📌 Seine Bücher: „Politik von rechts“, ein zweites („Die Zukunft wird rechts“ ❓) und geplant „rechtes Regieren“ – mit dem Wortspiel rechts/richtig [1:49] [seine Sicht].',
 '📌 Die heutigen Linken seien „nicht mehr das, was sie wirklich sind“; viele klassisch ausgebildete Marxisten in Ostberlin stünden der AfD nahe [1:50] [seine Sicht].')
ab('1:50','1:55','📚 Dekonstruktivismus, Foucault und Objektivität','Linke heute: Dekonstruktivismus, Foucault, Objektivität','a',
 '**Zusammenfassung:** Links sei heute der Dekonstruktivismus: alles nur Diskurs, richtig und falsch Ergebnis von Machtstrukturen (Michel Foucault). Krah erhebt dazu einen persönlichen Vorwurf gegen Foucault (❓, nicht geprüft) und setzt dagegen „objektive Maßstäbe“: Mann und Frau, das Verbot von Kindesmissbrauch, Tag und Nacht.',
 '📌 Gastgeber: Auch „ich möchte sein, was ich bin“ könne eine linksliberale Position sein; Krah: Er glaube an Objektivität – wer gegen sein objektives Selbst lebe, werde unglücklich [1:53–1:54] [seine Sicht].',
 '📌 Ein slowakischer Parlamentskollege habe sich mit Rohmilch und Biofleisch neu erfunden und sei ein erfolgreicher Jugend-Influencer geworden [1:55] (❓).')
ab('1:55','1:58','🎙️ Einspieler: Rudi Dutschke','Einspieler Rudi Dutschke: Arbeitszeit, Parteien','b',
 '**Zusammenfassung:** Der Gastgeber spielt einen Ausschnitt mit Rudi Dutschke vor, nach eigener Angabe kurz vor 1970 aufgenommen (im Ausschnitt fällt das Jahr 1967). Dutschke kritisiert, die Arbeitszeit sei trotz Produktivitätsfortschritt kaum gesunken, um Herrschaft zu sichern; Regierungen seien „institutionalisierte Lügeninstrumente“, Parteien dienten nur der Selbsterhaltung eines Apparats.',
 '💬 „Dem Volk wird nicht die Wahrheit gesagt.“ (Dutschke im Einspieler) [1:56]',
 '🔗 Gastgeber fragt Krah, ob es ihn „gruselt“, Dutschke zu hören [1:58].')
ab('1:58','2:04','🇩🇪 Krah über Dutschke – und „Was ist ein Deutscher?“','Krah über Dutschke und Wagenknecht; „Was ist ein Deutscher?“; Abschied','a',
 '**Zusammenfassung:** Krah: Marxisten analysierten meist richtig, aber unvollständig – es fehle der spirituelle Punkt; die Kritik an Parteien als Machterhaltsapparaten treffe auf alle zu, auch die inzwischen „ziemlich alt“ gewordene AfD. Wagenknecht sei „immer lesenswert“. Dutschke habe keine Lösung gehabt; im Streitgespräch habe Ralf Dahrendorf ihm Defizite gezeigt. Er selbst sei in der DDR geboren und wolle keine marxistische Lösung. Der Gastgeber hält Dutschke für eine der wichtigsten Figuren der letzten hundert Jahre.',
 '📌 Letzte Frage (angelehnt an Matt Walshs „What is a Woman?“): Deutscher sei, wer aus Sprache, Kultur, Landschaft, Liedern, Architektur und Geschichte „Inspiration und Kraft“ ziehe – oft mit Vorfahren hier, aber auch Hinzugekommene, deren Kinder „reinwachsen“ [2:02–2:03] [seine Sicht].',
 '💬 „Wird ein bisschen Deutscher.“ (Krah) [2:03]')

# ---------- Themen ----------
THEMEN = [{"k":"a","n":"AfD, Person & „rechts“"},{"k":"b","n":"Staat, Herrschaft & Freiheit"},{"k":"c","n":"Demografie, KI & Tech-Elite"},
 {"k":"d","n":"Sozialstaat, Beamte & Rüstung"},{"k":"e","n":"Außenpolitik, USA & Kulturwandel"},{"k":"f","n":"Migration & Wählergruppen"},
 {"k":"g","n":"Jugend, Sexualität & Kinderschutz"},{"k":"w","n":"Begrüßung/Organisatorisches"}]

# ---------- Abgleich ----------
AB = [
 ['Die AfD sei keine Nazi-Partei; der Vorwurf diene dazu, sich nicht mit Argumenten auseinanderzusetzen [0:05–0:09]',
  'Das Bundesamt für Verfassungsschutz stufte die AfD am 02.05.2025 als „gesichert rechtsextremistisch“ ein (Gutachten über 1.000 Seiten); am 08.05.2025 gab es gegenüber dem VG Köln eine Stillhaltezusage und behandelte die Partei bis zur Gerichtsentscheidung weiter als Verdachtsfall. Die Einstufung als Verdachtsfall hatten VG Köln (2022) und OVG Münster (2024, nicht rechtskräftig) bestätigt. Im Februar 2026 gab das VG Köln einem Eilantrag der AfD „im Wesentlichen“ statt: Die Einstufung darf bis zum Hauptsacheverfahren nicht verwendet werden. Das Gericht sah zugleich „hinreichende Gewissheit“, dass innerhalb der AfD verfassungsfeindliche Bestrebungen entfaltet werden, und einzelne Programmforderungen als verfassungswidrig, aber keine das Gesamtbild prägende Grundtendenz. Nicht rechtskräftig.',
  L('zdf')+' · '+L('srf')],
 ['Nach der Europawahl 2024 sei er nicht mehr für den Parteivorstand angetreten; heute „einfacher Abgeordneter“ [0:11]',
  'Krah war Spitzenkandidat der AfD zur Europawahl 2024. Nach seinen Äußerungen zur Waffen-SS in einem Interview mit La Repubblica (Mai 2024) schloss die Fraktion Identität und Demokratie die AfD am 23.05.2024 aus. Er war MdEP vom 02.07.2019 bis 24.03.2025 und ist seit 25.03.2025 Mitglied des Bundestages.',
  L('wiki')],
 ['Er stehe ständig in der Zeitung, „weil ich Ideen habe“ [0:12]',
  'Die Generalstaatsanwaltschaft Dresden leitete im Mai 2025 ein Ermittlungsverfahren gegen Krah wegen des Verdachts der Bestechlichkeit und Geldwäsche im Zusammenhang mit Zahlungen aus China (Zeit als Europaabgeordneter) ein. Der Bundestag hob am 11.09.2025 seine Immunität auf; Büro- und Wohnräume in Berlin, Dresden und Brüssel wurden durchsucht. Krah weist die Vorwürfe zurück. Stand der Quelle (11.09.2025): keine Anklage, die Behörde prüft Anklage oder Einstellung; späterer Stand nicht geprüft ❓. Es gilt die Unschuldsvermutung. Sein früherer Mitarbeiter Jian G. wurde am 30.09.2025 vom OLG Dresden wegen geheimdienstlicher Agententätigkeit für China (2019–2024, Tätigkeit im Büro Krahs im EP) zu 4 Jahren 9 Monaten verurteilt; Jian G. bestreitet die Vorwürfe, Rechtskraft laut Bericht offen ❓. Krah war Zeuge, nicht Angeklagter, und gab an, von der Agententätigkeit nichts gewusst zu haben. (Das Gespräch wurde vermutlich vor der Immunitätsaufhebung aufgenommen.)',
  L('lto')+' · '+L('beckjg')],
 ['Krah sitzt als gewählter Abgeordneter im Bundestag [0:11]',
  'Bundestagswahl 2025, Wahlkreis 162 Chemnitzer Umland – Erzgebirgskreis II: Krah gewann das Direktmandat mit 44,2 % der Erststimmen; die AfD erhielt dort 41,1 % der Zweitstimmen.',
  L('wk162')],
 ['Bis Ende des Jahrzehnts bekomme eine Frau im Schnitt nur noch ein Kind; man halbiere sich in einer Generation [0:13]',
  'Die zusammengefasste Geburtenziffer lag 2025 bei 1,32 Kindern je Frau (2,7 % weniger als 2024); 654.241 Geburten waren der niedrigste Stand seit der Nachkriegszeit. Der Tiefstwert Mitte der 1990er lag bei 1,24. Eurostat: 1,60 (2016) und 1,58 (2021) als jüngere Höchstwerte, 1,36 (2024). Eine Vorausberechnung „1,0 bis 2030“ wurde nicht geprüft ❓.',
  L('destgeb')+' · '+L('eufert')],
 ['Thiel halte woken Linksliberalismus für gefährlicher als KP China und Islam; er wolle den Menschen in einer digitalen Existenz auflösen [0:21–0:25]',
  'Belegt ist ein langes Interview mit Ross Douthat in der New York Times (26.06.2025). Auf die Frage, ob die Menschheit fortbestehen solle, zögerte Thiel lange und sagte dann „Yes“; er hofft, dass Technik den Tod überwindet. Greta Thunberg nannte er im Zusammenhang mit dem „Antichrist“. Die im Gespräch zugeschriebene Rangfolge der drei Gefahren und eine Aussage zu Geschlechtsumwandlungen sind in der geprüften Quelle nicht enthalten ❓.',
  L('thiel')],
 ['Der Sozialstaat koste „ungefähr 30 %“ der Wirtschaftsleistung [0:43]',
  'Eurostat (ESSPROS): Ausgaben für Sozialschutz in Deutschland 2024: 30,87 % des BIP (2013: 28,77 %; Höchstwert 2020: 32,26 %). Die Angabe im Gespräch trifft die Größenordnung. Zur Aussage, „immer mehr Leute“ würden arm, wurde keine Quelle geprüft ❓.',
  L('eusoz')],
 ['Die Zahl der Beamten steige; in der „Ampelzeit“ seien 100.000 neue Stellen geschaffen worden [0:46–0:47]',
  'Am 30.06.2024 arbeiteten rund 5,4 Mio. Menschen im öffentlichen Dienst, 95.900 (+1,8 %) mehr als ein Jahr zuvor; knapp 12 % aller Erwerbstätigen. Zuwächse vor allem an Schulen (+19.500, davon +16.300 Beamte), Hochschulen (+14.200) und kommunalen Kitas (+11.000). Eine Zahl für die gesamte Ampel-Zeit (2021–2025) wurde nicht geprüft ❓.',
  L('destod')],
 ['5-%-Ziel: 40 % des Bundeshaushalts für Rüstung; „wir sind jetzt bei zwei“ [0:54–0:55]',
  'Die NATO beschloss in Den Haag (24./25.06.2025): 3,5 % des BIP für Kernverteidigung und 1,5 % für verteidigungsrelevante Ausgaben (Infrastruktur, Industrie, Resilienz), zusammen 5 % bis 2035. Für Deutschland schätzte die NATO 2024 einen Anteil von 2,00 % des BIP. Verteidigungsausgaben 2025 laut Haushaltsausschuss: 86,37 Mrd. € (Einzelplan 14: 62,31 Mrd. €, Sondervermögen 24,06 Mrd. €). Verteidigungsausgaben über 1 % des BIP sind von der Schuldenbremse ausgenommen. Ein Anteil am Bundeshaushalt bei 5 % wurde nicht geprüft ❓.',
  L('bmvg')+' · '+L('nato')+' · '+L('hib')],
 ['Rüstungsgüter stünden „im Depot“; Deutschland rüste stark auf [0:50–0:56]',
  'NATO-Zahlen für Deutschland (laufende Preise): 34,7 Mrd. € (2014), 51,4 Mrd. € (2020), 67,6 Mrd. € (2023), 86,6 Mrd. € (2024, Schätzung). Der Anteil am BIP stieg von 1,16 % (2014) auf 2,00 % (2024, Schätzung); NATO gesamt 2,61 % (2024).',
  L('nato')],
 ['Im Wahlkreis „Duisburg Nord“ mit Marxloh sei die AfD bei den Zweitstimmen stärkste Kraft; das gehe nicht ohne türkische Stimmen [1:07]',
  'Wahlkreis 115 Duisburg II (umfasst den Duisburger Norden) bei der Bundestagswahl 2025: SPD 25,3 %, AfD 24,8 % (2021: 12,2 %), CDU 19,4 %, Linke 11,1 %; Direktmandat Mahmut Özdemir (SPD); Wahlbeteiligung 73,4 %. Im gesamten Wahlkreis lag die AfD damit knapp hinter der SPD; Ergebnisse einzelner Stadtteile wurden nicht geprüft ❓. Wie türkeistämmige Wähler abgestimmt haben, erfasst die amtliche Statistik nicht ❓.',
  L('wk115')],
 ['Die Türkei liege bei 1,4 Kindern je Frau und schrumpfe [1:08]',
  'Eurostat: zusammengefasste Geburtenziffer der Türkei 1,48 (2024), 1,51 (2023), 1,63 (2022); 2007 noch 2,13. Deutschland 2024: 1,36. Ob die Türkei bereits schrumpft und wie sich Aus- und Rückwanderung zwischen Deutschland und der Türkei verhalten, wurde nicht geprüft ❓.',
  L('eufert')],
 ['Afghanen seien bei Sexualstraftaten „grob überrepräsentiert“ [1:10]',
  '❓ Nicht geprüft. Amtliche Zahlen zu Tatverdächtigen nach Staatsangehörigkeit veröffentlicht das BKA (PKS, Lagebild „Kriminalität im Kontext von Zuwanderung“); Tatverdächtigenzahlen sind keine Verurteilungen und hängen u. a. von Alters- und Geschlechtsstruktur ab. Eine Zahl wird hier nicht genannt, weil keine Quelle geprüft wurde.',
  '–'],
 ['Columbia habe nach gestrichenen Bundesmitteln über ein Ende seiner DEI-Programme verhandelt; Harvard verweigere sich [1:21–1:22]',
  'Die US-Regierung zog im März 2025 rund 400 Mio. US-$ an Zuschüssen und Verträgen zurück. Am 23.07.2025 einigte sich Columbia: 200 Mio. US-$ Zahlung ohne Schuldeingeständnis plus 21 Mio. US-$ zur Beilegung von EEOC-Verfahren; Zusagen u. a. zum Ende von Rassenpräferenzen bei Einstellung und Zulassung und von „race-based DEI“-Programmen; die meisten Mittel werden wieder freigegeben. Zu Harvard wurde keine Quelle geprüft ❓.',
  L('columbia')],
 ['Jeff Bezos habe „die Vogue gekauft“; die Washington Post habe auf seinen Wunsch keine Wahlempfehlung für Biden abgegeben [0:18], [1:18], [1:21]',
  '❓ Nicht geprüft. Für einen Kauf der Vogue durch Bezos wurde keine Quelle gefunden (Vogue gehört zum Verlag Condé Nast 📚). Die Wahlempfehlung der Washington Post betraf 2024 Kamala Harris, nicht Joe Biden 📚 – Einzelheiten nicht geprüft.',
  '–'],
 ['Deutschland habe ein „extrem geringes Schutzalter“; ab 14 sei man aus dem strafrechtlichen Schutz heraus [1:28], [1:43]',
  'Laut Wissenschaftlichem Dienst des Bundestages liegt das Mindestalter der sexuellen Einwilligungsfähigkeit bei 14 Jahren (§ 176 StGB). Darüber hinaus schützt § 182 StGB Jugendliche unter 18 bei Ausnutzung einer Zwangslage oder gegen Entgelt und unter 16, wenn ein Täter über 21 die fehlende Fähigkeit zur sexuellen Selbstbestimmung ausnutzt; § 174 StGB schützt Schutzbefohlene bis 16 bzw. 18. Das Gesetz zur Bekämpfung sexualisierter Gewalt gegen Kinder (2021) verschärfte die Strafen für § 176 und § 184b.',
  L('wd')],
 ['„60 Missbrauchsfälle pro Tag“ (Gastgeber) [1:39]',
  'Bundeslagebild 2024: 16.354 registrierte Fälle sexuellen Missbrauchs von Kindern und 1.191 Fälle bei Jugendlichen; 42.854 Fälle kinderpornografischer Inhalte. Die Fallzahl war fast unverändert zum Vorjahr, aber über dem Fünfjahresschnitt. Das entspricht rund 45 Fällen von Kindesmissbrauch pro Tag (eigene Rechnung 📚); erfasst ist nur das Hellfeld.',
  L('lage')],
 ['Katholische Kirche: „Schweigekartell“, Täter gedeckt und versetzt [1:40–1:42]',
  'MHG-Studie (2018, im Auftrag der Bischofskonferenz): Hinweise auf 1.670 beschuldigte Kleriker und 3.677 Betroffene (1946–2014), 52 % 13 Jahre oder jünger. Kirchenrechtliche Verfahren gab es in 34 % der Fälle; beschuldigte Priester wurden häufiger versetzt; in sechs von sieben Teilprojekten fanden sich Hinweise auf vernichtete oder manipulierte Akten. Die Zahlen gelten als „untere Schätzgrößen“. Zur Aussage, das Problem sei heute „im Griff“, wurde keine Quelle geprüft ❓.',
  L('mhg')],
 ['Die Bundeszentrale für gesundheitliche Aufklärung „gehört erstmal abgeschafft“ [1:31]',
  'Die BZgA wurde am 13.02.2025 per Erlass in „Bundesinstitut für Öffentliche Gesundheit“ (BIÖG) umbenannt; die Behörde besteht unter neuem Namen fort.',
  L('bioeg')+' · '+L('parit')],
 ['Bei Wiederholungstätern solle man medikamentöse Mittel nutzen, wie in einigen US-Bundesstaaten [1:44–1:45]',
  '❓ Nicht geprüft: welche US-Bundesstaaten solche Regelungen haben und wie wirksam sie sind. Zu medizinischen Behandlungen äußern sich Fachgesellschaften; hier wird keine Empfehlung gegeben.',
  '–'],
]

# ---------- Diagramme ----------
de_fert = [[2000,1.38],[2001,1.35],[2002,1.34],[2003,1.34],[2004,1.36],[2005,1.34],[2006,1.33],[2007,1.37],[2008,1.38],[2009,1.36],[2010,1.39],[2011,1.39],[2012,1.41],[2013,1.42],[2014,1.47],[2015,1.5],[2016,1.6],[2017,1.57],[2018,1.57],[2019,1.54],[2020,1.53],[2021,1.58],[2022,1.46],[2023,1.39],[2024,1.36]]
tr_fert = [[2007,2.13],[2008,2.1],[2009,2.09],[2010,2.04],[2011,2.03],[2012,2.09],[2013,2.08],[2014,2.17],[2015,2.14],[2016,2.11],[2017,2.07],[2018,1.99],[2019,1.88],[2022,1.63],[2023,1.51],[2024,1.48]]
soz = [[2013,28.77],[2014,28.6],[2015,28.84],[2016,29.11],[2017,28.93],[2018,29.01],[2019,29.44],[2020,32.26],[2021,31.3],[2022,29.76],[2023,29.74],[2024,30.87]]
yrs = list(range(2014,2025))
mil_de = list(zip(yrs,[1.16,1.16,1.18,1.21,1.23,1.33,1.49,1.43,1.48,1.61,2.00]))
mil_nato = list(zip(yrs,[2.56,2.46,2.46,2.37,2.38,2.52,2.69,2.59,2.44,2.44,2.61]))
mil_eur = list(zip(yrs,[34749,35898,37598,40265,42127,46936,51392,52431,58266,67621,86638]))
P = lambda l: [[a,b] for a,b in l]

D = [
 {"typ":"kurs","id":"krah-geburten","titel":"📈 Geburtenziffer: Deutschland und Türkei (Kinder je Frau)",
  "reihen":[{"name":"Deutschland","kurz":"DE","einheit":"Kinder je Frau","dez":2,"hoeherGut":None,"punkte":P(de_fert)},
            {"name":"Türkei","kurz":"TR","einheit":"Kinder je Frau","dez":2,"hoeherGut":None,"punkte":P(tr_fert)}],
  "hoeherGut":None,"vergleich":True,
  "quelle":L('eufert')+", Stand 30.09.2026 (Türkei: 2020/2021 keine Werte) · "+L('destgeb')+" (2025: 1,32)",
  "hinweis":"Bezug zum Gespräch [0:13], [1:08]: Krah sagt für Deutschland „ein Kind“ bis Ende des Jahrzehnts voraus und nennt für die Türkei 1,4. Eurostat weicht bei Deutschland 2024 (1,36) leicht von Destatis (1,35) ab."},
 {"typ":"kurs","id":"krah-sozial","titel":"📈 Ausgaben für Sozialschutz in Deutschland (% des BIP)",
  "reihen":[{"name":"Sozialschutzausgaben","kurz":"% BIP","einheit":"%","dez":1,"hoeherGut":None,"punkte":P(soz)}],
  "hoeherGut":None,"vergleich":False,
  "quelle":L('eusoz')+", Stand 26.10.2026",
  "hinweis":"Bezug zum Gespräch [0:43]: „ungefähr 30 % der gesamten deutschen Wirtschaftsleistung“ für den Sozialstaat. ESSPROS-Abgrenzung (u. a. Rente, Gesundheit, Familie, Arbeitslosigkeit)."},
 {"typ":"kurs","id":"krah-nato-quote","titel":"📈 Verteidigungsausgaben in % des BIP: Deutschland und NATO gesamt",
  "reihen":[{"name":"Deutschland","kurz":"DE","einheit":"%","dez":2,"hoeherGut":None,"punkte":P(mil_de)},
            {"name":"NATO gesamt","kurz":"NATO","einheit":"%","dez":2,"hoeherGut":None,"punkte":P(mil_nato)}],
  "hoeherGut":None,"vergleich":True,
  "quelle":L('nato')+" (Tabelle 3, 2024 Schätzung), Datenstand 03.06.2025",
  "hinweis":"Bezug zum Gespräch [0:54–0:55]: „wir sind jetzt bei zwei“, Trump fordere 5 %. Beschluss Den Haag: 3,5 % + 1,5 % bis 2035 ("+L('bmvg')+")."},
 {"typ":"kurs","id":"krah-nato-euro","titel":"📈 Verteidigungsausgaben Deutschlands nach NATO-Definition (Mio. €)",
  "reihen":[{"name":"Verteidigungsausgaben","kurz":"Mio. €","einheit":"Mio. €","dez":0,"hoeherGut":None,"punkte":P(mil_eur)}],
  "hoeherGut":None,"vergleich":False,
  "quelle":L('nato')+" (Tabelle 1, laufende Preise, 2024 Schätzung), Datenstand 03.06.2025",
  "hinweis":"Bezug zum Gespräch [0:50–0:56]: Aufrüstung als „teurer Schuss in den Ofen“ [seine Sicht]. Haushalt 2025 laut Haushaltsausschuss: 86,37 Mrd. € ("+L('hib')+")."},
 {"typ":"balken","titel":"📊 Bundestagswahl 2025, Wahlkreis 115 Duisburg II – Zweitstimmen (%)","einheit":"%","dez":1,
  "zeilen":[["SPD",25.3],["AfD",24.8],["CDU",19.4],["Linke",11.1],["Grüne",6.6],["BSW",5.8]],
  "quelle":L('wk115')+", endgültiges Ergebnis",
  "hinweis":"Bezug zum Gespräch [1:07]: „Duisburg Nord … da sind wir stärkste Kraft“. Im gesamten Wahlkreis lag die AfD 0,5 Punkte hinter der SPD (2021: 12,2 %); Stadtteile nicht geprüft ❓."},
 {"typ":"balken","titel":"📊 Öffentlicher Dienst: Zuwachs an Beschäftigten vom 30.06.2023 zum 30.06.2024","einheit":"Personen","dez":0,
  "zeilen":[["Insgesamt",95900],["Schulen",19500],["Hochschulen inkl. Kliniken",14200],["Kommunale Kitas",11000]],
  "quelle":L('destod')+", vorläufige Ergebnisse",
  "hinweis":"Bezug zum Gespräch [0:46–0:47]: Die Zahl der Beamten steige, obwohl die Technik zum Ersetzen da sei. An Schulen stieg die Zahl der Beamtinnen und Beamten um 16.300."},
 {"typ":"vergleich","titel":"⚖️ Zahlen im Gespräch und Daten nebeneinander","la":"Im Gespräch genannt","lb":"Daten laut Quelle",
  "zeilen":[
   {"n":"Sozialschutzausgaben Deutschland (2024)","a":30,"b":30.87,"einheit":"% des BIP","f":"[0:43]","q":L('eusoz')},
   {"n":"Verteidigungsausgaben Deutschlands (2024, Schätzung)","a":2,"b":2.00,"einheit":"% des BIP","f":"[0:55]","q":L('nato')},
   {"n":"Geburtenziffer Türkei (2024)","a":1.4,"b":1.48,"einheit":"Kinder je Frau","f":"[1:08]","q":L('eufert')},
   {"n":"Fälle sexuellen Kindesmissbrauchs pro Tag (2024; 16.354 ÷ 366, eigene Rechnung)","a":60,"b":44.7,"einheit":"Fälle","f":"[1:39]","q":L('lage')}]},
]

# ---------- Zeitachse ----------
ZA = [
 ("1914","1914","Erster Weltkrieg – laut Krah Deutschlands Versuch, Supermacht zu werden","[1:03]",False),
 ("1915","1915","Versenkung der Lusitania (07.05.1915) – vom Gastgeber genannt","[0:58]",True),
 ("1916","1916","Wiederwahl Woodrow Wilsons als „Friedenspräsident“ (Gastgeber)","[0:58]",True),
 ("1917","1917","Kriegseintritt der USA (April 1917)","[0:58]",True),
 ("1920er","1920","Weimarer Republik, Armut – laut Gastgeber Hintergrund späterer Militarisierung","[0:54]",False),
 ("1940","1940","Rudi Dutschke geboren (07.03.1940, Schönefeld bei Luckenwalde)","[1:59]",True),
 ("1967","1967","Einspieler: Dutschke über Arbeitszeit, Wiedervereinigung und Parteien","[1:55–1:57]",False),
 ("1968","1968","Streitgespräch Dutschke – Ralf Dahrendorf (Freiburg, Januar 1968)","[2:00]",True),
 ("1968","1968","Attentat auf Dutschke (11.04.1968)","[2:01]",True),
 ("1977","1977","Maximilian Krah geboren (28.01.1977, Räckelwitz, DDR)","[1:59]",True),
 ("1979","1979","Margaret Thatcher Premierministerin – Beginn des Neoliberalismus laut Krah („späte 70er“)","[0:43]",True),
 ("1979","1979","Dutschke stirbt an Spätfolgen des Attentats (24.12.1979)","[2:01]",True),
 ("1979–1989","1979","Sowjetischer Krieg in Afghanistan – laut Krah Aufbau eines „Dschihad-Spielplatzes“","[1:15]",True),
 ("1991","1991","Krah tritt der Jungen Union bei (später CDU)","[0:06]",True),
 ("1999","1999","Kosovokrieg mit deutscher Beteiligung (Schröder)","[1:02]",True),
 ("2001","2001","11. September und folgende Kriege – laut Gastgeber Ursache großer Fluchtbewegungen","[1:16]",False),
 ("2003","2003","Deutschland beteiligt sich nicht am Irakkrieg","[1:02]",True),
 ("2005","2005","Nord-Stream-Abkommen (Schröder-Ära)","[1:02]",True),
 ("2013","2013","Gründung der AfD – laut Krah von Wirtschaftsprofessoren gegen die Euro-Rettung","[0:06]",True),
 ("2015","2015","Grenzöffnung/Fluchtbewegung – zweite „Welle“ der AfD","[0:06]",False),
 ("2015","2015","TV-Debatte: Trump antwortet „Only Rosie O’Donnell“","[1:19]",False),
 ("2015","2015","Gespräch Krahs mit einem Dresdner Vorsitzenden Richter über Überfallvergewaltigungen (Anekdote)","[1:40]",False),
 ("2016","2016","Krah verlässt die CDU und tritt der AfD bei","[0:06]",True),
 ("2018","2018","MHG-Studie zu sexuellem Missbrauch in der katholischen Kirche","[1:40]",True),
 ("2019","2019","Krah wird Mitglied des Europäischen Parlaments (02.07.2019); Jian G. arbeitet 2019–2024 in seinem Büro","[1:04]",True),
 ("2020–2022","2020","Corona-Politik – dritte „Welle“ der AfD laut Krah","[0:06–0:07]",False),
 ("2021","2021","Gesetz zur Bekämpfung sexualisierter Gewalt gegen Kinder","[1:28]",True),
 ("2022","2022","Fußball-WM in Katar – „Regenbogenbinde“ (Faeser)","[1:05]",True),
 ("2023","2023","Krahs Buch „Politik von rechts“ (Antaios)","[1:49]",True),
 ("2023","2023","Nike-Werbung („Mann im BH“) – laut Krah Kultur der Dekadenz","[1:17]",False),
 ("23.04.2024","2024","Festnahme von Krahs Mitarbeiter Jian G.","—",True),
 ("23.05.2024","2024","ID-Fraktion schließt die AfD nach Krahs SS-Äußerungen aus","[0:11]",True),
 ("2024","2024","Europawahl: AfD laut Krah „Jugendpartei“ geworden","[0:04]",False),
 ("13.02.2025","2025","BZgA wird in BIÖG umbenannt","[1:31]",True),
 ("23.02.2025","2025","Bundestagswahl: Krah gewinnt Wahlkreis 162 (44,2 %); AfD in Duisburg II 24,8 %","[1:07]",True),
 ("März 2025","2025","US-Regierung zieht rund 400 Mio. US-$ Bundesmittel von Columbia zurück","[1:21]",True),
 ("02.05.2025","2025","Verfassungsschutz stuft AfD als „gesichert rechtsextremistisch“ ein; 08.05. Stillhaltezusage","—",True),
 ("Mai 2025","2025","Generalstaatsanwaltschaft Dresden leitet Ermittlungsverfahren gegen Krah ein","—",True),
 ("24./25.06.2025","2025","NATO-Gipfel Den Haag: 5-%-Ziel bis 2035","[0:54]",True),
 ("26.06.2025","2025","Thiel-Interview mit Ross Douthat (New York Times)","[0:18]",True),
 ("Sommer 2025 ❓","2025","Aufnahme des Gesprächs (eingegrenzt aus Bezügen)","—",True),
 ("23.07.2025","2025","Columbia einigt sich mit der US-Regierung (200 Mio. + 21 Mio. US-$)","[1:21]",True),
 ("11.09.2025","2025","Bundestag hebt Krahs Immunität auf; Durchsuchungen","—",True),
 ("30.09.2025","2025","OLG Dresden verurteilt Jian G. zu 4 Jahren 9 Monaten","—",True),
 ("Februar 2026","2026","VG Köln: Eilantrag der AfD gegen die Einstufung im Wesentlichen erfolgreich","—",True),
 ("bis 2030","2030","Prognose Krah: im Schnitt „ein Kind“ je Frau bis Ende des Jahrzehnts","[0:13]",False),
 ("2035","2035","Zieljahr des NATO-5-%-Ziels","[0:54]",True),
]

PERS = [
 ["Maximilian Krah","AfD-Bundestagsabgeordneter (Wahlkreis 162), Jurist, MdEP 2019–2025","Gast","durchgehend"],
 ["Gastgeber (REALTALK MEDIA)","Name im Video nicht genannt ❓; laut eigener Aussage aus Kreuzberg, staatskritisch","Fragen, eigene Thesen, Widerspruch","durchgehend"],
 ["Heidi Reichinnek","Die Linke","Konkurrenz um junge Wähler","[0:04], [0:41]"],
 ["Sahra Wagenknecht","BSW","eingeladen; „immer lesenswert“","[0:01], [0:27], [1:59]"],
 ["Alice Weidel","AfD-Vorsitzende","nenne die AfD „libertär“ (Gastgeber)","[0:27]"],
 ["Peter Thiel","Investor, Palantir-Mitgründer","Posthumanismus, Gefahrenliste","[0:18–0:27], [1:24]"],
 ["Alex Karp","Palantir-Chef","„Neomarxist“ (Gastgeber)","[0:26–0:28]"],
 ["JD Vance","US-Vizepräsident","KI-Rede in Paris ❓, Deutschland-Sympathie","[0:16], [0:51], [1:24]"],
 ["Donald Trump","US-Präsident","5 %, Zölle, Kulturwandel","[0:54–0:56], [1:17–1:24]"],
 ["Jeff Bezos · Lauren Sánchez","Amazon-Gründer und Partnerin","Vogue ❓, Washington Post","[0:18], [1:18], [1:21], [1:23]"],
 ["Elon Musk","Unternehmer","Regulierung, „Blatt im Wind“ (Gastgeber)","[0:32], [1:25]"],
 ["Friedrich Merz","Bundeskanzler (CDU)","5-%-Ziel, Souveränität, Türkei","[0:55–0:56], [1:03], [1:09]"],
 ["Gerhard Schröder · Angela Merkel · Olaf Scholz","frühere Kanzler","Souveränitäts-Stufen","[1:02–1:04]"],
 ["Recep Tayyip Erdoğan","Präsident der Türkei","Beispiel für wachsende Souveränität","[0:15], [1:03]"],
 ["Mohammed bin Salman","saudischer Kronprinz","Machtverschiebung","[0:15], [1:04]"],
 ["Nancy Faeser","frühere Innenministerin (SPD)","„Regenbogenbinde“ in Katar","[1:05]"],
 ["Paul Ronzheimer · Tucker Carlson","Journalist (Bild) · US-Moderator","Gespräch über Deutschland ❓","[1:15]"],
 ["Karoline Leavitt","Pressesprecherin des Weißen Hauses","Beispiel für neuen Stil","[1:18]"],
 ["Larry Fink","BlackRock-Chef","ESG-Wende (Gastgeber)","[1:19]"],
 ["Woodrow Wilson","US-Präsident 1913–1921","„Friedenspräsident“ (Gastgeber)","[0:58]"],
 ["Armin Laschet","CDU","Beispiel für „konservativ“","[1:47–1:48]"],
 ["Michel Foucault","französischer Philosoph","Dekonstruktivismus; Vorwurf ❓","[1:51]"],
 ["Rudi Dutschke · Ralf Dahrendorf","Studentenführer · liberaler Soziologe","Einspieler, Streitgespräch","[1:55–2:01]"],
 ["Matt Walsh","US-Publizist („What Is a Woman?“)","Vorbild der Schlussfrage","[2:02]"],
 ["„Simo“ (Meet Your Mentor)","Podcaster ❓","früheres Krah-Gespräch","[1:06], [1:25]"],
]
ORTE = [
 ["Berlin-Kreuzberg","Sitz des Kanals laut Gastgeber, „Höhle des Löwen“","[0:01], [0:03]"],
 ["Dubai · Katar · Saudi-Arabien","Machtzentren und Staatsmodell","[0:15], [0:30–0:32], [1:04]"],
 ["Paris","KI-Rede von Vance ❓","[0:16]"],
 ["Silicon Valley · Wall Street","Machtverschiebung West- statt Ostküste","[0:18–0:21]"],
 ["Kiew · Singapur","Taschendiebstahl vs. Kameraüberwachung","[0:34]"],
 ["Görlitzer Park (Berlin)","Beispiel für Kriminalität","[0:35], [1:39]"],
 ["Brüssel","Krahs früheres EP-Büro, Delegationen","[0:44], [1:05–1:06]"],
 ["Ägypten","Dünger-Mangel durch Russland-Sanktionen (laut Krah)","[1:06]"],
 ["Duisburg-Marxloh / Wahlkreis Duisburg II","AfD-Ergebnis, türkeistämmige Wähler","[1:07]"],
 ["Türkei (Istanbul, Antalya, Bodrum)","Geburtenrate, Souveränität","[1:03], [1:08–1:10]"],
 ["Afghanistan","Krieg der 1980er, Herkunft von Geflüchteten","[1:10–1:15]"],
 ["Columbia University · Harvard (USA)","Bundesmittel und DEI","[1:21–1:22]"],
 ["Dresden","Gespräch mit Vorsitzendem Richter (2015)","[1:40]"],
 ["Slowakei","Parlamentskollege als Jugend-Influencer","[1:55]"],
]
BEGR = [
 ["Leadership / Herrschaft","laut Krah: die Fähigkeit, Menschen zum Wandel zu motivieren","[0:09–0:11]"],
 ["Libertär","Staat zieht sich aus fast allem zurück; Krah lehnt das Etikett ab","[0:27–0:33]"],
 ["„Wille zum Staat“ / Preußentum","Krahs Staatsideal: stark, schlank, ohne Eingriff ins Privatleben","[0:31]"],
 ["Neoliberalismus","Rückbau des Staates zugunsten des Marktes (Thatcher, Reagan)","[0:43]"],
 ["CBDC","digitales Zentralbankgeld; „PBDC“ = privates Digitalgeld (Gastgeber)","[0:33]"],
 ["Elektronische Patientenakte (ePA)","digitale Gesundheitsakte","[0:36]"],
 ["Transhumanismus / Posthumanismus","Erweiterung bzw. Auflösung des Menschen durch Technik","[0:16], [0:21–0:25]"],
 ["5-%-Ziel","NATO-Ziel für Verteidigungsausgaben (3,5 % + 1,5 % des BIP bis 2035)","[0:54]"],
 ["Souveränität","nach Krah eine Stufenleiter statt Ja/Nein","[1:01–1:04]"],
 ["DEI / ESG","Diversitäts- bzw. Nachhaltigkeitsprogramme in Unternehmen und Hochschulen","[1:19], [1:21]"],
 ["Schutzalter","Alter, ab dem sexuelle Handlungen nicht mehr als Kindesmissbrauch strafbar sind (14; Schutz bis 16/18 nach §§ 174, 182 StGB)","[1:28], [1:43]"],
 ["BZgA / BIÖG","Bundeszentrale für gesundheitliche Aufklärung, seit 2025 Bundesinstitut für Öffentliche Gesundheit","[1:31]"],
 ["Dekonstruktivismus","Denkrichtung, die Begriffe als Konstruktionen behandelt (Foucault laut Krah)","[1:51]"],
 ["Gesichert rechtsextremistisch / Verdachtsfall","Einstufungen des Verfassungsschutzes (nicht im Gespräch, nur Abgleich)","—"],
]
ZAHLEN = [
 ["Geburtenziffer (Prognose Krah)","„ein Kind“ je Frau bis Ende des Jahrzehnts","[0:13]"],
 ["Sozialstaat","„ungefähr 30 %“ der Wirtschaftsleistung","[0:43]"],
 ["Beamtenstellen","nur jede 2. nachbesetzen; 1/3 sofort, ½ absehbar durch Computer ersetzbar","[0:44], [0:46]"],
 ["Öffentlicher Dienst (Ampelzeit)","„100.000 neue Stellen“","[0:47]"],
 ["NATO-Ziel","5 % des BIP = „40 % des Bundeshaushalts“; Rente „30 %“; „wir sind bei zwei“","[0:54–0:55]"],
 ["Europa","„über 200 Millionen Menschen“","[0:52]"],
 ["Geburtenziffer Türkei","1,4","[1:08]"],
 ["Kindesmissbrauch (Gastgeber)","„60 Fälle pro Tag“","[1:39]"],
 ["Strafmaß (Krah)","„auf keinen Fall unter 5 Jahre“, wiederholt 8 Jahre","[1:44]"],
 ["Kinder (Gastgeber)","„acht Kinder von verschiedenen Frauen“","[1:36]"],
 ["Arbeitszeit (Dutschke-Einspieler)","seit Jahrzehnten nur wenige Stunden weniger pro Woche","[1:55]"],
]

KERN = [
 ["1","Die AfD sei keine Nazi-Partei; der Vorwurf ersetze Argumente.","Wellen: Euro, Grenzen, Corona – „recht behalten“; Abgrenzung von Neonazis","[0:05–0:09]","★★"],
 ["2","Politik müsse Menschen zum Wandel motivieren („Leadership“ statt Befehl).","US-Ausbildung; eigene Rolle als Ideengeber","[0:09–0:13]","★★"],
 ["3","Demografie und KI seien die Zukunftsfragen; Automatisierung ersetze fehlende Menschen.","Busse, Bahn, KI-Lehrer, Golfstaaten als Vorbild","[0:13–0:16]","★★★"],
 ["4","KI und Tech-Oligarchen bergen große Manipulationsrisiken; Thiel sei klug, aber im Posthumanismus.","KI-Puppen, Machtverschiebung zur Westküste, Leib-Seele-Einheit","[0:16–0:26]","★★★"],
 ["5","Krah sei kein Libertärer, sondern wolle einen starken, schlanken Staat („Wille zum Staat“).","Preußen, Dubai; Militär, Kultur; Krypto als Gegengewicht","[0:28–0:35]","★★★"],
 ["6","Sozialstaat und Verwaltung seien zu groß; Beamtenstellen ließen sich durch Computer ersetzen.","30 % der Wirtschaftsleistung, jede 2. Stelle, Behörden abschaffen","[0:43–0:50]","★★"],
 ["7","Das 5-%-Ziel sei nicht finanzierbar und diene vor allem US-Rüstungsexporten.","40 % des Haushalts, Handelsdefizit, Zölle; Rüstung ökonomisch schwach","[0:50–1:01]","★★"],
 ["8","Deutschland sei weniger souverän als unter Schröder; Diplomatie ohne Belehrung.","Kosovo/Irak/Nord Stream; Türkei als Gegenbeispiel; Brüsseler Delegationen","[1:01–1:07]","★★"],
 ["9","Einwanderer seien nach Gruppen zu unterscheiden; türkeistämmige Wähler seien Partner der AfD.","Duisburg, Geburtenrate Türkei, Afghanistan-Krieg","[1:07–1:17]","★★"],
 ["10","Kinderschutz: keine externe Sexualkunde an Grundschulen, härtere Strafen, Rechts heiße „leben als das, was ich bin“.","Schutzalter, BZgA, Kirche, Strafmaß; Objektivität gegen Dekonstruktivismus","[1:26–1:55]","★★★"],
]

BAUM = [
 {"t":"🏷️ AfD & Person [0:03–0:13]","k":[{"t":"Jugendpartei durch TikTok [0:04]"},{"t":"„Wie viel Nazi?“ – „gar kein“ [0:05]"},{"t":"Wellen: Euro, Grenzen, Corona [0:06]"},{"t":"Abgrenzung von Neonazis [0:08]"},{"t":"Einfacher Abgeordneter [0:11]"}]},
 {"t":"🧭 Staat & Herrschaft [0:09–0:43]","k":[{"t":"Leadership = Wandel motivieren [0:10]"},{"t":"Kein Libertärer [0:28]"},{"t":"„Wille zum Staat“: Preußen, Dubai [0:31]"},{"t":"Digitales Geld, digitale ID [0:33]"},{"t":"Wünschenswert vs. möglich [0:42]"}]},
 {"t":"🤖 Demografie, KI & Tech-Elite [0:13–0:40]","k":[{"t":"Ein Kind je Frau? [0:13]"},{"t":"Autonome Busse und Bahn [0:14]"},{"t":"Wer steuert die KI? [0:16]"},{"t":"Thiel, Karp, Palantir [0:18–0:28]"},{"t":"Patientenakte und Landarzt [0:36]"}]},
 {"t":"💶 Sozialstaat, Beamte & Rüstung [0:43–0:57]","k":[{"t":"Sozialstaat 30 % [0:43]"},{"t":"Jede 2. Beamtenstelle [0:44]"},{"t":"Deindustrialisierung [0:48]"},{"t":"Rüstung im Depot [0:50]"},{"t":"5-%-Ziel und US-Handelsdefizit [0:54]"}]},
 {"t":"🌍 Außenpolitik & Souveränität [0:57–1:07]","k":[{"t":"Kriegsangst, Wehrdienst [0:58]"},{"t":"Souveränität als Stufenleiter [1:01]"},{"t":"Schröder, Merkel, Scholz, Merz [1:02]"},{"t":"Türkei als Gegenbeispiel [1:03]"},{"t":"Diplomatie in Brüssel [1:05]"}]},
 {"t":"🧩 Migration & Wählergruppen [1:07–1:17]","k":[{"t":"Türkeistämmige Wähler [1:07]"},{"t":"Geburtenrate Türkei [1:08]"},{"t":"Gruppen unterscheiden [1:10]"},{"t":"Afghanistan der 80er [1:15]"}]},
 {"t":"🇺🇸 USA & Kulturwandel [1:17–1:26]","k":[{"t":"Nike, Mode, Leavitt [1:17]"},{"t":"Galionsfigur Trump [1:19]"},{"t":"Columbia und Harvard [1:21]"},{"t":"Widerspruch: Eliten machen Trump [1:22]"}]},
 {"t":"🧒 Jugend & Kinderschutz [1:26–1:46]","k":[{"t":"Pubertät und Identität [1:26]"},{"t":"Schutzalter 14 [1:28]"},{"t":"Sexualkunde, BZgA [1:31]"},{"t":"Treue und Familie [1:34–1:37]"},{"t":"Strafrecht, Kirche [1:38–1:46]"}]},
 {"t":"➡️ Rechts, Links & Deutschsein [1:46–2:04]","k":[{"t":"Rechts = leben als das, was ich bin [1:48]"},{"t":"Dekonstruktivismus [1:51]"},{"t":"Dutschke-Einspieler [1:55]"},{"t":"„Was ist ein Deutscher?“ [2:02]"}]},
]

INKUERZE = [
 '**Wer:** Maximilian Krah, AfD-Bundestagsabgeordneter, im Gespräch mit dem Gastgeber von REALTALK MEDIA (Name im Video nicht genannt ❓), einem Kanal aus Berlin-Kreuzberg; 2 Std. 4 Min., aufgenommen vermutlich im Sommer 2025 ❓.',
 '**AfD und Nazi-Vorwurf:** Krah weist den Vorwurf zurück und beschreibt die AfD als Sammelbecken von Kritikern der Euro-Rettung, der Grenzöffnung 2015 und der Corona-Politik [0:05–0:09].',
 '**Zukunft:** Demografie und KI seien die großen Themen; Automatisierung solle fehlende Arbeitskräfte ersetzen, zugleich warnt er vor Manipulation und einer Tech-Oligarchie um Thiel und andere [0:13–0:26].',
 '**Staat:** Er sei kein Libertärer, sondern wolle einen starken, schlanken Staat nach preußischem Vorbild; Sozialstaat und Verwaltung seien zu groß, das 5-%-Ziel der NATO nicht finanzierbar [0:28–0:57].',
 '**Außenpolitik und Migration:** Souveränität sei eine Stufenleiter (Schröder oben, Merz unten); türkeistämmige Wähler sieht er als Partner, Einwanderer seien nach Gruppen zu unterscheiden [1:01–1:17].',
 '**USA:** Trump bewirke einen Kulturwandel; der Gastgeber widerspricht: Die Eliten bestimmten Trump, nicht umgekehrt [1:17–1:26].',
 '**Kinderschutz:** Krah will keine externe Sexualkunde an Grundschulen, die BZgA abschaffen und härtere Strafen; zur Kirche spricht er von einem „Schweigekartell“ [1:26–1:46].',
 '**Abgleich:** Gegen Krah läuft seit Mai 2025 ein Ermittlungsverfahren (Immunität am 11.09.2025 aufgehoben; Stand dann: keine Anklage, Unschuldsvermutung); die Einstufung der AfD durch den Verfassungsschutz ist gerichtlich vorerst ausgesetzt (VG Köln, Februar 2026, nicht rechtskräftig).',
]
SICHT = [
 '[seine Sicht] Politik heißt für Krah, Menschen zum Wandel zu bewegen – weg von Phrasen der 80er Jahre, hin zu den Fragen der nächsten fünf bis zehn Jahren: Demografie, KI, neue Machtzentren am Golf und in Asien.',
 '[seine Sicht] Den Staat will er stark, aber schlank: Er soll Richtung vorgeben, Sicherheit und Kultur sichern, sich aber aus dem Privatleben heraushalten – „Preußen“ und „Dubai“ statt eines Staates, der überall mitredet.',
 '[seine Sicht] Technik ist für ihn unvermeidlich und nützlich, aber nur, wenn man ihren Preis – Datenmacht, Manipulation, Oligarchie – bewusst klein hält.',
 '[seine Sicht] Nach außen solle Deutschland Spielraum nutzen statt belehren; nach innen Einwanderer nach Gruppen unterscheiden und Verbündete suchen, etwa unter türkeistämmigen Wählern.',
 '[seine Sicht] „Rechts“ heißt für ihn, als das zu leben, was man objektiv ist – daraus leitet er seine Positionen zu Familie, Geschlecht, Kinderschutz und Deutschsein ab.',
]

SPANN = [
 'Der Gastgeber widerspricht offen beim Verhältnis von Trump und Eliten: Nicht Trump verändere die Eliten, die Eliten bestimmten Trump; am Ende einigen sich beide auf eine „Verschiebung“ innerhalb der Eliten [1:22–1:24].',
 'Bei der Medizin hält der Gastgeber dagegen, ein empathischer Hausarzt sei besser als die digitale Praxis; Krah antwortet, die Wahl bestehe nur zwischen einer schlechter werdenden Lage und der digitalen Lösung [0:38–0:40].',
 'Der Gastgeber bringt mehrfach eigene Thesen ein (Geheimdienste hinter Palantir und Terrorgruppen, gewollte Deindustrialisierung, Kriege als Geschäftsmodell), die Krah teils übernimmt, teils relativiert („nicht die Schuld geheimnisvoller Mächte“) [0:21], [0:41], [0:48], [0:58], [1:13].',
 'Krah ist „Gegner der EU“, wünscht sich aber eine europäische Wirtschaftskooperation und eine deutsche Vorreiterrolle [0:51–0:52].',
 'Krah lehnt die Aufnahme traumatisierter Menschen ab, beschreibt aber zugleich Krieg als Ursache von Radikalisierung, für den er die US-Politik der 1980er mitverantwortlich macht [1:12–1:15].',
 'Beim Thema Familie spricht der Gastgeber Krahs Privatleben an; Krah begründet seine Botschaft zur Treue gerade mit eigenen Fehlern und der Versöhnung [1:36–1:37].',
]
MIT = [
 'Mehrere Zahlen des Gesprächs passen zu amtlichen Daten: Sozialschutzausgaben rund 30 % des BIP, Verteidigungsausgaben 2024 rund 2 % des BIP, Geburtenziffer der Türkei um 1,5.',
 'Andere Aussagen halten der Prüfung nicht oder nur teilweise stand: Im Wahlkreis Duisburg II lag die SPD 2025 knapp vor der AfD; die BZgA wurde 2025 umbenannt, nicht abgeschafft; das Schutzalter von 14 wird durch §§ 174 und 182 StGB ergänzt.',
 'Zum Gast selbst gibt es amtliche Vorgänge, die im Gespräch nicht vorkommen: Ermittlungsverfahren der Generalstaatsanwaltschaft Dresden (Immunität am 11.09.2025 aufgehoben; Stand dann: keine Anklage, Unschuldsvermutung) und die Verurteilung seines früheren Mitarbeiters (OLG Dresden, 30.09.2025).',
 'Die Einstufung der AfD durch den Verfassungsschutz ist bis zum Hauptsacheverfahren ausgesetzt; das VG Köln sah zugleich verfassungsfeindliche Bestrebungen innerhalb der Partei (Februar 2026, nicht rechtskräftig).',
]
OFFEN = [
 'Wer führt das Gespräch, und wann wurde das Video veröffentlicht? (Per Suche nicht gefunden.)',
 'Belege für: Gen Z mehrheitlich Single, Vances KI-Rede in Paris, CIA-Ursprung von BCCI/In-Q-Tel und Palantir, Karps Dissertation über Adorno, Vogue-Kauf durch Bezos, Carlson–Ronzheimer-Gespräch.',
 'Wie hoch ist der Anteil von Tatverdächtigen bestimmter Staatsangehörigkeiten bei Sexualdelikten, und wie ist er einzuordnen (BKA-Lagebild)?',
 'Welche US-Bundesstaaten sehen medikamentöse Maßnahmen bei Sexualstraftätern vor, und was sagen Fachgesellschaften zur Wirksamkeit?',
 'Wie geht das Hauptsacheverfahren zur Einstufung der AfD aus, und wird im Verfahren gegen Krah Anklage erhoben oder eingestellt?',
]
WEITER = [
 'Bundeswahlleiterin und IT.NRW: Ergebnisse nach Stadtbezirken in Duisburg (Marxloh/Hamborn).',
 'Destatis: Bevölkerungsvorausberechnung (Geburtenziffer-Annahmen bis 2070) im Vergleich zu Krahs „ein Kind bis 2030“.',
 'NATO und Bundesfinanzministerium: Haushaltsplanung zum 5-%-Ziel bis 2029/2035.',
 'Unabhängige Beauftragte für Fragen des sexuellen Kindesmissbrauchs: Dunkelfeldstudien und Aufarbeitung in Kirchen.',
 'VG Köln / OVG NRW: Entscheidungen zur Einstufung der AfD im Wortlaut.',
]

# ---------- Zusammenbau ----------
nA = len(S)
kacheln = [[str(nA),'Abschnitte'],['10','Kernaussagen'],[str(len(AB)),'Abgleich-Punkte'],[str(len(ZA)),'Zeitachse'],[str(len(D)),'Diagramme']]
r1 = [
 {"typ":"folge","k":K,"titel":TITEL,"gast":GAST,"rolle":ROLLE,"kanal":KANAL,"datum":DATUM,"dauer":DAUER,"url":URL,
  "thema":"Maximilian Krah spricht bei REALTALK MEDIA in Berlin-Kreuzberg über den Nazi-Vorwurf gegen die AfD, sein Staatsverständnis, Demografie, KI und Tech-Eliten, Sozialstaat und Rüstung, Souveränität und Migration, Trump, Kinderschutz und darüber, was für ihn „rechts“ und „deutsch“ bedeutet.",
  "kacheln":kacheln},
 {"typ":"hinweis","text":"Auswertung nach dem Transkript (automatische Untertitel): Gesagtes ohne Zeichen, Ergänzungen 📚, Unklares ❓. Fundstellen [Stunde:Minute] springen ins Video. Der Gast ist aktiver Politiker: Seine Aussagen stehen als [seine Sicht], daneben im Abgleich amtliche und gerichtliche Feststellungen mit Quelle. Keine Wahlempfehlung. Die Bewertung bleibt dem Leser."},
 {"typ":"abschnitt","titel":"⚡ In Kürze","liste":INKUERZE},
 {"typ":"abschnitt","titel":"🔦 Aus Krahs Sicht – der rote Faden","liste":SICHT},
 {"typ":"text","text":"🎯 **Kernaussagen** – die zehn wichtigsten Thesen des Gesprächs:"},
 {"typ":"tabelle","kopf":["#","Aussage","Begründung im Gespräch","Fundstelle","Gewicht"],"zeilen":KERN},
 {"typ":"baum","titel":"🌳 Themenbaum des Gesprächs","wurzel":TITEL,"unter":f"{GAST} · {KANAL} · {DATUM} · {DAUER}","knoten":BAUM},
 {"typ":"illu","id":"krah_staatsbild","titel":"Skizze: Welcher Staat? Libertär, „übergriffig“ oder „Wille zum Staat“ (Darstellung laut Krah, schematisch)"},
 {"typ":"illu","id":"krah_verfahren","titel":"Skizze: Amtliche Vorgänge um Krah und die AfD 2024–2026 und Geburtenziffern (belegte Daten)"},
 {"typ":"tabelle","kopf":["🧭 Steckbrief",""],"schmal":True,"zeilen":[
  ["**Thema in einem Satz**","Krah über AfD, Staat, Zukunftstechnik, Außenpolitik, Migration, Kinderschutz und sein Verständnis von „rechts“."],
  ["**Titel**",TITEL],
  ["**Format**","Video-Interview im Studio, Gastgeber mit vorbereiteten Fragen; ein Einspieler (Rudi Dutschke) [1:55–1:57]; keine Werbeblöcke im Transkript"],
  ["**Sprecher**","👤 **Maximilian Krah** – Gast, AfD-Bundestagsabgeordneter · 🎙️ **Gastgeber** von REALTALK MEDIA – Name im Video nicht genannt ❓; bringt eigene Thesen ein und widerspricht an einzelnen Stellen"],
  ["**Dauer**",DAUER],
  ["**Datum**","Veröffentlichung nicht ermittelt ❓; Aufnahme vermutlich Ende Juni bis Mitte Juli 2025 (nach NATO-Gipfel und Thiel-Interview, vor der Columbia-Einigung) ❓"],
  ["**Grundton**","freundlich, locker (Duzen), stellenweise derb; der Gastgeber nennt sich selbst staatskritisch"],
  ["**Hinweis**","Aktiver Politiker: Aussagen als [seine Sicht]; Verfahren gegen ihn nur mit amtlicher Quelle und Datum, Unschuldsvermutung. Das Thema Missbrauch ist knapp und ohne Einzelheiten wiedergegeben."]]},
]
r2 = [
 {"typ":"text","text":f"🔎 Detaillierte Auswertung in der Reihenfolge des Gesprächs – {nA} Abschnitte. Lesehilfe: 💬 Zitat, 📌 Aussage/Zahl/Beispiel, 🔗 Bezug, 📚 Ergänzung, ❓ unklar. Video: [{TITEL}]({URL})"},
 {"typ":"gespraech","titel":"🧭 Gesprächsverlauf – wann worüber gesprochen wird","dauer":"2:04","themen":THEMEN,
  "teile":[{"von":v,"bis":b,"t":k,"th":th} for v,b,t,k,th,l in S]},
]
for v,b,t,k,th,l in S:
    r2.append({"typ":"abschnitt","titel":f"{t} [{v}–{b}]","th":th,"liste":l})
za_sorted = ZA  # bereits chronologisch
r3 = [
 {"typ":"zeitachse","titel":"📅 Zeitachse – Ereignisse, die im Gespräch vorkommen","eintraege":[{"z":z,"j":int(j),"t":t,"f":f,"e":e} for z,j,t,f,e in za_sorted]},
 {"typ":"tabelle","kopf":["👤 Person","Wer / was","Rolle im Gespräch","Fundstelle"],"zeilen":PERS},
 {"typ":"tabelle","kopf":["🗺️ Ort","Rolle","Fundstelle"],"zeilen":ORTE},
 {"typ":"tabelle","kopf":["📖 Begriff","Erklärung","Fundstelle"],"zeilen":BEGR},
 {"typ":"tabelle","kopf":["📊 Zahl im Gespräch","Angabe","Fundstelle"],"zeilen":ZAHLEN},
]
r4 = [
 {"typ":"text","text":"Neutraler Abgleich: links die Aussage im Gespräch, rechts die gängige Darstellung bzw. Daten mit Quelle. Die Bewertung bleibt dem Leser. Zu Verfahren gegen Personen nur, was Gerichte, Staatsanwaltschaften oder amtliche Stellen mitgeteilt haben – mit Datum; es gilt die Unschuldsvermutung."},
 {"typ":"tabelle","kopf":["Aussage im Gespräch","Gängige Darstellung (Mainstream) / Daten 📚","Quelle"],"stapel":True,"zeilen":AB},
] + D + [
 {"typ":"abschnitt","titel":"🧩 Spannungen im Gespräch","liste":SPANN},
 {"typ":"abschnitt","titel":"💡 Was man mitnehmen kann","liste":MIT},
 {"typ":"abschnitt","titel":"❓ Offen","liste":OFFEN},
 {"typ":"abschnitt","titel":"🔎 Weiter recherchieren","liste":WEITER},
]
reiter = [
 {"id":K,"titel":f"{G}: Überblick","bloecke":r1},
 {"id":K+"ab","titel":f"{G}: Gespräch im Detail","bloecke":r2},
 {"id":K+"zeit","titel":f"{G}: Zeitachse & Verzeichnisse","bloecke":r3},
 {"id":K+"abgleich","titel":f"{G}: Abgleich & Daten","bloecke":r4},
]
quellen = [[f"Video: {TITEL} – {KANAL} (YouTube)", URL]] + [[tit(k), url(k)] for k in Q]
out = {"k":K,"gast":GAST,"reiter":reiter,
 "folgen_zeile":[DATUM,f"{GAST} (AfD-Bundestagsabgeordneter)",TITEL,"Nazi-Vorwurf, Staat & Herrschaft, Demografie & KI, Thiel/Palantir, Sozialstaat & Beamte, 5-%-Ziel, Souveränität, Migration, Trump, Kinderschutz, „rechts“",f"{{{{a:realtalk-{K}|hier: {G}}}}}",f"[ansehen]({URL})"],
 "baum_ast":{"gruppe":"🏛️ Macht & Geschichte","t":"👤 Maximilian Krah bei REALTALK MEDIA – AfD, Staat, KI, Rüstung, Migration, Kinderschutz"},
 "neu":{"d":"2026-11-12","t":"REALTALK MEDIA – Maximilian Krah","k":f"Krah über AfD, Staat, KI, Rüstung, Migration und Kinderschutz – {nA} Abschnitte, Abgleich mit amtlichen Quellen, {len(D)} Diagramme.","h":f"#a-realtalk-{K}","art":"Video"},
 "quellen":quellen,
 "web":[]}
p = os.path.join(os.path.dirname(os.path.abspath(__file__)),'folge.json')
json.dump(out, open(p,'w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', nA, 'Abschnitte', len(AB), 'Abgleich', len(D), 'Diagramme', len(ZA), 'Zeitachse')
