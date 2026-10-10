"""Classify one-auxiliary path-closing hypothesis sets (pc1_4_3_size4.pkl): full validity by SAT (m = 4, 5), and
countermodels among the census algebras of order <= 8 with Q1, (S), (R) (ord2..ord8.json) -- an exhaustive test of
independence from Q1+(S)+(R) up to order 8.  Output: pc1_classified.json"""
import sys, os, json, pickle, itertools, time
sys.path.insert(0, '/home/claude/pa8w'); sys.path.insert(0, '/mnt/user-data/outputs/starsemigroup/embed')
from pathclose3 import fmt2
from pc3_verify import valid
from layered_search import canon

n = 3; V = ['p%d' % i for i in range(n + 1)]
d = pickle.load(open('pc1_4_3_size4.pkl', 'rb')); atoms, out = d['atoms'], d['out']

def holds_atom(A, at, P, x):
    th = lambda p, q: A[q][p]; le = lambda p, q: th(q, p) == p; mt = lambda p, q: th(p, q) == p and th(q, p) == q
    if at[0] == 'ch': return mt(P[at[1]], P[at[2]])
    k = at[1]
    if k == 'comm': return th(x, P[at[2]]) == th(P[at[2]], x)
    if k == 'zle': return le(x, P[at[2]])
    if k == 'lez': return le(P[at[2]], x)
    if k == 'sees': return th(x, P[at[2]]) == th(x, P[at[3]])
    if k == 'seen': return th(P[at[2]], x) == th(P[at[3]], x)
    if k == 'zeq': return th(P[at[2]], P[at[3]]) == x

def violation(A, H):
    """an assignment (any elements) satisfying the path and H with p_0 !~ p_n, or None"""
    N = len(A); th = lambda p, q: A[q][p]; mt = lambda p, q: th(p, q) == p and th(q, p) == q
    matched = {p: [q for q in range(N) if mt(p, q)] for p in range(N)}
    def paths(prefix):
        if len(prefix) == n + 1: yield prefix; return
        for q in matched[prefix[-1]]: yield from paths(prefix + [q])
    for p0 in range(N):
        for P in paths([p0]):
            if mt(P[0], P[-1]): continue
            for x in range(N):
                if all(holds_atom(A, at, P, x) for at in H): return (P, x)
    return None

census = []
for k in range(2, 9):
    f = f'/home/claude/pa8w/ord{k}.json'
    if os.path.exists(f): census += json.load(open(f))
print(len(census), "census algebras of order <= 8 with Q1, (S), (R)", flush=True)
res = []
for H in out:
    Hl = [atoms[k] for k in range(len(atoms)) if H >> k & 1]
    rec = dict(H=[list(a) for a in Hl], text=[fmt2(a, V) for a in Hl])
    t = time.time()
    rec['valid4'] = valid(Hl, n, 4)
    rec['valid5'] = valid(Hl, n, 5) if rec['valid4'] else None
    rec['secs'] = round(time.time() - t, 1)
    if rec['valid5']:
        cm = [(len(A), violation(A, Hl)) for A in census if violation(A, Hl)]
        rec['countermodels'] = len(cm); rec['min_order'] = min((c[0] for c in cm), default=None)
    res.append(rec)
    print(rec['text'], "valid4", rec['valid4'], "valid5", rec['valid5'], "countermodels<=8:", rec.get('countermodels'), "min order", rec.get('min_order'), f"({rec['secs']}s)", flush=True)
json.dump(res, open('pc1_classified.json', 'w'), indent=1)
