"""Minimal hypothesis subsets (among H1..H6 of (R')) under which given word equations hold in P_n."""
import sys, itertools, time
sys.path.insert(0, '/mnt/user-data/outputs/starsemigroup/embed')
from pmon import projections, mul
n = int(sys.argv[1]); P = projections(n)
memo = {}
def m(p, q):
    k = (p, q)
    if k not in memo: memo[k] = mul(p, q, n)
    return memo[k]
def th(x, p): return m(m(x, p), x)
def matched(p, q): return th(p, q) == p and th(q, p) == q
def comm(p, q): return m(p, q) == m(q, p)
H = {1: lambda a,c,b,x,y: matched(a, c), 2: lambda a,c,b,x,y: matched(b, c), 3: lambda a,c,b,x,y: comm(x, c),
     4: lambda a,c,b,x,y: th(x, a) == th(x, c), 5: lambda a,c,b,x,y: comm(y, a), 6: lambda a,c,b,x,y: th(x, b) == th(y, b)}
L = 'acbxy'
def ev(w, I):
    d = dict(zip(L, I)); r = d[w[0]]
    for ch in w[1:]: r = m(r, d[ch])
    return r
EQS = [('xb','yb'), ('cy','cx'), ('ab','acb'), ('xa','xca'), ('ax','yac'), ('xab','xcb'), ('xy','yx'), ('aba','a'), ('bx','by'), ('xa','cya')]
# which variables does each hypothesis/equation involve -> only enumerate needed variables
import random
random.seed(1)
def holds(eq, S, limit=None):
    """does eq hold for all (a,c,b,x,y) in P_n satisfying hypotheses S? Random sampling + full check for small n."""
    vars_needed = set(eq[0] + eq[1])
    for h in S: vars_needed |= set({1:'ac',2:'bc',3:'xc',4:'xac',5:'ya',6:'xyb'}[h])
    order = [v for v in 'acbxy' if v in vars_needed]
    # backtracking enumeration with early hypothesis checks
    cnt = 0
    def rec(assign, i):
        nonlocal cnt
        if i == len(order):
            I = tuple(assign.get(v, P[0]) for v in 'acbxy')
            cnt += 1
            return ev(eq[0], I) == ev(eq[1], I)
        v = order[i]
        for p in P:
            assign[v] = p
            ok = True
            for h in S:
                hv = {1:'ac',2:'bc',3:'xc',4:'xac',5:'ya',6:'xyb'}[h]
                if all(u in assign for u in hv) and v in hv:
                    I = tuple(assign.get(u, P[0]) for u in 'acbxy')
                    if not H[h](*I): ok = False; break
            if ok and not rec(assign, i + 1): return False
        del assign[v]
        return True
    return rec({}, 0)
for eq in EQS:
    t0 = time.time()
    if not holds(eq, set(range(1, 7))):
        print(eq, "FAILS even with all hypotheses"); continue
    minimal = []
    for k in range(0, 7):
        for S in itertools.combinations(range(1, 7), k):
            if any(set(M) <= set(S) for M in minimal): continue
            if holds(eq, set(S)): minimal.append(S)
    print(f"{eq[0]} = {eq[1]}: minimal hypothesis sets {minimal}  ({time.time()-t0:.0f}s)", flush=True)
