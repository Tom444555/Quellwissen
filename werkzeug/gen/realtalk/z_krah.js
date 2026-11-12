    krah_staatsbild(){ seed=7601; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3px">${t}</text>`;
      g+=T(380,18,'Welcher Staat? – Darstellung laut Krah (schematisch, keine Messwerte)',undefined,12.5,800);
      // Achsenfeld
      const x0=70,x1=470,y0=262,y1=44;
      g+=`<rect x="${x0}" y="${y1}" width="${x1-x0}" height="${y0-y1}" rx="10" fill="${lg('#f4ecd8','#ead9b8',90)}" stroke="var(--line)" stroke-width="1"/>`;
      g+=`<path d="M${x0},${y0} L${x1+8},${y0}" stroke="var(--muted)" stroke-width="1.6"/><path d="M${x1+8},${y0} l-7,-4 l0,8 z" fill="var(--muted)"/>`;
      g+=`<path d="M${x0},${y0} L${x0},${y1-8}" stroke="var(--muted)" stroke-width="1.6"/><path d="M${x0},${y1-8} l-4,7 l8,0 z" fill="var(--muted)"/>`;
      g+=T((x0+x1)/2,y0+20,'Eingriff ins Privatleben →  (wenig … viel)','var(--muted)',9.5,700);
      g+=`<text x="${x0-16}" y="${(y0+y1)/2}" transform="rotate(-90 ${x0-16} ${(y0+y1)/2})" style="fill:var(--muted);font:700 9.5px var(--label);text-anchor:middle">Stärke, Richtung →</text>`;
      const P=[
        [150,200,'#8a8a6a','Libertär',['Staat zieht sich zurück','„Markt gibt auch einem','Auftragskiller einen Preis“ [0:30]'],'u'],
        [395,185,'#b0604a','Heutiger Staat',['„mischt sich in alles ein“','„aus Schwäche“ [0:31]'],'u'],
        [165,88,'#4a7a5a','„Wille zum Staat“',['Preußen · Dubai','stark, schlank, mit Richtung [0:31]'],'r']];
      P.forEach(([x,y,c,t,L,pos],i)=>{
        g+=`<g opacity="0"><circle cx="${x}" cy="${y}" r="${i==2?17:13}" fill="${shade(c,0.25)}" stroke="${shade(c,-0.3)}" stroke-width="1.6"/>`;
        g+=T(x,y+(i==2?-24:-20),t,shade(c,-0.45),11,800);
        L.forEach((s,k)=>{ g+= pos=='u' ? T(x,y+30+k*12,s,k?'var(--muted)':'var(--ink)',8.6,k?600:650) : T(x+28,y-2+k*12,s,k?'var(--muted)':'var(--ink)',8.8,k?600:650,'start'); });
        g+=`<animate attributeName="opacity" from="0" to="1" dur=".4s" begin="${(0.2+i*0.35).toFixed(2)}s" fill="freeze"/></g>`; });
      // Pfeil vom heutigen Staat zum Ideal
      g+=`<g opacity="0"><path d="M383,170 C340,150 270,135 188,104" stroke="#4a7a5a" stroke-width="2" stroke-dasharray="5 4" fill="none"/><path d="M186,103 l10,-2 l-4,9 z" fill="#4a7a5a"/>`;
      g+=T(255,172,'Umbau laut Krah',shade('#4a7a5a',-0.4),9,750)+`<animate attributeName="opacity" from="0" to="1" dur=".4s" begin="1.3s" fill="freeze"/></g>`;
      // rechte Kästen
      const B=[[500,50,'#4a7a5a','Soll der Staat tragen',['Militär (keine Söldner)','Bibliotheken, Orchester','Polizei, schnelle Gerichte'],'[0:29–0:30], [0:46]'],
               [500,160,'#b0604a','Soll weg oder schrumpfen',['jede 2. Beamtenstelle','Umweltbundesamt (Beispiel)','Teile der Arbeitsverwaltung'],'[0:44–0:46]']];
      B.forEach(([x,y,c,t,L,f],i)=>{
        g+=`<g opacity="0"><rect x="${x}" y="${y}" width="235" height="96" rx="10" fill="${lg(shade(c,0.82),shade(c,0.66),90)}" stroke="${c}" stroke-width="1.3"/>`;
        g+=T(x+117,y+19,t,shade(c,-0.45),10.5,800);
        L.forEach((s,k)=>{ g+=T(x+16,y+40+k*16,'• '+s,'var(--ink)',9.2,650,'start'); });
        g+=T(x+219,y+89,f,'var(--muted)',7.8,600,'end');
        g+=`<animate attributeName="opacity" from="0" to="1" dur=".4s" begin="${(1.6+i*0.3).toFixed(2)}s" fill="freeze"/></g>`; });
      g+=T(617,284,'Positionen sind Krahs Sicht, keine Daten','var(--muted)',8.5,600);
      return {vb:'0 0 760 300',breit:true,leg:[],svg:g}; },
    krah_verfahren(){ seed=7602; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3px">${t}</text>`;
      g+=T(380,18,'Amtliche Vorgänge 2024–2026 (belegte Daten, Quellen im Abgleich)',undefined,12.5,800);
      const x0=40,x1=720,m0=2024+3/12,m1=2026+3/12,X=m=>R(x0+(m-m0)/(m1-m0)*(x1-x0)),ay=128;
      g+=`<path d="M${x0},${ay} L${x1},${ay}" stroke="var(--line)" stroke-width="2"/>`;
      [[2024.5,'Mitte 2024'],[2025,'2025'],[2025.5,'Mitte 2025'],[2026,'2026']].forEach(([m,t])=>{ g+=`<path d="M${X(m)},${ay-4} l0,8" stroke="var(--muted)"/>`+T(X(m),ay+16,t,'var(--muted)',8,600); });
      const E=[
        [2024+3.7/12,'Festnahme Jian G.','23.04.2024','#8a5a4a'],
        [2024+4.7/12,'ID-Fraktion schließt AfD aus','23.05.2024','#7a6a9a'],
        [2025+1.7/12,'Direktmandat WK 162: 44,2 %','23.02.2025','#5a7a9a'],
        [2025+4.05/12,'BfV: „gesichert rechtsextremistisch“','02.05.2025','#b0604a','end'],
        [2025+4.25/12,'Stillhaltezusage','08.05.2025','#c08a3e'],
        [2025+4.5/12,'Ermittlungsverfahren GenStA Dresden','Mai 2025','#8a5a4a'],
        [2025+8.35/12,'Immunität aufgehoben','11.09.2025','#8a5a4a'],
        [2025+8.97/12,'OLG Dresden: Urteil Jian G.','30.09.2025','#8a5a4a','start'],
        [2026+1.8/12,'VG Köln: Eilantrag der AfD','Feb. 2026, nicht rechtskräftig','#c08a3e','end']];
      E.forEach(([m,t,d,c,an],i)=>{ const x=X(m), up=i%2==0, lvl=Math.floor(i/2)%2, y=up? ay-26-lvl*30 : ay+40+lvl*30;
        const anchor = an || (x>620?'end':(x<110?'start':'middle'));
        g+=`<g opacity="0"><path d="M${x},${ay} L${x},${up?y+5:y-12}" stroke="${c}" stroke-width="1.2"/><circle cx="${x}" cy="${ay}" r="4.5" fill="${c}"/>`;
        g+=T(x,y,t,shade(c,-0.4),8.8,750,anchor)+T(x,up?y-11:y+11,d,'var(--muted)',7.6,600,anchor);
        g+=`<animate attributeName="opacity" from="0" to="1" dur=".35s" begin="${(i*0.18).toFixed(2)}s" fill="freeze"/></g>`; });
      g+=T(380,236,'Ermittlungsverfahren (Stand 11.09.2025): keine Anklage, Krah weist die Vorwürfe zurück – Unschuldsvermutung.','var(--muted)',8.6,650);
      // Geburtenziffer-Leiste
      const bx=230,by=266,bw=300,mx=2.2;
      const Bz=[['Türkei 2007',2.13,'#c08a3e'],['Türkei 2024',1.48,'#c08a3e'],['Deutschland 2024',1.36,'#4a7aa8'],['Deutschland 2025',1.32,'#4a7aa8']];
      g+=T(bx-8,by-6,'Geburtenziffer (Kinder je Frau):','var(--ink)',8.8,750,'end');
      Bz.forEach(([t,v,c],k)=>{ const w=R(v/mx*bw), yy=by-10+k*11;
        g+=`<rect x="${bx}" y="${yy}" width="${w}" height="7" rx="2" fill="${shade(c,0.15)}"/>`+T(bx+w+6,yy+7,t+': '+String(v).replace('.',','),'var(--muted)',7.6,600,'start'); });
      return {vb:'0 0 760 310',breit:true,leg:[],svg:g}; },
