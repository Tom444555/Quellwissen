# -*- coding: utf-8 -*-
# Erzeugt folge.json für „Tom Lausen: Enquete-Kommission, AfD & KI – Wer kontrolliert die Zukunft?“
# (K = enquete, Sammelstelle A-09 lausen)
import json, os, re
K = 'enquete'; G = 'Enquete und KI'
URL = 'https://www.youtube.com/watch?v=S-x0-LCeciE'
TITEL = 'Tom Lausen: Enquete-Kommission, AfD & KI – Wer kontrolliert die Zukunft?'
GAST = 'Tom Lausen'
KANAL = 'REALTALK MEDIA'
DATUM = '2026 ❓ (aufgenommen am 28.01.2026)'
DAUER = '2 Std. 4 Min.'
ROLLE = 'Datenanalyst, Publizist; sachverständiges Mitglied der Corona-Enquete-Kommission des Bundestages (benannt von der AfD-Fraktion)'

# ---------- Quellen (alle geprüft: per Suche gefunden/gelesen oder im Kompendium bereits geprüft) ----------
Q = dict(
 hib78='[Bundestag, hib 78/2026 – Anhörung der Enquete-Kommission Corona zum Verhältnis von Regierungen und Parlamenten (29.01.2026)](https://www.bundestag.de/presse/hib/kurzmeldungen-1140476)',
 to14='[Bundestag – Tagesordnung der 14. Sitzung der Enquete-Kommission, 29.01.2026 (PDF)](https://www.bundestag.de/resource/blob/1140024/TO-14-Sitzung-2026-01-29_oeff.pdf)',
 hib394='[Bundestag, hib 394/2025 – Enquete-Kommission konstituiert](https://www.bundestag.de/presse/hib/kurzmeldungen-1107614)',
 konst='[Bundestag – Konstituierung der Enquete-Kommission „Corona“](https://www.bundestag.de/dokumente/textarchiv/2025/kw37-pa-enquete-corona-konstituierung-1107024)',
 lausbt='[Bundestag – Tom Lausen, Sachverständiger der Enquete-Kommission](https://www.bundestag.de/ausschuesse/weitere_gremien/ee01/1107006-1107006)',
 med1512='[Bundestag-Mediathek – Anhörung vom 15.12.2025](https://www.bundestag.de/mediathek/video?videoid=7646762)',
 bmg='[BMG (10.01.2026): Warken widerspricht US-Gesundheitsminister](https://www.bundesgesundheitsministerium.de/ministerium/meldungen/warken-widerspricht-us-gesundheitsminister)',
 zdfk='[ZDFheute (11.01.2026): Faktencheck – Strafverfahren wegen Ausnahmen von Maskenpflicht und Impfen?](https://www.zdfheute.de/politik/ausland/faktencheck-kennedy-gesundheitssystem-deutschland-corona-strafverfahren-100.html)',
 ltobgh='[LTO: BGH bestätigt Verurteilung des früheren Weimarer Familienrichters wegen Rechtsbeugung (2 StR 54/24)](https://www.lto.de/recht/hintergruende/h/bgh-2str54-24-urteil-revision-verworfen-familienrichter-weimar-rechtsbeugung-corona)',
 ltobv='[LTO: BVerfG nimmt Verfassungsbeschwerde des Weimarer Familienrichters nicht an (2 BvR 373/25)](https://www.lto.de/recht/nachrichten/n/bverfg-2bvr373-25-familienrichter-weimar-verfassungsbeschwerde-unzulaessig)',
 bverfg06='[BVerfG, Pressemitteilung 11/2006 – Abschussermächtigung im Luftsicherheitsgesetz nichtig](https://www.bundesverfassungsgericht.de/SharedDocs/Pressemitteilungen/DE/2006/bvg06-011.html)',
 eurlex='[EUR-Lex – Verordnung (EU) 2024/1689 (KI-Verordnung, „AI Act“)](https://eur-lex.europa.eu/eli/reg/2024/1689?locale=de)',
 art2='[Art. 2 VO (EU) 2024/1689 – Anwendungsbereich](https://gesetze.legal/eu/vo_eu_2024_1689/2)',
 sciam='[Scientific American (03/2026): SpaceX reaches milestone of 10,000 Starlink satellites in orbit](https://scientificamerican.com/article/spacex-reaches-milestone-of-10-000-starlink-satellites-in-orbit/)',
 almon='[Al-Monitor (27.01.2026): Rights group says confirmed Iran protest toll over 6,000](https://www.al-monitor.com/originals/2026/01/rights-group-says-confirmed-iran-protest-toll-over-6000)',
 alblack='[Al-Monitor (01/2026): Iran’s internet blackout enters third week](https://www.al-monitor.com/originals/2026/01/irans-internet-blackout-enters-third-week-filtered-access-flickers-back)',
 semafor='[Semafor (14.01.2026): Iranians sidestep internet blackout with SpaceX’s Starlink](https://www.semafor.com/article/01/14/2026/iranians-sidestep-internet-blackout-with-spacexs-starlink)',
 annahar='[Annahar: Iran uses military jamming to block Starlink internet amid protests](https://en.annahar.com/en/business-tech/268938/iran-uses-military-jamming-to-block-starlink-internet-amid-protests)',
 aj53='[Al Jazeera (20.08.2013): CIA admits organising 1953 Iran coup](https://aljazeera.com/news/2013/8/20/cia-admits-organising-1953-iran-coup)',
 ji='[Jewish Insider (29.09.2025): Netanjahu vor US-Influencern zu TikTok-Verkauf und sozialen Medien](https://jewishinsider.com/2025/09/tiktok-sale-netanyahu-american-influencers-israel-jews/)',
 fang='[Lee Fang (28.07.2024): TikTok to ban some criticisms of Zionism](https://www.leefang.com/p/tiktok-to-ban-some-criticisms-of)',
 bpb='[bpb – Geborene und Gestorbene (nach Destatis/GENESIS, Stand 08/2020)](https://www.bpb.de/kurz-knapp/zahlen-und-fakten/soziale-situation-in-deutschland/61559/geborene-und-gestorbene/)',
 destst='[Destatis – Sterbefälle: Auswertung der unterjährigen Sterbefallzahlen seit 2020](https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Bevoelkerung/Sterbefaelle-Lebenserwartung/sterbefallzahlen.html)',
 aest='[Deutsches Ärzteblatt: Weniger Verstorbene gezählt (nach Destatis)](https://www.aerzteblatt.de/news/weniger-verstorbene-gezaehlt-dc3816d1-a74e-4947-9f94-d23e020ec90e)',
 aepfl='[Deutsches Ärzteblatt (18.12.2024): Zahl der Pflegebedürftigen steigt deutlich auf 5,7 Millionen (nach Destatis)](https://www.aerzteblatt.de/themen/pflegebeduerftigkeit/zahl-der-pflegebeduerftigen-steigt-deutlich-auf-57-millionen-baec142a-b2be-453c-98b8-6f6eb28fea4e)',
 rkiprot='[Deutsches Ärzteblatt, 25.3.2024 – RKI-Protokolle nach Klage freigegeben](https://www.aerzteblatt.de/n150239)',
 rkimeld='[Deutsches Ärzteblatt, 21.1.2022 – RKI blickt detaillierter auf COVID-19-Patienten mit Symptomen](https://www.aerzteblatt.de/themen/rki/rki-blickt-detaillierter-auf-covid-19-patienten-mit-symptomen-59b8e066-6c3d-4ab4-9f49-f142b59558b4)',
 sva='[Bericht des Sachverständigenausschusses nach § 5 Abs. 9 IfSG (30.6.2022, PDF)](https://www.bundesgesundheitsministerium.de/fileadmin/Dateien/3_Downloads/S/Sachverstaendigenausschuss/BER_lfSG-BMG.pdf)',
 pei='[PEI: Sicherheitsbericht 27.12.2020–31.03.2023 (Bulletin zur Arzneimittelsicherheit 2/2023)](https://www.pei.de/SharedDocs/Downloads/DE/newsroom/dossiers/sicherheitsberichte/sicherheitsbericht-27-12-20-bis-31-03-23-aus-bulletin-zur-arzneimittelsicherheit-2-2023-s-12-29.pdf?__blob=publicationFile&v=5)',
 nebenw='[nebenwirkungen.bund.de – Meldeportal für Verdachtsfälle](https://nebenwirkungen.bund.de)',
)
def url(k): return Q[k].split('](')[1][:-1]
def tit(k): return Q[k].split('](')[0][1:]

# ---------- Abschnitte (von, bis, Titel, Kurztitel, Thema, Liste) ----------
S = []
def ab(von, bis, titel, kurz, th, *liste):
    S.append((von, bis, titel, kurz, th, list(liste)))

ab('0:00','0:06','🏰 Dritte Runde – Lausen „in der Burg“','Begrüßung, Gewaltenteilung, Dettmar, „in der Burg“','a',
 '**Zusammenfassung:** Der Gastgeber (Name im Video nicht genannt ❓) begrüßt Lausen zur „dritten Runde“ und kündigt an, diesmal weniger über Corona und mehr über KI und eine mögliche Technokratie zu sprechen – Themen, die Lausen zuvor bei einem KI-Kanal („Everlast AI“ ❓) besprochen habe. Lausen sagt, er sitze jetzt „in der Burg“: Als Sachverständiger der Enquete-Kommission könne er die Verantwortlichen befragen. Er erklärt die Gewaltenteilung und deutet die Corona-Politik als Übergriff der Exekutive auf Parlamente und Gerichte.',
 '💬 „Die Exekutive hat ja quasi eine Art Putsch gemacht“ (Lausen) [0:02]',
 '📌 Beispiele: Frank Ulrich Montgomery habe nach einem Gerichtsurteil zu 2G von „kleinen Richterlein“ gesprochen [0:03] ❓ Zitat hier nicht geprüft; der Weimarer Familienrichter Christian Dettmar („Detmer“) habe für zwei Schulklassen die Maskenpflicht aufgehoben und sei „aus dem Dienst geworfen“ worden [0:04] [seine Sicht].',
 '📌 Die Sachverständigen der anderen Seite müssten sich seine Fragen noch anderthalb Jahre anhören; als Beispiel nennt er Michael Müller, früher Regierender Bürgermeister von Berlin [0:05–0:06].',
 '📚 Dettmar wurde 2023 vom LG Erfurt wegen Rechtsbeugung zu zwei Jahren auf Bewährung verurteilt; der BGH bestätigte das am 20.11.2024. Details im Abgleich. Zur Arbeitsweise der Kommission siehe auch {{a:lausen-manova|Manova-Gespräch}}.')
ab('0:06','0:09','🏷️ Kontaktschuld AfD und die Anhörung „morgen“','AfD-Nähe-Vorwurf; Ankündigung Maaßen/Faeser und Zitatliste','a',
 '**Zusammenfassung:** Der Gastgeber fragt nach dem Vorwurf der Kontaktschuld: Lausen und Michael Nehls („Nels“ ❓) säßen im Zeitkontingent der AfD. Lausen sagt, darauf werde er kaum angesprochen; manche dächten es sich aber und werteten seine Aussagen deshalb ab. Er kündigt an, in der Anhörung am nächsten Tag Hans-Georg Maaßen („Marsen“) zu befragen und eine Reihe von Zitaten über Ungeimpfte vorzulesen.',
 '📌 Quelle der Zitate sei das Buch „Ich habe mitgemacht“ (herausgegeben von Burkhard Müller-Ullrich, Kontrafunk ❓). Er nennt Nancy Faeser („Nancy Fer“), Joachim Gauck („Bekloppte“), einen FDP-Politiker („Sozialschädlinge“, Name ❓) und Boris Palmer (Impfpflicht notfalls mit Beugehaft) [0:08–0:09] [seine Sicht].',
 '📚 Die Anhörung vom 29.01.2026 hatte das Verhältnis von Regierungen und Parlamenten zum Thema; geladen waren u. a. Maaßen und Faeser ([hib 78/2026](https://www.bundestag.de/presse/hib/kurzmeldungen-1140476)). Daraus ergibt sich als Aufnahmetag der 28.01.2026.')
ab('0:09','0:12','📋 Lager-Angst und Kontaktnachverfolgung','Kommentare zu Lager-Angst; Kontaktnachverfolgung, Tegnell','b',
 '**Zusammenfassung:** Lausen berichtet von Hunderten Kommentaren unter einem früheren Video („Fair Talk“), in denen Ungeimpfte schrieben, sie hätten zur 2G-Zeit befürchtet, in Lager zu kommen. Deutschland mache Dinge „gerne zu Ende“: Die Kontaktnachverfolgung sei weitergeführt worden, obwohl sie nur am Anfang einer Welle funktioniere. Laut RKI-Protokollen seien die Gesundheitsämter überlastet gewesen; andere Behörden hätten aushelfen und Menschen hinterhertelefonieren müssen.',
 '💬 „Aber die Deutschen machen das zu Ende.“ (Lausen) [0:11]',
 '📌 Anders Tegnell („Technell“), Epidemiologe in Schweden, habe auf Kontaktnachverfolgung bei vielen Fällen verzichtet, weil sie Behörden überfordere [0:11] [seine Sicht].',
 '📚 Das RKI erklärte im Januar 2022, die Meldedaten würden wegen ausgelasteter Testkapazitäten und Gesundheitsämter zunehmend unvollständig ([Ärzteblatt](https://www.aerzteblatt.de/themen/rki/rki-blickt-detaillierter-auf-covid-19-patienten-mit-symptomen-59b8e066-6c3d-4ab4-9f49-f142b59558b4)).')
