    aloe(){ seed=231; let g=erde(318,62);
      const ab=(x,y,len,w,a,f)=>{ const P=[]; const n=14; for(let i=0;i<=n;i++){ const t=i/n, ww=w*Math.pow(1-t,0.85)*(t<0.08?0.8+t*2.5:1); P.push([t*len,-ww]); } const Q=[]; for(let i=n;i>=0;i--){ const t=i/n, ww=w*Math.pow(1-t,0.85)*(t<0.08?0.8+t*2.5:1); Q.push([t*len,ww]); }
        let d='M'+rot([P[0]],x,y,a)[0].map(R).join(','); P.slice(1).forEach(([px,py],i)=>{ const [ax,ay]=rot([[px,py]],x,y,a)[0]; d+=` L${R(ax)},${R(ay)}`; if(i%1===0&&i<n-1){ const [tx,ty]=rot([[px+2,py-3.2]],x,y,a)[0]; d+=` L${R(tx)},${R(ty)} L${R(ax)},${R(ay)}`; } });
        Q.forEach(([px,py],i)=>{ const [ax,ay]=rot([[px,py]],x,y,a)[0]; d+=` L${R(ax)},${R(ay)}`; if(i>0&&i<n-1){ const [tx,ty]=rot([[px-2,py+3.2]],x,y,a)[0]; d+=` L${R(tx)},${R(ty)} L${R(ax)},${R(ay)}`; } }); d+='Z';
        let s=`<path d="${d}" fill="${lg(shade(f,-0.3),shade(f,0.22),a)}" stroke="${shade(f,-0.55)}" stroke-width=".9"/>`;
        const [m1,m2]=rot([[len*0.05,0],[len*0.92,0]],x,y,a); s+=`<path d="M${R(m1[0])},${R(m1[1])} L${R(m2[0])},${R(m2[1])}" stroke="${shade(f,0.35)}" stroke-width="${R(w*0.25)}" stroke-linecap="round" opacity=".35"/>`;
        for(let i=0;i<6;i++){ const t=0.15+rnd()*0.6; const [fx,fy]=rot([[t*len,(rnd()-.5)*w*1.1*(1-t)]],x,y,a)[0]; s+=`<ellipse cx="${R(fx)}" cy="${R(fy)}" rx="2.6" ry="1.2" fill="#e8efe0" opacity=".55" transform="rotate(${a} ${R(fx)} ${R(fy)})"/>`; }
        return s; };
      // Rosette
      const B=[[-170,150,30],[-10,150,30],[-150,170,32],[-30,170,32],[-125,180,34],[-55,180,34],[-105,165,33],[-75,165,33],[-90,150,30]];
      B.forEach(([a,len,w],i)=>g+=ab(150,300,len,w,a,['#6f9a6a','#7aa476','#668f62'][i%3]));
      // Bluetenstand
      g+=stiel('M168,250 C172,150 178,40 184,-50',3.2,'#8a9a5a');
      for(let i=0;i<16;i++){ const y=-52+i*8, x=184-(i*0.2); for(const s of [-1,1]){ const xx=x+s*(4+i*0.25); g+=`<path d="M${R(x)},${y} Q${R(xx+s*4)},${y+3} ${R(xx+s*3)},${y+14}" stroke="#d8a020" stroke-width="4.2" fill="none" stroke-linecap="round" opacity="${i<4?0.75:1}"/><circle cx="${R(xx+s*3)}" cy="${y+14}" r="1.4" fill="#f8e070"/>`; } }
      // Ableger
      g+=stiel('M150,312 C200,320 230,316 250,310',2.4,'#b8a070')+ab(252,308,40,9,-120,'#7aa476')+ab(252,308,44,10,-70,'#6f9a6a');
      g+=fasern(150,318,10,40,110,'#c9b48a',.7);
      g+=mk(42,212,1)+mk(222,-20,2)+mk(266,286,3)+mk(150,356,4);
      return {vb:'0 -70 300 450', leg:['Dickfleischige, bläulich grüne Blätter mit weichen Randzähnen, in einer Rosette','Blütenstand: bis 90 cm hohe Traube mit gelben Röhrenblüten (im Zimmer selten)','Kindel (Ableger) an Ausläufern – so vermehrt man Aloe am einfachsten','Flaches Wurzelwerk; braucht durchlässige, sandige Erde'], svg:g}; },
    aloe_quer(){ let g='';
      const W=420,H=230, cx=210;
      // aeussere Form: V-foermiger Blattquerschnitt
      const aussen=`M40,70 Q210,40 380,70 Q300,180 210,205 Q120,180 40,70 Z`;
      const latex=`M58,76 Q210,50 362,76 Q292,170 210,192 Q128,170 58,76 Z`;
      const gel=`M74,82 Q210,62 346,82 Q284,158 210,178 Q136,158 74,82 Z`;
      g+=`<path d="${aussen}" fill="${lg('#3f7a3c','#7aaa66',90)}" stroke="#244a22" stroke-width="1.4"/>`;
      g+=`<path d="${latex}" fill="#e8c63a" stroke="#b08a1a" stroke-width=".8"/>`;
      g+=`<path d="${gel}" fill="${lg('#e6f2e2','#cfe3cc',90)}" stroke="#a8c4a2" stroke-width=".8" opacity=".95"/>`;
      // Leitbuendel als Punkte entlang der Latexschicht
      const pts=[]; for(let i=0;i<=24;i++){ const t=i/24; const x=62+t*296; const top=76-Math.sin(t*Math.PI)*14; pts.push([x,top+2]); } for(let i=1;i<24;i++){ const t=i/24; const x=62+t*296; const bot=76+(t<0.5?t*2:(1-t)*2)*112; pts.push([x,bot-3]); }
      pts.forEach(([x,y])=>g+=`<circle cx="${R(x)}" cy="${R(y)}" r="2.2" fill="#c87a10" stroke="#8a5a08" stroke-width=".5"/>`);
      // Gelzellen
      for(let i=0;i<40;i++){ const x=110+rnd()*200, y=86+rnd()*70; if(Math.abs(x-210)>(160-(y-80))*0.9) continue; g+=`<ellipse cx="${R(x)}" cy="${R(y)}" rx="${R(6+rnd()*5)}" ry="${R(4+rnd()*3)}" fill="none" stroke="#b8d0b0" stroke-width=".6"/>`; }
      // Tropfen gelber Saft
      g+=`<path d="M362,80 q10,14 4,24 q-8,8 -12,-2 q-2,-10 8,-22z" fill="#e8b020" stroke="#a87808"/>`;
      g+=mk(40,52,1)+mk(388,96,2)+mk(210,118,3)+mk(300,150,4);
      return {vb:'0 0 420 230', breit:true, leg:['Grüne Außenhaut (Epidermis mit dicker Wachsschicht)','Gelber Blattsaft (Latex) in den Zellen an den Leitbündeln: enthält Aloin – stark abführend','Durchsichtiges Gel (Speichergewebe): Wasser, Acemannan und andere Polysaccharide','Leitbündel – beim Filetieren den gelben Saft zuerst ablaufen lassen'], svg:g}; },
