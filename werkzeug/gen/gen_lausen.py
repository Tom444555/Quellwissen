import json, sys
sys.path.insert(0, '/home/claude/quellwissen/werkzeug')
from bausteine import *

URL = "https://www.youtube.com/watch?v=mgzb_dUm93Q"
VT = "Corona ist vorbei. Die Fragen sind es nicht."
G = "Fragen bleiben"
K = "fragen"

L_BT = "[Bundestag – Tom Lausen, Sachverständiger der Enquete-Kommission](https://www.bundestag.de/ausschuesse/weitere_gremien/ee01/1107006-1107006)"
L_KONST = "[Bundestag, hib 394/2025 – Enquete-Kommission konstituiert](https://www.bundestag.de/presse/hib/kurzmeldungen-1107614)"
L_TEXT = "[Bundestag – Konstituierung der Enquete-Kommission „Corona“](https://www.bundestag.de/dokumente/textarchiv/2025/kw37-pa-enquete-corona-konstituierung-1107024)"
L_ANH = "[Bundestag – Anhörung 7. Mai 2026: Lehren für Schutzmaßnahmen](https://www.bundestag.de/dokumente/textarchiv/2026/kw19-pa-enquete-corona-1170260)"
L_PROT = "[Bundestag – Wortprotokoll der 10. Sitzung, 1.12.2025 (PDF)](https://www.bundestag.de/resource/blob/1146200/2025-12-01_10-Sitzung.pdf)"
L_DEST20 = "[Destatis, Pressemitteilung 445/2021 – Krankenhausbehandlungen 2020](https://www.destatis.de/EN/Press/2021/09/PE21_445_231.html)"
L_DEST25 = "[Destatis, Pressemitteilung 376/2026 – Krankenhausbehandlungen 2025](https://www.destatis.de/DE/Presse/Pressemitteilungen/2026/10/PD26_376_231.html)"
L_DEST21 = "[Destatis, Pressemitteilung 563/2021](https://www.destatis.de/DE/Presse/Pressemitteilungen/2021/12/PD21_563_12.html)"
L_AEZ = "[Ärzte Zeitung – Zahl der Intensivbetten um fünf Prozent gestiegen](https://www.aerztezeitung.de/Politik/Zahl-der-Intensivbetten-um-fuenf-Prozent-gestiegen-425524.html)"
L_AEB = "[Deutsches Ärzteblatt – COVID-19-Pandemie: Historisch niedrige Bettenauslastung](https://www.aerzteblatt.de/archiv/218200)"
L_AEB24 = "[Deutsches Ärzteblatt – Krankenhäuser verzeichnen deutlichen Personalaufwuchs](https://www.aerzteblatt.de/news/krankenhauser-verzeichnen-deutlichen-personalaufwuchs)"
L_BIFG = "[BARMER Institut (bifg) – Entwicklung der Krankenhausfallzahlen (PDF)](https://www.bifg.de/media/dl/ePaper/bifg-ePaper-Krankenhausfallzahlen.pdf)"
L_THIEME = "[Thieme CNE – 19 Millionen Patienten 2015 (nach Destatis)](https://cne.thieme.de/cne-webapp/p/news/details/00555407-9c54-4a2d-aa05-41516613e97a)"
L_MYDRG = "[myDRG – Destatis-Meldung vom 20.12.2022](https://www.mydrg.de/myDRG_archives/2022/12/9-8-millionen-behandlungen-in-notfallambulanzen-im-jahr-2021.html)"
L_ONKO = "[Journal Onkologie – Krankenhausbehandlungen 2022 (nach Destatis)](https://www.journalonko.de/news/gesundheitspolitik/weniger-krankenhaus-behandlungen)"
L_STAT = "[statistiken-aktuell.de – Krankenhausbehandlungen 2024 (nach Destatis)](https://statistiken-aktuell.de/krankenhausbehandlungen-2024-datenmonitor/)"
L_MOB = "[COVID-19 Mobility Project (RKI und HU Berlin) – erster Mobilitätsbericht](https://covid-19-mobility.org/reports/first-report-general-mobility/)"
L_DESTMOB = "[Destatis – Mobilitätsindikatoren auf Basis von Mobilfunkdaten](https://destatis.de/EN/Service/EXSTAT/Datensaetze/mobility-indicators-mobilephone.html)"
L_SCHAADE = "[Ärzte Zeitung, 16.3.2020 – RKI: „Alles ist gut, was Abstand zwischen die Menschen bringt“](https://www.aerztezeitung.de/Politik/Alles-ist-gut-was-Abstand-zwischen-die-Menschen-bringt-407690.html)"
L_AEB16 = "[Deutsches Ärzteblatt, 16.3.2020 – RKI-Pressekonferenz](https://www.aerzteblatt.de/news/rki-gesundheitsaemter-sollten-unterstuetzung-aus-anderen-verwaltungsbereichen-bekommen-021805eb-3bce-4151-aa31-0fa2ff390b59)"
L_ORF = "[ORF, 22.3.2020 – Bund und Länder einigen sich auf Kontaktbeschränkungen](https://orf.at/stories/3158944/)"
L_MULTI = "[Multipolar – RKI-Protokolle, Teil 5 (PDF)](https://multipolar-magazin.de/media/pdf/rki-protokolle-5.pdf)"
L_NPP = "[RKI – Nationaler Pandemieplan Teil II (PDF)](https://www.rki.de/DE/Content/Infekt/Preparedness_Response/Pandemieplan_Teil_II_gesamt.pdf?__blob=publicationFile)"
L_NPPC = "[RKI – Ergänzung zum Nationalen Pandemieplan, COVID-19, März 2020 (PDF)](https://ms.sachsen-anhalt.de/fileadmin/Bibliothek/Politik_und_Verwaltung/MS/MS/2_Gesundheit/200303_Corona-Ergaenzung_zum_Nationalen_Pandemieplan_Version_1.0.pdf)"
L_BMI = "[abgeordnetenwatch.de – Szenarienpapier „Wie wir COVID-19 unter Kontrolle bekommen“ im Volltext](https://www.abgeordnetenwatch.de/node/3582)"
L_DRS = "[Bundestag, Drucksache 19/28063 – Antwort der Bundesregierung zum Szenarienpapier (PDF)](https://dserver.bundestag.de/btd/19/280/1928063.pdf)"
L_HIB21 = "[Bundestag, hib 441/2021 – Covid-19-Szenarienpapier vom Frühjahr 2020](https://www.bundestag.de/presse/hib/832660-832660)"
L_ADHOC = "[apotheke adhoc – Seehofers Worst-Case-Szenario](https://www.apotheke-adhoc.de/nachrichten/detail/politik/corona-krise-seehofer-worst-case-szenario-interner-bericht-des-bmi/)"
L_NOS = "[NOS (Niederlande) – Bericht über die E-Mails zum Szenarienpapier](https://nos.nl/artikel/2369301-schokeffect-gewenst-ging-duits-ministerie-te-ver-bij-verkopen-van-coronabeleid)"
L_WHO = "[Deutsches Ärzteblatt, 19.5.2022 – WHO-Autoren korrigieren Daten für Deutschland und Schweden](https://www.aerzteblatt.de/n134232)"
L_LIND = "[Lindström 2024 – Sweden’s excess mortality in 2020–2022 (Scand. J. Public Health)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12048725/)"
L_UDE = "[Universität Duisburg-Essen – Sterbefälle Deutschland, Schweden, Spanien 2016–2020](https://www.uni-due.de/2021-10-21-keine-uebersterblichkeit-durch-corona)"
L_EBM = "[Netzwerk Evidenzbasierte Medizin – Übersterblichkeit in der Pandemie (PDF)](https://www.ebm-netzwerk.de/de/medien/pdf/ebm-09_22_kvh-journal_uebersterblichkeit.pdf)"
L_BLZ = "[Berliner Zeitung – Kolumne von Michael Andrick zum Buch](https://www.berliner-zeitung.de/article/die-omissions-kommission-der-schwurbler-10491501)"
L_BLZI = "[Berliner Zeitung – Interview: „Der 12. März 2020 war der Wendepunkt“](https://www.berliner-zeitung.de/article/10023903)"
L_TE = "[Tichys Einblick – Besprechung „Fünf Minuten gegen die Macht“](https://www.tichyseinblick.de/feuilleton/buecher/corona-enquete-kommission-bundestag/)"
L_FREI = "[der Freitag – Kommentar zur Besetzung der Enquete-Kommission](https://www.freitag.de/autoren/ulrike-baureithel/enquete-kommission-zur-corona-aufarbeitung-aufarbeitung-nicht-afd-ueberlassen)"
L_AEBS = "[Deutsches Ärzteblatt – Sachverständige für Enquete-Kommission benannt](https://www.aerzteblatt.de/themen/bundestag/sachverstandige-fur-enquetekommission-zu-coronaaufarbeitung-benannt-c29af17e-57d6-498c-a07e-b730efbb1d2c)"
L_NK = "[Nordkurier – Lesung zu „Die Untersuchung“](https://www.nordkurier.de/regional/uckermark/ein-gespraech-mit-kuenstlicher-intelligenz-um-zu-verstehen-2961385)"
L_UNT = "[Leseprobe „Die Untersuchung“ (PDF, Achgut Edition)](https://cdn-assets.versacommerce.de/agshop_versacommerce_de/mediafiles/images/Leseprobe_Ulrike-Tom-Lausen_Die-Untersuchung.pdf)"

# ---------------- Person ----------------
person = R("person", "Person",
    txt("**Tom Lausen** (geb. 1967 in Hamburg) ist Programmierer, Datenanalyst und Publizist. Seit 2020 wertet er öffentlich zugängliche Gesundheitsdaten aus – Krankenhaus-, Intensiv- und Abrechnungsdaten – und trägt die Ergebnisse als Sachverständiger in Parlamenten vor. Seit 2025 ist er sachverständiges Mitglied der Enquete-Kommission des Bundestages zur Aufarbeitung der Corona-Pandemie (benannt von der AfD-Fraktion) und der entsprechenden Kommission des Thüringer Landtags. " + L_BT),
    txt("Dieser Eintrag ist als **Sammelstelle für seine Vorträge und Gespräche** angelegt: Jedes ausgewertete Video bekommt eigene Reiter (Überblick, Vortrag im Detail, Zeitachse, Abgleich & Daten). Links steht, was er sagt, rechts daneben die gängige Darstellung bzw. die Daten mit Quelle. Die Bewertung bleibt dem Leser."),
    illu("lausen_kette", "Skizze: Vom Modell zur Maßnahme (schematisch, Darstellung laut Lausen)"),
    tab(["🧭 Stationen", "Was", "Quelle"],
        ["1967", "geboren in Hamburg", L_BT],
        ["seit 2020", "Auswertung von Gesundheitsdaten zur Corona-Zeit, gemeinsam mit seiner Frau Ulrike Lausen (Corona-Recherchegruppe)", L_NK],
        ["Juli 2021", "Sachverständiger im Parlamentarischen Begleitgremium COVID-19-Pandemie des Bundestages", L_NK],
        ["2021", "Buch „Die Intensiv-Mafia“ (mit Walter van Rossum)", L_BT],
        ["2022–2025", "Geladener Sachkundiger und Sachverständiger in den Landtagen von Thüringen, Sachsen und Rheinland-Pfalz", L_BT],
        ["2022, 2024", "Parteisachverständiger vor dem Bundesverwaltungsgericht Leipzig in Verfahren zur Covid-19-Impfpflicht bei Soldaten", L_BT],
        ["2024", "Buch „Die Untersuchung“ (mit Ulrike Lausen)", L_UNT],
        ["seit 2025", "Mitglied der Enquete-Kommissionen „Corona“ des Thüringer Landtags und des Deutschen Bundestages", L_BT],
        ["2026", "Buch „5 Minuten gegen die Macht“ (mit Ulrike Lausen, Westend Verlag)", L_TE]),
    abs_("Kurz zusammengefasst", [
        "Arbeitsweise: amtliche und abrechnungsbezogene Daten selbst auswerten und daraus Fragen an Behörden und Politik ableiten.",
        "Kernthese [seine Sicht]: Die Corona-Maßnahmen beruhten weniger auf gemessenen Daten als auf Modellrechnungen für den schlimmsten Fall.",
        "Rolle: sachverständiges Mitglied der Enquete-Kommission des Bundestages; dort stehen je Fragesteller fünf Minuten für Frage und Antwort zur Verfügung – daher der Buchtitel.",
        "In derselben Kommission sitzt auch {{a:nehls|Dr. Michael Nehls (A-01)}} als Sachverständiger."]),
    tab(["🗞️ Stimmen zu Person und Buch", "Inhalt in Kürze", "Quelle"],
        ["Bundestag", "Führt ihn als „Datenanalyst und Publizist“; in der Meldung zur Konstituierung als „Buchautor und Datenanalyst“.", L_KONST],
        ["Berliner Zeitung (Interview)", "Lausen nennt den 12. März 2020 den Wendepunkt für den weiteren Verlauf der Maßnahmen.", L_BLZI],
        ["Berliner Zeitung (Kolumne Andrick)", "Bespricht das Buch zustimmend als Innenansicht der Kommission.", L_BLZ],
        ["Tichys Einblick", "Besprechung des Buchs; beschreibt ihn als datenorientierten Kritiker der Corona-Politik.", L_TE],
        ["der Freitag (Kommentar Baureithel)", "Sieht die Besetzung der Kommission kritisch; zu Lausens Stellungnahme über Daten zu Impfnebenwirkungen heißt es dort, darüber könne man diskutieren.", L_FREI],
        ["Deutsches Ärzteblatt", "Meldet die Benennung der Sachverständigen; die AfD-Fraktion kündigte Nehls, Homburg und Lausen an.", L_AEBS]),
)
person["bloecke"][-1]["stapel"] = True

