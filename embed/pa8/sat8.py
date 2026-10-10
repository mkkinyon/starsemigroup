"""SAT embedding search at level m for the order-8 candidates (post8.log records with embeds = None)."""
import json, sys, time, os
sys.path.insert(0, '/mnt/user-data/outputs/starsemigroup/embed')
from pa_sat import solve
m = int(sys.argv[1]); which = [int(a) for a in sys.argv[2:]]
recs = [json.loads(l) for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "post8.log"))]
cands = [r["A"] for r in recs if r["embeds"] is None]
for k in which or range(len(cands)):
    t = time.time(); r = solve(cands[k], m, verbose=False)
    print(f"candidate {k} (P_8^{k+1}): m = {m}: {'EMBEDS' if r else 'no embedding'} ({time.time()-t:.0f}s)", flush=True)
    if r: print("   ", r, flush=True)