ab('0:12','0:15','🏛️ Wie die Kommission arbeitet – und wer einlädt','Monatliche Anhörungen, Einladungsregel, „nicht politisch“','a',
 '**Zusammenfassung:** Auf die direkte Frage nach seinem Verhältnis zur AfD erklärt Lausen den Ablauf: Wissenschaftliche Mitarbeiter der Fraktion bereiten auf, was die geladenen Sachverständigen früher gesagt haben; einmal im Monat gebe es eine öffentliche Sitzung mit fünf bis sechs Sachverständigen, bis Juli des nächsten Jahres. Er selbst sei formal von Bundestagspräsidentin Julia Klöckner eingeladen worden, vorgeschlagen von der AfD.',
 '📌 Neu sei, dass veröffentlicht werde, welche Fraktion einen Sachverständigen eingeladen hat – weil manche nicht kämen, wenn die AfD einlädt; das nennt er „Tricksereien“ [0:13] ❓ hier nicht geprüft.',
 '📌 Er sei nicht politisch im Sinne von Landes- oder Bundespolitik; außer Corona äußere er sich nur zur Windkraft, die er „ein riesen Geschäftsmodell“ nennt [0:14]. Wenn ihn etwas interessiere, bitte er AfD-Abgeordnete, eine Anfrage an die Bundesregierung zu stellen [0:14–0:15].',
 '📚 Die AfD-Fraktion entsendet drei Abgeordnete und drei Sachverständige ([hib 394/2025](https://www.bundestag.de/presse/hib/kurzmeldungen-1107614)); siehe Diagramm im Abgleich.')
ab('0:15','0:18','🎯 „Eine Jagd“ – Spahn widerspricht','Ausgrenzung Ungeimpfter; Spahn weist „Jagd“ zurück','a',
 '**Zusammenfassung:** Corona sei eigentlich ein Gesundheitsthema, kein politisches. Ungeimpfte seien beleidigt, ausgegrenzt, bedroht und stigmatisiert worden, auch innerhalb von Familien; viele hätten sich dabei im Recht gefühlt. Lausen nennt das „eine Jagd“ und zitiert eine Journalistin (Name im Transkript „Bianca Blomenkamp“ ❓) mit einem Satz über Gewalt gegen Ungeimpfte.',
 '📌 In der Kommission habe er Jens Spahn gesagt, mit der „Pandemie der Ungeimpften“ habe er eine Jagd gestartet; Spahn habe das zurückgewiesen, im Saal sei Beifall geklopft worden [0:17–0:18] [seine Sicht].',
 '📌 Er befürchtet, dass der Abschlussbericht für die nächste Krise schnellere Gesetze, Lockdowns, Masken und Impfpflichten vorbereitet [0:18].',
 '📚 Mitschnitt der Anhörung mit Spahn: [Bundestag-Mediathek, 15.12.2025](https://www.bundestag.de/mediathek/video?videoid=7646762) ❓ Wortwechsel hier nicht nachgeprüft.')
ab('0:18','0:21','👵 Besuchsverbote und Pflege Dementer','Pflegeregeln, Besuchsverbote, Tegnell; Netflix-Doku','b',
 '**Zusammenfassung:** Lausen beschreibt, wie empfindlich Demenzkranke auf Veränderungen reagieren: Pflegende sollten nicht wechseln, nicht einmal ein anderes Parfüm tragen. Lockdowns, Besuchsverbote und Schutzkittel hätten deshalb großen Schaden angerichtet. Der Gastgeber verweist auf eine Netflix-Doku über Regionen mit vielen sehr alten Menschen: Lebenssinn und soziale Umgebung seien dort entscheidend.',
 '💬 „alleine diese Besuchsverbote haben garantiert tausenden Menschen das Leben gekostet“ (Lausen) [0:20]',
 '📌 Tegnell habe Besuchsverbote im Nachhinein einen Fehler genannt; das Virus sei eher durch Pflegekräfte eingetragen worden [0:19–0:20] ❓ Aussage hier nicht geprüft.',
 '📚 Der Sachverständigenausschuss nach § 5 Abs. 9 IfSG stellte 2022 fest, dass keine ausreichende begleitende Datenerhebung zu den Maßnahmen aufgebaut wurde ([Bericht](https://www.bundesgesundheitsministerium.de/fileadmin/Dateien/3_Downloads/S/Sachverstaendigenausschuss/BER_lfSG-BMG.pdf)); belastbare Zahlen zu Todesfällen durch Besuchsverbote liegen hier nicht vor ❓.')
ab('0:21','0:24','🇮🇹 Bergamo, Spanien und Drostens „Kosten“','Bergamo, Pflegeheime in Spanien, Drosten und Antes','b',
 '**Zusammenfassung:** Für Lausen ist die wichtigste Frage nicht die nächste Pandemie, sondern ob alte Menschen durch die Maßnahmen zu Tode kamen; er wählt dafür das Wort „hingerichtet“. Er war in Bergamo; dort seien in sechs Wochen rund 6.000 Menschen mehr gestorben, gleichzeitig wie an anderen Orten in Europa und in New York, danach nicht mehr. Danach seien die Maßnahmen das größte Problem gewesen.',
 '📌 In Spanien hätten Soldaten der Einheit UME beim Desinfizieren Tote in verlassenen Pflegeheimen gefunden; staatsanwaltschaftliche Ermittlungen seien eingestellt worden [0:23] ❓ hier nicht geprüft.',
 '📌 Er habe Christian Drosten gefragt, ob die Maßnahmen zusätzliche Tote forderten; Drosten habe das bejaht. Auch Gerd Antes ❓ sage, alle Maßnahmen hätten „Kosten“ gehabt [0:23–0:24] [seine Sicht].',
 '🔗 Zu Bergamo und den Klinikzahlen siehe {{a:lausen-fragen|Vortrag „Fragen bleiben“}}.')
ab('0:24','0:27','✈️ Luftsicherheitsurteil und mutlose Gerichte','„Hinrichtung“-Frage, Luftsicherheitsurteil, Gerichte','c',
 '**Zusammenfassung:** Lausen meint, Drosten sehe Todesfälle als „Kosten“ gegenüber geretteten Leben; das sei eine bloße Behauptung, die man sich in der Kommission gegenseitig erzähle. Der Gastgeber fragt, ob „Hinrichtung“ nicht Mord mit Vorsatz bedeute. Lausen verweist auf das Urteil zum Luftsicherheitsgesetz: Ein Leben dürfe nicht gegen viele abgewogen werden.',
 '📌 Begegnung im Gang: Eine Grünen-Abgeordnete und Ärztin („Frau Pichotta“, vermutlich Paula Piechotta ❓) habe seinen Gruß nicht erwidert [0:24].',
 '📌 Gerichte: Bewegung komme von den Amtsgerichten; viele Richter würden gern anders entscheiden, wüssten aber vom Fall Dettmar; die Gerichte hätten meist nur Formales geprüft, nicht die Verhältnismäßigkeit [0:26–0:28] [seine Sicht].',
 '📚 Das BVerfG erklärte am 15.02.2006 die Abschussermächtigung im Luftsicherheitsgesetz für nichtig ([Pressemitteilung](https://www.bundesverfassungsgericht.de/SharedDocs/Pressemitteilungen/DE/2006/bvg06-011.html)).')
ab('0:27','0:30','🧾 Rechtsbeugung, Maskenatteste und Kennedy','Dettmar vor BGH/BVerfG; Kennedy-Brief an Warken','c',
 '**Zusammenfassung:** Im Fall Dettmar habe der BGH nach Lausens Lesart die Schwelle für Rechtsbeugung gesenkt, weil Vorsatz nicht mehr nachgewiesen werden müsse – er betont, das sei seine Interpretation als Laie. Dann kommt er auf Verfahren gegen Ärzte wegen Maskenattesten: Der US-Gesundheitsminister Robert F. Kennedy Jr. habe dazu einen Brief an Bundesgesundheitsministerin Nina Warken geschrieben und ein Video auf X veröffentlicht.',
 '📌 Lausen deutet Kennedys Schritt als Sorge der Amerikaner vor einer erneuten Entgleisung Deutschlands; der Gastgeber fragt nach einer Anspielung auf das „Dritte Reich“ und sagt, die USA sollten aufhören, das zu finanzieren [0:28–0:30]. Später stellt Lausen klar, das sei seine Deutung, Kennedy habe sachlich formuliert [0:38].',
 '📚 LTO: Der BGH stützte das Urteil auf bewusste, elementare Rechtsverstöße; eine Absenkung der Vorsatzanforderungen wird dort nicht berichtet. Kennedys Brief und Video stammen vom 10./11.01.2026 ([ZDFheute](https://www.zdfheute.de/politik/ausland/faktencheck-kennedy-gesundheitssystem-deutschland-corona-strafverfahren-100.html)).')
ab('0:30','0:33','📨 Warken, Verfahrenszahlen und Merkel als Gast','Warken-Antwort, Attest-Verfahren, Merkel','c',
 '**Zusammenfassung:** Warken habe Falschinformationen verbreitet, indem sie die Verfahren als Betrug und Urkundenfälschung darstellte; ein Arzt, der ein Attest ausstellt, fälsche keine Urkunde. Lausen hat nach eigener Aussage Zahlen der meisten Generalstaatsanwaltschaften: Verfahren wegen unrichtiger Gesundheitszeugnisse habe es vorher kaum gegeben, 2020/21 dann massiv – „wie in Bergamo“.',
 '📌 Gegen Warkens Aussage sei anwaltlich vorgegangen worden; den Stand kenne er nicht [0:30] ❓.',
 '📌 Auf die Frage nach Spahn, Drosten und Lauterbach: Lauterbach interessiere ihn „gar nicht so“; Angela Merkel komme „im Februar oder März“ – freiwillig [0:31–0:32] ❓ Termin hier nicht geprüft.',
 '📚 Das BMG schrieb am 10.01.2026, verfolgt würden ausschließlich Betrug und Urkundenfälschung, etwa „falscher Impfpässe oder unechter Maskenatteste“. ZDFheute ordnet ein: Für Ärzte gilt § 278 StGB (unrichtige Gesundheitszeugnisse); eine zentrale Statistik der Verfahren gibt es nicht.')
ab('0:33','0:36','🔬 Das Experiment: Fakten über anderthalb Jahre','Hoffnung, Live-Bild, Anti-AfD-Video','a',
 '**Zusammenfassung:** Spahn sage offen, was er denke; die anderen seien „schwieriger“. Lausen trage keine Hoffnungen vor sich her, sondern tue, was er spüre. Im Saal höre man mehr als im Live-Bild, das nur den Sprechenden zeigt. Ihn interessiere, ob sich Fakten über anderthalb Jahre „durchfressen“, auch bei Leuten, die nichts wissen wollen.',
 '💬 „geht es, dass du sowas über anderthalb Jahre … abwehren kannst“ (Lausen) [0:34]',
 '📌 Der Gastgeber erwähnt ein Video eines Anti-AfD-Kanals mit rund 600.000 Aufrufen, das AfD-Vertreter in der Kommission vorführe; Lausen und Nehls („Dr. Nilson“ ❓) kämen darin nicht vor [0:35] ❓.',
 '📌 Der Gastgeber fasst seine Sicht zusammen: Parlamentarismus sei „nicht so wichtig“, Politik spiele mit der Wirtschaft „unter der Kontrolle der Bankenmafia“ [0:35] [seine Sicht].')
ab('0:36','0:39','🤝 „Fake-Opposition“? – die menschliche Ebene','AfD als Opposition, menschliche Ebene, ICE','a',
 '**Zusammenfassung:** Der Gastgeber fragt, ob die AfD eine „aufgebaute Fake-Opposition“ sein könne, die von Lausens Glaubwürdigkeit profitiere. Lausen antwortet, für ihn zähle die menschliche Ebene: Die Leute, mit denen er dort arbeite, seien „völlig in Ordnung“; mit schlimmen Leuten würde er nicht zusammensitzen. Er frage sie auch, was passiere, wenn die AfD an der Macht wäre.',
 '📌 Er habe auf der Herfahrt bei „Lion Media“ einen Beitrag über die US-Einwanderungsbehörde ICE gesehen; wenn das das politische Muster sei, lehne er es ab [0:37–0:38].',
 '📌 Das Video von Kennedy habe er übersetzt und auf seinem Kanal hochgeladen (Name im Transkript „Brüderle TV“ ❓); Amerikaner wollten nicht mit „ideologisierten Ländern“ arbeiten [0:38–0:39] [seine Sicht].')
