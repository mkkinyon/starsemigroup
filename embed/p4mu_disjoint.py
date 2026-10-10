"""Search the projection algebra of P_4/mu_1 (57 elements; has hexagon configurations with w != z)
for counterexamples to the two-disjoint-edges pattern {12,34} and to K_{2,2}, the 2-cycle+spare, etc."""
import sys, re, time, itertools
from pmon import Pn, projections, rank
from digraph import clause, parse_clause, search
n=4; P=Pn(n)
def kerpart(a): return tuple(sorted(tuple(x for x in b if x < n) for b in a if any(x < n for x in b)))
def cokerpart(a): return tuple(sorted(tuple(x - n for x in b if x >= n) for b in a if any(x >= n for x in b)))
def cls(a): return a if rank(a, n) >= 2 else ("low", kerpart(a), cokerpart(a))
projs=projections(n); reps={}
for p in projs:
    c=cls(p)
    if c not in reps or rank(p,n)<rank(reps[c],n): reps[c]=p
elems=sorted(reps, key=lambda c:(isinstance(c,tuple) and c[0]=="low", str(c))); idx={c:i for i,c in enumerate(elems)}; N=len(elems)
tab=[[idx[cls(P.prod(reps[d],reps[c],reps[d]))] for d in elems] for c in elems]
op=lambda x,y: tab[x][y]
print(f"P_4/mu_1: {N} projections", flush=True)
pats={"hexagon (sanity: should FAIL)":(3,[(i,j) for i in range(1,4) for j in range(1,4) if i!=j]),
      "2-cycle+spare {12,21}":(3,[(1,2),(2,1)]),
      "k=4 {12,34}":(4,[(1,2),(3,4)]), "k=4 K_{2,2}":(4,[(1,3),(1,4),(2,3),(2,4)]),
      "k=4 {12,32,14}":(4,[(1,2),(3,2),(1,4)])}
for name,(k,E) in pats.items():
    t=time.time(); res=search(parse_clause(clause(k,E)), range(N), op, distinct=False, limit=20000)
    print(f"  {name}: counterexamples = {res if res=='timeout' else len(res)} ({time.time()-t:.0f}s)", flush=True)
    if res and res!='timeout': print("     e.g.", res[0], flush=True)
