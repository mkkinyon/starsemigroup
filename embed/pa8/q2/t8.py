from hq import *
def C_Ha(s): # hub C_G (N(d)-block) meets at most one T(a)-block
    return all(sum(1 for i in idx if s.match[i][0] & CG) <= 1 for (idx, lab, AG, CG) in s.groups if CG in s.Nd)
def C_Hb(s): # hub C_G: |G| <= 2 ?
    return all(len(idx) <= 2 for (idx, lab, AG, CG) in s.groups if CG in s.Nd)
def C_Hc(s): # hub C_G with nonempty trace E_G: |G| = number of T(d) in E_G (known) ; E_G meets at most one T(a)-block?
    return all(sum(1 for A in s.A if A & (cls(CG, s.Pi1) & s.sd)) <= 1 for (idx, lab, AG, CG) in s.groups if CG in s.Nd)
def C_Hd(s): # any N(d)-block meets at most one T(a)-block
    return all(sum(1 for A in s.A if A & E) <= 1 for E in s.Nd)
def C_He(s): # any N(a)-block meets at most one T(d)-block  (=K4, known) ; any N(c)-block meets at most one T(d)? no (E_G). any N(b)-block meets at most one T(a)?
    return all(sum(1 for A in s.A if A & F) <= 1 for F in s.Nb)
def C_Hf(s): # any N(b)-block meets at most one T(d)-block (true: b|><|d) ; any N(c)-block meets at most one T(a) (true). N(b) meets at most one T(c): true. 
    return all(sum(1 for D in s.D if D & F) <= 1 for F in s.Nb)
def C_Hg(s): # hub C_G: number of T(a)-blocks meeting C_G ... equals 1 exactly? 
    return all(sum(1 for i in idx if s.match[i][0] & CG) == 1 for (idx, lab, AG, CG) in s.groups if CG in s.Nd)
def C_Hh(s): # hub with |G|=2: the T(a)-block not meeting C_G meets E_G?
    for (idx, lab, AG, CG) in s.groups:
        if CG in s.Nd and len(idx) == 2:
            E = cls(CG, s.Pi1) & s.sd
            for i in idx:
                if not (s.match[i][0] & CG) and not (s.match[i][0] & E): return False
    return True
claims = {k[2:]: v for k, v in list(globals().items()) if k.startswith('C_')}
run(4, ['instQ4.pkl'], claims, 3); run(5, ['instQ5_0.pkl', 'instQ5_1.pkl'], claims, 3)