ab('0:39','0:42','🎙️ Gastgeber: Wall Street, Präzedenzfall und Stillstand','Thesen des Gastgebers; Fiat-Geld und Systemwechsel','g',
 '**Zusammenfassung:** Der Gastgeber widerspricht: ICE erinnere ihn an die SA; die Kennedys hätten ihr Geld mit Opiumgeschäften gemacht; die Nationalsozialisten seien aus der Wall Street finanziert worden; Corona sei der Präzedenzfall gewesen, dass man „den Globus gleichschalten“ könne. Er verweist auf den Fall Epstein und beschreibt ein Gefühl von Stillstand in Spielen, Filmen und Musik – „Ruhe vor dem Sturm“.',
 '📌 Alle Aussagen dieses Abschnitts sind die Sicht des Gastgebers [0:39–0:41] ❓ (Opium-, Wall-Street-These hier nicht geprüft).',
 '📌 Lausen stimmt dem Gefühl eines Systemwechsels zu: Die Schulden im „Fiat-Schuldgeldsystem“ würden so hoch, dass etwas Neues kommen müsse [0:41–0:42] [seine Sicht].')
ab('0:42','0:45','🔲 QR-Code, Grenzkabine und Musks Raketen','Digitaler Euro, QR-Code/ID2020, EasyPASS, Musk','d',
 '**Zusammenfassung:** Nach Bitcoin kämen digitaler Euro und digitales Zentralbankgeld (CBDC). Lausen habe gehört, der QR-Code für Impfpässe sei 2018 von ID2020 entwickelt worden, einer laut ihm von Microsoft gegründeten Organisation – das habe er „noch nicht recherchiert“. Ein Schlüsselerlebnis: Bei der Rückkehr aus der Türkei habe in Hamburg eine Maschine in einer Kabine über die Einreise entschieden.',
 '💬 „das ist die Richtung, in die das geht“ (Lausen) [0:43]',
 '📌 Elon Musk dürfe schon unter den Demokraten Raketen starten; wer das dürfe, sei weder rechts noch links, sondern „Teil … des neuen Systemkäfigs“ [0:43–0:44] [seine Sicht]. Er selbst dürfe mit seiner Drohne nur 100 m hoch.',
 '📌 Musk habe rund 8.000 Satelliten im All und wolle 40.000; auch Russland, China, EU, Indien/Großbritannien und Amazon („über 1000“ ❓) bauen Netze [0:44–0:45].')
ab('0:45','0:48','🛰️ Satelliten als Käfig – Starlink in der Ukraine','Internet of Things, Tracking, „Käfig“, Ukraine','d',
 '**Zusammenfassung:** Die Satelliten sollen Internet an jedem Ort sichern – für das „Internet of Things“, also auch, um Menschen mit ID, Code oder Chip überall verfolgen zu können. Ihre Überflüge seien völkerrechtlich geregelt; trotzdem habe die Bild-Zeitung über russische Satelliten über Europa geschlagzeilt. Viele Tausend Satelliten um die Erde sähen aus wie ein Käfig – damit sei man beim Transhumanismus.',
 '📌 In der Ukraine hätten sich Russen Starlink-Geräte besorgt; die seien dann gezielt abgeschaltet worden [0:47] [seine Sicht].',
 '📚 SpaceX meldete im März 2026 10.000 Starlink-Satelliten im Orbit ([Scientific American](https://scientificamerican.com/article/spacex-reaches-milestone-of-10-000-starlink-satellites-in-orbit/)) – nach dem Gespräch.')
ab('0:48','0:51','🇮🇷 Gastgeber: Iran, Opferzahlen und Starlink','Iran-Proteste aus Sicht des Gastgebers; Krieg im All','g',
 '**Zusammenfassung:** Der Gastgeber schildert die Proteste im Iran: Die gemeldeten Todeszahlen seien von 500 über 2.500 und 12.000 auf 20.000 gestiegen, manche hätten 40.000 genannt; das vergleicht er mit Tagesverlusten im Zweiten Weltkrieg, in Gaza und im Golfkrieg und hält es für Propaganda. Er sieht ausländische Geheimdienste am Werk („Regime Change“ wie Operation Ajax), nennt Mike Pompeo und meint, Starlink sei bereitgestellt worden, damit sich „terroristische Zellen“ vernetzen; Iran habe Starlink mit russischer und chinesischer Hilfe gestört [0:48–0:50] [seine Sicht].',
 '📌 Lausen: Im All würden künftig Kriege geführt; die Bundeswehr werde vor allem Mess- und Verfahrenstechnik liefern [0:50–0:51].',
 '📚 Eine Menschenrechtsgruppe zählte bis 27.01.2026 über 6.000 bestätigte Tote ([Al-Monitor](https://www.al-monitor.com/originals/2026/01/rights-group-says-confirmed-iran-protest-toll-over-6000)); Internetsperre und Störung von Starlink sind berichtet (siehe Abgleich). Die CIA räumte 2013 ihre Rolle beim Putsch 1953 ein ([Al Jazeera](https://aljazeera.com/news/2013/8/20/cia-admits-organising-1953-iran-coup)).')
ab('0:51','0:54','🥇 AI Act, „rumregenauern“ und Goldpreis','AI Act, Zuversicht, Gold/Silber, Vorräte','d',
 '**Zusammenfassung:** Den europäischen AI Act ordnet Lausen in den Aufbau eines „Käfigs“ ein (er nennt 2020 als Beschlussjahr). Er wolle aber nicht „rumwolfen und rumregenauern“, wie sein bester Freund sagt – also keine düsteren Szenarien malen. Er sei zuversichtlich: Manches werde nicht funktionieren, weil die Menschen ihre Zustimmung entziehen, und man werde an Intelligenz gewinnen.',
 '📌 Gold und Silber hätten sich in kurzer Zeit vervier- bis verfünffacht; das zeige weniger, dass Gold mehr wert sei, als dass Währungen an Wert verlieren [0:52] [seine Sicht] ❓ Faktor hier nicht geprüft.',
 '📌 „Zwischentipp“: Vorräte anlegen, eine Petroleumheizung und eventuell einen Generator bereithalten – mit Hinweis auf den Stromausfall in Berlin [0:53–0:54].',
 '🔗 Gemeint ist u. a. {{a:regenauer|Tom-Oliver Regenauer (A-11)}}. 📚 Die KI-Verordnung ist die Verordnung (EU) 2024/1689 von 2024 (siehe Abgleich).')
ab('0:54','0:58','🕯️ Zukunftsbilder und die IQ-Frage','„Schwarzmagier“-These, IQ 90–150, KI als Akteur','e',
 '**Zusammenfassung:** Der Gastgeber meint, Zukunft entstehe aus den Gedanken der Bevölkerung; wer diese manipuliere, kontrolliere die Realität. Lausen setzt dagegen: Die künstliche Intelligenz sei ein neuer Akteur. Gemessen am IQ – den er nur als ein Messverfahren gelten lässt – liege der Mensch seit Jahrhunderten bei etwa 90 bis 150, ohne wesentlichen Fortschritt oder Rückgang.',
 '📌 Der Freund könne nach einem früheren Auftritt von Lausen nicht schlafen; Lausen: Vorräte seien „gar kein Wolfen“ [0:54–0:55].')
ab('0:58','1:03','💬 KI als Denkfabrik – und analogfreedom.eu','KI ohne Groll; überrumpelte Ministerpräsidenten; analogfreedom.eu','e',
 '**Zusammenfassung:** Mit Menschen stoße man in Gesprächen an Grenzen, über die einer nicht hinweg will; eine KI höre nicht auf und reagiere ohne Groll. So könne jeder eine eigene „Denkfabrik ohne Tabus“ betreiben und sich gedanklich auf neue Systeme vorbereiten. Die Ministerpräsidenten seien 2020 von Merkel und Drosten „überrumpelt“ worden – so schreibe es Spahn ❓ –, weil sie nie solche Denkprozesse geübt hätten.',
 '💬 „Denkfabriken zu gründen ohne Tabus“ (Lausen) [0:59]',
 '📌 Er habe die Seite analogfreedom.eu mit dem Vorschlag für ein „analoges Zugangsgrundrecht“ gestaltet; schon das Lesen erweitere das Bewusstsein. Eine große Bewegung wolle er nicht [1:01–1:02] ❓ Seite hier nicht geprüft.',
 '📌 Systemwechsel habe es immer gegeben – Kaiserzeit, Wirtschaftswunder; jetzt komme ein neues System, das man nicht so annehmen müsse [1:02–1:03] [seine Sicht].')
ab('1:03','1:06','🚪 Recht auf Ausstieg – analoge Treffen, Chip und Bratwurst','Ausstiegsrecht, analoge Treffen, Chip-Entscheidung','e',
 '**Zusammenfassung:** Kern seines Vorschlags: Wer bei der Digitalisierung mitmacht, soll ohne Nachteile wieder aussteigen dürfen – dauerhaft oder zeitweise. Am Anfang könne das ein Recht auf analoge Treffen sein, an Orten ohne Handy; dann auch ohne Menschen mit Chip. Wenn etwa ein Chip von Musk ins Gehirn kommen solle, werde es wieder Anreize geben wie bei der Corona-Impfung („noch eine Bratwurst“).',
 '📌 Der Gastgeber wendet ein, in einem totalitären System bekomme man vielleicht gar keine Wahl; Lausen rechnet damit nicht, weil Macht Zustimmung brauche [1:05–1:06].')
ab('1:06','1:09','🗳️ Zustimmung als Machtquelle – Erziehung, Glaube, Harari','COSMO-Umfragen, Sozialisierung, Glaube, Harari','e',
 '**Zusammenfassung:** Macht funktioniere nur mit Legitimation, also Zustimmung. In der Corona-Zeit habe man mit Befragungen von Cornelia Betsch (Uni Erfurt, COSMO) gemessen, ob die Menschen die Maßnahmen noch mittragen. Der Gastgeber nennt Sozialisierung, Erziehung und Glaube als Grundpfeiler; ein totalitäres System sei unnötig, wenn Menschen freiwillig mitmachen.',
 '📌 Gastgeber: Handys hörten mit; John Kiriakou („Kirako“ ❓) habe vom Abhören über Fernseher erzählt; Kinder würden früh von der Familie getrennt; soziale Medien sozialisierten global [1:07–1:08] [seine Sicht].',
 '📌 Gastgeber: Yuval Noah Harari preise beim Weltwirtschaftsforum die KI als künftigen Gottersatz [1:08] ❓ Wortlaut hier nicht geprüft. Kurzer Scherz über Klimaprognosen („Mutativ“, vermutlich Mojib Latif ❓) [1:09].')
ab('1:09','1:12','🧠 „IQ von 1000“ – KI als Werkzeug für Dokumente','Leistungssprung der KI; Kritik des Gastgebers','e',
 '**Zusammenfassung:** Lausen schätzt, dass heutige KI in den meisten Bereichen einen „IQ von 1000“ habe, später 4.000 bis 5.000. Lade man mehrere Dokumente oder Bücher mit Hunderten Seiten hoch, bekomme man in Sekunden klare Antworten; auch Rechenfehler früherer Versionen seien behoben. Es komme darauf an, sehr konkret zu arbeiten, mit genauen Vorlagen und Dokumenten.',
 '💬 „Die KI hat ein IQ von 1000 und labert nur …“ (Gastgeber, ironisch) [1:10]',
 '📌 Der Gastgeber hält dagegen: Bei Politik und Geschichte müsse er die KI ständig korrigieren; noch 2023 habe sie die Impfung „wirksam und sicher“ genannt [1:13] [seine Sicht].',
 '📚 Zur Sicherheit der Impfstoffe siehe den Abgleich (PEI); bei Verdacht auf Nebenwirkungen: ärztlich abklären lassen und über nebenwirkungen.bund.de melden.')
ab('1:12','1:15','🧭 Detmold-Versuch – und der Gastgeber zu Israel und TikTok','Vortrag in Detmold, Vertrauen in KI; Gastgeber zu Netanjahu/TikTok','e',
 '**Zusammenfassung:** Bei einem Vortrag in Detmold („Deadmold“) vor knapp 400 Menschen habe Lausen Dokumente von EU und Bundesrat mit KI ausgewertet; alle seien von der Geschwindigkeit fasziniert gewesen. Menschen folgten dem, der Antworten hat – bis er einen Fehler macht und das Vertrauen verliert.',
 '📌 Der Gastgeber sagt, Netanjahu und die israelische Regierung hätten erklärt, das Training von OpenAI und anderen zu beeinflussen und „Antizionismus“ herauszutrainieren; bei TikTok falle „Zionismus“ unter Hassrede und „Epstein“ könne man bald nicht mehr eingeben; KI sei ein Werkzeug der „Machtelite“ [1:13–1:15] [seine Sicht].',
 '📚 Belegt ist: Netanjahu nannte im September 2025 soziale Medien eine der wichtigsten „Waffen“ und den TikTok-Verkauf den wichtigsten laufenden Kauf ([Jewish Insider](https://jewishinsider.com/2025/09/tiktok-sale-netanyahu-american-influencers-israel-jews/)). TikToks Hassrede-Regel betrifft „Zionist“, wenn das Wort als Ersatz für Juden oder Israelis benutzt wird, nicht als Bezeichnung einer politischen Ideologie ([Lee Fang](https://www.leefang.com/p/tiktok-to-ban-some-criticisms-of)). Zu OpenAI fand sich kein Beleg ❓.')