# ---------------- Bücher ----------------
buecher = R("buecher", "Bücher",
    txt("Angaben nach Bundestag, Verlags- und Presseangaben; Inhalte in eigenen Worten. Stand: November 2026."),
    karten("buch", [
        {"id": "fuenfminuten", "titel": "5 Minuten gegen die Macht – Was über Corona ans Licht kommt und was im Protokoll verschwinden soll", "kat": "alle", "jahr": "2026", "verlag": "Westend Verlag",
         "kurz": "Mit Ulrike Lausen. Bericht aus der Enquete-Kommission des Bundestages, auch aus dem nicht öffentlichen Teil.",
         "zutaten": ["Paperback, 230 Seiten, 25,00 €", "Titel bezieht sich auf die fünf Minuten Frage- und Antwortzeit je Fragesteller"],
         "schritte": ["Schildert Befragungen von Fachleuten in der Kommission, darunter die frühere Direktorin der EU-Behörde ECDC.",
                      "These [seine Sicht]: Die Kommission in ihrer jetzigen Form könne die Corona-Jahre nicht aufarbeiten.",
                      "Anliegen: Inhalte festhalten, die sonst nur in Akten der Bundestagsverwaltung stehen."]},
        {"id": "untersuchung", "titel": "Die Untersuchung", "kat": "alle", "jahr": "2024", "verlag": "Achgut Edition",
         "kurz": "Mit Ulrike Lausen „und die KI“: Fragen zur Corona-Zeit werden einer künstlichen Intelligenz vorgelegt, die Antworten hinterfragt.",
         "zutaten": ["ISBN 978-3-9825848-0-5", "laut Bundestag ein Spiegel-Bestseller"],
         "schritte": ["Form: Dialog mit ChatGPT statt Streitgespräch zwischen Menschen.",
                      "Anspruch laut Buch: neutral gegenüber beiden Seiten der Corona-Debatte."]},
        {"id": "intensivmafia", "titel": "Die Intensiv-Mafia", "kat": "alle", "jahr": "2021", "verlag": "",
         "kurz": "Mit Walter van Rossum. Auswertung der Daten zu Intensivbetten und deren Finanzierung in der Corona-Zeit.",
         "zutaten": ["laut Bundestag ein Spiegel-Bestseller"],
         "schritte": ["Grundlage waren seine Recherchen zu Intensivkapazitäten, die er im Juli 2021 auch im Bundestag vortrug."]}]),
)

# ---------------- Kernideen ----------------
kern = R("kernideen", "Kernideen",
    txt("Seine Leitgedanken – als Wiedergabe seiner Sicht, bisher aus dem ersten ausgewerteten Video. Wird mit jedem weiteren Transkript ergänzt."),
    abs_("1. Erst die Daten, dann die Deutung", ["Ausgangspunkt sind amtliche Zahlen (Krankenhausfälle, Belegung, Mobilität). Aus Abweichungen zwischen Zahlen und öffentlicher Darstellung leitet er seine Fragen ab [seine Sicht]. [0:03]"]),
    abs_("2. „Fiktionen“ und unvollständige Information", ["Er nennt Annahmen ohne Messgrundlage „Fiktionen“; unvollständige Information sei das, wovon solche Lagen leben [seine Sicht]. [0:00]"]),
    abs_("3. Modellierung als Entscheidungsgrundlage", ["Worst-Case-Rechnungen hätten Regierungen in vielen Ländern zu Lockdowns bewegt; die Annahmen seien dabei auf ein Ziel hin eingestellt worden [seine Sicht]. [0:09]"]),
    abs_("4. Abbruchlogik", ["Wenn Daten zeigen, dass eine Maßnahme nichts mehr verändert, müsse sie beendet werden. Für den März 2020 nennt er die Mobilitätsdaten als solchen Punkt [seine Sicht]. [0:08]"]),
    abs_("5. Festhalten, was sonst verschwindet", ["Nicht öffentliche Befragungen sollen nachlesbar bleiben – deshalb das Buch [seine Sicht]. [0:14]"]),
)

# ---------------- Video 1 ----------------
THEMEN = [{"k": "a", "n": "Enquete & Buch"}, {"k": "b", "n": "Fiktion & Panik"}, {"k": "c", "n": "Kliniken & Schweden"}, {"k": "d", "n": "RKI-Protokolle & Mobilität"}, {"k": "e", "n": "Modellierung"}]
AB = [
 ("🎬 Vorstellung: Enquete-Kommission und neues Buch", "0:00", "0:01", "a", [
   "Lausen stellt sich als Mitglied der Bundestags-Kommission zur Aufarbeitung der Corona-Zeit vor und kündigt beim Westend Verlag sein neues Buch an. Die Kommission hält er für nicht fähig, die drei Jahre aufzuarbeiten [seine Sicht].",
   "📌 Leitbegriff des Vortrags: „Fiktionen“ – Annahmen, mit denen die Menschen nach seiner Darstellung drei Jahre lang gebunden wurden. [0:00]",
   "📚 Die Kommission wurde am 10. Juli 2025 eingesetzt und hat sich am 8. September 2025 konstituiert: 14 Abgeordnete und 14 Sachverständige. " + L_KONST]),
 ("😨 „Fiktionen“ und Panik über die Medien", "0:01", "0:02", "b", [
   "Hinter den „Fiktionen“ stehe als Instrument die Panikmache, verbreitet über die Medien. Ganze Länder hätten sich gleich verhalten; an einen falschen Alarm habe kaum jemand gedacht, weil alle dasselbe taten [seine Sicht].",
   "💬 „Es ist schön einfach, Fiktionen den Menschen nahezubringen“ (Lausen) [0:01]",
   "📌 Das müsse eigentlich in der Kommission aufgearbeitet werden; das geschehe nicht [seine Sicht]. [0:02]"]),
 ("🏛️ Nicht öffentlicher Teil: Gespräch mit der früheren ECDC-Direktorin", "0:02", "0:03", "a", [
   "Als sachverständiges Mitglied nimmt er auch an nicht öffentlichen Sitzungen teil. Er berichtet von einer Befragung der früheren Direktorin der EU-Seuchenbehörde ECDC, Dr. Ammon; dafür hatte er fünf Minuten. Daraus leitet er den Buchtitel ab.",
   "📌 Seine Deutung: Auch auf europäischer Ebene habe es Unwissenheit gegeben – „Unwissenheit aus Gehorsam“ [seine Sicht]. [0:03]",
   "📚 ECDC = Europäisches Zentrum für die Prävention und die Kontrolle von Krankheiten (Stockholm); Andrea Ammon leitete es von 2017 bis 2024. Die Behörde berät, die Entscheidungen treffen die Mitgliedstaaten (ohne geprüften Link)."]),
 ("🏥 Die Frage: Sind Kliniken in einer Pandemie unterbelegt?", "0:03", "0:05", "c", [
   "Er fragte die ECDC-Vertreterin, ob es typisch sei, dass Krankenhäuser in einer Pandemie historisch unterbelegt sind. Für Deutschland nennt er rund 2,5 Millionen Krankenhausfälle weniger im Jahr 2020. Den Einwand, das liege an den Maßnahmen, weist er mit Schweden zurück: Dort habe es fast keine Maßnahmen gegeben und ebenfalls eine historische Unterbelegung [seine Sicht].",
   "💬 „Ist es typisch in einer Pandemie, dass die Krankenhäuser historisch unterbelegt sind?“ (Lausen) [0:03]",
   "📌 Schweden: keine Maskenpflicht, kein Lockdown, keine Schulschließungen für die unteren Klassen. [0:04]",
   "📚 Destatis: 2020 rund 2,5 Millionen stationäre Fälle weniger als 2019 (−13 %); als Gründe nennt das Amt freigehaltene Betten und verschobene planbare Behandlungen. " + L_DEST20]),
 ("📋 Pandemiepläne: Appelle statt Zwang", "0:05", "0:06", "c", [
   "Den Hinweis auf Unterschiede zu Schweden (etwa mehr Homeoffice), den er Christian Drosten zuschreibt, hält er für nicht stichhaltig. Vor Covid-19 hätten die Pandemiepläne Appelle vorgesehen: Abstand halten, Kranke erkennen, bei Krankheit zu Hause bleiben. Das sei außer in Schweden ignoriert worden [seine Sicht].",
   "🔗 Pandemiepläne: " + L_NPP + " und " + L_NPPC]),
 ("📑 RKI-Krisenstab am 18. und 20. März 2020", "0:06", "0:07", "d", [
   "Er zitiert aus den Protokollen des RKI-Krisenstabs: Am 18. März sei diskutiert worden, ob Ausgangssperren das Infektionsrisiko senken; Appelle zum Abstandhalten seien sinnvoller, Ausgangssperren ein letztes Mittel der Politik. Das RKI solle sich nicht aktiv dagegen positionieren. Am 20. März stehe dort der Hinweis des Gesundheitsministeriums, das RKI solle nichts zu Ausgangssperren sagen.",
   "💬 „Es ist ein Mittel der Politik, es ist kein Mittel der Epidemiologie.“ (Lausen) [0:07]",
   "❓ Der Wortlaut der Protokollstellen ist hier nach dem Vortrag wiedergegeben und nicht gegen das Originalprotokoll geprüft."]),
 ("📶 Mobilität minus 40 Prozent – vor dem Lockdown", "0:07", "0:09", "d", [
   "Durch die Appelle sei die Mobilität schon vor dem Lockdown um 40 Prozent gesunken; das RKI habe Mobilfunkdaten von Telefónica zu rund 40 Millionen Nutzern gehabt. Im Lockdown sei die Mobilität nicht weiter gefallen, sondern wieder gestiegen. Das wäre der Punkt für eine „Abbruchlogik“ gewesen [seine Sicht].",
   "📌 In Schweden sei die Mobilität ebenfalls gesunken, aber weniger stark. [0:08]",
   "📚 Das Mobilitätsprojekt von RKI und HU Berlin beschreibt für Mitte März 2020 ein Plateau von etwa 40 % weniger Fahrten als üblich. " + L_MOB]),
 ("🧮 „Politische Pandemie“ und Worst-Case-Modelle", "0:09", "0:10", "e", [
   "Er spricht von einer „politischen Pandemie“, die von der Modellierung des schlimmsten Falls gelebt habe. Solche Modellrechnungen seien Staatslenkern weltweit vorgelegt worden – in den USA Präsident Trump durch Dr. Birx. Da es Lockdowns zuvor nie gegeben habe, habe man deren Wirkung nicht aus Erfahrung kennen können [seine Sicht].",
   "💬 „Modellierungen zeigen eine Welt, die in der Fantasie der Modellierer stattfindet.“ (Lausen) [0:09]",
   "❓ „Berks“ im Transkript: gemeint ist vermutlich Deborah Birx, Koordinatorin des Corona-Stabs im Weißen Haus."]),
 ("✉️ E-Mails zum Szenarienpapier des Innenministeriums", "0:10", "0:13", "e", [
   "Er liest aus E-Mails vom 20. März 2020 rund um das Papier vor, das er „Panikpapier“ nennt: Staatssekretär Markus Kerber dankt für ein Best-Case-Modell mit 126.000 Toten und schreibt zum Worst Case „whatever it takes“. In weiteren Mails gehe es darum, die Annahmen so einzustellen, dass am Ende eine Sterblichkeit von etwa 1,2 % der Infizierten herauskommt; die Letalität milder Fälle werde auf 0 % gesetzt, im Worst Case bleibe es bei über einer Million Toten.",
   "💬 „Liegen wir damit völlig falsch?“ (aus einer E-Mail, laut Lausen) [0:11]",
   "📌 Sein Schluss: Die Modellierer hätten ihre Annahmen nicht sorgfältig begründet [seine Sicht]. [0:12]",
   "❓ „Anderheiden“ im Transkript: gemeint ist vermutlich Matthias an der Heiden (RKI).",
   "📚 Das Papier heißt „Wie wir COVID-19 unter Kontrolle bekommen“. Laut Bundesregierung war die Autorengruppe kein Gremium des Ministeriums, Zielvorgaben habe es nicht gegeben. " + L_DRS]),
 ("🌍 Prognosen in anderen Ländern", "0:13", "0:14", "e", [
   "Am 5. März 2020 habe das RKI eine Modellierung herausgeben sollen, die das Gesundheitsministerium für gut befand, deren Veröffentlichung es aber untersagt habe; damit seien die Ministerpräsidenten zur Schulschließung bewegt worden. Aus Büchern von Gesundheitsministern nennt er erwartete Todeszahlen ohne Lockdown: Frankreich 300.000–500.000 (Véran), Schweden 85.000 (Tegnell; tatsächlich nach seiner Angabe 5.000), Italien 100.000 (Speranza), Schweiz 100.000 (Berset), Deutschland 400.000 (Spahn).",
   "📌 Rudolf Anschober (Österreich) habe sich in seinem Buch „Pandemia“ an die Zahl nicht erinnert. [0:14]",
   "❓ Die einzelnen Zahlen und Buchstellen sind hier nicht nachgeprüft."]),
 ("📚 Das Buch als Archiv – und der Ausblick", "0:14", "0:16", "a", [
   "In der Kommission stelle er die Unwissenheit vieler Beteiligter fest. Das Buch, geschrieben mit seiner Frau, halte nicht öffentliche Inhalte fest; in der Bundestagsverwaltung werde bereits gestrichen und gelöscht, auch Tonaufnahmen [seine Sicht]. Er rechnet mit weiteren Alarmmeldungen und nennt als Beispiel Berichte über Lungenpest.",
   "💬 „Diese Panikmache wird weitergehen.“ (Lausen) [0:15]",
   "❓ Die Angaben zu gelöschten Tonaufnahmen und Protokollstellen sind hier nicht geprüft; die Wortprotokolle der öffentlichen Sitzungen stehen online. " + L_PROT]),
]
teile = [{"von": v, "bis": b, "t": t.split(" ", 1)[1], "th": th} for t, v, b, th, _ in AB]
abschn = []
for t, v, b, th, l in AB:
    a = abs_(f"{t} [{v}–{b}]", l); a["th"] = th; abschn.append(a)

