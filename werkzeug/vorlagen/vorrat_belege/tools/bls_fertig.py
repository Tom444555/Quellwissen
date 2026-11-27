import pandas as pd, json, re, sys
A={a['i']:a for a in json.load(open('/home/claude/quellwissen/werkzeug/vorlagen/vorrat_belege/bls_abgleich.json'))}
IDS='ravioli eintopf chili gulasch corned_beef fruehstuecksfleisch jagdwurst rotkohl_glas baked_beans erbsen_moehren suppe_tuete bruehe muesli riegel marmelade nusscreme ketchup senf pueree zwieback knaecke crackers salzstangen puddingpulver apfelmus pfirsiche birnen mandarinen kirschen ananas sauerkraut gurken rote_bete tortilla reiswaffeln dinkelmehl'.split()
codes={i:A[i]['bls_code'] for i in IDS}
d=pd.read_excel('bls/BLS_4_0_2025_DE/BLS_4_0_Daten_2025_DE.xlsx')
d=d.set_index('BLS Code')
COL={'k':'ENERCC Energie (Kilokalorien) [kcal/100g]','e':'PROT625 Protein (Nx6,25) [g/100g]','f':'FAT Fett [g/100g]','c':'CHO Kohlenhydrate, verfügbar [g/100g]','b':'FIBT Ballaststoffe, gesamt [g/100g]','vc':'VITC Vitamin C [mg/100g]','ca':'CA Calcium [mg/100g]','fe':'FE Eisen [mg/100g]','mg':'MG Magnesium [mg/100g]','zn':'ZN Zink [mg/100g]','fol':'FOLFD Folat [µg/100g]','b12':'VITB12 Vitamin B12 (Cobalamine) [µg/100g]'}
R={'k':0,'e':1,'f':1,'c':1,'b':1,'vc':1,'ca':0,'fe':2,'mg':0,'zn':2,'fol':0,'b12':2}
out={}
for i,c in codes.items():
  row=d.loc[c]; v={}
  for k,col in COL.items():
    x=row[col]
    if pd.isna(x): continue
    if isinstance(x,str):
      if x.strip().upper() in ('TR','<LOD','<LOQ'): x=0
      else: print('??',i,k,x); continue
    v[k]=round(float(x),R[k]) if R[k] else int(round(float(x)))
  out[i]={'bls':c,'name':row['Lebensmittelbezeichnung'],'w':v}
json.dump(out,open('bls_fertig.json','w'),ensure_ascii=False,indent=1)
for i,o in out.items(): print(i,o['bls'],o['w'])
