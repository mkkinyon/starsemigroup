from hq import *
from t12 import kappas
def attach(s):
    """for non-hub groups: returns per i the set of D-indices attached to A_i (direct or via kappa with alpha=i), per k the A's attached"""
    Ai_D = {}; Dk_A = {}
    for (idx, lab, AG, CG) in s.groups:
        if CG in s.Nd: continue
        GG = cls(CG, s.Pi1)
        for i in idx:
            Ai_D[i] = {k for k in idx if s.match[i][0] & s.match[k][3]}
        for k in idx:
            Dk_A[k] = {i for i in idx if s.match[i][0] & s.match[k][3]}
        for kap in kappas(s, GG):
            alpha = [i for i in idx if any(E & s.match[i][0] for E in kap if E in s.Nc)]
            Ds = [k for k in idx if any(F & s.match[k][3] for F in kap if F in s.Na)]
            for i in alpha:
                for k in Ds: Ai_D[i].add(k); Dk_A[k].add(i)
    return Ai_D, Dk_A
def C_T2p(s): return all(len(v) <= 1 for v in attach(s)[0].values())
def C_T4p(s): return all(len(v) <= 1 for v in attach(s)[1].values())
def C_E5(s): return all(len(v) >= 1 for v in attach(s)[0].values())
def C_E6(s): return all(len(v) >= 1 for v in attach(s)[1].values())
def C_T1(s):
    for (idx, lab, AG, CG) in s.groups:
        if CG in s.Nd: continue
        GG = cls(CG, s.Pi1)
        for kap in kappas(s, GG):
            Ds = [k for k in idx if any(F & s.match[k][3] for F in kap if F in s.Na)]
            if len(Ds) > 1: return False
    return True
claims = {k[2:]: v for k, v in list(globals().items()) if k.startswith('C_')}
run(4, ['instQ4.pkl'], claims, 2); run(5, ['instQ5_0.pkl', 'instQ5_1.pkl'], claims, 2)
