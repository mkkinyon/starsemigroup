"""Contraction test on (W_2) instances in P_4: given a|><|c, c~x~y both identifying a with c, is there a projection z with
c~z, z identifying a with c, and z~b for every b with b|><|c, y~b?  (Then (W_2) would follow from (W_1) applied to z.)"""
import sys, pickle, time, itertools
sys.path.insert(0, '/home/claude/pa8w/embed')
from pmon import projections, mul
n = 4; P = projections(n); memo = {}
def m(p, q):
    k = (p, q)
    if k not in memo: memo[k] = mul(p, q, n)
    return memo[k]
th = lambda x, p: m(m(x, p), x)
mt = lambda p, q: th(p, q) == p and th(q, p) == q
comm = lambda p, q: m(p, q) == m(q, p)
inst = pickle.load(open('../rpp/w2inst4.pkl', 'rb'))
# group by (a, c, x, y)
groups = {}
for a, c, b, x, y in inst: groups.setdefault((a, c, x, y), set()).add(b)
print(len(inst), 'instances,', len(groups), 'groups (a,c,x,y)', flush=True)
t0 = time.time(); bad = 0; bad_ex = None; nontriv = 0; stats = {'z=x': 0, 'z=y': 0, 'other': 0}
for (a, c, x, y), Bs in groups.items():
    Z = [z for z in P if comm(z, c) and th(z, a) == th(z, c) and all(comm(z, b) for b in Bs)]
    if not Z:
        bad += 1
        if bad_ex is None: bad_ex = (a, c, x, y, sorted(Bs))
    else:
        if x in Z: stats['z=x'] += 1
        elif y in Z: stats['z=y'] += 1
        else: stats['other'] += 1
print(f"groups without a contracting z: {bad} of {len(groups)} ({time.time()-t0:.0f}s); {stats}", flush=True)
if bad_ex: print('example without z:', bad_ex)
