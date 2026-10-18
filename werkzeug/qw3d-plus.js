/* Quellwissen 3D „realistisch“: HDR-Himmel, prozedurale Erd-Texturen, Graswiese, Blatt-Material, Umgebungsverdeckung (GTAO). */
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { GTAOPass } from 'three/addons/postprocessing/GTAOPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { ShaderPass } from 'three/addons/postprocessing/ShaderPass.js';
import { Sky } from 'three/addons/objects/Sky.js';
window.THREE = Object.assign({}, THREE, { OrbitControls });


/* ---- kachelbares Rauschen ---- */
function hash(i, j, s) { let h = (i * 374761393 + j * 668265263 + s * 982451653) | 0; h = (h ^ (h >>> 13)) * 1274126177; return ((h ^ (h >>> 16)) >>> 0) / 4294967295; }
function vnoise(x, y, p, s) { const xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi; const u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf);
  const g = (a, b) => hash(((a % p) + p) % p, ((b % p) + p) % p, s);
  return (g(xi, yi) * (1 - u) + g(xi + 1, yi) * u) * (1 - v) + (g(xi, yi + 1) * (1 - u) + g(xi + 1, yi + 1) * u) * v; }
function fbm(x, y, p, s, okt) { let a = 0, amp = 0.5, f = 1, n = 0; for (let o = 0; o < okt; o++) { a += amp * vnoise(x * f, y * f, p * f, s + o); n += amp; amp *= 0.5; f *= 2; } return a / n; }
function erdTexturen(N, art) {
  const H = new Float32Array(N * N), A = new Float32Array(N * N * 3);
  let sd = art === 'mulch' ? 7 : 3; const r = () => (sd = sd * 16807 % 2147483647) / 2147483647;
  for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) { const u = x / N * 8, v = y / N * 8; const n = fbm(u, v, 8, 1, 5), k = fbm(u * 4, v * 4, 32, 9, 3);
    const i = y * N + x; H[i] = n * 0.6 + k * 0.4; const t = 0.62 + (n - 0.5) * 0.5 + (k - 0.5) * 0.35; A[i * 3] = t * 1.02; A[i * 3 + 1] = t * 0.98; A[i * 3 + 2] = t * 0.93; }
  // Kruemel, Steinchen, organische Reste
  const n = art === 'mulch' ? 260 : 900;
  for (let q = 0; q < n; q++) { const cx = r() * N, cy = r() * N, rad = (art === 'mulch' ? 3 + r() * 10 : 1 + r() * 4) * N / 512, typ = r(); const hell = typ < 0.15 ? 1.5 : typ < 0.5 ? 0.6 : 0.85; const lang = art === 'mulch' ? 3 + r() * 6 : 1, rot = r() * Math.PI;
    for (let dy = -rad * lang; dy <= rad * lang; dy++) for (let dx = -rad * lang; dx <= rad * lang; dx++) { const rx = dx * Math.cos(rot) + dy * Math.sin(rot), ry = -dx * Math.sin(rot) + dy * Math.cos(rot); const d = (rx / lang) ** 2 + ry ** 2; if (d > rad * rad) continue;
      const X = ((Math.round(cx + dx) % N) + N) % N, Y = ((Math.round(cy + dy) % N) + N) % N, i = Y * N + X, w = 1 - d / (rad * rad);
      H[i] += w * 0.35; const f = art === 'mulch' ? [1.5, 1.3, 0.85] : typ < 0.15 ? [1.4, 1.35, 1.25] : [hell, hell * 0.97, hell * 0.92];
      A[i * 3] = A[i * 3] * (1 - w) + f[0] * 0.62 * w; A[i * 3 + 1] = A[i * 3 + 1] * (1 - w) + f[1] * 0.62 * w; A[i * 3 + 2] = A[i * 3 + 2] * (1 - w) + f[2] * 0.62 * w; } }
  const ca = document.createElement('canvas'), cn = document.createElement('canvas'); ca.width = ca.height = cn.width = cn.height = N;
  const ia = ca.getContext('2d').createImageData(N, N), inn = cn.getContext('2d').createImageData(N, N);
  for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) { const i = y * N + x, hx = H[y * N + (x + 1) % N] - H[y * N + (x - 1 + N) % N], hy = H[((y + 1) % N) * N + x] - H[((y - 1 + N) % N) * N + x];
    const s = 6, nx = -hx * s, ny = -hy * s, nz = 1, l = Math.hypot(nx, ny, nz);
    inn.data[i * 4] = (nx / l * 0.5 + 0.5) * 255; inn.data[i * 4 + 1] = (ny / l * 0.5 + 0.5) * 255; inn.data[i * 4 + 2] = (nz / l * 0.5 + 0.5) * 255; inn.data[i * 4 + 3] = 255;
    for (let c = 0; c < 3; c++) ia.data[i * 4 + c] = Math.min(255, A[i * 3 + c] * 255); ia.data[i * 4 + 3] = 255; }
  ca.getContext('2d').putImageData(ia, 0, 0); cn.getContext('2d').putImageData(inn, 0, 0);
  const map = new THREE.CanvasTexture(ca), nor = new THREE.CanvasTexture(cn);
  for (const t of [map, nor]) { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.anisotropy = 4; } map.colorSpace = THREE.SRGBColorSpace; return { map, nor }; }

function uvsPlanar(g, s) { const p = g.attributes.position; g.computeVertexNormals(); const n = g.attributes.normal, uv = new Float32Array(p.count * 2);
  for (let i = 0; i < p.count; i++) { const ax = Math.abs(n.getX(i)), ay = Math.abs(n.getY(i)), az = Math.abs(n.getZ(i)); let u, v;
    if (ay >= ax && ay >= az) { u = p.getX(i); v = p.getZ(i); } else if (az >= ax) { u = p.getX(i); v = p.getY(i); } else { u = p.getZ(i); v = p.getY(i); }
    uv[i * 2] = u * s; uv[i * 2 + 1] = v * s; } g.setAttribute('uv', new THREE.BufferAttribute(uv, 2)); }

function halmGeo() {
  const g = new THREE.BufferGeometry(); const pos = [], col = [], idx = []; const S = 5;
  for (let i = 0; i <= S; i++) { const t = i / S, w = 0.006 * (1 - t * 0.9); pos.push(-w, t, 0, w, t, 0); const c = new THREE.Color(0x142408).lerp(new THREE.Color(0x5f8a30), Math.pow(t, 0.9)); col.push(c.r, c.g, c.b, c.r, c.g, c.b); if (i < S) { const a = i * 2; idx.push(a, a + 1, a + 2, a + 1, a + 3, a + 2); } }
  g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute('color', new THREE.Float32BufferAttribute(col, 3)); g.setIndex(idx);
  const p = g.attributes.position; for (let i = 0; i < p.count; i++) { const t = p.getY(i); p.setZ(i, 0.25 * t * t); } g.computeVertexNormals();
  return g; }
