    schrang_kette(){ seed=7800; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3px">${t}</text>`;
      const A=(d,b)=>`<animate attributeName="opacity" from="0" to="1" dur=".45s" begin="${b}s" fill="freeze"/>`;
      g+=T(380,18,'Krieg braucht Personal – wo die Kette reißen kann (Darstellung laut Schrang und Soufi-Siavash, schematisch)',undefined,11.5,800);
      const B=[
        ['👔 Wenige „ganz oben“','#9a6a4a',['entscheiden, verdienen','„die Knöpfe drücken“'],'[0:20], [0:48]'],
        ['📺 Erzählung','#b08a3e',['Werbung, Hollywood,','Talkshows: Abenteuer'],'[0:08], [0:41]'],
        ['📋 Musterung','#6f8a5a',['Gehorsam aus der Schule:','„Darf ich das?“'],'[0:20], [1:08]'],
        ['🪖 Front','#8a5a5a',['viele, die einander','nie getroffen haben'],'[1:01], [1:31]']];
      B.forEach(([t,c,L,f],i)=>{ const x=22+i*186, y=40, w=160, h=96;
        g+=`<g opacity="0"><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="12" fill="${lg(shade(c,0.78),shade(c,0.58),90)}" stroke="${c}" stroke-width="1.5"/>`;
        g+=T(x+w/2,y+22,t,shade(c,-0.45),11.5,800);
        L.forEach((s,k)=>{ g+=T(x+w/2,y+45+k*15,s,'var(--ink)',9.5,600); });
        g+=T(x+w/2,y+h-10,f,'var(--muted)',8.5,600);
        if(i<3){ const ax=x+w+2; g+=`<path d="M${ax},${y+h/2} l20,0" stroke="var(--line)" stroke-width="2" fill="none"/><path d="M${ax+20},${y+h/2-5} l7,5 l-7,5 z" fill="var(--line)"/>`; }
        g+=A(0,(0.2+i*0.3).toFixed(2))+`</g>`; });
      // Bruchstelle zwischen Musterung und Front
      const bx=22+3*186-14;
      g+=`<g opacity="0"><path d="M${bx},34 l-6,14 l8,10 l-7,14 l8,12 l-6,14 l7,12 l-6,16" stroke="#b5452f" stroke-width="2.6" fill="none" stroke-linecap="round"/>`;
      g+=`<rect x="${bx-150}" y="150" width="300" height="58" rx="10" fill="${lg('#f3dcd2','#e9c6b6',90)}" stroke="#b5452f" stroke-width="1.4"/>`;
      g+=T(bx,170,'✋ „Ich bin nicht dabei“ – Verweigerung',shade('#b5452f',-0.3),11,800);
      g+=T(bx,186,'Art. 4 Abs. 3 GG · „20 % Sand im Getriebe“','var(--ink)',9.5,650);
      g+=T(bx,200,'[0:20], [1:13]','var(--muted)',8.5,600);
      g+=`<path d="M${bx},150 L${bx},${40+96+2}" stroke="#b5452f" stroke-width="1.2" stroke-dasharray="3 3" fill="none"/>`+A(0,'1.45')+`</g>`;
      // Gegenmittel
      const M=[['🖼️ Krieg zeigen, wie er ist','Veteranen, Prothesen, Opferbilder','[0:09], [0:22], [0:44]','#7a8aa8'],
               ['🤝 Reden statt schießen','Dialog, Vergebung (Schrang)','[0:24], [1:15]','#8a7aa0'],
               ['✝️ Gewissen','„Du sollst nicht töten“','[0:55], [1:33]','#6a8a7a']];
      g+=`<g opacity="0">`+T(380,232,'Gegenmittel, die im Gespräch genannt werden','var(--muted)',10,700);
      M.forEach(([t,s,f,c],i)=>{ const x=40+i*235, y=242, w=210;
        g+=`<rect x="${x}" y="${y}" width="${w}" height="68" rx="10" fill="${shade(c,0.82)}" stroke="${c}" stroke-width="1.2"/>`;
        g+=T(x+w/2,y+20,t,shade(c,-0.45),10.5,800)+T(x+w/2,y+38,s,'var(--ink)',9.5,600)+T(x+w/2,y+56,f,'var(--muted)',8.5,600); });
      g+=A(0,'1.9')+`</g>`;
      return {vb:'0 0 760 322', breit:true, leg:[], svg:g}; },
    schrang_daten(){ seed=7801; let g='';
      const T=(x,y,t,c='var(--ink)',s=10,w=700,a='middle')=>`<text x="${x}" y="${y}" style="fill:${c};font:${w} ${s}px var(--label);text-anchor:${a};paint-order:stroke;stroke:var(--surface);stroke-width:3px">${t}</text>`;
      g+=T(380,18,'Deutschland: Verteidigungsausgaben und der neue Wehrdienst (belegte Daten)',undefined,12,800);
      // linkes Feld: % des BIP
      const D=[[2014,1.16],[2015,1.16],[2016,1.18],[2017,1.21],[2018,1.23],[2019,1.33],[2020,1.49],[2021,1.43],[2022,1.48],[2023,1.61],[2024,2.00]];
      const x0=50, y0=250, H=170, mx=2.2, bw=24, gap=7;
      g+=T(200,42,'Verteidigungsausgaben in % des BIP (NATO)','var(--muted)',10,700);
      g+=`<path d="M${x0-6},${y0} L${x0+D.length*(bw+gap)+4},${y0}" stroke="var(--line)" stroke-width="1.2"/>`;
      const y2=y0-2/mx*H;
      g+=`<path d="M${x0-6},${R(y2)} L${x0+D.length*(bw+gap)+4},${R(y2)}" stroke="#b5452f" stroke-width="1.2" stroke-dasharray="5 4"/>`+T(x0,R(y2)-6,'NATO-Ziel 2 %','#b5452f',8.5,700,'start');
      D.forEach(([j,v],i)=>{ const h=v/mx*H, x=x0+i*(bw+gap), y=y0-h;
        g+=`<rect x="${x}" y="${R(y)}" width="${bw}" height="${R(h)}" rx="3" fill="${i==D.length-1?'#b08a3e':'#7f9a6a'}" stroke="${i==D.length-1?'#8a6a2a':'#5f7a4a'}" stroke-width="1"><animate attributeName="height" from="0" to="${R(h)}" dur=".5s" begin="${(i*0.08).toFixed(2)}s" fill="freeze"/><animate attributeName="y" from="${y0}" to="${R(y)}" dur=".5s" begin="${(i*0.08).toFixed(2)}s" fill="freeze"/></rect>`;
        g+=T(x+bw/2,R(y)-5,v.toFixed(2).replace('.',','),'var(--ink)',8,700);
        g+=T(x+bw/2,y0+13,"'"+String(j).slice(2),'var(--muted)',8.5,600); });
      g+=T(200,y0+32,'2024 Schätzung · Quelle: NATO, Stand 03.06.2025','var(--muted)',8.5,600);
      // rechtes Feld: Zeitleiste Wehrdienst
      const S=[['05.12.2025','Bundestag beschließt neuen Wehrdienst'],['19.12.2025','Bundesrat billigt das Gesetz'],['01.01.2026','in Kraft: Fragebogen-Pflicht für Männer ab Jg. 2008'],['bis Mitte 2027','bis zu 24 Musterungszentren'],['2031','Ziel: 203.000 aktive Soldaten'],['2035','Ziel: 460.000 mit Reserve']];
      const lx=440, ly=68, st=37;
      g+=T(590,42,'Neuer Wehrdienst – Fahrplan (BMVg, Wehrbeauftragte)','var(--muted)',10,700);
      g+=`<path d="M${lx},${ly} L${lx},${ly+5*st}" stroke="var(--line)" stroke-width="1.6"/>`;
      S.forEach(([d,t],i)=>{ const y=ly+i*st;
        g+=`<g opacity="0"><circle cx="${lx}" cy="${y}" r="6" fill="${i<3?'#b08a3e':'#7a8aa8'}" stroke="var(--surface)" stroke-width="1.5"/>`;
        g+=T(lx+14,y-3,d,shade(i<3?'#b08a3e':'#7a8aa8',-0.4),10,800,'start')+T(lx+14,y+12,t,'var(--ink)',9.5,600,'start');
        g+=`<animate attributeName="opacity" from="0" to="1" dur=".4s" begin="${(0.9+i*0.2).toFixed(2)}s" fill="freeze"/></g>`; });
      g+=T(590,y0+32,'Dienst vorerst freiwillig – Pflicht nur bei verfehlten Zielen per neuem Gesetz','var(--muted)',8.5,600);
      g+=T(590,y0+46,'Ende 2024: 181.174 aktive Soldaten (Wehrbeauftragte)','var(--muted)',8.5,600);
      return {vb:'0 0 760 306', breit:true, leg:[], svg:g}; },
