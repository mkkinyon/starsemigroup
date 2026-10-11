import sys, pickle, time
sys.argv = ['x', sys.argv[1], '3']
exec(open('t1loc.py').read().split("def subsumed(")[0])
T1 = ((-1, ('J','a','b')), (-1, ('J3','x','b','c')), (1, ('J','b','c')))
S = pickle.load(open('t1loc_m4_K3.pkl', 'rb'))
t0 = time.time(); ok = holds(one, S, T1)
print(f"m={m}: T1 from the {len(S)} local clauses: {ok} ({time.time()-t0:.0f}s)", flush=True)
if ok:
    cur = list(S)
    for cl in list(cur):
        trial = [c2 for c2 in cur if c2 != cl]
        if holds(one, trial, T1): cur = trial
    print(f"minimal set ({len(cur)}):")
    for cl in cur: print('   ', fmt(cl))
    pickle.dump(cur, open(f't1loc_min_m{m}.pkl', 'wb'))
