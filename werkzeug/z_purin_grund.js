    purin_grundgeruest(){ seed=2406; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='start')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      const box=(x,y,w,h,f,st)=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="9" fill="${lg(f,shade(f,-.12),90)}" stroke="${st}" stroke-width="1.3"/>`;
      const pf=(d,c='#6a5a48')=>`<path d="${d}" stroke="${c}" stroke-width="1.7" fill="none" marker-end="url(#pg_pf)"/>`;
      g+=`<defs><marker id="pg_pf" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6a5a48"/></marker></defs>`;
      // Purin-Doppelring
      const cx=110, cy=150, r=44, P=[];
      for(let k=0;k<6;k++){ const a=(-90+60*k)*Math.PI/180; P.push([cx+r*Math.cos(a), cy+r*Math.sin(a)]); }
      // P0 oben C6, P1 rechts oben C5, P2 rechts unten C4, P3 unten N3, P4 links unten C2, P5 links oben N1
      const ex=P[1][0], m=(P[1][1]+P[2][1])/2, s=r, dp=s*1.539; // Abstand Kante → Spitze im Fünfeck
      const N9=[ex+s*0.425, P[2][1]+s*0.309-0.0], C8=[ex+dp, m], N7=[ex+s*0.425, P[1][1]-s*0.309];
      g+=`<path d="M${P.map(p=>p.map(v=>v.toFixed(1)).join(',')).join(' L')} Z" fill="#efe2c4" stroke="#7a5a38" stroke-width="2.4"/>`;
      g+=`<path d="M${P[2][0].toFixed(1)},${P[2][1].toFixed(1)} L${N9.map(v=>v.toFixed(1)).join(',')} L${C8.map(v=>v.toFixed(1)).join(',')} L${N7.map(v=>v.toFixed(1)).join(',')} L${P[1][0].toFixed(1)},${P[1][1].toFixed(1)}" fill="#e6d2b0" stroke="#7a5a38" stroke-width="2.4"/>`;
      const at=(p,t,c)=>`<circle cx="${p[0].toFixed(1)}" cy="${p[1].toFixed(1)}" r="10" fill="${c}" stroke="#5a4028" stroke-width="1"/>`+T(p[0],p[1]+4,t,'#fff',10,800,'middle').replace('stroke:var(--surface);stroke-width:3','stroke:none');
      [[P[5],'N'],[P[3],'N'],[N9,'N'],[N7,'N']].forEach(a=>g+=at(a[0],a[1],'#3f6a9a'));
      [[P[0],'C'],[P[1],'C'],[P[2],'C'],[P[4],'C'],[C8,'C']].forEach(a=>g+=at(a[0],a[1],'#6a6a6a'));
      g+=T(cx+30,58,'Purin-Grundgerüst','var(--ink)',12,800,'middle')+T(cx+30,74,'Sechsring + Fünfring, 4 × Stickstoff','var(--muted)',9.5,600,'middle');
      g+=T(cx+30,226,'Variationen am Gerüst ergeben','var(--muted)',9.5,600,'middle')+T(cx+30,240,'Adenin, Guanin, Koffein …','var(--muted)',9.5,600,'middle');
      // Verwendung
      const U=[['Adenin & Guanin','Buchstaben der Erbsubstanz DNA/RNA','#d9cfe8','#6a5a8a'],['ATP & GTP','Energieträger jeder Zelle','#f3d9b4','#9a6a38'],['cAMP','Botenstoff in der Zelle','#cfe0c4','#5a7a48']];
      U.forEach((u,i)=>{ const y=40+i*66; g+=box(268,y,200,50,u[2],u[3])+T(368,y+21,u[0],'var(--ink)',11.5,800,'middle')+T(368,y+38,u[1],'var(--muted)',9,600,'middle')+pf(`M${(C8[0]+14).toFixed(0)},${(cy+(i-1)*14).toFixed(0)} C230,${cy+(i-1)*14} 236,${y+25} 264,${y+25}`); });
      g+=T(368,256,'→ viele Zellkerne = viele Purine','#7a4a28',10,800,'middle')+T(368,271,'Innereien, Sprotten, Hefe, Keimlinge','var(--muted)',9,600,'middle')+T(368,285,'wenig: Fett, Öl, Milch, Ei','var(--muted)',9,600,'middle');
      // Abbau
      const K=[['Hypoxanthin',40],['Xanthin',112],['Harnsäure',184]];
      K.forEach((k,i)=>{ const f=i==2?'#f2c2a2':'#f1e2c8'; g+=box(540,k[1],180,40,f,'#9a7a58')+T(630,k[1]+25,k[0],'var(--ink)',12,800,'middle'); if(i<2) g+=pf(`M630,${k[1]+41} L630,${K[i+1][1]-3}`)+T(642,k[1]+60,'Xanthinoxidase','#2f5a7a',9,700); });
      g+=pf('M470,65 C500,62 512,60 536,60');
      g+=T(630,26,'Abbau beim Menschen','var(--ink)',11,800,'middle');
      g+=`<rect x="520" y="246" width="220" height="56" rx="9" fill="${lg('#eef2f6','#dde6ee',90)}" stroke="#7a8a9a" stroke-dasharray="4 3"/>`+T(630,266,'Koffein, Theobromin (Methylxanthine)','var(--ink)',9.5,800,'middle')+T(630,281,'→ Methylharnsäuren, nicht Harnsäure','var(--muted)',9,600,'middle')+T(630,295,'(Kaffee, Tee, Kakao)','var(--muted)',9,600,'middle');
      return {vb:'0 0 760 312',breit:true,leg:[],svg:g}; },
