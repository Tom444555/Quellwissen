    erdform_zeitstrahl(){ seed=1021; let g=''; const y=150;
      const T=(x,yy,t,c='var(--ink)',s=9,w=700)=>`<text x="${x}" y="${yy}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:middle;paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      const X=j=>j<-1000?70+(j+3000)/2000*50:j<0?120+(j+1000)/1000*200:j<1500?320+j/1500*140:j<1900?460+(j-1500)/400*140:600+(j-1900)/126*140;
      const F=[[-3000,'Mesopotamien'],[-750,'Homer: Okeanos'],[-600,'Thales: Scheibe auf Wasser'],[550,'Kosmas: Zeltmodell'],[1849,'Rowbotham'],[1892,'Gleason-Karte'],[1956,'Flat Earth Society'],[2015,'Internet-Welle']];
      const K=[[-500,'Pythagoreer: Kugel'],[-350,'Aristoteles: Belege'],[-240,'Eratosthenes misst'],[150,'Ptolemäus'],[1230,'Sacrobosco'],[1522,'Weltumsegelung'],[1687,'Newton: Abplattung'],[1851,'Foucault-Pendel'],[1946,'erstes Foto aus dem All'],[1972,'Blue Marble']];
      g+=T(380,16,'Vorstellungen von der Erdform im Lauf der Zeit',undefined,12.5,800);
      g+=`<path d="M14,${y} H746" stroke="var(--muted)" stroke-width="2"/>`;
      [[-1000,'1000 v. Chr.'],[-500,'500 v. Chr.'],[0,'0'],[1000,'1000'],[1500,'1500'],[1800,'1800'],[1900,'1900'],[2000,'2000']].forEach(([j,t])=>g+=`<path d="M${X(j)},${y-4} v8" stroke="var(--muted)"/>`+T(X(j),y+16,t,'var(--muted)',8.5,600));
      g+=T(40,40,'▲ Scheibe','#c86a20',10.5,800).replace('middle','start')+T(40,296,'▼ Kugel','#2a6aa8',10.5,800).replace('middle','start');
      F.forEach(([j,t],i)=>{ const x=X(j), yy=y-34-(i%3)*26; g+=`<path d="M${x},${y-6} V${yy+4}" stroke="#c86a20" stroke-width="1"/><g opacity="0"><ellipse cx="${x}" cy="${y-6}" rx="7" ry="3" fill="${lg('#f0b070','#c86a20',90)}" stroke="#7a3a10"/><animate attributeName="opacity" from="0" to="1" dur=".3s" begin="${(i*0.2).toFixed(1)}s" fill="freeze"/></g>`+T(x,yy-7,j<0?-j+' v. Chr.':j,'#c86a20',8.5,800)+T(x,yy+2,t,'var(--ink)',8.5,600); });
      K.forEach(([j,t],i)=>{ const x=X(j), yy=y+40+(i%4)*22; g+=`<path d="M${x},${y+6} V${yy-12}" stroke="#2a6aa8" stroke-width="1"/><g opacity="0"><circle cx="${x}" cy="${y+6}" r="5" fill="${lg('#8ac8ff','#2a6aa8',45)}" stroke="#1a3a6a"/><animate attributeName="opacity" from="0" to="1" dur=".3s" begin="${(i*0.2+0.1).toFixed(1)}s" fill="freeze"/></g>`+T(x,yy-2,j<0?-j+' v. Chr.':j,'#2a6aa8',8.5,800)+T(x,yy+8,t,'var(--ink)',8.5,600); });
      return {vb:'0 0 760 304',breit:true,leg:[],svg:g}; },

    erdform_modelle(){ seed=1022; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      g+=T(190,18,'Kugelmodell (gängige Darstellung)','#2a6aa8',12,800)+T(570,18,'Flache-Erde-Modell (Sicht der Vertreter)','#c86a20',12,800);
      // Kugel
      g+=`<circle cx="70" cy="150" r="26" fill="${lg('#fff6b0','#f0a020',45)}"/>`+T(70,196,'Sonne (sehr weit,','var(--muted)',9,600)+T(70,207,'109 × Erddurchmesser)','var(--muted)',9,600);
      for(let k=0;k<5;k++) g+=`<path d="M100,${130+k*10} L225,${130+k*10}" stroke="#f0c040" stroke-width="1" stroke-dasharray="4 4" opacity=".7"/>`;
      g+=`<g><circle cx="270" cy="150" r="50" fill="${lg('#5aa0e0','#1a4a8a',45)}" stroke="#0a2a5a"/><path d="M250,115 q20,10 10,30 q-15,10 5,25 q15,5 10,20" fill="#6aa050" opacity=".9"/><path d="M220,150 A50,50 0 0 0 320,150" fill="none"/><animateTransform attributeName="transform" type="rotate" from="0 270 150" to="360 270 150" dur="24s" repeatCount="indefinite"/></g>`;
      g+=`<path d="M270,150 m0,-50 a50,50 0 0 1 0,100" fill="rgba(0,0,20,.45)"/>`;
      g+=`<circle cx="345" cy="110" r="9" fill="#d8dce4" stroke="#8a8e98"/>`+T(345,95,'Mond','var(--muted)',9,600);
      g+=T(270,222,'Kugel, dreht sich in 24 Std.','var(--ink)',9.5,700)+T(270,234,'Schwerkraft zieht zum Mittelpunkt','var(--muted)',9,600)+T(270,246,'Tag/Nacht: halbe Kugel beleuchtet','var(--muted)',9,600);
      g+=`<path d="M380,30 V280" stroke="var(--muted)" stroke-dasharray="4 4"/>`;
      // Scheibe mit Kuppel
      g+=`<path d="M430,200 A140,120 0 0 1 710,200" fill="rgba(120,170,255,.12)" stroke="#8ab0e8" stroke-width="1.4" stroke-dasharray="6 4"/>`+T(570,70,'Kuppel / Firmament','#5a80c0',9.5,700);
      g+=`<path d="M440,200 L700,200 L692,212 L448,212 Z" fill="${lg('#6aa050','#3a6a30',90)}" stroke="#2a4a20"/><rect x="430" y="192" width="14" height="22" rx="3" fill="#e8f0fa" stroke="#8aa0bc"/><rect x="696" y="192" width="14" height="22" rx="3" fill="#e8f0fa" stroke="#8aa0bc"/>`;
      g+=T(437,230,'Eiswall','#6a80a0',9,700)+T(703,230,'Eiswall','#6a80a0',9,700)+T(570,226,'Nordpol in der Mitte','var(--muted)',9,600);
      g+=`<g><circle cx="520" cy="120" r="10" fill="${lg('#fff6b0','#f0a020',45)}"/><path d="M520,130 L480,200 L560,200 Z" fill="rgba(255,220,120,.25)"/><animateTransform attributeName="transform" type="translate" values="0,0;100,0;0,0" dur="10s" repeatCount="indefinite"/></g>`;
      g+=`<g><circle cx="640" cy="125" r="7" fill="#d8dce4" stroke="#8a8e98"/><animateTransform attributeName="transform" type="translate" values="0,0;-100,0;0,0" dur="10s" repeatCount="indefinite"/></g>`;
      g+=T(570,250,'Sonne und Mond klein und nah (oft ca. 5.000 km angegeben),','var(--ink)',9.5,700)+T(570,262,'kreisen über der Scheibe wie Scheinwerfer','var(--muted)',9,600)+T(570,274,'Schwerkraft: Dichte und Auftrieb bzw. Beschleunigung nach oben','var(--muted)',9,600);
      return {vb:'0 0 760 286',breit:true,leg:[],svg:g}; },
