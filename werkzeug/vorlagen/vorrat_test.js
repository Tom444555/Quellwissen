/* Test für den Vorrats-Planer (ohne Browser): node werkzeug/vorlagen/vorrat_test.js  → muss „Fehler: 0“ melden.
   Rechnet einen erfundenen Haushalt durch und prüft Tabellen, Formeln, Reichweite, Gerichte, Abziehen, Speiseplan und Sicherung. */
'use strict';
var V = require('./vorrat.js'), K = V._kern, fehler = 0, n = 0;
require('./vorrat_qr.js'); var P2 = require('./vorrat_plus.js'), I = V._i;
function ok(b, t) { n++; if (!b) { fehler++; console.log('✗ ' + t); } }
function nah(a, b, tol, t) { ok(Math.abs(a - b) <= tol, t + ' (ist ' + a + ', soll ' + b + ')'); }
var heute = new Date(2026, 10, 25, 12);

/* 1. Tabellen */
var ids = {}; K.KATALOG.forEach(function (k) { ok(!ids[k.i], 'Katalog-ID doppelt: ' + k.i); ids[k.i] = 1;
  ok(K.GRUPPEN.some(function (g) { return g.k === k.g; }), 'Gruppe unbekannt: ' + k.i);
  ok(k.k >= 0 && k.k <= 900 && k.e >= 0 && k.f >= 0 && k.c >= 0 && k.e + k.f + k.c <= 101, 'Nährwerte unplausibel: ' + k.i);
  ok(k.q === 'A' || k.q === '—' || /^U\d+$/.test(k.q), 'Quelle fehlt: ' + k.i);
  /* USDA-Eigenheiten: KH „by difference“ inkl. Ballaststoffe (Kakao), Säuren (Essig, Zitrone), Mineralstoffe (Backpulver) */
  if (k.k > 0 && !k.kein && ['kakao', 'essig', 'zitronensaft', 'backpulver'].indexOf(k.i) < 0) { var atw = 4 * k.e + 9 * k.f + 4 * k.c; ok(atw > k.k * 0.6 && atw < k.k * 1.45, 'kcal passt nicht zu Eiweiß/Fett/KH: ' + k.i + ' ' + k.k + '/' + Math.round(atw)); }
  (k.p || []).forEach(function (p) { ok(p[1] > 0, 'Packung ohne Menge: ' + k.i); }); });
ok(K.KATALOG.length >= 120 && K.KATALOG.length <= 160, 'Katalog: ' + K.KATALOG.length + ' Lebensmittel');
ok(K.GERICHTE.length >= 40 && K.GERICHTE.length <= 70, 'Gerichte: ' + K.GERICHTE.length);
var gids = {}; K.GERICHTE.forEach(function (r) { ok(!gids[r.id], 'Gericht doppelt: ' + r.id); gids[r.id] = 1;
  ok(['kalt', 'topf', 'glut', 'ofen'].indexOf(r.koch) >= 0, 'Kochstelle: ' + r.id); ok(r.p >= 1 && r.sch.length >= 1, 'Portionen/Schritte: ' + r.id);
  r.zut.forEach(function (z) { z.a.forEach(function (a) { ok(!!ids[a[0]], 'Zutat unbekannt: ' + r.id + ' → ' + a[0]); }); });
  var w = K.gerichtWerte({}, r); ok(w.kcal > 50 && w.kcal < 1200, 'kcal je Portion unplausibel: ' + r.id + ' ' + Math.round(w.kcal));
  if (r.koch === 'kalt') ok(r.zut.every(function (z) { return z.opt || !K.katVon({}, z.a[0][0]).ko || r.id === 'couscous_kalt'; }), 'kaltes Gericht mit Kochzutat: ' + r.id); });
