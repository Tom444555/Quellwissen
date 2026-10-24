    hefe_zelle(){ seed=921; let g='';
      const T=(x,y,t,c='var(--ink)',s=10.5,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      const cx=240, cy=128;
      g+=`<ellipse cx="${cx}" cy="${cy}" rx="92" ry="78" fill="${lg('#f4ead0','#d8c49a',45)}" stroke="#8a7448" stroke-width="5"/>`;
      g+=`<ellipse cx="${cx}" cy="${cy}" rx="86" ry="72" fill="none" stroke="#b8a070" stroke-width="1.2" stroke-dasharray="3 3"/>`;
      g+=`<ellipse cx="${cx+22}" cy="${cy+10}" rx="34" ry="30" fill="${lg('#d8e6f0','#a8c0d4',45)}" stroke="#6a88a0" stroke-width="1.2"/>`;
      g+=`<circle cx="${cx-34}" cy="${cy-18}" r="18" fill="${lg('#c89ac0','#8a5a88',45)}" stroke="#6a3a68"/><circle cx="${cx-30}" cy="${cy-20}" r="5" fill="#5a2a58"/>`;
      [[cx-50,cy+30,0],[cx+40,cy-40,40],[cx-10,cy+50,-30],[cx+66,cy+30,70]].forEach(([x,y,a])=>g+=`<ellipse cx="${x}" cy="${y}" rx="12" ry="6" fill="${lg('#f0a070','#c06a3a',0)}" stroke="#8a4a2a" transform="rotate(${a} ${x} ${y})"/><path d="M${x-8},${y} q4,-4 8,0 q4,4 8,0" stroke="#8a4a2a" fill="none" transform="rotate(${a} ${x} ${y})"/>`);
      for(let i=0;i<14;i++) g+=`<circle cx="${R(cx-60+rnd()*120)}" cy="${R(cy-50+rnd()*100)}" r="${R(2+rnd()*2.5)}" fill="#e8c860" opacity=".8"/>`;
      // Knospe
      g+=`<g transform-origin="${cx+86} ${cy-46}"><ellipse cx="${cx+104}" cy="${cy-62}" rx="30" ry="26" fill="${lg('#f4ead0','#d8c49a',45)}" stroke="#8a7448" stroke-width="4"/><circle cx="${cx+104}" cy="${cy-62}" r="8" fill="#a87aa6"/><animateTransform attributeName="transform" type="scale" values=".2;1;1;.2" keyTimes="0;.6;.9;1" dur="6s" repeatCount="indefinite"/></g>`;
      [['Zellwand',cx-130,cy-62,cx-86,cy-40],['Zellkern (Erbgut)',cx-128,cy-6,cx-52,cy-18],['Mitochondrien (Atmung)',cx-128,cy+60,cx-60,cy+32],['Vakuole',cx+150,cy+52,cx+50,cy+20],['Tochterzelle (Knospe)',cx+146,cy-104,cx+118,cy-80],['Reservestoffe',cx-128,cy+92,cx-20,cy+40]].forEach(([t,x,y,x2,y2])=>{ g+=`<path d="M${x2},${y2} L${x+(x<cx?36:-36)},${y-4}" stroke="var(--muted)" stroke-width=".8"/>`+T(x,y,t,'var(--ink)',10,700); });
      g+=T(cx,232,'S. cerevisiae · 5–10 µm · 1 Würfel ≈ 400 Mrd. Zellen','var(--muted)',10,600);
      // Sprossung
      const sx=500; g+=T(sx+95,22,'Vermehrung durch Sprossung','var(--ink)',12.5,800);
      [[0,0],[1,10],[2,20],[3,28]].forEach(([i,r])=>{ const x=sx+i*62, y=110;
        g+=`<ellipse cx="${x}" cy="${y}" rx="26" ry="22" fill="${lg('#f4ead0','#d8c49a',45)}" stroke="#8a7448" stroke-width="2.5"/><circle cx="${x-4}" cy="${y}" r="6" fill="#a87aa6"/>`;
        if(r) g+=`<ellipse cx="${x+18+r*.4}" cy="${y-18-r*.3}" rx="${R(r*.75)}" ry="${R(r*.65)}" fill="${lg('#f4ead0','#d8c49a',45)}" stroke="#8a7448" stroke-width="2"/>`;
        g+=T(x,y+46,['Mutterzelle','Knospe','wächst','löst sich'][i],'var(--muted)',9.5,700); });
      g+=T(sx+95,190,'Bei 30 °C und genug Nahrung verdoppelt','var(--ink)',10,700)+T(sx+95,204,'sich Hefe etwa alle 90–120 Minuten','var(--ink)',10,700);
      g+=T(sx+95,220,'Nach ~25 Sprossungen altert die Mutterzelle','var(--muted)',9,600);
      return {vb:'0 0 760 240',breit:true,leg:[],svg:g}; },
    hefe_gaerung(){ seed=922; let g='';
      const T=(x,y,t,c='var(--ink)',s=11,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      const box=(x,y,w,h,c,t)=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="10" fill="${c}" opacity=".14" stroke="${c}"/>`+T(x+w/2,y+18,t,shade(c,-0.4),12,800);
      g+=box(10,14,170,96,'#c89a40','Stärke & Zucker im Mehl');
      g+=T(95,52,'Stärke ─ Amylasen ─▶ Malzzucker','var(--ink)',9.5,700)+T(95,70,'Haushaltszucker ─ Invertase ─▶','var(--ink)',9.5,700)+T(95,84,'Traubenzucker + Fruchtzucker','var(--ink)',9.5,700);
      g+=`<path d="M182,62 h40" stroke="var(--muted)" stroke-width="2" marker-end="url(#pf)"/>`;
      g+=box(230,6,250,52,'#3a8a5a','mit Sauerstoff: Atmung')+T(355,46,'C₆H₁₂O₆ + 6 O₂ → 6 CO₂ + 6 H₂O + viel Energie','var(--ink)',9.5,700);
      g+=box(230,66,250,52,'#c0501a','ohne Sauerstoff: Gärung')+T(355,106,'C₆H₁₂O₆ → 2 C₂H₅OH (Alkohol) + 2 CO₂','var(--ink)',9.5,700);
      g+=T(355,134,'Hefe wächst ⇧','#3a8a5a',10,800,'middle')+T(355,148,'im Teig überwiegt rasch die Gärung','var(--muted)',9.5,600);
      // Teig mit Glutennetz
      const tx=500, ty=12, tw=250, th=200;
      g+=`<rect x="${tx}" y="${ty}" width="${tw}" height="${th}" rx="16" fill="${lg('#f6ead0','#e4cfa0',90)}" stroke="#b89a60"/>`;
      for(let i=0;i<9;i++){ const y=ty+20+i*21; g+=`<path d="M${tx+8},${y} q30,${R(rnd()*16-8)} 60,0 t60,0 t60,0 t60,0" stroke="#c8a868" stroke-width="1.2" fill="none" opacity=".7"/>`; }
      for(let i=0;i<16;i++){ const x=R(tx+20+rnd()*(tw-40)), y=R(ty+30+rnd()*(th-50)), r=R(4+rnd()*9);
        g+=`<circle cx="${x}" cy="${y}" r="${r}" fill="#fffaf0" stroke="#c8a868" stroke-width="1.2"><animate attributeName="r" values="${R(r*.3)};${r};${R(r*.3)}" dur="${R(4+rnd()*3)}s" repeatCount="indefinite"/></circle>`; }
      for(let i=0;i<10;i++) g+=`<ellipse cx="${R(tx+20+rnd()*(tw-40))}" cy="${R(ty+30+rnd()*(th-50))}" rx="2.6" ry="2.1" fill="#8a7448"/>`;
      g+=T(tx+tw/2,ty+th+18,'CO₂ dehnt das Klebergerüst – der Teig geht auf','var(--ink)',10,700);
      g+=T(250,186,'Beim Backen: Bläschen dehnen sich, Alkohol verdampft,','var(--muted)',10,600)+T(250,200,'ab ~55–60 °C stirbt die Hefe, Stärke verkleistert, Krume wird fest','var(--muted)',10,600);
      return {vb:'0 0 760 236',breit:true,leg:[],svg:g}; },
    hefe_temperatur(){ seed=923; let g='';
      const T=(x,y,t,c='var(--ink)',s=10.5,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      const X0=60, X1=720, Y0=170, x=t=>R(X0+(X1-X0)*(t+5)/70);
      const Z=[[-5,4,'#7aa8d8','Ruhe (Kühlschrank)'],[4,20,'#8ac0a0','langsam: viel Aroma'],[20,35,'#e0b040','aktiv: Optimum 26–35 °C'],[35,45,'#e07a2a','gestresst'],[45,65,'#c0301a','stirbt (ab ~55 °C tot)']];
      Z.forEach(([a,b,c,t])=>{ g+=`<rect x="${x(a)}" y="${Y0-120}" width="${x(b)-x(a)}" height="120" fill="${c}" opacity=".16"/>`+T((x(a)+x(b))/2,Y0-104,t,shade(c,-0.4),10,800); });
      let d=''; for(let t=-5;t<=65;t+=1){ const v=t<0?0:t<32?Math.pow(t/32,1.6):t<45?1-(t-32)/26:t<58?0.5*(1-(t-45)/13):0; d+=(d?' L':'M')+x(t)+','+R(Y0-v*96); }
      g+=`<path d="${d}" stroke="#6a3a1a" stroke-width="3" fill="none" stroke-dasharray="2000" stroke-dashoffset="2000"><animate attributeName="stroke-dashoffset" from="2000" to="0" dur="2.5s" fill="freeze"/></path>`;
      g+=`<path d="M${X0},${Y0} H${X1}" stroke="var(--ink)" stroke-width="1.4"/>`;
      [0,10,20,30,40,50,60].forEach(t=>g+=`<path d="M${x(t)},${Y0} v5" stroke="var(--ink)"/>`+T(x(t),Y0+18,t+' °C','var(--muted)',10,700));
      g+=T(x(37),Y0+36,'Handwarm ≈ 37 °C – Milch/Wasser für den Teig nie heißer','#c0501a',10.5,800);
      g+=T(X0-4,Y0-90,'Gär-','var(--muted)',9.5,700,'end')+T(X0-4,Y0-78,'kraft','var(--muted)',9.5,700,'end');
      return {vb:'0 0 760 216',breit:true,leg:[],svg:g}; },
    leiste_hefewasser(){ return Z.rezept_leiste([['schuessel','1 · Glas, Wasser, Datteln oder Bio-Äpfel',{f:'#cfe0ea',zutaten:['#7a4a2a','#7a4a2a','#c8402a']}],['warm','2 · 25–28 °C, 5–7 Tage stehen lassen',{t:'5–7 T.'}],['schuessel','3 · Täglich kurz schütteln, Deckel lüften',{f:'#f0e6c8'}],['kalt','4 · Sprudelt und riecht weinig: kühl lagern',{}],['schuessel','5 · Mit Mehl als Vorteig ansetzen',{f:'#e8d2a0'}]]); },
