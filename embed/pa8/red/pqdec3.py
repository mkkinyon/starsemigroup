import sys, time, pickle
exec(open('pqdec2.py').read().split("Q2 = meetst")[0])
K1 = meetst('abc', 'by', 'bc'); U2 = meetst('ac', 'bcy', 'c'); K2 = meetst('bcy', 'ac', 'bc')
S, new = pickle.load(open('inv5_m4_K3.pkl', 'rb')); V3 = pickle.load(open('inv6_m5.pkl', 'rb'))
base = [('mt','a','c'), ('comm','y','b'), ('eq',('y','a'),('y','c'))]
def decomp(name, g, extra_excl=()):
    pool_ = [cl for cl in S + V3 if not trivially_implies(cl, g) and cl not in extra_excl]
    t0 = time.time(); ok = holds4(base, pool_, g)
    print(f"m={m}: {name} from base + {len(pool_)} clauses: {ok} ({time.time()-t0:.0f}s)", flush=True)
    if ok:
        cur = list(pool_)
        for cl in list(cur):
            trial = [c2 for c2 in cur if c2 != cl]
            if holds4(base, trial, g): cur = trial
        print(f"   minimal set ({len(cur)}):")
        for cl in cur: print('      ', fmt2(cl))
        return cur
    return None
decomp("K1 (abc)^(by) <= (bc)", K1)
decomp("U2 (ac)^(bcy) <= (c)", U2)
decomp("K2 (bcy)^(ac) <= (bc)", K2, extra_excl=[U2])
