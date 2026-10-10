"""Partition monoid P_n utilities.

A partition of {0,...,2n-1} (top points 0..n-1, bottom points n..2n-1) is stored as a
canonical tuple of sorted tuples.
"""
import itertools
from functools import lru_cache

def canon(blocks):
    return tuple(sorted(tuple(sorted(b)) for b in blocks))

def all_set_partitions(elems):
    if not elems:
        yield []
        return
    first, rest = elems[0], elems[1:]
    for smaller in all_set_partitions(rest):
        for i in range(len(smaller)):
            yield smaller[:i] + [[first] + smaller[i]] + smaller[i + 1:]
        yield [[first]] + smaller

def partition_monoid(n):
    return [canon(p) for p in all_set_partitions(list(range(2 * n)))]

def mul(p, q, n):
    """product p*q (p on top of q)."""
    parent = {}
    def find(x):
        while parent.setdefault(x, x) != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        parent[find(a)] = find(b)
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
    return canon(comp.values())

def star(p, n):
    return canon([[(x + n) % (2 * n) for x in b] for b in p])

def rank(p, n):
    return sum(1 for b in p if b[0] < n and b[-1] >= n)

def identity(n):
    return canon([[i, n + i] for i in range(n)])

def is_projection(p, n):
    return p == star(p, n) and mul(p, p, n) == p

def projections(n):
    """projections of P_n: pairs (set partition of {0..n-1}, subset of blocks transversal)."""
    res = []
    for sp in all_set_partitions(list(range(n))):
        k = len(sp)
        for mask in range(1 << k):
            blocks = []
            for t, b in enumerate(sp):
                if mask >> t & 1:
                    blocks.append(b + [n + x for x in b])
                else:
                    blocks.append(list(b))
                    blocks.append([n + x for x in b])
            res.append(canon(blocks))
    return res

class Pn:
    """P_n with memoised products."""
    def __init__(self, n):
        self.n = n
        self._mul = {}
    def mul(self, p, q):
        key = (p, q)
        r = self._mul.get(key)
        if r is None:
            r = mul(p, q, self.n)
            self._mul[key] = r
        return r
    def star(self, p):
        return star(p, self.n)
    def rank(self, p):
        return rank(p, self.n)
    def prod(self, *ps):
        r = ps[0]
        for q in ps[1:]:
            r = self.mul(r, q)
        return r
