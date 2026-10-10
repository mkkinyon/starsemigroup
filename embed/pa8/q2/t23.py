from hq import *
import pickle
def hubs2(s): return [(idx, CG, cls(CG, s.Pi1)) for idx, lab, AG, CG in s.groups if CG in s.Nd and len(idx) == 2]
def C_2a(s):
    return all(sum(1 for i in idx if s.match[i][0] & CG) == 1 for idx, CG, GG in hubs2(s))
def C_2b(s): # the A not meeting C_G meets exactly one D (in E_G)
    for idx, CG, GG in hubs2(s):
        E = GG & s.sd
        for i in idx:
            if not (s.match[i][0] & CG):
                if sum(1 for D in s.D if D <= E and D & s.match[i][0]) != 1: return False
    return True
def C_2c(s): # the A meeting C_G meets no D
    for idx, CG, GG in hubs2(s):
        for i in idx:
            if (s.match[i][0] & CG) and any(D & s.match[i][0] for D in s.D): return False
    return True
def C_2d(s): # rho-class of C_G contains exactly one D (the other one) and the A meeting C_G
    for idx, CG, GG in hubs2(s):
        R = cls(CG, s.rho); E = GG & s.sd
        Ds = [D for D in s.D if D <= R]; As = [i for i in idx if s.match[i][0] <= R]
        if len(Ds) != 1 or len(As) != 1: return False
    return True
def C_2e(s): # Lam(C_G) = Lam_j : j is the index of the A NOT meeting C_G? or meeting?
    for idx, CG, GG in hubs2(s):
        L = cls(CG, s.Lam); js = [j for j, m in enumerate(s.match) if m[3] <= L]
        Ai = [i for i in idx if s.match[i][0] & CG]
        if js and Ai and js[0] == Ai[0]: return False   # claim: j != the A meeting C_G
    return True
def C_2f(s): # the D in E_G met directly by the "free" A: is it D_{sigma}? i.e. A_j meets D_j?
    for idx, CG, GG in hubs2(s):
        E = GG & s.sd
        for j in idx:
            if not (s.match[j][0] & CG):
                ks = [k for k, m in enumerate(s.match) if m[3] <= E and m[3] & s.match[j][0]]
                if ks and ks[0] != j: return False
    return True
def C_2g(s): # pi(G) = G for 2-hubs?
    for idx, CG, GG in hubs2(s):
        ks = {k for k, m in enumerate(s.match) if m[3] <= GG}
        if ks != set(idx): return False
    return True
claims = {k[2:]: v for k, v in list(globals().items()) if k.startswith('C_')}
run(4, ['instQ4.pkl'], claims, 2); run(5, ['instQ5_0.pkl', 'instQ5_1.pkl'], claims, 2)
