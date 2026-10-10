import sys, pickle, random
sys.path.insert(0,'/home/claude/pa8w/embed'); sys.path.insert(0,'/home/claude/pa8w/embed/pa8/rp')
from pmon import mul
from blocks import top_blocks, supp, join_classes
n=int(sys.argv[1]); inst=pickle.load(open(sys.argv[2],'rb')); memo={}
def m(p,q):
    k=(p,q)
    if k not in memo: memo[k]=mul(p,q,n)
    return memo[k]
th=lambda p,q: m(m(p,q),p)
S = inst if len(sys.argv)<4 else random.sample(inst,int(sys.argv[3]))
fails={}; ex={}
def check(name, cond, I):
    if not cond:
        fails[name]=fails.get(name,0)+1; ex.setdefault(name,I)
def cls(J,E): return next(K for K in J if E<=K)
for I in S:
    a,c,b,x,y=I; r=th(x,b); v=m(x,c); w=m(y,b); u=th(a,x); mm=m(x,y)
    sa,sb,sc,sx,sy,sr,sv,sw,su,sm=[supp(p,n) for p in (a,b,c,x,y,r,v,w,u,mm)]
    G=join_classes([a,c],n); D=join_classes([b,c],n); UW=join_classes([u,w],n); UV=join_classes([u,v],n); VW=join_classes([v,w],n)
    check('u~w', th(u,w)==u and th(w,u)==w, I)
    cT=[E for E,t in top_blocks(c,n) if t]; cN=[E for E,t in top_blocks(c,n) if not t]
    U=[E for E,t in top_blocks(u,n) if t]; W=[E for E,t in top_blocks(w,n) if t]; V=[E for E,t in top_blocks(v,n) if t]
    DT={cls(D,C) for C in cT}; GT={cls(G,C) for C in cT}
    def wl(K): return [l for l,Wl in enumerate(W) if K&Wl]
    def uj(K): return [j for j,Uj in enumerate(U) if K&Uj]
    for K in G:
        if K in GT: continue
        check('L1 a-free Gamma-class meets <=1 W_l', len(wl(K))<=1, I)
        # adjacent Delta-classes
        adjD={cls(D,E) for E in cN if E<=K}
        for Dc in adjD:
            if Dc in DT:
                Bp=next(B for B,t in top_blocks(b,n) if t and B<=Dc)
                if wl(K): check('L4 Gamma\' meets W_l => B_p in W_l', Bp<=W[wl(K)[0]], I)
            else:
                if wl(K) and uj(Dc): check('L3 Gamma\' W_l, Delta\' U_j => same UW-class', cls(UW,W[wl(K)[0]])==cls(UW,U[uj(Dc)[0]]), I)
        check('L6 a-free Gamma-class adjacent to a Delta-class meets supp w', not adjD or bool(wl(K)), I)
        check('L6b a-free Gamma-class adjacent to a T-Delta-class meets supp w', not (adjD&DT) or bool(wl(K)), I)
    for K in D:
        if K in DT: continue
        check('L2 T-free Delta-class meets <=1 U_j', len(uj(K))<=1, I)
        adjG={cls(G,E) for E in cN if E<=K}
        check('L7 T-free Delta-class adjacent to a Gamma-class meets supp u', not adjG or bool(uj(K)), I)
        for Gc in adjG:
            if Gc in GT:
                Ap=next(A for A,t in top_blocks(a,n) if t and A<=Gc)
                if uj(K): check('L5 Delta\' meets U_j => A_p in U_j', Ap<=U[uj(K)[0]], I)
print(f"{len(S)} instances")
for k in sorted(fails): print(f"  FAIL {fails[k]:6d}  {k}")
pickle.dump(ex,open('harness4_ex.pkl','wb'))