ab('1:15','1:18','🤖 Filter, Schmeichelei und humanoide Roboter','Steuerbarkeit der KI, Robotik, Filmbezüge','e',
 '**Zusammenfassung:** Lausen ist bei der „Elitensteuerung“ weniger überzeugt: Entwickler sagten, sie wüssten selbst nicht mehr genau, was herauskommt. Das sieht er daran, dass man der KI die Schmeichelei („tolle Frage“) kaum abtrainieren konnte – Filter funktionierten also nur begrenzt. KI sei ein neuer „Player“, der in die reale Welt kommt: fahrerlose Autos gebe es schon, humanoide Roboter kämen in etwa zwei Jahren auf die Straße, zuerst kleine um 1,30 m.',
 '📌 Filmbezüge: I, Robot, Terminator, Blade Runner und „Der Rasenmähermann“ (Lausen schwankt beim Jahr: 82, 86 oder 93 ❓) [1:17].')
ab('1:18','1:21','🎞️ Animatrix, Kriegsroboter und der AI Act','Gastgeber zu Animatrix; Anduril, Palantir; AI Act','e',
 '**Zusammenfassung:** Der Gastgeber erzählt eine Episode aus „Animatrix“: Ein Haushaltsroboter begeht einen Mord, Menschen greifen Roboter an, die KI wehrt sich und will die Menschheit auslöschen. Roboter, die töten, werde es jetzt im Krieg geben – er nennt Anduril und Palantir.',
 '📌 Gastgeber: Der AI Act sehe vor, Gelder aus Forschung, Wissenschaft und Kunst in KI-Projekte umzuleiten und massiv aufzurüsten [1:20–1:21] [seine Sicht] ❓.',
 '📚 Die KI-Verordnung gilt laut Art. 2 Abs. 3 nicht für KI-Systeme, die ausschließlich für militärische, Verteidigungs- oder nationale Sicherheitszwecke genutzt werden ([Art. 2](https://gesetze.legal/eu/vo_eu_2024_1689/2)); eine Umschichtung von Fördergeldern war darin hier nicht zu finden ❓.')
ab('1:21','1:24','🏧 Glühwein-Bargeld und die Zukunftsvision des Gastgebers','Corona aufarbeiten; Bargeld-Schlange; Harari-Szenario','f',
 '**Zusammenfassung:** Lausen: Corona müsse zu Ende aufgearbeitet werden, damit ein Erkenntnisgewinn für alle entsteht. Manchmal sei er hoffnungslos – etwa vor einer langen Schlange am Geldautomaten der Hamburger Sparkasse am Jungfernstieg, weil Leute für Glühwein Bargeld brauchten.',
 '📌 Der Gastgeber zeichnet ein Zukunftsbild: Roboter ersetzen Familie und Betreuung, KI wird Gottersatz, die „Unterschicht“ wird mit Drogen und Videospielen „stillgelegt“, wie Harari sage ❓; bei Grundeinkommen ohne Hunger, aber von oben regiert [1:22–1:24] [seine Sicht].')
ab('1:24','1:30','📉 „Strömungsabriss“, Pillenknick und Rente','Publikum ab 45; Kinder; Pillenknick, Rente','f',
 '**Zusammenfassung:** Lausen will über Zeiträume reden (bis 2030, danach). Bei seinen Vorträgen säßen fast nur Menschen ab 45 – ein „Strömungsabriss“ zu den Jüngeren, den er nicht erklären kann. Seine eigenen Kinder (30 und 28) seien klug und gut informiert, kämen aber nie zu Veranstaltungen.',
 '📌 Er verbindet das mit dem Pillenknick: Nach den geburtenstarken Jahrgängen „bis 1967“ seien weniger Kinder geboren worden; diese müssten nun die Renten tragen – „das kann gar nicht funktionieren“; ebenso in Japan und China [1:28–1:30] [seine Sicht].',
 '📚 Den Höchststand an Geburten gab es 1964 mit 1,357 Mio.; 1975 waren es 782.000 ([bpb nach Destatis](https://www.bpb.de/kurz-knapp/zahlen-und-fakten/soziale-situation-in-deutschland/61559/geborene-und-gestorbene/)); siehe Diagramm.')
ab('1:30','1:33','🦾 Pflegebedarf und Pflegeroboter','Pflegewelle; kein Pflegeroboter in drei Jahren','f',
 '**Zusammenfassung:** Viele aus den starken Jahrgängen würden pflegebedürftig; Pflege sei teuer und belastend, ob im Heim oder als 24-Stunden-Betreuung zu Hause wie in Italien. „100 Millionen“ Menschen verließen in den nächsten Jahren den Arbeitsmarkt (Bezug unklar ❓). Ohne Robotik werde es nicht gehen, sagt Lausen auf Nachfrage – aber in den nächsten drei Jahren werde kein Pflegeroboter einen alten Menschen berühren dürfen, weil schon das Anheben zu Verletzungen führen könne.',
 '📌 Der Gastgeber vergleicht das mit frühen Flugversuchen à la Leonardo da Vinci; Lausen widerspricht: So werde es nicht kommen [1:32–1:33].',
 '📚 Ende 2023 waren in Deutschland knapp 5,7 Mio. Menschen pflegebedürftig, 86 % wurden zu Hause versorgt ([Ärzteblatt nach Destatis](https://www.aerzteblatt.de/themen/pflegebeduerftigkeit/zahl-der-pflegebeduerftigen-steigt-deutlich-auf-57-millionen-baec142a-b2be-453c-98b8-6f6eb28fea4e)); siehe Diagramm.')
ab('1:33','1:39','⏳ Zeiträume, KI-Götter und wer die Technik kontrolliert','Unterscheidbarkeit, Unterwerfung; KI-Musik; Kontrolle','e',
 '**Zusammenfassung:** Roboter und Menschen werde man wohl noch etwa zehn Jahre unterscheiden können, im Film vielleicht nur noch wenige Jahre. Lausen will sich keine Angst vor ausgedachten Zukünften machen lassen. Ob es schlimm wäre, wenn eine KI die Religion ersetzt? Der Gastgeber: Das sei dasselbe wie in den letzten 2.000 Jahren, „eine Maske ab, die andere rauf“.',
 '💬 „Diese Unterwerfung ist die freiwillige Zustimmung“ (Lausen) [1:35]',
 '📌 Lausen: Das Bauchgefühl gegenüber Robotern werde bei vielen verschwinden – bis ein Update kommt und der Roboter etwa alle mit blauen Augen festnimmt [1:36].',
 '📌 Gastgeber: KI-Musik sei teils interessanter als generischer Pop; Pflegeroboter wären besser als Pflegende, die Alte misshandeln – entscheidend sei aber, wer die Technik kontrolliert; viele AfD-Mitglieder seien „herzensgute Menschen“, an der Spitze der „Pyramide“ gehe es um Macht [1:36–1:39] [seine Sicht].')
ab('1:39','1:45','🏚️ Das „globale Abrissteam“','Abriss, selbst hinfahren, Plünderung, Neubau-Bild','f',
 '**Zusammenfassung:** Lausen nennt die Gegenwart einen Abriss durch ein „globales Abrissteam“ – Energieversorgung in Europa, ICE, Gaza. Das Internet hätte Einblicke in andere Länder geben können; tatsächlich wisse man wenig, Nachrichten seien „nachgerichtet“. Er könne nur glauben, was er selbst prüft, wie in Bergamo; Reporter wie Billy Six seien hingefahren (2014, Flug „MH14“ = MH17 ❓).',
 '💬 „Abriss ist immer mit Plünderung verbunden.“ (Lausen) [1:43]',
 '📌 Nach dem Abriss werde es wieder besser; das Neue sehe „schick“ aus, habe aber Nachteile – wie ein dichter Neubau, in dem die Augen austrocknen. Den Goldpreis sieht er als Signal für das Ende des Abrisses [1:43–1:45] [seine Sicht].')
ab('1:45','1:48','⚡ Energie-Abriss, Kriegsangst und das Corona-Muster','Energie, Militarisierung, „vorgegaukelt“','f',
 '**Zusammenfassung:** Abgerissen werde die Energieversorgung: Kohlekraftwerke, die „gerade sieben Jahre alt“ seien ❓, Atomkraftwerke, Nord Stream; Windräder würden aufgestellt, aber nicht angeschlossen. Der Gastgeber fragt, ob Deutschland in einen Krieg gegen Russland getrieben werden soll. Lausen: Ein Abriss brauche Zustimmung – sonst Krieg, damit die Menschen danach das Neue wollen.',
 '📌 2020 habe in seinen Vorträgen niemand jemanden gekannt, der an Corona gestorben sei; ähnlich könne auch ein Krieg „vorgegaukelt“ sein; das Muster sei, Menschen etwas zu zeigen und ihnen Angst zu machen [1:46–1:48] [seine Sicht].',
 '📚 Destatis verzeichnete im Dezember 2020 32 % mehr Sterbefälle als im Mittel der Vorjahre ([Destatis](https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Bevoelkerung/Sterbefaelle-Lebenserwartung/sterbefallzahlen.html)); siehe Diagramm.')
ab('1:48','1:51','🚚 Bergamo-Lastwagen und Angstpolitik','Corona als Experiment; Militärlaster; spalten und herrschen','b',
 '**Zusammenfassung:** Corona sei weltweit drei bis fünf Jahre lang ein Live-Experiment gewesen: Wer macht wie lange mit, was ist dafür nötig. Die Bilder der Militärlastwagen in Bergamo seien logisch erklärbar: In Italien stürben täglich rund 2.000 Menschen, etwa die Hälfte zu Hause; wenn Bestatter wegen Infektionsrisiko nicht durften, musste die Armee die Toten holen [1:48–1:49] [seine Sicht] ❓.',
 '📌 Der Gastgeber verweist auf ein Gespräch mit Wolfgang Wodarg („Wodak“) über Übersterblichkeit [1:49]; beide sehen Angstpolitik als Mittel, zu spalten und zu herrschen [1:50–1:51].',
 '🔗 Mehr zu Bergamo und Klinikdaten: {{a:lausen-fragen|Vortrag „Fragen bleiben“}}.')
ab('1:51','1:54','🅰️ Optionen A bis D und Rüstung als Geschäftsmodell','Szenarien des Gastgebers; Lausens Variante D','f',
 '**Zusammenfassung:** Der Gastgeber nennt Optionen: A – Abriss durch großen Krieg und Neuaufbau (er nennt Gaza und Pläne für einen „Urlaubsort“), B – kalter Krieg mit Dauerangst, C – eine gebildetere Bevölkerung mit höherem Bewusstsein. Lausen hofft auf C, erwartet aber D: ein „virtuelles“ Ereignis, das mit wenigen echten Bildern beginnt und dann durch Dauerbeschallung Zustimmung erzeugt.',
 '💬 „Man wird ein virtuelles Ereignis erschaffen“ (Lausen) [1:52]',
 '📌 Die Aufrüstung der Bundeswehr sei vor allem ein Geschäftsmodell: Verfügbares Geld werde genommen [1:53] [seine Sicht].')
ab('1:54','1:57','🙋 Schlusswort: selbst mit KI Drucksachen prüfen','Lausens Appell; Gastgeber zu eigenen KI-Abos','e',
 '**Zusammenfassung:** Zur Frage, wie man ihn unterstützen kann: Er brauche keine Hilfe, Teams könne er nicht bilden. Jeder solle selbst mit KI arbeiten – etwa den Drucksachen-Server des Bundestages nutzen und prüfen, was die Bundesregierung zu Windkraft, KI oder anderen Themen tut oder nicht tut. Wenn zehn Prozent der Zuschauer das tun, sei allen geholfen.',
 '📌 Der Gastgeber stellt klar, er sei kritisch gegenüber KI als „Kerngeflecht“ von Transhumanismus und Technokratie, nutze sie aber selbst intensiv (Google AI Ultra, ChatGPT Plus, Leonardo AI); er wolle nicht wie die Gegner von Bob Dylans E-Gitarre oder des Drumcomputers reagieren [1:55–1:57].',
 '🔗 Lausens Methode, Dokumente mit KI auszuwerten, siehe auch {{a:lausen-manova|Manova-Gespräch}}.')
ab('1:57','2:03','📚 „Uniformation“ und Bücher besitzen','KI-Einheitsbrei; Dokumente statt Plaudern; physische Medien','f',
 '**Zusammenfassung:** Der Gastgeber erzählt von einem Vortrag, der für ihn „tot“ war, als er erfuhr, dass er mit KI geschrieben war. Lausen: Wenn alle so formulieren, entstehe ein sprachlicher Einheitsbrei – aus Information werde „Formation“; er warnt, man müsse spüren lernen, was nicht echt ist. Sein Rat: mit der KI Dokumente und Bücher untersuchen, nicht plaudern; wer falsche Antworten bemerkt, vertraue ihr ohnehin nicht mehr.',
 '💬 „Dann haben wir bald Uniformation.“ (Gastgeber) [1:59]',
 '📌 Schlussappell des Gastgebers: Streaming und E-Books entwerteten Besitz, Anbieter hätten Stellen aus Filmen und Kindle-Texten entfernt ❓; „nichts besitzen und glücklich sein“ schreibt er Harari zu ❓. Er rät, Bücher, Filme und Platten zu kaufen und sich analog zu treffen [2:00–2:02] [seine Sicht].')

