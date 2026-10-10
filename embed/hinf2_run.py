import sys, re, time
from hinf2 import mul, elements, ev, AX
import itertools
from digraph import clause, parse_clause
L=int(sys.argv[1]); which=sys.argv[2]
E=elements(L)
if which=="axioms":
    for a in AX:
        l,r=a.split("="); vs=sorted(set(re.findall(r"[xyz]",a)))
        bad=next((c for c in itertools.product(E,repeat=len(vs)) if ev(l,dict(zip(vs,c)))!=ev(r,dict(zip(vs,c)))),None)
        print(a, "OK" if bad is None else f"FAILS at {bad}", flush=True)
else:
    pats={"hexagon":(3,[(i,j) for i in range(1,4) for j in range(1,4) if i!=j]),
          "directed 4-cycle":(4,[(1,2),(2,3),(3,4),(4,1)]), "double square":(4,[(1,2),(2,1),(3,4),(4,3)])}
    k,Edges=pats[which]
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
    print(f"{which}: {len(out)} violations among levels <= {L} ({time.time()-t:.0f}s)", flush=True)
    for o in out[:3]: print("   ", o)
