/* Quellwissen – „Vorrat & Blackout-Planer“, Erweiterungen (Stufe 1 und 2) · Quelle: werkzeug/vorlagen/vorrat_plus.js
   Hängt sich über QWVorrat._i (Schnittstelle in vorrat.js) ein: Übersicht, Notfall-Blatt, Vergleich, Kosten, Startvorlage,
   Kalender-Erinnerungen, Strichcode, QR-Übertragung, weitere Bestände, Garten & Eingemachtes.
   Reine Rechnungen stehen unter QWVorrat._plus (für vorrat_test.js). */
(function (root) {
'use strict';
var V = root.QWVorrat; if (!V || !V._i) return;
var I = V._i, K = V._kern, H = I.HAKEN;
var esc = I.esc, fz = I.fz, kg = I.kg, liter = I.liter, zahl = I.zahl, uid = I.uid, klon = I.klon, feld = I.feld, zahlIn = I.zahlIn, seg = I.seg, balken = I.balken, leerText = I.leerText, tageText = I.tageText;
function S() { return I.zustand(); }
function heute() { return I.heute(); }
var MONATE = ['Jan.', 'Feb.', 'März', 'Apr.', 'Mai', 'Juni', 'Juli', 'Aug.', 'Sep.', 'Okt.', 'Nov.', 'Dez.'];
function ym(d) { return d.getFullYear() + '-' + (d.getMonth() < 9 ? '0' : '') + (d.getMonth() + 1); }
function plusMonate(s, n) { var m = /^(\d{4})-(\d{2})$/.exec(s || ''); if (!m) return ''; var t = (+m[1]) * 12 + (+m[2] - 1) + n; return Math.floor(t / 12) + '-' + (t % 12 < 9 ? '0' : '') + (t % 12 + 1); }
/* Läuft die Seite eingebettet (Claude-Artefakt)? Dort sind Drucken und Downloads gesperrt. */
function eingebettet() { if (typeof window === 'undefined') return true; try { return window.self !== window.top; } catch (e) { return true; } }
function druckMoeglich() { return typeof window !== 'undefined' && typeof window.print === 'function' && !eingebettet() && I.dateiMoeglich(); }
function ampelKlasse(a) { return a === 'gruen' ? 'vr-gut' : a === 'gelb' ? 'vr-mittel' : a === 'rot' ? 'vr-schlecht' : 'vr-grau'; }
function stufe(t, z) { return t >= z ? 'gruen' : t >= Math.min(3, z) ? 'gelb' : 'rot'; }
function datei(name, inhalt, typ) {
  var bl = new Blob([inhalt], { type: typ }), url = URL.createObjectURL(bl), a = document.createElement('a');
  a.href = url; a.download = name; document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(url); a.remove(); }, 800);
}
/* Kamera-Scan nur, wo der Browser BarcodeDetector wirklich kann (Safari auf iPhone/iPad: standardmäßig aus – Beleg technik.json) */
var SCAN = [];
if (typeof window !== 'undefined' && 'BarcodeDetector' in window && window.isSecureContext && window.BarcodeDetector.getSupportedFormats) {
  try { window.BarcodeDetector.getSupportedFormats().then(function (L) { SCAN = L || []; }).catch(function () { SCAN = []; }); } catch (e) { SCAN = []; } }
function kannScannen(f) { return typeof navigator !== 'undefined' && navigator.mediaDevices && navigator.mediaDevices.getUserMedia && f.some(function (x) { return SCAN.indexOf(x) >= 0; }); }
var QPLUS = [];  // weitere Quellen für den Abschnitt „Quellen und Stand“
function quelle(t, u, z) { if (!QPLUS.some(function (q) { return q[1] === u; })) { QPLUS.push([t, u, z || '']); I.QUELLEN.push([t, u, z || '']); } }

/* ===================================================================== Startvorlage nach der BLE-Vorratstabelle (Mischkost, © BLE 2024)
   Beispiel-Lebensmittel je Person für 10 Tage bei 2.200 kcal, in g bzw. ml; in Katalog-Lebensmittel übersetzt ([Katalog-ID, Menge, Hinweis]) */
var BLE_VORLAGE = [
  ['getreide', [['vkbrot', 710], ['zwieback', 180], ['knaecke', 710], ['nudeln', 280], ['reis', 180], ['haferflocken', 540], ['kartoffeln', 710]]],
  ['gemuese', [['gr_bohnen', 570], ['erbsen_moehren', 640], ['rotkohl_glas', 500], ['sauerkraut', 500], ['spargel', 290], ['mais', 290], ['pilze_dose', 290], ['gurken', 290], ['rote_bete', 290], ['zwiebeln', 360]]],
  ['obst', [['kirschen', 400], ['birnen', 180], ['pfirsiche', 180, 'statt Aprikosen aus der Dose'], ['mandarinen', 250], ['ananas', 250], ['rosinen', 140], ['haselnuesse', 100], ['pflaumen_getr', 250], ['aepfel', 710, 'Frischobst']]],
  ['milch', [['hmilch', 2000], ['hartkaese', 500]]],
  ['eiweiss', [['thunfisch', 165], ['sardinen', 50], ['makrele', 50, 'statt Heringsfilet'], ['corned_beef', 160], ['leberwurst', 160], ['salami', 160], ['wuerstchen', 160, 'Bockwurst'], ['eier', 265, '5 Eier']]],
  ['fett', [['butter', 180, 'oder Margarine'], ['rapsoel', 138, '0,15 l']]],
  ['trinken', [['wasser', 20000], ['zitronensaft', 140], ['kaffee', 180], ['tee', 90]]]
];
/* faktor = Personen-Äquivalent (Summe kcal / 2.200 oder Zahl der Personen) × Tage / 10 → Liste mit Packungen */
function vorlage(faktor) {
  var L = [];
  BLE_VORLAGE.forEach(function (g) { g[1].forEach(function (e) { var k = K.katVon(S() || {}, e[0]); if (!k) return; var menge = e[1] * faktor, pk = k.p && k.p.length ? k.p[0] : null;
    if (e[0] === 'wasser') pk = k.p[0];
    var anzahl = pk ? Math.max(1, Math.ceil(menge / pk[1] - 0.15)) : null;
    L.push({ g: g[0], id: e[0], n: k.n, menge: menge, pk: pk, anzahl: anzahl, hinweis: e[2] || '', e: pk ? 'p0' : (k.ml ? 'ml' : 'g'), m: pk ? anzahl : Math.round(menge) }); }); });
  return L;
}

/* ===================================================================== Vergleich: 3 · 10 · 28 Tage, „eine Person mehr“ */
var ZUSATZ = { n: 'Zusatzperson', s: 'm', a: 35, t: 'normal' };  // ohne Gewicht → DGE-Richtwert 25–51 Jahre (2.700 kcal bei PAL 1,6)
function fall(St, h, tage) {
  var A = K.alltag(St, h), W = K.wasser(St), Hh = K.haushalt(St), satt = A.max ? 90 : A.reicht;
  var fehltTage = Math.max(0, tage - Math.floor(satt + 1e-9)), wasserZiel = W.bedarf * tage;
  return { tage: tage, essenOk: satt >= tage, satt: satt, wasserOk: W.leitung || W.l >= wasserZiel, wasserL: W.l, wasserZiel: wasserZiel, wasserFehlt: W.leitung ? 0 : Math.max(0, wasserZiel - W.l),
    kcalFehlt: fehltTage * Hh.kcalSpar, fehltTage: fehltTage, personen: Hh.n, kcalTag: Hh.kcalSpar };
}
function vergleich(St, h, mitZusatz) {
  var T = St; if (mitZusatz) { T = klon(St); T.personen.push(Object.assign({ id: 'zusatz' }, ZUSATZ)); }
  return [3, 10, 28].map(function (t) { return fall(T, h, t); });
}

/* ===================================================================== Kosten und Einkauf in Etappen */
/* Einkaufsliste bis zum Ziel: Nachkauf (Mindestbestand) + Lücken je Gruppe (Vorschläge) + Wasser */
function einkauf(St, h) {
  var F = K.fehltListe(St, h), L = [];
  K.nachkauf(St).forEach(function (x) { L.push({ id: x.k.i, n: x.k.n, anzahl: x.anzahl, pk: x.einheit, g: x.g, grund: 'Mindestbestand', prio: 0 }); });
  if (F.wasserL > 0) { var w = K.katVon(St, 'wasser'), p = w.p[0]; L.push({ id: 'wasser', n: w.n, anzahl: Math.ceil(F.wasserL * 1000 / p[1]), pk: p[0], g: F.wasserL * 1000, grund: 'Wasser bis zum Ziel', prio: 1 }); }
  F.gruppen.slice().sort(function (a, b) { return a.ist / a.ziel - b.ist / b.ziel; }).forEach(function (x, i) {
    var ids = (({ getreide: ['nudeln', 'reis'], gemuese: ['linsen', 'kidney_dose'], obst: ['pfirsiche', 'rosinen'], milch: ['hmilch', 'hartkaese'], eiweiss: ['thunfisch', 'wuerstchen'], fett: ['rapsoel', 'butterschmalz'] })[x.g.k] || []);
    ids.forEach(function (id) { var k = K.katVon(St, id); if (!k || !k.p) return; var teil = x.gap / ids.length / (k.x || 1), pk = k.p[0];
      L.push({ id: id, n: k.n, anzahl: Math.max(1, Math.ceil(teil / pk[1])), pk: pk[0], g: Math.max(1, Math.ceil(teil / pk[1])) * pk[1], grund: x.g.kurz + ' bis zum Ziel', prio: 2 + i }); }); });
  L.forEach(function (e) { var k = K.katVon(St, e.id), pj = k ? K.preisJeG(St, k) : null; e.preis = pj != null ? Math.round(e.g * pj * 100) / 100 : null; });
  return L;
}
/* Etappen: in der Reihenfolge der Dringlichkeit, je Woche höchstens „budget“ Euro; Posten ohne Preis stehen extra */
function etappen(L, budget) {
  var mit = L.filter(function (e) { return e.preis != null; }).sort(function (a, b) { return a.prio - b.prio; }), ohne = L.filter(function (e) { return e.preis == null; }), W = [], cur = null;
  if (!(budget > 0)) return { wochen: [], ohne: ohne, summe: mit.reduce(function (s, e) { return s + e.preis; }, 0) };
  mit.forEach(function (e) {
    var rest = e.anzahl, je = e.preis / e.anzahl;
    while (rest > 0) {
      if (!cur || cur.summe + je > budget + 1e-9) { if (cur && !cur.posten.length && je > budget) { cur.posten.push({ n: e.n, pk: e.pk, anzahl: 1, preis: je }); cur.summe += je; rest--; continue; } cur = { summe: 0, posten: [] }; W.push(cur); if (W.length > 104) return { wochen: W, ohne: ohne, summe: NaN, zuViel: true }; }
      var n = Math.min(rest, Math.max(1, Math.floor((budget - cur.summe) / je + 1e-9))); if (cur.summe + je * n > budget + 1e-9 && cur.posten.length) { cur = null; continue; }
      var da = cur.posten.filter(function (p) { return p.n === e.n; })[0]; if (da) { da.anzahl += n; da.preis += je * n; } else cur.posten.push({ n: e.n, pk: e.pk, anzahl: n, preis: je * n });
      cur.summe += je * n; rest -= n;
    }
  });
  return { wochen: W, ohne: ohne, summe: mit.reduce(function (s, e) { return s + e.preis; }, 0) };
}

