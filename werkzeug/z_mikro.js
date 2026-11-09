    mn_vitd(){ seed=3201; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='start')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      const pf=(d,c='#6a5a48',w=1.8)=>`<path d="${d}" stroke="${c}" stroke-width="${w}" fill="none" marker-end="url(#vd_pf)"/>`;
      g+=`<defs><marker id="vd_pf" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#6a5a48"/></marker></defs>`;
      // Sonne
      g+=`<circle cx="46" cy="44" r="22" fill="#f6c840" stroke="#b88a10"><animate attributeName="r" values="22;24;22" dur="3s" repeatCount="indefinite"/></circle>`;
      for(let i=0;i<10;i++){ const a=i*36*Math.PI/180; g+=`<path d="M${(46+28*Math.cos(a)).toFixed(1)},${(44+28*Math.sin(a)).toFixed(1)} L${(46+36*Math.cos(a)).toFixed(1)},${(44+36*Math.sin(a)).toFixed(1)}" stroke="#e0a820" stroke-width="2"/>`; }
      g+=`<path d="M70,62 L118,108 M76,56 L126,100 M64,68 L110,114" stroke="#8a5ac8" stroke-width="1.6" stroke-dasharray="4 3"/>`+T(96,74,'UVB','#6a3aa8',10,800);
      const box=(x,y,w,h,f,t1,t2,t3)=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="10" fill="${f}" stroke="${shade(f,-.4)}" stroke-width="1.2"/>`+T(x+w/2,y+18,t1,'var(--ink)',11,800,'middle').replace('stroke:var(--surface)','stroke:'+f)+T(x+w/2,y+33,t2,'#3a3028',9,600,'middle').replace('stroke:var(--surface)','stroke:'+f)+(t3?T(x+w/2,y+46,t3,'#3a3028',9,600,'middle').replace('stroke:var(--surface)','stroke:'+f):'');
      g+=box(96,112,128,56,'#f2d0b8','① Haut','7-Dehydrocholesterin','→ Vitamin D3');
      g+=box(96,196,128,44,'#f6e6b0','Nahrung / Tablette','Fisch, Eigelb, D3/D2');
      g+=pf('M226,150 L262,150')+pf('M226,218 L262,170');
      g+=box(266,120,128,56,'#e8b49a','② Leber','→ 25(OH)D','Speicher, Blutwert');
      g+=pf('M396,150 L432,150');
      g+=box(436,120,128,56,'#d8a8a8','③ Niere','→ Calcitriol','aktives Hormon');
      g+=pf('M500,178 L470,214')+pf('M520,178 L560,214');
      g+=box(400,216,118,44,'#cfe0f2','Darm','Calcium ↑, Phosphat ↑')+box(530,216,118,44,'#e6e0d0','Knochen, Muskel','Abwehr, Gewebe');
      g+=T(330,196,'braucht Magnesium','#3a6a5a',9,700,'middle');
      // Monatsdiagramm Sonnenhöhe 49°N
      const dek=[-21,-13,-2.4,9.4,18.8,23.3,21.5,13.8,2.2,-9.6,-19,-23.3], M='JFMAMJJASOND'.split('');
      const X0=658, B=11, Y0=270, k=2.4; g+=T(786,26,'Mittagssonne Saarland (49° N)','var(--ink)',10.5,800,'end')+T(786,40,'Vitamin D erst über ca. 45°','var(--muted)',9,600,'end');
      dek.forEach((d,i)=>{ const h=90-49+d, x=X0+i*B, f=h>=45?'#f2b830':'#b8c4d0'; g+=`<rect x="${x}" y="${(Y0-h*k).toFixed(1)}" width="${B-2}" height="${(h*k).toFixed(1)}" rx="2" fill="${f}" stroke="${shade(f,-.35)}"><animate attributeName="height" from="0" to="${(h*k).toFixed(1)}" dur=".8s" begin="${(i*.05).toFixed(2)}s" fill="freeze"/><animate attributeName="y" from="${Y0}" to="${(Y0-h*k).toFixed(1)}" dur=".8s" begin="${(i*.05).toFixed(2)}s" fill="freeze"/></rect>`+T(x+4.5,Y0+12,M[i],'var(--muted)',8,700,'middle'); });
      g+=`<path d="M${X0-4},${Y0-45*k} L${X0+12*B},${Y0-45*k}" stroke="#c8503a" stroke-width="1.5" stroke-dasharray="4 3"/>`+T(X0+12*B,Y0-45*k-4,'45°','#c8503a',9,800,'end');
      g+=T(786,Y0+26,'Gelb: Bildung möglich','var(--muted)',8.5,600,'end')+T(786,Y0+38,'(Mitte April – Anfang Sept.)','var(--muted)',8.5,600,'end');
      g+=T(96,288,'Sommer: Gesicht, Hände, Arme 2–3× pro Woche ca. 12–25 min (BfR) – ohne Sonnenbrand','var(--ink)',9.5,700);
      return {vb:'0 0 790 320',breit:true,leg:[],svg:g}; },

    mn_netz(){ seed=3202; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='start')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      const N={fe:[380,150,'Eisen','#c8503a'],ca:[200,210,'Calcium','#9aa8b8'],zn:[560,90,'Zink','#6a7a9a'],cu:[690,150,'Kupfer','#c88a4a'],vc:[250,92,'Vitamin C','#e0484a'],vd:[70,150,'Vitamin D','#e8b830'],mg:[70,260,'Magnesium','#3a8a6a'],vk:[330,280,'Vitamin K','#3a7a3a'],ph:[540,240,'Phytat','#b8a07a'],ox:[420,260,'Oxalat','#a8b87a'],te:[560,170,'Kaffee, Tee','#7a5a3a'],fe2:[700,300,'Fett','#e8c840'],adek:[700,236,'Vit. A, D, E, K','#d8a040'],b12:[60,30,'Vitamin B12','#b85a8a'],fo:[200,26,'Folat','#5aa85a']};
      const K=[['vc','fe','+','fördert Aufnahme'],['ca','fe','−',''],['te','fe','−',''],['ph','fe','−',''],['ph','zn','−',''],['ph','ca','−',''],['ox','ca','−',''],['ox','fe','−',''],['zn','cu','−','hohe Dosen'],['fe','zn','−',''],['vd','ca','+','Aufnahme'],['mg','vd','+','Aktivierung'],['vk','ca','+','in den Knochen'],['fe2','adek','+','Aufnahme'],['fo','b12','~','verdeckt Mangel']];
      K.forEach(([a,b,s,t],i)=>{ const A=N[a], Bn=N[b], c=s==='+'?'#3a8a4a':s==='−'?'#c8503a':'#8a7a9a';
        const mx=(A[0]+Bn[0])/2+((i%2)?14:-14), my=(A[1]+Bn[1])/2+((i%3)-1)*10;
        g+=`<path d="M${A[0]},${A[1]} Q${mx},${my} ${Bn[0]},${Bn[1]}" stroke="${c}" stroke-width="2.2" fill="none" ${s==='−'?'stroke-dasharray="6 4"':''} opacity=".85"/>`;
        g+=`<circle cx="${(A[0]+2*mx+Bn[0])/4}" cy="${(A[1]+2*my+Bn[1])/4}" r="8" fill="${c}"/>`+T((A[0]+2*mx+Bn[0])/4,(A[1]+2*my+Bn[1])/4+4,s,'#fff',11,800,'middle').replace('stroke:var(--surface);stroke-width:3','stroke:none');
        if(t) g+=T((A[0]+2*mx+Bn[0])/4,(A[1]+2*my+Bn[1])/4+19,t,c,8.5,700,'middle'); });
      Object.values(N).forEach(([x,y,t,f])=>{ const w=t.length*6.4+18; g+=`<rect x="${(x-w/2).toFixed(1)}" y="${y-13}" width="${w.toFixed(1)}" height="26" rx="13" fill="${f}" stroke="${shade(f,-.4)}" stroke-width="1.2"/>`+T(x,y+4,t,'#1a1410',10,800,'middle').replace('stroke:var(--surface)','stroke:'+f); });
      g+=`<circle cx="20" cy="312" r="7" fill="#3a8a4a"/>`+T(32,316,'fördert','var(--ink)',9.5,700)+`<circle cx="100" cy="312" r="7" fill="#c8503a"/>`+T(112,316,'hemmt / konkurriert (gestrichelt)','var(--ink)',9.5,700)+`<circle cx="300" cy="312" r="7" fill="#8a7a9a"/>`+T(312,316,'beeinflusst','var(--ink)',9.5,700);
      return {vb:'0 0 760 326',breit:true,leg:[],svg:g}; },

    mn_darm(){ seed=3203; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='start')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      // Magen
      g+=`<path d="M150,40 C110,40 90,80 100,120 C110,170 170,190 220,170 C250,158 252,130 236,118 C222,108 206,124 190,120 C170,115 175,70 190,55 Z" fill="#f2b8a8" stroke="#9a5a4a" stroke-width="1.6"/>`;
      g+=`<path d="M150,40 L150,14" stroke="#c88a7a" stroke-width="10" stroke-linecap="round"/>`;
      // Dünndarm Schlingen
      let d='M236,150 C280,150 300,120 330,130'; for(let i=0;i<5;i++){ const y=120+i*30; d+=` C${560},${y} ${560},${y+30} 330,${y+30}`; }
      g+=`<path d="${d}" stroke="#e8a890" stroke-width="18" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="${d}" stroke="#c8786a" stroke-width="1.4" fill="none"/>`;
      // Dickdarm Rahmen
      g+=`<path d="M330,280 C300,286 290,300 300,304 L620,304 C650,304 660,290 660,260 L660,110 C660,96 650,90 640,90 L560,90" stroke="#c8a07a" stroke-width="22" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`;
      const L=(x,y,t1,t2,c)=>T(x,y,t1,c,10.5,800)+T(x,y+14,t2,'var(--muted)',9,600);
      g+=L(14,170,'Magen','Säure löst Eisen, Calcium,','#9a3a2a')+T(14,198,'B12 aus Eiweiß; Intrinsic Factor','var(--muted)',9,600);
      g+=L(250,30,'Zwölffingerdarm (Duodenum)','Eisen, Calcium, Zink, Kupfer, Folat','#a85a3a');
      g+=L(250,62,'Leerdarm (Jejunum)','die meisten Vitamine, Magnesium, Jod, Fett + A/D/E/K','#a85a3a');
      g+=`<path d="M300,48 L300,120 M300,80 L330,128" stroke="#a85a3a" stroke-width="1" stroke-dasharray="2 3"/>`;
      g+=L(578,188,'Krummdarm (Ileum)','B12 mit Intrinsic Factor,','#a85a3a')+T(578,216,'Gallensäuren','var(--muted)',9,600);
      g+=L(680,60,'Dickdarm','Natrium, Kalium, Wasser;','#8a6a3a')+T(680,88,'Bakterien bilden','var(--muted)',9,600)+T(680,102,'Vitamin K2, Biotin,','var(--muted)',9,600)+T(680,116,'kurzkettige Fettsäuren','var(--muted)',9,600);
      g+=`<rect x="14" y="236" width="246" height="66" rx="9" fill="#eef2f6" stroke="#7a8a9a"/>`+T(24,254,'Säureblocker, Magen-OP, Ältere:','#2f5a7a',9.5,800)+T(24,270,'weniger B12, Eisen, Calcium, Magnesium','var(--ink)',9,600)+T(24,286,'Morbus Crohn (Ileum): B12, Gallensäuren','var(--ink)',9,600);
      return {vb:'0 0 790 320',breit:true,leg:[],svg:g}; },
