"""Kapitel/Pflanze aus JSON in quelle/gruenwissen.html einsetzen.
Aufruf: python3 einbauen.py <bereich> <datei.json> [nach_id]
bereich: pflanzen | selbstversorgung | getreide | biochemie | autoren
Ersetzt einen Eintrag mit gleicher id, sonst Einfügen nach nach_id (oder ans Ende)."""
import json,re,sys,os
Q=os.path.join(os.path.dirname(__file__),'..','quelle','gruenwissen.html')
bereich,datei=sys.argv[1],sys.argv[2]; nach=sys.argv[3] if len(sys.argv)>3 else None
h=open(Q).read(); m=re.search(r'(<script type="application/json" id="daten">)(.*?)(</script>)',h,re.S)
d=json.loads(m.group(2)); arr=d[bereich]; neu=json.load(open(datei))
ids=[e['id'] for e in arr]
if neu['id'] in ids: arr[ids.index(neu['id'])]=neu
elif nach and nach in ids: arr.insert(ids.index(nach)+1,neu)
else: arr.append(neu)
s=json.dumps(d,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
open(Q,'w').write(h[:m.start(2)]+s+h[m.end(2):]); print('eingebaut:',neu['id'])
