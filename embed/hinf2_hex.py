import sys, re, time
from hinf2 import mul, elements
from digraph import clause, parse_clause
from termeval import make_eval
L=int(sys.argv[1]) if len(sys.argv)>1 else 6
E=elements(L); ev=make_eval(mul)
def run(name,k,Edges):
    lits=parse_clause(clause(k,Edges))
    hyps=[(l,r) for l,r,neg in lits if neg]; concl=[(l,r) for l,r,neg in lits if not neg]
    vars_=sorted({v for l,r,_ in lits for v in re.findall(r"[xy]\d",l+" "+r)})
    stage=[[] for _ in vars_]
    for l,r in hyps:
        vs=set(re.findall(r"[xy]\d",l+" "+r)); stage[max(vars_.index(v) for v in vs)].append((l,r))
    out=[]; t=time.time()
    def rec(kk,env):
        if kk==len(vars_):
            if all(ev(l,env)!=ev(r,env) for l,r in concl): out.append(dict(env))
            return
        for p in E:
            env[vars_[kk]]=p
            if all(ev(l,env)==ev(r,env) for l,r in stage[kk]): rec(kk+1,env)
        del env[vars_[kk]]
    rec(0,{})
    print(f"{name}: {len(out)} violations among levels <= {L} ({time.time()-t:.0f}s)")
    for o in out[:3]: print("   ", o)
run("hexagon",3,[(i,j) for i in range(1,4) for j in range(1,4) if i!=j])
run("triangle",3,[(1,2),(2,3),(3,1)])
run("directed 4-cycle",4,[(1,2),(2,3),(3,4),(4,1)])
run("double square",4,[(1,2),(2,1),(3,4),(4,3)])
run("2-cycle+spare",3,[(1,2),(2,1)])
run("path",3,[(1,2),(2,3)])
run("disjoint pairs",4,[(1,2),(3,4)])
run("cyclic octagon",4,[(i,j) for i in range(1,5) for j in range(1,5) if (i-j)%4 in (1,3)])
