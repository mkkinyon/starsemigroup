"""Proof DAG for Lemma A at position 2: statements about y derivable from (statements about x, x~y, y id), and A(y) from statements about y.
Usage: python3 dag.py m"""
import sys, time, itertools
sys.argv = ['x', sys.argv[1]]
exec(open('lemA_dec.py').read().split("base1 = ")[0])
base1 = [('mt','a','c'), ('comm','x','c'), idf('x')]
step = [('mt','a','c'), idf('x'), ('comm','x','y'), idf('y')]
names = list(PRED)
valid1 = [nm for nm in names if run(base1, [], (nm, 'x'))]
base2 = base1 + [('comm','x','y'), idf('y')]
valid2 = [nm for nm in names if run(base2, [], (nm, 'y'))]
print(f"m={m}: valid at position 1: {len(valid1)}; valid at position 2 (for y): {valid2}", flush=True)
# 1. which y-statements (other than A) suffice for A(y) with only the base (a|><|c, y id)?  minimal subsets of size <= 3
basey = [('mt','a','c'), idf('y')]
t0 = time.time(); found = []
cands = [nm for nm in valid2 if nm not in ('A', 'ac_le_ap', 'cp_le_ap')]
for k in (1, 2, 3):
    for S in itertools.combinations(cands, k):
        if any(set(f) <= set(S) for f in found): continue
        if run(basey, [(q, 'y') for q in S], ('A', 'y')): found.append(S); print(f"   A(y) <= {S} (with a|><|c, y id) ({time.time()-t0:.0f}s)", flush=True)
    if found: break
# 2. for each y-statement P valid at position 2: minimal x-statement sets (size <= 2) that give P(y) with x~y, y id, x id
print("derivations of y-statements from x-statements (x~y, y id, x id, a|><|c):", flush=True)
for Pn in valid2:
    ok = run(step, [(q, 'x') for q in valid1], (Pn, 'y'))
    if not ok: print(f"   {Pn}(y): NOT derivable from all x-statements", flush=True); continue
    best = None
    for k in (0, 1, 2):
        for S in itertools.combinations(valid1, k):
            if run(step, [(q, 'x') for q in S], (Pn, 'y')): best = S; break
        if best is not None: break
    print(f"   {Pn}(y) <= {best if best is not None else 'needs >= 3 x-statements'}", flush=True)
