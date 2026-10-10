import sys, time
from pmon import Pn, projections
from digraph import clause, parse_clause, search
n = 5
P = Pn(n); projs = projections(n)
op = lambda x, y: P.prod(y, x, y)
full = parse_clause(clause(3, [(1, 2), (2, 3), (3, 1)]))
tests = {
  "triangle, full": full,
  "triangle minus a1a3a1=w": [l for l in full if (l[0], l[1]) != ("x1 * x2", "x1 * x3")],
  "triangle minus a1b2a1=a1": [l for l in full if (l[0], l[1]) != ("y2 * x1", "x1")],
  "triangle minus b2b3b2=z": [l for l in full if (l[0], l[1]) != ("y1 * y2", "y2 * y3")],
}
for name, lits in tests.items():
    assert len(lits) == (14 if name == "triangle, full" else 13), (name, len(lits))
    t = time.time()
    res = search(lits, projs, op, distinct=False, limit=14000)
    print(f"P_5  {name}: counterexamples = {res if res == 'timeout' else len(res)}  ({time.time()-t:.0f}s)", flush=True)
    if res and res != "timeout":
        e = res[0]; print("    ", {v: e[v] for v in sorted(e)}, flush=True)
