# Quellwissen

Kompendium für Natur, Selbstversorgung und Gesundheit: Pflanzenkunde, Selbstversorgung, Getreide & Brot, Biochemie und Autoren.

Online: https://tom444555.github.io/Quellwissen/

Die Seite ist eine einzelne Datei (`index.html`) und läuft in jedem Browser, auch offline.

## Weiterarbeiten (für Claude)
- Quelle: `quelle/gruenwissen.html` (eine Datei: Daten-JSON + JS + CSS). Nie `index.html` direkt bearbeiten.
- Werkzeuge in `werkzeug/`: `bausteine.py`, `einbauen.py`, `zeichnung_einbauen.py`, `pruefen.py`, `foto.js`, `build.sh`.
- Ablauf: Quelle ändern → `python3 werkzeug/pruefen.py` → `bash werkzeug/build.sh` → commit & push.

### Werkzeuge (Kurzfassung)
- `bash werkzeug/alles.sh` – Realismus-Modul einbetten, prüfen, bauen (vor jedem Hochladen)
- `node werkzeug/foto3d.js p23 bild.png [--cam x,y,z,tx,ty,tz] [--niedrig] [--m männlich]` – 3D-Standbild ohne extra Server
- `node werkzeug/foto.js "#s-tinkturen-biochemie" bild.png` – Seiten-/Zeichnungs-Screenshot
- Git-Hook `werkzeug/hooks/pre-commit` (aktivieren: `git config core.hooksPath werkzeug/hooks`) blockt kaputte Commits
- GitHub Actions `.github/workflows/pruefen.yml` prüft jeden Push
