import sys, time
from pmon import Pn, projections
from digraph import clause, parse_clause, search
tests = {
  "k=3 {12,23} path": (3, [(1,2),(2,3)]),
  "k=3 {12,13} out-star": (3, [(1,2),(1,3)]),
  "k=3 {21,31} in-star": (3, [(2,1),(3,1)]),
  "k=3 {12,32}": (3, [(1,2),(3,2)]),
  "k=3 {12,31}": (3, [(1,2),(3,1)]),
  "k=4 {12,21} two isolated": (4, [(1,2),(2,1)]),
  "k=3 {12,21,33?} - no; k=3 {12,21} + (H2) only": (3, [(1,2),(2,1)]),
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
