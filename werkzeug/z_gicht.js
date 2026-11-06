    gicht_purinweg(){ seed=2101; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='start')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      const box=(x,y,w,h,f,st)=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="9" fill="${lg(f,shade(f,-.12),90)}" stroke="${st}" stroke-width="1.4"/>`;
      const pf=(d,c='#6a5a48')=>`<path d="${d}" stroke="${c}" stroke-width="1.8" fill="none" marker-end="url(#gpw_pf)"/>`;
      g+=`<defs><marker id="gpw_pf" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6a5a48"/></marker></defs>`;
      // Quellen
      const Q=[['Nahrung','Fleisch, Fisch, Bier …','#e8c9a0'],['Zellabbau','DNA und RNA','#d9cfe8'],['Eigensynthese','vor allem Leber','#cfe0c4']];
      Q.forEach((q,i)=>{ const y=30+i*62; g+=box(18,y,170,44,q[2],shade(q[2],-.35))+T(103,y+19,q[0],'var(--ink)',11,700,'middle')+T(103,y+34,q[1],'var(--muted)',9,600,'middle')+pf(`M190,${y+22} C230,${y+22} 236,${94} 256,${94}`); });
      // Kette
      const K=[['Purine (AMP, GMP)',74,'#efe2c4'],['Hypoxanthin',150,'#f1dcc0'],['Xanthin',226,'#f3d4b4'],['Harnsäure',302,'#f2c2a2']];
      K.forEach((k,i)=>{ g+=box(260,k[1],200,40,k[2],'#9a7a58')+T(360,k[1]+25,k[0],'var(--ink)',12,700,'middle'); if(i<3) g+=pf(`M360,${k[1]+41} L360,${K[i+1][1]-2}`); });
      // Enzym
      [[190,'Xanthinoxidase'],[266,'Xanthinoxidase']].forEach(e=>{ g+=`<ellipse cx="400" cy="${e[0]+12}" rx="9" ry="7" fill="#7aa6c8" stroke="#3f6a8a"/>`+T(416,e[0]+16,e[1],'#2f5a7a',10); });
      // Hemmer
      g+=`<rect x="548" y="196" width="196" height="56" rx="10" fill="${lg('#fbe3e0','#f2c8c2',90)}" stroke="#b8483a" stroke-width="1.4"/>`+T(646,218,'Allopurinol, Febuxostat','#9a2f22',11,700,'middle')+T(646,236,'blockieren das Enzym','#9a2f22',10,600,'middle');
      g+=`<path d="M546,214 C530,210 524,202 514,202" stroke="#b8483a" stroke-width="2" fill="none" stroke-dasharray="5 3"/><path d="M546,236 C530,250 524,278 514,278" stroke="#b8483a" stroke-width="2" fill="none" stroke-dasharray="5 3"/>`;
      g+=`<path d="M391,194 L409,210 M409,194 L391,210 M391,270 L409,286 M409,270 L391,286" stroke="#b8483a" stroke-width="2.4"/>`;
      // Uricase fehlt
      g+=pf('M462,322 L590,322','#9a8a78')+`<path d="M516,312 L536,332 M536,312 L516,332" stroke="#b8483a" stroke-width="2.6"/>`+T(526,348,'Uricase fehlt dem Menschen','#9a2f22',9.5,700,'middle');
      g+=box(594,302,150,40,'#e6ecd8','#7a8a5a')+T(669,320,'Allantoin','var(--ink)',11,700,'middle')+T(669,334,'(die meisten Säugetiere)','var(--muted)',8.5,600,'middle');
      // Ausscheidung
      g+=pf('M330,343 C320,370 260,372 252,388')+pf('M390,343 C400,370 460,372 468,388');
      g+=box(150,390,200,44,'#d6e6f2','#4f7a9a')+T(250,409,'Niere ≈ 2/3','var(--ink)',12,700,'middle')+T(250,425,'URAT1, GLUT9, ABCG2','var(--muted)',9,600,'middle');
      g+=box(372,390,200,44,'#e8dccb','#8a6a48')+T(472,409,'Darm ≈ 1/3','var(--ink)',12,700,'middle')+T(472,425,'ABCG2 – Bakterien bauen ab','var(--muted)',9,600,'middle');
      // wandernder Punkt
      g+=`<circle r="5" fill="#d9822b" stroke="#fff" stroke-width="1.2"><animateMotion dur="6s" repeatCount="indefinite" path="M360,94 L360,170 L360,246 L360,322 L250,410"/></circle>`;
      g+=T(18,232,'Purine sind Bausteine','var(--muted)',9.5,600)+T(18,246,'des Erbguts und der','var(--muted)',9.5,600)+T(18,260,'Energieträger (ATP).','var(--muted)',9.5,600);
      return {vb:'0 0 760 446',breit:true,leg:[],svg:g}; },
    gicht_gelenk(){ seed=2202; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='start')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      // Weichteil / Zehe
      g+=`<path d="M20,150 C60,110 250,96 330,130 C350,150 350,250 330,270 C250,304 60,290 20,250 Z" fill="${lg('#f3cdb4','#e2a888',90)}" stroke="#b07a5a" stroke-width="1.4"/>`;
      // Entzündungsglühen
      g+=`<ellipse cx="180" cy="200" rx="110" ry="80" fill="#e0503a" opacity=".22"><animate attributeName="opacity" values=".12;.34;.12" dur="2.4s" repeatCount="indefinite"/></ellipse>`;
      // Knochen
      g+=`<path d="M24,170 L140,170 C162,170 172,184 172,200 C172,216 162,230 140,230 L24,230 Z" fill="${lg('#fbf6e8','#e2d8bc',90)}" stroke="#a8986e" stroke-width="1.4"/>`;
      g+=`<path d="M326,176 L222,176 C204,176 194,188 194,200 C194,212 204,224 222,224 L326,224 Z" fill="${lg('#fbf6e8','#e2d8bc',90)}" stroke="#a8986e" stroke-width="1.4"/>`;
      // Knorpel
      g+=`<path d="M140,172 C160,174 170,186 170,200 C170,214 160,226 140,228" stroke="#8ab8d0" stroke-width="5" fill="none" opacity=".9"/><path d="M222,178 C206,180 196,190 196,200 C196,210 206,220 222,222" stroke="#8ab8d0" stroke-width="5" fill="none" opacity=".9"/>`;
      // Kapsel
      g+=`<path d="M128,160 C150,140 216,140 238,162 L238,238 C216,260 150,260 128,240 Z" fill="#f6e9b0" fill-opacity=".45" stroke="#c49a4a" stroke-width="1.6" stroke-dasharray="6 3"/>`;
      // Kristalle
      let k=''; for(let i=0;i<34;i++){ const x=150+rnd()*68, y=152+rnd()*96, a=rnd()*Math.PI, l=6+rnd()*9; k+=`M${(x-Math.cos(a)*l/2).toFixed(1)},${(y-Math.sin(a)*l/2).toFixed(1)} L${(x+Math.cos(a)*l/2).toFixed(1)},${(y+Math.sin(a)*l/2).toFixed(1)} `; }
      g+=`<path d="${k}" stroke="#ffffff" stroke-width="1.6" stroke-linecap="round"/><path d="${k}" stroke="#8aa0b8" stroke-width=".6" stroke-linecap="round"/>`;
      // Tophus
      g+=`<ellipse cx="260" cy="126" rx="22" ry="12" fill="#f4f1e6" stroke="#b8ae96"/>`;
      g+=T(120,52,'Großzehengrundgelenk (Podagra)','var(--ink)',12,700)+T(120,68,'Mittelfußknochen  |  Zehenglied','var(--muted)',9.5,600);
      g+=`<path d="M184,166 L120,96" stroke="var(--muted)" stroke-width=".9"/>`+T(26,92,'Uratkristalle (Nadeln)','var(--ink)',10);
      g+=`<path d="M258,116 L284,92" stroke="var(--muted)" stroke-width=".9"/>`+T(250,86,'Tophus','var(--ink)',10);
      g+=`<path d="M150,252 L120,318" stroke="var(--muted)" stroke-width=".9"/>`+T(40,332,'Gelenkkapsel mit Gelenkflüssigkeit','var(--ink)',10);
      g+=`<path d="M206,214 L240,318" stroke="var(--muted)" stroke-width=".9"/>`+T(206,348,'Knorpel','var(--ink)',10);
      // Kaskade
      const S=[['Uratkristalle lagern sich ab','#eef0f4'],['Makrophagen fressen Kristalle','#efe4d4'],['NLRP3-Inflammasom springt an','#f3dcc4'],['Interleukin-1β wird frei','#f6cfb4'],['Neutrophile strömen ein','#f6c0a4'],['Schmerz, Rötung, Schwellung','#f2a88a']];
      S.forEach((s,i)=>{ const y=30+i*56; g+=`<rect x="380" y="${y}" width="220" height="36" rx="9" fill="${lg(s[1],shade(s[1],-.1),90)}" stroke="#9a6a50" stroke-width="1.3"/>`+T(490,y+22,s[0],'var(--ink)',10.5,700,'middle');
        if(i<5) g+=`<path d="M490,${y+37} L490,${y+54}" stroke="#9a6a50" stroke-width="1.8"/><path d="M485,${y+48} L490,${y+55} L495,${y+48}" fill="#9a6a50"/>`; });
      g+=`<rect x="380" y="30" width="220" height="36" rx="9" fill="none" stroke="#d9822b" stroke-width="2.4" opacity="0"><animate attributeName="y" values="30;86;142;198;254;310" dur="6s" repeatCount="indefinite" calcMode="discrete"/><animate attributeName="opacity" values="1" dur="6s" repeatCount="indefinite"/></rect>`;
      // Angriffspunkte
      const A=[[142,'IL-1-Hemmer','(Ausnahmefälle)',198],[198,'Colchicin','bremst Neutrophile',254],[254,'NSAR','gegen Prostaglandine',310],[310,'Kortison','dämpft breit',282]];
      A.forEach(a=>{ g+=`<rect x="626" y="${a[0]}" width="122" height="36" rx="18" fill="${lg('#dceedd','#b8dcbc',90)}" stroke="#3f7a4a" stroke-width="1.3"/>`+T(687,a[0]+16,a[1],'#2f5a36',10.5,700,'middle')+T(687,a[0]+29,a[2],'#2f5a36',8.5,600,'middle')+`<path d="M626,${a[0]+18} L604,${a[3]-12}" stroke="#3f7a4a" stroke-width="1.6" stroke-dasharray="4 3"/>`; });
      return {vb:'0 0 760 360',breit:true,leg:[],svg:g}; },
    gicht_skala(){ seed=2303; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='start')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      const X=v=>60+v*55;
      g+=`<defs><linearGradient id="gsk_v" x1="0" x2="1"><stop offset="0" stop-color="#8fc48a"/><stop offset=".42" stop-color="#cfe08a"/><stop offset=".57" stop-color="#f2c45a"/><stop offset=".75" stop-color="#e8875a"/><stop offset="1" stop-color="#c8443a"/></linearGradient></defs>`;
      g+=`<rect x="${X(0)}" y="110" width="${X(12)-X(0)}" height="30" rx="8" fill="url(#gsk_v)" stroke="#8a6a50" stroke-width="1.2"/>`;
      for(let v=0;v<=12;v++) g+=`<path d="M${X(v)},140 L${X(v)},147" stroke="#6a5a48"/>`+T(X(v),160,v,'var(--muted)',9.5,600,'middle');
      g+=T(X(12)+4,180,'mg/dl Harnsäure im Blut','var(--muted)',9.5,600,'end');
      // Marken
      const M=(v,c,up,l1,l2,a='middle',dx=0)=>{ const y1=up?100:150, y2=up?60:196; g+=`<path d="M${X(v)},${up?108:142} L${X(v)},${y1}" stroke="${c}" stroke-width="2.2"/><path d="M${X(v)},${y1} L${X(v)},${up?y2+8:y2-14}" stroke="${c}" stroke-width="1" stroke-dasharray="3 2"/>`+T(X(v)+dx,up?y2-4:y2,l1,c,10.5,700,a)+T(X(v)+dx,up?y2+10:y2+14,l2,c,9,600,a); };
      M(5,'#2f6a3a',false,'Ziel < 5','bei Tophi / schwerer Gicht','end',14);
      M(6,'#2f6a3a',true,'Ziel < 6','für alle mit Harnsäuresenkung');
      M(6.8,'#9a2f22',false,'6,8 Löslichkeitsgrenze','bei 37 °C – darüber Kristalle möglich','start',-12);
      g+=`<path d="M${X(7.6)},62 L${X(11.8)},62" stroke="#c8443a" stroke-width="1"/>`+T(X(9.7),56,'Hyperurikämie: Kristalle können ausfallen','#9a2f22',10,700,'middle');
      // Treat-to-target
      g+=`<g><path d="M0,0 L-7,-12 L7,-12 Z" fill="#3a3028"/><animateTransform attributeName="transform" type="translate" values="${X(9.5)},108;${X(5.6)},108;${X(5.6)},108;${X(9.5)},108" keyTimes="0;.45;.85;1" dur="7s" repeatCount="indefinite"/></g>`;
      g+=T(X(0),30,'Treat-to-Target: Medikament langsam steigern, bis der Zielwert erreicht ist','var(--ink)',11,700);
      g+=T(X(0),238,'Im akuten Anfall kann der Wert normal sein – Kontrolle ca. 2 Wochen danach (S3-Leitlinie).','var(--muted)',9.5,600);
      return {vb:'0 0 760 252',breit:true,leg:[],svg:g}; },
    gicht_purine(){ seed=2404; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='start')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      const F={inn:'#a8443a',fis:'#4f86b0',fle:'#b07a4a',get:'#c8a050',gem:'#6aa04a',mil:'#d8c89a'};
      const D=[['Kalbsbries','inn',1260],['Rinderleber','inn',554],['Schweineniere','inn',334],['Jakobsmuscheln','fis',330],['Anchovis / Sardellen','fis',239],['Lachs','fis',170],['Schweinefleisch','fle',150],['Hähnchen ohne Haut','fle',120],['Rinderfilet','fle',110],['Haferflocken','get',100],['Erbsen, gegart','gem',86],['Spinat','gem',57],['Reis, gegart','get',33],['Kartoffeln, gegart','gem',15],['Apfel','gem',14],['Ei','mil',5],['Joghurt','mil',0]];
      const x0=190, sc=470/1260;
      g+=T(20,22,'Harnsäure aus Purinen, mg pro 100 g (DGE 2010; Leber: ernaehrung.de)','var(--ink)',11,700);
      D.forEach((d,i)=>{ const y=40+i*22, w=Math.max(1.5,d[2]*sc), c=F[d[1]];
        g+=T(x0-8,y+13,d[0],'var(--ink)',10,600,'end')+`<rect x="${x0}" y="${y+2}" width="${w.toFixed(1)}" height="15" rx="4" fill="${lg(shade(c,.15),shade(c,-.15),90)}" stroke="${shade(c,-.35)}" stroke-width=".9"><animate attributeName="width" from="0" to="${w.toFixed(1)}" dur="1.2s" begin="${(i*0.06).toFixed(2)}s" fill="freeze"/></rect>`+T(x0+w+6,y+14,d[2],'var(--ink)',9.5,700); });
      const L=[['inn','Innereien'],['fis','Fisch & Meeresfrüchte'],['fle','Fleisch'],['get','Getreide'],['gem','Gemüse & Obst'],['mil','Milch & Ei']];
      let lx=20; L.forEach(l=>{ const x=lx; lx+=l[1].length*6.2+40; g+=`<rect x="${x}" y="428" width="12" height="12" rx="3" fill="${F[l[0]]}"/>`+T(x+17,438,l[1],'var(--muted)',9.5,600); });
      g+=T(740,410,'Faustregel: höchstens ca. 500 mg Harnsäure pro Tag','var(--muted)',9.5,600,'end');
      return {vb:'0 0 760 450',breit:true,leg:[],svg:g}; },
