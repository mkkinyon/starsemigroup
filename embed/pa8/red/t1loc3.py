import sys, pickle, time
sys.argv = ['x', sys.argv[1], '3']
exec(open('t1loc.py').read().split("def subsumed(")[0])
T1 = ((-1, ('J','a','b')), (-1, ('J3','x','b','c')), (1, ('J','b','c')))
S = pickle.load(open('t1loc_m4_K3.pkl', 'rb'))
for name, basew in (("a|><|c, x~b", [('mt','a','c'), ('comm','x','b')]), ("a|><|c, x~b, x~c (drop x id)", [('mt','a','c'), ('comm','x','b'), ('comm','x','c')]), ("a|><|c, x~b, x id (drop x~c)", [('mt','a','c'), ('comm','x','b'), idf('x')])):
    t0 = time.time(); ok = holds(basew, S, T1)
    print(f"m={m}: [{name}] + all local clauses => T1: {ok} ({time.time()-t0:.0f}s)", flush=True)
    if ok:
        cur = list(S)
        for cl in list(cur):
            trial = [c2 for c2 in cur if c2 != cl]
            if holds(basew, trial, T1): cur = trial
        print(f"   minimal set ({len(cur)}):")
        for cl in cur: print('      ', fmt(cl))
