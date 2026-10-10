"""Enumerate all regular *-semigroups of order n up to *-isomorphism, by backtracking
on the multiplication table with the involution fixed.

Output: list of (table, star) with table[x][y] and star[x].
"""
import sys, itertools, pickle, time

def involutions(n):
    """one representative permutation of order <=2 for each number of fixed points"""
    res = []
    for j in range(n, -1, -1):
        if (n - j) % 2:
            continue
        st = list(range(n))
        for t in range(j, n, 2):
            st[t], st[t + 1] = t + 1, t
        res.append(st)
    return res

def enumerate_rss(n, star, callback=None):
    """all regular *-semigroup tables on {0..n-1} with the given involution."""
    T = [[-1] * n for _ in range(n)]
    results = []
    # pairs (x,y) in an order; each assignment also sets (y*,x*)
    order = []
    done = set()
    def add(x, y):
        if (x, y) not in done:
            order.append((x, y)); done.add((x, y)); done.add((star[y], star[x]))
    for x in range(n):
        add(x, star[x])
    for x in range(n):
        for y in range(n):
            add(x, y)

    def assign(x, y, z, trail):
        """set T[x][y]=z and consequences; return False on contradiction."""
        stack = [(x, y, z)]
        while stack:
            a, b, c = stack.pop()
            cur = T[a][b]
            if cur == c:
                continue
            if cur != -1:
                return False
            T[a][b] = c
            trail.append((a, b))
            sb, sa, sc = star[b], star[a], star[c]
            if T[sb][sa] != sc:
                if T[sb][sa] != -1:
                    return False
                stack.append((sb, sa, sc))
            # regularity: (x x*) x = x
            if b == star[a]:
                stack.append((c, a, a))
            if a == star[b]:
                stack.append((b, c, b))
            # associativity involving the new entry (a,b)=c
            # (a b) d = a (b d)
            for d in range(n):
                bd = T[b][d]
                cd = T[c][d]
                if bd != -1:
                    abd = T[a][bd]
                    if cd != -1 and abd != -1 and cd != abd:
                        return False
                    if cd != -1 and abd == -1:
                        stack.append((a, bd, cd))
                    if cd == -1 and abd != -1:
                        stack.append((c, d, abd))
                # d (a b) = (d a) b
                da = T[d][a]
                dc = T[d][c]
                if da != -1:
                    dab = T[da][b]
                    if dc != -1 and dab != -1 and dc != dab:
                        return False
                    if dc != -1 and dab == -1:
                        stack.append((da, b, dc))
                    if dc == -1 and dab != -1:
                        stack.append((d, c, dab))
                # (d a) b where the new entry is (d a)?? covered when (d,a) was set.
                # a (b d) with new entry (b,d): covered when (b,d) set; but the new
                # entry may be the *inner* one: (x y)=c is inner in  (x y) d  [done above]
                # and in  d (x y) [done]. Also new entry as outer: (a b) with a = T[p][q]:
                # for p,q with T[p][q]=a: (p q) b = p (q b): T[a][b]=c vs T[p][T[q][b]]
                pass
            # outer-position checks: for p,q with T[p][q] == a: p(q b) must be c
            for p in range(n):
                for q in range(n):
                    if T[p][q] == a:
                        qb = T[q][b]
                        if qb != -1:
                            pqb = T[p][qb]
                            if pqb == -1:
                                stack.append((p, qb, c))
                            elif pqb != c:
                                return False
                    if T[p][q] == b:
                        ap = T[a][p]
                        if ap != -1:
                            apq = T[ap][q]
                            if apq == -1:
                                stack.append((ap, q, c))
                            elif apq != c:
                                return False
        return True

    def undo(trail, upto):
        while len(trail) > upto:
            a, b = trail.pop()
            T[a][b] = -1

    def rec(k):
        if k == len(order):
            if callback is None:
                results.append([row[:] for row in T])
            else:
                callback(T)
            return
        x, y = order[k]
        if T[x][y] != -1:
            rec(k + 1)
            return
        trail = []
        for z in range(n):
            mark = len(trail)
            if assign(x, y, z, trail):
                rec(k + 1)
            undo(trail, mark)

    rec(0)
    return results

