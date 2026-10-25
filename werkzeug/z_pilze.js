    pilz_aufbau(){ seed=1001; let g='';
      const T=(x,y,t,c='var(--ink)',s=10.5,w=700,a='start')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      const L=(x1,y1,x2,y2)=>`<path d="M${x1},${y1} L${x2},${y2}" stroke="var(--muted)" stroke-width=".9"/>`;
      g+=`<path d="M40,300 Q200,288 380,300 T720,298 V330 H40 Z" fill="${lg('#8a6a48','#5a4030',90)}"/>`;
      // Myzel
      let m=''; for(let i=0;i<26;i++){ const x0=250+rnd()*40-20, a=rnd()*Math.PI, l=60+rnd()*120; m+=`M${x0},302 q${Math.cos(a)*l*.5},${10+rnd()*12} ${Math.cos(a)*l},${8+rnd()*20}`; }
      g+=`<path d="${m}" stroke="#f4ecd8" stroke-width="1" fill="none" opacity=".8" stroke-dasharray="400" stroke-dashoffset="400"><animate attributeName="stroke-dashoffset" from="400" to="0" dur="3s" fill="freeze"/></path>`;
      // Knolle mit Scheide
      g+=`<path d="M226,302 C214,270 228,252 250,250 C272,252 286,270 274,302 Z" fill="${lg('#f6f2e8','#d8d0bc',0)}" stroke="#a89a80"/><path d="M222,284 C228,262 238,256 250,262 C262,256 272,262 278,284" fill="none" stroke="#a89a80" stroke-width="1.4"/>`;
      // Stiel
      g+=`<path d="M238,256 C240,200 238,150 240,120 L260,120 C262,150 260,200 262,256 Z" fill="${lg('#fbf8f0','#e2dccb',0)}" stroke="#b0a68e"/>`;
      // Ring
      g+=`<path d="M236,150 C236,166 264,166 264,150 C268,160 270,170 262,174 C254,170 246,170 238,174 C230,170 232,160 236,150 Z" fill="#f2ecdc" stroke="#a89a80"/>`;
      // Hut
      g+=`<path d="M120,122 C130,50 370,50 380,122 Z" fill="${lg('#c8d098','#8a9a58',90)}" stroke="#5a6a38" stroke-width="1.4"/>`;
      g+=`<path d="M120,122 H380" stroke="#5a6a38"/>`;
      for(let x=128;x<374;x+=5) g+=`<path d="M${x},122 L${250+(x-250)*0.12},${x<250?130:130}" stroke="#ede6d4" stroke-width="1.6"/>`;
      g+=`<path d="M124,122 C140,134 360,134 376,122" fill="#f4eee0" stroke="#b8ae96"/>`;
      // Sporen
      for(let i=0;i<14;i++){ const x=150+rnd()*200; g+=`<circle cx="${x.toFixed(1)}" cy="136" r="1.6" fill="#8a7a5a"><animate attributeName="cy" values="136;300" dur="${(3+rnd()*3).toFixed(1)}s" begin="${(rnd()*3).toFixed(1)}s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;0" dur="${(3+rnd()*3).toFixed(1)}s" begin="0s" repeatCount="indefinite"/></circle>`; }
      // Beschriftung
      g+=L(330,80,450,60)+T(456,64,'Hut (Huthaut)')+L(350,126,450,100)+T(456,104,'Lamellen – hier entstehen die Sporen')+L(262,160,450,150)+T(456,154,'Ring (Manschette, Rest der Teilhülle)')+L(258,210,450,196)+T(456,200,'Stiel')+L(276,286,450,248)+T(456,252,'Knolle mit Scheide (Volva, Rest der Gesamthülle)')+L(360,312,450,300)+T(456,304,'Myzel – der eigentliche Pilz im Boden')+L(200,200,120,210)+T(114,214,'Sporen','var(--ink)',10.5,700,'end');
      g+=T(380,20,'Aufbau eines Lamellenpilzes (Beispiel Knollenblätterpilz – tödlich giftig!)','var(--ink)',12.5,800,'middle');
      return {vb:'0 0 760 336',breit:true,leg:[],svg:g}; },

    pilz_unterseiten(){ seed=1002; let g='';
      const T=(x,y,t,c='var(--ink)',s=10.5,w=700)=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:middle">${t}</text>`;
      const A=[['Lamellen','Champignon, Täublinge, Knollis','#efe6d2'],['Röhren / Poren','Steinpilz, Marone, Birkenpilz','#e8d880'],['Leisten','Pfifferling, Trompetenpfifferling','#f0b040'],['Stacheln','Semmelstoppelpilz, Habichtspilz','#e8c890']];
      A.forEach(([n,b,c],i)=>{ const cx=95+i*190, cy=110, R=70;
        g+=`<g><circle cx="${cx}" cy="${cy}" r="${R}" fill="${lg(shade(c,0.2),shade(c,-0.15),90)}" stroke="${shade(c,-0.45)}" stroke-width="1.4"/>`;
        if(i===0) for(let a=0;a<72;a++){ const t=a/72*Math.PI*2; g+=`<path d="M${cx+Math.cos(t)*14},${cy+Math.sin(t)*14} L${cx+Math.cos(t)*R*.97},${cy+Math.sin(t)*R*.97}" stroke="${shade(c,-0.35)}" stroke-width=".8"/>`; }
        if(i===1) for(let k=0;k<160;k++){ const r=Math.sqrt(rnd())*R*.9+4, t=rnd()*Math.PI*2; g+=`<circle cx="${(cx+Math.cos(t)*r).toFixed(1)}" cy="${(cy+Math.sin(t)*r).toFixed(1)}" r="1.9" fill="${shade(c,-0.4)}"/>`; }
        if(i===2) for(let a=0;a<28;a++){ const t=a/28*Math.PI*2; g+=`<path d="M${cx+Math.cos(t)*16},${cy+Math.sin(t)*16} Q${cx+Math.cos(t+.15)*R*.5},${cy+Math.sin(t+.15)*R*.5} ${cx+Math.cos(t)*R*.97},${cy+Math.sin(t)*R*.97} M${cx+Math.cos(t)*R*.6},${cy+Math.sin(t)*R*.6} L${cx+Math.cos(t+.1)*R*.95},${cy+Math.sin(t+.1)*R*.95}" stroke="${shade(c,-0.35)}" stroke-width="1.6" fill="none"/>`; }
        if(i===3) for(let k=0;k<120;k++){ const r=Math.sqrt(rnd())*R*.9+4, t=rnd()*Math.PI*2, x=cx+Math.cos(t)*r, y=cy+Math.sin(t)*r; g+=`<path d="M${(x-2).toFixed(1)},${(y+2).toFixed(1)} L${x.toFixed(1)},${(y-3).toFixed(1)} L${(x+2).toFixed(1)},${(y+2).toFixed(1)} Z" fill="${shade(c,-0.3)}"/>`; }
        g+=`<circle cx="${cx}" cy="${cy}" r="13" fill="#f4eee0" stroke="${shade(c,-0.45)}"/><animateTransform attributeName="transform" type="rotate" from="0 ${cx} ${cy}" to="${i%2?-360:360} ${cx} ${cy}" dur="60s" repeatCount="indefinite"/></g>`;
        g+=T(cx,206,n,'var(--ink)',12,800)+T(cx,222,b,'var(--muted)',9.5,600); });
      g+=T(380,18,'Hutunterseiten – das erste Merkmal beim Bestimmen','var(--ink)',12.5,800);
      return {vb:'0 0 760 232',breit:true,leg:[],svg:g}; },

    pilz_doppelgaenger(){ seed=1003; let g='';
      const T=(x,y,t,c='var(--ink)',s=10.5,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a}">${t}</text>`;
      const pilz=(cx,hut,lam,knolle,ring)=>{ let s=`<path d="M${cx-14},236 C${cx-12},190 ${cx-12},150 ${cx-10},118 L${cx+10},118 C${cx+12},150 ${cx+12},190 ${cx+14},236 Z" fill="${lg('#fbf8f0','#e2dccb',0)}" stroke="#b0a68e"/>`;
        if(knolle) s+=`<path d="M${cx-24},240 C${cx-30},212 ${cx-14},200 ${cx},202 C${cx+14},200 ${cx+30},212 ${cx+24},240 Z" fill="#f2ecdc" stroke="#a89a80"/><path d="M${cx-26},226 C${cx-18},206 ${cx+18},206 ${cx+26},226" fill="none" stroke="#a89a80" stroke-width="1.4"/>`;
        else s+=`<path d="M${cx-15},240 Q${cx},246 ${cx+15},240" stroke="#b0a68e" fill="none"/>`;
        s+=`<path d="M${cx-14},${ring} C${cx-14},${ring+12} ${cx+14},${ring+12} ${cx+14},${ring} L${cx+18},${ring+10} C${cx},${ring+20} ${cx},${ring+20} ${cx-18},${ring+10} Z" fill="#f2ecdc" stroke="#a89a80"/>`;
        s+=`<path d="M${cx-90},116 C${cx-80},44 ${cx+80},44 ${cx+90},116 Z" fill="${lg(shade(hut,0.25),shade(hut,-0.15),90)}" stroke="${shade(hut,-0.45)}" stroke-width="1.4"/>`;
        for(let x=cx-86;x<cx+86;x+=4.5) s+=`<path d="M${x},116 L${cx+(x-cx)*0.15},126" stroke="${lam}" stroke-width="1.7"/>`;
        return s; };
      g+=pilz(190,'#f0ead8','#c87a8a',false,150)+pilz(570,'#b8c088','#f6f2ea',true,140);
      g+=T(190,22,'Wiesenchampignon – essbar','#2a7a3a',13,800)+T(570,22,'Grüner Knollenblätterpilz – tödlich','#b02020',13,800);
      const L=[['Lamellen rosa, später schokobraun','Lamellen immer weiß'],['keine Knolle, Stiel unten gerade','Knolle mit häutiger Scheide (oft im Boden – ganz ausgraben!)'],['Ring schmal, unauffällig','Ring hängend, manchmal vergänglich'],['Wiesen, Weiden, kein Wald','Laubwald, v. a. bei Eichen und Buchen'],['riecht angenehm pilzig','Geruch süßlich, im Alter unangenehm']];
      L.forEach(([a,b],i)=>{ g+=T(190,272+i*17,'✓ '+a,'#2a6a3a',10,700)+T(570,272+i*17,'✗ '+b,'#a02020',10,700); });
      g+=`<path d="M380,40 V350" stroke="var(--muted)" stroke-dasharray="4 4"/>`;
      return {vb:'0 0 760 362',breit:true,leg:[],svg:g}; },
