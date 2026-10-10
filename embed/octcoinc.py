"""Which coincidences among the vertices are forced in P_n for the 18-constraint
sub-configuration (and for the full relaxed octagon)?  Enumerate all solutions
allowing equal vertices, record the coincidence patterns."""
import sys, time
from collections import Counter
sys.argv = ["x", sys.argv[1] if len(sys.argv) > 1 else "5"]
src = open("octmin.py").read()
src = src[:src.index("cons = full_constraints()")]
exec(src)
for i in range(M):
    comm[i].add(i); mat[i].add(i)      # allow coincidences

def all_solutions(cons, limit=1200):
    vars_ = sorted({v for _, x, y in cons for v in (x, y)})
    rel = {}
    for kind, x, y in cons:
        rel.setdefault(x, []).append((y, kind)); rel.setdefault(y, []).append((x, kind))
    pats = Counter(); ex = {}
    t = time.time()
    def rec(env, remaining):
        if time.time() - t > limit: raise TimeoutError
        if not remaining:
            pat = tuple(sorted((u, v) for u in vars_ for v in vars_ if u < v and env[u] == env[v]))
            pats[pat] += 1; ex.setdefault(pat, dict(env)); return
        best = None
        for v in remaining:
            cand = None
            for (u, kind) in rel.get(v, []):
                if u in env:
                    s = (mat if kind == "M" else comm)[env[u]]
                    cand = s if cand is None else cand & s
            if cand is None:
                cand = set(reps) if not env else set(range(M))
            if best is None or len(cand) < len(best[1]): best = (v, cand)
        v, cand = best
        for p in cand:
            env[v] = p; rec(env, remaining - {v}); del env[v]
    try:
        rec({}, set(vars_))
    except TimeoutError:
        print("  (timeout; partial counts)")
    return pats, ex

cons = full_constraints()
sub = [c for c in cons if not (c[0] == "C" and c[1][0] == "a" and c[2][0] == "a" and (c[1], c[2]) != ("a2", "a4"))]
for name, cs in (("18-constraint sub-configuration", sub), ("full relaxed octagon", cons)):
    t = time.time()
    pats, ex = all_solutions(cs)
    print(f"{name}: {sum(pats.values())} solutions in P_{n} ({time.time()-t:.0f}s)")
    for pat, cnt in sorted(pats.items(), key=lambda kv: (len(kv[0]), -kv[1]))[:12]:
        print(f"   {cnt:7d}  ", " ".join(f"{u}={v}" for u, v in pat) or "all distinct")
