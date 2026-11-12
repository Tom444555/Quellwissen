    pohlmannraf_muster(){ seed=7901; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3px">${t}</text>`;
      g+=T(380,18,'Beobachten – radikalisieren – nutzen (Darstellung laut Pohlmann, schematisch)',undefined,12.5,800);
      const S=[
        ['🌱 Bewegung entsteht','#6f9a52',['Protest gegen Schah,','Vietnam, Altnazis','„organisch“ [0:55]'],['Studenten 1967','Bewegung 2. Juni','Peacenik-Szene']],
        ['👂 Beobachten','#4a7aa8',['V-Leute einschleusen:','wer führt, was','wird gedacht? [0:40]'],['Urbach in der Kommune 1','Weingrabers Wohnung ❓','Stammheim abgehört']],
        ['🔥 Radikalisieren','#c0703e',['Waffen, Sprengstoff,','Anleitung zur Gewalt','[0:19], [0:35]'],['Molotowcocktails','Bombe 9.11.1969 📚','Rote Brigaden [0:50]']],
        ['🎯 Nutzen','#8a5a8a',['Gruppe als Schreckbild','„abräumen“ – oder','für Ziele einsetzen [0:51]'],['Manson als Schreckbild','Moro-Mord [1:39]','RAF im Kriegsfall ❓']]];
      S.forEach(([t,c,L,B],i)=>{ const x=22+i*186, y=44, w=160;
        g+=`<g opacity="0"><rect x="${x}" y="${y}" width="${w}" height="104" rx="12" fill="${lg(shade(c,0.82),shade(c,0.62),90)}" stroke="${c}" stroke-width="1.5"/>`;
        g+=T(x+w/2,y+22,t,shade(c,-0.45),12,800);
        L.forEach((s,k)=>{ g+=T(x+w/2,y+46+k*17,s,'var(--ink)',9.5,650); });
        g+=`<rect x="${x+8}" y="${y+118}" width="${w-16}" height="72" rx="8" fill="${shade(c,0.9)}" stroke="${shade(c,0.35)}" stroke-width="0.9" stroke-dasharray="4 3"/>`;
        g+=T(x+w/2,y+133,'Beispiele im Gespräch','var(--muted)',8.5,700);
        B.forEach((s,k)=>{ g+=T(x+w/2,y+151+k*15,s,shade(c,-0.4),9,650); });
        if(i<3){ const ax=x+w+3; g+=`<path d="M${ax},${y+52} l18,0" stroke="var(--line)" stroke-width="2" fill="none"/><path d="M${ax+18},${y+46} l7,6 l-7,6 z" fill="var(--line)"/>`; }
        g+=`<animate attributeName="opacity" from="0" to="1" dur=".45s" begin="${(0.2+i*0.35).toFixed(2)}s" fill="freeze"/></g>`; });
      const ly=258;
      g+=`<g opacity="0"><path d="M690,236 C690,${ly+20} 540,${ly+22} 380,${ly+22} C230,${ly+22} 290,${ly+8} 290,236" stroke="#a88a3c" stroke-width="1.6" stroke-dasharray="5 4" fill="none"/><path d="M284,242 l6,-8 l6,8 z" fill="#a88a3c"/>`;
      g+=T(480,ly+16,'kein Masterplan: „Pläne funktionieren nie so, wie man es vorhat“ – nachjustieren [0:48]',shade('#a88a3c',-0.45),9.5,750);
      g+=`<animate attributeName="opacity" from="0" to="1" dur=".45s" begin="1.7s" fill="freeze"/></g>`;
      return {vb:'0 0 760 300',breit:true,leg:[],svg:g}; },
    pohlmannraf_belege(){ seed=7902; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3px">${t}</text>`;
      g+=T(380,18,'Was amtlich belegt ist – Ereignisse und spätere Klärung (belegte Daten)',undefined,12.5,800);
      const x0=60, x1=720, j0=1960, j1=2030, X=j=>R(x0+(j-j0)/(j1-j0)*(x1-x0)), ay=172;
      g+=`<path d="M${x0-10},${ay} L${x1+12},${ay}" stroke="var(--line)" stroke-width="2"/><path d="M${x1+12},${ay-5} l8,5 l-8,5 z" fill="var(--line)"/>`;
      for(let j=1960;j<=2030;j+=10){ g+=`<path d="M${X(j)},${ay-4} l0,8" stroke="var(--line)" stroke-width="1.2"/>`+T(X(j),ay+16,String(j),'var(--muted)',8.5,650); }
      const U=[ // unten: Ereignisse
        [1964,'1964 Tonkin: gemeldeter Angriff 4.8.','#c0703e'],
        [1967,'1967 Kurras freigesprochen','#c0703e'],
        [1969,'1969 Urbach liefert Bombe (9.11.)','#c0703e'],
        [1971,'1971 Urbach enttarnt, neue Identität','#c0703e'],
        [1973,'1973 MKUltra-Akten vernichtet','#c0703e'],
        [1977,'1977 Senat: MKUltra – 149 Unterprojekte','#c0703e']];
      const O=[ // oben: spätere Klärungen
        [1990,'1990 EP: Gladio-Netze auflösen','#4a7aa8'],
        [2003,'2003 BVerfG: NPD-Verfahren eingestellt (V-Leute)','#4a7aa8'],
        [2005,'2005 NSA: Angriff 4.8.1964 gab es nicht','#4a7aa8'],
        [2009,'2009 Stasi-Akte: Kurras war IM','#4a7aa8'],
        [2012,'2012 OLG Stuttgart: Becker verurteilt','#4a7aa8'],
        [2026,'2026 LG Verden: Klette 13 Jahre','#4a7aa8']];
      U.forEach(([j,t,c],k)=>{ const y=ay+34+(U.length-1-k)*20, x=X(j);
        g+=`<g opacity="0"><path d="M${x},${ay} L${x},${y-4}" stroke="${c}" stroke-width="1" stroke-dasharray="2 2"/><circle cx="${x}" cy="${ay}" r="4.5" fill="${c}" stroke="${shade(c,-0.3)}" stroke-width="1"/>`;
        g+=T(x+4,y,t,shade(c,-0.45),9,700,'start');
        g+=`<animate attributeName="opacity" from="0" to="1" dur=".35s" begin="${(0.2+k*0.18).toFixed(2)}s" fill="freeze"/></g>`; });
      O.forEach(([j,t,c],k)=>{ const y=ay-22-k*20, x=X(j);
        g+=`<g opacity="0"><path d="M${x},${ay} L${x},${y+4}" stroke="${c}" stroke-width="1" stroke-dasharray="2 2"/><circle cx="${x}" cy="${ay}" r="4.5" fill="${c}" stroke="${shade(c,-0.3)}" stroke-width="1"/>`;
        g+=T(x-4,y,t,shade(c,-0.45),9,700,'end');
        g+=`<animate attributeName="opacity" from="0" to="1" dur=".35s" begin="${(1.3+k*0.18).toFixed(2)}s" fill="freeze"/></g>`; });
      g+=`<g opacity="0"><rect x="30" y="30" width="245" height="76" rx="10" fill="${lg('#efe4c8','#e2d2a8',90)}" stroke="#a88a3c" stroke-width="1.2"/>`;
      g+=T(152,47,'Abstand bis zur amtlichen Klärung',shade('#a88a3c',-0.5),10,800);
      g+=T(40,64,'Tonkin 1964 → NSA 2005: 41 Jahre','var(--ink)',9,650,'start');
      g+=T(40,80,'Ohnesorg 1967 → Kurras-Akte 2009: 42 Jahre','var(--ink)',9,650,'start');
      g+=T(40,96,'Urbach-Bombe 1969 → bekannt 2005: 36 Jahre','var(--ink)',9,650,'start');
      g+=`<animate attributeName="opacity" from="0" to="1" dur=".45s" begin="2.5s" fill="freeze"/></g>`;
      g+=T(712,ay+34,'● Ereignis','#c0703e',8.5,700,'end')+T(712,ay+48,'● spätere Klärung','#4a7aa8',8.5,700,'end');
      return {vb:'0 0 760 310',breit:true,leg:[],svg:g}; },
