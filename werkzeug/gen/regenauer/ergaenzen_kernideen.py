# Ergänzt bei A-11 die Reiter „Kernideen“ und „Seine Sicht“ um die Gespräche trump, iran, sozialismus (wiederholbar)
import json,re
Q='quelle/gruenwissen.html'; h=open(Q).read()
m=re.search(r'(<script type="application/json" id="daten">)(.*?)(</script>)',h,re.S); d=json.loads(m.group(2))
R=next(x for x in d['autoren'] if x['id']=='regenauer'); rt={r['id']:r for r in R['reiter']}
K=rt['kernideen']['bloecke']; S=rt['sicht']['bloecke']
def ab(B,anfang): return next(b for b in B if b['typ']=='abschnitt' and b['titel'].startswith(anfang))
def dazu(b,zeile):
    if zeile not in b['liste']: b['liste'].append(zeile)
dazu(ab(K,'1.'),'In den REALTALK-Gesprächen führt er das fort: Sichtbare Politik sei „Fernsehen“, Präsidenten beider Parteien gehörten zum selben Gefüge; den Gegner solle man dennoch nicht überschätzen – es seien wenige tausend gewöhnliche Menschen [seine Sicht]. [Trump und Epstein 1:45–1:57], [Iran und Energiekrise 1:11–1:17]')
dazu(ab(K,'3.'),'Nationalstaaten würden durch „gemachte Inkompetenz“ geschwächt, damit überstaatliche Stellen übernehmen; die EU nennt er das Pilotprojekt eines „Technate“ [seine Sicht]. [Trump und Epstein 1:45–1:57], [Iran und Energiekrise 0:54–0:57]')
dazu(ab(K,'5.'),'Neuere Bausteine aus seiner Sicht: Stablecoins nach dem GENIUS Act als Weg zu überwachbarem Geld auch ohne Zentralbankgeld; Energiemangel als Hebel, um über Kontingente, Bürger-Wallet und E-ID zuzuteilen („digitaler Gulag“) [seine Sicht]. [Trump und Epstein 0:00–0:03], [Iran und Energiekrise 0:14–0:20]')
dazu(ab(K,'6.'),'Im Gespräch über Sozialismus und Zionismus nennt er Eugenik und Kollektivismus den gemeinsamen Kern mehrerer Bewegungen um 1900 und sieht die Fortsetzung in der Technokratie [seine Sicht]. [Sozialismus und Zionismus 1:08–1:11], [Sozialismus und Zionismus 1:20–1:24]')
dazu(ab(K,'8.'),'Ohnmacht nennt er den größten Fehler: lokal vernetzen, Vereine, Kunst, Technik ohne die großen Anbieter, Erziehung mit Prinzipien. [Iran und Energiekrise 1:17–1:45], [Sozialismus und Zionismus 1:36]')
NEU=[
 ('9. Kriege und Krisen als Bühne',['Tagespolitik und Ankündigungen hält er für Ablenkung; entscheidend seien die Folgen. Den Iran-Krieg deutet er als Bühne („Truman Show“), die vor allem Energie verknappe; der Iran sei kein Gegenmodell, sondern setze dieselbe digitale Agenda um [seine Sicht]. [Iran und Energiekrise 0:11–0:33], [Iran und Energiekrise 0:42–0:47]']),
 ('10. Macht als Geflecht aus Finanzwelt, Geheimdiensten und Erpressung',['Den Fall Epstein versteht er vor allem als Finanz- und Erpressungsfall; Mafia, Geheimdienste, Banken und Politik seien verflochten. Was über belegbare Ebenen wie Banken und Denkfabriken hinausgeht, nennt er selbst Spekulation [seine Sicht]. [Trump und Epstein 0:18–0:48], [Iran und Energiekrise 1:02–1:11]']),
 ('11. Zionismus als politisches Projekt – getrennt vom Judentum',['Er trennt ausdrücklich zwischen Judentum, Israelis, Regierung und Zionismus und beschreibt den Zionismus als politisch-koloniales Projekt des späten 19. Jahrhunderts. Als Schlüsselfigur nennt er Moses Hess, von dem Linien zum Sozialismus wie zu Herzl führten; britisches Empire, Fabier und Frühzionisten hätten einander genützt [seine Sicht]. [Sozialismus und Zionismus 0:01–0:17], [Sozialismus und Zionismus 0:26–0:40]','Was Geschichtswissenschaft und Fachstellen dazu sagen, steht dort unter „Abgleich & Daten“.']),
]
for t,l in NEU:
    if not any(b.get('titel')==t for b in K): K.append({'typ':'abschnitt','titel':t,'liste':l})
dazu(ab(S,'📚'),'Populäre Erzählungen, die er nicht belegen kann, weist er zurück – etwa einen angeblichen Brief Albert Pikes oder die „Deagel“-Prognose. [Iran und Energiekrise 0:48–0:52]')
dazu(ab(S,'📚'),'Vorhersagen nennt er unseriös, macht in der Energiefrage aber ausdrücklich eine und hofft, sich zu irren. [Iran und Energiekrise 0:14–0:26]')
dazu(ab(S,'🧩'),'Sichtbare Politik sei Ablenkung; Versprechen wie die Freigabe der Epstein-Akten würden nicht eingelöst, gleich welche Partei regiert. [Trump und Epstein 0:12–0:21], [Trump und Epstein 1:42–1:45]')
dazu(ab(S,'🧩'),'Kriege und Mangel dienten dazu, Zuteilung und digitale Kontrolle durchzusetzen; die Geschichte von Sozialismus, Zionismus und Eugenik liest er als Vorgeschichte derselben Entwicklung. [Iran und Energiekrise 0:14–0:20], [Sozialismus und Zionismus 1:20–1:24]')
dazu(ab(S,'🛠️'),'Wissen in eigenes Handeln umsetzen – vor Ort und im persönlichen Kontakt; den Gegner nicht größer machen, als er ist. [Sozialismus und Zionismus 1:36], [Iran und Energiekrise 1:11–1:17]')
w=ab(S,'⚖️'); a='Den Abgleich mit Daten und der gängigen Darstellung sowie den Prüfstand findest du bei jedem Video im vierten Reiter.'
for z in ['Bei REALTALK widerspricht der Gastgeber beim Pike-Brief („komplizierter“) und sucht bei Ritualen „eine Mitte“; Regenauer bleibt bei seiner Linie. [Iran und Energiekrise 0:51], [Iran und Energiekrise 1:14–1:16]',
          'Er betont, alles sei mit Quellen belegt; einzelne zentrale Erzählungen bleiben im Gespräch ohne nachprüfbare Fundstelle ❓ (siehe Abgleich). [Sozialismus und Zionismus 0:07], [Sozialismus und Zionismus 1:30]']:
    if z not in w['liste']: w['liste'].insert(w['liste'].index(a) if a in w['liste'] else len(w['liste']),z)
s=json.dumps(d,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
open(Q,'w').write(h[:m.start(2)]+s+h[m.end(2):]); print('ok',len(K),len(S))