ZA = [
 ("2005–2017", 2005, "Nationaler Pandemieplan für Deutschland (erste Fassung 2005, überarbeitet 2017)", "", True),
 ("5.3.2020", 2020, "RKI soll eine Modellierung herausgeben; laut Lausen untersagt das Gesundheitsministerium die Veröffentlichung", "[0:13]", False),
 ("10.3.2020", 2020, "Krisenstab von Innen- und Gesundheitsministerium empfiehlt die Absage von Veranstaltungen über 1.000 Teilnehmer", "", True),
 ("16.3.2020", 2020, "RKI-Vizepräsident Schaade: Das RKI empfehle keine Einzelmaßnahmen, die Entscheidung liege bei der Politik", "", True),
 ("18.3.2020", 2020, "RKI-Krisenstab diskutiert laut Protokoll, ob Ausgangssperren das Infektionsrisiko senken", "[0:06]", False),
 ("19.3.2020", 2020, "Staatssekretär Kerber bittet Wissenschaftler um Mitarbeit am Szenarienpapier", "", True),
 ("20.3.2020", 2020, "Protokoll: Hinweis des Gesundheitsministeriums, das RKI solle nichts zu Ausgangssperren sagen; E-Mails zu Best Case und Worst Case", "[0:07]", False),
 ("22.3.2020", 2020, "Bund und Länder beschließen Kontaktbeschränkungen – bei Lausen „der Lockdown“", "[0:06]", False),
 ("Ende März 2020", 2020, "Szenarienpapier „Wie wir COVID-19 unter Kontrolle bekommen“ wird durch Medienberichte bekannt", "", True),
 ("2020", 2020, "Rund 2,5 Millionen Krankenhausfälle weniger als im Vorjahr", "[0:04]", False),
 ("Juli 2021", 2021, "Lausen als Sachverständiger im Parlamentarischen Begleitgremium des Bundestages", "", True),
 ("2024", 2024, "RKI-Krisenstabsprotokolle werden nach einer Klage des Magazins Multipolar öffentlich", "", True),
 ("10.7.2025", 2025, "Bundestag setzt die Enquete-Kommission zur Aufarbeitung der Corona-Pandemie ein", "", True),
 ("8.9.2025", 2025, "Die Kommission konstituiert sich; Lausen ist einer von 14 Sachverständigen", "[0:00]", False),
 ("7.5.2026", 2026, "Öffentliche Anhörung „Lehren für Schutzmaßnahmen bei künftigen Pandemien“", "", True),
 ("2026", 2026, "Buch „5 Minuten gegen die Macht“ erscheint im Westend Verlag; Vorstellung im Video", "[0:02]", False),
]

abg = tab(["Aussage im Video", "Gängige Darstellung (Mainstream) / Daten 📚", "Quelle"],
 ["2020 kamen in Deutschland 2,5 Millionen Fälle weniger in die Krankenhäuser; die Kliniken waren historisch unterbelegt. [0:04]",
  "Destatis bestätigt die Größenordnung: 2020 rund 2,5 Millionen stationäre Fälle weniger als 2019 (−13 %), Bettenauslastung 68,8 % statt 77,2 %. Als Ursache nennt das Amt freigehaltene Betten für Covid-19-Fälle und verschobene planbare Behandlungen. Laut Ärzteblatt war der Rückgang umso stärker, je weniger dringend eine Behandlung war; Covid-19-Fälle machten 2020 rund 2 % der Belegungstage aus.",
  L_DEST20 + " · " + L_AEZ + " · " + L_AEB],
 ["In einer Pandemie wären volle Krankenhäuser zu erwarten. [0:03]",
  "Die Statistikämter sehen den Rückgang als Folge der Pandemie-Organisation (Freihalten, Verschieben, weniger Notfallbesuche). Die Fallzahlen blieben auch danach niedrig: 2025 lagen sie 9,4 % unter 2019; das BARMER-Institut spricht von dauerhaft verändertem Inanspruchnahmeverhalten.",
  L_DEST21 + " · " + L_DEST25 + " · " + L_BIFG],
 ["Schweden hatte fast keine Maßnahmen und ebenfalls eine historische Unterbelegung der Kliniken. [0:04]",
  "Schweden verzichtete auf Lockdown und Maskenpflicht und setzte überwiegend auf Empfehlungen; es gab aber Regeln wie Obergrenzen für Versammlungen und Fernunterricht für Ältere (ohne geprüften Link). ❓ Zur Klinikbelegung in Schweden 2020 liegt hier keine geprüfte Quelle vor. Übersterblichkeit 2020/21 laut korrigierter WHO-Schätzung: Deutschland 73, Schweden 66 je 100.000 Einwohner; in Schweden fiel der größte Teil auf 2020.",
  L_WHO + " · " + L_LIND + " · " + L_UDE],
 ["Pandemiepläne sahen Appelle vor (Abstand, Kranke bleiben zu Hause), keine Lockdowns. [0:05]",
  "Der Nationale Pandemieplan und seine Covid-19-Ergänzung vom März 2020 beschreiben Stufen von Maßnahmen; welche davon angemessen waren, ist Gegenstand der Enquete-Kommission (Anhörung „Lehren für Schutzmaßnahmen“, Mai 2026).",
  L_NPP + " · " + L_NPPC + " · " + L_ANH],
 ["RKI-Protokoll 18.3.2020: Ausgangssperren seien ein Mittel der Politik; das RKI solle sich nicht dagegen positionieren. 20.3.: Hinweis des Ministeriums, nichts dazu zu sagen. [0:06]",
  "Die Protokolle des Krisenstabs sind seit 2024 öffentlich. Öffentlich sagte RKI-Vizepräsident Schaade am 16.3.2020, das RKI empfehle generell keine Einzelmaßnahmen, die Entscheidung liege bei den politisch Verantwortlichen; grundsätzlich sei alles gut, was Abstand bringe. ❓ Wortlaut der zitierten Protokollstellen hier nicht gegen das Original geprüft.",
  L_SCHAADE + " · " + L_AEB16 + " · " + L_MULTI],
 ["Die Mobilität war schon vor dem Lockdown um 40 % gesunken; das RKI hatte Telefónica-Daten. Im Lockdown stieg sie wieder. [0:07]",
  "Das Mobilitätsprojekt von RKI und HU Berlin (Mobilfunkdaten) zeigt ab Mitte März 2020 ein Plateau von etwa 40 % weniger Fahrten. Destatis veröffentlicht Mobilitätsindikatoren aus Mobilfunkdaten. Die bundesweiten Kontaktbeschränkungen wurden am 22.3.2020 beschlossen. ❓ Ob die Mobilität danach wieder stieg, ist hier nicht mit Zahlen geprüft.",
  L_MOB + " · " + L_DESTMOB + " · " + L_ORF],
 ["Im Szenarienpapier des Innenministeriums wurden Annahmen auf rund 1,2 % Sterblichkeit „kalibriert“; Worst Case über eine Million Tote. [0:10]",
  "Das Papier nennt für den Fall ohne Gegenmaßnahmen über eine Million Tote 2020 und für das Szenario mit Testen und Isolieren rund 12.000 Tote bei 1,2 % Sterblichkeit. Der niederländische Sender NOS berichtet aus den E-Mails, dass Modelle kalibriert und Annahmen zur Sterblichkeit milder Fälle verschoben wurden. Die Bundesregierung erklärte, die Wissenschaftlergruppe sei kein Gremium des Ministeriums gewesen; Zielvorgaben oder Einflussnahme habe es nicht gegeben.",
  L_BMI + " · " + L_NOS + " · " + L_DRS + " · " + L_ADHOC],
 ["Best-Case-Modell mit 126.000 Toten, „einer schweren Grippe“ entsprechend (E-Mail Kerber). [0:10]",
  "❓ Diese E-Mail-Stelle ist hier nicht im Original geprüft. Das veröffentlichte Papier selbst nennt als günstigstes Szenario rund 12.000 Tote.",
  L_ADHOC + " · " + L_HIB21],
 ["Eine RKI-Modellierung vom 5.3.2020 durfte nicht veröffentlicht werden und bewegte die Ministerpräsidenten zur Schulschließung. [0:13]",
  "❓ Hier nicht geprüft; keine Quelle gefunden.", "–"],
 ["Erwartete Tote ohne Lockdown: Frankreich 300.000–500.000, Schweden 85.000, Italien 100.000, Schweiz 100.000, Deutschland 400.000. [0:13]",
  "❓ Die einzelnen Zahlen und Buchstellen sind hier nicht nachgeprüft.", "–"],
 ["Die Enquete-Kommission ist nicht fähig, die Corona-Zeit aufzuarbeiten. [0:00]",
  "Auftrag laut Bundestag: Aufarbeitung der Pandemie und Lehren für künftige pandemische Ereignisse; 14 Abgeordnete und 14 Sachverständige, öffentliche Anhörungen mit Wortprotokollen. Über die Arbeit der Kommission gibt es unterschiedliche Urteile – zustimmend zu Lausens Sicht etwa die Kolumne in der Berliner Zeitung, kritisch zur Besetzung der Kommentar im Freitag.",
  L_TEXT + " · " + L_PROT + " · " + L_BLZ + " · " + L_FREI],
 ["In der Bundestagsverwaltung werden Protokollstellen gestrichen und Tonaufnahmen gelöscht. [0:15]",
  "❓ Hier nicht geprüft. Die Buchbesprechung bei Tichys Einblick gibt wieder, dass von nicht öffentlichen Sitzungen kein Wortprotokoll, sondern eine Zusammenfassung angefertigt werde.",
  L_TE],
)
abg["stapel"] = True

faelle = {"typ": "kurs", "id": "lausen-khfaelle", "titel": "📈 Stationäre Krankenhausfälle in Deutschland",
  "reihen": [{"name": "Krankenhausfälle", "kurz": "Fälle", "einheit": "Mio.", "dez": 1, "hoeherGut": None,
              "punkte": [[2015, 19.2], [2019, 19.4], [2020, 16.8], [2021, 16.7], [2022, 16.8], [2023, 17.2], [2024, 17.5], [2025, 17.7]]}],
  "hoeherGut": None,
  "quelle": "Statistisches Bundesamt (Destatis), Grunddaten der Krankenhäuser; Werte nach " + L_DEST25 + ", " + L_BIFG + ", " + L_THIEME + ", " + L_MYDRG + ", " + L_ONKO + ", " + L_STAT + ". Stand: Oktober 2026.",
  "hinweis": "Bezug zum Video [0:04]: Lausen nennt 2,5 Millionen Fälle weniger im Jahr 2020. Zwischen 2015 und 2019 lagen die Werte laut Destatis jedes Jahr über 19 Millionen; die Zwischenjahre sind hier nicht einzeln eingetragen."}
betten = {"typ": "balken", "titel": "📊 Bettenauslastung der Krankenhäuser", "einheit": "%", "dez": 1,
  "zeilen": [["2019", 77.2], ["2020", 68.8], ["2023", 71.2], ["2024", 72.0], ["2025", 72.6]],
  "quelle": L_AEZ + ", " + L_AEB24 + ", " + L_DEST25 + " (jeweils nach Destatis). Stand: Oktober 2026.",
  "hinweis": "Bezug zum Video [0:03]: „historisch unterbelegt“. Der Wert 2023 ergibt sich aus der Destatis-Angabe „2024 um 0,8 Prozentpunkte höher“."}
ueber = {"typ": "balken", "titel": "📊 Übersterblichkeit 2020 und 2021 je 100.000 Einwohner (WHO-Schätzung)", "einheit": "", "dez": 0,
  "zeilen": [["Deutschland – korrigiert", 73], ["Schweden – korrigiert", 66], ["Deutschland – erste Fassung", 116], ["Schweden – erste Fassung", 56]],
  "quelle": L_WHO + ". Stand: Mai 2022.",
  "hinweis": "Bezug zum Video [0:04]: Vergleich Deutschland–Schweden. Die WHO-Autoren haben ihre erste Schätzung für beide Länder korrigiert; andere Rechenwege kommen zu abweichenden Reihenfolgen. " + L_EBM}
