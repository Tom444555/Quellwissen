    realtalk25_gedaechtnis(){ seed=8500; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3px">${t}</text>`;
      g+=T(380,20,'Vom Zwischenspeicher zur Großhirnrinde: Schlaf und Gedächtnis',undefined,12.5,800);
      g+=T(380,36,'(Darstellung laut Nehls, schematisch)','var(--muted)',9.5,600);
      // Tag- und Nachthälfte
      g+=`<rect x="30" y="50" width="340" height="200" rx="14" fill="${lg(shade('#d9a441',0.8),shade('#d9a441',0.6),90)}" stroke="#c08a2e" stroke-width="1.4"/>`;
      g+=`<rect x="390" y="50" width="340" height="200" rx="14" fill="${lg(shade('#4a5f8a',0.7),shade('#4a5f8a',0.5),90)}" stroke="#4a5f8a" stroke-width="1.4"/>`;
      g+=T(200,72,'☀️ Tag: Erleben und Lernen',shade('#c08a2e',-0.45),11,800)+T(560,72,'🌙 Nacht: Schlaf',shade('#4a5f8a',-0.45),11,800);
      // Hippocampus füllt sich
      const hx=200, hy=160;
      g+=`<g opacity="0"><ellipse cx="${hx}" cy="${hy}" rx="70" ry="40" fill="${shade('#b0603e',0.75)}" stroke="#b0603e" stroke-width="1.5"/>`;
      g+=`<rect x="${hx-50}" y="${hy+5}" width="100" height="18" rx="5" fill="${shade('#b0603e',0.3)}"><animate attributeName="width" from="10" to="100" dur="2s" begin="0.4s" fill="freeze"/></rect>`;
      g+=T(hx,hy-10,'Hippocampus',shade('#b0603e',-0.5),11,800)+T(hx,hy+44+12,'Zwischenspeicher füllt sich','var(--ink)',9.5,650);
      g+=`<animate attributeName="opacity" from="0" to="1" dur=".5s" begin="0.1s" fill="freeze"/></g>`;
      ['Eindrücke','Gelerntes','Gespräche'].forEach((t,i)=>{ const y=104+i*0; const x=90+i*110;
        g+=`<g opacity="0">`+T(x,98,t,'var(--muted)',8.8,650)+`<path d="M${x},${103} L${hx+(x-hx)*0.35},${hy-38}" stroke="${shade('#c08a2e',-0.1)}" stroke-width="1.2" stroke-dasharray="3 3"/><animate attributeName="opacity" from="0" to="1" dur=".4s" begin="${(0.3+i*0.2).toFixed(1)}s" fill="freeze"/></g>`; });
      // Nacht: Tiefschlaf -> Großhirnrinde, REM verknüpft
      const cx=600, cy=145;
      g+=`<g opacity="0"><path d="M480,${cy+40} q120,-110 230,0" fill="${shade('#7a6a9a',0.6)}" stroke="#7a6a9a" stroke-width="1.5"/>`+T(cx,cy-2,'Großhirnrinde (Langzeitspeicher)',shade('#7a6a9a',-0.5),9.8,800);
      g+=`<animate attributeName="opacity" from="0" to="1" dur=".5s" begin="1.2s" fill="freeze"/></g>`;
      g+=`<g opacity="0"><ellipse cx="455" cy="205" rx="40" ry="20" fill="${shade('#b0603e',0.7)}" stroke="#b0603e"/>`+T(455,209,'Hippocampus',shade('#b0603e',-0.5),8.5,750);
      g+=`<path d="M490,196 Q520,170 545,${cy+18}" fill="none" stroke="#3f6a8a" stroke-width="2.2"/><path d="M545,${cy+18} l-9,1 l5,-8 z" fill="#3f6a8a"/>`;
      g+=T(545,240,'Tiefschlaf: überträgt','#2f4f6a',9,750)+`<animate attributeName="opacity" from="0" to="1" dur=".5s" begin="1.6s" fill="freeze"/></g>`;
      g+=`<g opacity="0">`;
      [[585,150],[620,140],[655,152],[690,165]].forEach(([x,y],i,a)=>{ g+=`<circle cx="${x}" cy="${y+20}" r="4" fill="#5a8a5a"/>`; if(i) g+=`<path d="M${a[i-1][0]},${a[i-1][1]+20} L${x},${y+20}" stroke="#5a8a5a" stroke-width="1.4"/>`; });
      g+=T(655,212,'REM-Schlaf: verknüpft','#3e6a3e',9,750)+`<animate attributeName="opacity" from="0" to="1" dur=".5s" begin="2.0s" fill="freeze"/></g>`;
      g+=T(380,272,'Schematisch nach dem Gespräch [0:45–0:48]; Forschungsstand siehe Reiter „Abgleich“ (Rasch und Born 2013).','var(--muted)',8.5,600);
      return {vb:'0 0 760 285', breit:true, leg:[], svg:g}; },
    realtalk25_lithium(){ seed=8501; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3px">${t}</text>`;
      g+=T(380,20,'Lithium: Größenordnungen in Mikrogramm pro Liter (belegte Daten)',undefined,12.5,800);
      g+=T(380,36,'logarithmische Skala – jede Stufe ist zehnmal größer','var(--muted)',9.5,600);
      const x0=70, x1=710, l0=0, l1=5, X=v=>R(x0+(Math.log10(v)-l0)/(l1-l0)*(x1-x0)), ay=150;
      g+=`<path d="M${x0},${ay} L${x1},${ay}" stroke="var(--line)" stroke-width="2"/>`;
      [1,10,100,1000,10000,100000].forEach(v=>{ g+=`<path d="M${X(v)},${ay-4} l0,8" stroke="var(--muted)"/>`+T(X(v),ay+18,v.toLocaleString('de-DE'),'var(--muted)',8.5,600); });
      g+=T(x1,ay+32,'Mikrogramm je Liter','var(--muted)',8.5,600,'end');
      // Wasser (oben) und Blut (unten)
      const W=[[12,'#4a7aa8','Dänemark, Trinkwasser','Median ≈ 12 (2017)'],[30.7,'#4a7aa8','Dänemark, Höchstwert','30,7 (2023)'],[120,'#4a7aa8','Texas, Trinkwasser','70–170 (1990)']];
      W.forEach(([v,c,t,s],i)=>{ const x=X(v), y=ay-30-i*26;
        g+=`<g opacity="0"><path d="M${x},${ay} L${x},${y+4}" stroke="${c}" stroke-width="1.2"/><circle cx="${x}" cy="${ay}" r="5" fill="${c}"/>`+T(x+6,y,'💧 '+t+': '+s,shade(c,-0.4),9,750,'start')+`<animate attributeName="opacity" from="0" to="1" dur=".4s" begin="${(i*0.25).toFixed(2)}s" fill="freeze"/></g>`; });
      g+=`<path d="M${X(70)},${ay-3} L${X(170)},${ay-3}" stroke="#4a7aa8" stroke-width="5" opacity=".45"/>`;
      const B=[[15,'#9a7a3a','Im Gespräch genannt: Blutwert bei 1 mg/Tag','15 (nicht geprüft)'],[4800,'#b0603e','Therapie-Blutspiegel 0,6–0,8 mmol/l','≈ 4.200–5.600'],[10400,'#8a3a3a','Toxisch ab 1,5 mmol/l','≈ 10.400']];
      B.forEach(([v,c,t,s],i)=>{ const x=X(v), y=ay+52+i*24, rx=i==0?x+6:x-6, an=i==0?'start':'end';
        g+=`<g opacity="0"><path d="M${x},${ay} L${x},${y-10}" stroke="${c}" stroke-width="1.2"/><rect x="${x-4}" y="${ay-4}" width="8" height="8" fill="${c}"/>`+T(rx,y,'🩸 '+t+': '+s,shade(c,-0.35),9,750,an)+`<animate attributeName="opacity" from="0" to="1" dur=".4s" begin="${(0.8+i*0.25).toFixed(2)}s" fill="freeze"/></g>`; });
      g+=`<path d="M${X(4160)},${ay+3} L${X(5550)},${ay+3}" stroke="#b0603e" stroke-width="5" opacity=".5"/>`;
      g+=T(380,268,'Quellen: Kessing 2017, Liew 2023, Schrauzer und Shrestha 1990, NICE QS95, Uniklinik Ulm; mmol/l umgerechnet mit 6,94 g/mol.','var(--muted)',8,600);
      return {vb:'0 0 760 280', breit:true, leg:[], svg:g}; },
