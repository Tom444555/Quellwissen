    gg_aufbau(){ seed=991; let g='';
      const A=[['I','Grundrechte','1–19',19,'#c8a040'],['II','Bund und Länder','20–37',18,'#4a8ac8'],['III','Bundestag','38–48',11,'#3a6a9a'],['IV','Bundesrat','50–53a',5,'#5a7ab8'],['V','Bundespräsident','54–61',8,'#8a6ab8'],['VI','Bundesregierung','62–69',8,'#6a5a9a'],['VII','Gesetzgebung','70–82',13,'#2a8a6a'],['VIII','Verwaltung','83–91e',14,'#4aa07a'],['IX','Rechtsprechung','92–104',13,'#b04a4a'],['X','Finanzen','104a–115',12,'#c87a30'],['Xa','Verteidigungsfall','115a–l',12,'#7a7a7a'],['XI','Übergang & Schluss','116–146',31,'#9a8a6a']];
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a}">${t}</text>`;
      g+=T(380,14,'Aufbau des Grundgesetzes – Abschnitte und Artikel',undefined,13,800); g+='<g transform="translate(0,14)">';
      const tot=A.reduce((s,a)=>s+a[3],0); let x=20; const bw=720;
      A.forEach(([n,t,r,k,c],i)=>{ const w=k/tot*bw, up=i%2===0;
        g+=`<rect x="${x.toFixed(1)}" y="66" width="${(w-2).toFixed(1)}" height="44" rx="5" fill="${lg(shade(c,0.3),shade(c,-0.1),90)}" stroke="${shade(c,-0.4)}" opacity="0"><animate attributeName="opacity" from="0" to="1" dur=".4s" begin="${(i*0.12).toFixed(2)}s" fill="freeze"/></rect>`;
        g+=T(x+w/2,93,n,'#fff',w>24?12:9,800);
        const ty=up?(i%4===0?52:30):(i%4===1?132:156); g+=`<path d="M${(x+w/2).toFixed(1)},${up?ty+4:112} V${up?66:ty-9}" stroke="${c}"/>`+T(x+w/2,ty,t,shade(c,-0.3),9,800)+T(x+w/2,ty+(up?-11:11),'Art. '+r,'var(--muted)',8.5,600);
        x+=w; });
      g+=`<rect x="20" y="176" width="${(19/tot*bw-2).toFixed(1)}" height="8" rx="4" fill="#c8a040"/>`+T(20,200,'Art. 1: Menschenwürde','#a07a10',9.5,800,'start');
      g+=`<rect x="${(20+19/tot*bw).toFixed(1)}" y="176" width="10" height="8" rx="4" fill="#4a8ac8"/>`+T(20+19/tot*bw+14,214,'Art. 20: Demokratie, Sozial-, Bundes-, Rechtsstaat','#2a5a9a',9.5,800,'start');
      g+=T(380,236,'Art. 1 und 20 sind durch die Ewigkeitsklausel (Art. 79 Abs. 3) unabänderlich. Breite = Zahl der Artikel (vereinfacht).','var(--muted)',9.5,600);
      g+='</g>'; return {vb:'0 0 760 260',breit:true,leg:[],svg:g}; },