vgl = {"typ": "vergleich", "titel": "⚖️ Zahlen im Video und Daten nebeneinander", "la": "Im Video genannt", "lb": "Daten laut Quelle",
  "zeilen": [
    {"n": "Krankenhausfälle weniger im Jahr 2020", "a": 2.5, "b": 2.5, "einheit": "Mio.", "dez": 1, "f": "[0:04]", "q": L_DEST20 + " (Vergleich mit 2019)"},
    {"n": "Rückgang der Mobilität Mitte März 2020", "a": 40, "b": 40, "einheit": "%", "dez": 0, "f": "[0:07]", "q": L_MOB + " (etwa −40 % Fahrten)"},
    {"n": "Worst Case im Szenarienpapier", "a": 1.0, "b": 1.0, "einheit": "Mio. Tote", "dez": 1, "at": "über 1 Mio.", "bt": "über 1 Mio.", "f": "[0:12]", "q": L_BMI},
    {"n": "Sterblichkeit je Infizierte im Szenarienpapier", "a": 1.2, "b": 1.2, "einheit": "%", "dez": 1, "f": "[0:11]", "q": L_ADHOC},
    {"n": "Günstigstes Szenario (Tote)", "a": 126000, "b": 12000, "einheit": "", "dez": 0, "f": "[0:10]", "q": L_ADHOC + " – im Video „Best Case“ aus einer E-Mail, im Papier das Szenario mit Testen und Isolieren"}]}

v_ueber = R(K, G + ": Überblick",
    {"typ": "folge", "k": K, "titel": VT, "gast": "Tom Lausen", "rolle": "Datenanalyst, Sachverständiger der Enquete-Kommission", "kanal": "Westend Verlag", "art": "Vortrag", "karte": "Westend Verlag · Buchvorstellung",
     "datum": "2026 ❓", "dauer": "16 Min.", "url": URL,
     "thema": "Kurzvortrag zur Buchvorstellung: Warum die Corona-Maßnahmen nach seiner Sicht auf Modellannahmen statt auf Daten beruhten – und was die Enquete-Kommission offen lässt.",
     "wege": [[K + "ab", "📖", "Vortrag im Detail", "Abschnitt für Abschnitt, mit Zitaten"], [K + "zeit", "📅", "Zeitachse & Verzeichnisse", "Ereignisse, Personen, Begriffe, Zahlen"], [K + "abgleich", "⚖️", "Abgleich & Daten", "Diagramme, Aussagen neben Daten, Quellen"]]},
    hin("Auswertung nach dem Transkript (automatische Untertitel): Gesagtes ohne Zeichen, Ergänzungen 📚, Unklares ❓. Fundstellen [Stunde:Minute] springen ins Video. Die Bewertung bleibt dem Leser."),
    abs_("⚡ In Kürze", [
        "Lausen stellt sein Buch „5 Minuten gegen die Macht“ vor und berichtet aus der Enquete-Kommission des Bundestages.",
        "Leitbegriff ist die „Fiktion“: Annahmen und Modellrechnungen, die nach seiner Sicht die Maßnahmen trugen.",
        "Datenpunkt 1: 2020 rund 2,5 Millionen Krankenhausfälle weniger – für ihn unvereinbar mit dem Bild einer Pandemie.",
        "Datenpunkt 2: Die Mobilität sei schon vor dem 22. März 2020 um 40 % gesunken; der Lockdown sei nicht mehr nötig gewesen.",
        "Beleg aus Akten: RKI-Krisenstabsprotokolle vom 18. und 20. März 2020 und E-Mails zum Szenarienpapier des Innenministeriums.",
        "Vergleich: Schweden als Land, das nach Pandemieplan gehandelt habe.",
        "Schluss: Das Buch soll nicht öffentliche Inhalte der Kommission festhalten."]),
    txt("🎯 **Kernaussagen** – die wichtigsten Thesen des Vortrags:"),
    tab(["#", "Aussage", "Begründung im Video", "Fundstelle", "Gewicht"],
        ["1", "Die Corona-Zeit beruhte auf „Fiktionen“ und unvollständiger Information.", "Panik über Medien, niemand rechnete mit falschem Alarm", "[0:00]", "★★★"],
        ["2", "Die Enquete-Kommission kann das nicht aufarbeiten.", "Erfahrungen aus den Sitzungen, fünf Minuten Fragezeit", "[0:00]", "★★"],
        ["3", "Kliniken waren 2020 historisch unterbelegt.", "2,5 Millionen Fälle weniger", "[0:04]", "★★★"],
        ["4", "Schweden zeigt, dass es nicht an den Maßnahmen lag.", "Dort ebenfalls Unterbelegung, ohne Lockdown", "[0:04]", "★★"],
        ["5", "Pandemiepläne sahen Appelle vor, keine Lockdowns.", "Verweis auf Pläne von WHO und Ländern", "[0:05]", "★★"],
        ["6", "Das RKI sah Ausgangssperren skeptisch und sollte schweigen.", "Protokolle vom 18. und 20. März 2020", "[0:06]", "★★★"],
        ["7", "Die Mobilität war vor dem Lockdown schon um 40 % gesunken.", "Mobilfunkdaten von Telefónica", "[0:07]", "★★★"],
        ["8", "Es fehlte eine Abbruchlogik.", "Mobilität stieg im Lockdown wieder", "[0:08]", "★★"],
        ["9", "Modellrechnungen wurden auf ein Ziel hin eingestellt.", "E-Mails zum Szenarienpapier", "[0:10]", "★★★"],
        ["10", "In ganz Europa wurden hohe Todeszahlen ohne Lockdown angekündigt.", "Bücher von Gesundheitsministern", "[0:13]", "★★"]),
    {"typ": "baum", "titel": "🌳 Themenbaum des Vortrags", "wurzel": VT, "unter": "Tom Lausen · Westend Verlag · 2026 · 16 Min.",
     "knoten": [
        {"t": "🏛️ Enquete & Buch", "k": [{"t": "Kommission des Bundestages [0:00]"}, {"t": "Fünf Minuten Fragezeit [0:03]"}, {"t": "Buch als Archiv [0:14]"}]},
        {"t": "😨 Fiktion & Panik", "k": [{"t": "Leitbegriff „Fiktionen“ [0:00]"}, {"t": "Panik über Medien [0:01]"}, {"t": "Ausblick: weitere Alarme [0:15]"}]},
        {"t": "🏥 Kliniken & Schweden", "k": [{"t": "2,5 Mio. Fälle weniger [0:04]"}, {"t": "Schweden ohne Lockdown [0:04]"}, {"t": "Pandemiepläne: Appelle [0:05]"}]},
        {"t": "📑 RKI-Protokolle & Mobilität", "k": [{"t": "Krisenstab 18.3. [0:06]"}, {"t": "Hinweis des Ministeriums 20.3. [0:07]"}, {"t": "Mobilität −40 % [0:07]"}, {"t": "Abbruchlogik [0:08]"}]},
        {"t": "🧮 Modellierung", "k": [{"t": "Worst Case [0:09]"}, {"t": "E-Mails zum Szenarienpapier [0:10]"}, {"t": "Kalibrierung auf 1,2 % [0:11]"}, {"t": "Prognosen anderer Länder [0:13]"}]}]},
    illu("lausen_maerz", "Skizze: März 2020 – die im Video genannten Daten (Darstellung laut Lausen, Kurve schematisch)"),
    tab(["🧭 Steckbrief", ""],
        ["Thema in einem Satz", "Buchvorstellung mit Kurzvortrag über Daten, Modelle und die Aufarbeitung der Corona-Zeit."],
        ["Titel", VT + " | Tom Lausen"],
        ["Format", "Monolog vor der Kamera im Westend Verlag, ohne Gesprächspartner; Buchwerbung am Schluss"],
        ["Sprecher", "Tom Lausen"],
        ["Dauer", "ca. 16 Minuten"],
        ["Datum", "2026 ❓ (genaues Veröffentlichungsdatum nicht ermittelt)"],
        ["Grundton", "sachlich vortragend, zugespitzt in den Schlussfolgerungen"]),
)
v_ueber["bloecke"][-1]["schmal"] = True

v_ab = R(K + "ab", G + ": Vortrag im Detail",
    txt("Elf Abschnitte in der Reihenfolge des Vortrags. Lesehilfe: 💬 Zitat · 📌 Aussage · 🔗 Bezug · 📚 Ergänzung · ❓ unklar."),
    {"typ": "gespraech", "titel": "🧭 Verlauf – wann worüber gesprochen wird", "dauer": "0:16", "themen": THEMEN, "teile": teile},
    *abschn)

v_zeit = R(K + "zeit", G + ": Zeitachse & Verzeichnisse",
    {"typ": "zeitachse", "titel": "📅 Zeitachse – Ereignisse, die im Vortrag vorkommen",
     "eintraege": [dict({"z": z, "j": j, "t": t, "e": e}, **({"f": f} if f else {})) for z, j, t, f, e in ZA]},
    tab(["👤 Person", "Wer / was", "Rolle im Vortrag", "Fundstelle"],
        ["Tom Lausen", "Datenanalyst, Sachverständiger der Enquete-Kommission", "Sprecher", "[0:00]"],
        ["Ulrike Lausen", "Mitautorin, seine Frau", "Buch gemeinsam geschrieben", "[0:14]"],
        ["Dr. Andrea Ammon", "frühere Direktorin des ECDC", "von ihm in der Kommission befragt", "[0:02]"],
        ["Christian Drosten", "Virologe", "ihm zugeschrieben: Schweden sei nicht vergleichbar", "[0:05]"],
        ["Markus Kerber", "damals Staatssekretär im Innenministerium", "E-Mail zum Best Case und Worst Case", "[0:10]"],
        ["Matthias an der Heiden ❓", "RKI („Anderheiden“ im Transkript)", "E-Mails zu den Modellannahmen", "[0:11]"],
        ["Deborah Birx ❓", "Corona-Koordinatorin im Weißen Haus („Berks“)", "legte Präsident Trump ein Modell vor", "[0:09]"],
        ["Anders Tegnell", "schwedischer Staatsepidemiologe", "85.000 Tote angekündigt, laut Lausen 5.000", "[0:13]"],
        ["Olivier Véran, Roberto Speranza, Alain Berset, Jens Spahn, Rudolf Anschober", "Gesundheitsminister (F, I, CH, D, A)", "erwartete Todeszahlen aus ihren Büchern", "[0:13]"]),
    tab(["📖 Begriff", "Erklärung", "Fundstelle"],
        ["Enquete-Kommission", "Kommission des Bundestages aus Abgeordneten und Sachverständigen; hier: Aufarbeitung der Corona-Pandemie", "[0:00]"],
        ["ECDC", "EU-Behörde für Prävention und Kontrolle von Krankheiten", "[0:02]"],
        ["RKI-Krisenstabsprotokolle", "Sitzungsprotokolle des Covid-19-Krisenstabs im Robert Koch-Institut", "[0:06]"],
        ["Abbruchlogik", "sein Begriff: vorher festgelegter Punkt, an dem eine Maßnahme beendet wird", "[0:08]"],
        ["Worst Case / Best Case", "schlimmster bzw. günstigster Fall einer Modellrechnung", "[0:09]"],
        ["Kalibrieren", "Modellannahmen so einstellen, dass ein bestimmtes Ergebnis herauskommt", "[0:11]"],
        ["Letalität", "Anteil der Erkrankten, die sterben", "[0:12]"],
        ["„Panikpapier“", "sein Wort für das Szenarienpapier „Wie wir COVID-19 unter Kontrolle bekommen“", "[0:10]"]),
    tab(["📊 Zahl im Vortrag", "Angabe", "Fundstelle"],
        ["Krankenhausfälle weniger 2020", "2,5 Millionen", "[0:04]"],
        ["Rückgang der Mobilität vor dem Lockdown", "40 %", "[0:07]"],
        ["Handynutzer in den Telefónica-Daten", "40 Millionen", "[0:08]"],
        ["Best Case (E-Mail)", "126.000 Tote", "[0:10]"],
        ["Sterblichkeit der milden Fälle (E-Mail)", "0,02 %, später 0 %", "[0:11]"],
        ["Sterblichkeit je Infizierte", "etwa 1,2 %", "[0:11]"],
        ["Letalität der Intensivpflichtigen bei Überlastung (E-Mail)", "80 %", "[0:12]"],
        ["Worst Case", "über eine Million Tote", "[0:12]"],
        ["Erwartete Tote ohne Lockdown", "F 300.000–500.000 · S 85.000 · I 100.000 · CH 100.000 · D 400.000", "[0:13]"]),
)

v_abg = R(K + "abgleich", G + ": Abgleich & Daten",
    txt("Neutraler Abgleich: oben die Daten als Diagramme, darunter links die Aussage im Video und rechts die gängige Darstellung bzw. Daten mit Quelle. Die Bewertung bleibt dem Leser."),
    vgl, faelle, betten, ueber, abg,
    abs_("🧩 Offene Enden im Vortrag", [
        "Der Vortrag hat keinen Gesprächspartner; Gegenfragen kommen nicht vor.",
        "Für Schweden wird die Klinikbelegung genannt, aber keine Zahl.",
        "Die Protokoll- und E-Mail-Zitate werden vorgelesen, ohne Fundstelle im Dokument."]),
    abs_("❓ Offen", [
        "Veröffentlichungsdatum des Videos.",
        "Wortlaut der RKI-Protokolle vom 18. und 20. März 2020 und der E-Mails vom 20. März 2020 im Original.",
        "RKI-Modellierung vom 5. März 2020 und ihre Rolle bei den Schulschließungen.",
        "Die Prognosezahlen aus den Büchern der Gesundheitsminister.",
        "Klinikbelegung und Mobilität in Schweden 2020.",
        "Angaben zu gelöschten Tonaufnahmen in der Bundestagsverwaltung.",
        "Welche Meldungen über Lungenpest gemeint sind."]),
    abs_("🔎 Weiter recherchieren", [
        "RKI-Krisenstabsprotokolle im Original nachlesen (18. und 20. März 2020).",
        "Wortprotokolle der Enquete-Kommission auf bundestag.de, besonders die Sitzungen zu Schutzmaßnahmen.",
        "Das Buch selbst für die nicht öffentlichen Befragungen."]),
)

