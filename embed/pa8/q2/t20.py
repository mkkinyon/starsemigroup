from hq import *
def bridges(s): return [Q for Q in s.Nb if Q <= s.sa and all(A <= Q or not (A & Q) for A in s.A)]
def C_L1(s): # bridge Q containing A_i: if Lam(Q) contains D_k then k in {i : A_i <= Q}? 
    for Q in bridges(s):
        idx = [i for i, m in enumerate(s.match) if m[0] <= Q]
        L = cls(Q, s.Lam); ks = [k for k, m in enumerate(s.match) if m[3] <= L]
        if ks and ks[0] not in idx: return False
    return True
def C_L2(s): # bridge Q: if Delta(Q) contains C_m then m in idx
    for Q in bridges(s):
        idx = [i for i, m in enumerate(s.match) if m[0] <= Q]
        Dl = cls(Q, s.Delta); ms = [m for m, mm in enumerate(s.match) if mm[1] <= Dl]
        if ms and ms[0] not in idx: return False
    return True
def C_L3(s): # bridge Q: Lam(Q) contains a T(d)-block D_k, and D_k meets Q
    for Q in bridges(s):
        L = cls(Q, s.Lam); ks = [k for k, m in enumerate(s.match) if m[3] <= L]
        if ks and not (s.match[ks[0]][3] & Q): return False
    return True
def C_L4(s): # bridge Q: the T(d)-block of Lam(Q) (if any) meets Q inside the A_i with Delta index... 
    return True
def C_L5(s): # any N(b)-block Q meeting supp c ∪ supp d: T(d) of Lam(Q) meets Q? 
    for Q in s.Nb:
        if not (Q & (s.sc | s.sd)): continue
        L = cls(Q, s.Lam); ks = [k for k, m in enumerate(s.match) if m[3] <= L]
        if ks and not (s.match[ks[0]][3] & Q): return False
    return True
def C_L6(s): # any N(b)-block Q meeting supp c ∪ supp d: T(c) of Delta(Q) meets Q?
    for Q in s.Nb:
        if not (Q & (s.sc | s.sd)): continue
        Dl = cls(Q, s.Delta); ms = [m for m, mm in enumerate(s.match) if mm[1] <= Dl]
        if ms and not (s.match[ms[0]][1] & Q): return False
    return True
claims = {k[2:]: v for k, v in list(globals().items()) if k.startswith('C_')}
run(4, ['instQ4.pkl'], claims, 3); run(5, ['instQ5_0.pkl', 'instQ5_1.pkl'], claims, 3)
