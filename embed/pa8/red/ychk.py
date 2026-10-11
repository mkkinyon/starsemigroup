import sys, re
sys.path.insert(0, '/home/claude/pa8w/embed')
from pmon import projections, mul
def parse(s): return [(set(int(p) for p in body.split()), 'T' if op == '[' else 'N') for op, body in re.findall(r'([\[\(])([^\]\)]*)[\]\)]', s)]
def emb(blocks, n):
    out = []
    for pts, k in blocks:
        if k == 'T': out.append(tuple(sorted(list(pts) + [p + n for p in pts])))
        else: out.append(tuple(sorted(pts))); out.append(tuple(sorted(p + n for p in pts)))
    used = set().union(*[pts for pts, k in blocks])
    for p in range(n):
        if p not in used: out += [(p,), (p + n,)]
    return tuple(sorted(out))
A = parse("(0 2) (1 3) [4]"); C = parse("(0) (1) (2) [3 4]"); Y = parse("[0 4] (1 2) [3]"); Z = parse("[0] (1 2) (3) [4]")
for n in (5, 6, 7):
    P = projections(n); a, c, y, z = (emb(B, n) for B in (A, C, Y, Z))
    m_ = lambda p, q: mul(p, q, n); th = lambda x, p: m_(m_(x, p), x); comm = lambda p, q: m_(p, q) == m_(q, p)
    ident = lambda p: th(p, a) == th(p, c)
    xs = [x for x in P if comm(x, c) and ident(x) and comm(x, y)]
    print(f"n={n}: y is a chain end (c~x~y): {len(xs)} witnesses x", flush=True)
    for x in xs[:3]: print('     x =', x)
    print(f"      y id {ident(y)}, z id {ident(z)}, y~z {comm(y, z)}")
