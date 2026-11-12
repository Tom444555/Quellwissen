    masterpeace_ebenen(){ seed=5201; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3px">${t}</text>`;
      g+=T(380,18,'Wie gesteuert wird – drei Ebenen (Darstellung laut Regenauer, schematisch)',undefined,12.5,800);
      g+=`<g opacity="0"><rect x="250" y="30" width="260" height="34" rx="17" fill="${lg('#e8d9b0','#d9c48e',90)}" stroke="#a88a3c" stroke-width="1.4"/>`+T(380,47,'„Superclass“: rund 6.000–7.000 Menschen',shade('#a88a3c',-0.45),10.5,800)+T(380,59,'geben laut Regenauer den Ton vor [0:03]','var(--muted)',8.5,600)+`<animate attributeName="opacity" from="0" to="1" dur=".4s" begin="0s" fill="freeze"/></g>`;
      const S=[
        ['💶 Finanzebene','#c08a3e',['BIZ in Basel','63 Zentralbanken','Zinsen · Geldmenge','Staatsanleihen'],'„Zentralbankenkartell“'],
        ['🏛️ Organisationsebene','#4a7aa8',['UN + Unterorganisationen','WHO · UNESCO · IWF','EU → Bund → Land','Gemeinde: Pläne, 30er-Zonen'],'Vorgaben von oben'],
        ['🎩 Clubs','#7a6a9a',['Bilderberg · WEF','Le Cercle · Trilaterale','Bohemian Grove','ohne Protokoll'],'„Indizien, keine Belege“']];
      S.forEach(([t,c,L,u],i)=>{ const x=30+i*240, y=82, w=220;
        g+=`<g opacity="0"><path d="M380,64 L${x+w/2},${y}" stroke="var(--line)" stroke-width="1.4" ${i==2?'stroke-dasharray="4 3"':''} fill="none"/>`;
        g+=`<rect x="${x}" y="${y}" width="${w}" height="150" rx="12" fill="${lg(shade(c,0.8),shade(c,0.62),90)}" stroke="${c}" stroke-width="1.5" ${i==2?'stroke-dasharray="5 3"':''}/>`;
        g+=T(x+w/2,y+22,t,shade(c,-0.45),12,800);
        L.forEach((s,k)=>{ g+=`<rect x="${x+20}" y="${y+34+k*24}" width="${w-40}" height="19" rx="6" fill="${shade(c,0.88)}" stroke="${shade(c,0.3)}" stroke-width="0.8"/>`+T(x+w/2,y+47+k*24,s,'var(--ink)',9.5,650);
          if(k<L.length-1 && i<2) g+=`<path d="M${x+w/2},${y+53+k*24} l0,5" stroke="${c}" stroke-width="1.4"/>`; });
        g+=T(x+w/2,y+144,u,shade(c,-0.35),9,700);
        g+=`<animate attributeName="opacity" from="0" to="1" dur=".45s" begin="${(0.4+i*0.35).toFixed(2)}s" fill="freeze"/></g>`; });
      const by=252;
      g+=`<g opacity="0"><path d="M150,232 L300,${by}" stroke="#c08a3e" stroke-width="1.6" fill="none"/><path d="M380,232 L380,${by}" stroke="#4a7aa8" stroke-width="1.6" fill="none"/>`;
      g+=`<rect x="170" y="${by}" width="420" height="38" rx="12" fill="${lg('#d8e6cf','#bcd3ad',90)}" stroke="#5a8a4a" stroke-width="1.4"/>`;
      g+=T(380,by+16,'📱 Bürger: Smartphone, App, CO2-Budget, digitales Geld',shade('#5a8a4a',-0.5),10.5,800)+T(380,by+30,'Regeln würden am Endgerät durchgesetzt – „kein Polizist“ nötig [0:22–0:24]','var(--muted)',8.8,600);
      g+=`<animate attributeName="opacity" from="0" to="1" dur=".45s" begin="1.6s" fill="freeze"/></g>`;
      return {vb:'0 0 760 300',breit:true,leg:[],svg:g}; },
    masterpeace_institutionen(){ seed=5202; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3px">${t}</text>`;
      g+=T(380,18,'Institutionen und Dokumente aus dem Gespräch – Jahre (belegte Daten)',undefined,12.5,800);
      const x0=50, x1=695, j0=1880, j1=2026, X=j=>R(x0+(j-j0)/(j1-j0)*(x1-x0)), ay=150;
      g+=`<path d="M${x0},${ay} L${x1},${ay}" stroke="var(--line)" stroke-width="2"/>`;
      [1900,1925,1950,1975,2000,2025].forEach(j=>{ g+=`<path d="M${X(j)},${ay-4} l0,8" stroke="var(--muted)" stroke-width="1"/>`+T(X(j),ay+18,String(j),'var(--muted)',8.5,600); });
      const E=[[1884,'Fabian Society','#8a6a4a'],[1917,'Balfour-Erklärung','#6a7a4a'],[1920,'Völkerbund','#4a7aa8'],[1930,'BIZ (Basel)','#c08a3e'],[1945,'UN (51 Staaten)','#4a7aa8'],[1946,'Huxley: UNESCO-Schrift','#7a5a9a'],[1948,'Staat Israel','#6a7a4a'],[2000,'„Replacement Migration“','#4a7aa8'],[2005,'IHR (WHO)','#4a8a7a'],[2008,'„Superclass“','#8a6a4a'],[2020,'Great Reset','#b05a4a'],[2024,'Pakt für die Zukunft','#4a7aa8']];
      E.forEach(([j,t,c],i)=>{ const x=X(j), up=i%2==0, lvl=(Math.floor(i/2)%2), y= up ? ay-30-lvl*34 : ay+38+lvl*34;
        g+=`<g opacity="0"><path d="M${x},${ay} L${x},${up?y+6:y-12}" stroke="${c}" stroke-width="1.2"/><circle cx="${x}" cy="${ay}" r="5" fill="${c}"/>`;
        g+=T(x,y,t,shade(c,-0.4),9.2,750)+T(x,up?y-11:y+11,String(j),'var(--muted)',8,600);
        g+=`<animate attributeName="opacity" from="0" to="1" dur=".35s" begin="${(i*0.18).toFixed(2)}s" fill="freeze"/></g>`; });
      // UN-Mitglieder als kleine Leiste
      const bx=470, by=262, bw=250;
      g+=T(bx,by-8,'UN-Mitgliedstaaten',shade('#4a7aa8',-0.4),9,800,'start');
      [[1945,51],[1960,99],[1980,154],[2011,193]].forEach(([j,v],k)=>{ const w=R(v/193*bw);
        g+=`<rect x="${bx}" y="${by+k*9}" width="${w}" height="6" rx="2" fill="${shade('#4a7aa8',0.5-k*0.15)}"/>`+T(bx-6,by+k*9+6,j+': '+v,'var(--muted)',7.5,600,'end'); });
      return {vb:'0 0 760 310',breit:true,leg:[],svg:g}; },
