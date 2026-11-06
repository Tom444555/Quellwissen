    dinkeljoghurt_bild(){ seed=1901; let g='';
      const T=(x,y,t,c='var(--muted)',s=11,w=700)=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:middle;paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      const flocke=(x,y)=>{ const r=R(rnd()*180); return `<ellipse cx="${x}" cy="${y}" rx="${R(3+rnd()*1.6)}" ry="${R(2+rnd())}" fill="${rnd()<.5?'#f4ead0':'#e6d6aa'}" stroke="#b8a070" stroke-width=".6" transform="rotate(${r} ${x} ${y})"/>`; };
      const broetchen=(x,y,s)=>{ let b=`<ellipse cx="${x}" cy="${R(y+s*0.62)}" rx="${R(s*1.02)}" ry="${R(s*0.26)}" fill="#000" opacity=".14"/>`;
        b+=`<path d="M${R(x-s)},${R(y+s*0.42)} Q${R(x-s*1.04)},${R(y-s*0.62)} ${x},${R(y-s*0.7)} Q${R(x+s*1.04)},${R(y-s*0.62)} ${R(x+s)},${R(y+s*0.42)} Q${x},${R(y+s*0.66)} ${R(x-s)},${R(y+s*0.42)} Z" fill="${lg(shade('#e0a85a',0.18),shade('#b8742e',-0.08),90)}" stroke="${shade('#b8742e',-0.4)}" stroke-width="1.1"/>`;
        b+=`<path d="M${R(x-s*0.62)},${R(y-s*0.3)} Q${R(x-s*0.1)},${R(y-s*0.62)} ${R(x+s*0.5)},${R(y-s*0.36)}" stroke="#f6d6a0" stroke-width="${R(s*0.14)}" fill="none" stroke-linecap="round" opacity=".55"/>`;
        b+=`<path d="M${R(x-s*0.92)},${R(y+s*0.3)} Q${x},${R(y+s*0.52)} ${R(x+s*0.92)},${R(y+s*0.3)}" stroke="${shade('#f0d0a0',0.05)}" stroke-width="1.6" fill="none" opacity=".7"/>`;
        for(let i=0;i<16;i++){ const a=rnd()*6.283, d=Math.sqrt(rnd()); b+=flocke(R(x+Math.cos(a)*d*s*0.72), R(y-s*0.22+Math.sin(a)*d*s*0.34)); }
        return b; };
      // Backblech mit 12 Brötchen
      const bx=300, by=140;
      g+=`<rect x="${bx-262}" y="${by-92}" width="524" height="192" rx="10" fill="${lg('#8a9098','#5a6068',90)}" stroke="#3a3e44" stroke-width="1.4"/>`;
      g+=`<rect x="${bx-250}" y="${by-82}" width="500" height="172" rx="4" fill="${lg('#f6eedc','#e4d6b4',90)}" stroke="#c8b890" stroke-width="1"/>`;
      for(let i=0;i<5;i++) g+=`<path d="M${bx-244},${R(by-60+i*34)} q${R(240)},${R(rnd()*6-3)} 488,0" stroke="#d8c8a0" stroke-width=".8" fill="none" opacity=".6"/>`;
      for(let r=0;r<2;r++) for(let c=0;c<6;c++){ const x=bx-208+c*83+(r?14:0)-(r?7:0), y=by-34+r*82; g+=broetchen(R(x),y,34); }
      g+=T(bx,by+128,'12 Dinkel-Joghurtbrötchen mit Haferflocken','var(--ink)',13,800);
      // Joghurtbecher
      const jx=636, jy=96;
      g+=`<path d="M${jx-30},${jy-34} L${jx-24},${jy+34} Q${jx},${jy+42} ${jx+24},${jy+34} L${jx+30},${jy-34} Z" fill="${lg('#ffffff','#dfe6ea',0)}" stroke="#8a98a4" stroke-width="1.3"/>`;
      g+=`<ellipse cx="${jx}" cy="${jy-34}" rx="30" ry="7" fill="#f8f8f4" stroke="#8a98a4"/><rect x="${jx-22}" y="${jy-12}" width="44" height="22" rx="3" fill="#7aa8c8"/><text x="${jx}" y="${jy+4}" style="fill:#fff;font:800 9.5px var(--label);text-anchor:middle">3,5 %</text>`;
      g+=T(jx,jy+60,'Joghurt','var(--muted)',10.5,700);
      // Haferflocken-Schälchen
      const hx=712, hy=112;
      g+=`<path d="M${hx-30},${hy-6} Q${hx-28},${hy+24} ${hx},${hy+26} Q${hx+28},${hy+24} ${hx+30},${hy-6} Z" fill="${lg('#c8ccd2','#8a9098',90)}" stroke="#5a6068" stroke-width="1.2"/><ellipse cx="${hx}" cy="${hy-6}" rx="30" ry="7" fill="#e8dcbc" stroke="#5a6068"/>`;
      for(let i=0;i<12;i++) g+=flocke(R(hx-22+rnd()*44),R(hy-10+rnd()*7));
      g+=T(hx,hy+44,'Haferflocken','var(--muted)',10.5,700);
      // Mehltüte
      const mx=674, my=206;
      g+=`<path d="M${mx-34},${my-30} L${mx-30},${my+34} H${mx+30} L${mx+34},${my-30} L${mx+24},${my-42} H${mx-24} Z" fill="${lg('#f6f0e2','#dcd0b4',0)}" stroke="#a8986e" stroke-width="1.2"/>`;
      g+=`<text x="${mx}" y="${my-4}" style="fill:#7a5a2a;font:800 10px var(--label);text-anchor:middle">DINKEL</text><text x="${mx}" y="${my+12}" style="fill:#7a5a2a;font:800 10px var(--label);text-anchor:middle">630</text>`;
      g+=T(mx,my+52,'Dinkelmehl 520 g','var(--muted)',10.5,700);
      return {vb:'0 0 760 280',breit:true,leg:[],svg:g}; },
    dinkeljoghurt_leiste(){ return Z.rezept_leiste([['schuessel','1 · Mehl, Hefe, Salz mischen',{zutaten:['#f4ecd8','#e8d8a0','#ffffff']}],['kneten','2 · Joghurt, Wasser, Milch, Öl unterkneten'],['warm','3 · ca. 60 Min. warm gehen',{t:'60 Min.'}],['teilen','4 · Rolle: 11 Schnitte = 12 Stück',{n:6,t:'12 Stück'}],['kerne','5 · Befeuchten, Körner aufstreuen',{t:'Hafer · Chia'}],['teilen','6 · Abgedeckt 20 Min. gehen',{n:6,t:'20 Min.'}],['ofen','7 · 200 °C O/U, 35 Min.',{t:'200 °C'}]]); },
