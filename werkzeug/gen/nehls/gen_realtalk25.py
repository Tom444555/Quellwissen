# -*- coding: utf-8 -*-
# Erzeugt folge.json für „MICHAEL NEHLS | Handystrahlen | RFK & Trump | Träume | Evolution & Glaube | Intelligenz“
# (K = realtalk25, Autor A-01 nehls, Reiter-Präfix „Realtalk Mai 2025“). Gesundheitsthema: Die Nacherzählung
# (Überblick, Abschnitte, Zeitachse, linke Abgleich-Spalte) ist von Hand aus dem Transkript geschrieben; die belegte
# Seite (rechte Spalte, Diagramme, Prüfstand, Skizzen) kommt aus fakten.json / pruefstand.json des Helfers.
import json, os, re
O = os.path.dirname(os.path.abspath(__file__))
K = 'realtalk25'; G = 'Realtalk Mai 2025'
URL = 'https://www.youtube.com/watch?v=GDsVuJ9UbLw'
TITEL = 'MICHAEL NEHLS | Handystrahlen | RFK & Trump | Träume | Evolution & Glaube | Intelligenz'
DAUER = '2 Std. 22 Min.'
FA = json.load(open(O + '/fakten.json')) if os.path.exists(O + '/fakten.json') else {}
V = FA.get('video', {})
DATUM = V.get('datum') or '2025 ❓'
if '❓' in DATUM: DATUM = '2025 ❓'
FZ = {z['k']: z for z in FA.get('zeilen', [])}
HILFE = 'Wer an Suizid denkt, findet rund um die Uhr Hilfe bei der Telefonseelsorge: 0800 111 0 111.'
BLI = '{{b:lithium|Lithium (Biochemie)}}'
BOM = '{{b:omega3|Omega-3-Fettsäuren (Biochemie)}}'
WDE = '{{w:demenz|Demenz in Zahlen}}'
WSU = '{{w:suizid|Suizid in Zahlen}}'
GAN = '{{a:ganser|Daniele Ganser (A-04)}}'
EIN = '{{a:nehls-einordnung|Abgleich zu Nehls’ Kernideen}}'
RTK = '{{a:realtalk|REALTALK MEDIA (A-12)}}'

def ab(titel, th, *liste):
    return {'typ': 'abschnitt', 'titel': titel, 'th': th, 'liste': list(liste)}

THEMEN = [
    {'k': 'a', 'n': 'Lithium & Buch'},
    {'k': 'b', 'n': 'Impfungen, Aluminium, Autismus'},
    {'k': 'c', 'n': 'Hippocampus, Schlaf, Träume'},
    {'k': 'd', 'n': 'Race Across America'},
    {'k': 'e', 'n': 'Evolution, Gene, Glaube'},
    {'k': 'f', 'n': 'Herkunft, Sprache, Intelligenz'},
    {'k': 'g', 'n': 'Alzheimer-Mittel & Pharma'},
    {'k': 'h', 'n': 'Politik: RFK, USA, EU'},
    {'k': 'w', 'n': 'Werbung/Organisatorisches'},
]

