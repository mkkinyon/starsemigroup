import sys, time, itertools
sys.argv = ['x', sys.argv[1]]
exec(open('sigma.py').read().split("for nm in S:")[0])
base1 = [('mt','a','c'), ('comm','x','c'), idf('x')]
valid1 = [nm for nm in ['a_Gamma', 'A', 'M', "G2'", "G2'a", 'N1', 'N2', 'S', 'Cin', 'Nin', 'Tc_in_p', 'ac_le_ap', 'cp_le_ap', 'pAC', 'aCP', 'Cin_T', 'Nin_N', 'Nc_in_p', 'pT_in_c', 'pN_in_c', 'Np_cblock', 'cx_classes']]
t0 = time.time()
for goal in ['S13: c-block E, u outside supp y, v in supp y => joined in yva (A restricted)', 'S14: c-block E, u,v both outside supp y => joined in yva']:
    found = []
    for k in (1, 2, 3):
        for Sx in itertools.combinations(valid1, k):
            if any(set(f) <= set(Sx) for f in found): continue
            if run(step, [(q, 'x') for q in Sx], (goal, 'y')): found.append(Sx); print(f"m={m}: [{goal[:4]}] <= {Sx} ({time.time()-t0:.0f}s)", flush=True)
        if found: break
    # does it need x id / y id?
    if found:
        Sx = found[0]
        for drop in (1, 3):
            H = [h for i, h in enumerate(step) if i != drop]
            print(f"      without {step[drop]}: {run(H, [(q, 'x') for q in Sx], (goal, 'y'))}")
