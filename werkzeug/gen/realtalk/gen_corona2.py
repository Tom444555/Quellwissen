# -*- coding: utf-8 -*-
# Erzeugt folge.json für „Corona 2.0: Dr. Nina & Heiko Schöning decken den Plan auf“
# (K = corona2, Sammelstelle A-12 realtalk). Gesundheitsthema: Die Nacherzählung (Überblick, Abschnitte,
# Zeitachse, linke Abgleich-Spalte) ist von Hand aus dem Transkript geschrieben; die belegte Seite
# (rechte Spalte, Diagramme, Prüfstand, Skizzen) kommt aus fakten.json / pruefstand.json des Helfers.
import json, os, re
O = os.path.dirname(os.path.abspath(__file__))
K = 'corona2'; G = 'Corona 2.0'
URL = 'https://www.youtube.com/watch?v=Pq-KGNIdZ4E'
TITEL = 'Corona 2.0: Dr. Nina & Heiko Schöning decken den Plan auf'
DAUER = '1 Std. 34 Min.'
FA = json.load(open(O + '/fakten.json')) if os.path.exists(O + '/fakten.json') else {}
V = FA.get('video', {})
DATUM = V.get('datum') or '2026 ❓'
FZ = {z['k']: z for z in FA.get('zeilen', [])}
for _b in FA.get('diagramme', []):
    if _b['typ'] == 'vergleich':
        for _z in _b['zeilen']:
            if _z['n'].startswith('Mikrobenarten'): _z['f'] = '[0:27]'
            if _z['n'].startswith('Mikrobengene'): _z['f'] = '[1:18]'
            if _z['n'].startswith('Träger'): _z['f'] = '[0:45]'
SCH1 = '{{a:realtalk-schoening|Schöning: Epstein und 9/11}}'
SCH1A = '{{a:realtalk-schoeningabgleich|Abgleich zum ersten Schöning-Gespräch}}'
LAU = '{{a:lausen|Tom Lausen (A-09)}}'
NEH = '{{a:nehls|Michael Nehls (A-01)}}'

def ab(titel, th, *liste):
    return {'typ': 'abschnitt', 'titel': titel, 'th': th, 'liste': list(liste)}

THEMEN = [
    {'k': 'a', 'n': 'Nachrichtenblock'},
    {'k': 'b', 'n': 'Ausbruch & Antibiotika'},
    {'k': 'c', 'n': 'Mikrobiom'},
    {'k': 'd', 'n': 'mRNA, Nano & Biowaffen'},
    {'k': 'e', 'n': 'Akteure: Wexner, Epstein'},
    {'k': 'f', 'n': 'Bundestag & Verfolgung'},
    {'k': 'g', 'n': 'Ernährung & Aufbau'},
    {'k': 'w', 'n': 'Werbung/Organisatorisches'},
]

