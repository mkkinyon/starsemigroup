"""Do chain ends stabilise?  E_k(a,c) = {z : exists chain c~x_1~...~x_k = z, all identifying}.  Is E_3 = E_2 (and E_2 = E_1)?  In P_n."""
import sys, time, itertools
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
t0 = time.time(); stats = {'pairs': 0, 'E2!=E1': 0, 'E3!=E2': 0, 'E4!=E3': 0}; ex = None
import random; random.seed(0)
pairs = [(a, c) for a in P for c in P if a != c and mt(a, c) and rank(a) >= 1]
if n >= 5: pairs = random.sample(pairs, 1500)
print(len(pairs), 'matched pairs (a,c) with rank >= 1', flush=True)
for a, c in pairs:
    ident = [p for p in P if th(p, a) == th(p, c)]
    E = [set(x for x in ident if comm(x, c))]
    for k in range(4):
        E.append(set(z for z in ident if any(comm(y, z) for y in E[-1])))
    stats['pairs'] += 1
    if E[1] != E[0]: stats['E2!=E1'] += 1
    if E[2] != E[1]:
        stats['E3!=E2'] += 1
        if ex is None: ex = (a, c, E[2] - E[1])
    if E[3] != E[2]: stats["E4!=E3"] += 1
    if E[4] != E[3]: stats["E5!=E4"] = stats.get("E5!=E4", 0) + 1
print(stats, f"({time.time()-t0:.0f}s)")
if ex:
    def blocks(p):
        out = []
        for b in p:
            top = {i for i in b if i < n}
            if top: out.append((top, 'T' if any(i >= n for i in b) else 'N'))
        return out
    show = lambda p: '  '.join(('[' if k == 'T' else '(') + ' '.join(map(str, sorted(bl))) + (']' if k == 'T' else ')') for bl, k in blocks(p))
    a, c, diff = ex; print('example: a =', show(a), ' c =', show(c)); [print('   new at length 3: z =', show(z)) for z in list(diff)[:5]]