# ---------- Themen ----------
THEMEN = [{"k":"a","n":"Enquete-Kommission & AfD"},{"k":"b","n":"Corona-Folgen & Pflege"},{"k":"c","n":"Recht & Gerichte"},
          {"k":"d","n":"Digitaler Käfig & Geld"},{"k":"e","n":"KI als Denkraum"},{"k":"f","n":"Gesellschaft, Abriss & Zukunft"},
          {"k":"g","n":"Thesen des Gastgebers"}]

# ---------- Überblick ----------
kern = [
 ["1","Die Exekutive hat in der Corona-Zeit Parlamente und Gerichte übergangen.","Gewaltenteilung, „kleine Richterlein“, Fall Dettmar","[0:02]","★★★"],
 ["2","Als Sachverständiger „in der Burg“ kann er die Verantwortlichen nun befragen.","Enquete-Kommission, noch anderthalb Jahre","[0:02]","★★"],
 ["3","Die Ausgrenzung Ungeimpfter war „eine Jagd“.","Zitatsammlung, Wortwechsel mit Spahn","[0:16]","★★★"],
 ["4","Besuchsverbote haben vielen alten Menschen das Leben gekostet; das muss zuerst untersucht werden.","Demenzpflege, Tegnell, Bergamo, Spanien","[0:20]","★★★"],
 ["5","Verfahren gegen Ärzte wegen Maskenattesten sind seit 2020 sprunghaft gestiegen.","eigene Zahlen der Generalstaatsanwaltschaften, Kennedy-Brief","[0:31]","★★"],
 ["6","Satelliten, QR-Codes und digitales Geld bilden einen neuen „Systemkäfig“.","Starlink, ID2020, Grenzkabine Hamburg","[0:43]","★★"],
 ["7","KI ist eine Chance: Jeder kann eine Denkfabrik ohne Tabus betreiben.","Gespräch ohne Groll, Dokumente hochladen","[0:59]","★★★"],
 ["8","Es braucht ein Recht, analog zu bleiben und aus digitalen Systemen auszusteigen.","analogfreedom.eu, analoge Treffen","[1:01]","★★"],
 ["9","Macht braucht Zustimmung; Unterwerfung unter KI geschieht freiwillig.","COSMO-Befragungen, Faszination für schnelle Antworten","[1:06]","★★"],
 ["10","Ein „globales Abrissteam“ baut Energie und Ordnung ab; ein künftiges Ereignis könnte „virtuell“ sein wie Corona.","Energiewende, Kriegsangst, Variante D","[1:40]","★★"],
]
baum = {"typ":"baum","titel":"🌳 Themenbaum des Gesprächs","wurzel":TITEL,
 "unter":f"Tom Lausen · REALTALK MEDIA · aufgenommen 28.01.2026 · {DAUER}",
 "knoten":[
  {"t":"🏛️ Enquete-Kommission","k":[{"t":"„In der Burg“ [0:02]"},{"t":"Anhörung mit Maaßen und Faeser [0:08]"},{"t":"Wer einlädt [0:13]"},{"t":"Spahn und die „Jagd“ [0:17]"},{"t":"Experiment anderthalb Jahre [0:34]"}]},
  {"t":"🏷️ AfD und Kontaktschuld","k":[{"t":"Vorwurf der AfD-Nähe [0:06]"},{"t":"„Nicht politisch“ [0:14]"},{"t":"Fake-Opposition? [0:36]"},{"t":"Menschliche Ebene [0:36]"}]},
  {"t":"👵 Corona-Folgen","k":[{"t":"Kontaktnachverfolgung [0:10]"},{"t":"Besuchsverbote und Demenz [0:19]"},{"t":"Bergamo und Spanien [0:22]"},{"t":"Militärlaster in Bergamo [1:48]"}]},
  {"t":"⚖️ Recht und Gerichte","k":[{"t":"Gewaltenteilung [0:02]"},{"t":"Fall Dettmar [0:04]"},{"t":"Luftsicherheitsurteil [0:25]"},{"t":"Kennedy und Warken [0:28]"},{"t":"Attest-Verfahren [0:31]"}]},
  {"t":"🛰️ Digitaler Käfig","k":[{"t":"QR-Code und Grenzkabine [0:42]"},{"t":"Musk und Satelliten [0:43]"},{"t":"Internet of Things [0:45]"},{"t":"Gold und Fiat-Geld [0:52]"}]},
  {"t":"🧠 KI als Denkraum","k":[{"t":"Denkfabrik ohne Groll [0:58]"},{"t":"analogfreedom.eu [1:01]"},{"t":"„IQ von 1000“ [1:10]"},{"t":"Filter und Schmeichelei [1:15]"},{"t":"Selbst Drucksachen prüfen [1:55]"}]},
  {"t":"🦾 Demografie und Pflege","k":[{"t":"Strömungsabriss ab 45 [1:26]"},{"t":"Pillenknick [1:28]"},{"t":"Pflegeroboter [1:31]"}]},
  {"t":"🏚️ Abriss und Zukunft","k":[{"t":"Globales Abrissteam [1:40]"},{"t":"Energie-Abriss [1:45]"},{"t":"Variante D [1:52]"},{"t":"„Uniformation“ [1:59]"}]},
  {"t":"🎙️ Thesen des Gastgebers","k":[{"t":"Wall Street und Präzedenzfall [0:40]"},{"t":"Iran und Starlink [0:48]"},{"t":"Israel, TikTok, KI [1:13]"},{"t":"Bücher besitzen [2:00]"}]},
 ]}

steck = {"typ":"tabelle","kopf":["🧭 Steckbrief",""],"schmal":True,"zeilen":[
 ["Thema in einem Satz","Tom Lausen über seine Arbeit in der Corona-Enquete-Kommission, den Vorwurf der AfD-Nähe, Corona-Folgen für alte Menschen und über KI als Werkzeug gegen einen befürchteten digitalen „Käfig“."],
 ["Titel",TITEL],
 ["Format","Studiogespräch zu zweit, ohne Werbeblock; Lausens Vorräte-Tipp bezeichnet er selbst scherzhaft als „Werbeeinblendung“ [0:53]. Angekündigte Publikumsfragen entfallen."],
 ["Sprecher","👤 **Tom Lausen** – Gast, Datenanalyst, Sachverständiger der Enquete-Kommission · 🎙️ **Gastgeber** von REALTALK MEDIA – Name im Video nicht genannt ❓; laut eigener Aussage aus der Musik-/Hip-Hop-Szene, knapp unter 45; bringt lange eigene Thesen ein (u. a. [0:39–0:41], [0:48–0:50], [1:13–1:15], [1:22–1:24], [2:00–2:02])"],
 ["Dauer","ca. 2 Std. 4 Min."],
 ["Datum","Veröffentlichung ❓ (2026). Aufgenommen am 28.01.2026: Lausen spricht von der Anhörung „morgen“ mit Maaßen und Faeser, die am 29.01.2026 stattfand."],
 ["Grundton","einvernehmlich und locker; der Gastgeber widerspricht an wenigen Stellen (Iran, Kennedy-Deutung, KI-Qualität) und geht mit eigenen Thesen weiter als Lausen"],
 ["Hinweis","Automatische Untertitel, Namen teils verhört (z. B. „Marsen“, „Detmer“, „Technell“). Gesundheitsthemen nur auf Laien-Ebene; keine Empfehlungen."],
]}

ueberblick = [
 {"typ":"folge","k":K,"titel":TITEL,"gast":GAST,"rolle":ROLLE,"kanal":KANAL,"art":"Gespräch","karte":"REALTALK MEDIA · Gespräch",
  "datum":DATUM,"dauer":DAUER,"url":URL,
  "thema":"Lausen erzählt aus der Corona-Enquete-Kommission, antwortet auf den Vorwurf der AfD-Nähe und erklärt, warum er KI als Denkwerkzeug gegen einen digitalen „Käfig“ sieht.",
  "wege":[[K+"ab","📖","Gespräch im Detail","Abschnitt für Abschnitt, mit Zitaten"],[K+"zeit","📅","Zeitachse & Verzeichnisse","Ereignisse, Personen, Begriffe, Zahlen"],[K+"abgleich","⚖️","Abgleich & Daten","Diagramme, Aussagen neben Daten, Quellen"]],
  "kacheln":[]},
 {"typ":"hinweis","text":"Auswertung nach dem Transkript (automatische Untertitel): Gesagtes ohne Zeichen, Ergänzungen 📚, Unklares ❓. Fundstellen [Stunde:Minute] springen ins Video. Die Bewertung bleibt dem Leser."},
 {"typ":"abschnitt","titel":"⚡ In Kürze","liste":[
  "Aufgenommen am Vorabend einer Anhörung der Enquete-Kommission mit Hans-Georg Maaßen und Nancy Faeser.",
  "Lausen deutet die Corona-Politik als Übergriff der Exekutive auf Parlamente und Gerichte.",
  "Zur AfD sagt er: Er sei nicht politisch, die Menschen dort seien „völlig in Ordnung“.",
  "Er will vorrangig klären, ob Besuchsverbote und Maßnahmen alten Menschen das Leben gekostet haben.",
  "Ab der 42. Minute geht es um Satelliten, QR-Codes und digitales Geld als möglichen „Käfig“.",
  "Lausen sieht in der KI vor allem eine Chance: eine Denkfabrik für jeden, ohne Groll und Tabus.",
  "Er fordert ein Recht, analog zu bleiben und aus digitalen Systemen ohne Nachteile auszusteigen.",
  "Der Gastgeber bringt lange eigene Thesen ein, etwa zu Iran, Israel und TikTok; Lausen geht dabei meist nicht mit."]},
 {"typ":"abschnitt","titel":"🔦 Aus Lausens Sicht – der rote Faden","liste":[
  "Corona ist für ihn das Lehrstück, an dem sich zeigen lässt, wie ein neues System mit Angst und Zustimmung eingeführt wird.",
  "Deshalb will er die Aufarbeitung zu Ende bringen: Wer das Muster einmal verstanden hat, fällt beim nächsten Mal nicht darauf herein.",
  "Die Gefahr sieht er weniger im Zwang als in der freiwilligen Unterwerfung unter bequeme digitale Angebote.",
  "Das Gegenmittel ist für ihn eigenes Denken – unterstützt von KI, mit der jeder Dokumente selbst prüfen kann – und ein Recht, analog zu bleiben.",
  "Die Gegenstimmen und die Daten dazu stehen im Reiter Abgleich & Daten."]},
 {"typ":"text","text":"🎯 **Kernaussagen** – die zehn wichtigsten Thesen des Gesprächs:"},
 {"typ":"tabelle","kopf":["#","Aussage","Begründung im Gespräch","Fundstelle","Gewicht"],"zeilen":kern},
 baum,
 {"typ":"illu","id":"enquete_denkraum","titel":"Skizze: Vom digitalen Käfig zum Denkraum (schematisch, Darstellung laut Lausen)"},
 {"typ":"illu","id":"enquete_vorgaenge","titel":"Skizze: Belegte Vorgänge rund um das Gespräch und Geburten seit 1950 (belegte Daten)"},
 steck,
]

# ---------- Gespräch im Detail ----------
def tsp(v,b): return f'[{v}–{b}]'
abs_bl=[]; teile=[]
for von,bis,titel,kurz,th,liste in S:
    abs_bl.append({"typ":"abschnitt","titel":f"{titel} {tsp(von,bis)}","th":th,"liste":liste})
    teile.append({"von":von,"bis":bis,"t":kurz,"th":th})
detail = [
 {"typ":"text","text":f"🔎 Detaillierte Auswertung in der Reihenfolge des Gesprächs – {len(S)} Abschnitte. Lesehilfe: 💬 Zitat, 📌 Aussage, 🔗 Bezug, 📚 Ergänzung, ❓ unklar. „[seine Sicht]“ kennzeichnet Aussagen von Lausen oder dem Gastgeber."},
 {"typ":"gespraech","titel":"🧭 Gesprächsverlauf – wann worüber gesprochen wird","dauer":"2:03","themen":THEMEN,"teile":teile},
] + abs_bl