/* ===================================================================== Kalender-Erinnerung (.ics, RFC 5545) */
function icsText(s) { return String(s).replace(/\\/g, '\\\\').replace(/;/g, '\\;').replace(/,/g, '\\,').replace(/\n/g, '\\n'); }
function icsFalten(z) { var out = [], b = z; while (b.length > 60) { out.push(b.slice(0, 60)); b = " " + b.slice(60); } out.push(b); return out.join('\r\n'); }
function icsDatum(d) { return d.getFullYear() + ('0' + (d.getMonth() + 1)).slice(-2) + ('0' + d.getDate()).slice(-2); }
/* posten: [{n, mhd:'JJJJ-MM', ort}] · vorlauf: Tage vor Monatsende */
function ics(posten, vorlauf, jetzt) {
  jetzt = jetzt || new Date(); vorlauf = vorlauf == null ? 30 : vorlauf;
  var st = jetzt.toISOString().replace(/[-:]/g, '').replace(/\.\d+/, ''), z = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Quellwissen//Vorrats-Planer//DE', 'CALSCALE:GREGORIAN'];
  posten.forEach(function (p, i) { var m = /^(\d{4})-(\d{2})$/.exec(p.mhd || ''); if (!m) return; var ende = new Date(+m[1], +m[2], 0, 12), tag = new Date(ende.getTime() - vorlauf * 86400000), nach = new Date(tag.getTime() + 86400000);
    z.push('BEGIN:VEVENT', 'UID:vorrat-' + (p.u || i) + '-' + m[1] + m[2] + '@quellwissen', 'DTSTAMP:' + st, 'DTSTART;VALUE=DATE:' + icsDatum(tag), 'DTEND;VALUE=DATE:' + icsDatum(nach),
      icsFalten('SUMMARY:' + icsText('Vorrat: ' + p.n + ' läuft ab (MHD ' + MONATE[+m[2] - 1] + ' ' + m[1] + ')')),
      icsFalten('DESCRIPTION:' + icsText('Mindesthaltbarkeitsdatum Ende ' + MONATE[+m[2] - 1] + ' ' + m[1] + (p.ort ? ', Lagerort: ' + p.ort : '') + '. Bald verbrauchen und nachkaufen.')),
      'BEGIN:VALARM', 'ACTION:DISPLAY', 'DESCRIPTION:' + icsText('Vorrat prüfen'), 'TRIGGER:PT9H', 'END:VALARM', 'END:VEVENT'); });
  z.push('END:VCALENDAR'); return z.join('\r\n') + '\r\n';
}

/* ===================================================================== Strichcode (GTIN/EAN) */
function gtinOk(c) { c = String(c || '').replace(/\D/g, ''); if ([8, 12, 13, 14].indexOf(c.length) < 0) return false; var s = 0; for (var i = 0; i < c.length - 1; i++) { var d = +c.charAt(c.length - 2 - i); s += i % 2 ? d : d * 3; } return (10 - s % 10) % 10 === +c.charAt(c.length - 1); }
/* Antwort von Open Food Facts (API v2) in ein eigenes Lebensmittel übersetzen */
function offNachKatalog(code, d) {
  var p = d && d.product; if (!p) return null; var n = p.nutriments || {}, kcal = n['energy-kcal_100g'];
  if (kcal == null && n.energy_100g != null) kcal = n.energy_100g / 4.184;
  var name = [p.product_name_de || p.product_name, p.brands].filter(Boolean).join(' · ').slice(0, 60);
  var menge = /(\d+[.,]?\d*)\s*(g|kg|ml|l)\b/i.exec(p.quantity || ''), pg = null;
  if (menge) { pg = parseFloat(menge[1].replace(',', '.')) * (/^k|^l$/i.test(menge[2]) ? 1000 : 1); }
  return { name: name || ('Artikel ' + code), k: kcal != null ? Math.round(kcal) : null, e: n.proteins_100g, f: n.fat_100g, c: n.carbohydrates_100g, pg: pg, ml: menge && /ml|^l$/i.test(menge[2]) };
}

/* ===================================================================== QR-Übertragung */
var QR_MAX = 1800;  // Zeichen je QR-Code: ein Code fasst höchstens 2.953 Byte (Version 40, Fehlerstufe L, Beleg technik.json) – bewusst Luft für Handy-Kameras
function b64(u8) { var s = ''; for (var i = 0; i < u8.length; i++) s += String.fromCharCode(u8[i]); return btoa(s).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, ''); }
function unb64(t) { t = t.replace(/-/g, '+').replace(/_/g, '/'); while (t.length % 4) t += '='; var s = atob(t), u = new Uint8Array(s.length); for (var i = 0; i < s.length; i++) u[i] = s.charCodeAt(i); return u; }
function zip(text, aus) {
  var u8 = new TextEncoder().encode(text);
  if (typeof CompressionStream === 'undefined' || aus) return Promise.resolve('Z0' + b64(u8));
  var cs = new Blob([u8]).stream().pipeThrough(new CompressionStream('deflate-raw'));
  return new Response(cs).arrayBuffer().then(function (b) { return 'Z1' + b64(new Uint8Array(b)); });
}
function unzip(t) {
  if (t.slice(0, 2) === 'Z0') return Promise.resolve(new TextDecoder().decode(unb64(t.slice(2))));
  if (typeof DecompressionStream === 'undefined') return Promise.reject(new Error('Dieses Gerät kann gepackte Codes nicht entpacken.'));
  var ds = new Blob([unb64(t.slice(2))]).stream().pipeThrough(new DecompressionStream('deflate-raw'));
  return new Response(ds).text();
}
/* Teile: „QWV:1/3:…“ */
function qrTeile(packed) { var n = Math.ceil(packed.length / QR_MAX), L = []; for (var i = 0; i < n; i++) L.push('QWV:' + (i + 1) + '/' + n + ':' + packed.slice(i * QR_MAX, (i + 1) * QR_MAX)); return L; }
function qrZusammen(texte) {
  var T = {}, n = 0; texte.forEach(function (t) { var m = /^QWV:(\d+)\/(\d+):([\s\S]*)$/.exec(String(t).trim()); if (!m) return; T[+m[1]] = m[3].replace(/\s+/g, ''); n = +m[2]; });
  if (!n) return null; var out = ''; for (var i = 1; i <= n; i++) { if (T[i] == null) return { fehlt: i, von: n, da: Object.keys(T).length }; out += T[i]; } return { text: out, von: n };
}
function qrSvg(text) {
  if (!root.QWVorratQR || !root.QWVorratQR.generate) return '';
  var q = root.QWVorratQR.generate(text), n = q.size, d = '';
  for (var r = 0; r < n; r++) for (var c = 0; c < n; c++) if (q.get(c, r)) d += 'M' + c + ',' + r + 'h1v1h-1z';
  return '<svg class="vr-qr" viewBox="-4 -4 ' + (n + 8) + ' ' + (n + 8) + '" role="img" aria-label="QR-Code" shape-rendering="crispEdges"><rect x="-4" y="-4" width="' + (n + 8) + '" height="' + (n + 8) + '" fill="#fff"/><path d="' + d + '" fill="#000"/></svg>';
}
/* kompakte Sicherung ohne Beispiel-Hinweis und ohne leere Felder */
function kompakt(St) { var x = klon(St); delete x.tab; Object.keys(x).forEach(function (k) { var v = x[k]; if (v == null || v === '' || (Array.isArray(v) && !v.length) || (typeof v === 'object' && !Array.isArray(v) && !Object.keys(v).length)) delete x[k]; }); return JSON.stringify(x); }

/* ===================================================================== Weitere Bestände (keine Dosierungen) */
var BKAT = [
  ['apotheke', 'Hausapotheke', '🩹', ['Persönliche Medikamente', 'Schmerzmittel', 'Fiebersenkende Mittel', 'Fieberthermometer', 'Wund- und Hautdesinfektion', 'Pflaster', 'Verbandmaterial', 'Mittel gegen Durchfall', 'Elektrolyte', 'Einmalhandschuhe']],
  ['hygiene', 'Hygiene', '🧻', ['Toilettenpapier', 'Seife', 'Zahnpasta', 'Müllbeutel', 'Feuchttücher', 'Desinfektionsmittel', 'Monatshygiene', 'Haushaltspapier']],
  ['baby', 'Baby & Kleinkind', '🍼', ['Windeln', 'Feuchttücher (Baby)', 'Fläschchen', 'Wundschutzcreme']],
  ['tiere', 'Haustiere', '🐾', ['Tierfutter', 'Katzenstreu', 'Medikamente fürs Tier']],
  ['licht', 'Batterien, Licht, Radio', '🔦', ['Batterien AA', 'Batterien AAA', 'Taschenlampe', 'Stirnlampe', 'Kerzen', 'Teelichter', 'Radio (Batterie/Kurbel)', 'Powerbank']],
  ['brennstoff', 'Brennstoff', '🔥', ['Gaskartuschen', 'Brennpaste', 'Grillkohle', 'Brennholz', 'Feuerzeug / Streichhölzer']]
];
var BK = {}; BKAT.forEach(function (b) { BK[b[0]] = b; });
var BEINH = ['Stück', 'Packung', 'Rollen', 'Flaschen', 'l', 'kg'];
/* Reichweite eines Bestands in Tagen (nur wenn ein Verbrauch je Tag bekannt ist); Gaskartuschen aus Speiseplan und Brenndauer */
function bestandTage(St, b, brennProTag) {
  var m = +b.m || 0, v = zahl(b.verbrauch);
  if (b.kat === 'brennstoff' && /kartusche/i.test(b.n) && !(v > 0)) { var bd = zahl((St.lage || {}).kartusche); if (bd > 0 && brennProTag > 0) v = brennProTag / bd; }
  return v > 0 ? m / v : null;
}
function bestandAmpel(St, b, h, z, brennProTag) {
  var d = I.mhdDatum(b.mhd); if (d && I.tageBis(d, h) < 0) return 'rot';
  var t = bestandTage(St, b, brennProTag); if (t == null) return (+b.m || 0) > 0 ? (d && I.tageBis(d, h) < 30 ? 'gelb' : 'gruen') : 'rot';
  return stufe(t, z);
}
function brennProTag(St, h) { var A = K.alltag(St, h), z = K.zielTage(St), T = A.tage.slice(0, z), m = 0; T.forEach(function (t) { m += t.brenn || 0; }); return T.length ? m / T.length : 0; }

