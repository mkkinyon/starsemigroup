import sys, time
from pmon import Pn, projections
from digraph import clause, parse_clause, search
pats={"k=4 {12,34}":[(1,2),(3,4)], "k=4 {12,32,14}":[(1,2),(3,2),(1,4)], "k=4 K_{2,2} {13,14,23,24}":[(1,3),(1,4),(2,3),(2,4)]}
n=int(sys.argv[1])
P=Pn(n); projs=projections(n); op=lambda x,y: P.prod(y,x,y)
print(f"P_{n}: {len(projs)} projections", flush=True)
for name,E in pats.items():
    t=time.time(); res=search(parse_clause(clause(4,E)), projs, op, distinct=False, limit=20000)
    print(f"  {name}: counterexamples = {res if res=='timeout' else len(res)} ({time.time()-t:.0f}s)", flush=True)
    if res and res!='timeout': print("     e.g.", res[0], flush=True)
