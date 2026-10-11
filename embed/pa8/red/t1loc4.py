import sys, pickle, time
sys.argv = ['x', sys.argv[1], '3']
exec(open('t1loc.py').read().split("def subsumed(")[0])
T1 = ((-1, ('J','a','b')), (-1, ('J3','x','b','c')), (1, ('J','b','c')))
S = pickle.load(open('t1loc_m4_K3.pkl', 'rb'))
bad = lambda cl: (1, ('J','b','c')) in cl and ((-1, ('J3','x','b','c')) in cl or (-1, ('J3','a','b','c')) in cl)
S2 = [cl for cl in S if not bad(cl)]
basew = [('mt','a','c'), ('comm','x','b')]
t0 = time.time(); ok = holds(basew, S2, T1)
print(f"m={m}: [a|><|c, x~b] + {len(S2)} local clauses (T1-like ones removed) => T1: {ok} ({time.time()-t0:.0f}s)", flush=True)
if ok:
    cur = list(S2)
    for cl in list(cur):
        trial = [c2 for c2 in cur if c2 != cl]
        if holds(basew, trial, T1): cur = trial
    print(f"   minimal set ({len(cur)}):")
    for cl in cur: print('      ', fmt(cl))
    pickle.dump(cur, open('t1loc_min.pkl', 'wb'))
