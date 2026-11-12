# Nehls: Reiter „Gespräche“ mit Folgenkarten anlegen; REALTALK: Steckbrief-Zeile umbenennen (wiederholbar)
import json,re
Q='quelle/gruenwissen.html'; h=open(Q).read()
m=re.search(r'(<script type="application/json" id="daten">)(.*?)(</script>)',h,re.S); d=json.loads(m.group(2))
n=next(x for x in d['autoren'] if x['id']=='nehls')
if not any(r['id']=='folgen' for r in n['reiter']):
    i=[r['id'] for r in n['reiter']].index('web')
    n['reiter'].insert(i,{"id":"folgen","titel":"Gespräche","bloecke":[
      {"typ":"text","text":"Lange Gespräche mit Michael Nehls, ausgewertet im Folgen-Aufbau: je Gespräch Überblick, Verlauf im Detail, Zeitachse und Abgleich mit Daten samt Prüfstand. Eine Karte antippen öffnet die Auswertung. Ältere Zusammenfassungen stehen weiter im Reiter „Videos“."},
      {"typ":"folgenkarten"}]})
if not any(s[0]=='Ausgewertete Videos' for s in n['steckbrief']): n['steckbrief'].append(["Ausgewertete Videos","0"])
r=next(x for x in d['autoren'] if x['id']=='realtalk')
for s in r['steckbrief']:
    if s[0]=='Ausgewertete Folgen': s[0]='Ausgewertete Videos'
s=json.dumps(d,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
open(Q,'w').write(h[:m.start(2)]+s+h[m.end(2):]); print('ok')