AB = [
 ab('🎬 Begrüßung und Vorgeplänkel [0:00–0:03]', 'w',
    'Michael Nehls ist zum zweiten Mal bei REALTALK zu Gast; aufgenommen wird am 1. Mai, draußen läuft eine Feier. Die beiden Gastgeber sprechen kurz über ein früheres Gespräch mit Jasmin Kosubek und über wechselhafte Kommentare im Livechat.',
    '📌 Für Nehls’ Werdegang verweisen sie auf das erste Gespräch [0:00–0:01].',
    '💬 „Der Held von heute ist der Kriegsverbrecher von morgen“ (Gastgeber, scherzhaft) [0:03]'),
 ab('📖 Das neue Buch und der Kinderarzt aus Potsdam [0:03–0:05]', 'a',
    'Nehls überreicht sein neues Buch über Lithium. Er habe monatelang sieben Tage die Woche zwölf Stunden daran gearbeitet; die erste Auflage sei vergriffen.',
    '📌 Antrieb seien Rückmeldungen eines Kinderarztes aus Potsdam gewesen (Name im Untertitel unsicher ❓), der Kindern Lithium in kleiner Menge gebe und täglich Sprachnachrichten von Eltern weiterleite [0:04].',
    '💬 „Dieses Buch wird die Welt verändern“ (Nehls) [0:03]',
    '🔗 Zum Stoff selbst: ' + BLI + '.'),
 ab('🤝 Gastgeber wünscht sich ein Streitgespräch [0:05–0:06]', 'a',
    'Der Gastgeber sagt, er kenne Mediziner, die Nehls’ Lithium-These kritisch sehen, und schlägt ein Gespräch mit einer solchen Fachkraft vor. Nehls fände das spannend, glaubt aber nicht, dass es zustande kommt.',
    '📌 Nehls: Im Buch steckten über 1.000 Studien; es gebe keine einzige, die seinen Erkenntnissen widerspreche [seine Sicht] [0:05–0:06].',
    '💬 „Die wissenschaftliche Sachlage, die ist so eindeutig auf meiner Seite“ (Nehls) [0:05]'),
 ab('🧒 Autismus und die „autobiografische Gedächtniszentrale“ [0:06–0:08]', 'c',
    'Als Beispiel für Erfahrungen des Kinderarztes nennt Nehls Autismus. Er beschreibt ihn als Entwicklungsstörung, die sich meist mit anderthalb bis zwei Jahren zeige – in der Zeit, in der der Hippocampus reife, den er „autobiografische Gedächtniszentrale“ nennt.',
    '📌 Entzündungen im Gehirn (Neuroinflammation) oder Mängel könnten diese Reifung stören; daher fehle der Blickkontakt und das soziale Lernen [seine Sicht] [0:06–0:07].',
    '📌 Der Co-Gastgeber sagt, in seiner Familie gebe es einen Fall [0:07–0:08].'),
 ab('💉 Fallbeispiel, Impfungen und Aluminium [0:08–0:10]', 'b',
    'Nehls schildert ein zweieinhalb- bis dreijähriges Kind mit Autismus-Diagnose, das neben Vitamin D und Omega-3 auch Lithium bekommen habe. Lithium sei kein Allheilmittel, dämpfe aber die Neuroinflammation [seine Sicht].',
    '📌 Impfungen in den ersten zwei Lebensjahren lösten Neuroinflammation aus; mit der Zahl der Impfungen steige die Autismus-Rate. Er beruft sich auf eine Studie vom März 2025, deren Grafiken er ins Buch übernommen habe [seine Sicht] [0:08–0:09].',
    '📌 Aluminium in Impfstoffen sei giftig für das Gehirn und der „Gegenspieler“ von Lithium [seine Sicht] [0:09–0:10].'),
 ab('🌍 Lithium in der „Wiege der Menschheit“ – und der Verlauf des Falls [0:10–0:12]', 'a',
    'Nehls sagt, das Kind habe nur die Menge bekommen, die „natürlich“ wäre. In Deutschland seien Leitungswasser und Nahrung lithiumarm; dort, wo sich das menschliche Gehirn entwickelt habe, sei Lithium Teil der Grundnahrung gewesen. Er vergleicht das mit Jodmangel in den Alpen.',
    '📌 Nach ein bis zwei Wochen habe das Kind die Mutter erstmals angeschaut; nach den Ferien habe die Betreuerin an der Diagnose gezweifelt [0:11–0:12].',
    '📌 Der Gastgeber: „fast eine Wunderheilung, wenn das stimmt“; Nehls: Man habe nur einen krank machenden Mangel behoben [seine Sicht] [0:12].'),
 ab('❓ Angeboren oder erworben? Die „verletzliche Phase“ und eine Lämmer-Studie [0:12–0:16]', 'b',
    'Der Co-Gastgeber sagt, er habe gedacht, Autismus bestehe von Geburt an. Nehls antwortet, eine Neigung könne da sein, entscheidend sei aber die Phase zwischen anderthalb und zwei Jahren. In dieser Zeit dürften keine Schadstoffe in den Körper kommen – Impfstoffe zählt er dazu [seine Sicht].',
    '📌 Die Studie von 2025 zeige Epilepsie, Lernstörungen, Autismus und ADS in Abhängigkeit von der Zahl der Injektionen [seine Sicht] [0:13–0:14].',
    '📌 Rund 50 % der Impfstoffe enthielten Aluminium; Formaldehyd sei teils noch enthalten, Quecksilber wohl nicht mehr [0:14].',
    '📌 Versuch mit Lämmern: Kochsalz, nur Aluminiumhydroxid oder Aluminium mit Impfstoff – die beiden Aluminium-Gruppen hätten nach einem Jahr auffälliges Sozialverhalten gezeigt. Damit sei die Ursache „im Prinzip schon bewiesen“ [seine Sicht] [0:14–0:15].'),
 ab('📜 „Grundgesetze des Lebens“, Pockenimpfung und „80 Impfungen“ [0:16–0:18]', 'b',
    'Nehls sagt, er sei als Kind geimpft worden, aber weit weniger als Kinder heute. Sein erstes Buchkapitel heiße „Grundgesetze des Lebens“: Nichts Nötiges dürfe fehlen (Gesetz des Minimums), nichts dürfe übertrieben werden (Gesetz des Maximums).',
    '📌 Früher habe man gesünder gegessen, mehr draußen gespielt, ohne Fernseher – das Gehirn sei widerstandsfähiger gewesen [seine Sicht] [0:16].',
    '📌 Erinnerung an die Pockenimpfung mit Hautritzung; ein Vierjähriger habe heute „80 Impfungen“ hinter sich [0:17].',
    '📌 Das sei seine „Nagelprobe“ für Robert F. Kennedy [0:17–0:18].'),
 ab('⚖️ Lithium verboten, Aluminium erlaubt [0:18–0:22]', 'a',
    'Nehls stellt gegenüber: Lithium sei in Europa als Nahrungsergänzung verboten, obwohl die meisten Europäer einen Mangel hätten; Aluminium dürfe Lebensmitteln zugesetzt werden. Sein Buch beweise auf fast 100 Seiten mit sechs Argumenten, dass Lithium lebensnotwendig sei [seine Sicht].',
    '📌 Zahlen im Gespräch: 28 E-Nummern mit Aluminium; für einen 70-kg-Menschen gälten in Europa 10 mg Aluminium täglich als unbedenklich, die WHO habe 2011 auf 20 mg erhöht; 1 mg Lithium sei dagegen verboten [0:18–0:19].',
    '📌 Laugenbrezeln von Aluminiumblechen seien aluminiumreich; er selbst nutze nur Geräte aus Stahl [0:20–0:21].',
    '📌 Der Gastgeber meint, Aluminiumpfannen seien billiger; Nehls weist auf den hohen Stromverbrauch der Herstellung hin [0:21].'),
 ab('🕊️ Empathie, Frieden und das „mentale Immunsystem“ [0:22–0:24]', 'c',
    'Der Hippocampus ist für Nehls das Zentrum der geistigen Gesundheit: Denkfähigkeit, Belastbarkeit, Neugier, Erinnerung – und die Fähigkeit, sich in andere hineinzuversetzen. Ohne sie gebe es keinen Kompromiss und keinen Frieden [seine Sicht].',
    '💬 „die Friedensfähigkeit hängt davon ab, dass meine autobiografische Gedächtniszentrale funktioniert“ (Nehls) [0:23]',
    '🔗 Darüber wolle er mit ' + GAN + ' sprechen [0:23].',
    '📌 Aluminium schwäche dieses „mentale Immunsystem“, Lithium sei der Gegenpol [seine Sicht] [0:23–0:24].'),
 ab('🧠 Trauma, Stress und ein schrumpfender Hippocampus [0:24–0:26]', 'c',
    'Der Gastgeber wendet ein, Krieg und Gewalt hätten auch nicht-stoffliche Ursachen, etwa Traumata. Nehls stimmt zu: Das Stoffliche sei nur der „Nährboden“, auf dem Gedanken wachsen.',
    '📌 Stresshormone ließen den Hippocampus schrumpfen; Menschen mit posttraumatischer Belastungsstörung hätten den kleinsten Hippocampus [0:25].',
    '📌 Neben Trauma-Therapie müsse der Nährboden stimmen: Giftstoffe raus, Vitalstoffe rein. Der Hippocampus könne als einziger Hirnbereich lebenslang wachsen [seine Sicht] [0:26].'),
 ab('🇨🇭 IC Forum Basel 2024: „Was braucht das Gehirn, um Frieden zu denken?“ [0:26–0:29]', 'h',
    'Nehls berichtet von einem Hauptvortrag am 12. April 2024 beim IC Forum in Basel auf Einladung des Schweizer Außenministeriums, vor 1.500 Delegierten aus über 100 Staaten; Thema der Tagung sei Frieden gewesen.',
    '📌 In 15 Minuten habe er das „mentale Immunsystem“ erklärt und gesagt, auch das Spike-Protein nach mRNA-Impfung löse Neuroinflammation aus [seine Sicht] [0:27–0:28].',
    '📌 Dort habe er angekündigt, die Lebensnotwendigkeit von Lithium zu beweisen; Lithium sei das „Friedenselement“ [seine Sicht] [0:28].',
    '📌 Gastgeber: Wer biochemisch geschwächt sei, sei also leichter zu beeinflussen? Nehls: Ja [0:28–0:29].'),
 ab('💧 Lithium im Trinkwasser: Kriminalität und Suizid [0:29–0:30]', 'a',
    'Nehls vergleicht Lithiummangel mit der enthemmenden Wirkung von viel Alkohol. Seit 1970 gebe es Studien: Wo das Trinkwasser etwas mehr Lithium enthalte (Mikrogramm je Liter), seien Kriminalität, Gewalt, Drogenkonsum und auch die Suizidrate niedriger.',
    '📌 Gemeint seien Spuren – ein Zehn- bis Hunderttausendstel der Mengen, die in der Psychiatrie gegeben werden [0:29–0:30].',
    '📚 ' + HILFE + ' Zahlen: ' + WSU + '.'),
 ab('📱 Handystrahlen [0:30–0:32]', 'c',
    'Der Co-Gastgeber fragt nach Strahlung. Nehls sagt, auch Funkwellen könnten Neuroinflammation auslösen; ein Handy am Ohr spüre er sofort und halte es deshalb auf Abstand [seine Sicht].',
    '💬 „in der ersten Sekunde merke ich das schon“ (Nehls) [0:31]',
    '📌 Der Gastgeber berichtet von Kribbeln in der Hand, wenn das Handy am Ladekabel hängt [0:31].',
    '📌 Bei Kindern sei die Schädeldecke dünner; die Strahlung dringe nur 1–2 cm ein, das reiche aber für eine Entzündung der äußeren Schichten [seine Sicht] [0:32].'),
 ab('🔗 Von der Korrelation zur „Kausalkette“ [0:32–0:34]', 'a',
    'Nehls räumt ein, dass die Trinkwasser-Studien nur Zusammenhänge zeigen. Sein Buch liefere die Erklärung dazu: wie Lithium in der Zelle auf bestimmte Proteine wirkt, die viele Körperfunktionen steuern – bis hin zum Sozialverhalten [seine Sicht].',
    '💬 „Was mein Buch liefert, ist die molekularen Zusammenhänge“ (Nehls) [0:33]'),
 ab('💊 Kleine und große Mengen: Kalium, Wasser und der „Faktor 85“ [0:34–0:39]', 'a',
    'Der Gastgeber kennt Lithium als Mittel, das teilnahmslos mache, und fragt, ob die niedrigere Suizidrate daher komme. Nehls verneint: Er spreche von Mengen, die 100- bis 1.000-mal kleiner seien als in der Therapie.',
    '📌 Vergleich Kalium: lebensnotwendig, in sehr hoher Dosis tödlich. Auch zu viel Wasser könne gefährlich sein [0:35–0:37].',
    '📌 Zahlen im Gespräch: Zwischen Bedarf und schädlicher Menge liege bei Selen und Zink etwa der Faktor 20, bei Wasser 10, bei Lithium über 85; Lithium sei „das sicherste Spurenelement“ [seine Sicht] [0:37–0:38].',
    '📌 Suizide hingen oft mit schwerer Depression, bipolarer Störung oder Schizophrenie zusammen, die er als Störungen des „mentalen Immunsystems“ mit Lithiummangel als Mitursache einordnet [seine Sicht] [0:34–0:35].',
    '📚 ' + HILFE),
 ab('🩺 John Cade 1949, bipolare Störung, Schizophrenie und der linke Hippocampus [0:39–0:43]', 'a',
    'Nehls erzählt von dem australischen Psychiater John Cade, der 1949 die Wirkung hoch dosierten Lithiums bei Manie beschrieb. Cade habe vermutet, ein Mangel in der Kindheit könne die Ursache sein – für Nehls ein frühes Argument, dass Lithium lebensnotwendig ist.',
    '📌 Zahlen im Gespräch: 1 mg am Tag hält er für nötig; in der Therapie würden 200–400 mg gegeben [0:39].',
    '📌 Auf Nachfrage beschreibt er Schizophrenie als „geteilte Seele“ mit Wahn und unsicherer Identität, bipolare Störung als Wechsel von Depression und Manie [0:41].',
    '📌 Beide seien, wie Autismus, Entwicklungsstörungen des Hippocampus; bei Rechtshändern trage der linke Hippocampus das „mentale Immunsystem“, und der Körper lenke knappes Lithium gezielt dorthin [seine Sicht] [0:41–0:43].'),
 ab('🕵️ Gastgeber fragt nach MK-Ultra [0:43–0:45]', 'c',
    'Der Gastgeber fragt nach dem CIA-Programm MK-Ultra. Nehls kennt es nicht. Der Gastgeber erklärt es als Programm, das mit Elektroschocks, LSD und Folter gespaltene Persönlichkeiten und sogar Attentäter erzeugt habe, und nennt den früheren CIA-Mitarbeiter Kevin Shipp [seine Sicht].',
    '📌 Nehls hält das für vorstellbar und leitet zu seiner Erfahrung mit Schlafentzug über [0:44].'),
 ab('🌙 Schlaf als „Upload“ und warum man Träume vom Ende her erinnert [0:45–0:48]', 'c',
    'Nehls erklärt sein Bild vom Gedächtnis: Der daumengroße Hippocampus speichere, was am Tag wichtig und gefühlsbetont war, und sei abends voll. Im Tiefschlaf werde in die Großhirnrinde („Festplatte“) übertragen, im REM-Schlaf mit Älterem verknüpft – das erlebe man als Traum.',
    '📌 Der Gastgeber vergleicht: Arbeitsspeicher und Festplatte; Nehls: wie eine volle Speicherkarte [0:46–0:47].',
    '📌 Man erinnere nur den Schluss eines Traums, weil der Hippocampus erst beim Aufwachen wieder aufzeichne [seine Sicht] [0:48].'),
 ab('💭 Luzides Träumen und Träume nach Psychiatrie-Medikamenten [0:48–0:53]', 'c',
    'Der Gastgeber erzählt von Klarträumen, in denen er die Genauigkeit der Traumwelt prüft, und von seiner Vermutung einer festen „Traumzeit“. Der Co-Gastgeber berichtet, er sei zehn Jahre in der Psychiatrie gewesen und habe unter Neuroleptika nicht geträumt.',
    '📌 Er schildert einen wiederkehrenden Traum, der sich als echte Kindheitserinnerung herausgestellt habe [0:52–0:53].',
    '❓ Auf die Frage nach der „Traumzeit“ geht Nehls nicht direkt ein.'),
 ab('🔁 Zwei Wirklichkeiten und „über Probleme schlafen“ [0:53–0:55]', 'c',
    'Nehls sagt, erinnerte Träume würden erneut gespeichert, verarbeitet und leicht verändert wieder geträumt. Das Gehirn verknüpfe nachts nach unbekannten Regeln neu; deshalb wache man oft klüger auf.',
    '💬 „deswegen soll man auch über Probleme schlafen“ (Nehls) [0:54]'),
 ab('🚴 Race Across America: Schlafentzug und Jure Robič [0:55–0:59]', 'd',
    'Als Beispiel für erzeugte Wahnbilder nennt Nehls das Radrennen quer durch die USA (4.800 km ohne Etappen). Fast alle Fahrer schliefen nur etwa eine Stunde am Tag; nach zwei bis drei Tagen beginne das Gehirn im Wachen zu „träumen“.',
    '📌 Der fünfmalige Sieger Jure Robič, Berufssoldat aus Slowenien, sei die ersten 48 Stunden ohne Schlaf gefahren und habe verfolgende Reiter gesehen; sein Team habe ihn damit angetrieben [0:56–0:58].',
    '📌 Veteranen hätten gesagt, Wahnbilder seien nicht zu vermeiden [0:57].'),
 ab('🏨 Nehls’ Weg: acht Stunden Schlaf – und eine Studie über ihn [0:59–1:02]', 'd',
    'Nehls sagt, er sei als Einziger jede Nacht für acht Stunden ins Hotel gegangen. Um Doping-Verdacht vorzubeugen, habe eine Universität ihm vor und während des Rennens täglich Blut abgenommen und Puls und Leistung gemessen.',
    '📌 Ergebnis laut Nehls: am Ziel rund 10 % leistungsfähiger als am Start; Platz fünf und Platz sechs bei zwei Teilnahmen [0:59–1:00].',
    '📌 Kurz vor dem Ziel habe er einen Weltmeister im zehnfachen Ironman überholt; seine Kinder hätten gefilmt und Interviews geführt [1:00–1:01].',
    '📌 Robič sei später bei einem Unfall mit dem Mountainbike gestorben [1:02].'),
 ab('🛣️ Extremsport: Jonas Deichmann, Sekundenschlaf, 880 km am Stück [1:02–1:04]', 'd',
    'Die Gastgeber erzählen vom Extremsportler Jonas Deichmann – das Gefährlichste sei der Straßenverkehr – und von Triathlon-Erfahrungen. Nehls nennt Sekundenschlaf bergab als größte Gefahr des Rennens.',
    '📌 Seine erste Etappe sei 880 km ohne Pause lang gewesen [1:03–1:04].'),
 ab('😴 Lithium, Magnesium und Tiefschlaf [1:04–1:06]', 'a',
    'Lithium steuere den Tag-Nacht-Rhythmus; wer die von ihm empfohlene kleine Menge nehme, berichte fast durchweg von tieferem Schlaf und lebhafteren Träumen [seine Sicht]. Lithium und Magnesium wirkten zusammen für das innere Gleichgewicht (Homöostase).',
    '💬 „jetzt räumt endlich mal jemand da oben auf“ (Leserin laut Nehls) [1:05]'),
 ab('🤷 „Ich merke nichts“ – der Gastgeber widerspricht aus Erfahrung [1:06–1:10]', 'a',
    'Der Gastgeber sagt, er habe Vitamin D (zeitweise 30.000 Einheiten täglich), Magnesium, Omega-3 und 1 mg Lithium ausprobiert und keinerlei Wirkung gespürt. Nehls antwortet, vielleicht habe er keinen Mangel; das sei gut so.',
    '📌 Der Nutzen zeige sich in der Statistik und unter Belastung: Wer stabil sei, merke wenig; wer stark gefordert werde, profitiere [seine Sicht] [1:08–1:09].',
    '📌 Beispiel Vitamin D: Ein starker Mangel mache Infektionen gefährlich, weil das Immunsystem überreagiere („Zytokinsturm“) [seine Sicht] [1:09].',
    '📌 Der Kinderarzt sehe die deutlichste Wirkung bei Kindern mit plötzlichen seelischen Problemen [1:10].'),
 ab('🧪 Passt eine Lösung für alle? Körpergefühl, Werbung, Omega-3 [1:10–1:15]', 'a',
    'Der Gastgeber meint, man könne nicht eine Lösung auf alle übertragen; sein Körper melde sofort, was ihm bekomme – Omega-3-Präparate etwa nicht, L-Glutamin dagegen schon. Es folgt eine Werbe-Einblendung für ein Glutamin-Produkt mit Rabattcode.',
    '📌 Nehls: Man solle auf sich hören, könne Mängel aber nicht immer unterscheiden. Den Omega-3-Index könne man messen; die Hälfte der Fettsäuren in den Synapsen sei DHA [1:13–1:15].',
    '📌 Werbung im Video [1:12–1:13].',
    '🔗 ' + BOM + '.'),
 ab('🐟 Fischer und Sammler, Fischhirn und die Urzelle LUCA [1:15–1:19]', 'e',
    'Nehls sagt, der menschliche Geist sei bei „Fischern und Sammlern“ entstanden; die Fundstätte sei 2024 Weltkulturerbe geworden. Im Gehirn von Fischen sei der Lithiumgehalt 20-mal höher als im Muskelfleisch. Der Gastgeber ergänzt, im Norden Irans esse man das Fischhirn mit.',
    '📌 Lithium habe schon die erste Zelle reguliert, den letzten gemeinsamen Vorfahren allen Lebens (LUCA); er zeige im Buch das zugehörige Gen [seine Sicht] [1:16–1:17].',
    '📌 Zur Person: Arzt, danach sechs Jahre Molekulargenetik, Habilitation [1:17–1:18].',
    '📌 Lithium-gesteuerte Proteine regelten die Autophagie (Zell-Recycling), die auch Viren zerlege; deshalb sei Lithium bei Covid oder anderen Infekten „das Mittel der Wahl“ [seine Sicht] [1:18–1:19].'),
 ab('🧩 GSK-3, Zivilisationskrankheiten und die Pharmaindustrie [1:19–1:24]', 'g',
    'Nehls erklärt die Homöostase am Bild eines Menschen, der im Stehen ständig ausgleicht. Fehle Lithium, sei das Enzym GSK-3 überaktiv – das sei die Hauptursache aller Zivilisationskrankheiten, an denen 90 % der Menschen sterben [seine Sicht].',
    '📌 Die Pharmaindustrie investiere seit 1980 jährlich 10 Milliarden, um GSK-3 zu beeinflussen; sie suche patentierbare Stoffe, die wie Lithium wirken, und wolle Lithium selbst nicht [seine Sicht] [1:21–1:23].',
    '📌 Das habe er in Basel gesagt, „dem Epizentrum der Pharmaindustrie“ [1:23].',
    '💬 „nichts anderes als Lithium-Mimetika“ (Nehls über gesuchte Wirkstoffe) [1:23]'),
 ab('⚡ Psychosen, Epilepsie und das Jahr 1949 [1:24–1:26]', 'a',
    'Der Co-Gastgeber fragt nach Hilfe bei psychotischen Schüben. Nehls nennt Schübe und auch Epilepsie entzündliche Vorgänge im Gehirn, die sich mit Lithium beherrschen ließen; der Kinderarzt berichte von Kindern, bei denen die Krampfneigung im EEG verschwunden sei [seine Sicht].',
    '📌 1949, im Jahr von Cades Entdeckung, sei Lithium „verboten“ worden; Todesfälle durch Überdosierung seien der US-Behörde FDA gelegen gekommen [seine Sicht] [1:25–1:26].'),
 ab('🧬 Der Molekulargenetiker: „Nacktmaus-Gen“ und innere Organe [1:26–1:28]', 'e',
    'Nehls beschreibt seine Forschung: Aufklärung von Erbkrankheiten, Methoden zur Veränderung des Erbguts. Er habe ein Gen gefunden, ohne das es kein anpassungsfähiges Immunsystem gibt („Nacktmaus-Gen“), und ein Gen, ohne das keine inneren Organe entstehen.',
    '📌 Bei jedem neuen Gen habe er gefragt, wann es in der Evolution entstanden ist [1:27–1:28].'),
 ab('🐺 Evolution im Labor, Hund und Kohl – oder doch ein Schöpfer? [1:28–1:31]', 'e',
    'Auf die Frage nach Darwin sagt Nehls, Evolution funktioniere: Seine Firma habe sie im Modell tausendfach beschleunigt. Sein kleiner Spitz sei vor etwa 5.000 Jahren noch Wolf gewesen; Kohlrabi und Brokkoli stammten von einer rapsähnlichen Pflanze.',
    '📌 Er bleibt vorsichtig: Er sehe nur, was er sehe; die Welt könne auch anders sein [1:30].',
    '💬 „vielleicht gibt’s auch ein Schöpfer, der all diese Wesen geschaffen hat“ (Nehls) [1:31]'),
 ab('🙏 Glaube, Bücher und Demut [1:31–1:34]', 'e',
    'Nehls sagt, er gehöre keiner bestimmten Religion an. Er lese seit der Kindheit alles: 70–80 Bücher über Religionen, 200–300 über Philosophie, 150 über Physik – und wisse, je mehr er lese, desto weniger.',
    '📌 Er nehme seit sieben bis acht Jahren täglich Lithium, seit er auf den Zusammenhang mit Alzheimer gestoßen sei; er glaubt, dadurch offener geworden zu sein [seine Sicht] [1:33].',
    '💬 „da bin ich einfach nur demütig“ (Nehls über die Herkunft der Schöpfung) [1:34]',
    '🔗 ' + WDE + '.'),
 ab('🌍 Pinnacle Point: der „Garten Eden“ und 1.300 Ethnien [1:34–1:39]', 'f',
    'Der Gastgeber fragt nach Eugenik und der Vererbung von Intelligenz. Nehls holt aus: Alle rund 1.300 Ethnien gingen auf eine Gruppe zurück, die eine Eiszeit an der Küste Südafrikas überlebt habe – am Pinnacle Point bei Mossel Bay, seinem „Garten Eden“.',
    '📌 Dort reichten Funde 160.000 Jahre zurück; die Muschelnahrung habe täglich 1–2 mg Lithium geliefert [seine Sicht] [1:36–1:37].',
    '📌 Hautfarben seien Anpassungen an das Licht (Vitamin D) [1:35–1:36].',
    '💬 „dass alle Menschen auf diesem Planeten die gleiche genetische Potenzial haben“ (Nehls) [1:37]',
    '📌 Vergleich mit Hunderassen und seinem Hund Johnny: verschieden im Aussehen, gleich im Wesen [1:38–1:39].'),
 ab('🗣️ Sprache: Babel, „Mutter“ und alte Wanderungen [1:39–1:44]', 'f',
    'Der Gastgeber bringt den Turmbau zu Babel und eine gemeinsame Ursprache ins Spiel. Nehls stimmt zu, dass Sprachen sich wie Gene auseinanderentwickeln; kulturelle und genetische Evolution folgten derselben Logik.',
    '📌 Gastgeber: Mutter, mother, madre, persisch mādar seien dasselbe Wort; auch Koreanisch und Türkisch seien sich sehr nah [seine Sicht] [1:42–1:43].',
    '📌 Nehls nennt die indogermanischen Sprachen und die Einwanderung nach Amerika über die Beringstraße [1:43–1:44].'),
 ab('🎓 Intelligenz: IQ-Tests, Flynn-Effekt, gleiches Potenzial [1:44–1:49]', 'f',
    'Zur eigentlichen Frage sagt Nehls: Wegen des gemeinsamen Ursprungs hätten alle Menschen das gleiche Potenzial. Ein IQ-Test messe, was der Test misst; der Anstieg der Werte (Flynn-Effekt) komme daher, dass Schulen auf die Tests hin geübt hätten.',
    '📌 In der Wildnis wären Kinder der Hadza unseren Kindern weit überlegen [1:45–1:46].',
    '📌 IQ-Messungen interessierten ihn nicht – wichtig sei das „mentale Immunsystem“: sich einfühlen, planen, Rückschläge aushalten [seine Sicht] [1:47].',
    '📌 Er schließt einen Anteil der Gene nicht aus („hat mit Sicherheit was damit zu tun“), nennt die Genetik aber ein Wunder [1:48].',
    '📌 Die „Grundgesetze des Lebens“ würden im Medizinstudium nicht gelehrt [seine Sicht] [1:47–1:48].'),
 ab('📚 Das Erbgut als Bibliothek: ein Buchstabe genügt [1:49–1:51]', 'e',
    'Nehls veranschaulicht das Erbgut: 1.000 Buchstaben je Seite, 1.000 Seiten je Buch, 3.000 Bücher. Fehle ein bestimmter Buchstabe, gebe es kein anpassungsfähiges Immunsystem – das habe er selbst herausgefunden.',
    '📌 Zahlen im Gespräch: rund 19.500 Gene beim Menschen, 19.000 bei einem 1 mm langen Wurm; Mais habe ein zehnmal größeres Erbgut [1:49].',
    '💬 „für mich absolutes Wunder“ (Nehls über die Entwicklung vom Ei zum Kind) [1:51]'),
 ab('🤖 Transhumanismus und Epigenetik [1:51–1:53]', 'e',
    'Menschen „aus der Retorte“ nennt Nehls eine Katastrophe. Die Prägung im Mutterleib (Epigenetik) sei kaum verstanden: Stress der Mutter mache das Kind ängstlich. Was ohne Mutterleib heranwachse, sei nicht absehbar [seine Sicht].',
    '💬 „Das ist Größenwahnsinn hoch drei“ (Nehls) [1:52]'),
 ab('🧠 Beta-Amyloid als „Schreibschutz“ [1:53–1:56]', 'g',
    'Nehls erklärt, wozu das Gehirn Beta-Amyloid brauche: Es schütze frische Erinnerungen davor, überschrieben zu werden. Mäuse ohne dieses Eiweiß lernten keinen Weg mehr.',
    '📌 Im Tiefschlaf werde es ausgewaschen und in der Leber abgebaut. Wer schlecht schlafe und sich wenig bewege, sammle es an; es verklebe und schade dann den Nervenzellen – eine von mehreren Ursachen für Alzheimer [seine Sicht] [1:55–1:56].'),
 ab('💉 Antikörper gegen Amyloid: Zulassung und Nebenwirkungen [1:56–1:59]', 'g',
    'Die Pharmaindustrie habe Beta-Amyloid zum Ziel erklärt und lasse es mit Antikörpern aus dem Gehirn entfernen. Nehls nennt das „gezielte Selbstzerstörung“. Die EU habe am 15. April 2025 ein erstes Mittel zugelassen; in den USA gebe es solche Mittel seit 2021 [seine Sicht].',
    '📌 Zahlen im Gespräch: rund 30.000 Dollar im Jahr [1:57].',
    '📌 Eine große US-Klinik nenne als Nebenwirkung, dass falsche Überzeugungen nicht mehr durch Fakten zu ändern seien; Nehls deutet das als dauerhafte Beeinflussbarkeit [seine Sicht] [1:57–1:58].',
    '📌 Übersichtsarbeiten von 2022/2023 zeigten laut Nehls: Die Antikörper ließen das Gehirn schrumpfen, Lithium bewirke das Gegenteil [seine Sicht] [1:58–1:59].',
    '🔗 Bisheriger ' + EIN + '.'),
 ab('🌪️ Monoklonale Antikörper und der Zytokinsturm bei Covid [1:59–2:03]', 'g',
    'Der Gastgeber fragt nach Antikörper-Therapien in der Corona-Zeit. Nehls beschreibt den Zytokinsturm als „Armada von Kriegsschiffen“; ein Antikörper gegen einen einzelnen Botenstoff (Interleukin-6) versenke nur eines davon.',
    '📌 Im Herbst 2020 habe eine Zeitung über das Scheitern dieses Ansatzes berichtet; danach sei nur die Impfung geblieben. Nehls meint, man habe ihn „absichtlich versagen lassen“ [seine Sicht] [2:00–2:02].',
    '📌 Mit genug Vitamin D sei ein schwerer Verlauf „praktisch gleich null“; Lithium hätte den Sturm verhindert [seine Sicht] [1:59–2:02].'),
 ab('🧭 Viele Mängel statt eines Mittels: „Medizin der Zukunft“ [2:03–2:06]', 'a',
    'Auf die Frage des Co-Gastgebers nach schweren Fällen kritisiert Nehls, die Medizin behandle meist mit einem einzigen Mittel. Bei bipolarer Störung halte man den Blutspiegel bei etwa 4.000 µg Lithium je Liter; mit 1 mg täglich komme man auf 15 µg.',
    '📌 Behebe man alle Mängel (Omega-3, Vitamin D, Magnesium, B-Vitamine), reiche vermutlich viel weniger Lithium [seine Sicht] [2:04–2:05].',
    '📌 Sein Papier zur „Medizin der Zukunft“ sei ins Englische übersetzt und drei Wochen zuvor Robert F. Kennedy übergeben worden; die EU habe ihn eingeladen [2:05–2:06].'),
 ab('🏭 Carnegie, Rockefeller, Flexner – und Lithium in der Limonade [2:06–2:09]', 'g',
    'Der Gastgeber fragt nach dem Einfluss der Familien Carnegie und Rockefeller. Nehls verweist auf den Flexner-Report, der die Erfahrungsheilkunde verdrängt habe. Früher habe man Menschen zu Quellen geschickt, die sich als lithiumreich erwiesen hätten, und „Lithia Water“ in die Städte gefahren.',
    '📌 7 Up sei 1929 entstanden; die Sieben stehe für Lithium, ein Glas habe 1 mg enthalten. 1949 habe die Rezeptur geändert werden müssen [seine Sicht] [2:07–2:09].',
    '📌 Die WHO habe 1996 geschrieben, wenig Lithium im Trinkwasser gehe mit mehr Einweisungen in die Psychiatrie einher – und zugleich, ein Bedarf des Menschen sei unbekannt [2:08–2:09].'),
 ab('🇺🇸 Robert F. Kennedy: geplatztes Treffen und die „Nagelprobe“ [2:09–2:13]', 'h',
    'Nehls erzählt von seiner US-Reise zum Buch „Das indoktrinierte Gehirn“: einen Tag bei Steve Bannon, dann bei Tucker Carlson in Florida. Ein zugesagtes Treffen mit Kennedy sei schroff abgesagt worden – einen Tag, bevor dieser sich Trump anschloss.',
    '📌 Er warnt davor, alles auf eine Person zu setzen [2:11].',
    '📌 Seine „Nagelprobe“: eine Seite der US-Behörde CDC, auf der empfohlen werde, Säuglingen im ersten Lebensjahr dreimal mRNA zu spritzen. Solange sie bestehe, wisse er nicht, ob Kennedy etwas ausrichten könne [2:12–2:13].',
    '📌 Die CDC nennt er die „Hauptlobbyorganisation für Impfstoffe“ [seine Sicht] [2:12].'),
 ab('🗳️ Gastgeber zu Kennedys und FDA; Nehls: „Scheindemokratie“ [2:13–2:17]', 'h',
    'Der Gastgeber warnt vor einem „falschen Retter“: Die Familie Kennedy habe eine belastete Geschichte, die FDA sei von der Wall Street finanziert, dieselben Leute stünden hinter „Operation Warp Speed“ und förderten den Transhumanismus [seine Sicht].',
    '📌 Nehls: Die USA seien eine „Scheindemokratie“ mit zwei Polen und denselben Geldgebern [seine Sicht] [2:14–2:15].',
    '💬 „ich bin Pessimist, der die Hoffnung nicht aufgibt“ (Nehls) [2:15–2:16]',
    '📌 Sein Schluss: selbst Verantwortung übernehmen, keiner Heilsfigur hinterherlaufen [2:16].'),
 ab('✍️ Schluss: Petition „Salzmarsch“ und Termin in der EU [2:17–2:22]', 'h',
    'Nehls dankt und wirbt für sein Buch (460 Seiten, über 1.000 Studien). Er sei für den 17. Juni eingeladen, in der EU zu sprechen. Grundlage sei eine Petition, die er am 11. April gestartet habe und „Salzmarsch“ nenne – in Anlehnung an Gandhi.',
    '📌 Das Quorum von 30.000 sei nach zwei Wochen erreicht gewesen; die Petition laufe bis 8. Juni [2:19–2:20].',
    '📌 Eine Studie von 2023 beziffere die Kosten des neuen Alzheimer-Mittels in der EU auf 133 Milliarden Euro im Jahr; mit Lithium ließen sich „Billionen“ sparen [seine Sicht] [2:19–2:20].',
    '📌 Eingeladen habe ihn die Opposition im EU-Parlament; das Buch werde für die USA übersetzt [2:21].',
    '📌 Danach folgen Publikumsfragen für Mitglieder, die nicht im Video sind [2:22].'),
]