/* ===================================================================== Garten und Eingemachtes */
/* Richtwerte (untere Grenze, Monate): Eingekochtes 6–12 Monate (BZfE „Haltbarkeit von Lebensmitteln“, Stand 20.02.2025);
   Getrocknetes etwa 1 Jahr, Tiefkühl Obst 8–12, Gemüse 6–12, Fleisch 3–12, Brot 1–3, Käse 2–4 Monate (BLE „So können Lebensmittel gelagert werden“) */
var EIGEN_ART = [['eingekocht', 'Eingekocht', function () { return 6; }], ['fermentiert', 'Fermentiert', function () { return null; }], ['getrocknet', 'Getrocknet', function () { return 12; }],
  ['eingefroren', 'Eingefroren', function (k) { return { obst: 8, gemuese: 6, eiweiss: 3, getreide: 1, milch: 2 }[k.g] || 3; }], ['ernte', 'Frische Ernte', function (k) { return k.h ? Math.max(0, Math.floor(k.h / 30)) : null; }]];
var EA = {}; EIGEN_ART.forEach(function (a) { EA[a[0]] = a; });
function eigenMhd(art, k, herg) { var mo = EA[art] ? EA[art][2](k) : null; if (mo == null || !herg) return ''; if (mo === 0) return herg; return plusMonate(herg, mo); }

/* ===================================================================== Ansichten */
var OF = function () { return I.offen(); };

/* ---------- Übersicht mit Ampel-Kacheln ---------- */
function uebersichtHTML() {
  var St = S(), h = heute(), Hh = K.haushalt(St), z = K.zielTage(St), L = St.lage || {};
  var h1 = '<section class="vr-bereich" data-b="uebersicht"><h2>Übersicht</h2>';
  if (!Hh.n) return h1 + I.leerText('Noch niemand im Haushalt – lege zuerst Personen an oder nimm die Startvorlage.', '<button type="button" class="vr-knopf vr-haupt" data-tab="haushalt">Zum Haushalt</button> <button type="button" class="vr-knopf" data-tab="vorlage">Startvorlage</button>') + '</section>';
  var A = K.alltag(St, h), W = K.wasser(St), satt = A.max ? 90 : A.reicht, bpt = brennProTag(St, h);
  var kh = 0, kd = 0; I.CHECK.forEach(function (c) { c[1].forEach(function (t) { kh++; if (St.haken[t]) kd++; }); });
  var kachel = function (id, tab, titel, icon, amp, gross, klein) {
    return '<button type="button" class="vr-ampel ' + ampelKlasse(amp) + '" data-tab="' + tab + '"' + (I.BEREICH[tab] ? '' : ' disabled') + '><span class="vr-ai" aria-hidden="true">' + icon + '</span><span class="vr-at"><span class="vr-fl">' + titel + '</span><b>' + gross + '</b><small>' + klein + '</small></span><i class="vr-adot" aria-label="' + ({ gruen: 'gut', gelb: 'mittel', rot: 'schlecht', '': 'noch offen' })[amp || ''] + '"></i></button>';
  };
  var licht = (St.bestaende || []).filter(function (b) { return b.kat === 'licht' || b.kat === 'brennstoff'; }), lichtAmp = '', lichtTxt = 'Licht, Radio, Brennstoff noch nicht erfasst';
  if (licht.length) { var schlecht = licht.map(function (b) { return bestandAmpel(St, b, h, z, bpt); }); lichtAmp = schlecht.indexOf('rot') >= 0 ? 'rot' : schlecht.indexOf('gelb') >= 0 ? 'gelb' : 'gruen'; lichtTxt = licht.length + ' Posten erfasst'; }
  if (H.uebersichtStrom) { var su = H.uebersichtStrom(St, h, z); if (su) { lichtAmp = su.amp; lichtTxt = su.txt; } }
  var aus = (St.bestaende || []).filter(function (b) { return b.kat === 'apotheke' || b.kat === 'hygiene' || b.kat === 'baby'; }), ausAb = aus.filter(function (b) { var d = I.mhdDatum(b.mhd); return d && I.tageBis(d, h) < 0; }).length;
  var au = H.uebersichtAusruestung ? H.uebersichtAusruestung(St) : null; if (au) { kd = au.d; kh = au.n; }
  var ausAmp = ausAb ? 'rot' : kd / kh >= 0.8 ? 'gruen' : kd / kh >= 0.4 ? 'gelb' : 'rot';
  var nf = H.uebersichtNotfallplan ? H.uebersichtNotfallplan(St) : { amp: '', txt: 'Treffpunkte und Kontakte festlegen' };
  var ab = H.uebersichtAblauf ? H.uebersichtAblauf(St) : { amp: '', txt: 'Was in welcher Stunde zu tun ist' };
  var wg = W.leitung ? 'gruen' : stufe(W.tage, z);
  h1 += '<p class="vr-unter">' + Hh.n + (Hh.n === 1 ? ' Person' : ' Personen') + ' · Ziel ' + z + ' Tage · ' + (L.strom ? 'Strom weg' : 'Strom da') + ' · ' + (L.leitung ? 'Leitungswasser da' : 'kein Leitungswasser') + ' · ' + I.KOCHT[L.koch] + '</p>';
  h1 += '<div class="vr-ampeln">' +
    kachel('essen', 'reichweite', 'Essen', '🥫', stufe(satt, z), (A.max ? '90+' : I.tageZahl(satt)) + ' Tage satt', 'Ziel ' + z + ' Tage' + (A.knapp ? ' · knapp ab Tag ' + A.knapp : '')) +
    kachel('wasser', I.BEREICH.wasser ? 'wasser' : 'reichweite', 'Wasser', '💧', wg, W.leitung ? 'Leitung läuft' : I.tageZahl(W.tage) + ' Tage', liter(W.l) + ' da · ' + liter(W.bedarf) + ' am Tag') +
    kachel('strom', I.BEREICH.strom ? 'strom' : 'bestaende', 'Strom & Wärme', '🔋', lichtAmp, lichtAmp ? ({ gruen: 'gut versorgt', gelb: 'knapp', rot: 'fehlt' })[lichtAmp] : 'noch offen', lichtTxt) +
    kachel('ausr', 'bestaende', 'Ausrüstung & Apotheke', '🩹', ausAmp, kd + ' von ' + kh + ' abgehakt', ausAb ? ausAb + ' Posten abgelaufen' : 'Checkliste nach BBK') +
    kachel('plan', I.BEREICH.notfallplan ? 'notfallplan' : 'blatt', 'Notfallplan', '📞', nf.amp, nf.gross || (nf.amp ? ({ gruen: 'steht', gelb: 'angefangen', rot: 'fehlt' })[nf.amp] : 'noch offen'), nf.txt) +
    kachel('ablauf', I.BEREICH.ablauf ? 'ablauf' : 'reichweite', 'Ablauf', '⏱', ab.amp, ab.gross || (ab.amp ? ({ gruen: 'erledigt', gelb: 'begonnen', rot: 'offen' })[ab.amp] : 'Stunde 0 bis Tag 10'), ab.txt) + '</div>';
  /* schnelle Wege */
  var NK = K.nachkauf(St), X = K.posten(St, h), bald = X.filter(function (x) { return x.rest != null && x.rest < 30; }).length;
  h1 += '<h3>Als Nächstes</h3><div class="vr-wege">' +
    weg('fehlt', '🛒', 'Fehlt noch', (NK.length ? NK.length + ' unter Mindestbestand · ' : '') + 'Einkaufsliste bis zum Ziel') +
    weg('gerichte', '🍲', 'Speiseplan', 'Was ihr aus dem Vorrat kochen könnt') +
    (bald ? weg('haltbar', '📅', bald + ' Posten laufen bald ab', 'zuerst verbrauchen') : '') +
    weg('blatt', '🖨', 'Notfall-Blatt', 'Alles Wichtige auf Papier') +
    weg('vergleich', '⚖', '3 · 10 · 28 Tage', 'Fälle vergleichen, eine Person mehr') +
    (St.lager.length < 5 ? weg('vorlage', '📋', 'Startvorlage', 'Vorrat nach der BLE-Tabelle vorschlagen lassen') : '') + '</div>';
  h1 += '<p class="vr-klein">Grün = Ziel erreicht, Gelb = knapp, Rot = fehlt, Grau = noch nicht erfasst. Antippen öffnet den Bereich.</p>';
  return h1 + '</section>';
}
function weg(tab, i, t, s) { return I.BEREICH[tab] ? '<button type="button" class="vr-weg" data-tab="' + tab + '"><span aria-hidden="true">' + i + '</span><span><b>' + esc(t) + '</b><small>' + esc(s) + '</small></span><span aria-hidden="true">›</span></button>' : ''; }

