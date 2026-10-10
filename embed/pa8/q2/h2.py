from hq import *
from run6 import run_sampled
import pickle, sys
def comps(V):
    parent = list(range(len(V)))
    def find(i):
        while parent[i] != i: parent[i] = parent[parent[i]]; i = parent[i]
        return i
    for i in range(len(V)):
        for j in range(i):
            if V[i] & V[j]: parent[find(i)] = find(j)
    cc = {}
    for i in range(len(V)): cc.setdefault(find(i), []).append(V[i])
    return list(cc.values())
def hubs(s):
    return [(idx, CG, cls(CG, s.Pi1)) for idx, lab, AG, CG in s.groups if CG in s.Nd]
def nus(s, GG, CG):
    V = [F for F in s.Na if F <= GG] + [E for E in s.Nc if E in s.Nd and E <= GG] + [CG]
    return comps(V)
def attached(s, GG, CG, i):
    A = s.match[i][0]; Ds = [m for m, mt in enumerate(s.match) if mt[3] <= GG]
    att = set(m for m in Ds if s.match[m][3] & A)
    for nu in nus(s, GG, CG):
        if any(E & A for E in nu):
            for F in nu:
                if F in s.Na:
                    att |= set(m for m in Ds if s.match[m][3] & F)
    return att
def C_nonhub_ok(s):
    # every rho-class inside a non-hub class has exactly one A and one D
    for idx, lab, AG, CG in s.groups:
        if CG in s.Nd: continue
        GG = cls(CG, s.Pi1)
        for R in s.rho:
            if not R <= GG: continue
            nA = sum(1 for A in s.A if A <= R); nD = sum(1 for D in s.D if D <= R)
            if (nA, nD) not in [(0, 0), (1, 1)]: return False
    return True
def C_H1(s):
    for idx, CG, GG in hubs(s):
        for nu in nus(s, GG, CG):
            if sum(1 for i in idx if any(E & s.match[i][0] for E in nu)) > 1: return False
    return True
def C_H2(s):
    for idx, CG, GG in hubs(s):
        for nu in nus(s, GG, CG):
            Ds = set(m for m, mt in enumerate(s.match) if mt[3] <= GG and any(F & mt[3] for F in nu if F in s.Na))
            if len(Ds) > 1: return False
    return True
def C_H3(s):
    return all(len(attached(s, GG, CG, i)) <= 1 for idx, CG, GG in hubs(s) for i in idx)
def C_H4(s):
    return all(len(attached(s, GG, CG, i)) >= 1 for idx, CG, GG in hubs(s) for i in idx)
def C_H5(s):
    for idx, CG, GG in hubs(s):
        for m, mt in enumerate(s.match):
            if mt[3] <= GG and not (cls(mt[3], s.rho) & s.sa): return False
    return True
def C_size(s):
    return all(len(idx) <= 2 for idx, CG, GG in hubs(s))
def C_pi(s):
    for idx, CG, GG in hubs(s):
        if sum(1 for mt in s.match if mt[3] <= GG) != len(idx): return False
    return True
claims = {'nonhub_ok': C_nonhub_ok, 'H1': C_H1, 'H2': C_H2, 'H3': C_H3, 'H4': C_H4, 'H5': C_H5, 'size': C_size, 'pi': C_pi}
if __name__ == "__main__":
    run(4, ['instQ4.pkl'], claims, 3)
    run_sampled(5, ['instQ5_0.pkl', 'instQ5_1.pkl'], claims, 3, maxu=3, maxy=2)
    run_sampled(6, ['instQ6_0.pkl', 'instQ6_1.pkl', 'instQ6_2.pkl'], claims, 3, maxu=3, maxy=2)