folgen = R("folgen", "Videos",
    txt("Alle ausgewerteten Videos mit Tom Lausen. Eine Karte antippen öffnet die Auswertung; oben in der Leiste lässt sich jedes Video auch direkt wählen. Weitere Transkripte kommen hier dazu."),
    {"typ": "folgenkarten"})

web = R("web", "Web",
    txt("Seiten und Videos. Stand: November 2026; YouTube-Titel sind die Originaltitel."),
    tab(["🌐 Seite", "Link"],
        ["Bundestag – Profil als Sachverständiger", L_BT],
        ["Enquete-Kommission – Konstituierung", L_TEXT],
        ["Interview Berliner Zeitung", L_BLZI]),
    tab(["🎬 Video", "Kanal", "Link"], [VT, "Westend Verlag", f"[ansehen]({URL})"]))

quellen = R("quellen", "Quellen",
    q([f"Video: {VT} | Tom Lausen – Westend Verlag (YouTube)", URL],
      *[[x[1:x.index("](")], x[x.index("](") + 2:-1]] for x in [L_BT, L_KONST, L_TEXT, L_ANH, L_PROT, L_AEBS, L_DEST20, L_DEST21, L_DEST25, L_AEZ, L_AEB, L_AEB24, L_BIFG, L_THIEME, L_MYDRG, L_ONKO, L_STAT, L_MOB, L_DESTMOB, L_SCHAADE, L_AEB16, L_ORF, L_MULTI, L_NPP, L_NPPC, L_BMI, L_DRS, L_HIB21, L_ADHOC, L_NOS, L_WHO, L_LIND, L_UDE, L_EBM, L_BLZ, L_BLZI, L_TE, L_FREI, L_NK, L_UNT]]),
    txt("Grundlage: Transkript des Videos (automatische Untertitel, abgerufen am 12.11.2026) sowie die verlinkten Seiten. Was nicht geprüft werden konnte, ist mit ❓ markiert."))


# ================= Video 2: MANOVA-Gespräch =================
URL2 = "https://www.youtube.com/watch?v=KYoXA1_1TBs"
VT2 = "Aufarbeitung der Aufarbeitung"
G2 = "Manova-Gespräch"; K2 = "manova"
L_HIB = "[Bundestag, hib 394/2025 – Besetzung der Enquete-Kommission](https://www.bundestag.de/presse/hib/kurzmeldungen-1107614)"
L_ANHS = "[Bundestag – Bericht zur Anhörung „Eindämmungsstrategien“ (7.5.2026)](https://www.bundestag.de/ausschuesse/weitere_gremien/ee01/anhoerungen/1170314-1170314)"
L_AEBV = "[Deutsches Ärzteblatt – Enquetekommission: Sachverständige verteidigen Coronamaßnahmen](https://www.aerzteblatt.de/news/enquetekommission-sachverstandige-verteidigen-coronamassnahmen)"
L_BLZS = "[Berliner Zeitung – RKI-Chef erinnert sich nicht an den 15.3.2020](https://www.berliner-zeitung.de/article/corona-enquete-rki-chef-erinnert-sich-nicht-an-lockdown-beratungen-10035055)"
L_BLZR = "[Berliner Zeitung – Bericht zur Risikohochstufung in der Enquete](https://www.berliner-zeitung.de/article/10307158)"
L_BMG = "[Bundesgesundheitsministerium, Schreiben vom 12.7.2024 zur Hochstufung (PDF)](https://multipolar-magazin.de/media/240712-hochstufung-dittmar.pdf)"
L_SCHST = "[Bundestag – ergänzende Stellungnahme Prof. Schaade, 26.5.2026 (PDF)](https://www.bundestag.de/resource/blob/1182320/21-27-38_ergaenzende-Stellungnahme-des-SV-Prof-Dr-Lars-Schaade.pdf)"
L_MP = "[Multipolar – „Die Menschen sollen Angst haben“ (PDF)](https://multipolar-magazin.de/media/pdf/die-menschen-sollen-angst-haben.pdf)"
L_SPV = "[Bundestag-Mediathek – Anhörung vom 15.12.2025](https://www.bundestag.de/mediathek/video?videoid=7646762)"
L_SPTE = "[Tichys Einblick – Bericht zu Spahns Aussage in der Enquete](https://www.tichyseinblick.de/video/interview/corona-debakel-in-deutschland-lug-und-trug/)"
L_SPZDF = "[ZDFheute – Spahn in der Enquete-Kommission (15.12.2025)](https://www.zdfheute.de/politik/deutschland/spahn-corona-masken-enquete-kommission-100.html)"
L_GFV = "[Gesellschaft für Virologie – Stellungnahme vom 18.12.2025 (PDF)](https://g-f-v.org/wp-content/uploads/2025/12/GfV-SN_Enquete-Kommission_Brandenburg_1218_final.pdf)"
L_RECHT = "[Bundestag – Wortprotokoll der 6. Sitzung, 3.11.2025: Rechtsstaat unter Pandemiebedingungen (PDF)](https://www.bundestag.de/resource/blob/1132350/2025-11-03_6-Sitzung-1-.pdf)"
L_HITZE = "[zm online – RKI-Bericht zur Hitzemortalität 2026](https://www.zm-online.de/news/detail/5100-menschen-starben-im-juni-in-deutschland-durch-die-hitze)"
L_HITZE2 = "[RKI – Wochenbericht Hitzemortalität, KW 36/2023 (PDF)](https://edoc.rki.de/bitstream/handle/176904/11304/RKI-Wochenbericht_Hitzemortalit%C3%A4t_KW36_2023-09-21.pdf)"
L_HITZE3 = "[Schwäbische Zeitung – RKI-Schätzungen 2018–2022](https://www.schwaebische.de/panorama/rki-schlagt-alarm-bereits-640-hitzetote-in-deutschland-in-diesem-jahr-1750762)"

TH2 = [{"k": "a", "n": "Kommission & Buch"}, {"k": "b", "n": "Regeln & Fragezeit"}, {"k": "c", "n": "Nicht öffentlich & Protokoll"}, {"k": "d", "n": "Daten & RKI"}, {"k": "e", "n": "Deutung & Stimmung"}, {"k": "f", "n": "Impfung, Papier & Medien"}]
AB2 = [
 ("🎬 Vorspann: die 15-jährige Schülerin", "0:00", "0:01", "e", [
   "Ausschnitt vom Ende des Gesprächs: Lausen schildert die Aussage einer 15-jährigen Schülerin in der Kommission. Sie sei als Ungeimpfte hinter Plastik und im Winter ans offene Fenster gesetzt worden. Von den anderen sei keine Reaktion gekommen.",
   "💬 „Wie die Steine. Nichts.“ (Lausen) [0:00]"]),
 ("👋 Vorstellung und die komischen Momente", "0:01", "0:04", "a", [
   "Walter van Rossum stellt Lausen als „Robin Hood der Daten“ vor; das Buch sei spannend und auf eine Weise komisch. Lausen nennt als komischen Moment eine Antwort von „Frau Büchs“ zum Fußballer Kimmich und den Streit um einen Aufkleber auf seinem Laptop: Er sollte ihn abnehmen, obwohl sein Name darauf stand; die Vorsitzende habe die Sitzung unterbrochen.",
   "❓ „Büchs“ im Transkript: gemeint ist vermutlich Alena Buyx, frühere Vorsitzende des Deutschen Ethikrats.",
   "📚 Vorsitzende der Kommission ist Franziska Hoppermann (CDU). " + L_HIB]),
 ("🏛️ Spielregeln: Enquete statt Untersuchungsausschuss", "0:04", "0:07", "a", [
   "Der Bundestag habe sich nicht auf einen Untersuchungsausschuss geeinigt, sondern auf eine Enquete-Kommission – das Wort bedeute Ermittlung. Der Einsetzungsantrag enthalte 43 Fragen zur Vergangenheit und 29 zur Zukunft. Die Fraktionen entsenden Abgeordnete nach Stärke und benennen ebenso viele sachverständige Mitglieder; er fragt im Zeitkontingent der AfD-Fraktion. Laufzeit: September 2025 bis Juli 2027.",
   "📌 Er unterscheidet: sachverständige Mitglieder (dauerhaft) und eingeladene Sachverständige (einmalig, themenbezogen). [0:06]",
   "📚 Besetzung laut Bundestag: CDU/CSU 5 Abgeordnete und 5 Sachverständige, AfD 3 und 3, SPD 3 und 3, Grüne 2 und 2, Linke 1 und 1. " + L_HIB]),
 ("⏱️ 24 Sitzungen und fünf Minuten", "0:07", "0:12", "b", [
   "Van Rossum hält 24 Sitzungen für wenig und vergleicht mit einem Gerichtsverfahren über Viehhaltung mit 40 Verhandlungstagen. Lausen: Ein Erkenntnisgewinn, der die staatlichen Maßnahmen als Ursache der Schäden zeige, sei nicht gewollt [seine Sicht]. Regel: fünf Minuten für Frage und Antwort zusammen, dann ein Gong. In Thüringen gebe es stattdessen eine Rednerliste; dort fragten fast nur die AfD-Seite und selten die Linke. Das Fünf-Minuten-Format sorge dafür, dass kritische Fragen nicht am Stück kommen [seine Sicht].",
   "💬 „Und dann darf man auch nicht weiter fragen, selbst wenn man mitten im Satz ist.“ (Lausen) [0:10]",
   "📌 Beispiel für seine Kritik an der Besetzung: Berlins früherer Regierender Bürgermeister Müller prüfe nun als Sachverständiger eigene Entscheidungen. [0:09]",
   "🔗 Bei [0:09] steht ein Spendenaufruf des Kanals."]),
 ("❓ Warum seine Fragen lang sind", "0:12", "0:15", "b", [
   "Van Rossum fragt, ob die langen Fragen Absicht sind. Lausen: Man wisse nicht, was kommt; die Befragten redeten sich teils um Kopf und Kragen. Er bringe Vorhalte in die Frage ein, weil ohne sie keine sinnvolle Antwort möglich sei; Stefan Homburg rate ihm zur Kürze. Drosten habe auf Vorhalt eingeräumt, dass Besuchsverbote Schäden verursachten.",
   "💬 „Ich bin aber nicht auf Empörung … oder auf Klickzahlen aus.“ (Lausen) [0:13]"]),
 ("🔒 Die nicht öffentlichen Gruppen", "0:15", "0:17", "c", [
   "Die 28 Mitglieder seien in fünf Gruppen aufgeteilt; seine heißt Datenwissenschaft und Kommunikation. Auch dort würden Fachleute befragt, meist per Videoschaltung, ohne Öffentlichkeit. Weil die Gruppen klein sind, könne man genauer nachfragen. Genau das hätten seine Frau und er im Buch aufgeschrieben.",
   "📌 Seine Wertung: Dort zeige sich, dass manche Befragte „keine Ahnung“ hätten [seine Sicht]. [0:16]"]),
 ("📈 Die Risikobewertung des RKI", "0:17", "0:18", "d", [
   "Ohne eine Risikobewertung „hoch“ wären Lockdown und Schulschließungen nicht möglich gewesen. Wie sie zustande kam, habe er zweimal nicht öffentlich mit RKI-Präsident Schaade besprochen. In der öffentlichen Sitzung habe dieser sich nicht erinnern können, wo er an dem Sonntag war, an dem entschieden wurde.",
   "💬 „Und dann platzte die Bombe.“ (Lausen) [0:17]",
   "📚 Laut Bundesgesundheitsministerium trafen RKI-Präsident und Vizepräsident die Entscheidung am Sonntag, 15. März 2020; verkündet wurde sie am 17. März. " + L_BMG]),
 ("🏥 Was Behördenleiter wissen", "0:18", "0:20", "d", [
   "Neu sei für ihn gewesen, dass hohe Beamte einfache, öffentlich zugängliche Statistiken nicht kennen. Die frühere ECDC-Direktorin habe auf seine Frage geantwortet, eine historische Unterbelegung der Kliniken sei nicht typisch für eine Pandemie – ohne den Schluss zu ziehen, dass dann etwas anders gelaufen sein könnte [seine Sicht].",
   "📌 Er hält das für gefährlich, wenn Behörden dann nur noch eingeübte Abläufe befolgen. [0:19]",
   "🔗 Zahlen zur Klinikbelegung: siehe Video „Fragen bleiben“, Reiter Abgleich & Daten."]),
 ("🗂️ Das Protokoll und die gelöschte Tonaufnahme", "0:20", "0:24", "c", [
   "Im Protokoll der nicht öffentlichen Sitzung sei die Antwort der ECDC-Direktorin falsch wiedergegeben worden. Er habe verlangt, die Tonaufnahme vorzuspielen; das sei abgelehnt worden. Später sei ein „nicht“ eingefügt worden, aber mit dem Zusatz „am Anfang einer Pandemie“, den sie nicht gesagt habe. Auf seinen erneuten Einspruch habe man ihm mitgeteilt, die Aufnahme sei bereits gelöscht. Er kündigt Dienst- und Fachaufsichtsbeschwerden an.",
   "📌 In seiner Gruppe sei er nicht zum Vorsitzenden gewählt worden; der Stellvertreter leite sie – er nennt ihn „Scheinvorsitzenden“. [0:21]",
   "❓ Vorgänge aus nicht öffentlichen Sitzungen; hier nicht prüfbar."]),
 ("⚖️ Warum die Kommission trotzdem zählt", "0:24", "0:26", "a", [
   "Van Rossum: Anders als ein Untersuchungsausschuss habe die Kommission keine strafrechtlichen Folgen. Lausen: Was dort öffentlich im Bundestag gesagt wird, habe Gewicht; für Beamte gelte die Wahrheitspflicht auch dort. Dass die Regierung nicht nachgehe, wenn die Entscheidung vom März 2020 nicht protokolliert und nicht erinnert wird, zeige ein Problem [seine Sicht].",
   "💬 „Die wichtigste Entscheidung seit 1945“ – ohne Protokolleintrag (Lausen) [0:25]"]),
 ("🎭 Zwei Arten von Aufklärung", "0:26", "0:31", "e", [
   "Van Rossum: Die einen wollten es beim nächsten Mal besser absichern, die anderen Bremsen einbauen und zuerst Daten sehen – „Pfütze oder Tsunami“. Lausen erklärt die Haltung der Mehrheit mit fehlender Empathie oder mit Schuld, die nicht ausgesprochen werden könne; „wir sind gut durchgekommen“ sei eine Fiktion [seine Sicht]. Er schildert noch einmal die Schülerin und die Vertreterin der Bundesschülerkonferenz, die Schulschließungen für wichtig hielt.",
   "💬 „Wir haben eine massive Theaterstück-Gestaltung gesehen.“ (Lausen) [0:28]"]),
 ("🌫️ Zeit schinden – und die Juristen", "0:31", "0:34", "b", [
   "Eingeladene Sachverständige redeten bei Unterbrechungen einfach weiter; er sieht darin ein Muster, um Fragezeit zu verbrauchen [seine Sicht]. Van Rossum fand die Juristen am selbstkritischsten: Die Runde aus Kanzlerin und Ministerpräsidenten habe keinen Verfassungsrang. Lausen stimmt zu, erwartet aber, dass im Abschlussbericht „nötig unter Unsicherheit“ stehen wird – deshalb das Buch vorher.",
   "🔗 Sitzung zum Rechtsstaat: " + L_RECHT]),
 ("😠 Die Stimmung im Saal", "0:34", "0:36", "e", [
   "Die Stimmung sei rau. Sachverständige Mitglieder sollten nicht an eine Parteilinie gebunden sein, hielten aber zusammen „wie ein Gummiring“; er vergleicht das mit der Lage vor dem Mauerfall 1989. Er nennt aggressive Äußerungen der Professoren Rosenbrock und Salzberger [seine Sicht].",
   "📌 Seine Forderung: sachlich und „von der Gesinnung frei“. [0:35]"]),
 ("💉 Spahn und der Fremdschutz", "0:36", "0:41", "f", [
   "Van Rossum nennt als verblüffendsten Moment Spahns Aussage, bei den Impfstoffen sei es nie um Fremd- oder Selbstschutz gegangen, höchstens um die Verhinderung schwerer Verläufe. Lausen: Das sei „wie ein gefundener Bernstein“. Er erzählt von einem Journalisten, der sich wegen des Fremdschutzes habe impfen lassen und trotzdem negativ über seinen Vortrag schrieb. Öffentlichkeit könnten nur die großen Sender herstellen; die müssten dann ihre eigene Berichterstattung aufarbeiten [seine Sicht]. Die Regeln für Geimpfte und Genesene hätten sich auf eine kleine Studie gestützt; das Paul-Ehrlich-Institut habe dem Ministerium intern geschrieben, die Sicherheit mit deutschen Daten nicht effizient beurteilen zu können.",
   "💬 „Aber deswegen habe ich mich doch impfen lassen.“ (der Journalist, laut Lausen) [0:37]",
   "❓ „Puhak-Studie“ im Transkript und das Schreiben des Paul-Ehrlich-Instituts: hier nicht geprüft.",
   "📚 Die Anhörung mit Jens Spahn war am 15. Dezember 2025. " + L_SPV]),
 ("📰 Das Papier des Innenministeriums und die Medien", "0:41", "0:45", "f", [
   "Van Rossum: Das Papier vom März 2020 zeige, dass die Pandemie auch organisiert worden sei; in der Kommission komme es nicht vor. Lausen: Papier und Impfung seien dort keine richtigen Themen. Im Buch werde mit einer „SMS um 22:15 Uhr“ gezeigt, wie lange vorher geplant worden sei [seine Sicht]. Van Rossum nennt die Medien die „maßlosesten Pandemietreiber“. Lausen kündigt Sitzungen zur Rolle der Medien (2. November) und zu Desinformation (17. Dezember) an.",
   "❓ „Herrn Holtmann 19. Januar 2019“ im Transkript: unklar, wer und welches Datum gemeint ist."]),
 ("📚 Aufarbeitung der Aufarbeitung", "0:45", "0:48", "a", [
   "Das Buch solle zeigen, wie die Aufarbeitung selbst abläuft, weil niemand drei Stunden Anhörung am Stück ansehe. Nicht behandelt würden Fragen aus dem Alltag: geänderte Arbeitsverträge, Zutritt nur für Geimpfte, Impfempfehlung und Masken für Kinder. Sein Ziel sei kein Durchbruch, sondern ein Protokoll für spätere Generationen – ein Gegengewicht zum offiziellen Bericht.",
   "💬 „Wahrheitsgetreu, detailgenau muss berichtet werden, was hier gelaufen ist.“ (Lausen) [0:47]"]),
 ("🏞️ Thüringen – und sein Fazit", "0:48", "0:51", "e", [
   "In Thüringen sei der Wille zur Aufarbeitung noch geringer, das Format mit Rednerliste aber besser. Sein Fazit: Die staatlichen Maßnahmen seien das größte Problem für Gesundheit und Überleben gewesen, nicht die Erkrankung [seine Sicht]. Als Vergleich nennt er die Hitzetoten: In Krankenhausdaten sehe er im Sommer viele Einweisungen aus Pflegeheimen wegen Flüssigkeitsmangel; das spreche für Lücken in der Versorgung [seine Sicht].",
   "📚 Das RKI schätzt hitzebedingte Sterbefälle statistisch aus Sterbe- und Temperaturdaten; meist wirken Hitze und Vorerkrankungen zusammen. " + L_HITZE]),
]
teile2 = [{"von": v, "bis": b, "t": t.split(" ", 1)[1], "th": th} for t, v, b, th, _ in AB2]
abschn2 = []
for t, v, b, th, l in AB2:
    a = abs_(f"{t} [{v}–{b}]", l); a["th"] = th; abschn2.append(a)

