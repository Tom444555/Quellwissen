// Screenshot einer Seite: NODE_PATH=$(npm root -g) node foto.js "#s-tinkturen-biochemie" [ausgabe.png]
// Speichert Seite + jede sichtbare Zeichnung (figure.illu). Für 3D: node foto.js 3d:p05
const { chromium } = require('playwright'); const path=require('path');
(async()=>{ const ziel=process.argv[2]||'', aus=process.argv[3]||'foto.png';
 const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 const p=await b.newPage({viewport:{width:1000,height:900}}); const err=[]; p.on('pageerror',e=>err.push(e.message));
 const f='file://'+path.resolve(__dirname,'..','quelle','gruenwissen.html');
 if(ziel.startsWith('3d:')){ await p.goto(f); await p.addScriptTag({path:path.resolve(__dirname,'..','lib','three.min.js')}); await p.addScriptTag({path:path.resolve(__dirname,'..','lib','OrbitControls.js')});
   await p.evaluate(id=>QW3D.oeffne(id,null),ziel.slice(3)); await p.waitForSelector('#qw3d canvas',{timeout:60000}); await p.waitForTimeout(1500); }
 else { await p.goto(f+ziel); await p.waitForTimeout(500);
   const figs=await p.$$('section.panel:not([hidden]) figure.illu'); let i=0; for(const el of figs) await el.screenshot({path:aus.replace('.png',`_z${i++}.png`)}); }
 await p.screenshot({path:aus}); console.log('Fehler:',err); await b.close(); })();
