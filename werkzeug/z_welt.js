    geld_zeitstrahl(){ seed=951; let g=''; const W=760,y=118;
      const T=(x,yy,t,c='var(--ink)',s=10,w=700,a='middle')=>`<text x="${x}" y="${yy}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      const E=[[-3000,'Silber nach Gewicht','#b8bcc4'],[-600,'erste Münzen','#e0b040'],[1024,'Papiergeld China','#d8c8a0'],[1694,'Bank of England','#7a8aa0'],[1717,'Goldstandard GB','#e8b830'],[1873,'Goldmark','#e8b830'],[1914,'Goldeinlösung endet','#c05030'],[1923,'Hyperinflation','#c03020'],[1944,'Bretton Woods','#4a8ac8'],[1971,'Nixon-Schock','#c03020'],[1999,'Euro','#2a5aa8'],[2009,'Bitcoin','#e8902a']];
      const X=j=>j<1000?44+(j+3000)/4000*216:j<1900?260+(j-1000)/900*240:500+(j-1900)/125*240;
      g+=`<path d="M14,${y} H746" stroke="var(--muted)" stroke-width="2"/>`;
      [[-3000,'3000 v. Chr.'],[0,'Zeitenwende'],[1000,'1000'],[1500,'1500'],[1900,'1900'],[1950,'1950'],[2000,'2000']].forEach(([j,t])=>g+=`<path d="M${X(j)},${y-5} v10" stroke="var(--muted)"/>`+T(X(j),y+22,t,'var(--muted)',9.5,600));
      g+=`<rect x="${X(1717)}" y="${y-4}" width="${X(1914)-X(1717)}" height="8" rx="4" fill="#e8b830" opacity=".55"/>`+T((X(1717)+X(1914))/2,y+36,'Goldstandard','#a07a10',10,800);
      g+=`<rect x="${X(1944)}" y="${y-4}" width="${X(1971)-X(1944)}" height="8" rx="4" fill="#4a8ac8" opacity=".6"/>`;
      g+=`<rect x="${X(1971)}" y="${y-4}" width="${X(2025)-X(1971)}" height="8" rx="4" fill="#c05030" opacity=".45"/>`+T((X(1971)+X(2025))/2,y+36,'reines Papiergeld','#a03a20',10,800);
      E.forEach(([j,t,c],i)=>{ const x=X(j), up=i%2===0, yy=up?y-34-(i%4)*10:y+56+(i%4)*8;
        g+=`<path d="M${x},${y} V${up?yy+8:yy-12}" stroke="${c}" stroke-width="1.2"/>`;
        g+=`<g><circle cx="${x}" cy="${y}" r="7" fill="${lg(shade(c,0.3),shade(c,-0.2),45)}" stroke="${shade(c,-0.5)}"/><animate attributeName="opacity" values="0;1" dur=".4s" begin="${i*0.25}s" fill="freeze"/></g>`;
        g+=T(x,yy,(j<0?-j+' v. Chr.':j),c,9.5,800)+T(x,yy+11,t,'var(--ink)',9.5,600); });
      return {vb:'0 0 760 200',breit:true,leg:[],svg:g}; },
    erf_zeitstrahl(){ seed=952; let g=''; const y=110;
      const T=(x,yy,t,c='var(--ink)',s=9.5,w=700)=>`<text x="${x}" y="${yy}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:middle;paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      const E=[[-3500,'Rad'],[-3200,'Schrift'],[105,'Papier'],[1450,'Buchdruck'],[1712,'Dampfmaschine'],[1796,'Impfung'],[1886,'Auto'],[1903,'Flugzeug'],[1928,'Penicillin'],[1941,'Computer'],[1969,'Internet'],[2007,'Smartphone']];
      const X=j=>j<1000?44+(j+3500)/4500*206:j<1900?250+(j-1000)/900*250:500+(j-1900)/125*240;
      g+=`<path d="M14,${y} H746" stroke="var(--muted)" stroke-width="2"/>`;
      E.forEach(([j,t],i)=>{ const x=X(j), up=i%2===0, yy=up?y-30-(i%4)*12:y+40+(i%4)*10;
        g+=`<path d="M${x},${y} V${up?yy+6:yy-11}" stroke="#c8a020" stroke-width="1"/>`;
        g+=`<g><circle cx="${x}" cy="${y-2}" r="7" fill="${lg('#fff6b0','#f0c020',90)}" stroke="#7a6010"/><rect x="${x-3}" y="${y+4}" width="6" height="4" fill="#8a8a8a"/><animate attributeName="opacity" values=".35;1;.35" dur="2.4s" begin="${i*0.2}s" repeatCount="indefinite"/></g>`;
        g+=T(x,yy,j<0?-j+' v. Chr.':j,'#a07a10',9.5,800)+T(x,yy+11,t); });
      g+=T(380,190,'Die Abstände wachsen nach rechts: Erfindungen folgen immer schneller aufeinander','var(--muted)',10,600);
      return {vb:'0 0 760 200',breit:true,leg:[],svg:g}; },
