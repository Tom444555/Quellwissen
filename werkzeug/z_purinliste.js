    gicht_purinliste(){ seed=2405; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='start')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3">${t}</text>`;
      const A={r:'#c8503a',y:'#d9a632',g:'#5f9e4a'};
      const D=[['Rinderleber','125 g',530,'r'],['Forelle','150 g',409,'r'],['Hering','150 g',323,'r'],['Schweineschnitzel','125 g',264,'r'],['Weizenbier','3 × 0,5 l',225,'g'],['Hähnchenbrust','150 g',188,'y'],['Rinderhack','125 g',135,'y'],['Erbsen','150 g',192,'y'],['Linsen, gegart','150 g',100,'y'],['Spinat','150 g',91,'y'],['Vollkornnudeln, gek.','200 g',84,'g'],['Roggenvollkornbrot','2 Scheiben',58,'y'],['Reis, gekocht','180 g',52,'g'],['Salami','30 g',44,'y'],['Kartoffeln','200 g',31,'g'],['Mozzarella','1 Kugel',13,'g'],['Gouda','30 g',4,'g'],['Ei','1 Stück',3,'g'],['Joghurt','150 g',0,'g']];
      D.sort((a,b)=>b[2]-a[2]);
      const x0=210, bw=500, mx=600, y0=46, h=21;
      g+=T(20,22,'Harnsäure pro übliche Portion (mg) – Farbe = Ampel je 100 g','var(--ink)',12,800);
      for(let v=0;v<=600;v+=100){ const x=x0+v/mx*bw; g+=`<path d="M${x},${y0-6} V${y0+D.length*h}" stroke="var(--muted)" stroke-opacity=".25" stroke-dasharray="2 3"/>`+T(x,y0+D.length*h+14,v,'var(--muted)',9,600,'middle'); }
      D.forEach((d,i)=>{ const y=y0+i*h, w=Math.max(1.5,d[2]/mx*bw), c=A[d[3]];
        g+=T(x0-8,y+11,d[0],'var(--ink)',10,700,'end')+T(x0-8,y+20,d[1],'var(--muted)',8,600,'end');
        g+=`<rect x="${x0}" y="${y+2}" width="${w.toFixed(1)}" height="14" rx="4" fill="${lg(shade(c,.15),shade(c,-.15),0)}" stroke="${shade(c,-.35)}" stroke-width=".8"><animate attributeName="width" from="0" to="${w.toFixed(1)}" dur="1s" begin="${(i*0.05).toFixed(2)}s" fill="freeze"/></rect>`+T(x0+w+6,y+14,d[2],'var(--ink)',9.5,800); });
      const xl=x0+500/mx*bw; g+=`<path d="M${xl},${y0-10} V${y0+D.length*h}" stroke="#2a6a9a" stroke-width="1.8" stroke-dasharray="6 3"/>`+T(xl,y0-12,'Tagesrahmen 500 mg','#2a6a9a',9.5,800,'middle');
      const yl=y0+D.length*h+30; let lx=20;
      [['g','unter 50 mg/100 g'],['y','50–150'],['r','über 150']].forEach(l=>{ g+=`<rect x="${lx}" y="${yl-10}" width="12" height="12" rx="3" fill="${A[l[0]]}"/>`+T(lx+17,yl,l[1],'var(--muted)',9.5,600); lx+=l[1].length*6+44; });
      g+=T(740,yl,'Mittelwerte aus der Purinliste; Kalbsbries (≈ 1700 mg) passt nicht aufs Bild','var(--muted)',8.5,600,'end');
      return {vb:`0 0 760 ${yl+10}`,breit:true,leg:[],svg:g}; },
