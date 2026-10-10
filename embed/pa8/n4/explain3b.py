"""Three-auxiliary explanations in the full equality language: symbols = the six elements (path a,c,b and x,y,z) and
the 30 terms theta_u(v), u != v; a hypothesis is the partition of the symbols induced by an assignment (x,y,z) in the
candidate; it is weakened greedily by splitting off symbols, under SAT validity at m=4; survivors checked at m=5.
Usage: python3 explain3b.py cand p0 p1 p2 [maxrows]"""
import sys, os, json, itertools, time
os.environ['EMBED_DIR'] = '/home/claude/pa8w/embed'
sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import valid
c, p0, p1, p2 = map(int, sys.argv[1:5]); maxrows = int(sys.argv[5]) if len(sys.argv) > 5 else 10**9
C = json.load(open('/home/claude/pa8w/embed/pa8/cand9.json'))[c]; N = len(C); th = lambda p, q: C[q][p]
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
def show(classes):
    return ' | '.join('='.join(fmt(s) for s in cl) for cl in classes if len(cl) >= 2)
seen = set(); found = []; t0 = time.time(); nrows = 0
# weight: prefer to split off terms/elements involving x,y,z first (drop auxiliary information), then path terms
def weight(s):
    if isinstance(s, str): return 0 if s in 'xyz' else 3
    return 1 if (s[0] in 'xyz' or s[1] in 'xyz') else 2
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
    # element 'a' and 'b' identity atoms are fine; skip rows where a==b etc. (degenerate)
    if V['a'] == V['b']: continue
    r = ok(classes, 4)
    if not r: continue
    # greedy splitting
    for s in sorted(SYM, key=weight):
        cl = next(cl for cl in classes if s in cl)
        if len(cl) < 2: continue
        cl.remove(s); classes.append([s])
        if not ok(classes, 4): classes.pop(); cl.append(s)
    classes = [cl for cl in classes if len(cl) >= 2]
    sig = tuple(sorted(tuple(sorted(map(str, cl))) for cl in classes))
    if sig in {f[0] for f in found}: continue
    v5 = ok(classes, 5); found.append((sig, v5))
    print(f"xyz={xyz} valid m=5: {v5}:  {show(classes)}   [{time.time()-t0:.0f}s]", flush=True)
print(f"done: {nrows} distinct rows, {len(found)} minimal partitions [{time.time()-t0:.0f}s]")
