from hq import *
import pickle
def hubs2(s): return [(idx, CG, cls(CG, s.Pi1)) for idx, lab, AG, CG in s.groups if CG in s.Nd and len(idx) == 2]
stats = {}
def C_stat(s):
    for idx, CG, GG in hubs2(s):
        E = GG & s.sd
        i = next(i for i in idx if s.match[i][0] & CG); j = next(j for j in idx if j != i)
        Ai, Ci, Bi, Di = s.match[i]; Aj, Cj, Bj, Dj = s.match[j]
        key = ('E_G in Gamma_i(meets C_G)', E <= cls(Ai, s.Gamma), 'Aj∩Dj in supp b', bool(Aj & Dj & s.sb), 'Lam(C_G)=Lam_i', Ci <= cls(CG, s.Lam) or Di <= cls(CG, s.Lam),
               'Delta(E_G)=Delta_i', Ci <= cls(E, s.Delta), 'Ai∩C_G in supp b', bool(Ai & CG & s.sb), 'Bi meets C_G', bool(Bi & CG), 'Bj meets C_G', bool(Bj & CG), 'Bi meets E', bool(Bi & E), 'Bj meets E', bool(Bj & E),
               'Ai∩Di', bool(Ai & Di), 'Aj∩Di', bool(Aj & Di))
        stats[key] = stats.get(key, 0) + 1
    return True
claims = {'stat': C_stat}


