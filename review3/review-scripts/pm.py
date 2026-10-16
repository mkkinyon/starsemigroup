"""Independent partition-monoid arithmetic (reviewer, 16 Oct).  A partition of X u X' (X=[n], X'=[n,2n)) is
stored as a frozenset of frozensets.  Products by union-find on three layers.  Used only to validate fast.py."""
import sys, itertools
sys.path.insert(0, '/home/claude/pa8w/review3/code')
import fast

def mul(al, be, n):
    par = list(range(3 * n))
    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    def union(x, y):
        x, y = find(x), find(y)
        if x != y: par[x] = y
    for B in al:
        B = list(B)
        for p in B[1:]: union(B[0], p)          # upper of al in [0,n), lower of al in [n,2n) = middle
    for B in be:
        B = [(p + n) for p in B]               # upper of be in [n,2n) = middle, lower in [2n,3n)
        for p in B[1:]: union(B[0], p)
    comps = {}
    for x in list(range(n)) + list(range(2 * n, 3 * n)):
        comps.setdefault(find(x), set()).add(x)
    out = set()
    for comp in comps.values():
        out.add(frozenset((x if x < n else x - n) for x in comp))
    return frozenset(out)

def star(al, n):
    return frozenset(frozenset((x + n if x < n else x - n) for x in B) for B in al)

def proj_to_partition(p, n):
    blocks, T = p
    out = set()
    for b in blocks:
        pts = [x for x in range(n) if b >> x & 1]
        if b & T:
            out.add(frozenset(pts + [x + n for x in pts]))
        else:
            out.add(frozenset(pts)); out.add(frozenset(x + n for x in pts))
    return frozenset(out)

def partition_to_proj(al, n):
    blocks = []; T = 0
    for B in al:
        up = [x for x in B if x < n]; lo = [x - n for x in B if x >= n]
        if up and lo:
            assert sorted(up) == sorted(lo)
            m = sum(1 << x for x in up); blocks.append(m); T |= m
        elif up:
            blocks.append(sum(1 << x for x in up))
    return (tuple(sorted(blocks)), T)

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    P = fast.projections(n)
    PP = {p: proj_to_partition(p, n) for p in P}
    # every element of P is a projection
    for p in P:
        assert mul(PP[p], PP[p], n) == PP[p] and star(PP[p], n) == PP[p]
    bad = 0
    for p in P:
        for q in P:
            pq = mul(PP[p], PP[q], n)
            pqp = mul(pq, PP[p], n)
            if partition_to_proj(pqp, n) != fast.theta(p, q): bad += 1
            if (pq == mul(PP[q], PP[p], n)) != fast.commute(p, q): bad += 1
    print('P_%d: %d projections, %d pairs, %d discrepancies with fast.theta/commute' % (n, len(P), len(P) ** 2, bad))
