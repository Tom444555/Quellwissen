"""python3 einbau_folge.py <ordner>  – baut scratch/<ordner>/folge.json in A-08 ein (wiederholbar)."""
import json,re,sys,subprocess,glob,os
O='/home/claude/scratch/'+sys.argv[1]; F=json.load(open(O+'/folge.json')); K=F['k']
Q='quelle/gruenwissen.html'
# Zeichnungen
for z in glob.glob(O+'/z_*.js'):
    h=open(Q).read(); namen=re.findall(r'^\s{4}(\w+)\(\)\{',open(z).read(),re.M); assert namen,z
    if not all(re.search(r'\n\s{4}'+n+r'\(\)\{',h) for n in namen): print(subprocess.run(['python3','werkzeug/zeichnung_einbauen.py',z],capture_output=True,text=True).stdout.strip(),namen)
h=open(Q).read(); m=re.search(r'(<script type="application/json" id="daten">)(.*?)(</script>)',h,re.S)
d=json.loads(m.group(2)); U=next(x for x in d['autoren'] if x['id']=='ungeskriptet')
ids=[K,K+'ab',K+'zeit',K+'abgleich']; assert [r['id'] for r in F['reiter']]==ids,[r['id'] for r in F['reiter']]
G=F['reiter'][0]['titel'].split(':')[0]
for r in F['reiter']: assert r['titel'].startswith(G+': '),r['titel']
# Prüfungen
ab=[b for b in F['reiter'][1]['bloecke'] if b['typ']=='abschnitt']; gv=next(b for b in F['reiter'][1]['bloecke'] if b['typ']=='gespraech')
th={t['k'] for t in gv['themen']}
for b in ab: assert re.search(r'\[\d+:\d\d[–-]\d+:\d\d\]\s*$',b['titel']),b['titel']; assert b.get('th') in th,b['titel']
if len(gv['teile'])!=len(ab): print('WARNUNG teile/abschnitte',len(gv['teile']),len(ab))
fo=next(b for b in F['reiter'][0]['bloecke'] if b['typ']=='folge')
alle=[b for r in F['reiter'] for b in r['bloecke']]
za=sum(len(b['eintraege']) for b in alle if b['typ']=='zeitachse'); abg=sum(len(b['zeilen']) for b in F['reiter'][3]['bloecke'] if b['typ']=='tabelle')
dia=sum(1 for b in alle if b['typ'] in('kurs','balken','vergleich','illu'))
fo['kacheln']=[[str(len(ab)),'Abschnitte'],['10','Kernaussagen'],[str(abg),'Abgleich-Punkte'],[str(za),'Zeitachse'],[str(dia),'Skizzen & Diagramme']]
fo['k']=K
alt=[r['id'] for r in U['reiter']]
U['reiter']=[r for r in U['reiter'] if r['id'] not in ids]
i=[r['id'] for r in U['reiter']].index('web'); U['reiter'][i:i]=F['reiter']
# Themenbaum der Folgen
fb=next(b for b in next(r for r in U['reiter'] if r['id']=='folgen')['bloecke'] if b['typ']=='baum'); ast=F.get('baum_ast')
if ast:
    for kn in fb['knoten']: kn['k']=[x for x in kn['k'] if x['t']!=ast['t']]
    ziel=next((kn for kn in fb['knoten'] if kn['t']==ast['gruppe']),None)
    if not ziel: ziel={"t":ast['gruppe'],"k":[]}; fb['knoten'].append(ziel)
    ziel['k'].append({"t":ast['t']})
# Web & Quellen
web=next(r for r in U['reiter'] if r['id']=='web'); t1,t2=[b for b in web['bloecke'] if b['typ']=='tabelle'][:2]
for w in F.get('web',[]):
    z=[w[0],'[%s](%s)'%(re.sub(r'^https?://(www\.)?','',w[1]).rstrip('/')[:40],w[1])]
    if not any(w[1] in x[1] for x in t1['zeilen']): t1['zeilen'].append(z)
if not any(fo['url'] in x[2] for x in t2['zeilen']): t2['zeilen'].append([fo['titel'],fo['gast'],'[ansehen](%s)'%fo['url']])
qu=next(b for b in next(r for r in U['reiter'] if r['id']=='quellen')['bloecke'] if b['typ']=='quellen'); hat={(e[0],e[1] if len(e)>1 else '') for e in map(tuple,qu['eintraege'])}
for e in F.get('quellen',[]):
    if (e[0],e[1] if len(e)>1 else '') not in hat: qu['eintraege'].append(e)
namen=[b['gast'] for r in U['reiter'] for b in r['bloecke'] if b['typ']=='folge']
for s in U['steckbrief']:
    if s[0]=='Ausgewertete Folgen': s[1]=', '.join(n.split()[-1] for n in namen)+' (hier); Krall, Ganser, Nehls, Kowallik (bei den Autoren)'
s=json.dumps(d,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
h=h[:m.start(2)]+s+h[m.end(2):]
# Was ist neu
n=F['neu']; zeile="  {d:%s,t:%s,k:%s,h:%s,art:'Podcast'},\n"%tuple(json.dumps(n[x],ensure_ascii=False).replace("'","’") for x in ('d','t','k','h'))
if n['h']+"'" not in h and n['h']+'"' not in h:
    a=re.search(r"\n(  \{d:'[\d-]+',t:)",h[h.index('<script id="qw-konfig">'):]); p=h.index('<script id="qw-konfig">')+a.start()+1; h=h[:p]+zeile+h[p:]
open(Q,'w').write(h); print('eingebaut',K,G,len(ab),'Abschnitte',abg,'Abgleich',za,'Zeitachse',dia,'Diagramme/Skizzen')
