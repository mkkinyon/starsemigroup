from hq import *
def nohub(s): return all(CG not in s.Nd for idx, lab, AG, CG in s.groups)
def C_NH1(s):
    if not nohub(s): return True
    return all(s.match[i][2] <= cls(CG, s.Pi1) for idx, lab, AG, CG in s.groups for i in idx)
def C_NH2(s):
    if not nohub(s): return True
    return all(any(Z <= K for K in s.Pi1) for Z in s.B + s.Nb)
def C_NH3(s):
    if not nohub(s): return True
    return all(any(Z <= K for K in s.Pi1) for Z in s.Y + s.Ny)
def C_NH4(s): # no-hub: N(b)-blocks meeting supp c are inside Pi1-classes
    if not nohub(s): return True
    return all(any(Z <= K for K in s.Pi1) for Z in s.Nb if Z & s.sc)
def C_NH5(s): # no-hub: Delta_i inside Gamma_G(i)
    if not nohub(s): return True
    return all(cls(s.match[i][1], s.Delta) <= cls(CG, s.Pi1) for idx, lab, AG, CG in s.groups for i in idx)
def C_cnt(s): return not nohub(s)
claims = {k[2:]: v for k, v in list(globals().items()) if k.startswith('C_')}
run(4, ['instQ4.pkl'], claims, 2); run(5, ['instQ5_0.pkl', 'instQ5_1.pkl'], claims, 2)
