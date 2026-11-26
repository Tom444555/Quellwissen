#!/bin/sh
# Schritt 0: DWD-Rohdaten in ein leeres Verzeichnis laden (Aufruf: sh 0_laden.sh <roh>)
set -e; R="$1"; mkdir -p "$R/jahr"; cd "$R"
B=https://opendata.dwd.de/climate_environment/CDC
for i in 01 02 03 04 05 06 07 08 09 10 11 12 17; do curl -sfO $B/grids_germany/multi_annual/sunshine_duration/grids_germany_multi_annual_sunshine_duration_1991-2020_$i.asc.gz; done
curl -sfO $B/grids_germany/multi_annual/frost_days/grids_germany_multi_annual_frost_days_1991-2020_17.asc.gz
curl -sfO $B/grids_germany/multi_annual/air_temperature_min/grids_germany_multi_annual_air_temp_min_1991-2020_01.asc.gz
U=$B/observations_germany/climate/annual/kl/historical/
curl -sf $U | grep -o 'jahreswerte_KL_[0-9]*_[0-9]*_[0-9]*_hist.zip' | sort -u | awk -F_ '{s=substr($4,1,4);e=substr($5,1,4); if(s<=2001 && e>=2010) print}' > liste.txt
curl -sf ${U}KL_Jahreswerte_Beschreibung_Stationen.txt | iconv -f latin1 -t utf8 > stationen.txt
cd jahr; xargs -P 12 -I{} curl -sfO $U{} < ../liste.txt; cd ..
M=$B/observations_germany/climate/multi_annual/mean_91-20
for f in Sonnenscheindauer_1991-2020.txt Frosttage_1991-2020.txt; do curl -sf $M/$f | iconv -f latin1 -t utf8 > n_$f; done
# Globalstrahlung (Schritt 5) – eigenes Unterverzeichnis
mkdir -p strahl; cd strahl
G=$B/grids_germany/multi_annual/radiation_global
curl -sfO $G/grids_germany_multi_annual_radiation_global_1991_2020.zip
for i in 01 02 03 04 05 06 07 08 09 10 11 12; do curl -sfO $G/grids_germany_multi_monthly_radiation_global_1991_2020_$i.zip; done
for s in 01443 01975 04336; do curl -sfO $B/observations_germany/climate/daily/solar/tageswerte_ST_${s}_row.zip; done
