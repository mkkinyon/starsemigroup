from hq import *
from run6 import run_sampled
def bridges(s): return [Q for Q in s.Nb if Q <= s.sa and all(A <= Q or not (A & Q) for A in s.A)]
def btype(s, Z): # Z ⊆ supp y, or Z ⊆ common group (N(y) and union of T(b)), or Z is co-bridge
    if Z <= s.sy: return True
    Q = next((Q for Q in s.Ny if Z <= Q), None)
    return Q is not None and (Q <= s.sb)
stats = {}
def C_stat(s):
    for Q in bridges(s):
        js = [j for j, m in enumerate(s.match) if m[0] <= Q]
        L = cls(Q, s.Lam); iis = [i for i, m in enumerate(s.match) if m[3] <= L]
        if not iis: continue
        i = iis[0]
        Ai, Ci, Bi, Di = s.match[i]
        same_grp = any(i in g[0] and any(j in g[0] for j in js) for g in s.groups)
        key = ('i in I_Q', i in js, 'same u-group', same_grp, 'A_i b-type', btype(s, Ai), 'Bi∩Di', bool(Bi & Di), 'Bi∩Ci', bool(Bi & Ci), 'Q meets Di', bool(Q & Di), 'Q meets Ci', bool(Q & Ci))
        stats[key] = stats.get(key, 0) + 1
    return True
run_sampled(5, ['instQ5_0.pkl', 'instQ5_1.pkl'], {'stat': C_stat}, 0, maxu=2, maxy=2)
run_sampled(6, ['instQ6_0.pkl', 'instQ6_1.pkl', 'instQ6_2.pkl'], {'stat': C_stat}, 0, maxu=2, maxy=2)
for k in sorted(stats, key=str): print(stats[k], k)
