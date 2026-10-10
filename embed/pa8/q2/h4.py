from hq import *
from run6 import run_sampled
from h2 import comps, hubs, nus
def ntype_block(s, Z):
    Qs = [Q for Q in s.Nb if Q in s.Ny and Z <= Q]
    return Qs[0] if Qs else None
def lam(s, Q):
    L = cls(Q, s.Lam); ks = [k for k, m in enumerate(s.match) if m[3] <= L]
    return ks[0] if ks else None
def dl(s, Q):
    Dl = cls(Q, s.Delta); ks = [k for k, m in enumerate(s.match) if m[1] <= Dl]
    return ks[0] if ks else None
def hubinfo(s):
    """list of (idx, CG, GG, j, E, Gp, kprime)"""
    out = []
    for idx, CG, GG in hubs(s):
        j = lam(s, CG); E = GG & s.sd; Gp = [m for m, mt in enumerate(s.match) if mt[3] <= E]
        kp = dl(s, E) if E else None
        out.append((idx, CG, GG, j, E, Gp, kp))
    return out
def C_V3(s):
    # common block E meeting a b-type a-block at q not in supp b => lam(E), dl(E) undefined
    for E in s.Nc:
        if E not in s.Nd: continue
        for Z in s.A + s.Na:
            if ntype_block(s, Z) is not None: continue
            q = (E & Z) - s.sb
            if q and (lam(s, E) is not None or dl(s, E) is not None): return False
    return True
def C_V5(s):
    # N-type N(a)-block (or A_i) meeting C_G: its Q has lam = j and dl = index of the C_i met
    for idx, CG, GG, j, E, Gp, kp in hubinfo(s):
        for Z in s.A + s.Na:
            if not (Z & CG): continue
            Q = ntype_block(s, Z)
            if Q is None: continue
            if lam(s, Q) != j: return False
            for i in idx:
                if Z & s.match[i][1] and dl(s, Q) != i: return False
    return True
def C_V7(s):
    for k, (A, C, B, D) in enumerate(s.match):
        L = cls(D, s.Lam)
        for F in s.Nb:
            if F <= L and F not in s.Ny: return False
    return True
def C_V8(s):
    for idx, CG, GG, j, E, Gp, kp in hubinfo(s):
        for Z in s.A + s.Na:
            if ntype_block(s, Z) is not None: continue
            for i in idx:
                if (Z & s.match[i][1]) and not (Z & s.match[i][1] <= s.match[i][2]): return False
            for m in Gp:
                if (Z & s.match[m][3]) and not (Z & s.match[m][3] <= s.match[m][2]): return False
    return True
def C_V9(s):
    for idx, CG, GG, j, E, Gp, kp in hubinfo(s):
        for i in idx:
            A = s.match[i][0]
            if (A & CG) - s.sb and ntype_block(s, A) is None: return False
    return True
def C_V10(s):
    for idx, CG, GG, j, E, Gp, kp in hubinfo(s):
        if len(idx) == 2:
            k = next(i for i in idx if i != j)   # C_G <= Lambda_j, j = l; k the other
            if s.match[k][1] & s.sb: return False
            if s.match[j][3] & s.sb: return False   # D_l misses supp b
            if dl(s, s.match[k][3] | s.match[j][3]) != k: return False  # D_G <= Delta_k
    return True
def C_V4(s):
    # 2-hub G={k,l}: if a nu touching A_k contains C_G, or A_k meets C_G, then A_k is N-type with pair (l,k)
    for idx, CG, GG, j, E, Gp, kp in hubinfo(s):
        if len(idx) != 2: continue
        k = next(i for i in idx if i != j); A = s.match[k][0]
        linked = bool(A & CG) or any(CG in nu and any(X & A for X in nu) for nu in nus(s, GG, CG))
        if linked:
            Q = ntype_block(s, A)
            if Q is None or lam(s, Q) != j or dl(s, Q) != k: return False
    return True
claims = {'V3': C_V3, 'V4': C_V4, 'V5': C_V5, 'V7': C_V7, 'V8': C_V8, 'V9': C_V9, 'V10': C_V10}
if __name__ == "__main__":
    run(4, ['instQ4.pkl'], claims, 3)
    run_sampled(5, ['instQ5_0.pkl', 'instQ5_1.pkl'], claims, 3, maxu=3, maxy=2)
    run_sampled(6, ['instQ6_0.pkl', 'instQ6_1.pkl', 'instQ6_2.pkl'], claims, 3, maxu=3, maxy=2)