/* ---------- Notfall-Blatt ---------- */
var NUMMERN = [['112', 'Feuerwehr und Rettungsdienst (bundesweit)'], ['110', 'Polizei (bundesweit)'], ['116 117', 'Ärztlicher Bereitschaftsdienst (bundesweit)']];
function blattInhalt() {
  var St = S(), h = heute(), Hh = K.haushalt(St), z = K.zielTage(St), A = K.alltag(St, h), W = K.wasser(St), X = K.posten(St, h);
  var d = h.toLocaleDateString('de-DE', { day: 'numeric', month: 'long', year: 'numeric' }), P = I.planZiel();
  var tab = function (kopf, zeilen) { return '<table class="vr-dt"><thead><tr>' + kopf.map(function (k) { return '<th>' + k + '</th>'; }).join('') + '</tr></thead><tbody>' + zeilen.map(function (z) { return '<tr>' + z.map(function (c) { return '<td>' + c + '</td>'; }).join('') + '</tr>'; }).join('') + '</tbody></table>'; };
  var h1 = '<div class="vr-blatt"><header class="vr-bk"><h1>Notfall-Blatt</h1><p>Stand ' + esc(d) + ' · Vorrat &amp; Blackout-Planer (Quellwissen)</p></header>';
  var nummern = H.blattNummern ? H.blattNummern(St) : NUMMERN.map(function (n) { return [esc(n[0]), esc(n[1])]; });
  h1 += '<section><h2>Wichtige Nummern</h2>' + tab(['Nummer', 'Wofür'], nummern) + '</section>';
  if (H.blattNotfallplan) h1 += H.blattNotfallplan(St);
  h1 += '<section><h2>Haushalt</h2>' + tab(['Person', 'Alter', 'kcal am Tag', 'Eiweiß'], Hh.P.map(function (x) { return [esc(x.p.n || '–'), esc(x.p.a || '–'), fz(x.b.kcal), fz(x.b.eiweiss) + ' g']; })) +
    (St.tiere.length ? '<p>Haustiere: ' + St.tiere.map(function (t) { return esc(t.n || 'Tier') + (t.futter ? ' (' + esc(t.futter) + ' g Futter am Tag)' : ''); }).join(', ') + '</p>' : '') +
    '<p><b>Reicht:</b> Essen ' + esc(A.max ? 'über 90 Tage' : tageText(A.reicht)) + ' satt · Wasser ' + esc(W.leitung ? 'Leitung läuft' : tageText(W.tage)) + ' (' + liter(W.l) + ' da, ' + liter(W.bedarf) + ' am Tag) · Ziel ' + z + ' Tage · Kochstelle: ' + esc(I.KOCHT[(St.lage || {}).koch]) + '</p></section>';
  if (H.blattRegion) h1 += H.blattRegion(St);
  if (H.blattAblauf) h1 += H.blattAblauf(St);
  h1 += '<section><h2>Vorrat (' + X.length + ' Posten)</h2>' + tab(['Lebensmittel', 'Menge', 'MHD', 'Ort'], X.slice().sort(function (a, b) { return a.k.g.localeCompare(b.k.g) || a.k.n.localeCompare(b.k.n, 'de'); }).map(function (x) {
    return [esc(x.it.n || x.k.n), fz(+x.it.m || 0, 2) + ' × ' + esc(I.einheitT(x.k, x.it.e).replace(/ \(.*\)$/, '')), esc(I.mhdText(x.it.mhd) || '–'), esc(K.ortName(St, x.it.o))]; })) + '</section>';
  if (P.tage.length) h1 += '<section><h2>Speiseplan (' + P.tage.length + ' Tage' + (P.sparsam ? ', sparsam' : '') + ')</h2>' + tab(['Tag', 'Mahlzeiten', 'gedeckt'], P.tage.map(function (t) {
    return ['Tag ' + t.d, t.essen.map(function (e) { return esc(e.n); }).join(' · ') + (t.extra.length ? ' · dazu ' + t.extra.map(function (x) { return esc(x.n.replace(/ \(.*\)$/, '')); }).join(', ') : '') || 'nichts mehr da', fz(Math.min(999, t.deckung * 100)) + ' %']; })) + '</section>';
  var B = St.bestaende || []; if (B.length) h1 += '<section><h2>Ausrüstung und Apotheke</h2>' + tab(['Was', 'Menge', 'Ablauf'], B.map(function (b) { return [esc(b.n), fz(+b.m || 0, 2) + ' ' + esc(b.e || ''), esc(I.mhdText(b.mhd) || '–')]; })) + '</section>';
  h1 += '<section><h2>Checkliste (BBK)</h2><div class="vr-dcheck">' + I.CHECK.map(function (c) { return '<div><h3>' + esc(c[0]) + '</h3><ul>' + c[1].map(function (t) { return '<li>' + (St.haken[t] ? '☑' : '☐') + ' ' + esc(t) + '</li>'; }).join('') + '</ul></div>'; }).join('') + '</div></section>';
  h1 += '<footer><p>Richtwerte ohne Gewähr. Wasser: 2 l je Person und Tag, davon 0,5 l zum Kochen (BBK-Ratgeber, Stand 11/2025). Gaskocher mit Kartusche nur im Freien, außer für Innenräume zugelassen.</p></footer></div>';
  return h1;
}
/* Kurzfassung: alles Wichtige auf einer A4-Seite (zweispaltig) */
function blattKurz() {
  var St = S(), h = heute(), Hh = K.haushalt(St), z = K.zielTage(St), A = K.alltag(St, h), W = K.wasser(St), L = St.lage || {};
  var d = h.toLocaleDateString('de-DE', { day: 'numeric', month: 'long', year: 'numeric' });
  var nummern = H.blattNummern ? H.blattNummern(St) : NUMMERN.map(function (n) { return [esc(n[0]), esc(n[1])]; }), schon = {};
  nummern = nummern.filter(function (n) { var k = String(n[0]).replace(/\D/g, ''); if (schon[k]) return false; schon[k] = 1; return true; });
  var h1 = '<div class="vr-blatt vr-kurz"><header class="vr-bk"><h1>Notfall-Blatt</h1><p>Stand ' + esc(d) + ' · ' + Hh.n + (Hh.n === 1 ? ' Person' : ' Personen') + (St.tiere.length ? ' · ' + St.tiere.length + (St.tiere.length === 1 ? ' Tier' : ' Tiere') : '') + ' · Kurzfassung</p></header><div class="vr-kspalten">';
  h1 += '<section><h2>Nummern</h2><table class="vr-dt vr-knr"><tbody>' + nummern.map(function (n) { return '<tr><td><b>' + n[0] + '</b></td><td>' + n[1] + '</td></tr>'; }).join('') + '</tbody></table></section>';
  h1 += '<section><h2>Vorrat reicht</h2><p class="vr-kgross">Essen: <b>' + esc(A.max ? 'über 90 Tage' : tageText(A.reicht)) + '</b> · Wasser: <b>' + esc(W.leitung ? 'Leitung läuft' : tageText(W.tage)) + '</b></p><p>' + liter(W.l) + ' Wasser da, ' + liter(W.bedarf) + ' am Tag · Ziel ' + z + ' Tage · Kochstelle: ' + esc(I.KOCHT[L.koch]) + '</p>' +
    (Hh.P.length ? '<p>' + Hh.P.map(function (x) { return esc(x.p.n || 'Person') + (x.p.a ? ' (' + esc(x.p.a) + ')' : ''); }).join(', ') + '</p>' : '') + '</section>';
  if (H.blattNotfallplan) h1 += H.blattNotfallplan(St);
  if (H.blattKurzRegion) h1 += H.blattKurzRegion(St);
  if (H.blattErsteStunde) h1 += H.blattErsteStunde(St);
  h1 += '</div><footer><p>Wasser: 2 l je Person und Tag (BBK-Ratgeber, Stand 11/2025). Gaskocher mit Kartusche nur im Freien, außer für Innenräume zugelassen. Kein Ersatz für Anweisungen der Behörden – Radio und Warn-App beachten. Ausführliche Fassung mit Vorrat, Speiseplan und Checkliste im Planer.</p></footer></div>';
  return h1;
}
function blattAktuell() { return OF().blattLang ? blattInhalt() : blattKurz(); }
function blattHTML() {
  var ok = druckMoeglich();
  return '<section class="vr-bereich" data-b="blatt"><h2>Notfall-Blatt</h2><p class="vr-unter">Alles Wichtige auf einem Blatt Papier – für den Fall, dass Handy und Strom ausfallen. Am besten ausdrucken und zu den Dokumenten legen; nach größeren Änderungen neu drucken.</p>' +
    (ok ? '<div class="vr-knoepfe"><button type="button" class="vr-knopf vr-haupt" data-drucken>🖨 Drucken / als PDF sichern</button></div><p class="vr-klein">Im Druckfenster „Als PDF sichern“ bzw. „PDF“ wählen, wenn kein Drucker da ist. A4, schwarz-weiß.</p>'
      : '<p class="vr-warn">In dieser Vorschau kann nicht gedruckt werden. Öffne den Planer in der installierten App (oder im Browser) und tippe dort auf „Drucken / als PDF sichern“. Bis dahin: Bildschirmfotos dieser Ansicht machen.</p>') +
    '<div class="vr-seg" role="group" aria-label="Umfang"><button type="button" data-blatt="kurz" aria-pressed="' + !OF().blattLang + '">Kurz · 1 Seite</button><button type="button" data-blatt="lang" aria-pressed="' + !!OF().blattLang + '">Ausführlich</button></div>' +
    '<div class="vr-blatt-vorschau">' + blattAktuell() + '</div></section>';
}
function drucken() {
  var alt = document.getElementById('vr-druck'); if (alt) alt.remove();
  var d = document.createElement('div'); d.id = 'vr-druck'; d.innerHTML = blattAktuell(); document.body.appendChild(d);
  document.documentElement.classList.add('vr-drucken');
  var fertig = function () { document.documentElement.classList.remove('vr-drucken'); var x = document.getElementById('vr-druck'); if (x) x.remove(); window.removeEventListener('afterprint', fertig); };
  window.addEventListener('afterprint', fertig);
  try { window.print(); } catch (e) { I.toast('Drucken ging nicht.'); }
  setTimeout(function () { if (!window.matchMedia || !matchMedia('print').matches) fertig(); }, 60000);
}

/* ---------- Vergleich ---------- */
function vergleichHTML() {
  var St = S(), h = heute(), O = OF(), mit = !!O.zusatz;
  if (!St.personen.length) return '<section class="vr-bereich" data-b="vergleich"><h2>Fälle vergleichen</h2>' + leerText('Lege zuerst Personen an.') + '</section>';
  var F = vergleich(St, h, mit), kosten = function (f) { return f.wasserFehlt > 0 ? Math.ceil(f.wasserFehlt / 1.5) + ' Fl. à 1,5 l' : '–'; };
  return '<section class="vr-bereich" data-b="vergleich"><h2>Fälle vergleichen</h2><p class="vr-unter">Reicht euer Vorrat für 3 Tage, 10 Tage oder 4 Wochen? Gerechnet mit eurer Lage (' + esc(I.KOCHT[(St.lage || {}).koch]) + ', ' + ((St.lage || {}).strom ? 'Strom weg' : 'Strom da') + ').</p>' +
    seg('vg:zusatz', [['0', 'So wie wir sind'], ['1', 'Eine Person mehr']], mit ? '1' : '0') +
    (mit ? '<p class="vr-klein">Zusatzperson: Erwachsene(r) ohne Angaben zu Gewicht – gerechnet mit dem DGE-Richtwert 2.700 kcal am Tag (Mann, 25 bis unter 51 Jahre, PAL 1,6), 2 l Wasser.</p>' : '') +
    '<div class="vr-faelle">' + F.map(function (f) { var ok = f.essenOk && f.wasserOk;
      return '<div class="vr-karte vr-fall ' + (ok ? 'vr-gut' : f.essenOk || f.wasserOk ? 'vr-mittel' : 'vr-schlecht') + '"><h3>' + (f.tage === 28 ? '4 Wochen' : f.tage + ' Tage') + '</h3><p class="vr-klein">' + f.personen + ' Personen · ' + fz(f.kcalTag) + ' kcal am Tag</p>' +
        '<dl><dt>Essen</dt><dd class="' + (f.essenOk ? 'vr-ja' : 'vr-nein') + '">' + (f.essenOk ? '✓ reicht' : '✗ ' + I.tageZahl(f.satt) + ' von ' + f.tage + ' Tagen') + '</dd>' +
        (f.fehltTage ? '<dt>Es fehlen</dt><dd>' + f.fehltTage + ' Tage ≈ ' + fz(f.kcalFehlt) + ' kcal</dd>' : '') +
        '<dt>Wasser</dt><dd class="' + (f.wasserOk ? 'vr-ja' : 'vr-nein') + '">' + (f.wasserOk ? '✓ reicht' : '✗ ' + liter(f.wasserL) + ' von ' + liter(f.wasserZiel)) + '</dd>' +
        (f.wasserFehlt > 0 ? '<dt>Wasser fehlt</dt><dd>' + kosten(f) + '</dd>' : '') + '</dl></div>'; }).join('') + '</div>' +
    '<p class="vr-klein">„Essen“ zählt die satten Tage aus dem Speiseplan (wie „Essen reicht“). 4 Wochen sind deutlich mehr als die 10 Tage, die der BBK empfiehlt – sinnvoll, wenn ihr länger vorsorgen wollt.</p></section>';
}

