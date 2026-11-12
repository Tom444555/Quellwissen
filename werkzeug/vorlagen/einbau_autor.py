"""python3 werkzeug/vorlagen/einbau_autor.py <autor-id> <ordner> [K-neu] [Titel-Präfix-neu]

Baut scratch/<ordner>/folge.json (Format aus auftrag_folge.md) bei einem beliebigen Autor ein
(Sammelstelle wie Lausen, Ganser, Wikihausen) – wiederholbar. Liegt daneben eine pruefstand.json,
wird der Prüfstand gleich hinter die Abgleich-Tabelle gesetzt.
K-neu / Präfix-neu benennen Reiter-Ids und Titel um (z. B. ganser -> video, „Ganser“ -> „Ungeskriptet“).
"""
import json,re,sys,subprocess,glob,os
AID=sys.argv[1]; O='/home/claude/scratch/'+sys.argv[2]; F=json.load(open(O+'/folge.json')); K0=F['k']
K=sys.argv[3] if len(sys.argv)>3 else K0
Q='quelle/gruenwissen.html'
EINL="**Gleicher Maßstab für beide Seiten.** Oben steht, was Daten und Fachstellen zu den Aussagen sagen. Hier steht, was auf Seiten von Staat, Behörden und Institutionen belegt ist – Versäumnisse, Korrekturen, Lücken in den Unterlagen. Nur Punkte mit Quelle; die Bewertung bleibt dem Leser."
link=re.compile(r'\[[^\]]+\]\(https?://[^)\s]+\)')
# Zeichnungen
for z in glob.glob(O+'/z_*.js'):
    h=open(Q).read(); namen=re.findall(r'^\s{4}(\w+)\(\)\{',open(z).read(),re.M); assert namen,z
    if not all(re.search(r'\n\s{4}'+n+r'\(\)\{',h) for n in namen): print(subprocess.run(['python3','werkzeug/zeichnung_einbauen.py',z],capture_output=True,text=True).stdout.strip(),namen)
h=open(Q).read(); m=re.search(r'(<script type="application/json" id="daten">)(.*?)(</script>)',h,re.S)
d=json.loads(m.group(2)); U=next(x for x in d['autoren'] if x['id']==AID)
ids0=[K0,K0+'ab',K0+'zeit',K0+'abgleich']; assert [r['id'] for r in F['reiter']]==ids0,[r['id'] for r in F['reiter']]
ids=[K,K+'ab',K+'zeit',K+'abgleich']
G0=F['reiter'][0]['titel'].split(':')[0]; G=sys.argv[4] if len(sys.argv)>4 else G0
for r,i in zip(F['reiter'],ids):
    assert r['titel'].startswith(G0+': '),r['titel']; r['id']=i; r['titel']=G+r['titel'][len(G0):]
# Prüfungen
ab=[b for b in F['reiter'][1]['bloecke'] if b['typ']=='abschnitt']; gv=next(b for b in F['reiter'][1]['bloecke'] if b['typ']=='gespraech')
th={t['k'] for t in gv['themen']}
for b in ab: assert re.search(r'\[\d+:\d\d[–-]\d+:\d\d\]\s*$',b['titel']),b['titel']; assert b.get('th') in th,b['titel']
if len(gv['teile'])!=len(ab): print('WARNUNG teile/abschnitte',len(gv['teile']),len(ab))
fo=next(b for b in F['reiter'][0]['bloecke'] if b['typ']=='folge')
# Prüfstand
pf=O+'/pruefstand.json'; n_p=0
if os.path.exists(pf):
    e=json.load(open(pf))['eintraege'][0]; r=F['reiter'][3]
    r['bloecke']=[b for b in r['bloecke'] if not b.get('pruefstand')]
    ok=lambda L:[z for z in L if len(z)==3 and link.search(z[2])]
    st,dl,au=ok(e.get('staat',[])),ok(e.get('datenluecken',[])),ok(e.get('autor_zeilen',[]))
    if (len(st),len(dl),len(au))!=(len(e.get('staat',[])),len(e.get('datenluecken',[])),len(e.get('autor_zeilen',[]))): print('WARNUNG Prüfstand-Zeile ohne Link verworfen')
    neu=[]
    if st: neu+=[{"typ":"text","text":EINL,"pruefstand":True},{"typ":"tabelle","kopf":["🏛️ Staat und Institutionen im Prüfstand","Was belegt ist 📚","Quelle"],"zeilen":st,"stapel":True,"pruefstand":True}]
    if dl: neu+=[{"typ":"tabelle","kopf":["📉 Daten, die nicht erhoben wurden","Was dazu belegt ist 📚","Quelle"],"zeilen":dl,"stapel":True,"pruefstand":True}]
    if au: neu+=[{"typ":"tabelle","kopf":["🔎 Aussagen im Prüfstand – Ergänzung","Was belegt ist 📚","Quelle"],"zeilen":au,"stapel":True,"pruefstand":True}]
    if e.get('fragen'): neu+=[{"typ":"abschnitt","titel":"❓ Offene Fragen an die Institutionen","liste":list(e['fragen']),"pruefstand":True}]
    if e.get('fazit'): neu+=[{"typ":"abschnitt","titel":"⚖️ Stand der Belege","liste":[e['fazit']],"pruefstand":True}]
    pos=max((i for i,b in enumerate(r['bloecke']) if b['typ']=='tabelle' and len(b['kopf'])>=3 and re.search(r'Aussage',b['kopf'][0])),default=len(r['bloecke'])-1)+1
    r['bloecke'][pos:pos]=neu; n_p=len(st)+len(dl)+len(au)
    for z in st+dl+au:
        for t,u in re.findall(r'\[([^\]]+)\]\((https?://[^)\s]+)\)',z[2]): F.setdefault('quellen',[]).append([t,u])
