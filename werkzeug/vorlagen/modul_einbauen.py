import re,sys
Q='quelle/gruenwissen.html'; h=open(Q).read()
css=open('werkzeug/vorlagen/folge.css').read().strip(); js=open('werkzeug/vorlagen/folge.js').read().strip()
# CSS
if '/* FOLGE-ANFANG */' in h:
    a=h.index('/* FOLGE-ANFANG */'); e=h.index('/* FOLGE-ENDE */')+len('/* FOLGE-ENDE */'); h=h[:a]+css+h[e:]
else:
    i=h.index('</style>\n',h.index('/* KURS-ENDE */')); 
    # letztes </style> vor qw-konfig
    k=h.index('<script id="qw-konfig">'); i=h.rindex('</style>',0,k); h=h[:i]+css+'\n'+h[i:]
# JS
blk='<script id="folge-modul">\n'+js+'\n</script>\n'
m=re.search(r'<script id="folge-modul">.*?</script>\n',h,re.S)
if m: h=h[:m.start()]+blk+h[m.end():]
else:
    i=h.index('<script id="kurs-modul">'); h=h[:i]+blk+h[i:]
# Haken im Hauptprogramm
alt="function block(b, pid, rid){\n  if(b.typ==='text')"
neu="""function block(b, pid, rid){
  if(b.typ==='folge') return QWFolge.folge(b,pid);
  if(b.typ==='folgenkarten') return QWFolge.folgenkarten(b,pid);
  if(b.typ==='gespraech') return QWFolge.gespraech(b);
  if(b.typ==='zeitachse'||(b.typ==='tabelle'&&b.zeitachse)) return QWFolge.zeitachse(b);
  if(b.typ==='balken') return QWFolge.balken(b);
  if(b.typ==='vergleich') return QWFolge.vergleich(b);
  if(b.typ==='abschnitt'&&QWFolge.istAbschnitt(b)) return QWFolge.abschnitt(b);
  if(b.typ==='text')"""
if 'QWFolge.folge(b,pid)' not in h:
    assert alt in h; h=h.replace(alt,neu,1)
alt="<h2>${esc(x.titel)}</h2>${x.bloecke.map(b=>block(b,pre,x.id)).join('')}</section>"
neu="<h2>${esc(x.titel)}</h2>${(QWFolge.reiter(),QWFolge.panel(x,x.bloecke.map(b=>block(b,pre,x.id)).join('')))}</section>"
if 'QWFolge.panel(x,' not in h:
    assert alt in h; h=h.replace(alt,neu,1)
alt="  main.innerHTML = `\n  <div class=\"stack seitenkopf\" style=\"--tc:${T.farbe||'var(--accent)'}\">"
if 'QWFolge.start(p,pre)' not in h:
    assert alt in h; h=h.replace(alt,"  QWFolge.inline=inline; QWFolge.start(p,pre);\n"+alt,1)
alt="initNaehrRechner(); QWKurs.init(main);\n  const tbd=main.querySelector('.tb-auto')"
if 'QWFolge.init(main)' not in h:
    assert alt in h; h=h.replace(alt,alt.replace("QWKurs.init(main);","QWKurs.init(main); QWFolge.init(main);"),1)
open(Q,'w').write(h); print('modul ok')
