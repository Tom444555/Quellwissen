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

alle = [person, buecher, kern, folgen, v_ueber, v_ab, v_zeit, v_abg, web, quellen]
dia = sum(1 for r in alle[4:8] for b in r["bloecke"] if b["typ"] in ("kurs", "balken", "vergleich", "illu"))
v_ueber["bloecke"][0]["kacheln"] = [[str(len(AB)), "Abschnitte"], ["10", "Kernaussagen"], [str(len(abg["zeilen"])), "Abgleich-Punkte"], [str(len(ZA)), "Zeitachse"], [str(dia), "Skizzen & Diagramme"]]

autor = {"id": "lausen", "nr": "A-09", "name": "Tom Lausen", "botan": "Datenanalyst, Publizist, Sachverständiger im Bundestag", "volksnamen": [],
  "kurz": "Tom Lausen wertet amtliche Gesundheitsdaten aus und sitzt als Sachverständiger in der Enquete-Kommission des Bundestages zur Corona-Aufarbeitung. Hier gesammelt: seine Vorträge und Gespräche – je Video Überblick, Vortrag im Detail, Zeitachse und Abgleich mit Daten.",
  "steckbrief": [["Geboren", "1967 in Hamburg"], ["Beruf", "Programmierer, Datenanalyst, Publizist"], ["Amt", "Sachverständiges Mitglied der Enquete-Kommission „Corona“ des Bundestages (seit 2025) und des Thüringer Landtags"],
                 ["Bücher", "Die Intensiv-Mafia (2021), Die Untersuchung (2024), 5 Minuten gegen die Macht (2026)"], ["Kernthemen", "Krankenhaus- und Intensivdaten, Modellrechnungen, RKI-Protokolle, Aufarbeitung"],
                 ["Ausgewertete Videos", "1 (Stand 12.11.2026)"]],
  "reiter": alle}
json.dump(autor, open("/home/claude/scratch/lausen/lausen.json", "w"), ensure_ascii=False)
print("ok", len(AB), len(abg["zeilen"]), len(ZA), dia)
