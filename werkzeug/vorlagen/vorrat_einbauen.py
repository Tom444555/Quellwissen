"""Setzt den „Vorrat & Blackout-Planer“ (werkzeug/vorlagen/vorrat.js + vorrat.css + werkzeug/z_vorrat.js) in die Quelle ein.
Aufruf aus dem Repo-Hauptordner: python3 werkzeug/vorlagen/vorrat_einbauen.py [pfad/zur/quelle.html]
Ohne Angabe wird quelle/gruenwissen.html geändert. Darf beliebig oft laufen. Danach: bash werkzeug/alles.sh

Was passiert (jeweils nur, wenn es noch fehlt bzw. ersetzt zwischen Markern):
  1. CSS zwischen /* VORRAT-ANFANG */ und /* VORRAT-ENDE */ (neu direkt hinter /* RECHNER-ENDE */)
  2. JS in <script id="vorrat-modul"> (neu direkt hinter dem Rechner-Modul)
  3. Zeichnung vorrat_bild ins Zeichen-Objekt Z (zwischen /* Z-VORRAT-ANFANG */ und /* Z-VORRAT-ENDE */)
  4. Route #vorrat, Funktion vorratSeite(), Leisten-Reiter „Mehr“
  5. Kachel oben auf der Rechner-Seite, Zeile im Blatt „Mehr“
  6. App-Suche findet die Seite (Vorrat, Blackout, Notvorrat, Stromausfall, Lager, Speiseplan, Haltbarkeit …)
  7. QW_KONFIG: Gruppen dürfen Verweise haben (links:[{t,h,i,k}]); Eintrag in Teil S, Gruppe „Sammeln & Küche“"""
import sys, os, re
basis = os.path.dirname(os.path.abspath(__file__))
werkzeug = os.path.dirname(basis)
Q = sys.argv[1] if len(sys.argv) > 1 else 'quelle/gruenwissen.html'
h = open(Q, encoding='utf-8').read()
js = open(os.path.join(basis, 'vorrat.js'), encoding='utf-8').read().strip('\n')
css = open(os.path.join(basis, 'vorrat.css'), encoding='utf-8').read().strip('\n')
zei = open(os.path.join(werkzeug, 'z_vorrat.js'), encoding='utf-8').read().rstrip('\n')
assert css.startswith('/* VORRAT-ANFANG */') and css.endswith('/* VORRAT-ENDE */') and '</script' not in js and '</script' not in zei
assert 'µ' not in zei, 'kein µ in Zeichnungen'
log = []

def einmal(alt, neu, was):
    global h
    if neu in h: return
    n = h.count(alt)
    if n != 1: sys.exit('Stelle für „%s“ nicht eindeutig gefunden (%d×) – Quelle prüfen.' % (was, n))
    h = h.replace(alt, neu, 1); log.append(was)

# 1. CSS
if '/* VORRAT-ANFANG */' in h:
    a = h.index('/* VORRAT-ANFANG */'); e = h.index('/* VORRAT-ENDE */') + len('/* VORRAT-ENDE */')
    h = h[:a] + css + h[e:]
else:
    e = h.index('/* RECHNER-ENDE */') + len('/* RECHNER-ENDE */')
    h = h[:e] + '\n' + css + h[e:]; log.append('CSS neu')

# 2. JS-Modul
k = '<script id="vorrat-modul">'
if k in h:
    a = h.index(k) + len(k); e = h.index('</script>', a)
    h = h[:a] + '\n' + js + '\n' + h[e:]
else:
    a = h.index('<script id="rechner-modul">'); e = h.index('</script>', a) + len('</script>')
    h = h[:e] + '\n' + k + '\n' + js + '\n</script>' + h[e:]; log.append('JS-Modul neu')

# 3. Zeichnung
ZA, ZE = '    /* Z-VORRAT-ANFANG */', '    /* Z-VORRAT-ENDE */'
if ZA in h:
    a = h.index(ZA); e = h.index(ZE) + len(ZE)
    h = h[:a] + ZA + '\n' + zei + '\n' + ZE + h[e:]
elif re.search(r'\n\s{4}vorrat_bild\(\)\{', h):
    log.append('Zeichnung vorrat_bild schon vorhanden (ohne Marker) – nicht ersetzt')
else:
    einmal("\n  };\n  const cache={};", "\n" + ZA + "\n" + zei + "\n" + ZE + "\n  };\n  const cache={};", 'Zeichnung')

# 4. Route, Seite, Reiter
einmal("  else if(h==='rechner'){ seite='rechner'; rechnerSeite(); }\n",
       "  else if(h==='rechner'){ seite='rechner'; rechnerSeite(); }\n  else if(h==='vorrat'){ seite='vorrat'; vorratSeite(); }\n", 'Route #vorrat')
einmal("(seite==='skills'||seite==='rechner')?'mehr'", "(seite==='skills'||seite==='rechner'||seite==='vorrat')?'mehr'", 'Reiter Mehr')
SEITE = """/* Seite „Vorrat & Blackout-Planer“ – Modul QWVorrat (Quelle: werkzeug/vorlagen/vorrat.js) */
function vorratSeite(){
  document.title='Vorrat & Blackout-Planer · Quellwissen';
  main.innerHTML=`<div class="stack seitenkopf">${krumen([['Start','#start'],['Rechner','#rechner'],['Vorrat & Blackout-Planer']])}</div><div id="vr-ort"></div><p class="fuss fusslinks"><a href="#rechner">Rechner</a><a href="#teil-S">Selbstversorgung</a><a href="#start">Startseite</a></p>`;
  if(window.QWVorrat) QWVorrat.seite(document.getElementById('vr-ort'),{figur:IL.has('vorrat_bild')?IL.figur('vorrat_bild','Vorratsregal mit Gläsern, Dosen, Nudeln, Wasser, Gaskocher und Kurbelradio'):''});
  scrollTo(0,0);
}
"""
einmal("function skillsSeite(){", SEITE + "function skillsSeite(){", 'vorratSeite()')

