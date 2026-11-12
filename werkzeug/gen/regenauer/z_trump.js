    trump_buehne(){ seed=7500; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3px">${t}</text>`;
      g+=T(380,18,'Bühne und Hintergrund – Darstellung laut Regenauer und Gastgeber (schematisch)',undefined,12.5,800);
      // Hintergrund: vier Kästen hinter dem Vorhang
      const H=[['🏦 Banken und Finanzwelt','#b08840','Großbanken, BIZ, Offshore','[0:21–0:27]'],
               ['🕵️ Geheimdienste','#6a7a9a','CIA, Mossad, MI6 (laut Sprechern)','[0:21], [0:38]'],
               ['🎲 Organisierte Kriminalität','#8a5a5a','Mafia-Familien, Prohibition','[0:27–0:31]'],
               ['👔 „Superclass“-Familien','#5a7a5a','wenige, kaum bekannt','[0:18–0:19]']];
      g+=`<g opacity="0"><rect x="20" y="30" width="720" height="104" rx="12" fill="${lg('#efe6d6','#e2d6bf',90)}" stroke="var(--line)" stroke-width="1" stroke-dasharray="5 3"/>`+T(38,46,'Hintergrund (nicht sichtbar)','var(--muted)',9,700,'start');
      H.forEach(([t,c,u,f],i)=>{ const x=36+i*178;
        g+=`<rect x="${x}" y="54" width="160" height="66" rx="10" fill="${lg(shade(c,0.78),shade(c,0.6),90)}" stroke="${c}" stroke-width="1.4"/>`;
        g+=T(x+80,73,t,shade(c,-0.45),10.5,800)+T(x+80,90,u,'var(--ink)',8.6,600)+T(x+80,108,f,'var(--muted)',8.2,600); });
      g+=`<animate attributeName="opacity" from="0" to="1" dur=".5s" begin="0s" fill="freeze"/></g>`;
      // Fäden zur Bühne
      g+=`<g opacity="0">`;
      [116,294,472,650].forEach((x,i)=>{ [ -30, 30 ].forEach(d=>{ const tx=380+d*(i-1.5)*1.6+(i-1.5)*40; g+=`<path d="M${x},120 Q${(x+tx)/2},${150+rnd()*10} ${tx},186" stroke="#9a8a6a" stroke-width="0.9" fill="none" stroke-dasharray="2 2"/>`; }); });
      g+=`<animate attributeName="opacity" from="0" to="1" dur=".5s" begin=".5s" fill="freeze"/></g>`;
      // Vorhang und Bühne
      g+=`<g opacity="0"><rect x="120" y="186" width="520" height="62" rx="8" fill="${lg('#c9a6a0','#b0847c',90)}" stroke="#8a5a52" stroke-width="1.4"/>`;
      g+=T(380,204,'🎭 Bühne: Präsidenten, Parteien, Parlamente, Medien',shade('#8a5a52',-0.5),11,800);
      g+=T(380,220,'„Marionetten im Vordergrund“ (Gastgeber) [0:46] · „Politik ist das, was da in der Glotze kommt“ [1:46]','var(--ink)',8.6,600);
      g+=T(380,236,'Popkultur und Stars als zweite Bühne [0:59], [1:45]','var(--muted)',8.4,600);
      g+=`<animate attributeName="opacity" from="0" to="1" dur=".5s" begin="1s" fill="freeze"/></g>`;
      // Publikum
      g+=`<g opacity="0">`;
      for(let i=0;i<17;i++){ const x=150+i*28+rnd()*6, y=258+rnd()*4; g+=`<circle cx="${R(x)}" cy="${R(y)}" r="6" fill="#c8b89a" stroke="#8a7a5a" stroke-width="0.8"/><path d="M${R(x-8)},${R(y+15)} Q${R(x)},${R(y+4)} ${R(x+8)},${R(y+15)}" fill="#d8ccb0" stroke="#8a7a5a" stroke-width="0.8"/>`; }
      g+=T(380,298,'Publikum: Wähler und Zuschauer – Prüffrage „Wen soll ich hassen?“ [1:47]','var(--ink)',9.2,700);
      g+=`<animate attributeName="opacity" from="0" to="1" dur=".5s" begin="1.4s" fill="freeze"/></g>`;
      return {vb:'0 0 760 310',breit:true,leg:[],svg:g}; },
    trump_akten(){ seed=7501; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3px">${t}</text>`;
      g+=T(380,18,'Der Epstein-Fall in amtlichen Stationen 2008–2025 (belegte Daten)',undefined,12.5,800);
      const X=j=>R(60+(j-2007)*(640/19)), y0=150;
      g+=`<path d="M50,${y0} L712,${y0}" stroke="var(--line)" stroke-width="2"/>`;
      for(let j=2008;j<=2025;j++){ const x=X(j); g+=`<path d="M${x},${y0-4} L${x},${y0+4}" stroke="var(--line)" stroke-width="1"/>`; if(j%2==0||j==2025) g+=T(x,y0+18,j,'var(--muted)',8.5,600); }
      const E=[
        [2008.5,140,'2008 · Florida','Schuldbekenntnis; 13 Monate','mit Freigang','#a87a4a',-1,1],
        [2019.6,420,'10.08.2019','Tod in Haft – amtlich','Suizid (Gerichtsmedizin, FBI)','#7a6a8a',1,1],
        [2020.05,440,'Jan. 2020 · MIT','850.000 US-$ Spenden','2002–2017','#5a7a8a',-1,2],
        [2020.85,520,'Nov. 2020 · OPR','Florida-Vereinbarung:','„poor judgment“','#8a6a4a',1,2],
        [2023.45,590,'Juni 2023','Generalinspekteur: Fehler','der Gefängnisbehörde','#6a8a5a',-1,1],
        [2023.5,640,'Juni 2023','JPMorgan-Vergleich','290 Mio. US-$','#b08840',1,1],
        [2025.5,640,'07.07.2025','DOJ/FBI-Memo: keine','„Klientenliste“, >1.000 Opfer','#8a4a4a',-1,2]];
      E.forEach(([j,bx,t,a,b,c,s,lv],i)=>{ const x=X(j), h=(lv==1?38:84), ty=y0+s*h, ry=(s<0?ty-40:ty-10), ey=(s<0?ry+44:ry);
        g+=`<g opacity="0"><circle cx="${x}" cy="${y0}" r="5.5" fill="${c}" stroke="${shade(c,-0.4)}" stroke-width="1"/>`;
        g+=`<path d="M${x},${y0+s*6} L${bx},${ey}" stroke="${c}" stroke-width="1" fill="none"/>`;
        g+=`<rect x="${bx-74}" y="${ry}" width="148" height="44" rx="8" fill="${shade(c,0.85)}" stroke="${c}" stroke-width="1.1"/>`;
        g+=T(bx,ry+13,t,shade(c,-0.45),9.2,800)+T(bx,ry+26,a,'var(--ink)',8.4,600)+T(bx,ry+38,b,'var(--ink)',8.4,600);
        g+=`<animate attributeName="opacity" from="0" to="1" dur=".4s" begin="${(0.2+i*0.25).toFixed(2)}s" fill="freeze"/></g>`; });
      g+=T(380,292,'Quellen: DOJ-Memo 07.07.2025, Generalinspekteur 06/2023, OPR 11/2020, MIT 01/2020, NPR (siehe Abgleich)','var(--muted)',8.4,600);
      return {vb:'0 0 760 300',breit:true,leg:[],svg:g}; },