alle=[b for r in F['reiter'] for b in r['bloecke']]
za=sum(len(b['eintraege']) for b in alle if b['typ']=='zeitachse'); abg=sum(len(b['zeilen']) for b in F['reiter'][3]['bloecke'] if b['typ']=='tabelle' and not b.get('pruefstand'))
dia=sum(1 for b in alle if b['typ'] in('kurs','balken','vergleich','illu'))
fo['kacheln']=[[str(len(ab)),'Abschnitte'],['10','Kernaussagen'],[str(abg),'Abgleich-Punkte'],[str(za),'Zeitachse'],[str(dia),'Skizzen & Diagramme']]
fo['k']=K
U['reiter']=[r for r in U['reiter'] if r['id'] not in ids]
i=[r['id'] for r in U['reiter']].index('web'); U['reiter'][i:i]=F['reiter']
# Web & Quellen
web=next(r for r in U['reiter'] if r['id']=='web'); tab=[b for b in web['bloecke'] if b['typ']=='tabelle']
if tab:
    for w in F.get('web',[]):
        if not any(w[1].rstrip('/') in x[-1] for x in tab[0]['zeilen']): tab[0]['zeilen'].append([w[0],'[%s](%s)'%(re.sub(r'^https?://(www\.)?','',w[1]).rstrip('/')[:40],w[1])])
    if len(tab)>1 and not any(fo['url'] in x[-1] for x in tab[1]['zeilen']): tab[1]['zeilen'].append([fo['titel'],fo.get('kanal',''),'[ansehen](%s)'%fo['url']])
qu=next(b for b in next(r for r in U['reiter'] if r['id']=='quellen')['bloecke'] if b['typ']=='quellen'); hat={e[1] for e in qu['eintraege'] if len(e)>1}
for e in F.get('quellen',[]):
    if len(e)>1 and e[1] not in hat: qu['eintraege'].append(e); hat.add(e[1])
nv=sum(1 for r in U['reiter'] for b in r['bloecke'] if b['typ']=='folge')
for s in U['steckbrief']:
    if s[0]=='Ausgewertete Videos': s[1]='%d (Stand %s)'%(nv,'.'.join(reversed(F['neu']['d'].split('-'))))
s=json.dumps(d,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
h=h[:m.start(2)]+s+h[m.end(2):]
# Was ist neu
n=dict(F['neu']); n['h']='#a-%s-%s'%(AID,K)
zeile="  {d:%s,t:%s,k:%s,h:%s,art:%s},\n"%tuple(json.dumps(n[x],ensure_ascii=False).replace("'","’") for x in ('d','t','k','h','art'))
zeile=re.sub(r'(?<=[:,])"|"(?=[,}])',"'",zeile)
if n['h']+"'" not in h and n['h']+'"' not in h:
    a=re.search(r"\n(  \{d:'[\d-]+',t:)",h[h.index('<script id="qw-konfig">'):]); p=h.index('<script id="qw-konfig">')+a.start()+1; h=h[:p]+zeile+h[p:]
open(Q,'w').write(h); print('eingebaut',AID,K,G,len(ab),'Abschnitte',abg,'Abgleich',za,'Zeitachse',dia,'Diagramme/Skizzen',n_p,'Prüfstand-Zeilen')
