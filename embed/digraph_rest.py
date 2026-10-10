import sys, time
from pmon import Pn, projections
from digraph import clause, parse_clause, search, CONDS
for n, names in ((4, ["double 2-cycle (k=4)"]), (5, ["directed triangle (k=3)", "hexagon (k=3, all pairs)"])):
    P = Pn(n); projs = projections(n)
    op = lambda x, y, P=P: P.prod(y, x, y)
    for name in names:
        k, E = CONDS[name]
        t = time.time()
        res = search(parse_clause(clause(k, E)), projs, op, distinct=False, limit=20000)
        print(f"P_{n} ({len(projs)} proj.)  {name}: counterexamples = {res if res == 'timeout' else len(res)}  ({time.time()-t:.0f}s)", flush=True)
