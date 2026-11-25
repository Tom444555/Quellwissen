#!/bin/sh
# Baut alle Themen-Ebenen neu und prüft sie
set -e
cd "$(dirname "$0")"
for s in sprachen religionen reiche handel welterbe megalithen fahrten buendnisse stuetzpunkte energiewege kraftwerke geld; do python3 $s.py >/dev/null; done
python3 pruefen.py
