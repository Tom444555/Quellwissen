/* Quellwissen · Weltkarte (eigenständiges Modul, offline) */
(function(){
const $=(s,r=document)=>r.querySelector(s);
const R2=Math.PI/180;
let DAT=null;
function daten(){ if(DAT) return DAT;
  DAT=JSON.parse(document.getElementById('weltdaten').textContent); DAT.idx={};
  DAT.laender.forEach(c=>{ DAT.idx[c.i]=c; let x0=1e9,x1=-1e9,y0=1e9,y1=-1e9; c.p.forEach(r=>r.forEach(([x,y])=>{x0=Math.min(x0,x);x1=Math.max(x1,x);y0=Math.min(y0,y);y1=Math.max(y1,y);})); c.bb=[x0,x1,y0,y1]; c.mitte=c.lp; });
  (DAT.bl||[]).forEach(b=>{ let x0=1e9,x1=-1e9,y0=1e9,y1=-1e9; b.p.forEach(r=>r.forEach(([x,y])=>{x0=Math.min(x0,x);x1=Math.max(x1,x);y0=Math.min(y0,y);y1=Math.max(y1,y);})); b.bb=[x0,x1,y0,y1]; });
  DAT.rmap={}; DAT.raster.forEach(g=>{ if(!g[5]) DAT.rmap[g[0]+','+g[1]]=g; });
  return DAT; }

/* ---------- kuratierte Daten (gerundet) ---------- */
const GETREIDE={
 weizen:{n:'Weizen',e:'🌾',c:'#f0b93a',q:'FAOSTAT 2022, Mio. t',l:'#g-brot',d:{CHN:137.7,IND:107.7,RUS:104.2,USA:44.9,AUS:36.2,CAN:34.3,FRA:33.6,PAK:26.2,DEU:22.6,UKR:20.2,TUR:19.8,ARG:18,KAZ:16.4,GBR:15.5,POL:13.2,IRN:10,EGY:9.7,ROU:8.7,ESP:7.4,ITA:6.8}},
 mais:{n:'Mais',e:'🌽',c:'#ffd84a',q:'FAOSTAT 2022, Mio. t',l:'#g-mais',d:{USA:348.8,CHN:277.2,BRA:109.4,ARG:59,IND:33.7,UKR:27,MEX:26.6,IDN:20,ZAF:16.1,RUS:15.8,CAN:14.5,NGA:12.7,FRA:10.9,ROU:8.8,EGY:7.4,ETH:10.7,TZA:6.9}},
 reis:{n:'Reis',e:'🍚',c:'#a8dc8a',q:'FAOSTAT 2022, Mio. t Rohreis',l:'#r-reisbrot',d:{CHN:208.5,IND:196.2,BGD:57.2,IDN:54.7,VNM:42.7,THA:34.3,MMR:24.7,PHL:19.8,KHM:11.6,PAK:11,BRA:10.8,JPN:10.4,NGA:8.3,USA:7.3,EGY:5.8,NPL:5.1,LKA:3.4}},
 gerste:{n:'Gerste',e:'🍺',c:'#d8a46a',q:'FAOSTAT 2022, Mio. t',l:'#g-bier',d:{RUS:23.4,AUS:14.4,FRA:11.6,DEU:11.4,CAN:10,TUR:8.5,GBR:7.4,ESP:6,UKR:5.8,ARG:5.3,USA:3.8,DNK:3.8,KAZ:3.5,POL:3.3,IRN:2.5,MAR:1.5}},
 hopfen:{n:'Hopfen',e:'🌿',c:'#7fd1a0',q:'FAOSTAT/IHGC 2022, Tsd. t',l:'#g-bier',d:{USA:47,DEU:34,CHN:6,CZE:5,POL:3.5,SVN:2.5,AUS:1.5,ESP:1,GBR:1,FRA:0.8}}};
const ROH={
 oel:{n:'Erdöl',e:'🛢️',c:'#ff8a3d',u:'Mrd. Barrel',q:'Reserven: Energy Institute 2020 · Förderung: OWID/EI',k:'oil',l:'#s-heizen',d:{VEN:304,SAU:297,CAN:168,IRN:158,IRQ:145,RUS:108,KWT:102,ARE:98,USA:69,LBY:48,NGA:37,KAZ:30,CHN:26,QAT:25,BRA:12,DZA:12,ECU:8,NOR:8,AGO:8,AZE:7,MEX:6,OMN:5,IND:4.5,EGY:3.1,GBR:2.5}},
 gas:{n:'Erdgas',e:'🔥',c:'#5fb8ff',u:'Bio. m³',q:'Reserven: Energy Institute 2020 · Förderung: OWID/EI',k:'gas',l:'#s-heizen',d:{RUS:37.4,IRN:32.1,QAT:24.7,TKM:13.6,USA:12.6,CHN:8.4,VEN:6.3,SAU:6,ARE:5.9,NGA:5.5,IRQ:3.5,AZE:2.5,AUS:2.4,CAN:2.4,DZA:2.3,KAZ:2.3,EGY:2.1,KWT:1.7,NOR:1.4,LBY:1.4}},
 kohle:{n:'Kohle',e:'⛏️',c:'#b0a8a0',u:'Mrd. t',q:'Reserven: Energy Institute 2020 · Förderung: OWID/EI',k:'coal',l:'#s-heizen',d:{USA:249,RUS:162,AUS:150,CHN:143,IND:111,DEU:36,IDN:35,UKR:34,POL:28,KAZ:26,TUR:11.5,ZAF:9.9,NZL:7.6,SRB:7.5,BRA:6.6,CAN:6.6,COL:4.6}},
 gold:{n:'Gold',e:'🥇',c:'#ffd23a',u:'Tsd. t Reserven',q:'USGS 2024: Reserven (Tsd. t) · Förderung 2023 (t)',d:{AUS:12,RUS:12,ZAF:5,IDN:3.6,USA:3,PER:2.5,BRA:2.4,CAN:2.3,CHN:2,UZB:1.8,MEX:1.4,PNG:1.2,GHA:1,KAZ:1},f:{CHN:370,AUS:310,RUS:310,CAN:200,USA:170,KAZ:130,GHA:130,MEX:120,UZB:100,IDN:110,PER:90,ZAF:100}},
 silber:{n:'Silber',e:'🥈',c:'#d8e0ea',u:'Tsd. t Reserven',q:'USGS 2024: Reserven (Tsd. t) · Förderung 2023 (t)',d:{PER:98,AUS:94,RUS:92,CHN:72,POL:61,MEX:37,CHL:26,USA:23,BOL:22},f:{MEX:6400,CHN:3400,PER:3100,CHL:1400,BOL:1300,POL:1300,RUS:1200,AUS:1100,USA:1000,ARG:800}},
 uran:{n:'Uran',e:'☢️',c:'#d6ff5a',u:'Tsd. t',q:'IAEA/NEA Red Book 2022, Ressourcen < 130 $/kg',d:{AUS:1684,KAZ:815,CAN:588,RUS:480,NAM:470,ZAF:320,NER:311,BRA:277,CHN:224,MNG:144,UZB:132,UKR:108,BWA:87,USA:59,TZA:58,JOR:52}},
 lithium:{n:'Lithium',e:'🔋',c:'#e07aff',u:'Tsd. t',q:'USGS 2024, Reserven (Bolivien: Ressourcen)',l:'#b-lithium',d:{CHL:9300,AUS:6200,ARG:3600,CHN:3000,USA:1100,CAN:930,ZWE:480,BRA:390,PRT:60,BOL:23000}}};
const T='C D'.split(' '), TE=['C','D','ET'];
const PFL={p01:[[20,50],'Eurasien (heute weltweit gemäßigt)',[[35,68,-10,140],[30,60,-130,-60]],T],p02:[[15,50],'Europa, Westasien',[[40,65,-10,90]],T],p03:[[30,48],'Eurasien (heute weltweit)',[[30,70,-180,180],[-55,-30,-75,175]],TE],p04:[[10,48],'Europa, Westasien, Nordafrika',[[34,62,-10,60]],T],p05:[[14,40],'Mittelmeerraum',[[30,46,-10,45]],['Cs','BS','Cf']],p06:[[10,50],'Europa (weltweit eingeschleppt)',[[30,65,-10,90],[30,55,-125,-65],[-45,-25,-75,175]],T],p07:[[20,52],'gesamte Nordhalbkugel',[[30,70,-180,180]],TE],p08:[[20,47],'Europa, Westasien',[[30,62,-10,100]],['C','D']],p09:[[60,48],'Eurasien',[[30,68,-10,150],[35,60,-100,-60]],T],p10:[[30,50],'Eurasien (weltweit eingeschleppt)',[[20,68,-180,180],[-50,-20,-75,175]],TE],p11:[[55,30],'vermutlich Persien bis Indien (heute weltweit)',[[15,45,-125,140],[-40,-15,-70,155]],['Cs','Cf','Cw','BS','Aw']],p12:[[20,46],'Europa, Westasien',[[35,60,-10,90]],T],p13:[[30,58],'boreale und gemäßigte Wälder der Nordhalbkugel',[[40,70,-180,180]],['Dfb','Dfc','Cfb']],p14:[[60,58],'Eurasien',[[40,70,-8,140]],['Dfb','Dfc','Cfb']],p15:[[127.4,0.8],'Molukken (Indonesien)',[[-8,3,95,135],[-25,-12,43,51],[-7,-4,38,40.5]],['Af','Aw']],p16:[[40,42],'Eurasien, Nordafrika',[[30,58,-10,100]],['BS','Cs','Dfb','Cf']],p17:[[-87,39],'östliches Nordamerika',[[30,46,-100,-75]],['Cfa','Dfa','Dfb']],p18:[[105,22],'Süd-/Südostasien',[[-10,28,70,125]],['Af','Aw','Cw']],p19:[[78,15],'Indien, Südostasien',[[5,30,68,110]],['Aw','Af','Cw']],p20:[[20,50],'Europa, Westasien',[[40,62,-10,60]],T],p21:[[-65,-20],'Anden (Bolivien, Nordargentinien)',[[-30,-10,-70,-55]],['H','Aw','Cf','BS']],p22:[[95,40],'Zentral- und Ostasien',[[25,55,-10,130]],['C','D','BS']],p23:[[46,16],'Arabische Halbinsel',[[12,30,35,60]],['BW','BS']],p24:[[40,52],'Eurasien',[[40,65,-10,130],[40,55,-100,-60]],T]};
const REZ=[['broetchen','Ostdeutsche Brötchen',12.4,51.3,'DEU'],['dinkelvollkorn','Dinkel-Vollkornbrot',9.2,48.6,'DEU'],['kartoffelbrot','Kartoffelbrot',10,51,'DEU'],['bierbrot','Bierbrot',11.5,49.5,'DEU'],['sauerkraut','Sauerkraut',7.8,48.4,'DEU'],['brioche','Brioche',-0.4,49.2,'FRA'],['grundteige','Focaccia & Pizza',14.25,40.85,'ITA'],['mohnkuchen','Mohnkuchen',15,50,'CZE'],['soljanka','Soljanka',37.6,55.8,'RUS'],['jagdwurstnudeln','Nudeln mit Jagdwurst',12,52,'DEU'],['baumstriezel','Baumstriezel',25,46.5,'ROU'],['reisbrot','Reisbrot',100,15,'THA']];
const AUT=[['storl','Wolf-Dieter Storl · Allgäu',10.2,47.7],['ganser','Daniele Ganser · Basel',7.6,47.56],['krall','Markus Krall · Schweiz',8.5,47.2],['nehls','Michael Nehls · Deutschland',9,49.2]];
/* Geschichte: Kriege [Name, von, bis, lon, lat, Opfer (Schätzung), Kurztext] */
const KRIEGE=[
 ['Dreißigjähriger Krieg',1618,1648,10.5,50.5,'ca. 4–8 Mio. Tote (mit Hunger und Seuchen)','Konfessions- und Machtkonflikt im Heiligen Römischen Reich mit Beteiligung fast aller europäischen Mächte; endete mit dem Westfälischen Frieden.'],
 ['Napoleonische Kriege',1803,1815,15,50,'ca. 3,5–6,5 Mio. Tote','Kriege Frankreichs unter Napoleon gegen wechselnde Koalitionen; Neuordnung Europas auf dem Wiener Kongress.'],
 ['Taiping-Aufstand',1850,1864,118,31,'ca. 20–30 Mio. Tote','Bürgerkrieg in China zwischen der Qing-Dynastie und dem „Himmlischen Reich“ der Taiping.'],
 ['Amerikanischer Bürgerkrieg',1861,1865,-78,38,'ca. 620.000–750.000 Tote','Krieg zwischen Nord- und Südstaaten der USA; endete mit der Abschaffung der Sklaverei.'],
 ['Erster Weltkrieg',1914,1918,3,50,'ca. 15–20 Mio. Tote','Krieg zwischen den Mittelmächten und der Entente; Ende der Kaiserreiche in Deutschland, Österreich-Ungarn, Russland und dem Osmanischen Reich.'],
 ['Russischer Bürgerkrieg',1917,1922,45,55,'ca. 7–12 Mio. Tote','Krieg zwischen Bolschewiki („Rote“) und ihren Gegnern („Weiße“) nach der Oktoberrevolution; Gründung der Sowjetunion 1922.'],
 ['Chinesischer Bürgerkrieg',1927,1949,113,34,'mehrere Millionen Tote','Krieg zwischen Kuomintang und Kommunisten (mit Unterbrechung im Zweiten Weltkrieg); Gründung der Volksrepublik China 1949.'],
 ['Zweiter Weltkrieg',1939,1945,20,50,'ca. 70–85 Mio. Tote','Größter Krieg der Geschichte, ausgelöst durch den deutschen Angriff auf Polen; in Asien Krieg Japans gegen China und die Alliierten. Holocaust an rund 6 Mio. Juden.'],
 ['Koreakrieg',1950,1953,127.5,38,'ca. 2,5–3 Mio. Tote','Krieg zwischen Nord- und Südkorea mit Beteiligung der USA, UNO-Truppen und Chinas; Waffenstillstand am 38. Breitengrad.'],
 ['Algerienkrieg',1954,1962,3,36,'ca. 0,3–1,5 Mio. Tote (Schätzungen weichen stark ab)','Unabhängigkeitskrieg Algeriens gegen Frankreich.'],
 ['Vietnamkrieg',1955,1975,106,16,'ca. 1,3–3 Mio. Tote','Krieg zwischen Nordvietnam (mit Vietcong) und Südvietnam mit den USA; endete mit der Einnahme Saigons.'],
 ['Nigerianischer Bürgerkrieg (Biafra)',1967,1970,7.5,6,'ca. 0,5–2 Mio. Tote, vor allem durch Hunger','Abspaltungsversuch der Region Biafra.'],
 ['Sowjetisch-Afghanischer Krieg',1979,1989,67,34,'ca. 0,5–2 Mio. Tote','Sowjetische Intervention in Afghanistan gegen Mudschaheddin, die u. a. von den USA und Pakistan unterstützt wurden.'],
 ['Iran-Irak-Krieg',1980,1988,47,32,'ca. 0,5–1 Mio. Tote','Grenz- und Machtkrieg zwischen Irak und Iran.'],
 ['Jugoslawienkriege',1991,2001,18,44,'ca. 130.000–140.000 Tote','Kriege beim Zerfall Jugoslawiens (Slowenien, Kroatien, Bosnien, Kosovo, Mazedonien).'],
 ['Ruanda: Bürgerkrieg und Völkermord',1990,1994,30,-2,'ca. 500.000–800.000 Tote (1994)','Bürgerkrieg zwischen Regierung und RPF; 1994 Völkermord an den Tutsi.'],
 ['Zweiter Kongokrieg',1998,2003,25,-3,'ca. 2,5–5,4 Mio. Tote (meist Krankheit und Hunger; umstrittene Zahl)','Krieg im Kongo mit Beteiligung mehrerer afrikanischer Staaten.'],
 ['Afghanistankrieg',2001,2021,67,34,'ca. 170.000–240.000 direkte Tote','Nach den Anschlägen vom 11. September Einsatz der USA und der NATO gegen Taliban und al-Qaida; Rückkehr der Taliban 2021.'],
 ['Irakkrieg',2003,2011,44,33,'ca. 150.000–600.000 Tote (Schätzungen weichen stark ab)','Einmarsch der USA und Verbündeter; Sturz Saddam Husseins, anschließend Aufstände und Bürgerkrieg.'],
 ['Syrischer Bürgerkrieg',2011,2024,38,35,'über 500.000 Tote','Aufstand gegen die Regierung Assad, später Krieg mit vielen Parteien und ausländischer Beteiligung; Sturz Assads im Dezember 2024.'],
 ['Krieg im Jemen',2014,null,45,15,'ca. 377.000 Tote bis 2021 (UN, direkt und indirekt)','Krieg zwischen Huthi und Regierung, ab 2015 mit einer von Saudi-Arabien geführten Koalition.'],
 ['Russisch-ukrainischer Krieg',2014,null,35,48.5,'Hunderttausende Tote und Verwundete (Schätzungen weichen stark ab)','2014 Annexion der Krim durch Russland und Kämpfe im Donbas; am 24.2.2022 Einmarsch Russlands in die Ukraine.'],
 ['Krieg in Gaza',2023,null,34.4,31.4,'ca. 1.200 Tote in Israel am 7.10.2023; laut Gesundheitsbehörde in Gaza über 60.000 Tote (Stand 2025)','Nach dem Angriff der Hamas auf Israel am 7.10.2023 Krieg im Gazastreifen.'],
 ['Bürgerkrieg im Sudan',2023,null,30,15,'Zehntausende Tote, über 10 Mio. Vertriebene','Krieg zwischen der sudanesischen Armee und der RSF-Miliz.']];
/* Völkerwanderungen [Name, Zeit-Text, Epoche, Farbe, Anzahl/Hinweis, Kurztext, [Pfade]] */
const WANDER=[
 ['Out of Africa','vor ca. 70.000–50.000 Jahren','vor','#ffd28a','Ausbreitung des modernen Menschen','Der Homo sapiens verlässt Afrika und besiedelt nach und nach alle Kontinente; Australien vor rund 50.000, Amerika vor rund 15.000–20.000 Jahren.',[[[36,8],[44,13],[55,24],[75,22],[100,15],[118,-3],[135,-25]],[[44,13],[38,32],[28,42],[10,48]],[[75,22],[100,42],[140,58],[170,65],[-160,64],[-120,52],[-100,30],[-78,5],[-65,-35]]]],
 ['Indogermanische Ausbreitung','ca. 3000–1000 v. Chr.','vor','#e8a0ff','nach der heute verbreiteten Steppen-Hypothese','Hirtenvölker aus der pontisch-kaspischen Steppe (Jamnaja-Kultur) verbreiten indogermanische Sprachen nach Europa sowie nach Iran und Indien.',[[[42,48],[25,49],[8,49],[-3,52]],[[42,48],[62,44],[70,36],[77,28]]]],
 ['Bantu-Expansion','ca. 1000 v. Chr.–500 n. Chr.','antike','#ff9a6a','','Bauern aus dem Grenzgebiet Kamerun/Nigeria breiten sich über Zentral-, Ost- und Südafrika aus – mit Ackerbau und Eisenverarbeitung.',[[[10,6],[18,-2],[26,-10],[30,-22]],[[10,6],[25,2],[34,-2],[38,-8]]]],
 ['Austronesische Seefahrer','ca. 3000 v. Chr.–1250 n. Chr.','vor','#6ad0ff','','Von Taiwan aus besiedeln Seefahrer die Philippinen, Indonesien, Madagaskar und den Pazifik bis Hawaii, Osterinsel und Neuseeland.',[[[121,23.5],[121,14],[117,-2],[140,-6],[178,-18],[-150,-17],[-157,20]],[[117,-2],[90,-6],[47,-19]],[[-150,-17],[-109,-27]],[[-150,-17],[174,-40]]]],
 ['Völkerwanderung der Spätantike','375–568 n. Chr.','antike','#ffcf5a','','Hunnen dringen nach Europa vor; Goten, Vandalen, Franken, Langobarden, Angeln und Sachsen ziehen in das Weströmische Reich, das 476 endet.',[[[62,47],[35,47],[20,47]],[[30,47],[20,45],[12,42],[-4,40]],[[16,51],[3,47],[-5,37],[10,36]],[[16,48],[10,45.5]],[[9,54.5],[0,52]]]],
 ['Arabische Expansion','632–750 n. Chr.','mittel','#7ad87a','','Nach dem Tod Mohammeds breitet sich das Kalifat von Arabien bis Spanien und Zentralasien aus.',[[[40,22],[36,33],[31,30],[10,34],[-6,35],[-4,40]],[[40,22],[44,33],[60,36],[70,40]]]],
 ['Wikinger','793–1066','mittel','#8ab8ff','','Skandinavische Seefahrer handeln, plündern und siedeln von Island und Grönland bis Neufundland sowie über die Flüsse Osteuropas bis Byzanz.',[[[10,60],[-2,56],[-20,64],[-45,61],[-55,51]],[[18,59],[30,59],[31,50],[29,41]],[[8,58],[-1,50],[0,46]]]],
 ['Mongolische Eroberungen','1206–1300','mittel','#ff6a6a','','Unter Dschingis Khan und seinen Nachfolgern entsteht das größte zusammenhängende Landreich der Geschichte.',[[[107,48],[80,42],[55,38],[44,33]],[[80,42],[50,47],[30,50],[18,50]],[[107,48],[116,40],[110,25]]]],
 ['Atlantischer Sklavenhandel','ca. 1500–1867','neu','#ff8a8a','ca. 12,5 Mio. Menschen verschleppt','Europäische Händler verschleppen Menschen aus West- und Zentralafrika gewaltsam nach Amerika, vor allem nach Brasilien und in die Karibik.',[[[3,6],[-20,5],[-38,-12]],[[3,6],[-30,12],[-72,18]],[[12,-6],[-20,-12],[-43,-23]],[[3,6],[-35,25],[-77,35]]]],
 ['Europäische Auswanderung nach Amerika','1820–1920','neu','#a8c8ff','ca. 50 Mio. Menschen','Massenauswanderung aus Irland, Deutschland, Italien, Skandinavien und Osteuropa nach Nord- und Südamerika.',[[[-8,53],[-40,48],[-74,40.7]],[[9,53],[-35,47],[-74,40.7]],[[14,41],[-20,10],[-58.4,-34.6]]]],
 ['Flucht und Vertreibung der Deutschen','1944–1950','20','#ffb0b0','ca. 12–14 Mio. Menschen','Flucht und Vertreibung von Deutschen aus Ostmitteleuropa am Ende des Zweiten Weltkriegs und danach.',[[[20.5,54.7],[14,53.5],[10,53]],[[17,51],[13,51],[10,50]],[[21,48.5],[16,48.5],[12,49]]]],
 ['Teilung Britisch-Indiens','1947','20','#ffc070','ca. 10–20 Mio. Menschen, Hunderttausende Tote','Bei der Gründung von Indien und Pakistan fliehen Muslime, Hindus und Sikhs über die neuen Grenzen.',[[[77,29.5],[74.3,31.5]],[[74.3,31.5],[77,29]],[[88.4,22.6],[90.4,23.8]]]],
 ['Gastarbeiter nach Westeuropa','1955–1973','20','#9ae0c0','Millionen Menschen','Anwerbeabkommen holen Arbeitskräfte aus Italien, Spanien, Griechenland, der Türkei und Jugoslawien nach Westdeutschland und Westeuropa.',[[[32.8,39.9],[20,44],[8.7,50.1]],[[14,41],[9,48]],[[-3.7,40.4],[2.3,48.9]]]],
 ['Flucht aus Syrien','seit 2011','heute','#ffd0a0','über 6 Mio. Menschen ins Ausland (UNHCR)','Flucht vor dem Bürgerkrieg, vor allem in die Türkei, nach Libanon, Jordanien und Europa.',[[[38,35],[35,39]],[[37,34],[35.5,33.9]],[[37,33],[36,31.9]],[[38,36],[28,40],[13.4,52.5]]]],
 ['Flucht aus der Ukraine','seit 2022','heute','#a0d0ff','rund 6 Mio. Menschen im Ausland (UNHCR)','Flucht vor dem Krieg, vor allem nach Polen, Deutschland, Tschechien und in andere EU-Länder.',[[[31,49.5],[21,52.2]],[[31,49.5],[13.4,52.5]],[[30,48],[14.4,50.1]]]]];
/* Erfindungen [Was, Jahr, Wer, Ort, lon, lat, Kurztext, Link] (negative Jahre = v. Chr.) */
const ERF=[
 ['Rad',-3500,'Sumerer','Mesopotamien',45.5,31,'Erst Töpferscheibe, dann Wagenrad.'],['Keilschrift',-3200,'Sumerer','Uruk',45.6,31.3,'Eine der ältesten Schriften, zuerst für Vorratslisten.'],['Bier',-3500,'Sumerer','Mesopotamien',44.4,32.5,'Vergorenes Getreide – eines der ältesten Lebensmittel-Verfahren.','#g-bier'],['Sauerteigbrot',-1500,'Ägypter','Ägypten',31.2,30,'Gelockertes Brot durch wilde Hefen und Milchsäurebakterien.','#s-hefe'],
 ['Münzgeld',-600,'Lyder','Sardes',28,38.5,'Erste geprägte Münzen aus Elektron (Gold-Silber-Legierung).','#w-geld'],['Wassermühle',-250,'Griechen','östliches Mittelmeer',23.7,37.97,'Wasserkraft mahlt Getreide.'],['Papier',105,'Cai Lun','Luoyang (China)',112.4,34.6,'Aus Pflanzenfasern geschöpftes Papier.'],['Schießpulver',850,'chinesische Alchemisten','China',108.9,34.3,'Ursprünglich auf der Suche nach Lebenselixieren entdeckt.'],
 ['Papiergeld',1024,'Song-Dynastie','Chengdu (China)',104.07,30.67,'Staatliche Jiaozi-Scheine.','#w-geld'],['Bewegliche Lettern',1040,'Bi Sheng','China',114.3,30.6,'Druck mit Tonlettern, Jahrhunderte vor Gutenberg.'],['Magnetkompass',1100,'Song-Dynastie','China',120.15,30.28,'Navigation auf See.'],['Buchdruck',1450,'Johannes Gutenberg','Mainz',8.27,50,'Metalllettern und Druckerpresse – Beginn der Massenmedien.'],
 ['Fernrohr',1608,'Hans Lipperhey','Middelburg',3.61,51.5,'Erstes Patent auf ein Linsenfernrohr.'],['Mikroskop (Einlinser)',1674,'Antoni van Leeuwenhoek','Delft',4.36,52.01,'Sieht als Erster Bakterien und Hefezellen.','#s-hefe'],['Pendeluhr',1656,'Christiaan Huygens','Den Haag',4.3,52.08,'Erste genaue Uhr.'],['Porzellan (Europa)',1708,'Johann Friedrich Böttger','Dresden/Meißen',13.47,51.16,'Nacherfindung des chinesischen Porzellans.'],
 ['Dampfmaschine',1712,'Thomas Newcomen','Dudley (England)',-2.08,52.51,'Pumpen für Bergwerke; James Watt verbessert sie ab 1769.'],['Blitzableiter',1752,'Benjamin Franklin','Philadelphia',-75.16,39.95,'Schutz vor Blitzschlag.'],['Heißluftballon',1783,'Brüder Montgolfier','Annonay',4.67,45.24,'Erster bemannter Flug.'],['Pockenimpfung',1796,'Edward Jenner','Berkeley (England)',-2.45,51.69,'Kuhpocken schützen vor Pocken.'],
 ['Batterie',1800,'Alessandro Volta','Como/Pavia',9.08,45.81,'Voltasche Säule – erste Stromquelle.'],['Konservierung in Gläsern',1809,'Nicolas Appert','Massy/Paris',2.27,48.73,'Haltbarmachen durch Erhitzen in verschlossenen Gefäßen.','#s-einfrieren'],['Laufmaschine',1817,'Karl Drais','Mannheim',8.47,49.49,'Vorläufer des Fahrrads.'],['Fotografie',1826,'Nicéphore Niépce','Saint-Loup-de-Varennes',4.86,46.72,'Älteste erhaltene Fotografie.'],
 ['Eisenbahn',1825,'George Stephenson','Stockton–Darlington',-1.32,54.57,'Erste öffentliche Dampfeisenbahn.'],['Telegraf (Morse)',1844,'Samuel Morse','Washington',-77,38.9,'Nachrichten über Draht.'],['Kunstdünger',1840,'Justus von Liebig','Gießen',8.67,50.58,'Mineralstofftheorie der Pflanzenernährung.','#s-boden'],['Pasteurisierung',1864,'Louis Pasteur','Paris',2.35,48.86,'Erhitzen tötet Keime – auch Beweis, dass Hefe gärt.','#s-hefe'],
 ['Telefon',1876,'Alexander Graham Bell (Vorläufer Philipp Reis 1861)','Boston',-71.06,42.36,'Sprache über Draht.'],['Kältemaschine',1876,'Carl von Linde','München',11.58,48.14,'Grundlage des Kühlschranks.','#s-einfrieren'],['Glühbirne (langlebig)',1879,'Thomas Edison','Menlo Park',-74.33,40.56,'Kohlefaden-Glühlampe.'],['Automobil',1886,'Carl Benz','Mannheim',8.47,49.49,'Benz Patent-Motorwagen Nr. 1.'],
 ['Dieselmotor',1893,'Rudolf Diesel','Augsburg',10.9,48.37,'Selbstzünder mit hohem Wirkungsgrad.'],['Röntgenstrahlen',1895,'Wilhelm Conrad Röntgen','Würzburg',9.93,49.79,'Blick in den Körper.'],['Funk / Radio',1895,'Guglielmo Marconi','Bologna',11.34,44.49,'Drahtlose Nachrichtenübertragung.'],['Motorflug',1903,'Brüder Wright','Kitty Hawk',-75.7,36.02,'Erster gesteuerter Motorflug.'],
 ['Haber-Bosch-Verfahren',1910,'Fritz Haber, Carl Bosch','Karlsruhe/Ludwigshafen',8.4,49.48,'Stickstoffdünger aus Luft – ernährt heute rund die Hälfte der Menschheit.','#s-boden'],['Penicillin',1928,'Alexander Fleming','London',-0.13,51.5,'Erstes Antibiotikum aus Schimmelpilzen.'],['Fernsehen',1926,'John Logie Baird','London',-0.14,51.52,'Erstes funktionierendes Fernsehbild.'],['Kernspaltung',1938,'Otto Hahn, Fritz Straßmann (Lise Meitner)','Berlin',13.29,52.45,'Entdeckung der Uranspaltung.'],
 ['Computer Z3',1941,'Konrad Zuse','Berlin',13.4,52.52,'Erster funktionsfähiger programmierbarer Rechner.'],['Transistor',1947,'Bardeen, Brattain, Shockley','Murray Hill (USA)',-74.4,40.68,'Grundbaustein aller Elektronik.'],['DNA-Doppelhelix',1953,'Watson, Crick (Franklin, Wilkins)','Cambridge',0.12,52.2,'Aufbau des Erbguts.'],['Satellit (Sputnik)',1957,'Sowjetunion','Baikonur',63.3,45.96,'Erster künstlicher Erdsatellit.'],
 ['Laser',1960,'Theodore Maiman','Malibu',-118.7,34.03,'Gebündeltes Licht.'],['Internet (ARPANET)',1969,'US-Forschungsnetz','Los Angeles',-118.44,34.07,'Erste Verbindung zwischen zwei Rechnern.'],['Mobiltelefon',1973,'Martin Cooper (Motorola)','New York',-74,40.75,'Erstes Handy-Gespräch.'],['World Wide Web',1989,'Tim Berners-Lee','CERN, Genf',6.05,46.23,'Verlinkte Seiten im Internet.'],['MP3',1991,'Fraunhofer-Institut','Erlangen',11,49.6,'Komprimierte Musik.'],['Smartphone (iPhone)',2007,'Apple','Cupertino',-122.03,37.32,'Computer in der Hosentasche.']];
/* Geldgeschichte [Ereignis, Jahr, Ort, lon, lat, Kurztext] */
const GELD=[['Silbergeld nach Gewicht',-3000,'Mesopotamien',44.4,32.5,'Silber wird abgewogen (Schekel); Tempel verleihen Gerste und Silber gegen Zins.'],['Erste Münzen',-600,'Lydien (Sardes)',28,38.5,'König Alyattes/Kroisos: geprägte Münzen aus Elektron, dann reines Gold und Silber.'],['Römische Münzverschlechterung',260,'Rom',12.5,41.9,'Der Silbergehalt des Denars sinkt auf wenige Prozent – Inflation im 3. Jahrhundert.'],['Erstes Papiergeld',1024,'Chengdu (China)',104.07,30.67,'Staatliche Jiaozi-Scheine; später Überdruck und Inflation.'],['Florin',1252,'Florenz',11.25,43.77,'Goldmünze als europäische Leitwährung.'],['Amsterdamer Wisselbank',1609,'Amsterdam',4.9,52.37,'Öffentliche Girobank.'],['Erste europäische Banknoten',1661,'Stockholm',18.07,59.33,'Stockholms Banco gibt Banknoten aus – und geht bald pleite.'],['Bank of England',1694,'London',-0.09,51.51,'Gegründet, um Kriege zu finanzieren.'],['John Law & Mississippi-Blase',1720,'Paris',2.35,48.86,'Papiergeldexperiment in Frankreich endet im Zusammenbruch.'],['Goldstandard Großbritannien',1717,'London',-0.13,51.5,'Isaac Newton legt den Goldpreis fest; ab 1821 offizieller Goldstandard.'],['Goldmark',1873,'Berlin',13.4,52.52,'Das Deutsche Reich führt die Goldwährung ein, finanziert auch mit französischen Reparationen.'],['Federal Reserve',1913,'Washington',-77.04,38.9,'Gründung der US-Zentralbank.'],['Goldeinlösung ausgesetzt',1914,'Europa',8,50,'Zur Kriegsfinanzierung beenden die Staaten den Umtausch von Banknoten in Gold.'],['Hyperinflation',1923,'Berlin',13.4,52.52,'Ein US-Dollar kostet im November 4,2 Billionen Mark; danach Rentenmark.'],['Goldverbot USA',1933,'Washington',-77.04,38.9,'Executive Order 6102: Privatpersonen müssen Gold abgeben; 1934 Goldpreis 35 $.'],['Bretton Woods',1944,'Bretton Woods (USA)',-71.44,44.26,'Dollar an Gold (35 $/Unze), andere Währungen an den Dollar; IWF und Weltbank entstehen.'],['D-Mark',1948,'Frankfurt am Main',8.68,50.11,'Währungsreform in den Westzonen.'],['Nixon-Schock',1971,'Washington',-77.04,38.9,'15. August: Die USA beenden die Goldeinlösung – seither reines Papiergeld (Fiatgeld).'],['Freie Wechselkurse',1973,'Paris',2.35,48.86,'Ende der festen Wechselkurse von Bretton Woods.'],['Euro',1999,'Frankfurt am Main',8.68,50.11,'Euro als Buchgeld, 2002 als Bargeld; EZB in Frankfurt.'],['Finanzkrise',2008,'New York',-74.01,40.71,'Bankenkrise; danach Nullzins und Anleihekäufe der Zentralbanken.'],['Bitcoin',2009,'Internet',-30,30,'Digitales Geld ohne Zentralbank (Satoshi Nakamoto).']];
/* Goethe [Ort, von, bis, lon, lat, Dauer, Anlass] – Reihenfolge = Lebensweg */
const GOETHE=[['Frankfurt am Main',1749,1765,8.68,50.11,'16 Jahre','Geburt am 28.8.1749, Kindheit und Jugend'],['Leipzig',1765,1768,12.37,51.34,'3 Jahre','Jurastudium'],['Frankfurt am Main',1768,1770,8.68,50.11,'1,5 Jahre','Krankheit und Genesung'],['Straßburg',1770,1771,7.75,48.58,'1,5 Jahre','Studienabschluss, Begegnung mit Herder, Friederike Brion in Sesenheim'],['Wetzlar',1772,1772,8.5,50.56,'4 Monate','Praktikum am Reichskammergericht – Stoff für den „Werther“'],['Frankfurt am Main',1772,1775,8.68,50.11,'3 Jahre','Anwalt; „Götz“, „Werther“ (1774)'],['Zürich / Gotthard',1775,1775,8.54,47.37,'2 Monate','Erste Schweizer Reise'],['Weimar',1775,1832,11.33,50.98,'56 Jahre','Minister unter Herzog Carl August, Dichter, Naturforscher; Tod am 22.3.1832'],['Brocken (Harz)',1777,1777,10.62,51.8,'Tage','Harzreise im Winter, Besteigung des Brockens'],['Genf / Chamonix',1779,1779,6.14,46.2,'3 Monate','Zweite Schweizer Reise'],['Karlsbad',1786,1786,12.87,50.23,'Wochen','Aufbruch zur Italienischen Reise am 3.9.1786 (insgesamt 16 Kuraufenthalte 1785–1823)'],['Verona',1786,1786,10.99,45.44,'Tage','Italienische Reise'],['Venedig',1786,1786,12.33,45.44,'2 Wochen','Italienische Reise'],['Rom',1786,1788,12.48,41.9,'ca. 16 Monate','Hauptstation der Italienischen Reise; Kunst und Antike'],['Neapel',1787,1787,14.25,40.85,'ca. 2 Monate','Vesuv-Besteigungen'],['Palermo / Sizilien',1787,1787,13.36,38.12,'ca. 6 Wochen','Suche nach der „Urpflanze“ im Botanischen Garten'],['Weimar',1788,1788,11.33,50.98,'',''],['Valmy (Champagne)',1792,1792,4.77,49.08,'Wochen','„Campagne in Frankreich“ mit dem Herzog'],['Mainz',1793,1793,8.27,50,'Wochen','Belagerung von Mainz'],['Jena',1794,1805,11.59,50.93,'viele Aufenthalte','Freundschaft mit Schiller, Universität'],['Teplitz',1812,1812,13.83,50.64,'Wochen','Begegnung mit Beethoven'],['Wiesbaden / Heidelberg',1814,1815,8.24,50.08,'Monate','Rhein- und Mainreisen; Marianne von Willemer, „West-östlicher Divan“'],['Marienbad',1823,1823,12.7,49.96,'Wochen','Ulrike von Levetzow, „Marienbader Elegie“'],['Weimar',1823,1832,11.33,50.98,'','Vollendung des „Faust II“ (1831)']];
/* zusätzliche Kriege/Operationen aus Gansers „Illegale Kriege“ */
KRIEGE.push(
 ['Sturz der Regierung Mossadegh (Iran)',1953,1953,51.4,35.7,'mehrere hundert Tote','Von CIA und britischem Geheimdienst unterstützter Putsch gegen Premier Mossadegh, der das Erdöl verstaatlicht hatte.'],
 ['Putsch in Guatemala',1954,1954,-90.5,14.6,'wenige hundert Tote; Folgebürgerkrieg 1960–1996 rund 200.000','Von der CIA organisierter Sturz des gewählten Präsidenten Árbenz.'],
 ['Suezkrise',1956,1956,32.3,30.6,'ca. 3.000 Tote','Angriff Israels, Großbritanniens und Frankreichs auf Ägypten nach der Verstaatlichung des Suezkanals.'],
 ['Invasion in der Schweinebucht',1961,1961,-81.1,22.1,'einige hundert Tote','Von der CIA organisierte Landung von Exilkubanern gegen Fidel Castro.'],
 ['Contra-Krieg in Nicaragua',1981,1990,-85.2,12.9,'ca. 30.000–50.000 Tote','Von den USA unterstützte Contras gegen die Sandinisten-Regierung; 1986 vom Internationalen Gerichtshof verurteilt.'],
 ['Golfkrieg (Kuwait)',1990,1991,47.5,29.3,'ca. 20.000–35.000 Tote','Irak besetzt Kuwait; eine Koalition unter Führung der USA befreit Kuwait mit UN-Mandat.'],
 ['Kosovokrieg / NATO-Luftangriffe',1999,1999,20.9,42.7,'ca. 13.500 Tote im Kosovokonflikt 1998–2000; ca. 500 zivile Tote durch die Luftangriffe','NATO bombardiert Jugoslawien 78 Tage lang – mit deutscher Beteiligung – ohne Mandat des UN-Sicherheitsrats.'],
 ['Libyenkrieg',2011,2011,13.2,32.9,'mehrere tausend bis über 10.000 Tote','Aufstand gegen Gaddafi; NATO-Luftangriffe auf Grundlage der UN-Resolution 1973 zur Flugverbotszone; Sturz und Tod Gaddafis.']);
/* Sicht Daniele Ganser und gängige Darstellung (neutral nebeneinander) */
const GANSER={
 'Sturz der Regierung Mossadegh (Iran)':['Beispiel für eine verdeckte Operation der USA und Großbritanniens; Ursprung des heutigen Misstrauens Irans gegenüber dem Westen.','Die CIA hat ihre Rolle 2013 in freigegebenen Akten offiziell bestätigt.'],
 'Putsch in Guatemala':['Illegaler Sturz einer gewählten Regierung im Interesse der United Fruit Company.','Die CIA-Beteiligung ist durch freigegebene Akten belegt.'],
 'Suezkrise':['Angriffskrieg ohne UN-Mandat; Verstoß gegen das Gewaltverbot der UN-Charta.','Auch damals von der UNO und den USA verurteilt; Rückzug der Angreifer.'],
 'Invasion in der Schweinebucht':['Illegale Invasion; der US-Botschafter bestritt vor dem UN-Sicherheitsrat jede Beteiligung. Erklärt die spätere Kuba-Krise.','Die Verantwortung der CIA ist offiziell bestätigt (u. a. Church-Ausschuss).'],
 'Vietnamkrieg':['Der Tonkin-Zwischenfall 1964 diente als Vorwand; ein Teil der Angriffe hat so nicht stattgefunden.','Freigegebene NSA-Dokumente (2005) bestätigen, dass der zweite Zwischenfall vom 4.8.1964 nicht stattfand.'],
 'Contra-Krieg in Nicaragua':['Illegaler Krieg der USA über Stellvertreter.','Der Internationale Gerichtshof verurteilte die USA 1986 (Nicaragua v. USA).'],
 'Kosovokrieg / NATO-Luftangriffe':['Illegaler Angriffskrieg ohne UN-Mandat, an dem sich Deutschland unter Schröder und Fischer beteiligte.','Die NATO begründete den Einsatz als humanitäre Intervention; völkerrechtlich ist er umstritten, da ein Mandat fehlte.'],
 'Afghanistankrieg':['Ohne ausreichende Rechtsgrundlage begonnen; der Auslöser 9/11 sei nicht aufgeklärt (WTC 7).','Die NATO berief sich auf das Selbstverteidigungsrecht (Art. 51) nach 9/11; der UN-Sicherheitsrat erkannte dieses in Resolution 1368 an.'],
 'Irakkrieg':['Illegaler Angriffskrieg auf Grundlage der Lüge von Massenvernichtungswaffen.','Massenvernichtungswaffen wurden nicht gefunden; UN-Generalsekretär Kofi Annan nannte den Krieg 2004 „illegal“.'],
 'Libyenkrieg':['Die UN-Resolution zur Flugverbotszone wurde zum Regimewechsel überdehnt; illegaler Krieg.','Die NATO berief sich auf Resolution 1973 (Schutz von Zivilisten); Russland und China kritisierten die Auslegung.'],
 'Syrischer Bürgerkrieg':['Auch ein verdeckter Krieg westlicher und regionaler Staaten zum Regimewechsel.','Westliche Regierungen betonen den Aufstand gegen Assad und dessen Gewalt gegen Zivilisten; die Unterstützung von Rebellen durch Ausland ist dokumentiert.'],
 'Russisch-ukrainischer Krieg':['Die Invasion 2022 war illegal, aber durch die NATO-Osterweiterung und den Putsch 2014 provoziert; Schüsse auf dem Maidan als False Flag; Frieden durch Neutralität der Ukraine.','Westliche Regierungen und die UN-Generalversammlung bewerten den Krieg als völkerrechtswidrigen, unprovozierten Angriff; die Ereignisse 2014 gelten dort als Revolution.'],
 'Zweiter Weltkrieg':['Ganser behandelt vor allem die Zeit danach: NATO-Geheimarmeen (Gladio) als Folge des Kalten Krieges.','Die Existenz der Stay-behind-Armeen ist seit 1990 offiziell bestätigt.']};

const EPOCHE={vor:'Vor- und Frühgeschichte',antike:'Antike',mittel:'Mittelalter',neu:'Neuzeit',20:'20. Jahrhundert',heute:'seit 2000'};
const KLIMA={Af:['Tropischer Regenwald','#2f6bff'],Aw:['Tropische Savanne','#46aafa'],BW:['Wüste','#ff4a3a'],BS:['Steppe','#f5a500'],Cs:['Mittelmeerklima','#f2e33a'],Cfa:['Feucht-subtropisch','#a8e05a'],Cwa:['Subtropisch, Wintertrocken','#5ac878'],Cfb:['Gemäßigt ozeanisch','#3fa848'],Dfb:['Kontinental','#30b6ff'],Dfc:['Subarktisch (Taiga-Klima)','#3a8a96'],ET:['Tundra','#b0b8c0'],EF:['Ewiges Eis','#e6eef6'],H:['Hochgebirge','#a08068']};
const BODEN={tscher:['Schwarzerde (Tschernosem)','#2b241e'],braun:['Braunerde, Parabraunerde','#9a7a4a'],podsol:['Podsol (Bleicherde)','#b8b0a0'],perma:['Permafrost (Kryosol)','#8fa3b8'],eis:['Eis','#e6eef6'],ferral:['Laterit (Ferralsol)','#c4522a'],rot:['Rotlehm, Acrisol','#b8703a'],wueste:['Wüstenboden, Sand','#e8c98a'],kastan:['Kastanozem (Steppenboden)','#8a6a3a'],vert:['Vertisol (Quelltonboden)','#6a5a7a'],loess:['Löss','#e0c070'],gebirge:['Gebirgsböden','#7a7a70']};
const VEGN={regen:['Tropischer Regenwald','#1f8a3a'],savanne:['Savanne','#c8b840'],wueste:['Wüste','#e8c88a'],steppe:['Steppe, Grasland','#b8c86a'],hartlaub:['Hartlaubwald (Macchie)','#8aa850'],subtrop:['Subtropischer Wald','#5ab060'],laub:['Laubwald','#3aa050'],misch:['Mischwald','#2f8a5a'],taiga:['Taiga (Nadelwald)','#1f6a5a'],tundra:['Tundra','#9aa890'],eis:['Eis','#e6eef6'],gebirge:['Gebirge','#9a8a78']};
const MAGMA=['#1b1035','#4a1a6e','#8a2a7a','#cf4a5a','#f78a3a','#fde27a'];
const DIV=['#2a6ab8','#7fb4e0','#e8e2d0','#f5a55a','#d2462a'];
const TEAL=['#0e2a3a','#145a6a','#1a8a8a','#4ac0a0','#b8f0b0'];
const GRN=['#2a2420','#3a4a2a','#4a7a3a','#6ab04a','#c8f07a'];
const ROT=['#2a1a2a','#5a2048','#9a2a4a','#d8503a','#ffb05a'];
const BLAU=['#3a1a1a','#7a3a2a','#c08040','#80c0a0','#5ad0ff'];
/* Deutschland nach Bundesländern (amtliche Zahlen): [Suizidrate 2024, Männer, Frauen, Suizide 2024, Demenz 65+ in Tsd., Straftaten je 100.000 (PKS 2024), Aufklärungsquote %] */
const DE={MV:[16.6,27.2,6.3,261,38,6661,64.4],SN:[15.9,24.1,8.0,645,104,7287,60.5],ST:[15.7,23.9,7.7,335,55,8447,55.3],HB:[15.3,20.4,10.4,108,14,15235,45.5],SH:[14.6,19.8,9.6,431,64,7196,60.6],BY:[14.0,20.0,8.2,1854,253,4635,67.9],BE:[13.7,16.5,11.1,505,67,14252,45.5],HE:[12.9,18.9,7.1,811,120,6046,61.9],TH:[12.8,20.8,4.9,269,52,7355,60.9],BB:[12.2,18.7,5.9,312,61,6842,58.4],RP:[12.0,18.1,6.1,496,83,5735,64.3],BW:[11.9,16.7,7.2,1336,219,5180,62.6],NI:[11.1,16.3,6.0,888,165,6485,62.8],HH:[10.9,13.1,8.8,202,32,11775,47.9],NW:[10.2,15.1,5.4,1835,353,7689,53.5],SL:[8.3,14.0,2.7,84,22,6597,61.2]};
/* [Lebenserwartung Jungen, Mädchen 2021/23, Durchschnittsalter 12/2024, verfügb. Einkommen je Ew. 2024, BIP je Ew. 2025, Ökolandbau-Anteil 2023 %] */
const DEX={"BW":[79.64,83.93,44.0,31966,59335,14.0],"BY":[78.94,83.51,44.3,33204,62200,null],"BE":[78.08,83.17,42.8,27595,59097,null],"BB":[77.17,83.09,47.5,27560,40759,17.6],"HB":[76.74,82.08,43.1,26542,60974,null],"HH":[78.14,82.98,42.2,32004,90208,null],"HE":[78.63,83.11,44.3,31683,60894,15.4],"MV":[76.24,82.58,48.1,26913,40495,null],"NI":[77.77,82.59,45.1,29080,49907,5.7],"NW":[77.91,82.43,44.5,29197,50470,6.1],"RP":[78.34,82.92,45.1,30519,44915,null],"SL":[77.09,81.92,46.4,26617,42765,19.4],"SN":[77.41,83.61,47.1,26818,41693,null],"ST":[75.49,82.07,48.3,26297,38452,null],"SH":[78.25,82.72,45.8,30247,44344,null],"TH":[76.76,82.59,47.9,26497,38591,8.2]};
const DEBUND={de_su:12.4,de_dem:null,de_hz:6894,de_aq:58.0,de_le:80.58,de_alt:44.8,de_ek:30069,de_bip:53516,de_oeko:11.1};
function deWert(c,k){ const d=DE[c]; if(!d) return null; if(k==='de_su') return d[0]; if(k==='de_hz') return d[5]; if(k==='de_aq') return d[6]; if(k==='de_dem') return d[4]*1000/(d[3]/d[0]*1e5)*100; const x=DEX[c]; if(k==='de_le') return (x[0]+x[1])/2; if(k==='de_alt') return x[2]; if(k==='de_ek') return x[3]; if(k==='de_bip') return x[4]; if(k==='de_oeko') return x[5]; return null; }
const MEERE=[['Atlantischer Ozean',-38,30,0],['Atlantischer Ozean',-18,-25,0],['Pazifischer Ozean',-150,22,0],['Pazifischer Ozean',-125,-25,0],['Pazifischer Ozean',168,12,0],['Indischer Ozean',78,-22,0],['Arktischer Ozean',-10,84,1],['Südlicher Ozean',20,-62,1],['Südlicher Ozean',-140,-64,1],
 ['Mittelmeer',18,35,2.6],['Karibisches Meer',-75,15,2.8],['Golf von Mexiko',-90,25,3],['Arabisches Meer',64,15,2.8],['Golf von Bengalen',89,14,3],['Südchinesisches Meer',114,13,3],['Beringmeer',-178,58,3],['Hudson Bay',-85,60,3.2],['Nordsee',3.5,56,3.6],['Ostsee',19,58,4.2],['Schwarzes Meer',34,43.2,3.6],['Kaspisches Meer',50.5,41,4],['Rotes Meer',38,20,3.8],['Japanisches Meer',135,40,3.6],['Ochotskisches Meer',150,54,3.4],['Korallenmeer',156,-17,3.2],['Tasmansee',160,-38,3.2],['Golf von Guinea',2,1,3.4],['Europäisches Nordmeer',2,69,3.4],['Philippinensee',132,19,3.4],['Golf von Alaska',-145,56,3.6],['Biskaya',-5,45.5,4.4],['Persischer Golf',51.5,27,4.4],['Labradorsee',-54,58,3.8]];
const TIEFEN=[['Marianengraben',142.2,11.35,10935],['Tongagraben',-174.7,-23.25,10800],['Philippinengraben',126.6,10.4,10540],['Kermadecgraben',-177.4,-31.9,10047],['Kurilengraben',152.5,44.2,9600],['Puerto-Rico-Graben',-66.5,19.8,8400],['Südsandwichgraben',-25.0,-56.2,8265],['Atacamagraben',-71.5,-23.4,8065],['Sundagraben',110.0,-10.6,7290],['Molloytief (Arktis)',2.8,79.1,5550],['Calypsotief (Mittelmeer)',21.1,36.6,5267],['Landsorttief (Ostsee)',18.3,58.6,459]];
/* Staats- und Regierungsform (vereinfacht, Stand 2026); nicht gelistete Staaten = Präsidial-/semipräsidentielle Republik */
const STAAT={
 pr:['Parlamentarische Republik','#4a9ad8','DEU AUT ITA IRL ISL MLT GRC ALB MKD MNE SRB BIH HRV SVN HUN CZE SVK POL EST LVA FIN CHE ISR IND PAK BGD NPL IRQ LBN ARM GEO MDA BGR SGP TTO DMA BRB MUS ETH SOM VUT SMR FJI WSM NRU MHL BWA ZAF XKX MNG'],
 pm:['Parlamentarische Monarchie','#9a7ad8','GBR CAN AUS NZL JAM BHS BLZ ATG KNA LCA VCT GRD PNG SLB TUV NOR SWE DNK NLD BEL LUX ESP AND MCO LIE JPN THA KHM MYS BTN LSO TON'],
 pp:['Präsidial- / semipräsidentielle Republik','#e8a050',''],
 am:['Monarchie mit starker Herrschermacht','#d8607a','SAU OMN QAT ARE BRN SWZ MAR JOR KWT BHR'],
 ep:['Einparteienstaat','#c03030','CHN VNM LAO CUB PRK ERI'],
 th:['Theokratie / geistliche Führung','#2a8a6a','IRN AFG VAT'],
 mi:['Militär-, Übergangs- oder Bürgerkriegsregierung','#8a8a8a','MMR MLI BFA NER SDN GIN SYR LBY HTI YEM'],
 na:['abhängiges oder umstrittenes Gebiet','#3a4458','GRL PRI NCL PYF FLK ESH ATF ATA HKG MAC ABW CUW BMU CYM TCA VGB VIR GUM MNP ASM FRO IMN JEY GGY ALA SPM WLF NIU COK PCN SHN SGS HMD IOT AIA MSR BLM MAF SXM NFK PSE SML NCY']};
const STAATI={}; Object.entries(STAAT).forEach(([k,v])=>v[2].split(' ').forEach(i=>i&&(STAATI[i]=k)));
function staatVon(i){ return STAATI[i]||'pp'; }
/* Grundkarten: n Name, u Einheit, k Datenschlüssel, s Skala(v)->0..1, p Palette, lg Legende [links, mitte, rechts] */
const GRUND={
 relief:{n:'Relief (Topografie)',g:'Natur',e:'⛰️'},
 klima:{n:'Klimazonen',g:'Natur',e:'🌡️',r:2},boden:{n:'Böden',g:'Natur',e:'🟫',r:3},veg:{n:'Vegetation',g:'Natur',e:'🌳',r:4},
 dichte:{n:'Bevölkerungs\u00addichte',g:'Menschen',e:'👥',u:'Ew./km²',p:MAGMA,s:v=>Math.log10(Math.max(v,1))/3,lg:['1','30','1000+']},
 wachstum:{n:'Wachstum',g:'Menschen',e:'📈',u:'% pro Jahr',p:DIV,s:v=>(v+1)/5,lg:['−1 %','±0','+4 %']},
 le:{n:'Lebens\u00aderwartung',g:'Menschen',e:'❤️',u:'Jahre',k:'le',p:BLAU,s:v=>(v-40)/45,lg:['40','62','85']},
 fr:{n:'Geburtenrate',g:'Menschen',e:'👶',u:'Kinder je Frau',k:'fr',p:DIV,s:v=>(v-1)/6,lg:['1','4','7']},
 km:{n:'Kinder\u00adsterblichkeit',g:'Menschen',e:'🍼',u:'je 1.000 unter 5 J.',k:'km',p:ROT,s:v=>Math.log10(Math.max(v,2))/2.5,lg:['2','30','300']},
 su:{n:'Suizidrate',g:'Menschen',e:'🕯️',u:'je 100.000 (altersstandardisiert)',p:ROT,s:v=>v/30,lg:['0','15','30+']},
 gl:{n:'Lebens\u00adzufriedenheit',g:'Menschen',e:'😊',u:'Skala 0–10',k:'gl',p:BLAU,s:v=>(v-3)/5,lg:['3','5,5','8']},
 un:{n:'Unter\u00adernährung',g:'Menschen',e:'🥣',u:'% der Bevölkerung',k:'un',p:ROT,s:v=>v/50,lg:['0 %','25 %','50 %']},
 energie:{n:'Energie pro Kopf',g:'Wirtschaft',e:'⚡',u:'kWh pro Kopf',k:'epc',p:TEAL,s:v=>Math.log10(Math.max(v,300))/5.2-0.45,lg:['wenig','','viel']},
 erneuerbar:{n:'Erneuerbarer Strom',g:'Wirtschaft',e:'🌱',u:'% des Stroms',k:'ren',p:GRN,s:v=>v/100,lg:['0 %','50 %','100 %']},
 keine:{n:'Nur Länder',g:'Natur',e:'🗺️'},
 staat:{n:'Staatsform',g:'Politik',e:'🏛️',kat:1,l:'#w-politik'},
 de_su:{n:'Suizidrate',g:'Deutschland',de:1,e:'🕯️',u:'je 100.000 Ew. · 2024',p:ROT,s:v=>(v-8)/9,lg:['8','12,5','17'],q:'Destatis, Todesursachenstatistik 2024 (Darstellung NaSPro)',l:'#w-suizid'},
 de_dem:{n:'Demenz (65+)',g:'Deutschland',de:1,e:'🧠',u:'Betroffene je 100 Ew. · berechnet',p:MAGMA,s:v=>(v-1.5)/1.2,lg:['1,5','2,1','2,7'],q:'Deutsche Alzheimer Gesellschaft, Infoblatt 1 (Stand 2025); Einwohner aus Destatis',l:'#w-demenz'},
 de_hz:{n:'Straftaten',g:'Deutschland',de:1,e:'🚔',u:'Fälle je 100.000 Ew. · PKS 2024',p:ROT,s:v=>(v-4500)/11000,lg:['4.500','10.000','15.200'],q:'BKA, Polizeiliche Kriminalstatistik 2024',l:'#w-kriminalitaet'},
 de_le:{n:'Lebens\u00aderwartung',g:'Deutschland',de:1,e:'❤️',u:'Jahre bei Geburt · 2021/23',p:BLAU,s:v=>(v-79)/3.2,lg:['79','80,6','82,2'],q:'Statistisches Bundesamt, Sterbetafel 2021/2023',l:'#w-deutschland'},
 de_alt:{n:'Durchschnitts\u00adalter',g:'Deutschland',de:1,e:'👵',u:'Jahre · Ende 2024',p:MAGMA,s:v=>(v-42)/6.5,lg:['42','45','48,3'],q:'vdek-Basisdaten nach Statistischem Bundesamt (12/2024)',l:'#w-deutschland'},
 de_ek:{n:'Einkommen',g:'Deutschland',de:1,e:'💶',u:'verfügbar je Einwohner · 2024',p:GRN,s:v=>(v-26000)/7500,lg:['26.000 €','29.700 €','33.200 €'],q:'Arbeitskreis VGR der Länder (2026)',l:'#w-deutschland'},
 de_bip:{n:'Wirtschafts\u00adleistung',g:'Deutschland',de:1,e:'🏭',u:'BIP je Einwohner · 2025',p:TEAL,s:v=>Math.log(v/38000)/Math.log(90000/38000),lg:['38.000 €','58.000 €','90.000 €'],q:'Arbeitskreis VGR der Länder (2026)',l:'#w-deutschland'},
 de_oeko:{n:'Ökolandbau',g:'Deutschland',de:1,e:'🌾',u:'% der Agrarfläche · 2023',p:GRN,s:v=>v/20,lg:['0 %','10 %','20 %'],q:'Umweltbundesamt nach Destatis; nur 7 Länder veröffentlicht',l:'#w-deutschland'},
 de_aq:{n:'Aufklärungs\u00adquote',g:'Deutschland',de:1,e:'🔎',u:'% der Fälle · PKS 2024',p:GRN,s:v=>(v-45)/23,lg:['45 %','56 %','68 %'],q:'BKA, Polizeiliche Kriminalstatistik 2024',l:'#w-kriminalitaet'}};
function ramp(stops,t){ t=Math.max(0,Math.min(1,t)); const n=stops.length-1, k=Math.min(n-1,Math.floor(t*n)), f=t*n-k; const hx=h=>[1,3,5].map(i=>parseInt(h.slice(i,i+2),16)); const a=hx(stops[k]),b=hx(stops[k+1]); return `rgb(${a.map((v,i)=>Math.round(v+(b[i]-v)*f)).join(',')})`; }

/* ---------- Zustand ---------- */
const S={modus:'globus',lam:-15,phi:25,zoom:1,px:0,py:0,grund:'relief',jahr:2023,unterlage:true,
 ov:{wolken:true,namen:true,staedte:true,grenzen:true,fluesse:true,landschaft:false,gipfel:false,weizen:false,mais:false,reis:false,gerste:false,hopfen:false,oel:false,gas:false,kohle:false,gold:false,silber:false,uran:false,lithium:false,pfl:false,rez:false,aut:false,nacht:false,kriege:false,wander:false,erf:false,geld:false,goethe:false,tiefen:false},
 bl:null,
 epoche:'',pflanze:'',sel:null,klick:null,hist:null,spin:true,bewegt:false};
let cv,ctx,W=0,H=0,DPR=1,wrap;

/* ---------- Projektion ---------- */
function radius(){ return Math.min(W,H)*0.45*S.zoom; }
function kf(){ return Math.min(W/360,H/180)*S.zoom; }
function rd(){ return Math.min(W,H)*0.44*S.zoom; }
function proj(lon,lat){
  if(S.modus==='globus'){ const l=(lon-S.lam)*R2,p=lat*R2,p0=S.phi*R2, r=radius();
    const cosc=Math.sin(p0)*Math.sin(p)+Math.cos(p0)*Math.cos(p)*Math.cos(l);
    return [W/2+r*Math.cos(p)*Math.sin(l), H/2-r*(Math.cos(p0)*Math.sin(p)-Math.sin(p0)*Math.cos(p)*Math.cos(l)), cosc]; }
  if(S.modus==='scheibe'){ const r=(90-lat)/180*rd(), a=(lon-S.lam)*R2; return [W/2+S.px+r*Math.sin(a), H/2+S.py+r*Math.cos(a), 1]; }
  const k=kf(); let x=lon-S.lam; x=((x+540)%360)-180; return [W/2+x*k+S.px, H/2-lat*k+S.py, 1]; }
function inv(x,y){
  if(S.modus==='globus'){ const r=radius(), X=(x-W/2)/r, Y=-(y-H/2)/r, rho=Math.hypot(X,Y); if(rho>1) return null; const c=Math.asin(rho), p0=S.phi*R2;
    const lat=Math.asin(Math.cos(c)*Math.sin(p0)+(rho?Y*Math.sin(c)*Math.cos(p0)/rho:0));
    const lon=S.lam*R2+Math.atan2(X*Math.sin(c), rho*Math.cos(p0)*Math.cos(c)-Y*Math.sin(p0)*Math.sin(c));
    return [((lon/R2+540)%360)-180, lat/R2]; }
  if(S.modus==='scheibe'){ const dx=x-W/2-S.px, dy=y-H/2-S.py, r=Math.hypot(dx,dy), R0=rd(); if(r>R0) return null; return [((Math.atan2(dx,dy)/R2+S.lam+540)%360)-180, 90-r/R0*180]; }
  const k=kf(); const lon=(x-W/2-S.px)/k+S.lam, lat=-(y-H/2-S.py)/k; if(Math.abs(lat)>90) return null; return [((lon+540)%360)-180,lat]; }
function pfad(ring,offen){
  if(S.modus==='globus'){ const r=radius(); let start=true, sichtbar=false; const pts=ring.map(([a,b])=>proj(a,b));
    for(const q of pts) if(q[2]>0){sichtbar=true;break;} if(!sichtbar) return false;
    if(offen){ for(const q of pts){ if(q[2]<0){start=true;continue;} if(start){ctx.moveTo(q[0],q[1]);start=false;} else ctx.lineTo(q[0],q[1]); } return true; }
    for(const q of pts){ let x=q[0],y=q[1]; if(q[2]<0){ const dx=x-W/2,dy=y-H/2,d=Math.hypot(dx,dy)||1; x=W/2+dx/d*r; y=H/2+dy/d*r; }
      if(start){ctx.moveTo(x,y);start=false;} else ctx.lineTo(x,y); } ctx.closePath(); return true; }
  if(S.modus==='scheibe'){ ring.forEach(([a,b],k)=>{ const q=proj(a,b); k?ctx.lineTo(q[0],q[1]):ctx.moveTo(q[0],q[1]); }); if(!offen) ctx.closePath(); return true; }
  let lx=null; ring.forEach(([a,b],k)=>{ const q=proj(a,b); if(k===0||Math.abs(q[0]-lx)>W*0.5) ctx.moveTo(q[0],q[1]); else ctx.lineTo(q[0],q[1]); lx=q[0]; }); if(!offen) ctx.closePath(); return true; }

/* ---------- Werte ---------- */
function ow(i){ return DAT.owid[i]||{}; }
function reihe(i,k){ const a=ow(i)[k]; if(!a) return null; const out=new Array(64).fill(null); for(let j=1;j<a.length;j++) out[a[0]+j-1]=a[j]; return out; }
function ser(i,k,jahr,genau){ const a=ow(i)[k]; if(!a) return null; let idx=jahr-1960-a[0]+1; if(genau) return idx>=1&&idx<a.length?a[idx]:null; idx=Math.min(idx,a.length-1); for(let j=idx;j>=1;j--) if(a[j]!=null) return {v:a[j],j:1960+a[0]+j-1}; return null; }
function wert(i,art,jahr){ const c=DAT.idx[i];
  if(art==='pop'){ const r=ser(i,'pop',jahr); return r&&r.v; }
  if(art==='dichte'){ const r=ser(i,'pop',jahr); return r&&c.a>200?r.v*1000/c.a:null; }
  if(art==='wachstum'){ const a=ser(i,'pop',jahr,true), b=ser(i,'pop',jahr-1,true); return a&&b?(a/b-1)*100:null; }
  if(art==='su'){ const m=ser(i,'sm',jahr), f=ser(i,'sf',jahr); return m&&f?(m.v+f.v)/2:null; }
  const g=GRUND[art]; if(g&&g.k){ const r=ser(i,g.k,jahr); return r&&r.v; } return null; }
function stand(i,art,jahr){ const k=art==='su'?'sm':(GRUND[art]&&GRUND[art].k); if(!k) return null; const r=ser(i,k,jahr); return r&&r.j; }
function farbe(i){ const g=GRUND[S.grund]; if(g.kat) return STAAT[staatVon(i)][1]; if(!g.p) return null; const v=wert(i,S.grund,S.jahr); return v==null?null:ramp(g.p,g.s(v)); }
function fmt(v,d=0){ return v==null?'–':v.toLocaleString('de-DE',{maximumFractionDigits:d,minimumFractionDigits:d}); }
function zstufe(){ return 2.2+2.4*Math.log2(Math.max(S.zoom,.5))-(W<520?.2:0); } // kleine Bildschirme: weniger Namen, mehr beim Zoomen

/* ---------- Relief (Textur) ---------- */
let TEX=null, TW=0, TH=0, RC=null, RKEY='', RTIMER=null;
function textur(){ if(TEX!==null||glAn()) return; TEX=false; const el=document.getElementById('weltrelief'); if(!el) return; const im=new Image(); im.onload=()=>{ const c=document.createElement('canvas'); TW=c.width=im.width; TH=c.height=im.height; const x=c.getContext('2d'); x.drawImage(im,0,0); TEX=x.getImageData(0,0,TW,TH).data; RKEY=''; zeichne(); }; im.src='data:image/jpeg;base64,'+el.textContent.trim(); }
function relief(fein){
  if(!TEX) return null; const s=fein?Math.min(DPR,1.5):0.5, w=Math.max(1,Math.round(W*s)), h=Math.max(1,Math.round(H*s)); const key=[S.modus,S.lam.toFixed(2),S.phi.toFixed(2),S.zoom.toFixed(3),S.px|0,S.py|0,w,h].join('|');
  if(key===RKEY&&RC) return RC; if(!RC) RC=document.createElement('canvas'); RC.width=w; RC.height=h; const x=RC.getContext('2d'); const img=x.createImageData(w,h), d=img.data;
  if(S.modus==='globus'){ const r=radius()*s, cx=W/2*s, cy=H/2*s, p0=S.phi*R2, sp=Math.sin(p0), cp=Math.cos(p0), l0=S.lam*R2;
    const y0=Math.max(0,Math.floor(cy-r)), y1=Math.min(h-1,Math.ceil(cy+r));
    for(let py=y0;py<=y1;py++){ const Y=-(py-cy)/r; const xx=Math.sqrt(Math.max(0,1-Y*Y))*r; const x0=Math.max(0,Math.floor(cx-xx)), x1=Math.min(w-1,Math.ceil(cx+xx));
      for(let px=x0;px<=x1;px++){ const X=(px-cx)/r, rr=X*X+Y*Y; if(rr>1) continue; const z=Math.sqrt(1-rr);
        const lat=Math.asin(z*sp+Y*cp), lon=l0+Math.atan2(X, z*cp-Y*sp);
        let u=((lon/(2*Math.PI)+0.5)%1+1)%1, v=0.5-lat/Math.PI; const o=(py*w+px)*4; let cr,cg,cb;
        if(fein){ const fx=u*TW-0.5, fy=Math.max(0,Math.min(TH-1.001,v*TH-0.5)), x0=Math.floor(fx), y0b=fy|0, ax=fx-x0, ay=fy-y0b, xa=((x0%TW)+TW)%TW, xb=(xa+1)%TW, i00=(y0b*TW+xa)*4, i10=(y0b*TW+xb)*4, i01=i00+TW*4, i11=i10+TW*4, w00=(1-ax)*(1-ay), w10=ax*(1-ay), w01=(1-ax)*ay, w11=ax*ay;
          cr=TEX[i00]*w00+TEX[i10]*w10+TEX[i01]*w01+TEX[i11]*w11; cg=TEX[i00+1]*w00+TEX[i10+1]*w10+TEX[i01+1]*w01+TEX[i11+1]*w11; cb=TEX[i00+2]*w00+TEX[i10+2]*w10+TEX[i01+2]*w01+TEX[i11+2]*w11; }
        else { const ti=(Math.min(TH-1,(v*TH)|0)*TW+((u*TW)|0))*4; cr=TEX[ti]; cg=TEX[ti+1]; cb=TEX[ti+2]; }
        // Licht: Sonne links oben vorn; Rand wird bläulich (Lufthülle); Meer bekommt einen sanften Glanz
        const dif=Math.max(0,-0.42*X+0.46*Y+0.78*z), sh=0.5+0.62*dif, at=Math.pow(1-z,3)*0.6;
        let gl=0; if(cb>cr+14&&cb>=cg){ const hh=Math.max(0,-0.22*X+0.24*Y+0.945*z); gl=Math.pow(hh,60)*46; }
        d[o]=Math.min(255,(cr*sh+gl)*(1-at)+70*at); d[o+1]=Math.min(255,(cg*sh+gl)*(1-at)+130*at); d[o+2]=Math.min(255,(cb*sh+gl)*(1-at)+225*at); d[o+3]=255; } } }
  else if(S.modus==='scheibe'){ const R0=rd()*s, cx=(W/2+S.px)*s, cy=(H/2+S.py)*s, y0=Math.max(0,Math.floor(cy-R0)), y1=Math.min(h-1,Math.ceil(cy+R0));
    for(let py=y0;py<=y1;py++){ const dy=py-cy; for(let px=0;px<w;px++){ const dx=px-cx, r=Math.sqrt(dx*dx+dy*dy); if(r>R0) continue; const lat=90-r/R0*180, lon=Math.atan2(dx,dy)/R2+S.lam;
      const u=(((lon+180)/360)%1+1)%1, ty=Math.min(TH-1,((0.5-lat/180)*TH)|0), ti=(ty*TW+((u*TW)|0))*4, o=(py*w+px)*4; d[o]=TEX[ti]; d[o+1]=TEX[ti+1]; d[o+2]=TEX[ti+2]; d[o+3]=255; } } }
  else { const k=kf()*s; for(let py=0;py<h;py++){ const lat=-((py-H/2*s-S.py*s)/k); if(lat>90||lat<-90) continue; const ty=Math.min(TH-1,((0.5-lat/180)*TH)|0);
      for(let px=0;px<w;px++){ const lon=(px-W/2*s-S.px*s)/k+S.lam; const u=(((lon+180)/360)%1+1)%1, ti=(ty*TW+((u*TW)|0))*4, o=(py*w+px)*4; d[o]=TEX[ti]; d[o+1]=TEX[ti+1]; d[o+2]=TEX[ti+2]; d[o+3]=255; } } }
  x.putImageData(img,0,0); RKEY=key; return RC; }

/* ---------- Naturbild der Erde (WebGL): Wasser nach Tiefe, Land nach Klimazone und Höhe, Schummerung, Wolken, Lufthülle,
   Tag-Nacht-Grenze, Stadtlichter, Sterne. Ein Programm für Globus, Karte und Scheibe. Alles aus den eingebetteten Daten
   (Relief, Höhen/Tiefen, 2°-Raster, Städte) – keine Datei wird nachgeladen. Ohne WebGL zeichnet weiter die Canvas-Fassung. ---------- */
const BIOF={regen:[26,74,32],savanne:[122,116,62],wueste:[198,170,120],steppe:[150,142,92],hartlaub:[98,106,62],subtrop:[58,98,44],laub:[54,94,42],misch:[46,86,42],taiga:[34,68,44],tundra:[118,114,94],gebirge:[122,114,102],eis:[238,242,247]};
const GLV='attribute vec2 a;void main(){gl_Position=vec4(a,0.,1.);}';
const GLF=`precision highp float;
uniform vec2 uGr,uPan,uSonneP;uniform float uDpr,uMode,uR,uLam,uPhi,uK,uZeit,uWolken,uThema,uPlain,uNacht,uRoh,uBereit,uFein,uUnscharf,uLichtart,uBump;
uniform vec3 uSonne,uBlick,uOst,uNord;uniform sampler2D tRel,tRelK,tHoe,tBio,tNac,tWol;
const float PI=3.14159265;
float h1(vec2 p){p=fract(p*vec2(123.34,456.21));p+=dot(p,p+45.32);return fract(p.x*p.y);}
float vn(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(h1(i),h1(i+vec2(1.,0.)),f.x),mix(h1(i+vec2(0.,1.)),h1(i+vec2(1.,1.)),f.x),f.y);}
float fbm(vec2 p){return .5*vn(p)+.25*vn(p*2.03+7.)+.125*vn(p*4.1+13.)+.0625*vn(p*8.3+29.);}
vec3 himmel(vec2 p){vec2 q=p/max(uGr.x,uGr.y);vec3 c=mix(vec3(.022,.036,.075),vec3(.006,.009,.02),clamp(length(q-.5*uGr/max(uGr.x,uGr.y))*1.5,0.,1.));
 float mw=fbm(q*3.2+vec2(uLam,-uPhi)*.03+3.);float band=exp(-pow((q.y-.42+(q.x-.5)*.6)*3.4,2.));c+=vec3(.05,.06,.1)*band*mw*mw*1.5;
 for(int i=0;i<3;i++){float fi=float(i);float cell=fi<.5?96.:(fi<1.5?44.:19.);vec2 pp=p+vec2(uLam,-uPhi)*(fi<.5?34.:(fi<1.5?16.:7.))+fi*37.;vec2 g=floor(pp/cell);float r=h1(g+fi*17.3);
  if(r>(fi<.5?.72:(fi<1.5?.6:.45))){vec2 st=(vec2(h1(g+1.3),h1(g+2.7))*.7+.15)*cell;float d=length(pp-g*cell-st);float gr=fi<.5?1.5:(fi<1.5?1.05:.75);float hell=(fi<.5?1.:(fi<1.5?.62:.36))*(.5+.5*h1(g+5.1));
   vec3 fa=mix(vec3(.75,.85,1.),vec3(1.,.9,.75),h1(g+9.7));c+=fa*hell*(smoothstep(gr,0.,d)+(fi<.5?.22*smoothstep(gr*4.,0.,d):0.));}}
 return c;}
void main(){
 vec2 p=vec2(gl_FragCoord.x,uGr.y*uDpr-gl_FragCoord.y)/uDpr;vec3 raum=uRoh>.5?vec3(0.):himmel(p);vec3 col=raum;float lon=0.,lat=0.,tr=0.,z=1.;vec2 q=vec2(0.);float rr=0.;vec2 dS=vec2(0.);float rS=0.;
 if(uMode<.5){q=(p-uGr*.5)/uR;q.y=-q.y;rr=dot(q,q);if(rr<1.){z=sqrt(1.-rr);float sp=sin(uPhi),cp=cos(uPhi);lat=asin(clamp(z*sp+q.y*cp,-1.,1.));lon=uLam+atan(q.x,z*cp-q.y*sp);tr=1.;}}
 else if(uMode<1.5){lon=((p.x-uGr.x*.5-uPan.x)/uK)*PI/180.+uLam;lat=-((p.y-uGr.y*.5-uPan.y)/uK)*PI/180.;if(abs(lat)<=PI*.5)tr=1.;}
 else{dS=p-uGr*.5-uPan;rS=length(dS)/uR;if(rS<=1.){lat=PI*.5-rS*PI;lon=atan(dS.x,dS.y)+uLam;tr=1.;}}
 if(tr>.5){
  vec2 uv=vec2(fract(lon/(2.*PI)+.5),clamp(.5-lat/PI,0.001,.999));float cl=cos(lat),sl=sin(lat),co=cos(lon),so=sin(lon);
  vec3 U=vec3(cl*co,cl*so,sl),E=vec3(-so,co,0.),N=vec3(-sl*co,-sl*so,cl);
  vec3 S=uLichtart<.5?uSonne:normalize(-.45*E+.45*N+.77*U);float nS=dot(U,S);
  float tag=uLichtart<.5?smoothstep(-.10,.20,nS):1.;if(uMode>1.5&&uNacht>.5)tag=mix(.2,1.,1.-smoothstep(.42,1.15,length(p-uSonneP)/uR));
  float still=max(uThema,uPlain);tag=mix(tag,1.,still);
  vec3 alb;float wasser=0.,eis=0.;float hE=0.,hN=0.;
  if(uBereit<.5||uPlain>.5){vec3 rel=uBereit>.5?texture2D(tRelK,uv).rgb:vec3(.1,.2,.4);wasser=uBereit>.5?smoothstep(.03,.11,rel.b-rel.r)*step(rel.g,rel.b+.03):1.;alb=mix(vec3(.118,.172,.227),vec3(.035,.13,.26),wasser);}
  else{
   vec3 rel=mix(texture2D(tRel,uv).rgb,texture2D(tRelK,uv).rgb,uUnscharf);float h=texture2D(tHoe,uv).r;vec2 e=vec2(1./2048.,1./1024.)*1.3;
   hE=(texture2D(tHoe,uv+vec2(e.x,0.)).r-texture2D(tHoe,uv-vec2(e.x,0.)).r)/max(cl,.2);hN=texture2D(tHoe,uv-vec2(0.,e.y)).r-texture2D(tHoe,uv+vec2(0.,e.y)).r;
   wasser=smoothstep(.03,.11,rel.b-rel.r)*step(rel.g,rel.b+.03);
   vec4 bio=texture2D(tBio,uv);float hoehe=clamp((h-.5)*2.,0.,1.),lum=dot(rel,vec3(.3,.59,.11));float kalt=smoothstep(.45,.97,abs(sl));
   vec3 land=mix(rel,bio.rgb*(.6+.8*lum),.6*bio.a);
   land=mix(land,vec3(.52,.47,.42)*(.7+.6*lum),smoothstep(.28,.6,hoehe)*.5);
   land=mix(land,vec3(.95,.96,.98),smoothstep(.56,.82,hoehe+kalt*.22));
   land*=.95+.1*vn(uv*vec2(4096.,2048.)*1.7)*uFein+.04*(fbm(uv*vec2(700.,350.))-.5);
   float tiefe=clamp((.5-h)/.4,0.,1.);
   vec3 w=mix(vec3(.17,.52,.58),vec3(.055,.29,.52),smoothstep(0.,.2,tiefe));w=mix(w,vec3(.028,.135,.33),smoothstep(.14,.58,tiefe));w=mix(w,vec3(.014,.065,.2),smoothstep(.55,1.,tiefe));
   w=mix(w,rel,.2);w+=vec3(.07,.13,.11)*(1.-smoothstep(0.,.09,tiefe))*.7;
   float lg=degrees(abs(lat));eis=smoothstep(0.,.3,(lg-(lat>0.?75.:63.))/10.+(fbm(uv*vec2(60.,30.))-.5)*.7);w=mix(w,vec3(.86,.9,.95)*(.9+.2*vn(uv*vec2(900.,450.))),eis*.92);
   alb=mix(land,w,wasser);
   alb=mix(alb,mix(vec3(dot(alb,vec3(.3,.59,.11))),alb,.5)*.92,uThema);
  }
  if(uRoh>.5){col=alb;}
  else{
   float bump=uBump*mix(1.,.22,wasser);vec3 nb=normalize(U-bump*(hE*E+hN*N));float dif=max(dot(nb,S),0.);
   float licht=uLichtart<.5?.05+1.08*pow(dif,.78):clamp(.2+.98*dif/.77,0.,1.5);licht=mix(licht,.6+.5*dif,still*step(uLichtart,.5));
   float wk=0.;
   if(uWolken>.01&&still<.5){vec2 cu=vec2(uv.x+uZeit,uv.y);float c=texture2D(tWol,cu).r*.72+texture2D(tWol,vec2(cu.x*3.+.37-uZeit*.6,abs(fract(uv.y*1.5+.25)*2.-1.))).r*.28;wk=smoothstep(.5,.82,c)*uWolken;
    vec2 sv=vec2(dot(S,E),-dot(S,N))*.0045;float cs=texture2D(tWol,cu+sv).r*.72+.14;alb*=1.-.36*smoothstep(.5,.8,cs)*uWolken*(1.-wk);}
   vec3 V=uMode<.5?uBlick:U;vec2 wu=uv*vec2(2.,1.);vec3 nw=normalize(U+(E*(fbm(wu*700.)-.47)+N*(fbm(wu*700.+31.)-.47))*.03+(E*(vn(wu*4200.)-.5)+N*(vn(wu*4200.+57.)-.5))*.06*uFein);
   float nh=max(dot(nw,normalize(S+V)),0.);float sp=(pow(nh,240.)*.95+pow(nh,34.)*.15)*wasser*(1.-eis)*(1.-wk)*tag*(1.-still);
   vec3 c=alb*licht*tag+alb*vec3(.05,.07,.12)*(1.-tag);c+=vec3(1.,.96,.86)*sp;
   float daem=exp(-pow((nS-.03)/.11,2.))*step(uLichtart,.5)*(1.-still);
   if(still<.5){float nl=texture2D(tNac,uv).r;c+=vec3(1.,.76,.42)*nl*(1.-tag)*(1.-wasser*.85)*(1.-wk*.8)*1.7;}
   c=mix(c,c*vec3(1.22,.86,.62)+vec3(.04,.015,0.),daem*.5);
   vec3 wc=vec3(1.)*(.08+.96*pow(max(nS+.12,0.),.55))*tag+vec3(.06,.075,.11)*(1.-tag);if(uLichtart>.5)wc=vec3(.97)*tag+vec3(.06,.075,.11)*(1.-tag);wc=mix(wc,wc*vec3(1.2,.8,.62),daem*.6);
   c=mix(c,wc,wk*.84);
   if(uMode<.5){float tw=smoothstep(-.3,.3,nS);vec3 at=mix(vec3(.28,.52,1.),vec3(1.,.55,.3),daem*.7)*(.1+.9*mix(tw,1.,still));c*=1.-.3*pow(1.-z,1.6);c=mix(c,at,pow(1.-z,2.8)*.78);}
   col=c;
  }
 }
 else if(uRoh<.5){
  if(uMode<.5){float rl=sqrt(rr);vec2 nd=q/rl;float nS=dot(nd.x*uOst+nd.y*uNord,uSonne);float still=max(uThema,uPlain);float tg=mix(smoothstep(-.5,.35,nS),1.,still*.7);float t=rl-1.;
   float halo=exp(-t*46.)*.9+exp(-t*12.)*.3+exp(-t*3.4)*.08;vec3 hc=mix(vec3(.2,.45,1.),vec3(.6,.8,1.),exp(-t*70.));hc=mix(hc,vec3(1.,.5,.25),exp(-pow(nS/.22,2.))*.45*(1.-still));
   col=raum*(1.-min(1.,halo*tg))+hc*halo*(.06+.94*tg);}
  else if(uMode>1.5){
   if(rS<1.075){float a=atan(dS.x,dS.y),t=(rS-1.)/.075;float n=fbm(vec2(a*46.,t*3.5+a*2.));vec3 ice=mix(vec3(.95,.97,1.),vec3(.5,.64,.8),clamp(smoothstep(.25,1.,t)*.85+(n-.5)*.5,0.,1.));
    ice*=mix(.62,1.,smoothstep(0.,.1,t))*(.86+.3*smoothstep(.05,.3,t)*(1.-smoothstep(.45,1.,t)));vec2 ld=normalize(vec2(-.6,-.8));ice*=.82+.26*dot(normalize(dS),ld);
    float tg=uNacht>.5?mix(.42,1.,1.-smoothstep(.42,1.15,length(p-uSonneP)/uR)):1.;col=ice*tg;}
   else{float t=rS-1.075;vec2 sd=(dS+vec2(-.03,-.045)*uR)/uR;float sch=smoothstep(1.2,1.02,length(sd));col=raum*(1.-.75*sch)+vec3(.2,.4,.75)*exp(-t*16.)*.3;}
  }
 }
 col+=(h1(p+.5)-.5)/170.;gl_FragColor=vec4(col,1.);}`;
let GL=null, GLZ=0, GLW=0, GLH=0, GLD=1;
function glAn(){ return !!(GL&&GL.ok); }
function glStart(){
  GL=null; if(/[?&]canvas/.test(location.search)) return; const m=$('.qwk-map',wrap); if(!m) return;
  const c=document.createElement('canvas'); c.className='qwk-erde'; c.setAttribute('aria-hidden','true');
  let g=null; try{ g=c.getContext('webgl',{alpha:false,antialias:false,depth:false,stencil:false,powerPreference:'high-performance',preserveDrawingBuffer:!!window.QW_STANDBILD}); }catch(e){}
  if(!g) return; const hp=g.getShaderPrecisionFormat(g.FRAGMENT_SHADER,g.HIGH_FLOAT); if(!hp||!hp.precision) return;
  const sh=(t,s)=>{ const o=g.createShader(t); g.shaderSource(o,s); g.compileShader(o); if(!g.getShaderParameter(o,g.COMPILE_STATUS)){ console.warn('Weltkarte: Shader',g.getShaderInfoLog(o)); return null; } return o; };
  const vs=sh(g.VERTEX_SHADER,GLV), fs=sh(g.FRAGMENT_SHADER,GLF); if(!vs||!fs) return;
  const pr=g.createProgram(); g.attachShader(pr,vs); g.attachShader(pr,fs); g.linkProgram(pr); if(!g.getProgramParameter(pr,g.LINK_STATUS)){ console.warn('Weltkarte: Programm',g.getProgramInfoLog(pr)); return; }
  g.useProgram(pr); const b=g.createBuffer(); g.bindBuffer(g.ARRAY_BUFFER,b); g.bufferData(g.ARRAY_BUFFER,new Float32Array([-1,-1,3,-1,-1,3]),g.STATIC_DRAW); const al=g.getAttribLocation(pr,'a'); g.enableVertexAttribArray(al); g.vertexAttribPointer(al,2,g.FLOAT,false,0,0);
  const U={}; const n=g.getProgramParameter(pr,g.ACTIVE_UNIFORMS); for(let i=0;i<n;i++){ const u=g.getActiveUniform(pr,i); U[u.name]=g.getUniformLocation(pr,u.name); }
  const T={}; const tex=(name,unit,src,o={})=>{ const t=T[name]||(T[name]=g.createTexture()); g.activeTexture(g.TEXTURE0+unit); g.bindTexture(g.TEXTURE_2D,t); g.pixelStorei(g.UNPACK_PREMULTIPLY_ALPHA_WEBGL,false); g.pixelStorei(g.UNPACK_FLIP_Y_WEBGL,false);
    if(src&&src.d) g.texImage2D(g.TEXTURE_2D,0,g.RGBA,src.w,src.h,0,g.RGBA,g.UNSIGNED_BYTE,src.d); else g.texImage2D(g.TEXTURE_2D,0,g.RGBA,g.RGBA,g.UNSIGNED_BYTE,src);
    g.texParameteri(g.TEXTURE_2D,g.TEXTURE_MIN_FILTER,g.LINEAR); g.texParameteri(g.TEXTURE_2D,g.TEXTURE_MAG_FILTER,g.LINEAR); g.texParameteri(g.TEXTURE_2D,g.TEXTURE_WRAP_S,o.rs?g.REPEAT:g.CLAMP_TO_EDGE); g.texParameteri(g.TEXTURE_2D,g.TEXTURE_WRAP_T,o.rt?g.REPEAT:g.CLAMP_TO_EDGE); g.uniform1i(U[name],unit); };
  const leer={d:new Uint8Array([0,0,0,255]),w:1,h:1}; ['tRel','tRelK','tHoe','tBio','tNac','tWol'].forEach((k,i)=>tex(k,i,leer));
  GL={g,c,U,tex,ok:true,bereit:false,relB:4096}; m.insertBefore(c,m.firstChild);
  c.addEventListener('webglcontextlost',e=>{ e.preventDefault(); if(GL&&GL.c===c){ GL.ok=false; c.remove(); RKEY=''; zeichne(); } });
  const bild=id=>new Promise((res,rej)=>{ const el=document.getElementById(id); if(!el) return rej(new Error(id)); const im=new Image(); im.onload=()=>res(im); im.onerror=rej; im.src='data:image/jpeg;base64,'+el.textContent.trim(); });
  const me=GL, mx=g.getParameter(g.MAX_TEXTURE_SIZE), sparsam=Math.min(screen.width||9999,screen.height||9999)<600||(navigator.deviceMemory||8)<4;
  const klein=(im,w)=>{ const k=document.createElement('canvas'); k.width=w; k.height=w/2; k.getContext('2d').drawImage(im,0,0,w,w/2); return k; };
  Promise.all([bild('weltrelief'),bild('welthoehe')]).then(([rel,hoe])=>{ if(GL!==me||!me.ok) return; const zielB=Math.min(rel.width,mx,sparsam?2048:4096); me.relB=zielB;
    tex('tRel',0,zielB<rel.width?klein(rel,zielB):rel,{rs:1}); tex('tRelK',1,klein(rel,1024),{rs:1}); tex('tHoe',2,hoe,{rs:1}); tex('tBio',3,glBiome()); me.bereit=true; zeichne();
    setTimeout(()=>{ if(GL!==me||!me.ok) return; tex('tNac',4,glNacht(),{rs:1}); zeichne(); setTimeout(()=>{ if(GL!==me||!me.ok) return; tex('tWol',5,glWolken(),{rs:1,rt:1}); me.wolken=true; zeichne(); },30); },30);
  }).catch(e=>{ console.warn('Weltkarte: Texturen',e); });
}
/* 2°-Raster der Vegetationszonen als kleine Farbtextur (Ränder aufgefüllt, damit Küsten nicht ausfransen) */
function glBiome(){ const w=180,h=90,d=new Uint8Array(w*h*4), ok=new Uint8Array(w*h);
  DAT.raster.forEach(r=>{ const f=BIOF[r[4]]; if(!f) return; const x=Math.round((r[0]+179)/2), y=Math.round((89-r[1])/2); if(x<0||x>=w||y<0||y>=h) return; const i=y*w+x; d[i*4]=f[0]; d[i*4+1]=f[1]; d[i*4+2]=f[2]; d[i*4+3]=255; ok[i]=1; });
  for(let lauf=0;lauf<4;lauf++){ const neu=[]; for(let y=0;y<h;y++) for(let x=0;x<w;x++){ const i=y*w+x; if(ok[i]) continue; let r=0,g=0,b=0,n=0; for(const [dx,dy] of [[1,0],[-1,0],[0,1],[0,-1]]){ const xx=(x+dx+w)%w, yy=y+dy; if(yy<0||yy>=h) continue; const j=yy*w+xx; if(ok[j]){ r+=d[j*4]; g+=d[j*4+1]; b+=d[j*4+2]; n++; } } if(n) neu.push([i,r/n,g/n,b/n]); }
    neu.forEach(([i,r,g,b])=>{ d[i*4]=r; d[i*4+1]=g; d[i*4+2]=b; d[i*4+3]=lauf<1?255:0; ok[i]=1; }); }
  return {d,w,h}; }
/* Stadtlichter aus den Städten (Größe nach Einwohnern) mit verstreuten Siedlungspunkten im Umland */
function glNacht(){ const w=1024,h=512,c=document.createElement('canvas'); c.width=w; c.height=h; const x=c.getContext('2d'); x.fillStyle='#000'; x.fillRect(0,0,w,h); x.globalCompositeOperation='lighter';
  let s=11; const rnd=()=>(s=(s*16807)%2147483647)/2147483647;
  DAT.staedte.forEach(([n,lo,la,p])=>{ const px=(lo+180)/360*w, py=(90-la)/180*h, k=1/Math.max(.35,Math.cos(la*R2)), gr=Math.sqrt(Math.max(p,.05));
    const punkt=(ax,ay,rad,hell)=>{ const g=x.createRadialGradient(ax,ay,0,ax,ay,rad); g.addColorStop(0,`rgba(255,255,255,${hell})`); g.addColorStop(1,'rgba(255,255,255,0)'); x.fillStyle=g; x.save(); x.translate(ax,ay); x.scale(k,1); x.translate(-ax,-ay); x.beginPath(); x.arc(ax,ay,rad,0,7); x.fill(); x.restore(); };
    punkt(px,py,1.1+gr*.55,Math.min(1,.5+gr*.14)); const m=Math.round(3+gr*5); for(let i=0;i<m;i++){ const a=rnd()*6.283, di=(1.5+rnd()*rnd()*(5+gr*3.2)); punkt(px+Math.cos(a)*di*k,py+Math.sin(a)*di,.7+rnd()*.6,.16+rnd()*.3); } });
  return c; }
/* Wolken: gebackenes Rauschen mit Wirbeln, in Ost-West-Richtung nahtlos; Bänder an Äquator und in den Westwindzonen */
function glWolken(){ const w=1024,h=512,d=new Uint8Array(w*h*4);
  const hs=(i,j,k)=>{ let n=(i*374761393+j*668265263+k*1274126177)|0; n=(n^(n>>>13))*1274126177; return ((n^(n>>>16))>>>0)/4294967295; };
  const n3=(x,y,z)=>{ const xi=Math.floor(x),yi=Math.floor(y),zi=Math.floor(z); let u=x-xi,v=y-yi,t=z-zi; u=u*u*(3-2*u); v=v*v*(3-2*v); t=t*t*(3-2*t);
    const a=hs(xi,yi,zi)+(hs(xi+1,yi,zi)-hs(xi,yi,zi))*u, b=hs(xi,yi+1,zi)+(hs(xi+1,yi+1,zi)-hs(xi,yi+1,zi))*u, c=hs(xi,yi,zi+1)+(hs(xi+1,yi,zi+1)-hs(xi,yi,zi+1))*u, e=hs(xi,yi+1,zi+1)+(hs(xi+1,yi+1,zi+1)-hs(xi,yi+1,zi+1))*u;
    return (a+(b-a)*v)+((c+(e-c)*v)-(a+(b-a)*v))*t; };
  const f3=(x,y,z,o)=>{ let s=0,m=.5,f=1,n=0; for(let i=0;i<o;i++){ s+=m*n3(x*f+i*7.1,y*f-i*3.3,z*f+i*5.7); n+=m; f*=2.07; m*=.5; } return s/n; };
  for(let py=0;py<h;py++){ const lat=(.5-(py+.5)/h)*Math.PI, cl=Math.cos(lat), sl=Math.sin(lat), ld=Math.abs(lat)/R2;
    const zone=.52+.2*Math.exp(-Math.pow(ld/9,2))+.2*Math.exp(-Math.pow((ld-52)/15,2))-.17*Math.exp(-Math.pow((ld-25)/9,2))+.08*Math.exp(-Math.pow((ld-80)/12,2));
    for(let px=0;px<w;px++){ const lon=(px+.5)/w*2*Math.PI, x0=cl*Math.cos(lon), y0=cl*Math.sin(lon), z0=sl;
      const wx=f3(x0*2.2+5,y0*2.2,z0*2.2,2)-.5, wy=f3(x0*2.2,y0*2.2+9,z0*2.2,2)-.5; const v=f3(x0*3.4+wx*1.5,y0*3.4+wy*1.5,z0*4.6+wx,5)*.8+f3(x0*13+wy*2,y0*13,z0*15,3)*.2;
      const o=(py*w+px)*4, g=Math.max(0,Math.min(255,(v+(zone-.5)*.75)*255)); d[o]=d[o+1]=d[o+2]=g; d[o+3]=255; } }
  return {d,w,h}; }
function glZeichne(mitRelief,thema){
  if(!glAn()) return false; const g=GL.g, U=GL.U, c=GL.c;
  const fl=W*H, dpr=Math.min(DPR,fl*DPR*DPR>2.6e6?Math.max(1,Math.sqrt(2.6e6/fl)):DPR), bw=Math.max(1,Math.round(W*dpr)), bh=Math.max(1,Math.round(H*dpr));
  if(c.width!==bw||c.height!==bh){ c.width=bw; c.height=bh; } g.viewport(0,0,bw,bh);
  const mode=S.modus==='globus'?0:S.modus==='scheibe'?2:1, l=S.lam*R2, p=S.phi*R2, cp=Math.cos(p), sp=Math.sin(p), cl=Math.cos(l), sl=Math.sin(l);
  const C=[cp*cl,cp*sl,sp], Ex=[-sl,cl,0], Ny=[-sp*cl,-sp*sl,cp]; let So;
  if(S.ov.nacht){ const [a,b]=sonne(); So=[Math.cos(b*R2)*Math.cos(a*R2),Math.cos(b*R2)*Math.sin(a*R2),Math.sin(b*R2)]; }
  else { const L=[-.47,.33,.82]; So=[0,1,2].map(i=>L[0]*Ex[i]+L[1]*Ny[i]+L[2]*C[i]); }
  const R=mode===0?radius():rd(), k=kf(), pxTex=mode===0?(GL.relB/(2*Math.PI))/(R*dpr):mode===1?(GL.relB/360)/(k*dpr):(GL.relB/2)/(R*dpr*2);
  g.uniform2f(U.uGr,W,H); g.uniform1f(U.uDpr,bw/W); g.uniform1f(U.uMode,mode); g.uniform1f(U.uR,R); g.uniform1f(U.uLam,l); g.uniform1f(U.uPhi,p); g.uniform1f(U.uK,k); g.uniform2f(U.uPan,S.px,S.py);
  g.uniform3fv(U.uSonne,So); g.uniform3fv(U.uBlick,C); g.uniform3fv(U.uOst,Ex); g.uniform3fv(U.uNord,Ny);
  let sx=0, sy=0; if(mode===2&&S.ov.nacht){ const [a,b]=sonne(), q=proj(a,b); sx=q[0]; sy=q[1]; } g.uniform2f(U.uSonneP,sx,sy);
  g.uniform1f(U.uZeit,GLZ); g.uniform1f(U.uWolken,S.ov.wolken&&GL.wolken?Math.max(.25,Math.min(1,1.25-S.zoom/9)):0); g.uniform1f(U.uThema,thema?1:0); g.uniform1f(U.uPlain,mitRelief?0:1); g.uniform1f(U.uNacht,S.ov.nacht?1:0); g.uniform1f(U.uRoh,0);
  g.uniform1f(U.uBereit,GL.bereit?1:0); g.uniform1f(U.uFein,Math.max(0,Math.min(1,(S.zoom-1.5)/4))); g.uniform1f(U.uUnscharf,Math.max(0,Math.min(1,Math.log2(Math.max(1,pxTex))/2))); g.uniform1f(U.uLichtart,mode===0||(mode===1&&S.ov.nacht)?0:1); g.uniform1f(U.uBump,mode===0?11:9);
  g.drawArrays(g.TRIANGLES,0,3); GLW=bw; GLH=bh; GLD=dpr; return true; }
/* Unbeleuchtetes Naturbild der Scheibe als Bild (für die 3D-Scheibe) */
function glScheibenbild(ts){ if(!glAn()||!GL.bereit) return null; const g=GL.g, U=GL.U, c=GL.c, mx=g.getParameter(g.MAX_RENDERBUFFER_SIZE)||ts; ts=Math.min(ts,mx); c.width=c.height=ts; g.viewport(0,0,ts,ts);
  g.uniform2f(U.uGr,ts,ts); g.uniform1f(U.uDpr,1); g.uniform1f(U.uMode,2); g.uniform1f(U.uR,ts/2); g.uniform1f(U.uLam,0); g.uniform1f(U.uPhi,0); g.uniform2f(U.uPan,0,0); g.uniform1f(U.uRoh,1); g.uniform1f(U.uPlain,0); g.uniform1f(U.uThema,0); g.uniform1f(U.uBereit,1); g.uniform1f(U.uFein,0); g.uniform1f(U.uUnscharf,0); g.uniform1f(U.uWolken,0);
  g.drawArrays(g.TRIANGLES,0,3); const k=document.createElement('canvas'); k.width=k.height=ts; k.getContext('2d').drawImage(c,0,0); zeichne(); return k; }

/* ---------- Zeichnen ---------- */
let sterne=null, BOX=[]; const SPERR=typeof CanvasRenderingContext2D!=='undefined'&&'letterSpacing' in CanvasRenderingContext2D.prototype;
function zeichne(fein){
  if(!ctx) return; BOX=[]; ctx.setTransform(DPR,0,0,DPR,0,0); ctx.clearRect(0,0,W,H);
  const G3=glZeichne(S.grund==='relief'||(S.unterlage&&!GRUND[S.grund].r),S.grund!=='relief');
  if(!G3){ const g0=ctx.createRadialGradient(W/2,H/2,0,W/2,H/2,Math.max(W,H)*0.8); g0.addColorStop(0,'#0e1a30'); g0.addColorStop(1,'#04070e'); ctx.fillStyle=g0; ctx.fillRect(0,0,W,H);
  if(!sterne){ sterne=[]; let s=7; const r=()=>(s=(s*16807)%2147483647)/2147483647; for(let i=0;i<260;i++) sterne.push([r(),r(),r()*1.2+.2,r()]); }
  sterne.forEach(([x,y,z,a])=>{ ctx.fillStyle=`rgba(200,220,255,${a*.6})`; ctx.fillRect(x*W,y*H,z,z); }); }
  const r=radius(), glob=S.modus==='globus', G=GRUND[S.grund], rast=G.r, mitRelief=S.grund==='relief'||(S.unterlage&&!rast);
  if(glob){ if(!G3){ const at=ctx.createRadialGradient(W/2,H/2,r*0.92,W/2,H/2,r*1.18); at.addColorStop(0,'rgba(110,190,255,.62)'); at.addColorStop(.18,'rgba(80,160,255,.3)'); at.addColorStop(.5,'rgba(60,130,255,.1)'); at.addColorStop(1,'rgba(40,100,255,0)'); ctx.fillStyle=at; ctx.beginPath(); ctx.arc(W/2,H/2,r*1.18,0,7); ctx.fill();
    const hof=ctx.createRadialGradient(W/2-r*.25,H/2-r*.28,r*.9,W/2,H/2,r*1.6); hof.addColorStop(0,'rgba(90,160,255,.13)'); hof.addColorStop(1,'rgba(40,100,255,0)'); ctx.fillStyle=hof; ctx.beginPath(); ctx.arc(W/2,H/2,r*1.6,0,7); ctx.fill();
    const oz=ctx.createRadialGradient(W/2-r*.35,H/2-r*.4,r*.1,W/2,H/2,r); oz.addColorStop(0,'#1d4f86'); oz.addColorStop(.6,'#0c2c52'); oz.addColorStop(1,'#071a33'); ctx.fillStyle=oz; ctx.beginPath(); ctx.arc(W/2,H/2,r,0,7); ctx.fill(); }
    ctx.save(); ctx.beginPath(); ctx.arc(W/2,H/2,r,0,7); ctx.clip(); }
  else if(S.modus==='scheibe'){ const R0=rd(), cx=W/2+S.px, cy=H/2+S.py; if(!G3){ const kg=ctx.createRadialGradient(cx,cy,R0*0.98,cx,cy,R0*1.35); kg.addColorStop(0,'rgba(120,180,255,.35)'); kg.addColorStop(1,'rgba(60,120,255,0)'); ctx.fillStyle=kg; ctx.beginPath(); ctx.arc(cx,cy,R0*1.35,0,7); ctx.fill();
    const eg=ctx.createRadialGradient(cx,cy,R0,cx,cy,R0*1.07); eg.addColorStop(0,'#f4f8ff'); eg.addColorStop(.6,'#c8d6e8'); eg.addColorStop(1,'#8aa0bc'); ctx.fillStyle=eg; ctx.beginPath(); ctx.arc(cx,cy,R0*1.07,0,7); ctx.fill();
    ctx.fillStyle='#0a2240'; ctx.beginPath(); ctx.arc(cx,cy,R0,0,7); ctx.fill(); } ctx.save(); ctx.beginPath(); ctx.arc(cx,cy,R0*1.07,0,7); ctx.clip(); }
  else if(!G3){ ctx.fillStyle='#0a2240'; const a=proj(-180,90),b=proj(180,-90); ctx.fillRect(0,a[1],W,b[1]-a[1]); }
  if(mitRelief&&!G3){ textur(); const rc=relief(fein!==false&&!S.bewegt); if(rc){ ctx.imageSmoothingEnabled=true; ctx.drawImage(rc,0,0,W,H); if(!fein&&!S.bewegt){} } }
  // Gradnetz
  ctx.strokeStyle=G3?'rgba(210,230,255,.07)':mitRelief?'rgba(255,255,255,.08)':'rgba(140,190,255,.10)'; ctx.lineWidth=.7;
  for(let la=-60;la<=60;la+=30){ ctx.beginPath(); let st=true; for(let lo=-180;lo<=180;lo+=4){ const q=proj(lo,la); if(q[2]<0){st=true;continue;} st?ctx.moveTo(q[0],q[1]):ctx.lineTo(q[0],q[1]); st=false; } ctx.stroke(); }
  for(let lo=-180;lo<180;lo+=30){ ctx.beginPath(); let st=true; for(let la=-88;la<=88;la+=4){ const q=proj(lo,la); if(q[2]<0){st=true;continue;} st?ctx.moveTo(q[0],q[1]):ctx.lineTo(q[0],q[1]); st=false; } ctx.stroke(); }
  // Länderflächen
  if(S.grund!=='relief'){ const alpha=mitRelief?0.62:1;
    DAT.laender.forEach(c=>{ const f=rast?null:farbe(c.i); if(mitRelief&&!f) return; ctx.beginPath(); let ok=false; c.p.forEach(rg=>{ if(pfad(rg)) ok=true; }); if(!ok) return; ctx.globalAlpha=alpha; ctx.fillStyle=f||(rast?'#22303a':'#1e2c3a'); ctx.fill(); ctx.globalAlpha=1; }); }
  if(rast){ const half=1.02, tab=rast===2?KLIMA:rast===3?BODEN:VEGN; ctx.save(); ctx.beginPath(); DAT.laender.forEach(c=>c.p.forEach(rg=>pfad(rg))); ctx.clip();
    DAT.raster.forEach(g=>{ const k=g[rast]; const q=proj(g[0],g[1]); if(q[2]<0.05) return; const a=proj(g[0]-half,g[1]+half),b=proj(g[0]+half,g[1]+half),c2=proj(g[0]+half,g[1]-half),d=proj(g[0]-half,g[1]-half);
      if(!glob && Math.abs(a[0]-b[0])>W/2) return; ctx.fillStyle=tab[k][1]; ctx.globalAlpha=.86; ctx.beginPath(); ctx.moveTo(a[0],a[1]); ctx.lineTo(b[0],b[1]); ctx.lineTo(c2[0],c2[1]); ctx.lineTo(d[0],d[1]); ctx.closePath(); ctx.fill(); ctx.globalAlpha=1; }); ctx.restore(); }
  if(G.de&&DAT.bl){ DAT.bl.forEach(b=>{ const v=deWert(b.i,S.grund); ctx.beginPath(); let ok=false; b.p.forEach(rg=>{ if(pfad(rg)) ok=true; }); if(!ok) return; ctx.globalAlpha=.88; ctx.fillStyle=v==null?'#333':ramp(G.p,G.s(v)); ctx.fill(); ctx.globalAlpha=1; ctx.strokeStyle=S.bl===b.i?'#fff':'rgba(255,255,255,.7)'; ctx.lineWidth=S.bl===b.i?2.6:.9; ctx.stroke(); }); }
  // Gewässer
  if(S.ov.fluesse){ ctx.fillStyle=G3&&mitRelief?(S.grund==='relief'?'rgba(24,82,132,.94)':'rgba(40,74,104,.9)'):mitRelief?'rgba(30,80,140,.9)':'#0c2c52'; DAT.seen.forEach(([n,rg])=>{ ctx.beginPath(); if(pfad(rg)) ctx.fill(); });
    const zs=zstufe(); ctx.strokeStyle=G3&&mitRelief?'rgba(96,160,214,.6)':mitRelief?'rgba(120,185,250,.62)':'rgba(90,170,255,.5)'; ctx.lineCap='round'; DAT.fluesse.forEach(([sr,n,l])=>{ if(sr>zs+3) return; ctx.lineWidth=Math.max(.5,2-sr*0.18)*Math.min(1.6,Math.sqrt(S.zoom)); ctx.beginPath(); if(pfad(l,true)) ctx.stroke(); }); }
  if(S.pflanze){ const P=PFL[S.pflanze]; ctx.fillStyle='rgba(120,255,170,.55)'; DAT.raster.forEach(g=>{ if(g[5]||!inBereich(P,g)) return; const q=proj(g[0],g[1]); if(q[2]<0.05) return; ctx.beginPath(); ctx.arc(q[0],q[1],Math.max(1.4,radius()/260*S.zoom),0,7); ctx.fill(); }); }
  // Grenzen
  if(S.ov.grenzen){ const gw=Math.min(1.7,.6+S.zoom/9); ctx.lineJoin='round';
    DAT.laender.forEach(c=>{ ctx.beginPath(); let ok=false; c.p.forEach(rg=>{ if(pfad(rg)) ok=true; }); if(!ok) return;
      if(mitRelief){ ctx.strokeStyle=G3?'rgba(8,16,28,.3)':'rgba(8,16,28,.42)'; ctx.lineWidth=gw*2.3; ctx.stroke(); ctx.strokeStyle=G3?'rgba(255,250,235,.5)':'rgba(255,255,255,.58)'; ctx.lineWidth=gw*.8; ctx.stroke(); }
      else { ctx.strokeStyle='rgba(225,238,255,.34)'; ctx.lineWidth=gw*.75; ctx.stroke(); } }); }
  if(S.sel){ const c=DAT.idx[S.sel]; ctx.beginPath(); c.p.forEach(rg=>pfad(rg)); ctx.strokeStyle='#fff'; ctx.lineWidth=2.2; ctx.shadowColor='rgba(120,200,255,.9)'; ctx.shadowBlur=12; ctx.stroke(); ctx.shadowBlur=0; }
  if(S.ov.nacht) nacht(G3);
  // Geschichte
  if(S.ov.wander) WANDER.forEach((w,wi)=>{ if(S.epoche&&w[2]!==S.epoche) return; const sel=S.hist&&S.hist[0]==='w'&&S.hist[1]===wi; w[6].forEach(p=>pfeil(p,w[3],sel)); });
  if(S.ov.kriege) KRIEGE.forEach((k,ki)=>{ if(S.epoche&&epocheVon(k[1])!==S.epoche) return; const q=proj(k[3],k[4]); if(q[2]<0.1) return; const sel=S.hist&&S.hist[0]==='k'&&S.hist[1]===ki; schwert(q[0],q[1],sel); if(S.zoom>1.5||sel) text(k[0],q[0]+9,q[1]+4,sel?13:11,'#ffd0c8'); });
  const jE=j=>j<500?(j<-1000?'vor':'antike'):j<1500?'mittel':j<1900?'neu':j<2000?'20':'heute';
  if(S.ov.goethe){ ctx.strokeStyle='rgba(255,150,120,.9)'; ctx.lineWidth=2*Math.min(1.5,Math.sqrt(S.zoom)); ctx.setLineDash([5,4]); ctx.beginPath(); let st=true; GOETHE.forEach(g=>{ const q=proj(g[3],g[4]); if(q[2]<0){st=true;return;} st?ctx.moveTo(q[0],q[1]):ctx.lineTo(q[0],q[1]); st=false; }); ctx.stroke(); ctx.setLineDash([]);
    const ges={}; GOETHE.forEach((g,gi)=>{ if(ges[g[0]]) return; ges[g[0]]=1; const q=proj(g[3],g[4]); if(q[2]<0.1) return; const jahre=GOETHE.filter(x=>x[0]===g[0]).reduce((a,x)=>a+Math.max(0.1,x[2]-x[1]),0); const R=3+Math.sqrt(jahre)*1.6; const sel=S.hist&&S.hist[0]==='g'&&GOETHE[S.hist[1]][0]===g[0];
      ctx.fillStyle=sel?'#ffd8c8':'rgba(255,140,110,.9)'; ctx.strokeStyle='#3a2a10'; ctx.lineWidth=1.2; ctx.beginPath(); ctx.arc(q[0],q[1],R,0,7); ctx.fill(); ctx.stroke(); if(S.zoom>2||sel||jahre>10) text(g[0],q[0]+R+3,q[1]+4,10.5,'#ffc8b0'); }); }
  if(S.ov.geld) GELD.forEach((g,gi)=>{ if(S.epoche&&jE(g[1])!==S.epoche) return; const q=proj(g[3],g[4]); if(q[2]<0.1) return; const sel=S.hist&&S.hist[0]==='m'&&S.hist[1]===gi; const R=sel?8:6; const gg=ctx.createRadialGradient(q[0]-2,q[1]-2,1,q[0],q[1],R); gg.addColorStop(0,'#fff3b0'); gg.addColorStop(1,'#c8901a'); ctx.fillStyle=gg; ctx.strokeStyle='#5a3a08'; ctx.lineWidth=1.2; ctx.beginPath(); ctx.arc(q[0],q[1],R,0,7); ctx.fill(); ctx.stroke(); if(S.zoom>2.2||sel) text(`${g[1]<0?-g[1]+' v. Chr.':g[1]} ${g[0]}`,q[0]+R+3,q[1]+4,10.5,'#ffe8a0'); });
  if(S.ov.erf) ERF.forEach((e,ei)=>{ if(S.epoche&&jE(e[1])!==S.epoche) return; const q=proj(e[4],e[5]); if(q[2]<0.1) return; const sel=S.hist&&S.hist[0]==='e'&&S.hist[1]===ei; const R=sel?8:5.5; ctx.fillStyle=sel?'#ffffff':'#ffe14a'; ctx.shadowColor='#ffe14a'; ctx.shadowBlur=sel?16:8; ctx.beginPath(); ctx.arc(q[0],q[1],R,0,7); ctx.fill(); ctx.shadowBlur=0; ctx.fillStyle='#3a3000'; ctx.fillRect(q[0]-1.5,q[1]+R-2,3,3); if(S.zoom>2.2||sel) text(e[0],q[0]+R+3,q[1]+4,10.5,'#fff3a0'); });
  // Mengen-Overlays
  const blase=(lon,lat,rad,col)=>{ const q=proj(lon,lat); if(q[2]<0.12) return; const R=rad*Math.sqrt(S.zoom); const gg=ctx.createRadialGradient(q[0]-R*.3,q[1]-R*.3,R*.1,q[0],q[1],R); gg.addColorStop(0,col); gg.addColorStop(1,col+'99'); ctx.fillStyle=gg; ctx.beginPath(); ctx.arc(q[0],q[1],R,0,7); ctx.fill(); ctx.strokeStyle='rgba(0,0,0,.45)'; ctx.lineWidth=1; ctx.stroke(); };
  Object.entries(GETREIDE).forEach(([k,G2],ix)=>{ if(!S.ov[k]) return; const mx=Math.max(...Object.values(G2.d)); Object.entries(G2.d).forEach(([i,v])=>{ const c=DAT.idx[i]; if(!c) return; const off=(ix-2)*1.6; blase(c.mitte[0]+off,c.mitte[1]+off*.4,4+16*Math.sqrt(v/mx),G2.c); }); });
  Object.entries(ROH).forEach(([k,G2],ix)=>{ if(!S.ov[k]) return; const mx=Math.max(...Object.values(G2.d).filter(v=>v<20000)); Object.entries(G2.d).forEach(([i,v])=>{ const c=DAT.idx[i]; if(!c) return; raute(c.mitte[0]-1.5+(ix%3)*1.2,c.mitte[1]-1.2,4+18*Math.sqrt(Math.min(v,mx)/mx),G2.c); }); });
  if(S.ov.pfl) Object.entries(PFL).forEach(([id,P])=>{ const q=proj(P[0][0],P[0][1]); if(q[2]<0.1) return; pin(q[0],q[1],'#ff6a8a'); if(S.zoom>1.3||S.pflanze===id) text(pname(id),q[0]+7,q[1]-6,11,'#ffd0dc'); });
  if(S.ov.rez) REZ.forEach(([id,n,lo,la])=>{ const q=proj(lo,la); if(q[2]<0.1) return; pin(q[0],q[1],'#c79aff'); if(S.zoom>1.8) text(n,q[0]+7,q[1]-6,11,'#e8d8ff'); });
  if(S.ov.aut) AUT.forEach(([id,n,lo,la])=>{ const q=proj(lo,la); if(q[2]<0.1) return; pin(q[0],q[1],'#6ac8ff'); if(S.zoom>1.8) text(n,q[0]+7,q[1]-6,11,'#d0ecff'); });
  if(G.de&&DAT.bl&&S.zoom>3.5){ const big=S.zoom>6; DAT.bl.slice().reverse().forEach(b=>{ const q=proj(b.lp[0],b.lp[1]); if(q[2]<0.2) return; const v=deWert(b.i,S.grund); const kurz=['BE','HB','HH'].includes(b.i); text(big&&!kurz?b.n:b.i,q[0],q[1]-2,big?11.5:10.5,'#ffffff',true,'700'); if(v!=null) text(fmt(v,['de_hz','de_ek','de_bip'].includes(S.grund)?0:1),q[0],q[1]+11,10.5,'#ffe8c0',true,'600'); }); }
  // Beschriftung: Landschaften, Gipfel, Länder, Städte
  const zs=zstufe();
  const rand=q=>glob?Math.max(0,Math.min(1,(q[2]-.2)/.3)):1; // zum Kugelrand hin ausblenden statt stauchen
  if(S.ov.namen&&mitRelief){ TLS='2.4px'; MEERE.forEach(([n,lo,la,rg])=>{ if(rg>zs-.6) return; const q=proj(lo,la); if(q[2]<0.3) return; TXA=rand(q)*.88; text(n,q[0],q[1],(rg<1?14.5:rg<2?12.5:11.5)-(W<520?1.8:0),'#c4dcf0',true,'italic 400','meer'); }); TLS='0px'; TXA=1; }
  if(S.ov.landschaft){ TLS='1px'; DAT.regionen.forEach(([n,k,lo,la,sr])=>{ if(sr>zs+0.5) return; const q=proj(lo,la); if(q[2]<0.25) return; TXA=rand(q); text(n,q[0],q[1],11,k==='Range/mtn'?'#ecd9bd':k==='Desert'?'#f3dfae':'#d6e6c6',true,'italic 400','meer'); }); TLS='0px'; TXA=1; }
  if(S.ov.gipfel) DAT.gipfel.forEach(([n,lo,la,hm,sr])=>{ if(sr>zs+1) return; const q=proj(lo,la); if(q[2]<0.15) return; ctx.fillStyle='#fff'; ctx.beginPath(); ctx.moveTo(q[0],q[1]-5); ctx.lineTo(q[0]+4,q[1]+2); ctx.lineTo(q[0]-4,q[1]+2); ctx.closePath(); ctx.fill(); text(`${n} ${fmt(hm)} m`,q[0]+6,q[1]+3,10,'#ffffff'); });
  if(S.ov.namen) DAT.laender.slice().sort((a,b)=>a.lr-b.lr).forEach(c=>{ if(c.lr>zs||(G.de&&c.i==='DEU')) return; const q=proj(c.lp[0],c.lp[1]); if(q[2]<0.24) return; const gross=c.lr<3, mittel=c.lr<4.5; TLS=gross?'1.5px':mittel?'1px':'.6px'; TXA=rand(q); text(c.n,q[0],q[1],(gross?13.5:mittel?12:11)-(W<520?(gross?2:.6):0),gross?'#fbf7ea':'#efece0',true,gross?'700':'500','sc'); }); TLS='0px'; TXA=1;
  if(S.ov.staedte) DAT.staedte.forEach(([n,lo,la,p,mz,hs])=>{ if(mz>zs) return; const q=proj(lo,la); if(q[2]<0.22) return; const R=1.4+Math.sqrt(Math.max(p,.1))*0.7; if(!frei(q[0]-R,q[1]+R,R*2,R*2)) return; TXA=rand(q); const ok=text(n,q[0]+R+3,q[1]+3.5,p>5?11:10.2,'#f6ecd6',false,p>5?'700':'500'); if(!ok){ TXA=1; return; } BOX.push([q[0]-R,q[1]+R,R*2,R*2]); ctx.globalAlpha=TXA; ctx.fillStyle=hs?'#f3cf62':'#f6e7c2'; ctx.strokeStyle='rgba(20,16,8,.75)'; ctx.lineWidth=1; ctx.beginPath(); if(hs) ctx.rect(q[0]-R,q[1]-R,R*2,R*2); else ctx.arc(q[0],q[1],R,0,7); ctx.fill(); ctx.stroke(); ctx.globalAlpha=1; TXA=1; });
  if(S.ov.tiefen) TIEFEN.forEach(([n,lo,la,t])=>{ const q=proj(lo,la); if(q[2]<0.15) return; ctx.fillStyle='#7fe0ff'; ctx.strokeStyle='#02101e'; ctx.lineWidth=1.2; ctx.beginPath(); ctx.moveTo(q[0]-5,q[1]-4); ctx.lineTo(q[0]+5,q[1]-4); ctx.lineTo(q[0],q[1]+4); ctx.closePath(); ctx.fill(); ctx.stroke(); text(`${n} −${fmt(t)} m`,q[0]+7,q[1]+4,10.5,'#bff0ff'); });
  if(S.klick){ const q=proj(S.klick[0],S.klick[1]); if(q[2]>0){ ctx.strokeStyle='#fff'; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(q[0],q[1],6,0,7); ctx.stroke(); } }
  if(S.modus==='scheibe'){ ctx.restore(); const R0=rd(), cx=W/2+S.px, cy=H/2+S.py; if(S.zoom<2.5){ TLS='1.5px'; text('Eiswall (Antarktis)',cx,cy+R0*1.036+4,11.5,G3&&!S.ov.nacht?'#1c2c44':'#f2f6ff',true,'italic 400','meer'); TLS='0px'; text('Nordpol',cx,cy-6,10.5,'#ffffff',true,'700'); } if(!G3){ ctx.strokeStyle='rgba(180,210,255,.5)'; ctx.lineWidth=1.2; ctx.beginPath(); ctx.arc(cx,cy,R0*1.07,0,7); ctx.stroke(); } }
  if(glob){ ctx.restore(); if(!G3){ const sh=ctx.createRadialGradient(W/2-r*.35,H/2-r*.4,r*.2,W/2,H/2,r*1.02); sh.addColorStop(0,mitRelief?'rgba(255,255,255,.03)':'rgba(255,255,255,.09)'); sh.addColorStop(.7,'rgba(0,0,0,0)'); sh.addColorStop(1,mitRelief?'rgba(0,5,20,.2)':'rgba(0,5,20,.55)'); ctx.fillStyle=sh; ctx.beginPath(); ctx.arc(W/2,H/2,r,0,7); ctx.fill();
    const saum=ctx.createRadialGradient(W/2,H/2,r*.9,W/2,H/2,r); saum.addColorStop(0,'rgba(120,190,255,0)'); saum.addColorStop(.8,'rgba(120,190,255,.1)'); saum.addColorStop(1,'rgba(150,210,255,.42)'); ctx.fillStyle=saum; ctx.beginPath(); ctx.arc(W/2,H/2,r,0,7); ctx.fill();
    ctx.strokeStyle='rgba(170,220,255,.5)'; ctx.lineWidth=1; ctx.beginPath(); ctx.arc(W/2,H/2,r,0,7); ctx.stroke(); } }
  if(G3) S.bewegt=false; else if(mitRelief&&(S.bewegt||fein===false)){ clearTimeout(RTIMER); RTIMER=setTimeout(()=>{ S.bewegt=false; zeichne(true); },160); }
}
const SCHRIFT={std:'"Alegreya Sans","Segoe UI",system-ui,-apple-system,Roboto,sans-serif',sc:'"Alegreya Sans SC","Alegreya Sans","Segoe UI",system-ui,sans-serif',meer:'"Alegreya",Georgia,"Times New Roman",serif'};
let TXA=1, TLS='0px', SCHRIFT_DA=false;
function schriftLaden(){ if(SCHRIFT_DA||!document.fonts||!document.fonts.load) return; SCHRIFT_DA=true; Promise.all(['500 12px "Alegreya Sans"','700 12px "Alegreya Sans"','500 12px "Alegreya Sans SC"','700 12px "Alegreya Sans SC"','italic 400 12px "Alegreya"'].map(f=>document.fonts.load(f).catch(()=>0))).then(()=>{ if(wrap&&document.body.contains(wrap)) zeichne(); }); }
function text(t,x,y,s=11.5,col='#eef3fa',mitte,gew='500',fam){ s+=1.4; if(gew==='600') gew='500'; else if(gew==='italic 600'||gew==='italic 700') gew='italic 400'; ctx.font=`${gew} ${s}px ${SCHRIFT[fam||(gew.indexOf('italic')===0?'meer':'std')]}`; if(SPERR) ctx.letterSpacing=TLS; const w=ctx.measureText(t).width; if(mitte) x-=w/2;
  if(x<-w||x>W||y<0||y>H+10) return false; if(frei(x,y,w,s)===false) return false; BOX.push([x,y,w,s]);
  if(TXA<=0.02) return true; ctx.globalAlpha=TXA; ctx.lineJoin='round'; ctx.lineWidth=Math.max(3.6,s*.34); ctx.strokeStyle='rgba(6,14,26,.16)'; ctx.strokeText(t,x,y); ctx.lineWidth=Math.max(1.8,s*.17); ctx.strokeStyle='rgba(6,14,26,.58)'; ctx.strokeText(t,x,y); ctx.fillStyle=col; ctx.fillText(t,x,y); ctx.globalAlpha=1; if(SPERR&&TLS!=='0px'&&!mitte){} return true; }
function frei(x,y,w,s){ return !BOX.some(b=>x<b[0]+b[2]+3&&x+w+3>b[0]&&y-s<b[1]+2&&y+2>b[1]-b[3]); }
function pin(x,y,c){ ctx.fillStyle=c; ctx.strokeStyle='#0a0f1a'; ctx.lineWidth=1.5; ctx.beginPath(); ctx.arc(x,y,4.6,0,7); ctx.fill(); ctx.stroke(); ctx.fillStyle='rgba(255,255,255,.8)'; ctx.beginPath(); ctx.arc(x-1.2,y-1.2,1.4,0,7); ctx.fill(); }
function raute(lon,lat,R,c){ const q=proj(lon,lat); if(q[2]<0.12) return; R*=Math.sqrt(S.zoom)*.9; ctx.fillStyle=c+'cc'; ctx.strokeStyle='rgba(0,0,0,.55)'; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(q[0],q[1]-R); ctx.lineTo(q[0]+R,q[1]); ctx.lineTo(q[0],q[1]+R); ctx.lineTo(q[0]-R,q[1]); ctx.closePath(); ctx.fill(); ctx.stroke(); }
function schwert(x,y,sel){ const R=sel?11:8; const gg=ctx.createRadialGradient(x,y,0,x,y,R*2); gg.addColorStop(0,'rgba(255,60,40,.55)'); gg.addColorStop(1,'rgba(255,60,40,0)'); ctx.fillStyle=gg; ctx.beginPath(); ctx.arc(x,y,R*2,0,7); ctx.fill();
  ctx.strokeStyle='#ffe0d8'; ctx.lineWidth=sel?2.4:1.8; ctx.beginPath(); ctx.moveTo(x-R*.7,y-R*.7); ctx.lineTo(x+R*.7,y+R*.7); ctx.moveTo(x+R*.7,y-R*.7); ctx.lineTo(x-R*.7,y+R*.7); ctx.stroke(); ctx.fillStyle='#d8302a'; ctx.beginPath(); ctx.arc(x,y,2.6,0,7); ctx.fill(); }
function pfeil(p,col,sel){ const pts=[]; for(let i=0;i<p.length-1;i++){ const [a,b]=[p[i],p[i+1]]; let dl=b[0]-a[0]; if(dl>180) dl-=360; if(dl<-180) dl+=360; const n=Math.max(2,Math.ceil(Math.hypot(dl,b[1]-a[1])/3)); for(let k=0;k<n;k++){ const t=k/n; pts.push([a[0]+dl*t,a[1]+(b[1]-a[1])*t]); } } pts.push(p[p.length-1]);
  const P=pts.map(([a,b])=>proj(((a+540)%360)-180,b)); ctx.strokeStyle=col; ctx.globalAlpha=sel?1:(S.hist&&S.hist[0]==='w'?.3:.85); ctx.lineWidth=(sel?3.4:2.2)*Math.min(1.5,Math.sqrt(S.zoom)); ctx.lineCap='round'; ctx.setLineDash([8,6]); ctx.lineDashOffset=-(performance.now()/60)%14;
  ctx.beginPath(); let st=true, lx=null; P.forEach(q=>{ if(q[2]<0||(lx!==null&&Math.abs(q[0]-lx)>W/2)){ st=true; lx=q[0]; return; } st?ctx.moveTo(q[0],q[1]):ctx.lineTo(q[0],q[1]); st=false; lx=q[0]; }); ctx.stroke(); ctx.setLineDash([]);
  const e=P[P.length-1], f=P[Math.max(0,P.length-3)]; if(e[2]>0&&f[2]>0){ const a=Math.atan2(e[1]-f[1],e[0]-f[0]), L=9*Math.min(1.5,Math.sqrt(S.zoom)); ctx.fillStyle=col; ctx.beginPath(); ctx.moveTo(e[0],e[1]); ctx.lineTo(e[0]-L*Math.cos(a-.45),e[1]-L*Math.sin(a-.45)); ctx.lineTo(e[0]-L*Math.cos(a+.45),e[1]-L*Math.sin(a+.45)); ctx.closePath(); ctx.fill(); }
  const s0=P[0]; if(s0[2]>0){ ctx.fillStyle=col; ctx.beginPath(); ctx.arc(s0[0],s0[1],3.4,0,7); ctx.fill(); } ctx.globalAlpha=1; }
function epocheVon(j){ return j<1500?'mittel':j<1900?'neu':j<2000?'20':'heute'; }
function pname(id){ const p=(window.QW_DATEN&&window.QW_DATEN.pflanzen||[]).find(x=>x.id===id); return p?p.name.replace(' & Kiefernknospen',''):id; }
function inBereich(P,g){ return P[2].some(b=>g[1]>=b[0]&&g[1]<=b[1]&&g[0]>=b[2]&&g[0]<=b[3]) && P[3].some(z=>g[2].startsWith(z)); }
function sonne(d){ d=d||new Date(); const t=(Date.UTC(d.getUTCFullYear(),d.getUTCMonth(),d.getUTCDate())-Date.UTC(d.getUTCFullYear(),0,0))/864e5; const dekl=-23.44*Math.cos(2*Math.PI/365*(t+10)); const h=d.getUTCHours()+d.getUTCMinutes()/60; return [(12-h)*15,dekl]; }
function nacht(G3){ const [sl,sp]=sonne(); const al=sl+180, ap=-sp; const pts=[]; for(let i=0;i<=180;i++){ const b=i*2*R2, d=90*R2, p1=ap*R2, l1=al*R2; const la=Math.asin(Math.sin(p1)*Math.cos(d)+Math.cos(p1)*Math.sin(d)*Math.cos(b)); const lo=l1+Math.atan2(Math.sin(b)*Math.sin(d)*Math.cos(p1),Math.cos(d)-Math.sin(p1)*Math.sin(la)); pts.push([((lo/R2+540)%360)-180,la/R2]); }
  if(S.modus==='scheibe'){ const q=proj(sl,sp), m=proj(sl+180,-sp), R0=rd(), cx=W/2+S.px, cy=H/2+S.py; const gg=ctx.createRadialGradient(q[0],q[1],R0*0.12,q[0],q[1],R0*1.1); gg.addColorStop(0,'rgba(2,6,20,0)'); gg.addColorStop(.45,'rgba(2,6,20,.15)'); gg.addColorStop(.7,'rgba(2,6,20,.6)'); gg.addColorStop(1,'rgba(2,6,20,.7)'); if(!G3){ ctx.save(); ctx.beginPath(); ctx.arc(cx,cy,R0,0,7); ctx.clip(); ctx.fillStyle=gg; ctx.fillRect(0,0,W,H); ctx.restore(); }
    ctx.fillStyle='#e8ecf4'; ctx.shadowColor='#c8d8ff'; ctx.shadowBlur=12; ctx.beginPath(); ctx.arc(m[0],m[1],5,0,7); ctx.fill(); ctx.shadowBlur=0; text('Mond',m[0]+8,m[1]+4,10,'#e8ecf4'); text('Sonne',q[0]+9,q[1]+4,10,'#ffe8a0'); }
  else if(G3){}
  else if(S.modus==='globus'){ ctx.beginPath(); pfad(pts); ctx.fillStyle='rgba(2,6,20,.55)'; ctx.fill(); }
  else { ctx.fillStyle='rgba(2,6,20,.5)'; for(let lo=-180;lo<180;lo+=2) for(let la=-89;la<90;la+=2){ const x=Math.cos(la*R2)*Math.cos((lo-sl)*R2)*Math.cos(sp*R2)+Math.sin(la*R2)*Math.sin(sp*R2); if(x<0){ const a=proj(lo,la+1),b=proj(lo+2,la-1); if(Math.abs(a[0]-b[0])<W/4) ctx.fillRect(a[0],a[1],b[0]-a[0]+.6,b[1]-a[1]+.6); } } }
  const q=proj(sl,sp); if(q[2]>0){ ctx.fillStyle='#ffd860'; ctx.shadowColor='#ffd860'; ctx.shadowBlur=14; ctx.beginPath(); ctx.arc(q[0],q[1],5,0,7); ctx.fill(); ctx.shadowBlur=0; } }

/* ---------- Treffer ---------- */
function inring(x,y,r){ let c=false; for(let i=0,j=r.length-1;i<r.length;j=i++){ const [xi,yi]=r[i],[xj,yj]=r[j]; if((yi>y)!==(yj>y)&&x<(xj-xi)*(y-yi)/((yj-yi)||1e-9)+xi) c=!c; } return c; }
function landAn(lon,lat){ for(const c of DAT.laender){ const b=c.bb; if(lon<b[0]||lon>b[1]||lat<b[2]||lat>b[3]) continue; if(c.p.some(r=>inring(lon,lat,r))) return c; } return null; }
function blAn(lon,lat){ const L=DAT.bl||[]; for(let k=L.length-1;k>=0;k--){ const b=L[k], bb=b.bb; if(lon<bb[0]||lon>bb[1]||lat<bb[2]||lat>bb[3]) continue; if(b.p.some(r=>inring(lon,lat,r))) return b; } return null; }
function rasterAn(lon,lat){ const x=Math.round((lon+179)/2)*2-179, y=Math.round((lat+89)/2)*2-89; return DAT.rmap[x+','+y]; }
function histAn(x,y){ let best=null,bd=18; if(S.ov.kriege) KRIEGE.forEach((k,i)=>{ if(S.epoche&&epocheVon(k[1])!==S.epoche) return; const q=proj(k[3],k[4]); if(q[2]<0.1) return; const d=Math.hypot(q[0]-x,q[1]-y); if(d<bd){bd=d;best=['k',i];} });
  if(S.ov.wander) WANDER.forEach((w,i)=>{ if(S.epoche&&w[2]!==S.epoche) return; w[6].forEach(p=>p.forEach(pt=>{ const q=proj(pt[0],pt[1]); if(q[2]<0.1) return; const d=Math.hypot(q[0]-x,q[1]-y); if(d<bd){bd=d;best=['w',i];} })); });
  const chk=(on,arr,lo,la,k)=>{ if(!on) return; arr.forEach((e,i)=>{ const q=proj(e[lo],e[la]); if(q[2]<0.1) return; const d=Math.hypot(q[0]-x,q[1]-y); if(d<bd){bd=d;best=[k,i];} }); };
  chk(S.ov.erf,ERF,4,5,'e'); chk(S.ov.geld,GELD,3,4,'m'); chk(S.ov.goethe,GOETHE,3,4,'g'); return best; }

/* ---------- Info-Karte ---------- */
function spark(i){ const p=reihe(i,'pop'); if(!p) return ''; const v=p.filter(x=>x!=null), mx=Math.max(...v), mn=Math.min(...v); const w=260,h=56; let d=''; p.forEach((x,k)=>{ if(x==null) return; const X=k/63*w, Y=h-4-(x-mn)/((mx-mn)||1)*(h-10); d+=(d?'L':'M')+X.toFixed(1)+','+Y.toFixed(1); }); const k=S.jahr-1960, cx=k/63*w, cy=p[k]!=null?h-4-(p[k]-mn)/((mx-mn)||1)*(h-10):h;
  return `<svg viewBox="0 0 ${w} ${h}" class="qwk-spark"><defs><linearGradient id="qwsg" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#9fcf8a" stop-opacity=".45"/><stop offset="1" stop-color="#9fcf8a" stop-opacity="0"/></linearGradient></defs><path d="${d}L${w},${h}L0,${h}Z" fill="url(#qwsg)"/><path d="${d}" fill="none" stroke="#9fcf8a" stroke-width="2"/><circle cx="${cx}" cy="${cy}" r="3.5" fill="#fff"/></svg>`; }
/* Länderverläufe als Kurs-Diagramm (Komponente QWKurs aus der Hauptdatei) */
const KZ={r:0}; let KLAND=null;
function kursReihen(i){ const J=(k,f=v=>v)=>{ const a=reihe(i,k); return a?a.map((v,j)=>v==null?null:[1960+j,f(v)]).filter(Boolean):[]; };
  const pop=J('pop'), pm=Math.max(0,...pop.map(p=>p[1])), gross=pm>=1000;
  const sm=reihe(i,'sm'), sf=reihe(i,'sf'), su=sm&&sf?sm.map((v,j)=>v!=null&&sf[j]!=null?[1960+j,(v+sf[j])/2]:null).filter(Boolean):[];
  return [
   {name:'Bevölkerung',kurz:'👥 Einwohner',einheit:gross?'Mio.':'Tsd.',dez:!gross?0:pm>=1e5?0:pm>=1e4?1:2,hoeherGut:null,farbe:'#7fb4ff',punkte:gross?pop.map(p=>[p[0],p[1]/1000]):pop},
   {name:'Lebenserwartung',kurz:'❤️ Lebenserw.',einheit:'Jahre',dez:1,hoeherGut:true,farbe:'#ff8fa3',punkte:J('le')},
   {name:'Geburtenrate',kurz:'👶 Geburten',einheit:'Kinder je Frau',dez:2,hoeherGut:null,farbe:'#ffd27a',punkte:J('fr')},
   {name:'Kindersterblichkeit',kurz:'🍼 Kindersterbl.',einheit:'je 1.000',dez:1,hoeherGut:false,farbe:'#ffa86b',punkte:J('km')},
   {name:'Suizidrate',kurz:'🕯️ Suizid',einheit:'je 100.000',dez:1,hoeherGut:false,farbe:'#c9a6ff',punkte:su},
   {name:'Lebenszufriedenheit',kurz:'😊 Zufriedenheit',einheit:'von 10',dez:2,hoeherGut:true,farbe:'#8ee6a8',punkte:J('gl')},
   {name:'Unterernährung',kurz:'🥣 Unterernährung',einheit:'%',dez:1,hoeherGut:false,farbe:'#ff9a8a',punkte:J('un')},
   {name:'Energie pro Kopf',kurz:'⚡ Energie',einheit:'kWh',dez:0,hoeherGut:null,farbe:'#5fd6d0',punkte:J('epc')},
   {name:'Erneuerbarer Strom',kurz:'🌱 Erneuerbar',einheit:'%',dez:1,hoeherGut:true,farbe:'#9fcf8a',punkte:J('ren')},
   {name:'Erdöl-Förderung',kurz:'🛢️ Öl',einheit:'TWh',dez:0,hoeherGut:null,farbe:'#ff8a3d',punkte:J('oil')},
   {name:'Erdgas-Förderung',kurz:'🔥 Gas',einheit:'TWh',dez:0,hoeherGut:null,farbe:'#5fb8ff',punkte:J('gas')},
   {name:'Kohle-Förderung',kurz:'⛏️ Kohle',einheit:'TWh',dez:0,hoeherGut:null,farbe:'#b0a8a0',punkte:J('coal')}
  ].filter(r=>r.punkte.length>=3&&r.punkte.some(p=>p[1]>0)); }
function kursLand(box,i){ const el=$('.qwk-kurs',box); if(!el) return; if(!window.QWKurs){ el.innerHTML=spark(i); return; }
  const neu=KLAND!==i; KLAND=i;
  QWKurs.mount(el,{reihen:kursReihen(i),kompakt:true,zeitraum:[10,25,50],marke:S.jahr,zustand:KZ,anim:neu,quelle:'Our World in Data (UN, Weltbank, Energy Institute, WHO, World Happiness Report)'}); }
function chip(t,href,kl=''){ return href?`<a class="qwk-chip ${kl}" href="${href}">${t}</a>`:`<span class="qwk-chip ${kl}">${t}</span>`; }
function infoHist(){ const box=$('.qwk-info',wrap); const [art,i]=S.hist;
  const kopf=(e,t,u)=>`<div class="qwk-kopf"><span class="qwk-flag">${e}</span><div><h2>${t}</h2><small>${u}</small></div><button class="qwk-x" aria-label="Schließen">✕</button></div>`;
  const jt=j=>j<0?(-j)+' v. Chr.':j;
  if(art==='k'){ const k=KRIEGE[i], g=GANSER[k[0]]; box.innerHTML=kopf('⚔️',k[0],`${k[1]===k[2]?k[1]:k[1]+'–'+(k[2]||'heute')} · ${EPOCHE[epocheVon(k[1])]}`)+`<p class="qwk-txt">${k[6]}</p><h4>Opfer (Schätzung)</h4><div>${chip('🕯️ '+k[5])}</div>${g?`<h4>Sicht Daniele Ganser</h4><p class="qwk-txt">${g[0]}</p><h4>Gängige Darstellung</h4><p class="qwk-txt">${g[1]}</p><div>${chip('👤 Ganser im Kompendium','#a-ganser','k')}${chip('📖 Kriege & Konflikte','#w-kriege','k')}</div>`:`<div>${chip('📖 Kriege & Konflikte','#w-kriege','k')}</div>`}<p class="qwk-hin2">Zahlen sind gerundete Schätzungen; je nach Quelle weichen sie teils stark voneinander ab. Die Sichtweisen stehen zur eigenen Meinungsbildung nebeneinander.</p>`; }
  else if(art==='e'){ const e=ERF[i]; box.innerHTML=kopf('💡',e[0],`${jt(e[1])} · ${e[3]}`)+`<p class="qwk-txt">${e[6]}</p><h4>Wer</h4><div>${chip('👤 '+e[2])}</div><div>${e[7]?chip('📖 Im Kompendium',e[7],'k'):''}${chip('💡 Alle Erfindungen','#w-erfindungen','k')}</div>`; }
  else if(art==='m'){ const g=GELD[i]; box.innerHTML=kopf('🪙',g[0],`${jt(g[1])} · ${g[2]}`)+`<p class="qwk-txt">${g[5]}</p><div>${chip('📖 Geldsystem & Geldgeschichte','#w-geld','k')}${chip('👤 Markus Krall','#a-krall','k')}</div>`; }
  else if(art==='g'){ const g=GOETHE[i], alle=GOETHE.filter(x=>x[0]===g[0]); box.innerHTML=kopf('✒️',g[0],'Goethes Lebens- und Reisestationen')+alle.filter(x=>x[6]).map(x=>`<div class="qwk-box"><small>${x[1]===x[2]?x[1]:x[1]+'–'+x[2]} · ${x[5]}</small><p class="qwk-txt" style="margin:4px 0 0">${x[6]}</p></div>`).join('')+`<div style="margin-top:10px">${chip('👤 Goethe im Kompendium','#a-goethe','k')}</div>`; }
  else { const w=WANDER[i]; box.innerHTML=`<div class="qwk-kopf"><span class="qwk-flag">🧭</span><div><h2>${w[0]}</h2><small>${w[1]} · ${EPOCHE[w[2]]}</small></div><button class="qwk-x" aria-label="Schließen">✕</button></div><p class="qwk-txt">${w[5]}</p>${w[4]?`<h4>Umfang</h4><div>${chip('👣 '+w[4])}</div>`:''}<p class="qwk-hin2">Pfeile zeigen die Hauptrichtungen vereinfacht, nicht die genauen Wege.</p>`; }
  $('.qwk-x',box).onclick=()=>{ S.hist=null; info(); zeichne(); wrap.classList.remove('qwk-info-auf'); }; }
function balken(k,hl){ const G=GRUND[k], arr=Object.keys(DE).map(c=>[c,deWert(c,k)]).filter(a=>a[1]!=null).sort((a,b)=>b[1]-a[1]), mx=Math.max(...arr.map(a=>a[1])), name=c=>((DAT.bl||[]).find(b=>b.i===c)||{n:c}).n, bund=DEBUND[k];
  return `<div class="qwk-bars">${arr.map(([c,v])=>`<div class="${c===hl?'hl':''}" data-bl="${c}"><span>${name(c)}</span><i><b style="width:${(Math.max(.05,Math.min(1,G.s(v)))*100).toFixed(1)}%;background:${ramp(G.p,G.s(v))}"></b></i><em>${fmt(v,['de_hz','de_ek','de_bip'].includes(k)?0:1)}</em></div>`).join('')}${bund!=null?`<div class="bund"><span>Deutschland</span><i><b style="width:${(Math.max(.05,Math.min(1,G.s(bund)))*100).toFixed(1)}%"></b></i><em>${fmt(bund,['de_hz','de_ek','de_bip'].includes(k)?0:1)}</em></div>`:''}</div>`; }
function infoBL(){ const box=$('.qwk-info',wrap), b=DAT.bl.find(x=>x.i===S.bl), d=DE[S.bl], G=GRUND[S.grund], ew=d[3]/d[0]*1e5;
  const rang=k=>{ const a=Object.keys(DE).map(c=>deWert(c,k)).sort((x,y)=>y-x); return a.indexOf(deWert(S.bl,k))+1; }, x=DEX[S.bl];
  box.innerHTML=`<div class="qwk-kopf"><span class="qwk-flag">🇩🇪</span><div><h2>${b.n}</h2><small>Bundesland · ca. ${fmt(ew/1e6,2)} Mio. Einwohner</small></div><button class="qwk-x" aria-label="Schließen">✕</button></div>
  <div class="qwk-kpi"><div><small>🕯️ Suizidrate 2024</small><b>${fmt(d[0],1)}</b> <i>je 100.000 · Rang ${rang('de_su')}/16</i></div><div><small>🧠 Demenz 65+</small><b>${fmt(d[4])} Tsd.</b> <i>${fmt(deWert(S.bl,'de_dem'),1)} je 100 Ew.</i></div><div><small>🚔 Straftaten 2024</small><b>${fmt(d[5])}</b> <i>je 100.000 · Rang ${rang('de_hz')}/16</i></div><div><small>🔎 Aufklärung</small><b>${fmt(d[6],1)} %</b> <i>Rang ${rang('de_aq')}/16</i></div></div>
  <div class="qwk-kpi" style="margin-top:8px"><div><small>❤️ Lebenserwartung</small><b>${fmt(deWert(S.bl,'de_le'),1)}</b> <i>♂ ${fmt(x[0],1)} · ♀ ${fmt(x[1],1)}</i></div><div><small>👵 Durchschnittsalter</small><b>${fmt(x[2],1)}</b> <i>Jahre</i></div><div><small>💶 Einkommen je Ew.</small><b>${fmt(x[3])} €</b> <i>verfügbar 2024</i></div><div><small>🏭 BIP je Ew.</small><b>${fmt(x[4])} €</b> <i>${x[5]!=null?'· Öko '+fmt(x[5],1)+' %':''}</i></div></div>
  <div class="qwk-box"><small>Suizide 2024: ${fmt(d[3])} (Männer ${fmt(d[1],1)}, Frauen ${fmt(d[2],1)} je 100.000)</small></div>
  <h4>${G.e} ${G.n} – alle Länder</h4>${balken(S.grund,S.bl)}
  <div>${chip('📖 Suizid','#w-suizid','k')}${chip('📖 Demenz','#w-demenz','k')}${chip('📖 Kriminalität','#w-kriminalitaet','k')}${chip('📊 Deutschland in Zahlen','#w-deutschland','k')}</div><p class="qwk-hin2">Quelle: ${G.q}. Einwohner aus Suizidzahl und -rate errechnet.</p>`;
  box.querySelectorAll('[data-bl]').forEach(r=>r.onclick=()=>{ S.bl=r.dataset.bl; infoBL(); zeichne(); });
  $('.qwk-x',box).onclick=()=>{ S.bl=null; info(); zeichne(); wrap.classList.remove('qwk-info-auf'); }; }
function info(){
  const box=$('.qwk-info',wrap); if(S.hist) return infoHist(); if(S.bl&&GRUND[S.grund].de) return infoBL(); if(!S.sel&&GRUND[S.grund].de){ box.innerHTML=`<div class="qwk-kopf"><span class="qwk-flag">🇩🇪</span><div><h2>${GRUND[S.grund].n}</h2><small>${GRUND[S.grund].u}</small></div></div>${balken(S.grund)}<p class="qwk-hin2">Bundesland antippen für alle Werte. Quelle: ${GRUND[S.grund].q}</p><div>${chip('📖 Mehr dazu',GRUND[S.grund].l,'k')}</div>`; box.querySelectorAll('[data-bl]').forEach(r=>r.onclick=()=>{ S.bl=r.dataset.bl; infoBL(); zeichne(); }); return; }
  if(!S.sel){ box.innerHTML=`<div class="qwk-leer"><div class="qwk-gl">🌍</div><b>Land antippen</b><p>Tippe auf ein Land, um Einwohner, Dichte, Lebenserwartung, Ernten, Rohstoffe und passende Kapitel aus dem Kompendium zu sehen.</p><p class="qwk-mini">Ziehen = drehen · Zwei Finger oder Mausrad = zoomen · Beim Hineinzoomen erscheinen Städte, Flüsse und Landschaften</p></div>`; return; }
  const c=DAT.idx[S.sel], i=c.i, j=S.jahr, o=ow(i);
  const pop=wert(i,'pop',j), di=wert(i,'dichte',j), wa=wert(i,'wachstum',j);
  let h=`<div class="qwk-kopf"><span class="qwk-flag">${c.f||'🏳️'}</span><div><h2>${c.n}</h2><small>Stand ${j}${S.klick?` · ${fmt(Math.abs(S.klick[1]),1)}° ${S.klick[1]>=0?'N':'S'}, ${fmt(Math.abs(S.klick[0]),1)}° ${S.klick[0]>=0?'O':'W'}`:''}</small></div><button class="qwk-x" aria-label="Schließen">✕</button></div>
  <div class="qwk-kpi"><div><small>Einwohner</small><b>${pop?pop>=1e6?fmt(pop/1e6,2)+' Mrd.':pop>=1000?fmt(pop/1000,1)+' Mio.':fmt(pop)+' Tsd.':'–'}</b></div><div><small>Dichte</small><b>${fmt(di)} <i>/km²</i></b></div><div><small>Wachstum</small><b class="${wa>0?'plus':'minus'}">${wa==null?'–':(wa>0?'+':'')+fmt(wa,1)+' %'}</b></div><div><small>Fläche (ca.)</small><b>${fmt(c.a/1000)} <i>Tsd. km²</i></b></div></div>
  <div class="qwk-box qwk-kursbox"><div class="qwk-kurs"></div></div>`;
  const ges=[['le','❤️ Lebenserwartung',v=>fmt(v,1)+' Jahre'],['fr','👶 Geburtenrate',v=>fmt(v,2)+' Kinder je Frau'],['km','🍼 Kindersterblichkeit',v=>fmt(v)+' je 1.000'],['su','🕯️ Suizidrate',v=>fmt(v,1)+' je 100.000'],['gl','😊 Lebenszufriedenheit',v=>fmt(v,1)+' von 10'],['un','🥣 Unterernährung',v=>fmt(v,1)+' %']].map(([k,n,f])=>{ const v=wert(i,k,j), st=stand(i,k,j); return v==null?'':chip(`${n}: ${f(v)}${st&&st!==j?` (${st})`:''}`); }).join('');
  h+=`<h4>Politik</h4><div>${chip('🏛️ '+STAAT[staatVon(i)][0],'#w-politik-systeme','k')}${i==='DEU'?chip('📜 Deutsche Geschichte','#w-dgeschichte','k'):''}</div>`;
  if(ges) h+=`<h4>Gesellschaft</h4><div>${ges}</div>`;
  const gt=Object.entries(GETREIDE).filter(([k,G2])=>G2.d[i]).map(([k,G2])=>chip(`${G2.e} ${G2.n} ${fmt(G2.d[i],1)} ${k==='hopfen'?'Tsd. t':'Mio. t'}`,G2.l));
  if(gt.length) h+=`<h4>Getreide (2022)</h4><div>${gt.join('')}</div>`;
  const rh=Object.entries(ROH).filter(([k,G2])=>G2.d[i]||(G2.f&&G2.f[i])||(G2.k&&ser(i,G2.k,j))).map(([k,G2])=>{ const pv=G2.k?ser(i,G2.k,j):null; return chip(`${G2.e} ${G2.n}${G2.d[i]?' · Reserven '+fmt(G2.d[i],G2.d[i]<10?1:0)+' '+G2.u:''}${pv&&pv.v?' · Förderung '+fmt(pv.v)+' TWh':''}${G2.f&&G2.f[i]?' · Förderung '+fmt(G2.f[i])+' t (2023)':''}`,G2.l); });
  if(rh.length) h+=`<h4>Rohstoffe & Energie</h4><div>${rh.join('')}</div>`;
  const en=wert(i,'energie',j), re=wert(i,'erneuerbar',j); h+=`<div>${en?chip('⚡ '+fmt(en)+' kWh pro Kopf'):''}${re!=null?chip('🌱 '+fmt(re,0)+' % erneuerbarer Strom'):''}</div>`;
  if(S.klick){ const g=rasterAn(S.klick[0],S.klick[1]); if(g) h+=`<h4>An dieser Stelle (Schema)</h4><div>${chip('🌡️ '+KLIMA[g[2]][0],'#s-boden')}${chip('🟫 '+BODEN[g[3]][0],'#s-boden')}${chip('🌳 '+VEGN[g[4]][0])}</div>`; }
  const kr=KRIEGE.filter(k=>{ const oc=landAn(k[3],k[4]); return oc&&oc.i===i; }).map(k=>chip(`⚔️ ${k[0]} (${k[1]}–${k[2]||'heute'})`));
  if(kr.length) h+=`<h4>Geschichte</h4><div>${kr.join('')}</div>`;
  const pf=Object.entries(PFL).filter(([id,P])=>{ const oc=landAn(P[0][0],P[0][1]); if(oc&&oc.i===i) return true; if(S.klick){ const g=rasterAn(S.klick[0],S.klick[1]); return g&&inBereich(P,g); } return false; }).map(([id,P])=>chip('🌿 '+pname(id),'#'+id,'k'));
  const rz=REZ.filter(r=>r[4]===i).map(r=>chip('🍽️ '+r[1],'#r-'+r[0],'k'));
  const au=AUT.filter(a=>{ const oc=landAn(a[2],a[3]); return oc&&oc.i===i; }).map(a=>chip('👤 '+a[1].split(' · ')[0],'#a-'+a[0],'k'));
  if(i==='DEU') h+=`<h4>Deutschland nach Bundesländern</h4><div>${Object.keys(GRUND).filter(k=>GRUND[k].de).map(k=>`<button class="qwk-chip k" data-dek="${k}">${GRUND[k].e} ${GRUND[k].n.replace('\u00ad','')}</button>`).join('')}</div>`;
  const kp=[...pf,...rz,...au]; if(kp.length) h+=`<h4>Im Kompendium</h4><div>${kp.join('')}</div>`;
  box.innerHTML=h; kursLand(box,i); box.querySelectorAll('[data-dek]').forEach(b=>b.onclick=()=>grundSetzen(b.dataset.dek)); $('.qwk-x',box).onclick=()=>{ S.sel=null; S.klick=null; info(); zeichne(); wrap.classList.remove('qwk-info-auf'); };
}

/* ---------- Legende ---------- */
function legende(){
  const g=GRUND[S.grund], L=$('.qwk-leg',wrap); let h=`<b>${g.e} ${g.n}</b>${g.u?` <span class="qwk-u">${g.u}</span>`:''}`;
  if(g.p) h+=`<div class="qwk-ramp" style="background:linear-gradient(90deg,${g.p.join(',')})"></div><div class="qwk-rl"><span>${g.lg[0]}</span><span>${g.lg[1]}</span><span>${g.lg[2]}</span></div>`;
  else if(g.r){ const t=g.r===2?KLIMA:g.r===3?BODEN:VEGN; h+=`<div class="qwk-kl">${Object.values(t).map(([n,c])=>`<span><i style="background:${c}"></i>${n}</span>`).join('')}</div><div class="qwk-hin">Vereinfachtes Schema (2°-Raster), keine Messkarte</div>`; }
  else if(S.grund==='relief') h+=`<div class="qwk-ramp" style="background:linear-gradient(90deg,#4e7842,#b0aa70,#aa8a60,#8c6c56,#f6f4f0)"></div><div class="qwk-rl"><span>Tiefland</span><span>Hochland</span><span>Hochgebirge, Eis</span></div>`;
  if(S.modus==='scheibe') h+=`<div class="qwk-hin">◎ Scheibe: Darstellung nach dem Flache-Erde-Modell – Nordpol in der Mitte, Antarktis als Eiswall am Rand (Kartennetz wie Gleason 1892). Sonne und Mond kreisen als Scheinwerfer (Tag & Nacht einschalten). Vergleich im Kapitel W-12.</div>`;
  if(g.de) h+=`<div class="qwk-hin">Quelle: ${g.q}</div>`;
  if(g.kat) h+=`<div class="qwk-kl">${Object.values(STAAT).map(([n,c])=>`<span><i style="background:${c}"></i>${n}</span>`).join('')}</div><div class="qwk-hin">Vereinfachte Einordnung, Stand 2026. Mehr im Kapitel W-08 Politik.</div>`;
  if(S.grund==='relief') h+=`<div class="qwk-ramp" style="background:linear-gradient(90deg,#468cb9,#1e508a,#133768,#081a40,#05112e)"></div><div class="qwk-rl"><span>Schelf 0–200 m</span><span>4.000 m</span><span>über 8.000 m</span></div>`;
  if(S.grund==='su') h+=`<div class="qwk-hin">Mittel aus Männer- und Frauenrate (IHME). Hilfe in Deutschland: Telefonseelsorge 0800 111 0 111</div>`;
  const ov=[]; Object.entries(GETREIDE).forEach(([k,G2])=>S.ov[k]&&ov.push(`<span><i class="r" style="background:${G2.c}"></i>${G2.n}</span>`)); Object.entries(ROH).forEach(([k,G2])=>S.ov[k]&&ov.push(`<span><i class="d" style="background:${G2.c}"></i>${G2.n}</span>`));
  if(S.ov.kriege) ov.push('<span><i class="r" style="background:#d8302a"></i>Kriege</span>'); if(S.ov.wander) ov.push('<span><i class="l"></i>Wanderungen</span>'); if(S.ov.erf) ov.push('<span><i class="r" style="background:#ffe14a"></i>Erfindungen</span>'); if(S.ov.geld) ov.push('<span><i class="r" style="background:#e8b030"></i>Geldgeschichte</span>'); if(S.ov.tiefen) ov.push('<span><i class="d" style="background:#7fe0ff"></i>Tiefseegräben (tiefste Stellen, ca.)</span>'); if(S.ov.goethe) ov.push('<span><i class="r" style="background:#ff8c6e"></i>Goethe (Größe = Dauer)</span>');
  if(S.ov.pfl) ov.push('<span><i class="r" style="background:#ff6a8a"></i>Pflanzen-Herkunft</span>'); if(S.ov.rez) ov.push('<span><i class="r" style="background:#c79aff"></i>Rezepte</span>'); if(S.ov.aut) ov.push('<span><i class="r" style="background:#6ac8ff"></i>Autoren</span>');
  if(ov.length) h+=`<div class="qwk-kl qwk-ov">${ov.join('')}</div>`;
  L.innerHTML=h; }

/* ---------- Oberfläche ---------- */
const CSS=`
.qwk{--k-bg:#070b10;--k-p:#0d151c;--k-p2:#131e27;--k-l:#243542;--k-t:#ecebdf;--k-m:#97a5a2;--k-a:#9fcf8a;position:relative;display:grid;grid-template-columns:300px 1fr 340px;grid-template-rows:auto 1fr auto;height:calc(100vh - 150px);height:calc(100dvh - var(--qw-oben,120px) - var(--qw-unten,0px) - env(safe-area-inset-bottom,0px) - 18px);min-height:480px;background:var(--k-bg);color:var(--k-t);border-radius:18px;overflow:hidden;font:15px var(--body,system-ui),system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;box-shadow:0 20px 60px rgba(0,0,0,.35);width:auto;max-width:1800px;margin:0 auto;margin-inline:max(16px,calc(50% - 900px))}
.qwk *{box-sizing:border-box}
.qwk-top{grid-column:1/4;display:flex;align-items:center;gap:12px;padding:12px 16px;background:linear-gradient(180deg,#0e171e,#0b1218);border-bottom:1px solid var(--k-l);flex-wrap:wrap}
.qwk-titel{display:flex;align-items:center;gap:10px;font:700 18px Georgia,serif}.qwk-gl2{width:30px;height:30px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#7ad8ff,#1b4f8a 60%,#08203e);box-shadow:0 0 14px rgba(80,170,255,.6)}
.qwk-titel small{display:block;font:500 11.5px system-ui;color:var(--k-m)}
.qwk-seg{display:inline-flex;background:#0a1117;border:1px solid var(--k-l);border-radius:12px;padding:3px;gap:2px}
.qwk-seg button{all:unset;cursor:pointer;padding:8px 12px;border-radius:9px;color:#aab6d0;font-weight:600;font-size:13px;transition:background .2s,color .2s}
.qwk-seg button[aria-pressed=true]{background:linear-gradient(180deg,#24363f,#1a2a32);color:#fff;box-shadow:inset 0 0 0 1px #45606c,0 4px 14px rgba(10,30,40,.35)}
.qwk-such{margin-left:auto;position:relative}.qwk-such input{all:unset;box-sizing:border-box;width:250px;padding:9px 12px 9px 34px;background:#0a1117;border:1px solid var(--k-l);border-radius:12px;color:var(--k-t);font-size:13.5px}.qwk-such:before{content:"⌕";position:absolute;left:12px;top:6px;color:var(--k-m);font-size:18px}
.qwk-side{background:var(--k-p);border-right:1px solid var(--k-l);overflow:auto;padding:10px 14px 20px}
.qwk-side h3{font:700 10.5px system-ui;letter-spacing:.14em;text-transform:uppercase;color:var(--k-m);margin:16px 2px 8px;display:flex;align-items:center;gap:8px}.qwk-side h3:after{content:"";flex:1;height:1px;background:var(--k-l)}
.qwk-grund{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px}.qwk-grund button span:last-child{hyphens:auto;-webkit-hyphens:auto}
.qwk-grund button{all:unset;display:flex;gap:6px;align-items:center;cursor:pointer;padding:8px 9px;line-height:1.25;border-radius:11px;background:var(--k-p2);border:1px solid var(--k-l);font-size:12.3px;font-weight:600;color:#cdd6ea;transition:.18s}
.qwk-grund button:hover{border-color:#36507a}.qwk-grund button[aria-pressed=true]{background:linear-gradient(180deg,#22331c,#1a2916);border-color:var(--k-a);color:#fff;box-shadow:0 0 0 1px rgba(159,207,138,.25),0 6px 18px rgba(159,207,138,.15)}
.qwk-sw{display:flex;align-items:center;gap:10px;padding:6px 4px;border-radius:9px;cursor:pointer;font-size:13.3px;user-select:none}.qwk-sw:hover{background:rgba(255,255,255,.03)}
.qwk-sw input{display:none}.qwk-sw .k{width:36px;height:21px;border-radius:12px;background:#1a2438;border:1px solid #2a3858;position:relative;flex:none;transition:.2s}.qwk-sw .k:after{content:"";position:absolute;top:2px;left:2px;width:15px;height:15px;border-radius:50%;background:#6a7898;transition:.2s}
.qwk-sw input:checked+.k{background:linear-gradient(90deg,#5d8f48,#9fcf8a);border-color:#9fcf8a;box-shadow:0 0 12px rgba(159,207,138,.35)}.qwk-sw input:checked+.k:after{left:17px;background:#fff}
.qwk-sw .dt{width:10px;height:10px;border-radius:50%;flex:none;box-shadow:0 0 8px currentColor}.qwk-sw .dt.d{border-radius:2px;transform:rotate(45deg)}
.qwk-sel{all:unset;box-sizing:border-box;width:100%;padding:9px 10px;background:var(--k-p2);border:1px solid var(--k-l);border-radius:11px;font-size:13px;color:var(--k-t);margin:6px 0}
.qwk-map{position:relative;overflow:hidden;touch-action:none;cursor:grab;-webkit-user-select:none;user-select:none;-webkit-touch-callout:none}.qwk-map:active{cursor:grabbing}.qwk-map canvas{display:block;width:100%;height:100%;position:relative}.qwk-map canvas.qwk-erde{position:absolute;inset:0}
.qwk-zoom{position:absolute;right:14px;top:14px;display:flex;flex-direction:column;gap:6px}.qwk-zoom{background:rgba(12,19,34,.78);border:1px solid var(--k-l);border-radius:14px;padding:3px;gap:2px!important;-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);box-shadow:0 8px 24px rgba(0,0,0,.35)}.qwk-zoom button{all:unset;cursor:pointer;width:42px;height:42px;border-radius:11px;display:grid;place-items:center;font-size:18px;color:#dfe8fa;transition:background .15s}.qwk-zoom button:hover,.qwk-zoom button:active{background:rgba(255,255,255,.1)}.qwk-zoom button[aria-pressed=true]{color:var(--k-a)}.qwk-zoom hr{all:unset;display:block;height:1px;background:var(--k-l);margin:1px 6px}
.qwk-leg{position:absolute;left:14px;bottom:14px;max-width:340px;background:rgba(10,16,30,.8);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);border:1px solid var(--k-l);border-radius:14px;padding:10px 12px;font-size:12px;cursor:pointer;box-shadow:0 8px 24px rgba(0,0,0,.35)}.qwk-leg>b{display:flex;align-items:center;gap:6px;font-size:12.5px}.qwk-leg>b:after{content:"Ebenen ›";margin-left:auto;padding-left:12px;font:600 11px system-ui;color:var(--k-a);white-space:nowrap}.qwk-u{color:var(--k-m);font-size:11px}
.qwk-ramp{height:9px;border-radius:5px;margin:7px 0 4px;width:250px;max-width:100%;box-shadow:inset 0 0 0 1px rgba(255,255,255,.12)}.qwk-rl{display:flex;justify-content:space-between;gap:8px;color:var(--k-m);width:250px;max-width:100%;font-size:11px}
.qwk-kl{display:flex;flex-wrap:wrap;gap:4px 10px;margin-top:7px}.qwk-kl span{display:flex;align-items:center;gap:5px;color:#cdd6ea}.qwk-kl i{width:10px;height:10px;border-radius:3px;display:inline-block}.qwk-kl i.r{border-radius:50%}.qwk-kl i.d{transform:rotate(45deg);border-radius:1px}.qwk-kl i.l{height:0;width:16px;border-top:2px dashed #ffd28a;border-radius:0}
.qwk-ov{border-top:1px solid var(--k-l);padding-top:7px}.qwk-hin{color:var(--k-m);font-size:11px;margin-top:5px;max-width:300px}
.qwk-info{background:var(--k-p);border-left:1px solid var(--k-l);overflow:auto;padding:16px}
.qwk-kopf{display:flex;align-items:center;gap:12px;margin-bottom:12px}.qwk-flag{font-size:30px}.qwk-kopf h2{margin:0;font:800 22px var(--display,Georgia),Georgia,serif;color:#fff}.qwk-kopf small{color:var(--k-m)}
.qwk-x{all:unset;cursor:pointer;margin-left:auto;width:30px;height:30px;border-radius:9px;display:grid;place-items:center;color:var(--k-m);border:1px solid var(--k-l)}
.qwk-kpi{display:grid;grid-template-columns:1fr 1fr;gap:8px}.qwk-kpi div{background:var(--k-p2);border:1px solid var(--k-l);border-radius:12px;padding:9px 10px}.qwk-kpi small{display:block;color:var(--k-m);font-size:11px}.qwk-kpi b{font-size:17px;color:#fff;font-variant-numeric:tabular-nums}.qwk-kpi i{font-style:normal;font-size:11px;color:var(--k-m);font-weight:500}.qwk-kpi .plus{color:#ffb070}.qwk-kpi .minus{color:#7fb4ff}
.qwk-box{background:var(--k-p2);border:1px solid var(--k-l);border-radius:12px;padding:9px 10px;margin-top:8px}.qwk-box small{color:var(--k-m);font-size:11px}.qwk-spark{width:100%;height:56px;display:block;margin-top:4px}
.qwk-kursbox{padding:10px 10px 8px}.qwk .kurs{--ink:#e8eefb;--muted:#8d9ab8;--line:#24324f;--surface:#111a2d;--accent:#9fcf8a;--w:#7fb4ff;--body:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;--label:system-ui,sans-serif;--ku-gut:#9fcf8a;--ku-schlecht:#ff8a7a;--ku-fill:rgba(255,255,255,.07);--ku-on:#24324f}.qwk .ku-q{font-size:10.5px}
.qwk-info h4{font:700 10.5px system-ui;letter-spacing:.14em;text-transform:uppercase;color:var(--k-m);margin:14px 0 7px}
.qwk-txt{line-height:1.5;color:#dbe4f6;margin:0 0 8px}.qwk-hin2{color:var(--k-m);font-size:11.5px;margin-top:10px}
.qwk-chip{display:inline-block;padding:5px 10px;margin:0 5px 6px 0;border-radius:20px;background:var(--k-p2);border:1px solid var(--k-l);color:#dbe4f6;font-size:12.5px;text-decoration:none}.qwk-chip.k{background:rgba(159,207,138,.1);border-color:rgba(159,207,138,.45);color:#d2ecc4}a.qwk-chip:hover{border-color:var(--k-a)}
.qwk-leer{text-align:center;color:var(--k-m);padding:30px 10px}.qwk-leer b{color:#fff;font-size:16px}.qwk-gl{font-size:40px;margin-bottom:8px}.qwk-mini{font-size:12px}
.qwk-zeit{grid-column:1/4;display:flex;align-items:center;gap:14px;padding:10px 18px;background:#0b1218;border-top:1px solid var(--k-l)}
.qwk-play{all:unset;cursor:pointer;width:38px;height:38px;border-radius:50%;background:linear-gradient(180deg,#5d8f48,#3f6a2e);display:grid;place-items:center;box-shadow:0 0 14px rgba(159,207,138,.35);font-size:14px}
.qwk-zeit input{flex:1;min-width:0;accent-color:#9fcf8a;height:28px}.qwk-jahr{font-variant-numeric:tabular-nums}.qwk-jahr{font:800 24px var(--display,Georgia),Georgia,serif;min-width:64px;text-align:right}.qwk-q{color:var(--k-m);font-size:10.5px;max-width:540px;line-height:1.35}
.qwk-bars{display:flex;flex-direction:column;gap:3px;margin:4px 0 10px}.qwk-bars div{display:grid;grid-template-columns:118px 1fr 52px;align-items:center;gap:7px;font-size:11.8px;color:#cdd6ea;cursor:pointer;padding:1px 3px;border-radius:6px}.qwk-bars div:hover,.qwk-bars .hl{background:rgba(255,255,255,.07);color:#fff;font-weight:700}.qwk-bars span{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.qwk-bars i{height:11px;background:#141d30;border-radius:6px;overflow:hidden}.qwk-bars i b{display:block;height:100%;border-radius:6px;animation:qwkbar .8s ease-out}.qwk-bars em{font-style:normal;text-align:right;font-variant-numeric:tabular-nums}.qwk-bars .bund{border-top:1px dashed #2a3858;margin-top:3px;padding-top:4px;color:#fff}.qwk-bars .bund b{background:repeating-linear-gradient(45deg,#8d9ab8 0 4px,#5a6888 4px 8px)}@keyframes qwkbar{from{width:0}}
.qwk-mob,.qwk-bk{display:none}.qwk-bk{align-items:center;justify-content:space-between;position:sticky;top:-8px;z-index:2;margin:-2px -4px 0;padding:4px;background:inherit}.qwk-bk b{font:700 17px Georgia,serif}.qwk-bk button{all:unset;cursor:pointer;width:32px;height:32px;border-radius:50%;display:grid;place-items:center;background:#18233a;color:#cdd6ea}
.qwk button:focus-visible,.qwk-map:focus-visible,.qwk-sw:focus-within,.qwk-such input:focus-visible,.qwk-sel:focus-visible{outline:2px solid var(--k-a);outline-offset:2px}
@media (max-width:980px){.qwk{grid-template-columns:1fr;grid-template-rows:auto minmax(300px,1fr) auto;margin-inline:8px;border-radius:18px}.qwk-top{grid-column:1;padding:8px 10px;gap:8px}.qwk-titel{display:none}.qwk-top>.qwk-seg:not(.qwk-mob){flex:1 1 100%;display:grid;grid-auto-flow:column;grid-auto-columns:1fr}.qwk-top>.qwk-seg:not(.qwk-mob) button{text-align:center;padding:8px 4px;white-space:nowrap;font-size:12.5px}.qwk-such{order:2;flex:1 1 150px}.qwk-mob{order:3}.qwk-mob button{padding:9px 12px}.qwk-zeit{grid-column:1}.qwk-side,.qwk-info{position:absolute;z-index:5;left:0;right:0;bottom:58px;max-height:62%;border:1px solid var(--k-l);border-bottom:0;border-radius:20px 20px 0 0;transform:translateY(calc(100% + 90px));transition:transform .34s cubic-bezier(.2,.85,.25,1);box-shadow:0 -14px 44px rgba(0,0,0,.55);background:rgba(12,19,34,.94);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);max-width:560px;margin:0 auto;overscroll-behavior:contain}.qwk-side:before,.qwk-info:before{content:"";display:block;width:38px;height:5px;border-radius:3px;background:#3a4868;margin:0 auto 6px}.qwk-info{padding-top:8px}.qwk-side{padding-top:8px}.qwk-bk{display:flex}.qwk.qwk-ebenen-auf .qwk-side,.qwk.qwk-info-auf .qwk-info{transform:none}.qwk-mob{display:inline-flex}.qwk-such{margin-left:0;width:100%}.qwk-such input{width:100%}.qwk-leg{bottom:10px;left:10px;max-width:calc(100% - 20px);padding:8px 10px}.qwk-leg .qwk-hin{display:none}.qwk-q,.qwk-j0{display:none}.qwk-zeit{padding:8px 12px;gap:10px}.qwk-zoom{right:10px;top:10px}}
@media (max-width:980px) and (max-height:700px){.qwk-leg .qwk-kl:not(.qwk-ov){display:none}}
@media (prefers-reduced-motion:reduce){.qwk-side,.qwk-info{transition:none}.qwk-bars i b{animation:none}}
`;
function ui(root){
  const sw=(k,n,c,d)=>`<label class="qwk-sw"><input type="checkbox" data-ov="${k}" ${S.ov[k]?'checked':''}><span class="k"></span>${c?`<span class="dt ${d?'d':''}" style="color:${c};background:${c}"></span>`:''}${n}</label>`;
  const gb=k=>`<button data-grund="${k}" aria-pressed="${S.grund===k}"><span>${GRUND[k].e}</span><span>${GRUND[k].n}</span></button>`;
  const gruppe=g=>Object.keys(GRUND).filter(k=>GRUND[k].g===g).map(gb).join('');
  const pl=(window.QW_DATEN&&window.QW_DATEN.pflanzen||[]).map(p=>`<option value="${p.id}">${p.nr} ${p.name.replace(' & Kiefernknospen','')}</option>`).join('');
  root.innerHTML=`<style>${CSS}</style><div class="qwk" lang="de">
  <div class="qwk-top"><div class="qwk-titel"><span class="qwk-gl2"></span><div>Weltkarte<small>Natur · Menschen · Rohstoffe · Geschichte</small></div></div>
   <div class="qwk-seg"><button data-modus="globus" aria-pressed="${S.modus==='globus'}">◉ Globus</button><button data-modus="flach" aria-pressed="${S.modus==='flach'}">▭ Karte</button><button data-modus="scheibe" aria-pressed="${S.modus==='scheibe'}" title="Darstellung im Flache-Erde-Modell">◎ Scheibe</button><button data-d3 title="Relief der Scheibe in 3D (Flache-Erde-Modell)">⛰ 3D-Scheibe</button></div>
   <div class="qwk-seg qwk-mob"><button data-auf="ebenen">☰ Ebenen</button><button data-auf="info">ⓘ Info</button></div>
   <div class="qwk-such"><input list="qwk-dl" placeholder="Land, Stadt oder Pflanze …"><datalist id="qwk-dl">${DAT.laender.map(c=>`<option value="${c.n}">`).join('')}${DAT.staedte.slice(0,400).map(s=>`<option value="${s[0]}">`).join('')}${Object.keys(PFL).map(id=>`<option value="${pname(id)}">`).join('')}</datalist></div></div>
  <aside class="qwk-side" aria-label="Ebenen">
   <div class="qwk-bk"><b>Ebenen</b><button data-zu aria-label="Ebenen schließen">✕</button></div>
   <h3>Grundkarte · Natur</h3><div class="qwk-grund">${gruppe('Natur')}</div>
   <h3>Grundkarte · Menschen</h3><div class="qwk-grund">${gruppe('Menschen')}</div>
   <h3>Grundkarte · Wirtschaft</h3><div class="qwk-grund">${gruppe('Wirtschaft')}</div>
   <h3>Grundkarte · Politik</h3><div class="qwk-grund">${gruppe('Politik')}</div>
   <h3>Deutschland · Bundesländer</h3><div class="qwk-grund">${gruppe('Deutschland')}</div>
   <label class="qwk-sw" style="margin-top:6px"><input type="checkbox" data-unterlage ${S.unterlage?'checked':''}><span class="k"></span>Relief unter Statistik legen</label>
   <h3>Beschriftung</h3>${sw('namen','Ländernamen')}${sw('grenzen','Grenzen')}${sw('staedte','Städte (mehr beim Zoomen)','#ffe9b8')}${sw('fluesse','Flüsse & Seen','#5aaaff')}${sw('landschaft','Gebirge & Landschaften','#f0d8b8')}${sw('gipfel','Gipfel','#ffffff')}${sw('tiefen','Meerestiefen & Tiefseegräben','#7fe0ff',1)}${sw('wolken','Wolken','#f2f5fa')}${sw('nacht','Tag & Nacht (jetzt)','#ffd860')}
   <h3>Geschichte</h3>${sw('kriege','⚔️ Kriege','#d8302a')}${sw('wander','🧭 Völkerwanderungen','#ffd28a')}${sw('erf','💡 Erfindungen','#ffe14a')}${sw('geld','🪙 Geldgeschichte','#e8b030')}${sw('goethe','✒️ Goethes Reisen','#ff8c6e')}<select class="qwk-sel" data-epoche><option value="">Alle Epochen</option>${Object.entries(EPOCHE).map(([k,v])=>`<option value="${k}">${v}</option>`).join('')}</select>
   <h3>Getreide · Teil G</h3>${Object.entries(GETREIDE).map(([k,G2])=>sw(k,G2.e+' '+G2.n,G2.c)).join('')}
   <h3>Rohstoffe & Energie</h3>${Object.entries(ROH).map(([k,G2])=>sw(k,G2.e+' '+G2.n,G2.c,1)).join('')}
   <h3>Kompendium</h3>${sw('pfl','🌿 Herkunft der Pflanzen','#ff6a8a')}<select class="qwk-sel" data-pflanze><option value="">Wildvorkommen einer Pflanze zeigen …</option>${pl}</select>${sw('rez','🍽️ Rezepte nach Herkunft','#c79aff')}${sw('aut','👤 Autoren','#6ac8ff')}
  </aside>
  <div class="qwk-map" tabindex="0" role="application" aria-label="Weltkarte: ziehen dreht, Pfeiltasten drehen, Plus und Minus zoomen"><canvas></canvas><div class="qwk-zoom"><button data-z="1.5" aria-label="Hineinzoomen">＋</button><button data-z="0.67" aria-label="Herauszoomen">－</button><hr><button data-z="0" aria-label="Ansicht zurücksetzen" title="Ansicht zurücksetzen">⟲</button><button data-spin aria-pressed="false" aria-label="Globus langsam drehen" title="Globus langsam drehen">↻</button></div><div class="qwk-leg" title="Ebenen öffnen"></div></div>
  <aside class="qwk-info"></aside>
  <div class="qwk-zeit"><button class="qwk-play" aria-label="Abspielen">▶</button><span class="qwk-j0" style="color:var(--k-m)">1960</span><input type="range" min="1960" max="2023" value="${S.jahr}"><span class="qwk-jahr">${S.jahr}</span><span class="qwk-q">Quellen: Grenzen, Städte, Flüsse – Natural Earth (gemeinfrei); Relief – three.js-Beispieltextur (MIT); Bevölkerung, Energie, Gesellschaft – Our World in Data (UN, Energy Institute, IHME, Gapminder, WHR, FAO); Getreide – FAOSTAT 2022; Rohstoffe – Energy Institute, USGS, IAEA; Klima/Böden – vereinfachtes Schema</span></div>
  </div>`;
  wrap=$('.qwk',root); cv=$('canvas',wrap); ctx=cv.getContext('2d');
}
function groesse(){ const m=$('.qwk-map',wrap), r=m.getBoundingClientRect(); DPR=Math.min(2,devicePixelRatio||1); W=r.width; H=r.height; cv.width=W*DPR; cv.height=H*DPR; RKEY=''; zeichne(); }
const RUHE=()=>!!window.QW_STANDBILD||(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches);
let RAF=0; function neu(){ S.bewegt=true; if(RAF) return; RAF=requestAnimationFrame(()=>{ RAF=0; zeichne(false); }); }
const ZMIN=.6, ZMAX=40, zgrenz=z=>Math.max(ZMIN,Math.min(ZMAX,z));
let ZT=null, ZR=0; function zoomZu(z){ z=zgrenz(z); if(RUHE()){ S.zoom=z; ZT=null; zeichne(); return; } ZT=z; if(ZR) return;
  const st=()=>{ ZR=0; if(ZT==null||!wrap||!document.body.contains(wrap)) return; const d=Math.log(ZT/S.zoom); if(Math.abs(d)<0.012){ S.zoom=ZT; ZT=null; S.bewegt=true; zeichne(false); return; } S.zoom*=Math.exp(d*0.26); S.bewegt=true; zeichne(false); ZR=requestAnimationFrame(st); }; ZR=requestAnimationFrame(st); }
let SW=0; function schwungAus(){ if(SW){ cancelAnimationFrame(SW); SW=0; } }
function schwung(vx,vy){ schwungAus(); if(RUHE()||Math.hypot(vx,vy)<0.08) return; let t0=performance.now();
  const st=t=>{ SW=0; if(!wrap||!document.body.contains(wrap)) return; const dt=Math.min(40,Math.max(1,t-t0)); t0=t; const dx=vx*dt, dy=vy*dt;
    if(S.modus==='globus'){ const f=57/radius(); S.lam-=dx*f; S.phi=Math.max(-85,Math.min(85,S.phi+dy*f)); } else { S.px+=dx; S.py+=dy; }
    const k=Math.pow(.935,dt/16); vx*=k; vy*=k; S.bewegt=true; zeichne(false); if(Math.hypot(vx,vy)>0.025) SW=requestAnimationFrame(st); }; SW=requestAnimationFrame(st); }
function ereignisse(){
  wrap.querySelectorAll('[data-ov]').forEach(i=>i.onchange=()=>{ S.ov[i.dataset.ov]=i.checked; legende(); zeichne(); });
  $('[data-unterlage]',wrap).onchange=e=>{ S.unterlage=e.target.checked; zeichne(); };
  wrap.querySelectorAll('[data-grund]').forEach(b=>b.onclick=()=>grundSetzen(b.dataset.grund));
  wrap.querySelectorAll('[data-modus]').forEach(b=>b.onclick=()=>{ S.modus=b.dataset.modus; S.zoom=1; S.px=S.py=0; wrap.querySelectorAll('[data-modus]').forEach(x=>x.setAttribute('aria-pressed',x===b)); if(S.modus==='scheibe') S.spin=false; legende(); zeichne(); });
  $('[data-d3]',wrap).onclick=()=>scheibe3d();
  wrap.querySelectorAll('[data-auf]').forEach(b=>b.onclick=()=>{ const a=b.dataset.auf, an=!wrap.classList.contains('qwk-'+a+'-auf'); wrap.classList.remove('qwk-ebenen-auf','qwk-info-auf'); if(an) wrap.classList.add('qwk-'+a+'-auf'); });
  wrap.querySelectorAll('[data-zu]').forEach(b=>b.onclick=()=>wrap.classList.remove('qwk-ebenen-auf','qwk-info-auf'));
  $('.qwk-leg',wrap).onclick=()=>{ wrap.classList.remove('qwk-info-auf'); wrap.classList.toggle('qwk-ebenen-auf'); };
  const sb=$('[data-spin]',wrap); if(sb) sb.onclick=()=>{ S.spin=!S.spin&&S.modus==='globus'; sb.setAttribute('aria-pressed',S.spin); };
  wrap.querySelectorAll('[data-z]').forEach(b=>b.onclick=()=>{ const z=+b.dataset.z; S.spin=false; schwungAus(); if(!z){ ZT=null; S.zoom=1; S.px=S.py=0; zeichne(); } else zoomZu((ZT||S.zoom)*z); });
  $('[data-pflanze]',wrap).onchange=e=>{ S.pflanze=e.target.value; if(S.pflanze){ const P=PFL[S.pflanze]; flieg(P[0][0],P[0][1]); } zeichne(); };
  $('[data-epoche]',wrap).onchange=e=>{ S.epoche=e.target.value; zeichne(); };
  const rg=$('.qwk-zeit input',wrap), jl=$('.qwk-jahr',wrap); rg.oninput=()=>{ S.jahr=+rg.value; jl.textContent=S.jahr; zeichne(); info(); };
  let spiel=null; $('.qwk-play',wrap).onclick=e=>{ const b=e.currentTarget; if(spiel){ clearInterval(spiel); spiel=null; b.textContent='▶'; return; } b.textContent='❚❚'; if(S.jahr>=2023) S.jahr=1960; spiel=setInterval(()=>{ S.jahr++; rg.value=S.jahr; jl.textContent=S.jahr; zeichne(); info(); if(S.jahr>=2023){ clearInterval(spiel); spiel=null; b.textContent='▶'; } },160); };
  $('.qwk-such input',wrap).onchange=e=>{ const v=e.target.value.trim().toLowerCase(); const c=DAT.laender.find(c=>c.n.toLowerCase()===v); if(c){ waehle(c,c.lp); flieg(c.lp[0],c.lp[1]); return; }
    const st=DAT.staedte.find(s=>s[0].toLowerCase()===v); if(st){ S.ov.staedte=true; const cc=landAn(st[1],st[2]); if(cc) waehle(cc,[st[1],st[2]]); flieg(st[1],st[2],Math.max(S.zoom,4)); return; }
    const id=Object.keys(PFL).find(id=>pname(id).toLowerCase()===v); if(id){ S.pflanze=id; $('[data-pflanze]',wrap).value=id; S.ov.pfl=true; flieg(PFL[id][0][0],PFL[id][0][1]); zeichne(); } };
  const m=$('.qwk-map',wrap), P=new Map(); let start=null, d0=0, z0=1, bewegt=false;
  let vx=0, vy=0, lt=0, lx=0, ly=0;
  m.addEventListener('pointerdown',e=>{ if(e.target.closest('.qwk-zoom,.qwk-leg')) return; m.setPointerCapture(e.pointerId); P.set(e.pointerId,[e.clientX,e.clientY]); S.spin=false; { const sb=$('[data-spin]',wrap); if(sb) sb.setAttribute('aria-pressed',false); } bewegt=false; schwungAus(); ZT=null; vx=vy=0; lt=e.timeStamp; lx=e.clientX; ly=e.clientY; wrap.classList.remove('qwk-ebenen-auf'); start={x:e.clientX,y:e.clientY,lam:S.lam,phi:S.phi,px:S.px,py:S.py}; if(P.size===2){ const [a,b]=[...P.values()]; d0=Math.hypot(a[0]-b[0],a[1]-b[1]); z0=S.zoom; } });
  m.addEventListener('pointermove',e=>{ if(!P.has(e.pointerId)) return; P.set(e.pointerId,[e.clientX,e.clientY]);
    if(P.size===2){ const [a,b]=[...P.values()]; S.zoom=zgrenz(z0*Math.hypot(a[0]-b[0],a[1]-b[1])/(d0||1)); bewegt=true; vx=vy=0; neu(); return; }
    const dx=e.clientX-start.x, dy=e.clientY-start.y; if(Math.hypot(dx,dy)>4) bewegt=true; if(!bewegt) return;
    const jt=e.timeStamp, dt=jt-lt; if(dt>4){ const g=Math.min(1,dt/60); vx=vx*(1-g)+(e.clientX-lx)/dt*g; vy=vy*(1-g)+(e.clientY-ly)/dt*g; lt=jt; lx=e.clientX; ly=e.clientY; }
    if(S.modus==='globus'){ const f=57/radius(); S.lam=start.lam-dx*f; S.phi=Math.max(-85,Math.min(85,start.phi+dy*f)); } else { S.px=start.px+dx; S.py=start.py+dy; }
    neu(); });
  const ende=e=>{ if(!P.has(e.pointerId)) return; const mehr=P.size>1; P.delete(e.pointerId); if(P.size===1){ const [q]=[...P.values()]; start={x:q[0],y:q[1],lam:S.lam,phi:S.phi,px:S.px,py:S.py}; vx=vy=0; lt=e.timeStamp; lx=q[0]; ly=q[1]; }
    if(bewegt&&P.size===0&&!mehr&&e.type==='pointerup'&&e.timeStamp-lt<120) schwung(vx,vy);
    if(!bewegt&&P.size===0){ const r=m.getBoundingClientRect(), x=e.clientX-r.left, y=e.clientY-r.top; const h=histAn(x,y); if(h){ S.hist=h; S.sel=null; info(); zeichne(); wrap.classList.add('qwk-info-auf'); return; } const ll=inv(x,y); if(ll&&GRUND[S.grund].de){ const b=blAn(ll[0],ll[1]); if(b){ S.bl=b.i; S.sel=null; S.hist=null; info(); zeichne(); wrap.classList.add('qwk-info-auf'); return; } } if(ll){ const c=landAn(ll[0],ll[1]); S.hist=null; S.bl=null; if(c) waehle(c,ll); else { S.sel=null; S.klick=null; info(); zeichne(); } } } };
  m.addEventListener('pointerup',ende); m.addEventListener('pointercancel',ende);
  m.addEventListener('wheel',e=>{ e.preventDefault(); S.spin=false; schwungAus(); zoomZu((ZT||S.zoom)*Math.exp(-Math.max(-120,Math.min(120,e.deltaY))*0.0022)); },{passive:false});
  m.addEventListener('dblclick',e=>{ if(e.target.closest('.qwk-zoom,.qwk-leg')) return; e.preventDefault(); zoomZu((ZT||S.zoom)*2); });
  m.addEventListener('keydown',e=>{ const k=e.key, sch=18/Math.sqrt(S.zoom); let ok=true; schwungAus();
    if(k==='+'||k==='=') zoomZu((ZT||S.zoom)*1.5); else if(k==='-') zoomZu((ZT||S.zoom)/1.5); else if(k==='0'){ ZT=null; S.zoom=1; S.px=S.py=0; zeichne(); }
    else if(k==='ArrowLeft'||k==='ArrowRight'){ const v=k==='ArrowLeft'?-1:1; if(S.modus==='globus'||S.modus==='flach') S.lam+=v*sch; else S.px-=v*40; S.spin=false; neu(); }
    else if(k==='ArrowUp'||k==='ArrowDown'){ const v=k==='ArrowUp'?1:-1; if(S.modus==='globus') S.phi=Math.max(-85,Math.min(85,S.phi+v*sch)); else S.py+=v*40; S.spin=false; neu(); }
    else ok=false; if(ok) e.preventDefault(); });
  if(!window.QWWELT_RS){ window.QWWELT_RS=true; let rt=0; addEventListener('resize',()=>{ clearTimeout(rt); rt=setTimeout(()=>{ if(wrap&&document.body.contains(wrap)) groesse(); },80); }); }
}
function grundSetzen(k){ S.grund=k; wrap.querySelectorAll('[data-grund]').forEach(x=>x.setAttribute('aria-pressed',x.dataset.grund===k)); if(GRUND[k].de){ S.sel=null; S.hist=null; if(S.zoom<5) flieg(10.4,51.2,W<700?6.5:7.5); } else S.bl=null; legende(); zeichne(); info(); }
function waehle(c,ll){ S.sel=c.i; S.klick=ll; S.hist=null; info(); zeichne(); wrap.classList.add('qwk-info-auf'); wrap.classList.remove('qwk-ebenen-auf'); }
function flieg(lon,lat,zz){ S.spin=false; if(S.modus==='scheibe'){ if(zz) S.zoom=zz; const r=(90-lat)/180*rd(), a=(lon-S.lam)*R2; S.px=-r*Math.sin(a); S.py=-r*Math.cos(a); zeichne(); return; } if(S.modus!=='globus'){ S.lam=lon; S.px=0; S.py=lat*kf(); zeichne(); return; } const a={l:S.lam,p:S.phi,z:S.zoom}, b={l:lon,p:Math.max(-60,Math.min(60,lat)),z:zz||Math.max(S.zoom,1.5)}; let dl=((b.l-a.l+540)%360)-180; const t0=performance.now();
  schwungAus(); ZT=null; const weit=Math.hypot(dl*Math.cos((a.p+b.p)/2*R2),b.p-a.p), dauer=RUHE()?1:Math.min(1500,650+weit*7), tal=Math.min(a.z,b.z), hub=weit>25&&tal>1.3?Math.min(.7,weit/160):0;
  (function st(t){ const k=Math.min(1,(t-t0)/dauer), e=k<.5?4*k*k*k:1-Math.pow(-2*k+2,3)/2; S.lam=a.l+dl*e; S.phi=a.p+(b.p-a.p)*e; S.zoom=Math.exp(Math.log(a.z)+(Math.log(b.z)-Math.log(a.z))*e)*(1-hub*Math.sin(Math.PI*k)*(1-1/tal)); S.bewegt=k<1; zeichne(k>=1); if(k<1&&document.body.contains(wrap)) requestAnimationFrame(st); })(t0); }
/* ---------- 3D-Scheibe (three.js, wird erst beim Klick geladen) ---------- */
let D3=null;
function bildDaten(id){ return new Promise((res,rej)=>{ const el=document.getElementById(id); if(!el) return rej(new Error(id+' fehlt')); const im=new Image(); im.onload=()=>{ const c=document.createElement('canvas'); c.width=im.width; c.height=im.height; const x=c.getContext('2d'); x.drawImage(im,0,0); res({d:x.getImageData(0,0,c.width,c.height).data,w:c.width,h:c.height}); }; im.onerror=rej; im.src='data:image/jpeg;base64,'+el.textContent.trim(); }); }
function ladeSkript(src,ok){ return new Promise(res=>{ if(ok()) return res(); const s=document.createElement('script'); s.src=src; s.onload=()=>res(); s.onerror=()=>{ s.remove(); res(); }; document.head.appendChild(s); }); }
async function dreiLaden(){
  try{ const T=await import('three'); const O=await import('three/addons/controls/OrbitControls.js'); return {T,OC:O.OrbitControls}; }
  catch(e){ console.warn('three (Modul) nicht geladen, versuche lib/',e); }
  if(!(window.THREE&&THREE.WebGLRenderer)) await ladeSkript('lib/three.min.js',()=>window.THREE&&THREE.WebGLRenderer);
  if(window.THREE&&!THREE.OrbitControls) await ladeSkript('lib/OrbitControls.js',()=>window.THREE.OrbitControls);
  if(window.THREE&&THREE.WebGLRenderer) return {T:window.THREE,OC:THREE.OrbitControls||null};
  throw new Error('three.js nicht verfügbar');
}
const AUSSEN={
  kuppel:{n:'Kuppelrand',t:'<b>Nach Darstellung mancher Vertreter</b> endet die Welt am Eisring: Dort setzt die Himmelskuppel (das Firmament) auf. Sonne und Mond kreisen als Leuchten darunter, die Sterne sitzen an der Kuppel, der Polarstern genau über dem Nordpol. <b>Gängige Darstellung:</b> Eine feste Kuppel wurde nie beobachtet; Raumstationen (ISS, rund 400 km Höhe) und Sonden wie Voyager 1 (über 24 Mrd. km entfernt) bewegen sich ungehindert. Sterne zeigen messbare jährliche Parallaxen (Gaia: über 1 Mrd. Sterne) und stehen damit unterschiedlich weit entfernt.'},
  wasser:{n:'Wasser über der Feste',t:'<b>Nach Darstellung mancher Vertreter</b>, die sich auf 1. Mose 1,6–8 berufen, liegen über der festen Himmelskuppel („Feste“) weitere Wasser; manche verbinden damit die „Fenster des Himmels“ der Sintflut-Erzählung (1. Mose 7,11). <b>Gängige Darstellung:</b> Die Stelle spiegelt das altorientalische Weltbild wider. Wetterballone (bis etwa 40 km), Raketen und Satelliten durchqueren die Lufthülle; Wasserdampf findet sich fast nur in den unteren rund 10–15 km, darüber folgt nahezu leerer Raum.'},
  laender:{n:'Weitere Länder',t:'<b>Nach Darstellung mancher Vertreter</b> (z. B. Mark Sargent) liegen hinter einem breiten Eisgürtel weitere, unerforschte Länder, teils von einem zweiten Eisring umschlossen; sie berufen sich u. a. auf Admiral Byrd (Operation Highjump 1946/47). <b>Gängige Darstellung:</b> Byrd meinte Gebiete auf dem antarktischen Kontinent selbst; Weltumsegelungen und polar umlaufende Satelliten, die beide Pole täglich rund 14-mal überqueren, zeigen keine weiteren Kontinente. Land und Meer hier sind frei erzeugt – ohne Namen, nicht belegt.'},
  eis:{n:'Endloses Eis',t:'<b>Nach Darstellung mancher Vertreter</b> folgt hinter der Wand endloses Eis, das niemand durchquert habe; der Antarktisvertrag (1959) sperre den Zugang. <b>Gängige Darstellung:</b> Die Antarktis ist ein Kontinent von rund 14 Mio. km². Sie wurde mehrfach durchquert, erstmals 1957/58 von der Commonwealth-Transantarktis-Expedition (Fuchs, Hillary); am Südpol steht seit 1956/57 die Amundsen-Scott-Station, 2023/24 kamen ca. 120 000 Besucher (IAATO).'},
  saeulen:{n:'Säulen',t:'<b>Nach Darstellung mancher Vertreter</b> ruht die Scheibe auf Säulen oder Grundfesten; sie berufen sich auf Bibelstellen wie 1. Samuel 2,8, Hiob 9,6 oder Psalm 75,4, die von „Säulen“ bzw. „Pfeilern“ der Erde sprechen. Was darunter liegt, bleibt offen. <b>Gängige Darstellung:</b> Erdbebenwellen durchlaufen den ganzen Erdkörper und zeigen Kruste, Mantel sowie einen flüssigen äußeren und festen inneren Kern; die tiefste Bohrung (Kola, 12,26 km) blieb in der Kruste.'}};
const WAND3D='<b>Zur Eiswand – gängige Darstellung:</b> James Clark Ross beschrieb 1841 die nach ihm benannte Eisbarriere (heute Ross-Schelfeis) als senkrechte Eisklippe von etwa 150–200 Fuß (rund 45–60 m) Höhe; ihre Abbruchkante ist über 600 km lang. Solche Schelfeiskanten säumen Teile der antarktischen Küste.';
const CSS3D=`.qwk-3d{position:fixed;inset:0;z-index:9000;background:#03060f;color:#e8eefb;font:14px system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;touch-action:none}
.qwk-3d canvas{display:block;width:100%;height:100%;outline:none}
.qwk-3d .k3-bar{position:absolute;top:12px;left:12px;right:12px;display:flex;flex-wrap:wrap;gap:8px;align-items:center;pointer-events:none}
.qwk-3d .k3-bar>*,.qwk-3d .k3-info{pointer-events:auto}
.qwk-3d .k3-t{font:700 17px Georgia,serif;padding:7px 14px;border-radius:12px;background:rgba(8,14,28,.72);border:1px solid #1f2b44;backdrop-filter:blur(6px)}
.qwk-3d .k3-t small{display:block;font:500 11px system-ui;color:#8d9ab8}
.qwk-3d button,.qwk-3d label{all:unset;cursor:pointer;padding:8px 12px;border-radius:11px;background:rgba(8,14,28,.72);border:1px solid #1f2b44;color:#cfe0ff;font-weight:600;font-size:13px;backdrop-filter:blur(6px);display:inline-flex;align-items:center;gap:6px}
.qwk-3d button[aria-pressed=true]{background:linear-gradient(180deg,#24363f,#1a2a32);color:#fff;border-color:#2e5b8a}
.qwk-3d .k3-zu{margin-left:auto;width:20px;justify-content:center;font-size:16px}
.qwk-3d input[type=range]{width:110px;accent-color:#9fcf8a}
.qwk-3d .k3-uhr{font-variant-numeric:tabular-nums;color:#ffd860}
.qwk-3d .k3-info{position:absolute;left:12px;bottom:12px;width:min(470px,calc(100% - 24px));box-sizing:border-box;padding:11px 13px;border-radius:14px;background:rgba(8,14,28,.8);border:1px solid #1f2b44;color:#b4c0da;font-size:12.5px;line-height:1.45;backdrop-filter:blur(8px)}
.qwk-3d .k3-info h4{display:flex;align-items:center;margin:0 0 7px;font:600 11px system-ui;letter-spacing:.08em;text-transform:uppercase;color:#8d9ab8}
.qwk-3d .k3-seg{display:flex;flex-wrap:wrap;gap:4px;margin-bottom:8px}
.qwk-3d .k3-seg button{padding:6px 10px;font-size:12.5px}
.qwk-3d .k3-info p{margin:0 0 6px}.qwk-3d .k3-info b{color:#e8eefb;font-weight:600}
.qwk-3d .k3-info small{display:block;color:#7d8aa8;font-size:11.5px}
.qwk-3d .k3-info a{color:#9fcf8a}
.qwk-3d .k3-klapp{margin-left:auto;padding:1px 9px!important;font-size:13px!important}.qwk-3d .k3-info.zu p,.qwk-3d .k3-info.zu small{display:none}.qwk-3d .k3-info.zu .k3-seg{margin-bottom:0}
.qwk-3d .k3-kam{position:fixed;right:12px;bottom:12px;display:flex;flex-direction:column;gap:6px}.qwk-3d .k3-kam button{justify-content:flex-start}
.qwk-3d .k3-bar label b{font-weight:600}.qwk-3d .k3-info .k3-wand{color:#9aa7c2;font-size:12px;margin:0 0 6px}.qwk-3d .k3-info summary{cursor:pointer;color:#cfe0ff;font-weight:600}.qwk-3d .k3-info .k3-opt{padding:5px 10px;font-size:12px;margin:0 0 7px}.qwk-3d .k3-info.zu .k3-wand,.qwk-3d .k3-info.zu .k3-opt{display:none!important}
.qwk-3d .k3-lade{position:absolute;inset:0;display:grid;place-items:center;color:#8d9ab8;font-size:15px;pointer-events:none}
@media (max-width:700px){.qwk-3d .k3-t{font-size:15px}.qwk-3d button,.qwk-3d label{padding:7px 9px;font-size:12px}.qwk-3d input[type=range]{width:80px}.qwk-3d .k3-info{font-size:11.5px;padding:9px 11px;max-height:46vh;overflow:auto}.qwk-3d .k3-info p{margin-bottom:4px}.qwk-3d .k3-t small,.qwk-3d .k3-bar>button span,.qwk-3d .k3-bar>label>span{display:none}.qwk-3d .k3-t{padding:6px 11px}.qwk-3d .k3-kam{position:static;flex-direction:row;flex-wrap:wrap;flex-basis:100%;gap:5px}.qwk-3d .k3-kam button{padding:6px 8px;font-size:11.5px}.qwk-3d .k3-seg button{padding:5px 8px;font-size:11.5px}}`;
function scheibe3dZu(){ if(!D3) return; const d=D3; D3=null; d.aus=true; cancelAnimationFrame(d.raf); removeEventListener('resize',d.rs); removeEventListener('keydown',d.kd);
  try{ d.ctl&&d.ctl.dispose(); }catch(e){} if(d.sc) d.sc.traverse(o=>{ if(o.geometry) o.geometry.dispose(); const m=o.material; (Array.isArray(m)?m:m?[m]:[]).forEach(x=>{ for(const k in x){ const v=x[k]; if(v&&v.isTexture) v.dispose(); } x.dispose(); }); });
  if(d.r){ d.r.dispose(); try{ d.r.forceContextLoss(); }catch(e){} } d.el.remove(); if(location.hash==='#welt-scheibe3d') history.replaceState(null,'','#welt-scheibe'); }
/* kleines Wertrauschen für Eis und Landformen */
function hs3(i,j){ let h=(i*374761393+j*668265263)|0; h=(h^(h>>>13))*1274126177; return ((h^(h>>>16))>>>0)/4294967295; }
function rs3(x,y){ const xi=Math.floor(x), yi=Math.floor(y), u=x-xi, v=y-yi, a=u*u*(3-2*u), b=v*v*(3-2*v); return (hs3(xi,yi)*(1-a)+hs3(xi+1,yi)*a)*(1-b)+(hs3(xi,yi+1)*(1-a)+hs3(xi+1,yi+1)*a)*b; }
function fk3(a,f,y,o){ const k=f/6.2832; return fb3(Math.cos(a)*k+y*1.7+11,Math.sin(a)*k-y*1.3+5,o); }
function fb3(x,y,o){ let s=0,f=1,m=0.5,n=0; for(let i=0;i<o;i++){ s+=m*rs3(x*f+i*17.3,y*f-i*9.1); n+=m; f*=2.03; m*=0.5; } return s/n; }
async function scheibe3d(){
  if(D3||!wrap) return; const el=document.createElement('div'); el.className='qwk-3d';
  el.innerHTML=`<style>${CSS3D}</style><div class="k3-lade">3D-Scheibe wird geladen …</div><div class="k3-bar"><div class="k3-t">⛰ 3D-Scheibe<small>Relief der Erde im Scheibenmodell</small></div><button data-k3="wasser" aria-pressed="true" title="Wasser">💧<span>Wasser</span></button><button data-k3="namen" aria-pressed="true" title="Namen und Kreise">Aa<span>Namen</span></button><button data-k3="wolken" aria-pressed="false" title="Wolken">☁<span>Wolken</span></button><button data-k3="raffer" aria-pressed="false" title="Tag im Zeitraffer">▶<span>Tag im Zeitraffer</span></button><label title="Überhöhung der Höhen"><span>Höhe</span><input type="range" min="10" max="120" value="40" data-k3="hoch"><b data-k3="hw">40×</b></label><span class="k3-uhr" data-k3="uhr"></span><button class="k3-zu" data-k3="zu" aria-label="Schließen">✕</button><div class="k3-kam" role="group" aria-label="Kamera">${[['oben','⊙','Von oben'],['eisrand','◠','Am Eisrand'],['aussen','◎','Von außen'],['rund','⟳','Rundflug']].map(([k,i,t])=>`<button data-kam="${k}" title="${t}"${k==='rund'?' aria-pressed="false"':''}>${i} ${t}</button>`).join('')}</div></div>
  <div class="k3-info"><h4>Hinter der Eiswand<button class="k3-klapp" data-k3="klapp" aria-expanded="true" aria-label="Infotafel ein- oder ausklappen">▾</button></h4><div class="k3-seg">${Object.entries(AUSSEN).map(([k,v])=>`<button data-aus="${k}" aria-pressed="${k==='kuppel'}">${v.n}</button>`).join('')}</div><p data-k3="txt">${AUSSEN.kuppel.t}</p><button class="k3-opt" data-k3="kuppelz" aria-pressed="true">◠ Kuppel zeigen</button><details class="k3-wand"><summary>Zur Eiswand: Ross 1841</summary>${WAND3D}</details><small>Darstellung nach dem Flache-Erde-Modell, Höhen stark überhöht. Vergleich im Kapitel <a href="#w-erdform">W-12</a>. Ziehen = drehen, Mausrad/zwei Finger = zoomen, rechte Taste/zwei Finger = verschieben.</small></div>`;
  wrap.appendChild(el); const d=D3={el,aus:false,raf:0}; const q=s=>el.querySelector(`[data-k3="${s}"]`);
  q('zu').onclick=scheibe3dZu; el.querySelector('.k3-info a').onclick=()=>scheibe3dZu(); d.kd=e=>{ if(e.key==='Escape') scheibe3dZu(); }; addEventListener('keydown',d.kd);
  let L,HB,RB; try{ [L,HB,RB]=await Promise.all([dreiLaden(),bildDaten('welthoehe'),TEX?Promise.resolve({d:TEX,w:TW,h:TH}):bildDaten('weltrelief')]); }
  catch(e){ console.warn(e); el.querySelector('.k3-lade').textContent='3D-Ansicht nicht verfügbar (three.js konnte nicht geladen werden).'; return; }
  if(d.aus) return; el.querySelector('.k3-lade').remove();
  const T=L.T, KERNE=navigator.hardwareConcurrency||4, RAM=navigator.deviceMemory||8, mobil=Math.min(innerWidth,innerHeight)<700||/Mobi|Android|iPhone|iPad/i.test(navigator.userAgent);
  /* Qualitätsstufe: 0 = sparsam, 1 = mittel (Handy), 2 = hoch (Desktop) */
  const Q=/[?&]hoch/.test(location.search)?2:(!mobil&&KERNE>4&&RAM>3)?2:(KERNE>=6&&RAM>=4)?1:0, klein=Q<2, RD=10, NR=[130,200,300][Q], NS=[260,400,600][Q], R2D=Math.PI/180;
  /* Renderer & Szene */
  const r=d.r=new T.WebGLRenderer({antialias:Q>0,powerPreference:'high-performance'}); r.setPixelRatio(Math.min([1.25,1.5,2][Q],devicePixelRatio||1));
  if('outputColorSpace' in r) r.outputColorSpace=T.SRGBColorSpace; else r.outputEncoding=T.sRGBEncoding;
  r.toneMapping=T.ACESFilmicToneMapping; r.toneMappingExposure=1.08; if(Q===2){ r.shadowMap.enabled=true; r.shadowMap.type=T.PCFShadowMap; } el.insertBefore(r.domElement,el.firstChild);
  const sc=d.sc=new T.Scene(); sc.background=new T.Color(0x03060f); sc.fog=new T.FogExp2(0x03060f,0.006);
  const cam=new T.PerspectiveCamera(38,1,0.1,1500); cam.position.set(0,13.5,17.5); d.cam=cam;
  const srgb=t=>{ if('colorSpace' in t) t.colorSpace=T.SRGBColorSpace; else t.encoding=T.sRGBEncoding; return t; };
  const mat=(o)=>{ const m=new T.MeshStandardMaterial(o); return m; };
  /* Eigenleuchten aus der Grundfarbe, damit Eis und Länder auch abseits der Sonne Farbe zeigen */
  const selbst=(m,k)=>{ m.onBeforeCompile=sh=>{ sh.fragmentShader=sh.fragmentShader.replace('#include <emissivemap_fragment>','#include <emissivemap_fragment>\n totalEmissiveRadiance+=diffuseColor.rgb*'+k.toFixed(3)+';'); }; m.customProgramCacheKey=()=>'qwselbst'+k; return m; };
  /* Höhenkarte (bilinear) in Kilometern */
  const hoehe=(lon,lat)=>{ const x=((lon+180)/360*HB.w-0.5+HB.w)%HB.w, y=Math.max(0,Math.min(HB.h-1.001,(90-lat)/180*HB.h-0.5)); const x0=Math.floor(x), y0=Math.floor(y), fx=x-x0, fy=y-y0, x1=(x0+1)%HB.w;
    const g=(a,b)=>HB.d[(b*HB.w+a)*4]; const v=(g(x0,y0)*(1-fx)+g(x1,y0)*fx)*(1-fy)+(g(x0,y0+1)*(1-fx)+g(x1,y0+1)*fx)*fy;
    return v>=128?0.04+Math.max(0,v-129)/126*8.8:-Math.max(0.05,(126-v)/13.5+0.1); };
  /* Scheibe als radiales Gitter */
  const nv=1+NR*NS, pos=new Float32Array(nv*3), uv=new Float32Array(nv*2), hk=new Float32Array(nv);
  const setz=(i,rr,a,lat,lon)=>{ const x=rr*Math.sin(a), z=rr*Math.cos(a); pos[i*3]=x; pos[i*3+2]=z; uv[i*2]=x/RD*0.5+0.5; uv[i*2+1]=0.5-z/RD*0.5; hk[i]=hoehe(lon,lat); };
  setz(0,0,0,90,0);
  for(let i=1;i<=NR;i++) for(let j=0;j<NS;j++){ const a=j/NS*2*Math.PI; setz(1+(i-1)*NS+j,RD*i/NR,a,90-180*i/NR,((a/R2D+540)%360)-180); }
  const idx=new Uint32Array(NS*3+(NR-1)*NS*6); let ii=0; for(let j=0;j<NS;j++){ idx[ii++]=0; idx[ii++]=1+j; idx[ii++]=1+(j+1)%NS; }
  for(let i=1;i<NR;i++){ const o=1+(i-1)*NS, n=o+NS; for(let j=0;j<NS;j++){ const j1=(j+1)%NS; idx[ii++]=o+j; idx[ii++]=n+j; idx[ii++]=n+j1; idx[ii++]=o+j; idx[ii++]=n+j1; idx[ii++]=o+j1; } }
  const geo=new T.BufferGeometry(); geo.setAttribute('position',new T.BufferAttribute(pos,3)); geo.setAttribute('uv',new T.BufferAttribute(uv,2)); geo.setIndex(new T.BufferAttribute(idx,1));
  const KM=1/2000; let ueber=40;
  /* Farbtextur (azimutal, bilinear) + Detail-Normalenkarte aus der Höhenkarte */
  const TS=[1024,1536,2048][Q], tc=document.createElement('canvas'); tc.width=tc.height=TS; const tx=tc.getContext('2d'), id=tx.createImageData(TS,TS), od=id.data, HT=new Float32Array(TS*TS);
  const RW=RB.w, RH=RB.h, rd_=RB.d;
  for(let py=0;py<TS;py++){ const dz=(py+0.5)/TS*2-1; for(let px=0;px<TS;px++){ const dx=(px+0.5)/TS*2-1, rr=Math.min(1,Math.hypot(dx,dz)); const lat=90-rr*180, lon=Math.atan2(dx,dz)/R2D;
      let sx=(lon+180)/360*RW-0.5, sy=Math.max(0,Math.min(RH-1.001,(90-lat)/180*RH-0.5)); sx=(sx+RW)%RW; const x0=Math.floor(sx), y0=Math.floor(sy), fx=sx-x0, fy=sy-y0, x1=(x0+1)%RW, o=(py*TS+px)*4;
      const a=(y0*RW+x0)*4, b=(y0*RW+x1)*4, c=((y0+1)*RW+x0)*4, e=((y0+1)*RW+x1)*4;
      for(let k=0;k<3;k++) od[o+k]=(rd_[a+k]*(1-fx)+rd_[b+k]*fx)*(1-fy)+(rd_[c+k]*(1-fx)+rd_[e+k]*fx)*fy; od[o+3]=255; HT[py*TS+px]=hoehe(lon,lat); } }
  tx.putImageData(id,0,0); { const nb=glScheibenbild(TS); if(nb) tx.drawImage(nb,0,0,TS,TS); } const tex=srgb(new T.CanvasTexture(tc)); tex.anisotropy=Math.min(8,r.capabilities.getMaxAnisotropy()); tex.needsUpdate=true;
  const BL=new Float32Array(TS*TS), TMP=new Float32Array(TS*TS), BR=Q<2?2:3;
  for(let y=0;y<TS;y++){ let s=0; for(let x=-BR;x<=BR;x++) s+=HT[y*TS+Math.max(0,Math.min(TS-1,x))]; for(let x=0;x<TS;x++){ TMP[y*TS+x]=s/(2*BR+1); s+=HT[y*TS+Math.min(TS-1,x+BR+1)]-HT[y*TS+Math.max(0,x-BR)]; } }
  for(let x=0;x<TS;x++){ let s=0; for(let y=-BR;y<=BR;y++) s+=TMP[Math.max(0,Math.min(TS-1,y))*TS+x]; for(let y=0;y<TS;y++){ BL[y*TS+x]=s/(2*BR+1); s+=TMP[Math.min(TS-1,y+BR+1)*TS+x]-TMP[Math.max(0,y-BR)*TS+x]; } }
  const nc=document.createElement('canvas'); nc.width=nc.height=TS; const nx_=nc.getContext('2d'), nd=nx_.createImageData(TS,TS), ndd=nd.data, sp2=2*(2*RD/TS), kk=KM*40*2.2;
  const det=(x,y)=>{ x=Math.max(0,Math.min(TS-1,x)); y=Math.max(0,Math.min(TS-1,y)); const i=y*TS+x; return HT[i]-BL[i]; };
  for(let y=0;y<TS;y++) for(let x=0;x<TS;x++){ const gx=-(det(x+1,y)-det(x-1,y))/sp2*kk, gy=(det(x,y+1)-det(x,y-1))/sp2*kk, l=Math.hypot(gx,gy,1), o=(y*TS+x)*4; ndd[o]=(gx/l*0.5+0.5)*255; ndd[o+1]=(gy/l*0.5+0.5)*255; ndd[o+2]=(1/l*0.5+0.5)*255; ndd[o+3]=255; }
  nx_.putImageData(nd,0,0); const ntex=new T.CanvasTexture(nc); ntex.needsUpdate=true;
  const bodenM=mat({map:tex,normalMap:ntex,roughness:0.9,metalness:0}); const boden=new T.Mesh(geo,bodenM); boden.receiveShadow=true; boden.castShadow=true; sc.add(boden);
  const hochSetzen=()=>{ const k=KM*ueber; for(let i=0;i<nv;i++) pos[i*3+1]=hk[i]*k; geo.attributes.position.needsUpdate=true; geo.computeVertexNormals(); geo.computeBoundingSphere(); bodenM.normalScale.set(ueber/40,ueber/40); };
  hochSetzen();
  /* Wasserfläche */
  const wM=new T.MeshPhongMaterial({color:0x1a5a8e,specular:0xcfe2f6,shininess:140,transparent:true,opacity:glAn()?0.2:0.34,depthWrite:false});
  wM.onBeforeCompile=sh=>{ sh.fragmentShader=sh.fragmentShader.replace('#include <dithering_fragment>','#include <dithering_fragment>\n float qwFr=pow(1.0-abs(dot(normalize(vViewPosition),normal)),3.0); gl_FragColor.rgb+=vec3(.10,.18,.30)*qwFr; gl_FragColor.a=min(1.0,gl_FragColor.a+qwFr*0.4);'); }; wM.customProgramCacheKey=()=>'qwwasser';
  const wasser=new T.Mesh(new T.CircleGeometry(RD*1.004,256),wM); wasser.rotation.x=-Math.PI/2; wasser.position.y=0; sc.add(wasser);
  /* ---------- Eiswand: Eisklippe mit Abbruchkanten, Schichtung, Hohlkehle, Spalten und Schneekrone ---------- */
  const NA=[720,1200,2160][Q], FR=[18,24,32][Q], TR=[12,16,22][Q], OR=6, R0=RD*1.002, RA=RD*1.15, YB=-0.32, YO=0.17, TAU=2*Math.PI;
  const gl3=(a,b,x)=>{ const t=Math.max(0,Math.min(1,(x-a)/(b-a))); return t*t*(3-2*t); }, saw=x=>x-Math.floor(x), misch=(a,b,m)=>a.map((v,i)=>v*(1-m)+b[i]*m);
  let sd=20250; const zuf=()=>{ sd=(sd*16807)%2147483647; return (sd-1)/2147483646; };
  const spalt=a=>{ let s=0; for(const [f,o,w] of [[37,0.3,0.06],[71,1.7,0.045],[113,4.1,0.035]]){ const t=(a*f/TAU+o+0.25*fk3(a,5,o,1)+10)%1; s=Math.max(s,Math.max(0,1-Math.abs(t-0.5)/w)); } return s*s; };
  const kante=a=>{ const f1=saw(a*47/TAU+1.4*fk3(a,3,2.2,2)), f2=saw(a*173/TAU+0.9*fk3(a,5,6.1,1)); return 0.09*fk3(a,7,4.1,3)+0.04*fk3(a,26,8.3,2)+0.035*f1*f1*gl3(0.35,0.7,fk3(a,11,3.3,2))+0.012*f2*gl3(0.4,0.6,fk3(a,17,5.5,1)); };
  const RISSE=[[29,0.13],[47,0.61],[97,0.37],[151,0.82]].filter(([f])=>f*12<=NA);
  const riss=a=>{ let s=0, l=0; for(const [f,o] of RISSE){ const w=Math.max(0.05,1.5*f/NA), t=saw(a*f/TAU+o+0.25*fk3(a,4,o*3,1)), v=Math.max(0,1-Math.abs(t-0.5)/w); if(v>s&&fk3(a,9,o*7,1)>0.42){ s=v; l=0.3+0.55*fk3(a,13,o*5,1); } } return [s,l]; };
  const hoeheW=a=>0.74+0.3*fk3(a,4,1.3,3)+0.12*fk3(a,22,7.7,2)-0.1*Math.sqrt(spalt(a));
  /* bläuliches Durchscheinen: dunkle, blaue Stellen und streifender Blick leuchten leicht nach */
  const eisLicht=(m,k)=>{ m.onBeforeCompile=sh=>{ sh.fragmentShader=sh.fragmentShader.replace('#include <emissivemap_fragment>','#include <emissivemap_fragment>\n{ float qL=dot(diffuseColor.rgb,vec3(.299,.587,.114)); float qF=pow(1.0-abs(dot(normal,normalize(vViewPosition))),2.0); totalEmissiveRadiance+=diffuseColor.rgb*'+k.toFixed(3)+'+vec3(.03,.15,.30)*(1.0-qL)*.8+vec3(.05,.14,.28)*qF*.4; }'); }; m.customProgramCacheKey=()=>'qweis'+k; return m; };
  const tiefF=[0.08,0.30,0.55], mittel=[0.42,0.70,0.86], hell=[0.90,0.96,1.0];
  const rows=1+(FR+1)+TR+OR, nW=(NA+1)*rows, wP=new Float32Array(nW*3), wC=new Float32Array(nW*3), wU=new Float32Array(nW*2); let wo=0, wu=0, uA=0;
  const wPush=(rr,y,sa,ca,c,v)=>{ wP[wo]=rr*sa; wP[wo+1]=y; wP[wo+2]=rr*ca; wC[wo]=c[0]; wC[wo+1]=c[1]; wC[wo+2]=c[2]; wo+=3; wU[wu++]=uA; wU[wu++]=v; };
  for(let j=0;j<=NA;j++){ uA=j/NA*40; const a=(j%NA)/NA*TAU, sa=Math.sin(a), ca=Math.cos(a), ht=hoeheW(a), sv=spalt(a), rE=R0+kante(a), [rs,rl]=riss(a), tq=fk3(a,6,0.5,2), seg=Math.floor(saw(a/TAU)*183)%183;
    wPush(RD*0.97,YB-0.06,sa,ca,[0.05,0.16,0.3],0);
    let rTop=rE;
    for(let k=0;k<=FR;k++){ const t=k/FR, y=YB+(ht-YB)*t, li=Math.floor(y*16+fk3(a,9,y*3,2)*1.4), lage=li/16;
      const stufe=0.016*(fk3(a,48,li*0.73,1)-0.5), jag=0.05*fk3(a,14,y*2,3)+0.03*fk3(a,30,lage*9,2)+0.12*sv*(0.4+0.6*fk3(a,30,y*8,2));
      const kehle=0.045*Math.exp(-Math.pow((y-0.03)/0.06,2)), krone=-0.035*gl3(0.86,1,t)*(1-sv), rr=rE+jag+stufe+kehle+krone; rTop=rr;
      const band=0.5+0.5*Math.sin(y*52+3*fk3(a,12,y*2,2)), n=fk3(a,40,y*8,2);
      let c=misch(misch(tiefF,mittel,0.35+0.4*tq),hell,0.15+0.55*band*(0.6+0.4*n)); c=misch(c,tiefF,0.6*gl3(0.22,-0.12,y));
      if(sv>0.2) c=misch(c,[0.04,0.22,0.42],Math.min(1,sv*1.2)); if(t>0.88) c=misch(c,[0.97,0.98,1],(t-0.88)/0.12);
      wPush(rr,y,sa,ca,c,Math.min(0.86,(y-YB)/1.3*0.86)); }
    const r0=Math.max(R0+0.06,rTop+0.02);
    for(let k=1;k<=TR;k++){ const t=k/TR, rr=r0+(RA-r0)*t, cr=rs*(1-gl3(rl-0.15,rl,t)), sas=0.012*Math.sin(rr*55+a*31+4*fk3(a,60,t*3,1));
      const y=ht+0.07*Math.sin(Math.PI*Math.min(1,t*1.6))*(0.7+0.3*fk3(a,40,t*3,1))-(ht-YO)*Math.pow(t,1.6)+0.02*fk3(a,80,t*6,2)+sas*(1-t)-0.08*cr;
      const n=0.93+0.05*fk3(a,90,rr*20,1)+sas*2; let c=[n,n+0.012,1]; if(cr>0) c=misch(c,cr>0.7?[0.04,0.18,0.38]:[0.3,0.6,0.85],Math.min(1,cr*1.3));
      wPush(rr,y,sa,ca,c,0.95); }
    for(let k=0;k<OR;k++){ const t=k/(OR-1), y=YO-0.03-(YO-0.03+1.05)*t, rr=t<1?RA+0.035+0.04*fk3(a,18,t*4,2)*(1-t)+0.015*hs3(k,seg):RA+0.04;
      const band=0.5+0.5*Math.sin(y*30+2*fk3(a,9,y,2)); wPush(rr,y,sa,ca,misch(misch(tiefF,mittel,0.5),hell,0.25+0.45*band*(1-t)),Math.max(0,(y+1.05)/1.3*0.86)); } }
  const wi=new Uint32Array(NA*(rows-1)*6); let wq=0; for(let j=0;j<NA;j++) for(let k=0;k<rows-1;k++){ const a=j*rows+k, b=(j+1)*rows+k; wi[wq++]=a; wi[wq++]=a+1; wi[wq++]=b; wi[wq++]=b; wi[wq++]=a+1; wi[wq++]=b+1; }
  const wg=new T.BufferGeometry(); wg.setAttribute('position',new T.BufferAttribute(wP,3)); wg.setAttribute('color',new T.BufferAttribute(wC,3)); wg.setAttribute('uv',new T.BufferAttribute(wU,2)); wg.setIndex(new T.BufferAttribute(wi,1)); wg.computeVertexNormals();
  const eisT=(()=>{ const w=[256,512,512][Q], c=document.createElement('canvas'); c.width=c.height=w; const x=c.getContext('2d'), im=x.createImageData(w,w), D=im.data, P=TAU/w;
    for(let py=0;py<w;py++){ const v=1-py/w; for(let px=0;px<w;px++){ const wa=0.007*Math.sin(px*P*2+1.3)+0.004*Math.sin(px*P*5+v*9)+0.002*Math.sin(px*P*13);
      let g=0.9+0.05*Math.sin((v+wa)*170)+0.035*Math.sin((v+wa*1.7)*61+2)+0.03*(rs3((px%w)*0.11,py*0.05)-0.5); if(v>0.88) g=0.96+0.04*rs3(px*0.2,py*0.2); const o=(py*w+px)*4; D[o]=D[o+1]=D[o+2]=Math.max(0,Math.min(255,g*255)); D[o+3]=255; } }
    x.putImageData(im,0,0); x.lineCap='round';
    for(let i=0;i<16;i++){ const v=0.06+0.78*zuf(), y0=(1-v)*w, a1=zuf()*TAU, amp=2+zuf()*5; x.beginPath(); for(let px=0;px<=w;px+=4){ const y=y0+amp*Math.sin(px*P*2+a1)+1.5*Math.sin(px*P*7+a1*3); px?x.lineTo(px,y):x.moveTo(px,y); } x.lineWidth=0.8+zuf()*1.6; x.strokeStyle='rgba(70,120,170,'+(0.25+0.35*zuf()).toFixed(2)+')'; x.stroke(); }
    for(let i=0;i<9;i++){ const px0=zuf()*w, ya=(0.12+0.5*zuf())*w, yb=Math.min(0.88*w,ya+(0.15+0.5*zuf())*w); for(const dx of [0,w,-w]){ x.beginPath(); for(let y=ya;y<=yb;y+=6){ const px=px0+dx+3*Math.sin(y*0.08+i)+2*(hs3(i,y|0)-0.5); y===ya?x.moveTo(px,y):x.lineTo(px,y); } x.lineWidth=1.2+0.3*i%1.5; x.strokeStyle='rgba(40,85,140,.55)'; x.stroke(); } }
    const t=new T.CanvasTexture(c); t.wrapS=T.RepeatWrapping; t.wrapT=T.ClampToEdgeWrapping; t.anisotropy=Math.min(8,r.capabilities.getMaxAnisotropy()); return t; })();
  const wallM=eisLicht(new (T.MeshPhysicalMaterial||T.MeshStandardMaterial)({vertexColors:true,map:eisT,bumpMap:eisT,bumpScale:0.5,roughness:0.42,metalness:0,side:T.DoubleSide}),0.24); if('clearcoat' in wallM){ wallM.clearcoat=0.5; wallM.clearcoatRoughness=0.3; }
  const wall=new T.Mesh(wg,wallM); wall.castShadow=true; wall.receiveShadow=true; sc.add(wall);
  /* Sockel: Gesteinskörper unter Scheibe und Eisring (nur von unten/außen sichtbar) */
  const sockelY=rr=>-1.05-1.75*Math.pow(Math.max(0,1-Math.pow(rr/(RA+0.04),2)),0.7);
  { const nr=[14,22,30][Q], ns=[128,192,256][Q], Rb=RA+0.04, P=new Float32Array((nr+1)*(ns+1)*3), C=new Float32Array(P.length), I=[]; let o=0;
    for(let i=0;i<=nr;i++){ const rr=Rb*(1-i/nr); for(let j=0;j<=ns;j++){ const a=(j%ns)/ns*TAU, x=rr*Math.sin(a), z=rr*Math.cos(a), m=Math.min(1,(Rb-rr)*1.5), y=sockelY(rr)-0.32*m*fb3(x*0.45+3,z*0.45,4);
      const b=0.5+0.5*Math.sin(y*9+2*fb3(x*0.3,z*0.3,2)), g=0.15+0.1*b+0.06*fb3(x*2,z*2,2); P[o]=x; P[o+1]=y; P[o+2]=z; C[o]=g*1.05; C[o+1]=g*0.98; C[o+2]=g*0.92; o+=3; } }
    for(let i=0;i<nr;i++) for(let j=0;j<ns;j++){ const a=i*(ns+1)+j, b=a+ns+1; I.push(a,b,a+1, a+1,b,b+1); }
    const g=new T.BufferGeometry(); g.setAttribute('position',new T.BufferAttribute(P,3)); g.setAttribute('color',new T.BufferAttribute(C,3)); g.setIndex(I); g.computeVertexNormals();
    sc.add(new T.Mesh(g,selbst(mat({vertexColors:true,roughness:0.95,metalness:0,side:T.DoubleSide}),0.2))); }
  /* Eisberge (Tafeleisberge) und Treibeis im Südlichen Ozean vor dem Eisgürtel – instanziert */
  const EB=new T.Group(); sc.add(EB);
  { const bergG=(seed,flach)=>{ const g=new T.IcosahedronGeometry(1,Q>0?2:1), p=g.attributes.position; for(let i=0;i<p.count;i++){ let x=p.getX(i), y=p.getY(i), z=p.getZ(i); const n=0.72+0.55*fb3(x*1.4+seed+z*0.7,y*1.4-z*1.1+seed*0.5,3); x*=n; y*=n; z*=n; y=flach?(y>0?Math.min(y*0.6,0.3+0.02*Math.sin(x*9+seed)):y*0.9):(y>0?y*0.85:y*0.8); p.setXYZ(i,x,y,z); }
      g.computeVertexNormals(); const nn=g.attributes.normal, c=[]; for(let i=0;i<p.count;i++){ const y=p.getY(i); c.push(...(y<-0.02?[0.16,0.42,0.64]:nn.getY(i)>0.55?[0.96,0.98,1]:[0.6,0.8,0.94])); } g.setAttribute('color',new T.Float32BufferAttribute(c,3)); return g; };
    const bergM=eisLicht(mat({vertexColors:true,roughness:0.4,metalness:0}),0.2), schollenM=selbst(mat({color:0xe6f0fa,roughness:0.75,metalness:0}),0.25);
    const meerAn=(x,z)=>{ const rr=Math.hypot(x,z); return hoehe(Math.atan2(x,z)/R2D,90-rr/RD*180); };
    const ort=(rmin,rmax,tief,nah)=>{ for(let v=0;v<80;v++){ const rr=rmin+(rmax-rmin)*zuf(), a=zuf()*TAU, x=rr*Math.sin(a), z=rr*Math.cos(a); if(meerAn(x,z)>-tief) continue; if(nah&&meerAn(x*(1+0.4/rr),z*(1+0.4/rr))<0&&meerAn(x*(1+0.8/rr),z*(1+0.8/rr))<0) continue; return [x,z]; } return null; };
    const M4=new T.Matrix4(), qq=new T.Quaternion(), yA=new T.Vector3(0,1,0), v1=new T.Vector3(), v2=new T.Vector3();
    const setze=(geo,m,n,f)=>{ const im=new T.InstancedMesh(geo,m,n); let k=0; for(let v=0;v<n;v++){ const r=f(); if(!r) continue; qq.setFromAxisAngle(yA,zuf()*TAU); v1.set(r[0],r[1],r[2]); v2.set(r[3],r[4],r[5]); M4.compose(v1,qq,v2); im.setMatrixAt(k++,M4); } im.count=k; im.frustumCulled=false; im.receiveShadow=true; EB.add(im); return im; };
    const NB=[15,30,48][Q], NF=[70,160,300][Q];
    [bergG(1.3,true),bergG(4.7,true),bergG(8.1,false)].forEach((g,fi)=>{ const im=setze(g,bergM,Math.round(NB/3),()=>{ const o=ort(8.0,9.9,0.25,zuf()<0.8); if(!o) return null; const s=0.022+0.05*Math.pow(zuf(),2); return [o[0],0.004,o[1],s*(0.8+0.6*zuf()),s*(fi<2?0.75:1.1),s]; }); im.castShadow=Q===2; });
    const fg=new T.CylinderGeometry(1,0.92,0.14,7,1), fp=fg.attributes.position; for(let i=0;i<fp.count;i++){ const x=fp.getX(i), z=fp.getZ(i), k=0.7+0.55*hs3(Math.round(x*100)+500,Math.round(z*100)+500); fp.setX(i,x*k); fp.setZ(i,z*k); } fg.computeVertexNormals();
    setze(fg,schollenM,NF,()=>{ const o=ort(8.0,9.95,0.05,zuf()<0.9); if(!o) return null; const s=0.006+0.016*zuf(); return [o[0],0.002,o[1],s,s,s*(0.6+0.6*zuf())]; }); }
  /* ---------- Gemeinsame Bausteine ---------- */
  const textur=(w,f)=>{ const c=document.createElement('canvas'); c.width=c.height=w; f(c.getContext('2d'),w); const t=new T.CanvasTexture(c); t.wrapS=t.wrapT=T.RepeatWrapping; t.anisotropy=Math.min(8,r.capabilities.getMaxAnisotropy()); return srgb(t); };
  /* kachelbares Rauschen (vier versetzte Proben überblendet) */
  const kachel=(f,px,py,w)=>{ const u=px/w, v=py/w; return f(px,py)*(1-u)*(1-v)+f(px-w,py)*u*(1-v)+f(px,py-w)*(1-u)*v+f(px-w,py-w)*u*v; };
  const schneeT=textur(512,(x,w)=>{ const im=x.createImageData(w,w), D=im.data; for(let i=0;i<w*w;i++){ const px=i%w, py=i/w|0;
      const n=kachel((a,b)=>fb3(a/40+20,b/40+20,4)*0.5+fb3(a/90+40,b/9+40,3)*0.35+rs3(a/3+60,b/3+60)*0.15,px,py,w), v=200+n*55; D[i*4]=v-12; D[i*4+1]=v-4; D[i*4+2]=Math.min(255,v+8); D[i*4+3]=255; }
    x.putImageData(im,0,0);
    for(let s=0;s<5;s++){ const px=zuf()*w, py=zuf()*w, ang=zuf()*Math.PI, L=60+zuf()*170, pts=[]; for(let u=0;u<=24;u++) pts.push([px+Math.cos(ang)*L*u/24+7*Math.sin(u*0.9+s), py+Math.sin(ang)*L*u/24+5*Math.cos(u*1.3+s)]);
      for(const [dx,dy] of [[0,0],[w,0],[-w,0],[0,w],[0,-w]]) for(const [lw,col] of [[7,'rgba(165,205,238,.5)'],[3.4,'rgba(40,95,150,.9)'],[1.3,'rgba(8,26,55,.95)']]){ x.beginPath(); pts.forEach(([a,b],u)=>u?x.lineTo(a+dx,b+dy):x.moveTo(a+dx,b+dy)); x.lineWidth=lw*(0.6+0.4*Math.sin(s)); x.strokeStyle=col; x.lineCap='round'; x.stroke(); } } });
  schneeT.repeat.set(1/8,1/8);
  const feldT=textur(256,(x,w)=>{ const im=x.createImageData(w,w), D=im.data; for(let i=0;i<w*w;i++){ const px=i%w, py=i/w|0, n=kachel((a,b)=>fb3(a/24+7,b/24+7,4)*0.6+rs3(a/3+9,b/3+9)*0.4,px,py,w), v=215+n*40; D[i*4]=D[i*4+1]=D[i*4+2]=Math.min(255,v); D[i*4+3]=255; } x.putImageData(im,0,0); }); feldT.repeat.set(1/3,1/3);
  /* Polargitter-Ring: Radienliste rad, Höhenfunktion hf(x,z,r), Farbfunktion cf(x,z,r,h,steigung) */
  const ringFeld=(rad,ns,hf,cf)=>{ const nr=rad.length, n=nr*(ns+1), P=new Float32Array(n*3), C=new Float32Array(n*3), U=new Float32Array(n*2), Hh=new Float32Array(n);
    for(let i=0;i<nr;i++){ const rr=rad[i]; for(let j=0;j<=ns;j++){ const a=(j%ns)/ns*TAU, x=rr*Math.sin(a), z=rr*Math.cos(a), o=i*(ns+1)+j, h=hf(x,z,rr); P[o*3]=x; P[o*3+1]=h; P[o*3+2]=z; U[o*2]=x; U[o*2+1]=z; Hh[o]=h; } }
    for(let i=0;i<nr;i++){ const rr=rad[i], i0=Math.max(0,i-1), i1=Math.min(nr-1,i+1), dr=rad[i1]-rad[i0]||1, da=TAU/ns*rr; for(let j=0;j<=ns;j++){ const o=i*(ns+1)+j, jl=(j+ns-1)%ns, jr=(j+1)%ns;
      const s1=(Hh[i1*(ns+1)+j]-Hh[i0*(ns+1)+j])/dr, s2=(Hh[i*(ns+1)+jr]-Hh[i*(ns+1)+jl])/(2*da), c=cf(P[o*3],P[o*3+2],rr,Hh[o],Math.hypot(s1,s2)); C[o*3]=c[0]; C[o*3+1]=c[1]; C[o*3+2]=c[2]; } }
    const I=new Uint32Array((nr-1)*ns*6); let k=0; for(let i=0;i<nr-1;i++) for(let j=0;j<ns;j++){ const a=i*(ns+1)+j, b=a+ns+1; I[k++]=a; I[k++]=b; I[k++]=a+1; I[k++]=a+1; I[k++]=b; I[k++]=b+1; }
    const g=new T.BufferGeometry(); g.setAttribute('position',new T.BufferAttribute(P,3)); g.setAttribute('color',new T.BufferAttribute(C,3)); g.setAttribute('uv',new T.BufferAttribute(U,2)); g.setIndex(new T.BufferAttribute(I,1)); g.computeVertexNormals(); return g; };
  const reihe=(a,b,n,k)=>{ const o=[]; for(let i=0;i<n;i++){ const t=i/n; o.push(a+(b-a)*(k?(Math.exp(k*t)-1)/(Math.exp(k)-1):t)); } return o; };
  const dunstM=(farbe,staerke,pot)=>new T.ShaderMaterial({transparent:true,depthWrite:false,side:T.DoubleSide,fog:false,uniforms:{c:{value:new T.Color(farbe)}},
    vertexShader:'varying vec2 vU;void main(){vU=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',
    fragmentShader:'uniform vec3 c;varying vec2 vU;void main(){gl_FragColor=vec4(c,pow(1.-vU.y,'+pot.toFixed(2)+')*'+staerke.toFixed(3)+');}'});
  /* Himmelsglocke mit Dunst zum Horizont (Horizontfarbe = Nebelfarbe) */
  const himmel=(horiz,oben)=>{ const m=new T.Mesh(new T.SphereGeometry(700,48,24),new T.ShaderMaterial({side:T.BackSide,depthWrite:false,fog:false,uniforms:{a:{value:new T.Color(horiz)},b:{value:new T.Color(oben)}},
    vertexShader:'varying float vH;void main(){vH=normalize(position).y;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',
    fragmentShader:'uniform vec3 a;uniform vec3 b;varying float vH;void main(){float t=smoothstep(-.02,.5,vH);gl_FragColor=vec4(mix(a,b,pow(t,.55)),1.);}'})); m.renderOrder=-2; return m; };
  const punkte=(n,f,size,col,op)=>{ const p=new Float32Array(n*3); for(let i=0;i<n;i++){ const v=f(); p[i*3]=v[0]; p[i*3+1]=v[1]; p[i*3+2]=v[2]; } const g=new T.BufferGeometry(); g.setAttribute('position',new T.BufferAttribute(p,3)); return new T.Points(g,new T.PointsMaterial({size,color:col,transparent:true,opacity:op,depthWrite:false,sizeAttenuation:true,fog:false})); };
  sc.add(punkte(3500,()=>{ const u=zuf()*TAU, c=zuf()*2-1, s=Math.sqrt(1-c*c); return [320*s*Math.cos(u),320*c,320*s*Math.sin(u)]; },1.0,0xffffff,0.85));
  const kU={t:{value:0}}, lagePol=(lon,lat)=>{ const rr=(90-lat)/180*RD, a=lon*R2D; return [rr*Math.sin(a),rr*Math.cos(a)]; };
  /* ---------- Beschriftungen: Sprites mit Bildschirmgrößen-Grenzen und Ausblenden bei Überlappung ---------- */
  const LBL=[];
  const schild=(txt,o={})=>{ const fs=o.fs||44, c=document.createElement('canvas'), x=c.getContext('2d'); const font=(o.it?'italic ':'')+(o.w||600)+' '+fs+'px '+(o.serif?'"Alegreya",Georgia,serif':'"Alegreya Sans SC","Alegreya Sans",system-ui,sans-serif'); x.font=font; const zl=String(txt).split('\n'); const w=Math.ceil(Math.max(...zl.map(z=>x.measureText(z).width)))+24, h=Math.ceil(fs*1.3*zl.length)+12; c.width=w; c.height=h; x.font=font; x.textAlign='center'; x.textBaseline='middle';
    zl.forEach((z,i)=>{ const y=6+fs*0.65+i*fs*1.3, f2=i&&o.c2?o.c2:o.c||'#f2ead8'; x.lineWidth=7; x.strokeStyle='rgba(3,8,18,.22)'; x.strokeText(z,w/2,y); x.lineWidth=3.5; x.strokeStyle='rgba(3,8,18,.6)'; x.strokeText(z,w/2,y); x.fillStyle=f2; x.fillText(z,w/2,y); });
    const t=srgb(new T.CanvasTexture(c)); t.minFilter=T.LinearFilter; t.generateMipmaps=false; const s=new T.Sprite(new T.SpriteMaterial({map:t,transparent:true,depthWrite:false,depthTest:o.dt!==false,fog:false,opacity:0})); const k=o.k||0.0105; s.scale.set(w*k,h*k,1); s.renderOrder=6;
    const kl=1; s.userData.l={w:w*k,h:h*k,prio:o.p||5,pmin:(o.pmin||17)*kl*(h/(fs*1.3+12)),pmax:(o.pmax||38)*kl*(h/(fs*1.3+12)),z:0}; LBL.push(s); LBL.sort((a,b)=>b.userData.l.prio-a.userData.l.prio); return s; };
  const aktiv=o=>{ for(o=o.parent;o;o=o.parent) if(!o.visible) return false; return true; };
  const vv=new T.Vector3(), boxen=[]; let barH=60;
  const sperr=[...el.querySelectorAll('.k3-info,.k3-kam')], eR=el.getBoundingClientRect();
  const ordnen=()=>{ const H=el.clientHeight, W=el.clientWidth, f=H/(2*Math.tan(cam.fov*R2D/2)); boxen.length=0; for(const x of sperr){ const b=x.getBoundingClientRect(); if(b.width) boxen.push([b.left-eR.left-4,b.top-eR.top-4,b.right-eR.left+4,b.bottom-eR.top+4]); }
    for(const s of LBL){ const L=s.userData.l; L.z=0; if(!aktiv(s)) continue; s.getWorldPosition(vv); const di=vv.distanceTo(cam.position); vv.project(cam); if(vv.z>1||Math.abs(vv.x)>1.05||Math.abs(vv.y)>1.05) continue;
      let ph=L.h*f/di; const fac=Math.max(L.pmin,Math.min(L.pmax,ph))/ph; s.scale.set(L.w*fac,L.h*fac,1); ph*=fac; const pw=ph*L.w/L.h, cx=(vv.x+1)/2*W, cy=(1-vv.y)/2*H;
      const b=[cx-pw*0.44,cy-ph*0.36,cx+pw*0.44,cy+ph*0.36]; if(b[1]<barH||boxen.some(o=>b[0]<o[2]&&b[2]>o[0]&&b[1]<o[3]&&b[3]>o[1])) continue; boxen.push(b); L.z=1; } };
  const blenden=()=>{ for(const s of LBL){ const o=s.material.opacity, z=s.userData.l.z; if(o!==z) s.material.opacity=Math.abs(z-o)<0.05?z:o+(z-o)*0.22; s.visible=s.material.opacity>0.01; } };
  const NAMEN=new T.Group(); sc.add(NAMEN);
  [['NORDAMERIKA',-100,42],['SÜDAMERIKA',-60,-14],['EUROPA',18,52],['AFRIKA',20,6],['ASIEN',95,50],['AUSTRALIEN',134,-25]].forEach(([n,lo,la])=>{ const s=schild(n.split('').join(' '),{fs:34,w:700,c:'#f4ead6',p:8}); const [x,z]=lagePol(lo,la); s.position.set(x,0.55,z); NAMEN.add(s); });
  [['Atlantischer\nOzean',-38,28],['Pazifischer Ozean',-150,8],['Pazifischer Ozean',165,-15],['Indischer\nOzean',78,-22],['Südlicher Ozean',60,-58],['Südlicher Ozean',-120,-60]].forEach(([n,lo,la])=>{ const s=schild(n,{fs:38,it:true,serif:true,w:400,c:'#a9d4ff',k:0.0095,p:5,pmax:32}); const [x,z]=lagePol(lo,la); s.position.set(x,0.3,z); NAMEN.add(s); });
  const ewS=schild('Eiswall (Antarktis)',{fs:36,it:true,serif:true,w:600,c:'#eaf4ff',k:0.011,p:7}); ewS.position.set(0,1.9,RD*1.06); NAMEN.add(ewS);
  /* Breitenkreise fein auf der Scheibe, beschriftet am Atlantik */
  const kreis=(rr,y,farbe,op,gestr,ziel)=>{ const p=[]; for(let i=0;i<=360;i++){ const a=i/360*TAU; p.push(new T.Vector3(rr*Math.sin(a),y,rr*Math.cos(a))); } const g=new T.BufferGeometry().setFromPoints(p); const m=gestr?new T.LineDashedMaterial({color:farbe,transparent:true,opacity:op,dashSize:gestr,gapSize:gestr*0.7,depthWrite:false}):new T.LineBasicMaterial({color:farbe,transparent:true,opacity:op,depthWrite:false}); const l=new T.Line(g,m); if(gestr) l.computeLineDistances(); (ziel||sc).add(l); return l; };
  const KREISE=new T.Group(); sc.add(KREISE);
  [[66.56,'Nördl. Polarkreis',0x9fd0ff,0.07],[23.44,'Wendekreis des Krebses',0xffc070,0.09],[0,'Äquator',0xffd860,0],[-23.44,'Wendekreis des Steinbocks',0xffc070,0.09],[-66.56,'Südl. Polarkreis',0x9fd0ff,0.07]].forEach(([la,n,f,ds])=>{ const rr=(90-la)/180*RD; kreis(rr,0.014,f,0.55,ds,KREISE); const s=schild(n,{fs:26,w:500,c:'#'+f.toString(16).padStart(6,'0'),k:0.0075,p:3,pmin:19,pmax:28}); const [x,z]=lagePol(-22,la); s.position.set(x,0.12,z); NAMEN.add(s); });
  /* Nordpol-Markierung */
  const pol=new T.Group(); pol.add(new T.Mesh(new T.CylinderGeometry(0.012,0.012,0.7,8),new T.MeshBasicMaterial({color:0xdfe8ff}))); pol.children[0].position.y=0.35;
  const pk=new T.Mesh(new T.SphereGeometry(0.045,16,8),new T.MeshBasicMaterial({color:0xffffff})); pk.position.y=0.72; pol.add(pk);
  const pr=new T.Mesh(new T.RingGeometry(0.16,0.19,64),new T.MeshBasicMaterial({color:0xcfe0ff,transparent:true,opacity:0.6,side:T.DoubleSide,depthWrite:false})); pr.rotation.x=-Math.PI/2; pr.position.y=0.03; pol.add(pr); sc.add(pol);
  const polS=schild('Nordpol',{fs:34,w:700,c:'#ffffff',k:0.0095,p:10}); polS.position.set(0,1.25,0); NAMEN.add(polS);
  /* Licht */
  sc.add(new T.AmbientLight(0x5a6c90,0.21)); sc.add(new T.HemisphereLight(0x8fb4ff,0x101522,0.14));
  const dl=new T.DirectionalLight(0xbfd4ff,0.22); dl.position.set(-8,12,6); sc.add(dl); const dl2=new T.DirectionalLight(0x9cb8e8,0.24); dl2.position.set(10,5,-30); sc.add(dl2);
  const dlU=new T.DirectionalLight(0x8ea6d8,0.3); dlU.position.set(8,-14,10); sc.add(dlU); /* nur für Unterseite/Säulen wirksam */
  const glanz=(farbe)=>{ const c=document.createElement('canvas'); c.width=c.height=128; const x=c.getContext('2d'), g=x.createRadialGradient(64,64,0,64,64,64); g.addColorStop(0,farbe); g.addColorStop(0.25,farbe.replace(/[\d.]+\)$/,'0.45)')); g.addColorStop(1,'rgba(0,0,0,0)'); x.fillStyle=g; x.fillRect(0,0,128,128); return new T.Sprite(new T.SpriteMaterial({map:new T.CanvasTexture(c),blending:T.AdditiveBlending,depthWrite:false,transparent:true,fog:false})); };
  const koerper=(rad,farbe,glow,gs,int,ang,lc,schatten)=>{ const g=new T.Group(); g.add(new T.Mesh(new T.SphereGeometry(rad,32,16),new T.MeshBasicMaterial({color:farbe,toneMapped:false}))); const s=glanz(glow); s.scale.set(gs,gs,1); g.add(s);
    const sp=new T.SpotLight(lc,int,0,ang,0.8,0); sp.position.set(0,0,0); if(schatten&&Q===2){ sp.castShadow=true; sp.shadow.mapSize.set(2048,2048); sp.shadow.bias=-0.0004; sp.shadow.normalBias=0.02; sp.shadow.camera.near=0.5; sp.shadow.camera.far=22; } sc.add(sp.target); g.add(sp); sc.add(g); return {g,sp}; };
  const SO=koerper(0.26,0xfff3c4,'rgba(255,214,110,1)',2.2,6,0.85,0xfff0d8,true), MO=koerper(0.19,0xe6ecf5,'rgba(190,210,255,1)',1.5,1.1,0.7,0x8fb0ff,false);
  const halo=glanz('rgba(255,170,80,.55)'); halo.scale.set(6,6,1); halo.material.opacity=0.55; SO.g.add(halo);
  /* Lichtkegel unter Sonne und Mond */
  const kegelM=(farbe,st)=>new T.ShaderMaterial({transparent:true,depthWrite:false,blending:T.AdditiveBlending,side:T.DoubleSide,fog:false,uniforms:{t:kU.t},
    vertexShader:'varying float vY;varying float vA;varying vec3 vN;varying vec3 vV;void main(){vY=uv.y;vA=uv.x;vec4 mv=modelViewMatrix*vec4(position,1.);vN=normalize(normalMatrix*normal);vV=normalize(-mv.xyz);gl_Position=projectionMatrix*mv;}',
    fragmentShader:'uniform float t;varying float vY;varying float vA;varying vec3 vN;varying vec3 vV;void main(){float e=abs(dot(vN,vV));float s=.55+.45*sin(vA*157.+t*.5)*sin(vA*63.-t*.37);gl_FragColor=vec4(vec3('+farbe+')*vY*vY*e*s*'+st+',1.);}'});
  const HS=3.2;
  const kegel=new T.Mesh(new T.CylinderGeometry(0.22,3.5,HS,72,1,true),kegelM('1.,.84,.55','.085')); kegel.position.y=-HS/2; SO.g.add(kegel);
  const mKegel=new T.Mesh(new T.CylinderGeometry(0.16,2.6,HS*0.92,64,1,true),kegelM('.62,.74,1.','.05')); mKegel.position.y=-HS*0.46; MO.g.add(mKegel);
  /* Mond mit Phase */
  const mU={L:{value:new T.Vector3(0,0,1)}}; MO.g.children[0].material=new T.ShaderMaterial({uniforms:mU,
    vertexShader:'varying vec3 vN;varying vec3 vP;void main(){vN=normalize(normalMatrix*normal);vP=position;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',
    fragmentShader:'uniform vec3 L;varying vec3 vN;varying vec3 vP;void main(){float l=smoothstep(-.06,.14,dot(normalize(vN),L));float m=.86+.14*sin(vP.x*61.)*sin(vP.y*53.+1.)*sin(vP.z*47.+2.);vec3 c=mix(vec3(.03,.04,.065),vec3(.9,.93,1.)*m,l);gl_FragColor=vec4(c,1.);}'});
  const mondAlter=z=>{ const jd=z.getTime()/864e5+2440587.5; return (((jd-2451550.1)/29.530588853)%1+1)%1; };
  /* Bahnen auf Sonnenhöhe: Grenzen (Wendekreise, Äquator) gestrichelt, heutige Sonnen- und Mondbahn als feine Leuchtringe */
  [23.44,0,-23.44].forEach(la=>kreis((90-la)/180*RD,HS,0xffd28a,0.16,0.16));
  const bahn=(farbe,op)=>kreis(1,0,farbe,op,0);
  const sBahn=bahn(0xffd860,0.8), mBahn=bahn(0x9fb6ff,0.5);
  /* ---------- Varianten „Hinter der Eiswand“ (werden beim ersten Aufruf gebaut) ---------- */
  /* Kuppel (Firmament) mit Gitter, Lichtreflex, Fußring und Sternen; Polarstern über dem Nordpol */
  const KY=0.82, RK=RA-0.12, KB=0.25, kS={value:new T.Vector3()}; let kuppelG=null, sterneG=null, kuppelZeig=true;
  const sternPos=(raG,dec)=>{ const rr=(90-dec)/180*RD, a=raG*R2D; return [rr*Math.sin(a)*0.993,KB+KY*Math.sqrt(Math.max(0,RK*RK-rr*rr))*0.993,rr*Math.cos(a)*0.993]; };
  const baueKuppel=()=>{ const g=new T.Group();
    const dm=new T.ShaderMaterial({transparent:true,depthWrite:false,side:T.DoubleSide,fog:false,extensions:{derivatives:true},uniforms:{t:kU.t,S:kS},
      vertexShader:'varying vec3 vN;varying vec3 vW;varying vec3 vP;void main(){vP=position;vN=normalize(vec3(position.x,position.y/'+KY.toFixed(3)+',position.z));vec4 w=modelMatrix*vec4(position,1.);vW=w.xyz;gl_Position=projectionMatrix*viewMatrix*w;}',
      fragmentShader:'uniform float t;uniform vec3 S;varying vec3 vN;varying vec3 vW;varying vec3 vP;void main(){vec3 V=normalize(cameraPosition-vW);vec3 N=normalize(vN);float f=pow(1.-abs(dot(N,V)),2.6);'+
        'vec2 q=vec2(atan(vP.x,vP.z)/6.2832*48.,asin(clamp(vP.y/'+RK.toFixed(3)+',0.,1.))/1.5708*12.);vec2 gq=abs(fract(q)-.5)/max(fwidth(q),vec2(1e-4));float gn=1.-min(min(gq.x,gq.y),1.);gn*=smoothstep(11.6,10.,q.y);'+
        'float s=.5+.5*sin(vP.y*2.2+atan(vP.x,vP.z)*3.+t*.35);vec3 L=normalize(S-vW);float sp=pow(max(dot(reflect(-V,N),L),0.),70.)+pow(max(dot(reflect(-V,-N),L),0.),70.);'+
        'vec3 c=mix(vec3(.30,.50,1.),vec3(.78,.9,1.),f)+vec3(.25,.18,.45)*s*f*.4;c=mix(c,vec3(.78,.9,1.),gn*.55);c+=vec3(1.,.9,.72)*sp;'+
        'float a=(.016+.27*f)*(.8+.2*s)+gn*(.11+.12*f)+.05*(1.-smoothstep(0.,.3,vP.y))+sp*.55;gl_FragColor=vec4(c,min(a,.92));}'});
    const dome=new T.Mesh(new T.SphereGeometry(RK,[96,128,160][Q],[40,56,72][Q],0,TAU,0,Math.PI/2),dm); dome.scale.y=KY; dome.position.y=KB; dome.renderOrder=3; g.add(dome);
    const fuss=new T.Mesh(new T.LatheGeometry([[0.2,-0.18],[0.17,-0.02],[0.12,0.02],[0.05,0.045],[-0.03,0.05],[-0.08,0.02],[-0.1,-0.18]].map(([dr,y])=>new T.Vector2(RK+dr,y)),[128,192,256][Q]),
      selbst(mat({color:0xb4cdea,roughness:0.28,metalness:0.55,emissive:0x16283f,emissiveIntensity:0.6}),0.12)); fuss.position.y=KB; fuss.receiveShadow=true; g.add(fuss);
    /* Sterne an der Kuppel: dort, wo sie im Zenit stehen (Deklination → Abstand vom Pol), drehen mit der Sternzeit */
    sterneG=new T.Group(); g.add(sterneG);
    const ST={Polaris:[2.530,89.26,1.98],Dubhe:[11.062,61.75,1.79],Merak:[11.031,56.38,2.37],Phecda:[11.897,53.69,2.44],Megrez:[12.257,57.03,3.31],Alioth:[12.900,55.96,1.77],Mizar:[13.399,54.93,2.23],Alkaid:[13.792,49.31,1.86],
      Caph:[0.153,59.15,2.28],Schedar:[0.675,56.54,2.24],GamCas:[0.945,60.72,2.47],Ruchbah:[1.430,60.24,2.68],Segin:[1.907,63.67,3.37],Kochab:[14.845,74.16,2.08],Pherkad:[15.345,71.83,3.05],
      Betelgeuse:[5.919,7.41,0.5],Bellatrix:[5.419,6.35,1.64],Mintaka:[5.533,-0.30,2.23],Alnilam:[5.604,-1.20,1.69],Alnitak:[5.679,-1.94,1.74],Saiph:[5.796,-9.67,2.07],Rigel:[5.242,-8.20,0.13],
      Sirius:[6.752,-16.72,-1.46],Canopus:[6.399,-52.70,-0.74],Arcturus:[14.261,19.18,-0.05],AlphaCen:[14.660,-60.83,-0.27],Vega:[18.616,38.78,0.03],Capella:[5.278,46.0,0.08],Procyon:[7.655,5.22,0.34],
      Achernar:[1.629,-57.24,0.46],Hadar:[14.064,-60.37,0.61],Altair:[19.846,8.87,0.76],Acrux:[12.443,-63.10,0.76],Aldebaran:[4.599,16.51,0.86],Antares:[16.490,-26.43,0.96],Spica:[13.420,-11.16,0.97],
      Pollux:[7.755,28.03,1.14],Fomalhaut:[22.961,-29.62,1.16],Deneb:[20.690,45.28,1.25],Mimosa:[12.795,-59.69,1.25],Regulus:[10.139,11.97,1.35],Castor:[7.577,31.89,1.58],Gacrux:[12.519,-57.11,1.63],
      Mirfak:[3.405,49.86,1.79],Alpheratz:[0.140,29.09,2.06],Algol:[3.136,40.96,2.1]};
    const SP=[], SG=[], SC=[], ad=(ra,dec,mag,c)=>{ SP.push(...sternPos(ra*15,dec)); SG.push(Math.max(1.1,5.4-mag*1.2)); SC.push(...c); };
    for(const k in ST){ const [ra,dec,m]=ST[k]; ad(ra,dec,m,k==='Polaris'?[1,0.97,0.86]:/Betelgeuse|Antares|Aldebaran|Arcturus/.test(k)?[1,0.8,0.62]:/Rigel|Spica|Vega|Sirius|Achernar|Acrux/.test(k)?[0.8,0.88,1]:[1,1,0.96]); }
    for(let i=0;i<[600,1000,1600][Q];i++){ const t=zuf(); ad(zuf()*24,Math.asin(zuf()*2-1)/R2D,3.0+3.2*Math.sqrt(zuf()),t<0.15?[1,0.86,0.72]:t<0.35?[0.78,0.86,1]:[1,1,1]); }
    const sg=new T.BufferGeometry(); sg.setAttribute('position',new T.Float32BufferAttribute(SP,3)); sg.setAttribute('g',new T.Float32BufferAttribute(SG,1)); sg.setAttribute('col',new T.Float32BufferAttribute(SC,3));
    const sm=new T.ShaderMaterial({transparent:true,depthWrite:false,blending:T.AdditiveBlending,fog:false,uniforms:{t:kU.t,ph:{value:900}},
      vertexShader:'attribute float g;attribute vec3 col;uniform float t;uniform float ph;varying vec3 vC;varying float vT;void main(){vC=col;vec4 mv=modelViewMatrix*vec4(position,1.);vT=.78+.22*sin(t*2.3+position.x*41.+position.z*17.);gl_PointSize=clamp(g*ph/(-mv.z)*.011,1.,g*2.4);gl_Position=projectionMatrix*mv;}',
      fragmentShader:'varying vec3 vC;varying float vT;void main(){float d=length(gl_PointCoord-.5);float a=smoothstep(.5,0.,d);a*=a;gl_FragColor=vec4(vC*a*vT,1.);}'});
    const pts=new T.Points(sg,sm); pts.frustumCulled=false; pts.renderOrder=4; sterneG.add(pts); g.userData.sm=sm;
    const LIN=[['Alkaid','Mizar'],['Mizar','Alioth'],['Alioth','Megrez'],['Megrez','Phecda'],['Phecda','Merak'],['Merak','Dubhe'],['Dubhe','Megrez'],['Caph','Schedar'],['Schedar','GamCas'],['GamCas','Ruchbah'],['Ruchbah','Segin'],
      ['Betelgeuse','Bellatrix'],['Bellatrix','Mintaka'],['Mintaka','Alnilam'],['Alnilam','Alnitak'],['Alnitak','Saiph'],['Saiph','Rigel'],['Rigel','Mintaka'],['Betelgeuse','Alnitak'],['Acrux','Gacrux'],['Polaris','Kochab'],['Kochab','Pherkad']];
    const lp=[]; LIN.forEach(([a,b])=>{ lp.push(...sternPos(ST[a][0]*15,ST[a][1]),...sternPos(ST[b][0]*15,ST[b][1])); }); const lg=new T.BufferGeometry(); lg.setAttribute('position',new T.Float32BufferAttribute(lp,3));
    sterneG.add(new T.LineSegments(lg,new T.LineBasicMaterial({color:0x9db8ff,transparent:true,opacity:0.32,depthWrite:false,fog:false})));
    const nS=(txt,ra,dec,dy,p)=>{ const s=schild(txt,{fs:30,w:600,c:'#e6eeff',k:0.009,p,pmin:19,pmax:30}); const v=sternPos(ra*15,dec); s.position.set(v[0],v[1]+dy,v[2]); sterneG.add(s); };
    nS('Polarstern',2.53,89.26,-0.45,9); nS('Großer Wagen',12.3,56,-0.5,4); nS('Orion',5.6,-1,-0.6,3); nS('Kassiopeia',1.0,60.5,-0.5,3); nS('Kreuz des Südens',12.5,-60,-0.5,3);
    return g; };
  /* Wasser über der Feste: bewegte Wasserschicht über der Kuppel */
  const baueWasserOben=()=>{ const g=new T.Group(), R=RK+0.95;
    const m=new T.ShaderMaterial({transparent:true,depthWrite:false,side:T.DoubleSide,fog:false,uniforms:{t:kU.t},
      vertexShader:'uniform float t;varying vec3 vW;varying vec3 vN;varying float vE;void main(){vec3 p=position;vec3 n=normalize(p);vE=acos(clamp(n.y,-1.,1.));float w=sin(p.x*1.3+t*.8)*.5+sin(p.z*1.7-t*.6)*.35+sin((p.x+p.z)*2.9+t*1.3)*.15;p+=n*w*.16;vN=n;vec4 wp=modelMatrix*vec4(p,1.);vW=wp.xyz;gl_Position=projectionMatrix*viewMatrix*wp;}',
      fragmentShader:'uniform float t;varying vec3 vW;varying vec3 vN;varying float vE;void main(){vec3 V=normalize(cameraPosition-vW);float f=pow(1.-abs(dot(normalize(vN),V)),2.);float c1=sin(vW.x*2.1+t*.9+sin(vW.z*1.7+t*.4)*2.)*sin(vW.z*2.3-t*.7+sin(vW.x*1.3)*2.);float k=pow(abs(c1),6.)*.8;'+
        'vec3 c=mix(vec3(.04,.2,.4),vec3(.35,.68,.95),f)+vec3(.55,.85,1.)*k*.45;float a=(.38+.42*f+k*.2)*(1.-smoothstep(.95,1.3,vE));gl_FragColor=vec4(c,a);}'});
    const sch=new T.Mesh(new T.SphereGeometry(R,[96,128,192][Q],[24,32,48][Q],0,TAU,0,1.3),m); sch.scale.y=KY; sch.position.y=KB; sch.renderOrder=4; g.add(sch);
    const s=schild('Wasser über der Feste?\nnach Darstellung mancher Vertreter',{fs:34,c:'#cfe6ff',c2:'#9fb4d0',k:0.022,p:6,dt:false}); s.position.set(0,KB+R*KY+1.3,0); g.add(s); return g; };
  /* Weitere Länder: Eisgürtel, Meer mit frei erzeugten, namenlosen Landmassen, äußerer Eisring */
  const baueLaender=()=>{ const g=new T.Group(), R1=23, R2=84, SL=YO-0.12;
    const rad=[...reihe(RA-0.25,R1,[16,22,30][Q],0),R1,R1+0.07,...reihe(R1+0.14,R2,[80,120,170][Q],0.9),R2,R2+0.1,...reihe(R2+0.2,140,[16,22,30][Q],1.5),140];
    const hf=(x,z,rr)=>{ if(rr<=R1) return SL+0.13+0.05*fb3(x*0.3,z*0.3,3)*gl3(RA,RA+2,rr);
      if(rr>=R2+0.05) return SL+1.4+0.9*gl3(R2,R2+18,rr)+0.25*fb3(x*0.12,z*0.12,3)+0.8*Math.pow(1-Math.abs(2*fb3(x*0.05+4,z*0.05,4)-1),3)*gl3(R2+3,R2+12,rr);
      const m=gl3(R1+2,R1+7,rr)*gl3(R2-2,R2-8,rr), c=fb3(x*0.028+3,z*0.028-7,5)+0.12*fb3(x*0.09,z*0.09,3)-0.06; const L=(c-0.53)*m-(1-m)*0.08; let h=SL+L*3.0;
      if(L>0){ const rg=1-Math.abs(2*fb3(x*0.06+1,z*0.06+2,4)-1); h+=Math.pow(rg,2.2)*gl3(0,0.12,L)*2.4; } return h; };
    const cf=(x,z,rr,h,sl)=>{ if(rr<=R1+0.001||rr>=R2+0.07){ const n=0.92+0.08*fb3(x*0.5,z*0.5,2); return sl>1.2?[0.5,0.72,0.9]:[0.9*n,0.94*n,n]; }
      const e=h-SL; if(e<0){ const d=gl3(-0.3,0,e); return misch([0.04,0.12,0.22],[0.18,0.52,0.56],d*d); }
      const kalt=Math.max(gl3(R1+14,R1+3,rr),gl3(R2-16,R2-3,rr)), tr=fb3(x*0.05+7,z*0.05,3);
      let c=e<0.03?[0.74,0.69,0.52]:misch([0.30,0.44,0.20],[0.56,0.52,0.33],gl3(0.4,0.7,tr));
      if(e>=0.03) c=misch(c,[0.14,0.28,0.14],gl3(0.08,0.25,e)*(1-gl3(0.5,0.8,tr))*0.8);
      c=misch(c,[0.43,0.37,0.28],gl3(0.45,0.9,e)); c=misch(c,[0.47,0.46,0.45],Math.max(gl3(0.9,1.3,e),0.7*gl3(0.8,1.6,sl)));
      c=misch(c,[0.5,0.53,0.46],kalt*0.6); return misch(c,[0.95,0.96,1],gl3(1.45-kalt*0.9,1.75-kalt*0.9,e)); };
    const land=new T.Mesh(ringFeld(rad,[384,640,960][Q],hf,cf),selbst(mat({vertexColors:true,map:feldT,roughness:0.92,metalness:0}),0.28)); land.receiveShadow=true; g.add(land);
    const meer=new T.Mesh(new T.RingGeometry(R1-0.4,R2+0.06,[192,256,384][Q],1),new T.MeshPhongMaterial({color:0x1c4f7a,specular:0x8fb0d0,shininess:90,transparent:true,opacity:0.8,depthWrite:false}));
    meer.rotation.x=-Math.PI/2; meer.position.y=SL; meer.renderOrder=1; g.add(meer);
    g.add(himmel(0x0e1a2c,0x03060f)); const hz=new T.Mesh(new T.CylinderGeometry(150,150,30,96,1,true),dunstM(0x2a4466,0.55,2.4)); hz.position.y=15; g.add(hz);
    const s1=schild('Weitere Länder?\nhypothetisch – nicht belegt',{fs:34,c:'#e2e6ee',c2:'#a9b3c6',k:0.03,p:6,dt:false}); s1.position.set(0,6,-48); g.add(s1);
    const s2=schild('Äußerer Eisring?\nnach Darstellung mancher Vertreter',{fs:30,c:'#e6f2ff',c2:'#a9b3c6',k:0.03,p:5,dt:false}); s2.position.set(-30,5,R2*0.72); g.add(s2); return g; };
  /* Endloses Eis: Eisebene mit Verwehungen, Gletscherspalten, Gebirgszügen, Dunst und Polarlicht */
  const baueEis=()=>{ const g=new T.Group(); const rad=reihe(RA-0.25,440,[90,130,180][Q],5); rad.push(440);
    const hf=(x,z,rr)=>{ const d=rr-RA; let h=YO-0.02+0.05*fb3(x*0.35,z*0.35,3)*gl3(0,2,d)+0.9*fb3(x*0.025+5,z*0.025,3)*gl3(2,30,d);
      const m=gl3(22,55,rr)*gl3(0.38,0.6,fb3(x*0.006+2,z*0.006-4,2)); if(m>0){ const rg=1-Math.abs(2*fb3(x*0.03+9,z*0.03-3,5)-1); h+=m*Math.pow(rg,2.6)*(5+9*fb3(x*0.01,z*0.01,2)); } return h; };
    const cf=(x,z,rr,h,sl)=>{ const n=0.9+0.1*fb3(x*0.2,z*0.2,2); let c=[0.86*n,0.91*n,0.99*n]; c=misch(c,[0.62,0.75,0.92],0.35*gl3(0.4,0.0,fb3(x*0.08,z*0.08,2))); return misch(c,[0.2,0.21,0.24],gl3(0.75,1.4,sl)); };
    const eb=new T.Mesh(ringFeld(rad,[256,384,512][Q],hf,cf),selbst(mat({vertexColors:true,map:schneeT,roughness:0.82,metalness:0}),0.3)); eb.receiveShadow=true; g.add(eb);
    g.add(himmel(0x0e1a2c,0x02050c)); const hz=new T.Mesh(new T.CylinderGeometry(300,300,40,96,1,true),dunstM(0x2a4466,0.6,2.2)); hz.position.y=20; g.add(hz);
    /* Polarlicht: drei bewegte Lichtvorhänge über dem Horizont */
    const pm=new T.ShaderMaterial({transparent:true,depthWrite:false,blending:T.AdditiveBlending,side:T.DoubleSide,fog:false,uniforms:{t:kU.t},
      vertexShader:'uniform float t;varying vec2 vU;void main(){vU=uv;vec3 p=position;p.y+=sin(uv.x*11.+t*.21)*1.5*uv.y;gl_Position=projectionMatrix*modelViewMatrix*vec4(p,1.);}',
      fragmentShader:'uniform float t;varying vec2 vU;void main(){float r=.6+.25*sin(vU.x*190.+t*.7+sin(vU.x*37.+t*.3)*3.)+.15*sin(vU.x*520.-t*1.1);r*=.55+.45*sin(vU.x*23.-t*.23);float v=pow(1.-vU.y,1.5)*smoothstep(0.,.1,vU.y);float e=smoothstep(0.,.1,vU.x)*smoothstep(1.,.9,vU.x);vec3 c=mix(vec3(.15,1.,.55),vec3(.62,.3,1.),smoothstep(.3,1.,vU.y));gl_FragColor=vec4(c*r*v*e*.38,1.);}'});
    [[150,-0.9,1.3,26,30],[190,-0.2,1.1,30,40],[130,0.6,0.9,22,26]].forEach(([R,a0,sp,y0,H])=>{ const pg=new T.PlaneGeometry(1,1,[80,120,160][Q],1), p=pg.attributes.position, u=pg.attributes.uv;
      for(let i=0;i<p.count;i++){ const s=u.getX(i), v=u.getY(i), a=Math.PI+a0+sp*(s-0.5), rr=R+9*Math.sin(s*7+R); p.setXYZ(i,rr*Math.sin(a),y0+v*H,rr*Math.cos(a)); } const m=new T.Mesh(pg,pm); m.frustumCulled=false; m.renderOrder=2; g.add(m); });
    const s=schild('Endloses Eis?\nnach Darstellung mancher Vertreter',{fs:34,c:'#eef5ff',c2:'#a9b3c6',k:0.03,p:6,dt:false}); s.position.set(0,5,-42); g.add(s); return g; };
  /* Säulen bzw. Grundfesten unter der Scheibe */
  const baueSaeulen=()=>{ const g=new T.Group(), UNT=-17;
    const verbinde=(teile)=>{ let n=0; teile.forEach(t=>n+=t.attributes.position.count); const P=new Float32Array(n*3), N=new Float32Array(n*3), I=[]; let o=0;
      teile.forEach(t=>{ P.set(t.attributes.position.array,o*3); N.set(t.attributes.normal.array,o*3); const ix=t.index.array; for(let i=0;i<ix.length;i++) I.push(ix[i]+o); o+=t.attributes.position.count; });
      const b=new T.BufferGeometry(); b.setAttribute('position',new T.BufferAttribute(P,3)); b.setAttribute('normal',new T.BufferAttribute(N,3)); b.setIndex(I); return b; };
    const saeule=H=>{ const sh=new T.CylinderGeometry(0.27,0.31,H-0.62,32,Q?10:5,true), p=sh.attributes.position; for(let i=0;i<p.count;i++){ const x=p.getX(i), z=p.getZ(i), a=Math.atan2(z,x), k=1-0.06*Math.pow(0.5+0.5*Math.cos(a*20),2); p.setX(i,x*k); p.setZ(i,z*k); } sh.computeVertexNormals(); sh.translate(0,-0.3-(H-0.62)/2,0);
      const b=verbinde([new T.BoxGeometry(0.92,0.12,0.92).translate(0,-0.06,0),new T.CylinderGeometry(0.42,0.29,0.18,32).translate(0,-0.21,0),sh,new T.CylinderGeometry(0.37,0.42,0.16,32).translate(0,-H+0.24,0),new T.BoxGeometry(0.92,0.16,0.92).translate(0,-H+0.08,0)]);
      const p2=b.attributes.position, C=new Float32Array(p2.count*3); for(let i=0;i<p2.count;i++){ const y=p2.getY(i), k=0.2+0.8*gl3(-H,0,y), n=0.92+0.08*Math.sin(y*7+p2.getX(i)*5); C[i*3]=0.5*k*n; C[i*3+1]=0.46*k*n; C[i*3+2]=0.41*k*n; } b.setAttribute('color',new T.BufferAttribute(C,3)); return b; };
    const stein=selbst(mat({vertexColors:true,roughness:0.85,metalness:0.02}),0.07), M4=new T.Matrix4(), qq=new T.Quaternion(), yA=new T.Vector3(0,1,0), v1=new T.Vector3(), v2=new T.Vector3(1,1,1);
    [[0,1],[4.6,8],[8.6,16]].forEach(([rr,n])=>{ const top=sockelY(rr)+0.25, im=new T.InstancedMesh(saeule(top-UNT),stein,n); for(let i=0;i<n;i++){ const a=(i+0.5)/n*TAU; qq.setFromAxisAngle(yA,a); v1.set(rr*Math.sin(a),top,rr*Math.cos(a)); M4.compose(v1,qq,v2); im.setMatrixAt(i,M4); } im.frustumCulled=false; g.add(im); });
    const c=document.createElement('canvas'); c.width=c.height=128; const x=c.getContext('2d'), gr=x.createRadialGradient(64,64,0,64,64,64); gr.addColorStop(0,'rgba(70,95,150,.55)'); gr.addColorStop(1,'rgba(0,0,0,0)'); x.fillStyle=gr; x.fillRect(0,0,128,128);
    const ne=new T.Mesh(new T.PlaneGeometry(70,70),new T.MeshBasicMaterial({map:new T.CanvasTexture(c),transparent:true,depthWrite:false,blending:T.AdditiveBlending,fog:false})); ne.rotation.x=-Math.PI/2; ne.position.y=UNT+0.6; g.add(ne);
    const s=schild('Säulen der Erde?\nnach Darstellung mancher Vertreter',{fs:34,c:'#efe6d6',c2:'#b8ad9a',k:0.022,p:6,dt:false}); s.position.set(0,-11,4); g.add(s); return g; };
  const VAR={
    kuppel:{bau:null,nebel:[0x03060f,0.006],kam:[[0,13.5,17.5],[0,0,0]],fern:[[0,15,33],[0,2.5,0]],kuppel:true},
    wasser:{bau:baueWasserOben,nebel:[0x03060f,0.005],kam:[[0,15,26],[0,3,0]],fern:[[0,19,40],[0,3.5,0]],kuppel:true},
    laender:{bau:baueLaender,nebel:[0x0e1a2c,0.0055],kam:[[0,21,29],[0,0,-13]],fern:[[0,46,80],[0,0,-14]]},
    eis:{bau:baueEis,nebel:[0x0e1a2c,0.0105],kam:[[0,7.5,27],[0,0,-6]],fern:[[0,3.2,25],[0,1.4,-8]]},
    saeulen:{bau:baueSaeulen,nebel:[0x050811,0.03],kam:[[0,-6.5,25],[0,-5.5,0]],fern:[[17,-13,23],[0,-6,0]],unten:true}};
  const AU={}; let akt='kuppel';
  /* Steuerung */
  let ctl=null; if(L.OC){ ctl=d.ctl=new L.OC(cam,r.domElement); ctl.enableDamping=true; ctl.dampingFactor=0.08; ctl.minDistance=0.7; ctl.maxDistance=130; ctl.maxPolarAngle=Math.PI*0.48; ctl.target.set(0,0,0); ctl.enablePan=true; ctl.update(); }
  else cam.lookAt(0,0,0);
  /* Bedienung */
  let flug=null, rund=false; const hoch=()=>el.clientWidth<el.clientHeight?1.6:1;
  const fliege=(p,z,dauer,nach)=>{ if(!ctl){ cam.position.set(...p); cam.lookAt(...z); return; } const f=hoch(), zv=new T.Vector3(...z); flug={t0:performance.now(),p0:cam.position.clone(),z0:ctl.target.clone(),p1:new T.Vector3(...p).sub(zv).multiplyScalar(f).add(zv),z1:zv,dauer:dauer||1600,nach}; };
  const rundSetzen=an=>{ rund=an; const b=el.querySelector('[data-kam="rund"]'); if(b) b.setAttribute('aria-pressed',an); };
  d.flugAus=()=>{ flug=null; rundSetzen(false); };
  if(ctl) ctl.addEventListener('start',()=>{ flug=null; rundSetzen(false); });
  const polGrenze=()=>{ if(ctl) ctl.maxPolarAngle=VAR[akt].unten?Math.PI*0.96:Math.PI*0.48; };
  const kuppelSicht=()=>{ const an=!!VAR[akt].kuppel; if(an&&!kuppelG){ kuppelG=baueKuppel(); sc.add(kuppelG); } if(kuppelG) kuppelG.visible=an&&kuppelZeig; const b=q('kuppelz'); b.style.display=an?'':'none'; b.setAttribute('aria-pressed',kuppelZeig); };
  const aussen=(k,erst)=>{ akt=k; const V=VAR[k]; if(V.bau&&!AU[k]){ AU[k]=V.bau(); sc.add(AU[k]); } for(const g in AU) AU[g].visible=g===k; kuppelSicht();
    if(V.unten) polGrenze(); if(!erst) fliege(...V.kam,1500,polGrenze); else polGrenze();
    sc.fog.color.setHex(V.nebel[0]); sc.fog.density=V.nebel[1]; el.querySelectorAll('[data-aus]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.aus===k)); q('txt').innerHTML=AUSSEN[k].t; };
  d.aussen=aussen;
  el.querySelectorAll('[data-aus]').forEach(b=>b.onclick=()=>aussen(b.dataset.aus));
  q('kuppelz').onclick=()=>{ kuppelZeig=!kuppelZeig; kuppelSicht(); };
  el.querySelectorAll('[data-kam]').forEach(b=>b.onclick=()=>{ const k=b.dataset.kam; if(k==='rund'){ flug=null; rundSetzen(!rund); return; } rundSetzen(false); const V=VAR[akt];
    if(k==='oben') fliege([0,27,0.02],[0,0,0],1600,polGrenze); else if(k==='aussen') fliege(...V.fern,1700,polGrenze); else fliege(V.unten?[0,-0.4,14.2]:[0,1.7,7.2],V.unten?[0,-1.2,9]:[0,0.75,14],1700,polGrenze); });
  q('wasser').onclick=e=>{ wasser.visible=!wasser.visible; e.currentTarget.setAttribute('aria-pressed',wasser.visible); };
  const info=el.querySelector('.k3-info'), klapp=e=>{ const zu=info.classList.toggle('zu',e); q('klapp').textContent=zu?'▴':'▾'; q('klapp').setAttribute('aria-expanded',!zu); }; q('klapp').onclick=()=>klapp(!info.classList.contains('zu')); if(el.clientWidth<700) klapp(true);
  let wolken=null; q('wolken').onclick=e=>{ if(!wolken){ const W2=[384,512,768][Q], c=document.createElement('canvas'); c.width=c.height=W2; const x=c.getContext('2d'), im=x.createImageData(W2,W2);
      for(let py=0;py<W2;py++) for(let px=0;px<W2;px++){ const dx=px/W2*2-1, dz=py/W2*2-1, rr=Math.hypot(dx,dz); if(rr>1) continue; const n=fb3(dx*7+3,dz*7-2,5), m=fb3(dx*2.3,dz*2.3,2); const v=Math.max(0,Math.min(1,(n*0.7+m*0.5-0.63)*3.4)); const o=(py*W2+px)*4; im.data[o]=im.data[o+1]=im.data[o+2]=255; im.data[o+3]=v*230*Math.min(1,(1-rr)*14); }
      x.putImageData(im,0,0); wolken=new T.Mesh(new T.CircleGeometry(RD,128),selbst(mat({map:srgb(new T.CanvasTexture(c)),transparent:true,depthWrite:false,roughness:1}),0.1)); wolken.rotation.x=-Math.PI/2; wolken.position.y=0.62; wolken.renderOrder=2; sc.add(wolken); wolken.visible=false; }
    wolken.visible=!wolken.visible; e.currentTarget.setAttribute('aria-pressed',wolken.visible); };
  q('namen').onclick=e=>{ NAMEN.visible=!NAMEN.visible; e.currentTarget.setAttribute('aria-pressed',NAMEN.visible); };
  let raffer=false, off=0, tl=performance.now(); q('raffer').onclick=e=>{ raffer=!raffer; const b=e.currentTarget; b.setAttribute('aria-pressed',raffer); b.innerHTML=raffer?'❚❚<span>Zeitraffer anhalten</span>':'▶<span>Tag im Zeitraffer</span>'; if(!raffer) off=0; };
  q('hoch').oninput=e=>{ ueber=+e.target.value; q('hw').textContent=ueber+'×'; hochSetzen(); };
  const groe=()=>{ const w=el.clientWidth, h=el.clientHeight; r.setSize(w,h,false); cam.aspect=w/h; cam.fov=w<h?52:38; cam.updateProjectionMatrix(); barH=el.querySelector('.k3-bar').offsetHeight+14; if(kuppelG) kuppelG.userData.sm.uniforms.ph.value=h*r.getPixelRatio(); }; d.rs=groe; addEventListener('resize',groe);
  aussen('kuppel',true); groe(); if(el.clientWidth<el.clientHeight){ cam.position.multiplyScalar(1.75); if(ctl) ctl.update(); }
  /* sanfte Kamerafahrt beim Öffnen */
  if(ctl){ const p1=cam.position.clone(); cam.position.set(-p1.z*1.3,p1.y*2.6,p1.z*1.5); ctl.update(); flug={t0:performance.now()+200,p0:cam.position.clone(),z0:ctl.target.clone(),p1,z1:ctl.target.clone(),dauer:2800}; }
  const uhr=q('uhr'); let letzteU='', letzteD=99, bild=0, nahW=0;
  const schritt=t=>{ if(d.aus) return; if(!document.body.contains(el)){ D3=d; scheibe3dZu(); return; } d.raf=requestAnimationFrame(schritt);
    const dt=Math.min(100,t-tl); tl=t; if(raffer) off+=dt/1000*2*3600e3; /* 2 h pro Sekunde */
    const zt=new Date(Date.now()+off), [sl,sp]=sonne(zt), [ax,az]=lagePol(sl,sp), ma=mondAlter(zt), ml=sp*Math.cos(2*Math.PI*ma), [mx,mz]=lagePol(sl-ma*360,ml), ph=2*Math.PI*ma, hell=(1-Math.cos(ph))/2;
    mU.L.value.set(Math.sin(ph),0.15,-Math.cos(ph)).normalize(); MO.sp.intensity=0.15+1.3*hell; MO.g.children[1].material.opacity=0.25+0.75*hell; mKegel.visible=hell>0.08; if(wolken&&wolken.visible) wolken.rotation.z+=dt*0.000012;
    SO.g.position.set(ax,HS,az); SO.sp.target.position.set(ax,0,az); MO.g.position.set(mx,HS*0.92,mz); MO.sp.target.position.set(mx,0,mz); kS.value.set(ax,HS,az);
    if(Math.abs(sp+ml-letzteD)>0.01){ letzteD=sp+ml; const s1=(90-sp)/180*RD, s2=(90-ml)/180*RD; sBahn.scale.set(s1,1,s1); sBahn.position.y=HS; mBahn.scale.set(s2,1,s2); mBahn.position.y=HS*0.92; }
    if(sterneG&&kuppelG.visible){ const jd=zt.getTime()/864e5+2440587.5, gmst=(280.46061837+360.98564736629*(jd-2451545))%360; sterneG.rotation.y=-gmst*R2D; }
    kU.t.value=t/1000; if(flug){ const f=Math.max(0,Math.min(1,(t-flug.t0)/(flug.dauer||1400))), e=f<.5?2*f*f:1-Math.pow(-2*f+2,2)/2; cam.position.lerpVectors(flug.p0,flug.p1,e); ctl.target.lerpVectors(flug.z0,flug.z1,e); if(f>=1){ const n=flug.nach; flug=null; if(n) n(); } }
    if(rund&&ctl){ const w=dt*0.00009, tg=ctl.target, dx=cam.position.x-tg.x, dz=cam.position.z-tg.z, c=Math.cos(w), s=Math.sin(w); cam.position.x=tg.x+dx*c-dz*s; cam.position.z=tg.z+dx*s+dz*c; }
    const u=zt.toLocaleString('de-DE',{day:'2-digit',month:'2-digit',hour:'2-digit',minute:'2-digit'})+' Uhr'; if(u!==letzteU){ uhr.textContent='☀ '+u; letzteU=u; }
    if(ctl) ctl.update(); { const ab=ctl?cam.position.distanceTo(ctl.target):20, n=Math.max(0.04,Math.min(0.5,ab*0.02)); if(Math.abs(n-nahW)>nahW*0.1){ nahW=n; cam.near=n; cam.updateProjectionMatrix(); } }
    if(bild++%4===0) ordnen(); blenden(); r.render(sc,cam); };
  d.raf=requestAnimationFrame(schritt);
}
let letzt=0; function dreh(t){ if(!wrap||!document.body.contains(wrap)) return; if(S.spin&&S.modus==='globus'){ if(t-letzt>31){ S.lam+=Math.min(.4,(t-letzt)*0.0045); letzt=t; S.bewegt=true; zeichne(false); } } else if(S.ov.wander&&t-letzt>80){ letzt=t; zeichne(); }
  if(glAn()&&GL.wolken&&S.ov.wolken&&!RUHE()&&!D3&&t-wzug>110){ GLZ=(GLZ+Math.min(400,t-wzug)*1.1e-6)%1; const still=t-wzug>0&&!(S.spin&&S.modus==='globus'); wzug=t; if(still&&S.grund==='relief') glZeichne(true,false); }
  requestAnimationFrame(dreh); }
let wzug=0;

window.QWWELT={ oeffne(root,ebene){ daten(); let mit3d=false; if(ebene==='scheibe3d'){ mit3d=true; ebene='scheibe'; } if(ebene==='scheibe'){ S.modus='scheibe'; S.zoom=1; S.px=S.py=0; S.ov.nacht=true; ebene=''; } if(ebene){ if(GRUND[ebene]){ S.grund=ebene; if(GRUND[ebene].de){ S.lam=10.4; S.phi=51.2; S.zoom=7; S.spin=false; } } else if(ebene in S.ov) S.ov[ebene]=true; } ui(root); glStart(); schriftLaden(); ereignisse(); requestAnimationFrame(()=>{ groesse(); legende(); info(); }); S.spin=!RUHE()&&!(GRUND[S.grund].de)&&S.modus==='globus'; { const sb=$('[data-spin]',wrap); if(sb) sb.setAttribute('aria-pressed',S.spin); } requestAnimationFrame(dreh); if(mit3d) scheibe3d(); },
  d3:()=>D3, zustand:S, zeichne:()=>zeichne(), legende:()=>legende(), waehle:(i)=>{ const c=DAT.idx[i]; if(c){ waehle(c,c.lp); flieg(c.lp[0],c.lp[1]); } }, flieg:(a,b,z)=>flieg(a,b,z), hist:(a,i)=>{ S.hist=[a,i]; info(); zeichne(); }, grund:k=>grundSetzen(k), bl:c=>{ S.bl=c; info(); zeichne(); } };
})();