let HALM = null, HALM_M = null;
function grasWiese(scene, frei, anzahl, rmax) { const g = HALM || (HALM = halmGeo());
  const m = HALM_M || (HALM_M = durchlicht(new THREE.MeshStandardMaterial({ vertexColors: true, side: THREE.DoubleSide, roughness: 0.75 }), 0.8));
  const im = new THREE.InstancedMesh(g, m, anzahl), o = new THREE.Object3D(), c = new THREE.Color(); let sd = 5; const r = () => (sd = sd * 16807 % 2147483647) / 2147483647; let k = 0;
  while (k < anzahl) { const a = r() * Math.PI * 2, d = Math.pow(r(), 0.75) * rmax, x = Math.cos(a) * d, z = Math.sin(a) * d - 0.7; if (frei(x, z)) continue;
    o.position.set(x, -0.03, z); o.rotation.set(0, r() * Math.PI * 2, (r() - 0.5) * 0.3); const h = 0.025 + r() * 0.06 * (0.6 + 0.9 * fbm(x * 0.7 + 3, z * 0.7 + 3, 64, 4, 2)); o.scale.set(1 + r(), h, h); o.updateMatrix(); im.setMatrixAt(k, o.matrix);
    c.setHSL(0.18 + r() * 0.1, 0.35 + r() * 0.25, 0.45 + r() * 0.35); im.setColorAt(k, c); k++; }
  im.receiveShadow = true; scene.add(im); }


/* ---- Texturen fuer Pflanzen ---- */
function canvasTex(N, M, mal) { const c = document.createElement('canvas'); c.width = N; c.height = M; mal(c.getContext('2d'), N, M); const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.anisotropy = 8; return t; }
function hoeheZuNormal(N, M, H, s) { return canvasTex(N, M, (x) => { const im = x.createImageData(N, M);
  for (let j = 0; j < M; j++) for (let i = 0; i < N; i++) { const k = j * N + i, hx = H[j * N + (i + 1) % N] - H[j * N + (i - 1 + N) % N], hy = H[((j + 1) % M) * N + i] - H[((j - 1 + M) % M) * N + i];
    const nx = -hx * s, ny = -hy * s, l = Math.hypot(nx, ny, 1); im.data[k * 4] = (nx / l * .5 + .5) * 255; im.data[k * 4 + 1] = (ny / l * .5 + .5) * 255; im.data[k * 4 + 2] = (1 / l * .5 + .5) * 255; im.data[k * 4 + 3] = 255; } x.putImageData(im, 0, 0); }); }
// Blattadern: u entlang der Mittelrippe (0..1), v quer (0.5 = Mitte)
function blattTexturen() { const N = 512, M = 256, H = new Float32Array(N * M), A = new Float32Array(N * M);
  for (let j = 0; j < M; j++) for (let i = 0; i < N; i++) { const u = i / N, v = j / M, d = Math.abs(v - 0.5); let h = 0, a = 0;
    const mr = Math.exp(-Math.pow(d / 0.012, 2)) * (1 - u * 0.6); h += mr * 1.0; a += mr * 0.55;
    // Seitenadern: schraeg nach vorn, 11 Paare
    const w = (u * 11 - d * 9.5); const f = w - Math.floor(w); const sa = Math.exp(-Math.pow((f - 0.5) / 0.045, 2)) * Math.min(1, d * 14) * (1 - d * 1.4); h += sa * 0.45; a += sa * 0.35;
    // feine Netzadern
    const n = fbm(u * 40, v * 20, 1e9, 3, 2); const net = Math.pow(Math.abs(Math.sin(u * 230 + n * 6) * Math.sin(v * 140 + n * 5)), 8); h += net * 0.12;
    H[j * N + i] = h; A[j * N + i] = Math.min(1, a); }
  const nor = hoeheZuNormal(N, M, H, 9);
  const map = canvasTex(N, M, (x) => { const im = x.createImageData(N, M); for (let k = 0; k < N * M; k++) { const n = 0.9 + 0.1 * fbm((k % N) / 30, Math.floor(k / N) / 30, 1e9, 7, 3); const l = n + A[k] * 0.55; im.data[k * 4] = Math.min(255, l * 225); im.data[k * 4 + 1] = Math.min(255, l * 240); im.data[k * 4 + 2] = Math.min(255, l * 200); im.data[k * 4 + 3] = 255; } x.putImageData(im, 0, 0); });
  map.colorSpace = THREE.SRGBColorSpace; return { map, nor }; }
// Stengel: Laengsriefen (v entlang, u rundum)
function stengelTexturen() { const N = 256, M = 512, H = new Float32Array(N * M), A = new Float32Array(N * M);
  for (let j = 0; j < M; j++) for (let i = 0; i < N; i++) { const u = i / N, v = j / M; const rippe = Math.pow(0.5 + 0.5 * Math.cos(u * Math.PI * 2 * 8 + fbm(u * 4, v * 6, 1e9, 2, 2) * 1.5), 3);
    const fein = fbm(u * 64, v * 16, 64, 5, 3); H[j * N + i] = rippe * 0.8 + fein * 0.3; A[j * N + i] = 0.86 + rippe * 0.16 + (fein - 0.5) * 0.12 + (fbm(u * 8, v * 40, 8, 11, 2) - 0.5) * 0.15; }
  const nor = hoeheZuNormal(N, M, H, 7);
  const map = canvasTex(N, M, (x) => { const im = x.createImageData(N, M); for (let k = 0; k < N * M; k++) { const l = A[k]; im.data[k * 4] = Math.min(255, l * 238); im.data[k * 4 + 1] = Math.min(255, l * 240); im.data[k * 4 + 2] = Math.min(255, l * 220); im.data[k * 4 + 3] = 255; } x.putImageData(im, 0, 0); });
  map.colorSpace = THREE.SRGBColorSpace; return { map, nor }; }
// Haerchen auf Stengeln (Trichome)
function haerchen(mesh, anzahl, laenge, farbe) { const g = mesh.geometry, p = g.attributes.position, n = g.attributes.normal, tris = p.count / 3; const pos = []; let sd = 9; const r = () => (sd = sd * 16807 % 2147483647) / 2147483647;
  for (let k = 0; k < anzahl; k++) { const t = Math.floor(r() * tris) * 3; let a = r(), b = r(); if (a + b > 1) { a = 1 - a; b = 1 - b; } const c = 1 - a - b; const P = new THREE.Vector3(), Nn = new THREE.Vector3();
    for (const [w, idx] of [[a, t], [b, t + 1], [c, t + 2]]) { P.x += p.getX(idx) * w; P.y += p.getY(idx) * w; P.z += p.getZ(idx) * w; Nn.x += n.getX(idx) * w; Nn.y += n.getY(idx) * w; Nn.z += n.getZ(idx) * w; }
    Nn.normalize(); Nn.y += 0.6; Nn.normalize(); const L = laenge * (0.5 + r()); pos.push(P.x, P.y, P.z, P.x + Nn.x * L, P.y + Nn.y * L, P.z + Nn.z * L); }
  const lg = new THREE.BufferGeometry(); lg.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); return new THREE.LineSegments(lg, new THREE.LineBasicMaterial({ color: farbe, transparent: true, opacity: 0.35 })); }

