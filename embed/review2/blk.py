"""Independent block calculus for projections of P_X (reviewer's code, not the project's).
A projection is (blocks, T) with blocks a frozenset of frozensets partitioning X and T a frozenset of the
transversal blocks.  theta_p(q) is computed from Lemma 1.1(a) directly (no partition-monoid product)."""
from itertools import combinations

def proj(blocks, tblocks):
    blocks = frozenset(frozenset(b) for b in blocks)
    T = frozenset(frozenset(b) for b in tblocks)
    assert T <= blocks
    return (blocks, T)

def join_classes(P1, P2):
    """classes of the join of two partitions (union-find)."""
    parent = {}
    def find(x):
        while parent.setdefault(x, x) != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for P in (P1, P2):
        for b in P:
            b = list(b)
            for y in b[1:]:
                parent[find(b[0])] = find(y)
    cl = {}
    for b in P1:
        for x in b:
            cl.setdefault(find(x), set()).add(x)
    return [frozenset(c) for c in cl.values()]

def theta(p, q):
    """theta_p(q) = p q p by Lemma 1.1(a): all N(p)-blocks, and U_K for classes K of eps_p v eps_q meeting supp p,
    U_K transversal iff K meets supp q."""
    (Bp, Tp), (Bq, Tq) = p, q
    suppp = frozenset().union(*Tp) if Tp else frozenset()
    suppq = frozenset().union(*Tq) if Tq else frozenset()
    blocks = set(b for b in Bp if b not in Tp)
    T = set()
    for K in join_classes(Bp, Bq):
        if K & suppp:
            U = frozenset().union(*[b for b in Tp if b <= K])
            blocks.add(U)
            if K & suppq: T.add(U)
    return (frozenset(blocks), frozenset(T))

def commute(p, q): return theta(p, q) == theta(q, p)
def matched(p, q): return theta(p, q) == p and theta(q, p) == q
def leq(q, p): return theta(p, q) == q   # q <= p
def rank(p): return len(p[1])

def all_projections(X):
    X = list(X)
    def parts(elems):
        if not elems:
            yield []; return
        first, rest = elems[0], elems[1:]
        for sm in parts(rest):
            for i in range(len(sm)):
                yield sm[:i] + [[first] + sm[i]] + sm[i+1:]
            yield [[first]] + sm
    out = []
    for sp in parts(X):
        k = len(sp)
        for mask in range(1 << k):
            out.append(proj(sp, [sp[t] for t in range(k) if mask >> t & 1]))
    return out

def show(p):
    (B, T) = p
    def s(b): return ' '.join(str(x) for x in sorted(b))
    return ''.join(('[%s]' if b in T else '(%s)') % s(b) for b in sorted(B, key=lambda b: min(b)))
