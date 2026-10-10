from hq import *
from run6 import run_sampled
import pickle
# cross-wiring of 2-hubs on the b-side: D_H <= Delta_k, C_H <= Lambda_l with {k,l}=H, k != l
def hubs(s):
    return [(idx, CG, cls(CG, s.Pi1)) for idx, lab, AG, CG in s.groups if CG in s.Nd]
def C_cross(s):
    for idx, CG, GG in hubs(s):
        if len(idx) != 2: continue
        k, l = sorted(idx)
        DH = s.match[k][3] | s.match[l][3]
        assert DH in s.Nc
        dk = [m for m in idx if DH <= cls(s.match[m][1], s.Delta)]  # Delta index of D_H
        lk = [m for m in idx if CG <= cls(s.match[m][3], s.Lam)]    # Lambda index of C_H
        if len(dk) != 1 or len(lk) != 1 or dk[0] == lk[0]: return False
    return True
shown = [0]
def C_show2(s):
    if shown[0] >= 4: return True
    for idx, CG, GG in hubs(s):
        if len(idx) == 2:
            shown[0] += 1
            P, T = TAB[s.n]
            print("---- 2-hub", sorted(idx))
            for nm, i in zip('acbduy', s.ids): print(f"    {nm} = {show(P, s.n, i)}")
            for i, (A, C, B, D) in enumerate(s.match): print("   ", i, 'A', sorted(A), 'C', sorted(C), 'B', sorted(B), 'D', sorted(D))
            print("    Gamma", [sorted(g) for g in s.Gamma]); print("    Delta", [sorted(g) for g in s.Delta]); print("    Lam", [sorted(g) for g in s.Lam]); print("    rho", [sorted(g) for g in s.rho])
            print("    Pi1", [sorted(g) for g in s.Pi1]); print("    Pa", [sorted(g) for g in s.Pa]); print("    Pb", [sorted(g) for g in s.Pb])
            print("    groups", [(sorted(i), l) for i, l, _, _ in s.groups])
            return True
    return True
TAB = {}
for n in (5, 6):
    TAB[n] = pickle.load(open(f'/home/claude/pa8w/gen/tab{n}.pkl', 'rb'))
run_sampled(5, ['instQ5_0.pkl', 'instQ5_1.pkl'], {'cross': C_cross, 'show': C_show2}, 2, maxu=3, maxy=2)
run_sampled(6, ['instQ6_0.pkl', 'instQ6_1.pkl', 'instQ6_2.pkl'], {'cross': C_cross, 'show': C_show2}, 2, maxu=3, maxy=2)