const Farbe = { vertexShader: 'varying vec2 vUv; void main(){ vUv=uv; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0); }',
  fragmentShader: 'uniform sampler2D tDiffuse; varying vec2 vUv; void main(){ vec4 c=texture2D(tDiffuse,vUv); vec3 k=c.rgb; float l=dot(k,vec3(0.299,0.587,0.114)); k=mix(vec3(l),k,1.08); k=pow(k,vec3(0.97,0.99,1.03)); vec2 d=vUv-0.5; float v=smoothstep(0.85,0.25,length(d*vec2(1.0,0.8))); k*=mix(0.78,1.0,v); gl_FragColor=vec4(k,c.a); }',
  uniforms: { tDiffuse: { value: null } } };


/* ---- Qualitaet je nach Geraet ---- */
const KERNE = navigator.hardwareConcurrency || 4, RAM = navigator.deviceMemory || 8;
const HOCH = /[?&]hoch/.test(location.search) || !(KERNE <= 4 || RAM <= 3);
let TX = null; const tex = () => TX || (TX = { erde: erdTexturen(512, 'erde'), mulch: erdTexturen(512, 'mulch'), blatt: blattTexturen(), stengel: stengelTexturen() });

let FL = null; function flecken() { if (FL) return FL; FL = canvasTex(256, 256, (x, N) => { x.fillStyle = '#d8dcd6'; x.fillRect(0, 0, N, N); let sd = 77; const r = () => (sd = sd * 16807 % 2147483647) / 2147483647;
  for (let i = 0; i < 26; i++) { x.fillStyle = `rgba(250,252,246,${0.5 + r() * 0.4})`; x.beginPath(); x.ellipse(r() * N, r() * N, 3 + r() * 6, 1.5 + r() * 2, 0, 0, Math.PI * 2); x.fill(); }
  const im = x.getImageData(0, 0, N, N); for (let k = 0; k < N * N; k++) { const n = 0.94 + 0.06 * fbm((k % N) / 20, Math.floor(k / N) / 20, 1e9, 88, 2); for (let c = 0; c < 3; c++) im.data[k * 4 + c] *= n; } x.putImageData(im, 0, 0); }); FL.colorSpace = THREE.SRGBColorSpace; FL.repeat.set(3, 1); return FL; }
/* Pflanze veredeln (auch nach Umschalten ♀/♂) */
window.QW3D_PLUS_P = (pflanze) => { const { blatt: bt, stengel: st } = tex(); const haare = [];
  pflanze.traverse(o => { if (!o.isMesh) return; o.castShadow = true; o.receiveShadow = true; const m = o.material;
    if (m.userData && m.userData.dick) { o.material = durchlicht(new THREE.MeshPhysicalMaterial({ vertexColors: true, roughness: 0.42, clearcoat: 0.55, clearcoatRoughness: 0.35, sheen: 0.25, sheenColor: new THREE.Color(0xc8e0d0), map: flecken(), normalMap: tex().erde.nor, normalScale: new THREE.Vector2(0.12, 0.12) }), 0.3); return; }
    if (m.vertexColors && m.side === THREE.DoubleSide) o.material = durchlicht(new THREE.MeshPhysicalMaterial({ vertexColors: true, side: THREE.DoubleSide, map: bt.map, normalMap: bt.nor, normalScale: new THREE.Vector2(0.9, 0.9), roughness: 0.5, sheen: 0.6, sheenRoughness: 0.45, sheenColor: new THREE.Color(0x9fdc70), specularIntensity: 0.45, clearcoat: 0.15, clearcoatRoughness: 0.4, emissive: new THREE.Color(0x0e1c06) }), 0.55);
    else if (m.vertexColors && !o.isInstancedMesh) { st.map.repeat.set(1, 3); st.nor.repeat.set(1, 3); o.material = new THREE.MeshPhysicalMaterial({ vertexColors: true, map: st.map, normalMap: st.nor, normalScale: new THREE.Vector2(1.2, 1.2), roughness: 0.55, sheen: 0.4, sheenColor: new THREE.Color(0xc8e0a0), specularIntensity: 0.5 }); haare.push(o); }
    else if (m.isMeshStandardMaterial && !o.isInstancedMesh && m.color && m.color.g > m.color.r) { o.material = m.clone(); o.material.map = st.map; o.material.normalMap = st.nor; o.material.roughness = 0.55; } });
  if (HOCH) haare.forEach(o => { const tri = o.geometry.attributes.position.count / 3; pflanze.add(haerchen(o, Math.min(2500, Math.round(tri * 0.6)), 0.003, 0xc8d8b0)); }); };


/* ================= Wurzeln: plastisch, verzweigt, als Relief in der Schnittflaeche ================= */
function puffer() { return { pos: [], nor: [], uv: [], col: [], idx: [] }; }
function pufferGeo(B) { const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(B.pos, 3)); g.setAttribute('normal', new THREE.Float32BufferAttribute(B.nor, 3)); g.setAttribute('uv', new THREE.Float32BufferAttribute(B.uv, 2)); g.setAttribute('color', new THREE.Float32BufferAttribute(B.col, 3)); g.setIndex(B.idx); return g; }
function rohrIn(B, pts, r0, r1, ca, cb, rs, knoten) {
  const cu = new THREE.CatmullRomCurve3(pts), L = cu.getLength(), seg = Math.max(4, Math.min(80, Math.round(L / 0.008))); const fr = cu.computeFrenetFrames(seg, false);
  const base = B.pos.length / 3, P = new THREE.Vector3(), N = new THREE.Vector3(), c = new THREE.Color();
  for (let i = 0; i <= seg; i++) { const t = i / seg; cu.getPointAt(t, P); let r = r0 + (r1 - r0) * Math.pow(t, 0.7); if (knoten) r *= 1 + 0.1 * Math.max(0, Math.sin(t * L * 90)) ** 6; if (i === seg) r *= 0.3;
    c.copy(ca).lerp(cb, Math.pow(t, 1.4));
    for (let j = 0; j <= rs; j++) { const a = j / rs * Math.PI * 2; N.copy(fr.normals[i]).multiplyScalar(Math.cos(a)).addScaledVector(fr.binormals[i], Math.sin(a)).normalize();
      const w = 1 + 0.06 * Math.sin(a * 3 + t * 20); B.pos.push(P.x + N.x * r * w, P.y + N.y * r * w, P.z + N.z * r * w); B.nor.push(N.x, N.y, N.z); B.uv.push(j / rs, t * L * 6); const k = 0.92 + 0.08 * Math.sin(a * 5 + t * 31); B.col.push(c.r * k, c.g * k, c.b * k); } }
  for (let i = 0; i < seg; i++) for (let j = 0; j < rs; j++) { const a = base + i * (rs + 1) + j, b = a + rs + 1; B.idx.push(a, b, a + 1, b, b + 1, a + 1); } }
function wurzelTextur() { const N = 128, M = 512, H = new Float32Array(N * M);
  for (let j = 0; j < M; j++) for (let i = 0; i < N; i++) { const u = i / N, v = j / M; H[j * N + i] = 0.5 * fbm(u * 8, v * 64, 8, 21, 3) + 0.35 * Math.pow(Math.abs(Math.sin((v * 40 + fbm(u * 4, v * 8, 4, 2, 2) * 3) * Math.PI)), 8) + 0.25 * fbm(u * 32, v * 8, 32, 7, 2); }
  return hoeheZuNormal(N, M, H, 6); }