ZA2 = [
 ("15.3.2020", 2020, "RKI-Präsident und Vizepräsident entscheiden, die Risikobewertung auf „hoch“ zu setzen", "[0:17]", False),
 ("17.3.2020", 2020, "Die Hochstufung wird öffentlich verkündet", "", True),
 ("März 2020", 2020, "Papier des Innenministeriums, im Gespräch „geleakte Papiere“", "[0:41]", False),
 ("2021", 2021, "Regeln mit Zutritt nur für Geimpfte und Genesene (2G)", "[0:39]", False),
 ("10.7.2025", 2025, "Bundestag setzt die Enquete-Kommission ein", "", True),
 ("8.9.2025", 2025, "Konstituierung; Vorsitz Franziska Hoppermann", "[0:05]", False),
 ("3.11.2025", 2025, "Anhörung „Der Rechtsstaat unter Pandemiebedingungen“", "[0:32]", False),
 ("1.12.2025", 2025, "Anhörung u. a. mit Christian Drosten", "[0:13]", False),
 ("15.12.2025", 2025, "Anhörung mit Jens Spahn zu Beschaffung und Versorgung", "[0:36]", False),
 ("7.5.2026", 2026, "Anhörung zu Eindämmungsstrategien; Fragen an Schaade und Braun zum 15. März 2020", "[0:17]", False),
 ("Herbst 2026", 2026, "Anhörung zu Bildung und Jugend mit der 15-jährigen Schülerin („gestern“)", "[0:29]", False),
 ("Herbst 2026", 2026, "Mitteilung an Lausen, die Tonaufnahme sei gelöscht („letzte Woche“)", "[0:23]", False),
 ("2.11.2026", 2026, "Angekündigte Sitzung zur Rolle der Medien", "[0:44]", False),
 ("17.12.2026", 2026, "Angekündigte Sitzung zu Destabilisierung, Radikalisierung und Desinformation", "[0:44]", False),
 ("Juli 2027", 2027, "Geplantes Ende der Kommission", "[0:05]", False),
]
abg2 = tab(["Aussage im Gespräch", "Gängige Darstellung (Mainstream) / Daten 📚", "Quelle"],
 ["Besetzung: CDU etwa zehn, AfD sechs Personen; insgesamt 28 (14 Abgeordnete, 14 Sachverständige). [0:05]",
  "Der Bundestag nennt dieselben Größen: CDU/CSU 5+5, AfD 3+3, SPD 3+3, Grüne 2+2, Linke 1+1.", L_HIB],
 ["Ein Erkenntnisgewinn, der die Maßnahmen als Ursache der Schäden zeigt, ist nicht gewollt. [0:08]",
  "Der Bundestag beschreibt als Ziel, zu überlegen, wie man sich auf eine Pandemie besser vorbereiten und sie besser bewältigen kann. In der Anhörung vom Mai 2026 verteidigten mehrere Sachverständige die Maßnahmen; eine RKI-Analyse von 2023 sieht einen wesentlichen Beitrag zur Eindämmung.", L_ANHS + " · " + L_AEBV],
 ["Fünf Minuten für Frage und Antwort zusammen; 24 Sitzungen in zwei Jahren. [0:08]",
  "Die Fünf-Minuten-Regel wird auch in der Buchbesprechung der Berliner Zeitung beschrieben. Die öffentlichen Anhörungen dauern jeweils rund drei Stunden und stehen mit Wortprotokoll online.", L_BLZ + " · " + L_PROT],
 ["Michael Müller prüft als Sachverständiger eigene Entscheidungen. [0:09]",
  "Müller, früherer Regierender Bürgermeister von Berlin, wurde von der SPD-Fraktion als Sachverständiger benannt.", L_HIB],
 ["Ohne die Risikobewertung „hoch“ wären Lockdown und Schulschließungen nicht möglich gewesen; Schaade konnte sich nicht erinnern, wo er entschied. [0:17]",
  "Ärzteblatt und Berliner Zeitung berichten, dass sich Schaade und der frühere Kanzleramtschef Braun an ihren Aufenthaltsort am 15. März 2020 nicht erinnerten. Beide wiesen laut Bundestag einen Zusammenhang mit einer Absprache zum Herunterfahren des Landes zurück. Schaade begründet die Hochstufung mit der Dynamik der Fallzahlen (Verdopplung etwa alle drei Tage) und einer vorliegenden Modellierung.", L_AEBV + " · " + L_BLZS + " · " + L_ANHS + " · " + L_SCHST + " · " + L_BMG],
 ["Die frühere ECDC-Direktorin hielt eine historische Unterbelegung der Kliniken für nicht typisch für eine Pandemie. [0:19]",
  "❓ Nicht öffentliche Sitzung, hier nicht prüfbar. Zu den Klinikzahlen siehe Video „Fragen bleiben“: Destatis nennt als Gründe freigehaltene Betten und verschobene Behandlungen.", L_DEST20],
 ["Das Protokoll gab die Antwort falsch wieder; die Tonaufnahme wurde gelöscht. [0:20]",
  "❓ Hier nicht prüfbar; eine Stellungnahme der Bundestagsverwaltung liegt hier nicht vor.", "–"],
 ["Spahn sagte, bei der Impfung sei es nie um Fremdschutz gegangen, nur um schwere Verläufe. [0:36]",
  "Berichte über die Anhörung vom 15.12.2025 geben Spahn so wieder: Ziel sei immer der Schutz vor schweren Verläufen gewesen; Kritiker verweisen auf frühere Aussagen zu Ansteckung und Herdenimmunität. Die Anhörung steht in der Mediathek. Die Gesellschaft für Virologie weist die Aussage zurück, Impfungen böten grundsätzlich keinen Übertragungs- oder Fremdschutz.", L_SPV + " · " + L_SPTE + " · " + L_SPZDF + " · " + L_GFV],
 ["Die 2G-Regeln stützten sich auf eine kleine Studie; das Paul-Ehrlich-Institut konnte die Sicherheit mit deutschen Daten nicht effizient beurteilen. [0:39]",
  "❓ Hier nicht geprüft; keine Quelle gefunden.", "–"],
 ["Das Papier des Innenministeriums zeigt, dass die Pandemie „organisiert“ wurde. [0:41]",
  "Die Bundesregierung beschreibt das Szenarienpapier als Arbeit einer Wissenschaftlergruppe ohne Zielvorgaben des Ministeriums; es habe Szenarien und Vorschläge zur Kommunikation enthalten.", L_DRS + " · " + L_BMI],
 ["Die Medien waren die größten „Pandemietreiber“ und fehlen als Thema. [0:43]",
  "Lausen selbst nennt eine Sitzung zur Rolle der Medien am 2. November 2026. ❓ Tagesordnung hier nicht geprüft.", "–"],
 ["Die Runde aus Kanzlerin und Ministerpräsidenten hatte keinen Verfassungsrang; Juristen in der Kommission sahen Rechtsbrüche. [0:32]",
  "Die Kommission hat dazu am 3.11.2025 eine eigene Anhörung gehalten; das Wortprotokoll ist öffentlich. ❓ Die einzelnen Aussagen der Juristen sind hier nicht nachgelesen.", L_RECHT],
 ["Die staatlichen Maßnahmen waren das größte Problem, nicht die Erkrankung. [0:49]",
  "Die RKI-eigene Analyse von 2023 kommt zum Schluss, dass Maskenpflicht und Kontaktbeschränkungen wesentlich zur Bekämpfung beitrugen; die Folgen der Maßnahmen (Besuchsverbote, Schulen) sind selbst Thema der Kommission.", L_AEBV],
 ["Hitzetote gehen eher auf Versorgungslücken in Heimen zurück als auf das Klima. [0:49]",
  "Das RKI schätzt die hitzebedingten Sterbefälle aus Sterbe- und Temperaturdaten: 2018 rund 8.400, 2019 rund 6.900, 2022 bis 2025 je etwa 2.600 bis 4.900. Meist wirke Hitze zusammen mit Vorerkrankungen. ❓ Seine Auswertung der Einweisungen wegen Flüssigkeitsmangel ist hier nicht geprüft.", L_HITZE + " · " + L_HITZE2],
)
abg2["stapel"] = True
vgl2 = {"typ": "vergleich", "titel": "⚖️ Zahlen im Gespräch und Daten nebeneinander", "la": "Im Gespräch genannt", "lb": "Daten laut Quelle",
  "zeilen": [
    {"n": "Mitglieder der Kommission", "a": 28, "b": 28, "dez": 0, "f": "[0:09]", "q": L_HIB},
    {"n": "CDU/CSU: Abgeordnete und Sachverständige", "a": 10, "b": 10, "dez": 0, "f": "[0:05]", "q": L_HIB},
    {"n": "AfD: Abgeordnete und Sachverständige", "a": 6, "b": 6, "dez": 0, "f": "[0:05]", "q": L_HIB},
    {"n": "Fragezeit je Fragesteller (Minuten, Frage und Antwort)", "a": 5, "b": 5, "dez": 0, "f": "[0:08]", "q": L_BLZ}]}
