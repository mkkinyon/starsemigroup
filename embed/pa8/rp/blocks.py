"""Block-calculus helpers for projections of P_n (pmon format)."""
def top_blocks(p, n):
    """list of (frozenset of top points, transversal?)"""
    res = []
    for blk in p:
        top = frozenset(i for i in blk if i < n)
        if top: res.append((top, any(i >= n for i in blk)))
    return res
def supp(p, n): return frozenset().union(*[t for t, tr in top_blocks(p, n) if tr]) if any(tr for _, tr in top_blocks(p, n)) else frozenset()
def join_classes(ps, n):
    """classes of the join of the top partitions of the projections ps"""
    parent = list(range(n))
    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]; i = parent[i]
        return i
    for p in ps:
        for t, _ in top_blocks(p, n):
            t = sorted(t)
            for j in t[1:]: parent[find(j)] = find(t[0])
    cl = {}
    for i in range(n): cl.setdefault(find(i), set()).add(i)
    return [frozenset(c) for c in cl.values()]
