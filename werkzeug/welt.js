/* Quellwissen · Weltkarte (eigenständiges Modul, offline) */
(function(){
const $=(s,r=document)=>r.querySelector(s);
const R2=Math.PI/180;
let DAT=null;
function daten(){ if(!DAT){ DAT=JSON.parse(document.getElementById('weltdaten').textContent); DAT.idx={}; DAT.laender.forEach(c=>{ DAT.idx[c.i]=c; let x0=1e9,x1=-1e9,y0=1e9,y1=-1e9; c.p.forEach(r=>r.forEach(([x,y])=>{x0=Math.min(x0,x);x1=Math.max(x1,x);y0=Math.min(y0,y);y1=Math.max(y1,y);})); c.bb=[x0,x1,y0,y1]; let sx=0,sy=0,n=0,best=0,bi=0; c.p.forEach((r,k)=>{ if(r.length>best){best=r.length;bi=k;} }); c.p[bi].forEach(([x,y])=>{sx+=x;sy+=y;n++;}); c.mitte=[sx/n,sy/n]; }); DAT.rmap={}; DAT.raster.forEach(g=>{ if(!g[5]) DAT.rmap[g[0]+','+g[1]]=g; }); } return DAT; }

/* ---------- kuratierte Daten (gerundet) ---------- */
const GETREIDE={
 weizen:{n:'Weizen',e:'🌾',c:'#f0b93a',q:'FAOSTAT 2022, Mio. t',l:'#g-brot',d:{CHN:137.7,IND:107.7,RUS:104.2,USA:44.9,AUS:36.2,CAN:34.3,FRA:33.6,PAK:26.2,DEU:22.6,UKR:20.2,TUR:19.8,ARG:18,KAZ:16.4,GBR:15.5,POL:13.2,IRN:10,EGY:9.7,ROU:8.7,ESP:7.4,ITA:6.8}},
 mais:{n:'Mais',e:'🌽',c:'#ffd84a',q:'FAOSTAT 2022, Mio. t',l:'#g-mais',d:{USA:348.8,CHN:277.2,BRA:109.4,ARG:59,IND:33.7,UKR:27,MEX:26.6,IDN:20,ZAF:16.1,RUS:15.8,CAN:14.5,NGA:12.7,FRA:10.9,ROU:8.8,EGY:7.4,ETH:10.7,TZA:6.9}},
 reis:{n:'Reis',e:'🍚',c:'#a8dc8a',q:'FAOSTAT 2022, Mio. t Rohreis',l:'#r-reisbrot',d:{CHN:208.5,IND:196.2,BGD:57.2,IDN:54.7,VNM:42.7,THA:34.3,MMR:24.7,PHL:19.8,KHM:11.6,PAK:11,BRA:10.8,JPN:10.4,NGA:8.3,USA:7.3,EGY:5.8,NPL:5.1,LKA:3.4}},
 gerste:{n:'Gerste',e:'🍺',c:'#d8a46a',q:'FAOSTAT 2022, Mio. t',l:'#g-bier',d:{RUS:23.4,AUS:14.4,FRA:11.6,DEU:11.4,CAN:10,TUR:8.5,GBR:7.4,ESP:6,UKR:5.8,ARG:5.3,USA:3.8,DNK:3.8,KAZ:3.5,POL:3.3,IRN:2.5,MAR:1.5}},
 hopfen:{n:'Hopfen',e:'🌿',c:'#7fd1a0',q:'FAOSTAT/IHGC 2022, Tsd. t',l:'#g-bier',d:{USA:47,DEU:34,CHN:6,CZE:5,POL:3.5,SVN:2.5,AUS:1.5,ESP:1,GBR:1,FRA:0.8}}};
const ROH={
 oel:{n:'Erdöl',e:'🛢️',c:'#ff8a3d',q:'Reserven: Energy Institute 2020, Mrd. Barrel · Förderung: OWID/EI, TWh',k:'oil',l:'#s-heizen',d:{VEN:304,SAU:297,CAN:168,IRN:158,IRQ:145,RUS:108,KWT:102,ARE:98,USA:69,LBY:48,NGA:37,KAZ:30,CHN:26,QAT:25,BRA:12,DZA:12,ECU:8,NOR:8,AGO:8,AZE:7,MEX:6,OMN:5,IND:4.5,EGY:3.1,GBR:2.5}},
 gas:{n:'Erdgas',e:'🔥',c:'#5fb8ff',q:'Reserven: Energy Institute 2020, Bio. m³ · Förderung: OWID/EI, TWh',k:'gas',l:'#s-heizen',d:{RUS:37.4,IRN:32.1,QAT:24.7,TKM:13.6,USA:12.6,CHN:8.4,VEN:6.3,SAU:6,ARE:5.9,NGA:5.5,IRQ:3.5,AZE:2.5,AUS:2.4,CAN:2.4,DZA:2.3,KAZ:2.3,EGY:2.1,KWT:1.7,NOR:1.4,LBY:1.4}},
 kohle:{n:'Kohle',e:'⛏️',c:'#b0a8a0',q:'Reserven: Energy Institute 2020, Mrd. t · Förderung: OWID/EI, TWh',k:'coal',l:'#s-heizen',d:{USA:249,RUS:162,AUS:150,CHN:143,IND:111,DEU:36,IDN:35,UKR:34,POL:28,KAZ:26,TUR:11.5,ZAF:9.9,NZL:7.6,SRB:7.5,BRA:6.6,CAN:6.6,COL:4.6}},
 uran:{n:'Uran',e:'☢️',c:'#d6ff5a',q:'IAEA/NEA Red Book 2022, Ressourcen < 130 $/kg, Tsd. t',d:{AUS:1684,KAZ:815,CAN:588,RUS:480,NAM:470,ZAF:320,NER:311,BRA:277,CHN:224,MNG:144,UZB:132,UKR:108,BWA:87,USA:59,TZA:58,JOR:52}},
 lithium:{n:'Lithium',e:'🔋',c:'#e07aff',q:'USGS 2024, Reserven, Tsd. t (Bolivien: Ressourcen ~23.000)',l:'#b-lithium',d:{CHL:9300,AUS:6200,ARG:3600,CHN:3000,USA:1100,CAN:930,ZWE:480,BRA:390,PRT:60,BOL:23000}}};
const STAEDTE=[['Tokio',139.7,35.7,37],['Delhi',77.2,28.6,34],['Shanghai',121.5,31.2,29],['Dhaka',90.4,23.8,23],['São Paulo',-46.6,-23.5,22.6],['Kairo',31.2,30,22],['Mexiko-Stadt',-99.1,19.4,22],['Peking',116.4,39.9,21.7],['Mumbai',72.9,19.1,21.3],['Osaka',135.5,34.7,19],['New York',-74,40.7,18.9],['Chongqing',106.5,29.6,17],['Karatschi',67,24.9,17],['Kinshasa',15.3,-4.3,17],['Lagos',3.4,6.5,16],['Istanbul',29,41,16],['Buenos Aires',-58.4,-34.6,15.5],['Kolkata',88.4,22.6,15.5],['Manila',121,14.6,14.7],['Guangzhou',113.3,23.1,14],['Tianjin',117.2,39.1,14],['Rio de Janeiro',-43.2,-22.9,13.7],['Bangalore',77.6,13,13.6],['Lahore',74.3,31.5,13.5],['Shenzhen',114.1,22.5,13],['Moskau',37.6,55.8,12.7],['Los Angeles',-118.2,34.1,12.5],['Chennai',80.3,13.1,12],['Bogotá',-74.1,4.7,11.5],['Jakarta',106.8,-6.2,11.4],['Lima',-77,-12,11.2],['Paris',2.35,48.86,11.2],['Bangkok',100.5,13.75,11],['Hyderabad',78.5,17.4,10.8],['Seoul',127,37.6,10],['London',-0.13,51.5,9.6],['Teheran',51.4,35.7,9.5],['Luanda',13.2,-8.8,9.3],['Ho-Chi-Minh-Stadt',106.7,10.8,9.3],['Chicago',-87.6,41.9,9],['Kuala Lumpur',101.7,3.1,8.6],['Berlin',13.4,52.5,3.6]];
// Pflanzen: Herkunft [lon,lat], Text, Bereiche [lat0,lat1,lon0,lon1], erlaubte Klimazonen (Präfix)
const T='C D'.split(' '), TE=['C','D','ET'];
const PFL={p01:[[20,50],'Eurasien (heute weltweit gemäßigt)',[[35,68,-10,140],[30,60,-130,-60]],T],p02:[[15,50],'Europa, Westasien',[[40,65,-10,90]],T],p03:[[30,48],'Eurasien (heute weltweit)',[[30,70,-180,180],[-55,-30,-75,175]],TE],p04:[[10,48],'Europa, Westasien, Nordafrika',[[34,62,-10,60]],T],p05:[[14,40],'Mittelmeerraum',[[30,46,-10,45]],['Cs','BS','Cf']],p06:[[10,50],'Europa (weltweit eingeschleppt)',[[30,65,-10,90],[30,55,-125,-65],[-45,-25,-75,175]],T],p07:[[20,52],'gesamte Nordhalbkugel',[[30,70,-180,180]],TE],p08:[[20,47],'Europa, Westasien',[[30,62,-10,100]],['C','D']],p09:[[60,48],'Eurasien',[[30,68,-10,150],[35,60,-100,-60]],T],p10:[[30,50],'Eurasien (weltweit eingeschleppt)',[[20,68,-180,180],[-50,-20,-75,175]],TE],p11:[[55,30],'vermutlich Persien bis Indien (heute weltweit)',[[15,45,-125,140],[-40,-15,-70,155]],['Cs','Cf','Cw','BS','Aw']],p12:[[20,46],'Europa, Westasien',[[35,60,-10,90]],T],p13:[[30,58],'boreale und gemäßigte Wälder der Nordhalbkugel',[[40,70,-180,180]],['Dfb','Dfc','Cfb']],p14:[[60,58],'Eurasien',[[40,70,-8,140]],['Dfb','Dfc','Cfb']],p15:[[127.4,0.8],'Molukken (Indonesien)',[[-8,3,95,135],[-25,-12,43,51],[-7,-4,38,40.5]],['Af','Aw']],p16:[[40,42],'Eurasien, Nordafrika',[[30,58,-10,100]],['BS','Cs','Dfb','Cf']],p17:[[-87,39],'östliches Nordamerika',[[30,46,-100,-75]],['Cfa','Dfa','Dfb']],p18:[[105,22],'Süd-/Südostasien',[[-10,28,70,125]],['Af','Aw','Cw']],p19:[[78,15],'Indien, Südostasien',[[5,30,68,110]],['Aw','Af','Cw']],p20:[[20,50],'Europa, Westasien',[[40,62,-10,60]],T],p21:[[-65,-20],'Anden (Bolivien, Nordargentinien)',[[-30,-10,-70,-55]],['H','Aw','Cf','BS']],p22:[[95,40],'Zentral- und Ostasien',[[25,55,-10,130]],['C','D','BS']],p23:[[46,16],'Arabische Halbinsel',[[12,30,35,60]],['BW','BS']],p24:[[40,52],'Eurasien',[[40,65,-10,130],[40,55,-100,-60]],T]};
const REZ=[['broetchen','Ostdeutsche Brötchen',12.4,51.3,'DEU'],['dinkelvollkorn','Dinkel-Vollkornbrot',9.2,48.6,'DEU'],['kartoffelbrot','Kartoffelbrot',10,51,'DEU'],['bierbrot','Bierbrot',11.5,49.5,'DEU'],['sauerkraut','Sauerkraut',7.8,48.4,'DEU'],['brioche','Brioche',-0.4,49.2,'FRA'],['grundteige','Focaccia & Pizza',14.25,40.85,'ITA'],['mohnkuchen','Mohnkuchen',15,50,'CZE'],['soljanka','Soljanka',37.6,55.8,'RUS'],['jagdwurstnudeln','Nudeln mit Jagdwurst',12,52,'DEU'],['baumstriezel','Baumstriezel',25,46.5,'ROU'],['reisbrot','Reisbrot',100,15,'THA']];
const AUT=[['storl','Wolf-Dieter Storl · Allgäu',10.2,47.7],['ganser','Daniele Ganser · Basel',7.6,47.56],['krall','Markus Krall · Schweiz',8.5,47.2],['nehls','Michael Nehls · Deutschland',9,49.2]];
const KLIMA={Af:['Tropischer Regenwald','#2f6bff'],Aw:['Tropische Savanne','#46aafa'],BW:['Wüste','#ff4a3a'],BS:['Steppe','#f5a500'],Cs:['Mittelmeerklima','#f2e33a'],Cfa:['Feucht-subtropisch','#a8e05a'],Cwa:['Subtropisch, Wintertrocken','#5ac878'],Cfb:['Gemäßigt ozeanisch','#3fa848'],Dfb:['Kontinental','#30b6ff'],Dfc:['Subarktisch (Taiga-Klima)','#3a8a96'],ET:['Tundra','#b0b8c0'],EF:['Ewiges Eis','#e6eef6'],H:['Hochgebirge','#a08068']};
const BODEN={tscher:['Schwarzerde (Tschernosem)','#2b241e'],braun:['Braunerde, Parabraunerde','#9a7a4a'],podsol:['Podsol (Bleicherde)','#b8b0a0'],perma:['Permafrost (Kryosol)','#8fa3b8'],eis:['Eis','#e6eef6'],ferral:['Laterit (Ferralsol)','#c4522a'],rot:['Rotlehm, Acrisol','#b8703a'],wueste:['Wüstenboden, Sand','#e8c98a'],kastan:['Kastanozem (Steppenboden)','#8a6a3a'],vert:['Vertisol (Quelltonboden)','#6a5a7a'],loess:['Löss','#e0c070'],gebirge:['Gebirgsböden','#7a7a70']};
const VEGN={regen:['Tropischer Regenwald','#1f8a3a'],savanne:['Savanne','#c8b840'],wueste:['Wüste','#e8c88a'],steppe:['Steppe, Grasland','#b8c86a'],hartlaub:['Hartlaubwald (Macchie)','#8aa850'],subtrop:['Subtropischer Wald','#5ab060'],laub:['Laubwald','#3aa050'],misch:['Mischwald','#2f8a5a'],taiga:['Taiga (Nadelwald)','#1f6a5a'],tundra:['Tundra','#9aa890'],eis:['Eis','#e6eef6'],gebirge:['Gebirge','#9a8a78']};
const GRUND={dichte:{n:'Bevölkerungsdichte',u:'Ew./km²',z:1},wachstum:{n:'Wachstum pro Jahr',u:'%',z:1},energie:{n:'Energie pro Kopf',u:'kWh',z:1},erneuerbar:{n:'Erneuerbarer Strom',u:'%',z:1},klima:{n:'Klimazonen',r:2},boden:{n:'Böden',r:3},veg:{n:'Vegetation',r:4},keine:{n:'Nur Länder'}};

/* ---------- Farbskalen ---------- */
function lerp(a,b,t){return a+(b-a)*t;}
function hx(h){return [1,3,5].map(i=>parseInt(h.slice(i,i+2),16));}
function ramp(stops,t){ t=Math.max(0,Math.min(1,t)); const n=stops.length-1, k=Math.min(n-1,Math.floor(t*n)), f=t*n-k; const a=hx(stops[k]),b=hx(stops[k+1]); return `rgb(${a.map((v,i)=>Math.round(lerp(v,b[i],f))).join(',')})`; }
const MAGMA=['#1b1035','#4a1a6e','#8a2a7a','#cf4a5a','#f78a3a','#fde27a'];
const DIV=['#2a6ab8','#7fb4e0','#e8e2d0','#f5a55a','#d2462a'];
const TEAL=['#0e2a3a','#145a6a','#1a8a8a','#4ac0a0','#b8f0b0'];
const GRN=['#2a2420','#3a4a2a','#4a7a3a','#6ab04a','#c8f07a'];

/* ---------- Zustand ---------- */
const S={modus:'globus',lam:-15,phi:25,zoom:1,px:0,py:0,grund:'dichte',jahr:2023,ov:{staedte:false,weizen:true,mais:false,reis:true,gerste:false,hopfen:false,oel:false,gas:false,kohle:false,uran:false,lithium:false,pfl:true,rez:false,aut:false,nacht:false},pflanze:'',sel:null,klick:null,spin:true};
let cv,ctx,W=0,H=0,DPR=1,wrap;

/* ---------- Projektion ---------- */
function radius(){ return Math.min(W,H)*0.42*S.zoom; }
function proj(lon,lat){
  if(S.modus==='globus'){ const l=(lon-S.lam)*R2,p=lat*R2,p0=S.phi*R2, r=radius();
    const cosc=Math.sin(p0)*Math.sin(p)+Math.cos(p0)*Math.cos(p)*Math.cos(l);
    return [W/2+r*Math.cos(p)*Math.sin(l), H/2-r*(Math.cos(p0)*Math.sin(p)-Math.sin(p0)*Math.cos(p)*Math.cos(l)), cosc]; }
  const k=Math.min(W/360,H/180)*S.zoom; let x=lon-S.lam; x=((x+540)%360)-180; return [W/2+x*k+S.px, H/2-(lat-0)*k+S.py, 1];
}
function inv(x,y){
  if(S.modus==='globus'){ const r=radius(), X=(x-W/2)/r, Y=-(y-H/2)/r, rho=Math.hypot(X,Y); if(rho>1) return null; const c=Math.asin(rho), p0=S.phi*R2;
    const lat=Math.asin(Math.cos(c)*Math.sin(p0)+(rho?Y*Math.sin(c)*Math.cos(p0)/rho:0));
    const lon=S.lam*R2+Math.atan2(X*Math.sin(c), rho*Math.cos(p0)*Math.cos(c)-Y*Math.sin(p0)*Math.sin(c));
    return [((lon/R2+540)%360)-180, lat/R2]; }
  const k=Math.min(W/360,H/180)*S.zoom; const lon=(x-W/2-S.px)/k+S.lam, lat=-(y-H/2-S.py)/k; if(Math.abs(lat)>90) return null; return [((lon+540)%360)-180,lat];
}
function pfad(ring){ // gibt Pfad auf ctx
  if(S.modus==='globus'){ const r=radius(); let start=true, sichtbar=false; const pts=ring.map(([a,b])=>proj(a,b));
    for(const q of pts) if(q[2]>0){sichtbar=true;break;} if(!sichtbar) return false;
    for(const q of pts){ let x=q[0],y=q[1]; if(q[2]<0){ const dx=x-W/2,dy=y-H/2,d=Math.hypot(dx,dy)||1; x=W/2+dx/d*r; y=H/2+dy/d*r; }
      if(start){ctx.moveTo(x,y);start=false;} else ctx.lineTo(x,y); } ctx.closePath(); return true; }
  let lx=null; ring.forEach(([a,b],k)=>{ const q=proj(a,b); if(k===0||Math.abs(q[0]-lx)>W*0.5) ctx.moveTo(q[0],q[1]); else ctx.lineTo(q[0],q[1]); lx=q[0]; }); ctx.closePath(); return true;
}

/* ---------- Werte ---------- */
function ow(i){ return DAT.owid[i]||{}; }
function wert(i,art,jahr){ const o=ow(i), k=jahr-1960, c=DAT.idx[i];
  if(art==='dichte'){ const p=o.pop&&o.pop[k]; return p&&c.a>500?p*1000/c.a:null; }
  if(art==='wachstum'){ const a=o.pop&&o.pop[k], b=o.pop&&o.pop[k-1]; return a&&b?(a/b-1)*100:null; }
  if(art==='energie'){ return o.epc?o.epc[k]:null; }
  if(art==='erneuerbar'){ return o.ren?o.ren[k]:null; }
  if(art==='pop'){ return o.pop?o.pop[k]:null; }
  return null; }
function farbe(i){ const g=S.grund, v=wert(i,g,S.jahr); if(v==null) return null;
  if(g==='dichte') return ramp(MAGMA,Math.log10(Math.max(v,1))/3);
  if(g==='wachstum') return ramp(DIV,(v+1)/5);
  if(g==='energie') return ramp(TEAL,Math.log10(Math.max(v,300))/5.2-0.45);
  if(g==='erneuerbar') return ramp(GRN,v/100);
  return null; }
function fmt(v,d=0){ return v==null?'–':v.toLocaleString('de-DE',{maximumFractionDigits:d,minimumFractionDigits:d}); }

/* ---------- Zeichnen ---------- */
let sterne=null;
function zeichne(){
  if(!ctx) return; BOX=[]; ctx.setTransform(DPR,0,0,DPR,0,0); ctx.clearRect(0,0,W,H);
  const g0=ctx.createRadialGradient(W/2,H/2,0,W/2,H/2,Math.max(W,H)*0.8); g0.addColorStop(0,'#0e1a30'); g0.addColorStop(1,'#04070e'); ctx.fillStyle=g0; ctx.fillRect(0,0,W,H);
  if(!sterne){ sterne=[]; let s=7; const r=()=>(s=(s*16807)%2147483647)/2147483647; for(let i=0;i<260;i++) sterne.push([r(),r(),r()*1.2+.2,r()]); }
  sterne.forEach(([x,y,z,a])=>{ ctx.fillStyle=`rgba(200,220,255,${a*.6})`; ctx.fillRect(x*W,y*H,z,z); });
  const r=radius(), glob=S.modus==='globus';
  if(glob){ const at=ctx.createRadialGradient(W/2,H/2,r*0.92,W/2,H/2,r*1.18); at.addColorStop(0,'rgba(80,170,255,.55)'); at.addColorStop(.35,'rgba(60,140,255,.18)'); at.addColorStop(1,'rgba(40,100,255,0)'); ctx.fillStyle=at; ctx.beginPath(); ctx.arc(W/2,H/2,r*1.18,0,7); ctx.fill();
    const oz=ctx.createRadialGradient(W/2-r*.35,H/2-r*.4,r*.1,W/2,H/2,r); oz.addColorStop(0,'#1d4f86'); oz.addColorStop(.6,'#0c2c52'); oz.addColorStop(1,'#071a33'); ctx.fillStyle=oz; ctx.beginPath(); ctx.arc(W/2,H/2,r,0,7); ctx.fill();
    ctx.save(); ctx.beginPath(); ctx.arc(W/2,H/2,r,0,7); ctx.clip(); }
  else { ctx.fillStyle='#0a2240'; const a=proj(-180,90),b=proj(180,-90); ctx.fillRect(Math.min(a[0],b[0])-W,a[1],W*3,b[1]-a[1]); }
  // Gradnetz
  ctx.strokeStyle='rgba(140,190,255,.10)'; ctx.lineWidth=.7;
  for(let la=-60;la<=60;la+=30){ ctx.beginPath(); let st=true; for(let lo=-180;lo<=180;lo+=4){ const q=proj(lo,la); if(q[2]<0){st=true;continue;} st?ctx.moveTo(q[0],q[1]):ctx.lineTo(q[0],q[1]); st=false; } ctx.stroke(); }
  for(let lo=-180;lo<180;lo+=30){ ctx.beginPath(); let st=true; for(let la=-88;la<=88;la+=4){ const q=proj(lo,la); if(q[2]<0){st=true;continue;} st?ctx.moveTo(q[0],q[1]):ctx.lineTo(q[0],q[1]); st=false; } ctx.stroke(); }
  // Länder
  const rast=GRUND[S.grund].r;
  DAT.laender.forEach(c=>{ const f=rast?null:farbe(c.i); ctx.beginPath(); let ok=false; c.p.forEach(rg=>{ if(pfad(rg)) ok=true; }); if(!ok) return;
    ctx.fillStyle=f||(rast?'#22303a':'#1e2c3a'); ctx.fill(); });
  // Raster
  if(rast){ const half=1.02; ctx.save(); ctx.beginPath(); DAT.laender.forEach(c=>c.p.forEach(rg=>pfad(rg))); ctx.clip(); DAT.raster.forEach(g=>{ const tab=rast===2?KLIMA:rast===3?BODEN:VEGN, k=g[rast]; const q=proj(g[0],g[1]); if(q[2]<0.05) return;
      const a=proj(g[0]-half,g[1]+half),b=proj(g[0]+half,g[1]+half),c2=proj(g[0]+half,g[1]-half),d=proj(g[0]-half,g[1]-half);
      if(!glob && Math.abs(a[0]-b[0])>W/2) return;
      ctx.fillStyle=tab[k][1]; ctx.globalAlpha=.86; ctx.beginPath(); ctx.moveTo(a[0],a[1]); ctx.lineTo(b[0],b[1]); ctx.lineTo(c2[0],c2[1]); ctx.lineTo(d[0],d[1]); ctx.closePath(); ctx.fill(); ctx.globalAlpha=1; }); ctx.restore(); }
  // Wildvorkommen gewählter Pflanze
  if(S.pflanze){ const P=PFL[S.pflanze]; ctx.fillStyle='rgba(120,255,170,.55)'; DAT.raster.forEach(g=>{ if(g[5]||!inBereich(P,g)) return; const q=proj(g[0],g[1]); if(q[2]<0.05) return; ctx.beginPath(); ctx.arc(q[0],q[1],Math.max(1.4,radius()/260*S.zoom),0,7); ctx.fill(); }); }
  // Grenzen
  ctx.strokeStyle='rgba(220,235,255,.22)'; ctx.lineWidth=.6;
  DAT.laender.forEach(c=>{ ctx.beginPath(); let ok=false; c.p.forEach(rg=>{ if(pfad(rg)) ok=true; }); if(ok) ctx.stroke(); });
  if(S.sel){ const c=DAT.idx[S.sel]; ctx.beginPath(); c.p.forEach(rg=>pfad(rg)); ctx.strokeStyle='#fff'; ctx.lineWidth=2.2; ctx.shadowColor='rgba(120,200,255,.9)'; ctx.shadowBlur=12; ctx.stroke(); ctx.shadowBlur=0; }
  // Tag/Nacht
  if(S.ov.nacht) nacht();
  // Overlays
  const blase=(lon,lat,rad,col,lbl)=>{ const q=proj(lon,lat); if(q[2]<0.12) return; const R=rad*Math.sqrt(S.zoom); const gg=ctx.createRadialGradient(q[0]-R*.3,q[1]-R*.3,R*.1,q[0],q[1],R); gg.addColorStop(0,col); gg.addColorStop(1,col+'99'); ctx.fillStyle=gg; ctx.beginPath(); ctx.arc(q[0],q[1],R,0,7); ctx.fill(); ctx.strokeStyle='rgba(0,0,0,.45)'; ctx.lineWidth=1; ctx.stroke(); if(lbl&&S.zoom>1.4) text(lbl,q[0]+R+3,q[1]+4); };
  Object.entries(GETREIDE).forEach(([k,G])=>{ if(!S.ov[k]) return; const mx=Math.max(...Object.values(G.d)); Object.entries(G.d).forEach(([i,v],n)=>{ const c=DAT.idx[i]; if(!c) return; const off=(Object.keys(GETREIDE).indexOf(k)-2)*1.6; blase(c.mitte[0]+off,c.mitte[1]+off*.4,4+16*Math.sqrt(v/mx),G.c,null); }); });
  Object.entries(ROH).forEach(([k,G])=>{ if(!S.ov[k]) return; const mx=Math.max(...Object.values(G.d).filter(v=>v<20000)); Object.entries(G.d).forEach(([i,v])=>{ const c=DAT.idx[i]; if(!c) return; const R=4+18*Math.sqrt(Math.min(v,mx)/mx); raute(c.mitte[0]-1.5,c.mitte[1]-1.2,R,G.c); }); });
  if(S.ov.staedte) STAEDTE.forEach(([n,lo,la,p])=>{ const q=proj(lo,la); if(q[2]<0.1) return; const R=2+Math.sqrt(p)*1.1*Math.sqrt(S.zoom); const gg=ctx.createRadialGradient(q[0],q[1],0,q[0],q[1],R*2.4); gg.addColorStop(0,'rgba(255,230,150,.95)'); gg.addColorStop(.35,'rgba(255,190,90,.5)'); gg.addColorStop(1,'rgba(255,160,60,0)'); ctx.fillStyle=gg; ctx.beginPath(); ctx.arc(q[0],q[1],R*2.4,0,7); ctx.fill(); if(S.zoom>1.6||p>20) text(n,q[0]+R+2,q[1]-R); });
  if(S.ov.pfl) Object.entries(PFL).forEach(([id,P])=>{ const q=proj(P[0][0],P[0][1]); if(q[2]<0.1) return; pin(q[0],q[1],'#ff6a8a'); if(S.zoom>1.3||S.pflanze===id) text(pname(id),q[0]+7,q[1]-6); });
  if(S.ov.rez) REZ.forEach(([id,n,lo,la])=>{ const q=proj(lo,la); if(q[2]<0.1) return; pin(q[0],q[1],'#c79aff'); if(S.zoom>1.8) text(n,q[0]+7,q[1]-6); });
  if(S.ov.aut) AUT.forEach(([id,n,lo,la])=>{ const q=proj(lo,la); if(q[2]<0.1) return; pin(q[0],q[1],'#6ac8ff'); if(S.zoom>1.8) text(n,q[0]+7,q[1]-6); });
  if(S.klick){ const q=proj(S.klick[0],S.klick[1]); if(q[2]>0){ ctx.strokeStyle='#fff'; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(q[0],q[1],6,0,7); ctx.stroke(); } }
  if(glob){ ctx.restore(); const sh=ctx.createRadialGradient(W/2-r*.35,H/2-r*.4,r*.2,W/2,H/2,r*1.02); sh.addColorStop(0,'rgba(255,255,255,.07)'); sh.addColorStop(.7,'rgba(0,0,0,0)'); sh.addColorStop(1,'rgba(0,5,20,.55)'); ctx.fillStyle=sh; ctx.beginPath(); ctx.arc(W/2,H/2,r,0,7); ctx.fill();
    ctx.strokeStyle='rgba(140,200,255,.35)'; ctx.lineWidth=1.2; ctx.beginPath(); ctx.arc(W/2,H/2,r,0,7); ctx.stroke(); }
}
let BOX=[];
function text(t,x,y){ ctx.font='600 11.5px system-ui,-apple-system,Segoe UI,Roboto,sans-serif'; const w=ctx.measureText(t).width; if(BOX.some(b=>x<b[0]+b[2]+4&&x+w+4>b[0]&&y-11<b[1]+2&&y+2>b[1]-11)) return; BOX.push([x,y,w]); ctx.lineWidth=3.2; ctx.strokeStyle='rgba(4,8,16,.85)'; ctx.strokeText(t,x,y); ctx.fillStyle='#eaf2ff'; ctx.fillText(t,x,y); }
function pin(x,y,c){ ctx.fillStyle=c; ctx.strokeStyle='#0a0f1a'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.arc(x,y,4.6,0,7); ctx.fill(); ctx.stroke(); ctx.fillStyle='rgba(255,255,255,.8)'; ctx.beginPath(); ctx.arc(x-1.2,y-1.2,1.4,0,7); ctx.fill(); }
function raute(lon,lat,R,c){ const q=proj(lon,lat); if(q[2]<0.12) return; R*=Math.sqrt(S.zoom)*.9; ctx.fillStyle=c+'cc'; ctx.strokeStyle='rgba(0,0,0,.55)'; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(q[0],q[1]-R); ctx.lineTo(q[0]+R,q[1]); ctx.lineTo(q[0],q[1]+R); ctx.lineTo(q[0]-R,q[1]); ctx.closePath(); ctx.fill(); ctx.stroke(); }
function pname(id){ const p=(window.QW_DATEN&&window.QW_DATEN.pflanzen||[]).find(x=>x.id===id); return p?p.name.replace(' & Kiefernknospen',''):id; }
function inBereich(P,g){ return P[2].some(b=>g[1]>=b[0]&&g[1]<=b[1]&&g[0]>=b[2]&&g[0]<=b[3]) && P[3].some(z=>g[2].startsWith(z)); }
function sonne(){ const d=new Date(), t=(Date.UTC(d.getUTCFullYear(),d.getUTCMonth(),d.getUTCDate())-Date.UTC(d.getUTCFullYear(),0,0))/864e5; const dekl=-23.44*Math.cos(2*Math.PI/365*(t+10)); const h=d.getUTCHours()+d.getUTCMinutes()/60; return [(12-h)*15,dekl]; }
function nacht(){ const [sl,sp]=sonne(); const al=sl+180, ap=-sp; const pts=[]; for(let i=0;i<=180;i++){ const b=i*2*R2, d=90*R2, p1=ap*R2, l1=al*R2; const la=Math.asin(Math.sin(p1)*Math.cos(d)+Math.cos(p1)*Math.sin(d)*Math.cos(b)); const lo=l1+Math.atan2(Math.sin(b)*Math.sin(d)*Math.cos(p1),Math.cos(d)-Math.sin(p1)*Math.sin(la)); pts.push([((lo/R2+540)%360)-180,la/R2]); }
  if(S.modus==='globus'){ ctx.beginPath(); pfad(pts); ctx.fillStyle='rgba(2,6,20,.55)'; ctx.fill(); }
  else { ctx.fillStyle='rgba(2,6,20,.5)'; for(let lo=-180;lo<180;lo+=2) for(let la=-89;la<90;la+=2){ const x=Math.cos(la*R2)*Math.cos((lo-sl)*R2)*Math.cos(sp*R2)+Math.sin(la*R2)*Math.sin(sp*R2); if(x<0){ const a=proj(lo,la+1),b=proj(lo+2,la-1); if(Math.abs(a[0]-b[0])<W/4) ctx.fillRect(a[0],a[1],b[0]-a[0]+.6,b[1]-a[1]+.6); } } }
  const q=proj(sl,sp); if(q[2]>0){ ctx.fillStyle='#ffd860'; ctx.shadowColor='#ffd860'; ctx.shadowBlur=14; ctx.beginPath(); ctx.arc(q[0],q[1],5,0,7); ctx.fill(); ctx.shadowBlur=0; } }

/* ---------- Treffer ---------- */
function inring(x,y,r){ let c=false; for(let i=0,j=r.length-1;i<r.length;j=i++){ const [xi,yi]=r[i],[xj,yj]=r[j]; if((yi>y)!==(yj>y)&&x<(xj-xi)*(y-yi)/((yj-yi)||1e-9)+xi) c=!c; } return c; }
function landAn(lon,lat){ for(const c of DAT.laender){ const b=c.bb; if(lon<b[0]||lon>b[1]||lat<b[2]||lat>b[3]) continue; if(c.p.some(r=>inring(lon,lat,r))) return c; } return null; }
function rasterAn(lon,lat){ const x=Math.round((lon+179)/2)*2-179, y=Math.round((lat+89)/2)*2-89; return DAT.rmap[x+','+y]; }

/* ---------- Info-Karte ---------- */
function spark(i){ const p=ow(i).pop; if(!p) return ''; const v=p.filter(x=>x!=null), mx=Math.max(...v), mn=Math.min(...v); const w=260,h=56; let d=''; p.forEach((x,k)=>{ if(x==null) return; const X=k/63*w, Y=h-4-(x-mn)/((mx-mn)||1)*(h-10); d+=(d?'L':'M')+X.toFixed(1)+','+Y.toFixed(1); }); const k=S.jahr-1960, cx=k/63*w, cy=p[k]!=null?h-4-(p[k]-mn)/((mx-mn)||1)*(h-10):h;
  return `<svg viewBox="0 0 ${w} ${h}" class="qwk-spark"><defs><linearGradient id="qwsg" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#4ad0a0" stop-opacity=".45"/><stop offset="1" stop-color="#4ad0a0" stop-opacity="0"/></linearGradient></defs><path d="${d}L${w},${h}L0,${h}Z" fill="url(#qwsg)"/><path d="${d}" fill="none" stroke="#4ad0a0" stroke-width="2"/><circle cx="${cx}" cy="${cy}" r="3.5" fill="#fff"/></svg>`; }
function chip(t,href,kl=''){ return href?`<a class="qwk-chip ${kl}" href="${href}">${t}</a>`:`<span class="qwk-chip ${kl}">${t}</span>`; }
function info(){
  const box=$('.qwk-info',wrap); if(!S.sel){ box.innerHTML=`<div class="qwk-leer"><div class="qwk-gl">🌍</div><b>Land antippen</b><p>Tippe auf ein Land, um Einwohner, Dichte, Wachstum, Ernten, Rohstoffe und passende Kapitel aus dem Kompendium zu sehen.</p><p class="qwk-mini">Ziehen = drehen · Zwei Finger oder Mausrad = zoomen</p></div>`; return; }
  const c=DAT.idx[S.sel], i=c.i, j=S.jahr, o=ow(i);
  const pop=wert(i,'pop',j), di=wert(i,'dichte',j), wa=wert(i,'wachstum',j), en=wert(i,'energie',j), re=wert(i,'erneuerbar',j);
  let h=`<div class="qwk-kopf"><span class="qwk-flag">${c.f||'🏳️'}</span><div><h2>${c.n}</h2><small>Stand ${j}${S.klick?` · ${fmt(Math.abs(S.klick[1]),1)}° ${S.klick[1]>=0?'N':'S'}, ${fmt(Math.abs(S.klick[0]),1)}° ${S.klick[0]>=0?'O':'W'}`:''}</small></div><button class="qwk-x" aria-label="Schließen">✕</button></div>
  <div class="qwk-kpi"><div><small>Einwohner</small><b>${pop?pop>=1e6?fmt(pop/1e6,2)+' Mrd.':pop>=1000?fmt(pop/1000,1)+' Mio.':fmt(pop)+' Tsd.':'–'}</b></div><div><small>Dichte</small><b>${fmt(di)} <i>/km²</i></b></div><div><small>Wachstum</small><b class="${wa>0?'plus':'minus'}">${wa==null?'–':(wa>0?'+':'')+fmt(wa,1)+' %'}</b></div><div><small>Fläche (ca.)</small><b>${fmt(c.a/1000)} <i>Tsd. km²</i></b></div></div>
  <div class="qwk-box"><small>Bevölkerung 1960–2023</small>${spark(i)}</div>`;
  const gt=Object.entries(GETREIDE).filter(([k,G])=>G.d[i]).map(([k,G])=>chip(`${G.e} ${G.n} ${fmt(G.d[i],1)} ${k==='hopfen'?'Tsd. t':'Mio. t'}`,G.l));
  if(gt.length) h+=`<h4>Getreide (2022)</h4><div>${gt.join('')}</div>`;
  const rh=Object.entries(ROH).filter(([k,G])=>G.d[i]||(G.k&&o[G.k]&&o[G.k][j-1960])).map(([k,G])=>{ const pv=G.k&&o[G.k]?o[G.k][j-1960]:null; const ein={oel:'Mrd. Barrel',gas:'Bio. m³',kohle:'Mrd. t',uran:'Tsd. t',lithium:'Tsd. t'}[k]; return chip(`${G.e} ${G.n}${G.d[i]?' · Reserven '+fmt(G.d[i],G.d[i]<10?1:0)+' '+ein:''}${pv?' · Förderung '+fmt(pv)+' TWh':''}`,G.l); });
  if(rh.length) h+=`<h4>Rohstoffe & Energie</h4><div>${rh.join('')}</div>`;
  h+=`<h4>Energie</h4><div>${chip('⚡ '+(en?fmt(en)+' kWh pro Kopf':'keine Angabe'))}${re!=null?chip('🌱 '+fmt(re,0)+' % erneuerbarer Strom'):''}</div>`;
  if(S.klick){ const g=rasterAn(S.klick[0],S.klick[1]); if(g) h+=`<h4>An dieser Stelle (Schema)</h4><div>${chip('🌡️ '+KLIMA[g[2]][0],'#s-boden')}${chip('🟫 '+BODEN[g[3]][0],'#s-boden')}${chip('🌳 '+VEGN[g[4]][0])}</div>`; }
  const pf=Object.entries(PFL).filter(([id,P])=>{ const oc=landAn(P[0][0],P[0][1]); if(oc&&oc.i===i) return true; if(S.klick){ const g=rasterAn(S.klick[0],S.klick[1]); return g&&inBereich(P,g); } return false; }).map(([id,P])=>chip('🌿 '+pname(id),'#'+id,'k'));
  const rz=REZ.filter(r=>r[4]===i).map(r=>chip('🍽️ '+r[1],'#r-'+r[0],'k'));
  const au=AUT.filter(a=>{ const oc=landAn(a[2],a[3]); return oc&&oc.i===i; }).map(a=>chip('👤 '+a[1].split(' · ')[0],'#a-'+a[0],'k'));
  const kp=[...pf,...rz,...au]; if(kp.length) h+=`<h4>Im Kompendium</h4><div>${kp.join('')}</div>`;
  box.innerHTML=h; $('.qwk-x',box).onclick=()=>{ S.sel=null; S.klick=null; info(); zeichne(); wrap.classList.remove('qwk-info-auf'); };
}

/* ---------- Legende ---------- */
function legende(){
  const g=S.grund, L=$('.qwk-leg',wrap); let h=`<b>${GRUND[g].n}</b>`;
  const bar=(st,a,b,m)=>`<div class="qwk-ramp" style="background:linear-gradient(90deg,${st.join(',')})"></div><div class="qwk-rl"><span>${a}</span><span>${m||''}</span><span>${b}</span></div>`;
  if(g==='dichte') h+=bar(MAGMA,'1','1000+ Ew./km²','30');
  else if(g==='wachstum') h+=bar(DIV,'−1 %','+4 % / Jahr','±0');
  else if(g==='energie') h+=bar(TEAL,'wenig','viel (kWh/Kopf)');
  else if(g==='erneuerbar') h+=bar(GRN,'0 %','100 % des Stroms');
  else if(GRUND[g].r){ const t=GRUND[g].r===2?KLIMA:GRUND[g].r===3?BODEN:VEGN; h+=`<div class="qwk-kl">${Object.values(t).map(([n,c])=>`<span><i style="background:${c}"></i>${n}</span>`).join('')}</div><div class="qwk-hin">Vereinfachtes Schema (2°-Raster), keine Messkarte</div>`; }
  const ov=[]; Object.entries(GETREIDE).forEach(([k,G])=>S.ov[k]&&ov.push(`<span><i class="r" style="background:${G.c}"></i>${G.n}</span>`)); Object.entries(ROH).forEach(([k,G])=>S.ov[k]&&ov.push(`<span><i class="d" style="background:${G.c}"></i>${G.n}</span>`));
  if(S.ov.staedte) ov.push('<span><i class="r" style="background:#ffc860"></i>Großstädte</span>'); if(S.ov.pfl) ov.push('<span><i class="r" style="background:#ff6a8a"></i>Pflanzen-Herkunft</span>'); if(S.ov.rez) ov.push('<span><i class="r" style="background:#c79aff"></i>Rezepte</span>'); if(S.ov.aut) ov.push('<span><i class="r" style="background:#6ac8ff"></i>Autoren</span>');
  if(ov.length) h+=`<div class="qwk-kl qwk-ov">${ov.join('')}</div><div class="qwk-hin">● Ernte 2022 · ◆ Reserven – Größe ~ Menge</div>`;
  L.innerHTML=h; }

/* ---------- Oberfläche ---------- */
const CSS=`
.qwk{--k-bg:#060a13;--k-p:#0c1322;--k-p2:#111a2d;--k-l:#1f2b44;--k-t:#e8eefb;--k-m:#8d9ab8;--k-a:#4ad0a0;--k-a2:#ffb54a;position:relative;display:grid;grid-template-columns:290px 1fr 330px;grid-template-rows:auto 1fr auto;height:calc(100vh - 120px);min-height:560px;background:var(--k-bg);color:var(--k-t);border-radius:18px;overflow:hidden;font:14px system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;box-shadow:0 20px 60px rgba(0,0,0,.35);width:calc(100vw - 32px);max-width:1800px;margin-left:calc(50% - min(50vw - 16px, 900px))}
.qwk *{box-sizing:border-box}
.qwk-top{grid-column:1/4;display:flex;align-items:center;gap:12px;padding:12px 16px;background:linear-gradient(180deg,#0c1426,#0a101d);border-bottom:1px solid var(--k-l);flex-wrap:wrap}
.qwk-titel{display:flex;align-items:center;gap:10px;font:700 18px Georgia,serif;letter-spacing:.2px}.qwk-titel .qwk-gl2{width:30px;height:30px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#7ad8ff,#1b4f8a 60%,#08203e);box-shadow:0 0 14px rgba(80,170,255,.6)}
.qwk-titel small{display:block;font:500 11.5px system-ui;color:var(--k-m);letter-spacing:.3px}
.qwk-seg{display:inline-flex;background:#0a1120;border:1px solid var(--k-l);border-radius:12px;padding:3px;gap:2px}
.qwk-seg button{all:unset;cursor:pointer;padding:7px 12px;border-radius:9px;color:var(--k-m);font-weight:600;font-size:13px;transition:.2s}
.qwk-seg button[aria-pressed=true]{background:linear-gradient(180deg,#1d3a5c,#15304e);color:#fff;box-shadow:inset 0 0 0 1px #2e5b8a,0 4px 14px rgba(40,120,220,.25)}
.qwk-such{margin-left:auto;position:relative}.qwk-such input{all:unset;box-sizing:border-box;width:240px;padding:9px 12px 9px 34px;background:#0a1120;border:1px solid var(--k-l);border-radius:12px;color:var(--k-t);font-size:13.5px}.qwk-such:before{content:"⌕";position:absolute;left:12px;top:6px;color:var(--k-m);font-size:18px}
.qwk-side{background:var(--k-p);border-right:1px solid var(--k-l);overflow:auto;padding:12px 14px 20px}
.qwk-side h3{font:700 10.5px system-ui;letter-spacing:.14em;text-transform:uppercase;color:var(--k-m);margin:16px 2px 8px;display:flex;align-items:center;gap:8px}.qwk-side h3:after{content:"";flex:1;height:1px;background:var(--k-l)}
.qwk-grund{display:grid;grid-template-columns:1fr 1fr;gap:6px}
.qwk-grund button{all:unset;cursor:pointer;padding:9px 10px;line-height:1.25;border-radius:11px;background:var(--k-p2);border:1px solid var(--k-l);font-size:12.5px;font-weight:600;color:#cdd6ea;display:flex;gap:7px;align-items:center;transition:.18s}
.qwk-grund button:hover{border-color:#36507a}.qwk-grund button[aria-pressed=true]{background:linear-gradient(180deg,#123a34,#0f2e2a);border-color:var(--k-a);color:#fff;box-shadow:0 0 0 1px rgba(74,208,160,.25),0 6px 18px rgba(74,208,160,.15)}
.qwk-sw{display:flex;align-items:center;gap:10px;padding:7px 4px;border-radius:9px;cursor:pointer;font-size:13.5px;user-select:none}.qwk-sw:hover{background:rgba(255,255,255,.03)}
.qwk-sw input{display:none}.qwk-sw .k{width:36px;height:21px;border-radius:12px;background:#1a2438;border:1px solid #2a3858;position:relative;flex:none;transition:.2s}.qwk-sw .k:after{content:"";position:absolute;top:2px;left:2px;width:15px;height:15px;border-radius:50%;background:#6a7898;transition:.2s}
.qwk-sw input:checked+.k{background:linear-gradient(90deg,#1f8a6a,#4ad0a0);border-color:#4ad0a0;box-shadow:0 0 12px rgba(74,208,160,.35)}.qwk-sw input:checked+.k:after{left:17px;background:#fff}
.qwk-sw .dt{width:10px;height:10px;border-radius:50%;flex:none;box-shadow:0 0 8px currentColor}.qwk-sw .dt.d{border-radius:2px;transform:rotate(45deg)}
.qwk-sel{all:unset;width:100%;padding:9px 10px;background:var(--k-p2);border:1px solid var(--k-l);border-radius:11px;font-size:13px;color:var(--k-t);margin-top:6px}
.qwk-map{position:relative;overflow:hidden;touch-action:none;cursor:grab}.qwk-map:active{cursor:grabbing}.qwk-map canvas{display:block;width:100%;height:100%}
.qwk-zoom{position:absolute;right:14px;top:14px;display:flex;flex-direction:column;gap:6px}.qwk-zoom button{all:unset;cursor:pointer;width:38px;height:38px;border-radius:12px;background:rgba(12,19,34,.85);border:1px solid var(--k-l);display:grid;place-items:center;font-size:17px;color:#dfe8fa;backdrop-filter:blur(6px)}.qwk-zoom button:hover{border-color:var(--k-a)}
.qwk-leg{position:absolute;left:14px;bottom:14px;max-width:330px;background:rgba(10,16,30,.86);backdrop-filter:blur(8px);border:1px solid var(--k-l);border-radius:14px;padding:10px 12px;font-size:12px}
.qwk-ramp{height:9px;border-radius:5px;margin:7px 0 4px;width:240px}.qwk-rl{display:flex;justify-content:space-between;color:var(--k-m);width:240px}
.qwk-kl{display:flex;flex-wrap:wrap;gap:4px 10px;margin-top:7px}.qwk-kl span{display:flex;align-items:center;gap:5px;color:#cdd6ea}.qwk-kl i{width:10px;height:10px;border-radius:3px;display:inline-block}.qwk-kl i.r{border-radius:50%}.qwk-kl i.d{transform:rotate(45deg);border-radius:1px}
.qwk-ov{border-top:1px solid var(--k-l);padding-top:7px}.qwk-hin{color:var(--k-m);font-size:11px;margin-top:5px}
.qwk-info{background:var(--k-p);border-left:1px solid var(--k-l);overflow:auto;padding:16px}
.qwk-kopf{display:flex;align-items:center;gap:12px;margin-bottom:12px}.qwk-flag{font-size:30px}.qwk-kopf h2{margin:0;font:700 20px Georgia,serif;color:#fff}.qwk-kopf small{color:var(--k-m)}
.qwk-x{all:unset;cursor:pointer;margin-left:auto;width:30px;height:30px;border-radius:9px;display:grid;place-items:center;color:var(--k-m);border:1px solid var(--k-l)}
.qwk-kpi{display:grid;grid-template-columns:1fr 1fr;gap:8px}.qwk-kpi div{background:var(--k-p2);border:1px solid var(--k-l);border-radius:12px;padding:9px 10px}.qwk-kpi small{display:block;color:var(--k-m);font-size:11px}.qwk-kpi b{font-size:17px;color:#fff}.qwk-kpi i{font-style:normal;font-size:11px;color:var(--k-m);font-weight:500}.qwk-kpi .plus{color:#ffb070}.qwk-kpi .minus{color:#7fb4ff}
.qwk-box{background:var(--k-p2);border:1px solid var(--k-l);border-radius:12px;padding:9px 10px;margin-top:8px}.qwk-box small{color:var(--k-m);font-size:11px}.qwk-spark{width:100%;height:56px;display:block;margin-top:4px}
.qwk-info h4{font:700 10.5px system-ui;letter-spacing:.14em;text-transform:uppercase;color:var(--k-m);margin:14px 0 7px}
.qwk-chip{display:inline-block;padding:5px 10px;margin:0 5px 6px 0;border-radius:20px;background:var(--k-p2);border:1px solid var(--k-l);color:#dbe4f6;font-size:12.5px;text-decoration:none}.qwk-chip.k{background:rgba(74,208,160,.1);border-color:rgba(74,208,160,.45);color:#a9f0d4}a.qwk-chip:hover{border-color:var(--k-a)}
.qwk-leer{text-align:center;color:var(--k-m);padding:30px 10px}.qwk-leer b{color:#fff;font-size:16px}.qwk-gl{font-size:40px;margin-bottom:8px}.qwk-mini{font-size:12px}
.qwk-zeit{grid-column:1/4;display:flex;align-items:center;gap:14px;padding:10px 18px;background:#0a101d;border-top:1px solid var(--k-l)}
.qwk-play{all:unset;cursor:pointer;width:38px;height:38px;border-radius:50%;background:linear-gradient(180deg,#1f8a6a,#14664e);display:grid;place-items:center;box-shadow:0 0 14px rgba(74,208,160,.35);font-size:14px}
.qwk-zeit input{flex:1;accent-color:#4ad0a0}.qwk-jahr{font:700 22px Georgia,serif;min-width:64px;text-align:right}.qwk-q{color:var(--k-m);font-size:10.5px;max-width:520px;line-height:1.35}
.qwk-mob{display:none}
@media (max-width:980px){.qwk{grid-template-columns:1fr;grid-template-rows:auto minmax(440px,1fr) auto;height:calc(100vh - 16px);width:calc(100vw - 16px);margin-left:calc(50% - 50vw + 8px);border-radius:14px}.qwk-top{padding:10px 12px;gap:8px}.qwk-titel small{display:none}.qwk-top{grid-column:1}.qwk-zeit{grid-column:1}.qwk-side,.qwk-info{position:absolute;z-index:5;left:0;right:0;bottom:62px;max-height:52%;border:1px solid var(--k-l);border-radius:18px 18px 0 0;transform:translateY(calc(100% + 90px));transition:.3s;box-shadow:0 -10px 40px rgba(0,0,0,.5)}.qwk.qwk-ebenen-auf .qwk-side,.qwk.qwk-info-auf .qwk-info{transform:none}.qwk-mob{display:inline-flex}.qwk-such{margin-left:0;width:100%}.qwk-such input{width:100%}.qwk-leg{bottom:10px;left:10px;right:auto;max-width:70%}.qwk-q{display:none}}
`;
function ui(root){
  const sw=(k,n,c,d)=>`<label class="qwk-sw"><input type="checkbox" data-ov="${k}" ${S.ov[k]?'checked':''}><span class="k"></span>${c?`<span class="dt ${d?'d':''}" style="color:${c};background:${c}"></span>`:''}${n}</label>`;
  const gb=(k,e)=>`<button data-grund="${k}" aria-pressed="${S.grund===k}">${e} ${GRUND[k].n}</button>`;
  const pl=(window.QW_DATEN&&window.QW_DATEN.pflanzen||[]).map(p=>`<option value="${p.id}">${p.nr} ${p.name.replace(' & Kiefernknospen','')}</option>`).join('');
  root.innerHTML=`<style>${CSS}</style><div class="qwk">
  <div class="qwk-top"><div class="qwk-titel"><span class="qwk-gl2"></span><div>Weltkarte<small>Bevölkerung · Ernährung · Rohstoffe · Natur</small></div></div>
   <div class="qwk-seg"><button data-modus="globus" aria-pressed="true">◉ Globus</button><button data-modus="flach" aria-pressed="false">▭ Karte</button></div>
   <div class="qwk-seg qwk-mob"><button data-auf="ebenen">☰ Ebenen</button><button data-auf="info">ⓘ Land</button></div>
   <div class="qwk-such"><input list="qwk-dl" placeholder="Land oder Pflanze suchen …"><datalist id="qwk-dl">${DAT.laender.map(c=>`<option value="${c.n}">`).join('')}${Object.keys(PFL).map(id=>`<option value="${pname(id)}">`).join('')}</datalist></div></div>
  <aside class="qwk-side">
   <h3>Grundkarte</h3><div class="qwk-grund">${gb('dichte','👥')}${gb('wachstum','📈')}${gb('energie','⚡')}${gb('erneuerbar','🌱')}${gb('klima','🌡️')}${gb('boden','🟫')}${gb('veg','🌳')}${gb('keine','🗺️')}</div>
   <h3>Menschen</h3>${sw('staedte','Großstädte (Ballungsräume)','#ffc860')}${sw('nacht','Tag & Nacht (jetzt)','#ffd860')}
   <h3>Getreide · Teil G</h3>${Object.entries(GETREIDE).map(([k,G])=>sw(k,G.e+' '+G.n,G.c)).join('')}
   <h3>Rohstoffe & Energie</h3>${Object.entries(ROH).map(([k,G])=>sw(k,G.e+' '+G.n,G.c,1)).join('')}
   <h3>Kompendium</h3>${sw('pfl','🌿 Herkunft der Pflanzen','#ff6a8a')}<select class="qwk-sel" data-pflanze><option value="">Wildvorkommen einer Pflanze zeigen …</option>${pl}</select>${sw('rez','🍽️ Rezepte nach Herkunft','#c79aff')}${sw('aut','👤 Autoren','#6ac8ff')}
  </aside>
  <div class="qwk-map"><canvas></canvas><div class="qwk-zoom"><button data-z="1.4" aria-label="Hineinzoomen">＋</button><button data-z="0.7" aria-label="Herauszoomen">－</button><button data-z="0" aria-label="Zurücksetzen">⟲</button></div><div class="qwk-leg"></div></div>
  <aside class="qwk-info"></aside>
  <div class="qwk-zeit"><button class="qwk-play" aria-label="Abspielen">▶</button><span style="color:var(--k-m)">1960</span><input type="range" min="1960" max="2023" value="${S.jahr}"><span class="qwk-jahr">${S.jahr}</span><span class="qwk-q">Quellen: Bevölkerung & Energie – Our World in Data (UN, Energy Institute); Getreide – FAOSTAT 2022; Reserven – Energy Institute, USGS, IAEA; Klima/Böden – vereinfachtes Schema</span></div>
  </div>`;
  wrap=$('.qwk',root); cv=$('canvas',wrap); ctx=cv.getContext('2d');
}
function groesse(){ const m=$('.qwk-map',wrap), r=m.getBoundingClientRect(); DPR=Math.min(2,devicePixelRatio||1); W=r.width; H=r.height; cv.width=W*DPR; cv.height=H*DPR; zeichne(); }
function ereignisse(){
  wrap.querySelectorAll('[data-ov]').forEach(i=>i.onchange=()=>{ S.ov[i.dataset.ov]=i.checked; legende(); zeichne(); });
  wrap.querySelectorAll('[data-grund]').forEach(b=>b.onclick=()=>{ S.grund=b.dataset.grund; wrap.querySelectorAll('[data-grund]').forEach(x=>x.setAttribute('aria-pressed',x===b)); legende(); zeichne(); });
  wrap.querySelectorAll('[data-modus]').forEach(b=>b.onclick=()=>{ S.modus=b.dataset.modus; S.zoom=1; S.px=S.py=0; wrap.querySelectorAll('[data-modus]').forEach(x=>x.setAttribute('aria-pressed',x===b)); zeichne(); });
  wrap.querySelectorAll('[data-auf]').forEach(b=>b.onclick=()=>{ wrap.classList.toggle('qwk-'+b.dataset.auf+'-auf'); });
  wrap.querySelectorAll('[data-z]').forEach(b=>b.onclick=()=>{ const z=+b.dataset.z; S.spin=false; if(!z){ S.zoom=1; S.px=S.py=0; } else S.zoom=Math.max(.6,Math.min(14,S.zoom*z)); zeichne(); });
  $('[data-pflanze]',wrap).onchange=e=>{ S.pflanze=e.target.value; if(S.pflanze){ const P=PFL[S.pflanze]; flieg(P[0][0],P[0][1]); } zeichne(); };
  const rg=$('.qwk-zeit input',wrap), jl=$('.qwk-jahr',wrap); rg.oninput=()=>{ S.jahr=+rg.value; jl.textContent=S.jahr; zeichne(); info(); };
  let spiel=null; $('.qwk-play',wrap).onclick=e=>{ if(spiel){ clearInterval(spiel); spiel=null; e.target.textContent='▶'; return; } e.target.textContent='❚❚'; if(S.jahr>=2023) S.jahr=1960; spiel=setInterval(()=>{ S.jahr++; rg.value=S.jahr; jl.textContent=S.jahr; zeichne(); info(); if(S.jahr>=2023){ clearInterval(spiel); spiel=null; e.target.textContent='▶'; } },140); };
  $('.qwk-such input',wrap).onchange=e=>{ const v=e.target.value.trim().toLowerCase(); const c=DAT.laender.find(c=>c.n.toLowerCase()===v); if(c){ waehle(c,c.mitte); flieg(c.mitte[0],c.mitte[1]); return; } const id=Object.keys(PFL).find(id=>pname(id).toLowerCase()===v); if(id){ S.pflanze=id; $('[data-pflanze]',wrap).value=id; S.ov.pfl=true; flieg(PFL[id][0][0],PFL[id][0][1]); zeichne(); } };
  const m=$('.qwk-map',wrap), P=new Map(); let start=null, d0=0, z0=1, bewegt=false;
  m.addEventListener('pointerdown',e=>{ m.setPointerCapture(e.pointerId); P.set(e.pointerId,[e.clientX,e.clientY]); S.spin=false; bewegt=false; start={x:e.clientX,y:e.clientY,lam:S.lam,phi:S.phi,px:S.px,py:S.py}; if(P.size===2){ const [a,b]=[...P.values()]; d0=Math.hypot(a[0]-b[0],a[1]-b[1]); z0=S.zoom; } });
  m.addEventListener('pointermove',e=>{ if(!P.has(e.pointerId)) return; P.set(e.pointerId,[e.clientX,e.clientY]);
    if(P.size===2){ const [a,b]=[...P.values()]; S.zoom=Math.max(.6,Math.min(14,z0*Math.hypot(a[0]-b[0],a[1]-b[1])/d0)); bewegt=true; zeichne(); return; }
    const dx=e.clientX-start.x, dy=e.clientY-start.y; if(Math.hypot(dx,dy)>4) bewegt=true; if(!bewegt) return;
    if(S.modus==='globus'){ const f=57/radius(); S.lam=start.lam-dx*f; S.phi=Math.max(-85,Math.min(85,start.phi+dy*f)); } else { S.px=start.px+dx; S.py=start.py+dy; }
    zeichne(); });
  const ende=e=>{ if(!P.has(e.pointerId)) return; P.delete(e.pointerId); if(!bewegt&&P.size===0){ const r=m.getBoundingClientRect(); const ll=inv(e.clientX-r.left,e.clientY-r.top); if(ll){ const c=landAn(ll[0],ll[1]); if(c) waehle(c,ll); else { S.sel=null; S.klick=null; info(); zeichne(); } } } };
  m.addEventListener('pointerup',ende); m.addEventListener('pointercancel',ende);
  m.addEventListener('wheel',e=>{ e.preventDefault(); S.spin=false; S.zoom=Math.max(.6,Math.min(14,S.zoom*(e.deltaY<0?1.15:1/1.15))); zeichne(); },{passive:false});
  addEventListener('resize',()=>{ if(document.body.contains(wrap)) groesse(); });
}
function waehle(c,ll){ S.sel=c.i; S.klick=ll; info(); zeichne(); wrap.classList.add('qwk-info-auf'); wrap.classList.remove('qwk-ebenen-auf'); }
function flieg(lon,lat){ S.spin=false; if(S.modus!=='globus'){ S.lam=lon; S.px=0; S.py=lat*Math.min(W/360,H/180)*S.zoom; zeichne(); return; } const a={l:S.lam,p:S.phi,z:S.zoom}, b={l:lon,p:Math.max(-60,Math.min(60,lat)),z:Math.max(S.zoom,1.5)}; let dl=((b.l-a.l+540)%360)-180; const t0=performance.now();
  (function st(t){ const k=Math.min(1,(t-t0)/900), e=k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2; S.lam=a.l+dl*e; S.phi=a.p+(b.p-a.p)*e; S.zoom=a.z+(b.z-a.z)*e; zeichne(); if(k<1&&document.body.contains(wrap)) requestAnimationFrame(st); })(t0); }
function dreh(){ if(!wrap||!document.body.contains(wrap)) return; if(S.spin&&S.modus==='globus'){ S.lam+=0.08; zeichne(); } requestAnimationFrame(dreh); }

window.QWWELT={ oeffne(root){ daten(); ui(root); ereignisse(); requestAnimationFrame(()=>{ groesse(); legende(); info(); }); S.spin=!window.QW_STANDBILD; requestAnimationFrame(dreh); },
  zustand:S, zeichne:()=>zeichne(), waehle:(i)=>{ const c=DAT.idx[i]; if(c){ waehle(c,c.mitte); flieg(c.mitte[0],c.mitte[1]); } } };
})();
