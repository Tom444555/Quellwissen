# Quellwissen

Kompendium für Natur, Selbstversorgung und Gesundheit: Pflanzenkunde, Selbstversorgung, Getreide & Brot, Biochemie und Autoren.

Online: https://tom444555.github.io/Quellwissen/

Die Seite ist eine einzelne Datei (`index.html`) und läuft in jedem Browser, auch offline.

## Weiterarbeiten (für Claude)
- Quelle: `quelle/gruenwissen.html` (eine Datei: Daten-JSON + JS + CSS). Nie `index.html` direkt bearbeiten.
- Werkzeuge in `werkzeug/`: `bausteine.py`, `einbauen.py`, `zeichnung_einbauen.py`, `pruefen.py`, `foto.js`, `build.sh`.
- Ablauf: Quelle ändern → `python3 werkzeug/pruefen.py` → `bash werkzeug/build.sh` → commit & push.