/* ---------- Kosten ---------- */
function kostenHTML() {
  var St = S(), h = heute(), L = einkauf(St, h), b = zahl(St.budget), E = etappen(L, b), z = K.zielTage(St);
  var h1 = '<section class="vr-bereich" data-b="kosten"><h2>Kosten und Einkauf in Etappen</h2><p class="vr-unter">Was kostet der fehlende Vorrat bis zum Ziel von ' + z + ' Tagen? Preise trägst du selbst ein – sie bleiben auf dem Gerät.</p>';
  if (!L.length) return h1 + '<p class="vr-ok">Es fehlt nichts bis zum Ziel.</p></section>';
  h1 += '<div class="vr-karte"><ul class="vr-kliste" role="list">' + L.map(function (e) { var k = K.katVon(St, e.id);
    return '<li><span><b>' + esc(e.n) + '</b><small>' + e.anzahl + ' × ' + esc(String(e.pk).replace(/ \(.*\)$/, '')) + ' · ' + esc(e.grund) + '</small></span>' + zahlIn('data-preis="' + esc(e.id) + '" aria-label="Preis je ' + esc(I.einheitT(k, I.stdEinheit(k))) + '"', (St.preise || {})[e.id] || '', '€ je ' + esc(I.einheitT(k, I.stdEinheit(k)).replace(/ \(.*\)$/, '').replace(/^Packung /, 'Pck. ')), 'Preis') +
      '<b class="vr-kpreis">' + (e.preis != null ? fz(e.preis, 2) + ' €' : '–') + '</b></li>'; }).join('') + '</ul>' +
    '<p class="vr-summe-k">Zusammen: <b>' + fz(E.summe, 2) + ' €</b>' + (E.ohne.length ? ' <small>+ ' + E.ohne.length + ' Posten ohne Preis</small>' : '') + '</p></div>';
  h1 += '<h3>In Etappen einkaufen</h3><div class="vr-karte">' + feld('Betrag je Woche', zahlIn('data-budget', St.budget || '', '€', 'z. B. 20')) +
    (b > 0 ? (E.zuViel ? '<p class="vr-warn">Mit diesem Betrag dauert es über 2 Jahre – lieber einen höheren Betrag wählen.</p>' : '<ol class="vr-wochen">' + E.wochen.map(function (w, i) { return '<li><b>Woche ' + (i + 1) + '</b> <small>' + fz(w.summe, 2) + ' €</small><span>' + w.posten.map(function (p) { return p.anzahl + ' × ' + esc(p.n.replace(/ \(.*\)$/, '')); }).join(', ') + '</span></li>'; }).join('') + '</ol>' +
      '<p class="vr-klein">' + E.wochen.length + ' Wochen. Reihenfolge: zuerst was unter dem Mindestbestand ist, dann Wasser, dann die Gruppen mit der größten Lücke.</p>') : '<p class="vr-klein">Trage einen Betrag ein – dann teilt der Planer den Einkauf auf Wochen auf.</p>') +
    (E.ohne.length ? '<p class="vr-klein">Ohne Preis (nicht eingeplant): ' + E.ohne.map(function (e) { return esc(e.n.replace(/ \(.*\)$/, '')); }).join(', ') + '.</p>' : '') + '</div>';
  return h1 + '<p class="vr-klein">Mengen nach der BLE-Vorratstabelle, umgerechnet auf euren Bedarf; Vorschläge sind Beispiele. Keine Preise oder Läden im Programm – nur deine eigenen Angaben.</p></section>';
}

/* ---------- Startvorlage ---------- */
function vorlageHTML() {
  var St = S(), O = OF(), Hh = K.haushalt(St), z = K.zielTage(St);
  var art = O.vlArt || (Hh.n ? 'haushalt' : 'personen'), n = +O.vlN || Math.max(1, Hh.n || 2), t = +O.vlT || z;
  var faktor = (art === 'haushalt' && Hh.kcal > 0 ? Hh.kcal / 2200 : n) * t / 10, L = vorlage(faktor), weg = O.vlWeg || {};
  var h1 = '<section class="vr-bereich" data-b="vorlage"><h2>Startvorlage</h2><p class="vr-unter">Ein fertiger Vorschlag nach der Vorratstabelle der BLE (Mischkost, je Person für 10 Tage bei 2.200 kcal) – in übliche Packungen umgerechnet. Haken weg, was ihr nicht wollt, dann übernehmen und anpassen.</p>' +
    '<div class="vr-karte"><div class="vr-felder">' + feld('Rechnen für', seg('vl:art', [['haushalt', 'Unseren Haushalt'], ['personen', 'Personen']], art), 'vr-voll') +
    (art === 'personen' ? feld('Personen', zahlIn('data-vl="n"', n, '', '', 'numeric')) : '<p class="vr-klein vr-voll">' + Hh.n + ' Personen mit zusammen ' + fz(Hh.kcal) + ' kcal am Tag = ' + fz(Hh.kcal / 2200, 1) + '-mal die Menge für eine Person.</p>') +
    feld('Tage', zahlIn('data-vl="t"', t, '', '', 'numeric')) + '</div></div>';
  K.GRUPPEN.forEach(function (g) { var G = L.filter(function (e) { return e.g === g.k; }); if (!G.length) return;
    h1 += '<h3>' + g.i + ' ' + esc(g.n) + '</h3><ul class="vr-vliste" role="list">' + G.map(function (e) {
      return '<li><label><input type="checkbox" data-vlweg="' + e.id + '"' + (weg[e.id] ? '' : ' checked') + '><span><b>' + (e.pk ? e.anzahl + ' × ' : '') + esc(e.n) + '</b><small>' + (e.pk ? esc(e.pk[0]) + ' · ' : '') + (e.id === 'wasser' || e.id === 'hmilch' || e.id === 'zitronensaft' ? liter(e.menge / 1000) : kg(e.menge)) + ' laut Tabelle' + (e.hinweis ? ' · ' + esc(e.hinweis) : '') + '</small></span></label></li>'; }).join('') + '</ul>'; });
  h1 += '<div class="vr-knoepfe"><button type="button" class="vr-knopf vr-haupt" data-vl-uebernehmen>Ausgewählte ins Lager übernehmen</button></div>' +
    '<p class="vr-klein">Quelle: BLE, Vorratstabelle Mischkost (ernaehrungsvorsorge.de, © BLE 2024); Hering und Aprikosen sind durch ähnliche Lebensmittel aus dem Katalog ersetzt. Datum (MHD) trägst du nach dem Einkauf im Lager nach.</p></section>';
  return h1;
}

/* ---------- Bestände (Ausrüstung, Apotheke …) ---------- */
function bestaendeHTML() {
  var St = S(), h = heute(), z = K.zielTage(St), bpt = brennProTag(St, h), O = OF();
  var h1 = '<section class="vr-bereich" data-b="bestaende"><h2>Ausrüstung &amp; Apotheke</h2><p class="vr-unter">Was außer Essen da ist – mit Ablaufdatum und, wenn du einen Verbrauch je Tag einträgst, mit Reichweite.</p>' +
    '<p class="vr-warn">Hausapotheke: Hier steht nur, was da ist und wann es abläuft – keine Dosierungen. Einnahme nach Packungsbeilage oder ärztlichem Rat.</p>';
  BKAT.forEach(function (b) { var L = (St.bestaende || []).filter(function (x) { return x.kat === b[0]; }), offen = O['bk:' + b[0]] != null ? O['bk:' + b[0]] : !!L.length;
    var amps = L.map(function (x) { return bestandAmpel(St, x, h, z, bpt); }), amp = !L.length ? '' : amps.indexOf('rot') >= 0 ? 'rot' : amps.indexOf('gelb') >= 0 ? 'gelb' : 'gruen';
    h1 += '<details class="vr-bk-gr" data-bk="' + b[0] + '"' + (offen ? ' open' : '') + '><summary><span aria-hidden="true">' + b[2] + '</span>' + esc(b[1]) + ' <i class="vr-amp ' + (amp ? 'vr-amp-' + amp : 'vr-amp-leer') + '"></i><span class="vr-zaehl">' + L.length + '</span></summary>' +
      (L.length ? '<ul class="vr-liste" role="list">' + L.map(function (x) { var t = bestandTage(St, x, bpt), d = I.mhdDatum(x.mhd), r = d ? I.tageBis(d, h) : null;
        return '<li class="vr-posten vr-bposten" data-bu="' + esc(x.u) + '"><div class="vr-pk"><b><i class="vr-amp vr-amp-' + bestandAmpel(St, x, h, z, bpt) + '"></i>' + esc(x.n) + '</b><span>' + (t != null ? 'reicht ' + tageText(t) : 'Verbrauch eintragen für Reichweite') + (r != null ? (r < 0 ? ' · abgelaufen' : ' · läuft in ' + r + ' T. ab') : '') + '</span></div>' +
          '<div class="vr-pm"><button type="button" class="vr-rund" data-bminus aria-label="weniger">−</button><span class="vr-ein vr-menge"><input type="text" inputmode="decimal" data-bf="m" value="' + esc(String(x.m == null ? '' : x.m).replace('.', ',')) + '" aria-label="Menge"></span><button type="button" class="vr-rund" data-bplus aria-label="mehr">＋</button>' +
          '<select data-bf="e" aria-label="Einheit">' + BEINH.map(function (e) { return '<option' + (e === x.e ? ' selected' : '') + '>' + e + '</option>'; }).join('') + '</select></div>' +
          '<div class="vr-pd">' + I.mhdSel({ mhd: x.mhd }) + feld('Verbrauch je Tag', zahlIn('data-bf="verbrauch"', x.verbrauch || '', esc(x.e || ''), /kartusche/i.test(x.n) ? 'aus Speiseplan' : 'leer = offen')) + '<button type="button" class="vr-x" data-bweg aria-label="entfernen">✕</button></div></li>'; }).join('') + '</ul>' : '<p class="vr-klein">Noch nichts eingetragen.</p>') +
      '<div class="vr-chips">' + b[3].filter(function (n) { return !L.some(function (x) { return x.n === n; }); }).map(function (n) { return '<button type="button" class="vr-chip" data-badd="' + b[0] + '" data-n="' + esc(n) + '">＋ ' + esc(n) + '</button>'; }).join('') + '</div>' +
      '<div class="vr-pm vr-beigen"><span class="vr-ein"><input type="text" data-bneu="' + b[0] + '" placeholder="Eigener Eintrag" maxlength="40"></span><button type="button" class="vr-knopf" data-badd="' + b[0] + '">Hinzufügen</button></div>' +
      (b[0] === 'brennstoff' ? '<p class="vr-klein">Gaskartuschen: Ohne eigenen Verbrauch rechnet der Planer mit den Kochzeiten aus dem Speiseplan (' + fz(bpt) + ' Minuten am Tag) und der Brenndauer unter „Haushalt → Lage“' + (zahl((St.lage || {}).kartusche) > 0 ? ' (' + fz(zahl(St.lage.kartusche)) + ' Minuten je Kartusche)' : ' – dort noch eintragen') + '. Schätzung.</p>' : '') + '</details>'; });
  return h1 + (H.bestaendeUnten ? H.bestaendeUnten() : '<p class="vr-klein">Die Abhak-Liste nach dem BBK-Ratgeber steht unter „Vorrat → Fehlt noch“.</p>') + '</section>';
}

