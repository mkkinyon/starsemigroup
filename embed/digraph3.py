import sys, time
from pmon import Pn, projections
from digraph import clause, parse_clause, search
tests = {
  "k=2 square {12,21}": (2, [(1,2),(2,1)]),
  "k=3 star at 1 {12,21,13,31}": (3, [(1,2),(2,1),(1,3),(3,1)]),
  "k=3 transitive tournament {12,23,13}": (3, [(1,2),(2,3),(1,3)]),
  "k=3 {12,21,23} (3 no out-edge)": (3, [(1,2),(2,1),(2,3)]),
  "k=3 {12,21} only (3 isolated)": (3, [(1,2),(2,1)]),
  "k=4 path {12,23,34}": (4, [(1,2),(2,3),(3,4)]),
  "k=3 single edge {12}": (3, [(1,2)]),
}
for n in (2, 3, 4):
    P = Pn(n); projs = projections(n)
    op = lambda x, y, P=P: P.prod(y, x, y)
    for name, (k, E) in tests.items():
        t = time.time()
        res = search(parse_clause(clause(k, E)), projs, op, distinct=False, limit=1500)
        print(f"P_{n}  {name}: counterexamples = {res if res == 'timeout' else len(res)}  ({time.time()-t:.0f}s)", flush=True)
        if res and res != "timeout":
            e = res[0]; print("      ", {v: e[v] for v in sorted(e)}, flush=True)
