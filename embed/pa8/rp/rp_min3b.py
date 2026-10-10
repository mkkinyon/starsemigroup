import sys; sys.argv = ['x', '3']
exec(open('rp_min.py').read().split("for eq in EQS:")[0])
import time, itertools
for eq in [('yabya','ya'), ('byab','bxcb'), ('yaxc','xc'), ('bxb', 'bxcb')]:
    t0 = time.time()
    if not holds(eq, set(range(1, 7))): print(eq, "FAILS"); continue
    minimal = []
    for k in range(0, 7):
        for S in itertools.combinations(range(1, 7), k):
            if any(set(M) <= set(S) for M in minimal): continue
            if holds(eq, set(S)): minimal.append(S)
    print(eq, minimal, f"{time.time()-t0:.0f}s", flush=True)
