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
      g+=T(cx,cy+96,'Apfeltaschen mit Hefeteig, goldbraun gebacken','var(--ink)',13,800);
      // Querschnitt rechts
      const qx=600, qy=104;
      g+=`<path d="M${qx-96},${qy+40} Q${qx},${qy-58} ${qx+96},${qy+40} Z" fill="${lg('#e0a050','#b06a24',90)}" stroke="#7a4214" stroke-width="1.3"/>`;
      g+=`<path d="M${qx-80},${qy+34} Q${qx},${qy-38} ${qx+80},${qy+34} Z" fill="${lg('#fbecc8','#f0d8a0',90)}"/>`;
      g+=`<path d="M${qx-50},${qy+30} Q${qx},${qy-8} ${qx+50},${qy+30} Z" fill="${lg('#f0d070','#d0962a',90)}"/>`;
      for(let i=0;i<10;i++){ const x=R(qx-34+rnd()*68), y=R(qy+14+rnd()*14); g+=`<rect x="${x}" y="${y}" width="7" height="6" rx="1.5" fill="${rnd()<.5?'#f8e6a0':'#e8c060'}" stroke="#b88a2a" stroke-width=".6"/>`; }
      g+=`<path d="M${qx-96},${qy+40} H${qx+96}" stroke="#7a4214" stroke-width="1.6"/>`;
      g+=zucker(qx,qy-6,80,60).replace(/<rect /g,'<rect clip-path="url(#apfq)" ');
      g+=`<defs><clipPath id="apfq"><path d="M${qx-96},${qy+40} Q${qx},${qy-58} ${qx+96},${qy+40} Q${qx},${qy-38} ${qx-96},${qy+40} Z"/></clipPath></defs>`;
      [['außen: goldbraun, mit Milch bestrichen',qx,qy-24],['lockerer Hefeteig',qx,qy+62],['Füllung: Apfelwürfel, eingekocht',qx,qy+78]].forEach(([t,x,y])=>g+=T(x,y,t,'var(--ink)',10.5,700));
      // Apfel daneben
      const ax=556, ay=226;
      g+=`<circle cx="${ax}" cy="${ay}" r="20" fill="${lg('#c8d860','#7a9a2a',45)}" stroke="#5a7a20"/><path d="M${ax},${ay-20} q2,-8 6,-10" stroke="#6a4a2a" stroke-width="2" fill="none"/><path d="M${ax+4},${ay-24} q12,-6 16,2 q-10,4 -16,-2z" fill="#6a9a30"/>`;
      g+=`<path d="M${ax+40},${ay+16} A20,20 0 0 1 ${ax+40},${ay-22} L${ax+40},${ay+16}" fill="#7a9a2a"/><path d="M${ax+42},${ay+14} A18,18 0 0 1 ${ax+42},${ay-20} Z" fill="#f8f0c8"/><ellipse cx="${ax+48}" cy="${ay-4}" rx="2.4" ry="4" fill="#5a3a1a"/>`;
      g+=T(ax+110,ay+4,'säuerliche Äpfel','var(--muted)',10.5,700);
      return {vb:'0 0 760 260',breit:true,leg:[],svg:g}; },
    apfeltaschen_leiste(){ return Z.rezept_leiste([['schuessel','1 · Mehl, Mulde, Hefe + Zucker, lauwarme Flüssigkeit',{f:'#f4ecd8',zutaten:['#e8d8a8','#ffffff','#f8f4ea']}],['kneten','2 · Geschmolzenes Fett zugeben, glatt kneten',{t:''}],['warm','3 · Ca. 1 Std. warm gehen lassen',{t:'1 Std.'}],['topf','4 · Äpfel köcheln, bis die Flüssigkeit verdampft ist',{t:'einkochen'}],['abkuehlen','5 · Füllung abkühlen lassen',{t:'kalt'}]]); },
    apfeltaschen_backen(){ return Z.rezept_leiste([['quadrate','6 · 3–4 mm ausrollen, Quadrate 10 × 10 cm',{t:'10 × 10 cm'}],['fuellen','7 · Füllen, zum Dreieck klappen, andrücken'],['warm','8 · Zugedeckt ca. 10 Min. nachgehen',{t:'10 Min.',f:'#e8d2a0'}],['pinsel','9 · Mit Milch bestreichen'],['ofen','10 · 175 °C Umluft, ca. 20 Min.',{t:'175 °C'}]]); },
    teigdicke_vergleich(){ seed=1602; let g='';
      const T=(x,y,t,c='var(--muted)',s=11,w=700)=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:middle;paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      const S=6, FH=18, base=168;
      [[3,'gut: durch und locker','dünn genug, gart innen durch','#3a7a2a'],[5,'Grenze: innen eher weich','bei Hefeteig noch möglich, länger backen','#a8761a'],[8,'zu dick → innen roh/weich','Hitze erreicht die Mitte zu spät','#b03a24']].forEach(([mm,a,b,c],k)=>{
        const cx=130+k*250, t=mm*S, H=2*t+FH, y0=base-H;
        g+=`<ellipse cx="${cx}" cy="${base+6}" rx="108" ry="7" fill="#000" opacity=".08"/>`;
        g+=`<rect x="${cx-104}" y="${y0}" width="208" height="${H}" rx="${R(Math.min(18,H/2))}" fill="${lg('#c8803a','#e8b468',90)}" stroke="#7a4214" stroke-width="1.4"/>`;
        g+=`<rect x="${cx-96}" y="${y0+5}" width="192" height="${H-10}" rx="${R(Math.min(14,H/2-5))}" fill="${lg('#f6e2b4','#f0d49a',90)}"/>`;
        // Poren der Krume
        for(let i=0;i<Math.round(mm*7);i++){ const x=R(cx-90+rnd()*180), yy=rnd()<.5?R(y0+7+rnd()*(t-9)):R(base-t+2+rnd()*(t-9)); g+=`<ellipse cx="${x}" cy="${yy}" rx="${R(1.2+rnd()*1.6)}" ry="${R(1+rnd())}" fill="#d8b070" opacity=".55"/>`; }
        // roher/feuchter Kern am Rand der Füllung
        if(t>22){ const r=t-22; [[y0+t-r,r],[base-t,r]].forEach(([yy,hh])=>{ g+=`<rect x="${cx-86}" y="${R(yy)}" width="172" height="${R(hh)}" fill="#efe6cc" opacity=".95"/>`; for(let j=0;j<10;j++) g+=`<path d="M${cx-80+j*17},${R(yy+hh/2)} q4,-3 8,0" stroke="#c8b890" stroke-width="1" fill="none"/>`; }); }
        // Füllung
        g+=`<rect x="${cx-84}" y="${base-t-FH}" width="168" height="${FH}" rx="6" fill="${lg('#f0d070','#d0962a',90)}"/>`;
        for(let i=0;i<9;i++){ g+=`<rect x="${R(cx-76+i*17+rnd()*4)}" y="${R(base-t-FH+5+rnd()*5)}" width="8" height="6" rx="1.5" fill="${rnd()<.5?'#f8e6a0':'#e8c060'}" stroke="#b88a2a" stroke-width=".6"/>`; }
        // Maßpfeil links
        g+=`<path d="M${cx-114},${base-t} V${base} M${cx-118},${base-t} h8 M${cx-118},${base} h8" stroke="var(--ink)" stroke-width="1.2"/>`;
        g+=T(cx,y0-12,mm+' mm Teig','var(--ink)',14,800);
        g+=T(cx,base+30,a,c,12,800)+T(cx,base+46,b,'var(--muted)',10.5,700);
      });
      if(true) g+=T(630,base-8*S*2-FH+26,'feucht-roh','#8a6a3a',10,700).replace('stroke-width:3','stroke-width:2');
      return {vb:'0 0 760 230',breit:true,leg:[],svg:g}; },
