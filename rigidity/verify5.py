"""
Two further questions:
 (a) Are all regular involutions of S conjugate under Aut(S)?  (i.e. is (S,*) determined
     up to isomorphism by the semigroup S?)
 (b) Are the natural involutions on small diagram monoids (Temperley-Lieb, Brauer,
     partition) the unique regular involutions?
"""
import itertools
from verify import find_inversions, is_semigroup, rees, cyclic_group, square_band
from verify3 import group_over_band

# ---------------------------------------------------------------------------
# automorphisms by backtracking with propagation
# ---------------------------------------------------------------------------
def find_automorphisms(mul):
    n = len(mul)
    # cheap invariants: idempotent?, |{x : x^2 = x}| etc. -> restrict images
    idem = [mul[x][x] == x for x in range(n)]
    left = [len(set(mul[x])) for x in range(n)]
    right = [len(set(mul[y][x] for y in range(n))) for x in range(n)]
    inv = lambda x: (idem[x], left[x], right[x])
    cand = [[y for y in range(n) if inv(y) == inv(x)] for x in range(n)]
    results = []

    def close(f):
        f = dict(f)
        used = set(f.values())
        queue = list(f.keys())
        while queue:
            x = queue.pop()
            for y in list(f.keys()):
                for a, b in ((x, y), (y, x)):
                    c = mul[a][b]
                    d = mul[f[a]][f[b]]
                    if c in f:
                        if f[c] != d:
                            return None
                    else:
                        if d in used or inv(c) != inv(d):
                            return None
                        f[c] = d
                        used.add(d)
                        queue.append(c)
        return f

    def rec(f):
        for x in range(n):
            if x not in f:
                break
        else:
            results.append([f[i] for i in range(n)])
            return
        used = set(f.values())
        for y in cand[x]:
            if y in used:
                continue
            new = close({**f, x: y})
            if new is not None:
                rec(new)

    rec({})
    for f in results:
        assert len(set(f)) == n and all(f[mul[a][b]] == mul[f[a]][f[b]] for a in range(n) for b in range(n))
    return results

def conjugacy_classes(mul, invs, auts):
    """orbits of Aut(S) on Inv(S) under psi . d = psi d psi^{-1}"""
    n = len(mul)
    key = lambda d: tuple(d)
    classes = []
    seen = set()
    for d in invs:
        if key(d) in seen:
            continue
        orb = set()
        for psi in auts:
            psi_inv = [0] * n
            for i, v in enumerate(psi):
                psi_inv[v] = i
            conj = [psi[d[psi_inv[x]]] for x in range(n)]
            orb.add(key(conj))
        seen |= orb
        classes.append(orb)
    return classes

# ---------------------------------------------------------------------------
# diagram monoids
# ---------------------------------------------------------------------------
def canon_partition(blocks):
    return tuple(sorted(tuple(sorted(b)) for b in blocks))

def partition_product(p, q, n):
    """p, q: partitions of {0..n-1} u {n..2n-1} (top/bottom). Product p*q: bottom of p glued to top of q."""
    parent = {}
    def find(x):
        while parent.setdefault(x, x) != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        parent[find(a)] = find(b)
    # nodes: ('t',i) top of p, ('m',i) middle, ('b',i) bottom of q
    for blk in p:
        nodes = [('t', i) if i < n else ('m', i - n) for i in blk]
        for a in nodes[1:]:
            union(nodes[0], a)
    for blk in q:
        nodes = [('m', i) if i < n else ('b', i - n) for i in blk]
        for a in nodes[1:]:
            union(nodes[0], a)
    comp = {}
    for i in range(n):
        comp.setdefault(find(('t', i)), []).append(i)
        comp.setdefault(find(('b', i)), []).append(n + i)
    return canon_partition(comp.values())

def all_partitions(elems):
    if not elems:
        yield []
        return
    first, rest = elems[0], elems[1:]
    for smaller in all_partitions(rest):
        for i in range(len(smaller)):
            yield smaller[:i] + [[first] + smaller[i]] + smaller[i + 1:]
        yield [[first]] + smaller

