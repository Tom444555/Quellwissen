    pohlmannschmidt_wende(){ seed=8001; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3px">${t}</text>`;
      const box=(x,y,w,h,c,l1,l2,l3,dash,t0)=>{ let s=`<g opacity="0"><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="11" fill="${lg(shade(c,0.82),shade(c,0.64),90)}" stroke="${c}" stroke-width="1.5" ${dash?'stroke-dasharray="6 4"':''}/>`;
        s+=T(x+w/2,y+18,l1,shade(c,-0.45),11,800); if(l2) s+=T(x+w/2,y+33,l2,'var(--ink)',9.2,650); if(l3) s+=T(x+w/2,y+46,l3,'var(--muted)',8.6,600);
        return s+`<animate attributeName="opacity" from="0" to="1" dur=".4s" begin="${t0}s" fill="freeze"/></g>`; };
      const pfeil=(x1,y1,x2,y2,c,dash,t0)=>{ const a=Math.atan2(y2-y1,x2-x1), hx=R(x2-9*Math.cos(a-0.4)), hy=R(y2-9*Math.sin(a-0.4)), kx=R(x2-9*Math.cos(a+0.4)), ky=R(y2-9*Math.sin(a+0.4));
        return `<g opacity="0"><path d="M${x1},${y1} L${x2},${y2}" stroke="${c}" stroke-width="1.8" fill="none" ${dash?'stroke-dasharray="5 4"':''}/><path d="M${x2},${y2} L${hx},${hy} L${kx},${ky} Z" fill="${c}"/><animate attributeName="opacity" from="0" to="1" dur=".35s" begin="${t0}s" fill="freeze"/></g>`; };
      g+=T(380,18,'Der Sturz Schmidts 1982 – wie Pohlmanns US-Quelle ihn schildert (schematisch)',undefined,12.5,800);
      // obere Reihe: Konflikt
      g+=box(20,34,220,56,'#7a5a3a','🇺🇸 Reagans „Grand Strategy“','Sowjetunion „totrüsten“','[0:18]',false,0);
      g+=box(270,34,220,56,'#3f7a6a','🔥 Erdgas-Röhren-Geschäft','Devisen für Moskau („8–10 Mrd. $“)','[0:17–0:19]',false,0.3);
      g+=box(520,34,220,56,'#9a4a3a','🪟 Vier-Augen-Gespräch','Schmidt schaut aus dem Fenster','laut Peter Schweizer [0:19]',false,0.6);
      g+=pfeil(240,62,268,62,'var(--line)',false,0.45)+pfeil(490,62,518,62,'var(--line)',false,0.75);
      // untere Reihe: behauptete Operation
      g+=pfeil(630,92,630,130,'#9a4a3a',true,0.95);
      g+=box(520,132,220,56,'#9a4a3a','💵 „Das Geld kam von uns“','UPI-Korrespondent, ungenannt','Flick-Affäre [0:08]',true,1.05);
      g+=pfeil(518,160,490,160,'#9a4a3a',true,1.25);
      g+=box(270,132,220,56,'#b08a2a','🟡 FDP: „pleite und gespalten“','„zwei Leute“ stimmen anders','[0:09]',true,1.35);
      g+=pfeil(268,160,240,160,'#9a4a3a',true,1.55);
      g+=box(20,132,220,56,'#4a6a9a','🗳️ Misstrauensvotum','1.10.1982: Kohl löst Schmidt ab','belegt: 256 zu 235 [0:07]',false,1.65);
      // Gegenstimmen
      g+=box(20,212,340,52,'#6a6a6a','✉️ Schmidt an Pohlmann','„wahrscheinlich durchaus unseriös“ –','andere Gründe, „Machenschaften“ der FDP [0:35]',false,1.95);
      g+=box(400,212,340,52,'#6a6a6a','🧭 Bahr zu Schmidts Antwort','Er „hängt komplett mit drin“ –','sonst gäbe er einen strategischen Fehler zu [0:35]',false,2.15);
      // Legende
      g+=`<g opacity="0"><path d="M40,288 l40,0" stroke="var(--ink)" stroke-width="1.6"/>`+T(88,291,'durchgezogen: belegter Vorgang oder Aussage mit Fundstelle','var(--muted)',8.8,600,'start');
      g+=`<path d="M420,288 l40,0" stroke="var(--ink)" stroke-width="1.6" stroke-dasharray="5 4"/>`+T(468,291,'gestrichelt: Behauptung der Quelle, nicht belegt ❓','var(--muted)',8.8,600,'start');
      g+=`<animate attributeName="opacity" from="0" to="1" dur=".4s" begin="2.4s" fill="freeze"/></g>`;
      return {vb:'0 0 760 304',breit:true,leg:[],svg:g}; },
    pohlmannschmidt_daten(){ seed=8002; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3px">${t}</text>`;
      g+=T(380,18,'Erdgas-Röhren-Geschäft, Embargo und Wende 1982 – belegte Daten',undefined,12.5,800);
      // Monatsachse Okt. 1981 – Jan. 1983
      const x0=40, x1=720, m0=1981*12+9, m1=1983*12+0, X=(j,m,t)=>R(x0+((j*12+m-1+(t-1)/30)-m0)/(m1-m0)*(x1-x0)), ay=128;
      g+=`<path d="M${x0},${ay} L${x1},${ay}" stroke="var(--line)" stroke-width="2"/>`;
      const E=[
        [1981,11,20,'Röhren-Vertrag','Ruhrgas – Sojusgasexport','#3f7a6a',-1,0],
        [1981,12,29,'US-Embargo','wegen Kriegsrecht in Polen','#9a4a3a',1,0],
        [1982,6,22,'Embargo ausgedehnt','auf europäische Firmen','#9a4a3a',-1,0],
        [1982,7,13,'Kreditrahmenvertrag','Leningrad','#3f7a6a',1,0],
        [1982,9,9,'Lambsdorff-Papier','„Wende-Papier“','#b08a2a',-1,1,'end'],
        [1982,9,17,'FDP-Minister','treten zurück','#b08a2a',1,1],
        [1982,10,1,'Misstrauensvotum','Kohl 256 : 235','#4a6a9a',-1,0,'start'],
        [1982,11,13,'Embargo','aufgehoben','#9a4a3a',1,0]];
      E.forEach(([j,m,t,l1,l2,c,up,lvl,an='middle'],i)=>{ const x=X(j,m,t), y= up<0 ? ay-34-lvl*40 : ay+44+lvl*40, tx= an=='end'? x-5 : an=='start'? x+5 : x;
        g+=`<g opacity="0"><path d="M${x},${ay} L${x},${up<0?(an=='middle'?y+16:y-14):(an=='middle'?y-24:y+14)}" stroke="${c}" stroke-width="1.2"/><circle cx="${x}" cy="${ay}" r="5" fill="${c}"/>`;
        g+=T(tx,y-10,l1,shade(c,-0.4),9.4,800,an)+T(tx,y+2,l2,'var(--ink)',8.4,600,an)+T(tx,y+13,`${String(t).padStart(2,'0')}.${String(m).padStart(2,'0')}.${j}`,'var(--muted)',8,600,an);
        g+=`<animate attributeName="opacity" from="0" to="1" dur=".35s" begin="${(i*0.22).toFixed(2)}s" fill="freeze"/></g>`; });
      [[1981,10,'Okt. 81'],[1982,1,'Jan. 82'],[1982,4,'Apr. 82'],[1982,7,'Jul. 82'],[1982,10,'Okt. 82'],[1983,1,'Jan. 83']].forEach(([j,m,t])=>{ const x=X(j,m,1); g+=`<path d="M${x},${ay-4} l0,8" stroke="var(--muted)" stroke-width="1"/>`+T(x,ay+17,t,'var(--muted)',8.3,600); });
      // Stimmen 1.10.1982
      const bx=70, by=262, bw=300;
      g+=T(bx,by-10,'Abstimmung am 1.10.1982 (Bundestag)',shade('#4a6a9a',-0.4),9.4,800,'start');
      [['Ja',256,'#4a6a9a'],['nötig',249,'#8a8a8a'],['Nein',235,'#9a4a3a']].forEach(([t,v,c],k)=>{ const w=R(v/260*bw);
        g+=`<g opacity="0"><rect x="${bx+44}" y="${by+k*15}" width="${w}" height="10" rx="3" fill="${shade(c,0.25)}" stroke="${c}" stroke-width="0.8"/>`+T(bx+38,by+k*15+9,t,'var(--muted)',8.4,700,'end')+T(bx+50+w,by+k*15+9,String(v),'var(--ink)',8.4,700,'start');
        g+=`<animate attributeName="opacity" from="0" to="1" dur=".35s" begin="${(1.9+k*0.15).toFixed(2)}s" fill="freeze"/></g>`; });
      g+=T(560,268,'Quellen: bpb-Chronik, Deutscher Bundestag','var(--muted)',8.4,600)+T(560,281,'Datum des ersten Embargos: 29.12.1981 📚','var(--muted)',8.4,600);
      return {vb:'0 0 760 312',breit:true,leg:[],svg:g}; },
