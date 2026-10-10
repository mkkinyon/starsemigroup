def iso(A, B):
    """isomorphism A -> B of binary tables (backtracking with incremental checks), or None"""
    n = len(A)
    if n != len(B): return None
    f = {}
    def ok():
        for u in f:
            for v in f:
                w = A[u][v]
                if w in f and B[f[u]][f[v]] != f[w]: return False
                if w not in f and B[f[u]][f[v]] in f.values(): return False
        return True
    def rec(i, used):
        if i == n: return dict(f)
        for y in range(n):
            if y in used: continue
            f[i] = y
            if ok():
                r = rec(i+1, used | {y})
                if r: return r
            del f[i]
        return None
    return rec(0, set())
