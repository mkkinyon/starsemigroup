"""Second pass over the order-9 candidates (post9_*.log: embeds = None, minimal, no violated condition):
semilattices embed (partial identities on the join-irreducibles); the others are tested by SAT at m = 8 (and 9 if asked).
Usage: python3 pass2_9.py PART NPARTS [m ...]   -> pass2_9_PART.log (JSON lines)"""
import json, sys, os, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, '/mnt/user-data/outputs/starsemigroup/embed')
from pa_sat import solve
PART = int(sys.argv[1]); NPARTS = int(sys.argv[2]); ms = [int(a) for a in sys.argv[3:]] or [8]
recs = []
import glob
for f in sorted(glob.glob(os.path.join(HERE, 'post9_*.log'))): recs += [json.loads(l) for l in open(f)]
cands = [r["A"] for r in recs if r["embeds"] is None and r.get("minimal", True) and r.get("violates") is None]
LOG = os.path.join(HERE, f'pass2_9_{PART}.log')
done = set()
for f in glob.glob(os.path.join(HERE, 'pass2_9_*.log')):
    for l in open(f): done.add(tuple(map(tuple, json.loads(l)["A"])))
print(len(recs), "records,", len(cands), "candidates,", len(done), "already done", flush=True)
def load_done():
    d = set()
    for f in glob.glob(os.path.join(HERE, 'pass2_9_*.log')):
        for l in open(f): d.add(tuple(map(tuple, json.loads(l)["A"])))
    return d
for i, A in enumerate(cands):
    if i % NPARTS != PART or tuple(map(tuple, A)) in load_done(): continue
    N = len(A)
    if all(A[x][y] == A[y][x] for x in range(N) for y in range(N)):
        rec = dict(A=A, semilattice=True, embeds="semilattice")
    else:
        rec = dict(A=A, semilattice=False, embeds=None, tried=[])
        for m in ms:
            t = time.time(); r = solve(A, m, verbose=False); rec["tried"].append([m, round(time.time() - t)])
            if r: rec["embeds"] = m; break
        print("candidate:", "EMBEDS at m=%d" % rec["embeds"] if rec["embeds"] else "no embedding for m in %s" % ms, rec["tried"], A, flush=True)
    with open(LOG, "a") as g: g.write(json.dumps(rec) + "\n")
print("done")
