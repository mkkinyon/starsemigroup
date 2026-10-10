from hq import *
def C_Y7(s):  # every N(b)-block meeting supp c or supp d is an N(y)-block
    return all(F in s.Ny for F in s.Nb if F & (s.sc | s.sd))
def C_Y8(s):  # ... and is a union of T(a)-blocks or an N(a)-block
    return all(F in s.Na or (F <= s.sa and all(A <= F or not (A & F) for A in s.A)) for F in s.Nb if F & (s.sc | s.sd))
def C_Y8c(s): # every N(c)-block meeting supp y meets T(y)-blocks of only one Pi^b class
    for E in s.Nc:
        Qs = {cls(Y, s.Pb) for Y in s.Y if Y & E}
        if len(Qs) > 1: return False
    return True
def C_BiGT(s): # B_i inside Gamma_G for T-labelled G containing i
    return all(s.match[i][2] <= cls(CG, s.Pi1) for (idx, lab, AG, CG) in s.groups if lab for i in idx)
def C_BiGN(s): # B_i inside Gamma_G for N-labelled G containing i, when C_G <= supp d
    return all(s.match[i][2] <= cls(CG, s.Pi1) for (idx, lab, AG, CG) in s.groups if not lab and CG <= s.sd for i in idx)
def C_DeltaT(s): # Delta_i inside Gamma_G for T-labelled G
    return all(cls(s.match[i][1], s.Delta) <= cls(CG, s.Pi1) for (idx, lab, AG, CG) in s.groups if lab for i in idx)
def C_offdiag(s): # in T-lab Gamma_G: D_k ∩ C_m (k != m, both in G) lies in N(b)-blocks
    for (idx, lab, AG, CG) in s.groups:
        if not lab: continue
        for k in idx:
            for m in idx:
                if k != m and (s.match[k][3] & s.match[m][1] & s.sb): return False
    return True
def C_AiDk(s): # in T-lab Gamma_G: A_i ∩ D_k ⊆ C_i
    return all((s.match[i][0] & s.match[k][3]) <= s.match[i][1] for (idx, lab, AG, CG) in s.groups if lab for i in idx for k in idx)
def C_NaNb(s): # every N(a)-block meeting supp c ∪ supp d is an N(b)-block or a union of T(b)-blocks
    return all(F in s.Nb or (F <= s.sb and all(B <= F or not (B & F) for B in s.B)) for F in s.Na if F & (s.sc | s.sd))
def C_Ny_c(s): # every N(y)-block meeting supp c is an N(b)-block or a union of T(b)-blocks  [trivial from y~b]
    return all(F in s.Nb or (F <= s.sb and all(B <= F or not (B & F) for B in s.B)) for F in s.Ny if F & s.sc)
claims = {k[2:]: v for k, v in list(globals().items()) if k.startswith('C_')}
run(4, ['instQ4.pkl'], claims, 3); run(5, ['instQ5_0.pkl'], claims, 3)
