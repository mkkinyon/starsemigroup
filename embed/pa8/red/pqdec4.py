import sys, time, pickle
exec(open('pqdec3.py').read().split('decomp("K1')[0])
T2 = meetst('ab', 'bcy', 'bc')
pool_ = [cl for cl in S + V3 if (1, ('J','b','c')) not in cl]
print(f"m={m}: T2 from base + {len(pool_)} clauses without +J(bc): {holds4(base, pool_, T2)}")
pool2 = [cl for cl in S + V3 if (1, ('J','b','c')) not in cl or not any(a[0] in ('J','J3') and 'y' in a[1:] and s < 0 for s, a in cl)]
print(f"m={m}: T2 from base + {len(pool2)} clauses (no clause '+J(bc) with negative y-join'): {holds4(base, pool2, T2)}")
if holds4(base, pool2, T2):
    cur = list(pool2)
    for cl in list(cur):
        trial = [c2 for c2 in cur if c2 != cl]
        if holds4(base, trial, T2): cur = trial
    for cl in cur: print('      ', fmt2(cl))