/* ---------- Lager: Strichcode, Garten, Erinnerungen ---------- */
function strichcodeHTML() {
  var O = OF(), sc = O.sc || {}, kamera = kannScannen(['ean_13', 'ean_8', 'upc_a']);
  var h1 = '<details class="vr-mehr vr-strich"' + (sc.offen ? ' open' : '') + '><summary>Mit Strichcode erfassen</summary><div class="vr-karte">' +
    '<div class="vr-pm"><span class="vr-ein"><input type="text" inputmode="numeric" id="vr-ean" placeholder="Nummer unter dem Strichcode, z. B. 4000400000000" value="' + esc(sc.code || '') + '" autocomplete="off"></span><button type="button" class="vr-knopf vr-haupt" data-ean-los>Suchen</button></div>' +
    (kamera ? '<div class="vr-knoepfe"><button type="button" class="vr-knopf" data-ean-kamera>📷 Mit der Kamera scannen</button></div>' : '<p class="vr-klein">Scannen mit der Kamera kann dieser Browser nicht (z. B. Safari auf iPhone und iPad) – bitte die Nummer unter dem Strichcode abtippen.</p>') +
    '<div class="vr-ean-video"></div><div class="vr-ean-erg" aria-live="polite">' + (sc.erg || '') + '</div>' +
    '<p class="vr-klein">Bekannte Nummern merkt sich der Planer auf diesem Gerät. Nachschlagen bei Open Food Facts geht nur mit Internet und nur, wenn du auf den Knopf tippst (Open Food Facts erlaubt höchstens 15 Abrufe je Minute); ohne Netz bleibt alles andere benutzbar.</p></div></details>';
  return h1;
}
function gartenHTML() {
  var O = OF(), g = O.ga || { art: 'eingekocht' }, St = S(), basis = g.basis ? K.katVon(St, g.basis) : null;
  var K2 = I.KATALOG.filter(function (k) { return ['gemuese', 'obst', 'eiweiss', 'getreide', 'milch'].indexOf(k.g) >= 0; });
  var herg = g.herg || ym(heute()), mhd = basis ? eigenMhd(g.art, basis, herg) : '';
  return '<details class="vr-mehr vr-garten"' + (g.offen ? ' open' : '') + '><summary>Eigenes aus Garten und Küche einbuchen</summary><div class="vr-karte">' +
    '<p class="vr-klein">Eingekochtes, Fermentiertes, Getrocknetes, Eingefrorenes oder frische Ernte. Die Nährwerte nimmt der Planer vom ähnlichsten Lebensmittel aus dem Katalog.</p>' +
    seg('ga:art', EIGEN_ART.map(function (a) { return [a[0], a[1]]; }), g.art, 'vr-seg-wrap') +
    '<div class="vr-felder">' + feld('Was ist drin? (ähnlichstes Lebensmittel)', '<select data-ga="basis"><option value="">bitte wählen</option>' + K.GRUPPEN.filter(function (gr) { return K2.some(function (k) { return k.g === gr.k; }); }).map(function (gr) {
      return '<optgroup label="' + esc(gr.kurz) + '">' + K2.filter(function (k) { return k.g === gr.k; }).map(function (k) { return '<option value="' + k.i + '"' + (g.basis === k.i ? ' selected' : '') + '>' + esc(k.n) + '</option>'; }).join('') + '</optgroup>'; }).join('') + '</select>', 'vr-voll') +
    feld('Name (freiwillig)', '<span class="vr-ein"><input type="text" data-ga="name" maxlength="50" value="' + esc(g.name || '') + '" placeholder="z. B. Bohnen aus dem Garten"></span>', 'vr-voll') +
    feld('Gläser / Beutel', zahlIn('data-ga="anzahl"', g.anzahl || '', 'Stück', '1', 'numeric')) + feld('Inhalt je Stück', zahlIn('data-ga="inhalt"', g.inhalt || '', 'g', 'z. B. 400', 'numeric')) +
    feld('Hergestellt / geerntet', monatJahr('ga-herg', herg)) + '</div>' +
    '<p class="vr-klein">' + (!basis ? 'Wähle das ähnlichste Lebensmittel – dann rechnet der Planer Nährwerte und Haltbarkeit.' : mhd ? 'Haltbar etwa bis <b>' + I.mhdText(mhd) + '</b> (Richtwert, untere Grenze: ' + esc(artQuelle(g.art)) + '). Das Datum kannst du danach im Lager ändern.' : 'Für „' + esc(EA[g.art][1]) + '“ gibt es keinen belegten Richtwert – trage das Datum danach im Lager selbst ein.') + '</p>' +
    '<div class="vr-knoepfe"><button type="button" class="vr-knopf vr-haupt" data-ga-buchen>Ins Lager buchen</button></div>' +
    '<p class="vr-klein">Mehr dazu in der App: <a href="#s-einfrieren-lagerdauer">Einfrieren – Lagerdauer</a> · <a href="#s-trocknen">Kräuter trocknen</a> · <a href="#r-sauerkraut">Sauerkraut selber machen</a> · <a href="#s-kueche-reste">Küchenwissen – Reste</a></p></div></details>';
}
function artQuelle(a) { return a === 'eingekocht' ? 'Eingekochtes 6–12 Monate, BZfE' : a === 'getrocknet' ? 'Trockenobst und -gemüse etwa 1 Jahr, BLE' : a === 'eingefroren' ? 'Tiefkühl-Richtwerte der BLE' : 'übliche Haltbarkeit aus dem Katalog'; }
function monatJahr(id, wert) { var m = /^(\d{4})-(\d{2})$/.exec(wert || ''), y0 = new Date().getFullYear(), J = []; for (var y = y0 - 3; y <= y0 + 1; y++) J.push(y);
  return '<span class="vr-mhd" data-mj="' + id + '"><select data-mjm aria-label="Monat">' + MONATE.map(function (t, i) { return '<option value="' + (i + 1) + '"' + (m && +m[2] === i + 1 ? ' selected' : '') + '>' + t + '</option>'; }).join('') + '</select><select data-mjj aria-label="Jahr">' + J.map(function (y) { return '<option' + (m && +m[1] === y ? ' selected' : '') + '>' + y + '</option>'; }).join('') + '</select></span>'; }
function erinnerungHTML() {
  var St = S(), n = St.lager.filter(function (it) { return it.mhd; }).length, ok = I.dateiMoeglich();
  return '<details class="vr-mehr vr-erinn"><summary>Erinnerungen vor dem Ablaufdatum (Kalender)</summary><div class="vr-karte">' + (ok ?
    '<p class="vr-klein">Eine Kalender-Datei (.ics) mit einem Termin je Posten – ' + fz(+(St.erinnVorlauf || 30)) + ' Tage vor Monatsende des MHD, mit Hinweis um 9 Uhr. Auf iPhone/iPad öffnet sie der Kalender, auf Android die Kalender-App.</p>' +
    '<div class="vr-felder">' + feld('Vorlauf', zahlIn('data-erinn', St.erinnVorlauf || 30, 'Tage', '30', 'numeric')) + '</div><div class="vr-knoepfe"><button type="button" class="vr-knopf vr-haupt" data-ics-alle' + (n ? '' : ' disabled') + '>Alle ' + n + ' als Kalender-Datei</button><button type="button" class="vr-knopf" data-ics-text' + (n ? '' : ' disabled') + '>Termine als Text kopieren</button></div><p class="vr-klein">Einzeln: im Posten unter „Mindestbestand, Preis …“. iPhone/iPad: Datei öffnen und „Zum Kalender hinzufügen“ – ob die Erinnerung aus der Datei übernommen wird, kann je nach Weg abweichen. Android: Google Kalender übernimmt .ics-Dateien laut Google-Hilfe nur am Computer über die Kalender-Webseite – am Handy die Termine lieber von Hand anlegen („als Text kopieren“).</p>'
    : '<p class="vr-warn">In dieser Vorschau gehen keine Dateien. In der installierten App kannst du hier Kalender-Erinnerungen (.ics) speichern.</p>') + '</div></details>';
}

/* ---------- QR in der Sicherung ---------- */
function qrHTML() {
  var O = OF(), q = O.qr || {}, kamera = kannScannen(['qr_code']);
  return '<details class="vr-mehr vr-qrbox"' + (q.offen ? ' open' : '') + '><summary>Per QR-Code aufs andere Gerät</summary>' +
    '<div class="vr-knoepfe"><button type="button" class="vr-knopf" data-qr-zeigen>QR-Code anzeigen</button>' + (kamera ? '<button type="button" class="vr-knopf" data-qr-lesen>QR-Code einlesen</button>' : '') + '</div>' +
    (kamera ? '' : '<p class="vr-klein">Einlesen: Dieses Gerät kann im Browser nicht scannen. Auf dem iPhone/iPad die Kamera-App auf den Code richten, den angezeigten Text kopieren und oben unter „Text einfügen“ einsetzen (bei mehreren Codes alle nacheinander, je eine Zeile).</p>') +
    '<div class="vr-qr-ort" aria-live="polite">' + (q.html || '') + '</div><div class="vr-qr-video"></div></details>';
}

