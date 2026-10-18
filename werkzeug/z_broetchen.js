    broetchen_ablauf(){ seed=301; let g=`<path d="M150,10 V200 M300,10 V200 M450,10 V200 M600,10 V200 M750,10 V200" stroke="var(--line)" stroke-width="1"/>`;
      const teig=(x,y,rx,ry,f='#e8d2a0')=>`<ellipse cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" fill="${lg(shade(f,0.12),shade(f,-0.18),90)}" stroke="#a88a50" stroke-width="1.2"/>`;
      const schuessel=(x,y,w,h)=>`<path d="M${x-w/2},${y} Q${x-w/2},${y+h} ${x},${y+h} Q${x+w/2},${y+h} ${x+w/2},${y} Z" fill="${lg('#c8ccd2','#8a9098',0)}" stroke="#5a6068" stroke-width="1.4"/><path d="M${x-w/2-4},${y} H${x+w/2+4}" stroke="#5a6068" stroke-width="3" stroke-linecap="round"/>`;
      // 1 Kneten
      g+=vign(0,'1 · Kneten: 5 + 5 Min.',teig(75,120,40,20)+schuessel(75,118,96,60)+`<g><path d="M75,30 V100 M75,100 q-14,10 -6,26 q8,8 14,-2" stroke="#4a4f56" stroke-width="5" fill="none" stroke-linecap="round"/><animateTransform attributeName="transform" type="rotate" values="0 75 110;360 75 110" dur="3s" repeatCount="indefinite"/></g><text x="118" y="44" style="fill:var(--muted);font:700 11px var(--label)">Stufe 1</text>`);
      // 2 Kalte Gare
      g+=vign(1,'2 · Kalte Gare: 2 × 1 Std.',`<rect x="22" y="36" width="106" height="150" rx="8" fill="${lg('#eef3f6','#d4dde4',0)}" stroke="#8a98a4" stroke-width="1.4"/><path d="M22,100 H128" stroke="#8a98a4"/><text x="34" y="56" style="fill:#5a7a9a;font:700 12px var(--label)">❄ 4–7 °C</text>`+
        `<g>${teig(75,150,30,14)}<animateTransform attributeName="transform" type="scale" values="1 1;1.12 1.35;1 1" dur="5s" repeatCount="indefinite" additive="sum"/></g>`.replace('<g>','<g transform-origin="75 162">')+`<path d="M38,134 H112 V176 H38 Z" fill="none" stroke="#9aa4ae" stroke-dasharray="4 3"/>`);
      // 3 Falten
      g+=vign(2,'3 · Falten, dann wieder 1 Std.',teig(75,130,46,22)+`<path d="M34,124 q10,-34 40,-30" stroke="#b05a20" stroke-width="2.4" fill="none"/><path d="M116,124 q-10,-34 -40,-30" stroke="#b05a20" stroke-width="2.4" fill="none"/><path d="M70,96 l6,-4 l1,7" fill="#b05a20"/><path d="M80,96 l-6,-4 l-1,7" fill="#b05a20"/><path d="M40,138 Q75,150 110,138" stroke="#a88a50" fill="none" stroke-dasharray="3 3"/>`);
      // 4 Teilen & Formen
      let b4=''; for(let i=0;i<8;i++){ const x=30+(i%4)*30, y=110+Math.floor(i/4)*36; b4+=teig(x,y,12,9); }
      g+=vign(3,'4 · 8 Stücke, rund schleifen, längs rollen',b4+`<rect x="44" y="46" width="62" height="34" rx="6" fill="${lg('#f4f4f2','#d0d0cc',90)}" stroke="#8a8a84"/><text x="75" y="68" style="fill:var(--ink);font:800 13px var(--label);text-anchor:middle">80 g</text>`);
      // 5 Stueckgare & Einschneiden
      g+=vign(4,'5 · 30 Min. gehen, nach 15 Min. einschneiden',`<ellipse cx="75" cy="128" rx="44" ry="24" fill="${lg('#f0dcae','#cfae74',90)}" stroke="#a88a50" stroke-width="1.2"/><path d="M42,124 Q75,114 108,124" stroke="#7a5a2a" stroke-width="2.4" fill="none"/><path d="M96,74 L132,40" stroke="#6a6e74" stroke-width="4" stroke-linecap="round"/><path d="M96,74 L80,92" stroke="#3a2a1a" stroke-width="7" stroke-linecap="round"/><text x="16" y="176" style="fill:var(--muted);font:700 11px var(--label)">Küchentuch drüber</text>`);
      // 6 Backen mit Dampf
      let dampf=''; for(let i=0;i<3;i++) dampf+=`<path d="M${52+i*24},150 q-6,-12 0,-24 q6,-12 0,-24" stroke="#c8d4dc" stroke-width="3" fill="none" stroke-linecap="round" opacity="0"><animate attributeName="opacity" values="0;.9;0" dur="2.4s" begin="${i*0.6}s" repeatCount="indefinite"/><animateTransform attributeName="transform" type="translate" values="0 10;0 -14" dur="2.4s" begin="${i*0.6}s" repeatCount="indefinite"/></path>`;
      g+=vign(5,'6 · 220 °C, Dampf, 20 Min.',`<rect x="14" y="30" width="122" height="150" rx="8" fill="${lg('#3a3e44','#5a5f66',90)}" stroke="#22262a"/><rect x="24" y="44" width="102" height="122" rx="4" fill="${lg('#ffb050','#c8501a',90)}" opacity=".85"/><path d="M24,104 H126 M24,152 H126" stroke="#3a3e44" stroke-width="3"/>`+[40,75,110].map(x=>`<ellipse cx="${x}" cy="96" rx="15" ry="8" fill="${lg('#e8b060','#9a5a1a',90)}" stroke="#7a4a1a"/><path d="M${x-9},94 Q${x},90 ${x+9},94" stroke="#f0d8a0" stroke-width="1.6" fill="none"/>`).join('')+dampf+`<text x="75" y="22" style="fill:var(--ink);font:800 12px var(--label);text-anchor:middle">220 °C O/U</text>`);
      return {vb:'0 0 900 230', breit:true, leg:[], svg:g}; },
    gluten_netz(){ seed=302; let g='';
      const kette=(x,y,len,a,col,welle)=>{ let d=`M${x},${y}`; for(let i=1;i<=12;i++){ const t=i/12; const [px,py]=rot([[t*len,Math.sin(t*Math.PI*welle)*6]],x,y,a)[0]; d+=` L${R(px)},${R(py)}`; } return `<path d="${d}" stroke="${col}" stroke-width="3" fill="none" stroke-linecap="round"/>`; };
      // links: einzelne Eiweisse + Wasser
      g+=`<text x="110" y="24" style="fill:var(--ink);font:800 13px var(--label);text-anchor:middle">Mehl + Wasser</text>`;
      for(let i=0;i<6;i++) g+=kette(30+rnd()*120,50+rnd()*110,40,rnd()*360,'#c8901a',3);
      for(let i=0;i<5;i++){ const x=40+rnd()*130, y=60+rnd()*100; g+=`<circle cx="${R(x)}" cy="${R(y)}" r="7" fill="none" stroke="#b05a8a" stroke-width="2.4"/><circle cx="${R(x+5)}" cy="${R(y+4)}" r="5" fill="none" stroke="#b05a8a" stroke-width="2"/>`; }
      for(let i=0;i<14;i++) g+=`<circle cx="${R(25+rnd()*170)}" cy="${R(45+rnd()*125)}" r="2.2" fill="#5aa0d8"/>`;
      g+=`<path d="M215,110 H275" stroke="var(--ink)" stroke-width="2.4"/><path d="M275,110 l-10,-6 v12 z" fill="var(--ink)"/><text x="245" y="98" style="fill:var(--ink);font:800 12px var(--label);text-anchor:middle">Kneten</text>`;
      // rechts: Netzwerk mit Gasblasen
      g+=`<text x="410" y="24" style="fill:var(--ink);font:800 13px var(--label);text-anchor:middle">Glutennetz hält Gärgas</text>`;
      for(let r=0;r<5;r++) g+=kette(300,52+r*28,220,0,'#c8901a',4+r%2);
      for(let c=0;c<7;c++){ const x=310+c*33; g+=`<path d="M${x},50 L${x+6},170" stroke="#b05a8a" stroke-width="2" opacity=".8"/>`; }
      for(let i=0;i<7;i++) for(let j=0;j<4;j++) g+=`<circle cx="${313+i*33}" cy="${54+j*28}" r="2.6" fill="#7a4a1a"/>`;
      [[360,96,10],[430,128,13],[470,72,9],[395,150,8]].forEach(([x,y,r],i)=>g+=`<circle cx="${x}" cy="${y}" r="${r}" fill="${lg('#ffffff','#dfe8ee',90)}" stroke="#9aa8b4" stroke-width="1.2"><animate attributeName="r" values="${r*0.4};${r*1.15};${r*0.4}" dur="${4+i}s" repeatCount="indefinite"/></circle>`);
      g+=mk(60,186,1)+mk(130,186,2)+mk(168,186,3)+mk(470,186,4)+mk(330,186,5);
      return {vb:'0 0 540 200', breit:true, leg:['Glutenin: lange Eiweißketten – geben Festigkeit und Elastizität','Gliadin: knäuelige Eiweiße – machen den Teig dehnbar','Wasser: erst damit können sich die Eiweiße entfalten und verbinden','Kohlendioxid der Hefe sammelt sich in Bläschen, das Netz hält es fest – der Teig geht auf','Querverbindungen (Disulfid-Brücken, braune Punkte) entstehen beim Kneten und Falten'], svg:g}; },
    broetchen_quer(){ seed=303; let g='';
      g+=`<path d="M30,170 Q20,120 60,80 Q120,30 210,40 Q300,30 350,90 Q380,130 370,170 Z" fill="${lg('#e8a050','#8a4a14',90)}" stroke="#5a3010" stroke-width="2"/>`;
      g+=`<path d="M44,164 Q40,124 72,92 Q126,50 210,58 Q290,50 334,100 Q358,132 354,164 Z" fill="${lg('#fbf2dc','#efdcb0',90)}" stroke="#d8b878" stroke-width="1"/>`;
      for(let i=0;i<70;i++){ const x=70+rnd()*270, y=80+rnd()*80; if(y<100&&(x<110||x>310)) continue; g+=`<ellipse cx="${R(x)}" cy="${R(y)}" rx="${R(2+rnd()*6)}" ry="${R(1.5+rnd()*4)}" fill="#e4cc98" stroke="#cdb07a" stroke-width=".6"/>`; }
      g+=`<path d="M170,44 Q200,18 236,40 L228,56 Q204,40 178,58 Z" fill="${lg('#f4d8a0','#c8904a',0)}" stroke="#7a4a14"/>`;
      g+=`<path d="M30,170 H370" stroke="#6a3a10" stroke-width="3"/>`;
      g+=mk(200,22,1)+mk(52,110,2)+mk(210,120,3)+mk(380,178,4);
      return {vb:'0 0 400 200', breit:true, leg:['Ausbund: Am Schnitt reißt die Kruste kontrolliert auf – der Dampf hält sie dort lange weich','Kruste: Maillard-Reaktion und Karamellisierung ab etwa 140 °C – Farbe, Duft, Röstaroma','Krume: verkleisterte Stärke und geronnenes Klebereiweiß, Poren vom Gärgas','Boden: klingt hohl, wenn genug Wasser verdampft ist'], svg:g}; },