def span(t):
    m = re.search(r'\[(\d+:\d\d)[–-](\d+:\d\d)\]\s*$', t); return m[1], m[2]
TEILE = []
for b in AB:
    v, bi = span(b['titel'])
    kurz = re.sub(r'\s*\[\d+:\d\d[–-]\d+:\d\d\]\s*$', '', b['titel']); kurz = re.sub(r'^\S+\s', '', kurz)
    TEILE.append({'von': v, 'bis': bi, 't': kurz, 'th': b['th']})
for a, b in zip(TEILE, TEILE[1:]): assert a['bis'] == b['von'], (a, b)

# ---------- Abgleich: links Gespräch (von Hand), rechts Fachstellen (Helfer) ----------
ABG = [
 ('li_essenziell', 'Nehls: Lithium sei ein lebensnotwendiges Spurenelement; sein Buch beweise das mit sechs unabhängigen Argumenten. Ohne Lithium wäre Leben nicht möglich; er hält 1 mg am Tag für nötig [seine Sicht] [0:18, 0:39, 1:08].'),
 ('li_recht', 'Nehls: Lithium sei in Europa als Nahrungsergänzung verboten, obwohl die meisten Europäer einen Mangel hätten [0:18].'),
 ('li_1949', 'Nehls: 1949 habe John Cade die Wirkung bei Manie beschrieben und einen Mangel als Ursache vermutet; im selben Jahr sei Lithium „verboten“ worden, Todesfälle seien der FDA gelegen gekommen. 7 Up (seit 1929) sei nach Lithium benannt, ein Glas habe 1 mg enthalten [seine Sicht] [0:39–0:41, 1:25–1:26, 2:07–2:09].'),
 ('li_trinkwasser', 'Nehls: Seit 1970 zeigten Studien, dass schon etwas mehr Lithium im Trinkwasser mit weniger Kriminalität, Gewalt, Drogenkonsum, Suiziden, Psychiatrie-Einweisungen und Alzheimer einhergehe; er räumt ein, das seien Korrelationen [0:29–0:30, 0:32, 1:33, 2:08].'),
 ('li_therapie', 'Nehls: In der Therapie gebe man 200–400 mg und halte den Blutspiegel bei etwa 4.000 µg/l; 1 mg täglich ergebe 15 µg/l. Hohe Dosen stellten Menschen „still“ [0:39–0:40, 2:04].'),
 ('li_sicherheit', 'Nehls: Zwischen Bedarf und schädlicher Menge liege bei Selen und Zink etwa der Faktor 20, bei Wasser 10, bei Lithium über 85 – Lithium sei „das sicherste Spurenelement“ [seine Sicht] [0:37–0:38].'),
 ('li_alzheimer', 'Nehls: Lithium beuge Alzheimer vor; im Vergleich mit den neuen Antikörpern halte Lithium die Krankheit auf und lasse das Gehirn wachsen [seine Sicht] [1:33, 1:58–1:59].'),
 ('li_autismus', 'Nehls: Autismus entstehe in einer verletzlichen Phase mit anderthalb bis zwei Jahren durch Neuroinflammation und Mängel; ein Kind habe nach ein bis zwei Wochen Lithium (dazu Vitamin D, Omega-3) Blickkontakt aufgenommen [seine Sicht] [0:06–0:13].'),
 ('li_epilepsie_schlaf', 'Nehls: Lithium vertiefe den Schlaf und steuere den Tag-Nacht-Rhythmus; Epilepsie und psychotische Schübe seien entzündlich und mit Lithium beherrschbar [seine Sicht] [1:04–1:05, 1:24–1:25].'),
 ('li_covid', 'Nehls: Bei Covid oder anderen Infekten sei Lithium „das Mittel der Wahl“; es hätte den Zytokinsturm verhindert [seine Sicht] [1:19, 2:02].'),
 ('gsk3', 'Nehls: Ohne Lithium sei das Enzym GSK-3 überaktiv – die Hauptursache aller Zivilisationskrankheiten; die Pharmaindustrie investiere seit 1980 jährlich 10 Mrd. in Stoffe, die wie Lithium wirken [seine Sicht] [1:21–1:23].'),
 ('impf_autismus', 'Nehls: Impfungen lösten Neuroinflammation aus; eine Studie vom Frühjahr 2025 zeige Autismus, Epilepsie, Lernstörungen und ADS in Abhängigkeit von der Zahl der Injektionen; ein Versuch mit Lämmern habe die Ursächlichkeit von Aluminium „im Prinzip bewiesen“. Impfstoffe nennt er „Schadstoffe“ [seine Sicht] [0:08–0:15].'),
 ('impfkalender', 'Nehls: Ein Vierjähriger habe heute „80 Impfungen“; 50 % der Impfstoffe enthielten Aluminium, Formaldehyd teils noch, Quecksilber wohl nicht mehr; die Pockenimpfung sei früher Pflicht gewesen [0:14, 0:17].'),
 ('autismus_zahlen', 'Nehls: Mit der Impfrate sei die Autismus-Rate stark gestiegen [seine Sicht] [0:09].'),
 ('aluminium', 'Nehls: 28 E-Nummern erlaubten Aluminium in Lebensmitteln; für 70 kg gälten in Europa 10 mg täglich als unbedenklich, bei der WHO seit 2011 20 mg; Laugenbrezeln von Alublechen seien aluminiumreich; Aluminium sei giftig für das Gehirn [0:18–0:22].'),
 ('handy', 'Nehls: Funkwellen lösten Neuroinflammation aus; ein Handy am Ohr spüre er „in der ersten Sekunde“; bei Kindern sei die Wirkung stärker [seine Sicht] [0:30–0:32]. Gastgeber: Kribbeln und Aufwachen durch das Handy [0:31, 1:11].'),
 ('hippocampus', 'Nehls: Der Hippocampus reife bis etwa zwei Jahre (daher keine frühen Erinnerungen), könne lebenslang wachsen und schrumpfe unter Stress; bei posttraumatischer Belastungsstörung sei er am kleinsten; bei Rechtshändern sei der linke entscheidend [seine Sicht] [0:06–0:07, 0:25–0:26, 0:42].'),
 ('schlaf', 'Nehls: Im Tiefschlaf werde der Tagesinhalt des Hippocampus in die Großhirnrinde übertragen, im REM-Schlaf verknüpft; Beta-Amyloid werde im Tiefschlaf ausgewaschen; Schlafentzug führe zu Wahnbildern [0:45–0:48, 0:55–0:56, 1:55].'),
 ('schizo', 'Nehls: Schizophrenie sei eine „geteilte Seele“; man wechsle womöglich zwischen zwei Personen. Gastgeber: Das Schlimmste seien dann multiple Persönlichkeiten – Nehls: „Genau“ [0:41].'),
 ('amyloid_ak', 'Nehls: Die EU habe am 15.04.2025 einen Antikörper gegen Beta-Amyloid zugelassen (USA seit 2021; rund 30.000 $ im Jahr). Die Mittel beschleunigten Alzheimer und ließen das Gehirn schrumpfen; eine US-Klinik nenne unbeirrbare falsche Überzeugungen als Nebenwirkung; laut einer Studie von 2023 koste das die EU 133 Mrd. € im Jahr [seine Sicht] [1:56–1:59, 2:19–2:20].'),
 ('zytokin', 'Nehls: Der Antikörper gegen Interleukin-6 sei 2020 bei Covid gescheitert – man habe ihn „absichtlich versagen lassen“; mit einem Vitamin-D-Spiegel wie bei Naturvölkern sei ein schwerer Verlauf „praktisch gleich null“ [seine Sicht] [1:09, 1:59–2:02].'),
 ('omega3', 'Nehls: Die Hälfte der Fettsäuren in den Synapsen sei die Omega-3-Fettsäure DHA; im Gehirn von Fischen sei der Lithiumgehalt 20-mal höher als im Muskel [1:14–1:16].'),
 ('evolution', 'Nehls: Schon die Urzelle LUCA (vor 4,2 Mrd. Jahren) sei durch Lithium reguliert gewesen; der moderne Mensch sei am Pinnacle Point in Südafrika entstanden (Welterbe 2024, Funde bis 160.000 Jahre), alle 1.300 Ethnien stammten von dort; der Spitz sei vor 5.000 Jahren noch Wolf gewesen; Kohl stamme von einer rapsähnlichen Pflanze [1:16–1:18, 1:29–1:30, 1:34–1:37].'),
 ('genom', 'Nehls: Er habe das „Nacktmaus-Gen“ entdeckt; der Mensch habe rund 19.500 Gene, ein kleiner Wurm 19.000; Mais habe ein zehnmal größeres Erbgut; Stress der Mutter präge das Kind epigenetisch [1:27, 1:49–1:52].'),
 ('intelligenz', 'Gastgeber fragt, ob Intelligenz großteils vererbt sei. Nehls: Alle Menschen hätten das gleiche Potenzial; IQ-Tests seien kulturell geprägt; der Flynn-Effekt komme vom Üben auf die Tests; die Genetik habe aber „mit Sicherheit was damit zu tun“ [1:44–1:48].'),
 ('sprache', 'Gastgeber: Es habe eine gemeinsame Ursprache gegeben; Mutter/mother/madre/mādar seien ein Wort; Koreanisch und Türkisch seien sich sehr nah. Nehls stimmt zu und nennt die indogermanischen Sprachen [1:39–1:43].'),
 ('mkultra', 'Gastgeber: Das CIA-Programm MK-Ultra habe mit Elektroschocks, LSD und Folter gespaltene Persönlichkeiten und Attentäter erzeugt (er nennt Kevin Shipp) [seine Sicht] [0:43–0:44].'),
 ('raam', 'Nehls: Beim Race Across America sei er zweimal gestartet (Platz 5 und 6), mit acht Stunden Schlaf je Nacht; eine Universität habe ihn dabei untersucht. Jure Robič habe fünfmal gewonnen und sei später tödlich verunglückt [0:55–1:02].'),
 ('icforum', 'Nehls: Am 12.04.2024 habe er beim IC Forum in Basel vor 1.500 Delegierten aus über 100 Staaten den Hauptvortrag zum Thema Frieden gehalten [0:26–0:28].'),
 ('rfk', 'Nehls: Ein Treffen mit Robert F. Kennedy sei kurz vor dessen Anschluss an Trump abgesagt worden; die CDC empfehle, Säuglingen im ersten Jahr dreimal mRNA zu spritzen – das sei seine „Nagelprobe“. Gastgeber: Die FDA sei von der Wall Street finanziert und stehe hinter „Operation Warp Speed“ [seine Sicht] [2:09–2:14].'),
 ('flexner', 'Nehls: Carnegie- und Rockefeller-Stiftung hätten mit dem Flexner-Report die Erfahrungsheilkunde verdrängt [seine Sicht] [2:06–2:07].'),
 ('petition', 'Nehls: Seine Petition („Salzmarsch“), gestartet am 11.04.2025, habe das Quorum von 30.000 nach zwei Wochen erreicht; am 17.06.2025 spreche er auf Einladung der Opposition im EU-Parlament [2:18–2:21].'),
 ('vitd', 'Gastgeber: Er habe zeitweise 30.000 Einheiten Vitamin D täglich genommen und nichts gespürt [1:07].'),
 ('buch', 'Nehls: Das Buch sei „Spiegel-Bestseller“-Autor-Werk, unter den ersten 40 bei Amazon, die erste Auflage vergriffen; 460 Seiten, über 1.000 Studien [0:03, 2:17].'),
]
ZUSATZ = {
 'li_trinkwasser': ' ' + HILFE,
 'li_therapie': ' Lithium als Arznei gehört in ärztliche Hand; Fragen dazu bitte an Ärztin oder Arzt.',
 'impf_autismus': ' Bei Fragen zu Impfungen: Kinderärztin oder Kinderarzt; Verdachtsfälle von Nebenwirkungen lassen sich unter [nebenwirkungen.bund.de](https://nebenwirkungen.bund.de) melden.',
}
abg_zeilen = []
for k, aussage in ABG:
    z = FZ.get(k)
    if z: abg_zeilen.append([aussage, z['fakt'] + ZUSATZ.get(k, ''), z.get('quelle') or '❓'])
    else: abg_zeilen.append([aussage, '❓ Dazu liegt hier keine geprüfte Quelle vor.' + ZUSATZ.get(k, ''), '❓'])

