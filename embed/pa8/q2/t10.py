from hq import *
def C_Z2(s): # N(c)∩N(d) block E: if Delta(E) = Delta_m and Lam(E) = Lam_k then m = k
    for E in s.Nc:
        if E not in s.Nd: continue
        dm = [m for m, (A, C, B, D) in enumerate(s.match) if C <= cls(E, s.Delta)]
        lk = [k for k, (A, C, B, D) in enumerate(s.match) if D <= cls(E, s.Lam)]
        if dm and lk and dm != lk: return False
    return True
def C_Z3(s): # N(b)-block F meeting supp c or supp d: if Delta(F)=Delta_m and Lam(F)=Lam_k then m = k
    for F in s.Nb:
        dm = [m for m, (A, C, B, D) in enumerate(s.match) if C <= cls(F, s.Delta)]
        lk = [k for k, (A, C, B, D) in enumerate(s.match) if D <= cls(F, s.Lam)]
        if dm and lk and dm != lk: return False
    return True
def C_Z4(s): # every N(c)∩N(d) block E: Delta(E) meets supp b iff Lam(E) meets supp b?
    for E in s.Nc:
        if E not in s.Nd: continue
        if bool(cls(E, s.Delta) & s.sb) != bool(cls(E, s.Lam) & s.sb): return False
    return True
def C_Z5(s): # D_k ∩ C_k != ∅ for k in T-lab group
    return all(bool(s.match[k][1] & s.match[k][3]) for (idx, lab, AG, CG) in s.groups if lab for k in idx)
def C_Z6(s): # D_k ∩ C_k ∩ B_k != ∅ for k in T-lab group
    return all(bool(s.match[k][1] & s.match[k][3] & s.match[k][2]) for (idx, lab, AG, CG) in s.groups if lab for k in idx)
claims = {k[2:]: v for k, v in list(globals().items()) if k.startswith('C_')}
run(4, ['instQ4.pkl'], claims, 4); run(5, ['instQ5_0.pkl'], claims, 4)
