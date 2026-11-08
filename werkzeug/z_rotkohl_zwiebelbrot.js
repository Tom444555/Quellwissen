    rotkohl_bild(){ seed=2001; let g='';
      const T=(x,y,t,c='var(--muted)',s=11,w=700)=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:middle;paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      const streifen=(x,y)=>{ const a=rnd()*180, l=10+rnd()*14, c=rnd()<.5?'#7a2a5e':(rnd()<.5?'#5e1e4a':'#9a3a72'); return `<path d="M${R(x-l/2)},${y} q${R(l/2)},${R(rnd()*8-4)} ${R(l)},0" stroke="${c}" stroke-width="${R(2.6+rnd()*1.6)}" fill="none" stroke-linecap="round" transform="rotate(${R(a)} ${x} ${y})"/>`; };
      const wuerfel=(x,y)=>`<rect x="${x}" y="${y}" width="${R(7+rnd()*3)}" height="${R(6+rnd()*3)}" rx="1.5" fill="${rnd()<.6?'#c88aa0':'#e2b8a8'}" stroke="#8a4a62" stroke-width=".6" transform="rotate(${R(rnd()*60-30)} ${x} ${y})"/>`;
      const nelke=(x,y,r=0)=>`<g transform="rotate(${r} ${x} ${y})"><path d="M${x},${y} v14" stroke="#5a3418" stroke-width="2.6" stroke-linecap="round"/><circle cx="${x}" cy="${y-1}" r="3.6" fill="#6a3e1e" stroke="#3e2210" stroke-width=".7"/></g>`;
      const piment=(x,y)=>`<circle cx="${x}" cy="${y}" r="4.4" fill="${lg('#8a5a34','#4a2c16',90)}" stroke="#3a2210" stroke-width=".7"/>`;
      const lorbeer=(x,y,r)=>`<g transform="rotate(${r} ${x} ${y})"><path d="M${x-26},${y} Q${x},${y-12} ${x+26},${y} Q${x},${y+12} ${x-26},${y} Z" fill="${lg('#7a8a4a','#4e5e2a',90)}" stroke="#3a4620" stroke-width="1"/><path d="M${x-24},${y} H${x+24}" stroke="#a8b878" stroke-width=".9"/></g>`;
      // Holzbrett / Tisch
      g+=`<rect x="20" y="214" width="720" height="30" rx="6" fill="${lg('#c89a64','#9a6a3a',90)}" stroke="#6a4420" stroke-width="1"/>`;
      for(let i=0;i<2;i++) g+=`<path d="M30,${224+i*10} q340,${R(rnd()*6-3)} 700,0" stroke="#8a5a2c" stroke-width=".8" fill="none" opacity=".5"/>`;
      // Schüssel mit Rotkohl
      const sx=250, sy=150;
      g+=`<ellipse cx="${sx}" cy="${sy+80}" rx="150" ry="12" fill="#000" opacity=".16"/>`;
      g+=`<path d="M${sx-158},${sy-12} Q${sx-150},${sy+78} ${sx},${sy+82} Q${sx+150},${sy+78} ${sx+158},${sy-12} Z" fill="${lg('#f4f0e8','#cfc6b4',90)}" stroke="#8a8270" stroke-width="1.4"/>`;
      g+=`<path d="M${sx-120},${sy+30} Q${sx},${sy+56} ${sx+120},${sy+30}" stroke="#4a7aa8" stroke-width="5" fill="none" opacity=".55"/>`;
      g+=`<ellipse cx="${sx}" cy="${sy-12}" rx="158" ry="34" fill="${lg('#e8e2d4','#d0c8b6',90)}" stroke="#8a8270" stroke-width="1.4"/>`;
      g+=`<ellipse cx="${sx}" cy="${sy-14}" rx="146" ry="28" fill="${lg('#6a1e50','#4a1238',90)}"/>`;
      g+=`<path d="M${sx-120},${sy-22} Q${sx},${sy-62} ${sx+120},${sy-22} Q${sx},${sy-6} ${sx-120},${sy-22} Z" fill="${lg('#8a2e68','#5e1a48',90)}"/>`;
      for(let i=0;i<170;i++){ const a=rnd()*6.283, d=Math.sqrt(rnd()); const x=R(sx+Math.cos(a)*d*132), y=R(sy-22+Math.sin(a)*d*24-(1-d)*12); g+=streifen(x,y); }
      for(let i=0;i<18;i++){ const a=rnd()*6.283, d=Math.sqrt(rnd())*0.85; g+=wuerfel(R(sx+Math.cos(a)*d*120),R(sy-26+Math.sin(a)*d*20-(1-d)*8)); }
      g+=lorbeer(sx+40,sy-34,-18)+lorbeer(sx-56,sy-24,14);
      g+=nelke(sx-10,sy-38,20)+nelke(sx+86,sy-22,-30)+piment(sx+14,sy-22)+piment(sx-92,sy-14);
      // Dampf
      for(let i=0;i<3;i++) g+=`<path d="M${sx-40+i*40},${sy-58} q-8,-14 0,-28 q8,-14 0,-28" stroke="#c8d2d8" stroke-width="3" fill="none" stroke-linecap="round" opacity=".55"/>`;
      g+=T(sx,sy+112,'Rotkohl wie von Oma – geschmort mit Apfel, Lorbeer, Nelken, Piment','var(--ink)',13,800);
      // halber Kohlkopf
      const kx=520, ky=150;
      g+=`<ellipse cx="${kx}" cy="${ky+50}" rx="56" ry="8" fill="#000" opacity=".14"/>`;
      g+=`<path d="M${kx-56},${ky+46} Q${kx-62},${ky-46} ${kx},${ky-52} Q${kx+62},${ky-46} ${kx+56},${ky+46} Z" fill="${lg('#8a4a8a','#4e2058',0)}" stroke="#3a1440" stroke-width="1.3"/>`;
      g+=`<ellipse cx="${kx}" cy="${ky+4}" rx="46" ry="44" fill="#f2e8f0" stroke="#5e2a62" stroke-width="1.2"/>`;
      for(let i=0;i<9;i++){ const r=8+i*4.4; g+=`<path d="M${R(kx-r)},${R(ky+6+rnd()*4)} Q${R(kx-r*0.6)},${R(ky-r*0.9)} ${R(kx+rnd()*6-3)},${R(ky-r*0.95)} Q${R(kx+r*0.7)},${R(ky-r*0.8)} ${R(kx+r)},${R(ky+4+rnd()*6)}" stroke="#7a2e78" stroke-width="${R(2.4+rnd()*1.4)}" fill="none" stroke-linecap="round"/>`; }
      g+=`<path d="M${kx-6},${ky+46} L${kx-4},${ky+6} Q${kx},${ky-4} ${kx+4},${ky+6} L${kx+6},${ky+46} Z" fill="#e8f0d8" stroke="#a8b890" stroke-width=".8"/>`;
      g+=T(kx,262,'Rotkohl 1 kg','var(--muted)',10.5,700);
      // Äpfel
      const apfel=(x,y,s,c0,c1)=>`<path d="M${x},${y-s*0.7} Q${x+s*1.05},${y-s*1.05} ${x+s*0.95},${y+s*0.1} Q${x+s*0.8},${y+s*0.95} ${x},${y+s*0.8} Q${x-s*0.8},${y+s*0.95} ${x-s*0.95},${y+s*0.1} Q${x-s*1.05},${y-s*1.05} ${x},${y-s*0.7} Z" fill="${lg(c0,c1,45)}" stroke="${shade(c1,-0.35)}" stroke-width="1.1"/><path d="M${x},${y-s*0.7} q2,-10 6,-14" stroke="#5a3a1a" stroke-width="2.2" fill="none" stroke-linecap="round"/><path d="M${x+5},${y-s*0.9} q12,-8 18,0 q-10,6 -18,0 Z" fill="#6a9a3a"/>`;
      g+=apfel(626,120,26,'#f0c040','#c84a2a')+apfel(684,138,22,'#c8a848','#a8743a');
      g+=T(654,182,'Elstar · Boskop','var(--muted)',10.5,700);
      // Gewürzschälchen
      const gx=650, gy=226;
      g+=`<ellipse cx="${gx}" cy="${gy}" rx="52" ry="12" fill="${lg('#f4f0e8','#cfc6b4',90)}" stroke="#8a8270" stroke-width="1.1"/>`;
      g+=lorbeer(gx-22,gy-4,-8)+nelke(gx+8,gy-10,30)+nelke(gx+20,gy-8,-20)+piment(gx+34,gy-3)+piment(gx+28,gy+3)+piment(gx-2,gy+2);
      g+=T(gx,262,'Lorbeer · Nelken · Piment','var(--muted)',10.5,700);
      return {vb:'0 0 760 280',breit:true,leg:[],svg:g}; },
    rotkohl_leiste(){ return Z.rezept_leiste([['schuessel','1 · Kohl in feine Streifen, Äpfel, Zwiebeln würfeln',{zutaten:['#7a2a5e','#9a3a72','#e2b8a8','#f2ead8']}],['topf','2 · Zwiebeln in Schmalz glasig',{t:'glasig'}],['topf','3 · Kohl + Äpfel mit Zucker karamellisieren',{t:'+ 2 EL Zucker'}],['topf','4 · Rotwein + Apfelessig, Gewürze',{t:'ablöschen'}],['topf','5 · Zugedeckt, niedrige Hitze',{t:'60–90 Min.'}],['kalt','6 · Tipp: 1 Tag durchziehen lassen']]); },
    zwiebelbrot_bild(){ seed=2101; let g='';
      const T=(x,y,t,c='var(--muted)',s=11,w=700)=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:middle;paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      const zw=(x,y)=>`<rect x="${x}" y="${y}" width="${R(5+rnd()*4)}" height="${R(4+rnd()*3)}" rx="1.4" fill="${rnd()<.5?'#e8c070':'#d8a04a'}" stroke="#a8742a" stroke-width=".5" opacity=".9" transform="rotate(${R(rnd()*70-35)} ${x} ${y})"/>`;
      const pore=(x,y)=>`<ellipse cx="${x}" cy="${y}" rx="${R(1.5+rnd()*2.6)}" ry="${R(1+rnd()*1.6)}" fill="#d8c08a" opacity=".8"/>`;
      // Brett
      g+=`<rect x="20" y="214" width="720" height="30" rx="6" fill="${lg('#c89a64','#9a6a3a',90)}" stroke="#6a4420" stroke-width="1"/>`;
      for(let i=0;i<2;i++) g+=`<path d="M30,${224+i*10} q340,${R(rnd()*6-3)} 700,0" stroke="#8a5a2c" stroke-width=".8" fill="none" opacity=".5"/>`;
      // Kastenform mit Brot (Seitenansicht, schräg) – Form
      const fx=46, fy=120, fw=262, fh=88;
      g+=`<ellipse cx="${fx+fw/2+30}" cy="${fy+fh+12}" rx="${fw/2+40}" ry="10" fill="#000" opacity=".16"/>`;
      // Laib oben (Kuppel) ragt aus der Form
      g+=`<path d="M${fx-4},${fy+8} Q${fx+6},${fy-62} ${fx+fw/2},${fy-66} Q${fx+fw-6},${fy-62} ${fx+fw+4},${fy+8} Z" fill="${lg('#e0a050','#a8641e',90)}" stroke="#6a3a10" stroke-width="1.3"/>`;
      g+=`<path d="M${fx+30},${fy-38} Q${fx+fw/2},${fy-66} ${fx+fw-40},${fy-40}" stroke="#f4cc88" stroke-width="7" fill="none" stroke-linecap="round" opacity=".45"/>`;
      for(let i=0;i<22;i++){ const x=R(fx+20+rnd()*(fw-40)); const t=(x-fx)/fw; const y=R(fy-8-Math.sin(t*Math.PI)*48*rnd()); g+=`<path d="M${x},${y} q3,-3 7,0" stroke="#6a3a10" stroke-width="1.6" fill="none" opacity=".6"/>`; }
      g+=`<path d="M${fx-10},${fy} L${fx+4},${fy+fh} H${fx+fw-4} L${fx+fw+10},${fy} Z" fill="${lg('#a8aeb6','#5e646c',90)}" stroke="#3a3e44" stroke-width="1.4"/>`;
      g+=`<path d="M${fx-14},${fy} H${fx+fw+14}" stroke="#3a3e44" stroke-width="4" stroke-linecap="round"/>`;
      g+=`<path d="M${fx+20},${fy+18} H${fx+fw-20}" stroke="#d0d6dc" stroke-width="2" opacity=".5"/>`;
      // herausgezogener angeschnittener Laib rechts daneben (Anschnittfläche)
      const lx=420, ly=150;
      g+=`<path d="M${lx},${ly+52} V${ly-14} Q${lx+6},${ly-74} ${lx+70},${ly-78} L${lx+190},${ly-78} Q${lx+250},${ly-72} ${lx+254},${ly-14} V${ly+52} Z" fill="${lg('#d89a4a','#9a5a1a',90)}" stroke="#6a3a10" stroke-width="1.3"/>`;
      // Anschnittfläche (links, Krume)
      g+=`<path d="M${lx},${ly+52} V${ly-14} Q${lx+6},${ly-74} ${lx+70},${ly-78} L${lx+70},${ly+52} Z" fill="#7a4618"/>`;
      g+=`<path d="M${lx+6},${ly+48} V${ly-12} Q${lx+12},${ly-66} ${lx+66},${ly-70} V${ly+48} Z" fill="${lg('#fbf0d4','#efdcaa',0)}"/>`;
      // Scheibe davor
      const sx=lx-30, sy=ly+4;
      g+=`<path d="M${sx-36},${sy+56} V${sy-6} Q${sx-32},${sy-62} ${sx+18},${sy-64} Q${sx+46},${sy-60} ${sx+48},${sy-6} V${sy+56} Z" fill="#8a4e1c" stroke="#5a3010" stroke-width="1.2"/>`;
      g+=`<path d="M${sx-30},${sy+50} V${sy-4} Q${sx-26},${sy-54} ${sx+18},${sy-56} Q${sx+40},${sy-52} ${sx+42},${sy-4} V${sy+50} Z" fill="${lg('#fdf4dc','#f0ddb0',0)}"/>`;
      for(let i=0;i<46;i++) g+=pore(R(sx-24+rnd()*60),R(sy-44+rnd()*90));
      for(let i=0;i<20;i++) g+=zw(R(sx-24+rnd()*58),R(sy-40+rnd()*84));
      for(let i=0;i<24;i++) g+=pore(R(lx+12+rnd()*50),R(ly-50+rnd()*94));
      for(let i=0;i<12;i++) g+=zw(R(lx+12+rnd()*46),R(ly-44+rnd()*86));
      g+=T(lx+80,266,'Anschnitt: Zwiebelstücke in der Krume','var(--muted)',10.5,700);
      g+=T(fx+fw/2,266,'Zwiebelbrot in der Kastenform','var(--ink)',13,800);
      // Zwiebeln
      const zwiebel=(x,y,s,halb)=>halb
        ? `<ellipse cx="${x}" cy="${y}" rx="${s}" ry="${R(s*0.86)}" fill="#f6ecd0" stroke="#b88a3a" stroke-width="1.2"/>`+[0.75,0.5,0.25].map(f=>`<ellipse cx="${x}" cy="${R(y+s*0.05)}" rx="${R(s*f)}" ry="${R(s*0.86*f)}" fill="none" stroke="#d8b46a" stroke-width="1.2"/>`).join('')
        : `<path d="M${x},${y-s*1.25} Q${x+s*1.15},${y-s*0.5} ${x+s},${y+s*0.4} Q${x+s*0.6},${y+s} ${x},${y+s} Q${x-s*0.6},${y+s} ${x-s},${y+s*0.4} Q${x-s*1.15},${y-s*0.5} ${x},${y-s*1.25} Z" fill="${lg('#e8b060','#a8642a',45)}" stroke="#6a3a14" stroke-width="1.1"/><path d="M${x},${y-s*1.2} q2,-8 -2,-14" stroke="#8a6a3a" stroke-width="1.6" fill="none"/>`+[-0.45,0,0.45].map(f=>`<path d="M${R(x+f*s)},${R(y-s*0.9)} Q${R(x+f*s*1.4)},${y} ${R(x+f*s*0.8)},${R(y+s*0.9)}" stroke="#c8843a" stroke-width=".9" fill="none" opacity=".7"/>`).join('');
      g+=zwiebel(720,92,22,false)+zwiebel(718,170,20,true);
      g+=T(712,206,'2 große Zwiebeln','var(--muted)',10.5,700);
      return {vb:'0 0 760 280',breit:true,leg:[],svg:g}; },
    zwiebelbrot_leiste(){ return Z.rezept_leiste([['abkuehlen','1 · Zwiebeln glasig braten, abkühlen',{t:'abkühlen!'}],['schuessel','2 · Mehl, Hefe, Zucker mischen',{zutaten:['#f4ecd8','#e8d8a0','#ffffff']}],['kneten','3 · Wasser, Öl, Salz – 8–10 Min. kneten',{t:'8–10 Min.'}],['schuessel','4 · Zwiebeln unterkneten',{zutaten:['#e8c070','#d8a04a','#e8c070']}],['warm','5 · 60 Min. warm gehen',{t:'60 Min.'}],['kasten','6 · In die Form, 20 Min. ruhen',{t:'20 Min.',auf:true}],['ofen','7 · 180 °C O/U, 45–50 Min.',{t:'180 °C'}]]); },
