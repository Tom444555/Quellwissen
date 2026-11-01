    senfeier_bild(){ seed=1701; let g='';
      const T=(x,y,t,c='var(--muted)',s=11,w=700)=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:middle;paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      const pet=(cx,cy,r,n)=>{ let s=''; for(let i=0;i<n;i++){ const a=rnd()*6.283, d=Math.sqrt(rnd())*r, x=R(cx+Math.cos(a)*d), y=R(cy+Math.sin(a)*d*0.7); s+=`<ellipse cx="${x}" cy="${y}" rx="${R(1.6+rnd()*1.6)}" ry="${R(1+rnd())}" fill="${rnd()<.6?'#3f7a2a':'#5f9a38'}" transform="rotate(${R(rnd()*180)} ${x} ${y})"/>`; } return s; };
      const ei=(x,y,s,rot)=>`<g transform="rotate(${rot} ${x} ${y})"><ellipse cx="${x}" cy="${y}" rx="${R(s)}" ry="${R(s*0.72)}" fill="${lg('#fffdf8','#e6e0d2',90)}" stroke="#b8ad96" stroke-width="1.1"/><ellipse cx="${R(x+s*0.08)}" cy="${R(y+s*0.04)}" rx="${R(s*0.48)}" ry="${R(s*0.4)}" fill="${lg('#f8c838','#e09a18',60)}" stroke="#c88a18" stroke-width=".8"/><ellipse cx="${R(x-s*0.1)}" cy="${R(y-s*0.1)}" rx="${R(s*0.14)}" ry="${R(s*0.08)}" fill="#fff4c0" opacity=".7"/></g>`;
      const kart=(x,y,s,rot)=>`<g transform="rotate(${rot} ${x} ${y})"><ellipse cx="${x}" cy="${y}" rx="${R(s)}" ry="${R(s*0.7)}" fill="${lg('#f6e2a0','#d8b860',80)}" stroke="#a8884a" stroke-width="1.1"/><path d="M${R(x-s*0.5)},${R(y-s*0.3)} q${R(s*0.3)},${R(-s*0.25)} ${R(s*0.7)},${R(-s*0.1)}" stroke="#fff6d0" stroke-width="2.4" fill="none" stroke-linecap="round" opacity=".7"/></g>`;
      // Teller
      const cx=250, cy=142;
      g+=`<ellipse cx="${cx}" cy="${cy+12}" rx="226" ry="76" fill="#000" opacity=".1"/>`;
      g+=`<ellipse cx="${cx}" cy="${cy}" rx="220" ry="76" fill="${lg('#fbfaf6','#dcdad2',90)}" stroke="#b8b4aa" stroke-width="1.3"/><ellipse cx="${cx}" cy="${cy+4}" rx="168" ry="54" fill="none" stroke="#d4d0c6" stroke-width="1.2"/>`;
      // Senfsoße als See
      g+=`<path d="M${cx-150},${cy+6} C${cx-150},${cy-44} ${cx-30},${cy-56} ${cx+20},${cy-40} C${cx+60},${cy-28} ${cx+60},${cy+44} ${cx-10},${cy+50} C${cx-80},${cy+56} ${cx-150},${cy+44} ${cx-150},${cy+6} Z" fill="${lg('#f2d460','#d4a628',90)}" stroke="#b88a20" stroke-width="1.2"/>`;
      g+=`<path d="M${cx-120},${cy-18} q40,-22 90,-18" stroke="#fbeaa0" stroke-width="5" fill="none" stroke-linecap="round" opacity=".6"/>`;
      for(let i=0;i<22;i++){ const x=R(cx-130+rnd()*170), y=R(cy-30+rnd()*70); g+=`<circle cx="${x}" cy="${y}" r="${R(.7+rnd()*.8)}" fill="#8a5a18" opacity=".55"/>`; }
      // Speckwürfel (herzhafte Variante)
      for(let i=0;i<9;i++){ const x=R(cx-120+rnd()*150), y=R(cy-20+rnd()*56); g+=`<rect x="${x}" y="${y}" width="8" height="6" rx="1.5" fill="${lg('#e8a080','#b0503a',90)}" stroke="#7a3020" stroke-width=".6" transform="rotate(${R(rnd()*60-30)} ${x} ${y})"/><rect x="${x+1}" y="${y+1}" width="6" height="1.6" fill="#fbe8d8" opacity=".8" transform="rotate(${R(rnd()*20-10)} ${x} ${y})"/>`; }
      [[cx-100,cy-8,30,-8],[cx-40,cy-20,30,10],[cx-70,cy+26,30,4],[cx+4,cy+16,28,-12]].forEach(([x,y,s,r])=>g+=ei(x,y,s,r));
      g+=pet(cx-60,cy+4,90,40);
      // Salzkartoffeln rechts
      [[cx+120,cy-18,26,-10],[cx+150,cy+16,24,14],[cx+100,cy+26,25,4],[cx+160,cy-20,20,30]].sort((a,b)=>a[1]-b[1]).forEach(([x,y,s,r])=>g+=kart(x,y,s,r));
      g+=pet(cx+130,cy+4,40,22);
      g+=T(cx,cy+102,'Eier in Senfsoße mit Salzkartoffeln','var(--ink)',13,800);
      // Senfglas
      const sx=560, sy=118;
      g+=`<path d="M${sx-30},${sy-40} L${sx-34},${sy+44} Q${sx},${sy+54} ${sx+34},${sy+44} L${sx+30},${sy-40} Z" fill="${lg('#f0f4f6','#c8d4dc',0)}" stroke="#7a8a98" stroke-width="1.3" opacity=".95"/>`;
      g+=`<path d="M${sx-31},${sy-24} L${sx-33},${sy+42} Q${sx},${sy+50} ${sx+33},${sy+42} L${sx+31},${sy-24} Z" fill="${lg('#e8c040','#c09420',90)}" opacity=".9"/>`;
      g+=`<rect x="${sx-34}" y="${sy-56}" width="68" height="18" rx="4" fill="${lg('#c84030','#8a2018',90)}" stroke="#6a1810"/>`;
      g+=`<rect x="${sx-26}" y="${sy-6}" width="52" height="30" rx="3" fill="#fbf6e8" stroke="#b8ad96"/><text x="${sx}" y="${sy+14}" style="fill:#7a3a10;font:800 11px var(--label);text-anchor:middle">SENF</text>`;
      g+=T(sx,sy+74,'mittelscharfer Senf','var(--muted)',10.5,700);
      // Topf mit Mehlschwitze
      const px=680, py=120;
      g+=`<path d="M${px-46},${py-20} L${px-40},${py+40} Q${px},${py+52} ${px+40},${py+40} L${px+46},${py-20} Z" fill="${lg('#4a4a50','#222226',0)}" stroke="#101012"/><ellipse cx="${px}" cy="${py-20}" rx="46" ry="10" fill="${lg('#f0d060','#d8aa30',0)}" stroke="#101012"/>`;
      g+=`<path d="M${px+46},${py-14} h22" stroke="#1e1e22" stroke-width="6" stroke-linecap="round"/><path d="M${px-6},${py-70} L${px+6},${py-22}" stroke="#a8763a" stroke-width="4" stroke-linecap="round"/>`;
      g+=T(px,py+74,'Mehlschwitze + Brühe','var(--muted)',10.5,700);
      [['hart gekochte Eier',cx-180,cy-60],['Speckwürfel (Variante)',cx-20,cy-74]].forEach(([t,x,y])=>g+=T(x,y,t,'var(--ink)',10.5,700));
      return {vb:'0 0 760 260',breit:true,leg:[],svg:g}; },
    senfeier_leiste(){ return Z.rezept_leiste([['kartoffel','1 · Kartoffeln ca. 20 Min. in Salzwasser'],['topf','2 · Eier ca. 10 Min. hart kochen, pellen',{t:'10 Min.'}],['topf','3 · Butter + Mehl: Mehlschwitze',{t:'goldgelb'}],['schuessel','4 · Brühe und Sahne nach und nach einrühren',{f:'#f4ecd0'}],['topf','5 · Senf einrühren, 4–5 Min. köcheln',{t:'4–5 Min.'}],['schuessel','6 · Eier in der Soße warmhalten',{f:'#e8c840',zutaten:['#ffffff','#f8c838','#3f7a2a']}]]); },
    kartoffelsalat_bild(){ seed=1801; let g='';
      const T=(x,y,t,c='var(--muted)',s=11,w=700)=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:middle;paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      // Schüssel mit Salat
      const bx=220, by=150;
      g+=`<ellipse cx="${bx}" cy="${by+70}" rx="150" ry="16" fill="#000" opacity=".1"/>`;
      g+=`<path d="M${bx-170},${by-20} Q${bx-160},${by+70} ${bx},${by+74} Q${bx+160},${by+70} ${bx+170},${by-20} Z" fill="${lg('#f4f6f8','#b8c4cc',90)}" stroke="#7a8a98" stroke-width="1.4"/>`;
      g+=`<path d="M${bx-120},${by+50} q120,26 240,0" stroke="#5a8aa8" stroke-width="3" fill="none" opacity=".5"/>`;
      g+=`<ellipse cx="${bx}" cy="${by-20}" rx="170" ry="36" fill="${lg('#f8f0d0','#e8d8a0',90)}" stroke="#a89a6a" stroke-width="1.2"/>`;
      // Hügel Salat
      g+=`<path d="M${bx-160},${by-18} Q${bx-120},${by-70} ${bx},${by-76} Q${bx+120},${by-70} ${bx+160},${by-18} Q${bx},${by+12} ${bx-160},${by-18} Z" fill="${lg('#faf2d4','#eadcac',90)}" stroke="#c8b880" stroke-width="1"/>`;
      const inBowl=()=>{ const a=rnd()*6.283, d=Math.sqrt(rnd()); return [R(bx+Math.cos(a)*d*140), R(by-34+Math.sin(a)*d*34)]; };
      for(let i=0;i<34;i++){ const [x,y]=inBowl(); g+=`<path d="M${x-9},${y} a9,6 0 0 1 18,0 Z" fill="${lg('#f6e4a0','#dcc070',90)}" stroke="#b89a50" stroke-width=".7" transform="rotate(${R(rnd()*50-25)} ${x} ${y})"/>`; }
      for(let i=0;i<16;i++){ const [x,y]=inBowl(); g+=`<rect x="${x}" y="${y}" width="7" height="6" rx="1.4" fill="${lg('#8aa840','#5a7a24',90)}" stroke="#3a5a18" stroke-width=".6" transform="rotate(${R(rnd()*60)} ${x} ${y})"/>`; }
      for(let i=0;i<8;i++){ const [x,y]=inBowl(); g+=`<rect x="${x}" y="${y}" width="7" height="6" rx="1.4" fill="#fbf2d8" stroke="#c84a3a" stroke-width="1" transform="rotate(${R(rnd()*60)} ${x} ${y})"/>`; }
      for(let i=0;i<6;i++){ const [x,y]=inBowl(); g+=`<rect x="${x}" y="${y}" width="5" height="5" rx="1" fill="#fbfaf2" stroke="#d8d0b8" stroke-width=".6"/>`; }
      // Ei-Garnitur oben
      [[bx-40,by-60],[bx+10,by-64],[bx+60,by-56]].forEach(([x,y])=>g+=`<ellipse cx="${x}" cy="${y}" rx="14" ry="10" fill="#fffdf6" stroke="#c8c0aa"/><circle cx="${x+1}" cy="${y}" r="5.5" fill="${lg('#f8c838','#e09a18',60)}"/>`);
      for(let i=0;i<30;i++){ const [x,y]=inBowl(); g+=`<circle cx="${x}" cy="${R(y-6)}" r="1.4" fill="#3f7a2a"/>`; }
      g+=T(bx,by+100,'Kartoffelsalat mit Mayonnaise','var(--ink)',13,800);
      // Wiener auf Brett
      const wx=560, wy=150;
      g+=`<rect x="${wx-120}" y="${wy-30}" width="240" height="96" rx="14" fill="${lg('#d8a868','#a8743a',90)}" stroke="#7a4a1e" stroke-width="1.3"/>`;
      for(let i=0;i<4;i++) g+=`<path d="M${wx-110},${wy-14+i*22} q110,${R(rnd()*6-3)} 220,0" stroke="#9a6a32" stroke-width="1" fill="none" opacity=".5"/>`;
      const wurst=(y,dx)=>`<path d="M${wx-92+dx},${y} Q${wx+dx},${y-14} ${wx+92+dx},${y}" stroke="#7a3a1e" stroke-width="20" fill="none" stroke-linecap="round"/><path d="M${wx-92+dx},${y} Q${wx+dx},${y-14} ${wx+92+dx},${y}" stroke="${'#c8683a'}" stroke-width="17" fill="none" stroke-linecap="round"/><path d="M${wx-80+dx},${y-5} Q${wx+dx},${y-17} ${wx+80+dx},${y-5}" stroke="#eaa070" stroke-width="4" fill="none" stroke-linecap="round" opacity=".7"/>`;
      g+=wurst(wy+4,0)+wurst(wy+30,6)+wurst(wy+54,-4);
      // Senfklecks
      g+=`<ellipse cx="${wx+96}" cy="${wy-12}" rx="14" ry="8" fill="${lg('#f0d050','#c89a20',90)}" stroke="#a87a18"/>`;
      g+=T(wx,wy+96,'Wiener Würstchen, nur heiß gezogen','var(--ink)',12,800);
      // Zutaten oben rechts
      const zy=58;
      g+=`<ellipse cx="470" cy="${zy}" rx="13" ry="22" fill="${lg('#9ab84a','#5a7a24',0)}" stroke="#3a5a18" transform="rotate(-30 470 ${zy})"/>`;
      g+=`<circle cx="540" cy="${zy}" r="18" fill="${lg('#e85040','#a82418',45)}" stroke="#7a1810"/><path d="M540,${zy-18} q2,-8 6,-10" stroke="#6a4a2a" stroke-width="2" fill="none"/>`;
      g+=`<ellipse cx="610" cy="${zy}" rx="18" ry="16" fill="${lg('#f4e0b0','#c8a060',60)}" stroke="#8a6a30"/><path d="M610,${zy-16} q-3,-8 2,-12" stroke="#8a6a30" stroke-width="2" fill="none"/>`;
      g+=`<ellipse cx="680" cy="${zy}" rx="14" ry="18" fill="#fffdf6" stroke="#c8c0aa"/>`;
      [['Gewürzgurke',470],['Apfel',540],['Zwiebel',610],['Ei (Variante)',680]].forEach(([t,x])=>g+=T(x,zy+36,t,'var(--muted)',10,700));
      return {vb:'0 0 760 270',breit:true,leg:[],svg:g}; },
    kartoffelsalat_leiste(){ return Z.rezept_leiste([['kartoffel','1 · Kartoffeln 20–25 Min. garen'],['teilen','2 · Zwiebel, Apfel, Gurken würfeln',{n:6,t:'Würfel'}],['teilen','3 · Kartoffeln pellen, in dünne Scheiben',{n:6,t:'Scheiben'}],['schuessel','4 · Heiße Brühe darübergießen',{f:'#e8d090'}],['schuessel','5 · Mayo + 2 EL Gurkenwasser, ziehen lassen',{f:'#f4ecc8',zutaten:['#7a9a3a','#c84a3a']}],['topf','6 · Wiener ca. 5 Min. in heißem Wasser',{t:'nicht kochen'}]]); },
