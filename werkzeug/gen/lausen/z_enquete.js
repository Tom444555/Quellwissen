    enquete_denkraum(){ seed=8200; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3px">${t}</text>`;
      const F=(i,inner)=>`<g opacity="0">${inner}<animate attributeName="opacity" from="0" to="1" dur=".45s" begin="${(0.15+i*0.3).toFixed(2)}s" fill="freeze"/></g>`;
      g+=T(380,20,'Vom digitalen Käfig zum Denkraum – Darstellung laut Lausen (schematisch, keine Messwerte)',undefined,12.5,800);
      // linkes Feld: Käfig
      g+=`<rect x="20" y="36" width="250" height="250" rx="12" fill="${lg('#efe6d6','#e2d3bb',90)}" stroke="var(--line)"/>`;
      g+=T(145,56,'Der „Käfig“, den er kommen sieht',shade('#7a5a3a',-0.3),11,800);
      const cx=145, cy=160;
      let k='';
      k+=`<circle cx="${cx}" cy="${cy}" r="46" fill="${lg('#6f9fb8','#3f6f88',120)}" stroke="${shade('#3f6f88',-0.3)}" stroke-width="1.4"/>`;
      k+=`<path d="M${cx-30},${cy-18} q14,-10 26,-2 q10,8 22,0 q8,10 -4,22 q-14,6 -22,-6 q-12,4 -22,-14z" fill="#8fae6a" opacity=".85"/>`;
      [[78,20,-20],[70,26,25],[84,16,70]].forEach(([rx,ry,rot],i)=>{
        k+=`<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" transform="rotate(${rot} ${cx} ${cy})" fill="none" stroke="#8a6a4a" stroke-width="1.1" stroke-dasharray="3 3"/>`;
        for(let j=0;j<5;j++){ const a=j*1.25+i; const x=cx+rx*Math.cos(a), y=cy+ry*Math.sin(a);
          const p=rot*Math.PI/180, X=cx+(x-cx)*Math.cos(p)-(y-cy)*Math.sin(p), Y=cy+(x-cx)*Math.sin(p)+(y-cy)*Math.cos(p);
          k+=`<rect x="${R(X-3)}" y="${R(Y-2)}" width="6" height="4" fill="#5a5a5a"/>`; } });
      g+=F(0,k);
      const LL=[['Satelliten-Netz [0:45]',236],['QR-Code, Grenzkabine [0:42]',252],['Digitales Geld (CBDC) [0:42]',268]];
      g+=F(1,LL.map(([t,y])=>T(145,y,t,'var(--ink)',9.5,650)).join(''));
      // Mitte: Pfeil KI
      let m='';
      m+=`<path d="M282,160 C330,128 400,128 448,160" stroke="#4a7a5a" stroke-width="3" fill="none"/><path d="M450,161 l-12,-2 l6,-9 z" fill="#4a7a5a"/>`;
      m+=T(365,118,'KI als Denkfabrik',shade('#4a7a5a',-0.35),11.5,800);
      m+=T(365,134,'ohne Groll, ohne Tabus [0:59]','var(--muted)',9,650);
      const st=['Dokumente hochladen','genau nachfragen','eigene Entwürfe [1:12]'];
      st.forEach((s,i)=>{ m+=`<rect x="300" y="${178+i*30}" width="130" height="22" rx="11" fill="${shade('#cfe0c4',i*-0.06)}" stroke="#7a9a6a"/>`+T(365,193+i*30,s,'var(--ink)',9.2,700); });
      m+=`<path d="M365,200 v8 M365,230 v8" stroke="#7a9a6a" stroke-width="1.5"/>`;
      g+=F(2,m);
      // rechtes Feld: Denkraum
      let r='';
      r+=`<rect x="460" y="36" width="280" height="250" rx="12" fill="${lg('#eef3e4','#dde8cf',90)}" stroke="var(--line)"/>`;
      r+=T(600,56,'Sein Gegenentwurf',shade('#4a7a5a',-0.35),11,800);
      // Tür
      r+=`<rect x="510" y="80" width="60" height="96" rx="4" fill="#c9a77a" stroke="#7a5a3a"/><rect x="516" y="86" width="48" height="84" fill="#f5eedd"/><path d="M516,86 L548,96 L548,180 L516,170 z" fill="#b08858" stroke="#7a5a3a"/><circle cx="543" cy="134" r="2.4" fill="#5a4a2a"/>`;
      r+=T(540,192,'Recht auf Ausstieg','var(--ink)',9.5,800);
      r+=T(540,205,'ohne Nachteile [1:04]','var(--muted)',8.8,650);
      // Tisch analoge Treffen
      r+=`<ellipse cx="665" cy="140" rx="42" ry="14" fill="#a8835a" stroke="#6a4a2a"/>`;
      [[628,118],[702,118],[640,166],[690,166]].forEach(([x,y])=>{ r+=`<circle cx="${x}" cy="${y}" r="8" fill="#e0b48a" stroke="#8a5a3a"/>`; });
      r+=`<g transform="translate(700,92)"><rect x="-7" y="-11" width="14" height="22" rx="3" fill="#ddd" stroke="#555"/><path d="M-11,-13 L11,13" stroke="#b0402a" stroke-width="2.4"/></g>`;
      r+=T(665,192,'Analoge Treffen','var(--ink)',9.5,800);
      r+=T(665,205,'ohne Handy [1:04]','var(--muted)',8.8,650);
      r+=T(600,236,'analogfreedom.eu: „analoges','var(--ink)',9.2,700);
      r+=T(600,250,'Zugangsgrundrecht“ [1:01]','var(--ink)',9.2,700);
      r+=T(600,270,'Jeder prüft Drucksachen selbst [1:55]','var(--muted)',8.8,650);
      g+=F(3,r);
      g+=T(380,306,'Gefahr laut Lausen: weniger Zwang als freiwillige Zustimmung [1:35]','var(--muted)',9.5,700);
      return {vb:'0 0 760 316', breit:true, leg:[], svg:g}; },
    enquete_vorgaenge(){ seed=8201; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3px">${t}</text>`;
      g+=T(380,20,'Belegte Vorgänge rund um das Gespräch (2024–2026) und Geburten in Deutschland',undefined,12.5,800);
      // Zeitstrahl: Monate ab Juli 2024 (0) bis April 2026 (21)
      const x0=50,x1=720,y=150, M=21, X=m=>R(x0+(x1-x0)*m/M);
      g+=`<path d="M${x0},${y} L${x1+10},${y}" stroke="var(--muted)" stroke-width="2"/><path d="M${x1+10},${y} l-8,-4 l0,8 z" fill="var(--muted)"/>`;
      [[0,'Juli 2024'],[6,'Jan. 2025'],[12,'Juli 2025'],[18,'Jan. 2026']].forEach(([m,t])=>{ g+=`<path d="M${X(m)},${y-5} v10" stroke="var(--muted)"/>`+T(X(m),y+26,t,'var(--muted)',9,700); });
      // [Monat, Ebene(oben + / unten -), Farbe, Zeile1, Zeile2]
      const E=[
        [0.03,1,'#5a7aa0','01.08.2024: EU-KI-Verordnung','in Kraft'],
        [4.6,2,'#a0603a','20.11.2024: BGH bestätigt','Urteil gegen Dettmar'],
        [11.1,1,'#a0603a','05.06.2025: BVerfG nimmt','Beschwerde nicht an'],
        [14.3,2,'#6a8a4a','Sept. 2025: Enquete-','Kommission konstituiert'],
        [20.2,1,'#5a7aa0','März 2026: 10.000','Starlink-Satelliten'],
      ];
      E.forEach(([m,lv,c,a,b],i)=>{
        const x=X(m), ly=y-18-lv*30;
        const tx=Math.min(Math.max(x,108),670);
        let s=`<path d="M${x},${y} L${x},${ly+6}" stroke="${c}" stroke-width="1.2" stroke-dasharray="2 2"/>`;
        s+=`<circle cx="${x}" cy="${y}" r="5" fill="${shade(c,0.3)}" stroke="${shade(c,-0.3)}" stroke-width="1.4"/>`;
        s+=T(tx,ly-10,a,shade(c,-0.35),9,800)+T(tx,ly+2,b,'var(--ink)',8.6,650);
        g+=`<g opacity="0">${s}<animate attributeName="opacity" from="0" to="1" dur=".35s" begin="${(0.1+i*0.22).toFixed(2)}s" fill="freeze"/></g>`; });
      // Januar 2026: Bündel in einem Kasten unter der Achse
      const jx=X(18.6), bx0=420, bw=300, by0=184;
      const J=[['10./11.01.','Warken antwortet Kennedy','#8a5a8a'],['27.01.','über 6.000 bestätigte Tote im Iran','#b04a3a'],['28.01.','Aufnahme dieses Gesprächs','#555'],['29.01.','Anhörung mit Maaßen, Faeser u. a.','#6a8a4a']];
      let jb=`<circle cx="${jx}" cy="${y}" r="6" fill="#d9c3a0" stroke="#7a5a3a" stroke-width="1.4"/><path d="M${jx},${y+6} L${jx},${by0}" stroke="#7a5a3a" stroke-width="1.2" stroke-dasharray="2 2"/>`;
      jb+=`<rect x="${bx0}" y="${by0}" width="${bw}" height="66" rx="8" fill="${lg('#f6efe2','#ece0c8',90)}" stroke="var(--line)"/>`;
      J.forEach(([d,t,c],k)=>{ jb+=T(bx0+12,by0+16+k*14,d,shade(c,-0.3),9,800,'start')+T(bx0+78,by0+16+k*14,t,'var(--ink)',8.8,650,'start'); });
      jb+=T(bx0-8,by0+16,'Januar 2026','var(--muted)',9,800,'end');
      g+=`<g opacity="0">${jb}<animate attributeName="opacity" from="0" to="1" dur=".4s" begin="1.3s" fill="freeze"/></g>`;
      // Geburten-Leiste
      const by=272, B=[['1964',1357],['1975',782],['2019',778]];
      g+=T(60,by-6,'Lebendgeborene (Tsd.) – Pillenknick [1:28]:','var(--muted)',9.5,700,'start');
      B.forEach(([j,v],i)=>{ const w=R(v/1357*120), bx=60+i*230;
        g+=`<rect x="${bx}" y="${by}" width="${w}" height="16" rx="3" fill="${shade('#c08a4a',i*0.18)}" stroke="#7a5a2a"><animate attributeName="width" from="0" to="${w}" dur=".6s" begin="${(0.4+i*0.2).toFixed(2)}s" fill="freeze"/></rect>`;
        g+=T(bx+w+6,by+12,`${j}: ${v.toLocaleString('de-DE')}`,'var(--ink)',9.5,800,'start'); });
      g+=T(380,306,'Quellen: hib 78/2026, LTO, BMG, Al-Monitor, Scientific American, EUR-Lex, bpb nach Destatis – siehe Abgleich','var(--muted)',8.6,600);
      return {vb:'0 0 760 316', breit:true, leg:[], svg:g}; },
