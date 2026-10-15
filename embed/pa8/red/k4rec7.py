import sys, pickle
sys.path.insert(0, '/home/claude/pa8w/review2/review-scripts')
from fast import *
INST = pickle.load(open('k4inst4.pkl', 'rb'))
stats = {}
def rec(name, val):
    s = stats.setdefault(name, [0, 0]); s[0] += 1; s[1] += val
def refines(p, J): return all(any(K & B == B for K in J) for B in p[0])
def join3(p, q, s): return join((join(p, q), p[1]), s)  # join of partitions: treat join(p,q) as block list
def J3(p, q, s):
    # classes of eps_p v eps_q v eps_s
    return join(((tuple(join(p, q))), 0), s)
def nT(p, J): return sum(1 for K in J if K & p[1])
for I in INST:
    a, b, c, y, z = I['a'], I['b'], I['c'], I['y'], I['z']
    r = theta(y, a); v = theta(b, a); u = theta(a, b)
    Jab = join(a, b); Jar = join(a, r); Jbr = join(b, r); Jabr = J3(a, b, r)
    rec('(G1)_r: eps_r <= eps_a v eps_b', refines(r, Jab))
    rec('(G2)_r: no class of a v b v r has two T(r)', all(sum(1 for R in r[0] if R & r[1] and R & K) <= 1 for K in Jabr))
    dv = len(join(v, a)) - len(join(v, r)); dr = len(Jar) - len(r[0])
    rec('delta_ar(v) = delta_ar(r)', dv == dr)
    dvp = nT(a, join(v, a)) - nT(r, join(v, r)); rec("delta'_ar(v)=0", dvp == 0)
    # also with c: (G1)_c
    rec('(G1)_c: eps_c <= eps_a v eps_b', refines(c, Jab))
    rec('delta_ar(b) = delta_ar(r)', len(Jab) - len(Jbr) == dr)
    rec('delta_ac(v) = delta_ac(c)', len(join(v,a)) - len(join(v,c)) == len(join(a,c)) - len(c[0]))
print(len(INST), 'instances')
for k, (tot, ok) in stats.items(): print('  %-44s %d/%d%s' % (k, ok, tot, '   ALWAYS' if ok == tot else ('   NEVER' if ok == 0 else '')))
