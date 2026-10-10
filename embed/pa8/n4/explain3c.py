"""explain3b for arbitrary algebras: enumerate all unclosed 2-paths a~c~b (a !~ b, a<b) of a named algebra and, for each,
run the three-auxiliary explanation search of explain3b.py (full equality language, greedy weakening under SAT validity
at m=4, survivors checked at m=5).  Reports which paths admit an m=5-valid 2-path explanation.
Usage: python3 explain3c.py NAME [maxrows]     NAME in  P8:k (k=1..7)  |  R9  |  Q0  |  cand:k
"""
import sys, os, json, itertools, time, pickle
os.environ['EMBED_DIR'] = '/home/claude/pa8w/embed'
sys.path.append('/home/claude/pa8w/embed'); sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import valid

def load(name):
    E = '/home/claude/pa8w/embed/pa8/'
    if name.startswith('P8:'):
        P8 = [json.loads(l)['A'] for l in open(E + 'post8.log') if json.loads(l).get('embeds') is None]
        return P8[int(name[3:]) - 1]
    if name.startswith('cand:'):
        return json.load(open(E + 'cand9.json'))[int(name[5:])]
    if name == 'R9':
        for f in ['post9_0.log', 'post9_1.log', 'post9_3.log']:
            for l in open(E + f):
                r = json.loads(l)
                if r.get('embeds') is None and r.get('minimal') and r.get('violates', [None])[0] == 'Rprime': return r['A']
    if name == 'Q0':
        os.chdir('/home/claude/pa8w/embed')
        Tq, sq, A2 = pickle.load(open('hex_smallest.pkl', 'rb'))
        from layered import proj_algebra
        P, A = proj_algebra(list(range(len(Tq))), Tq, sq); return A
    if name.endswith('.json'):
        import json as _j; return _j.load(open(name))
    raise ValueError(name)

name = sys.argv[1]; maxrows = int(sys.argv[2]) if len(sys.argv) > 2 else 10**9
C = load(name); N = len(C); th = lambda p, q: C[q][p]
mt = lambda p, q: th(p, q) == p and th(q, p) == q
E = ['a', 'c', 'b', 'x', 'y', 'z']
SYM = E + [(u, v) for u in E for v in E if u != v]
path = [('mt', 'a', 'c'), ('mt', 'c', 'b')]; concl = ('mt', 'a', 'b')
def value(s, V): return V[s] if isinstance(s, str) else th(V[s[0]], V[s[1]])
def atoms_of(classes):
    out = list(path)
    for cl in classes:
        if len(cl) < 2: continue
        base = next((s for s in cl if isinstance(s, str)), cl[0])
        for s in cl:
            if s != base: out.append(('eq', s, base))
    return out
def ok(classes, m):
    try: return valid(atoms_of(classes), concl, m)
    except ValueError: return None
def fmt(s): return s if isinstance(s, str) else f"th_{s[0]}({s[1]})"
def show(classes): return ' | '.join('='.join(fmt(s) for s in cl) for cl in classes if len(cl) >= 2)
def weight(s):
    if isinstance(s, str): return 0 if s in 'xyz' else 3
    return 1 if (s[0] in 'xyz' or s[1] in 'xyz') else 2

paths = [(p0, p1, p2) for p0 in range(N) for p1 in range(N) for p2 in range(p0 + 1, N)
         if p1 not in (p0, p2) and mt(p0, p1) and mt(p1, p2) and not mt(p0, p2)]
print(f"{name}: order {N}, {len(paths)} unclosed 2-paths (a<b): {paths}", flush=True)
T0 = time.time(); summary = {}
for (p0, p1, p2) in paths:
    seen = set(); found = []; t0 = time.time(); nrows = 0
    for xyz in itertools.product(range(N), repeat=3):
        if nrows >= maxrows: break
        if len(set(xyz) | {p0, p1, p2}) < 6: continue
        V = dict(zip(E, (p0, p1, p2) + xyz))
        vals = {}
        for s in SYM: vals.setdefault(value(s, V), []).append(s)
        key = tuple(sorted(tuple(sorted(map(str, cl))) for cl in vals.values()))
        if key in seen: continue
        seen.add(key); nrows += 1
        classes = [list(cl) for cl in vals.values()]
        r = ok(classes, 4)
        if not r: continue
        for s in sorted(SYM, key=weight):
            cl = next(cl for cl in classes if s in cl)
            if len(cl) < 2: continue
            cl.remove(s); classes.append([s])
            if not ok(classes, 4): classes.pop(); cl.append(s)
        classes = [cl for cl in classes if len(cl) >= 2]
        sig = tuple(sorted(tuple(sorted(map(str, cl))) for cl in classes))
        if sig in {f[0] for f in found}: continue
        v5 = ok(classes, 5); found.append((sig, v5))
        print(f"  path {(p0,p1,p2)} xyz={xyz} valid m=5: {v5}:  {show(classes)}   [{time.time()-t0:.0f}s]", flush=True)
    n5 = sum(1 for f in found if f[1])
    summary[(p0, p1, p2)] = (len(found), n5)
    print(f"path {(p0,p1,p2)}: {nrows} rows, {len(found)} m=4-minimal partitions, {n5} valid at m=5 [{time.time()-t0:.0f}s]", flush=True)
print(f"SUMMARY {name}: " + '; '.join(f"{p}: {a} m4 / {b} m5" for p, (a, b) in summary.items()) + f"  [{time.time()-T0:.0f}s]", flush=True)
