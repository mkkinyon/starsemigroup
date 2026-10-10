from hq import *
def C_sanity(s):   # Pi1 = eps_u v eps_c = eps_u v eps_d
    return set(s.Pi1) == set(s.Pi1d)
def C_CG(s):       # each C_G is an N(d)-block or subset of supp d; T-labelled => subset of supp d
    return all((CG in s.Nd) or (CG <= s.sd) for (_, lab, AG, CG) in s.groups) and all(CG <= s.sd for (_, lab, AG, CG) in s.groups if lab)
def C_plain(s):    # plain Pi1 classes (no T(a)) do not meet supp d
    return all(K & s.sd == frozenset() for K in s.Pi1 if not (K & s.sa))
def C_hubE(s):     # N-labelled G with C_G an N(d)-block: Gamma_G ∩ supp d is an N(c)-block or empty
    for (idx, lab, AG, CG) in s.groups:
        GG = cls(CG, s.Pi1)
        if CG in s.Nd:
            E = GG & s.sd
            if E and E not in s.Nc: return False
    return True
def C_Tgroup_D(s): # T-labelled G: number of T(d)-blocks inside C_G equals |G|
    return all(sum(1 for D in s.D if D <= CG) == len(idx) for (idx, lab, AG, CG) in s.groups if lab)
def C_Ngroup_D(s): # N-labelled G: number of T(d)-blocks inside Gamma_G equals |G|
    return all(sum(1 for D in s.D if D <= cls(CG, s.Pi1)) == len(idx) for (idx, lab, AG, CG) in s.groups if not lab)
def C_Tgroup_single(s): # T-labelled G has |G| = 1 ?
    return all(len(idx) == 1 for (idx, lab, AG, CG) in s.groups if lab)
def C_Ngroup_single(s):
    return all(len(idx) == 1 for (idx, lab, AG, CG) in s.groups if not lab)
def C_sigma(s):    # rho-matching equals sigma
    return all(Di <= cls(Ai, s.rho) for (Ai, Ci, Bi, Di) in s.match)
def C_sigma_T(s):  # in T-labelled groups, rho-matching is sigma
    return all(Di <= cls(Ai, s.rho) for (idx, lab, AG, CG) in s.groups if lab for i in idx for (Ai, Ci, Bi, Di) in [s.match[i]])
def C_Bi_in_GammaG(s): # B_i inside Gamma_G for i in G
    return all(s.match[i][2] <= cls(CG, s.Pi1) for (idx, lab, AG, CG) in s.groups for i in idx)
claims = {k[2:]: v for k, v in list(globals().items()) if k.startswith('C_')}
run(4, ['instQ4.pkl'], claims); run(5, ['instQ5_0.pkl', 'instQ5_1.pkl'], claims)
