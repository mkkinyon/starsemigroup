"""Projection algebra of P_5/mu_1 (303 elements; violates the hexagon condition): search for
counterexamples to the two-disjoint-edges pattern {12,34}."""
import sys, time, pickle
from pmon import Pn, projections, rank
from digraph import clause, parse_clause, search
n=5; P=Pn(n)
def kerpart(a): return tuple(sorted(tuple(x for x in b if x < n) for b in a if any(x < n for x in b)))
def cokerpart(a): return tuple(sorted(tuple(x - n for x in b if x >= n) for b in a if any(x >= n for x in b)))
def cls(a): return a if rank(a, n) >= 2 else ("low", kerpart(a), cokerpart(a))
t=time.time()
projs=projections(n); reps={}
for p in projs:
    c=cls(p)
    if c not in reps or rank(p,n)<rank(reps[c],n): reps[c]=p
elems=sorted(reps, key=lambda c:(isinstance(c,tuple) and c[0]=="low", str(c))); idx={c:i for i,c in enumerate(elems)}; N=len(elems)
tab=[[idx[cls(P.rawmul(P.rawmul(reps[d],reps[c]),reps[d]))] if hasattr(P,'rawmul') else idx[cls(P.prod(reps[d],reps[c],reps[d]))] for d in elems] for c in elems]
pickle.dump(tab, open("p5mu_table.pkl","wb"))
print(f"P_5/mu_1: {N} projections, table in {time.time()-t:.0f}s", flush=True)
op=lambda x,y: tab[x][y]
for name,(k,E) in {"k=4 {12,34}":(4,[(1,2),(3,4)]), "k=4 K_{2,2}":(4,[(1,3),(1,4),(2,3),(2,4)])}.items():
    t=time.time(); res=search(parse_clause(clause(k,E)), range(N), op, distinct=False, limit=200000)
    print(f"  {name}: counterexamples = {res if res=='timeout' else len(res)} ({time.time()-t:.0f}s)", flush=True)
    if res and res!='timeout': print("     e.g.", res[0], flush=True)
