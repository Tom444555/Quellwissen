    leiste_bierbrot(){ return Z.rezept_leiste([['schuessel','1 · Hefe + Zucker in lauwarmem Wasser',{zutaten:['#f0e0b0','#ffffff']}],['schuessel','2 · Mehl + Salz, Mulde, Hefewasser + Bier',{f:'#c8b090',zutaten:['#3a2010','#f0e0b0']}],['kneten','3 · 3–4 Min. elastisch kneten',{t:'3–4 Min.'}],['warm','4 · Mind. 60 Min. warm gehen',{t:'60 Min.',f:'#c8a87a'}],['ofen','5 · 240 °C Umluft, Wasserschale unten',{t:'240 °C'}],['ofen','6 · Einschneiden, 15 Min. 240 °C, 25 Min. 200 °C',{t:'200 °C'}]]); },
    leiste_dinkelbroetchen(){ return Z.rezept_leiste([['schuessel','1 · Mehl, Salz, Hefe vermengen',{zutaten:['#f4ecd8','#ffffff','#e8d8a0']}],['schuessel','2 · Wasser + Öl, nur kurz verrühren',{zutaten:['#9ac8e0','#d8c050']}],['warm','3 · 1 Std. bei Zimmertemperatur',{t:'1 Std.'}],['kalt','4 · 8–20 Std. Kühlschrank'],['teilen','5 · In 8 Stücke teilen – NICHT kneten',{n:8}],['ofen','6 · 230 °C O/U, 20–25 Min.',{t:'230 °C'}]]); },
    leiste_mohnkuchen(){ return Z.rezept_leiste([['schuessel','1 · Trockenes mischen',{zutaten:['#f4f0e8','#2a2a3a','#2a2a3a','#ffffff']}],['schuessel','2 · Eier, Milch, Öl verquirlen',{f:'#f0d880',zutaten:['#f8d040','#fbf6ea']}],['schuessel','3 · Zusammen kurz vermengen',{f:'#8a8a94'}],['kasten','4 · In die gefettete Form',{f:'#7a7a86'}],['ofen','5 · 180 °C, 30–35 Min.',{inhalt:'kasten',t:'180 °C'}],['gitter','6 · Stäbchenprobe, auskühlen',{f:'#6a6a74',t:'Stäbchenprobe'}]]); },
    banane_reife(){ seed=601; let g='';
      const ban=(x,y,c0,c1,fl,dun)=>{ let s=`<path d="M${x-48},${y-6} Q${x-20},${y+30} ${x+40},${y+4} Q${x+52},${y-4} ${x+50},${y-14} Q${x+40},${y-4} ${x+10},${y+4} Q${x-26},${y+8} ${x-44},${y-14} Z" fill="${lg(c0,c1,90)}" stroke="${shade(c1,-0.45)}" stroke-width="1.3"/>`;
        s+=`<path d="M${x+48},${y-12} l8,-10" stroke="#5a4a2a" stroke-width="4" stroke-linecap="round"/><path d="M${x-46},${y-10} l-4,-2" stroke="#2a1a0a" stroke-width="4" stroke-linecap="round"/>`;
        for(let i=0;i<fl;i++){ const t=rnd(); s+=`<ellipse cx="${R(x-40+t*84)}" cy="${R(y-2+Math.sin(t*Math.PI)*10+(rnd()-.5)*8)}" rx="${R(1+rnd()*2.4)}" ry="${R(1+rnd()*1.6)}" fill="${dun}" opacity=".85"/>`; } return s; };
      const B=[['grün','#a8c860','#6a9a30',0,'',78,8,'resistente Stärke'],['gelb','#f8e070','#e0b830',2,'#6a4a1a',40,46,'mild süß'],['fleckig','#f0d060','#c89a28',26,'#4a2a10',14,72,'sehr süß'],['schwarz','#5a4030','#2a1a10',8,'#1a0a00',6,80,'Backbanane']];
      B.forEach(([n,c0,c1,fl,dun,st,zu,note],i)=>{ const x=80+i*150;
        g+=ban(x,50,c0,c1,fl,dun);
        g+=`<text x="${x}" y="96" style="fill:var(--ink);font:800 13px var(--label);text-anchor:middle">${n}</text><text x="${x}" y="112" style="fill:var(--muted);font:600 11px var(--label);text-anchor:middle">${note}</text>`;
        const bar=(bx,h,c,lab)=>`<rect x="${bx}" y="${250-h*1.1}" width="26" height="${h*1.1}" rx="3" fill="${lg(shade(c,.2),shade(c,-.2),90)}"><animate attributeName="height" values="0;${h*1.1}" dur="1.2s" begin="${i*0.25}s" fill="freeze"/><animate attributeName="y" values="250;${250-h*1.1}" dur="1.2s" begin="${i*0.25}s" fill="freeze"/></rect><text x="${bx+13}" y="264" style="fill:var(--muted);font:700 10px var(--label);text-anchor:middle">${lab}</text>`;
        g+=bar(x-32,st,'#e8dcc0','Stärke')+bar(x+6,zu,'#e0a040','Zucker'); });
      g+=`<path d="M10,250 H610" stroke="var(--line)"/><text x="610" y="284" style="fill:var(--muted);font:600 10.5px var(--label);text-anchor:end">Anteile grob, in % der Trockenmasse [Ergänzung, Richtwerte]</text>`;
      g+=`<path d="M60,128 H560" stroke="#c8a040" stroke-width="2" stroke-dasharray="6 4"><animate attributeName="stroke-dashoffset" values="20;0" dur="1s" repeatCount="indefinite"/></path><path d="M560,128 l-10,-5 v10 z" fill="#c8a040"/><text x="310" y="146" style="fill:#a07a20;font:800 11px var(--label);text-anchor:middle">Ethylen + Amylasen: Stärke → Zucker</text>`;
      return {vb:'0 0 620 292', breit:true, leg:[], svg:g}; },
    magnesium_balken(){ seed=602; let g='';
      const D=[['Kürbiskerne','28 g',168],['Gekochter Spinat','180 g',158],['Quinoa (gekocht)','185 g',120],['Schwarze Bohnen (gekocht)','172 g',120],['Edamame','155 g',100],['Mandeln','28 g',80],['Cashewkerne','28 g',74],['Dunkle Schokolade','28 g',65],['Avocado','200 g',58]];
      const X0=236, S=1.2;
      g+=`<text x="10" y="20" style="fill:var(--ink);font:800 13px var(--label)">Magnesium pro Portion (Werte aus der Vorlage)</text>`;
      g+=`<path d="M${X0+350*S},30 V${40+D.length*26}" stroke="#c05030" stroke-width="1.6" stroke-dasharray="5 3"/><text x="${X0+350*S}" y="${52+D.length*26}" style="fill:#c05030;font:700 10.5px var(--label);text-anchor:middle">350 mg Männer</text>`;
      g+=`<path d="M${X0+300*S},30 V${40+D.length*26}" stroke="#d08a2a" stroke-width="1.2" stroke-dasharray="3 3"/><text x="${X0+300*S}" y="26" style="fill:#d08a2a;font:700 10.5px var(--label);text-anchor:middle">300 mg Frauen (Tagesbedarf)</text>`;
      D.forEach(([n,p,mg],i)=>{ const y=36+i*26, w=mg*S;
        g+=`<text x="${X0-8}" y="${y+13}" style="fill:var(--ink);font:700 12px var(--label);text-anchor:end">${n} <tspan style="fill:var(--muted);font-weight:600">${p}</tspan></text>`;
        g+=`<rect x="${X0}" y="${y+2}" width="${w}" height="16" rx="4" fill="${lg('#8ac870','#3a8a4a',0)}"><animate attributeName="width" values="0;${w}" dur="1s" begin="${i*0.12}s" fill="freeze"/></rect><text x="${X0+w+6}" y="${y+14}" style="fill:var(--ink);font:800 11px var(--label)">${mg} mg</text>`; });
      return {vb:`0 0 ${X0+350*S+60} ${62+D.length*26}`, breit:true, leg:[], svg:g}; },
    sauerkraut_gaerung(){ seed=603; let g='';
      // Glas
      g+=`<rect x="40" y="40" width="140" height="190" rx="18" fill="#eef4f0" opacity=".55" stroke="#8aa8a0" stroke-width="2"/><rect x="58" y="24" width="104" height="20" rx="5" fill="${lg('#c8ccd2','#8a9098',90)}"/>`;
      g+=`<rect x="44" y="70" width="132" height="156" rx="14" fill="${lg('#f2f0b8','#c8d070',90)}" opacity=".55"/>`;
      for(let i=0;i<46;i++){ const x=52+rnd()*116, y=96+rnd()*124; g+=`<path d="M${R(x)},${R(y)} q${R(6+rnd()*8)},${R((rnd()-.5)*6)} ${R(14+rnd()*10)},${R((rnd()-.5)*4)}" stroke="#d8e090" stroke-width="2.4" fill="none" opacity=".9"/>`; }
      g+=`<ellipse cx="110" cy="90" rx="52" ry="10" fill="${lg('#c8c0b0','#8a8070',90)}" stroke="#5a5040"/><text x="110" y="94" style="fill:#fff;font:700 10px var(--label);text-anchor:middle">Gewicht</text>`;
      g+=`<path d="M44,78 H176" stroke="#9ab8a0" stroke-width="2"/><text x="190" y="82" style="fill:#5a8a9a;font:700 10.5px var(--label)">Lake bedeckt alles</text>`;
      for(let i=0;i<8;i++) g+=`<circle cx="${R(60+rnd()*100)}" cy="220" r="${R(1.6+rnd()*2)}" fill="none" stroke="#7aa8b8" stroke-width="1"><animate attributeName="cy" values="220;80" dur="${R(3+rnd()*3)}s" begin="${R(rnd()*3)}s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;1;0" dur="${R(3+rnd()*3)}s" repeatCount="indefinite"/></circle>`;
      g+=`<text x="110" y="252" style="fill:var(--muted);font:700 11px var(--label);text-anchor:middle">CO₂-Bläschen = Gärung läuft</text>`;
      // Diagramm pH
      const X0=300,Y0=40,W=320,H=170;
      g+=`<path d="M${X0},${Y0} V${Y0+H} H${X0+W}" stroke="var(--ink)" stroke-width="1.4" fill="none"/>`;
      g+=`<text x="${X0-8}" y="${Y0+6}" style="fill:var(--muted);font:700 10px var(--label);text-anchor:end">pH 6,2</text><text x="${X0-8}" y="${Y0+H-6}" style="fill:var(--muted);font:700 10px var(--label);text-anchor:end">pH 3,5</text>`;
      g+=`<path d="M${X0},${Y0+8} C${X0+50},${Y0+20} ${X0+90},${Y0+110} ${X0+150},${Y0+130} S${X0+260},${Y0+150} ${X0+W},${Y0+152}" stroke="#c05030" stroke-width="3" fill="none" stroke-dasharray="420" stroke-dashoffset="420"><animate attributeName="stroke-dashoffset" values="420;0" dur="3s" fill="freeze"/></path>`;
      g+=`<path d="M${X0},${Y0+122} H${X0+W}" stroke="#2e7e44" stroke-dasharray="4 3"/><text x="${X0+W}" y="${Y0+116}" style="fill:#2e7e44;font:700 10px var(--label);text-anchor:end">pH unter 4,1: haltbar</text>`;
      [['1–3 Tage','Leuconostoc',X0+45,'#d8a020'],['bis ~1 Woche','L. brevis, Pediokokken',X0+150,'#8a9a30'],['danach','L. plantarum',X0+265,'#2e7e44']].forEach(([t,b,x,c])=>g+=`<rect x="${x-52}" y="${Y0+H+10}" width="104" height="34" rx="6" fill="${c}" opacity=".15" stroke="${c}"/><text x="${x}" y="${Y0+H+24}" style="fill:${c};font:800 10.5px var(--label);text-anchor:middle">${b}</text><text x="${x}" y="${Y0+H+38}" style="fill:var(--muted);font:600 10px var(--label);text-anchor:middle">${t}</text>`);
      g+=`<text x="${X0+W/2}" y="${Y0-14}" style="fill:var(--ink);font:800 12px var(--label);text-anchor:middle">Säure steigt, pH fällt – die Bakterien lösen sich ab</text>`;
      return {vb:'0 0 640 270', breit:true, leg:[], svg:g}; },
    teig_vergleich(){ seed=604; let g='';
      const T=[['Focaccia','#f0e0c0',[78,10,1,0],'Wasser + viel Öl'],['Pizza','#f2e4c8',[62,7,1,0],'Wasser + Öl'],['Brioche','#f0d080',[47,18,13,26],'Milch, Butter, Eier'],['Croissant','#f2d898',[47,22,10,13],'Milch, viel Butter']];
      const F=[['Flüssigkeit','#5aa0d8'],['Fett','#e8c040'],['Zucker','#e09a9a'],['Ei','#f0a020']];
      T.forEach(([n,c,v,s],i)=>{ const x=90+i*170;
        g+=`<ellipse cx="${x}" cy="62" rx="${50-i*2}" ry="${26+(i>1?6:0)}" fill="${lg(shade(c,.15),shade(c,-.2),90)}" stroke="${shade(c,-.45)}"><animate attributeName="ry" values="${26+(i>1?6:0)};${30+(i>1?6:0)};${26+(i>1?6:0)}" dur="${4+i*0.5}s" repeatCount="indefinite"/></ellipse>`;
        g+=`<text x="${x}" y="114" style="fill:var(--ink);font:800 13px var(--label);text-anchor:middle">${n}</text><text x="${x}" y="130" style="fill:var(--muted);font:600 10.5px var(--label);text-anchor:middle">${s}</text>`;
        v.forEach((p,k)=>{ const bx=x-56+k*29, h=p*1.2; if(!p) return; g+=`<rect x="${bx}" y="${250-h}" width="22" height="${h}" rx="3" fill="${F[k][1]}"><animate attributeName="height" values="0;${h}" dur="1s" begin="${i*.2}s" fill="freeze"/><animate attributeName="y" values="250;${250-h}" dur="1s" begin="${i*.2}s" fill="freeze"/></rect><text x="${bx+11}" y="${244-h}" style="fill:var(--ink);font:700 9.5px var(--label);text-anchor:middle">${p}</text>`; }); });
      g+=`<path d="M10,250 H680" stroke="var(--line)"/>`;
      F.forEach(([n,c],k)=>g+=`<rect x="${150+k*120}" y="262" width="12" height="12" rx="2" fill="${c}"/><text x="${166+k*120}" y="272" style="fill:var(--ink);font:700 11px var(--label)">${n}</text>`);
      g+=`<text x="680" y="292" style="fill:var(--muted);font:600 10px var(--label);text-anchor:end">in % vom Mehlgewicht (Bäckerprozent), umgerechnet aus den Tassenangaben [Ergänzung]</text>`;
      return {vb:'0 0 690 300', breit:true, leg:[], svg:g}; },
    rainfarn(){ seed=605; let g=erde();
      g+=rhizom([[150,322],[110,332],[70,328],[30,340]],'#c8a870','#8a6a40',4.4)+rhizom([[150,322],[196,334],[240,330],[286,340]],'#c8a870','#8a6a40',4.4);
      const st=[[110,96],[150,70],[190,92],[132,84],[170,80]];
      st.forEach(([x2,y2])=>g+=stiel(`M150,318 Q${(150+x2)/2+(x2<150?-6:6)},220 ${x2},${y2+30}`,2.6,'#6a7a3a'));
      for(let k=0;k<6;k++){ const y=300-k*34, s=k%2?1:-1; g+=fieder(150+s*2,y,58-k*5,s<0?-170+k*6:-10-k*6,s,false,1.15); }
      // Doldenrispe
      st.forEach(([x2,y2])=>{ g+=stiel(`M${x2},${y2+30} L${x2},${y2+8}`,1.6,'#6a7a3a');
        for(let i=0;i<7;i++){ const a=-150+i*20, ex=R(x2+Math.cos(a*Math.PI/180)*22), ey=R(y2+8+Math.sin(a*Math.PI/180)*16);
          g+=`<path d="M${x2},${y2+8} L${ex},${ey}" stroke="#6a7a3a" stroke-width=".9"/>`;
          g+=`<g><circle cx="${ex}" cy="${ey}" r="5.2" fill="${lg('#f8dc40','#d0a010',90)}" stroke="#9a7a10" stroke-width=".7"/>${[0,1,2,3].map(()=>`<circle cx="${R(ex+(rnd()-.5)*5)}" cy="${R(ey+(rnd()-.5)*5)}" r=".8" fill="#a07a08"/>`).join('')}<animateTransform attributeName="transform" type="translate" values="0 0;${R((rnd()-.5)*2)} 1;0 0" dur="${R(2.5+rnd()*2)}s" repeatCount="indefinite"/></g>`; } });
      g+=`<g transform="translate(232,40)"><circle cx="20" cy="20" r="18" fill="${lg('#f8dc40','#d0a010',90)}" stroke="#9a7a10"/>`+[...Array(30)].map(()=>{ const a=rnd()*6.28, r=Math.sqrt(rnd())*15; return `<circle cx="${R(20+Math.cos(a)*r)}" cy="${R(20+Math.sin(a)*r)}" r="1.4" fill="#c09010"/>`; }).join('')+`<text x="20" y="52" style="fill:var(--muted);font:700 9.5px var(--label);text-anchor:middle">Knopf ohne</text><text x="20" y="63" style="fill:var(--muted);font:700 9.5px var(--label);text-anchor:middle">Zungenblüten</text></g>`;
      g+=mk(40,226,1)+mk(96,64,2)+mk(212,150,3)+mk(60,356,4);
      return {vb:'0 0 300 420', leg:['Blätter einfach bis doppelt fiederschnittig, gesägt, farnähnlich; riechen gerieben stark würzig-kampferartig','Viele flache, knopfförmige goldgelbe Köpfchen ohne Zungenblüten in einer Doldenrispe (Juli–September)','Stängel aufrecht, kantig, oft rötlich überlaufen, 60–150 cm','Kriechender Wurzelstock – bildet dichte Bestände an Wegrändern und Böschungen'], svg:g}; },
