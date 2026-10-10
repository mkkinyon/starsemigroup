"""Layered graph semigroups.
Data: levels V_1, ..., V_L (disjoint finite sets), a reflexive symmetric relation |><| ("matched") on each level,
complete on the bottom level V_L, and descent maps bot: V_i -> V_{i+1}.
Elements: pairs (p, q) with p, q on the same level.  Product: (p,q)(r,s) = (bot^alpha p, bot^beta s) where
q, r are first brought to their common (lower) level and then descended together until they become matched.
(x,y)^* = (y,x).  Q(G, bot) is the case L = 2.  P9 (the 9-element algebra of the notes) is a 3-level example.
Functions: build(levels, matched, bot) -> (elems, T, st) tables; is_rss; proj_algebra (table A[x][y] = y x y)."""
import itertools, random
from graphsg import is_rss, q1

def build(levels, matched, bot):
    """levels: list of lists of element names (level 1 first); matched: set of frozensets {p,q} (p != q) of matched
    pairs on a common level (the bottom level is made complete automatically); bot: dict p -> element of next level."""
    lv = {p: i for i, L in enumerate(levels) for p in L}
    L = len(levels)
    M = set(matched) | {frozenset((p, q)) for p, q in itertools.combinations(levels[-1], 2)}
    def mt(p, q): return p == q or frozenset((p, q)) in M
    def descend(q, r):
        """returns (alpha, beta): numbers of bot-steps to apply to q's side and r's side"""
        a = b = 0
        while lv[q] < lv[r]: q = bot[q]; a += 1
        while lv[r] < lv[q]: r = bot[r]; b += 1
        while not mt(q, r): q = bot[q]; r = bot[r]; a += 1; b += 1
        return a, b
    def down(p, n):
        for _ in range(n): p = bot[p]
        return p
    elems = [(p, q) for Lv in levels for p in Lv for q in Lv]
    idx = {e: i for i, e in enumerate(elems)}
    T = []
    for (p, q) in elems:
        row = []
        for (r, s) in elems:
            a, b = descend(q, r)
            row.append(idx[(down(p, a), down(s, b))])
        T.append(row)
    st = [idx[(q, p)] for (p, q) in elems]
    return elems, T, st

def proj_algebra(elems, T, st):
    P = [i for i in range(len(elems)) if st[i] == i and T[i][i] == i]
    loc = {p: k for k, p in enumerate(P)}
    return P, [[loc[T[T[y][x]][y]] for y in P] for x in P]

def random_structure(sizes, edge_prob=0.5, rng=random):
    levels = [[f"{chr(97 + i)}{j}" for j in range(n)] for i, n in enumerate(sizes)]
    matched = set()
    for Lv in levels[:-1]:
        for p, q in itertools.combinations(Lv, 2):
            if rng.random() < edge_prob: matched.add(frozenset((p, q)))
    bot = {p: rng.choice(levels[i + 1]) for i in range(len(levels) - 1) for p in levels[i]}
    return levels, matched, bot

def bot_preserves(levels, matched, bot):
    """does p |><| q imply bot p |><| bot q (with the bottom level complete)?"""
    L = len(levels)
    M = set(matched) | {frozenset((p, q)) for p, q in itertools.combinations(levels[-1], 2)}
    for i, Lv in enumerate(levels[:-1]):
        for p, q in itertools.combinations(Lv, 2):
            if frozenset((p, q)) in M:
                bp, bq = bot[p], bot[q]
                if bp != bq and frozenset((bp, bq)) not in M: return False
    return True

if __name__ == "__main__":
    # P9 as a layered structure
    levels = [["a", "b", "c", "d"], ["m", "n", "k"], ["w", "z"]]
    matched = {frozenset(x) for x in [("a", "c"), ("b", "c"), ("b", "d"), ("m", "n"), ("m", "k")]}
    bot = dict(a="m", b="m", c="n", d="k", m="w", n="z", k="z")
    elems, T, st = build(levels, matched, bot)
    print("P9 structure:", len(elems), "elements, rss:", is_rss(T, st))
    P, A = proj_algebra(elems, T, st)
    names = [elems[p][0] for p in P]
    for i, p in enumerate(P): print("  theta_%s:" % names[i], " ".join(names[A[j][i]] for j in range(len(P))))
    # random test: associativity vs the condition "bot preserves matching"
    random.seed(1); stats = {}
    for trial in range(3000):
        sizes = [random.randint(1, 4), random.randint(1, 3), random.randint(1, 2)][: random.randint(2, 3)]
        levels, matched, bot = random_structure(sizes)
        elems, T, st = build(levels, matched, bot)
        key = (bot_preserves(levels, matched, bot), is_rss(T, st))
        stats[key] = stats.get(key, 0) + 1
        if key == (False, True) or key == (True, False):
            if stats[key] <= 3: print("  example", key, levels, sorted(map(tuple, matched)), bot)
    print("(bot preserves matching, is rss):", stats)
