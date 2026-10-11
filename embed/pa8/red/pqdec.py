import sys, time, pickle
exec(open('tind.py').read().split("Tyz = ")[0])
Q2 = meetst('cy', 'ab', 'bc'); P2 = meetst('acy', 'bcy', 'cy')
S, new = pickle.load(open('inv5_m4_K3.pkl', 'rb'))           # 100 local clauses over (y,a,c,b), valid under W2 (m<=5)
V3 = pickle.load(open('inv6_m5.pkl', 'rb'))                  # 54 J3-clauses valid under W2 at m=5
pool_ = [cl for cl in S + V3 if cl not in (Q2, P2)]
base = [('mt','a','c'), ('comm','y','b'), ('eq',('y','a'),('y','c'))]
for name, g in (("Q2", Q2), ("P2", P2)):
    t0 = time.time(); ok = holds4(base, pool_, g)
    print(f"m={m}: {name} from base(a|><|c, y~b, y id) + {len(pool_)} local clauses: {ok} ({time.time()-t0:.0f}s)", flush=True)
    if ok:
        cur = list(pool_)
        for cl in list(cur):
            trial = [c2 for c2 in cur if c2 != cl]
            if holds4(base, trial, g): cur = trial
        print(f"   minimal set ({len(cur)}):")
        for cl in cur: print('      ', fmt2(cl) if 'fmt2' in dir() else cl)
