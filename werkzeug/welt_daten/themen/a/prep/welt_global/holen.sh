#!/bin/sh
# Rohdaten holen (nach Gebrauch wieder gelöscht). Danach: gold_json.py, boeden.py, sonne.py (sonne.py lädt selbst per Zarr/S3)
R=/home/claude/scratch/welt_global/roh; mkdir -p $R/wrb $R/power
curl -s -o $R/il_dsd.xml "https://api.imf.org/external/sdmx/2.1/dataflow/IMF.STA/IL/latest?references=all"
for f in M Q A; do curl -s -o $R/rgv_$f.xml "https://api.imf.org/external/sdmx/2.1/data/IMF.STA,IL/.RGV_REVS.FTO.$f?startPeriod=2020"; done
curl -s -o $R/rgv_A_alt.xml "https://api.imf.org/external/sdmx/2.1/data/IMF.STA,IL/.RGV_REVS.FTO.A?startPeriod=1990"
curl -s -o $R/rgv_M_alt.xml "https://api.imf.org/external/sdmx/2.1/data/IMF.STA,IL/.RGV_REVS.FTO.M?startPeriod=2005&endPeriod=2019"
for f in MostProbable.vrt MostProbable.vrt.ovr MostProbable.rat.json; do curl -s -o $R/wrb/$f https://files.isric.org/soilgrids/latest/data/wrb/$f; done
