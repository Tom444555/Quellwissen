#!/bin/sh
# Aufruf: sparql.sh abfrage.rq ausgabe.json
curl -s -m 300 -G https://query.wikidata.org/sparql --data-urlencode 'format=json' --data-urlencode "query@$1" -A 'QuellwissenDatenabruf/1.0 (research script)' -o "$2"
