"""Independent randomised test of the hub-case lemma at the type level (union-find, no SAT):
random sets of kappa types and direct overlaps; whenever Gamma(a,c), Gamma(b,c), Gamma(b,d) are fine, check Gamma(a,d)."""
import random, itertools, sys
def components(edges, verts):
    par = {v: v for v in verts}
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for u, v in edges: par[f(u)] = f(v)
    return {v: f(v) for v in verts}
def fine(comp, Ta, Tc):
    for x, y in itertools.combinations(Ta, 2):
        if comp[x] == comp[y]: return False
    for x, y in itertools.combinations(Tc, 2):
        if comp[x] == comp[y]: return False
    for x in Ta:
        if not any(comp[x] == comp[y] for y in Tc): return False
    for y in Tc:
        if not any(comp[x] == comp[y] for x in Ta): return False
    return True
def test(p, mode, trials):
    A = [f"A{i}" for i in range(p)]; B = [f"B{i}" for i in range(p)]; C = [f"C{i}" for i in range(p)]; D = [f"D{i}" for i in range(p)]
    types = [(a, b, c, d) for a in A + [None] for b in B + [None] for c in C + [None] for d in D + [None]
             if (a, b, c, d) != (None,)*4 and not (mode == "B1" and (a is None) != (b is None))]
    aspec = A + B if mode == "B2" else [(a, b) for a in A for b in B]
    over_all = [(u, v) for u in aspec for v in C + D]
    def ablock(u, proj):
        if mode == "B2":
            if proj == "a": return u if u.startswith("A") else "Sb"
            return u if u.startswith("B") else "Sa"
        return u[0] if proj == "a" else u[1]
    def cblock(v, proj):
        if proj == "c": return v if v.startswith("C") else "Kp"
        return v if v.startswith("D") else "K"
    hits = 0
    for _ in range(trials):
        k = random.randint(1, 6); ts = random.sample(types, k); ov = [o for o in over_all if random.random() < 0.15]
        def graph(pa, pc):
            verts = set(); edges = []
            for u in aspec: verts.add(ablock(u, pa))
            for v in C + D: verts.add(cblock(v, pc))
            for i, t in enumerate(ts):
                node = f"k{i}"; verts.add(node)
                if mode == "B2":
                    if t[0]: edges.append((node, ablock(t[0], pa)))
                    if t[1]: edges.append((node, ablock(t[1], pa)))
                elif t[0]: edges.append((node, ablock((t[0], t[1]), pa)))
                if t[2]: edges.append((node, cblock(t[2], pc)))
                if t[3]: edges.append((node, cblock(t[3], pc)))
            for (u, v) in ov: edges.append((ablock(u, pa), cblock(v, pc)))
            return components(edges, verts)
        if fine(graph("a","c"), A, C) and fine(graph("b","c"), B, C) and fine(graph("b","d"), B, D):
            hits += 1
            if not fine(graph("a","d"), A, D):
                print("COUNTEREXAMPLE", p, mode, ts, ov); return
    print(f"p={p} {mode}: {hits} configurations with the hypotheses among {trials} samples, no counterexample")
random.seed(1)
for mode in ("B1", "B2"):
    for p in (1, 2, 3): test(p, mode, 300000)
