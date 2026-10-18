    frost_kristalle(){ seed=701; let g='';
      const zelle=(ox,oy,schnell)=>{ let s='';
        for(let r=0;r<3;r++) for(let c=0;c<3;c++){ const x=ox+c*62, y=oy+r*52;
          s+=`<path d="M${x+4},${y+4} h52 v42 h-52 z" fill="${lg('#d8ecc0','#a8cc88',90)}" stroke="#5a8a3a" stroke-width="2.2" rx="6"/>`;
          if(!schnell&&(r+c)%2===0) s+=`<path d="M${x+52},${y+6} l10,8" stroke="#c03030" stroke-width="2"/>`; }
        const n=schnell?60:7;
        for(let i=0;i<n;i++){ const x=ox+6+rnd()*178, y=oy+6+rnd()*146, L=schnell?3+rnd()*2:16+rnd()*14, a=rnd()*60;
          let k=''; for(let j=0;j<3;j++){ const aa=(a+j*60)*Math.PI/180; k+=`M${R(x-Math.cos(aa)*L)},${R(y-Math.sin(aa)*L)} L${R(x+Math.cos(aa)*L)},${R(y+Math.sin(aa)*L)} `; }
          s+=`<path d="${k}" stroke="#4a9ad8" stroke-width="${schnell?1.4:2.6}" stroke-linecap="round" opacity="0"><animate attributeName="opacity" values="0;1;1" keyTimes="0;.5;1" dur="${schnell?1.2:4}s" begin="${R(rnd()*(schnell?1:3))}s" fill="freeze"/></path>`; }
        return s; };
      g+=`<text x="105" y="22" style="fill:#a03a2a;font:800 13px var(--label);text-anchor:middle">langsam gefroren</text>`+zelle(10,34,false);
      g+=`<text x="105" y="210" style="fill:var(--muted);font:600 11px var(--label);text-anchor:middle">große Kristalle zerstechen Zellen</text>`;
      g+=`<text x="345" y="22" style="fill:#2e6a9a;font:800 13px var(--label);text-anchor:middle">schnell gefroren</text>`+zelle(250,34,true);
      g+=`<text x="345" y="210" style="fill:var(--muted);font:600 11px var(--label);text-anchor:middle">kleine Kristalle, Zellen bleiben heil</text>`;
      // Gefrierkurve
      const X0=500,Y0=40,W=200,H=150, y=t=>R(Y0+H*(20-t)/40);
      g+=`<text x="${X0+W/2}" y="22" style="fill:var(--ink);font:800 13px var(--label);text-anchor:middle">Gefrierkurve</text>`;
      g+=`<path d="M${X0},${Y0} V${Y0+H} H${X0+W}" stroke="var(--ink)" fill="none"/>`;
      [[20,'+20 °C'],[0,'0 °C'],[-5,'−5 °C'],[-18,'−18 °C']].forEach(([t,l])=>g+=`<text x="${X0-6}" y="${y(t)+4}" style="fill:var(--muted);font:700 10px var(--label);text-anchor:end">${l}</text><path d="M${X0},${y(t)} h${W}" stroke="var(--line)" stroke-dasharray="2 3"/>`);
      g+=`<rect x="${X0+40}" y="${y(0)}" width="80" height="${y(-5)-y(0)}" fill="#4a9ad8" opacity=".15"/><text x="${X0+80}" y="${y(-5)+12}" style="fill:#2e6a9a;font:700 9.5px var(--label);text-anchor:middle">Kristallisationszone</text>`;
      const d=`M${X0},${y(18)} C${X0+20},${y(6)} ${X0+30},${y(0)} ${X0+40},${y(-1)} L${X0+120},${y(-4)} C${X0+140},${y(-10)} ${X0+170},${y(-17)} ${X0+W},${y(-18)}`;
      g+=`<path d="${d}" stroke="#2e6a9a" stroke-width="3" fill="none"/><circle r="5" fill="#c03030"><animateMotion dur="5s" repeatCount="indefinite" path="${d}"/></circle>`;
      g+=`<text x="${X0+W/2}" y="${Y0+H+18}" style="fill:var(--muted);font:600 10px var(--label);text-anchor:middle">Zeit → je kürzer die blaue Zone, desto besser</text>`;
      return {vb:'0 0 720 220', breit:true, leg:[], svg:g}; },
    frost_brand(){ seed=702; let g='';
      const beutel=(ox,luft)=>{ let s=`<path d="M${ox},40 h170 v130 q0,14 -14,14 h-142 q-14,0 -14,-14 z" fill="#eef4fa" opacity=".55" stroke="#8aa8c0" stroke-width="2"/>`;
        s+=`<rect x="${ox+(luft?30:8)}" y="${luft?96:52}" width="${luft?110:154}" height="${luft?70:118}" rx="10" fill="${lg('#e89a8a','#b85a4a',90)}"/>`;
        if(luft){ s+=`<rect x="${ox+30}" y="96" width="110" height="14" rx="6" fill="#d8d0c8" opacity=".9"/><text x="${ox+85}" y="128" style="fill:#fff;font:800 11px var(--label);text-anchor:middle">grau, trocken</text>`;
          for(let i=0;i<10;i++){ const x=ox+36+rnd()*100; s+=`<circle cx="${R(x)}" cy="96" r="2.2" fill="#9ac8f0"><animate attributeName="cy" values="96;48;60" dur="${R(2.5+rnd()*2)}s" begin="${R(rnd()*2)}s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;1;0" dur="${R(2.5+rnd()*2)}s" repeatCount="indefinite"/></circle>`; }
          for(let i=0;i<14;i++) s+=`<path d="M${R(ox+12+rnd()*146)},${R(46+rnd()*10)} l3,-3 m-3,0 l3,3" stroke="#6a9ac8" stroke-width="1.2"/>`; }
        return s; };
      g+=`<text x="95" y="24" style="fill:#a03a2a;font:800 13px var(--label);text-anchor:middle">✗ viel Luft im Beutel</text>`+beutel(10,true)+`<text x="95" y="204" style="fill:var(--muted);font:600 11px var(--label);text-anchor:middle">Eis sublimiert, setzt sich als Reif ab</text>`;
      g+=`<text x="305" y="24" style="fill:#2e6a1e;font:800 13px var(--label);text-anchor:middle">✓ Luft herausgedrückt</text>`+beutel(220,false)+`<text x="305" y="204" style="fill:var(--muted);font:600 11px var(--label);text-anchor:middle">kein Raum zum Austrocknen</text>`;
      g+=`<text x="480" y="60" style="fill:var(--ink);font:800 12px var(--label)">Gefrierbrand =</text><text x="480" y="80" style="fill:var(--ink);font:600 11.5px var(--label)">Wassermoleküle gehen direkt</text><text x="480" y="96" style="fill:var(--ink);font:600 11.5px var(--label)">von Eis zu Dampf. Zurück bleibt</text><text x="480" y="112" style="fill:var(--ink);font:600 11.5px var(--label)">poröses Gewebe; Sauerstoff</text><text x="480" y="128" style="fill:var(--ink);font:600 11.5px var(--label)">dringt ein → Fett wird ranzig.</text><text x="480" y="152" style="fill:#2e6a1e;font:700 11.5px var(--label)">Nicht giftig – nur zäh und fade:</text><text x="480" y="168" style="fill:#2e6a1e;font:700 11.5px var(--label)">Stellen großzügig wegschneiden.</text>`;
      return {vb:'0 0 680 214', breit:true, leg:[], svg:g}; },