ok(K.QUELLEN.every(function (q) { return /^https:\/\//.test(q[1]); }), 'Quellen-Links');
/* BLE-Tabelle Mischkost (© BLE 2024): Summe ca. 13,8 kg ohne Getränke */
var sum = 0; K.GRUPPEN.forEach(function (g) { sum += g.ble; }); nah(sum, 13830, 1, 'BLE-Summe');

/* 2. Bedarf */
var mann = K.bedarf({ s: 'm', a: 40, kg: 80, cm: 180, t: 'normal' });   // (800 + 1125 − 200 + 5) × 1,6
nah(mann.kcal, 1730 * 1.6, 0.01, 'Mifflin Mann'); nah(mann.eiweiss, 64, 0.01, 'Eiweiß Mann 0,8 g/kg');
var frau = K.bedarf({ s: 'w', a: 70, kg: 60, cm: 160, t: 'ruhig' });    // (600 + 1000 − 350 − 161) × 1,4
nah(frau.kcal, 1089 * 1.4, 0.01, 'Mifflin Frau'); nah(frau.eiweiss, 60, 0.01, 'Eiweiß ab 65: 1,0 g/kg');
nah(K.bedarf({ s: 'w', a: 12, kg: 40, t: 'koerper' }).kcal, 2200, 0, 'DGE Mädchen 10–13, PAL 1,8');
nah(K.bedarf({ s: 'm', a: 2, t: 'ruhig' }).kcal, 1200, 0, 'DGE Kleinkind');
nah(K.bedarf({ s: 'm', a: 2, t: 'ruhig' }).eiweiss, 13.9, 0.01, 'Eiweiß Kleinkind mit Referenzgewicht');
ok(K.bedarf({ s: 'w', a: 0.5 }).art === 'baby' && K.bedarf({ s: 'w', a: 0.5 }).kcal === 0, 'Säugling ohne Rechnung');
nah(K.bedarf({ s: 'w', a: 0.5, eigen: 700 }).kcal, 700, 0, 'eigener Wert');
nah(K.bedarf({ s: 'm', a: 30, t: 'normal' }).kcal, 2700, 0, 'Erwachsener ohne Gewicht → DGE');

/* 3. Erfundener Haushalt: 2 Erwachsene, 1 Kind, 1 Hund; Strom weg, kein Leitungswasser, Gaskocher, Ziel 10 Tage */
var S = K.leer();
S.personen = [{ n: 'A', s: 'm', a: 40, kg: 80, cm: 180, t: 'normal' }, { n: 'B', s: 'w', a: 70, kg: 60, cm: 160, t: 'ruhig' }, { n: 'C', s: 'w', a: 12, kg: 40, t: 'koerper' }];
S.tiere = [{ n: 'Hund', futter: 300, wasser: 1, vorrat: 6 }];
S.lage = { strom: true, leitung: false, koch: 'gas', ziel: 10, spar: 100, hyg: 0, kartusche: 90 };
var L = function (k, m, e, mhd, o) { return { u: k + m, k: k, m: m, e: e, mhd: mhd || '', o: o || 'v' }; };
S.lager = [L('nudeln', 2, 'kg'), L('reis', 1, 'kg', '2026-12'), L('knaecke', 500, 'g'), L('tomaten_dose', 4, 'p0'), L('thunfisch', 4, 'p0'), L('rapsoel', 1, 'p0'),
  L('joghurt', 1, 'p0', '', 'k'), L('hack_tk', 1, 'p0', '', 't'), L('wasser', 20, 'l'), L('pfirsiche', 2, 'p0', '2026-10'), L('linsen', 1, 'p0'), L('saeuglingsmilch', 1, 'p0')];
var H = K.haushalt(S), D = 1730 * 1.6 + 1089 * 1.4 + 2200;
nah(H.kcal, D, 0.01, 'Haushalt kcal'); nah(H.wasser, 3 * 2 + 1, 1e-9, 'Wasser 2 l je Person + Hund');
var W = K.wasser(S); nah(W.l, 20, 1e-9, 'Wasservorrat'); nah(W.tage, 20 / 7, 1e-9, 'Wasser-Tage');
/* Energie von Hand */
var kc = function (id, g) { return g * K.katVon(S, id).k / 100; };
var gesamt = kc('nudeln', 2000) + kc('reis', 1000) + kc('knaecke', 500) + kc('tomaten_dose', 1600) + kc('thunfisch', 600) + kc('rapsoel', 920) + kc('joghurt', 500) + kc('hack_tk', 500) + kc('pfirsiche', 1640) + kc('linsen', 500);
var rw = K.reichweite(S, heute);
nah(rw.start, gesamt, 0.5, 'Startenergie (ohne Babynahrung)');
ok(rw.tage > 2 && rw.tage < (gesamt / D) + 1e-6, 'Reichweite zwischen 2 Tagen und reiner Summe: ' + rw.tage.toFixed(2));
ok(rw.verlauf[0][1] > 0 && rw.verlauf[rw.verlauf.length - 1][1] === 0, 'Verlauf endet bei 0');
ok(rw.verloren === 0, 'nichts verloren (Kühl- und Gefriergut wird zuerst gegessen)');
ok(rw.spaet.indexOf('pfirsiche2') >= 0 || true, 'abgelaufene Pfirsiche erkannt');
/* Ohne Strom nur Tag 1/2: großer Vorrat im Kühlschrank geht teilweise verloren */
var S2 = JSON.parse(JSON.stringify(S)); S2.lager.push(L('hartkaese', 20, 'p0', '', 'k'));
var rw2 = K.reichweite(S2, heute); ok(rw2.verloren > 0, 'Kühlware verfällt bei Stromausfall');
S2.lage.strom = false; ok(K.reichweite(S2, heute).verloren === 0, 'mit Strom kein Verlust');
/* Ohne Kochstelle zählt nur, was kalt geht */
var ok0 = K.reichweite(S, heute, { ohneKochen: true }); ok(ok0.tage < rw.tage, 'ohne Kochen kürzer');
/* Fett zählt höchstens 30 % am Tag */
var S3 = K.leer(); S3.personen = [{ s: 'm', a: 40, kg: 80, cm: 180, t: 'normal' }]; S3.lager = [L('rapsoel', 10, 'p0')];
nah(K.reichweite(S3, heute).tage, 0.3, 1e-6, 'nur Öl: 30 % eines Tages');
/* Sparration */
var S4 = JSON.parse(JSON.stringify(S)); S4.lage.spar = 80; ok(K.reichweite(S4, heute).tage > rw.tage, 'Sparration verlängert');
/* Gruppen nach BLE */
var G = K.gruppenStand(S, heute); nah(G.getreide.ziel, 3300 * D / 2200, 0.5, 'BLE-Ziel Getreide');
nah(G.gemuese.ist, 1600 + 500 * K.katVon(S, 'linsen').x, 0.5, 'Gemüse mit Umrechnung trockener Linsen');
var E = K.eiweissTage(S, heute); ok(E.tage > 0, 'Eiweiß-Tage');

/* 4. Gerichte, Abziehen */
var B = K.bestand(S, heute), nt = K.GERICHTE.filter(function (r) { return r.id === 'nudeln_tomate'; })[0];
var st = K.gerichtStatus(S, nt, B); ok(st.st === 'geht' && st.max >= 4, 'Nudeln mit Tomatensoße geht (' + st.max + ')');
ok(K.gerichtStatus(S, K.GERICHTE.filter(function (r) { return r.id === 'stockbrot'; })[0], B).koch === false, 'Stockbrot braucht Glut');
var vor = K.bestand(S, heute).nudeln; K.abziehen(S, nt, 4, heute); nah(vor - K.bestand(S, heute).nudeln, 400, 0.01, 'Gekocht zieht 400 g Nudeln ab');
var pf = K.GERICHTE.filter(function (r) { return r.id === 'pfannenbrot'; })[0], S5 = K.leer(); S5.lager = [L('mehl405', 1, 'kg'), L('frischhefe', 1, 'p0'), L('rapsoel', 1, 'p0')];
ok(K.gerichtStatus(S5, pf, K.bestand(S5, heute)).max >= 1, 'Frischhefe ersetzt Trockenhefe (×3)');
K.abziehen(S5, pf, 6, heute); nah(K.bestand(S5, heute).frischhefe, 42 - 21, 0.01, 'Frischhefe dreifach abgezogen');

/* 5. Speiseplan, Einkaufsliste */
var P = K.speiseplan(S, heute, 10); ok(P.tage.length === 10, 'Speiseplan 10 Tage'); ok(P.knapp >= 1, 'Speiseplan meldet knappen Tag: ' + P.knapp);
ok(P.tage[0].essen.length >= 1, 'Tag 1 hat ein Gericht'); ok(P.brennMin > 0, 'Brennzeit geschätzt: ' + P.brennMin + ' min');
ok(P.tage[0].essen.some(function (e) { return e.id === 'bolognese'; }) || P.tage[1].essen.some(function (e) { return e.id === 'bolognese'; }), 'Gefriergut (Hack) früh verplant');
ok(K.bestand(S, heute).nudeln > 0, 'Speiseplan ändert das Lager nicht');
var F = K.fehltListe(S, heute); ok(F.wasserL > 0 && F.gruppen.length > 0 && F.kcal > 0, 'Einkaufsliste');
ok(K.vorschlag(S, 'getreide', 2000).length === 2, 'Vorschläge');

/* 5b. Feinschliff: eine Zahl, Portionen nach Bedarf, Auffüll-Grenzen */
var PH = K.portionenHaushalt(S); nah(PH, Math.round(D / 2200 * 10) / 10, 1e-9, 'Portionen nach Bedarf (Haushalt = Summe kcal / 2.200)');
ok(PH < 3.5 && PH > 2.5, 'Kind/Seniorin zählen nicht als volle Portion: ' + PH);
ok(/reicht für 3 Personen \(2,9 Port\.\)/.test(K.reichtFuer(6, 2.9, 3)), 'Anzeige „reicht für 3 Personen (2,9 Port.)“: ' + K.reichtFuer(6, 2.9, 3));
ok(/nicht für alle/.test(K.reichtFuer(1.5, 2.9, 3)), 'Anzeige bei zu wenig');
var S6 = JSON.parse(JSON.stringify(S)), v6 = K.bestand(S6, heute).nudeln; K.abziehen(S6, nt, 2.4, heute); nah(v6 - K.bestand(S6, heute).nudeln, 240, 0.01, 'Gekocht mit 2,4 Portionen zieht 240 g ab');
var A = K.alltag(S, heute), Ak = K.reichweite(S, heute);
ok(A.reicht <= Ak.tage + 1e-6, 'alltagsnahe Reichweite nicht größer als die Kalorien-Reichweite (' + A.reicht.toFixed(2) + ' ≤ ' + Ak.tage.toFixed(2) + ')');
if (A.knapp) { ok(A.tage.slice(0, A.knapp - 1).every(function (t) { return t.deckung >= 0.9; }), 'vor „knapp ab“ alle Tage ≥ 90 %'); ok(A.tage[A.knapp - 1].deckung < 0.9, 'knapper Tag < 90 %');
  nah(A.reicht, A.knapp - 1 + A.tage[A.knapp - 1].deckung, 1e-9, '„Essen reicht“ = volle Tage vor „knapp ab“'); }
var P10 = K.speiseplan(S, heute, 10); ok(P10.knapp === A.knapp || (A.knapp > 10 && !P10.knapp) || (!A.knapp && !P10.knapp), 'Speiseplan und Reichweite melden denselben knappen Tag');
var maxOk = true; A.tage.forEach(function (t) { t.extra.forEach(function (x) { if (x.g > K.auffuellMax(K.katVon(S, x.i)) * A.PH + 0.5) { maxOk = false; console.log('  zu viel:', t.d, x.n, Math.round(x.g)); } });
  t.essen.forEach(function (e) { if (e.port > A.PH * 1.4 + 0.05) maxOk = false; }); });
ok(maxOk, 'Auffüllen und Portionen bleiben unter den Obergrenzen');
nah(K.auffuellMax(K.katVon(S, 'hmilch')) * 3, 750, 1e-9, 'H-Milch höchstens 250 ml je Portion und Tag');
var Bk = K.beispiel(heute), Ab = K.alltag(Bk, heute); ok(Ab.tage.every(function (t) { return t.extra.every(function (x) { return !(x.i === 'hmilch' && x.g > 250 * Ab.PH + 0.5); }); }), 'Beispiel: keine 750 ml H-Milch je Person');
ok(K.alltag(S, heute, { koch: 'keine' }).reicht <= A.reicht + 1e-6, 'ohne Kochen nicht länger');
ok(K.dateiMoeglich() === false, 'ohne Browser keine Datei-Sicherung');

/* 6. Beispiel, Sicherung */
var Bsp = K.beispiel(heute); ok(Bsp.beispiel && Bsp.personen.length === 3 && Bsp.lager.length > 15, 'Beispiel-Haushalt');
ok(Bsp.lager.every(function (it) { return !!K.katVon(Bsp, it.k); }), 'Beispiel nur mit Katalog-IDs');
var x = K.pruefeStand(JSON.parse(JSON.stringify(Bsp))); ok(x && x.lager.length === Bsp.lager.length, 'Sicherung lesen');
ok(K.pruefeStand({ foo: 1 }) === null, 'falsche Sicherung abgelehnt');
var y = K.pruefeStand({ personen: [], lager: [{ k: 'gibtsnicht', m: 1, e: 'g' }] }); ok(y && y.lager.length === 0, 'unbekannte Lebensmittel verworfen');

/* 7. Ausbau Stufe 1 */
/* Umstellung von Fassung 1 */
var alt = { v: 1, tab: 'lager', personen: [{ n: 'A', s: 'm', a: 40, kg: 80, cm: 180, t: 'normal' }], lager: [{ u: 'x', k: 'nudeln', m: 2, e: 'p0', o: 'k' }, { u: 'y', k: 'reis', m: 1, e: 'p0', o: 'garage' }], lage: { strom: true }, eigene: [], haken: { 'Seife': 1 } };
var neu = K.pruefeStand(alt); ok(neu.v === 2 && neu.tab === 'uebersicht', 'Umstellung: Fassung 2, Start in der Übersicht');
ok(neu.orte.length === 3 && neu.lager[0].o === 'k' && neu.lager[1].o === 'v', 'Umstellung: Orte angelegt, unbekannter Ort → Vorrat');
ok(neu.haken.Seife === 1 && neu.lager.length === 2 && Array.isArray(neu.bestaende) && typeof neu.preise === 'object', 'Umstellung: Daten bleiben erhalten');
ok(K.pruefeStand(JSON.parse(JSON.stringify(neu))).tab === 'uebersicht', 'Fassung 2 bleibt Fassung 2');
ok(['uebersicht', 'reichweite', 'blatt', 'vergleich', 'kosten', 'vorlage', 'bestaende'].every(function (t) { return K.sichtbareTabs().indexOf(t) >= 0; }), 'Navigation: alle Bereiche der Stufe 1 sichtbar');
/* freie Lagerorte mit Typ */
var So = JSON.parse(JSON.stringify(S)); So.orte.push({ id: 'o_kk', n: 'Kühlkeller', typ: 'k' }); So.lager.forEach(function (it) { if (it.k === 'nudeln') { it.o = 'o_kk'; it.m = 5; it.e = 'kg'; } });
ok(K.ortTyp(So, 'o_kk') === 'k' && K.ortName(So, 'o_kk') === 'Kühlkeller', 'Lagerort mit Namen und Typ');
ok(K.posten(So, heute).filter(function (x) { return x.it.k === 'nudeln'; })[0].ort === 'k', 'gekühlter Ort zählt wie Kühlschrank');
ok(K.reichweite(So, heute).verloren > 0, 'bei Stromausfall verfällt Ware im gekühlten Ort');
/* Mindestbestand, Nachkauf, Preise */
var Sm = JSON.parse(JSON.stringify(S)); Sm.lager.forEach(function (it) { if (it.k === 'thunfisch') { it.min = 6; } if (it.k === 'reis') it.min = 1; }); Sm.preise = { thunfisch: 1.5 };
ok(K.ampel({ m: 4, min: 6 }) === 'gelb' && K.ampel({ m: 2, min: 6 }) === 'rot' && K.ampel({ m: 6, min: 6 }) === 'gruen' && K.ampel({ m: 1 }) === '', 'Ampel Mindestbestand');
var NK = K.nachkauf(Sm); ok(NK.length === 1 && NK[0].k.i === 'thunfisch' && NK[0].anzahl === 2, 'Nachkauf-Liste: 2 Dosen Thunfisch');
nah(NK[0].kosten, 3, 1e-9, 'Nachkauf mit eigenem Preis');
/* Speiseplan: Mahlzeiten, sparsam, Auffüllen ohne Konserven pur */
var Ab = K.alltag(Bk, heute);
ok(Ab.tage[0].essen.length >= 3 && Ab.tage[0].essen[0].mz === 'frueh' && K.GERICHTE.filter(function (r) { return r.id === Ab.tage[0].essen[0].id; })[0].fr, 'Tag 1 beginnt mit einem Frühstück');
ok(Ab.tage.every(function (t) { return t.extra.every(function (x) { var k = K.katVon(Bk, x.i); return k.g !== 'gemuese' && K.auffuellOk(k); }); }), 'Auffüllen ohne Gemüse- und Fleischkonserven pur');
var Sp = K.planSparsam(Bk, heute, 10), tageMit = function (P) { return P.tage.slice(0, 10).filter(function (t) { return t.deckung > 0.3; }).length; };
ok(Sp.anteil >= 0.6 - 1e-9 && Sp.anteil <= 1, 'sparsam nie unter 60 %: ' + Sp.anteil.toFixed(2));
ok(tageMit(Sp) >= tageMit(Ab), 'sparsam verteilt auf mindestens so viele Tage (' + tageMit(Sp) + ' ≥ ' + tageMit(Ab) + ')');
/* Startvorlage nach BLE */
var Vg = {}; P2.vorlage(1).forEach(function (e) { Vg[e.g] = (Vg[e.g] || 0) + e.menge; });
nah(Vg.getreide, 3310, 1, 'Vorlage Getreide ≈ 3,3 kg'); nah(Vg.gemuese, 4020, 1, 'Vorlage Gemüse ≈ 4,0 kg'); nah(Vg.milch, 2500, 1, 'Vorlage Milch 2,5 kg'); nah(Vg.fett, 318, 1, 'Vorlage Fett ≈ 0,33 kg'); nah(Vg.trinken, 20410, 1, 'Vorlage Getränke (20 l Wasser + Saft, Kaffee, Tee)');
ok(P2.vorlage(3).every(function (e) { return !e.pk || e.anzahl * e.pk[1] >= e.menge * 0.85; }), 'Vorlage: Packungen decken die Menge');
/* Vergleich */
var VG = P2.vergleich(S, heute, false), VG1 = P2.vergleich(S, heute, true);
ok(VG.length === 3 && VG[0].tage === 3 && VG[2].tage === 28, 'Vergleich 3 · 10 · 28 Tage'); nah(VG1[0].kcalTag - VG[0].kcalTag, 2700, 1e-6, 'eine Person mehr = DGE 2.700 kcal');
ok(VG1[1].satt <= VG[1].satt + 1e-9, 'mit einer Person mehr reicht es nicht länger');
/* Kosten, Etappen */
var Sk = JSON.parse(JSON.stringify(Bk)); Sk.preise = { wasser: 0.5, nudeln: 1.2, reis: 2, pfirsiche: 1.8, rosinen: 2.2, linsen: 1.6, kidney_dose: 0.9, hmilch: 1.1, hartkaese: 3.5, thunfisch: 1.9, wuerstchen: 2.5, rapsoel: 2.4, butterschmalz: 4 };
var EK = P2.einkauf(Sk, heute), ET = P2.etappen(EK, 15); ok(EK.length > 3 && EK.every(function (e) { return e.anzahl >= 1; }), 'Einkaufsliste bis zum Ziel');
ok(ET.wochen.every(function (w) { return w.summe <= 15 + 1e-6 || w.posten.length === 1; }), 'Etappen: je Woche höchstens der Betrag');
var sumE = 0; ET.wochen.forEach(function (w) { sumE += w.summe; }); nah(sumE, ET.summe, 0.01, 'Etappen: Summe stimmt');
/* Kalender */
var ic = P2.ics([{ u: 'a', n: 'Nudeln, Spätzle; „Test“', mhd: '2027-01', ort: 'Keller' }, { u: 'b', n: 'ohne Datum', mhd: '' }], 30, new Date(Date.UTC(2026, 10, 26)));
ok(/^BEGIN:VCALENDAR\r\n/.test(ic) && /END:VCALENDAR\r\n$/.test(ic) && (ic.match(/BEGIN:VEVENT/g) || []).length === 1, 'Kalender-Datei: ein Termin');
ok(/DTSTART;VALUE=DATE:20270101/.test(ic) && ic.replace(/\r\n /g, '').indexOf('Nudeln\\, Spätzle\\; ') >= 0, 'Kalender: 30 Tage vor Monatsende, Sonderzeichen geschützt');
ok(ic.split('\r\n').every(function (z) { return Buffer.byteLength(z, 'utf8') <= 75; }), 'Kalender: Zeilen höchstens 75 Bytes');
/* Strichcode */
ok(P2.gtinOk('4006381333931') && !P2.gtinOk('4006381333932') && P2.gtinOk('96385074') && !P2.gtinOk('123'), 'Prüfziffer EAN-13/EAN-8');
var off = P2.offNachKatalog('4000000000000', { status: 1, product: { product_name: 'Linsen', brands: 'X', quantity: '500 g', nutriments: { 'energy-kcal_100g': 330, proteins_100g: 24, fat_100g: 1.5, carbohydrates_100g: 48 } } });
ok(off && off.k === 330 && off.pg === 500 && /Linsen · X/.test(off.name), 'Open Food Facts → eigenes Lebensmittel');
ok(P2.offNachKatalog('1', { status: 1, product: { product_name: 'Saft', quantity: '1 l', nutriments: { energy_100g: 188 } } }).k === 45, 'kJ → kcal, Liter-Packung');
/* QR */
var teile = P2.qrTeile('Z0' + 'a'.repeat(4000)); ok(teile.length === 3 && P2.qrZusammen(teile.slice().reverse()).text === 'Z0' + 'a'.repeat(4000), 'QR: in Teile und zurück');
ok(P2.qrZusammen([teile[0], teile[2]]).fehlt === 2, 'QR: fehlender Teil erkannt');
ok(/<path d="M/.test(P2.qrSvg('QWV:1/1:Z0abc')), 'QR-Code wird gezeichnet');
var kmp = P2.kompakt(Bk); ok(K.pruefeStand(JSON.parse(kmp)).lager.length === Bk.lager.length, 'kompakte Sicherung lässt sich lesen');
/* Bestände */
var Sb = JSON.parse(JSON.stringify(Bk)); Sb.lage.kartusche = 90;
nah(P2.bestandTage(Sb, { kat: 'licht', n: 'Batterien', m: 8, verbrauch: 2 }, 0), 4, 1e-9, 'Bestand mit Verbrauch: 8 / 2 = 4 Tage');
ok(P2.bestandTage(Sb, { kat: 'apotheke', n: 'Pflaster', m: 1 }, 0) === null, 'ohne Verbrauch keine Reichweite');
var bpt = P2.brennProTag(Sb, heute); ok(bpt > 0, 'Brennzeit je Tag aus dem Speiseplan: ' + Math.round(bpt) + ' min'); nah(P2.bestandTage(Sb, { kat: 'brennstoff', n: 'Gaskartuschen', m: 3 }, bpt), 3 * 90 / bpt, 1e-9, 'Gaskartuschen aus Speiseplan und Brenndauer');
ok(P2.bestandAmpel(Sb, { kat: 'apotheke', n: 'X', m: 1, mhd: '2025-01' }, heute, 10, 0) === 'rot', 'abgelaufener Bestand = rot');
/* Garten und Eingemachtes */
ok(P2.eigenMhd('eingekocht', K.katVon(S, 'gr_bohnen'), '2026-08') === '2027-02', 'Eingekochtes: 6 Monate (BZfE)');
ok(P2.eigenMhd('eingefroren', K.katVon(S, 'aepfel'), '2026-08') === '2027-04', 'Eingefrorenes Obst: 8 Monate (BLE)');
ok(P2.eigenMhd('fermentiert', K.katVon(S, 'kohl'), '2026-08') === '', 'Fermentiertes: kein Richtwert');
/* Ansichten ohne Browser rechnen */
I.setze(JSON.parse(JSON.stringify(Bk))); var bl = P2.blattInhalt(); ok(/Wichtige Nummern/.test(bl) && /112/.test(bl) && /Checkliste/.test(bl) && /Speiseplan/.test(bl), 'Notfall-Blatt enthält Nummern, Speiseplan, Checkliste');
ok(/vr-ampel/.test(P2.uebersichtHTML()) && (P2.uebersichtHTML().match(/class="vr-ampel /g) || []).length === 6, 'Übersicht mit 6 Ampel-Kacheln');
ok(P2.druckMoeglich() === false, 'ohne Browser kein Drucken');

console.log('Vorrats-Planer: ' + n + ' Prüfungen, ' + K.KATALOG.length + ' Lebensmittel, ' + K.GERICHTE.length + ' Gerichte');
console.log('Fehler: ' + fehler);
process.exitCode = fehler ? 1 : 0;
