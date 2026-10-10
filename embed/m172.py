import sys, time, pickle
from mace4parse import parse_models
from pa_embed2 import PPm, embed
ms = list(parse_models(open('pa_6_partial.out').read()))
N, T, c = ms[172]
m = int(sys.argv[1])
t = time.time(); D = PPm(m); print(f"P(P_{m}): {D.N} projections, {len(D.reps)} orbits ({time.time()-t:.0f}s)", flush=True)
t = time.time(); r = embed(T, D, limit=20000)
print("result:", r, f"({time.time()-t:.0f}s)")
if r and r != "timeout":
    for i, v in enumerate(r): print(i, D.projs[v])
