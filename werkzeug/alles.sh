#!/bin/bash
# Ein Befehl für alles vor dem Hochladen: Realismus-Modul einbetten, prüfen, bauen.
set -e; cd "$(dirname "$0")/.."
node --input-type=module --check < werkzeug/qw3d-plus.js
python3 werkzeug/plus_einbauen.py
python3 werkzeug/welt_einbauen.py
NODE_PATH=$(npm root -g) node werkzeug/minis_bauen.js
python3 werkzeug/pruefen.py | tee /tmp/qw_pruefen.txt; grep -q '^OK$' /tmp/qw_pruefen.txt
bash werkzeug/build.sh
echo "fertig – jetzt: git add -A && git commit && git push; Artefakt und Projekt-Dokument aktualisieren"
