"""SAT verification in P(P_m) of path-closing hypothesis sets (pathclose3 atoms; two auxiliaries x, y; path p_0..p_n;
conclusion p_0 ~ p_n).  Elements 0..n = path, n+1 = x, n+2 = y, then fresh elements for products named in atoms.
Variables are NOT required to be distinct (full validity).  Returns True iff H => p_0 ~ p_n holds in P(P_m)."""
import sys, os
EMBED = os.environ.get("EMBED_DIR", "/mnt/user-data/outputs/starsemigroup/embed"); sys.path.insert(0, EMBED)
from pa_sat import solve

def table_for(H, n):
    """partial table (with fresh elements) encoding the path and the atoms H; returns (T, x, y)"""
    x, y = n + 1, n + 2; Z = {'x': x, 'y': y}
    cons = {}          # (a, b) -> value  meaning theta_b(a) = value, i.e. T[a][b] = value
    fresh = [n + 3]
    def new():
        fresh[0] += 1; return fresh[0] - 1
    def set_(a, b, v):
        if (a, b) in cons and cons[(a, b)] != v: raise ValueError("conflict")
        cons[(a, b)] = v
    for i in range(n):
        set_(i + 1, i, i); set_(i, i + 1, i + 1)          # p_i ~ p_{i+1}: theta_{p_i}(p_{i+1}) = p_i, theta_{p_{i+1}}(p_i) = p_{i+1}
    eqs = []
    def eq(t1, t2): eqs.append((t1, t2))
    for at in H:
        if at[0] == 'ch':
            a, b = at[1], at[2]; set_(b, a, a); set_(a, b, b)
        elif at[0] in ('x', 'y'):
            z, k = Z[at[0]], at[1]
            if k == 'comm': eq(('th', at[2], z), ('th', z, at[2]))
            elif k == 'zle': set_(z, at[2], z)
            elif k == 'lez': set_(at[2], z, at[2])
            elif k == 'sees': eq(('th', at[2], z), ('th', at[3], z))
            elif k == 'seen': eq(('th', z, at[2]), ('th', z, at[3]))
            elif k == 'zeq': set_(at[3], at[2], z)
        else:
            k = at[1]
            if k == 'comm': eq(('th', y, x), ('th', x, y))
            elif k == 'xley': set_(x, y, x)
            elif k == 'ylex': set_(y, x, y)
            else:
                i = at[2]
                if k == 'sees': eq(('th', i, x), ('th', i, y))
                elif k == 'xsees': eq(('th', i, x), ('th', at[3], y))
                elif k == 'xseen': eq(('th', x, i), ('th', y, at[3]))
                elif k == 'seen': eq(('th', x, i), ('th', y, i))
                elif k == 'x=th_y': set_(i, y, x)
                elif k == 'y=th_x': set_(i, x, y)
                elif k == 'x=th_p_y': set_(y, i, x)
                elif k == 'y=th_p_x': set_(x, i, y)
    # union-find over the product terms appearing in equalities
    parent = {}
    def find(t):
        parent.setdefault(t, t)
        while parent[t] != t: parent[t] = parent[parent[t]]; t = parent[t]
        return t
    for t1, t2 in eqs:
        a, b = find((t1[1], t1[2])), find((t2[1], t2[2]))
        if a != b: parent[a] = b
    classes = {}
    for t in list(parent): classes.setdefault(find(t), []).append(t)
    for cl in classes.values():
        named = {cons[t] for t in cl if t in cons}
        if len(named) > 1: raise ValueError("equality of two named elements")
        v = named.pop() if named else new()
        for t in cl: set_(t[0], t[1], v)
    N = fresh[0]; T = [[None] * N for _ in range(N)]
    for i in range(N): T[i][i] = i
    for (a, b), v in cons.items(): T[a][b] = v
    return T

def valid(H, n, m, verbose=False):
    T = table_for(H, n); N = len(T)
    for (a, b) in ((n, 0), (0, n)):      # negate theta_0(p_n) = p_0  /  theta_n(p_0) = p_n
        T2 = [row[:] + [None] for row in T] + [[None] * (N + 1)]
        for i in range(N + 1): T2[i][i] = i
        if T2[a][b] is not None: raise ValueError("conclusion already constrained")
        T2[a][b] = N
        if solve(T2, m, distinct=[(N, b)], verbose=verbose, symbreak=False) is not None: return False
    return True

if __name__ == "__main__":
    import json
    n, m = int(sys.argv[1]), int(sys.argv[2])
    Hs = json.load(open(sys.argv[3]))
    for H in Hs:
        H = [tuple(a) for a in H]
        print(valid(H, n, m), H, flush=True)

def valid_eq(H, n, m, t1, t2, verbose=False):
    """H => theta_{t1[1]}(t1[0]) = theta_{t2[1]}(t2[0])  (terms as (p, q) pairs of element indices: path 0..n, x = n+1, y = n+2)"""
    T = table_for(H, n); N = len(T)
    T2 = [row[:] + [None, None] for row in T] + [[None] * (N + 2), [None] * (N + 2)]
    for i in range(N + 2): T2[i][i] = i
    idx = []
    for j, (p, q) in enumerate((t1, t2)):
        if T2[p][q] is None: T2[p][q] = N + j
        idx.append(T2[p][q])
    return solve(T2, m, distinct=[(idx[0], idx[1])], verbose=verbose, symbreak=False) is None
