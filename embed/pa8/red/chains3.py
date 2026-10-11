import sys, re
sys.path.insert(0, '/home/claude/pa8w/embed')
from pmon import projections, mul
n = 4; P = projections(n)
m_ = lambda p, q: mul(p, q, n); th = lambda x, p: m_(m_(x, p), x); comm = lambda p, q: m_(p, q) == m_(q, p)
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
show = lambda p: '  '.join(('[' if k == 'T' else '(') + ' '.join(map(str, sorted(bl))) + (']' if k == 'T' else ')') for bl, k in blocks(p))
a = topm(parse("[0] (1 2 3)")); c = topm(parse("[0] (1) (2 3)")); z = topm(parse("[0 1] (2) (3)"))
ident = [p for p in P if th(p, a) == th(p, c)]
E1 = [x for x in ident if comm(x, c)]
print("E1 (c~x, x id):"); [print('   ', show(x)) for x in E1]
E2 = [y for y in ident if any(comm(x, y) for x in E1)]
print("E2 size", len(E2), "; z in E2:", z in E2)
print("length-3 chains to z:")
for x in E1:
    for y in ident:
        if comm(x, y) and comm(y, z): print('   c ~', show(x), ' ~ ', show(y), ' ~ z')
