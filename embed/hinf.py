"""Abstract 'unrolled hexagon' H_inf: elements v_n (v in a1,a2,a3,b1,b2,b3; n>=0 level), m_i,n, W, Z.
x*y = theta_y(x).  Levelled elements: theta_y(x) keeps y's blocks from level max(lev y, lev x + shift(x->y)).
Only crossing pair: b3 (level k) <-> a1 (level k+1)."""
import itertools, re, sys
A=["a1","a2","a3"]; B=["b1","b2","b3"]
MATCH={("a1","b2"),("a3","b2"),("a3","b1"),("a2","b1"),("a2","b3")}   # levelwise matched pairs (both orders)
MATCH|={(v,u) for u,v in MATCH}
def idx(v): return int(v[1])
def rel(v): 
    """relatives: a_i ~ m_i, b_i ~ m_i; 'family' for the crossing shift: a1-family {a1,m1}, b3-family {b3,m3}"""
    return v
def shift(x,y):
    """level shift when x is sandwiched by y: y keeps level-k blocks iff x has a block in that class;
    crossing: b3-family level k pairs with a1-family level k+1."""
    fx = 'A1' if x in ("a1","m1") else ('B3' if x in ("b3","m3") else None)
    fy = 'A1' if y in ("a1","m1") else ('B3' if y in ("b3","m3") else None)
    if fx=='B3' and fy=='A1': return +1     # x=b3-fam at level n pairs with y=a1-fam at level n+1
    if fx=='A1' and fy=='B3': return -1
    return 0
def mul(x,y):
    """x*y = theta_y(x); elements are ('W',),('Z',),(name,level)"""
    if y[0] in ("W","Z"): return y                       # theta_W(x)=W
    if x[0]=="W":
        if y[0] in A: return x
        if y[0] in B: return ("m%d"%idx(y[0]), y[1])
        return y                                          # y = m_i: W*m = m
    if x[0]=="Z":
        if y[0] in B: return x
        if y[0] in A: return ("m%d"%idx(y[0]), y[1])
        return y
    u,n=x; v,m=y
    L=max(m, n+shift(u,v))
    if u==v: return (v,L)
    if (u,v) in MATCH: return (v,L)
    if u[0]=="m":
        i=idx(u)
        if v in ("a%d"%i,"b%d"%i): return (u,L)          # m_i <= a_i, b_i
        if v[0]=="m": return (v,L)                        # theta_{m_j}(m_i)=m_j
        if v in A: return ("W",)
        return ("Z",)
    if v[0]=="m":
        i=idx(v)
        if u in ("a%d"%i,"b%d"%i): return (v,L)
        return (v,L)                                      # theta_{m_i}(a_j)=m_i (m_i w m_i = m_i)
    # u,v vertices, not matched, not equal
    if u in A and v in A: return ("W",)
    if u in B and v in B: return ("Z",)
    if idx(u)==idx(v): return ("m%d"%idx(u), L)           # commuting pair a_i,b_i
    # remaining: crossing pair (a1,b3) either order
    if u=="b3" and v=="a1": return ("a1",L)               # theta_{a1_m}(b3_n)=a1_{max(m,n+1)}
    if u=="a1" and v=="b3": return ("b3",max(m,n-1))
    raise Exception((x,y))
def elements(L):
    return [("W",),("Z",)]+[(v,n) for n in range(L+1) for v in A+B+["m1","m2","m3"]]
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