sitze = {"typ": "balken", "titel": "📊 Wer in der Enquete-Kommission sitzt (Abgeordnete + Sachverständige)", "einheit": "", "dez": 0,
  "zeilen": [["CDU/CSU", 10], ["AfD", 6], ["SPD", 6], ["Grüne", 4], ["Linke", 2]],
  "quelle": L_HIB + ". Stand: September 2025.", "hinweis": "Bezug zum Gespräch [0:05]: Jede Fraktion benennt so viele Sachverständige, wie sie Abgeordnete entsendet."}
zeitb = {"typ": "balken", "titel": "📊 Rechenbeispiel: Zeit in der Kommission (nach den Angaben im Gespräch)", "einheit": "Std.", "dez": 0,
  "zeilen": [["24 Sitzungen zu je 3 Stunden", 72], ["Vergleich im Gespräch: 40 Verhandlungstage, hier mit je 6 Stunden gerechnet", 240]],
  "quelle": "Eigene Rechnung aus den Angaben im Gespräch (24 Sitzungen, 14–17 Uhr; 40 Verhandlungstage). Die 6 Stunden je Verhandlungstag sind eine Annahme zur Veranschaulichung.",
  "hinweis": "Bezug zum Gespräch [0:07]: van Rossums Vergleich mit einem Gerichtsverfahren."}
hitze = {"typ": "balken", "titel": "📊 Hitzebedingte Sterbefälle in Deutschland (RKI-Schätzung)", "einheit": "", "dez": 0,
  "zeilen": [["2018", 8400], ["2019", 6900], ["2020", 3700], ["2022", 4500], ["2023", 3200]],
  "quelle": L_HITZE + ", " + L_HITZE3 + ", " + L_HITZE2 + ". Stand: Juli 2026.",
  "hinweis": "Bezug zum Gespräch [0:49]. Für 2018 nannte das RKI früher rund 8.700; 2021 lag die Schätzung unter 2.000, 2024 und 2025 bei etwa 3.000."}

v2_ueber = R(K2, G2 + ": Überblick",
    {"typ": "folge", "k": K2, "titel": VT2 + " | Tom Lausen und Walter van Rossum im MANOVA-Gespräch", "gast": "Tom Lausen", "rolle": "im Gespräch mit Walter van Rossum", "kanal": "Manova",
     "art": "Gespräch", "karte": "Manova · Gespräch mit Walter van Rossum", "datum": "Herbst 2026 ❓", "dauer": "51 Min.", "url": URL2,
     "thema": "Wie die Enquete-Kommission des Bundestages arbeitet, was in den nicht öffentlichen Gruppen geschieht und warum Lausen das in einem Buch festhält.",
     "wege": [[K2 + "ab", "📖", "Gespräch im Detail", "Abschnitt für Abschnitt, mit Zitaten"], [K2 + "zeit", "📅", "Zeitachse & Verzeichnisse", "Ereignisse, Personen, Begriffe, Zahlen"], [K2 + "abgleich", "⚖️", "Abgleich & Daten", "Diagramme, Aussagen neben Daten, Quellen"]]},
    hin("Auswertung nach dem Transkript (automatische Untertitel): Gesagtes ohne Zeichen, Ergänzungen 📚, Unklares ❓. Fundstellen [Stunde:Minute] springen ins Video. Die Bewertung bleibt dem Leser."),
    abs_("⚡ In Kürze", [
        "Lausen erklärt die Spielregeln der Kommission: 28 Mitglieder, monatliche Sitzungen bis Juli 2027, fünf Minuten für Frage und Antwort.",
        "Er sieht darin ein Format, das zusammenhängende Kritik verhindert; in Thüringen gebe es eine Rednerliste.",
        "In nicht öffentlichen Kleingruppen könne er genauer nachfragen – daraus stammt der Kern des Buchs.",
        "Beispiel Risikobewertung: Der RKI-Präsident habe sich nicht erinnern können, wo die Hochstufung im März 2020 entschieden wurde.",
        "Beispiel Protokoll: Eine Antwort sei falsch wiedergegeben und die Tonaufnahme gelöscht worden.",
        "Als stärksten Fund nennt er Spahns Aussage, bei der Impfung sei es nie um Fremdschutz gegangen.",
        "Sein Ziel: ein genaues Gegenprotokoll für spätere Generationen, bevor der Abschlussbericht erscheint."]),
    abs_("🔦 Aus Lausens Sicht – der rote Faden", [
        "Er versteht sich als jemand, der die Ermittlung nachholt, die der Name „Enquete“ verspricht: nachfragen, festhalten, veröffentlichen.",
        "Sein Maßstab sind Daten, die jeder nachprüfen kann. Wer eine Behörde leitet und sie nicht kennt, hat nach seiner Überzeugung die Lage nicht verstanden.",
        "Er rechnet nicht mit einem Schuldeingeständnis. Ihm reicht, dass spätere Generationen nicht nur den offiziellen Bericht vorfinden.",
        "Die Gegenstimmen und die Daten dazu stehen im Reiter Abgleich & Daten."]),
    txt("🎯 **Kernaussagen** – die wichtigsten Thesen des Gesprächs:"),
    tab(["#", "Aussage", "Begründung im Gespräch", "Fundstelle", "Gewicht"],
        ["1", "Die Kommission ist so gebaut, dass wenig herauskommt.", "24 Sitzungen, fünf Minuten je Frage und Antwort", "[0:07]", "★★★"],
        ["2", "Die Mehrheit will kein Ergebnis, das die Maßnahmen als Ursache der Schäden zeigt.", "Fragen ohne Bezug, Zusammenhalt der Mehrheit", "[0:08]", "★★★"],
        ["3", "Die nicht öffentlichen Gruppen sind der eigentliche Erkenntnisort.", "kleine Runden, genaueres Nachfragen", "[0:15]", "★★"],
        ["4", "Die Hochstufung des Risikos im März 2020 ist nicht dokumentiert.", "Schaade erinnert sich nicht; kein Protokolleintrag", "[0:17]", "★★★"],
        ["5", "Behördenleiter kennen einfache Statistiken nicht.", "Antwort der früheren ECDC-Direktorin", "[0:18]", "★★"],
        ["6", "Protokolle werden verändert, Tonaufnahmen gelöscht.", "Vorgang um die Antwort der ECDC-Direktorin", "[0:20]", "★★★"],
        ["7", "Auch ohne Strafbarkeit zählt, was dort gesagt wird.", "Wahrheitspflicht der Beamten, Öffentlichkeit des Bundestages", "[0:24]", "★★"],
        ["8", "Spahns Aussage zum Fremdschutz ist der wichtigste Fund.", "widerspreche der Begründung für 2G", "[0:36]", "★★★"],
        ["9", "Die großen Medien berichten nicht darüber.", "müssten eigene Berichterstattung aufarbeiten", "[0:38]", "★★"],
        ["10", "Die staatlichen Maßnahmen waren das größte Problem, nicht die Erkrankung.", "Erfahrungen aus beiden Kommissionen", "[0:49]", "★★"]),
    {"typ": "baum", "titel": "🌳 Themenbaum des Gesprächs", "wurzel": VT2, "unter": "Tom Lausen · Walter van Rossum · Manova · 2026 · 51 Min.",
     "knoten": [
        {"t": "🏛️ Kommission & Buch", "k": [{"t": "Enquete statt Untersuchungsausschuss [0:04]"}, {"t": "43 und 29 Fragen [0:04]"}, {"t": "Warum sie trotzdem zählt [0:24]"}, {"t": "Gegenprotokoll [0:47]"}]},
        {"t": "⏱️ Regeln & Fragezeit", "k": [{"t": "24 Sitzungen [0:07]"}, {"t": "Fünf Minuten und Gong [0:10]"}, {"t": "Rednerliste in Thüringen [0:11]"}, {"t": "Zeit schinden [0:31]"}]},
        {"t": "🔒 Nicht öffentlich & Protokoll", "k": [{"t": "Fünf Gruppen [0:15]"}, {"t": "Protokoll geändert [0:20]"}, {"t": "Tonaufnahme gelöscht [0:23]"}]},
        {"t": "📈 Daten & RKI", "k": [{"t": "Risikobewertung „hoch“ [0:17]"}, {"t": "Schaade erinnert sich nicht [0:17]"}, {"t": "Klinikbelegung [0:19]"}]},
        {"t": "🎭 Deutung & Stimmung", "k": [{"t": "Die Schülerin [0:29]"}, {"t": "„Theaterstück“ [0:28]"}, {"t": "Raue Stimmung [0:34]"}, {"t": "Hitzetote als Vergleich [0:49]"}]},
        {"t": "💉 Impfung, Papier & Medien", "k": [{"t": "Spahn zum Fremdschutz [0:36]"}, {"t": "2G und Paul-Ehrlich-Institut [0:39]"}, {"t": "Papier des Innenministeriums [0:41]"}, {"t": "Rolle der Medien [0:43]"}]}]},
    tab(["🧭 Steckbrief", ""],
        ["Thema in einem Satz", "Innenansicht der Corona-Enquete-Kommission aus Sicht eines ihrer Sachverständigen."],
        ["Titel", VT2 + " | Tom Lausen und Walter van Rossum im MANOVA-Gespräch"],
        ["Format", "Zwiegespräch; Vorspann mit Ausschnitt, ein Spendenaufruf des Kanals bei [0:09]"],
        ["Sprecher", "Tom Lausen; Walter van Rossum (Fragen) – Mitautor von Lausens erstem Buch"],
        ["Dauer", "ca. 51 Minuten"],
        ["Datum", "Herbst 2026 ❓ (genaues Datum nicht ermittelt; im Gespräch steht die Sitzung vom 2. November noch bevor)"],
        ["Grundton", "einvernehmlich; der Fragende teilt Lausens Sicht, Gegenfragen sind selten"]),
)
v2_ueber["bloecke"][-1]["schmal"] = True
v2_ab = R(K2 + "ab", G2 + ": Gespräch im Detail",
    txt("17 Abschnitte in der Reihenfolge des Gesprächs. Lesehilfe: 💬 Zitat · 📌 Aussage · 🔗 Bezug · 📚 Ergänzung · ❓ unklar."),
    {"typ": "gespraech", "titel": "🧭 Gesprächsverlauf – wann worüber gesprochen wird", "dauer": "0:51", "themen": TH2, "teile": teile2},
    *abschn2)