# ---------- Zeitachse & Verzeichnisse ----------
Z = [
 ("1953","1953","Operation Ajax: Putsch im Iran, von der CIA 2013 eingeräumt – vom Gastgeber genannt","[0:49]",True),
 ("1964","1964","Höchststand der Geburten in Deutschland (1,357 Mio.)","[1:28]",True),
 ("1965","1965","Bob Dylan spielt in Newport erstmals E-Gitarre – vom Gastgeber genannt","[1:56]",True),
 ("1967","1967","Lausen geboren; laut ihm Ende der geburtenstarken Jahrgänge","[1:28]",True),
 ("1975","1975","Geburten auf 782.000 gesunken (Pillenknick)","[1:28]",True),
 ("1992","1992","Film „Der Rasenmähermann“ (Lausen nennt 82, 86 oder 93 ❓)","[1:17]",True),
 ("2003","2003","„Animatrix“ erscheint – vom Gastgeber beschrieben","[1:18]",True),
 ("2006","2006","BVerfG: Abschussermächtigung im Luftsicherheitsgesetz nichtig (15.02.)","[0:25]",True),
 ("2014","2014","Absturz von MH17; Reporter Billy Six vor Ort (laut Lausen ❓)","[1:42]",True),
 ("2018","2018","QR-Code für Impfpässe angeblich von ID2020 entwickelt – laut Lausen ungeprüft ❓","[0:42]",False),
 ("2020","2020","Bergamo: laut Lausen 6.000 zusätzliche Tote in sechs Wochen ❓","[0:22]",False),
 ("2020","2020","Ministerpräsidenten von Merkel und Drosten „überrumpelt“ (laut Spahns Buch, nach Lausen ❓)","[1:00]",False),
 ("2020","2020","Spanien: Soldaten der UME finden Tote in Pflegeheimen (laut Lausen ❓)","[0:23]",False),
 ("2020–2021","2020","Laut Lausen sprunghaft mehr Verfahren wegen unrichtiger Gesundheitszeugnisse","[0:31]",False),
 ("Dez. 2020","2020","Sterbefälle 32 % über dem Mittel der Vorjahre (Destatis)","[1:47]",True),
 ("2021","2021","Wiederholte Äußerungen über Ungeimpfte (Gauck, Palmer u. a.), von Lausen gesammelt","[0:08]",False),
 ("2021","2021","Weimarer Familienrichter Dettmar hebt für zwei Schulklassen die Maskenpflicht auf","[0:04]",True),
 ("Jan. 2022","2022","RKI: Meldedaten wegen ausgelasteter Gesundheitsämter zunehmend unvollständig","[0:10]",True),
 ("2022","2022","Sachverständigenausschuss: keine ausreichende begleitende Datenerhebung","[0:20]",True),
 ("2023","2023","KI nennt die Impfung „wirksam und sicher“ – laut Gastgeber","[1:13]",False),
 ("Aug. 2023","2023","LG Erfurt: zwei Jahre auf Bewährung für Dettmar wegen Rechtsbeugung","[0:27]",True),
 ("Ende 2023","2023","5,7 Mio. Pflegebedürftige in Deutschland (Destatis)","[1:30]",True),
 ("März 2024","2024","RKI-Krisenstabsprotokolle nach Klage veröffentlicht","[0:10]",True),
 ("2024","2024","TikTok: „Zionist“ als Ersatzwort für Juden/Israelis fällt unter Hassrede-Regel","[1:14]",True),
 ("Juli 2024","2024","KI-Verordnung (EU) 2024/1689 im Amtsblatt; Lausen nennt 2020","[0:51]",True),
 ("Nov. 2024","2024","BGH bestätigt Urteil gegen Dettmar (20.11.)","[0:27]",True),
 ("Juni 2025","2025","BVerfG nimmt Verfassungsbeschwerde Dettmars nicht an (05.06.)","[0:27]",True),
 ("Sept. 2025","2025","Enquete-Kommission Corona konstituiert; Lausen sachverständiges Mitglied","[0:12]",True),
 ("Sept. 2025","2025","Netanjahu nennt soziale Medien „Waffen“ und den TikTok-Kauf den wichtigsten laufenden Kauf","[1:14]",True),
 ("15.12.2025","2025","Anhörung mit Jens Spahn; Lausen spricht von „Jagd“","[0:17]",True),
 ("Dez. 2025","2025","Bargeld-Schlange vor dem Glühwein am Hamburger Jungfernstieg (Lausen)","[1:21]",False),
 ("Jan. 2026","2026","Stromausfall in Berlin – von Lausen erwähnt ❓","[0:53]",False),
 ("Jan. 2026","2026","Proteste im Iran, Internetsperre, Starlink-Nutzung und -Störung","[0:48]",True),
 ("10.01.2026","2026","BMG: Warken weist Kennedys Vorwürfe zurück","[0:30]",True),
 ("11.01.2026","2026","Kennedy: Brief an Warken und Video auf X zu Verfahren gegen Ärzte","[0:28]",True),
 ("27.01.2026","2026","Menschenrechtsgruppe: über 6.000 bestätigte Tote im Iran","[0:48]",True),
 ("28.01.2026","2026","Aufnahme dieses Gesprächs (Vorabend der Anhörung)","[0:00]",True),
 ("29.01.2026","2026","Anhörung der Enquete-Kommission mit Maaßen, Faeser, de Maizière, Waldhoff, Volkmann, Kropp","[0:08]",True),
 ("Feb./März 2026","2026","Auftritt Angela Merkels in der Kommission – laut Lausen erwartet ❓","[0:32]",False),
 ("März 2026","2026","SpaceX meldet 10.000 Starlink-Satelliten im Orbit","[0:44]",True),
 ("Juli 2027","2027","Ende der Kommissionsarbeit – laut Lausen","[0:12]",False),
 ("bis 2030","2030","Zeitraum, über den Lausen konkret reden will","[1:25]",False),
 ("~2028","2028","Humanoide Roboter auf der Straße – Lausens Erwartung („in den nächsten zwei Jahren“)","[1:17]",False),
 ("~2036","2036","Roboter und Menschen laut Lausen noch etwa zehn Jahre unterscheidbar","[1:33]",False),
]
Zbl={"typ":"zeitachse","titel":"📅 Zeitachse – Ereignisse, die im Gespräch vorkommen","eintraege":[]}
for z,j,t,f,e in Z:
    Zbl["eintraege"].append({"z":z,"j":int(j),"t":t,"f":f,"e":e})
Zbl["eintraege"].sort(key=lambda x:x["j"])

personen = [
 ["Tom Lausen","Datenanalyst, Sachverständiger der Corona-Enquete-Kommission (benannt von der AfD)","Gast","[0:00]"],
 ["Gastgeber (Name ❓)","Moderator von REALTALK MEDIA","stellt Fragen, bringt eigene Thesen","[0:00]"],
 ["Frank Ulrich Montgomery","Ärztefunktionär, früher Präsident des Weltärztebunds","„kleine Richterlein“ (laut Lausen)","[0:03]"],
 ["Christian Dettmar","früherer Familienrichter in Weimar","Masken-Beschluss, Verurteilung","[0:04]"],
 ["Michael Müller","SPD, früher Regierender Bürgermeister von Berlin","Sachverständiger der Kommission","[0:06]"],
 ["Michael Nehls („Nels“)","Arzt, Autor","laut Gastgeber ebenfalls Fragesteller ❓","[0:06]"],
 ["Jens Spahn","CDU, früher Bundesgesundheitsminister","„Jagd“-Wortwechsel, Buch","[0:17]"],
 ["Christian Drosten","Virologe","„Kosten“ der Maßnahmen","[0:23]"],
 ["Hans-Georg Maaßen („Marsen“)","früher Präsident des Bundesamts für Verfassungsschutz","Sachverständiger am 29.01.2026","[0:08]"],
 ["Nancy Faeser („Nancy Fer“)","SPD, frühere Bundesinnenministerin","Gast am 29.01.2026; Zitat","[0:08]"],
 ["Joachim Gauck","früherer Bundespräsident","Zitat über Ungeimpfte","[0:08]"],
 ["Boris Palmer","Oberbürgermeister von Tübingen","Zitat Impfpflicht/Beugehaft","[0:09]"],
 ["Burkhard Müller-Ullrich","Publizist (Kontrafunk)","Buch „Ich habe mitgemacht“ ❓","[0:08]"],
 ["Anders Tegnell („Technell“)","früher Staatsepidemiologe Schwedens","Kontaktnachverfolgung, Besuchsverbote","[0:11]"],
 ["Julia Klöckner","Bundestagspräsidentin","formale Einladung der Sachverständigen","[0:13]"],
 ["„Bianca Blomenkamp“ ❓","Journalistin (Name unklar)","Zitat laut Lausen","[0:17]"],
 ["Gerd Antes ❓","Medizinstatistiker","„Kosten“ der Maßnahmen (laut Lausen)","[0:23]"],
 ["Paula Piechotta ❓ („Pichotta“)","Grünen-Abgeordnete, Ärztin","Begegnung im Gang","[0:24]"],
 ["Robert F. Kennedy Jr.","US-Gesundheitsminister","Brief und Video an Warken","[0:28]"],
 ["Nina Warken („Lina Wagen“)","CDU, Bundesgesundheitsministerin","Antwort an Kennedy","[0:30]"],
 ["Karl Lauterbach","SPD, früher Bundesgesundheitsminister","interessiert Lausen „nicht so“","[0:31]"],
 ["Angela Merkel","frühere Bundeskanzlerin","laut Lausen künftige Anhörung ❓","[0:32]"],
 ["Elon Musk","Unternehmer (SpaceX, Starlink)","„Teil des Systemkäfigs“","[0:43]"],
 ["Mike Pompeo","früher CIA-Direktor, US-Außenminister","vom Gastgeber genannt","[0:49]"],
 ["Cornelia Betsch („Frau Beitsch“)","Psychologin, Uni Erfurt (COSMO)","Messung der Zustimmung","[1:07]"],
 ["Yuval Noah Harari","Historiker, Autor","vom Gastgeber genannt","[1:08]"],
 ["John Kiriakou („Kirako“ ❓)","früher CIA-Mitarbeiter","vom Gastgeber genannt","[1:07]"],
 ["Benjamin Netanjahu","israelischer Ministerpräsident","vom Gastgeber genannt","[1:14]"],
 ["Billy Six","Reporter","Berichte aus der Ukraine (laut Lausen)","[1:42]"],
 ["Wolfgang Wodarg („Wodak“)","Arzt, früher Bundestagsabgeordneter","früherer Gast des Kanals","[1:49]"],
 ["Bob Dylan","Musiker","E-Gitarre 1965 (Gastgeber)","[1:56]"],
]
orte = [
 ["Bundestag („die Burg“)","Sitz der Enquete-Kommission","[0:02]"],["Weimar","Familiengericht, Fall Dettmar","[0:04]"],
 ["Schweden","Gegenbeispiel ohne Lockdown","[0:11]"],["Bergamo","Übersterblichkeit 2020, Lausens Reise","[0:22]"],
 ["Spanien / Madrid","Pflegeheime, Einsatz der UME","[0:23]"],["USA","Kennedy, ICE","[0:28]"],
 ["Hamburg (Flughafen, Jungfernstieg)","Grenzkabine; Bargeld-Schlange","[0:43]"],["Ukraine","Starlink-Nutzung","[0:47]"],
 ["Iran","Proteste, Internetsperre","[0:48]"],["Gaza","vom Gastgeber genannt","[0:48]"],
 ["Berlin","Studio, Stromausfall","[0:53]"],["Detmold („Deadmold“)","Vortrag vor knapp 400 Menschen","[1:12]"],
 ["Japan, China","Demografie wie in Deutschland","[1:29]"],["Italien","häusliche 24-Stunden-Pflege; Militärlaster","[1:30]"],
]
begriffe = [
 ["Enquete-Kommission","vom Bundestag eingesetztes Gremium aus Abgeordneten und Sachverständigen, das einen Themenkomplex untersucht","[0:02]"],
 ["Gewaltenteilung","Trennung von Exekutive (Regierung, Behörden), Legislative (Parlament) und Judikative (Gerichte)","[0:02]"],
 ["Rechtsbeugung (§ 339 StGB)","bewusste, schwerwiegende Verletzung des Rechts durch Richter oder Amtsträger","[0:27]"],
 ["Kontaktschuld","Abwertung einer Person wegen ihres Umgangs mit anderen","[0:06]"],
 ["Kontaktnachverfolgung","Ermittlung von Kontaktpersonen Infizierter durch Gesundheitsämter","[0:10]"],
 ["Unrichtiges Gesundheitszeugnis (§§ 278, 279 StGB)","falsches ärztliches Zeugnis bzw. dessen Gebrauch","[0:31]"],
 ["Luftsicherheitsurteil","BVerfG 2006: Staat darf kein entführtes Flugzeug mit Unbeteiligten abschießen","[0:25]"],
 ["Fiat-Geld","Geld ohne Warendeckung, das durch Kredit entsteht","[0:41]"],
 ["CBDC / digitaler Euro","digitales Zentralbankgeld","[0:42]"],
 ["ID2020","Initiative für digitale Identität (2016 gegründet) – Lausens Aussage zum QR-Code ❓","[0:42]"],
 ["Starlink","Satelliten-Internet von SpaceX","[0:44]"],
 ["Internet of Things","Vernetzung von Geräten und Gegenständen","[0:45]"],
 ["AI Act / KI-Verordnung","EU-Verordnung 2024/1689 mit Regeln für KI-Systeme nach Risiko","[0:51]"],
 ["COSMO","COVID-19 Snapshot Monitoring, regelmäßige Befragung der Uni Erfurt","[1:07]"],
 ["„Rumregenauern“, „rumwolfen“","Lausens Wort für düstere Zukunftsszenarien","[0:51]"],
 ["Denkfabrik / Thinktank","Gruppe, die Ideen und Konzepte ausarbeitet","[0:58]"],
 ["Analoges Zugangsgrundrecht","Lausens Vorschlag eines Rechts, ohne digitale Mittel teilzuhaben","[1:01]"],
 ["Pillenknick","Rückgang der Geburten ab Mitte der 1960er-Jahre","[1:28]"],
 ["Strömungsabriss","Lausens Bild für fehlende Jüngere bei seinen Veranstaltungen","[1:26]"],
 ["„Uniformation“","Wortspiel des Gastgebers: KI-Einheitsbrei","[1:59]"],
]
zahlen = [
 ["5–6","Sachverständige je monatlicher Anhörung","[0:12]"],["anderthalb Jahre","Restlaufzeit der Kommission","[0:05]"],
 ["Hunderte","Kommentare zur Lager-Angst","[0:09]"],["6.000","zusätzliche Tote in Bergamo in sechs Wochen (laut Lausen ❓)","[0:22]"],
 ["600.000","Aufrufe eines Anti-AfD-Videos (Gastgeber ❓)","[0:35]"],["100 m","erlaubte Flughöhe seiner Drohne","[0:43]"],
 ["8.000 / 40.000","Starlink-Satelliten heute / geplant (laut Lausen)","[0:44]"],["über 1.000","Satelliten von Amazon (laut Lausen ❓)","[0:45]"],
 ["500 → 40.000","im Umlauf genannte Iran-Todeszahlen (Gastgeber)","[0:48]"],["20.000–30.000","Tote pro Tag im Zweiten Weltkrieg (Gastgeber ❓)","[0:48]"],
 ["4- bis 5-fach","Anstieg von Gold und Silber (laut Lausen ❓)","[0:52]"],["90–150","IQ-Spanne des Menschen","[0:55]"],
 ["1.000 / 4.000–5.000","„IQ“ der KI heute / später (Lausens Schätzung)","[1:10]"],["knapp 400","Zuhörer in Detmold","[1:12]"],
 ["1,30 m","Größe erster Straßenroboter (Erwartung)","[1:17]"],["45","Altersgrenze seines Publikums","[1:26]"],
 ["30 und 28","Alter seiner Kinder","[1:27]"],["100 Millionen","verlassen den Arbeitsmarkt (Bezug ❓)","[1:30]"],
 ["3 Jahre","bis dahin kein Pflegeroboter am Menschen","[1:31]"],["10 Jahre","Roboter noch von Menschen unterscheidbar","[1:33]"],
 ["2.000","Tote pro Tag in Italien (laut Lausen ❓)","[1:49]"],["10 %","Anteil der Zuschauer, die mit KI Drucksachen prüfen sollen","[1:55]"],
]
zeit = [Zbl,
 {"typ":"tabelle","kopf":["👤 Person","Wer / was","Rolle im Gespräch","Fundstelle"],"zeilen":personen},
 {"typ":"tabelle","kopf":["🗺️ Ort","Rolle","Fundstelle"],"zeilen":orte},
 {"typ":"tabelle","kopf":["📖 Begriff","Erklärung","Fundstelle"],"zeilen":begriffe},
 {"typ":"tabelle","kopf":["📊 Zahl im Gespräch","Angabe","Fundstelle"],"zeilen":zahlen}]

