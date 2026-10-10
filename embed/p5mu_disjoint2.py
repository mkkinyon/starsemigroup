import pickle, time
from digraph import clause, parse_clause, search
tab=pickle.load(open("p5mu_table.pkl","rb")); N=len(tab); op=lambda x,y: tab[x][y]
print(f"P_5/mu_1: {N} projections", flush=True)
for name,(k,E) in {"k=4 {12,34}":(4,[(1,2),(3,4)]), "k=4 K_{2,2}":(4,[(1,3),(1,4),(2,3),(2,4)])}.items():
    t=time.time(); res=search(parse_clause(clause(k,E)), range(N), op, distinct=False, limit=400000)
    print(f"  {name}: counterexamples = {res if res=='timeout' else len(res)} ({time.time()-t:.0f}s)", flush=True)
    if res and res!='timeout': print("     e.g.", res[0], flush=True)
