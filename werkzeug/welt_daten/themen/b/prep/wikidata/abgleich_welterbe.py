"""Abgleich welterbe_staetten.json (Wikidata) mit b/fertig/welterbe.json (Länderzählung)."""
import json, collections
D = json.load(open('welterbe_staetten.json'))['daten']
b = json.load(open('/home/claude/quellwissen/werkzeug/welt_daten/themen/b/fertig/welterbe.json'))['daten']
c = collections.Counter(i for e in D for i in e['iso3'])
for k in sorted(set(c) | set(b)):
    if c.get(k, 0) != b.get(k, {}).get('n', 0):
        print(f"{k}\tWikidata {c.get(k,0)}\tb {b.get(k,{}).get('n',0)}")
