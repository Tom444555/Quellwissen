    apfeltaschen_bild(){ seed=1601; let g='';
      const T=(x,y,t,c='var(--muted)',s=11,w=700)=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:middle;paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      const zucker=(cx,cy,r,n)=>{ let s=''; for(let i=0;i<n;i++){ const a=rnd()*6.283, d=Math.sqrt(rnd())*r, x=R(cx+Math.cos(a)*d), y=R(cy+Math.sin(a)*d*0.8); s+=`<rect x="${x}" y="${y}" width="1.8" height="1.8" fill="${rnd()<.75?'#fffdf6':'#f0e2c0'}" opacity="${R(.6+rnd()*.4)}" transform="rotate(${R(rnd()*90)} ${x} ${y})"/>`; } return s; };
      // Tasche: Dreieck mit gewölbter Oberseite, angedrückter Rand, Füllung schaut heraus
      const tasche=(x,y,s,rot)=>{ const p=[[-1,0.62],[1,0.62],[0,-0.78]].map(([a,b])=>[R(x+a*s),R(y+b*s)]);
        const [A,B,C]=p; let t=`<g transform="rotate(${rot} ${x} ${y})">`;
        t+=`<path d="M${A[0]},${A[1]} Q${x},${R(y+0.8*s)} ${B[0]},${B[1]} Q${R(x+0.7*s)},${R(y-0.1*s)} ${C[0]},${C[1]} Q${R(x-0.7*s)},${R(y-0.1*s)} ${A[0]},${A[1]} Z" fill="${lg(shade('#d89848',0.18),shade('#b8702a',-0.12),80)}" stroke="#7a4214" stroke-width="1.3"/>`;
        // Rand angedrückt (heller Saum + Gabelspuren)
        t+=`<path d="M${R(A[0]+0.16*s)},${R(A[1]-0.06*s)} Q${x},${R(y+0.62*s)} ${R(B[0]-0.16*s)},${R(B[1]-0.06*s)}" stroke="#8a4a18" stroke-width="1" fill="none" opacity=".6"/>`;
        for(let k=1;k<8;k++){ const u=k/8, ex=R(A[0]+(B[0]-A[0])*u), ey=R(A[1]+(B[1]-A[1])*u+Math.sin(u*Math.PI)*0.16*s); t+=`<path d="M${ex},${ey} l0,-${R(0.1*s)}" stroke="#8a4a18" stroke-width="1" opacity=".55"/>`; }
        // Füllung am Spalt
        t+=`<path d="M${R(x-0.18*s)},${R(y+0.36*s)} q${R(0.18*s)},${R(0.12*s)} ${R(0.36*s)},0" stroke="${lg('#f2d070','#c8902a',0)}" stroke-width="${R(0.09*s)}" fill="none" stroke-linecap="round"/>`;
        // Glanz und Bräunung
        t+=`<path d="M${R(x-0.5*s)},${R(y+0.1*s)} Q${R(x-0.1*s)},${R(y-0.5*s)} ${R(x+0.1*s)},${R(y-0.55*s)}" stroke="#f6d49a" stroke-width="${R(0.12*s)}" fill="none" stroke-linecap="round" opacity=".55"/>`;
        t+=zucker(x,y+0.05*s,0.62*s,Math.round(s*2.4))+'</g>'; return t; };
      // Teller
      const cx=230, cy=150;
      g+=`<ellipse cx="${cx}" cy="${cy+12}" rx="206" ry="70" fill="#000" opacity=".1"/>`;
      g+=`<ellipse cx="${cx}" cy="${cy}" rx="200" ry="70" fill="${lg('#fbfaf6','#dcdad2',90)}" stroke="#b8b4aa" stroke-width="1.3"/><ellipse cx="${cx}" cy="${cy+4}" rx="150" ry="48" fill="none" stroke="#d4d0c6" stroke-width="1.2"/>`;
      [[cx-110,cy+4,46,-14],[cx+108,cy+6,46,12],[cx-38,cy+20,50,4],[cx+40,cy-14,44,-6],[cx-74,cy-24,40,8]].sort((a,b)=>a[1]-b[1]).forEach(([x,y,s,r])=>g+=tasche(x,y,s,r));
      g+=zucker(cx,cy+10,170,70);
      g+=T(cx,cy+96,'Apfeltaschen mit Quark-Öl-Teig, gezuckert','var(--ink)',13,800);
      // Querschnitt rechts
      const qx=600, qy=104;
      g+=`<path d="M${qx-96},${qy+40} Q${qx},${qy-58} ${qx+96},${qy+40} Z" fill="${lg('#e0a050','#b06a24',90)}" stroke="#7a4214" stroke-width="1.3"/>`;
      g+=`<path d="M${qx-80},${qy+34} Q${qx},${qy-38} ${qx+80},${qy+34} Z" fill="${lg('#fbecc8','#f0d8a0',90)}"/>`;
      g+=`<path d="M${qx-50},${qy+30} Q${qx},${qy-8} ${qx+50},${qy+30} Z" fill="${lg('#f0d070','#d0962a',90)}"/>`;
      for(let i=0;i<10;i++){ const x=R(qx-34+rnd()*68), y=R(qy+14+rnd()*14); g+=`<rect x="${x}" y="${y}" width="7" height="6" rx="1.5" fill="${rnd()<.5?'#f8e6a0':'#e8c060'}" stroke="#b88a2a" stroke-width=".6"/>`; }
      g+=`<path d="M${qx-96},${qy+40} H${qx+96}" stroke="#7a4214" stroke-width="1.6"/>`;
      g+=zucker(qx,qy-6,80,60).replace(/<rect /g,'<rect clip-path="url(#apfq)" ');
      g+=`<defs><clipPath id="apfq"><path d="M${qx-96},${qy+40} Q${qx},${qy-58} ${qx+96},${qy+40} Q${qx},${qy-38} ${qx-96},${qy+40} Z"/></clipPath></defs>`;
      [['außen: goldbraun, Kristallzucker',qx,qy-24],['weicher Quark-Öl-Teig',qx,qy+62],['Füllung: Apfelwürfel, gekocht',qx,qy+78]].forEach(([t,x,y])=>g+=T(x,y,t,'var(--ink)',10.5,700));
      // Apfel daneben
      const ax=556, ay=210;
      g+=`<circle cx="${ax}" cy="${ay}" r="20" fill="${lg('#c8d860','#7a9a2a',45)}" stroke="#5a7a20"/><path d="M${ax},${ay-20} q2,-8 6,-10" stroke="#6a4a2a" stroke-width="2" fill="none"/><path d="M${ax+4},${ay-24} q12,-6 16,2 q-10,4 -16,-2z" fill="#6a9a30"/>`;
      g+=`<path d="M${ax+40},${ay+16} A20,20 0 0 1 ${ax+40},${ay-22} L${ax+40},${ay+16}" fill="#7a9a2a"/><path d="M${ax+42},${ay+14} A18,18 0 0 1 ${ax+42},${ay-20} Z" fill="#f8f0c8"/><ellipse cx="${ax+48}" cy="${ay-4}" rx="2.4" ry="4" fill="#5a3a1a"/>`;
      g+=T(ax+110,ay+4,'säuerliche Äpfel','var(--muted)',10.5,700);
      return {vb:'0 0 760 260',breit:true,leg:[],svg:g}; },
    apfeltaschen_leiste(){ return Z.rezept_leiste([['schuessel','1 · Quark, Milch, Öl, Zucker, Salz verrühren',{f:'#f8f4ea',zutaten:['#ffffff','#f6f0d8','#f0e070']}],['schuessel','2 · Mehl + Backpulver darübersieben',{f:'#f4ecd8',zutaten:['#ffffff','#ffffff','#f4f0e8']}],['kneten','3 · 1 Min. mit Knethaken, zur Kugel',{t:''}],['kalt','4 · Teig kühl stellen'],['topf','5 · Apfelwürfel süßen, mit Zitrone aufkochen',{t:'aufkochen'}]]); },
    apfeltaschen_backen(){ return Z.rezept_leiste([['teilen','6 · Ausrollen, Quadrate 10 × 10 cm',{n:6,t:'10 × 10 cm'}],['pinsel','7 · 1 EL Füllung, Spitzen aufeinander, andrücken'],['ofen','8 · 180 °C O/U, 15–20 Min.',{t:'180 °C'}],['gitter','9 · Kristallzucker oder Zitronenguss',{f:'#d89848',t:'nach Belieben'}]]); },
