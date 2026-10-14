/* Quellwissen Service Worker: online immer die neueste Version, offline die gespeicherte. */
const CACHE = 'quellwissen-v1';
const KERN = ['./', './index.html', './manifest.webmanifest', './icon-192.png', './icon-512.png', './icon-maskable.png', './apple-touch-icon.png'];
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(KERN)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  const req = e.request; if (req.method !== 'GET') return;
  const url = new URL(req.url);
  const seite = req.mode === 'navigate' || (url.origin === location.origin && /\/(index\.html)?$/.test(url.pathname));
  if (seite) { // Netz zuerst: immer aktuell, offline aus dem Speicher
    e.respondWith(fetch(req, {cache: 'no-store'}).then(r => { const k = r.clone(); caches.open(CACHE).then(c => c.put('./index.html', k)); return r; })
      .catch(() => caches.match('./index.html').then(r => r || caches.match('./'))));
    return;
  }
  // Schriften, Bilder, Fotos: aus dem Speicher, im Hintergrund auffrischen
  e.respondWith(caches.match(req).then(hit => {
    const netz = fetch(req).then(r => { if (r && (r.ok || r.type === 'opaque')) { const k = r.clone(); caches.open(CACHE).then(c => c.put(req, k)); } return r; }).catch(() => hit);
    return hit || netz;
  }));
});