def is_rss(T, star):
    n = len(T)
    for x in range(n):
        if star[star[x]] != x or T[T[x][star[x]]][x] != x:
            return False
        for y in range(n):
            if star[T[x][y]] != T[star[y]][star[x]]:
                return False
            for z in range(n):
                if T[T[x][y]][z] != T[x][T[y][z]]:
                    return False
    return True

def canonical(T, star):
    n = len(T)
    best = None
    for perm in itertools.permutations(range(n)):
        inv = [0] * n
        for i, v in enumerate(perm):
            inv[v] = i
        st = tuple(perm[star[inv[i]]] for i in range(n))
        tab = tuple(perm[T[inv[i]][inv[j]]] for i in range(n) for j in range(n))
        key = (st, tab)
        if best is None or key < best:
            best = key
    return best

def all_rss(n):
    found = {}
    for star in involutions(n):
        t = time.time()
        raw = enumerate_rss(n, star)
        for T in raw:
            assert is_rss(T, star)
            key = canonical(T, star)
            found.setdefault(key, (T, star))
        print(f"  n={n}, fixed points={sum(1 for i in range(n) if star[i]==i)}: {len(raw)} tables, "
              f"{len(found)} classes so far ({time.time()-t:.1f}s)", file=sys.stderr)
    return list(found.values())

if __name__ == "__main__":
    N = int(sys.argv[1])
    allres = {}
    for n in range(1, N + 1):
        allres[n] = all_rss(n)
        print(f"order {n}: {len(allres[n])} regular *-semigroups up to *-isomorphism")
    with open(f"rss_upto{N}.pkl", "wb") as f:
        pickle.dump(allres, f)

def refine_colors(T, star, rounds=3):
    n = len(T)
    col = [(star[x] == x, T[x][x] == x) for x in range(n)]
    for _ in range(rounds):
        new = []
        for x in range(n):
            row = tuple(sorted((col[y], col[T[x][y]], col[T[y][x]]) for y in range(n)))
            new.append((col[x], row))
        # relabel to small ints
        keys = sorted(set(new))
        idx = {k: i for i, k in enumerate(keys)}
        col2 = [idx[k] for k in new]
        if len(keys) == len(set(col)):
            return col2
        col = col2
    return col

def canonical_fast(T, star):
    n = len(T)
    col = refine_colors(T, star)
    classes = {}
    for x in range(n):
        classes.setdefault(col[x], []).append(x)
    # order classes by colour; permutations act within classes
    groups = [classes[c] for c in sorted(classes)]
    best = None
    for perms in itertools.product(*[itertools.permutations(g) for g in groups]):
        # element order: concatenation of permuted groups -> new labels 0..n-1
        inv = [x for g in perms for x in g]      # inv[newlabel] = old element
        perm = [0] * n
        for i, x in enumerate(inv):
            perm[x] = i
        st = tuple(perm[star[inv[i]]] for i in range(n))
        tab = tuple(perm[T[inv[i]][inv[j]]] for i in range(n) for j in range(n))
        key = (tuple(len(g) for g in groups), st, tab)
        if best is None or key < best:
            best = key
    return best

def all_rss_fast(n):
    found = {}
    for star in involutions(n):
        t = time.time()
        raw = enumerate_rss(n, star)
        for T in raw:
            key = canonical_fast(T, star)
            found.setdefault(key, (T, star))
        print(f"  n={n}, fixed points={sum(1 for i in range(n) if star[i]==i)}: {len(raw)} tables, "
              f"{len(found)} classes so far ({time.time()-t:.1f}s)", file=sys.stderr)
    return list(found.values())


def all_rss_stream(n, log=None):
    found = {}
    for star in involutions(n):
        t = time.time()
        cnt = [0]
        def cb(T, star=star):
            cnt[0] += 1
            key = canonical_fast(T, star)
            if key not in found:
                found[key] = ([row[:] for row in T], star)
            if log and cnt[0] % 200000 == 0:
                print(f"    ...{cnt[0]} tables, {len(found)} classes, {time.time()-t:.0f}s", file=log, flush=True)
        enumerate_rss(n, star, cb)
        if log:
            print(f"  n={n}, fixed points={sum(1 for i in range(n) if star[i]==i)}: {cnt[0]} tables, "
                  f"{len(found)} classes so far ({time.time()-t:.1f}s)", file=log, flush=True)
    return list(found.values())
