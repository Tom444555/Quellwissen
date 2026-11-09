    ern_bilanz(){ seed=3101; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='start')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      // Ständer und Balken
      g+=`<path d="M372,292 L388,292 L384,78 L376,78 Z" fill="#8a6a48" stroke="#4a3420" stroke-width="1.2"/>`;
      g+=`<ellipse cx="380" cy="296" rx="70" ry="9" fill="#a88a64" stroke="#4a3420" stroke-width="1.2"/>`;
      g+=`<rect x="150" y="66" width="460" height="10" rx="5" fill="#9a7a52" stroke="#4a3420" stroke-width="1.2"/>`;
      g+=`<circle cx="380" cy="71" r="9" fill="#c8a46a" stroke="#4a3420" stroke-width="1.2"/>`;
      g+=`<path d="M380,58 L372,44 L388,44 Z" fill="#c8a46a" stroke="#4a3420"/>`;
      const schale=(cx,titel,unter,stapel)=>{ let s='';
        s+=`<path d="M${cx-4},76 L${cx-70},216 M${cx+4},76 L${cx+70},216" stroke="#6a5a48" stroke-width="1.1"/>`;
        let y=212; const H=118;
        stapel.forEach(([t,p,f,z])=>{ const h=H*p; y-=h; s+=`<rect x="${cx-58}" y="${y.toFixed(1)}" width="116" height="${(h-1.5).toFixed(1)}" rx="4" fill="${f}" stroke="${shade(f,-.35)}" stroke-width="1">`+
          `<animate attributeName="opacity" from="0" to="1" dur=".6s" begin="${(0.2+stapel.indexOf(stapel.find(x=>x[0]===t))*0.25).toFixed(2)}s" fill="freeze"/></rect>`;
          s+=T(cx,y+h/2+(z?-1:4),t,'#2a2018',h>22?10:8.5,800,'middle').replace('stroke:var(--surface)','stroke:'+f);
          if(z&&h>26) s+=T(cx,y+h/2+11,z,'#3a3028',8.5,600,'middle').replace('stroke:var(--surface)','stroke:'+f); });
        s+=`<path d="M${cx-80},214 Q${cx},250 ${cx+80},214 Z" fill="#c9b08a" stroke="#4a3420" stroke-width="1.3"/>`;
        s+=T(cx,268,titel,'var(--ink)',13,800,'middle')+T(cx,284,unter,'var(--muted)',9.5,600,'middle');
        return s; };
      g+=schale(190,'Zufuhr','Energie aus Essen und Trinken',[['Alkohol 7 kcal/g',.06,'#b89ac8',''],['Eiweiß 4 kcal/g',.16,'#d98a72',''],['Fett 9 kcal/g',.34,'#f0cf6a','Öl, Butter, Käse, Nüsse'],['Kohlenhydrate 4 kcal/g',.44,'#e8b07a','Brot, Reis, Obst, Zucker']]);
      g+=schale(570,'Verbrauch','Energie, die der Körper umsetzt',[['Aktivität & NEAT',.25,'#e88a5a','Sport, Gehen, Stehen'],['Verdauung (TEF) ~10 %',.1,'#9cc87a',''],['Grundumsatz 60–70 %',.65,'#7aa8d8','Organe, Gehirn, Wärme']]);
      // Ergebnis-Kästen
      const K=[['Zufuhr > Verbrauch','Speicher wachsen: Glykogen, Fett','#f3d9b4'],['Zufuhr = Verbrauch','Gewicht bleibt stabil','#dde8d0'],['Zufuhr < Verbrauch','Speicher werden geleert','#d6e4f2']];
      K.forEach((k,i)=>{ const x=286, y=106+i*38; g+=`<rect x="${x}" y="${y}" width="188" height="32" rx="7" fill="${k[2]}" stroke="#8a7a68" stroke-width="1"/>`+T(380,y+14,k[0],'var(--ink)',10,800,'middle').replace('stroke:var(--surface)','stroke:'+k[2])+T(380,y+26,k[1],'#4a4038',8.5,600,'middle').replace('stroke:var(--surface)','stroke:'+k[2]); });
      g+=T(380,24,'Energiebilanz','var(--ink)',13,800,'middle');
      return {vb:'0 0 760 300',breit:true,leg:[],svg:g}; },

    ern_fettweg(){ seed=3102; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='start')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      const pf=(d,c='#6a5a48',w=1.8)=>`<path d="${d}" stroke="${c}" stroke-width="${w}" fill="none" marker-end="url(#fw_pf)"/>`;
      g+=`<defs><marker id="fw_pf" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6a5a48"/></marker></defs>`;
      const kette=(x,y,n,l=6)=>{ let d=`M${x},${y}`; for(let i=1;i<=n;i++) d+=` L${x+i*l},${y+(i%2?-3:0)}`; return `<path d="${d}" stroke="#b88a2a" stroke-width="1.6" fill="none"/>`; };
      // 1 Fettzelle
      g+=`<circle cx="92" cy="176" r="64" fill="#f4e6c8" stroke="#8a6a3a" stroke-width="1.6"/><circle cx="96" cy="182" r="50" fill="#f2cf62" stroke="#a8862a" stroke-width="1.2"/><ellipse cx="44" cy="140" rx="10" ry="7" fill="#b8a0c8" stroke="#6a5a7a"/>`;
      g+=T(92,100,'① Fettzelle','var(--ink)',11,800,'middle')+T(96,186,'Triglyceride','#5a4010',9.5,800,'middle').replace('stroke:var(--surface)','stroke:#f2cf62');
      g+=`<rect x="8" y="26" width="168" height="44" rx="8" fill="#eef2f6" stroke="#7a8a9a"/>`+T(92,43,'Adrenalin, Glukagon ↑ → fördern','#2f5a7a',9,700,'middle')+T(92,60,'Insulin ↑ → hemmt den Abbau','#9a3a2a',9,700,'middle');
      g+=pf('M158,170 L214,170')+T(186,162,'Lipolyse','#7a4a1a',9.5,800,'middle')+T(186,186,'ATGL, HSL','var(--muted)',8.5,600,'middle');
      // 2 Blut
      g+=`<rect x="218" y="128" width="196" height="84" rx="12" fill="#e8a0a0" stroke="#9a3a3a" stroke-width="1.4"/>`;
      for(let i=0;i<5;i++){ const x=232+i*36, y=150+(i%2)*28; g+=`<ellipse cx="${x+6}" cy="${y}" rx="9" ry="7" fill="#f6e0c0" stroke="#9a7a5a"/>`+kette(x+14,y+2,3); }
      g+=T(316,120,'② Blut: Fettsäuren an Albumin','var(--ink)',10,800,'middle');
      g+=pf('M300,214 L300,250')+`<rect x="236" y="252" width="128" height="40" rx="8" fill="#e6d2b0" stroke="#8a6a48"/>`+T(300,268,'Glycerin → Leber','var(--ink)',9.5,800,'middle')+T(300,283,'wird zu Glukose','var(--muted)',8.5,600,'middle');
      g+=pf('M416,170 L452,170');
      // 3 Muskelzelle + Mitochondrium
      g+=`<rect x="456" y="70" width="296" height="232" rx="26" fill="#f2cdc4" stroke="#9a5a4a" stroke-width="1.5"/>`;
      for(let i=0;i<7;i++) g+=`<path d="M${470+i*40},78 L${470+i*40},294" stroke="#d8a89a" stroke-width="1" stroke-dasharray="3 5"/>`;
      g+=T(744,92,'③ Muskelzelle','var(--ink)',11,800,'end');
      g+=`<ellipse cx="610" cy="196" rx="132" ry="78" fill="#e8c890" stroke="#8a5a2a" stroke-width="1.8"/>`;
      let cr=''; for(let i=0;i<6;i++){ const x=510+i*40; cr+=`<path d="M${x},140 q10,14 0,28 q-10,14 0,28 q10,14 0,28" stroke="#b88a4a" stroke-width="1.2" fill="none" opacity=".55"/>`; } g+=cr;
      g+=`<rect x="474" y="184" width="26" height="22" rx="4" fill="#9ac8a8" stroke="#3a6a4a"/>`+T(487,222,'Carnitin','#2a5a3a',8.5,800,'middle');
      g+=T(610,132,'Mitochondrium','#6a3a10',10,800,'middle');
      const box=(x,y,w,t,f)=>`<rect x="${x}" y="${y}" width="${w}" height="24" rx="6" fill="${f}" stroke="#6a5a48"/>`+T(x+w/2,y+16,t,'#2a2018',9.5,800,'middle').replace('stroke:var(--surface)','stroke:'+f);
      g+=box(504,150,86,'β-Oxidation','#f6e6b0')+pf('M590,162 L604,162','#6a5a48',1.4)+box(606,150,78,'Acetyl-CoA','#f6d6a0');
      g+=`<circle cx="620" cy="226" r="26" fill="#f6e0c0" stroke="#8a5a2a" stroke-width="1.4" stroke-dasharray="4 3"><animateTransform attributeName="transform" type="rotate" from="0 620 226" to="360 620 226" dur="12s" repeatCount="indefinite"/></circle>`;
      g+=T(620,223,'Citrat-','#5a3a10',8.5,800,'middle')+T(620,234,'zyklus','#5a3a10',8.5,800,'middle');
      g+=pf('M640,175 L630,198','#6a5a48',1.4);
      g+=`<rect x="664" y="206" width="66" height="40" rx="6" fill="#c8d8ec" stroke="#4a6a8a"/>`+T(697,222,'Atmungs-','#1a3a5a',8.5,800,'middle')+T(697,234,'kette','#1a3a5a',8.5,800,'middle');
      g+=pf('M647,226 L662,226','#6a5a48',1.4);
      g+=`<path d="M697,252 l6,10 l11,1 l-8,8 l3,11 l-12,-6 l-12,6 l3,-11 l-8,-8 l11,-1 Z" fill="#f2c040" stroke="#8a6a10"><animate attributeName="opacity" values="1;.45;1" dur="2s" repeatCount="indefinite"/></path>`+T(724,272,'ATP','#7a5a00',10,800);
      g+=T(697,200,'+ O₂','#2f5a7a',9,800,'middle');
      // Ausgänge
      g+=pf('M612,200 C600,120 560,60 540,30','#4a6a8a',2);
      g+=`<path d="M500,8 q-14,0 -16,18 q-2,16 10,16 q8,0 9,-12 Z M520,8 q14,0 16,18 q2,16 -10,16 q-8,0 -9,-12 Z" fill="#e8b4b4" stroke="#9a5a5a"/>`;
      g+=T(546,22,'CO₂ → Lunge: ca. 84 %','#2f5a7a',10.5,800)+T(546,36,'wird ausgeatmet','var(--muted)',8.5,600);
      g+=pf('M590,272 L560,320','#4a8aaa',2)+T(552,334,'H₂O → Urin, Schweiß, Atem: ca. 16 %','#2a6a8a',10,800,'end');
      g+=T(8,328,'C₅₅H₁₀₄O₆ + 78 O₂ → 55 CO₂ + 52 H₂O + Energie','var(--ink)',10,800)+T(8,343,'(Meerman & Brown 2014)','var(--muted)',8.5,600);
      return {vb:'0 0 760 350',breit:true,leg:[],svg:g}; },

    ern_fettsaeuren(){ seed=3103; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='start')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      const kette=(db,L,turn)=>{ let th=0, p=[[0,0]], s=1; const D=new Set(db.map(x=>x[0]));
        for(let i=1;i<18;i++){ const a=th+s*30*Math.PI/180; p.push([p[i-1][0]+L*Math.cos(a), p[i-1][1]+L*Math.sin(a)]); s=-s;
          const k=db.find(x=>x[0]===i); if(k&&k[1]==='c') th-=turn*Math.PI/180; }
        const a=Math.atan2(p[17][1]-p[0][1],p[17][0]-p[0][0]); const c=Math.cos(-a), sn=Math.sin(-a);
        return p.map(([x,y])=>[x*c-y*sn, x*sn+y*c]); };
      const zeichne=(ox,oy,db,L,turn,farbe,kopf=true)=>{ const p=kette(db,L,turn); const ys=p.map(q=>q[1]); const dy=oy-(Math.min(...ys)+Math.max(...ys))/2;
        const P=p.map(([x,y])=>[ox+x,y+dy]); let s=`<path d="M${P.map(q=>q.map(v=>v.toFixed(1)).join(',')).join(' L')}" stroke="${farbe}" stroke-width="2.4" fill="none" stroke-linejoin="round"/>`;
        db.forEach(([i])=>{ const a=P[i-1], b=P[i], mx=(a[0]+b[0])/2, my=(a[1]+b[1])/2, cx=(P[i-2]?P[i-2][0]+P[i+1][0]:a[0]*2)/2, cy=(P[i-2]?P[i-2][1]+P[i+1][1]:a[1]*2)/2;
          let nx=-(b[1]-a[1]), ny=b[0]-a[0]; const l=Math.hypot(nx,ny); nx/=l; ny/=l; if((cx-mx)*nx+(cy-my)*ny<0){ nx=-nx; ny=-ny; }
          s+=`<path d="M${(a[0]+(b[0]-a[0])*.18+nx*4.5).toFixed(1)},${(a[1]+(b[1]-a[1])*.18+ny*4.5).toFixed(1)} L${(a[0]+(b[0]-a[0])*.82+nx*4.5).toFixed(1)},${(a[1]+(b[1]-a[1])*.82+ny*4.5).toFixed(1)}" stroke="#c83a2a" stroke-width="2.2"/>`; });
        if(kopf) s+=`<circle cx="${P[0][0].toFixed(1)}" cy="${P[0][1].toFixed(1)}" r="9" fill="#e86a5a" stroke="#8a2a1a"/>`+T(P[0][0]-12,P[0][1]+4,'COOH','#8a2a1a',8.5,800,'end');
        return s; };
      const R=[['Stearinsäure','C18:0 · gesättigt · gerade → fest',[],'#7a6a5a'],['Ölsäure','C18:1 cis (Omega-9) · 1 Knick → flüssig',[[9,'c']],'#9a8a2a'],['Linolsäure','C18:2 (Omega-6) · essenziell',[[9,'c'],[12,'c']],'#c88a2a'],['α-Linolensäure','C18:3 (Omega-3) · essenziell',[[9,'c'],[12,'c'],[15,'c']],'#3a8a6a'],['Elaidinsäure (trans)','C18:1 trans · gestreckt wie gesättigt',[[9,'t']],'#8a4a6a']];
      R.forEach((r,i)=>{ const y=40+i*62; g+=zeichne(64,y,r[2],15,32,r[3])+T(340,y-4,r[0],'var(--ink)',11,800)+T(340,y+10,r[1],'var(--muted)',9,600); });
      g+=T(64,346,'rote Doppelstriche = Doppelbindungen','#c83a2a',9,700);
      // Triglycerid
      g+=`<rect x="540" y="20" width="212" height="314" rx="12" fill="#f6efe2" stroke="#b8a888" stroke-dasharray="5 4"/>`;
      g+=T(646,42,'Triglycerid','var(--ink)',12,800,'middle')+T(646,56,'Glycerin + 3 Fettsäuren','var(--muted)',9,600,'middle');
      [[96,[] ,'#7a6a5a'],[176,[[9,'c']],'#9a8a2a'],[262,[[9,'c'],[12,'c']],'#c88a2a']].forEach(([y,db,f])=>{ g+=zeichne(590,y,db,9,32,f,false)+`<path d="M573,${y} L590,${y}" stroke="#6a5a48" stroke-width="2"/>`+T(581,y-6,'Ester','var(--muted)',7.5,700,'middle'); });
      g+=`<path d="M566,96 L566,262" stroke="#6a5a48" stroke-width="5" stroke-linecap="round"/>`;
      [96,176,262].forEach(y=>g+=`<circle cx="566" cy="${y}" r="7" fill="#c8b8e8" stroke="#5a4a7a"/>`);
      g+=T(556,320,'Glycerin','#5a4a7a',9.5,800,'start');
      return {vb:'0 0 760 352',breit:true,leg:[],svg:g}; },

    ern_aminosaeuren(){ seed=3104; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='start')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      const E=[['Leu','#d9534f'],['Lys','#e8883a'],['Val','#e8c23a'],['Phe','#8ab83a'],['Ile','#3aa86a'],['Met','#3a9ab8'],['Thr','#4a6ad8'],['His','#8a5ac8'],['Trp','#c85aa8']];
      g+=T(20,24,'Ein Protein = Kette aus Aminosäuren','var(--ink)',12,800);
      let d='', P=[];
      for(let i=0;i<22;i++){ const x=36+i*20, y=96+Math.sin(i*0.7)*30; P.push([x,y]); }
      g+=`<path d="M${P.map(p=>p.map(v=>v.toFixed(1)).join(',')).join(' L')}" stroke="#8a7a68" stroke-width="2" fill="none"/>`;
      P.forEach((p,i)=>{ const e=i%3===0||i%5===1?E[(i*4)%9]:null; const f=e?e[1]:'#c8c0b4';
        g+=`<circle cx="${p[0].toFixed(1)}" cy="${p[1].toFixed(1)}" r="9" fill="${f}" stroke="${shade(f,-.4)}" stroke-width="1"><animate attributeName="r" values="0;9" dur=".4s" begin="${(i*0.06).toFixed(2)}s" fill="freeze"/></circle>`; });
      g+=T(20,150,'farbig: 9 essenzielle (mit der Nahrung) · grau: 11 bildet der Körper selbst','var(--muted)',9,600);
      const N=['Leucin','Lysin','Valin','Phenylalanin','Isoleucin','Methionin','Threonin','Histidin','Tryptophan'];
      E.forEach((e,i)=>{ const x=26+(i%3)*150, y=180+Math.floor(i/3)*24; g+=`<circle cx="${x}" cy="${y-4}" r="7" fill="${e[1]}" stroke="${shade(e[1],-.4)}"/>`+T(x+12,y,`${N[i]} (${e[0]})`,'var(--ink)',9.5,700); });
      g+=T(20,266,'Getreide + Hülsenfrüchte ergänzen sich: Lysin ↔ Methionin','#5a4a2a',10,800);
      // Minimum-Fass
      const bx=500, by=268, W=26;
      g+=T(620,24,'Gesetz vom Minimum','var(--ink)',12,800,'middle')+T(620,38,'Beispiel Getreide: Lysin ist knapp','var(--muted)',9,600,'middle');
      const H=[178,92,170,184,166,150,160,176,172];
      g+=`<rect x="${bx}" y="${by-92}" width="${W*9}" height="92" fill="#7ab8e0" opacity=".85"><animate attributeName="height" from="0" to="92" dur="1.4s" fill="freeze"/><animate attributeName="y" from="${by}" to="${by-92}" dur="1.4s" fill="freeze"/></rect>`;
      H.forEach((h,i)=>{ const x=bx+i*W, f=i===1?'#d89a5a':'#b8865a'; g+=`<rect x="${x+1}" y="${by-h}" width="${W-2}" height="${h}" rx="3" fill="${f}" stroke="#5a3a1a" stroke-width="1" />`+T(x+W/2,by+14,E[i][0],i===1?'#9a4a10':'var(--muted)',8.5,800,'middle'); });
      g+=`<rect x="${bx+1}" y="${by-92}" width="${W*9-2}" height="92" fill="#4a9ad0" opacity=".5"><animate attributeName="height" from="0" to="92" dur="1.4s" fill="freeze"/><animate attributeName="y" from="${by}" to="${by-92}" dur="1.4s" fill="freeze"/></rect>`;
      g+=`<path d="M${bx-4},${by-40} Q${bx+W*4.5},${by-30} ${bx+W*9+4},${by-40} M${bx-4},${by-140} Q${bx+W*4.5},${by-130} ${bx+W*9+4},${by-140}" stroke="#3a2a18" stroke-width="2.5" fill="none"/>`;
      g+=`<path d="M${bx+W*1.5},${by-92} q10,-4 14,8 q4,18 -2,40" stroke="#4a9ad0" stroke-width="3" fill="none" stroke-linecap="round"><animate attributeName="stroke-dasharray" values="0 80;80 0" dur="1.4s" begin="1.2s" fill="freeze"/></path>`;
      g+=T(bx+W*2.5,by-98,'läuft über bei Lysin','#2a6a9a',9,800);
      return {vb:'0 0 760 290',breit:true,leg:[],svg:g}; },

    ern_blutzucker(){ seed=3105; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='start')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      const X0=70, X1=600, Y0=250, Y1=30, X=t=>X0+(X1-X0)*t/180, Y=v=>Y0-(Y0-Y1)*(v-60)/(170-60);
      for(let v=60;v<=160;v+=20) g+=`<path d="M${X0},${Y(v).toFixed(1)} L${X1},${Y(v).toFixed(1)}" stroke="var(--line)" stroke-width="1"/>`+T(X0-8,Y(v)+4,String(v),'var(--muted)',9,600,'end');
      for(let t=0;t<=180;t+=30) g+=T(X(t),Y0+16,String(t),'var(--muted)',9,600,'middle');
      g+=T(X0+(X1-X0)/2,Y0+32,'Minuten nach dem Essen','var(--muted)',9.5,700,'middle')+T(18,140,'Blutzucker mg/dl','var(--muted)',9.5,700,'middle').replace('<text','<text transform="rotate(-90 18 140)"');
      const kur=(A,tp,dip)=>{ let p=[]; for(let t=0;t<=180;t+=3){ const v=88+A*Math.pow(t/tp,2)*Math.exp(2*(1-t/tp))-dip*Math.exp(-Math.pow((t-125)/28,2)); p.push([X(t),Y(v)]); } return 'M'+p.map(q=>q.map(v=>v.toFixed(1)).join(',')).join(' L'); };
      const ins=(A,tp)=>{ let p=[]; for(let t=0;t<=180;t+=3){ const v=64+A*Math.pow(t/tp,2)*Math.exp(2*(1-t/tp)); p.push([X(t),Y(v)]); } return 'M'+p.map(q=>q.map(v=>v.toFixed(1)).join(',')).join(' L'); };
      const lin=(d,f,w,da,b)=>`<path d="${d}" stroke="${f}" stroke-width="${w}" fill="none" ${da?`stroke-dasharray="${da}"`:'pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"'}>${da?'':`<animate attributeName="stroke-dashoffset" from="1" to="0" dur="1.6s" begin="${b}s" fill="freeze"/>`}</path>`;
      g+=lin(ins(52,40),'#e8a07a',1.8,'5 4',0)+lin(ins(22,55),'#7ab89a',1.8,'5 4',0);
      g+=lin(kur(60,35,16),'#d9534f',3,'',0.2)+lin(kur(26,52,0),'#3a8a6a',3,'',0.6);
      g+=`<path d="M${X0},${Y(70).toFixed(1)} L${X1},${Y(70).toFixed(1)}" stroke="#9a8a7a" stroke-width="1" stroke-dasharray="2 3"/>`;
      g+=T(X(36)+6,Y(150)-6,'hoher GI: Weißbrot, Cornflakes','#b8332f',10,800)+T(X(128),Y(87),'Dip unter Ausgangswert → Hunger','#b8332f',9,700,'middle');
      g+=T(X(70),Y(118)-6,'niedriger GI: Linsen, Vollkorn + Eiweiß','#2a6a4a',10,800);
      // Legende rechts
      const L=[['#d9534f','Blutzucker, hoher GI'],['#3a8a6a','Blutzucker, niedriger GI'],['#e8a07a','Insulin, hoher GI'],['#7ab89a','Insulin, niedriger GI']];
      L.forEach((l,i)=>{ const y=60+i*22; g+=`<path d="M622,${y} L652,${y}" stroke="${l[0]}" stroke-width="${i<2?3:1.8}" ${i>1?'stroke-dasharray="5 4"':''}/>`+T(658,y+4,l[1],'var(--ink)',9,700); });
      g+=T(622,170,'Schematisch nach typischen','var(--muted)',8.5,600)+T(622,182,'Messkurven [Ergänzung]','var(--muted)',8.5,600);
      return {vb:'0 0 760 290',breit:true,leg:[],svg:g}; },

    ern_gewichtsverlauf(){ seed=3106; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='start')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      const X0=70, X1=520, Y0=34, Y1=250, X=m=>X0+(X1-X0)*m/36, Y=k=>Y0+(Y1-Y0)*(-k)/30;
      for(let k=0;k>=-30;k-=5) g+=`<path d="M${X0},${Y(k)} L${X1},${Y(k)}" stroke="var(--line)" stroke-width="1"/>`+T(X0-8,Y(k)+4,k===0?'0':String(k).replace('-','−'),'var(--muted)',9,600,'end');
      for(let m=0;m<=36;m+=6) g+=T(X(m),Y1+16,String(m),'var(--muted)',9,600,'middle');
      g+=T((X0+X1)/2,Y1+32,'Monate mit dauerhaft 500 kcal weniger pro Tag','var(--muted)',9.5,700,'middle')+T(20,142,'kg Gewicht','var(--muted)',9.5,700,'middle').replace('<text','<text transform="rotate(-90 20 142)"');
      const regel=m=>-500*30.44*m/7700; const mEnd=30/(500*30.44/7700);
      g+=`<path d="M${X(0)},${Y(0)} L${X(mEnd).toFixed(1)},${Y(-30)}" stroke="#d9534f" stroke-width="3" fill="none" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"><animate attributeName="stroke-dashoffset" from="1" to="0" dur="1.4s" fill="freeze"/></path>`;
      let p=[]; for(let m=0;m<=36;m+=.5){ const w=-20.9*(1-Math.exp(-Math.pow(m/15.8,1.334))); p.push([X(m),Y(w)]); }
      g+=`<path d="M${p.map(q=>q.map(v=>v.toFixed(1)).join(',')).join(' L')}" stroke="#2f6a9a" stroke-width="3" fill="none" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"><animate attributeName="stroke-dashoffset" from="1" to="0" dur="2s" begin=".4s" fill="freeze"/></path>`;
      g+=`<path d="M${X0},${Y(-20.9)} L${X1},${Y(-20.9)}" stroke="#2f6a9a" stroke-width="1" stroke-dasharray="4 4"/>`;
      g+=`<circle cx="${X(12)}" cy="${Y(regel(12)).toFixed(1)}" r="5" fill="#d9534f"/><circle cx="${X(12)}" cy="${Y(-10.45).toFixed(1)}" r="5" fill="#2f6a9a"/>`;
      g+=T(X(12)+10,Y(regel(12))+4,'7700-Regel: −24 kg nach 1 Jahr','#b8332f',10,800);
      g+=T(X(12)+10,Y(-10.45)-8,'Modell (Hall 2011): ca. −10 kg','#1f4f7a',10,800);
      g+=T(X1-4,Y(-20.9)-6,'Plateau ca. −21 kg','#1f4f7a',9.5,800,'end');
      g+=`<rect x="538" y="40" width="216" height="150" rx="10" fill="#f4efe6" stroke="#b8a888"/>`;
      ['Warum flacher?','• leichter Körper verbraucht weniger','• etwas Anpassung des Stoffwechsels','• anfangs Wasser & Glykogen,','  später Fett + etwas Muskel','Faustregel: 24 kcal/Tag','weniger ≈ 1 kg am Ende'].forEach((t,i)=>g+=T(548,60+i*18,t,i===0?'var(--ink)':'#4a4038',i===0?10.5:9,i===0?800:600));
      return {vb:'0 0 760 290',breit:true,leg:[],svg:g}; },

    ern_teller(){ seed=3107; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='start')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      const cx=200, cy=160, R0=140, R=118;
      g+=`<circle cx="${cx}" cy="${cy}" r="${R0}" fill="#f4f0e8" stroke="#8a8478" stroke-width="1.6"/><circle cx="${cx}" cy="${cy}" r="${R+4}" fill="#ece6da" stroke="#b8b0a2"/>`;
      g+=`<path d="M${cx},${cy-R} A${R},${R} 0 0 0 ${cx},${cy+R} Z" fill="#b8d89a" stroke="#5a7a3a" stroke-width="1.2"/>`;
      g+=`<path d="M${cx},${cy} L${cx},${cy-R} A${R},${R} 0 0 1 ${cx+R},${cy} Z" fill="#e8b49a" stroke="#8a4a3a" stroke-width="1.2"/>`;
      g+=`<path d="M${cx},${cy} L${cx+R},${cy} A${R},${R} 0 0 1 ${cx},${cy+R} Z" fill="#f2dca2" stroke="#9a7a3a" stroke-width="1.2"/>`;
      // Gemüse: Brokkoli, Tomaten, Salat
      for(let i=0;i<9;i++){ const a=(100+i*20)*Math.PI/180, r=40+rnd()*50, x=cx+r*Math.cos(a), y=cy+r*Math.sin(a)*1.05;
        if(i%3===0) g+=`<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="11" fill="#d9483a" stroke="#8a2a1a"/><circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="4" fill="#f2a08a"/>`;
        else g+=`<path d="M${x-2},${y+12} L${x+2},${y+12} L${x+1},${y} L${x-1},${y} Z" fill="#8aa85a"/><circle cx="${x-6}" cy="${y-2}" r="7" fill="#4a8a3a" stroke="#2a5a2a"/><circle cx="${x+5}" cy="${y-4}" r="7" fill="#5a9a42" stroke="#2a5a2a"/><circle cx="${x}" cy="${y-9}" r="7" fill="#4a8a3a" stroke="#2a5a2a"/>`; }
      // Eiweiß: Fischfilet + Ei
      g+=`<path d="M${cx+20},${cy-50} q30,-34 74,-12 q-10,22 -40,26 q-24,2 -34,-14 Z" fill="#f2b8a0" stroke="#9a5a4a"/><path d="M${cx+34},${cy-56} l12,6 M${cx+52},${cy-62} l12,8" stroke="#c88a7a"/>`;
      g+=`<ellipse cx="${cx+46}" cy="${cy-84}" rx="20" ry="15" fill="#fbf8f0" stroke="#a8a090"/><circle cx="${cx+48}" cy="${cy-83}" r="8" fill="#f2c040" stroke="#b88a10"/>`;
      // Beilage: Kartoffeln
      [[40,40],[72,26],[56,66],[28,80],[84,58]].forEach(([dx,dy])=>g+=`<ellipse cx="${cx+dx}" cy="${cy+dy}" rx="15" ry="11" fill="#e8c878" stroke="#9a7a3a" transform="rotate(${(dx*7)%40-20} ${cx+dx} ${cy+dy})"/>`);
      // Glas Wasser und Öl
      g+=`<path d="M370,90 L410,90 L404,170 L376,170 Z" fill="#cfe6f6" stroke="#5a8aaa" stroke-width="1.3"/><path d="M372,110 L408,110" stroke="#8ab8d8"/>`+T(390,188,'Wasser','var(--ink)',9.5,800,'middle');
      g+=`<path d="M390,222 q-12,16 0,26 q12,-10 0,-26 Z" fill="#e8c840" stroke="#8a7a10"/>`+T(390,268,'1 EL Öl','var(--ink)',9.5,800,'middle');
      // Legende
      const L=[['#b8d89a','½ Gemüse & Salat','Volumen, Ballaststoffe, wenig kcal'],['#e8b49a','¼ Eiweiß','Fisch, Geflügel, Ei, Hülsenfrüchte, Tofu, Quark'],['#f2dca2','¼ Sättigungsbeilage','Kartoffeln, Vollkorn, Reis, Nudeln'],['#e8c840','Fett sparsam','pflanzliche Öle, Nüsse'],['#cfe6f6','Trinken','Wasser, Tee, ungesüßt']];
      L.forEach((l,i)=>{ const y=44+i*50; g+=`<rect x="450" y="${y}" width="22" height="22" rx="5" fill="${l[0]}" stroke="${shade(l[0],-.4)}"/>`+T(482,y+11,l[1],'var(--ink)',11.5,800)+T(482,y+26,l[2],'var(--muted)',9,600); });
      return {vb:'0 0 760 310',breit:true,leg:[],svg:g}; },

    ern_100kcal(){ seed=3108; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='start')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      const D=[['Öl',11,'#e8c840'],['Butter',13,'#f2e08a'],['Schokolade',19,'#8a5a3a'],['Chips',19,'#e8b84a'],['Gouda',28,'#f2c860'],['Vollkornbrot',50,'#b88a5a'],['Hähnchen',91,'#f2c8b0'],['Kartoffeln',139,'#e8cc88'],['Magerquark',149,'#f6f2ea'],['Apfel',189,'#d9584a'],['Brokkoli',294,'#5a9a42'],['Erdbeeren',313,'#e0484a'],['Gurke',714,'#7ab85a']];
      const k=2.15, base=212; let x=14;
      D.forEach((d,i)=>{ const r=k*Math.sqrt(d[1]); const cx=x+r; x+=2*r+(i<5?14:10);
        g+=`<circle cx="${cx.toFixed(1)}" cy="${(base-r).toFixed(1)}" r="${r.toFixed(1)}" fill="${d[2]}" stroke="${shade(d[2],-.45)}" stroke-width="1.2"><animate attributeName="r" from="0" to="${r.toFixed(1)}" dur=".6s" begin="${(i*0.08).toFixed(2)}s" fill="freeze"/></circle>`;
        const yl=base+16+(i<9?(i%2)*24:0);
        g+=T(cx,yl,d[0],'var(--ink)',9.5,800,'middle')+T(cx,yl+12,d[1]+' g','var(--muted)',9,700,'middle'); });
      g+=`<path d="M8,${base} L752,${base}" stroke="#8a7a68" stroke-width="1.4"/>`;
      g+=T(14,28,'So viel sind 100 kcal','var(--ink)',13,800)+T(14,44,'Fläche ∝ Gewicht – links energiedicht, rechts energiearm','var(--muted)',9.5,600);
      return {vb:'0 0 760 270',breit:true,leg:[],svg:g}; },
