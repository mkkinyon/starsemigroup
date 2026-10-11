"""For a given (a, c) in P_5: the set of chain ends y (c~x~y, both identifying) versus the set of y satisfying the local invariants I12 (+ y id).
Prints the y's that satisfy I12 but are not chain ends."""
import sys, re, itertools
sys.path.insert(0, '/home/claude/pa8w/embed')
from pmon import projections, mul
n = 5; P = projections(n); memo = {}
def m_(p, q):
    k = (p, q)
    if k not in memo: memo[k] = mul(p, q, n)
    return memo[k]
th = lambda x, p: m_(m_(x, p), x); comm = lambda p, q: m_(p, q) == m_(q, p)
def parse(s): return [(set(int(p) for p in body.split()), 'T' if op == '[' else 'N') for op, body in re.findall(r'([\[\(])([^\]\)]*)[\]\)]', s)]
def topm(blocks):
    out = []
    for pts, k in blocks:
        if k == 'T': out.append(tuple(sorted(list(pts) + [p + n for p in pts])))
        else: out.append(tuple(sorted(pts))); out.append(tuple(sorted(p + n for p in pts)))
    return tuple(sorted(out))
def blocks(p):
    out = []
    for b in p:
        top = {i for i in b if i < n}
        if top: out.append((top, 'T' if any(i >= n for i in b) else 'N'))
    return out
def show(p): return '  '.join(('[' if k == 'T' else '(') + ' '.join(map(str, sorted(bl))) + (']' if k == 'T' else ')') for bl, k in blocks(p))
def part(p): return [bl for bl, k in blocks(p)]
def supp(p): return set().union(*[bl for bl, k in blocks(p) if k == 'T']) if any(k == 'T' for _, k in blocks(p)) else set()
def joinf(parts):
    parent = {u: u for u in range(n)}
    def f(u):
        while parent[u] != u: u = parent[u]
        return u
    for Pp in parts:
        for bl in Pp:
            bl = sorted(bl)
            for q in bl[1:]: parent[f(q)] = f(bl[0])
    return lambda u, v: f(u) == f(v)
def I12(y, a, c):
    """the twelve local invariants for y relative to (a, c), evaluated directly"""
    Ea, Ec, Ey = joinf([part(a)]), joinf([part(c)]), joinf([part(y)])
    Jac, Jay, Jcy, J3 = joinf([part(a), part(c)]), joinf([part(a), part(y)]), joinf([part(c), part(y)]), joinf([part(a), part(c), part(y)])
    Sa, Sc, Sy = supp(a), supp(c), supp(y)
    X = range(n)
    for u in X:
        for v in X:
            if u == v: continue
            if Ec(u, v) and not Jay(u, v): return 'A'
            if Jac(u, v) and Jcy(u, v) and not Ec(u, v): return 'M'
            if J3(u, v) and u in Sc and v in Sc and not Jcy(u, v): return "G2'"
            if J3(u, v) and u in Sa and v in Sa and not Jay(u, v): return "G2'a"
            if Ey(u, v) and u not in Sy and u in Sa and u not in Sc and not Jac(u, v): return 'N1'
            if Ey(u, v) and u not in Sy and u in Sa and u not in Sc and v not in Sc and not Ec(u, v): return 'N2'
            if u in Sy and u in Sa and u not in Sc: return 'S'
            if Jac(u, v) and not Jay(u, v): return 'ac_le_ap'
            if Jcy(u, v) and not Jay(u, v): return 'cp_le_ap'
            if Ey(u, v) and Jac(u, v) and not Ec(u, v): return 'pAC'
            if Ea(u, v) and Jcy(u, v) and not Ec(u, v): return 'aCP'
            for w in X:
                if Ec(u, v) and u not in Sc and w in Sa and Jac(u, w) and not Ey(u, v): return 'a_Gamma'
    return None
def analyse(a, c):
    ident = lambda p: th(p, a) == th(p, c)
    Xs = [x for x in P if comm(x, c) and ident(x)]
    ends = set()
    for x in Xs:
        for y in P:
            if ident(y) and comm(x, y): ends.add(y)
    loc = [y for y in P if ident(y) and I12(y, a, c) is None]
    extra = [y for y in loc if y not in ends]
    print(f"a = {show(a)};  c = {show(c)}:  chain ends {len(ends)}, I12-satisfying identifying y: {len(loc)}, not chain ends: {len(extra)}")
    return extra
if __name__ == '__main__':
    a = topm(parse("(0 2) (1 3) [4]")); c = topm(parse("(0) (1) (2) [3 4]"))
    extra = analyse(a, c)
    for y in extra[:20]: print('   y =', show(y))