AB = [
 ab('🎬 Vorspann: Sätze aus dem Gespräch und Ankündigung [0:00–0:03]', 'w',
    'Das Video beginnt mit kurzen Ausschnitten aus dem späteren Gespräch (Epstein und Wexner, Antibiotika-Abgabe, Nanotechnologie). Danach begrüßt der Gastgeber zur Sendung „Good Morning Germany“ und kündigt das Thema an: Heiko Schöning spreche von „Corona 2.0“.',
    '📌 Der Gastgeber begründet sein Interesse damit, dass Schöning die Corona-Pandemie in einem 2019 ausgestrahlten Interview angekündigt habe und „mit so ziemlich allem recht“ gehabt habe [seine Sicht] [0:01].',
    '📌 Er fragt, was ein „Angriff auf das Mikrobiom“ mit Coronaviren zu tun habe und ob wieder Lockdowns drohen [0:01–0:02].',
    '🔗 Verweis auf das erste Gespräch der beiden: ' + SCH1 + ' – dort wurde dieses zweite Gespräch über Schönings zweites Buch angekündigt [0:02].',
    '📌 Zweiter Gast ist eine Ärztin, die als „Dr. Nina“ vorgestellt wird [0:02–0:03].'),
 ab('📰 Nachrichten: Todesstrafen-Gesetz in Israel, Eichmann und Rafi Eitan [0:03–0:06]', 'a',
    'Vor dem Gespräch zeigt der Gastgeber einen Nachrichtenblock. Zuerst ein eingespielter Beitrag: Das israelische Parlament habe ein Gesetz beschlossen, nach dem Militärgerichte Palästinenser wegen terroristischer Morde zum Tode verurteilen können; israelische Staatsbürger fielen nicht darunter.',
    '📌 Im Beitrag: Schnellverfahren, einfache Mehrheit, keine Berufung; die einzige vollstreckte Hinrichtung in Israel sei die Adolf Eichmanns 1962 gewesen [0:03–0:04].',
    '📌 Der Gastgeber knüpft an: Rafi Eitan habe Eichmann gefasst, komme in Whitney Webbs Buch „Eine Nation unter Erpressung“ vor und habe der AfD Glückwünsche geschickt [0:04–0:05].',
    '📌 Er verliest einen Text, der das Gesetz als „Apartheid“ bezeichnet und mit „Free Palestine“ endet [seine Sicht] [0:05–0:06].'),
 ab('📰 Werbung, Ben Salomo, Reza Pahlavi und ein Video aus Israel [0:06–0:11]', 'a',
    'Nach einer kurzen Werbe-Einblendung für ein Probiotikum spottet der Gastgeber über eine Veranstaltung, auf der der Rapper Ben Salomo zusammen mit Reza Pahlavi aufgetreten sei.',
    '📌 Werbung im Video: Probiotikum eines Sportnahrungs-Herstellers [0:06].',
    '📌 Danach zeigt er ein Video von Israelis, die im eigenen Land für Palästinenser demonstrieren, und sagt, man dürfe nicht pauschal bewerten, wofür die israelische Flagge stehe [0:08–0:11].',
    '💬 „dass auf beiden Seiten des politischen Spektrums immer gute Leute“ existieren (Gastgeber) [0:10]'),
 ab('📰 Lindsey Graham: „flatten“ und Disneyland [0:11–0:15]', 'a',
    'Ein englischer Ausschnitt zeigt US-Senator Lindsey Graham, der den Krieg in Gaza mit der Zerstörung Berlins und den Atombomben auf Japan vergleicht. Der Gastgeber widerspricht der Begründung für die Atombomben und spottet über Grahams Auftreten.',
    '📌 Der Gastgeber: Japan habe militärisch schon kapituliert gehabt; beim Angriff auf Pearl Harbor habe man die eigenen Soldaten geopfert [seine Sicht] [0:12].',
    '📌 Eingespielter US-Kommentar über Graham in Disneyland; dazu abfällige Bemerkungen über sein Privatleben, die hier nicht wiedergegeben werden [0:13–0:15].'),
 ab('📰 Gebet im Weißen Haus, Reuters zu Iran und NATO, Libanon [0:15–0:20]', 'a',
    'Der Gastgeber zeigt ein Video eines Gebets im Weißen Haus und einer Predigerin und nennt das religiösen Fanatismus. Dann verliest er zwei Reuters-Meldungen.',
    '📌 Reuters, 1. April 2026: Trump sage, die USA könnten bald aus dem Iran-Krieg aussteigen, und drohe mit einem NATO-Austritt [0:17–0:18].',
    '📌 Reuters, 31. März 2026: Im Libanon seien mehr als eine Million Menschen durch israelische Angriffe vertrieben worden [0:18].',
    '📌 Der Gastgeber: Deutschland sei über Ramstein beteiligt und habe früher Giftgas geliefert, mit dem an der iranischen Grenze 100.000 Menschen getötet worden seien [seine Sicht] [0:19].'),
 ab('📰 Roboter-Video und Überleitung [0:20–0:22]', 'a',
    'Ein letzter Ausschnitt zeigt einen humanoiden Roboter. Dann leitet der Gastgeber zum Thema über: Schöning habe im Bundestag gesprochen, ein Zusammenschnitt gehe um.',
    '📌 Der Gastgeber nennt die Bezeichnung „Corona 2.0“ selbst „zugegebenermaßen provokativ“ [0:21].',
    '📌 Begrüßung der Gäste; beide sind zugeschaltet, die Ärztin wird hier mit vollem Namen genannt (im Untertitel unklar ❓) [0:21–0:22].'),
 ab('🦠 Schöning: der Ausbruch in England als „gefälschte Pandemie“ [0:22–0:25]', 'b',
    'Schöning sagt, seit Mitte März sei eine „gefälschte Pandemie“ im Anzug. In England habe die Presse nach zwei Todesfällen an Hirnhautentzündung (Meningitis) eine Massenhysterie erzeugt; erstmals habe man massenweise Gesunde antreten lassen, um ihnen Antibiotika zu geben [seine Sicht].',
    '💬 „Es handelt sich tatsächlich um eine gefälschte Pandemie“ (Schöning) [0:22]',
    '📌 In den ersten Tagen über 10.000 Dosen Antibiotika und dazu Impfungen; Menschen mit Masken in der Schlange [0:23–0:24].',
    '📌 Dieselbe Panik gebe es in Neuseeland und Frankreich; der Tagesspiegel habe „wie Covid 2.0“ geschrieben, auch die New York Times berichte [0:24].',
    '📌 Antibiotika schädigten die Darmflora – das habe er im Buchtitel „Angriff aufs Mikrobiom“ zusammengefasst [0:25].'),
 ab('🧫 Dr. Nina: Was das Mikrobiom ist [0:25–0:29]', 'c',
    'Die Ärztin erklärt das Mikrobiom für Laien: Mikroben im Darm, auf der Haut, in Nase und allen Körperöffnungen. Ohne sie könne der Mensch nicht leben. Vielfalt bedeute gute Abwehr; Antibiotika träfen neben den krankmachenden auch die nützlichen Bakterien.',
    '💬 „Wir sind eine große Wohngemeinschaft“ (Dr. Nina) [0:26]',
    '📌 Zahlen im Gespräch: rund 2 kg Darmbesiedlung, 19.000 menschliche Gene gegenüber 6–9 Millionen Genen der Mikroben; Jäger in Tansania 600–900 „Stämme“, Stadtmenschen etwa 300 [0:26–0:27].',
    '📌 Ein gestörtes Mikrobiom (Dysbiose) schwäche die Abwehr und führe zu Depression und Ängsten; so entstünden „ängstliche, gefügige Menschen“ [ihre Sicht] [0:28].',
    '📌 Der Gastgeber betont, sie verteufle die Schulmedizin nicht: Penicillin habe viele Leben gerettet, könne aber missbraucht werden [0:25–0:26].'),
 ab('❓ Wie groß ist die Gefahr? „Inszenierung“ und Plan in Phasen [0:29–0:34]', 'b',
    'Der Gastgeber fragt, ob wirklich ein globales Ausmaß drohe und ob Ärzte widersprechen. Schöning antwortet, medizinisch sei klar, dass man solche Mengen Antibiotika nicht an Gesunde gebe; daran und an der Berichterstattung sehe man die Inszenierung [seine Sicht].',
    '📌 Deutschland: etwa drei Fälle je Million Einwohner und Jahr, rund 300 Fälle jährlich – zwei Tote hätte man „jederzeit“ zum Anlass nehmen können [0:30–0:31].',
    '📌 Der englische Gesundheitsminister habe zwei Tage nach den Todesfällen im Parlament eine große Impfkampagne angekündigt [0:31].',
    '📌 Vorgeplant habe das ein „Verbrechersyndikat“ um Jeffrey Epstein und Leslie Wexner; im Wexner Medical Center in Columbus (Ohio) seien rund 2 Milliarden Dollar investiert worden [seine Sicht] [0:31–0:32].',
    '📌 Man sei in „Phase 1“. Durch Aufklärung könne man es „im Keim ersticken“ – wie bei den Affenpocken, deren Pandemie die WHO ausgerufen und dann „abgeblasen“ habe [seine Sicht] [0:32–0:33].',
    '❓ Auf die Frage nach ärztlichen Gegenstimmen nennt Schöning keine Namen oder Einwände.'),
 ab('💉 Gastgeber und Dr. Nina zur Meningokokken-Impfung [0:34–0:36]', 'b',
    'Der Gastgeber erzählt von einem Arztbesuch mit einem Kind aus der Verwandtschaft: Ein junger Arzt habe gesagt, die Impfung gegen Hirnhautentzündung sei für Europa wenig geeignet, weil die Haupterreger in tropischen Gebieten vorkämen.',
    '📌 Dr. Nina widerspricht teilweise: Sie kenne Meningitis-Fälle auch hier, etwa nach Zeckenstichen; die genauen Zahlen kenne sie nicht [0:35].',
    '💬 „mich betrügt man nur einmal und nicht zweimal“ (Dr. Nina zu Impfungen nach Corona) [0:35]',
    '📌 Sie fragt Schöning, ob gegen Bakterien nun mit mRNA geimpft werden solle [0:36].'),
 ab('🧬 mRNA gegen Bakterien? Resistenzen und „Stufe 1“ [0:36–0:38]', 'd',
    'Schöning sagt, mRNA-Präparate seien als „Bakterienimpfung“ vorbereitet. Er nennt sie „Genmanipulation“, weder Antibiotikum noch Impfung [seine Sicht]. In England und Frankreich seien bisher klassische Antibiotika ausgegeben worden.',
    '📌 Genannt werden Penicillin und ein zweites Mittel (im Untertitel unverständlich ❓) [0:37].',
    '📌 Sein erwarteter Ablauf: Massenabgabe züchte Resistenzen, dann heiße es „multiresistente Killerbakterien“, es folgten Lockdown und Quarantäne, danach biete die Industrie mRNA an [seine Sicht] [0:37–0:38].',
    '📌 Er kündigt an, er habe selbst eine Meningokokken-Erkrankung (Serogruppe B) gehabt [0:38].'),
 ab('🔬 Dr. Nina: Antibiotika, mRNA und Nanopartikel [0:38–0:43]', 'd',
    'Die Ärztin hält vorbeugende Antibiotika für fahrlässig, bei einer bakteriellen Infektion aber für sehr hilfreich. Dann erklärt sie ihre Sicht auf mRNA: Sie brauche eine Hülle aus Lipid-Nanopartikeln, und diese Partikel überwänden alle Schranken im Körper.',
    '💬 „prophylaktisch obsolet meiner Ansicht nach“ (Dr. Nina) [0:38]',
    '📌 Die Partikel brächten die mRNA „in den Zellkern“; sie gelangten binnen einer halben Minute bis ins Gehirn, die Blut-Hirn-Schranke halte sie nicht auf – das sei seit 30 Jahren bekannt [ihre Sicht] [0:39–0:41].',
    '📌 Persönlich: Vor 2010 sei sie an Krebs erkrankt und habe eine Behandlung mit Nanopartikeln nach Lektüre zur Giftigkeit abgelehnt [0:41].',
    '📌 Eine Impfung gegen Bakterien sei für sie biologisch nicht nachvollziehbar. Vom Mikrobiom werde man seit Langem getrennt: Pestizide, Leben in Städten, auch Chlordioxid („CDL“) auf Dauer [ihre Sicht] [0:42].',
    '📌 Sie habe sich vier Äcker angeschafft und baue ihr Gemüse selbst an; sie sagt selbst, bei Nanotechnologie sei sie keine Expertin [0:42–0:43].'),
 ab('🚣 Schönings eigene Meningitis mit 19 Jahren [0:43–0:48]', 'b',
    'Schöning schildert, er sei als 19-jähriger Leistungsruderer nach der Einberufung zur Bundeswehr an einer bakteriellen Hirnhautentzündung erkrankt und fast binnen 24 Stunden gestorben. Antibiotika hätten ihn gerettet; deshalb nehme er die Fälle in England ernst.',
    '💬 „nur Antibiotika haben mir das Leben gerettet, Penicillin“ (Schöning) [0:43]',
    '📌 Vorgeschichte: fünf Tage Schlafentzug und Stress, dann eine Regatta im Regen mit vier Rennen; rund 10 % der Europäer trügen die Bakterien ohnehin im Nasen-Rachen-Raum [0:45–0:46].',
    '📌 Nach den Siegen hätten alle aus demselben Pokal getrunken; niemand sonst sei erkrankt, niemand habe vorbeugend Antibiotika genommen [0:46–0:47].',
    '📌 Sein Schluss: Vorbeugung nur im Einzelfall, wenn ein Arzt es für eine geschwächte Kontaktperson entscheidet – nicht für alle Kontakte [seine Sicht] [0:47–0:48].'),
 ab('🧨 Gastgeber: aus kleinen Meldungen wird Großes [0:48–0:49]', 'b',
    'Der Gastgeber zieht einen Vergleich: Gemeldete Brandanschläge einer „neuen iranischen Terrororganisation“ auf Krankenwagen in Europa hält er für nicht belegt; so werde ein Feindbild vorbereitet, das später größer genutzt werden könne [seine Sicht].',
    '📌 Noch gebe es keine Lockdowns und keine großflächige Panik [0:48].'),
 ab('🏛️ Schöning im Bundestag: Einladung, Polizei, Vorhersage [0:49–0:54]', 'f',
    'Der Gastgeber fragt nach Schönings Auftritt im Bundestag, zu dem ein AfD-Abgeordneter eingeladen hatte, und nach dem Vorwurf der AfD-Nähe. Schöning sagt, er sei nie in einer Partei gewesen. Die Veranstaltung habe „Verfolgung von Regierungskritikern“ geheißen; es sei besonders um die inhaftierte Ärztin Bianca Witzschel gegangen.',
    '📌 Beim Einlass habe man ihn über eine halbe Stunde warten lassen; dann hätten vier bewaffnete Polizisten Haft oder die sofortige Zahlung von über 3.000 € verlangt – wegen einer Sache, von der er und sein Anwalt nichts gewusst hätten. Jemand habe das Geld ausgelegt [0:51–0:52].',
    '📌 In der Rede habe er an seine Ankündigung von 2019 erinnert, die Freilassung inhaftierter Ärzte gefordert und vor „Corona 2.0“ gewarnt [0:52–0:53].',
    '🔗 Der Gastgeber nennt als frühere Redner bei solchen Veranstaltungen ' + LAU + ' und ' + NEH + ' [0:49–0:50].',
    '📌 Der Gastgeber gibt die Kritik wieder, eine Oppositionspartei schmücke sich mit glaubwürdigen Fachleuten und handle in Regierungsverantwortung dann doch anders – beweisen lasse sich das nicht [0:54].'),
 ab('🗳️ Dr. Nina lehnte eine Einladung ab; Krankenhaus in Bürgerhand [0:54–0:57]', 'f',
    'Dr. Nina berichtet, auch sie sei von der AfD eingeladen worden, über ihre Vorschläge zum Gesundheitswesen zu sprechen, und habe abgelehnt. Sie habe die Partei früher kurze Zeit gut gefunden, als diese gegen die EU war (ob als Mitglied, bleibt im Untertitel unklar ❓), und wolle nie wieder in die Parteipolitik.',
    '📌 Ihr Grund: Oppositionelle würden eingefangen, etikettiert und seien dann „weg“ [ihre Sicht] [0:55–0:56].',
    '💬 „selber machen, nicht machen lassen“ (Dr. Nina) [0:56]',
    '📌 Ihre Idee: ein Krankenhaus für einen Landkreis über Schwarmfinanzierung – 60 Millionen Euro, rund 40.000 Menschen mit je 1.500 € [0:56].'),
 ab('🌱 Dr. Nina: Trennung vom Mikrobiom seit Jahrzehnten [0:57–0:59]', 'c',
    'Für die Ärztin ist der „Angriff auf das Mikrobiom“ eine lange Geschichte: Leben in Städten, wenig Muttermilch, viele Kaiserschnitte. Die Mikroben seien eine Milliarden Jahre alte Intelligenz – die „Software“ zur „Hardware“ Körper.',
    '📌 Heute würden „fast alle Geburten“ per Kaiserschnitt gemacht; sie selbst habe keine Muttermilch bekommen [0:57].',
    '📌 Ohne diese „Software“ werde der Mensch leichter steuerbar; das gehe in Richtung Transhumanismus [ihre Sicht] [0:57–0:58].',
    '📌 Antibiotika seien bei einer Meningitis mit Symptomen und Laborwerten „sensationell gut“, vorbeugend in Massen aber „unmedizinisch“ [0:58].'),
 ab('🚓 Schöning: Bremen 2020, Staatsschutz und das Buch [0:59–1:03]', 'f',
    'Schöning nennt Parteipolitik eine Ablenkung und schildert ein Beispiel für Verfolgung: Am 5. Dezember 2020 sei er in Bremen vor einer Demonstration mit rund 50 anderen eingekesselt worden. Als ein Mann kollabierte, habe er einen Krankenwagen gerufen und sei wegen angeblichen Notruf-Missbrauchs in Gewahrsam gekommen.',
    '📌 Verhört habe ihn der Staatsschutz; am 6. Dezember sei er entlassen worden. Sein Schluss: Man habe ihn am Sprechen hindern wollen [seine Sicht] [1:00–1:01].',
    '📌 Sein Interview mit der Vorhersage liege seinem Buch „Game Over“ als DVD bei, weil es immer wieder gelöscht worden sei [1:01].',
    '📌 Er bittet, die englische Ausgabe „Attack on the Microbiome“ an Bekannte in England und Neuseeland zu schicken; man werde es später wieder versuchen, „im Windschatten“ des Iran-Kriegs [seine Sicht] [1:02–1:03].'),
 ab('☣️ Dr. Nina: Biowaffen, Nanotechnologie und „NWO“ [1:03–1:06]', 'd',
    'Die Ärztin verweist auf ein Video („2022 bis 2030“) und auf den Friedensforscher Jürgen Altmann: Nanotechnologische Biowaffen seien billig und überall herstellbar; daraus werde die Forderung nach einem Gewaltmonopol der UN abgeleitet. Sie deutet das als Druckmittel hin zu einer Weltordnung [ihre Sicht].',
    '📌 Mit Corona habe ein „Zeitalter“ solcher Bedrohungen begonnen [ihre Sicht] [1:04].',
    '📌 Ärzte sollten mit „gesundem Menschenverstand“ durch solche Lagen führen. Beispiel: Ein sehr ansteckender und sehr tödlicher Erreger wie Ebola könne keine große Pandemie auslösen, weil die Wirte nicht überleben [1:05].',
    '📌 Lob für Schönings Buch; das Mikrobiom sei „etwas Heiliges“ [1:05–1:06].'),
 ab('🐭 Keimfreie Mäuse, Toxoplasmose, raus aus der Stadt [1:06–1:07]', 'c',
    'Dr. Nina nennt Tierversuche: Steril aufgezogene Mäuse verhielten sich orientierungslos, überängstlich oder ganz ohne Angst; nach Besiedlung mit Mikroben werde ihr Verhalten normal. Toxoplasmose lasse eine Maus der Katze entgegenlaufen.',
    '📌 Sie hält Erreger für geeignet, Menschen in Panik zu versetzen, und vermutet Forschung dazu [ihre Sicht] [1:07].',
    '📌 Ihr Rat: raus aus den Städten, sich um das eigene Essen kümmern [1:07].'),
 ab('🏥 Wer sind die Akteure? Wexner Medical Center, Epstein, Whitney Webb [1:07–1:13]', 'e',
    'Der Gastgeber fragt nach den heutigen Hauptakteuren. Schöning nennt als wichtigste Einrichtung das Wexner Medical Center in Columbus (Ohio) und als Hauptkomplizen Epsteins Leslie Wexner. Dort werde die Erzählung zu Antibiotika weitergeführt; eine dort tätige Fachfrau, die er namentlich nennt, habe Verbindungen zu Geheimdiensten [seine Sicht].',
    '📌 „Epstein-Klasse“, Geheimdienste und organisiertes Verbrechen seien „mehr oder weniger eins“; das sei in seinem Buch mit Hunderten Quellen belegt [seine Sicht] [1:09–1:10].',
    '📌 Wexner sei vor einigen Monaten zu Hause und mit Anwalt befragt worden, statt vor dem Parlament zu erscheinen – für Schöning ein Zeichen, dass Milliardäre geschützt werden [seine Sicht] [1:10].',
    '📌 Er empfiehlt Whitney Webbs „Eine Nation unter Erpressung“ statt der „3 Millionen“ veröffentlichten Seiten; Erpressung und Korruption erklärten auch deutsche Politik, etwa Dieselpreise von 2,40 € [seine Sicht] [1:10–1:12].',
    '📌 Im Bundestag habe er erstmals den Namen einer Deutschen genannt, die mit Epstein in dessen Flugzeug geflogen sei; im Gespräch fällt der Name nicht [1:12–1:13].',
    '🔗 Mehr zu Schönings Sicht auf Epstein: ' + SCH1 + '.'),
 ab('🌐 „Nicht nur der Westen“: Biowaffen weltweit, Genesis 2.0, Iran [1:13–1:16]', 'd',
    'Dr. Nina erweitert Schönings Bild: Nach dem, was sie gelesen habe, flössen weltweit hohe Summen in militärische Nanotechnologie und Biowaffen – USA, Russland, China, Indien. Schöning stimmt zu: Das Corona-Geschehen hätten auch China, Russland und der Iran mitgetragen.',
    '💬 „da sehe ich jetzt keinen, der führend ist“ (Dr. Nina) [1:13]',
    '📌 Sie verweist auf den Film „Genesis 2.0“ und das Zitat eines Klon-Forschers, Gottes Werk müsse vervollkommnet werden; das sei Transhumanismus [1:14].',
    '📌 Schöning: Der Iran sei nach China und Italien das dritte Land mit harten Corona-Maßnahmen gewesen; auch der Ayatollah habe sich impfen lassen [1:15].',
    '📌 Er verweist auf seinen Vortrag „Das Zeitalter der Biowaffen hat begonnen“ [1:14–1:15].'),
 ab('🎓 Gastgeber: Vertrauen, Universitäten und Antibiotika bei Husten [1:16–1:18]', 'c',
    'Der Gastgeber sieht weltweit sinkendes Vertrauen in Institutionen und hält Universitäten für eine Wurzel des Problems. Er erzählt, vor etwa 15 Jahren habe ein Arzt in der Türkei einem zwei- bis dreijährigen Kind wegen Husten Antibiotika verschrieben.',
    '📌 Sein Schluss: Der „Angriff auf das Mikrobiom“ finde in vielen Ländern seit Jahrzehnten statt [seine Sicht] [1:17].'),
 ab('👶 Schöning: „unsere Helfer“, Militärpapier, Geburt und Muttermilch [1:18–1:19]', 'c',
    'Schöning nennt die Mikroben Freunde und Helfer mit „150-mal mehr“ Genen als der Mensch. Die britische Armee und die Bundeswehr hätten ein öffentlich auffindbares Papier herausgegeben, in dem das Mikrobiom als Waffe vorkomme.',
    '📌 Babys bekämen die guten Bakterien bei der natürlichen Geburt und über die Muttermilch; am Kaiserschnitt verdienten Kliniken mehr [seine Sicht] [1:18–1:19].',
    '📌 Sein Rat: bunt und vielfältig essen [1:19].'),
 ab('🥬 Was hilft dem Mikrobiom? Dr. Nina: Natur statt Präparate [1:19–1:23]', 'g',
    'Der Gastgeber fragt nach wirksamen Maßnahmen für Stadtmenschen. Dr. Nina erwähnt zuerst eine Mikrobiom-Bank in der Schweiz und deutet sie als Zeichen, dass natürliche durch künstliche Intelligenz ersetzt werden solle [ihre Sicht]. Dann ihre Ratschläge.',
    '📌 Das Mikrobiom baue man am besten in der Kindheit auf: draußen spielen, natürliche Geburt [1:21].',
    '📌 Fermentiertes und Kefir, Apfelpektin und Ballaststoffe; von Bakterien-Präparaten erwartet sie wenig, weil sich die Vielfalt nicht züchten lasse [1:22].',
    '📌 Sie habe sich in der Corona-Zeit bewusst nicht abgeschirmt; manche reisten für eine Stuhlübertragung nach Tansania [1:21–1:22].',
    '💬 „Man kann ein bisschen was machen in der Stadt, aber so viel ist es nicht“ (Dr. Nina) [1:22]'),
 ab('🇵🇪 „Kinder im Dreck“? Lima und ein OP in Südamerika [1:23–1:26]', 'g',
    'Der Gastgeber hakt nach: Meine sie damit auch Kleinkinder, die auf dem Boden eines Einkaufszentrums krabbeln? Dr. Nina antwortet mit Erlebnissen aus Peru und Brasilien: Straßenkinder auf Müllbergen bei Lima seien nicht krank gewesen; ein Chirurg habe den Schweiß ins Operationsfeld tropfen lassen.',
    '📌 Sie räumt ein, dass es viele Gifte gebe, sagt aber, die Angst vor Mikroben sei hierzulande zu groß [ihre Sicht] [1:24–1:25].',
    '📌 Vorsicht sei bei „Industrieprodukten“ nötig, „sei es Impfung oder Antibiotika“ [ihre Sicht] [1:25].',
    '📌 Bei Implantaten aus Metall gelte das Beispiel aus dem OP nicht [1:24, 1:25].'),
 ab('🍲 Schöning: Gemüsesuppe, Sauerkraut, Joghurt – und Kritik an „Vowst“ [1:26–1:29]', 'g',
    'Schöning sagt, nach einer Antibiotika-Kur dauere der Wiederaufbau des Mikrobioms laut einer Studie aus Schweden Jahre. Er empfiehlt gekochte Gemüsesuppe mit vielen bunten Zutaten, Sauerkraut, Kimchi, Kefir und Naturjoghurt statt teurer Produkte.',
    '📌 Ein in den USA eingeführtes Präparat („Vowst“, er verbindet es mit Nestlé) habe mehr Nebenwirkungen und ergebe für ihn kaum Sinn [seine Sicht] [1:27–1:28].',
    '📌 Therapeuten und Betroffenen rät er, über eine Stuhltransplantation von Gesunden nachzudenken [seine Sicht] [1:28].',
    '📌 Er wiederholt: „Kriminelle Vereinigungen“ wollten das Mikrobiom monopolisieren [seine Sicht] [1:29].'),
 ab('💪 Dr. Nina: keine Angst – „wir sind stark“ [1:29–1:31]', 'g',
    'Dr. Nina setzt einen anderen Ton als Schöning: Wer Antibiotika genommen habe, habe sein Mikrobiom nicht für Jahrzehnte zerstört; es baue sich wieder auf. Auch die innere Haltung spiele eine Rolle.',
    '💬 „wir sind stark und nicht schwach“ (Dr. Nina) [1:29]',
    '📌 Sie verweist auf ihre Sprechstunde für „Vitalmedizin“ in München, eine eigene Aufbaukur und ein noch unveröffentlichtes Buch [1:29–1:30].',
    '📌 Der Gastgeber nennt die Links zu Schönings Buch und zum neuen Kanal der Ärztin [1:30–1:31].'),
 ab('📣 Abspann: Mitgliedschaft und Benzinpreis [1:31–1:33]', 'w',
    'Der Gastgeber sagt, schlechte Nachrichten könnten Bewusstsein schaffen und dadurch befreiend wirken. Er wirbt für die Patreon-Mitgliedschaft (4,99 € im Monat) und bittet um Abos und Kommentare.',
    '📌 Zum Schluss die Frage, warum Diesel in Deutschland 2,50 € koste und anderswo weniger [1:32–1:33].'),
]

