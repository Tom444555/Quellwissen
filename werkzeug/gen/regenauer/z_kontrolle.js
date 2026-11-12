    kontrolle_pyramide(){ seed=5301; let g='';
      const T=(x,y,t,c='var(--ink)',s=11,w=700,o=true)=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:middle${o?';paint-order:stroke;stroke:var(--surface);stroke-width:3px':''}">${t}</text>`;
      g+=T(380,20,'Wer lenkt? – Pyramide der „Global Governance“ (Darstellung laut Regenauer)',undefined,12.5,800);
      const S=[['Banken &amp; Finanzkartelle','#8a5a2a'],['Policy Makers &amp; Thinktanks','#a0703a'],['UN, IWF, Weltbank','#5a7a9a'],['Nationale Regierungen &amp; Behörden','#6a8a5a'],['Medien („Propaganda Outlets“)','#9a6a7a'],['Öffentlichkeit – hier wird gewählt','#7a7a6a']];
      const top=38, h=40, cx=290;
      S.forEach(([t,c],i)=>{ const y=top+i*h, w1=120+i*76, w2=120+(i+1)*76;
        const pts=`${R(cx-w1/2)},${y} ${R(cx+w1/2)},${y} ${R(cx+w2/2)},${y+h-3} ${R(cx-w2/2)},${y+h-3}`;
        g+=`<g opacity="0"><polygon points="${pts}" fill="${lg(shade(c,0.35),c,90)}" stroke="${shade(c,-0.35)}" stroke-width="1.3"/>`+T(cx,y+h/2+4,t,'#fff',i<1?9.5:10.5,800,false)+`<animate attributeName="opacity" from="0" to="1" begin="${(0.15*i).toFixed(2)}s" dur="0.5s" fill="freeze"/></g>`; });
      // Pfeil Einfluss nach unten
      g+=`<path d="M592 50 L592 262" stroke="var(--muted)" stroke-width="2.4" fill="none" stroke-dasharray="5 4"/><polygon points="584,258 600,258 592,274" fill="var(--muted)"/>`;
      g+=T(682,70,'Einfluss',undefined,11,800)+T(682,86,'von oben nach unten','var(--muted)',10,600);
      g+=T(682,150,'Seine These:','var(--ink)',10.5,800)+T(682,166,'Wahlen wirken nur','var(--muted)',10,600)+T(682,180,'auf die unteren Stufen','var(--muted)',10,600);
      g+=T(682,240,'[1:07–1:09]','var(--muted)',10,600);
      g+=T(380,292,'Schema nach der Folie im Vortrag – Deutung des Referenten, keine belegte Struktur','var(--muted)',9.5,600);
      return {vb:'0 0 760 300', breit:true, leg:[], svg:g}; },
    kontrolle_eudi(){ seed=5302; let g='';
      const T=(x,y,t,c='var(--ink)',s=11,w=700,o=true)=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:middle${o?';paint-order:stroke;stroke:var(--surface);stroke-width:3px':''}">${t}</text>`;
      g+=T(380,20,'Die EU-Wallet (EUDI) – Zeitplan und Regeln (belegte Daten)',undefined,12.5,800);
      g+=`<line x1="50" y1="120" x2="710" y2="120" stroke="var(--line)" stroke-width="3"/>`;
      const P=[[90,'04/2024','eIDAS 2.0 in Kraft','VO (EU) 2024/1183','#5a7a9a'],[250,'12/2025','ID Austria:','4,8 Mio. Registrierungen','#6a8a5a'],[420,'Ende 2026','EU-Frist: jeder Staat','bietet eine Wallet an','#a0703a'],[600,'02.01.2027','geplanter Start','in Deutschland','#8a5a2a']];
      P.forEach(([x,d,a,b,c],i)=>{ const up=i%2===0, yb=up?42:138;
        g+=`<g opacity="0"><circle cx="${x}" cy="120" r="10" fill="${c}" stroke="${shade(c,-0.35)}" stroke-width="1.3"/><line x1="${x}" y1="${up?110:130}" x2="${x}" y2="${up?92:138}" stroke="${c}" stroke-width="1.6"/><rect x="${x-76}" y="${yb}" width="152" height="50" rx="9" fill="${lg(shade(c,0.8),shade(c,0.6),90)}" stroke="${c}" stroke-width="1.2"/>`+T(x,yb+15,d,shade(c,-0.45),11,800)+T(x,yb+30,a,'var(--ink)',9.5,700)+T(x,yb+43,b,'var(--muted)',9.5,600)+`<animate attributeName="opacity" from="0" to="1" begin="${(0.2*i).toFixed(2)}s" dur="0.5s" fill="freeze"/></g>`; });
      const K=[['Freiwillig','Art. 5a Abs. 15: keine','Benachteiligung ohne Wallet','#6a8a5a'],['Annahmepflicht','Banken und sehr große','Online-Plattformen','#a0703a'],['Kritik','BfDI warnt vor Wert','der Identitätsdaten','#9a6a7a']];
      K.forEach(([t,a,b,c],i)=>{ const x=130+i*250;
        g+=`<rect x="${x-105}" y="206" width="210" height="58" rx="10" fill="${lg(shade(c,0.82),shade(c,0.65),90)}" stroke="${c}" stroke-width="1.2"/>`+T(x,224,t,shade(c,-0.45),11,800)+T(x,240,a,'var(--ink)',9.5,600)+T(x,254,b,'var(--ink)',9.5,600); });
      g+=T(380,288,'Quellen: netzpolitik.org (10.03.2026), Bundeskanzleramt Österreich (15.12.2025)','var(--muted)',9.5,600);
      return {vb:'0 0 760 300', breit:true, leg:[], svg:g}; },
