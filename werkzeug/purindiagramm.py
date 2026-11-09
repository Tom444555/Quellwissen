"""Gicht › Purinliste: alle Tabellenzeilen in eine Datenliste für das interaktive Diagramm umwandeln.
Aufruf: python3 werkzeug/purindiagramm.py   (erneut ausführen, wenn Tabellen im Reiter geändert wurden)
Schreibt/ersetzt Block {"typ":"purindiagramm","daten":[…]} im Reiter selbstversorgung/gicht/purinliste
(an Stelle des statischen Bildes gicht_purinliste bzw. nach dem Ampel-Hinweis).
Datensatz: g Gruppe, n Name, q Quellen, a Ampel g/y/r/u, u unsicher(❓), v=[min,max] mg/100 g (oder None),
p Portion, pg Portion in g/ml (Rechner), pv=[min,max] mg je Portion (oder None), x Zusatz/Notiz, ml True bei Getränken (mg/100 ml)."""
import json,re,os
Q=os.path.join(os.path.dirname(__file__),'..','quelle','gruenwissen.html')
GRUPPE=[('Fertiggerichte','Fertiggerichte'),('Feinkost','Feinkost & Salate'),('Saucen','Saucen & Würzmittel'),('Fleisch','Fleisch'),('Wurst','Wurst'),('Innereien','Innereien'),('Fisch','Fisch'),('Milch','Milch & Käse'),
        ('Eier','Eier'),('Fette','Fette'),('Getreide','Getreide'),('Weizen','Getreide'),('Roggen','Getreide'),('Dinkel','Getreide'),
        ('Hafer','Getreide'),('Beilagen','Beilagen'),('Hülsen','Hülsenfrüchte'),('Gemüse','Gemüse'),('Obst','Obst'),('Nüsse','Nüsse'),
        ('Bier','Bier'),('Sonstiges','Sonstiges')]
AMP={'🟢':'g','🟡':'y','🔴':'r','❓':'u'}
num=lambda s:float(s.replace(',','.'))
def gramm(p):
    """Übliche Portion in g bzw. ml (für den Gericht-Rechner)."""
    if not p: return None
    m=re.search(r'≈\s*(\d+(?:,\d+)?)\s*(g|ml)\b',p) or re.search(r'(\d+(?:,\d+)?)\s*(g|ml|l)\b',p)
    if m: x=num(m.group(1))*(1000 if m.group(2)=='l' else 1); return int(x)
    return 15 if 'EL' in p else 10 if 'TL' in p else 200 if 'Glas' in p else None
def spanne(s):
    m=re.search(r'(\d+(?:,\d+)?)\s*(?:–|-)\s*(\d+(?:,\d+)?)',s) or re.search(r'(\d+(?:,\d+)?)',s)
    if not m: return None
    a=num(m.group(1)); b=num(m.group(2)) if m.lastindex>1 else a
    return [int(a) if a==int(a) else a, int(b) if b==int(b) else b]
h=open(Q).read(); m=re.search(r'(<script type="application/json" id="daten">)(.*?)(</script>)',h,re.S)
d=json.loads(m.group(2)); kap=next(e for e in d['selbstversorgung'] if e['id']=='gicht')
r=next(x for x in kap['reiter'] if x['id']=='purinliste'); B=r['bloecke']
B[:]=[b for b in B if b['typ']!='purindiagramm']
daten=[]; gruppe=None
for b in B:
    if b['typ']=='abschnitt' and not b.get('liste'):
        t=b['titel']; gruppe=next((g for k,g in GRUPPE if k in t),gruppe)
    if b['typ']!='tabelle' or len(b['kopf']) not in (3,4) or b['kopf'][0] in ('Faustregel','Brot','Rezept (Kochbuch)'): continue
    getraenk='ml' in b['kopf'][1]; bier=b['kopf'][0].startswith('Bier')
    g='Bier' if bier else ('Getränke' if getraenk else gruppe)
    for z1,z2,z3,*_ in b['zeilen']:
        amp=AMP.get(z1[:1],'u'); name=re.search(r'\*\*(.+?)\*\*',z1).group(1)
        q=z1.split('**',2)[2].strip().lstrip('·').strip()
        unsicher='❓' in z1 or '❓' in z2 or 'abgeleitet' in z1
        v=spanne(z2) if z2.strip()!='❓' else None
        p=pv=None; x=''
        if v is None: x=z3
        elif bier: p='0,5 l'; pv=spanne(z3)
        elif '→' in z3:
            p,rest=[s.strip() for s in z3.split('→',1)]; pv=spanne(rest)
            x=re.sub(r'^\*{0,2}(ca\. )?[\d–,\. ]+(mg)?\*{0,2}\s*','',rest).replace('**','').strip(' ·')
        else:  # Getränke ohne Portion: „0 – aber Alkohol“, „0 (+ Zucker…)“
            pv=spanne(z3); p='1 Glas'; x=re.sub(r'^[\d–\s]+','',z3).strip(' –')
        if pv is None and v is not None and v==[0,0]: pv=[0,0]
        e={'g':g,'n':name,'a':amp,'v':v,'p':p,'pv':pv}
        pg=gramm(p)
        if pg: e['pg']=pg
        if q: e['q']=q
        if unsicher: e['u']=1
        if x: e['x']=x
        if getraenk: e['ml']=1
        daten.append(e)
blk={'typ':'purindiagramm','titel':'Alle Lebensmittel der Purinliste im Vergleich','daten':daten}
i=next((k for k,b in enumerate(B) if b.get('typ')=='illu' and b.get('id')=='gicht_purinliste'),None)
if i is not None: B[i]=blk
else: B.insert(next(k for k,b in enumerate(B) if b['typ']=='hinweis')+1,blk)
s=json.dumps(d,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
open(Q,'w').write(h[:m.start(2)]+s+h[m.end(2):])
ohne=sum(1 for e in daten if e['v'] is None)
print(f'{len(daten)} Zeilen, davon {ohne} ohne Messwert, Gruppen:',sorted({e["g"] for e in daten}))
