from hq import *
def hubs(s): return [(idx, CG, cls(CG, s.Pi1)) for idx, lab, AG, CG in s.groups if CG in s.Nd]
def pi_of(s, GG):  # indices k with D_k inside Gamma_G
    return [k for k, m in enumerate(s.match) if m[3] <= GG]
def C_H1p(s): # Lam(C_G) contains exactly one T(d)-block, D_j with j in G
    for idx, CG, GG in hubs(s):
        L = cls(CG, s.Lam); js = [j for j, m in enumerate(s.match) if m[3] <= L]
        if len(js) != 1 or js[0] not in idx: return False
    return True
def C_H2p(s): # Delta(E_G) contains exactly one T(c)-block C_k with k in pi(G)
    for idx, CG, GG in hubs(s):
        E = GG & s.sd; Dl = cls(E, s.Delta); ks = [k for k, m in enumerate(s.match) if m[1] <= Dl]
        if len(ks) != 1 or ks[0] not in pi_of(s, GG): return False
    return True
def C_H1q(s): # Lam(C_G) contains at least one T(d)
    for idx, CG, GG in hubs(s):
        L = cls(CG, s.Lam)
        if not any(m[3] <= L for m in s.match): return False
    return True
def C_H2q(s): # Delta(E_G) contains at least one T(c)
    for idx, CG, GG in hubs(s):
        E = GG & s.sd; Dl = cls(E, s.Delta)
        if not any(m[1] <= Dl for m in s.match): return False
    return True
def C_H8(s): # 2-hub G={i,j}: the two A's: exactly one meets C_G; the D_j in Lam(C_G): j is the one whose A meets C_G?
    for idx, CG, GG in hubs(s):
        if len(idx) != 2: continue
        L = cls(CG, s.Lam); js = [j for j, m in enumerate(s.match) if m[3] <= L]
        Ai = [i for i in idx if s.match[i][0] & CG]
        if len(Ai) != 1: return False
        if js and js[0] != Ai[0]: return False
    return True
def C_H9(s): # 2-hub: E_G = D_k ∪ D_l with {k,l} = pi(G); exactly one of D_k, D_l meets supp b (i.e. B_k or B_l meets E_G)? 
    for idx, CG, GG in hubs(s):
        if len(idx) != 2: continue
        ks = pi_of(s, GG)
        nb = sum(1 for k in ks if s.match[k][3] & s.match[k][2])
        if nb > 1: return False
    return True
claims = {k[2:]: v for k, v in list(globals().items()) if k.startswith('C_')}
run(4, ['instQ4.pkl'], claims, 3); run(5, ['instQ5_0.pkl', 'instQ5_1.pkl'], claims, 3)
