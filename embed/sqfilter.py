import sys, time
from mace4parse import parse_models
from digraph import clause, parse_clause, search
TRI = parse_clause(clause(3, [(1,2),(2,3),(3,1)]))
HEX = parse_clause(clause(3, [(i,j) for i in range(1,4) for j in range(1,4) if i!=j]))
fn = sys.argv[1]
for k,(N,T,c) in enumerate(parse_models(open(fn).read()),1):
    op=lambda x,y:T[x][y]
    t=time.time()
    rt = search(TRI, range(N), op, distinct=False)
    rh = search(HEX, range(N), op, distinct=False)
    def fmt(r):
        if not r: return "holds"
        e=r[0]; return f"FAILS {[e['x1'],e['x2'],e['x3']]}|{[e['y1'],e['y2'],e['y3']]} w={T[e['x1']][e['x2']]} z={T[e['y1']][e['y2']]}"
    print(f"model {k} (size {N}): triangle {fmt(rt)}; hexagon {fmt(rh)}  [{time.time()-t:.0f}s]", flush=True)
