"""Prüft die drei Ebenen: Pflichtfelder im Kopf, Quellen vollständig, Koordinaten im Bereich, Punkt im angegebenen Land/Bundesland."""
import json, sys, collections
sys.path.insert(0, '/home/claude/scratch/wikidata')
import geo
PFLICHT = ['id', 'name', 'gruppe', 'typ', 'einheit', 'legende', 'quellen', 'hinweis', 'daten']
fehler = []
for f in ('welterbe_staetten.json', 'naturparks.json', 'heilbaeder.json'):
    d = json.load(open(f))
    for k in PFLICHT:
        if k not in d: fehler.append(f'{f}: Kopf ohne {k}')
    for q in d['quellen']:
        for k in ('t', 'u', 'stand', 'lizenz'):
            if not q.get(k): fehler.append(f'{f}: Quelle ohne {k}')
    n = 0; abw = []
    for e in d['daten']:
        if e.get('lon') is None: continue
        n += 1
        if not (-180 <= e['lon'] <= 180 and -90 <= e['lat'] <= 90): fehler.append(f"{f}: {e['n']} außerhalb")
        if d['gruppe'] == 'Deutschland':
            bl, innen = geo.bundesland(e['lon'], e['lat'], 0.1)
            if bl != e['land']: abw.append((e['n'], e['land'], bl, e['lon'], e['lat']))
    print(f, len(d['daten']), 'Einträge,', n, 'mit Lage; Bundesland-Abweichungen:', abw)
print('Fehler:', fehler or 'keine')
