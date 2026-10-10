"""For each order-8 candidate and each conclusion (p ~ q for non-matched pairs; p <= q for non-comparable pairs where
the full diagram implies it at m=4), compute a greedy-minimal hypothesis set valid at m=5.  Output qi_all.jsonl"""
import sys, os, json, time, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qi_extract import minimise, valid, fails_in, fmt
cands = json.load(open("cand9.json"))
which = [int(a) for a in sys.argv[1:]] or range(len(cands)); MAXR = 2
out = open("qi_all9.jsonl", "a")
for ci in which:
    C = cands[ci]; k = len(C)
    th = lambda p, q: C[q][p]
    Hfull = {(x, y): C[x][y] for x in range(k) for y in range(k) if x != y}
    concls = []
    for p, q in itertools.combinations(range(k), 2):
        if not (th(p, q) == p and th(q, p) == q): concls.append(('mt', p, q))
    for p, q in itertools.permutations(range(k), 2):
        if th(q, p) != p and th(p, q) != q: concls.append(('le', p, q))
    nres = 0
    for concl in concls:
        if nres >= MAXR: break
        if not valid(k, Hfull, concl, 4): continue
        nres += 1
        t = time.time()
        H = minimise(C, concl, 5, verbose=False)
        rec = dict(cand=ci, concl=concl, H=[[list(a), v] for a, v in H.items()], n=len(H), secs=round(time.time() - t))
        out.write(json.dumps(rec) + "\n"); out.flush()
        print(ci, len(H), fmt(H, concl), f"({rec['secs']}s)", flush=True)
