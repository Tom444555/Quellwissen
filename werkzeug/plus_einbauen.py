"""Bettet werkzeug/qw3d-plus.js (realistische 3D-Optik, three r170+ als ES-Modul) in quelle/gruenwissen.html ein.
Die Importmap zeigt im Artefakt auf jsDelivr; build.sh schreibt sie für GitHub auf lib/three/ um."""
import os,re
B=os.path.dirname(__file__); Q=os.path.join(B,'..','quelle','gruenwissen.html')
h=open(Q).read(); code=open(os.path.join(B,'qw3d-plus.js')).read()
IM='<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/"}}</script>\n'
if '<script type="importmap">' not in h: h=IM+h
blk='<script type="text/plain" id="qw3d-plus">'+code.replace('</script','<\\/script')+'</script>'
if 'id="qw3d-plus"' in h: h=re.sub(r'<script type="text/plain" id="qw3d-plus">.*?</script>',lambda m:blk,h,flags=re.S)
else: h=h.replace('<script type="application/json" id="daten">',blk+'\n<script type="application/json" id="daten">',1)
open(Q,'w').write(h); print('ok')
