import sys, time
sys.argv = ['x', sys.argv[1]]
exec(open('endstep.py').read().split("t0 = time.time()")[0])
t0 = time.time()
for gname in ['A', 'G2abc']:
    g = (gname, 'b'); cur = list(I12)
    assert run2(end, [(q, 'y') for q in cur], g)
    for nm in list(cur):
        trial = [q for q in cur if q != nm]
        if run2(end, [(q, 'y') for q in trial], g): cur = trial
    print(f"m={m}: minimal invariants of y for {gname}(b): {cur} ({time.time()-t0:.0f}s)", flush=True)
    # does 'y id' matter?
    print(f"      without y id: {run2(end[:-1], [(q, 'y') for q in cur], g)}")
