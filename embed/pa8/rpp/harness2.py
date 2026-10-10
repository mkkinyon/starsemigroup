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
    sa,sb,sc,sx,sy,sr,sv,sw,su=[supp(p,n) for p in (a,b,c,x,y,r,v,w,u)]
    G=join_classes([a,c],n); D=join_classes([b,c],n)
    XB=join_classes([x,b],n); YA=join_classes([y,a],n); YC=join_classes([y,c],n); YB=join_classes([y,b],n); XC=join_classes([x,c],n); XA=join_classes([x,a],n)
    VW=join_classes([v,w],n); UV=join_classes([u,v],n)
    cT=[E for E,t in top_blocks(c,n) if t]; cN=[E for E,t in top_blocks(c,n) if not t]
    DT={cls(D,C) for C in cT}; GT={cls(G,C) for C in cT}
    Ny=[E for E,t in top_blocks(y,n) if not t]; Nx=[E for E,t in top_blocks(x,n) if not t]
    # I2: in an a-free Gamma-class, all c-blocks lying in T-Delta-classes lie in the same one
    for K in G:
        if K&sa: continue
        ds={cls(D,E) for E in cN if E<=K and cls(D,E) in DT}
        check('I2 a-free Gamma-class meets <=1 Delta_i', len(ds)<=1, I)
        # which classes of other joins contain K?
        check('I4 a-free Gamma-class inside one class of VW', any(K<=L for L in VW), I)
        check('I5 a-free Gamma-class inside one class of XB', any(K<=L for L in XB), I)
        check('I6 a-free Gamma-class inside one class of YB', any(K<=L for L in YB), I)
        check('I7 a-free Gamma-class inside one class of YC', any(K<=L for L in YC), I)
        check('I8 a-free Gamma-class is b-free or meets supp b in ...', True, I)
    for K in D:
        if K in DT: continue
        gs={cls(G,E) for E in cN if E<=K and cls(G,E) in GT}
        check('I3 T-free Delta-class meets <=1 Gamma_i', len(gs)<=1, I)
    # Delta_i inside a class of XB? YA? 
    for C in cT:
        Di=cls(D,C); Gi=cls(G,C)
        check('I9 Delta_i inside one class of XB', any(Di<=L for L in XB), I)
        check('I10 Delta_i inside one class of YC', any(Di<=L for L in YC), I)
        check('I11 Delta_i inside one class of YA', any(Di<=L for L in YA), I)
        check('I12 Gamma_i inside one class of YA', any(Gi<=L for L in YA), I)
        check('I13 Gamma_i inside one class of YC', any(Gi<=L for L in YC), I)
        check('I14 Gamma_i inside one class of XB', any(Gi<=L for L in XB), I)
        check('I15 Delta_i inside one class of XA', any(Di<=L for L in XA), I)
        # N(c)-blocks of Delta_i inside Sy: are they N(x)? inside Sx: are they N(y)?
        for E in cN:
            if not E<=Di: continue
            if E<=sy: check('I16 E in Delta_i, E in Sy => E is N(x)', E in Nx, I)
            if E<=sx: check('I17 E in Delta_i, E in Sx => E is N(y)', E in Ny, I)
            if E<=sx: check('I17b E in Delta_i, E in Sx => E inside an N(y)-block', any(E<=N for N in Ny), I)
            if E<=sx: check('I17c E in Delta_i, E in Sx => E ∩ Sy = ∅', not E&sy, I)
            if E<=sy: check('I16c E in Delta_i, E in Sy => E ∩ Sx = ∅', not E&sx, I)
print(f"{len(S)} instances")
for k in sorted(fails): print(f"  FAIL {fails[k]:6d}  {k}")
pickle.dump(ex,open('harness2_ex.pkl','wb'))
