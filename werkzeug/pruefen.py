"""Prüft quelle/gruenwissen.html: JSON, interne Links {{p:..}} {{s:..}} {{g:..}} {{b:..}} {{a:..}}, Illu-IDs, JS-Syntax (node --check)."""
import json,re,os,subprocess,tempfile
Q=os.path.join(os.path.dirname(__file__),'..','quelle','gruenwissen.html')
h=open(Q).read(); d=json.loads(re.search(r'id="daten">(.*?)</script>',h,re.S).group(1))
B={'p':'pflanzen','s':'selbstversorgung','g':'getreide','b':'biochemie','a':'autoren','w':'welt'}
ids={k:{e['id'] for e in d[v]} for k,v in B.items()}
fehler=0
for t,ref in re.findall(r'\{\{(\w):([^|}]+)',json.dumps(d,ensure_ascii=False)):
    if t not in B: continue
    teile=ref.split('#')[0].split('-')
    if not any('-'.join(teile[:i]) in ids[t] for i in range(1,len(teile)+1)): print('Link kaputt:',t,ref); fehler+=1
for i in set(re.findall(r'"(?:illu|id)":"([a-z0-9_]+)"',json.dumps([b for v in B.values() for e in d[v] for r in e.get('reiter',[]) for b in r['bloecke'] if b.get('typ')=='illu']+[{'illu':e.get('illu')} for v in B.values() for e in d[v] if e.get('illu')]))):
    if not re.search(r'\n\s{4}'+i+r'\(\)\{',h): print('Zeichnung fehlt:',i); fehler+=1
for k,s in enumerate(re.findall(r'<script>(.*?)</script>',h,re.S)):
    f=tempfile.NamedTemporaryFile('w',suffix='.js',delete=False); f.write(s); f.close()
    r=subprocess.run(['node','--check',f.name],capture_output=True,text=True)
    if r.returncode: print('JS-Fehler in Skript',k,r.stderr[:400]); fehler+=1
print('OK' if not fehler else f'{fehler} Fehler')