window.QW3D_PLUS_W = (w, s, info, c) => {
  if (!w) return null; s = s || 1; let sd = 4242; const r = () => (sd = sd * 16807 % 2147483647) / 2147483647;
  const B = puffer(), haar = []; const farbe = new THREE.Color(w.farbe || 0xd8c8a0); const alt = farbe.clone().multiplyScalar(0.72).lerp(new THREE.Color(0x6a4a2a), 0.25), jung = farbe.clone().lerp(new THREE.Color(0xf4efe0), 0.3);
  const hind = []; if (info.boden) info.boden.children.forEach(o => { if (o.isMesh && o.geometry.type === 'CircleGeometry' && o.position.z > 0 && o.geometry.parameters.radius < 0.25) hind.push([o.position.x, o.position.y - info.y0, o.geometry.parameters.radius + 0.012]); });
  const ymax = x => info.profil(x) - info.y0 - 0.015, ymin = info.UNTEN - info.y0 + 0.04, xm = info.BX * 0.94;
  const relief = p => new THREE.Vector3(p.x, p.y, 0.02 + Math.max(-0.25, Math.min(0.25, p.z)) * 0.06);
  function pfad(st, d0, len, grav, wand) { const n = Math.max(4, Math.round(len / 0.02)), sl = len / n, pts = [st.clone()]; let p = st.clone(), d = d0.clone().normalize();
    for (let k = 0; k < n; k++) { d.add(new THREE.Vector3((r() - .5) * wand, (r() - .5) * wand - grav, (r() - .5) * wand * 0.6)).normalize(); p = p.clone().addScaledVector(d, sl);
      if (p.y > ymax(p.x)) { p.y = ymax(p.x); d.y = -Math.abs(d.y) - 0.2; } if (p.y < ymin) { p.y = ymin; d.y = Math.abs(d.y) * 0.2; d.x += Math.sign(d.x || 1) * 0.5; } if (Math.abs(p.x) > xm) { p.x = Math.sign(p.x) * xm; d.x *= -0.5; }
      for (const [hx, hy, hr] of hind) { const dx = p.x - hx, dy = p.y - hy, dd = Math.hypot(dx, dy); if (dd < hr) { p.x = hx + dx / (dd || 1) * hr; p.y = hy + dy / (dd || 1) * hr; d.x += dx / (dd || 1) * 0.8; d.y += dy / (dd || 1) * 0.8; d.normalize(); } } pts.push(p); }
    return pts; }
  function ast(st, d, len, rad, stufe, maxStufe) { if (len < 0.015 || rad < 0.0006) return;
    const pts = pfad(st, d, len, stufe === 0 ? 0.3 : 0.1 + 0.05 * stufe, stufe === 0 ? 0.22 : 0.5); const rp = pts.map(relief);
    const ca = alt.clone().lerp(jung, stufe * 0.25), cb = jung.clone(); rohrIn(B, rp, rad, rad * (stufe === 0 ? 0.15 : 0.25), ca, cb, stufe === 0 ? 12 : stufe === 1 ? 8 : 5, stufe <= 1);
    if (stufe < maxStufe) { const n = stufe === 0 ? (w.seiten || 18) : stufe === 1 ? 7 : 4;
      for (let k = 0; k < n; k++) { const t = 0.06 + r() * 0.86, i = Math.min(pts.length - 2, Math.floor(t * (pts.length - 1))); const sx = r() < 0.5 ? -1 : 1;
        const sdv = new THREE.Vector3(sx * (0.6 + r() * 0.6), -0.2 - r() * 0.5, (r() - .5) * 0.8); ast(pts[i], sdv, len * (0.22 + r() * 0.3) * (1 - t * 0.45), rad * (0.3 + 0.2 * r()) * (1 - t * 0.5), stufe + 1, maxStufe); } }
    else { for (let i = Math.floor(rp.length * 0.4); i < rp.length; i++) for (let q = 0; q < 5; q++) { const p = rp[i], a = r() * Math.PI * 2, l = 0.002 + r() * 0.004; haar.push(p.x, p.y, p.z, p.x + Math.cos(a) * l, p.y + Math.sin(a) * l, p.z + 0.002); } } }
  const O = new THREE.Vector3(0, -0.005, 0); const g = new THREE.Group();
  if (w.typ === 'pfahl') ast(O, new THREE.Vector3(0.02, -1, 0), w.l * s, Math.max(0.006, w.r * s), 0, 3);
  else if (w.typ === 'faser' || w.typ === 'flach') { const n = w.typ === 'flach' ? 9 : Math.min(w.n || 20, 34); for (let k = 0; k < n; k++) { const a = -1.35 + 2.7 * (k + r() * 0.6) / n; const d = w.typ === 'flach' ? new THREE.Vector3(Math.sin(a) * 1.2, -0.25 - r() * 0.2, (r() - .5) * 0.5) : new THREE.Vector3(Math.sin(a), -Math.cos(a) * 0.9 - 0.2, (r() - .5) * 0.6);
      ast(O.clone().add(new THREE.Vector3((r() - .5) * 0.02, 0, 0)), d, (w.l || 0.4) * s * (0.6 + 0.5 * r()), (w.typ === 'flach' ? 0.022 : w.dick ? 0.005 : 0.003) * s, 1, w.typ === 'flach' ? 3 : 2); }
    if (w.stuetz) for (let k = 0; k < 6; k++) { const a = k * 1.05; rohrIn(B, [new THREE.Vector3(0, 0.08, 0), new THREE.Vector3(Math.cos(a) * 0.06, 0.03, 0.005), new THREE.Vector3(Math.cos(a) * 0.1, -0.04, 0.005)].map(p => new THREE.Vector3(p.x, p.y, 0.005 + p.z * 0.06)), 0.005, 0.003, alt, jung, 8); } }
  else if (w.typ === 'rhizom') { const om = new THREE.Color(w.farbe), im = new THREE.Color(w.innen || w.farbe);
    if (w.knollig) { const kg = new THREE.SphereGeometry(1, 20, 14); const kp = kg.attributes.position; for (let i = 0; i < kp.count; i++) { const v = new THREE.Vector3().fromBufferAttribute(kp, i); v.multiplyScalar(1 + 0.18 * (fbm(v.x * 2 + 5, v.y * 2 + v.z, 1e9, 3, 3) - 0.5) + 0.04 * Math.sin(v.y * 18)); kp.setXYZ(i, v.x, v.y, v.z); } kg.computeVertexNormals();
      const mo = new THREE.MeshPhysicalMaterial({ color: om.clone().multiplyScalar(0.7), roughness: 0.75, normalMap: tex().stengel.nor, normalScale: new THREE.Vector2(1.5, 1.5), sheen: 0.3 }), mi = new THREE.MeshStandardMaterial({ color: im, roughness: 0.45 });
      for (let k = 0; k < 9; k++) { const x = -0.26 + k * 0.065, y = -0.055 - 0.02 * Math.sin(k * 1.7); const b = new THREE.Mesh(kg, mo); b.scale.set(0.038, 0.026, 0.022); b.position.set(x, y, -0.004); b.rotation.z = (r() - .5) * 0.6; g.add(b);
        const fi = new THREE.Mesh(kg, mo); fi.scale.set(0.016, 0.034, 0.016); fi.position.set(x + 0.02, y - 0.045 * (k % 2 ? 1 : -0.7), -0.004); fi.rotation.z = (r() - .5); g.add(fi);
        if (k % 2 === 0) { const cg = new THREE.CircleGeometry(1, 28); const cp = cg.attributes.position; for (let i = 1; i < cp.count; i++) { const f = 1 + 0.08 * Math.sin(i * 1.3); cp.setXY(i, cp.getX(i) * f, cp.getY(i) * f); } const cut = new THREE.Mesh(cg, mi); cut.scale.set(0.034, 0.022, 1); cut.position.set(x, y, 0.0185); g.add(cut);
          const ring = new THREE.Mesh(new THREE.RingGeometry(0.85, 1, 28), new THREE.MeshStandardMaterial({ color: om.clone().multiplyScalar(0.7), roughness: 0.6 })); ring.scale.copy(cut.scale); ring.position.set(x, y, 0.0187); g.add(ring); } }
      for (let k = 0; k < 14; k++) ast(new THREE.Vector3(-0.26 + r() * 0.52, -0.08, 0), new THREE.Vector3((r() - .5), -1, 0), 0.15 * s, 0.0022, 2, 3); }
    else { const pts = []; const W = w.weit ? 0.6 : 0.45; for (let i = 0; i <= 10; i++) pts.push(new THREE.Vector3(-W + 2 * W * i / 10, -0.05 - 0.025 * Math.sin(i * 1.3), 0.005)); rohrIn(B, pts, 0.01, 0.008, om, om.clone().lerp(new THREE.Color(0xffffff), 0.2), 10, true);
      for (let i = 1; i < 10; i++) { const p = pts[i]; ast(p, new THREE.Vector3((r() - .5) * 0.6, -1, 0), 0.16 * s, 0.003, 2, 3); } } }
  else if (w.typ === 'myzel') { const lp = []; for (let i = 0; i < 1600; i++) { const x = (r() - .5) * 2.6, y = -0.02 - Math.pow(r(), 1.5) * 0.4, a = r() * 6.28, l = 0.02 + r() * 0.07; lp.push(x, y, 0.006, x + Math.cos(a) * l, y + Math.sin(a) * l * 0.6, 0.006); }
    const lg = new THREE.BufferGeometry(); lg.setAttribute('position', new THREE.Float32BufferAttribute(lp, 3)); g.add(new THREE.LineSegments(lg, new THREE.LineBasicMaterial({ color: 0xf4efe2, transparent: true, opacity: 0.55 })));
    for (let k = 0; k < 10; k++) ast(new THREE.Vector3((r() - .5) * 1.6, -0.02, 0), new THREE.Vector3(r() - .5, -0.4, 0), 0.4, 0.0018, 2, 3); }
  if (B.pos.length) { const nm = wurzelTextur(); const m = new THREE.Mesh(pufferGeo(B), new THREE.MeshPhysicalMaterial({ vertexColors: true, roughness: 0.72, normalMap: nm, normalScale: new THREE.Vector2(1.1, 1.1), clearcoat: 0.12, clearcoatRoughness: 0.6, specularIntensity: 0.3, envMapIntensity: 0.5 })); m.castShadow = true; m.receiveShadow = true; g.add(m); }
  if (haar.length) { const hg = new THREE.BufferGeometry(); hg.setAttribute('position', new THREE.Float32BufferAttribute(haar, 3)); g.add(new THREE.LineSegments(hg, new THREE.LineBasicMaterial({ color: 0xd8ccb0, transparent: true, opacity: 0.22 }))); }
  return g; };

