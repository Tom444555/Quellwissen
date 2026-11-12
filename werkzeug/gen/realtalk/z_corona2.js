    corona2_mikrobiom(){ seed=8400; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3px">${t}</text>`;
      g+=T(380,20,'Wo Mikroben im Körper leben und was sie beeinflusst (schematisch)',undefined,12.5,800);
      // Körperumriss
      const bx=230, skin='#c9a27e';
      g+=`<g opacity="0"><circle cx="${bx}" cy="70" r="26" fill="${lg(shade(skin,0.75),shade(skin,0.55),90)}" stroke="${skin}" stroke-width="1.6"/>`;
      g+=`<path d="M${bx-40},104 Q${bx},94 ${bx+40},104 L${bx+52},200 L${bx+30},204 L${bx+26},270 L${bx+6},270 L${bx},214 L${bx-6},270 L${bx-26},270 L${bx-30},204 L${bx-52},200 Z" fill="${lg(shade(skin,0.78),shade(skin,0.6),90)}" stroke="${skin}" stroke-width="1.6"/>`;
      g+=`<animate attributeName="opacity" from="0" to="1" dur=".4s" begin="0s" fill="freeze"/></g>`;
      // Darm
      g+=`<g opacity="0"><path d="M${bx-22},150 q10,-12 22,0 t22,0 q6,14 -10,16 t-24,2 q-12,10 0,18 t26,0" fill="none" stroke="#9a6a4a" stroke-width="5" stroke-linecap="round"/>`;
      g+=`<animate attributeName="opacity" from="0" to="1" dur=".4s" begin=".3s" fill="freeze"/></g>`;
      const O=[[bx,76,'Mund/Nase','#4a7aa8',bx-130,64],[bx,165,'Darm (größter Anteil)','#9a6a4a',bx-150,160],[bx+48,130,'Haut','#b0603e',bx-130,112]];
      O.forEach(([x,y,t,c,lx,ly],i)=>{ g+=`<g opacity="0"><circle cx="${x}" cy="${y}" r="4" fill="${c}"/><path d="M${x-6},${y} L${lx+70},${ly-4}" stroke="${c}" stroke-width="1" stroke-dasharray="3 2"/>`+T(lx+64,ly,t,shade(c,-0.3),9.5,750,'end');
        g+=`<animate attributeName="opacity" from="0" to="1" dur=".35s" begin="${(0.6+i*0.2).toFixed(2)}s" fill="freeze"/></g>`; });
      // Einflüsse
      const E=[['👶 Geburt','Kaiserschnitt oder vaginal','#7a6a9a'],['🍼 Stillen','Muttermilch','#5a8a6a'],['🥬 Ernährung','Ballaststoffe, Fermentiertes','#4a8a4a'],['💊 Antibiotika','Spuren noch nach Jahren','#b0603e'],['🌳 Umgebung','Bauernhof, Tiere, Erde','#9a7a3a']];
      const x0=440,w=270,h=34,gap=10,y0=48;
      E.forEach(([t,s,c],i)=>{ const y=y0+i*(h+gap);
        g+=`<g opacity="0"><rect x="${x0}" y="${y}" width="${w}" height="${h}" rx="9" fill="${shade(c,0.85)}" stroke="${c}" stroke-width="1.3"/>`;
        g+=T(x0+12,y+14,t,shade(c,-0.45),10.5,800,'start')+T(x0+12,y+27,s,'var(--ink)',8.8,600,'start');
        g+=`<path d="M${x0-4},${y+h/2} L${bx+70},${150+(i-2)*14}" stroke="${shade(c,-0.1)}" stroke-width="1.4"/><circle cx="${bx+70}" cy="${150+(i-2)*14}" r="2.5" fill="${c}"/>`;
        g+=`<animate attributeName="opacity" from="0" to="1" dur=".35s" begin="${(1.3+i*0.22).toFixed(2)}s" fill="freeze"/></g>`; });
      g+=T(380,286,'Bakterien und Körperzellen etwa gleich viele (je rund 3–4·10¹³), Bakterienmasse etwa 0,2 kg (Sender u. a. 2016)','var(--muted)',8.5,600);
      return {vb:'0 0 760 300', breit:true, leg:[], svg:g}; },
    corona2_meningokokken(){ seed=8401; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3px">${t}</text>`;
      g+=T(380,20,'Meningokokken in Zahlen (belegte Daten)',undefined,12.5,800);
      // links: Fälle je Jahr
      const D=[[2019,257],[2020,138],[2021,71],[2022,141],[2023,253],[2024,342],[2025,318]];
      const bx0=50, by=230, bw=34, bg=12, sc=0.42;
      g+=T(bx0+140,46,'Gemeldete Erkrankungen in Deutschland je Jahr','#7a3a3a',10,800);
      g+=`<path d="M${bx0-6},${by} L${bx0+D.length*(bw+bg)},${by}" stroke="var(--line)" stroke-width="1.5"/>`;
      D.forEach(([j,v],i)=>{ const x=bx0+i*(bw+bg), h=R(v*sc);
        g+=`<g opacity="0"><rect x="${x}" y="${by-h}" width="${bw}" height="${h}" rx="4" fill="${lg(shade('#b0603e',0.35),shade('#b0603e',0.05),90)}" stroke="#8a4a2e" stroke-width="1"/>`;
        g+=T(x+bw/2,by-h-5,String(v),'var(--ink)',9,750)+T(x+bw/2,by+14,String(j),'var(--muted)',8.5,600);
        g+=`<animate attributeName="opacity" from="0" to="1" dur=".3s" begin="${(i*0.15).toFixed(2)}s" fill="freeze"/></g>`; });
      g+=T(bx0+155,by+32,'2025: 0,38 je 100.000 Einwohner (NRZ/SurvStat@RKI)','var(--muted)',8.5,600);
      // rechts: Träger und Serogruppen
      const rx=430;
      g+=`<g opacity="0">`+T(rx+150,46,'Träger ohne Erkrankung','#4a6a8a',10,800);
      for(let k=0;k<10;k++){ const cx=rx+30+k*28, c=k==0?'#4a7aa8':'#d8d0c4'; g+=`<circle cx="${cx}" cy="70" r="10" fill="${c}" stroke="${shade(c,-0.25)}" stroke-width="1"/>`; }
      g+=T(rx+150,98,'etwa 1 von 10 Menschen trägt sie im Rachen (CDC)','var(--ink)',9,650);
      g+=T(rx+150,112,'Metaanalyse Europa: 4,5 % Säuglinge · 23,7 % mit 19 J. · 7,8 % mit 50 J.','var(--muted)',8.2,600);
      g+=`<animate attributeName="opacity" from="0" to="1" dur=".4s" begin="1.2s" fill="freeze"/></g>`;
      const SG=[['B',56,'#7a6a9a'],['Y',21,'#4a8a6a'],['W',15,'#9a7a3a'],['C',4,'#4a7aa8']];
      g+=`<g opacity="0">`+T(rx+150,140,'Serogruppen EU/EWR 2024 (ECDC)','#4a6a8a',10,800);
      let xx=rx+10; const sw=280;
      SG.forEach(([n,p,c])=>{ const w=R(sw*p/96); g+=`<rect x="${xx}" y="150" width="${w}" height="26" fill="${shade(c,0.3)}" stroke="${shade(c,-0.2)}" stroke-width="1"/>`;
        if(w>=26) g+=T(xx+w/2,167,n+' '+p+' %','var(--ink)',8.8,750); xx+=w; });
      g+=T(rx+150,194,'C: 4 % · Rest ohne Angabe/andere','var(--muted)',8.2,600);
      g+=T(rx+150,214,'Sterblichkeit EU/EWR 2024: 10 % (202 Tote)','var(--ink)',9,700);
      g+=`<animate attributeName="opacity" from="0" to="1" dur=".4s" begin="1.6s" fill="freeze"/></g>`;
      g+=T(380,286,'Quellen: NRZ Meningokokken (SurvStat@RKI), CDC, Christensen u. a. 2010, ECDC Jahresbericht 2024','var(--muted)',8.2,600);
      return {vb:'0 0 760 300', breit:true, leg:[], svg:g}; },
