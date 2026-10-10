"""Analysis of a census file ord<n>.json (from extend.py): for each algebra test the triangle condition and
embeddability into P(P_m) (backtracking for m <= 4, SAT for m = 5..MS).  One JSON line per algebra in
post<n>.log (resumable: algebras already in the log are skipped).  Any CANDIDATE is a potential fifth obstruction.
Usage: python3 post8.py n [MS]"""
import sys, os, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); EMBED = os.environ.get("EMBED_DIR", os.path.dirname(HERE))
sys.path.insert(0, EMBED)
from pa7_post import triangle_ok
from pa_embed2 import PPm, embed
from pa_sat import solve

from layered_search import canon
from newconds import violated
n = int(sys.argv[1]); MS = int(sys.argv[2]) if len(sys.argv) > 2 else 7
PART = int(sys.argv[3]) if len(sys.argv) > 3 else 0; NPARTS = int(sys.argv[4]) if len(sys.argv) > 4 else 1   # indices i = PART mod NPARTS
MLIST = [5, 7] if MS == 7 else list(range(5, MS + 1))     # m = 6 is skipped: an UNSAT proof there is expensive and unneeded
algs = json.load(open(os.path.join(HERE, f"ord{n}.json")))
# known non-embeddable algebras of smaller order (from post<k>.log): an algebra containing one as a subalgebra is
# non-embeddable and not minimal; it is recorded with embeds = None, minimal = False and not tested further
known = set()
for k in range(2, n):
    f = os.path.join(HERE, f"post{k}.log")
    if os.path.exists(f):
        for l in open(f):
            r = json.loads(l)
            if r["embeds"] is None and r.get("minimal", True): known.add(canon(r["A"]))
def contains_known(A):
    N = len(A)
    for e in range(N):
        keep = [p for p in range(N) if p != e]
        if any(A[x][y] == e for x in keep for y in keep): continue
        pos = {p: i for i, p in enumerate(keep)}
        if canon([[pos[A[x][y]] for y in keep] for x in keep]) in known: return True
    return False
LOG = os.path.join(HERE, f"post{n}.log" if NPARTS == 1 else f"post{n}_{PART}.log")
done = set()
import glob
for f in glob.glob(os.path.join(HERE, f"post{n}.log")) + glob.glob(os.path.join(HERE, f"post{n}_*.log")):
    for l in open(f): done.add(tuple(map(tuple, json.loads(l)["A"])))
Ds = {}; stats = dict(total=len(algs), tri_fail=0, emb=0, nonemb=0); hist = {}
t0 = time.time()
for i, A in enumerate(algs):
    if i % NPARTS != PART or tuple(map(tuple, A)) in done: continue
    tri = triangle_ok(A); rec = dict(A=A, triangle=tri, embeds=None, minimal=True)
    viol = violated(A) if tri else None
    if tri and known and contains_known(A):
        rec["minimal"] = False; rec["violates"] = viol; stats["nonmin"] = stats.get("nonmin", 0) + 1
    elif tri and viol is not None:      # violates one of the quasi-identities of Section 5.8: non-embeddable, no SAT needed
        rec["violates"] = viol; stats["viol"] = stats.get("viol", 0) + 1
        print("VIOLATES", viol[0], A, flush=True)
    elif tri:
        found = None
        for m in range(1, 5):
            if m not in Ds: Ds[m] = PPm(m)
            r = embed(A, Ds[m], limit=30)
            if r == "timeout": break
            if r is not None: found = m; break
        if found is None:
            for m in MLIST:
                if solve(A, m, verbose=False): found = m; break
        rec["embeds"] = found; stats["emb" if found else "nonemb"] += 1; hist[found] = hist.get(found, 0) + 1
        if not found: print("CANDIDATE (no embedding into P(P_m), m <=", MS, "):", A, flush=True)
    else:
        stats["tri_fail"] += 1; print("TRIANGLE FAILS:", A, flush=True)
    with open(LOG, "a") as g: g.write(json.dumps(rec) + "\n")
    if (i + 1) % 200 == 0: print(f"{i+1}/{len(algs)} ({time.time()-t0:.0f}s) {stats} {hist}", flush=True)
print("done:", stats, hist)
