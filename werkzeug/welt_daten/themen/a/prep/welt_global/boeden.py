# Vorherrschende WRB-Referenzbodengruppe je 2°-Zelle aus SoilGrids 2.0 (ISRIC), Overview 1/30°
import rasterio, numpy as np, json, base64, sys
W='/home/claude/scratch/welt_global/roh/wrb/'
with rasterio.open(W+'MostProbable.vrt.ovr', overview_level=0) as d:
    a=d.read(1)
H,Wd=a.shape; px=360/Wd                       # 1/30 Grad
top=83.999167206                               # aus MostProbable.vrt (GeoTransform)
print(a.shape,px,file=sys.stderr)
# auf volles Gitter 90..-90 bringen (Zeilen 1/30 Grad)
full=np.full((int(180/px),Wd),255,np.uint8)
r0=int(round((90-top)/px)); full[r0:r0+H]=a
n=int(2/px)  # 60 Pixel je 2°-Zelle
blk=full.reshape(90,n,180,n).transpose(0,2,1,3).reshape(90,180,n*n)
out=np.full((90,180),255,np.uint8); anteil=np.zeros((90,180))
for i in range(90):
    for j in range(180):
        v=blk[i,j]; v=v[v<30]
        if v.size>=0.25*n*n:
            c=np.bincount(v,minlength=30); k=int(c.argmax()); out[i,j]=k+1; anteil[i,j]=c[k]/v.size
np.save('/home/claude/scratch/welt_global/roh/boeden_out.npy',out)
print('Zellen mit Wert',(out<255).sum(),'mittl. Anteil der Hauptgruppe',round(anteil[out<255].mean(),2),file=sys.stderr)
print(np.bincount(out[out<255],minlength=31),file=sys.stderr)