def span(t):
    m = re.search(r'\[(\d+:\d\d)[–-](\d+:\d\d)\]\s*$', t); return m[1], m[2]
TEILE = []
for b in AB:
    v, bi = span(b['titel'])
    kurz = re.sub(r'\s*\[\d+:\d\d[–-]\d+:\d\d\]\s*$', '', b['titel']); kurz = re.sub(r'^\S+\s', '', kurz)
    TEILE.append({'von': v, 'bis': bi, 't': kurz, 'th': b['th']})

# ---------- Abgleich: links Gespräch (von Hand), rechts Fachstellen (Helfer) ----------
ABG = [
 ('ausbruch_uk', 'Schöning: In England seien wegen zwei Todesfällen in den ersten Tagen über 10.000 Dosen Antibiotika und dazu Impfungen an Gesunde gegeben worden; der Gesundheitsminister habe zwei Tage später im Parlament eine große Impfkampagne angekündigt. Für ihn ist das eine Inszenierung [seine Sicht] [0:23–0:25, 0:31].'),
 ('ausbruch_andere', 'Schöning: Dieselbe Panik gebe es zeitgleich in Neuseeland und Frankreich; der Tagesspiegel habe „wie Covid 2.0“ geschrieben, auch die New York Times berichte [0:24–0:25].'),
 ('prophylaxe', 'Schöning: Antibiotika vorbeugend an Massen von Gesunden zu geben sei medizinisch falsch; richtig sei es nur im Einzelfall für geschwächte Kontaktpersonen. Dr. Nina: „prophylaktisch obsolet“ [0:29, 0:38, 0:44, 0:47].'),
 ('mening_de', 'Schöning: In Deutschland gebe es rund 300 Fälle im Jahr, etwa drei je Million Einwohner; rund 10 % der Europäer trügen die Bakterien im Nasen-Rachen-Raum, ohne krank zu sein [0:30, 0:45].'),
 ('menb_impfung', 'Gastgeber: Ein Arzt habe ihm gesagt, die Impfung gegen Hirnhautentzündung ziele auf Erreger, die vor allem in tropischen Regionen vorkommen, und sei für Europa wenig geeignet [0:34–0:35].'),
 ('mrna_bakterien', 'Schöning: mRNA-Präparate seien als „Bakterienimpfung“ vorbereitet; bisher seien in England und Frankreich klassische Antibiotika gegeben worden [0:36–0:38].'),
 ('mrna_einordnung', 'Schöning nennt mRNA-Impfstoffe „Genmanipulation“, weder Antibiotikum noch Impfung [seine Sicht] [0:37]. Dr. Nina: Lipid-Nanopartikel brächten die mRNA „in den Zellkern“, gelangten binnen einer halben Minute ins Gehirn und überwänden jede Schranke; ein rotes Blutkörperchen messe 4 µ, ein Nanopartikel 1 µ [ihre Sicht] [0:39–0:41].'),
 ('resistenz', 'Schöning: Die Massenabgabe züchte Resistenzen; dann werde vor „multiresistenten Killerbakterien“ gewarnt, es folgten Lockdown und Quarantäne und danach mRNA als Rettung [seine Sicht] [0:37–0:38].'),
 ('mikrobiom_zahlen', 'Dr. Nina: rund 2 kg Mikroben im Darm; 19.000 menschliche Gene gegenüber 6–9 Millionen Genen der Mikroben; der Mensch sei zu 99,999 % „Wohngemeinschaft“; Jäger in Tansania hätten 600–900 „Stämme“, Stadtmenschen etwa 300 [0:26–0:27]. Schöning: „150-mal mehr“ Gene [1:18].'),
 ('mikrobiom_psyche', 'Dr. Nina: Ein gestörtes Mikrobiom mache ängstlich und depressiv; steril aufgezogene Mäuse verhielten sich orientierungslos; Toxoplasmose lasse die Maus zur Katze laufen und mache beim Menschen Depressionen [ihre Sicht] [0:28, 1:06–1:07].'),
 ('antibiotika_erholung', 'Schöning: Laut einer Studie aus Schweden dauere der Wiederaufbau nach Antibiotika Jahre, etwa 60 Stämme fehlten sehr lange [1:26]. Dr. Nina: Der Körper baue das Mikrobiom wieder auf; niemand habe es für Jahrzehnte zerstört [1:29].'),
 ('geburt_stillen', 'Dr. Nina und Schöning: Natürliche Geburt und Muttermilch gäben dem Kind die guten Bakterien mit; heute würden „fast alle Geburten“ per Kaiserschnitt gemacht [0:57, 1:18–1:19].'),
 ('fmt_vowst', 'Schöning: Therapeuten sollten über eine Stuhltransplantation von Gesunden nachdenken; das Präparat „Vowst“ (er verbindet es mit Nestlé) habe mehr Nebenwirkungen und ergebe kaum Sinn [seine Sicht] [1:27–1:28].'),
 ('ernaehrung', 'Beide Gäste: bunt und vielfältig essen, Fermentiertes (Sauerkraut, Kimchi, Kefir), Naturjoghurt, Ballaststoffe; von Präparaten halten sie wenig [1:19–1:28].'),
 ('cdl', 'Dr. Nina: Chlordioxid („CDL“) könne „akut mal gut sein“, auf Dauer würde sie es nie nehmen – niemand könne belegen, dass es nur schädliche Bakterien trifft [ihre Sicht] [0:42].'),
 ('hygiene_kinder', 'Dr. Nina: Kinder im Dreck spielen lassen; Straßenkinder auf Müllbergen in Lima seien nicht krank gewesen; die Angst vor Mikroben sei zu groß [ihre Sicht] [1:21–1:25].'),
 ('vorhersage2019', 'Gastgeber und Schöning: Schöning habe die Corona-Pandemie in einem Interview vorhergesagt, das 2018 aufgezeichnet und im Dezember 2019 ausgestrahlt worden sei [0:01, 0:52].'),
 ('bundestag', 'Schöning: Er habe im Bundestag bei einer Veranstaltung „Verfolgung von Regierungskritikern“ gesprochen, auf Einladung eines Abgeordneten; Thema sei die inhaftierte Ärztin Bianca Witzschel gewesen. Vor dem Einlass hätten vier Polizisten Haft oder über 3.000 € verlangt [0:50–0:53].'),
 ('bremen2020', 'Schöning: Am 5.12.2020 sei er in Bremen eingekesselt, wegen eines Notrufs für einen Kollabierten in Gewahrsam genommen, vom Staatsschutz verhört und am 6.12. entlassen worden [0:59–1:01].'),
 ('wexner', 'Schöning: Epstein und sein „Hauptkomplize“ Leslie Wexner hätten die Sache vorgeplant; am Wexner Medical Center in Columbus (Ohio) seien rund 2 Mrd. $ investiert worden; Wexner sei nur zu Hause befragt worden [seine Sicht] [0:31–0:32, 1:08–1:10].'),
 ('whitney_webb', 'Schöning empfiehlt Whitney Webbs „Eine Nation unter Erpressung“ (in seinem Verlag erschienen). Gastgeber: Rafi Eitan, der Eichmann fasste, komme darin vor und habe der AfD Glückwünsche geschickt [0:04–0:05, 1:11].'),
 ('epstein_akten', 'Schöning: Die „3 Millionen“ veröffentlichten Seiten seien eine Ablenkung; besser 500 Seiten Webb lesen [seine Sicht] [1:12].'),
 ('mpox', 'Schöning: Die WHO habe eine Affenpocken-Pandemie ausgerufen; weil die Menschen nicht mitmachten, sei sie „abgeblasen“ worden [seine Sicht] [0:33].'),
 ('ebola', 'Dr. Nina: Ein Erreger, der so ansteckend und tödlich sei wie Ebola, könne keine große Pandemie auslösen, weil die Wirte nicht überleben [1:05].'),
 ('iran_corona', 'Schöning: Der Iran sei nach China und Italien das dritte Land gewesen, das Corona „total durchgezogen“ habe; auch der Ayatollah habe sich impfen lassen [1:15].'),
 ('biowaffen', 'Dr. Nina: Der Friedensforscher Jürgen Altmann erkläre in einem NATO-Bericht, nanotechnologische Biowaffen seien billig und überall herstellbar, und folgere ein Gewaltmonopol der UN [ihre Sicht] [1:03–1:04]. Schöning: Britische Armee und Bundeswehr hätten ein Papier veröffentlicht, das Mikrobiom als Waffe einzusetzen [1:18].'),
 ('mikrobiom_bank', 'Dr. Nina: In der Schweiz würden alle Mikroben der Welt eingefroren; sie deutet das als Vorbereitung auf deren Verlust [ihre Sicht] [1:20].'),
 ('genesis2', 'Dr. Nina: Der Arte-Film „Genesis 2.0“ (2019) zeige die größte Klonfabrik in China; ein Professor sage dort, Gottes Werk müsse vervollkommnet werden [1:14].'),
 ('nachrichtenblock', 'Nachrichtenblock des Gastgebers: Todesstrafen-Gesetz in Israel nur für Palästinenser; Eichmann 1962 als einzige Hinrichtung; Reuters 1.4.2026 zu Trump, Iran und NATO; über eine Million Vertriebene im Libanon; 100.000 Giftgas-Tote an der iranischen Grenze mit Gas aus Deutschland; Diesel 2,40–2,50 € [0:03–0:19, 1:11, 1:32].'),
 ('krankenhaus', 'Dr. Nina: Ein Krankenhaus koste 60 Mio. €; rund 40.000 Menschen mit je 1.500 € könnten es gemeinsam kaufen [0:56].'),
]
ZUSATZ = {
 'vorhersage2019': ' Ausführlich mit Quellen: ' + SCH1A + '.',
 'mrna_einordnung': ' Bei Fragen zur eigenen Gesundheit: Ärztin oder Arzt; Verdachtsfälle von Nebenwirkungen lassen sich unter [nebenwirkungen.bund.de](https://nebenwirkungen.bund.de) melden.',
}
abg_zeilen = []
for k, aussage in ABG:
    z = FZ.get(k)
    if z: abg_zeilen.append([aussage, z['fakt'] + ZUSATZ.get(k, ''), z.get('quelle') or '❓'])
    else: abg_zeilen.append([aussage, '❓ Dazu liegt hier keine geprüfte Quelle vor.' + ZUSATZ.get(k, ''), '❓'])

