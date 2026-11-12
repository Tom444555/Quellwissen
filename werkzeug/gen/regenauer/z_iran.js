    iran_hebel(){ seed=7300; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3px">${t}</text>`;
      g+=T(380,20,'Vom Krieg zur Zuteilung – die Kette laut Regenauer (schematisch)',undefined,12.5,800);
      const S=[
        ['🎭 Bühne','#7a6a9a',['Iran-Krieg','Hormus gesperrt','tägliche Ankündigungen'],'[0:20–0:47]'],
        ['⛽ Mangel','#c08a3e',['Raffineriebrände','Preise steigen','Düngemittel knapp'],'[0:11–0:26]'],
        ['📏 Kontingent','#b05a4a',['20 l privat (Beispiel)','200 l Gewerbe','Rationierung'],'[0:18]'],
        ['📲 Zuteilung','#4a7aa8',['Bürger-Wallet','E-ID · digitaler Euro','Übergangsgeld'],'[0:18], [0:58]']];
      const w=160, h=128, y=48;
      S.forEach(([t,c,L,f],i)=>{ const x=22+i*186;
        g+=`<g opacity="0"><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="12" fill="${lg(shade(c,0.82),shade(c,0.64),90)}" stroke="${c}" stroke-width="1.5"/>`;
        g+=T(x+w/2,y+22,t,shade(c,-0.45),12,800);
        L.forEach((s,k)=>{ g+=`<rect x="${x+12}" y="${y+34+k*25}" width="${w-24}" height="20" rx="6" fill="${shade(c,0.9)}" stroke="${shade(c,0.35)}" stroke-width="0.8"/>`+T(x+w/2,y+48+k*25,s,'var(--ink)',9.3,650); });
        g+=T(x+w/2,y+h-8,f,'var(--muted)',8.5,600);
        if(i<S.length-1) g+=`<path d="M${x+w+4},${y+h/2} l18,0" stroke="${shade(c,-0.2)}" stroke-width="2.2" fill="none"/><path d="M${x+w+22},${y+h/2} l-7,-5 l0,10 z" fill="${shade(c,-0.2)}"/>`;
        g+=`<animate attributeName="opacity" from="0" to="1" dur=".45s" begin="${(0.2+i*0.4).toFixed(2)}s" fill="freeze"/></g>`; });
      // Ergebnis-Band
      const by=y+h+26;
      g+=`<g opacity="0"><path d="M${22+3*186+w/2},${y+h} L${22+3*186+w/2},${by} L560,${by}" stroke="#4a7aa8" stroke-width="1.6" fill="none"/>`;
      g+=`<rect x="200" y="${by-18}" width="360" height="36" rx="18" fill="${lg('#e9c9c0','#d9a99a',90)}" stroke="#a0503e" stroke-width="1.5"/>`;
      g+=T(380,by-2,'„digitaler Gulag“: völlige Abhängigkeit',shade('#a0503e',-0.4),11,800)+T(380,by+12,'Essen und Energie nur mit Nachweis [0:24–0:26], [0:58]','var(--muted)',8.5,600);
      g+=`<animate attributeName="opacity" from="0" to="1" dur=".45s" begin="1.9s" fill="freeze"/></g>`;
      // Gegenweg
      const gy=by+44;
      g+=`<g opacity="0"><rect x="120" y="${gy}" width="520" height="40" rx="10" fill="${lg('#d9e6c6','#bfd3a3',90)}" stroke="#5f8a3e" stroke-width="1.5" stroke-dasharray="5 3"/>`;
      g+=T(380,gy+17,'🌾 Gegenweg: zehn Leute im Ort – Mehl, Brot, Quelle, Generator',shade('#5f8a3e',-0.45),10.5,800)+T(380,gy+31,'Vereine · Netzwerke · Selbstorganisation [1:17–1:28]','var(--muted)',8.5,600);
      g+=`<animate attributeName="opacity" from="0" to="1" dur=".45s" begin="2.3s" fill="freeze"/></g>`;
      g+=T(380,gy+58,'Darstellung laut Regenauer – keine belegte Abfolge','var(--muted)',8.5,600);
      return {vb:'0 0 760 340', breit:true, leg:[], svg:g}; },
    iran_hormus(){ seed=7301; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3px">${t}</text>`;
      g+=T(380,20,'Straße von Hormus – Mengen 2024 und Ablauf Februar bis April 2026 (belegte Daten)',undefined,12,800);
      // Küsten schematisch
      let top='M20,70', bot='M20,170';
      for(let x=20;x<=360;x+=20){ top+=` L${x},${(60+Math.sin(x/40)*8+rnd()*6).toFixed(1)}`; bot+=` L${x},${(178+Math.cos(x/35)*8+rnd()*6).toFixed(1)}`; }
      g+=`<path d="${top} L360,30 L20,30 Z" fill="#d9c49a" stroke="#a88a5a" stroke-width="1.2"/>`;
      g+=`<path d="${bot} L360,205 L20,205 Z" fill="#d9c49a" stroke="#a88a5a" stroke-width="1.2"/>`;
      g+=`<rect x="20" y="76" width="340" height="94" fill="#a9c8d8" opacity="0.55"/>`;
      g+=T(70,48,'Iran','var(--ink)',10,800)+T(80,196,'Oman · VAE','var(--ink)',9.5,700);
      g+=T(190,90,'Straße von Hormus','#2f5a74',10.5,800);
      // Fluss-Pfeile
      [['Öl ≈ 20 Mio. Barrel/Tag','#8a5a2a',122],['LNG ≈ 1/5 des Welthandels','#4a7a5a',146]].forEach(([t,c,y],i)=>{
        g+=`<g opacity="0"><path d="M40,${y} L310,${y}" stroke="${c}" stroke-width="${i?5:8}" stroke-linecap="round"/><path d="M322,${y} l-14,-9 l0,18 z" fill="${c}"/>`+T(175,y-8,t,shade(c,-0.3),9.5,800);
        g+=`<animate attributeName="opacity" from="0" to="1" dur=".4s" begin="${(0.2+i*0.3).toFixed(2)}s" fill="freeze"/></g>`; });
      // Kennzahlen rechts
      const K=[['≈ 20 %','des Weltverbrauchs an Ölflüssigkeiten'],['> 25 %','des seegestützten Ölhandels'],['84 % / 83 %','Rohöl / LNG mit Ziel Asien'],['≈ 2,6 Mio.','Barrel/Tag Umgehung per Pipeline']];
      K.forEach(([a,b],i)=>{ const y=50+i*40;
        g+=`<g opacity="0"><rect x="384" y="${y}" width="356" height="32" rx="8" fill="${shade('#c08a3e',0.86)}" stroke="#c08a3e" stroke-width="1"/>`+T(396,y+21,a,shade('#c08a3e',-0.45),12,800,'start')+T(496,y+20,b,'var(--ink)',9.5,650,'start');
        g+=`<animate attributeName="opacity" from="0" to="1" dur=".35s" begin="${(0.8+i*0.2).toFixed(2)}s" fill="freeze"/></g>`; });
      g+=T(562,222,'Quelle: EIA (Juni 2025), Daten 2024','var(--muted)',8.5,600);
      // Zeitleiste 2026
      const ay=272, x0=50, x1=720, d0=0, d1=49; // Tage ab 28.02.
      const X=d=>R(x0+(d-d0)/(d1-d0)*(x1-x0));
      g+=`<path d="M${x0},${ay} L${x1},${ay}" stroke="var(--line)" stroke-width="2"/>`;
      const E=[[0,'28.02.','Angriffe beginnen','#b05a4a'],[1,'01.03.','Hormus gesperrt','#8a5a2a'],[11,'11.03.','IEA: 400 Mio. Barrel','#c08a3e'],[39,'08.04.','Waffenruhe','#5f8a3e'],[42,'11.04.','Islamabad ohne Ergebnis','#7a6a9a'],[44,'13.04.','US-Blockade iran. Häfen','#4a7aa8'],[48,'17.04.','Paris-Konferenz','#4a7aa8']];
      E.forEach(([d,z,t,c],i)=>{ const x=X(d), up=i%2==0, lvl=Math.floor(i/2)%2, y=up? ay-14-lvl*22 : ay+22+lvl*22;
        const anc = x<110?'start':(x>650?'end':'middle');
        g+=`<g opacity="0"><circle cx="${x}" cy="${ay}" r="5" fill="${c}"/><path d="M${x},${ay} L${x},${up?y+4:y-10}" stroke="${c}" stroke-width="1"/>`+T(x,y,z+' '+t,shade(c,-0.4),8.8,750,anc);
        g+=`<animate attributeName="opacity" from="0" to="1" dur=".35s" begin="${(1.6+i*0.2).toFixed(2)}s" fill="freeze"/></g>`; });
      g+=T(380,334,'Quellen: IEA, Unione Sarda, Business Today, Bundesregierung (2026)','var(--muted)',8.5,600);
      return {vb:'0 0 760 345', breit:true, leg:[], svg:g}; },
