from hq import *
def hubs(s): return [(idx, CG, cls(CG, s.Pi1)) for idx, lab, AG, CG in s.groups if CG in s.Nd]
def C_H1(s): # Lam(C_G) contains a T(d)-block, and it lies in E_G
    for idx, CG, GG in hubs(s):
        L = cls(CG, s.Lam); Ds = [D for D in s.D if D <= L]
        if len(Ds) != 1 or not Ds[0] <= GG: return False
    return True
def C_H2(s): # Delta(E_G) contains a T(c)-block, in C_G
    for idx, CG, GG in hubs(s):
        E = GG & s.sd
        if not E: return False
        Dl = cls(E, s.Delta); Cs = [C for C in s.C if C <= Dl]
        if len(Cs) != 1 or not Cs[0] <= CG: return False
    return True
def C_H3(s): # |pi(G)| = |G| (number of T(d) in E_G = |G|)
    return all(sum(1 for D in s.D if D <= (GG & s.sd)) == len(idx) for idx, CG, GG in hubs(s))
def C_H4(s): # the A_i meeting C_G (if any) is not the one whose D... : the B_i in Lam(C_G)? Delta(E_G)=Delta_i where A_i meets C_G?
    for idx, CG, GG in hubs(s):
        E = GG & s.sd; Dl = cls(E, s.Delta); i0 = [i for i in idx if s.match[i][1] <= Dl]
        Ai = [i for i in idx if s.match[i][0] & CG]
        if Ai and i0 and Ai != i0: return False
    return True
def C_H5(s): # 2-hub: the A meeting C_G is rho-connected to the D in Lam(C_G)
    for idx, CG, GG in hubs(s):
        L = cls(CG, s.Lam); Dk = next(D for D in s.D if D <= L)
        Ai = [i for i in idx if s.match[i][0] & CG]
        if Ai and not (Dk <= cls(s.match[Ai[0]][0], s.rho)): return False
    return True
def C_H6(s): # B_i meets C_G for the i with Delta(E_G) = Delta_i ?
    for idx, CG, GG in hubs(s):
        E = GG & s.sd; Dl = cls(E, s.Delta); i0 = [i for i in idx if s.match[i][1] <= Dl]
        if i0 and not (s.match[i0[0]][2] & CG): return False
    return True
def C_H7(s): # 1-hub: A_i meets C_G or E_G
    for idx, CG, GG in hubs(s):
        E = GG & s.sd
        for i in idx:
            if not (s.match[i][0] & (CG | E)): return False
    return True
claims = {k[2:]: v for k, v in list(globals().items()) if k.startswith('C_')}
run(4, ['instQ4.pkl'], claims, 3); run(5, ['instQ5_0.pkl', 'instQ5_1.pkl'], claims, 3)
