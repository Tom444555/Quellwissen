"""Neue Zeichenfunktionen (JS-Datei mit 'name(){ ... return {vb,breit,leg,svg}; },') ins IL-Objekt Z einsetzen.
Aufruf: python3 zeichnung_einbauen.py <datei.js>"""
import sys,os,re
Q=os.path.join(os.path.dirname(__file__),'..','quelle','gruenwissen.html')
h=open(Q).read(); z=open(sys.argv[1]).read()
for name in re.findall(r'^\s{4}(\w+)\(\)\{',z,re.M):
    if re.search(r'\n\s{4}'+name+r'\(\)\{',h): sys.exit('gibt es schon: '+name)
h=h.replace("\n  };\n  const cache={};","\n"+z+"\n  };\n  const cache={};",1); open(Q,'w').write(h); print('ok')
