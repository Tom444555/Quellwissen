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
const DEBUND={de_su:12.4,de_dem:null,de_hz:6894,de_aq:58.0};
function deWert(c,k){ const d=DE[c]; if(!d) return null; if(k==='de_su') return d[0]; if(k==='de_hz') return d[5]; if(k==='de_aq') return d[6]; if(k==='de_dem') return d[4]*1000/(d[3]/d[0]*1e5)*100; return null; }
const TIEFEN=[['Marianengraben',142.2,11.35,10935],['Tongagraben',-174.7,-23.25,10800],['Philippinengraben',126.6,10.4,10540],['Kermadecgraben',-177.4,-31.9,10047],['Kurilengraben',152.5,44.2,9600],['Puerto-Rico-Graben',-66.5,19.8,8400],['Südsandwichgraben',-25.0,-56.2,8265],['Atacamagraben',-71.5,-23.4,8065],['Sundagraben',110.0,-10.6,7290],['Molloytief (Arktis)',2.8,79.1,5550],['Calypsotief (Mittelmeer)',21.1,36.6,5267],['Landsorttief (Ostsee)',18.3,58.6,459]];
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
 de_su:{n:'Suizidrate',g:'Deutschland',de:1,e:'🕯️',u:'je 100.000 Ew. · 2024',p:ROT,s:v=>(v-8)/9,lg:['8','12,5','17'],q:'Destatis, Todesursachenstatistik 2024 (Darstellung NaSPro)',l:'#w-suizid'},
 de_dem:{n:'Demenz (65+)',g:'Deutschland',de:1,e:'🧠',u:'Betroffene je 100 Ew. · berechnet',p:MAGMA,s:v=>(v-1.5)/1.2,lg:['1,5','2,1','2,7'],q:'Deutsche Alzheimer Gesellschaft, Infoblatt 1 (Stand 2025); Einwohner aus Destatis',l:'#w-demenz'},
 de_hz:{n:'Straftaten',g:'Deutschland',de:1,e:'🚔',u:'Fälle je 100.000 Ew. · PKS 2024',p:ROT,s:v=>(v-4500)/11000,lg:['4.500','10.000','15.200'],q:'BKA, Polizeiliche Kriminalstatistik 2024',l:'#w-kriminalitaet'},
 de_aq:{n:'Aufklärungs\u00adquote',g:'Deutschland',de:1,e:'🔎',u:'% der Fälle · PKS 2024',p:GRN,s:v=>(v-45)/23,lg:['45 %','56 %','68 %'],q:'BKA, Polizeiliche Kriminalstatistik 2024',l:'#w-kriminalitaet'}};
function ramp(stops,t){ t=Math.max(0,Math.min(1,t)); const n=stops.length-1, k=Math.min(n-1,Math.floor(t*n)), f=t*n-k; const hx=h=>[1,3,5].map(i=>parseInt(h.slice(i,i+2),16)); const a=hx(stops[k]),b=hx(stops[k+1]); return `rgb(${a.map((v,i)=>Math.round(v+(b[i]-v)*f)).join(',')})`; }

/* ---------- Zustand ---------- */
const S={modus:'globus',lam:-15,phi:25,zoom:1,px:0,py:0,grund:'relief',jahr:2023,unterlage:true,
 ov:{namen:true,staedte:true,grenzen:true,fluesse:true,landschaft:false,gipfel:false,weizen:false,mais:false,reis:false,gerste:false,hopfen:false,oel:false,gas:false,kohle:false,gold:false,silber:false,uran:false,lithium:false,pfl:false,rez:false,aut:false,nacht:false,kriege:false,wander:false,erf:false,geld:false,goethe:false,tiefen:false},
 bl:null,
 epoche:'',pflanze:'',sel:null,klick:null,hist:null,spin:true,bewegt:false};
let cv,ctx,W=0,H=0,DPR=1,wrap;

/* ---------- Projektion ---------- */
function radius(){ return Math.min(W,H)*0.42*S.zoom; }
function kf(){ return Math.min(W/360,H/180)*S.zoom; }
function proj(lon,lat){
  if(S.modus==='globus'){ const l=(lon-S.lam)*R2,p=lat*R2,p0=S.phi*R2, r=radius();
    const cosc=Math.sin(p0)*Math.sin(p)+Math.cos(p0)*Math.cos(p)*Math.cos(l);
    return [W/2+r*Math.cos(p)*Math.sin(l), H/2-r*(Math.cos(p0)*Math.sin(p)-Math.sin(p0)*Math.cos(p)*Math.cos(l)), cosc]; }
  const k=kf(); let x=lon-S.lam; x=((x+540)%360)-180; return [W/2+x*k+S.px, H/2-lat*k+S.py, 1]; }
function inv(x,y){
  if(S.modus==='globus'){ const r=radius(), X=(x-W/2)/r, Y=-(y-H/2)/r, rho=Math.hypot(X,Y); if(rho>1) return null; const c=Math.asin(rho), p0=S.phi*R2;
    const lat=Math.asin(Math.cos(c)*Math.sin(p0)+(rho?Y*Math.sin(c)*Math.cos(p0)/rho:0));
    const lon=S.lam*R2+Math.atan2(X*Math.sin(c), rho*Math.cos(p0)*Math.cos(c)-Y*Math.sin(p0)*Math.sin(c));
    return [((lon/R2+540)%360)-180, lat/R2]; }
  const k=kf(); const lon=(x-W/2-S.px)/k+S.lam, lat=-(y-H/2-S.py)/k; if(Math.abs(lat)>90) return null; return [((lon+540)%360)-180,lat]; }
