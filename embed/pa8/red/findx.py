"""Given a, c, y in P_5 (counterexample to the last-link step), is there x in P_m (m = 5, 6, 7) with c~x~y and x identifying a with c?"""
import sys, time
sys.path.insert(0, '/home/claude/pa8w/embed')
from pmon import projections, mul
def emb(blocks, n0, n):   # blocks as [(set,kind)] over range(n0) -> pmon partition over n points (extra points singletons)
    out = []
    for pts, k in blocks:
        if k == 'T': out.append(tuple(sorted(list(pts) + [p + n for p in pts])))
        else: out.append(tuple(sorted(pts))); out.append(tuple(sorted(p + n for p in pts)))
    for p in range(n0, n): out += [(p,), (p + n,)]
    return tuple(sorted(out))
import re
def parse(s): return [(set(int(p) for p in body.split()), 'T' if op == '[' else 'N') for op, body in re.findall(r'([\[\(])([^\]\)]*)[\]\)]', s)]
A = parse("[0 2] [1 3] (4)"); C = parse("(0) (1) [2] [3 4]"); Y = parse("(0 1) [2 4] [3]"); B = parse("(0 1) [2] (3) [4]")
for n in (5, 6, 7):
    t = time.time(); P = projections(n); a, c, y, b = (emb(Z, 5, n) for Z in (A, C, Y, B))
    m = lambda p, q: mul(p, q, n); th = lambda x, p: m(m(x, p), x)
    found = [x for x in P if m(x, c) == m(c, x) and m(x, y) == m(y, x) and th(x, a) == th(x, c)]
    print(f"n={n}: {len(P)} projections, {len(found)} x with c~x~y, x id ({time.time()-t:.0f}s)", flush=True)
    for x in found[:3]: print('   x =', x)