# --- JSON schreiben ---
K=[("Acrisols","Acrisole","#d8a06a","Saure, stark verwitterte Tonanreicherungsböden der feuchten Tropen und Subtropen; wenig Nährstoffe."),
("Albeluvisols","Albeluvisole (heute Retisole)","#c8c0a8","Böden mit gebleichten, zungenförmig in den tonreichen Unterboden greifenden Streifen; kühl-gemäßigte und boreale Zone."),
("Alisols","Alisole","#e0b878","Saure, tonreiche Böden mit viel austauschbarem Aluminium; feuchte Subtropen."),
("Andosols","Andosole","#5a4a6a","Junge Böden aus Vulkanasche: locker, dunkel, speichern viel Wasser, meist fruchtbar."),
("Arenosols","Arenosole (Sandböden)","#f2e2a8","Kaum entwickelte Sandböden; trocken und nährstoffarm (Dünen, Sandflächen)."),
("Calcisols","Calcisole","#f0d8b8","Böden trockener Gebiete mit angereichertem Kalk im Unterboden."),
("Cambisols","Cambisole (Braunerden)","#c8a060","Mäßig entwickelte Verwitterungsböden mit braunem Unterboden; in Mitteleuropa am häufigsten."),
("Chernozems","Schwarzerden (Chernozeme)","#2a2420","Tiefgründig schwarzer, humusreicher Oberboden auf Löss der Steppen; zählen zu den fruchtbarsten Ackerböden."),
("Cryosols","Cryosole (Permafrostböden)","#a8c8d8","Böden über dauerhaft gefrorenem Untergrund; Tundra und nördliche Taiga."),
("Durisols","Durisole","#d8c8a0","Trockengebietsböden mit einer durch Kieselsäure verhärteten Schicht."),
("Ferralsols","Ferralsole","#c84a2a","Uralte, tief verwitterte rote bis gelbe Tropenböden aus Eisen- und Aluminiumoxiden; arm an Nährstoffen."),
("Fluvisols","Fluvisole (Auenböden)","#6ab0d0","Junge, geschichtete Böden aus Fluss-, See- oder Meeresablagerungen; Flussauen und Deltas."),
("Gleysols","Gleye","#6a8aa0","Vom Grundwasser geprägte, zeitweise nasse Böden mit grau-blauen und rostfleckigen Horizonten."),
("Gypsisols","Gypsisole","#f8f0d8","Wüstenböden mit angereichertem Gips."),
("Histosols","Histosole (Moorböden)","#4a3a28","Böden aus Torf, also überwiegend aus abgestorbenen Pflanzenresten; Moore."),
("Kastanozems","Kastanozeme","#8a6a40","Kastanienbraune Steppenböden: weniger Humus als Schwarzerden, Kalk im Unterboden; trockenere Steppen."),
("Leptosols","Leptosole (Felsböden)","#a0a0a0","Sehr flachgründige oder steinreiche Böden über Fels; Gebirge und Wüsten."),
("Lixisols","Lixisole","#e8a888","Tonanreicherungsböden wechselfeuchter Tropen mit wenig Speicherkraft für Nährstoffe; erosionsanfällig."),
("Luvisols","Luvisole (Parabraunerden)","#d0b048","Böden mit in den Unterboden verlagertem Ton, basenreich und fruchtbar; oft auf Löss."),
("Nitisols","Nitisole","#a83a3a","Tiefgründige, gut gekrümelte rote Tonböden der Tropen, oft aus Basalt; fruchtbar."),
("Phaeozems","Phaeozeme","#5a4a30","Dunkle, humusreiche Böden wie Schwarzerden, aber kalkfrei; feuchtere Steppen und Prärien."),
("Planosols","Planosole","#b0a0b8","Böden mit scharfem Übergang zu dichtem, wasserstauendem Unterboden."),
("Plinthosols","Plinthosole","#b85a3a","Tropenböden mit eisenreichem Plinthit, der an der Luft zu Laterit verhärtet."),
("Podzols","Podsole","#d8d0c8","Saure, ausgewaschene Böden unter Nadelwald und Heide mit gebleichtem Ober- und rostbraunem Anreicherungshorizont."),
("Regosols","Regosole","#e8d8b8","Schwach entwickelte Böden aus Lockergestein, ohne deutliche Horizonte."),
("Solonchaks","Solontschake (Salzböden)","#f0f0f0","Böden mit viel löslichem Salz an oder nahe der Oberfläche; Senken in Trockengebieten."),
("Solonetz","Solonetze","#c8c0d8","Natriumreiche Böden mit dichtem, säuligem Unterboden."),
("Stagnosols","Stagnosole (Pseudogleye)","#8aa0b0","Böden mit Staunässe über dichtem Unterboden, abwechselnd nass und trocken."),
("Umbrisols","Umbrisole","#6a5a48","Saure Böden mit dunklem, humusreichem Oberboden; kühl-feuchte Gebirge und Küsten."),
("Vertisols","Vertisole","#5a5a58","Schwere, quellfähige Tonböden, die in Trockenzeiten tiefe Risse bilden.")]
kl={str(i+1):[d,f,e,en] for i,(en,d,f,e) in enumerate(K)}
vork=[int(x) for x in sorted(set(out[out<255].tolist()))]
kopf={"id":"boeden","name":"Böden (vorherrschende Bodengruppe)","gruppe":"Natur","typ":"raster","einheit":"",
 "raster":{"zellen":"2°","zeilen":90,"spalten":180,"start_lat":89,"start_lon":-179,"schritt":2,
   "reihenfolge":"wie klima_raster: Index = ((89-lat)/2)*180 + (lon+179)/2",
   "kodierung":"Base64, 1 Byte = Klassen-Nummer 1–30 (siehe „klassen“); 255 = keine Angabe (Meer, Eis, Fels ohne Boden, Antarktis, nördlich 84° N)"},
 "klassen_felder":["name","farbe","erklaerung","wrb"],
 "klassen":kl,
 "legende":[[kl[str(k)][0],kl[str(k)][1]] for k in vork],
 "quellen":[{"t":"ISRIC – World Soil Information, SoilGrids: WRB-Referenzbodengruppen, wahrscheinlichste Klasse (MostProbable, 250 m; Übersichtsstufe 1/30°). Hengl, T. et al. (2017): SoilGrids250m: Global gridded soil information based on machine learning. PLoS ONE 12(2): e0169748",
   "u":"https://files.isric.org/soilgrids/latest/data/wrb/","stand":"Modell 2017, Neuberechnung 2023 (Dateien 01.02.2023)",
   "lizenz":"CC BY 4.0 – Nennung: „SoilGrids, ISRIC – World Soil Information (CC BY 4.0)“; Änderung: auf 2°-Zellen vereinfacht (häufigste Klasse)"}],
 "hinweis":"Je 2°-Zelle die häufigste WRB-Referenzbodengruppe aus ca. 3.600 Bildpunkten (1/30°) der ISRIC-Übersichtsstufe; Zelle nur gefüllt, wenn mind. 25 % Boden-Bildpunkte. Stark vereinfacht: Innerhalb einer Zelle wechseln Böden auf kleinem Raum (z. B. Saarland = Braunerden, daneben Parabraunerden, Pseudogleye, Auenböden). Gruppen nach WRB 2006 (SoilGrids-Stand; Albeluvisole heißen seit WRB 2014 Retisole). Deutsche Namen und Erklärungen eigene Fassung. Ersetzt das bisherige Schema BODEN.",
 "daten":base64.b64encode(out.tobytes()).decode()}
json.dump(kopf,open('/home/claude/scratch/welt_global/boeden.json','w'),ensure_ascii=False,separators=(',',':'))
