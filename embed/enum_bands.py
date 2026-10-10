"""Enumerate *-bands (regular *-semigroups that are bands) with nontrivial involution."""
import sys, pickle, time
from enum_rss import involutions, canonical_fast, is_rss
import enum_rss

def enumerate_bands(n, star, callback):
    # reuse enumerate_rss machinery by pre-assigning x*x = x: simplest is to copy the code
    # with an initial assignment.  We monkeypatch by wrapping rec: assign diagonal first.
    T = [[-1] * n for _ in range(n)]
    results = []
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
    src = open("enum_rss.py").read()
    # extract assign/undo definitions by exec-ing enumerate_rss's inner code is messy; re-implement:
    def assign(x, y, z, trail):
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
            if b == star[a]:
                stack.append((c, a, a))
            if a == star[b]:
                stack.append((b, c, b))
            # band: (ab)(ab) = ab  -> T[c][c] = c
            if T[c][c] != c:
                if T[c][c] != -1:
                    return False
                stack.append((c, c, c))
            for d in range(n):
                bd = T[b][d]; cd = T[c][d]
                if bd != -1:
                    abd = T[a][bd]
                    if cd != -1 and abd != -1 and cd != abd:
                        return False
                    if cd != -1 and abd == -1:
                        stack.append((a, bd, cd))
                    if cd == -1 and abd != -1:
                        stack.append((c, d, abd))
                da = T[d][a]; dc = T[d][c]
                if da != -1:
                    dab = T[da][b]
                    if dc != -1 and dab != -1 and dc != dab:
                        return False
                    if dc != -1 and dab == -1:
                        stack.append((da, b, dc))
                    if dc == -1 and dab != -1:
                        stack.append((d, c, dab))
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
            a, b = trail.pop(); T[a][b] = -1
    def rec(k):
        if k == len(order):
            callback(T); return
        x, y = order[k]
        if T[x][y] != -1:
            rec(k + 1); return
        trail = []
        for z in range(n):
            mark = len(trail)
            if assign(x, y, z, trail):
                rec(k + 1)
            undo(trail, mark)
    trail = []
    for x in range(n):
        assert assign(x, x, x, trail)
    rec(0)

def all_bands(n, log=None):
    found = {}
    for star in involutions(n):
        if all(star[i] == i for i in range(n)):
            continue
        t = time.time(); cnt = [0]
        def cb(T, star=star):
            cnt[0] += 1
            key = canonical_fast(T, star)
            if key not in found:
                found[key] = ([row[:] for row in T], star)
        enumerate_bands(n, star, cb)
        if log:
            print(f"  n={n}, fixed={sum(1 for i in range(n) if star[i]==i)}: {cnt[0]} tables, {len(found)} classes ({time.time()-t:.1f}s)", file=log, flush=True)
    return list(found.values())

if __name__ == "__main__":
    N = int(sys.argv[1])
    res = {}
    for n in range(2, N + 1):
        res[n] = all_bands(n, sys.stdout)
        for T, star in res[n]:
            assert is_rss(T, star) and all(T[x][x] == x for x in range(n))
        print(f"order {n}: {len(res[n])} *-bands with nontrivial involution", flush=True)
        with open(f"bands_upto{N}.pkl", "wb") as f:
            pickle.dump(res, f)
