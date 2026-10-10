"""Three-auxiliary explanations of an unclosed 2-path (p0,p1,p2) in an order-9 candidate: for every (x,y,z) in A^3,
the row of true atoms (structured language below) is minimised greedily under SAT validity at m=4 (then m=5).
Usage: python3 explain3.py cand p0 p1 p2"""
import sys, os, json, itertools, time
os.environ['EMBED_DIR'] = '/home/claude/pa8w/embed'
sys.path.insert(0, '/home/claude/pa8w/n4')
from qi import valid
c, p0, p1, p2 = map(int, sys.argv[1:5])
C = json.load(open('/home/claude/pa8w/embed/pa8/cand9.json'))[c]; N = len(C); th = lambda p, q: C[q][p]
P = ['a', 'c', 'b']; Z = ['x', 'y', 'z']
def atoms():
    A = []
    for z in Z:
        for p in P: A += [('comm', z, p), ('le', z, p), ('le', p, z)]
        for p, q in itertools.combinations(P, 2): A += [('eq', (z, p), (z, q)), ('eq', (p, z), (q, z))]
    for z1, z2 in itertools.combinations(Z, 2):
        A += [('comm', z1, z2), ('le', z1, z2), ('le', z2, z1)]
        for p in P:
            for q in P: A += [('eq', (z1, p), (z2, q)), ('eq', (p, z1), (q, z2))]
    return A
A = atoms()
def holds(at, V):
    k = at[0]
    if k == 'comm': return th(V[at[1]], V[at[2]]) == th(V[at[2]], V[at[1]])
    if k == 'le': return th(V[at[2]], V[at[1]]) == V[at[1]]
    if k == 'eq':
        ev = lambda t: th(V[t[0]], V[t[1]])
        return ev(at[1]) == ev(at[2])
path = [('mt', 'a', 'c'), ('mt', 'c', 'b')]; concl = ('mt', 'a', 'b')
def fmt(at):
    if at[0] == 'comm': return f"{at[1]}{at[2]}={at[2]}{at[1]}"
    if at[0] == 'le': return f"{at[1]}<={at[2]}"
    f = lambda t: f"th_{t[0]}({t[1]})"
    return f"{f(at[1])}={f(at[2])}"
seen = set(); found = []; t0 = time.time(); nrows = 0
for xyz in itertools.product(range(N), repeat=3):
    V = dict(zip(P, (p0, p1, p2))); V.update(zip(Z, xyz))
    row = tuple(i for i, at in enumerate(A) if holds(at, V))
    if row in seen: continue
    seen.add(row); nrows += 1
    if any(set(f) <= set(row) for f in found): continue   # already explained by a found minimal set
    S = list(row)
    try:
        if not valid(path + [A[i] for i in S], concl, 4): continue
        # drop atoms: cross atoms first, then le/comm, then sees/seen
        order = sorted(S, key=lambda i: (0 if (A[i][0] == 'eq' and A[i][1][0] in Z and A[i][2][0] in Z) or (A[i][0] in ('comm', 'le') and A[i][1] in Z and A[i][2] in Z) else 1 if A[i][0] in ('le', 'comm') else 2, i))
        for i in order:
            S2 = [j for j in S if j != i]
            if valid(path + [A[j] for j in S2], concl, 4): S = S2
        v5 = valid(path + [A[j] for j in S], concl, 5)
    except ValueError: continue
    found.append(tuple(S))
    print(f"xyz={xyz} size {len(S)} valid m=5: {v5}: ", ', '.join(fmt(A[j]) for j in S), f"[{time.time()-t0:.0f}s]", flush=True)
print(f"done: {nrows} distinct rows, {len(found)} minimal sets [{time.time()-t0:.0f}s]")
