import sys, re, time
from hinf2 import mul, elements, ev
from digraph import clause, parse_clause
L=int(sys.argv[1]); E=elements(L)
lits=parse_clause(clause(4,[(1,2)]))
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
print(f"k=4 single edge: {len(out)} violations among levels <= {L} ({time.time()-t:.0f}s)")
for o in out[:3]: print("  ",o)