/* ===================================================================== Ereignisse */
var KAM = null;
function kameraStopp() { if (KAM) { try { KAM.strom.getTracks().forEach(function (t) { t.stop(); }); } catch (e) { /* weg */ } clearInterval(KAM.t); KAM = null; } var R = I.wurzel(); if (R) R.querySelectorAll('.vr-ean-video, .vr-qr-video').forEach(function (x) { x.innerHTML = ''; }); }
function kameraStart(ort, formate, treffer) {
  kameraStopp(); var R = I.wurzel(), box = R.querySelector(ort); if (!box) return;
  var det; try { det = new root.BarcodeDetector({ formats: formate }); } catch (e) { I.toast('Scannen geht auf diesem Gerät nicht.'); return; }
  navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } }).then(function (st) {
    box.innerHTML = '<video playsinline muted class="vr-video"></video><button type="button" class="vr-knopf" data-kamera-zu>Kamera aus</button>'; var v = box.querySelector('video'); v.srcObject = st; v.play();
    KAM = { strom: st, t: setInterval(function () { if (v.readyState < 2) return; det.detect(v).then(function (L) { if (L && L.length) treffer(L[0].rawValue); }).catch(function () { /* weiter */ }); }, 350) };
  }).catch(function () { I.toast('Kein Zugriff auf die Kamera.'); });
}
function eanSuchen(code) {
  var St = S(), O = OF(); code = String(code || '').replace(/\D/g, ''); O.sc = O.sc || {}; O.sc.code = code; O.sc.offen = true;
  if (!gtinOk(code)) { O.sc.erg = '<p class="vr-warn">Diese Nummer stimmt nicht (Prüfziffer). Bitte noch einmal abtippen.</p>'; I.zeichnen(false); return; }
  var id = (St.ean || {})[code], k = id ? K.katVon(St, id) : null;
  if (k) { St.lager.push({ u: uid(), k: k.i, m: 1, e: I.stdEinheit(k), mhd: '', o: k.l || 'v', ean: code }); O.sc.erg = '<p class="vr-ok">' + esc(k.n) + ' ins Lager gelegt.</p>'; I.nachAenderung(true); return; }
  O.sc.erg = '<p>Nummer <b>' + esc(code) + '</b> ist noch unbekannt.</p><div class="vr-knoepfe">' + (navigator.onLine !== false ? '<button type="button" class="vr-knopf vr-haupt" data-off="' + code + '">Bei Open Food Facts nachschlagen (Internet)</button>' : '<span class="vr-klein">Ohne Internet kein Nachschlagen.</span>') +
    '</div><p class="vr-klein">Oder einem Lebensmittel zuordnen: oben im Suchfeld suchen und antippen – die Nummer wird dann dazu gemerkt.</p>';
  O.eanWarte = code; I.zeichnen(false);
}
function offHolen(code) {
  var O = OF(); O.sc.erg = '<p class="vr-klein">Frage Open Food Facts …</p>'; I.zeichnen(false);
  var url = 'https://world.openfoodfacts.org/api/v2/product/' + encodeURIComponent(code) + '.json?fields=product_name,product_name_de,brands,quantity,nutriments';
  fetch(url, { headers: { Accept: 'application/json' } }).then(function (r) { return r.json(); }).then(function (d) {
    var x = d && d.status === 1 ? offNachKatalog(code, d) : null;
    if (!x) { O.sc.erg = '<p class="vr-warn">Bei Open Food Facts nicht gefunden. Lege das Lebensmittel unter „Eigenes Lebensmittel anlegen“ selbst an.</p>'; I.zeichnen(false); return; }
    O.offErg = { code: code, x: x };
    O.sc.erg = '<div class="vr-off"><p><b>' + esc(x.name) + '</b><br><small>' + (x.k != null ? fz(x.k) + ' kcal' : 'kcal unbekannt') + (x.e != null ? ' · Eiweiß ' + fz(x.e, 1) + ' g' : '') + (x.f != null ? ' · Fett ' + fz(x.f, 1) + ' g' : '') + (x.c != null ? ' · KH ' + fz(x.c, 1) + ' g' : '') + ' je 100 ' + (x.ml ? 'ml' : 'g') + (x.pg ? ' · Packung ' + fz(x.pg) + (x.ml ? ' ml' : ' g') : '') + '</small></p>' +
      '<div class="vr-felder">' + feld('Gruppe', '<select data-offg>' + K.GRUPPEN.map(function (g) { return '<option value="' + g.k + '">' + esc(g.kurz) + '</option>'; }).join('') + '</select>') + '</div>' +
      '<div class="vr-knoepfe"><button type="button" class="vr-knopf vr-haupt" data-off-anlegen' + (x.k == null ? ' disabled' : '') + '>Anlegen und ins Lager</button></div>' +
      '<p class="vr-klein">Daten von Open Food Facts (openfoodfacts.org): Datenbank unter Open Database License (ODbL), Einzelinhalte unter Database Contents License (DbCL) – Namensnennung, Weitergabe unter gleichen Bedingungen. Angaben ohne Gewähr – mit der Packung vergleichen.</p></div>';
    I.zeichnen(false);
  }).catch(function () { O.sc.erg = '<p class="vr-warn">Kein Netz oder Open Food Facts nicht erreichbar. Ohne Netz: Lebensmittel selbst anlegen.</p>'; I.zeichnen(false); });
}
function qrZeigen() {
  var O = OF(); O.qr = { offen: true, html: '<p class="vr-klein">Erzeuge QR-Code …</p>' }; I.zeichnen(false);
  zip(kompakt(S())).then(function (p) { var T = qrTeile(p);
    if (T.length > 6) { O.qr.html = '<p class="vr-warn">Zu viele Daten für QR-Codes (' + T.length + ' Codes). Bitte „Als Text kopieren“ nehmen.</p>'; I.zeichnen(false); return; }
    O.qr.teil = 0; O.qr.T = T; qrZeichnen();
  }).catch(function () { O.qr.html = '<p class="vr-warn">QR-Code ging nicht – bitte „Als Text kopieren“.</p>'; I.zeichnen(false); });
}
function qrZeichnen() {
  var O = OF(), T = O.qr.T, i = O.qr.teil;
  O.qr.html = '<div class="vr-qrwrap">' + qrSvg(T[i]) + '</div><p class="vr-klein">' + (T.length > 1 ? 'Code ' + (i + 1) + ' von ' + T.length + ' – nacheinander einlesen. ' : '') + 'Auf dem anderen Gerät: „QR-Code einlesen“ oder mit der Kamera-App scannen und den Text unter „Text einfügen“ einsetzen.</p>' +
    (T.length > 1 ? '<div class="vr-knoepfe"><button type="button" class="vr-knopf" data-qr-teil="-1"' + (i ? '' : ' disabled') + '>‹ Zurück</button><button type="button" class="vr-knopf" data-qr-teil="1"' + (i < T.length - 1 ? '' : ' disabled') + '>Weiter ›</button></div>' : '');
  I.zeichnen(false);
}
function qrText(text) {
  var Z = qrZusammen(String(text).split(/\n+/));
  if (!Z) return false; if (Z.fehlt) { I.toast('Code ' + Z.fehlt + ' von ' + Z.von + ' fehlt noch.'); return true; }
  unzip(Z.text).then(function (j) { I.sicherungLesen(j); }).catch(function (e) { I.toast(e && e.message ? e.message : 'Der Code ließ sich nicht lesen.'); });
  return true;
}
var QR_GESAMMELT = [];