# 5. Kachel auf der Rechner-Seite, Zeile im Blatt „Mehr“
KACHEL = '<a class="vr-kachel" href="#vorrat"><span class="vr-ki" aria-hidden="true">🥫</span><span><b>Vorrat &amp; Blackout-Planer</b><small>Wie lange reichen Essen und Wasser? Was kann ich kochen, was fehlt noch?</small></span><span class="neu-pf" aria-hidden="true">›</span></a>'
einmal("${krumen([['Start','#start'],['Rechner & Umrechner']])}</div><div id=\"rz-ort\"></div>",
       "${krumen([['Start','#start'],['Rechner & Umrechner']])}</div>" + KACHEL + "<div id=\"rz-ort\"></div>", 'Kachel Rechner-Seite')
einmal("${zeile('#rechner','🧮','Rechner &amp; Umrechner','Prozent, Einheiten, Währungen, Chemie, Kalender','var(--c-b)')}",
       "${zeile('#rechner','🧮','Rechner &amp; Umrechner','Prozent, Einheiten, Währungen, Chemie, Kalender','var(--c-b)')}${zeile('#vorrat','🥫','Vorrat &amp; Blackout-Planer','Wie lange reichen Essen und Wasser?','var(--c-s)')}", 'Blatt Mehr')

# 4b. App-Suche: Eintrag für die Seite (wie andere Seiten über add(label, art, wo, hash, extra))
einmal("\nfunction suchen(q){", "\n/* VORRAT-SUCHE */ add('Vorrat & Blackout-Planer','Werkzeug','Rechner','vorrat','Vorrat Notvorrat Blackout Stromausfall Lager Lebensmittel Speiseplan Haltbarkeit Mindesthaltbarkeit Wasservorrat Krisenvorsorge Notfall Vorsorge Reichweite');\nfunction suchen(q){", 'Suche')

# 6. Verweise in Gruppen (QW_KONFIG): Render-Code und Eintrag
einmal("({t:g.t,rest:!!g.rest,items:", "({t:g.t,rest:!!g.rest,links:g.links||[],items:", 'Gruppen-Verweise (Daten)')
einmal("return gr.filter(g=>g.items.length||g.sammel);", "return gr.filter(g=>g.items.length||g.sammel||(g.links&&g.links.length));", 'Gruppen-Verweise (Filter)')
einmal("g.items.map(e=>zweig([eName(e,T.k),'#'+pre+e.id,g.kurz?null:e.illu])).join('')}",
       "g.items.map(e=>zweig([eName(e,T.k),'#'+pre+e.id,g.kurz?null:e.illu])).join('')+(g.links||[]).map(l=>zweig([l.t,l.h])).join('')}", 'Gruppen-Verweise (Startseite)')
einmal("${g.items.map(karten?kachel:eintrag).join('')}</div></section>",
       "${g.items.map(karten?kachel:eintrag).join('')}</div>${(g.links||[]).map(l=>`<a class=\"werk-teaser\" href=\"${esc(l.h)}\"><span class=\"werk-i\" aria-hidden=\"true\">${esc(l.i||'🧮')}</span><span><b>${esc(l.t)}</b>${l.k?`<small>${esc(l.k)}</small>`:''}</span><span class=\"neu-pf\" aria-hidden=\"true\">›</span></a>`).join('')}</section>", 'Gruppen-Verweise (Teil-Seite)')
einmal("     gruppen  [{t:'Name', ids:['id1','id2']}] – Reihenfolge der ids = Reihenfolge der Anzeige.\n",
       "     gruppen  [{t:'Name', ids:['id1','id2']}] – Reihenfolge der ids = Reihenfolge der Anzeige.\n              links:[{t:'Titel', h:'#ziel', i:'🥫', k:'Kurztext'}] an einer Gruppe: Verweise auf Werkzeug-Seiten (z. B. #vorrat).\n", 'Konfig-Kommentar')
if "h:'#vorrat'" not in h.split('<script id="qw-konfig">', 1)[1].split('</script>', 1)[0]:
    m = re.search(r"\{t:'Sammeln & Küche',ids:\[[^\]]*\]", h)
    if not m: sys.exit('Gruppe „Sammeln & Küche“ in QW_KONFIG nicht gefunden.')
    h = h[:m.end()] + ",links:[{t:'Vorrat & Blackout-Planer',h:'#vorrat',i:'🥫',k:'Wie lange reichen Essen und Wasser? Was kann ich daraus kochen?'}]" + h[m.end():]
    log.append('Konfig-Eintrag')

open(Q, 'w', encoding='utf-8').write(h)
print('Vorrat-Modul eingesetzt in', Q, '·', len(js), 'Zeichen JS,', len(css), 'Zeichen CSS' + (' · neu: ' + ', '.join(log) if log else ''))
