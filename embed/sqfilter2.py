import sys, time
from mace4parse import parse_models
from digraph import clause, parse_clause, search
from walk_hex import hex_eqs
TRI = parse_clause(clause(3, [(1,2),(2,3),(3,1)]))
HEX = parse_clause(clause(3, [(i,j) for i in range(1,4) for j in range(1,4) if i!=j]))
def walk_hex(T,c):
    """walk a1 -> theta_{b3} -> theta_{a2} -> theta_{b1} -> theta_{a3} -> theta_{b2} -> theta_{a1};
    if closed, test whether {a1,a2,p | b1,b2,q} (p=a3 b1 a3, q=b3 a1 b3) is a hexagon with w!=z."""
    cur=c['a1']; seq=[cur]
    for s in ['b3','a2','b1','a3','b2','a1']:
        cur=T[cur][c[s]]; seq.append(cur)
    if cur!=c['a1']: return False
    A={1:c['a1'],2:c['a2'],3:seq[4]}; B={1:c['b1'],2:c['b2'],3:seq[1]}
    m=lambda p,q: T[q][p]==p and T[p][q]==q
    for i in (1,2,3):
        if T[A[i]][B[i]]!=T[B[i]][A[i]]: return False
        for j in (1,2,3):
            if i!=j and (not m(A[i],B[j]) or T[A[i]][A[j]]!=c['cw'] or T[B[i]][B[j]]!=c['cz']): return False
    return True
fn=sys.argv[1]; t0=time.time(); n=0; quick=0; surv=[]
for k,(N,T,c) in enumerate(parse_models(open(fn).read()),1):
    n+=1
    if walk_hex(T,c): quick+=1; continue
    op=lambda x,y:T[x][y]
    rt=search(TRI, range(N), op, distinct=False); rh=search(HEX, range(N), op, distinct=False)
    print(f"model {k}: walk test inconclusive; triangle {'holds' if not rt else 'FAILS'}; hexagon {'holds' if not rh else 'FAILS'}", flush=True)
    if not rt or not rh: surv.append(k)
print(f"{n} models; {quick} disposed of by the closed walk; survivors (triangle or hexagon holds): {surv}  [{time.time()-t0:.0f}s]")