# ---------- Zeitachse ----------
ZA = [
 {'z': 'vor 4,2 Mrd. Jahren', 'j': -4200000000, 't': 'LUCA, der letzte gemeinsame Vorfahr allen Lebens – laut Nehls schon durch Lithium reguliert.', 'f': '[1:17, 1:30]', 'e': False},
 {'z': 'vor rund 160.000 Jahren', 'j': -160000, 't': 'Älteste Funde am Pinnacle Point (Südafrika), Nehls’ „Garten Eden“.', 'f': '[1:36]', 'e': False},
 {'z': 'vor rund 10.000 Jahren', 'j': -8000, 't': 'Kohlsorten entstehen laut Nehls aus einer rapsähnlichen Pflanze.', 'f': '[1:30]', 'e': False},
 {'z': 'vor rund 5.000 Jahren', 'j': -3000, 't': 'Der Vorfahr des Spitzes sei noch Wolf gewesen (Nehls).', 'f': '[1:29]', 'e': False},
 {'z': 'Ende 19. Jh.', 'j': 1890, 't': '„Lithia Water“ wird in Städte wie New York gefahren.', 'f': '[2:07]', 'e': False},
 {'z': '1910', 'j': 1910, 't': 'Flexner-Report (im Gespräch ohne Jahr genannt).', 'f': '[2:06]', 'e': True},
 {'z': '1929', 'j': 1929, 't': 'Die Limonade 7 Up entsteht – laut Nehls mit Lithium.', 'f': '[2:07]', 'e': False},
 {'z': '1949', 'j': 1949, 't': 'John Cade beschreibt Lithium bei Manie; laut Nehls wird Lithium im selben Jahr „verboten“.', 'f': '[0:39, 1:25]', 'e': False},
 {'z': '1960er/70er', 'j': 1965, 't': 'MK-Ultra (Zeitangabe des Gastgebers).', 'f': '[0:43]', 'e': False},
 {'z': 'ab 1970', 'j': 1970, 't': 'Erste Studien zu Lithium im Trinkwasser (Nehls).', 'f': '[0:29]', 'e': False},
 {'z': 'Ende 1970er', 'j': 1978, 't': 'Nehls erinnert sich an seine Pockenimpfung.', 'f': '[0:17]', 'e': False},
 {'z': '1980', 'j': 1980, 't': 'Entdeckung von GSK-3; seither Forschung der Industrie (Nehls).', 'f': '[1:22]', 'e': False},
 {'z': '1996', 'j': 1996, 't': 'WHO-Veröffentlichung zu Lithium im Trinkwasser und Psychiatrie-Einweisungen (Nehls).', 'f': '[2:08]', 'e': False},
 {'z': '2000er', 'j': 2008, 't': 'Nehls fährt zweimal das Race Across America; Sieger ist beide Male Jure Robič.', 'f': '[0:55–1:02]', 'e': False},
 {'z': '2011', 'j': 2011, 't': 'WHO erhöht laut Nehls den Richtwert für Aluminium.', 'f': '[0:19]', 'e': False},
 {'z': '2015', 'j': 2015, 't': 'Nehls veröffentlicht „Die Algenöl-Revolution“.', 'f': '[1:15]', 'e': False},
 {'z': 'um 2017/18', 'j': 2018, 't': 'Nehls beginnt, täglich Lithium zu nehmen („seit 7, 8 Jahren“).', 'f': '[1:33]', 'e': False},
 {'z': 'Herbst 2020', 'j': 2020, 't': 'Zeitungsbericht über das Scheitern eines Antikörpers gegen Interleukin-6 bei Covid (Nehls).', 'f': '[2:00]', 'e': False},
 {'z': '2021', 'j': 2021, 't': 'Erste Zulassung eines Amyloid-Antikörpers in den USA (Nehls).', 'f': '[1:57]', 'e': False},
 {'z': '2023', 'j': 2023, 't': 'Studie zu den Kosten der Antikörper-Therapie in der EU (Nehls: 133 Mrd. € im Jahr).', 'f': '[2:19]', 'e': False},
 {'z': '12.04.2024', 'j': 2024, 't': 'Hauptvortrag beim IC Forum in Basel (Nehls).', 'f': '[0:26]', 'e': False},
 {'z': '2024', 'j': 2024, 't': 'Pinnacle Point wird Welterbe; LUCA-Studie erscheint; US-Reise mit Bannon und Carlson, Absage Kennedys.', 'f': '[1:15, 1:18, 2:09–2:11]', 'e': False},
 {'z': 'März 2025', 'j': 2025, 't': 'Studie zu Impfungen und Entwicklungsstörungen, auf die sich Nehls beruft.', 'f': '[0:09]', 'e': False},
 {'z': '11.04.2025', 'j': 2025, 't': 'Start der Petition „Salzmarsch“.', 'f': '[2:19]', 'e': False},
 {'z': '15.04.2025', 'j': 2025, 't': 'EU-Zulassung eines Amyloid-Antikörpers (laut Nehls in den Tagesthemen).', 'f': '[1:56, 1:58]', 'e': False},
 {'z': '01.05.2025', 'j': 2025, 't': 'Aufnahme des Gesprächs („mitten im ersten Mai“).', 'f': '[0:01]', 'e': False},
 {'z': '08.06.2025', 'j': 2025, 't': 'Ende der Zeichnungsfrist der Petition (Ankündigung).', 'f': '[2:20]', 'e': False},
 {'z': '17.06.2025', 'j': 2025, 't': 'Angekündigter Termin im EU-Parlament.', 'f': '[2:18]', 'e': False},
]
_hz = {e['z'] for e in FA.get('zeitachse', [])}
ZA = [e for e in ZA if not (e['e'] and e['z'] in _hz)]
for e in FA.get('zeitachse', []):
    e = dict(e); e['e'] = True; e.setdefault('f', ''); ZA.append(e)
