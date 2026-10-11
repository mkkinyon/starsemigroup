"""Faster bitmask block calculus (reviewer's). projection = (blocks: tuple of int bitmasks sorted, T: bitmask of supp)."""
import itertools

def set_partitions(n):
    def parts(elems):
        if not elems:
            yield []; return
        first, rest = elems[0], elems[1:]
        for sm in parts(rest):
            for i in range(len(sm)):
                yield sm[:i] + [[first] + sm[i]] + sm[i+1:]
            yield [[first]] + sm
    return list(parts(list(range(n))))

def projections(n):
    out = []
    for sp in set_partitions(n):
        masks = [sum(1 << x for x in b) for b in sp]
        for mask in range(1 << len(sp)):
            T = sum(masks[t] for t in range(len(sp)) if mask >> t & 1)
            out.append((tuple(sorted(masks)), T))
    return out

def join(p, q):
    """classes of eps_p v eps_q as bitmasks."""
    Bp, Bq = p[0], q[0]
    cls = list(Bp)
    for b in Bq:
        merged = b; rest = []
        for c in cls:
            if c & b: merged |= c
            else: rest.append(c)
        rest.append(merged); cls = rest
    return cls

def theta(p, q):
    """theta_p(q), Lemma 1.1(a)."""
    Bp, Tp = p; Bq, Tq = q
    blocks = [b for b in Bp if not (b & Tp)]
    T = 0
    for K in join(p, q):
        if K & Tp:
            U = K & Tp
            blocks.append(U)
            if K & Tq: T |= U
    return (tuple(sorted(blocks)), T)

def commute(p, q):
    Bp, Tp = p; Bq, Tq = q
    sp = set(Bp); sq = set(Bq)
    for K in join(p, q):
        U = K & Tp; L = K & Tq
        if U and L:
            if U != K or L != K: return False
        elif U:
            if U != K or K not in sq: return False
        elif L:
            if L != K or K not in sp: return False
        else:
            if K not in sp or K not in sq: return False
    return True

def matched(p, q): return theta(p, q) == p and theta(q, p) == q

def show(p, n):
    Bp, Tp = p
    def s(b): return ' '.join(str(x) for x in range(n) if b >> x & 1)
    return ''.join(('[%s]' if b & Tp else '(%s)') % s(b) for b in sorted(Bp, key=lambda b: (b & -b)))

def parse(s, n):
    import re
    blocks = []; T = 0
    for kind, body in re.findall(r'([\(\[])([^\)\]]*)[\)\]]', s):
        b = sum(1 << int(t) for t in body.split()); blocks.append(b)
        if kind == '[': T |= b
    assert sum(blocks) == (1 << n) - 1, s
    return (tuple(sorted(blocks)), T)