# ---------- Zeitachse ----------
ZA = [
 {'z': 'vor Milliarden Jahren', 't': 'Mikroben besiedeln die Erde – für Dr. Nina eine uralte „Intelligenz“, auf die der Körper zurückgreift.', 'f': '[0:57]', 'e': False},
 {'z': '1962', 'j': 1962, 't': 'Hinrichtung Adolf Eichmanns in Israel – im Nachrichtenblock als einzige vollstreckte Todesstrafe genannt.', 'f': '[0:04]', 'e': False},
 {'z': '1970er/80er', 'j': 1975, 't': 'Laut Dr. Nina beginnt die Entfernung von der Natur: weniger Muttermilch, mehr Kaiserschnitte, Leben in Städten.', 'f': '[0:57]', 'e': False},
 {'z': 'mit 19 Jahren', 't': 'Schöning erkrankt nach der Einberufung zur Bundeswehr und einer Ruderregatta an Meningokokken-Meningitis; Penicillin rettet ihn.', 'f': '[0:43–0:47]', 'e': False},
 {'z': '2001', 'j': 2001, 't': '11. September – der Gastgeber erinnert an Schönings Verbindung von Anschlägen, Biowaffen und Pandemie.', 'f': '[1:07]', 'e': False},
 {'z': 'vor 2010', 'j': 2009, 't': 'Dr. Nina erkrankt an Krebs und lehnt eine Behandlung mit Nanopartikeln ab.', 'f': '[0:41]', 'e': False},
 {'z': 'um 2011', 'j': 2011, 't': 'Gastgeber erlebt in der Türkei, dass ein Kleinkind wegen Husten Antibiotika bekommt.', 'f': '[1:16]', 'e': False},
 {'z': '2018', 'j': 2018, 't': 'Aufzeichnung von Schönings Interview mit der Ankündigung einer Pandemie (laut Gastgeber).', 'f': '[0:01]', 'e': False},
 {'z': '2019', 'j': 2019, 't': 'Film „Genesis 2.0“ läuft laut Dr. Nina bei Arte.', 'f': '[1:14]', 'e': False},
 {'z': 'Dez. 2019', 'j': 2019, 't': 'Ausstrahlung von Schönings Interview.', 'f': '[0:52]', 'e': False},
 {'z': '2020', 'j': 2020, 't': 'Corona-Pandemie; laut Schöning zieht der Iran als drittes Land nach China und Italien harte Maßnahmen durch.', 'f': '[1:15]', 'e': False},
 {'z': '05.–06.12.2020', 'j': 2020, 't': 'Bremen: Schöning wird nach eigener Schilderung vor einer Demonstration eingekesselt, in Gewahrsam genommen und am Folgetag entlassen.', 'f': '[0:59–1:00]', 'e': False},
 {'z': 'nach 2020', 'j': 2022, 't': 'Laut Schöning ruft die WHO eine Affenpocken-Pandemie aus und beendet sie wieder.', 'f': '[0:33]', 'e': False},
 {'z': 'Anfang 2026', 'j': 2026, 't': 'Befragung Leslie Wexners zu Epstein „vor ein paar Monaten“ (Schöning).', 'f': '[1:10]', 'e': False},
 {'z': 'Mitte März 2026', 'j': 2026, 't': 'Meningitis-Ausbruch in England; Antibiotika und Impfungen für viele Menschen – für Schöning der Beginn von „Corona 2.0“.', 'f': '[0:23]', 'e': False},
 {'z': 'Ende März 2026', 'j': 2026, 't': 'Schöning spricht bei einer Veranstaltung im Bundestag („letzte Woche“).', 'f': '[0:33, 0:50]', 'e': False},
 {'z': '31.03.2026', 'j': 2026, 't': 'Reuters: über eine Million Vertriebene im Libanon (vom Gastgeber verlesen).', 'f': '[0:18]', 'e': False},
 {'z': '01.04.2026', 'j': 2026, 't': 'Reuters: Trump zu Ausstieg aus dem Iran-Krieg und NATO (vom Gastgeber verlesen); Aufnahme des Gesprächs kurz danach.', 'f': '[0:17]', 'e': False},
 {'z': '2022–2030', 'j': 2030, 't': 'Zeitraum im Titel eines Videos, auf das Dr. Nina verweist: Sie erwartet weitere ausgerufene Bedrohungen.', 'f': '[1:03]', 'e': False},
]
for e in FA.get('zeitachse', []):
    e = dict(e); e['e'] = True; e.setdefault('f', ''); ZA.append(e)