ZA.sort(key=lambda e: (e.get('j', -10**12)))

PERS = [
 ['Michael Nehls', 'Arzt, Molekulargenetiker, Autor', 'Gast', '[0:00]'],
 ['Gastgeber und Co-Gastgeber', 'Moderatoren von REALTALK MEDIA; Namen nicht belegt ❓', 'stellen Fragen, bringen eigene Erfahrungen ein', '[0:00]'],
 ['Jasmin Kosubek', 'Journalistin', 'führte kurz zuvor ein Gespräch mit Nehls', '[0:01]'],
 ['Kinderarzt aus Potsdam', 'Name im Untertitel unsicher ❓', 'berichtet Nehls von Kindern, die Lithium erhalten', '[0:04, 1:10, 1:25]'],
 ['Daniele Ganser', 'Historiker und Friedensforscher', 'Nehls will mit ihm über Friedensfähigkeit sprechen', '[0:23]'],
 ['John Cade', 'australischer Psychiater (im Untertitel „Ces“, „Kate“)', 'beschrieb 1949 Lithium bei Manie', '[0:39, 1:25]'],
 ['Jure Robič', 'slowenischer Radsportler, fünfmaliger Sieger', 'Beispiel für Wahnbilder durch Schlafentzug', '[0:56–0:58, 1:02]'],
 ['Jonas Deichmann', 'Extremsportler', 'vom Gastgeber erwähnt', '[1:02]'],
 ['Kevin Shipp', 'früherer CIA-Mitarbeiter (im Untertitel „Chip“)', 'vom Gastgeber zu MK-Ultra genannt', '[0:44]'],
 ['Robert F. Kennedy Jr.', 'US-Gesundheitsminister', 'geplatztes Treffen; „Nagelprobe“', '[0:17, 2:05, 2:09–2:13]'],
 ['Donald Trump', 'US-Präsident', 'im Zusammenhang mit Kennedy und Bannon', '[2:09–2:10]'],
 ['Tucker Carlson, Steve Bannon', 'US-Moderatoren', 'Gastgeber von Nehls auf seiner US-Reise', '[2:09]'],
 ['John F. Kennedy', 'US-Präsident 1961–1963', 'Nehls zitiert im Buch eine Rede', '[2:11]'],
 ['James Flynn', 'Intelligenzforscher', 'Namensgeber des Flynn-Effekts', '[1:45]'],
 ['Mahatma Gandhi', 'Anführer der indischen Unabhängigkeitsbewegung', 'Vorbild für den Namen „Salzmarsch“', '[2:18]'],
 ['Ursula von der Leyen', 'Präsidentin der EU-Kommission', 'habe ihn nicht eingeladen (Nehls)', '[2:21]'],
 ['Johnny', 'Nehls’ Hund, ein Spitz', 'Beispiel für Evolution; ihm ist ein Buch gewidmet', '[1:29, 1:38]'],
]
ORTE = [
 ['Berlin', 'Aufnahmeort am 1. Mai', '[0:01]'],
 ['Potsdam', 'Praxis des genannten Kinderarztes', '[0:04]'],
 ['Basel', 'IC Forum 2024; Sitz großer Pharmafirmen', '[0:26, 1:23]'],
 ['Pinnacle Point, Mossel Bay (Südafrika)', 'Fundstätte, Nehls’ „Garten Eden“', '[1:36]'],
 ['USA', 'Race Across America; Reise 2024; Zulassungen', '[0:55, 2:09]'],
 ['Florida', 'Gespräch mit Tucker Carlson', '[2:09–2:10]'],
 ['Slowenien', 'Heimat von Jure Robič', '[0:56]'],
 ['Alpen', 'Beispiel für Jodmangel', '[0:11]'],
 ['Iran', 'Fischhirn als Speise (Gastgeber)', '[1:16]'],
 ['Brüssel/Straßburg, EU-Parlament', 'angekündigter Termin am 17. Juni', '[2:18]'],
 ['Beringstraße', 'Weg nach Amerika', '[1:44]'],
]
BEGR = [
 ['Hippocampus', 'Hirnstruktur für neue Erinnerungen; bei Nehls „autobiografische Gedächtniszentrale“', '[0:06]'],
 ['Mentales Immunsystem', 'Nehls’ Begriff für die seelische Widerstandskraft, die er im Hippocampus verortet', '[0:23]'],
 ['Neuroinflammation', 'Entzündungsvorgänge im Gehirn', '[0:07]'],
 ['Gesetz des Minimums / Maximums', 'Nehls’ „Grundgesetze des Lebens“: Nichts darf fehlen, nichts zu viel sein', '[0:16]'],
 ['Essenziell', 'lebensnotwendig und von außen zuzuführen', '[0:18]'],
 ['Homöostase', 'Selbstregulation, inneres Gleichgewicht', '[1:05, 1:20]'],
 ['GSK-3', 'Enzym (Glykogensynthase-Kinase 3), das Lithium hemmt', '[1:21]'],
 ['Autophagie', 'Recycling von Zellbestandteilen', '[1:18]'],
 ['LUCA', 'Last Universal Common Ancestor – letzter gemeinsamer Vorfahr allen Lebens', '[1:17]'],
 ['Tiefschlaf / REM-Schlaf', 'Schlafphasen; bei Nehls „Upload“ und Verknüpfung', '[0:46]'],
 ['Beta-Amyloid', 'Eiweißbruchstück, das sich bei Alzheimer ablagert', '[1:53]'],
 ['Monoklonaler Antikörper', 'im Labor hergestellter, einheitlicher Antikörper (Endung „-mab“)', '[1:59]'],
 ['Zytokinsturm', 'überschießende Ausschüttung von Botenstoffen des Immunsystems', '[1:09, 2:00]'],
 ['Epigenetik', 'chemische Markierungen am Erbgut, die das Ablesen der Gene steuern', '[1:51]'],
 ['Flynn-Effekt', 'Anstieg der Ergebnisse in IQ-Tests über Jahrzehnte', '[1:45]'],
 ['Omega-3-Index', 'Anteil von EPA und DHA in Zellmembranen', '[1:14]'],
 ['Flexner-Report', 'Gutachten zur Ärzteausbildung in den USA', '[2:06]'],
 ['MK-Ultra', 'CIA-Programm zu Bewusstseinskontrolle', '[0:43]'],
]
ZAHL = [
 ['Studien im Buch', 'über 1.000; 460 Seiten', '[0:05, 2:17]'],
 ['Lithium täglich nach Nehls', '1 mg', '[0:39]'],
 ['Lithium in der Therapie', '200–400 mg; Blutspiegel etwa 4.000 µg/l gegenüber 15 µg/l', '[0:39, 2:04]'],
 ['Abstand Bedarf – schädliche Menge', 'Selen/Zink 20, Wasser 10, Lithium über 85', '[0:37–0:38]'],
 ['Aluminium als unbedenklich', '10 mg (EU) bzw. 20 mg (WHO) täglich bei 70 kg', '[0:19]'],
 ['E-Nummern mit Aluminium', '28', '[0:18]'],
 ['Impfungen bis zum 4. Lebensjahr', '„80“', '[0:17]'],
 ['Impfstoffe mit Aluminium', '50 %', '[0:14]'],
 ['IC Forum Basel', '1.500 Delegierte, über 100 Staaten, 15 Minuten Vortrag', '[0:26–0:27]'],
 ['Race Across America', '4.800 km; Nehls: 8 Std. Schlaf je Nacht, Platz 5 und 6; erste Etappe 880 km', '[0:55–1:04]'],
 ['Fischhirn', '20-mal mehr Lithium als Muskelfleisch', '[1:16]'],
 ['DHA in Synapsen', '50 % der Fettsäuren', '[1:14]'],
 ['Forschung zu GSK-3', '10 Mrd. jährlich seit 1980', '[1:22]'],
 ['Pinnacle Point', 'Funde bis 160.000 Jahre; 1–2 mg Lithium täglich aus Muscheln', '[1:36–1:37]'],
 ['Ethnien', 'rund 1.300', '[1:34]'],
 ['Erbgut', '3.000 Bücher zu 1.000 Seiten zu 1.000 Buchstaben; 19.500 Gene', '[1:49–1:50]'],
 ['Antikörper-Therapie', 'rund 30.000 $ im Jahr; 133 Mrd. € im Jahr für die EU', '[1:57, 2:19]'],
 ['Petition', 'Quorum 30.000 nach zwei Wochen', '[2:19–2:20]'],
 ['Vitamin D beim Gastgeber', 'zeitweise 30.000 Einheiten täglich', '[1:07]'],
]

