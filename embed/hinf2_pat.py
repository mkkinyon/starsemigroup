import sys, re, time
from hinf2 import mul, elements, ev
from digraph import clause, parse_clause
L=int(sys.argv[1]); E=elements(L)
pats={"k4 disjoint {12,34}":(4,[(1,2),(3,4)]), "k4 path {12,23}":(4,[(1,2),(2,3)]), "k4 triangle+isolated":(4,[(1,2),(2,3),(3,1)]),
      "k4 2-cycle {12,21}":(4,[(1,2),(2,1)]), "k4 K22":(4,[(1,3),(1,4),(2,3),(2,4)]), "k4 hexagon+isolated":(4,[(i,j) for i in range(1,4) for j in range(1,4) if i!=j])}
for name,(k,Edges) in pats.items():
    lits=parse_clause(clause(k,Edges))
    hyps=[(l,r) for l,r,neg in lits if neg]; concl=[(l,r) for l,r,neg in lits if not neg]
    vars_=sorted({v for l,r,_ in lits for v in re.findall(r"[xy]\d",l+" "+r)})
    stage=[[] for _ in vars_]
    for l,r in hyps:
        vs=set(re.findall(r"[xy]\d",l+" "+r)); stage[max(vars_.index(v) for v in vs)].append((l,r))
    out=[]; t=time.time()
    def rec(kk,env):
        if len(out)>3: return
        if kk==len(vars_):
            if all(ev(l,env)!=ev(r,env) for l,r in concl): out.append(dict(env))
            return
        for p in E:
            env[vars_[kk]]=p
            if all(ev(l,env)==ev(r,env) for l,r in stage[kk]): rec(kk+1,env)
        del env[vars_[kk]]
    rec(0,{})
    print(f"{name}: {'NO violation' if not out else 'violated'} (levels <= {L}, {time.time()-t:.0f}s)", flush=True)
    for o in out[:2]: print("   ",o)
