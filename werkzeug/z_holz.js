    holz_obst(){ seed=811; let g='';
      const T=(x,y,t,c,s=12,w=800)=>`<text x="${x}" y="${y}" style="fill:${c||'var(--ink)'};font:${w} ${s}px var(--label);text-anchor:middle;paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      const scheibe=(cx,cy,r,kern,splint,rinde)=>{ let s=`<ellipse cx="${cx}" cy="${cy}" rx="${r+5}" ry="${r+5}" fill="${rinde}"/>`;
        s+=`<ellipse cx="${cx}" cy="${cy}" rx="${r}" ry="${r}" fill="${lg(splint,shade(splint,-0.18),45)}"/>`;
        s+=`<ellipse cx="${cx+2}" cy="${cy+1}" rx="${R(r*.62)}" ry="${R(r*.58)}" fill="${lg(kern,shade(kern,-0.20),45)}"/>`;
        for(let i=1;i<=7;i++){ const rr=r*i/8+rnd()*1.5; s+=`<ellipse cx="${R(cx+rnd()*1.5)}" cy="${R(cy+rnd()*1.5)}" rx="${R(rr)}" ry="${R(rr*(.95+rnd()*.06))}" fill="none" stroke="${shade(kern,-0.30)}" stroke-width=".7" opacity=".4"/>`; }
        for(let i=0;i<3;i++){ const a=rnd()*6.28; s+=`<path d="M${cx},${cy} L${R(cx+Math.cos(a)*r*.9)},${R(cy+Math.sin(a)*r*.9)}" stroke="${shade(kern,-0.45)}" stroke-width=".8" opacity=".5"/>`; }
        return s+`<circle cx="${cx}" cy="${cy}" r="1.6" fill="${shade(kern,-0.50)}"/>`; };
      const scheit=(x,y,L,rinde)=>{ let s=`<path d="M${x},${y} h${L} l8,-26 h-${L} z" fill="${lg('#e8c89a','#c89a62',90)}"/>`;
        s+=`<path d="M${x},${y} h${L} v14 h-${L} z" fill="${lg(rinde,shade(rinde,-0.25),90)}"/>`;
        for(let i=0;i<5;i++) s+=`<path d="M${R(x+6+rnd()*(L-12))},${y+2} v${R(6+rnd()*6)}" stroke="${shade(rinde,-0.40)}" stroke-width="1"/>`;
        for(let i=0;i<4;i++) s+=`<path d="M${R(x+8+i*L/4)},${y-3} l${R(6+rnd()*3)},${-R(18+rnd()*4)}" stroke="#b08050" stroke-width=".7" opacity=".7"/>`;
        return s; };
      const flamme=(x,y,k)=>`<path d="M${x},${y} c-7,-6 -6,-14 0,-22 c1,7 7,9 6,16 c3,-3 3,-6 2,-9 c5,6 4,13 -1,15 z" fill="${lg('#f8d040','#e0501a',90)}"><animateTransform attributeName="transform" type="scale" values="1 1;1 1.12;1 .95;1 1" dur="${1.2+k*.2}s" repeatCount="indefinite" additive="sum"/></path>`;
      const arten=[
        ['Apfel','#e8b88a','#f8e6c8','#9a7a5a',(x,y)=>`<circle cx="${x}" cy="${y}" r="15" fill="${lg('#e84a30','#a82818',60)}"/><path d="M${x},${y-14} q2,-7 6,-9" stroke="#5a3a1a" stroke-width="2" fill="none"/><path d="M${x+5},${y-18} q8,-6 13,0 q-7,4 -13,0z" fill="#5a9a3a"/>`,'dicht · gute Glut · ruhiger Abbrand',3],
        ['Kirsche','#d8845a','#f6dcb8','#8a5a4a',(x,y)=>`<path d="M${x-8},${y} q4,-20 12,-28 M${x+9},${y+2} q-2,-18 -5,-30" stroke="#4a6a2a" stroke-width="1.6" fill="none"/><circle cx="${x-8}" cy="${y+4}" r="8" fill="${lg('#e02030','#8a0a18',60)}"/><circle cx="${x+9}" cy="${y+6}" r="8" fill="${lg('#e02030','#8a0a18',60)}"/>`,'recht dicht · schöne Flamme · Duft',3],
        ['Birne','#d49a70','#f4dcbc','#8a7868',(x,y)=>`<path d="M${x},${y-20} c-6,0 -7,10 -9,16 c-6,8 -4,20 9,20 c13,0 15,-12 9,-20 c-2,-6 -3,-16 -9,-16z" fill="${lg('#d8c840','#9a9a20',60)}"/><path d="M${x},${y-20} v-6" stroke="#5a3a1a" stroke-width="2"/>`,'dicht · lange Brenndauer',3],
        ['Pflaume','#a85a52','#f0d0a8','#7a5a5a',(x,y)=>`<ellipse cx="${x}" cy="${y}" rx="11" ry="14" fill="${lg('#5a3a8a','#2a1a4a',60)}"/><path d="M${x-2},${y-12} q-2,10 0,24" stroke="#3a2a5a" stroke-width="1" fill="none" opacity=".6"/><ellipse cx="${x+3}" cy="${y-5}" rx="3" ry="5" fill="#9a8ac8" opacity=".35"/>`,'oft knorrig · ordentliche Wärme · seltener',2]];
      arten.forEach(([n,kern,splint,rinde,frucht,txt,fl],i)=>{ const x0=10+i*188, cx=x0+60;
        g+=T(x0+88,22,n,'#6a3a1a',15);
        g+=scheit(x0+8,150,96,rinde)+scheibe(cx,92,40,kern,splint,rinde)+frucht(x0+142,108);
        g+=T(x0+88,182,txt.split(' · ').slice(0,2).join(' · '),'var(--muted)',10,600)+T(x0+88,196,txt.split(' · ').slice(2).join(' · '),'var(--muted)',10,600);
        for(let k=0;k<fl;k++) g+=flamme(x0+66+k*16,228,k); });
      return {vb:'0 0 760 236',breit:true,leg:[],svg:g}; },
    verbrennung_phasen(){ seed=812; let g='';
      const T=(x,y,t,c,s=11,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c||'var(--ink)'};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      const Z=[['1 · Trocknen','bis ~150 °C','Wasser verdampft','#7aa8d8'],['2 · Entgasen','150–600 °C','Holz zerfällt zu Holzgas (Pyrolyse)','#d8a040'],['3 · Gas verbrennt','600–1100 °C','helle Flamme: CO, H₂, CH₄ verbrennen','#e8602a'],['4 · Glut','~800 °C','Holzkohle glüht flammenlos aus','#b8301a']];
      Z.forEach(([t,tem,b,c],i)=>{ const x=14+i*186;
        g+=`<rect x="${x}" y="40" width="176" height="128" rx="10" fill="${c}" opacity=".12" stroke="${c}"/>`;
        g+=T(x+88,28,t,shade(c,-0.40),13,800)+T(x+88,186,tem,shade(c,-0.40),12,800)+T(x+88,202,b,'var(--muted)',10,600);
        // Scheit
        g+=`<path d="M${x+38},150 h100 l6,-16 h-100z" fill="${i<3?lg('#d8b080','#a87a48',90):lg('#3a2a22','#1a1210',90)}"/>`;
        if(i===0) for(let k=0;k<5;k++) g+=`<circle cx="${x+50+k*18}" cy="130" r="3" fill="#9ac8f0"><animate attributeName="cy" values="130;60" dur="2.5s" begin="${k*.5}s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;0" dur="2.5s" begin="${k*.5}s" repeatCount="indefinite"/></circle>`;
        if(i===1) for(let k=0;k<5;k++) g+=`<path d="M${x+52+k*18},130 q-6,-15 0,-30 q6,-15 0,-30" stroke="#b0a090" stroke-width="5" fill="none" stroke-linecap="round" opacity="0"><animate attributeName="opacity" values="0;.7;0" dur="3s" begin="${k*.6}s" repeatCount="indefinite"/></path>`;
        if(i===2) for(let k=0;k<4;k++){ const fx=x+56+k*22; g+=`<path d="M${fx},134 c-12,-10 -10,-30 2,-56 c2,16 14,20 10,38 c6,-6 6,-12 4,-18 c8,12 6,30 -6,36z" fill="${lg('#fae060','#e0401a',90)}"><animateTransform attributeName="transform" type="translate" values="0 0;0 -4;0 2;0 0" dur="${1+k*.15}s" repeatCount="indefinite"/></path>`; }
        if(i===3) for(let k=0;k<7;k++) g+=`<circle cx="${R(x+46+rnd()*92)}" cy="${R(138+rnd()*8)}" r="${R(2+rnd()*2)}" fill="#ff7a2a"><animate attributeName="opacity" values=".3;1;.3" dur="${R(1.5+rnd())}s" repeatCount="indefinite"/></circle>`;
        if(i<3) g+=`<path d="M${x+178},104 l8,0" stroke="var(--muted)" stroke-width="2" marker-end="url(#pf)"/>`; });
      g+=T(380,226,'Feuchtes Holz bleibt lange in Phase 1 – die Energie geht ins Wasser, es qualmt und rußt.','var(--ink)',11,700);
      return {vb:'0 0 760 236',breit:true,leg:[],svg:g}; },
    holz_feuchte(){ seed=813; let g='';
      const T=(x,y,t,c,s=11,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c||'var(--ink)'};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      g+=T(190,22,'Wassergehalt und Wärme','var(--ink)',13,800);
      const B=[['frisch','50 %',50,'2,3 kWh/kg','#4a8ad8'],['1 Sommer','30 %',30,'3,4 kWh/kg','#8aa8a0'],['2 Jahre','15 %',15,'4,2 kWh/kg','#c89a4a']];
      B.forEach(([t,p,w,k,c],i)=>{ const y=50+i*58;
        g+=T(60,y+16,t,'var(--ink)',11,800,'end')+`<rect x="70" y="${y}" width="250" height="24" rx="5" fill="${lg('#e8c89a','#c89a62',0)}"/>`;
        g+=`<rect x="70" y="${y}" width="0" height="24" rx="5" fill="${c}" opacity=".75"><animate attributeName="width" from="0" to="${w*5}" dur="1.6s" begin="${i*.4}s" fill="freeze"/></rect>`;
        g+=T(330,y+16,p+' Wasser','var(--ink)',11,800,'start')+T(70,y+40,'Heizwert ca. '+k,'var(--muted)',10,600,'start'); });
      g+=T(190,226,'Ziel: unter 20 % Holzfeuchte (max. 25 %, nicht unter 11 %)','#6a3a1a',10.5,800);
      // Stapel
      const X=470; g+=T(X+130,22,'Richtig stapeln','var(--ink)',13,800);
      g+=`<path d="M${X},60 l130,-24 l130,24 z" fill="${lg('#8a8a8a','#5a5a5a',90)}"/>`;
      for(let r=0;r<6;r++) for(let c=0;c<9;c++){ const cx=X+22+c*27+(r%2)*6, cy=78+r*22; g+=`<circle cx="${cx}" cy="${cy}" r="10" fill="${lg('#e0c090','#b88a58',45)}" stroke="#6a4a2a" stroke-width="1.6"/><circle cx="${cx}" cy="${cy}" r="4" fill="none" stroke="#a87a48" stroke-width=".6"/>`; }
      g+=`<rect x="${X+6}" y="206" width="250" height="8" fill="#8a6a40"/><rect x="${X+20}" y="214" width="10" height="10" fill="#6a4a2a"/><rect x="${X+230}" y="214" width="10" height="10" fill="#6a4a2a"/>`;
      for(let k=0;k<3;k++) g+=`<path d="M${X-30},${100+k*30} h22" stroke="#7aa8d8" stroke-width="2.5" marker-end="url(#pf)"><animate attributeName="opacity" values=".2;1;.2" dur="2s" begin="${k*.4}s" repeatCount="indefinite"/></path>`;
      g+=T(X-20,92,'Wind',"#4a7aa8",10,800)+T(X+130,234,'Dach · Sonne · Wind · 10 cm vom Boden und von der Wand','var(--muted)',10,700);
      return {vb:'0 0 760 240',breit:true,leg:[],svg:g}; },
