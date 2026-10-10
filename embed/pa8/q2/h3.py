from hq import *
from run6 import run_sampled
def C_Pi1eq(s): return set(s.Pi1) == set(s.Pi1d)
def C_rho_meets_AG(s):
    for idx, lab, AG, CG in s.groups:
        GG = cls(CG, s.Pi1)
        for R in s.rho:
            if R <= GG and not (R & AG): return False
    return True
def C_rho_in_plain_noD(s):
    # rho-classes not inside any Gamma_G contain no T(d)
    GGs = [cls(CG, s.Pi1) for idx, lab, AG, CG in s.groups]
    for R in s.rho:
        if not any(R <= GG for GG in GGs) and any(D <= R for D in s.D): return False
    return True
claims = {'Pi1eq': C_Pi1eq, 'rho_meets_AG': C_rho_meets_AG, 'plain_noD': C_rho_in_plain_noD}
run(4, ['instQ4.pkl'], claims, 3)
run_sampled(5, ['instQ5_0.pkl', 'instQ5_1.pkl'], claims, 3, maxu=3, maxy=2)
