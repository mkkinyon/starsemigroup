"""Minimise the diagram of an order-9 candidate C with respect to a path-closing conclusion (mt p q), eliminating whole
variables first (all atoms mentioning an element), then atoms, under SAT validity in P(P_m) (variables not distinct).
Usage: python3 min9.py cand p q m"""
import sys, os, json, time
os.environ['EMBED_DIR'] = '/home/claude/pa8w/embed'
sys.path.insert(0, '/home/claude/pa8w/embed/pa8')
from qi_extract import valid
c, p, q, m = map(int, sys.argv[1:5])
C = json.load(open('/home/claude/pa8w/embed/pa8/cand9.json'))[c]; k = len(C); nm = 'abcdefghi'
concl = ('mt', p, q)
H = {(x, y): C[x][y] for x in range(k) for y in range(k) if x != y}
def mentions(H, z): return {key for key in H if z in key or H[key] == z}
def show(H):
    out = []
    for (x, y), v in sorted(H.items()):
        if v == x: out.append(f"{nm[x]}<={nm[y]}")
        elif v == y: out.append(f"{nm[y]}{nm[x]}{nm[y]}={nm[y]}")
        else: out.append(f"{nm[y]}{nm[x]}{nm[y]}={nm[v]}")
    return ', '.join(out)
t0 = time.time()
assert valid(k, H, concl, m), "full diagram not valid?!"
# variable elimination: try elements other than p, q, most-mentioned first
others = sorted([z for z in range(k) if z not in (p, q)], key=lambda z: -len(mentions(H, z)))
for z in others:
    H2 = {key: v for key, v in H.items() if key not in mentions(H, z)}
    if H2 and valid(k, H2, concl, m): H = H2; print(f"  eliminated {nm[z]} ({len(H)} atoms, {time.time()-t0:.0f}s)", flush=True)
# atom-wise greedy
for key in sorted(H, key=lambda key: (key[0] in (p, q)) + (key[1] in (p, q))):
    H2 = {kk: v for kk, v in H.items() if kk != key}
    if valid(k, H2, concl, m): H = H2
vars_ = sorted({z for key, v in H.items() for z in (key[0], key[1], v)} | {p, q})
print(f"cand {c} concl {nm[p]}~{nm[q]} m={m}: {len(H)} atoms, {len(vars_)} vars [{time.time()-t0:.0f}s]\n   {show(H)}", flush=True)
json.dump({'cand': c, 'concl': [p, q], 'm': m, 'H': [[list(key), v] for key, v in H.items()]}, open(f'min9_{c}_{p}{q}_{m}.json', 'w'))
