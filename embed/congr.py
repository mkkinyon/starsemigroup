"""*-congruences of small regular *-semigroups and tests on the quotients."""
import sys, time, itertools, pickle
from embed import PnData, find_embedding, check_embedding
from analyse import props
from enum_rss import is_rss

class UF:
    def __init__(self, n): self.p = list(range(n))
    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]; x = self.p[x]
        return x
    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b: return False
        self.p[a] = b; return True

def congruence_closure(T, star, pairs):
    n = len(T); uf = UF(n)
    queue = list(pairs)
    while queue:
        a, b = queue.pop()
        if uf.find(a) == uf.find(b): continue
        uf.union(a, b)
        queue.append((star[a], star[b]))
        for c in range(n):
            queue.append((T[a][c], T[b][c])); queue.append((T[c][a], T[c][b]))
    return tuple(uf.find(x) for x in range(n))

def canon_part(part):
    m = {}; out = []
    for x in part:
        if x not in m: m[x] = len(m)
        out.append(m[x])
    return tuple(out)

def all_congruences(T, star, maxcount=5000):
    n = len(T)
    principal = set()
    for a in range(n):
        for b in range(a + 1, n):
            principal.add(canon_part(congruence_closure(T, star, [(a, b)])))
    principal = list(principal)
    congs = set(principal); congs.add(tuple(range(n)))
    frontier = list(principal)
    while frontier and len(congs) < maxcount:
        new = []
        for c in frontier:
            for p in principal:
                # join: closure of pairs from both
                pairs = [(x, y) for x in range(n) for y in range(x+1, n) if c[x] == c[y] or p[x] == p[y]]
                j = canon_part(congruence_closure(T, star, pairs))
                if j not in congs:
                    congs.add(j); new.append(j)
        frontier = new
    return congs

def quotient(T, star, part):
    classes = sorted(set(part)); idx = {c: i for i, c in enumerate(classes)}
    rep = {}
    for x, c in enumerate(part):
        rep.setdefault(c, x)
    m = len(classes)
    Tq = [[idx[part[T[rep[classes[i]]][rep[classes[j]]]]] for j in range(m)] for i in range(m)]
    sq = [idx[part[star[rep[classes[i]]]]] for i in range(m)]
    return Tq, sq

if __name__ == "__main__":
    from pmon import partition_monoid, mul, star as pstar
    nmax = int(sys.argv[2]); n = int(sys.argv[1])
    elems = partition_monoid(n); idx = {e: i for i, e in enumerate(elems)}
    T = [[idx[mul(p, q, n)] for q in elems] for p in elems]
    st = [idx[pstar(p, n)] for p in elems]
    t = time.time(); congs = all_congruences(T, st)
    print(f"P_{n}: {len(congs)} *-congruences ({time.time()-t:.0f}s)")
    Ds = {k: PnData(k) for k in range(1, nmax + 1)}
    for c in sorted(congs, key=lambda c: -len(set(c))):
        Tq, sq = quotient(T, st, c)
        assert is_rss(Tq, sq)
        pr = props(Tq, sq)
        if len(Tq) == len(T): continue
        deg = None
        for k in range(1, nmax + 1):
            if find_embedding(Tq, sq, Ds[k]): deg = k; break
        print(f"  quotient of size {len(Tq)}: Q1={pr['Q1']} inverse={pr['inverse']} nP={pr['nP']} deg={deg}", flush=True)
