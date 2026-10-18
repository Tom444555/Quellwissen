    ak_tafel(rows,titel,sd){ seed=sd; const M=['Jan','Feb','Mär','Apr','Mai','Jun','Jul','Aug','Sep','Okt','Nov','Dez'];
      const X0=178, CW=52, Y0=58, RH=27, H=Y0+rows.length*RH+56, jetzt=new Date().getMonth();
      let g=`<text x="10" y="34" style="fill:#3f7a3a;font:800 22px var(--label)">${titel}</text>`;
      for(let m=0;m<12;m++){ const x=X0+m*CW;
        g+=`<rect x="${x}" y="${Y0-4}" width="${CW}" height="${rows.length*RH+4}" fill="${m%2?'#efe6d6':'#f8f3ea'}" opacity=".75"/>`;
        const heute=m===jetzt;
        g+=`<path d="M${x+5},${Y0-30} h${CW-10} a4,4 0 0 1 4,4 v14 a4,4 0 0 1 -4,4 h-${(CW-10)/2-6} l-6,6 l-6,-6 h-${(CW-10)/2-6} a4,4 0 0 1 -4,-4 v-14 a4,4 0 0 1 4,-4 z" fill="${heute?lg('#e0a040','#b8701a',90):lg('#c8a47a','#9a7650',90)}" stroke="${heute?'#8a5010':'#7a5a38'}" stroke-width="1"/>`;
        g+=`<text x="${x+CW/2}" y="${Y0-15}" style="fill:#fff8ec;font:800 11.5px var(--label);text-anchor:middle">${M[m]}</text>`; }
      g+=`<rect x="${X0+jetzt*CW+1}" y="${Y0-4}" width="${CW-2}" height="${rows.length*RH+4}" fill="none" stroke="#d08a2a" stroke-width="2" stroke-dasharray="5 3" rx="3"><animate attributeName="stroke-dashoffset" values="0;16" dur="2s" repeatCount="indefinite"/></rect>`;
      g+=`<text x="${X0+jetzt*CW+CW/2}" y="${Y0+rows.length*RH+16}" style="fill:#b8701a;font:800 11px var(--label);text-anchor:middle">▲ jetzt</text>`;
      g+=`<text x="${X0+12*CW+46}" y="${Y0-14}" style="fill:var(--muted);font:700 11px var(--label);text-anchor:middle">Saattiefe</text>`;
      const bar=(von,bis,y,h,c0,c1,del,tip)=>{ const x=X0+(von-1)*CW+2, w=(bis-von+1)*CW-4;
        return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${h/2}" fill="${lg(c0,c1,90)}" stroke="${shade(c1,-0.35)}" stroke-width=".7"><title>${tip}</title><animate attributeName="width" values="0;${w}" dur=".7s" begin="${del}s" fill="freeze" calcMode="spline" keySplines=".2 .8 .3 1"/></rect>`; };
      rows.forEach(([name,tiefe,aus,ern],i)=>{ const y=Y0+i*RH;
        g+=`<path d="M6,${y+RH} H${X0+12*CW+96}" stroke="#d8ccb8" stroke-width=".8"/>`;
        g+=`<text x="12" y="${y+RH/2+4.5}" style="fill:var(--ink);font:600 13px var(--label)">${name}</text>`;
        const mon=l=>l.map(([a,b])=>a===b?M[a-1]:M[a-1]+'–'+M[b-1]).join(', ');
        aus.forEach(([a,b])=>g+=bar(a,b,y+4,9,'#d4ec7a','#9cc83a',0.1+i*0.03,name+' · Aussaat: '+mon(aus)));
        ern.forEach(([a,b])=>g+=bar(a,b,y+14,9,'#5cae6a','#2e7e44',0.4+i*0.03,name+' · Ernte: '+mon(ern)));
        // Saattiefe mit kleinem Bodenschnitt
        const tx=X0+12*CW+10, cm=parseFloat(String(tiefe).replace(',','.'))||0, licht=/andr/.test(tiefe);
        g+=`<rect x="${tx}" y="${y+9}" width="16" height="15" rx="2" fill="${lg('#a88058','#6e4e30',90)}"/><path d="M${tx},${y+9} h16" stroke="#5a7a2a" stroke-width="1.6"/>`;
        g+=`<ellipse cx="${tx+8}" cy="${licht?y+8:R(y+10+Math.min(cm,5)*2.4)}" rx="2.4" ry="1.8" fill="#f2dca0" stroke="#7a5a20" stroke-width=".6"/>`;
        if(licht) g+=`<g stroke="#e8b030" stroke-width="1"><path d="M${tx+8},${y+1} v3 M${tx+2},${y+3} l2,2 M${tx+14},${y+3} l-2,2"/></g>`;
        g+=`<text x="${tx+22}" y="${y+RH/2+4.5}" style="fill:var(--ink);font:700 12px var(--label)">${tiefe}</text>`; });
      const ly=Y0+rows.length*RH+36;
      g+=`<rect x="12" y="${ly-10}" width="34" height="10" rx="5" fill="${lg('#d4ec7a','#9cc83a',90)}"/><text x="54" y="${ly}" style="fill:var(--ink);font:700 12px var(--label)">Aussaat (vorziehen oder direkt)</text>`;
      g+=`<rect x="290" y="${ly-10}" width="34" height="10" rx="5" fill="${lg('#5cae6a','#2e7e44',90)}"/><text x="332" y="${ly}" style="fill:var(--ink);font:700 12px var(--label)">Ernte</text>`;
      g+=`<path d="M410,${ly-9} l4,4 M418,${ly-11} v4 M426,${ly-9} l-4,4" stroke="#e8b030" stroke-width="1.2"/><text x="434" y="${ly}" style="fill:var(--ink);font:700 12px var(--label)">Lichtkeimer: nur andrücken</text>`;
      g+=`<text x="${X0+12*CW+96}" y="${ly}" style="fill:var(--muted);font:600 10.5px var(--label);text-anchor:end">nach Gartencenter.de · Mitteleuropa</text>`;
      return {vb:`0 0 ${X0+12*CW+100} ${H}`, breit:true, leg:[], svg:g}; },
    aussaat_gemuese(){ return Z.ak_tafel([
      ['Blumenkohl','1 cm',[[3,5]],[[6,10]]],['Brokkoli','0,5–1 cm',[[3,3],[6,6]],[[1,3],[10,12]]],['Feldsalat','1–2 cm',[[3,9]],[[4,12]]],
      ['Fenchel','0,5–1 cm',[[4,4],[6,6]],[[6,6],[9,9]]],['Grünkohl','1 cm',[[7,7]],[[8,12]]],['Gurken','2–3 cm',[[5,6]],[[7,9]]],
      ['Karotten','2 cm',[[3,4],[6,7]],[[8,11]]],['Kohlrabi','1 cm',[[3,6]],[[6,10]]],['Kopfsalat','1 cm',[[3,7]],[[5,10]]],
      ['Kürbis / Zucchini','2,5 cm',[[5,6]],[[7,10]]],['Lauchzwiebel','1–2 cm',[[3,3]],[[10,12]]],['Mangold','2–3 cm',[[3,11]],[[5,11]]],
      ['Mark- u. Zuckererbsen','3–5 cm',[[3,6]],[[6,9]]],['Melone','1,5–2 cm',[[6,6]],[[8,10]]],['Paprika','1 cm',[[2,4]],[[8,10]]],
      ['Pastinake','1–2 cm',[[4,4]],[[10,12]]],['Porree','2–3 cm',[[3,5]],[[1,2],[9,12]]],['Puffbohnen','4–6 cm',[[2,4]],[[6,7]]],
      ['Radieschen','0,5–1 cm',[[4,9]],[[4,11]]],['Rosenkohl','0,5–1 cm',[[5,6]],[[9,12]]],['Rot-/Weiß-/Wirsingkohl','1 cm',[[3,5]],[[9,11]]],
      ['Sellerie','andrücken',[[4,5]],[[9,10]]],['Spinat','1–2 cm',[[2,5],[7,10]],[[4,7],[9,10]]],['Steckrübe','1–2 cm',[[4,6]],[[10,12]]],
      ['Tomate','0,5 cm',[[1,4]],[[7,10]]],['Zwiebeln','1–2 cm',[[3,4],[8,9]],[[6,7],[9,10]]]],'Gemüse',501); },
    aussaat_kraeuter(){ return Z.ak_tafel([
      ['Basilikum','andrücken',[[3,7]],[[7,9]]],['Blattkoriander','1 cm',[[4,6]],[[7,10]]],['Bohnenkraut','andrücken',[[4,6]],[[6,11]]],
      ['Dill','andrücken',[[5,7]],[[7,10]]],['Lavendel','0,5 cm',[[5,6]],[[7,8]]],['Liebstöckel','0,5 cm',[[3,5]],[[5,10]]],
      ['Majoran','0,5 cm',[[5,5]],[[7,10]]],['Petersilie','0,5–1 cm',[[3,8]],[[5,12]]],['Rosmarin','0,5 cm',[[2,4]],[[5,10]]],
      ['Rucola','0,5 cm',[[3,9]],[[4,10]]],['Schnittlauch','2 cm',[[4,7]],[[7,11]]],['Thymian','0,5 cm',[[5,6]],[[7,9]]]],'Kräuter',502); },
    keimung_chemie(){ seed=503; let g='';
      // Korn im Schnitt (Getreidemodell)
      g+=`<text x="190" y="22" style="fill:var(--ink);font:800 13px var(--label);text-anchor:middle">Was im quellenden Samen passiert</text>`;
      g+=`<path d="M60,140 Q50,60 170,48 Q300,40 330,130 Q340,215 190,222 Q70,226 60,140 Z" fill="${lg('#c89a50','#8a6028',90)}" stroke="#5a3a14" stroke-width="2"/>`;
      g+=`<path d="M74,140 Q66,72 172,62 Q290,56 316,132 Q324,204 190,208 Q84,212 74,140 Z" fill="${lg('#e6c87a','#c8a04a',90)}" stroke="#a87a2a" stroke-width="1"/>`;
      g+=`<path d="M84,140 Q78,82 174,74 Q280,70 304,134 Q310,194 190,196 Q94,198 84,140 Z" fill="${lg('#fbf3dc','#eedcae',90)}" stroke="#d8c08a"/>`;
      for(let i=0;i<46;i++){ const a=rnd()*Math.PI*2, r=Math.sqrt(rnd()); const x=R(200+Math.cos(a)*r*90), y=R(136+Math.sin(a)*r*50); g+=`<circle cx="${x}" cy="${y}" r="${R(2.4+rnd()*2.6)}" fill="#f6ecd0" stroke="#d2b880" stroke-width=".7"><animate attributeName="r" values="${R(2.6+rnd()*2)};.6" dur="7s" begin="${R(rnd()*2)}s" repeatCount="indefinite"/></circle>`; }
      g+=`<path d="M84,118 Q66,140 82,168 Q104,190 122,164 Q132,140 114,118 Q100,104 84,118 Z" fill="${lg('#e8e8a0','#a8c050',90)}" stroke="#6a8a2a" stroke-width="1.4"/>`;
      g+=`<path d="M100,132 q-6,10 0,22" stroke="#5a7a2a" stroke-width="2.2" fill="none"/>`;
      // Keimwurzel waechst heraus
      g+=`<path d="M84,160 Q70,186 52,206" stroke="#f2eccc" stroke-width="5" fill="none" stroke-linecap="round" stroke-dasharray="70" stroke-dashoffset="70"><animate attributeName="stroke-dashoffset" values="70;0;0;70" keyTimes="0;.5;.9;1" dur="7s" repeatCount="indefinite"/></path>`;
      // Wasser
      for(let i=0;i<6;i++){ const y=60+i*26; g+=`<path d="M352,${y} q-4,-7 0,-12 q4,5 0,12 z" fill="#5aa0d8" opacity="0"><animate attributeName="opacity" values="0;1;0" dur="3s" begin="${i*0.5}s" repeatCount="indefinite"/><animateTransform attributeName="transform" type="translate" values="0 0;-50 0" dur="3s" begin="${i*0.5}s" repeatCount="indefinite"/></path>`; }
      // GA-Pfeile Embryo -> Aleuron
      g+=`<path d="M124,128 Q170,92 236,70" stroke="#c03070" stroke-width="2.2" fill="none" stroke-dasharray="5 4"><animate attributeName="stroke-dashoffset" values="18;0" dur="1s" repeatCount="indefinite"/></path><text x="158" y="94" style="paint-order:stroke;stroke:#fffaf0;stroke-width:3px;fill:#c03070;font:800 11px var(--label)">GA</text>`;
      // Amylase -> Zucker -> Embryo
      g+=`<path d="M280,92 Q250,120 230,130" stroke="#3a7ab0" stroke-width="2.2" fill="none" marker-end=""/><text x="236" y="110" style="paint-order:stroke;stroke:#fffaf0;stroke-width:3px;fill:#3a7ab0;font:800 10.5px var(--label)">α-Amylase</text>`;
      g+=`<path d="M200,150 Q160,160 126,150" stroke="#b07a10" stroke-width="2.4" fill="none" stroke-dasharray="4 4"><animate attributeName="stroke-dashoffset" values="0;16" dur="1s" repeatCount="indefinite"/></path><text x="146" y="176" style="paint-order:stroke;stroke:#fffaf0;stroke-width:3px;fill:#b07a10;font:800 10.5px var(--label)">Zucker</text>`;
      g+=mk(352,40,1)+mk(100,104,2)+mk(250,56,3)+mk(222,158,4)+mk(40,206,5);
      // Waage ABA / GA
      g+=`<text x="520" y="22" style="fill:var(--ink);font:800 13px var(--label);text-anchor:middle">Bremse und Gaspedal</text>`;
      g+=`<path d="M520,190 l-16,26 h32 z" fill="${lg('#a8a8a0','#6a6a64',90)}"/>`;
      g+=`<g><path d="M430,190 H610" stroke="#5a5a54" stroke-width="5" stroke-linecap="round"/>`+
        `<rect x="420" y="146" width="62" height="40" rx="8" fill="${lg('#f0b0a0','#c0604a',90)}" stroke="#8a3a2a"/><text x="451" y="171" style="fill:#fff;font:800 14px var(--label);text-anchor:middle">ABA</text>`+
        `<rect x="558" y="146" width="62" height="40" rx="8" fill="${lg('#b8e090','#5a9a3a',90)}" stroke="#2e6a1e"/><text x="589" y="171" style="fill:#fff;font:800 14px var(--label);text-anchor:middle">GA</text>`+
        `<animateTransform attributeName="transform" type="rotate" values="-9 520 190;-9 520 190;9 520 190;9 520 190;-9 520 190" keyTimes="0;.3;.5;.8;1" dur="8s" repeatCount="indefinite"/></g>`;
      g+=`<text x="451" y="236" style="fill:#8a3a2a;font:700 11px var(--label);text-anchor:middle">Keimruhe</text><text x="589" y="236" style="fill:#2e6a1e;font:700 11px var(--label);text-anchor:middle">Keimung</text>`;
      g+=`<text x="520" y="64" style="fill:var(--muted);font:600 11px var(--label);text-anchor:middle">Kälte, Licht, Zeit, Auswaschen</text><text x="520" y="80" style="fill:var(--muted);font:600 11px var(--label);text-anchor:middle">senken ABA – heben GA</text>`;
      return {vb:'0 0 640 250', breit:true, leg:['Quellung: Der trockene Same (5–15 % Wasser) saugt Wasser auf, Zellen und Enzyme werden wieder aktiv, die Atmung springt an','Der Embryo bildet das Hormon Gibberellin (GA) und schickt es zur Aleuronschicht','Die Aleuronschicht bildet Enzyme, vor allem α-Amylase','Die Amylase spaltet Stärke in Malzzucker und Traubenzucker – Energie und Baustoff für den Keimling','Die Keimwurzel durchbricht die Samenschale – meist zuerst, damit Wasser gesichert ist'], svg:g}; },
    saattiefe_regel(){ seed=504; let g='';
      g+=`<rect x="0" y="70" width="440" height="160" fill="${lg('#b08a60','#6a4a2a',90)}" opacity=".85"/>`;
      for(let i=0;i<70;i++) g+=`<ellipse cx="${R(rnd()*440)}" cy="${R(74+rnd()*152)}" rx="${R(1+rnd()*2.4)}" ry="${R(.8+rnd()*1.6)}" fill="${rnd()<.5?'#5a3a1a':'#c8a878'}" opacity=".6"/>`;
      g+=`<path d="M0,70 H440" stroke="#4a6a2a" stroke-width="3"/>`;
      g+=`<path d="M22,70 V226" stroke="#fff" stroke-width="1.2"/>`; for(let c=0;c<=6;c++) g+=`<path d="M18,${70+c*24} h8" stroke="#fff"/><text x="30" y="${74+c*24}" style="fill:#fff;font:700 10px var(--label)">${c} cm</text>`;
      const keim=(x,y,len,o)=>`<path d="M${x},${y} Q${x+4},${(y+70)/2} ${x},${70-len}" stroke="#7aa040" stroke-width="2" fill="none" stroke-dasharray="${200}" stroke-dashoffset="200"><animate attributeName="stroke-dashoffset" values="200;0;0" keyTimes="0;.6;1" dur="6s" begin="${o}s" repeatCount="indefinite"/></path>`;
      const sam=[[110,'Basilikum','Licht: auflegen',0,2,'#3a2a1a'],[200,'Möhre','1–2 cm',36,2.4,'#8a6a3a'],[290,'Erbse','3–5 cm',96,6,'#c8c070'],[380,'Puffbohne','4–6 cm',120,10,'#a88a5a']];
      sam.forEach(([x,n,t,d,r,c],i)=>{ const y=d?70+d:68;
        g+=keim(x,y,22+i*4,i*0.4);
        g+=`<ellipse cx="${x}" cy="${y}" rx="${r*1.4}" ry="${r}" fill="${lg(shade(c,.3),shade(c,-.3),90)}" stroke="${shade(c,-.5)}"/>`;
        g+=`<text x="${x}" y="22" style="fill:var(--ink);font:800 12px var(--label);text-anchor:middle">${n}</text><text x="${x}" y="38" style="fill:var(--muted);font:600 10.5px var(--label);text-anchor:middle">${t}</text>`; });
      g+=`<g stroke="#e8b030" stroke-width="1.6"><path d="M110,46 v8 M98,50 l5,5 M122,50 l-5,5"/></g>`;
      g+=`<text x="300" y="218" style="fill:#fff;font:700 11px var(--label);text-anchor:middle">Faustregel: 2–3 × so tief wie der Same dick ist</text>`;
      // Phytochrom
      g+=`<text x="560" y="22" style="fill:var(--ink);font:800 13px var(--label);text-anchor:middle">Phytochrom – der Lichtschalter</text>`;
      g+=`<rect x="478" y="96" width="70" height="44" rx="10" fill="${lg('#f8e0a0','#d0a040',90)}" stroke="#8a6010"/><text x="513" y="123" style="fill:#5a3a00;font:800 15px var(--label);text-anchor:middle">Pr</text>`;
      g+=`<rect x="574" y="96" width="70" height="44" rx="10" fill="${lg('#c8e8a0','#5a9a3a',90)}" stroke="#2e6a1e"/><text x="609" y="123" style="fill:#fff;font:800 15px var(--label);text-anchor:middle">Pfr</text>`;
      g+=`<path d="M520,92 Q561,58 602,92" stroke="#d03020" stroke-width="3" fill="none"/><path d="M602,92 l-10,-2 l6,-8 z" fill="#d03020"/><text x="561" y="62" style="fill:#d03020;font:800 11px var(--label);text-anchor:middle">Hellrot 660 nm</text>`;
      g+=`<path d="M602,144 Q561,178 520,144" stroke="#7a1a3a" stroke-width="3" fill="none"/><path d="M520,144 l10,2 l-6,8 z" fill="#7a1a3a"/><text x="561" y="190" style="fill:#7a1a3a;font:800 11px var(--label);text-anchor:middle">Dunkelrot 730 nm / Dunkel</text>`;
      g+=`<circle cx="609" cy="118" r="30" fill="none" stroke="#9ad060" stroke-width="2" opacity="0"><animate attributeName="opacity" values="0;.9;0" dur="3s" repeatCount="indefinite"/><animate attributeName="r" values="26;40" dur="3s" repeatCount="indefinite"/></circle>`;
      g+=`<text x="561" y="216" style="fill:var(--muted);font:600 11px var(--label);text-anchor:middle">Pfr = aktiv: schaltet bei Lichtkeimern</text><text x="561" y="231" style="fill:var(--muted);font:600 11px var(--label);text-anchor:middle">die Keimung (über mehr GA) frei</text>`;
      return {vb:'0 0 660 240', breit:true, leg:[], svg:g}; },
    anzucht_ablauf(){ seed=505; let g=`<path d="M150,10 V200 M300,10 V200 M450,10 V200 M600,10 V200 M750,10 V200" stroke="var(--line)" stroke-width="1"/>`;
      const schale=(x,y,w)=>`<path d="M${x-w/2},${y} L${x-w/2+8},${y+34} H${x+w/2-8} L${x+w/2},${y} Z" fill="${lg('#7a8a9a','#4a5664',90)}" stroke="#2e3640"/><path d="M${x-w/2+3},${y+4} H${x+w/2-3}" stroke="#5a3e24" stroke-width="7"/>`;
      const sml=(x,y,h,s=1,c='#7ab040')=>`<path d="M${x},${y} q2,${-h/2} 0,${-h}" stroke="${shade(c,-.2)}" stroke-width="${1.6*s}" fill="none"/>`+blatt(x,y-h,7*s,3*s,-150,{fill:c,adern:false})+blatt(x,y-h,7*s,3*s,-30,{fill:c,adern:false});
      g+=vign(0,'1 · Anzuchterde, nährstoffarm',schale(75,130,110)+`<path d="M40,60 l14,50 h42 l14,-50 z" fill="${lg('#f0e8d0','#c8b890',90)}" stroke="#8a7a50"/><text x="75" y="84" style="fill:#5a4a2a;font:800 11px var(--label);text-anchor:middle">Anzucht-</text><text x="75" y="97" style="fill:#5a4a2a;font:800 11px var(--label);text-anchor:middle">erde</text>`+[0,1,2,3,4].map(i=>`<circle cx="${60+i*7}" cy="114" r="2" fill="#5a3e24"><animate attributeName="cy" values="112;132" dur="1.4s" begin="${i*0.25}s" repeatCount="indefinite"/></circle>`).join(''));
      g+=vign(1,'2 · Säen, leicht andrücken',schale(75,130,110)+[46,62,78,94,110].map(x=>`<ellipse cx="${x}" cy="131" rx="2.6" ry="1.8" fill="#e8d090" stroke="#7a5a20" stroke-width=".6"/>`).join('')+`<rect x="40" y="96" width="70" height="12" rx="3" fill="${lg('#d8b888','#9a7a4a',90)}" stroke="#6a4a2a"><animateTransform attributeName="transform" type="translate" values="0 0;0 18;0 0" dur="2.4s" repeatCount="indefinite"/></rect>`);
      g+=vign(2,'3 · Feucht halten, nicht nass',schale(75,140,110)+`<path d="M24,140 Q24,70 75,66 Q126,70 126,140" fill="#dff0ff" opacity=".35" stroke="#9ab8d0"/><path d="M100,40 h22 v14 h-22 z M104,40 v-8 h8" fill="${lg('#a8d0f0','#5a8ab0',0)}" stroke="#3a5a7a"/>`+[0,1,2,3].map(i=>`<circle cx="${96-i*6}" cy="${60+i*8}" r="1.6" fill="#5aa0d8" opacity="0"><animate attributeName="opacity" values="0;1;0" dur="1.6s" begin="${i*0.2}s" repeatCount="indefinite"/></circle>`).join('')+`<text x="40" y="190" style="fill:var(--muted);font:700 11px var(--label)">Haube lüften</text>`);
      let k=''; [46,62,78,94,110].forEach((x,i)=>k+=`<g transform="translate(0,0)">${sml(x,134,18)}<animateTransform attributeName="transform" type="translate" values="0 18;0 0" dur="2s" begin="${i*0.15}s" fill="freeze"/></g>`);
      g+=vign(3,'4 · Gekeimt: hell und kühler',schale(75,134,110)+k+`<circle cx="120" cy="40" r="12" fill="${lg('#ffe080','#f0a020',90)}"/><text x="30" y="56" style="fill:#3a6a9a;font:800 12px var(--label)">16–18 °C</text>`);
      g+=vign(4,'5 · Pikieren beim ersten echten Blatt',`<rect x="22" y="128" width="40" height="40" rx="4" fill="${lg('#c86a3a','#8a3a1a',90)}"/><rect x="88" y="128" width="40" height="40" rx="4" fill="${lg('#c86a3a','#8a3a1a',90)}"/>`+sml(42,130,22,1.2)+`<g>${sml(108,90,24,1.2)}<path d="M108,92 v14" stroke="#e8e0d0" stroke-width="2.4"/><animateTransform attributeName="transform" type="translate" values="0 0;0 38;0 38;0 0" keyTimes="0;.4;.8;1" dur="3s" repeatCount="indefinite"/></g><path d="M130,40 L110,92" stroke="#c8a060" stroke-width="3" stroke-linecap="round"/>`);
      g+=vign(5,'6 · Abhärten: 1–2 Wochen stundenweise raus',`<circle cx="40" cy="44" r="14" fill="${lg('#ffe080','#f0a020',90)}"><animate attributeName="r" values="12;15;12" dur="3s" repeatCount="indefinite"/></circle><path d="M80,50 q6,-16 22,-10 q10,-12 22,0 q12,2 6,14 h-48 z" fill="#eef2f6" stroke="#aab4be"/><rect x="50" y="140" width="50" height="30" rx="4" fill="${lg('#c86a3a','#8a3a1a',90)}"/>`+`<g>${sml(75,142,42,1.8,'#5a9a34')}<animateTransform attributeName="transform" type="rotate" values="-4 75 142;5 75 142;-4 75 142" dur="2.6s" repeatCount="indefinite"/></g>`);
      return {vb:'0 0 900 230', breit:true, leg:[], svg:g}; },
    saemling_fehler(){ seed=506; let g=`<path d="M180,10 V210 M360,10 V210" stroke="var(--line)"/>`;
      const topf=x=>`<rect x="${x-30}" y="160" width="60" height="40" rx="4" fill="${lg('#c86a3a','#8a3a1a',90)}"/><path d="M${x-30},162 h60" stroke="#5a3e24" stroke-width="5"/>`;
      // kraeftig
      g+=topf(90)+stiel('M90,160 q2,-30 0,-60',3,'#4a8a2a')+blatt(90,100,26,9,-160,{fill:'#4a8a30'})+blatt(90,100,26,9,-20,{fill:'#4a8a30'})+blatt(90,124,18,7,-150,{fill:'#5a9a3a',adern:false})+blatt(90,124,18,7,-30,{fill:'#5a9a3a',adern:false});
      g+=`<text x="90" y="24" style="fill:#2e6a1e;font:800 13px var(--label);text-anchor:middle">✓ kompakt</text><text x="90" y="40" style="fill:var(--muted);font:600 11px var(--label);text-anchor:middle">hell, kühl, sparsam gießen</text>`;
      // vergeilt
      g+=topf(270)+`<g>`+stiel('M270,160 q10,-56 -4,-100',1.4,'#a8c870')+blatt(266,60,14,4,-160,{fill:'#b8d080',adern:false})+blatt(266,60,14,4,-10,{fill:'#b8d080',adern:false})+`<animateTransform attributeName="transform" type="rotate" values="0 270 160;8 270 160;0 270 160" dur="3s" repeatCount="indefinite"/></g><text x="270" y="24" style="fill:#a05a10;font:800 13px var(--label);text-anchor:middle">✗ vergeilt</text><text x="270" y="40" style="fill:var(--muted);font:600 11px var(--label);text-anchor:middle">zu warm, zu dunkel</text>`;
      g+=`<text x="270" y="190" style="fill:#fff;font:800 11px var(--label);text-anchor:middle">22 °C+</text>`;
      // Umfallkrankheit
      g+=topf(450)+stiel('M436,160 q0,-24 -2,-40',2,'#6a9a3a')+blatt(434,120,16,6,-160,{fill:'#5a9a3a',adern:false})+blatt(434,120,16,6,-20,{fill:'#5a9a3a',adern:false});
      g+=`<path d="M462,158 q6,-4 30,-6" stroke="#8a9a5a" stroke-width="2" fill="none"/><ellipse cx="462" cy="157" rx="4" ry="2.4" fill="#5a3a1a"/>`+blatt(492,152,14,5,-10,{fill:'#9aa86a',adern:false});
      for(let i=0;i<14;i++) g+=`<path d="M${R(424+rnd()*60)},160 l${R((rnd()-.5)*8)},-${R(3+rnd()*5)}" stroke="#f4f4f0" stroke-width=".7" opacity=".9"/>`;
      g+=`<text x="450" y="24" style="fill:#8a2a1a;font:800 13px var(--label);text-anchor:middle">✗ Umfallkrankheit</text><text x="450" y="40" style="fill:var(--muted);font:600 11px var(--label);text-anchor:middle">Pilze bei Nässe und Enge</text>`;
      return {vb:'0 0 540 230', breit:true, leg:[], svg:g}; },