/* ================= Huegelbeet: plastische Schnittflaeche, Holz, Erdschollen ================= */
function rindeTexturen() { const N = 256, M = 512, H = new Float32Array(N * M), A = new Float32Array(N * M);
  for (let j = 0; j < M; j++) for (let i = 0; i < N; i++) { const u = i / N, v = j / M; const ri = Math.pow(Math.abs(Math.sin((u * 10 + fbm(u * 6, v * 3, 6, 31, 3) * 2.2) * Math.PI)), 0.35); const pl = fbm(u * 12, v * 6, 12, 33, 4);
    H[j * N + i] = ri * 0.7 + pl * 0.5; A[j * N + i] = 0.35 + ri * 0.45 + (pl - 0.5) * 0.3; }
  const nor = hoeheZuNormal(N, M, H, 10); const map = canvasTex(N, M, x => { const im = x.createImageData(N, M); for (let k = 0; k < N * M; k++) { const l = A[k]; im.data[k * 4] = l * 150; im.data[k * 4 + 1] = l * 128; im.data[k * 4 + 2] = l * 104; im.data[k * 4 + 3] = 255; } x.putImageData(im, 0, 0); });
  map.colorSpace = THREE.SRGBColorSpace; return { map, nor }; }
function hirnholz(seed) { const N = 256, H = new Float32Array(N * N), A = new Float32Array(N * N * 3);
  for (let j = 0; j < N; j++) for (let i = 0; i < N; i++) { const x = (i / N - 0.5) * 2, y = (j / N - 0.5) * 2, rr = Math.hypot(x, y), a = Math.atan2(y, x); const k = j * N + i;
    const st = fbm(a * 2 + 10, rr * 3, 1e9, seed, 3); const rings = Math.sin((rr * 18 + st * 1.6) * Math.PI); const riss = Math.exp(-Math.pow(((a + Math.PI) * 3 / Math.PI % 1 - 0.5) / 0.02, 2)) * (rr > 0.15 ? 1 : 0) * (fbm(a * 3, 1, 1e9, seed + 1, 1) > 0.55 ? 1 : 0);
    const kern = rr < 0.55 ? 0.82 : 1; let l = (0.78 + 0.1 * rings) * kern - riss * 0.5; if (rr > 0.92) l = 0.38 + 0.1 * st; H[k] = rings * 0.2 - riss + (rr > 0.92 ? 0.4 : 0);
    A[k * 3] = l * 0.86; A[k * 3 + 1] = l * 0.68; A[k * 3 + 2] = l * 0.46; }
  const nor = hoeheZuNormal(N, N, H, 4); const map = canvasTex(N, N, x => { const im = x.createImageData(N, N); for (let k = 0; k < N * N; k++) { im.data[k * 4] = A[k * 3] * 255; im.data[k * 4 + 1] = A[k * 3 + 1] * 255; im.data[k * 4 + 2] = A[k * 3 + 2] * 255; im.data[k * 4 + 3] = 255; } x.putImageData(im, 0, 0); });
  map.colorSpace = THREE.SRGBColorSpace; map.wrapS = map.wrapT = THREE.ClampToEdgeWrapping; return { map, nor }; }
