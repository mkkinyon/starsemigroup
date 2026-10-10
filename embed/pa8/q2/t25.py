from hq import *
from run6 import run_sampled
def C_KL(s): # all N(b)-blocks in a Lambda-class containing a T(d)-block are N(y)-blocks
    for (A, C, B, D) in s.match:
        L = cls(D, s.Lam)
        if any(F <= L and F not in s.Ny for F in s.Nb): return False
    return True
def C_KD(s): # all N(b)-blocks in a Delta-class containing a T(c)-block are N(y)-blocks
    for (A, C, B, D) in s.match:
        Dl = cls(C, s.Delta)
        if any(F <= Dl and F not in s.Ny for F in s.Nb): return False
    return True
def C_agood(s): # N(y)-blocks are N(a)-blocks or unions of T(a)-blocks; and N(b) or unions of T(b)
    for Q in s.Ny:
        ga = Q in s.Na or (Q <= s.sa and all(A <= Q or not (A & Q) for A in s.A))
        gb = Q in s.Nb or (Q <= s.sb and all(B <= Q or not (B & Q) for B in s.B))
        if not (ga and gb): return False
    return True
def C_Ty(s): # T(y)-blocks meet supp c ∪ supp d only inside supp b
    return all((Y & (s.sc | s.sd)) <= s.sb for Y in s.Y)
claims = {k[2:]: v for k, v in list(globals().items()) if k.startswith('C_')}
run_sampled(5, ['instQ5_0.pkl', 'instQ5_1.pkl'], claims, 2, maxu=2, maxy=3)
run_sampled(6, ['instQ6_0.pkl', 'instQ6_1.pkl', 'instQ6_2.pkl'], claims, 2, maxu=2, maxy=3)
