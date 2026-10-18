// 3D-Ansicht als Standbild rendern – ohne extra Server.
// NODE_PATH=$(npm root -g) node werkzeug/foto3d.js p23 [aus.png] [--cam x,y,z,tx,ty,tz] [--niedrig] [--m männlich]
// Voraussetzung: bash werkzeug/build.sh (index.html aktuell). Software-Rendering: 1–2 Min. pro Bild.
const http = require('http'), fs = require('fs'), path = require('path'); const { chromium } = require('playwright');
const ROOT = path.resolve(__dirname, '..'); const a = process.argv.slice(2); const id = a[0] || 'p22'; const aus = (a[1] && !a[1].startsWith('--')) ? a[1] : `/tmp/3d_${id}.png`;
const opt = k => { const i = a.indexOf(k); return i >= 0 ? a[i + 1] : null; };
const TYP = { '.html': 'text/html', '.js': 'text/javascript', '.jpg': 'image/jpeg', '.png': 'image/png', '.json': 'application/json', '.webmanifest': 'application/manifest+json' };
const srv = http.createServer((q, r) => { const f = path.join(ROOT, decodeURIComponent(q.url.split('?')[0].split('#')[0])); if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { r.writeHead(404); return r.end(); } r.writeHead(200, { 'Content-Type': TYP[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(r); });
srv.listen(0, async () => { const port = srv.address().port;
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] }); const p = await b.newPage({ viewport: { width: 1100, height: 720 } });
  const err = []; p.on('pageerror', e => err.push(e.message)); p.on('console', m => { if (m.type() === 'error' && !/TUNNEL|Failed to load resource/.test(m.text())) err.push(m.text()); });
  await p.goto(`http://127.0.0.1:${port}/index.html${a.includes('--niedrig') ? '' : '?hoch'}`); await p.waitForTimeout(500);
  await p.evaluate(id => { window.QW3D_STANDBILD = true; QW3D.oeffne(id, null); }, id); await p.waitForFunction(() => window.QW3D_AKTIV, null, { timeout: 180000 });
  const m = opt('--m'); if (m) await p.evaluate(m => [...document.querySelectorAll('#qw3d button')].find(x => x.textContent.includes(m)).click(), m);
  await p.evaluate(cv => { const A = QW3D_AKTIV; A.ctl.autoRotate = false; if (cv) { const v = cv.split(',').map(Number); A.cam.position.set(v[0], v[1], v[2]); A.ctl.target.set(v[3], v[4], v[5]); } A.ctl.update(); A.zeichne(); }, opt('--cam') || '');
  await p.screenshot({ path: aus, timeout: 180000 }); console.log('three r' + await p.evaluate(() => THREE.REVISION), '→', aus, err.length ? 'Fehler: ' + err.join(' | ') : 'ohne Fehler');
  await b.close(); srv.close(); });
