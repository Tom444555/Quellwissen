#!/usr/bin/env python3
"""Bettet die Weltkarte ein (Daten + Modul) und verdrahtet Route, Navigation und Startseite. Idempotent."""
import re,os,subprocess
W=os.path.dirname(__file__); Q=os.path.join(W,'..','quelle','gruenwissen.html')
s=open(Q).read()
daten=open(os.path.join(W,'welt_daten','welt_basis.json')).read().replace('</','<\\/')
modul=open(os.path.join(W,'welt.js')).read()
subprocess.run(['node','--check',os.path.join(W,'welt.js')],check=True)
import base64
rel=base64.b64encode(open(os.path.join(W,'welt_daten','relief.jpg'),'rb').read()).decode()
blk=f'<script type="application/json" id="weltdaten">{daten}</script>\n<script type="text/plain" id="weltrelief">{rel}</script>\n<script id="welt-modul">{modul}</script>\n'
s=re.sub(r'<script type="application/json" id="weltdaten">.*?</script>\n(<script type="text/plain" id="weltrelief">.*?</script>\n)?<script id="welt-modul">.*?</script>\n','',s,flags=re.S)
i=s.index('<script type="application/json" id="daten">'); s=s[:i]+blk+s[i:]
if 'window.QW_DATEN=D;' not in s: s=s.replace("const D = JSON.parse(document.getElementById('daten').textContent);","const D = JSON.parse(document.getElementById('daten').textContent); window.QW_DATEN=D;",1)
if 'data-ziel="welt"' not in s: s=s.replace('<button data-ziel="teil-A">A · Autoren</button>','<button data-ziel="teil-A">A · Autoren</button>\n      <button data-ziel="welt" class="welt-knopf">🌍 Weltkarte</button>',1)
if 'function weltSeite' not in s:
    s=s.replace('function route(){',"""function weltSeite(){ main.innerHTML='<div id="welt-wurzel"></div>'; if(window.QWWELT) QWWELT.oeffne(document.getElementById('welt-wurzel')); scrollTo(0,0); }
function route(){""",1)
    s=s.replace("if(!h || h==='start') startSeite();","if(!h || h==='start') startSeite();\n  else if(h==='welt'){ teil='W'; weltSeite(); }",1)
    s=s.replace("b.setAttribute('aria-current', b.dataset.ziel==='teil-'+teil)","b.setAttribute('aria-current', b.dataset.ziel==='teil-'+teil || (teil==='W'&&b.dataset.ziel==='welt'))",1)
if 'class="welt-teaser"' not in s:
    s=s.replace("  ${uebersicht()}\n  ${legende()}`;","""  <a class="welt-teaser" href="#welt"><span class="wt-globus"></span><span class="wt-text"><b>🌍 Weltkarte</b><small>Bevölkerung, Wachstum, Getreide, Rohstoffe, Klima, Böden und alle Pflanzen des Kompendiums – interaktiv auf dem Globus</small></span><span class="wt-pfeil">→</span></a>
  ${uebersicht()}
  ${legende()}`;""",1)
    css=""".welt-teaser{box-sizing:border-box;width:100%;max-width:100%;display:flex;align-items:center;gap:16px;margin:18px 0 22px;padding:16px 18px;border-radius:18px;background:radial-gradient(circle at 12% 50%,#16335a,#070c18 70%);color:#eaf2ff;text-decoration:none;box-shadow:0 10px 30px rgba(5,10,25,.35);border:1px solid #1f2b44}
.welt-teaser b{font:700 19px Georgia,serif;display:block}.welt-teaser small{color:#9fb0d0;font-size:13px;line-height:1.4}
.wt-globus{flex:none;width:64px;height:64px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#8ad8ff,#2a6fb0 45%,#0b2a50 75%);box-shadow:0 0 0 3px rgba(80,170,255,.15),0 0 26px rgba(80,170,255,.55)}
.wt-pfeil{margin-left:auto;font-size:24px;color:#4ad0a0}
.teile .welt-knopf{background:#0d1a30;color:#cfe3ff;border-color:#1f3a60}
</style>"""
    s=s.replace('</style>',css,1)
open(Q,'w').write(s); print('Weltkarte eingebettet',len(daten)//1024,'KB Daten')
