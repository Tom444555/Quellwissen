/* Quellwissen – „Vorrat & Blackout-Planer“, Bereich „Notfall“ (Stufe 2: nur Inhalte aus den Beleg-Dateien, vorrat_fakten.js)
   Ablauf Stunde 0 bis Tag 10 · Wasser genauer · Strom & Wärme · Kochen ohne Strom · Notfallplan · Region · Nährstoff-Check
   Quelle: werkzeug/vorlagen/vorrat_notfall.js · reine Rechnungen unter QWVorrat._notfall */
(function (root) {
'use strict';
var V = root.QWVorrat; if (!V || !V._i) return;
var I = V._i, K = V._kern, H = I.HAKEN, F = root.QWVorratFakten || { Q: [], T: {} };
var esc = I.esc, fz = I.fz, liter = I.liter, zahl = I.zahl, feld = I.feld, zahlIn = I.zahlIn, seg = I.seg, balken = I.balken, tageText = I.tageText;
function S() { return I.zustand(); }
function OF() { return I.offen(); }
function T(n) { return F.T[n] || null; }
function E(n, id) { var t = T(n); if (!t) return null; for (var i = 0; i < t.E.length; i++) if (t.E[i][0] === id) return t.E[i]; return null; }
function wert(n, id, ersatz) { var e = E(n, id); return e && e[4] != null ? +e[4] : ersatz; }
function stufe(t, z) { return t >= z ? 'gruen' : t >= Math.min(3, z) ? 'gelb' : 'rot'; }
/* Quellen der Belege in den Abschnitt „Quellen und Stand“ übernehmen */
Object.keys(F.T).forEach(function (n) { if (n === 'technik') return; (F.T[n].q || []).forEach(function (qi) { var q = F.Q[qi]; if (q && q[1] && !I.QUELLEN.some(function (x) { return x[1] === q[1]; })) I.QUELLEN.push([q[0] + (q[2] ? ' (Stand: ' + q[2] + ')' : ''), q[1], F.T[n].thema]); }); });

/* ---------- Bausteine ---------- */
/* Stand kurz: ohne Links und Zusatzbemerkungen */
function standKurz(s) { s = String(s || '').replace(/https?:\S+/g, '').split(/;|\(gelesen|\(Original/)[0].replace(/[\s,:(]+$/, '').trim(); return s; }
function quelleHTML(qi) { var q = F.Q[qi]; if (!q) return ''; var st = standKurz(q[2]); return '<small class="vr-q">Quelle: ' + (q[1] ? '<a href="' + esc(q[1]) + '" target="_blank" rel="noopener">' + esc(q[0]) + '</a>' : esc(q[0])) + (st ? ' · Stand: ' + esc(st) : '') + '</small>'; }
function wertHTML(e) { return e[4] != null ? '<span class="vr-wert"><b>' + fz(+e[4], +e[4] % 1 ? 2 : 0) + '</b> ' + esc(e[5]) + '</span>' : ''; }
function eintragHTML(e, mitHaken, haken) {
  return '<li class="vr-fakt' + (e[6] ? ' vr-fakt-w' : '') + '">' + (mitHaken ? '<label class="vr-fh"><input type="checkbox" data-ablauf="' + esc(e[0]) + '"' + (haken ? ' checked' : '') + '><b>' + esc(e[2]) + '</b></label>' : '<b>' + esc(e[2]) + '</b>') +
    (e[3] ? '<p>' + esc(e[3]) + '</p>' : '') + wertHTML(e) + (e[6] ? '<p class="vr-warnung"><span aria-hidden="true">⚠</span> ' + esc(e[6]) + '</p>' : '') + quelleHTML(e[7]) + '</li>';
}
function gruppen(n, nur) { var t = T(n), G = []; if (!t) return G; t.E.forEach(function (e) { if (nur && nur.indexOf(e[1]) < 0) return; var g = G.filter(function (x) { return x.t === e[1]; })[0]; if (!g) { g = { t: e[1], E: [] }; G.push(g); } g.E.push(e); }); return G; }
function faktenHTML(n, nur, titelStufe) { return gruppen(n, nur).map(function (g) { return '<h' + (titelStufe || 3) + '>' + esc(g.t) + '</h' + (titelStufe || 3) + '><ul class="vr-fakten" role="list">' + g.E.map(function (e) { return eintragHTML(e); }).join('') + '</ul>'; }).join(''); }
function fehltHTML(n) { return '<div class="vr-leer"><p>Die Belege für diesen Teil liegen noch nicht vor. Sobald sie geprüft sind, erscheinen sie hier.</p></div>'; }
function kopf(n, titel, text) { var t = T(n); return '<section class="vr-bereich" data-b="' + n + '"><h2>' + titel + '</h2><p class="vr-unter">' + text + '</p>' + (t ? '<p class="vr-klein">Stand der Belege: ' + esc(t.stand) + '. Jede Angabe nennt ihre Quelle; Richtwerte sind als solche gekennzeichnet.</p>' : ''); }

/* ===================================================================== Ablauf Stunde 0 bis Tag 10 */
function ablaufStand(St) { var t = T('ablauf'); if (!t) return { n: 0, d: 0 }; var d = 0; t.E.forEach(function (e) { if ((St.ablauf || {})[e[0]]) d++; }); return { n: t.E.length, d: d }; }
function ablaufHTML() {
  var St = S(), t = T('ablauf'), h = kopf('ablauf', 'Ablauf: Stunde 0 bis Tag 10', 'Was in welcher Phase eines Stromausfalls zu tun ist – zum Abhaken, wenn es so weit ist. Die Haken bleiben auf diesem Gerät.');
  if (!t) return h + fehltHTML() + '</section>';
  var a = ablaufStand(St);
  h += '<div class="vr-karte vr-zahlkarte"><span class="vr-fl">Erledigt</span><b class="vr-gz vr-gz-t">' + a.d + ' von ' + a.n + '</b>' + balken(a.d, a.n, 'vr-gut') + '<div class="vr-knoepfe"><button type="button" class="vr-knopf" data-ablauf-neu' + (a.d ? '' : ' disabled') + '>Alle Haken entfernen</button></div></div>';
  h += '<ol class="vr-zeitachse">' + gruppen('ablauf').map(function (g) { var d = g.E.filter(function (e) { return (St.ablauf || {})[e[0]]; }).length;
    return '<li class="vr-phase' + (d === g.E.length ? ' vr-phase-ok' : '') + '"><h3><span class="vr-pdot" aria-hidden="true"></span>' + esc(g.t) + ' <small class="vr-zaehl">' + d + '/' + g.E.length + '</small></h3><ul class="vr-fakten" role="list">' + g.E.map(function (e) { return eintragHTML(e, true, (St.ablauf || {})[e[0]]); }).join('') + '</ul></li>'; }).join('') + '</ol>';
  return h + '<p class="vr-klein">Kein Ersatz für Anweisungen der Behörden vor Ort – Radio und Warn-App beachten.</p></section>';
}
H.uebersichtAblauf = function (St) { var a = ablaufStand(St); if (!a.n) return { amp: '', txt: 'Was in welcher Stunde zu tun ist' };
  return a.d === 0 ? { amp: '', gross: 'Stunde 0 bis Tag 10', txt: a.n + ' Schritte zum Abhaken' } : { amp: a.d === a.n ? 'gruen' : 'gelb', gross: a.d + ' von ' + a.n + ' erledigt', txt: 'Ablauf im Ernstfall' }; };
H.blattAblauf = function () { var t = T('ablauf'); if (!t) return '';
  return '<section><h2>Ablauf bei Stromausfall</h2><div class="vr-dcheck">' + gruppen('ablauf').map(function (g) { return '<div><h3>' + esc(g.t) + '</h3><ul>' + g.E.map(function (e) { return '<li>☐ ' + esc(e[2]) + (e[6] ? ' – ⚠ ' + esc(e[6]) : '') + '</li>'; }).join('') + '</ul></div>'; }).join('') + '</div></section>'; };

/* ===================================================================== Wasser genauer */
function wasserHTML() {
  var St = S(), t = T('wasser'), Wq = St.wasserQ || (St.wasserQ = {}), Hh = K.haushalt(St), W = K.wasser(St), z = K.zielTage(St), kochen = (St.lage || {}).koch !== 'keine';
  var h = kopf('wasser', 'Wasser', 'Wie viel ihr braucht, was an Notquellen da ist und wie man Wasser sicher macht. Die Rechnung fließt in „Wasser reicht … Tage“ ein.');
  var pflegeE = E('wasser', 'bedarf-who-hygiene'), toiE = E('wasser', 'bedarf-toilette');
  h += '<div class="vr-gross"><div class="vr-karte ' + (W.leitung ? 'vr-gut' : W.tage >= z ? 'vr-gut' : W.tage >= Math.min(3, z) ? 'vr-mittel' : 'vr-schlecht') + '"><span class="vr-fl">Trinkwasser reicht</span>' + (W.leitung ? '<b class="vr-gz vr-gz-t">Leitung läuft</b>' : '<b class="vr-gz">' + I.tageZahl(W.tage) + '</b><span class="vr-ge">Tage</span>') +
    '<small>' + liter(W.vorrat) + ' Vorrat' + (W.notquellen ? ' + ' + liter(W.notquellen) + ' aus Notquellen' : '') + ' · ' + liter(W.bedarf) + ' am Tag</small></div>' +
    '<div class="vr-karte ' + (W.brauchTage == null ? '' : W.brauchTage >= z ? 'vr-gut' : W.brauchTage >= 3 ? 'vr-mittel' : 'vr-schlecht') + '"><span class="vr-fl">Brauchwasser reicht</span>' + (W.brauchTage == null ? '<b class="vr-gz vr-gz-t">–</b><small>Körperpflege oder Spülen unten wählen</small>' : W.leitung ? '<b class="vr-gz vr-gz-t">Leitung läuft</b>' : '<b class="vr-gz">' + I.tageZahl(W.brauchTage) + '</b><span class="vr-ge">Tage</span><small>' + liter(W.brauch) + ' da · ' + liter(W.brauchBedarf) + ' am Tag</small>') + '</div></div>';
  /* Bedarf */
  h += '<h3>Bedarf am Tag</h3><div class="vr-karte"><ul class="vr-bedarf" role="list"><li><span>Trinken und Kochen (2 l je Person, BBK)</span><b>' + liter(Hh.n * 2) + '</b></li>' + (Hh.tiereW ? '<li><span>Haustiere</span><b>' + liter(Hh.tiereW) + '</b></li>' : '') + (Hh.hyg ? '<li><span>Waschwasser aus dem Vorrat (Haushalt → Lage)</span><b>' + liter(Hh.n * Hh.hyg) + '</b></li>' : '') + '</ul>' +
    '<label class="vr-schalter"><input type="checkbox" data-wq="pflege"' + (Wq.pflege ? ' checked' : '') + '><span>Körperpflege mit Brauchwasser einplanen</span></label>' +
    (Wq.pflege ? feld('Liter je Person und Tag', zahlIn('data-wqz="pflegeL"', Wq.pflegeL || '', 'l', pflegeE ? 'z. B. ' + fz(+pflegeE[4]) + ' (WHO)' : '')) + (pflegeE ? '<p class="vr-klein">' + esc(pflegeE[3]) + ' <i>Internationale Angabe.</i> ' + quelleHTML(pflegeE[7]) + '</p>' : '') : '') +
    feld('Toilette', seg('wq:toilette', [['beutel', 'Beutel/Eimer (kein Wasser)'], ['spuelen', 'Mit Wasser spülen']], Wq.toilette || 'beutel', 'vr-seg-wrap'), 'vr-voll') +
    (Wq.toilette === 'spuelen' ? feld('Liter je Person und Tag zum Spülen', zahlIn('data-wqz="toiletteL"', Wq.toiletteL || '', 'l', 'eigener Wert')) + (toiE ? '<p class="vr-klein">' + esc(toiE[3]) + ' ' + quelleHTML(toiE[7]) + '</p>' : '') : '') + '</div>';
  /* Notquellen */
  h += '<h3>Eigene Notquellen</h3><div class="vr-karte"><p class="vr-klein">Wie viel Liter hättet ihr hier? Spülkasten, Warmwasserspeicher und Regenwasser zählen nur dann als Trinkwasser, wenn ihr sie abkocht; Badewanne und Pool nur als Brauchwasser.</p><div class="vr-felder">' +
    I.WQ.map(function (q) { return feld(esc(q[1]) + ' <small>(' + ({ brauch: 'Brauchwasser', abkochen: 'nur abgekocht', trink: 'trinkbar' })[q[2]] + ')</small>', zahlIn('data-wqq="' + q[0] + '"', (Wq.q || {})[q[0]] || '', 'l', '0')); }).join('') + '</div>' +
    '<label class="vr-schalter"><input type="checkbox" data-wq="abkochen"' + (Wq.abkochen ? ' checked' : '') + (kochen ? '' : ' disabled') + '><span>Spülkasten, Speicher und Regenwasser abkochen und trinken' + (kochen ? '' : ' (geht nur mit einer Kochstelle)') + '</span></label>' +
    (E('wasser', 'auf-abkochen') ? '<p class="vr-warnung"><span aria-hidden="true">⚠</span> ' + esc(E('wasser', 'auf-abkochen')[6]) + '</p>' : '') + '</div>';
  var ab1 = E('wasser', 'auf-abkochen'), ab2 = E('wasser', 'auf-abkochen-international');
  if (ab1 && ab2) h += '<h3>Abkochen: zwei Angaben</h3><div class="vr-widerspruch"><div class="vr-karte"><b>Umweltbundesamt</b><p>' + esc(ab1[3]) + '</p>' + quelleHTML(ab1[7]) + '</div><div class="vr-karte"><b>CDC (USA, international)</b><p>' + esc(ab2[3]) + '</p>' + quelleHTML(ab2[7]) + '</div></div><p class="vr-klein">Die Angaben unterscheiden sich in der Kochdauer; der Planer entscheidet das nicht.</p>';
  h += t ? faktenHTML('wasser', ['Notquellen', 'Aufbereitung', 'Lagern', 'Toilette', 'Bedarf']) : fehltHTML();
  return h + '</section>';
}

/* ===================================================================== Strom & Wärme */
/* Gerätevorlagen aus strom.json: [id, Name, Art (wh = Wh je Ladung · w = Watt × Stunden · tag = Wh je Tag), Wert-Funktion] */
var GERAETE = [
  ['smartphone', 'Smartphone laden', 'wh', function () { return wert('strom', 'v-smartphone', null); }, 'Ladungen am Tag'],
  ['laptop', 'Laptop laden', 'wh', function () { return wert('strom', 'v-laptop', null); }, 'Ladungen am Tag'],
  ['router', 'WLAN-Router', 'w', function () { return wert('strom', 'v-router', null); }, 'Stunden am Tag'],
  ['lichterkette', 'Lichterkette', 'w', function () { var h = wert('strom', 'v-lichterkette', null); return h ? 500 / h : null; }, 'Stunden am Tag'],
  ['led', 'LED-Lampe (Watt von der Packung)', 'w', function () { return null; }, 'Stunden am Tag'],
  ['radio', 'Radio (Watt laut Gerät)', 'w', function () { return null; }, 'Stunden am Tag'],
  ['kgk-neu', 'Kühl-Gefrier-Kombi, sparsam', 'tag', function () { return wert('strom', 'v-kgk-neu', null) * 1000; }, ''],
  ['kgk-alt', 'Kühl-Gefrier-Kombi, Altgerät', 'tag', function () { return wert('strom', 'v-kgk-alt', null) * 1000; }, ''],
  ['kuehl-klein', 'Kleiner Kühlschrank, sparsam', 'tag', function () { return wert('strom', 'v-kuehl-klein', null) * 1000; }, ''],
  ['gefrier', 'Gefrierschrank, hoher Verbrauch', 'tag', function () { return wert('strom', 'v-gefrier-hoch', null) * 1000; }, ''],
  ['pumpe-neu', 'Heizungspumpe, Hocheffizienz', 'w', function () { return wert('strom', 'v-pumpe-neu', null); }, 'Stunden am Tag'],
  ['pumpe-alt', 'Heizungspumpe, alt', 'w', function () { return wert('strom', 'v-pumpe-alt', null); }, 'Stunden am Tag'],
  ['eigen', 'Eigenes Gerät', 'w', function () { return null; }, 'Stunden am Tag']
];
var GER = {}; GERAETE.forEach(function (g) { GER[g[0]] = g; });
var GERQ = { smartphone: 'v-smartphone', laptop: 'v-laptop', router: 'v-router', lichterkette: 'v-lichterkette', led: 'v-led', 'kgk-neu': 'v-kgk-neu', 'kgk-alt': 'v-kgk-alt', 'kuehl-klein': 'v-kuehl-klein', gefrier: 'v-gefrier-hoch', 'pumpe-neu': 'v-pumpe-neu', 'pumpe-alt': 'v-pumpe-alt' };
/* Wh je Tag eines Geräts: g = {typ, menge (Ladungen bzw. Stunden), w (eigener Wert: Wh je Ladung bzw. Watt bzw. Wh je Tag)} */
function geraetWh(g) { var V0 = GER[g.typ]; if (!V0) return 0; var w = zahl(g.w); if (!(w > 0)) w = V0[3](); if (!(w > 0)) return 0; var m = zahl(g.menge);
  if (V0[2] === 'tag') return w * (g.an === false ? 0 : 1); return w * (m > 0 ? m : 0); }
/* Speicher in Wh: Powerbanks (mAh × 3,7 V × nutzbarer Anteil), Powerstation (Wh), Stromerzeuger (Liter ÷ l je kWh) */
function speicherWh(st) {
  st = st || {}; var v = wert('strom', 's-formel', 3.7), f = wert('strom', 's-powerbank-real', 0.75), pb = 0;
  (st.pb || []).forEach(function (p) { var m = zahl(p.mah), n = zahl(p.n) || 1; if (m > 0) pb += m * v / 1000 * f * n; });
  var ps = zahl(st.ps) > 0 ? zahl(st.ps) : 0, lkwh = wert('strom', 'g-verbrauch', null), gen = zahl(st.benzin) > 0 && lkwh ? zahl(st.benzin) / lkwh * 1000 : 0;
  return { pb: pb, ps: ps, gen: gen, summe: pb + ps + gen };
}
/* Solar: Ertrag am Tag im gewählten Monat (Monatswerte kWh je kWp aus den Belegen, Simulation); ohne Monat das Jahresmittel. Nur mit Speicher nutzbar. */
var MONAT = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'], MTAGE = [31, 28.25, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
var NEIG = [['30', 'Süd, geneigt 30°', 'Dach, Aufständerung'], ['60', 'Süd, steil 60°', 'steile Aufständerung'], ['90', 'Süd, senkrecht 90°', 'Balkongeländer, Fassade'], ['ost', 'Ost, geneigt 30°', 'Dach nach Osten'], ['west', 'West, geneigt 30°', 'Dach nach Westen']];
/* Standort für Solar: je Bundesland eine Landeshauptstadt (pv-orte); ohne Wahl das Bundesland aus „Region“, sonst Saarland */
function solarOrte() { var e = E('strom', 'pv-orte'); return (e && e[8] && e[8].orte) || null; }
function solarLand(st) { var O = solarOrte(), Z = null; try { Z = S(); } catch (x) {} var l = (st || {}).ort || ((Z || {}).region || {}).land; return O && O[l] ? l : 'SL'; }
function solarMonate(st) { var n = String((st || {}).neig || '30'), O = solarOrte(), l = solarLand(st), m = O && O[l] && O[l].a[n];
  if (!m) { var e = E('strom', 'pv-monat'), x = e && e[8]; m = x && ((x.neigung && x.neigung[n]) || (n === '30' && x.monate)); } return m && m.length === 12 ? m : null; }
function solarMonat(st) { var m = (st || {}).monat; return m === '' || m == null || !(+m >= 0 && +m <= 11) ? I.heute().getMonth() : +m; }
function solarWhTag(st, monat) { var wp = zahl((st || {}).wp), M = solarMonate(st); if (!(wp > 0)) return 0;
  if (monat != null && M) return wp * M[monat] / MTAGE[monat];
  var r = wert('strom', 'pv-ertrag-jahr', null); return r ? wp * (r / 100) * 1000 / 365 : 0; }
function stromRechnung(St) {
  var st = St.strom || {}, G = St.stromG || [], bedarf = 0; G.forEach(function (g) { bedarf += geraetWh(g); });
  var sp = speicherWh(st), mo = solarMonate(st) ? solarMonat(st) : null, sol = sp.pb + sp.ps > 0 ? solarWhTag(st, mo) : 0, netto = bedarf - sol;
  return { bedarf: bedarf, speicher: sp, solar: sol, monat: mo, tage: bedarf <= 0 ? null : netto <= 0 ? Infinity : sp.summe / netto };
}
function solarHTML(st) {
  var M = solarMonate(st), wp = zahl(st.wp); if (!(wp > 0)) return '';
  if (!M) return '<p class="vr-klein">Solar: ' + esc((E('strom', 'pv-ertrag-jahr') || [])[3] || '') + ' Das ist ein Jahresmittel – im Winter deutlich weniger. Nutzbar nur mit Speicher. ' + quelleHTML((E('strom', 'pv-ertrag-jahr') || [])[7]) + '</p>';
  var mo = solarMonat(st), jetzt = I.heute().getMonth(), max = Math.max.apply(null, M.map(function (v, i) { return v / MTAGE[i]; })), sl = solarLand(st), e = E('strom', sl === 'SL' || !E('strom', 'pv-orte') ? 'pv-monat' : 'pv-orte'), ng = String(st.neig || '30'), OO = solarOrte(), oo = OO && OO[sl];
  return '<div class="vr-solar"><div class="vr-felder">' + feld('Solar rechnen für', '<select class="vr-wahl" data-stz="monat"><option value="">aktueller Monat (' + MONAT[jetzt] + ')</option>' + MONAT.map(function (n, i) { return '<option value="' + i + '"' + (String(st.monat) === String(i) ? ' selected' : '') + '>' + n + '</option>'; }).join('') + '</select>') + feld('Standort', (function () { var O = solarOrte() || {}, l = solarLand(st); return '<select class="vr-wahl" data-stz="ort">' + Object.keys(O).sort(function (a, b) { return O[a].land.localeCompare(O[b].land, 'de'); }).map(function (k) { return '<option value="' + k + '"' + (k === l ? ' selected' : '') + '>' + esc(O[k].land) + ' (' + esc(O[k].ort) + ')</option>'; }).join('') + '</select>'; })()) + feld('Aufstellung', '<select class="vr-wahl" data-stz="neig">' + NEIG.map(function (n) { return '<option value="' + n[0] + '"' + (ng === n[0] ? ' selected' : '') + '>' + n[1] + ' – ' + n[2] + '</option>'; }).join('') + '</select>') + '</div>' +
    '<p class="vr-klein"><b>' + fz(wp) + ' Wp bringen im ' + MONAT[mo] + ' im Mittel rund ' + fz(solarWhTag(st, mo)) + ' Wh am Tag.</b> Nutzbar nur mit Speicher.' + (oo ? ' Gerechnet für ' + esc(oo.ort) + (oo.jahr && oo.jahr[ng] ? ', im Jahr ' + fz(oo.jahr[ng] * wp / 1000) + ' kWh' : '') + '.' : '') + '</p>' +
    '<ul class="vr-monate" role="list" aria-label="Solarertrag je Monat in Wattstunden am Tag">' + M.map(function (v, i) { var w = wp * v / MTAGE[i]; return '<li' + (i === mo ? ' class="is-an"' : '') + '><span>' + MONAT[i].slice(0, 3) + '</span><i style="--b:' + Math.round(v / MTAGE[i] / max * 100) + '%"></i><b>' + fz(w) + '</b></li>'; }).join('') + '</ul>' +
    '<p class="vr-klein">Wh am Tag je Monat. ' + esc(e[3]) + ' ' + quelleHTML(e[7]) + '</p>' + (e[6] ? '<p class="vr-klein">' + esc(e[6]) + '</p>' : '') +
    '</div>';
}
/* Kochwasser aus dem Speiseplan (Liter je Tag) und theoretischer Gasbedarf (g je Liter, ohne Verluste) */
function kochwasserProTag(St, h) { var A = K.alltag(St, h), z = K.zielTage(St), Tg = A.tage.slice(0, z), l = 0;
  Tg.forEach(function (t) { t.essen.forEach(function (e) { var r = K.GERICHTE.filter(function (x) { return x.id === e.id; })[0]; if (r && r.koch !== 'kalt') l += K.gerichtWerte(St, r).wasser * e.port / 1000; }); });
  return Tg.length ? l / Tg.length : 0; }
function stromHTML() {
  var St = S(), t = T('strom'), h0 = I.heute(), z = K.zielTage(St), O = OF(), st = St.strom || (St.strom = {}), R = stromRechnung(St);
  var h = kopf('strom', 'Strom & Wärme', 'Wie lange reichen Powerbank, Powerstation und Solar für eure wichtigsten Geräte? Was braucht ihr an Brennstoff, und wie bleibt ihr warm?');
  if (!t) return h + fehltHTML() + '</section>';
  h += '<div class="vr-karte vr-zahlkarte ' + (R.tage == null ? '' : R.tage >= z ? 'vr-gut' : R.tage >= Math.min(3, z) ? 'vr-mittel' : 'vr-schlecht') + '"><span class="vr-fl">Strom reicht</span>' +
    (R.tage == null ? '<b class="vr-gz vr-gz-t">–</b><small>Unten Geräte und Speicher eintragen.</small>' : '<b class="vr-gz">' + (isFinite(R.tage) ? I.tageZahl(R.tage) : '∞') + '</b><span class="vr-ge">' + (isFinite(R.tage) ? 'Tage' : 'solange die Sonne reicht') + '</span>' + balken(isFinite(R.tage) ? R.tage : z, z) +
      '<small>Bedarf ' + fz(R.bedarf) + ' Wh am Tag · Speicher ' + fz(R.speicher.summe) + ' Wh' + (R.solar ? ' · Solar Ø ' + fz(R.solar) + ' Wh am Tag (' + (R.monat != null ? MONAT[R.monat] : 'Jahresmittel') + ')' : '') + '</small>') + '</div>';
  /* Speicher */
  var pb = st.pb && st.pb.length ? st.pb : [{ mah: '', n: 1 }];
  h += '<h3>Speicher</h3><div class="vr-karte"><h4>Powerbanks</h4><ul class="vr-pbl" role="list">' + pb.map(function (p, i) { return '<li data-pb="' + i + '">' + feld('Kapazität', zahlIn('data-pbf="mah"', p.mah || '', 'mAh', 'z. B. 10.000', 'numeric')) + feld('Anzahl', zahlIn('data-pbf="n"', p.n || 1, '', '', 'numeric')) + (i ? '<button type="button" class="vr-x" data-pbweg aria-label="entfernen">✕</button>' : '') + '</li>'; }).join('') + '</ul>' +
    '<div class="vr-knoepfe"><button type="button" class="vr-knopf" data-pbneu>＋ weitere Powerbank</button></div><p class="vr-klein">' + esc((E('strom', 's-formel') || [])[3] || '') + ' ' + esc((E('strom', 's-powerbank-real') || [])[3] || '') + ' Gerechnet mit ' + fz(wert('strom', 's-powerbank-real', 0.75) * 100) + ' %. ' + quelleHTML((E('strom', 's-powerbank-real') || [])[7]) + '</p>' +
    '<div class="vr-felder">' + feld('Powerstation', zahlIn('data-stz="ps"', st.ps || '', 'Wh', 'laut Gerät')) + feld('Solarmodul(e)', zahlIn('data-stz="wp"', st.wp || '', 'Wp', 'Nennleistung')) + feld('Benzin für Stromerzeuger', zahlIn('data-stz="benzin"', st.benzin || '', 'l', '0')) + '</div>' +
    solarHTML(st) +
    (zahl(st.benzin) > 0 ? '<p class="vr-klein">Stromerzeuger: ' + esc((E('strom', 'g-verbrauch') || [])[3] || '') + ' ' + quelleHTML((E('strom', 'g-verbrauch') || [])[7]) + '</p>' + ['g-draussen', 'g-tanken', 'g-einspeisen'].map(function (id) { var e = E('strom', id); return e && e[6] ? '<p class="vr-warnung"><span aria-hidden="true">⚠</span> ' + esc(e[6]) + '</p>' : ''; }).join('') : '') + '</div>';
  /* Geräte */
  var G = St.stromG || [];
  h += '<h3>Geräte</h3><div class="vr-karte">' + (G.length ? '<ul class="vr-geraete" role="list">' + G.map(function (g, i) { var V0 = GER[g.typ] || GERAETE[GERAETE.length - 1], std = V0[3](), wh = geraetWh(g), e = GERQ[g.typ] ? E('strom', GERQ[g.typ]) : null;
      return '<li data-ge="' + i + '"><div class="vr-pk"><b>' + esc(g.n || V0[1]) + '</b><span>' + (wh > 0 ? fz(wh) + ' Wh am Tag' : 'Wert eintragen') + '</span></div><div class="vr-felder">' +
        (V0[2] !== 'tag' ? feld(V0[4], zahlIn('data-gef="menge"', g.menge || '', V0[2] === 'wh' ? '×' : 'h', '0')) : '') +
        feld(V0[2] === 'wh' ? 'Wh je Ladung' : V0[2] === 'w' ? 'Leistung' : 'Wh am Tag', zahlIn('data-gef="w"', g.w || '', V0[2] === 'w' ? 'W' : 'Wh', std > 0 ? fz(std, std % 1 ? 1 : 0) + (std > 0 && e ? ' (Richtwert)' : '') : 'eigener Wert')) + '</div>' +
        (e ? '<p class="vr-klein">' + esc(e[3]) + ' ' + quelleHTML(e[7]) + '</p>' : '') + '<button type="button" class="vr-x" data-geweg aria-label="Gerät entfernen">✕</button></li>'; }).join('') + '</ul>' : '<p class="vr-klein">Noch keine Geräte – unten antippen.</p>') +
    '<div class="vr-chips">' + GERAETE.map(function (g) { return '<button type="button" class="vr-chip" data-geneu="' + g[0] + '">＋ ' + esc(g[1]) + '</button>'; }).join('') + '</div>' +
    (function () { var e = E('strom', 'v-medizin'); return e ? '<p class="vr-warnung"><span aria-hidden="true">⚠</span> ' + esc(e[3]) + ' ' + esc(e[6] || '') + '</p>' : ''; })() + '</div>';
  /* Brennstoff fürs Kochen */
  var wl = kochwasserProTag(St, h0), gl = wert('waerme_kochen', 'b-gas-je-liter', null), kz = zahl((St.lage || {}).kartusche), PL = 0; K.alltag(St, h0).tage.slice(0, z).forEach(function (tg) { PL += tg.brenn || 0; });
  h += '<h3>Brennstoff fürs Kochen</h3><div class="vr-karte">' + ((St.lage || {}).koch === 'keine' ? '<p class="vr-klein">Ohne Kochstelle wird nichts gekocht – der Speiseplan nimmt nur kalte Gerichte.</p>' :
    '<ul class="vr-bedarf" role="list"><li><span>Kochwasser laut Speiseplan</span><b>' + liter(wl) + ' am Tag</b></li>' + (gl ? '<li><span>Gas theoretisch (' + fz(gl) + ' g je Liter, ohne Verluste)</span><b>' + fz(wl * gl) + ' g am Tag</b></li>' : '') +
    '<li><span>Flammzeit laut Speiseplan</span><b>' + fz(PL / Math.max(1, Math.min(z, K.alltag(St, h0).tage.length))) + ' min am Tag</b></li>' + (kz > 0 ? '<li><span>Kartuschen für ' + z + ' Tage (Brenndauer ' + fz(kz) + ' min)</span><b>' + Math.ceil(PL / kz) + ' Stück</b></li>' : '') + '</ul>' +
    '<p class="vr-klein">' + esc((E('waerme_kochen', 'b-gas-je-liter') || [])[3] || '') + ' ' + quelleHTML((E('waerme_kochen', 'b-gas-je-liter') || [])[7]) + '</p>' + (kz > 0 ? '' : '<p class="vr-klein">Für eine Kartuschen-Zahl die Brenndauer unter „Haushalt → Lage“ eintragen (steht im Datenblatt des Kochers).</p>')) + '</div>';
  h += '<p class="vr-klein">Die Kühlgeräte-Werte stammen aus 2012 (alte Effizienzklassen A+++ bis A) und sind mit den heutigen Klassen A–G nicht direkt vergleichbar. Werte „abgeleitet“ oder „umgerechnet“ sind aus den Quellangaben gerechnet (Richtwert).</p>';
  h += faktenHTML('waerme_kochen', ['Heizen']) + faktenHTML('waerme_kochen', ['Brennstoffe']) + faktenHTML('strom', ['Verbraucher', 'Speicher', 'Solar', 'Notstrom']);
  return h + '</section>';
}
H.uebersichtStrom = function (St, h, z) { var R = stromRechnung(St); if (R.tage == null) return null; return { amp: stufe(isFinite(R.tage) ? R.tage : 999, z), txt: 'Strom reicht ' + (isFinite(R.tage) ? tageText(R.tage) : 'mit Solar') + ' · ' + fz(R.bedarf) + ' Wh am Tag' }; };

/* ===================================================================== Kochen ohne Strom */
var KOCH_GERICHTE = ['kk_erbsen', 'kk_milchreis', 'kk_reis', 'kk_hirse', 'kk_quinoa', 'kk_polenta', 'kk_kartoffeln', 'kk_rotkohl', 'kk_linsen', 'kk_bohnen', 'kk_huehnersuppe', 'kk_gulasch', 'couscous_warm', 'bulgur', 'porridge'];
function kochenHTML() {
  var St = S(), t = T('waerme_kochen'), B = K.bestand(St, I.heute());
  var h = kopf('kochen', 'Kochen ohne Strom', 'Womit ihr sicher kocht, wie die Kochkiste Brennstoff spart, und welche Gerichte dazu passen.');
  if (!t) return h + fehltHTML() + '</section>';
  h += faktenHTML('waerme_kochen', ['Kochen', 'Kochkiste']);
  h += '<h3>Passende Gerichte</h3><p class="vr-klein">Kochkiste: geeignet laut BZfE; kurze Garzeit: Getreideflocken, Couscous, Bulgur (Verbraucherzentrale Niedersachsen). Antippen öffnet das Gericht.</p><ul class="vr-kgl" role="list">' + KOCH_GERICHTE.map(function (id) {
    var r = K.GERICHTE.filter(function (x) { return x.id === id; })[0]; if (!r) return ''; var st = K.gerichtStatus(St, r, B);
    return '<li><button type="button" class="vr-weg" data-kgoeffne="' + id + '"><span aria-hidden="true">' + (r.art === 'kiste' ? '🧺' : '🍲') + '</span><span><b>' + esc(r.n) + '</b><small>' + (r.art === 'kiste' ? 'Kochkiste' : 'kurze Garzeit') + ' · ' + (st.st === 'geht' ? 'geht jetzt' : st.st === 'fast' ? 'fast – es fehlt wenig' : 'fehlt einiges') + '</small></span><span aria-hidden="true">›</span></button></li>'; }).join('') + '</ul>';
  return h + '</section>';
}


/* ===================================================================== Familien-Notfallplan (Felder laut notfallplan.json; bleibt auf dem Gerät) */
function npFelder() { var t = T('notfallplan'); return t ? t.E : []; }
function npTyp(e) { return (e[8] && e[8].feldtyp) || 'text'; }
function npStand(St) { var n = 0, d = 0; npFelder().forEach(function (e) { var ty = npTyp(e); if (ty === 'text' || ty === 'liste' || ty === 'person') { n++; if (String((St.notfall || {})[e[0]] || '').trim()) d++; } }); return { n: n, d: d }; }
function notfallplanHTML() {
  var St = S(), t = T('notfallplan'), N = St.notfall || (St.notfall = {});
  var h = kopf('notfallplan', 'Familien-Notfallplan', 'Wo trefft ihr euch, wen ruft ihr an, wer kümmert sich um wen? Alles bleibt nur auf diesem Gerät und kommt mit aufs Notfall-Blatt.');
  if (!t) return h + fehltHTML() + '</section>';
  var a = npStand(St);
  h += '<div class="vr-karte vr-zahlkarte"><span class="vr-fl">Ausgefüllt</span><b class="vr-gz vr-gz-t">' + a.d + ' von ' + a.n + ' Feldern</b>' + balken(a.d, a.n, 'vr-gut') + '</div>';
  var nr = npFelder().filter(function (e) { return npTyp(e) === 'nummer' && e[4] != null; });
  h += '<h3>Wichtige Nummern</h3><ul class="vr-nummern" role="list">' + nr.map(function (e) { var num = String(e[4]); return '<li><a class="vr-tel" href="tel:' + esc(num.replace(/\s/g, '')) + '">' + esc(num.length === 6 && /^\d+$/.test(num) ? num.slice(0, 3) + ' ' + num.slice(3) : num) + '</a><span><b>' + esc(e[2]) + '</b><small>' + esc(e[3]) + '</small>' + quelleHTML(e[7]) + '</span></li>'; }).join('') + '</ul>';
  h += '<h3>Euer Plan</h3><div class="vr-np">' + npFelder().filter(function (e) { return !(npTyp(e) === 'nummer' && e[4] != null); }).map(function (e) {
    var ty = npTyp(e), v = N[e[0]];
    var eingabe = ty === 'haken' ? '<label class="vr-schalter"><input type="checkbox" data-np="' + e[0] + '"' + (v ? ' checked' : '') + '><span>' + esc(e[2]) + '</span></label>'
      : ty === 'liste' ? '<textarea class="vr-text" rows="3" data-np="' + e[0] + '" aria-label="' + esc(e[2]) + '" placeholder="eine Angabe je Zeile">' + esc(v || '') + '</textarea>'
      : '<span class="vr-ein"><input type="' + (ty === 'nummer' ? 'tel' : 'text') + '" data-np="' + e[0] + '" value="' + esc(v || '') + '" aria-label="' + esc(e[2]) + '" maxlength="200"></span>';
    return '<div class="vr-karte vr-npf' + (e[6] ? ' vr-fakt-w' : '') + '">' + (ty === 'haken' ? '' : '<b>' + esc(e[2]) + '</b>') + '<p class="vr-klein">' + esc(e[3]) + '</p>' + eingabe + (e[6] ? '<p class="vr-warnung"><span aria-hidden="true">⚠</span> ' + esc(e[6]) + '</p>' : '') + quelleHTML(e[7]) + '</div>'; }).join('') + '</div>';
  return h + '<p class="vr-klein">Druckt das Notfall-Blatt aus, damit die Angaben auch ohne Handy da sind (Haushalt &amp; Plan → Notfall-Blatt).</p></section>';
}
H.uebersichtNotfallplan = function (St) { var a = npStand(St); if (!a.n) return { amp: '', txt: 'Treffpunkte und Kontakte festlegen' }; return { amp: a.d === 0 ? 'rot' : a.d >= a.n * 0.6 ? 'gruen' : 'gelb', gross: a.d + ' von ' + a.n + ' Feldern', txt: a.d ? 'Treffpunkte, Kontakte, Aufgaben' : 'noch nichts eingetragen' }; };
H.blattNummern = function (St) { var L = npFelder().filter(function (e) { return npTyp(e) === 'nummer' && e[4] != null; }).map(function (e) { return [esc(String(e[4])), esc(e[2])]; });
  var eig = String((St.notfall || {})['nr-eigene'] || '').split(/\n+/).filter(function (x) { return x.trim(); }).map(function (x) { return [esc(x.trim()), 'eigene Nummer']; });
  var gift = String((St.notfall || {})['nr-gift-andere'] || '').trim(); if (gift) eig.push([esc(gift), 'Giftnotruf']);
  return L.concat(eig).concat(H.regionNummern ? H.regionNummern(St) : []); };
H.blattNotfallplan = function (St) { var N = St.notfall || {}, Z = npFelder().filter(function (e) { var ty = npTyp(e); return ty !== 'nummer' && String(N[e[0]] || '').trim() && N[e[0]] !== false; });
  return '<section><h2>Familien-Notfallplan</h2>' + (Z.length ? '<table class="vr-dt"><tbody>' + Z.map(function (e) { var v = N[e[0]]; return '<tr><th>' + esc(e[2]) + '</th><td>' + (v === true ? '☑' : esc(String(v)).replace(/\n/g, '<br>')) + '</td></tr>'; }).join('') + '</tbody></table>'
    : '<p>Treffpunkt nah: ____________________ · Treffpunkt fern: ____________________</p><p>Kontakte: ________________________________________________</p>') + '</section>'; };

/* ===================================================================== Ausrüstung: Checkliste mit Quellen (ausruestung.json) */
function ausrStand(St) { var t = T('ausruestung'); if (!t) return null; var d = 0; t.E.forEach(function (e) { if ((St.haken || {})['aus:' + e[0]]) d++; }); return { n: t.E.length, d: d }; }
H.bestaendeUnten = function () { var St = S(), t = T('ausruestung'); if (!t) return ''; var a = ausrStand(St);
  return '<h3>Checkliste nach BBK <small class="vr-zaehl">' + a.d + ' von ' + a.n + '</small></h3>' + balken(a.d, a.n, 'vr-gut') + gruppen('ausruestung').map(function (g) { var d = g.E.filter(function (e) { return St.haken['aus:' + e[0]]; }).length;
    return '<details class="vr-bk-gr"' + (OF()['au:' + g.t] ? ' open' : '') + ' data-au="' + esc(g.t) + '"><summary>' + esc(g.t) + ' <span class="vr-zaehl">' + d + '/' + g.E.length + '</span></summary><ul class="vr-fakten" role="list">' + g.E.map(function (e) {
      return '<li class="vr-fakt' + (e[6] ? ' vr-fakt-w' : '') + '"><label class="vr-fh"><input type="checkbox" data-aus="' + esc(e[0]) + '"' + (St.haken['aus:' + e[0]] ? ' checked' : '') + '><b>' + esc(e[2]) + '</b></label><p>' + esc(e[3]) + '</p>' + wertHTML(e) + (e[6] ? '<p class="vr-warnung"><span aria-hidden="true">⚠</span> ' + esc(e[6]) + '</p>' : '') + quelleHTML(e[7]) + '</li>'; }).join('') + '</ul></details>'; }).join(''); };
H.uebersichtAusruestung = function (St) { var a = ausrStand(St); return a ? { d: a.d, n: a.n } : null; };

/* ===================================================================== Nährstoff-Check über die geplanten Tage */
function vitCBedarf(p) { var a = zahl(p.a), m = p.s !== 'w', id = null; if (!isFinite(a) || a < 1) return null;
  id = a < 4 ? 'c-1-4' : a < 7 ? 'c-4-7' : a < 10 ? 'c-7-10' : a < 13 ? 'c-10-13' : a < 15 ? 'c-13-15' : a < 19 ? (m ? 'c-15-19-m' : 'c-15-19-w') : (m ? 'c-m' : 'c-w'); return wert('naehrstoffe', id, null); }
function ballaststoffBedarf(p, kcal) { var a = zahl(p.a); if (isFinite(a) && a < 19) { var w = wert('naehrstoffe', 'b-kind', null); return w != null ? w * kcal / 1000 : null; } return wert('naehrstoffe', 'b-erw', null); }
/* Mineralstoffe und Vitamine nach Alter und Geschlecht (DGE-Referenzwerte, naehrstoffe.json). Säuglinge (unter 1 Jahr) ohne Wert.
   Eisen: Frauen bis 50 mit dem Wert vor den Wechseljahren, ab 51 danach (Annahme). Zink: Wert bei mittlerer Phytatzufuhr. */
var MIKRO = {
  ca: function (a, m) { return a < 4 ? 'ca-1-4' : a < 7 ? 'ca-4-7' : a < 10 ? 'ca-7-10' : a < 13 ? 'ca-10-13' : a < 19 ? 'ca-13-19' : 'ca-erw'; },
  fe: function (a, m) { return a < 7 ? 'fe-1-7' : a < 10 ? 'fe-7-10' : a < 13 ? 'fe-10-13' : a < 19 ? (m ? 'fe-13-19-m' : 'fe-13-19-w') : m ? 'fe-m' : a < 51 ? 'fe-w-prae' : 'fe-w-post'; },
  mg: function (a, m) { return a < 4 ? 'mg-1-4' : a < 7 ? 'mg-4-7' : a < 10 ? 'mg-7-10' : a < 13 ? (m ? 'mg-10-13-m' : 'mg-10-13-w') : a < 15 ? (m ? 'mg-13-15-m' : 'mg-13-15-w') : a < 19 ? (m ? 'mg-15-19-m' : 'mg-15-19-w') : m ? 'mg-m' : 'mg-w'; },
  zn: function (a, m) { return a < 4 ? 'zn-1-4' : a < 7 ? 'zn-4-7' : a < 10 ? 'zn-7-10' : a < 13 ? (m ? 'zn-10-13-m' : 'zn-10-13-w') : a < 15 ? (m ? 'zn-13-15-m' : 'zn-13-15-w') : a < 19 ? (m ? 'zn-15-19-m' : 'zn-15-19-w') : m ? 'zn-m' : 'zn-w'; },
  fol: function (a) { return a < 4 ? 'fol-1-4' : a < 7 ? 'fol-4-7' : a < 10 ? 'fol-7-10' : a < 13 ? 'fol-10-13' : 'fol-13'; },
  b12: function (a) { return a < 4 ? 'b12-1-4' : a < 7 ? 'b12-4-7' : a < 10 ? 'b12-7-10' : a < 13 ? 'b12-10-13' : 'b12-13'; }
};
var MIKRO_K = ['ca', 'fe', 'mg', 'zn', 'fol', 'b12'];
function mikroBedarf(key, p) { var a = zahl(p.a); if (!isFinite(a) || a < 1 || !MIKRO[key]) return null; return wert('naehrstoffe', MIKRO[key](a, p.s !== 'w'), null); }
function calciumBedarf(p) { return mikroBedarf('ca', p); }
function eisenBedarf(p) { return mikroBedarf('fe', p); }
function naehrBedarf(St) { var Hh = K.haushalt(St), r = { e: Hh.eiweiss, f: 0, b: 0, vc: 0, fehlt: [], fehltM: {} }, fa = wert('naehrstoffe', 'f-erw', null);
  MIKRO_K.forEach(function (k) { r[k] = 0; r.fehltM[k] = []; });
  Hh.P.forEach(function (x) { if (fa != null) r.f += x.b.kcal * fa / 100 / 9; var b = ballaststoffBedarf(x.p, x.b.kcal); if (b != null) r.b += b; var c = vitCBedarf(x.p); if (c != null) r.vc += c; else r.fehlt.push(x.p.n || 'Person');
    MIKRO_K.forEach(function (k) { var w = mikroBedarf(k, x.p); if (w != null) r[k] += w; else r.fehltM[k].push(x.p.n || 'Person'); }); });
  r.fehltCa = r.fehltM.ca; r.fehltFe = r.fehltM.fe; return r; }
/* Nährstoffe eines Tages aus dem Plan (Gerichte: erste genannte Zutat je Portion; Auffüllen: tatsächliches Lebensmittel) */
var NK = ['e', 'f', 'b', 'vc'].concat(MIKRO_K), UNB = ['vc'].concat(MIKRO_K);
function naehrLeer() { var r = { kcal: 0, unb: {} }; NK.forEach(function (k) { r[k] = 0; }); UNB.forEach(function (k) { r.unb[k] = 0; }); return r; }
function naehrTag(St, t) { var r = naehrLeer();
  var dazu = function (k, g) { if (!k) return; var f = g / 100; r.e += (k.e || 0) * f; r.f += (k.f || 0) * f; r.b += (k.b || 0) * f; r.kcal += (k.k || 0) * f;
    UNB.forEach(function (n) { if (k[n] != null) r[n] += k[n] * f; else if (k.k > 0) r.unb[n] += (k.k || 0) * f; }); };
  t.essen.forEach(function (e) { var g0 = K.GERICHTE.filter(function (x) { return x.id === e.id; })[0]; if (!g0) return; g0.zut.forEach(function (z) { if (z.opt) return; dazu(K.katVon(St, z.a[0][0]), z.g / g0.p * e.port); }); });
  t.extra.forEach(function (x) { dazu(K.katVon(St, x.i), x.g); });
  r.unbekanntVc = r.unb.vc; r.unbekanntCa = r.unb.ca; r.unbekanntFe = r.unb.fe; return r; }
function naehrCheck(St, h, P) {
  var B = naehrBedarf(St), T0 = (P || I.planZiel()).tage.filter(function (t) { return t.kcal > 0; }), sum = naehrLeer(), unter = {};
  NK.forEach(function (k) { unter[k] = 0; });
  T0.forEach(function (t) { var n = naehrTag(St, t); NK.forEach(function (k) { sum[k] += n[k]; if (B[k] > 0 && n[k] < B[k] * 0.9) unter[k]++; }); sum.kcal += n.kcal; UNB.forEach(function (k) { sum.unb[k] += n.unb[k]; }); });
  var d = T0.length || 1, schnitt = {}, unb = {}; NK.forEach(function (k) { schnitt[k] = sum[k] / d; }); UNB.forEach(function (k) { unb[k] = sum.kcal ? sum.unb[k] / sum.kcal : 0; });
  return { bedarf: B, schnitt: schnitt, tage: T0.length, unter: unter, unb: unb, unbekanntVc: unb.vc, unbekanntCa: unb.ca, unbekanntFe: unb.fe };
}
/* Womit aus dem Vorrat ausgleichen: Lebensmittel im Lager mit dem höchsten Gehalt je 100 kcal */
function ausgleich(St, h, key) { return K.posten(St, h).filter(function (x) { return x.k[key] > 0 && x.k.k > 0 && x.k.g !== 'baby'; }).sort(function (a, b) { return b.k[key] / b.k.k - a.k[key] / a.k.k; }).filter(function (x, i, A) { return A.findIndex(function (y) { return y.k.i === x.k.i; }) === i; }).slice(0, 3); }
var NAEHR = [['e', 'Eiweiß', 'g', 'p-19-65'], ['f', 'Fett', 'g', 'f-erw'], ['b', 'Ballaststoffe', 'g', 'b-erw'], ['vc', 'Vitamin C', 'mg', 'c-m'], ['ca', 'Calcium', 'mg', 'ca-erw'], ['fe', 'Eisen', 'mg', 'fe-m'], ['mg', 'Magnesium', 'mg', 'mg-m'], ['zn', 'Zink', 'mg', 'zn-m'], ['fol', 'Folat', 'µg', 'fol-13'], ['b12', 'Vitamin B12', 'µg', 'b12-13']];
function naehrHTML() {
  var St = S(), h0 = I.heute(), t = T('naehrstoffe'), z = K.zielTage(St);
  var h = kopf('naehrstoffe', 'Nährstoff-Check', 'Deckt der Speiseplan der nächsten ' + z + ' Tage Eiweiß, Fett, Ballaststoffe, Vitamin C, Calcium, Eisen, Magnesium, Zink, Folat und Vitamin B12? Und womit lässt sich aus dem Vorrat ausgleichen?');
  if (!t) return h + fehltHTML() + '</section>';
  if (!St.personen.length || !St.lager.length) return h + '<div class="vr-leer"><p>Dafür braucht es Personen und Vorrat.</p></div></section>';
  var P = I.planZiel(), C = naehrCheck(St, h0, P);
  h += '<p class="vr-klein">Grundlage: ' + (P.sparsam ? 'sparsamer' : 'satter') + ' Speiseplan, ' + C.tage + ' Tage mit Essen. Gerichte mit der ersten genannten Zutat gerechnet, Werte roh (ohne Kochverluste). Bedarf: DGE-Referenzwerte für gesunde Menschen.</p>';
  h += '<div class="vr-naehr">' + NAEHR.filter(function (n) { return C.bedarf[n[0]] > 0; }).map(function (n) { var ist = C.schnitt[n[0]], soll = C.bedarf[n[0]], p = soll ? ist / soll : 0, A = ausgleich(St, h0, n[0]);
    return '<div class="vr-karte ' + (p >= 0.9 ? 'vr-gut' : p >= 0.6 ? 'vr-mittel' : 'vr-schlecht') + '"><span class="vr-fl">' + n[1] + '</span><b class="vr-nz">' + fz(ist, ist < 10 ? 1 : 0) + ' ' + n[2] + ' <small>von ' + fz(soll) + ' ' + n[2] + ' am Tag</small></b>' + balken(ist, soll) +
      '<small>' + fz(p * 100) + ' % im Schnitt · ' + C.unter[n[0]] + ' von ' + C.tage + ' Tagen unter 90 %</small>' + (p < 0.9 && A.length ? '<small class="vr-ausgl">Ausgleichen mit: ' + A.map(function (x) { return esc(x.it.n || x.k.n.replace(/ \(.*\)$/, '')); }).join(', ') + '</small>' : '') + '</div>'; }).join('') + '</div>';
  if (C.unbekanntVc > 0.05) h += '<p class="vr-klein">Für ' + fz(C.unbekanntVc * 100) + ' % der Kalorien fehlt ein belegter Vitamin-C-Wert (z. B. Öle, Honig); sie zählen mit 0.</p>';
  var ohne = Math.max.apply(null, MIKRO_K.map(function (k) { return C.unb[k] || 0; }));
  if (ohne > 0.05) h += '<p class="vr-klein">Mineralstoffe und Vitamine: Für bis zu ' + fz(ohne * 100) + ' % der Kalorien fehlt ein belegter Wert (z. B. Kaffee, Tee, Wasser, Säuglingsnahrung); sie zählen mit 0. Der Vorrat kann also mehr liefern, als hier steht.</p>';
  var ohneP = {}; MIKRO_K.forEach(function (k) { C.bedarf.fehltM[k].forEach(function (n) { ohneP[n] = 1; }); });
  if (Object.keys(ohneP).length) h += '<p class="vr-klein">Ohne Bedarf für Mineralstoffe und B-Vitamine (Säugling oder Alter fehlt): ' + Object.keys(ohneP).map(esc).join(', ') + '.</p>';
  h += '<p class="vr-klein">[Ergänzung] Eisen: Für Frauen bis 50 Jahre rechnet der Check mit dem Wert vor den Wechseljahren, ab 51 mit dem danach. Zink: Wert bei mittlerer Phytatzufuhr (viel Vollkorn und Hülsenfrüchte → mehr nötig). Schwangere und Stillende brauchen teils mehr (siehe Referenzwerte).</p>';
  h += '<p class="vr-klein">Gehalte: USDA FoodData Central, SR Legacy (2018), je 100 g, Folat ohne zugesetzte Folsäure; wo USDA nur angereicherte US-Ware führt oder keinen Wert hat (Brot, Nudeln, Reis, Mehl, Öle, Fette u. a.), ergänzt aus Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS) 4.0, CC BY 4.0, Werte ausgewählt und gerundet. Der Check zählt die enthaltene Menge, nicht, wie viel der Körper davon aufnimmt. Vitamin B12 steckt fast nur in tierischen Lebensmitteln.</p>';
  if (C.bedarf.fehlt.length) h += '<p class="vr-klein">Ohne Vitamin-C-Bedarf (Säugling oder Alter fehlt): ' + C.bedarf.fehlt.map(esc).join(', ') + '.</p>';
  h += '<h3>Einordnen: Was in 10 Tagen zählt</h3>' + faktenHTML('naehrstoffe', ['Einordnung'], 4) + faktenHTML('naehrstoffe', ['Vitamin-C-Quellen'], 4);
  h += '<details class="vr-mehr"><summary>Alle Referenzwerte mit Quellen</summary>' + faktenHTML('naehrstoffe', ['Energie', 'Eiweiß', 'Makronährstoffe', 'Vitamin C', 'Calcium', 'Eisen', 'Magnesium', 'Zink', 'Folat', 'Vitamin B12'], 4) + '</details>';
  return h + '</section>';
}


/* ===================================================================== Region (region_saarland.json): Warnwege, Zuständigkeit, Anlaufstellen, Störungsnummern */
var REGION_OBER = { 'Landeshauptstadt Saarbrücken': 'Regionalverband Saarbrücken', 'Heusweiler': 'Regionalverband Saarbrücken', 'Quierschied': 'Regionalverband Saarbrücken', 'Homburg (Saarpfalz-Kreis)': 'Saarpfalz-Kreis', 'Völklingen': 'Regionalverband Saarbrücken', 'Sulzbach/Saar': 'Regionalverband Saarbrücken', 'Neunkirchen': 'Landkreis Neunkirchen', 'Saarlouis': 'Landkreis Saarlouis', 'Dillingen/Saar': 'Landkreis Saarlouis', 'Saarwellingen': 'Landkreis Saarlouis', 'Merzig': 'Landkreis Merzig-Wadern', 'St. Ingbert': 'Saarpfalz-Kreis', 'Bexbach': 'Saarpfalz-Kreis' };
function regionGebiete() { var t = T('region_saarland'), G = []; if (!t) return G; t.E.forEach(function (e) { var g = e[8] && e[8].gebiet; if (g && g !== 'Saarland' && g !== 'andere Bundesländer' && G.indexOf(g) < 0) G.push(g); }); return G; }
/* Einträge für die Auswahl: Saarland allgemein + Kreis + Ort; anderes Bundesland: nur der allgemeine Block */
function regionEintraege(r) { var t = T('region_saarland'); if (!t || !r || !r.land) return [];
  if (r.land !== 'SL') return t.E.filter(function (e) { return e[8] && e[8].gebiet === 'andere Bundesländer'; });
  var G = ['Saarland']; if (r.gebiet) { G.push(r.gebiet); if (REGION_OBER[r.gebiet]) G.push(REGION_OBER[r.gebiet]); }
  return t.E.filter(function (e) { return e[8] && G.indexOf(e[8].gebiet) >= 0; }); }
function telNummer(w) { return typeof w === 'string' && /^[0-9 ()\/+-]{3,}$/.test(w) && /\d{3}/.test(w); }
function regionHTML() {
  var St = S(), t = T('region_saarland'), r = St.region || {};
  var h = kopf('region', 'Region', 'Wie ihr gewarnt werdet, wer zuständig ist, wo es Anlaufstellen gibt und welche Störungsnummern gelten. Für das Saarland nach Kreis und Ort, für andere Länder der allgemeine Teil.');
  if (!t) return h + fehltHTML() + '</section>';
  var G = regionGebiete(), kreise = G.filter(function (g) { return /kreis|verband/i.test(g); }), orte = G.filter(function (g) { return kreise.indexOf(g) < 0; });
  h += '<div class="vr-karte"><div class="vr-felder">' + feld('Bundesland', seg('rg:land', [['SL', 'Saarland'], ['andere', 'anderes Bundesland']], r.land || ''), 'vr-voll') +
    (r.land === 'SL' ? feld('Kreis oder Ort (freiwillig)', '<select data-rg="gebiet"><option value="">nur Saarland allgemein</option><optgroup label="Kreise">' + kreise.map(function (g) { return '<option' + (r.gebiet === g ? ' selected' : '') + '>' + esc(g) + '</option>'; }).join('') + '</optgroup><optgroup label="Orte mit eigenen Angaben">' + orte.map(function (g) { return '<option' + (r.gebiet === g ? ' selected' : '') + '>' + esc(g) + '</option>'; }).join('') + '</optgroup></select>', 'vr-voll') : '') + '</div>' +
    '<p class="vr-klein">Die Auswahl bleibt auf diesem Gerät. Für andere Orte im Saarland gelten der Kreis und die allgemeinen Angaben.</p></div>';
  if (!r.land) return h + '<div class="vr-leer"><p>Wähle oben dein Bundesland.</p></div></section>';
  var L = regionEintraege(r), nr = L.filter(function (e) { return telNummer(e[4]); });
  if (nr.length) h += '<h3>Nummern</h3><ul class="vr-nummern" role="list">' + nr.map(function (e) { return '<li><a class="vr-tel" href="tel:' + esc(String(e[4]).replace(/[^0-9+]/g, '')) + '">' + esc(e[4]) + '</a><span><b>' + esc(e[2]) + '</b><small>' + esc(e[3]) + '</small>' + (e[6] ? '<span class="vr-warnung"><span aria-hidden="true">⚠</span> ' + esc(e[6]) + '</span>' : '') + quelleHTML(e[7]) + '</span></li>'; }).join('') + '</ul>';
  var Gr = []; L.filter(function (e) { return !telNummer(e[4]); }).forEach(function (e) { var g = Gr.filter(function (x) { return x.t === e[1]; })[0]; if (!g) { g = { t: e[1], E: [] }; Gr.push(g); } g.E.push(e); });
  h += Gr.map(function (g) { return '<h3>' + esc(g.t) + '</h3><ul class="vr-fakten" role="list">' + g.E.map(function (e) { return eintragHTML(e); }).join('') + '</ul>'; }).join('');
  if (r.land === 'SL') {
    /* Eine veröffentlichte Liste von Anlaufstellen liegt laut Belegen nur für Homburg bzw. den Saarpfalz-Kreis vor (Feuerwehrgerätehäuser) */
    var mitListe = r.gebiet === 'Homburg (Saarpfalz-Kreis)' || r.gebiet === 'Saarpfalz-Kreis';
    if (!mitListe) h += '<p class="vr-hinweis2">Notfalltreffpunkte: Für ' + esc(r.gebiet || 'das Saarland allgemein') + ' liegt keine veröffentlichte amtliche Liste vor – bitte bei der Gemeinde nachfragen (Behördennummer 115).</p>';
    h += '<h3>Abweichende Angaben</h3><div class="vr-widerspruch">' +
      '<div class="vr-karte"><b>Wie lange vorsorgen?</b><p>BBK: möglichst <b>10 Tage</b> (mindestens 3). Regionalverband Saarbrücken und Saarpfalz-Kreis: <b>14 Tage</b>.</p><p class="vr-klein">Beide Angaben stehen nebeneinander; das Ziel stellst du unter „Haushalt → Lage“ ein (14 Tage ist wählbar).</p>' + quelleHTML((E('region_saarland', 'rv-vorrat') || [])[7]) + '</div>' +
      '<div class="vr-karte"><b>Giftnotruf</b><p>Für das Saarland gilt <b>06131 19240</b> (Giftinformationszentrum Mainz, seit 01.04.2021). Die Nummer <b>06841 19240</b> (Homburg) steht noch auf einigen Kreis- und Gemeindeseiten; die Beratung dort endete am 31.03.2021.</p><p class="vr-klein">Im Zweifel 112.</p>' + quelleHTML((E('notfallplan', 'nr-gift-saar') || [])[7]) + '</div></div>';
    h += '<h3>Radio</h3><p class="vr-klein">Vom Sender Göttelborner Höhe: <b>SR 1 auf 88,0 MHz</b>, <b>SR 3 Saarlandwelle auf 95,5 MHz</b> (laut Wikipedia, nicht amtlich – eine Liste des SR wurde nicht gefunden). Passt der Empfang nicht: Sendersuchlauf. Aktuelles bei <a href="https://www.sr.de/" target="_blank" rel="noopener">sr.de</a>.</p>';
    h += '<p class="vr-klein">Das Notfall-Blatt übernimmt die Nummern dieser Auswahl.</p>'; }
  return h + '</section>';
}
H.lageHinweis = function (St) { var r = St.region || {}; return r.land === 'SL' && E('region_saarland', 'rv-vorrat') ? '<p class="vr-klein">Regionalverband Saarbrücken und Saarpfalz-Kreis empfehlen 14 Tage (BBK: 10 Tage) – siehe „Notfall → Region“.</p>' : ''; };
H.regionNummern = function (St) { return regionEintraege(St.region || {}).filter(function (e) { return telNummer(e[4]); }).map(function (e) { return [esc(e[4]), esc(e[2])]; }); };
H.blattRegion = function (St) { var L = regionEintraege(St.region || {}).filter(function (e) { return !telNummer(e[4]) && /Warnwege|Anlaufstellen/.test(e[1]); }); if (!L.length) return '';
  return '<section><h2>Region: Warnung und Anlaufstellen</h2><ul>' + L.map(function (e) { return '<li><b>' + esc(e[2]) + ':</b> ' + esc(e[3]) + '</li>'; }).join('') + '</ul></section>'; };

/* ===================================================================== Ereignisse */
H.klick.push(function (t, a) {
  var St = S(), O = OF();
  if (t.hasAttribute('data-ablauf-neu')) { I.undo(I.klon(St)); St.ablauf = {}; I.nachAenderung(true); I.toast('Haken entfernt.', true); return true; }
  if (t.hasAttribute('data-set') && a('data-set') === 'rg:land') { St.region = St.region || {}; St.region.land = a('data-wert'); if (St.region.land !== 'SL') St.region.gebiet = ''; I.nachAenderung(true); return true; }
  if (t.hasAttribute('data-set') && a('data-set') === 'wq:toilette') { St.wasserQ = St.wasserQ || {}; St.wasserQ.toilette = a('data-wert'); I.nachAenderung(true); return true; }
  if (t.hasAttribute('data-pbneu')) { St.strom = St.strom || {}; St.strom.pb = (St.strom.pb && St.strom.pb.length ? St.strom.pb : [{ mah: '', n: 1 }]).concat([{ mah: '', n: 1 }]); I.nachAenderung(true); return true; }
  if (t.hasAttribute('data-pbweg')) { var i = +t.closest('[data-pb]').getAttribute('data-pb'); St.strom.pb.splice(i, 1); I.nachAenderung(true); return true; }
  if (t.hasAttribute('data-geneu')) { var g = GER[a('data-geneu')]; St.stromG = St.stromG || []; St.stromG.push({ typ: g[0], n: g[0] === 'eigen' ? '' : g[1], menge: '', w: '' }); I.nachAenderung(true); return true; }
  if (t.hasAttribute('data-geweg')) { var j = +t.closest('[data-ge]').getAttribute('data-ge'); I.undo(I.klon(St)); St.stromG.splice(j, 1); I.nachAenderung(true); I.toast('Gerät entfernt.', true); return true; }
  if (t.hasAttribute('data-kgoeffne')) { O['g:' + a('data-kgoeffne')] = true; O['gl:geht'] = true; O['gl:fast'] = true; O['gl:rest'] = true; I.tab('gerichte'); setTimeout(function () { var el = I.wurzel().querySelector('[data-g="' + a('data-kgoeffne') + '"]'); if (el) el.scrollIntoView({ block: 'center' }); }, 50); return true; }
  return false;
});
H.aenderung.push(function (t) {
  var St = S();
  if (t.hasAttribute('data-rg')) { St.region = St.region || {}; St.region[t.getAttribute('data-rg')] = t.value; I.nachAenderung(true); return true; }
  if (t.hasAttribute('data-np')) { St.notfall = St.notfall || {}; St.notfall[t.getAttribute('data-np')] = t.type === 'checkbox' ? t.checked : t.value; I.nachAenderung(true); return true; }
  if (t.hasAttribute('data-aus')) { St.haken = St.haken || {}; if (t.checked) St.haken['aus:' + t.getAttribute('data-aus')] = 1; else delete St.haken['aus:' + t.getAttribute('data-aus')]; var d = t.closest('[data-au]'); if (d) OF()['au:' + d.getAttribute('data-au')] = true; I.nachAenderung(true); return true; }
  if (t.hasAttribute('data-ablauf')) { St.ablauf = St.ablauf || {}; if (t.checked) St.ablauf[t.getAttribute('data-ablauf')] = 1; else delete St.ablauf[t.getAttribute('data-ablauf')]; I.nachAenderung(true); return true; }
  if (t.hasAttribute('data-wq')) { St.wasserQ = St.wasserQ || {}; St.wasserQ[t.getAttribute('data-wq')] = t.checked; I.nachAenderung(true); return true; }
  if (t.hasAttribute('data-wqq') || t.hasAttribute('data-wqz') || t.hasAttribute('data-stz') || t.hasAttribute('data-pbf') || t.hasAttribute('data-gef')) { I.nachAenderung(true); return true; }
  return false;
});
H.eingabe.push(function (t) {
  var St = S();
  if (t.hasAttribute('data-np') && t.type !== 'checkbox') { St.notfall = St.notfall || {}; St.notfall[t.getAttribute('data-np')] = t.value; I.sichern(); return true; }
  if (t.hasAttribute('data-wqq')) { St.wasserQ = St.wasserQ || {}; St.wasserQ.q = St.wasserQ.q || {}; St.wasserQ.q[t.getAttribute('data-wqq')] = t.value.trim(); I.sichern(); return true; }
  if (t.hasAttribute('data-wqz')) { St.wasserQ = St.wasserQ || {}; St.wasserQ[t.getAttribute('data-wqz')] = t.value.trim(); I.sichern(); return true; }
  if (t.hasAttribute('data-stz')) { St.strom = St.strom || {}; St.strom[t.getAttribute('data-stz')] = t.value.trim(); I.sichern(); return true; }
  if (t.hasAttribute('data-pbf')) { St.strom = St.strom || {}; St.strom.pb = St.strom.pb && St.strom.pb.length ? St.strom.pb : [{ mah: '', n: 1 }]; St.strom.pb[+t.closest('[data-pb]').getAttribute('data-pb')][t.getAttribute('data-pbf')] = t.value.trim(); I.sichern(); return true; }
  if (t.hasAttribute('data-gef')) { var g = (St.stromG || [])[+t.closest('[data-ge]').getAttribute('data-ge')]; if (g) { g[t.getAttribute('data-gef')] = t.value.trim(); I.sichern(); } return true; }
  return false;
});

var B = I.BEREICH;
B.ablauf = ablaufHTML; B.wasser = wasserHTML; B.strom = stromHTML; B.kochen = kochenHTML; B.notfallplan = notfallplanHTML; B.naehrstoffe = naehrHTML; B.region = regionHTML;
V._notfall = { F: F, T: T, E: E, wert: wert, ablaufStand: ablaufStand, geraetWh: geraetWh, speicherWh: speicherWh, solarWhTag: solarWhTag, solarMonate: solarMonate, stromRechnung: stromRechnung, kochwasserProTag: kochwasserProTag, npStand: npStand, regionEintraege: regionEintraege, regionGebiete: regionGebiete, telNummer: telNummer, naehrBedarf: naehrBedarf, calciumBedarf: calciumBedarf, eisenBedarf: eisenBedarf, mikroBedarf: mikroBedarf, naehrTag: naehrTag, naehrCheck: naehrCheck, vitCBedarf: vitCBedarf, ausgleich: ausgleich, ausrStand: ausrStand, GERAETE: GERAETE, KOCH_GERICHTE: KOCH_GERICHTE, eintragHTML: eintragHTML };
if (typeof module !== 'undefined' && module.exports) module.exports = V._notfall;
})(typeof window !== 'undefined' ? window : globalThis);
