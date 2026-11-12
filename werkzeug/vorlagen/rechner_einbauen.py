"""Setzt das Rechner-Modul (werkzeug/vorlagen/rechner.js + rechner.css) in die Quelle ein.
Aufruf aus dem Repo-Hauptordner: python3 werkzeug/vorlagen/rechner_einbauen.py [pfad/zur/quelle.html]
Ohne Angabe wird quelle/gruenwissen.html geändert. Danach: bash werkzeug/alles.sh"""
import sys, os
basis = os.path.dirname(os.path.abspath(__file__))
Q = sys.argv[1] if len(sys.argv) > 1 else 'quelle/gruenwissen.html'
h = open(Q, encoding='utf-8').read()
js = open(os.path.join(basis, 'rechner.js'), encoding='utf-8').read().strip('\n')
css = open(os.path.join(basis, 'rechner.css'), encoding='utf-8').read().strip('\n')
assert css.startswith('/* RECHNER-ANFANG */') and '</script' not in js
a = h.index('/* RECHNER-ANFANG */'); e = h.index('/* RECHNER-ENDE */')
h = h[:a] + css + '\n' + h[e:]
k = '<script id="rechner-modul">'; a = h.index(k) + len(k); e = h.index('</script>', a)
h = h[:a] + '\n' + js + '\n' + h[e:]
open(Q, 'w', encoding='utf-8').write(h)
print('Rechner-Modul eingesetzt in', Q, '·', len(js), 'Zeichen JS,', len(css), 'Zeichen CSS')
