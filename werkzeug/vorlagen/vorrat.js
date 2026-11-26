/* Quellwissen – „Vorrat & Blackout-Planer“ (eigenständiges Modul, ES2019, offline, ohne Bibliotheken) · Quelle: werkzeug/vorlagen/vorrat.js
   Schnittstelle: window.QWVorrat.seite(el, {figur})  ·  reine Rechenlogik zusätzlich unter QWVorrat._kern
   Speicher: localStorage „qw_vorrat_v1“ (nur auf diesem Gerät). Einbau: python3 werkzeug/vorlagen/vorrat_einbauen.py */
(function (root) {
'use strict';

/* ===================================================================== 1. Helfer */
var SPEICHER = 'qw_vorrat_v1';
function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
var NFC = {};
function nf(d) { return NFC[d] || (NFC[d] = new Intl.NumberFormat('de-DE', { maximumFractionDigits: d, minimumFractionDigits: 0 })); }
function fz(x, d) { if (x == null || !isFinite(x)) return '–'; return nf(d || 0).format(d ? x : Math.round(x)).replace('-', '−'); }
function kg(g) { return g >= 1000 ? fz(g / 1000, g >= 10000 ? 0 : 1) + ' kg' : fz(g) + ' g'; }
function liter(l) { return fz(l, l < 10 ? 1 : 0) + ' l'; }
function zahl(s) { if (typeof s === 'number') return s; s = String(s == null ? '' : s).trim().replace(/\s/g, '').replace(',', '.'); if (!s) return NaN; var x = parseFloat(s); return isFinite(x) ? x : NaN; }
function tageText(t) { if (!isFinite(t)) return 'unbegrenzt'; if (t >= 730) return 'über 2 Jahre'; if (t < 1) return t <= 0 ? '0 Tage' : 'unter 1 Tag'; var r = Math.floor(t + 1e-9); return r + (r === 1 ? ' Tag' : ' Tage'); }
function tageZahl(t) { if (!isFinite(t)) return '∞'; if (t >= 730) return '730+'; if (t < 1 && t > 0) return '<1'; return String(Math.floor(t + 1e-9)); }
function uid() { return Math.random().toString(36).slice(2, 9); }
function klon(x) { return JSON.parse(JSON.stringify(x)); }
var MONATE = ['Jan.', 'Feb.', 'März', 'Apr.', 'Mai', 'Juni', 'Juli', 'Aug.', 'Sep.', 'Okt.', 'Nov.', 'Dez.'];
/* MHD „JJJJ-MM“ → letzter Tag des Monats */
function mhdDatum(s) { var m = /^(\d{4})-(\d{2})$/.exec(s || ''); if (!m) return null; return new Date(+m[1], +m[2], 0, 12); }
function mhdText(s) { var m = /^(\d{4})-(\d{2})$/.exec(s || ''); return m ? MONATE[+m[2] - 1] + ' ' + m[1] : ''; }
function tageBis(d, heute) { return Math.floor((d.getTime() - heute.getTime()) / 86400000); }

/* ===================================================================== 2. Tabellen */
/* Lebensmittelgruppen nach der Vorratstabelle der BLE (ernaehrungsvorsorge.de, Mischkost, © BLE 2024):
   Menge je Person für 10 Tage bei durchschnittlich 2.200 kcal am Tag. g = Gramm (Getränke: Milliliter) */
var GRUPPEN = [
  { k: 'getreide', n: 'Getreide, Brot, Kartoffeln, Nudeln, Reis', kurz: 'Getreide & Brot', i: '🌾', ble: 3300 },
  { k: 'gemuese', n: 'Gemüse, Hülsenfrüchte, Pilze', kurz: 'Gemüse & Hülsenfrüchte', i: '🥕', ble: 4000 },
  { k: 'obst', n: 'Obst und Nüsse', kurz: 'Obst & Nüsse', i: '🍎', ble: 2500 },
  { k: 'milch', n: 'Milch und Milchprodukte', kurz: 'Milch', i: '🥛', ble: 2500 },
  { k: 'eiweiss', n: 'Fisch, Fleisch, Eier', kurz: 'Fisch, Fleisch, Eier', i: '🥚', ble: 1200 },
  { k: 'fett', n: 'Fette und Öle', kurz: 'Fette & Öle', i: '🫒', ble: 330 },
  { k: 'trinken', n: 'Getränke', kurz: 'Getränke', i: '💧', ble: 0 },
  { k: 'sonst', n: 'Sonstiges (Zucker, Honig, Salz, Brühe, Backzutaten, Süßes)', kurz: 'Sonstiges', i: '🧂', ble: 0 },
  { k: 'baby', n: 'Babynahrung', kurz: 'Baby', i: '🍼', ble: 0 }
];
var GR = {}; GRUPPEN.forEach(function (g) { GR[g.k] = g; });
var BLE_KCAL = 2200, BLE_TAGE = 10;

/* Katalog: je 100 g (Getränke/Milch: je 100 ml) – k kcal, e Eiweiß, f Fett, c Kohlenhydrate (bei USDA „by difference“, inkl. Ballaststoffe).
   q Quelle: A = Nährwert-Liste der App (S-23), U<Nr> = USDA FoodData Central SR Legacy (fdc_id), — = ohne Energie.
   ko = braucht Kochen · w = Kochwasser ml je 100 g · z = Kochzeit min · h/ht = übliche Haltbarkeit ungeöffnet (Tage, Richtwert; Text)
   p = übliche Packungen [Name, g] (Richtwert – das Etikett gilt) · st = g je Stück · l = Lagerort-Vorgabe (k Kühlschrank, t Gefriertruhe)
   ml = Menge in ml · fl = zählt als Trinkwasser · x = Umrechnung auf die Menge der BLE-Tabelle (z. B. trockene Linsen → gekochte: Energie-Verhältnis)
   b = Ballaststoffe g, vc = Vitamin C mg je 100 g (USDA SR Legacy; bei App-Einträgen b aus der App-Liste, vc vom ähnlichsten USDA-Eintrag vq) */
var KATALOG = [
{"i":"haferflocken","n":"Haferflocken","g":"getreide","k":370,"e":13.5,"f":7,"c":58.7,"q":"A","b":10,"vc":0.0,"vq":"U169705","h":365,"ht":"etwa 1 Jahr","p":[["Packung 500 g",500]],"s":"hafer müsli porridge"},
{"i":"nudeln","n":"Nudeln (Hartweizen), trocken","g":"getreide","k":355,"e":12.5,"f":1.5,"c":71,"q":"A","b":3,"vc":0.0,"vq":"U169736","ko":1,"w":1000,"z":10,"h":365,"ht":"etwa 1 Jahr","p":[["Packung 500 g",500]],"s":"spaghetti makkaroni penne pasta teigwaren"},
{"i":"nudeln_vk","n":"Vollkornnudeln, trocken","g":"getreide","k":352,"e":13.9,"f":2.9,"c":73.4,"q":"U169738","b":9.2,"ko":1,"w":1000,"z":12,"h":365,"ht":"etwa 1 Jahr","p":[["Packung 500 g",500]],"s":"pasta"},
{"i":"eiernudeln","n":"Eiernudeln / Spätzle, trocken","g":"getreide","k":384,"e":14.2,"f":4.4,"c":71.3,"q":"U169731","b":3.3,"vc":0.0,"ko":1,"w":1000,"z":10,"h":365,"ht":"etwa 1 Jahr","p":[["Packung 500 g",500]],"s":"spätzle bandnudeln"},
{"i":"reis","n":"Reis, weiß, trocken","g":"getreide","k":350,"e":7,"f":0.6,"c":78,"q":"A","b":1.4,"vc":0.0,"vq":"U168877","ko":1,"w":200,"z":20,"h":365,"ht":"etwa 1 Jahr","p":[["Packung 1 kg",1000],["Kochbeutel 125 g",125]],"s":"langkorn basmati"},
{"i":"reis_vk","n":"Vollkornreis, trocken","g":"getreide","k":350,"e":7.5,"f":2.7,"c":72,"q":"A","b":3.5,"vc":0.0,"vq":"U169703","ko":1,"w":250,"z":35,"h":365,"ht":"etwa 1 Jahr","p":[["Packung 1 kg",1000]]},
{"i":"couscous","n":"Couscous, trocken","g":"getreide","k":355,"e":12.8,"f":0.6,"c":72,"q":"A","b":5,"vc":0.0,"vq":"U169699","ko":1,"w":120,"z":5,"h":365,"ht":"etwa 1 Jahr","p":[["Packung 500 g",500]]},
{"i":"bulgur","n":"Bulgur, trocken","g":"getreide","k":342,"e":12.3,"f":1.3,"c":75.9,"q":"U170688","b":12.5,"vc":0.0,"ko":1,"w":200,"z":15,"h":365,"ht":"etwa 1 Jahr","p":[["Packung 500 g",500]]},
{"i":"hirse","n":"Hirse, trocken","g":"getreide","k":378,"e":11.0,"f":4.2,"c":72.8,"q":"U169702","b":8.5,"vc":0.0,"ko":1,"w":250,"z":20,"h":365,"ht":"etwa 1 Jahr","p":[["Packung 500 g",500]]},
{"i":"quinoa","n":"Quinoa, trocken","g":"getreide","k":355,"e":14,"f":6,"c":57,"q":"A","b":7,"vq":"U168874","ko":1,"w":200,"z":15,"h":365,"ht":"etwa 1 Jahr","p":[["Packung 500 g",500]]},
{"i":"griess","n":"Weichweizengrieß","g":"getreide","k":360,"e":12.7,"f":1.1,"c":72.8,"q":"U169715","b":3.9,"vc":0.0,"ko":1,"z":5,"h":365,"ht":"etwa 1 Jahr","p":[["Packung 500 g",500]],"s":"grieß griessbrei"},
{"i":"polenta","n":"Polenta / Maisgrieß","g":"getreide","k":370,"e":7.1,"f":1.8,"c":79.5,"q":"U168929","b":3.9,"vc":0.0,"ko":1,"w":400,"z":10,"h":365,"ht":"etwa 1 Jahr","p":[["Packung 500 g",500]],"s":"maisgriess"},
{"i":"weizenkoerner","n":"Weizenkörner (ganz)","g":"getreide","k":327,"e":12.6,"f":1.5,"c":71.2,"q":"U168890","b":12.2,"vc":0.0,"ko":1,"w":300,"z":60,"h":730,"ht":"2 Jahre","p":[["Sack 1 kg",1000],["Sack 5 kg",5000]],"s":"getreide korn dinkel"},
{"i":"mehl405","n":"Weizenmehl Type 405/550","g":"getreide","k":345,"e":10,"f":1,"c":71,"q":"A","b":4,"vc":0.0,"vq":"U168894","ko":1,"ht":"MHD auf der Packung","p":[["Packung 1 kg",1000]],"s":"mehl"},
{"i":"vollkornmehl","n":"Weizenvollkornmehl","g":"getreide","k":330,"e":12,"f":2,"c":60,"q":"A","b":10,"vc":0.0,"vq":"U168893","ko":1,"ht":"MHD auf der Packung","p":[["Packung 1 kg",1000]],"s":"mehl vollkorn"},
{"i":"dinkelmehl","n":"Dinkelmehl","g":"getreide","k":338,"e":14.6,"f":2.4,"c":70.2,"q":"U169745","b":10.7,"vc":0.0,"ko":1,"ht":"MHD auf der Packung","p":[["Packung 1 kg",1000]],"s":"mehl dinkel 630 vollkorn"},
{"i":"roggenmehl","n":"Roggenmehl (Type 997/1150)","g":"getreide","k":349,"e":10.9,"f":1.5,"c":75.4,"q":"U168886","b":11.8,"vc":0.0,"ko":1,"ht":"MHD auf der Packung","p":[["Packung 1 kg",1000]],"s":"mehl roggen"},
{"i":"roggenvollkornmehl","n":"Roggenvollkornmehl","g":"getreide","k":325,"e":15.9,"f":2.2,"c":68.6,"q":"U168885","b":23.8,"vc":0.0,"ko":1,"ht":"MHD auf der Packung","p":[["Packung 1 kg",1000]],"s":"mehl roggen vollkorn"},
{"i":"staerke","n":"Speisestärke","g":"getreide","k":381,"e":0.3,"f":0.1,"c":91.3,"q":"U169698","b":0.9,"vc":0.0,"ko":1,"h":365,"ht":"etwa 1 Jahr","p":[["Packung 400 g",400]],"s":"maisstärke stärke"},
{"i":"kartoffeln","n":"Kartoffeln, roh","g":"getreide","k":77,"e":2.0,"f":0.1,"c":17.5,"q":"U170026","b":2.1,"vc":19.7,"ko":1,"w":100,"z":20,"h":180,"ht":"6–8 Monate (dunkel, 5–10 °C)","p":[["Netz 2,5 kg",2500],["Sack 10 kg",10000]],"st":150},
{"i":"pueree","n":"Kartoffelpüree-Flocken","g":"getreide","k":354,"e":8.3,"f":0.4,"c":81.2,"q":"U170445","b":6.6,"vc":81.0,"ko":1,"w":450,"z":2,"h":365,"ht":"1–2 Jahre","p":[["Packung 3 × 3 Port. (ca. 240 g)",240]],"s":"kartoffelbrei püree"},
{"i":"knaecke","n":"Knäckebrot","g":"getreide","k":366,"e":7.9,"f":1.3,"c":82.2,"q":"U172739","b":16.5,"vc":0.0,"h":365,"ht":"etwa 1 Jahr","p":[["Packung 250 g",250]],"s":"knäcke"},
{"i":"zwieback","n":"Zwieback","g":"getreide","k":426,"e":10.1,"f":9.7,"c":74.2,"q":"U171372","b":2.5,"vc":5.3,"h":365,"ht":"etwa 1 Jahr","p":[["Packung 225 g",225]]},
{"i":"vkbrot","n":"Vollkornbrot (Schnittbrot, verpackt)","g":"getreide","k":200,"e":6.5,"f":1.2,"c":38,"q":"A","b":8,"vc":0.0,"vq":"U174918","ht":"MHD auf der Packung","p":[["Packung 500 g",500]],"s":"pumpernickel schwarzbrot"},
{"i":"mischbrot","n":"Brot, frisch (Mischbrot)","g":"getreide","k":220,"e":6.5,"f":1.2,"c":43,"q":"A","b":6,"vc":0.4,"vq":"U172684","h":10,"ht":"10–12 Tage","p":[["Laib 1 kg",1000],["Laib 750 g",750]],"s":"brot laib"},
{"i":"toast","n":"Toastbrot","g":"getreide","k":260,"e":8,"f":3.5,"c":47,"q":"A","b":3,"vc":0.0,"vq":"U174924","ht":"MHD auf der Packung","p":[["Packung 500 g",500]]},
{"i":"broetchen","n":"Brötchen","g":"getreide","k":260,"e":8.5,"f":1.5,"c":51,"q":"A","b":3,"vc":0.0,"vq":"U175031","h":1,"ht":"1–2 Tage","st":55,"s":"semmel schrippe"},
{"i":"tortilla","n":"Weizen-Tortillas (Fladen)","g":"getreide","k":297,"e":8.0,"f":7.6,"c":49.3,"q":"U167535","b":2.4,"vc":0.0,"ht":"MHD auf der Packung","p":[["Packung 8 St. (ca. 320 g)",320]],"st":40,"s":"wraps fladen"},
{"i":"reiswaffeln","n":"Reiswaffeln","g":"getreide","k":392,"e":7.1,"f":4.3,"c":81.1,"q":"U168107","b":4.2,"vc":0.0,"ht":"MHD auf der Packung","p":[["Packung 100 g",100]]},
{"i":"cornflakes","n":"Cornflakes","g":"getreide","k":378,"e":7,"f":0.9,"c":84,"q":"A","b":3,"vc":65.0,"vq":"U174648","h":365,"ht":"etwa 1 Jahr","p":[["Packung 375 g",375]],"s":"maisflocken"},
{"i":"muesli","n":"Müsli (mit Nüssen, gesüßt)","g":"getreide","k":489,"e":13.7,"f":24.3,"c":53.9,"q":"U171646","b":8.9,"vc":1.2,"ht":"MHD auf der Packung","p":[["Packung 750 g",750]],"s":"granola knuspermüsli"},
{"i":"ravioli","n":"Ravioli in Tomatensoße (Dose)","g":"getreide","k":77,"e":2.5,"f":1.4,"c":13.6,"q":"U173328","b":1.3,"vc":0.0,"z":5,"h":365,"ht":"1–2 Jahre","p":[["Dose 800 g",800],["Dose 400 g",400]],"s":"fertiggericht konserve"},
{"i":"linsen","n":"Linsen (braun/Teller), trocken","g":"gemuese","k":352,"e":24.6,"f":1.1,"c":63.4,"q":"U172420","b":10.7,"vc":4.5,"ko":1,"w":300,"z":30,"h":365,"ht":"etwa 1 Jahr","p":[["Packung 500 g",500]],"x":3.03,"s":"hülsenfrüchte"},
{"i":"rote_linsen","n":"Rote Linsen, trocken","g":"gemuese","k":358,"e":23.9,"f":2.2,"c":63.1,"q":"U174284","b":10.8,"vc":1.7,"ko":1,"w":250,"z":12,"h":365,"ht":"etwa 1 Jahr","p":[["Packung 500 g",500]],"x":3.09,"s":"hülsenfrüchte dal"},
{"i":"erbsen_getr","n":"Schälerbsen (getrocknet)","g":"gemuese","k":364,"e":23.1,"f":3.9,"c":61.6,"q":"U172428","b":22.2,"vc":1.8,"ko":1,"w":300,"z":45,"h":365,"ht":"etwa 1 Jahr","p":[["Packung 500 g",500]],"x":3.08,"s":"erbsen hülsenfrüchte erbsensuppe"},
{"i":"bohnen_getr","n":"Weiße Bohnen, getrocknet","g":"gemuese","k":333,"e":23.4,"f":0.8,"c":60.3,"q":"U175202","b":15.2,"vc":0.0,"ko":1,"w":300,"z":90,"h":365,"ht":"etwa 1 Jahr","p":[["Packung 500 g",500]],"x":2.4,"s":"hülsenfrüchte einweichen"},
{"i":"kidney_getr","n":"Kidneybohnen, getrocknet","g":"gemuese","k":337,"e":22.5,"f":1.1,"c":61.3,"q":"U173744","b":15.2,"vc":4.5,"ko":1,"w":300,"z":90,"h":365,"ht":"etwa 1 Jahr","p":[["Packung 500 g",500]],"x":2.72,"s":"hülsenfrüchte rote bohnen"},
{"i":"kicher_getr","n":"Kichererbsen, getrocknet","g":"gemuese","k":378,"e":20.5,"f":6.0,"c":63.0,"q":"U173756","b":12.2,"vc":4.0,"ko":1,"w":300,"z":90,"h":365,"ht":"etwa 1 Jahr","p":[["Packung 500 g",500]],"x":2.3,"s":"hülsenfrüchte"},
{"i":"kidney_dose","n":"Kidneybohnen (Dose, abgetropft)","g":"gemuese","k":124,"e":8.0,"f":1.1,"c":21.5,"q":"U174285","b":5.5,"vc":0.2,"h":365,"ht":"1–2 Jahre","p":[["Dose 400 g (250 g abgetropft)",250],["Dose 800 g (500 g abgetropft)",500]],"s":"rote bohnen konserve"},
{"i":"kicher_dose","n":"Kichererbsen (Dose, abgetropft)","g":"gemuese","k":139,"e":7.0,"f":2.8,"c":22.5,"q":"U173800","b":6.4,"vc":0.1,"h":365,"ht":"1–2 Jahre","p":[["Dose 400 g (240 g abgetropft)",240]],"s":"konserve hummus"},
{"i":"bohnen_dose","n":"Weiße Bohnen (Dose)","g":"gemuese","k":114,"e":7.3,"f":0.3,"c":21.2,"q":"U175204","b":4.8,"vc":0.0,"h":365,"ht":"1–2 Jahre","p":[["Dose 400 g (250 g abgetropft)",250]],"s":"konserve"},
{"i":"baked_beans","n":"Bohnen in Tomatensoße (Dose)","g":"gemuese","k":94,"e":4.8,"f":0.4,"c":21.1,"q":"U175182","b":4.1,"vc":0.0,"h":365,"ht":"1–2 Jahre","p":[["Dose 415 g",415]],"s":"baked beans konserve"},
{"i":"gr_bohnen","n":"Grüne Bohnen (Dose, abgetropft)","g":"gemuese","k":21,"e":1.1,"f":0.4,"c":4.2,"q":"U169143","b":1.9,"vc":2.8,"h":365,"ht":"1–2 Jahre","p":[["Dose 425 ml (220 g abgetropft)",220],["Dose 850 ml (440 g abgetropft)",440]],"s":"brechbohnen konserve"},
{"i":"erbsen_moehren","n":"Erbsen & Möhren (Dose)","g":"gemuese","k":38,"e":2.2,"f":0.3,"c":8.5,"q":"U170424","b":2.0,"vc":6.6,"h":365,"ht":"1–2 Jahre","p":[["Dose 425 ml (280 g abgetropft)",280],["Dose 850 ml (530 g abgetropft)",530]],"s":"karotten konserve"},
{"i":"mais","n":"Mais (Dose, abgetropft)","g":"gemuese","k":67,"e":2.3,"f":1.2,"c":14.3,"q":"U169214","b":2.0,"vc":1.8,"h":365,"ht":"1–2 Jahre","p":[["Dose 425 ml (285 g abgetropft)",285],["Dose 212 ml (140 g abgetropft)",140]],"s":"zuckermais konserve"},
{"i":"rotkohl_glas","n":"Rotkohl (Glas)","g":"gemuese","k":29,"e":1.5,"f":0.1,"c":6.9,"q":"U169978","b":2.6,"vc":34.4,"z":10,"h":365,"ht":"1–2 Jahre","p":[["Glas 720 ml (680 g)",680]],"s":"blaukraut konserve"},
{"i":"sauerkraut","n":"Sauerkraut (Dose/Glas)","g":"gemuese","k":19,"e":0.9,"f":0.1,"c":4.3,"q":"U169279","b":2.9,"vc":14.7,"h":365,"ht":"1–2 Jahre","p":[["Dose 850 ml (770 g)",770],["Glas 720 ml (680 g)",680]],"s":"konserve"},
{"i":"pilze_dose","n":"Champignons (Dose, abgetropft)","g":"gemuese","k":25,"e":1.9,"f":0.3,"c":5.1,"q":"U169254","b":2.4,"vc":0.0,"h":365,"ht":"1–2 Jahre","p":[["Dose 314 ml (170 g abgetropft)",170]],"s":"pilze konserve"},
{"i":"gurken","n":"Gewürzgurken (Glas, abgetropft)","g":"gemuese","k":12,"e":0.5,"f":0.3,"c":2.4,"q":"U168558","b":1.0,"vc":2.3,"h":365,"ht":"1–2 Jahre","p":[["Glas 720 ml (360 g abgetropft)",360]],"s":"essiggurken konserve"},
{"i":"rote_bete","n":"Rote Bete (Glas, abgetropft)","g":"gemuese","k":31,"e":0.9,"f":0.1,"c":7.2,"q":"U169966","b":1.8,"vc":4.1,"h":365,"ht":"1–2 Jahre","p":[["Glas 720 ml (350 g abgetropft)",350]],"s":"rote beete konserve"},
{"i":"tomaten_dose","n":"Tomaten, gehackt (Dose)","g":"gemuese","k":16,"e":0.8,"f":0.2,"c":3.5,"q":"U170051","b":1.9,"vc":12.6,"h":365,"ht":"1–2 Jahre","p":[["Dose 400 g",400],["Packung 500 g",500]],"s":"konserve tomate"},
{"i":"passata","n":"Passierte Tomaten","g":"gemuese","k":38,"e":1.6,"f":0.2,"c":9.0,"q":"U170546","b":1.9,"vc":10.6,"h":365,"ht":"1–2 Jahre","p":[["Packung 500 g",500],["Flasche 700 g",700]],"s":"tomatensoße konserve"},
{"i":"tomatenmark","n":"Tomatenmark","g":"gemuese","k":82,"e":4.3,"f":0.5,"c":18.9,"q":"U170459","b":4.1,"vc":21.9,"h":365,"ht":"1–2 Jahre","p":[["Tube 200 g",200],["Dose 70 g",70]]},
{"i":"spargel","n":"Spargel (Glas, abgetropft)","g":"gemuese","k":19,"e":2.1,"f":0.7,"c":2.5,"q":"U169207","b":1.6,"vc":18.4,"h":365,"ht":"1–2 Jahre","p":[["Glas 370 ml (205 g abgetropft)",205]],"s":"konserve"},
{"i":"eintopf","n":"Erbseneintopf (Dose)","g":"gemuese","k":77,"e":4.6,"f":1.7,"c":11.2,"q":"U171555","b":1.7,"vc":2.9,"z":5,"h":365,"ht":"1–2 Jahre","p":[["Dose 800 g",800],["Dose 400 g",400]],"s":"suppe eintopf fertiggericht konserve"},
{"i":"pilze_getr","n":"Pilze, getrocknet","g":"gemuese","k":296,"e":9.6,"f":1.0,"c":75.4,"q":"U168436","b":11.5,"vc":3.5,"ko":1,"w":200,"z":20,"h":365,"ht":"etwa 1 Jahr","p":[["Beutel 30 g",30]],"s":"steinpilze shiitake"},
{"i":"zwiebeln","n":"Zwiebeln","g":"gemuese","k":38,"e":1.1,"f":0.1,"c":7.6,"q":"A","b":1.7,"vc":7.4,"vq":"U170000","ht":"MHD auf der Packung","p":[["Netz 1 kg",1000]],"st":100,"s":"zwiebel"},
{"i":"knoblauch","n":"Knoblauch","g":"gemuese","k":149,"e":6.4,"f":0.5,"c":33.1,"q":"U169230","b":2.1,"vc":31.2,"ht":"MHD auf der Packung","st":5,"s":"knolle zehe"},
{"i":"moehren","n":"Möhren, frisch","g":"gemuese","k":38,"e":0.9,"f":0.2,"c":6.8,"q":"A","b":2.8,"vc":5.9,"vq":"U170393","h":8,"ht":"etwa 8 Tage (Kühlschrank)","p":[["Beutel 1 kg",1000]],"l":"k","st":80,"s":"karotten möhre"},
{"i":"kohl","n":"Weißkohl / Rotkohl, frisch","g":"gemuese","k":24,"e":1.3,"f":0.1,"c":3.3,"q":"A","b":2.5,"vc":36.6,"vq":"U169975","ht":"MHD auf der Packung","l":"k","st":1000,"s":"kraut kohlkopf"},
{"i":"erbsen_tk","n":"Erbsen (tiefgekühlt)","g":"gemuese","k":73,"e":5.4,"f":0.4,"c":9.4,"q":"A","b":5.1,"vc":18.0,"vq":"U170016","ko":1,"w":50,"z":5,"h":180,"ht":"6–12 Monate (−18 °C)","p":[["Beutel 750 g",750]],"l":"t","s":"tk tiefkühl"},
{"i":"spinat_tk","n":"Spinat (tiefgekühlt)","g":"gemuese","k":29,"e":3.6,"f":0.6,"c":4.2,"q":"U169287","b":2.9,"vc":5.5,"ko":1,"z":10,"h":180,"ht":"6–12 Monate (−18 °C)","p":[["Packung 450 g",450]],"l":"t","s":"tk tiefkühl"},
{"i":"gemuese_tk","n":"Gemüsemischung (tiefgekühlt)","g":"gemuese","k":72,"e":3.3,"f":0.5,"c":13.5,"q":"U170471","b":4.0,"vc":10.4,"ko":1,"w":50,"z":8,"h":180,"ht":"6–12 Monate (−18 °C)","p":[["Beutel 750 g",750]],"l":"t","s":"tk tiefkühl"},
{"i":"aepfel","n":"Äpfel","g":"obst","k":53,"e":0.3,"f":0.2,"c":11.4,"q":"A","b":2.4,"vc":4.6,"vq":"U171688","h":90,"ht":"3–5 Monate (kühl, dunkel)","p":[["Beutel 1 kg",1000]],"st":150,"s":"apfel"},
{"i":"bananen","n":"Bananen","g":"obst","k":93,"e":1.1,"f":0.3,"c":20.2,"q":"A","b":2.6,"vc":8.7,"vq":"U173944","ht":"MHD auf der Packung","st":120,"s":"banane"},
{"i":"orangen","n":"Orangen","g":"obst","k":47,"e":0.9,"f":0.1,"c":9.4,"q":"A","b":2.4,"vc":53.2,"vq":"U169097","ht":"MHD auf der Packung","st":150,"s":"apfelsine"},
{"i":"pfirsiche","n":"Pfirsiche (Dose)","g":"obst","k":54,"e":0.5,"f":0.0,"c":14.6,"q":"U169111","b":1.3,"vc":2.4,"h":365,"ht":"etwa 1 Jahr","p":[["Dose 820 g",820],["Dose 410 g",410]],"s":"konserve obst"},
{"i":"birnen","n":"Birnen (Dose)","g":"obst","k":57,"e":0.2,"f":0.0,"c":15.2,"q":"U169938","b":1.6,"vc":0.7,"h":365,"ht":"etwa 1 Jahr","p":[["Dose 820 g",820]],"s":"konserve obst"},
{"i":"mandarinen","n":"Mandarinen (Dose)","g":"obst","k":61,"e":0.5,"f":0.1,"c":16.2,"q":"U169924","b":0.7,"vc":19.8,"h":365,"ht":"etwa 1 Jahr","p":[["Dose 314 ml (300 g)",300]],"s":"konserve obst"},
{"i":"ananas","n":"Ananas (Dose, im Saft)","g":"obst","k":60,"e":0.4,"f":0.1,"c":15.7,"q":"U169126","b":0.8,"vc":9.5,"h":365,"ht":"etwa 1 Jahr","p":[["Dose 580 ml (565 g)",565]],"s":"konserve obst"},
{"i":"kirschen","n":"Sauerkirschen (Glas)","g":"obst","k":75,"e":0.7,"f":0.1,"c":19.3,"q":"U173956","b":0.8,"vc":2.0,"h":365,"ht":"etwa 1 Jahr","p":[["Glas 720 ml (680 g)",680]],"s":"konserve obst"},
{"i":"apfelmus","n":"Apfelmus (Glas)","g":"obst","k":68,"e":0.2,"f":0.2,"c":17.5,"q":"U171696","b":1.2,"vc":1.7,"h":365,"ht":"etwa 1 Jahr","p":[["Glas 720 ml (710 g)",710],["Glas 360 ml (355 g)",355]],"s":"konserve obst"},
{"i":"rosinen","n":"Rosinen","g":"obst","k":299,"e":3.3,"f":0.2,"c":79.3,"q":"U168165","b":4.5,"vc":2.3,"h":365,"ht":"etwa 1 Jahr","p":[["Beutel 250 g",250]],"s":"trockenobst sultaninen"},
{"i":"pflaumen_getr","n":"Trockenpflaumen","g":"obst","k":240,"e":2.2,"f":0.4,"c":63.9,"q":"U168162","b":7.1,"vc":0.6,"h":365,"ht":"etwa 1 Jahr","p":[["Beutel 250 g",250]],"s":"trockenobst backpflaumen"},
{"i":"aprikosen_getr","n":"Aprikosen, getrocknet","g":"obst","k":241,"e":3.4,"f":0.5,"c":62.6,"q":"U173941","b":7.3,"vc":1.0,"h":365,"ht":"etwa 1 Jahr","p":[["Beutel 200 g",200]],"s":"trockenobst"},
{"i":"feigen_getr","n":"Feigen, getrocknet","g":"obst","k":249,"e":3.3,"f":0.9,"c":63.9,"q":"U174665","b":9.8,"vc":1.2,"h":365,"ht":"etwa 1 Jahr","p":[["Beutel 200 g",200]],"s":"trockenobst"},
{"i":"datteln","n":"Datteln, getrocknet","g":"obst","k":290,"e":1.8,"f":0.2,"c":68,"q":"A","b":6.7,"vc":0.4,"vq":"U171726","h":365,"ht":"etwa 1 Jahr","p":[["Beutel 200 g",200]],"s":"trockenobst"},
{"i":"haselnuesse","n":"Haselnüsse","g":"obst","k":650,"e":15,"f":61,"c":7,"q":"A","b":9.7,"vc":6.3,"vq":"U170581","ht":"MHD auf der Packung","p":[["Beutel 200 g",200]],"s":"nüsse"},
{"i":"walnuesse","n":"Walnüsse","g":"obst","k":690,"e":15,"f":65,"c":7,"q":"A","b":6.7,"vc":1.3,"vq":"U170187","ht":"MHD auf der Packung","p":[["Beutel 200 g",200]],"s":"nüsse"},
{"i":"mandeln","n":"Mandeln","g":"obst","k":580,"e":21,"f":50,"c":5.7,"q":"A","b":12.5,"vc":0.0,"vq":"U170158","ht":"MHD auf der Packung","p":[["Beutel 200 g",200]],"s":"nüsse"},
{"i":"erdnuesse","n":"Erdnüsse, geröstet","g":"obst","k":610,"e":24,"f":50,"c":13,"q":"A","b":8,"vc":0.0,"vq":"U173806","ht":"MHD auf der Packung","p":[["Dose 200 g",200]],"s":"nüsse"},
{"i":"cashew","n":"Cashewkerne","g":"obst","k":580,"e":18,"f":44,"c":27,"q":"A","b":3.3,"vc":0.5,"vq":"U170162","ht":"MHD auf der Packung","p":[["Beutel 200 g",200]],"s":"nüsse"},
{"i":"erdnussmus","n":"Erdnussmus / Erdnussbutter","g":"obst","k":600,"e":25,"f":50,"c":14,"q":"A","b":6,"vc":0.0,"vq":"U172470","ht":"MHD auf der Packung","p":[["Glas 350 g",350]],"s":"erdnussbutter nüsse"},
{"i":"sonnenblumenkerne","n":"Sonnenblumenkerne","g":"obst","k":600,"e":21,"f":51,"c":11,"q":"A","b":8.6,"vc":1.4,"vq":"U170562","ht":"MHD auf der Packung","p":[["Beutel 200 g",200]],"s":"kerne saaten"},
{"i":"kuerbiskerne","n":"Kürbiskerne","g":"obst","k":590,"e":30,"f":49,"c":5,"q":"A","b":6,"vc":1.9,"vq":"U170556","ht":"MHD auf der Packung","p":[["Beutel 200 g",200]],"s":"kerne saaten"},
{"i":"leinsamen","n":"Leinsamen","g":"obst","k":510,"e":18,"f":42,"c":1.6,"q":"A","b":27,"vc":0.6,"vq":"U169414","ht":"MHD auf der Packung","p":[["Beutel 250 g",250]],"s":"kerne saaten"},
{"i":"hmilch","n":"H-Milch 3,5 %","g":"milch","k":64,"e":3.3,"f":3.5,"c":4.8,"q":"A","b":0,"vc":0.0,"vq":"U171265","ht":"MHD auf der Packung","p":[["Packung 1 l",1000]],"ml":1,"s":"milch haltbarmilch uht"},
{"i":"hmilch15","n":"H-Milch 1,5 %","g":"milch","k":47,"e":3.4,"f":1.5,"c":4.9,"q":"A","b":0,"vc":0.2,"vq":"U171267","ht":"MHD auf der Packung","p":[["Packung 1 l",1000]],"ml":1,"s":"milch haltbarmilch fettarm"},
{"i":"frischmilch","n":"Frischmilch","g":"milch","k":64,"e":3.3,"f":3.5,"c":4.8,"q":"A","b":0,"vc":0.0,"vq":"U171265","h":2,"ht":"2–5 Tage (Kühlschrank)","p":[["Flasche 1 l",1000]],"l":"k","ml":1,"s":"milch"},
{"i":"milchpulver","n":"Vollmilchpulver","g":"milch","k":496,"e":26.3,"f":26.7,"c":38.4,"q":"U173454","b":0.0,"vc":8.6,"ht":"MHD auf der Packung","p":[["Packung 400 g",400]],"x":8.13,"s":"trockenmilch pulver"},
{"i":"kondensmilch","n":"Kondensmilch 7,5 %","g":"milch","k":134,"e":6.8,"f":7.6,"c":10.0,"q":"U172194","b":0.0,"vc":1.9,"ht":"MHD auf der Packung","p":[["Dose 340 g",340],["Tube 170 g",170]],"s":"dosenmilch"},
{"i":"hartkaese","n":"Hartkäse am Stück (z. B. Parmesan, Bergkäse)","g":"milch","k":390,"e":35,"f":26,"c":0,"q":"A","b":0,"vc":0.0,"vq":"U170848","ht":"MHD auf der Packung","p":[["Stück 200 g",200]],"l":"k","s":"käse"},
{"i":"gouda","n":"Schnittkäse (z. B. Gouda)","g":"milch","k":360,"e":25,"f":29,"c":0,"q":"A","b":0,"vc":0.0,"vq":"U171241","h":8,"ht":"8–10 Tage","p":[["Packung 400 g",400]],"l":"k","s":"käse"},
{"i":"joghurt","n":"Naturjoghurt","g":"milch","k":66,"e":3.8,"f":3.5,"c":4.6,"q":"A","b":0,"vc":0.5,"vq":"U171284","h":14,"ht":"etwa 2 Wochen (Kühlschrank)","p":[["Becher 500 g",500]],"l":"k","s":"jogurt"},
{"i":"quark","n":"Magerquark","g":"milch","k":67,"e":12,"f":0.3,"c":4,"q":"A","b":0,"vc":0.0,"vq":"U172181","ht":"MHD auf der Packung","p":[["Becher 500 g",500]],"l":"k","s":"topfen"},
{"i":"sahne","n":"Schlagsahne 30 %","g":"milch","k":290,"e":2.4,"f":30,"c":3.2,"q":"A","b":0,"vc":0.6,"vq":"U170859","h":14,"ht":"etwa 2 Wochen (Kühlschrank)","p":[["Becher 200 g",200]],"l":"k","s":"sahne"},
{"i":"hafermilch","n":"Haferdrink","g":"milch","k":46,"e":1,"f":1.5,"c":6.7,"q":"A","b":0.8,"ht":"MHD auf der Packung","p":[["Packung 1 l",1000]],"ml":1,"s":"hafermilch pflanzendrink"},
{"i":"sojadrink","n":"Sojadrink ungesüßt","g":"milch","k":35,"e":3.3,"f":1.9,"c":0.5,"q":"A","b":0.6,"ht":"MHD auf der Packung","p":[["Packung 1 l",1000]],"ml":1,"s":"sojamilch pflanzendrink"},
{"i":"thunfisch","n":"Thunfisch im eigenen Saft (Dose, abgetropft)","g":"eiweiss","k":110,"e":25,"f":1,"c":0,"q":"A","b":0,"vc":0.0,"vq":"U173709","h":730,"ht":"mehrere Jahre","p":[["Dose 185 g (150 g abgetropft)",150]],"s":"fisch konserve"},
{"i":"sardinen","n":"Sardinen in Öl (Dose, abgetropft)","g":"eiweiss","k":208,"e":24.6,"f":11.4,"c":0.0,"q":"U175139","b":0.0,"vc":0.0,"h":730,"ht":"mehrere Jahre","p":[["Dose 125 g (90 g abgetropft)",90]],"s":"fisch konserve"},
{"i":"makrele","n":"Makrelenfilet (Dose, abgetropft)","g":"eiweiss","k":156,"e":23.2,"f":6.3,"c":0.0,"q":"U175121","b":0.0,"vc":0.9,"h":730,"ht":"mehrere Jahre","p":[["Dose 125 g (90 g abgetropft)",90]],"s":"fisch konserve"},
{"i":"lachs_dose","n":"Lachs (Dose, abgetropft)","g":"eiweiss","k":138,"e":23.1,"f":5.0,"c":0.0,"q":"U175175","b":0.0,"vc":0.0,"h":730,"ht":"mehrere Jahre","p":[["Dose 213 g (150 g abgetropft)",150]],"s":"fisch konserve"},
{"i":"corned_beef","n":"Corned Beef (Dose)","g":"eiweiss","k":250,"e":27.1,"f":14.9,"c":0.0,"q":"U170602","b":0.0,"vc":0.0,"h":730,"ht":"mehrere Jahre","p":[["Dose 340 g",340]],"s":"fleisch konserve rind"},
{"i":"fruehstuecksfleisch","n":"Frühstücksfleisch (Dose)","g":"eiweiss","k":334,"e":12.5,"f":30.3,"c":2.1,"q":"U174571","b":0.0,"vc":1.0,"h":730,"ht":"mehrere Jahre","p":[["Dose 200 g",200]],"s":"fleisch konserve schwein"},
{"i":"leberwurst","n":"Leberwurst (Dose/Glas)","g":"eiweiss","k":300,"e":14,"f":27,"c":1.5,"q":"A","b":0,"vc":0.0,"vq":"U173870","h":730,"ht":"mehrere Jahre","p":[["Dose 125 g",125],["Glas 200 g",200]],"s":"wurst konserve"},
{"i":"wuerstchen","n":"Würstchen im Glas (Wiener/Bockwurst)","g":"eiweiss","k":280,"e":13,"f":25,"c":1,"q":"A","b":0,"z":5,"h":730,"ht":"mehrere Jahre","p":[["Glas 6 St. (250 g abgetropft)",250]],"st":42,"s":"bockwurst wiener wurst konserve"},
{"i":"salami","n":"Salami / Dauerwurst","g":"eiweiss","k":380,"e":21,"f":33,"c":1,"q":"A","b":0,"vc":0.0,"vq":"U172938","ht":"MHD auf der Packung","p":[["Stück 250 g",250]],"s":"wurst dauerwurst"},
{"i":"jagdwurst","n":"Jagdwurst / Fleischwurst","g":"eiweiss","k":308,"e":15.2,"f":24.6,"c":5.5,"q":"U172013","b":0.0,"vc":0.8,"ht":"MHD auf der Packung","p":[["Ring 400 g",400]],"l":"k","s":"wurst lyoner"},
{"i":"chili","n":"Chili con Carne (Dose)","g":"eiweiss","k":107,"e":5.8,"f":3.5,"c":13.1,"q":"U172097","b":3.3,"vc":0.2,"z":5,"h":730,"ht":"mehrere Jahre","p":[["Dose 800 g",800],["Dose 400 g",400]],"s":"fertiggericht konserve"},
{"i":"gulasch","n":"Rindergulasch / Eintopf mit Fleisch (Dose)","g":"eiweiss","k":99,"e":4.4,"f":5.5,"c":7.8,"q":"U173330","b":0.9,"vc":0.7,"z":5,"h":730,"ht":"mehrere Jahre","p":[["Dose 800 g",800],["Dose 400 g",400]],"s":"fertiggericht konserve eintopf"},
{"i":"eier","n":"Eier (Größe M)","g":"eiweiss","k":143,"e":12.6,"f":9.5,"c":0.7,"q":"A","b":0,"vc":0.0,"vq":"U171287","ko":1,"w":50,"z":10,"ht":"MHD auf der Packung","p":[["Packung 10 St.",530],["Packung 6 St.",318]],"st":53,"s":"ei hühnerei"},
{"i":"hack_tk","n":"Hackfleisch (tiefgekühlt)","g":"eiweiss","k":254,"e":17,"f":20,"c":0,"q":"A","b":0,"vc":0.0,"vq":"U174036","ko":1,"z":15,"h":90,"ht":"3–12 Monate (−18 °C)","p":[["Packung 500 g",500]],"l":"t","s":"hack fleisch tk"},
{"i":"haehnchen_tk","n":"Hähnchenbrust (tiefgekühlt)","g":"eiweiss","k":110,"e":23,"f":1.5,"c":0,"q":"A","b":0,"vc":0.0,"vq":"U171077","ko":1,"z":20,"h":90,"ht":"3–12 Monate (−18 °C)","p":[["Packung 1 kg",1000]],"l":"t","s":"huhn fleisch tk geflügel"},
{"i":"fisch_tk","n":"Fischfilet (tiefgekühlt)","g":"eiweiss","k":82,"e":18,"f":0.7,"c":0,"q":"A","b":0,"vc":1.0,"vq":"U171955","ko":1,"z":15,"h":90,"ht":"3–12 Monate (−18 °C)","p":[["Packung 400 g",400]],"l":"t","s":"seelachs kabeljau tk"},
{"i":"tofu","n":"Tofu natur","g":"eiweiss","k":125,"e":13.5,"f":7.5,"c":1,"q":"A","b":1,"vc":0.2,"vq":"U172475","ht":"MHD auf der Packung","p":[["Packung 200 g",200]],"l":"k","s":"soja fleischersatz"},
{"i":"rapsoel","n":"Rapsöl","g":"fett","k":884,"e":0,"f":100,"c":0,"q":"A","b":0,"h":180,"ht":"6–12 Monate","p":[["Flasche 1 l (920 g)",920],["Flasche 0,5 l (460 g)",460]],"s":"öl speiseöl"},
{"i":"sonnenblumenoel","n":"Sonnenblumenöl","g":"fett","k":884,"e":0,"f":100,"c":0,"q":"A","b":0,"h":180,"ht":"6–12 Monate","p":[["Flasche 1 l (920 g)",920]],"s":"öl speiseöl"},
{"i":"olivenoel","n":"Olivenöl","g":"fett","k":884,"e":0,"f":100,"c":0,"q":"A","b":0,"h":180,"ht":"6–12 Monate","p":[["Flasche 0,75 l (690 g)",690],["Flasche 0,5 l (460 g)",460]],"s":"öl"},
{"i":"butter","n":"Butter","g":"fett","k":741,"e":0.7,"f":82,"c":0.6,"q":"A","b":0,"h":28,"ht":"4–6 Wochen (Kühlschrank)","p":[["Stück 250 g",250]],"l":"k"},
{"i":"margarine","n":"Margarine","g":"fett","k":720,"e":0.2,"f":80,"c":0.4,"q":"A","b":0,"h":28,"ht":"4–6 Wochen (Kühlschrank)","p":[["Becher 500 g",500]],"l":"k"},
{"i":"butterschmalz","n":"Butterschmalz","g":"fett","k":876,"e":0.3,"f":99.5,"c":0.0,"q":"U173412","b":0.0,"vc":0.0,"h":180,"ht":"viele Monate","p":[["Glas 500 g",500],["Packung 250 g",250]],"s":"ghee"},
{"i":"schmalz","n":"Schweineschmalz","g":"fett","k":900,"e":0,"f":100,"c":0,"q":"A","b":0,"ht":"MHD auf der Packung","p":[["Becher 250 g",250]]},
{"i":"kokosfett","n":"Kokosfett","g":"fett","k":890,"e":0,"f":100,"c":0,"q":"A","b":0,"h":180,"ht":"viele Monate","p":[["Packung 250 g",250]],"s":"kokosöl palmin"},
{"i":"wasser","n":"Mineralwasser","g":"trinken","k":0,"e":0,"f":0,"c":0,"q":"—","b":0,"vc":0,"h":365,"ht":"MHD meist 1–1½ Jahre","p":[["Flasche 1,5 l",1500],["Flasche 1 l",1000],["Flasche 0,5 l",500],["Kasten 6 × 1,5 l",9000],["Kasten 12 × 0,7 l",8400]],"ml":1,"fl":1,"s":"trinkwasser sprudel flasche"},
{"i":"wasser_kanister","n":"Trinkwasser im Kanister (selbst abgefüllt)","g":"trinken","k":0,"e":0,"f":0,"c":0,"q":"—","b":0,"vc":0,"ht":"MHD auf der Packung","p":[["Kanister 5 l",5000],["Kanister 10 l",10000],["Kanister 20 l",20000]],"ml":1,"fl":1,"s":"leitungswasser kanister"},
{"i":"apfelsaft","n":"Apfelsaft","g":"trinken","k":46,"e":0.1,"f":0.1,"c":11.3,"q":"U173933","b":0.2,"vc":0.9,"ht":"MHD auf der Packung","p":[["Flasche 1 l",1000]],"ml":1,"fl":1,"s":"saft"},
{"i":"orangensaft","n":"Orangensaft","g":"trinken","k":43,"e":0.7,"f":0.2,"c":9,"q":"A","b":0.2,"vc":50.0,"vq":"U169098","ht":"MHD auf der Packung","p":[["Packung 1 l",1000]],"ml":1,"fl":1,"s":"saft"},
{"i":"zitronensaft","n":"Zitronensaft","g":"trinken","k":17,"e":0.5,"f":0.1,"c":5.6,"q":"U167748","b":0.7,"vc":14.3,"ht":"MHD auf der Packung","p":[["Flasche 200 ml",200]],"ml":1,"s":"zitrone"},
{"i":"tee","n":"Tee (schwarz oder Kräuter)","g":"trinken","k":0,"e":0,"f":0,"c":0,"q":"—","b":0,"vc":0,"h":3650,"ht":"praktisch unbegrenzt (trocken)","p":[["Packung 20 Beutel (40 g)",40]],"kein":1,"s":"teebeutel"},
{"i":"kaffee","n":"Kaffee (Pulver)","g":"trinken","k":0,"e":0,"f":0,"c":0,"q":"—","b":0,"vc":0,"ht":"MHD auf der Packung","p":[["Packung 500 g",500],["Glas Instant 100 g",100]],"kein":1,"s":"instant"},
{"i":"zucker","n":"Zucker","g":"sonst","k":400,"e":0,"f":0,"c":100,"q":"A","b":0,"vc":0.0,"vq":"U169655","h":3650,"ht":"praktisch unbegrenzt (trocken)","p":[["Packung 1 kg",1000]],"s":"zucker"},
{"i":"honig","n":"Honig","g":"sonst","k":326,"e":0.3,"f":0,"c":81,"q":"A","b":0,"ht":"MHD auf der Packung","p":[["Glas 500 g",500]]},
{"i":"marmelade","n":"Konfitüre / Marmelade","g":"sonst","k":278,"e":0.4,"f":0.1,"c":68.9,"q":"U169641","b":1.1,"vc":8.8,"h":365,"ht":"etwa 1 Jahr","p":[["Glas 450 g",450]],"s":"marmelade gelee"},
{"i":"nusscreme","n":"Nuss-Nougat-Creme","g":"sonst","k":539,"e":5.4,"f":29.7,"c":62.4,"q":"U168000","b":5.4,"vc":0.0,"ht":"MHD auf der Packung","p":[["Glas 400 g",400]],"s":"schokocreme"},
{"i":"schoko","n":"Vollmilchschokolade","g":"sonst","k":535,"e":7,"f":30,"c":57,"q":"A","b":2,"vc":0.0,"vq":"U167587","ht":"MHD auf der Packung","p":[["Tafel 100 g",100]],"s":"schokolade"},
{"i":"zartbitter","n":"Zartbitterschokolade","g":"sonst","k":575,"e":7.8,"f":42,"c":35,"q":"A","b":11,"vq":"U170273","ht":"MHD auf der Packung","p":[["Tafel 100 g",100]],"s":"schokolade"},
{"i":"kakao","n":"Kakaopulver (ungesüßt)","g":"sonst","k":228,"e":19.6,"f":13.7,"c":57.9,"q":"U169593","b":37.0,"vc":0.0,"ht":"MHD auf der Packung","p":[["Dose 250 g",250]]},
{"i":"kekse","n":"Butterkekse","g":"sonst","k":435,"e":7.5,"f":11,"c":74,"q":"A","b":2.5,"vc":0.0,"vq":"U172819","ht":"MHD auf der Packung","p":[["Packung 200 g",200]],"s":"kekse"},
{"i":"riegel","n":"Müsliriegel","g":"sonst","k":471,"e":10.1,"f":19.8,"c":64.4,"q":"U167542","b":5.3,"vc":0.9,"ht":"MHD auf der Packung","p":[["Packung 6 St. (150 g)",150]],"st":25,"s":"riegel"},
{"i":"salzstangen","n":"Salzstangen / Brezeln","g":"sonst","k":384,"e":10.0,"f":2.9,"c":80.4,"q":"U167555","b":3.4,"vc":2.1,"ht":"MHD auf der Packung","p":[["Beutel 250 g",250]]},
{"i":"chips","n":"Kartoffelchips","g":"sonst","k":530,"e":6,"f":33,"c":50,"q":"A","b":4.5,"vc":21.6,"vq":"U169677","ht":"MHD auf der Packung","p":[["Beutel 175 g",175]]},
{"i":"crackers","n":"Cracker","g":"sonst","k":418,"e":9.5,"f":8.6,"c":74.0,"q":"U172746","b":2.8,"vc":0.0,"ht":"MHD auf der Packung","p":[["Packung 200 g",200]]},
{"i":"salz","n":"Salz","g":"sonst","k":0,"e":0,"f":0,"c":0,"q":"—","b":0,"vc":0,"h":3650,"ht":"praktisch unbegrenzt (trocken)","p":[["Packung 500 g",500]],"kein":1},
{"i":"bruehe","n":"Gemüsebrühe (Pulver)","g":"sonst","k":267,"e":16.7,"f":13.9,"c":18.0,"q":"U171562","b":0.0,"vc":1.1,"ht":"MHD auf der Packung","p":[["Glas 150 g (ca. 7 l)",150]],"s":"brühe bouillon suppenpulver"},
{"i":"trockenhefe","n":"Trockenhefe","g":"sonst","k":325,"e":40.4,"f":7.6,"c":41.2,"q":"U175043","b":26.9,"vc":0.3,"ht":"MHD auf der Packung","p":[["Päckchen 7 g",7]],"s":"hefe"},
{"i":"frischhefe","n":"Frische Hefe","g":"sonst","k":105,"e":8.4,"f":1.9,"c":18.1,"q":"U175042","b":8.1,"vc":0.1,"ko":1,"ht":"MHD auf der Packung","p":[["Würfel 42 g",42]],"l":"k","s":"hefe würfel"},
{"i":"backpulver","n":"Backpulver","g":"sonst","k":51,"e":0.1,"f":0.0,"c":24.1,"q":"U172804","b":0.2,"vc":0.0,"ko":1,"ht":"MHD auf der Packung","p":[["Päckchen 15 g",15]]},
{"i":"puddingpulver","n":"Puddingpulver","g":"sonst","k":379,"e":0.3,"f":0.4,"c":93.5,"q":"U169609","b":0.6,"vc":0.0,"ko":1,"z":5,"ht":"MHD auf der Packung","p":[["Päckchen 37 g",37]],"s":"pudding"},
{"i":"essig","n":"Essig","g":"sonst","k":21,"e":0.0,"f":0.0,"c":0.9,"q":"U173469","b":0.0,"vc":0.0,"h":3650,"ht":"praktisch unbegrenzt (trocken)","p":[["Flasche 750 ml",750]],"ml":1},
{"i":"senf","n":"Senf","g":"sonst","k":60,"e":3.7,"f":3.3,"c":5.8,"q":"U172234","b":4.0,"vc":0.3,"ht":"MHD auf der Packung","p":[["Tube 200 ml",200]]},
{"i":"ketchup","n":"Ketchup","g":"sonst","k":101,"e":1.0,"f":0.1,"c":27.4,"q":"U168556","b":0.3,"vc":4.1,"ht":"MHD auf der Packung","p":[["Flasche 500 ml (550 g)",550]]},
{"i":"mayonnaise","n":"Mayonnaise","g":"sonst","k":720,"e":1,"f":79,"c":1.5,"q":"A","b":0,"ht":"MHD auf der Packung","p":[["Glas 250 ml (240 g)",240]],"s":"mayo"},
{"i":"suppe_tuete","n":"Instant-Suppe (Tüte)","g":"sonst","k":377,"e":15.4,"f":6.5,"c":62.3,"q":"U171571","b":3.2,"vc":0.0,"ko":1,"w":500,"z":5,"ht":"MHD auf der Packung","p":[["Tüte 60 g (für 0,5 l)",60]],"s":"tütensuppe nudelsuppe"},
{"i":"saeuglingsmilch","n":"Säuglingsmilch (Pulver)","g":"baby","k":522,"e":10.9,"f":28.9,"c":54.7,"q":"U173561","b":0.0,"vc":47.3,"ko":1,"ht":"MHD auf der Packung","p":[["Packung 800 g",800]],"s":"pre milch anfangsnahrung baby"},
{"i":"babybrei_getreide","n":"Getreidebrei für Babys (Pulver)","g":"baby","k":390,"e":6.7,"f":2.2,"c":83.1,"q":"U170969","b":1.3,"vc":2.4,"ko":1,"ht":"MHD auf der Packung","p":[["Packung 250 g",250]],"s":"baby brei reisflocken"},
{"i":"babygl_menue","n":"Baby-Menü im Glas","g":"baby","k":53,"e":2.0,"f":1.1,"c":8.7,"q":"U173513","b":1.1,"vc":0.2,"ht":"MHD auf der Packung","p":[["Glas 190 g",190]],"s":"baby gläschen"},
{"i":"babygl_obst","n":"Obstbrei für Babys (Glas)","g":"baby","k":41,"e":0.2,"f":0.2,"c":10.8,"q":"U173512","b":1.7,"vc":38.3,"ht":"MHD auf der Packung","p":[["Glas 125 g",125]],"s":"baby gläschen apfel"}
];
var KAT = {}; KATALOG.forEach(function (k) { KAT[k.i] = k; });

/* DGE-Richtwerte für die Energiezufuhr (kcal/Tag), Ableitung 2015, für PAL 1,4 · 1,6 · 1,8; Referenzgewicht kg (m, w) */
var DGE_E = [
  [1, 4, [1200, 1200, 1200], [1100, 1100, 1100], 13.9, 13.2],
  [4, 7, [1400, 1600, 1800], [1300, 1500, 1700], 20.2, 20.1],
  [7, 10, [1700, 1900, 2100], [1500, 1800, 2000], 29.3, 28.7],
  [10, 13, [1900, 2200, 2400], [1700, 2000, 2200], 41.0, 42.1],
  [13, 15, [2300, 2600, 2900], [1900, 2200, 2500], 55.5, 54.0],
  [15, 19, [2600, 3000, 3400], [2000, 2300, 2600], 69.2, 59.5],
  [19, 25, [2400, 2800, 3100], [1900, 2200, 2500], 70.8, 60.5],
  [25, 51, [2300, 2700, 3000], [1800, 2100, 2400], 70.7, 60.0],
  [51, 65, [2200, 2500, 2800], [1700, 2000, 2200], 68.7, 58.2],
  [65, 200, [2100, 2500, 2800], [1700, 1900, 2100], 66.8, 57.1]
];
var TAETIG = [['ruhig', 'ruhig', 1.4, 'meist sitzend'], ['normal', 'normal', 1.6, 'etwas Bewegung'], ['koerper', 'körperlich', 1.8, 'viel auf den Beinen']];
/* DGE-Referenzwerte Protein (g je kg Körpergewicht und Tag), Ableitung 2017 */
function eiweissProKg(a, s) { if (a < 4) return 1.0; if (a < 15) return 0.9; if (a < 19) return s === 'w' ? 0.8 : 0.9; if (a < 65) return 0.8; return 1.0; }
/* BBK-Ratgeber (Stand 11/2025): 2 l Wasser je Person und Tag, davon 0,5 l zum Kochen */
var WASSER_TAG = 2, WASSER_KOCHEN = 0.5;

var ORTE = [['v', 'Vorrat'], ['k', 'Kühlschrank'], ['t', 'Gefriertruhe']];
var ORT = { v: 'Vorrat', k: 'Kühlschrank', t: 'Gefriertruhe' };
/* Lagerorte sind frei benennbar (S.orte: {id, n, typ}); typ v = ungekühlt, k = gekühlt, t = gefroren – zählt für „Strom weg“ */
var ORTE_STD = [{ id: 'v', n: 'Vorrat', typ: 'v' }, { id: 'k', n: 'Kühlschrank', typ: 'k' }, { id: 't', n: 'Gefriertruhe', typ: 't' }];
function ortVon(S, id) { var L = (S && S.orte) || ORTE_STD; for (var i = 0; i < L.length; i++) if (L[i].id === id) return L[i]; return ORTE_STD.filter(function (o) { return o.id === id; })[0] || ORTE_STD[0]; }
function ortTyp(S, id) { return ortVon(S, id || 'v').typ; }
function ortName(S, id) { return ortVon(S, id || 'v').n; }
var KOCH = [['keine', 'Keine', 'keine Kochstelle'], ['gas', 'Gaskocher', 'Campingkocher mit Kartusche'], ['feuer', 'Grill / Feuer', 'Grill, Feuerstelle'], ['holzofen', 'Holzofen', 'mit Backfach'], ['herd', 'Herd normal', 'Herd und Backofen gehen']];
var KOCHT = {}; KOCH.forEach(function (k) { KOCHT[k[0]] = k[1]; });
/* welche Kochstelle reicht für welches Gericht */
var KANN = { kalt: ['keine', 'gas', 'feuer', 'holzofen', 'herd'], topf: ['gas', 'feuer', 'holzofen', 'herd'], glut: ['feuer', 'holzofen'], ofen: ['holzofen', 'herd'] };
var KNAME = { kalt: 'ohne Kochen', topf: 'Topf/Pfanne', glut: 'Glut/Feuer', ofen: 'Backofen' };
var ZIELE = [3, 10, 14, 28];
var VORSCHLAG = { getreide: ['nudeln', 'reis', 'haferflocken', 'knaecke'], gemuese: ['linsen', 'kidney_dose', 'erbsen_moehren', 'tomaten_dose'], obst: ['pfirsiche', 'apfelmus', 'rosinen', 'haselnuesse'],
  milch: ['hmilch', 'hartkaese', 'milchpulver'], eiweiss: ['thunfisch', 'wuerstchen', 'corned_beef'], fett: ['rapsoel', 'butterschmalz'] };

/* Gerichte: [id, Name, Art, Kochstelle, Portionen, Wasser ml (ganze Menge), Zeit min, Zutaten, Schritte, Zusatz]
   Zutat: ['id|id2|id3*3', Gramm für die ganze Menge, optional]. „*3“ = von dieser Zutat die dreifache Menge (z. B. Frischhefe statt Trockenhefe).
   Kochstelle: kalt · topf (Gaskocher, Grill, Holzofen, Herd) · glut (offenes Feuer/Holzofen) · ofen (Backofen/Holzofen mit Backfach). fr = fürs Frühstück */
var GERICHTE_ROH = [
  /* ---- kalt: ohne Kochen ---- */
  ['muesli', 'Haferflocken-Müsli mit Milch', 'kalt', 'kalt', 1, 0, 5, [['haferflocken|muesli', 60], ['hmilch|hmilch15|frischmilch|hafermilch|sojadrink', 200], ['rosinen|aprikosen_getr|pflaumen_getr|datteln', 20, 1]], ['Haferflocken in eine Schüssel geben.', 'Milch oder Pflanzendrink darübergießen, 5 Minuten quellen lassen.', 'Trockenobst klein schneiden und darüberstreuen.'], { fr: 1 }],
  ['oats', 'Über-Nacht-Haferflocken mit Apfelmus', 'kalt', 'kalt', 1, 0, 5, [['haferflocken', 60], ['hmilch|hmilch15|frischmilch|hafermilch|sojadrink', 150], ['apfelmus|pfirsiche|kirschen', 100]], ['Haferflocken und Milch mischen, abgedeckt über Nacht stehen lassen.', 'Am Morgen Apfelmus oder Obst unterrühren.'], { fr: 1 }],
  ['joghurt', 'Joghurt mit Müsli', 'kalt', 'kalt', 1, 0, 3, [['joghurt|quark', 150], ['muesli|haferflocken|cornflakes', 50]], ['Joghurt in eine Schüssel geben, Müsli darüber.', 'Kühlware zuerst aufbrauchen.'], { fr: 1 }],
  ['quark_obst', 'Quark mit Obst', 'kalt', 'kalt', 2, 0, 5, [['quark|joghurt', 250], ['pfirsiche|mandarinen|kirschen|apfelmus|ananas', 200], ['honig|zucker', 10, 1]], ['Quark glatt rühren, bei Bedarf mit etwas Obstsaft aus der Dose.', 'Obst abtropfen, klein schneiden und unterheben. Nach Geschmack süßen.'], { fr: 1 }],
  ['knaecke_wurst', 'Knäckebrot mit Leberwurst und Gurke', 'kalt', 'kalt', 1, 0, 3, [['knaecke|zwieback|vkbrot', 50], ['leberwurst|fruehstuecksfleisch|salami', 40], ['gurken', 30, 1]], ['Knäckebrot bestreichen bzw. belegen.', 'Gurkenscheiben darauflegen.'], { fr: 1 }],
  ['knaecke_kaese', 'Knäckebrot mit Käse und Apfel', 'kalt', 'kalt', 1, 0, 3, [['knaecke|zwieback|vkbrot|mischbrot', 50], ['hartkaese|gouda', 40], ['aepfel|birnen', 150]], ['Käse in Scheiben schneiden und aufs Brot legen.', 'Apfel dazu essen.'], { fr: 1 }],
  ['brot_erdnuss', 'Brot mit Erdnussmus und Banane', 'kalt', 'kalt', 1, 0, 3, [['vkbrot|mischbrot|toast|knaecke', 100], ['erdnussmus|nusscreme', 25], ['bananen|aepfel', 120]], ['Brot mit Erdnussmus bestreichen.', 'Banane in Scheiben darauflegen.'], { fr: 1 }],
  ['brot_honig', 'Brot mit Butter und Honig', 'kalt', 'kalt', 1, 0, 2, [['vkbrot|mischbrot|toast|broetchen|knaecke', 100], ['butter|margarine', 15, 1], ['honig|marmelade|nusscreme', 25]], ['Brot mit Butter und Honig oder Marmelade bestreichen.'], { fr: 1 }],
  ['corned_brot', 'Brot mit Corned Beef und Gurke', 'kalt', 'kalt', 2, 0, 5, [['vkbrot|mischbrot|knaecke|toast', 200], ['corned_beef|fruehstuecksfleisch', 170], ['gurken|rote_bete', 60, 1], ['senf', 10, 1]], ['Fleisch aus der Dose in Scheiben schneiden.', 'Brot mit Senf bestreichen, Fleisch und Gurke darauflegen.'], {}],
  ['thunfisch_bohnen', 'Bohnen-Thunfisch-Salat', 'kalt', 'kalt', 2, 0, 10, [['thunfisch|lachs_dose|makrele', 150], ['bohnen_dose|kidney_dose|kicher_dose', 250], ['zwiebeln', 50, 1], ['rapsoel|olivenoel|sonnenblumenoel', 20], ['essig|zitronensaft', 15, 1]], ['Bohnen abtropfen lassen, Fisch zerpflücken.', 'Zwiebel fein würfeln.', 'Alles mit Öl und Essig mischen, salzen und pfeffern.'], {}],
  ['kicher_salat', 'Kichererbsen-Mais-Salat', 'kalt', 'kalt', 2, 0, 10, [['kicher_dose|kidney_dose|bohnen_dose', 240], ['mais', 140], ['gurken|rote_bete|tomaten_dose', 100, 1], ['olivenoel|rapsoel', 20], ['essig|zitronensaft', 15, 1]], ['Kichererbsen und Mais abtropfen lassen.', 'Gurken klein schneiden.', 'Mit Öl, Essig, Salz und Pfeffer mischen.'], {}],
  ['wraps', 'Wraps mit Bohnen und Mais', 'kalt', 'kalt', 2, 0, 10, [['tortilla', 160], ['baked_beans|kidney_dose|bohnen_dose', 250], ['mais', 140], ['hartkaese|gouda', 40, 1]], ['Bohnen grob zerdrücken.', 'Auf die Fladen streichen, Mais und geriebenen Käse darüber.', 'Aufrollen. Schmeckt kalt, warm noch besser.'], {}],
  ['fisch_knaecke', 'Sardinen auf Knäckebrot', 'kalt', 'kalt', 1, 0, 3, [['sardinen|makrele|thunfisch|lachs_dose', 90], ['knaecke|zwieback|vkbrot', 50], ['zitronensaft', 5, 1]], ['Fisch mit der Gabel zerdrücken und auf das Knäckebrot geben.', 'Nach Geschmack Zitronensaft darüber.'], {}],
  ['couscous_kalt', 'Couscous-Salat (kalt gequollen)', 'kalt', 'kalt', 2, 220, 40, [['couscous', 150], ['tomaten_dose|passata', 200], ['gurken|mais', 80, 1], ['olivenoel|rapsoel', 15], ['bruehe', 4, 1]], ['Couscous mit 220 ml kaltem Wasser und etwas Brühpulver übergießen.', 'Abgedeckt etwa 30–40 Minuten quellen lassen, mit der Gabel auflockern.', 'Tomaten, Gurken und Öl untermischen.'], {}],
  ['obstsalat', 'Obstsalat aus der Dose mit Nüssen', 'kalt', 'kalt', 2, 0, 5, [['pfirsiche|birnen|mandarinen|ananas|kirschen', 300], ['haselnuesse|walnuesse|mandeln|cashew', 40]], ['Obst abtropfen lassen und klein schneiden.', 'Gehackte Nüsse darüberstreuen.'], { fr: 1 }],
  ['studentenfutter', 'Nüsse und Trockenobst', 'kalt', 'kalt', 1, 0, 1, [['erdnuesse|haselnuesse|mandeln|cashew|walnuesse', 30], ['rosinen|aprikosen_getr|pflaumen_getr|datteln|feigen_getr', 30]], ['Nüsse und Trockenobst mischen – gut für unterwegs.'], {}],
  ['dose_kalt', 'Eintopf aus der Dose mit Brot', 'kalt', 'kalt', 1, 0, 2, [['eintopf|chili|gulasch|ravioli|baked_beans', 400], ['mischbrot|vkbrot|knaecke|zwieback', 60]], ['Fertiggerichte aus der Dose sind gegart und können zur Not kalt gegessen werden.', 'Gut umrühren, Brot dazu.'], {}],
  /* ---- warm: Topf oder Pfanne auf Gaskocher, Grill, Feuer, Holzofen oder Herd ---- */
  ['dose_warm', 'Eintopf aus der Dose, aufgewärmt', 'warm', 'topf', 1, 0, 5, [['eintopf|chili|gulasch|ravioli|baked_beans', 400], ['mischbrot|vkbrot|knaecke|zwieback', 60, 1]], ['Doseninhalt in einen Topf geben (nicht in der Dose erhitzen).', 'Unter Rühren heiß werden lassen, Deckel drauf spart Brennstoff.'], {}],
  ['porridge', 'Haferbrei', 'warm', 'topf', 1, 0, 5, [['haferflocken', 70], ['hmilch|hmilch15|frischmilch|hafermilch|sojadrink', 250], ['rosinen|apfelmus|aprikosen_getr', 30, 1], ['zucker|honig', 10, 1]], ['Milch mit den Haferflocken aufkochen.', 'Unter Rühren 2–3 Minuten köcheln, dann zugedeckt quellen lassen.', 'Mit Obst und etwas Süße essen.'], { fr: 1 }],
  ['griessbrei', 'Grießbrei mit Kirschen', 'warm', 'topf', 3, 0, 10, [['griess', 100], ['hmilch|hmilch15|frischmilch', 750], ['zucker', 30], ['kirschen|apfelmus|pfirsiche', 300, 1]], ['Milch mit Zucker aufkochen.', 'Grieß unter Rühren einrieseln lassen, kurz köcheln, vom Feuer nehmen und quellen lassen.', 'Mit Kirschen oder Apfelmus essen.'], { fr: 1 }],
  ['milchreis', 'Milchreis mit Apfelmus', 'warm', 'topf', 4, 0, 35, [['reis', 200], ['hmilch|hmilch15|frischmilch', 1000], ['zucker', 40], ['apfelmus|kirschen|pfirsiche', 300, 1]], ['Milch mit Reis und Zucker aufkochen.', 'Bei kleinster Flamme zugedeckt etwa 30 Minuten quellen lassen, ab und zu rühren.', 'Mit Apfelmus oder Kirschen essen.'], {}],
  ['pudding', 'Vanillepudding', 'warm', 'topf', 4, 0, 8, [['puddingpulver', 37], ['hmilch|hmilch15|frischmilch', 500], ['zucker', 40]], ['Pulver mit Zucker und etwas Milch glatt rühren.', 'Übrige Milch aufkochen, Pulver einrühren, kurz aufkochen lassen.', 'Abkühlen lassen.'], {}],
  ['ruehrei', 'Rührei mit Brot', 'warm', 'topf', 2, 0, 8, [['eier', 212], ['butter|margarine|rapsoel', 10], ['mischbrot|vkbrot|toast|broetchen', 200]], ['Eier verquirlen, salzen.', 'In der Pfanne mit Fett bei mittlerer Hitze stocken lassen, dabei schieben.', 'Mit Brot essen.'], { fr: 1 }],
  ['pfannkuchen', 'Pfannkuchen mit Apfelmus', 'warm', 'topf', 4, 0, 25, [['mehl405|dinkelmehl|vollkornmehl', 250], ['eier', 159], ['hmilch|hmilch15|frischmilch', 500], ['rapsoel|sonnenblumenoel|butterschmalz', 30], ['apfelmus|marmelade', 360, 1]], ['Mehl, Eier, Milch und eine Prise Salz zu einem glatten Teig rühren.', 'Pfanne mit wenig Öl erhitzen, dünne Pfannkuchen von beiden Seiten backen.', 'Mit Apfelmus oder Marmelade essen.'], {}],
  ['nudeln_tomate', 'Nudeln mit Tomatensoße', 'warm', 'topf', 4, 1200, 15, [['nudeln|nudeln_vk|eiernudeln', 400], ['passata|tomaten_dose', 500], ['zwiebeln', 50, 1], ['olivenoel|rapsoel', 15], ['hartkaese', 30, 1]], ['Nudeln wassersparend kochen: 1,2 l Wasser, Deckel drauf, oft rühren; ist das Wasser fast weg, sind sie meist gar.', 'Zwiebel in Öl andünsten, Tomaten dazu, salzen, 5 Minuten köcheln.', 'Soße über die Nudeln, Käse darüber.'], {}],
  ['bolognese', 'Nudeln Bolognese (Gefriergut zuerst)', 'warm', 'topf', 4, 1200, 25, [['hack_tk', 400], ['nudeln|nudeln_vk|eiernudeln', 400], ['passata|tomaten_dose', 500], ['zwiebeln', 80, 1], ['rapsoel', 10]], ['Hackfleisch auftauen lassen und vollständig durchbraten.', 'Zwiebel dazu, Tomaten angießen, 10 Minuten köcheln.', 'Nudeln wassersparend kochen und mit der Soße mischen.'], {}],
  ['jagdwurstnudeln', 'Nudeln mit Jagdwurst und Tomatensoße', 'warm', 'topf', 4, 2000, 30, [['nudeln|eiernudeln|nudeln_vk', 500], ['jagdwurst|wuerstchen|fruehstuecksfleisch', 150], ['zwiebeln', 100, 1], ['butter|margarine|rapsoel', 40], ['mehl405|dinkelmehl', 40], ['tomatenmark', 10], ['ketchup', 220], ['zucker', 5, 1]], ['Wurst und Zwiebel würfeln und anbraten.', 'Aus Butter und Mehl eine Mehlschwitze rühren, mit 0,5 l Wasser ablöschen, Tomatenmark und Ketchup einrühren.', 'Wurst in die Soße, Nudeln kochen und mischen. Ausführlich im Rezept der App.'], { rz: 'jagdwurstnudeln' }],
  ['reis_gemuese', 'Reis mit Erbsen und Möhren', 'warm', 'topf', 3, 500, 20, [['reis|reis_vk', 250], ['erbsen_moehren|erbsen_tk|gemuese_tk|mais', 280], ['bruehe', 8], ['butter|rapsoel|margarine', 15, 1]], ['Reis mit 500 ml Wasser und Brühpulver aufkochen.', 'Zugedeckt bei kleinster Flamme 15–20 Minuten quellen lassen.', 'Gemüse untermischen und heiß werden lassen.'], {}],
  ['thunfisch_reis', 'Reis mit Thunfisch und Tomaten', 'warm', 'topf', 3, 500, 20, [['reis', 250], ['thunfisch|lachs_dose|makrele', 150], ['tomaten_dose|passata', 400], ['zwiebeln', 50, 1], ['olivenoel|rapsoel', 15]], ['Reis mit 500 ml Wasser zugedeckt quellen lassen.', 'Zwiebel in Öl andünsten, Tomaten dazu, kurz köcheln.', 'Fisch zerpflücken, unterheben, mit dem Reis essen.'], {}],
  ['chili_reis', 'Chili con Carne mit Reis', 'warm', 'topf', 4, 400, 20, [['chili', 800], ['reis', 200]], ['Reis mit 400 ml Wasser zugedeckt quellen lassen.', 'Chili im Topf erhitzen und zum Reis essen.'], {}],
  ['haehnchen_reis', 'Hähnchen-Reis-Pfanne (Gefriergut zuerst)', 'warm', 'topf', 4, 500, 30, [['haehnchen_tk', 400], ['reis', 250], ['gemuese_tk|erbsen_tk|erbsen_moehren', 400], ['rapsoel', 20], ['bruehe', 6]], ['Hähnchen auftauen, klein schneiden und vollständig durchbraten.', 'Reis mit 500 ml Wasser und Brühe quellen lassen.', 'Gemüse zum Fleisch geben, alles mischen.'], {}],
  ['linseneintopf', 'Linseneintopf', 'warm', 'topf', 4, 1500, 35, [['linsen|rote_linsen', 250], ['kartoffeln', 300], ['moehren|erbsen_moehren', 150, 1], ['zwiebeln', 80, 1], ['bruehe', 10], ['essig', 15, 1], ['wuerstchen', 250, 1]], ['Zwiebel und Gemüse würfeln, mit Linsen, Kartoffelwürfeln und 1,5 l Wasser aufkochen.', 'Brühe dazu, zugedeckt etwa 30 Minuten köcheln.', 'Mit Essig abschmecken, Würstchen darin heiß werden lassen.'], {}],
  ['dal', 'Rote-Linsen-Dal mit Reis', 'warm', 'topf', 4, 1100, 25, [['rote_linsen', 200], ['reis', 200], ['tomaten_dose|passata', 400], ['zwiebeln', 80, 1], ['rapsoel', 15], ['bruehe', 6]], ['Zwiebel in Öl andünsten, Linsen, Tomaten, Brühe und 700 ml Wasser dazu.', 'Etwa 15 Minuten köcheln, bis die Linsen zerfallen.', 'Reis mit 400 ml Wasser zugedeckt quellen lassen und dazu essen.'], {}],
  ['erbsensuppe', 'Erbsensuppe aus Schälerbsen', 'warm', 'topf', 4, 1500, 60, [['erbsen_getr', 300], ['kartoffeln', 300], ['moehren', 150, 1], ['zwiebeln', 80, 1], ['bruehe', 10], ['wuerstchen|fruehstuecksfleisch', 250, 1]], ['Erbsen mit 1,5 l Wasser aufkochen, Schaum abschöpfen.', 'Zugedeckt etwa 45 Minuten köcheln, dann Kartoffel- und Gemüsewürfel dazu, weitere 15 Minuten.', 'Mit Brühe abschmecken, Würstchen darin erwärmen.'], {}],
  ['bohneneintopf', 'Weiße-Bohnen-Eintopf mit Tomaten', 'warm', 'topf', 4, 1800, 90, [['bohnen_getr', 300], ['tomaten_dose|passata', 400], ['kartoffeln', 300], ['zwiebeln', 80, 1], ['bruehe', 10], ['fruehstuecksfleisch|wuerstchen|corned_beef', 200, 1]], ['Bohnen über Nacht in reichlich Wasser einweichen, Einweichwasser weggießen.', 'Mit frischem Wasser etwa 60 Minuten weich kochen.', 'Tomaten, Kartoffeln, Zwiebel und Brühe dazu, weitere 25 Minuten köcheln.'], { hinweis: 'Getrocknete Bohnen immer gut durchkochen, nie roh essen.' }],
  ['kartoffeln_quark', 'Pellkartoffeln mit Quark', 'warm', 'topf', 4, 1000, 25, [['kartoffeln', 800], ['quark|joghurt', 500], ['leinsamen', 20, 1], ['zwiebeln', 50, 1]], ['Kartoffeln mit Schale in wenig Wasser zugedeckt etwa 20–25 Minuten garen.', 'Quark mit etwas Milch oder Wasser, Salz und Zwiebelwürfeln verrühren.', 'Kühlware zuerst verbrauchen.'], {}],
  ['bratkartoffeln', 'Bratkartoffeln mit Spiegelei', 'warm', 'topf', 3, 800, 35, [['kartoffeln', 700], ['eier', 159], ['rapsoel|schmalz|butterschmalz', 40], ['zwiebeln', 80, 1]], ['Kartoffeln kochen (am besten vom Vortag), pellen und in Scheiben schneiden.', 'In der Pfanne mit Fett und Zwiebeln knusprig braten.', 'Eier daneben in die Pfanne schlagen und braten.'], {}],
  ['pueree_wurst', 'Kartoffelpüree mit Würstchen', 'warm', 'topf', 3, 500, 10, [['pueree', 160], ['hmilch|hmilch15|frischmilch', 250], ['butter|margarine', 20, 1], ['wuerstchen|jagdwurst', 250]], ['Wasser und Milch erhitzen (nicht kochen), vom Feuer nehmen.', 'Flocken einrühren, kurz quellen lassen, Butter dazu.', 'Würstchen im heißen Wasser erwärmen.'], {}],
  ['sauerkraut_kartoffeln', 'Sauerkraut mit Kartoffeln und Würstchen', 'warm', 'topf', 4, 800, 25, [['sauerkraut', 770], ['kartoffeln', 800], ['wuerstchen|jagdwurst|fruehstuecksfleisch', 250]], ['Kartoffeln schälen und in Salzwasser garen.', 'Sauerkraut im Topf erhitzen, Würstchen darin erwärmen.'], {}],
  ['rotkohl_kartoffeln', 'Rotkohl mit Kartoffeln und Corned Beef', 'warm', 'topf', 4, 800, 25, [['rotkohl_glas', 680], ['kartoffeln', 800], ['corned_beef|fruehstuecksfleisch|wuerstchen', 340]], ['Kartoffeln garen.', 'Rotkohl erhitzen, Fleisch in Scheiben schneiden und kurz anbraten.', 'Frischer Rotkohl: siehe Rezept der App.'], { rz: 'rotkohl' }],
  ['soljanka', 'Soljanka', 'warm', 'topf', 4, 1000, 30, [['salami|jagdwurst|wuerstchen|fruehstuecksfleisch', 400], ['zwiebeln', 200], ['gurken', 180], ['tomatenmark', 40], ['bruehe', 15], ['rapsoel', 10]], ['Zwiebeln in Öl anbraten, Wurststreifen und Gurkenscheiben dazu.', 'Tomatenmark kurz mitrösten, mit 1 l Wasser und Brühe auffüllen.', 'Etwa 20 Minuten köcheln. Ausführlich im Rezept der App.'], { rz: 'soljanka' }],
  ['couscous_warm', 'Couscous mit Kichererbsen und Tomaten', 'warm', 'topf', 3, 300, 10, [['couscous', 250], ['kicher_dose|bohnen_dose', 240], ['tomaten_dose|passata', 400], ['bruehe', 8], ['olivenoel|rapsoel', 20]], ['300 ml Wasser mit Brühe aufkochen, über den Couscous gießen, zugedeckt 5 Minuten quellen lassen.', 'Tomaten und Kichererbsen im Topf erhitzen.', 'Mit Öl unter den Couscous mischen.'], {}],
  ['bulgur', 'Bulgur-Tomaten-Pfanne', 'warm', 'topf', 3, 400, 20, [['bulgur|hirse', 250], ['tomaten_dose|passata', 400], ['zwiebeln', 80, 1], ['rapsoel', 15], ['bruehe', 6]], ['Zwiebel in Öl andünsten, Bulgur kurz mitrösten.', 'Tomaten, 400 ml Wasser und Brühe dazu, zugedeckt 15 Minuten quellen lassen.'], {}],
  ['polenta', 'Polenta mit Tomatensoße und Käse', 'warm', 'topf', 4, 1000, 15, [['polenta', 250], ['passata|tomaten_dose', 500], ['hartkaese|gouda', 50, 1], ['bruehe', 8]], ['1 l Wasser mit Brühe aufkochen, Polenta einrühren.', 'Unter Rühren etwa 5–10 Minuten quellen lassen (Packung beachten).', 'Tomatensoße erhitzen, Käse darüber.'], {}],
  ['hirse_gemuese', 'Hirse mit Gemüse', 'warm', 'topf', 3, 600, 25, [['hirse', 250], ['gemuese_tk|erbsen_moehren|erbsen_tk', 400], ['bruehe', 8], ['butter|rapsoel', 15, 1]], ['Hirse heiß abspülen, mit 600 ml Wasser und Brühe aufkochen.', 'Zugedeckt 20 Minuten quellen lassen.', 'Gemüse untermischen und heiß werden lassen.'], {}],
  ['spinat_ei', 'Spinat mit Ei und Kartoffeln (Gefriergut zuerst)', 'warm', 'topf', 4, 1000, 25, [['spinat_tk', 450], ['eier', 212], ['kartoffeln', 800], ['butter|margarine', 20, 1]], ['Kartoffeln garen, Eier hart kochen (10 Minuten).', 'Spinat im Topf mit wenig Wasser auftauen und erhitzen.', 'Alles zusammen essen.'], {}],
  ['nudeln_oel', 'Nudeln mit Öl oder Butter (und Käse)', 'warm', 'topf', 4, 1200, 15, [['nudeln|nudeln_vk|eiernudeln', 400], ['olivenoel|rapsoel|butter|sonnenblumenoel', 40], ['hartkaese|gouda', 40, 1]], ['Nudeln wassersparend in 1,2 l Wasser mit Deckel garen.', 'Abgießen bzw. Restwasser verdampfen lassen, Öl oder Butter untermischen, salzen.', 'Mit geriebenem Käse essen.'], {}],
  ['brueh_reis', 'Brühreis', 'warm', 'topf', 3, 600, 20, [['reis|reis_vk', 250], ['bruehe', 8], ['butter|rapsoel|olivenoel', 20, 1]], ['Reis mit 600 ml Wasser und Brühpulver aufkochen.', 'Zugedeckt bei kleinster Flamme quellen lassen, etwas Fett unterrühren.'], {}],
  ['salzkartoffeln', 'Salzkartoffeln mit Butter', 'warm', 'topf', 4, 1000, 25, [['kartoffeln', 1000], ['butter|margarine|rapsoel', 30, 1]], ['Kartoffeln schälen, in wenig Salzwasser zugedeckt etwa 20 Minuten garen.', 'Abgießen, mit Butter oder einem Schuss Öl essen.'], {}],
  ['linsen_reis', 'Linsen mit Reis und Röstzwiebeln', 'warm', 'topf', 4, 1100, 35, [['linsen|rote_linsen', 200], ['reis', 200], ['rapsoel|olivenoel|sonnenblumenoel', 40], ['zwiebeln', 150, 1], ['bruehe', 6, 1]], ['Linsen in 700 ml Wasser etwa 15 Minuten vorkochen.', 'Reis und 400 ml Wasser dazu, zugedeckt 20 Minuten quellen lassen.', 'Zwiebeln in Öl braun rösten und darübergeben.'], {}],
  ['bohnen_reis', 'Bohnen mit Reis', 'warm', 'topf', 4, 400, 20, [['kidney_dose|bohnen_dose|kicher_dose|baked_beans', 500], ['reis', 200], ['rapsoel|olivenoel', 15], ['tomatenmark|passata', 40, 1]], ['Reis mit 400 ml Wasser zugedeckt quellen lassen.', 'Bohnen mit Öl und etwas Tomatenmark erhitzen, würzen.', 'Zum Reis essen.'], {}],
  ['porridge_wasser', 'Haferbrei mit Wasser und Obst', 'warm', 'topf', 1, 250, 5, [['haferflocken', 70], ['pfirsiche|apfelmus|rosinen|aepfel|bananen|kirschen|pflaumen_getr', 60], ['zucker|honig', 10, 1]], ['Haferflocken mit 250 ml Wasser und einer Prise Salz aufkochen.', '2–3 Minuten köcheln, Obst unterrühren, nach Geschmack süßen.'], { fr: 1 }],
  ['bohnensalat', 'Bohnensalat mit Zwiebeln', 'kalt', 'kalt', 2, 0, 10, [['kidney_dose|bohnen_dose|kicher_dose|gr_bohnen', 300], ['rapsoel|olivenoel|sonnenblumenoel', 20], ['zwiebeln', 50, 1], ['essig|zitronensaft', 15, 1]], ['Bohnen abtropfen lassen.', 'Mit Öl, Essig, Salz, Pfeffer und Zwiebelwürfeln mischen, kurz durchziehen lassen.'], {}],
  ['suppe_tuete', 'Instant-Suppe mit Zwieback', 'warm', 'topf', 2, 500, 5, [['suppe_tuete', 60], ['zwieback|knaecke|mischbrot', 60]], ['Suppenpulver nach Packung in 500 ml Wasser einrühren und aufkochen.', 'Zwieback dazu.'], {}],
  /* ---- Kochkiste: kurz ankochen, im geschlossenen Topf in einer gut isolierten Kiste ohne weitere Energie nachgaren (BZfE „Energie sparen mit der Kochkiste“, 03.01.2023).
     Belegte Zeiten nur für Erbsensuppe (15 min kochen, 2–3 h Kiste) und Milchreis (1 h Kiste); geeignet laut BZfE u. a. Reis, Hirse, Quinoa, Maisgrieß, Kartoffeln, Rotkohl, Hülsenfrüchte, Suppen, Gulasch.
     Flammzeit (z) sonst = geschätzte Zeit bis zum Aufkochen. ---- */
  ['kk_erbsen', 'Erbsensuppe aus der Kochkiste', 'kiste', 'topf', 4, 1500, 15, [['erbsen_getr', 300], ['kartoffeln', 300], ['moehren', 150, 1], ['zwiebeln', 80, 1], ['bruehe', 10]], ['Alles mit 1,5 l Wasser aufkochen und etwa 15 Minuten kochen.', 'Topf fest verschlossen in die Kochkiste stellen und 2 bis 3 Stunden ohne Flamme garen lassen.', 'Abschmecken; ist es noch nicht weich, kurz aufkochen und zurück in die Kiste.'], { beleg: 'kk-erbsen' }],
  ['kk_milchreis', 'Milchreis aus der Kochkiste', 'kiste', 'topf', 4, 0, 8, [['reis', 200], ['hmilch|hmilch15|frischmilch', 1000], ['zucker', 40], ['apfelmus|kirschen|pfirsiche', 300, 1]], ['Milch mit Zucker aufkochen, Reis einrühren und kurz aufkochen lassen.', 'Topf fest verschlossen etwa 1 Stunde in der Kochkiste garen.', 'Mit Apfelmus oder Kirschen essen.'], { beleg: 'kk-milchreis' }],
  ['kk_reis', 'Reis aus der Kochkiste', 'kiste', 'topf', 3, 500, 8, [['reis|reis_vk', 250], ['bruehe', 6, 1], ['butter|rapsoel', 15, 1]], ['Reis mit 500 ml Wasser und etwas Brühe aufkochen und kurz kochen lassen.', 'Fest verschlossen in die Kochkiste stellen und ohne Flamme fertig quellen lassen.', 'Vor dem Essen probieren; Garzeit in der Kiste ist länger als auf dem Herd.'], { beleg: 'kk-geeignet' }],
  ['kk_hirse', 'Hirse mit Gemüse aus der Kochkiste', 'kiste', 'topf', 3, 600, 8, [['hirse', 250], ['erbsen_moehren|gemuese_tk|mais', 280], ['bruehe', 8]], ['Hirse heiß abspülen, mit 600 ml Wasser und Brühe aufkochen.', 'Gemüse dazu, fest verschlossen in der Kochkiste nachgaren.', 'Mit der Gabel auflockern.'], { beleg: 'kk-geeignet' }],
  ['kk_quinoa', 'Quinoa-Bohnen-Topf aus der Kochkiste', 'kiste', 'topf', 3, 500, 8, [['quinoa', 200], ['kidney_dose|bohnen_dose|kicher_dose', 250], ['tomaten_dose|passata', 400], ['bruehe', 6]], ['Quinoa gründlich abspülen, mit 500 ml Wasser, Tomaten und Brühe aufkochen.', 'Bohnen dazu, fest verschlossen in die Kochkiste stellen und nachgaren.'], { beleg: 'kk-geeignet' }],
  ['kk_polenta', 'Polenta aus der Kochkiste', 'kiste', 'topf', 4, 1000, 8, [['polenta', 250], ['bruehe', 8], ['hartkaese|gouda', 50, 1]], ['1 l Wasser mit Brühe aufkochen, Maisgrieß unter Rühren einrieseln lassen und kurz aufkochen.', 'Fest verschlossen in der Kochkiste quellen lassen, danach durchrühren, Käse unterziehen.'], { beleg: 'kk-geeignet' }],
  ['kk_kartoffeln', 'Pellkartoffeln aus der Kochkiste', 'kiste', 'topf', 4, 1000, 10, [['kartoffeln', 1000], ['quark|joghurt|butter', 250, 1]], ['Kartoffeln mit Schale in wenig Wasser zugedeckt aufkochen und ein paar Minuten kochen.', 'Topf fest verschlossen in die Kochkiste stellen und garen lassen.', 'Mit einer Gabel prüfen, ob sie weich sind.'], { beleg: 'kk-geeignet' }],
  ['kk_rotkohl', 'Rotkohl mit Kartoffeln aus der Kochkiste', 'kiste', 'topf', 4, 600, 10, [['kohl|rotkohl_glas', 700], ['kartoffeln', 800], ['zwiebeln', 80, 1], ['essig|apfelmus', 30, 1]], ['Kohl fein schneiden (oder Glasware nehmen), mit gewürfelten Kartoffeln, etwas Wasser, Essig und Zwiebel aufkochen.', 'Fest verschlossen in der Kochkiste garen lassen.'], { beleg: 'kk-geeignet' }],
  ['kk_linsen', 'Linseneintopf aus der Kochkiste', 'kiste', 'topf', 4, 1500, 10, [['linsen|rote_linsen', 250], ['kartoffeln', 300], ['moehren|erbsen_moehren', 150, 1], ['bruehe', 10], ['essig', 15, 1]], ['Linsen, Kartoffel- und Gemüsewürfel mit 1,5 l Wasser und Brühe aufkochen und ein paar Minuten kochen.', 'Fest verschlossen in die Kochkiste stellen und nachgaren.', 'Mit Essig abschmecken.'], { beleg: 'kk-geeignet' }],
  ['kk_bohnen', 'Weiße-Bohnen-Eintopf aus der Kochkiste', 'kiste', 'topf', 4, 1800, 20, [['bohnen_getr', 300], ['tomaten_dose|passata', 400], ['kartoffeln', 300], ['bruehe', 10]], ['Bohnen über Nacht einweichen, Einweichwasser weggießen.', 'Mit frischem Wasser, Tomaten, Kartoffeln und Brühe aufkochen und gut durchkochen lassen.', 'Fest verschlossen in der Kochkiste weich garen; vor dem Essen noch einmal aufkochen.'], { beleg: 'kk-geeignet', hinweis: 'Getrocknete Bohnen immer gut durchkochen, nie roh oder halb gar essen.' }],
  ['kk_huehnersuppe', 'Hühnersuppe aus der Kochkiste (Gefriergut zuerst)', 'kiste', 'topf', 4, 1500, 15, [['haehnchen_tk', 400], ['moehren|erbsen_moehren|gemuese_tk', 250], ['nudeln|eiernudeln|reis', 150], ['bruehe', 10]], ['Hähnchen auftauen lassen, klein schneiden und mit Gemüse und 1,5 l Wasser aufkochen, bis das Fleisch durch ist.', 'Nudeln dazu, fest verschlossen in der Kochkiste nachgaren.'], { beleg: 'kk-geeignet' }],
  ['kk_gulasch', 'Gulasch mit Kartoffeln aus der Kochkiste', 'kiste', 'topf', 4, 800, 15, [['gulasch|chili', 800], ['kartoffeln', 800]], ['Kartoffeln würfeln, mit dem Gulasch und etwas Wasser aufkochen.', 'Fest verschlossen in der Kochkiste garen, bis die Kartoffeln weich sind.'], { beleg: 'kk-geeignet' }],
  /* ---- Brot ohne Backofen ---- */
  ['pfannenbrot', 'Pfannenbrot mit Hefe', 'brot', 'topf', 6, 300, 30, [['mehl405|dinkelmehl|vollkornmehl', 500], ['trockenhefe|frischhefe*3', 7], ['rapsoel|olivenoel', 30], ['zucker', 5, 1]], ['Mehl, Hefe, 1½ TL Salz, Öl und 300 ml lauwarmes Wasser zu einem weichen Teig kneten.', 'Zugedeckt 45–60 Minuten gehen lassen.', 'In 6 Stücke teilen, flach drücken und in der Pfanne mit Deckel bei kleiner Hitze je Seite 5–7 Minuten backen.'], {}],
  ['fladen_backpulver', 'Schnelle Fladen ohne Hefe', 'brot', 'topf', 4, 0, 15, [['mehl405|dinkelmehl|vollkornmehl', 300], ['backpulver', 10], ['joghurt|hmilch|frischmilch|quark', 200], ['rapsoel|olivenoel', 20]], ['Mehl, Backpulver und eine Prise Salz mischen, Joghurt und Öl unterkneten.', 'In 4 Teile teilen, dünn ausrollen.', 'In der heißen Pfanne ohne Fett je Seite 2–3 Minuten backen.'], {}],
  ['chapati', 'Wasser-Fladen (wie Chapati)', 'brot', 'topf', 4, 180, 20, [['vollkornmehl|mehl405|dinkelmehl', 300], ['rapsoel|olivenoel', 10, 1]], ['Mehl, ½ TL Salz und 180 ml Wasser zu einem glatten Teig kneten, 15 Minuten ruhen lassen.', 'In 8 Kugeln teilen, sehr dünn ausrollen.', 'In der trockenen, heißen Pfanne je Seite etwa 1 Minute backen.'], {}],
  ['stockbrot', 'Stockbrot', 'brot', 'glut', 6, 250, 15, [['mehl405|dinkelmehl', 500], ['trockenhefe|frischhefe*3', 7], ['rapsoel|olivenoel', 40], ['zucker', 10, 1]], ['Mehl, Hefe, 1½ TL Salz, Zucker, Öl und 250 ml lauwarmes Wasser zu einem festen Teig kneten, 30 Minuten gehen lassen.', 'Teigstränge um geschälte Stöcke wickeln.', 'Über der Glut (nicht in die Flammen) unter Drehen 10–15 Minuten backen.'], {}],
  ['topfbrot_glut', 'Topfbrot in der Glut', 'brot', 'glut', 10, 380, 50, [['mehl405|dinkelmehl', 500], ['roggenmehl|vollkornmehl', 100, 1], ['trockenhefe|frischhefe*3', 7]], ['Mehl, Hefe, 2 TL Salz und 380 ml lauwarmes Wasser zu einem weichen Teig rühren, 1–2 Stunden gehen lassen.', 'In einen gefetteten gusseisernen Topf mit Deckel geben.', 'Topf in die Glut stellen, auch Glut auf den Deckel legen; etwa 40–50 Minuten backen. Klopfprobe: hohl = fertig.'], {}],
  /* ---- Backofen / Holzofen mit Backfach ---- */
  ['dinkeltopf', 'Dinkel-Joghurt-Brot aus dem Topf', 'ofen', 'ofen', 10, 350, 60, [['dinkelmehl|mehl405', 600], ['roggenmehl|dinkelmehl', 100], ['trockenhefe|frischhefe*3', 7], ['joghurt', 150], ['zucker', 5, 1]], ['Hefe in 350 ml lauwarmem Wasser lösen, mit Mehl, Joghurt und Salz gründlich kneten.', 'Eine Stunde gehen lassen, in einen Topf mit Deckel geben.', 'Bei 180 °C etwa 50 Minuten backen, dann ohne Deckel bräunen. Ausführlich im Rezept der App.'], { rz: 'dinkeltopf' }],
  ['dinkelvollkorn', 'Dinkel-Vollkornbrot mit Saaten', 'ofen', 'ofen', 12, 500, 60, [['dinkelmehl|vollkornmehl', 500], ['sonnenblumenkerne|kuerbiskerne', 100], ['leinsamen', 25, 1], ['essig', 30, 1], ['trockenhefe|frischhefe*3', 14]], ['Alle Zutaten mit 500 ml lauwarmem Wasser verrühren und in eine gefettete Kastenform füllen.', 'In den kalten Ofen, bei 200 °C etwa 60 Minuten backen.', 'Ausführlich im Rezept der App.'], { rz: 'dinkelvollkorn' }],
  ['zwiebelbrot', 'Zwiebelbrot ohne Sauerteig', 'ofen', 'ofen', 10, 300, 45, [['mehl405|dinkelmehl', 500], ['trockenhefe|frischhefe*3', 7], ['rapsoel|sonnenblumenoel', 45], ['zwiebeln', 200]], ['Zwiebeln in Öl glasig braten und abkühlen lassen.', 'Mehl, Hefe, Salz, Öl und 300 ml lauwarmes Wasser kneten, Zwiebeln unterkneten, gehen lassen.', 'In der Kastenform backen. Ausführlich im Rezept der App.'], { rz: 'zwiebelbrot' }],
  ['roggenvollkorn', 'Roggen-Vollkornbrot mit Kernen', 'ofen', 'ofen', 12, 450, 60, [['roggenvollkornmehl|roggenmehl', 350], ['vollkornmehl|dinkelmehl', 150], ['trockenhefe|frischhefe*3', 7], ['honig|zucker', 7, 1], ['sonnenblumenkerne|kuerbiskerne', 40, 1], ['leinsamen', 20, 1]], ['Mehle, Hefe und Salz mischen, Honig und 450 ml lauwarmes Wasser zu einem klebrigen Teig rühren, Kerne dazu.', 'Eine Stunde gehen lassen, in die gefettete Kastenform füllen.', 'Backen und gut auskühlen lassen. Ausführlich im Rezept der App.'], { rz: 'roggenvollkorn' }],
  ['kartoffelbrot', 'Kartoffelbrot', 'ofen', 'ofen', 10, 600, 60, [['kartoffeln', 400], ['mehl405|dinkelmehl', 500], ['trockenhefe|frischhefe*3', 7]], ['Kartoffeln kochen, pellen und zerdrücken.', 'Mit Mehl, Hefe, Salz und 100 ml lauwarmem Wasser kneten, 1 Stunde gehen lassen.', 'In der Kastenform backen. Ausführlich im Rezept der App.'], { rz: 'kartoffelbrot' }],
  ['nudelauflauf', 'Nudelauflauf mit Käse und Gemüse', 'ofen', 'ofen', 4, 800, 45, [['nudeln|eiernudeln|nudeln_vk', 300], ['hmilch|hmilch15|frischmilch', 400], ['eier', 106], ['hartkaese|gouda', 100], ['erbsen_moehren|mais|erbsen_tk|gemuese_tk', 280]], ['Nudeln bissfest vorkochen.', 'Mit Gemüse in eine Form geben, Milch und Eier verquirlt darübergießen, Käse obendrauf.', 'Bei etwa 180 °C 25–30 Minuten backen.'], {}],
  ['ofenkartoffeln', 'Ofenkartoffeln mit Quark', 'ofen', 'ofen', 4, 0, 45, [['kartoffeln', 1000], ['rapsoel|olivenoel', 30], ['quark|joghurt', 500, 1]], ['Kartoffeln gründlich waschen, halbieren, mit Öl und Salz mischen.', 'Mit der Schnittfläche nach unten bei etwa 200 °C 35–45 Minuten backen.', 'Mit Quark essen.'], {}],
  ['haferkekse', 'Haferflocken-Kekse', 'ofen', 'ofen', 6, 0, 15, [['haferflocken', 200], ['mehl405|dinkelmehl|vollkornmehl', 100], ['zucker|honig', 80], ['butter|margarine', 100], ['eier', 53], ['backpulver', 5, 1]], ['Butter schmelzen, mit Zucker und Ei verrühren.', 'Haferflocken, Mehl und Backpulver unterrühren, kleine Häufchen aufs Blech setzen.', 'Bei 180 °C etwa 12–15 Minuten backen.'], {}],
  ['ruehrkuchen', 'Einfacher Rührkuchen', 'ofen', 'ofen', 12, 0, 50, [['mehl405|dinkelmehl', 300], ['zucker', 150], ['eier', 212], ['rapsoel|sonnenblumenoel|butter', 150], ['hmilch|hmilch15|frischmilch', 125], ['backpulver', 15]], ['Eier mit Zucker schaumig rühren, Öl und Milch dazu.', 'Mehl mit Backpulver unterrühren, in eine gefettete Form füllen.', 'Bei 175 °C etwa 45–50 Minuten backen (Stäbchenprobe).'], {}]
];
function zutatLesen(z) { return { a: z[0].split('|').map(function (s) { var m = s.split('*'); return [m[0], m[1] ? +m[1] : 1]; }), g: z[1], opt: !!z[2] }; }
var GERICHTE = GERICHTE_ROH.map(function (r) { return { id: r[0], n: r[1], art: r[2], koch: r[3], p: r[4], wa: r[5], z: r[6], zut: r[7].map(zutatLesen), sch: r[8], rz: r[9].rz, fr: !!r[9].fr, hinweis: r[9].hinweis || '', beleg: r[9].beleg || '' }; });
var ARTEN = [['alle', 'Alle'], ['kalt', 'Ohne Kochen'], ['warm', 'Topf & Pfanne'], ['kiste', 'Kochkiste'], ['brot', 'Brot ohne Ofen'], ['ofen', 'Backofen']];

/* Abhak-Liste nach den Checklisten des BBK-Ratgebers (Stand 11/2025) – alles außer Essen und Trinken */
var CHECK = [
  ['Information', ['Radio mit Batterie, Solar oder Kurbel (mit Ersatzbatterien)', 'Warn-App auf dem Handy (z. B. NINA)', 'Aufgeladene Powerbank', 'Wichtige Telefonnummern auf Papier']],
  ['Licht und Wärme', ['Taschenlampe und Ersatzbatterien', 'Kerzen und Feuerzeug oder Streichhölzer', 'Kochgelegenheit ohne Strom (z. B. Campingkocher, Gasgrill)', 'Brennstoff für die Kochgelegenheit (z. B. Gaskartuschen)', 'Warme Kleidung, Decken, Schlafsäcke', 'Heizgelegenheit ohne Strom, für Innenräume zugelassen', 'Brennstoff für die Heizgelegenheit']],
  ['Hausapotheke', ['Persönliche Medikamente (Vorrat für mindestens 10 Tage)', 'Schmerzmittel und fiebersenkende Mittel', 'Fieberthermometer', 'Wund- und Hautdesinfektion', 'Pflaster und Verbandmaterial', 'Mittel gegen Durchfall, Übelkeit, Erbrechen', 'Elektrolyte gegen Flüssigkeitsverlust', 'Einmalhandschuhe, Pinzette, Schere']],
  ['Hygiene', ['Zahnbürsten und Zahnpasta', 'Seife', 'Toilettenpapier', 'Persönliche Hygieneartikel (Monatshygiene, Windeln)', 'Stabile Müllbeutel (auch für die Toilette) oder Campingtoilette', 'Desinfektionsmittel', 'Feuchttücher und Haushaltspapier', 'Haushaltshandschuhe']],
  ['Brandschutz', ['Rauchmelder', 'Feuerlöscher oder Feuerlöschspray', 'Kohlenmonoxid-Melder (bei Gas, Holz, Kohle im Haus)']],
  ['Sonstiges', ['Bargeld in kleinen Scheinen', 'Mappe mit wichtigen Dokumenten', 'Behälter für Brauchwasser (z. B. Kanister, Eimer)', 'Dosenöffner und Taschenmesser', 'Futtervorrat für Haustiere', 'Ersatz für Brille oder Hörgerät-Batterien', 'Atemschutzmasken (FFP2)']]
];
/* Übliche Haltbarkeit (BLE „So können Lebensmittel gelagert werden“) */
var HALTB = [
  ['Gemüsekonserven', '1–2 Jahre', 'trocken, luftig, möglichst unter 20 °C'], ['Obstkonserven, Marmelade', 'etwa 1 Jahr', 'trocken, luftig, unter 20 °C'], ['Fisch- und Fleischkonserven', 'mehrere Jahre', 'kühl und trocken, MHD beachten'],
  ['Trockenobst und -gemüse', 'etwa 1 Jahr', 'trocken, dunkel, in Glas oder Dose'], ['Kartoffelflocken', '1–2 Jahre', 'trocken, unter 20 °C'], ['Grieß, Haferflocken, Reis, Nudeln, Stärke', 'etwa 1 Jahr', 'dicht verschlossen und trocken'],
  ['Getreide, ganzes Korn', '2 Jahre', 'trocken, ab und zu lüften'], ['Knäckebrot, Zwieback', 'etwa 1 Jahr', 'MHD beachten'], ['Vollkornbrot (frisch)', '10–12 Tage', 'Brotkasten oder Steintopf'],
  ['Speiseöl, ungeöffnet', '6–12 Monate', 'dunkel, bis 20 °C'], ['Butter, Margarine', '4–6 Wochen', 'Kühlschrank'], ['Kartoffeln (größere Menge)', '6–8 Monate', 'dunkel, luftig, 5–10 °C'],
  ['Äpfel', '3–5 Monate', 'kühl, dunkel, feucht'], ['Zucker, Salz, Tee', 'praktisch unbegrenzt', 'trocken'], ['Tiefkühl: Gemüse / Obst', '6–12 / 8–12 Monate', 'mindestens −18 °C'], ['Tiefkühl: Fleisch / Brot', '3–12 / 1–3 Monate', 'mindestens −18 °C']
];
var QUELLEN = [
  ['BBK: Ratgeber „Vorsorgen für Krisen und Katastrophen“, 2. Auflage, Stand 11/2025 (PDF)', 'https://www.bbk.bund.de/SharedDocs/Downloads/DE/Mediathek/Publikationen/Buergerinformationen/Ratgeber/BBK-Vorsorgen-fuer-Krisen-und-Katastrophen.pdf?__blob=publicationFile&v=39', '10 Tage, mindestens 3 Tage; 2 l Wasser je Person und Tag, davon 0,5 l zum Kochen; Kochen ohne Strom; Hausapotheke'],
  ['BBK: Essen und Trinken bevorraten', 'https://www.bbk.bund.de/DE/Warnung-Vorsorge/Vorsorge/So-koennen-Sie-sich-vorbereiten/Bevorraten/bevorraten_node.html', 'haltbar, fertig, kurze Kochzeit'],
  ['BBK: Checklisten zur Vorsorge (PDF)', 'https://www.bbk.bund.de/SharedDocs/Downloads/DE/Mediathek/Publikationen/Buergerinformationen/Ratgeber/Checklisten-zur-Vorsorge-Krisen-und-Katastrophen.pdf?__blob=publicationFile&v=19', 'Abhak-Liste „Fehlt noch“'],
  ['BLE: Vorratstabelle Mischkost (ernaehrungsvorsorge.de, © BLE 2024, PDF)', 'https://www.ernaehrungsvorsorge.de/fileadmin/SITE_MASTER/content/Dokumente/Anhang_3.1_Vorratstabelle_Mischkost_-_DIN_A4.pdf', 'Mengen je Gruppe für 1 Person, 10 Tage, 2.200 kcal; Energiewerte nach BLS 3.02'],
  ['BLE: Vorratstabelle und Vorratskalkulator', 'https://www.ernaehrungsvorsorge.de/private-vorsorge/notvorrat/vorratstabelle', 'Erläuterungen, vegetarische Fassung'],
  ['BLE: So können Lebensmittel gelagert werden', 'https://www.ernaehrungsvorsorge.de/private-vorsorge/empfehlungen-tipps/so-koennen-lebensmittel-gelagert-werden', 'übliche Haltbarkeiten'],
  ['Verbraucherzentrale Niedersachsen: Verpflegung bei Stromausfall (Stand 04.08.2026)', 'https://www.verbraucherzentrale-niedersachsen.de/wissen/lebensmittel/auswaehlen-zubereiten-aufbewahren/verpflegung-bei-stromausfall-vorraete-sichern-tiefkuehlkost-retten-und-ohne-strom-kochen-124714', 'Kühlschrank 4–6 Stunden, Gefriergerät oft bis 48 Stunden, BfR zu −12 °C'],
  ['Verbraucherzentrale Niedersachsen: Trinkwasservorrat (Stand 24.09.2026)', 'https://www.verbraucherzentrale-niedersachsen.de/wissen/lebensmittel/auswaehlen-zubereiten-aufbewahren/trinkwasservorrat-so-sichern-sie-die-versorgung-im-haushalt-125990', 'Wasser lagern, Glas und PET, Säuglingsnahrung'],
  ['DGE: Referenzwerte Energie (Richtwerte, Ableitung 2015)', 'https://www.dge.de/wissenschaft/referenzwerte/energie/', 'Kinder und Jugendliche; PAL 1,4 · 1,6 · 1,8'],
  ['DGE: Referenzwerte Protein (Ableitung 2017)', 'https://www.dge.de/wissenschaft/referenzwerte/protein/', 'g Eiweiß je kg Körpergewicht'],
  ['Mifflin et al. (1990): Gleichung für den Ruheumsatz (PubMed)', 'https://pubmed.ncbi.nlm.nih.gov/2305711/', 'Erwachsene, wie im Energie-Rechner der App'],
  ['Verbraucherzentrale: MHD ist nicht gleich Verbrauchsdatum (Stand 02.10.2025)', 'https://www.verbraucherzentrale.de/wissen/lebensmittel/auswaehlen-zubereiten-aufbewahren/mindesthaltbarkeitsdatum-mhd-ist-nicht-gleich-verbrauchsdatum-13452', ''],
  ['BZfE: Lebensmittelverderb erkennen (Stand 20.02.2025)', 'https://www.bzfe.de/nachhaltiger-konsum/lagern-kochen-essen-teilen/lebensmittelverderb-erkennen/', 'Warnzeichen'],
  ['BZfE: Lagerung – neue Vorräte nach hinten (Stand 13.08.2026)', 'https://www.bzfe.de/einfache-sprache/kochen-und-aufbewahren/lagerung', 'zuerst rein, zuerst raus'],
  ['BZfE: Private Ernährungsvorsorge (Stand 09.06.2026)', 'https://www.bzfe.de/kueche-und-alltag/private-ernaehrungsvorsorge', '„first in, first out“'],
  ['USDA FoodData Central, SR Legacy (2018)', 'https://fdc.nal.usda.gov/', 'Nährwerte je 100 g (Nummer im Katalog)']
];

/* ===================================================================== 3. Rechenkern (ohne DOM) */
function katVon(S, id) { if (KAT[id]) return KAT[id]; var e = (S.eigene || []).filter(function (x) { return x.i === id; })[0]; return e || null; }
function einheiten(k) {
  var L = k.ml ? [{ k: 'ml', t: 'ml', g: 1 }, { k: 'l', t: 'l', g: 1000 }] : [{ k: 'g', t: 'g', g: 1 }, { k: 'kg', t: 'kg', g: 1000 }];
  if (k.st) L.push({ k: 'st', t: 'Stück (ca. ' + fz(k.st) + ' g)', g: k.st });
  (k.p || []).forEach(function (p, i) { L.push({ k: 'p' + i, t: p[0], g: p[1] }); });
  return L;
}
function einheitG(k, e) { var L = einheiten(k); for (var i = 0; i < L.length; i++) if (L[i].k === e) return L[i].g; return 1; }
function einheitT(k, e) { var L = einheiten(k); for (var i = 0; i < L.length; i++) if (L[i].k === e) return L[i].t; return 'g'; }
function stdEinheit(k) { return k.p && k.p.length ? 'p0' : k.st ? 'st' : k.ml ? 'l' : 'g'; }
function gramm(S, it) { var k = katVon(S, it.k); if (!k) return 0; return Math.max(0, (+it.m || 0) * einheitG(k, it.e)); }

/* Tagesbedarf einer Person: Erwachsene (ab 18) nach Mifflin-St Jeor × PAL, Kinder/Jugendliche nach DGE-Richtwerten */
function bedarf(p) {
  var a = zahl(p.a), m = p.s !== 'w', ti = 0;
  TAETIG.forEach(function (t, i) { if (t[0] === p.t) ti = i; }); if (!p.t) ti = 1;
  var pal = TAETIG[ti][2], eig = zahl(p.eigen), kgw = zahl(p.kg), cm = zahl(p.cm), r = { kcal: 0, eiweiss: 0, art: '', text: '' };
  if (!isFinite(a)) { r.art = 'fehlt'; r.text = 'Alter eingeben'; }
  else if (a < 1) { r.art = 'baby'; r.text = 'Säugling: Bedarf von Hand eintragen (Kinderarzt, Packung der Säuglingsnahrung)'; }
  else {
    var row = null; DGE_E.forEach(function (d) { if (a >= d[0] && a < d[1]) row = d; });
    var refKg = row ? (m ? row[4] : row[5]) : 70;
    var kgE = isFinite(kgw) && kgw > 0 ? kgw : refKg;
    if (a >= 18 && isFinite(kgw) && kgw >= 30 && isFinite(cm) && cm >= 120) {
      var gu = 10 * kgw + 6.25 * cm - 5 * a + (m ? 5 : -161);
      r.kcal = gu * pal; r.art = 'formel'; r.text = 'Grundumsatz ' + fz(gu) + ' kcal × ' + fz(pal, 1) + ' (Mifflin-St Jeor)';
    } else if (row) {
      r.kcal = (m ? row[2] : row[3])[ti]; r.art = 'dge'; r.text = 'DGE-Richtwert für ' + row[0] + ' bis unter ' + (row[1] > 100 ? '…' : row[1]) + ' Jahre' + (row[0] === 1 ? '' : ', PAL ' + fz(pal, 1));
    }
    r.eiweiss = eiweissProKg(a, p.s) * kgE;
  }
  if (isFinite(eig) && eig > 0) { r.kcal = eig; r.text = 'eigener Wert' + (r.text ? ' (berechnet: ' + r.text + ')' : ''); r.art = 'eigen'; }
  return r;
}
function haushalt(S) {
  var P = (S.personen || []).map(function (p) { return { p: p, b: bedarf(p) }; });
  var kcal = 0, eiw = 0; P.forEach(function (x) { kcal += x.b.kcal; eiw += x.b.eiweiss; });
  var n = P.length, L = S.lage || {}, hyg = Math.max(0, zahl(L.hyg) || 0);
  var tiereW = 0; (S.tiere || []).forEach(function (t) { tiereW += Math.max(0, zahl(t.wasser) || 0); });
  var wasser = n * (WASSER_TAG + hyg) + tiereW;
  var spar = [100, 80, 60].indexOf(+L.spar) >= 0 ? +L.spar : 100;
  return { P: P, n: n, kcal: kcal, kcalSpar: kcal * spar / 100, spar: spar, eiweiss: eiw, wasser: wasser, wasserKochen: n * WASSER_KOCHEN, tiereW: tiereW, hyg: hyg };
}
function zielTage(S) { var L = S.lage || {}; var z = L.ziel === 'frei' ? zahl(L.zielFrei) : +L.ziel; return isFinite(z) && z > 0 ? Math.min(365, Math.round(z)) : 10; }
function kannKochen(S, need) { var k = (S.lage || {}).koch || 'gas'; return (KANN[need] || []).indexOf(k) >= 0; }

/* Lagerposten mit Werten */
function posten(S, heute) {
  return (S.lager || []).map(function (it) {
    var k = katVon(S, it.k); if (!k) return null;
    var g = gramm(S, it), d = mhdDatum(it.mhd);
    return { it: it, k: k, g: g, kcal: g * (k.k || 0) / 100, eiw: g * (k.e || 0) / 100, ort: ortTyp(S, it.o), ortId: it.o || 'v', mhd: d, rest: d ? tageBis(d, heute) : null, ko: !!k.ko };
  }).filter(Boolean);
}
/* Reihenfolge beim Essen: Kühlschrank, Gefriertruhe, dann was zuerst abläuft */
function rang(x, strom) { var r = 0; if (strom) r = x.ort === 'k' ? 0 : x.ort === 't' ? 1 : 2; return r * 1e6 + (x.rest == null ? 9e5 : Math.max(-1e4, Math.min(8e5, x.rest))); }

/* Fett, Zucker, Mehl und andere Zutaten zählen je Tag höchstens mit 30 % des Bedarfs (Annahme: so viel lässt sich sinnvoll verkochen;
   die DGE nennt für Fett 30–35 % der Energie). Sonst würde z. B. eine Flasche Öl allein mehrere Tage „füllen“. */
var ZUTAT_ANTEIL = 0.3;
function begrenzt(k) { return k.g === 'fett' || ['zucker', 'honig', 'marmelade', 'nusscreme', 'mayonnaise', 'ketchup', 'bruehe', 'kakao', 'puddingpulver', 'butterschmalz'].indexOf(k.i) >= 0; }
/* Reichweite: Tag für Tag essen. Bei Stromausfall zählt Kühlschrank-Ware nur am 1. Tag, Gefriergut nur an den Tagen 1–2 (VZ: Kühlschrank 4–6 h, Gefriergerät oft bis 48 h) */
function reichweite(S, heute, opt) {
  opt = opt || {}; var H = haushalt(S), D = H.kcalSpar, L = S.lage || {}, strom = !!L.strom, kochen = opt.ohneKochen ? false : ((L.koch || 'gas') !== 'keine');
  var X = posten(S, heute).filter(function (x) { return x.k.g !== 'baby' && x.kcal > 0; });
  X.forEach(function (x) { x.r = x.kcal; x.e = x.eiw; x.pur = !begrenzt(x.k); });
  X.sort(function (a, b) { return rang(a, strom) - rang(b, strom); });
  var nutzbar = function (x, d) { if (x.ko && !kochen) return false; if (strom && x.ort === 'k' && d > 1) return false; if (strom && x.ort === 't' && d > 2) return false; return true; };
  var start = 0; X.forEach(function (x) { if (nutzbar(x, 1)) start += x.r; });
  var verlauf = [[0, D > 0 ? start / D : 0]], tage = 0, verloren = 0, spaet = [], d = 0, MAX = 730;
  if (D <= 0) return { D: 0, tage: 0, verlauf: [], start: start, verloren: 0, spaet: [], max: false };
  while (d < MAX) {
    d++; var need = D, zut = D * ZUTAT_ANTEIL;
    for (var i = 0; i < X.length && need > 1e-9; i++) { var x = X[i]; if (x.r <= 1e-9 || !nutzbar(x, d)) continue;
      var t = Math.min(x.r, need); if (!x.pur) { t = Math.min(t, zut); if (t <= 1e-9) continue; zut -= t; } if (x.rest != null && x.rest < d - 1 && spaet.indexOf(x) < 0) spaet.push(x); x.r -= t; need -= t; }
    var rest = 0; X.forEach(function (x) { if (x.r > 1e-9 && nutzbar(x, d + 1)) rest += x.r; });
    if (need > 1e-9) { tage += (D - need) / D; verlauf.push([d, 0]); break; }
    tage += 1; verlauf.push([d, rest / D]);
    if (rest <= 1e-9) break;
  }
  X.forEach(function (x) { if (x.r > 1e-9 && strom && (x.ort === 'k' || x.ort === 't')) verloren += x.r; });
  return { D: D, tage: tage, verlauf: verlauf, start: start, verloren: verloren, spaet: spaet.map(function (x) { return x.it.u; }), max: d >= MAX };
}
/* Notquellen (S.wasserQ.q, Liter): Spülkasten, Warmwasserspeicher, Regen nur abgekocht trinkbar (CDC/UBA, siehe Bereich „Wasser“);
   Eiswürfel aus einwandfreiem Wasser direkt; Badewanne und Pool nur als Brauchwasser (Toilette, Körperpflege) */
var WQ = [['wanne', 'Badewanne', 'brauch'], ['boiler', 'Warmwasserspeicher (Trinkwasseranlage)', 'abkochen'], ['spuelkasten', 'Spülkasten (klar, ohne Reiniger)', 'abkochen'], ['eis', 'Eiswürfel aus Trinkwasser', 'trink'], ['regen', 'Regenwasser', 'abkochen'], ['pool', 'Pool', 'brauch']];
function notquellen(S) {
  var W = S.wasserQ || {}, q = W.q || {}, r = { trink: 0, abkochen: 0, brauch: 0 };
  WQ.forEach(function (x) { var l = zahl(q[x[0]]); if (isFinite(l) && l > 0) r[x[2]] += l; });
  return r;
}
function wasser(S) {
  var H = haushalt(S), L = S.lage || {}, l = 0, Wq = S.wasserQ || {}, nq = notquellen(S), kochen = (L.koch || 'gas') !== 'keine';
  (S.lager || []).forEach(function (it) { var k = katVon(S, it.k); if (k && k.fl) l += gramm(S, it) / 1000; });
  var vorrat = l, dazu = nq.trink + (Wq.abkochen && kochen ? nq.abkochen : 0); l += dazu;
  var tage = L.leitung ? Infinity : (H.wasser > 0 ? l / H.wasser : 0);
  /* Brauchwasser: Körperpflege und Toilette (nur wenn eingestellt) */
  var n = H.n, brauchBedarf = n * ((Wq.pflege ? zahl(Wq.pflegeL) || 0 : 0) + (Wq.toilette === 'spuelen' ? zahl(Wq.toiletteL) || 0 : 0));
  var brauch = nq.brauch + (Wq.abkochen && kochen ? 0 : nq.abkochen);
  return { l: l, vorrat: vorrat, notquellen: dazu, bedarf: H.wasser, tage: tage, leitung: !!L.leitung, brauch: brauch, brauchBedarf: brauchBedarf, brauchTage: L.leitung ? Infinity : brauchBedarf > 0 ? brauch / brauchBedarf : null };
}
function gruppenStand(S, heute) {
  var H = haushalt(S), z = zielTage(S), fak = H.kcal / BLE_KCAL * z / BLE_TAGE, R = {};
  GRUPPEN.forEach(function (g) { R[g.k] = { g: g, ist: 0, ziel: g.ble * fak, kcal: 0 }; });
  posten(S, heute).forEach(function (x) { var r = R[x.k.g]; if (!r) return; r.ist += x.g * (x.k.x || 1); r.kcal += x.kcal; });
  return R;
}
function eiweissTage(S, heute) { var H = haushalt(S), e = 0; posten(S, heute).forEach(function (x) { if (x.k.g !== 'baby') e += x.eiw; }); return { g: e, tage: H.eiweiss > 0 ? e / H.eiweiss : 0, bedarf: H.eiweiss }; }

/* Gerichte gegen das Lager prüfen */
function bestand(S, heute) { var B = {}; posten(S, heute).forEach(function (x) { B[x.it.k] = (B[x.it.k] || 0) + x.g; }); return B; }
function zutatDa(z, B) { var s = 0; z.a.forEach(function (a) { s += (B[a[0]] || 0) / a[1]; }); return s; }
function gerichtWerte(S, r) {
  var k = 0, e = 0; r.zut.forEach(function (z) { if (z.opt) return; var kk = katVon(S, z.a[0][0]); if (!kk) return; k += z.g * (kk.k || 0) / 100; e += z.g * (kk.e || 0) / 100; });
  return { kcal: k / r.p, eiweiss: e / r.p, wasser: r.wa / r.p };
}
function gerichtStatus(S, r, B) {
  var max = Infinity, fehlt = [];
  r.zut.forEach(function (z) { if (z.opt) return; var je = z.g / r.p, da = zutatDa(z, B), n = da / je; if (n < max) max = n;
    if (n < 1 - 1e-9) fehlt.push({ z: z, g: je - da }); });
  if (!isFinite(max)) max = 0;
  max = Math.floor(max * 10 + 1e-6) / 10;
  var st = max >= 1 ? 'geht' : fehlt.length <= 2 ? 'fast' : 'fehlt';
  return { st: st, max: max, fehlt: fehlt, koch: kannKochen(S, r.koch) };
}
/* Portionen nach Bedarf: 1 Portion = eine Mahlzeit für jemanden mit 2.200 kcal Tagesbedarf (Bezugswert der BLE-Tabelle).
   Ein Kind mit 1.500 kcal bekommt 0,7 Portionen, ein Erwachsener mit 2.800 kcal 1,3. */
var PORTION_KCAL = 2200;
function portionenHaushalt(S) { var H = haushalt(S); return Math.round(H.kcalSpar / PORTION_KCAL * 10) / 10; }
function portText(p) { return fz(p, 1) + (Math.abs(p - 1) < 1e-9 ? ' Portion' : ' Portionen'); }
function zutatName(S, z) { return z.a.map(function (a) { var k = katVon(S, a[0]); return k ? k.n.replace(/ \(.*\)$/, '').replace(/, trocken$/, '') : a[0]; }).filter(function (v, i, A) { return A.indexOf(v) === i; }).slice(0, 3).join(' oder '); }

/* Zutaten abziehen: zuerst Kühlschrank/Gefriertruhe, dann was zuerst abläuft. Gibt verbrauchte Mengen zurück */
function abziehen(S, r, port, heute) {
  var strom = !!(S.lage || {}).strom, X = posten(S, heute), weg = [];
  r.zut.forEach(function (z) {
    var need = z.g / r.p * port; if (z.opt && zutatDa(z, bestand(S, heute)) <= 0) return;
    var C = X.filter(function (x) { return z.a.some(function (a) { return a[0] === x.it.k; }); }).sort(function (a, b) { return rang(a, true) - rang(b, true); });
    C.forEach(function (x) { if (need <= 1e-9) return; var f = 1; z.a.forEach(function (a) { if (a[0] === x.it.k) f = a[1]; });
      var g = gramm(S, x.it), nimm = Math.min(g, need * f); if (nimm <= 0) return;
      var eg = einheitG(x.k, x.it.e); x.it.m = Math.max(0, Math.round((g - nimm) / eg * 1000) / 1000); need -= nimm / f; weg.push([x.k.n, nimm]); });
  });
  S.lager = (S.lager || []).filter(function (it) { return (+it.m || 0) > 1e-6; });
  return weg;
}

/* Was man auch pur essen kann (zum Auffüllen eines Tages im Speiseplan) */
var NICHT_PUR = ['zwiebeln', 'knoblauch', 'zucker', 'salz', 'bruehe', 'essig', 'senf', 'ketchup', 'mayonnaise', 'tomatenmark', 'passata', 'staerke', 'trockenhefe', 'frischhefe', 'backpulver', 'puddingpulver', 'kakao', 'honig', 'zitronensaft', 'marmelade', 'nusscreme', 'pilze_getr', 'tee', 'kaffee'];
function pur(k) { return ['baby', 'fett', 'trinken'].indexOf(k.g) < 0 && NICHT_PUR.indexOf(k.i) < 0 && !/mehl/.test(k.i); }
/* Speiseplan-Vorschlag: je Tag bis zu drei Gerichte (Portionen = Personen) aus dem Lager, Lücken mit Fertigem füllen */
/* Höchstmenge je Lebensmittel und Tag beim Auffüllen, je Portion (= 2.200-kcal-Bedarf), in g bzw. ml – alltagsnahe Annahme */
function auffuellMax(k) {
  if (/nuesse|mandeln|cashew|kerne|leinsamen|erdnussmus/.test(k.i)) return 50;
  if (/rosinen|pflaumen_getr|aprikosen_getr|feigen_getr|datteln/.test(k.i)) return 50;
  if (k.g === 'sonst') return 40;                       // Süßes, Kekse, Chips
  if (/hartkaese|gouda/.test(k.i)) return 60;
  if (k.g === 'milch') return k.ml ? 250 : 150;        // Milch zum Trinken, Joghurt/Quark
  if (k.g === 'eiweiss') return 120;
  if (k.g === 'obst') return 200;
  if (k.g === 'gemuese') return 150;
  if (k.g === 'getreide') return /haferflocken|muesli|cornflakes/.test(k.i) ? 80 : 120;
  return 100;
}
/* Darf ein Tag damit aufgefüllt werden? Nur, was man üblicherweise pur isst: Brot, Flocken, Obst (auch aus der Dose als Nachtisch),
   Nüsse, Milchprodukte, Süßes, Dauerwurst – keine Gemüse- oder Fleischkonserven pur, keine Zutaten. */
function auffuellOk(k) {
  if (!pur(k) || k.ko || k.fl) return false;
  if (k.g === 'gemuese') return false;
  if (k.g === 'getreide') return k.i !== 'ravioli' && k.i !== 'kartoffeln';
  if (k.g === 'eiweiss') return ['salami', 'leberwurst', 'jagdwurst'].indexOf(k.i) >= 0;
  return ['obst', 'milch', 'sonst'].indexOf(k.g) >= 0 || (k.q === 'eigen' && k.g !== 'baby');
}
/* Mahlzeiten eines Tages mit Anteil am Tagesbedarf (Richtwert für die Verteilung) */
var MAHLZEITEN = [['frueh', 'Frühstück', 0.25], ['mittag', 'Mittag', 0.35], ['abend', 'Abend', 0.30], ['zwischen', 'Zwischenmahlzeit', 0.10]];
var MZN = {}; MAHLZEITEN.forEach(function (m) { MZN[m[0]] = m[1]; });
/* Speiseplan: je Tag Frühstück, Mittag, Abend und eine kalte Zwischenmahlzeit aus dem Lager; Portionen nach Bedarf und passend zum Anteil
   der Mahlzeit; Lücken nur mit pur Essbarem in alltagsnahen Mengen füllen; was dann fehlt, bleibt als Lücke stehen.
   opt.koch = andere Kochmöglichkeit · opt.stopp = früh aufhören, wenn nichts mehr da ist · opt.anteil = Tagesziel als Anteil des Bedarfs („sparsam“) */
function speiseplan(S0, heute, tage, opt) {
  opt = opt || {};
  var S = klon(S0); if (opt.koch) S.lage.koch = opt.koch;
  var H = haushalt(S), D = H.kcalSpar, PH = D / PORTION_KCAL, T = D * Math.min(1, opt.anteil || 1), strom = !!(S.lage || {}).strom, leitung = !!(S.lage || {}).leitung;
  var W = wasser(S0), wasserFrei = leitung ? Infinity : W.l * 1000, tageL = [], zuletzt = {}, knapp = 0, brennMin = 0, leer = 0;
  if (D <= 0 || !H.n) return { tage: [], knapp: 0, brennMin: 0, reicht: 0, rest: 0, PH: 0, anteil: 1 };
  for (var d = 1; d <= tage; d++) {
    if (strom) S.lager = (S.lager || []).filter(function (it) { var ty = ortTyp(S, it.o); return !((ty === 'k' && d > 1) || (ty === 't' && d > 2)); });
    var B = bestand(S, heute), X = posten(S, heute), dringend = {};
    X.forEach(function (x) { var w = 0; if (strom && x.ort === 'k') w = 3; else if (strom && x.ort === 't') w = 2; else if (x.rest != null && x.rest - d < 30) w = 1; if (w) dringend[x.it.k] = Math.max(dringend[x.it.k] || 0, w); });
    var tag = { d: d, essen: [], extra: [], kcal: 0, brenn: 0 }, heuteGenutzt = {}, anteilBis = 0;
    MAHLZEITEN.forEach(function (m) {
      anteilBis += m[2];
      var ziel = T * anteilBis - tag.kcal; if (ziel < T * 0.04) return;
      var zw = m[0] === 'zwischen', best = null, bs = -1e9;
      GERICHTE.forEach(function (r) {
        if (!kannKochen(S, r.koch) || heuteGenutzt[r.id]) return;
        if (zw && r.koch !== 'kalt') return;
        var st = gerichtStatus(S, r, B), wv = gerichtWerte(S, r); if (st.max <= 0 || wv.kcal <= 0) return;
        var port = Math.min(st.max, Math.max(PH * (zw ? 0.2 : 0.5), Math.min(PH * 1.4, ziel / wv.kcal)));
        if (port < PH * (zw ? 0.15 : 0.4)) return;
        if (!leitung && wv.wasser * port > wasserFrei * 0.5) return;
        var kc = wv.kcal * port, s = 40 - Math.abs(kc - ziel) / Math.max(ziel, 1) * 40;
        r.zut.forEach(function (z) { if (z.opt) return; var w = 0; z.a.forEach(function (a) { if (dringend[a[0]] && zutatDa({ a: [a] }, B) > 0) w = Math.max(w, dringend[a[0]]); }); s += 12 * w; });
        if (zuletzt[r.id] && d - zuletzt[r.id] < 3) s -= 30;
        if (m[0] === 'frueh') s += r.fr ? 20 : -90; else if (r.fr && !zw) s -= 15;
        if ((m[0] === 'mittag' || m[0] === 'abend') && r.koch !== 'kalt') s += 8;
        s -= r.z / 10;
        if (s > bs) { bs = s; best = { r: r, port: Math.floor(port * 10 + 1e-6) / 10, wv: wv }; }
      });
      if (!best || best.port <= 0) return;
      abziehen(S, best.r, best.port, heute); B = bestand(S, heute); heuteGenutzt[best.r.id] = 1; zuletzt[best.r.id] = d;
      if (!leitung) wasserFrei -= best.wv.wasser * best.port;
      var bz = best.r.koch === 'kalt' ? 0 : best.r.z; brennMin += bz; tag.brenn += bz;
      tag.essen.push({ id: best.r.id, n: best.r.n, port: best.port, kcal: best.wv.kcal * best.port, mz: m[0], klein: zw }); tag.kcal += best.wv.kcal * best.port;
    });
    if (tag.kcal < T * 0.95) {
      var F = posten(S, heute).filter(function (x) { return x.kcal > 0 && auffuellOk(x.k); }).sort(function (a, b) { return rang(a, strom) - rang(b, strom); });
      F.forEach(function (x) { var gap = T - tag.kcal; if (gap <= 1) return; var gmax = auffuellMax(x.k) * PH, schon = 0;
        tag.extra.forEach(function (e) { if (e.i === x.k.i) schon += e.g; });
        var g = Math.min(x.g, gmax - schon, gap / x.k.k * 100); if (g < 5) return;
        var eg = einheitG(x.k, x.it.e); x.it.m = Math.max(0, Math.round((x.g - g) / eg * 1000) / 1000); tag.kcal += g * x.k.k / 100;
        var da = tag.extra.filter(function (e) { return e.i === x.k.i; })[0]; if (da) da.g += g; else tag.extra.push({ i: x.k.i, n: x.k.n, g: g }); });
      S.lager = (S.lager || []).filter(function (it) { return (+it.m || 0) > 1e-6; });
    }
    tag.deckung = tag.kcal / D; tag.luecke = Math.max(0, D - tag.kcal); if (!knapp && tag.deckung < 0.9) knapp = d;
    tageL.push(tag);
    if (opt.stopp && tag.deckung < 0.02) { if (++leer >= 2) break; } else leer = 0;
  }
  /* reicht = volle Tage (mindestens 90 % gedeckt) vor dem ersten knappen Tag, plus der Anteil dieses Tages */
  var reicht = knapp ? knapp - 1 + tageL[knapp - 1].deckung : tageL.length, rest = 0, summe = 0;
  tageL.forEach(function (t, i) { summe += t.kcal; if (knapp && i >= knapp) rest += Math.min(1, t.deckung); });
  return { tage: tageL, knapp: knapp, brennMin: brennMin, reicht: reicht, rest: rest, PH: PH, voll: !knapp && tageL.length >= tage, summe: summe, anteil: T / D };
}
/* „Sparsam“: das, was sich insgesamt als Mahlzeiten machen lässt, gleichmäßig auf die Ziel-Tage verteilen (höchstens 100 %) */
var SPAR_MIN = 0.6; /* nie unter 60 % planen – wie die kleinste Ration */
function planSparsam(S, heute, z) {
  var A = alltag(S, heute), D = haushalt(S).kcalSpar; if (!D) return A;
  var anteil = Math.max(SPAR_MIN, Math.min(1, A.summe / (D * z)));
  if (anteil >= 0.999) return speiseplan(S, heute, z);
  var best = null;
  for (var i = 0; i < 4; i++) { var P = speiseplan(S, heute, z, { anteil: anteil }), letzte = P.tage[z - 1];
    best = P; if (!letzte || letzte.deckung >= anteil * 0.8 || anteil <= SPAR_MIN) break; anteil = Math.max(SPAR_MIN, anteil * 0.9); }
  return best;
}
/* Alltagsnahe Reichweite: der Speiseplan, so lange, bis nichts mehr da ist (höchstens 90 Tage) */
var ALLTAG_MAX = 90, MEMO = {};
function alltag(S, heute, opt) {
  opt = opt || {}; var key = JSON.stringify([S.personen, S.lage, S.lager, S.eigene, S.orte, opt.koch || '', heute.toDateString()]);
  if (MEMO[key]) return MEMO[key];
  var keys = Object.keys(MEMO); if (keys.length > 12) MEMO = {};
  var P = speiseplan(S, heute, ALLTAG_MAX, { koch: opt.koch, stopp: true }); 
  P.max = !P.knapp && P.tage.length >= ALLTAG_MAX;
  return (MEMO[key] = P);
}

/* Mindestbestand (lebender Vorrat): it.min in derselben Einheit wie die Menge. Ampel: grün ≥ Mindest, gelb ≥ halb, rot darunter */
function ampel(it) { var mi = +it.min || 0; if (!mi) return ''; var m = +it.m || 0; return m >= mi ? 'gruen' : m >= mi / 2 ? 'gelb' : 'rot'; }
/* Preis je Einheit des Postens: S.preise[katId] = Preis je Standard-Packung (bzw. je kg/l/Stück) */
function preisJeG(S, k) { var p = zahl((S.preise || {})[k.i]); if (!isFinite(p) || p <= 0) return null; return p / einheitG(k, stdEinheit(k)); }
/* Nachkauf-Liste: alle Posten unter Mindestbestand, gleiche Lebensmittel zusammengefasst */
function nachkauf(S) {
  var M = {};
  (S.lager || []).forEach(function (it) { var mi = +it.min || 0; if (!mi) return; var k = katVon(S, it.k); if (!k) return; var eg = einheitG(k, it.e);
    var fehltG = Math.max(0, (mi - (+it.m || 0)) * eg); if (fehltG <= 0) return; var x = M[k.i] || (M[k.i] = { k: k, g: 0, e: it.e });
    x.g += fehltG; });
  return Object.keys(M).map(function (id) { var x = M[id], eg = einheitG(x.k, x.e), pj = preisJeG(S, x.k);
    return { k: x.k, g: x.g, anzahl: Math.ceil(x.g / eg - 1e-9), einheit: einheitT(x.k, x.e), kosten: pj != null ? Math.ceil(x.g / eg - 1e-9) * eg * pj : null }; });
}
/* Einkaufsliste bis zum Ziel */
function fehltListe(S, heute) {
  var H = haushalt(S), z = zielTage(S), R = gruppenStand(S, heute), W = wasser(S), out = [];
  GRUPPEN.forEach(function (g) { var r = R[g.k]; if (!g.ble) return; var gap = r.ziel - r.ist; if (gap > r.ziel * 0.05 && gap > 50) out.push({ g: g, gap: gap, ziel: r.ziel, ist: r.ist }); });
  var wz = W.bedarf * z, wl = W.leitung ? 0 : Math.max(0, wz - W.l);
  var rw = reichweite(S, heute), kcalFehlt = Math.max(0, H.kcal * z - rw.start);
  return { gruppen: out, wasserL: wl, wasserZiel: wz, kcal: kcalFehlt, ziel: z };
}
function vorschlag(S, gk, gap) {
  var ids = (VORSCHLAG[gk] || []).slice(0, 2), out = [];
  ids.forEach(function (id) { var k = KAT[id]; if (!k) return; var teil = gap / ids.length / (k.x || 1), pg = k.p && k.p.length ? k.p[0] : null;
    var nm = k.n.replace(/ \(.*\)$/, '').replace(/, trocken$/, ''); if (pg) out.push(Math.max(1, Math.ceil(teil / pg[1])) + ' × ' + nm + ' (' + pg[0].replace(/ \(.*\)$/, '') + ')'); else out.push(kg(teil) + ' ' + nm); });
  return out;
}

/* Beispiel-Haushalt beim ersten Öffnen */
function beispiel(heute) {
  var y = heute.getFullYear(), mo = heute.getMonth() + 1, m = function (plus) { var t = (mo - 1) + plus, yy = y + Math.floor(t / 12), mm = (t % 12 + 12) % 12 + 1; return yy + '-' + (mm < 10 ? '0' : '') + mm; };
  var L = function (k, mm, e, mhd, o) { return { u: uid(), k: k, m: mm, e: e, mhd: mhd || '', o: o || (KAT[k].l || 'v') }; };
  var B0 = leer(); return Object.assign(B0, { beispiel: true, tab: 'uebersicht',
    personen: [{ id: uid(), n: 'Erwachsener', s: 'm', a: 42, kg: 84, cm: 180, t: 'normal' }, { id: uid(), n: 'Erwachsene', s: 'w', a: 39, kg: 64, cm: 168, t: 'normal' }, { id: uid(), n: 'Kind', s: 'm', a: 9, kg: 30, cm: 136, t: 'normal' }],
    tiere: [], lage: { strom: true, leitung: false, koch: 'gas', ziel: 10, zielFrei: 21, spar: 100, hyg: 0, kartusche: '' },
    lager: [L('nudeln', 4, 'p0', m(14)), L('reis', 1, 'p0', m(10)), L('haferflocken', 2, 'p0', m(5)), L('knaecke', 2, 'p0', m(8)), L('kartoffeln', 1, 'p0', ''),
      L('linsen', 1, 'p0', m(20)), L('kidney_dose', 2, 'p0', m(24)), L('erbsen_moehren', 2, 'p0', m(30)), L('tomaten_dose', 3, 'p0', m(18)), L('zwiebeln', 1, 'p0', ''),
      L('pfirsiche', 2, 'p0', m(16)), L('apfelmus', 1, 'p0', m(2)), L('rosinen', 1, 'p0', m(6)), L('haselnuesse', 1, 'p0', m(1)),
      L('hmilch', 4, 'p0', m(3)), L('hartkaese', 1, 'p0', '', 'k'), L('joghurt', 1, 'p0', m(0), 'k'),
      L('thunfisch', 3, 'p0', m(36)), L('wuerstchen', 1, 'p0', m(20)), L('eier', 1, 'p0', m(0), 'k'), L('hack_tk', 1, 'p0', m(4), 't'),
      L('rapsoel', 1, 'p0', m(9)), L('butter', 1, 'p0', m(1), 'k'), L('wasser', 2, 'p3', m(14)), L('zucker', 1, 'p0', ''), L('honig', 1, 'p0', m(24)), L('bruehe', 1, 'p0', m(12))],
    eigene: [], haken: {} });
}
function leer() { return { v: 2, beispiel: false, tab: 'uebersicht', personen: [], tiere: [], lage: { strom: true, leitung: false, koch: 'gas', ziel: 10, zielFrei: 21, spar: 100, hyg: 0, kartusche: '' }, lager: [], eigene: [], haken: {},
  orte: klon(ORTE_STD), preise: {}, ean: {}, plan: { modus: 'satt' }, budget: '', bestaende: [], notfall: {}, ablauf: {}, region: {}, stromG: [], wasserQ: {}, strom: {} }; }
function pruefeStand(x) {
  if (!x || typeof x !== 'object' || !Array.isArray(x.personen) || !Array.isArray(x.lager)) return null;
  var S = leer(); Object.keys(S).forEach(function (k) { if (x[k] != null) S[k] = x[k]; });
  S.lage = Object.assign(leer().lage, x.lage || {}); S.lager = S.lager.filter(function (it) { return it && it.k && (KAT[it.k] || (S.eigene || []).some(function (e) { return e.i === it.k; })); });
  S.lager.forEach(function (it) { if (!it.u) it.u = uid(); });
  /* Umstellung von Fassung 1: Orte, neue Felder, Startansicht „Übersicht“ */
  if (!Array.isArray(S.orte) || !S.orte.length) S.orte = klon(ORTE_STD);
  ORTE_STD.forEach(function (o) { if (!S.orte.some(function (x) { return x.id === o.id; })) S.orte.push(klon(o)); });
  S.lager.forEach(function (it) { if (!S.orte.some(function (o) { return o.id === it.o; })) it.o = 'v'; });
  ['preise', 'ean', 'notfall', 'ablauf', 'region', 'wasserQ', 'haken', 'strom'].forEach(function (k) { if (!S[k] || typeof S[k] !== 'object' || Array.isArray(S[k])) S[k] = {}; });
  ['bestaende', 'stromG', 'eigene', 'tiere'].forEach(function (k) { if (!Array.isArray(S[k])) S[k] = []; });
  if (!S.plan || typeof S.plan !== 'object') S.plan = { modus: 'satt' };
  if (!(x.v >= 2)) { S.tab = 'uebersicht'; } S.v = 2;
  return S;
}

var KERN = { KATALOG: KATALOG, GERICHTE: GERICHTE, GRUPPEN: GRUPPEN, DGE_E: DGE_E, QUELLEN: QUELLEN, CHECK: CHECK, bedarf: bedarf, haushalt: haushalt, reichweite: reichweite, wasser: wasser, gruppenStand: gruppenStand,
  eiweissTage: eiweissTage, alltag: alltag, dateiMoeglich: dateiMoeglich, reichtFuer: reichtFuer, portionenHaushalt: portionenHaushalt, auffuellMax: auffuellMax, PORTION_KCAL: PORTION_KCAL, bestand: bestand, gerichtWerte: gerichtWerte, gerichtStatus: gerichtStatus, abziehen: abziehen, speiseplan: speiseplan, fehltListe: fehltListe, vorschlag: vorschlag,
  beispiel: beispiel, leer: leer, pruefeStand: pruefeStand, ampel: ampel, notquellen: notquellen, WQ: WQ, sichtbareTabs: function () { return sichtbareTabs(); }, NAV: NAV, nachkauf: nachkauf, preisJeG: preisJeG, planSparsam: planSparsam, auffuellOk: auffuellOk, ortTyp: ortTyp, ortName: ortName, MAHLZEITEN: MAHLZEITEN, einheitG: einheitG, stdEinheit: stdEinheit, gramm: gramm, einheiten: einheiten, zielTage: zielTage, posten: posten, katVon: katVon, kannKochen: kannKochen };

/* ===================================================================== 4. Oberfläche */
var S = null, R = null, FIG = null, UNDO = null, TOAST_T = null, SPEICHER_T = null, SUCHE = '', GF = { st: 'alle', art: 'alle', meine: true, ohneW: false }, PLAN = null, OFFEN = {};
/* Navigation: vier Gruppen, darin die Bereiche. Bereiche ohne Darstellung (z. B. wenn vorrat_plus.js fehlt) werden nicht gezeigt. */
var NAV = [['start', 'Übersicht', '⌂', ['uebersicht']], ['vorrat', 'Vorrat', '🥫', ['reichweite', 'lager', 'gerichte', 'naehrstoffe', 'fehlt', 'haltbar']],
  ['plan', 'Haushalt & Plan', '👪', ['haushalt', 'vergleich', 'kosten', 'vorlage', 'blatt']], ['notfall', 'Notfall', '🔦', ['ablauf', 'bestaende', 'strom', 'wasser', 'kochen', 'notfallplan', 'region']]];
var TABNAME = { uebersicht: ['Übersicht', '⌂'], reichweite: ['Reichweite', '◔'], lager: ['Lager', '🥫'], gerichte: ['Gerichte', '🍲'], fehlt: ['Fehlt noch', '🛒'], haltbar: ['Haltbarkeit', '📅'], naehrstoffe: ['Nährstoffe', '🥕'],
  haushalt: ['Haushalt', '👪'], vergleich: ['Vergleich', '⚖'], kosten: ['Kosten', '€'], vorlage: ['Startvorlage', '📋'], blatt: ['Notfall-Blatt', '🖨'],
  ablauf: ['Ablauf', '⏱'], bestaende: ['Ausrüstung', '🩹'], strom: ['Strom & Wärme', '🔋'], wasser: ['Wasser', '💧'], kochen: ['Kochen ohne Strom', '🔥'], notfallplan: ['Notfallplan', '📞'], region: ['Region', '📍'] };
/* Erweiterungen (vorrat_plus.js) hängen sich hier ein */
var HAKEN = { klick: [], eingabe: [], aenderung: [], postenMehr: [], lagerOben: [], fehltOben: [], haushaltUnten: [], nachZeichnen: [] };
function sichtbareTabs() { var L = []; NAV.forEach(function (g) { g[3].forEach(function (t) { if (BEREICH[t]) L.push(t); }); }); return L; }
function gruppeVon(t) { for (var i = 0; i < NAV.length; i++) if (NAV[i][3].indexOf(t) >= 0) return NAV[i]; return NAV[1]; }
function heute() { var d = new Date(); d.setHours(12, 0, 0, 0); return d; }
function laden() { try { var x = JSON.parse(localStorage.getItem(SPEICHER) || 'null'); return pruefeStand(x); } catch (e) { return null; } }
function sichern() { if (SPEICHER_T) clearTimeout(SPEICHER_T); SPEICHER_T = setTimeout(function () { try { localStorage.setItem(SPEICHER, JSON.stringify(S)); } catch (e) { toast('Speichern ging nicht – ist der Speicher voll oder gesperrt?'); } }, 250); }
function sichernJetzt() { try { localStorage.setItem(SPEICHER, JSON.stringify(S)); } catch (e) { /* gesperrt */ } }

function seg(name, L, wert, cls) { return '<div class="vr-seg ' + (cls || '') + '" role="group">' + L.map(function (o) { return '<button type="button" data-set="' + name + '" data-wert="' + esc(o[0]) + '" aria-pressed="' + (String(wert) === String(o[0])) + '">' + esc(o[1]) + '</button>'; }).join('') + '</div>'; }
function feld(lbl, inner, cls) { return '<label class="vr-feld ' + (cls || '') + '"><span class="vr-fl">' + lbl + '</span>' + inner + '</label>'; }
function zahlIn(attr, wert, einh, ph, mode) { return '<span class="vr-ein"><input type="text" inputmode="' + (mode || 'decimal') + '" ' + attr + ' value="' + esc(wert == null ? '' : String(wert).replace('.', ',')) + '" placeholder="' + esc(ph || '') + '" autocomplete="off">' + (einh ? '<i>' + einh + '</i>' : '') + '</span>'; }
function balken(ist, ziel, cls) { var p = ziel > 0 ? Math.min(100, ist / ziel * 100) : 0; return '<span class="vr-bar ' + (cls || '') + '" role="img" aria-label="' + fz(p) + ' Prozent"><i style="width:' + p.toFixed(1) + '%"></i></span>'; }
function leerText(t, knopf) { return '<div class="vr-leer"><p>' + t + '</p>' + (knopf || '') + '</div>'; }

/* ---------- Kopf, Leiste ---------- */
function kopfHTML() {
  return '<header class="vr-kopf"><p class="vr-ober">Werkzeug · offline · nur auf diesem Gerät</p><h1>Vorrat &amp; Blackout-Planer</h1>' +
    '<p class="vr-intro">Wie lange reichen Essen und Wasser für deinen Haushalt? Was kannst du daraus kochen und backen, was fehlt noch und was läuft bald ab?</p>' +
    (FIG ? '<div class="vr-bild">' + FIG + '</div>' : '') + '</header>';
}
function leisteHTML() { return '<div class="vr-leiste">' + leisteInnen() + '</div>'; }
function leisteInnen() {
  var G = gruppeVon(S.tab), unter = G[3].filter(function (t) { return BEREICH[t]; });
  return '<div class="vr-kurz" aria-live="polite">' + kurzZeile() + '</div><nav class="vr-gnav" aria-label="Bereiche">' + NAV.filter(function (g) { return g[3].some(function (t) { return BEREICH[t]; }); }).map(function (g) {
      var erst = g[3].filter(function (t) { return BEREICH[t]; })[0];
      return '<button type="button" data-tab="' + (g === G ? S.tab : (OFFEN['g:' + g[0]] && BEREICH[OFFEN['g:' + g[0]]] ? OFFEN['g:' + g[0]] : erst)) + '" aria-current="' + (g === G) + '"><span aria-hidden="true">' + g[2] + '</span>' + esc(g[1]) + '</button>'; }).join('') + '</nav>' +
    (unter.length > 1 ? '<nav class="vr-tabs" role="tablist" aria-label="' + esc(G[1]) + '">' + unter.map(function (t) { return '<button type="button" role="tab" data-tab="' + t + '" aria-selected="' + (S.tab === t) + '"><span aria-hidden="true">' + TABNAME[t][1] + '</span>' + TABNAME[t][0] + '</button>'; }).join('') + '</nav>' : '');
}
function kurzZeile() {
  var h = heute(), H = haushalt(S), A = alltag(S, h), W = wasser(S), z = zielTage(S), rw = { tage: A.max ? 730 : A.reicht };
  if (!H.n) return '<span>Noch niemand im Haushalt – lege unter „Haushalt“ Personen an.</span>';
  var gut = function (t) { return t >= z ? 'vr-gut' : t >= Math.min(3, z) ? 'vr-mittel' : 'vr-schlecht'; };
  return '<span><b>' + H.n + '</b> ' + (H.n === 1 ? 'Person' : 'Personen') + '</span><span><b>' + fz(H.kcalSpar) + '</b> kcal/Tag</span>' +
    '<span class="' + gut(rw.tage) + '">Essen <b>' + tageText(rw.tage) + '</b></span><span class="' + gut(W.tage) + '">Wasser <b>' + (W.leitung ? 'Leitung' : tageText(W.tage)) + '</b></span>';
}

/* ---------- 1. Haushalt ---------- */
function personHTML(p, i) {
  var b = bedarf(p);
  return '<article class="vr-karte vr-person" data-p="' + i + '"><div class="vr-kh"><input class="vr-name" type="text" data-pf="n" value="' + esc(p.n || '') + '" placeholder="Name" aria-label="Name" maxlength="40">' +
    '<button type="button" class="vr-x" data-weg-p="' + i + '" aria-label="Person entfernen">✕</button></div>' +
    '<div class="vr-felder">' + feld('Geschlecht', seg('p' + i + ':s', [['m', 'Mann'], ['w', 'Frau']], p.s || 'm')) +
    feld('Alter', zahlIn('data-pf="a"', p.a, 'Jahre', '', 'numeric')) + feld('Gewicht', zahlIn('data-pf="kg"', p.kg, 'kg')) + feld('Größe', zahlIn('data-pf="cm"', p.cm, 'cm', '', 'numeric')) +
    feld('Tätigkeit', seg('p' + i + ':t', TAETIG.map(function (t) { return [t[0], t[1]]; }), p.t || 'normal'), 'vr-voll') + '</div>' +
    '<div class="vr-erg" data-perg="' + i + '">' + personErg(p, b) + '</div>' +
    '<details class="vr-mehr"><summary>Eigenen Kalorienwert eintragen</summary>' + feld('Eigener Wert (z. B. vom Arzt; leer = berechnet)', zahlIn('data-pf="eigen"', p.eigen, 'kcal/Tag', '', 'numeric')) + '</details></article>';
}
function personErg(p, b) {
  if (!b.kcal) return '<p class="vr-hinweis">' + esc(b.text || 'Angaben ergänzen') + '</p>';
  return '<div class="vr-zahlen"><div><b>' + fz(b.kcal) + '</b><small>kcal am Tag</small></div><div><b>' + fz(b.eiweiss) + ' g</b><small>Eiweiß (DGE)</small></div><div><b>' + fz(WASSER_TAG + (haushalt(S).hyg || 0), 1) + ' l</b><small>Wasser</small></div></div>' +
    '<p class="vr-klein">' + esc(b.text) + (b.art === 'dge' ? ' · Richtwert' : '') + '</p>';
}
function tierHTML(t, i) {
  var f = zahl(t.futter), v = zahl(t.vorrat), tg = f > 0 && v >= 0 ? v * 1000 / f : NaN;
  return '<article class="vr-karte vr-tier" data-t="' + i + '"><div class="vr-kh"><input class="vr-name" type="text" data-tf="n" value="' + esc(t.n || '') + '" placeholder="z. B. Hund" aria-label="Name des Tieres" maxlength="30"><button type="button" class="vr-x" data-weg-t="' + i + '" aria-label="Tier entfernen">✕</button></div>' +
    '<div class="vr-felder">' + feld('Futter am Tag', zahlIn('data-tf="futter"', t.futter, 'g', '', 'numeric')) + feld('Wasser am Tag', zahlIn('data-tf="wasser"', t.wasser, 'l')) + feld('Futter im Vorrat', zahlIn('data-tf="vorrat"', t.vorrat, 'kg')) + '</div>' +
    '<p class="vr-klein" data-terg="' + i + '">' + (isFinite(tg) ? 'Futter reicht etwa <b>' + tageText(tg) + '</b>.' : 'Mengen eintragen – das Futter steht auf der Packung oder beim Tierarzt.') + '</p></article>';
}
function haushaltHTML() {
  var H = haushalt(S), L = S.lage;
  var h = '<section class="vr-bereich" data-b="haushalt"><h2>Haushalt</h2><p class="vr-unter">Wer gehört dazu? Daraus ergibt sich, wie viel ihr am Tag braucht.</p>';
  h += S.personen.length ? '<div class="vr-raster">' + S.personen.map(personHTML).join('') + '</div>' : leerText('Noch niemand angelegt – tippe auf „Person hinzufügen“.');
  h += '<div class="vr-knoepfe"><button type="button" class="vr-knopf vr-haupt" data-neu-p>＋ Person hinzufügen</button></div>';
  h += '<div class="vr-karte vr-summe"><div class="vr-zahlen"><div><b>' + fz(H.kcal) + '</b><small>kcal am Tag für alle</small></div><div><b>' + fz(H.eiweiss) + ' g</b><small>Eiweiß am Tag</small></div><div><b>' + fz(H.wasser, 1) + ' l</b><small>Wasser am Tag</small></div></div>' +
    '<p class="vr-klein">Erwachsene ab 18: Grundumsatz nach Mifflin-St Jeor (wie im Energie-Rechner der App) × Tätigkeit (ruhig 1,4 · normal 1,6 · körperlich 1,8). Kinder und Jugendliche: Richtwerte der DGE. Eiweiß: DGE-Referenzwerte je kg Körpergewicht. Wasser: 2 l je Person und Tag, davon 0,5 l zum Kochen (BBK). Alles Richtwerte.</p></div>';
  h += '<h3>Haustiere</h3>' + (S.tiere.length ? '<div class="vr-raster">' + S.tiere.map(tierHTML).join('') + '</div>' : '<p class="vr-klein">Keine Haustiere eingetragen.</p>') +
    '<div class="vr-knoepfe"><button type="button" class="vr-knopf" data-neu-t>＋ Haustier hinzufügen</button></div>';
  h += '<h3>Lage</h3><div class="vr-karte vr-lage"><div class="vr-felder">' +
    feld('Strom weg?', seg('lage:strom', [['1', 'Ja'], ['0', 'Nein']], L.strom ? '1' : '0')) +
    feld('Leitungswasser da?', seg('lage:leitung', [['1', 'Ja'], ['0', 'Nein']], L.leitung ? '1' : '0')) +
    feld('Kochmöglichkeit', seg('lage:koch', KOCH.map(function (k) { return [k[0], k[1]]; }), L.koch, 'vr-seg-wrap'), 'vr-voll') +
    (L.strom && L.koch === 'herd' ? '<p class="vr-warn vr-voll">Ein Elektroherd geht ohne Strom nicht. „Herd normal“ nur wählen, wenn es ein Gasherd ist.</p>' : '') +
    feld('Ziel: so viele Tage', seg('lage:ziel', ZIELE.map(function (z) { return [String(z), String(z)]; }).concat([['frei', 'frei']]), String(L.ziel)), 'vr-voll') +
    (L.ziel === 'frei' ? feld('Eigene Zahl', zahlIn('data-lf="zielFrei"', L.zielFrei, 'Tage', '', 'numeric')) : '') +
    feld('Ration', seg('lage:spar', [['100', '100 %'], ['80', '80 %'], ['60', '60 %']], String(L.spar)), 'vr-voll') +
    (+L.spar < 100 ? '<p class="vr-warn vr-voll">Weniger essen geht nur für kurze Zeit und nur für gesunde Erwachsene – nicht für Kinder, Schwangere, Stillende, Kranke oder ältere Menschen. Wasser nie kürzen. Das ist eine Rechenhilfe, keine Empfehlung.</p>' : '') +
    feld('Zusätzlich Wasser zum Waschen', zahlIn('data-lf="hyg"', L.hyg || '', 'l je Person/Tag', '0 = aus'), 'vr-voll') +
    (L.koch === 'gas' ? feld('Brenndauer einer Gaskartusche (steht auf der Packung)', zahlIn('data-lf="kartusche"', L.kartusche, 'Minuten', 'leer = keine Schätzung', 'numeric'), 'vr-voll') : '') +
    '</div><p class="vr-klein">Der BBK rät, sich möglichst 10 Tage selbst versorgen zu können – aber auch ein Vorrat für 3 Tage hilft schon sehr.</p>' + (HAKEN.lageHinweis ? HAKEN.lageHinweis(S) : '') + '</div>';
  h += sicherungHTML();
  return h + '</section>';
}
/* Datei speichern/laden geht nicht, wenn die Seite eingebettet läuft (Claude-Artefakt: Downloads gesperrt) */
function dateiMoeglich() {
  if (typeof window === 'undefined') return false;
  var rahmen = true; try { rahmen = window.self !== window.top; } catch (e) { rahmen = true; }
  var hn = (location && location.hostname) || '', pr = (location && location.protocol) || '';
  if (rahmen || /claude|anthropic/i.test(hn) || pr === 'blob:' || pr === 'about:' || pr === 'data:') return false;
  return true;
}
function sicherungHTML() {
  var datei = dateiMoeglich();
  return '<h3>Sicherung</h3><div class="vr-karte"><p class="vr-klein">Alles bleibt nur auf diesem Gerät. Zum Umzug (z. B. vom iPhone aufs iPad) ' + (datei ? 'als Datei speichern oder ' : '') + 'als Text kopieren und auf dem anderen Gerät einfügen.</p>' +
    (datei ? '' : '<p class="vr-hinweis vr-klein">In dieser Vorschau sind Downloads gesperrt – darum hier nur „Als Text kopieren“ und „Text einfügen“. In der installierten App geht auch das Speichern als Datei.</p>') +
    '<div class="vr-knoepfe">' + (datei ? '<button type="button" class="vr-knopf" data-sich="datei">Als Datei speichern</button><label class="vr-knopf vr-datei">Datei laden<input type="file" accept=".json,application/json,text/plain" data-sich-datei></label>' : '') +
    '<button type="button" class="vr-knopf" data-sich="kopie">Als Text kopieren</button></div>' +
    '<details class="vr-mehr"><summary>Text einfügen</summary><textarea class="vr-text" rows="4" placeholder="Hier den kopierten Text einfügen" aria-label="Sicherungstext"></textarea><div class="vr-knoepfe"><button type="button" class="vr-knopf vr-haupt" data-sich="einfuegen">Übernehmen</button></div></details>' +
    HAKEN.haushaltUnten.map(function (f) { return f(); }).join('') +
    '<div class="vr-knoepfe"><button type="button" class="vr-knopf vr-gefahr" data-sich="alles-weg">Alles löschen</button></div></div>';
}

/* ---------- 2. Lager ---------- */
function alleKat() { return KATALOG.concat(S.eigene || []); }
function sucheTreffer(q) {
  q = q.toLowerCase().trim(); if (!q) return [];
  var W = q.split(/\s+/);
  return alleKat().map(function (k) { var t = (k.n + ' ' + (k.s || '')).toLowerCase(), s = 0; for (var i = 0; i < W.length; i++) { var p = t.indexOf(W[i]); if (p < 0) return null; s += p === 0 ? 0 : t.charAt(p - 1) === ' ' ? 1 : 3; } return [s + (k.n.toLowerCase().indexOf(q) === 0 ? -2 : 0), k]; })
    .filter(Boolean).sort(function (a, b) { return a[0] - b[0] || a[1].n.localeCompare(b[1].n, 'de'); }).slice(0, 10).map(function (x) { return x[1]; });
}
function trefferHTML() {
  var T = sucheTreffer(SUCHE);
  if (!SUCHE) return '';
  if (!T.length) return '<p class="vr-klein">Nichts gefunden. Lege es unten unter „Eigenes Lebensmittel“ an.</p>';
  return '<ul class="vr-treffer" role="list">' + T.map(function (k) { return '<li><button type="button" data-add="' + esc(k.i) + '"><span>' + esc(k.n) + '</span><small>' + GR[k.g].kurz + ' · ' + fz(k.k) + ' kcal/100 ' + (k.ml ? 'ml' : 'g') + '</small><b aria-hidden="true">＋</b></button></li>'; }).join('') + '</ul>';
}
function mhdSel(it) {
  var m = /^(\d{4})-(\d{2})$/.exec(it.mhd || ''), y0 = new Date().getFullYear(), jm = m ? +m[1] : 0, mm = m ? +m[2] : 0, J = [];
  for (var y = y0 - 2; y <= y0 + 10; y++) J.push(y); if (jm && J.indexOf(jm) < 0) J.unshift(jm);
  return '<span class="vr-mhd"><select data-lf2="mm" aria-label="Haltbar bis Monat"><option value="">Monat</option>' + MONATE.map(function (t, i) { return '<option value="' + (i + 1) + '"' + (mm === i + 1 ? ' selected' : '') + '>' + t + '</option>'; }).join('') + '</select>' +
    '<select data-lf2="jj" aria-label="Haltbar bis Jahr"><option value="">Jahr</option>' + J.map(function (y) { return '<option' + (jm === y ? ' selected' : '') + '>' + y + '</option>'; }).join('') + '</select></span>';
}
function postenHTML(x, h) {
  var it = x.it, k = x.k, warn = x.rest != null && x.rest < 0 ? ' vr-ab' : x.rest != null && x.rest < 30 ? ' vr-bald' : '';
  var amp = ampel(it);
  return '<li class="vr-posten' + warn + '" data-u="' + esc(it.u) + '"><div class="vr-pk"><b>' + (amp ? '<i class="vr-amp vr-amp-' + amp + '" title="Mindestbestand ' + (amp === 'gruen' ? 'erreicht' : 'unterschritten') + '"></i>' : '') + esc(it.n || k.n) + (it.art ? ' <small class="vr-art">' + esc(it.art) + '</small>' : '') + '</b><span>' + fz(x.kcal) + ' kcal' + (k.fl ? ' · ' + liter(x.g / 1000) : ' · ' + kg(x.g)) + ' · ' + esc(ortName(S, it.o)) + '</span></div>' +
    '<div class="vr-pm"><button type="button" class="vr-rund" data-minus aria-label="weniger">−</button><span class="vr-ein vr-menge"><input type="text" inputmode="decimal" data-lf2="m" value="' + esc(String(Math.round((+it.m || 0) * 100) / 100).replace('.', ',')) + '" aria-label="Menge"></span>' +
    '<button type="button" class="vr-rund" data-plus aria-label="mehr">＋</button>' +
    '<select data-lf2="e" aria-label="Einheit">' + einheiten(k).map(function (e) { return '<option value="' + e.k + '"' + (e.k === it.e ? ' selected' : '') + '>' + esc(e.t.replace(/ \((ca\. )?(\d[^)]*abgetropft|\d+ g)\)$/, '')) + '</option>'; }).join('') + '</select></div>' +
    '<div class="vr-pd">' + mhdSel(it) + '<select data-lf2="o" aria-label="Lagerort">' + S.orte.map(function (o) { return '<option value="' + esc(o.id) + '"' + (o.id === (it.o || 'v') ? ' selected' : '') + '>' + esc(o.n) + '</option>'; }).join('') + '</select>' +
    '<button type="button" class="vr-x" data-weg-l aria-label="' + esc(k.n) + ' entfernen">✕</button></div>' +
    '<details class="vr-pmehr"' + (OFFEN['pm:' + it.u] ? ' open' : '') + ' data-pm="' + esc(it.u) + '"><summary>Mindestbestand, Preis' + (HAKEN.postenMehr.length ? ', Erinnerung, Strichcode' : '') + '</summary><div class="vr-felder">' +
    feld('Mindestens da (in ' + esc(einheitT(k, it.e).replace(/ \(.*\)$/, '')) + ')', zahlIn('data-lf2="min"', it.min || '', '', 'leer = egal')) +
    feld('Preis je ' + esc(einheitT(k, stdEinheit(k)).replace(/ \(.*\)$/, '')) + ' (freiwillig)', zahlIn('data-preis="' + esc(k.i) + '"', (S.preise || {})[k.i] || '', '€')) + '</div>' +
    HAKEN.postenMehr.map(function (f) { return f(x); }).join('') + '</details>' +
    (warn ? '<p class="vr-klein vr-pw">' + (x.rest < 0 ? 'MHD überschritten – prüfen (Aussehen, Geruch, Geschmack).' : 'Läuft in ' + x.rest + ' Tagen ab – bald verbrauchen.') + '</p>' : '') + '</li>';
}
function lagerHTML() {
  var h0 = heute(), X = posten(S, h0), sum = 0; X.forEach(function (x) { if (x.k.g !== 'baby') sum += x.kcal; });
  var h = '<section class="vr-bereich" data-b="lager"><h2>Lager</h2><p class="vr-unter">Was hast du im Haus? Suchen, antippen, Menge anpassen.</p>' +
    '<div class="vr-such"><label class="vr-vh" for="vr-such">Lebensmittel suchen</label><span aria-hidden="true">⌕</span><input id="vr-such" type="search" placeholder="z. B. Nudeln, Thunfisch, Wasser …" autocomplete="off" value="' + esc(SUCHE) + '"></div>' +
    '<div class="vr-treffer-ort" aria-live="polite">' + trefferHTML() + '</div>' +
    '<details class="vr-mehr vr-katalog"><summary>Aus der Liste wählen (' + KATALOG.length + ' Lebensmittel)</summary>' + GRUPPEN.map(function (g) {
      var K = alleKat().filter(function (k) { return k.g === g.k; }); if (!K.length) return '';
      return '<details class="vr-kg"><summary>' + g.i + ' ' + esc(g.n) + ' <span>' + K.length + '</span></summary><div class="vr-chips">' + K.map(function (k) { return '<button type="button" class="vr-chip" data-add="' + esc(k.i) + '">' + esc(k.n) + '</button>'; }).join('') + '</div></details>'; }).join('') + '</details>' +
    '<details class="vr-mehr"><summary>Eigenes Lebensmittel anlegen</summary>' + eigenFormHTML() + '</details>';
  h += HAKEN.lagerOben.map(function (f) { return f(); }).join('') + orteHTML();
  if (!X.length) h += leerText('Noch nichts im Lager – tippe oben ins Suchfeld oder auf „Aus der Liste wählen“.');
  else {
    var LF = OFFEN.lf || { ort: '', q: '', ansicht: 'liste' }, q = (LF.q || '').toLowerCase().trim();
    var Y = X.filter(function (x) { return (!LF.ort || (x.it.o || 'v') === LF.ort) && (!q || (x.k.n + ' ' + (x.k.s || '') + ' ' + ortName(S, x.it.o)).toLowerCase().indexOf(q) >= 0); });
    h += '<div class="vr-lfilter"><h3>Im Lager <small class="vr-zaehl">' + X.length + ' Posten · ' + fz(sum) + ' kcal</small></h3>' +
      '<div class="vr-such vr-such-klein"><label class="vr-vh" for="vr-finde">Im Lager finden</label><span aria-hidden="true">⌕</span><input id="vr-finde" type="search" placeholder="Wo liegt was? z. B. Reis" autocomplete="off" value="' + esc(LF.q || '') + '"></div>' +
      '<div class="vr-chips vr-kein-wisch"><button type="button" class="vr-chip" data-lort="" aria-pressed="' + !LF.ort + '">Alle Orte</button>' + S.orte.map(function (o) { var n = X.filter(function (x) { return (x.it.o || 'v') === o.id; }).length;
        return n ? '<button type="button" class="vr-chip" data-lort="' + esc(o.id) + '" aria-pressed="' + (LF.ort === o.id) + '">' + esc(o.n) + ' <small>' + n + '</small></button>' : ''; }).join('') + '</div>' +
      seg('lf:ansicht', [['liste', 'Alles bearbeiten'], ['alltag', 'Alltag: verbraucht']], LF.ansicht || 'liste') + '</div><div class="vr-lliste">' + lagerListeHTML(Y, LF, h0) + '</div>';
  }
  h += '<p class="vr-klein">Nährwerte je 100 g aus der Nährwert-Liste der App bzw. USDA FoodData Central (gerundet); Packungsgrößen und Haltbarkeiten sind Richtwerte – maßgeblich ist das Etikett.</p>';
  return h + '</section>';
}
function lagerListeHTML(Y, LF, h0) {
  if (!Y.length) return '<p class="vr-klein">Nichts gefunden.</p>';
  if (LF.ansicht === 'alltag') return '<p class="vr-klein">Für den Alltag: Was ihr aus dem Vorrat nehmt, mit „verbraucht“ abziehen. Steht ein Mindestbestand fest, zeigt die Ampel, wann nachgekauft werden muss (Liste unter „Fehlt noch“).</p><ul class="vr-alltag" role="list">' +
    Y.slice().sort(function (a, b) { var o = { rot: 0, gelb: 1, gruen: 2, '': 3 }; return o[ampel(a.it)] - o[ampel(b.it)] || a.k.n.localeCompare(b.k.n, 'de'); }).map(function (x) { var it = x.it, amp = ampel(it);
      return '<li data-u="' + esc(it.u) + '" class="vr-posten vr-posten-kurz"><span class="vr-amp ' + (amp ? 'vr-amp-' + amp : 'vr-amp-leer') + '" aria-label="' + (amp === 'rot' ? 'nachkaufen' : amp === 'gelb' ? 'bald nachkaufen' : amp ? 'genug' : 'kein Mindestbestand') + '"></span><span class="vr-ak"><b>' + esc(x.k.n) + '</b><small>' + fz(+it.m || 0, 2) + ' × ' + esc(einheitT(x.k, it.e).replace(/ \(.*\)$/, '')) + (it.min ? ' · mindestens ' + fz(+it.min, 2) : '') + ' · ' + esc(ortName(S, it.o)) + '</small></span><button type="button" class="vr-knopf vr-verbr" data-minus>− 1 verbraucht</button></li>'; }).join('') + '</ul>';
  var h = ''; GRUPPEN.forEach(function (g) { var G = Y.filter(function (x) { return x.k.g === g.k; }); if (!G.length) return;
    h += '<h3 class="vr-gt">' + g.i + ' ' + esc(g.n) + '</h3><ul class="vr-liste" role="list">' + G.map(function (x) { return postenHTML(x, h0); }).join('') + '</ul>'; });
  return h;
}
function orteHTML() {
  return '<details class="vr-mehr vr-orte"' + (OFFEN.orte ? ' open' : '') + '><summary>Lagerorte verwalten (' + S.orte.length + ')</summary><div class="vr-karte"><ul class="vr-ortliste" role="list">' + S.orte.map(function (o) {
    return '<li data-ort="' + esc(o.id) + '"><span class="vr-ein"><input type="text" data-ortn value="' + esc(o.n) + '" maxlength="30" aria-label="Name des Lagerorts"></span><select data-ortt aria-label="Art des Lagerorts">' + [['v', 'ungekühlt'], ['k', 'gekühlt'], ['t', 'gefroren']].map(function (t) { return '<option value="' + t[0] + '"' + (o.typ === t[0] ? ' selected' : '') + '>' + t[1] + '</option>'; }).join('') + '</select>' +
      (['v', 'k', 't'].indexOf(o.id) < 0 ? '<button type="button" class="vr-x" data-ortweg aria-label="Lagerort entfernen">✕</button>' : '<span class="vr-x vr-x-leer"></span>') + '</li>'; }).join('') + '</ul>' +
    '<div class="vr-pm"><span class="vr-ein"><input type="text" id="vr-ortneu" placeholder="z. B. Keller, Garage, Speisekammer" maxlength="30"></span><button type="button" class="vr-knopf" data-ortneu>Hinzufügen</button></div>' +
    '<p class="vr-klein">„gekühlt“ und „gefroren“ zählen bei Stromausfall wie Kühlschrank bzw. Gefriertruhe (nur Tag 1 bzw. Tag 1–2).</p></div></details>';
}
function eigenFormHTML() {
  return '<div class="vr-eigen"><div class="vr-felder">' + feld('Name', '<span class="vr-ein"><input type="text" data-ef="n" maxlength="50" placeholder="z. B. Bohnensuppe vom Markt"></span>', 'vr-voll') +
    feld('Gruppe', '<select data-ef="g">' + GRUPPEN.map(function (g) { return '<option value="' + g.k + '">' + esc(g.kurz) + '</option>'; }).join('') + '</select>') +
    feld('kcal je 100 g', zahlIn('data-ef="k"', '', 'kcal', 'Etikett')) + feld('Eiweiß je 100 g', zahlIn('data-ef="e"', '', 'g')) + feld('Fett je 100 g', zahlIn('data-ef="f"', '', 'g')) + feld('Kohlenhydrate je 100 g', zahlIn('data-ef="c"', '', 'g')) +
    feld('Packungsgröße', zahlIn('data-ef="pg"', '', 'g', 'freiwillig')) + feld('Ohne Kochen essbar?', seg('ef:ko', [['0', 'Ja'], ['1', 'Nein']], '0')) + '</div>' +
    '<div class="vr-knoepfe"><button type="button" class="vr-knopf vr-haupt" data-eigen-neu>Anlegen und ins Lager</button></div></div>';
}

/* ---------- 3. Reichweite ---------- */
function kursSVG(V, ziel, von, schwelle) {
  var W = Math.max(330, Math.min(900, ((R && R.clientWidth) || 700) - 64)), Hh = W < 500 ? 220 : 240, pl = 34, pr = 12, pt = 14, pb = 26, P = V.filter(function (p) { return p[0] >= von; }); if (P.length < 2) P = V.slice(-2);
  var x0 = P[0][0], x1 = Math.max(P[P.length - 1][0], x0 + 1), ymax = Math.max(schwelle != null ? 110 : 1, Math.max.apply(null, P.map(function (p) { return p[1]; })) * 1.05);
  var X = function (x) { return pl + (x - x0) / (x1 - x0) * (W - pl - pr); }, Y = function (y) { return pt + (1 - y / ymax) * (Hh - pt - pb); };
  var d = P.map(function (p, i) { return (i ? 'L' : 'M') + X(p[0]).toFixed(1) + ',' + Y(p[1]).toFixed(1); }).join('');
  var st = Math.pow(10, Math.floor(Math.log10(ymax))) || 1; if (ymax / st < 3) st /= 2; if (ymax / st > 8) st *= 2;
  var g = ''; for (var v = 0; v <= ymax; v += st) g += '<line x1="' + pl + '" x2="' + (W - pr) + '" y1="' + Y(v).toFixed(1) + '" y2="' + Y(v).toFixed(1) + '" class="vr-gl"/><text x="' + (pl - 6) + '" y="' + (Y(v) + 4).toFixed(1) + '" class="vr-ax" text-anchor="end">' + fz(v, st < 1 ? 1 : 0) + '</text>';
  var xs = Math.max(1, Math.ceil((x1 - x0) / 6)); for (var t = Math.ceil(x0); t <= x1; t += xs) g += '<text x="' + X(t).toFixed(1) + '" y="' + (Hh - 8) + '" class="vr-ax" text-anchor="middle">' + 'Tag ' + t + '</text>';
  if (ziel >= x0 && ziel <= x1) g += '<line x1="' + X(ziel).toFixed(1) + '" x2="' + X(ziel).toFixed(1) + '" y1="' + pt + '" y2="' + (Hh - pb) + '" class="vr-ziel"/><text x="' + (X(ziel) + 4).toFixed(1) + '" y="' + (pt + 10) + '" class="vr-ax vr-zt">Ziel ' + ziel + ' T.</text>';
  if (schwelle != null && schwelle <= ymax) g += '<line x1="' + pl + '" x2="' + (W - pr) + '" y1="' + Y(schwelle).toFixed(1) + '" y2="' + Y(schwelle).toFixed(1) + '" class="vr-schwelle"/>';
  var hi = P.reduce(function (a, p) { return p[1] > a[1] ? p : a; }, P[0]);
  return '<svg viewBox="0 0 ' + W + ' ' + Hh + '" class="vr-kurs-svg" role="img" aria-label="Tagesdeckung in Prozent über die Tage">' + g +
    '<path d="' + d + 'L' + X(P[P.length - 1][0]).toFixed(1) + ',' + Y(0).toFixed(1) + 'L' + X(P[0][0]).toFixed(1) + ',' + Y(0).toFixed(1) + 'Z" class="vr-flaeche"/><path d="' + d + '" class="vr-linie"/>' +
    '<circle cx="' + X(hi[0]).toFixed(1) + '" cy="' + Y(hi[1]).toFixed(1) + '" r="4" class="vr-punkt"/></svg>';
}
function kursHTML(A, z) {
  var V = []; A.tage.forEach(function (t) { V.push([t.d, Math.min(1.5, t.deckung) * 100]); }); if (V.length < 2) return '';
  var von = OFFEN.kz || 0, erst = V[0][1], letzt = V[V.length - 1], hoch = V.reduce(function (a, p) { return p[1] > a[1] ? p : a; }, V[0]), tief = V.reduce(function (a, p) { return p[1] < a[1] ? p : a; }, V[0]);
  var ch = letzt[1] - erst, sz = 0; V.forEach(function (p) { sz += Math.min(100, p[1]); });
  return '<div class="vr-karte vr-kurs"><div class="vr-kk"><span class="vr-fl">Wie gut ist jeder Tag gedeckt? (Mahlzeiten aus dem Lager)</span><div class="vr-kw"><b>' + fz(erst) + ' %</b> <small>Tag 1</small></div>' +
    '<div class="vr-kc ' + (ch < 0 ? 'vr-schlecht' : 'vr-plus') + '">' + (ch < 0 ? '▼ ' : '▲ ') + fz(Math.abs(ch)) + ' Punkte bis Tag ' + letzt[0] + '</div></div>' + kursSVG(V, z, von, 90) +
    '<div class="vr-kz" role="group" aria-label="Zeitraum">' + [[0, 'Alle'], [Math.max(0, letzt[0] - 10), 'Letzte 10 T.']].map(function (b) { return '<button type="button" data-kz="' + b[0] + '" aria-pressed="' + (von === b[0]) + '">' + b[1] + '</button>'; }).join('') + '</div>' +
    '<div class="vr-stats"><div><small>▲ Hoch</small><b>' + fz(hoch[1]) + ' % · Tag ' + hoch[0] + '</b></div><div><small>▼ Tief</small><b>' + fz(tief[1]) + ' % · Tag ' + tief[0] + '</b></div><div><small>Ø je Tag</small><b>' + fz(sz / V.length) + ' %</b></div><div><small>Knapp ab</small><b>' + (A.knapp ? 'Tag ' + A.knapp : '–') + '</b></div></div>' +
    '<p class="vr-klein">Gestrichelte Linie: 90 % des Tagesbedarfs. Grundlage ist der Speiseplan-Vorschlag mit der gewählten Kochmöglichkeit.</p></div>';
}
function reichweiteHTML() {
  var h0 = heute(), H = haushalt(S), z = zielTage(S), L = S.lage;
  var h = '<section class="vr-bereich" data-b="reichweite"><h2>Reichweite</h2>';
  if (!H.n) return h + leerText('Noch niemand im Haushalt – lege zuerst Personen an.', '<button type="button" class="vr-knopf vr-haupt" data-tab="haushalt">Zum Haushalt</button>') + '</section>';
  var rwK = reichweite(S, h0), A = alltag(S, h0), W = wasser(S), okA = alltag(S, h0, { koch: 'keine' }), E = eiweissTage(S, h0);
  var rw = { tage: A.max ? 730 : A.reicht }, ok = { tage: okA.max ? 730 : okA.reicht };
  var farbe = function (t) { return t >= z ? 'vr-gut' : t >= Math.min(3, z) ? 'vr-mittel' : 'vr-schlecht'; };
  var zuerst = W.leitung ? 'essen' : (W.tage < rw.tage ? 'wasser' : 'essen');
  h += '<p class="vr-unter">Für ' + H.n + (H.n === 1 ? ' Person' : ' Personen') + ', ' + fz(H.kcalSpar) + ' kcal am Tag' + (H.spar < 100 ? ' (Ration ' + H.spar + ' %)' : '') + ' · Ziel ' + z + ' Tage · ' + (L.strom ? 'Strom weg' : 'Strom da') + ' · ' + KOCHT[L.koch] + '</p>';
  if (!S.lager.length) h += leerText('Noch nichts im Lager – trage unter „Lager“ ein, was du hast.', '<button type="button" class="vr-knopf vr-haupt" data-tab="lager">Zum Lager</button>');
  h += '<div class="vr-gross"><div class="vr-karte ' + farbe(rw.tage) + '"><span class="vr-fl">Essen reicht</span><b class="vr-gz">' + (A.max ? '90+' : tageZahl(rw.tage)) + '</b><span class="vr-ge">' + (Math.floor(rw.tage) === 1 ? 'Tag' : 'Tage') + '</span>' + balken(rw.tage, z) + '<small>Ziel ' + z + ' Tage' + (A.rest >= 0.5 ? ' · danach Reste für ca. ' + fz(A.rest, 1) + ' Tage' : '') + '</small><small class="vr-rechn">rechnerisch nach Kalorien: ' + tageText(rwK.tage) + '</small></div>' +
    '<div class="vr-karte ' + (W.leitung ? 'vr-gut' : farbe(W.tage)) + '"><span class="vr-fl">Wasser reicht</span>' + (W.leitung ? '<b class="vr-gz vr-gz-t">Leitung läuft</b><span class="vr-ge">Vorrat ' + liter(W.l) + ' als Reserve</span>' : '<b class="vr-gz">' + tageZahl(W.tage) + '</b><span class="vr-ge">' + (W.tage === 1 ? 'Tag' : 'Tage') + '</span>' + balken(W.tage, z)) + '<small>' + liter(W.l) + ' da · ' + liter(W.bedarf) + ' am Tag</small></div></div>';
  if (S.lager.length && H.kcal > 0) h += '<p class="vr-zuerst ' + (zuerst === 'wasser' ? 'vr-warn' : '') + '">' + (W.leitung ? 'Solange Leitungswasser kommt, begrenzt das Essen.' : zuerst === 'wasser' ? '<b>Zuerst geht das Wasser aus</b> – nach ' + tageText(W.tage) + '. Wasser ist wichtiger als Essen.' : '<b>Zuerst geht das Essen aus</b> – nach ' + tageText(rw.tage) + '.') + '</p>';
  if (S.lager.length && H.kcal > 0) h += '<p class="vr-klein">„Essen reicht“ zählt die Tage, an denen sich aus dem Lager mit der Kochmöglichkeit „' + KOCHT[L.koch] + '“ echte Mahlzeiten für alle machen lassen (mindestens 90 % des Bedarfs). „Rechnerisch nach Kalorien“ zählt alle Kalorien im Lager – auch Öl, Zucker oder Mehl, die sich ohne passende Zutaten nicht zu Mahlzeiten machen lassen.</p>';
  h += kursHTML(A, z);
  h += '<div class="vr-kacheln"><div class="vr-karte"><span class="vr-fl">Ganz ohne Kochen</span><b>' + tageText(ok.tage) + '</b><small>nur mit Essen, das kalt geht</small></div>' +
    '<div class="vr-karte"><span class="vr-fl">Eiweiß reicht</span><b>' + tageText(E.tage) + '</b><small>' + fz(E.g) + ' g da · ' + fz(E.bedarf) + ' g am Tag</small></div>' +
    '<div class="vr-karte"><span class="vr-fl">Energie im Lager</span><b>' + fz(rwK.start) + ' kcal</b><small>davon nutzbar mit ' + KOCHT[L.koch] + '</small></div>' +
    (L.strom && rwK.verloren > 1 ? '<div class="vr-karte vr-schlecht"><span class="vr-fl">Geht verloren</span><b>' + fz(rwK.verloren) + ' kcal</b><small>Kühl-/Gefriergut, das nicht rechtzeitig gegessen wird</small></div>' : '') + '</div>';
  /* Gruppen nach BLE-Tabelle */
  var G = gruppenStand(S, h0);
  h += '<h3>Vorrat nach Lebensmittelgruppen</h3><div class="vr-karte"><ul class="vr-gruppen" role="list">' + GRUPPEN.filter(function (g) { return g.ble; }).map(function (g) { var r = G[g.k], p = r.ziel ? r.ist / r.ziel : 0;
    return '<li><span class="vr-gn">' + g.i + ' ' + esc(g.kurz) + '</span><span class="vr-gw">' + kg(r.ist) + ' <small>von ' + kg(r.ziel) + '</small></span>' + balken(r.ist, r.ziel, p >= 1 ? 'vr-gut' : p >= 0.5 ? 'vr-mittel' : 'vr-schlecht') + '</li>'; }).join('') +
    '<li><span class="vr-gn">💧 Getränke</span><span class="vr-gw">' + liter(W.l) + ' <small>von ' + liter(W.bedarf * z) + '</small></span>' + balken(W.l, W.bedarf * z, W.l >= W.bedarf * z ? 'vr-gut' : 'vr-mittel') + '</li></ul>' +
    '<p class="vr-klein">Ziel nach der Vorratstabelle der BLE (je Person für 10 Tage bei 2.200 kcal), umgerechnet auf euren Bedarf (' + fz(H.kcal) + ' kcal) und ' + z + ' Tage. Trockene Hülsenfrüchte und Milchpulver werden über den Energiegehalt auf die Menge der Tabelle umgerechnet. Richtwert.</p></div>';
  /* Strom weg: zuerst essen */
  var X = posten(S, h0);
  if (L.strom) { var K = X.filter(function (x) { return x.ort === 'k' || x.ort === 't'; }).sort(function (a, b) { return rang(a, true) - rang(b, true); });
    h += '<h3>Zuerst essen</h3><div class="vr-karte">' + (K.length ? '<ul class="vr-liste-k" role="list">' + K.map(function (x) { return '<li><span>' + (x.ort === 'k' ? '❄︎ Kühlschrank' : '🧊 Gefriertruhe') + '</span><b>' + esc(x.k.n) + '</b><small>' + kg(x.g) + '</small></li>'; }).join('') + '</ul>' : '<p class="vr-klein">Nichts im Kühlschrank oder in der Gefriertruhe eingetragen.</p>') +
      '<p class="vr-klein">Ohne Strom hält ein geschlossener Kühlschrank je nach Füllung etwa 4–6 Stunden kalt, ein Gefriergerät oft bis zu 48 Stunden (Verbraucherzentrale Niedersachsen). Darum zählt die Rechnung Kühlware nur am 1. Tag und Gefriergut nur an den ersten 2 Tagen.</p></div>'; }
  /* läuft ab */
  var AB = X.filter(function (x) { return x.rest != null && x.rest <= z; }).sort(function (a, b) { return a.rest - b.rest; }), SP = rwK.spaet;
  if (AB.length || SP.length) h += '<h3>Läuft bald ab</h3><div class="vr-karte"><ul class="vr-liste-k" role="list">' + AB.map(function (x) { return '<li><span>' + (x.rest < 0 ? 'abgelaufen' : 'in ' + x.rest + ' T.') + '</span><b>' + esc(x.k.n) + '</b><small>' + mhdText(x.it.mhd) + (SP.indexOf(x.it.u) >= 0 ? ' · wird erst später gegessen' : '') + '</small></li>'; }).join('') + '</ul>' +
    '<p class="vr-klein">Nach dem Mindesthaltbarkeitsdatum ist vieles noch gut – erst prüfen (Aussehen, Geruch, Geschmack). Mehr unter „Haltbarkeit“.</p></div>';
  /* Brennstoff */
  var kart = zahl(L.kartusche);
  if (L.koch === 'gas') { var PL = { brennMin: 0 }; A.tage.slice(0, z).forEach(function (t) { PL.brennMin += t.brenn; });
    h += '<h3>Gaskartuschen (Schätzung)</h3><div class="vr-karte">' + (isFinite(kart) && kart > 0 ? '<p>Der Speiseplan-Vorschlag für ' + Math.min(z, A.tage.length) + ' Tage braucht etwa <b>' + fz(PL.brennMin) + ' Minuten</b> Flamme. Bei ' + fz(kart) + ' Minuten je Kartusche sind das etwa <b>' + Math.ceil(PL.brennMin / kart) + ' Kartuschen</b>.</p>' : '<p class="vr-klein">Trage unter „Haushalt → Lage“ die Brenndauer einer Kartusche ein (steht auf der Packung). Dann schätzt der Planer, wie viele Kartuschen der Speiseplan braucht.</p>') +
      '<p class="vr-klein">Schätzung aus den Kochzeiten der Gerichte – Wind, Kälte, Topfgröße und Deckel ändern viel. Campingkocher mit Kartusche nur im Freien benutzen, außer sie sind für Innenräume zugelassen (BBK).</p></div>'; }
  var baby = X.filter(function (x) { return x.k.g === 'baby'; });
  if (baby.length) h += '<p class="vr-klein">Babynahrung (' + baby.length + ' Posten) zählt nicht zur Reichweite der anderen – sie ist für das Baby reserviert.</p>';
  return h + '</section>';
}

/* ---------- 4. Gerichte ---------- */
function reichtFuer(max, PH, n) {
  if (PH > 0 && max >= PH) { var mal = Math.floor(max / PH + 1e-9); return 'reicht für ' + n + (n === 1 ? ' Person' : ' Personen') + ' (' + fz(PH, 1) + ' Port.)' + (mal >= 2 ? ' · ' + (mal > 20 ? '20+' : mal) + '×' : ''); }
  return fz(max, 1) + ' Port. – nicht für alle';
}
function gerichtHTML(r, st, B) {
  var wv = gerichtWerte(S, r), H = haushalt(S), PH = portionenHaushalt(S), open = OFFEN['g:' + r.id];
  var badge = !st.koch ? '<span class="vr-badge vr-grau">braucht ' + KNAME[r.koch] + '</span>' : st.st === 'geht' ? '<span class="vr-badge vr-gut">geht jetzt · ' + reichtFuer(st.max, PH, H.n) + '</span>' : st.st === 'fast' ? '<span class="vr-badge vr-mittel">fast</span>' : '<span class="vr-badge vr-grau">fehlt einiges</span>';
  var h = '<article class="vr-karte vr-gericht" data-g="' + r.id + '"><button type="button" class="vr-gk" data-auf="g:' + r.id + '" aria-expanded="' + !!open + '"><span class="vr-gi" aria-hidden="true">' + ({ kalt: '🥣', warm: '🍲', brot: '🫓', ofen: '🍞', kiste: '🧺' })[r.art] + '</span><span class="vr-gtx"><b>' + esc(r.n) + '</b><small>' + fz(wv.kcal) + ' kcal · ' + (r.wa ? fz(wv.wasser) + ' ml Wasser' : 'ohne Wasser') + ' · ' + r.z + ' min · ' + KNAME[r.koch] + '</small></span>' + badge + '</button>';
  if (st.st === 'fast' && st.koch) h += '<p class="vr-fehlt">Fehlt: ' + st.fehlt.map(function (f) { return esc(zutatName(S, f.z)) + ' (' + kg(f.g) + ')'; }).join(', ') + '</p>';
  if (open) {
    h += '<div class="vr-gd"><h4>Zutaten für ' + r.p + ' ' + (r.p === 1 ? 'Portion' : 'Portionen') + '</h4><ul class="vr-zut">' + r.zut.map(function (z) { var da = zutatDa(z, B), ok = da >= z.g / r.p;
      return '<li class="' + (ok ? 'vr-da' : 'vr-nicht') + '"><span aria-hidden="true">' + (ok ? '✓' : '○') + '</span>' + fz(z.g) + ' g ' + esc(zutatName(S, z)) + (z.a.some(function (a) { return a[1] !== 1; }) ? ' (Frischhefe: dreifache Menge)' : '') + (z.opt ? ' <small>(nach Belieben)</small>' : '') + '</li>'; }).join('') + '<li class="vr-da"><span aria-hidden="true">·</span>Salz, Pfeffer, Gewürze nach Geschmack</li>' + (r.wa ? '<li><span aria-hidden="true">💧</span>' + fz(r.wa) + ' ml Wasser (Kochen und Teig)</li>' : '') + '</ul>' +
      '<h4>So geht es</h4><ol class="vr-schritte">' + r.sch.map(function (s) { return '<li>' + esc(s) + '</li>'; }).join('') + '</ol>' + (r.hinweis ? '<p class="vr-warn">' + esc(r.hinweis) + '</p>' : '') +
      (r.art === 'kiste' ? '<p class="vr-klein">Kochkiste: kurz ankochen, im fest verschlossenen Topf in einer gut isolierten Kiste ohne weitere Energie nachgaren (BZfE, „Energie sparen mit der Kochkiste“, Stand 03.01.2023)' + (r.beleg === 'kk-geeignet' ? '; die Zeit in der Kiste ist nicht belegt – vor dem Essen prüfen, ob es gar ist. Die Flammzeit ist geschätzt.' : '.') + ' Mehr unter „Notfall → Kochen ohne Strom“.</p>' : '') +
      (r.rz ? '<p><a class="vr-link" href="#r-' + r.rz + '">Ausführliches Rezept in der App öffnen ›</a></p>' : '') +
      '<p class="vr-klein">' + fz(wv.kcal) + ' kcal und ' + fz(wv.eiweiss) + ' g Eiweiß je Portion, gerechnet aus dem Katalog (erste genannte Zutat). 1 Portion = Mahlzeit für jemanden mit 2.200 kcal Tagesbedarf; euer Haushalt braucht ' + portText(PH) + ' je Mahlzeit (Kinder und Menschen mit kleinem Bedarf entsprechend weniger). Richtwert.</p>' +
      (st.max >= 0.5 ? '<div class="vr-koch"><span class="vr-fl">Gekocht für</span><div class="vr-pm"><button type="button" class="vr-rund" data-port="-0.5" aria-label="weniger Portionen">−</button><b class="vr-port" data-portw="' + Math.min(PH, st.max) + '" data-max="' + st.max + '">' + fz(Math.min(PH, st.max), 1) + '</b><button type="button" class="vr-rund" data-port="0.5" aria-label="mehr Portionen">＋</button></div><span class="vr-klein vr-portinfo">' + (st.max >= PH ? 'Portionen = alle ' + H.n + ' Personen' : 'reicht nicht für alle') + '</span><button type="button" class="vr-knopf vr-haupt" data-gekocht="' + r.id + '">Gekocht – vom Lager abziehen</button></div>' : '') + '</div>';
  }
  return h + '</article>';
}
function gerichteHTML() {
  var h0 = heute(), B = bestand(S, h0), L = S.lage;
  var h = '<section class="vr-bereich" data-b="gerichte"><h2>Was kann ich kochen und backen?</h2><p class="vr-unter">' + GERICHTE.length + ' einfache Vorratsgerichte, abgeglichen mit deinem Lager. Kochstelle: <b>' + KOCHT[L.koch] + '</b> (ändern unter „Haushalt → Lage“).</p>';
  h += '<div class="vr-filter">' + seg('gf:st', [['alle', 'Alle'], ['geht', 'Geht jetzt'], ['fast', 'Fast']], GF.st) + seg('gf:art', ARTEN, GF.art, 'vr-seg-wrap') +
    '<div class="vr-chips"><button type="button" class="vr-chip" data-gf-t="meine" aria-pressed="' + GF.meine + '">Nur meine Kochstelle</button><button type="button" class="vr-chip" data-gf-t="ohneW" aria-pressed="' + GF.ohneW + '">Ohne Wasser</button></div></div>';
  h += '<div class="vr-knoepfe"><button type="button" class="vr-knopf vr-haupt" data-plan>📋 Speiseplan-Vorschlag für ' + zielTage(S) + ' Tage</button></div><div class="vr-plan-ort">' + (PLAN ? planHTML() : '') + '</div>';
  var L2 = GERICHTE.map(function (r) { return { r: r, st: gerichtStatus(S, r, B) }; }).filter(function (x) {
    if (GF.meine && !x.st.koch) return false; if (GF.ohneW && x.r.wa > 0) return false; if (GF.art !== 'alle' && x.r.art !== GF.art) return false;
    if (GF.st === 'geht' && x.st.st !== 'geht') return false; if (GF.st === 'fast' && x.st.st !== 'fast') return false; return true; });
  var ord = { geht: 0, fast: 1, fehlt: 2 }; L2.sort(function (a, b) { return (a.st.koch ? 0 : 3) + ord[a.st.st] - (b.st.koch ? 0 : 3) - ord[b.st.st]; });
  var gruppe = function (key, titel, M, auf) { if (!M.length) return ''; var o = OFFEN['gl:' + key] != null ? OFFEN['gl:' + key] : auf;
    return '<details class="vr-glgr" data-gl="' + key + '"' + (o ? ' open' : '') + '><summary>' + titel + ' <span>' + M.length + '</span></summary><div class="vr-gliste">' + M.map(function (x) { return gerichtHTML(x.r, x.st, B); }).join('') + '</div></details>'; };
  var Lg = L2.filter(function (x) { return x.st.koch && x.st.st === 'geht'; }), Lf = L2.filter(function (x) { return x.st.koch && x.st.st === 'fast'; }), Lr = L2.filter(function (x) { return !x.st.koch || x.st.st === 'fehlt'; });
  h += L2.length ? gruppe('geht', 'Geht jetzt', Lg, true) + gruppe('fast', 'Fast – es fehlt nur wenig', Lf, GF.st === 'fast' || !Lg.length) + gruppe('rest', 'Fehlt mehr oder andere Kochstelle', Lr, false) : leerText(S.lager.length ? 'Mit diesen Filtern passt kein Gericht. Tippe auf „Alle“ oder ändere die Kochstelle.' : 'Noch nichts im Lager – dann kann auch nichts passen. Trage unter „Lager“ ein, was du hast.');
  return h + '</section>';
}
function planZiel() { var h0 = heute(), z = zielTage(S), D = haushalt(S).kcalSpar, sp = (S.plan || {}).modus === 'sparsam';
  var A = sp ? planSparsam(S, h0, z) : alltag(S, h0), T = A.tage.slice(0, z);
  while (T.length < z && T.length) T.push({ d: T.length + 1, essen: [], extra: [], kcal: 0, deckung: 0, luecke: D, brenn: 0 });
  var knapp = 0; T.forEach(function (t) { if (!knapp && t.deckung < (sp ? A.anteil * 0.9 : 0.9)) knapp = t.d; });
  return { tage: T, knapp: knapp, PH: A.PH, sparsam: sp, anteil: A.anteil || 1 }; }
function planHTML() {
  var P = PLAN, z = P.tage.length;
  if (!z) return leerText('Für einen Speiseplan braucht es Personen und Vorrat.');
  return '<div class="vr-karte vr-plan"><div class="vr-kh"><h3>Speiseplan-Vorschlag</h3><button type="button" class="vr-x" data-plan-zu aria-label="Speiseplan schließen">✕</button></div>' +
    seg('plan:modus', [['satt', 'Satt (100 %)'], ['sparsam', 'Sparsam strecken']], P.sparsam ? 'sparsam' : 'satt') +
    (P.sparsam ? '<p class="vr-warn">Sparsam: jeden Tag etwa <b>' + fz(P.anteil * 100) + ' %</b> des Bedarfs, damit der Vorrat gleichmäßiger über ' + z + ' Tage reicht (nie unter 60 %). Nur kurz und nur für gesunde Erwachsene – nicht für Kinder, Schwangere, Stillende, Kranke oder Ältere. Wasser nie kürzen.</p>' : '') +
    '<p class="' + (P.knapp ? 'vr-warn' : 'vr-ok') + '">' + (P.knapp ? 'Ab <b>Tag ' + P.knapp + '</b> wird es knapp (' + (P.sparsam ? 'weniger als geplant' : 'weniger als 90 % des Tagesbedarfs') + ').' : P.sparsam ? 'So reicht der Vorrat gleichmäßig für alle ' + z + ' Tage.' : 'Der Vorrat deckt alle ' + z + ' Tage.') + '</p>' +
    '<ol class="vr-plantage">' + P.tage.map(function (t) { return '<li class="' + (t.deckung < 0.9 ? 'vr-knapp' : '') + '"><div class="vr-pt"><b>Tag ' + t.d + '</b><span>' + fz(Math.min(999, t.deckung * 100)) + ' %</span></div>' + balken(t.deckung, 1, t.deckung >= 0.9 ? 'vr-gut' : t.deckung >= 0.6 ? 'vr-mittel' : 'vr-schlecht') +
      '<ul>' + t.essen.map(function (e) { return '<li><span class="vr-mz">' + (MZN[e.mz] || '') + '</span>' + esc(e.n) + ' <small>· ' + fz(e.port, 1) + ' Port.</small></li>'; }).join('') + (t.extra.length ? '<li class="vr-klein">dazu: ' + t.extra.map(function (x) { return esc(x.n.replace(/ \(.*\)$/, '')) + ' ' + kg(x.g); }).join(', ') + '</li>' : '') + (!t.essen.length && !t.extra.length ? '<li class="vr-klein">nichts mehr da</li>' : '') + (t.luecke > 0.1 * haushalt(S).kcalSpar ? '<li class="vr-luecke">Lücke: ' + fz(Math.round(t.luecke / 10) * 10) + ' kcal</li>' : '') + '</ul></li>'; }).join('') + '</ol>' +
    '<p class="vr-klein">Frühstück, Mittag, Abend und eine kalte Zwischenmahlzeit (Richtwert 25 · 35 · 30 · 10 % des Tagesbedarfs). Zuerst Kühlschrank und Gefriertruhe, dann was bald abläuft; möglichst Abwechslung. Portionen nach Bedarf (Haushalt: ' + portText(P.PH) + ' = eine normale Mahlzeit für alle). Lücken werden nur mit pur Essbarem (Brot, Flocken, Obst, Nüsse, Milchprodukte, Süßes – keine Gemüse- oder Fleischkonserven pur) in alltagsnahen Mengen gefüllt – was dann fehlt, steht als Lücke da. Derselbe Plan liegt der Zahl „Essen reicht“ zugrunde. Er ändert das Lager nicht – erst „Gekocht“ zieht ab.</p></div>';
}

/* ---------- 5. Fehlt noch ---------- */
function fehltHTML() {
  var h0 = heute(), F = fehltListe(S, h0), B = bestand(S, h0), H = haushalt(S);
  var h = '<section class="vr-bereich" data-b="fehlt"><h2>Fehlt noch</h2><p class="vr-unter">Was fehlt bis zum Ziel von <b>' + F.ziel + ' Tagen</b>?</p>';
  if (!H.n) return h + leerText('Lege zuerst unter „Haushalt“ Personen an.') + '</section>';
  var A = alltag(S, h0), fehltT = A.max ? 0 : Math.max(0, F.ziel - Math.floor(A.reicht + 1e-9));
  h += '<div class="vr-kacheln"><div class="vr-karte ' + (fehltT > 0 ? 'vr-mittel' : 'vr-gut') + '"><span class="vr-fl">Essen</span><b>' + (fehltT > 0 ? 'noch ' + fehltT + (fehltT === 1 ? ' Tag' : ' Tage') : 'reicht') + '</b><small>' + (fehltT > 0 ? '≈ ' + fz(fehltT * H.kcal) + ' kcal als Mahlzeiten · rechnerisch nach Kalorien fehlen ' + (F.kcal > 0 ? fz(F.kcal / H.kcal, 1) + ' Tagesrationen' : 'keine') : 'für das Ziel') + '</small></div>' +
    '<div class="vr-karte ' + (F.wasserL > 0 ? 'vr-mittel' : 'vr-gut') + '"><span class="vr-fl">Wasser</span><b>' + (F.wasserL > 0 ? 'noch ' + liter(F.wasserL) : (S.lage.leitung ? 'Leitung läuft' : 'reicht')) + '</b><small>' + (F.wasserL > 0 ? '≈ ' + Math.ceil(F.wasserL / 1.5) + ' Flaschen à 1,5 l' : 'Ziel ' + liter(F.wasserZiel)) + '</small></div></div>';
  var liste = [], NK = nachkauf(S);
  h += HAKEN.fehltOben.map(function (f) { return f(); }).join('');
  if (NK.length) { var nkSum = 0, nkOhne = 0; NK.forEach(function (x) { if (x.kosten != null) nkSum += x.kosten; else nkOhne++; });
    h += '<h3>Nachkaufen (unter Mindestbestand)</h3><div class="vr-karte"><ul class="vr-fl-liste" role="list">' + NK.map(function (x) { liste.push(x.k.n + ': ' + x.anzahl + ' × ' + x.einheit.replace(/ \(.*\)$/, ''));
      return '<li><b><i class="vr-amp vr-amp-rot"></i>' + esc(x.k.n) + '</b><small>' + x.anzahl + ' × ' + esc(x.einheit.replace(/ \(.*\)$/, '')) + (x.kosten != null ? ' · ca. ' + fz(x.kosten, 2) + ' €' : '') + '</small></li>'; }).join('') + '</ul>' +
      (nkSum ? '<p class="vr-klein">Zusammen ca. <b>' + fz(nkSum, 2) + ' €</b>' + (nkOhne ? ' (ohne ' + nkOhne + ' Posten ohne Preis)' : '') + ' – nach deinen eigenen Preisen.</p>' : '') + '</div>'; }
  if (F.gruppen.length) { h += '<h3>Nach Lebensmittelgruppen</h3><div class="vr-karte"><ul class="vr-fl-liste" role="list">' + F.gruppen.map(function (x) { var v = vorschlag(S, x.g.k, x.gap); liste.push(x.g.kurz + ': noch ' + kg(x.gap) + ' – z. B. ' + v.join(' + '));
    return '<li><b>' + x.g.i + ' ' + esc(x.g.kurz) + ': noch ' + kg(x.gap) + '</b><small>z. B. ' + esc(v.join(' + ')) + '</small>' + balken(x.ist, x.ziel, 'vr-mittel') + '</li>'; }).join('') + '</ul><p class="vr-klein">Nach der Vorratstabelle der BLE, umgerechnet auf euren Bedarf. Vorschläge sind Beispiele – nimm, was ihr gern esst.</p></div>'; }
  else if (S.lager.length) h += '<p class="vr-ok">Alle Lebensmittelgruppen sind für ' + F.ziel + ' Tage gut gefüllt.</p>';
  if (F.wasserL > 0) liste.push('Wasser: noch ' + liter(F.wasserL));
  /* fehlende Zutaten der „fast“-Gerichte */
  var Z = {}; GERICHTE.forEach(function (r) { var st = gerichtStatus(S, r, B); if (st.st !== 'fast' || !st.koch) return; st.fehlt.forEach(function (f) { var k = zutatName(S, f.z); Z[k] = Z[k] || { g: 0, r: [] }; Z[k].g = Math.max(Z[k].g, f.g * Math.max(1, H.n)); Z[k].r.push(r.n); }); });
  var ZK = Object.keys(Z).sort(function (a, b) { return Z[b].r.length - Z[a].r.length; }), ZN = ZK.length; ZK = ZK.slice(0, 12);
  if (ZK.length) { h += '<h3>Damit mehr Gerichte gehen</h3><div class="vr-karte"><ul class="vr-fl-liste" role="list">' + ZK.map(function (k) { liste.push(k + ' (für ' + Z[k].r.length + ' Gerichte)'); return '<li><b>' + esc(k) + '</b><small>für ' + esc(Z[k].r.slice(0, 3).join(', ')) + (Z[k].r.length > 3 ? ' …' : '') + '</small></li>'; }).join('') + '</ul>' + (ZN > ZK.length ? '<p class="vr-klein">Die ' + ZK.length + ' wichtigsten von ' + ZN + ' fehlenden Zutaten – alle stehen unter „Gerichte → Fast“.</p>' : '') + '</div>'; }
  /* Abhak-Liste BBK */
  var n = 0, d = 0; CHECK.forEach(function (c) { c[1].forEach(function (t) { n++; if (S.haken[t]) d++; }); });
  h += '<h3>Alles außer Essen <small class="vr-zaehl">' + d + ' von ' + n + '</small></h3><div class="vr-karte">' + balken(d, n, 'vr-gut') + CHECK.map(function (c) {
    return '<fieldset class="vr-check"><legend>' + esc(c[0]) + '</legend>' + c[1].map(function (t) { if (!S.haken[t]) liste.push(t); return '<label><input type="checkbox" data-haken="' + esc(t) + '"' + (S.haken[t] ? ' checked' : '') + '><span>' + esc(t) + '</span></label>'; }).join('') + '</fieldset>'; }).join('') +
    '<p class="vr-klein">Nach den Checklisten im BBK-Ratgeber „Vorsorgen für Krisen und Katastrophen“. Haken bleiben auf diesem Gerät gespeichert.</p></div>';
  OFFEN.liste = liste;
  h += '<div class="vr-knoepfe"><button type="button" class="vr-knopf vr-haupt" data-liste="kopie">Liste kopieren</button>' + (typeof navigator !== 'undefined' && navigator.share ? '<button type="button" class="vr-knopf" data-liste="teilen">Teilen</button>' : '') + '</div>';
  return h + '</section>';
}

/* ---------- 6. Haltbarkeit ---------- */
function haltbarHTML() {
  var h0 = heute(), X = posten(S, h0);
  var K = [['ab', 'Abgelaufen', function (x) { return x.rest != null && x.rest < 0; }], ['30', 'In weniger als 30 Tagen', function (x) { return x.rest != null && x.rest >= 0 && x.rest < 30; }], ['90', 'In 30 bis 90 Tagen', function (x) { return x.rest != null && x.rest >= 30 && x.rest < 90; }], ['gut', 'Länger als 90 Tage', function (x) { return x.rest != null && x.rest >= 90; }], ['ohne', 'Ohne Datum', function (x) { return x.rest == null; }]];
  var h = '<section class="vr-bereich" data-b="haltbar"><h2>Haltbarkeit</h2><p class="vr-unter">Dein Lager nach Mindesthaltbarkeitsdatum (MHD) – das Älteste zuerst verbrauchen.</p>';
  if (!X.length) h += leerText('Noch nichts im Lager.');
  else h += '<div class="vr-karte">' + K.map(function (k) { var G = X.filter(k[2]).sort(function (a, b) { return (a.rest == null ? 1e9 : a.rest) - (b.rest == null ? 1e9 : b.rest); }); if (!G.length) return '';
    return '<h3 class="vr-hk vr-hk-' + k[0] + '">' + k[1] + ' <span>' + G.length + '</span></h3><ul class="vr-liste-k" role="list">' + G.map(function (x) { return '<li><span>' + (x.it.mhd ? mhdText(x.it.mhd) : (x.k.ht || '–')) + '</span><b>' + esc(x.k.n) + '</b><small>' + ORT[x.ort] + '</small></li>'; }).join('') + '</ul>'; }).join('') + '</div>';
  h += '<div class="vr-info">' +
    '<div class="vr-karte"><h3>MHD oder Verbrauchsdatum?</h3><p><b>Mindesthaltbarkeitsdatum</b> („mindestens haltbar bis“): Bis dahin garantiert der Hersteller Geruch, Geschmack und Nährwert – ungeöffnet und richtig gelagert. Danach ist vieles noch gut: erst ansehen, riechen, probieren.</p><p><b>Verbrauchsdatum</b> („zu verbrauchen bis“): steht auf leicht verderblicher Ware wie Hackfleisch oder frischem Fisch. Danach nicht mehr essen.</p><p class="vr-klein">Nach dem Öffnen gilt das MHD nicht mehr (Verbraucherzentrale).</p></div>' +
    '<div class="vr-karte"><h3>Zuerst rein, zuerst raus</h3><p>Neue Vorräte nach hinten stellen, damit die älteren zuerst benutzt werden (BZfE). So bleibt der Vorrat frisch und nichts verdirbt: im Alltag aus dem Vorrat essen und laufend nachkaufen.</p></div>' +
    '<div class="vr-karte"><h3>Strom weg: Kühlschrank und Gefriertruhe</h3><ul><li>Türen so selten wie möglich öffnen.</li><li>Der geschlossene Kühlschrank hält je nach Füllung etwa <b>4–6 Stunden</b> kalt.</li><li>Ein Gefriergerät hält geschlossen oft <b>bis zu 48 Stunden</b>, besonders wenn es voll ist.</li><li>Steigt die Temperatur von −18 °C auf −12 °C, bleiben die Lebensmittel laut BfR gesundheitlich unbedenklich.</li><li>Aufgetaute gegarte Speisen und rohe pflanzliche Lebensmittel bald verarbeiten; <b>rohe tierische Lebensmittel vollständig durcherhitzen</b>. Angetautes Speiseeis wegwerfen.</li></ul><p class="vr-klein">Verbraucherzentrale Niedersachsen, Stand 04.08.2026.</p></div>' +
    '<div class="vr-karte"><h3>Wasser lagern</h3><ul><li>Mineralwasser hat meist ein MHD von 1 bis 1½ Jahren; ungeöffnet ist es meist deutlich länger gut.</li><li>Glasflaschen eignen sich für lange Lagerung, PET eher für kurze bis mittlere – kühl, dunkel, ohne Sonne.</li><li>Für Säuglingsnahrung Leitungswasser abkochen und auf etwa 30–40 °C abkühlen lassen.</li></ul><p class="vr-klein">Verbraucherzentrale Niedersachsen, Stand 24.09.2026.</p></div>' +
    '<div class="vr-karte"><h3>Warnzeichen – dann wegwerfen</h3><ul><li><b>Verpackung:</b> aufgeblähte Packungen, gewölbte Deckel, eingedrückte Dosen.</li><li><b>Aussehen:</b> Schimmel, Flecken, faule oder schmierige Stellen, Schädlinge.</li><li><b>Geruch:</b> muffig, ranzig, faulig, säuerlich oder ungewohnt.</li><li><b>Geschmack:</b> sauer, ranzig, muffig oder ungewöhnlich bitter.</li></ul><p class="vr-klein">BZfE „Lebensmittelverderb erkennen“, Stand 20.02.2025.</p></div>' +
    '<div class="vr-karte"><h3>Übliche Haltbarkeit ungeöffnet</h3><div class="vr-tab-wrap"><table class="vr-tab"><thead><tr><th>Lebensmittel</th><th>Haltbarkeit</th><th>Lagerung</th></tr></thead><tbody>' + HALTB.map(function (r) { return '<tr><td>' + esc(r[0]) + '</td><td>' + esc(r[1]) + '</td><td>' + esc(r[2]) + '</td></tr>'; }).join('') + '</tbody></table></div><p class="vr-klein">Richtwerte nach BLE (ernaehrungsvorsorge.de). Das Datum auf der Packung geht vor.</p></div>' +
    '<div class="vr-karte vr-wichtig"><h3>Besondere Bedürfnisse</h3><ul><li><b>Babys und Kleinkinder:</b> Säuglingsnahrung, Wasser zum Abkochen, Fläschchen, Windeln einplanen.</li><li><b>Wer regelmäßig Medikamente braucht:</b> Vorrat für mindestens 10 Tage (BBK), Haltbarkeit und Lagerung beachten – ggf. Kühlung bei Stromausfall mit Arzt oder Apotheke klären.</li><li><b>Diabetes, Allergien, Unverträglichkeiten, Kranke, Schwangere:</b> Vorrat darauf abstimmen und Fragen mit Arzt oder Apotheke besprechen.</li><li><b>Haustiere:</b> Futter und Wasser mitrechnen.</li></ul><p class="vr-klein">Dieser Planer rechnet mit Richtwerten und ersetzt keine Beratung.</p></div></div>';
  return h + '</section>';
}
function quellenHTML() {
  return '<details class="vr-quellen"><summary>Quellen und Stand</summary><ol>' + QUELLEN.map(function (q) { return '<li><a href="' + esc(q[1]) + '" target="_blank" rel="noopener">' + esc(q[0]) + '</a>' + (q[2] ? '<small> – ' + esc(q[2]) + '</small>' : '') + '</li>'; }).join('') + '</ol>' +
    '<p class="vr-klein">Geprüft im November 2026. Alle Zahlen sind Richtwerte; Kochwasser, Kochzeiten und Packungsgrößen sind übliche Angaben – maßgeblich sind Etikett und Packung.</p></details>';
}

/* ---------- Aufbau und Aktualisieren ---------- */
var BEREICH = { reichweite: reichweiteHTML, haushalt: haushaltHTML, lager: lagerHTML, gerichte: gerichteHTML, fehlt: fehltHTML, haltbar: haltbarHTML };
function zeichnen(rollen) {
  if (!R) return;
  var ort = R.querySelector('.vr-inhalt'), y = window.scrollY;
  ort.innerHTML = (S.beispiel ? '<div class="vr-beispiel"><p><b>Das ist ein Beispiel-Haushalt</b> mit 3 Personen und einem kleinen Lager – zum Ausprobieren.</p><button type="button" class="vr-knopf" data-beispiel-weg>Beispiel löschen</button></div>' : '') + BEREICH[S.tab]();
  R.querySelector('.vr-leiste').innerHTML = leisteInnen();
  HAKEN.nachZeichnen.forEach(function (f) { f(R); });
  if (rollen) { var nb = R.querySelector('.vr-tabs [aria-selected="true"]'); if (nb && nb.scrollIntoView) try { nb.scrollIntoView({ block: 'nearest', inline: 'center' }); } catch (e) { /* alt */ }
    var top = R.querySelector('.vr-leiste').getBoundingClientRect().top + window.scrollY - (parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--qw-oben')) || 0);
    if (window.scrollY > top) window.scrollTo(0, top); }
  else window.scrollTo(0, y);
}
function tab(t) { if (!BEREICH[t] || t === S.tab) return; S.tab = t; OFFEN['g:' + gruppeVon(t)[0]] = t; PLAN = null; sichern(); zeichnen(true); }
function toast(t, undo) {
  var el = R && R.querySelector('.vr-toast'); if (!el) return;
  el.innerHTML = '<span>' + t + '</span>' + (undo ? '<button type="button" data-undo>Rückgängig</button>' : ''); el.hidden = false;
  if (TOAST_T) clearTimeout(TOAST_T); TOAST_T = setTimeout(function () { el.hidden = true; UNDO = null; }, undo ? 8000 : 3500);
}
function nachAenderung(neuZeichnen) { if (S.beispiel) { /* bleibt Beispiel, bis gelöscht */ } sichern(); if (neuZeichnen) zeichnen(false); else R.querySelector('.vr-kurz').innerHTML = kurzZeile(); }
function kopieren(text, ok) {
  var fertig = function () { toast(ok || 'Kopiert.'); };
  if (navigator.clipboard && navigator.clipboard.writeText) { navigator.clipboard.writeText(text).then(fertig, function () { altKopie(text); fertig(); }); } else { altKopie(text); fertig(); }
}
function altKopie(text) { var t = document.createElement('textarea'); t.value = text; t.setAttribute('readonly', ''); t.style.position = 'fixed'; t.style.opacity = '0'; document.body.appendChild(t); t.select(); try { document.execCommand('copy'); } catch (e) { /* alt */ } document.body.removeChild(t); }
function sicherungText() { return JSON.stringify({ app: 'Quellwissen Vorrat', v: 1, datum: new Date().toISOString().slice(0, 10), daten: S }); }
function sicherungLesen(text) {
  try { var x = JSON.parse(String(text || '').trim()); if (x && x.daten) x = x.daten; var n = pruefeStand(x); if (!n) throw new Error('x');
    UNDO = klon(S); S = n; S.beispiel = false; S.tab = BEREICH.uebersicht ? 'uebersicht' : 'reichweite'; sichernJetzt(); PLAN = null; zeichnen(true); toast('Sicherung übernommen.', true); } catch (e) { toast('Das ist keine gültige Sicherung.'); }
}

function binden() {
  R.addEventListener('click', function (ev) {
    var t = ev.target.closest('button, [data-tab], [data-klick]'); if (!t || !R.contains(t)) return;
    var a = function (n) { return t.getAttribute(n); };
    if (t.hasAttribute('data-tab')) { tab(a('data-tab')); return; }
    for (var hk = 0; hk < HAKEN.klick.length; hk++) if (HAKEN.klick[hk](t, a, ev)) return;
    if (t.hasAttribute('data-undo')) { if (UNDO) { S = UNDO; UNDO = null; sichernJetzt(); PLAN = null; zeichnen(false); toast('Rückgängig gemacht.'); } return; }
    if (t.hasAttribute('data-beispiel-weg')) { UNDO = klon(S); S = leer(); sichernJetzt(); PLAN = null; zeichnen(true); toast('Beispiel gelöscht.', true); return; }
    if (t.hasAttribute('data-set')) { var k = a('data-set'), w = a('data-wert'), p = k.split(':');
      if (p[0] === 'lage') { if (p[1] === 'strom' || p[1] === 'leitung') S.lage[p[1]] = w === '1'; else if (p[1] === 'ziel') S.lage.ziel = w === 'frei' ? 'frei' : +w; else if (p[1] === 'spar') S.lage.spar = +w; else S.lage[p[1]] = w; PLAN = null; nachAenderung(true); return; }
      if (p[0] === 'gf') { GF[p[1]] = w; zeichnen(false); return; }
      if (p[0] === 'lf') { OFFEN.lf = Object.assign(OFFEN.lf || { ort: '', q: '' }, { ansicht: w }); zeichnen(false); return; }
      if (p[0] === 'plan') { S.plan = S.plan || {}; S.plan[p[1]] = w; PLAN = planZiel(); nachAenderung(true); return; }
      if (p[0] === 'ef') { var sg = t.parentNode.querySelectorAll('button'); for (var i = 0; i < sg.length; i++) sg[i].setAttribute('aria-pressed', sg[i] === t); return; }
      if (p[0].charAt(0) === 'p') { var pi = +p[0].slice(1); if (S.personen[pi]) { S.personen[pi][p[1]] = w; nachAenderung(true); } return; }
      return; }
    if (t.hasAttribute('data-gf-t')) { GF[a('data-gf-t')] = !GF[a('data-gf-t')]; zeichnen(false); return; }
    if (t.hasAttribute('data-neu-p')) { S.personen.push({ id: uid(), n: '', s: 'w', a: '', kg: '', cm: '', t: 'normal' }); nachAenderung(true); var L = R.querySelectorAll('.vr-person'); if (L.length) { var inp = L[L.length - 1].querySelector('.vr-name'); if (inp) inp.focus(); } return; }
    if (t.hasAttribute('data-weg-p')) { UNDO = klon(S); S.personen.splice(+a('data-weg-p'), 1); nachAenderung(true); toast('Person entfernt.', true); return; }
    if (t.hasAttribute('data-neu-t')) { S.tiere.push({ id: uid(), n: '', futter: '', wasser: '', vorrat: '' }); nachAenderung(true); return; }
    if (t.hasAttribute('data-weg-t')) { UNDO = klon(S); S.tiere.splice(+a('data-weg-t'), 1); nachAenderung(true); toast('Haustier entfernt.', true); return; }
    if (t.hasAttribute('data-add')) { var kk = katVon(S, a('data-add')); if (!kk) return; var it = { u: uid(), k: kk.i, m: 1, e: stdEinheit(kk), mhd: '', o: kk.l || 'v' }; S.lager.push(it); SUCHE = ''; nachAenderung(true);
      var row = R.querySelector('[data-u="' + it.u + '"]'); if (row) { row.scrollIntoView({ block: 'center' }); row.classList.add('vr-blitz'); }
      toast(esc(kk.n) + ' hinzugefügt – Menge und Datum anpassen.'); return; }
    var li = t.closest('.vr-posten');
    if (li && (t.hasAttribute('data-minus') || t.hasAttribute('data-plus'))) { var it2 = lagerItem(li); if (!it2) return; var kat = katVon(S, it2.k), st = /^(g|ml)$/.test(it2.e) ? 100 : /^(kg|l)$/.test(it2.e) ? 0.5 : 1;
      it2.m = Math.max(0, Math.round(((+it2.m || 0) + (t.hasAttribute('data-plus') ? st : -st)) * 100) / 100); void kat; nachAenderung(true);
      if (t.classList.contains('vr-verbr')) { var am = ampel(it2); toast(esc(kat.n) + ': noch ' + fz(it2.m, 2) + (am === 'rot' || am === 'gelb' ? ' – unter dem Mindestbestand, steht auf der Nachkauf-Liste.' : '.')); } return; }
    if (t.hasAttribute('data-lort')) { OFFEN.lf = Object.assign(OFFEN.lf || { ansicht: 'liste' }, { ort: a('data-lort') }); zeichnen(false); return; }
    if (t.hasAttribute('data-ortneu')) { var inp = R.querySelector('#vr-ortneu'), nm = inp && inp.value.trim(); if (!nm) { toast('Bitte einen Namen eingeben.'); return; } S.orte.push({ id: 'o_' + uid(), n: nm, typ: 'v' }); OFFEN.orte = true; nachAenderung(true); return; }
    if (t.hasAttribute('data-ortweg')) { var oid = t.closest('[data-ort]').getAttribute('data-ort'); UNDO = klon(S); S.lager.forEach(function (it) { if (it.o === oid) it.o = 'v'; }); S.orte = S.orte.filter(function (o) { return o.id !== oid; }); OFFEN.orte = true; nachAenderung(true); toast('Lagerort entfernt – die Posten liegen jetzt unter „Vorrat“.', true); return; }
    if (li && t.hasAttribute('data-weg-l')) { UNDO = klon(S); var u = li.getAttribute('data-u'); S.lager = S.lager.filter(function (x) { return x.u !== u; }); nachAenderung(true); toast('Entfernt.', true); return; }
    if (t.hasAttribute('data-eigen-neu')) { eigenAnlegen(t.closest('.vr-eigen')); return; }
    if (t.hasAttribute('data-auf')) { OFFEN[a('data-auf')] = !OFFEN[a('data-auf')]; zeichnen(false); return; }
    if (t.hasAttribute('data-port')) { var b = t.parentNode.querySelector('[data-portw]'), mx = +b.getAttribute('data-max') || 99, v = Math.round(((+b.getAttribute('data-portw') || 1) + (+a('data-port'))) * 10) / 10; v = Math.max(0.5, Math.min(mx, v)); b.setAttribute('data-portw', v); b.textContent = fz(v, 1);
      var pi = t.closest('.vr-koch').querySelector('.vr-portinfo'), PH = portionenHaushalt(S); if (pi) pi.textContent = v >= PH - 1e-9 ? 'Portionen = alle ' + haushalt(S).n + ' Personen' : 'reicht für etwa ' + fz(v / PH * 100) + ' % des Haushalts'; return; }
    if (t.hasAttribute('data-gekocht')) { var r = GERICHTE.filter(function (g) { return g.id === a('data-gekocht'); })[0], pw = t.closest('.vr-gd').querySelector('[data-portw]'), port = +pw.getAttribute('data-portw') || 1;
      UNDO = klon(S); abziehen(S, r, port, heute()); PLAN = null; nachAenderung(true); toast(esc(r.n) + ': Zutaten für ' + fz(port, 1) + ' Port. abgezogen.', true); return; }
    if (t.hasAttribute('data-plan')) { PLAN = planZiel(); var po = R.querySelector('.vr-plan-ort'); po.innerHTML = planHTML(); po.scrollIntoView({ block: 'start' }); return; }
    if (t.hasAttribute('data-plan-zu')) { PLAN = null; R.querySelector('.vr-plan-ort').innerHTML = ''; return; }
    if (t.hasAttribute('data-kz')) { OFFEN.kz = +a('data-kz'); zeichnen(false); return; }
    if (t.hasAttribute('data-liste')) { var txt = 'Vorrat – fehlt noch (Ziel ' + zielTage(S) + ' Tage)\n' + (OFFEN.liste || []).map(function (x) { return '☐ ' + x; }).join('\n');
      if (a('data-liste') === 'teilen' && navigator.share) navigator.share({ title: 'Vorrat – fehlt noch', text: txt }).catch(function () { /* abgebrochen */ }); else kopieren(txt, 'Liste kopiert.'); return; }
    if (t.hasAttribute('data-sich')) { var w2 = a('data-sich');
      if (w2 === 'datei') { var bl = new Blob([sicherungText()], { type: 'application/json' }), url = URL.createObjectURL(bl), aa = document.createElement('a'); aa.href = url; aa.download = 'vorrat-' + new Date().toISOString().slice(0, 10) + '.json'; document.body.appendChild(aa); aa.click(); setTimeout(function () { URL.revokeObjectURL(url); aa.remove(); }, 500); toast('Datei wird gespeichert.'); }
      else if (w2 === 'kopie') { var st2 = sicherungText(), ta = R.querySelector('.vr-text'); if (ta) { ta.value = st2; var dt = ta.closest('details'); if (dt) dt.open = true; }
        kopieren(st2, 'Sicherung kopiert – auf dem anderen Gerät unter „Text einfügen“ einsetzen. Der Text steht auch im Feld darunter.'); }
      else if (w2 === 'einfuegen') sicherungLesen(R.querySelector('.vr-text').value);
      else if (w2 === 'alles-weg') { UNDO = klon(S); S = leer(); sichernJetzt(); PLAN = null; zeichnen(true); toast('Alles gelöscht.', true); }
      return; }
  });
  R.addEventListener('input', function (ev) {
    var t = ev.target;
    for (var hk = 0; hk < HAKEN.eingabe.length; hk++) if (HAKEN.eingabe[hk](t, ev)) return;
    if (t.id === 'vr-finde') { OFFEN.lf = Object.assign(OFFEN.lf || { ort: '', ansicht: 'liste' }, { q: t.value }); var h0 = heute(), LF = OFFEN.lf, q = t.value.toLowerCase().trim();
      var Y = posten(S, h0).filter(function (x) { return (!LF.ort || (x.it.o || 'v') === LF.ort) && (!q || (x.k.n + ' ' + (x.k.s || '') + ' ' + ortName(S, x.it.o)).toLowerCase().indexOf(q) >= 0); }); R.querySelector('.vr-lliste').innerHTML = lagerListeHTML(Y, LF, h0); return; }
    if (t.hasAttribute('data-preis')) { var pv = zahl(t.value); S.preise = S.preise || {}; if (isFinite(pv) && pv > 0) S.preise[t.getAttribute('data-preis')] = pv; else delete S.preise[t.getAttribute('data-preis')]; nachAenderung(false); return; }
    if (t.getAttribute('data-lf2') === 'min') { var itm = lagerItem(t.closest('.vr-posten')), mv = zahl(t.value); if (itm) { if (isFinite(mv) && mv > 0) itm.min = mv; else delete itm.min; nachAenderung(false); } return; }
    if (t.id === 'vr-such') { SUCHE = t.value; R.querySelector('.vr-treffer-ort').innerHTML = trefferHTML(); return; }
    if (t.hasAttribute('data-pf')) { var c = t.closest('[data-p]'), i = +c.getAttribute('data-p'), p = S.personen[i]; if (!p) return; var f = t.getAttribute('data-pf'); p[f] = f === 'n' ? t.value : t.value.trim();
      var e = c.querySelector('[data-perg="' + i + '"]'); if (e) e.innerHTML = personErg(p, bedarf(p)); nachAenderung(false); return; }
    if (t.hasAttribute('data-tf')) { var c2 = t.closest('[data-t]'), j = +c2.getAttribute('data-t'), tt = S.tiere[j]; if (!tt) return; tt[t.getAttribute('data-tf')] = t.value; nachAenderung(false); return; }
    if (t.hasAttribute('data-lf')) { S.lage[t.getAttribute('data-lf')] = t.value.trim(); PLAN = null; nachAenderung(false); return; }
    if (t.getAttribute('data-lf2') === 'm') { var it = lagerItem(t.closest('.vr-posten')); var v = zahl(t.value); if (it && isFinite(v) && v >= 0) { it.m = v; nachAenderung(false); } return; }
  });
  R.addEventListener('toggle', function (ev) { var d = ev.target; if (!d || !d.getAttribute) return; if (d.getAttribute('data-gl')) OFFEN['gl:' + d.getAttribute('data-gl')] = d.open;
    if (d.getAttribute('data-pm')) OFFEN['pm:' + d.getAttribute('data-pm')] = d.open; if (d.classList.contains('vr-orte')) OFFEN.orte = d.open; }, true);
  R.addEventListener('change', function (ev) {
    var t = ev.target;
    for (var hk = 0; hk < HAKEN.aenderung.length; hk++) if (HAKEN.aenderung[hk](t, ev)) return;
    if (t.hasAttribute('data-haken')) { var k = t.getAttribute('data-haken'); if (t.checked) S.haken[k] = 1; else delete S.haken[k]; nachAenderung(true); return; }
    if (t.hasAttribute('data-sich-datei')) { var f = t.files && t.files[0]; if (!f) return; var rd = new FileReader(); rd.onload = function () { sicherungLesen(rd.result); }; rd.readAsText(f); t.value = ''; return; }
    if (t.hasAttribute('data-pf') || t.hasAttribute('data-tf') || t.hasAttribute('data-lf')) { nachAenderung(true); return; }
    if (t.hasAttribute('data-ortn') || t.hasAttribute('data-ortt')) { var o = S.orte.filter(function (x) { return x.id === t.closest('[data-ort]').getAttribute('data-ort'); })[0]; if (!o) return;
      if (t.hasAttribute('data-ortn')) o.n = t.value.trim() || o.n; else o.typ = t.value; OFFEN.orte = true; nachAenderung(true); return; }
    if (t.hasAttribute('data-preis') || t.getAttribute('data-lf2') === 'min') { nachAenderung(true); return; }
    var l2 = t.getAttribute('data-lf2'); if (!l2) return; var it = lagerItem(t.closest('.vr-posten')); if (!it) return;
    if (l2 === 'm') { var v = zahl(t.value); if (isFinite(v) && v >= 0) it.m = v; }
    else if (l2 === 'e') { var kat = katVon(S, it.k), g = gramm(S, it); it.e = t.value; it.m = Math.round(g / einheitG(kat, it.e) * 100) / 100; }
    else if (l2 === 'o') it.o = t.value;
    else if (l2 === 'mm' || l2 === 'jj') { var box = t.closest('.vr-mhd'), mm = box.querySelector('[data-lf2="mm"]').value, jj = box.querySelector('[data-lf2="jj"]').value; it.mhd = mm && jj ? jj + '-' + (mm < 10 ? '0' : '') + mm : ''; }
    nachAenderung(true);
  });
  /* Wischen zwischen den Bereichen (Handy, Tablet) */
  var x0 = null, y0 = 0, t0 = 0;
  R.addEventListener('touchstart', function (e) { var t = e.target; if (t.closest('input, select, textarea, .vr-tabs, .vr-gnav, .vr-tab-wrap, .vr-kurs, .vr-seg, .vr-chips, .vr-kein-wisch')) { x0 = null; return; } x0 = e.touches[0].clientX; y0 = e.touches[0].clientY; t0 = Date.now(); }, { passive: true });
  R.addEventListener('touchend', function (e) { if (x0 == null) return; var dx = e.changedTouches[0].clientX - x0, dy = e.changedTouches[0].clientY - y0; x0 = null;
    if (Math.abs(dx) < 80 || Math.abs(dy) > Math.abs(dx) * 0.6 || Date.now() - t0 > 700) return;
    var TB = sichtbareTabs(), i = TB.indexOf(S.tab), n = i + (dx < 0 ? 1 : -1); if (n >= 0 && n < TB.length) tab(TB[n]); }, { passive: true });
}
function lagerItem(li) { if (!li) return null; var u = li.getAttribute('data-u'); return S.lager.filter(function (x) { return x.u === u; })[0] || null; }
function eigenAnlegen(box) {
  var q = function (n) { return box.querySelector('[data-ef="' + n + '"]'); }, n = q('n').value.trim(), k = zahl(q('k').value);
  if (!n) { toast('Bitte einen Namen eingeben.'); q('n').focus(); return; }
  if (!isFinite(k) || k < 0 || k > 950) { toast('Bitte kcal je 100 g vom Etikett eintragen.'); q('k').focus(); return; }
  var ko = box.querySelector('[data-set="ef:ko"][aria-pressed="true"]'), pg = zahl(q('pg').value);
  var e = { i: 'e_' + uid(), n: n, g: q('g').value, k: k, e: zahl(q('e').value) || 0, f: zahl(q('f').value) || 0, c: zahl(q('c').value) || 0, q: 'eigen', ht: 'MHD auf der Packung' };
  if (ko && ko.getAttribute('data-wert') === '1') e.ko = 1; if (e.g === 'trinken') { e.ml = 1; } if (isFinite(pg) && pg > 0) e.p = [['Packung ' + fz(pg) + ' g', pg]];
  S.eigene.push(e); S.lager.push({ u: uid(), k: e.i, m: 1, e: stdEinheit(e), mhd: '', o: 'v' }); nachAenderung(true); toast(esc(n) + ' angelegt und ins Lager gelegt.');
}

function seite(el, opt) {
  if (!el) return; opt = opt || {};
  S = laden(); if (!S) { S = beispiel(heute()); sichernJetzt(); }
  if (!BEREICH[S.tab]) S.tab = BEREICH.uebersicht ? 'uebersicht' : 'reichweite';
  FIG = opt.figur || null; PLAN = null; SUCHE = ''; OFFEN = {};
  el.innerHTML = '<div class="vr-seite">' + kopfHTML() + '<div class="vr-leiste"></div>' + '<div class="vr-inhalt"></div>' + quellenHTML() + '<div class="vr-toast" role="status" aria-live="polite" hidden></div></div>';
  R = el.querySelector('.vr-seite'); binden(); zeichnen(false);
  return R;
}

/* Schnittstelle für Erweiterungen (vorrat_plus.js) – nur innerhalb der App benutzen */
var INTERN = { WQ: WQ, ARTEN: ARTEN, HAKEN: HAKEN, BEREICH: BEREICH, TABNAME: TABNAME, NAV: NAV, QUELLEN: QUELLEN, CHECK: CHECK, KATALOG: KATALOG, KAT: KAT, GERICHTE: GERICHTE, GERICHTE_ROH: GERICHTE_ROH, GRUPPEN: GRUPPEN, GR: GR, ORTE_STD: ORTE_STD, KOCHT: KOCHT, MZN: MZN,
  zustand: function () { return S; }, setze: function (n) { S = n; }, wurzel: function () { return R; }, offen: function () { return OFFEN; }, undo: function (x) { UNDO = x; },
  sichern: function () { sichern(); }, sichernJetzt: function () { sichernJetzt(); }, zeichnen: function (r) { zeichnen(r); }, nachAenderung: function (n) { nachAenderung(n); }, toast: function (t, u) { toast(t, u); }, tab: function (t) { tab(t); },
  heute: heute, esc: esc, fz: fz, kg: kg, liter: liter, zahl: zahl, uid: uid, klon: klon, feld: feld, zahlIn: zahlIn, seg: seg, balken: balken, leerText: leerText, tageText: tageText, tageZahl: tageZahl,
  mhdText: mhdText, mhdDatum: mhdDatum, tageBis: tageBis, kopieren: function (t, o) { kopieren(t, o); }, dateiMoeglich: dateiMoeglich, sicherungText: function () { return sicherungText(); }, sicherungLesen: function (t) { sicherungLesen(t); },
  planZiel: function () { return planZiel(); }, mhdSel: mhdSel, einheitT: einheitT, stdEinheit: stdEinheit, kurzZeile: function () { return kurzZeile(); } };
root.QWVorrat = { seite: seite, _kern: KERN, _i: INTERN };
if (typeof module !== 'undefined' && module.exports) module.exports = root.QWVorrat;
})(typeof window !== 'undefined' ? window : globalThis);