v2_zeit = R(K2 + "zeit", G2 + ": Zeitachse & Verzeichnisse",
    {"typ": "zeitachse", "titel": "📅 Zeitachse – Ereignisse, die im Gespräch vorkommen",
     "eintraege": [dict({"z": z, "j": j, "t": t, "e": e}, **({"f": f} if f else {})) for z, j, t, f, e in ZA2]},
    tab(["👤 Person", "Wer / was", "Rolle im Gespräch", "Fundstelle"],
        ["Tom Lausen", "Sachverständiges Mitglied der Kommission", "Gesprächspartner", "[0:01]"],
        ["Walter van Rossum", "Journalist, Mitautor von „Die Intensiv-Mafia“", "stellt die Fragen", "[0:01]"],
        ["Ulrike Lausen", "Mitautorin", "hält sich laut van Rossum im Hintergrund", "[0:01]"],
        ["Franziska Hoppermann", "Vorsitzende der Kommission (CDU)", "Streit um den Aufkleber", "[0:03]"],
        ["Julia Klöckner", "Bundestagspräsidentin", "berief die Sachverständigen", "[0:06]"],
        ["Alena Buyx ❓", "frühere Vorsitzende des Ethikrats („Büchs“)", "Antwort zu Kimmich", "[0:02]"],
        ["Michael Müller", "früherer Regierender Bürgermeister, Sachverständiger", "Beispiel für die Besetzung", "[0:09]"],
        ["Stefan Homburg", "Sachverständiger", "rät zu kurzen Fragen", "[0:13]"],
        ["Christian Drosten", "Virologe", "räumte auf Vorhalt Schäden durch Besuchsverbote ein", "[0:14]"],
        ["Lars Schaade", "RKI-Präsident („Schade“)", "Risikobewertung, erinnert sich nicht", "[0:17]"],
        ["Dr. Andrea Ammon", "frühere ECDC-Direktorin („Amon“)", "Antwort zur Klinikbelegung, Protokoll", "[0:19]"],
        ["Rolf Rosenbrock, Bernd Salzberger", "Sachverständige", "laut Lausen aggressive Äußerungen", "[0:35]"],
        ["Jens Spahn", "früherer Gesundheitsminister", "Aussage zum Fremdschutz", "[0:36]"],
        ["Roger Bittel", "betreibt einen Videokanal", "verfolgt die Sitzungen live", "[0:44]"]),
    tab(["📖 Begriff", "Erklärung", "Fundstelle"],
        ["Enquete-Kommission", "Gremium aus Abgeordneten und Sachverständigen; Lausen übersetzt „Ermittlung“", "[0:04]"],
        ["Untersuchungsausschuss", "Gremium mit Zeugenpflicht und Vereidigung", "[0:24]"],
        ["Sachverständiges Mitglied", "dauerhaft berufen, im Unterschied zu einmalig eingeladenen Sachverständigen", "[0:06]"],
        ["Fragezeitkontingent", "Redezeit je Fraktion", "[0:06]"],
        ["Risikobewertung", "Einstufung des RKI: gering, mäßig, hoch, sehr hoch", "[0:17]"],
        ["Fremdschutz", "Schutz anderer durch die eigene Impfung", "[0:36]"],
        ["2G", "Zutritt nur für Geimpfte und Genesene", "[0:39]"],
        ["Volumenmangel", "Flüssigkeitsmangel, Diagnose in Krankenhausdaten", "[0:50]"]),
    tab(["📊 Zahl im Gespräch", "Angabe", "Fundstelle"],
        ["Fragen im Einsetzungsantrag", "43 zur Vergangenheit, 29 zur Zukunft", "[0:04]"],
        ["Mitglieder", "28 (14 Abgeordnete, 14 Sachverständige)", "[0:09]"],
        ["Laufzeit", "September 2025 bis Juli 2027, 24 Sitzungen", "[0:05]"],
        ["Sitzungsdauer", "3 Stunden (14–17 Uhr), sechs eingeladene Sachverständige", "[0:10]"],
        ["Fragezeit", "5 Minuten für Frage und Antwort", "[0:08]"],
        ["Arbeitsgruppen", "5, mit je 6 bis 7 Personen", "[0:15]"],
        ["Rundfunkbeitrag", "„1836 im Monat“ = 18,36 € 📚", "[0:38]"],
        ["Schüler in der Bundesschülerkonferenz", "8 Millionen", "[0:30]"]),
)
v2_abg = R(K2 + "abgleich", G2 + ": Abgleich & Daten",
    txt("Neutraler Abgleich: oben die Daten als Diagramme, darunter links die Aussage im Gespräch und rechts die gängige Darstellung bzw. Daten mit Quelle. Die Bewertung bleibt dem Leser."),
    vgl2, sitze, zeitb, hitze, abg2,
    abs_("🧩 Spannungen im Gespräch", [
        "Van Rossum nennt die Kommission „unverbindliches Palaver“; Lausen widerspricht und hält sie für wichtig. [0:24]",
        "Van Rossum fragt, ob die langen Fragen ungeschickt sind; Lausen verteidigt sie. [0:12]",
        "Lausen sagt, das Thema Medien komme nicht vor – und nennt gleich darauf die Sitzung dazu. [0:43]",
        "Sonst sind sich beide einig; eine Gegenposition aus der Kommission kommt nicht zu Wort."]),
    abs_("❓ Offen", [
        "Veröffentlichungsdatum des Gesprächs.",
        "Alle Vorgänge aus nicht öffentlichen Sitzungen (Protokoll, Tonaufnahme, Wahl des Gruppenvorsitzes).",
        "Schreiben des Paul-Ehrlich-Instituts und die genannte Studie zu 2G.",
        "Wer mit „Holtmann“ gemeint ist und welches Datum.",
        "Zeitungsbericht über den Aufkleber.",
        "Die Auswertung zu Einweisungen wegen Flüssigkeitsmangel."]),
    abs_("🔎 Weiter recherchieren", [
        "Mediathek des Bundestages: Anhörungen vom 15.12.2025 (Spahn) und 7.5.2026 (Schaade, Braun).",
        "Wortprotokoll vom 3.11.2025 zu den Aussagen der Juristen.",
        "Das Buch für die nicht öffentlichen Befragungen."]),
)

# ================= Reiter „Seine Sicht“ =================
sicht = R("sicht", "Seine Sicht",
    txt("Dieser Reiter gibt **Lausens Standpunkt in seiner eigenen Logik** wieder – so, wie er ihn in den ausgewerteten Videos begründet. Es ist seine Sicht, keine Feststellung des Kompendiums; was andere dazu sagen und was die Daten zeigen, steht bei jedem Video unter „Abgleich & Daten“."),
    abs_("🔦 Warum er das macht", [
        "Der Bundestag hat sich eine „Enquete“ gegeben – das heißt Ermittlung. Lausen nimmt das Wort ernst: ermitteln, was geschah, wer entschied und auf welcher Grundlage. [Manova 0:04]",
        "Nach seiner Überzeugung leistet die Kommission das nicht. Also macht er es selbst: Er fragt nach, hält die Antworten fest und veröffentlicht sie. [Fragen bleiben 0:14]",
        "Er versteht das als Arbeit, die dem Staat zugestanden hätte – eine Prüfung der eigenen Entscheidungen anhand der eigenen Akten und Zahlen."]),
    abs_("📊 Wie er vorgeht", [
        "Er beginnt bei Zahlen, die jeder nachschlagen kann: Krankenhausfälle, Belegung, Mobilität.",
        "Dann legt er die Akten daneben: Protokolle des RKI-Krisenstabs, E-Mails zum Szenarienpapier, Antworten in den Anhörungen.",
        "Wo Zahlen und Begründung nicht zusammenpassen, stellt er die Frage – in fünf Minuten, deshalb mit Vorhalt.",
        "Was nicht öffentlich gesagt wird, schreibt er auf, bevor es nur noch in einer Zusammenfassung steht."]),
    abs_("🧱 Seine stärksten Punkte", [
        "2020 gab es rund 2,5 Millionen Krankenhausfälle weniger als im Jahr davor. Die Zahl stimmt mit Destatis überein; für ihn passt sie nicht zu einer Pandemie, die das Gesundheitssystem überlastet.",
        "Die Mobilität war Mitte März 2020 schon um etwa 40 % gesunken, bevor die Kontaktbeschränkungen kamen. Auch diese Größe findet sich im Mobilitätsprojekt des RKI. Für ihn folgt daraus: Der Lockdown war nicht mehr nötig.",
        "Die Hochstufung des Risikos am 15. März 2020 trafen zwei Personen; wo, daran konnte sich der RKI-Präsident in der Anhörung nicht erinnern. Für ihn ist das der Kern: die folgenreichste Entscheidung ohne Aktenvermerk.",
        "Das Szenarienpapier des Innenministeriums rechnet mit über einer Million Toten im schlimmsten Fall. Für ihn zeigt der E-Mail-Verkehr, dass die Annahmen auf dieses Ergebnis hin eingestellt wurden.",
        "Spahn sagte in der Kommission, Ziel der Impfung sei immer der Schutz vor schweren Verläufen gewesen. Für ihn entfällt damit die Begründung für Regeln, die Ungeimpfte ausschlossen."]),
    abs_("🎯 Was er erreichen will", [
        "Kein Schuldeingeständnis – damit rechnet er nicht.",
        "Ein Gegenprotokoll: Wer in zwanzig Jahren nachliest, soll nicht nur den Abschlussbericht finden. [Manova 0:47]",
        "Eine „Abbruchlogik“ für künftige Lagen: vorher festlegen, bei welchen Daten eine Maßnahme endet. [Fragen bleiben 0:08]",
        "Dass zuerst gemessen wird, bevor gewarnt wird – „Pfütze oder Tsunami“, wie es im Manova-Gespräch heißt. [Manova 0:27]"]),
    abs_("↔️ Wo andere widersprechen", [
        "Destatis erklärt den Rückgang der Klinikfälle mit freigehaltenen Betten und verschobenen Behandlungen.",
        "Der RKI-Präsident begründet die Hochstufung mit der Verdopplung der Fallzahlen etwa alle drei Tage.",
        "Die Bundesregierung bestreitet Zielvorgaben an die Autoren des Szenarienpapiers.",
        "Eine RKI-Analyse von 2023 sieht einen wesentlichen Beitrag der Maßnahmen zur Eindämmung.",
        "Im Einzelnen mit Quellen: {{a:lausen-fragenabgleich|Abgleich zu „Fragen bleiben“}} und {{a:lausen-manovaabgleich|Abgleich zum Manova-Gespräch}}."]),
)

alle = [person, buecher, kern, sicht, folgen, v2_ueber, v2_ab, v2_zeit, v2_abg, v_ueber, v_ab, v_zeit, v_abg, web, quellen]
dia = sum(1 for r in [v_ueber, v_ab, v_zeit, v_abg] for b in r["bloecke"] if b["typ"] in ("kurs", "balken", "vergleich", "illu"))
v_ueber["bloecke"][0]["kacheln"] = [[str(len(AB)), "Abschnitte"], ["10", "Kernaussagen"], [str(len(abg["zeilen"])), "Abgleich-Punkte"], [str(len(ZA)), "Zeitachse"], [str(dia), "Skizzen & Diagramme"]]

dia2 = sum(1 for r in [v2_ueber, v2_ab, v2_zeit, v2_abg] for b in r["bloecke"] if b["typ"] in ("kurs", "balken", "vergleich", "illu"))
v2_ueber["bloecke"][0]["kacheln"] = [[str(len(AB2)), "Abschnitte"], ["10", "Kernaussagen"], [str(len(abg2["zeilen"])), "Abgleich-Punkte"], [str(len(ZA2)), "Zeitachse"], [str(dia2), "Diagramme"]]
web["bloecke"][-1]["zeilen"].append([VT2 + " | Tom Lausen und Walter van Rossum im MANOVA-Gespräch", "Manova", f"[ansehen]({URL2})"])
quellen["bloecke"][0]["eintraege"][1:1] = [[f"Video: {VT2} | Tom Lausen und Walter van Rossum im MANOVA-Gespräch – Manova (YouTube)", URL2]]
quellen["bloecke"][0]["eintraege"] += [[x[1:x.index("](")], x[x.index("](") + 2:-1]] for x in [L_HIB, L_ANHS, L_AEBV, L_BLZS, L_BLZR, L_BMG, L_SCHST, L_MP, L_SPV, L_SPTE, L_SPZDF, L_GFV, L_RECHT, L_HITZE, L_HITZE2, L_HITZE3]]
kern["bloecke"] += [abs_("6. Die Aufarbeitung selbst aufarbeiten", ["Wie eine Kommission fragt, protokolliert und zusammenfasst, entscheidet darüber, was später als Ergebnis gilt – deshalb beobachtet er auch das Verfahren [seine Sicht]. [0:45]"]),
                    abs_("7. Maßnahmen als eigene Schadensquelle", ["Die Folgen von Isolation, Besuchsverboten und Schulschließungen müssten ebenso gezählt werden wie die Erkrankung selbst [seine Sicht]. [0:49]"])]
kern["bloecke"][0]["text"] = "Seine Leitgedanken – als Wiedergabe seiner Sicht, aus den bisher ausgewerteten Videos. Wird mit jedem weiteren Transkript ergänzt."
autor = {"id": "lausen", "nr": "A-09", "name": "Tom Lausen", "botan": "Datenanalyst, Publizist, Sachverständiger im Bundestag", "volksnamen": [],
  "kurz": "Tom Lausen wertet amtliche Gesundheitsdaten aus und sitzt als Sachverständiger in der Enquete-Kommission des Bundestages zur Corona-Aufarbeitung. Hier gesammelt: seine Vorträge und Gespräche – je Video Überblick, Vortrag im Detail, Zeitachse und Abgleich mit Daten.",
  "steckbrief": [["Geboren", "1967 in Hamburg"], ["Beruf", "Programmierer, Datenanalyst, Publizist"], ["Amt", "Sachverständiges Mitglied der Enquete-Kommission „Corona“ des Bundestages (seit 2025) und des Thüringer Landtags"],
                 ["Bücher", "Die Intensiv-Mafia (2021), Die Untersuchung (2024), 5 Minuten gegen die Macht (2026)"], ["Kernthemen", "Krankenhaus- und Intensivdaten, Modellrechnungen, RKI-Protokolle, Aufarbeitung"],
                 ["Ausgewertete Videos", "2 (Stand 12.11.2026)"]],
  "reiter": alle}
json.dump(autor, open("/home/claude/scratch/lausen/lausen.json", "w"), ensure_ascii=False)
print("ok", len(AB), len(abg["zeilen"]), len(ZA), dia)
