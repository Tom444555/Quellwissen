    leppe_lernweg(){ seed=8101; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3px">${t}</text>`;
      const F=(i,d)=>`<animate attributeName="opacity" from="0" to="1" dur=".45s" begin="${d.toFixed(2)}s" fill="freeze"/>`;
      g+=T(380,18,'Schule heute und „Schule der Zukunft“ (Darstellung laut Leppe, schematisch)',undefined,12.5,800);
      // linke Spalte: heute
      const L=[['😟 Druck · Angst · Strafe','#b8674a'],['📚 Stoff für alle gleich','#a8885a'],['📝 Prüfung, dann vergessen','#9a7a6a']];
      g+=`<g opacity="0"><rect x="20" y="34" width="250" height="196" rx="14" fill="${lg('#f3e2d6','#e9cfbd',90)}" stroke="#b8674a" stroke-width="1.4"/>`+T(145,54,'Schule heute',shade('#b8674a',-0.45),12.5,800);
      L.forEach(([t,c],k)=>{ const y=68+k*46; g+=`<rect x="40" y="${y}" width="210" height="32" rx="9" fill="${shade(c,0.75)}" stroke="${c}" stroke-width="1"/>`+T(145,y+20,t,'var(--ink)',10,700);
        if(k<2) g+=`<path d="M145,${y+33} l0,12" stroke="${c}" stroke-width="1.6"/><path d="M140,${y+40} l5,6 l5,-6" fill="none" stroke="${c}" stroke-width="1.6"/>`; });
      g+=T(145,222,'„1,5 % bleiben“ [0:36] ❓','var(--muted)',9,650);
      g+=F(0,0.1)+`</g>`;
      // Pfeil
      g+=`<g opacity="0"><path d="M282,132 C320,132 330,132 368,132" stroke="#6a8a5a" stroke-width="2.4" fill="none" stroke-dasharray="6 4"/><path d="M362,125 l10,7 l-10,7" fill="none" stroke="#6a8a5a" stroke-width="2.4"/>`+T(325,122,'Schritt 1',shade('#6a8a5a',-0.4),9.5,800)+T(325,150,'Lehrplan bleibt',`var(--muted)`,8.5,650)+F(0,0.6)+`</g>`;
      // rechte Spalte: Zukunft
      g+=`<g opacity="0"><rect x="380" y="34" width="360" height="196" rx="14" fill="${lg('#e2eedb','#cfe2c3',90)}" stroke="#6a8a5a" stroke-width="1.4"/>`+T(560,54,'„Schule der Zukunft“ – Schritt 1',shade('#6a8a5a',-0.5),12.5,800);
      const K=[['🤝 Beziehung','#7a9a6a'],['👤 Vorbild','#7a9a6a'],['🖼️ Bild','#6a8aa8'],['😂 lustig','#c8a24a'],['❤️ emotional','#c0705a'],['🔗 verknüpft','#8a7aa8']];
      K.forEach(([t,c],k)=>{ const x=394+(k%3)*114, y=68+Math.floor(k/3)*38; g+=`<rect x="${x}" y="${y}" width="104" height="28" rx="14" fill="${shade(c,0.78)}" stroke="${c}" stroke-width="1"/>`+T(x+52,y+18,t,'var(--ink)',9.5,700); });
      g+=T(560,158,'gleicher Stoff „50–90 % schneller“ [1:25]',shade('#6a8a5a',-0.45),10,800);
      const Z=[['⚽ Sport','#6a9a8a'],['🎵 Musik','#8a7aa8'],['🎨 Kunst','#c8a24a'],['🌿 Interessen','#7a9a6a']];
      Z.forEach(([t,c],k)=>{ const x=398+k*84; g+=`<rect x="${x}" y="176" width="76" height="26" rx="8" fill="${shade(c,0.8)}" stroke="${c}" stroke-width="1"/>`+T(x+38,193,t,'var(--ink)',9,700); });
      g+=T(560,220,'gewonnene Zeit – frei nutzbar [1:26–1:27]','var(--muted)',8.8,650);
      g+=F(0,1.0)+`</g>`;
      // fünf Hauptfächer
      const H=['✍️ Lesen · Schreiben · Rechnen','🏃 Körper kennen','🫀 Seele kennen','🌳 mit der Natur','🧠 Lernen lernen'];
      g+=`<g opacity="0">`+T(380,252,'Leppes fünf Hauptfächer [1:45–1:46]',shade('#8a6a4a',-0.3),11,800);
      H.forEach((t,k)=>{ const x=22+k*146; g+=`<rect x="${x}" y="262" width="138" height="28" rx="9" fill="${lg('#f1e6cf','#e6d5b1',90)}" stroke="#a88a5a" stroke-width="1"/>`+T(x+69,280,t,'var(--ink)',8.8,700); });
      g+=F(0,1.5)+`</g>`;
      return {vb:'0 0 760 300',breit:true,leg:[],svg:g}; },
    leppe_pflicht(){ seed=8102; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3px">${t}</text>`;
      g+=T(380,18,'Schulpflicht (Deutschland) und Unterrichtspflicht (Österreich) – Stationen (belegte Daten)',undefined,12,800);
      // nicht lineare Achse: Abschnitte
      const J=[1717,1763,1938,1949,2006,2021,2025], X=[78,170,270,370,480,590,700];
      const ay=150;
      g+=`<path d="M30,${ay} L735,${ay}" stroke="var(--line)" stroke-width="2"/>`;
      g+=`<path d="M214,${ay-6} l8,12 M222,${ay-6} l8,12" stroke="var(--muted)" stroke-width="1.2"/>`;
      J.forEach((j,i)=>{ g+=`<circle cx="${X[i]}" cy="${ay}" r="5" fill="#a88a5a" stroke="${shade('#a88a5a',-0.4)}" stroke-width="1"/>`+T(X[i],ay+20,j,'var(--muted)',9.5,800); });
      const DE=[ [0,'Preußen: Edikt','Schulpflicht 5–12 J.'], [1,'Preußen: General-','landschulreglement'], [2,'Reichsschul-','pflichtgesetz'], [3,'Grundgesetz:','Schule = Landesrecht'], [4,'BVerfG + EGMR:','Schulpflicht bestätigt'], [5,'BVerfG: „Recht auf','schulische Bildung“'] ];
      DE.forEach(([i,a,b],k)=>{ const y= (k%2? 62:94), x=X[i];
        g+=`<g opacity="0"><path d="M${x},${ay-6} L${x},${y+18}" stroke="#4a7aa8" stroke-width="1.2" stroke-dasharray="3 3"/>`;
        g+=`<rect x="${x-56}" y="${y-14}" width="112" height="32" rx="8" fill="${lg('#dfe8f2','#c9d9ea',90)}" stroke="#4a7aa8" stroke-width="1"/>`+T(x,y-1,a,shade('#4a7aa8',-0.5),8.6,800)+T(x,y+12,b,'var(--ink)',8.4,650);
        g+=`<animate attributeName="opacity" from="0" to="1" dur=".4s" begin="${(0.2+k*0.25).toFixed(2)}s" fill="freeze"/></g>`; });
      g+=T(30,40,'🇩🇪 Deutschland',shade('#4a7aa8',-0.4),10.5,800,'start');
      const AT=[ [5,'2021/22:','7.515 Kinder (≈1 %)'], [6,'2024/25:','rund 1.800 Kinder'] ];
      g+=T(30,284,'🇦🇹 Österreich: häuslicher Unterricht + Externistenprüfung',shade('#b8674a',-0.4),10.5,800,'start');
      AT.forEach(([i,a,b],k)=>{ const y=206+k*34, x=X[i];
        g+=`<g opacity="0"><path d="M${x},${ay+26} L${x},${y-14}" stroke="#b8674a" stroke-width="1.2" stroke-dasharray="3 3"/>`;
        g+=`<rect x="${x-58}" y="${y-14}" width="116" height="32" rx="8" fill="${lg('#f3e0d6','#ead0c2',90)}" stroke="#b8674a" stroke-width="1"/>`+T(x,y-1,a,shade('#b8674a',-0.5),8.6,800)+T(x,y+12,b,'var(--ink)',8.4,650);
        g+=`<animate attributeName="opacity" from="0" to="1" dur=".4s" begin="${(1.8+k*0.3).toFixed(2)}s" fill="freeze"/></g>`; });
      g+=`<g opacity="0"><rect x="30" y="196" width="250" height="40" rx="9" fill="${shade('#b8674a',0.85)}" stroke="#b8674a" stroke-width="0.9"/>`+T(155,212,'vor 2020: jährlich ca. 2.300–2.600 Kinder','var(--ink)',8.6,700)+T(155,226,'(≈0,3 % der Schulpflichtigen)','var(--muted)',8.2,650)+`<animate attributeName="opacity" from="0" to="1" dur=".4s" begin="1.6s" fill="freeze"/></g>`;
      return {vb:'0 0 760 300',breit:true,leg:[],svg:g}; },