KERN = [
 ['1', 'Lithium ist ein lebensnotwendiges Spurenelement, und die meisten Europäer haben zu wenig.', 'Sechs Argumente im Buch; Trinkwasser-Studien; 1 mg täglich als Bedarf.', '[0:18, 0:29, 0:39]', '★★★'],
 ['2', 'Der Hippocampus ist das „mentale Immunsystem“ – von ihm hängen Empathie und Friedensfähigkeit ab.', 'Er speichert Erfahrungen mit anderen; Stress, Gifte und Mängel lassen ihn schrumpfen.', '[0:22–0:28]', '★★★'],
 ['3', 'Aluminium und Impfungen in den ersten Lebensjahren fördern Autismus; Lithium wirkt dagegen.', 'Studie vom Frühjahr 2025, Lämmer-Versuch, Fallbeispiel eines Kinderarztes.', '[0:06–0:17]', '★★★'],
 ['4', 'Lithium ist verboten, Aluminium erlaubt – das ist verkehrt herum.', '28 E-Nummern, 10–20 mg Aluminium täglich als unbedenklich; 1 mg Lithium nicht erhältlich.', '[0:18–0:22]', '★★'],
 ['5', 'Schlaf ist der „Upload“ des Gedächtnisses; Schlafentzug macht Wahnbilder.', 'Tiefschlaf überträgt, REM verknüpft; Race Across America als Beleg aus eigener Erfahrung.', '[0:45–1:02]', '★★★'],
 ['6', 'Überaktives GSK-3 durch Lithiummangel ist die Wurzel der Zivilisationskrankheiten.', 'Die Industrie suche patentierbare Stoffe, die wie Lithium wirken.', '[1:19–1:24]', '★★'],
 ['7', 'Alle Menschen stammen von einer Gruppe in Südafrika ab und haben das gleiche Potenzial.', 'Pinnacle Point, Lithium aus Muscheln; IQ-Tests messen Kultur.', '[1:34–1:49]', '★★★'],
 ['8', 'Antikörper gegen Beta-Amyloid schaden mehr, als sie nützen.', 'Beta-Amyloid habe eine Aufgabe; die Mittel ließen das Gehirn schrumpfen und kosteten Milliarden.', '[1:53–1:59, 2:19]', '★★'],
 ['9', 'Medizin sollte alle Mängel beheben statt ein einzelnes Mittel zu geben.', '„Medizin der Zukunft“; Kritik am Vorgehen bei Covid und bipolarer Störung.', '[1:59–2:06]', '★★'],
 ['10', 'Keiner Heilsfigur folgen – selbst Verantwortung übernehmen.', 'Erfahrung mit Kennedy; „Nagelprobe“ CDC-Seite; Petition und Termin in der EU.', '[2:09–2:21]', '★★'],
]

