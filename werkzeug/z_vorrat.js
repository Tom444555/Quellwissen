    vorrat_bild(){ seed=2611; let g='';
      const T=(x,y,t,c='var(--muted)',s=11,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      // Regal: zwei Seitenwangen, drei Böden
      const X0=30, X1=560, B=[96,176,256];
      g+=`<rect x="${X0-14}" y="18" width="14" height="262" rx="3" fill="${lg('#b88a58','#7a5230',0)}" stroke="#4e3218" stroke-width="1.1"/>`;
      g+=`<rect x="${X1}" y="18" width="14" height="262" rx="3" fill="${lg('#b88a58','#7a5230',0)}" stroke="#4e3218" stroke-width="1.1"/>`;
      g+=`<rect x="${X0}" y="18" width="${X1-X0}" height="250" fill="#f3ead8" opacity=".35"/>`;
      for(const y of B){ g+=`<rect x="${X0-14}" y="${y}" width="${X1-X0+28}" height="11" rx="2" fill="${lg('#c89a64','#8a5e34',90)}" stroke="#5a3a1c" stroke-width="1"/>`;
        g+=`<path d="M${X0},${y+4} q${(X1-X0)/2},${R(rnd()*3-1.5)} ${X1-X0},0" stroke="#7a5028" stroke-width=".7" fill="none" opacity=".5"/>`; }
      // oberes Fach: Gläser und Dosen
      const glas=(x,w,h,inh,deckel)=>{ const y=B[0]; let s=`<rect x="${x}" y="${y-h}" width="${w}" height="${h}" rx="6" fill="${lg('#eef3f1','#c4d0cc',0)}" stroke="#7d8a86" stroke-width="1"/>`;
        s+=`<rect x="${x+3}" y="${y-h+12}" width="${w-6}" height="${h-15}" rx="4" fill="${inh}"/>`;
        s+=`<rect x="${x-1}" y="${y-h-7}" width="${w+2}" height="9" rx="2" fill="${deckel}" stroke="${shade(deckel,-0.4)}" stroke-width=".8"/>`;
        s+=`<rect x="${x+5}" y="${y-h+16}" width="4" height="${h-26}" rx="2" fill="#ffffff" opacity=".35"/>`; return s; };
      const dose=(x,w,h,band,y0)=>{ const y=y0||B[0]; let s=`<rect x="${x}" y="${y-h}" width="${w}" height="${h}" rx="3" fill="${lg('#d8dce0','#8a9096',0)}" stroke="#555b62" stroke-width="1"/>`;
        s+=`<rect x="${x}" y="${y-h*0.72}" width="${w}" height="${h*0.48}" fill="${band}"/>`;
        s+=`<ellipse cx="${x+w/2}" cy="${y-h}" rx="${w/2}" ry="3" fill="#c8ccd0" stroke="#555b62" stroke-width=".8"/>`;
        for(let i=1;i<4;i++) s+=`<path d="M${x},${R(y-h+i*3)} H${x+w}" stroke="#6a7078" stroke-width=".4" opacity=".5"/>`; return s; };
      g+=glas(44,40,58,'#8a2f5a','#c0392b')+glas(90,40,58,'#7a8a2a','#d4a017')+glas(136,40,50,'#b0202e','#c0392b');
      g+=dose(190,38,52,'#d98c2b')+dose(232,38,52,'#4f8a3c')+dose(274,38,52,'#c84b3a');
      g+=dose(320,48,30,'#3a6ea5')+`<rect x="320" y="${B[0]-60}" width="48" height="28" rx="3" fill="${lg('#d8dce0','#8a9096',0)}" stroke="#555b62" stroke-width="1"/><rect x="320" y="${B[0]-52}" width="48" height="12" fill="#3a6ea5"/>`;
      g+=glas(380,46,66,'#e3b23c','#7a5634')+glas(432,38,46,'#b85d0f','#7a5634');
      g+=`<rect x="478" y="${B[0]-74}" width="66" height="74" rx="4" fill="${lg('#e8d7a8','#b89a5a',0)}" stroke="#7a6230" stroke-width="1"/><rect x="484" y="${B[0]-62}" width="54" height="24" rx="3" fill="#c0392b" opacity=".85"/>`;
      // mittleres Fach: Säcke, Packungen, Knäckebrot
      const sack=(x,w,h,f,band)=>{ const y=B[1]; let s=`<path d="M${x},${y} L${x+3},${y-h+12} Q${x+w/2},${y-h-6} ${x+w-3},${y-h+12} L${x+w},${y} Z" fill="${lg(shade(f,0.15),shade(f,-0.2),0)}" stroke="${shade(f,-0.45)}" stroke-width="1"/>`;
        s+=`<path d="M${x+6},${y-h+14} Q${x+w/2},${y-h+4} ${x+w-6},${y-h+14}" stroke="${shade(f,-0.4)}" stroke-width="1.1" fill="none"/>`;
        if(band) s+=`<rect x="${x+8}" y="${y-h*0.55}" width="${w-16}" height="${h*0.28}" rx="3" fill="${band}" opacity=".85"/>`; return s; };
      g+=sack(44,56,62,'#efe6cf','#b7472a')+sack(106,50,56,'#f4f1e6','#3a6ea5')+sack(162,52,60,'#e9dcc0','#4f8a3c');
      g+=`<rect x="222" y="${B[1]-58}" width="34" height="58" rx="2" fill="${lg('#2f6aa8','#1f4a78',0)}" stroke="#163556" stroke-width="1"/><rect x="226" y="${B[1]-46}" width="26" height="18" rx="2" fill="#f4c430"/>`;
      g+=`<rect x="260" y="${B[1]-58}" width="34" height="58" rx="2" fill="${lg('#c0392b','#8e241a',0)}" stroke="#5e160f" stroke-width="1"/><rect x="264" y="${B[1]-46}" width="26" height="18" rx="2" fill="#f6f3e7"/>`;
      for(let i=0;i<4;i++) g+=`<rect x="${302+i*3}" y="${B[1]-40+i*2}" width="76" height="${40-i*2}" rx="2" fill="${lg('#e8c98a','#b98f4a',90)}" stroke="#7a5a26" stroke-width=".8"/>`;
      for(let i=0;i<14;i++) g+=`<circle cx="${R(312+rnd()*60)}" cy="${R(B[1]-30+rnd()*24)}" r="1.1" fill="#7a5a26" opacity=".6"/>`;
      g+=`<rect x="392" y="${B[1]-52}" width="44" height="52" rx="3" fill="${lg('#f0e6c8','#c8b47e',0)}" stroke="#8a7440" stroke-width="1"/><path d="M398,${B[1]-30} h32" stroke="#8a7440" stroke-width="3"/>`;
      // Kerzen, Streichhölzer, Taschenlampe
      g+=`<rect x="450" y="${B[1]-44}" width="12" height="44" rx="2" fill="#fbf6e6" stroke="#b8ae90" stroke-width="1"/><rect x="466" y="${B[1]-36}" width="12" height="36" rx="2" fill="#fbf6e6" stroke="#b8ae90" stroke-width="1"/>`;
      g+=`<path d="M456,${B[1]-44} v-6" stroke="#333" stroke-width="1"/><path d="M472,${B[1]-36} v-6" stroke="#333" stroke-width="1"/>`;
      g+=`<rect x="486" y="${B[1]-18}" width="64" height="18" rx="7" fill="${lg('#4a4f57','#24282e',90)}" stroke="#15181c" stroke-width="1"/><rect x="540" y="${B[1]-22}" width="12" height="26" rx="3" fill="#6b7078" stroke="#15181c" stroke-width="1"/>`;
      // unteres Fach: Wasserflaschen und Kanister
      const flasche=(x)=>{ const y=B[2]; let s=`<path d="M${x},${y} V${y-50} Q${x},${y-60} ${x+6},${y-64} V${y-72} H${x+14} V${y-64} Q${x+20},${y-60} ${x+20},${y-50} V${y} Z" fill="${lg('#e4f1f8','#9cc4dc',0)}" stroke="#5a86a0" stroke-width="1"/>`;
        s+=`<rect x="${x+6}" y="${y-76}" width="8" height="5" rx="1.5" fill="#2f7fb8"/><rect x="${x+1}" y="${y-38}" width="18" height="14" fill="#2f7fb8" opacity=".75"/>`;
        s+=`<rect x="${x+3}" y="${y-48}" width="3" height="40" rx="1.5" fill="#ffffff" opacity=".45"/>`; return s; };
      for(let i=0;i<6;i++) g+=flasche(44+i*24);
      g+=`<path d="M200,${B[2]} V${B[2]-62} Q200,${B[2]-70} 208,${B[2]-70} H262 Q270,${B[2]-70} 270,${B[2]-62} V${B[2]} Z" fill="${lg('#7fb0d6','#3f78a8',0)}" stroke="#244e70" stroke-width="1.1"/>`;
      g+=`<rect x="248" y="${B[2]-80}" width="14" height="12" rx="2" fill="#244e70"/><path d="M212,${B[2]-70} q8,-14 24,0" stroke="#244e70" stroke-width="4" fill="none"/>`;
      g+=`<rect x="206" y="${B[2]-46}" width="58" height="20" rx="3" fill="#f6f3e7" opacity=".7"/>`;
      // Gaskocher mit Kartusche, Topf
      g+=`<rect x="300" y="${B[2]-36}" width="58" height="36" rx="8" fill="${lg('#5a6068','#2c3036',90)}" stroke="#15181c" stroke-width="1"/><rect x="306" y="${B[2]-28}" width="22" height="14" rx="3" fill="#c0392b"/>`;
      g+=`<path d="M296,${B[2]-38} H362" stroke="#2c3036" stroke-width="4" stroke-linecap="round"/>`;
      g+=`<path d="M304,${B[2]-40} V${B[2]-68} Q304,${B[2]-72} 310,${B[2]-72} H348 Q354,${B[2]-72} 354,${B[2]-68} V${B[2]-40} Z" fill="${lg('#c8ccd0','#7a8088',0)}" stroke="#3a3e44" stroke-width="1.1"/>`;
      g+=`<path d="M298,${B[2]-72} H360" stroke="#3a3e44" stroke-width="3" stroke-linecap="round"/><path d="M322,${B[2]-76} h14" stroke="#3a3e44" stroke-width="3" stroke-linecap="round"/>`;
      g+=`<rect x="372" y="${B[2]-58}" width="30" height="58" rx="6" fill="${lg('#f08a24','#b85d0f',0)}" stroke="#7a3a08" stroke-width="1"/><rect x="380" y="${B[2]-66}" width="14" height="9" rx="2" fill="#7a8088"/>`;
      // Kurbelradio
      g+=`<rect x="418" y="${B[2]-46}" width="84" height="46" rx="6" fill="${lg('#e7d9b0','#b8a66e',90)}" stroke="#6e5e2c" stroke-width="1"/>`;
      for(let i=0;i<5;i++) g+=`<path d="M${426+i*7},${B[2]-36} v26" stroke="#6e5e2c" stroke-width="2"/>`;
      g+=`<circle cx="482" cy="${B[2]-23}" r="11" fill="${lg('#5a6068','#2c3036',90)}" stroke="#15181c" stroke-width="1"/><path d="M482,${B[2]-23} l14,-10" stroke="#15181c" stroke-width="2.4" stroke-linecap="round"/>`;
      g+=`<path d="M420,${B[2]-46} l22,-26" stroke="#6b7078" stroke-width="1.6"/>`;
      g+=`<rect x="512" y="${B[2]-26}" width="40" height="26" rx="4" fill="${lg('#3d8a5a','#245a38',0)}" stroke="#163a22" stroke-width="1"/><path d="M520,${B[2]-14} h24" stroke="#f6f3e7" stroke-width="2"/>`;
      // Boden
      g+=`<path d="M8,280 H582" stroke="#8a7a5a" stroke-width="1.2" opacity=".6"/>`;
      g+=T(295,300,'Das Ältere nach vorn, Neues nach hinten','var(--ink)',17,800);
      return {vb:'0 0 590 310',breit:true,leg:[],svg:g}; },
