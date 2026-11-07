    gicht_stress(){ seed=2301; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='start')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      g+=`<defs><marker id="gst_pf" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#b8483a"/></marker><marker id="gst_pb" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6a5a48"/></marker></defs>`;
      // Knoten: [x, y, Farbe, Titel, Zeile1, Zeile2]
      const N=[
        [22,20,'#f3d9b0','Stresshormone','Adrenalin, Noradrenalin,','Cortisol steigen'],
        [22,152,'#d9d2ec','Schlaf','Schlafmangel, Schichtarbeit,','Schlafapnoe'],
        [22,284,'#f6cfc4','Entzündung','Insulinresistenz,','Entzündungsbereitschaft ❓'],
        [538,20,'#cfe2f0','Niere','Durchblutung ↓ ❓, Laktat','bremst die Ausscheidung'],
        [538,152,'#d4ead8','Trinken','vergessen → Urin','konzentriert, Austrocknung'],
        [538,284,'#f1e2bf','Essen & Trinken','Stressessen, Alkohol, Süßes,','ausgelassene Mahlzeiten']];
      // Sammelleitungen außen zum Ergebnis
      g+=`<path d="M22,62 L10,62 L10,458 L196,458" stroke="#6a5a48" stroke-width="1.6" fill="none" marker-end="url(#gst_pb)"/>`;
      g+=`<path d="M22,194 L10,194 M22,326 L10,326" stroke="#6a5a48" stroke-width="1.6"/>`;
      g+=`<path d="M738,62 L750,62 L750,458 L564,458" stroke="#6a5a48" stroke-width="1.6" fill="none" marker-end="url(#gst_pb)"/>`;
      g+=`<path d="M738,194 L750,194 M738,326 L750,326" stroke="#6a5a48" stroke-width="1.6"/>`;
      // Pfeile vom Stress zu den Knoten (fließend)
      const cx=380, cy=196;
      N.forEach((n,i)=>{ const links=n[0]<300; const ex=links?n[0]+200:n[0]; const ey=n[1]+42;
        const sx=cx+(links?-1:1)*70*Math.cos(Math.atan2(ey-cy,Math.abs(ex-cx))); const sy=cy+70*Math.sin(Math.atan2(ey-cy,Math.abs(ex-cx)));
        g+=`<path d="M${R(sx)},${R(sy)} L${ex+(links?4:-4)},${ey}" stroke="#b8483a" stroke-width="2" fill="none" stroke-dasharray="6 4" marker-end="url(#gst_pf)"><animate attributeName="stroke-dashoffset" values="20;0" dur="1.2s" repeatCount="indefinite"/></path>`; });
      // Knoten-Kästen
      N.forEach(n=>{ const [x,y,f,t,a,b]=n;
        g+=`<rect x="${x}" y="${y}" width="200" height="84" rx="10" fill="${lg(f,shade(f,-.12),90)}" stroke="${shade(f,-.45)}" stroke-width="1.4"/>`;
        g+=`<rect x="${x}" y="${y}" width="8" height="84" rx="4" fill="${shade(f,-.35)}"/>`;
        g+=T(x+18,y+26,t,'var(--ink)',13,700)+T(x+18,y+48,a,'var(--muted)',10,600)+T(x+18,y+64,b,'var(--muted)',10,600); });
      // Stress in der Mitte
      g+=`<circle cx="${cx}" cy="${cy}" r="70" fill="#e0503a" opacity=".18"><animate attributeName="r" values="66;84;66" dur="2.6s" repeatCount="indefinite"/><animate attributeName="opacity" values=".26;.06;.26" dur="2.6s" repeatCount="indefinite"/></circle>`;
      g+=`<circle cx="${cx}" cy="${cy}" r="66" fill="${lg('#f7c9b6','#e48a6c',90)}" stroke="#a8402e" stroke-width="1.6"/>`;
      for(let i=0;i<14;i++){ const a=i/14*Math.PI*2+rnd()*.2, r1=50+rnd()*6, r2=60+rnd()*4; g+=`<path d="M${R(cx+Math.cos(a)*r1)},${R(cy+Math.sin(a)*r1)} L${R(cx+Math.cos(a+.05)*r2)},${R(cy+Math.sin(a+.05)*r2)}" stroke="#a8402e" stroke-width=".8" opacity=".5"/>`; }
      g+=T(cx,cy-4,'Stress','#7a2a1c',20,800,'middle')+T(cx,cy+16,'Arbeit, Termine,','#7a2a1c',10,600,'middle')+T(cx,cy+30,'Ärger, Druck','#7a2a1c',10,600,'middle');
      // Ergebnis unten
      g+=`<rect x="200" y="420" width="360" height="80" rx="12" fill="${lg('#fbe3d6','#f0b8a0',90)}" stroke="#a8402e" stroke-width="1.6"/>`;
      g+=T(380,448,'Harnsäure ↑  +  Entzündungsbereitschaft ↑','#7a2a1c',13,800,'middle')+T(380,470,'→ Gichtanfall wahrscheinlicher','#7a2a1c',12,700,'middle')+T(380,488,'(vor allem, wenn die Harnsäure schon hoch ist)','#7a2a1c',9.5,600,'middle');
      // Kristallnadeln
      for(let i=0;i<9;i++){ const x=222+rnd()*30, y=436+rnd()*48, a=rnd()*Math.PI; g+=`<path d="M${R(x)},${R(y)} L${R(x+Math.cos(a)*14)},${R(y+Math.sin(a)*14)}" stroke="#e8eef4" stroke-width="2.2" stroke-linecap="round"><animate attributeName="opacity" values="1;.4;1" dur="${(1.5+rnd()).toFixed(2)}s" repeatCount="indefinite"/></path>`; }
      // Rückkopplung
      g+=`<path d="M548,422 C590,380 560,300 446,236" stroke="#8a7a68" stroke-width="1.4" fill="none" stroke-dasharray="3 4" marker-end="url(#gst_pb)"/>`;
      g+=T(394,356,'Schmerz und schlechter','var(--muted)',9.5,600)+T(394,369,'Schlaf verstärken Stress','var(--muted)',9.5,600);
      g+=T(366,356,'akuter Stress für den Körper:','var(--muted)',9.5,600,'end')+T(366,369,'OP, Infekt, Unfall – Leitlinie','var(--muted)',9.5,600,'end');
      g+=T(380,512,'Pfeile = Wege, die Studien nahelegen oder die als Auslöser anerkannt sind; ❓ = beim Menschen wenig untersucht','var(--muted)',8.5,600,'middle');
      return {vb:'0 0 760 520',breit:true,leg:[],svg:g}; },
    gicht_naturstoffe(){ seed=2302; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='start')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      const box=(x,y,w,h,f,st)=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="9" fill="${lg(f,shade(f,-.12),90)}" stroke="${st}" stroke-width="1.4"/>`;
      const pf=(d,c='#6a5a48')=>`<path d="${d}" stroke="${c}" stroke-width="1.8" fill="none" marker-end="url(#gns_pf)"/>`;
      const tag=(x,y,w,zeilen,f,st,c)=>{ let s=`<rect x="${x}" y="${y}" width="${w}" height="${14+zeilen.length*14}" rx="8" fill="${f}" stroke="${st}" stroke-width="1.3"/>`; zeilen.forEach((z,i)=>{ s+=T(x+10,y+19+i*14,z,i?c:st,i?9.5:10.5,i?600:800); }); return s; };
      const strich=(d,c)=>`<path d="${d}" stroke="${c}" stroke-width="1.5" fill="none" stroke-dasharray="4 3"/>`;
      g+=`<defs><marker id="gns_pf" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6a5a48"/></marker></defs>`;
      // Ablauf
      g+=box(20,190,120,48,'#efe2c4','#9a7a58')+T(80,210,'Purine','var(--ink)',12,700,'middle')+T(80,226,'Essen, Zellabbau','var(--muted)',9,600,'middle');
      g+=pf('M142,214 L172,214');
      g+=`<ellipse cx="196" cy="214" rx="22" ry="15" fill="${lg('#a8c8e0','#6f98b8',90)}" stroke="#3f6a8a" stroke-width="1.3"/>`+T(196,218,'XO','#1f4a6a',10,800,'middle');
      g+=pf('M220,214 L250,214');
      g+=box(252,190,150,48,'#f2c2a2','#9a6a48')+T(327,210,'Harnsäure','var(--ink)',12,700,'middle')+T(327,226,'im Blut','var(--muted)',9,600,'middle');
      g+=pf('M404,200 C440,180 452,110 478,96');
      g+=box(480,64,150,48,'#d6e6f2','#4f7a9a')+T(555,84,'Niere','var(--ink)',12,700,'middle')+T(555,100,'Ausscheidung (URAT1)','var(--muted)',9,600,'middle');
      g+=pf('M632,88 L656,88');
      g+=box(658,64,92,48,'#f2ecc8','#9a8a48')+T(704,84,'Urin','var(--ink)',12,700,'middle')+T(704,100,'pH zählt','var(--muted)',9,600,'middle');
      g+=pf('M404,228 C440,250 444,300 468,316');
      g+=box(470,296,130,48,'#eef2f6','#7a8a9a')+T(535,316,'Uratkristalle','var(--ink)',12,700,'middle')+T(535,332,'im Gelenk','var(--muted)',9,600,'middle');
      g+=pf('M602,320 L624,320');
      g+=`<rect x="626" y="296" width="124" height="48" rx="9" fill="#e0503a" opacity=".2"><animate attributeName="opacity" values=".12;.38;.12" dur="2.2s" repeatCount="indefinite"/></rect>`;
      g+=box(626,296,124,48,'#f6cfc4','#a8402e')+T(688,316,'Entzündung','var(--ink)',12,700,'middle')+T(688,332,'NLRP3 → IL-1β','var(--muted)',9,600,'middle');
      // Angriffspunkte
      g+=strich('M196,230 L160,292','#3f7a3a')+tag(20,292,250,['① Bildung bremsen (XO-Hemmung)','Quercetin, Luteolin/Apigenin (Sellerie),','OPC – meist Labor, kleine Studien'],'#e6f2df','#3f7a3a','var(--ink)');
      g+=strich('M300,62 L478,80','#3f7a3a')+tag(20,20,280,['② Ausscheidung fördern','Vitamin C (urikosurisch, RCT-Meta-Analyse)','Tees: mehr Urin – Brennnessel, Birke, Goldrute'],'#e6f2df','#3f7a3a','var(--ink)');
      g+=strich('M704,114 L704,132','#3f7a3a')+tag(640,132,112,['③ Urin-pH ↑','Citrat, Natron:','Harnsäure im','Urin löslicher'],'#e6f2df','#3f7a3a','var(--ink)');
      g+=strich('M555,114 L555,132','#b8483a')+tag(446,132,184,['✕ bremst Ausscheidung','Salicylat niedrig dosiert','(Weidenrinde ❓), Laktat,','Alkohol, Fasten'],'#fbe3e0','#b8483a','var(--ink)');
      g+=strich('M688,346 L688,372','#3f7a3a')+tag(420,372,330,['④ Entzündung dämpfen','Kirschen (Anthocyane), Curcumin, Gingerole,','Harpagosid (Teufelskralle), Omega-3','Arzneimittel: Colchicin (aus der Herbstzeitlose)'],'#e6f2df','#3f7a3a','var(--ink)');
      // wandernder Punkt
      g+=`<circle r="5" fill="#d9822b" stroke="#fff" stroke-width="1.2"><animateMotion dur="5s" repeatCount="indefinite" path="M80,214 L196,214 L327,214 C420,240 444,300 535,320 L688,320"/></circle>`;
      g+=T(20,410,'Grün = möglicher Angriffspunkt eines Naturstoffs,','var(--muted)',9.5,600)+T(20,424,'rot = bremst die Ausscheidung.','var(--muted)',9.5,600)+T(20,438,'Wie stark die Belege sind: siehe Tabelle.','var(--muted)',9.5,600);
      return {vb:'0 0 760 450',breit:true,leg:[],svg:g}; },
