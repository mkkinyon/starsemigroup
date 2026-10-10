"""Find minimal sub-configurations of the (relaxed) octagon that cannot be realized
by distinct projections in P_n.  Constraints: C = commute, M = matched (p q p = p, q p q = q)."""
import sys, time, itertools
from pmon import Pn, projections, canon, mul as rawmul

n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
P = Pn(n)
projs = projections(n)
pi = {p: i for i, p in enumerate(projs)}
M = len(projs)
t0 = time.time()
comm = [set() for _ in range(M)]; mat = [set() for _ in range(M)]
for i in range(M):
    for j in range(i + 1, M):
        pq = rawmul(projs[i], projs[j], n); qp = rawmul(projs[j], projs[i], n)
        if pq == qp:
            comm[i].add(j); comm[j].add(i)
        elif rawmul(pq, projs[i], n) == projs[i] and rawmul(qp, projs[j], n) == projs[j]:
            mat[i].add(j); mat[j].add(i)
print(f"P_{n}: {M} projections, relations computed ({time.time()-t0:.0f}s)", flush=True)

def act(perm, p):
    return canon([[perm[x] if x < n else n + perm[x - n] for x in blk] for blk in p])
perms = list(itertools.permutations(range(n)))
seen = set(); reps = []
for i, p in enumerate(projs):
    if i in seen: continue
    reps.append(i)
    for perm in perms:
        seen.add(pi[act(perm, p)])

V = ["a1", "a2", "a3", "a4", "b1", "b2", "b3", "b4"]
def full_constraints():
    cons = []
    for i in range(4):
        for j in range(i + 1, 4):
            cons.append(("C", f"a{i+1}", f"a{j+1}")); cons.append(("C", f"b{i+1}", f"b{j+1}"))
        cons.append(("C", f"a{i+1}", f"b{i+1}"))
        cons.append(("M", f"a{i+1}", f"b{(i+1)%4+1}")); cons.append(("M", f"a{i+1}", f"b{(i-1)%4+1}"))
    return cons

def realizable(cons, limit=60.0):
    """is there an assignment of distinct projections satisfying cons?  True/False/None(timeout)"""
    vars_ = sorted({v for _, x, y in cons for v in (x, y)})
    rel = {}
    for kind, x, y in cons:
        rel.setdefault(x, []).append((y, kind)); rel.setdefault(y, []).append((x, kind))
    t = time.time()
    def rec(env, remaining):
        if time.time() - t > limit:
            raise TimeoutError
        if not remaining:
            return True
        # choose the most constrained variable: smallest candidate set
        best = None
        for v in remaining:
            cand = None
            for (u, kind) in rel.get(v, []):
                if u in env:
                    s = (mat if kind == "M" else comm)[env[u]]
                    cand = s if cand is None else cand & s
            if cand is None:
                cand = set(reps) if not env else set(range(M))
            cand = cand - set(env.values())
            if best is None or len(cand) < len(best[1]):
                best = (v, cand)
        v, cand = best
        for p in cand:
            env[v] = p
            if rec(env, remaining - {v}):
                return True
            del env[v]
        return False
    try:
        return rec({}, set(vars_))
    except TimeoutError:
        return None

cons = full_constraints()
print("full relaxed octagon realizable:", realizable(cons))
# greedy minimisation: remove constraints while still unrealizable
cur = list(cons)
changed = True
while changed:
    changed = False
    for c in list(cur):
        trial = [d for d in cur if d != c]
        r = realizable(trial)
        if r is False:
            cur = trial; changed = True
            print(f"  dropped {c}: still unrealizable ({len(cur)} constraints left)", flush=True)
        elif r is None:
            print(f"  dropping {c}: timeout (kept)", flush=True)
print("minimal unrealizable sub-configuration:")
for c in cur: print("  ", c)
