"""Which hypotheses of the directed-triangle condition are needed (relative to P_n)?
Drop each hypothesis literal in turn and search for counterexamples."""
import sys, time
from pmon import Pn, projections
from digraph import clause, parse_clause, search

n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
P = Pn(n); projs = projections(n)
op = lambda x, y: P.prod(y, x, y)
lits = parse_clause(clause(3, [(1, 2), (2, 3), (3, 1)]))
hyps = [l for l in lits if l[2]]
print(f"P_{n}: {len(projs)} projections; {len(hyps)} hypotheses", flush=True)
for h in hyps:
    sub = [l for l in lits if l != h]
    t = time.time()
    res = search(sub, projs, op, distinct=False, limit=3000)
    print(f"  drop {h[0]} = {h[1]}: counterexamples = {res if res == 'timeout' else len(res)}  ({time.time()-t:.0f}s)", flush=True)