ZA.sort(key=lambda e: (e.get('j', -10**9)))

PERS = [
 ['Heiko Schöning', 'Arzt, Autor („Game Over“, „Angriff aufs Mikrobiom“), Verleger', 'Gast; spricht von „Corona 2.0“', '[0:22]'],
 ['„Dr. Nina“', 'Ärztin aus München, Sprechstunde „Vitalmedizin“; Nachname im Untertitel unklar ❓', 'Gast; erklärt Mikrobiom und Nanopartikel', '[0:25]'],
 ['Gastgeber', 'Moderator von REALTALK MEDIA („Good Morning Germany“); Name nicht belegt ❓', 'führt durch Nachrichtenblock und Gespräch', '[0:00]'],
 ['Leslie Wexner', 'US-Unternehmer, Namensgeber des Wexner Medical Center', 'laut Schöning „Hauptkomplize“ Epsteins [seine Sicht]', '[0:31, 1:08]'],
 ['Jeffrey Epstein', 'US-Finanzier, 2019 gestorben', 'laut Schöning Teil eines „Syndikats“ [seine Sicht]', '[0:31]'],
 ['Whitney Webb', 'US-Journalistin, Autorin von „One Nation Under Blackmail“', 'von Schöning empfohlen', '[0:04, 1:11]'],
 ['Rafi Eitan', 'israelischer Geheimdienstmann (1926–2019)', 'vom Gastgeber mit Eichmann-Festnahme und AfD-Gruß genannt', '[0:04–0:05]'],
 ['Bianca Witzschel', 'Ärztin; laut Schöning wegen Masken-Attesten in Haft', 'Anlass der Bundestags-Veranstaltung', '[0:51]'],
 ['Tom Lausen, Michael Nehls', 'frühere Redner bei ähnlichen Veranstaltungen', 'vom Gastgeber genannt', '[0:49–0:50]'],
 ['Jürgen Altmann', 'Physiker und Friedensforscher (im Untertitel „Jörg“)', 'von Dr. Nina zu Nanotechnologie zitiert', '[1:03]'],
 ['Bill Gates', 'Unternehmer und Stifter', 'habe vor Corona oft vor Ebola gewarnt (Dr. Nina)', '[1:05]'],
 ['Lindsey Graham', 'US-Senator', 'im Nachrichtenblock mit „flatten“-Aussagen', '[0:11–0:15]'],
 ['Itamar Ben-Gvir', 'israelischer Minister für nationale Sicherheit', 'im eingespielten Beitrag zum Todesstrafen-Gesetz', '[0:03]'],
 ['Ben Salomo, Reza Pahlavi', 'Rapper; Sohn des letzten Schahs', 'Ziel des Spotts im Nachrichtenblock', '[0:06–0:08]'],
 ['Donald Rumsfeld, Jerome Hauer', 'frühere US-Amtsträger', 'vom Gastgeber als Stichworte zu 9/11 genannt', '[1:07]'],
]
ORTE = [
 ['England', 'Ausbruch von Meningokokken-Meningitis im März 2026', '[0:23]'],
 ['Neuseeland, Frankreich', 'laut Schöning gleiche Meldungen zur gleichen Zeit', '[0:24]'],
 ['Columbus (Ohio)', 'Sitz des Wexner Medical Center', '[0:31, 1:08]'],
 ['Berlin, Bundestag', 'Veranstaltung „Verfolgung von Regierungskritikern“', '[0:50–0:53]'],
 ['Bremen', 'Demonstration am 5.12.2020, Gewahrsam', '[0:59–1:00]'],
 ['Tansania', 'Jäger und Sammler mit sehr vielfältigem Mikrobiom', '[0:27, 1:22]'],
 ['Lima (Peru), Brasilien', 'Dr. Ninas Arbeit als Ärztin; Müllberge, OP-Erlebnis', '[1:23–1:25]'],
 ['Türkei', 'Antibiotika bei Husten (Erlebnis des Gastgebers)', '[1:16]'],
 ['Schweiz', 'Mikrobiom-Bank', '[1:20]'],
 ['München', 'Praxis von Dr. Nina', '[1:30]'],
 ['Israel, Westjordanland, Libanon, Iran', 'Nachrichtenblock', '[0:03–0:19]'],
]
BEGR = [
 ['Mikrobiom', 'Gesamtheit der Mikroben, die auf und im Menschen leben, vor allem im Darm', '[0:25]'],
 ['Dysbiose', 'gestörtes Gleichgewicht des Mikrobioms', '[0:28]'],
 ['Meningitis / Meningokokken', 'Hirnhautentzündung; Meningokokken sind Bakterien, die sie auslösen können', '[0:24, 0:30]'],
 ['Prophylaxe', 'vorbeugende Gabe, hier von Antibiotika an Menschen ohne Krankheitszeichen', '[0:23, 0:38]'],
 ['Resistenz', 'Bakterien sprechen auf ein Antibiotikum nicht mehr an', '[0:37]'],
 ['mRNA', 'Boten-RNA; Bauplan, den Zellen ablesen', '[0:36–0:39]'],
 ['Lipid-Nanopartikel', 'winzige Fetthülle, in der mRNA verpackt wird', '[0:39]'],
 ['Blut-Hirn-Schranke', 'Barriere zwischen Blut und Gehirn', '[0:40]'],
 ['CDL', 'Chlordioxid-Lösung', '[0:42]'],
 ['Stuhltransplantation', 'Übertragung von Darmbakterien eines Gesunden', '[1:22, 1:28]'],
 ['Fermentieren', 'Haltbarmachen durch Mikroben, z. B. Sauerkraut, Kimchi, Kefir', '[1:19–1:26]'],
 ['Transhumanismus', 'Bestreben, den Menschen technisch zu verändern', '[0:58, 1:14]'],
 ['Staatsschutz', 'Abteilung der Polizei für politisch motivierte Straftaten', '[1:00]'],
 ['„Mega Group“', 'von Schöning genannter Kreis um Wexner [seine Sicht]', '[1:10]'],
 ['NWO', '„Neue Weltordnung“ – von Dr. Nina benutzter Begriff', '[1:04]'],
]
ZAHL = [
 ['Antibiotika-Dosen in England in den ersten Tagen', 'über 10.000', '[0:23]'],
 ['Todesfälle als Auslöser', '2', '[0:23]'],
 ['Meningokokken-Fälle in Deutschland', 'rund 300 im Jahr, etwa 3 je Million', '[0:30]'],
 ['Träger der Bakterien in Europa', 'rund 10 %', '[0:45]'],
 ['Masse der Darmbesiedlung', 'etwa 2 kg', '[0:26, 1:18]'],
 ['Gene: Mensch gegenüber Mikroben', '19.000 gegenüber 6–9 Millionen; „150-mal mehr“', '[0:26, 1:18]'],
 ['Bakterien-„Stämme“: Jäger in Tansania gegenüber Städtern', '600–900 gegenüber etwa 300', '[0:27]'],
 ['Investition am Wexner Medical Center', 'rund 2 Mrd. US-$', '[0:31]'],
 ['Verlangte Zahlung vor dem Bundestag', 'über 3.000 €', '[0:52]'],
 ['Krankenhaus in Bürgerhand', '60 Mio. €; je 1.500 € von rund 40.000 Menschen', '[0:56]'],
 ['Fehlende Stämme nach Antibiotika', '60, über Jahre', '[1:26]'],
 ['Vertriebene im Libanon (Reuters)', 'über 1 Million', '[0:18]'],
 ['Dieselpreis', '2,40–2,50 € je Liter', '[1:11, 1:32]'],
 ['Patreon-Mitgliedschaft', '4,99 € im Monat', '[1:32]'],
]

