# Baut goldreserven.json aus den IWF-IL-Abrufen (RGV_REVS, Feinunzen)
# Abruf: https://api.imf.org/external/sdmx/2.1/data/IMF.STA,IL/.RGV_REVS.FTO.{M,Q,A}?startPeriod=2020 (+ A ab 1990, M 2005–2019)
import re, json
R='/home/claude/scratch/welt_global/roh/'; OZ=32150.7466
laender={l['i']:l['n'] for l in json.load(open('/home/claude/quellwissen/werkzeug/welt_daten/welt_basis.json'))['laender']}
def key(p):
    if '-M' in p: y,m=p.split('-M'); return (int(y),int(m))
    if '-Q' in p: y,q=p.split('-Q'); return (int(y),int(q)*3)
    return (int(p),12)
def stand(p):
    if '-M' in p: y,m=p.split('-M'); return f'{int(m):02d}/{y}'
    if '-Q' in p: y,q=p.split('-Q'); return f'{q}. Quartal {y}'
    return f'Ende {p}'
best={}
for f in ['rgv_M.xml','rgv_Q.xml','rgv_A.xml','rgv_M_alt.xml','rgv_A_alt.xml']:
    x=open(R+f).read()
    for se in re.finditer(r'<Series ([^>]*)>(.*?)</Series>',x,re.S):
        c=re.search(r'COUNTRY="([^"]+)"',se.group(1)).group(1)
        obs=[(p,float(v)) for p,v in re.findall(r'TIME_PERIOD="([^"]+)" OBS_VALUE="([^"]+)"',se.group(2)) if v not in('','NaN')]
        if not obs: continue
        p,v=max(obs,key=lambda o:key(o[0]))
        if c not in best or key(p)>key(best[c][0]): best[c]=(p,v)
INST={'EZB':'Europäische Zentralbank (EZB)','IMF':'Internationaler Währungsfonds (IWF)','BIS':'Bank für Internationalen Zahlungsausgleich (BIZ)',
      'BEA':'Bank der Zentralafrikanischen Staaten (BEAC; CMR, CAF, TCD, COG, GAB, GNQ)','BCE':'Zentralbank der Westafrikanischen Staaten (BCEAO; BEN, BFA, CIV, GNB, MLI, NER, SEN, TGO)'}
UMBEN={'CWX':'CUW','KOS':'XKX','WBG':'PSE'}  # CWX = Zentralbank von Curaçao und Sint Maarten
# G759 = WAEMU-Aggregat = Bestand der BCEAO (neuer als die BCE-Reihe)
if 'G759' in best and ('BCE' not in best or key(best['G759'][0])>key(best['BCE'][0])): best['BCE']=best.pop('G759')
daten={}; inst={}; alt=[]; fehlt=[]
def rund(t): return round(t,1) if t>=1 else round(t,2)
for c,(p,v) in best.items():
    t=v/OZ
    if c in INST: inst[c]={'n':INST[c],'t':rund(t),'stand':stand(p)}; continue
    c2=UMBEN.get(c,c)
    if c2 not in laender: fehlt.append((c,p,round(t,1))); continue
    if key(p)<(2015,1): alt.append((c,p,round(t,1))); continue
    e={'t':rund(t),'stand':stand(p)}
    if c=='CWX': e['hinweis']='Gemeinsame Zentralbank von Curaçao und Sint Maarten'
    daten[c2]=e
daten=dict(sorted(daten.items(),key=lambda z:-z[1]['t']))
print('Länder',len(daten),'davon >0:',sum(1 for v in daten.values() if v['t']>0))
print('nicht zugeordnet (Aggregate/alte Codes):',fehlt)
print('vor 2015 (weggelassen):',alt)
print('Institutionen:',inst)
alt_txt=', '.join(f'{c} ({stand(p)}: {t} t)' for c,p,t in sorted(alt))
kopf={"id":"goldreserven","name":"Goldreserven der Zentralbanken","gruppe":"Wirtschaft","typ":"land-wert","einheit":"Tonnen",
 "legende":{"palette":"gold","skala":"Wurzel 0–8.200 t (Kreisgröße)","stufen":["100 t","1.000 t","8.000 t"]},
 "quellen":[{"t":"International Monetary Fund, International Liquidity (IL) – Teil der International Financial Statistics (IFS), Reihe „Gold reserves (volume)“ (RGV_REVS, Feinunzen), Meldungen der Zentralbanken nach IRFCL-Schema; Abruf über die SDMX-Schnittstelle api.imf.org am 26.11.2026",
   "u":"https://api.imf.org/external/sdmx/2.1/data/IMF.STA,IL/.RGV_REVS.FTO.M","stand":"neuester Monat je Land (meist 09–10/2026)",
   "lizenz":"IWF-Nutzungsbedingungen, „Special Terms for Statistical Data“ (https://www.imf.org/en/About/copyright-and-terms): Herunterladen, Bearbeiten, Veröffentlichen und Weitergeben erlaubt mit Quellenangabe „Source: International Monetary Fund, International Liquidity (IL), <Link>“ und Kennzeichnung von Umrechnungen; kommerzielle Weiterverwendung nur mit Genehmigung (copyright@imf.org)"}],
 "hinweis":("Bestand in Tonnen = Feinunzen ÷ 32.150,7466 (eigene Umrechnung, auf 0,1 t gerundet; unter 1 t auf 0,01 t). Neuester gemeldeter Monat je Land im Feld „stand“ – einzelne Länder melden selten (z. B. Russland 11/2025, Libanon 03/2025, Venezuela 06/2018). "
   "Wert 0 = Land meldet keinen Goldbestand (z. B. Kanada, Norwegen). Länder des Euroraums mit ihrer nationalen Zentralbank; EZB, IWF, BIZ und die Regionalzentralbanken BEAC und BCEAO stehen nicht als Land, sondern unter „daten_institutionen“ "
   "(Mitgliedsländer von BEAC/BCEAO halten ihr Gold über diese Banken). Weggelassen, weil letzte Meldung vor 2015: "+alt_txt+". Ohne Meldung im IWF-Datensatz: u. a. Nordkorea, Myanmar, Kuba. "
   "Amtliche Angaben sind Selbstauskünfte der Zentralbanken. Kommerzielle Nutzung (Verkauf von App/Buch) braucht laut IWF eine Genehmigung (copyright@imf.org)."),
 "daten":daten,"daten_institutionen":inst}
json.dump(kopf,open('/home/claude/scratch/welt_global/goldreserven.json','w'),ensure_ascii=False,separators=(',',':'))
