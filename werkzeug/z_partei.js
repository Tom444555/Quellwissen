    partei_schritte(){ seed=1011; let g='';
      const S=[['1','Gründungs­versammlung','Mitglieder, Name, Satzung, Programm beschließen','#4a8ac8'],['2','Vorstand wählen','mindestens 3 Personen, Schatzmeister','#3a6a9a'],['3','Unterlagen melden','Satzung, Programm, Vorstand an die Bundeswahlleiterin','#6a5a9a'],['4','Aufbauen','Landesverbände, Konto, Finanzordnung, Mitglieder','#2a8a6a'],['5','Wahl anzeigen','97 Tage vorher, Parteieigenschaft wird geprüft','#c87a30'],['6','Unter­schriften','Kandidaten geheim wählen, Unterstützer sammeln','#b04a4a'],['7','Rechenschaft','jährlicher Finanzbericht, Spenden offenlegen','#7a7a7a']];
      const T=(x,y,t,c='var(--ink)',s=10,w=700)=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:middle">${t}</text>`;
      g+=T(380,16,'Parteigründung in Deutschland – Schritt für Schritt',undefined,12.5,800);
      const bw=98, gap=8.6;
      S.forEach(([n,t,u,c],i)=>{ const x=12+i*(bw+gap), y=34;
        g+=`<g opacity="0"><rect x="${x}" y="${y}" width="${bw}" height="128" rx="10" fill="${lg(shade(c,0.75),shade(c,0.55),90)}" stroke="${c}" stroke-width="1.4"/><circle cx="${x+bw/2}" cy="${y+22}" r="14" fill="${c}"/>`+T(x+bw/2,y+27,n,'#fff',13,800);
        const w1=t.split('­'); w1.forEach((s,k)=>g+=T(x+bw/2,y+54+k*12,s+(k<w1.length-1?'-':''),shade(c,-0.4),10,800));
        const ws=u.split(' '); let z='',zl=[]; ws.forEach(w=>{ if((z+' '+w).length>17){ zl.push(z); z=w; } else z=z?z+' '+w:w; }); zl.push(z);
        zl.forEach((s,k)=>g+=T(x+bw/2,y+86+k*11,s,'var(--ink)',8.6,600));
        g+=`<animate attributeName="opacity" from="0" to="1" dur=".4s" begin="${(i*0.3).toFixed(1)}s" fill="freeze"/></g>`;
        if(i<S.length-1) g+=`<path d="M${x+bw+1},${y+64} l${gap-2},0" stroke="var(--muted)" stroke-width="1.6"/>`; });
      return {vb:'0 0 760 172',breit:true,leg:[],svg:g}; },
