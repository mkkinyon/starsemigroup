"""Post-processing of the chunked order-7 enumeration (pa7/chunk_*.out: projection algebras with Q1 and (S)):
merge the chunks up to isomorphism, test the triangle condition (all instances, variables not necessarily distinct),
and test embeddability into P(P_m) by SAT (m up to MS).  Results: pa7_post.log (one JSON line per algebra) and a
summary.  Usage: python3 pa7_post.py [MS] [files...]"""
import sys, glob, json, os, itertools, time
from mace4parse import parse_models
from layered_search import canon
from graphsg import q1
from graphsg_survey import s_violations

def triangle_ok(A):
    """A[x][y] = theta_y(x) = y x y.  Returns True iff every triangle configuration has w = z."""
    N = len(A); th = lambda p, q: A[q][p]
    comm = [[th(x, y) == th(y, x) for y in range(N)] for x in range(N)]
    mt = [[th(x, y) == x and th(y, x) == y for y in range(N)] for x in range(N)]
    # commuting triples with a common pairwise product, grouped by that product
    triples = {}
    for a1, a2, a3 in itertools.product(range(N), repeat=3):
        if comm[a1][a2] and comm[a2][a3] and comm[a1][a3]:
            w = th(a1, a2)
            if th(a2, a3) == w and th(a1, a3) == w: triples.setdefault(w, []).append((a1, a2, a3))
    for w, ta in triples.items():
        for z, tb in triples.items():
            if z == w: continue
            for a1, a2, a3 in ta:
                for b1, b2, b3 in tb:
                    if comm[a1][b1] and comm[a2][b2] and comm[a3][b3] and mt[a1][b2] and mt[a2][b3] and mt[a3][b1]:
                        return False
    return True

if __name__ == "__main__":
    MS = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    files = sys.argv[2:] or sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pa7", "chunk_*.out")))
    seen = {}; order = []
    for f in files:
        for N, T, c in parse_models(open(f).read()):
            key = canon(T)
            if key not in seen: seen[key] = T; order.append(key)
    print(f"{len(files)} files, {len(seen)} algebras up to isomorphism", flush=True)
    LOG = "pa7_post.log"
    done = set()
    if os.path.exists(LOG):
        for l in open(LOG): done.add(tuple(map(tuple, json.loads(l)["A"])))
    from pa_sat import solve
    stats = dict(total=len(seen), q1=0, S=0, tri=0, emb=0, nonemb=0)
    for key in order:
        A = [list(r) for r in key]
        if key in done: continue
        assert q1(A) and s_violations(A) == 0
        stats["q1"] += 1; stats["S"] += 1
        tri = triangle_ok(A)
        if not tri: continue
        stats["tri"] += 1
        found = None; t0 = time.time()
        for m in range(1, MS + 1):
            if solve(A, m, verbose=False): found = m; break
        stats["emb" if found else "nonemb"] += 1
        rec = dict(A=A, embeds=found, secs=round(time.time() - t0, 1))
        with open(LOG, "a") as f: f.write(json.dumps(rec) + "\n")
        if not found: print("CANDIDATE (no embedding into P(P_m), m <= %d):" % MS, A, flush=True)
    print(stats)
