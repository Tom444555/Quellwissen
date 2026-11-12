    regenauer_ebenen(){ seed=5101; let g='';
      const T=(x,y,t,c='var(--ink)',s=11,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a}">${t}</text>`;
      g+=T(380,22,'Wer gibt wem etwas vor? – Darstellung laut Regenauer (schematisch)','var(--ink)',13.5,800);
      const E=[['Banken und Finanzkartelle','Zentralbanken, BIZ in Basel','#8d4a43'],['Denkfabriken und Stiftungen','schreiben die Leitlinien','#865324'],['Überstaatliche Organisationen','UN, IWF, Weltbank, WHO','#6e6016'],['Nationale Regierungen und Behörden','setzen um','#376393'],['Medien','vermitteln','#794e7f'],['Öffentlichkeit','wählt – nur auf dieser Ebene','#436d39']];
      E.forEach(([a,b,c],i)=>{ const w=250+i*86, x=380-w/2, y=40+i*42;
        g+=`<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="${(0.2+i*0.3).toFixed(1)}s" dur="0.5s" fill="freeze"/><rect x="${x}" y="${y}" width="${w}" height="34" rx="9" fill="${c}" fill-opacity=".17" stroke="${c}" stroke-width="1.5"/>${T(380,y+15,a,'var(--ink)',11.5,800)}${T(380,y+28,b,'var(--muted)',9.5,600)}</g>`;
        if(i<E.length-1) g+=`<path d="M380 ${y+34} v8" stroke="var(--muted)" stroke-width="1.6"/><path d="M380 ${y+43} l-4 -6 h8z" fill="var(--muted)"/>`; });
      g+=T(380,306,'So ordnet er es in seinen Vorträgen; was Fachstellen dazu sagen, steht je Video unter „Abgleich & Daten“.','var(--muted)',9.5,600);
      return {vb:'0 0 760 316',breit:true,leg:[],svg:g}; },
    regenauer_weg(){ seed=5102; let g='';
      const T=(x,y,t,c='var(--ink)',s=11,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a}">${t}</text>`;
      g+=T(380,22,'Stationen nach eigenen Angaben','var(--ink)',13.5,800);
      const S=[['1978','geboren,','Bühl (Baden)','#436d39'],['1996','erstes Gewerbe,','Plattenlabel','#865324'],['danach','SAP-Berater,','IT-Projekte weltweit','#376393'],['2008','Umzug in','die Schweiz','#006f79'],['2021','Blog','regenauer.press','#794e7f'],['2022–25','vier Bände','im Eigenverlag','#8d4a43'],['2024','Vierteljahresschrift','Gegendruck','#6e6016']];
      g+=`<path d="M40 86 H720" stroke="var(--line)" stroke-width="3" stroke-linecap="round"/>`;
      S.forEach(([j,a,b,c],i)=>{ const x=62+i*106;
        g+=`<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="${(0.2+i*0.25).toFixed(2)}s" dur="0.45s" fill="freeze"/><circle cx="${x}" cy="86" r="9" fill="${c}"/><circle cx="${x}" cy="86" r="3.4" fill="#fff"/>${T(x,62,j,c,12.5,800)}${T(x,116,a,'var(--ink)',10,700)}${T(x,130,b,'var(--ink)',10,700)}</g>`; });
      g+=T(380,160,'Quelle: seine Angaben in den ausgewerteten Vorträgen und Gesprächen; Buchdaten nach Handel.','var(--muted)',9.5,600);
      return {vb:'0 0 760 172',breit:true,leg:[],svg:g}; },