KERN = [
 ['1', 'In England läuft seit Mitte März 2026 eine „gefälschte Pandemie“.', 'Nach zwei Todesfällen seien über 10.000 Dosen Antibiotika an Gesunde gegeben worden; Presse und Minister hätten Panik erzeugt.', '[0:22–0:25]', '★★★'],
 ['2', 'Antibiotika vorbeugend in Massen sind medizinisch falsch.', 'Vorbeugung nur im Einzelfall; Schönings eigene Erkrankung: niemand im Ruderboot bekam Antibiotika, niemand erkrankte.', '[0:29, 0:43–0:48]', '★★★'],
 ['3', 'Das Mikrobiom ist lebenswichtig, und Antibiotika treffen auch die nützlichen Bakterien.', 'Vielfalt gleich Abwehr; Dysbiose schwäche Immunsystem und Psyche.', '[0:25–0:29]', '★★★'],
 ['4', 'Hinter dem Geschehen steht ein Plan in Phasen.', 'Schöning nennt Epstein, Wexner und das Wexner Medical Center und verweist auf sein Buch.', '[0:31–0:33, 1:08–1:10]', '★★★'],
 ['5', 'Auf Resistenzen folgen Lockdowns und mRNA „gegen Bakterien“.', 'So beschreibt Schöning die nächsten Stufen; bisher seien klassische Antibiotika gegeben worden.', '[0:36–0:38]', '★★'],
 ['6', 'mRNA-Präparate und Nanopartikel sind riskant.', 'Dr. Nina: Die Partikel überwänden jede Schranke bis ins Gehirn; sie sagt selbst, sie sei keine Expertin.', '[0:39–0:43]', '★★'],
 ['7', 'Aufklärung kann die Sache „im Keim ersticken“.', 'Beispiel Affenpocken; Buch und Bundestagsrede sollen verbreitet werden.', '[0:33, 1:02]', '★★'],
 ['8', 'Regierungskritiker werden verfolgt.', 'Schöning schildert die Szene vor dem Bundestag und den Gewahrsam in Bremen 2020; Parteipolitik sei Ablenkung.', '[0:50–0:53, 0:59–1:01]', '★★'],
 ['9', 'Es hat ein Zeitalter der Biowaffen und Nanotechnologie begonnen – weltweit.', 'Dr. Nina sieht keinen führenden Staat; Schöning stimmt zu und nennt China, Russland, Iran.', '[1:03–1:05, 1:13–1:15]', '★★'],
 ['10', 'Das Mikrobiom stärkt man mit Natur, Vielfalt und Fermentiertem – nicht mit Angst.', 'Gemüsesuppe, Sauerkraut, Kefir, Joghurt; Dr. Nina: Der Körper baut es wieder auf.', '[1:19–1:30]', '★★★'],
]