function pfad(ring,offen){
  if(S.modus==='globus'){ const r=radius(); let start=true, sichtbar=false; const pts=ring.map(([a,b])=>proj(a,b));
    for(const q of pts) if(q[2]>0){sichtbar=true;break;} if(!sichtbar) return false;
    if(offen){ for(const q of pts){ if(q[2]<0){start=true;continue;} if(start){ctx.moveTo(q[0],q[1]);start=false;} else ctx.lineTo(q[0],q[1]); } return true; }
    for(const q of pts){ let x=q[0],y=q[1]; if(q[2]<0){ const dx=x-W/2,dy=y-H/2,d=Math.hypot(dx,dy)||1; x=W/2+dx/d*r; y=H/2+dy/d*r; }
      if(start){ctx.moveTo(x,y);start=false;} else ctx.lineTo(x,y); } ctx.closePath(); return true; }
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
function farbe(i){ const g=GRUND[S.grund]; if(!g.p) return null; const v=wert(i,S.grund,S.jahr); return v==null?null:ramp(g.p,g.s(v)); }
function fmt(v,d=0){ return v==null?'–':v.toLocaleString('de-DE',{maximumFractionDigits:d,minimumFractionDigits:d}); }
function zstufe(){ return 2.2+2.4*Math.log2(Math.max(S.zoom,.5)); }

/* ---------- Relief (Textur) ---------- */
let TEX=null, TW=0, TH=0, RC=null, RKEY='', RTIMER=null;
function textur(){ if(TEX!==null) return; TEX=false; const el=document.getElementById('weltrelief'); if(!el) return; const im=new Image(); im.onload=()=>{ const c=document.createElement('canvas'); TW=c.width=im.width; TH=c.height=im.height; const x=c.getContext('2d'); x.drawImage(im,0,0); TEX=x.getImageData(0,0,TW,TH).data; RKEY=''; zeichne(); }; im.src='data:image/jpeg;base64,'+el.textContent.trim(); }
function relief(fein){
  if(!TEX) return null; const s=fein?Math.min(DPR,1.5):0.5, w=Math.max(1,Math.round(W*s)), h=Math.max(1,Math.round(H*s)); const key=[S.modus,S.lam.toFixed(2),S.phi.toFixed(2),S.zoom.toFixed(3),S.px|0,S.py|0,w,h].join('|');
  if(key===RKEY&&RC) return RC; if(!RC) RC=document.createElement('canvas'); RC.width=w; RC.height=h; const x=RC.getContext('2d'); const img=x.createImageData(w,h), d=img.data;
  if(S.modus==='globus'){ const r=radius()*s, cx=W/2*s, cy=H/2*s, p0=S.phi*R2, sp=Math.sin(p0), cp=Math.cos(p0), l0=S.lam*R2;
    const y0=Math.max(0,Math.floor(cy-r)), y1=Math.min(h-1,Math.ceil(cy+r));
    for(let py=y0;py<=y1;py++){ const Y=-(py-cy)/r; const xx=Math.sqrt(Math.max(0,1-Y*Y))*r; const x0=Math.max(0,Math.floor(cx-xx)), x1=Math.min(w-1,Math.ceil(cx+xx));
      for(let px=x0;px<=x1;px++){ const X=(px-cx)/r, rr=X*X+Y*Y; if(rr>1) continue; const z=Math.sqrt(1-rr);
        const lat=Math.asin(z*sp+Y*cp), lon=l0+Math.atan2(X, z*cp-Y*sp);
        let u=((lon/(2*Math.PI)+0.5)%1+1)%1, v=0.5-lat/Math.PI; const tx=(u*TW)|0, ty=Math.min(TH-1,(v*TH)|0), ti=(ty*TW+tx)*4, o=(py*w+px)*4;
        const sh=0.55+0.45*z; d[o]=TEX[ti]*sh; d[o+1]=TEX[ti+1]*sh; d[o+2]=TEX[ti+2]*sh; d[o+3]=255; } } }
  else { const k=kf()*s; for(let py=0;py<h;py++){ const lat=-((py-H/2*s-S.py*s)/k); if(lat>90||lat<-90) continue; const ty=Math.min(TH-1,((0.5-lat/180)*TH)|0);
      for(let px=0;px<w;px++){ const lon=(px-W/2*s-S.px*s)/k+S.lam; const u=(((lon+180)/360)%1+1)%1, ti=(ty*TW+((u*TW)|0))*4, o=(py*w+px)*4; d[o]=TEX[ti]; d[o+1]=TEX[ti+1]; d[o+2]=TEX[ti+2]; d[o+3]=255; } } }
  x.putImageData(img,0,0); RKEY=key; return RC; }

/* ---------- Zeichnen ---------- */
let sterne=null, BOX=[];
function zeichne(fein){
  if(!ctx) return; BOX=[]; ctx.setTransform(DPR,0,0,DPR,0,0); ctx.clearRect(0,0,W,H);
  const g0=ctx.createRadialGradient(W/2,H/2,0,W/2,H/2,Math.max(W,H)*0.8); g0.addColorStop(0,'#0e1a30'); g0.addColorStop(1,'#04070e'); ctx.fillStyle=g0; ctx.fillRect(0,0,W,H);
  if(!sterne){ sterne=[]; let s=7; const r=()=>(s=(s*16807)%2147483647)/2147483647; for(let i=0;i<260;i++) sterne.push([r(),r(),r()*1.2+.2,r()]); }
  sterne.forEach(([x,y,z,a])=>{ ctx.fillStyle=`rgba(200,220,255,${a*.6})`; ctx.fillRect(x*W,y*H,z,z); });
  const r=radius(), glob=S.modus==='globus', G=GRUND[S.grund], rast=G.r, mitRelief=S.grund==='relief'||(S.unterlage&&!rast);
  if(glob){ const at=ctx.createRadialGradient(W/2,H/2,r*0.92,W/2,H/2,r*1.18); at.addColorStop(0,'rgba(80,170,255,.55)'); at.addColorStop(.35,'rgba(60,140,255,.18)'); at.addColorStop(1,'rgba(40,100,255,0)'); ctx.fillStyle=at; ctx.beginPath(); ctx.arc(W/2,H/2,r*1.18,0,7); ctx.fill();
    const oz=ctx.createRadialGradient(W/2-r*.35,H/2-r*.4,r*.1,W/2,H/2,r); oz.addColorStop(0,'#1d4f86'); oz.addColorStop(.6,'#0c2c52'); oz.addColorStop(1,'#071a33'); ctx.fillStyle=oz; ctx.beginPath(); ctx.arc(W/2,H/2,r,0,7); ctx.fill();
    ctx.save(); ctx.beginPath(); ctx.arc(W/2,H/2,r,0,7); ctx.clip(); }
  else { ctx.fillStyle='#0a2240'; const a=proj(-180,90),b=proj(180,-90); ctx.fillRect(0,a[1],W,b[1]-a[1]); }
  if(mitRelief){ textur(); const rc=relief(fein!==false&&!S.bewegt); if(rc){ ctx.imageSmoothingEnabled=true; ctx.drawImage(rc,0,0,W,H); if(!fein&&!S.bewegt){} } }
  // Gradnetz
  ctx.strokeStyle=mitRelief?'rgba(255,255,255,.08)':'rgba(140,190,255,.10)'; ctx.lineWidth=.7;
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
  if(S.ov.fluesse){ ctx.fillStyle=mitRelief?'rgba(30,80,140,.9)':'#0c2c52'; DAT.seen.forEach(([n,rg])=>{ ctx.beginPath(); if(pfad(rg)) ctx.fill(); });
    const zs=zstufe(); ctx.strokeStyle=mitRelief?'rgba(90,170,255,.85)':'rgba(90,170,255,.55)'; DAT.fluesse.forEach(([sr,n,l])=>{ if(sr>zs+3) return; ctx.lineWidth=Math.max(.5,2-sr*0.18)*Math.min(1.6,Math.sqrt(S.zoom)); ctx.beginPath(); if(pfad(l,true)) ctx.stroke(); }); }
  if(S.pflanze){ const P=PFL[S.pflanze]; ctx.fillStyle='rgba(120,255,170,.55)'; DAT.raster.forEach(g=>{ if(g[5]||!inBereich(P,g)) return; const q=proj(g[0],g[1]); if(q[2]<0.05) return; ctx.beginPath(); ctx.arc(q[0],q[1],Math.max(1.4,radius()/260*S.zoom),0,7); ctx.fill(); }); }
  // Grenzen
  if(S.ov.grenzen){ ctx.strokeStyle=mitRelief?'rgba(255,255,255,.55)':'rgba(220,235,255,.25)'; ctx.lineWidth=mitRelief?.8:.6; ctx.setLineDash(mitRelief?[3,2]:[]);
    DAT.laender.forEach(c=>{ ctx.beginPath(); let ok=false; c.p.forEach(rg=>{ if(pfad(rg)) ok=true; }); if(ok) ctx.stroke(); }); ctx.setLineDash([]); }
  if(S.sel){ const c=DAT.idx[S.sel]; ctx.beginPath(); c.p.forEach(rg=>pfad(rg)); ctx.strokeStyle='#fff'; ctx.lineWidth=2.2; ctx.shadowColor='rgba(120,200,255,.9)'; ctx.shadowBlur=12; ctx.stroke(); ctx.shadowBlur=0; }
  if(S.ov.nacht) nacht();
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
  if(G.de&&DAT.bl&&S.zoom>3.5){ const big=S.zoom>6; DAT.bl.slice().reverse().forEach(b=>{ const q=proj(b.lp[0],b.lp[1]); if(q[2]<0.2) return; const v=deWert(b.i,S.grund); const kurz=['BE','HB','HH'].includes(b.i); text(big&&!kurz?b.n:b.i,q[0],q[1]-2,big?11.5:10.5,'#ffffff',true,'700'); if(v!=null) text(fmt(v,S.grund==='de_hz'?0:1),q[0],q[1]+11,10.5,'#ffe8c0',true,'600'); }); }
  // Beschriftung: Landschaften, Gipfel, Länder, Städte
  const zs=zstufe();
  if(S.ov.landschaft) DAT.regionen.forEach(([n,k,lo,la,sr])=>{ if(sr>zs+0.5) return; const q=proj(lo,la); if(q[2]<0.2) return; text(n.toUpperCase(),q[0],q[1],10,k==='Range/mtn'?'#f0d8b8':k==='Desert'?'#ffe0a0':'#d8e8c8',true,'italic 600'); });
  if(S.ov.gipfel) DAT.gipfel.forEach(([n,lo,la,hm,sr])=>{ if(sr>zs+1) return; const q=proj(lo,la); if(q[2]<0.15) return; ctx.fillStyle='#fff'; ctx.beginPath(); ctx.moveTo(q[0],q[1]-5); ctx.lineTo(q[0]+4,q[1]+2); ctx.lineTo(q[0]-4,q[1]+2); ctx.closePath(); ctx.fill(); text(`${n} ${fmt(hm)} m`,q[0]+6,q[1]+3,10,'#ffffff'); });
  if(S.ov.namen) DAT.laender.slice().sort((a,b)=>a.lr-b.lr).forEach(c=>{ if(c.lr>zs||(G.de&&c.i==='DEU')) return; const q=proj(c.lp[0],c.lp[1]); if(q[2]<0.25) return; text(c.n,q[0],q[1],c.lr<3?13:c.lr<4.5?11.5:10.5,'#ffffff',true,'700'); });
  if(S.ov.staedte) DAT.staedte.forEach(([n,lo,la,p,mz,hs])=>{ if(mz>zs) return; const q=proj(lo,la); if(q[2]<0.15) return; const R=1.6+Math.sqrt(Math.max(p,.1))*0.8; if(!frei(q[0]-R,q[1]+R,R*2,R*2)) return; if(!text(n,q[0]+R+3,q[1]+4,10.5,'#fff3d8')) return; BOX.push([q[0]-R,q[1]+R,R*2,R*2]); ctx.fillStyle=hs?'#ffd860':'#ffe9b8'; ctx.strokeStyle='rgba(0,0,0,.7)'; ctx.lineWidth=1; ctx.beginPath(); if(hs) ctx.rect(q[0]-R,q[1]-R,R*2,R*2); else ctx.arc(q[0],q[1],R,0,7); ctx.fill(); ctx.stroke(); });
  if(S.ov.tiefen) TIEFEN.forEach(([n,lo,la,t])=>{ const q=proj(lo,la); if(q[2]<0.15) return; ctx.fillStyle='#7fe0ff'; ctx.strokeStyle='#02101e'; ctx.lineWidth=1.2; ctx.beginPath(); ctx.moveTo(q[0]-5,q[1]-4); ctx.lineTo(q[0]+5,q[1]-4); ctx.lineTo(q[0],q[1]+4); ctx.closePath(); ctx.fill(); ctx.stroke(); text(`${n} −${fmt(t)} m`,q[0]+7,q[1]+4,10.5,'#bff0ff'); });
  if(S.klick){ const q=proj(S.klick[0],S.klick[1]); if(q[2]>0){ ctx.strokeStyle='#fff'; ctx.lineWidth=2; ctx.beginPath(); ctx.arc(q[0],q[1],6,0,7); ctx.stroke(); } }
  if(glob){ ctx.restore(); const sh=ctx.createRadialGradient(W/2-r*.35,H/2-r*.4,r*.2,W/2,H/2,r*1.02); sh.addColorStop(0,'rgba(255,255,255,.07)'); sh.addColorStop(.7,'rgba(0,0,0,0)'); sh.addColorStop(1,'rgba(0,5,20,.55)'); ctx.fillStyle=sh; ctx.beginPath(); ctx.arc(W/2,H/2,r,0,7); ctx.fill();
    ctx.strokeStyle='rgba(140,200,255,.35)'; ctx.lineWidth=1.2; ctx.beginPath(); ctx.arc(W/2,H/2,r,0,7); ctx.stroke(); }
  if(mitRelief&&(S.bewegt||fein===false)){ clearTimeout(RTIMER); RTIMER=setTimeout(()=>{ S.bewegt=false; zeichne(true); },160); }
}
function text(t,x,y,s=11.5,col='#eaf2ff',mitte,gew='600'){ ctx.font=`${gew} ${s}px system-ui,-apple-system,Segoe UI,Roboto,sans-serif`; const w=ctx.measureText(t).width; if(mitte) x-=w/2;
  if(x<-w||x>W||y<0||y>H+10) return false; if(frei(x,y,w,s)===false) return false; BOX.push([x,y,w,s]);
  ctx.lineWidth=3.2; ctx.strokeStyle='rgba(4,8,16,.85)'; ctx.lineJoin='round'; ctx.strokeText(t,x,y); ctx.fillStyle=col; ctx.fillText(t,x,y); return true; }
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
function sonne(){ const d=new Date(), t=(Date.UTC(d.getUTCFullYear(),d.getUTCMonth(),d.getUTCDate())-Date.UTC(d.getUTCFullYear(),0,0))/864e5; const dekl=-23.44*Math.cos(2*Math.PI/365*(t+10)); const h=d.getUTCHours()+d.getUTCMinutes()/60; return [(12-h)*15,dekl]; }
function nacht(){ const [sl,sp]=sonne(); const al=sl+180, ap=-sp; const pts=[]; for(let i=0;i<=180;i++){ const b=i*2*R2, d=90*R2, p1=ap*R2, l1=al*R2; const la=Math.asin(Math.sin(p1)*Math.cos(d)+Math.cos(p1)*Math.sin(d)*Math.cos(b)); const lo=l1+Math.atan2(Math.sin(b)*Math.sin(d)*Math.cos(p1),Math.cos(d)-Math.sin(p1)*Math.sin(la)); pts.push([((lo/R2+540)%360)-180,la/R2]); }
  if(S.modus==='globus'){ ctx.beginPath(); pfad(pts); ctx.fillStyle='rgba(2,6,20,.55)'; ctx.fill(); }
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
  return `<svg viewBox="0 0 ${w} ${h}" class="qwk-spark"><defs><linearGradient id="qwsg" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#4ad0a0" stop-opacity=".45"/><stop offset="1" stop-color="#4ad0a0" stop-opacity="0"/></linearGradient></defs><path d="${d}L${w},${h}L0,${h}Z" fill="url(#qwsg)"/><path d="${d}" fill="none" stroke="#4ad0a0" stroke-width="2"/><circle cx="${cx}" cy="${cy}" r="3.5" fill="#fff"/></svg>`; }
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
function balken(k,hl){ const G=GRUND[k], arr=Object.keys(DE).map(c=>[c,deWert(c,k)]).sort((a,b)=>b[1]-a[1]), mx=Math.max(...arr.map(a=>a[1])), name=c=>((DAT.bl||[]).find(b=>b.i===c)||{n:c}).n, bund=DEBUND[k];
  return `<div class="qwk-bars">${arr.map(([c,v])=>`<div class="${c===hl?'hl':''}" data-bl="${c}"><span>${name(c)}</span><i><b style="width:${(v/mx*100).toFixed(1)}%;background:${ramp(G.p,G.s(v))}"></b></i><em>${fmt(v,k==='de_hz'?0:1)}</em></div>`).join('')}${bund!=null?`<div class="bund"><span>Deutschland</span><i><b style="width:${(bund/mx*100).toFixed(1)}%"></b></i><em>${fmt(bund,k==='de_hz'?0:1)}</em></div>`:''}</div>`; }
function infoBL(){ const box=$('.qwk-info',wrap), b=DAT.bl.find(x=>x.i===S.bl), d=DE[S.bl], G=GRUND[S.grund], ew=d[3]/d[0]*1e5;
  const rang=k=>{ const a=Object.keys(DE).map(c=>deWert(c,k)).sort((x,y)=>y-x); return a.indexOf(deWert(S.bl,k))+1; };
  box.innerHTML=`<div class="qwk-kopf"><span class="qwk-flag">🇩🇪</span><div><h2>${b.n}</h2><small>Bundesland · ca. ${fmt(ew/1e6,2)} Mio. Einwohner</small></div><button class="qwk-x" aria-label="Schließen">✕</button></div>
  <div class="qwk-kpi"><div><small>🕯️ Suizidrate 2024</small><b>${fmt(d[0],1)}</b> <i>je 100.000 · Rang ${rang('de_su')}/16</i></div><div><small>🧠 Demenz 65+</small><b>${fmt(d[4])} Tsd.</b> <i>${fmt(deWert(S.bl,'de_dem'),1)} je 100 Ew.</i></div><div><small>🚔 Straftaten 2024</small><b>${fmt(d[5])}</b> <i>je 100.000 · Rang ${rang('de_hz')}/16</i></div><div><small>🔎 Aufklärung</small><b>${fmt(d[6],1)} %</b> <i>Rang ${rang('de_aq')}/16</i></div></div>
  <div class="qwk-box"><small>Suizide 2024: ${fmt(d[3])} (Männer ${fmt(d[1],1)}, Frauen ${fmt(d[2],1)} je 100.000)</small></div>
  <h4>${G.e} ${G.n} – alle Länder</h4>${balken(S.grund,S.bl)}
  <div>${chip('📖 Suizid','#w-suizid','k')}${chip('📖 Demenz','#w-demenz','k')}${chip('📖 Kriminalität','#w-kriminalitaet','k')}</div><p class="qwk-hin2">Quelle: ${G.q}. Einwohner aus Suizidzahl und -rate errechnet.</p>`;
  box.querySelectorAll('[data-bl]').forEach(r=>r.onclick=()=>{ S.bl=r.dataset.bl; infoBL(); zeichne(); });
  $('.qwk-x',box).onclick=()=>{ S.bl=null; info(); zeichne(); wrap.classList.remove('qwk-info-auf'); }; }
function info(){
  const box=$('.qwk-info',wrap); if(S.hist) return infoHist(); if(S.bl&&GRUND[S.grund].de) return infoBL(); if(!S.sel&&GRUND[S.grund].de){ box.innerHTML=`<div class="qwk-kopf"><span class="qwk-flag">🇩🇪</span><div><h2>${GRUND[S.grund].n}</h2><small>${GRUND[S.grund].u}</small></div></div>${balken(S.grund)}<p class="qwk-hin2">Bundesland antippen für alle Werte. Quelle: ${GRUND[S.grund].q}</p><div>${chip('📖 Mehr dazu',GRUND[S.grund].l,'k')}</div>`; box.querySelectorAll('[data-bl]').forEach(r=>r.onclick=()=>{ S.bl=r.dataset.bl; infoBL(); zeichne(); }); return; }
  if(!S.sel){ box.innerHTML=`<div class="qwk-leer"><div class="qwk-gl">🌍</div><b>Land antippen</b><p>Tippe auf ein Land, um Einwohner, Dichte, Lebenserwartung, Ernten, Rohstoffe und passende Kapitel aus dem Kompendium zu sehen.</p><p class="qwk-mini">Ziehen = drehen · Zwei Finger oder Mausrad = zoomen · Beim Hineinzoomen erscheinen Städte, Flüsse und Landschaften</p></div>`; return; }
  const c=DAT.idx[S.sel], i=c.i, j=S.jahr, o=ow(i);
  const pop=wert(i,'pop',j), di=wert(i,'dichte',j), wa=wert(i,'wachstum',j);
  let h=`<div class="qwk-kopf"><span class="qwk-flag">${c.f||'🏳️'}</span><div><h2>${c.n}</h2><small>Stand ${j}${S.klick?` · ${fmt(Math.abs(S.klick[1]),1)}° ${S.klick[1]>=0?'N':'S'}, ${fmt(Math.abs(S.klick[0]),1)}° ${S.klick[0]>=0?'O':'W'}`:''}</small></div><button class="qwk-x" aria-label="Schließen">✕</button></div>
  <div class="qwk-kpi"><div><small>Einwohner</small><b>${pop?pop>=1e6?fmt(pop/1e6,2)+' Mrd.':pop>=1000?fmt(pop/1000,1)+' Mio.':fmt(pop)+' Tsd.':'–'}</b></div><div><small>Dichte</small><b>${fmt(di)} <i>/km²</i></b></div><div><small>Wachstum</small><b class="${wa>0?'plus':'minus'}">${wa==null?'–':(wa>0?'+':'')+fmt(wa,1)+' %'}</b></div><div><small>Fläche (ca.)</small><b>${fmt(c.a/1000)} <i>Tsd. km²</i></b></div></div>
  <div class="qwk-box"><small>Bevölkerung 1960–2023</small>${spark(i)}</div>`;
  const ges=[['le','❤️ Lebenserwartung',v=>fmt(v,1)+' Jahre'],['fr','👶 Geburtenrate',v=>fmt(v,2)+' Kinder je Frau'],['km','🍼 Kindersterblichkeit',v=>fmt(v)+' je 1.000'],['su','🕯️ Suizidrate',v=>fmt(v,1)+' je 100.000'],['gl','😊 Lebenszufriedenheit',v=>fmt(v,1)+' von 10'],['un','🥣 Unterernährung',v=>fmt(v,1)+' %']].map(([k,n,f])=>{ const v=wert(i,k,j), st=stand(i,k,j); return v==null?'':chip(`${n}: ${f(v)}${st&&st!==j?` (${st})`:''}`); }).join('');
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
  if(i==='DEU') h+=`<h4>Deutschland nach Bundesländern</h4><div>${['de_su','de_dem','de_hz','de_aq'].map(k=>`<button class="qwk-chip k" data-dek="${k}">${GRUND[k].e} ${GRUND[k].n.replace('\u00ad','')}</button>`).join('')}</div>`;
  const kp=[...pf,...rz,...au]; if(kp.length) h+=`<h4>Im Kompendium</h4><div>${kp.join('')}</div>`;
  box.innerHTML=h; box.querySelectorAll('[data-dek]').forEach(b=>b.onclick=()=>grundSetzen(b.dataset.dek)); $('.qwk-x',box).onclick=()=>{ S.sel=null; S.klick=null; info(); zeichne(); wrap.classList.remove('qwk-info-auf'); };
}

/* ---------- Legende ---------- */
function legende(){
  const g=GRUND[S.grund], L=$('.qwk-leg',wrap); let h=`<b>${g.e} ${g.n}</b>${g.u?` <span class="qwk-u">${g.u}</span>`:''}`;
  if(g.p) h+=`<div class="qwk-ramp" style="background:linear-gradient(90deg,${g.p.join(',')})"></div><div class="qwk-rl"><span>${g.lg[0]}</span><span>${g.lg[1]}</span><span>${g.lg[2]}</span></div>`;
  else if(g.r){ const t=g.r===2?KLIMA:g.r===3?BODEN:VEGN; h+=`<div class="qwk-kl">${Object.values(t).map(([n,c])=>`<span><i style="background:${c}"></i>${n}</span>`).join('')}</div><div class="qwk-hin">Vereinfachtes Schema (2°-Raster), keine Messkarte</div>`; }
  else if(S.grund==='relief') h+=`<div class="qwk-ramp" style="background:linear-gradient(90deg,#4e7842,#b0aa70,#aa8a60,#8c6c56,#f6f4f0)"></div><div class="qwk-rl"><span>Tiefland</span><span>Hochland</span><span>Hochgebirge, Eis</span></div>`;
  if(g.de) h+=`<div class="qwk-hin">Quelle: ${g.q}</div>`;
  if(S.grund==='relief') h+=`<div class="qwk-ramp" style="background:linear-gradient(90deg,#468cb9,#1e508a,#133768,#081a40,#05112e)"></div><div class="qwk-rl"><span>Schelf 0–200 m</span><span>4.000 m</span><span>über 8.000 m</span></div>`;
  if(S.grund==='su') h+=`<div class="qwk-hin">Mittel aus Männer- und Frauenrate (IHME). Hilfe in Deutschland: Telefonseelsorge 0800 111 0 111</div>`;
  const ov=[]; Object.entries(GETREIDE).forEach(([k,G2])=>S.ov[k]&&ov.push(`<span><i class="r" style="background:${G2.c}"></i>${G2.n}</span>`)); Object.entries(ROH).forEach(([k,G2])=>S.ov[k]&&ov.push(`<span><i class="d" style="background:${G2.c}"></i>${G2.n}</span>`));
  if(S.ov.kriege) ov.push('<span><i class="r" style="background:#d8302a"></i>Kriege</span>'); if(S.ov.wander) ov.push('<span><i class="l"></i>Wanderungen</span>'); if(S.ov.erf) ov.push('<span><i class="r" style="background:#ffe14a"></i>Erfindungen</span>'); if(S.ov.geld) ov.push('<span><i class="r" style="background:#e8b030"></i>Geldgeschichte</span>'); if(S.ov.tiefen) ov.push('<span><i class="d" style="background:#7fe0ff"></i>Tiefseegräben (tiefste Stellen, ca.)</span>'); if(S.ov.goethe) ov.push('<span><i class="r" style="background:#ff8c6e"></i>Goethe (Größe = Dauer)</span>');
  if(S.ov.pfl) ov.push('<span><i class="r" style="background:#ff6a8a"></i>Pflanzen-Herkunft</span>'); if(S.ov.rez) ov.push('<span><i class="r" style="background:#c79aff"></i>Rezepte</span>'); if(S.ov.aut) ov.push('<span><i class="r" style="background:#6ac8ff"></i>Autoren</span>');
  if(ov.length) h+=`<div class="qwk-kl qwk-ov">${ov.join('')}</div>`;
  L.innerHTML=h; }

/* ---------- Oberfläche ---------- */
const CSS=`
.qwk{--k-bg:#060a13;--k-p:#0c1322;--k-p2:#111a2d;--k-l:#1f2b44;--k-t:#e8eefb;--k-m:#8d9ab8;--k-a:#4ad0a0;position:relative;display:grid;grid-template-columns:300px 1fr 340px;grid-template-rows:auto 1fr auto;height:calc(100vh - 120px);min-height:560px;background:var(--k-bg);color:var(--k-t);border-radius:18px;overflow:hidden;font:14px system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;box-shadow:0 20px 60px rgba(0,0,0,.35);width:calc(100vw - 32px);max-width:1800px;margin-left:calc(50% - min(50vw - 16px, 900px))}
.qwk *{box-sizing:border-box}
.qwk-top{grid-column:1/4;display:flex;align-items:center;gap:12px;padding:12px 16px;background:linear-gradient(180deg,#0c1426,#0a101d);border-bottom:1px solid var(--k-l);flex-wrap:wrap}
.qwk-titel{display:flex;align-items:center;gap:10px;font:700 18px Georgia,serif}.qwk-gl2{width:30px;height:30px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#7ad8ff,#1b4f8a 60%,#08203e);box-shadow:0 0 14px rgba(80,170,255,.6)}
.qwk-titel small{display:block;font:500 11.5px system-ui;color:var(--k-m)}
.qwk-seg{display:inline-flex;background:#0a1120;border:1px solid var(--k-l);border-radius:12px;padding:3px;gap:2px}
.qwk-seg button{all:unset;cursor:pointer;padding:7px 12px;border-radius:9px;color:var(--k-m);font-weight:600;font-size:13px;transition:.2s}
.qwk-seg button[aria-pressed=true]{background:linear-gradient(180deg,#1d3a5c,#15304e);color:#fff;box-shadow:inset 0 0 0 1px #2e5b8a,0 4px 14px rgba(40,120,220,.25)}
.qwk-such{margin-left:auto;position:relative}.qwk-such input{all:unset;box-sizing:border-box;width:250px;padding:9px 12px 9px 34px;background:#0a1120;border:1px solid var(--k-l);border-radius:12px;color:var(--k-t);font-size:13.5px}.qwk-such:before{content:"⌕";position:absolute;left:12px;top:6px;color:var(--k-m);font-size:18px}
.qwk-side{background:var(--k-p);border-right:1px solid var(--k-l);overflow:auto;padding:10px 14px 20px}
.qwk-side h3{font:700 10.5px system-ui;letter-spacing:.14em;text-transform:uppercase;color:var(--k-m);margin:16px 2px 8px;display:flex;align-items:center;gap:8px}.qwk-side h3:after{content:"";flex:1;height:1px;background:var(--k-l)}
.qwk-grund{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px}.qwk-grund button span:last-child{hyphens:auto;-webkit-hyphens:auto}
.qwk-grund button{all:unset;display:flex;gap:6px;align-items:center;cursor:pointer;padding:8px 9px;line-height:1.25;border-radius:11px;background:var(--k-p2);border:1px solid var(--k-l);font-size:12.3px;font-weight:600;color:#cdd6ea;transition:.18s}
.qwk-grund button:hover{border-color:#36507a}.qwk-grund button[aria-pressed=true]{background:linear-gradient(180deg,#123a34,#0f2e2a);border-color:var(--k-a);color:#fff;box-shadow:0 0 0 1px rgba(74,208,160,.25),0 6px 18px rgba(74,208,160,.15)}
.qwk-sw{display:flex;align-items:center;gap:10px;padding:6px 4px;border-radius:9px;cursor:pointer;font-size:13.3px;user-select:none}.qwk-sw:hover{background:rgba(255,255,255,.03)}
.qwk-sw input{display:none}.qwk-sw .k{width:36px;height:21px;border-radius:12px;background:#1a2438;border:1px solid #2a3858;position:relative;flex:none;transition:.2s}.qwk-sw .k:after{content:"";position:absolute;top:2px;left:2px;width:15px;height:15px;border-radius:50%;background:#6a7898;transition:.2s}
.qwk-sw input:checked+.k{background:linear-gradient(90deg,#1f8a6a,#4ad0a0);border-color:#4ad0a0;box-shadow:0 0 12px rgba(74,208,160,.35)}.qwk-sw input:checked+.k:after{left:17px;background:#fff}
.qwk-sw .dt{width:10px;height:10px;border-radius:50%;flex:none;box-shadow:0 0 8px currentColor}.qwk-sw .dt.d{border-radius:2px;transform:rotate(45deg)}
.qwk-sel{all:unset;box-sizing:border-box;width:100%;padding:9px 10px;background:var(--k-p2);border:1px solid var(--k-l);border-radius:11px;font-size:13px;color:var(--k-t);margin:6px 0}
.qwk-map{position:relative;overflow:hidden;touch-action:none;cursor:grab}.qwk-map:active{cursor:grabbing}.qwk-map canvas{display:block;width:100%;height:100%}
.qwk-zoom{position:absolute;right:14px;top:14px;display:flex;flex-direction:column;gap:6px}.qwk-zoom button{all:unset;cursor:pointer;width:38px;height:38px;border-radius:12px;background:rgba(12,19,34,.85);border:1px solid var(--k-l);display:grid;place-items:center;font-size:17px;color:#dfe8fa;backdrop-filter:blur(6px)}.qwk-zoom button:hover{border-color:var(--k-a)}
.qwk-leg{position:absolute;left:14px;bottom:14px;max-width:340px;background:rgba(10,16,30,.86);backdrop-filter:blur(8px);border:1px solid var(--k-l);border-radius:14px;padding:10px 12px;font-size:12px}.qwk-u{color:var(--k-m);font-size:11px}
.qwk-ramp{height:9px;border-radius:5px;margin:7px 0 4px;width:250px}.qwk-rl{display:flex;justify-content:space-between;color:var(--k-m);width:250px}
.qwk-kl{display:flex;flex-wrap:wrap;gap:4px 10px;margin-top:7px}.qwk-kl span{display:flex;align-items:center;gap:5px;color:#cdd6ea}.qwk-kl i{width:10px;height:10px;border-radius:3px;display:inline-block}.qwk-kl i.r{border-radius:50%}.qwk-kl i.d{transform:rotate(45deg);border-radius:1px}.qwk-kl i.l{height:0;width:16px;border-top:2px dashed #ffd28a;border-radius:0}
.qwk-ov{border-top:1px solid var(--k-l);padding-top:7px}.qwk-hin{color:var(--k-m);font-size:11px;margin-top:5px;max-width:300px}
.qwk-info{background:var(--k-p);border-left:1px solid var(--k-l);overflow:auto;padding:16px}
.qwk-kopf{display:flex;align-items:center;gap:12px;margin-bottom:12px}.qwk-flag{font-size:30px}.qwk-kopf h2{margin:0;font:700 20px Georgia,serif;color:#fff}.qwk-kopf small{color:var(--k-m)}
.qwk-x{all:unset;cursor:pointer;margin-left:auto;width:30px;height:30px;border-radius:9px;display:grid;place-items:center;color:var(--k-m);border:1px solid var(--k-l)}
.qwk-kpi{display:grid;grid-template-columns:1fr 1fr;gap:8px}.qwk-kpi div{background:var(--k-p2);border:1px solid var(--k-l);border-radius:12px;padding:9px 10px}.qwk-kpi small{display:block;color:var(--k-m);font-size:11px}.qwk-kpi b{font-size:17px;color:#fff}.qwk-kpi i{font-style:normal;font-size:11px;color:var(--k-m);font-weight:500}.qwk-kpi .plus{color:#ffb070}.qwk-kpi .minus{color:#7fb4ff}
.qwk-box{background:var(--k-p2);border:1px solid var(--k-l);border-radius:12px;padding:9px 10px;margin-top:8px}.qwk-box small{color:var(--k-m);font-size:11px}.qwk-spark{width:100%;height:56px;display:block;margin-top:4px}
.qwk-info h4{font:700 10.5px system-ui;letter-spacing:.14em;text-transform:uppercase;color:var(--k-m);margin:14px 0 7px}
.qwk-txt{line-height:1.5;color:#dbe4f6;margin:0 0 8px}.qwk-hin2{color:var(--k-m);font-size:11.5px;margin-top:10px}
.qwk-chip{display:inline-block;padding:5px 10px;margin:0 5px 6px 0;border-radius:20px;background:var(--k-p2);border:1px solid var(--k-l);color:#dbe4f6;font-size:12.5px;text-decoration:none}.qwk-chip.k{background:rgba(74,208,160,.1);border-color:rgba(74,208,160,.45);color:#a9f0d4}a.qwk-chip:hover{border-color:var(--k-a)}
.qwk-leer{text-align:center;color:var(--k-m);padding:30px 10px}.qwk-leer b{color:#fff;font-size:16px}.qwk-gl{font-size:40px;margin-bottom:8px}.qwk-mini{font-size:12px}
.qwk-zeit{grid-column:1/4;display:flex;align-items:center;gap:14px;padding:10px 18px;background:#0a101d;border-top:1px solid var(--k-l)}
.qwk-play{all:unset;cursor:pointer;width:38px;height:38px;border-radius:50%;background:linear-gradient(180deg,#1f8a6a,#14664e);display:grid;place-items:center;box-shadow:0 0 14px rgba(74,208,160,.35);font-size:14px}
.qwk-zeit input{flex:1;accent-color:#4ad0a0}.qwk-jahr{font:700 22px Georgia,serif;min-width:64px;text-align:right}.qwk-q{color:var(--k-m);font-size:10.5px;max-width:540px;line-height:1.35}
.qwk-bars{display:flex;flex-direction:column;gap:3px;margin:4px 0 10px}.qwk-bars div{display:grid;grid-template-columns:118px 1fr 52px;align-items:center;gap:7px;font-size:11.8px;color:#cdd6ea;cursor:pointer;padding:1px 3px;border-radius:6px}.qwk-bars div:hover,.qwk-bars .hl{background:rgba(255,255,255,.07);color:#fff;font-weight:700}.qwk-bars span{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.qwk-bars i{height:11px;background:#141d30;border-radius:6px;overflow:hidden}.qwk-bars i b{display:block;height:100%;border-radius:6px;animation:qwkbar .8s ease-out}.qwk-bars em{font-style:normal;text-align:right;font-variant-numeric:tabular-nums}.qwk-bars .bund{border-top:1px dashed #2a3858;margin-top:3px;padding-top:4px;color:#fff}.qwk-bars .bund b{background:repeating-linear-gradient(45deg,#8d9ab8 0 4px,#5a6888 4px 8px)}@keyframes qwkbar{from{width:0}}
.qwk-mob{display:none}
@media (max-width:980px){.qwk{grid-template-columns:1fr;grid-template-rows:auto minmax(440px,1fr) auto;height:calc(100vh - 16px);width:calc(100vw - 16px);margin-left:calc(50% - 50vw + 8px);border-radius:14px}.qwk-top{grid-column:1;padding:10px 12px;gap:8px}.qwk-titel small{display:none}.qwk-zeit{grid-column:1}.qwk-side,.qwk-info{position:absolute;z-index:5;left:0;right:0;bottom:62px;max-height:52%;border:1px solid var(--k-l);border-radius:18px 18px 0 0;transform:translateY(calc(100% + 90px));transition:.3s;box-shadow:0 -10px 40px rgba(0,0,0,.5)}.qwk.qwk-ebenen-auf .qwk-side,.qwk.qwk-info-auf .qwk-info{transform:none}.qwk-mob{display:inline-flex}.qwk-such{margin-left:0;width:100%}.qwk-such input{width:100%}.qwk-leg{bottom:10px;left:10px;max-width:70%}.qwk-q{display:none}}
`;
function ui(root){
  const sw=(k,n,c,d)=>`<label class="qwk-sw"><input type="checkbox" data-ov="${k}" ${S.ov[k]?'checked':''}><span class="k"></span>${c?`<span class="dt ${d?'d':''}" style="color:${c};background:${c}"></span>`:''}${n}</label>`;
  const gb=k=>`<button data-grund="${k}" aria-pressed="${S.grund===k}"><span>${GRUND[k].e}</span><span>${GRUND[k].n}</span></button>`;
  const gruppe=g=>Object.keys(GRUND).filter(k=>GRUND[k].g===g).map(gb).join('');
  const pl=(window.QW_DATEN&&window.QW_DATEN.pflanzen||[]).map(p=>`<option value="${p.id}">${p.nr} ${p.name.replace(' & Kiefernknospen','')}</option>`).join('');
  root.innerHTML=`<style>${CSS}</style><div class="qwk" lang="de">
  <div class="qwk-top"><div class="qwk-titel"><span class="qwk-gl2"></span><div>Weltkarte<small>Natur · Menschen · Rohstoffe · Geschichte</small></div></div>
   <div class="qwk-seg"><button data-modus="globus" aria-pressed="true">◉ Globus</button><button data-modus="flach" aria-pressed="false">▭ Karte</button></div>
   <div class="qwk-seg qwk-mob"><button data-auf="ebenen">☰ Ebenen</button><button data-auf="info">ⓘ Info</button></div>
   <div class="qwk-such"><input list="qwk-dl" placeholder="Land, Stadt oder Pflanze …"><datalist id="qwk-dl">${DAT.laender.map(c=>`<option value="${c.n}">`).join('')}${DAT.staedte.slice(0,400).map(s=>`<option value="${s[0]}">`).join('')}${Object.keys(PFL).map(id=>`<option value="${pname(id)}">`).join('')}</datalist></div></div>
  <aside class="qwk-side">
   <h3>Grundkarte · Natur</h3><div class="qwk-grund">${gruppe('Natur')}</div>
   <h3>Grundkarte · Menschen</h3><div class="qwk-grund">${gruppe('Menschen')}</div>
   <h3>Grundkarte · Wirtschaft</h3><div class="qwk-grund">${gruppe('Wirtschaft')}</div>
   <h3>Deutschland · Bundesländer</h3><div class="qwk-grund">${gruppe('Deutschland')}</div>
   <label class="qwk-sw" style="margin-top:6px"><input type="checkbox" data-unterlage ${S.unterlage?'checked':''}><span class="k"></span>Relief unter Statistik legen</label>
   <h3>Beschriftung</h3>${sw('namen','Ländernamen')}${sw('grenzen','Grenzen')}${sw('staedte','Städte (mehr beim Zoomen)','#ffe9b8')}${sw('fluesse','Flüsse & Seen','#5aaaff')}${sw('landschaft','Gebirge & Landschaften','#f0d8b8')}${sw('gipfel','Gipfel','#ffffff')}${sw('tiefen','Meerestiefen & Tiefseegräben','#7fe0ff',1)}${sw('nacht','Tag & Nacht (jetzt)','#ffd860')}
   <h3>Geschichte</h3>${sw('kriege','⚔️ Kriege','#d8302a')}${sw('wander','🧭 Völkerwanderungen','#ffd28a')}${sw('erf','💡 Erfindungen','#ffe14a')}${sw('geld','🪙 Geldgeschichte','#e8b030')}${sw('goethe','✒️ Goethes Reisen','#ff8c6e')}<select class="qwk-sel" data-epoche><option value="">Alle Epochen</option>${Object.entries(EPOCHE).map(([k,v])=>`<option value="${k}">${v}</option>`).join('')}</select>
   <h3>Getreide · Teil G</h3>${Object.entries(GETREIDE).map(([k,G2])=>sw(k,G2.e+' '+G2.n,G2.c)).join('')}
   <h3>Rohstoffe & Energie</h3>${Object.entries(ROH).map(([k,G2])=>sw(k,G2.e+' '+G2.n,G2.c,1)).join('')}
   <h3>Kompendium</h3>${sw('pfl','🌿 Herkunft der Pflanzen','#ff6a8a')}<select class="qwk-sel" data-pflanze><option value="">Wildvorkommen einer Pflanze zeigen …</option>${pl}</select>${sw('rez','🍽️ Rezepte nach Herkunft','#c79aff')}${sw('aut','👤 Autoren','#6ac8ff')}
  </aside>
  <div class="qwk-map"><canvas></canvas><div class="qwk-zoom"><button data-z="1.5" aria-label="Hineinzoomen">＋</button><button data-z="0.67" aria-label="Herauszoomen">－</button><button data-z="0" aria-label="Zurücksetzen">⟲</button></div><div class="qwk-leg"></div></div>
  <aside class="qwk-info"></aside>
  <div class="qwk-zeit"><button class="qwk-play" aria-label="Abspielen">▶</button><span style="color:var(--k-m)">1960</span><input type="range" min="1960" max="2023" value="${S.jahr}"><span class="qwk-jahr">${S.jahr}</span><span class="qwk-q">Quellen: Grenzen, Städte, Flüsse – Natural Earth (gemeinfrei); Relief – three.js-Beispieltextur (MIT); Bevölkerung, Energie, Gesellschaft – Our World in Data (UN, Energy Institute, IHME, Gapminder, WHR, FAO); Getreide – FAOSTAT 2022; Rohstoffe – Energy Institute, USGS, IAEA; Klima/Böden – vereinfachtes Schema</span></div>
  </div>`;
  wrap=$('.qwk',root); cv=$('canvas',wrap); ctx=cv.getContext('2d');
}
function groesse(){ const m=$('.qwk-map',wrap), r=m.getBoundingClientRect(); DPR=Math.min(2,devicePixelRatio||1); W=r.width; H=r.height; cv.width=W*DPR; cv.height=H*DPR; RKEY=''; zeichne(); }
function neu(){ S.bewegt=true; zeichne(false); }
function ereignisse(){
  wrap.querySelectorAll('[data-ov]').forEach(i=>i.onchange=()=>{ S.ov[i.dataset.ov]=i.checked; legende(); zeichne(); });
  $('[data-unterlage]',wrap).onchange=e=>{ S.unterlage=e.target.checked; zeichne(); };
  wrap.querySelectorAll('[data-grund]').forEach(b=>b.onclick=()=>grundSetzen(b.dataset.grund));
  wrap.querySelectorAll('[data-modus]').forEach(b=>b.onclick=()=>{ S.modus=b.dataset.modus; S.zoom=1; S.px=S.py=0; wrap.querySelectorAll('[data-modus]').forEach(x=>x.setAttribute('aria-pressed',x===b)); zeichne(); });
  wrap.querySelectorAll('[data-auf]').forEach(b=>b.onclick=()=>{ wrap.classList.toggle('qwk-'+b.dataset.auf+'-auf'); });
  wrap.querySelectorAll('[data-z]').forEach(b=>b.onclick=()=>{ const z=+b.dataset.z; S.spin=false; if(!z){ S.zoom=1; S.px=S.py=0; } else S.zoom=Math.max(.6,Math.min(40,S.zoom*z)); zeichne(); });
  $('[data-pflanze]',wrap).onchange=e=>{ S.pflanze=e.target.value; if(S.pflanze){ const P=PFL[S.pflanze]; flieg(P[0][0],P[0][1]); } zeichne(); };
  $('[data-epoche]',wrap).onchange=e=>{ S.epoche=e.target.value; zeichne(); };
  const rg=$('.qwk-zeit input',wrap), jl=$('.qwk-jahr',wrap); rg.oninput=()=>{ S.jahr=+rg.value; jl.textContent=S.jahr; zeichne(); info(); };
  let spiel=null; $('.qwk-play',wrap).onclick=e=>{ const b=e.currentTarget; if(spiel){ clearInterval(spiel); spiel=null; b.textContent='▶'; return; } b.textContent='❚❚'; if(S.jahr>=2023) S.jahr=1960; spiel=setInterval(()=>{ S.jahr++; rg.value=S.jahr; jl.textContent=S.jahr; zeichne(); info(); if(S.jahr>=2023){ clearInterval(spiel); spiel=null; b.textContent='▶'; } },160); };
  $('.qwk-such input',wrap).onchange=e=>{ const v=e.target.value.trim().toLowerCase(); const c=DAT.laender.find(c=>c.n.toLowerCase()===v); if(c){ waehle(c,c.lp); flieg(c.lp[0],c.lp[1]); return; }
    const st=DAT.staedte.find(s=>s[0].toLowerCase()===v); if(st){ S.ov.staedte=true; const cc=landAn(st[1],st[2]); if(cc) waehle(cc,[st[1],st[2]]); flieg(st[1],st[2],Math.max(S.zoom,4)); return; }
    const id=Object.keys(PFL).find(id=>pname(id).toLowerCase()===v); if(id){ S.pflanze=id; $('[data-pflanze]',wrap).value=id; S.ov.pfl=true; flieg(PFL[id][0][0],PFL[id][0][1]); zeichne(); } };
  const m=$('.qwk-map',wrap), P=new Map(); let start=null, d0=0, z0=1, bewegt=false;
  m.addEventListener('pointerdown',e=>{ m.setPointerCapture(e.pointerId); P.set(e.pointerId,[e.clientX,e.clientY]); S.spin=false; bewegt=false; start={x:e.clientX,y:e.clientY,lam:S.lam,phi:S.phi,px:S.px,py:S.py}; if(P.size===2){ const [a,b]=[...P.values()]; d0=Math.hypot(a[0]-b[0],a[1]-b[1]); z0=S.zoom; } });
  m.addEventListener('pointermove',e=>{ if(!P.has(e.pointerId)) return; P.set(e.pointerId,[e.clientX,e.clientY]);
    if(P.size===2){ const [a,b]=[...P.values()]; S.zoom=Math.max(.6,Math.min(40,z0*Math.hypot(a[0]-b[0],a[1]-b[1])/d0)); bewegt=true; neu(); return; }
    const dx=e.clientX-start.x, dy=e.clientY-start.y; if(Math.hypot(dx,dy)>4) bewegt=true; if(!bewegt) return;
    if(S.modus==='globus'){ const f=57/radius(); S.lam=start.lam-dx*f; S.phi=Math.max(-85,Math.min(85,start.phi+dy*f)); } else { S.px=start.px+dx; S.py=start.py+dy; }
    neu(); });
  const ende=e=>{ if(!P.has(e.pointerId)) return; P.delete(e.pointerId); if(!bewegt&&P.size===0){ const r=m.getBoundingClientRect(), x=e.clientX-r.left, y=e.clientY-r.top; const h=histAn(x,y); if(h){ S.hist=h; S.sel=null; info(); zeichne(); wrap.classList.add('qwk-info-auf'); return; } const ll=inv(x,y); if(ll&&GRUND[S.grund].de){ const b=blAn(ll[0],ll[1]); if(b){ S.bl=b.i; S.sel=null; S.hist=null; info(); zeichne(); wrap.classList.add('qwk-info-auf'); return; } } if(ll){ const c=landAn(ll[0],ll[1]); S.hist=null; S.bl=null; if(c) waehle(c,ll); else { S.sel=null; S.klick=null; info(); zeichne(); } } } };
  m.addEventListener('pointerup',ende); m.addEventListener('pointercancel',ende);
  m.addEventListener('wheel',e=>{ e.preventDefault(); S.spin=false; S.zoom=Math.max(.6,Math.min(40,S.zoom*(e.deltaY<0?1.15:1/1.15))); neu(); },{passive:false});
  addEventListener('resize',()=>{ if(document.body.contains(wrap)) groesse(); });
}
function grundSetzen(k){ S.grund=k; wrap.querySelectorAll('[data-grund]').forEach(x=>x.setAttribute('aria-pressed',x.dataset.grund===k)); if(GRUND[k].de){ S.sel=null; S.hist=null; if(S.zoom<5) flieg(10.4,51.2,W<700?6.5:7.5); } else S.bl=null; legende(); zeichne(); info(); }
function waehle(c,ll){ S.sel=c.i; S.klick=ll; S.hist=null; info(); zeichne(); wrap.classList.add('qwk-info-auf'); wrap.classList.remove('qwk-ebenen-auf'); }
function flieg(lon,lat,zz){ S.spin=false; if(S.modus!=='globus'){ S.lam=lon; S.px=0; S.py=lat*kf(); zeichne(); return; } const a={l:S.lam,p:S.phi,z:S.zoom}, b={l:lon,p:Math.max(-60,Math.min(60,lat)),z:zz||Math.max(S.zoom,1.5)}; let dl=((b.l-a.l+540)%360)-180; const t0=performance.now();
  (function st(t){ const k=Math.min(1,(t-t0)/900), e=k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2; S.lam=a.l+dl*e; S.phi=a.p+(b.p-a.p)*e; S.zoom=a.z+(b.z-a.z)*e; S.bewegt=k<1; zeichne(k>=1); if(k<1&&document.body.contains(wrap)) requestAnimationFrame(st); })(t0); }
let letzt=0; function dreh(t){ if(!wrap||!document.body.contains(wrap)) return; if(S.spin&&S.modus==='globus'){ S.lam+=0.08; S.bewegt=true; zeichne(false); } else if(S.ov.wander&&t-letzt>80){ letzt=t; zeichne(); } requestAnimationFrame(dreh); }

window.QWWELT={ oeffne(root,ebene){ daten(); if(ebene){ if(GRUND[ebene]){ S.grund=ebene; if(GRUND[ebene].de){ S.lam=10.4; S.phi=51.2; S.zoom=7; S.spin=false; } } else if(ebene in S.ov) S.ov[ebene]=true; } ui(root); ereignisse(); requestAnimationFrame(()=>{ groesse(); legende(); info(); }); S.spin=!window.QW_STANDBILD&&!(GRUND[S.grund].de); requestAnimationFrame(dreh); },
  zustand:S, zeichne:()=>zeichne(), legende:()=>legende(), waehle:(i)=>{ const c=DAT.idx[i]; if(c){ waehle(c,c.lp); flieg(c.lp[0],c.lp[1]); } }, flieg:(a,b,z)=>flieg(a,b,z), hist:(a,i)=>{ S.hist=[a,i]; info(); zeichne(); }, grund:k=>grundSetzen(k), bl:c=>{ S.bl=c; info(); zeichne(); } };
})();