BAUM = {'typ': 'baum', 'titel': '🌳 Themenbaum des Gesprächs', 'wurzel': 'Michael Nehls bei REALTALK: Lithium, Gehirn, Evolution und Politik',
 'unter': 'Michael Nehls · REALTALK MEDIA · %s · %s' % (DATUM, DAUER),
 'knoten': [
  {'t': '💊 Lithium & Buch', 'k': [{'t': 'Neues Buch, Kinderarzt [0:03]'}, {'t': 'Verboten gegenüber erlaubt [0:18]'}, {'t': 'Trinkwasser-Studien [0:29]'}, {'t': 'Kleine und große Mengen [0:34]'}, {'t': 'John Cade 1949 [0:39]'}, {'t': '„Ich merke nichts“ [1:06]'}]},
  {'t': '💉 Impfungen, Aluminium, Autismus', 'k': [{'t': 'Autismus und Reifung [0:06]'}, {'t': 'Studie 2025 [0:08]'}, {'t': 'Lämmer-Versuch [0:14]'}, {'t': '„80 Impfungen“ [0:17]'}, {'t': 'Aluminium im Essen [0:19]'}]},
  {'t': '🧠 Hippocampus, Schlaf, Träume', 'k': [{'t': 'Mentales Immunsystem [0:22]'}, {'t': 'Trauma und Stress [0:24]'}, {'t': 'Handystrahlen [0:30]'}, {'t': 'Schlaf als Upload [0:45]'}, {'t': 'Klarträume [0:48]'}]},
  {'t': '🚴 Race Across America', 'k': [{'t': 'Schlafentzug, Robič [0:55]'}, {'t': 'Acht Stunden Schlaf [0:59]'}, {'t': 'Sekundenschlaf [1:03]'}]},
  {'t': '🧬 Evolution, Gene, Glaube', 'k': [{'t': 'Fischer und Sammler, LUCA [1:15]'}, {'t': 'Nacktmaus-Gen [1:26]'}, {'t': 'Hund, Kohl, Schöpfer [1:28]'}, {'t': 'Bücher und Demut [1:31]'}, {'t': 'Erbgut als Bibliothek [1:49]'}, {'t': 'Transhumanismus [1:51]'}]},
  {'t': '🌍 Herkunft, Sprache, Intelligenz', 'k': [{'t': 'Pinnacle Point [1:34]'}, {'t': 'Babel und „Mutter“ [1:39]'}, {'t': 'IQ und Flynn-Effekt [1:44]'}]},
  {'t': '🏭 Alzheimer-Mittel & Pharma', 'k': [{'t': 'GSK-3 [1:19]'}, {'t': 'Beta-Amyloid [1:53]'}, {'t': 'Antikörper [1:56]'}, {'t': 'Zytokinsturm [1:59]'}, {'t': 'Flexner, 7 Up [2:06]'}]},
  {'t': '🏛️ Politik: RFK, USA, EU', 'k': [{'t': 'IC Forum Basel [0:26]'}, {'t': 'Kennedy und die Nagelprobe [2:09]'}, {'t': '„Scheindemokratie“ [2:14]'}, {'t': 'Petition, EU-Termin [2:17]'}]},
 ]}

folge = {'typ': 'folge', 'k': K, 'titel': TITEL, 'gast': 'Michael Nehls',
 'rolle': 'Arzt, Molekulargenetiker, Sachbuchautor',
 'kanal': 'REALTALK MEDIA', 'datum': DATUM, 'dauer': DAUER, 'url': URL,
 'thema': 'Zweites REALTALK-Gespräch mit Michael Nehls: sein Lithium-Buch, Autismus und Impfungen aus seiner Sicht, Hippocampus, Schlaf und Träume, das Race Across America, Evolution und Glaube, Intelligenz, Alzheimer-Antikörper sowie Robert F. Kennedy und eine Petition an die EU.',
 'kacheln': []}

