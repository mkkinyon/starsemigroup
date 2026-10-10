"""2-cycle-plus-spare hypotheses in P_n: does a3 z a3 = m3 (and b3 w b3 = m3) follow?"""
import sys, time
from pmon import Pn, projections
from digraph import clause, parse_clause, search
E=[(1,2),(2,1)]
lits=[l for l in parse_clause(clause(3,E)) if l[2]]      # hypotheses only
for n in range(2, int(sys.argv[1])+1 if len(sys.argv)>1 else 4):
    P=Pn(n); projs=projections(n); op=lambda x,y,P=P: P.prod(y,x,y)
    for name,(l,r) in {"a3 z a3 = m3":("(y1 * y2) * x3","x3 * y3"), "b3 w b3 = m3":("(x1 * x2) * y3","x3 * y3"),
                       "w = z":("x1 * x2","y1 * y2")}.items():
        t=time.time()
        res=search(lits+[(l,r,False)], projs, op, distinct=False, limit=3000)
        print(f"P_{n}: {name}: counterexamples = {res if res=='timeout' else len(res)} ({time.time()-t:.0f}s)", flush=True)
        if res and res!='timeout': print("   e.g.", res[0])
