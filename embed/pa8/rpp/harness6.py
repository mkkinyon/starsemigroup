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
    G=join_classes([a,c],n); D=join_classes([b,c],n); XA=join_classes([x,a],n); YA=join_classes([y,a],n); XB=join_classes([x,b],n); YB=join_classes([y,b],n)
    cT=[E for E,t in top_blocks(c,n) if t]; Nx=[E for E,t in top_blocks(x,n) if not t]; Ny=[E for E,t in top_blocks(y,n) if not t]
    for C in cT:
        Gi=cls(G,C); Di=cls(D,C)
        Ai=next(A for A,t in top_blocks(a,n) if t and A<=Gi); Bi=next(B for B,t in top_blocks(b,n) if t and B<=Di)
        vis = C<=sx
        check('T1 C_i in Sx <=> A_i in supp u', vis == (Ai<=su), I)
        check('T1b C_i in Sx <=> A_i meets supp u', vis == bool(Ai&su), I)
        check('T2 C_i in Sx <=> B_i in Sy', vis == (Bi<=sy), I)
        check('T2b C_i in Sx <=> B_i in supp w', vis == (Bi<=sw), I)
        check('T2c C_i in Sx <=> C_i in Sy', vis == (C<=sy), I)
        check('T2d C_i in Sx <=> C_i in supp r', vis == (C<=sr), I)
        check('T2e C_i in Sx <=> C_i meets Sy', vis == bool(C&sy), I)
        check('T2f C_i in Sx <=> C_i in supp m', vis == (C<=sm), I)
        if not vis:
            check('T3 invisible: Gamma_i ∩ (Sx ∪ Sy) = ∅', not Gi&(sx|sy), I)
            check('T3b invisible: Delta_i ∩ (Sx ∪ Sy) = ∅', not Di&(sx|sy), I)
            check('T3c invisible: Gamma_i ∩ Sx = ∅', not Gi&sx, I)
            check('T3d invisible: Delta_i ∩ Sy = ∅', not Di&sy, I)
            check('T3e invisible: A_i ∩ Sy = ∅', not Ai&sy, I)
            check('T3f invisible: A_i ∩ Sx = ∅', not Ai&sx, I)
            check('T3g invisible: B_i ∩ Sx = ∅', not Bi&sx, I)
            check('T3h invisible: C_i is an N(y)-block or inside one', any(C<=N for N in Ny), I)
            check('T3i invisible: the N(x)-block M containing C_i is an N(y)-block', next(N for N in Nx if C<=N) in Ny, I)
            check('T3j invisible: Gamma_i ∪ Delta_i inside one class of ... rho_a_b', True, I)
        else:
            check('T4 visible: A_i meets Sy', bool(Ai&sy), I)
            check('T4b visible: A_i meets Sx', bool(Ai&sx), I)
            check('T4c visible: B_i meets Sx', bool(Bi&sx), I)
            check('T4d visible: C_i meets supp r', bool(C&sr), I)
            check('T4e visible: B_i meets supp r', bool(Bi&sr), I)
            check('T4f visible: A_i meets supp r', bool(Ai&sr), I)
            check('T4g visible: C_i ∩ Sy ⊆ supp r', (C&sy)<=sr, I)
            check('T4h visible: A_i ∩ Sy nonempty', bool(Ai&sy), I)
print(f"{len(S)} instances")
for k in sorted(fails): print(f"  FAIL {fails[k]:6d}  {k}")
pickle.dump(ex,open('harness6_ex.pkl','wb'))
