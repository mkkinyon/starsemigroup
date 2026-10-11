import sys, re
sys.path.insert(0, '/home/claude/pa8w/embed')
from pmon import projections, mul
n = 5; P = projections(n); memo = {}
def m_(p, q):
    k = (p, q)
    if k not in memo: memo[k] = mul(p, q, n)
    return memo[k]
th = lambda x, p: m_(m_(x, p), x); comm = lambda p, q: m_(p, q) == m_(q, p)
def parse(s): return [(set(int(p) for p in body.split()), 'T' if op == '[' else 'N') for op, body in re.findall(r'([\[\(])([^\]\)]*)[\]\)]', s)]
def emb(blocks):
    out = []
    for pts, k in blocks:
        if k == 'T': out.append(tuple(sorted(list(pts) + [p + n for p in pts])))
        else: out.append(tuple(sorted(pts))); out.append(tuple(sorted(p + n for p in pts)))
    return tuple(sorted(out))
def blocks(p):
    out = []
    for b in p:
        top = frozenset(i for i in b if i < n)
        if top: out.append((top, any(i >= n for i in b)))
    return out
show = lambda p: '  '.join(('[' if t else '(') + ' '.join(map(str, sorted(bl))) + (']' if t else ')') for bl, t in blocks(p))
a = emb(parse("(0 2) (1 3) [4]")); c = emb(parse("(0) (1) (2) [3 4]"))
ident = lambda p: th(p, a) == th(p, c)
I = [p for p in P if ident(p)]
E1 = [x for x in I if comm(x, c)]
E2 = [y for y in I if any(comm(x, y) for x in E1)]
print("E1:"); [print('   ', show(x)) for x in E1]
print("E2 \\ E1:"); [print('   ', show(y)) for y in E2 if y not in E1]
E3 = [z for z in I if any(comm(y, z) for y in E2)]
print("E3 \\ E2:"); [print('   ', show(z)) for z in E3 if z not in E2]