# ---------- Abgleich ----------
A = [
 ["Die Exekutive habe Parlamente „ausgeschaltet“, eine Art „Putsch“. [0:02]",
  "In der Anhörung vom 29.01.2026 sagte Waldhoff, der Bundestag sei jederzeit arbeitsfähig gewesen; Maaßen sah eine Machtverschiebung zur Exekutive; Faeser und Volkmann nannten die vielen Entscheidungen in der Ministerpräsidentenkonferenz und per Rechtsverordnung als Problem. Einig waren sich die Geladenen, dass die Balance zwischen Exekutive und Parlamenten für künftige Krisen verbessert werden muss.",
  Q['hib78']],
 ["Morgen kommen Maaßen als Sachverständiger und Faeser. [0:08]",
  "Bestätigt: Anhörung am 29.01.2026 mit Waldhoff, Maaßen, Faeser, Volkmann, Kropp und de Maizière.",
  Q['hib78']+' · '+Q['to14']],
 ["Monatlich kommen fünf bis sechs Sachverständige. [0:12]",
  "Zur Anhörung am 29.01.2026 waren sechs Personen geladen. Die Kommission besteht aus 14 Abgeordneten und 14 Sachverständigen; die AfD stellt je drei.",
  Q['hib78']+' · '+Q['hib394']],
 ["Lausen sei von der Bundestagspräsidentin eingeladen, von der AfD vorgeschlagen. [0:13]",
  "Der Bundestag führt Lausen als sachverständiges Mitglied der Enquete-Kommission, benannt von der AfD-Fraktion. ❓ Die genannte Änderung der Einladungspraxis ist hier nicht geprüft.",
  Q['lausbt']+' · '+Q['konst']],
 ["Dettmar sei „aus dem Dienst geworfen“ worden. [0:04]",
  "Das LG Erfurt verurteilte ihn im August 2023 wegen Rechtsbeugung zu zwei Jahren auf Bewährung; der BGH bestätigte am 20.11.2024 (2 StR 54/24). Er war vorläufig vom Dienst suspendiert, die Bezüge um 25 % gekürzt. Das BVerfG nahm seine Verfassungsbeschwerde am 05.06.2025 nicht zur Entscheidung an.",
  Q['ltobgh']+' · '+Q['ltobv']],
 ["Der BGH habe die Schwelle für Rechtsbeugung gesenkt, Vorsatz müsse nicht mehr nachgewiesen werden (seine Interpretation). [0:27]",
  "Laut LTO stützte der BGH die Verurteilung auf elementare Rechtsverstöße, bei denen sich der Richter bewusst und schwerwiegend vom Recht entfernt habe; auf seine Motive komme es wegen der Kombination der Verstöße nicht an. Eine Absenkung der Vorsatzanforderungen wird dort nicht berichtet.",
  Q['ltobgh']],
 ["Kontaktnachverfolgung funktioniere nur am Anfang; Gesundheitsämter seien überlastet gewesen. [0:10]",
  "Im Januar 2022 erklärte das RKI, die PCR-Meldedaten würden wegen ausgelasteter Testkapazitäten und Gesundheitsämter zunehmend unvollständig. Die Protokolle des RKI-Krisenstabs wurden im März 2024 nach einer Klage teilgeschwärzt veröffentlicht.",
  Q['rkimeld']+' · '+Q['rkiprot']],
 ["Besuchsverbote hätten „garantiert tausenden Menschen das Leben gekostet“. [0:20]",
  "❓ Eine amtliche Zahl dazu liegt hier nicht vor. Der Sachverständigenausschuss stellte 2022 fest, dass keine ausreichende begleitende Datenerhebung zu den Maßnahmen aufgebaut worden war; ihre Folgen ließen sich deshalb nur begrenzt bewerten.",
  Q['sva']],
 ["Spahn habe den Vorwurf einer „Jagd“ auf Ungeimpfte zurückgewiesen. [0:17]",
  "❓ Der Wortwechsel ist hier nicht nachgeprüft; der Mitschnitt der Anhörung ist öffentlich.",
  Q['med1512']],
 ["Ein Leben dürfe nicht gegen viele abgewogen werden (Luftsicherheitsurteil). [0:25]",
  "Das BVerfG erklärte am 15.02.2006 die Ermächtigung, ein entführtes Flugzeug mit Unbeteiligten an Bord abzuschießen, für nichtig – mit Verweis auf Menschenwürde und Recht auf Leben. Ob und wie sich das auf Pandemiemaßnahmen übertragen lässt, ist eine juristische Deutungsfrage.",
  Q['bverfg06']],
 ["Kennedy habe Warken in Brief und Video kritisiert. [0:28]",
  "Kennedy schrieb Warken und veröffentlichte ein Video auf X; er sprach von über tausend verfolgten Ärzten und Tausenden Patienten. ZDFheute nennt für diese Zahl keinen Beleg; eine zentrale Erfassung der Verfahren gibt es laut ZDFheute nicht.",
  Q['zdfk']],
 ["Warken habe die Verfahren als Betrug und Urkundenfälschung dargestellt; ein Arzt-Attest sei aber keine Urkundenfälschung. [0:30]",
  "Das BMG schrieb am 10.01.2026, verfolgt würden ausschließlich Betrug und Urkundenfälschung, etwa „falscher Impfpässe oder unechter Maskenatteste“. ZDFheute: Für Ärzte gilt § 278 StGB (unrichtiges Gesundheitszeugnis), für Patienten § 279; Verstöße gegen Masken- oder Impfpflicht selbst waren Ordnungswidrigkeiten. Der BGH bestätigte 2025 zwei Verurteilungen von Ärzten.",
  Q['bmg']+' · '+Q['zdfk']],
 ["2020/21 habe es massiv mehr Verfahren wegen unrichtiger Gesundheitszeugnisse gegeben. [0:31]",
  "❓ Lausens Zahlen der Generalstaatsanwaltschaften sind hier nicht einsehbar. Laut ZDFheute gibt es keine zentrale Erfassung dieser Verfahren.",
  Q['zdfk']],
 ["Musk habe rund 8.000 Satelliten im All und wolle 40.000. [0:44]",
  "SpaceX meldete im März 2026 – rund sechs Wochen nach der Aufnahme – 10.000 Starlink-Satelliten im Orbit. ❓ Die Ausbauziele sind hier nicht geprüft.",
  Q['sciam']],
 ["Gastgeber: Iran-Todeszahlen bis 20.000 oder 40.000 seien Propaganda; Starlink sei für „terroristische Zellen“ bereitgestellt und dann gestört worden. [0:48–0:50]",
  "Eine Menschenrechtsgruppe zählte bis 27.01.2026 über 6.000 bestätigte Tote. Berichtet sind eine wochenlange Internetsperre, die Nutzung von Starlink durch Iraner und dessen Störung durch militärisches Jamming. ❓ Zur Behauptung gesteuerter Zellen liegen hier keine Belege vor.",
  Q['almon']+' · '+Q['alblack']+' · '+Q['semafor']+' · '+Q['annahar']],
 ["Gastgeber: „Regime Change“ wie bei Operation Ajax. [0:49]",
  "Die CIA räumte 2013 ein, den Putsch gegen Mossadegh 1953 organisiert zu haben. ❓ Für 2026 ist eine solche Beteiligung hier nicht belegt.",
  Q['aj53']],
 ["Der AI Act sei 2020 beschlossen worden. [0:51]",
  "Die KI-Verordnung ist die Verordnung (EU) 2024/1689 vom 13.06.2024, veröffentlicht am 12.07.2024, in Kraft seit 01.08.2024; ihre Pflichten gelten gestaffelt.",
  Q['eurlex']],
 ["Gastgeber: Der AI Act lenke Geld aus Forschung und Kunst in KI und Aufrüstung. [1:20]",
  "Nach Art. 2 Abs. 3 gilt die Verordnung nicht für KI-Systeme, die ausschließlich militärischen, Verteidigungs- oder nationalen Sicherheitszwecken dienen. ❓ Regeln zur Umschichtung von Fördergeldern waren darin hier nicht zu finden.",
  Q['art2']],
 ["Gastgeber: Netanjahu und Israel steuerten das Training von OpenAI; „Antizionismus“ werde herausgefiltert. [1:13–1:14]",
  "Belegt ist: Netanjahu nannte vor US-Influencern im September 2025 soziale Medien eine der wichtigsten „Waffen“ und den TikTok-Verkauf den wichtigsten laufenden Kauf; er sprach auch über Elon Musk. ❓ Zu einem Einfluss auf das Training von OpenAI wurde hier kein Beleg gefunden.",
  Q['ji']],
 ["Gastgeber: Bei TikTok falle der Begriff „Zionismus“ unter Hassrede. [1:14]",
  "Laut einem Bericht von 2024 wendet TikTok seine Hassrede-Regel auf „Zionist“ an, wenn das Wort als Ersatz für Juden oder Israelis benutzt wird, nicht wenn es eine politische Ideologie bezeichnet. ❓ Die Aussage zu „Epstein“ ist hier nicht geprüft.",
  Q['fang']],
 ["Geburtenstarke Jahrgänge „bis 1967“, danach der Pillenknick. [1:28]",
  "Die meisten Geburten gab es 1964 (1.357.304); 1967 lagen sie noch über 1 Mio. (1965: 1.325.386, 1970: 1.047.737), 1975 bei 782.310 (Diagramm).",
  Q['bpb']],
 ["Viele aus den starken Jahrgängen würden pflegebedürftig. [1:29]",
  "Ende 2023 waren knapp 5,7 Mio. Menschen pflegebedürftig, 730.000 mehr als Ende 2021; 86 % wurden zu Hause versorgt. Den starken Anstieg führt Destatis vor allem auf den 2017 erweiterten Pflegebegriff zurück; demografisch allein wären es rund 5,1 Mio.",
  Q['aepfl']],
 ["2020 habe niemand jemanden gekannt, der an Corona gestorben ist. [1:47]",
  "Destatis zählte im April 2020 10 % und im Dezember 2020 32 % mehr Sterbefälle als im Mittel der vier Vorjahre; 2021 und 2022 lagen mehrere Monate deutlich darüber (Diagramm). Über Bekanntschaften sagen diese Zahlen nichts aus.",
  Q['destst']],
 ["Gastgeber: KI nenne die Impfung noch 2023 „wirksam und sicher“. [1:13]",
  "Das PEI wertet Verdachtsmeldungen zu Nebenwirkungen aus und veröffentlicht Sicherheitsberichte. Bei Verdacht auf eine Nebenwirkung: ärztlich abklären lassen und über das Portal des PEI melden. Keine Empfehlung.",
  Q['pei']+' · '+Q['nebenw']],
]

