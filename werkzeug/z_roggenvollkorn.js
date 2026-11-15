    roggenvollkorn_bild(){ seed=2201; let g='';
      const T=(x,y,t,c='var(--muted)',s=11,w=700)=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:middle;paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      const kern=(x,y,art)=>{ const w=R(rnd()*180);
        if(art==='k') return `<ellipse cx="${x}" cy="${y}" rx="5.4" ry="2.7" fill="#6f8f3c" stroke="#3c5a1c" stroke-width=".6" transform="rotate(${w} ${x} ${y})"/>`;
        if(art==='s') return `<ellipse cx="${x}" cy="${y}" rx="4.2" ry="2.1" fill="#ece4c8" stroke="#a89a70" stroke-width=".6" transform="rotate(${w} ${x} ${y})"/>`;
        if(art==='l') return `<ellipse cx="${x}" cy="${y}" rx="2.9" ry="1.5" fill="#7c4c24" stroke="#4a2a10" stroke-width=".5" transform="rotate(${w} ${x} ${y})"/>`;
        return `<ellipse cx="${x}" cy="${y}" rx="4.8" ry="3.1" fill="#f3e8c8" stroke="#c4ae7a" stroke-width=".6" transform="rotate(${w} ${x} ${y})"/>`; };
      const art=()=>{ const z=rnd(); return z<.3?'k':z<.6?'s':z<.85?'l':'h'; };
      const pore=(x,y)=>`<ellipse cx="${x}" cy="${y}" rx="${R(1.2+rnd()*2)}" ry="${R(.8+rnd()*1.3)}" fill="#7e5a34" opacity=".5"/>`;
      // Brett
      g+=`<rect x="20" y="214" width="720" height="30" rx="6" fill="${lg('#c89a64','#9a6a3a',90)}" stroke="#6a4420" stroke-width="1"/>`;
      for(let i=0;i<2;i++) g+=`<path d="M30,${224+i*10} q340,${R(rnd()*6-3)} 700,0" stroke="#8a5a2c" stroke-width=".8" fill="none" opacity=".5"/>`;
      // Kastenform mit Brot
      const fx=40, fy=122, fw=236, fh=86;
      g+=`<ellipse cx="${fx+fw/2+24}" cy="${fy+fh+12}" rx="${fw/2+36}" ry="10" fill="#000" opacity=".16"/>`;
      g+=`<path d="M${fx-4},${fy+8} Q${fx+6},${fy-50} ${fx+fw/2},${fy-54} Q${fx+fw-6},${fy-50} ${fx+fw+4},${fy+8} Z" fill="${lg('#9a6a3a','#5e3a18',90)}" stroke="#3e2410" stroke-width="1.3"/>`;
      g+=`<path d="M${fx+30},${fy-30} Q${fx+fw/2},${fy-54} ${fx+fw-40},${fy-32}" stroke="#c89a62" stroke-width="7" fill="none" stroke-linecap="round" opacity=".35"/>`;
      for(let i=0;i<46;i++){ const x=R(fx+18+rnd()*(fw-36)); const t=(x-fx)/fw; const y=R(fy-6-Math.sin(t*Math.PI)*40*rnd()); g+=kern(x,y,art()); }
      g+=`<path d="M${fx-10},${fy} L${fx+4},${fy+fh} H${fx+fw-4} L${fx+fw+10},${fy} Z" fill="${lg('#a8aeb6','#5e646c',90)}" stroke="#3a3e44" stroke-width="1.4"/>`;
      g+=`<path d="M${fx-14},${fy} H${fx+fw+14}" stroke="#3a3e44" stroke-width="4" stroke-linecap="round"/>`;
      g+=`<path d="M${fx+20},${fy+18} H${fx+fw-20}" stroke="#d0d6dc" stroke-width="2" opacity=".5"/>`;
      // angeschnittener Laib
      const lx=372, ly=152;
      g+=`<path d="M${lx},${ly+52} V${ly-10} Q${lx+6},${ly-62} ${lx+66},${ly-66} L${lx+168},${ly-66} Q${lx+222},${ly-60} ${lx+226},${ly-10} V${ly+52} Z" fill="${lg('#96663a','#5a3616',90)}" stroke="#3e2410" stroke-width="1.3"/>`;
      for(let i=0;i<34;i++) g+=kern(R(lx+80+rnd()*132),R(ly-60+rnd()*18),art());
      g+=`<path d="M${lx},${ly+52} V${ly-10} Q${lx+6},${ly-62} ${lx+66},${ly-66} L${lx+66},${ly+52} Z" fill="#4e3014"/>`;
      g+=`<path d="M${lx+6},${ly+48} V${ly-8} Q${lx+12},${ly-55} ${lx+62},${ly-59} V${ly+48} Z" fill="${lg('#c6a074','#ad8454',0)}"/>`;
      // Scheibe davor
      const sx=lx-34, sy=ly+4;
      g+=`<path d="M${sx-36},${sy+56} V${sy-4} Q${sx-32},${sy-52} ${sx+16},${sy-54} Q${sx+44},${sy-50} ${sx+46},${sy-4} V${sy+56} Z" fill="#5a3818" stroke="#3a2410" stroke-width="1.2"/>`;
      g+=`<path d="M${sx-30},${sy+50} V${sy-2} Q${sx-26},${sy-45} ${sx+16},${sy-47} Q${sx+38},${sy-43} ${sx+40},${sy-2} V${sy+50} Z" fill="${lg('#caa67a','#b08a5a',0)}"/>`;
      for(let i=0;i<56;i++) g+=pore(R(sx-24+rnd()*58),R(sy-34+rnd()*80));
      for(let i=0;i<13;i++) g+=kern(R(sx-20+rnd()*52),R(sy-28+rnd()*70),['k','s','l'][i%3]);
      for(let i=0;i<30;i++) g+=pore(R(lx+12+rnd()*46),R(ly-40+rnd()*84));
      for(let i=0;i<8;i++) g+=kern(R(lx+16+rnd()*40),R(ly-34+rnd()*74),['k','s','l'][i%3]);
      g+=T(lx+70,266,'Anschnitt: dichte, saftige Krume mit Kernen','var(--muted)',10.5,700);
      g+=T(fx+fw/2,266,'Roggen-Vollkornbrot in der Kastenform','var(--ink)',13,800);
      // Schälchen mit Kernen
      const schale=(x,y,a,name)=>{ let s=`<ellipse cx="${x}" cy="${y}" rx="34" ry="12" fill="${lg('#eef0ea','#c2c8c0',90)}" stroke="#7a8078" stroke-width="1.1"/><ellipse cx="${x}" cy="${y-2}" rx="27" ry="8" fill="${a==='k'?'#52702a':a==='s'?'#cfc6a4':'#5c3616'}" opacity=".9"/>`;
        for(let i=0;i<16;i++) s+=kern(R(x-21+rnd()*42),R(y-6+rnd()*8),a);
        return s+T(x,y+26,name,'var(--muted)',10,700); };
      g+=schale(684,58,'s','Sonnenblume')+schale(684,118,'k','Kürbis')+schale(684,178,'l','Leinsamen');
      return {vb:'0 0 760 280',breit:true,leg:[],svg:g}; },
    roggenvollkorn_leiste(){ return Z.rezept_leiste([['schuessel','1 · Beide Mehle, Hefe, Salz mischen',{zutaten:['#b89a70','#d8c090','#ffffff'],f:'#c8ac80'}],['kneten','2 · Honig + Wasser: klebrig rühren',{t:'450 ml'}],['kerne','3 · Kerne und Leinsamen dazu',{t:'je 2 EL'}],['warm','4 · 60 Min. warm gehen',{t:'60 Min.',f:'#b89468'}],['kasten','5 · In die Form, bestreuen, 20 Min. ruhen',{t:'20 Min.',auf:true,f:'#b89468'}],['ofen','6 · 200 °C O/U, 50–55 Min.',{t:'200 °C'}],['gitter','7 · Ganz auskühlen lassen',{f:'#a8703a'}]]); },