function veredleHuegel(boden, info) {
  const { profil, BX, UNTEN, SCH } = info; const lagen = SCH.map(([f, c0, c1]) => [f, new THREE.Color(c0), new THREE.Color(c1)]); const unter = [new THREE.Color(0x5a4a3a), new THREE.Color(0x6e5a44)];
  // alte flache Schnittbaender vorne ausblenden
  boden.children.forEach(o => { if (!o.isMesh) return; o.geometry.computeBoundingBox(); const b = o.geometry.boundingBox; const z0 = b.min.z + o.position.z, z1 = b.max.z + o.position.z;
    if (o.material.vertexColors && z1 < 0.002 && z0 > -0.001 && o.geometry.attributes.position.count < 3000) o.visible = false;
    if ((o.geometry.type === 'RingGeometry') && o.position.z > 0) o.visible = false; });
  // neue Schnittflaeche mit Relief
  const nx = 300, ny = 160, pos = [], col = [], uv = [], idx = []; const c = new THREE.Color();
  for (let j = 0; j <= ny; j++) for (let i = 0; i <= nx; i++) { const x = -BX + 2 * BX * i / nx, top = profil(x), v = j / ny, y = UNTEN + (top - UNTEN) * v;
    let f = y > 0 ? y / Math.max(top, 1e-4) : -1; const st = fbm(x * 5 + 7, y * 5, 1e9, 41, 3) - 0.5; const fn = f + st * 0.07;
    let k = -1; if (f >= 0) { k = lagen.length - 1; for (let q = 0; q < lagen.length; q++) { const fu = q < lagen.length - 1 ? lagen[q + 1][0] : 0; if (fn > fu) { k = q; break; } } }
    const fo = k >= 0 ? lagen[k][0] : 0, fu2 = k >= 0 ? (k < lagen.length - 1 ? lagen[k + 1][0] : 0) : -1; const tl = k >= 0 ? Math.min(1, Math.max(0, (fn - fu2) / Math.max(1e-3, fo - fu2))) : Math.min(1, Math.max(0, (y - UNTEN) / -UNTEN));
    const [ca, cb] = k >= 0 ? [lagen[k][1], lagen[k][2]] : unter; c.copy(ca).lerp(cb, tl);
    const nm = SCH[k] ? SCH[k][3] : ''; let d = (fbm(x * 18, y * 18, 1e9, 43, 4) - 0.5) * 0.014;
    if (nm.startsWith('Laub')) { const fa = fbm(x * 2.5, y * 70, 1e9, 44, 3); c.lerp(new THREE.Color(0xc8a24a), Math.max(0, fa - 0.5) * 1.4); d += (fa - 0.5) * 0.008; }
    if (nm === 'Grassoden') { const fa = fbm(x * 30, y * 30, 1e9, 45, 2); c.lerp(new THREE.Color(0x4a5a26), Math.max(0, fa - 0.55) * 1.6); }
    if (nm === 'Kompost' || nm === 'Mutterboden') { const kr = fbm(x * 45, y * 45, 1e9, 46, 2); d += Math.max(0, kr - 0.6) * 0.03; c.multiplyScalar(0.9 + kr * 0.25); }
    const kante = Math.min(1, (top - y) / 0.03, (BX - Math.abs(x)) / 0.06, Math.max(0, y - UNTEN) / 0.02); const z = 0.001 + Math.max(0, kante) * d;
    const sch = 0.9 + 0.2 * fbm(x * 9, y * 9, 1e9, 47, 2); pos.push(x, y, z); col.push(c.r * sch, c.g * sch, c.b * sch); uv.push(x * 3, y * 3); }
  for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) { const a = j * (nx + 1) + i, b = a + 1, cc = a + nx + 1, dd = cc + 1; idx.push(a, b, cc, b, dd, cc); }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute('color', new THREE.Float32BufferAttribute(col, 3)); g.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2)); g.setIndex(idx); g.computeVertexNormals();
  const { erde } = tex(); const sm = new THREE.Mesh(g, new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.97, map: erde.map, normalMap: erde.nor, normalScale: new THREE.Vector2(1.2, 1.2) })); sm.receiveShadow = true; boden.add(sm);
  // Holz: Rinde und Hirnholz, leicht vorstehend
  const ri = rindeTexturen(); let n = 0;
  boden.children.forEach(o => { if (!o.isMesh) return; const gp = o.geometry.parameters || {};
    if (o.geometry.type === 'CylinderGeometry' && gp.radiusTop > 0.05) { o.material = new THREE.MeshStandardMaterial({ color: 0xffffff, map: ri.map, normalMap: ri.nor, normalScale: new THREE.Vector2(1.5, 1.5), roughness: 0.95 }); ri.map.repeat.set(1, 3); ri.nor.repeat.set(1, 3); o.position.z += 0.014; o.castShadow = true; o.receiveShadow = true; }
    if (o.geometry.type === 'CircleGeometry' && gp.radius < 0.2 && o.position.z > 0) { const h = hirnholz(60 + n++); o.material = new THREE.MeshStandardMaterial({ map: h.map, normalMap: h.nor, roughness: 0.85 }); o.geometry = new THREE.CircleGeometry(gp.radius / 0.92, 48); o.position.z = 0.0145; o.receiveShadow = true; } });
  // Erdschollen auf der Oberflaeche
  boden.children.forEach(o => { if (!o.isMesh || !o.material.vertexColors || o.geometry.attributes.position.count < 3000) return; const p = o.geometry.attributes.position;
    for (let i = 0; i < p.count; i++) { const x = p.getX(i), z = p.getZ(i); if (Math.abs(x) > BX) continue; const k = Math.min(1, (BX - Math.abs(x)) / 0.15, -z / 0.05); const kl = fbm(x * 9 + 3, z * 9, 1e9, 51, 4), gr = fbm(x * 40, z * 40, 1e9, 52, 2);
      p.setY(i, p.getY(i) + k * ((kl - 0.5) * 0.03 + Math.max(0, gr - 0.62) * 0.025)); } p.needsUpdate = true; o.geometry.computeVertexNormals(); });
  // Regenwuermer feucht glaenzend
  boden.traverse(o => { if (o.isMesh && o.geometry.type === 'TubeGeometry') o.material = new THREE.MeshPhysicalMaterial({ color: 0xb46a6a, roughness: 0.35, clearcoat: 0.8, clearcoatRoughness: 0.2, sheen: 0.4 }); });
}
/* Blatt-Durchlicht (Gegenlicht laesst Blaetter leuchten) */
function durchlicht(m, staerke) { m.onBeforeCompile = sh => { sh.fragmentShader = sh.fragmentShader.replace('#include <lights_fragment_end>', `#include <lights_fragment_end>
  #if NUM_DIR_LIGHTS > 0
    { vec3 vd = normalize(vViewPosition); float bl = pow(max(dot(vd, directionalLights[0].direction), 0.0), 3.0); reflectedLight.directDiffuse += diffuseColor.rgb * directionalLights[0].color * bl * ${staerke.toFixed(2)}; }
  #endif`); }; m.customProgramCacheKey = () => 'durchlicht' + staerke; return m; }


