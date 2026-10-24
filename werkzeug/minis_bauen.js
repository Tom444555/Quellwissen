// Rendert die kleinen Vorschaubilder der Startseite als PNG (2x) und bettet sie ein – Startseite lädt dadurch schnell.
const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
(async()=>{const Q=path.resolve(__dirname,'..','quelle','gruenwissen.html');
 const b=await chromium.launch();const p=await b.newPage({viewport:{width:1024,height:900},deviceScaleFactor:2});
 await p.goto('file://'+Q+'#start');await p.waitForTimeout(300);
 const ids=await p.evaluate(()=>[...new Set([...document.querySelectorAll('.bm-mini[data-mini], .bm-mini')].map(e=>e.dataset.mini||e.dataset.id).filter(Boolean))]);
 await p.evaluate(()=>{const d=document.createElement('div');d.id='mb-test';d.style.cssText='position:fixed;left:0;top:0;z-index:99999;background:transparent';document.body.appendChild(d);});
 const out={};
 for(const id of ids){ await p.evaluate(id=>{const d=document.getElementById('mb-test');d.innerHTML=`<span class="bm-mini" style="background:transparent">${QW_IL.mini(id,'')}</span>`;},id);
   const el=await p.$('#mb-test .bm-mini'); const buf=await el.screenshot({omitBackground:true,type:'png'}); out[id]='data:image/png;base64,'+buf.toString('base64'); }
 let s=fs.readFileSync(Q,'utf8'); s=s.replace(/<script type="application\/json" id="minibilder">.*?<\/script>\n/s,'');
 const i=s.indexOf('<script type="application/json" id="daten">'); s=s.slice(0,i)+`<script type="application/json" id="minibilder">${JSON.stringify(out)}</script>\n`+s.slice(i);
 fs.writeFileSync(Q,s); console.log('Vorschaubilder:',ids.length, Math.round(JSON.stringify(out).length/1024)+' KB'); await b.close(); })();
