    schoening_kette(){ seed=8300; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3px">${t}</text>`;
      g+=T(380,18,'Der rote Faden 2001–2026 (Darstellung laut Schöning, schematisch)',undefined,12.5,800);
      const S=[
        ['2001','✈️ 9/11','#b0603e',['Vier Flugzeuge','WTC 7 ohne Flugzeug'],'[0:17], [0:56]'],
        ['2001','✉️ Anthrax','#9a7a3a',['Briefe, 5 Tote','Patriot Act'],'[0:16], [0:52]'],
        ['2008','🧪 Ivins','#7a6a9a',['FBI: Einzeltäter','laut S. „vorgeschoben“'],'[0:16–0:23]'],
        ['2018/19','🎥 Ankündigung','#4a7aa8',['KenFM-Interview','„für 2020 geplant“'],'[0:04]'],
        ['2020','🦠 Corona','#4a8a6a',['Pandemie, Impfung','„Lasst euch impfen“'],'[0:04], [0:49]'],
        ['2026','🃏 Heute','#8a5a5a',['Epstein-Akten, Gaza','„Better Normal“'],'[0:32], [1:26]']];
      const w=110, gap=12, x0=(760-(S.length*w+(S.length-1)*gap))/2, y=46, h=96;
      S.forEach(([j,t,c,L,f],i)=>{ const x=R(x0+i*(w+gap));
        g+=`<g opacity="0"><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="11" fill="${lg(shade(c,0.82),shade(c,0.62),90)}" stroke="${c}" stroke-width="1.5"/>`;
        g+=T(x+w/2,y+16,j,'var(--muted)',8.5,700)+T(x+w/2,y+34,t,shade(c,-0.45),11,800);
        L.forEach((s,k)=>{ g+=T(x+w/2,y+54+k*15,s,'var(--ink)',8.6,650); });
        g+=T(x+w/2,y+h-6,f,'var(--muted)',7.6,600);
        if(i<S.length-1) g+=`<path d="M${x+w+1},${y+h/2} l${gap-3},0" stroke="${shade(c,-0.2)}" stroke-width="2"/><path d="M${x+w+gap-2},${y+h/2} l-5,-4 l0,8 z" fill="${shade(c,-0.2)}"/>`;
        g+=`<animate attributeName="opacity" from="0" to="1" dur=".4s" begin="${(i*0.28).toFixed(2)}s" fill="freeze"/></g>`; });
      // Personen-Brücke
      const P=[
        ['Richard Tubb','Cipro an Bord der Air Force One 2001 → Heritage-Kommission 2020 → Medicago','[1:03–1:11]','#4a8a6a'],
        ['Jerome Hauer','Dark Winter 2001 → Trümmer 9/11 → Emergent BioSolutions','[1:19–1:25]','#9a7a3a'],
        ['Edwin Meese','laut Schöning Vertuschung im Anthrax-Fall, Heritage Foundation','[0:23], [1:01]','#7a6a9a']];
      const py=170;
      g+=`<g opacity="0">`+T(380,py-8,'Personen, die laut Schöning die Ereignisse verbinden (Vorwürfe = seine Sicht ❓)',shade('#8a5a5a',-0.3),10,800);
      P.forEach(([n,t,f,c],k)=>{ const yy=py+6+k*30;
        g+=`<rect x="70" y="${yy}" width="620" height="24" rx="8" fill="${shade(c,0.86)}" stroke="${shade(c,0.2)}" stroke-width="1"/>`;
        g+=T(82,yy+16,'👤 '+n,shade(c,-0.45),10,800,'start')+T(200,yy+16,t,'var(--ink)',9,600,'start')+T(680,yy+16,f,'var(--muted)',8,600,'end'); });
      g+=`<animate attributeName="opacity" from="0" to="1" dur=".5s" begin="1.8s" fill="freeze"/></g>`;
      g+=T(380,282,'Schematisch nach dem Gespräch; belegte Abweichungen siehe Reiter „Abgleich und Daten“.','var(--muted)',8.5,600);
      return {vb:'0 0 760 295', breit:true, leg:[], svg:g}; },
    schoening_daten(){ seed=8301; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3px">${t}</text>`;
      g+=T(380,18,'Belegte Daten zu den Themen des Gesprächs, 2001–2026 (belegte Daten)',undefined,12.5,800);
      const x0=60, x1=700, j0=2000.5, j1=2026.5, X=j=>R(x0+(j-j0)/(j1-j0)*(x1-x0)), ay=158;
      g+=`<path d="M${x0},${ay} L${x1},${ay}" stroke="var(--line)" stroke-width="2"/>`;
      [2001,2005,2010,2015,2020,2025].forEach(j=>{ g+=`<path d="M${X(j)},${ay-4} l0,8" stroke="var(--muted)" stroke-width="1"/>`+T(X(j),ay+17,String(j),'var(--muted)',8.5,600); });
      const E=[
        [2001.47,'06/2001','Dark Winter','#9a7a3a'],
        [2001.70,'09/2001','9/11 · Anthrax','#b0603e'],
        [2008.90,'11/2008','NIST: WTC 7','#4a7aa8'],
        [2010.13,'02/2010','Amerithrax abgeschl.','#7a6a9a'],
        [2011.12,'02/2011','National Academies','#7a6a9a'],
        [2016.70,'09/2016','Politico: Tubb, Cipro','#4a8a6a'],
        [2020.26,'04/2020','Heritage-Kommission','#4a8a6a'],
        [2022.36,'05/2022','Kongress: Emergent','#9a7a3a'],
        [2022.52,'07/2022','AT: Impfpflicht ab','#5a8a4a'],
        [2023.69,'09/2023','IMEC-Memorandum','#8a5a5a'],
        [2026.06,'01/2026','Davos · Epstein-Akten','#8a5a5a']];
      E.forEach(([j,d,t,c],i)=>{ const x=X(j), up=i%2==0, lvl=Math.floor(i/2)%3, y= up ? ay-28-lvl*30 : ay+38+lvl*30;
        g+=`<g opacity="0"><path d="M${x},${ay} L${x},${up?y+6:y-12}" stroke="${c}" stroke-width="1.2"/><circle cx="${x}" cy="${ay}" r="5" fill="${c}"/>`;
        g+=T(x,y,t,shade(c,-0.4),9,750)+T(x,up?y-11:y+11,d,'var(--muted)',7.8,600);
        g+=`<animate attributeName="opacity" from="0" to="1" dur=".35s" begin="${(i*0.17).toFixed(2)}s" fill="freeze"/></g>`; });
      g+=T(380,292,'Quellen: FBI, US-Justizministerium, National Academies, NIST, Politico, Heritage, US-Kongress, Nationalrat AT, Weißes Haus, AP/JTA','var(--muted)',8,600);
      return {vb:'0 0 760 300', breit:true, leg:[], svg:g}; },
