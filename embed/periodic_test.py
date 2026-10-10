import random, itertools, re, sys
from periodic import *
from pmon import Pn, projections
from termeval import make_eval
m=int(sys.argv[1]) if len(sys.argv)>1 else 3
elems=all_elements(m,(-1,0,1),(0,1,2)); alg=Alg(m,elems); N=len(elems)
print("elements:",N)
# 1. column elements vs P_m
P=Pn(m); projs=projections(m)
def to_periodic(p):
    # p: partition of [0..2m-1]; blocks with i<m upper; T-block if it meets both rows
    types=[]
    for b in p:
        up=[x for x in b if x<m]
        if not up: continue
        lab='T' if any(x>=m for x in b) else 'N'
        types.append(normalise_type(up,1,{i:0 for i in up},lab))
    return make_element(types)
col={p:to_periodic(p) for p in projs}
bad=0
for p in projs:
    for q in projs:
        r=P.prod(q,p,q)   # p*q = q p q
        e=theta(col[q],col[p],m)
        if e!=col[r]: bad+=1
print("column elements agree with P_%d:"%m, bad==0)
# 2. axioms on random triples (all elements if small)
ev=make_eval(alg.mul)
AX=["x*x=x","(y*x)*x=y*x","(x*y)*x=y*x","((z*x)*y)*x=z*(y*x)","(((z*x)*y)*x)*y=(z*x)*y"]
random.seed(0)
for a in AX:
    l,r=a.split("="); vs=sorted(set(re.findall(r"[xyz]",a)))
    fails=0
    for _ in range(20000):
        env={v:random.randrange(N) for v in vs}
        if ev(l,env)!=ev(r,env): fails+=1
    print(a, "fails:",fails)
# 3. Q1 on random pairs with a common lower bound
le=lambda x,y: alg.mul(x,y)==x
fails=0; tested=0
for _ in range(20000):
    x,y,r=random.randrange(N),random.randrange(N),random.randrange(N)
    if le(r,x) and le(r,y):
        tested+=1
        if alg.mul(x,y)!=alg.mul(y,x): fails+=1
print("Q1: tested",tested,"fails",fails)
