"""Unrolled 2k-gon U_k: low W,Z,m_1..m_k; chains e_{i,n}, f_{j,n}, i,j in [k].
e_i |><| f_j levelwise for j = i+-1 (mod k), except the crossing pair (e_1, f_k): f_{k,n} <-> e_{1,n+1}.
Non-adjacent (i,j), i != j: rule ANTI: 'low' (e_i*f_j = Z, f_j*e_i = W) or 'oneside'."""
import itertools, re, sys
K=4; ANTI="low"
def setup(k, anti="low"):
    global K, ANTI; K=k; ANTI=anti
def adj(i,j): return (j-i)%K in (1,K-1)
def mul(x,y):
    if len(y)==1: return y                      # theta_low(x) = low
    if len(x)==1:
        l=x[0]; v,m=y; i=int(v[1:])
        if v[0]=="e":
            if l=="W": return x
            if l=="Z": return ("m%d"%i,)
            return x if l=="m%d"%i else ("W",)
        else:
            if l=="Z": return x
            if l=="W": return ("m%d"%i,)
            return x if l=="m%d"%i else ("Z",)
    u,n=x; v,m=y; i=int(u[1:]); j=int(v[1:])
    if u[0]==v[0]:
        if i==j: return (v,max(n,m))
        return ("W",) if u[0]=="e" else ("Z",)
    if i==j: return ("m%d"%i,)
    if u[0]=="e":                               # e_i,n sandwiched by f_j,m
        if adj(i,j):
            if (i,j)==(1,K): return (v,max(m,n-1))
            return (v,max(n,m))
        return ("Z",) if ANTI=="low" else (v,max(m,n))
    else:                                       # f_i,n sandwiched by e_j,m
        if adj(i,j):
            if (j,i)==(1,K): return (v,max(m,n+1))
            return (v,max(n,m))
        return ("W",) if ANTI=="low" else (v,max(m,n+1))
def elements(L):
    return [("W",),("Z",)]+[("m%d"%i,) for i in range(1,K+1)]+[(v,n) for n in range(L+1) for i in range(1,K+1) for v in ("e%d"%i,"f%d"%i)]
AX=["x*x=x","(y*x)*x=y*x","(x*y)*x=y*x","((z*x)*y)*x=z*(y*x)","(((z*x)*y)*x)*y=(z*x)*y"]
from termeval import make_eval
ev=make_eval(mul)
def check_axioms(L):
    E=elements(L); res={}
    for a in AX:
        l,r=a.split("="); vs=sorted(set(re.findall(r"[xyz]",a)))
        bad=next((c for c in itertools.product(E,repeat=len(vs)) if ev(l,dict(zip(vs,c)))!=ev(r,dict(zip(vs,c)))),None)
        res[a]="OK" if bad is None else f"FAILS at {bad}: {ev(l,dict(zip(vs,bad)))} vs {ev(r,dict(zip(vs,bad)))}"
    return res
if __name__=="__main__":
    k=int(sys.argv[1]); anti=sys.argv[2]; L=int(sys.argv[3])
    setup(k,anti)
    for a,r in check_axioms(L).items(): print(a,r)
