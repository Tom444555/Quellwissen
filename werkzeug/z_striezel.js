    striezel_bild(){ seed=901; let g='';
      const T=(x,y,t,c='var(--muted)',s=11,w=700)=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:middle;paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      const zucker=(x0,y0,w,h,n)=>{ let s=''; for(let i=0;i<n;i++){ const x=R(x0+rnd()*w), y=R(y0+rnd()*h); s+=`<rect x="${x}" y="${y}" width="1.6" height="1.6" fill="${rnd()<.6?'#fff8e8':'#7a3a14'}" opacity="${R(.5+rnd()*.5)}" transform="rotate(${R(rnd()*90)} ${x} ${y})"/>`; } return s; };
      // stehender Striezel
      const cx=150, top=46, H=170, W=58;
      g+=`<ellipse cx="${cx}" cy="${top+H+4}" rx="${W+16}" ry="9" fill="#000" opacity=".12"/>`;
      for(let i=10;i>=0;i--){ const y=top+16+i*15;
        g+=`<path d="M${cx-W-1},${y} Q${cx},${y+16} ${cx+W+1},${y} L${cx+W+1},${y+15} Q${cx},${y+31} ${cx-W-1},${y+15} Z" fill="${lg('#e8a050','#a85a1c',90)}"/>`;
        g+=`<path d="M${cx-W-1},${y+15} Q${cx},${y+31} ${cx+W+1},${y+15}" stroke="#7a3a10" stroke-width="1.4" fill="none" opacity=".7"/>`; }
      g+=zucker(cx-W,top+16,2*W,H-6,260);
      g+=`<ellipse cx="${cx}" cy="${top+16}" rx="${W}" ry="15" fill="${lg('#f0c078','#c8803a',90)}"/><ellipse cx="${cx}" cy="${top+17}" rx="${W-8}" ry="10" fill="${lg('#f6dca8','#e8b878',90)}"/>`;
      // abgewickelte Spirale oben
      g+=`<path d="M${cx+W-6},${top+14} C${cx+W+20},${top-6} ${cx+W+34},${top+6} ${cx+W+26},${top+30}" stroke="${lg('#e8a050','#a85a1c',0)}" stroke-width="12" fill="none" stroke-linecap="round"><animate attributeName="d" values="M${cx+W-6},${top+14} C${cx+W+20},${top-6} ${cx+W+34},${top+6} ${cx+W+26},${top+30};M${cx+W-6},${top+14} C${cx+W+26},${top-12} ${cx+W+44},${top+2} ${cx+W+38},${top+28};M${cx+W-6},${top+14} C${cx+W+20},${top-6} ${cx+W+34},${top+6} ${cx+W+26},${top+30}" dur="5s" repeatCount="indefinite"/></path>`;
      for(let i=0;i<3;i++) g+=`<path d="M${cx-20+i*20},${top} q-6,-14 0,-28 q6,-14 0,-26" stroke="#d8d0c8" stroke-width="3" fill="none" stroke-linecap="round" opacity="0"><animate attributeName="opacity" values="0;.8;0" dur="3s" begin="${i*.9}s" repeatCount="indefinite"/><animateTransform attributeName="transform" type="translate" values="0 6;0 -12" dur="3s" begin="${i*.9}s" repeatCount="indefinite"/></path>`;
      g+=T(cx,top+H+28,'Baumstriezel (Kürtőskalács)','var(--ink)',13,800);
      // Querschnitt
      const qx=360,qy=120;
      g+=`<circle cx="${qx}" cy="${qy}" r="56" fill="${lg('#e8a050','#a85a1c',45)}"/><circle cx="${qx}" cy="${qy}" r="44" fill="${lg('#f6dca8','#ecc890',45)}"/><circle cx="${qx}" cy="${qy}" r="38" fill="var(--surface)"/>`;
      g+=zucker(qx-56,qy-56,112,112,90).replace(/<rect /g,'<rect clip-path="url(#strq)" ');
      g+=`<defs><clipPath id="strq"><path d="M${qx-56},${qy} a56,56 0 1,0 112,0 a56,56 0 1,0 -112,0 M${qx-44},${qy} a44,44 0 1,1 88,0 a44,44 0 1,1 -88,0" clip-rule="evenodd"/></clipPath></defs>`;
      [['außen: Zimtzucker, karamellisiert',qx,qy-66],['innen hohl (Holzrolle)',qx,qy+76],['dazwischen: weicher Hefeteig',qx,qy+92]].forEach(([t,x,y])=>g+=T(x,y,t,'var(--ink)',10.5,700));
      
      // liegender Striezel mit Spirale
      const lx=548, ly=150;
      for(let i=0;i<8;i++){ const x=lx+i*18; g+=`<ellipse cx="${x}" cy="${ly}" rx="12" ry="40" fill="${lg('#eaa656','#a85a1c',0)}" stroke="#7a3a10" stroke-width="1"/>`; }
      g+=zucker(lx-10,ly-38,150,76,180);
      g+=`<ellipse cx="${lx+140}" cy="${ly}" rx="14" ry="38" fill="${lg('#f6dca8','#e8b878',0)}"/><ellipse cx="${lx+141}" cy="${ly}" rx="9" ry="30" fill="#5a3a24" opacity=".55"/>`;
      g+=`<path d="M${lx+150},${ly+30} C${lx+190},${ly+40} ${lx+210},${ly+10} ${lx+190},${ly-6}" stroke="${lg('#e8a050','#a85a1c',0)}" stroke-width="13" fill="none" stroke-linecap="round"/>`;
      g+=T(lx+80,ly+66,'zum Abwickeln – Streifen für Streifen','var(--muted)',10.5,700);
      return {vb:'0 0 760 250',breit:true,leg:[],svg:g}; },
    striezel_schritte(){ seed=902; let g=''; const n=6, w=126;
      const T=(x,y,t,s=10.5,c='var(--ink)',wt=800)=>`<text x="${x}" y="${y}" style="fill:${c};font:${wt} ${s}px var(--label);text-anchor:middle;paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      const holz=(x,y,L,papier)=>`<rect x="${x-L/2-18}" y="${y-5}" width="18" height="10" rx="4" fill="${lg('#d8a868','#9a6a38',90)}"/><rect x="${x+L/2}" y="${y-5}" width="18" height="10" rx="4" fill="${lg('#d8a868','#9a6a38',90)}"/><rect x="${x-L/2}" y="${y-12}" width="${L}" height="24" rx="5" fill="${papier?lg('#f2e8d8','#c8b8a0',90):lg('#e8c08a','#b8884a',90)}" stroke="${papier?'#a89878':'#7a5a30'}"/>`;
      for(let i=1;i<n;i++) g+=`<path d="M${i*w},14 V196" stroke="var(--line)"/>`;
      const X=i=>i*w+w/2;
      // 1 Streifen schneiden
      g+=`<rect x="10" y="70" width="106" height="66" rx="4" fill="${lg('#f6ecd0','#e4d2a8',90)}" stroke="#c8b080"/>`;
      for(let k=1;k<5;k++) g+=`<path d="M10,${70+k*13} H116" stroke="#c8b080" stroke-width="1.2"/>`;
      g+=`<g><circle cx="40" cy="96" r="13" fill="${lg('#f0f2f4','#9aa0a8',45)}" stroke="#6a7078"/><circle cx="40" cy="96" r="3" fill="#6a7078"/><path d="M40,96 l26,-30" stroke="#5a6068" stroke-width="5" stroke-linecap="round"/><animateTransform attributeName="transform" type="translate" values="0 0;50 0;0 0" dur="3s" repeatCount="indefinite"/></g>`;
      g+=T(X(0),160,'1 · Teig ausrollen,',9.5)+T(X(0),173,'2 cm breite',9.5)+T(X(0),186,'Streifen schneiden',9.5);
      // 2 Backpapier
      g+=holz(X(1),104,80,true)+`<path d="M${X(1)-40},92 l10,24 M${X(1)-20},92 l10,24 M${X(1)},92 l10,24 M${X(1)+20},92 l10,24" stroke="#a89878" stroke-width=".8"/>`;
      g+=T(X(1),160,'2 · Nudelholz mit',9.5)+T(X(1),173,'Backpapier straff',9.5)+T(X(1),186,'umwickeln',9.5);
      // 3 Wickeln (animiert)
      g+=holz(X(2),104,80,true);
      for(let k=0;k<6;k++){ const t=(k*0.12+0.05).toFixed(2), t2=(k*0.12+0.1).toFixed(2); g+=`<path d="M${X(2)-38+k*13},92 q4,12 0,24" stroke="#e8d2a0" stroke-width="11" fill="none" opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;${t};${t2};.92;1" dur="5s" repeatCount="indefinite"/></path>`; }
      g+=`<path d="M${X(2)+40},92 q14,-30 -2,-50" stroke="#e8d2a0" stroke-width="10" fill="none" stroke-linecap="round"/>`;
      g+=T(X(2),160,'3 · Streifen',9.5)+T(X(2),173,'überlappend wickeln,',9.5)+T(X(2),186,'Enden andrücken',9.5);
      // 4 Auflaufform gehen lassen
      g+=`<path d="M${X(3)-52},110 h104 l-8,30 h-88 z" fill="${lg('#ffffff','#d8dce0',90)}" stroke="#9aa0a8"/>`;
      g+=`<g transform-origin="${X(3)} 100">`+holz(X(3),100,74,false)+`<animateTransform attributeName="transform" type="scale" values="1 1;1 1.2;1 1" dur="5s" repeatCount="indefinite"/></g>`;
      g+=T(X(3),70,'20 Min.',12,'var(--muted)')+T(X(3),160,'4 · frei hängend',9.5)+T(X(3),173,'auf die Form,',9.5)+T(X(3),186,'20 Min. gehen lassen',9.5);
      // 5 Butter + Zimtzucker
      g+=holz(X(4),104,80,false);
      g+=`<g><path d="M${X(4)-10},40 l20,46" stroke="#3a3e44" stroke-width="5" stroke-linecap="round"/><path d="M${X(4)+10},86 l-6,10 l14,0 z" fill="#3a3e44"/><animateTransform attributeName="transform" type="translate" values="-26 0;26 0;-26 0" dur="2.5s" repeatCount="indefinite"/></g>`;
      for(let k=0;k<8;k++) g+=`<circle cx="${R(X(4)-36+rnd()*72)}" cy="60" r="1.6" fill="${k%2?'#fff8e8':'#8a4a1a'}"><animate attributeName="cy" values="60;92" dur="1.4s" begin="${R(rnd()*1.4)}s" repeatCount="indefinite"/></circle>`;
      g+=T(X(4),160,'5 · mit Butter',9.5)+T(X(4),173,'einpinseln, rundum',9.5)+T(X(4),186,'Zimtzucker',9.5);
      // 6 Ofen
      const ox=X(5); g+=`<rect x="${ox-54}" y="48" width="108" height="96" rx="8" fill="${lg('#4a4f56','#2a2e34',90)}"/><rect x="${ox-44}" y="58" width="88" height="70" rx="4" fill="#1a1c20"/>`;
      g+=`<g>`+holz(ox,100,52,false).replace(/#e8c08a/g,'#e8a050').replace(/#b8884a/g,'#a85a1c')+`<animateTransform attributeName="transform" type="rotate" values="0 ${ox} 100;0 ${ox} 100;180 ${ox} 100;180 ${ox} 100" keyTimes="0;.45;.55;1" dur="6s" repeatCount="indefinite"/></g>`;
      g+=`<path d="M${ox-40},124 h80" stroke="#e8602a" stroke-width="3"><animate attributeName="opacity" values=".4;1;.4" dur="1.5s" repeatCount="indefinite"/></path>`;
      g+=T(ox,40,'180 °C Umluft',11,'#c0501a')+T(ox,160,'6 · 10 Min. backen,',9.5)+T(ox,173,'drehen, nochmal',9.5)+T(ox,186,'10 Min. goldbraun',9.5);
      return {vb:'0 0 756 200',breit:true,leg:[],svg:g}; },
    leiste_striezel_teig(){ return Z.rezept_leiste([['schuessel','1 · Mehl, Hefe, Zucker, Salz mischen',{zutaten:['#f4f0e8','#e8d8a0','#ffffff','#ffffff']}],['warm','2 · Milch lauwarm (nicht kochen)',{t:'~37 °C',f:'#f8f4ea'}],['kneten','3 · Milch + Eier, 5 Min. kneten',{t:'glatt'}],['warm','4 · 45 Min. warm gehen lassen',{t:'45 Min.'}],['teilen','5 · Teig halbieren, eine Hälfte kühl',{n:2,t:'½ + ½'}]]); },
