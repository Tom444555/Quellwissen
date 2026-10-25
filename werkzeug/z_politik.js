    de_staatsformen(){ seed=981; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      const X=j=>j<1800?30+(j-800)/1000*170:200+(j-1800)/226*540;
      g+=T(380,18,'Deutsche Staatsformen von 800 bis heute',undefined,13,800);
      [[800,'800'],[1000,'1000'],[1200,'1200'],[1400,'1400'],[1600,'1600'],[1800,'1800'],[1850,'1850'],[1900,'1900'],[1950,'1950'],[2000,'2000']].forEach(([j,t])=>g+=`<path d="M${X(j)},34 V246" stroke="var(--muted)" stroke-opacity=".25" stroke-dasharray="2 3"/>`+T(X(j),262,t,'var(--muted)',9,600));
      g+=`<path d="M200,30 V250" stroke="var(--muted)" stroke-width="1.2"/>`+T(200,276,'← 1000 Jahre gestaucht | ab 1800 gedehnt →','var(--muted)',9,600);
      const B=[[800,843,0,'Frankenreich','#9a8a60'],[843,962,2,'Ostfrankenreich','#b8a070'],[962,1806,1,'Heiliges Römisches Reich (844 Jahre)','#c8a040'],[1806,1813,0,'Rheinbund','#a0a0a0'],[1815,1866,1,'Deutscher Bund','#8aa0b8'],[1867,1871,0,'Nordd. Bund','#6a8aa8'],[1871,1918,1,'Kaiserreich','#3a5a8a'],[1919,1933,0,'Weimarer Republik','#c8a030'],[1933,1945,1,'NS-Diktatur','#5a3030'],[1945,1949,2,'Besatzung','#8a8a8a'],[1949,2026,1,'Bundesrepublik','#2a7a5a'],[1949,1990,2,'DDR','#b04040'],[1990,2026,3,'vereint seit 1990','#4aa07a']];
      B.forEach(([a,b,l,t,c],i)=>{ const x=X(a), w=Math.max(3,X(b)-x), y=44+l*48;
        g+=`<rect x="${x}" y="${y}" width="${w.toFixed(1)}" height="30" rx="5" fill="${lg(shade(c,0.25),shade(c,-0.15),90)}" stroke="${shade(c,-0.4)}"><animate attributeName="width" from="0" to="${w.toFixed(1)}" dur=".7s" begin="${(i*0.12).toFixed(2)}s" fill="freeze"/></rect>`;
        const innen=w>t.length*5.6+6; g+=innen?T(x+w/2,y+19,t,'#fff',9.5,800).replace('stroke:var(--surface)','stroke:'+shade(c,-0.4)):T(x+w/2,y+(l%2||l===2?44:-5),t,shade(c,-0.3),9,800); });
      g+=T(X(1918),224,'1918: Ende der Monarchie','var(--muted)',9,700)+T(X(1990),240,'3.10.1990','var(--muted)',9,700);
      return {vb:'0 0 760 286',breit:true,leg:[],svg:g}; },

    kanzler_balken(){ seed=982; let g='';
      const K=[['Konrad Adenauer','CDU',1949.71,1963.79],['Ludwig Erhard','CDU',1963.79,1966.92],['Kurt Georg Kiesinger','CDU',1966.92,1969.80],['Willy Brandt','SPD',1969.80,1974.35],['Helmut Schmidt','SPD',1974.35,1982.75],['Helmut Kohl','CDU',1982.75,1998.82],['Gerhard Schröder','SPD',1998.82,2005.89],['Angela Merkel','CDU',2005.89,2021.94],['Olaf Scholz','SPD',2021.94,2025.35],['Friedrich Merz','CDU',2025.35,2026.8]];
      const T=(x,y,t,c='var(--ink)',s=10.5,w=600,a='start')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a}">${t}</text>`;
      const x0=150, bw=560, X=j=>x0+(j-1949)/(2027-1949)*bw;
      g+=T(380,18,'Bundeskanzler seit 1949 – Amtszeiten',undefined,13,800,'middle');
      [1950,1960,1970,1980,1990,2000,2010,2020].forEach(j=>g+=`<path d="M${X(j)},30 V${36+K.length*24}" stroke="var(--muted)" stroke-opacity=".25" stroke-dasharray="2 3"/>`+T(X(j),50+K.length*24,j,'var(--muted)',9,600,'middle'));
      K.forEach(([n,p,a,b],i)=>{ const y=34+i*24, c=p==='SPD'?'#d8302a':'#3a3a3a', w=X(b)-X(a), J=(b-a);
        g+=T(x0-8,y+13,n,'var(--ink)',10.5,700,'end');
        g+=`<rect x="${X(a).toFixed(1)}" y="${y+2}" width="${w.toFixed(1)}" height="16" rx="4" fill="${lg(shade(c,0.3),c,90)}"><animate attributeName="width" from="0" to="${w.toFixed(1)}" dur=".6s" begin="${(i*0.15).toFixed(2)}s" fill="freeze"/></rect>`;
        g+=i===K.length-1?T(X(a)-6,y+14,`${p} · seit Mai 2025`,'var(--muted)',9.5,700,'end'):T(X(b)+5,y+14,`${p} · ${J.toFixed(1).replace('.',',')} J.`,c==='#3a3a3a'?'var(--muted)':'#c0302a',9.5,700); });
      g+=`<rect x="560" y="${60+K.length*24}" width="12" height="10" rx="2" fill="#3a3a3a"/>`+T(576,69+K.length*24,'CDU','var(--ink)',9.5,700)+`<rect x="614" y="${60+K.length*24}" width="12" height="10" rx="2" fill="#d8302a"/>`+T(630,69+K.length*24,'SPD','var(--ink)',9.5,700);
      return {vb:`0 0 760 ${78+K.length*24}`,breit:true,leg:[],svg:g}; },

    bundestag_sitze(){ seed=983; let g='';
      const P=[['Die Linke',64,'#be3075'],['SPD',120,'#e3000f'],['Grüne',85,'#46962b'],['SSW',1,'#003c8f'],['CDU/CSU',208,'#2a2a2a'],['AfD',152,'#009ee0']];
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a}">${t}</text>`;
      const cx=380, cy=262, rows=13, r0=100, r1=232, S=[]; let L=0; const rr=[]; for(let k=0;k<rows;k++){ const r=r0+(r1-r0)*k/(rows-1); rr.push(r); L+=r; }
      let tot=0; rr.forEach((r,k)=>{ const n=k<rows-1?Math.round(630*r/L):630-tot; tot+=n; for(let j=0;j<n;j++){ const a=Math.PI-(Math.PI*(j+.5)/n); S.push([a,r]); } });
      S.sort((p,q)=>q[0]-p[0]); let i=0;
      P.forEach(([n,z,c],pi)=>{ for(let k=0;k<z;k++,i++){ const [a,r]=S[i]; g+=`<circle cx="${(cx+r*Math.cos(a)).toFixed(1)}" cy="${(cy-r*Math.sin(a)).toFixed(1)}" r="4.1" fill="${c}" opacity="0"><animate attributeName="opacity" from="0" to="1" dur=".3s" begin="${(pi*0.25+k*0.002).toFixed(3)}s" fill="freeze"/></circle>`; } });
      g+=T(cx,cy-18,'630',undefined,26,800)+T(cx,cy,'Sitze im 21. Bundestag','var(--muted)',10,700);
      P.forEach(([n,z,c],k)=>{ const x=70+k*118; g+=`<rect x="${x-34}" y="284" width="12" height="12" rx="3" fill="${c}"/>`+T(x-18,294,`${n} ${z}`,'var(--ink)',10.5,700,'start'); });
      g+=T(cx,318,'Wahl 23.2.2025. Sitzordnung vereinfacht von links nach rechts. Mehrheit: 316 Sitze.','var(--muted)',9.5,600);
      return {vb:'0 0 760 328',breit:true,leg:[],svg:g}; },

    politik_zeitstrahl(){ seed=984; let g=''; const y=118;
      const T=(x,yy,t,c='var(--ink)',s=9.5,w=700)=>`<text x="${x}" y="${yy}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:middle;paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      const E=[[-508,'Demokratie Athen','#4a8ac8'],[-509,'Röm. Republik','#c8a040'],[1215,'Magna Carta','#8a6a40'],[1689,'Bill of Rights','#8a3a6a'],[1748,'Gewaltenteilung','#6a8a3a'],[1787,'US-Verfassung','#3a5a9a'],[1789,'Franz. Revolution','#c03020'],[1848,'Revolutionen','#c86a20'],[1893,'Frauenwahlrecht NZ','#a04a8a'],[1917,'Russ. Revolution','#b02020'],[1922,'Faschismus','#3a3a3a'],[1945,'Vereinte Nationen','#2a8ac8'],[1960,'Dekolonisierung','#c8a020'],[1989,'Mauerfall','#2a9a6a'],[1993,'EU','#2a5aa8']];
      const X=j=>j<1500?44+(j+600)/2100*200:j<1900?244+(j-1500)/400*236:480+(j-1900)/126*260;
      g+=`<path d="M14,${y} H746" stroke="var(--muted)" stroke-width="2"/>`;
      [[-500,'500 v. Chr.'],[0,'0'],[1000,'1000'],[1500,'1500'],[1700,'1700'],[1900,'1900'],[1950,'1950'],[2000,'2000']].forEach(([j,t])=>g+=`<path d="M${X(j)},${y-5} v10" stroke="var(--muted)"/>`+T(X(j),y+22,t,'var(--muted)',9,600));
      E.forEach(([j,t,c],i)=>{ const x=X(j), up=i%2===0, yy=up?y-30-(i%4)*12:y+50+(i%4)*10;
        g+=`<path d="M${x},${y} V${up?yy+6:yy-11}" stroke="${c}" stroke-width="1.1"/>`;
        g+=`<g><rect x="${x-6}" y="${y-6}" width="12" height="12" rx="3" transform="rotate(45 ${x} ${y})" fill="${lg(shade(c,0.35),shade(c,-0.15),45)}" stroke="${shade(c,-0.5)}"/><animate attributeName="opacity" values="0;1" dur=".4s" begin="${i*0.2}s" fill="freeze"/></g>`;
        g+=T(x,yy,j<0?-j+' v. Chr.':j,c,9,800)+T(x,yy+11,t,'var(--ink)',9,600); });
      return {vb:'0 0 760 222',breit:true,leg:[],svg:g}; },
