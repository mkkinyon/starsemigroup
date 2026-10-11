"""Normal form hypothesis for 3-chains: x1' in Split(c), x2' in Split(z), x1' ~ x2', both identifying.  Split(p) = projections obtained from p by
cutting some N(p)-blocks into T-blocks (T(p)-blocks unchanged).  Test on all z in comp(c) in P_4 (and sampled pairs in P_5)."""
import sys, time, random
sys.path.insert(0, '/home/claude/pa8w/embed')
from pmon import projections, mul
n = int(sys.argv[1]); P = projections(n); memo = {}
def m_(p, q):
    k = (p, q)
    if k not in memo: memo[k] = mul(p, q, n)
    return memo[k]
th = lambda x, p: m_(m_(x, p), x); comm = lambda p, q: m_(p, q) == m_(q, p)
mt = lambda p, q: th(p, q) == p and th(q, p) == q
rank = lambda p: sum(1 for b in p if any(i < n for i in b) and any(i >= n for i in b))
def blocks(p):
    out = []
    for b in p:
        top = frozenset(i for i in b if i < n)
        if top: out.append((top, any(i >= n for i in b)))
    return out
def in_split(q, p):   # q in Split(p)?
    bq = dict(blocks(q)); bp = blocks(p)
    for pts, t in bp:
        if t:
            if bq.get(pts) is not True: return False
        else:
            if pts in bq and bq[pts] is False: continue
            # must be a union of T(q)-blocks
            if not all(bq[b] for b in bq if b <= pts) or frozenset().union(*[b for b in bq if b <= pts]) != pts: return False
    return True
random.seed(0); t0 = time.time()
pairs = [(a, c) for a in P for c in P if a != c and mt(a, c) and rank(a) >= 1]
if n >= 5: pairs = random.sample(pairs, 200)
tot = hard_tot = ok = ok_hard = 0; fails = []
for a, c in pairs:
    ident = lambda p: th(p, a) == th(p, c)
    I = [p for p in P if ident(p)]
    E1 = [x for x in I if comm(x, c)]; E2 = set(y for y in I if any(comm(x, y) for x in E1)); E3 = set(z for z in I if any(comm(y, z) for y in E2))
    S1 = [x for x in E1 if in_split(x, c)]
    for z in E3:
        tot += 1; hard = z not in E2; hard_tot += hard
        S2 = [y for y in I if comm(y, z) and in_split(y, z)]
        if any(comm(x, y) for x in S1 for y in S2): ok += 1; ok_hard += hard
        elif len(fails) < 3: fails.append((a, c, z))
print(f"n={n}: normal form works for {ok}/{tot} (hard: {ok_hard}/{hard_tot}) ({time.time()-t0:.0f}s)")
show = lambda p: '  '.join(('[' if t else '(') + ' '.join(map(str, sorted(bl))) + (']' if t else ')') for bl, t in blocks(p))
for a, c, z in fails: print('   fail: a =', show(a), '; c =', show(c), '; z =', show(z))
