    wisnewski_muster(){ seed=7700; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3px">${t}</text>`;
      g+=T(380,18,'Das wiederkehrende Muster (Darstellung laut Wisnewski, schematisch)',undefined,12.5,800);
      // zwei Quellen links: RAF und 11.9.
      const Q=[['🔍 RAF, „dritte Generation“','1985–1993: Morde ohne','ermittelte Täter [0:08]','#8a6a4a',40],['✈️ 11. September 2001','Täter nach 48 Stunden','benannt [0:19]','#4a7aa8',150]];
      Q.forEach(([t,a,b,c,y],i)=>{
        g+=`<g opacity="0"><rect x="15" y="${y}" width="180" height="78" rx="12" fill="${lg(shade(c,0.82),shade(c,0.62),90)}" stroke="${c}" stroke-width="1.5"/>`;
        g+=T(105,y+22,t,shade(c,-0.45),11,800)+T(105,y+44,a,'var(--ink)',9.5,650)+T(105,y+58,b,'var(--ink)',9.5,650);
        g+=`<path d="M195,${y+39} C226,${y+39} 226,134 252,134" stroke="${c}" stroke-width="1.6" fill="none" marker-end="url(#wmA)"/>`;
        g+=`<animate attributeName="opacity" from="0" to="1" dur=".4s" begin="${(0.2+i*0.3).toFixed(2)}s" fill="freeze"/></g>`; });
      g+=`<defs><marker id="wmA" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#7a6a5a"/></marker></defs>`;
      // Kette der Schritte
      const S=[['Ereignis','Anschlag mit','vielen Opfern','#b0703a'],['Täter sofort','Fahndungsplakate,','Bildergalerie','#a0603a'],['Begriff','„neues Pearl Harbor“,','„Krieg gegen Terror“','#7a6a9a'],['Folgen','Gesetze, Kriege,','Kontrolle','#5a8a4a']];
      S.forEach(([t,a,b,c],i)=>{ const x=256+i*124, y=96, w=116;
        g+=`<g opacity="0"><rect x="${x}" y="${y}" width="${w}" height="76" rx="11" fill="${lg(shade(c,0.85),shade(c,0.66),90)}" stroke="${c}" stroke-width="1.5"/>`;
        g+=`<circle cx="${x+14}" cy="${y+14}" r="9" fill="${shade(c,0.2)}" stroke="${shade(c,-0.3)}" stroke-width="1"/>`+T(x+14,y+18,String(i+1),'#fff',9.5,800);
        g+=T(x+w/2+6,y+20,t,shade(c,-0.5),11,800)+T(x+w/2,y+44,a,'var(--ink)',8.8,650)+T(x+w/2,y+58,b,'var(--ink)',8.8,650);
        if(i<S.length-1) g+=`<path d="M${x+w},${y+38} l10,0" stroke="#7a6a5a" stroke-width="1.6" marker-end="url(#wmA)"/>`;
        g+=`<animate attributeName="opacity" from="0" to="1" dur=".4s" begin="${(0.9+i*0.3).toFixed(2)}s" fill="freeze"/></g>`; });
      // Stafettenlauf der Begriffe
      const by=206;
      g+=`<g opacity="0">`+T(500,by,'„Stafettenlauf der Begriffe“ [0:18]',shade('#7a6a9a',-0.4),10.5,800);
      const B=[['Pearl Harbor 1941',360],['11.9.2001',500],['7.10.2023',640]];
      B.forEach(([t,x],i)=>{ g+=`<rect x="${x-62}" y="${by+10}" width="124" height="24" rx="12" fill="${shade('#7a6a9a',0.85)}" stroke="#7a6a9a" stroke-width="1"/>`+T(x,by+26,t,'var(--ink)',9.5,700);
        if(i<B.length-1) g+=`<path d="M${x+62},${by+22} l14,0" stroke="#7a6a9a" stroke-width="1.4" marker-end="url(#wmA)"/>`; });
      g+=`<animate attributeName="opacity" from="0" to="1" dur=".45s" begin="2.2s" fill="freeze"/></g>`;
      g+=`<g opacity="0">`+T(105,262,'„gängiges Werkzeug der Dienste“ [0:12]','var(--muted)',9,650)+T(500,262,'Belegte Daten und amtliche Gegendarstellung: siehe Reiter „Abgleich und Daten“','var(--muted)',9,650);
      g+=`<animate attributeName="opacity" from="0" to="1" dur=".4s" begin="2.6s" fill="freeze"/></g>`;
      return {vb:'0 0 760 280',breit:true,leg:[],svg:g}; },
    wisnewski_ablauf(){ seed=7701; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3px">${t}</text>`;
      g+=T(380,18,'Vormittag des 11. September 2001 – Zeiten laut 9/11-Kommission (belegte Daten)',undefined,12.5,800);
      const x0=60, x1=720, t0=8*60+30, t1=10*60+15, X=m=>x0+(m-t0)/(t1-t0)*(x1-x0), ay=150;
      g+=`<line x1="${x0}" y1="${ay}" x2="${x1}" y2="${ay}" stroke="var(--line)" stroke-width="2"/>`;
      for(let m=t0;m<=t1;m+=15){ const x=R(X(m)); const h=Math.floor(m/60), mi=String(m%60).padStart(2,'0');
        g+=`<line x1="${x}" y1="${ay-4}" x2="${x}" y2="${ay+4}" stroke="var(--line)" stroke-width="1.2"/>`+T(x,ay+18,`${h}:${mi}`,'var(--muted)',9,600); }
      const E=[[8*60+46.7,'American 11','Nordturm 8:46','#b05a3a',-1,58],[9*60+3,'United 175','Südturm 9:03','#c07a3a',-1,96],[9*60+37.8,'American 77','Pentagon 9:37','#8a5a8a',-1,58],[10*60+3.2,'United 93','Shanksville 10:03','#5a7a4a',-1,96]];
      E.forEach(([m,t,u,c,s,dy],i)=>{ const x=R(X(m)), y=ay-dy;
        g+=`<g opacity="0"><line x1="${x}" y1="${ay}" x2="${x}" y2="${y+20}" stroke="${c}" stroke-width="1.4" stroke-dasharray="3 2"/>`;
        g+=`<circle cx="${x}" cy="${ay}" r="6" fill="${c}" stroke="${shade(c,-0.35)}" stroke-width="1"/>`;
        g+=`<rect x="${x-58}" y="${y-14}" width="116" height="36" rx="9" fill="${lg(shade(c,0.85),shade(c,0.68),90)}" stroke="${c}" stroke-width="1.3"/>`;
        g+=T(x,y+1,t,shade(c,-0.5),10,800)+T(x,y+15,u,'var(--ink)',9,650);
        g+=`<animate attributeName="opacity" from="0" to="1" dur=".4s" begin="${(0.3+i*0.35).toFixed(2)}s" fill="freeze"/></g>`; });
      // Meldungen an NEADS (unten)
      const N=[[8*60+37.7,'NEADS erfährt von AA 11','9 Min. vor Einschlag','#4a7aa8',44],[10*60+7,'NEADS erfährt von UA 93','10:07 – nach dem Absturz','#4a7aa8',44]];
      N.forEach(([m,t,u,c,dy],i)=>{ const x=R(X(m)), y=ay+dy;
        g+=`<g opacity="0"><path d="M${x},${ay} l-6,10 l12,0 z" fill="${c}"/>`;
        g+=`<rect x="${x-74}" y="${y-6}" width="148" height="34" rx="9" fill="${shade(c,0.86)}" stroke="${c}" stroke-width="1.2"/>`;
        g+=T(x,y+8,t,shade(c,-0.45),9.5,800)+T(x,y+21,u,'var(--ink)',8.8,650);
        g+=`<animate attributeName="opacity" from="0" to="1" dur=".4s" begin="${(1.8+i*0.35).toFixed(2)}s" fill="freeze"/></g>`; });
      g+=`<g opacity="0">`+T(380,240,'▲ = Meldung an die Luftverteidigung (NEADS) · ● = Einschlag / Absturz','var(--muted)',9,650);
      g+=T(380,256,'Am Nachmittag (17:20:52) stürzte WTC 7 ein – laut NIST durch Feuer; Gegenstudie und Antwort im Abgleich.','var(--muted)',9,650);
      g+=T(380,272,'Wisnewski hält das Ausbleiben von Abfangjägern für ein Zeichen der Inszenierung [0:38].','var(--muted)',9,650);
      g+=`<animate attributeName="opacity" from="0" to="1" dur=".4s" begin="2.6s" fill="freeze"/></g>`;
      return {vb:'0 0 760 285',breit:true,leg:[],svg:g}; },