BAUM = {'typ': 'baum', 'titel': '🌳 Themenbaum des Gesprächs', 'wurzel': TITEL,
 'unter': 'Heiko Schöning und Dr. Nina · REALTALK MEDIA · %s · %s' % (DATUM, DAUER),
 'knoten': [
  {'t': '📰 Nachrichtenblock', 'k': [{'t': 'Todesstrafen-Gesetz in Israel [0:03]'}, {'t': 'Lindsey Graham [0:11]'}, {'t': 'Reuters: Iran, NATO, Libanon [0:17]'}, {'t': 'Roboter [0:20]'}]},
  {'t': '🦠 Ausbruch & Antibiotika', 'k': [{'t': 'England: über 10.000 Dosen [0:23]'}, {'t': 'Neuseeland, Frankreich, Presse [0:24]'}, {'t': 'Fallzahlen Deutschland [0:30]'}, {'t': 'Schönings eigene Meningitis [0:43]'}, {'t': 'Vorbeugung nur im Einzelfall [0:47]'}]},
  {'t': '🧫 Mikrobiom', 'k': [{'t': '„Wohngemeinschaft“ [0:26]'}, {'t': 'Vielfalt und Abwehr [0:27]'}, {'t': 'Psyche und Ängste [0:28]'}, {'t': 'Geburt, Muttermilch, Stadt [0:57]'}, {'t': 'Keimfreie Mäuse [1:06]'}]},
  {'t': '🧬 mRNA, Nano & Biowaffen', 'k': [{'t': 'mRNA „gegen Bakterien“ [0:36]'}, {'t': 'Resistenzen, „Stufe 1“ [0:37]'}, {'t': 'Nanopartikel und Schranken [0:39]'}, {'t': 'Altmann, „NWO“ [1:03]'}, {'t': 'Weltweit, Genesis 2.0 [1:13]'}]},
  {'t': '🏥 Akteure laut Schöning', 'k': [{'t': 'Epstein und Wexner [0:31]'}, {'t': 'Wexner Medical Center [1:08]'}, {'t': 'Whitney Webb [1:11]'}, {'t': 'Erpressung und Korruption [1:11]'}]},
  {'t': '🏛️ Bundestag & Verfolgung', 'k': [{'t': 'Einladung, AfD-Frage [0:49]'}, {'t': 'Polizei vor dem Einlass [0:51]'}, {'t': 'Dr. Nina lehnt ab [0:55]'}, {'t': 'Bremen 2020, Staatsschutz [0:59]'}]},
  {'t': '🥬 Ernährung & Aufbau', 'k': [{'t': 'Kindheit, Natur, Kefir [1:21]'}, {'t': 'Lima und der OP [1:23]'}, {'t': 'Suppe, Sauerkraut, Joghurt [1:26]'}, {'t': 'Vowst, Stuhltransplantation [1:27]'}, {'t': '„Wir sind stark“ [1:29]'}]},
 ]}

folge = {'typ': 'folge', 'k': K, 'titel': TITEL, 'gast': 'Heiko Schöning und Dr. Nina',
 'rolle': 'Arzt und Autor („Game Over“, „Angriff aufs Mikrobiom“) · Ärztin aus München („Vitalmedizin“)',
 'kanal': 'REALTALK MEDIA', 'datum': DATUM, 'dauer': DAUER, 'url': URL,
 'thema': 'Heiko Schöning deutet die Massen-Vorbeugung mit Antibiotika nach einem Meningitis-Ausbruch in England als Beginn von „Corona 2.0“ und als geplanten Angriff auf das Mikrobiom; die Ärztin „Dr. Nina“ erklärt das Mikrobiom, ihre Sicht auf mRNA und Nanopartikel und was sie für die Darmgesundheit rät.',
 'kacheln': []}

R1 = {'id': K, 'titel': G + ': Überblick', 'bloecke': [
 folge,
 {'typ': 'hinweis', 'text': 'Auswertung nach dem Transkript (automatische Untertitel): Gesagtes ohne Zeichen, Ergänzungen 📚, Unklares ❓. Fundstellen [Stunde:Minute] springen ins Video. **Gesundheitsthema:** Aussagen der Gäste stehen als „[seine Sicht]“ bzw. „[ihre Sicht]“; im Reiter „Abgleich & Daten“ steht daneben der Stand der Fachstellen (RKI, STIKO, PEI, EMA u. a.). Das ist keine medizinische Beratung und keine Empfehlung – bei Beschwerden oder Fragen zu Arzneien und Impfungen bitte Ärztin oder Arzt fragen. Die Bewertung bleibt dem Leser.'},
 {'typ': 'abschnitt', 'titel': '⚡ In Kürze', 'liste': [
  'Zweites Gespräch von REALTALK MEDIA mit Heiko Schöning, diesmal zusammen mit einer Ärztin („Dr. Nina“); aufgenommen Anfang April 2026.',
  'Die ersten rund 20 Minuten sind ein Nachrichtenblock des Gastgebers (Israel, Iran-Krieg, Libanon, USA).',
  'Schöning nennt die Antibiotika-Abgabe an viele Gesunde nach einem Meningitis-Ausbruch in England „Corona 2.0“ und eine „gefälschte Pandemie“ [seine Sicht].',
  'Er sieht dahinter einen Plan in Phasen und nennt Jeffrey Epstein, Leslie Wexner und das Wexner Medical Center [seine Sicht].',
  'Dr. Nina erklärt das Mikrobiom, hält vorbeugende Antibiotika für falsch, bei echter Infektion aber für lebensrettend, und äußert Bedenken zu mRNA und Nanopartikeln [ihre Sicht].',
  'Schöning erzählt von seiner eigenen Meningokokken-Erkrankung mit 19, von seinem Auftritt im Bundestag und von einem Gewahrsam in Bremen 2020.',
  'Zum Schluss Ratschläge beider für das Mikrobiom: Natur, vielfältiges Essen, Fermentiertes – und Dr. Ninas Satz, man solle keine Angst haben.',
  'Im Abgleich stehen dazu die Angaben der britischen und deutschen Gesundheitsbehörden, Studien zum Mikrobiom und der Prüfstand für Staat und Institutionen.']},
 {'typ': 'abschnitt', 'titel': '🔦 Aus Schönings und Dr. Ninas Sicht – der rote Faden', 'liste': [
  'Schöning [seine Sicht]: Wer eine Pandemie ankündigen konnte, erkennt auch die nächste. Entscheidend sei nicht der Erreger, sondern das Muster – Angstbilder, Massenabgabe eines Mittels an Gesunde, Auftritt eines Ministers.',
  'Schöning [seine Sicht]: Das Ziel sei das Mikrobiom, die natürliche Abwehr des Menschen. Antibiotika in Massen schwächten es und züchteten Resistenzen; darauf folgten Einschränkungen und neue Präparate.',
  'Schöning [seine Sicht]: Die Planer seien ein Geflecht aus Reichen, Geheimdiensten und organisiertem Verbrechen; Namen und Belege stünden in seinem Buch.',
  'Dr. Nina [ihre Sicht]: Der Mensch werde seit Jahrzehnten von der Natur und seinen Mikroben getrennt; ein geschwächtes Mikrobiom mache ängstlich und lenkbar.',
  'Dr. Nina [ihre Sicht]: Die Gefahr komme nicht nur aus dem Westen; weltweit werde an Nanotechnologie und Biowaffen gearbeitet.',
  'Beide: Aufklärung und ein gestärkter Körper seien der Ausweg – in die Natur gehen, vielfältig essen, sich nicht ängstigen lassen. Was Fachstellen dazu sagen, steht unter „Abgleich & Daten“.']},
 {'typ': 'text', 'text': '🎯 **Kernaussagen** – die zehn wichtigsten Thesen des Gesprächs:'},
 {'typ': 'tabelle', 'kopf': ['#', 'Aussage', 'Begründung im Gespräch', 'Fundstelle', 'Gewicht'], 'zeilen': KERN},
 BAUM,
 {'typ': 'illu', 'id': 'corona2_mikrobiom', 'titel': 'Skizze: Wo Mikroben im Körper leben und was sie beeinflusst (schematisch)'},
 {'typ': 'illu', 'id': 'corona2_meningokokken', 'titel': 'Skizze: Meningokokken in Zahlen (belegte Daten)'},
 {'typ': 'tabelle', 'kopf': ['🧭 Steckbrief', ''], 'schmal': True, 'zeilen': [
  ['Thema in einem Satz', 'Antibiotika-Vorbeugung nach einem Meningitis-Ausbruch als „Corona 2.0“, das Mikrobiom und wie man es schützt.'],
  ['Titel', TITEL],
  ['Format', 'Sendung „Good Morning Germany“: rund 20 Minuten Nachrichtenblock, dann Videogespräch zu dritt; Werbe-Einblendung (Probiotikum) und Hinweis auf Patreon'],
  ['Sprecher', 'Gastgeber (Name nicht belegt ❓), Heiko Schöning, „Dr. Nina“ (Nachname im Untertitel unklar ❓)'],
  ['Dauer', DAUER],
  ['Datum', DATUM + ' – aufgenommen Anfang April 2026 (Reuters-Meldung vom 1.4.2026 wird verlesen)'],
  ['Grundton', 'warnend bei Schöning, erklärend und am Ende beruhigend bei Dr. Nina; der Gastgeber fragt nach Gegenstimmen und hakt bei einzelnen Ratschlägen nach'],
  ['Hinweis', 'Erstes Gespräch der beiden: ' + SCH1 + '. Gesundheitsaussagen sind Sicht der Gäste; Stand der Fachstellen im Abgleich.'],
 ]},
]}

