import json,re,glob,sys
Q='quelle/gruenwissen.html'; h=open(Q).read(); m=re.search(r'(<script type="application/json" id="daten">)(.*?)(</script>)',h,re.S)
d=json.loads(m.group(2)); A={a['id']:a for a in d['autoren']}
EINL="**Gleicher Maßstab für beide Seiten.** Oben steht, was Daten und Fachstellen zu den Aussagen sagen. Hier steht, was auf Seiten von Staat, Behörden und Institutionen belegt ist – Versäumnisse, Korrekturen, Lücken in den Unterlagen. Nur Punkte mit Quelle; die Bewertung bleibt dem Leser."
link=re.compile(r'\[[^\]]+\]\(https?://[^)\s]+\)')
n_s=n_a=n_k=0; fehl=[]
for f in sorted(glob.glob('/home/claude/scratch/staat/[abc]*.json')):
    if f.endswith('bestand.json'): continue
    for e in json.load(open(f))['eintraege']:
        r=next(x for x in A[e['autor']]['reiter'] if x['id']==e['reiter'])
        r['bloecke']=[b for b in r['bloecke'] if not b.get('pruefstand')]
        # Korrekturen
        for k in e.get('korrekturen',[]):
            treffer=0
            for b in r['bloecke']:
                if b['typ']!='tabelle': continue
                for z in b['zeilen']:
                    for i,c in enumerate(z):
                        if isinstance(c,str) and k['alt'] in c: z[i]=c.replace(k['alt'],k['neu'],1); treffer+=1
            if treffer==1: n_k+=1
            elif not any(k['neu'] in c for b in r['bloecke'] if b['typ']=='tabelle' for z in b['zeilen'] for c in z if isinstance(c,str)): fehl.append((e['reiter'],treffer,k['alt'][:50]))
        st=[z for z in e.get('staat',[]) if len(z)==3 and link.search(z[2])]; au=[z for z in e.get('autor_zeilen',[]) if len(z)==3 and link.search(z[2])]
        if len(st)!=len(e.get('staat',[])) or len(au)!=len(e.get('autor_zeilen',[])): fehl.append((e['reiter'],'Zeile ohne Link verworfen'))
        neu=[]
        if st:
            neu+=[{"typ":"text","text":EINL,"pruefstand":True},
                  {"typ":"tabelle","kopf":["🏛️ Staat und Institutionen im Prüfstand","Was belegt ist 📚","Quelle"],"zeilen":st,"stapel":True,"pruefstand":True}]; n_s+=len(st)
        dl=[z for z in e.get('datenluecken',[]) if len(z)==3 and link.search(z[2])]
        if dl:
            neu+=[{"typ":"tabelle","kopf":["📉 Daten, die nicht erhoben wurden","Was dazu belegt ist 📚","Quelle"],"zeilen":dl,"stapel":True,"pruefstand":True}]; n_s+=len(dl)
        if e.get('fragen'):
            neu+=[{"typ":"abschnitt","titel":"❓ Offene Fragen an die Institutionen","liste":list(e['fragen']),"pruefstand":True}]
        if au:
            neu+=[{"typ":"tabelle","kopf":["🔎 Aussagen des Autors im Prüfstand – Ergänzung","Was belegt ist 📚","Quelle"],"zeilen":au,"stapel":True,"pruefstand":True}]; n_a+=len(au)
        if e.get('fazit'): neu+=[{"typ":"abschnitt","titel":"⚖️ Stand der Belege","liste":[e['fazit']],"pruefstand":True}]
        # Position: nach der Abgleich-Tabelle
        pos=max((i for i,b in enumerate(r['bloecke']) if b['typ']=='tabelle' and len(b['kopf'])>=3 and re.search(r'Aussage|Position|Thema',b['kopf'][0])),default=len(r['bloecke'])-1)+1
        r['bloecke'][pos:pos]=neu
        # Quellenverzeichnis des Autors ergänzen
        qr=next((x for x in A[e['autor']]['reiter'] if x['id']=='quellen'),None)
        if qr:
            qb=next(b for b in qr['bloecke'] if b['typ']=='quellen'); hat={x[1] for x in qb['eintraege'] if len(x)>1}
            for z in st+au+dl:
                for t,u in re.findall(r'\[([^\]]+)\]\((https?://[^)\s]+)\)',z[2]):
                    if u not in hat: qb['eintraege'].append([t,u]); hat.add(u)
s=json.dumps(d,ensure_ascii=False,separators=(',',':')).replace('</','<\\/'); open(Q,'w').write(h[:m.start(2)]+s+h[m.end(2):])
print('Staat-Zeilen',n_s,'Autor-Zeilen',n_a,'Korrekturen',n_k,'Probleme',fehl)
