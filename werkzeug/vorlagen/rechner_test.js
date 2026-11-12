const Q=require('./rechner.js') /* Aufruf: node werkzeug/vorlagen/rechner_test.js – rechnet alle Karten mit Vorgabewerten */,K=Q._kern;
console.log(K.BEREICHE.map(b=>b[0]+':'+b[5]+':'+K.KARTEN.filter(k=>k.b===b[0]).length).join(' '));
console.log('Karten',K.KARTEN.length);
const ctx={heute:K.heuteDatum(Date.UTC(2026,10,12,10)),jetzt:Date.UTC(2026,10,12,10),kurse:K.richtKurse(),kursInfo:'x',grad:true,land:'SL'};
let fehler=0;
for(const k of K.KARTEN){const v={};k.f.forEach(f=>v[f.k]=f.w==null?null:f.w); if(k.vor){const vv=k.vor(ctx);for(const a in vv)v[a]=vv[a];}
 try{const e=k.r(v,ctx); if(!e||e.gross==null||/NaN|undefined/.test(JSON.stringify([e.gross,e.label,e.zeilen,e.schritte,e.hinweis]))){fehler++;console.log('!!',k.id,JSON.stringify([e.gross,e.label,e.zeilen,e.schritte]).slice(0,500));}
  if(/^(g-|ku-|b-|ge-|gs-|k-sonne|m-|z-)/.test(k.id)) console.log(k.id.padEnd(13),String(e.gross).padEnd(16),(e.einh||'').padEnd(22),'|',e.label,'|',(e.zeilen||[]).map(z=>z.join('=')).join(' ; ').slice(0,360));
 }catch(err){ if(!err.leer){fehler++;console.log('FEHLER',k.id,err.message);} }
}
console.log('Fehler:',fehler);
