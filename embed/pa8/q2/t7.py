from hq import *
def C_K1(s): # T-lab G: A_i meets at most one D_k
    return all(sum(1 for k in idx if s.match[i][0] & s.match[k][3]) <= 1 for (idx, lab, AG, CG) in s.groups if lab for i in idx)
def C_K2(s): # T-lab G: A_i meets supp d
    return all(bool(s.match[i][0] & s.sd) for (idx, lab, AG, CG) in s.groups if lab for i in idx)
def C_K3(s): # any G: A_i meets at most one T(d)-block
    return all(sum(1 for D in s.D if s.match[i][0] & D) <= 1 for i in range(len(s.match)))
def C_K4(s): # N(a)-block meets at most one T(d)-block?
    return all(sum(1 for D in s.D if F & D) <= 1 for F in s.Na)
def C_K5(s): # N(a)-block inside supp c ∪ supp d ... meets at most one T(c)-block (true by a|><|c) and at most one T(d)
    return all(sum(1 for D in s.D if F & D) <= 1 for F in s.Na if F & s.sc)
def C_K6(s): # T(d)-block meets at most one T(a)-block
    return all(sum(1 for A in s.A if A & D) <= 1 for D in s.D)
def C_K7(s): # a-block meeting a T(d)-block D_k and a T(c)-block C_m: then ... (k==m?) 
    for blk in s.A + s.Na:
        ks = [k for k in range(len(s.match)) if blk & s.match[k][3]]; ms = [m for m in range(len(s.match)) if blk & s.match[m][1]]
        if ks and ms and set(ks) != set(ms): return False
    return True
claims = {k[2:]: v for k, v in list(globals().items()) if k.startswith('C_')}
run(4, ['instQ4.pkl'], claims, 3); run(5, ['instQ5_0.pkl'], claims, 3)
