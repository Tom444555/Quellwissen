"""Baut werkzeug/vorlagen/vorrat_fakten.js aus den Beleg-Dateien (JSON) für den Vorrats-Planer.
Aufruf: python3 werkzeug/vorlagen/vorrat_fakten_bauen.py <ordner-mit-json>
Erwartet je Datei {thema, stand, eintraege:[{id, titel, text, wert, einheit, warnung, quelle:{t,u,stand}, abschnitt|kategorie, …}], quellen, hinweis}.
Quellen werden in einer gemeinsamen Tabelle gesammelt (spart Platz). Inhalte werden nicht verändert."""
import sys, os, json, glob
basis = os.path.dirname(os.path.abspath(__file__))
ordner = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vorrat_belege', 'fakten')   # Belege liegen im Repo
Q, QI, out = [], {}, {}
def qidx(q):
    if not q: return -1
    if isinstance(q, str): q = {'t': q, 'u': '', 'stand': ''}
    key = (q.get('t', ''), q.get('u', ''), q.get('stand', ''))
    if key not in QI: QI[key] = len(Q); Q.append(list(key))
    return QI[key]
STD = {'id', 'titel', 'text', 'wert', 'einheit', 'warnung', 'quelle', 'abschnitt', 'kategorie'}
for f in sorted(glob.glob(os.path.join(ordner, '*.json'))):
    name = os.path.splitext(os.path.basename(f))[0]
    d = json.load(open(f, encoding='utf-8'))
    E = []
    for e in d.get('eintraege', []):
        x = [e.get('id'), e.get('abschnitt') or e.get('kategorie') or '', e.get('titel', ''), e.get('text', ''), e.get('wert'), e.get('einheit') or '', e.get('warnung') or '', qidx(e.get('quelle'))]
        mehr = {k: v for k, v in e.items() if k not in STD}
        if mehr: x.append(mehr)
        E.append(x)
    qs = [qidx(q) for q in (d.get('quellen') or []) if isinstance(q, dict)]
    out[name] = {'thema': d.get('thema', ''), 'stand': d.get('stand', ''), 'hinweis': d.get('hinweis', ''), 'E': E, 'q': qs}
    for k in d:
        if k not in ('thema', 'stand', 'eintraege', 'quellen', 'hinweis'): out[name][k] = d[k]
js = ('/* Belege für den Vorrats-Planer – erzeugt von vorrat_fakten_bauen.py aus den Beleg-Dateien (nicht von Hand ändern).\n'
      '   Eintrag: [id, Abschnitt/Kategorie, Titel, Text, Wert, Einheit, Warnung, Quellen-Nr., Zusatzfelder?] · Q: [Titel, Adresse, Stand] */\n'
      '(function (root) {\nroot.QWVorratFakten = ' + json.dumps({'Q': Q, 'T': out}, ensure_ascii=False, separators=(',', ':')) + ';\n})(typeof window !== "undefined" ? window : globalThis);\n')
assert '</script' not in js.lower()
open(os.path.join(basis, 'vorrat_fakten.js'), 'w', encoding='utf-8').write(js)
print('vorrat_fakten.js:', len(js.encode('utf-8')) // 1024, 'KB ·', ', '.join('%s (%d)' % (k, len(v['E'])) for k, v in out.items()), '·', len(Q), 'Quellen')