H.klick.push(function (t, a) {
  var St = S(), O = OF();
  if (t.hasAttribute('data-drucken')) { drucken(); return true; }
  if (t.hasAttribute('data-blatt')) { OF().blattLang = a('data-blatt') === 'lang'; I.zeichnen(); return true; }
  if (t.hasAttribute('data-set')) { var p = a('data-set').split(':'), w = a('data-wert');
    if (p[0] === 'vg') { O.zusatz = w === '1'; I.zeichnen(false); return true; }
    if (p[0] === 'vl') { O.vlArt = w; I.zeichnen(false); return true; }
    if (p[0] === 'ga') { O.ga = Object.assign(O.ga || {}, { art: w, offen: true }); I.zeichnen(false); return true; }
    return false; }
  if (t.hasAttribute('data-vl-uebernehmen')) { var Hh = K.haushalt(St), art = O.vlArt || (Hh.n ? 'haushalt' : 'personen'), n = +O.vlN || Math.max(1, Hh.n || 2), tg = +O.vlT || K.zielTage(St);
    var L = vorlage((art === 'haushalt' && Hh.kcal > 0 ? Hh.kcal / 2200 : n) * tg / 10).filter(function (e) { return !(O.vlWeg || {})[e.id]; });
    I.undo(klon(St)); L.forEach(function (e) { var k = K.katVon(St, e.id); St.lager.push({ u: uid(), k: e.id, m: e.m, e: e.e, mhd: '', o: k.l || 'v' }); }); St.beispiel = false;
    I.nachAenderung(false); I.toast(L.length + ' Posten ins Lager übernommen – jetzt Mengen und Datum anpassen.', true); I.tab('lager'); return true; }
  if (t.hasAttribute('data-badd')) { var kat = a('data-badd'), nm = a('data-n'); if (!nm) { var inp = I.wurzel().querySelector('[data-bneu="' + kat + '"]'); nm = inp && inp.value.trim(); }
    if (!nm) { I.toast('Bitte einen Namen eingeben.'); return true; }
    St.bestaende.push({ u: uid(), kat: kat, n: nm, m: 1, e: /papier|toilette/i.test(nm) ? 'Rollen' : 'Stück', mhd: '', verbrauch: '' }); O['bk:' + kat] = true; I.nachAenderung(true); return true; }
  var bl = t.closest('[data-bu]');
  if (bl) { var b = St.bestaende.filter(function (x) { return x.u === bl.getAttribute('data-bu'); })[0]; if (!b) return true;
    if (t.hasAttribute('data-bweg')) { I.undo(klon(St)); St.bestaende = St.bestaende.filter(function (x) { return x !== b; }); I.nachAenderung(true); I.toast('Entfernt.', true); return true; }
    if (t.hasAttribute('data-bplus') || t.hasAttribute('data-bminus')) { b.m = Math.max(0, (+b.m || 0) + (t.hasAttribute('data-bplus') ? 1 : -1)); I.nachAenderung(true); return true; } }
  if (t.hasAttribute('data-ean-los')) { eanSuchen(I.wurzel().querySelector('#vr-ean').value); return true; }
  if (t.hasAttribute('data-ean-kamera')) { kameraStart('.vr-ean-video', ['ean_13', 'ean_8', 'upc_a', 'upc_e'], function (c) { kameraStopp(); eanSuchen(c); }); return true; }
  if (t.hasAttribute('data-kamera-zu')) { kameraStopp(); return true; }
  if (t.hasAttribute('data-off')) { offHolen(a('data-off')); return true; }
  if (t.hasAttribute('data-off-anlegen')) { var r = O.offErg; if (!r) return true; var g = I.wurzel().querySelector('[data-offg]').value;
    var e = { i: 'e_' + uid(), n: r.x.name, g: g, k: r.x.k, e: +r.x.e || 0, f: +r.x.f || 0, c: +r.x.c || 0, q: 'eigen', ht: 'MHD auf der Packung', ean: r.code, quelle: 'Open Food Facts (ODbL)' };
    if (r.x.ml) e.ml = 1; if (r.x.pg) e.p = [['Packung ' + fz(r.x.pg) + (r.x.ml ? ' ml' : ' g'), r.x.pg]];
    St.eigene.push(e); St.ean[r.code] = e.i; St.lager.push({ u: uid(), k: e.i, m: 1, e: I.stdEinheit(e), mhd: '', o: 'v', ean: r.code });
    O.sc.erg = '<p class="vr-ok">' + esc(e.n) + ' angelegt und ins Lager gelegt.</p>'; O.offErg = null; O.eanWarte = null; I.nachAenderung(true); return true; }
  if (t.hasAttribute('data-add') && O.eanWarte) { St.ean[O.eanWarte] = a('data-add'); I.toast('Strichcode ' + O.eanWarte + ' gemerkt.'); O.eanWarte = null; O.sc = { offen: false }; return false; }
  if (t.hasAttribute('data-ga-buchen')) { var ga = O.ga || {}, bk = ga.basis ? K.katVon(St, ga.basis) : null; if (!bk) { I.toast('Bitte wählen, was drin ist.'); return true; }
    var an = Math.max(1, +zahl(ga.anzahl) || 1), inh = +zahl(ga.inhalt) || (bk.p && bk.p[0] ? bk.p[0][1] : 500), herg = ga.herg || ym(heute()), ort = ga.art === 'eingefroren' ? (St.orte.filter(function (o) { return o.typ === 't'; })[0] || { id: 't' }).id : 'v';
    St.lager.push({ u: uid(), k: bk.i, m: an * inh, e: bk.ml ? 'ml' : 'g', mhd: eigenMhd(ga.art, bk, herg), o: ort, n: ga.name || (bk.n.replace(/ \(.*\)$/, '').replace(/, trocken$/, '')), art: EA[ga.art][1], herg: herg });
    O.ga = { art: ga.art, offen: true }; I.nachAenderung(true); I.toast('Eingebucht.'); return true; }
  if (t.hasAttribute('data-ics-alle')) { var P = St.lager.filter(function (it) { return it.mhd; }).map(function (it) { var k = K.katVon(St, it.k); return { u: it.u, n: it.n || (k ? k.n : ''), mhd: it.mhd, ort: K.ortName(St, it.o) }; });
    datei('vorrat-erinnerungen.ics', ics(P, +zahl(St.erinnVorlauf) || 30), 'text/calendar'); I.toast('Kalender-Datei wird gespeichert – öffnen, um die Termine zu übernehmen.'); return true; }
  if (t.hasAttribute('data-ics-text')) { var TX = St.lager.filter(function (it) { return it.mhd; }).map(function (it) { var k = K.katVon(St, it.k), m = /^(\d{4})-(\d{2})$/.exec(it.mhd), ende = new Date(+m[1], +m[2], 0, 12), tag = new Date(ende.getTime() - (+zahl(St.erinnVorlauf) || 30) * 86400000);
      return tag.toLocaleDateString('de-DE') + ' – ' + (it.n || k.n) + ' läuft ab (MHD ' + I.mhdText(it.mhd) + ', ' + K.ortName(St, it.o) + ')'; }).sort(); I.kopieren(TX.join('\n'), 'Termine kopiert.'); return true; }
  if (t.hasAttribute('data-ics')) { var it = St.lager.filter(function (x) { return x.u === a('data-ics'); })[0]; if (!it) return true; var k2 = K.katVon(St, it.k);
    datei('vorrat-' + (it.n || k2.n).replace(/[^a-z0-9äöüß]+/gi, '-').slice(0, 30) + '.ics', ics([{ u: it.u, n: it.n || k2.n, mhd: it.mhd, ort: K.ortName(St, it.o) }], +zahl(St.erinnVorlauf) || 30), 'text/calendar'); return true; }
  if (t.hasAttribute('data-qr-zeigen')) { qrZeigen(); return true; }
  if (t.hasAttribute('data-qr-teil')) { O.qr.teil = Math.max(0, Math.min(O.qr.T.length - 1, O.qr.teil + (+a('data-qr-teil')))); qrZeichnen(); return true; }
  if (t.hasAttribute('data-qr-lesen')) { QR_GESAMMELT = []; O.qr = Object.assign(O.qr || {}, { offen: true });
    kameraStart('.vr-qr-video', ['qr_code'], function (txt) { if (QR_GESAMMELT.indexOf(txt) >= 0) return; QR_GESAMMELT.push(txt); var Z = qrZusammen(QR_GESAMMELT);
      if (Z && Z.fehlt) I.toast('Code ' + Z.da + ' von ' + Z.von + ' gelesen – nächsten zeigen.'); else if (Z) { kameraStopp(); qrText(QR_GESAMMELT.join('\n')); } }); return true; }
  if (t.getAttribute('data-sich') === 'einfuegen') { var ta = I.wurzel().querySelector('.vr-text'); if (ta && /^\s*QWV:/.test(ta.value)) { qrText(ta.value); return true; } return false; }
  return false;
});
H.eingabe.push(function (t) {
  var St = S(), O = OF();
  if (t.hasAttribute('data-vl')) { var v = Math.max(1, Math.min(365, Math.round(zahl(t.value)) || 1)); if (t.getAttribute('data-vl') === 'n') O.vlN = v; else O.vlT = v; return true; }
  if (t.hasAttribute('data-budget')) { St.budget = t.value.trim(); I.sichern(); return true; }
  if (t.hasAttribute('data-erinn')) { St.erinnVorlauf = t.value.trim(); I.sichern(); return true; }
  if (t.hasAttribute('data-ga')) { O.ga = O.ga || {}; O.ga[t.getAttribute('data-ga')] = t.value; return true; }
  var bl = t.closest('[data-bu]'); if (bl && t.hasAttribute('data-bf')) { var b = St.bestaende.filter(function (x) { return x.u === bl.getAttribute('data-bu'); })[0]; if (b) { var f = t.getAttribute('data-bf'); b[f] = f === 'm' ? (isFinite(zahl(t.value)) ? zahl(t.value) : b.m) : t.value; I.sichern(); } return true; }
  return false;
});
H.aenderung.push(function (t) {
  var St = S(), O = OF();
  if (t.hasAttribute('data-vl') || t.hasAttribute('data-budget')) { I.zeichnen(false); return true; }
  if (t.hasAttribute('data-vlweg')) { O.vlWeg = O.vlWeg || {}; if (t.checked) delete O.vlWeg[t.getAttribute('data-vlweg')]; else O.vlWeg[t.getAttribute('data-vlweg')] = 1; return true; }
  if (t.hasAttribute('data-ga')) { O.ga = O.ga || {}; O.ga[t.getAttribute('data-ga')] = t.value; O.ga.offen = true; I.zeichnen(false); return true; }
  var mj = t.closest('[data-mj]'); if (mj) { var mm = mj.querySelector('[data-mjm]').value, jj = mj.querySelector('[data-mjj]').value; O.ga = O.ga || {}; O.ga.herg = jj + '-' + (mm < 10 ? '0' : '') + mm; O.ga.offen = true; I.zeichnen(false); return true; }
  var bl = t.closest('[data-bu]'); if (bl) { var b = St.bestaende.filter(function (x) { return x.u === bl.getAttribute('data-bu'); })[0]; if (!b) return true;
    var l2 = t.getAttribute('data-lf2'); if (l2 === 'mm' || l2 === 'jj') { var box = t.closest('.vr-mhd'), m2 = box.querySelector('[data-lf2="mm"]').value, j2 = box.querySelector('[data-lf2="jj"]').value; b.mhd = m2 && j2 ? j2 + '-' + (m2 < 10 ? '0' : '') + m2 : ''; }
    I.nachAenderung(true); return true; }
  return false;
});
H.postenMehr.push(function (x) { return x.it.mhd && I.dateiMoeglich() ? '<div class="vr-knoepfe"><button type="button" class="vr-knopf" data-ics="' + esc(x.it.u) + '">📅 Erinnerung in den Kalender</button></div>' : ''; });
H.postenMehr.push(function (x) { return x.it.ean || x.k.ean ? '<p class="vr-klein">Strichcode: ' + esc(x.it.ean || x.k.ean) + (x.k.quelle ? ' · Daten: ' + esc(x.k.quelle) : '') + '</p>' : ''; });
H.lagerOben.push(function () { return strichcodeHTML() + gartenHTML() + erinnerungHTML(); });
H.haushaltUnten.push(function () { return qrHTML(); });
H.fehltOben.push(function () { return I.BEREICH.kosten ? '<div class="vr-knoepfe"><button type="button" class="vr-knopf" data-tab="kosten">€ Kosten und Einkauf in Etappen</button><button type="button" class="vr-knopf" data-tab="vergleich">⚖ 3 · 10 · 28 Tage vergleichen</button></div>' : ''; });
if (typeof document !== 'undefined') document.addEventListener('visibilitychange', function () { if (document.hidden) kameraStopp(); });

var B = I.BEREICH;
B.uebersicht = uebersichtHTML; B.blatt = blattHTML; B.vergleich = vergleichHTML; B.kosten = kostenHTML; B.vorlage = vorlageHTML; B.bestaende = bestaendeHTML;
quelle('BZfE: Haltbarkeit von Lebensmitteln (Stand 20.02.2025)', 'https://www.bzfe.de/kueche-und-alltag/kochen/haltbarkeit-von-lebensmitteln', 'Eingekochtes 6–12 Monate (Garten und Eingemachtes)');
quelle('Open Food Facts – offene Lebensmitteldatenbank (ODbL)', 'https://world.openfoodfacts.org/', 'Nachschlagen per Strichcode, nur auf Knopfdruck mit Netz');
quelle('lean-qr von David Evans (MIT-Lizenz)', 'https://github.com/davidje13/lean-qr', 'QR-Codes zum Übertragen');

V._plus = { vorlage: vorlage, BLE_VORLAGE: BLE_VORLAGE, vergleich: vergleich, einkauf: einkauf, etappen: etappen, ics: ics, gtinOk: gtinOk, offNachKatalog: offNachKatalog, qrTeile: qrTeile, qrZusammen: qrZusammen, qrSvg: qrSvg, zip: zip, unzip: unzip, kompakt: kompakt,
  bestandTage: bestandTage, bestandAmpel: bestandAmpel, brennProTag: brennProTag, eigenMhd: eigenMhd, plusMonate: plusMonate, blattInhalt: blattInhalt, blattKurz: blattKurz, uebersichtHTML: uebersichtHTML, BKAT: BKAT, quelle: quelle, druckMoeglich: druckMoeglich, eingebettet: eingebettet, stufe: stufe, ampelKlasse: ampelKlasse, weg: weg, monatJahr: monatJahr };
if (typeof module !== 'undefined' && module.exports) module.exports = V._plus;
})(typeof window !== 'undefined' ? window : globalThis);
