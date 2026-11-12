    sozialismus_linien(){ seed=7401; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3px">${t}</text>`;
      g+=T(380,18,'Linien von Moses Hess bis heute (Darstellung laut Regenauer, schematisch)',undefined,12.5,800);
      const cx=380, cy=150;
      g+=`<g opacity="0"><circle cx="${cx}" cy="${cy}" r="46" fill="${lg('#ead9b2','#d6bd86',90)}" stroke="#a8843c" stroke-width="1.6"/>`+T(cx,cy-6,'Moses Hess',shade('#a8843c',-0.5),12,800)+T(cx,cy+9,'1812–1875','var(--muted)',9,650)+T(cx,cy+22,'[0:06–0:17]','var(--muted)',8,600)+`<animate attributeName="opacity" from="0" to="1" dur=".4s" begin="0s" fill="freeze"/></g>`;
      const B=[
        [120,62,'#b5523e','Sozialismus','Marx · Engels · SPD','[0:11–0:15]'],
        [640,62,'#7a5a9a','Fabian Society','Labour · Dritter Weg · LSE','[0:15–0:26]'],
        [120,238,'#4f7a9a','Zionismus','Rom u. Jerusalem → Herzl','[0:33], [1:06]'],
        [640,238,'#6a7a3e','Empire','Rhodes · Milner · Balfour','[0:26–0:50]']];
      B.forEach(([x,y,c,t,u,f],i)=>{
        const w=196,h=58;
        g+=`<g opacity="0"><path d="M${cx+(x<cx?-40:40)},${cy+(y<cy?-22:22)} L${x+(x<cx?w/2:-w/2)},${y}" stroke="${c}" stroke-width="1.6" stroke-dasharray="5 3" fill="none"/>`;
        g+=`<rect x="${x-w/2}" y="${y-h/2}" width="${w}" height="${h}" rx="12" fill="${lg(shade(c,0.82),shade(c,0.66),90)}" stroke="${c}" stroke-width="1.4"/>`;
        g+=T(x,y-8,t,shade(c,-0.45),11.5,800)+T(x,y+7,u,'var(--ink)',9,650)+T(x,y+20,f,'var(--muted)',8,600);
        g+=`<animate attributeName="opacity" from="0" to="1" dur=".4s" begin="${(0.4+i*0.3).toFixed(2)}s" fill="freeze"/></g>`; });
      // Mitte unten: Finanz, NS-Zeit
      g+=`<g opacity="0"><path d="M${cx},${cy+46} L${cx},212" stroke="#8a6a4a" stroke-width="1.6" fill="none"/>`;
      g+=`<rect x="${cx-110}" y="212" width="220" height="48" rx="12" fill="${lg('#e6d6c4','#d2bca2',90)}" stroke="#8a6a4a" stroke-width="1.4"/>`;
      g+=T(cx,229,'Finanzoligarchie und NS-Zeit',shade('#8a6a4a',-0.5),10.5,800)+T(cx,243,'Rockefeller, Bush, Transfer-Abkommen','var(--ink)',8.8,650)+T(cx,255,'[0:35], [0:50–1:04]','var(--muted)',8,600);
      g+=`<animate attributeName="opacity" from="0" to="1" dur=".4s" begin="1.7s" fill="freeze"/></g>`;
      g+=`<g opacity="0"><path d="M${cx},260 L${cx},276" stroke="#3e6a6a" stroke-width="1.6"/>`;
      g+=`<rect x="${cx-195}" y="276" width="390" height="30" rx="10" fill="${lg('#d4e4e2','#b8d0cc',90)}" stroke="#3e6a6a" stroke-width="1.4"/>`;
      g+=T(cx,295,'Heute: Eugenik, Kollektivismus, Technokratie – Plattformen und Daten [1:09–1:36]',shade('#3e6a6a',-0.5),9,750);
      g+=`<animate attributeName="opacity" from="0" to="1" dur=".4s" begin="2.1s" fill="freeze"/></g>`;
      g+=T(380,326,'Verbindungen sind Regenauers Deutung; belegte Eckdaten stehen in der zweiten Skizze und im Abgleich.','var(--muted)',8.5,600);
      return {vb:'0 0 760 336',breit:true,leg:[],svg:g}; },
    sozialismus_daten(){ seed=7402; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3px">${t}</text>`;
      g+=T(380,18,'Daten aus dem Gespräch, die Quellen bestätigen – 1812 bis 1960 (belegte Daten, nicht maßstäblich)',undefined,12,800);
      const E=[
        ['1812','Hess geboren','Bonn','#a8843c'],
        ['1862','„Rom und','Jerusalem“','#4f7a9a'],
        ['1884','Fabian Society','gegründet','#7a5a9a'],
        ['1894','Glen Grey Act','Kapkolonie','#6a7a3e'],
        ['1917','Balfour-','Erklärung','#6a7a3e'],
        ['1921','Londoner Plan','132 Mrd. Mark','#8a6a4a'],
        ['1929','Young-Plan','112 Mrd. bis 1988','#8a6a4a'],
        ['1930','BIZ gegründet','Basel','#8a6a4a'],
        ['1933','Haavara-','Abkommen','#b5523e'],
        ['1934','Betar-Marine-','schule (Italien)','#4f7a9a'],
        ['1941–45','Holocaust: 6 Mio.','Juden ermordet','#5a4a4a'],
        ['1942','UBC-Vermögen','beschlagnahmt','#8a6a4a'],
        ['1947','UN-Res. 181','33 : 13 : 10','#4f7a9a'],
        ['1960','Eichmann','gefasst','#5a4a4a']];
      const cols=7, w=96, h=86, gx=8, x0=(760-(cols*w+(cols-1)*gx))/2;
      E.forEach(([j,a,b,c],i)=>{ const r=Math.floor(i/cols), k=i%cols, x=x0+k*(w+gx), y=40+r*(h+44);
        g+=`<g opacity="0"><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="10" fill="${lg(shade(c,0.84),shade(c,0.68),90)}" stroke="${c}" stroke-width="1.3"/>`;
        g+=`<rect x="${x+14}" y="${y+8}" width="${w-28}" height="20" rx="8" fill="${shade(c,0.55)}" stroke="${c}" stroke-width="0.8"/>`+T(x+w/2,y+22,j,shade(c,-0.55),10.5,800);
        g+=T(x+w/2,y+48,a,shade(c,-0.5),9.2,750)+T(x+w/2,y+63,b,'var(--ink)',8.6,650);
        if(k<cols-1) g+=`<path d="M${x+w+1},${y+h/2} l${gx-2},0" stroke="var(--line)" stroke-width="1.4"/>`;
        g+=`<animate attributeName="opacity" from="0" to="1" dur=".3s" begin="${(i*0.14).toFixed(2)}s" fill="freeze"/></g>`; });
      g+=`<path d="M${x0+6*(w+gx)+w/2},${40+h} C${x0+6*(w+gx)+w/2},${40+h+22} ${x0+w/2},${40+h+18} ${x0+w/2},${40+h+44}" stroke="var(--line)" stroke-width="1.4" fill="none" stroke-dasharray="4 3"/>`;
      g+=T(380,300,'Quellen: JA/Britannica (Hess), Fabian Society, Kap-Parlament, Rothschild Archive, DHM/LeMO, BIZ, bpb, Wikipedia (Betar-Schule), USHMM, Guardian, Britannica, Yad Vashem','var(--muted)',7.8,600);
      return {vb:'0 0 760 312',breit:true,leg:[],svg:g}; },
