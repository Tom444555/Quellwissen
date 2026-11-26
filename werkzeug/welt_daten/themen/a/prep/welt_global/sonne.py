# Mittlere Globalstrahlung (ALLSKY_SFC_SW_DWN) aus NASA POWER Klimatologie (Zarr, S3), 1° -> 2°-Zellen
import zarr, fsspec, numpy as np, json, base64, sys
U='https://nasa-power.s3.amazonaws.com/syn1deg/temporal/power_syn1deg_climatology_temporal_lst.zarr'
g=zarr.open_consolidated(fsspec.get_mapper(U),mode='r')
lat=g['lat'][:]; lon=g['lon'][:]; t=g['time'][:]
a=g['ALLSKY_SFC_SW_DWN'][:]          # (13,180,360) W/m2, Index 12 = Jahr?
print('lat',lat[:3],lat[-1],'lon',lon[:3],'time',t,file=sys.stderr)
np.save('/home/claude/scratch/welt_global/roh/power/ghi.npy',a); np.save('/home/claude/scratch/welt_global/roh/power/lat.npy',lat); np.save('/home/claude/scratch/welt_global/roh/power/lon.npy',lon)
print(dict(g.attrs).get('time_coverage_start'),dict(g.attrs).get('time_coverage_end'),file=sys.stderr)

# --- 2°-Raster ---
def zu2(m):  # m: (180,360), lat -89.5..89.5, lon -179.5..179.5
    b=m.reshape(90,2,180,2).mean(axis=(1,3))   # Zeile 0 = lat -89 (Süd)
    return b[::-1]                              # Zeile 0 = lat 89 (Nord)
kwh=a*24/1000
eb={'jahr':zu2(kwh[12]),'jun':zu2(kwh[5]),'dez':zu2(kwh[11])}
def enc(x):
    v=np.where(np.isnan(x),255,np.clip(np.round(x*20),0,254)).astype(np.uint8)
    return base64.b64encode(v.tobytes()).decode()
def zelle(e,la,lo):
    i=int((89-(2*np.floor(la/2)+1))/2); j=int(((2*np.floor(lo/2)+1)+179)/2); return round(float(eb[e][i,j]),2)
for n,la,lo in [('Saarbrücken',49.23,7.0),('Madrid',40.42,-3.7),('Kairo',30.04,31.24),('Oslo',59.91,10.75)]:
    print(n,'2°-Zelle Jahr',zelle('jahr',la,lo),'kWh/m²/Tag =',round(zelle('jahr',la,lo)*365),'kWh/m²/Jahr',file=sys.stderr)
kopf={"id":"sonneneinstrahlung","name":"Sonneneinstrahlung (Globalstrahlung)","gruppe":"Natur","typ":"raster","einheit":"kWh/m² pro Tag",
 "raster":{"zellen":"2°","zeilen":90,"spalten":180,"start_lat":89,"start_lon":-179,"schritt":2,
   "reihenfolge":"wie klima_raster: Index = ((89-lat)/2)*180 + (lon+179)/2",
   "kodierung":"Base64, 1 Byte je Zelle; Byte ÷ 20 = kWh/m² pro Tag (Schritt 0,05); 255 = keine Angabe. Jahressumme ≈ Tageswert × 365 kWh/m²."},
 "ebenen":{"jahr":"Mittlere Globalstrahlung im Jahresdurchschnitt","jun":"Mittel im Juni","dez":"Mittel im Dezember"},
 "legende":{"jahr":[[0.5,"#2a2a5a"],[2,"#4a5aa0"],[3,"#7ab0a0"],[4,"#f0d060"],[5,"#f5a040"],[6,"#e05020"],[7,"#a01818"]],
   "stufen":["2 kWh/m²·Tag ≈ 730 kWh/m²·Jahr","4 ≈ 1.460","6 ≈ 2.190"]},
 "quellen":[{"t":"NASA Langley Research Center, POWER Project (Prediction Of Worldwide Energy Resources), Klimatologie ALLSKY_SFC_SW_DWN („All Sky Surface Shortwave Downward Irradiance“, Quelle CERES SYN1deg, 1°), Version 10; Datei power_syn1deg_climatology_temporal_lst.zarr",
   "u":"https://power.larc.nasa.gov/","stand":"Klimatologie 2001–2025 laut POWER-API (Zarr-Metadaten nennen noch 2001–2020; Werte identisch mit der API)",
   "lizenz":"CC BY 4.0 (LICENSE.txt im offiziellen Daten-Bucket s3://nasa-power); NASA-Daten, Nennung: „These data were obtained from the NASA Langley Research Center (LaRC) POWER Project funded through the NASA Earth Science/Applied Science Program.“"}],
 "hinweis":"Mittlere tägliche Sonnenenergie auf eine waagrechte Fläche (direkt + diffus, alle Wetterlagen) aus Satellitendaten; je 2°-Zelle Mittel aus vier 1°-Feldern. Keine Sonnenstunden (Sonnenscheindauer): dafür gibt es keine frei lizenzierte Weltkarte (CRU CL 2.0 steht unter ODbL mit Weitergabe unter gleichen Bedingungen). Für Orte grob: Die 2°-Zellen weichen in Stichproben bis ca. 7 % von PVGIS (EU-JRC, SARAH-3, Ortswert) ab (Saarbrücken 3,22 zu 3,22; Madrid 4,56 zu 4,87; Kairo 5,58 zu 5,97; Oslo 2,75 zu 2,60 kWh/m²·Tag). Auch über Meer und Eis gefüllt.",
 "daten":{k:enc(v) for k,v in eb.items()}}
json.dump(kopf,open('/home/claude/scratch/welt_global/sonneneinstrahlung.json','w'),ensure_ascii=False,separators=(',',':'))
