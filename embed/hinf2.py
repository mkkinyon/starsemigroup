"""Abstract 'unrolled hexagon' H_inf, version 2: low elements W,Z,m1,m2,m3 (absorbing, as in P(Q_0)),
chains e_{i,n}, f_{j,n} (n>=0).  x*y = theta_y(x)."""
import itertools, re, sys
LOW=["W","Z","m1","m2","m3"]
MATCH={(1,2),(3,2),(3,1),(2,1),(2,3)}     # (i,j): e_i |><| f_j levelwise; crossing pair (1,3): f_{3,n} <-> e_{1,n+1}
def mul(x,y):
    if y[0] in LOW: return y
    if x[0] in LOW:
        l=x[0]; v,m=y; i=int(v[1])
        if v[0]=="e":
            if l=="W": return x
            if l=="Z": return ("m%d"%i,)
            return x if l=="m%d"%i else ("W",)
        else:
            if l=="Z": return x
            if l=="W": return ("m%d"%i,)
            return x if l=="m%d"%i else ("Z",)
    u,n=x; v,m=y; i=int(u[1]); j=int(v[1])
    if u[0]==v[0]:
        if i==j: return (v,max(n,m))
        return ("W",) if u[0]=="e" else ("Z",)
    if i==j: return ("m%d"%i,)
    if u[0]=="e":   # x=e_i,n sandwiched by f_j,m
        if (i,j) in MATCH: return (v,max(n,m))
        return (v,max(m,n-1))          # (1,3): e_{1,n} * f_{3,m} = f_{3,max(m,n-1)}
    else:           # x=f_j,n sandwiched by e_i,m  (u=f_i, v=e_j)
        if (j,i) in MATCH: return (v,max(n,m))
        return (v,max(m,n+1))          # f_{3,n} * e_{1,m} = e_{1,max(m,n+1)}
def elements(L):
    return [(l,) for l in LOW]+[(v,n) for n in range(L+1) for v in ["e1","e2","e3","f1","f2","f3"]]
AX=["x*x=x","(y*x)*x=y*x","(x*y)*x=y*x","((z*x)*y)*x=z*(y*x)","(((z*x)*y)*x)*y=(z*x)*y"]
from termeval import make_eval
ev=make_eval(mul)
if __name__=="__main__":
    L=int(sys.argv[1]) if len(sys.argv)>1 else 4
    E=elements(L)
    for a in AX:
        l,r=a.split("="); vs=sorted(set(re.findall(r"[xyz]",a)))
        bad=[c for c in itertools.product(E,repeat=len(vs)) if ev(l,dict(zip(vs,c)))!=ev(r,dict(zip(vs,c)))]
        print(a, "OK" if not bad else f"FAILS {len(bad)} e.g. {bad[0]} -> {ev(l,dict(zip(vs,bad[0])))} vs {ev(r,dict(zip(vs,bad[0])))}")