/* ================= Bodenprofil & Kompost: plastische Schnittflaechen ================= */
function holzTex() { return canvasTex(128, 512, (x, N, M) => { const im = x.createImageData(N, M); for (let j = 0; j < M; j++) for (let i = 0; i < N; i++) { const k = (j * N + i) * 4, u = i / N, v = j / M;
  const g = fbm(u * 3, v * 40, 3, 61, 3), r = Math.pow(Math.abs(Math.sin((u * 9 + g * 3) * Math.PI)), 6); const l = 0.55 + 0.25 * g - 0.18 * r + 0.08 * fbm(u * 20, v * 4, 20, 62, 2);
  im.data[k] = l * 175; im.data[k + 1] = l * 132; im.data[k + 2] = l * 88; im.data[k + 3] = 255; } x.putImageData(im, 0, 0); }); }
function schnittRelief(scene, sn) {
  const { lagen, x0, x1, d, art } = sn; const L = lagen.map(([o, u, c0, c1, t]) => ({ o, u, a: new THREE.Color(c0), b: new THREE.Color(c1), t }));
  const yTop = L[0].o + (art === 'boden' ? 0.02 : 0.02), yBot = L[L.length - 1].u;
  // alte flache Baender ausblenden
  scene.children.forEach(o => { if (o.isMesh && o.material.vertexColors && o.material.side === THREE.DoubleSide && o.geometry.attributes.position.count < 500) o.visible = false; });
  const flaechen = [ { pt: (u, y) => new THREE.Vector3(x0 + (x1 - x0) * u, y, 0), n: new THREE.Vector3(0, 0, 1), len: x1 - x0 },
    { pt: (u, y) => new THREE.Vector3(x0, y, -d * u), n: new THREE.Vector3(-1, 0, 0), len: d }, { pt: (u, y) => new THREE.Vector3(x1, y, -d * u), n: new THREE.Vector3(1, 0, 0), len: d } ];
  const { erde } = tex(); const mat = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.96, map: erde.map, normalMap: erde.nor, normalScale: new THREE.Vector2(1.1, 1.1) });
  const c = new THREE.Color(), weiss = new THREE.Color(0xf0eadc), gelb = new THREE.Color(0xd2b058), gruen = new THREE.Color(0x5a7a2a), rost = new THREE.Color(0xa8582a), grau = new THREE.Color(0x8a8478), dunkel = new THREE.Color(0x1a120a), orange = new THREE.Color(0xc87a2a);
  flaechen.forEach((F, fi) => { const nu = Math.round(F.len * 140), nv = Math.round((yTop - yBot) * 140); const pos = [], col = [], uv = [], idx = [];
    for (let j = 0; j <= nv; j++) for (let i = 0; i <= nu; i++) { const u = i / nu, y = yBot + (yTop - yBot) * j / nv; const P = F.pt(u, y); const s = fi * 100 + u * F.len;
      const st = (fbm(s * 4, y * 4, 1e9, 71, 3) - 0.5) * 0.06; const yy = y + st; let k = L.length - 1; for (let q = 0; q < L.length; q++) if (yy > L[q].u) { k = q; break; } const Lk = L[k];
      const tl = Math.min(1, Math.max(0, (yy - Lk.u) / Math.max(1e-3, Lk.o - Lk.u))); c.copy(Lk.b).lerp(Lk.a, 1 - tl); let dd = (fbm(s * 16, y * 16, 1e9, 72, 4) - 0.5) * 0.012; const t = Lk.t;
      const n1 = fbm(s * 40, y * 40, 1e9, 73, 2), n2 = fbm(s * 9, y * 9, 1e9, 74, 3), str = fbm(s * 2, y * 60, 1e9, 75, 3);
      if (art === 'boden') {
        if (t.startsWith('O')) { c.lerp(n1 > 0.55 ? orange : dunkel, Math.abs(n1 - 0.5) * 1.2); dd += (n1 - 0.5) * 0.012; }
        else if (t.startsWith('A')) { c.multiplyScalar(0.85 + n1 * 0.35); dd += Math.max(0, n1 - 0.62) * 0.03; if (str > 0.68) c.lerp(new THREE.Color(0xd8c8a8), (str - 0.68) * 2); }
        else if (t.startsWith('B')) { c.lerp(rost, Math.max(0, n2 - 0.5) * 1.2); c.lerp(grau, Math.max(0, 0.42 - n2) * 1.5); }
        else { const stein = fbm(s * 7 + 3, y * 7, 1e9, 76, 2); if (stein > 0.56) { c.copy(grau).multiplyScalar(0.75 + n1 * 0.5); dd += (stein - 0.56) * 0.12; } } }
      else {
        if (t.startsWith('Abdeckung')) { c.lerp(gelb, Math.max(0, str - 0.45) * 1.5); dd += (str - 0.5) * 0.02; }
        else if (t.startsWith('Frisch')) { c.lerp(n2 > 0.55 ? gruen : orange, Math.abs(n2 - 0.5) * 1.3); if (n1 > 0.78) c.lerp(weiss, 0.7); dd += (n2 - 0.5) * 0.02; }
        else if (t.startsWith('Rotte')) { if (n1 > 0.72) c.lerp(weiss, (n1 - 0.72) * 2.5); dd += (n2 - 0.5) * 0.014; }
        else if (t.startsWith('Reifer')) { c.multiplyScalar(0.8 + n1 * 0.4); dd += Math.max(0, n1 - 0.6) * 0.025; }
        else { if (str > 0.55) c.lerp(new THREE.Color(0x7a5a38), (str - 0.55) * 2); dd += (str - 0.5) * 0.02; } }
      const kante = Math.min(1, u / 0.03, (1 - u) / 0.03, (yTop - y) / 0.02, (y - yBot) / 0.02); const Q = P.clone().addScaledVector(F.n, Math.max(0, kante) * dd + 0.002);
      pos.push(Q.x, Q.y, Q.z); col.push(c.r, c.g, c.b); uv.push(s * 3, y * 3); }
    for (let j = 0; j < nv; j++) for (let i = 0; i < nu; i++) { const a = j * (nu + 1) + i, b = a + 1, cc = a + nu + 1, e = cc + 1; if (fi === 1) idx.push(a, cc, b, b, cc, e); else idx.push(a, b, cc, b, e, cc); }
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute('color', new THREE.Float32BufferAttribute(col, 3)); g.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2)); g.setIndex(idx); g.computeVertexNormals();
    const m = new THREE.Mesh(g, mat); m.receiveShadow = true; m.castShadow = true; scene.add(m); });
  if (art === 'kompost') { const ht = holzTex(); ht.colorSpace = THREE.SRGBColorSpace; const hm = new THREE.MeshStandardMaterial({ map: ht, roughness: 0.9 });
    scene.traverse(o => { if (o.isMesh && o.geometry.type === 'BoxGeometry') { o.material = hm; o.castShadow = true; o.receiveShadow = true; } }); }
  scene.traverse(o => { if (o.isMesh && o.geometry.type === 'DodecahedronGeometry') { o.material = o.material.clone(); o.material.color.multiplyScalar(0.42); o.material.color.offsetHSL(0.02, 0.03, 0); o.material.roughness = 0.85; o.material.normalMap = tex().erde.nor; o.castShadow = true; } });
  // Grasbueschel auf dem Bodenblock als echte Halme
  scene.traverse(o => { if (o.isInstancedMesh && o.geometry.type === 'ConeGeometry') { o.geometry = HALM || (HALM = halmGeo()); o.material = HALM_M || (HALM_M = durchlicht(new THREE.MeshStandardMaterial({ vertexColors: true, side: THREE.DoubleSide, roughness: 0.75 }), 0.8));
    const M4 = new THREE.Matrix4(), p = new THREE.Vector3(), q = new THREE.Quaternion(), sc = new THREE.Vector3(); for (let i = 0; i < o.count; i++) { o.getMatrixAt(i, M4); M4.decompose(p, q, sc); p.y -= sc.y / 2; sc.set(1.4, sc.y * 1.3, sc.y * 1.3); M4.compose(p, q, sc); o.setMatrixAt(i, M4); } o.instanceMatrix.needsUpdate = true; o.castShadow = true; } }); }

