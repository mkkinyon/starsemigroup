import sys, time
from pmon import Pn, projections
from digraph import clause, parse_clause, search
P = Pn(5); projs = projections(5)
op = lambda x, y: P.prod(y, x, y)
for name, (k, E) in {"k=3 path {12,23}": (3, [(1,2),(2,3)]), "k=3 2-cycle+spare {12,21}": (3, [(1,2),(2,1)]),
                     "k=3 star {12,21,13,31}": (3, [(1,2),(2,1),(1,3),(3,1)])}.items():
    t = time.time()
    res = search(parse_clause(clause(k, E)), projs, op, distinct=False, limit=30000)
    print(f"P_5  {name}: counterexamples = {res if res == 'timeout' else len(res)}  ({time.time()-t:.0f}s)", flush=True)
    if res and res != "timeout":
        e = res[0]; print("      ", {v: e[v] for v in sorted(e)}, flush=True)