def partition_monoid(n):
    elems = [canon_partition(p) for p in all_partitions(list(range(2 * n)))]
    return elems

def matchings(points, partial=False):
    """perfect (or partial) matchings of a list of points, as lists of blocks"""
    if not points:
        yield []
        return
    first, rest = points[0], points[1:]
    if partial:
        for m in matchings(rest, True):
            yield [[first]] + m
    for k in range(len(rest)):
        for m in matchings(rest[:k] + rest[k + 1:], partial):
            yield [[first, rest[k]]] + m

def brauer_elems(n):
    return [canon_partition(m) for m in matchings(list(range(2 * n)))]

def motzkin_elems(n):
    return [canon_partition(m) for m in matchings(list(range(2 * n)), partial=True)]

def is_planar(p, n):
    # planar iff no two blocks cross when the 2n points are arranged on a circle:
    # order top 0..n-1 left to right, bottom n..2n-1 right to left
    pos = {i: i for i in range(n)}
    pos.update({n + i: 2 * n - 1 - i for i in range(n)})
    blocks = [sorted(pos[x] for x in b) for b in p]
    for b1 in blocks:
        for b2 in blocks:
            if b1 is b2:
                continue
            for a, c in itertools.combinations(b1, 2):
                if any(a < x < c for x in b2) and any(not (a < x < c) for x in b2):
                    return False
    return True

def diagram_table(elems, n):
    index = {e: i for i, e in enumerate(elems)}
    mul = [[index[partition_product(p, q, n)] for q in elems] for p in elems]
    return mul

def flip(p, n):
    return canon_partition([[(x + n) % (2 * n) for x in b] for b in p])

def diagram_monoid(kind, n):
    if kind == "partition":
        elems = partition_monoid(n)
    elif kind == "brauer":
        elems = brauer_elems(n)
    elif kind == "TL":
        elems = [p for p in brauer_elems(n) if is_planar(p, n)]
    elif kind == "motzkin":
        elems = [p for p in motzkin_elems(n) if is_planar(p, n)]
    mul = diagram_table(elems, n)
    assert is_semigroup(mul)
    star = [elems.index(flip(p, n)) for p in elems]
    return mul, star

if __name__ == "__main__":
    print("(a) conjugacy of regular involutions under Aut(S)")
    tests = []
    for m in (2, 3):
        tests.append((f"square band {m}x{m}", square_band(m)))
    Z3 = cyclic_group(3)
    P = [[0, 0, 0, 1], [0, 0, 1, 0], [0, 2, 0, 0], [2, 0, 0, 0]]
    tests.append(("M[Z3;4,4;P] non-orthodox", rees(Z3, range(4), P)))
    S3 = list(itertools.permutations(range(3)))
    for Hname, H in [("<(01)>", [(0, 1, 2), (1, 0, 2)]), ("<(012)>", [(0, 1, 2), (1, 2, 0), (2, 0, 1)])]:
        mul, _ = group_over_band(H, range(3))
        tests.append((f"H u (3x3 band), H={Hname}", mul))
    Z2 = cyclic_group(2)
    for name, mul in tests:
        invs = find_inversions(mul)
        auts = find_automorphisms(mul)
        cls = conjugacy_classes(mul, invs, auts)
        print(f"  {name}: |S|={len(mul)}, |Inv|={len(invs)}, |Aut|={len(auts)}, "
              f"Aut-orbits on Inv: {sorted(len(c) for c in cls)}")

    print("(b) diagram monoids")
    for kind, ns in [("TL", (2, 3, 4, 5, 6)), ("brauer", (2, 3, 4)), ("partition", (2, 3)), ("motzkin", (2, 3, 4))]:
        for n in ns:
            mul, star = diagram_monoid(kind, n)
            invs = find_inversions(mul)
            assert star in invs
            print(f"  {kind}_{n}: |S|={len(mul)}, regular involutions = {len(invs)}")
