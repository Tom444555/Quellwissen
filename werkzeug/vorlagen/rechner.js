
/* Quellwissen – „Rechner & Umrechner“ (eigenständiges Modul, ES2019, offline, ohne Bibliotheken) · Quelle: werkzeug/vorlagen/rechner.js
   Schnittstelle: window.QWRechner.seite(el)  ·  reine Rechenlogik zusätzlich unter QWRechner._kern */
(function (root) {
'use strict';

/* ===================================================================== 1. Zahlen */
var NFC = {};
function nf(max, min) { var k = max + '|' + (min || 0); return NFC[k] || (NFC[k] = new Intl.NumberFormat('de-DE', { maximumFractionDigits: max, minimumFractionDigits: min || 0 })); }
var HOCHZ = { '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹', '-': '⁻' };
function hoch(n) { return String(n).split('').map(function (c) { return HOCHZ[c] || c; }).join(''); }
function rund(x, s) { if (!isFinite(x) || x === 0) return x; return parseFloat(x.toPrecision(s || 12)); }
function minus(s) { return String(s).replace(/-/g, '−'); }
/* Zahl mit sig signifikanten Stellen, deutsche Schreibweise, ohne Gleitkomma-Artefakte */
function zahl(x, sig) {
  if (x == null || typeof x !== 'number' || isNaN(x)) return '–';
  if (!isFinite(x)) return x > 0 ? '∞' : '−∞';
  sig = sig || 10;
  var r = rund(rund(x, 14), sig); if (r === 0) return '0';
  var a = Math.abs(r);
  if (a >= 1e15 || a < 1e-5) {
    var e = Math.floor(Math.log10(a)), m = rund(r / Math.pow(10, e), Math.min(sig, 10));
    if (Math.abs(m) >= 10) { m = rund(m / 10, 10); e++; }
    return minus(nf(Math.max(0, Math.min(sig - 1, 9))).format(m)) + ' × 10' + hoch(e);
  }
  var dec = Math.max(0, sig - 1 - Math.floor(Math.log10(a)));
  return minus(nf(Math.min(dec, 20)).format(r));
}
function kfm(x, d) { var p = Math.pow(10, d), y = rund(Math.abs(x) * p, 12); return (x < 0 ? -1 : 1) * Math.round(y) / p; } /* kaufmännisch runden */
function fix(x, d) { if (!isFinite(x)) return zahl(x); return minus(nf(d, d).format(kfm(x, d))); }
function dz(x, d) { if (!isFinite(x)) return zahl(x); return minus(nf(d).format(kfm(x, d))); }
function geld(x) { return fix(x, 2) + ' €'; }
function gz(x) { return minus(nf(0).format(Math.round(x))); }
/* deutsche Zahl lesen: „1.234,5“, „2,5“, „1.5“, „1e5“, „−3“ */
function zahlLesen(s) {
  if (typeof s === 'number') return s;
  if (s == null) return NaN;
  s = String(s).trim().replace(/[\s  '’]/g, '').replace(/[−–]/g, '-').replace(/^\+/, '');
  if (!s) return NaN;
  s = s.replace(/[×x]10\^?([-+]?\d+)$/i, 'e$1');
  if (/^-?\d{1,3}(\.\d{3})+(,\d+)?(e[-+]?\d+)?$/i.test(s)) s = s.replace(/\./g, '').replace(',', '.');
  else if (/^-?\d{1,3}(,\d{3})+\.\d+$/.test(s)) s = s.replace(/,/g, '');
  else if (s.indexOf(',') >= 0) s = s.replace(/\./g, '').replace(',', '.');
  if (!/^-?(\d+\.?\d*|\.\d+)(e[-+]?\d+)?$/i.test(s)) return NaN;
  return parseFloat(s);
}
function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }

/* ===================================================================== 2. Ausdrucks-Parser (ohne eval) */
var KONST = { pi: Math.PI, e: Math.E, phi: (1 + Math.sqrt(5)) / 2, tau: 2 * Math.PI };
var FNAME = { sqrt: 'sqrt', wurzel: 'sqrt', cbrt: 'cbrt', kubikwurzel: 'cbrt', ln: 'ln', log: 'log', lg: 'log', log10: 'log', ld: 'log2', log2: 'log2', exp: 'exp', abs: 'abs', betrag: 'abs',
  round: 'round', runden: 'round', floor: 'floor', abrunden: 'floor', ceil: 'ceil', aufrunden: 'ceil', min: 'min', max: 'max', fak: 'fak', 'fakultät': 'fak',
  sin: 'sin', cos: 'cos', tan: 'tan', asin: 'asin', acos: 'acos', atan: 'atan', arcsin: 'asin', arccos: 'acos', arctan: 'atan', sinh: 'sinh', cosh: 'cosh', tanh: 'tanh', root: 'root' };
function fakultaet(n) {
  if (n < 0 || Math.floor(n) !== n) throw new Error('Die Fakultät ist nur für natürliche Zahlen definiert.');
  if (n > 170) throw new Error('Die Fakultät von ' + n + ' ist zu groß.');
  var r = 1; for (var i = 2; i <= n; i++) r *= i; return r;
}
function lexer(s) {
  s = String(s).toLowerCase().replace(/[−–—]/g, '-').replace(/[×·∙⋅]/g, '*').replace(/÷/g, '/').replace(/\*\*/g, '^').replace(/π/g, ' pi ').replace(/[\[{]/g, '(').replace(/[\]}]/g, ')');
  var t = [], i = 0, m;
  while (i < s.length) {
    var r = s.slice(i), c = s[i];
    if (/\s/.test(c)) { i++; continue; }
    if ((m = /^\d{1,3}(?:\.\d{3})+(?![\d.])(?:,\d+)?/.exec(r)) || (m = /^(?:\d+(?:[.,]\d+)?|[.,]\d+)(?:e[-+]?\d+)?/.exec(r))) {
      t.push({ t: 'num', v: zahlLesen(m[0]) }); i += m[0].length; continue;
    }
    if ((m = /^[a-zäöüß][a-zäöüß0-9]*/.exec(r))) { t.push({ t: 'id', v: m[0] }); i += m[0].length; continue; }
    if ('+-*/:^%!()²³°√∛;'.indexOf(c) >= 0) { t.push({ t: 'op', v: c }); i++; continue; }
    throw new Error('Unbekanntes Zeichen „' + c + '“.');
  }
  return t;
}
function trig(n, x, grad) {
  var r;
  if (n === 'sin' || n === 'cos' || n === 'tan') {
    if (grad) {
      var m = ((x % 360) + 360) % 360;
      if (n === 'tan' && m % 180 === 90) throw new Error('tan(' + zahl(x) + '°) ist nicht definiert.');
      x = x * Math.PI / 180;
    }
    r = Math[n](x); if (Math.abs(r) < 1e-14) r = 0; return r;
  }
  r = Math[n](x); if (isNaN(r)) throw new Error(n + '(' + zahl(x) + ') ist nicht definiert.');
  return grad ? r * 180 / Math.PI : r;
}
function rufe(n, a, grad) {
  var x = a[0];
  if (a.length === 0) throw new Error('Funktion ' + n + ' braucht einen Wert.');
  switch (n) {
    case 'sqrt': if (x < 0) throw new Error('Die Wurzel aus einer negativen Zahl ist reell nicht definiert.'); return Math.sqrt(x);
    case 'cbrt': return Math.cbrt(x);
    case 'root': if (a.length < 2) throw new Error('root(x; n) braucht zwei Werte.'); if (x < 0 && a[1] % 2 === 1) return -Math.pow(-x, 1 / a[1]); return Math.pow(x, 1 / a[1]);
    case 'ln': if (x <= 0) throw new Error('ln ist nur für positive Zahlen definiert.'); return Math.log(x);
    case 'log': if (x <= 0) throw new Error('log ist nur für positive Zahlen definiert.'); return a.length > 1 ? Math.log(x) / Math.log(a[1]) : Math.log10(x);
    case 'log2': if (x <= 0) throw new Error('ld ist nur für positive Zahlen definiert.'); return Math.log2(x);
    case 'exp': return Math.exp(x);
    case 'abs': return Math.abs(x);
    case 'round': var p = Math.pow(10, a[1] || 0); return Math.round(x * p) / p;
    case 'floor': return Math.floor(x);
    case 'ceil': return Math.ceil(x);
    case 'min': return Math.min.apply(null, a);
    case 'max': return Math.max.apply(null, a);
    case 'fak': return fakultaet(x);
    case 'sinh': case 'cosh': case 'tanh': return Math[n](x);
    default: return trig(n, x, grad);
  }
}
function ausdruck(text, opt) {
  opt = opt || {};
  var t = lexer(text), i = 0, grad = opt.grad !== false, schritte = [];
  if (!t.length) throw new Error('Bitte einen Rechenausdruck eingeben.');
  function ist(typ, w) { var x = t[i]; return !!x && x.t === typ && (w === undefined || x.v === w); }
  function next() { return t[i++]; }
  function sch(s) { if (schritte.length < 16) schritte.push(s); }
  function op(a, o, b, r) { sch(zahl(a) + ' ' + o + ' ' + (b < 0 ? '(' + zahl(b) + ')' : zahl(b)) + ' = ' + zahl(r)); return r; }
  function beginntWert() { var x = t[i]; return !!x && (x.t === 'num' || (x.t === 'id' && x.v !== 'von' && x.v !== 'of') || (x.t === 'op' && (x.v === '(' || x.v === '√' || x.v === '∛'))); }
  function expr() {
    var l = term();
    while (ist('op', '+') || ist('op', '-')) {
      var o = next().v, r = term(), v;
      if (r.p) { var f = o === '+' ? 1 + r.v : 1 - r.v; v = l.v * f; sch(zahl(l.v) + (o === '+' ? ' + ' : ' − ') + zahl(r.v * 100) + ' % = ' + zahl(l.v) + ' · ' + zahl(f) + ' = ' + zahl(v)); }
      else v = op(l.v, o === '+' ? '+' : '−', r.v, o === '+' ? l.v + r.v : l.v - r.v);
      l = { v: v };
    }
    return l;
  }
  function term() {
    var l = unary();
    for (;;) {
      var x = t[i], r;
      if (x && x.t === 'op' && (x.v === '*' || x.v === '/' || x.v === ':')) {
        next(); r = unary();
        if (x.v === '*') l = { v: op(l.v, '·', r.v, l.v * r.v) };
        else { if (r.v === 0) throw new Error('Division durch 0 ist nicht definiert.'); l = { v: op(l.v, ':', r.v, l.v / r.v) }; }
      } else if (x && x.t === 'id' && (x.v === 'von' || x.v === 'of')) { next(); r = unary(); l = { v: op(l.v, '·', r.v, l.v * r.v) }; }
      else if (beginntWert()) { r = unary(); l = { v: op(l.v, '·', r.v, l.v * r.v) }; }
      else break;
    }
    return l;
  }
  function unary() {
    if (ist('op', '-')) { next(); var u = unary(); return { v: -u.v, p: u.p }; }
    if (ist('op', '+')) { next(); return unary(); }
    return potenz();
  }
  function potenz() {
    var b = postfix();
    if (ist('op', '^')) {
      next(); var e = unary(), r = Math.pow(b.v, e.v);
      if (isNaN(r)) throw new Error('Diese Potenz ist reell nicht definiert.');
      return { v: op(b.v, '^', e.v, r) };
    }
    return b;
  }
  function postfix() {
    var a = primaer();
    for (;;) {
      if (ist('op', '!')) { next(); var f = fakultaet(a.v); sch(zahl(a.v) + '! = ' + zahl(f)); a = { v: f }; }
      else if (ist('op', '%')) { next(); a = { v: a.v / 100, p: true }; }
      else if (ist('op', '²')) { next(); a = { v: op(a.v, '^', 2, a.v * a.v) }; }
      else if (ist('op', '³')) { next(); a = { v: op(a.v, '^', 3, a.v * a.v * a.v) }; }
      else if (ist('op', '°')) { next(); if (!grad) a = { v: a.v * Math.PI / 180 }; }
      else break;
    }
    return a;
  }
  function primaer() {
    var x = next(), r;
    if (!x) throw new Error('Der Ausdruck endet unerwartet.');
    if (x.t === 'num') return { v: x.v };
    if (x.t === 'op' && x.v === '(') {
      var e = expr();
      if (!ist('op', ')')) throw new Error('Eine schließende Klammer fehlt.');
      next(); return { v: e.v, p: e.p };
    }
    if (x.t === 'op' && (x.v === '√' || x.v === '∛')) {
      var a = postfix(); r = rufe(x.v === '√' ? 'sqrt' : 'cbrt', [a.v], grad); sch(x.v + zahl(a.v) + ' = ' + zahl(r)); return { v: r };
    }
    if (x.t === 'id') {
      var n = x.v;
      if (KONST[n] !== undefined && !ist('op', '(')) return { v: KONST[n] };
      var fn = FNAME[n];
      if (!fn) throw new Error('Das Wort „' + n + '“ kenne ich in Rechenausdrücken nicht.');
      var args = [];
      if (ist('op', '(')) {
        next();
        if (!ist('op', ')')) { args.push(expr().v); while (ist('op', ';')) { next(); args.push(expr().v); } }
        if (!ist('op', ')')) throw new Error('Eine schließende Klammer fehlt.');
        next();
      } else args.push(postfix().v);
      r = rufe(fn, args, grad);
      sch(n + '(' + args.map(function (z) { return zahl(z); }).join('; ') + (/^(sin|cos|tan)$/.test(fn) && grad ? '°' : '') + ') = ' + zahl(r));
      return { v: r };
    }
    throw new Error('Unerwartetes Zeichen „' + x.v + '“.');
  }
  var erg = expr();
  if (i < t.length) throw new Error('Unerwartetes Zeichen „' + t[i].v + '“.');
  if (!isFinite(erg.v)) throw new Error('Das Ergebnis ist zu groß oder nicht definiert.');
  return { wert: erg.v, prozent: !!erg.p, schritte: schritte };
}

/* ===================================================================== 3. Einheiten (SI/NIST-Definitionen) */
var KAT = {
  laenge: { n: 'Länge', b: 'm', e: [
    ['nm', 'Nanometer', 1e-9, 'nanometer'], ['µm', 'Mikrometer', 1e-6, 'um|mikrometer|mikron'], ['mm', 'Millimeter', 1e-3, 'millimeter'], ['cm', 'Zentimeter', 1e-2, 'zentimeter'],
    ['dm', 'Dezimeter', 0.1, 'dezimeter'], ['m', 'Meter', 1, 'meter'], ['km', 'Kilometer', 1000, 'kilometer'],
    ['in', 'Zoll (inch)', 0.0254, 'zoll|inch|inches|″'], ['ft', 'Fuß (foot)', 0.3048, 'fuß|fuss|feet|foot'], ['yd', 'Yard', 0.9144, 'yard|yards'],
    ['mi', 'Meile (mile)', 1609.344, 'meile|meilen|mile|miles|landmeile'], ['sm', 'Seemeile', 1852, 'seemeile|seemeilen|nmi'],
    ['AE', 'Astronomische Einheit', 149597870700, 'au|astronomische einheit'], ['Lj', 'Lichtjahr', 9460730472580800, 'ly|lichtjahr|lichtjahre'], ['pc', 'Parsec', 3.0856775814913673e16, 'parsec']] },
  flaeche: { n: 'Fläche', b: 'm²', e: [
    ['mm²', 'Quadratmillimeter', 1e-6, 'mm2|quadratmillimeter'], ['cm²', 'Quadratzentimeter', 1e-4, 'cm2|quadratzentimeter'], ['dm²', 'Quadratdezimeter', 0.01, 'dm2'],
    ['m²', 'Quadratmeter', 1, 'm2|qm|quadratmeter'], ['a', 'Ar', 100, 'ar|are'], ['ha', 'Hektar', 1e4, 'hektar'], ['km²', 'Quadratkilometer', 1e6, 'km2|quadratkilometer'],
    ['Morgen', 'Morgen (2500 m², regional verschieden)', 2500, 'morgen'], ['in²', 'Quadratzoll', 0.00064516, 'sq in|quadratzoll'], ['ft²', 'Quadratfuß', 0.09290304, 'sq ft|quadratfuß|quadratfuss'],
    ['yd²', 'Quadratyard', 0.83612736, 'sq yd|quadratyard'], ['acre', 'Acre', 4046.8564224, 'acres|ac'], ['mi²', 'Quadratmeile', 2589988.110336, 'sq mi|quadratmeile|quadratmeilen'],
    ['Fußballfeld', 'Fußballfeld (105 × 68 m)', 7140, 'fußballfeld|fußballfelder|fussballfeld']] },
  volumen: { n: 'Volumen', b: 'l', e: [
    ['mm³', 'Kubikmillimeter', 1e-6, 'mm3'], ['ml', 'Milliliter', 1e-3, 'milliliter'], ['cm³', 'Kubikzentimeter', 1e-3, 'cm3|ccm|kubikzentimeter'], ['cl', 'Zentiliter', 0.01, 'zentiliter'],
    ['dl', 'Deziliter', 0.1, 'deziliter'], ['l', 'Liter', 1, 'liter|ltr'], ['hl', 'Hektoliter', 100, 'hektoliter'], ['m³', 'Kubikmeter', 1000, 'm3|cbm|kubikmeter'],
    ['TL', 'Teelöffel (5 ml)', 0.005, 'teelöffel|teeloeffel|tsp'], ['EL', 'Esslöffel (15 ml)', 0.015, 'esslöffel|essloeffel|tbsp'], ['Tasse', 'Tasse (250 ml, Richtmaß)', 0.25, 'tasse|tassen'],
    ['cup', 'US-Cup', 0.2365882365, 'cups|us-cup|us cup'], ['fl oz', 'US-Flüssigunze', 0.0295735295625, 'floz|fl. oz|fluid ounce'], ['pt (US)', 'US-Pint', 0.473176473, 'pint|pints|us-pint'],
    ['pt (UK)', 'Brit. Pint', 0.56826125, 'uk-pint|imperial pint'], ['qt', 'US-Quart', 0.946352946, 'quart|quarts'], ['gal', 'US-Gallone', 3.785411784, 'gallone|gallonen|gallon|gallons|us-gallone'],
    ['gal (UK)', 'Brit. Gallone', 4.54609, 'uk-gallone|imperial gallon|britische gallone'], ['bbl', 'Barrel (Öl)', 158.987294928, 'barrel|barrels|fass'],
    ['in³', 'Kubikzoll', 0.016387064, 'in3|kubikzoll'], ['ft³', 'Kubikfuß', 28.316846592, 'ft3|kubikfuß|kubikfuss']] },
  masse: { n: 'Masse / Gewicht', b: 'kg', e: [
    ['µg', 'Mikrogramm', 1e-9, 'ug|mikrogramm'], ['mg', 'Milligramm', 1e-6, 'milligramm'], ['ct', 'Karat', 0.0002, 'karat'], ['g', 'Gramm', 1e-3, 'gramm|gr'],
    ['dag', 'Dekagramm', 0.01, 'dekagramm'], ['kg', 'Kilogramm', 1, 'kilo|kilogramm|kilos'], ['t', 'Tonne', 1000, 'tonne|tonnen'],
    ['Pfd', 'Pfund (dt., 500 g)', 0.5, 'pfd|dt. pfund|deutsches pfund'], ['Ztr', 'Zentner (50 kg)', 50, 'zentner'], ['dz', 'Doppelzentner', 100, 'doppelzentner'],
    ['gr', 'Grain', 6.479891e-5, 'grain'], ['oz', 'Unze', 0.028349523125, 'unze|unzen|ounce|ounces'], ['ozt', 'Feinunze (Troy)', 0.0311034768, 'feinunze|troy-unze|troyunze|troy ounce'],
    ['lb', 'Pfund (lb)', 0.45359237, 'lbs|pfund|pound|pounds'], ['st', 'Stone', 6.35029318, 'stone'], ['sh tn', 'Short ton (US)', 907.18474, 'short ton'], ['lg tn', 'Long ton (UK)', 1016.0469088, 'long ton']] },
  temperatur: { n: 'Temperatur', b: 'K', spezial: true, e: [
    ['°C', 'Grad Celsius', 0, '°c|c|celsius|grad celsius|grad'], ['°F', 'Grad Fahrenheit', 0, '°f|f|fahrenheit|grad fahrenheit'], ['K', 'Kelvin', 0, 'k|kelvin'],
    ['°Ra', 'Grad Rankine', 0, 'rankine|°ra'], ['°Ré', 'Grad Réaumur', 0, 'réaumur|reaumur|°ré|°re']],
    zu: function (u, w) { return { '°C': w + 273.15, '°F': (w + 459.67) * 5 / 9, 'K': w, '°Ra': w * 5 / 9, '°Ré': w * 1.25 + 273.15 }[u]; },
    von: function (u, k) { return { '°C': k - 273.15, '°F': k * 9 / 5 - 459.67, 'K': k, '°Ra': k * 9 / 5, '°Ré': (k - 273.15) * 0.8 }[u]; } },
  geschw: { n: 'Geschwindigkeit', b: 'm/s', e: [
    ['m/s', 'Meter pro Sekunde', 1, 'meter pro sekunde'], ['km/h', 'Kilometer pro Stunde', 1 / 3.6, 'kmh|kilometer pro stunde|stundenkilometer'], ['mph', 'Meilen pro Stunde', 0.44704, 'meilen pro stunde'],
    ['kn', 'Knoten', 1852 / 3600, 'knoten|kt'], ['ft/s', 'Fuß pro Sekunde', 0.3048, 'fps'], ['Mach', 'Mach (343 m/s, Luft 20 °C)', 343, 'mach'], ['c', 'Lichtgeschwindigkeit', 299792458, 'lichtgeschwindigkeit']] },
  zeit: { n: 'Zeit', b: 's', e: [
    ['ns', 'Nanosekunde', 1e-9, 'nanosekunde|nanosekunden'], ['µs', 'Mikrosekunde', 1e-6, 'us|mikrosekunde|mikrosekunden'], ['ms', 'Millisekunde', 1e-3, 'millisekunde|millisekunden'],
    ['s', 'Sekunde', 1, 'sek|sekunde|sekunden'], ['min', 'Minute', 60, 'minute|minuten'], ['h', 'Stunde', 3600, 'std|stunde|stunden'], ['d', 'Tag', 86400, 'tag|tage|tagen'],
    ['Wo', 'Woche', 604800, 'woche|wochen'], ['Mon', 'Monat (Ø 30,44 d)', 2629746, 'monat|monate|monaten'], ['J', 'Jahr (Ø 365,2425 d)', 31556952, 'jahr|jahre|jahren'],
    ['Jz', 'Jahrzehnt', 315569520, 'jahrzehnt|jahrzehnte'], ['Jh', 'Jahrhundert', 3155695200, 'jahrhundert|jahrhunderte'], ['Jt', 'Jahrtausend', 31556952000, 'jahrtausend|jahrtausende']] },
  druck: { n: 'Druck', b: 'Pa', e: [
    ['Pa', 'Pascal', 1, 'pascal'], ['hPa', 'Hektopascal', 100, 'hektopascal'], ['kPa', 'Kilopascal', 1000, 'kilopascal'], ['MPa', 'Megapascal', 1e6, 'megapascal'],
    ['mbar', 'Millibar', 100, 'millibar'], ['bar', 'Bar', 1e5, 'bar'], ['atm', 'Physikal. Atmosphäre', 101325, 'atmosphäre'], ['at', 'Techn. Atmosphäre', 98066.5, 'techn. atmosphäre'],
    ['Torr', 'Torr', 101325 / 760, 'torr'], ['mmHg', 'mm Quecksilbersäule', 133.322387415, 'mm hg'], ['mWS', 'Meter Wassersäule', 9806.65, 'meter wassersäule'], ['psi', 'psi (lbf/in²)', 6894.757293168361, 'psi']] },
  energie: { n: 'Energie', b: 'J', e: [
    ['eV', 'Elektronenvolt', 1.602176634e-19, 'elektronenvolt'], ['erg', 'Erg', 1e-7, 'erg'], ['J', 'Joule', 1, 'joule'], ['kJ', 'Kilojoule', 1000, 'kilojoule'], ['MJ', 'Megajoule', 1e6, 'megajoule'],
    ['GJ', 'Gigajoule', 1e9, 'gigajoule'], ['Wh', 'Wattstunde', 3600, 'wattstunde|wattstunden'], ['kWh', 'Kilowattstunde', 3.6e6, 'kilowattstunde|kilowattstunden'], ['MWh', 'Megawattstunde', 3.6e9, 'megawattstunde'],
    ['cal', 'Kalorie', 4.184, 'kalorie|kalorien'], ['kcal', 'Kilokalorie', 4184, 'kilokalorie|kilokalorien'], ['BTU', 'British Thermal Unit', 1055.05585262, 'btu'], ['ft·lbf', 'Foot-pound', 1.3558179483314004, 'ft lbf|ftlbf']] },
  leistung: { n: 'Leistung', b: 'W', e: [
    ['mW', 'Milliwatt', 1e-3, 'milliwatt'], ['W', 'Watt', 1, 'watt'], ['kW', 'Kilowatt', 1000, 'kilowatt'], ['MW', 'Megawatt', 1e6, 'megawatt'],
    ['PS', 'Pferdestärke (metrisch)', 735.49875, 'pferdestärke|pferdestärken'], ['hp', 'Horsepower (mech.)', 745.69987158227022, 'horsepower'], ['BTU/h', 'BTU pro Stunde', 0.29307107017222, 'btu/h'], ['kcal/h', 'Kilokalorie pro Stunde', 4184 / 3600, 'kcal/h']] },
  kraft: { n: 'Kraft', b: 'N', e: [
    ['dyn', 'Dyn', 1e-5, 'dyn'], ['mN', 'Millinewton', 1e-3, 'millinewton'], ['N', 'Newton', 1, 'newton'], ['kN', 'Kilonewton', 1000, 'kilonewton'], ['MN', 'Meganewton', 1e6, 'meganewton'],
    ['kp', 'Kilopond', 9.80665, 'kilopond'], ['lbf', 'Pound-force', 4.4482216152605, 'pound-force']] },
  daten: { n: 'Datenmenge', b: 'B', e: [
    ['bit', 'Bit', 0.125, 'bits'], ['B', 'Byte', 1, 'byte|bytes'], ['kbit', 'Kilobit', 125, 'kilobit'], ['kB', 'Kilobyte', 1e3, 'kb|kilobyte'], ['KiB', 'Kibibyte', 1024, 'kibibyte'],
    ['Mbit', 'Megabit', 125000, 'megabit'], ['MB', 'Megabyte', 1e6, 'mb|megabyte'], ['MiB', 'Mebibyte', 1048576, 'mebibyte'], ['Gbit', 'Gigabit', 1.25e8, 'gigabit'],
    ['GB', 'Gigabyte', 1e9, 'gb|gigabyte'], ['GiB', 'Gibibyte', 1073741824, 'gibibyte'], ['TB', 'Terabyte', 1e12, 'tb|terabyte'], ['TiB', 'Tebibyte', 1099511627776, 'tebibyte'], ['PB', 'Petabyte', 1e15, 'petabyte']] },
  winkel: { n: 'Winkel', b: '°', e: [
    ['°', 'Grad', 1, 'grad|deg|altgrad'], ['′', 'Bogenminute', 1 / 60, 'bogenminute|bogenminuten'], ['″', 'Bogensekunde', 1 / 3600, 'bogensekunde|bogensekunden'], ['rad', 'Radiant', 180 / Math.PI, 'radiant|bogenmaß'],
    ['mrad', 'Milliradiant', 0.18 / Math.PI, 'milliradiant'], ['gon', 'Gon (Neugrad)', 0.9, 'gon|neugrad'], ['U', 'Umdrehung (Vollwinkel)', 360, 'umdrehung|umdrehungen|vollwinkel']] },
  verbrauch: { n: 'Kraftstoffverbrauch', b: 'l/100 km', spezial: true, e: [
    ['l/100 km', 'Liter pro 100 km', 0, 'l/100km|l/100 km|liter pro 100 km'], ['km/l', 'Kilometer pro Liter', 0, 'km/l'], ['mpg (US)', 'Meilen pro US-Gallone', 0, 'mpg|mpg us'], ['mpg (UK)', 'Meilen pro brit. Gallone', 0, 'mpg uk']],
    zu: function (u, w) { var k = { 'l/100 km': 0, 'km/l': 100, 'mpg (US)': 100 * 3.785411784 / 1.609344, 'mpg (UK)': 100 * 4.54609 / 1.609344 }[u]; return k ? k / w : w; },
    von: function (u, w) { return KAT.verbrauch.zu(u, w); } }
};
var KAT_REIHE = ['laenge', 'flaeche', 'volumen', 'masse', 'temperatur', 'geschw', 'zeit', 'druck', 'energie', 'leistung', 'kraft', 'daten', 'winkel', 'verbrauch'];
/* Alltagsvergleiche je Größe (Basiswert) */
var VERGLEICH = {
  laenge: [['Blatt Papier (Dicke)', 1e-4], ['Fingerbreite', 0.02], ['Zollstock', 2], ['Fußballfeld (Länge)', 105], ['Eiffelturm', 330], ['Zugspitze (Höhe)', 2962], ['Marathon', 42195], ['Saarland (Ost–West)', 90000], ['Erdumfang', 40075017], ['Entfernung Mond', 384400000]],
  flaeche: [['Briefmarke', 0.0006], ['DIN-A4-Blatt', 0.06237], ['Parkplatz', 12.5], ['Tennisplatz', 260.87], ['Fußballfeld', 7140], ['Saarland', 2569.69e6], ['Deutschland', 357588e6]],
  volumen: [['Teelöffel', 0.005], ['Weinglas', 0.2], ['Gießkanne', 10], ['Badewanne', 150], ['Heizöltank', 5000], ['Schwimmbecken (50 m)', 2.5e6]],
  masse: [['Büroklammer', 0.001], ['Tafel Schokolade', 0.1], ['Liter Wasser', 1], ['Mensch', 75], ['Kleinwagen', 1100], ['Elefant', 6000], ['Blauwal', 150000]],
  geschw: [['Schnecke', 0.001], ['Fußgänger', 1.4], ['Radfahrer', 5.5], ['Autobahn (130 km/h)', 36.1], ['Schall in Luft', 343], ['ISS', 7660]],
  zeit: [['Wimpernschlag', 0.3], ['Fußballspiel', 5400], ['Tag', 86400], ['Jahr', 31556952], ['Menschenleben (80 J)', 2.52e9]],
  energie: [['Kalorie', 4.184], ['Tafel Schokolade', 2.2e6], ['Liter Heizöl', 3.6e7], ['Jahresstrom 2-Pers.-Haushalt', 9e9]],
  leistung: [['LED-Lampe', 8], ['Laptop', 60], ['Wasserkocher', 2000], ['Kleinwagen (70 PS)', 51500], ['Windrad', 3e6]],
  druck: [['Luftdruck auf Meereshöhe', 101325], ['Autoreifen', 250000], ['Wasserleitung', 400000]],
  daten: [['Textseite', 2000], ['Foto (Handy)', 3e6], ['Spielfilm (HD)', 4e9]],
  kraft: [['Apfel (Gewicht)', 1], ['Mensch (Gewicht)', 736]],
  winkel: [['rechter Winkel', 90], ['Vollkreis', 360]]
};
var ALIAS = {};
function aliasRein(s) { return String(s).toLowerCase().replace(/\s+/g, ' ').replace(/\s*\/\s*/g, '/').trim(); }
function aliasAdd(a, x) { a = aliasRein(a); if (!a) return; (ALIAS[a] = ALIAS[a] || []).push(x); }
KAT_REIHE.forEach(function (k) {
  KAT[k].e.forEach(function (u) {
    var x = { kat: k, id: u[0] }, seen = {};
    [u[0]].concat(u[3].split('|')).forEach(function (a) { var r = aliasRein(a); if (!seen[r]) { seen[r] = 1; aliasAdd(r, x); } });
  });
});
function einheitFinden(s) {
  s = aliasRein(s).replace(/^(?:grad\s+)?(?=°)/, '');
  var kand = [s, s.replace(/n$/, ''), s.replace(/en$/, ''), s.replace(/e$/, ''), s.replace(/s$/, ''), s.replace(/^in\s+/, '')];
  for (var i = 0; i < kand.length; i++) if (ALIAS[kand[i]]) return ALIAS[kand[i]];
  return null;
}
function einheitPaar(a, b) {
  var A = einheitFinden(a), B = einheitFinden(b);
  if (!A || !B) return null;
  for (var i = 0; i < A.length; i++) for (var j = 0; j < B.length; j++) if (A[i].kat === B[j].kat) return [A[i], B[j]];
  return { fehler: true, A: A, B: B };
}
function einheit(kat, id) { var e = KAT[kat].e; for (var i = 0; i < e.length; i++) if (e[i][0] === id) return e[i]; return null; }
function umrechnen(kat, von, nach, w) {
  var K = KAT[kat];
  if (K.spezial) return K.von(nach, K.zu(von, w));
  return w * einheit(kat, von)[2] / einheit(kat, nach)[2];
}
/* Küche: Dichte in g/ml (Richtwerte) */
var ZUTATEN = [['wasser', 'Wasser', 1.0], ['milch', 'Milch', 1.03], ['sahne', 'Sahne', 1.0], ['oel', 'Öl', 0.92], ['butter', 'Butter', 0.91], ['honig', 'Honig', 1.42],
  ['mehl', 'Weizenmehl', 0.55], ['zucker', 'Zucker', 0.85], ['puderzucker', 'Puderzucker', 0.56], ['salz', 'Salz', 1.2], ['reis', 'Reis (roh)', 0.85],
  ['hafer', 'Haferflocken', 0.41], ['kakao', 'Kakaopulver', 0.45], ['staerke', 'Speisestärke', 0.6], ['nuesse', 'Nüsse, gemahlen', 0.45]];
var ZUTAT_ALIAS = { 'wasser': 'wasser', 'milch': 'milch', 'sahne': 'sahne', 'öl': 'oel', 'oel': 'oel', 'speiseöl': 'oel', 'olivenöl': 'oel', 'butter': 'butter', 'honig': 'honig', 'mehl': 'mehl', 'weizenmehl': 'mehl',
  'zucker': 'zucker', 'puderzucker': 'puderzucker', 'salz': 'salz', 'reis': 'reis', 'haferflocken': 'hafer', 'kakao': 'kakao', 'kakaopulver': 'kakao', 'stärke': 'staerke', 'speisestärke': 'staerke', 'nüsse': 'nuesse', 'mandeln': 'nuesse' };
var KUECHE_E = [['ml', 'ml', 'v', 1], ['l', 'l', 'v', 1000], ['TL', 'TL (5 ml)', 'v', 5], ['EL', 'EL (15 ml)', 'v', 15], ['Tasse', 'Tasse (250 ml)', 'v', 250], ['cup', 'US-Cup (236,6 ml)', 'v', 236.5882365],
  ['g', 'g', 'm', 1], ['kg', 'kg', 'm', 1000], ['oz', 'oz (28,35 g)', 'm', 28.349523125], ['lb', 'lb (453,6 g)', 'm', 453.59237]];
function zutat(id) { for (var i = 0; i < ZUTATEN.length; i++) if (ZUTATEN[i][0] === id) return ZUTATEN[i]; return ZUTATEN[0]; }
function kuecheE(id) { for (var i = 0; i < KUECHE_E.length; i++) if (KUECHE_E[i][0] === id) return KUECHE_E[i]; return null; }

/* ===================================================================== 4. Währungen (Richtwerte, EUR-Basis) */
var KURS_STAND = '11/2026';
var WAEHRUNGEN = [
  ['EUR', 'Euro', 1, 'euro|€|eur'], ['USD', 'US-Dollar', 1.16, 'dollar|us-dollar|$|usd'], ['GBP', 'Britisches Pfund', 0.88, 'pfund sterling|britische pfund|britisches pfund|£|gbp'],
  ['CHF', 'Schweizer Franken', 0.93, 'franken|schweizer franken|chf'], ['JPY', 'Japanischer Yen', 178, 'yen|¥|jpy'], ['CNY', 'Chinesischer Yuan', 8.25, 'yuan|renminbi|cny'],
  ['CAD', 'Kanadischer Dollar', 1.62, 'kanadische dollar|cad'], ['AUD', 'Australischer Dollar', 1.77, 'australische dollar|aud'], ['NZD', 'Neuseeland-Dollar', 2.02, 'nzd'],
  ['SEK', 'Schwedische Krone', 10.95, 'schwedische kronen|sek'], ['NOK', 'Norwegische Krone', 11.7, 'norwegische kronen|nok'], ['DKK', 'Dänische Krone', 7.46, 'dänische kronen|dkk'],
  ['PLN', 'Polnischer Złoty', 4.25, 'zloty|złoty|pln'], ['CZK', 'Tschechische Krone', 24.4, 'tschechische kronen|czk'], ['HUF', 'Ungarischer Forint', 390, 'forint|huf'],
  ['RON', 'Rumänischer Leu', 5.08, 'leu|lei|ron'], ['TRY', 'Türkische Lira', 49, 'türkische lira|lira|try'], ['INR', 'Indische Rupie', 102.5, 'rupie|rupien|inr'],
  ['KRW', 'Südkoreanischer Won', 1650, 'won|krw'], ['BRL', 'Brasilianischer Real', 6.25, 'real|brl'], ['MXN', 'Mexikanischer Peso', 21.3, 'peso|mexikanische peso|mxn'],
  ['ZAR', 'Südafrikanischer Rand', 20.3, 'rand|zar'], ['SGD', 'Singapur-Dollar', 1.51, 'sgd'], ['HKD', 'Hongkong-Dollar', 9.03, 'hkd'], ['THB', 'Thailändischer Baht', 37.8, 'baht|thb'],
  ['ISK', 'Isländische Krone', 147, 'isländische kronen|isk'], ['ILS', 'Israelischer Schekel', 3.85, 'schekel|ils'], ['AED', 'VAE-Dirham', 4.26, 'dirham|aed']];
var W_ALIAS = {};
WAEHRUNGEN.forEach(function (w) { w[3].split('|').concat([w[0].toLowerCase()]).forEach(function (a) { W_ALIAS[a] = w[0]; }); });
function waehrungFinden(s) { s = aliasRein(s); return W_ALIAS[s] || W_ALIAS[s.replace(/n$/, '')] || W_ALIAS[s.replace(/s$/, '')] || null; }
function richtKurse() { var k = {}; WAEHRUNGEN.forEach(function (w) { k[w[0]] = w[2]; }); return k; }
function waehrungName(c) { for (var i = 0; i < WAEHRUNGEN.length; i++) if (WAEHRUNGEN[i][0] === c) return WAEHRUNGEN[i][1]; return c; }

/* ===================================================================== 5. Chemie */
var EL_ROH = 'H,Wasserstoff,1.00794;He,Helium,4.0026;Li,Lithium,6.941;Be,Beryllium,9.0122;B,Bor,10.811;C,Kohlenstoff,12.0107;N,Stickstoff,14.0067;O,Sauerstoff,15.9994;F,Fluor,18.9984;Ne,Neon,20.1797;' +
  'Na,Natrium,22.9898;Mg,Magnesium,24.305;Al,Aluminium,26.9815;Si,Silicium,28.0855;P,Phosphor,30.9738;S,Schwefel,32.065;Cl,Chlor,35.453;Ar,Argon,39.948;K,Kalium,39.0983;Ca,Calcium,40.078;' +
  'Sc,Scandium,44.9559;Ti,Titan,47.867;V,Vanadium,50.9415;Cr,Chrom,51.9961;Mn,Mangan,54.938;Fe,Eisen,55.845;Co,Cobalt,58.9332;Ni,Nickel,58.6934;Cu,Kupfer,63.546;Zn,Zink,65.38;' +
  'Ga,Gallium,69.723;Ge,Germanium,72.63;As,Arsen,74.9216;Se,Selen,78.971;Br,Brom,79.904;Kr,Krypton,83.798;Rb,Rubidium,85.4678;Sr,Strontium,87.62;Y,Yttrium,88.9058;Zr,Zirconium,91.224;' +
  'Nb,Niob,92.9064;Mo,Molybdän,95.95;Tc,Technetium,98*;Ru,Ruthenium,101.07;Rh,Rhodium,102.9055;Pd,Palladium,106.42;Ag,Silber,107.8682;Cd,Cadmium,112.414;In,Indium,114.818;Sn,Zinn,118.71;' +
  'Sb,Antimon,121.76;Te,Tellur,127.6;I,Iod,126.9045;Xe,Xenon,131.293;Cs,Caesium,132.9055;Ba,Barium,137.327;La,Lanthan,138.9055;Ce,Cer,140.116;Pr,Praseodym,140.9077;Nd,Neodym,144.242;' +
  'Pm,Promethium,145*;Sm,Samarium,150.36;Eu,Europium,151.964;Gd,Gadolinium,157.25;Tb,Terbium,158.9254;Dy,Dysprosium,162.5;Ho,Holmium,164.9303;Er,Erbium,167.259;Tm,Thulium,168.9342;Yb,Ytterbium,173.045;' +
  'Lu,Lutetium,174.9668;Hf,Hafnium,178.49;Ta,Tantal,180.9479;W,Wolfram,183.84;Re,Rhenium,186.207;Os,Osmium,190.23;Ir,Iridium,192.217;Pt,Platin,195.084;Au,Gold,196.9666;Hg,Quecksilber,200.592;' +
  'Tl,Thallium,204.38;Pb,Blei,207.2;Bi,Bismut,208.9804;Po,Polonium,209*;At,Astat,210*;Rn,Radon,222*;Fr,Francium,223*;Ra,Radium,226*;Ac,Actinium,227*;Th,Thorium,232.0377;' +
  'Pa,Protactinium,231.0359;U,Uran,238.0289;Np,Neptunium,237*;Pu,Plutonium,244*;Am,Americium,243*;Cm,Curium,247*;Bk,Berkelium,247*;Cf,Californium,251*;Es,Einsteinium,252*;Fm,Fermium,257*;' +
  'Md,Mendelevium,258*;No,Nobelium,259*;Lr,Lawrencium,262*;Rf,Rutherfordium,267*;Db,Dubnium,268*;Sg,Seaborgium,269*;Bh,Bohrium,270*;Hs,Hassium,269*;Mt,Meitnerium,278*;Ds,Darmstadtium,281*;' +
  'Rg,Roentgenium,282*;Cn,Copernicium,285*;Nh,Nihonium,286*;Fl,Flerovium,289*;Mc,Moscovium,290*;Lv,Livermorium,293*;Ts,Tenness,294*;Og,Oganesson,294*';
var GRENZEN = [2, 10, 18, 36, 54, 86, 118];
var KAT_EL = { alkali: 'Alkalimetall', erdalkali: 'Erdalkalimetall', uebergang: 'Übergangsmetall', f: 'Lanthanoid / Actinoid', metall: 'Metall (Hauptgruppe)', halbmetall: 'Halbmetall', nichtmetall: 'Nichtmetall', halogen: 'Halogen', edelgas: 'Edelgas' };
var ELEMENTE = [], EL = {};
EL_ROH.split(';').forEach(function (z, i) {
  var p = z.split(','), Z = i + 1, instabil = /\*$/.test(p[2]), per = 0;
  while (Z > GRENZEN[per]) per++;
  var vor = per ? GRENZEN[per - 1] : 0, n = Z - vor, g = null, zeile = per + 1, spalte;
  if (per === 0) g = n === 1 ? 1 : 18;
  else if (per <= 2) g = n <= 2 ? n : n + 10;
  else if (per <= 4) g = n;
  else { if (n <= 2) g = n; else if (n <= 17) g = null; else g = n - 14; }
  spalte = g; if (g === null) { zeile = per + 4; spalte = n; }
  var k;
  if (g === 18) k = 'edelgas'; else if (g === 17) k = 'halogen'; else if (g === 1 && Z > 1) k = 'alkali'; else if (g === 2) k = 'erdalkali';
  else if (g === null) k = 'f'; else if (g >= 3 && g <= 12) k = 'uebergang';
  else if ([5, 14, 32, 33, 51, 52].indexOf(Z) >= 0) k = 'halbmetall'; else if ([1, 6, 7, 8, 15, 16, 34].indexOf(Z) >= 0) k = 'nichtmetall'; else k = 'metall';
  var e = { z: Z, s: p[0], n: p[1], m: parseFloat(p[2]), instabil: instabil, periode: per + 1, gruppe: g, zeile: zeile, spalte: spalte, kat: k };
  ELEMENTE.push(e); EL[p[0]] = e;
});
var STOFFE = { 'wasser': 'H2O', 'kochsalz': 'NaCl', 'salz': 'NaCl', 'natriumchlorid': 'NaCl', 'schwefelsäure': 'H2SO4', 'salzsäure': 'HCl', 'salpetersäure': 'HNO3', 'kohlendioxid': 'CO2', 'kohlenmonoxid': 'CO',
  'glucose': 'C6H12O6', 'glukose': 'C6H12O6', 'traubenzucker': 'C6H12O6', 'saccharose': 'C12H22O11', 'zucker': 'C12H22O11', 'ethanol': 'C2H5OH', 'alkohol': 'C2H5OH', 'methan': 'CH4', 'ammoniak': 'NH3',
  'natronlauge': 'NaOH', 'natriumhydroxid': 'NaOH', 'kalk': 'CaCO3', 'calciumcarbonat': 'CaCO3', 'kalkstein': 'CaCO3', 'natron': 'NaHCO3', 'essigsäure': 'CH3COOH', 'zitronensäure': 'C6H8O7', 'citronensäure': 'C6H8O7',
  'sauerstoff': 'O2', 'stickstoff': 'N2', 'wasserstoff': 'H2', 'ozon': 'O3', 'kupfersulfat': 'CuSO4', 'kupfervitriol': 'CuSO4·5H2O', 'koffein': 'C8H10N4O2', 'gips': 'CaSO4·2H2O', 'löschkalk': 'Ca(OH)2', 'calciumhydroxid': 'Ca(OH)2',
  'propan': 'C3H8', 'butan': 'C4H10', 'harnstoff': 'CO(NH2)2', 'ascorbinsäure': 'C6H8O6', 'vitamin c': 'C6H8O6', 'magnesiumsulfat': 'MgSO4', 'bittersalz': 'MgSO4·7H2O', 'eisenoxid': 'Fe2O3', 'rost': 'Fe2O3', 'quarz': 'SiO2' };
function formelLesen(f) {
  var s = String(f == null ? '' : f).replace(/[₀-₉]/g, function (c) { return String(c.charCodeAt(0) - 0x2080); }).replace(/\s+/g, '').replace(/[·•∙⋅*]/g, '.').replace(/[\[{]/g, '(').replace(/[\]}]/g, ')');
  if (!s) throw new Error('Bitte eine Summenformel eingeben, z. B. H2SO4.');
  if (!/[A-Z]/.test(s)) throw new Error('Elementsymbole beginnen mit Großbuchstaben (z. B. NaCl statt nacl).');
  var gesamt = {};
  function addMul(z, q, k) { for (var e in q) z[e] = (z[e] || 0) + q[e] * k; }
  s.split('.').forEach(function (t) {
    var m = /^(\d+)(.*)$/.exec(t), k = 1, i = 0;
    if (m) { k = +m[1]; t = m[2]; }
    if (!t) throw new Error('Ein Teil der Formel ist leer.');
    function zahlNach() { var m2 = /^\d+/.exec(t.slice(i)); if (m2) { i += m2[0].length; return +m2[0]; } return 1; }
    function gruppe() {
      var c = {};
      while (i < t.length) {
        var ch = t[i];
        if (ch === '(') { i++; var inner = gruppe(); if (t[i] !== ')') throw new Error('Eine Klammer ist nicht geschlossen.'); i++; addMul(c, inner, zahlNach()); }
        else if (ch === ')') break;
        else if (/[A-Z]/.test(ch)) {
          var sym = ch; i++;
          if (i < t.length && /[a-z]/.test(t[i])) { sym += t[i]; i++; }
          if (!EL[sym]) throw new Error('Unbekanntes Elementsymbol „' + sym + '“.');
          c[sym] = (c[sym] || 0) + zahlNach();
        } else throw new Error('Unerwartetes Zeichen „' + ch + '“ in der Formel.');
      }
      return c;
    }
    var g = gruppe(); if (i < t.length) throw new Error('Eine schließende Klammer ist überzählig.');
    addMul(gesamt, g, k);
  });
  return gesamt;
}
function formelHuebsch(f) {
  return esc(String(f).replace(/\s+/g, '').replace(/[.*•∙⋅]/g, '·')).replace(/([A-Za-z)\]])(\d+)/g, function (a, b, c) { return b + c.split('').map(function (d) { return '₀₁₂₃₄₅₆₇₈₉'[+d]; }).join(''); });
}
function stoffZuFormel(s) { var k = String(s || '').trim(); var l = k.toLowerCase(); return STOFFE[l] ? { formel: STOFFE[l], name: k.charAt(0).toUpperCase() + k.slice(1) } : { formel: k, name: '' }; }
function molMasse(f) {
  var st = stoffZuFormel(f), c = formelLesen(st.formel), M = 0, teile = [];
  for (var s in c) { var m = EL[s].m * c[s]; M += m; teile.push({ s: s, n: c[s], el: EL[s], m: m }); }
  teile.forEach(function (t) { t.anteil = t.m / M; });
  return { M: M, teile: teile, formel: st.formel, name: st.name };
}

/* ===================================================================== 6. Kalender (über Julianische Tageszahl) */
var WT = ['Sonntag', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag'];
var WTK = ['So', 'Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa'];
var MON = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'];
function fl(x) { return Math.floor(x); }
function mod(a, b) { return ((a % b) + b) % b; }
function jdnG(y, m, d) { var a = fl((14 - m) / 12), yy = y + 4800 - a, mm = m + 12 * a - 3; return d + fl((153 * mm + 2) / 5) + 365 * yy + fl(yy / 4) - fl(yy / 100) + fl(yy / 400) - 32045; }
function jdnJ(y, m, d) { var a = fl((14 - m) / 12), yy = y + 4800 - a, mm = m + 12 * a - 3; return d + fl((153 * mm + 2) / 5) + 365 * yy + fl(yy / 4) - 32083; }
function ausJdnG(J) {
  var a = J + 32044, b = fl((4 * a + 3) / 146097), c = a - fl(146097 * b / 4), d = fl((4 * c + 3) / 1461), e = c - fl(1461 * d / 4), m = fl((5 * e + 2) / 153);
  return { y: 100 * b + d - 4800 + fl(m / 10), m: m + 3 - 12 * fl(m / 10), d: e - fl((153 * m + 2) / 5) + 1 };
}
function ausJdnJ(J) {
  var c = J + 32082, d = fl((4 * c + 3) / 1461), e = c - fl(1461 * d / 4), m = fl((5 * e + 2) / 153);
  return { y: d - 4800 + fl(m / 10), m: m + 3 - 12 * fl(m / 10), d: e - fl((153 * m + 2) / 5) + 1 };
}
function jdn(y, m, d, kal) { return kal === 'j' ? jdnJ(y, m, d) : jdnG(y, m, d); }
function ausJdn(J, kal) { return kal === 'j' ? ausJdnJ(J) : ausJdnG(J); }
function wochentag(J) { return mod(J + 1, 7); } /* 0 = Sonntag */
function schaltG(y) { return mod(y, 4) === 0 && (mod(y, 100) !== 0 || mod(y, 400) === 0); }
function schaltJ(y) { return mod(y, 4) === 0; }
function monLaenge(y, m, kal) { if (m === 2) return (kal === 'j' ? schaltJ(y) : schaltG(y)) ? 29 : 28; return [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1]; }
function jahrText(y) { return y > 0 ? String(y) : (1 - y) + ' v. Chr.'; }
function datumLang(o) { return o.d + '. ' + MON[o.m - 1] + ' ' + jahrText(o.y); }
function datumKurz(o) { return (o.d < 10 ? '0' : '') + o.d + '.' + (o.m < 10 ? '0' : '') + o.m + '.' + (o.y > 0 ? o.y : jahrText(o.y)); }
function heuteDatum(ms) { var d = ms != null ? new Date(ms) : new Date(); return { y: d.getFullYear(), m: d.getMonth() + 1, d: d.getDate() }; }
var MON_NAMEN = { januar: 1, jan: 1, jänner: 1, februar: 2, feb: 2, märz: 3, maerz: 3, mär: 3, april: 4, apr: 4, mai: 5, juni: 6, jun: 6, juli: 7, jul: 7, august: 8, aug: 8, september: 9, sep: 9, sept: 9, oktober: 10, okt: 10, november: 11, nov: 11, dezember: 12, dez: 12 };
/* Datum lesen: „24.12.2031“, „24.12.“, „1.1.500 v. Chr.“, „24. Dezember 2031“, „2031-12-24“ */
function datumLesen(s, kal, ctxHeute) {
  if (s && typeof s === 'object') return s;
  s = String(s == null ? '' : s).trim().toLowerCase().replace(/[−–]/g, '-');
  if (!s) return null;
  var h = ctxHeute || heuteDatum();
  if (s === 'heute') return { y: h.y, m: h.m, d: h.d };
  var vchr = /(v\.?\s*chr\.?|v\.?\s*u\.?\s*z\.?)\s*$/.test(s);
  s = s.replace(/(v\.?\s*chr\.?|v\.?\s*u\.?\s*z\.?|n\.?\s*chr\.?|u\.?\s*z\.?)\s*$/, '').trim();
  var y, m, d, ohne = false, r;
  if ((r = /^(\d{1,2})\.\s*(\d{1,2})\.?\s*(-?\d{1,7})?$/.exec(s))) { d = +r[1]; m = +r[2]; y = r[3] != null ? +r[3] : null; }
  else if ((r = /^(\d{1,2})\.?\s*([a-zäöü]+)\.?\s*(-?\d{1,7})?$/.exec(s)) && MON_NAMEN[r[2]]) { d = +r[1]; m = MON_NAMEN[r[2]]; y = r[3] != null ? +r[3] : null; }
  else if ((r = /^(-?\d{1,7})-(\d{1,2})-(\d{1,2})$/.exec(s))) { y = +r[1]; m = +r[2]; d = +r[3]; }
  else return null;
  if (y === null) { y = h.y; ohne = true; }
  else if (r[3] != null && /^\d{2}$/.test(r[3]) && !vchr && /^(\d{1,2})\./.test(s)) { y = 2000 + y > h.y + 30 ? 1900 + y : 2000 + y; }
  if (vchr) { if (y <= 0) return null; y = 1 - y; }
  if (m < 1 || m > 12 || d < 1 || d > monLaenge(y, m, kal)) return null;
  return { y: y, m: m, d: d, ohneJahr: ohne };
}
function plusMonate(o, n, kal) {
  var t = o.y * 12 + (o.m - 1) + n, y = fl(t / 12), m = t - 12 * y + 1;
  return { y: y, m: m, d: Math.min(o.d, monLaenge(y, m, kal)) };
}
function differenzYMD(a, b, kal) { /* a <= b */
  var y = b.y - a.y, m = b.m - a.m, d = b.d - a.d;
  if (d < 0) { m--; var pm = b.m - 1 || 12, py = b.m === 1 ? b.y - 1 : b.y; d += monLaenge(py, pm, kal); }
  if (m < 0) { y--; m += 12; }
  return { y: y, m: m, d: d };
}
function ymdText(o) {
  var p = [];
  if (o.y) p.push(gz(o.y) + (o.y === 1 ? ' Jahr' : ' Jahre'));
  if (o.m) p.push(o.m + (o.m === 1 ? ' Monat' : ' Monate'));
  if (o.d || !p.length) p.push(o.d + (o.d === 1 ? ' Tag' : ' Tage'));
  return p.join(', ');
}
function isoWoche(J) {
  var wd = mod(J, 7) + 1, thu = J - wd + 4, ty = ausJdnG(thu).y;
  return { w: fl((thu - jdnG(ty, 1, 1)) / 7) + 1, y: ty };
}
function tagDesJahres(o, kal) { return jdn(o.y, o.m, o.d, kal) - jdn(o.y, 1, 1, kal) + 1; }
function osternG(y) {
  var a = mod(y, 19), b = fl(y / 100), c = mod(y, 100), d = fl(b / 4), e = mod(b, 4), f = fl((b + 8) / 25), g = fl((b - f + 1) / 3), h = mod(19 * a + b - d - g + 15, 30),
    i = fl(c / 4), k = mod(c, 4), l = mod(32 + 2 * e + 2 * i - h - k, 7), m = fl((a + 11 * h + 22 * l) / 451), mon = fl((h + l - 7 * m + 114) / 31), tag = mod(h + l - 7 * m + 114, 31) + 1;
  return { y: y, m: mon, d: tag };
}
function osternJ(y) { var a = mod(y, 4), b = mod(y, 7), c = mod(y, 19), d = mod(19 * c + 15, 30), e = mod(2 * a + 4 * b - d + 34, 7); return { y: y, m: fl((d + e + 114) / 31), d: mod(d + e + 114, 31) + 1 }; }
var LAENDER = [['BW', 'Baden-Württemberg'], ['BY', 'Bayern'], ['BE', 'Berlin'], ['BB', 'Brandenburg'], ['HB', 'Bremen'], ['HH', 'Hamburg'], ['HE', 'Hessen'], ['MV', 'Mecklenburg-Vorpommern'],
  ['NI', 'Niedersachsen'], ['NW', 'Nordrhein-Westfalen'], ['RP', 'Rheinland-Pfalz'], ['SL', 'Saarland'], ['SN', 'Sachsen'], ['ST', 'Sachsen-Anhalt'], ['SH', 'Schleswig-Holstein'], ['TH', 'Thüringen']];
function feiertage(y, land) {
  var L = [], E = jdnG(osternG(y).y, osternG(y).m, osternG(y).d);
  function in_(l) { return l.split(' ').indexOf(land) >= 0; }
  function add(J, n, gesetzlich, hinweis) { L.push({ J: J, n: n, g: gesetzlich !== false, h: hinweis || '' }); }
  function fest(m, d, n, g, h) { add(jdnG(y, m, d), n, g, h); }
  fest(1, 1, 'Neujahr');
  if (in_('BW BY ST')) fest(1, 6, 'Heilige Drei Könige');
  if ((land === 'BE' && y >= 2019) || (land === 'MV' && y >= 2023)) fest(3, 8, 'Internationaler Frauentag');
  add(E - 48, 'Rosenmontag', false); add(E - 46, 'Aschermittwoch', false); add(E - 3, 'Gründonnerstag', false);
  add(E - 2, 'Karfreitag'); add(E, 'Ostersonntag', land === 'BB'); add(E + 1, 'Ostermontag');
  fest(5, 1, 'Tag der Arbeit'); add(E + 39, 'Christi Himmelfahrt'); add(E + 49, 'Pfingstsonntag', land === 'BB'); add(E + 50, 'Pfingstmontag');
  if (in_('BW BY HE NW RP SL')) add(E + 60, 'Fronleichnam'); else if (in_('SN TH')) add(E + 60, 'Fronleichnam', false, 'nur in einzelnen Gemeinden');
  if (land === 'SL') fest(8, 15, 'Mariä Himmelfahrt'); else if (land === 'BY') fest(8, 15, 'Mariä Himmelfahrt', true, 'in Gemeinden mit überwiegend kath. Bevölkerung');
  if (land === 'TH' && y >= 2019) fest(9, 20, 'Weltkindertag');
  if (y >= 1990) fest(10, 3, 'Tag der Deutschen Einheit');
  if (y === 2017 || in_('BB MV SN ST TH') || (in_('HB HH NI SH') && y >= 2018)) fest(10, 31, 'Reformationstag'); else fest(10, 31, 'Reformationstag', false);
  if (in_('BW BY NW RP SL')) fest(11, 1, 'Allerheiligen');
  var bb = jdnG(y, 11, 22); while (wochentag(bb) !== 3) bb--;
  add(bb, 'Buß- und Bettag', land === 'SN');
  fest(12, 24, 'Heiligabend', false); fest(12, 25, '1. Weihnachtstag'); fest(12, 26, '2. Weihnachtstag'); fest(12, 31, 'Silvester', false);
  L.sort(function (a, b) { return a.J - b.J; });
  return L;
}
function istFeiertag(J, land, cache) {
  var y = ausJdnG(J).y, k = y + land;
  if (!cache[k]) { cache[k] = {}; feiertage(y, land).forEach(function (f) { if (f.g) cache[k][f.J] = f.n; }); }
  return cache[k][J] || null;
}
function arbeitstage(J1, J2, land) {
  if (J2 < J1) { var t = J1; J1 = J2; J2 = t; }
  if (J2 - J1 > 400000) return null;
  var n = 0, c = {};
  for (var J = J1; J <= J2; J++) { var w = wochentag(J); if (w > 0 && w < 6 && !istFeiertag(J, land, c)) n++; }
  return n;
}
/* Mondphase (Näherung über mittleren synodischen Monat) */
var SYN = 29.530588853;
function mondphase(JD) {
  var alter = mod(JD - 2451550.1, SYN), f = alter / SYN, beleuchtet = (1 - Math.cos(2 * Math.PI * f)) / 2, n;
  if (alter < 1.85 || alter > SYN - 1.85) n = 'Neumond'; else if (alter < 5.53) n = 'Zunehmende Sichel'; else if (alter < 9.22) n = 'Erstes Viertel'; else if (alter < 12.91) n = 'Zunehmender Mond';
  else if (alter < 16.61) n = 'Vollmond'; else if (alter < 20.30) n = 'Abnehmender Mond'; else if (alter < 23.99) n = 'Letztes Viertel'; else n = 'Abnehmende Sichel';
  var bisVoll = mod(SYN / 2 - alter, SYN), bisNeu = SYN - alter;
  return { alter: alter, f: f, beleuchtet: beleuchtet, name: n, bisVoll: bisVoll, bisNeu: bisNeu };
}
/* Tagundnachtgleichen und Sonnenwenden (Meeus, mittlere Werte, Näherung) */
function jahreszeiten(y) {
  var T, Y;
  if (y >= 1000 && y <= 3000) {
    Y = (y - 2000) / 1000;
    T = [[2451623.80984, 365242.37404, 0.05169, -0.00411, -0.00057], [2451716.56767, 365241.62603, 0.00325, 0.00888, -0.0003], [2451810.21715, 365242.01767, -0.11575, 0.00337, 0.00078], [2451900.05952, 365242.74049, -0.06223, -0.00823, 0.00032]];
  } else if (y >= -1000 && y < 1000) {
    Y = y / 1000;
    T = [[1721139.29189, 365242.1374, 0.06134, 0.00111, -0.00071], [1721233.25401, 365241.72562, -0.05323, 0.00907, 0.00025], [1721325.70455, 365242.49558, -0.11677, -0.00297, 0.00074], [1721414.39987, 365242.88257, -0.00769, -0.00933, -0.00006]];
  } else return null;
  var namen = ['Frühlingsanfang (Tagundnachtgleiche)', 'Sommeranfang (Sonnenwende)', 'Herbstanfang (Tagundnachtgleiche)', 'Winteranfang (Sonnenwende)'];
  return T.map(function (c, i) { var JDE = c[0] + c[1] * Y + c[2] * Y * Y + c[3] * Y * Y * Y + c[4] * Y * Y * Y * Y; return { n: namen[i], JD: JDE }; });
}
function jdZuDatumZeit(JD) {
  var J = fl(JD + 0.5), frac = JD + 0.5 - J, min = Math.round(frac * 1440);
  if (min >= 1440) { J++; min -= 1440; }
  var kal = J >= 2299161 ? 'g' : 'j';
  return { dat: ausJdn(J, kal), kal: kal, J: J, h: fl(min / 60), min: min % 60 };
}
/* Zeitzonen */
var ZONEN = [['Europe/Berlin', 'Berlin'], ['Europe/London', 'London'], ['America/New_York', 'New York'], ['America/Chicago', 'Chicago'], ['America/Los_Angeles', 'Los Angeles'], ['America/Sao_Paulo', 'São Paulo'],
  ['Europe/Moscow', 'Moskau'], ['Europe/Istanbul', 'Istanbul'], ['Asia/Dubai', 'Dubai'], ['Asia/Kolkata', 'Neu-Delhi'], ['Asia/Bangkok', 'Bangkok'], ['Asia/Shanghai', 'Peking'], ['Asia/Singapore', 'Singapur'],
  ['Asia/Tokyo', 'Tokio'], ['Australia/Sydney', 'Sydney'], ['Pacific/Auckland', 'Auckland'], ['Africa/Johannesburg', 'Johannesburg'], ['Africa/Cairo', 'Kairo'], ['UTC', 'UTC']];
var ZONEN_ALIAS = { berlin: 'Europe/Berlin', deutschland: 'Europe/Berlin', london: 'Europe/London', england: 'Europe/London', 'new york': 'America/New_York', newyork: 'America/New_York', chicago: 'America/Chicago',
  'los angeles': 'America/Los_Angeles', kalifornien: 'America/Los_Angeles', 'são paulo': 'America/Sao_Paulo', 'sao paulo': 'America/Sao_Paulo', brasilien: 'America/Sao_Paulo', moskau: 'Europe/Moscow', istanbul: 'Europe/Istanbul',
  dubai: 'Asia/Dubai', indien: 'Asia/Kolkata', delhi: 'Asia/Kolkata', 'neu-delhi': 'Asia/Kolkata', bangkok: 'Asia/Bangkok', thailand: 'Asia/Bangkok', peking: 'Asia/Shanghai', china: 'Asia/Shanghai', shanghai: 'Asia/Shanghai',
  singapur: 'Asia/Singapore', tokio: 'Asia/Tokyo', tokyo: 'Asia/Tokyo', japan: 'Asia/Tokyo', sydney: 'Australia/Sydney', australien: 'Australia/Sydney', auckland: 'Pacific/Auckland', neuseeland: 'Pacific/Auckland',
  johannesburg: 'Africa/Johannesburg', kairo: 'Africa/Cairo', 'ägypten': 'Africa/Cairo', utc: 'UTC', gmt: 'UTC' };
function zoneName(tz) { for (var i = 0; i < ZONEN.length; i++) if (ZONEN[i][0] === tz) return ZONEN[i][1]; return tz; }
function tzVersatz(tz, ms) {
  try {
    var f = new Intl.DateTimeFormat('en-US', { timeZone: tz, hourCycle: 'h23', year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric' }), p = {};
    f.formatToParts(new Date(ms)).forEach(function (x) { p[x.type] = x.value; });
    return Math.round((Date.UTC(+p.year, +p.month - 1, +p.day, +p.hour % 24, +p.minute, +p.second) - ms) / 60000);
  } catch (e) { return 0; }
}
function versatzText(min) { var s = min < 0 ? '−' : '+', a = Math.abs(min); return 'UTC' + s + fl(a / 60) + (a % 60 ? ':' + (a % 60 < 10 ? '0' : '') + a % 60 : ''); }
function zeitIn(tz, ms) {
  try { return new Intl.DateTimeFormat('de-DE', { timeZone: tz, weekday: 'short', day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' }).format(new Date(ms)); } catch (e) { return '–'; }
}
function zeitLesen(s) { /* „1:30:00“, „45:10“, „90 min“ → Sekunden */
  s = String(s == null ? '' : s).trim().replace(',', '.'); if (!s) return null;
  var r;
  if ((r = /^(\d+):(\d{1,2}):(\d{1,2}(?:\.\d+)?)$/.exec(s))) return +r[1] * 3600 + +r[2] * 60 + +r[3];
  if ((r = /^(\d+):(\d{1,2}(?:\.\d+)?)$/.exec(s))) return +r[1] * 60 + +r[2];
  if ((r = /^(\d+(?:\.\d+)?)\s*(h|std)$/.exec(s))) return +r[1] * 3600;
  if ((r = /^(\d+(?:\.\d+)?)\s*(min)?$/.exec(s))) return +r[1] * 60;
  return null;
}
function dauerText(sek) { sek = Math.round(sek); var h = fl(sek / 3600), m = fl(sek % 3600 / 60), s = sek % 60; return (h ? h + ':' + (m < 10 ? '0' : '') : '') + m + ':' + (s < 10 ? '0' : '') + s; }

/* ===================================================================== 7. Diagramme (SVG-Text, Farben über CSS-Variablen) */
var FARB = ['var(--rz-f1)', 'var(--rz-f2)', 'var(--rz-f3)', 'var(--rz-f4)', 'var(--rz-f5)', 'var(--rz-f6)', 'var(--rz-f7)', 'var(--rz-f8)'];
var svgZ = 0;
function balken(items, opt) {
  opt = opt || {};
  var vals = items.map(function (x) { return Math.abs(x.v); }), max = Math.max.apply(null, vals.concat([1e-300])), lg = opt.log, lmin, lmax;
  if (lg) { var pos = vals.filter(function (v) { return v > 0; }); lmin = Math.log10(Math.min.apply(null, pos)) - 0.3; lmax = Math.log10(Math.max.apply(null, pos)); if (lmax - lmin < 1) lmin = lmax - 1; }
  var h = '<div class="rz-bal" role="img" aria-label="' + esc(opt.titel || 'Balkendiagramm') + '">';
  items.forEach(function (x, i) {
    var w = lg ? (x.v > 0 ? (Math.log10(Math.abs(x.v)) - lmin) / (lmax - lmin) * 100 : 0) : Math.abs(x.v) / max * 100;
    w = Math.max(x.v ? 1.2 : 0, Math.min(100, w));
    h += '<div class="rz-bz' + (x.hl ? ' rz-hl' : '') + '"><span class="rz-bl">' + x.l + '</span><span class="rz-bv">' + (x.txt != null ? x.txt : zahl(x.v)) + '</span>' +
      '<svg class="rz-bs" viewBox="0 0 100 10" preserveAspectRatio="none" aria-hidden="true"><rect class="rz-bh" width="100" height="10"/><rect class="rz-b" width="' + w.toFixed(2) + '" height="10" style="fill:' + (x.f || FARB[i % 8]) + '"/></svg></div>';
  });
  if (lg) h += '<p class="rz-mini">Balkenlänge logarithmisch (jede Stufe = Faktor 10)</p>';
  return h + '</div>';
}
function ring(items, opt) {
  opt = opt || {};
  var sum = items.reduce(function (a, x) { return a + Math.max(0, x.v); }, 0) || 1, r = 46, C = 2 * Math.PI * r, off = 0;
  var s = '<div class="rz-ring"><svg viewBox="0 0 120 120" role="img" aria-label="' + esc(opt.titel || 'Ringdiagramm') + '"><circle cx="60" cy="60" r="' + r + '" class="rz-rh"/><g class="rz-rg" transform="rotate(-90 60 60)">';
  items.forEach(function (x, i) {
    var len = Math.max(0, x.v) / sum * C; if (len <= 0) return;
    s += '<circle cx="60" cy="60" r="' + r + '" fill="none" stroke-width="16" style="stroke:' + (x.f || FARB[i % 8]) + '" stroke-dasharray="' + Math.max(0, len - (items.length > 1 ? 0.8 : 0)).toFixed(2) + ' ' + C.toFixed(2) + '" stroke-dashoffset="' + (-off).toFixed(2) + '"/>';
    off += len;
  });
  s += '</g>';
  if (opt.mitte) s += '<text x="60" y="' + (opt.unter ? 60 : 66) + '" text-anchor="middle" class="rz-rm">' + esc(opt.mitte) + '</text>';
  if (opt.unter) s += '<text x="60" y="78" text-anchor="middle" class="rz-ru">' + esc(opt.unter) + '</text>';
  s += '</svg><ul class="rz-leg">';
  items.forEach(function (x, i) { s += '<li><i style="background:' + (x.f || FARB[i % 8]) + '"></i><span>' + x.l + '</span><b>' + (x.txt != null ? x.txt : zahl(x.v)) + '</b><em>' + dz(Math.max(0, x.v) / sum * 100, 1) + ' %</em></li>'; });
  return s + '</ul></div>';
}
function skala(wert, zonen, min, max, opt) {
  opt = opt || {};
  var p = Math.max(0, Math.min(100, (wert - min) / (max - min) * 100)), s = '<div class="rz-skala" role="img" aria-label="' + esc(opt.titel || 'Skala') + ': ' + esc(zahl(wert, 3)) + '"><svg viewBox="0 0 100 10" preserveAspectRatio="none" aria-hidden="true">', a = min;
  zonen.forEach(function (z, i) { var b = Math.min(z.bis, max), x = (a - min) / (max - min) * 100, w = (b - a) / (max - min) * 100; s += '<rect x="' + x.toFixed(2) + '" width="' + Math.max(0, w).toFixed(2) + '" height="10" style="fill:' + (z.f || FARB[i % 8]) + '"/>'; a = b; });
  s += '</svg><span class="rz-sm" style="left:' + p.toFixed(2) + '%"><b>' + esc(opt.txt || zahl(wert, 3)) + '</b></span><div class="rz-sl">';
  a = min;
  zonen.forEach(function (z) { var b = Math.min(z.bis, max); s += '<span style="flex:' + Math.max(0.0001, b - a) + '">' + esc(z.l) + '</span>'; a = b; });
  return s + '</div></div>';
}
function schoeneTicks(lo, hi, n) {
  if (hi === lo) { hi = lo + 1; }
  var roh = (hi - lo) / n, mag = Math.pow(10, fl(Math.log10(roh))), st = [1, 2, 2.5, 5, 10].map(function (k) { return k * mag; }).filter(function (k) { return k >= roh; })[0] || roh;
  var a = fl(lo / st) * st, t = [];
  for (var v = a; v < hi + st * 0.999; v += st) t.push(rund(v, 12));
  if (t.length < 2) t.push(rund(a + st, 12));
  return t;
}
function kurzZahl(v) { var a = Math.abs(v); if (a >= 1e9) return dz(v / 1e9, 1) + ' Mrd.'; if (a >= 1e6) return dz(v / 1e6, 1) + ' Mio.'; if (a >= 1e4) return dz(v / 1e3, 0) + ' Tsd.'; return zahl(v, 4); }
/* Verlaufsdiagramm im Börsenkurs-Stil; d = { x:[Beschriftungen], s:[{n, w:[], f, flaeche}], fmt:'geld'|'zahl', von, bis } */
function kursSVG(d, W, von, bis) {
  W = Math.max(260, Math.round(W || 600)); var H = 190, pl = 52, pr = 12, pt = 12, pb = 26, id = 'rzg' + (++svgZ);
  von = von || 0; bis = bis == null ? d.x.length - 1 : bis;
  var n = bis - von + 1, alle = [];
  d.s.forEach(function (s) { for (var i = von; i <= bis; i++) alle.push(s.w[i]); });
  var lo = Math.min.apply(null, alle), hi = Math.max.apply(null, alle);
  if (lo > 0 && lo < hi * 0.6) lo = 0;
  var ticks = schoeneTicks(lo, hi, 4); lo = ticks[0]; hi = ticks[ticks.length - 1];
  function X(i) { return pl + (n <= 1 ? 0 : (i - von) / (n - 1) * (W - pl - pr)); }
  function Y(v) { return pt + (1 - (v - lo) / (hi - lo || 1)) * (H - pt - pb); }
  var s = '<svg class="rz-ksvg" viewBox="0 0 ' + W + ' ' + H + '" width="' + W + '" height="' + H + '" tabindex="0" role="img" aria-label="Verlaufsdiagramm, Pfeiltasten zeigen Einzelwerte">';
  s += '<defs><linearGradient id="' + id + '" x1="0" y1="0" x2="0" y2="1"><stop offset="0" style="stop-color:' + d.s[0].f + ';stop-opacity:.32"/><stop offset="1" style="stop-color:' + d.s[0].f + ';stop-opacity:0"/></linearGradient></defs>';
  ticks.forEach(function (t) { var y = Y(t).toFixed(1); s += '<line class="rz-gl" x1="' + pl + '" x2="' + (W - pr) + '" y1="' + y + '" y2="' + y + '"/><text class="rz-ax" x="' + (pl - 6) + '" y="' + (+y + 4) + '" text-anchor="end">' + esc(kurzZahl(t)) + '</text>'; });
  var schritt = Math.max(1, Math.ceil(n / Math.max(2, fl((W - pl) / 70))));
  for (var i = von; i <= bis; i += schritt) s += '<text class="rz-ax" x="' + X(i).toFixed(1) + '" y="' + (H - 8) + '" text-anchor="middle">' + esc(d.x[i]) + '</text>';
  d.s.forEach(function (se, k) {
    var p = '';
    for (var j = von; j <= bis; j++) p += (j === von ? 'M' : 'L') + X(j).toFixed(1) + ' ' + Y(se.w[j]).toFixed(1);
    if (k === 0) s += '<path class="rz-kfl" d="' + p + 'L' + X(bis).toFixed(1) + ' ' + Y(Math.max(lo, 0)).toFixed(1) + 'L' + X(von).toFixed(1) + ' ' + Y(Math.max(lo, 0)).toFixed(1) + 'Z" style="fill:url(#' + id + ')"/>';
    s += '<path class="rz-kl' + (k ? ' rz-kl2' : '') + '" d="' + p + '" pathLength="1" style="stroke:' + se.f + '"/>';
  });
  s += '<g class="rz-km" style="display:none"><line class="rz-kmv" x1="0" x2="0" y1="' + pt + '" y2="' + (H - pb) + '"/>';
  d.s.forEach(function (se) { s += '<circle r="4.5" style="fill:' + se.f + '"/>'; });
  s += '</g></svg>';
  return { svg: s, X: X, Y: Y, von: von, bis: bis };
}

/* ===================================================================== 8. Rechenkarten (Logik + Rechenweg) */
function LeerFehler(t) { this.message = t || 'Bitte Werte eingeben.'; this.leer = true; }
function brauche(v) { for (var i = 1; i < arguments.length; i++) { var x = v[arguments[i]]; if (x == null || (typeof x === 'number' && isNaN(x))) throw new LeerFehler(); } }
function pos(v, k, name) { if (!(v[k] > 0)) throw new Error((name || k) + ' muss größer als 0 sein.'); }
function F(k, l, e, w, x) { var o = { k: k, l: l, e: e || '', w: w }; if (x) for (var a in x) o[a] = x[a]; return o; }
function W(k, l, opt, w, x) { var o = { k: k, l: l, typ: 'wahl', opt: opt, w: w }; if (x) for (var a in x) o[a] = x[a]; return o; }
function D(k, l, w, x) { var o = { k: k, l: l, typ: 'datum', w: w }; if (x) for (var a in x) o[a] = x[a]; return o; }
function T(k, l, w, x) { var o = { k: k, l: l, typ: 'text', w: w }; if (x) for (var a in x) o[a] = x[a]; return o; }
var LAND_OPT = LAENDER.map(function (l) { return [l[0], l[1]]; });
var KAL_OPT = [['g', 'gregorianisch'], ['j', 'julianisch']];
function kalHinweis(y) {
  if (y < -45) return 'Für dieses Jahr ist der Kalender nur zurückgerechnet (proleptisch): Den julianischen Kalender gibt es erst seit 45 v. Chr., den gregorianischen seit 1582. Die Siebentagewoche lief aber lückenlos durch, deshalb lässt sich der Wochentag rechnerisch bestimmen – damals hat ihn so niemand gezählt.';
  if (y < 1582) return 'Vor der Kalenderreform (Oktober 1582) galt historisch der julianische Kalender; das gregorianische Datum ist zurückgerechnet (proleptisch).';
  if (y < 1700) return 'Katholische Gebiete stellten ab 15.10.1582 um, die evangelischen Gebiete Deutschlands erst 1700 – Datumsangaben dieser Zeit sind je nach Ort julianisch oder gregorianisch.';
  return '';
}
function datumZeile(o, kal) { var J = jdn(o.y, o.m, o.d, kal); return datumLang(o) + ' · ' + WT[wochentag(J)]; }
function kalBlatt(o, J, kal) {
  return '<div class="rz-blatt" aria-hidden="true"><span class="rz-blm">' + MON[o.m - 1] + '</span><b>' + o.d + '</b><span class="rz-blj">' + esc(jahrText(o.y)) + '</span><span class="rz-blw">' + WT[wochentag(J)] + (kal === 'j' ? ' (jul.)' : '') + '</span></div>';
}
function datumOderHeute(v, k, ctx, kal) { var d = datumLesen(v[k] == null || v[k] === '' ? 'heute' : v[k], kal, ctx.heute); if (!d) throw new Error('Datum nicht erkannt – bitte z. B. 24.12.2031 oder 1.1.500 v. Chr. eingeben.'); return d; }

var KARTEN = [];
function K(o) { KARTEN.push(o); return o; }

/* ---------- Prozent ---------- */
K({ id: 'p-wert', b: 'prozent', t: 'Prozentwert', u: 'p % von G', f: [F('p', 'Prozentsatz p', '%', 15), F('g', 'Grundwert G', '', 240)],
  r: function (v) { brauche(v, 'p', 'g'); var w = v.g * v.p / 100;
    return { wert: w, gross: zahl(w), label: zahl(v.p) + ' % von ' + zahl(v.g), schritte: ['Formel: W = G · p / 100', 'Einsetzen: W = ' + zahl(v.g) + ' · ' + zahl(v.p) + ' / 100', 'Ergebnis: W = ' + zahl(w)],
      svg: ring([{ l: 'Prozentwert', v: Math.abs(w), txt: zahl(w) }, { l: 'Rest', v: Math.max(0, v.g - w), txt: zahl(Math.max(0, v.g - w)) }], { mitte: zahl(v.p, 4) + ' %' }) }; } });
K({ id: 'p-satz', b: 'prozent', t: 'Prozentsatz', u: 'W ist wie viel % von G?', f: [F('w', 'Prozentwert W', '', 30), F('g', 'Grundwert G', '', 120)],
  r: function (v) { brauche(v, 'w', 'g'); if (v.g === 0) throw new Error('Der Grundwert darf nicht 0 sein.'); var p = v.w / v.g * 100;
    return { wert: p, gross: zahl(p, 6), einh: '%', label: zahl(v.w) + ' von ' + zahl(v.g), schritte: ['Formel: p = W / G · 100', 'Einsetzen: p = ' + zahl(v.w) + ' / ' + zahl(v.g) + ' · 100', 'Ergebnis: p = ' + zahl(p, 6) + ' %'],
      svg: ring([{ l: 'Anteil', v: Math.abs(v.w) }, { l: 'Rest', v: Math.max(0, v.g - v.w) }], { mitte: zahl(p, 3) + ' %' }) }; } });
K({ id: 'p-grund', b: 'prozent', t: 'Grundwert', u: 'W entspricht p % – wie viel sind 100 %?', f: [F('w', 'Prozentwert W', '', 45), F('p', 'Prozentsatz p', '%', 15)],
  r: function (v) { brauche(v, 'w', 'p'); if (v.p === 0) throw new Error('Der Prozentsatz darf nicht 0 sein.'); var g = v.w / v.p * 100;
    return { wert: g, gross: zahl(g), label: '100 %, wenn ' + zahl(v.w) + ' = ' + zahl(v.p) + ' %', schritte: ['Formel: G = W / p · 100', 'Einsetzen: G = ' + zahl(v.w) + ' / ' + zahl(v.p) + ' · 100', 'Ergebnis: G = ' + zahl(g)],
      svg: balken([{ l: zahl(v.p) + ' %', v: v.w }, { l: '100 %', v: g, hl: true }]) }; } });
K({ id: 'p-auf', b: 'prozent', t: 'Aufschlag / Abschlag', u: 'Grundwert um p % erhöhen oder senken', f: [F('g', 'Grundwert', '', 240), F('p', 'Prozentsatz', '%', 19), W('r', 'Richtung', [['+', 'Aufschlag (+)'], ['-', 'Abschlag (−)']], '+')],
  r: function (v) { brauche(v, 'g', 'p'); var f = v.r === '-' ? 1 - v.p / 100 : 1 + v.p / 100, e = v.g * f, d = e - v.g;
    return { wert: e, gross: zahl(e), label: zahl(v.g) + (v.r === '-' ? ' − ' : ' + ') + zahl(v.p) + ' %', zeilen: [['Veränderung', (d >= 0 ? '+' : '') + zahl(d)], ['Faktor', zahl(f)]],
      schritte: ['Faktor q = 1 ' + (v.r === '-' ? '−' : '+') + ' p/100 = ' + zahl(f), 'Ergebnis = G · q = ' + zahl(v.g) + ' · ' + zahl(f) + ' = ' + zahl(e)],
      svg: balken([{ l: 'vorher', v: v.g }, { l: 'nachher', v: e, hl: true }]) }; } });
K({ id: 'p-veraend', b: 'prozent', t: 'Prozentuale Veränderung', u: 'von A auf B', f: [F('a', 'Alter Wert A', '', 80), F('n', 'Neuer Wert B', '', 100)],
  r: function (v) { brauche(v, 'a', 'n'); if (v.a === 0) throw new Error('Der alte Wert darf nicht 0 sein.'); var p = (v.n - v.a) / v.a * 100;
    return { wert: p, gross: (p > 0 ? '+' : '') + zahl(p, 6), einh: '%', label: 'von ' + zahl(v.a) + ' auf ' + zahl(v.n), zeilen: [['Differenz', (v.n - v.a >= 0 ? '+' : '') + zahl(v.n - v.a)], ['Faktor', zahl(v.n / v.a, 6)], ['Rückweg', 'von ' + zahl(v.n) + ' auf ' + zahl(v.a) + ' = ' + zahl((v.a - v.n) / v.n * 100, 4) + ' %']],
      schritte: ['Formel: Δ% = (B − A) / A · 100', 'Einsetzen: (' + zahl(v.n) + ' − ' + zahl(v.a) + ') / ' + zahl(v.a) + ' · 100', 'Ergebnis: ' + zahl(p, 6) + ' %', 'Achtung: Der Rückweg hat eine andere Prozentzahl, weil sich der Grundwert ändert.'],
      svg: balken([{ l: 'A', v: v.a }, { l: 'B', v: v.n, hl: true }]) }; } });
K({ id: 'mwst', b: 'prozent', t: 'Mehrwertsteuer', u: 'brutto ↔ netto, 19 % oder 7 %', f: [F('b', 'Betrag', '€', 100), W('s', 'Steuersatz', [['19', '19 % (Regelsatz)'], ['7', '7 % (ermäßigt)']], '19'), W('r', 'Betrag ist', [['n', 'netto → brutto'], ['b', 'brutto → netto']], 'n')],
  r: function (v) { brauche(v, 'b'); var s = +v.s / 100, net, bru;
    if (v.r === 'b') { bru = v.b; net = bru / (1 + s); } else { net = v.b; bru = net * (1 + s); }
    var st = bru - net;
    return { wert: v.r === 'b' ? net : bru, gross: fix(v.r === 'b' ? net : bru, 2), einh: '€', label: v.r === 'b' ? 'netto (aus ' + geld(bru) + ' brutto)' : 'brutto (aus ' + geld(net) + ' netto)',
      zeilen: [['Netto', geld(net)], ['MwSt. ' + v.s + ' %', geld(st)], ['Brutto', geld(bru)]],
      schritte: v.r === 'b' ? ['Netto = Brutto / (1 + ' + v.s + ' %) = ' + fix(bru, 2) + ' / ' + zahl(1 + s) + ' = ' + fix(net, 2) + ' €', 'Steuer = Brutto − Netto = ' + fix(st, 2) + ' €', 'Häufiger Fehler: Brutto − 19 % ergibt NICHT den Nettobetrag.']
        : ['Brutto = Netto · (1 + ' + v.s + ' %) = ' + fix(net, 2) + ' · ' + zahl(1 + s) + ' = ' + fix(bru, 2) + ' €', 'Steuer = Netto · ' + v.s + ' % = ' + fix(st, 2) + ' €'],
      svg: ring([{ l: 'Netto', v: net, txt: geld(net) }, { l: 'MwSt.', v: st, txt: geld(st) }], { mitte: geld(bru), unter: 'brutto' }) }; } });

/* ---------- Dreisatz, Verhältnis, Rezept ---------- */
K({ id: 'dreisatz', b: 'dreisatz', t: 'Dreisatz', u: 'proportional oder umgekehrt proportional', f: [F('a', 'Menge 1', '', 3), F('b', 'Wert zu Menge 1', '', 7.5), F('c', 'Menge 2', '', 5), W('m', 'Art', [['p', 'je mehr, desto mehr'], ['u', 'je mehr, desto weniger']], 'p')],
  r: function (v) { brauche(v, 'a', 'b', 'c'); if (!v.a || !v.c) throw new Error('Die Mengen dürfen nicht 0 sein.'); var x, e;
    if (v.m === 'u') { x = v.a * v.b / v.c; e = v.a * v.b; return { wert: x, gross: zahl(x), label: 'umgekehrt proportional', schritte: ['1. Schritt (auf 1): ' + zahl(v.a) + ' → ' + zahl(v.b) + ', also 1 → ' + zahl(v.b) + ' · ' + zahl(v.a) + ' = ' + zahl(e), '2. Schritt (auf ' + zahl(v.c) + '): ' + zahl(e) + ' / ' + zahl(v.c) + ' = ' + zahl(x)], zeilen: [['Produkt bleibt gleich', zahl(e)]], svg: balken([{ l: zahl(v.a), v: v.b }, { l: zahl(v.c), v: x, hl: true }]) }; }
    e = v.b / v.a; x = e * v.c;
    return { wert: x, gross: zahl(x), label: 'proportional: ' + zahl(v.c) + ' → ?', zeilen: [['Wert für 1', zahl(e)]], schritte: ['1. Schritt (auf 1): ' + zahl(v.b) + ' / ' + zahl(v.a) + ' = ' + zahl(e), '2. Schritt (auf ' + zahl(v.c) + '): ' + zahl(e) + ' · ' + zahl(v.c) + ' = ' + zahl(x)], svg: balken([{ l: zahl(v.a), v: v.b }, { l: zahl(v.c), v: x, hl: true }]) }; } });
K({ id: 'verhaeltnis', b: 'dreisatz', t: 'Verhältnis', u: 'a : b = c : x', f: [F('a', 'a', '', 2), F('b', 'b', '', 3), F('c', 'c', '', 10)],
  r: function (v) { brauche(v, 'a', 'b', 'c'); if (!v.a) throw new Error('a darf nicht 0 sein.'); var x = v.b * v.c / v.a;
    var g = function (p, q) { p = Math.abs(p); q = Math.abs(q); while (q) { var t = q; q = p % q; p = t; } return p; }, z = '';
    if (Number.isInteger(v.a) && Number.isInteger(v.b) && v.a && v.b) { var k = g(v.a, v.b); z = zahl(v.a / k) + ' : ' + zahl(v.b / k); }
    return { wert: x, gross: zahl(x), label: zahl(v.a) + ' : ' + zahl(v.b) + ' = ' + zahl(v.c) + ' : x', zeilen: z ? [['gekürzt', z], ['als Dezimalzahl', zahl(v.a / v.b, 6)]] : [['als Dezimalzahl', zahl(v.a / v.b, 6)]], schritte: ['x = b · c / a = ' + zahl(v.b) + ' · ' + zahl(v.c) + ' / ' + zahl(v.a) + ' = ' + zahl(x)],
      svg: ring([{ l: 'a', v: v.a }, { l: 'b', v: v.b }], { mitte: zahl(v.a) + ':' + zahl(v.b) }) }; } });
K({ id: 'rezept', b: 'kueche', t: 'Rezept umrechnen', u: 'Portionen skalieren', f: [F('alt', 'Rezept für', 'Portionen', 4), F('neu', 'Gewünscht', 'Portionen', 6), T('zutaten', 'Zutaten (eine pro Zeile)', '500 g Mehl\n250 ml Milch\n3 Eier\n1 Prise Salz\n0,5 TL Backpulver', { zeilen: 5 })],
  r: function (v) { brauche(v, 'alt', 'neu'); pos(v, 'alt', 'Portionen'); var f = v.neu / v.alt, z = [];
    String(v.zutaten || '').split(/\n/).forEach(function (l) { l = l.trim(); if (!l) return; var m = /^((?:\d+[.,]?\d*|[.,]\d+)(?:\s*[-–]\s*\d+[.,]?\d*)?|½|¼|¾)\s*(.*)$/.exec(l);
      if (!m) { z.push([esc(l), '–']); return; }
      var roh = m[1].replace('½', '0,5').replace('¼', '0,25').replace('¾', '0,75'), n = zahlLesen(roh.split(/[-–]/)[0]), rest = m[2];
      var neu = n * f, t = neu >= 10 ? zahl(Math.round(neu), 6) : zahl(neu, 3), em = /^(g|kg|mg|ml|l|cl|dl|el|tl|tasse[n]?|prise[n]?|pck\.?|päckchen|msp\.?|bund|zehe[n]?|scheibe[n]?|becher|dose[n]?|stück|stk\.?)\s+(.*)$/i.exec(rest);
      if (em) { rest = em[2]; t += ' ' + em[1]; }
      if (/^(ei|eier|stück|stk)\b/i.test(rest) || /\bei(er)?\b/i.test(rest)) t = zahl(neu, 2) + (Math.abs(neu - Math.round(neu)) > 0.2 ? ' (≈ ' + Math.max(1, Math.round(neu)) + ')' : '');
      z.push([esc(rest || 'Zutat'), esc(t)]); });
    return { wert: f, gross: '× ' + zahl(f, 4), label: 'Faktor von ' + zahl(v.alt) + ' auf ' + zahl(v.neu) + ' Portionen', zeilen: z, schritte: ['Faktor = neu / alt = ' + zahl(v.neu) + ' / ' + zahl(v.alt) + ' = ' + zahl(f, 6), 'Jede Menge wird mit dem Faktor multipliziert.', 'Gewürze, Backpulver und Hefe eher vorsichtig skalieren; Back- und Garzeiten ändern sich nicht proportional.'] }; } });

/* ---------- Einheiten ---------- */
var KAT_OPT = KAT_REIHE.map(function (k) { return [k, KAT[k].n]; });
function einhOpt(v) { var k = KAT[v.kat] ? v.kat : 'laenge'; return KAT[k].e.map(function (u) { return [u[0], u[0] + ' – ' + u[1]]; }); }
var STD_PAAR = { laenge: ['km', 'mi'], flaeche: ['ha', 'm²'], volumen: ['l', 'gal'], masse: ['kg', 'lb'], temperatur: ['°C', '°F'], geschw: ['km/h', 'mph'], zeit: ['h', 'min'], druck: ['bar', 'psi'], energie: ['kWh', 'MJ'],
  leistung: ['kW', 'PS'], kraft: ['N', 'kp'], daten: ['GB', 'GiB'], winkel: ['°', 'rad'], verbrauch: ['l/100 km', 'mpg (US)'] };
K({ id: 'einheit', b: 'einheiten', t: 'Einheiten umrechnen', u: 'alle Zieleinheiten auf einen Blick', breit: true,
  f: [W('kat', 'Größe', KAT_OPT, 'laenge', { segment: true }), F('w', 'Wert', '', 5), W('von', 'Von', einhOpt, 'km', { dyn: 'kat' }), W('nach', 'Nach', einhOpt, 'mi', { dyn: 'kat', tausch: 'von' })],
  r: function (v) {
    brauche(v, 'w'); var k = KAT[v.kat] ? v.kat : 'laenge', Kt = KAT[k];
    if (!einheit(k, v.von)) v.von = STD_PAAR[k][0]; if (!einheit(k, v.nach)) v.nach = STD_PAAR[k][1];
    if (k === 'verbrauch' && v.w <= 0) throw new Error('Der Verbrauch muss größer als 0 sein.');
    if (k === 'temperatur' && Kt.zu(v.von, v.w) < 0) throw new Error('Unter dem absoluten Nullpunkt (0 K = −273,15 °C) gibt es keine Temperatur.');
    var e = umrechnen(k, v.von, v.nach, v.w), uv = einheit(k, v.von), un = einheit(k, v.nach), schritte = [], zeilen = [], items = [];
    if (k === 'temperatur') {
      var form = { '°C': { '°F': '°F = °C · 9/5 + 32', 'K': 'K = °C + 273,15' }, '°F': { '°C': '°C = (°F − 32) · 5/9', 'K': 'K = (°F + 459,67) · 5/9' }, 'K': { '°C': '°C = K − 273,15', '°F': '°F = K · 9/5 − 459,67' } };
      schritte.push((form[v.von] && form[v.von][v.nach]) || 'Umweg über Kelvin: ' + zahl(v.w) + ' ' + v.von + ' = ' + zahl(Kt.zu(v.von, v.w)) + ' K');
      schritte.push(zahl(v.w) + ' ' + v.von + ' = ' + zahl(e) + ' ' + v.nach);
    } else if (k === 'verbrauch') {
      schritte.push('Verbrauch und Reichweite sind Kehrwerte: km/l = 100 / (l/100 km); mpg (US) = 235,215 / (l/100 km).'); schritte.push(zahl(v.w) + ' ' + v.von + ' = ' + zahl(e) + ' ' + v.nach);
    } else {
      schritte.push('1 ' + v.von + ' = ' + zahl(uv[2]) + ' ' + Kt.b + (v.nach !== Kt.b ? ', 1 ' + v.nach + ' = ' + zahl(un[2]) + ' ' + Kt.b : ''));
      schritte.push(zahl(v.w) + ' ' + v.von + ' · ' + zahl(uv[2]) + (un[2] !== 1 ? ' / ' + zahl(un[2]) : '') + ' = ' + zahl(e) + ' ' + v.nach);
      schritte.push('Faktor: 1 ' + v.von + ' = ' + zahl(uv[2] / un[2]) + ' ' + v.nach);
    }
    Kt.e.forEach(function (u) { var x = umrechnen(k, v.von, u[0], v.w); zeilen.push([u[1], zahl(x, 8) + ' ' + u[0]]); items.push({ l: esc(u[0]), v: x, txt: zahl(x, 6), hl: u[0] === v.nach || u[0] === v.von }); });
    var svg, basis = k === 'temperatur' || k === 'verbrauch' ? null : v.w * uv[2];
    if (k === 'temperatur') { var c = Kt.von('°C', Kt.zu(v.von, v.w)); svg = skala(c, [{ bis: 0, l: 'Frost', f: FARB[1] }, { bis: 20, l: 'kühl', f: FARB[6] }, { bis: 37, l: 'warm', f: FARB[0] }, { bis: 100, l: 'heiß', f: FARB[2] }, { bis: 200, l: 'Backofen', f: FARB[4] }], -40, 200, { titel: 'Temperatur', txt: zahl(c, 4) + ' °C' }); }
    else if (k === 'verbrauch' || !VERGLEICH[k] || !(v.w * uv[2] > 0)) svg = '';
    else {
      var bw = v.w * uv[2], refs = VERGLEICH[k].map(function (r) { return { r: r, d: Math.abs(Math.log10(r[1] / bw)) }; }).sort(function (a, b) { return a.d - b.d; }).slice(0, 4);
      var bi = refs.map(function (x) { return { l: esc(x.r[0]), v: x.r[1], txt: zahl(x.r[1] / un[2], 3) + ' ' + esc(v.nach) }; });
      bi.push({ l: 'Ihr Wert', v: bw, txt: zahl(e, 4) + ' ' + esc(v.nach), hl: true, f: 'var(--accent)' });
      bi.sort(function (a, b) { return a.v - b.v; });
      svg = '<h4 class="rz-zt">Größenvergleich</h4>' + balken(bi, { log: true, titel: 'Größenvergleich mit Alltagsdingen' });
    }
    var verg = '';
    if (basis && VERGLEICH[k]) {
      var best = VERGLEICH[k].map(function (r) { return { r: r, q: basis / r[1] }; }).filter(function (x) { return x.q >= 0.05 && x.q <= 5000; }).sort(function (a, b) { return Math.abs(Math.log10(a.q) - 0.3) - Math.abs(Math.log10(b.q) - 0.3); }).slice(0, 2);
      if (best.length) verg = 'Zum Vergleich: ' + best.map(function (x) { return '≈ ' + zahl(x.q, 3) + ' × ' + x.r[0]; }).join(' · ');
    }
    return { wert: e, gross: zahl(e, 10), einh: v.nach, label: zahl(v.w) + ' ' + uv[1], zeilen: zeilen, schritte: schritte, svg: svg, hinweis: verg + (k === 'masse' && (v.von === 'lb' || v.nach === 'lb') ? (verg ? ' · ' : '') + 'Pfund = internationales Pfund (453,59237 g); das deutsche Pfund (500 g) heißt hier „Pfd“.' : '') + (k === 'volumen' && (v.von === 'Tasse' || v.nach === 'Tasse') ? (verg ? ' · ' : '') + 'Tasse = 250 ml (Richtmaß); eine US-Cup hat 236,6 ml.' : ''), zeilenTitel: 'Alle Einheiten' };
  } });
K({ id: 'kueche', b: 'kueche', t: 'Küche: Volumen ↔ Gewicht', u: 'Richtwerte für Zutaten (lose eingefüllt)',
  f: [W('z', 'Zutat', ZUTATEN.map(function (z) { return [z[0], z[1]]; }), 'mehl'), F('w', 'Menge', '', 1), W('von', 'Einheit', KUECHE_E.map(function (e) { return [e[0], e[1]]; }), 'Tasse')],
  r: function (v) { brauche(v, 'w'); var z = zutat(v.z), e = kuecheE(v.von) || KUECHE_E[4], ml, g;
    if (e[2] === 'v') { ml = v.w * e[3]; g = ml * z[2]; } else { g = v.w * e[3]; ml = g / z[2]; }
    var zeilen = KUECHE_E.map(function (x) { return [esc(x[1]), esc(zahl(x[2] === 'v' ? ml / x[3] : g / x[3], 3) + ' ' + x[0])]; });
    return { wert: e[2] === 'v' ? g : ml, gross: zahl(e[2] === 'v' ? g : ml, 3), einh: e[2] === 'v' ? 'g' : 'ml', label: zahl(v.w) + ' ' + e[1] + ' ' + z[1], zeilen: zeilen,
      schritte: ['Dichte (Richtwert) ' + z[1] + ': ' + zahl(z[2]) + ' g/ml', e[2] === 'v' ? 'Masse = Volumen · Dichte = ' + zahl(ml) + ' ml · ' + zahl(z[2]) + ' = ' + zahl(g, 4) + ' g' : 'Volumen = Masse / Dichte = ' + zahl(g) + ' g / ' + zahl(z[2]) + ' = ' + zahl(ml, 4) + ' ml'],
      hinweis: 'Richtwerte – je nach Sorte, Feuchte und Einfüllart (gesiebt, festgedrückt) bis ±15 % Abweichung. Zum genauen Backen wiegen.' }; } });

/* ---------- Währungen ---------- */
var W_OPT = WAEHRUNGEN.map(function (w) { return [w[0], w[0] + ' – ' + w[1]]; });
K({ id: 'waehrung', b: 'waehrung', t: 'Währungsrechner', u: 'Referenzkurse, EUR-Basis', breit: true, f: [F('w', 'Betrag', '', 100), W('von', 'Von', W_OPT, 'EUR'), W('nach', 'Nach', W_OPT, 'USD', { tausch: 'von' })],
  r: function (v, ctx) { brauche(v, 'w'); var ku = (ctx && ctx.kurse) || richtKurse(), a = ku[v.von], b = ku[v.nach];
    if (!a || !b) throw new Error('Für diese Währung ist kein Kurs hinterlegt.');
    var e = v.w / a * b, zeilen = [], stand = (ctx && ctx.kursInfo) || 'Richtwert Stand ' + KURS_STAND + ', kein Live-Kurs';
    ['EUR', 'USD', 'GBP', 'CHF', 'JPY', 'CNY', 'PLN', 'CZK', 'SEK', 'DKK', 'TRY', 'CAD'].forEach(function (c) { if (c !== v.von && ku[c]) zeilen.push([c + ' – ' + waehrungName(c), fix(v.w / a * ku[c], ku[c] / a * v.w >= 1000 ? 0 : 2) + ' ' + c]); });
    return { wert: e, gross: fix(e, 2), einh: v.nach, label: fix(v.w, 2) + ' ' + v.von + ' (' + waehrungName(v.von) + ')',
      zeilen: [['Kurs', '1 ' + v.von + ' = ' + zahl(b / a, 6) + ' ' + v.nach], ['Gegenkurs', '1 ' + v.nach + ' = ' + zahl(a / b, 6) + ' ' + v.von]].concat(zeilen),
      schritte: ['Kurse je 1 EUR: ' + v.von + ' = ' + zahl(a) + ', ' + v.nach + ' = ' + zahl(b), 'Betrag in EUR: ' + zahl(v.w) + ' / ' + zahl(a) + ' = ' + zahl(v.w / a), 'Betrag in ' + v.nach + ': ' + zahl(v.w / a) + ' · ' + zahl(b) + ' = ' + fix(e, 2)],
      hinweis: stand + '. Banken und Wechselstuben rechnen mit Aufschlägen.' }; } });

/* ---------- Physik & Technik ---------- */
K({ id: 'ohm', b: 'physik', t: 'Ohmsches Gesetz & Leistung', u: 'zwei beliebige Werte eingeben', f: [F('U', 'Spannung U', 'V', 230), F('I', 'Stromstärke I', 'A', null), F('R', 'Widerstand R', 'Ω', null), F('P', 'Leistung P', 'W', 2300)],
  r: function (v) {
    var g = ['U', 'I', 'R', 'P'].filter(function (k) { return v[k] != null && !isNaN(v[k]); });
    if (g.length < 2) throw new LeerFehler('Zwei der vier Werte eingeben.');
    var a = g[0], b = g[1], U = v.U, I = v.I, R = v.R, P = v.P, s = [];
    var k = a + b;
    if (k === 'UI') { R = U / I; P = U * I; s = ['R = U / I = ' + zahl(U) + ' / ' + zahl(I) + ' = ' + zahl(R) + ' Ω', 'P = U · I = ' + zahl(U) + ' · ' + zahl(I) + ' = ' + zahl(P) + ' W']; }
    else if (k === 'UR') { I = U / R; P = U * U / R; s = ['I = U / R = ' + zahl(U) + ' / ' + zahl(R) + ' = ' + zahl(I) + ' A', 'P = U² / R = ' + zahl(P) + ' W']; }
    else if (k === 'UP') { I = P / U; R = U * U / P; s = ['I = P / U = ' + zahl(P) + ' / ' + zahl(U) + ' = ' + zahl(I) + ' A', 'R = U² / P = ' + zahl(R) + ' Ω']; }
    else if (k === 'IR') { U = I * R; P = I * I * R; s = ['U = R · I = ' + zahl(R) + ' · ' + zahl(I) + ' = ' + zahl(U) + ' V', 'P = I² · R = ' + zahl(P) + ' W']; }
    else if (k === 'IP') { U = P / I; R = P / (I * I); s = ['U = P / I = ' + zahl(U) + ' V', 'R = P / I² = ' + zahl(R) + ' Ω']; }
    else { I = Math.sqrt(P / R); U = Math.sqrt(P * R); s = ['I = √(P / R) = ' + zahl(I) + ' A', 'U = √(P · R) = ' + zahl(U) + ' V']; }
    if (!isFinite(U + I + R + P)) throw new Error('Mit diesen Werten ist keine Lösung möglich (Division durch 0).');
    if (g.length > 2) s.unshift('Mehr als zwei Werte eingegeben – gerechnet wird mit ' + a + ' und ' + b + '.');
    var fehlt = ['U', 'I', 'R', 'P'].filter(function (x) { return x !== a && x !== b; }), main = fehlt[0], mv = { U: U, I: I, R: R, P: P }, me = { U: 'V', I: 'A', R: 'Ω', P: 'W' };
    return { wert: mv[main], gross: zahl(mv[main], 6), einh: me[main], label: { U: 'Spannung', I: 'Stromstärke', R: 'Widerstand', P: 'Leistung' }[main],
      zeilen: [['Spannung U', zahl(U, 6) + ' V'], ['Stromstärke I', zahl(I, 6) + ' A'], ['Widerstand R', zahl(R, 6) + ' Ω'], ['Leistung P', zahl(P, 6) + ' W = ' + zahl(P / 1000, 6) + ' kW']],
      schritte: ['Grundformeln: U = R · I und P = U · I'].concat(s), hinweis: I > 16 && U <= 250 ? 'Hinweis: Haushaltsstromkreise sind meist mit 16 A abgesichert.' : '' }; } });
K({ id: 'stromkosten', b: 'physik', t: 'Stromkosten', u: 'Energie = Leistung · Zeit', f: [F('P', 'Leistung', 'W', 2000), F('h', 'Dauer je Tag', 'h', 3), F('tage', 'Anzahl Tage', 'Tage', 1), F('preis', 'Strompreis', '€/kWh', 0.35)],
  r: function (v) { brauche(v, 'P', 'h', 'preis'); var tage = v.tage == null ? 1 : v.tage, kwh = v.P / 1000 * v.h * tage, k = kwh * v.preis, jahr = v.P / 1000 * v.h * 365 * v.preis;
    return { wert: k, gross: fix(k, 2), einh: '€', label: zahl(kwh, 6) + ' kWh in ' + zahl(tage) + (tage === 1 ? ' Tag' : ' Tagen'), zeilen: [['Energie', zahl(kwh, 6) + ' kWh'], ['Kosten pro Tag', geld(v.P / 1000 * v.h * v.preis)], ['Hochgerechnet auf ein Jahr', geld(jahr)]],
      schritte: ['E = P · t = ' + zahl(v.P / 1000) + ' kW · ' + zahl(v.h) + ' h · ' + zahl(tage) + ' = ' + zahl(kwh, 6) + ' kWh', 'Kosten = E · Preis = ' + zahl(kwh, 6) + ' kWh · ' + fix(v.preis, 2) + ' €/kWh = ' + fix(k, 2) + ' €'],
      svg: balken([{ l: 'Tag', v: v.P / 1000 * v.h * v.preis, txt: geld(v.P / 1000 * v.h * v.preis) }, { l: 'Monat', v: v.P / 1000 * v.h * 30.44 * v.preis, txt: geld(v.P / 1000 * v.h * 30.44 * v.preis) }, { l: 'Jahr', v: jahr, txt: geld(jahr) }], { log: true }) }; } });
K({ id: 'vst', b: 'physik', t: 'Geschwindigkeit – Weg – Zeit', u: 'zwei Werte eingeben', f: [F('v', 'Geschwindigkeit', 'km/h', 80), F('s', 'Weg', 'km', 120), F('t', 'Zeit', 'h', null)],
  r: function (v) { var g = ['v', 's', 't'].filter(function (k) { return v[k] != null && !isNaN(v[k]); }); if (g.length < 2) throw new LeerFehler('Zwei der drei Werte eingeben.');
    var V = v.v, S = v.s, Tt = v.t, s;
    if (g.indexOf('v') >= 0 && g.indexOf('s') >= 0) { if (!V) throw new Error('v darf nicht 0 sein.'); Tt = S / V; s = 't = s / v = ' + zahl(S) + ' km / ' + zahl(V) + ' km/h = ' + zahl(Tt) + ' h'; }
    else if (g.indexOf('v') >= 0) { S = V * Tt; s = 's = v · t = ' + zahl(V) + ' · ' + zahl(Tt) + ' = ' + zahl(S) + ' km'; }
    else { if (!Tt) throw new Error('t darf nicht 0 sein.'); V = S / Tt; s = 'v = s / t = ' + zahl(S) + ' / ' + zahl(Tt) + ' = ' + zahl(V) + ' km/h'; }
    var main = ['v', 's', 't'].filter(function (k) { return g.indexOf(k) < 0 || g.indexOf(k) > 1; })[0] || 't';
    return { wert: { v: V, s: S, t: Tt }[main], gross: main === 't' ? dauerText(Tt * 3600) : zahl({ v: V, s: S }[main], 6), einh: { v: 'km/h', s: 'km', t: Tt >= 1 ? 'h:mm:ss' : 'min:ss' }[main], label: { v: 'Geschwindigkeit', s: 'Weg', t: 'Fahrzeit' }[main],
      zeilen: [['Geschwindigkeit', zahl(V, 6) + ' km/h = ' + zahl(V / 3.6, 6) + ' m/s'], ['Weg', zahl(S, 6) + ' km'], ['Zeit', zahl(Tt, 6) + ' h = ' + zahl(Tt * 60, 6) + ' min']], schritte: ['Formel: s = v · t', s] }; } });
K({ id: 'mechanik', b: 'physik', t: 'Kraft, Arbeit, Energie', u: 'F = m·a · W = F·s · Ekin · Epot', f: [F('m', 'Masse m', 'kg', 75), F('a', 'Beschleunigung a', 'm/s²', 9.81), F('s', 'Weg s', 'm', 10), F('vv', 'Geschwindigkeit v', 'm/s', 5), F('hh', 'Höhe h', 'm', 3)],
  r: function (v) { brauche(v, 'm'); var z = [], s = [], Fk = null, roh = [];
    if (v.a != null) { Fk = v.m * v.a; z.push(['Kraft F = m · a', zahl(Fk, 6) + ' N']); roh.push([Fk, 'N']); s.push('F = ' + zahl(v.m) + ' kg · ' + zahl(v.a) + ' m/s² = ' + zahl(Fk, 6) + ' N'); }
    if (Fk != null && v.s != null) { z.push(['Arbeit W = F · s', zahl(Fk * v.s, 6) + ' J']); roh.push([Fk * v.s, 'J']); s.push('W = ' + zahl(Fk, 6) + ' N · ' + zahl(v.s) + ' m = ' + zahl(Fk * v.s, 6) + ' J'); }
    if (v.vv != null) { var ek = 0.5 * v.m * v.vv * v.vv; z.push(['Bewegungsenergie Ekin = ½ m v²', zahl(ek, 6) + ' J']); roh.push([ek, 'J']); s.push('Ekin = 0,5 · ' + zahl(v.m) + ' · ' + zahl(v.vv) + '² = ' + zahl(ek, 6) + ' J'); }
    if (v.hh != null) { var ep = v.m * 9.80665 * v.hh; z.push(['Lageenergie Epot = m g h', zahl(ep, 6) + ' J']); roh.push([ep, 'J']); s.push('Epot = ' + zahl(v.m) + ' · 9,80665 · ' + zahl(v.hh) + ' = ' + zahl(ep, 6) + ' J'); }
    if (!z.length) throw new LeerFehler('Masse und mindestens einen weiteren Wert eingeben.');
    return { wert: roh[0][0], gross: zahl(roh[0][0], 6), einh: roh[0][1], label: z[0][0].split(' =')[0], zeilen: z, schritte: s, hinweis: 'Gewichtskraft auf der Erde: F = m · 9,80665 m/s² (Normfallbeschleunigung).' }; } });
K({ id: 'druck', b: 'physik', t: 'Druck', u: 'p = F / A', f: [F('F', 'Kraft F', 'N', 1000), F('A', 'Fläche A', 'm²', 0.5), F('p', 'Druck p', 'Pa', null)],
  r: function (v) { var g = ['F', 'A', 'p'].filter(function (k) { return v[k] != null; }); if (g.length < 2) throw new LeerFehler('Zwei der drei Werte eingeben.');
    var Fv = v.F, A = v.A, p = v.p, s, main;
    if (Fv != null && A != null) { if (!A) throw new Error('A darf nicht 0 sein.'); p = Fv / A; main = 'p'; s = 'p = F / A = ' + zahl(Fv) + ' / ' + zahl(A) + ' = ' + zahl(p) + ' Pa'; }
    else if (Fv != null) { A = Fv / p; main = 'A'; s = 'A = F / p = ' + zahl(A) + ' m²'; } else { Fv = p * A; main = 'F'; s = 'F = p · A = ' + zahl(Fv) + ' N'; }
    var mv = { F: Fv, A: A, p: p };
    return { wert: mv[main], gross: zahl(mv[main], 6), einh: { F: 'N', A: 'm²', p: 'Pa' }[main], label: { F: 'Kraft', A: 'Fläche', p: 'Druck' }[main], zeilen: [['Druck', zahl(p, 6) + ' Pa = ' + zahl(p / 1e5, 6) + ' bar = ' + zahl(p / 100, 6) + ' hPa'], ['Kraft', zahl(Fv, 6) + ' N'], ['Fläche', zahl(A, 6) + ' m²']], schritte: ['Formel: p = F / A', s] }; } });
K({ id: 'dichte', b: 'physik', t: 'Dichte', u: 'ρ = m / V', f: [F('m', 'Masse m', 'kg', 7.85), F('V', 'Volumen V', 'l', 1), F('rho', 'Dichte ρ', 'kg/l', null)],
  r: function (v) { var g = ['m', 'V', 'rho'].filter(function (k) { return v[k] != null; }); if (g.length < 2) throw new LeerFehler('Zwei der drei Werte eingeben.');
    var m = v.m, V = v.V, r = v.rho, s, main;
    if (m != null && V != null) { if (!V) throw new Error('V darf nicht 0 sein.'); r = m / V; main = 'rho'; s = 'ρ = m / V = ' + zahl(m) + ' / ' + zahl(V) + ' = ' + zahl(r) + ' kg/l'; }
    else if (m != null) { V = m / r; main = 'V'; s = 'V = m / ρ = ' + zahl(V) + ' l'; } else { m = r * V; main = 'm'; s = 'm = ρ · V = ' + zahl(m) + ' kg'; }
    var ref = [['Holz (Fichte)', 0.47], ['Wasser', 1], ['Beton', 2.4], ['Aluminium', 2.7], ['Stahl', 7.85], ['Blei', 11.34], ['Gold', 19.32]];
    return { wert: { m: m, V: V, rho: r }[main], gross: zahl({ m: m, V: V, rho: r }[main], 6), einh: { m: 'kg', V: 'l', rho: 'kg/l' }[main], label: { m: 'Masse', V: 'Volumen', rho: 'Dichte' }[main],
      zeilen: [['Dichte', zahl(r, 6) + ' kg/l = ' + zahl(r * 1000, 6) + ' kg/m³ = ' + zahl(r, 6) + ' g/cm³']], schritte: ['Formel: ρ = m / V (1 kg/l = 1 g/cm³ = 1000 kg/m³)', s],
      svg: balken(ref.map(function (x) { return { l: x[0], v: x[1], txt: zahl(x[1]) }; }).concat([{ l: 'Ihr Wert', v: r, txt: zahl(r, 4), hl: true }]).sort(function (a, b) { return a.v - b.v; }), { titel: 'Dichtevergleich' }) }; } });
K({ id: 'fall', b: 'physik', t: 'Freier Fall', u: 'ohne Luftwiderstand', f: [F('h', 'Fallhöhe h', 'm', 20), F('t', 'oder Fallzeit t', 's', null)],
  r: function (v) { var g = 9.80665, h = v.h, t = v.t, s;
    if (h != null) { if (h < 0) throw new Error('Höhe muss positiv sein.'); t = Math.sqrt(2 * h / g); s = 't = √(2h / g) = √(2 · ' + zahl(h) + ' / 9,80665) = ' + zahl(t, 6) + ' s'; }
    else if (t != null) { h = 0.5 * g * t * t; s = 'h = ½ g t² = ' + zahl(h, 6) + ' m'; } else throw new LeerFehler();
    var vend = g * t;
    return { wert: v.h != null ? t : h, gross: zahl(v.h != null ? t : h, 4), einh: v.h != null ? 's' : 'm', label: v.h != null ? 'Fallzeit' : 'Fallhöhe', zeilen: [['Fallzeit', zahl(t, 4) + ' s'], ['Höhe', zahl(h, 6) + ' m'], ['Aufprallgeschwindigkeit', zahl(vend, 4) + ' m/s = ' + zahl(vend * 3.6, 4) + ' km/h']],
      schritte: ['g = 9,80665 m/s²', s, 'v = g · t = ' + zahl(vend, 6) + ' m/s'], hinweis: 'Ohne Luftwiderstand – reale Körper fallen langsamer.' }; } });
var STOFF_C = [['wasser', 'Wasser', 4186], ['oel', 'Speiseöl', 1970], ['alu', 'Aluminium', 897], ['eisen', 'Eisen/Stahl', 450], ['kupfer', 'Kupfer', 385], ['luft', 'Luft', 1005], ['beton', 'Beton', 880]];
K({ id: 'waerme', b: 'physik', t: 'Wärmemenge (z. B. Wasser erwärmen)', u: 'Q = m · c · ΔT', f: [W('st', 'Stoff', STOFF_C.map(function (x) { return [x[0], x[1] + ' (c = ' + x[2] + ' J/(kg·K))']; }), 'wasser'), F('m', 'Masse', 'kg', 1.5), F('t1', 'Anfangstemperatur', '°C', 15), F('t2', 'Endtemperatur', '°C', 100), F('P', 'Heizleistung (optional)', 'W', 2000)],
  r: function (v) { brauche(v, 'm', 't1', 't2'); var c = STOFF_C.filter(function (x) { return x[0] === v.st; })[0] || STOFF_C[0], dT = v.t2 - v.t1, Q = v.m * c[2] * dT, z = [['in Kilojoule', zahl(Q / 1000, 6) + ' kJ'], ['in Kilowattstunden', zahl(Q / 3.6e6, 4) + ' kWh'], ['in Kilokalorien', zahl(Q / 4184, 5) + ' kcal']];
    if (v.P) z.push(['Dauer bei ' + zahl(v.P) + ' W (verlustfrei)', dauerText(Math.abs(Q) / v.P) + ' (min:s)']);
    return { wert: Q, gross: zahl(Q / 1000, 5), einh: 'kJ', label: 'Wärme für ' + zahl(v.m) + ' kg ' + c[1] + ', ΔT = ' + zahl(dT) + ' K', zeilen: z,
      schritte: ['Q = m · c · ΔT', 'Q = ' + zahl(v.m) + ' kg · ' + c[2] + ' J/(kg·K) · ' + zahl(dT) + ' K = ' + zahl(Q, 6) + ' J', 'Zeit t = Q / P'], hinweis: 'Ohne Wärmeverluste und ohne Verdampfen; reale Wasserkocher brauchen etwa 10–20 % länger.' }; } });
K({ id: 'gas', b: 'physik', t: 'Ideales Gas', u: 'p · V = n · R · T – drei Werte eingeben', f: [F('p', 'Druck p', 'hPa', 1013.25), F('V', 'Volumen V', 'l', null), F('n', 'Stoffmenge n', 'mol', 1), F('T', 'Temperatur', '°C', 0)],
  r: function (v) { var R = 8.314462618, g = ['p', 'V', 'n', 'T'].filter(function (k) { return v[k] != null; }); if (g.length < 3) throw new LeerFehler('Drei der vier Werte eingeben.');
    var p = v.p != null ? v.p * 100 : null, V = v.V != null ? v.V / 1000 : null, n = v.n, T = v.T != null ? v.T + 273.15 : null, main, s;
    if (T != null && T <= 0) throw new Error('Die Temperatur muss über dem absoluten Nullpunkt liegen.');
    if (V == null) { V = n * R * T / p; main = 'V'; s = 'V = n R T / p = ' + zahl(n) + ' · 8,314 · ' + zahl(T) + ' / ' + zahl(p) + ' = ' + zahl(V * 1000, 6) + ' l'; }
    else if (p == null) { p = n * R * T / V; main = 'p'; s = 'p = n R T / V = ' + zahl(p / 100, 6) + ' hPa'; }
    else if (n == null) { n = p * V / (R * T); main = 'n'; s = 'n = p V / (R T) = ' + zahl(n, 6) + ' mol'; }
    else { T = p * V / (n * R); main = 'T'; s = 'T = p V / (n R) = ' + zahl(T, 6) + ' K'; }
    var mv = { p: p / 100, V: V * 1000, n: n, T: T - 273.15 };
    return { wert: mv[main], gross: zahl(mv[main], 6), einh: { p: 'hPa', V: 'l', n: 'mol', T: '°C' }[main], label: { p: 'Druck', V: 'Volumen', n: 'Stoffmenge', T: 'Temperatur' }[main],
      zeilen: [['Druck', zahl(p / 100, 6) + ' hPa'], ['Volumen', zahl(V * 1000, 6) + ' l'], ['Stoffmenge', zahl(n, 6) + ' mol'], ['Temperatur', zahl(T, 6) + ' K = ' + zahl(T - 273.15, 6) + ' °C'], ['Molvolumen', zahl(V * 1000 / n, 6) + ' l/mol']],
      schritte: ['R = 8,314462618 J/(mol·K); Einheiten in SI umrechnen (Pa, m³, K)', s], hinweis: 'Bei 0 °C und 1013,25 hPa nimmt 1 mol eines idealen Gases 22,414 l ein, bei 25 °C 24,465 l.' }; } });

/* ---------- Geometrie ---------- */
var FORMEN = [['rechteck', 'Rechteck'], ['dreieck', 'Dreieck'], ['kreis', 'Kreis'], ['trapez', 'Trapez'], ['quader', 'Quader'], ['zylinder', 'Zylinder'], ['kugel', 'Kugel'], ['kegel', 'Kegel']];
var FORM_F = { rechteck: ['a', 'b'], dreieck: ['a', 'b', 'c'], kreis: ['r'], trapez: ['a', 'c', 'h'], quader: ['a', 'b', 'c'], zylinder: ['r', 'h'], kugel: ['r'], kegel: ['r', 'h'] };
function skizze(form, v, ein) {
  var L = function (k) { return v[k] != null ? k + ' = ' + zahl(v[k], 4) + (ein ? ' ' + ein : '') : k; }, s = '<svg class="rz-skizze" viewBox="0 0 240 150" role="img" aria-label="Skizze ' + form + '">', st = 'class="rz-sk"';
  switch (form) {
    case 'rechteck': s += '<rect ' + st + ' x="30" y="25" width="150" height="90"/><text x="105" y="135" text-anchor="middle">' + L('a') + '</text><text x="188" y="74">' + L('b') + '</text><line class="rz-sk2" x1="30" y1="115" x2="180" y2="25"/>'; break;
    case 'pyth': s += '<path ' + st + ' d="M30 120 L180 120 L180 30 Z"/><path class="rz-sk2" d="M166 120 L166 106 L180 106"/><text x="105" y="140" text-anchor="middle">' + L('b') + '</text><text x="188" y="80">' + L('a') + '</text><text x="96" y="66" text-anchor="end">' + L('c') + '</text>'; break;
    case 'dreieck': s += '<path ' + st + ' d="M30 120 L210 120 L150 25 Z"/><text x="120" y="140" text-anchor="middle">' + L('c') + '</text><text x="190" y="72">' + L('a') + '</text><text x="40" y="72">' + L('b') + '</text>'; break;
    case 'kreis': s += '<circle ' + st + ' cx="120" cy="72" r="56"/><line class="rz-sk2" x1="120" y1="72" x2="176" y2="72"/><circle cx="120" cy="72" r="2.5" class="rz-skp"/><text x="148" y="66" text-anchor="middle">' + L('r') + '</text>'; break;
    case 'trapez': s += '<path ' + st + ' d="M25 120 L215 120 L170 30 L70 30 Z"/><line class="rz-sk2" x1="70" y1="30" x2="70" y2="120"/><text x="120" y="140" text-anchor="middle">' + L('a') + '</text><text x="120" y="22" text-anchor="middle">' + L('c') + '</text><text x="76" y="80">' + L('h') + '</text>'; break;
    case 'quader': s += '<path ' + st + ' d="M40 50 L160 50 L160 125 L40 125 Z M40 50 L80 22 L200 22 L160 50 M200 22 L200 97 L160 125"/><path class="rz-sk2" d="M40 125 L80 97 L200 97 M80 97 L80 22"/><text x="100" y="142" text-anchor="middle">' + L('a') + '</text><text x="188" y="122">' + L('b') + '</text><text x="4" y="92">' + L('c') + '</text>'; break;
    case 'zylinder': s += '<ellipse ' + st + ' cx="120" cy="30" rx="60" ry="14"/><path ' + st + ' d="M60 30 L60 115 A60 14 0 0 0 180 115 L180 30"/><path class="rz-sk2" d="M60 115 A60 14 0 0 1 180 115 M120 30 L180 30"/><text x="150" y="25" text-anchor="middle">' + L('r') + '</text><text x="186" y="78">' + L('h') + '</text>'; break;
    case 'kugel': s += '<circle ' + st + ' cx="120" cy="72" r="58"/><ellipse class="rz-sk2" cx="120" cy="72" rx="58" ry="16"/><line class="rz-sk2" x1="120" y1="72" x2="178" y2="72"/><text x="149" y="66" text-anchor="middle">' + L('r') + '</text>'; break;
    case 'kegel': s += '<path ' + st + ' d="M120 18 L60 120 A60 14 0 0 0 180 120 Z"/><path class="rz-sk2" d="M60 120 A60 14 0 0 1 180 120 M120 18 L120 120 L180 120"/><text x="150" y="114" text-anchor="middle">' + L('r') + '</text><text x="126" y="80">' + L('h') + '</text>'; break;
  }
  return s + '</svg>';
}
K({ id: 'formen', b: 'geometrie', t: 'Flächen & Körper', u: 'Fläche, Umfang, Volumen, Oberfläche', breit: true,
  f: [W('form', 'Form', FORMEN, 'rechteck', { segment: true }), F('a', 'a', '', 4, { nur: { form: ['rechteck', 'dreieck', 'trapez', 'quader'] } }), F('b', 'b', '', 3, { nur: { form: ['rechteck', 'dreieck', 'quader'] } }),
    F('c', 'c', '', 5, { nur: { form: ['dreieck', 'trapez', 'quader'] } }), F('r', 'Radius r', '', 3, { nur: { form: ['kreis', 'zylinder', 'kugel', 'kegel'] } }), F('h', 'Höhe h', '', 5, { nur: { form: ['trapez', 'zylinder', 'kegel'] } }),
    T('ein', 'Längeneinheit', 'm', { kurz: true })],
  r: function (v) {
    var f = v.form || 'rechteck', need = FORM_F[f], P = Math.PI, z = [], s = [], main = null, e = String(v.ein || '').trim().slice(0, 6), e2 = e ? ' ' + e + '²' : '', e3 = e ? ' ' + e + '³' : '', e1 = e ? ' ' + e : '';
    need.forEach(function (k) { brauche(v, k); if (!(v[k] > 0)) throw new Error(k + ' muss größer als 0 sein.'); });
    var a = v.a, b = v.b, c = v.c, r = v.r, h = v.h, A, U, V, O;
    var roh = [];
    function add(l, val, ei, form) { z.push([l, zahl(val, 8) + ei]); roh.push(val); if (form) s.push(l + ': ' + form + ' = ' + zahl(val, 8) + ei); }
    if (f === 'rechteck') { A = a * b; U = 2 * (a + b); add('Fläche A', A, e2, 'a · b = ' + zahl(a) + ' · ' + zahl(b)); add('Umfang U', U, e1, '2 · (a + b)'); add('Diagonale d', Math.hypot(a, b), e1, '√(a² + b²)'); main = 'A'; }
    if (f === 'dreieck') { if (a + b <= c || a + c <= b || b + c <= a) throw new Error('Mit diesen Seiten gibt es kein Dreieck (Dreiecksungleichung).'); var sh = (a + b + c) / 2; A = Math.sqrt(sh * (sh - a) * (sh - b) * (sh - c)); U = a + b + c;
      add('Fläche A', A, e2, 'Heron: √(s(s−a)(s−b)(s−c)), s = ' + zahl(sh)); add('Umfang U', U, e1, 'a + b + c'); add('Höhe auf c', 2 * A / c, e1, '2A / c');
      if (Math.abs(a * a + b * b - c * c) < 1e-9 * c * c) z.push(['Besonderheit', 'rechtwinklig (a² + b² = c²)']); main = 'A'; }
    if (f === 'kreis') { A = P * r * r; U = 2 * P * r; add('Fläche A', A, e2, 'π · r² = π · ' + zahl(r) + '²'); add('Umfang U', U, e1, '2 · π · r'); add('Durchmesser d', 2 * r, e1); main = 'A'; }
    if (f === 'trapez') { A = (a + c) / 2 * h; add('Fläche A', A, e2, '(a + c) / 2 · h = (' + zahl(a) + ' + ' + zahl(c) + ') / 2 · ' + zahl(h)); add('Mittellinie m', (a + c) / 2, e1, '(a + c) / 2'); main = 'A'; }
    if (f === 'quader') { V = a * b * c; O = 2 * (a * b + a * c + b * c); add('Volumen V', V, e3, 'a · b · c'); add('Oberfläche O', O, e2, '2(ab + ac + bc)'); add('Raumdiagonale', Math.sqrt(a * a + b * b + c * c), e1, '√(a² + b² + c²)'); main = 'V'; }
    if (f === 'zylinder') { V = P * r * r * h; O = 2 * P * r * (r + h); add('Volumen V', V, e3, 'π · r² · h'); add('Oberfläche O', O, e2, '2πr(r + h)'); add('Mantelfläche M', 2 * P * r * h, e2, '2πrh'); main = 'V'; }
    if (f === 'kugel') { V = 4 / 3 * P * r * r * r; O = 4 * P * r * r; add('Volumen V', V, e3, '4/3 · π · r³'); add('Oberfläche O', O, e2, '4 · π · r²'); main = 'V'; }
    if (f === 'kegel') { var sl = Math.hypot(r, h); V = P * r * r * h / 3; O = P * r * (r + sl); add('Volumen V', V, e3, '⅓ · π · r² · h'); add('Mantellinie s', sl, e1, '√(r² + h²)'); add('Oberfläche O', O, e2, 'πr(r + s)'); main = 'V'; }
    if (e === 'm' && V != null) z.push(['Volumen in Litern', zahl(V * 1000, 8) + ' l']);
    var fi = 0; if (v._fokus) z.forEach(function (x, i) { if (fi === 0 && x[0].indexOf(v._fokus) === 0) fi = i; });
    var hz = z[fi], tz = hz[1].split(' ');
    return { wert: roh[fi], gross: zahl(roh[fi], 8), einh: tz.slice(1).join(' ').replace(/^× 10\S*\s*/, ''), label: hz[0] + ' · ' + FORMEN.filter(function (x) { return x[0] === f; })[0][1], zeilen: z, schritte: s, svg: skizze(f, v, e) };
  } });
K({ id: 'pyth', b: 'geometrie', t: 'Rechtwinkliges Dreieck', u: 'Pythagoras: a² + b² = c² – zwei Seiten eingeben', f: [F('a', 'Kathete a', '', 3), F('b', 'Kathete b', '', 4), F('c', 'Hypotenuse c', '', null)],
  r: function (v) { var g = ['a', 'b', 'c'].filter(function (k) { return v[k] != null; }); if (g.length < 2) throw new LeerFehler('Zwei Seiten eingeben.');
    var a = v.a, b = v.b, c = v.c, s, m;
    if (a != null && b != null) { c = Math.hypot(a, b); m = 'c'; s = 'c = √(a² + b²) = √(' + zahl(a * a) + ' + ' + zahl(b * b) + ') = ' + zahl(c, 8); }
    else { if (c <= (a != null ? a : b)) throw new Error('Die Hypotenuse muss die längste Seite sein.'); if (a == null) { a = Math.sqrt(c * c - b * b); m = 'a'; } else { b = Math.sqrt(c * c - a * a); m = 'b'; } s = m + ' = √(c² − ' + (m === 'a' ? 'b' : 'a') + '²) = ' + zahl(m === 'a' ? a : b, 8); }
    var al = Math.atan2(a, b) * 180 / Math.PI;
    return { wert: { a: a, b: b, c: c }[m], gross: zahl({ a: a, b: b, c: c }[m], 8), label: 'Seite ' + m, zeilen: [['Winkel α (gegenüber a)', zahl(al, 6) + '°'], ['Winkel β (gegenüber b)', zahl(90 - al, 6) + '°'], ['Fläche', zahl(a * b / 2, 8)]], schritte: ['Satz des Pythagoras: a² + b² = c²', s], svg: skizze('pyth', { a: a, b: b, c: c }, '') }; } });
K({ id: 'wand', b: 'bau', t: 'Wandfläche & Farbe', u: 'Streichen: Fläche, Liter, Eimer', f: [F('u', 'Raumumfang (Summe der Wände)', 'm', 16), F('h', 'Raumhöhe', 'm', 2.5), F('ab', 'Abzug Fenster/Türen', 'm²', 4), F('decke', 'Deckenfläche (optional)', 'm²', 0), F('n', 'Anstriche', '', 2), F('erg', 'Ergiebigkeit', 'm²/l', 7), F('eimer', 'Eimergröße', 'l', 10)],
  r: function (v) { brauche(v, 'u', 'h', 'erg'); var Aw = Math.max(0, v.u * v.h - (v.ab || 0)) + (v.decke || 0), n = v.n || 1, l = Aw * n / v.erg, e = v.eimer ? Math.ceil(l / v.eimer) : null;
    return { wert: l, gross: zahl(l, 3), einh: 'l', label: 'Farbe für ' + zahl(Aw, 4) + ' m² · ' + n + ' Anstrich(e)', zeilen: [['Streichfläche', zahl(Aw, 6) + ' m²'], ['Farbbedarf', zahl(l, 4) + ' l']].concat(e ? [['Eimer à ' + zahl(v.eimer) + ' l', e + ' Stück']] : []),
      schritte: ['Fläche = Umfang · Höhe − Abzug + Decke = ' + zahl(v.u) + ' · ' + zahl(v.h) + ' − ' + zahl(v.ab || 0) + ' + ' + zahl(v.decke || 0) + ' = ' + zahl(Aw, 6) + ' m²', 'Liter = Fläche · Anstriche / Ergiebigkeit = ' + zahl(Aw, 6) + ' · ' + n + ' / ' + zahl(v.erg) + ' = ' + zahl(l, 4) + ' l'], hinweis: 'Ergiebigkeit steht auf dem Eimer (Dispersionsfarbe meist 6–8 m²/l). Etwa 10 % Reserve einplanen.' }; } });
K({ id: 'fliesen', b: 'bau', t: 'Fliesen & Bodenbelag', u: 'Anzahl inkl. Verschnitt', f: [F('l', 'Raumlänge', 'm', 4), F('b', 'Raumbreite', 'm', 3), F('fl', 'Fliese Länge', 'cm', 60), F('fb', 'Fliese Breite', 'cm', 30), F('vs', 'Verschnitt', '%', 10), F('pk', 'm² pro Paket (optional)', 'm²', 1.44)],
  r: function (v) { brauche(v, 'l', 'b', 'fl', 'fb'); var A = v.l * v.b, af = v.fl * v.fb / 1e4, vs = v.vs == null ? 10 : v.vs, Ag = A * (1 + vs / 100), n = Math.ceil(Ag / af - 1e-9);
    var z = [['Bodenfläche', zahl(A, 6) + ' m²'], ['mit Verschnitt', zahl(Ag, 6) + ' m²'], ['Fläche je Fliese', zahl(af, 6) + ' m²']]; if (v.pk) z.push(['Pakete à ' + zahl(v.pk) + ' m²', Math.ceil(Ag / v.pk - 1e-9) + ' Stück']);
    return { wert: n, gross: gz(n), einh: 'Fliesen', label: 'für ' + zahl(A, 4) + ' m² + ' + zahl(vs) + ' % Verschnitt', zeilen: z, schritte: ['Fläche = ' + zahl(v.l) + ' · ' + zahl(v.b) + ' = ' + zahl(A, 6) + ' m²', '+ Verschnitt: · ' + zahl(1 + vs / 100) + ' = ' + zahl(Ag, 6) + ' m²', 'Anzahl = ' + zahl(Ag, 6) + ' / ' + zahl(af, 6) + ' = ' + zahl(Ag / af, 6) + ' → aufgerundet ' + n], hinweis: 'Verschnitt: gerade verlegt ca. 5–10 %, diagonal 15 %.' }; } });
K({ id: 'beet', b: 'garten', t: 'Beet- & Erdvolumen', u: 'Hochbeet, Mulch, Kies', f: [F('l', 'Länge', 'm', 2), F('b', 'Breite', 'm', 1.2), F('h', 'Füllhöhe', 'cm', 30), F('sack', 'Sackgröße', 'l', 40)],
  r: function (v) { brauche(v, 'l', 'b', 'h'); var V = v.l * v.b * v.h / 100, L = V * 1000, s = v.sack ? Math.ceil(L / v.sack - 1e-9) : null;
    return { wert: L, gross: zahl(L, 6), einh: 'l', label: zahl(V, 4) + ' m³', zeilen: [['Volumen', zahl(V, 6) + ' m³'], ['Fläche', zahl(v.l * v.b, 6) + ' m²']].concat(s ? [['Säcke à ' + zahl(v.sack) + ' l', s + ' Stück']] : []),
      schritte: ['V = Länge · Breite · Höhe = ' + zahl(v.l) + ' · ' + zahl(v.b) + ' · ' + zahl(v.h / 100) + ' m = ' + zahl(V, 6) + ' m³', '1 m³ = 1000 l → ' + zahl(L, 6) + ' l'], hinweis: 'Erde sackt nach – etwa 10–20 % mehr einplanen.' }; } });
K({ id: 'rohr', b: 'bau', t: 'Rohrinhalt', u: 'Wassermenge in Leitungen', f: [F('d', 'Innendurchmesser', 'mm', 20), F('l', 'Länge', 'm', 25)],
  r: function (v) { brauche(v, 'd', 'l'); var r = v.d / 2000, V = Math.PI * r * r * v.l, L = V * 1000;
    return { wert: L, gross: zahl(L, 4), einh: 'l', label: 'Inhalt von ' + zahl(v.l) + ' m Rohr, Ø ' + zahl(v.d) + ' mm', zeilen: [['pro Meter', zahl(L / v.l, 4) + ' l/m'], ['Masse Wasser', '≈ ' + zahl(L, 4) + ' kg']], schritte: ['V = π · r² · l = π · ' + zahl(r) + '² m² · ' + zahl(v.l) + ' m = ' + zahl(V, 6) + ' m³ = ' + zahl(L, 6) + ' l'] }; } });

/* ---------- Chemie ---------- */
K({ id: 'molmasse', b: 'chemie', t: 'Molare Masse', u: 'aus Summenformel, mit Klammern und Hydraten', breit: true, f: [T('formel', 'Summenformel oder Stoffname', 'H2SO4', { formel: true })],
  r: function (v) { if (!v.formel) throw new LeerFehler('Summenformel eingeben, z. B. CuSO4·5H2O.'); var r = molMasse(v.formel);
    var zeilen = r.teile.map(function (t) { return [t.s + ' – ' + t.el.n, t.n + ' × ' + dz(t.el.m, 4) + ' = ' + dz(t.m, 3) + ' g/mol · ' + dz(t.anteil * 100, 2) + ' %']; });
    return { wert: r.M, gross: dz(r.M, 3), einh: 'g/mol', label: (r.name ? r.name + ' · ' : '') + 'M(' + formelHuebsch(r.formel) + ')', labelHtml: true, zeilen: zeilen, zeilenTitel: 'Zusammensetzung',
      schritte: ['M = Σ (Anzahl · Atommasse)', r.teile.map(function (t) { return t.n + ' · ' + dz(t.el.m, 4); }).join(' + ') + ' = ' + dz(r.M, 4) + ' g/mol'],
      svg: ring(r.teile.map(function (t) { return { l: t.s + ' (' + esc(t.el.n) + ')', v: t.m, txt: dz(t.anteil * 100, 2) + ' %' }; }), { mitte: dz(r.M, 2), unter: 'g/mol', titel: 'Massenanteile' }),
      hinweis: 'Atommassen nach IUPAC (Standardwerte, auf 4–5 Stellen); bei radioaktiven Elementen Massenzahl des stabilsten Isotops.' }; } });
K({ id: 'stoffmenge', b: 'chemie', t: 'Stoffmenge ↔ Masse ↔ Teilchen', u: 'n = m / M · N = n · Nₐ', f: [T('formel', 'Summenformel', 'NaCl', { formel: true }), F('m', 'Masse m', 'g', 50), F('n', 'oder Stoffmenge n', 'mol', null)],
  r: function (v) { if (!v.formel) throw new LeerFehler(); var r = molMasse(v.formel), M = r.M, m = v.m, n = v.n, s, main;
    if (m != null) { n = m / M; main = 'n'; s = 'n = m / M = ' + zahl(m) + ' g / ' + dz(M, 3) + ' g/mol = ' + zahl(n, 6) + ' mol'; }
    else if (n != null) { m = n * M; main = 'm'; s = 'm = n · M = ' + zahl(n) + ' mol · ' + dz(M, 3) + ' g/mol = ' + zahl(m, 6) + ' g'; } else throw new LeerFehler('Masse oder Stoffmenge eingeben.');
    var N = n * 6.02214076e23;
    return { wert: main === 'n' ? n : m, gross: zahl(main === 'n' ? n : m, 5), einh: main === 'n' ? 'mol' : 'g', label: formelHuebsch(r.formel) + ' (M = ' + dz(M, 3) + ' g/mol)', labelHtml: true,
      zeilen: [['Masse', zahl(m, 6) + ' g'], ['Stoffmenge', zahl(n, 6) + ' mol = ' + zahl(n * 1000, 6) + ' mmol'], ['Teilchenzahl', zahl(N, 5)], ['Gasvolumen (falls Gas, 0 °C)', zahl(n * 22.414, 5) + ' l']], schritte: ['M(' + r.formel + ') = ' + dz(M, 3) + ' g/mol', s, 'N = n · Nₐ = ' + zahl(n, 6) + ' · 6,02214076 × 10²³ = ' + zahl(N, 5)] }; } });
K({ id: 'konz', b: 'chemie', t: 'Konzentration', u: 'mol/l, g/l und Massenanteil', f: [T('formel', 'Summenformel', 'NaCl', { formel: true }), F('m', 'Masse gelöster Stoff', 'g', 9), F('V', 'Volumen Lösung', 'ml', 1000), F('ml', 'Masse Lösung (optional, für Massen-%)', 'g', null)],
  r: function (v) { brauche(v, 'm', 'V'); pos(v, 'V', 'Volumen'); var z = [], s = [], M = null; try { if (v.formel) M = molMasse(v.formel).M; } catch (e) { throw e; }
    var bl = v.m / (v.V / 1000); z.push(['Massenkonzentration β', zahl(bl, 6) + ' g/l']); s.push('β = m / V = ' + zahl(v.m) + ' g / ' + zahl(v.V / 1000) + ' l = ' + zahl(bl, 6) + ' g/l');
    var c = null; if (M) { c = bl / M; z.unshift(['Stoffmengenkonzentration c', zahl(c, 6) + ' mol/l = ' + zahl(c * 1000, 6) + ' mmol/l']); s.push('c = β / M = ' + zahl(bl, 6) + ' / ' + dz(M, 3) + ' = ' + zahl(c, 6) + ' mol/l'); }
    var w = null; if (v.ml) { w = v.m / v.ml * 100; z.push(['Massenanteil w', zahl(w, 5) + ' %']); s.push('w = m(Stoff) / m(Lösung) = ' + zahl(w, 5) + ' %'); }
    return { wert: c != null ? c : bl, gross: zahl(c != null ? c : bl, 5), einh: c != null ? 'mol/l' : 'g/l', label: (v.formel ? formelHuebsch(v.formel) + ' · ' : '') + zahl(v.m) + ' g in ' + zahl(v.V) + ' ml', labelHtml: true, zeilen: z, schritte: s }; } });
K({ id: 'verduennen', b: 'chemie', t: 'Verdünnen', u: 'c₁ · V₁ = c₂ · V₂ – drei Werte eingeben', f: [F('c1', 'Ausgangskonzentration c₁', '', 1), F('v1', 'Ausgangsvolumen V₁', 'ml', null), F('c2', 'Zielkonzentration c₂', '', 0.1), F('v2', 'Zielvolumen V₂', 'ml', 500)],
  r: function (v) { var g = ['c1', 'v1', 'c2', 'v2'].filter(function (k) { return v[k] != null; }); if (g.length < 3) throw new LeerFehler('Drei der vier Werte eingeben.');
    var c1 = v.c1, v1 = v.v1, c2 = v.c2, v2 = v.v2, m, s;
    if (v1 == null) { v1 = c2 * v2 / c1; m = 'v1'; s = 'V₁ = c₂ · V₂ / c₁ = ' + zahl(c2) + ' · ' + zahl(v2) + ' / ' + zahl(c1) + ' = ' + zahl(v1, 6) + ' ml'; }
    else if (v2 == null) { v2 = c1 * v1 / c2; m = 'v2'; s = 'V₂ = c₁ · V₁ / c₂ = ' + zahl(v2, 6) + ' ml'; }
    else if (c2 == null) { c2 = c1 * v1 / v2; m = 'c2'; s = 'c₂ = c₁ · V₁ / V₂ = ' + zahl(c2, 6); } else { c1 = c2 * v2 / v1; m = 'c1'; s = 'c₁ = c₂ · V₂ / V₁ = ' + zahl(c1, 6); }
    if (c2 > c1) throw new Error('Durch Verdünnen wird die Konzentration kleiner – c₂ muss kleiner als c₁ sein.');
    var mv = { c1: c1, v1: v1, c2: c2, v2: v2 };
    return { wert: mv[m], gross: zahl(mv[m], 5), einh: m[0] === 'v' ? 'ml' : '', label: { v1: 'Ausgangslösung abmessen', v2: 'Endvolumen', c1: 'Ausgangskonzentration', c2: 'Endkonzentration' }[m],
      zeilen: [['Ausgangslösung', zahl(v1, 6) + ' ml'], ['Lösungsmittel dazu', zahl(v2 - v1, 6) + ' ml'], ['Endvolumen', zahl(v2, 6) + ' ml'], ['Verdünnungsfaktor', '1 : ' + zahl(v2 / v1, 4)]],
      schritte: ['Die Stoffmenge bleibt gleich: c₁ · V₁ = c₂ · V₂', s], svg: ring([{ l: 'Ausgangslösung', v: v1, txt: zahl(v1, 4) + ' ml' }, { l: 'Lösungsmittel', v: v2 - v1, txt: zahl(v2 - v1, 4) + ' ml' }], { mitte: '1:' + zahl(v2 / v1, 3) }), hinweis: 'Volumen-Additivität angenommen (bei starken Säuren/Ethanol nur näherungsweise).' }; } });
K({ id: 'mischkreuz', b: 'chemie', t: 'Mischungskreuz', u: 'zwei Lösungen auf Zielgehalt mischen', f: [F('w1', 'Gehalt Lösung 1', '%', 40), F('w2', 'Gehalt Lösung 2 (Wasser = 0)', '%', 0), F('wz', 'Zielgehalt', '%', 10), F('mz', 'Gewünschte Gesamtmenge', 'g', 1000)],
  r: function (v) { brauche(v, 'w1', 'w2', 'wz'); var hi = Math.max(v.w1, v.w2), lo = Math.min(v.w1, v.w2); if (v.wz > hi || v.wz < lo) throw new Error('Der Zielgehalt muss zwischen den beiden Ausgangsgehalten liegen.'); if (v.w1 === v.w2) throw new Error('Die Gehalte müssen verschieden sein.');
    var t1 = Math.abs(v.wz - v.w2), t2 = Math.abs(v.w1 - v.wz), mz = v.mz || (t1 + t2), m1 = mz * t1 / (t1 + t2), m2 = mz - m1;
    return { wert: m1, gross: zahl(t1, 4) + ' : ' + zahl(t2, 4), label: 'Teile Lösung 1 : Lösung 2', zeilen: [['Lösung 1 (' + zahl(v.w1) + ' %)', zahl(m1, 6) + ' g'], ['Lösung 2 (' + zahl(v.w2) + ' %)', zahl(m2, 6) + ' g']],
      schritte: ['Teile Lösung 1 = |Ziel − Gehalt 2| = |' + zahl(v.wz) + ' − ' + zahl(v.w2) + '| = ' + zahl(t1), 'Teile Lösung 2 = |Gehalt 1 − Ziel| = |' + zahl(v.w1) + ' − ' + zahl(v.wz) + '| = ' + zahl(t2), 'Auf ' + zahl(mz) + ' g verteilt: ' + zahl(m1, 6) + ' g + ' + zahl(m2, 6) + ' g'],
      svg: ring([{ l: 'Lösung 1', v: m1, txt: zahl(m1, 4) + ' g' }, { l: 'Lösung 2', v: m2, txt: zahl(m2, 4) + ' g' }], { mitte: zahl(v.wz) + ' %' }), hinweis: 'Gilt für Massenanteile (Massen-%), nicht für Volumenprozent.' }; } });
K({ id: 'ph', b: 'chemie', t: 'pH-Wert', u: 'aus c(H⁺), c(OH⁻) oder pOH (25 °C)', f: [W('art', 'Gegeben', [['h', 'c(H⁺) in mol/l'], ['oh', 'c(OH⁻) in mol/l'], ['ph', 'pH-Wert'], ['poh', 'pOH-Wert']], 'h'), F('w', 'Wert', '', 0.001)],
  r: function (v) { brauche(v, 'w'); var ph, s;
    if (v.art === 'h') { pos(v, 'w', 'Konzentration'); ph = -Math.log10(v.w); s = 'pH = −lg c(H⁺) = −lg ' + zahl(v.w) + ' = ' + zahl(ph, 4); }
    else if (v.art === 'oh') { pos(v, 'w', 'Konzentration'); var poh = -Math.log10(v.w); ph = 14 - poh; s = 'pOH = −lg c(OH⁻) = ' + zahl(poh, 4) + ' → pH = 14 − pOH = ' + zahl(ph, 4); }
    else if (v.art === 'poh') { ph = 14 - v.w; s = 'pH = 14 − pOH = ' + zahl(ph, 4); } else { ph = v.w; s = 'pH gegeben'; }
    var bez = ph < 3 ? 'stark sauer' : ph < 6.5 ? 'sauer' : ph <= 7.5 ? 'neutral' : ph < 11 ? 'basisch' : 'stark basisch';
    return { wert: ph, gross: zahl(ph, 4), einh: 'pH', label: bez, zeilen: [['c(H⁺)', zahl(Math.pow(10, -ph), 4) + ' mol/l'], ['c(OH⁻)', zahl(Math.pow(10, ph - 14), 4) + ' mol/l'], ['pOH', zahl(14 - ph, 4)]], schritte: ['Bei 25 °C gilt pH + pOH = 14 (Ionenprodukt des Wassers 10⁻¹⁴)', s],
      svg: skala(ph, [{ bis: 3, l: 'stark sauer', f: FARB[4] }, { bis: 6.5, l: 'sauer', f: FARB[2] }, { bis: 7.5, l: 'neutral', f: FARB[0] }, { bis: 11, l: 'basisch', f: FARB[1] }, { bis: 14, l: 'stark bas.', f: FARB[3] }], 0, 14, { titel: 'pH-Skala', txt: 'pH ' + zahl(ph, 3) }),
      hinweis: 'Gilt für starke Säuren/Basen in verdünnter Lösung (vollständige Dissoziation). Für schwache Säuren den pKs-Wert berücksichtigen.' }; } });

/* ---------- Kalender & Zeit ---------- */
function wtVergleich(o, kal) {
  var J = jdn(o.y, o.m, o.d, kal), g = ausJdnG(J), j = ausJdnJ(J), z = [];
  z.push(['Gregorianisch' + (J < 2299161 ? ' (proleptisch)' : ''), datumLang(g) + ' · ' + WT[wochentag(J)]]);
  z.push(['Julianisch' + (J >= 2299161 ? ' (alter Stil)' : j.y < -45 ? ' (proleptisch)' : ''), datumLang(j) + ' · ' + WT[wochentag(J)]]);
  return z;
}
K({ id: 'k-wochentag', b: 'kalender', t: 'Wochentag zu jedem Datum', u: 'auch weit in Vergangenheit und Zukunft', breit: true,
  f: [F('t', 'Tag', '', null, { ganz: true }), F('m', 'Monat', '', null, { ganz: true }), F('j', 'Jahr (astron.: 0 = 1 v. Chr.)', '', null, { ganz: true }), W('kal', 'Datum ist', KAL_OPT, 'g')],
  vor: function (ctx) { return { t: ctx.heute.d, m: ctx.heute.m, j: ctx.heute.y }; },
  r: function (v, ctx) { brauche(v, 't', 'm', 'j'); var kal = v.kal === 'j' ? 'j' : 'g', y = Math.round(v.j), m = Math.round(v.m), d = Math.round(v.t);
    if (m < 1 || m > 12) throw new Error('Monat 1 bis 12.'); if (d < 1 || d > monLaenge(y, m, kal)) throw new Error('Diesen Tag gibt es im ' + MON[m - 1] + ' ' + jahrText(y) + ' nicht.');
    if (Math.abs(y) > 10000000) throw new Error('Bitte ein Jahr zwischen −10.000.000 und 10.000.000.');
    var o = { y: y, m: m, d: d }, J = jdn(y, m, d, kal), wt = wochentag(J), H = jdnG(ctx.heute.y, ctx.heute.m, ctx.heute.d), diff = J - H, g = ausJdnG(J), kw = isoWoche(J);
    var z = wtVergleich(o, kal).concat([['Julianische Tageszahl (JD 12 Uhr UT)', gz(J)], ['Tag des Jahres', tagDesJahres(o, kal) + ' von ' + (jdn(y + 1, 1, 1, kal) - jdn(y, 1, 1, kal))],
      ['Kalenderwoche (ISO, gregor.)', 'KW ' + kw.w + (kw.y !== g.y ? ' (' + jahrText(kw.y) + ')' : '')], ['Schaltjahr', (kal === 'j' ? schaltJ(y) : schaltG(y)) ? 'ja' : 'nein'],
      ['Abstand zu heute', diff === 0 ? 'heute' : (diff > 0 ? 'in ' : 'vor ') + gz(Math.abs(diff)) + ' Tagen (≈ ' + zahl(Math.abs(diff) / 365.2425, 4) + ' Jahre)']]);
    var schritte = ['Datum → Julianische Tageszahl (fortlaufende Tageszählung seit 1. Januar 4713 v. Chr.): JD = ' + gz(J),
      'Wochentag = (JD + 1) mod 7 = ' + mod(J + 1, 7) + ' → ' + WT[wt] + ' (0 = Sonntag)', 'Kalender-Regel: ' + (kal === 'j' ? 'julianisch – jedes 4. Jahr Schaltjahr' : 'gregorianisch – jedes 4. Jahr Schaltjahr, außer volle Jahrhunderte, die nicht durch 400 teilbar sind'),
      y <= 0 ? 'Astronomische Jahreszählung: Jahr 0 = 1 v. Chr., Jahr −1 = 2 v. Chr. (historisch gibt es kein Jahr 0).' : ''].filter(Boolean);
    var fok = v._fokus === 'kw';
    return { wert: wt, gross: fok ? 'KW ' + kw.w : WT[wt], label: datumLang(o) + (kal === 'j' ? ' (julianisch)' : ''), zeilen: z, schritte: schritte, svg: kalBlatt(o, J, kal), hinweis: kalHinweis(y) }; } });
K({ id: 'k-plusminus', b: 'kalender', t: 'Datum ± Zeitraum', u: 'heute + 100 Tage, vor 5000 Jahren …', f: [D('d', 'Ausgangsdatum', ''), F('n', 'Anzahl', '', 100, { ganz: true }), W('e', 'Einheit', [['t', 'Tage'], ['w', 'Wochen'], ['m', 'Monate'], ['j', 'Jahre']], 't'), W('r', 'Richtung', [['+', 'später (+)'], ['-', 'früher (−)']], '+')],
  r: function (v, ctx) { brauche(v, 'n'); var o = datumOderHeute(v, 'd', ctx, 'g'), n = Math.round(v.n) * (v.r === '-' ? -1 : 1), z, J0 = jdnG(o.y, o.m, o.d), J;
    if (Math.abs(n) > 5e6) throw new Error('Bitte höchstens 5 Millionen.');
    if (v.e === 't' || v.e === 'w') { J = J0 + n * (v.e === 'w' ? 7 : 1); z = ausJdnG(J); }
    else { z = plusMonate(o, n * (v.e === 'j' ? 12 : 1), 'g'); J = jdnG(z.y, z.m, z.d); }
    var eN = { t: 'Tage', w: 'Wochen', m: 'Monate', j: 'Jahre' }[v.e];
    return { wert: J, gross: WT[wochentag(J)], label: datumLang(z), zeilen: wtVergleich(z, 'g').concat([['Abstand', gz(Math.abs(J - J0)) + ' Tage'], ['Ausgangsdatum', datumLang(o) + ' · ' + WT[wochentag(J0)]]]),
      schritte: [datumLang(o) + ' ' + (n < 0 ? '−' : '+') + ' ' + gz(Math.abs(n)) + ' ' + eN, v.e === 't' || v.e === 'w' ? 'Über die Julianische Tageszahl: ' + gz(J0) + (n < 0 ? ' − ' : ' + ') + gz(Math.abs(J - J0)) + ' = ' + gz(J) : 'Monate/Jahre werden im Kalender gezählt; gibt es den Tag im Zielmonat nicht (31.), gilt der Monatsletzte.', 'Wochentag = (JD + 1) mod 7 → ' + WT[wochentag(J)]],
      svg: kalBlatt(z, J, 'g'), hinweis: kalHinweis(z.y) }; } });
K({ id: 'k-diff', b: 'kalender', t: 'Zeitraum zwischen zwei Daten', u: 'Tage, Wochen, Jahre-Monate-Tage, Arbeitstage', f: [D('a', 'Von', ''), D('b', 'Bis', '24.12.'), W('land', 'Bundesland (Arbeitstage)', LAND_OPT, 'SL', { land: true })],
  r: function (v, ctx) { var a = datumOderHeute(v, 'a', ctx, 'g'), b = datumOderHeute(v, 'b', ctx, 'g'), Ja = jdnG(a.y, a.m, a.d), Jb = jdnG(b.y, b.m, b.d);
    if (b.ohneJahr && Jb < Ja) { b = { y: b.y + 1, m: b.m, d: b.d }; Jb = jdnG(b.y, b.m, b.d); }
    var t = Jb - Ja, x = t < 0 ? b : a, y = t < 0 ? a : b, ymd = differenzYMD(x, y, 'g'), at = arbeitstage(Ja, Jb, v.land || 'SL');
    var z = [['Wochen', fl(Math.abs(t) / 7) + ' Wochen und ' + Math.abs(t) % 7 + ' Tage'], ['Kalendarisch', ymdText(ymd)], ['Stunden', gz(Math.abs(t) * 24)], ['Von', datumLang(a) + ' · ' + WT[wochentag(Ja)]], ['Bis', datumLang(b) + ' · ' + WT[wochentag(Jb)]]];
    if (at != null) z.push(['Arbeitstage (Mo–Fr ohne Feiertage ' + (v.land || 'SL') + ', beide Tage mitgezählt)', gz(at)]);
    return { wert: t, gross: gz(t), einh: Math.abs(t) === 1 ? 'Tag' : 'Tage', label: (t < 0 ? 'zurück: ' : '') + datumKurz(a) + ' → ' + datumKurz(b), zeilen: z,
      schritte: ['Beide Daten in Julianische Tageszahlen: ' + gz(Ja) + ' und ' + gz(Jb), 'Differenz = ' + gz(Jb) + ' − ' + gz(Ja) + ' = ' + gz(t) + ' Tage (Starttag nicht mitgezählt)', 'Mit Start- und Endtag: ' + gz(Math.abs(t) + 1) + ' Tage'],
      svg: balken([{ l: 'Tage', v: Math.abs(t), txt: gz(Math.abs(t)) }, { l: 'Arbeitstage', v: at || 0, txt: at == null ? '–' : gz(at) }, { l: 'Wochenenden/Feiertage', v: Math.max(0, Math.abs(t) + 1 - (at || 0)), txt: gz(Math.max(0, Math.abs(t) + 1 - (at || 0))) }]) }; } });
K({ id: 'k-alter', b: 'kalender', t: 'Alter & Geburtstag', u: 'genaues Alter, Lebenstage, nächster Geburtstag', f: [D('g', 'Geburtsdatum', '15.03.1985'), D('s', 'Stichtag', '')],
  r: function (v, ctx) { var g = datumOderHeute(v, 'g', ctx, 'g'), s = datumOderHeute(v, 's', ctx, 'g'), Jg = jdnG(g.y, g.m, g.d), Js = jdnG(s.y, s.m, s.d);
    if (Js < Jg) throw new Error('Der Stichtag liegt vor dem Geburtsdatum.');
    var a = differenzYMD(g, s, 'g'), ny = s.y, nb; for (;;) { var dd = Math.min(g.d, monLaenge(ny, g.m, 'g')); nb = jdnG(ny, g.m, dd); if (nb >= Js) break; ny++; }
    var t10 = Jg + 10000;
    return { wert: a.y, gross: gz(a.y), einh: 'Jahre', label: ymdText(a), zeilen: [['Lebenstage', gz(Js - Jg)], ['Lebenswochen', gz(fl((Js - Jg) / 7))], ['Geboren an einem', WT[wochentag(Jg)]],
      ['Nächster Geburtstag', nb === Js ? 'heute – herzlichen Glückwunsch!' : 'in ' + gz(nb - Js) + ' Tagen, ' + WT[wochentag(nb)] + ' (' + (ny - g.y) + '.)'], ['10.000. Lebenstag', datumLang(ausJdnG(t10)) + ' · ' + WT[wochentag(t10)]]],
      schritte: ['Kalendarisches Alter: volle Jahre, dann volle Monate, dann Resttage', 'Lebenstage = JD(Stichtag) − JD(Geburt) = ' + gz(Js) + ' − ' + gz(Jg)] }; } });
K({ id: 'k-countdown', b: 'kalender', t: 'Countdown', u: 'läuft live mit', live: true, f: [D('z', 'Zieldatum', '24.12.'), T('uhr', 'Uhrzeit', '18:00', { kurz: true })],
  r: function (v, ctx) { var z = datumOderHeute(v, 'z', ctx, 'g'), u = /^(\d{1,2})(?::(\d{2}))?$/.exec(String(v.uhr || '0:00').trim()) || [0, 0, 0], hh = +u[1] || 0, mm = +u[2] || 0;
    if (z.ohneJahr) { var t0 = new Date(z.y, z.m - 1, z.d, hh, mm).getTime(); if (t0 < ctx.jetzt) z = { y: z.y + 1, m: z.m, d: z.d }; }
    if (z.y < 100 || z.y > 270000) throw new Error('Countdown nur für Jahre 100 bis 270.000.');
    var ziel = new Date(z.y, z.m - 1, z.d, hh, mm); ziel.setFullYear(z.y); var ms = ziel.getTime() - ctx.jetzt, vorbei = ms < 0; ms = Math.abs(ms);
    var d = fl(ms / 864e5), h = fl(ms % 864e5 / 36e5), mi = fl(ms % 36e5 / 6e4), se = fl(ms % 6e4 / 1000), zz = function (x) { return (x < 10 ? '0' : '') + x; };
    return { wert: ms, gross: gz(d) + ' T ' + zz(h) + ':' + zz(mi) + ':' + zz(se), label: (vorbei ? 'seit ' : 'bis ') + datumLang(z) + ', ' + zz(hh) + ':' + zz(mm) + ' Uhr', zeilen: [['in Stunden', zahl(ms / 36e5, 6)], ['in Minuten', gz(ms / 6e4)], ['in Sekunden', gz(ms / 1000)], ['in Wochen', zahl(ms / 6048e5, 4)]],
      schritte: ['Differenz in Millisekunden zwischen Zielzeit und jetzt (Gerätezeit, Ortszeit inkl. Sommerzeit).'] }; } });
K({ id: 'k-feiertage', b: 'kalender', t: 'Ostern & Feiertage', u: 'gesetzliche Feiertage je Bundesland', breit: true, f: [F('j', 'Jahr', '', null, { ganz: true }), W('land', 'Bundesland', LAND_OPT, 'SL', { land: true })],
  vor: function (ctx) { return { j: ctx.heute.y }; },
  r: function (v, ctx) { brauche(v, 'j'); var y = Math.round(v.j), land = v.land || 'SL';
    if (y < 1583 || y > 9999) { var oj = osternJ(y); if (y < 1 || y > 9999) throw new Error('Ostern hier für die Jahre 1 bis 9999.');
      return { wert: 0, gross: oj.d + '. ' + MON[oj.m - 1], label: 'Ostersonntag ' + y + ' (julianisch, nach alter Osterrechnung)', zeilen: [['Gregorianisch entspricht', datumLang(ausJdnG(jdnJ(oj.y, oj.m, oj.d)))]], schritte: ['Vor 1583: julianische Osterformel (Meeus): a = J mod 4, b = J mod 7, c = J mod 19, d = (19c + 15) mod 30, e = (2a + 4b − d + 34) mod 7'], hinweis: 'Gesetzliche Feiertage im heutigen Sinn gibt es für dieses Jahr nicht.' }; }
    var o = osternG(y), L = feiertage(y, land), H = jdnG(ctx.heute.y, ctx.heute.m, ctx.heute.d), n = 0;
    var z = L.map(function (f) { var d = ausJdnG(f.J); if (f.g) n++; return [(f.g ? '' : '<span class="rz-grau">') + esc(f.n) + (f.g ? '' : ' (kein gesetzl. Feiertag)</span>') + (f.h ? ' <small>' + esc(f.h) + '</small>' : ''), WTK[wochentag(f.J)] + ', ' + datumKurz(d) + (f.J === H ? ' · heute' : '')]; });
    var a = mod(y, 19), b = fl(y / 100), c = mod(y, 100);
    return { wert: jdnG(o.y, o.m, o.d), gross: o.d + '. ' + MON[o.m - 1], label: 'Ostersonntag ' + y + ' · ' + n + ' gesetzliche Feiertage in ' + LAENDER.filter(function (l) { return l[0] === land; })[0][1], zeilen: z, zeilenHtml: true, zeilenTitel: 'Feiertage ' + y,
      schritte: ['Osterformel nach Gauß (in der Fassung von Butcher/Meeus): a = J mod 19 = ' + a + ', b = J div 100 = ' + b + ', c = J mod 100 = ' + c, 'Ostern ist der erste Sonntag nach dem ersten Frühlingsvollmond (frühestens 22. März, spätestens 25. April).', 'Bewegliche Feste: Karfreitag −2, Christi Himmelfahrt +39, Pfingstmontag +50, Fronleichnam +60 Tage.'],
      hinweis: 'Stand: geltendes Landesrecht; für frühere Jahre vereinfacht. Grau: keine gesetzlichen Feiertage.' }; } });
K({ id: 'k-monat', b: 'kalender', t: 'Monatskalender', u: 'beliebiger Monat, beliebiges Jahr', f: [F('m', 'Monat', '', null, { ganz: true }), F('j', 'Jahr', '', null, { ganz: true }), W('kal', 'Kalender', KAL_OPT, 'g'), W('land', 'Feiertage', LAND_OPT, 'SL', { land: true })],
  vor: function (ctx) { return { m: ctx.heute.m, j: ctx.heute.y }; },
  r: function (v, ctx) { brauche(v, 'm', 'j'); var m = Math.round(v.m), y = Math.round(v.j), kal = v.kal === 'j' ? 'j' : 'g'; if (m < 1 || m > 12) throw new Error('Monat 1 bis 12.');
    var J1 = jdn(y, m, 1, kal), n = monLaenge(y, m, kal), off = mod(wochentag(J1) + 6, 7), H = jdnG(ctx.heute.y, ctx.heute.m, ctx.heute.d), fc = {}, land = v.land || 'SL';
    var h = '<table class="rz-mk"><caption>' + MON[m - 1] + ' ' + esc(jahrText(y)) + (kal === 'j' ? ' (julianisch)' : '') + '</caption><thead><tr><th scope="col" class="rz-kw">KW</th>' + ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So'].map(function (x) { return '<th scope="col">' + x + '</th>'; }).join('') + '</tr></thead><tbody>';
    var tag = 1 - off;
    while (tag <= n) {
      h += '<tr><th scope="row" class="rz-kw">' + isoWoche(J1 + Math.max(tag, 1) - 1).w + '</th>';
      for (var i = 0; i < 7; i++, tag++) {
        if (tag < 1 || tag > n) { h += '<td></td>'; continue; }
        var J = J1 + tag - 1, f = (y >= 1583 && kal === 'g') ? istFeiertag(J, land, fc) : null, cls = (J === H ? ' rz-heute' : '') + (f ? ' rz-fei' : '') + (i >= 5 ? ' rz-we' : '');
        h += '<td class="' + cls.trim() + '"' + (f ? ' title="' + esc(f) + '"' : '') + '>' + tag + (f ? '<i aria-label="' + esc(f) + '"></i>' : '') + '</td>';
      }
      h += '</tr>';
    }
    h += '</tbody></table>';
    return { wert: n, gross: MON[m - 1], einh: jahrText(y), label: n + ' Tage · beginnt am ' + WT[wochentag(J1)], schritte: ['Erster Tag: JD ' + gz(J1) + ' → ' + WT[wochentag(J1)], 'Wochen nach ISO 8601 (Woche beginnt Montag; KW 1 enthält den ersten Donnerstag).'], svg: h, hinweis: (kalHinweis(y) ? kalHinweis(y) + ' ' : '') + (y >= 1583 && kal === 'g' ? 'Punkt = gesetzlicher Feiertag (' + land + ').' : '') }; } });
K({ id: 'k-zonen', b: 'kalender', t: 'Weltzeit & Zeitzonen', u: 'live, mit Sommerzeit', live: true, breit: true, f: [T('uhr', 'Uhrzeit umrechnen (leer = jetzt)', '', { kurz: true }), W('von', 'Von Zeitzone', ZONEN.map(function (z) { return [z[0], z[1]]; }), 'Europe/Berlin'), W('nach', 'Nach Zeitzone', ZONEN.map(function (z) { return [z[0], z[1]]; }), 'America/New_York', { tausch: 'von' })],
  r: function (v, ctx) { var ms = ctx.jetzt, u = /^(\d{1,2})(?::(\d{2}))?$/.exec(String(v.uhr || '').trim()), schritte = [];
    if (u) { var h = ctx.heute, ov = tzVersatz(v.von, ms), utc = Date.UTC(h.y, h.m - 1, h.d, +u[1], +(u[2] || 0)) - ov * 60000; ov = tzVersatz(v.von, utc); ms = Date.UTC(h.y, h.m - 1, h.d, +u[1], +(u[2] || 0)) - ov * 60000; schritte.push(u[0] + ' Uhr in ' + zoneName(v.von) + ' (' + versatzText(ov) + ') = ' + new Date(ms).toISOString().slice(11, 16) + ' UTC'); }
    var vn = tzVersatz(v.nach, ms), vv = tzVersatz(v.von, ms);
    schritte.push('Zeitunterschied ' + zoneName(v.nach) + ' − ' + zoneName(v.von) + ': ' + (vn - vv >= 0 ? '+' : '−') + dz(Math.abs(vn - vv) / 60, 2) + ' h');
    var z = ZONEN.map(function (x) { return [esc(x[1]) + ' <small>' + versatzText(tzVersatz(x[0], ms)) + '</small>', esc(zeitIn(x[0], ms))]; });
    var t = zeitIn(v.nach, ms).split(', ');
    return { wert: vn - vv, gross: t[t.length - 1], einh: 'Uhr', label: zoneName(v.nach) + ' · ' + t.slice(0, -1).join(', ') + (u ? ' (wenn ' + u[0] + ' Uhr in ' + zoneName(v.von) + ')' : ''), zeilen: z, zeilenHtml: true, zeilenTitel: u ? 'Gleichzeitig' : 'Jetzt in', schritte: schritte, hinweis: 'Zeitzonen und Sommerzeit aus der Zeitzonen-Datenbank des Geräts.' }; } });
K({ id: 'k-unix', b: 'kalender', t: 'Unix-Zeit', u: 'Sekunden seit 1.1.1970 UTC', live: true, f: [T('u', 'Unix-Zeitstempel (leer = jetzt)', '', { kurz: false }), D('d', 'oder Datum → Unix (0 Uhr Ortszeit)', '')],
  r: function (v, ctx) { var ms, s = [];
    if (v.d) { var o = datumLesen(v.d, 'g', ctx.heute); if (!o) throw new Error('Datum nicht erkannt.'); var dt = new Date(o.y, o.m - 1, o.d); dt.setFullYear(o.y); ms = dt.getTime(); s.push(datumLang(o) + ' 0:00 Ortszeit'); }
    else if (v.u) { var n = zahlLesen(v.u); if (isNaN(n)) throw new Error('Bitte eine Zahl eingeben.'); ms = Math.abs(n) > 1e11 ? n : n * 1000; s.push(Math.abs(n) > 1e11 ? 'Wert als Millisekunden erkannt' : 'Wert in Sekunden'); }
    else ms = ctx.jetzt;
    var dd = new Date(ms); if (isNaN(dd.getTime())) throw new Error('Außerhalb des darstellbaren Bereichs.');
    return { wert: fl(ms / 1000), gross: String(fl(ms / 1000)), einh: 's', label: dd.toLocaleString('de-DE', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' }),
      zeilen: [['UTC (ISO 8601)', dd.toISOString()], ['Millisekunden', String(Math.round(ms))], ['Julianisches Datum', zahl(ms / 864e5 + 2440587.5, 12)]], schritte: s.concat(['Unix-Zeit = Sekunden seit 1.1.1970, 0:00 UTC (ohne Schaltsekunden)', 'JD = Unix/86400 + 2440587,5']) }; } });
function mondSVG(f) {
  var r = 46, cx = 60, cy = 60, x = Math.abs(Math.cos(2 * Math.PI * f)) * r, zun = f < 0.5, sw;
  if (zun) sw = f < 0.25 ? 0 : 1; else sw = f < 0.75 ? 0 : 1;
  var p = 'M' + cx + ' ' + (cy - r) + ' A' + r + ' ' + r + ' 0 0 ' + (zun ? 1 : 0) + ' ' + cx + ' ' + (cy + r) + ' A' + x.toFixed(2) + ' ' + r + ' 0 0 ' + sw + ' ' + cx + ' ' + (cy - r) + ' Z';
  return '<svg class="rz-mond" viewBox="0 0 120 120" role="img" aria-label="Mondansicht"><circle cx="60" cy="60" r="46" class="rz-mn"/><path d="' + p + '" class="rz-mh"/></svg>';
}
K({ id: 'k-mond', b: 'kalender', t: 'Mondphase', u: 'Näherung über den mittleren Mondumlauf', f: [D('d', 'Datum', '')],
  r: function (v, ctx) { var o = datumOderHeute(v, 'd', ctx, 'g'), JD = jdnG(o.y, o.m, o.d), ph = mondphase(JD), J = JD;
    var nv = J + Math.round(ph.bisVoll), nn = J + Math.round(ph.bisNeu);
    return { wert: ph.beleuchtet, gross: ph.name, label: datumLang(o) + ' · ' + dz(ph.beleuchtet * 100, 0) + ' % beleuchtet', zeilen: [['Mondalter', dz(ph.alter, 1) + ' Tage seit Neumond'], ['Nächster Vollmond (≈)', datumLang(ausJdnG(nv)) + ' · ' + WTK[wochentag(nv)]], ['Nächster Neumond (≈)', datumLang(ausJdnG(nn)) + ' · ' + WTK[wochentag(nn)]]],
      schritte: ['Mittlerer synodischer Monat: 29,530589 Tage', 'Bezugs-Neumond: 6. Januar 2000, 18:14 UT (JD 2451550,1)', 'Mondalter = (JD − 2451550,1) mod 29,530589 = ' + dz(ph.alter, 2) + ' Tage'], svg: mondSVG(ph.f), hinweis: 'Näherung: Der wahre Mond weicht bis zu etwa ±14 Stunden vom Mittelwert ab.' }; } });
K({ id: 'k-jahreszeiten', b: 'kalender', t: 'Jahreszeiten & Sonnenwenden', u: 'astronomischer Beginn (Näherung)', f: [F('j', 'Jahr', '', null, { ganz: true })], vor: function (ctx) { return { j: ctx.heute.y }; },
  r: function (v) { brauche(v, 'j'); var y = Math.round(v.j), L = jahreszeiten(y); if (!L) throw new Error('Diese Näherung gilt für die Jahre −1000 bis 3000.');
    var z = L.map(function (x) { var d = jdZuDatumZeit(x.JD), zz = function (q) { return (q < 10 ? '0' : '') + q; }; return [x.n, WTK[wochentag(d.J)] + ', ' + datumKurz(d.dat) + (d.kal === 'j' ? ' (jul.)' : '') + ', ≈ ' + zz(d.h) + ':' + zz(d.min) + ' UT']; });
    var f = jdZuDatumZeit(L[0].JD);
    return { wert: L[0].JD, gross: f.dat.d + '. ' + MON[f.dat.m - 1], label: 'Frühlingsanfang ' + jahrText(y), zeilen: z, schritte: ['Mittlere Termine nach J. Meeus (Astronomical Algorithms, Tab. 27), Polynom in Jahrtausenden', 'Ohne periodische Korrekturen und ΔT – Abweichung meist unter einer Stunde, in fernen Jahrhunderten mehr.'], hinweis: 'Zeiten in Weltzeit (UT); MEZ = UT + 1 h, MESZ = UT + 2 h.' }; } });

/* ---------- Geld & Alltag ---------- */
function farbeAuf(gut) { return gut ? 'var(--rz-f1)' : 'var(--rz-f5)'; }
K({ id: 'zins', b: 'geld', t: 'Zinseszins & Sparplan', u: 'Kapital, monatliche Rate, Laufzeit', breit: true, f: [F('k0', 'Startkapital', '€', 10000), F('rate', 'Monatliche Sparrate', '€', 0), F('p', 'Zinssatz', '% p. a.', 3), F('n', 'Laufzeit', 'Jahre', 10, { ganz: true }), W('iv', 'Zinsgutschrift', [['j', 'jährlich'], ['m', 'monatlich']], 'j')],
  r: function (v) { brauche(v, 'k0', 'p', 'n'); var n = Math.round(v.n), rate = v.rate || 0, i = v.p / 100; if (n < 1 || n > 100) throw new Error('Laufzeit 1 bis 100 Jahre.');
    var K = v.k0, ein = v.k0, x = ['Start'], s1 = [K], s2 = [ein];
    for (var j = 1; j <= n; j++) {
      if (v.iv === 'm') { for (var mm = 0; mm < 12; mm++) K = (K + rate) * (1 + i / 12); }
      else K = K * (1 + i) + rate * (12 + i * 6.5);
      ein += rate * 12; x.push(j + '. J'); s1.push(rund(K, 12)); s2.push(ein);
    }
    var Z = K - ein;
    return { wert: K, gross: fix(K, 2), einh: '€', label: 'Endkapital nach ' + n + ' Jahren', zeilen: [['Eingezahlt', geld(ein)], ['Zinsen', geld(Z)], ['Zinsanteil am Endkapital', dz(Z / K * 100, 1) + ' %']],
      schritte: rate ? ['Monatliche Raten zu Monatsbeginn' + (v.iv === 'm' ? ', Zins monatlich: K = (K + Rate) · (1 + p/12)' : ', Zins jährlich: K_neu = K · (1 + p) + Rate · (12 + p · 6,5)'), 'Ergebnis nach ' + n + ' Jahren: ' + geld(K)]
        : ['Formel: Kₙ = K₀ · (1 + p)ⁿ' + (v.iv === 'm' ? ' bzw. monatlich K₀ · (1 + p/12)^(12n)' : ''), 'Kₙ = ' + fix(v.k0, 2) + ' · ' + zahl(v.iv === 'm' ? 1 + i / 12 : 1 + i) + hoch(v.iv === 'm' ? 12 * n : n) + ' = ' + fix(K, 2) + ' €'],
      kurs: { x: x, s: [{ n: 'Kapital', w: s1, f: 'var(--rz-f1)' }, { n: 'Eingezahlt', w: s2, f: 'var(--rz-f3)' }], fmt: 'geld' }, hinweis: 'Ohne Steuern, Gebühren und Inflation. Keine Anlageempfehlung.' }; } });
K({ id: 'kredit', b: 'geld', t: 'Kredit / Annuität', u: 'Monatsrate oder Laufzeit, Tilgungsverlauf', breit: true, f: [F('k', 'Kreditbetrag', '€', 20000), F('p', 'Sollzins', '% p. a.', 5), F('n', 'Laufzeit', 'Jahre', 5), F('rate', 'oder Monatsrate', '€', null)],
  r: function (v) { brauche(v, 'k', 'p'); var i = v.p / 1200, N, A, s = [];
    if (v.n != null && v.n > 0) { N = Math.round(v.n * 12); A = i ? v.k * i / (1 - Math.pow(1 + i, -N)) : v.k / N; s.push('Annuität A = K · i / (1 − (1 + i)^−n), i = ' + zahl(v.p) + ' % / 12, n = ' + N + ' Monate'); s.push('A = ' + fix(v.k, 2) + ' · ' + zahl(i, 6) + ' / (1 − ' + zahl(1 + i, 8) + '^−' + N + ') = ' + fix(A, 2) + ' €'); }
    else if (v.rate) { A = v.rate; if (A <= v.k * i) throw new Error('Die Rate deckt nicht einmal die Zinsen (' + geld(v.k * i) + ' pro Monat).'); N = Math.ceil(i ? -Math.log(1 - v.k * i / A) / Math.log(1 + i) : v.k / A); s.push('Laufzeit n = −ln(1 − K·i/A) / ln(1 + i) = ' + N + ' Monate'); }
    else throw new LeerFehler('Laufzeit oder Monatsrate eingeben.');
    var R = v.k, x = ['Start'], s1 = [R], s2 = [0], zs = 0;
    for (var m = 1; m <= N; m++) { var z = R * i, t = Math.min(A - z, R); R -= t; zs += z; if (m % 12 === 0 || m === N) { x.push(m % 12 === 0 ? (m / 12) + '. J' : dz(m / 12, 1) + ' J'); s1.push(Math.max(0, rund(R, 10))); s2.push(zs); } }
    return { wert: A, gross: fix(A, 2), einh: '€ / Monat', label: geld(v.k) + ' zu ' + zahl(v.p) + ' % über ' + (N % 12 ? dz(N / 12, 1) : N / 12) + ' Jahre', zeilen: [['Laufzeit', N + ' Monate'], ['Zinsen gesamt', geld(zs)], ['Gesamtbetrag', geld(v.k + zs)]], schritte: s,
      kurs: { x: x, s: [{ n: 'Restschuld', w: s1, f: 'var(--rz-f2)' }, { n: 'Zinsen bisher', w: s2, f: 'var(--rz-f5)' }], fmt: 'geld', fallendGut: true }, hinweis: 'Monatliche Raten, konstanter Zins, keine Gebühren. Keine Finanzberatung.' }; } });
K({ id: 'inflation', b: 'geld', t: 'Inflation & Kaufkraft', u: 'Was ist ein Betrag in n Jahren wert?', f: [F('b', 'Betrag heute', '€', 1000), F('r', 'Inflationsrate', '% p. a.', 2.5), F('n', 'Jahre', '', 20, { ganz: true })],
  r: function (v) { brauche(v, 'b', 'r', 'n'); var n = Math.round(v.n); if (n < 1 || n > 200) throw new Error('1 bis 200 Jahre.'); var q = 1 + v.r / 100, kk = v.b / Math.pow(q, n), pr = v.b * Math.pow(q, n), x = [], s1 = [], s2 = [];
    for (var j = 0; j <= n; j++) { x.push(j ? j + '. J' : 'heute'); s1.push(v.b / Math.pow(q, j)); s2.push(v.b * Math.pow(q, j)); }
    return { wert: kk, gross: fix(kk, 2), einh: '€', label: 'Kaufkraft von ' + geld(v.b) + ' in ' + n + ' Jahren', zeilen: [['Gleicher Warenkorb kostet dann', geld(pr)], ['Kaufkraftverlust', dz((1 - kk / v.b) * 100, 1) + ' %'], ['Halbierung der Kaufkraft nach', zahl(Math.log(2) / Math.log(q), 3) + ' Jahren']],
      schritte: ['Kaufkraft = B / (1 + r)ⁿ = ' + fix(v.b, 2) + ' / ' + zahl(q) + hoch(n) + ' = ' + fix(kk, 2) + ' €', 'Preis = B · (1 + r)ⁿ = ' + fix(pr, 2) + ' €'],
      kurs: { x: x, s: [{ n: 'Kaufkraft', w: s1, f: 'var(--rz-f5)' }, { n: 'Preis Warenkorb', w: s2, f: 'var(--rz-f6)' }], fmt: 'geld' } }; } });
K({ id: 'rabatt', b: 'geld', t: 'Rabatt', u: 'auch mehrere Rabatte nacheinander', f: [F('p', 'Preis', '€', 80), F('r1', 'Rabatt', '%', 20), F('r2', 'zweiter Rabatt (optional)', '%', null)],
  r: function (v) { brauche(v, 'p', 'r1'); var a = v.p * (1 - v.r1 / 100), b = v.r2 ? a * (1 - v.r2 / 100) : a, ges = (1 - b / v.p) * 100;
    return { wert: b, gross: fix(b, 2), einh: '€', label: 'statt ' + geld(v.p), zeilen: [['Ersparnis', geld(v.p - b)], ['Gesamtrabatt', dz(ges, 2) + ' %']].concat(v.r2 ? [['Nach 1. Rabatt', geld(a)]] : []),
      schritte: ['Preis · (1 − ' + zahl(v.r1) + ' %) = ' + fix(a, 2) + ' €'].concat(v.r2 ? ['· (1 − ' + zahl(v.r2) + ' %) = ' + fix(b, 2) + ' €', 'Rabatte multiplizieren sich: ' + zahl(v.r1) + ' % + ' + zahl(v.r2) + ' % ergibt nur ' + dz(ges, 2) + ' %, nicht ' + zahl(v.r1 + v.r2) + ' %.'] : []),
      svg: ring([{ l: 'Zu zahlen', v: b, txt: geld(b) }, { l: 'Ersparnis', v: v.p - b, txt: geld(v.p - b) }], { mitte: '−' + dz(ges, 0) + ' %' }) }; } });
K({ id: 'trinkgeld', b: 'geld', t: 'Trinkgeld & Teilen', u: 'Rechnung aufteilen', f: [F('b', 'Rechnungsbetrag', '€', 86.4), F('tg', 'Trinkgeld', '%', 10), F('pers', 'Personen', '', 3, { ganz: true })],
  r: function (v) { brauche(v, 'b'); var tg = v.tg || 0, p = Math.max(1, Math.round(v.pers || 1)), g = v.b * (1 + tg / 100), je = g / p, auf = Math.ceil(je);
    return { wert: je, gross: fix(je, 2), einh: '€ pro Person', label: 'Gesamt ' + geld(g) + ' inkl. ' + zahl(tg) + ' % Trinkgeld', zeilen: [['Trinkgeld', geld(g - v.b)], ['Aufgerundet pro Person', geld(auf) + ' (gesamt ' + geld(auf * p) + ')']], schritte: ['Gesamt = ' + fix(v.b, 2) + ' · ' + zahl(1 + tg / 100) + ' = ' + fix(g, 2) + ' €', 'Pro Person = ' + fix(g, 2) + ' / ' + p + ' = ' + fix(je, 2) + ' €'] }; } });
K({ id: 'lohn', b: 'geld', t: 'Stundenlohn ↔ Monat ↔ Jahr', u: 'brutto, mit Wochenstunden', f: [F('w', 'Betrag', '€', 18.5), W('art', 'Betrag ist', [['h', 'Stundenlohn'], ['m', 'Monatslohn'], ['j', 'Jahreslohn']], 'h'), F('std', 'Wochenstunden', 'h', 40), F('mon', 'Gehälter pro Jahr', '', 12)],
  r: function (v) { brauche(v, 'w', 'std'); var f = 52 / 12, st = v.std, mo = v.mon || 12, h, m, j;
    if (v.art === 'm') { m = v.w; h = m / (st * f); } else if (v.art === 'j') { j = v.w; m = j / mo; h = j / (st * 52); } else { h = v.w; m = h * st * f; }
    if (j == null) j = v.art === 'h' ? h * st * 52 * (mo / 12) : m * mo;
    return { wert: v.art === 'h' ? m : h, gross: fix(v.art === 'h' ? m : h, 2), einh: v.art === 'h' ? '€ / Monat' : '€ / Stunde', label: 'bei ' + zahl(st) + ' Wochenstunden (brutto)', zeilen: [['Stundenlohn', geld(h)], ['Monatslohn', geld(m)], ['Jahreslohn (' + zahl(mo) + ' Gehälter)', geld(j)], ['Monatsstunden (Ø)', zahl(st * f, 4) + ' h']],
      schritte: ['Ø Wochen pro Monat = 52 / 12 = 4,333', 'Monatsstunden = ' + zahl(st) + ' · 4,333 = ' + zahl(st * f, 4) + ' h', 'Monatslohn = Stundenlohn · Monatsstunden'], hinweis: 'Bruttowerte; Netto hängt von Steuerklasse und Sozialabgaben ab.' }; } });
K({ id: 'sprit', b: 'geld', t: 'Spritkosten einer Fahrt', u: 'Strecke, Verbrauch, Preis', f: [F('km', 'Strecke', 'km', 300), F('vb', 'Verbrauch', 'l/100 km', 6.5), F('pr', 'Preis', '€/l', 1.75), F('pers', 'Personen (teilen)', '', 1, { ganz: true }), W('hz', 'Fahrt', [['e', 'einfach'], ['h', 'hin und zurück']], 'e')],
  r: function (v) { brauche(v, 'km', 'vb', 'pr'); var km = v.km * (v.hz === 'h' ? 2 : 1), l = km * v.vb / 100, k = l * v.pr, p = Math.max(1, Math.round(v.pers || 1));
    return { wert: k, gross: fix(k, 2), einh: '€', label: zahl(km) + ' km · ' + zahl(l, 4) + ' l', zeilen: [['Verbrauch', zahl(l, 4) + ' l'], ['pro Person', geld(k / p)], ['pro km', fix(k / km * 100, 1) + ' ct']], schritte: ['Liter = ' + zahl(km) + ' km · ' + zahl(v.vb) + ' / 100 = ' + zahl(l, 4) + ' l', 'Kosten = ' + zahl(l, 4) + ' l · ' + fix(v.pr, 2) + ' €/l = ' + fix(k, 2) + ' €'], hinweis: 'Nur Kraftstoff; Verschleiß und Versicherung nicht enthalten.' }; } });
K({ id: 'geraet', b: 'geld', t: 'Stromverbrauch von Geräten', u: 'Betrieb + Standby, pro Jahr', f: [F('P', 'Leistung im Betrieb', 'W', 120), F('h', 'Betriebsstunden pro Tag', 'h', 4), F('sb', 'Standby-Leistung', 'W', 1), F('pr', 'Strompreis', '€/kWh', 0.35)],
  r: function (v) { brauche(v, 'P', 'h', 'pr'); var h = Math.min(24, v.h), eb = v.P * h * 365 / 1000, es = (v.sb || 0) * (24 - h) * 365 / 1000, e = eb + es, k = e * v.pr;
    return { wert: k, gross: fix(k, 2), einh: '€ / Jahr', label: zahl(e, 4) + ' kWh pro Jahr', zeilen: [['Betrieb', zahl(eb, 4) + ' kWh = ' + geld(eb * v.pr)], ['Standby', zahl(es, 4) + ' kWh = ' + geld(es * v.pr)], ['pro Monat', geld(k / 12)]], schritte: ['Betrieb: ' + zahl(v.P) + ' W · ' + zahl(h) + ' h · 365 = ' + zahl(eb, 4) + ' kWh', 'Standby: ' + zahl(v.sb || 0) + ' W · ' + zahl(24 - h) + ' h · 365 = ' + zahl(es, 4) + ' kWh', 'Kosten = ' + zahl(e, 4) + ' kWh · ' + fix(v.pr, 2) + ' € = ' + fix(k, 2) + ' €'],
      svg: ring([{ l: 'Betrieb', v: eb, txt: geld(eb * v.pr) }, { l: 'Standby', v: es, txt: geld(es * v.pr) }], { mitte: geld(k), unter: 'pro Jahr' }) }; } });

/* ---------- Gesundheit ---------- */
var BMI_Z = [{ bis: 18.5, l: 'Unter', f: FARB[1] }, { bis: 25, l: 'Normal', f: FARB[0] }, { bis: 30, l: 'Über', f: FARB[5] }, { bis: 35, l: 'Adip. I', f: FARB[2] }, { bis: 40, l: 'II', f: FARB[4] }, { bis: 45, l: 'III', f: FARB[3] }];
K({ id: 'bmi', b: 'gesundheit', t: 'Body-Mass-Index', u: 'WHO-Einteilung für Erwachsene', f: [F('kg', 'Gewicht', 'kg', 80), F('cm', 'Größe', 'cm', 180)],
  r: function (v) { brauche(v, 'kg', 'cm'); pos(v, 'cm', 'Größe'); var m = v.cm / 100, b = v.kg / (m * m), k = b < 18.5 ? 'Untergewicht' : b < 25 ? 'Normalgewicht' : b < 30 ? 'Übergewicht (Präadipositas)' : b < 35 ? 'Adipositas Grad I' : b < 40 ? 'Adipositas Grad II' : 'Adipositas Grad III';
    return { wert: b, gross: dz(b, 1), einh: 'kg/m²', label: k, zeilen: [['Normalgewicht bei dieser Größe', dz(18.5 * m * m, 1) + ' – ' + dz(24.9 * m * m, 1) + ' kg']], schritte: ['BMI = Gewicht / Größe² = ' + zahl(v.kg) + ' kg / (' + zahl(m) + ' m)² = ' + dz(b, 2), 'WHO: < 18,5 Untergewicht · 18,5–24,9 Normal · 25–29,9 Präadipositas · ab 30 Adipositas'],
      svg: skala(b, BMI_Z, 15, 45, { titel: 'BMI-Skala', txt: dz(b, 1) }), hinweis: 'Grober Richtwert – berücksichtigt weder Muskelmasse, Alter noch Körperbau. Ersetzt keine ärztliche Beratung.' }; } });
K({ id: 'grundumsatz', b: 'gesundheit', t: 'Grund- & Gesamtumsatz', u: 'Mifflin-St Jeor', f: [W('g', 'Geschlecht', [['m', 'männlich'], ['w', 'weiblich']], 'm'), F('a', 'Alter', 'Jahre', 40), F('kg', 'Gewicht', 'kg', 80), F('cm', 'Größe', 'cm', 180),
  W('pal', 'Aktivität (PAL)', [['1.2', '1,2 – kaum Bewegung'], ['1.4', '1,4 – sitzend, wenig Sport'], ['1.6', '1,6 – gehend/stehend'], ['1.8', '1,8 – körperlich arbeitend'], ['2.0', '2,0 – schwere Arbeit/viel Sport']], '1.6')],
  r: function (v) { brauche(v, 'a', 'kg', 'cm'); var gu = 10 * v.kg + 6.25 * v.cm - 5 * v.a + (v.g === 'w' ? -161 : 5), pal = parseFloat(v.pal) || 1.4;
    return { wert: gu, gross: gz(gu), einh: 'kcal/Tag', label: 'Grundumsatz (Ruhe)', zeilen: [['Gesamtumsatz bei PAL ' + dz(pal, 1), gz(gu * pal) + ' kcal/Tag'], ['in Kilojoule', gz(gu * pal * 4.184) + ' kJ/Tag']], schritte: ['GU = 10 · kg + 6,25 · cm − 5 · Alter ' + (v.g === 'w' ? '− 161' : '+ 5'), 'GU = ' + zahl(10 * v.kg) + ' + ' + zahl(6.25 * v.cm) + ' − ' + zahl(5 * v.a) + (v.g === 'w' ? ' − 161' : ' + 5') + ' = ' + gz(gu) + ' kcal', 'Gesamtumsatz = GU · PAL'],
      svg: balken([{ l: 'Grundumsatz', v: gu, txt: gz(gu) + ' kcal' }, { l: 'Gesamtumsatz', v: gu * pal, txt: gz(gu * pal) + ' kcal', hl: true }]), hinweis: 'Schätzformel mit ca. ±10 % Streuung. Ersetzt keine ärztliche Beratung.' }; } });
K({ id: 'trinken', b: 'gesundheit', t: 'Trinkmenge (Richtwert)', u: 'für gesunde Erwachsene', f: [F('kg', 'Körpergewicht', 'kg', 75), W('akt', 'Situation', [['n', 'normal'], ['s', 'Sport / Hitze']], 'n')],
  r: function (v) { brauche(v, 'kg'); var ml = v.kg * 35 + (v.akt === 's' ? 750 : 0);
    return { wert: ml, gross: dz(ml / 1000, 1), einh: 'l / Tag', label: 'Gesamtwasserbedarf (Faustregel 35 ml/kg)', zeilen: [['davon über Getränke (≈ 70 %)', dz(ml * 0.7 / 1000, 1) + ' l'], ['DGE-Richtwert Getränke', 'ca. 1,5 l pro Tag']], schritte: ['Faustregel: 30–35 ml je kg Körpergewicht', zahl(v.kg) + ' kg · 35 ml = ' + gz(v.kg * 35) + ' ml' + (v.akt === 's' ? ' + 750 ml für Sport/Hitze' : '')], hinweis: 'Bei Herz- oder Nierenerkrankungen gelten andere Mengen. Ersetzt keine ärztliche Beratung.' }; } });
K({ id: 'pace', b: 'gesundheit', t: 'Tempo / Pace', u: 'Laufen, Gehen, Radfahren', f: [F('km', 'Strecke', 'km', 10), T('zeit', 'Zeit (h:mm:ss oder mm:ss)', '55:00', { kurz: true })],
  r: function (v) { brauche(v, 'km'); pos(v, 'km', 'Strecke'); var s = zeitLesen(v.zeit); if (!s) throw new LeerFehler('Zeit eingeben, z. B. 55:00.'); var p = s / v.km, kmh = v.km / (s / 3600);
    var ziele = [[5, '5 km'], [10, '10 km'], [21.0975, 'Halbmarathon'], [42.195, 'Marathon']];
    return { wert: p, gross: dauerText(p), einh: 'min/km', label: zahl(kmh, 4) + ' km/h', zeilen: ziele.map(function (z) { return [z[1] + ' bei gleichem Tempo', dauerText(p * z[0])]; }).concat([['pro Meile', dauerText(p * 1.609344)]]), schritte: ['Pace = Zeit / Strecke = ' + gz(s) + ' s / ' + zahl(v.km) + ' km = ' + zahl(p, 5) + ' s/km', 'Geschwindigkeit = ' + zahl(v.km) + ' km / ' + zahl(s / 3600, 5) + ' h = ' + zahl(kmh, 5) + ' km/h'], hinweis: 'Hochrechnung bei konstantem Tempo – längere Strecken sind real meist langsamer.' }; } });

/* ===================================================================== 8b. Praxis-Rechner (seit 12.11.2026)
   Garten · Küche · Baustelle · Geld · Gesundheit · Sonne · Musik · Zahlen.
   Alle Tabellenwerte sind Richtwerte; leere Felder mit „(leer = Richtwert)“ nehmen den Tabellenwert. */
function oder(x, d) { return x == null || (typeof x === 'number' && isNaN(x)) ? d : x; }
function auf(x) { return Math.ceil(x - 1e-9); }
function zeile(L, id) { for (var i = 0; i < L.length; i++) if (L[i][0] === id) return L[i]; return L[0]; }
function wahlOpt(L) { return L.map(function (x) { return [x[0], x[1]]; }); }
function uhr(min) { min = ((Math.round(min) % 1440) + 1440) % 1440; var h = Math.floor(min / 60), m = min % 60; return (h < 10 ? '0' : '') + h + ':' + (m < 10 ? '0' : '') + m; }
function uhrLesen(s) { var m = /^\s*(\d{1,2})(?:[:.h](\d{1,2}))?\s*(?:uhr)?\s*$/i.exec(String(s == null ? '' : s)); if (!m) return null; var h = +m[1], mi = +(m[2] || 0); if (h > 24 || mi > 59) return null; return (h % 24) * 60 + mi; }
function stdText(h) { if (!isFinite(h)) return '–'; var m = Math.round(h * 60); return Math.floor(m / 60) + ' h ' + (m % 60 < 10 ? '0' : '') + (m % 60) + ' min'; }

/* ---------- Garten ---------- */
/* id, Name, Reihenabstand cm, Abstand in der Reihe cm, Tausendkorngewicht g (bei Kartoffeln Pflanzknolle) */
var SAAT = [['moehre', 'Möhre', 25, 3, 1], ['radies', 'Radieschen', 15, 3, 8], ['salat', 'Kopfsalat', 30, 30, 1], ['spinat', 'Spinat', 20, 5, 10], ['feldsalat', 'Feldsalat', 12, 2, 1.2],
  ['rotebete', 'Rote Bete', 30, 8, 16], ['mangold', 'Mangold', 35, 25, 16], ['kohlrabi', 'Kohlrabi', 30, 25, 3.5], ['zwiebel', 'Zwiebel (Saat)', 25, 5, 3.5], ['lauch', 'Porree / Lauch', 30, 12, 3],
  ['buschbohne', 'Buschbohne', 40, 8, 350], ['erbse', 'Erbse', 40, 4, 250], ['dickebohne', 'Dicke Bohne', 50, 10, 1300], ['zuckermais', 'Zuckermais', 60, 25, 180], ['kuerbis', 'Kürbis', 150, 100, 200],
  ['zucchini', 'Zucchini', 100, 100, 130], ['gurke', 'Gurke (Freiland)', 120, 30, 25], ['tomate', 'Tomate', 80, 50, 3], ['kartoffel', 'Kartoffel (Pflanzknollen)', 65, 33, 60000]];
K({ id: 'g-saat', b: 'garten', t: 'Saatgutbedarf', u: 'Pflanzen, Samen und Gramm für ein Beet', s: 'saat samen aussaat pflanzabstand reihenabstand säen',
  f: [W('k', 'Kultur', wahlOpt(SAAT), 'moehre'), F('a', 'Beetfläche', 'm²', 4), F('ra', 'Reihenabstand (leer = Richtwert)', 'cm', null), F('ab', 'Abstand in der Reihe (leer = Richtwert)', 'cm', null), F('keim', 'Keimfähigkeit', '%', 85)],
  r: function (v) { brauche(v, 'a'); pos(v, 'a', 'Beetfläche'); var k = zeile(SAAT, v.k), ra = oder(v.ra, k[2]), ab = oder(v.ab, k[3]), keim = oder(v.keim, 85); if (!(ra > 0) || !(ab > 0)) throw new Error('Abstände müssen größer als 0 sein.'); if (!(keim > 0) || keim > 100) throw new Error('Keimfähigkeit zwischen 1 und 100 %.');
    var n = v.a / (ra * ab / 1e4), reihe = v.a / (ra / 100), samen = n / (keim / 100), g = samen * k[4] / 1000, knolle = k[0] === 'kartoffel';
    return { wert: n, gross: gz(n), einh: 'Pflanzen', label: k[1] + ' auf ' + zahl(v.a, 4) + ' m²',
      zeilen: [['Abstände', zahl(ra) + ' × ' + zahl(ab) + ' cm'], ['Reihenlänge gesamt', zahl(reihe, 3) + ' m'], [knolle ? 'Pflanzknollen (inkl. Ausfall)' : 'Samen (inkl. Keimausfall)', gz(Math.ceil(samen)) + ' Stück'], [knolle ? 'Pflanzgut' : 'Saatgut', knolle ? '≈ ' + zahl(g / 1000, 3) + ' kg' : '≈ ' + zahl(g, 3) + ' g']],
      schritte: ['Pflanzen = Fläche / (Reihenabstand · Abstand in der Reihe) = ' + zahl(v.a) + ' m² / (' + zahl(ra / 100) + ' m · ' + zahl(ab / 100) + ' m) = ' + zahl(n, 5), 'Samen = Pflanzen / Keimfähigkeit = ' + zahl(n, 5) + ' / ' + zahl(keim / 100) + ' = ' + zahl(samen, 5), 'Gewicht = Samen · Tausendkorngewicht / 1000 = ' + zahl(samen, 5) + ' · ' + zahl(k[4]) + ' g / 1000 = ' + zahl(g, 4) + ' g'],
      hinweis: 'Richtwerte für den Hausgarten – die Angaben auf der Saatguttüte gehen vor. Feine Saat (Möhre, Feldsalat) wird meist dichter gesät und später vereinzelt.' }; } });

var JAUCHE = [['bn', 'Brennnesseljauche – gießen (1 : 10)', 10], ['bnb', 'Brennnesseljauche – Jungpflanzen / über das Blatt (1 : 20)', 20], ['bw', 'Beinwelljauche – gießen (1 : 10)', 10], ['sh', 'Ackerschachtelhalm-Brühe (1 : 5)', 5], ['x', 'eigenes Verhältnis', 10]];
K({ id: 'g-jauche', b: 'garten', t: 'Jauche & Brühe verdünnen', u: 'Ansatz und Wasser für die Gießkanne', s: 'jauche brühe brennnessel beinwell verdünnung gießkanne dünger',
  f: [W('art', 'Ansatz', wahlOpt(JAUCHE), 'bn'), F('x', 'Verdünnung 1 : x (leer = Richtwert)', '', null), F('m', 'Fertige Gießmenge', 'l', 10)],
  r: function (v) { brauche(v, 'm'); pos(v, 'm', 'Gießmenge'); var a = zeile(JAUCHE, v.art), x = oder(v.x, a[2]); if (!(x > 0)) throw new Error('Das Verhältnis muss größer als 0 sein.'); var j = v.m / (1 + x), w = v.m - j;
    return { wert: j, gross: zahl(j, 3), einh: 'l Ansatz', label: '+ ' + zahl(w, 3) + ' l Wasser = ' + zahl(v.m) + ' l (1 : ' + zahl(x) + ')', zeilen: [['Ansatz', zahl(j * 1000, 3) + ' ml'], ['Wasser', zahl(w, 4) + ' l'], ['Anteil Ansatz', dz(100 / (1 + x), 1) + ' %']],
      schritte: ['1 : ' + zahl(x) + ' heißt: 1 Teil Ansatz + ' + zahl(x) + ' Teile Wasser = ' + zahl(1 + x) + ' Teile', 'Ansatz = Gießmenge / ' + zahl(1 + x) + ' = ' + zahl(v.m) + ' l / ' + zahl(1 + x) + ' = ' + zahl(j, 4) + ' l', 'Wasser = ' + zahl(v.m) + ' − ' + zahl(j, 4) + ' = ' + zahl(w, 4) + ' l'],
      svg: ring([{ l: 'Ansatz', v: j, txt: zahl(j, 3) + ' l' }, { l: 'Wasser', v: w, txt: zahl(w, 3) + ' l' }], { mitte: '1 : ' + zahl(x) }),
      hinweis: 'Übliche Garten-Richtwerte. Nicht in praller Sonne und nicht auf trockenen Boden ausbringen; über das Blatt nur stark verdünnt.' }; } });

var DACH = [['h', 'geneigtes Dach, Ziegel/Beton/Metall (0,8)', 0.8], ['k', 'Flachdach mit Kies (0,6)', 0.6], ['g', 'Gründach (0,4)', 0.4]];
K({ id: 'g-regen', b: 'garten', t: 'Regentonne & Gießwasser', u: 'Ertrag vom Dach und wie lange die Tonne reicht', s: 'regenwasser regentonne zisterne dachfläche gießen niederschlag',
  f: [F('a', 'Dachfläche (Grundfläche)', 'm²', 60), F('mm', 'Niederschlag', 'mm', 60), W('dach', 'Dachart (Ertragsbeiwert)', wahlOpt(DACH), 'h'), F('t', 'Tonne / Speicher', 'l', 300), F('beet', 'Beetfläche', 'm²', 20), F('bed', 'Gießbedarf je Woche', 'l/m²', 20)],
  r: function (v) { brauche(v, 'a', 'mm'); var e = zeile(DACH, v.dach)[2], L = v.a * v.mm * e, z = [['Ertrag', zahl(L, 4) + ' l = ' + zahl(L / 1000, 3) + ' m³']], s = ['1 mm Regen = 1 l je m²', 'Ertrag = Dachfläche · Niederschlag · Beiwert = ' + zahl(v.a) + ' m² · ' + zahl(v.mm) + ' mm · ' + zahl(e) + ' = ' + zahl(L, 5) + ' l'];
    if (v.t > 0) z.push(['Tonne (' + zahl(v.t) + ' l) voll nach', zahl(v.t / (v.a * e), 3) + ' mm Regen']);
    if (v.beet > 0 && v.bed > 0) { var w = v.beet * v.bed; z.push(['Gießbedarf', zahl(w, 4) + ' l je Woche']); if (v.t > 0) z.push(['Volle Tonne reicht', zahl(v.t / w * 7, 2) + ' Tage']); z.push(['Ertrag deckt', zahl(L / w, 2) + ' Wochen']); s.push('Gießbedarf = Beetfläche · Bedarf = ' + zahl(v.beet) + ' m² · ' + zahl(v.bed) + ' l/m² = ' + zahl(w, 4) + ' l je Woche'); }
    return { wert: L, gross: zahl(L, 4), einh: 'l', label: 'Regenwasser aus ' + zahl(v.mm) + ' mm Niederschlag', zeilen: z, schritte: s, hinweis: 'In Deutschland fallen im Jahresmittel grob 600–1000 mm, in einem Sommermonat etwa 60–80 mm. Gemüsebeete brauchen im Sommer etwa 15–25 l/m² je Woche (Richtwert).' }; } });

/* id, Name, Schüttdichte kg/l, Empfehlung */
var MULCH = [['kompost', 'Kompost', 0.7, 'Als Düngung genügen 2–3 l/m² im Jahr (0,2–0,3 cm), zur Bodenverbesserung bis 1 cm.'], ['rinde', 'Rindenmulch', 0.35, 'Üblich sind 5–7 cm; vorher Stickstoff (z. B. Hornspäne) geben.'], ['haecksel', 'Holzhäcksel', 0.3, 'Üblich sind 5–8 cm auf Wegen und unter Gehölzen.'],
  ['rasen', 'Rasenschnitt (angetrocknet)', 0.2, 'Nur dünn, 2–3 cm, sonst fault die Schicht.'], ['stroh', 'Stroh', 0.08, 'Üblich sind 5–10 cm, z. B. unter Erdbeeren.'], ['laub', 'Laub', 0.08, 'Üblich sind 5–10 cm als Winterschutz.'], ['erde', 'Pflanzerde', 1.0, 'Erde sackt nach – 10–20 % mehr einplanen.'], ['kies', 'Kies / Splitt', 1.6, 'Für Wege meist 3–5 cm auf Vlies.'], ['sand', 'Sand', 1.5, 'Zum Abmagern schwerer Böden einarbeiten.']];
K({ id: 'g-mulch', b: 'garten', t: 'Kompost & Mulch', u: 'Menge für eine Schicht: Liter, Säcke, Gewicht', s: 'kompost mulch rindenmulch häcksel schicht säcke',
  f: [W('mat', 'Material', wahlOpt(MULCH), 'rinde'), F('a', 'Fläche', 'm²', 10), F('d', 'Schichtdicke', 'cm', 5), F('sack', 'Sackgröße', 'l', 50)],
  r: function (v) { brauche(v, 'a', 'd'); var m = zeile(MULCH, v.mat), L = v.a * v.d * 10, kg = L * m[2], z = [['Volumen', zahl(L / 1000, 3) + ' m³'], ['je m²', zahl(v.d * 10, 3) + ' l'], ['Gewicht (grob)', '≈ ' + (kg >= 1000 ? zahl(kg / 1000, 3) + ' t' : zahl(kg, 3) + ' kg')]];
    if (v.sack > 0) z.push(['Säcke à ' + zahl(v.sack) + ' l', auf(L / v.sack) + ' Stück']);
    return { wert: L, gross: zahl(L, 4), einh: 'l', label: m[1] + ', ' + zahl(v.d) + ' cm auf ' + zahl(v.a) + ' m²', zeilen: z, schritte: ['1 cm Schicht auf 1 m² = 10 l', 'Volumen = Fläche · Dicke · 10 = ' + zahl(v.a) + ' · ' + zahl(v.d) + ' · 10 = ' + zahl(L, 5) + ' l', 'Gewicht ≈ Volumen · Schüttdichte = ' + zahl(L, 5) + ' l · ' + zahl(m[2]) + ' kg/l = ' + zahl(kg, 4) + ' kg'], hinweis: m[3] + ' Schüttdichten schwanken stark mit der Feuchte.' }; } });

/* id, Name, kWh je Raummeter (lufttrocken, 15–20 % Wassergehalt), Hartholz? */
var HOLZ = [['buche', 'Buche', 1900, 1], ['eiche', 'Eiche', 1900, 1], ['birke', 'Birke', 1800, 1], ['kiefer', 'Kiefer', 1500, 0], ['fichte', 'Fichte', 1300, 0], ['pappel', 'Pappel', 1200, 0]];
K({ id: 'g-holz', b: 'garten', t: 'Brennholz: Maße & Heizwert', u: 'Raummeter, Schüttraummeter, Festmeter – und was drinsteckt', s: 'brennholz ster raummeter schüttraummeter festmeter heizwert kaminholz',
  f: [F('m', 'Menge', '', 5), W('e', 'Einheit', [['rm', 'Raummeter / Ster (geschichtet)'], ['srm', 'Schüttraummeter (lose)'], ['fm', 'Festmeter (massiv)']], 'rm'), W('art', 'Holzart', wahlOpt(HOLZ), 'buche'), F('preis', 'Preis je Einheit (optional)', '€', null)],
  r: function (v) { brauche(v, 'm'); pos(v, 'm', 'Menge'); var h = zeile(HOLZ, v.art), fFm = h[3] ? 0.62 : 0.64, fSrm = h[3] ? 1.48 : 1.62, rm = v.e === 'rm' ? v.m : v.e === 'srm' ? v.m / fSrm : v.m / fFm, kwh = rm * h[2];
    var z = [['Raummeter (33-cm-Scheite, geschichtet)', zahl(rm, 3) + ' Rm'], ['Schüttraummeter', zahl(rm * fSrm, 3) + ' Srm'], ['Festmeter', zahl(rm * fFm, 3) + ' Fm'], ['entspricht Heizöl', '≈ ' + gz(kwh / 10) + ' l'], ['Gewicht lufttrocken', '≈ ' + gz(kwh / 4) + ' kg']];
    if (v.preis > 0) z.push(['Preis je kWh', dz(v.preis * v.m / kwh * 100, 2) + ' ct']);
    return { wert: kwh, gross: gz(kwh), einh: 'kWh', label: zahl(v.m) + ' ' + ({ rm: 'Rm', srm: 'Srm', fm: 'Fm' })[v.e] + ' ' + h[1] + ', lufttrocken', zeilen: z,
      schritte: ['Umrechnung ' + (h[3] ? 'Hartholz' : 'Nadel-/Weichholz') + ' (33-cm-Scheite): 1 Rm ≈ ' + zahl(fFm) + ' Fm ≈ ' + zahl(fSrm) + ' Srm', 'Heizwert = ' + zahl(rm, 4) + ' Rm · ' + gz(h[2]) + ' kWh/Rm = ' + gz(kwh) + ' kWh', '1 l Heizöl ≈ 10 kWh · lufttrockenes Holz ≈ 4 kWh/kg'],
      svg: balken(HOLZ.map(function (x) { return { l: x[1], v: x[2], txt: gz(x[2]) + ' kWh/Rm', hl: x[0] === h[0] }; })),
      hinweis: 'Richtwerte bei 15–20 % Wassergehalt (Bayerische Landesanstalt für Wald und Forstwirtschaft, Fachagentur Nachwachsende Rohstoffe). Grobe Faustformel der Forstämter: 1 Rm ≈ 0,7 Fm, 1 Srm ≈ 0,5 Fm. Waldfrisches Holz hat etwa die Hälfte des Heizwerts.' }; } });

/* id, Name, Verbrauch kg je Person und Jahr, Ertrag kg/m² */
var ERNTE = [['kartoffel', 'Kartoffeln', 55, 3], ['moehre', 'Möhren', 10, 4], ['zwiebel', 'Zwiebeln', 9, 3], ['tomate', 'Tomaten (frisch)', 9, 6], ['gurke', 'Gurken', 6.5, 4], ['kohl', 'Weiß-/Rotkohl', 5, 5], ['salat', 'Salat', 5, 3], ['zucchini', 'Zucchini', 3, 5], ['bohne', 'Buschbohnen', 2, 1.5], ['rotebete', 'Rote Bete', 1.5, 3], ['kuerbis', 'Kürbis', 2, 3], ['erbse', 'Erbsen (gepalt)', 1, 0.8]];
K({ id: 'g-ernte', b: 'garten', t: 'Anbaufläche je Person', u: 'Wie viel Beet für den Jahresbedarf?', s: 'selbstversorgung ernte ertrag anbaufläche bedarf jahresbedarf',
  f: [W('k', 'Kultur', wahlOpt(ERNTE), 'kartoffel'), F('p', 'Personen', '', 2), F('vb', 'Verbrauch je Person (leer = Richtwert)', 'kg/Jahr', null), F('er', 'Ertrag (leer = Richtwert)', 'kg/m²', null), F('grad', 'Anteil aus dem eigenen Garten', '%', 100)],
  r: function (v) { brauche(v, 'p'); var k = zeile(ERNTE, v.k), vb = oder(v.vb, k[2]), er = oder(v.er, k[3]), grad = oder(v.grad, 100); if (!(er > 0)) throw new Error('Der Ertrag muss größer als 0 sein.'); var kg = v.p * vb * grad / 100, a = kg / er;
    return { wert: a, gross: zahl(a, 3), einh: 'm²', label: k[1] + ' für ' + zahl(v.p) + ' Person(en)', zeilen: [['Erntemenge', zahl(kg, 4) + ' kg im Jahr'], ['Verbrauch je Person', zahl(vb) + ' kg/Jahr'], ['Ertrag', zahl(er) + ' kg/m²'], ['je Woche', zahl(kg / 52, 2) + ' kg']],
      schritte: ['Erntemenge = Personen · Verbrauch · Anteil = ' + zahl(v.p) + ' · ' + zahl(vb) + ' kg · ' + zahl(grad) + ' % = ' + zahl(kg, 5) + ' kg', 'Fläche = Erntemenge / Ertrag = ' + zahl(kg, 5) + ' kg / ' + zahl(er) + ' kg/m² = ' + zahl(a, 4) + ' m²'],
      svg: balken(ERNTE.slice(0, 8).map(function (x) { return { l: x[1], v: x[2] / x[3], txt: zahl(x[2] / x[3], 2) + ' m² je Person', hl: x[0] === k[0] }; })),
      hinweis: 'Verbrauch grob nach dem Pro-Kopf-Verbrauch in Deutschland (BLE/BMEL), Erträge als Richtwerte für den Hausgarten – beides schwankt stark mit Boden, Sorte und Jahr.' }; } });

/* ---------- Küche ---------- */
K({ id: 'ku-teig', b: 'kueche', t: 'Teigausbeute & Sauerteig', u: 'TA, Hydration, Salz in Bäckerprozent', s: 'teigausbeute ta hydration sauerteig brot bäckerprozent anstellgut',
  f: [F('mehl', 'Mehl im Hauptteig', 'g', 500), F('wasser', 'Wasser im Hauptteig', 'g', 340), F('st', 'Sauerteig / Vorteig (optional)', 'g', 100), F('sta', 'TA des Sauerteigs', '', 200), F('salz', 'Salz', 'g', 11)],
  r: function (v) { brauche(v, 'mehl', 'wasser'); pos(v, 'mehl', 'Mehl'); var st = v.st || 0, sta = oder(v.sta, 200); if (st && !(sta > 100)) throw new Error('Die TA des Sauerteigs muss über 100 liegen.');
    var stM = st ? st * 100 / sta : 0, stW = st - stM, M = v.mehl + stM, Wg = v.wasser + stW, ta = (M + Wg) / M * 100, hyd = Wg / M * 100, salz = v.salz || 0, ges = v.mehl + v.wasser + st + salz, art = ta < 160 ? 'fester Teig (z. B. Brötchen, Brezeln)' : ta < 170 ? 'mittelfester Teig (z. B. Weizenbrot)' : ta < 180 ? 'weicher Teig (z. B. Mischbrot)' : 'sehr weicher Teig (z. B. Roggenbrot, Ciabatta)';
    var z = [['Hydration', dz(hyd, 1) + ' %'], ['Gesamtmehl', zahl(M, 4) + ' g'], ['Gesamtwasser', zahl(Wg, 4) + ' g'], ['Teiggewicht', zahl(ges, 4) + ' g']]; if (salz) z.push(['Salz', dz(salz / M * 100, 2) + ' % vom Mehl']); if (st) z.push(['Versäuertes Mehl', dz(stM / M * 100, 1) + ' %']);
    return { wert: ta, gross: dz(ta, 0), einh: 'TA', label: art, zeilen: z, schritte: (st ? ['Sauerteig TA ' + zahl(sta) + ': Mehl = ' + zahl(st) + ' · 100 / ' + zahl(sta) + ' = ' + zahl(stM, 4) + ' g, Wasser = ' + zahl(stW, 4) + ' g'] : []).concat(['TA = (Mehl + Wasser) / Mehl · 100 = (' + zahl(M, 4) + ' + ' + zahl(Wg, 4) + ') / ' + zahl(M, 4) + ' · 100 = ' + dz(ta, 1), 'Hydration = Wasser / Mehl · 100 = ' + dz(hyd, 1) + ' % (TA − 100)']),
      svg: skala(ta, [{ bis: 160, l: 'fest' }, { bis: 170, l: 'mittel' }, { bis: 180, l: 'weich' }, { bis: 200, l: 'sehr weich' }], 150, 200, { titel: 'Teigausbeute', txt: dz(ta, 0) }), hinweis: 'Üblich sind 1,8–2,2 % Salz bezogen auf das Mehl.' }; } });

K({ id: 'ku-form', b: 'kueche', t: 'Backform umrechnen', u: 'Rezeptmenge an eine andere Form anpassen', s: 'backform springform kuchenform blech durchmesser umrechnen',
  f: [W('fa', 'Form im Rezept', [['r', 'rund'], ['e', 'eckig']], 'r'), F('da', 'Durchmesser im Rezept', 'cm', 26, { nur: { fa: ['r'] } }), F('la', 'Länge im Rezept', 'cm', 30, { nur: { fa: ['e'] } }), F('ba', 'Breite im Rezept', 'cm', 20, { nur: { fa: ['e'] } }),
    W('fn', 'Eigene Form', [['r', 'rund'], ['e', 'eckig']], 'r'), F('dn', 'Durchmesser eigene Form', 'cm', 20, { nur: { fn: ['r'] } }), F('ln', 'Länge eigene Form', 'cm', 30, { nur: { fn: ['e'] } }), F('bn', 'Breite eigene Form', 'cm', 20, { nur: { fn: ['e'] } }), F('bsp', 'Beispiel: Menge im Rezept', 'g', 250)],
  r: function (v) { var A = function (f, d, l, b) { if (f === 'r') { if (!(d > 0)) throw new LeerFehler('Durchmesser eingeben.'); return Math.PI * d * d / 4; } if (!(l > 0) || !(b > 0)) throw new LeerFehler('Länge und Breite eingeben.'); return l * b; };
    var a1 = A(v.fa, v.da, v.la, v.ba), a2 = A(v.fn, v.dn, v.ln, v.bn), f = a2 / a1, z = [['Fläche im Rezept', zahl(a1, 4) + ' cm²'], ['Fläche eigene Form', zahl(a2, 4) + ' cm²']]; if (v.bsp > 0) z.push(['Aus ' + zahl(v.bsp) + ' g werden', zahl(v.bsp * f, 3) + ' g']); z.push(['Aus 3 Eiern werden', '≈ ' + dz(3 * f, 1) + ' Eier']);
    return { wert: f, gross: '× ' + dz(f, 2), label: 'alle Zutaten mit diesem Faktor malnehmen', zeilen: z, schritte: ['Runde Form: A = π · d² / 4 · eckige Form: A = Länge · Breite', 'Faktor = Fläche neu / Fläche alt = ' + zahl(a2, 5) + ' / ' + zahl(a1, 5) + ' = ' + zahl(f, 4)], svg: balken([{ l: 'Rezept', v: a1, txt: zahl(a1, 4) + ' cm²' }, { l: 'eigene Form', v: a2, txt: zahl(a2, 4) + ' cm²', hl: true }]),
      hinweis: 'Gilt bei gleicher Füllhöhe. Die Backzeit ändert sich kaum mit der Fläche, aber mit der Höhe – Stäbchenprobe machen.' }; } });

K({ id: 'ku-lake', b: 'kueche', t: 'Salzlake', u: 'Salzmenge zum Fermentieren und Einlegen', s: 'salzlake lake fermentieren sauerkraut salzgurken einlegen',
  f: [F('w', 'Wasser', 'ml', 1000), F('g', 'Gemüse (optional)', 'g', 0), F('p', 'Salzgehalt', '%', 2), W('bez', 'Prozent bezogen auf', [['w', 'das Wasser'], ['wg', 'Wasser + Gemüse'], ['g', 'nur das Gemüse (Trockensalzen)']], 'w')],
  r: function (v) { brauche(v, 'p'); var basis = v.bez === 'w' ? (v.w || 0) : v.bez === 'g' ? (v.g || 0) : (v.w || 0) + (v.g || 0); if (!(basis > 0)) throw new LeerFehler(v.bez === 'g' ? 'Gemüsegewicht eingeben.' : 'Wassermenge eingeben.'); var s = basis * v.p / 100;
    return { wert: s, gross: zahl(s, 3), einh: 'g Salz', label: zahl(v.p) + ' % von ' + zahl(basis) + ' g', zeilen: [['je Liter / Kilogramm', zahl(v.p * 10, 3) + ' g'], ['in gestrichenen Esslöffeln', '≈ ' + dz(s / 18, 1) + ' EL (1 EL ≈ 18 g)']],
      schritte: ['1 ml Wasser ≈ 1 g', 'Salz = Bezugsmenge · Prozent / 100 = ' + zahl(basis) + ' g · ' + zahl(v.p) + ' / 100 = ' + zahl(s, 4) + ' g'], hinweis: 'Übliche Richtwerte: Sauerkraut etwa 2 % auf das Gemüsegewicht, Gemüse in Lake 2–3 %, Salzgurken 3–5 %. Salz ohne Rieselhilfe und ohne Jod verwenden.' }; } });

K({ id: 'ku-gelier', b: 'kueche', t: 'Gelierzucker', u: 'Zucker und Gläser für Marmelade', s: 'gelierzucker marmelade konfitüre gelee einkochen gläser',
  f: [F('f', 'Früchte / Saft (vorbereitet)', 'g', 1000), W('typ', 'Gelierzucker', [['1', '1 : 1'], ['2', '2 : 1'], ['3', '3 : 1']], '2'), F('glas', 'Glasgröße', 'ml', 250)],
  r: function (v) { brauche(v, 'f'); var t = +v.typ, zk = v.f / t, ges = v.f + zk, z = [['Gesamtmasse', zahl(ges, 4) + ' g'], ['Zuckeranteil', dz(zk / ges * 100, 0) + ' %']]; if (v.glas > 0) z.push(['Gläser à ' + zahl(v.glas) + ' ml', '≈ ' + auf(ges / 1.25 / v.glas) + ' Stück']);
    return { wert: zk, gross: zahl(zk, 4), einh: 'g Gelierzucker', label: v.typ + ' : 1 auf ' + zahl(v.f) + ' g Frucht', zeilen: z, schritte: ['„' + v.typ + ' : 1“ heißt: ' + v.typ + ' Teile Frucht auf 1 Teil Zucker', 'Zucker = Frucht / ' + v.typ + ' = ' + zahl(v.f) + ' / ' + v.typ + ' = ' + zahl(zk, 4) + ' g', 'Gläser grob: Masse / 1,25 g/ml / Glasgröße'],
      svg: ring([{ l: 'Frucht', v: v.f, txt: zahl(v.f) + ' g' }, { l: 'Zucker', v: zk, txt: zahl(zk, 4) + ' g' }], { mitte: v.typ + ' : 1' }), hinweis: 'Kochzeit nach Packung (meist 3–4 Minuten sprudelnd). 2 : 1 und 3 : 1 enthalten Konservierungsstoff und halten geöffnet kürzer.' }; } });

K({ id: 'ku-alk', b: 'kueche', t: 'Alkohol verdünnen', u: 'Ansatzalkohol für Tinkturen und Liköre einstellen', s: 'tinktur ansatz weingeist verdünnen volumenprozent likör alkohol',
  f: [F('c1', 'Alkohol vorhanden', 'Vol.-%', 96), F('c2', 'gewünschte Stärke', 'Vol.-%', 40), F('v2', 'gewünschte Menge', 'ml', 500)],
  r: function (v) { brauche(v, 'c1', 'c2', 'v2'); if (!(v.c1 > 0) || v.c1 > 100 || !(v.c2 > 0)) throw new Error('Stärken zwischen 0 und 100 Vol.-% eingeben.'); if (v.c2 > v.c1) throw new Error('Die gewünschte Stärke kann nicht höher sein als die vorhandene.'); var a = v.v2 * v.c2 / v.c1, w = v.v2 - a;
    return { wert: a, gross: zahl(a, 4), einh: 'ml Alkohol', label: zahl(v.c1) + ' Vol.-% → ' + zahl(v.c2) + ' Vol.-%, ' + zahl(v.v2) + ' ml', zeilen: [['Wasser', 'bis ' + zahl(v.v2) + ' ml auffüllen (≈ ' + zahl(w, 4) + ' ml)'], ['Reiner Alkohol darin', zahl(v.v2 * v.c2 / 100, 4) + ' ml']],
      schritte: ['Mischungsgleichung: c₁ · V₁ = c₂ · V₂', 'V₁ = V₂ · c₂ / c₁ = ' + zahl(v.v2) + ' · ' + zahl(v.c2) + ' / ' + zahl(v.c1) + ' = ' + zahl(a, 5) + ' ml'], svg: ring([{ l: 'Alkohol ' + zahl(v.c1) + ' %', v: a, txt: zahl(a, 4) + ' ml' }, { l: 'Wasser', v: w, txt: '≈ ' + zahl(w, 4) + ' ml' }], { mitte: zahl(v.c2) + ' %' }),
      hinweis: 'Alkohol und Wasser ziehen sich beim Mischen zusammen: Erst den Alkohol abmessen, dann mit Wasser bis zur Zielmenge auffüllen. Reine Rechenhilfe – keine Dosier- oder Anwendungsempfehlung.' }; } });

function plato(sg) { return -616.868 + 1111.14 * sg - 630.272 * sg * sg + 135.997 * sg * sg * sg; }
function dichteAusPlato(p) { return 1 + p / (258.6 - p / 258.2 * 227.1); }
K({ id: 'ku-bier', b: 'kueche', t: 'Alkoholgehalt: Bier, Met, Most', u: 'aus Stammwürze und Restextrakt (Spindel)', s: 'bier brauen stammwürze restextrakt plato spindel met most vergärungsgrad',
  f: [F('og', 'Vor der Gärung (°P oder Dichte)', '', 12), F('fg', 'Nach der Gärung (°P oder Dichte)', '', 3)],
  r: function (v) { brauche(v, 'og', 'fg'); var sg = function (x) { return x < 1.5 ? x : dichteAusPlato(x); }, o = sg(v.og), f = sg(v.fg); if (!(o > 1) || f > o) throw new Error('Der Wert vor der Gärung muss höher sein als danach.'); var abv = (o - f) * 131.25, po = plato(o), pf = plato(f), vg = (po - pf) / po * 100;
    return { wert: abv, gross: dz(abv, 1), einh: 'Vol.-%', label: 'geschätzter Alkoholgehalt', zeilen: [['Stammwürze', dz(po, 1) + ' °P = Dichte ' + fix(o, 3)], ['Restextrakt (scheinbar)', dz(pf, 1) + ' °P = Dichte ' + fix(f, 3)], ['Scheinbarer Vergärungsgrad', dz(vg, 0) + ' %']],
      schritte: ['Werte unter 1,5 werden als Dichte gelesen, sonst als Grad Plato', 'Dichte aus Plato: SG = 1 + P / (258,6 − P / 258,2 · 227,1)', 'Alkohol ≈ (Dichte vorher − Dichte nachher) · 131,25 = (' + fix(o, 4) + ' − ' + fix(f, 4) + ') · 131,25 = ' + dz(abv, 2) + ' Vol.-%'],
      hinweis: 'Faustformel für die Bierspindel, Genauigkeit etwa ± 0,3 Vol.-%. Ein Refraktometer zeigt nach der Gärung falsche Werte an und braucht eine Korrektur.' }; } });

var GASMARK = [[140, 1], [150, 2], [170, 3], [180, 4], [190, 5], [200, 6], [220, 7], [230, 8], [240, 9]];
K({ id: 'ku-ofen', b: 'kueche', t: 'Backofen-Temperatur', u: 'Ober-/Unterhitze ↔ Umluft ↔ Gas ↔ Fahrenheit', s: 'backofen umluft heißluft oberhitze unterhitze gasstufe gas mark fahrenheit',
  f: [F('t', 'Temperatur im Rezept', '', 180), W('von', 'Angabe gilt für', [['ou', 'Ober-/Unterhitze (°C)'], ['um', 'Umluft / Heißluft (°C)'], ['f', 'Fahrenheit (°F, Ober-/Unterhitze)']], 'ou')],
  r: function (v) { brauche(v, 't'); var ou = v.von === 'um' ? v.t + 20 : v.von === 'f' ? (v.t - 32) / 1.8 : v.t, um = ou - 20, gs = Math.max(1, Math.min(8, Math.round((ou - 120) / 20))), gm = GASMARK.reduce(function (a, b) { return Math.abs(b[0] - ou) < Math.abs(a[0] - ou) ? b : a; })[1];
    return { wert: v.von === 'um' ? ou : um, gross: gz(v.von === 'um' ? ou : um), einh: '°C ' + (v.von === 'um' ? 'Ober-/Unterhitze' : 'Umluft'), label: 'statt ' + zahl(v.t) + (v.von === 'f' ? ' °F' : ' °C ' + (v.von === 'um' ? 'Umluft' : 'Ober-/Unterhitze')),
      zeilen: [['Ober-/Unterhitze', gz(ou) + ' °C'], ['Umluft / Heißluft', gz(um) + ' °C'], ['Gasherd (Stufe 1–8, Richtwert)', 'Stufe ' + gs], ['Gas Mark (britische Rezepte)', String(gm)], ['Fahrenheit', gz(ou * 1.8 + 32) + ' °F']],
      schritte: ['Umluft = Ober-/Unterhitze − 20 °C (Faustregel)', '°C = (°F − 32) / 1,8', 'Gasstufe ≈ (Temperatur − 120) / 20, je nach Hersteller verschieden'], hinweis: 'Faustregeln – Öfen weichen oft 10–20 °C ab. Bei Umluft die Backzeit etwas früher prüfen.' }; } });

/* ---------- Baustelle ---------- */
K({ id: 'b-durchfluss', b: 'bau', t: 'Rohr-Durchfluss', u: 'Volumenstrom, Fließgeschwindigkeit, Durchmesser', s: 'durchfluss volumenstrom fließgeschwindigkeit rohr leitung l/min sanitär',
  f: [W('ges', 'Gesucht', [['q', 'Volumenstrom'], ['v', 'Fließgeschwindigkeit'], ['d', 'Innendurchmesser']], 'q', { segment: true }), F('d', 'Innendurchmesser', 'mm', 16, { nur: { ges: ['q', 'v'] } }), F('v', 'Fließgeschwindigkeit', 'm/s', 1.5, { nur: { ges: ['q', 'd'] } }), F('q', 'Volumenstrom', 'l/min', 18, { nur: { ges: ['v', 'd'] } })],
  r: function (v) { var d = v.d, w = v.v, q = v.q, A;
    if (v.ges === 'q') { brauche(v, 'd', 'v'); pos(v, 'd', 'Durchmesser'); A = Math.PI * d * d / 4; q = w * A * 0.06; }
    else if (v.ges === 'v') { brauche(v, 'd', 'q'); pos(v, 'd', 'Durchmesser'); A = Math.PI * d * d / 4; w = q / 0.06 / A; }
    else { brauche(v, 'v', 'q'); pos(v, 'v', 'Geschwindigkeit'); A = q / 0.06 / w; d = Math.sqrt(4 * A / Math.PI); }
    var z = [['Volumenstrom', zahl(q, 4) + ' l/min = ' + zahl(q / 60, 3) + ' l/s = ' + zahl(q * 0.06, 3) + ' m³/h'], ['Fließgeschwindigkeit', zahl(w, 3) + ' m/s'], ['Innendurchmesser', zahl(d, 4) + ' mm'], ['Querschnitt', zahl(A, 4) + ' mm²']];
    return { wert: v.ges === 'q' ? q : v.ges === 'v' ? w : d, gross: zahl(v.ges === 'q' ? q : v.ges === 'v' ? w : d, 4), einh: v.ges === 'q' ? 'l/min' : v.ges === 'v' ? 'm/s' : 'mm', label: v.ges === 'q' ? 'Volumenstrom' : v.ges === 'v' ? 'Fließgeschwindigkeit' : 'nötiger Innendurchmesser', zeilen: z,
      schritte: ['Querschnitt A = π · d² / 4', 'Volumenstrom Q = v · A; mit v in m/s und A in mm²: Q [l/min] = v · A · 0,06', v.ges === 'q' ? 'Q = ' + zahl(w) + ' · ' + zahl(A, 5) + ' · 0,06 = ' + zahl(q, 5) + ' l/min' : v.ges === 'v' ? 'v = Q / (A · 0,06) = ' + zahl(q) + ' / (' + zahl(A, 5) + ' · 0,06) = ' + zahl(w, 4) + ' m/s' : 'A = Q / (v · 0,06) = ' + zahl(A, 5) + ' mm² → d = √(4 A / π) = ' + zahl(d, 4) + ' mm'],
      hinweis: 'Reine Strömungsrechnung ohne Druckverlust. Zulässige Fließgeschwindigkeiten und die Bemessung von Trinkwasserleitungen regelt DIN 1988-300.' }; } });

K({ id: 'b-gefaelle', b: 'bau', t: 'Gefälle', u: 'Prozent, Höhenunterschied, Verhältnis, Winkel', s: 'gefälle neigung steigung prozent abwasser terrasse höhenunterschied',
  f: [F('l', 'Länge (waagerecht)', 'm', 5), W('art', 'Bekannt ist', [['p', 'Gefälle in %'], ['h', 'Höhenunterschied in cm'], ['n', 'Verhältnis 1 : n'], ['w', 'Winkel in Grad']], 'p'), F('x', 'Wert', '', 2)],
  r: function (v) { brauche(v, 'l', 'x'); pos(v, 'l', 'Länge'); var p = v.art === 'p' ? v.x : v.art === 'h' ? v.x / (v.l * 100) * 100 : v.art === 'n' ? (v.x ? 100 / v.x : NaN) : Math.tan(v.x * Math.PI / 180) * 100; if (!isFinite(p)) throw new Error('Wert prüfen.'); var h = v.l * p, win = Math.atan(p / 100) * 180 / Math.PI;
    return { wert: h, gross: zahl(h, 4), einh: 'cm', label: 'Höhenunterschied auf ' + zahl(v.l) + ' m', zeilen: [['Gefälle', zahl(p, 4) + ' %'], ['je Meter', zahl(p * 10, 4) + ' mm'], ['Verhältnis', p ? '1 : ' + zahl(100 / p, 4) : '–'], ['Winkel', zahl(win, 3) + '°'], ['Schräge Länge', zahl(Math.sqrt(v.l * v.l + h * h / 1e4), 5) + ' m']],
      schritte: ['Gefälle in % = Höhenunterschied / Länge · 100', '1 % = 1 cm je Meter = 10 mm je Meter', 'Höhe = ' + zahl(v.l) + ' m · ' + zahl(p, 4) + ' % = ' + zahl(h, 4) + ' cm', 'Winkel = arctan(Gefälle / 100) = ' + zahl(win, 3) + '°'],
      hinweis: 'Übliche Richtwerte: Terrassen und Pflaster 1,5–2,5 %, Abwasserleitungen im Gebäude meist 1–2 % (maßgeblich sind DIN EN 12056 und DIN 1986-100).' }; } });

var HAUS = [['p', 'Passivhaus (≈ 10 W/m²)', 10], ['n', 'Neubau nach GEG (≈ 40 W/m²)', 40], ['s', 'saniert / Baujahr ab 2002 (≈ 60 W/m²)', 60], ['m', 'Baujahr 1984–2001 (≈ 80 W/m²)', 80], ['a', 'Baujahr 1960–1983, teilsaniert (≈ 120 W/m²)', 120], ['u', 'Altbau unsaniert (≈ 160 W/m²)', 160]];
K({ id: 'b-heizlast', b: 'bau', t: 'Heizlast (Überschlag)', u: 'grobe Kesselleistung aus Fläche und Baualter', s: 'heizlast heizleistung kessel wärmepumpe kw wohnfläche überschlag',
  f: [F('a', 'Beheizte Fläche', 'm²', 130), W('typ', 'Gebäude', wahlOpt(HAUS), 'm'), F('q', 'Spezifische Heizlast (leer = Richtwert)', 'W/m²', null), F('h', 'Vollbenutzungsstunden', 'h/Jahr', 2000)],
  r: function (v) { brauche(v, 'a'); var q = oder(v.q, zeile(HAUS, v.typ)[2]), kw = v.a * q / 1000, h = oder(v.h, 2000);
    return { wert: kw, gross: dz(kw, 1), einh: 'kW', label: 'Heizlast für ' + zahl(v.a) + ' m² bei ' + zahl(q) + ' W/m²', zeilen: [['Jahres-Heizwärme (grob)', gz(kw * h) + ' kWh'], ['je m² und Jahr', gz(q * h / 1000) + ' kWh/m²'], ['entspricht Heizöl / Erdgas', '≈ ' + gz(kw * h / 10) + ' l bzw. m³']],
      schritte: ['Heizlast = Fläche · spezifische Heizlast = ' + zahl(v.a) + ' m² · ' + zahl(q) + ' W/m² = ' + zahl(kw * 1000, 5) + ' W', 'Jahreswärme ≈ Heizlast · Vollbenutzungsstunden = ' + dz(kw, 2) + ' kW · ' + zahl(h) + ' h = ' + gz(kw * h) + ' kWh'],
      svg: balken(HAUS.map(function (x) { return { l: x[1].replace(/ \(.*/, ''), v: x[2] * v.a / 1000, txt: dz(x[2] * v.a / 1000, 1) + ' kW', hl: x[2] === q }; })),
      hinweis: 'Nur ein Überschlag zur Einordnung. Für die Auslegung von Kessel oder Wärmepumpe gilt die raumweise Heizlastberechnung nach DIN EN 12831; Warmwasser kommt hinzu.' }; } });

var BETON = [['b', 'Beton (≈ 2,4 t/m³)', 2.4], ['e', 'Zementestrich (≈ 2,0 t/m³)', 2.0], ['f', 'Fließestrich (≈ 2,1 t/m³)', 2.1], ['m', 'Mauer-/Putzmörtel (≈ 1,8 t/m³)', 1.8]];
K({ id: 'b-beton', b: 'bau', t: 'Beton & Estrich', u: 'Volumen, Gewicht, Säcke', s: 'beton estrich fundament bodenplatte kubikmeter säcke trockenbeton mörtel',
  f: [F('l', 'Länge', 'm', 4), F('b', 'Breite', 'm', 3), F('d', 'Dicke', 'cm', 10), W('mat', 'Material', wahlOpt(BETON), 'b'), F('sack', 'Sackgewicht (Fertigmischung)', 'kg', 40), F('erg', 'Ergiebigkeit je Sack (leer = Richtwert)', 'l', null)],
  r: function (v) { brauche(v, 'l', 'b', 'd'); var m = zeile(BETON, v.mat), V = v.l * v.b * v.d / 100, t = V * m[2], z = [['Fläche', zahl(v.l * v.b, 5) + ' m²'], ['Volumen', zahl(V * 1000, 5) + ' l'], ['Gewicht (frisch)', zahl(t, 3) + ' t']], s = ['V = Länge · Breite · Dicke = ' + zahl(v.l) + ' · ' + zahl(v.b) + ' · ' + zahl(v.d / 100) + ' m = ' + zahl(V, 5) + ' m³', 'Gewicht = V · Rohdichte = ' + zahl(V, 5) + ' · ' + zahl(m[2]) + ' = ' + zahl(t, 4) + ' t'];
    if (v.sack > 0) { var erg = oder(v.erg, v.sack * 0.5), n = auf(V * 1000 / erg); z.push(['Säcke à ' + zahl(v.sack) + ' kg (' + zahl(erg) + ' l je Sack)', n + ' Stück']); z.push(['Trockenmaterial', zahl(n * v.sack / 1000, 3) + ' t']); s.push('Säcke = Volumen / Ergiebigkeit = ' + zahl(V * 1000, 5) + ' l / ' + zahl(erg) + ' l = ' + zahl(V * 1000 / erg, 4) + ' → ' + n); }
    return { wert: V, gross: zahl(V, 3), einh: 'm³', label: m[1].replace(/ \(.*/, '') + ', ' + zahl(v.d) + ' cm stark', zeilen: z, schritte: s, hinweis: 'Richtwert: 40 kg Fertigmischung ergeben etwa 20 l (Angabe auf dem Sack prüfen). 5–10 % Reserve einplanen; ab etwa 1 m³ lohnt meist Lieferbeton.' }; } });

var PUTZ = [['kz', 'Kalkzement- / Kalkputz (≈ 1,4 kg/m² je mm)', 1.4], ['g', 'Gipsputz (≈ 1,0 kg/m² je mm)', 1.0], ['l', 'Leichtputz (≈ 1,0 kg/m² je mm)', 1.0], ['le', 'Lehmputz (≈ 1,7 kg/m² je mm)', 1.7], ['fk', 'Fliesenkleber, Zahnung 8 mm (≈ 3 kg/m²)', 3]];
K({ id: 'b-putz', b: 'bau', t: 'Putz & Kleber', u: 'Verbrauch in Kilogramm und Säcken', s: 'putz verputzen kalkzementputz gipsputz lehmputz fliesenkleber säcke verbrauch',
  f: [F('a', 'Fläche', 'm²', 30), W('art', 'Material', wahlOpt(PUTZ), 'kz'), F('d', 'Putzdicke', 'mm', 15, { nur: { art: ['kz', 'g', 'l', 'le'] } }), F('vb', 'Verbrauch (leer = Richtwert)', 'kg/m²', null), F('sack', 'Sackgewicht', 'kg', 30)],
  r: function (v) { brauche(v, 'a'); var p = zeile(PUTZ, v.art), kleber = p[0] === 'fk', d = kleber ? 1 : oder(v.d, 15), je = v.vb != null ? v.vb : p[2] * d, kg = v.a * je, z = [['Verbrauch', zahl(je, 4) + ' kg/m²']]; if (v.sack > 0) z.push(['Säcke à ' + zahl(v.sack) + ' kg', auf(kg / v.sack) + ' Stück']);
    return { wert: kg, gross: zahl(kg, 4), einh: 'kg', label: p[1].replace(/ \(.*/, '') + ' für ' + zahl(v.a) + ' m²', zeilen: z, schritte: [kleber || v.vb != null ? 'Verbrauch je m²: ' + zahl(je, 4) + ' kg' : 'Verbrauch je m² = ' + zahl(p[2]) + ' kg/mm · ' + zahl(d) + ' mm = ' + zahl(je, 4) + ' kg', 'Menge = Fläche · Verbrauch = ' + zahl(v.a) + ' · ' + zahl(je, 4) + ' = ' + zahl(kg, 5) + ' kg'], hinweis: 'Richtwerte – der Verbrauch steht im technischen Merkblatt des Herstellers und hängt vom Untergrund ab. Etwa 10 % Reserve einplanen.' }; } });

K({ id: 'b-pflaster', b: 'bau', t: 'Pflaster & Unterbau', u: 'Steine, Bettung, Tragschicht, Aushub', s: 'pflaster pflastern steine splitt schotter tragschicht bettung aushub einfahrt terrasse',
  f: [F('a', 'Fläche', 'm²', 20), F('sl', 'Stein Länge', 'cm', 20), F('sb', 'Stein Breite', 'cm', 10), F('sd', 'Stein Dicke', 'cm', 8), F('fu', 'Fuge', 'mm', 4), F('bett', 'Bettung (Splitt)', 'cm', 4), F('trag', 'Tragschicht (Schotter)', 'cm', 25), F('vs', 'Verschnitt', '%', 5)],
  r: function (v) { brauche(v, 'a', 'sl', 'sb'); var fu = (v.fu || 0) / 10, je = 1e4 / ((v.sl + fu) * (v.sb + fu)), vs = oder(v.vs, 5), n = auf(v.a * je * (1 + vs / 100)), bett = v.a * (v.bett || 0) / 100, trag = v.a * (v.trag || 0) / 100, tief = (v.sd || 0) + (v.bett || 0) + (v.trag || 0);
    return { wert: n, gross: gz(n), einh: 'Steine', label: 'für ' + zahl(v.a) + ' m² inkl. ' + zahl(vs) + ' % Verschnitt', zeilen: [['Steine je m²', dz(je, 1) + ' Stück'], ['Bettung', zahl(bett, 3) + ' m³ ≈ ' + zahl(bett * 1.6, 3) + ' t Splitt'], ['Tragschicht (verdichtet)', zahl(trag, 3) + ' m³ ≈ ' + zahl(trag * 2.0, 3) + ' t Schotter'], ['Aushubtiefe', zahl(tief) + ' cm'], ['Aushub (fest)', zahl(v.a * tief / 100, 3) + ' m³']],
      schritte: ['Steine je m² = 10 000 / ((Länge + Fuge) · (Breite + Fuge)) = 10 000 / (' + zahl(v.sl + fu) + ' · ' + zahl(v.sb + fu) + ') = ' + zahl(je, 4), 'Anzahl = Fläche · Steine je m² · (1 + Verschnitt) = ' + zahl(v.a * je * (1 + vs / 100), 5) + ' → ' + n, 'Schichten: Volumen = Fläche · Dicke; Splitt ≈ 1,6 t/m³, Schotter verdichtet ≈ 2,0 t/m³'],
      hinweis: 'Richtwerte: Gehweg/Terrasse 15–20 cm Tragschicht, Pkw-Einfahrt 25–40 cm, je nach Boden und Frosttiefe. Gefälle mindestens 2 %. Aushub lockert sich um etwa 25 % auf.' }; } });

K({ id: 'b-daemm', b: 'bau', t: 'Dämmung & U-Wert', u: 'Wärmedurchgang vor und nach dem Dämmen', s: 'dämmung u-wert wärmeleitfähigkeit wls dämmstoff wärmedurchgang fassade dach',
  f: [F('a', 'Fläche', 'm²', 100), F('d', 'Dämmdicke', 'cm', 16), W('wls', 'Wärmeleitstufe', [['0.032', 'WLS 032'], ['0.035', 'WLS 035'], ['0.040', 'WLS 040'], ['0.045', 'WLS 045 (z. B. Holzfaser, Zellulose)']], '0.035'), F('ualt', 'U-Wert des Bauteils vorher (optional)', 'W/m²K', 1.4), F('gt', 'Heizgradtage · 24 / 1000', 'kKh/a', 84)],
  r: function (v) { brauche(v, 'd'); pos(v, 'd', 'Dämmdicke'); var lam = +v.wls, R = v.d / 100 / lam, uS = 1 / R, z = [['Wärmedurchlasswiderstand R', zahl(R, 4) + ' m²K/W'], ['U-Wert nur der Dämmschicht', zahl(uS, 3) + ' W/m²K']], s = ['R = Dicke / λ = ' + zahl(v.d / 100) + ' m / ' + zahl(lam) + ' W/mK = ' + zahl(R, 4) + ' m²K/W'], wert = uS, lab = 'U-Wert der Dämmschicht allein', svg;
    if (v.ualt > 0) { var un = 1 / (1 / v.ualt + R); wert = un; lab = 'U-Wert nach dem Dämmen (vorher ' + zahl(v.ualt) + ')'; z.push(['Wärmeverlust sinkt um', dz((1 - un / v.ualt) * 100, 0) + ' %']); s.push('U neu = 1 / (1 / U alt + R) = 1 / (' + zahl(1 / v.ualt, 4) + ' + ' + zahl(R, 4) + ') = ' + zahl(un, 3) + ' W/m²K');
      if (v.a > 0) { var gt = oder(v.gt, 84), e = (v.ualt - un) * v.a * gt; z.push(['Einsparung (grob)', gz(e) + ' kWh im Jahr']); s.push('Einsparung ≈ (U alt − U neu) · Fläche · ' + zahl(gt) + ' kKh/a = ' + gz(e) + ' kWh/a'); }
      svg = balken([{ l: 'vorher', v: v.ualt, txt: zahl(v.ualt, 3) + ' W/m²K' }, { l: 'nachher', v: un, txt: zahl(un, 3) + ' W/m²K', hl: true }]); }
    if (v.a > 0) z.push(['Dämmstoff-Volumen', zahl(v.a * v.d / 100, 4) + ' m³']);
    return { wert: wert, gross: zahl(wert, 3), einh: 'W/m²K', label: lab, zeilen: z, schritte: s, svg: svg, hinweis: 'Überschlag ohne Wärmebrücken und Übergangswiderstände. Das GEG verlangt bei der Sanierung von Außenwänden höchstens 0,24 W/m²K; Förderprogramme fordern meist 0,20 W/m²K.' }; } });

K({ id: 'b-treppe', b: 'bau', t: 'Treppe', u: 'Steigungen, Auftritt, Lauflänge nach der Schrittmaßregel', s: 'treppe stufen steigung auftritt schrittmaß lauflänge geschosshöhe',
  f: [F('h', 'Geschosshöhe (Fertigboden bis Fertigboden)', 'cm', 275), F('s', 'Wunsch-Steigung', 'cm', 18), F('a', 'Auftritt (leer = aus Schrittmaß 63 cm)', 'cm', null)],
  r: function (v) { brauche(v, 'h', 's'); pos(v, 's', 'Steigung'); var n = Math.max(1, Math.round(v.h / v.s)), s = v.h / n, a = oder(v.a, 63 - 2 * s), sm = 2 * s + a, lauf = (n - 1) * a, win = Math.atan(s / a) * 180 / Math.PI; if (!(a > 0)) throw new Error('Der Auftritt muss größer als 0 sein.');
    var ok = function (x, lo, hi) { return x >= lo && x <= hi ? '✓' : '✗'; };
    return { wert: n, gross: String(n), einh: 'Steigungen', label: dz(s, 1) + ' cm hoch · ' + dz(a, 1) + ' cm Auftritt', zeilen: [['Stufen (Auftritte)', String(n - 1)], ['Lauflänge', zahl(lauf, 4) + ' cm'], ['Neigung', dz(win, 1) + '°'], ['Schrittmaß 2 s + a (59–65 cm)', dz(sm, 1) + ' cm ' + ok(sm, 59, 65)], ['Bequemlichkeit a − s (≈ 12 cm)', dz(a - s, 1) + ' cm'], ['Sicherheit a + s (≈ 46 cm)', dz(a + s, 1) + ' cm']],
      schritte: ['Anzahl = Geschosshöhe / Wunsch-Steigung = ' + zahl(v.h) + ' / ' + zahl(v.s) + ' = ' + zahl(v.h / v.s, 4) + ' → ' + n, 'Steigung s = ' + zahl(v.h) + ' / ' + n + ' = ' + zahl(s, 4) + ' cm', 'Auftritt a = 63 − 2 · s = ' + zahl(63 - 2 * s, 4) + ' cm (Schrittmaßregel)', 'Lauflänge = (Anzahl − 1) · a = ' + (n - 1) + ' · ' + zahl(a, 4) + ' = ' + zahl(lauf, 5) + ' cm'],
      hinweis: 'DIN 18065: in Wohngebäuden mit bis zu zwei Wohnungen Steigung höchstens 20 cm und Auftritt mindestens 23 cm, sonst Steigung 14–19 cm und Auftritt 26–37 cm. Die Landesbauordnung geht vor.' }; } });

K({ id: 'b-angebot', b: 'bau', t: 'Angebot kalkulieren', u: 'Material mit Zuschlag, Lohn, Nachlass, Mehrwertsteuer', breit: true, s: 'angebot kalkulation materialzuschlag stundensatz lohn nachlass mehrwertsteuer rechnung',
  f: [F('mat', 'Material (Einkauf netto)', '€', 850), F('zs', 'Materialzuschlag', '%', 20), F('std', 'Arbeitsstunden', 'h', 12), F('satz', 'Stundensatz netto', '€/h', 65), F('pau', 'Anfahrt / Pauschalen netto', '€', 45), F('nl', 'Nachlass', '%', 0), W('mwst', 'Mehrwertsteuer', [['19', '19 %'], ['7', '7 %'], ['0', 'ohne (z. B. § 13b UStG)']], '19')],
  r: function (v) { var mat = v.mat || 0, zs = mat * (v.zs || 0) / 100, lohn = (v.std || 0) * (v.satz || 0), pau = v.pau || 0, sum = mat + zs + lohn + pau; if (!(sum > 0)) throw new LeerFehler('Material oder Arbeitszeit eingeben.'); var nl = sum * (v.nl || 0) / 100, net = sum - nl, st = net * +v.mwst / 100, bru = net + st;
    var z = [['Material inkl. ' + zahl(v.zs || 0) + ' % Zuschlag', geld(mat + zs)], ['Lohn (' + zahl(v.std || 0) + ' h × ' + geld(v.satz || 0) + ')', geld(lohn)], ['Pauschalen', geld(pau)]]; if (nl) z.push(['Nachlass ' + zahl(v.nl) + ' %', '− ' + geld(nl)]); z.push(['Netto', geld(net)], ['MwSt. ' + v.mwst + ' %', geld(st)], ['Brutto', geld(bru)], ['Rohertrag über dem Materialeinkauf', geld(net - mat)]);
    return { wert: bru, gross: fix(bru, 2), einh: '€', label: 'Angebotssumme brutto', zeilen: z, schritte: ['Material = Einkauf · (1 + Zuschlag) = ' + fix(mat, 2) + ' · ' + zahl(1 + (v.zs || 0) / 100) + ' = ' + fix(mat + zs, 2) + ' €', 'Lohn = Stunden · Stundensatz = ' + zahl(v.std || 0) + ' · ' + fix(v.satz || 0, 2) + ' = ' + fix(lohn, 2) + ' €', 'Netto = Summe − Nachlass = ' + fix(sum, 2) + ' − ' + fix(nl, 2) + ' = ' + fix(net, 2) + ' €', 'Brutto = Netto · (1 + ' + v.mwst + ' %) = ' + fix(bru, 2) + ' €'],
      svg: ring([{ l: 'Material', v: mat, txt: geld(mat) }, { l: 'Zuschlag', v: zs, txt: geld(zs) }, { l: 'Lohn', v: lohn, txt: geld(lohn) }, { l: 'Pauschalen', v: pau, txt: geld(pau) }, { l: 'MwSt.', v: st, txt: geld(st) }], { mitte: geld(bru), unter: 'brutto' }), hinweis: 'Rechenhilfe für den Überschlag – ersetzt nicht die Kalkulation des Betriebs.' }; } });

/* ---------- Geld ---------- */
function est2026(x) { x = Math.floor(x); if (x <= 12348) return 0; if (x <= 17799) { var y = (x - 12348) / 1e4; return Math.floor((914.51 * y + 1400) * y); } if (x <= 69878) { var z = (x - 17799) / 1e4; return Math.floor((173.1 * z + 2397) * z + 1034.87); } if (x <= 277825) return Math.floor(0.42 * x - 11135.63); return Math.floor(0.45 * x - 19470.38); }
K({ id: 'ge-netto', b: 'geld', t: 'Brutto → Netto (Schätzung)', u: 'Lohnsteuer und Sozialabgaben 2026, gesetzlich versichert', breit: true, s: 'brutto netto lohn gehalt lohnsteuer sozialabgaben steuerklasse nettolohn',
  f: [F('b', 'Bruttolohn im Monat', '€', 3500), W('kl', 'Steuerklasse', [['1', 'I oder IV'], ['2', 'II (alleinerziehend)'], ['3', 'III']], '1'), F('kind', 'Kinder (für die Pflegeversicherung)', '', 0), F('zus', 'Zusatzbeitrag der Krankenkasse', '%', 2.9), W('ki', 'Kirchensteuer', [['0', 'keine'], ['9', '9 %'], ['8', '8 % (Bayern, Baden-Württemberg)']], '0')],
  r: function (v) { brauche(v, 'b'); pos(v, 'b', 'Bruttolohn'); var b = v.b, kvB = Math.min(b, 5812.5), rvB = Math.min(b, 8450), zus = oder(v.zus, 2.9), kind = Math.max(0, Math.round(v.kind || 0));
    var pvS = 1.8 + (kind === 0 ? 0.6 : 0) - (kind >= 2 ? Math.min(kind - 1, 4) * 0.25 : 0), kv = kvB * (7.3 + zus / 2) / 100, pv = kvB * pvS / 100, rv = rvB * 0.093, av = rvB * 0.013, sv = kv + pv + rv + av;
    var J = b * 12, kvV = 12 * kvB * (7.0 + zus / 2) / 100, pvV = 12 * pv, avV = 12 * av, vp = 12 * rv + Math.max(kvV + pvV, Math.min(kvV + pvV + avV, 1900)), zve = Math.max(0, J - 1230 - 36 - vp - (v.kl === '2' ? 4260 : 0));
    var est = v.kl === '3' ? 2 * est2026(zve / 2) : est2026(zve), fg = v.kl === '3' ? 40700 : 20350, soli = est > fg ? Math.min(0.055 * est, 0.119 * (est - fg)) : 0, kist = est * +v.ki / 100, lst = est / 12, st = (est + soli + kist) / 12, netto = b - sv - st;
    var z = [['Lohnsteuer', geld(lst)]]; if (soli) z.push(['Solidaritätszuschlag', geld(soli / 12)]); if (kist) z.push(['Kirchensteuer', geld(kist / 12)]);
    z.push(['Krankenversicherung (' + dz(7.3 + zus / 2, 2) + ' %)', geld(kv)], ['Pflegeversicherung (' + dz(pvS, 2) + ' %)', geld(pv)], ['Rentenversicherung (9,3 %)', geld(rv)], ['Arbeitslosenversicherung (1,3 %)', geld(av)], ['Abzüge gesamt', geld(sv + st) + ' = ' + dz((sv + st) / b * 100, 1) + ' %'], ['Netto im Jahr', geld(netto * 12)]);
    return { wert: netto, gross: fix(netto, 2), einh: '€', label: 'geschätztes Netto im Monat', zeilen: z,
      schritte: ['Sozialabgaben bis zur Beitragsbemessungsgrenze (KV/PV 5.812,50 €, RV/AV 8.450 € im Monat): ' + geld(sv), 'Zu versteuern im Jahr ≈ 12 · Brutto − 1.230 € Arbeitnehmer-Pauschbetrag − 36 € − Vorsorgepauschale (' + geld(vp) + ')' + (v.kl === '2' ? ' − 4.260 € Entlastungsbetrag' : '') + ' = ' + geld(zve), 'Einkommensteuer nach § 32a EStG 2026' + (v.kl === '3' ? ' (Splitting: 2 · Steuer auf die Hälfte)' : '') + ': ' + geld(est) + ' im Jahr = ' + geld(lst) + ' im Monat', 'Netto = Brutto − Steuern − Sozialabgaben = ' + fix(b, 2) + ' − ' + fix(st, 2) + ' − ' + fix(sv, 2) + ' = ' + fix(netto, 2) + ' €'],
      svg: ring([{ l: 'Netto', v: Math.max(0, netto), txt: geld(netto) }, { l: 'Steuern', v: st, txt: geld(st) }, { l: 'Sozialabgaben', v: sv, txt: geld(sv) }], { mitte: dz(netto / b * 100, 0) + ' %', unter: 'bleiben' }),
      hinweis: 'Schätzung mit den Werten für 2026 (Tarif § 32a EStG, Beitragssätze und Bemessungsgrenzen, durchschnittlicher Zusatzbeitrag 2,9 %). Ohne Freibeträge, Kinderfreibetrag bei Soli/Kirchensteuer, Sachbezüge, Steuerklassen V/VI und Sachsen-Sonderregel der Pflegeversicherung. Verbindlich ist die Lohnabrechnung; genau rechnet der Lohnsteuerrechner des Bundesfinanzministeriums (bmf-steuerrechner.de).' }; } });

K({ id: 'ge-miete', b: 'geld', t: 'Miete je Quadratmeter', u: 'kalt, warm und Anteil am Einkommen', s: 'miete quadratmeter kaltmiete warmmiete nebenkosten mietbelastung',
  f: [F('k', 'Kaltmiete', '€', 650), F('nk', 'Nebenkosten', '€', 180), F('a', 'Wohnfläche', 'm²', 72), F('ein', 'Haushalts-Netto (optional)', '€', null)],
  r: function (v) { brauche(v, 'k', 'a'); pos(v, 'a', 'Wohnfläche'); var w = v.k + (v.nk || 0), z = [['Warmmiete', geld(w)], ['warm je m²', geld(w / v.a)], ['Nebenkosten je m²', geld((v.nk || 0) / v.a)], ['Miete im Jahr (warm)', geld(w * 12)]], svg;
    if (v.ein > 0) { z.push(['Anteil kalt am Netto', dz(v.k / v.ein * 100, 1) + ' %'], ['Anteil warm am Netto', dz(w / v.ein * 100, 1) + ' %']); svg = skala(w / v.ein * 100, [{ bis: 30, l: 'bis 30 %' }, { bis: 40, l: '30–40 %' }, { bis: 60, l: 'über 40 %' }], 0, 60, { titel: 'Mietbelastung warm', txt: dz(w / v.ein * 100, 0) + ' %' }); }
    return { wert: v.k / v.a, gross: fix(v.k / v.a, 2), einh: '€/m²', label: 'Kaltmiete je Quadratmeter', zeilen: z, schritte: ['Kaltmiete je m² = ' + fix(v.k, 2) + ' € / ' + zahl(v.a) + ' m² = ' + fix(v.k / v.a, 2) + ' €/m²', 'Warmmiete = Kaltmiete + Nebenkosten = ' + fix(w, 2) + ' €'], svg: svg, hinweis: 'Als Faustregel gilt eine Warmmiete bis etwa 30 % des Nettoeinkommens als gut tragbar; ab 40 % spricht die Statistik von Überbelastung.' }; } });

K({ id: 'ge-auto', b: 'geld', t: 'Autokosten je Kilometer', u: 'Wertverlust, Sprit, Fixkosten', breit: true, s: 'auto autokosten kilometer wertverlust versicherung kfz unterhalt',
  f: [F('kauf', 'Kaufpreis', '€', 22000), F('rest', 'Restwert am Ende', '€', 9000), F('j', 'Haltedauer', 'Jahre', 6), F('km', 'Fahrleistung', 'km/Jahr', 12000), F('vb', 'Verbrauch', 'l bzw. kWh/100 km', 6.5), F('pr', 'Preis je Liter / kWh', '€', 1.75), F('vers', 'Versicherung', '€/Jahr', 650), F('st', 'Kfz-Steuer', '€/Jahr', 120), F('wa', 'Wartung, Reifen, TÜV', '€/Jahr', 700), F('so', 'Sonstiges (Stellplatz, Pflege)', '€/Jahr', 0)],
  r: function (v) { brauche(v, 'kauf', 'j', 'km'); pos(v, 'j', 'Haltedauer'); pos(v, 'km', 'Fahrleistung'); var wv = (v.kauf - (v.rest || 0)) / v.j, sp = v.km / 100 * (v.vb || 0) * (v.pr || 0), fx = (v.vers || 0) + (v.st || 0), wa = (v.wa || 0) + (v.so || 0), ges = wv + sp + fx + wa, je = ges / v.km;
    return { wert: je, gross: fix(je, 2), einh: '€/km', label: 'Gesamtkosten je Kilometer', zeilen: [['im Monat', geld(ges / 12)], ['im Jahr', geld(ges)], ['Wertverlust', geld(wv) + ' im Jahr'], ['Kraftstoff / Strom', geld(sp) + ' im Jahr = ' + fix(sp / v.km * 100, 2) + ' € je 100 km'], ['über die ganze Haltedauer', geld(ges * v.j)]],
      schritte: ['Wertverlust = (Kaufpreis − Restwert) / Jahre = (' + fix(v.kauf, 2) + ' − ' + fix(v.rest || 0, 2) + ') / ' + zahl(v.j) + ' = ' + fix(wv, 2) + ' €', 'Kraftstoff = km / 100 · Verbrauch · Preis = ' + fix(sp, 2) + ' €', 'Kosten je km = Summe / Fahrleistung = ' + fix(ges, 2) + ' / ' + gz(v.km) + ' = ' + fix(je, 3) + ' €'],
      svg: ring([{ l: 'Wertverlust', v: Math.max(0, wv), txt: geld(wv) }, { l: 'Kraftstoff', v: sp, txt: geld(sp) }, { l: 'Versicherung + Steuer', v: fx, txt: geld(fx) }, { l: 'Wartung + Sonstiges', v: wa, txt: geld(wa) }], { mitte: fix(je * 100, 0) + ' ct', unter: 'je km' }), hinweis: 'Ohne Finanzierungskosten und entgangene Zinsen. Zum Vergleich: Die steuerliche Kilometerpauschale für Dienstfahrten beträgt 0,30 €/km.' }; } });

K({ id: 'ge-pv', b: 'geld', t: 'Photovoltaik: Ertrag & Amortisation', u: 'Eigenverbrauch, Einspeisung, Rückzahldauer', breit: true, s: 'photovoltaik pv solar solaranlage einspeisevergütung eigenverbrauch amortisation balkonkraftwerk',
  f: [F('kwp', 'Anlagengröße', 'kWp', 8), F('er', 'Ertrag je kWp', 'kWh/Jahr', 950), F('vb', 'Stromverbrauch im Haus', 'kWh/Jahr', 4000), F('ev', 'Eigenverbrauchsanteil', '%', 30), F('sp', 'Strompreis', 'ct/kWh', 35), F('eg', 'Einspeisevergütung', 'ct/kWh', 7.7), F('ko', 'Anschaffung (optional)', '€', 12000)],
  r: function (v) { brauche(v, 'kwp', 'er'); var E = v.kwp * v.er, ev = Math.min(E * oder(v.ev, 30) / 100, v.vb > 0 ? v.vb : Infinity), ein = E - ev, g1 = ev * (v.sp || 0) / 100, g2 = ein * (v.eg || 0) / 100, g = g1 + g2;
    var z = [['Erzeugung', gz(E) + ' kWh im Jahr'], ['Selbst verbraucht', gz(ev) + ' kWh → ' + geld(g1) + ' gespart'], ['Eingespeist', gz(ein) + ' kWh → ' + geld(g2) + ' Vergütung']]; if (v.vb > 0) z.push(['Autarkiegrad', dz(ev / v.vb * 100, 0) + ' %']); var s = ['Erzeugung = kWp · Ertrag = ' + zahl(v.kwp) + ' · ' + zahl(v.er) + ' = ' + gz(E) + ' kWh', 'Nutzen = Eigenverbrauch · Strompreis + Einspeisung · Vergütung = ' + fix(g1, 2) + ' + ' + fix(g2, 2) + ' = ' + fix(g, 2) + ' €'], kurs;
    if (v.ko > 0 && g > 0) { var jahre = v.ko / g; z.push(['Amortisation', dz(jahre, 1) + ' Jahre'], ['Überschuss nach 20 Jahren', geld(g * 20 - v.ko)]); s.push('Amortisation = Anschaffung / Nutzen im Jahr = ' + fix(v.ko, 2) + ' / ' + fix(g, 2) + ' = ' + dz(jahre, 1) + ' Jahre'); var x = [], w = []; for (var i = 0; i <= 25; i++) { x.push(i ? i + '. J' : 'Start'); w.push(rund(g * i - v.ko, 10)); } kurs = { x: x, s: [{ n: 'Saldo', w: w, f: 'var(--rz-f1)' }], fmt: 'geld', titel: 'Saldo über 25 Jahre' }; }
    return { wert: g, gross: fix(g, 2), einh: '€', label: 'Nutzen im Jahr', zeilen: z, schritte: s, kurs: kurs, svg: ring([{ l: 'Eigenverbrauch', v: ev, txt: gz(ev) + ' kWh' }, { l: 'Einspeisung', v: ein, txt: gz(ein) + ' kWh' }], { mitte: gz(E), unter: 'kWh' }),
      hinweis: 'Vergütung 7,70 ct/kWh: fester Satz für Dachanlagen bis 10 kWp mit Teileinspeisung bei Inbetriebnahme vom 1.8.2026 bis 31.1.2027 (Bundesnetzagentur); für Neuanlagen ab 2027 ist eine Neuregelung in Beratung. Ohne Speicher sind 25–35 % Eigenverbrauch üblich, mit Speicher 50–70 %. Ohne Wartung, Zählerkosten und Leistungsabnahme der Module.' }; } });

K({ id: 'ge-entnahme', b: 'geld', t: 'Entnahmeplan', u: 'Wie lange reicht das Ersparte?', breit: true, s: 'entnahme entnahmeplan rente kapitalverzehr ausstieg vermögen reicht',
  f: [F('k', 'Kapital', '€', 200000), F('e', 'Entnahme im Monat (heutige Kaufkraft)', '€', 1000), F('p', 'Rendite', '% p. a.', 3), F('i', 'Inflation (Entnahme steigt jährlich)', '% p. a.', 2)],
  r: function (v) { brauche(v, 'k', 'e'); pos(v, 'e', 'Entnahme'); var p = (v.p || 0) / 100, inf = (v.i || 0) / 100, K = v.k, e = v.e, m = 0, sum = 0, x = ['Start'], w = [K], mz = Math.pow(1 + p, 1 / 12) - 1, max = 1200;
    while (K > 0 && m < max) { if (m && m % 12 === 0) e *= 1 + inf; K = K * (1 + mz) - e; sum += K < 0 ? Math.max(0, e + K) : e; m++; if (m % 12 === 0) { x.push(m / 12 + '. J'); w.push(rund(Math.max(0, K), 10)); } }
    var ewig = m >= max, jahre = m / 12, real = (1 + p) / (1 + inf) - 1;
    if (!ewig && m % 12) { x.push(dz(jahre, 1) + ' J'); w.push(0); }
    return { wert: jahre, gross: ewig ? 'über 100' : dz(jahre, 1), einh: 'Jahre', label: ewig ? 'Das Kapital wird nicht aufgezehrt' : 'bis das Kapital aufgebraucht ist', zeilen: [['Entnommen insgesamt', ewig ? '–' : geld(sum)], ['Reale Rendite (nach Inflation)', dz(real * 100, 2) + ' %'], ['Dauerhaft entnehmbar (Kapital bleibt real erhalten)', real > 0 ? geld(v.k * real / 12) + ' im Monat' : '–'], ['Entnahme im Jahr / Kapital', dz(v.e * 12 / v.k * 100, 1) + ' %']],
      schritte: ['Monatszins = (1 + Rendite)^(1/12) − 1 = ' + zahl(mz * 100, 4) + ' %', 'Jeden Monat: Kapital · (1 + Monatszins) − Entnahme; die Entnahme steigt jedes Jahr um die Inflation', 'Ergebnis: ' + (ewig ? 'nach 100 Jahren ist noch Kapital da' : m + ' Monate = ' + dz(jahre, 1) + ' Jahre')],
      kurs: { x: ewig ? x.slice(0, 61) : x, s: [{ n: 'Kapital', w: ewig ? w.slice(0, 61) : w, f: 'var(--rz-f1)' }], fmt: 'geld', titel: 'Kapitalverlauf' }, hinweis: 'Gleichmäßige Rendite ohne Schwankungen, Steuern und Kosten – echte Verläufe weichen ab. Reine Rechenhilfe, keine Anlage- oder Finanzberatung.' }; } });

/* ---------- Gesundheit ---------- */
var EIW = [['e', 'Erwachsene (0,8 g je kg)', 0.8, 0.8], ['s', 'ab 65 Jahren (1,0 g je kg)', 1.0, 1.0], ['a', 'regelmäßiger Ausdauersport (1,2–1,6 g je kg)', 1.2, 1.6], ['k', 'Kraftsport / Muskelaufbau (1,6–2,0 g je kg)', 1.6, 2.0]];
K({ id: 'gs-eiweiss', b: 'gesundheit', t: 'Eiweißbedarf', u: 'Richtwert je Tag nach Körpergewicht', s: 'eiweiß protein eiweißbedarf proteinbedarf',
  f: [F('kg', 'Körpergewicht', 'kg', 80), W('z', 'Situation', wahlOpt(EIW), 'e')],
  r: function (v) { brauche(v, 'kg'); pos(v, 'kg', 'Gewicht'); var z = zeile(EIW, v.z), lo = v.kg * z[2], hi = v.kg * z[3], txt = lo === hi ? gz(lo) : gz(lo) + '–' + gz(hi);
    return { wert: lo, gross: txt, einh: 'g Eiweiß am Tag', label: z[1], zeilen: [['bei 3 Mahlzeiten', (lo === hi ? gz(lo / 3) : gz(lo / 3) + '–' + gz(hi / 3)) + ' g je Mahlzeit'], ['Energie aus Eiweiß', gz(lo * 4.1) + (lo === hi ? '' : '–' + gz(hi * 4.1)) + ' kcal']], schritte: ['Bedarf = Körpergewicht · Richtwert = ' + zahl(v.kg) + ' kg · ' + zahl(z[2]) + (lo === hi ? '' : ' bis ' + zahl(z[3])) + ' g/kg = ' + txt + ' g'],
      svg: balken(EIW.map(function (x) { return { l: x[1].replace(/ \(.*/, ''), v: v.kg * x[3], txt: (x[2] === x[3] ? gz(v.kg * x[2]) : gz(v.kg * x[2]) + '–' + gz(v.kg * x[3])) + ' g', hl: x[0] === z[0] }; })),
      hinweis: 'Referenzwerte der Deutschen Gesellschaft für Ernährung (0,8 g/kg, ab 65 Jahren 1,0 g/kg als Schätzwert); Sport-Spannen nach dem Positionspapier der DGE-Arbeitsgruppe Sporternährung. Bezogen auf Normalgewicht. Bei Nierenerkrankungen die Eiweißmenge ärztlich abklären.' }; } });

K({ id: 'gs-koffein', b: 'gesundheit', t: 'Koffein-Abbau', u: 'Wie viel ist nach x Stunden noch im Körper?', s: 'koffein kaffee halbwertszeit espresso energydrink schlaf', breit: true,
  f: [F('mg', 'Koffein aufgenommen', 'mg', 180), F('t', 'Stunden seitdem', 'h', 6), F('hw', 'Halbwertszeit', 'h', 5), F('gr', 'Schwelle „kaum noch spürbar“', 'mg', 50)],
  r: function (v) { brauche(v, 'mg', 't'); var hw = oder(v.hw, 5); if (!(hw > 0)) throw new Error('Die Halbwertszeit muss größer als 0 sein.'); var rest = v.mg * Math.pow(0.5, v.t / hw), gr = oder(v.gr, 50), tg = v.mg > gr && gr > 0 ? hw * Math.log(v.mg / gr) / Math.LN2 : 0, x = [], w = [];
    for (var i = 0; i <= 24; i++) { x.push(i + ' h'); w.push(rund(v.mg * Math.pow(0.5, i / hw), 6)); }
    return { wert: rest, gross: gz(rest), einh: 'mg', label: 'noch im Körper nach ' + zahl(v.t) + ' Stunden', zeilen: [['Abgebaut', dz((1 - rest / v.mg) * 100, 0) + ' %'], ['Unter ' + zahl(gr) + ' mg nach', stdText(tg)], ['Zum Vergleich', 'Filterkaffee 200 ml ≈ 90 mg · Espresso ≈ 80 mg · Energydrink 250 ml ≈ 80 mg · Schwarztee 200 ml ≈ 45 mg · Cola 330 ml ≈ 35 mg']],
      schritte: ['Rest = Menge · 0,5^(Zeit / Halbwertszeit) = ' + zahl(v.mg) + ' · 0,5^(' + zahl(v.t) + ' / ' + zahl(hw) + ') = ' + zahl(rest, 4) + ' mg', 'Zeit bis zur Schwelle = Halbwertszeit · log₂(Menge / Schwelle) = ' + zahl(tg, 3) + ' h'], kurs: { x: x, s: [{ n: 'Koffein (mg)', w: w, f: 'var(--rz-f3)' }], titel: 'Abbau über 24 Stunden' },
      hinweis: 'Die Halbwertszeit liegt bei gesunden Erwachsenen meist zwischen 3 und 7 Stunden (kürzer bei Rauchern, deutlich länger in der Schwangerschaft und mit manchen Medikamenten). Die EFSA nennt bis 200 mg auf einmal und 400 mg am Tag als unbedenklich für gesunde Erwachsene, in Schwangerschaft und Stillzeit 200 mg am Tag.' }; } });

K({ id: 'gs-alkohol', b: 'gesundheit', t: 'Alkohol: Promille-Schätzung', u: 'Widmark-Formel und Abbauzeit', s: 'alkohol promille widmark abbau blutalkohol bier wein', breit: true,
  f: [F('n', 'Anzahl Getränke', '', 2), F('ml', 'Menge je Getränk', 'ml', 500), F('vol', 'Alkoholgehalt', 'Vol.-%', 5), F('kg', 'Körpergewicht', 'kg', 80), W('g', 'Verteilungsfaktor', [['m', 'Mann (0,68)'], ['w', 'Frau (0,55)']], 'm'), F('t', 'Stunden seit Trinkbeginn', 'h', 2), F('ab', 'Abbau je Stunde', '‰', 0.15)],
  r: function (v) { brauche(v, 'n', 'ml', 'vol', 'kg'); pos(v, 'kg', 'Gewicht'); var g = v.n * v.ml * v.vol / 100 * 0.8, r = v.g === 'w' ? 0.55 : 0.68, c0 = g * 0.9 / (v.kg * r), ab = oder(v.ab, 0.15), t = v.t || 0, c = Math.max(0, c0 - ab * t), x = [], w = [], T = Math.min(48, Math.ceil(c0 / 0.1) + 1);
    for (var i = 0; i <= T; i++) { x.push(i + ' h'); w.push(rund(Math.max(0, c0 - ab * i), 4)); }
    return { wert: c, gross: dz(c, 2), einh: '‰', label: 'geschätzt nach ' + zahl(t) + ' Stunden', zeilen: [['Reiner Alkohol', zahl(g, 3) + ' g'], ['Rechnerischer Höchstwert', dz(c0, 2) + ' ‰'], ['Bei ' + zahl(ab) + ' ‰/h auf 0 nach', stdText(c0 / ab) + ' ab Trinkbeginn'], ['Bei langsamem Abbau (0,1 ‰/h) auf 0 nach', stdText(c0 / 0.1) + ' ab Trinkbeginn']],
      schritte: ['Alkohol in g = Menge in ml · Vol.-% / 100 · 0,8 g/ml = ' + zahl(g, 4) + ' g', 'Widmark: Promille = Alkohol · 0,9 / (Gewicht · Faktor) = ' + zahl(g, 4) + ' · 0,9 / (' + zahl(v.kg) + ' · ' + zahl(r) + ') = ' + dz(c0, 2) + ' ‰ (10 % Resorptionsverlust)', 'Abbau: ' + dz(c0, 2) + ' − ' + zahl(ab) + ' · ' + zahl(t) + ' = ' + dz(c, 2) + ' ‰'], kurs: { x: x, s: [{ n: 'Promille', w: w, f: 'var(--rz-f5)' }], titel: 'Geschätzter Verlauf' },
      hinweis: 'Sehr grobe Schätzung: Der echte Wert hängt von Körperbau, Essen, Trinktempo und Gesundheit ab und kann deutlich abweichen. Nicht geeignet, um die Fahrtüchtigkeit zu beurteilen – wer getrunken hat, fährt nicht. Abbau lässt sich nicht beschleunigen. Hilfe bei Fragen zum eigenen Trinken: Sucht & Drogen Hotline 01806 313031.' }; } });

K({ id: 'gs-schlaf', b: 'gesundheit', t: 'Schlafzyklen', u: 'Wann ins Bett, um zu einer bestimmten Zeit aufzustehen?', s: 'schlaf schlafzyklus schlafenszeit aufstehen wecker einschlafen',
  f: [T('auf', 'Aufstehen um', '06:00', { kurz: true }), F('zy', 'Länge eines Zyklus', 'min', 90), F('ein', 'Einschlafdauer', 'min', 15)],
  r: function (v) { var a = uhrLesen(v.auf); if (a == null) throw new LeerFehler('Uhrzeit eingeben, z. B. 06:00.'); var zy = oder(v.zy, 90), ein = oder(v.ein, 15); if (!(zy > 0)) throw new Error('Die Zykluslänge muss größer als 0 sein.');
    var z = [6, 5, 4, 3].map(function (n) { return [n + ' Zyklen = ' + stdText(n * zy / 60) + ' Schlaf', 'ins Bett um ' + uhr(a - n * zy - ein)]; });
    return { wert: a - 5 * zy - ein, gross: uhr(a - 5 * zy - ein), einh: 'Uhr', label: 'ins Bett für 5 Zyklen (' + stdText(5 * zy / 60) + ' Schlaf)', zeilen: z, schritte: ['Zubettgehzeit = Aufstehzeit − Zyklen · Zykluslänge − Einschlafdauer', uhr(a) + ' − 5 · ' + zahl(zy) + ' min − ' + zahl(ein) + ' min = ' + uhr(a - 5 * zy - ein) + ' Uhr'],
      hinweis: 'Ein Schlafzyklus dauert im Mittel etwa 90 Minuten, einzeln zwischen 70 und 110 – die Rechnung ist eine Orientierung. Fachgesellschaften empfehlen Erwachsenen mindestens 7 Stunden Schlaf.' }; } });

var PZONEN = [[50, 60, 'sehr leicht (Erholung)'], [60, 70, 'leicht (Grundlagenausdauer)'], [70, 80, 'mittel (aerober Bereich)'], [80, 90, 'hart (Schwellenbereich)'], [90, 100, 'maximal']];
K({ id: 'gs-puls', b: 'gesundheit', t: 'Pulsbereiche', u: 'Maximalpuls und Trainingszonen', s: 'puls herzfrequenz maximalpuls trainingszonen karvonen ruhepuls',
  f: [F('alter', 'Alter', 'Jahre', 45), F('ruhe', 'Ruhepuls (optional, für Karvonen)', '/min', null), W('f', 'Formel für den Maximalpuls', [['t', '208 − 0,7 · Alter (Tanaka)'], ['k', '220 − Alter (klassisch)']], 't'), F('max', 'gemessener Maximalpuls (optional)', '/min', null)],
  r: function (v) { brauche(v, 'alter'); var max = v.max > 0 ? v.max : v.f === 'k' ? 220 - v.alter : 208 - 0.7 * v.alter, ru = v.ruhe > 0 ? v.ruhe : null, P = function (p) { return ru ? ru + (max - ru) * p / 100 : max * p / 100; };
    return { wert: max, gross: gz(max), einh: 'Schläge/min', label: v.max > 0 ? 'gemessener Maximalpuls' : 'geschätzter Maximalpuls', zeilen: PZONEN.map(function (z) { return [z[0] + '–' + z[1] + ' % · ' + z[2], gz(P(z[0])) + '–' + gz(P(z[1])) + ' /min']; }),
      schritte: [v.max > 0 ? 'Maximalpuls gemessen: ' + gz(max) : v.f === 'k' ? 'HFmax = 220 − Alter = 220 − ' + zahl(v.alter) + ' = ' + gz(max) : 'HFmax = 208 − 0,7 · Alter = 208 − 0,7 · ' + zahl(v.alter) + ' = ' + zahl(max, 4), ru ? 'Karvonen: Zielpuls = Ruhepuls + (HFmax − Ruhepuls) · Prozent' : 'Zielpuls = HFmax · Prozent'],
      svg: balken(PZONEN.map(function (z, i) { return { l: z[0] + '–' + z[1] + ' %', v: P(z[1]), txt: gz(P(z[0])) + '–' + gz(P(z[1])), f: FARB[[1, 0, 5, 2, 4][i]] }; })),
      hinweis: 'Schätzformeln treffen den einzelnen Menschen oft nur auf ± 10 Schläge. Bei Herz-Kreislauf-Erkrankungen oder Medikamenten wie Betablockern die Belastung ärztlich festlegen lassen.' }; } });

/* ---------- Kalender: Sonne ---------- */
var ORTE = [['sb', 'Saarbrücken', 49.24, 6.99], ['b', 'Berlin', 52.52, 13.4], ['hh', 'Hamburg', 53.55, 9.99], ['m', 'München', 48.14, 11.58], ['k', 'Köln', 50.94, 6.96], ['f', 'Frankfurt am Main', 50.11, 8.68], ['s', 'Stuttgart', 48.78, 9.18], ['dd', 'Dresden', 51.05, 13.74], ['l', 'Leipzig', 51.34, 12.37], ['w', 'Wien', 48.21, 16.37], ['z', 'Zürich', 47.37, 8.54], ['x', 'eigene Koordinaten', 49.24, 6.99]];
function sonne(J, lat, lon, hoehe) {
  var rad = Math.PI / 180, n = J - 2451545 + 0.0008, js = n - lon / 360, M = mod(357.5291 + 0.98560028 * js, 360), C = 1.9148 * Math.sin(M * rad) + 0.02 * Math.sin(2 * M * rad) + 0.0003 * Math.sin(3 * M * rad), lam = mod(M + C + 180 + 102.9372, 360);
  var jt = 2451545 + js + 0.0053 * Math.sin(M * rad) - 0.0069 * Math.sin(2 * lam * rad), dek = Math.asin(Math.sin(lam * rad) * Math.sin(23.4397 * rad)), co = (Math.sin(hoehe * rad) - Math.sin(lat * rad) * Math.sin(dek)) / (Math.cos(lat * rad) * Math.cos(dek));
  var hmax = 90 - Math.abs(lat - dek / rad);
  if (co > 1) return { mittag: jt, nie: true, hmax: hmax }; if (co < -1) return { mittag: jt, immer: true, hmax: hmax };
  var w = Math.acos(co) / rad; return { mittag: jt, auf: jt - w / 360, unter: jt + w / 360, hmax: hmax };
}
function jdUhr(JD, tz) { var ms = (JD - 2440587.5) * 864e5, off = tzVersatz(tz, ms), d = new Date(ms + off * 6e4); return uhr(d.getUTCHours() * 60 + d.getUTCMinutes() + (d.getUTCSeconds() >= 30 ? 1 : 0)); }
K({ id: 'k-sonne', b: 'kalender', t: 'Sonnenauf- & -untergang', u: 'Tageslänge und Dämmerung für Ort und Datum', s: 'sonnenaufgang sonnenuntergang tageslänge dämmerung sonne',
  f: [D('d', 'Datum', ''), W('ort', 'Ort', wahlOpt(ORTE), 'sb'), F('lat', 'Breite (Nord +)', '°', 49.24, { nur: { ort: ['x'] } }), F('lon', 'Länge (Ost +)', '°', 6.99, { nur: { ort: ['x'] } })],
  r: function (v, ctx) { var d = datumOderHeute(v, 'd', ctx, 'g'), o = zeile(ORTE, v.ort), lat = v.ort === 'x' ? v.lat : o[2], lon = v.ort === 'x' ? v.lon : o[3]; if (lat == null || lon == null || Math.abs(lat) > 90 || Math.abs(lon) > 180) throw new Error('Koordinaten prüfen (Breite −90 bis 90, Länge −180 bis 180).');
    var J = jdnG(d.y, d.m, d.d), tz = 'Europe/Berlin', s = sonne(J, lat, lon, -0.833), dm = sonne(J, lat, lon, -6), name = v.ort === 'x' ? dz(lat, 2) + '° / ' + dz(lon, 2) + '°' : o[1];
    if (s.nie || s.immer) return { wert: 0, gross: s.nie ? 'Polarnacht' : 'Polartag', label: name + ' · ' + datumLang(d), zeilen: [['Sonnenhöchststand', jdUhr(s.mittag, tz) + ' Uhr']] };
    var len = (s.unter - s.auf) * 24;
    return { wert: len, gross: jdUhr(s.auf, tz) + ' – ' + jdUhr(s.unter, tz), einh: 'Uhr', label: name + ' · ' + datumLang(d), zeilen: [['Tageslänge', stdText(len)], ['Sonnenhöchststand', jdUhr(s.mittag, tz) + ' Uhr, ' + dz(s.hmax, 1) + '° über dem Horizont'], ['Bürgerliche Dämmerung', dm.auf ? 'ab ' + jdUhr(dm.auf, tz) + ' · bis ' + jdUhr(dm.unter, tz) + ' Uhr' : 'die ganze Nacht']],
      schritte: ['Sonnenstand nach der Näherung der US-Wetterbehörde NOAA aus der Julianischen Tageszahl', 'Aufgang und Untergang: Mittelpunkt der Sonne 0,833° unter dem Horizont (Lichtbrechung und Sonnenradius)', 'Bürgerliche Dämmerung: Sonne 6° unter dem Horizont'],
      svg: skala(len, [{ bis: 8, l: 'kurz' }, { bis: 12, l: '' }, { bis: 16, l: '' }, { bis: 24, l: 'lang' }], 0, 24, { titel: 'Tageslänge in Stunden', txt: stdText(len) }), hinweis: 'Zeiten in mitteleuropäischer Zeit (im Sommer Sommerzeit), flacher Horizont, Genauigkeit etwa ± 2 Minuten.' }; } });

/* ---------- Musik ---------- */
var TON_D = ['C', 'Cis', 'D', 'Dis', 'E', 'F', 'Fis', 'G', 'Gis', 'A', 'B', 'H'], TON_I = ['C', 'C♯', 'D', 'E♭', 'E', 'F', 'F♯', 'G', 'A♭', 'A', 'B♭', 'B'], TON_NR = { c: 0, d: 2, e: 4, f: 5, g: 7, a: 9, h: 11, b: 11 };
K({ id: 'm-tempo', b: 'musik', t: 'Tempo ↔ Millisekunden', u: 'Notenlängen für Delay, Hall und Klick', s: 'tempo bpm millisekunden delay notenwert metronom',
  f: [F('bpm', 'Tempo', 'BPM', 120), F('takt', 'Schläge je Takt', '', 4)],
  r: function (v) { brauche(v, 'bpm'); pos(v, 'bpm', 'Tempo'); var q = 60000 / v.bpm, t = oder(v.takt, 4), L = [['Halbe', 2], ['Viertel', 1], ['punktierte Achtel', 0.75], ['Vierteltriole', 2 / 3], ['Achtel', 0.5], ['Achteltriole', 1 / 3], ['Sechzehntel', 0.25]];
    return { wert: q, gross: zahl(q, 4), einh: 'ms', label: 'eine Viertelnote bei ' + zahl(v.bpm) + ' BPM', zeilen: L.map(function (x) { return [x[0], zahl(q * x[1], 4) + ' ms']; }).concat([['Ein Takt (' + zahl(t) + ' Schläge)', zahl(q * t / 1000, 4) + ' s'], ['Schläge je Sekunde', zahl(v.bpm / 60, 4) + ' Hz'], ['Takte je Minute', zahl(v.bpm / t, 4)]]),
      schritte: ['Viertel = 60 000 ms / BPM = 60 000 / ' + zahl(v.bpm) + ' = ' + zahl(q, 5) + ' ms', 'Punktiert = · 1,5 · Triole = · 2/3'], hinweis: 'Für Delays klingen Viertel, punktierte Achtel und Achtel am häufigsten musikalisch; die Vorverzögerung eines Halls liegt oft bei einer Zweiunddreißigstel bis Sechzehntel.' }; } });

function notenName(m) { var n = ((m % 12) + 12) % 12, o = Math.floor(m / 12) - 1; return TON_D[n] + o + (TON_D[n] !== TON_I[n].replace('♯', 'is') ? ' (international ' + TON_I[n] + o + ')' : ''); }
function noteLesen(s) { var m = /^\s*([a-hA-H])(isis|eses|is|es|s|#|♯|b|♭)?\s*(-?\d)?\s*$/.exec(String(s)); if (!m) return null; var g = m[1].toLowerCase(), n = TON_NR[g], v = m[2] || ''; if (g === 'b' && !v) n = 10; else if (g === 'b' && (v === 'b' || v === '♭')) n = 10;
  else n += v === 'is' || v === '#' || v === '♯' ? 1 : v === 'isis' ? 2 : v === 'es' || v === 's' || v === 'b' || v === '♭' ? -1 : v === 'eses' ? -2 : 0; var o = m[3] == null ? 4 : +m[3]; return (o + 1) * 12 + n; }
K({ id: 'm-note', b: 'musik', t: 'Frequenz ↔ Note', u: 'Hertz, Notenname und Abweichung in Cent', s: 'frequenz note hertz stimmen stimmgerät kammerton cent tonhöhe',
  f: [T('x', 'Frequenz in Hz oder Note (z. B. 440, A4, Fis3, B2)', '440', { kurz: true }), F('a4', 'Kammerton A4', 'Hz', 440)],
  r: function (v) { var a4 = oder(v.a4, 440), txt = String(v.x == null ? '' : v.x).trim(); if (!txt) throw new LeerFehler('Frequenz oder Note eingeben.'); var f = zahlLesen(txt), midi, cent = 0, s;
    if (!isNaN(f)) { if (!(f > 0)) throw new Error('Die Frequenz muss größer als 0 sein.'); var mx = 69 + 12 * Math.log(f / a4) / Math.LN2; midi = Math.round(mx); cent = (mx - midi) * 100; s = ['Halbtöne ab A4 = 12 · log₂(f / ' + zahl(a4) + ') = ' + zahl(mx - 69, 5), 'Nächste Note: ' + notenName(midi) + ', Abweichung ' + (cent >= 0 ? '+' : '') + dz(cent, 1) + ' Cent']; }
    else { midi = noteLesen(txt); if (midi == null) throw new Error('Nicht erkannt – z. B. 440, A4, Fis3 oder Es2 eingeben.'); f = a4 * Math.pow(2, (midi - 69) / 12); s = ['f = Kammerton · 2^(Halbtöne / 12) = ' + zahl(a4) + ' · 2^(' + (midi - 69) + ' / 12) = ' + zahl(f, 6) + ' Hz']; }
    var soll = a4 * Math.pow(2, (midi - 69) / 12), git = [['E2', 40], ['A2', 45], ['D3', 50], ['G3', 55], ['H3', 59], ['E4', 64]].map(function (g) { return g[0] + ' ' + dz(a4 * Math.pow(2, (g[1] - 69) / 12), 1); }).join(' · ');
    return { wert: f, gross: isNaN(zahlLesen(txt)) ? zahl(f, 5) : notenName(midi).replace(/ \(.*/, ''), einh: isNaN(zahlLesen(txt)) ? 'Hz' : (Math.abs(cent) < 0.05 ? '' : (cent > 0 ? '+' : '−') + dz(Math.abs(cent), 0) + ' Cent'), label: isNaN(zahlLesen(txt)) ? notenName(midi) : zahl(f, 6) + ' Hz · ' + (Math.abs(cent) < 5 ? 'stimmt' : cent > 0 ? 'zu hoch' : 'zu tief'),
      zeilen: [['Note', notenName(midi)], ['Sollfrequenz', zahl(soll, 6) + ' Hz'], ['Halbton tiefer / höher', zahl(soll / Math.pow(2, 1 / 12), 5) + ' / ' + zahl(soll * Math.pow(2, 1 / 12), 5) + ' Hz'], ['Wellenlänge in Luft (343 m/s)', zahl(343 / f, 3) + ' m'], ['Gitarre, leere Saiten (Hz)', git]], schritte: s,
      hinweis: 'Deutsche Notennamen: H ist das internationale B, B ist das internationale B♭. Oktavzahl nach internationaler Zählung (A4 = Kammerton, C4 = eingestrichenes c).' }; } });

function akkordTeil(tok, hs, deutschEin, deutschAus) {
  var m = /^([A-H])(#|♯|b|♭|is|es(?!us)|s(?!us))?(.*)$/.exec(tok); if (!m) return tok; var g = m[1], v = m[2] || '', n = TON_NR[g.toLowerCase()];
  if (g === 'B') { if (deutschEin || v === 'b' || v === '♭') { n = 10; if (v === 'b' || v === '♭') v = ''; } }
  n += v === '#' || v === '♯' || v === 'is' ? 1 : v === 'b' || v === '♭' || v === 'es' || v === 's' ? -1 : 0; n = (((n + hs) % 12) + 12) % 12;
  var name = TON_I[n].replace('♯', '#').replace('♭', 'b'); if (deutschAus) name = n === 11 ? 'H' : n === 10 ? 'B' : name; return name + m[3];
}
function akkordeTransponieren(text, hs, dEin, dAus) { return String(text).split(/(\s+|\|)/).map(function (t) { if (!t || /^(\s+|\|)$/.test(t)) return t; return t.split('/').map(function (p) { return akkordTeil(p, hs, dEin, dAus); }).join('/'); }).join(''); }
K({ id: 'm-kapo', b: 'musik', t: 'Kapodaster & Transponieren', u: 'Griffe ↔ klingende Akkorde', s: 'kapodaster kapo transponieren akkorde tonart gitarre griffe',
  f: [T('akk', 'Akkorde (mit Leerzeichen getrennt)', 'G C D Em'), F('k', 'Kapodaster im Bund (oder Halbtöne)', '', 2), W('r', 'Richtung', [['k', 'Griffe → so klingt es'], ['g', 'klingende Akkorde → Griffe mit Kapo']], 'k'), W('sw', 'Schreibweise', [['i', 'international (B, B♭ als Bb)'], ['d', 'deutsch (H, B)']], 'i')],
  r: function (v) { var t = String(v.akk == null ? '' : v.akk).trim(); if (!t) throw new LeerFehler('Akkorde eingeben, z. B. G C D Em.'); var k = Math.round(oder(v.k, 0)), hs = v.r === 'g' ? -k : k, d = v.sw === 'd', aus = akkordeTransponieren(t, hs, d, d), zl = [];
    for (var i = 1; i <= 7; i++) if (i !== k) zl.push(['Kapo ' + i + '. Bund', akkordeTransponieren(t, v.r === 'g' ? -i : i, d, d)]);
    return { wert: hs, gross: aus, label: v.r === 'g' ? 'so greifen mit Kapo im ' + k + '. Bund' : 'so klingt es mit Kapo im ' + k + '. Bund', zeilen: zl.slice(0, 6), zeilenTitel: 'Andere Bünde', schritte: ['Jeder Bund = 1 Halbton', v.r === 'g' ? 'Griffe = klingende Akkorde − ' + k + ' Halbtöne' : 'Klang = gegriffene Akkorde + ' + k + ' Halbtöne', 'Zusätze wie m, 7, sus4 und Bässe hinter dem Schrägstrich bleiben erhalten'],
      hinweis: 'Tipp: Für eine bequeme Lage die Tonart wählen, in der offene Akkorde (C, G, D, A, E, Am, Em, Dm) entstehen. Für Bläser: negative Zahl transponiert abwärts.' }; } });

/* ---------- Zahlen & Statistik ---------- */
var ROEM = [[1000, 'M'], [900, 'CM'], [500, 'D'], [400, 'CD'], [100, 'C'], [90, 'XC'], [50, 'L'], [40, 'XL'], [10, 'X'], [9, 'IX'], [5, 'V'], [4, 'IV'], [1, 'I']];
function roemisch(n) { if (!(n >= 1 && n <= 3999) || Math.floor(n) !== n) return null; var s = ''; ROEM.forEach(function (r) { while (n >= r[0]) { s += r[1]; n -= r[0]; } }); return s; }
function roemLesen(s) { s = String(s).toUpperCase().trim(); if (!/^[MDCLXVI]+$/.test(s)) return null; var n = 0, i = 0; ROEM.forEach(function (r) { while (s.substr(i, r[1].length) === r[1]) { n += r[0]; i += r[1].length; } }); return i === s.length && roemisch(n) === s ? n : null; }
function gruppen(s, k) { var o = ''; for (var i = s.length; i > 0; i -= k) o = s.slice(Math.max(0, i - k), i) + (o ? ' ' + o : ''); return o; }
K({ id: 'z-system', b: 'zahlen', t: 'Zahlensysteme', u: 'dezimal ↔ binär ↔ hexadezimal ↔ römisch', s: 'binär hexadezimal hex oktal römische zahlen zahlensystem dual',
  f: [T('z', 'Zahl', '2026', { kurz: true }), W('von', 'Eingabe ist', [['10', 'dezimal'], ['2', 'binär'], ['8', 'oktal'], ['16', 'hexadezimal'], ['r', 'römisch']], '10')],
  r: function (v) { var t = String(v.z == null ? '' : v.z).replace(/[\s._]/g, ''); if (!t) throw new LeerFehler('Zahl eingeben.'); var n;
    if (v.von === 'r') { n = roemLesen(t); if (n == null) throw new Error('Keine gültige römische Zahl (I bis MMMCMXCIX).'); }
    else { var b = +v.von, ok = { 2: /^[01]+$/, 8: /^[0-7]+$/, 10: /^\d+$/, 16: /^(0x)?[0-9a-f]+$/i }[b]; if (!ok.test(t)) throw new Error('Die Eingabe passt nicht zum gewählten Zahlensystem (nur ganze Zahlen ab 0).'); n = parseInt(t.replace(/^0x/i, ''), b); if (!(n <= 9007199254740991)) throw new Error('Die Zahl ist zu groß (höchstens 2⁵³ − 1).'); }
    var bin = n.toString(2), ro = roemisch(n), st = [], r = n, i = 0; while (r > 0 && i < 6) { st.push(r + ' : 2 = ' + Math.floor(r / 2) + ' Rest ' + (r % 2)); r = Math.floor(r / 2); i++; }
    return { wert: n, gross: v.von === '10' ? gruppen(bin, 4) : gz(n), einh: v.von === '10' ? 'binär' : 'dezimal', label: 'aus ' + ({ 10: 'dezimal', 2: 'binär', 8: 'oktal', 16: 'hexadezimal', r: 'römisch' })[v.von] + ' ' + t.toUpperCase(),
      zeilen: [['Dezimal', gz(n)], ['Binär', gruppen(bin, 4)], ['Oktal', n.toString(8)], ['Hexadezimal', gruppen(n.toString(16).toUpperCase(), 4)], ['Römisch', ro || 'nur für 1 bis 3999'], ['Stellen binär', bin.length + ' Bit']],
      schritte: ['Dezimal → binär: fortlaufend durch 2 teilen, die Reste von unten nach oben lesen'].concat(st).concat(r > 0 ? ['… und so weiter bis 0'] : []), hinweis: 'Je 4 Binärstellen ergeben eine Hexadezimalstelle. Römische Zahlen kennen keine Null und reichen in der üblichen Schreibweise bis 3999.' }; } });

K({ id: 'z-statistik', b: 'zahlen', t: 'Statistik aus einer Zahlenliste', u: 'Mittelwert, Median, Streuung, Quartile', breit: true, s: 'statistik mittelwert durchschnitt median standardabweichung varianz quartil spannweite',
  f: [T('l', 'Zahlen (mit Leerzeichen, Semikolon oder Zeilenumbruch getrennt)', '12 15 11 19 15 22 17 14', { zeilen: 3 })],
  r: function (v) { var roh = String(v.l == null ? '' : v.l).split(/[\s;]+/).filter(Boolean), a = roh.map(zahlLesen), schl = roh.filter(function (x, i) { return isNaN(a[i]); }); if (!roh.length) throw new LeerFehler('Zahlen eingeben.'); if (schl.length) throw new Error('Nicht lesbar: ' + schl.slice(0, 3).join(', ') + ' – Dezimalstellen mit Komma schreiben.');
    var n = a.length, s = a.slice().sort(function (x, y) { return x - y; }), sum = a.reduce(function (x, y) { return x + y; }, 0), mw = sum / n, q = function (p) { var i = (n - 1) * p, lo = Math.floor(i), hi = Math.ceil(i); return s[lo] + (s[hi] - s[lo]) * (i - lo); }, ss = a.reduce(function (x, y) { return x + (y - mw) * (y - mw); }, 0), sdS = n > 1 ? Math.sqrt(ss / (n - 1)) : 0, sdP = Math.sqrt(ss / n);
    var h = {}, hm = 0; a.forEach(function (x) { h[x] = (h[x] || 0) + 1; if (h[x] > hm) hm = h[x]; }); var modi = hm > 1 ? Object.keys(h).filter(function (k) { return h[k] === hm; }).map(function (k) { return zahl(+k); }).join(', ') + ' (je ' + hm + '×)' : 'keiner (alle Werte einmal)';
    return { wert: mw, gross: zahl(mw, 6), label: 'Mittelwert aus ' + n + ' Werten', zeilen: [['Summe', zahl(sum, 10)], ['Median', zahl(q(0.5), 8)], ['Häufigster Wert (Modus)', modi], ['Kleinster / größter Wert', zahl(s[0]) + ' / ' + zahl(s[n - 1])], ['Spannweite', zahl(s[n - 1] - s[0], 8)], ['Standardabweichung (Stichprobe, n − 1)', zahl(sdS, 6)], ['Standardabweichung (Gesamtheit, n)', zahl(sdP, 6)], ['Unteres / oberes Quartil', zahl(q(0.25), 6) + ' / ' + zahl(q(0.75), 6)], ['Variationskoeffizient', mw ? dz(sdS / Math.abs(mw) * 100, 1) + ' %' : '–']],
      schritte: ['Mittelwert = Summe / Anzahl = ' + zahl(sum, 10) + ' / ' + n + ' = ' + zahl(mw, 8), 'Median: mittlerer Wert der sortierten Liste (bei gerader Anzahl Mittel der beiden mittleren)', 'Standardabweichung = √(Summe der quadrierten Abweichungen / (n − 1)) = √(' + zahl(ss, 8) + ' / ' + (n - 1) + ') = ' + zahl(sdS, 6), 'Quartile mit linearer Interpolation (wie QUARTILE in der Tabellenkalkulation)'],
      svg: n <= 16 ? balken(s.map(function (x, i) { return { l: (i + 1) + '.', v: x, txt: zahl(x), f: x === q(0.5) ? 'var(--rz-f3)' : 'var(--rz-f2)' }; })) : null, hinweis: 'Der Median ist unempfindlich gegen Ausreißer, der Mittelwert nicht – liegen beide weit auseinander, ist die Verteilung schief.' }; } });

var KARTE = {}; KARTEN.forEach(function (k) { KARTE[k.id] = k; });

/* ===================================================================== 9. Fragefeld (regelbasiert) */
var NUM = '([-−]?(?:\\d{1,3}(?:\\.\\d{3})+(?![\\d])|\\d+)(?:[.,]\\d+)?(?:e[-+]?\\d+)?)';
function rx(s, f) { return new RegExp(s.replace(/NUM/g, NUM), f || 'i'); }
function zahlenIn(s) { var r = [], m, re = rx('NUM', 'gi'); while ((m = re.exec(s))) r.push(zahlLesen(m[1])); return r; }
var EINH_RE = '(€\\/kwh|ct\\/kwh|l\\/100\\s?km|km\\/h|mol\\/l|kwh|kw|mw|w|v|ma|a|kω|kohm|ω|ohm|cent|ct|€|eur|euro|%|prozent|stunden|std|h|minuten|min|sekunden|s|tage|tag|jahre|jahren|jahr|j|monate|monaten|km|cm|mm|m|kg|g|mol|ml|l|°c|grad|hpa|pa|bar|personen|pers)';
function werteMitEinheit(s) {
  var r = [], m, re = new RegExp(NUM + '\\s*' + EINH_RE + '?(?![a-zäöü])', 'gi');
  while ((m = re.exec(s))) r.push({ v: zahlLesen(m[1]), u: (m[2] || '').toLowerCase().replace(/\s/g, '') });
  return r;
}
function nimm(L, units) { for (var i = 0; i < L.length; i++) if (units.indexOf(L[i].u) >= 0) { var x = L[i]; L.splice(i, 1); return x.v; } return null; }
function datumsTeile(s) {
  var r = [], m, re = /(\d{1,2})\.\s?(\d{1,2})\.(?:\s?(-?\d{1,7}))?(\s*v\.?\s*chr\.?)?|(\d{1,2})\.?\s+(januar|jänner|februar|märz|maerz|april|mai|juni|juli|august|september|oktober|november|dezember)(?:\s+(-?\d{1,7}))?(\s*v\.?\s*chr\.?)?/gi;
  while ((m = re.exec(s))) r.push(m[0].trim());
  return r;
}
var BEISPIELE = ['Treppe', 'Salzlake', 'Brutto Netto', '15 % von 240', '240 + 19 %', 'von 80 auf 100 in Prozent', '5 km in Meilen', '3 Tassen in ml', '180 °C in Fahrenheit', '72 kg in Pfund', '2,5 ha in m²', '100 USD in EUR', 'molare Masse H2SO4',
  'wie viel Mol sind 50 g NaCl', 'Wochentag 24.12.2031', 'welcher Tag war vor 5000 Jahren', 'Wochentag in 2000 Jahren', 'Tage bis 24.12.', 'Tage zwischen 1.1.2020 und 11.11.2026',
  'Dreisatz: 3 kg kosten 7,50, was kosten 5 kg', 'Wurzel aus 2', '2^10', '(3+4)*5/2', 'Kreis r=3 Fläche', 'BMI 80 kg 1,80 m', 'Ohm 230 V 10 A', 'kWh Kosten 2000 W 3 h 0,35 €', 'Zinsen 10000 € 3 % 10 Jahre'];
function karteErg(id, werte, extra) { var o = { typ: 'karte', karte: id, werte: werte }; if (extra) for (var k in extra) o[k] = extra[k]; return o; }
function frage(q, ctx) {
  var o = String(q == null ? '' : q).trim().replace(/\?+$/, '').trim(); if (!o) return null;
  var s = o.toLowerCase().replace(/[−–]/g, '-').replace(/\s+/g, ' ').trim(), m, h = ctx.heute, L;
  /* --- Chemie --- */
  if ((m = /^(?:die\s+)?(?:molare?\s*masse|molmasse|molekülmasse|molgewicht)\s*(?:von|der|des|für|aus)?\s*(.+)$/i.exec(o)) || (m = /^M\s*\(\s*(.+?)\s*\)$/.exec(o))) return karteErg('molmasse', { formel: m[1].trim() });
  if ((m = rx('^wie\\s*viel(?:e)?\\s*mol\\s*(?:sind|ergeben|entsprechen|hat|haben)?\\s*NUM\\s*(mg|g|kg)\\s+(.+)$').exec(o))) return karteErg('stoffmenge', { formel: m[3].trim(), m: zahlLesen(m[1]) * { mg: 0.001, g: 1, kg: 1000 }[m[2].toLowerCase()], n: null });
  if ((m = rx('^NUM\\s*(mg|g|kg)\\s+(\\S+)\\s+(?:in|zu|=|als)\\s*mol$').exec(o))) return karteErg('stoffmenge', { formel: m[3], m: zahlLesen(m[1]) * { mg: 0.001, g: 1, kg: 1000 }[m[2].toLowerCase()], n: null });
  if ((m = rx('^NUM\\s*(mmol|mol)\\s+(\\S+)\\s+(?:in|zu|=|als)\\s*(?:gramm|g)$').exec(o))) return karteErg('stoffmenge', { formel: m[3], m: null, n: zahlLesen(m[1]) * (m[2].toLowerCase() === 'mmol' ? 0.001 : 1) });
  if (/\bph\b/.test(s) && (L = werteMitEinheit(s.replace(/10\s*\^\s*-\s*(\d+)/, function (a, b) { return String(Math.pow(10, -b)).replace('.', ','); }))).length) { var c = nimm(L, ['mol/l']); if (c == null && L.length) c = L[0].v; if (c != null) return karteErg('ph', { art: /oh/.test(s) ? 'oh' : 'h', w: c }); }
  if ((m = /^(?:element|ordnungszahl)\s+(.+)$/i.exec(o)) || (EL[o] && o.length <= 2) || (/^[a-zäöü]+$/i.test(o) && (m = null, elementSuchen(o)))) { var e = elementSuchen(m ? m[1] : o); if (e) return { typ: 'element', el: e }; }
  if (STOFFE[s]) return karteErg('molmasse', { formel: o });
  /* --- Kalender --- */
  if (/schaltjahr/.test(s) && (m = /(-?\d{1,7})/.exec(s))) { var yy = +m[1]; return { typ: 'direkt', gross: schaltG(yy) ? 'Ja' : 'Nein', label: jahrText(yy) + (schaltG(yy) ? ' ist ein Schaltjahr' : ' ist kein Schaltjahr') + ' (gregorianisch)', zeilen: [['Julianisch', schaltJ(yy) ? 'Schaltjahr' : 'kein Schaltjahr'], ['Tage im Jahr', String(schaltG(yy) ? 366 : 365)]], schritte: ['Regel: durch 4 teilbar → Schaltjahr; volle Jahrhunderte nur, wenn durch 400 teilbar', jahrText(yy) + ': ' + (mod(yy, 4) ? 'nicht durch 4 teilbar' : mod(yy, 100) ? 'durch 4, nicht durch 100 teilbar' : mod(yy, 400) ? 'durch 100, aber nicht durch 400 teilbar' : 'durch 400 teilbar')], oeffne: { karte: 'k-wochentag', werte: { t: 29, m: 2, j: yy } } }; }
  if ((m = /\b(?:vor|in)\s+(\d[\d.]*)\s*(tag|tagen|tage|woche|wochen|monat|monaten|monate|jahr|jahren|jahre)\b/.exec(s)) && !/(zins|kredit|darlehen|inflation|kaufkraft|spar|€|%|euro)/.test(s)) {
    var nn = zahlLesen(m[1]), ein = m[2][0] === 'w' ? 'w' : m[2][0] === 'm' ? 'm' : m[2][0] === 'j' ? 'j' : 't', vor = /\bvor\s+\d/.test(s);
    return karteErg('k-plusminus', { d: '', n: nn, e: ein, r: vor ? '-' : '+' });
  }
  var dts = datumsTeile(s);
  if ((m = /tage?\s+(?:zwischen|von)\s+(.+?)\s+(?:und|bis)\s+(.+)$/.exec(s)) || (/^(?:zeitraum|differenz|abstand)\b/.test(s) && dts.length === 2 && (m = [0, dts[0], dts[1]]))) {
    var a1 = datumLesen(m[1], 'g', h), b1 = datumLesen(m[2], 'g', h); if (a1 && b1) return karteErg('k-diff', { a: m[1], b: m[2] });
  }
  if ((m = /(?:tage|wie lange(?: noch)?|wie viele tage(?: noch)?|countdown)\s+bis\s+(?:zum\s+|zu\s+|an\s+)?(.+)$/.exec(s))) {
    var zz = m[1].trim(), fest = { weihnachten: '24.12.', heiligabend: '24.12.', silvester: '31.12.', neujahr: '1.1.', 'tag der arbeit': '1.5.', halloween: '31.10.', nikolaus: '6.12.' };
    if (/ostern/.test(zz)) { var oy = osternG(h.y); if (jdnG(oy.y, oy.m, oy.d) < jdnG(h.y, h.m, h.d)) oy = osternG(h.y + 1); zz = oy.d + '.' + oy.m + '.' + oy.y; }
    if (fest[zz]) zz = fest[zz];
    if (datumLesen(zz, 'g', h)) return karteErg('k-diff', { a: '', b: zz });
  }
  if (/(ostern|ostersonntag|feiertage)/.test(s) && !/bis/.test(s)) { m = /(\d{3,4})/.exec(s); return karteErg('k-feiertage', { j: m ? +m[1] : h.y }); }
  if (/(kalenderwoche|\bkw\b)/.test(s)) { var dk = dts.length ? datumLesen(dts[0], 'g', h) : h; if (dk) return karteErg('k-wochentag', { t: dk.d, m: dk.m, j: dk.y, kal: 'g', _fokus: 'kw' }); }
  if (/(mondphase|\bmond\b|vollmond|neumond)/.test(s)) return karteErg('k-mond', { d: dts[0] || '' });
  if (/(alter|wie alt|geburtstag)/.test(s) && dts.length) return karteErg('k-alter', { g: dts[0], s: dts[1] || '' });
  if (/(unix|zeitstempel|timestamp)/.test(s)) { m = /(\d{6,})/.exec(s); return karteErg('k-unix', { u: m ? m[1] : '', d: m ? '' : (dts[0] || '') }); }
  if ((m = /(?:uhrzeit|wie spät(?: ist es)?|zeit)\s+(?:in|auf)\s+(.+)$/.exec(s))) { var tz = ZONEN_ALIAS[m[1].trim()]; if (tz) return karteErg('k-zonen', { uhr: '', von: 'Europe/Berlin', nach: tz }); }
  if (/(jahreszeit|sonnenwende|tagundnachtgleiche|frühlingsanfang|sommeranfang|herbstanfang|winteranfang)/.test(s)) { m = /(-?\d{1,4})/.exec(s); return karteErg('k-jahreszeiten', { j: m ? +m[1] : h.y }); }
  if (/(wochentag|welcher tag|was für ein tag|welchen tag|tag war|tag ist)/.test(s) || (dts.length === 1 && s.replace(dts[0].toLowerCase(), '').trim() === '')) {
    if (dts.length) { var d0 = datumLesen(dts[0], /julian/.test(s) ? 'j' : 'g', h); if (d0) return karteErg('k-wochentag', { t: d0.d, m: d0.m, j: d0.y, kal: /julian/.test(s) ? 'j' : 'g' }); }
    if (/heute|morgen|gestern/.test(s) || /^(welcher tag ist|was für ein tag ist)/.test(s)) { var dd = /morgen/.test(s) ? 1 : /gestern/.test(s) ? -1 : 0, Jx = jdnG(h.y, h.m, h.d) + dd, ox = ausJdnG(Jx); return karteErg('k-wochentag', { t: ox.d, m: ox.m, j: ox.y, kal: 'g' }); }
  }
  /* --- Prozent --- */
  if ((m = rx('^NUM\\s*(?:%|prozent)\\s*(?:von|aus)\\s*NUM').exec(s))) return karteErg('p-wert', { p: zahlLesen(m[1]), g: zahlLesen(m[2]) });
  if ((m = rx('von\\s*NUM\\s*(?:€|eur|euro)?\\s*(?:auf|zu|nach)\\s*NUM').exec(s)) && /(prozent|%|veränder|steiger|anstieg|zunahme|abnahme|gesunken|gestiegen|plus|minus)/.test(s)) return karteErg('p-veraend', { a: zahlLesen(m[1]), n: zahlLesen(m[2]) });
  if ((m = rx('^NUM\\s*(?:€|eur)?\\s*(?:ist|sind)?\\s*(?:wie\\s*viel(?:e)?\\s*(?:prozent|%)\\s*)?von\\s*NUM\\s*(?:€|eur)?\\s*(?:in\\s*(?:prozent|%))?$').exec(s)) && /(prozent|%)/.test(s)) return karteErg('p-satz', { w: zahlLesen(m[1]), g: zahlLesen(m[2]) });
  if ((m = rx('^NUM\\s*(?:%|prozent)\\s*(?:sind|=|entsprechen|ist)\\s*NUM').exec(s))) return karteErg('p-grund', { p: zahlLesen(m[1]), w: zahlLesen(m[2]) });
  if (/(mwst|mehrwertsteuer|umsatzsteuer|netto|brutto)/.test(s)) {
    L = werteMitEinheit(s); var satz = /\b7\s*(%|prozent)/.test(s) ? '7' : '19'; L = L.filter(function (x) { return x.u !== '%' && x.u !== 'prozent'; });
    if (L.length) { var ib = s.indexOf('brutto'), inn = s.indexOf('netto'), rr = ib >= 0 && (inn < 0 || ib < inn) ? 'b' : 'n'; return karteErg('mwst', { b: L[0].v, s: satz, r: rr }); }
  }
  if (/rabatt|nachlass|skonto/.test(s)) { L = werteMitEinheit(s); var rp = nimm(L, ['%', 'prozent']), rb = L.length ? L[0].v : null; if (rp != null && rb != null) return karteErg('rabatt', { p: rb, r1: rp, r2: nimm(L, ['%', 'prozent']) }); }
  if (/trinkgeld/.test(s)) { L = werteMitEinheit(s); var tp = nimm(L, ['%', 'prozent']), tps = nimm(L, ['personen', 'pers']); if (L.length) return karteErg('trinkgeld', { b: L[0].v, tg: tp == null ? 10 : tp, pers: tps || 1 }); }
  /* --- Dreisatz --- */
  if (/dreisatz/.test(s) || (/(kost|wieg|ergeb|brauch|schaff|reich|benötig|dauer|fahr|verbrauch)/.test(s) && /(was|wie\s?viel|wie lange)/.test(s) && /[,;]/.test(s))) {
    var zl = zahlenIn(s.replace(/dreisatz:?/, ''));
    if (zl.length >= 3) { var anti = /(umgekehrt|antiprop)/.test(s) || (/(arbeiter|personen|leute|maschinen|pumpen|bagger|helfer|handwerker|maler)/.test(s) && /(brauch|benötig|dauer|schaff|lange)/.test(s)); return karteErg('dreisatz', { a: zl[0], b: zl[1], c: zl[2], m: anti ? 'u' : 'p' }); }
  }
  /* --- Geometrie --- */
  if ((m = /\b(kreis|kugel|zylinder|kegel|quader|würfel|rechteck|quadrat|dreieck|trapez)\b/.exec(s))) {
    var form = { 'würfel': 'quader', quadrat: 'rechteck' }[m[1]] || m[1], gw = {}, mm, re = rx('\\b(r|d|h|a|b|c)\\s*=\\s*NUM', 'gi');
    while ((mm = re.exec(s))) gw[mm[1].toLowerCase()] = zahlLesen(mm[2]);
    if ((mm = rx('radius\\s*(?:von|=)?\\s*NUM').exec(s))) gw.r = zahlLesen(mm[1]);
    if ((mm = rx('durchmesser\\s*(?:von|=)?\\s*NUM').exec(s))) gw.d = zahlLesen(mm[1]);
    if ((mm = rx('höhe\\s*(?:von|=)?\\s*NUM').exec(s))) gw.h = zahlLesen(mm[1]);
    if ((mm = rx('NUM\\s*(?:x|×|\\*|mal)\\s*NUM(?:\\s*(?:x|×|\\*|mal)\\s*NUM)?').exec(s))) { gw.a = zahlLesen(mm[1]); gw.b = zahlLesen(mm[2]); if (mm[3]) gw.c = zahlLesen(mm[3]); }
    if (gw.d && !gw.r) gw.r = gw.d / 2;
    if (Object.keys(gw).length === 0) { var zg = zahlenIn(s); if (zg.length) { if (/kreis|kugel|zylinder|kegel/.test(form)) { gw.r = zg[0]; if (zg[1]) gw.h = zg[1]; } else { gw.a = zg[0]; if (zg[1]) gw.b = zg[1]; if (zg[2]) gw.c = zg[2]; } } }
    if (m[1] === 'quadrat') gw.b = gw.a; if (m[1] === 'würfel') { gw.b = gw.a; gw.c = gw.a; }
    if (Object.keys(gw).length) { var fk = /oberfläche/.test(s) ? 'Oberfläche' : /(fläche|flächeninhalt)/.test(s) ? 'Fläche' : /umfang/.test(s) ? 'Umfang' : /(volumen|inhalt|rauminhalt)/.test(s) ? 'Volumen' : /diagonale/.test(s) ? 'Diagonale' : null;
      var w = { form: form, ein: '' }; FORM_F[form].forEach(function (k) { w[k] = gw[k] != null ? gw[k] : null; }); if (fk) w._fokus = fk; return karteErg('formen', w); }
  }
  /* --- Gesundheit, Physik, Geld --- */
  if (/\bbmi\b|body.?mass/.test(s)) { L = werteMitEinheit(s); var kg = nimm(L, ['kg']), cm = nimm(L, ['cm']), mt = nimm(L, ['m']); if (cm == null && mt != null) cm = mt * 100; if (cm == null && L.length) { var x0 = L[0].v; cm = x0 < 3 ? x0 * 100 : x0; } if (kg != null && cm != null) return karteErg('bmi', { kg: kg, cm: cm }); }
  if (/grundumsatz|kalorienbedarf/.test(s)) { L = werteMitEinheit(s); var gk = nimm(L, ['kg']), gc = nimm(L, ['cm']), ga = nimm(L, ['jahre', 'j', 'jahren']); if (gk && gc && ga) return karteErg('grundumsatz', { g: /(frau|weib)/.test(s) ? 'w' : 'm', a: ga, kg: gk, cm: gc, pal: '1.4' }); }
  if (/\bpace\b|tempo|laufzeit/.test(s)) { L = werteMitEinheit(s); var pk = nimm(L, ['km']), pm = /(\d+:\d{2}(?::\d{2})?)/.exec(s), pmin = nimm(L, ['min', 'minuten']); if (pk && (pm || pmin)) return karteErg('pace', { km: pk, zeit: pm ? pm[1] : String(pmin) }); }
  if (/(kwh|stromkosten|strom kosten|stromverbrauch)/.test(s)) { L = werteMitEinheit(s); var P = nimm(L, ['w']), Pk = nimm(L, ['kw']), hh = nimm(L, ['h', 'std', 'stunden']), pr = nimm(L, ['€/kwh', '€', 'eur', 'euro']), ct = nimm(L, ['ct/kwh', 'ct', 'cent']), td = nimm(L, ['tage', 'tag']);
    if (P == null && Pk != null) P = Pk * 1000; if (pr == null && ct != null) pr = ct / 100; if (P != null && hh != null) return karteErg('stromkosten', { P: P, h: hh, tage: td || 1, preis: pr == null ? 0.35 : pr }); }
  if (/\bohm\b|spannung|stromstärke|widerstand|leistung/.test(s)) { L = werteMitEinheit(s); var U = nimm(L, ['v']), I = nimm(L, ['a']), mA = nimm(L, ['ma']), R = nimm(L, ['ω', 'ohm']), kR = nimm(L, ['kω', 'kohm']), PW = nimm(L, ['w']), PkW = nimm(L, ['kw']);
    if (I == null && mA != null) I = mA / 1000; if (R == null && kR != null) R = kR * 1000; if (PW == null && PkW != null) PW = PkW * 1000;
    var g4 = { U: U, I: I, R: R, P: PW }; if (Object.keys(g4).filter(function (k) { return g4[k] != null; }).length >= 2) return karteErg('ohm', g4); }
  if (/(kredit|darlehen|annuität|finanzierung)/.test(s)) { L = werteMitEinheit(s); var kp = nimm(L, ['%', 'prozent']), kj = nimm(L, ['jahre', 'jahren', 'jahr', 'j']), kk = nimm(L, ['€', 'eur', 'euro']); if (kk == null && L.length) kk = L.shift().v; if (kk && kp != null && kj) return karteErg('kredit', { k: kk, p: kp, n: kj, rate: null }); }
  if (/(inflation|kaufkraft)/.test(s)) { L = werteMitEinheit(s); var ip = nimm(L, ['%', 'prozent']), ij = nimm(L, ['jahre', 'jahren', 'jahr', 'j']), ib2 = nimm(L, ['€', 'eur', 'euro']); if (ib2 == null && L.length) ib2 = L.shift().v; if (ib2 && ip != null && ij) return karteErg('inflation', { b: ib2, r: ip, n: ij }); }
  if (/(zins|sparplan|sparen|anlage|kapital)/.test(s)) { L = werteMitEinheit(s); var zp = nimm(L, ['%', 'prozent']), zj = nimm(L, ['jahre', 'jahren', 'jahr', 'j']), zk = nimm(L, ['€', 'eur', 'euro']), zr = null;
    if (zk == null && L.length) zk = L.shift().v; if ((m = rx('NUM\\s*(?:€|eur|euro)?\\s*(?:monatlich|pro monat|im monat|je monat|mtl)').exec(s))) zr = zahlLesen(m[1]); if (zr === zk) { zk = 0; }
    if (zp != null && zj && (zk != null || zr)) return karteErg('zins', { k0: zk || 0, rate: zr || 0, p: zp, n: zj, iv: /monatlich.*(zins|gutschrift)|(zins|gutschrift).*monatlich/.test(s) ? 'm' : 'j' }); }
  if (/(sprit|benzin|diesel|tank|fahrtkosten|fahrt kostet|fahrt kosten)/.test(s)) { L = werteMitEinheit(s); var sk = nimm(L, ['km']), sl = nimm(L, ['l/100km', 'l']), sp = nimm(L, ['€', 'eur', 'euro']); if (sk && sl) return karteErg('sprit', { km: sk, vb: sl, pr: sp || 1.75, pers: 1, hz: /(hin und zurück|retour)/.test(s) ? 'h' : 'e' }); }
  /* --- Umrechnung (Einheiten, Währung, Küche) --- */
  var um = null;
  if ((m = rx('^NUM\\s*(.+?)\\s+(?:in|nach|zu|als|=|→|->|to|umgerechnet in|umrechnen in|sind wie viele?|sind wieviel(?:e)?|entsprechen wie viele?)\\s+(.+)$').exec(o))) um = { w: zahlLesen(m[1]), a: m[2], b: m[3] };
  else if ((m = rx('^wie\\s*viel(?:e)?\\s+(.+?)\\s+(?:sind|ist|ergeben|entsprechen|hat|haben)\\s+NUM\\s*(.+)$').exec(o))) um = { w: zahlLesen(m[2]), a: m[3], b: m[1] };
  else if ((m = rx('^NUM\\s*([a-z$€£¥]{3,4}|euro|dollar)$').exec(o)) && waehrungFinden(m[2]) && waehrungFinden(m[2]) !== 'EUR') um = { w: zahlLesen(m[1]), a: m[2], b: 'EUR' };
  if (um) {
    var A = um.a.trim().replace(/[.,;:]+$/, ''), B = um.b.trim().replace(/[.,;:]+$/, '').replace(/^(?:in|nach)\s+/i, '');
    var wa = waehrungFinden(A), wb = waehrungFinden(B);
    if (wa && wb) return karteErg('waehrung', { w: um.w, von: wa, nach: wb });
    var zm = /^(.+?)\s+([a-zäöüß]+)$/i.exec(A), zt = zm && ZUTAT_ALIAS[zm[2].toLowerCase()];
    if (zt) { var ea = kuecheEinheit(zm[1]), eb = kuecheEinheit(B); if (ea && eb) return karteErg('kueche', { z: zt, w: um.w, von: ea }, { ziel: eb }); }
    var p2 = einheitPaar(A, B);
    if (p2 && !p2.fehler) return karteErg('einheit', { kat: p2[0].kat, w: um.w, von: p2[0].id, nach: p2[1].id });
    if (p2 && p2.fehler) return { typ: 'fehler', text: '„' + A + '“ (' + KAT[p2.A[0].kat].n + ') und „' + B + '“ (' + KAT[p2.B[0].kat].n + ') lassen sich nicht ineinander umrechnen.' };
  }
  /* --- Rechenausdruck --- */
  var ex = s.replace(/^(was ist|was sind|was ergibt|wie viel ist|wieviel ist|wie viel sind|berechne|rechne|ausrechnen|=)\s*/, '').replace(/[=?]\s*$/, '')
    .replace(rx('(\\d+)\\.\\s*wurzel\\s*(?:aus|von)\\s*NUM'), 'root($2;$1)').replace(/(?:quadrat)?wurzel\s*(?:aus|von)\s*/g, '√').replace(/kubikwurzel\s*(?:aus|von)\s*/g, '∛')
    .replace(/\bhoch\b/g, '^').replace(/\bmal\b/g, '*').replace(/geteilt durch|\bdurch\b/g, '/').replace(/\bplus\b/g, '+').replace(/\bminus\b/g, '-').replace(/\bquadrat\b/g, '^2').replace(/\bprozent\b/g, '%')
    .replace(/fakultät\s*(?:von|aus)?\s*(\d+)/g, '$1!').replace(/(\d)\s*!/g, '$1!');
  try { var r = ausdruck(ex, { grad: ctx.grad !== false }); return { typ: 'ausdruck', ausdruck: ex, wert: r.wert, prozent: r.prozent, schritte: r.schritte }; }
  catch (err) { if (/^[\d\s.,+\-*/:^()%!²³√π×÷·]+$/.test(ex) || /(sin|cos|tan|log|ln|sqrt|wurzel|root|pi|√)/.test(ex)) return { typ: 'fehler', text: err.message }; }
  return { typ: 'unbekannt' };
}
function kuecheEinheit(s) { s = aliasRein(s); var map = { ml: 'ml', milliliter: 'ml', l: 'l', liter: 'l', tl: 'TL', teelöffel: 'TL', el: 'EL', esslöffel: 'EL', tasse: 'Tasse', tassen: 'Tasse', cup: 'cup', cups: 'cup', g: 'g', gramm: 'g', kg: 'kg', oz: 'oz', unzen: 'oz', lb: 'lb' }; return map[s] || null; }
function elementSuchen(q) {
  q = String(q).trim(); if (!q) return null;
  if (/^\d+$/.test(q)) return ELEMENTE[+q - 1] || null;
  var l = q.toLowerCase();
  for (var i = 0; i < ELEMENTE.length; i++) if (ELEMENTE[i].s.toLowerCase() === l || ELEMENTE[i].n.toLowerCase() === l) return ELEMENTE[i];
  return null;
}
/* Frage-Ergebnis in einheitliches Ergebnisobjekt überführen */
function frageAuswerten(q, ctx) {
  var f = frage(q, ctx);
  if (!f) return null;
  if (f.typ === 'karte') {
    var k = KARTE[f.karte], v = {};
    k.f.forEach(function (fd) { v[fd.k] = fd.w == null ? null : fd.w; });
    if (k.vor) { var vv = k.vor(ctx); for (var a in vv) v[a] = vv[a]; }
    for (var b in f.werte) v[b] = f.werte[b];
    try { var e = k.r(v, ctx); e.titel = k.t; e.karte = f.karte; e.werte = f.werte; if (f.karte === 'kueche' && f.ziel) kuecheZiel(e, v, f.ziel); return e; }
    catch (err) { return { fehler: err.message, karte: f.karte, werte: f.werte, titel: k.t }; }
  }
  if (f.typ === 'ausdruck') {
    var w = f.wert, txt = f.prozent ? zahl(w * 100) + ' %' : zahl(w);
    return { titel: 'Rechnung', wert: w, gross: txt, label: ausdruckHuebsch(f.ausdruck), schritte: ['Regeln: Klammern zuerst, dann Potenzen, dann Punkt- vor Strichrechnung.'].concat(f.schritte.length ? f.schritte : ['Ergebnis: ' + txt]).concat(/(sin|cos|tan)/.test(f.ausdruck) ? ['Winkel in ' + (ctx.grad !== false ? 'Grad' : 'Bogenmaß') + '.'] : []), karte: 'rechner', werte: { ausdruck: f.ausdruck } };
  }
  if (f.typ === 'element') { var el = f.el; return { titel: 'Element', wert: el.m, gross: el.s, label: el.n + ' · Ordnungszahl ' + el.z, zeilen: elementZeilen(el), karte: 'molmasse', werte: { formel: el.s }, element: el }; }
  if (f.typ === 'direkt') { f.titel = f.titel || 'Ergebnis'; if (f.oeffne) { f.karte = f.oeffne.karte; f.werte = f.oeffne.werte; } return f; }
  if (f.typ === 'fehler') return { fehler: f.text };
  return { unbekannt: true };
}
function kuecheZiel(e, v, ziel) {
  var x = kuecheE(ziel), z = zutat(v.z), src = kuecheE(v.von); if (!x || !src) return;
  var ml = src[2] === 'v' ? v.w * src[3] : v.w * src[3] / z[2], g = ml * z[2], wert = x[2] === 'v' ? ml / x[3] : g / x[3];
  e.wert = wert; e.gross = zahl(wert, 3); e.einh = x[0];
}
function elementZeilen(el) {
  return [['Symbol', el.s], ['Ordnungszahl', String(el.z)], ['Atommasse', (el.instabil ? '[' + el.m + '] (Massenzahl des stabilsten Isotops)' : dz(el.m, 4) + ' u')], ['Periode', String(el.periode)], ['Gruppe', el.gruppe ? String(el.gruppe) : (el.z < 90 ? 'Lanthanoide (Gr. 3)' : 'Actinoide (Gr. 3)')], ['Kategorie', KAT_EL[el.kat]]];
}
function ausdruckHuebsch(s) { return String(s).replace(/\*/g, ' · ').replace(/\//g, ' : ').replace(/\+/g, ' + ').replace(/(\d)-/g, '$1 − ').replace(/\s+/g, ' ').replace(/\./g, ',').trim(); }

var KERN = { zahl: zahl, fix: fix, dz: dz, kfm: kfm, rund: rund, zahlLesen: zahlLesen, ausdruck: ausdruck, KAT: KAT, KAT_REIHE: KAT_REIHE, umrechnen: umrechnen, einheitFinden: einheitFinden, einheitPaar: einheitPaar,
  molMasse: molMasse, formelLesen: formelLesen, ELEMENTE: ELEMENTE, EL: EL, jdnG: jdnG, jdnJ: jdnJ, ausJdnG: ausJdnG, ausJdnJ: ausJdnJ, wochentag: wochentag, WT: WT, osternG: osternG, osternJ: osternJ,
  isoWoche: isoWoche, feiertage: feiertage, arbeitstage: arbeitstage, differenzYMD: differenzYMD, datumLesen: datumLesen, mondphase: mondphase, jahreszeiten: jahreszeiten, schaltG: schaltG,
  KARTEN: KARTEN, KARTE: KARTE, kartenSuche: kartenSuche, akkordeTransponieren: akkordeTransponieren, sonne: sonne, est2026: est2026, frage: frage, frageAuswerten: frageAuswerten, richtKurse: richtKurse, WAEHRUNGEN: WAEHRUNGEN, heuteDatum: heuteDatum, BEISPIELE: BEISPIELE, kursSVG: kursSVG, tzVersatz: tzVersatz };

/* ===================================================================== 10. Oberfläche */
var SPEICHER = 'qw-rechner', ST = {}, TIMER = null, IO = null, RO = null, KURS_LAEUFT = false, SPEICHER_T = null, KURS_DATEN = {}, KURS_Z = 0;
function laden() { try { var x = JSON.parse(localStorage.getItem(SPEICHER) || '{}'); return x && typeof x === 'object' ? x : {}; } catch (e) { return {}; } }
function sichern(sofort) {
  clearTimeout(SPEICHER_T);
  var f = function () { try { localStorage.setItem(SPEICHER, JSON.stringify(ST)); } catch (e) { /* Speicher voll oder gesperrt */ } };
  if (sofort) f(); else SPEICHER_T = setTimeout(f, 300);
}
function bewegungAus() { try { return root.matchMedia && root.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) { return false; } }
var GRUPPEN = [['grund', 'Rechnen & Umrechnen'], ['praxis', 'Haus, Garten & Alltag'], ['wissen', 'Wissen & Technik']];
var BEREICHE = [
  ['rechner', 'Rechner', '±', 'Grundrechner mit Verlauf und wissenschaftlichen Funktionen',
    'Eigener Formel-Parser (kein eval): Klammern → Potenzen → Punkt vor Strich → Strich. „240 + 19 %“ rechnet 240 · 1,19; „15 % von 240“ rechnet 0,15 · 240. Funktionen: sin, cos, tan (Grad oder Bogenmaß), asin …, √, ∛, ln, log (Basis 10), ld, n!, π, e. Dezimalkomma; Tausenderpunkte werden erkannt; Funktionswerte mit Semikolon trennen: root(27; 3), log(8; 2).', 'grund'],
  ['prozent', 'Prozent', '%', 'Anteil, Grundwert, Auf- und Abschlag, Veränderung, Mehrwertsteuer',
    'Prozentwert W = G · p / 100 · Prozentsatz p = W / G · 100 · Grundwert G = W · 100 / p · Aufschlag: G · (1 + p/100) · Veränderung = (neu − alt) / alt · 100 · Brutto = Netto · 1,19 (bzw. 1,07), Netto = Brutto / 1,19.', 'grund'],
  ['dreisatz', 'Dreisatz & Verhältnis', 'a:b', 'Dreisatz und Verhältnisse',
    'Proportional („je mehr, desto mehr“): erst auf 1 teilen, dann mit der gesuchten Menge malnehmen. Umgekehrt proportional („je mehr, desto weniger“): das Produkt bleibt gleich. Rezept: Faktor = gewünschte Portionen / Portionen im Rezept.', 'grund'],
  ['einheiten', 'Einheiten', '⇄', '14 Größen von Länge bis Kraftstoffverbrauch',
    'Wert · Faktor(Ausgangseinheit) = Wert in der Basiseinheit; geteilt durch Faktor(Zieleinheit) = Ergebnis. Faktoren exakt nach SI/NIST: 1 in = 2,54 cm, 1 ft = 0,3048 m, 1 mi = 1609,344 m, 1 lb = 0,45359237 kg, 1 US-gal = 3,785411784 l, 1 acre = 4046,8564224 m², 1 PS = 735,49875 W, 1 kWh = 3,6 MJ, 1 cal = 4,184 J. Temperatur über Kelvin (K = °C + 273,15), Verbrauch über Kehrwerte.', 'grund'],
  ['waehrung', 'Währungen', '€', 'Referenzkurse für 28 Währungen, eigene Kurse möglich',
    'Betrag in Zielwährung = Betrag / Kurs(von) · Kurs(nach); alle Kurse als „1 EUR = …“. Mitgeliefert sind Richtwerte (Stand ' + KURS_STAND + '). Mit Internetverbindung lädt die Seite die aktuellen Referenzkurse der Europäischen Zentralbank über frankfurter.app; eigene Kurse haben Vorrang.', 'grund'],
  ['garten', 'Garten', '❀', 'Saatgut, Jauche, Regenwasser, Mulch, Brennholz, Anbaufläche',
    'Pflanzen = Fläche / (Reihenabstand · Abstand in der Reihe) · Verdünnung 1 : x = 1 Teil Ansatz + x Teile Wasser · Regenertrag = Dachfläche · Niederschlag · Beiwert (1 mm = 1 l/m²) · 1 cm Schicht auf 1 m² = 10 l · Brennholz: 1 Rm ≈ 0,62–0,64 Fm ≈ 1,5–1,6 Srm · Anbaufläche = Verbrauch / Ertrag. Tabellenwerte sind Richtwerte für den Hausgarten.', 'praxis'],
  ['kueche', 'Küche', '♨', 'Rezepte, Küchenmaße, Teig, Backform, Lake, Gelierzucker, Ofen',
    'Rezeptfaktor = gewünschte Portionen / Portionen im Rezept · Teigausbeute TA = (Mehl + Wasser) / Mehl · 100 · Backform-Faktor = Fläche neu / Fläche alt · Salz = Bezugsmenge · Prozent / 100 · Gelierzucker 2 : 1 = halb so viel Zucker wie Frucht · Verdünnen c₁ V₁ = c₂ V₂ · Alkohol ≈ (Dichte vorher − nachher) · 131,25 · Umluft = Ober-/Unterhitze − 20 °C.', 'praxis'],
  ['bau', 'Baustelle', '⌂', 'Rohre, Gefälle, Heizlast, Beton, Putz, Pflaster, Dämmung, Treppe, Angebot',
    'Volumenstrom Q = v · π d² / 4 · Gefälle in % = Höhe / Länge · 100 (1 % = 1 cm je Meter) · Heizlast ≈ Fläche · W/m² · Beton V = Länge · Breite · Dicke · Putz = Fläche · Dicke · kg/m² je mm · U = 1 / (1 / U alt + d / λ) · Treppe: 2 · Steigung + Auftritt = 59–65 cm · Brutto = Netto · 1,19. Überschläge – maßgeblich sind Normen, Herstellerangaben und die Planung.', 'praxis'],
  ['geld', 'Geld', '↗', 'Netto, Zinsen, Kredit, Auto, Photovoltaik, Entnahme',
    'Zinseszins Kₙ = K₀ · (1 + p)ⁿ · Annuität A = K · i / (1 − (1 + i)⁻ⁿ) mit i = Jahreszins / 12 · Kaufkraft = Betrag / (1 + r)ⁿ · Monatsstunden = Wochenstunden · 52 / 12. Reine Rechenhilfen – keine Anlage- oder Finanzberatung.', 'praxis'],
  ['gesundheit', 'Gesundheit', '♡', 'BMI, Kalorien, Eiweiß, Koffein, Schlaf, Puls',
    'BMI = Gewicht / Größe² · Grundumsatz nach Mifflin-St Jeor: 10 · kg + 6,25 · cm − 5 · Alter + 5 (Männer) bzw. − 161 (Frauen) · Gesamtumsatz = Grundumsatz · PAL. Alle Werte sind grobe Richtwerte und ersetzen keine ärztliche Beratung.', 'praxis'],
  ['physik', 'Physik & Technik', 'Ω', 'Strom, Bewegung, Kraft, Druck, Wärme, Gas, Konstanten',
    'U = R · I, P = U · I · E = P · t · s = v · t · F = m · a, W = F · s, Ekin = ½ m v², Epot = m g h · p = F / A · ρ = m / V · freier Fall t = √(2h/g) · Q = m · c · ΔT · p V = n R T. Eingaben in den angegebenen Einheiten; intern wird in SI gerechnet.', 'wissen'],
  ['geometrie', 'Geometrie', '△', 'Flächen, Körper, Pythagoras',
    'Rechteck A = a · b · Dreieck (Heron) A = √(s(s−a)(s−b)(s−c)) · Kreis A = π r², U = 2 π r · Trapez A = (a + c)/2 · h · Quader V = a b c · Zylinder V = π r² h · Kugel V = 4/3 π r³ · Kegel V = ⅓ π r² h · Pythagoras a² + b² = c².', 'wissen'],
  ['chemie', 'Chemie', 'mol', 'Molare Masse, Stoffmenge, Konzentration, pH, Periodensystem',
    'M = Σ (Anzahl · Atommasse) · n = m / M · N = n · Nₐ (Nₐ = 6,02214076 × 10²³ /mol) · c = n / V · c₁ V₁ = c₂ V₂ · pH = −lg c(H⁺), pH + pOH = 14 (25 °C). Nur Rechenhilfen – keine Herstellungs- oder Dosieranleitungen.', 'wissen'],
  ['kalender', 'Kalender & Zeit', '31', 'Wochentage, Feiertage, Zeitzonen, Mond und Sonne',
    'Jedes Datum wird in die Julianische Tageszahl (JD) umgerechnet – eine fortlaufende Zählung der Tage seit dem 1. Januar 4713 v. Chr. Wochentag = (JD + 1) mod 7 (0 = Sonntag). Gregorianisch: Schaltjahr alle 4 Jahre, außer volle Jahrhunderte, die nicht durch 400 teilbar sind; julianisch: jedes 4. Jahr. Astronomische Jahreszählung: Jahr 0 = 1 v. Chr., −1 = 2 v. Chr. So bleiben Rechnungen über Jahrtausende exakt – unabhängig vom Datumsobjekt des Browsers.', 'wissen'],
  ['musik', 'Musik', '♪', 'Tempo und Notenlängen, Frequenz und Note, Kapodaster',
    'Viertelnote in ms = 60 000 / BPM · Frequenz f = Kammerton · 2^(Halbtöne / 12) · 100 Cent = 1 Halbton · Kapodaster: jeder Bund = 1 Halbton höher.', 'wissen'],
  ['zahlen', 'Zahlen & Statistik', 'Σ', 'Binär, Hex, römische Zahlen, Mittelwert, Median, Streuung',
    'Stellenwert: Zahl = Σ Ziffer · Basis^Stelle · Mittelwert = Summe / Anzahl · Median = mittlerer Wert der sortierten Liste · Standardabweichung s = √(Σ (x − Mittelwert)² / (n − 1)).', 'wissen']
];
var BNAME = {}; BEREICHE.forEach(function (b) { BNAME[b[0]] = b[1]; });
KERN.BEREICHE = BEREICHE; KERN.GRUPPEN = GRUPPEN;
/* Verweise auf Rechner, die es an anderer Stelle der App schon gibt */
var VERWEISE = [{ id: 'gs-naehr', b: 'gesundheit', t: 'Nährwerte einer Mahlzeit', u: 'Kalorien, Eiweiß, Fett, Kohlenhydrate, Ballaststoffe', text: 'Der Mahlzeiten-Rechner mit 113 Lebensmitteln, Vorlagen und Tagesziel steht im Kapitel „Nährwerte“.', h: '#s-naehrwerte-naehrliste', knopf: 'Zum Mahlzeiten-Rechner →', s: 'nährwerte mahlzeit kalorien kcal lebensmittel' }];
/* Suche nach Rechnern über Titel, Untertitel und Stichwörter */
function kartenSuche(q) {
  var w = String(q).toLowerCase().split(/[^a-zäöüß0-9]+/).filter(function (x) { return x.length >= 3; }); if (!w.length) return [];
  var L = KARTEN.map(function (k) { return { id: k.id, t: k.t, b: k.b, txt: (k.t + ' ' + (k.u || '') + ' ' + (k.s || '') + ' ' + BNAME[k.b]).toLowerCase() }; }).concat(VERWEISE.map(function (v) { return { id: v.id, t: v.t, b: v.b, txt: (v.t + ' ' + v.u + ' ' + v.s).toLowerCase() }; }));
  var ganz = String(q).toLowerCase().trim(), genau = L.filter(function (k) { return k.txt.indexOf(ganz) >= 0; }); if (genau.length) return genau.slice(0, 8);
  var alle = L.filter(function (k) { return w.every(function (x) { return k.txt.indexOf(x) >= 0; }); });
  return (alle.length ? alle : L.filter(function (k) { return w.some(function (x) { return k.txt.indexOf(x) >= 0; }); })).slice(0, 8);
}
var NEG = { 'einheit.w': 1, 'k-wochentag.j': 1, 'k-monat.j': 1, 'k-jahreszeiten.j': 1, 'waerme.t1': 1, 'waerme.t2': 1, 'gas.T': 1, 'p-veraend.a': 1, 'p-veraend.n': 1, 'p-wert.g': 1, 'p-satz.w': 1 };
var KONSTANTEN = [['c', 'Lichtgeschwindigkeit', '299 792 458 m/s', 'exakt'], ['gₙ', 'Normfallbeschleunigung', '9,806 65 m/s²', 'Norm'], ['G', 'Gravitationskonstante', '6,674 30 × 10⁻¹¹ m³/(kg·s²)', ''],
  ['h', 'Planck-Konstante', '6,626 070 15 × 10⁻³⁴ J·s', 'exakt'], ['ħ', 'reduz. Planck-Konstante', '1,054 571 817 × 10⁻³⁴ J·s', ''], ['k_B', 'Boltzmann-Konstante', '1,380 649 × 10⁻²³ J/K', 'exakt'],
  ['Nₐ', 'Avogadro-Konstante', '6,022 140 76 × 10²³ mol⁻¹', 'exakt'], ['R', 'Gaskonstante', '8,314 462 618 J/(mol·K)', ''], ['e', 'Elementarladung', '1,602 176 634 × 10⁻¹⁹ C', 'exakt'],
  ['mₑ', 'Elektronenmasse', '9,109 383 7 × 10⁻³¹ kg', ''], ['mₚ', 'Protonenmasse', '1,672 621 9 × 10⁻²⁷ kg', ''], ['ε₀', 'elektrische Feldkonstante', '8,854 187 8 × 10⁻¹² F/m', ''],
  ['σ', 'Stefan-Boltzmann-Konstante', '5,670 374 4 × 10⁻⁸ W/(m²·K⁴)', ''], ['Vₘ', 'Molvolumen ideales Gas (0 °C, 1013,25 hPa)', '22,413 97 l/mol', ''], ['p₀', 'Normdruck (atm)', '101 325 Pa', 'exakt'],
  ['T₀', 'absoluter Nullpunkt', '0 K = −273,15 °C', 'exakt'], ['c_Schall', 'Schall in Luft (20 °C)', '≈ 343 m/s', ''], ['c_Wasser', 'spez. Wärme Wasser', '≈ 4186 J/(kg·K)', '']];
var EL_FARBE = { alkali: 'var(--rz-f5)', erdalkali: 'var(--rz-f3)', uebergang: 'var(--rz-f2)', f: 'var(--rz-f4)', metall: 'var(--rz-f8)', halbmetall: 'var(--rz-f6)', nichtmetall: 'var(--rz-f1)', halogen: 'var(--rz-f7)', edelgas: 'var(--rz-f4)' };

function ctxNeu() {
  var k = richtKurse(), info = 'Richtwert Stand ' + KURS_STAND + ', kein Live-Kurs';
  if (ST.kurse && ST.kurse.rates) { for (var c in ST.kurse.rates) if (k[c] != null) k[c] = ST.kurse.rates[c]; var d = String(ST.kurse.datum || '').split('-'); info = 'Stand: ' + (d.length === 3 ? d[2] + '.' + d[1] + '.' + d[0] : ST.kurse.datum) + ', Quelle EZB über frankfurter.app'; }
  var eig = ST.eigene || {}, n = 0; for (var e in eig) if (eig[e] > 0 && k[e] != null) { k[e] = eig[e]; n++; }
  if (n) info += ' · ' + n + ' eigene' + (n === 1 ? 'r Kurs' : ' Kurse');
  return { heute: heuteDatum(), jetzt: Date.now(), kurse: k, kursInfo: info, grad: ST.grad !== false, land: ST.land || 'SL' };
}
function zeigeEing(x) { if (x == null) return ''; if (typeof x === 'number') return String(rund(x, 12)).replace('.', ','); return String(x); }
function rohWerte(def, ctx) {
  var g = (ST.v && ST.v[def.id]) || {}, vor = def.vor ? def.vor(ctx) : {}, w = {};
  def.f.forEach(function (fd) {
    var x = g[fd.k];
    if (x === undefined) x = vor[fd.k] !== undefined ? vor[fd.k] : (fd.land ? (ST.land || fd.w) : fd.w);
    w[fd.k] = x;
  });
  def.f.forEach(function (fd) {
    if (fd.typ !== 'wahl') return;
    var opts = typeof fd.opt === 'function' ? fd.opt(w) : fd.opt;
    if (!opts.some(function (o) { return o[0] === w[fd.k]; })) w[fd.k] = def.id === 'einheit' && STD_PAAR[w.kat] ? STD_PAAR[w.kat][fd.k === 'von' ? 0 : 1] : opts[0][0];
  });
  return w;
}
function feldZahl(r) { if (r == null || String(r).trim() === '') return null; if (typeof r === 'number') return r; var n = zahlLesen(r); if (!isNaN(n)) return n; try { return ausdruck(r).wert; } catch (e) { return NaN; } }
function sichtbar(fd, w) { if (!fd.nur) return true; for (var k in fd.nur) if (fd.nur[k].indexOf(w[k]) < 0) return false; return true; }
function feldHTML(def, fd, w) {
  var val = w[fd.k], hid = sichtbar(fd, w) ? '' : ' hidden', uid = 'rz-' + def.id + '-' + fd.k;
  if (fd.typ === 'wahl') {
    var opts = typeof fd.opt === 'function' ? fd.opt(w) : fd.opt;
    if (fd.segment) return '<div class="rz-feld rz-voll"' + hid + '><span class="rz-fl" id="' + uid + '">' + esc(fd.l) + '</span><div class="rz-seg" role="radiogroup" aria-labelledby="' + uid + '">' +
      opts.map(function (o) { var an = o[0] === val; return '<button type="button" role="radio" aria-checked="' + an + '" tabindex="' + (an ? 0 : -1) + '" data-k="' + fd.k + '" data-v="' + esc(o[0]) + '">' + esc(o[1]) + '</button>'; }).join('') + '</div></div>';
    return '<label class="rz-feld' + (fd.tausch ? ' rz-mit-tausch' : '') + '"' + hid + '><span class="rz-fl">' + esc(fd.l) + '</span><span class="rz-sel"><select data-k="' + fd.k + '">' +
      opts.map(function (o) { return '<option value="' + esc(o[0]) + '"' + (o[0] === val ? ' selected' : '') + '>' + esc(o[1]) + '</option>'; }).join('') + '</select></span></label>' +
      (fd.tausch ? '<button type="button" class="rz-tausch" data-a="' + fd.tausch + '" data-b="' + fd.k + '" aria-label="' + esc(fd.tausch === 'von' ? 'Von und Nach tauschen' : 'tauschen') + '">⇅</button>' : '');
  }
  if (fd.typ === 'text' && fd.zeilen) return '<label class="rz-feld rz-voll"' + hid + '><span class="rz-fl">' + esc(fd.l) + '</span><textarea data-k="' + fd.k + '" rows="' + fd.zeilen + '" spellcheck="false">' + esc(zeigeEing(val)) + '</textarea></label>';
  var im = fd.typ === 'text' || fd.typ === 'datum' || NEG[def.id + '.' + fd.k] ? 'text' : 'decimal', ph = fd.typ === 'datum' ? 'TT.MM.JJJJ – leer = heute' : '';
  return '<label class="rz-feld' + (fd.formel || (fd.typ === 'text' && !fd.kurz) || fd.typ === 'datum' ? ' rz-breitfeld' : '') + '"' + hid + '><span class="rz-fl">' + esc(fd.l) + '</span><span class="rz-ein"><input type="text" inputmode="' + im + '" data-k="' + fd.k + '" value="' + esc(zeigeEing(val)) + '"' + (ph ? ' placeholder="' + ph + '"' : '') + ' autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false" enterkeyhint="done">' + (fd.e ? '<em>' + esc(fd.e) + '</em>' : '') + '</span></label>';
}
var FORMEL_BSP = ['H2O', 'NaCl', 'H2SO4', 'CuSO4·5H2O', 'Ca(OH)2', 'C6H12O6', 'CO2', 'NH3', 'Glucose'];
function karteHTML(def, ctx) {
  var w = rohWerte(def, ctx), h = '<article class="rz-karte' + (def.breit ? ' rz-breit' : '') + '" data-k="' + def.id + '" id="rz-k-' + def.id + '" aria-labelledby="rz-kt-' + def.id + '"><header class="rz-kh"><h3 id="rz-kt-' + def.id + '" tabindex="-1">' + esc(def.t) + '</h3>' + (def.u ? '<p>' + esc(def.u) + '</p>' : '') + '</header><div class="rz-felder">';
  def.f.forEach(function (fd) { h += feldHTML(def, fd, w); });
  h += '</div>';
  if (def.id === 'molmasse') h += '<div class="rz-chips rz-chips-k" aria-label="Beispiele">' + FORMEL_BSP.map(function (f) { return '<button type="button" class="rz-chip" data-formel="' + esc(f) + '">' + formelHuebsch(f) + '</button>'; }).join('') + '</div>';
  return h + '<div class="rz-aus" aria-live="polite"></div></article>';
}
function ergebnisHTML(e, opt) {
  opt = opt || {};
  var dopp = false;
  if (e.kurs && typeof e.wert === 'number') { var hw0 = e.kurs.s[0].w, last = hw0[hw0.length - 1]; dopp = Math.abs(last - e.wert) <= 1e-6 * Math.max(1, Math.abs(e.wert)); if (dopp) e.kurs.titel = e.label; }
  var h = '<div class="rz-erg"><div class="rz-ek"' + (dopp ? ' hidden' : '') + '><div class="rz-gross"><span class="rz-zahl">' + esc(e.gross) + '</span>' + (e.einh ? ' <span class="rz-einh">' + esc(e.einh) + '</span>' : '') + '</div>' +
    (e.label ? '<div class="rz-label">' + (e.labelHtml ? e.label : esc(e.label)) + '</div>' : '') + '</div>';
  if (e.kurs) { var kid = 'k' + (++KURS_Z); KURS_DATEN[kid] = e.kurs; h += '<div class="rz-kurs" data-kid="' + kid + '"></div>'; }
  if (e.svg) h += '<div class="rz-dia">' + e.svg + '</div>';
  if (e.zeilen && e.zeilen.length) {
    h += (e.zeilenTitel ? '<h4 class="rz-zt">' + esc(e.zeilenTitel) + '</h4>' : '') + '<dl class="rz-zeilen">' + e.zeilen.map(function (z) { return '<div><dt>' + (e.zeilenHtml ? z[0] : esc(z[0])) + '</dt><dd>' + (e.zeilenHtml ? z[1] : esc(z[1])) + '</dd></div>'; }).join('') + '</dl>';
  }
  if (e.schritte && e.schritte.length) h += '<details class="rz-weg"' + (opt.wegOffen ? ' open' : '') + '><summary>Rechenweg</summary><ol>' + e.schritte.map(function (s) { return '<li>' + esc(s) + '</li>'; }).join('') + '</ol></details>';
  if (e.hinweis) h += '<p class="rz-hinweis">' + esc(e.hinweis) + '</p>';
  return h + '</div>';
}
function karteRechnen(card, anim) {
  var id = card.getAttribute('data-k'), def = KARTE[id]; if (!def) return;
  var ctx = ctxNeu(), w = rohWerte(def, ctx), v = {}, out = card.querySelector('.rz-aus'), unlesbar = [];
  def.f.forEach(function (fd) {
    if (fd.typ) { v[fd.k] = w[fd.k]; return; }
    v[fd.k] = feldZahl(w[fd.k]);
    var inp = card.querySelector('input[data-k="' + fd.k + '"]');
    if (inp) { if (typeof v[fd.k] === 'number' && isNaN(v[fd.k])) { inp.setAttribute('aria-invalid', 'true'); unlesbar.push(fd.l); v[fd.k] = null; } else inp.removeAttribute('aria-invalid'); }
  });
  var offen = !!out.querySelector('details.rz-weg[open]'), h;
  try { h = ergebnisHTML(def.r(v, ctx), { wegOffen: offen }); }
  catch (err) { h = err && err.leer ? '<p class="rz-leer">' + esc(err.message) + '</p>' : '<p class="rz-fehler" role="alert">' + esc(err && err.message ? err.message : String(err)) + '</p>'; }
  if (unlesbar.length) h = '<p class="rz-fehler" role="alert">Eingabe nicht lesbar: ' + esc(unlesbar.join(', ')) + ' – bitte Zahl wie 2,5 oder 1.250 eingeben.</p>' + h;
  out.innerHTML = h;
  out.classList.toggle('rz-anim', !!anim && !bewegungAus());
  kurseMalen(out);
}
function karteNeu(R, id, fokus) {
  var alt = R.querySelector('.rz-karte[data-k="' + id + '"]:not(.rz-ant)'); if (!alt) return null;
  var tmp = document.createElement('div'); tmp.innerHTML = karteHTML(KARTE[id], ctxNeu());
  var neu = tmp.firstChild; alt.parentNode.replaceChild(neu, alt); karteRechnen(neu, true);
  if (fokus) { var f = neu.querySelector(fokus); if (f) f.focus(); }
  return neu;
}
function wertSetzen(id, k, val) { ST.v = ST.v || {}; ST.v[id] = ST.v[id] || {}; ST.v[id][k] = val; sichern(); }

/* ---------- Verlaufsdiagramm (Börsenkurs-Stil) ---------- */
function kurseMalen(box) { var L = box.querySelectorAll('.rz-kurs[data-kid]'); for (var i = 0; i < L.length; i++) { var el = L[i], kid = el.getAttribute('data-kid'); if (KURS_DATEN[kid]) { el._d = KURS_DATEN[kid]; delete KURS_DATEN[kid]; el._von = 0; } kursZeichnen(el); } }
function kfmt(d, x) { return d.fmt === 'geld' ? geld(x) : zahl(x, 6); }
function kursZeichnen(el) {
  var d = el._d; if (!d) return;
  var n = d.x.length, von = el._von || 0, bis = n - 1, W0 = el.clientWidth || (el.parentNode && el.parentNode.clientWidth) || 600;
  var opt = [[5, '5 J'], [10, '10 J'], [25, '25 J']].filter(function (o) { return o[0] < n - 1; }), h = '';
  h += '<div class="rz-kk"><div class="rz-kkl"><div class="rz-kwert"></div><div class="rz-kdelta"></div><div class="rz-kinfo"></div></div>';
  if (opt.length) h += '<div class="rz-kzr" role="group" aria-label="Zeitraum">' + opt.map(function (o) { var an = von === n - 1 - o[0]; return '<button type="button" data-zr="' + o[0] + '" aria-pressed="' + an + '">' + o[1] + '</button>'; }).join('') + '<button type="button" data-zr="0" aria-pressed="' + (von === 0) + '">Max</button></div>';
  h += '</div>';
  var g = kursSVG(d, Math.max(260, W0), von, bis); el._g = g;
  h += '<div class="rz-kplot">' + g.svg + '</div>';
  var hw = d.s[0].w.slice(von, bis + 1), hi = Math.max.apply(null, hw), lo = Math.min.apply(null, hw);
  h += '<div class="rz-kstat"><span>Hoch <b>' + kfmt(d, hi) + '</b></span><span>Tief <b>' + kfmt(d, lo) + '</b></span><span>Start <b>' + kfmt(d, d.s[0].w[von]) + '</b></span></div>';
  h += '<ul class="rz-kleg">' + d.s.map(function (s, i) { return '<li><i class="' + (i ? 'rz-strich' : '') + '" style="background:' + s.f + '"></i>' + esc(s.n) + '</li>'; }).join('') + '</ul>';
  el.innerHTML = h;
  kursMarke(el, null);
}
function kursMarke(el, idx) {
  var d = el._d, g = el._g; if (!d || !g) return;
  var aktiv = idx != null, i = aktiv ? idx : g.bis, v0 = d.s[0].w[g.von], v = d.s[0].w[i], dv = v - v0, gut = d.fallendGut ? dv <= 0 : dv >= 0;
  el.querySelector('.rz-kwert').textContent = kfmt(d, v);
  var de = el.querySelector('.rz-kdelta');
  de.textContent = (dv > 0 ? '▲ +' : dv < 0 ? '▼ −' : '■ ') + kfmt(d, Math.abs(dv)) + (v0 ? ' (' + (dv >= 0 ? '+' : '−') + dz(Math.abs(dv / v0 * 100), 1) + ' %)' : '');
  de.className = 'rz-kdelta ' + (dv === 0 ? '' : gut ? 'rz-gut' : 'rz-schlecht');
  el.querySelector('.rz-kinfo').textContent = aktiv ? d.x[i] + ': ' + d.s.map(function (s) { return s.n + ' ' + kfmt(d, s.w[i]); }).join(' · ') : (d.titel ? d.titel + ' · ' : d.s[0].n + ' · ') + 'Zeitraum ' + d.x[g.von] + ' – ' + d.x[g.bis];
  var m = el.querySelector('.rz-km'); if (!m) return;
  m.style.display = aktiv ? '' : 'none';
  if (aktiv) {
    var x = g.X(i).toFixed(1), l = m.querySelector('line'); l.setAttribute('x1', x); l.setAttribute('x2', x);
    var c = m.querySelectorAll('circle'); d.s.forEach(function (s, k) { c[k].setAttribute('cx', x); c[k].setAttribute('cy', g.Y(s.w[i]).toFixed(1)); });
  }
  el._i = aktiv ? i : null;
}
function kursZeiger(ev) {
  var svg = ev.target.closest && ev.target.closest('.rz-ksvg'); if (!svg) return;
  var el = svg.closest('.rz-kurs'), g = el._g; if (!g) return;
  var r = svg.getBoundingClientRect(), x = (ev.clientX - r.left) / r.width * svg.viewBox.baseVal.width, best = g.von, bd = 1e9;
  for (var i = g.von; i <= g.bis; i++) { var dd = Math.abs(g.X(i) - x); if (dd < bd) { bd = dd; best = i; } }
  kursMarke(el, best);
}

/* ---------- Seite aufbauen ---------- */
function heuteHTML(ctx) {
  var h = ctx.heute, J = jdnG(h.y, h.m, h.d), kw = isoWoche(J), ph = mondphase(J), land = ctx.land, nf2 = null;
  [h.y, h.y + 1].forEach(function (y) { feiertage(y, land).forEach(function (f) { if (!nf2 && f.g && f.J >= J) nf2 = f; }); });
  var usd = ctx.kurse.USD;
  return '<section class="rz-heute" aria-label="Heute auf einen Blick"><div class="rz-hk rz-hk-tag"><span class="rz-ober">Heute</span><b>' + WT[wochentag(J)] + '</b><span>' + datumLang(h) + '</span><small>KW ' + kw.w + ' · Tag ' + tagDesJahres(h, 'g') + ' von ' + (schaltG(h.y) ? 366 : 365) + '</small></div>' +
    '<div class="rz-hk"><span class="rz-ober">Mond (Näherung)</span><div class="rz-hm">' + mondSVG(ph.f) + '<span><b>' + ph.name + '</b><small>' + dz(ph.beleuchtet * 100, 0) + ' % beleuchtet</small></span></div></div>' +
    '<div class="rz-hk"><span class="rz-ober">Nächster Feiertag (' + land + ')</span><b>' + (nf2 ? esc(nf2.n) : '–') + '</b><small>' + (nf2 ? WTK[wochentag(nf2.J)] + ', ' + datumKurz(ausJdnG(nf2.J)) + (nf2.J === J ? ' · heute' : ' · in ' + (nf2.J - J) + ' Tagen') : '') + '</small></div>' +
    '<div class="rz-hk"><span class="rz-ober">Euro</span><b>1 € = ' + zahl(usd, 4) + ' $</b><small class="rz-kursinfo">' + esc(ctx.kursInfo.split(' · ')[0]) + '</small></div></section>';
}
function rechnerHTML() {
  var T1 = [['C', 'C', 'rz-t2', 'Alles löschen'], ['(', '(', 'rz-t2'], [')', ')', 'rz-t2'], ['/', '÷', 'rz-t3', 'geteilt'], ['7', '7'], ['8', '8'], ['9', '9'], ['*', '×', 'rz-t3', 'mal'], ['4', '4'], ['5', '5'], ['6', '6'], ['-', '−', 'rz-t3', 'minus'],
    ['1', '1'], ['2', '2'], ['3', '3'], ['+', '+', 'rz-t3', 'plus'], ['%', '%', 'rz-t2', 'Prozent'], ['0', '0'], [',', ',', '', 'Komma'], ['=', '=', 'rz-t4', 'ist gleich']];
  var T2 = [['sin(', 'sin'], ['cos(', 'cos'], ['tan(', 'tan'], ['^', 'xʸ'], ['^2', 'x²'], ['√(', '√'], ['asin(', 'sin⁻¹'], ['acos(', 'cos⁻¹'], ['atan(', 'tan⁻¹'], ['ln(', 'ln'], ['log(', 'log'], ['!', 'n!'], ['π', 'π'], ['e', 'e'], ['1/(', '1/x'], ['∛(', '∛'], [';', ';'], ['ans', 'Ans']];
  var t = function (L, cls) { return L.map(function (k) { return '<button type="button" class="rz-taste ' + (k[2] || '') + '" data-t="' + esc(k[0]) + '"' + (k[3] ? ' aria-label="' + k[3] + '"' : '') + '>' + esc(k[1]) + '</button>'; }).join(''); };
  return '<article class="rz-karte rz-rechner" data-r="1" aria-labelledby="rz-rt"><header class="rz-kh"><h3 id="rz-rt" tabindex="-1">Rechner</h3><p>Tippen oder tippen lassen – Enter rechnet</p></header>' +
    '<div class="rz-display"><label class="rz-vh" for="rz-rein">Rechenausdruck</label><input id="rz-rein" class="rz-rein" type="text" inputmode="none" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false" placeholder="0"><output class="rz-rout" for="rz-rein" aria-live="polite"></output><button type="button" class="rz-taste rz-zurueck" data-t="⌫" aria-label="Letztes Zeichen löschen">⌫</button></div>' +
    '<div class="rz-rmod"><div class="rz-seg rz-seg-k" role="radiogroup" aria-label="Winkelmaß"><button type="button" role="radio" data-grad="1" aria-checked="' + (ST.grad !== false) + '">Grad</button><button type="button" role="radio" data-grad="0" aria-checked="' + (ST.grad === false) + '">Bogenmaß</button></div>' +
    '<button type="button" class="rz-klein" data-wiss aria-expanded="' + (!!ST.wiss) + '">Wissenschaftlich</button><button type="button" class="rz-klein" data-tast aria-label="Bildschirmtastatur des Geräts verwenden">Tastatur</button></div>' +
    '<div class="rz-wiss"' + (ST.wiss ? '' : ' hidden') + '>' + t(T2) + '</div><div class="rz-tasten">' + t(T1) + '</div><div class="rz-aus rz-raus" aria-live="polite"></div></article>' +
    '<article class="rz-karte" aria-labelledby="rz-vt"><header class="rz-kh"><h3 id="rz-vt">Verlauf</h3><p>die letzten 20 Rechnungen – antippen übernimmt</p></header><ol class="rz-rverl"></ol><button type="button" class="rz-klein" data-rverl-leer>Verlauf leeren</button></article>';
}
function periodenHTML() {
  var h = '<article class="rz-karte rz-breit" data-pse="1" aria-labelledby="rz-pse-t"><header class="rz-kh"><h3 id="rz-pse-t">Periodensystem</h3><p>Element antippen für Details – alle 118 Elemente</p></header><div class="rz-pse-box"><div class="rz-pse" role="grid" aria-label="Periodensystem der Elemente">';
  ELEMENTE.forEach(function (e) {
    h += '<button type="button" class="rz-el" data-z="' + e.z + '" style="grid-row:' + e.zeile + ';grid-column:' + e.spalte + ';background:' + EL_FARBE[e.kat] + (e.kat === 'f' ? ';opacity:.82' : '') + '" aria-label="' + esc(e.n + ', ' + e.s + ', Ordnungszahl ' + e.z) + '"><small>' + e.z + '</small>' + e.s + '</button>';
  });
  h += '<span class="rz-pse-lu" style="grid-row:6;grid-column:3">57–71</span><span class="rz-pse-lu" style="grid-row:7;grid-column:3">89–103</span></div></div><ul class="rz-leg rz-pse-leg">';
  for (var k in KAT_EL) if (k !== 'edelgas' || true) h += '<li><i style="background:' + EL_FARBE[k] + (k === 'f' ? ';opacity:.82' : '') + '"></i><span>' + KAT_EL[k] + '</span></li>';
  return h + '</ul><div class="rz-elinfo" aria-live="polite"><p class="rz-leer">Kein Element gewählt.</p></div></article>';
}
function elementHTML(e) {
  return '<div class="rz-elk"><div class="rz-elbig" style="background:' + EL_FARBE[e.kat] + '"><small>' + e.z + '</small><b>' + e.s + '</b><span>' + (e.instabil ? '[' + e.m + ']' : dz(e.m, 3)) + '</span></div><div><h4>' + esc(e.n) + '</h4><dl class="rz-zeilen">' +
    elementZeilen(e).slice(2).map(function (z) { return '<div><dt>' + esc(z[0]) + '</dt><dd>' + esc(z[1]) + '</dd></div>'; }).join('') + '</dl><button type="button" class="rz-klein" data-elformel="' + e.s + '">In Summenformel übernehmen</button></div></div>';
}
function kurseKarteHTML(ctx) {
  var eig = ST.eigene || {};
  return '<article class="rz-karte rz-breit" data-kurse="1" aria-labelledby="rz-ku-t"><header class="rz-kh"><h3 id="rz-ku-t">Kurse (1 EUR = …)</h3><p class="rz-kursinfo">' + esc(ctx.kursInfo) + '</p></header>' +
    '<p class="rz-hinweis">Richtwert, kein Live-Kurs – außer die EZB-Referenzkurse wurden geladen (werktags gegen 16 Uhr aktualisiert). Eigene Werte überschreiben den Kurs.</p>' +
    '<div class="rz-aktion"><button type="button" class="rz-knopf" data-kurse-laden>Online aktualisieren</button><button type="button" class="rz-klein" data-kurse-reset>Eigene Kurse löschen</button></div>' +
    '<details class="rz-weg rz-kursauf"><summary>Alle Kurse ansehen und eigene eintragen</summary><div class="rz-kursliste">' + WAEHRUNGEN.slice(1).map(function (w) {
      return '<label class="rz-feld"><span class="rz-fl">' + w[0] + ' – ' + esc(w[1]) + '</span><span class="rz-ein"><input type="text" inputmode="decimal" data-eigen="' + w[0] + '" value="' + (eig[w[0]] ? zeigeEing(eig[w[0]]) : '') + '" placeholder="' + esc(zahl(ctx.kurse[w[0]] && !eig[w[0]] ? ctx.kurse[w[0]] : richtKurse()[w[0]], 6)) + '" autocomplete="off"></span></label>';
    }).join('') + '</div></details></article>';
}
function konstHTML() {
  return '<article class="rz-karte rz-breit" aria-labelledby="rz-ko-t"><header class="rz-kh"><h3 id="rz-ko-t">Naturkonstanten</h3><p>SI 2019 / CODATA – „exakt“ = per Definition festgelegt</p></header><div class="rz-tabbox"><table class="rz-tab"><thead><tr><th scope="col">Zeichen</th><th scope="col">Größe</th><th scope="col">Wert</th></tr></thead><tbody>' +
    KONSTANTEN.map(function (k) { return '<tr><th scope="row">' + esc(k[0]) + '</th><td>' + esc(k[1]) + '</td><td class="rz-num">' + esc(k[2]) + (k[3] ? ' <small>' + k[3] + '</small>' : '') + '</td></tr>'; }).join('') + '</tbody></table></div></article>';
}
function kalWissenHTML() {
  return '<article class="rz-karte rz-breit" aria-labelledby="rz-kwi-t"><header class="rz-kh"><h3 id="rz-kwi-t">Kalenderwissen kurz</h3></header><div class="rz-text">' +
    '<p><b>Julianischer Kalender</b> – 45 v. Chr. von Julius Caesar eingeführt; jedes vierte Jahr ist ein Schaltjahr. Das Jahr ist dadurch im Mittel 11 Minuten zu lang.</p>' +
    '<p><b>Gregorianischer Kalender</b> – 1582 von Papst Gregor XIII. eingeführt: Auf Donnerstag, 4. Oktober folgte direkt Freitag, 15. Oktober 1582. Volle Jahrhunderte sind nur Schaltjahre, wenn sie durch 400 teilbar sind (2000 ja, 1900 nein). Evangelische Gebiete Deutschlands stellten 1700 um, Großbritannien 1752, Russland 1918.</p>' +
    '<p><b>Proleptisch</b> heißt: Ein Kalender wird über seine Einführung hinaus zurückgerechnet. Für „vor 5000 Jahren“ gab es weder diese Kalender noch die heutige Jahreszählung – der Wochentag ist aber eindeutig, weil die Siebentagewoche rechnerisch lückenlos durchläuft.</p>' +
    '<p><b>Jahr 0</b> – Historiker zählen 1 v. Chr. → 1 n. Chr. ohne Jahr 0. Die Astronomie verwendet Jahr 0 = 1 v. Chr., −1 = 2 v. Chr. usw.; so funktionieren Schaltjahrregeln und Differenzen ohne Sonderfall.</p>' +
    '<p><b>Julianische Tageszahl</b> – fortlaufende Tageszählung seit 1. Januar 4713 v. Chr. (julianisch), 12 Uhr Weltzeit. Sie ist das Werkzeug, mit dem hier alle Datumsrechnungen laufen.</p></div></article>';
}
function kartenVon(id) { return KARTEN.filter(function (k) { return k.b === id; }); }
function verweisHTML(v) { return '<article class="rz-karte rz-verweis" id="rz-k-' + v.id + '"><header class="rz-kh"><h3 tabindex="-1">' + esc(v.t) + '</h3><p>' + esc(v.u) + '</p></header><p class="rz-vt">' + esc(v.text) + '</p><a class="rz-knopf rz-link" href="' + esc(v.h) + '">' + esc(v.knopf) + '</a></article>'; }
function sprungHTML(id) {
  var L = kartenVon(id).map(function (k) { return [k.id, k.t]; }).concat(VERWEISE.filter(function (v) { return v.b === id; }).map(function (v) { return [v.id, v.t]; }));
  if (L.length < 4) return '';
  return '<nav class="rz-inh" aria-label="Rechner in diesem Bereich"><span class="rz-vl">' + L.length + ' Rechner</span><div class="rz-chips">' + L.map(function (x) { return '<button type="button" class="rz-chip" data-karte="' + x[0] + '">' + esc(x[1]) + '</button>'; }).join('') + '</div></nav>';
}
function bereichHTML(b, ctx) {
  var id = b[0], h = '<section class="rz-bereich" hidden data-b="' + id + '" id="rz-b-' + id + '" aria-labelledby="rz-bt-' + id + '"><button type="button" class="rz-heim" data-ziel="">‹ Alle Bereiche</button><header class="rz-bk"><span class="rz-ic" aria-hidden="true">' + b[2] + '</span><div><h2 id="rz-bt-' + id + '">' + esc(b[1]) + '</h2><p>' + esc(b[3]) + '</p></div></header>' +
    '<details class="rz-so"><summary>So wird gerechnet</summary><p>' + esc(b[4]) + '</p></details>' + (id === 'gesundheit' ? '<p class="rz-warn">Neutrale Rechenhilfen – ersetzen keine ärztliche Beratung.</p>' : '') + sprungHTML(id) + '<div class="rz-grid">';
  if (id === 'rechner') h += rechnerHTML();
  KARTEN.forEach(function (k) { if (k.b === id) h += karteHTML(k, ctx); });
  if (id === 'waehrung') h += kurseKarteHTML(ctx);
  if (id === 'physik') h += konstHTML();
  if (id === 'chemie') h += periodenHTML();
  VERWEISE.forEach(function (v) { if (v.b === id) h += verweisHTML(v); });
  if (id === 'kalender') h += kalWissenHTML();
  return h + '</div></section>';
}
function chipsHTML(L, cls) { return L.map(function (q) { return '<button type="button" class="rz-chip ' + (cls || '') + '" data-q="' + esc(q) + '">' + esc(q) + '</button>'; }).join(''); }
function verlaufHTML() {
  var v = ST.verlauf || [], f = ST.fav || [];
  if (!v.length && !f.length) return '';
  return (f.length ? '<div class="rz-vz"><span class="rz-vl">★ Favoriten</span><div class="rz-chips">' + chipsHTML(f, 'rz-chip-fav') + '</div></div>' : '') +
    (v.length ? '<div class="rz-vz"><span class="rz-vl">Zuletzt</span><div class="rz-chips">' + chipsHTML(v.slice(0, 20)) + '</div><button type="button" class="rz-klein" data-verl-leer>leeren</button></div>' : '');
}
function aufbau(ctx) {
  var nav = '<button type="button" data-ziel="" aria-current="true"><span aria-hidden="true">⌂</span>Übersicht</button>', kach = '';
  GRUPPEN.forEach(function (g) {
    var B = BEREICHE.filter(function (b) { return b[5] === g[0]; });
    nav += '<span class="rz-nt" aria-hidden="true">' + esc(g[1]) + '</span>' + B.map(function (b) { return '<button type="button" data-ziel="' + b[0] + '"><span aria-hidden="true">' + b[2] + '</span>' + esc(b[1]) + '</button>'; }).join('');
    kach += '<h2 class="rz-gt">' + esc(g[1]) + '</h2><div class="rz-kacheln">' + B.map(function (b) { var n = kartenVon(b[0]).length + VERWEISE.filter(function (v) { return v.b === b[0]; }).length + (b[0] === 'rechner' ? 1 : 0); return '<button type="button" class="rz-kachel" data-ziel="' + b[0] + '"><span class="rz-ic" aria-hidden="true">' + b[2] + '</span><b>' + esc(b[1]) + '</b><small>' + esc(b[3]) + '</small><em>' + n + ' Rechner</em></button>'; }).join('') + '</div>';
  });
  var h = '<header class="rz-kopf"><p class="rz-ober">Werkzeug · offline</p><h1>Rechner &amp; Umrechner</h1><p class="rz-intro">Rechnen, umrechnen, nachschlagen – vom Prozentwert bis zum Periodensystem, vom Saatgut bis zum Angebot. Alles läuft ohne Netz direkt im Gerät.</p></header>' +
    '<div class="rz-leiste"><form class="rz-frage" role="search" aria-label="Frage stellen"><label class="rz-vh" for="rz-fq">Frage, Rechnung oder Name eines Rechners eingeben</label><span class="rz-fi" aria-hidden="true">?</span>' +
    '<input id="rz-fq" type="search" enterkeyhint="go" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false" placeholder="z. B. 5 km in Meilen · 15 % von 240 · Treppe · Salzlake">' +
    '<button type="submit" class="rz-los" aria-label="Berechnen">=</button></form>' +
    '<nav class="rz-nav" aria-label="Bereiche">' + nav + '</nav></div>' +
    '<div class="rz-verlauf">' + verlaufHTML() + '</div><div class="rz-antwort"></div>' +
    '<div class="rz-start"><div class="rz-chips rz-bsp" aria-label="Beispiele">' + chipsHTML(BEISPIELE) + '</div>' + heuteHTML(ctx) + '<section aria-label="Alle Bereiche">' + kach + '</section></div>';
  BEREICHE.forEach(function (b) { h += bereichHTML(b, ctx); });
  return h + '<p class="rz-fuss">Rechenhilfen ohne Gewähr. Umrechnungsfaktoren nach SI/NIST, Atommassen nach IUPAC, Kalender über die Julianische Tageszahl. Währungen: Richtwerte bzw. EZB-Referenzkurse. Tabellenwerte für Garten, Küche und Baustelle sind Richtwerte.</p>';
}
/* Zeigt genau einen Bereich (oder mit id = '' die Übersicht); Karten werden erst beim ersten Öffnen gerechnet */
function zeige(R, id, ohneRollen) {
  id = id && BNAME[id] ? id : '';
  var B = R.querySelectorAll('.rz-bereich'), s = null;
  for (var i = 0; i < B.length; i++) { var an = B[i].getAttribute('data-b') === id; B[i].hidden = !an; if (an) s = B[i]; }
  R.querySelector('.rz-start').hidden = !!id;
  navAktiv(R, id);
  var nb = R.querySelector('.rz-nav button[aria-current="true"]'); if (nb && nb.scrollIntoView && !ohneRollen) try { nb.scrollIntoView({ block: 'nearest', inline: 'center' }); } catch (e) { /* alt */ }
  if (s) {
    if (!s._fertig) { var L = s.querySelectorAll('.rz-karte[data-k]'); for (var j = 0; j < L.length; j++) karteRechnen(L[j], true); s._fertig = true; if (id === 'rechner') rechnerVerlauf(R); }
    else { var K2 = s.querySelectorAll('.rz-kurs'); for (var k = 0; k < K2.length; k++) kursZeichnen(K2[k]); }
  }
  if (!ohneRollen) { var ziel = s || R; ziel.scrollIntoView({ behavior: 'auto', block: 'start' }); if (s) { var h2 = s.querySelector('h2'); h2.setAttribute('tabindex', '-1'); try { h2.focus({ preventScroll: true }); } catch (e2) { /* alt */ } } }
  return s;
}
function zurKarte(R, id) {
  var k = KARTE[id], v = null; if (!k) { v = VERWEISE.filter(function (x) { return x.id === id; })[0]; if (!v) return; }
  zeige(R, (k || v).b, true);
  var ziel = R.querySelector('#rz-k-' + id); if (!ziel) return;
  ziel.scrollIntoView({ behavior: 'auto', block: 'start' });
  ziel.classList.remove('rz-blitz'); void ziel.offsetWidth; ziel.classList.add('rz-blitz');
  var hd = ziel.querySelector('h3'); if (hd) try { hd.focus({ preventScroll: true }); } catch (e) { hd.focus(); }
}

/* ---------- Fragefeld ---------- */
function antwortZeigen(R, q) {
  var box = R.querySelector('.rz-antwort'), ctx = ctxNeu(), e = frageAuswerten(q, ctx), h;
  if (!e) { box.innerHTML = ''; return; }
  var fav = (ST.fav || []).indexOf(q) >= 0;
  var treffer = e.unbekannt ? kartenSuche(q) : [];
  if (treffer.length) {
    h = '<article class="rz-karte rz-ant rz-ant-leer" tabindex="-1"><header class="rz-kh"><p class="rz-ober">Passende Rechner</p></header><div class="rz-chips">' + treffer.map(function (k) { return '<button type="button" class="rz-chip" data-karte="' + k.id + '">' + esc(k.t) + ' <small>· ' + esc(BNAME[k.b]) + '</small></button>'; }).join('') + '</div></article>';
  } else if (e.unbekannt || e.fehler && !e.karte) {
    h = '<article class="rz-karte rz-ant rz-ant-leer" tabindex="-1"><header class="rz-kh"><p class="rz-ober">Fragefeld</p></header><p class="rz-ant-t">' + (e.fehler ? esc(e.fehler) : 'Das habe ich leider nicht verstanden.') + '</p>' +
      '<p class="rz-mini">Ich verstehe Rechnungen, Umrechnungen und Fragen in kurzer Form. Probieren Sie zum Beispiel:</p><div class="rz-chips">' + chipsHTML(['12 % von 80', '3 Meilen in km', '100 € in CHF', 'molare Masse NaCl', 'Wochentag 1.1.1900', 'Tage bis 24.12.', 'Kreis r=2 Umfang', 'Wurzel aus 81']) + '</div></article>';
  } else {
    var bn = e.karte === 'rechner' ? 'Rechner' : (KARTE[e.karte] ? BNAME[KARTE[e.karte].b] : '');
    h = '<article class="rz-karte rz-ant" tabindex="-1" aria-label="Ergebnis"><header class="rz-kh"><p class="rz-ober">' + esc((bn ? bn + ' · ' : '') + (e.titel || '')) + '</p><button type="button" class="rz-stern" aria-pressed="' + fav + '" aria-label="Als Favorit merken">' + (fav ? '★' : '☆') + '</button></header>' +
      (e.fehler ? '<p class="rz-fehler" role="alert">' + esc(e.fehler) + '</p>' : ergebnisHTML(e, { wegOffen: true })) + (e.element ? elementHTML(e.element) : '') +
      '<div class="rz-aktion">' + (e.karte ? '<button type="button" class="rz-knopf" data-oeffnen>Im Rechner öffnen →</button>' : '') + (e.gross ? '<button type="button" class="rz-klein" data-kopie>Ergebnis kopieren</button>' : '') + '</div></article>';
  }
  box.innerHTML = h;
  var art = box.firstChild; art._e = e; art._q = q;
  art.classList.toggle('rz-anim', !bewegungAus());
  kurseMalen(art);
  if (treffer.length === 1) zurKarte(R, treffer[0].id);
  if (!e.unbekannt) { ST.verlauf = [q].concat((ST.verlauf || []).filter(function (x) { return x !== q; })).slice(0, 20); sichern(); R.querySelector('.rz-verlauf').innerHTML = verlaufHTML(); }
}
function oeffnen(R, karte, werte) {
  var ziel;
  zeige(R, karte === 'rechner' ? 'rechner' : (KARTE[karte] ? KARTE[karte].b : ''), true);
  if (karte === 'rechner') { var inp = R.querySelector('.rz-rein'); inp.value = werte.ausdruck || ''; rechnerVorschau(R); ziel = R.querySelector('.rz-rechner'); }
  else {
    var def = KARTE[karte]; if (!def) return;
    ST.v = ST.v || {}; var alt = ST.v[karte] || {}, neu = {};
    def.f.forEach(function (fd) { if (werte && Object.prototype.hasOwnProperty.call(werte, fd.k)) neu[fd.k] = werte[fd.k] == null ? '' : (typeof werte[fd.k] === 'number' ? zeigeEing(werte[fd.k]) : werte[fd.k]); else if (alt[fd.k] !== undefined) neu[fd.k] = alt[fd.k]; });
    ST.v[karte] = neu; sichern();
    ziel = karteNeu(R, karte);
  }
  if (!ziel) return;
  ziel.scrollIntoView({ behavior: bewegungAus() ? 'auto' : 'smooth', block: 'start' });
  ziel.classList.remove('rz-blitz'); void ziel.offsetWidth; ziel.classList.add('rz-blitz');
  var hd = ziel.querySelector('h3'); if (hd) try { hd.focus({ preventScroll: true }); } catch (e) { hd.focus(); }
}

/* ---------- Rechner ---------- */
function rechnerVorschau(R) {
  var inp = R.querySelector('.rz-rein'), out = R.querySelector('.rz-rout'), s = inp.value.replace(/ans/g, '(' + String(ST.ans || 0) + ')');
  if (!inp.value.trim()) { out.textContent = ''; return null; }
  try { var r = ausdruck(s, { grad: ST.grad !== false }); out.textContent = '= ' + zahl(r.wert, 12); out.classList.remove('rz-err'); return r; }
  catch (e) { out.textContent = ''; return null; }
}
function rechnerVerlauf(R) {
  var L = ST.rverlauf || [], ol = R.querySelector('.rz-rverl');
  ol.innerHTML = L.length ? L.map(function (x, i) { return '<li><button type="button" data-rv="' + i + '"><span>' + esc(ausdruckHuebsch(x.a)) + '</span><b>= ' + esc(x.r) + '</b></button></li>'; }).join('') : '<li class="rz-leer">Noch keine Rechnungen.</li>';
}
function rechnerGleich(R) {
  var inp = R.querySelector('.rz-rein'), out = R.querySelector('.rz-rout'), aus = R.querySelector('.rz-raus'), a = inp.value.trim(); if (!a) return;
  try {
    var r = ausdruck(a.replace(/ans/g, '(' + String(ST.ans || 0) + ')'), { grad: ST.grad !== false }), t = zahl(r.wert, 12);
    ST.ans = r.wert; ST.rverlauf = [{ a: a, r: t }].concat(ST.rverlauf || []).slice(0, 20); sichern();
    aus.innerHTML = ergebnisHTML({ gross: t, label: ausdruckHuebsch(a), schritte: ['Regeln: Klammern → Potenzen → Punkt vor Strich → Strich.'].concat(r.schritte) });
    inp.value = t.indexOf('×') >= 0 ? String(r.wert).replace('.', ',') : t.replace(/\./g, '');
    out.textContent = ''; rechnerVerlauf(R);
  } catch (e) { out.textContent = e.message; out.classList.add('rz-err'); }
}
function rechnerTaste(R, t) {
  var inp = R.querySelector('.rz-rein');
  if (t === '=') return rechnerGleich(R);
  if (t === 'C') { inp.value = ''; R.querySelector('.rz-raus').innerHTML = ''; rechnerVorschau(R); return; }
  var a = inp.selectionStart != null ? inp.selectionStart : inp.value.length, b = inp.selectionEnd != null ? inp.selectionEnd : a;
  if (document.activeElement !== inp) { a = b = inp.value.length; }
  if (t === '⌫') { if (a === b && a > 0) a--; inp.value = inp.value.slice(0, a) + inp.value.slice(b); inp.setSelectionRange && inp.setSelectionRange(a, a); rechnerVorschau(R); return; }
  var ins = { '*': '×', '/': '÷', '-': '−' }[t] || t;
  inp.value = inp.value.slice(0, a) + ins + inp.value.slice(b);
  try { inp.setSelectionRange(a + ins.length, a + ins.length); } catch (e) { /* nichts */ }
  rechnerVorschau(R);
}

/* ---------- Währungskurse online ---------- */
function kurseHolen(R, erzwingen) {
  if (KURS_LAEUFT || typeof fetch !== 'function') return;
  if (!erzwingen && ST.kurse && ST.kurse.geholt && Date.now() - ST.kurse.geholt < 6 * 3600e3) return;
  if (typeof navigator !== 'undefined' && navigator.onLine === false) { if (erzwingen) kursStatus(R, 'Keine Internetverbindung – es bleiben die bisherigen Kurse.'); return; }
  KURS_LAEUFT = true;
  var ctrl = typeof AbortController === 'function' ? new AbortController() : null, to = setTimeout(function () { if (ctrl) ctrl.abort(); }, 8000);
  fetch('https://api.frankfurter.app/latest?from=EUR', ctrl ? { signal: ctrl.signal } : {}).then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); }).then(function (j) {
    if (!j || !j.rates || !j.rates.USD) throw new Error('unerwartete Antwort');
    ST.kurse = { datum: j.date, rates: j.rates, geholt: Date.now() }; sichern(true);
    if (R.isConnected) { kurseAuffrischen(R); }
  }).catch(function () { if (erzwingen && R.isConnected) kursStatus(R, 'Aktualisieren nicht möglich – es bleiben die bisherigen Kurse.'); })
    .then(function () { clearTimeout(to); KURS_LAEUFT = false; });
}
function kursStatus(R, t) { var L = R.querySelectorAll('.rz-kursinfo'); for (var i = 0; i < L.length; i++) L[i].textContent = t; }
function kurseAuffrischen(R) {
  var ctx = ctxNeu(), alt = R.querySelector('[data-kurse]');
  if (alt) { var tmp = document.createElement('div'); tmp.innerHTML = kurseKarteHTML(ctx); alt.parentNode.replaceChild(tmp.firstChild, alt); }
  var hz = R.querySelector('.rz-heute'); if (hz) { var t2 = document.createElement('div'); t2.innerHTML = heuteHTML(ctx); hz.parentNode.replaceChild(t2.firstChild, hz); }
  var w = R.querySelector('.rz-karte[data-k="waehrung"]'); if (w) karteRechnen(w, false);
}

/* ---------- Ereignisse ---------- */
function binden(R) {
  R.addEventListener('submit', function (ev) { var f = ev.target.closest('.rz-frage'); if (!f) return; ev.preventDefault(); var q = f.querySelector('input').value.trim(); if (q) antwortZeigen(R, q); });
  R.addEventListener('input', function (ev) {
    var t = ev.target;
    if (t.classList.contains('rz-rein')) return rechnerVorschau(R);
    if (t.hasAttribute('data-eigen')) { ST.eigene = ST.eigene || {}; var n = zahlLesen(t.value); if (n > 0) ST.eigene[t.getAttribute('data-eigen')] = n; else delete ST.eigene[t.getAttribute('data-eigen')]; sichern(); var w = R.querySelector('.rz-karte[data-k="waehrung"]'); if (w) karteRechnen(w, false); var ki = R.querySelector('[data-kurse] .rz-kursinfo'); if (ki) ki.textContent = ctxNeu().kursInfo; return; }
    var card = t.closest('.rz-karte[data-k]'); if (!card || !t.hasAttribute('data-k')) return;
    wertSetzen(card.getAttribute('data-k'), t.getAttribute('data-k'), t.value);
    if (t.tagName !== 'SELECT') karteRechnen(card, false);
  });
  R.addEventListener('change', function (ev) {
    var t = ev.target, card = t.closest('.rz-karte[data-k]'); if (!card || t.tagName !== 'SELECT') return;
    var id = card.getAttribute('data-k'), k = t.getAttribute('data-k'), def = KARTE[id], fd = def && def.f.filter(function (x) { return x.k === k; })[0];
    wertSetzen(id, k, t.value);
    if (fd && fd.land) { ST.land = t.value; sichern(); }
    var dyn = def.f.some(function (x) { return x.dyn === k || (x.nur && x.nur[k]); });
    if (dyn) karteNeu(R, id, 'select[data-k="' + k + '"]'); else karteRechnen(card, true);
  });
  R.addEventListener('keydown', function (ev) {
    var t = ev.target;
    if (t.classList && t.classList.contains('rz-rein') && ev.key === 'Enter') { ev.preventDefault(); rechnerGleich(R); return; }
    if (t.getAttribute && t.getAttribute('role') === 'radio' && /^(ArrowLeft|ArrowRight|ArrowUp|ArrowDown)$/.test(ev.key)) {
      var L = Array.prototype.slice.call(t.parentNode.querySelectorAll('[role="radio"]')), i = L.indexOf(t) + (/Right|Down/.test(ev.key) ? 1 : -1);
      i = (i + L.length) % L.length; ev.preventDefault(); L[i].focus(); L[i].click(); return;
    }
    if (t.classList && t.classList.contains('rz-ksvg') && /^(ArrowLeft|ArrowRight|Home|End|Escape)$/.test(ev.key)) {
      var el = t.closest('.rz-kurs'), g = el._g, cur = el._i == null ? g.bis : el._i; ev.preventDefault();
      if (ev.key === 'Escape') return kursMarke(el, null);
      cur = ev.key === 'Home' ? g.von : ev.key === 'End' ? g.bis : Math.max(g.von, Math.min(g.bis, cur + (ev.key === 'ArrowRight' ? 1 : -1)));
      kursMarke(el, cur);
    }
  });
  R.addEventListener('pointermove', kursZeiger);
  R.addEventListener('pointerdown', kursZeiger);
  R.addEventListener('pointerout', function (ev) { var svg = ev.target.closest && ev.target.closest('.rz-ksvg'); if (svg && ev.pointerType === 'mouse' && !svg.contains(ev.relatedTarget)) kursMarke(svg.closest('.rz-kurs'), null); });
  R.addEventListener('click', function (ev) {
    var t = ev.target.closest('button'); if (!t || !R.contains(t)) return;
    var q = t.getAttribute('data-q');
    if (q != null) { var fi = R.querySelector('#rz-fq'); fi.value = q; antwortZeigen(R, q); var a = R.querySelector('.rz-ant'); if (a && t.closest('.rz-bsp,.rz-verlauf,.rz-ant')) { try { a.focus({ preventScroll: true }); } catch (e) { /* alt */ } a.scrollIntoView({ block: 'nearest', behavior: bewegungAus() ? 'auto' : 'smooth' }); } return; }
    if (t.hasAttribute('data-ziel')) { zeige(R, t.getAttribute('data-ziel')); return; }
    if (t.hasAttribute('data-karte')) { zurKarte(R, t.getAttribute('data-karte')); return; }
    if (t.hasAttribute('data-oeffnen')) { var art = t.closest('.rz-ant'); if (art && art._e) oeffnen(R, art._e.karte, art._e.werte); return; }
    if (t.hasAttribute('data-kopie')) { var e = t.closest('.rz-ant')._e, txt = e.gross + (e.einh ? ' ' + e.einh : ''); try { navigator.clipboard.writeText(txt).then(function () { t.textContent = 'Kopiert ✓'; }, function () { t.textContent = txt; }); } catch (er) { t.textContent = txt; } return; }
    if (t.classList.contains('rz-stern')) { var an = t.closest('.rz-ant'), qq = an._q; ST.fav = ST.fav || []; var i = ST.fav.indexOf(qq); if (i >= 0) ST.fav.splice(i, 1); else ST.fav.unshift(qq); ST.fav = ST.fav.slice(0, 30); sichern(); t.setAttribute('aria-pressed', i < 0); t.textContent = i < 0 ? '★' : '☆'; R.querySelector('.rz-verlauf').innerHTML = verlaufHTML(); return; }
    if (t.hasAttribute('data-verl-leer')) { ST.verlauf = []; sichern(); R.querySelector('.rz-verlauf').innerHTML = verlaufHTML(); return; }
    if (t.getAttribute('role') === 'radio' && t.hasAttribute('data-v')) { var card = t.closest('.rz-karte[data-k]'), id = card.getAttribute('data-k'), k = t.getAttribute('data-k'); wertSetzen(id, k, t.getAttribute('data-v')); if (id === 'einheit' && k === 'kat') { ST.v.einheit.von = STD_PAAR[t.getAttribute('data-v')][0]; ST.v.einheit.nach = STD_PAAR[t.getAttribute('data-v')][1]; } karteNeu(R, id, '[role="radio"][data-v="' + t.getAttribute('data-v') + '"]'); return; }
    if (t.classList.contains('rz-tausch')) { var c2 = t.closest('.rz-karte[data-k]'), id2 = c2.getAttribute('data-k'), A = t.getAttribute('data-a'), B = t.getAttribute('data-b'), sa = c2.querySelector('select[data-k="' + A + '"]').value, sb = c2.querySelector('select[data-k="' + B + '"]').value; wertSetzen(id2, A, sb); wertSetzen(id2, B, sa); karteNeu(R, id2, '.rz-tausch'); return; }
    if (t.hasAttribute('data-formel')) { var c3 = t.closest('.rz-karte[data-k]'); wertSetzen(c3.getAttribute('data-k'), 'formel', t.getAttribute('data-formel')); var inp3 = c3.querySelector('input[data-k="formel"]'); inp3.value = t.getAttribute('data-formel'); karteRechnen(c3, true); return; }
    if (t.hasAttribute('data-z')) { var el = ELEMENTE[+t.getAttribute('data-z') - 1], box = R.querySelector('.rz-elinfo'); box.innerHTML = elementHTML(el); var pr = R.querySelector('.rz-el[aria-pressed="true"]'); if (pr) pr.setAttribute('aria-pressed', 'false'); t.setAttribute('aria-pressed', 'true'); return; }
    if (t.hasAttribute('data-elformel')) { var mk = R.querySelector('.rz-karte[data-k="molmasse"]'), fi2 = mk.querySelector('input[data-k="formel"]'), nf3 = (ST.v && ST.v.molmasse && ST.v.molmasse.formel != null && fi2.value !== 'H2SO4' ? fi2.value : '') + t.getAttribute('data-elformel'); fi2.value = nf3; wertSetzen('molmasse', 'formel', nf3); karteRechnen(mk, true); mk.scrollIntoView({ behavior: bewegungAus() ? 'auto' : 'smooth', block: 'center' }); return; }
    if (t.hasAttribute('data-t')) { rechnerTaste(R, t.getAttribute('data-t')); return; }
    if (t.hasAttribute('data-grad')) { ST.grad = t.getAttribute('data-grad') === '1'; sichern(); var gL = R.querySelectorAll('[data-grad]'); for (var gi = 0; gi < gL.length; gi++) gL[gi].setAttribute('aria-checked', gL[gi] === t); rechnerVorschau(R); return; }
    if (t.hasAttribute('data-wiss')) { ST.wiss = !ST.wiss; sichern(); t.setAttribute('aria-expanded', ST.wiss); R.querySelector('.rz-wiss').hidden = !ST.wiss; return; }
    if (t.hasAttribute('data-tast')) { var ri = R.querySelector('.rz-rein'); ri.setAttribute('inputmode', ri.getAttribute('inputmode') === 'none' ? 'text' : 'none'); ri.blur(); ri.focus(); return; }
    if (t.hasAttribute('data-rv')) { var x = (ST.rverlauf || [])[+t.getAttribute('data-rv')]; if (x) { var ri2 = R.querySelector('.rz-rein'); ri2.value = x.a; rechnerVorschau(R); ri2.scrollIntoView({ block: 'center', behavior: bewegungAus() ? 'auto' : 'smooth' }); } return; }
    if (t.hasAttribute('data-rverl-leer')) { ST.rverlauf = []; sichern(); rechnerVerlauf(R); return; }
    if (t.hasAttribute('data-zr')) { var kel = t.closest('.rz-kurs'), z = +t.getAttribute('data-zr'); kel._von = z ? Math.max(0, kel._d.x.length - 1 - z) : 0; kursZeichnen(kel); var nb = kel.querySelector('[data-zr="' + z + '"]'); if (nb) nb.focus(); return; }
    if (t.hasAttribute('data-kurse-laden')) { kursStatus(R, 'Lade EZB-Kurse …'); kurseHolen(R, true); return; }
    if (t.hasAttribute('data-kurse-reset')) { ST.eigene = {}; sichern(); kurseAuffrischen(R); return; }
  });
}
function navAktiv(R, id) { var L = R.querySelectorAll('.rz-nav button'); for (var i = 0; i < L.length; i++) { var an = L[i].getAttribute('data-ziel') === (id || ''); if (an) L[i].setAttribute('aria-current', 'true'); else L[i].removeAttribute('aria-current'); } }

function seite(el) {
  if (!el) return;
  if (TIMER) { clearInterval(TIMER); TIMER = null; }
  if (IO) { IO.disconnect(); IO = null; }
  if (RO) { RO.disconnect(); RO = null; }
  ST = laden(); if (!ST.v || typeof ST.v !== 'object') ST.v = {};
  var ctx = ctxNeu();
  el.innerHTML = '<div class="rz-seite">' + aufbau(ctx) + '</div>';
  var R = el.querySelector('.rz-seite');
  binden(R);
  zeige(R, '', true);
  var lst = R.querySelector('.rz-leiste'); if (lst) R.style.setProperty('--rz-lh', lst.offsetHeight + 'px');
  var breite = R.clientWidth;
  if (typeof ResizeObserver === 'function') {
    RO = new ResizeObserver(function () { if (Math.abs(R.clientWidth - breite) < 8) return; breite = R.clientWidth; if (lst) R.style.setProperty('--rz-lh', lst.offsetHeight + 'px'); var K2 = R.querySelectorAll('.rz-bereich:not([hidden]) .rz-kurs, .rz-antwort .rz-kurs'); for (var k = 0; k < K2.length; k++) kursZeichnen(K2[k]); });
    RO.observe(R);
  }
  TIMER = setInterval(function () {
    if (!R.isConnected) { clearInterval(TIMER); TIMER = null; return; }
    if (typeof document !== 'undefined' && document.hidden) return;
    var LV = R.querySelectorAll('.rz-karte[data-k]');
    for (var m = 0; m < LV.length; m++) { var d = KARTE[LV[m].getAttribute('data-k')]; if (d && d.live && !LV[m].closest('[hidden]') && !LV[m].contains(document.activeElement)) karteRechnen(LV[m], false); }
  }, 1000);
  kurseHolen(R, false);
  return R;
}

root.QWRechner = { seite: seite, _kern: KERN };
if (typeof module !== 'undefined' && module.exports) module.exports = root.QWRechner;


})(typeof window !== 'undefined' ? window : globalThis);