R1 = {'id': K, 'titel': G + ': Überblick', 'bloecke': [
 folge,
 {'typ': 'hinweis', 'text': 'Auswertung nach dem Transkript (automatische Untertitel): Gesagtes ohne Zeichen, Ergänzungen 📚, Unklares ❓. Fundstellen [Stunde:Minute] springen ins Video. **Gesundheitsthema:** Aussagen zu Lithium, Impfungen, Autismus und Arzneien stehen als „[seine Sicht]“; im Reiter „Abgleich & Daten“ steht daneben der Stand der Fachstellen (PEI, RKI/STIKO, EMA, BfR, EFSA u. a.). Das ist keine medizinische Beratung und keine Empfehlung – Lithium ist in höheren Mengen ein Arzneimittel; bei Fragen zu Impfungen, Arzneien oder Nahrungsergänzung bitte Ärztin oder Arzt fragen. Die Bewertung bleibt dem Leser.'},
 {'typ': 'abschnitt', 'titel': '⚡ In Kürze', 'liste': [
  'Zweites Gespräch von REALTALK MEDIA mit Michael Nehls, aufgenommen am 1. Mai 2025; Anlass ist sein neues Buch „Das Lithium-Komplott“.',
  'Nehls hält Lithium für lebensnotwendig und einen Mangel für weit verbreitet; er verbindet ihn mit Autismus, Depression, Gewalt, Alzheimer und vielen Volkskrankheiten [seine Sicht].',
  'Impfungen und Aluminium in den ersten Lebensjahren sieht er als Auslöser von Entzündungen im Gehirn [seine Sicht]; die Fachstellen sehen das anders (siehe Abgleich).',
  'Ausführlich erklärt er sein Bild vom Hippocampus, vom Schlaf als „Upload“ und von Träumen – und erzählt vom Race Across America mit acht Stunden Schlaf je Nacht.',
  'Der Gastgeber widerspricht an einer Stelle aus eigener Erfahrung: Er habe von Lithium, Vitamin D und Magnesium nichts gemerkt.',
  'Es folgen Evolution und Glaube, die Herkunft des Menschen in Südafrika, Sprache und Intelligenz: Alle Menschen hätten das gleiche Potenzial.',
  'Nehls kritisiert Antikörper gegen Beta-Amyloid und die Pharmaindustrie und berichtet von einem geplatzten Treffen mit Robert F. Kennedy.',
  'Am Ende wirbt er für eine Petition und einen Termin im EU-Parlament am 17. Juni 2025.']},
 {'typ': 'abschnitt', 'titel': '🔦 Aus Nehls’ Sicht – der rote Faden', 'liste': [
  '[seine Sicht] Das Gehirn des Menschen entstand unter Bedingungen, in denen nichts Wichtiges fehlte – auch Lithium nicht. Heute fehlt es, während Schadstoffe wie Aluminium zunehmen.',
  '[seine Sicht] Am empfindlichsten ist der Hippocampus, das „mentale Immunsystem“. Entzündungen und Mängel schwächen ihn; darunter leiden Denken, Belastbarkeit und Mitgefühl – bis hin zur Friedensfähigkeit einer Gesellschaft.',
  '[seine Sicht] Lithium hält über das Enzym GSK-3 viele Vorgänge im Gleichgewicht. Ein Mangel steht deshalb hinter vielen Krankheiten, und kleine Mengen genügen, um ihn zu beheben.',
  '[seine Sicht] Die Medizin setzt auf einzelne, patentierbare Mittel statt auf das Beheben aller Mängel; Behörden und Industrie haben kein Interesse an einem billigen Naturstoff.',
  '[seine Sicht] Alle Menschen haben denselben Ursprung und dasselbe Potenzial; es kommt darauf an, ihm die „Grundgesetze des Lebens“ zu erfüllen.',
  '[seine Sicht] Ändern wird sich das nicht durch eine Heilsfigur, sondern wenn Einzelne Verantwortung übernehmen – daher Buch, Petition und Auftritt in der EU. Was Fachstellen dazu sagen, steht unter „Abgleich & Daten“.']},
 {'typ': 'text', 'text': '🎯 **Kernaussagen** – die zehn wichtigsten Thesen des Gesprächs:'},
 {'typ': 'tabelle', 'kopf': ['#', 'Aussage', 'Begründung im Gespräch', 'Fundstelle', 'Gewicht'], 'zeilen': KERN},
 BAUM,
 {'typ': 'illu', 'id': 'realtalk25_gedaechtnis', 'titel': 'Skizze: Vom Zwischenspeicher zur Großhirnrinde – Schlaf und Gedächtnis (Darstellung laut Nehls, schematisch)'},
 {'typ': 'illu', 'id': 'realtalk25_lithium', 'titel': 'Skizze: Lithium – Größenordnungen (belegte Daten)'},
 {'typ': 'tabelle', 'kopf': ['🧭 Steckbrief', ''], 'schmal': True, 'zeilen': [
  ['Thema in einem Satz', 'Nehls über Lithium, Gehirn und Schlaf, Evolution, Intelligenz, Alzheimer-Mittel und US-Gesundheitspolitik.'],
  ['Titel', TITEL],
  ['Format', 'Studiogespräch zu dritt; eine Werbe-Einblendung (Glutamin-Produkt); Publikumsfragen danach nur für Mitglieder'],
  ['Sprecher', 'Michael Nehls; Gastgeber und Co-Gastgeber von REALTALK MEDIA (Namen nicht belegt ❓)'],
  ['Dauer', DAUER],
  ['Datum', DATUM + ' – aufgenommen am 1. Mai 2025 (Bezüge im Gespräch)'],
  ['Grundton', 'begeistert und überzeugt bei Nehls; die Gastgeber fragen als Laien nach, steuern Persönliches bei und widersprechen vereinzelt'],
  ['Hinweis', 'Kanal: ' + RTK + '. Gesundheitsaussagen sind Nehls’ Sicht; Stand der Fachstellen im Abgleich. Frühere Auswertungen: Reiter „Videos“ und „Abgleich“.'],
 ]},
]}

R2 = {'id': K + 'ab', 'titel': G + ': Gespräch im Detail', 'bloecke': [
 {'typ': 'text', 'text': '%d Abschnitte in der Reihenfolge des Videos. Lesehilfe: 💬 Zitat, 📌 Aussage, 🔗 Bezug, 📚 Ergänzung, ❓ unklar. Aussagen zu Gesundheit sind die Sicht der Sprechenden; der Stand der Fachstellen steht im Reiter „Abgleich & Daten“.' % len(AB)},
 {'typ': 'gespraech', 'titel': '🧭 Gesprächsverlauf – wann worüber gesprochen wird', 'dauer': '2:22', 'themen': THEMEN, 'teile': TEILE},
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
 {'typ': 'text', 'text': 'Neutraler Abgleich: links die Aussage im Gespräch, rechts die gängige Darstellung bzw. Daten mit Quelle. Die Bewertung bleibt dem Leser. Keine medizinische Beratung und keine Empfehlung. ' + HILFE},
 {'typ': 'tabelle', 'kopf': ['Aussage im Gespräch', 'Gängige Darstellung (Mainstream) / Daten 📚', 'Quelle'], 'stapel': True, 'zeilen': abg_zeilen},
 {'typ': 'abschnitt', 'titel': '🧩 Spannungen im Gespräch', 'liste': [
  'Der Gastgeber wünscht sich ein Streitgespräch mit einer Fachkraft, die Nehls’ These kritisch sieht [0:05]; Nehls rechnet nicht damit und sagt, keine Studie widerspreche ihm.',
  'Der Gastgeber hat Lithium, Vitamin D und Magnesium selbst ausprobiert und nichts gespürt [1:06]; Nehls deutet das als Zeichen, dass kein Mangel bestand.',
  'Der Gastgeber fragt, ob Lithium nur abstumpfe [0:34]; Nehls trennt Spurenmengen von Arzneidosen.',
  'Nehls nennt die Trinkwasser-Studien selbst Korrelationen [0:32] und zugleich die Ursächlichkeit durch sein Buch belegt.',
  'Der Co-Gastgeber fragt zweimal nach Hilfe bei schweren psychotischen Schüben [1:24, 2:03]; Nehls antwortet allgemein mit Entzündung und Mängeln.',
  'Zur Vererbung von Intelligenz sagt Nehls, alle hätten das gleiche Potenzial – und dass die Genetik „mit Sicherheit was damit zu tun“ habe [1:44–1:48].',
  'Der Gastgeber warnt vor Kennedy als „falschem Retter“ [2:13]; Nehls teilt die Vorsicht, hofft aber weiter.',
  'Im Gespräch über Mängel und Präparate läuft eine Werbe-Einblendung für ein Nahrungsergänzungsmittel [1:12].']},
 {'typ': 'abschnitt', 'titel': '💡 Was man mitnehmen kann', 'liste': [
  'Welche von Nehls’ Aussagen Studien stützen, wo nur Zusammenhänge vorliegen und wo Fachstellen widersprechen, zeigt die Tabelle Zeile für Zeile.',
  'Schlaf, Bewegung und Ernährung als Grundlage geistiger Gesundheit sind auch in der Fachwelt anerkannt; strittig sind Umfang und einzelne Stoffe.',
  'Zwischen Spurenmengen und Arzneidosen von Lithium liegen Größenordnungen (siehe Skizze); Arzneidosen brauchen ärztliche Überwachung.',
  'Zu Impfungen im Kindesalter berät die Kinderarztpraxis; maßgeblich sind die Empfehlungen der STIKO.']},
 {'typ': 'abschnitt', 'titel': '❓ Offen', 'liste': [
  'Namen der beiden Gastgeber; genaues Veröffentlichungsdatum (soweit oben mit ❓).',
  'Die Fallberichte des Kinderarztes sind nur aus Nehls’ Erzählung bekannt.',
  'Angaben, die sich nur auf Nehls’ Buch stützen (z. B. Lithium und LUCA, Lithium im linken Hippocampus), wurden hier nicht am Buch geprüft.',
  'Nehls’ Platzierungen beim Race Across America: siehe Abgleich (im Steckbrief des Eintrags stand bisher eine andere Angabe).']},
 {'typ': 'abschnitt', 'titel': '🔎 Weiter recherchieren', 'liste': [
  'Stoff-Tafel ' + BLI + ' und ' + BOM + '.',
  'Zahlen zu ' + WDE + ' und ' + WSU + '.',
  'Bisheriger ' + EIN + ' und die Reiter „Kernideen“ und „Videos“ dieses Eintrags.',
  'Stellungnahmen von BfR und EFSA zu Aluminium und zu Lithium in Nahrungsergänzungsmitteln (Links in der Tabelle).']},
]}

quellen = [['Video: ' + TITEL + ' – REALTALK MEDIA (YouTube)', URL]] + [list(q) for q in FA.get('quellen', [])]
for z in abg_zeilen:
    for t, u in re.findall(r'\[([^\]]+)\]\((https?://[^)\s]+)\)', z[2]): quellen.append([t, u])
gesehen = set(); Q2 = []
for q in quellen:
    if q[1] not in gesehen: gesehen.add(q[1]); Q2.append(q)

F = {'k': K, 'gast': 'Michael Nehls', 'reiter': [R1, R2, R3, R4],
 'folgen_zeile': [DATUM, 'Michael Nehls', TITEL, 'Lithium, Hippocampus, Schlaf, Evolution, Intelligenz, RFK', '{{a:nehls-realtalk25|hier: Realtalk Mai 2025}}', '[ansehen](%s)' % URL],
 'neu': {'d': '2026-11-12', 't': 'Michael Nehls – Gespräch bei REALTALK (Mai 2025)',
         'k': 'Lithium, Gehirn, Schlaf, Evolution, Intelligenz, RFK: %d Abschnitte, Abgleich mit Fachstellen, Diagramme und Prüfstand.' % len(AB),
         'h': '#a-nehls-realtalk25', 'art': 'Video'},
 'quellen': Q2, 'web': []}
json.dump(F, open(O + '/folge.json', 'w'), ensure_ascii=False, indent=1)
print('folge.json', len(AB), 'Abschnitte', len(abg_zeilen), 'Abgleich', len(ZA), 'Zeitachse', len(FA.get('diagramme', [])), 'Diagramme', 'fehlende Fakten:', [k for k, _ in ABG if k not in FZ])
