import pickle, numpy as np
exec(open('search2.py').read().split("t0 = time.time()")[0])
def V(m):
    p = pack1(m); return valid_p(p[0], p[1], full=True)
def atoms(m): return [NAMES[i] for i in np.nonzero(m)[0]]
print("S_Q(x,y) valid:", V(SQ[('x','y')]), atoms(SQ[('x','y')]))
print("S_P1(x,x) valid:", V(SP[('x','x')]), atoms(SP[('x','x')]))
print("S_R'(accb,x,y) valid:", V(SR[('accb','x','y')]), atoms(SR[('accb','x','y')]))
# pairwise intersections
import itertools
def pair(D1, D2, name):
    n = 0; ex = None
    for k1, m1 in D1.items():
        for k2, m2 in D2.items():
            if V(m1 & m2): n += 1; ex = ex or (k1, k2, atoms(m1 & m2))
    print(name, "valid pairs:", n, ex)
pair(SQ, SP, "Q&P1"); pair(SQ, SR, "Q&R'"); pair(SP, SR, "P1&R'")
