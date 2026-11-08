    waschmittel_titel(){ seed=3101; let g='';
      const T=(x,y,t,c='var(--muted)',s=11,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      // Tisch
      g+=`<rect x="14" y="236" width="732" height="28" rx="6" fill="${lg('#c89a64','#9a6a3a',90)}" stroke="#6a4420" stroke-width="1"/>`;
      for(let i=0;i<2;i++) g+=`<path d="M24,${245+i*9} q340,${R(rnd()*6-3)} 712,0" stroke="#8a5a2c" stroke-width=".8" fill="none" opacity=".5"/>`;
      // Flasche Flüssigwaschmittel
      const fx=110;
      g+=`<ellipse cx="${fx}" cy="238" rx="52" ry="7" fill="#000" opacity=".15"/>`;
      g+=`<path d="M${fx-12},40 h24 v26 q36,14 36,52 v112 q0,8 -8,8 h-80 q-8,0 -8,-8 v-112 q0,-38 36,-52 Z" fill="${lg('#eef4f6','#c4d2d8',0)}" stroke="#6a7a84" stroke-width="1.4" opacity=".95"/>`;
      g+=`<path d="M${fx-42},132 q42,-8 84,0 v96 q0,6 -6,6 h-72 q-6,0 -6,-6 Z" fill="${lg('#f2e2a8','#d8bc6a',90)}" opacity=".9"/>`;
      g+=`<path d="M${fx-42},132 q42,-8 84,0" stroke="#fff" stroke-width="2" fill="none" opacity=".7"/>`;
      g+=`<rect x="${fx-15}" y="26" width="30" height="18" rx="3" fill="${lg('#5a8a6a','#3a6a4a',90)}" stroke="#2a4a34"/>`;
      g+=`<rect x="${fx-30}" y="160" width="60" height="38" rx="4" fill="#fbf6e8" stroke="#8a7a5a"/>`;
      g+=`<text x="${fx}" y="176" style="fill:#5a4a2a;font:800 10px var(--label);text-anchor:middle">Flüssig-</text><text x="${fx}" y="189" style="fill:#5a4a2a;font:800 10px var(--label);text-anchor:middle">waschmittel</text>`;
      g+=`<path d="M${fx-30},96 q-6,40 0,90" stroke="#fff" stroke-width="5" fill="none" opacity=".45" stroke-linecap="round"/>`;
      // Glas Waschpulver
      const gx=250;
      g+=`<ellipse cx="${gx}" cy="238" rx="50" ry="7" fill="#000" opacity=".15"/>`;
      g+=`<rect x="${gx-44}" y="118" width="88" height="116" rx="12" fill="${lg('#f2f6f8','#cfdae0',0)}" stroke="#6a7a84" stroke-width="1.4"/>`;
      g+=`<path d="M${gx-40},150 q40,-10 80,0 v76 q0,4 -4,4 h-72 q-4,0 -4,-4 Z" fill="${lg('#ffffff','#e4e0d6',90)}"/>`;
      for(let i=0;i<60;i++) g+=`<circle cx="${R(gx-36+rnd()*72)}" cy="${R(152+rnd()*72)}" r="${R(.6+rnd()*1.2)}" fill="${rnd()<.5?'#d8d2c2':'#f6f0dc'}"/>`;
      g+=`<rect x="${gx-48}" y="102" width="96" height="20" rx="4" fill="${lg('#c8a060','#8a6a34',90)}" stroke="#5a4420"/>`;
      g+=`<rect x="${gx-30}" y="172" width="60" height="30" rx="4" fill="#fbf6e8" stroke="#8a7a5a"/>`;
      g+=`<text x="${gx}" y="191" style="fill:#5a4a2a;font:800 10px var(--label);text-anchor:middle">Waschpulver</text>`;
      // Kernseife mit Reibe und Flocken
      const sx=400;
      g+=`<ellipse cx="${sx+10}" cy="238" rx="70" ry="7" fill="#000" opacity=".14"/>`;
      g+=`<path d="M${sx-58},204 l18,-22 h64 l-18,22 Z" fill="${lg('#f4ead0','#e2d2a8',0)}" stroke="#8a7a50"/><path d="M${sx-58},204 h64 v30 h-64 Z" fill="${lg('#eadcb4','#c8b480',90)}" stroke="#8a7a50" stroke-width="1.2"/><path d="M${sx+6},204 l18,-22 v30 l-18,22 Z" fill="${lg('#d8c898','#b0a070',0)}" stroke="#8a7a50"/>`;
      g+=`<text x="${sx-26}" y="224" style="fill:#8a7a50;font:800 9px var(--label);text-anchor:middle">SEIFE</text>`;
      // Reibe
      g+=`<path d="M${sx+34},234 L${sx+48},116 h34 L${sx+96},234 Z" fill="${lg('#e0e4e8','#9aa2aa',0)}" stroke="#5a6068" stroke-width="1.4"/><path d="M${sx+56},110 q9,-16 18,0" stroke="#5a6068" stroke-width="4" fill="none"/>`;
      for(let r=0;r<6;r++) for(let c=0;c<3;c++){ const y=134+r*16, x=sx+54+c*9-(r*1.4)+r*2.2*(c-1)*.2; g+=`<path d="M${R(x)},${y} q4,-4 8,0" stroke="#5a6068" stroke-width="1.2" fill="none"/>`; }
      for(let i=0;i<16;i++){ const x=R(sx-60+rnd()*150), y=R(232+rnd()*4); g+=`<path d="M${x},${y} q4,-5 9,-1" stroke="#c8b480" stroke-width="2.2" fill="none" stroke-linecap="round"/>`; }
      // Efeuranke
      const efeu=(x,y,s,w)=>`<g transform="translate(${x} ${y}) rotate(${w}) scale(${s})"><path d="M0,0 L-12,-10 L-8,-22 L-2,-16 L0,-30 L4,-16 L10,-22 L12,-10 Z" fill="${lg('#4a7a3a','#2a4a22',90)}" stroke="#1e3418" stroke-width=".9" stroke-linejoin="round"/><path d="M0,0 V-26 M0,-8 L-9,-16 M0,-8 L9,-16" stroke="#b8d0a0" stroke-width=".7" fill="none"/></g>`;
      g+=`<path d="M560,232 C580,190 560,150 600,120 S660,80 700,96" stroke="#5a4a2a" stroke-width="3" fill="none"/>`;
      [[574,206,1.3,-30],[566,170,1.2,-70],[590,136,1.3,-20],[622,112,1.2,20],[656,96,1.1,-40],[694,94,1.0,30],[600,180,1.0,40]].forEach(a=>g+=efeu(...a));
      // Kastanien
      const kast=(x,y,r)=>`<ellipse cx="${x}" cy="${y}" rx="${r}" ry="${R(r*.88)}" fill="${lg('#9a4e22','#4a2210',120)}" stroke="#2a1408" stroke-width="1.2"/><ellipse cx="${x}" cy="${R(y+r*.5)}" rx="${R(r*.62)}" ry="${R(r*.3)}" fill="${lg('#d8c09a','#b09a70',90)}"/><path d="M${R(x-r*.4)},${R(y-r*.4)} q${R(r*.3)},${R(-r*.3)} ${R(r*.6)},0" stroke="#e0a070" stroke-width="2" fill="none" opacity=".7"/>`;
      g+=kast(650,218,17)+kast(684,224,15)+kast(712,212,16)+kast(626,228,12);
      // Zitronensäure-Tütchen & Natron
      g+=`<path d="M488,234 v-54 l6,-8 h40 l6,8 v54 Z" fill="${lg('#fff6c8','#e8d888',0)}" stroke="#9a8a40" stroke-width="1.2"/><text x="514" y="206" style="fill:#7a6a20;font:800 8px var(--label);text-anchor:middle">Zitronen-</text><text x="514" y="216" style="fill:#7a6a20;font:800 8px var(--label);text-anchor:middle">säure</text>`;
      // Seifenblasen
      for(let i=0;i<9;i++){ const x=R(70+rnd()*480), y=R(30+rnd()*60), r=R(5+rnd()*9), d=R(3+rnd()*3); g+=`<circle cx="${x}" cy="${y}" r="${r}" fill="${lg('#e8f4ff','#c8e0f0',45)}" stroke="#8ab0d0" stroke-width=".9" opacity=".75"><animate attributeName="cy" values="${y};${y-14};${y}" dur="${d}s" repeatCount="indefinite"/></circle>`; }
      g+=T(380,290,'Waschmittel und Reiniger selbst machen – Kernseife, Soda, Natron, Zitronensäure, Efeu und Kastanien','var(--ink)',13,800);
      return {vb:'0 0 760 300', breit:true, leg:[], svg:g}; },
    waschmittel_mizelle(){ seed=3201; let g='';
      const T=(x,y,t,c='var(--ink)',s=10.5,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      const kopf=(x,y,r=6,f='#3a7ac8')=>`<circle cx="${x}" cy="${y}" r="${r}" fill="${lg(shade(f,0.25),shade(f,-0.2),90)}" stroke="${shade(f,-0.45)}" stroke-width="1"/>`;
      const schwanz=(x,y,len,w)=>{ const a=w*Math.PI/180; let d=`M${x},${y}`; const n=6; for(let i=1;i<=n;i++){ const t=len*i/n, o=(i%2?4:-4); d+=` L${R(x+Math.cos(a)*t-Math.sin(a)*o)},${R(y+Math.sin(a)*t+Math.cos(a)*o)}`; } return `<path d="${d}" stroke="#c88a2a" stroke-width="2.4" fill="none" stroke-linejoin="round" stroke-linecap="round"/>`; };
      // Feld 1: Tensid-Molekül
      g+=`<rect x="10" y="10" width="220" height="270" rx="12" fill="none" stroke="var(--line)"/>`;
      g+=T(120,32,'1 · Ein Seifen-Teilchen (Tensid)','var(--ink)',12,800);
      g+=schwanz(80,130,110,0)+kopf(68,130,13);
      g+=`<text x="68" y="134" style="fill:#fff;font:800 10px var(--label);text-anchor:middle">–</text>`;
      g+=T(68,166,'Kopf: wasserliebend','#2a5a9a',10.5,800)+T(68,180,'(Carboxylat, geladen)','var(--muted)',9.5,600);
      g+=T(150,112,'Schwanz: fettliebend','#9a6418',10.5,800)+T(150,98,'(Kohlenstoffkette)','var(--muted)',9.5,600);
      g+=T(120,222,'Kernseife = Natriumsalze','var(--muted)',10,700)+T(120,236,'von Fettsäuren','var(--muted)',10,700)+T(120,254,'(z. B. Natriumstearat)','var(--muted)',9.5,600);
      // Feld 2: Mizelle
      g+=`<rect x="240" y="10" width="250" height="270" rx="12" fill="none" stroke="var(--line)"/>`;
      g+=T(365,32,'2 · Mizelle umschließt Fett','var(--ink)',12,800);
      const mx=365,my=140;
      g+=`<circle cx="${mx}" cy="${my}" r="66" fill="${lg('#e8f2fa','#cfe2f0',90)}" opacity=".6"/>`;
      g+=`<circle cx="${mx}" cy="${my}" r="30" fill="${lg('#f6d870','#d8a830',90)}" stroke="#a87a18" stroke-width="1"/>`;
      g+=T(mx,my+4,'Fett','#6a4a08',11,800);
      for(let i=0;i<16;i++){ const a=i/16*Math.PI*2, x=R(mx+Math.cos(a)*62), y=R(my+Math.sin(a)*62); g+=schwanz(x,y,30,a*180/Math.PI+180)+kopf(x,y,6); }
            g+=T(365,232,'Schwänze stecken im Fett,','var(--muted)',10,700)+T(365,246,'Köpfe zeigen ins Wasser –','var(--muted)',10,700)+T(365,260,'das Fett wird ausgespült','var(--muted)',10,700);
      // Feld 3: hartes Wasser -> Kalkseife
      g+=`<rect x="500" y="10" width="250" height="270" rx="12" fill="none" stroke="var(--line)"/>`;
      g+=T(625,32,'3 · Hartes Wasser: Kalkseife','var(--ink)',12,800);
      const ca=(x,y)=>`<circle cx="${x}" cy="${y}" r="11" fill="${lg('#f0f0f0','#b8bcc0',90)}" stroke="#6a7078" stroke-width="1.1"/><text x="${x}" y="${y+3.5}" style="fill:#3a4048;font:800 8.5px var(--label);text-anchor:middle">Ca²⁺</text>`;
      g+=schwanz(560,90,40,180)+kopf(572,90,6)+ca(590,90)+kopf(608,90,6)+schwanz(620,90,40,0);
      g+=T(625,120,'2 Seifenteilchen + 1 Kalk-Ion','var(--muted)',10,700)+T(625,134,'→ unlösliche Kalkseife','#6a7078',10.5,800);
      // Faser mit Flocken
      g+=`<path d="M520,190 C580,176 660,204 730,186" stroke="${lg('#c89a8a','#9a6a5a',90)}" stroke-width="18" fill="none" stroke-linecap="round"/>`;
      for(let i=0;i<14;i++){ const x=R(530+rnd()*190), y=R(178+rnd()*12); g+=`<ellipse cx="${x}" cy="${y}" rx="${R(3+rnd()*4)}" ry="${R(2+rnd()*2)}" fill="#e8e8e4" stroke="#8a8e92" stroke-width=".7"/>`; }
      g+=T(625,222,'lagert sich in Faser und','var(--muted)',10,700)+T(625,236,'Maschine ab → Grauschleier','var(--muted)',10,700);
      g+=T(625,258,'Soda/Citrat binden Kalk vorher','#3a7a4a',10,800);
      g+=T(380,304,'Wie Seife Schmutz löst – und warum hartes Wasser sie ausbremst','var(--ink)',12.5,800);
      return {vb:'0 0 760 316', breit:true, leg:[], svg:g}; },
    wasch_leiste(liste){ seed=3301; let g=''; const n=liste.length;
      for(let i=1;i<n;i++) g+=`<path d="M${i*150},10 V200" stroke="var(--line)" stroke-width="1"/>`;
      const txt=(x,y,t,s=12,c='var(--ink)')=>`<text x="${x}" y="${y}" style="fill:${c};font:800 ${s}px var(--label);text-anchor:middle;paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      const schuessel=(x,y,w,h)=>`<path d="M${x-w/2},${y} Q${x-w/2},${y+h} ${x},${y+h} Q${x+w/2},${y+h} ${x+w/2},${y} Z" fill="${lg('#d8dce0','#8a9098',0)}" stroke="#5a6068" stroke-width="1.3"/><path d="M${x-w/2-4},${y} H${x+w/2+4}" stroke="#5a6068" stroke-width="3" stroke-linecap="round"/>`;
      const dampf=(x0,y0)=>[0,1,2].map(i=>`<path d="M${x0+i*18},${y0} q-6,-10 0,-20 q6,-10 0,-20" stroke="#c8d4dc" stroke-width="3" fill="none" stroke-linecap="round" opacity="0"><animate attributeName="opacity" values="0;.9;0" dur="2.4s" begin="${i*0.6}s" repeatCount="indefinite"/></path>`).join('');
      const pulver=(x,y,w,c=['#ffffff','#e8e2d0','#f4ecd0'])=>[...Array(26)].map(()=>`<circle cx="${R(x-w/2+rnd()*w)}" cy="${R(y-rnd()*8)}" r="${R(1+rnd()*1.6)}" fill="${c[Math.floor(rnd()*c.length)]}" stroke="#a8a090" stroke-width=".3"/>`).join('');
      const I={
        reiben:p=>`<path d="M30,150 l12,-14 h40 l-12,14 Z" fill="#f0e4c0" stroke="#8a7a50"/><path d="M30,150 h40 v20 h-40 Z" fill="${lg('#eadcb4','#c8b480',90)}" stroke="#8a7a50"/><path d="M84,170 L92,60 h26 L128,170 Z" fill="${lg('#e0e4e8','#9aa2aa',0)}" stroke="#5a6068" stroke-width="1.3"/>`+[...Array(5)].map((_,r)=>`<path d="M98,${78+r*16} q4,-4 8,0 M108,${80+r*16} q4,-4 8,0" stroke="#5a6068" fill="none"/>`).join('')+[...Array(10)].map(()=>{const x=R(36+rnd()*90),y=R(176+rnd()*8);return `<path d="M${x},${y} q4,-5 8,-1" stroke="#c8b480" stroke-width="2" fill="none" stroke-linecap="round"/>`;}).join('')+(p.t?txt(52,60,p.t,12):''),
        mischen:p=>schuessel(75,120,104,60)+pulver(75,122,80,p.c)+`<g><path d="M110,44 L84,118" stroke="#8a6a3a" stroke-width="6" stroke-linecap="round"/><animateTransform attributeName="transform" type="rotate" values="-8 84 118;8 84 118;-8 84 118" dur="2s" repeatCount="indefinite"/></g>`+(p.t?txt(48,56,p.t,12):''),
        giessen:p=>schuessel(75,130,104,56)+pulver(75,132,80)+`<path d="M86,40 h40 l6,10 v30 h-46 Z" fill="${lg('#e0e4e8','#8a9098',0)}" stroke="#4a5058" stroke-width="1.3" transform="rotate(-30 110 60)"/><path d="M82,74 Q76,96 74,124" stroke="#7ab0d8" stroke-width="5" fill="none" stroke-linecap="round"><animate attributeName="stroke-dasharray" values="0,80;80,0" dur="1.5s" repeatCount="indefinite"/></path>`+dampf(44,110)+(p.t?txt(40,52,p.t,12):''),
        ruehren:p=>schuessel(75,118,104,62)+`<ellipse cx="75" cy="120" rx="46" ry="12" fill="${lg('#f2e6b8','#d8c080',90)}"/><g><path d="M75,30 V112" stroke="#8a6a3a" stroke-width="6" stroke-linecap="round"/><ellipse cx="75" cy="114" rx="8" ry="4" fill="#8a6a3a"/><animateTransform attributeName="transform" type="rotate" values="-14 75 120;14 75 120;-14 75 120" dur="1.6s" repeatCount="indefinite"/></g>`+(p.t?txt(120,52,p.t,11,'var(--muted)'):''),
        abkuehlen:p=>schuessel(75,124,104,56)+`<ellipse cx="75" cy="126" rx="46" ry="12" fill="${lg('#f2e6b8','#d8c080',90)}"/><rect x="112" y="40" width="12" height="74" rx="6" fill="#f4f6f8" stroke="#6a7078"/><circle cx="118" cy="116" r="10" fill="#d84a3a" stroke="#6a7078"/><rect x="115" y="80" width="6" height="34" fill="#d84a3a"><animate attributeName="height" values="34;14;34" dur="5s" repeatCount="indefinite"/><animate attributeName="y" values="80;100;80" dur="5s" repeatCount="indefinite"/></rect>`+(p.t?txt(52,60,p.t,12):''),
        flasche:p=>`<path d="M62,40 h26 v24 q30,12 30,44 v74 q0,6 -6,6 h-74 q-6,0 -6,-6 v-74 q0,-32 30,-44 Z" fill="${lg('#eef4f6','#c4d2d8',0)}" stroke="#6a7a84" stroke-width="1.3"/><path d="M38,120 q37,-8 74,0 v60 q0,4 -4,4 h-66 q-4,0 -4,-4 Z" fill="${lg('#f2e2a8','#d8bc6a',90)}"/><rect x="60" y="28" width="30" height="14" rx="3" fill="#5a8a6a" stroke="#2a4a34"/>`+(p.t?txt(75,154,p.t,11,'#5a4a2a'):''),
        glas:p=>`<rect x="35" y="70" width="80" height="112" rx="12" fill="${lg('#f2f6f8','#cfdae0',0)}" stroke="#6a7a84" stroke-width="1.3"/><path d="M39,100 q36,-8 72,0 v76 q0,3 -3,3 h-66 q-3,0 -3,-3 Z" fill="${lg('#ffffff','#e4e0d6',90)}"/>`+pulver(75,170,64)+pulver(75,140,64)+`<rect x="31" y="56" width="88" height="18" rx="4" fill="${lg('#c8a060','#8a6a34',90)}" stroke="#5a4420"/>`+(p.t?txt(75,44,p.t,12):''),
        dosieren:p=>`<circle cx="75" cy="128" r="54" fill="${lg('#e8ecf0','#a8b0b8',0)}" stroke="#4a5058" stroke-width="2"/><circle cx="75" cy="128" r="40" fill="${lg('#5a7a9a','#2a4a6a',90)}" stroke="#2a3a4a"/><circle cx="75" cy="128" r="30" fill="none" stroke="#8ab0d0" stroke-dasharray="4 5"><animateTransform attributeName="transform" type="rotate" values="0 75 128;360 75 128" dur="4s" repeatCount="indefinite"/></circle><path d="M96,46 h30 l-4,12 h-22 Z" fill="${lg('#f4f4f4','#c0c0c0',90)}" stroke="#6a7078"/><path d="M98,46 h26" stroke="#fff"/>`+(p.t?txt(56,40,p.t,12):''),
        saeure:p=>schuessel(75,124,104,56)+`<ellipse cx="75" cy="126" rx="46" ry="12" fill="${lg('#f2e6b8','#d8c080',90)}"/><path d="M92,40 v34 l8,10 h-36 l8,-10 v-34 Z" fill="${lg('#fff6c8','#e8d888',0)}" stroke="#9a8a40" transform="rotate(25 82 60)"/>`+[...Array(6)].map((_,k)=>`<circle cx="${R(55+k*8)}" cy="118" r="${R(2+rnd()*2)}" fill="#fff" stroke="#8ab0d0"><animate attributeName="cy" values="122;104;122" dur="${R(1+rnd())}s" repeatCount="indefinite"/></circle>`).join('')+(p.t?txt(44,56,p.t,12):'')
      };
      liste.forEach(([icon,titel,p],i)=>g+=vign(i,titel,I[icon](p||{})));
      return {vb:`0 0 ${n*150} 230`, breit:true, leg:[], svg:g}; },
    waschmittel_fluessig_leiste(){ return Z.wasch_leiste([['reiben','1 · 30 g Kernseife fein raspeln',{t:'30 g'}],['mischen','2 · Flocken + 40 g Waschsoda',{t:'+ Soda',c:['#f0e4c0','#ffffff','#e8dcb0']}],['giessen','3 · 2 l kochendes Wasser darüber',{t:'2 l'}],['ruehren','4 · Rühren, bis alles gelöst ist',{t:'lösen'}],['abkuehlen','5 · Abkühlen, ggf. durchrühren',{t:'abkühlen'}],['saeure','6 · Zitronensäure + Öl, abfüllen',{t:'zum Schluss'}]]); },
    waschmittel_pulver_leiste(){ return Z.wasch_leiste([['reiben','1 · 100 g Kernseife fein reiben',{t:'100 g'}],['mischen','2 · 150 g Soda, 150 g Natron, 100 g Zitronensäure',{t:'mischen'}],['glas','3 · Luftdicht ins Glas',{t:'trocken!'}],['dosieren','4 · 1–3 EL (30–50 g) je Wäsche',{t:'1–3 EL'}]]); },