R2 = {'id': K + 'ab', 'titel': G + ': Gespräch im Detail', 'bloecke': [
 {'typ': 'text', 'text': '%d Abschnitte in der Reihenfolge des Videos. Lesehilfe: 💬 Zitat, 📌 Aussage, 🔗 Bezug, 📚 Ergänzung, ❓ unklar. Aussagen zu Gesundheit sind die Sicht der Sprechenden; der Stand der Fachstellen steht im Reiter „Abgleich & Daten“.' % len(AB)},
 {'typ': 'gespraech', 'titel': '🧭 Gesprächsverlauf – wann worüber gesprochen wird', 'dauer': '1:33', 'themen': THEMEN, 'teile': TEILE},
] + AB}

R3 = {'id': K + 'zeit', 'titel': G + ': Zeitachse & Verzeichnisse', 'bloecke': [
 {'typ': 'zeitachse', 'titel': '📅 Zeitachse – Ereignisse, die im Gespräch vorkommen', 'eintraege': ZA},
 {'typ': 'tabelle', 'kopf': ['👤 Person', 'Wer / was', 'Rolle im Gespräch', 'Fundstelle'], 'zeilen': PERS},
 {'typ': 'tabelle', 'kopf': ['🗺️ Ort', 'Rolle', 'Fundstelle'], 'zeilen': ORTE},
 {'typ': 'tabelle', 'kopf': ['📖 Begriff', 'Erklärung', 'Fundstelle'], 'zeilen': BEGR},
 {'typ': 'tabelle', 'kopf': ['📊 Zahl im Gespräch', 'Angabe', 'Fundstelle'], 'zeilen': ZAHL},
]}

R4 = {'id': K + 'abgleich', 'titel': G + ': Abgleich & Daten', 'bloecke':
 list(FA.get('diagramme', [])) + [
 {'typ': 'text', 'text': 'Neutraler Abgleich: links die Aussage im Gespräch, rechts die gängige Darstellung bzw. Daten mit Quelle. Die Bewertung bleibt dem Leser. Keine medizinische Beratung – bei Beschwerden wie hohem Fieber, starken Kopfschmerzen, Nackensteife oder punktförmigen Hautblutungen sofort den Notruf 112 wählen.'},
 {'typ': 'tabelle', 'kopf': ['Aussage im Gespräch', 'Gängige Darstellung (Mainstream) / Daten 📚', 'Quelle'], 'stapel': True, 'zeilen': abg_zeilen},
 {'typ': 'abschnitt', 'titel': '🧩 Spannungen im Gespräch', 'liste': [
  'Der Gastgeber fragt, ob Ärzte Schöning widersprechen [0:29]; Schöning nennt keine Gegenstimmen, sondern bekräftigt seine Sicht.',
  'Schöning warnt vor der Massenabgabe von Antibiotika – und sagt zugleich, Penicillin habe ihm das Leben gerettet und die Fälle in England nehme er „absolut ernst“ [0:43].',
  'Dr. Nina widerspricht dem Gastgeber: Meningitis gebe es auch hier; die Zahlen zur Impfung kenne sie aber nicht [0:35].',
  'Zur Erholung des Mikrobioms nach Antibiotika setzen die Gäste verschiedene Akzente: „Jahre“ (Schöning) [1:26], „es baut sich wieder auf“ (Dr. Nina) [1:29].',
  'Schöning verortet die Verantwortlichen vor allem in den USA; Dr. Nina weitet das auf alle Großmächte aus [1:13] – Schöning stimmt zu.',
  'Schöning sprach auf Einladung eines AfD-Abgeordneten im Bundestag; Dr. Nina lehnte eine ähnliche Einladung ab [0:55].',
  'Der Gastgeber hakt beim Rat „Kinder im Dreck spielen lassen“ nach [1:23].',
  'Im Video zum Schutz des Mikrobioms läuft Werbung für ein Probiotikum [0:06]; beide Gäste halten wenig von Präparaten [1:22, 1:28].']},
 {'typ': 'abschnitt', 'titel': '💡 Was man mitnehmen kann', 'liste': [
  'Worüber sich Gäste und Fachstellen einig sind und wo nicht, zeigt die Tabelle Zeile für Zeile – etwa bei der Frage, wem Antibiotika nach einem Meningokokken-Fall angeboten werden.',
  'Das Mikrobiom ist ein junges Forschungsfeld; viele Zusammenhänge stammen aus Tierversuchen (siehe Abgleich).',
  'Die Ratschläge zur Ernährung (vielfältig, ballaststoffreich, Fermentiertes) decken sich in weiten Teilen mit Empfehlungen von Fachgesellschaften.',
  'Verdacht auf Meningitis ist ein Notfall: nicht abwarten, 112 anrufen.']},
 {'typ': 'abschnitt', 'titel': '❓ Offen', 'liste': [
  'Voller Name der Ärztin und des Gastgebers; genaues Veröffentlichungsdatum des Videos (soweit oben mit ❓).',
  'Schönings Schilderungen zur Szene vor dem Bundestag und zum Gewahrsam in Bremen – soweit keine unabhängige Quelle gefunden wurde, stehen sie nur als seine Angabe da.',
  'Die Belege, auf die Schöning für den behaupteten Plan verweist, stehen in seinem Buch und wurden hier nicht geprüft.',
  'Der Name, den Schöning im Bundestag genannt haben will, fällt im Gespräch nicht.']},
 {'typ': 'abschnitt', 'titel': '🔎 Weiter recherchieren', 'liste': [
  'Lageberichte der britischen Gesundheitsbehörde UKHSA zum Ausbruch und das Protokoll der Parlamentsdebatte.',
  'RKI-Ratgeber Meningokokken und die Empfehlungen der STIKO.',
  'Erstes Gespräch mit Schöning samt Abgleich: ' + SCH1A + '.',
  'Übersichtsarbeiten zum Darm-Mikrobiom und zur Wirkung von Antibiotika (Quellen in der Tabelle oben).']},
]}

quellen = [['Video: ' + TITEL + ' – REALTALK MEDIA (YouTube)', URL]] + [list(q) for q in FA.get('quellen', [])]
for z in abg_zeilen:
    for t, u in re.findall(r'\[([^\]]+)\]\((https?://[^)\s]+)\)', z[2]): quellen.append([t, u])
gesehen = set(); Q2 = []
for q in quellen:
    if q[1] not in gesehen: gesehen.add(q[1]); Q2.append(q)

F = {'k': K, 'gast': 'Heiko Schöning und Dr. Nina', 'reiter': [R1, R2, R3, R4],
 'folgen_zeile': [DATUM, 'Heiko Schöning und Dr. Nina', TITEL, 'Meningitis-Ausbruch, Antibiotika, Mikrobiom, mRNA', '{{a:realtalk-corona2|hier: Corona 2.0}}', '[ansehen](%s)' % URL],
 'neu': {'d': '2026-11-12', 't': 'REALTALK MEDIA – „Corona 2.0“ mit Schöning und Dr. Nina',
         'k': 'Antibiotika-Vorbeugung, Mikrobiom, mRNA: %d Abschnitte, Abgleich mit Fachstellen, Diagramme und Prüfstand.' % len(AB),
         'h': '#a-realtalk-corona2', 'art': 'Video'},
 'quellen': Q2, 'web': [list(w) for w in FA.get('web', [])]}
json.dump(F, open(O + '/folge.json', 'w'), ensure_ascii=False, indent=1)
print('folge.json', len(AB), 'Abschnitte', len(abg_zeilen), 'Abgleich', len(ZA), 'Zeitachse', len(FA.get('diagramme', [])), 'Diagramme', 'fehlende Fakten:', [k for k, _ in ABG if k not in FZ])
