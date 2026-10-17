import json
# Bausteine für Kapiteldaten (Quellwissen). Achtung: tab(kopf, zeile1, zeile2, ...) – Zeilen einzeln, NICHT als Liste in Liste.
def tab(kopf, *zeilen): return {"typ":"tabelle","kopf":kopf,"zeilen":list(zeilen)}
def txt(t): return {"typ":"text","text":t}
def hin(t): return {"typ":"hinweis","text":t}
def abs_(titel, liste=None, nummern=None):
    b={"typ":"abschnitt","titel":titel}
    if liste: b["liste"]=liste
    if nummern: b["nummern"]=nummern
    return b
def illu(i,t): return {"typ":"illu","id":i,"titel":t}
def std(licht,wasser,naehr,ph,boden,ell="",note=""):
    return {"typ":"standort","licht":licht,"wasser":wasser,"naehrstoffe":naehr,"ph":ph,"boden":boden,"ellenberg":ell,"hinweis":note}
def karten(art, eintraege, filt=None):
    if not filt:
        ks=[]
        for e in eintraege:
            if e["kat"] not in ks: ks.append(e["kat"])
        names={"innerlich":"Innerlich","aeusserlich":"Äußerlich","kueche":"Küche","vorrat":"Vorrat","garten":"Garten","sammeln":"Sammeln","anbau":"Anbau","alle":"Alle","haus":"Haus"}
        filt=[["alle","Alle"]]+([[k,names.get(k,k)] for k in ks] if len(ks)>1 else [])
    return {"typ":"karten","art":art,"filter":filt,"eintraege":eintraege}
def anw(id,titel,kat,beleg,teil,kurz,zut,schr,hinweis=None,tipp=None):
    e={"id":id,"titel":titel,"kat":kat,"beleg":beleg,"teil":teil,"kurz":kurz,"zutaten":zut,"schritte":schr}
    if hinweis: e["hinweis"]=hinweis
    if tipp: e["tipp"]=tipp
    return e
def rez(id,titel,kat,menge,zeit,kurz,zut,schr,tipp=None,hinweis=None):
    e={"id":id,"titel":titel,"kat":kat,"menge":menge,"zeit":zeit,"kurz":kurz,"zutaten":zut,"schritte":schr}
    if tipp: e["tipp"]=tipp
    if hinweis: e["hinweis"]=hinweis
    return e
def q(*l): return {"typ":"quellen","eintraege":[list(x) for x in l]}
def R(id,titel,*b): return {"id":id,"titel":titel,"bloecke":list(b)}