geb = [[1950,1.117],[1955,1.113],[1960,1.262],[1964,1.357],[1965,1.325],[1970,1.048],[1975,0.782],[1980,0.866],[1990,0.906],[2000,0.767],[2010,0.678],[2015,0.738],[2016,0.792],[2019,0.778]]
gest = [[1950,0.748],[1955,0.796],[1960,0.877],[1964,0.870],[1965,0.908],[1970,0.976],[1975,0.990],[1980,0.952],[1990,0.921],[2000,0.839],[2010,0.859],[2015,0.925],[2016,0.911],[2019,0.940]]
diag = [
 {"typ":"kurs","id":"enquete-geburten","titel":"📈 Lebendgeborene und Gestorbene in Deutschland (Mio.)",
  "reihen":[{"name":"Lebendgeborene","kurz":"Geborene","einheit":"Mio.","dez":3,"hoeherGut":None,"punkte":geb},
            {"name":"Gestorbene","kurz":"Gestorbene","einheit":"Mio.","dez":3,"hoeherGut":None,"punkte":gest}],
  "hoeherGut":None,"vergleich":True,
  "quelle":Q['bpb']+" (GENESIS-Online, Statistisches Jahrbuch); 2019 vorläufig. Stand: August 2020.",
  "hinweis":"Bezug zum Gespräch [1:28]: Pillenknick. Gestorbene ohne Totgeborene. Für 2022 nennt Destatis rund 1,07 Mio. Gestorbene, für 2024 etwa 1,0 Mio. (vorläufig) – "+Q['aest']+"."},
 {"typ":"kurs","id":"enquete-dezember","titel":"📈 Sterbefälle im Dezember: Abweichung vom Mittel der vier Vorjahre (%)",
  "reihen":[{"name":"Abweichung im Dezember","kurz":"Dez.","einheit":"%","dez":0,"hoeherGut":False,"punkte":[[2020,32],[2021,25],[2022,23],[2023,-5],[2024,-14],[2025,-12]]}],
  "hoeherGut":False,
  "quelle":Q['destst']+". Stand: November 2026.",
  "hinweis":"Bezug zum Gespräch [1:47]: „2020 hat niemand jemanden gekannt …“. Die Vergleichsbasis (Median der vier Vorjahre) verschiebt sich jedes Jahr; die Werte sind deshalb nicht direkt vergleichbar."},
 {"typ":"balken","titel":"📊 Sterbefälle 2020–2022: einzelne Monate im Vergleich zum Mittel der Vorjahre (%)","einheit":"%","dez":0,
  "zeilen":[["April 2020",10],["Dezember 2020",32],["Januar 2021",26],["November 2021",22],["Oktober 2022",20],["Dezember 2022",23]],
  "quelle":Q['destst']+". Stand: November 2026.",
  "hinweis":"Bezug zum Gespräch [0:22] und [1:47]: Übersterblichkeit. Ausgewählt sind die Monate mit den höchsten Abweichungen je Jahr; im Februar und März 2021 lagen die Werte leicht darunter (−1 % und −6 %)."},
 {"typ":"balken","titel":"📊 Wie Pflegebedürftige Ende 2023 versorgt wurden (Mio.)","einheit":"Mio.","dez":2,
  "zeilen":[["Zu Hause, nur Pflegegeld (meist Angehörige)",3.1],["Zu Hause mit ambulantem Dienst",1.1],["Zu Hause, Pflegegrad 1",0.68],["Vollstationär im Heim",0.8]],
  "quelle":Q['aepfl']+". Stand: Dezember 2023.",
  "hinweis":"Bezug zum Gespräch [1:29–1:31]: Pflegebedarf, häusliche Pflege, Pflegeroboter. Zusammen knapp 5,7 Mio."},
 {"typ":"balken","titel":"📊 Wer in der Enquete-Kommission sitzt (Abgeordnete + Sachverständige)","einheit":"","dez":0,
  "zeilen":[["CDU/CSU",10],["AfD",6],["SPD",6],["Grüne",4],["Linke",2]],
  "quelle":Q['hib394']+". Stand: September 2025.",
  "hinweis":"Bezug zum Gespräch [0:06–0:14]: Lausen fragt im Zeitkontingent der AfD, die drei Abgeordnete und drei Sachverständige stellt."},
 {"typ":"vergleich","titel":"⚖️ Zahlen im Gespräch und Daten nebeneinander","la":"Im Gespräch genannt","lb":"Daten laut Quelle","zeilen":[
  {"n":"Geladene Gäste je Anhörung (29.01.2026)","a":6,"b":6,"dez":0,"at":"5–6","f":"[0:12]","q":Q['hib78']},
  {"n":"Letztes geburtenstarkes Jahr / Höchststand","a":1967,"b":1964,"dez":0,"at":"„bis 1967“","bt":"Höchststand 1964","f":"[1:28]","q":Q['bpb']},
  {"n":"Beschlussjahr der EU-KI-Verordnung","a":2020,"b":2024,"dez":0,"f":"[0:51]","q":Q['eurlex']},
  {"n":"Starlink-Satelliten im Orbit","a":8000,"b":10000,"dez":0,"at":"rund 8.000","bt":"10.000 (März 2026, nach dem Gespräch)","f":"[0:44]","q":Q['sciam']},
  {"n":"Tote bei den Iran-Protesten (Gastgeber: genannte Höchstwerte)","a":20000,"b":6000,"dez":0,"at":"bis 20.000 (auch 40.000)","bt":"über 6.000 bestätigt (27.01.2026)","f":"[0:48]","q":Q['almon']},
 ]},
]

schluss = [
 {"typ":"abschnitt","titel":"🧩 Spannungen im Gespräch","liste":[
  "Der Gastgeber zieht Kennedys Brief in Richtung „Nazi-Karte“; Lausen stellt klar, das sei nur seine eigene Deutung gewesen, Kennedy habe sachlich formuliert [0:28–0:38].",
  "Der Gastgeber hält die AfD für eine mögliche „Fake-Opposition“ und Parlamente für unwichtig; Lausen setzt auf die menschliche Ebene und widerspricht nicht direkt [0:35–0:37].",
  "Der Gastgeber sieht KI als Werkzeug einer „Machtelite“; Lausen ist davon „noch nicht so überzeugt“ und sieht eher schwer steuerbare Systeme [1:14–1:16].",
  "Der Gastgeber hält KI-Antworten zu Politik für unbrauchbar; Lausen hält sie bei konkreter Arbeit mit Dokumenten für sehr leistungsfähig [1:10–1:13].",
  "Beim Pflegeroboter widerspricht Lausen dem Vergleich mit tödlichen Flugversuchen: Solche Roboter würden gar nicht erst zugelassen [1:32].",
  "Zu Iran, Israel und Gaza äußert sich Lausen kaum: Er könne nicht einschätzen, was dort passiert, ohne selbst hinzufahren [1:42]."]},
 {"typ":"abschnitt","titel":"💡 Was man mitnehmen kann","liste":[
  "Die Anhörungen der Enquete-Kommission sind öffentlich; Tagesordnungen, Protokolle und Mitschnitte stehen beim Bundestag.",
  "Lausens Methode ist überprüfbar: Bundestagsdrucksachen und Gesetzestexte lassen sich selbst lesen – mit oder ohne KI.",
  "Bei Zahlen lohnt der Blick in die Primärquelle: Bei Geburten, Sterbefällen und Pflege zeigen die amtlichen Reihen, wie groß die Effekte sind.",
  "Gerichtsentscheidungen wie im Fall Dettmar sind veröffentlicht; Kommentar und Urteil lassen sich nebeneinander lesen."]},
 {"typ":"abschnitt","titel":"❓ Offen","liste":[
  "Veröffentlichungsdatum des Videos und Name des Gastgebers.",
  "Lausens Zahlen der Generalstaatsanwaltschaften zu Attest-Verfahren 2020/21.",
  "Belege für Todesfälle infolge von Besuchsverboten; Bergamo-Zahl; Ermittlungen in Spanien.",
  "Die Aussagen von Drosten und Antes zu „Kosten“ der Maßnahmen im Wortlaut.",
  "Wer die Journalistin „Bianca Blomenkamp“ ist und von wem der „Sozialschädlinge“-Satz stammt.",
  "Die vom Gastgeber genannten Aussagen zu OpenAI, TikTok/„Epstein“, Harari und Kindle-Löschungen."]},
 {"typ":"abschnitt","titel":"🔎 Weiter recherchieren","liste":[
  "Wortprotokoll der Anhörung vom 29.01.2026 und die schriftlichen Stellungnahmen der Sachverständigen (Bundestag, Enquete-Kommission Corona).",
  "Strafverfolgungsstatistik von Destatis zu §§ 278, 279 StGB für 2019–2023.",
  "ISTAT-Sterbedaten der Provinz Bergamo für März und April 2020.",
  "Volltext der Verordnung (EU) 2024/1689 (Art. 2, Art. 5) und die Zeitplan-Übersicht der EU-Kommission.",
  "Pflegestatistik von Destatis (Zeitreihe seit 1999) und die Pflegevorausberechnung.",
  "Das Abschlussdokument der Enquete-Kommission, wenn es erscheint."]},
]

abgl = [{"typ":"text","text":"Neutraler Abgleich: links die Aussage im Gespräch, rechts die gängige Darstellung bzw. Daten mit Quelle. Die Bewertung bleibt dem Leser."},
        {"typ":"tabelle","kopf":["Aussage im Gespräch","Gängige Darstellung (Mainstream) / Daten 📚","Quelle"],"stapel":True,"zeilen":A}] + diag + schluss

# ---------- Kacheln ----------
nd = sum(1 for b in diag if b['typ'] in ('kurs','balken','vergleich'))
qn = len(Q)+1
ueberblick[0]['kacheln'] = [[str(len(S)),"Abschnitte"],["10","Kernaussagen"],[str(len(A)),"Abgleich-Punkte"],[str(len(Zbl['eintraege'])),"Zeitachse"],[str(nd),"Diagramme"]]

reiter = [
 {"id":K,"titel":f"{G}: Überblick","bloecke":ueberblick},
 {"id":K+"ab","titel":f"{G}: Gespräch im Detail","bloecke":detail},
 {"id":K+"zeit","titel":f"{G}: Zeitachse & Verzeichnisse","bloecke":zeit},
 {"id":K+"abgleich","titel":f"{G}: Abgleich & Daten","bloecke":abgl},
]
quellen = [[f"Video: {TITEL} – REALTALK MEDIA (YouTube)",URL]] + [[tit(k),url(k)] for k in Q]
out = {"k":K,"gast":GAST,"reiter":reiter,
 "folgen_zeile":["2026 ❓ (aufgenommen 28.01.2026)","Tom Lausen (Datenanalyst, Sachverständiger der Enquete-Kommission)",TITEL,
                 "Enquete-Kommission, AfD-Nähe, Besuchsverbote, Attest-Verfahren, Satelliten & digitales Geld, KI als Denkraum, analoges Grundrecht, Demografie & Pflege",
                 "{{a:lausen-enquete|hier: Enquete und KI}}",f"[ansehen]({URL})"],
 "baum_ast":{"gruppe":"🧬 Gesundheit & Corona-Aufarbeitung","t":"👤 Tom Lausen bei REALTALK MEDIA – Enquete-Kommission, AfD, KI, analoge Freiheit"},
 "neu":{"d":"2026-11-12","t":"Tom Lausen – Enquete und KI (REALTALK MEDIA)",
        "k":f"Lausen über die Corona-Enquete, den Vorwurf der AfD-Nähe und KI als Denkwerkzeug – {len(S)} Abschnitte, Abgleich mit Quellen, {nd} Diagramme.",
        "h":"#a-lausen-enquete","art":"Video"},
 "quellen":quellen,
 "web":[["Tom Lausen – Bundestag, Sachverständiger der Enquete-Kommission",url('lausbt')]]}
p=os.path.join(os.path.dirname(os.path.abspath(__file__)),'folge.json')
json.dump(out, open(p,'w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', len(S), 'Abschnitte,', len(A), 'Abgleich,', nd, 'Diagramme,', len(Zbl['eintraege']), 'Zeitachse')