window.QW3D_PLUS = ({ scene, renderer, cam, c, pflanze, boden, info }) => {
  if (boden && info && (!c.szene || c.szene === 'huegel')) veredleHuegel(boden, info);
  if (info && info.schnitt) schnittRelief(scene, info.schnitt);
  // kleine Pflanzen der Szene (Salat, Kohl, Löwenzahn) mit neuen Materialien
  scene.children.forEach(o => { if (o.isGroup && o !== pflanze && o !== boden && !o.userData.qwP) { let hatBlatt = false; o.traverse(m => { if (m.isMesh && m.material.vertexColors && m.material.side === THREE.DoubleSide) hatBlatt = true; }); if (hatBlatt) { o.userData.qwP = true; window.QW3D_PLUS_P(o); } } });
  renderer.setPixelRatio(Math.min(HOCH ? 1.5 : 1.25, devicePixelRatio));
  cam.far = 800; cam.updateProjectionMatrix(); renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 0.92; renderer.outputColorSpace = THREE.SRGBColorSpace; renderer.shadowMap.type = THREE.PCFShadowMap;
  const sonne = new THREE.Vector3().setFromSphericalCoords(1, THREE.MathUtils.degToRad(90 - 24), THREE.MathUtils.degToRad(-35));
  const sky = new Sky(); sky.scale.setScalar(90); const u = sky.material.uniforms; u.turbidity.value = 4.5; u.rayleigh.value = 1.6; u.mieCoefficient.value = 0.006; u.mieDirectionalG.value = 0.82; u.sunPosition.value.copy(sonne);
  const pm = new THREE.PMREMGenerator(renderer); const hs = new THREE.Scene(); hs.add(sky.clone()); scene.environment = pm.fromScene(hs, 0.02).texture; scene.environmentIntensity = 0.12; scene.add(sky); scene.background = null;
  scene.fog = new THREE.FogExp2(0xdde6ee, 0.03);
  scene.traverse(o => { if (o.isHemisphereLight) o.intensity = 0.15; if (o.isDirectionalLight) { if (o.castShadow) { o.color.set(0xffd09a); o.intensity = 5.5; o.position.copy(sonne).multiplyScalar(8); o.shadow.mapSize.set(HOCH ? 4096 : 1024, HOCH ? 4096 : 1024); o.shadow.normalBias = 0.015; o.shadow.radius = 3; Object.assign(o.shadow.camera, { left: -3.5, right: 3.5, top: 4.5, bottom: -2.5, far: 30 }); o.shadow.camera.updateProjectionMatrix(); if (o.shadow.map) { o.shadow.map.dispose(); o.shadow.map = null; } } else { o.intensity = 0.25; o.color.set(0xbcd2ff); } } });
  // Erde: alle Bodenflaechen (Vertexfarben, Rauheit 1)
  const { erde, mulch } = tex(); const neu = new Map(), pfl = new Set(); if (pflanze) pflanze.traverse(o => pfl.add(o));
  scene.traverse(o => { if (!o.isMesh || pfl.has(o) || !o.material.vertexColors || o.material.roughness !== 1) return; uvsPlanar(o.geometry, 3); const oben = o.geometry.attributes.position.count > 3000; const k = o.material.uuid + oben; let m = neu.get(k);
    if (!m) { m = o.material.clone(); const t = oben ? mulch : erde; m.map = t.map; m.normalMap = t.nor; m.normalScale = new THREE.Vector2(0.8, 0.8); m.needsUpdate = true; neu.set(k, m); } o.material = m; o.receiveShadow = true; });
  scene.traverse(o => { if (o.isMesh && !o.isInstancedMesh && !pfl.has(o) && o.geometry.type === 'CylinderGeometry' && o.geometry.parameters.radiusTop <= 0.003 && o.geometry.parameters.height < 0.2) o.scale.set(0.6, 0.55, 0.6); });
  // Wiese
  const unten = c.szene === 'boden';
  scene.traverse(o => { if (o.isMesh && o.geometry.type === 'CircleGeometry' && o.geometry.parameters.radius > 2) { o.geometry = new THREE.CircleGeometry(250, 96); const mat = new THREE.MeshStandardMaterial({ color: 0x3f5a28, roughness: 1 }); o.material = mat;
    new THREE.TextureLoader().load(import.meta.resolve('three/addons/') + '../textures/gras.jpg', t => { t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(100, 100); mat.map = t; mat.color.set(0x7a8a5a); mat.needsUpdate = true; }, undefined, () => {}); } });
  if (!unten) { const frei = c.szene === 'kompost' ? (x, z) => Math.abs(x) < 0.85 && z > -1.35 && z < 0.35 : (x, z) => Math.abs(x) < 1.65 && z > -1.75 && z < 0.45; grasWiese(scene, frei, HOCH ? 60000 : 18000, HOCH ? 8.5 : 6); }
  // Nachbearbeitung
  if (!HOCH) return null;
  const w = renderer.domElement.width, h = renderer.domElement.height;
  const rt = new THREE.WebGLRenderTarget(w, h, { type: THREE.HalfFloatType, samples: 4 }); const comp = new EffectComposer(renderer, rt); comp.addPass(new RenderPass(scene, cam));
  const ao = new GTAOPass(scene, cam, w, h); ao.blendIntensity = 0.4; ao.updateGtaoMaterial({ radius: 0.06, distanceExponent: 2, thickness: 0.25, scale: 0.8 }); if (!/noao/.test(location.search)) comp.addPass(ao);
  comp.addPass(new UnrealBloomPass(new THREE.Vector2(w, h), 0.1, 0.4, 2.2)); comp.addPass(new OutputPass()); comp.addPass(new ShaderPass(Farbe));
  const gr = () => { comp.setPixelRatio(renderer.getPixelRatio()); comp.setSize(renderer.domElement.clientWidth, renderer.domElement.clientHeight); }; addEventListener('resize', gr); gr();
  return { render: () => comp.render(), ende: () => { removeEventListener('resize', gr); comp.dispose(); } };
};
