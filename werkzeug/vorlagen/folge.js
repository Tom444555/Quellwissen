/* Quellwissen · Folgen-Modul: Kopfkarte, Gesprächsverlauf, aufklappbare Abschnitte, Zeitachse, Balken, Zahlenvergleich, Sprungmarken ins Video */
window.QWFolge=(function(){
  const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const F=['#436d39','#376393','#865324','#794e7f','#8d4a43','#6e6016','#006f79','#5a6826','#605791','#8b4e32'];
  const api={inline:esc};
  const inl=t=>api.inline(t);
  const sek=t=>{ const m=/^(\d+):(\d\d)$/.exec(String(t||'').trim()); return m?(+m[1])*3600+(+m[2])*60:0; };
  const zahl=(v,dez)=>v==null||isNaN(v)?'–':Number(v).toLocaleString('de-DE',{minimumFractionDigits:dez||0,maximumFractionDigits:dez==null?(Math.abs(v)<10&&v%1?1:(v%1?1:0)):dez});
  let S={urls:{},th:null,eintrag:null,pre:''};
  const LM={'💬':'zitat','📌':'merk','🔗':'link','📚':'buch','❓':'frage'};
  const li=x=>{ const m=/^(💬|📌|🔗|📚|❓)\s*/u.exec(x); return m?`<li class="li-m li-${LM[m[1]]}"><span class="li-i">${m[1]}</span><span>${inl(x.slice(m[0].length))}</span></li>`:`<li>${inl(x)}</li>`; };

  /* ---- Seitenstart: Video-Adressen je Reiter merken ---- */
  api.start=function(p,pre){ S={urls:{},th:null,eintrag:p,pre:pre||''};
    (p.reiter||[]).forEach(r=>(r.bloecke||[]).forEach(b=>{ if(b.typ==='folge'&&b.url){ wege(b).forEach(w=>S.urls[w[0]]=b.url); S.urls[r.id]=b.url; } })); };
  api.reiter=function(){ S.th=null; };
  function wege(b){ const k=b.k||''; return b.wege||[[k+'ab','📖','Gespräch im Detail','Abschnitt für Abschnitt, mit Zitaten'],[k+'zeit','📅','Zeitachse & Verzeichnisse','Ereignisse, Personen, Orte, Begriffe'],[k+'abgleich','⚖️','Abgleich & Daten','Aussagen neben Daten, Diagramme, Quellen']]; }

  /* ---- Kopfkarte einer Folge ---- */
  api.folge=function(b,pid){
    const W=wege(b).map(w=>`<a class="fo-weg" href="#${esc(pid)}-${esc(w[0])}"><span class="fo-wi">${w[1]}</span><span class="fo-wt"><strong>${esc(w[2])}</strong><small>${esc(w[3]||'')}</small></span><span class="fo-wp" aria-hidden="true">›</span></a>`).join('');
    const WG=wege(b), ziel=l=>/Abschn/.test(l)?WG[0][0]:/Zeit/.test(l)?WG[1][0]:/Abgleich|Diagramm|Verl|Quelle/.test(l)?WG[2][0]:'';
    const K=(b.kacheln||[]).map(k=>{ const z=ziel(k[1]); return z?`<a class="fo-ka fo-weg0" href="#${esc(pid)}-${esc(z)}"><strong>${esc(k[0])}</strong><span>${esc(k[1])} ›</span></a>`:`<button type="button" class="fo-ka" data-kern="1"><strong>${esc(k[0])}</strong><span>${esc(k[1])} ↓</span></button>`; }).join('');
    return `<section class="fo-kopf">
      <div class="fo-auge">${esc(b.art||'Podcast-Folge')}${b.kanal?' · '+esc(b.kanal):''}</div>
      <h3 class="fo-titel">${esc(b.titel)}</h3>
      <div class="fo-gast"><strong>${esc(b.gast||'')}</strong>${b.rolle?' · '+esc(b.rolle):''}</div>
      ${b.thema?`<p class="fo-thema">${inl(b.thema)}</p>`:''}
      <div class="fo-zeile">${b.datum?`<span class="fo-chip">📅 ${esc(b.datum)}</span>`:''}${b.dauer?`<span class="fo-chip">⏱ ${esc(b.dauer)}</span>`:''}${b.url?`<a class="fo-play" href="${esc(b.url)}" target="_blank" rel="noopener"><span aria-hidden="true">▶</span> Video ansehen</a>`:''}</div>
      ${K?`<div class="fo-kacheln">${K}</div>`:''}
      <nav class="fo-wege" aria-label="Bereiche dieser Folge">${W}</nav>
    </section>`; };

  /* ---- Übersicht aller Folgen als Karten ---- */
  api.folgenkarten=function(b,pid){ const p=S.eintrag; if(!p) return '';
    const L=[]; p.reiter.forEach(r=>r.bloecke.forEach(x=>{ if(x.typ==='folge') L.push([r,x]); }));
    return `<div class="fo-liste">${L.map(([r,x])=>`<a class="fo-karte" href="#${esc(pid)}-${esc(r.id)}"><div class="fo-kg">${esc(x.karte||x.gast||'')}</div><div class="fo-kt">${esc(x.titel)}</div>${x.thema?`<p>${inl(x.thema)}</p>`:''}<div class="fo-km">${x.datum?`<span>📅 ${esc(x.datum)}</span>`:''}${x.dauer?`<span>⏱ ${esc(x.dauer)}</span>`:''}<span class="fo-auf">Auswertung öffnen ›</span></div></a>`).join('')}</div>`; };

  /* ---- Gesprächsverlauf (Band + Themenanteile) ---- */
  api.gespraech=function(b){
    const T=b.teile||[], TH=b.themen||[]; if(!T.length) return '';
    const farbe={}, name={}; TH.forEach((t,i)=>{ farbe[t.k]=t.farbe||F[i%F.length]; name[t.k]=t.n; }); S.th={farbe,name};
    const ende=Math.max(sek(b.dauer),...T.map(t=>sek(t.bis))), ges=ende||1, min={};
    const seg=T.map((t,i)=>{ const d=Math.max(sek(t.bis)-sek(t.von),60); if(t.th) min[t.th]=(min[t.th]||0)+d/60;
      const c=t.th&&farbe[t.th]?farbe[t.th]:(i%2?'var(--muted)':'var(--ink-3,var(--muted))');
      return `<button type="button" class="gv-seg" data-von="${esc(t.von)}" data-th="${esc(t.th||'')}" style="flex:${d} 1 0;background:${c}" title="${esc(t.von+'–'+t.bis+' · '+t.t)}" aria-label="${esc(t.von+' bis '+t.bis+': '+t.t)}"></button>`; }).join('');
    const h=Math.floor(ges/3600), marken=[]; for(let i=0;i<=h;i++) marken.push(`<span style="left:${(i*3600/ges*100).toFixed(2)}%">${i}:00</span>`);
    const sum=Object.values(min).reduce((a,x)=>a+x,0)||1, mx=Math.max(1,...Object.values(min));
    const anteile=TH.filter(t=>min[t.k]).sort((a,c)=>min[c.k]-min[a.k]).map(t=>`<button type="button" class="gv-th" data-th="${esc(t.k)}" aria-pressed="false"><span class="gv-pk" style="background:${farbe[t.k]}"></span><span class="gv-tn">${esc(t.n)}</span><span class="gv-bal"><i style="width:${(min[t.k]/mx*100).toFixed(1)}%;background:${farbe[t.k]}"></i></span><span class="gv-tw">${Math.round(min[t.k])} Min. · ${Math.round(min[t.k]/sum*100)} %</span></button>`).join('');
    return `<figure class="gv" data-gv>
      ${b.titel?`<figcaption class="pd-titel">${esc(b.titel)}</figcaption>`:''}
      <div class="gv-band" role="group" aria-label="Abschnitte entlang der Gesprächszeit">${seg}</div>
      <div class="gv-achse" aria-hidden="true">${marken.join('')}</div>
      <p class="gv-info" aria-live="polite">Band antippen: springt zum Abschnitt. ${T.length} Abschnitte in ${esc(b.dauer||'')} Std.</p>
      ${anteile?`<div class="gv-kopf">Themenanteile <small>antippen filtert die Abschnitte</small></div><div class="gv-themen">${anteile}</div>`:''}
    </figure>`; };

  /* ---- Aufklappbarer Abschnitt (Titel endet mit [h:mm–h:mm]) ---- */
  api.istAbschnitt=b=>!!(b.liste&&/\[\d{1,2}:\d\d(?:\s*[–-]\s*\d{1,2}:\d\d)?\]\s*$/.test(b.titel||''));
  api.abschnitt=function(b){
    const m=/\s*\[(\d{1,2}:\d\d)(?:\s*[–-]\s*(\d{1,2}:\d\d))?\]\s*$/.exec(b.titel), t=b.titel.slice(0,m.index);
    const th=b.th&&S.th?S.th:null, c=th&&th.farbe[b.th]?th.farbe[b.th]:'var(--tc,var(--accent))';
    const L=b.liste.slice(), kopf=L.length&&!/^(💬|📌|🔗|📚|❓)/u.test(L[0])?L.shift():'';
    return `<details class="ab-akk" data-von="${m[1]}" data-th="${esc(b.th||'')}" style="--thc:${c}">
      <summary><span class="ab-zeit">${m[1]}${m[2]?'–'+m[2]:''}</span><span class="ab-t">${esc(t)}</span>${th&&th.name[b.th]?`<span class="ab-th">${esc(th.name[b.th])}</span>`:''}<span class="ab-pf" aria-hidden="true"></span></summary>
      <div class="ab-k">${kopf?`<p class="ab-lead">${inl(kopf)} <span class="ab-sprung">[${m[1]}]</span></p>`:''}${L.length?`<ul>${L.map(li).join('')}</ul>`:''}</div>
    </details>`; };

  /* ---- Zeitachse ---- */
  const EPO=[[-1e9,'Vorgeschichte und Antike'],[500,'Mittelalter'],[1500,'Frühe Neuzeit'],[1800,'19. Jahrhundert'],[1914,'1914–1945'],[1945,'1945–1989'],[1990,'1990–2019'],[2020,'Seit 2020']];
  function jahr(z){ const s=String(z||''); let m;
    if((m=/vor\s+(?:ca\.|etwa|rund)?\s*([\d.]+)\s*(Mio\.|Millionen|Mrd\.)?\s*Jahren/i.exec(s))){ const n=+m[1].replace(/\./g,'')*(m[2]?(/Mrd/.test(m[2])?1e9:1e6):1); return 2026-n; }
    if((m=/(\d{1,5})\s*v\.\s*Chr/.exec(s))) return -(+m[1]);
    if((m=/(\d{1,2})\.\s*(?:Jh|Jahrhundert)/.exec(s))) return (+m[1]-1)*100+1;
    if((m=/(?:^|[^\d.])(\d{4})(?!\d)/.exec(' '+s))) return +m[1];
    if((m=/(?:^|\D)(\d{3})(?!\d)\s*(?:n\.\s*Chr)?/.exec(' '+s))&&/n\.\s*Chr|^\D*\d{3}\D*$/.test(s)) return +m[1];
    if(/Steinzeit|Eiszeit|Urzeit/i.test(s)) return -10000; if(/Antike|Altertum|Römer|römisch/i.test(s)) return -100; if(/Mittelalter/i.test(s)) return 1000;
    if(/DDR/i.test(s)) return 1970; if(/Nachkrieg/i.test(s)) return 1950; if(/heute|aktuell|derzeit/i.test(s)) return 2026;
    return null; }
  const epoche=j=>{ let e=EPO[0][1]; for(const [ab,n] of EPO) if(j>=ab) e=n; return e; };
  api.zeitachse=function(b){
    let E;
    if(b.eintraege) E=b.eintraege.map(x=>({z:x.z,t:x.t,j:x.j,e:!!x.e,x:[x.f?['Fundstelle',x.f]:null,x.o?['Ort',x.o]:null].filter(Boolean)}));
    else E=b.zeilen.map(r=>{ let z=String(r[0]||''), t=String(r[1]||''), e=false; if(/^📚\s*/u.test(z)){ e=true; z=z.replace(/^📚\s*/u,''); } if(/^📚\s*/u.test(t)){ e=true; t=t.replace(/^📚\s*/u,''); }
      return {z,t,e,x:r.slice(2).map((v,i)=>v?[String(b.kopf[i+2]||'').replace(/^\P{L}+/u,''),v]:null).filter(Boolean)}; });
    let vor=null; E.forEach(x=>{ const j=x.j!=null?x.j:jahr(x.z); x.j=j; x.ep=j!=null?epoche(j):vor; if(x.ep) vor=x.ep; });
    const erste=E.find(x=>x.ep); E.forEach(x=>{ if(!x.ep) x.ep=erste?erste.ep:''; });
    const gr=[]; E.forEach(x=>{ if(!gr.length||gr[gr.length-1].n!==x.ep) gr.push({n:x.ep,L:[]}); gr[gr.length-1].L.push(x); });
    const mitEp=gr.length>1&&gr.every(g=>g.n), hatErg=E.some(x=>x.e)&&E.some(x=>!x.e), id='za'+Math.random().toString(36).slice(2,8);
    const eintrag=x=>`<li class="za-e${x.e?' za-erg':''}"><div class="za-z">${inl(x.z)}</div><div class="za-p" aria-hidden="true"></div><div class="za-k"><div class="za-t">${inl(x.t)}</div>${x.x.filter(a=>a[1].length>44).map(([k,v])=>`<div class="za-n">${k?`<small>${esc(k)}</small> `:''}${inl(v)}</div>`).join('')}${x.e||x.x.some(a=>a[1].length<=44)?`<div class="za-x">${x.e?'<span class="za-b">📚 ergänzt</span>':''}${x.x.filter(a=>a[1].length<=44).map(([k,v])=>`<span class="za-m">${/Fundstelle|Quelle/.test(k)?'':`<small>${esc(k)}</small> `}${inl(v)}</span>`).join('')}</div>`:''}</div></li>`;
    const titel=b.titel||(b.kopf?String(b.kopf[0]).replace(/^📅\s*/u,'')+' und '+b.kopf[1]:'');
    return `<figure class="za" data-za>
      ${b.titel?`<figcaption class="pd-titel">${esc(b.titel)}</figcaption>`:''}
      <div class="za-leiste">${hatErg?`<div class="za-filter" role="group" aria-label="Einträge filtern"><button type="button" data-zf="alle" aria-pressed="true">Alle <small>${E.length}</small></button><button type="button" data-zf="orig" aria-pressed="false">Im Text genannt <small>${E.filter(x=>!x.e).length}</small></button><button type="button" data-zf="erg" aria-pressed="false">📚 Ergänzt <small>${E.filter(x=>x.e).length}</small></button></div>`:`<span class="za-anz">${E.length} Einträge${titel&&!b.titel?' · '+esc(titel):''}</span>`}
      ${mitEp?`<div class="za-spr" role="group" aria-label="Zu einem Zeitabschnitt springen">${gr.map((g,i)=>`<button type="button" data-zs="${id}-${i}">${esc(g.n)} <small>${g.L.length}</small></button>`).join('')}</div>`:''}</div>
      ${gr.map((g,i)=>`<section class="za-g" id="${id}-${i}">${mitEp?`<h4 class="za-ep"><span>${esc(g.n)}</span></h4>`:''}<ol class="za-l">${g.L.map(eintrag).join('')}</ol></section>`).join('')}
    </figure>`; };

  /* ---- Balken (Kategorienvergleich) ---- */
  api.balken=function(b){ const Z=b.zeilen||[], mx=Math.max(...Z.map(z=>Math.abs(z[1])),1e-9), eh=b.einheit?' '+b.einheit:'';
    return `<figure class="ku-fig fb">${b.titel?`<figcaption class="pd-titel">${esc(b.titel)}</figcaption>`:''}
      <div class="fb-l">${Z.map((z,i)=>`<div class="fb-z"><span class="fb-n">${inl(z[0])}</span><span class="fb-b"><i style="width:${(Math.abs(z[1])/mx*100).toFixed(1)}%;animation-delay:${i*40}ms${z[2]?';background:'+esc(z[2]):''}"></i></span><span class="fb-w">${zahl(z[1],b.dez)}${esc(eh)}</span></div>`).join('')}</div>
      ${b.quelle?`<p class="fb-q">Quelle: ${inl(b.quelle)}</p>`:''}${b.hinweis?`<p class="fb-q">${inl(b.hinweis)}</p>`:''}</figure>`; };

  /* ---- Zahlenvergleich: im Gespräch genannt / Daten laut Quelle ---- */
  api.vergleich=function(b){ const la=b.la||'Im Gespräch genannt', lb=b.lb||'Daten laut Quelle';
    return `<figure class="ku-fig fv">${b.titel?`<figcaption class="pd-titel">${esc(b.titel)}</figcaption>`:''}
      <div class="fv-leg"><span><i class="fv-a"></i>${esc(la)}</span><span><i class="fv-b"></i>${esc(lb)}</span></div>
      ${(b.zeilen||[]).map(z=>{ const mx=Math.max(Math.abs(z.a||0),Math.abs(z.b||0),1e-9), eh=z.einheit?' '+z.einheit:(b.einheit?' '+b.einheit:'');
        const bal=(v,k,t)=>`<div class="fv-r"><span class="fv-b0"><i class="${k}" style="width:${(Math.abs(v||0)/mx*100).toFixed(1)}%"></i></span><span class="fv-w">${t?inl(t):zahl(v,z.dez)+esc(eh)}</span></div>`;
        return `<div class="fv-z"><div class="fv-n">${inl(z.n)}${z.f?` <span class="fv-f">${inl(z.f)}</span>`:''}</div>${bal(z.a,'fv-a',z.at)}${bal(z.b,'fv-b',z.bt)}${z.q?`<div class="fv-q">Quelle: ${inl(z.q)}</div>`:''}</div>`; }).join('')}
      ${b.hinweis?`<p class="fb-q">${inl(b.hinweis)}</p>`:''}</figure>`; };

  /* ---- Reiter fertigstellen: Werkzeugleiste + Sprungmarken ins Video ---- */
  api.panel=function(r,html){
    const n=(html.match(/<details class="ab-akk"/g)||[]).length;
    if(n>=4) html=html.replace('<details class="ab-akk"',`<div class="ab-werk"><span>${n} Abschnitte</span><button type="button" data-ab-alle="1">Alle öffnen</button></div><details class="ab-akk"`);
    let url=S.urls[r.id]; if(!url) return html;
    const basis=url+(url.indexOf('?')<0?'?':'&')+'t=';
    let tief=0; const zu=/^<(a|summary|svg|button|script|figcaption)\b/i, auf=/^<\/(a|summary|svg|button|script|figcaption)>/i;
    return html.split(/(<[^>]+>)/).map(s=>{ if(s[0]==='<'){ if(zu.test(s)&&!/\/>$/.test(s)) tief++; else if(auf.test(s)) tief=Math.max(0,tief-1); return s; }
      if(tief) return s;
      return s.replace(/\[(\d{1,2}):(\d\d)((?:\s*[–-]\s*\d{1,2}:\d\d)?)\]/g,(m,h,mi,rest)=>`<a class="zs" href="${esc(basis)}${(+h)*3600+(+mi)*60}s" target="_blank" rel="noopener" title="Im Video an diese Stelle springen">▸ ${h}:${mi}${rest}</a>`); }).join(''); };

  /* ---- Bedienung nach dem Seitenaufbau ---- */
  api.init=function(main){
    main.querySelectorAll('[data-kern]').forEach(k=>k.addEventListener('click',()=>{ const P=k.closest('.panel'), z=P&&[...P.querySelectorAll('table')].find(t=>{ const th=t.querySelector('th'); return th&&th.textContent.trim()==='#'; }); if(z){ const kp=document.querySelector('.kopf'), y=z.getBoundingClientRect().top+scrollY-((kp&&kp.offsetHeight)||60)-110; scrollTo({top:y,behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'auto':'smooth'}); } }));
    main.querySelectorAll('a.fo-weg,a.fo-weg0').forEach(a=>a.addEventListener('click',ev=>{ const rid=a.getAttribute('href').split('-').pop(), k=main.querySelector('.reiter button[data-r="'+rid+'"]'); if(k){ ev.preventDefault(); k.click(); const an=document.getElementById('reiteranker'); if(an) an.scrollIntoView(); } }));
    main.querySelectorAll('[data-ab-alle]').forEach(k=>k.addEventListener('click',()=>{ const P=k.closest('.panel'), D=[...P.querySelectorAll('details.ab-akk:not([hidden])')], auf=D.some(d=>!d.open); D.forEach(d=>d.open=auf); k.textContent=auf?'Alle schließen':'Alle öffnen'; }));
    main.querySelectorAll('[data-gv]').forEach(g=>{ const P=g.closest('.panel')||main, info=g.querySelector('.gv-info');
      g.querySelectorAll('.gv-seg').forEach(s=>s.addEventListener('click',()=>{ const d=P.querySelector('details.ab-akk[data-von="'+s.dataset.von+'"]'); g.querySelectorAll('.gv-seg').forEach(x=>x.classList.toggle('an',x===s)); if(info) info.textContent=s.title;
        if(d){ d.hidden=false; d.open=true; const k=document.querySelector('.kopf,header'), y=d.getBoundingClientRect().top+scrollY-((k&&k.offsetHeight)||60)-70; scrollTo({top:y,behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'auto':'smooth'}); d.classList.add('ab-blink'); setTimeout(()=>d.classList.remove('ab-blink'),1600); } }));
      g.querySelectorAll('.gv-th').forEach(t=>t.addEventListener('click',()=>{ const an=t.getAttribute('aria-pressed')!=='true'; g.querySelectorAll('.gv-th').forEach(x=>x.setAttribute('aria-pressed',x===t&&an)); const th=an?t.dataset.th:'';
        g.querySelectorAll('.gv-seg').forEach(x=>x.classList.toggle('aus',!!th&&x.dataset.th!==th)); let z=0; P.querySelectorAll('details.ab-akk').forEach(d=>{ d.hidden=!!th&&d.dataset.th!==th; if(!d.hidden) z++; });
        const w=P.querySelector('.ab-werk span'); if(w) w.textContent=z+' Abschnitte'+(th?' · Thema „'+t.querySelector('.gv-tn').textContent+'“':''); })); });
    main.querySelectorAll('[data-za]').forEach(z=>{
      z.querySelectorAll('[data-zf]').forEach(k=>k.addEventListener('click',()=>{ z.querySelectorAll('[data-zf]').forEach(x=>x.setAttribute('aria-pressed',x===k)); const f=k.dataset.zf;
        z.querySelectorAll('.za-e').forEach(e=>{ const erg=e.classList.contains('za-erg'); e.hidden=f==='orig'?erg:f==='erg'?!erg:false; }); z.querySelectorAll('.za-g').forEach(g=>g.hidden=!g.querySelector('.za-e:not([hidden])')); }));
      z.querySelectorAll('[data-zs]').forEach(k=>k.addEventListener('click',()=>{ const d=document.getElementById(k.dataset.zs); if(d&&!d.hidden){ const kp=document.querySelector('.kopf,header'), y=d.getBoundingClientRect().top+scrollY-((kp&&kp.offsetHeight)||60)-64; scrollTo({top:y,behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'auto':'smooth'}); } })); });
  };
  return api;
})();
